from common import *
from portal import OWNERS as OWNERS_PORTAL, PORTAL_CSS
from content import load_news, load_preowned
LS = SITE["lightspeed"]; TS = SITE["two_stroke"]
NEWS = load_news()
PREOWNED_BIKES = load_preowned()

def enq(subject, body=None): return mailto(subject, body)

def numbers(items):
    return '<div class="numbers">' + "".join(f'<div><b>{b}</b><span>{s}</span></div>' for b,s in items) + '</div>'

def numbers_band(items, note=None):
    n = f'<p class="price">{note}</p>' if note else ""
    return f'<div class="numbers-band"><div class="wrap">{numbers(items)}{n}</div></div>'

def chapter(n, t): return f'<div class="chapter"><span>{n}</span>{t}</div>'

def subnav(name, items):
    links = "".join(f'<a href="#{i}">{t}</a>' for i,t in items)
    return f'<nav class="subnav" aria-label="{name} sections"><div class="wrap"><span class="name">{name}</span>{links}</div></nav>'

def anno(items):
    """items: (title, tag, body, img). The first image is shown until an item is opened."""
    first = items[0][3]
    lis = "".join(f'<details data-img="{img}"{" open" if i==0 else ""}><summary>{t}<small>{tag}</small></summary><p>{b}</p></details>' for i,(t,tag,b,img) in enumerate(items))
    return f'<div class="anno"><figure><img src="{first}" alt="{items[0][0]}" loading="lazy"></figure><div class="list">{lis}</div></div>'

ARROW_L = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M15 5l-7 7 7 7"/></svg>'
ARROW_R = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 5l7 7-7 7"/></svg>'
def strip(kicker, title, items):
    """items: (img, alt, h3, p, object-position or None)"""
    figs = "".join(f'<figure><img src="{img}" alt="{alt}" loading="lazy"{f" style=\"object-position:{pos}\"" if pos else ""}><figcaption><h3>{h}</h3><p>{d}</p></figcaption></figure>' for img,alt,h,d,pos in items)
    return f"""<section class="strip-head"><div class="wrap">{chapter(kicker[0],kicker[1])}<h2 class="section-title">{title}</h2></div></section>
<div class="strip-wrap"><div class="strip-nav"><button type="button" class="prev" aria-label="Previous">{ARROW_L}</button><button type="button" class="next" aria-label="Next">{ARROW_R}</button></div><div class="strip">{figs}</div></div>"""

LETTER = f"""
<section class="light letter-wrap">
  <div class="wrap letter">
    {chapter("A note from the founder","")}
    <p>I spent the first part of my career designing motorcycles for other companies, where the brief was always a bike for as many people as possible. I started Langen in 2018 to build a motorcycle for one rider at a time, with a team small enough to know each of those riders by name, and to make it light enough that you feel the road through every part of it.</p>
    <p>We are a small company in Wigan and we intend to stay one. Every bike goes through the same hands, and every owner has my number. If you commission one, you will spend a day with us before anything is cut, and you will know who made each part and why it is the way it is.</p>
    <p>Every part on a Langen has a job. If we cannot say what a part is for, it comes off.</p>
    <footer>Christofer Ratcliffe<br><small>Founder, Langen Motorcycles</small></footer>
  </div>
</section>
"""

def news_cards(items, feature=True):
    out=[]
    for i,it in enumerate(items):
        cls="card feature" if (feature and i==0) else "card"
        href=it["external"] or it["href"]
        out.append(f'<a class="{cls}" id="{it["slug"]}" href="{href}"><img src="{it["image"]}" alt="{it["image_alt"]}" loading="lazy"><div class="txt"><span class="meta">{it["date_display"]}</span><h3>{it["title"]}</h3><p>{it["summary"]}</p></div></a>')
    return "".join(out)

# ------------------------------------------------------------------ HOME
HOME = f"""
<section class="hero open film" style="padding:0">
  <!-- The opening film: 22 s silent loop cut from the Gun Hill Studios Lightspeed film. site.js picks the 720 or 1080 file by screen size
       and skips the video entirely for reduced-motion / data-saver visitors, who see the poster. -->
  <img class="bg" src="assets/home_hero_poster.jpg" alt="Langen Lightspeed halo headlamp in the dark" fetchpriority="high" style="object-position:50% 50%">
  <video class="bg" muted loop playsinline preload="none" aria-hidden="true" data-src="assets/home_hero.mp4" data-src-small="assets/home_hero_720.mp4" poster="assets/home_hero_poster.jpg"></video>
  <div class="veil"></div>
  <div class="wrap">
    <div class="kicker">Langen · Wigan, England</div>
    <h1>Made for one rider at a time.</h1>
    <a class="tlink" href="lightspeed.html">The Lightspeed</a>
  </div>
  <div class="scroll" aria-hidden="true">Scroll</div>
</section>

<section class="manifesto">
  <div class="wrap">
    <span class="kicker">Why we exist</span>
    <h2>We build one motorcycle at a time, for one rider, around how they sit on it and where they ride it.</h2>
  </div>
</section>

<div class="models">
  <a class="model" href="lightspeed.html">
    <img src="assets/ls_profile.jpg" alt="Langen Lightspeed, side profile, studio" loading="lazy">
    <div class="veil"></div>
    <div class="txt"><img src="assets/ls_white.png" alt="Lightspeed"><p>185 horsepower. 185 kilograms. One of 185.</p><span class="cta">Explore</span></div>
  </a>
  <a class="model" href="two-stroke.html">
    <img src="assets/ts_profile.jpg" alt="Langen Two Stroke, side profile, studio" loading="lazy">
    <div class="veil"></div>
    <div class="txt"><img class="ts" src="assets/2strokeWhite.svg" alt="Two Stroke"><p>Our first motorcycle. One hundred built, 2019 to 2025.</p><span class="cta">Explore</span></div>
  </a>
</div>

<section class="light">
  <div class="wrap split">
    <div>
      {chapter("01","The idea")}
      <h2 class="section-title">Built around the rider.</h2>
      <p class="lede">Before anything is cut, we measure the rider: height, reach, how they sit, where they ride. Seat, bars, footrests, ride height and suspension are set to those numbers. Then paint, finishes and the machined parts are chosen with the engineers who will make them. The bike that leaves Wigan has been built around one person.</p>
      <div class="btns" style="margin-top:30px"><a class="tlink" href="commission.html">How a commission works</a></div>
    </div>
    <img src="assets/ts_build_frame2.jpg" alt="A Langen engineer fitting a Two Stroke chassis in the workshop" loading="lazy" style="object-position:30% 50%">
  </div>
</section>

<section class="bleed">
  <img class="bg" src="assets/workshop_wide.jpg" alt="Inside the Langen workshop in Wigan – four Two Strokes on the lifts" style="object-position:55% 45%">
  <div class="veil"></div>
  <div class="wrap">
    {chapter("02","The people")}
    <h2>A small team, and you will meet all of them.</h2>
    <p>The engineers and designers here came from CCM, Triumph, BAC, McLaren and M-Sport. There is no dealer. You deal with the people who design and build the bikes, and when you call about yours, one of them picks up.</p>
    <div class="btns" style="margin-top:26px"><a class="tlink" href="about.html">About Langen</a></div>
  </div>
</section>

<section class="pull">
  <div class="wrap">
    <blockquote class="big">Every part on a Langen has a job. If we cannot say what a part is for, it comes off.<footer><a class="tlink" href="about.html">Christofer Ratcliffe, founder</a></footer></blockquote>
  </div>
</section>

<section class="carbon">
  <div class="wrap split wide">
    <div>
      {chapter("03","The ride")}
      <h2 class="section-title">Weight comes first.</h2>
      <p class="lede">The Two Stroke weighs 120 kg. The Lightspeed weighs 185 kg and makes 185 horsepower. Every design here starts with a weight target and the rest of the bike is held to it, because weight is what you feel in every corner, every braking point and every change of direction.</p>
      <blockquote>“…the benchmark handling of its sweet-steering chassis. Langen Motorcycles’ debut model has hit the bullseye.”<footer>motorcycle.com</footer></blockquote>
    </div>
    <img src="assets/ls_front_bokeh.jpg" alt="Lightspeed head-on, lights on, in a dark studio" loading="lazy" style="object-position:50% 50%">
  </div>
</section>

<section class="light">
  <div class="wrap">
    {chapter("04","Lately")}
    <h2 class="section-title">From the workshop.</h2>
    <div class="news">{news_cards(NEWS[:3], feature=False)}
    </div>
    <div class="btns" style="margin-top:34px"><a class="tlink" href="news.html">All news</a></div>
  </div>
</section>

{enquire_block("Talk to us", "Tell us where you are and what you have in mind, and Christofer or one of the team will reply personally, usually within a working day.")}
<style>.bar{{display:none}}body{{padding-bottom:0}}</style>
"""

