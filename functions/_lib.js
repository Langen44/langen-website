// Shared helpers for the Langen owners' portal (Cloudflare Pages Functions).
// Bindings expected: env.DB (D1), env.FILES (R2), env.SESSION_SECRET (secret string).

const enc = new TextEncoder();
const MODELS = { lightspeed: "Lightspeed", "two-stroke": "Two Stroke" };
const SESSION_DAYS = 30;

export const json = (data, status = 200, headers = {}) =>
  new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...headers } });

export function normModel(m) { m = String(m || "").toLowerCase().trim(); return MODELS[m] ? m : null; }
export function normNumber(n) { n = String(n || "").replace(/\D/g, ""); if (!n) return null; return n.padStart(3, "0").slice(-3); }
export function modelName(m) { return MODELS[m] || m; }

// ---- password hashing: PBKDF2-SHA256, 100k iterations, 16-byte salt ----
const b64 = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf)));
const unb64 = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));

export async function hashPassword(password, saltB64) {
  const salt = saltB64 ? unb64(saltB64) : crypto.getRandomValues(new Uint8Array(16));
  const key = await crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt, iterations: 100000 }, key, 256);
  return { hash: b64(bits), salt: b64(salt) };
}
export async function verifyPassword(password, hash, salt) {
  const h = await hashPassword(password, salt);
  return timingSafeEqual(h.hash, hash);
}
function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}

// ---- sessions: HMAC-signed cookie "model.number.exp.sig" ----
async function hmac(secret, msg) {
  const key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return b64(await crypto.subtle.sign("HMAC", key, enc.encode(msg))).replace(/=+$/, "");
}
export async function makeSession(env, model, number) {
  const exp = Math.floor(Date.now() / 1000) + SESSION_DAYS * 86400;
  const payload = `${model}.${number}.${exp}`;
  const sig = await hmac(env.SESSION_SECRET, payload);
  const value = `${payload}.${sig}`;
  return { value, cookie: `ln_session=${value}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_DAYS * 86400}` };
}
export const clearCookie = "ln_session=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0";

export async function readSession(request, env) {
  const m = /(?:^|;\s*)ln_session=([^;]+)/.exec(request.headers.get("cookie") || "");
  if (!m) return null;
  const parts = m[1].split(".");
  if (parts.length !== 4) return null;
  const [model, number, exp, sig] = parts;
  if (Number(exp) < Date.now() / 1000) return null;
  const expect = await hmac(env.SESSION_SECRET, `${model}.${number}.${exp}`);
  if (!timingSafeEqual(sig, expect)) return null;
  return { model, number };
}

export async function getOwner(env, model, number) {
  return env.DB.prepare("SELECT model, number, name, activation_code, password_hash, password_salt, created_at, activated_at FROM owners WHERE model = ? AND number = ?").bind(model, number).first();
}

// Rate limiting (per IP, per route) using D1 — small and good enough for this volume.
export async function rateLimited(env, request, route, max = 10, windowSec = 900) {
  if (!env.DB) return false; // no database bound (preview deploys): don't block, don't crash
  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  const key = `${route}:${ip}`;
  const now = Math.floor(Date.now() / 1000);
  const row = await env.DB.prepare("SELECT count, window_start FROM ratelimit WHERE key = ?").bind(key).first();
  if (!row || now - row.window_start > windowSec) {
    await env.DB.prepare("INSERT OR REPLACE INTO ratelimit (key, count, window_start) VALUES (?, 1, ?)").bind(key, now).run();
    return false;
  }
  if (row.count >= max) return true;
  await env.DB.prepare("UPDATE ratelimit SET count = count + 1 WHERE key = ?").bind(key).run();
  return false;
}

// ---------------------------------------------------------------- shared helpers for the forms, email and lists
export function clean(s, max = 500) { return String(s ?? "").replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "").trim().slice(0, max); }
export function isEmail(s) { return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(s || "")); }
export function esc(s) { return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
export function ip(request) { return request.headers.get("cf-connecting-ip") || "unknown"; }

// Cloudflare Turnstile – only enforced when the secret is configured.
export async function turnstileOk(env, request, token) {
  if (!env.TURNSTILE_SECRET) return true;
  if (!token) return false;
  try {
    const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ secret: env.TURNSTILE_SECRET, response: token, remoteip: ip(request) }),
    });
    const j = await r.json();
    return !!j.success;
  } catch { return false; }
}

// Transactional email through Resend. No-op (returns false) until RESEND_API_KEY is set.
export async function sendEmail(env, { to, subject, text, html, replyTo }) {
  if (!env.RESEND_API_KEY) return false;
  const from = env.MAIL_FROM || "Langen Motorcycles <enquiries@langenmotorcycles.co.uk>";
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { authorization: `Bearer ${env.RESEND_API_KEY}`, "content-type": "application/json" },
    body: JSON.stringify({ from, to: Array.isArray(to) ? to : [to], subject, text, html, reply_to: replyTo }),
  });
  return r.ok;
}

