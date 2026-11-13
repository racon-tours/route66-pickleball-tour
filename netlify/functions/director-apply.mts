import type { Context, Config } from "@netlify/functions";
import { getStore } from "@netlify/blobs";

/**
 * Tour-director couple application (Director Bench hiring pipeline, Nov 2026).
 *
 * The form at https://pickle.tours/directors posts here natively (no JS needed).
 * Each application is:
 *   1. saved to Netlify Blobs — store "directors" in production, "directors-preview" elsewhere —
 *      key director/<email>, so nothing is lost if Trello or Resend is down;
 *   2. (production only) opened as a card on Trello board "Director Bench", list Applied
 *      (TRELLO_KEY + TRELLO_TOKEN, optional TRELLO_DIRECTOR_LIST_ID);
 *   3. (production only) emailed to mike@pickle.tours via Resend (RESEND_API_KEY, optional DIRECTOR_ALERT_TO).
 * Applicants are NOT added to MailerLite: this is a job application, not a marketing sign-up.
 * Then the browser goes to https://pickle.tours/directors-thanks (or ?status=error on failure).
 */

const DONE = "https://pickle.tours/directors-thanks";
const FORM = "https://pickle.tours/directors";
const APPLIED_LIST = "6af65e439e8b2b009aab5707"; // Director Bench › Applied

const redirect = (to: string) => new Response(null, { status: 303, headers: { Location: to } });

export default async (req: Request, ctx: Context) => {
  if (req.method !== "POST") return redirect(FORM);
  const form = await req.formData().catch(() => null);
  if (!form) return redirect(FORM);
  const s = (k: string, max = 200) => String(form.get(k) ?? "").trim().slice(0, max);
  const all = (k: string) => form.getAll(k).map((v) => String(v).trim().slice(0, 20)).filter(Boolean);

  if (s("bot-field")) return redirect(DONE); // honeypot

  const email = s("email").toLowerCase();
  const rec = {
    name_1: s("name_1", 100),
    name_2: s("name_2", 100),
    email,
    phone: s("phone", 40),
    city: s("city", 80),
    state: s("state", 80),
    home_club: s("home_club", 150),
    referred_by: s("referred_by", 150),
    level_1: s("level_1", 40),
    level_2: s("level_2", 40),
    start: s("start", 40),
    months: all("months"),
    lead_experience: s("lead_experience", 1500),
    why: s("why", 1500),
    agree: form.get("agree") ? "yes" : "no",
    submitted_at: new Date().toISOString(),
    ip: req.headers.get("x-nf-client-connection-ip") ?? undefined,
  };
  if (!rec.name_1 || !rec.name_2 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || rec.agree !== "yes") {
    return redirect(`${DONE}?status=error`);
  }

  const prod = ctx?.deploy?.context === "production";
  let saved = false;
  try {
    await getStore(prod ? "directors" : "directors-preview").setJSON(`director/${email}`, rec);
    saved = true;
  } catch (err) {
    console.error("director-apply: blob save failed", err);
  }

  const couple = `${rec.name_1} & ${rec.name_2}`;
  const summary = [
    `${couple} — ${[rec.city, rec.state].filter(Boolean).join(", ") || "(no city)"}`,
    `Email: ${rec.email}   Phone: ${rec.phone || "-"}`,
    `Home club: ${rec.home_club || "-"}   Referred by: ${rec.referred_by || "-"}`,
    `Play level: ${rec.name_1}: ${rec.level_1 || "-"} / ${rec.name_2}: ${rec.level_2 || "-"}`,
    `Could start: ${rec.start || "-"}   Months available: ${rec.months.join(", ") || "-"}`,
    ``,
    `Group-leading experience:`,
    rec.lead_experience || "-",
    ``,
    `Why us:`,
    rec.why || "-",
    ``,
    `Submitted: ${rec.submitted_at}`,
    ``,
    `Next: score against the Director Bench scorecard and book the phone screen (playbook: claude/Director_Bench_Hiring_Playbook_v1.0.md).`,
  ].join("\n");

  let carded = false;
  const tk = Netlify.env.get("TRELLO_KEY"), tt = Netlify.env.get("TRELLO_TOKEN");
  if (prod && tk && tt) {
    const list = Netlify.env.get("TRELLO_DIRECTOR_LIST_ID") || APPLIED_LIST;
    const tag = rec.referred_by ? ` (ref: ${rec.referred_by})` : "";
    const q = new URLSearchParams({ key: tk, token: tt, idList: list, pos: "top",
      name: `${couple} — ${rec.state || rec.city || "?"}${tag}`, desc: summary });
    try {
      const r = await fetch(`https://api.trello.com/1/cards?${q}`, { method: "POST" });
      if (r.ok) carded = true; else console.error(`director-apply: Trello ${r.status} ${(await r.text()).slice(0, 300)}`);
    } catch (err) { console.error("director-apply: Trello failed", err); }
  }

  const rk = Netlify.env.get("RESEND_API_KEY");
  if (prod && rk) {
    try {
      const r = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { Authorization: `Bearer ${rk}`, "Content-Type": "application/json" },
        body: JSON.stringify({
          from: "Pickle Dot Tours <noreply@pickle.tours>",
          to: [Netlify.env.get("DIRECTOR_ALERT_TO") || "mike@pickle.tours"],
          reply_to: rec.email,
          subject: `Tour director application: ${couple}${rec.referred_by ? ` (ref: ${rec.referred_by})` : ""}`,
          text: summary,
        }),
      });
      if (!r.ok) console.error(`director-apply: Resend ${r.status} ${(await r.text()).slice(0, 300)}`);
    } catch (err) { console.error("director-apply: Resend failed", err); }
  }

  return redirect(saved || carded ? DONE : `${DONE}?status=error`);
};

export const config: Config = { path: "/api/director-apply" };