# ------------------------------------------------------------------ LIGHTSPEED
LIGHTSPEED = f"""
<section class="hero" style="padding:0">
  <img class="bg" src="assets/ls_top_dark.jpg" alt="Langen Lightspeed from above, in the dark" fetchpriority="high" data-mobile-pos style="object-position:72% 40%;--mpos:58% 30%">
  <div class="veil"></div>
  <div class="wrap">
    <div class="kicker">One of 185</div>
    <img class="mark" src="assets/ls_white.png" alt="Lightspeed">
    <h1>A 185 hp V-twin, built around its rider.</h1>
    <div class="btns">
      <a class="btn gold" href="{ENQ_LS}">{ICON_MAIL}Enquire about a build</a>
      <a class="tlink" href="{STRIPE}">Reserve a build number</a>
    </div>
  </div>
</section>
{subnav("Lightspeed",[("overview","Overview"),("engineering","Engineering"),("colour","Colour"),("commission","Commission"),("worldwide","Worldwide"),("technical","Technical")])}
{numbers_band([("185","hp"),("185","kg"),("185","builds"),("1,000","bhp / tonne")], 'From ' + LS['price_from'] + ' plus VAT. A numbered build is reserved with a refundable ' + LS['deposit'] + ' deposit. <a href="#" class="terms-link">Deposit terms</a>' + (f' · {LS["allocated"]} of {LS["builds"]} allocated' if LS.get('allocated') else ''))}

<section class="light" id="overview">
  <div class="wrap split">
    <div>
      {chapter("01","The motorcycle")}
      <h2 class="section-title">What it is.</h2>
      <p class="lede">The Lightspeed is a 1,190cc V-twin road bike with 185 horsepower and a dry weight of 185 kilograms. It has superbike suspension and brakes, a 19-litre tank and a 790 mm seat, and it is built to be ridden a long way. Up close, most of what you see was machined, welded or laid up within a few miles of the workshop.</p>
      <blockquote>Every Lightspeed is set up and specified for the person who ordered it. We spend a day with each owner before we start, and it shows in the bike.<footer>Christofer Ratcliffe, founder</footer></blockquote>
    </div>
    <img class="sq" src="assets/ls_studio_grey.jpg" alt="Lightspeed, front three-quarter, studio" loading="lazy" style="object-position:50% 55%">
  </div>
</section>

<section class="bleed">
  <img class="bg" src="assets/ls_macro_engine.jpg" alt="Lightspeed engine cover with the LS mark, carbon and titanium around it" style="object-position:50% 50%">
  <div class="veil"></div>
  <div class="wrap">
    <h2>Nothing is hidden under a panel.</h2>
    <p>The engine and the chassis are in plain view. The carbon is laid by hand, the frame is welded by a firm that welds for Formula 1 teams, and the billet parts are machined a few minutes from the workshop. We would rather you could see all of that.</p>
  </div>
</section>

<section id="engineering">
  <div class="wrap">
    {chapter("02","What it is made of")}
    <h2 class="section-title">Every part was chosen or made here.</h2>
    {anno([
      ("The engine","1,190cc V-twin","Liquid-cooled 72º V-twin, developed by Rotax and built by Buell, running Langen's own injection and electronics. 185 hp, 138 Nm, with most of the torque available from the middle of the rev range.","assets/ls_macro_engine_exhaust.jpg"),
      ("185 kilograms","Carbon and forged aluminium","Full carbon bodywork and Langen forged, CNC-machined wheels. Over 1,000 bhp per tonne, on a bike with a 19-litre tank.","assets/ls_macro_sprocket.jpg"),
      ("Öhlins at both ends","Set to you","FGRT 301 48 mm forks with a superbike cartridge kit; twin STX piggyback shocks behind. Set to you at your fitting. K-Tech Racing pack available.","assets/ls_macro_shock.jpg"),
      ("Brakes","Made with HEL","Twin 320 mm floating discs and four-piston radial calipers made with HEL; 265 mm at the rear. Cornering ABS.","assets/ls_macro_caliper.jpg"),
      ("Electronics","Written in house","Traction, wheelie, launch and cruise control, developed in house so they could be calibrated for this engine and this chassis. The dash is machined from solid aluminium and carries a TFT touchscreen.","assets/ls_macro_cockpit.jpg"),
      ("The exhaust","Machined end cap","Langen system with a machined, engraved end cap. A full titanium race system is available.","assets/ls_macro_endcap.jpg"),
    ])}
  </div>
</section>

{strip(("","In detail"),"Close up.",[
  ("assets/ls_macro_lamp_side.jpg","Lightspeed halo headlamp in its carbon nacelle","The headlamp.","LED halo lamp in a machined bezel and carbon nacelle.","45% 50%"),
  ("assets/ls_macro_filler.jpg","Lightspeed machined filler cap","The filler cap.","Machined from one piece of aluminium, a few minutes from the workshop.","50% 50%"),
  ("assets/ls_macro_tank.jpg","Lightspeed tank with the Langen script","The tank.","Hand-laid carbon under paint, or left bare. Nineteen litres.","60% 50%"),
  ("assets/ls_macro_endcap.jpg","Lightspeed exhaust end cap","The end cap.","Machined and engraved. A titanium race system is available.","55% 50%"),
  ("assets/ls_macro_cockpit.jpg","Lightspeed cockpit from above","The cockpit.","A machined dash, a TFT touchscreen, and bars set to your reach at the fitting.","50% 45%"),
  ("assets/ls_macro_fuelcap.jpg","Lightspeed carbon tank top and fuel cap","The bodywork.","Every panel is laid up by hand by a firm that also makes parts for Formula 1 teams.","50% 50%"),
  ("assets/ls_macro_sprocket.jpg","Lightspeed rear sprocket and forged wheel","The rear wheel.","Forged aluminium, machined and anodised. The sprocket carrier is our own part.","50% 50%"),
  ("assets/ls_macro_caliper.jpg","Lightspeed brake caliper and disc","The brakes.","Four-piston radial calipers made with HEL on 320 mm floating discs.","50% 50%"),
  ("assets/ls_macro_wheel.jpg","Lightspeed front wheel and radiator","The front wheel.","Our own forged aluminium wheel, machined and anodised to the owner's specification.","50% 50%"),
  ("assets/ls_macro_seat.jpg","Lightspeed seat and tail","The tail.","A seat shaped for long days, on a hand-laid carbon tail unit.","50% 50%"),
])}

<div class="band">
  <div class="wrap">
    <h2>Talk to us about a build</h2>
    <div class="btns"><a class="btn" href="{ENQ_LS}">Email Langen</a><a class="btn" href="{STRIPE}">Reserve a build number</a></div>
  </div>
</div>

<section id="colour">
  <div class="wrap">
    {chapter("03","Specification")}
    <h2 class="section-title">Colour and finish.</h2>
    <p class="body">The standard Lightspeed is silver over a bronze chassis with champagne wheels. Bodywork, frame, wheels, seat and the anodised and machined parts are then specified individually with the design team, and if you want a finish we have not done before, we will develop it with you.</p>
    <div class="studies">
      <figure><img src="assets/ls_col_blue.jpg" alt="Lightspeed specification study: cobalt blue over black frame" loading="lazy"><figcaption><span>01</span>Cobalt over black frame</figcaption></figure>
      <figure><img src="assets/ls_col_greenfade.jpg" alt="Lightspeed specification study: racing green fade" loading="lazy"><figcaption><span>02</span>Racing green fade</figcaption></figure>
      <figure><img src="assets/ls_col_purple.jpg" alt="Lightspeed specification study: imperial purple with bronze frame" loading="lazy"><figcaption><span>03</span>Imperial purple, bronze frame</figcaption></figure>
      <figure><img src="assets/ls_col_silver.jpg" alt="Lightspeed specification study: satin silver with wire-spoked wheels" loading="lazy"><figcaption><span>04</span>Satin silver, wire-spoked wheels</figcaption></figure>
      <figure><img src="assets/ls_col_greenbronze.jpg" alt="Lightspeed specification study: heritage green with bronze chassis" loading="lazy"><figcaption><span>05</span>Heritage green, bronze chassis</figcaption></figure>
      <figure><img src="assets/ls_purple_cobbles.jpg" alt="Supernova purple Lightspeed on wet cobbles" loading="lazy" style="object-position:50% 70%"><figcaption><span>06</span>Supernova purple – an owner's build</figcaption></figure>
    </div>
    <p class="note">Studies are visualisations prepared for owners during specification. Finishes are agreed in person at Langen.</p>
  </div>
</section>

<section class="bleed">
  <img class="bg" src="assets/ls_pub_side.jpg" alt="Lightspeed outside a Lancashire inn at dusk" style="object-position:50% 55%">
  <div class="veil"></div>
  <div class="wrap">
    <h2>Built to be ridden a long way.</h2>
    <p>A 790 mm seat, a 19-litre tank, cruise control, and touring options for owners who will cover distance. Standard gearing gives around 150 mph; we will gear it longer or shorter to suit how you ride.</p>
  </div>
</section>

<section class="light" id="commission">
  <div class="wrap">
    {chapter("04","The commission")}
    <h2 class="section-title">How a Lightspeed is commissioned.</h2>
    <p class="lede">Six steps, most of them at the workshop in Wigan. For overseas owners we do the same over a video call with the bike in front of us.</p>
    <div class="steps">
      <div class="step"><h3>Allocation</h3><p>A refundable {LS["deposit"]} deposit secures one of {LS["builds"]} numbered builds. It stays refundable until your specification is agreed, the sales agreement is signed and manufacturing begins.</p></div>
      <div class="step"><h3>Consultation</h3><p>A day at the workshop with the design engineers: see the bike, sit on it, see how it is built, and talk about yours.</p></div>
      <div class="step"><h3>Fitting</h3><p>Seat height and shape, bar height and sweep, footrest position, ride height and suspension, measured and set to you before the build starts.</p></div>
      <div class="step"><h3>Specification</h3><p>Paint, finishes, materials and hard parts, agreed with the designers and recorded in the sales agreement.</p></div>
      <div class="step"><h3>The build</h3><p>Built by hand by a small team, with parts made or machined locally. We send updates as it comes together, and you are welcome to visit.</p></div>
      <div class="step"><h3>Handover</h3><p>Handed over complete and set up to your fitting, with its certificate and build record, by the people who built it.</p></div>
    </div>
    <div class="btns" style="margin-top:40px"><a class="btn gold" href="commission.html">The commission in full</a><a class="tlink" href="{STRIPE}">Reserve a build number</a></div>
  </div>
</section>

<section id="worldwide">
  <div class="wrap">
    {chapter("05","Worldwide")}
    <h2 class="section-title">Fifty of the 185 will go to America.</h2>
    <p class="body">UK-specification Lightspeeds are delivering first, in build order. Fully homologated versions for the United States, Europe, Japan, the Middle East and Australasia follow through 2027.</p>
    <p class="body">US riders who would rather not wait can take an early UK-specification build and register it through the Montana route, as a number of Two Stroke owners have. We ship door to door by air, crated and insured; duty and local taxes are paid on arrival. Ask and we will put a landed figure together for your state.</p>
    <div class="own three">
      <div><h3>Numbered</h3><p>Each build is numbered, its specification recorded, its certificate issued in the owner's name.</p></div>
      <div><h3>Looked after</h3><p>The engineers who built it maintain it. Overseas owners appoint a workshop, which we equip with the documents, tools and a direct line to Wigan.</p></div>
      <div><h3>First refusal</h3><p>Future ultra-limited Langen editions are offered to Lightspeed owners and build-number holders before anyone else.</p></div>
    </div>
  </div>
</section>

<section class="light">
  <div class="wrap split rev">
    <div>
      <div class="kicker">By invitation</div>
      <h2 class="section-title">LS12 Lightspeed Turbo</h2>
      <p class="lede">Twelve turbocharged Lightspeeds, drawn from the 185. It will be the fastest motorcycle we build.</p>
      <p class="body">Offered first to Lightspeed build-number holders and Two Stroke owners. Owners will be invited to the reveal.</p>
    </div>
    <img src="assets/turbo_side.jpg" alt="LS12 Lightspeed Turbo, side profile" loading="lazy">
  </div>
</section>

<section id="technical">
  <div class="wrap">
    {chapter("06","In numbers")}
    <h2 class="section-title">Technical specification</h2>
    <div class="kpis"><div><b>1,190cc</b><span>Displacement</span></div><div><b>185 kg</b><span>Dry weight</span></div><div><b>185 hp</b><span>at 10,600 rpm</span></div><div><b>138 Nm</b><span>at 8,200 rpm</span></div></div>
    <div class="specs">
      <dl>
        <dt>Engine</dt><dd>Liquid-cooled 72º V-twin. Developed by Rotax, manufactured by Buell. Langen electronics</dd>
        <dt>Fuel supply</dt><dd>Langen EFI, two-port injectors. Twin Bosch 60 mm throttle bodies</dd>
        <dt>Bore x stroke</dt><dd>106 x 67.5 mm · 13.4:1 compression</dd>
        <dt>Gearbox</dt><dd>6-speed. Hydraulic wet slipper clutch. Renthal 520 chain</dd>
        <dt>Chassis</dt><dd>High tensile steel tubular space frame</dd>
        <dt>Front suspension</dt><dd>Öhlins FGRT 301 48 mm USD forks, superbike cartridge kit, 120 mm travel</dd>
        <dt>Rear suspension</dt><dd>Twin Öhlins 36 mm STX piggyback shocks, adjustable, 120 mm travel</dd>
      </dl>
      <dl>
        <dt>Front brakes</dt><dd>Twin 320 mm EBC floating discs, Langen / HEL 4-piston radial calipers</dd>
        <dt>Rear brake</dt><dd>265 mm EBC disc, Langen / HEL 2-piston caliper</dd>
        <dt>ABS</dt><dd>Continental 2-channel with cornering function</dd>
        <dt>Rider aids</dt><dd>Traction, wheelie, launch and cruise control – developed in house</dd>
        <dt>Wheels</dt><dd>Langen forged aluminium. 3.5 x 17" front, 8.0 x 17" rear</dd>
        <dt>Tyres</dt><dd>Pirelli Diablo Rosso III. 120/70-17 front, 240/45-17 rear</dd>
        <dt>Dash</dt><dd>CNC-machined, TFT touchscreen with switch-cube interface</dd>
        <dt>Seat · tank</dt><dd>790 mm · 19 litres. Full carbon fibre bodywork</dd>
      </dl>
    </div>
  </div>
</section>

{enquire_block("Reserve your build number", "The Lightspeed starts at " + LS['price_from'] + " plus VAT. A numbered build is reserved with a " + LS['deposit'] + " deposit, refundable until your specification session is complete, the sales agreement is signed and manufacturing begins. Tell us where you are and what you have in mind, and Christofer or one of the team will come back to you directly.")}
"""

