import { json, normModel, normNumber, clean, isEmail, getOwner, rateLimited, signToken, sendEmail } from "../_lib.js";
// POST /api/reset-request – owner asks for a password reset link (model + build number + the email we hold for them).
export async function onRequestPost({ request, env }) {
  if (await rateLimited(env, request, "reset", 5, 3600)) return json({ error: "Too many attempts. Try again in an hour." }, 429);
  let b; try { b = await request.json(); } catch { return json({ error: "Bad request" }, 400); }
  const model = normModel(b.model), number = normNumber(b.number), email = clean(b.email, 200).toLowerCase();
  if (!model || !number || !isEmail(email)) return json({ error: "Choose your model, enter your build number and the email address we hold for you." }, 400);
  const o = await getOwner(env, model, number);
  // Always answer the same way so build numbers can't be probed.
  const generic = { ok: true, message: "If those details match our records, a reset link is on its way." };
  if (!o || !o.email || o.email.toLowerCase() !== email) return json(generic);
  const token = await signToken(env, `${model}:${number}`, 3600);
  const link = new URL(`/owners.html?reset=${encodeURIComponent(token)}`, request.url).toString();
  await sendEmail(env, { to: email, subject: "Langen owners' portal – reset your password", text: `Hello${o.name ? " " + o.name.split(" ")[0] : ""},\n\nUse this link within the next hour to choose a new password for your ${model === "lightspeed" ? "Lightspeed" : "Two Stroke"} No. ${number}:\n${link}\n\nIf you didn't ask for this, ignore this email.\n\nLangen Motorcycles` });
  return json(generic);
}