// Mailchimp audience subscribe (idempotent: PUT by email hash). No-op until MAILCHIMP_API_KEY + MAILCHIMP_AUDIENCE are set.
export async function mailchimpSubscribe(env, { email, name, tags = [], source = "website" }) {
  if (!env.MAILCHIMP_API_KEY || !env.MAILCHIMP_AUDIENCE) return { ok: false, skipped: true };
  const dc = env.MAILCHIMP_API_KEY.split("-").pop();
  const hash = await md5(email.trim().toLowerCase());
  const [first, ...rest] = String(name || "").trim().split(/\s+/);
  const body = {
    email_address: email, status_if_new: env.MAILCHIMP_DOUBLE_OPTIN === "0" ? "subscribed" : "pending",
    merge_fields: { FNAME: first || "", LNAME: rest.join(" ") },
    tags: [...new Set([source, ...tags].filter(Boolean))],
  };
  const r = await fetch(`https://${dc}.api.mailchimp.com/3.0/lists/${env.MAILCHIMP_AUDIENCE}/members/${hash}`, {
    method: "PUT", headers: { authorization: `Basic ${btoa("anystring:" + env.MAILCHIMP_API_KEY)}`, "content-type": "application/json" },
    body: JSON.stringify(body),
  });
  const j = await r.json().catch(() => ({}));
  if (r.ok && body.tags.length) {
    await fetch(`https://${dc}.api.mailchimp.com/3.0/lists/${env.MAILCHIMP_AUDIENCE}/members/${hash}/tags`, {
      method: "POST", headers: { authorization: `Basic ${btoa("anystring:" + env.MAILCHIMP_API_KEY)}`, "content-type": "application/json" },
      body: JSON.stringify({ tags: body.tags.map((t) => ({ name: t, status: "active" })) }),
    }).catch(() => {});
  }
  return { ok: r.ok, status: r.status, detail: j.title || j.detail };
}

// Workers have no MD5 in SubtleCrypto; Mailchimp needs it for the member id. Small, standard implementation.
export async function md5(str) {
  const bytes = enc.encode(str);
  function rotl(x, c) { return (x << c) | (x >>> (32 - c)); }
  const K = Array.from({ length: 64 }, (_, i) => Math.floor(Math.abs(Math.sin(i + 1)) * 2 ** 32));
  const S = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21];
  const len = bytes.length, bitLen = len * 8;
  const padded = new Uint8Array(((len + 8) >> 6 << 6) + 64);
  padded.set(bytes); padded[len] = 0x80;
  const dv = new DataView(padded.buffer);
  dv.setUint32(padded.length - 8, bitLen >>> 0, true); dv.setUint32(padded.length - 4, Math.floor(bitLen / 2 ** 32), true);
  let a0 = 0x67452301, b0 = 0xefcdab89, c0 = 0x98badcfe, d0 = 0x10325476;
  for (let off = 0; off < padded.length; off += 64) {
    const M = Array.from({ length: 16 }, (_, i) => dv.getUint32(off + i * 4, true));
    let A = a0, B = b0, C = c0, D = d0;
    for (let i = 0; i < 64; i++) {
      let F, g;
      if (i < 16) { F = (B & C) | (~B & D); g = i; }
      else if (i < 32) { F = (D & B) | (~D & C); g = (5 * i + 1) % 16; }
      else if (i < 48) { F = B ^ C ^ D; g = (3 * i + 5) % 16; }
      else { F = C ^ (B | ~D); g = (7 * i) % 16; }
      F = (F + A + K[i] + M[g]) >>> 0;
      A = D; D = C; C = B; B = (B + rotl(F, S[i])) >>> 0;
    }
    a0 = (a0 + A) >>> 0; b0 = (b0 + B) >>> 0; c0 = (c0 + C) >>> 0; d0 = (d0 + D) >>> 0;
  }
  return [a0, b0, c0, d0].map((v) => [v & 255, (v >> 8) & 255, (v >> 16) & 255, (v >>> 24) & 255].map((b) => b.toString(16).padStart(2, "0")).join("")).join("");
}

// Signed, time-limited tokens (password reset links). payload is a short string without dots.
export async function signToken(env, payload, ttlSec) {
  const exp = Math.floor(Date.now() / 1000) + ttlSec;
  const msg = `${payload}.${exp}`;
  const sig = await hmacHex(env.SESSION_SECRET, msg);
  return `${msg}.${sig}`;
}
export async function verifyToken(env, token) {
  const parts = String(token || "").split(".");
  if (parts.length < 3) return null;
  const sig = parts.pop(), exp = parts.pop(), payload = parts.join(".");
  if (Number(exp) < Date.now() / 1000) return null;
  const expect = await hmacHex(env.SESSION_SECRET, `${payload}.${exp}`);
  return timingSafeEqual(sig, expect) ? payload : null;
}
async function hmacHex(secret, msg) {
  const key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return [...new Uint8Array(await crypto.subtle.sign("HMAC", key, enc.encode(msg)))].map((b) => b.toString(16).padStart(2, "0")).join("");
}
export async function hmacSha256Hex(secret, msg) { return hmacHex(secret, msg); }
export { timingSafeEqual };