# ------------------------------------------------------------------ TWO STROKE
TWOSTROKE = f"""
<section class="hero short" style="padding:0">
  <img class="bg" src="assets/ts_goodwood_hill.jpg" alt="Langen Two Stroke on the hill at the Goodwood Festival of Speed" fetchpriority="high" style="object-position:60% 45%">
  <div class="veil"></div>
  <div class="wrap">
    <div class="kicker">2019 – 2025 · One hundred built</div>
    <img class="mark" src="assets/2strokeWhite.svg" alt="Two Stroke" style="width:min(70%,360px)">
    <h1>Our first motorcycle.</h1>
    <div class="btns">
      <a class="btn gold" href="pre-owned.html">Currently offered</a>
      <a class="tlink" href="{ENQ_TS}">Register interest</a>
    </div>
  </div>
</section>
{subnav("Two Stroke",[("overview","Overview"),("engineering","Engineering"),("pre-owned","Changing hands"),("technical","Technical")])}
{numbers_band([("76","hp"),("120","kg"),("100","built"),("12,700","rpm")], 'A 249.5cc two-stroke V-twin developed in Maranello, in a 120 kg motorcycle. One hundred were built between 2019 and 2025, and all of them were sold.')}

<section class="light" id="overview">
  <div class="wrap split">
    <div>
      {chapter("01","The idea")}
      <h2 class="section-title">Where Langen started.</h2>
      <p class="lede">The Two Stroke was the first bike we built: a road-legal two-stroke with an aluminium space frame, carbon bodywork and a weight of 120 kg, designed and built by a small team in Wigan to a standard we would put against anything from a large factory.</p>
      <p class="body">Öhlins and K-Tech suspension, HEL brakes, and an engine developed with Vins Motors in Maranello running Langen's own patented injection. Every one of the hundred was specified by its owner, and we know each of them by number.</p>
      <blockquote>“Build quality is spectacular… the whole package is a triumph of handling prowess.”<footer><a href="https://www.motorcyclenews.com/bike-reviews/langen/two-stroke/2022/">Motorcycle News</a></footer></blockquote>
    </div>
    <img src="assets/ts_studio.jpg" alt="Langen Two Stroke, side profile, studio" loading="lazy">
  </div>
</section>

<section id="engineering">
  <div class="wrap">
    {chapter("02","What it is made of")}
    <h2 class="section-title">The engineering.</h2>
    {anno([
      ("Vins Motors V-twin","249.5cc two-stroke","90º two-stroke twin, developed in Maranello, with Langen's patented electronic injection. 76 hp, 45 Nm, a power band from 9,500 rpm.","assets/ts_macro_engine.jpg"),
      ("120 kilograms","Aluminium and carbon","7020-T6 aluminium space frame, carbon fibre tank and bodywork, spoked tubeless rims. Over 600 bhp per tonne.","assets/ts_macro_hub.jpg"),
      ("Öhlins and K-Tech","Made for us","Öhlins 43 mm forks, fully adjustable. Twin K-Tech Razor piggyback shocks, made for us, with length adjustment.","assets/ts_shock.jpg"),
      ("Billet parts","Machined from solid","Billet yokes, levers and lamp bezels. Brembo Serie Oro discs with HEL billet calipers.","assets/ts_macro_lever.jpg"),
      ("One instrument","Carbon surround","A single round instrument in a carbon surround, electric start and LED lighting.","assets/ts_speedo.jpg"),
      ("Owner specified","Paint, seat, finishes","Paint, finishes, seat and hard parts were chosen by each owner, so no two of the hundred are the same.","assets/ts_macro_tank.jpg"),
    ])}
  </div>
</section>

{strip(("","In detail"),"Close up.",[
  ("assets/ts_seat_14.jpg","Two Stroke number 14 in yellow with a quilted seat","Number 14.","Yellow over carbon, quilted seat, white frame.","50% 50%"),
  ("assets/ts_yokes_gold.jpg","Two Stroke gold-anodised yokes and instrument","Billet yokes.","Machined top yoke, gold anodised, single round dial.","50% 50%"),
  ("assets/ts_lamp_gold.jpg","Two Stroke headlamp with gold bezel","The lamp.","Machined bezel, LED lamp, carbon surround.","50% 50%"),
  ("assets/ts_macro_seat.jpg","Two Stroke leather seat with Langen stitching","The seat.","Leather or Alcantara, stitched by hand, embroidered with the script.","50% 50%"),
  ("assets/ts_purple_tank.jpg","Two Stroke in metallic purple","Metallic purple.","Paint, finishes and hard parts were chosen by each owner.","50% 50%"),
  ("assets/ts_carbon_script.jpg","Carbon exhaust shroud with the Langen script","Carbon shroud.","Laid by hand and finished in gloss, with the script set into the weave.","50% 50%"),
  ("assets/ts_wheel_gold.jpg","Two Stroke gold forged wheel and brake","Gold wheel.","Dymag forged wheels on some owners' builds; wire-spoked on the signature specification.","50% 50%"),
  ("assets/ts_seat_leather.jpg","Two Stroke brown leather seat","Brown leather.","Leather and stitching chosen by the owner.","50% 50%"),
])}

<section class="light" id="pre-owned">
  <div class="wrap split">
    <div>
      {chapter("03","Changing hands")}
      <h2 class="section-title">When one comes back.</h2>
      <p class="lede">When an owner sells, the bike comes back through the factory. We inspect it, prepare it, issue a new certificate and offer it first to the people who have registered interest.</p>
      <div class="btns" style="margin-top:24px"><a class="btn gold" href="pre-owned.html">Currently offered</a><a class="tlink" href="{ENQ_TS}">Register interest</a></div>
    </div>
    <img src="assets/ts_tank_top.jpg" alt="Two Stroke 024 bespoke paint" loading="lazy">
  </div>
</section>

<section class="bleed">
  <img class="bg" src="assets/ts_ride_green2.jpg" alt="Two Stroke at speed on a country road" style="object-position:55% 50%">
  <div class="veil"></div>
  <div class="wrap">
    <h2>Still ridden.</h2>
    <p>Two Strokes have run at Goodwood, Silverstone and the Three Sisters, and the hundred are ridden on three continents.</p>
  </div>
</section>

<section id="technical">
  <div class="wrap">
    {chapter("04","In numbers")}
    <h2 class="section-title">Technical specification</h2>
    <div class="kpis"><div><b>249.5cc</b><span>Displacement</span></div><div><b>120 kg</b><span>Weight</span></div><div><b>76 hp</b><span>Power</span></div><div><b>45 Nm</b><span>Torque</span></div></div>
    <div class="specs">
      <dl>
        <dt>Engine</dt><dd>90º V-twin, two-stroke. Developed with Vins Motors, Maranello</dd>
        <dt>Fuel supply</dt><dd>Langen patented electronic injection</dd>
        <dt>Power band</dt><dd>9,500 – 11,700 rpm · redline 12,700 rpm</dd>
        <dt>Gearbox</dt><dd>6-speed, extractable cassette. Multi-disc wet clutch</dd>
        <dt>Chassis</dt><dd>7020-T6 aluminium space frame</dd>
        <dt>Bodywork</dt><dd>Carbon fibre fuel tank and bodywork</dd>
      </dl>
      <dl>
        <dt>Front suspension</dt><dd>Öhlins 43 mm forks – compression, rebound and preload adjustable</dd>
        <dt>Rear suspension</dt><dd>Twin bespoke K-Tech Razor piggyback shocks – damping, preload and length adjustable</dd>
        <dt>Front brakes</dt><dd>Twin 320 mm Brembo Serie Oro discs, HEL radial billet calipers</dd>
        <dt>Rear brake</dt><dd>265 mm Brembo Serie Oro disc, HEL billet caliper</dd>
        <dt>Wheels · tyres</dt><dd>Spoked tubeless rims. Dunlop TT100 GP Radial, 120/70-17 and 150/70-17</dd>
        <dt>Electrics</dt><dd>Electric start, LED lighting</dd>
      </dl>
    </div>
  </div>
</section>

{enquire_block("Register your interest", "Tell us what you are looking for and where you are. When a Two Stroke that fits comes back to the factory, Christofer or one of the team will contact you before it is offered more widely.", ENQ_TS, "Register interest", secondary=False, pdf=False)}
"""

