#!/usr/bin/env python3
"""Builds every page of builtbycompo.co.uk from the shared layout below.
Run:  python3 tools/build.py            (writes the real site pages into the repo root)
      python3 tools/build.py --preview  (also writes _preview/ for a private preview)
Edit the wording in the PAGES section, then run it again."""
import sys, os, html, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://builtbycompo.co.uk"
EMAIL = "luke@builtbycompo.co.uk"
WA = "447517945561"   # used in the WhatsApp link only; the number is not shown on the page
YEAR = "2026"
TODO = lambda t: f'<mark class="todo">[{t}]</mark>'

NAV = [("about.html", "About me"), ("what-i-do.html", "What I do"), ("pricing.html", "Pricing"), ("faqs.html", "FAQs")]
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def ribbon_track(words, n=8):
    spans = "".join(f"<span>{w}</span>" for w in words) * n
    return f'<div class="ribbon-shift" data-speed="{{speed}}"><div class="ribbon-track" aria-hidden="true">{spans}{spans}</div></div>'

def ribbons():
    unit = "Websites that work  •  Bespoke builds  •  Built only for you  •  "
    return f'''<div class="arc" role="img" aria-label="Websites that work. Bespoke builds. Built only for you.">
  <svg viewBox="0 0 1600 400" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    <path id="arc-path" d="M-200,395 Q760,-70 1800,215" fill="none" stroke="#ff5412" stroke-width="150"/>
    <text dy="27" xml:space="preserve"><textPath href="#arc-path" startOffset="0" data-unit="{len(unit)}">{unit * 7}</textPath></text>
  </svg>
</div>'''

def ribbon_solo(words, cls="a", speed="-0.3"):
    t = ribbon_track(words).replace("{speed}", speed)
    return f'<div class="ribbon solo {cls}" role="img" aria-label="{html.escape(". ".join(words))}.">{t}</div>'

SEAL = '''<svg class="{cls}" viewBox="0 0 200 200" role="img" aria-label="Built by Compo. Bespoke websites. Essex, England.">
  <defs><path id="sealpath-{id}" d="M100,100 m-74,0 a74,74 0 1,1 148,0 a74,74 0 1,1 -148,0"/></defs>
  <circle cx="100" cy="100" r="97" fill="none" stroke="currentColor" stroke-width="3"/>
  <circle cx="100" cy="100" r="54" fill="none" stroke="currentColor" stroke-width="2"/>
  <text font-family="Nunito,'Century Gothic',sans-serif" font-weight="800" font-size="13.5" fill="currentColor"><textPath href="#sealpath-{id}" startOffset="0" textLength="463" lengthAdjust="spacing">BUILT BY COMPO ✦ BESPOKE WEBSITES ✦ ESSEX, ENGLAND ✦ </textPath></text>
  <text x="100" y="100" dy=".355em" text-anchor="middle" font-family="Nunito,'Century Gothic',sans-serif" font-weight="900" font-size="78" fill="currentColor">C</text>
</svg>'''

def cta_panel(heading='Tell me about <span class="coop">your project</span>'):
    return f'''<section>
  <div class="wrap">
    <div class="cta-panel reveal">
      <span class="sticker pop">No pressure</span>
      <h2>{heading}</h2>
      <p>Send me a message and we'll have a proper conversation. I'd like to get to know your business before I suggest anything.</p>
      <div class="row"><a class="btn hot" href="contact.html">Start a conversation {ARROW}</a></div>
    </div>
  </div>
</section>'''

# ------------------------------------------------------------------ PAGES
PAGES = {}

