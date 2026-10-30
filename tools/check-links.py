"""Fails if any page in dist/ links to a file that doesn't exist. Run after build.py."""
import re, os, glob, sys
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dist")
bad = []
for f in glob.glob(os.path.join(root, "*.html")):
    h = re.sub(r"<!--.*?-->", "", open(f, encoding="utf-8").read(), flags=re.S)
    for m in re.finditer(r'(?:href|src|srcset|imagesrcset)="([^"]+)"', h):
        for part in m.group(1).split(","):
            u = part.strip().split(" ")[0].split("#")[0].split("?")[0]
            if not u or u.startswith(("http", "mailto:", "tel:", "data:", "/api/")): continue
            if not os.path.exists(os.path.join(root, u)): bad.append((os.path.basename(f), u))
if bad:
    print("Broken links:"); [print(" ", f, "->", u) for f, u in sorted(set(bad))]; sys.exit(1)
print(f"links ok ({len(glob.glob(os.path.join(root, '*.html')))} pages)")