# ------------------------------------------------------------------ PRE-OWNED
def cpo_cards():
    out=[]
    for b in PREOWNED_BIKES:
        if b.get("status") == "sold": continue
        lis="".join(f"<li>{f}</li>" for f in b["highlights"])
        badge = ' · Reserved' if b.get("status") == "reserved" else ''
        out.append(f'<a class="card" href="{b["brochure"]}"><img src="{b["image"]}" alt="Langen {b["model"]} {b["number"]}" loading="lazy"><div class="txt"><span class="meta">{b["model"]} No. {b["number"]} · {b.get("meta","")}{badge}</span><h3>{b["title"]}</h3><div class="price">{b["price"]}</div><ul>{lis}</ul><span class="cta">View the brochure</span></div></a>')
    if not out:
        out.append('<p class="body">Nothing is offered at the moment. Register your interest and you will hear first when one comes back.</p>')
    return "".join(out)

PREOWNED = f"""
<section class="hero short" style="padding:0">
  <img class="bg" src="assets/ts_track.jpg" alt="Langen Two Stroke on an empty circuit" fetchpriority="high" style="object-position:62% 42%">
  <div class="veil"></div>
  <div class="wrap">
    <div class="kicker">Certified Pre-Owned</div>
    <h1>Two Strokes offered through the factory.</h1>
    <p>We know every Two Stroke by number. When an owner sells, the bike comes back to the workshop that built it, and we offer it to the next owner ourselves.</p>
    <div class="btns"><a class="btn gold" href="#available">Currently offered</a><a class="tlink" href="{ENQ_TS}">Register interest</a></div>
  </div>
</section>

<section class="light">
  <div class="wrap split">
    <div>
      {chapter("01","The record")}
      <h2 class="section-title">The record stays with the bike.</h2>
      <p class="lede">Each Langen has a build number, a recorded specification and the name of the person it was built for. Selling it through the factory keeps that record complete.</p>
      <p class="body">Before a bike is offered, the engineers who built it check its history, inspect it and prepare it to the standard it left with. It gets a new Certificate of Ownership in the new owner's name, and the new owner gets what a first owner has: direct support from the factory, the owners' portal and first refusal on future editions.</p>
      <p class="body">If you want to, the design team can change colours, finishes and contact points before handover.</p>
    </div>
    <img src="assets/ts_studio.jpg" alt="Langen Two Stroke, side profile, studio" loading="lazy">
  </div>
</section>

<section id="available">
  <div class="wrap">
    {chapter("02","Currently offered")}
    <h2 class="section-title">Motorcycles available through the factory.</h2>
    <p class="body">Each listing opens the brochure we prepared for that bike, with its specification, history and condition. Interest is taken in order, and a bike is usually sold within days of being offered.</p>
    <div class="cpo">{cpo_cards()}</div>
    <p class="note" style="margin-top:22px">From time to time a build allocation is released by a client unable to proceed. These are offered from {TS["slot_price"]} plus VAT and are completed to the new owner's specification. Register your interest and you will hear first.</p>
  </div>
</section>

<section class="light">
  <div class="wrap">
    {chapter("03","What accompanies it")}
    <h2 class="section-title">What comes with a motorcycle from the factory.</h2>
    <div class="own three">
      <div><h3>Verified history</h3><p>Ownership, servicing and provenance confirmed against our own records and external data partners, and supplied with the bike.</p></div>
      <div><h3>Factory preparation</h3><p>Over forty mechanical, electrical, cosmetic and documentation checks, a full test ride, and sign-off by a Langen technician.</p></div>
      <div><h3>Warranty and support</h3><p>A minimum twelve-month warranty from Langen, and the same direct line to the engineers that a new build receives.</p></div>
      <div><h3>Certificate of Ownership</h3><p>A new factory-issued certificate in your name, recording the motorcycle's number and specification.</p></div>
      <div><h3>Changes before handover</h3><p>Colours, finishes and contact points can be changed with the design team before handover.</p></div>
      <div><h3>Delivery worldwide</h3><p>Pre-owned bikes carry no VAT in the UK or US. We arrange delivery door to door, crated and insured; local taxes and duty are paid on arrival.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap split rev">
    <div>
      {chapter("04","Passing yours on")}
      <h2 class="section-title">Selling your Langen.</h2>
      <p class="lede">If you decide to sell, talk to us first. We know the bike, we know who is waiting for one, and selling through the factory keeps the record and the value intact.</p>
      <div class="btns" style="margin-top:24px"><a class="btn gold" href="{enq("Passing on my Langen", "Hi Langen,\\n\\nI am thinking of passing on my Langen.\\n\\nName:\\nModel and build number:\\nMileage and condition:\\n")}">Talk to us</a></div>
    </div>
    <img src="assets/ts_ride_lane.jpg" alt="Two Stroke on a country lane" loading="lazy" style="object-position:50% 50%">
  </div>
</section>

{enquire_block("Register your interest", "Tell us what you are looking for and where you are. When a bike that fits comes back to the factory, Christofer or one of the team will contact you before it is offered more widely.", ENQ_TS, "Register interest", secondary=False, pdf=False)}
"""

