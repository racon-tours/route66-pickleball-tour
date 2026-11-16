"""Build the Kimp-design home page for the sandbox from the current site's copy.
Usage: python3 build.py <old index.html> <new index.html>"""
import re, sys, html as H
old = open(sys.argv[1]).read()

def sect(sid):
    return re.search(r'<section[^>]*id="%s".*?</section>' % sid, old, re.S).group(0)

def inner(sec):  # contents of the first .wrap
    return re.search(r'<div class="wrap">(.*)</div>\s*</section>', sec, re.S).group(1)

head = old.split('<style>')[0]
head_tail = old.split('</style>', 1)[1].split('<body>')[0]
scripts = re.search(r'</footer>(.*)</body>', old, re.S).group(1)
# The new route cards use their own tab script; drop the old strip/tab script.
scripts = re.sub(r'<script>\s*\(function\(\)\{\s*/\* draw the route line.*?</script>', '', scripts, flags=re.S)

def stops(panel):
    p = re.search(r'id="%s".*?<div class="stops">(.*?)</div>\s*</div>\s*</div>' % panel, old, re.S).group(1)
    out = []
    for m in re.finditer(r'<div class="stop[^"]*">(.*?)</div>', p, re.S):
        b = m.group(1)
        g = lambda c: re.search(r'class="%s[^"]*"[^>]*>(.*?)</' % c, b, re.S).group(1).strip()
        href = re.search(r'href="([^"]+)"', b).group(1)
        out.append(dict(day=g('marker'), city=g('cap-city'), land=g('cap-landmark'),
                        detail=g('cap-detail'), play=g('cap-play'), href=href))
    return out

PHOTO = {'chicago': ('card-chicago.webp', 'center'), 'st-louis': ('card-stlouis.webp', 'center'),
         'grand-lake': ('card-grandlake.webp', 'center'), 'amarillo': ('vignette-ranch.webp', 'center'),
         'albuquerque': ('card-albuquerque.webp', 'center'), 'flagstaff': ('card-flagstaff.webp', 'center'),
         'la-quinta': ('vignette-bus.webp', 'center'), 'santa-monica': ('pier-sunset.webp', 'center 60%')}

def cards(lst):
    o = []
    for s in lst:
        slug = s['href'].rstrip('/').split('/')[-1]
        img, pos = PHOTO.get(slug, ('card-flagstaff.webp', 'center'))
        o.append(f'''        <a class="day-card" href="{s['href']}">
          <span class="day-photo"><img src="/assets/kimp/{img}" alt="" loading="lazy" style="object-position:{pos}"><span class="day-pill">{s['day']}</span></span>
          <span class="day-city">{s['city']}</span>
          <span class="day-title">{s['land']}</span>
          <span class="day-detail">{s['detail']}</span>
          <span class="day-tag">{s['play']}</span>
        </a>''')
    return '\n'.join(o)

def para(sec, cls=None):
    return re.findall(r'<p%s>(.*?)</p>' % (f' class="{cls}"' if cls else ''), sec, re.S)

route = sect('route'); country = sect('country'); tourn = sect('tournament'); comfort = sect('comfort')
season = sect('season'); book = sect('book'); live = sect('info-session'); faq = sect('faq'); wait = sect('waitlist')
idea = re.search(r'<section class="concept.*?</section>', old, re.S).group(0)
hero = re.search(r'<header class="hero".*?</header>', old, re.S).group(0)
stats = re.findall(r'<div class="stat[^"]*"><b>(.*?)</b><span>(.*?)</span>', old)
footer = re.search(r'<footer.*?</footer>', old, re.S).group(0)

def h2(sec): return re.search(r'<h2>(.*?)</h2>', sec, re.S).group(1)
def label(sec): return re.search(r'<span class="label">(.*?)</span>', sec, re.S).group(1)

