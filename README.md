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

## Club affiliate pages
Pickleball clubs refer members with a code (e.g. `MPCMEMBER500`; never "FAM", which travel advisors read as a familiarization trip) and get their own page at `/<slug>`.

| Path | What |
|---|---|
| `/club-preview/<token>` | Private, noindex preview linked from the outreach email |
| `/join/<token>` | Four-step sign-up: A page address, B code, C agreement, D MailerLite opt-in |
| `/<slug>` | Live club page (only once the club finishes sign-up); waitlist form tags signups with `referral_club` |
| `/api/club-admin` | Mac pipeline only (`~/dev/pickle-ops/clubs/clubs.py`) |
| `/club-terms.html` | Club Referral Agreement — **draft until counsel signs off** |

Data lives in Netlify Blobs: store `clubs` in production, `clubs-preview` everywhere else.
Code: `netlify/lib/` (data + page templates), `netlify/functions/club-*.mts`.

Env vars: `CLUB_ADMIN_KEY_SHA256` (comma-separated fingerprints of the keys in `~/.config/racon/club-admin.secret` on each Mac),
`CLUB_REGISTRATION_OPEN=true` to open sign-up in production (leave unset until the agreement is final),
optional `CLUB_DISCOUNT_TEXT` (default "$500 per player").
