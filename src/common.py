import json as _json
from content import load_site
SITE = load_site()
STRIPE = SITE["lightspeed"]["stripe_deposit_link"]
MAIL = SITE["company"]["email"]
TEL = SITE["company"]["phone"]
TELFMT = SITE["company"]["phone_display"]
BROCHURE = SITE["lightspeed"]["brochure"]
FEAT = SITE.get("features", {})
TURNSTILE = (SITE.get("forms", {}) or {}).get("turnstile_site_key", "") or ""
REPLY_TIME = (SITE.get("forms", {}) or {}).get("reply_time", "within a working day")

def mailto(subject, body=None):
    import urllib.parse as u
    s = "mailto:" + MAIL + "?subject=" + u.quote(subject)
    if body:
        s += "&body=" + u.quote(body)
    return s

ENQ_LS = mailto("Lightspeed enquiry", "Hi Langen,\n\nI'd like to find out more about commissioning a Lightspeed.\n\nName:\nCountry:\nAnything in mind (colour, timing, questions):\n")
ENQ_TS = mailto("Two Stroke – Certified Pre-Owned enquiry", "Hi Langen,\n\nI'd like to register my interest in a Certified Pre-Owned Two Stroke.\n\nName:\nCountry:\nAnything in mind:\n")
ENQ_GEN = mailto("Enquiry", "Hi Langen,\n\nName:\nCountry:\nHow can we help:\n")

