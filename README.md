# Pickle Tours — Route 66 Pickleball Tour (marketing site)

Phase 1 static marketing site + waitlist for the Racon Tours Route 66 pickleball product.

## Stack
- Pure static HTML/CSS/JS, no build step
- Netlify Forms for the waitlist (form `waitlist` — submissions appear in Netlify dashboard → Forms; add email/Zapier/MailerLite notifications there)
- `thanks.html` is the post-submit page

## Deploy
- **Netlify CLI:** `netlify deploy --prod --dir .`
- **Drag & drop:** drop this folder at app.netlify.com/drop
- **Git:** push to `racon-tours/pickle-tours`, connect repo in Netlify (build command: none, publish dir: `.`)

## Phase 2 (booking)
Replace the waitlist section CTA with the Bokun booking widget embed; everything else stays.