# ------------------------------------------------------------------ COMMISSION
COMMISSION = f"""
<section class="hero short" style="padding:0">
  <img class="bg" src="assets/ts_build_frame.jpg" alt="A Langen engineer holding a Two Stroke chassis aloft in the workshop" fetchpriority="high" style="object-position:40% 40%">
  <div class="veil"></div>
  <div class="wrap">
    <div class="kicker">Commissioning a Langen</div>
    <h1>How a Langen is commissioned.</h1>
    <p>A refundable deposit, a day at the workshop, a fitting, a specification, the build and the handover. Owners tell us the day at the workshop is one of the best parts, so we take our time over it.</p>
  </div>
</section>

<section class="light">
  <div class="wrap">
    {chapter("01","Six steps")}
    <h2 class="section-title">From deposit to handover.</h2>
    <p class="lede">From a refundable deposit to the day you ride it away. Most of it happens in person, in Wigan; for overseas owners we do the same over a video call with the bike in front of us.</p>
    <div class="steps">
      <div class="step"><h3>Allocation</h3><p>A refundable {LS["deposit"]} deposit secures a numbered build. It stays refundable until your specification is agreed, the sales agreement is signed and manufacturing begins. <a href="#" class="terms-link">Deposit terms</a>.</p></div>
      <div class="step"><h3>Consultation</h3><p>A day at the workshop with the design engineers. You see the bike, sit on it, see how it is built, and we talk about what you want from yours.</p></div>
      <div class="step"><h3>Fitting</h3><p>Seat height and shape, bar height and sweep, footrest position, ride height and suspension set-up, measured and set to you before the build starts.</p></div>
      <div class="step"><h3>Specification</h3><p>Paint, exposed carbon or a mix. Frame, swingarm and wheel colours. Seat material and stitching. Machined and anodised hardware. Wheels, exhaust, suspension pack. A visual is prepared and a sales agreement drawn up.</p></div>
      <div class="step"><h3>The build</h3><p>Built by hand by a small team, with parts made or machined locally. You receive updates as it comes together, and you are welcome to visit.</p></div>
      <div class="step"><h3>Handover</h3><p>Handed over complete and set up to your fitting, with its certificate and build record, by the people who built it. Delivered to you, or collected from Wigan.</p></div>
    </div>
  </div>
</section>

<section class="bleed">
  <img class="bg" src="assets/ts_seat_leather.jpg" alt="A brown leather Langen seat, embroidered, on a carbon tail" style="object-position:50% 50%">
  <div class="veil"></div>
  <div class="wrap">
    <h2>Parts we have not made yet.</h2>
    <p>There is no fixed options list. Most owners choose from the finishes and hard parts we already make. If you need something we have not made before, such as a thumb brake, a different footrest hanger or a seat built to a measurement, we design it into the bike during the build.</p>
  </div>
</section>

<section>
  <div class="wrap">
    {chapter("02","What it costs")}
    <h2 class="section-title">The price.</h2>
    <p class="body">A standard Lightspeed is {LS["price_from"]} plus VAT: silver over a bronze chassis with champagne wheels, complete and ready to ride. The final figure depends on how far you take the specification. A heavily specified bike, with full custom paint, the K-Tech suspension pack, upgraded wheels and bespoke finishes throughout, can reach {LS["price_heavily_specified"]}; most builds land between the two. The {LS["deposit"]} deposit comes off the price.</p>
    <div class="own three">
      <div><h3>United Kingdom</h3><p>Registered under the Individual Vehicle Approval scheme as an individual commission. UK builds deliver first, in build order.</p></div>
      <div><h3>United States</h3><p>Fully homologated Lightspeeds deliver from late 2027; fifty of the 185 are allocated to the US. Earlier UK-specification builds can be registered through the Montana route. Export prices are without UK VAT; air freight door to door, crated and insured, is typically around £3,000, with duty and state taxes paid on arrival.</p></div>
      <div><h3>Rest of the world</h3><p>Homologated versions for Europe, Japan, the Middle East and Australasia follow in 2027. Collectors not intending road use can take an early UK-specification build anywhere. Ask for a landed figure for your country.</p></div>
    </div>
  </div>
</section>

<section class="light">
  <div class="wrap">
    {chapter("03","Afterwards")}
    <h2 class="section-title">Owning one.</h2>
    <div class="own three">
      <div><h3>Direct to the factory</h3><p>There is no dealer. The engineers who built your motorcycle look after it, and you have Christofer's number.</p></div>
      <div><h3>Overseas support</h3><p>Overseas owners appoint a workshop of their choice; we furnish it with the internal documents, tools and a direct line to the people who designed and built the bike.</p></div>
      <div><h3>Owners' portal</h3><p>Documentation, build updates and the record for your motorcycle, in one place.</p></div>
      <div><h3>First refusal</h3><p>Future ultra-limited editions are offered to owners and build-number holders before anyone else.</p></div>
      <div><h3>Provenance</h3><p>Every build numbered, its specification recorded, a certificate issued. Certified Pre-Owned keeps that record intact when a bike changes hands.</p></div>
      <div><h3>Visits</h3><p>Owners are welcome at the workshop at any time, by appointment, with or without the bike.</p></div>
    </div>
  </div>
</section>

{enquire_block("Talk to us", "Tell us where you are and what you have in mind, and Christofer or one of the team will reply personally. If you would rather talk, send a time that suits and we will call you.")}
"""