PAGES["index.html"] = dict(
  title="Built by Compo · Website design in Essex",
  desc="Bespoke websites for small businesses, designed, built and looked after by Compo. A small web studio based in Essex, England.",
  body=f'''
<section class="hero">
    <div class="hero-panel">
      <canvas class="liquid" data-strength="0.3" aria-hidden="true"></canvas>
      <div class="seal-wrap">{SEAL.format(cls="seal", id="h")}</div>
      <h1 class="wipe">Websites<br>that work.</h1>
      <div class="hero-foot">
        <p class="lede reveal" style="--d:.25s">I'm Compo. I design, build and look after bespoke websites for small businesses.</p>
        <div class="row reveal" style="--d:.35s">
          <a class="btn" href="contact.html">Tell me about your project {ARROW}</a>
          <a class="btn ghost" href="pricing.html">See pricing</a>
        </div>
      </div>
    </div>
</section>

{ribbons()}

<section class="statement-sec">
  <div class="wrap">
    <p class="eyebrow reveal">A bit about me</p>
    <div class="sticker-row"><span class="sticker pop" style="--r:-5deg">One-person studio</span><span class="sticker peach pop" style="--r:3deg;--d:.35s">Allergic to templates</span><span class="sticker red pop" style="--r:-3deg;--d:.5s">Phones first</span></div>
    <p class="statement" data-fill>I think a good website should be simple to use, quick to load and easy to find. So I design and build each one from scratch, then look after it once it's live.</p>
    <div class="row reveal"><a class="btn ghost" href="about.html">More about me {ARROW}</a></div>
  </div>
</section>

<section class="work" aria-labelledby="work-h">
  <div class="wrap sec-head">
    <p class="eyebrow reveal">Selected work</p>
    <h2 id="work-h" class="reveal">Recently <span class="coop">built</span></h2>
    <p class="muted reveal" style="max-width:34ch">Drag or swipe to look around. One of these spots is always yours.</p>
  </div>
  <div class="slider reveal" tabindex="0" role="region" aria-label="Portfolio, scrolls sideways">
    <div class="slider-track">
      <a class="card-work" href="https://tanyahill.co.uk" rel="noopener">
        <img src="img/work-tanya.jpg" width="960" height="960" loading="lazy" alt="Homepage of tanyahill.co.uk, a business coaching website with a 'Which boss are you?' quiz">
        <span class="cap"><span>Tanya Hill Coaching</span></span>
      </a>
      <a class="card-work yours c1" href="contact.html"><span><span class="big">Your website</span><span class="sm">This spot's free</span></span></a>
      <a class="card-work yours c2" href="contact.html"><span><span class="big">Your website</span><span class="sm">Could be next</span></span></a>
      <a class="card-work yours c3" href="contact.html"><span><span class="big">Your website</span><span class="sm">Let's talk</span></span></a>
    </div>
  </div>
</section>

<section aria-labelledby="svc-h">
  <div class="wrap" style="display:grid;gap:clamp(24px,4vw,44px)">
    <div style="display:grid;gap:14px">
      <p class="eyebrow reveal">What I do</p>
      <h2 id="svc-h" class="reveal">This is my <span class="coop">thing</span></h2>
    </div>
    <ul class="svc-list">
      <li class="reveal"><h3>Design</h3><p>A look made for your business, drawn up for a phone screen first because that's where most of your visitors are.</p></li>
      <li class="reveal"><h3>Build</h3><p>Written by hand, so it loads quickly and only has what you need on it.</p></li>
      <li class="reveal"><h3>Custom features</h3><p>Quizzes, galleries, booking buttons. If it helps your customers get in touch, I can build it.</p></li>
      <li class="reveal"><h3>Hosting and care</h3><p>I keep your site online, check it every month and make your changes for you.</p></li>
    </ul>
    <div class="row reveal"><a class="btn ghost" href="what-i-do.html">Everything I do {ARROW}</a></div>
  </div>
</section>

<section aria-labelledby="say-h">
  <div class="wrap deck-wrap">
    <div style="display:grid;gap:14px;justify-items:center;text-align:center">
      <h2 id="say-h" class="reveal">Apparently, they <span class="coop">like it</span></h2>
    </div>
    <ul class="deck solo reveal">
      <li>
        <div class="quote-mark" aria-hidden="true">“</div>
        <blockquote>Built by Compo was amazing and gave me a website that helped my business grow and looks great.</blockquote>
        <div class="who"><img class="av" src="img/tanya-hill.jpg" width="96" height="96" loading="lazy" alt="Tanya Hill"><span><b>Tanya Hill</b><span>Tanya Hill Coaching</span></span></div>
      </li>
    </ul>
  </div>
</section>

{cta_panel()}
''')

