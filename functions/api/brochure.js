import { json, clean, isEmail, ip, rateLimited, sendEmail, mailchimpSubscribe } from "../_lib.js";
// POST /api/brochure – brochure request: records the contact, tags them in Mailchimp, returns the PDF link.
export async function onRequestPost({ request, env }) {
  if (await rateLimited(env, request, "brochure", 10, 3600)) return json({ error: "Too many requests. Try again later." }, 429);
  let b; try { b = await request.json(); } catch { return json({ error: "Bad request" }, 400); }
  if (clean(b.website)) return json({ ok: true, url: brochureUrl(request) });
  const email = clean(b.email, 200), name = clean(b.name, 120);
  if (!isEmail(email)) return json({ error: "Please add a working email address." }, 400);
  const url = brochureUrl(request);
  if (env.DB) { try { await env.DB.prepare("INSERT INTO subscribers (email, name, source, page) VALUES (?,?,?,?)").bind(email, name, "brochure", clean(b.page, 200)).run(); } catch {} }
  try { await mailchimpSubscribe(env, { email, name, tags: ["Brochure – Lightspeed"], source: "brochure" }); } catch {}
  try {
    await sendEmail(env, { to: email, subject: "The Langen Lightspeed brochure", text: `Hello${name ? " " + name.split(" ")[0] : ""},\n\nThank you for your interest in the Lightspeed. The brochure is here:\n${url}\n\nIf you'd like to talk about a build, reply to this email or call 01942 724 059.\n\nKind regards,\nChristofer\nLangen Motorcycles`, replyTo: env.ENQUIRY_TO || "info@langenmotorcycles.co.uk" });
    await sendEmail(env, { to: env.ENQUIRY_TO || "info@langenmotorcycles.co.uk", subject: `Brochure request – ${name || email}`, text: `${name || "-"} <${email}> requested the Lightspeed brochure from ${clean(b.page, 200) || "/"} (${ip(request)}).` });
  } catch {}
  return json({ ok: true, url });
}
function brochureUrl(request) { return new URL("/assets/Langen_Lightspeed_Brochure.pdf", request.url).toString(); }