# ---------------------------------------------------------------------------
# Visual system v3 — black / carbon / aluminium / paper, bronze as a metal
# ---------------------------------------------------------------------------
CSS = r"""
:root{
  --ink:#0e0e10;          /* page black */
  --ink2:#151517;         /* raised black */
  --carbon:#131315;       /* carbon ground (texture applied via .carbon) */
  --paper:#f3f2ef;        /* off-white, neutral not cream */
  --paper2:#e9e7e2;
  --alu:#c7c7c3;          /* aluminium light */
  --alu2:#8a8a86;         /* aluminium dark */
  --bronze:#a8865a;       /* flat fallback only */
  --bronze-hi:#e6c994;
  --bronze-lo:#6b5133;
  --bronze-grad:linear-gradient(135deg,#6b5133 0%,#a8865a 22%,#e6c994 46%,#c9a46f 58%,#8c6b44 82%,#6b5133 100%);
  --alu-grad:linear-gradient(135deg,#7e7e7b 0%,#c9c9c6 30%,#f2f2f0 48%,#c2c2bf 66%,#767673 100%);
  --muted:rgba(255,255,255,.62);
  --line:rgba(255,255,255,.14);
  --line-dark:rgba(0,0,0,.14);
  --sat:env(safe-area-inset-bottom,0px);
  /* legacy aliases so nothing breaks */
  --gold:#a8865a;--gold2:#c9a46f;
}
*{box-sizing:border-box;margin:0;padding:0}
[hidden]{display:none!important}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
body{background:var(--ink);color:#fff;font-family:"Barlow",system-ui,sans-serif;font-weight:400;line-height:1.6;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
img{max-width:100%;display:block}
a{color:inherit}
h1,h2,h3,h4,.cond{font-family:"Barlow Condensed","Barlow",sans-serif;font-weight:600;line-height:.98;text-transform:uppercase;letter-spacing:.025em}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
@media (max-width:640px){.wrap{padding:0 20px}}

/* metal finishes */
.bronze-text,.chapter span,.numbers b,.step::before,.cpo .card .price,.bikehead .num{background:var(--bronze-grad);-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent}
.light .numbers b,.light .step::before{background:linear-gradient(135deg,#5a4530 0%,#9a7a52 30%,#c9a46f 50%,#8c6b44 70%,#5a4530 100%);-webkit-background-clip:text;background-clip:text}
.alu-text{background:var(--alu-grad);-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent}
.rule{height:1px;background:var(--line);border:0}
.rule.bronze{background:linear-gradient(90deg,transparent,#c9a46f 30%,#e6c994 50%,#c9a46f 70%,transparent)}

.kicker{font-family:"Barlow Condensed";font-weight:500;font-size:13px;letter-spacing:.34em;text-transform:uppercase;color:rgba(255,255,255,.66)}
.light .kicker{color:#5f5d58}

/* buttons: square, quiet, one metallic per page */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.6em;font-family:"Barlow Condensed",sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:.18em;font-size:14px;line-height:1;text-decoration:none;padding:15px 26px 14px;border:1px solid rgba(255,255,255,.55);border-radius:0;min-height:48px;transition:background .18s,color .18s,border-color .18s;cursor:pointer;background:transparent;color:#fff}
.btn:hover,.btn:focus-visible{background:#fff;color:var(--ink);border-color:#fff}
.btn.ghost{color:#fff}
.btn.gold{background:var(--bronze-grad);color:#15110c;border:0;padding:16px 28px 15px;box-shadow:inset 0 1px 0 rgba(255,255,255,.45),inset 0 -1px 0 rgba(0,0,0,.35),0 1px 0 rgba(0,0,0,.4);position:relative;overflow:hidden}
.btn.gold::after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,0) 0 2px,rgba(255,255,255,.06) 2px 3px);pointer-events:none}
.btn.gold:hover,.btn.gold:focus-visible{filter:brightness(1.08);color:#15110c}
.light .btn.ghost,.btn.dark{color:var(--ink);background:transparent;border-color:rgba(0,0,0,.6)}
.light .btn.ghost:hover,.btn.dark:hover,.light .btn.ghost:focus-visible{background:var(--ink);color:#fff;border-color:var(--ink)}
.btn:focus-visible{outline:2px solid #fff;outline-offset:3px}
.light .btn:focus-visible{outline-color:var(--ink)}
.btn svg{width:16px;height:16px;flex:none}
.btns{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.tlink{font-family:"Barlow Condensed";font-weight:600;letter-spacing:.18em;text-transform:uppercase;font-size:14px;text-decoration:none;color:#fff;border-bottom:1px solid rgba(255,255,255,.45);padding-bottom:4px;transition:border-color .18s}
.tlink:hover{border-color:#fff}
.light .tlink{color:var(--ink);border-color:rgba(0,0,0,.4)}
.light .tlink:hover{border-color:var(--ink)}

/* top bar: hairline, centred wordmark, transparent over heroes */
.top{position:fixed;top:0;left:0;right:0;z-index:20;background:transparent;transition:background .25s,border-color .25s;border-bottom:1px solid transparent}
.top.scrolled,.top.solid{background:rgba(14,14,16,.92);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom-color:rgba(255,255,255,.08)}
.top .wrap{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;height:72px;gap:18px}
.top .logo{height:26px}
.top .brand{justify-self:center;display:inline-flex}
.nav{display:flex;gap:28px;align-items:center}
.nav.r{justify-self:end}
.nav a{font-family:"Barlow Condensed";font-weight:600;text-transform:uppercase;letter-spacing:.2em;font-size:12.5px;text-decoration:none;color:rgba(255,255,255,.78);padding:6px 0;border-bottom:1px solid transparent;transition:color .18s,border-color .18s}
.nav a:hover,.nav a.on{color:#fff;border-color:rgba(255,255,255,.7)}
.nav a.enq{color:#fff;border-color:rgba(255,255,255,.45)}
.burger{display:none;background:none;border:0;color:#fff;width:44px;height:44px;align-items:center;justify-content:center;cursor:pointer;margin-left:-12px}
.burger svg{width:24px;height:24px}
.top .mob-enq{display:none;justify-self:end;font-family:"Barlow Condensed";font-weight:600;text-transform:uppercase;letter-spacing:.2em;font-size:12.5px;text-decoration:none;color:#fff;border-bottom:1px solid rgba(255,255,255,.45);padding-bottom:3px}
@media (max-width:1040px){.nav{display:none}.burger{display:inline-flex}.top .mob-enq{display:inline-block}}
@media (max-width:640px){.top .wrap{height:64px}.top .logo{height:22px}}
.drawer{display:none;position:fixed;inset:0;z-index:19;background:#0e0e10;padding:92px 24px calc(28px + var(--sat));overflow:auto}
.drawer.open{display:block}
.drawer a{display:block;font-family:"Barlow Condensed";font-weight:600;text-transform:uppercase;letter-spacing:.14em;font-size:28px;text-decoration:none;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.08);color:rgba(255,255,255,.85)}
.drawer a.on{color:#fff}
.drawer .btns{margin-top:28px}
.drawer .btns .btn{flex:1}
.drawer small{display:block;margin-top:28px;color:var(--muted);font-size:14px;line-height:1.7}

/* hero: full viewport, atmospheric, text low-left */
.hero{position:relative;min-height:100vh;min-height:100svh;display:flex;align-items:flex-end;overflow:hidden;background:var(--ink)}
.hero.short{min-height:72vh;min-height:72svh}
.hero.short .veil{background:linear-gradient(180deg,rgba(14,14,16,.5) 0%,rgba(14,14,16,.08) 24%,rgba(14,14,16,.3) 48%,rgba(14,14,16,.84) 78%,var(--ink) 100%)}
.hero img.bg,.hero video.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:62% 40%}
.hero .veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,14,16,.45) 0%,rgba(14,14,16,0) 26%,rgba(14,14,16,0) 55%,rgba(14,14,16,.72) 82%,var(--ink) 100%)}
.hero .wrap{position:relative;padding-bottom:72px;padding-top:140px;width:100%}
.hero .mark{width:min(80%,440px);margin:14px 0 20px}
.hero h1{font-size:clamp(36px,5.2vw,68px);max-width:18ch;font-weight:500;letter-spacing:.03em}
.hero p{max-width:50ch;margin:18px 0 26px;font-size:clamp(16px,1.6vw,18px);color:rgba(255,255,255,.86)}
.hero .price{font-size:14px;color:var(--muted);margin-top:18px;max-width:52ch}
.hero h1+.tlink{margin-top:26px;display:inline-block}
.hero .btns{margin-top:24px}
.hero .price a{color:#fff}
.hero .scroll{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);font-family:"Barlow Condensed";font-weight:500;font-size:11px;letter-spacing:.34em;text-transform:uppercase;color:rgba(255,255,255,.55);display:flex;flex-direction:column;align-items:center;gap:10px}
.hero .scroll::after{content:"";width:1px;height:34px;background:linear-gradient(180deg,rgba(255,255,255,.7),rgba(255,255,255,0));animation:drop 2.4s ease-in-out infinite}
@keyframes drop{0%{transform:scaleY(0);transform-origin:top}50%{transform:scaleY(1);transform-origin:top}51%{transform-origin:bottom}100%{transform:scaleY(0);transform-origin:bottom}}
.hero.open .wrap{padding-bottom:110px}
.hero.open h1{font-size:clamp(34px,4.6vw,60px);max-width:16ch}
@media (max-width:640px){.hero img.bg[data-mobile-pos]{object-position:var(--mpos)!important}}
@media (max-width:640px){.hero.short{min-height:64svh}.hero img.bg,.hero video.bg{object-position:56% 30%}.hero .wrap{padding-bottom:56px;padding-top:110px}.kicker{font-size:12px;letter-spacing:.28em}.hero h1{font-size:34px}.hero p{font-size:16px;margin:14px 0 22px}.hero .price{display:none}.hero .mark{margin:10px 0 14px}.hero.open .wrap{padding-bottom:92px}.hero.open h1{font-size:36px}}

/* sections */
section{padding:96px 0}
@media (max-width:640px){section{padding:72px 0}}
.section-title{font-size:clamp(30px,4.2vw,52px);max-width:20ch;margin-bottom:20px}
.lede{font-size:clamp(17px,1.7vw,20px);max-width:58ch;color:#fff;line-height:1.55}
.body{max-width:60ch;color:var(--muted)}
.body+.body,.lede+.body{margin-top:14px}
.light{background:var(--paper);color:var(--ink)}
.light .body,.light .lede{color:#2b2a28}
.light .body{color:#4a4844}
.light .section-title{color:var(--ink)}
.carbon{background:var(--carbon) url(assets/carbon.png) repeat;background-size:64px 64px}
.carbon::before{content:none}
blockquote{border-left:1px solid rgba(255,255,255,.35);padding:6px 0 6px 24px;margin:34px 0 0;max-width:60ch;font-size:clamp(17px,1.7vw,20px);color:#fff;line-height:1.5}
.light blockquote{color:var(--ink);border-color:rgba(0,0,0,.35)}
blockquote footer{font-family:"Barlow Condensed";font-weight:500;letter-spacing:.2em;text-transform:uppercase;font-size:12.5px;color:var(--muted);margin-top:14px}
.light blockquote footer{color:#6b6965}
.split{display:grid;gap:36px;align-items:center}
@media (min-width:860px){.split{grid-template-columns:1fr 1fr;gap:64px}.split.rev>:first-child{order:2}.split.wide{grid-template-columns:.8fr 1.2fr}}
.split img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover}
.split img.sq{aspect-ratio:1/1}
.split img.tall{aspect-ratio:4/5}

/* manifesto: one sentence on black */
.manifesto{padding:140px 0;text-align:center}
.manifesto h2,.manifesto p.big{font-family:"Barlow Condensed";font-weight:500;font-size:clamp(28px,3.8vw,50px);line-height:1.1;text-transform:uppercase;letter-spacing:.03em;max-width:28ch;margin:0 auto;color:#fff}
.manifesto .kicker{margin-bottom:26px;display:block}
.manifesto .tlink{display:inline-block;margin-top:34px}
.manifesto.light h2,.manifesto.light p.big{color:var(--ink)}
@media (max-width:640px){.manifesto{padding:96px 0}}

/* full-bleed */
.bleed{position:relative;min-height:78vh;display:flex;align-items:flex-end;overflow:hidden;padding:0}
.bleed img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.bleed .veil{position:absolute;inset:0;background:linear-gradient(90deg,rgba(14,14,16,.55) 0%,rgba(14,14,16,.25) 45%,rgba(14,14,16,0) 70%),linear-gradient(180deg,rgba(14,14,16,.1) 0%,rgba(14,14,16,0) 30%,rgba(14,14,16,.86) 100%)}
.bleed .wrap{position:relative;padding-top:140px;padding-bottom:64px;width:100%}
.bleed h2{font-size:clamp(30px,4.6vw,56px);max-width:16ch;font-weight:500}
@media (max-width:640px){.bleed .veil{background:linear-gradient(180deg,rgba(14,14,16,.2) 0%,rgba(14,14,16,.55) 35%,rgba(14,14,16,.93) 100%)}.bleed{min-height:86svh}}
.bleed p{max-width:54ch;margin-top:16px;color:rgba(255,255,255,.88)}

/* model cards (home) */
.models{display:grid;gap:2px;background:var(--ink)}
@media (min-width:760px){.models{grid-template-columns:1fr 1fr}}
.model{position:relative;display:block;min-height:560px;overflow:hidden;text-decoration:none;color:#fff}
.model img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.6,.2,1)}
.model:hover img{transform:scale(1.035)}
.model .veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,14,16,0) 45%,rgba(14,14,16,.88) 100%)}
.model .txt{position:absolute;left:0;right:0;bottom:0;padding:32px 30px}
.model .txt img{position:static;height:auto;width:min(100%,320px);object-fit:contain;object-position:left center;margin-bottom:14px}
.model .txt img.ts{width:min(56%,200px)}
.model h2{font-size:clamp(28px,3.4vw,40px);font-weight:500}
.model p{color:rgba(255,255,255,.8);max-width:40ch;margin:6px 0 16px;font-size:15px}
.model .cta{font-family:"Barlow Condensed";font-weight:600;letter-spacing:.2em;text-transform:uppercase;font-size:12.5px;color:#fff;border-bottom:1px solid rgba(255,255,255,.45);padding-bottom:3px}
@media (max-width:640px){.model{min-height:72svh}}

/* numbers band (model pages) */
.numbers-band{border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:38px 0;background:var(--ink)}
.numbers-band .wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:24px}
.numbers-band .price{font-size:14px;color:var(--muted);max-width:48ch}
.numbers-band .price a{color:#fff}
.numbers{display:flex;gap:44px;flex-wrap:wrap}
.numbers div{font-family:"Barlow Condensed";font-weight:500;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}
.numbers b{display:block;font-size:46px;font-weight:600;line-height:1;letter-spacing:0;margin-bottom:6px}
@media (max-width:640px){.numbers{gap:22px 28px}.numbers b{font-size:36px}.numbers-band{padding:30px 0}}

/* callouts */
.callouts{display:grid;gap:30px 40px;margin-top:48px}
@media (min-width:700px){.callouts{grid-template-columns:1fr 1fr}}
@media (min-width:1000px){.callouts{grid-template-columns:1fr 1fr 1fr}}
.callout{display:flex;gap:18px;align-items:flex-start}
.callout img{width:88px;height:88px;object-fit:cover;flex:none;filter:saturate(.85)}
.callout h3{font-size:20px;margin-bottom:6px}
.callout p{font-size:15px;color:var(--muted)}
.light .callout p{color:#4a4844}

/* photo pair / grid */
.pair{display:grid;gap:2px;background:var(--ink)}
@media (min-width:700px){.pair{grid-template-columns:1fr 1fr}}
.pair figure{position:relative}
.pair img{width:100%;aspect-ratio:1/1;object-fit:cover}
.pair figcaption{position:absolute;left:0;right:0;bottom:0;padding:80px 26px 26px;background:linear-gradient(180deg,rgba(14,14,16,0),rgba(14,14,16,.85));color:#fff}
.pair figcaption h3{font-size:24px;font-weight:500}
.pair figcaption p{font-size:15px;color:rgba(255,255,255,.8);max-width:44ch}
.studies{display:grid;gap:14px;margin-top:36px}
@media (min-width:700px){.studies{grid-template-columns:1fr 1fr}}
@media (min-width:1000px){.studies{grid-template-columns:1fr 1fr 1fr}}
.studies figure{background:#2a2a2c}
.studies img{width:100%;aspect-ratio:16/9;object-fit:cover}
.studies figcaption{font-family:"Barlow Condensed";font-weight:500;letter-spacing:.18em;text-transform:uppercase;font-size:12px;padding:12px 0 0;color:var(--muted)}
.studies figcaption span{color:#fff;margin-right:12px}
.light .studies figcaption{color:#6b6965}.light .studies figcaption span{color:var(--ink)}
.note{font-size:13px;color:var(--muted);margin-top:14px}
.light .note{color:#6b6965}

/* steps */
.steps{counter-reset:s;display:grid;gap:34px 40px;margin-top:48px}
@media (min-width:700px){.steps{grid-template-columns:1fr 1fr}}
@media (min-width:1000px){.steps.three{grid-template-columns:1fr 1fr 1fr}}
.step{position:relative;padding-top:18px;border-top:1px solid var(--line)}
.light .step{border-color:var(--line-dark)}
.step::before{counter-increment:s;content:"0" counter(s);display:block;font-family:"Barlow Condensed";font-weight:600;font-size:30px;line-height:1;margin-bottom:12px}
.step h3{font-size:22px;margin-bottom:6px}
.step p{font-size:15px;color:var(--muted)}
.light .step p{color:#4a4844}

/* list blocks */
.own{display:grid;gap:26px 40px;margin-top:40px}
@media (min-width:700px){.own{grid-template-columns:1fr 1fr}}
@media (min-width:1000px){.own.three{grid-template-columns:1fr 1fr 1fr}}
.own div{border-top:1px solid var(--line);padding-top:16px}
.light .own div{border-color:var(--line-dark)}
.own h3{font-size:20px;margin-bottom:6px}
.own p{font-size:15px;color:var(--muted)}
.light .own p{color:#4a4844}

/* specs */
.specs{display:grid;gap:0 48px;margin-top:40px}
@media (min-width:700px){.specs{grid-template-columns:1fr 1fr}}
.specs dl{display:grid;grid-template-columns:150px 1fr;gap:12px 16px;font-size:15px}
.specs dt{font-family:"Barlow Condensed";font-weight:600;text-transform:uppercase;letter-spacing:.16em;color:var(--muted);font-size:12.5px;padding-top:3px}
.specs dd{color:#fff;padding-bottom:12px;border-bottom:1px solid rgba(255,255,255,.1)}
.kpis{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin-top:34px}
@media (min-width:700px){.kpis{grid-template-columns:repeat(4,1fr)}}
.kpis div{border-top:1px solid var(--line);padding-top:14px}
.kpis b{display:block;font-family:"Barlow Condensed";font-weight:500;font-size:40px;line-height:1;color:#fff}
.kpis span{font-family:"Barlow Condensed";font-weight:500;letter-spacing:.2em;text-transform:uppercase;font-size:12px;color:var(--muted)}
.light .kpis b{color:var(--ink)}

/* band */
.band{background:var(--paper);color:var(--ink);padding:40px 0;border-top:1px solid var(--line-dark)}
.band .wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:18px}
.band h2{font-size:clamp(24px,3vw,34px);font-weight:500}
.band .btn{border-color:rgba(0,0,0,.6);color:var(--ink);background:transparent}
.band .btn:hover,.band .btn:focus-visible{background:var(--ink);color:#fff}

/* press quotes */
.quotes{display:grid;gap:26px 40px;margin-top:40px}
@media (min-width:860px){.quotes{grid-template-columns:1fr 1fr}}
.quotes blockquote{margin:0;font-size:17px}
.quotes blockquote a{color:#fff;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.4)}
.light .quotes blockquote a{color:var(--ink);border-color:rgba(0,0,0,.4)}

/* news */
.news{display:grid;gap:2px;margin-top:40px;background:var(--line)}
@media (min-width:700px){.news{grid-template-columns:1fr 1fr}}
@media (min-width:1000px){.news{grid-template-columns:1fr 1fr 1fr}}
.card{background:var(--ink);display:flex;flex-direction:column;text-decoration:none;color:#fff}
.card img{width:100%;aspect-ratio:16/10;object-fit:cover;transition:opacity .25s}
.card:hover img{opacity:.85}
.card .txt{padding:22px 22px 26px}
.card .meta{font-family:"Barlow Condensed";font-weight:500;letter-spacing:.22em;text-transform:uppercase;font-size:11.5px;color:var(--muted)}
.card h3{font-size:22px;margin:10px 0 8px;font-weight:500}
.card p{font-size:15px;color:var(--muted)}
.light .news{background:var(--line-dark)}
.light .card{background:var(--paper);color:var(--ink)}
.light .card p{color:#4a4844}
.light .card .meta{color:#6b6965}
.card.feature{grid-column:1/-1}
@media (min-width:860px){.card.feature{display:grid;grid-template-columns:1.3fr 1fr}.card.feature img{height:100%;aspect-ratio:auto}.card.feature .txt{padding:36px}.card.feature h3{font-size:34px}}
.article{max-width:70ch}
.article p{margin-bottom:18px;color:var(--muted);font-size:17px}
.article h2{font-size:28px;margin:32px 0 12px}
.article blockquote{font-size:17px}

/* FAQ */
.faq{max-width:70ch;margin-top:34px}
.faq details{border-top:1px solid rgba(255,255,255,.14);padding:18px 0}
.light .faq details{border-color:var(--line-dark)}
.faq summary{cursor:pointer;font-family:"Barlow Condensed";font-weight:500;text-transform:uppercase;letter-spacing:.06em;font-size:20px;list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--muted);font-weight:300;font-size:24px;line-height:1}
.faq details[open] summary::after{content:"–"}
.faq p{margin-top:12px;color:var(--muted);font-size:15px;max-width:62ch}
.light .faq p{color:#4a4844}

/* CPO cards */
.cpo{display:grid;gap:2px;margin-top:40px;background:var(--line)}
@media (min-width:760px){.cpo{grid-template-columns:1fr 1fr}}
.cpo .card .price{font-family:"Barlow Condensed";font-weight:600;font-size:28px;margin-top:6px}
.cpo ul{list-style:none;margin:14px 0 18px;color:var(--muted);font-size:14px;display:grid;gap:5px}
.cpo ul li::before{content:"—";color:rgba(255,255,255,.4);margin-right:8px}
.cpo .cta{font-family:"Barlow Condensed";font-weight:600;letter-spacing:.2em;text-transform:uppercase;font-size:12.5px;color:#fff;border-bottom:1px solid rgba(255,255,255,.45);padding-bottom:3px;align-self:flex-start}

/* careers */
.roles{display:grid;gap:2px;margin-top:34px;background:var(--line)}
.role{background:var(--ink);padding:26px;display:grid;gap:8px}
@media (min-width:760px){.role{grid-template-columns:1fr auto;align-items:center;gap:24px}}
.role h3{font-size:24px}
.role .meta{font-family:"Barlow Condensed";font-weight:500;letter-spacing:.2em;text-transform:uppercase;font-size:11.5px;color:var(--muted);margin:4px 0 8px}
.role p{font-size:15px;color:var(--muted);max-width:70ch}

/* enquire block */
#enquire{background:var(--carbon) url(assets/carbon.png) repeat;background-size:64px 64px;padding:110px 0 120px;border-top:1px solid var(--line)}
#enquire .grid{display:grid;gap:40px}
@media (min-width:860px){#enquire .grid{grid-template-columns:1.2fr 1fr;gap:80px}}
#enquire h2{font-size:clamp(34px,5vw,60px);font-weight:500}
#enquire .lede{margin:18px 0 34px}
#enquire .contact{font-size:17px;line-height:1.7}
#enquire .contact a{text-decoration:none;font-family:"Barlow Condensed";font-weight:500;font-size:26px;letter-spacing:.04em;color:#fff;display:block;line-height:1.3}
#enquire .contact a:hover{color:var(--alu)}
#enquire .contact small{display:block;color:var(--muted);font-size:14px;margin-top:22px;line-height:1.55}
#enquire .btns .btn{font-size:15px;padding:19px 30px 18px;min-height:56px}
#enquire .pdf{margin-top:26px;font-size:14px;color:var(--muted)}
#enquire .pdf a{color:#fff}

/* enquiry panel */
.modal{position:fixed;inset:0;z-index:50;display:none;align-items:flex-end;justify-content:center;background:rgba(0,0,0,.72);padding:0}
.modal.open{display:flex}
@media (min-width:640px){.modal{align-items:center;padding:20px}}
.sheet{background:var(--ink2);color:#fff;width:100%;max-width:520px;border:1px solid rgba(255,255,255,.14);padding:28px 22px calc(28px + var(--sat))}
@media (min-width:640px){.sheet{padding:36px}}
.sheet h3{font-size:30px;margin-bottom:6px;font-weight:500}
.sheet p{color:var(--muted);font-size:15px;margin-bottom:20px}
.sheet .addr{display:flex;align-items:center;justify-content:space-between;gap:12px;background:var(--ink);border:1px solid rgba(255,255,255,.12);padding:12px 14px;margin-bottom:12px}
.sheet .addr span{font-family:"Barlow Condensed";font-weight:500;font-size:20px;letter-spacing:.02em;word-break:break-all}
.sheet .addr button{font-family:"Barlow Condensed";font-weight:600;text-transform:uppercase;letter-spacing:.16em;font-size:12.5px;color:#fff;background:none;border:1px solid rgba(255,255,255,.5);padding:8px 12px;cursor:pointer;flex:none}
.sheet .addr button:hover{background:#fff;color:var(--ink)}
.sheet .list{display:grid;gap:10px;margin-top:6px}
.sheet .list .btn{width:100%;font-size:14px}
.sheet.terms{max-width:640px;max-height:90vh;overflow:auto}
.sheet.terms h3{font-size:24px;margin-bottom:14px}
.sheet.terms ol{padding-left:20px;font-size:14px;color:var(--muted);display:grid;gap:10px}
.sheet.terms ol b{color:#fff}
.sheet.terms p{font-size:12px;margin-top:16px}
.sheet .close{margin-top:16px;width:100%;background:none;border:0;color:var(--muted);font:inherit;font-size:14px;cursor:pointer;padding:8px;text-decoration:underline}

.cookie{position:fixed;left:12px;right:12px;bottom:calc(84px + var(--sat));z-index:40;background:var(--ink2);border:1px solid rgba(255,255,255,.14);padding:14px 16px;display:none;gap:12px;align-items:center;flex-wrap:wrap;font-size:14px;color:var(--muted);box-shadow:0 8px 30px rgba(0,0,0,.4)}
@media (min-width:860px){.cookie{left:auto;right:20px;bottom:20px;max-width:440px}}
.cookie.show{display:flex}
.cookie p{flex:1 1 220px;margin:0}
.cookie button{font-family:"Barlow Condensed";font-weight:600;text-transform:uppercase;letter-spacing:.16em;font-size:12.5px;padding:9px 14px;cursor:pointer;border:1px solid rgba(255,255,255,.5);background:none;color:#fff}
.cookie button.yes{background:#fff;color:var(--ink);border-color:#fff}

/* mobile sticky bar */
.bar{position:fixed;left:0;right:0;bottom:0;z-index:30;display:flex;gap:8px;padding:10px 12px calc(10px + var(--sat));background:rgba(14,14,16,.94);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-top:1px solid rgba(255,255,255,.1)}
.bar .btn{flex:1;font-size:13px;padding:12px 10px;min-height:46px}
@media (min-width:860px){.bar{display:none}}
body{padding-bottom:78px}
@media (min-width:860px){body{padding-bottom:0}}

/* footer */
.site-footer{padding:64px 0 90px;font-size:14px;color:var(--muted);border-top:1px solid rgba(255,255,255,.08);background:var(--ink)}
.site-footer .cols{display:grid;gap:30px}
@media (min-width:760px){.site-footer .cols{grid-template-columns:1.4fr 1fr 1fr 1fr}}
.site-footer h4{font-size:12.5px;letter-spacing:.24em;color:#fff;margin-bottom:14px;font-weight:600}
.site-footer a{text-decoration:none;display:block;padding:3px 0;color:var(--muted)}
.site-footer a:hover{color:#fff}
.site-footer .logo{height:26px;margin-bottom:16px}
.site-footer .legal{margin-top:44px;padding-top:18px;border-top:1px solid rgba(255,255,255,.08);display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px;font-size:12px}
.site-footer .social{display:flex;gap:14px;margin-top:14px}
.site-footer .social a{display:inline-flex;padding:0}
.site-footer .social svg{width:18px;height:18px;fill:currentColor}
.page-head{padding:150px 0 48px}
.page-head h1{font-size:clamp(36px,5.6vw,66px);max-width:18ch;font-weight:500}
.page-head .lede{margin-top:18px}
@media (max-width:640px){.page-head{padding:120px 0 36px}}

/* chapter markers, founder's letter, pull quote */
.chapter{font-family:"Barlow Condensed";font-weight:500;font-size:12.5px;letter-spacing:.3em;text-transform:uppercase;color:var(--muted);margin-bottom:18px;display:flex;align-items:center;gap:14px}
.chapter span{font-weight:600;font-size:14px;letter-spacing:.1em}
.chapter span:not(:empty)::after{content:"";display:inline-block;width:36px;height:1px;background:rgba(255,255,255,.3);margin-left:14px;vertical-align:middle;-webkit-text-fill-color:initial}
.chapter span:empty{display:none}
.light .chapter{color:#6b6965}
.light .chapter span:not(:empty)::after{background:rgba(0,0,0,.3)}
.letter-wrap{padding:110px 0}
.letter{max-width:680px}
.letter p{font-size:clamp(18px,1.9vw,21px);line-height:1.6;margin-bottom:22px;color:#1c1c1d}
.letter-wrap:not(.light) .letter p{color:#fff}
.letter p:first-of-type::first-letter{font-family:"Barlow Condensed";font-weight:600;font-size:3.4em;line-height:.8;float:left;padding:6px 12px 0 0}
.letter footer{font-family:"Barlow Condensed";font-weight:500;font-size:26px;letter-spacing:.02em;margin-top:30px;text-transform:none}
.letter footer small{display:block;font-weight:500;font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:var(--muted);margin-top:6px}
.light .letter footer small{color:#6b6965}
.pull blockquote.big{border:0;padding:0;margin:0 auto;max-width:30ch;text-align:center;font-family:"Barlow Condensed";font-weight:500;font-size:clamp(28px,3.8vw,48px);line-height:1.08;text-transform:uppercase;letter-spacing:.03em}
.pull blockquote.big footer{margin-top:26px;text-transform:none;letter-spacing:.04em;font-size:15px}
.section-title{max-width:20ch}

/* ===== v3.1: motion, sub-navigation, annotated features, gallery strip ===== */
.hero img.bg{transform:scale(1.06);animation:kb 16s cubic-bezier(.2,.5,.3,1) forwards}
.hero.film video.bg{opacity:0;transition:opacity 1.2s ease}
.hero.film video.bg.on{opacity:1}
.hero.film img.bg{animation:none;transform:none}
@keyframes kb{to{transform:scale(1)}}
.rv{opacity:0;transform:translateY(22px);transition:opacity 1s ease,transform 1.1s cubic-bezier(.2,.6,.2,1)}
.rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.hero img.bg{transform:none;animation:none}.rv{opacity:1;transform:none;transition:none}}
.skip{position:absolute;left:-999px;top:8px;z-index:100;background:#fff;color:var(--ink);padding:10px 14px;font-family:"Barlow Condensed";font-weight:600;letter-spacing:.14em;text-transform:uppercase;font-size:13px;text-decoration:none}
.skip:focus{left:8px}

/* sticky chapter index under model-page heroes */
.subnav{position:sticky;top:72px;z-index:15;background:rgba(14,14,16,.9);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.subnav .wrap{display:flex;align-items:center;gap:28px;height:52px;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.subnav .wrap::-webkit-scrollbar{display:none}
.subnav .name{font-family:"Barlow Condensed";font-weight:600;letter-spacing:.2em;text-transform:uppercase;font-size:12.5px;color:#fff;flex:none;padding-right:24px;border-right:1px solid var(--line)}
.subnav a{font-family:"Barlow Condensed";font-weight:500;letter-spacing:.2em;text-transform:uppercase;font-size:12px;color:var(--muted);text-decoration:none;white-space:nowrap;padding:18px 0 16px;border-bottom:1px solid transparent;transition:color .18s,border-color .18s}
.subnav a:hover,.subnav a.on{color:#fff;border-color:#fff}
@media (max-width:640px){.subnav{top:64px}.subnav .wrap{gap:22px;height:48px}.subnav .name{display:none}.anno .list summary small{display:none}.anno .list summary{font-size:20px}}
.subnav+.numbers-band{border-top:0}

/* annotated feature: sticky figure + accordion */
.anno{display:grid;gap:34px;margin-top:48px}
@media (min-width:900px){.anno{grid-template-columns:1.1fr 1fr;gap:64px;align-items:start}.anno figure{position:sticky;top:140px}}
.anno figure{margin:0;background:var(--ink2);aspect-ratio:4/3;overflow:hidden}
.anno figure img{width:100%;height:100%;object-fit:cover;transition:opacity .45s ease}
.anno figure img.fade{opacity:0}
.anno .list details{border-top:1px solid var(--line);padding:0}
.anno .list details:last-child{border-bottom:1px solid var(--line)}
.light .anno .list details{border-color:var(--line-dark)}
.anno .list summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:20px 0;font-family:"Barlow Condensed";font-weight:500;text-transform:uppercase;letter-spacing:.08em;font-size:22px}
.anno .list summary::-webkit-details-marker{display:none}
.anno .list summary::after{content:"+";color:var(--muted);font-weight:300;font-size:26px;line-height:1;flex:none}
.anno .list details[open] summary::after{content:"–"}
.anno .list details[open] summary{color:#fff}
.anno .list p{padding:0 0 22px;color:var(--muted);font-size:15.5px;max-width:48ch;line-height:1.6}
.light .anno .list p{color:#4a4844}
.anno .list summary small{font-family:"Barlow Condensed";font-weight:500;letter-spacing:.2em;font-size:11.5px;color:var(--muted);margin-right:auto;margin-left:14px}

/* gallery strip: scroll-snap, swipe on touch, arrows on desktop */
.strip-wrap{position:relative;padding:0}
.strip{display:flex;gap:2px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;-webkit-overflow-scrolling:touch;background:var(--ink)}
.strip::-webkit-scrollbar{display:none}
.strip figure{flex:0 0 78vw;scroll-snap-align:start;position:relative;margin:0}
@media (min-width:700px){.strip figure{flex-basis:44vw}}
@media (min-width:1100px){.strip figure{flex-basis:33.4vw}}
.strip img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}
.strip figcaption{position:absolute;left:0;right:0;bottom:0;padding:70px 22px 22px;background:linear-gradient(180deg,rgba(14,14,16,0),rgba(14,14,16,.8));color:#fff}
.strip figcaption h3{font-size:20px;font-weight:500}
.strip figcaption p{font-size:14px;color:rgba(255,255,255,.78);max-width:40ch;margin-top:4px}
.strip-nav{position:absolute;right:24px;top:-64px;display:none;gap:8px}
@media (min-width:900px){.strip-nav{display:flex}}
.strip-nav button{width:44px;height:44px;border:1px solid rgba(255,255,255,.45);background:transparent;color:#fff;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;transition:background .18s,color .18s}
.strip-nav button:hover{background:#fff;color:var(--ink)}
.strip-nav svg{width:18px;height:18px}
.strip-head{padding:96px 0 32px}
.strip-head .wrap{position:relative}
.strip-head .section-title{margin-bottom:0}

/* ===== forms (enquiry panel + contact page), newsletter, brochure, assistant ===== */
.enq-form{display:grid;gap:12px;margin-top:4px}
.enq-form label{display:grid;gap:6px;font-family:"Barlow Condensed";font-weight:500;letter-spacing:.2em;text-transform:uppercase;font-size:12px;color:var(--muted)}
.enq-form input,.enq-form select,.enq-form textarea{font:inherit;font-size:16px;color:#fff;background:var(--ink);border:1px solid rgba(255,255,255,.18);padding:12px 14px;width:100%;border-radius:0;-webkit-appearance:none;appearance:none}
.enq-form select{background-image:linear-gradient(45deg,transparent 50%,rgba(255,255,255,.6) 50%),linear-gradient(135deg,rgba(255,255,255,.6) 50%,transparent 50%);background-position:calc(100% - 20px) 50%,calc(100% - 14px) 50%;background-size:6px 6px;background-repeat:no-repeat;padding-right:40px}
.enq-form textarea{min-height:110px;resize:vertical}
.enq-form input:focus,.enq-form select:focus,.enq-form textarea:focus{outline:none;border-color:#fff}
.enq-form .row2{display:grid;gap:12px}
@media (min-width:560px){.enq-form .row2{grid-template-columns:1fr 1fr}}
.enq-form .chk{display:flex;align-items:center;gap:10px;text-transform:none;letter-spacing:0;font-family:"Barlow";font-size:14px;color:var(--muted);cursor:pointer}
.enq-form .chk input{width:18px;height:18px;padding:0;accent-color:#fff;-webkit-appearance:auto;appearance:auto}
.enq-form .hp{position:absolute;left:-9999px;top:-9999px;height:0;overflow:hidden}
.enq-form .err{color:#f3b2a6;font-size:14px;min-height:1.2em}
.enq-form .err a{color:#fff}
.enq-form button[type=submit]{width:100%}
.enq-form button[disabled]{opacity:.6;cursor:wait}
.light .enq-form input,.light .enq-form select,.light .enq-form textarea{background:#fff;color:var(--ink);border-color:rgba(0,0,0,.25)}
.light .enq-form input:focus,.light .enq-form select:focus,.light .enq-form textarea:focus{border-color:var(--ink)}
.light .enq-form label{color:#5f5d58}.light .enq-form .chk{color:#4a4844}.light .enq-form .chk input{accent-color:var(--ink)}
.light .enq-form .err{color:#9b2c1f}.light .enq-form .err a{color:var(--ink)}
.done{padding:10px 0 6px}
.done h3{font-size:28px;font-weight:500;margin-bottom:8px}
.done p{color:var(--muted);font-size:15px}
.sheet .intro{color:var(--muted);font-size:15px;margin:0 0 18px}
.sheet details.alt{margin-top:18px;border-top:1px solid rgba(255,255,255,.12);padding-top:12px}
.sheet details.alt summary{cursor:pointer;list-style:none;font-family:"Barlow Condensed";font-weight:500;letter-spacing:.18em;text-transform:uppercase;font-size:12.5px;color:var(--muted);display:flex;justify-content:space-between}
.sheet details.alt summary::-webkit-details-marker{display:none}
.sheet details.alt summary::after{content:"+"}
.sheet details.alt[open] summary::after{content:"–"}
.sheet details.alt .addr{margin-top:14px}
.sheet{max-height:92vh;overflow:auto}
@media (min-width:640px){.sheet{max-width:560px}}
.sheet.wide{max-width:640px}
.contact-form{max-width:640px;margin-top:34px}
.contact-form .btn{width:auto}
.cf-turnstile{margin:4px 0}
/* newsletter (footer) */
.nl{border-top:1px solid rgba(255,255,255,.08);padding:40px 0 10px;margin-bottom:34px}
.nl .wrap{display:grid;gap:18px}
@media (min-width:860px){.nl .wrap{grid-template-columns:1fr 1fr;align-items:center;gap:60px}}
.nl h4{font-size:22px;letter-spacing:.04em;text-transform:none;margin-bottom:6px;font-weight:500;color:#fff}
.nl p{color:var(--muted);font-size:14px;max-width:46ch}
.nl form{display:flex;gap:0;max-width:460px}
.nl input{flex:1;font:inherit;font-size:15px;color:#fff;background:var(--ink2);border:1px solid rgba(255,255,255,.18);border-right:0;padding:12px 14px;min-width:0;border-radius:0}
.nl input:focus{outline:none;border-color:#fff}
.nl button{font-family:"Barlow Condensed";font-weight:600;letter-spacing:.16em;text-transform:uppercase;font-size:12.5px;padding:0 18px;border:1px solid rgba(255,255,255,.5);background:transparent;color:#fff;cursor:pointer;white-space:nowrap}
.nl button:hover{background:#fff;color:var(--ink)}
.nl .msg{font-size:13px;color:var(--muted);margin-top:8px;min-height:1.2em}
/* assistant */
.ask{position:fixed;right:18px;bottom:calc(18px + var(--sat));z-index:35;display:inline-flex;align-items:center;gap:10px;background:var(--ink2);color:#fff;border:1px solid rgba(255,255,255,.3);padding:12px 16px;font-family:"Barlow Condensed";font-weight:600;letter-spacing:.16em;text-transform:uppercase;font-size:12.5px;cursor:pointer;box-shadow:0 8px 30px rgba(0,0,0,.4)}
.ask:hover{background:#fff;color:var(--ink)}
.ask svg{width:16px;height:16px}
@media (max-width:859px){.ask{bottom:calc(88px + var(--sat))}}
.chat{display:flex;flex-direction:column;gap:12px;max-height:50vh;overflow:auto;padding:4px 0 10px;margin-bottom:12px}
.chat .m{max-width:88%;padding:12px 14px;font-size:15px;line-height:1.5;border:1px solid rgba(255,255,255,.12)}
.chat .m.u{align-self:flex-end;background:#fff;color:var(--ink);border-color:#fff}
.chat .m.a{align-self:flex-start;background:var(--ink);color:#fff}
.chat .m.a.wait{color:var(--muted)}
.chatform{display:flex;gap:0}
.chatform input{flex:1;font:inherit;font-size:16px;color:#fff;background:var(--ink);border:1px solid rgba(255,255,255,.18);border-right:0;padding:12px 14px;min-width:0;border-radius:0}
.chatform input:focus{outline:none;border-color:#fff}
.chatform button{font-family:"Barlow Condensed";font-weight:600;letter-spacing:.16em;text-transform:uppercase;font-size:12.5px;padding:0 18px;border:1px solid rgba(255,255,255,.5);background:transparent;color:#fff;cursor:pointer}
.chatform button:hover{background:#fff;color:var(--ink)}
.sheet .fine{font-size:12px;color:var(--muted);margin-top:12px}
""" + __import__("portal").PORTAL_CSS

