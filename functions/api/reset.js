import { json, verifyToken, hashPassword, makeSession } from "../_lib.js";
// POST /api/reset – sets a new password from a reset link token.
export async function onRequestPost({ request, env }) {
  let b; try { b = await request.json(); } catch { return json({ error: "Bad request" }, 400); }
  const payload = await verifyToken(env, b.token);
  if (!payload) return json({ error: "That link has expired. Ask for a new one." }, 400);
  const [model, number] = payload.split(":");
  const password = String(b.password || "");
  if (password.length < 10) return json({ error: "Choose a password of at least 10 characters." }, 400);
  const { hash, salt } = await hashPassword(password);
  await env.DB.prepare("UPDATE owners SET password_hash = ?, password_salt = ? WHERE model = ? AND number = ?").bind(hash, salt, model, number).run();
  const s = await makeSession(env, model, number);
  return json({ ok: true }, 200, { "set-cookie": s.cookie });
}
