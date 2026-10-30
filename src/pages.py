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
    <p>I spent the first part of my career designing motorcycles for other people's badges. The brief was always the same: a bike for everyone, which is to say a bike for no one in particular. Langen began as the opposite idea – that a motorcycle could be made for one rider, by people who would know that rider by name, and that it should be light enough and alive enough to make a Tuesday evening feel like a holiday.</p>
    <p>We are a small company in Wigan. We keep it that way on purpose. Every bike we build goes through the same hands, and every owner has my number. If you commission one, you will spend a day with us before anything is cut, and you will know exactly who made it and why each part is the way it is.</p>
    <p>Everything on a Langen is there because it has to be. Nothing is there because the brochure needed it.</p>
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
    <h2>We don't believe a motorcycle can be made for more than one person. So we don't try.</h2>
  </div>
</section>

<div class="models">
  <a class="model" href="lightspeed.html">
    <img src="assets/ls_pub_front.jpg" alt="Langen Lightspeed outside a black-and-white Lancashire inn" loading="lazy" style="object-position:40% 50%">
    <div class="veil"></div>
    <div class="txt"><img src="assets/ls_white.png" alt="Lightspeed"><p>185 horsepower. 185 kilograms. One of 185.</p><span class="cta">Explore</span></div>
  </a>
  <a class="model" href="two-stroke.html">
    <img src="assets/ts_ride_green.jpg" alt="Langen Two Stroke ridden hard on a Lancashire lane" loading="lazy" style="object-position:45% 50%">
    <div class="veil"></div>
    <div class="txt"><img class="ts" src="assets/2strokeWhite.svg" alt="Two Stroke"><p>The one that started it. One hundred built.</p><span class="cta">Explore</span></div>
  </a>
</div>

<section class="light">
  <div class="wrap split">
    <div>
      {chapter("01","The idea")}
      <h2 class="section-title">It begins with the rider, not the bike.</h2>
      <p class="lede">Each Langen starts with the person who will ride it: height, reach, how and where they ride. Position, geometry and suspension are set to them. Then paint, finishes and the machined details are chosen with the engineers who will make them. The bike that leaves Wigan fits one person, and it is theirs in every sense.</p>
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
    <h2>One workshop. You will know their names.</h2>
    <p>Engineers and designers who came from CCM, Triumph, BAC, McLaren and M-Sport to build the motorcycles the big factories can't. There is no dealer in between: the person who welds your chassis is the person who answers the phone when you call about it.</p>
    <div class="btns" style="margin-top:26px"><a class="tlink" href="about.html">About Langen</a></div>
  </div>
</section>

<section class="pull">
  <div class="wrap">
    <blockquote class="big">Everything on a Langen is there because it has to be. Nothing is there because the brochure needed it.<footer><a class="tlink" href="about.html">Christofer Ratcliffe, founder</a></footer></blockquote>
  </div>
</section>

<section class="carbon">
  <div class="wrap split wide">
    <div>
      {chapter("03","The ride")}
      <h2 class="section-title">Light enough to feel. Fast enough to matter.</h2>
      <p class="lede">A Langen weighs what a motorcycle weighed before motorcycles got heavy. The Two Stroke is 120 kg; the Lightspeed, with 185 horsepower, is 185. That is not a specification so much as a point of view: that the pleasure of riding is in how a bike moves beneath you, not in what it does on paper.</p>
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

{enquire_block("Begin a conversation", "Every Langen starts with a conversation, usually with Christofer. Tell us where you are and what you have in mind – a colour, a fit, a road you want it for – and we will come back to you personally.")}
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
    <h1>Built for its owner. Alive on any road.</h1>
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
      <h2 class="section-title">A hyper-naked with manners.</h2>
      <p class="lede">The Lightspeed has the agility of a hyper-naked, components from the superbike paddock, the torque of a drag bike and a seat you can sit in all day. Its silhouette is what stops people in the street. What keeps them there is the engineering they find up close.</p>
      <blockquote>Each Lightspeed has the character of a Langen and the character of the person it was built for. We believe it is impossible to make a motorcycle for more than one rider, so we don't.<footer>Christofer Ratcliffe, founder</footer></blockquote>
    </div>
    <img class="sq" src="assets/ls_studio_grey.jpg" alt="Lightspeed, front three-quarter, studio" loading="lazy" style="object-position:50% 55%">
  </div>
