# Pickle Tours — Route 66 Pickleball Tour (marketing site)

Phase 1 static marketing site + waitlist for the Pickle Tours Route 66 pickleball product.
Live at https://route66pickleballtour.com

## Stack
- Pure static HTML/CSS/JS, no build step
- One Netlify Function, `netlify/functions/waitlist.mts`, serves `POST /api/waitlist`:
  it adds the visitor to MailerLite (group "Pickle Tours — Route 66 Waitlist") with
  skill level / direction / seat type stored as custom fields, then redirects to `thanks.html`
- `thanks.html` is the post-submit page; `?status=error` shows a fallback line if MailerLite was unreachable

## Environment variables (Netlify → Project configuration → Environment variables)
| Key | Value |
|---|---|
| `MAILERLITE_API_KEY` | MailerLite API token (secret) |
| `MAILERLITE_GROUP_ID` | `197519394240201970` — Route 66 Waitlist group |

## Deploy
**Continuous deployment.** Netlify builds every push to `main` on
`github.com/racon-tours/route66-pickleball-tour`; branches get deploy previews.
Do not `netlify deploy` by hand — commit and push instead, from whichever Mac you're on.

Local check: `netlify dev` (needs the env vars above in `.env` or `netlify env:import`).

## Phase 2 (booking)
Replace the waitlist section CTA with the Bokun booking widget embed; everything else stays.

## Club affiliate pages
Pickleball clubs refer members with a code (e.g. `MPCFAM`) and get their own page at `/<slug>`.

| Path | What |
|---|---|
| `/club-preview/<token>` | Private, noindex preview linked from the outreach email |
| `/join/<token>` | Four-step sign-up: A page address, B code, C agreement, D MailerLite opt-in |
| `/<slug>` | Live club page (only once the club finishes sign-up); waitlist form tags signups with `referral_club` |
| `/api/club-admin` | Mac pipeline only (`~/dev/pickle-ops/clubs/clubs.py`) |
| `/club-terms.html` | Club Referral Agreement — **draft until counsel signs off** |

Data lives in Netlify Blobs: store `clubs` in production, `clubs-preview` everywhere else.
Code: `netlify/lib/` (data + page templates), `netlify/functions/club-*.mts`.

Env vars: `CLUB_ADMIN_KEY_SHA256` (fingerprint of the key in `~/.config/racon/club-admin.secret`),
`CLUB_REGISTRATION_OPEN=true` to open sign-up in production (leave unset until the agreement is final),
optional `CLUB_DISCOUNT_TEXT` (default "$500 per player").
