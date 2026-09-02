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