PAGES["about.html"] = dict(
  title="About me · Built by Compo",
  desc="Built by Compo is a small web studio in Essex, England, run by Compo. I design, build and look after bespoke websites for small businesses.",
  body=f'''
<section class="page-hero">
  <div class="wrap">
    <h1 class="wipe">Hello, I'm <span class="coop">Compo.</span></h1>
  </div>
</section>

<section class="about-main" style="padding-top:0">
  <div class="wrap">
    <div class="about-copy">
      <h2 class="reveal" style="font-size:clamp(1.6rem,4vw,2.6rem)">A small studio based in Essex, England</h2>
      <p class="reveal">Built by Compo is me, a laptop and a lot of coffee. Compo has been my nickname for years, and it stuck.</p>
      <p class="reveal">I make websites for small businesses that want something better than a template. I design each one from scratch, build it by hand and set it up to be found on Google. Then I host it and look after it, so you never have to log in to anything.</p>
      <p class="reveal">I like things that are simple, quick and a bit different. I'll tell you plainly what I think will work, and I'll always give you a fixed price before I start.</p>
      <p class="reveal">When I'm not building websites, I'm usually out walking Lemon, my chihuahua. She's in charge of morale.</p>
    </div>
    <div class="reveal" style="display:grid;gap:14px;justify-items:center">
      <p class="display" style="font-size:clamp(1.6rem,4vw,2.4rem);color:var(--orange-text)">Websites that work</p>
      {SEAL.format(cls="about-seal", id="a")}
    </div>
  </div>
</section>

{ribbon_solo(["Design", "Build", "Hosting", "Care"], "ink")}

<section>
  <div class="wrap" style="display:grid;gap:clamp(24px,4vw,44px)">
    <h2 class="reveal">How I <span class="coop">work</span></h2>
    <ul class="svc-list">
      <li class="reveal"><h3>We talk</h3><p>A relaxed conversation about your business, your customers and what you need the site to do.</p></li>
      <li class="reveal"><h3>I quote</h3><p>One fixed price in writing, with everything it includes. Nothing starts until you're happy.</p></li>
      <li class="reveal"><h3>I build</h3><p>You get a private preview link to watch it come together, with two rounds of changes included.</p></li>
      <li class="reveal"><h3>We launch</h3><p>Your site goes live on your own domain, and I keep looking after it on a monthly care plan.</p></li>
    </ul>
  </div>
</section>

{cta_panel('Fancy a <span class="coop">chat?</span>')}
''')

def svc(h, lead, ticks, i):
    lis = "".join(f"<li>{t}</li>" for t in ticks)
    return f'''<div class="svc-block">
      <h2 class="reveal">{h}</h2>
      <div class="body"><p class="lede reveal" style="max-width:none">{lead}</p><ul class="ticks reveal">{lis}</ul></div>
    </div>'''

PAGES["what-i-do.html"] = dict(
  title="What I do · Built by Compo",
  desc="Website design, hand-built websites, custom features, SEO set-up, hosting and monthly care for small businesses in Essex and beyond.",
  body=f'''
<section class="page-hero">
  <div class="wrap">
    <h1 class="wipe">This is my <span class="coop">thing.</span></h1>
    <p class="lede reveal" style="max-width:44ch">I take a website from first idea to live and looked after. Here's what that covers.</p>
  </div>
</section>

<section style="padding-block:0"><div class="wrap">
    {svc('Website <span class="coop">design</span>', "Every site starts as a blank page, not a template. I design it around your business and your customers.", ["Designed for phones first, then tablets and laptops", "Your colours, your photos and your way of talking", "Clear buttons that lead to a call, a message or a booking"], 1)}
</div></section>
<section style="padding-block:0"><div class="wrap">
    {svc('Website <span class="coop">build</span>', "I build your site by hand, so it's quick, tidy and only carries what it needs.", ["Fast pages, tested on real phones", "Built to be easy to read and use for everyone", "Simple animations included, like the ones on this site", "Your domain connected for you"], 2)}
</div></section>
<section style="padding-block:0"><div class="wrap">
    {svc('Custom <span class="coop">features</span>', "Sometimes a site needs to do more than show information. I can build tools that are made just for you.", ["Quizzes with personal results, like the one on tanyahill.co.uk", "Photo galleries, booking helpers and enquiry buttons", "Custom animation and illustration as extras"], 3)}
</div></section>
<section style="padding-block:0"><div class="wrap">
    {svc('SEO <span class="coop">set-up</span>', "SEO is short for search engine optimisation. It's the behind-the-scenes work that helps Google understand your site and show it to people searching for what you do.", ["Page titles and descriptions written the way people search", "Your site registered with Google, so new pages get picked up", "Fast, tidy pages, which Google rewards", "Help with your Google Business Profile, so you show up on Maps", "A proper preview image when your link is shared"], 4)}
</div></section>
<section style="padding-block:0"><div class="wrap">
    {svc('Hosting and <span class="coop">care</span>', "Once you're live, I keep things running. You send me changes by WhatsApp or email and I make them.", ["Hosting included in every care plan", "A health check every month", "Small changes made for you, with no logging in", "You own your domain, your accounts and your finished site"], 5)}
</div></section>

{cta_panel('Got something <span class="coop">in mind?</span>')}
''')

