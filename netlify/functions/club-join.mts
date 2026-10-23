import type { Context, Config } from "@netlify/functions";
import {
  getClub, putClub, store, isProduction, isFree, normSlug, slugProblem, normCodePrefix, codeProblem,
  CODE_SUFFIX, TERMS_VERSION, SITE, html,
} from "../lib/clubs.mts";
import { clubPage, joinPage, donePage, notFound } from "../lib/pages.mts";

/**
 * Club affiliate sign-up.
 *   GET  /club-preview/:token  private preview of the club's page (linked from the outreach email)
 *   GET  /join/:token          four-step sign-up form
 *   GET  /api/club-check       live slug / code availability for the form
 *   POST /api/club-register    completes sign-up: claims slug + code, records agreement,
 *                              opts into MailerLite, flips the club to active (page goes live)
 *
 * Sign-up is always open on previews/branch deploys. In production it stays closed until
 * the env var CLUB_REGISTRATION_OPEN=true (set once counsel finalises the agreement).
 */

const registrationOpen = (ctx: Context) =>
  !isProduction(ctx) || Netlify.env.get("CLUB_REGISTRATION_OPEN") === "true";

const ML = "https://connect.mailerlite.com/api";
const ML_GROUP = "Pickle Tours — Club Affiliates";

async function ml(path: string, init: RequestInit = {}) {
  const key = Netlify.env.get("MAILERLITE_API_KEY");
  if (!key) throw new Error("MAILERLITE_API_KEY not set");
  const res = await fetch(ML + path, {
    ...init,
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json", Accept: "application/json" },
  });
  if (!res.ok) throw new Error(`MailerLite ${path} ${res.status} ${(await res.text()).slice(0, 300)}`);
  return res.json();
}

/** Find-or-create the club partner group, and the referral_club field the club pages tag members with. */
async function mailerliteSetup(): Promise<string> {
  const fields = await ml(`/fields?filter[keyword]=referral_club&limit=100`);
  if (!fields.data?.some((f: any) => f.key === "referral_club")) {
    await ml(`/fields`, { method: "POST", body: JSON.stringify({ name: "Referral Club", type: "text" }) });
  }
  const groups = await ml(`/groups?filter[name]=${encodeURIComponent(ML_GROUP)}&limit=50`);
  const g = groups.data?.find((x: any) => x.name === ML_GROUP);
  if (g) return g.id;
  return (await ml(`/groups`, { method: "POST", body: JSON.stringify({ name: ML_GROUP }) })).data.id;
}

async function check(ctx: Context, url: URL) {
  const kind = url.searchParams.get("kind");
  const token = url.searchParams.get("token") ?? "";
  const raw = url.searchParams.get("value") ?? "";
  const json = (o: object) => Response.json(o, { headers: { "Cache-Control": "no-store" } });
  if (kind === "slug") {
    const v = normSlug(raw);
    const p = slugProblem(v);
    if (p) return json({ ok: false, value: v, message: p });
    return json((await isFree(ctx, "slug", v, token)) ? { ok: true, value: v } : { ok: false, value: v, message: "That address is taken. Try another." });
  }
  if (kind === "code") {
    const pre = normCodePrefix(raw);
    const p = codeProblem(pre);
    const v = pre + CODE_SUFFIX;
    if (p) return json({ ok: false, value: v, message: p });
    return json((await isFree(ctx, "code", v, token)) ? { ok: true, value: v } : { ok: false, value: v, message: `${v} is taken. Try another.` });
  }
  return json({ ok: false, message: "bad request" });
}

async function register(req: Request, ctx: Context) {
  const form = await req.formData().catch(() => null);
  if (!form) return html(notFound(), 400);
  const s = (k: string, max = 200) => String(form.get(k) ?? "").trim().slice(0, max);
  const club = await getClub(ctx, s("token", 64));
  if (!club || club.status === "declined") return html(notFound(), 404);
  if (!registrationOpen(ctx)) return html(joinPage(club, false), 403);

  const fail = (msg: string) => html(joinPage({ ...club, suggested_slug: s("slug"), suggested_code: s("code") + CODE_SUFFIX }, true, msg), 422);
  const slug = normSlug(s("slug", 60));
  const pre = normCodePrefix(s("code", 30));
  const code = pre + CODE_SUFFIX;
  const signer_name = s("signer_name", 120), signer_title = s("signer_title", 120);
  const signer_email = s("signer_email", 200).toLowerCase();
  const sp = slugProblem(slug); if (sp) return fail(`Page address: ${sp}`);
  const cp = codeProblem(pre); if (cp) return fail(`Members' code: ${cp}`);
  if (!signer_name || !signer_title) return fail("Please add your name and title.");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(signer_email)) return fail("Please add a valid email.");
  if (s("agree") !== "yes") return fail("Please agree to the Club Referral Agreement.");
  if (!(await isFree(ctx, "slug", slug, club.token))) return fail("That page address was just taken. Try another.");
  if (!(await isFree(ctx, "code", code, club.token))) return fail(`${code} was just taken. Try another.`);

  const st = store(ctx);
  const prev = club.registration;
  if (prev && prev.slug !== slug) await st.delete(`slug/${prev.slug}`);
  if (prev && prev.code !== code) await st.delete(`code/${prev.code}`);
  await st.set(`slug/${slug}`, club.token);
  await st.set(`code/${code}`, club.token);

  const optin = s("optin") === "yes";
  club.registration = {
    slug, code, terms_version: TERMS_VERSION, signer_name, signer_title, signer_email,
    agreed_at: new Date().toISOString(), agreed_ip: req.headers.get("x-nf-client-connection-ip") ?? undefined,
    mailerlite_optin: optin,
  };
  club.status = "active";

  // MailerLite: always make sure the referral field exists (club pages tag waitlist signups with it);
  // add the signer to the partner group only if they opted in. Failure never blocks going live.
  try {
    const gid = await mailerliteSetup();
    if (optin) {
      await ml(`/subscribers`, { method: "POST", body: JSON.stringify({
        email: signer_email, groups: [gid], status: "active",
        fields: { name: signer_name, company: club.club_name, referral_club: code },
      }) });
    }
    club.registration.mailerlite_ok = true;
  } catch (e) {
    console.error("club-register: MailerLite", e);
    club.registration.mailerlite_ok = false;
  }
  await putClub(ctx, club);

  const base = isProduction(ctx) ? SITE : new URL(req.url).origin;
  return html(donePage(club, `${base}/${slug}`));
}

export default async (req: Request, ctx: Context) => {
  const url = new URL(req.url);
  const p = url.pathname;
  if (p === "/api/club-check") return check(ctx, url);
  if (p === "/api/club-register") return req.method === "POST" ? register(req, ctx) : html(notFound(), 405);

  const token = ctx.params?.token ?? "";
  const club = await getClub(ctx, token);
  if (!club || club.status === "declined") return html(notFound(), 404);
  const noindex = { "X-Robots-Tag": "noindex, nofollow" };
  if (p.startsWith("/club-preview/")) return html(clubPage(club, "preview", `/join/${club.token}`), 200, noindex);
  return html(joinPage(club, registrationOpen(ctx)), 200, noindex);
};

export const config: Config = {
  path: ["/club-preview/:token", "/join/:token", "/api/club-check", "/api/club-register"],
};
