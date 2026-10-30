# Deploying the Langen website

Everything runs on one Cloudflare account. Nothing here needs a terminal; every step is in the Cloudflare dashboard. Budget twenty minutes the first time. Nothing goes on the real domain until step 7.

## 1. Connect the repository

Cloudflare dashboard → **Workers & Pages → Create → Pages → Connect to Git** → choose this repository.

| Setting | Value |
| --- | --- |
| Production branch | `main` |
| Build command | `pip install -r requirements.txt && python3 build.py` |
| Build output directory | `dist` |
| Environment variable | `PYTHON_VERSION` = `3.12` |

Save and deploy. The first build takes two to three minutes (it makes the image sizes); you get a `*.pages.dev` link at the end. Every later push to `main` redeploys; every other branch gets a preview link of its own.

## 2. Database (D1)

**Workers & Pages → D1 → Create** → name it `langen-site`. Open it → **Console** → paste the whole of `schema.sql` → Execute. Safe to run again later.

Then in the Pages project: **Settings → Functions → D1 database bindings → Add**: variable name `DB`, database `langen-site`. Do this for Production and Preview.

## 3. Owner files (R2)

**R2 → Create bucket** → `langen-owner-files`. Pages project → **Settings → Functions → R2 bucket bindings → Add**: variable name `FILES`, bucket `langen-owner-files`.

Folder layout inside the bucket (create folders by uploading into them):

```
lightspeed/007/        documents and videos for that bike only
lightspeed/shared/     every Lightspeed owner sees these (handbook, service schedule)
two-stroke/024/
two-stroke/shared/
```

File names become titles (`03-build-record.pdf` → "build record"), so number them to control the order.

## 4. Secrets

Pages project → **Settings → Environment variables → Add** (tick *Encrypt* for each). Set them for Production; the same values work for Preview.

| Name | Where it comes from | Needed for |
| --- | --- | --- |
| `SESSION_SECRET` | Any long random string (40+ characters) | Owners' portal sign-in and reset links – **required** |
| `RESEND_API_KEY` | resend.com → API keys. First verify the domain under Domains (two DNS records; Cloudflare adds them in one click once DNS is here) | Enquiry emails to you, brochure emails, password resets |
| `MAIL_FROM` | e.g. `Langen Motorcycles <enquiries@langenmotorcycles.co.uk>` | Sender name on those emails (defaults to that) |
| `ENQUIRY_TO` | e.g. `info@langenmotorcycles.co.uk` | Where enquiries land (defaults to that) |
| `MAILCHIMP_API_KEY` | Mailchimp → Account → Extras → API keys | Newsletter and brochure sign-ups |
| `MAILCHIMP_AUDIENCE` | Mailchimp → Audience → Settings → Audience name and defaults → Audience ID | same |
| `MAILCHIMP_DOUBLE_OPTIN` | `1` (default) sends a confirmation email; `0` adds people straight away | optional |
| `TURNSTILE_SECRET` | Cloudflare → Turnstile → Add site (domain: your site) → secret key. Put the **site key** in `content/site.yml` → `forms.turnstile_site_key` | Invisible spam protection on the forms |
| `STRIPE_WEBHOOK_SECRET` | Stripe → Developers → Webhooks → Add endpoint `https://<your site>/api/stripe-webhook`, event `checkout.session.completed` → signing secret | Recording deposits in the database |
| `ANTHROPIC_API_KEY` | console.anthropic.com | The assistant (optional) |
| `ASSISTANT_ENABLED` | `1` to switch the assistant's API on (and set `features.assistant: true` in `content/site.yml` to show the button) | optional |

Until a key is set, that feature degrades quietly: the enquiry form falls back to an email link, the newsletter box says the list isn't connected, the assistant button isn't shown.

Redeploy once after adding secrets (Deployments → Retry deployment) so the Functions pick them up.

## 5. Check it works

On the preview link:

1. Send yourself an enquiry from the Lightspeed page. It should arrive in your inbox within a minute, with the visitor's address as reply-to, and appear in D1 → `enquiries`.
2. Request the brochure. The PDF opens and the address appears in Mailchimp with the tag *Brochure – Lightspeed*.
3. Add a test owner in D1 → Console: `INSERT INTO owners (model, number, name, email, activation_code) VALUES ('lightspeed','001','Test','you@example.com','TEST-CODE-1');` then register on the owners' page with that code, and try the password-reset link.
4. In Stripe, send a test webhook for `checkout.session.completed`; a row appears in `reservations` and you get an email.

## 6. Content

- Sign in at [app.pagescms.org](https://app.pagescms.org) with GitHub and open this repository: News, Pre-owned, Settings and Assistant appear as forms. Saving commits to `main` and the site rebuilds.
- Photos: drop JPGs into `assets/` (through Pages CMS or GitHub). The build makes the phone and laptop sizes; reference the original name in content files.
- Analytics: put the GA4 ID and Meta pixel ID in `content/site.yml` → `analytics`. Nothing loads until they're set, and nothing loads until the visitor accepts the cookie notice.

## 7. Go live on langenmotorcycles.co.uk

1. Pages project → **Custom domains → Set up a custom domain** → `www.langenmotorcycles.co.uk`, and again for `langenmotorcycles.co.uk`.
2. If the domain's DNS isn't on Cloudflare yet: **Add a site** in Cloudflare, let it import the records, then change the nameservers at the registrar to the two Cloudflare gives you. Takes an hour or so to propagate; the old site keeps working meanwhile.
3. Cloudflare creates the certificates automatically. The old Webflow addresses (`/motorcycles/lightspeed` and so on) forward via `static/_redirects`.
4. Cancel Webflow.

## Adding an owner

D1 → `langen-site` → Console:

```sql
INSERT INTO owners (model, number, name, email, activation_code)
VALUES ('lightspeed', '007', 'Shashi', 'owner@example.com', 'LS7-K4PQ-2M');
```

Give them the activation code with the bike (a printed card) or by email. They set their own password on first use; if they forget it, the portal emails them a reset link, or you clear it with `UPDATE owners SET password_hash = NULL, password_salt = NULL WHERE model='lightspeed' AND number='007';` and they register again.

## Reading enquiries without the inbox

D1 → Console: `SELECT created_at, name, email, country, model, utm, substr(message,1,120) AS message FROM enquiries ORDER BY id DESC LIMIT 50;`

## Opening the home page with film

Export a 10–20 s MP4 (H.264, 1920×1080, no audio, ≤ 6 MB) as `assets/home_hero.mp4`, then in `src/pages.py` swap the home hero `<img class="bg" …>` for the `<video>` tag shown in the comment beside it. The poster frame covers devices that block autoplay.
