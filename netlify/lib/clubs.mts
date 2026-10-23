/**
 * Club affiliate program — shared data + rendering helpers.
 *
 * Storage: Netlify Blobs. Production uses store "clubs"; every other deploy
 * context (deploy previews, branch deploys, netlify dev) uses "clubs-preview",
 * so testing never touches real club records.
 *
 * Keys:
 *   club/<token>   JSON ClubRecord (one per prospect; token is unguessable)
 *   slug/<slug>    token that owns the URL slug   (written on registration)
 *   code/<CODE>    token that owns the promo code (written on registration)
 */
import { getStore } from "@netlify/blobs";

export const TERMS_VERSION = "DRAFT-2026-10"; // bump when counsel finalises the agreement
export const CODE_SUFFIX = "FAM";
export const SITE = "https://route66pickleballtour.com";

export const RESERVED = new Set([
  "api", "assets", "join", "club-preview", "club-terms", "thanks", "index", "robots", "sitemap",
  "dates", "terms", "privacy", "brochure", "admin", "clubs", "club", "about", "contact", "faq",
  "book", "booking", "waitlist", "route66", "pickle", "pickletours", "tour", "tours", "netlify",
]);

export type Status = "prospect" | "active" | "declined";

export interface ClubRecord {
  token: string;
  club_name: string;
  city?: string;
  state?: string;
  contact_name?: string;
  contact_email?: string;
  website?: string;
  logo_url?: string;
  member_note?: string;        // e.g. "1,200 members, 24 courts"
  suggested_slug: string;
  suggested_code: string;      // full code incl. suffix, e.g. MPCFAM
  status: Status;
  trello_card_id?: string;
  created_at: string;
  updated_at: string;
  registration?: {
    slug: string;
    code: string;
    terms_version: string;
    signer_name: string;
    signer_title: string;
    signer_email: string;
    agreed_at: string;
    agreed_ip?: string;
    mailerlite_optin: boolean;
    mailerlite_ok?: boolean;
  };
}

export function isProduction(ctx: any): boolean {
  return ctx?.deploy?.context === "production";
}

export function store(ctx: any) {
  return getStore({ name: isProduction(ctx) ? "clubs" : "clubs-preview", consistency: "strong" });
}

export async function getClub(ctx: any, token: string): Promise<ClubRecord | null> {
  if (!/^[a-z0-9]{16,64}$/.test(token)) return null;
  return (await store(ctx).get(`club/${token}`, { type: "json" })) as ClubRecord | null;
}

export async function putClub(ctx: any, rec: ClubRecord) {
  rec.updated_at = new Date().toISOString();
  await store(ctx).setJSON(`club/${rec.token}`, rec);
}

export async function listClubs(ctx: any): Promise<ClubRecord[]> {
  const s = store(ctx);
  const { blobs } = await s.list({ prefix: "club/" });
  const out: ClubRecord[] = [];
  for (const b of blobs) {
    const r = (await s.get(b.key, { type: "json" })) as ClubRecord | null;
    if (r) out.push(r);
  }
  return out;
}

export async function clubBySlug(ctx: any, slug: string): Promise<ClubRecord | null> {
  const token = await store(ctx).get(`slug/${slug}`);
  if (!token) return null;
  const rec = await getClub(ctx, token);
  return rec && rec.status === "active" ? rec : null;
}

export function normSlug(v: string): string {
  return v.toLowerCase().trim().replace(/[^a-z0-9-]+/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "");
}

export function slugProblem(slug: string): string | null {
  if (slug.length < 3 || slug.length > 40) return "Use 3–40 letters, numbers or dashes.";
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(slug)) return "Use letters, numbers and single dashes only.";
  if (RESERVED.has(slug)) return "That address is reserved. Try another.";
  return null;
}

export function normCodePrefix(v: string): string {
  let p = v.toUpperCase().replace(/[^A-Z0-9]/g, "");
  if (p.endsWith(CODE_SUFFIX) && p.length > CODE_SUFFIX.length) p = p.slice(0, -CODE_SUFFIX.length);
  return p;
}

export function codeProblem(prefix: string): string | null {
  if (prefix.length < 2 || prefix.length > 14) return "Use 2–14 letters or numbers before FAM.";
  return null;
}

/** Is slug/code free for this token? (A club re-submitting its own choices is fine.) */
export async function isFree(ctx: any, kind: "slug" | "code", value: string, token?: string) {
  const owner = await store(ctx).get(`${kind}/${value}`);
  return !owner || owner === token;
}

export const esc = (s: unknown) =>
  String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!));

export function discountText(): string {
  return Netlify.env.get("CLUB_DISCOUNT_TEXT") || "$500 per player";
}

export function html(body: string, status = 200, extraHeaders: Record<string, string> = {}) {
  return new Response(body, {
    status,
    headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store", ...extraHeaders },
  });
}

export async function sha256Hex(s: string): Promise<string> {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
