import { json, readSession, getOwner, modelName } from "../_lib.js";
// Returns the signed-in owner and the files they may see:
//   FILES bucket layout:  <model>/<number>/...   (this bike only)
//                         <model>/shared/...     (every owner of that model)
export async function onRequestGet({ request, env }) {
  const s = await readSession(request, env);
  if (!s) return json({ error: "Not signed in" }, 401);
  const o = await getOwner(env, s.model, s.number);
  if (!o) return json({ error: "Not signed in" }, 401);
  async function list(prefix) {
    const out = []; let cursor;
    do {
      const r = await env.FILES.list({ prefix, cursor, include: ["httpMetadata", "customMetadata"] });
      for (const obj of r.objects) {
        if (obj.key.endsWith("/")) continue;
        const name = obj.key.slice(prefix.length);
        out.push({ key: obj.key, name, size: obj.size, uploaded: obj.uploaded, type: obj.httpMetadata?.contentType || guessType(name), title: obj.customMetadata?.title || prettify(name) });
      }
      cursor = r.truncated ? r.cursor : undefined;
    } while (cursor);
    return out.sort((a, b) => a.name.localeCompare(b.name));
  }
  const mine = await list(`${s.model}/${s.number}/`);
  const shared = await list(`${s.model}/shared/`);
  return json({ model: s.model, modelName: modelName(s.model), number: s.number, name: o.name || "", mine, shared });
}
function guessType(n) {
  n = n.toLowerCase();
  if (n.endsWith(".pdf")) return "application/pdf";
  if (/\.(mp4|m4v)$/.test(n)) return "video/mp4"; if (n.endsWith(".mov")) return "video/quicktime"; if (n.endsWith(".webm")) return "video/webm";
  if (/\.(jpe?g)$/.test(n)) return "image/jpeg"; if (n.endsWith(".png")) return "image/png";
  return "application/octet-stream";
}
function prettify(n) { return n.replace(/\.[a-z0-9]+$/i, "").replace(/[_-]+/g, " ").replace(/^\d+\s*/, "").trim(); }
