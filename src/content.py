"""Loads everything under content/: site facts, news articles, pre-owned listings, assistant text."""
import os, re, glob, datetime
import yaml
import markdown as md

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
CONTENT = os.path.join(ROOT, "content")

def _front_matter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    return (yaml.safe_load(m.group(1)) or {}), m.group(2)

def render_md(text):
    return md.markdown(text.strip(), extensions=["smarty", "sane_lists"]) if text.strip() else ""

def load_site():
    with open(os.path.join(CONTENT, "site.yml"), encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_news():
    items = []
    for path in glob.glob(os.path.join(CONTENT, "news", "*.md")):
        with open(path, encoding="utf-8") as f:
            fm, body = _front_matter(f.read())
        slug = os.path.splitext(os.path.basename(path))[0]
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug)
        d = fm.get("date")
        if isinstance(d, str):
            d = datetime.date.fromisoformat(d[:10])
        if d is None:
            d = datetime.date.today()
        items.append({
            "slug": slug,
            "href": f"news-{slug}.html",
            "title": fm.get("title", slug.replace("-", " ").title()),
            "date": d,
            "date_display": d.strftime("%B %Y"),
            "date_long": d.strftime("%-d %B %Y"),
            "summary": fm.get("summary", ""),
            "image": fm.get("image", ""),
            "image_alt": fm.get("image_alt", ""),
            "feature": bool(fm.get("feature")),
            "body_html": render_md(body),
            "external": fm.get("link", ""),
        })
    items.sort(key=lambda i: i["date"], reverse=True)
    return items

def load_preowned():
    bikes = []
    for path in sorted(glob.glob(os.path.join(CONTENT, "pre-owned", "*.md"))):
        with open(path, encoding="utf-8") as f:
            fm, body = _front_matter(f.read())
        fm.setdefault("status", "available")
        fm["number"] = str(fm.get("number", "")).zfill(3)
        fm["highlights"] = fm.get("highlights") or []
        fm["body_html"] = render_md(body)
        bikes.append(fm)
    return bikes

def load_assistant():
    out = {}
    for name in ("system", "knowledge"):
        p = os.path.join(CONTENT, "assistant", f"{name}.md")
        out[name] = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    return out
