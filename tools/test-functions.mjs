// Runs the API Functions against stubbed bindings. `node tools/test-functions.mjs`
import { md5 } from "../functions/_lib.js";
import * as enquire from "../functions/api/enquire.js";
import * as subscribe from "../functions/api/subscribe.js";
import * as brochure from "../functions/api/brochure.js";
import * as stripe from "../functions/api/stripe-webhook.js";
import * as assist from "../functions/api/assist.js";
import * as resetReq from "../functions/api/reset-request.js";
import * as reset from "../functions/api/reset.js";
import * as register from "../functions/api/register.js";
import * as login from "../functions/api/login.js";

let fails = 0;
const ok = (c, m) => { if (c) console.log("  ✓", m); else { fails++; console.log("  ✗", m); } };

// ---- stub D1 ----
function fakeDB() {
  const rows = { owners: [{ model: "lightspeed", number: "007", name: "Shashi Test", email: "owner@example.com", activation_code: "LS7-K4PQ-2M", password_hash: null, password_salt: null }], enquiries: [], subscribers: [], reservations: [], conversations: [], ratelimit: new Map() };
  const db = { rows, prepare(sql) { return { sql, args: [], bind(...a) { this.args = a; return this; },
    async first() {
      if (sql.includes("FROM owners")) { const [m, n] = this.args; return rows.owners.find((o) => o.model === m && o.number === n) || null; }
      if (sql.includes("FROM ratelimit")) return rows.ratelimit.get(this.args[0]) || null;
      if (sql.includes("MAX(build_number)")) return { n: rows.reservations.length + 1 };
      return null; },
    async run() {
      if (sql.startsWith("INSERT INTO enquiries")) rows.enquiries.push(this.args);
      else if (sql.startsWith("INSERT INTO subscribers")) rows.subscribers.push(this.args);
      else if (sql.startsWith("INSERT OR IGNORE INTO reservations")) rows.reservations.push(this.args);
      else if (sql.startsWith("INSERT INTO conversations")) rows.conversations.push(this.args);
      else if (sql.startsWith("INSERT OR REPLACE INTO ratelimit")) rows.ratelimit.set(this.args[0], { count: 1, window_start: this.args[1] });
      else if (sql.startsWith("UPDATE ratelimit")) { const r = rows.ratelimit.get(this.args[0]); r.count++; }
      else if (sql.startsWith("UPDATE owners SET password_hash = ?")) { const o = rows.owners.find((x) => x.model === this.args[2] && x.number === this.args[3]); o.password_hash = this.args[0]; o.password_salt = this.args[1]; }
      return { success: true }; } }; } };
  return db;
}
// ---- stub fetch ----
const calls = [];
globalThis.fetch = async (url, opts = {}) => {
  calls.push({ url: String(url), opts });
  const u = String(url);
  if (u.includes("turnstile")) return new Response(JSON.stringify({ success: JSON.parse(opts.body).response === "good" }));
  if (u.includes("resend.com")) return new Response("{}", { status: 200 });
  if (u.includes("mailchimp.com")) return new Response(JSON.stringify({ status: "pending" }), { status: 200 });
  if (u.includes("anthropic.com")) return new Response(JSON.stringify({ content: [{ type: "text", text: "From £37,000 plus VAT." }] }), { status: 200 });
  if (u.endsWith("/assistant/system.txt")) return new Response("SYSTEM");
  if (u.endsWith("/assistant/knowledge.txt")) return new Response("KNOWLEDGE");
  return new Response("not found", { status: 404 });
};
const req = (path, body, headers = {}) => new Request("https://example.test" + path, { method: "POST", headers: { "content-type": "application/json", "cf-connecting-ip": "1.2.3.4", ...headers }, body: typeof body === "string" ? body : JSON.stringify(body) });
const base = { SESSION_SECRET: "test-secret-please-change", RESEND_API_KEY: "re_test", MAILCHIMP_API_KEY: "abc-us21", MAILCHIMP_AUDIENCE: "aud1" };

console.log("md5");
ok((await md5("hello")) === "5d41402abc4b2a76b9719d911017c592", "md5 matches reference");