def price(name, amt, per, blurb, ticks, feature=False):
    lis = "".join(f"<li>{t}</li>" for t in ticks)
    cls = "price feature" if feature else "price"
    return f'''<article class="{cls} reveal">
      {'<span class="sticker pop">Most popular</span>' if feature else ''}
      <h3>{name}</h3>
      <p class="amt">{amt}{f" <small>{per}</small>" if per else ""}</p>
      <p>{blurb}</p>
      <ul class="ticks">{lis}</ul>
    </article>'''

PAGES["pricing.html"] = dict(
  title="Pricing · Built by Compo",
  desc="Clear website prices. Starter £1,195, Standard £1,795, Bespoke from £2,750, with monthly care plans from £50. Fixed quotes before any work starts.",
  body=f'''
<section class="page-hero">
  <div class="wrap">
    <h1 class="wipe">Clear <span class="coop">prices.</span></h1>
    <p class="lede reveal" style="max-width:46ch">No hidden extras. You get one fixed price in writing before I start, and these are the starting points.</p>
  </div>
</section>

<section style="padding-top:0" aria-labelledby="builds-h">
  <div class="wrap" style="display:grid;gap:24px">
    <h2 id="builds-h" class="reveal">Website <span class="coop">builds</span></h2>
    <div class="price-grid">
      {price("Starter", "£1,195", "", "A smart, simple site that gets you found and gets you contacted.", ["Up to 5 pages", "Designed for phones first", "WhatsApp or booking button", "SEO basics set up", "Privacy policy page"])}
      {price("Standard", "£1,795", "", "More room to show what you do, with one custom feature.", ["Up to 8 pages", "One custom feature, such as a gallery or simple quiz", "Full SEO set-up", "Help with your Google Business Profile"], True)}
      {price("Bespoke", "from £2,750", "", "For custom tools, custom animation or a more involved design.", ["Custom tools, like a quiz with result pages", "Custom animation and design", "Help with your wording", "Quoted to fit the job"])}
    </div>
    <p class="muted reveal">Every build includes simple animations, connecting your domain, and two rounds of changes.</p>
  </div>
</section>

{ribbon_solo(["Hosting", "Health checks", "Changes made for you"], "b", "-0.3")}

<section aria-labelledby="care-h">
  <div class="wrap" style="display:grid;gap:24px">
    <h2 id="care-h" class="reveal">Monthly <span class="coop">plans</span></h2>
    <div class="price-grid two">
      {price("Care", "£50", "a month", "Your site hosted, checked and kept up to date.", ["Hosting", "A health check every month", "Renewals and security looked after", "Up to 30 minutes of small changes each month"])}
      {price("Growth", "£125", "a month", "Everything in Care, with more time and more help being found.", ["Everything in Care", "Google Business Profile posts", "Monthly search tweaks", "Up to 2 hours of changes each month", "A short monthly report"])}
    </div>
  </div>
</section>

<section style="padding-top:0" aria-labelledby="know-h">
  <div class="wrap" style="display:grid;gap:24px">
    <h2 id="know-h" class="reveal" style="font-size:clamp(1.6rem,4vw,2.6rem)">Good to know</h2>
    <div class="notes">
      <div class="reveal"><b>How payment works</b>Half to start, half when your site is ready to go live.</div>
      <div class="reveal"><b>No VAT to add</b>I'm not VAT registered, so the price you see is the price you pay.</div>
      <div class="reveal"><b>You own it</b>Your domain, your accounts and your finished website are yours.</div>
      <div class="reveal"><b>No long contracts</b>Care plans have a 3-month minimum to begin with, then run month to month with 30 days' notice.</div>
      <div class="reveal"><b>What's not included</b>Your domain name (about £4 a year for a .co.uk), business email, photography and paid tools.</div>
      <div class="reveal"><b>Extra work</b>Anything outside your plan gets a fixed price, agreed before I start.</div>
    </div>
    <p class="muted reveal">The full terms come with your quote. See also my <a href="refunds.html">refund policy</a>.</p>
  </div>
</section>

{cta_panel('Not sure which <span class="coop">fits?</span>')}
''')

