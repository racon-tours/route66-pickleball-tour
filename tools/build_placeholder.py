#!/usr/bin/env python3
"""Build the one-screen waitlist placeholder (index.html) from the full home page.

The full page is kept as tools/full-home.html so the sandbox and the eventual relaunch
start from it. Run from the repo root:  git show 168e083:index.html > /tmp/full.html && python3 tools/build_placeholder.py /tmp/full.html
"""
import re, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
import sys
full = pathlib.Path(sys.argv[1]).read_text()

head, body = full.split("<body>", 1)

def grab(pattern):
    m = re.search(pattern, body, re.S)
    if not m:
        raise SystemExit(f"missing block: {pattern}")
    return m.group(0)

gtm_ns   = grab(r"<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->")
waitlist = grab(r'<section class="waitlist" id="waitlist">.*?</section>')
footer   = grab(r'<footer class="pdt-foot">.*?</footer>')
club_js  = grab(r"<script>\s*/\* Club short links.*?</script>")

extra_css = """
  /* ---------- placeholder ---------- */
  .ph-hero{min-height:auto;padding:4rem 0 3rem}
  .ph-hero .badge{max-width:220px;height:auto;margin:0 auto 1.6rem;display:block}
  .ph-top{display:flex;justify-content:center;padding:1.2rem 0;background:var(--chalk)}
  .ph-top img{height:40px;width:auto}
</style>"""
head = head.replace("</style>", extra_css, 1)

page = f"""{head}<body>
{gtm_ns}

<div class="ph-top"><img src="/assets/pdt-wordmark-green.png" alt="Pickle Dot Tours" width="640" height="163"></div>

<header class="hero ph-hero" id="top">
  <div class="kitchen-line kl-left" aria-hidden="true"></div>
  <div class="kitchen-line kl-right" aria-hidden="true"></div>
  <div class="hero-inner">
    <img class="badge" src="/assets/route66-pickleball-tour-logo.png" alt="Route 66 Pickleball Tour" width="804" height="883">
    <p class="label">Chicago &#8644; Santa Monica &middot; 16 departures in 2027</p>
    <h1>7 days on the road.<br>4 days in paradise.</h1>
    <p class="lede">The Great American Pickleball Road Trip: eleven days by motorcoach from the BEGIN sign in Chicago
      to the end of the Santa Monica Pier, with courts booked for our group most mornings.
      512 player seats in 2027, and there will not be more.</p>
    <a class="btn" href="#waitlist">Join the waitlist</a>
  </div>
</header>

{waitlist}

{footer}

{club_js}
</body>
</html>
"""
(root / "index.html").write_text(page)
print("index.html written", len(page), "bytes")
