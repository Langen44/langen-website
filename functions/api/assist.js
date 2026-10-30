import { json, clean, ip, rateLimited } from "../_lib.js";
// POST /api/assist – "Ask the workshop". Answers only from /assistant/knowledge.txt with /assistant/system.txt as instructions.
// Needs ANTHROPIC_API_KEY and ASSISTANT_ENABLED=1 in Cloudflare; logs each exchange to D1 (conversations) when bound.
const MODEL = "claude-sonnet-4-5";
export async function onRequestPost({ request, env }) {
  if (env.ASSISTANT_ENABLED !== "1" || !env.ANTHROPIC_API_KEY) return json({ error: "The assistant isn't switched on yet – the team will answer by email." }, 404);
  if (await rateLimited(env, request, "assist", 40, 3600)) return json({ error: "That's plenty of questions for now – the team will take it from here if you use the enquiry form." }, 429);
  let b; try { b = await request.json(); } catch { return json({ error: "Bad request" }, 400); }
  const msgs = (Array.isArray(b.messages) ? b.messages : []).slice(-8).map((m) => ({ role: m.role === "assistant" ? "assistant" : "user", content: clean(m.content, 1000) })).filter((m) => m.content);
  if (!msgs.length || msgs[msgs.length - 1].role !== "user") return json({ error: "Ask a question." }, 400);
  const base = new URL(request.url).origin;
  const [system, knowledge] = await Promise.all([fetch(base + "/assistant/system.txt").then((r) => r.text()), fetch(base + "/assistant/knowledge.txt").then((r) => r.text())]);
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify({ model: env.ASSISTANT_MODEL || MODEL, max_tokens: 400, temperature: 0.3,
      system: `${system}\n\n# Knowledge (the only facts you may use)\n${knowledge}`, messages: msgs }),
  });
  if (!r.ok) { console.log("anthropic error", r.status, await r.text()); return json({ error: "I can't answer just now – the team will, if you use the enquiry form." }, 502); }
  const j = await r.json();
  const reply = (j.content || []).filter((c) => c.type === "text").map((c) => c.text).join("\n").trim() || "I'm not sure – the team will know. Use the enquiry form and they'll come back to you.";
  if (env.DB) { try { await env.DB.prepare("INSERT INTO conversations (ip, page, question, answer) VALUES (?,?,?,?)").bind(ip(request), clean(b.page, 200), msgs[msgs.length - 1].content, reply).run(); } catch {} }
  return json({ reply });
}