NAV = [("lightspeed.html","Lightspeed"),("two-stroke.html","Two Stroke"),("pre-owned.html","Pre-Owned"),("commission.html","Commission"),("about.html","About"),("news.html","News"),("contact.html","Contact")]
NAV_L = NAV[:4]
NAV_R = NAV[4:]

ICON_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="5" width="18" height="14"/><path d="m3 7 9 6 9-6"/></svg>'

def head(title, desc, canonical, og="assets/ls_og.jpg"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://www.langenmotorcycles.co.uk/{og}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.langenmotorcycles.co.uk/{canonical}">
<link rel="canonical" href="https://www.langenmotorcycles.co.uk/{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0e0e10">
<link rel="icon" href="assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600;700&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
<!-- Analytics: set the IDs in site.js (GA4 measurement ID for www.langenmotorcycles.co.uk and the Meta pixel). Nothing loads until they are set. -->
<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('consent','default',{{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'}});
try{{if(localStorage.getItem('ln_consent')==='granted'){{gtag('consent','update',{{analytics_storage:'granted'}});}}}}catch(e){{}}
</script>
<link rel="stylesheet" href="site.css">
{'<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>' if TURNSTILE else ''}
</head>
<body>
"""

def nav(current, solid=False):
    def links(items):
        return "".join(f'<a href="{h}"{" class=\"on\"" if h==current else ""}>{t}</a>' for h,t in items)
    all_links = links(NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="top{' solid' if solid else ''}" id="top">
  <div class="wrap">
    <nav class="nav l" aria-label="Motorcycles">{links(NAV_L)}</nav>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 7h18M3 12h18M3 17h18"/></svg></button>
    <a class="brand" href="index.html" aria-label="Langen Motorcycles"><img class="logo" src="assets/langen_logo_white.svg" alt="Langen"></a>
    <nav class="nav r" aria-label="Langen">{links(NAV_R)}<a class="enq" href="{ENQ_LS}">Enquire</a></nav>
    <a class="mob-enq" href="{ENQ_LS}">Enquire</a>
  </div>
</header>
<div class="drawer" id="drawer">
  {all_links}
  <a href="owners.html">Owners' portal</a>
  <a href="https://langenmotorcycles.shop.dowlis.com/">Merch</a>
  <a href="careers.html">Careers</a>
  <div class="btns"><a class="btn ghost" href="{STRIPE}">Reserve</a><a class="btn gold" href="{ENQ_LS}">Enquire</a></div>
  <small>Langen Motorcycles · Kingfisher Court, Wigan WN4 9DW<br><a href="tel:{TEL}" style="display:inline;padding:0">{TELFMT}</a> · <a href="mailto:{MAIL}" style="display:inline;padding:0">{MAIL}</a></small>
</div>
"""

def enquiry_form(form_id="enq-form", subject="Enquiry", model="lightspeed", light=False):
    """The one enquiry form, used in the panel and on the contact page. Posts to /api/enquire."""
    ts = f'<div class="cf-turnstile" data-sitekey="{TURNSTILE}" data-theme="{"light" if light else "dark"}" data-size="flexible"></div>' if TURNSTILE else ""
    sel = lambda v: ' selected' if v == model else ''
    return f"""<form class="enq-form" id="{form_id}" novalidate>
  <input type="hidden" name="subject" value="{subject}">
  <input type="hidden" name="page" value="">
  <div class="row2"><label>Name<input name="name" required autocomplete="name"></label><label>Email<input name="email" type="email" required autocomplete="email" inputmode="email"></label></div>
  <div class="row2"><label>Country<input name="country" autocomplete="country-name"></label><label>Phone (optional)<input name="phone" type="tel" autocomplete="tel" inputmode="tel"></label></div>
  <label>About<select name="model"><option value="lightspeed"{sel("lightspeed")}>The Lightspeed</option><option value="two-stroke"{sel("two-stroke")}>A pre-owned Two Stroke</option><option value="visit"{sel("visit")}>Visiting the workshop</option><option value="other"{sel("other")}>Something else</option></select></label>
  <label>Message<textarea name="message" rows="4" placeholder="A colour, a question, a road you want it for…"></textarea></label>
  <label class="chk"><input type="checkbox" name="newsletter" value="1"> Keep me informed about Langen news</label>
  <div class="hp" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
  {ts}
  <div class="err" aria-live="polite"></div>
  <button class="btn gold" type="submit">Send enquiry</button>
</form>
<div class="done" hidden><h3>Thank you.</h3><p>Your enquiry is with Christofer and the team. We reply personally, usually {REPLY_TIME}.</p></div>"""

def enquire_block(title="Talk to us about a build", lede=None, primary=None, primary_label="Enquire by email", secondary=True, pdf=True):
    lede = lede or "Tell us where you are and what you have in mind, and Christofer or one of the team will come back to you personally. Every Langen is commissioned in conversation, not bought from a page."
    primary = primary or ENQ_LS
    sec = f'<a class="btn ghost" href="{STRIPE}">Reserve a Lightspeed – £1,000 refundable deposit</a>' if secondary else ""
    if pdf and FEAT.get("brochure_gate"):
        pdfl = f'<p class="pdf">Prefer a document? <a href="{BROCHURE}" class="bro-link">Request the Lightspeed brochure (PDF)</a></p>'
    elif pdf:
        pdfl = f'<p class="pdf">Prefer a document? <a href="{BROCHURE}" download>Download the Lightspeed brochure (PDF, 5 MB)</a></p>'
    else:
        pdfl = ""
    return f"""<section id="enquire">
  <div class="wrap grid">
    <div>
      <h2>{title}</h2>
      <p class="lede">{lede}</p>
      <div class="btns">
        <a class="btn gold" href="{primary}">{ICON_MAIL}{primary_label}</a>
        {sec}
      </div>
      {pdfl}
    </div>
    <div class="contact">
      <a href="mailto:{MAIL}">{MAIL}</a>
      <a href="tel:{TEL}">{TELFMT}</a>
      <small>Langen Motorcycles<br>Unit 1, Kingfisher Court, South Lancs Industrial Estate<br>Wigan, Greater Manchester WN4 9DW<br>United Kingdom<br><br>Visits to the workshop are by appointment.</small>
    </div>
  </div>
</section>
"""

NEWSLETTER = f"""<section class="nl" aria-label="Newsletter">
  <div class="wrap">
    <div><h4>Hear from the workshop.</h4><p>An occasional note when something is worth telling – a delivery, a reveal, a date for the diary. No more than once a month.</p></div>
    <div><form class="nl-form" novalidate><input type="email" name="email" placeholder="Your email address" required autocomplete="email" inputmode="email" aria-label="Email address"><button type="submit">Keep me informed</button></form><div class="msg" aria-live="polite"></div></div>
  </div>
</section>
""" if FEAT.get("newsletter") else ""

ASK_BTN = f"""<button type="button" class="ask" id="ask" aria-haspopup="dialog"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 5h16v11H9l-5 4z"/></svg>{FEAT.get("assistant_name","Ask the workshop")}</button>
<div class="modal" id="askm" role="dialog" aria-modal="true" aria-labelledby="ask-title" hidden>
  <div class="sheet">
    <h3 id="ask-title">{FEAT.get("assistant_name","Ask the workshop")}</h3>
    <p class="intro">Quick answers about the motorcycles, prices, delivery and visiting. For anything else, the team replies personally.</p>
    <div class="chat" id="chat"><div class="m a">Hello. What would you like to know?</div></div>
    <form class="chatform" id="chatform"><input name="q" placeholder="Ask a question…" autocomplete="off" aria-label="Your question" maxlength="500"><button type="submit">Send</button></form>
    <p class="fine">An automated assistant that answers from Langen's published information. It doesn't take bookings or payments.</p>
    <button type="button" class="close" id="ask-close">Close</button>
  </div>
</div>
""" if FEAT.get("assistant") else ""

FOOTER = f"""{NEWSLETTER}<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <img class="logo" src="assets/langen_logo_white.svg" alt="Langen">
        <p>Hand-built British motorcycles, designed, engineered and made to order in Wigan, England. We do things differently here.</p>
        <div class="social">
          <a href="https://www.instagram.com/langenmotorcycles/" aria-label="Instagram"><svg viewBox="0 0 24 24"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 4.7a5.1 5.1 0 1 0 0 10.2 5.1 5.1 0 0 0 0-10.2zm0 8.4a3.3 3.3 0 1 1 0-6.6 3.3 3.3 0 0 1 0 6.6zm5.3-8.6a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4z"/></svg></a>
          <a href="https://www.facebook.com/LangenMotorcycles/" aria-label="Facebook"><svg viewBox="0 0 24 24"><path d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.5 1.6-1.5h1.7V4.4c-.3 0-1.3-.1-2.5-.1-2.5 0-4.1 1.5-4.1 4.2v2.3H7.4V14h2.8v8h3.3z"/></svg></a>
          <a href="https://www.youtube.com/channel/UCXdvDfQtxKh5ncwrAJJo38A" aria-label="YouTube"><svg viewBox="0 0 24 24"><path d="M23 7.2c-.3-1-1-1.8-2-2C19.2 4.7 12 4.7 12 4.7s-7.2 0-9 .5c-1 .3-1.8 1-2 2C.5 9 .5 12 .5 12s0 3 .5 4.8c.3 1 1 1.8 2 2 1.8.5 9 .5 9 .5s7.2 0 9-.5c1-.3 1.8-1 2-2 .5-1.8.5-4.8.5-4.8s0-3-.5-4.8zM9.7 15.1V8.9l6 3.1-6 3.1z"/></svg></a>
          <a href="https://www.linkedin.com/company/langen-motorcycles/" aria-label="LinkedIn"><svg viewBox="0 0 24 24"><path d="M20.4 2H3.6C2.7 2 2 2.7 2 3.6v16.8c0 .9.7 1.6 1.6 1.6h16.8c.9 0 1.6-.7 1.6-1.6V3.6c0-.9-.7-1.6-1.6-1.6zM8 19H5V9.5h3V19zM6.5 8.2a1.7 1.7 0 1 1 0-3.5 1.7 1.7 0 0 1 0 3.5zM19 19h-3v-4.6c0-1.1 0-2.5-1.5-2.5s-1.8 1.2-1.8 2.4V19h-3V9.5h2.9v1.3c.4-.8 1.4-1.5 2.8-1.5 3 0 3.6 2 3.6 4.6V19z"/></svg></a>
        </div>
      </div>
      <div><h4>Motorcycles</h4><a href="lightspeed.html">Lightspeed</a><a href="two-stroke.html">Two Stroke</a><a href="pre-owned.html">Certified Pre-Owned</a><a href="commission.html">Commissioning</a></div>
      <div><h4>Langen</h4><a href="about.html">About</a><a href="news.html">News</a><a href="careers.html">Careers</a><a href="https://langenmotorcycles.shop.dowlis.com/">Merch</a><a href="contact.html">Contact</a></div>
      <div><h4>Owners</h4><a href="owners.html">Owners' portal</a><a href="owners.html#press">Press</a><a href="contact.html#faq">FAQ</a><a href="privacy.html">Privacy policy</a></div>
    </div>
    <div class="legal"><span>© Langen Technology Ltd, trading as Langen Motorcycles. Registered in England &amp; Wales no. 11601010.</span><span>Specifications correct at time of publication and subject to change.</span></div>
  </div>
</footer>
<div class="bar">
  <a class="btn ghost" href="{STRIPE}">Reserve</a>
  <a class="btn gold" href="{ENQ_LS}">Enquire</a>
</div>
<div class="cookie" id="cookie" role="dialog" aria-label="Cookie notice">
  <p>We use analytics to understand how this site is read. No advertising cookies are set. OK?</p>
  <button type="button" class="yes" id="ck-yes">Accept</button><button type="button" id="ck-no">Decline</button>
</div>
<div class="modal" id="terms" role="dialog" aria-modal="true" aria-labelledby="terms-title" hidden>
  <div class="sheet terms">
    <h3 id="terms-title" tabindex="-1" style="outline:none">Lightspeed reservation deposit – terms</h3>
    <ol>
      <li><b>The deposit.</b> A reservation deposit of {SITE["lightspeed"]["deposit"]} (the “Deposit”) is payable to Langen Technology Ltd, trading as Langen Motorcycles (“Langen”). On receipt, Langen allocates you a numbered Lightspeed build slot, in order of deposits received, from a production run limited to {SITE["lightspeed"]["builds"]} motorcycles.</li>
      <li><b>What the Deposit secures.</b> The Deposit secures your place in the build queue and an invitation to a specification session with the Langen team. It does not, on its own, constitute an order for a motorcycle.</li>
      <li><b>Refundable period.</b> The Deposit is fully refundable at any time until all three of the following have occurred: (a) your specification session has been completed; (b) you have signed a Langen sales agreement for the motorcycle; and (c) Langen has commenced manufacture of your motorcycle. Until then, you may request a refund for any reason.</li>
      <li><b>After that point.</b> Once (a), (b) and (c) have all occurred, the Deposit is applied to the purchase price and is governed by the terms of your signed sales agreement, including any cancellation provisions in it.</li>
      <li><b>How to request a refund.</b> Email {MAIL} from the address used at reservation, quoting your name and build slot number. Langen will refund the full Deposit to the original payment method within 14 days of your request. Your build slot is released on refund.</li>
      <li><b>Price.</b> The Lightspeed is priced from {SITE["lightspeed"]["price_from"]} plus VAT and any applicable local taxes, duties and delivery. The final price depends on the specification you choose and is confirmed in your sales agreement. The Deposit is deducted from the final price.</li>
      <li><b>Delivery and specification.</b> Delivery estimates and market availability are indicative and may change, including for reasons of homologation in your country. Langen may make changes to the specification of the Lightspeed before your sales agreement is signed.</li>
      <li><b>Transfer.</b> Build slots are personal to you and may not be sold or transferred without Langen’s written agreement.</li>
      <li><b>Your rights.</b> These terms do not affect your statutory rights as a consumer. They are governed by the laws of England and Wales.</li>
    </ol>
    <p>Langen Technology Ltd, registered in England &amp; Wales no. 11601010. Unit 1, Kingfisher Court, Wigan WN4 9DW.</p>
    <button type="button" class="close" id="terms-close">Close</button>
  </div>
</div>
<div class="modal" id="enq" role="dialog" aria-modal="true" aria-labelledby="enq-title" hidden>
  <div class="sheet">
    <h3 id="enq-title">Enquire</h3>
    <p class="intro">Tell us where you are and what you have in mind. Christofer or one of the team will reply personally, usually {REPLY_TIME}.</p>
    {enquiry_form("enq-form")}
    <details class="alt"><summary>Prefer email or phone?</summary>
      <div class="addr"><span>{MAIL}</span><button type="button" id="copy-btn">Copy</button></div>
      <div class="list">
        <a class="btn ghost" id="enq-mail" href="{ENQ_GEN}">Open in your email app</a>
        <a class="btn ghost" href="tel:{TEL}">Call {TELFMT}</a>
        <a class="btn ghost" href="{STRIPE}">Reserve a Lightspeed – £1,000 refundable deposit</a>
      </div>
    </details>
    <button type="button" class="close" id="enq-close">Close</button>
  </div>
</div>
<div class="modal" id="bro" role="dialog" aria-modal="true" aria-labelledby="bro-title" hidden>
  <div class="sheet">
    <h3 id="bro-title">The Lightspeed brochure</h3>
    <p class="intro">Tell us where to send it and the brochure opens straight away. We'll keep you informed as the first Lightspeeds are delivered; unsubscribe any time.</p>
    <form class="enq-form bro-form" novalidate>
      <input type="hidden" name="subject" value="Brochure request">
      <div class="row2"><label>Name<input name="name" autocomplete="name"></label><label>Email<input name="email" type="email" required autocomplete="email" inputmode="email"></label></div>
      <div class="hp" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
      <div class="err" aria-live="polite"></div>
      <button class="btn gold" type="submit">Send me the brochure</button>
    </form>
    <div class="done" hidden><h3>On its way.</h3><p>If it hasn't opened, <a href="{BROCHURE}" id="bro-direct" style="color:#fff">download the brochure here</a>.</p></div>
    <button type="button" class="close" id="bro-close">Close</button>
  </div>
</div>
{ASK_BTN}
<script src="site.js"></script>
</body>
</html>
"""

JS = "// Built from content/site.yml – edit the IDs there, not here.\nvar LANGEN_GA4_ID = " + _json.dumps((SITE.get("analytics") or {}).get("ga4_id", "") or "") + ";\nvar LANGEN_META_PIXEL = " + _json.dumps(str((SITE.get("analytics") or {}).get("meta_pixel", "") or "")) + ";\n" + r"""
(function(){
  if(LANGEN_GA4_ID){
    var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+LANGEN_GA4_ID;document.head.appendChild(s);
    gtag('js',new Date());gtag('config',LANGEN_GA4_ID);
  }
  if(LANGEN_META_PIXEL){
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    fbq('init',LANGEN_META_PIXEL);fbq('track','PageView');
  }
})();
// ---- film hero: load the right file, only when motion is welcome ----
(function(){var v=document.querySelector('.hero.film video.bg');if(!v)return;
  var m=window.matchMedia('(prefers-reduced-motion: reduce)').matches,sd=navigator.connection&&navigator.connection.saveData;
  if(m||sd)return;
  var small=Math.min(window.innerWidth,window.innerHeight)<=760;
  v.src=small?(v.dataset.srcSmall||v.dataset.src):v.dataset.src;
  v.addEventListener('playing',function(){v.classList.add('on');},{once:true});
  var p=v.play();if(p&&p.catch)p.catch(function(){});
})();
// ---- top bar: transparent over the hero, solid once scrolled ----
(function(){var t=document.getElementById('top');if(!t)return;function f(){t.classList.toggle('scrolled',window.scrollY>24);}f();window.addEventListener('scroll',f,{passive:true});})();

// ---- reveal on scroll ----
(function(){
  if(!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var els=document.querySelectorAll('section:not(.hero) > .wrap, .models .model, .bleed .wrap, .numbers-band .wrap, .pair figure, .strip figure');
  var io=new IntersectionObserver(function(en){en.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});
  els.forEach(function(el){var r=el.getBoundingClientRect();if(r.top<window.innerHeight*.9){return;}el.classList.add('rv');io.observe(el);});
})();
// ---- sticky chapter index ----
(function(){
  var sn=document.querySelector('.subnav');if(!sn)return;
  var links=[].slice.call(sn.querySelectorAll('a[href^="#"]'));
  var secs=links.map(function(a){return document.querySelector(a.getAttribute('href'))}).filter(Boolean);
  function upd(){var y=window.scrollY+140,cur=null;secs.forEach(function(s){if(s.offsetTop<=y)cur=s;});links.forEach(function(a){a.classList.toggle('on',cur&&a.getAttribute('href')==='#'+cur.id);});}
  upd();window.addEventListener('scroll',upd,{passive:true});
  links.forEach(function(a){a.addEventListener('click',function(e){var t=document.querySelector(a.getAttribute('href'));if(!t)return;e.preventDefault();var top=t.getBoundingClientRect().top+window.scrollY-120;window.scrollTo({top:top,behavior:'smooth'});history.replaceState(null,'',a.getAttribute('href'));});});
})();
// ---- annotated feature: one open at a time, swap the figure ----
(function(){
  document.querySelectorAll('.anno').forEach(function(an){
    var img=an.querySelector('figure img'),items=an.querySelectorAll('details');
    items.forEach(function(d){d.addEventListener('toggle',function(){if(!d.open)return;items.forEach(function(o){if(o!==d)o.open=false;});var src=d.getAttribute('data-img');if(src&&img.getAttribute('src')!==src){img.classList.add('fade');setTimeout(function(){var pic=img.parentElement;if(pic&&pic.tagName==='PICTURE'){[].forEach.call(pic.querySelectorAll('source'),function(s){s.remove();});}img.src=src;img.alt=d.querySelector('summary').textContent.trim();img.onload=function(){img.classList.remove('fade');};},220);}});});
  });
})();
// ---- gallery strip arrows ----
(function(){
  document.querySelectorAll('.strip-wrap').forEach(function(w){var s=w.querySelector('.strip'),nav=w.querySelector('.strip-nav');if(!s||!nav)return;
    var step=function(){var f=s.querySelector('figure');return f?f.getBoundingClientRect().width+2:400;};
    nav.querySelector('.prev').addEventListener('click',function(){s.scrollBy({left:-step(),behavior:'smooth'});});
    nav.querySelector('.next').addEventListener('click',function(){s.scrollBy({left:step(),behavior:'smooth'});});
  });
})();
// ---- cookie banner ----
(function(){var c=document.getElementById('cookie'),seen=null;try{seen=localStorage.getItem('ln_consent');}catch(e){}
if(!seen){c.classList.add('show');}
function set(v){try{localStorage.setItem('ln_consent',v);}catch(e){}c.classList.remove('show');if(v==='granted'&&window.gtag){gtag('consent','update',{analytics_storage:'granted'});}}
document.getElementById('ck-yes').addEventListener('click',function(){set('granted');});
document.getElementById('ck-no').addEventListener('click',function(){set('denied');});
})();
// ---- mobile menu ----
(function(){var b=document.getElementById('burger'),d=document.getElementById('drawer'),t=document.getElementById('top');if(!b)return;
b.addEventListener('click',function(){var o=d.classList.toggle('open');b.setAttribute('aria-expanded',o);document.body.style.overflow=o?'hidden':'';t.classList.toggle('solid',o);});
})();
// ---- enquiry panel, forms, brochure, newsletter, assistant ----
(function(){
  var m=document.getElementById('enq'),last=null,mailBtn=document.getElementById('enq-mail');
  function lead(kind){if(window.fbq)fbq('track','Lead',{content_name:'Langen enquiry'});if(window.gtag)gtag('event','generate_lead',{method:kind});}
  function reserve(){if(window.fbq)fbq('track','InitiateCheckout',{content_name:'Lightspeed deposit',currency:'GBP',value:1000});if(window.gtag)gtag('event','begin_checkout',{currency:'GBP',value:1000});}
  function subjectOf(href){var t=/subject=([^&]+)/.exec(href||'');return t?decodeURIComponent(t[1]).replace(/\+/g,' '):'Enquiry';}
  function openSheet(el){el.hidden=false;el.classList.add('open');document.body.style.overflow='hidden';}
  function closeSheet(el){el.classList.remove('open');el.hidden=true;document.body.style.overflow='';}
  // open the panel from any mailto link outside the footer/drawer/contact block
  function open(e){e.preventDefault();last=e.currentTarget;var href=last.getAttribute('href'),subj=subjectOf(href);
    if(mailBtn)mailBtn.href=href;document.getElementById('enq-title').textContent=subj;
    var f=document.getElementById('enq-form');if(f){f.subject.value=subj;f.page.value=location.pathname;var sel=f.model;if(/two stroke|pre-owned/i.test(subj))sel.value='two-stroke';else if(/visit/i.test(subj))sel.value='visit';else if(/lightspeed/i.test(subj))sel.value='lightspeed';else sel.value='other';}
    openSheet(m);var first=m.querySelector('input[name=name]');if(first)first.focus();
    if(window.fbq)fbq('trackCustom','EnquiryPanelOpen');if(window.gtag)gtag('event','enquiry_panel_open');}
  function close(){closeSheet(m);if(last)last.focus();}
  document.querySelectorAll('a[href^="mailto:"]').forEach(function(a){if(!m.contains(a)&&!a.closest('.site-footer')&&!a.closest('.drawer')&&!a.closest('#enquire .contact')&&!a.closest('.contact-form'))a.addEventListener('click',open);});
  document.getElementById('enq-close').addEventListener('click',close);
  m.addEventListener('click',function(e){if(e.target===m)close();});
  // ---- form submission (panel + contact page) ----
  function post(path,data){return fetch(path,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(data)}).then(function(r){return r.json().catch(function(){return {}}).then(function(j){return {ok:r.ok,status:r.status,j:j}})}).catch(function(){return {ok:false,status:0,j:{}}})}
  function vals(f){var o={};new FormData(f).forEach(function(v,k){o[k]=v});if(window.turnstile&&f.querySelector('.cf-turnstile')){try{o.turnstile=turnstile.getResponse(f.querySelector('.cf-turnstile'));}catch(e){}}return o}
  var MAILTO='mailto:'+'info@langenmotorcycles.co.uk';
  document.querySelectorAll('form.enq-form:not(.bro-form)').forEach(function(f){
    f.addEventListener('submit',function(e){e.preventDefault();var err=f.querySelector('.err'),btn=f.querySelector('button[type=submit]');err.innerHTML='';
      var v=vals(f);if(!v.name||!v.email||!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.email)){err.textContent='Please add your name and a working email address.';return;}
      v.page=v.page||location.pathname;try{v.utm=location.search.slice(0,300);v.referrer=document.referrer.slice(0,200);}catch(x){}
      btn.disabled=true;btn.textContent='Sending…';
      post('/api/enquire',v).then(function(r){btn.disabled=false;btn.textContent='Send enquiry';
        if(r.ok){f.hidden=true;var d=f.nextElementSibling;if(d&&d.classList.contains('done'))d.hidden=false;lead('form');try{if(window.turnstile)turnstile.reset();}catch(x){}}
        else{var body=encodeURIComponent('Hi Langen,\n\n'+(v.message||'')+'\n\nName: '+v.name+'\nCountry: '+(v.country||'')+'\nPhone: '+(v.phone||''));
          var em=(r.j&&r.j.error)||'We couldn\'t send that just now.';if(!/[.!?]$/.test(em))em+='.';err.innerHTML=em+' You can <a href="'+MAILTO+'?subject='+encodeURIComponent(v.subject||'Enquiry')+'&body='+body+'">email us directly</a> instead.';}
      });});
  });
  // ---- brochure request ----
  var bro=document.getElementById('bro'),broLast=null;
  document.querySelectorAll('a.bro-link').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();broLast=a;openSheet(bro);var i=bro.querySelector('input[name=email]');if(i)i.focus();if(window.gtag)gtag('event','brochure_request_open');});});
  if(bro){document.getElementById('bro-close').addEventListener('click',function(){closeSheet(bro);if(broLast)broLast.focus();});bro.addEventListener('click',function(e){if(e.target===bro)closeSheet(bro);});
    var bf=bro.querySelector('form.bro-form');bf.addEventListener('submit',function(e){e.preventDefault();var err=bf.querySelector('.err'),btn=bf.querySelector('button[type=submit]'),v=vals(bf);err.textContent='';
      if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.email||'')){err.textContent='Please add a working email address.';return;}
      btn.disabled=true;btn.textContent='One moment…';v.page=location.pathname;
      post('/api/brochure',v).then(function(r){btn.disabled=false;btn.textContent='Send me the brochure';var url=(r.ok&&r.j&&r.j.url)||document.getElementById('bro-direct').getAttribute('href');
        bf.hidden=true;bf.nextElementSibling.hidden=false;document.getElementById('bro-direct').href=url;if(window.gtag)gtag('event','brochure_download');if(window.fbq)fbq('track','Lead',{content_name:'Brochure request'});
        try{window.open(url,'_blank','noopener');}catch(x){location.href=url;}});});}
  // ---- newsletter ----
  document.querySelectorAll('form.nl-form').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();var msg=f.parentElement.querySelector('.msg'),em=f.email.value.trim();msg.textContent='';
    if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)){msg.textContent='Please add a working email address.';return;}
    f.querySelector('button').disabled=true;post('/api/subscribe',{email:em,source:'footer',page:location.pathname}).then(function(r){f.querySelector('button').disabled=false;
      if(r.ok){f.hidden=true;msg.textContent='Thank you – you\'re on the list. If Mailchimp asks you to confirm, that email is from us.';if(window.gtag)gtag('event','newsletter_signup');}
      else{msg.textContent=(r.j&&r.j.error)||'We couldn\'t add you just now – email '+'info@langenmotorcycles.co.uk'+' and we\'ll do it by hand.';}});});});
  // ---- assistant ----
  var ask=document.getElementById('ask'),am=document.getElementById('askm');
  if(ask&&am){var chat=document.getElementById('chat'),cf=document.getElementById('chatform'),hist=[];
    function add(role,text,wait){var d=document.createElement('div');d.className='m '+(role==='user'?'u':'a')+(wait?' wait':'');d.textContent=text;chat.appendChild(d);chat.scrollTop=chat.scrollHeight;return d;}
    ask.addEventListener('click',function(){openSheet(am);cf.q.focus();if(window.gtag)gtag('event','assistant_open');});
    document.getElementById('ask-close').addEventListener('click',function(){closeSheet(am);});am.addEventListener('click',function(e){if(e.target===am)closeSheet(am);});
    cf.addEventListener('submit',function(e){e.preventDefault();var q=cf.q.value.trim();if(!q)return;cf.q.value='';add('user',q);hist.push({role:'user',content:q});var w=add('assistant','…',true);
      post('/api/assist',{messages:hist.slice(-8),page:location.pathname}).then(function(r){var t=(r.ok&&r.j&&r.j.reply)||(r.j&&r.j.error)||'I can\'t answer just now – the team will, if you use the enquiry form.';w.textContent=t;w.classList.remove('wait');hist.push({role:'assistant',content:t});});});}
  // ---- terms sheet ----
  var t=document.getElementById('terms'),tlast=null;
  function topen(e){e.preventDefault();tlast=e.currentTarget;openSheet(t);t.querySelector('.sheet').scrollTop=0;document.getElementById('terms-title').focus();}
  function tclose(){closeSheet(t);if(tlast)tlast.focus();}
  document.querySelectorAll('.terms-link').forEach(function(a){a.addEventListener('click',topen);});
  document.getElementById('terms-close').addEventListener('click',tclose);
  t.addEventListener('click',function(e){if(e.target===t)tclose();});
  document.addEventListener('keydown',function(e){if(e.key!=='Escape')return;[m,t,bro,am].forEach(function(x){if(x&&x.classList.contains('open'))closeSheet(x);});});
  // ---- copy address + tracking on the secondary links ----
  var cb=document.getElementById('copy-btn');
  if(cb){cb.addEventListener('click',function(){var v='info@langenmotorcycles.co.uk';function done(){cb.textContent='Copied';setTimeout(function(){cb.textContent='Copy';},2000);lead('copy');}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(v).then(done,fb);}else{fb();}
    function fb(){var r=document.createRange();r.selectNodeContents(cb.previousElementSibling);var s=window.getSelection();s.removeAllRanges();s.addRange(r);try{document.execCommand('copy');done();}catch(e){}}});}
  if(mailBtn)mailBtn.addEventListener('click',function(){lead('email');});
  document.querySelectorAll('#enq a[href^="tel:"]').forEach(function(a){a.addEventListener('click',function(){lead('phone');});});
  document.querySelectorAll('a[href*="buy.stripe.com"]').forEach(function(a){a.addEventListener('click',reserve);});
  document.querySelectorAll('a[href$=".pdf"]:not(.bro-link)').forEach(function(a){a.addEventListener('click',function(){if(window.gtag)gtag('event','brochure_download');});});
})();
"""