# ------------------------------------------------------------------ ABOUT
ABOUT = f"""
<section class="hero short" style="padding:0">
  <img class="bg" src="assets/ts_news.jpg" alt="Langen Two Stroke in front of the We Do Things Differently Here wall at the workshop" fetchpriority="high" style="object-position:70% 50%">
  <div class="veil"></div>
  <div class="wrap">
    <div class="kicker">Langen Motorcycles · Wigan, England</div>
    <h1>Who we are.</h1>
    <p>Langen was founded in Wigan in 2018 by Christofer Ratcliffe to build light, hand-made motorcycles, one at a time, to order.</p>
  </div>
</section>

<section class="light">
  <div class="wrap split">
    <div>
      {chapter("01","The story")}
      <h2 class="section-title">The story so far.</h2>
      <p class="lede">Christofer Ratcliffe was Chief Design Engineer at CCM when he began drawing an ultra-lightweight road motorcycle of his own. In 2019 a partnership with Vincenzo Mattia's Vins Motors in Maranello gave it an engine, and Langen Motorcycles was born.</p>
      <p class="body">The Two Stroke followed: one hundred built, every one sold, now ridden on three continents. The team grew with it, with engineers and designers from CCM, Triumph, BAC, McLaren and M-Sport.</p>
      <p class="body">The Lightspeed, revealed at Gunhill Studios in November 2025, is the second model: 185 horsepower, 185 kilograms, 185 builds, with Langen's own electronics and the highest UK manufacturing content of any motorcycle maker. The LS12 Turbo – twelve of them – comes next.</p>
    </div>
    <img src="assets/team.jpg" alt="The Langen team with the first Lightspeed" loading="lazy" style="object-position:50% 50%">
  </div>
</section>

{LETTER.replace('class="light letter-wrap"','class="letter-wrap"')}

<section class="light">
  <div class="wrap">
    {chapter("02","How we work")}
    <h2 class="section-title">What happens here.</h2>
    <div class="steps three">
      <div class="step"><h3>Design</h3><p>Every component is drawn here and judged on weight, function and finish. Each one has to justify its place on the bike.</p></div>
      <div class="step"><h3>Engineering</h3><p>Chassis analysed with our own FEA tools, electronics and rider aids written in house, materials chosen on weight and strength.</p></div>
      <div class="step"><h3>Testing</h3><p>Dyno, road and track before anything is signed off, to procedures in line with the large manufacturers.</p></div>
      <div class="step"><h3>Making</h3><p>Chassis welded and bodywork laid up by local partners who also make for Formula 1 and aerospace. Billet parts are machined a few minutes from the workshop.</p></div>
      <div class="step"><h3>Commissioning</h3><p>Each bike is built to its owner's fit and specification, agreed with the design team in person.</p></div>
      <div class="step"><h3>Looking after it</h3><p>Owners deal with the factory directly, and the engineers who built the bike maintain it.</p></div>
    </div>
  </div>
</section>

<section class="bleed">
  <img class="bg" src="assets/awards.jpg" alt="The Langen team receiving the Highly Commended award at the Wigan Borough Business Awards 2026" style="object-position:50% 30%">
  <div class="veil"></div>
  <div class="wrap">
    <div class="kicker">Wigan Borough Business Awards 2026</div>
    <h2>Highly Commended, Small Business of the Year.</h2>
    <p>“The judges were particularly impressed by the ambition behind Langen Motorcycles and its determination to compete at the very highest level despite operating with a relatively small team… demonstrating that you don't have to be the biggest to compete on a global stage.”</p>
    <div class="btns" style="margin-top:22px"><a class="tlink" href="news-business-awards.html">Read more</a></div>
  </div>
</section>

<section class="light">
  <div class="wrap">
    {chapter("03","Where")}
    <div class="split">
      <div>
        <h2 class="section-title">Kingfisher Court, Wigan.</h2>
        <p class="lede">Beside the Three Sisters circuit, two minutes from junction 25 of the M6 and twenty from Manchester. The line on the workshop wall, “We do things differently here”, is Wigan's own, and we have taken it on.</p>
        <p class="body">Visits are by appointment and always welcome, whether you own one, are thinking about one, or just want to see a motorcycle being built by hand.</p>
        <div class="btns" style="margin-top:24px"><a class="btn gold" href="contact.html">Arrange a visit</a></div>
      </div>
      <img src="assets/workshop_wide2.jpg" alt="Inside the Langen workshop in Wigan" loading="lazy" style="object-position:50% 50%">
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    {chapter("04","In print")}
    <div class="quotes">
      <blockquote>“…excellent power-to-weight ratio, and the benchmark handling of its sweet-steering chassis. Langen Motorcycles’ debut model has hit the bullseye.”<footer>motorcycle.com</footer></blockquote>
      <blockquote>“Build quality is spectacular… the whole package is a triumph of handling prowess.”<footer><a href="https://www.motorcyclenews.com/bike-reviews/langen/two-stroke/2022/">Motorcycle News</a></footer></blockquote>
      <blockquote>“In the flesh it is just stunning.”<footer>Petrol Revolt</footer></blockquote>
      <blockquote>“The way it rides is incredible.”<footer>The Late Brake Show</footer></blockquote>
    </div>
  </div>
</section>

{enquire_block("Arrange a visit", "Tell us when suits and we will show you round the workshop and the bikes.", enq("Workshop visit", "Hi Langen,\\n\\nI'd like to arrange a visit to the workshop.\\n\\nName:\\nWhere I'm travelling from:\\nDates that suit:\\n"), "Arrange a visit")}
"""

