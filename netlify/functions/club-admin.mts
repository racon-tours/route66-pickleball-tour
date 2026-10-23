import type { Context, Config } from "@netlify/functions";
import { ClubRecord, getClub, putClub, listClubs, store, sha256Hex, normSlug, normCodePrefix, CODE_SUFFIX } from "../lib/clubs.mts";

/**
 * /api/club-admin — used only by the Mac pipeline (~/dev/pickle-ops/clubs/clubs.py).
 * Auth: Bearer key. Only its SHA-256 is stored here (or in CLUB_ADMIN_KEY_SHA256), so the key itself
 * lives solely in ~/.config/racon/club-admin.secret on the Mac.
 *
 *   GET                                    → all club records
 *   POST {action:"upsert", club:{...}}     → create/update a prospect (never touches registration)
 *   POST {action:"set", token, trello_card_id?, status?:"prospect"|"declined"}
 */
export default async (req: Request, ctx: Context) => {
  // SHA-256 of the 36-byte random key in ~/.config/racon/club-admin.secret. A fingerprint of a
  // high-entropy key is safe to publish; the env var overrides it if the key is ever rotated.
  const want = Netlify.env.get("CLUB_ADMIN_KEY_SHA256") || "08e23bbf18fecb6f413fcda4b52e91d1581b58be67473b9eb805f02a9e65f746";
  const got = (req.headers.get("authorization") ?? "").replace(/^Bearer\s+/i, "");
  if (!want) return new Response("forbidden: CLUB_ADMIN_KEY_SHA256 not set", { status: 403 });
  if (!got || (await sha256Hex(got)) !== want.trim().toLowerCase()) return new Response("forbidden: bad key", { status: 403 });

  if (req.method === "GET") return Response.json(await listClubs(ctx));
  if (req.method !== "POST") return new Response("method", { status: 405 });
  const body = await req.json().catch(() => ({}));

  if (body.action === "upsert") {
    const c = body.club ?? {};
    if (!/^[a-z0-9]{24,64}$/.test(c.token ?? "") || !c.club_name) return new Response("token + club_name required", { status: 400 });
    const now = new Date().toISOString();
    const prev = await getClub(ctx, c.token);
    const pick = (k: string) => (typeof c[k] === "string" ? c[k].trim().slice(0, 300) : undefined);
    const rec: ClubRecord = {
      ...(prev ?? { status: "prospect", created_at: now }),
      token: c.token,
      club_name: pick("club_name")!,
      city: pick("city"), state: pick("state"), contact_name: pick("contact_name"),
      contact_email: pick("contact_email"), website: pick("website"), logo_url: pick("logo_url"),
      member_note: pick("member_note"),
      suggested_slug: normSlug(pick("suggested_slug") ?? c.club_name),
      suggested_code: normCodePrefix(pick("suggested_code") ?? "CLUB") + CODE_SUFFIX,
    } as ClubRecord;
    if (prev?.registration) rec.registration = prev.registration;
    if (prev?.trello_card_id) rec.trello_card_id = prev.trello_card_id;
    await putClub(ctx, rec);
    return Response.json(rec);
  }

  if (body.action === "set") {
    const rec = await getClub(ctx, body.token ?? "");
    if (!rec) return new Response("not found", { status: 404 });
    if (typeof body.trello_card_id === "string") rec.trello_card_id = body.trello_card_id;
    if (body.status === "declined" || body.status === "prospect") {
      // Declining a live club takes its page down and frees its address + code.
      if (rec.registration && body.status === "declined") {
        await store(ctx).delete(`slug/${rec.registration.slug}`);
        await store(ctx).delete(`code/${rec.registration.code}`);
      }
      rec.status = body.status;
    }
    await putClub(ctx, rec);
    return Response.json(rec);
  }
  return new Response("unknown action", { status: 400 });
};

export const config: Config = { path: "/api/club-admin" };
