import type { Context, Config } from "@netlify/functions";
import { clubBySlug, html, trackingUrl, MANUAL_LINKS } from "../lib/clubs.mts";
import { notFound } from "../lib/pages.mts";

/**
 * route66pickleballtour.com/<slug> — a club's short link (no club page since 3 Nov 2026).
 * Forwards to the home page with GA tags naming the club and its code.
 * preferStatic keeps every real file (index.html, thanks.html, robots.txt …) winning over this.
 * Resolves for clubs that finished sign-up (status "active") and clubs in MANUAL_LINKS; everything else 404s.
 * 302, not 301, so a link can be repointed later without browsers having cached the old target.
 */
export default async (req: Request, ctx: Context) => {
  const slug = (ctx.params?.slug ?? "").toLowerCase();
  if (!/^[a-z0-9-]{3,40}$/.test(slug)) return html(notFound(), 404);
  let code = MANUAL_LINKS[slug];
  if (!code) {
    const club = await clubBySlug(ctx, slug);
    code = club?.registration?.code ?? "";
  }
  if (!code) return html(notFound(), 404);
  return new Response(null, {
    status: 302,
    headers: { Location: trackingUrl(slug, code), "Cache-Control": "no-store", "X-Robots-Tag": "noindex" },
  });
};

export const config: Config = { path: "/:slug", preferStatic: true };
