#!/usr/bin/env python3
"""Build the city guides (/cities/<slug>), /westbound, /eastbound and /faq from tools/pages_data.py.

The look comes from index.html: its <style> block, nav, footer and analytics tag are reused, so
the new pages always match the home page. Run from the repo root:

    python3 tools/build_pages.py

Then commit the generated .html files with the data change. sitemap.xml is rewritten too.
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pages_data as D  # noqa: E402

SITE = "https://route66pickleballtour.com"
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
BASE_CSS = re.search(r"<style>(.*?)</style>", INDEX, re.S).group(1)
GTM_HEAD = re.search(r"<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->", INDEX, re.S).group(0)
GTM_BODY = re.search(r"<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->", INDEX, re.S).group(0)
FOOTER = re.search(r'<footer class="pdt-foot">.*?</footer>', INDEX, re.S).group(0)
ORG = {"@type": "Organization", "@id": "https://pickle.tours/#org", "name": "Pickle Dot Tours", "url": "https://pickle.tours"}
SHARE_IMG = SITE + "/assets/route66-pickleball-tour-2027-badge.png"
BY_SLUG = {c["slug"]: c for c in D.CITIES}

e = lambda s: html.escape(s, quote=True)

EXTRA_CSS = """
  .sub-hero{background:var(--green);color:var(--chalk);padding:4rem 0 3.6rem;position:relative}
  .sub-hero .label{color:var(--chalk)}
  .sub-hero h1{color:var(--optic);font-weight:400;margin-bottom:.6rem}
  .sub-hero .state{font-family:'Barlow Condensed',sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:.16em;font-size:1.1rem;margin-bottom:1.4rem;display:block}
  .sub-hero .lede{max-width:44rem;color:var(--chalk)}
  .crumbs{font-family:'Barlow Condensed',sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:.12em;font-size:.95rem;margin-bottom:1.2rem}
  .crumbs a{color:var(--chalk)}
  .guide{padding:3.5rem 0}
  .guide .wrap{max-width:880px}
  .stay{display:grid;grid-template-columns:1fr 1fr;gap:1.6rem;margin-bottom:3rem}
  .card{background:#FFFFFF;border:3px solid var(--green);padding:1.3rem 1.4rem}
  .card h3{font-size:1.2rem;color:var(--green);margin-bottom:.35rem}
  .card .where{font-family:'Barlow Condensed',sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:.95rem;color:var(--clay);display:block;margin-bottom:.4rem}
  .card p{font-size:16px;line-height:1.6;margin:0}
  .when dl div{display:grid;grid-template-columns:7.5rem 1fr;gap:.6rem;padding:.35rem 0;border-top:1px solid var(--rule)}
  .when dl div:first-child{border-top:none}
  .when dt{font-family:'Barlow Condensed',sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:.95rem;color:var(--clay)}
  .when dd{font-size:15.5px;line-height:1.55}
  @media(max-width:720px){.stay{grid-template-columns:1fr}}
  .photos{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:0 0 3rem}
  .ph-slot{aspect-ratio:4/3;border:2px dashed var(--muted);display:flex;align-items:center;justify-content:center;text-align:center;padding:1rem;font-family:'Barlow Condensed',sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:.1em;font-size:.9rem;color:var(--muted);background:#FFFFFF}
  @media(max-width:720px){.photos{grid-template-columns:1fr}}
  .picks{margin-bottom:2.6rem}
  .picks h2{font-size:clamp(1.5rem,3vw,1.9rem);border-top:3px solid var(--green);padding-top:1rem;margin-bottom:1rem}
  .pick{padding:.9rem 0;border-bottom:1px solid var(--rule)}
  .pick h3{font-size:1.15rem;color:var(--ink);margin-bottom:.15rem;font-family:'Merriweather',Georgia,serif;font-weight:700}
  .pick .where{font-family:'Barlow Condensed',sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:.1em;font-size:.92rem;color:var(--clay);display:block;margin-bottom:.25rem}
  .pick p{font-size:16.5px;line-height:1.65;margin:0}
  .tips{background:#FFFFFF;border-left:6px solid var(--optic);padding:1.2rem 1.4rem;margin:2rem 0}
  .tips h2{font-size:1.3rem;margin-bottom:.6rem}
  .tips li{margin:.3rem 0 .3rem 1.1rem;font-size:16.5px}
  .checked{font-size:15px;color:var(--muted);font-style:italic}
  .pager{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;border-top:3px solid var(--green);padding-top:1.2rem;margin-top:2.6rem}
  .pager a{font-family:'Barlow Condensed',sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:.1em;text-decoration:none;color:var(--green)}
  .pager a:hover{color:var(--clay)}
  .cta-band{background:var(--green);color:var(--chalk);padding:3rem 0;text-align:center}
  .cta-band h2{color:var(--chalk)}
  .cta-band p{max-width:36rem;margin:0 auto 1.6rem}
  .cta-band .btn{margin:.3rem}
  .days{list-style:none}
  .day{display:grid;grid-template-columns:8.5rem 1fr;gap:1.4rem;padding:1.6rem 0;border-top:1px solid var(--rule)}
  .day:first-child{border-top:3px solid var(--green)}
  .day .marker{font-family:'Barlow Condensed',sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:.1em;background:var(--green);color:var(--chalk);padding:.2rem .6rem;display:inline-block}
  .day .wd{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:.1em;font-size:.9rem;color:var(--muted);margin-top:.4rem}
  .day .city{font-family:'Barlow Condensed',sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:.14em;font-size:1rem}
  .day .landmark{font-family:'Yesteryear',cursive;font-size:30px;line-height:1.15;color:var(--green);display:block;margin:.1rem 0 .4rem}
  .day p{font-size:16.5px;line-height:1.65;margin:0 0 .5rem}
  .day .play{font-family:'Barlow Condensed',sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:.9rem;color:var(--clay)}
  .day ul{margin:.5rem 0 0 1.1rem;font-size:15.5px;color:var(--ink)}
  .day .guide-link{font-family:'Barlow Condensed',sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:.08em;font-size:.95rem;color:var(--green)}
  @media(max-width:620px){.day{grid-template-columns:1fr;gap:.6rem}}
"""


def nav():
    return """<nav>
  <div class="nav-inner">
    <a class="wordmark" href="/">
      <img class="pdt-head" src="/assets/pdt-wordmark-green.png" alt="Pickle Dot Tours" width="640" height="163">
    </a>
    <div class="nav-links">
      <a href="/#route">The Route</a>
      <a href="/westbound">Westbound</a>
      <a href="/eastbound">Eastbound</a>
      <a href="/faq">FAQ</a>
      <a class="btn small clay" href="/#waitlist">Join the Waitlist</a>
    </div>
  </div>
</nav>"""


def page(path, title, desc, body, jsonld, fonts=""):
    url = SITE + path
    font_link = f'<link href="https://fonts.googleapis.com/css2?family={fonts}&display=swap" rel="stylesheet">\n' if fonts else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32">
<link rel="icon" href="/assets/favicon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/favicon-180.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pickle Dot Tours">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SHARE_IMG}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SHARE_IMG}">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Barlow+Condensed:wght@600;700&family=Merriweather:ital,wght@0,400;0,700;1,400&family=Yesteryear&display=swap" rel="stylesheet">
{font_link}<style>{BASE_CSS}{EXTRA_CSS}</style>
{GTM_HEAD}
</head>
<body>
{GTM_BODY}
{nav()}
{body}
{FOOTER}
</body>
</html>
"""


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}


def cta():
    return """<section class="cta-band">
  <div class="wrap">
    <h2>Eleven days, Chicago to the Pacific.</h2>
    <p>Ten pickleball sessions, historic hotels and the whole of Route 66. Waitlist members hear the dates first.</p>
    <a class="btn" href="/#waitlist">Join the 2027 waitlist</a>
    <a class="btn clay" href="/#info-session">Join a Tuesday info session</a>
  </div>
</section>"""


def city_page(c, i):
    path = f"/cities/{c['slug']}"
    fam = c["font"].replace(" ", "+")
    when = "".join(f"<div><dt>{e(d)}</dt><dd>{e(t)}</dd></div>" for d, t in c["when"])
    hotels = "".join(f"""<div class="card"><span class="where">Your hotel</span><h3>{e(n)}</h3>
      <p><b>{e(a)}</b></p><p>{e(w)}</p></div>""" for n, a, w in c["hotels"])
    sections = ""
    for head, picks in c["sections"]:
        items = "".join(f"""<div class="pick"><h3>{e(n)}</h3><span class="where">{e(w)}</span><p>{e(why)}</p></div>"""
                        for n, w, why in picks)
        sections += f'<div class="picks"><h2>{e(head)}</h2>{items}</div>\n'
    tips = "".join(f"<li>{e(t)}</li>" for t in c["tips"])
    slots = "".join(f'<div class="ph-slot" data-photo="{c["slug"]}-{k}">Photo to choose: {lbl}</div>'
                    for k, lbl in (("hotel", "the hotel"), ("neighborhood", "the neighborhood"), ("landmark", "a Route 66 landmark")))
    prev_c = D.CITIES[i - 1] if i > 0 else None
    next_c = D.CITIES[i + 1] if i + 1 < len(D.CITIES) else None
    pager = '<div class="pager">'
    pager += f'<a href="/cities/{prev_c["slug"]}">&larr; {e(prev_c["name"])}</a>' if prev_c else '<a href="/westbound">&larr; Westbound day by day</a>'
    pager += f'<a href="/cities/{next_c["slug"]}">{e(next_c["name"])} &rarr;</a>' if next_c else '<a href="/eastbound">Eastbound day by day &rarr;</a>'
    pager += "</div>"
    body = f"""<header class="sub-hero">
  <div class="wrap">
    <p class="crumbs"><a href="/">Route 66 Pickleball Tour</a> &rsaquo; City guides</p>
    <h1 style="font-family:'{c['font']}',cursive">{e(c['name'])}</h1>
    <span class="state">{e(c['state'])}</span>
    <p class="lede">{e(c['intro'])}</p>
  </div>
</header>
<section class="guide">
  <div class="wrap">
    <div class="stay">
      {hotels}
      <div class="card when"><span class="where">When we're here</span><dl>{when}</dl></div>
    </div>
    <div class="photos">{slots}</div>
{sections}
    <div class="tips"><h2>Good to know</h2><ul>{tips}</ul></div>
    <p class="checked">Picks checked {D.CHECKED}. Hours change, so call ahead or ask the front desk. Dinner and drinks are on you; breakfast and lunch are on the tour.</p>
    {pager}
  </div>
</section>
{cta()}"""
    ld = [crumbs([("Route 66 Pickleball Tour", "/"), (c["name"], path)]),
          {"@context": "https://schema.org", "@type": "WebPage", "url": SITE + path, "name": c["title"],
           "about": {"@type": "City", "name": f"{c['name']}, {c['state']}"}, "publisher": ORG}]
    return path, page(path, c["title"], c["desc"], body, ld, fonts=fam)


def direction_page(key, days, other):
    nice = "Westbound" if key == "westbound" else "Eastbound"
    route = "Chicago to Santa Monica" if key == "westbound" else "Santa Monica to Chicago"
    path = f"/{key}"
    title = f"{nice} Route 66 Pickleball Tour: {route} day by day"
    desc = f"The 11-day {nice.lower()} Route 66 Pickleball Tour, {route}, day by day: where we sleep, where we play and the Route 66 landmarks along the way."
    items = ""
    for day, wd, slug, landmark, what, play, along in days:
        if slug:
            c = BY_SLUG[slug]
            city = f'<span class="city">{e(c["name"])}, {e(c["state"])}</span>'
            link = f'<a class="guide-link" href="/cities/{slug}">{e(c["name"])} guide: where to eat and what to do &rarr;</a>'
        else:
            city, link = '<span class="city">Fly home</span>', ""
        al = ("<ul>" + "".join(f"<li>{e(a)}</li>" for a in along) + "</ul>") if along else ""
        items += f"""<li class="day"><div><span class="marker">{e(day)}</span><span class="wd">{e(wd)}</span></div>
  <div>{city}<span class="landmark">{e(landmark)}</span><p>{e(what)}</p><span class="play">{e(play)}</span>{al}<p style="margin-top:.6rem">{link}</p></div></li>\n"""
    body = f"""<header class="sub-hero">
  <div class="wrap">
    <p class="crumbs"><a href="/">Route 66 Pickleball Tour</a> &rsaquo; {nice}</p>
    <h1>{nice}</h1>
    <span class="state">{route} &middot; 11 days, 10 nights</span>
    <p class="lede">The same tour as the {other} run, in the other direction: same resorts, same landmarks, ten morning sessions. Here's how the days fall.</p>
  </div>
</header>
<section class="guide">
  <div class="wrap">
    <ol class="days">
{items}    </ol>
    <p class="checked">Exact stops and times are in the route book every guest receives before departure. Landmarks along the way can change with road conditions.</p>
    <div class="pager"><a href="/">&larr; The tour</a><a href="/{other}">{other.capitalize()} day by day &rarr;</a></div>
  </div>
</section>
{cta()}"""
    ld = [crumbs([("Route 66 Pickleball Tour", "/"), (nice, path)]),
          {"@context": "https://schema.org", "@type": "TouristTrip", "name": title, "url": SITE + path, "provider": ORG,
           "itinerary": {"@type": "ItemList", "itemListElement": [
               {"@type": "ListItem", "position": n + 1, "item": {"@type": "City", "name": f'{BY_SLUG[d[2]]["name"]}, {BY_SLUG[d[2]]["state"]}'}}
               for n, d in enumerate([x for x in days if x[2]])]}}]
    return path, page(path, title, desc, body, ld)


def faq_page():
    path = "/faq"
    title = "Route 66 Pickleball Tour FAQ: levels, what's included, booking and travel"
    desc = "Answers to common questions about the Route 66 Pickleball Tour: skill level, partners, what's included, hotels, deposits, airports and luggage."
    groups, qa = "", []
    for g, items in D.FAQ:
        groups += f'<div class="faq-group"><h3>{e(g)}</h3>'
        for q, a in items:
            groups += f"<details><summary>{e(q)}</summary><p>{a}</p></details>"
            qa.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}})
        groups += "</div>\n"
    body = f"""<header class="sub-hero">
  <div class="wrap">
    <p class="crumbs"><a href="/">Route 66 Pickleball Tour</a> &rsaquo; FAQ</p>
    <h1>Before you ask.</h1>
    <p class="lede">Everything people ask us about the tour. Still wondering? Call or text 1-888-774-DINK, or bring your question to a Tuesday info session.</p>
  </div>
</header>
<section class="faq">
  <div class="wrap">
{groups}  </div>
</section>
{cta()}"""
    ld = [crumbs([("Route 66 Pickleball Tour", "/"), ("FAQ", path)]),
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qa}]
    return path, page(path, title, desc, body, ld)


def write(path, content):
    f = ROOT / (path.lstrip("/") + ".html")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content, encoding="utf-8")
    return path


def sitemap(paths):
    home = re.search(r"<url><loc>https://route66pickleballtour.com/</loc>.*?</url>",
                     (ROOT / "sitemap.xml").read_text(encoding="utf-8"), re.S).group(0)
    urls = "\n".join(f"  <url><loc>{SITE}{p}</loc><changefreq>monthly</changefreq><priority>{'0.8' if p in ('/westbound', '/eastbound') else '0.7'}</priority></url>" for p in paths)
    (ROOT / "sitemap.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  {home}
{urls}
</urlset>
""", encoding="utf-8")


if __name__ == "__main__":
    built = [write(*direction_page("westbound", D.WESTBOUND, "eastbound")),
             write(*direction_page("eastbound", D.EASTBOUND, "westbound")),
             write(*faq_page())]
    built += [write(*city_page(c, i)) for i, c in enumerate(D.CITIES)]
    sitemap(built)
    print("built", len(built), "pages:", ", ".join(built))