</section>

<section class="bleed">
  <img class="bg" src="assets/ls_macro_engine.jpg" alt="Lightspeed engine cover with the LS mark, carbon and titanium around it" style="object-position:50% 50%">
  <div class="veil"></div>
  <div class="wrap">
    <h2>Nothing is covered up.</h2>
    <p>The engine is on show because we are proud of it. The chassis is on show because it is beautiful. Carbon laid by hand, steel welded by people who weld for Formula 1, billet turned minutes from the factory door – all of it where you can see it.</p>
  </div>
</section>

<section id="engineering">
  <div class="wrap">
    {chapter("02","What it is made of")}
    <h2 class="section-title">Every part chosen, or made, by us.</h2>
    {anno([
      ("The engine","1,190cc V-twin","Liquid-cooled 72º V-twin, developed by Rotax and built by Buell, running Langen's own injection and electronics. 185 hp, 138 Nm, and a mid-range that pulls rather than waits.","assets/ls_macro_engine_exhaust.jpg"),
      ("185 kilograms","Carbon and forged aluminium","Full carbon bodywork and Langen forged, CNC-machined wheels. Over 1,000 bhp per tonne – a figure from the race paddock, on a bike with a 19-litre tank.","assets/ls_macro_sprocket.jpg"),
      ("Öhlins at both ends","Set to you","FGRT 301 48 mm forks with a superbike cartridge kit; twin STX piggyback shocks behind. Set to you at your fitting. K-Tech Racing pack available.","assets/ls_macro_shock.jpg"),
      ("Brakes","Made with HEL","Twin 320 mm floating discs and four-piston radial calipers made with HEL; 265 mm at the rear. Cornering ABS.","assets/ls_macro_caliper.jpg"),
      ("Electronics, written here","In house","Traction, wheelie, launch and cruise control developed in house, because nobody else's would do what we wanted. A dash turned from solid, with a TFT touchscreen.","assets/ls_macro_cockpit.jpg"),
      ("The exhaust","Machined end cap","Langen system with a machined, engraved end cap. A full titanium race system for owners who want it louder and lighter.","assets/ls_macro_endcap.jpg"),
    ])}
  </div>
</section>

