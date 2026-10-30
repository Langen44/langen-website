import { json, normModel, normNumber, hashPassword, makeSession, getOwner, rateLimited } from "../_lib.js";
// First-time set-up: model + build number + activation code (issued by Langen) + chosen password.
export async function onRequestPost({ request, env }) {
  if (await rateLimited(env, request, "register", 10)) return json({ error: "Too many attempts. Try again in 15 minutes." }, 429);
  let b; try { b = await request.json(); } catch { return json({ error: "Bad request" }, 400); }
  const model = normModel(b.model), number = normNumber(b.number);
  const norm = (c) => String(c || "").toUpperCase().replace(/[^A-Z0-9]/g, "");
  const code = norm(b.code);
  const password = String(b.password || "");
  if (!model || !number) return json({ error: "Choose your model and enter your build number." }, 400);
  if (!code) return json({ error: "Enter the activation code that came with your motorcycle." }, 400);
  if (password.length < 10) return json({ error: "Choose a password of at least 10 characters." }, 400);
  const o = await getOwner(env, model, number);
  if (!o || norm(o.activation_code) !== code) return json({ error: "We couldn't match that build number and activation code. Check the card that came with your bike, or email us." }, 400);
  if (o.password_hash) return json({ error: "This motorcycle is already registered. Sign in instead, or email us if you've lost the password." }, 400);
  const { hash, salt } = await hashPassword(password);
  await env.DB.prepare("UPDATE owners SET password_hash = ?, password_salt = ?, activated_at = CURRENT_TIMESTAMP WHERE model = ? AND number = ?").bind(hash, salt, model, number).run();
  const s = await makeSession(env, model, number);
  return json({ ok: true }, 200, { "set-cookie": s.cookie });
}