PAGES["contact.html"] = dict(
  title="Contact · Built by Compo",
  desc="Tell me about your project. Message Compo at Built by Compo by email or WhatsApp to talk about a new website for your business.",
  body=f'''
<section class="page-hero" style="padding-bottom:0">
  <div class="wrap">
    <h1 class="wipe">Let's <span class="coop">talk.</span></h1>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="cta-panel contact-grid reveal">
      <div style="display:grid;gap:20px">
        <h2 style="font-size:clamp(2rem,5vw,3.8rem)">Tell me about <span class="coop">your project</span></h2>
        <p>I'd like a proper conversation, so I can understand your business before I suggest anything. Pop your name in and I'll get a message started for you.</p>
        <p class="small">This form doesn't send or store anything. It opens your own email or WhatsApp with a message ready, and you press send.</p>
      </div>
      <form class="form" id="project-form" data-email="{EMAIL}" data-wa="{WA}" novalidate>
        <fieldset>
          <legend>How would you like to message me?</legend>
          <div class="choice">
            <label><input type="radio" name="how" id="how-email" value="email" checked><span>Email</span></label>
            <label><input type="radio" name="how" id="how-wa" value="whatsapp"><span>WhatsApp</span></label>
          </div>
        </fieldset>
        <div class="field"><label for="first">First name</label><input id="first" name="first" autocomplete="given-name" required></div>
        <div class="field"><label for="last">Last name</label><input id="last" name="last" autocomplete="family-name" required></div>
        <div class="field"><label for="business">Business name</label><input id="business" name="business" autocomplete="organization"></div>
        <div class="row"><button class="btn hot" type="submit" id="form-go">Open my email app {ARROW}</button></div>
        <p id="form-out" class="small" role="status" aria-live="polite"></p>
      </form>
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap narrow">
    <ul class="plain-list">
      <li class="reveal"><b>Email</b><span><a href="mailto:{EMAIL}">{EMAIL}</a> <button class="btn ghost mini" type="button" data-copy="{EMAIL}">Copy</button></span></li>
      <li class="reveal"><b>WhatsApp</b><span><a href="https://wa.me/{WA}" rel="noopener">Message me on WhatsApp</a></span></li>
      <li class="reveal"><b>Where</b><span>Essex, England. I work with businesses anywhere in the UK.</span></li>
      <li class="reveal"><b>When</b><span>Monday to Saturday. I aim to reply within one working day.</span></li>
    </ul>
  </div>
</section>
''')

FAQS = [
 ("What projects do you take on?", ["Websites for small businesses, sole traders and local services. That could be a simple five-page site or something with custom tools, like a quiz or a booking helper.", "If you're not sure whether your idea fits, ask me. I'll tell you straight if I'm not the right person for it."]),
 ("How much does a project cost?", ['My <a href="pricing.html">pricing page</a> shows the starting price for each type of build and for the monthly plans.', "Bespoke projects vary, so those prices depend on what you need. Take a look at the pricing page or start a conversation, and I'll give you one fixed price before anything begins."]),
 ("How involved do I have to be?", ["Not very. I need your knowledge of your business, the facts and your feedback. I do the rest.", "You'll get a private preview link while I build, and two rounds of changes are included."]),
 ("When can you start, and how long will it take?", ["It depends on the size of the project and what I already have booked in. Once we've talked, I'll give you an accurate start date and timeframe in writing with your quote.", "The clock starts when I have your wording and photos, so having those ready is the quickest way to a finished site."]),
 ("Do you design and build the website?", ["Yes. I design it, build it, host it and look after it. One person from start to finish.", "On a care plan I also run a health check every month and make your updates for you, so the site keeps running well."]),
]

