import { json, normModel, normNumber, verifyPassword, makeSession, getOwner, rateLimited } from "../_lib.js";
export async function onRequestPost({ request, env }) {
  if (await rateLimited(env, request, "login", 15)) return json({ error: "Too many attempts. Try again in 15 minutes." }, 429);
  let b; try { b = await request.json(); } catch { return json({ error: "Bad request" }, 400); }
  const model = normModel(b.model), number = normNumber(b.number), password = String(b.password || "");
  if (!model || !number || !password) return json({ error: "Choose your model, enter your build number and password." }, 400);
  const o = await getOwner(env, model, number);
  if (!o || !o.password_hash || !(await verifyPassword(password, o.password_hash, o.password_salt))) {
    return json({ error: "That build number and password don't match." }, 401);
  }
  const s = await makeSession(env, model, number);
  return json({ ok: true }, 200, { "set-cookie": s.cookie });
}