# ------------------------------------------------------------------ NEWS (content/news/*.md)
NEWS_PAGE = f"""
<section class="page-head">
  <div class="wrap">
    <div class="kicker">News</div>
    <h1>From the workshop.</h1>
    <p class="lede">Reveals, events, awards and news from the workshop.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="news">{news_cards(NEWS)}</div>
    <p class="note" style="margin-top:30px">For press enquiries and image requests, see the <a href="owners.html#press" style="color:#fff">press page</a>.</p>
  </div>
</section>
{enquire_block("Stay in touch", "If you would like to hear from us as the first Lightspeeds are delivered, send us your email address and we will keep you informed.", enq("Keep me informed", "Hi Langen,\\n\\nPlease keep me informed about Langen news and the Lightspeed.\\n\\nName:\\nCountry:\\n"), "Keep me informed", secondary=False, pdf=False)}
"""

def article_page(it):
    body = it["body_html"] or f"<p>{it['summary']}</p>"
    return f"""
<section class="page-head">
  <div class="wrap">
    <div class="kicker">News · {it["date_long"]}</div>
    <h1>{it["title"]}</h1>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    {f'<img src="{it["image"]}" alt="{it["image_alt"]}" style="margin-bottom:34px">' if it["image"] else ''}
    <div class="article">{body}</div>
    <div class="btns" style="margin-top:34px"><a class="tlink" href="news.html">All news</a></div>
  </div>
</section>
{enquire_block()}
"""

# ------------------------------------------------------------------ CONTACT
FAQ = [
 (f"What makes a Langen different?",f"Each one is built to order for one rider. Your riding position, geometry and suspension are set to you before the build starts, and paint, finishes and the machined details are chosen with the design team who will make them. The engineers who build your bike also look after it; there is no dealer."),
 (f"How limited are they?",f"The Two Stroke was a run of 100, now sold out. The Lightspeed is limited to {LS["builds"]} builds worldwide, each numbered, with {LS["us_allocation"]} allocated to the United States. The LS12 Turbo will be twelve."),
 (f"What does a Lightspeed cost?",f"From {LS["price_from"]} plus VAT for a complete, finished motorcycle. The final figure depends on your specification; a heavily specified bike can reach {LS["price_heavily_specified"]}. Export builds are priced without UK VAT, plus shipping, duty and local taxes."),
 (f"How do I reserve one?",f"A {LS["deposit"]} deposit reserves a numbered build. It is fully refundable until your specification session is complete, the sales agreement is signed and manufacturing begins, and it comes off the price of the bike."),
 (f"Can I have one outside the UK?",f"Yes. UK-specification builds deliver first; fully homologated versions for the USA, Europe, Japan, the Middle East and Australasia follow through 2027. US owners can take an early UK-specification bike through the Montana route. We arrange air freight door to door, crated and insured; clearance and duty are paid on arrival."),
 (f"How far can I customise it?",f"As far as you like. Colours, finishes, seat, wheels, exhaust and suspension are specified with the design team, and if you need a part we have not made before, such as a thumb brake or a different footrest hanger, we design it into the bike during the build."),
 (f"Can I visit?",f"Please do. The workshop is at Kingfisher Court, Wigan, next to the Three Sisters circuit. Visits are by appointment; email or call and we will find a time."),
 (f"Is the Two Stroke still available?",f"New builds are closed. When an owner passes one on it comes back through the factory, inspected, certified and warranted, and is offered to the people who have registered interest first."),
]
CONTACT = f"""
<section class="page-head">
  <div class="wrap">
    <div class="kicker">Contact</div>
    <h1>Email, call, or come and see us.</h1>
    <p class="lede">Every enquiry is answered personally by Christofer or one of the team. Tell us where you are and what you have in mind.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="contact-form">{enquiry_form("contact-form-el", "Enquiry", "lightspeed")}</div>
  </div>
</section>
<section class="light" style="padding-top:64px">
  <div class="wrap">
    <div class="own three">
      <div><h3>Lightspeed</h3><p>Commissioning a build, reserving a number, colours, fit, timing and export.</p><div class="btns" style="margin-top:14px"><a class="btn ghost" href="{ENQ_LS}">Enquire</a></div></div>
      <div><h3>Two Stroke</h3><p>Register interest in a Certified Pre-Owned Two Stroke or a released build allocation.</p><div class="btns" style="margin-top:14px"><a class="btn ghost" href="{ENQ_TS}">Register interest</a></div></div>
      <div><h3>Anything else</h3><p>Owners, press, partners, suppliers, careers, or a visit to the workshop.</p><div class="btns" style="margin-top:14px"><a class="btn ghost" href="{ENQ_GEN}">Email us</a></div></div>
    </div>
  </div>
</section>
<section class="light" style="padding-top:0">
  <div class="wrap split">
    <div>
      <h2 class="section-title">Find us.</h2>
      <p class="lede">Langen Motorcycles<br>Unit 1, Kingfisher Court<br>South Lancs Industrial Estate<br>Wigan, Greater Manchester WN4 9DW<br>United Kingdom</p>
      <p class="body" style="margin-top:18px"><a href="tel:{TEL}" style="color:var(--ink);text-decoration:none;font-family:'Barlow Condensed';font-weight:700;font-size:24px">{TELFMT}</a><br><a href="mailto:{MAIL}" style="color:var(--ink);text-decoration:none;font-family:'Barlow Condensed';font-weight:700;font-size:24px">{MAIL}</a></p>
      <p class="body" style="margin-top:18px">Beside the Three Sisters circuit, two minutes from junction 25 of the M6 and twenty from Manchester. Visits by appointment.</p>
    </div>
    <img src="assets/ls_pub_lamp.jpg" alt="Lightspeed headlamp outside a Lancashire inn" loading="lazy" style="object-position:50% 50%">
  </div>
</section>
<section id="faq">
  <div class="wrap">
    <h2 class="section-title">Common questions.</h2>
    <div class="faq">{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in FAQ)}</div>
  </div>
</section>
{enquire_block()}
"""