PAGES["faqs.html"] = dict(
  title="FAQs · Built by Compo",
  desc="Answers to common questions about working with Built by Compo: what I take on, what it costs, how involved you need to be and how long it takes.",
  jsonld={"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(re.sub("<[^>]+>", "", a) for a in ans)}} for q, ans in FAQS]},
  body=f'''
<section class="page-hero">
  <div class="wrap">
    <h1 class="wipe">Things you <span class="coop">might ask.</span></h1>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap narrow">
    <div class="faq">
      {"".join(f'<details class="reveal" name="faq"><summary>{q}</summary><div class="ans">{"".join(f"<p>{a}</p>" for a in ans)}</div></details>' for q, ans in FAQS)}
    </div>
  </div>
</section>
{cta_panel('Something <span class="coop">else?</span>')}
''')

DRAFT = '<p class="draft"><b>Draft.</b> Highlighted parts still need your decision, and this page should be checked by a solicitor or a fixed-fee legal service before you rely on it.</p>'
def legal(h1, inner):
    return f'''
<section class="page-hero"><div class="wrap narrow"><h1 style="font-size:clamp(2.2rem,7vw,4.5rem)">{h1}</h1><p class="muted">Last updated: 12 November {YEAR}</p></div></section>
<section style="padding-top:0"><div class="wrap narrow legal">{inner}</div></section>'''

WHO = f'Built by Compo is the trading name of Luke Compton, a sole trader based in Essex, England. Email: <a href="mailto:{EMAIL}">{EMAIL}</a>.'

PAGES["privacy.html"] = dict(title="Privacy policy · Built by Compo", desc="How Built by Compo collects, uses and protects your personal information.", body=legal("Privacy policy", f'''
<h2>Who I am</h2>
<p>{WHO} I'm the "controller" of your personal information, which means I decide how it's used.</p>
<h2>What I collect, and why</h2>
<div class="scroll-x"><table>
<tr><th>When</th><th>What</th><th>Why (lawful basis)</th></tr>
<tr><td>You email or WhatsApp me</td><td>Your name, business name, contact details and whatever you tell me</td><td>To reply and discuss your project (legitimate interests; steps before a contract)</td></tr>
<tr><td>You become a client</td><td>Contact and billing details, project files, and records of our messages and payments</td><td>To do the work and get paid (contract); to keep tax records (legal obligation)</td></tr>
<tr><td>You visit this website</td><td>Technical details such as your IP address, kept briefly in my host's security logs.</td><td>To keep the site secure and working (legitimate interests)</td></tr>
</table></div>
<p>The contact form on this site does not send or store anything. It only prepares a message in your own email or WhatsApp app.</p>
<h2>Who I share it with</h2>
<p>I never sell your information. I use a small number of trusted services to run the business, and they only process information on my instructions or as independent providers:</p>
<ul>
<li>Google Workspace, for email and documents</li>
<li>WhatsApp (Meta), if you choose to message me there</li>
<li>GitHub, which hosts this website</li>
<li>Cloudflare, which manages my domain name</li>
</ul>
<p>Some of these companies store information outside the UK. Where they do, they use safeguards approved under UK data protection law, such as the UK–US Data Bridge or standard contract clauses.</p>
<h2>How long I keep it</h2>
<ul>
<li>Enquiries that don't go ahead: up to 12 months</li>
<li>Client records and invoices: 6 years after our work ends, for tax and legal reasons</li>
</ul>
<h2>Your rights</h2>
<p>You can ask me for a copy of your information, ask me to correct or delete it, ask me to limit how I use it, or object to me using it. To do any of these, email <a href="mailto:{EMAIL}">{EMAIL}</a> and I'll reply within one month.</p>
<p>If you're unhappy with how I've handled your information, please tell me first so I can put it right. You can also complain to the Information Commissioner's Office at <a href="https://ico.org.uk/make-a-complaint/" rel="noopener">ico.org.uk</a> or on 0303 123 1113.</p>
<h2>Cookies</h2>
<p>This website doesn't use cookies. See the <a href="cookies.html">cookie policy</a>.</p>
<h2>Changes</h2>
<p>If I change this policy, I'll update the date at the top of this page.</p>
'''))

PAGES["cookies.html"] = dict(title="Cookie policy · Built by Compo", desc="Built by Compo's website doesn't use cookies. Here's what it does save on your device.", body=legal("Cookie policy", f'''
<h2>The short version</h2>
<p>This website doesn't set any cookies, and it has no advertising or tracking tools. That's why you don't see a cookie banner.</p>
<h2>What is saved on your device</h2>
<p>Nothing. This website doesn't save anything in your browser.</p>
<h2>Visitor counts</h2>
<p>This website doesn't use any analytics or visitor tracking.</p>
<h2>Other websites</h2>
<p>If you follow a link to WhatsApp, a client's website or a social network, that site may set its own cookies. Their policies apply there.</p>
<h2>Questions</h2>
<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
'''))

PAGES["terms.html"] = dict(title="Terms and conditions · Built by Compo", desc="Terms for using the Built by Compo website.", body=legal("Terms and conditions", f'''
<h2>About these terms</h2>
<p>These terms cover your use of this website, builtbycompo.co.uk. {WHO}</p>
<p>If you hire me, our work together is covered by my separate Terms of Business, which you'll receive with your written quote. Nothing on this website is a binding offer. A contract only begins when you accept a written quote.</p>
<h2>Prices</h2>
<p>Prices on this site are a guide and are correct on the date shown at the top of this page. I'm not VAT registered, so no VAT is added. Your fixed price will always be confirmed in your quote.</p>
<h2>Using this website</h2>
<ul>
<li>You may view and share pages from this site for your own use.</li>
<li>Please don't copy the design, wording, images or code for your own or anyone else's commercial use without my written permission. They belong to me or to the people who licensed them to me.</li>
<li>Please don't misuse the site, for example by trying to break it or gain access to anything that isn't public.</li>
</ul>
<h2>Accuracy</h2>
<p>I take care to keep this site correct and up to date, but I can't promise it's free from mistakes. It's general information, not professional advice.</p>
<h2>Links to other websites</h2>
<p>I link to client websites and other services. I'm not responsible for what's on websites I don't run.</p>
<h2>My responsibility to you</h2>
<p>Nothing in these terms limits my liability where it would be unlawful to do so, including for death or personal injury caused by negligence, or for fraud. Otherwise, I'm not liable for losses that come from using, or not being able to use, this website.</p>
<h2>Law</h2>
<p>These terms are governed by the law of England and Wales, and the courts of England and Wales will deal with any dispute.</p>
<h2>Contact</h2>
<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
'''))

PAGES["refunds.html"] = dict(title="Refund policy · Built by Compo", desc="How deposits, payments, cancellations and refunds work at Built by Compo.", body=legal("Refund policy", f'''
<h2>Website builds</h2>
<ul>
<li>You pay half to start and half when your site is ready to go live.</li>
<li><b>Deposit:</b> the deposit books your place in my diary and is non-refundable once paid.</li>
<li>If you cancel part-way through, I keep the deposit. If the work done by then is worth more than the deposit, you pay the difference.</li>
<li>The final payment isn't refundable once your site has gone live.</li>
</ul>
<h2>If something isn't right</h2>
<p>For 30 days after launch, if anything doesn't work the way we agreed, I'll fix it free of charge. Please tell me first and give me the chance to put it right.</p>
<h2>Monthly plans</h2>
<ul>
<li>Your first Care plan has a 3-month minimum. After that it runs month to month.</li>
<li>You can cancel with 30 days' notice by email or WhatsApp.</li>
<li>Monthly payments aren't refunded for part-used months.</li>
</ul>
<h2>Costs paid to other companies</h2>
<p>Domain names, email accounts and other services you buy from another company are covered by that company's own refund rules.</p>
<h2>Your legal rights</h2>
<p>My services are for businesses. If you're buying as a consumer, meaning not for your trade, business or profession, you may have extra rights, including a 14-day right to cancel a service you ordered at a distance. Nothing in this policy takes away any legal rights you have.</p>
<h2>How to ask for a refund</h2>
<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> with your name and project. I'll reply within 5 working days, and any refund due is paid within 14 days to the account you paid from.</p>
'''))

PAGES["404.html"] = dict(title="Page not found · Built by Compo", desc="That page doesn't exist.", noindex=True, body=f'''
<section class="page-hero"><div class="wrap"><h1>Nothing <span class="coop">here.</span></h1><p class="lede">That page has moved or never existed.</p><div class="row"><a class="btn" href="{{HOME}}">Back to the homepage {ARROW}</a></div></div></section>''')

# ------------------------------------------------------------------ LAYOUT
def page(name, p, preview=False):
    home = "index.html" if preview else "./"
    cur = lambda href: ' aria-current="page"' if href == name else ""
    nav = "".join(f'<a href="{h}"{cur(h)}>{t}</a>' for h, t in NAV)
    canon = SITE + "/" + ("" if name == "index.html" else name.replace(".html", ""))
    ld = p.get("jsonld") or ({"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Built by Compo", "url": SITE + "/", "email": EMAIL, "areaServed": "GB", "address": {"@type": "PostalAddress", "addressRegion": "Essex", "addressCountry": "GB"}, "description": "Bespoke websites for small businesses, designed, built and looked after by Compo."} if name == "index.html" else None)
    head = f'''<title>{p["title"]}</title>
<meta name="description" content="{html.escape(p["desc"])}">
{'<meta name="robots" content="noindex">' if p.get("noindex") else f'<link rel="canonical" href="{canon}">'}
<meta name="theme-color" content="#f6f4ef">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Built by Compo">
<meta property="og:title" content="{html.escape(p["title"])}">
<meta property="og:description" content="{html.escape(p["desc"])}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/img/og-2.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Built by Compo. Websites that work.">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="icon" href="icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="fonts/nunito.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="css/site.css">
{f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""}'''
    body = f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-head{" over" if name == "index.html" else ""}">
  <div class="wrap">
    <a class="logo" href="{home}" aria-label="Built by Compo, home">Built by <b>Compo</b></a>
    <button class="btn menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main"><canvas class="liquid" data-strength="0.3" aria-hidden="true"></canvas>{nav}<a class="btn" href="contact.html"{cur("contact.html")}>Let's talk</a></nav>
  </div>
</header>
<main id="main">{p["body"].replace("{HOME}", home)}</main>
<footer class="site-foot">
  <canvas class="liquid" data-strength="0.3" aria-hidden="true"></canvas>
  <div class="wrap">
    <div class="foot-hello">
      <p class="foot-label">Say hello</p>
      <a class="foot-email" href="mailto:{EMAIL}">{EMAIL}</a>
      <div class="row"><a class="btn hot" href="https://wa.me/{WA}" rel="noopener">Message me on WhatsApp {ARROW}</a></div>
    </div>
    <nav class="foot-pills" aria-label="Footer">
      {"".join(f'<a href="{h}">{t}</a>' for h, t in NAV)}<a href="contact.html">Contact</a>
    </nav>
    <a class="foot-logo" href="{home}" aria-label="Built by Compo, home">Built by Compo</a>
    <div class="foot-bar">
      <ul>
        <li><a href="privacy.html">Privacy policy</a></li>
        <li><a href="cookies.html">Cookie policy</a></li>
        <li><a href="terms.html">Terms and conditions</a></li>
        <li><a href="refunds.html">Refund policy</a></li>
        <li><button class="motion-link" type="button" aria-pressed="false">Pause animations</button></li>
      </ul>
      <p>© {YEAR} Built by Compo · Essex, England. Designed and built by me, obviously.</p>
    </div>
  </div>
</footer>
<script src="js/site.js"></script>
<script src="js/liquid.js"></script>'''
    if name == "404.html" and not preview: head = '<base href="/">\n' + head
    if preview == "bare":   # artifact main page: the publisher adds the outer skeleton
        return head.replace(p["title"], "Built by Compo Site", 1) + '\n<meta name="claude:viewport-fit-sides" content="cover">\n<script>document.documentElement.classList.add("no-js")</script>\n' + body
    return f'<!doctype html>\n<html lang="en-GB" class="no-js">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n'

def main():
    preview = "--preview" in sys.argv
    for name, p in PAGES.items():
        open(os.path.join(ROOT, name), "w", encoding="utf-8").write(page(name, p))
    urls = "".join(f"  <url><loc>{SITE}/{'' if n == 'index.html' else n.replace('.html', '')}</loc><lastmod>{YEAR}-11-12</lastmod></url>\n" for n, p in PAGES.items() if not p.get("noindex"))
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    if preview:
        d = os.path.join(ROOT, "_preview"); os.makedirs(d, exist_ok=True)
        for name, p in PAGES.items():
            out = page(name, p, preview="bare" if name == "index.html" else True)
            open(os.path.join(d, name), "w", encoding="utf-8").write(out)
    print("Built", len(PAGES), "pages")

if __name__ == "__main__":
    main()