{strip(("","In detail"),"The parts you will come to know.",[
  ("assets/ls_macro_lamp_side.jpg","Lightspeed halo headlamp in its carbon nacelle","Halo, carbon, billet.","LED halo lamp in a machined bezel and carbon nacelle.","45% 50%"),
  ("assets/ls_macro_filler.jpg","Lightspeed machined filler cap","Turned from solid.","The filler cap, machined in one piece minutes from the factory door.","50% 50%"),
  ("assets/ls_macro_tank.jpg","Lightspeed tank with the Langen script","The tank.","Hand-laid carbon under paint, or left bare. Nineteen litres.","60% 50%"),
  ("assets/ls_macro_endcap.jpg","Lightspeed exhaust end cap","The end cap.","Machined and engraved by hand. A titanium race system is available.","55% 50%"),
  ("assets/ls_macro_cockpit.jpg","Lightspeed cockpit from above","The cockpit.","A dash turned from solid, a TFT touchscreen, bars set to your reach.","50% 45%"),
  ("assets/ls_macro_fuelcap.jpg","Lightspeed carbon tank top and fuel cap","Carbon, by hand.","Every panel is laid up by people who make for Formula 1.","50% 50%"),
  ("assets/ls_macro_sprocket.jpg","Lightspeed rear sprocket and forged wheel","The rear wheel.","Forged, machined, anodised; the sprocket carrier is a Langen part.","50% 50%"),
  ("assets/ls_macro_caliper.jpg","Lightspeed brake caliper and disc","The brakes.","Four-piston radial calipers made with HEL on 320 mm floating discs.","50% 50%"),
  ("assets/ls_macro_wheel.jpg","Lightspeed front wheel and radiator","Forged, in house.","Langen forged aluminium wheels, machined and anodised to the specification.","50% 50%"),
  ("assets/ls_macro_seat.jpg","Lightspeed seat and tail","The tail.","A seat you can sit in all day, over a hand-laid carbon tail.","50% 50%"),
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
    <h2 class="section-title">Your colour. Your character.</h2>
    <p class="body">The standard Lightspeed is silver over a bronze chassis with champagne wheels. From there, no two need look alike: bodywork, frame, wheels, seat and every anodised or machined detail are specified individually, and where the palette runs out the design team will develop a finish with you.</p>
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
    <h2>Any road. Any distance.</h2>
    <p>A 790 mm seat, a 19-litre tank, cruise control and touring options for owners who mean to use all 185 horsepower. Geared for around 150 mph as standard; we will gear it longer or shorter to suit how you ride.</p>
  </div>
</section>

<section class="light" id="commission">
  <div class="wrap">
    {chapter("04","The commission")}
    <h2 class="section-title">Not bought. Commissioned.</h2>
    <p class="lede">A Lightspeed is made in conversation with the people who will build it. Six steps, most of them in Wigan; a video call with the bike in front of us if you are overseas.</p>
    <div class="steps">
      <div class="step"><h3>Allocation</h3><p>A refundable {LS["deposit"]} deposit secures one of {LS["builds"]} numbered builds. It stays refundable until your specification is agreed, the sales agreement is signed and manufacturing begins.</p></div>
      <div class="step"><h3>Consultation</h3><p>A day at the workshop with the design engineers: see the bike, sit on it, see how it is built, and talk about yours.</p></div>
      <div class="step"><h3>Fitting</h3><p>Seat height and shape, bar height and sweep, footrest position, ride height and suspension – measured and set to you, not adjusted afterwards.</p></div>
      <div class="step"><h3>Specification</h3><p>Paint, finishes, materials and hard parts, settled with the designers until it is unmistakably yours.</p></div>
      <div class="step"><h3>The build</h3><p>By hand, by a small team, with parts made or machined locally. Updates as it comes together; visit whenever you like.</p></div>
      <div class="step"><h3>Handover</h3><p>Complete, set up to your fitting, with its certificate and build record – and the people who made it.</p></div>
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
      <p class="lede">Twelve, worldwide, drawn from the 185. A forced-induction Lightspeed with one purpose: to be the fastest motorcycle Langen will ever build.</p>
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
    <h1>The one that started it.</h1>
    <div class="btns">
      <a class="btn gold" href="pre-owned.html">Currently offered</a>
      <a class="tlink" href="{ENQ_TS}">Register interest</a>
    </div>
  </div>
</section>
{subnav("Two Stroke",[("overview","Overview"),("engineering","Engineering"),("pre-owned","Changing hands"),("technical","Technical")])}
{numbers_band([("76","hp"),("120","kg"),("100","built"),("12,700","rpm")], 'A 249.5cc two-stroke V-twin from Maranello in a 120 kg motorcycle that sounds like nothing else on the road. One hundred were built. All of them were sold.')}

<section class="light" id="overview">
  <div class="wrap split">
    <div>
      {chapter("01","The idea")}
      <h2 class="section-title">Simplify, then add lightness.</h2>
      <p class="lede">The Two Stroke was the first thing Langen set out to prove: that a small team of engineers could build a motorcycle the big factories wouldn't – a road-going two-stroke with race DNA, refined enough to ride every day, light enough to feel every yard of it.</p>
      <p class="body">An aluminium space frame, carbon bodywork, Öhlins and K-Tech suspension, HEL brakes and an engine developed with Vins Motors in Maranello, with Langen's own patented injection. Every one of the hundred was specified by its owner, and every one is known to us by number.</p>
      <blockquote>“Build quality is spectacular… the whole package is a triumph of handling prowess.”<footer><a href="https://www.motorcyclenews.com/bike-reviews/langen/two-stroke/2022/">Motorcycle News</a></footer></blockquote>
    </div>
    <img src="assets/ts_studio.jpg" alt="Langen Two Stroke, side profile, studio" loading="lazy">
  </div>
</section>

<section id="engineering">
  <div class="wrap">
    {chapter("02","What it is made of")}
    <h2 class="section-title">Race DNA. Road manners.</h2>
    {anno([
      ("Vins Motors V-twin","249.5cc two-stroke","90º two-stroke twin, developed in Maranello, with Langen's patented electronic injection. 76 hp, 45 Nm, a power band from 9,500 rpm.","assets/ts_macro_engine.jpg"),
      ("120 kilograms","Aluminium and carbon","7020-T6 aluminium space frame, carbon fibre tank and bodywork, spoked tubeless rims. Over 600 bhp per tonne.","assets/ts_macro_hub.jpg"),
      ("Öhlins and K-Tech","Made for us","Öhlins 43 mm forks, fully adjustable. Twin K-Tech Razor piggyback shocks, made for us, with length adjustment.","assets/ts_shock.jpg"),
      ("Machined, not moulded","Billet throughout","Billet yokes, levers and lamp bezels. Brembo Serie Oro discs with HEL billet calipers.","assets/ts_macro_lever.jpg"),
      ("One dial","And very little else","A single round instrument in a carbon surround. Electric start, LED lighting, and very little else between you and the engine.","assets/ts_speedo.jpg"),
      ("No two alike","Owner specified","Paint, finishes, seat and hard parts were chosen by each owner. Which is why no two that come back to the factory are the same.","assets/ts_macro_tank.jpg"),
    ])}
  </div>
</section>

{strip(("","In detail"),"No two left the factory alike.",[
  ("assets/ts_seat_14.jpg","Two Stroke number 14 in yellow with a quilted seat","Number 14.","Yellow over carbon, quilted seat, white frame.","50% 50%"),
  ("assets/ts_yokes_gold.jpg","Two Stroke gold-anodised yokes and instrument","Billet yokes.","Machined top yoke, gold anodised, single round dial.","50% 50%"),
  ("assets/ts_lamp_gold.jpg","Two Stroke headlamp with gold bezel","The lamp.","Machined bezel, LED lamp, carbon surround.","50% 50%"),
  ("assets/ts_macro_seat.jpg","Two Stroke leather seat with Langen stitching","The seat.","Leather or Alcantara, stitched by hand, embroidered with the script.","50% 50%"),
  ("assets/ts_purple_tank.jpg","Two Stroke in metallic purple","An owner's purple.","Paint, finishes and hard parts were chosen by each owner.","50% 50%"),
  ("assets/ts_carbon_script.jpg","Carbon exhaust shroud with the Langen script","Carbon shroud.","Laid by hand, finished in gloss, the script set into the weave.","50% 50%"),
  ("assets/ts_wheel_gold.jpg","Two Stroke gold forged wheel and brake","Gold wheel.","Dymag forged wheels on some owners' builds; wire-spoked on the signature specification.","50% 50%"),
  ("assets/ts_seat_leather.jpg","Two Stroke brown leather seat","Brown leather.","A seat specified by its owner, down to the thread.","50% 50%"),
])}

<section class="light" id="pre-owned">
  <div class="wrap split">
    <div>
      {chapter("03","Changing hands")}
      <h2 class="section-title">One hundred were built. Occasionally, one comes back.</h2>
      <p class="lede">When an owner passes theirs on, it returns through the factory and is offered to the next person who will keep it – record, provenance and relationship intact.</p>
      <div class="btns" style="margin-top:24px"><a class="btn gold" href="pre-owned.html">Currently offered</a><a class="tlink" href="{ENQ_TS}">Register interest</a></div>
    </div>
    <img src="assets/ts_tank_top.jpg" alt="Two Stroke 024 bespoke paint" loading="lazy">
  </div>
</section>

<section class="bleed">
  <img class="bg" src="assets/ts_ride_green2.jpg" alt="Two Stroke at speed on a country road" style="object-position:55% 50%">
  <div class="veil"></div>
  <div class="wrap">
    <h2>A sound nothing else makes.</h2>
    <p>Goodwood, the Three Sisters, Silverstone, the Trough of Bowland. One hundred built, every one still turning heads.</p>
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

{enquire_block("Register your interest", "Tell us what you are looking for – a specification, a colour, a number – and where you are. When the right Two Stroke comes back to the factory, you will hear from Christofer or one of the team before it is offered more widely.", ENQ_TS, "Register interest", secondary=False, pdf=False)}
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
    <h1>One hundred were built. Occasionally, one comes back.</h1>
    <p>Every Two Stroke is known to us by number. When an owner decides the time has come to pass theirs on, it returns to the workshop that built it and is offered, through the factory, to the next person who will keep it.</p>
    <div class="btns"><a class="btn gold" href="#available">Currently offered</a><a class="tlink" href="{ENQ_TS}">Register interest</a></div>
  </div>
</section>

<section class="light">
  <div class="wrap split">
    <div>
      {chapter("01","The record")}
      <h2 class="section-title">A place in the record.</h2>
      <p class="lede">Each Langen carries its build number, its original specification and the name of the person it was built for. Changing hands through the factory keeps that record whole – the way the great marques have always handled the cars that matter.</p>
      <p class="body">Before a motorcycle is offered it is returned to the engineers who made it. Its history is verified, it is inspected and prepared to the standard it left with, and it receives a new Certificate of Ownership in the new owner's name. The relationship with the factory passes with the bike: direct support, the owners' portal, first refusal on future editions.</p>
      <p class="body">Should you wish it, the design team will refine colours, finishes and contact points before handover, so that what you take on is yours as well as its history.</p>
    </div>
    <img src="assets/ts_studio.jpg" alt="Langen Two Stroke, side profile, studio" loading="lazy">
  </div>
</section>

<section id="available">
  <div class="wrap">
    {chapter("02","Currently offered")}
    <h2 class="section-title">Motorcycles available through the factory.</h2>
    <p class="body">Each listing opens the brochure prepared for that motorcycle: its specification, history and condition. Interest is taken in order; a bike is usually spoken for within days of being offered.</p>
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
      <div><h3>Refinement</h3><p>Colours, finishes and contact points can be revised with the design team before handover.</p></div>
      <div><h3>Delivery worldwide</h3><p>Pre-owned bikes carry no VAT in the UK or US. We arrange delivery door to door, crated and insured; local taxes and duty are paid on arrival.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap split rev">
    <div>
      {chapter("04","Passing yours on")}
      <h2 class="section-title">When the time comes.</h2>
      <p class="lede">If you decide to part with your Langen, the factory is the right place to do it. We know the bike, we know who is waiting, and the record – and the value – stay intact.</p>
      <div class="btns" style="margin-top:24px"><a class="btn gold" href="{enq("Passing on my Langen", "Hi Langen,\\n\\nI am thinking of passing on my Langen.\\n\\nName:\\nModel and build number:\\nMileage and condition:\\n")}">Talk to us</a></div>
    </div>
    <img src="assets/ts_ride_lane.jpg" alt="Two Stroke on a country lane" loading="lazy" style="object-position:50% 50%">
  </div>
</section>

{enquire_block("Register your interest", "Tell us what you are looking for – a particular specification, a colour, a number – and where you are. When the right motorcycle comes back to the factory, you will hear from Christofer or one of the team before it is offered more widely.", ENQ_TS, "Register interest", secondary=False, pdf=False)}
"""

# ------------------------------------------------------------------ COMMISSION
COMMISSION = f"""
<section class="hero short" style="padding:0">
  <img class="bg" src="assets/ts_build_frame.jpg" alt="A Langen engineer holding a Two Stroke chassis aloft in the workshop" fetchpriority="high" style="object-position:40% 40%">
  <div class="veil"></div>
  <div class="wrap">
    <div class="kicker">Commissioning a Langen</div>
    <h1>The best part is before the bike exists.</h1>
    <p>Owners tell us the commission – the day in the workshop, the drawings, the arguments about colour – is nearly as good as the motorcycle. We take that as a compliment, and have built the process around it.</p>
  </div>
</section>

<section class="light">
  <div class="wrap">
    {chapter("01","Six steps")}
    <h2 class="section-title">Six steps, one conversation.</h2>
    <p class="lede">From a refundable deposit to the day you ride it away. Most of it happens in person, in Wigan; for overseas owners we do the same over a video call with the bike in front of us.</p>
    <div class="steps">
      <div class="step"><h3>Allocation</h3><p>A refundable {LS["deposit"]} deposit secures a numbered build. It stays refundable until your specification is agreed, the sales agreement is signed and manufacturing begins. <a href="#" class="terms-link">Deposit terms</a>.</p></div>
      <div class="step"><h3>Consultation</h3><p>A day at the workshop with the design engineers. You see the bike, sit on it, see how it is built, and we talk about what you want from yours.</p></div>
      <div class="step"><h3>Fitting</h3><p>Seat height and shape, bar height and sweep, footrest position, ride height and suspension set-up – measured and set to you, not adjusted afterwards.</p></div>
      <div class="step"><h3>Specification</h3><p>Paint, exposed carbon or a mix. Frame, swingarm and wheel colours. Seat material and stitching. Machined and anodised hardware. Wheels, exhaust, suspension pack. A visual is prepared and a sales agreement drawn up.</p></div>
      <div class="step"><h3>The build</h3><p>By hand, by a small team, with parts made or machined locally. You receive updates as it comes together, and you are welcome to visit.</p></div>
      <div class="step"><h3>Handover</h3><p>Presented complete, set up to your fitting, with its certificate, build record and the people who made it. Delivered to you, or collected from Wigan.</p></div>
    </div>
  </div>
</section>

<section class="bleed">
  <img class="bg" src="assets/ts_seat_leather.jpg" alt="A brown leather Langen seat, embroidered, on a carbon tail" style="object-position:50% 50%">
  <div class="veil"></div>
  <div class="wrap">
    <h2>On the menu, and off it.</h2>
    <p>There is no fixed options list. Most owners choose from the finishes and hard parts we already make. Where someone needs something that doesn't exist yet – a thumb brake, a different footrest hanger, a seat built to a measurement – we engineer it into the bike rather than bolt it on afterwards.</p>
  </div>
</section>

<section>
  <div class="wrap">
    {chapter("02","What it costs")}
    <h2 class="section-title">A finished motorcycle, then your choices.</h2>
    <p class="body">A standard Lightspeed is {LS["price_from"]} plus VAT: silver over a bronze chassis with champagne wheels, complete and ready to ride. Nothing is needed to make it whole. The final figure depends on how far you take the specification; a heavily specified bike with full custom paint, the K-Tech suspension pack, upgraded wheels and bespoke finishes throughout can reach {LS["price_heavily_specified"]}, with most builds landing between the two. The {LS["deposit"]} deposit comes off the price.</p>
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
    <h2 class="section-title">The relationship doesn't end at handover.</h2>
    <div class="own three">
      <div><h3>Direct to the factory</h3><p>No dealer in between. The engineers who built your motorcycle look after it, and owners have a direct line to Christofer.</p></div>
      <div><h3>Overseas support</h3><p>Overseas owners appoint a workshop of their choice; we furnish it with the internal documents, tools and a direct line to the people who designed and built the bike.</p></div>
      <div><h3>Owners' portal</h3><p>Documentation, build updates and the record for your motorcycle, in one place.</p></div>
      <div><h3>First refusal</h3><p>Future ultra-limited editions are offered to owners and build-number holders before anyone else.</p></div>
      <div><h3>Provenance</h3><p>Every build numbered, its specification recorded, a certificate issued. Certified Pre-Owned keeps that record intact when a bike changes hands.</p></div>
      <div><h3>The door is open</h3><p>Owners are welcome at the workshop. Bring the bike; bring a friend who is thinking about one.</p></div>
    </div>
  </div>
</section>

{enquire_block("Begin a conversation", "Tell us where you are and what you have in mind – a colour, a fit, a question – and Christofer or one of the team will come back to you personally. If it is easier to talk, send a time that suits and we'll call you.")}
"""

# ------------------------------------------------------------------ ABOUT
ABOUT = f"""
<section class="hero short" style="padding:0">
  <img class="bg" src="assets/ts_news.jpg" alt="Langen Two Stroke in front of the We Do Things Differently Here wall at the workshop" fetchpriority="high" style="object-position:70% 50%">
  <div class="veil"></div>
  <div class="wrap">
    <div class="kicker">Langen Motorcycles · Wigan, England</div>
    <h1>Engineers first.</h1>
    <p>Langen was founded in 2018 to build the motorcycles its founder couldn't buy: light, mechanical, hand-made, and engineered around the rider rather than the showroom.</p>
  </div>
</section>

<section class="light">
  <div class="wrap split">
    <div>
      {chapter("01","The story")}
      <h2 class="section-title">The story so far.</h2>
      <p class="lede">Christofer Ratcliffe was Chief Design Engineer at CCM when he began drawing an ultra-lightweight road motorcycle unlike anything on sale. In 2019 a partnership with Vincenzo Mattia's Vins Motors in Maranello gave it an engine, and Langen Motorcycles was born.</p>
      <p class="body">The Two Stroke followed – one hundred built, every one sold, ridden on three continents and reviewed as a benchmark for handling. The team grew with it: engineers and designers from CCM, Triumph, BAC, McLaren and M-Sport, each with a reason to question how things are usually done.</p>
      <p class="body">The Lightspeed, revealed at Gunhill Studios in November 2025, is the second model: 185 horsepower, 185 kilograms, 185 builds, with Langen's own electronics and the highest UK manufacturing content of any motorcycle maker. The LS12 Turbo – twelve of them – comes next.</p>
    </div>
    <img src="assets/team.jpg" alt="The Langen team with the first Lightspeed" loading="lazy" style="object-position:50% 50%">
  </div>
</section>

{LETTER.replace('class="light letter-wrap"','class="letter-wrap"')}

<section class="light">
  <div class="wrap">
    {chapter("02","How we work")}
    <h2 class="section-title">Everything is there for a reason.</h2>
    <div class="steps three">
      <div class="step"><h3>Design</h3><p>Every component is drawn by us and judged on weight, function and how it looks in the hand. If a part can't be made better, it isn't on the bike.</p></div>
      <div class="step"><h3>Engineering</h3><p>Chassis analysed in our own FEA tools, electronics and rider aids written in house, materials chosen for what they do rather than what they cost.</p></div>
      <div class="step"><h3>Testing</h3><p>Dyno, road and track before anything is signed off – procedures in line with the large OEMs, with the attention that comes from building slowly, by hand.</p></div>
      <div class="step"><h3>Making</h3><p>Chassis welded and bodywork laid up by local partners who make for Formula 1 and aerospace. Billet parts machined minutes from the factory door.</p></div>
      <div class="step"><h3>Commissioning</h3><p>Each bike built to its owner's fit and specification, with the design team, in person. No two alike.</p></div>
      <div class="step"><h3>Looking after it</h3><p>Owners deal with the factory directly. The engineers who built the bike are the ones who maintain it.</p></div>
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
        <h2 class="section-title">Next to a racetrack, on purpose.</h2>
        <p class="lede">Kingfisher Court, Wigan – beside the Three Sisters circuit, twenty minutes from Manchester, in the part of England that built the first machines. The local mantra is one we have adopted: we do things differently here.</p>
        <p class="body">Visits are by appointment and always welcome. Owners, prospective owners and anyone who wants to see a motorcycle built by hand.</p>
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

{enquire_block("Come and see for yourself", "The best way to understand a Langen is to stand next to one. Tell us when suits and we'll put the kettle on.", enq("Workshop visit", "Hi Langen,\\n\\nI'd like to arrange a visit to the workshop.\\n\\nName:\\nWhere I'm travelling from:\\nDates that suit:\\n"), "Arrange a visit")}
"""

# ------------------------------------------------------------------ NEWS (content/news/*.md)
NEWS_PAGE = f"""
<section class="page-head">
  <div class="wrap">
    <div class="kicker">News</div>
    <h1>From the workshop.</h1>
    <p class="lede">Reveals, events, awards and the occasional look over the engineers' shoulders.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="news">{news_cards(NEWS)}</div>
    <p class="note" style="margin-top:30px">For press enquiries and image requests, see the <a href="owners.html#press" style="color:#fff">press page</a>.</p>
  </div>
</section>
{enquire_block("Stay in touch", "If you would like to hear from us as the first Lightspeeds are delivered, drop us a line and we will add you to the small list of people we write to directly.", enq("Keep me informed", "Hi Langen,\\n\\nPlease keep me informed about Langen news and the Lightspeed.\\n\\nName:\\nCountry:\\n"), "Keep me informed", secondary=False, pdf=False)}
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
 (f"What makes a Langen different?",f"Each one is commissioned rather than bought. Your riding position, geometry and suspension are set to you before the build starts, and paint, finishes and the machined details are chosen with the design team who will make them. The engineers who build your bike are the ones who look after it – there is no dealer in between."),
 (f"How limited are they?",f"The Two Stroke was a run of 100, now sold out. The Lightspeed is limited to {LS["builds"]} builds worldwide, each numbered, with {LS["us_allocation"]} allocated to the United States. The LS12 Turbo will be twelve."),
 (f"What does a Lightspeed cost?",f"From {LS["price_from"]} plus VAT for a complete, finished motorcycle. The final figure depends on your specification; a heavily specified bike can reach {LS["price_heavily_specified"]}. Export builds are priced without UK VAT, plus shipping, duty and local taxes."),
 (f"How do I reserve one?",f"A {LS["deposit"]} deposit reserves a numbered build. It is fully refundable until your specification session is complete, the sales agreement is signed and manufacturing begins, and it comes off the price of the bike."),
 (f"Can I have one outside the UK?",f"Yes. UK-specification builds deliver first; fully homologated versions for the USA, Europe, Japan, the Middle East and Australasia follow through 2027. US owners can take an early UK-specification bike through the Montana route. We arrange air freight door to door, crated and insured; clearance and duty are paid on arrival."),
 (f"How far can I customise it?",f"As far as you like. Colours, finishes, seat, wheels, exhaust and suspension are specified with the design team, and where a part doesn't exist yet – a thumb brake, a different footrest hanger – we engineer it into the bike rather than bolting it on afterwards."),
 (f"Can I visit?",f"Please do. The workshop is at Kingfisher Court, Wigan, next to the Three Sisters circuit. Visits are by appointment; email or call and we will find a time."),
 (f"Is the Two Stroke still available?",f"New builds are closed. When an owner passes one on it comes back through the factory, inspected, certified and warranted, and is offered to the people who have registered interest first."),
]
CONTACT = f"""
<section class="page-head">
  <div class="wrap">
    <div class="kicker">Contact</div>
    <h1>Talk to the people who build them.</h1>
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
    <h2 class="section-title">Questions we are asked most.</h2>
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
    <h1>A small team. Room for a few more.</h1>
    <p class="lede">We build the motorcycles that used to be posters on bedroom walls, in a workshop in Wigan, with people who came from CCM, Triumph, BAC, McLaren and M-Sport to do it. If you would rather make one thing properly than a thousand things adequately, read on.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="own three">
      <div><h3>What we are for</h3><p>Motorcycles that move your soul – machines that unite technical performance with the purity of the ride.</p></div>
      <div><h3>How we behave</h3><p>Honesty, integrity, inclusiveness, innovation, quality, openness, creativity – and fun. Each upheld with equal dedication.</p></div>
      <div><h3>What we expect</h3><p>That you question the norm, own your work, and care about the rider at the end of it.</p></div>
    </div>
    <h2 class="section-title" style="margin-top:60px">Open roles</h2>
    <div class="roles">
      <div class="role"><div><h3>Lead Technician</h3><div class="meta">Wigan · Full-time</div><p>An experienced, proactive technician for a fast-moving workshop: assembly and development work, primarily but not only on motorcycles. Best suited to someone with high-level workshop experience at an OEM or dealership.</p></div><a class="btn ghost" href="{enq("Application – Lead Technician")}">Apply</a></div>
      <div class="role"><div><h3>Automotive Design Engineer</h3><div class="meta">Wigan · Full-time</div><p>Design and development across the whole motorcycle, from chassis to machined detail. Experience designing to a high standard in the automotive industry; all levels considered for the right person.</p></div><a class="btn ghost" href="{enq("Application – Automotive Design Engineer")}">Apply</a></div>
      <div class="role"><div><h3>Customer Development Specialist</h3><div class="meta">Wigan · Full-time</div><p>Building and keeping owner relationships, from first enquiry to handover and beyond. Proactive, adaptable, and good with people who care about details.</p></div><a class="btn ghost" href="{enq("Application – Customer Development Specialist")}">Apply</a></div>
    </div>
    <p class="note" style="margin-top:26px">Nothing that fits? We are always interested in engineers, technicians and makers who want to be part of the story. Send a CV and a few lines about what you'd bring.</p>
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
 "index.html":      ("Langen Motorcycles – hand-built in Wigan, England","Langen builds motorcycles to order for one rider at a time. The Lightspeed: 185 hp, 185 kg, 185 builds. The Two Stroke: 100 built. We do things differently here.","index.html","assets/ls_front_bokeh.jpg",HOME,None),
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
