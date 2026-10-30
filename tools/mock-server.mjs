// Serves dist/ with a pretend /api so the forms can be exercised locally: `node tools/mock-server.mjs 8790`
import http from "node:http"; import fs from "node:fs"; import path from "node:path";
const root = path.resolve(import.meta.dirname, "..", "dist"), port = Number(process.argv[2] || 8790);
const types = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".webp": "image/webp", ".jpg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml", ".pdf": "application/pdf", ".txt": "text/plain", ".xml": "application/xml" };
http.createServer((req, res) => {
  const u = new URL(req.url, "http://x");
  if (u.pathname.startsWith("/api/")) {
    let body = ""; req.on("data", (c) => body += c); req.on("end", () => {
      const j = (o, s = 200) => { res.writeHead(s, { "content-type": "application/json" }); res.end(JSON.stringify(o)); };
      const p = u.pathname.slice(5); let b = {}; try { b = JSON.parse(body || "{}"); } catch {}
      if (p === "enquire") return b.email === "fail@example.com" ? j({ error: "Pretend failure" }, 500) : j({ ok: true });
      if (p === "subscribe") return j({ ok: true });
      if (p === "brochure") return j({ ok: true, url: "/assets/Langen_Lightspeed_Brochure.pdf" });
      if (p === "assist") return j({ reply: "From £37,000 plus VAT, with the standard silver-over-bronze colourway included." });
      if (p === "me") return j({ error: "Not signed in" }, 401);
      if (p === "reset-request") return j({ ok: true, message: "If those details match our records, a reset link is on its way." });
      return j({ error: "mock: unknown" }, 404);
    }); return;
  }
  let f = path.join(root, decodeURIComponent(u.pathname)); if (u.pathname === "/") f = path.join(root, "index.html");
  if (!fs.existsSync(f) && fs.existsSync(f + ".html")) f += ".html";
  if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end("404"); }
  res.writeHead(200, { "content-type": types[path.extname(f)] || "application/octet-stream" }); fs.createReadStream(f).pipe(res);
}).listen(port, "127.0.0.1", () => console.log("mock on http://127.0.0.1:" + port));
