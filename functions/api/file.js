import { readSession } from "../_lib.js";
// Streams a file from R2 if the signed-in owner is allowed to see it. Supports Range for video.
export async function onRequestGet({ request, env }) {
  const s = await readSession(request, env);
  if (!s) return new Response("Not signed in", { status: 401 });
  const key = new URL(request.url).searchParams.get("key") || "";
  const allowed = key.startsWith(`${s.model}/${s.number}/`) || key.startsWith(`${s.model}/shared/`);
  if (!allowed || key.includes("..")) return new Response("Forbidden", { status: 403 });
  const range = request.headers.get("range");
  const obj = await env.FILES.get(key, range ? { range: request.headers } : undefined);
  if (!obj) return new Response("Not found", { status: 404 });
  const h = new Headers();
  obj.writeHttpMetadata(h);
  h.set("etag", obj.httpEtag);
  h.set("accept-ranges", "bytes");
  h.set("cache-control", "private, max-age=0");
  h.set("content-disposition", `inline; filename="${key.split("/").pop()}"`);
  if (obj.range) {
    const start = obj.range.offset ?? 0, len = obj.range.length ?? (obj.size - start);
    h.set("content-range", `bytes ${start}-${start + len - 1}/${obj.size}`);
    h.set("content-length", String(len));
    return new Response(obj.body, { status: 206, headers: h });
  }
  h.set("content-length", String(obj.size));
  return new Response(obj.body, { headers: h });
}
