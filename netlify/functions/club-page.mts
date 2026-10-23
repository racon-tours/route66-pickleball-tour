import type { Context, Config } from "@netlify/functions";
import { clubBySlug, html } from "../lib/clubs.mts";
import { clubPage, notFound } from "../lib/pages.mts";

/**
 * route66pickleballtour.com/<slug> — a live club page.
 * preferStatic keeps every real file (index.html, thanks.html, robots.txt …) winning over this.
 * Only clubs that finished sign-up (status "active") resolve; everything else is a 404.
 */
export default async (req: Request, ctx: Context) => {
  const slug = (ctx.params?.slug ?? "").toLowerCase();
  const club = /^[a-z0-9-]{3,40}$/.test(slug) ? await clubBySlug(ctx, slug) : null;
  if (!club) return html(notFound(), 404);
  return new Response(clubPage(club, "live"), {
    headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "public, max-age=0, must-revalidate" },
  });
};

export const config: Config = { path: "/:slug", preferStatic: true };