halves = re.findall(r'<div class="half">\s*<h3>(.*?)</h3>(.*?)</div>', tourn, re.S)
comforts = re.findall(r'<div class="comfort-item">.*?<h3>(.*?)</h3>\s*<p>(.*?)</p>', comfort, re.S)
dl = re.findall(r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>', season, re.S)
season_p = re.search(r'<h2>.*?</h2>\s*<p>(.*?)</p>', season, re.S).group(1)
form = re.search(r'<form.*?</form>', wait, re.S).group(0)
hero_label = re.search(r'<p class="label">(.*?)</p>', hero, re.S).group(1)
hero_h1 = re.search(r'<h1>(.*?)</h1>', hero, re.S).group(1)
hero_lede = re.search(r'<p class="lede">(.*?)</p>', hero, re.S).group(1)
COMFORT_IMG = ['comfort-hotel.webp', 'comfort-coach.webp', 'card-albuquerque.webp']
STAT_COLOR = ['red', 'blue', 'red', 'blue']

css = open(sys.argv[3] if len(sys.argv) > 3 else 'kimp.css').read()

body = f'''<body>
<a class="skip" href="#main">Skip to content</a>
<nav class="topnav" aria-label="Main">
  <a class="brand" href="/" aria-label="Route 66 Pickleball Tour home"><img src="/assets/route66-pickleball-tour-logo.png" alt="" width="76" height="80"></a>
  <div class="menu">
    <a href="#route">The Route</a><a href="#country">The Country</a><a href="#tournament">The Pickleball</a><a href="#season">2027 Season</a><a href="#faq">FAQ</a>
  </div>
  <a class="pill red" href="#book">Book Now</a>
</nav>

<main id="main">
<header class="hero" id="top">
  <div class="hero-frame">
    <img class="hero-bg" src="/assets/kimp/hero.webp" alt="" fetchpriority="high">
    <div class="hero-inner">
      <img class="hero-badge" src="/assets/route66-pickleball-tour-logo.png" alt="Route 66 Pickleball Tour" width="160" height="176">
      <p class="eyebrow">{hero_label}</p>
      <h1>{hero_h1}</h1>
      <p class="hero-lede">{hero_lede}</p>
      <div class="hero-ctas"><a class="btn optic" href="#book">See dates &amp; book</a><a class="btn ghost" href="#waitlist">Get the brochure</a></div>
    </div>
  </div>
</header>

<div class="stats" aria-label="The tour at a glance">
{''.join(f'  <div class="stat"><b class="{STAT_COLOR[i]}">{n}</b><span>{t}</span></div>{chr(10)}' for i, (n, t) in enumerate(stats))}</div>

<section class="idea">
  <div class="wrap two">
    <div>
      <span class="script">{label(idea)}</span>
      <h2>{h2(idea)}</h2>
      {''.join(f'<p class="body-lg">{p}</p>' for p in para(idea))}
    </div>
    <div class="idea-art" aria-hidden="true">
      <img class="pier" src="/assets/kimp/pier-sign.webp" alt="" loading="lazy">
      <img class="coach" src="/assets/kimp/coach-boarding.webp" alt="" loading="lazy">
    </div>
  </div>
</section>

<section class="route" id="route">
  <div class="wrap">
    <div class="two route-head">
      <div><span class="script">{label(route)}</span><h2>{h2(route)}</h2></div>
      <p class="body-lg">{para(route)[0]}</p>
    </div>
    <div class="dir-toggle" role="tablist" aria-label="Choose a direction">
      <button role="tab" id="tab-wb" aria-controls="cards-wb" aria-selected="true"><b>Westbound</b><span>Chicago to Santa Monica</span></button>
      <button role="tab" id="tab-eb" aria-controls="cards-eb" aria-selected="false" tabindex="-1"><b>Eastbound</b><span>Santa Monica to Chicago</span></button>
    </div>
  </div>
  <div class="road" aria-hidden="true"><div class="bus"><img src="/assets/kimp/bus-top.webp" alt=""><span id="bus-day">Day 1</span></div></div>
  <div class="cards" id="cards-wb" role="tabpanel" aria-labelledby="tab-wb" tabindex="0">
{cards(stops('panel-wb'))}
  </div>
  <div class="cards" id="cards-eb" role="tabpanel" aria-labelledby="tab-eb" tabindex="0" hidden>
{cards(stops('panel-eb'))}
  </div>
  <p class="wrap scroll-hint">&larr; Scroll for every stop &rarr; &nbsp;Tap a card for that city&rsquo;s neighborhood guide.</p>
</section>

<section class="country" id="country">
  <img class="vig vig-l" src="/assets/kimp/vignette-ranch.webp" alt="" loading="lazy">
  <img class="vig vig-r" src="/assets/kimp/vignette-bus.webp" alt="" loading="lazy">
  <div class="wrap center">
    <span class="script">{label(country)}</span>
    <p class="passage">{para(country, 'passage')[0]}</p>
    <p class="kicker">{para(country, 'kicker')[0]}</p>
    <img class="quarry" src="/assets/kimp/quarry.webp" alt="" loading="lazy">
  </div>
</section>

<section class="tourn" id="tournament">
  <div class="wrap">
    <img class="paddles" src="/assets/kimp/paddles.webp" alt="" loading="lazy">
    <span class="script">{label(tourn)}</span>
    <h2>{h2(tourn)}</h2>
    <div class="notes">
{''.join(f'      <article class="note n{i+1}"><span class="num">0{i+1}</span><h3>{t}</h3>{b}</article>{chr(10)}' for i, (t, b) in enumerate(halves))}    </div>
  </div>
</section>

<section class="comfort" id="comfort">
  <div class="wrap center">
    <span class="script">{label(comfort)}</span>
    <h2>{h2(comfort)}</h2>
    <div class="comforts">
{''.join(f'      <article class="c-card"><img src="/assets/kimp/{COMFORT_IMG[i]}" alt="" loading="lazy"><h3>{t}</h3><p>{p}</p></article>{chr(10)}' for i, (t, p) in enumerate(comforts))}    </div>
  </div>
</section>

<section class="season" id="season">
  <div class="wrap">
    <div class="two route-head">
      <div><span class="script">{label(season)}</span><h2>{h2(season)}</h2></div>
      <p class="body-lg">{season_p}</p>
    </div>
    <dl class="facts">
{''.join(f'      <div><dt>{a}</dt><dd>{b}</dd></div>{chr(10)}' for a, b in dl)}    </dl>
  </div>
</section>

<section class="book" id="book">
  <div class="wrap">
{inner(book).replace('<span class="label">', '<span class="script">')}
  </div>
</section>

<section class="live" id="info-session">
  <div class="wrap">
{inner(live).replace('<span class="label">', '<span class="script">')}
  </div>
</section>

<section class="faq" id="faq">
  <div class="wrap">
{inner(faq).replace('<span class="label">', '<span class="script">')}
  </div>
</section>

<section class="waitlist" id="waitlist">
  <img class="wl-l" src="/assets/kimp/canyon.webp" alt="" loading="lazy">
  <img class="wl-r" src="/assets/kimp/pier-sunset.webp" alt="" loading="lazy">
  <div class="wrap center">
    <span class="script">{label(wait)}</span>
    <h2>{h2(wait)}</h2>
    <p class="body-lg">{re.search(r'<p class="lede">(.*?)</p>', wait, re.S).group(1)}</p>
    <div class="form-card">
{form}
    </div>
  </div>
</section>
</main>

{footer}
<script>
  /* Westbound / eastbound cards */
  (function(){{
    var tabs=[].slice.call(document.querySelectorAll('.dir-toggle [role=tab]'));
    function sel(t,focus){{tabs.forEach(function(x){{var on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;
      document.getElementById(x.getAttribute('aria-controls')).hidden=!on}});if(focus)t.focus()}}
    tabs.forEach(function(t,i){{t.addEventListener('click',function(){{sel(t)}});
      t.addEventListener('keydown',function(e){{var d=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(d){{e.preventDefault();sel(tabs[(i+d+tabs.length)%tabs.length],true)}}}})}});
    /* the bus label follows the first card in view */
    var lab=document.getElementById('bus-day');
    [].forEach.call(document.querySelectorAll('.cards'),function(c){{c.addEventListener('scroll',function(){{
      var cs=c.querySelectorAll('.day-card'),best=cs[0];for(var k=0;k<cs.length;k++){{if(cs[k].offsetLeft-c.scrollLeft>-80){{best=cs[k];break}}}}
      lab.textContent=best.querySelector('.day-pill').textContent}},{{passive:true}})}});
  }})();
</script>
{scripts}
</body>
</html>
'''
page = head + '<style>\n' + css + '\n</style>' + head_tail + body
open(sys.argv[2], 'w').write(page)
print('written', len(page))
