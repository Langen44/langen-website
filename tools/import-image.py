"""Copy a library image into assets/ as a web-source JPG: python3 tools/import-image.py <src.webp> <assets/name.jpg>"""
import sys
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
if im.width > 2000:
    im = im.resize((2000, round(im.height * 2000 / im.width)), Image.LANCZOS)
im.save(dst, quality=88, optimize=True, progressive=True)
print(dst, im.size)
