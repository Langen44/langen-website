import { json, hmacSha256Hex, timingSafeEqual, sendEmail } from "../_lib.js";
// POST /api/stripe-webhook – records completed deposits (checkout.session.completed) in D1 and emails the team.
// Stripe → Developers → Webhooks → endpoint https://<site>/api/stripe-webhook, event checkout.session.completed; signing secret → STRIPE_WEBHOOK_SECRET.
export async function onRequestPost({ request, env }) {
  if (!env.STRIPE_WEBHOOK_SECRET) return json({ error: "Webhook not configured" }, 503);
  const payload = await request.text();
  const sig = request.headers.get("stripe-signature") || "";
  const parts = Object.fromEntries(sig.split(",").map((p) => p.split("=")));
  const t = parts.t, v1 = parts.v1;
  if (!t || !v1 || Math.abs(Date.now() / 1000 - Number(t)) > 300) return json({ error: "Bad signature" }, 400);
  const expect = await hmacSha256Hex(env.STRIPE_WEBHOOK_SECRET, `${t}.${payload}`);
  if (!timingSafeEqual(expect, v1)) return json({ error: "Bad signature" }, 400);
  let ev; try { ev = JSON.parse(payload); } catch { return json({ error: "Bad payload" }, 400); }
  if (ev.type !== "checkout.session.completed") return json({ received: true });
  const s = ev.data?.object || {};
  const email = s.customer_details?.email || s.customer_email || "", name = s.customer_details?.name || "";
  const amount = (s.amount_total ?? 0) / 100, currency = (s.currency || "gbp").toUpperCase();
  let number = null;
  if (env.DB) {
    try {
      const row = await env.DB.prepare("SELECT COALESCE(MAX(build_number), 0) + 1 AS n FROM reservations WHERE model = 'lightspeed'").first();
      number = row?.n || 1;
      await env.DB.prepare("INSERT OR IGNORE INTO reservations (stripe_session, model, build_number, name, email, amount, currency, country, raw) VALUES (?,?,?,?,?,?,?,?,?)")
        .bind(s.id, "lightspeed", number, name, email, amount, currency, s.customer_details?.address?.country || "", payload.slice(0, 20000)).run();
    } catch (e) { console.log("reservation insert failed", String(e)); }
  }
  try {
    await sendEmail(env, { to: env.ENQUIRY_TO || "info@langenmotorcycles.co.uk", subject: `Deposit received – ${name || email} – ${currency} ${amount}`,
      text: `A Lightspeed deposit has been paid.\n\nName: ${name}\nEmail: ${email}\nAmount: ${currency} ${amount}\nProvisional build number: ${number ?? "(no database)"}\nStripe session: ${s.id}\n` });
  } catch {}
  return json({ received: true, build_number: number });
}
