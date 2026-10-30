#!/usr/bin/env python3
"""Builds the Langen website into dist/.

    pip install -r requirements.txt
    python3 build.py

Cloudflare Pages runs exactly this (build command `python3 build.py`, output directory `dist`).
Content lives in content/, page code in src/, source images in assets/.
"""
import os, re, sys, json, glob, shutil
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
from PIL import Image
from common import *
from pages import PAGES, NEWS, article_page
from content import load_assistant

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dist") + os.sep
SITE_URL = SITE["company"]["domain"]
WIDTHS = (640, 1200, 2000)

# ---------------------------------------------------------------- assets
def copy_assets():
    os.makedirs(OUT + "assets/r", exist_ok=True)
    for src in glob.glob(os.path.join(ROOT, "assets", "*")):
        if os.path.isfile(src):
            dst = OUT + "assets/" + os.path.basename(src)
            if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
                shutil.copy2(src, dst)
    for src in glob.glob(os.path.join(ROOT, "static", "*")):
        shutil.copy2(src, OUT + os.path.basename(src))

def variants():
    """WebP at three widths for every JPG (never upscaled). Skipped when up to date."""
    made = {}
    for src in sorted(glob.glob(os.path.join(ROOT, "assets", "*.jpg"))):
        name = os.path.splitext(os.path.basename(src))[0]
        im = None; outs = []
        for w in WIDTHS:
            if im is None:
                im = Image.open(src).convert("RGB")
            w2 = min(w, im.width)
            dst = f"{OUT}assets/r/{name}-{w2}.webp"
            if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
                r = im if w2 == im.width else im.resize((w2, round(im.height * w2 / im.width)), Image.LANCZOS)
                r.save(dst, "WEBP", quality=78, method=4)
            if w2 not in [o[0] for o in outs]:
                outs.append((w2, dst))
            if w2 == im.width:
                break
        made[name] = outs
    return made

IMG_RE = re.compile(r'<img\b([^>]*?)\bsrc="assets/([\w\-]+)\.jpg"([^>]*)>')
SIZES = (
    ('class="anno"', '(min-width:900px) 52vw, 100vw'),
    ('class="strip"', '(min-width:1100px) 34vw, (min-width:700px) 44vw, 78vw'),
    ('class="model"', '(min-width:760px) 50vw, 100vw'),
    ('class="pair"', '(min-width:700px) 50vw, 100vw'),
    ('class="studies"', '(min-width:1000px) 33vw, (min-width:700px) 50vw, 100vw'),
    ('class="news"', '(min-width:1000px) 33vw, (min-width:700px) 50vw, 100vw'),
    ('class="cpo"', '(min-width:760px) 50vw, 100vw'),
    ('class="callout"', '96px'),
    ('class="wrap split', '(min-width:860px) 50vw, 100vw'),
    ('class="card feature"', '(min-width:860px) 60vw, 100vw'),
)
def sizes_for(before, attrs):
    if 'class="bg"' in attrs:
        return "100vw"
    ctx = before[-900:]
    best, best_i = None, -1
    for key, val in SIZES:
        i = ctx.rfind(key)
        if i > best_i:
            best_i, best = i, val
    return best or "(min-width:1180px) 1132px, 100vw"

