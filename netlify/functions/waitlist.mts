import type { Context, Config } from "@netlify/functions";

/**
 * Brochure form + Postcards from the Kitchen signup → MailerLite.
 *
 * Two kinds of post (field "kind"):
 *   brochure (default, and what older forms send) — joins the brochure group
 *     (MAILERLITE_GROUP_ID), whose automation emails the brochure. If the
 *     "news" box was ticked (news=yes) it also joins the News group.
 *   news — the footer signup on both sites; joins only the News group.
 *   ontheroad — the "On the Road" sign-up on the home page; joins only the
 *     On the Road group (MAILERLITE_OTR_GROUP_ID), which will carry the 12-email series.
 * The thanks page gets ?for=brochure|news|both so it can say the right thing.
 *
 * The form on index.html posts here natively (no JS required). On success the
 * subscriber (email only) is upserted into the Route 66 Waitlist group as
 * "active" (single opt-in, Mike 11 Nov 2026); joining the group starts the
 * MailerLite "Guest welcome" automation, then the browser is redirected to
 * /thanks.html. On any failure the visitor still lands on /thanks.html, but
 * with ?status=error so the page can show a "we'll email you" fallback, and
 * the failure is logged so it shows in the Netlify function log.
 *
 * Env vars (Netlify → Project configuration → Environment variables):
 *   MAILERLITE_API_KEY   — secret; a MailerLite API token
 *   MAILERLITE_GROUP_ID       — brochure group (its automation sends the brochure)
 *   MAILERLITE_NEWS_GROUP_ID  — "Postcards from the Kitchen" group (general prospecting list)
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
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return redirect(`${THANKS}?status=error`);
  }

  const apiKey = Netlify.env.get("MAILERLITE_API_KEY");
  const groupId = Netlify.env.get("MAILERLITE_GROUP_ID");
  if (!apiKey || !groupId) {
    console.error("waitlist: MAILERLITE_API_KEY / MAILERLITE_GROUP_ID not set");
    return redirect(`${THANKS}?status=error`);
  }

  const rawKind = clean(form.get("kind"), 20);
  const kind = rawKind === "news" ? "news" : rawKind === "ontheroad" ? "ontheroad" : "brochure";
  const otrGroup = Netlify.env.get("MAILERLITE_OTR_GROUP_ID") || "204621344764069579"; // "On the Road (Route 66 email series)"
  const wantsNews = kind === "news" || clean(form.get("news"), 10) === "yes";
  const newsGroup = Netlify.env.get("MAILERLITE_NEWS_GROUP_ID") || "204488616319124956"; // "Postcards from the Kitchen" group
  if (wantsNews && !newsGroup) console.error("waitlist: MAILERLITE_NEWS_GROUP_ID not set; news opt-in not recorded");
  const groups = [
    ...(kind === "brochure" ? [groupId] : []),
    ...(kind === "ontheroad" ? [otrGroup] : []),
    ...(wantsNews && newsGroup ? [newsGroup] : []),
  ];
  if (!groups.length) return redirect(`${THANKS}?for=news&status=error`);
  const forWhat = kind === "news" ? "news" : kind === "ontheroad" ? "ontheroad" : wantsNews ? "both" : "brochure";

  const ip = req.headers.get("x-nf-client-connection-ip") ?? undefined;
  // Visitors who arrived by a club's short link post its members' code, so the signup is credited to that club.
  const club = clean(form.get("club"), 20).toUpperCase().replace(/[^A-Z0-9]/g, "");

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
        groups,
        ...(club ? { fields: { referral_club: club } } : {}),
        status: "active",
        ip_address: ip,
        subscribed_at: new Date().toISOString().replace("T", " ").slice(0, 19),
      }),
    });

    if (!res.ok) {
      const body = await res.text().catch(() => "");
      console.error(`waitlist: MailerLite ${res.status} ${body.slice(0, 500)}`);
      return redirect(`${THANKS}?for=${forWhat}&status=error`);
    }
  } catch (err) {
    console.error("waitlist: request failed", err);
    return redirect(`${THANKS}?for=${forWhat}&status=error`);
  }

  return redirect(`${THANKS}?for=${forWhat}`);
};

export const config: Config = {
  path: "/api/waitlist",
};
