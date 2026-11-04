import type { Context, Config } from "@netlify/functions";
import {
  ClubRecord, putClub, store, isProduction, isFree, slugProblem, codeProblem, normCodePrefix,
  CODE_SUFFIX, TERMS_VERSION, html, STATES, BLOCKED_STATES,
} from "../lib/clubs.mts";
import { registerPage, registeredPage, notFound } from "../lib/pages.mts";

/**
 * Self-serve club registration (step B of club onboarding).
 *
 *   Step A  Club or pro joins the "Pickle Dot Tours — Club Affiliates" MailerLite list; the welcome
 *           email's "Register for referral commission" button links to /clubs/register?email=<their email>.
 *   Step B  GET /clubs/register shows the form; POST /api/club-signup saves it:
 *             - one short name makes both the link (route66pickleballtour.com/<name>) and the code (<NAME>500)
 *             - club address and contact details (they become the Tour Amigo partner record)
 *             - agreement to the Club Referral Agreement (signer, title, time, IP, version)
 *           The club is saved as active (its link works), the MailerLite subscriber is tagged with the code,
 *           a card opens on Trello "Club Affiliates → Active" and Mike gets an email.
 *   Step C  Claude adds the partner and creates the code in Tour Amigo (club-partner-onboarding skill), then
 *           moves the card to Onboarded; the Mac sync (~/dev/pickle-ops/clubs/clubs.py) then emails the kit.
 *
 * States in BLOCKED_STATES get a "not available in your state yet" page instead of the form.
 */

const registrationOpen = (ctx: Context) =>
  !isProduction(ctx) || Netlify.env.get("CLUB_REGISTRATION_OPEN") === "true";

const ML = "https://connect.mailerlite.com/api";
const ML_GROUP = "Pickle Dot Tours — Club Affiliates";
const TRELLO_ACTIVE_LIST = "6adae72f79e9a73bc71cd928"; // Club Affiliates → Active

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

async function mlGroupId(): Promise<string> {
  const groups = await ml(`/groups?filter[name]=${encodeURIComponent(ML_GROUP)}&limit=50`);
  const g = groups.data?.find((x: any) => x.name === ML_GROUP);
  if (g) return g.id;
  return (await ml(`/groups`, { method: "POST", body: JSON.stringify({ name: ML_GROUP }) })).data.id;
}

async function ensureField() {
  const fields = await ml(`/fields?filter[keyword]=referral_club&limit=100`);
  if (!fields.data?.some((f: any) => f.key === "referral_club")) {
    await ml(`/fields`, { method: "POST", body: JSON.stringify({ name: "Referral Club", type: "text" }) });
  }
}

export interface Signup {
  club_name: string; short: string; contact_name: string; contact_title: string; email: string; phone: string;
  address_1: string; city: string; state: string; zip: string; website: string;
}

const blank = (email = ""): Signup => ({
  club_name: "", short: "", contact_name: "", contact_title: "", email, phone: "",
  address_1: "", city: "", state: "", zip: "", website: "",
});

