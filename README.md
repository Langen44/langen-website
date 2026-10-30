# Langen Motorcycles – website

The site for langenmotorcycles.co.uk: a static site built by `build.py`, plus a handful of Cloudflare Pages Functions for the enquiry form, newsletter, brochure requests, Stripe deposits, the owners' portal and an optional assistant.

```
content/      what the site says – edit these (or use Pages CMS)
  site.yml      prices, counts, contact details, analytics IDs, feature switches
  news/         one Markdown file per article
  pre-owned/    one file per bike offered through the factory
  assistant/    the assistant's instructions and the facts it may use
assets/       source photos (JPG), logos, the brochure – the build makes the phone/laptop sizes
src/          page code (Python): common.py = layout/CSS/JS, pages.py = page copy, portal.py = owners' portal
functions/    Cloudflare Pages Functions (the /api/* endpoints)
static/       files copied as-is into the site (_redirects)
tools/        tests and checks
build.py      builds everything into dist/
```

## Edit content

- **News:** add `content/news/YYYY-MM-DD-slug.md` with the front matter you see in the existing files. The build makes `news-slug.html` and the cards everywhere.
- **Pre-owned:** add or edit `content/pre-owned/*.md`; set `status: sold` to retire a bike without deleting its record.
- **Facts:** `content/site.yml`.
- Or sign in to [Pages CMS](https://app.pagescms.org) with GitHub and edit all of the above as forms.

Every change to `main` deploys automatically; a change on any other branch gets its own preview link.

## Build locally

```
pip install -r requirements.txt
python3 build.py              # → dist/
node tools/mock-server.mjs    # serves dist/ with a pretend /api at http://127.0.0.1:8790
node tools/test-functions.mjs # exercises the Functions against stubbed bindings
python3 tools/check-links.py  # no broken links in dist/
```

## Deploy

See **DEPLOY.md** – Cloudflare Pages connected to this repository, one D1 database, one R2 bucket, and the secrets for email, Mailchimp, Stripe and (optionally) the assistant.
