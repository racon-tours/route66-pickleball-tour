import type { Context, Config } from "@netlify/functions";
import { getStore } from "@netlify/blobs";

/**
 * Travel-advisor sign-up (interim, until Tour Amigo self-registration is in place).
 *
 * The form at https://pickle.tours/advisors posts here natively (no JS needed).
 * Each sign-up is:
 *   1. saved to Netlify Blobs — store "advisors" in production, "advisors-preview" elsewhere —
 *      key advisor/<email>, so nothing is lost even if MailerLite is down;
 *   2. upserted into MailerLite group "Pickle Dot Tours — Travel Advisors" (created on first use)
 *      with their agency, host, advisor ID and address as fields. The hourly advisor sync reads that
 *      group, opens a Trello card per new advisor, and the Tour Amigo portal login is created from it.
 * Then the browser goes to https://pickle.tours/advisors-thanks (or ?status=error on failure).
 *
 * Env vars: MAILERLITE_API_KEY (already set for the waitlist).
 */

const DONE = "https://pickle.tours/advisors-thanks";
const FORM = "https://pickle.tours/advisors";
const ML = "https://connect.mailerlite.com/api";
const ML_GROUP = "Pickle Dot Tours — Travel Advisors";
const CUSTOM_FIELDS: Record<string, string> = {
  advisor_host: "Advisor Host",
  advisor_id: "Advisor ID",
  advisor_address: "Advisor Address",
  advisor_webinar: "Advisor Webinar",
};

const redirect = (to: string) => new Response(null, { status: 303, headers: { Location: to } });

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

async function groupId(): Promise<string> {
  const existing = await ml(`/fields?limit=100`);
  const have = new Set((existing.data ?? []).map((f: any) => f.key));
  for (const [key, name] of Object.entries(CUSTOM_FIELDS)) {
    if (!have.has(key)) await ml(`/fields`, { method: "POST", body: JSON.stringify({ name, type: "text" }) });
  }
  const groups = await ml(`/groups?filter[name]=${encodeURIComponent(ML_GROUP)}&limit=50`);
  const g = groups.data?.find((x: any) => x.name === ML_GROUP);
  if (g) return g.id;
  return (await ml(`/groups`, { method: "POST", body: JSON.stringify({ name: ML_GROUP }) })).data.id;
}

export default async (req: Request, ctx: Context) => {
  if (req.method !== "POST") return redirect(FORM);
  const form = await req.formData().catch(() => null);
  if (!form) return redirect(FORM);
  const s = (k: string, max = 200) => String(form.get(k) ?? "").trim().slice(0, max);

  if (s("bot-field")) return redirect(DONE); // honeypot

  const email = s("email").toLowerCase();
  const rec = {
    first_name: s("first_name", 80),
    last_name: s("last_name", 80),
    email,
    phone: s("phone", 40),
    agency: s("agency", 120),
    host: s("host") === "Other" ? s("host_other", 120) || "Other" : s("host", 120),
    advisor_id: s("advisor_id", 60),
    street: s("street"),
    city: s("city", 80),
    state: s("state", 80),
    zip: s("zip", 20),
    country: s("country", 80) || "United States",
    webinar: form.get("webinar") ? "yes" : "no",
    submitted_at: new Date().toISOString(),
    ip: req.headers.get("x-nf-client-connection-ip") ?? undefined,
  };
  if (!rec.first_name || !rec.last_name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return redirect(`${DONE}?status=error`);
  }

  const prod = ctx?.deploy?.context === "production";
  let saved = false;
  try {
    await getStore(prod ? "advisors" : "advisors-preview").setJSON(`advisor/${email}`, rec);
    saved = true;
  } catch (err) {
    console.error("advisor-signup: blob save failed", err);
  }

  let listed = false;
  try {
    const gid = await groupId();
    const address = [rec.street, rec.city, rec.state, rec.zip, rec.country].filter(Boolean).join(", ");
    await ml(`/subscribers`, {
      method: "POST",
      body: JSON.stringify({
        email,
        groups: [gid],
        status: "active", // business registration they asked for; no double opt-in email
        ip_address: rec.ip,
        fields: {
          name: rec.first_name,
          last_name: rec.last_name,
          company: rec.agency,
          phone: rec.phone,
          city: rec.city,
          state: rec.state,
          z_i_p: rec.zip,
          country: rec.country,
          advisor_host: rec.host,
          advisor_id: rec.advisor_id,
          advisor_address: address,
          advisor_webinar: rec.webinar,
        },
      }),
    });
    listed = true;
  } catch (err) {
    console.error("advisor-signup: MailerLite failed", err);
  }

  const summary = [
    `${rec.first_name} ${rec.last_name} — ${rec.agency || "(no agency)"}`,
    `Host: ${rec.host || "-"}   Advisor ID: ${rec.advisor_id || "-"}`,
    `Email: ${rec.email}   Phone: ${rec.phone || "-"}`,
    `Address: ${[rec.street, rec.city, rec.state, rec.zip, rec.country].filter(Boolean).join(", ")}`,
    `Webinar invite: ${rec.webinar}`,
    `Submitted: ${rec.submitted_at}`,
    ``,
    `Next: create the Tour Amigo distribution partner (group "Fora Travel Advisors" if Fora) and a user login, then move this card to Portal Sent.`,
  ].join("\n");

  // Trello card on the Travel Advisors board (only when the Trello credentials are set).
  const tk = Netlify.env.get("TRELLO_KEY"), tt = Netlify.env.get("TRELLO_TOKEN");
  if (prod && tk && tt) {
    const list = Netlify.env.get("TRELLO_ADVISOR_LIST_ID") || "6ae9107428beed63b46602df";
    const q = new URLSearchParams({ key: tk, token: tt, idList: list, pos: "top",
      name: `${rec.first_name} ${rec.last_name} — ${rec.agency || rec.host || "Advisor"}`, desc: summary });
    try {
      const r = await fetch(`https://api.trello.com/1/cards?${q}`, { method: "POST" });
      if (!r.ok) console.error(`advisor-signup: Trello ${r.status} ${(await r.text()).slice(0, 300)}`);
    } catch (err) { console.error("advisor-signup: Trello failed", err); }
  }

  // Email alert to Mike via Resend (only when the key is set).
  const rk = Netlify.env.get("RESEND_API_KEY");
  if (prod && rk) {
    try {
      const r = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { Authorization: `Bearer ${rk}`, "Content-Type": "application/json" },
        body: JSON.stringify({
          from: "Pickle Dot Tours <noreply@pickle.tours>",
          to: [Netlify.env.get("ADVISOR_ALERT_TO") || "mike@pickle.tours"],
          reply_to: rec.email,
          subject: `New travel advisor: ${rec.first_name} ${rec.last_name} (${rec.host || "no host"})`,
          text: summary,
        }),
      });
      if (!r.ok) console.error(`advisor-signup: Resend ${r.status} ${(await r.text()).slice(0, 300)}`);
    } catch (err) { console.error("advisor-signup: Resend failed", err); }
  }

  return redirect(saved || listed ? DONE : `${DONE}?status=error`);
};

export const config: Config = { path: "/api/advisor-signup" };