def responsive(html, made):
    out, pos = [], 0
    for m in IMG_RE.finditer(html):
        name = m.group(2)
        if name not in made:
            continue
        out.append(html[pos:m.start()])
        attrs = m.group(1) + m.group(3)
        srcset = ", ".join(f"assets/r/{name}-{w}.webp {w}w" for w, _ in made[name])
        sizes = sizes_for(html[:m.start()], attrs)
        img = m.group(0)
        if "decoding=" not in img:
            img = img[:-1] + ' decoding="async">'
        out.append(f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">{img}</picture>')
        pos = m.end()
    out.append(html[pos:])
    return "".join(out)

def preload_for(body, made):
    m = re.search(r'<img\b[^>]*fetchpriority="high"[^>]*\bsrc="assets/([\w\-]+)\.jpg"', body) or \
        re.search(r'<img\b[^>]*\bsrc="assets/([\w\-]+)\.jpg"[^>]*fetchpriority="high"', body)
    if not m or m.group(1) not in made:
        return ""
    name = m.group(1)
    srcset = ", ".join(f"assets/r/{name}-{w}.webp {w}w" for w, _ in made[name])
    return f'<link rel="preload" as="image" type="image/webp" imagesrcset="{srcset}" imagesizes="100vw">\n'

# ---------------------------------------------------------------- structured data
CO = SITE["company"]
ORG = {
  "@context": "https://schema.org", "@type": "Organization",
  "name": CO["name"], "legalName": CO["legal"], "url": SITE_URL, "logo": SITE_URL + "assets/langen_logo_white.svg",
  "address": {"@type": "PostalAddress", "streetAddress": CO["address_lines"][0], "addressLocality": "Wigan", "addressRegion": "Greater Manchester", "postalCode": "WN4 9DW", "addressCountry": "GB"},
  "telephone": CO["phone"], "email": CO["email"],
  "sameAs": ["https://www.instagram.com/langenmotorcycles/", "https://www.facebook.com/LangenMotorcycles/", "https://www.youtube.com/channel/UCXdvDfQtxKh5ncwrAJJo38A", "https://www.linkedin.com/company/langen-motorcycles/"],
}
PRODUCTS = {
  "lightspeed.html": {"@context": "https://schema.org", "@type": "Product", "name": "Langen Lightspeed", "brand": {"@type": "Brand", "name": "Langen Motorcycles"},
     "description": "A 1,190cc V-twin, 185 hp, 185 kg, limited to 185 commissioned builds. Hand-built to order in Wigan, England.",
     "image": SITE_URL + "assets/ls_og.jpg", "url": SITE_URL + "lightspeed",
     "offers": {"@type": "Offer", "priceCurrency": "GBP", "price": re.sub(r"[^\d]", "", SITE["lightspeed"]["price_from"]), "availability": "https://schema.org/PreOrder", "url": SITE_URL + "lightspeed"}},
  "two-stroke.html": {"@context": "https://schema.org", "@type": "Product", "name": "Langen Two Stroke", "brand": {"@type": "Brand", "name": "Langen Motorcycles"},
     "description": "249.5cc two-stroke V-twin, 76 hp, 120 kg. One hundred built, 2019–2025.", "image": SITE_URL + "assets/ts_studio.jpg", "url": SITE_URL + "two-stroke"},
}
def jsonld(fn, extra=None):
    blocks = [ORG] if fn == "index.html" else []
    if fn in PRODUCTS: blocks.append(PRODUCTS[fn])
    if fn == "contact.html": blocks.append({**ORG, "@type": "LocalBusiness", "priceRange": "££££"})
    if extra: blocks.append(extra)
    return "".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>\n' for b in blocks)

# ---------------------------------------------------------------- build
def page(fn, title, desc, canon, og, body, navkey, made, extra_ld=None):
    h = head(title, desc, canon, og)
    h = h.replace('<link rel="stylesheet" href="site.css">', preload_for(body, made) + jsonld(fn, extra_ld) + '<link rel="stylesheet" href="site.css">')
    html = h + nav(navkey) + '<main id="main">\n' + body + '\n</main>\n' + FOOTER
    html = responsive(html, made)
    with open(OUT + fn, "w", encoding="utf-8") as f:
        f.write(html)
    return len(html)

def main():
    os.makedirs(OUT, exist_ok=True)
    copy_assets()
    made = variants()
    with open(OUT + "site.css", "w", encoding="utf-8") as f: f.write(CSS)
    with open(OUT + "site.js", "w", encoding="utf-8") as f: f.write(JS)
    built = []
    for fn, (title, desc, canon, og, body, navkey) in PAGES.items():
        n = page(fn, title, desc, canon, og, body, navkey, made)
        built.append(fn); print(f"{fn:34s} {n // 1024:3d} KB")
    for it in NEWS:
        fn = f"news-{it['slug']}.html"
        ld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": it["title"], "datePublished": it["date"].isoformat(), "image": SITE_URL + it["image"] if it["image"] else None, "publisher": {"@type": "Organization", "name": CO["name"]}}
        n = page(fn, f"{it['title']} – Langen Motorcycles", it["summary"][:155], fn, it["image"] or "assets/ls_og.jpg", article_page(it), "news.html", made, ld)
        built.append(fn); print(f"{fn:34s} {n // 1024:3d} KB")
    # 404 for Cloudflare Pages
    nf = head("Page not found – Langen Motorcycles", "That page isn't here.", "404.html") + nav(None, solid=True) + '''<main id="main">
<section class="page-head" style="min-height:70vh">
  <div class="wrap">
    <div class="kicker">404</div>
    <h1>That page isn't here.</h1>
    <p class="lede">It may have moved when the site was rebuilt. The motorcycles are where you'd expect them.</p>
    <div class="btns" style="margin-top:30px"><a class="btn ghost" href="index.html">Home</a><a class="tlink" href="lightspeed.html">The Lightspeed</a></div>
  </div>
</section>
</main>
''' + FOOTER
    with open(OUT + "404.html", "w", encoding="utf-8") as f: f.write(responsive(nf, made))
    # assistant text, served as static files the Function reads at request time
    os.makedirs(OUT + "assistant", exist_ok=True)
    a = load_assistant()
    with open(OUT + "assistant/system.txt", "w", encoding="utf-8") as f: f.write(a["system"])
    with open(OUT + "assistant/knowledge.txt", "w", encoding="utf-8") as f: f.write(a["knowledge"])
    # sitemap + robots
    def loc(fn): return SITE_URL + ("" if fn == "index.html" else fn[:-5])
    pri = lambda fn: "1.0" if fn == "index.html" else "0.8" if fn in ("lightspeed.html", "commission.html", "pre-owned.html") else "0.5"
    with open(OUT + "sitemap.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                "".join(f"  <url><loc>{loc(fn)}</loc><priority>{pri(fn)}</priority></url>\n" for fn in built if fn not in ("owners.html",)) + "</urlset>\n")
    with open(OUT + "robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /assistant/\nSitemap: {SITE_URL}sitemap.xml\n")
    # favicon from the dark logo
    im = Image.open(os.path.join(ROOT, "assets", "langen_logo_dark.png")).convert("RGBA")
    bg = Image.new("RGBA", (256, 256), (14, 14, 16, 255))
    im.thumbnail((220, 220)); bg.paste(im, ((256 - im.width) // 2, (256 - im.height) // 2), im); bg.save(OUT + "assets/favicon.png")
    print(f"{len(built)} pages, {sum(len(v) for v in made.values())} image variants → dist/")

if __name__ == "__main__":
    main()
