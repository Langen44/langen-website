import { json, clean, isEmail, rateLimited, mailchimpSubscribe } from "../_lib.js";
// POST /api/subscribe – footer newsletter sign-up → Mailchimp audience.
export async function onRequestPost({ request, env }) {
  if (await rateLimited(env, request, "subscribe", 10, 3600)) return json({ error: "Too many attempts. Try again later." }, 429);
  let b; try { b = await request.json(); } catch { return json({ error: "Bad request" }, 400); }
  const email = clean(b.email, 200), name = clean(b.name, 120), source = clean(b.source, 40) || "footer";
  if (!isEmail(email)) return json({ error: "Please add a working email address." }, 400);
  if (env.DB) { try { await env.DB.prepare("INSERT INTO subscribers (email, name, source, page) VALUES (?,?,?,?)").bind(email, name, source, clean(b.page, 200)).run(); } catch {} }
  const r = await mailchimpSubscribe(env, { email, name, source });
  if (r.skipped) return env.DB ? json({ ok: true, note: "recorded" }) : json({ error: "The mailing list isn't connected yet." }, 503);
  if (!r.ok && r.status !== 400) return json({ error: "The mailing list didn't accept that just now." }, 502);
  return json({ ok: true });
}