async function submit(req: Request, ctx: Context) {
  const form = await req.formData().catch(() => null);
  if (!form) return html(notFound(), 400);
  if (String(form.get("bot-field") ?? "")) return html(registeredPage(), 200); // honeypot
  const s = (k: string, max = 200) => String(form.get(k) ?? "").trim().slice(0, max);
  const v: Signup = {
    club_name: s("club_name", 120), short: s("short", 30), contact_name: s("contact_name", 120),
    contact_title: s("contact_title", 120), email: s("email", 200).toLowerCase(), phone: s("phone", 40),
    address_1: s("address_1", 200), city: s("city", 80), state: s("state", 2).toUpperCase(), zip: s("zip", 10),
    website: s("website", 200),
  };
  const open = registrationOpen(ctx);
  if (!open) return html(registerPage(v, false), 403);
  const fail = (msg: string) => html(registerPage(v, true, msg), 422);

  if (!v.club_name) return fail("Please add your club's name.");
  if (!STATES[v.state]) return fail("Please choose your club's state.");
  if (BLOCKED_STATES.has(v.state)) return html(registerPage(v, true, undefined, true), 200);
  const pre = normCodePrefix(v.short);
  const slug = pre.toLowerCase();
  const code = pre + CODE_SUFFIX;
  const cp = codeProblem(pre) ?? slugProblem(slug);
  if (cp) return fail(`Short name: ${cp}`);
  if (!v.contact_name || !v.contact_title) return fail("Please add your name and title.");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.email)) return fail("Please add a valid email.");
  if (v.phone.replace(/\D/g, "").length < 10) return fail("Please add a phone number with area code.");
  if (!v.address_1 || !v.city || !/^\d{5}(-\d{4})?$/.test(v.zip)) return fail("Please add the club's street address, city and ZIP.");
  if (s("agree") !== "yes") return fail("Please agree to the Club Referral Agreement.");
  if (!(await isFree(ctx, "slug", slug)) || !(await isFree(ctx, "code", code))) {
    return fail(`${pre} is already taken by another club. Try another short name.`);
  }

  const token = [...crypto.getRandomValues(new Uint8Array(16))].map((b) => b.toString(16).padStart(2, "0")).join("");
  const now = new Date().toISOString();
  const website = v.website && !/^https?:\/\//i.test(v.website) ? `https://${v.website}` : v.website;
  const rec: ClubRecord = {
    token, club_name: v.club_name, city: v.city, state: v.state,
    contact_name: v.contact_name, contact_email: v.email, website: website || undefined,
    suggested_slug: slug, suggested_code: code, status: "active", created_at: now, updated_at: now,
    address_1: v.address_1, zip: v.zip, phone: v.phone, contact_title: v.contact_title,
    meta: { source: "self-signup" },
    registration: {
      slug, code, terms_version: TERMS_VERSION, signer_name: v.contact_name, signer_title: v.contact_title,
      signer_email: v.email, agreed_at: now, agreed_ip: req.headers.get("x-nf-client-connection-ip") ?? undefined,
      mailerlite_optin: true,
    },
  };
  const st = store(ctx);
  await st.set(`slug/${slug}`, token);
  await st.set(`code/${code}`, token);

  // MailerLite: they joined the list in step A; tag them with the code (re-adds to the group if they came another way).
  try {
    await ensureField();
    await ml(`/subscribers`, { method: "POST", body: JSON.stringify({
      email: v.email, groups: [await mlGroupId()],
      fields: { name: v.contact_name, company: v.club_name, phone: v.phone, referral_club: code },
    }) });
    rec.registration!.mailerlite_ok = true;
  } catch (e) {
    console.error("club-signup: MailerLite", e);
    rec.registration!.mailerlite_ok = false;
  }

  // Trello card on Club Affiliates → Active. Everything Tour Amigo needs is on it.
  const tk = Netlify.env.get("TRELLO_KEY"), tt = Netlify.env.get("TRELLO_TOKEN");
  const desc = [
    `**${v.club_name}** · ${v.city}, ${v.state} · self-signup ${now.slice(0, 10)}`,
    ``,
    `**Link:** route66pickleballtour.com/${slug}`,
    `**Code to create in Tour Amigo:** ${code} ($500 off per person)`,
    ``,
    `**Contact:** ${v.contact_name}, ${v.contact_title}`,
    `**Email:** ${v.email}`,
    `**Phone:** ${v.phone}`,
    `**Address:** ${v.address_1}, ${v.city}, ${v.state} ${v.zip}`,
    `**Website:** ${website || "(none given)"}`,
    ``,
    `Agreed to the Club Referral Agreement v${TERMS_VERSION} on ${now.slice(0, 16).replace("T", " ")} UTC.`,
    `MailerLite tag: ${rec.registration!.mailerlite_ok ? "done" : "FAILED — check"}`,
    ``,
    `**Next:** add the partner and create ${code} in Tour Amigo, then move this card to Onboarded — the kit email goes out from there.`,
  ].join("\n");
  if (tk && tt && isProduction(ctx)) {
    try {
      const q = new URLSearchParams({ key: tk, token: tt, idList: TRELLO_ACTIVE_LIST, pos: "top",
        name: `${v.club_name} — ${code}`, desc });
      const r = await fetch(`https://api.trello.com/1/cards?${q}`, { method: "POST" });
      if (r.ok) rec.trello_card_id = (await r.json()).id;
      else console.error(`club-signup: Trello ${r.status} ${(await r.text()).slice(0, 300)}`);
    } catch (e) { console.error("club-signup: Trello failed", e); }
  }
  await putClub(ctx, rec);

  // Email alert to Mike.
  const rk = Netlify.env.get("RESEND_API_KEY");
  if (rk && isProduction(ctx)) {
    try {
      const r = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { Authorization: `Bearer ${rk}`, "Content-Type": "application/json" },
        body: JSON.stringify({
          from: "Pickle Dot Tours <noreply@pickle.tours>", to: [Netlify.env.get("CLUB_ALERT_TO") || "mike@pickle.tours"],
          reply_to: v.email, subject: `New club affiliate: ${v.club_name} (${code})`, text: desc.replace(/\*\*/g, ""),
        }),
      });
      if (!r.ok) console.error(`club-signup: Resend ${r.status} ${(await r.text()).slice(0, 300)}`);
    } catch (e) { console.error("club-signup: Resend failed", e); }
  }

  return html(registeredPage(v.club_name, v.email));
}

export default async (req: Request, ctx: Context) => {
  const url = new URL(req.url);
  if (url.pathname === "/api/club-signup") return req.method === "POST" ? submit(req, ctx) : html(notFound(), 405);
  const email = (url.searchParams.get("email") ?? "").trim().slice(0, 200);
  return html(registerPage(blank(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ? email : ""), registrationOpen(ctx)), 200,
    { "X-Robots-Tag": "noindex, nofollow" });
};

export const config: Config = { path: ["/clubs/register", "/api/club-signup"] };
