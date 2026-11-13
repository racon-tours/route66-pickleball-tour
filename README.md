# Pickle Dot Tours — Route 66 Pickleball Tour (marketing site)

Phase 1 static marketing site + waitlist for the Pickle Dot Tours Route 66 pickleball product.
Live at https://route66pickleballtour.com

## Stack
- Pure static HTML/CSS/JS, no build step
- One Netlify Function, `netlify/functions/waitlist.mts`, serves `POST /api/waitlist`:
  it adds the visitor to MailerLite (group "Pickle Dot Tours — Route 66 Waitlist") with
  skill level / direction / seat type stored as custom fields, then redirects to `thanks.html`
- `thanks.html` is the post-submit page; `?status=error` shows a fallback line if MailerLite was unreachable

## Environment variables (Netlify → Project configuration → Environment variables)
| Key | Value |
|---|---|
| `MAILERLITE_API_KEY` | MailerLite API token (secret) |
| `MAILERLITE_GROUP_ID` | `202160777372632936` — Route 66 Waitlist group |

## Deploy
**Continuous deployment.** Netlify builds every push to `main` on
`github.com/racon-tours/route66-pickleball-tour`; branches get deploy previews.
Do not `netlify deploy` by hand — commit and push instead, from whichever Mac you're on.

Local check: `netlify dev` (needs the env vars above in `.env` or `netlify env:import`).

## Phase 2 (booking)
Replace the waitlist section CTA with the Bokun booking widget embed; everything else stays.

## Travel advisor sign-up
`netlify/functions/advisor-signup.mts` serves `POST /api/advisor-signup`, the target of the form at
https://pickle.tours/advisors. It saves each advisor to Netlify Blobs (store `advisors`, key
`advisor/<email>`) and adds them to MailerLite group "Pickle Dot Tours — Travel Advisors", then
redirects to https://pickle.tours/advisors-thanks. Interim until advisors can self-register in Tour Amigo.
In production it also opens a card on Trello board "Travel Advisors" (list Registered) when
`TRELLO_KEY` + `TRELLO_TOKEN` are set, and emails mike@pickle.tours via Resend when `RESEND_API_KEY`
is set (optional `TRELLO_ADVISOR_LIST_ID`, `ADVISOR_ALERT_TO`).

The form carries a required acceptance box for the Travel Advisor Agreement (https://pickle.tours/advisor-terms)
and a hidden `terms_version`. The function stores the version, time, IP and browser on the advisor record and
appends a never-overwritten entry at `acceptance/<email>/<time>` in the same store; the Trello card and
MailerLite field `advisor_terms` show the version and time. When the agreement text changes, change the
version on the page and in the form's hidden field together.

## Tour-director applications
`netlify/functions/director-apply.mts` serves `POST /api/director-apply`, the target of the form at
https://pickle.tours/directors (married/partnered couples applying to be tour directors). It saves each
application to Netlify Blobs (store `directors`, key `director/<email>`), and in production opens a card on
Trello board "Director Bench" (list Applied) and emails mike@pickle.tours via Resend — same `TRELLO_KEY`,
`TRELLO_TOKEN`, `RESEND_API_KEY` as the advisor sign-up (optional `TRELLO_DIRECTOR_LIST_ID`, `DIRECTOR_ALERT_TO`).
Applicants are not added to MailerLite. Then redirects to https://pickle.tours/directors-thanks.

## Club affiliate links
Pickleball clubs refer members with a code (`<CLUB>500`, e.g. `ABQE500`; never "MEMBER", never "FAM", which travel advisors read as a familiarization trip).
Clubs do **not** get a web page (dropped 3 Nov 2026). Each club gets a short link, `/<slug>`, that forwards (302) to the
home page with GA tags: `utm_source=<slug>&utm_medium=club&utm_campaign=club-referral&utm_content=<CODE>`. In GA4, filter
session medium = `club`. The home page keeps the code for the visit and sends it with a waitlist signup, so MailerLite
tags that subscriber with `referral_club`.

| Path | What |
|---|---|
| `/clubs/register` | **Self-serve sign-up** (from the MailerLite welcome email, `?email=` prefills): one short name → link + code, club address/contact, agreement. Hawaii (`CLUB_BLOCKED_STATES`) is turned away and Mike is emailed to follow up; Florida (`CLUB_HELD_STATES`) registers but stays on hold — link off, no kit — until `clubs.py release FL` on the Mac. Opens a Trello card in Club Affiliates → Active and emails Mike. |
| `/join/<token>` | Outreach sign-up (clubs Mike emailed first): A club link, B code, C agreement, D MailerLite opt-in |
| `/club-preview/<token>` | Forwards to `/join/<token>` (older outreach emails link here) |
| `/<slug>` | Club short link (clubs that finished sign-up, plus `MANUAL_LINKS` in `netlify/lib/clubs.mts` for clubs set up by hand) |
| `/api/club-admin` | Mac pipeline only (`~/dev/pickle-ops/clubs/clubs.py`) |
| `/club-terms.html` | Club Referral Agreement (counsel signed off, Nov 2026) |

**Onboarding:** club registers → card in Active → Claude adds the Tour Amigo partner and code (club-partner-onboarding skill) and moves the card to Onboarded → the Mac sync emails the kit (flyer, newsletter graphic, link, code).

The code itself (the $500 discount) lives in Tour Amigo as a Tour Commercial Rule; the link only does tracking.

Data lives in Netlify Blobs: store `clubs` in production, `clubs-preview` everywhere else.
Code: `netlify/lib/` (data + page templates), `netlify/functions/club-*.mts`.

Env vars: `CLUB_ADMIN_KEY_SHA256` (comma-separated fingerprints of the keys in `~/.config/racon/club-admin.secret` on each Mac),
`CLUB_REGISTRATION_OPEN=true` to open sign-up in production (leave unset until the agreement is final),
optional `CLUB_DISCOUNT_TEXT` (default "$500 per player").