console.log("enquire");
{ const env = { ...base, DB: fakeDB() };
  let r = await enquire.onRequestPost({ request: req("/api/enquire", { name: "A", email: "nope" }), env }); ok(r.status === 400, "rejects bad email");
  calls.length = 0; r = await enquire.onRequestPost({ request: req("/api/enquire", { name: "Bot", email: "b@x.com", website: "spam" }), env });
  ok(r.status === 200 && env.DB.rows.enquiries.length === 0 && calls.length === 0, "honeypot swallows silently");
  calls.length = 0; r = await enquire.onRequestPost({ request: req("/api/enquire", { name: "Paul Aherns", email: "paul@example.com", country: "USA", model: "lightspeed", subject: "Lightspeed enquiry", message: "Bronze?", newsletter: "1", page: "/lightspeed", utm: "?utm_source=facebook" }), env });
  const j = await r.json(); ok(r.status === 200 && j.ok, "accepts a valid enquiry");
  ok(env.DB.rows.enquiries.length === 1 && env.DB.rows.enquiries[0][0] === "Paul Aherns", "stores in D1");
  const mail = calls.find((c) => c.url.includes("resend")); const body = JSON.parse(mail.opts.body);
  ok(mail && body.reply_to === "paul@example.com" && body.subject.includes("Paul Aherns"), "emails the team with reply-to set");
  ok(calls.some((c) => c.url.includes("mailchimp") && c.opts.method === "PUT"), "subscribes to Mailchimp when ticked");
  const envT = { ...env, TURNSTILE_SECRET: "s" };
  r = await enquire.onRequestPost({ request: req("/api/enquire", { name: "A", email: "a@b.co", turnstile: "bad" }), env: envT }); ok(r.status === 400, "turnstile enforced when configured");
  r = await enquire.onRequestPost({ request: req("/api/enquire", { name: "A", email: "a@b.co", turnstile: "good" }), env: envT }); ok(r.status === 200, "turnstile passes with a good token");
  const envNone = { SESSION_SECRET: "x" };
  r = await enquire.onRequestPost({ request: req("/api/enquire", { name: "A", email: "a@b.co" }), env: envNone }); ok(r.status === 503, "503 when nothing is connected (front end falls back to email)");
  const envDbOnly = { SESSION_SECRET: "x", DB: fakeDB() };
  r = await enquire.onRequestPost({ request: req("/api/enquire", { name: "A", email: "a@b.co" }), env: envDbOnly }); ok(r.status === 503 && envDbOnly.DB.rows.enquiries.length === 1, "no email key: stored but visitor is sent to the email link (nothing silent)");
}
console.log("subscribe / brochure");
{ const env = { ...base, DB: fakeDB() }; calls.length = 0;
  let r = await subscribe.onRequestPost({ request: req("/api/subscribe", { email: "news@example.com", source: "footer" }), env }); ok(r.status === 200, "subscribe ok");
  const mc = calls.find((c) => c.url.includes("mailchimp")); ok(mc && mc.url.includes("us21.api.mailchimp.com/3.0/lists/aud1/members/" + (await md5("news@example.com"))), "Mailchimp URL uses dc + md5 member id");
  r = await brochure.onRequestPost({ request: req("/api/brochure", { email: "b@example.com", name: "Bea" }), env }); const j = await r.json();
  ok(r.status === 200 && j.url === "https://example.test/assets/Langen_Lightspeed_Brochure.pdf", "brochure returns the PDF url");
  ok(env.DB.rows.subscribers.length === 2, "both recorded in D1");
}
console.log("stripe webhook");
{ const env = { ...base, DB: fakeDB(), STRIPE_WEBHOOK_SECRET: "whsec_test" };
  const payload = JSON.stringify({ type: "checkout.session.completed", data: { object: { id: "cs_1", amount_total: 100000, currency: "gbp", customer_details: { email: "dep@example.com", name: "Dep Ositor", address: { country: "GB" } } } } });
  const t = Math.floor(Date.now() / 1000);
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode("whsec_test"), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = [...new Uint8Array(await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(`${t}.${payload}`)))].map((b) => b.toString(16).padStart(2, "0")).join("");
  let r = await stripe.onRequestPost({ request: req("/api/stripe-webhook", payload, { "stripe-signature": `t=${t},v1=deadbeef` }), env }); ok(r.status === 400, "rejects a bad signature");
  r = await stripe.onRequestPost({ request: req("/api/stripe-webhook", payload, { "stripe-signature": `t=${t},v1=${sig}` }), env }); const j = await r.json();
  ok(r.status === 200 && j.build_number === 1 && env.DB.rows.reservations.length === 1, "records the deposit with build number 1");
}
console.log("assistant");
{ let r = await assist.onRequestPost({ request: req("/api/assist", { messages: [{ role: "user", content: "price?" }] }), env: { ...base } }); ok(r.status === 404, "off by default");
  const env = { ...base, DB: fakeDB(), ANTHROPIC_API_KEY: "k", ASSISTANT_ENABLED: "1" }; calls.length = 0;
  r = await assist.onRequestPost({ request: req("/api/assist", { messages: [{ role: "user", content: "How much is a Lightspeed?" }], page: "/" }), env }); const j = await r.json();
  ok(r.status === 200 && j.reply.includes("£37,000"), "answers when enabled");
  const a = calls.find((c) => c.url.includes("anthropic")); const b = JSON.parse(a.opts.body);
  ok(b.system.includes("SYSTEM") && b.system.includes("KNOWLEDGE") && b.max_tokens === 400, "prompt built from the static files");
  ok(env.DB.rows.conversations.length === 1, "logged to D1");
}
console.log("portal: register, login, reset");
{ const env = { ...base, DB: fakeDB() };
  let r = await register.onRequestPost({ request: req("/api/register", { model: "lightspeed", number: "7", code: "ls7 k4pq 2m", password: "longpassword1" }), env }); ok(r.status === 200, "register with activation code");
  r = await login.onRequestPost({ request: req("/api/login", { model: "lightspeed", number: "007", password: "longpassword1" }), env }); ok(r.status === 200, "login works");
  calls.length = 0; r = await resetReq.onRequestPost({ request: req("/api/reset-request", { model: "lightspeed", number: "007", email: "owner@example.com" }), env }); ok(r.status === 200, "reset request accepted");
  const mail = calls.find((c) => c.url.includes("resend")); const token = decodeURIComponent(/reset=([^\s]+)/.exec(JSON.parse(mail.opts.body).text)[1]);
  r = await reset.onRequestPost({ request: req("/api/reset", { token, password: "anotherlongpass2" }), env }); ok(r.status === 200, "reset sets a new password from the link");
  r = await login.onRequestPost({ request: req("/api/login", { model: "lightspeed", number: "007", password: "anotherlongpass2" }), env }); ok(r.status === 200, "login with the new password");
  calls.length = 0; r = await resetReq.onRequestPost({ request: req("/api/reset-request", { model: "lightspeed", number: "007", email: "wrong@example.com" }), env }); ok(r.status === 200 && !calls.some((c) => c.url.includes("resend")), "wrong email: same reply, no mail (no probing)");
}
console.log(fails ? `\n${fails} FAILED` : "\nall passed");
process.exit(fails ? 1 : 0);
