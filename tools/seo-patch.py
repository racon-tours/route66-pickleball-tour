#!/usr/bin/env python3
"""One-shot technical SEO patch for index.html / thanks.html. Idempotent."""
import re, pathlib, json
ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://route66pickleballtour.com"
GTM = "GTM-M5XQRL26"  # replaced by tools/set-gtm.sh

TITLE = "Route 66 Pickleball Tour 2027 | 10-Day Chicago–Santa Monica Trip"
DESC = ("A 10-day guided pickleball tour down Route 66 between Chicago and Santa Monica: "
        "ten court sessions, historic hotels, 32 players per departure. Sixteen 2027 departures.")

ld = [
 {"@context":"https://schema.org","@type":"Organization","@id":"https://pickle.tours/#org",
  "name":"Pickle Tours","legalName":"Nichols & Company dba Pickle Dot Tours",
  "url":"https://pickle.tours","logo":"https://pickle.tours/assets/favicon-512.png",
  "email":"hello@pickle.tours","telephone":"+1-888-774-3465",
  "address":{"@type":"PostalAddress","streetAddress":"4303 McPherson Ave","addressLocality":"St. Louis",
             "addressRegion":"MO","postalCode":"63108","addressCountry":"US"}},
 {"@context":"https://schema.org","@type":"WebSite","@id":SITE+"/#website","url":SITE+"/",
  "name":"Route 66 Pickleball Tour","publisher":{"@id":"https://pickle.tours/#org"},"inLanguage":"en-US"},
 {"@context":"https://schema.org","@type":"TouristTrip","@id":SITE+"/#trip","url":SITE+"/",
  "name":"Route 66 Pickleball Tour 2027",
  "description":"Ten-day guided motorcoach pickleball tour along Route 66 between Chicago and Santa Monica, "
                "with ten court sessions, historic hotels, club-pro coaching and a bracket championship. "
                "Runs both westbound and eastbound; sixteen departures March–October 2027.",
  "image":SITE+"/assets/route66-pickleball-tour-2027-badge.png",
  "touristType":["Pickleball players","Active adults","Road-trip travelers"],
  "provider":{"@id":"https://pickle.tours/#org"},
  "itinerary":{"@type":"ItemList","numberOfItems":8,"itemListElement":[
     {"@type":"ListItem","position":i+1,"item":{"@type":"City","name":n}} for i,n in enumerate([
        "Chicago, Illinois","St. Louis, Missouri","Grand Lake, Oklahoma","Amarillo, Texas",
        "Albuquerque, New Mexico","Flagstaff, Arizona","Coachella Valley, California","Santa Monica, California"])]},
  "subjectOf":{"@type":"WebPage","url":SITE+"/"},
  "offers":{"@type":"Offer","url":SITE+"/#waitlist","availability":"https://schema.org/PreOrder",
            "description":"Join the 2027 waitlist for first access to dates and pricing."}}
]
ld_tag = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(",",":")) + '</script>'

gtm_head = ('<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({\'gtm.start\':\n'
            'new Date().getTime(),event:\'gtm.js\'});var f=d.getElementsByTagName(s)[0],\n'
            'j=d.createElement(s),dl=l!=\'dataLayer\'?\'&l=\'+l:\'\';j.async=true;j.src=\n'
            '\'https://www.googletagmanager.com/gtm.js?id=\'+i+dl;f.parentNode.insertBefore(j,f);\n'
            '})(window,document,\'script\',\'dataLayer\',\'%s\');</script>\n<!-- End Google Tag Manager -->' % GTM)
gtm_body = ('<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=%s"\n'
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
            '<!-- End Google Tag Manager (noscript) -->' % GTM)

def strip(s):
    s = re.sub(r'<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->\n?', '', s, flags=re.S)
    s = re.sub(r'<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->\n?', '', s, flags=re.S)
    s = re.sub(r'<link rel="canonical"[^>]*>\n?', '', s)
    s = re.sub(r'<meta name="twitter:[^>]*>\n?', '', s)
    s = re.sub(r'<meta property="og:(url|site_name|image:alt)"[^>]*>\n?', '', s)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', s, flags=re.S)
    return s

# ---- index.html
p = ROOT/"index.html"; s = strip(p.read_text())
s = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', s, count=1)
s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', s, count=1)
s = s.replace('<meta property="og:image" content="/assets/route66-pickleball-tour-2027-badge.png">',
              f'<meta property="og:image" content="{SITE}/assets/route66-pickleball-tour-2027-badge.png">')
s = s.replace('<meta property="og:title" content="Route 66 Pickleball Tour — Pickle Tours">',
              f'<meta property="og:title" content="{TITLE}">')
s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{DESC}">', s, count=1)
extra = (f'<link rel="canonical" href="{SITE}/">\n'
         f'<meta property="og:url" content="{SITE}/">\n'
         '<meta property="og:site_name" content="Pickle Tours">\n'
         '<meta property="og:image:alt" content="Route 66 Pickleball Tour 2027 badge">\n'
         '<meta name="twitter:card" content="summary_large_image">\n'
         f'<meta name="twitter:title" content="{TITLE}">\n'
         f'<meta name="twitter:description" content="{DESC}">\n'
         f'<meta name="twitter:image" content="{SITE}/assets/route66-pickleball-tour-2027-badge.png">\n')
s = s.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="website">\n' + extra + ld_tag, 1)
s = s.replace('</head>', gtm_head + '\n</head>', 1)
s = s.replace('<body>', '<body>\n' + gtm_body, 1)
p.write_text(s)

# ---- thanks.html (noindex stays; GTM so the conversion fires)
p = ROOT/"thanks.html"; s = strip(p.read_text())
s = s.replace('</head>', gtm_head + '\n</head>', 1)
s = re.sub(r'<body([^>]*)>', lambda m: f'<body{m.group(1)}>\n' + gtm_body, s, count=1)
p.write_text(s)

(ROOT/"robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /thanks\nDisallow: /api/\n\nSitemap: {SITE}/sitemap.xml\n")
(ROOT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
  f'  <url><loc>{SITE}/</loc><changefreq>weekly</changefreq><priority>1.0</priority>\n'
  f'    <image:image><image:loc>{SITE}/assets/route66-pickleball-tour-2027-badge.png</image:loc><image:title>Route 66 Pickleball Tour 2027</image:title></image:image>\n'
  '  </url>\n</urlset>\n')
print("patched")
