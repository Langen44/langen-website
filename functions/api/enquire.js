import { json, clean, isEmail, esc, ip, rateLimited, turnstileOk, sendEmail, mailchimpSubscribe } from "../_lib.js";
// POST /api/enquire – the enquiry form (panel + contact page).
// Saves to D1 (if bound), emails the team (if RESEND_API_KEY), subscribes to Mailchimp when the box is ticked.
const MODELS = { lightspeed: "Lightspeed", "two-stroke": "Two Stroke (pre-owned)", visit: "Workshop visit", other: "General" };
export async function onRequestPost({ request, env }) {
  if (await rateLimited(env, request, "enquire", 8, 3600)) return json({ error: "That's a lot of enquiries from one place. Try again in an hour, or email us." }, 429);
  let b; try { b = await request.json(); } catch { return json({ error: "Bad request" }, 400); }
  if (clean(b.website)) return json({ ok: true }); // honeypot: pretend success
  const name = clean(b.name, 120), email = clean(b.email, 200), country = clean(b.country, 80), phone = clean(b.phone, 40);
  const message = clean(b.message, 4000), model = MODELS[b.model] ? b.model : "other", subject = clean(b.subject, 120) || "Enquiry";
  const page = clean(b.page, 200), utm = clean(b.utm, 300), referrer = clean(b.referrer, 200), newsletter = b.newsletter === "1" || b.newsletter === true;
  if (!name || !isEmail(email)) return json({ error: "Please add your name and a working email address." }, 400);
  if (!(await turnstileOk(env, request, b.turnstile))) return json({ error: "We couldn't verify that you're human. Please try again." }, 400);

  let stored = false;
  if (env.DB) {
    try {
      await env.DB.prepare("INSERT INTO enquiries (name, email, country, phone, model, subject, message, page, utm, referrer, newsletter, ip) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)")
        .bind(name, email, country, phone, model, subject, message, page, utm, referrer, newsletter ? 1 : 0, ip(request)).run();
      stored = true;
    } catch (e) { console.log("enquiry insert failed", String(e)); }
  }
  const to = env.ENQUIRY_TO || "info@langenmotorcycles.co.uk";
  const text = `${subject}\n\nName: ${name}\nEmail: ${email}\nCountry: ${country || "-"}\nPhone: ${phone || "-"}\nAbout: ${MODELS[model]}\nNewsletter: ${newsletter ? "yes" : "no"}\n\n${message || "(no message)"}\n\n—\nPage: ${page}\nUTM: ${utm || "-"}\nReferrer: ${referrer || "-"}\n`;
  const html = `<p><b>${esc(subject)}</b></p><table cellpadding="4"><tr><td>Name</td><td>${esc(name)}</td></tr><tr><td>Email</td><td><a href="mailto:${esc(email)}">${esc(email)}</a></td></tr><tr><td>Country</td><td>${esc(country || "-")}</td></tr><tr><td>Phone</td><td>${esc(phone || "-")}</td></tr><tr><td>About</td><td>${esc(MODELS[model])}</td></tr><tr><td>Newsletter</td><td>${newsletter ? "yes" : "no"}</td></tr></table><p style="white-space:pre-wrap">${esc(message || "(no message)")}</p><p style="color:#888;font-size:12px">Page ${esc(page)} · UTM ${esc(utm || "-")} · Referrer ${esc(referrer || "-")}</p>`;
  let mailed = false;
  try { mailed = await sendEmail(env, { to, subject: `Website enquiry – ${subject} – ${name}`, text, html, replyTo: email }); } catch (e) { console.log("enquiry email failed", String(e)); }
  if (newsletter) { try { await mailchimpSubscribe(env, { email, name, tags: ["Enquiry", MODELS[model]], source: "enquiry-form" }); } catch (e) { console.log("mailchimp failed", String(e)); } }
  if (!stored && !mailed) return json({ error: "The enquiry service isn't connected yet." }, 503);
  return json({ ok: true });
}
