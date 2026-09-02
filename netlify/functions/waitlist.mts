import type { Context, Config } from "@netlify/functions";

/**
 * Waitlist form → MailerLite.
 *
 * The form on index.html posts here natively (no JS required). On success the
 * subscriber is upserted into the Route 66 Waitlist group with the three
 * optional answers stored as custom fields, then the browser is redirected to
 * /thanks.html. On any failure the visitor still lands on /thanks.html, but
 * with ?status=error so the page can show a "we'll email you" fallback, and
 * the failure is logged so it shows in the Netlify function log.
 *
 * Env vars (Netlify → Project configuration → Environment variables):
 *   MAILERLITE_API_KEY   — secret; a MailerLite API token
 *   MAILERLITE_GROUP_ID  — the group new signups land in
 */

const THANKS = "/thanks.html";
const HOME = "/#waitlist";

function redirect(to: string, status = 303): Response {
  return new Response(null, { status, headers: { Location: to } });
}

function clean(v: FormDataEntryValue | null, max = 200): string {
  return typeof v === "string" ? v.trim().slice(0, max) : "";
}

export default async (req: Request, _context: Context) => {
  if (req.method !== "POST") return redirect(HOME);

  let form: FormData;
  try {
    form = await req.formData();
  } catch {
    return redirect(HOME);
  }

  // Honeypot: bots fill the hidden field. Pretend it worked.
  if (clean(form.get("bot-field"))) return redirect(THANKS);

  const email = clean(form.get("email")).toLowerCase();
  const first = clean(form.get("first_name"), 80);
  const last = clean(form.get("last_name"), 80);
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return redirect(`${THANKS}?status=error`);
  }

  const apiKey = Netlify.env.get("MAILERLITE_API_KEY");
  const groupId = Netlify.env.get("MAILERLITE_GROUP_ID");
  if (!apiKey || !groupId) {
    console.error("waitlist: MAILERLITE_API_KEY / MAILERLITE_GROUP_ID not set");
    return redirect(`${THANKS}?status=error`);
  }

  const fields: Record<string, string> = { name: first, last_name: last };
  const skill = clean(form.get("skill_level"));
  const direction = clean(form.get("direction"));
  const seat = clean(form.get("seat_type"));
  if (skill) fields.skill_level = skill;
  if (direction) fields.direction = direction;
  if (seat) fields.seat_type = seat;

  const ip = req.headers.get("x-nf-client-connection-ip") ?? undefined;

  try {
    const res = await fetch("https://connect.mailerlite.com/api/subscribers", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        email,
        fields,
        groups: [groupId],
        status: "active",
        ip_address: ip,
        subscribed_at: new Date().toISOString().replace("T", " ").slice(0, 19),
      }),
    });

    if (!res.ok) {
      const body = await res.text().catch(() => "");
      console.error(`waitlist: MailerLite ${res.status} ${body.slice(0, 500)}`);
      return redirect(`${THANKS}?status=error`);
    }
  } catch (err) {
    console.error("waitlist: request failed", err);
    return redirect(`${THANKS}?status=error`);
  }

  return redirect(THANKS);
};

export const config: Config = {
  path: "/api/waitlist",
};