# ------------------------------------------------------------------ CAREERS
CAREERS = f"""
<section class="page-head">
  <div class="wrap">
    <div class="kicker">Careers</div>
    <h1>Working at Langen.</h1>
    <p class="lede">We are a small team in Wigan, with people who came from CCM, Triumph, BAC, McLaren and M-Sport, building motorcycles by hand to order. The roles we are hiring for are below.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="own three">
      <div><h3>What we are for</h3><p>Motorcycles that move the soul: technical performance and the purity of the ride in one machine.</p></div>
      <div><h3>How we behave</h3><p>Honesty, integrity, inclusiveness, innovation, quality, openness, creativity, and fun.</p></div>
      <div><h3>What we expect</h3><p>That you question the norm, own your work, and care about the rider at the end of it.</p></div>
    </div>
    <h2 class="section-title" style="margin-top:60px">Open roles</h2>
    <div class="roles">
      <div class="role"><div><h3>Lead Technician</h3><div class="meta">Wigan · Full-time</div><p>An experienced, proactive technician for a fast-moving workshop: assembly and development work, primarily but not only on motorcycles. Best suited to someone with high-level workshop experience at an OEM or dealership.</p></div><a class="btn ghost" href="{enq("Application – Lead Technician")}">Apply</a></div>
      <div class="role"><div><h3>Automotive Design Engineer</h3><div class="meta">Wigan · Full-time</div><p>Design and development across the whole motorcycle, from chassis to machined detail. Experience designing to a high standard in the automotive industry; all levels considered for the right person.</p></div><a class="btn ghost" href="{enq("Application – Automotive Design Engineer")}">Apply</a></div>
      <div class="role"><div><h3>Customer Development Specialist</h3><div class="meta">Wigan · Full-time</div><p>Building and keeping owner relationships, from first enquiry to handover and beyond. Proactive, adaptable, and good with people who care about details.</p></div><a class="btn ghost" href="{enq("Application – Customer Development Specialist")}">Apply</a></div>
    </div>
    <p class="note" style="margin-top:26px">If none of these fit, we are still interested in hearing from engineers, technicians and makers. Send a CV and a few lines about what you would bring.</p>
  </div>
</section>
{enquire_block("Introduce yourself", "Send a CV and a few lines about what you ride, what you've built and why Langen.", enq("Careers – introduction"), "Email the team", secondary=False, pdf=False)}
"""

# ------------------------------------------------------------------ PRIVACY
PRIVACY = f"""
<section class="page-head">
  <div class="wrap"><div class="kicker">Legal</div><h1>Privacy policy</h1></div>
</section>
<section style="padding-top:0">
  <div class="wrap"><div class="article">
    <h2>The personal information we collect and use</h2>
    <p><b>Information you provide to us.</b> Name, address, telephone number, email address and, when you make a purchase, payment details (processed by our payment provider; we do not store card numbers). We collect this when you enquire, reserve a build, make a purchase, register for the owners' portal or sign up to news.</p>
    <p><b>Information you provide about third parties.</b> If you give us information about another person, you confirm they have appointed you to act on their behalf and agreed that you may consent to the processing of their personal data, receive data-protection notices on their behalf and consent to the transfer of their data abroad.</p>
    <h2>How we use it</h2>
    <p>To answer your enquiry, process your reservation or order and send related information, to give you access to the owners' portal, and – if you have opted in – to send occasional news about Langen. You can opt out of marketing at any time by replying to any message or emailing {MAIL}.</p>
    <h2>Who it may be shared with</h2>
    <p>Our payment provider, our shipping partners where a motorcycle is being delivered, and law-enforcement agencies in connection with any investigation to help prevent unlawful activity. We do not sell or share your personal information with any other third party.</p>
    <h2>Analytics and cookies</h2>
    <p>This site uses analytics to understand how it is read. No analytics cookies are set until you accept them in the notice at the foot of the page, and no advertising cookies are set. The owners' portal sets a single cookie to keep you signed in. Declining analytics has no effect on your use of the site.</p>
    <h2>How long we keep it</h2>
    <p>Six years from your last contact with us, or longer where required by law in connection with a purchase. Owner records are kept for the life of the motorcycle.</p>
    <h2>Keeping it secure</h2>
    <p>We have appropriate security measures in place to prevent personal information being lost, used or accessed in an unauthorised way. Access is limited to those with a genuine business need, and all data is encrypted in transit. No transfer over the internet is entirely secure; if you have particular concerns, contact us using the details below.</p>
    <h2>Your rights</h2>
    <p>Under UK data protection law you have rights to access, correct, erase and restrict the processing of your personal information, to object to direct marketing, to data portability and to complain to the Information Commissioner's Office (ico.org.uk). To exercise any of them, email {MAIL} or write to Langen Technology Ltd, Unit 1, Kingfisher Court, Wigan WN4 9DW.</p>
    <p class="note">Langen Technology Ltd, registered in England &amp; Wales no. 11601010, trading as Langen Motorcycles. Last updated October 2026.</p>
  </div></div>
</section>
"""

PAGES = {
 "index.html":      ("Langen Motorcycles – hand-built in Wigan, England","Langen builds motorcycles to order for one rider at a time, in Wigan, England. The Lightspeed: 185 hp, 185 kg, 185 builds. The Two Stroke: 100 built.","index.html","assets/ls_front_bokeh.jpg",HOME,None),
 "lightspeed.html": ("Langen Lightspeed – 185 hp, 185 kg, one of 185","The Langen Lightspeed: a 1,190cc V-twin, 185 hp, 185 kg, limited to 185 commissioned builds. From £37,000 plus VAT. Reserve a numbered build with a refundable £1,000 deposit.","lightspeed.html","assets/ls_og.jpg",LIGHTSPEED,"lightspeed.html"),
 "two-stroke.html": ("Langen Two Stroke – one hundred built","The Langen Two Stroke: 249.5cc two-stroke V-twin by Vins Motors, 76 hp, 120 kg, 100 built. Occasionally one comes back through the factory.","two-stroke.html","assets/ts_goodwood_hill.jpg",TWOSTROKE,"two-stroke.html"),
 "pre-owned.html":  ("Certified Pre-Owned – Langen Motorcycles","One hundred Two Strokes were built. When one changes hands, it does so through the factory that made it, with its record and provenance intact.","pre-owned.html","assets/ts_track.jpg",PREOWNED,"pre-owned.html"),
 "commission.html": ("Commissioning a Langen","How a Langen is commissioned: a refundable deposit, a day with the design engineers, fitting, specification, the build and handover. What it costs and how it reaches you worldwide.","commission.html","assets/ts_build_frame.jpg",COMMISSION,"commission.html"),
 "about.html":      ("About Langen Motorcycles – engineers first","Founded in 2018 in Wigan by Christofer Ratcliffe, with a team from CCM, Triumph, BAC, McLaren and M-Sport. Hand-built motorcycles with the highest UK manufacturing content of any motorcycle maker.","about.html","assets/ts_news.jpg",ABOUT,"about.html"),
 "news.html":       ("News – Langen Motorcycles","Reveals, events and awards from Langen Motorcycles.","news.html","assets/awards.jpg",NEWS_PAGE,"news.html"),
 "contact.html":    ("Contact Langen Motorcycles","Email, call or visit the workshop in Wigan. Every enquiry is answered personally.","contact.html","assets/ls_exhaust.jpg",CONTACT,"contact.html"),
 "careers.html":    ("Careers – Langen Motorcycles","Open roles at Langen Motorcycles in Wigan: Lead Technician, Automotive Design Engineer, Customer Development Specialist.","careers.html","assets/workshop2.jpg",CAREERS,None),
 "owners.html":     ("Owners' portal – Langen Motorcycles","Sign in to the Langen owners' portal for the build record, documents and videos for your motorcycle.","owners.html","assets/ls_og.jpg",OWNERS_PORTAL,None),
 "privacy.html":    ("Privacy policy – Langen Motorcycles","How Langen Technology Ltd collects and uses personal information.","privacy.html","assets/ls_og.jpg",PRIVACY,None),
}
