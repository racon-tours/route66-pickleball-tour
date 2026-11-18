"""Live site, Mike 18 Nov 2026: only two calls to action until tickets go on sale —
join the email list (hear when tickets go on sale) and join an info session.
No booking link, no brochure (sandbox-only until finished), no separate news signup."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent

def sub(s, old, new, count=1, regex=False):
    n = len(re.findall(old, s, re.S)) if regex else s.count(old)
    assert n >= 1, f'not found: {old[:60]}'
    return re.sub(old, new, s, count=count, flags=re.S) if regex else s.replace(old, new, count)

p = root / 'index.html'; s = p.read_text()
s = sub(s, r'<p class="ph-ctas">.*?</p>',
        '<p class="ph-ctas"><a class="btn" href="#waitlist">Get notified when tickets go on sale</a> '
        '<a class="btn" href="https://pickle.tours/webinars/info-session">Join an info session</a></p>', regex=True)
s = sub(s, r'<section class="waitlist" id="brochure"><span id="waitlist"></span>.*?</section>', '''<section class="waitlist" id="waitlist">
  <div class="wrap">
    <span class="label">Tickets aren&rsquo;t on sale yet</span>
    <h2>Be first in line.</h2>
    <p class="lede">Join the list and we&rsquo;ll email you before 2027 departures go on sale.
      No deposit, no obligation.</p>
    <form name="waitlist" method="POST" action="/api/waitlist" data-lead="waitlist">
      <input type="hidden" name="kind" value="waitlist">
      <p style="display:none"><label>Don't fill this out: <input name="bot-field"></label></p>
      <input type="hidden" name="club" id="club-code" value="">
      <div class="field">
        <label for="email">Email</label>
        <input id="email" name="email" type="email" autocomplete="email" required>
      </div>
      <button class="btn" type="submit">Notify me</button>
      <p class="fine">We&rsquo;ll only email you about the tour. Unsubscribe anytime.</p>
    </form>
    <p class="fine" style="margin-top:1.6rem">Questions first? <a href="https://pickle.tours/webinars/info-session">Join a free Tuesday info session</a>.</p>
  </div>
</section>''', regex=True)
s = sub(s, r'<div class="news-foot">.*?</form></div>\s*', '', regex=True)
p.write_text(s)

p = root / 'thanks.html'; s = p.read_text()
s = sub(s, '<p class="body">Every 2027 departure is on sale now. Ready to pick a date, or want to talk it through first?</p>',
        '<p class="body">Want to talk it through first? Join us for a free info session, live every Tuesday.</p>')
s = sub(s, '<a class="btn" href="https://pickletours.touramigo.com/">Book now</a> ', '')
s = sub(s, '<p class="body" id="t-news" hidden>',
        '<p class="body" id="t-waitlist" hidden>You&rsquo;re on the list. We&rsquo;ll email you before 2027 departures go on sale.</p>\n    <p class="body" id="t-news" hidden>')
s = sub(s, "if(w==='news'){",
        "if(w==='waitlist'){document.getElementById('t-brochure').hidden=true;document.getElementById('t-waitlist').hidden=false;"
        "document.getElementById('t-label').textContent=\"You're in\";document.getElementById('t-head').textContent=\"You\\u2019re on the list.\"}\n    if(w==='news'){")
p.write_text(s)

p = root / 'confirmed.html'; s = p.read_text()
s = sub(s, r'<p class="body">Every 2027 Route 66 departure is on sale now\..*?</p>',
        '<p class="body">Tickets for 2027 aren&rsquo;t on sale yet; we&rsquo;ll email you before they are. '
        'Questions in the meantime? <a href="https://pickle.tours/webinars/info-session">Join a Tuesday info session</a>.</p>', regex=True)
p.write_text(s)

p = root / 'netlify/functions/waitlist.mts'; s = p.read_text()
s = sub(s, 'const kind = clean(form.get("kind"), 20) === "news" ? "news" : "brochure";',
        'const rawKind = clean(form.get("kind"), 20);\n'
        '  // waitlist (live home page): same Prospective Guests group, but the thanks page says "on the list", not "brochure".\n'
        '  const kind = rawKind === "news" ? "news" : rawKind === "waitlist" ? "waitlist" : "brochure";')
s = sub(s, '...(kind === "brochure" ? [groupId] : []),', '...(kind !== "news" ? [groupId] : []),')
s = sub(s, 'const forWhat = kind === "news" ? "news" : wantsNews ? "both" : "brochure";',
        'const forWhat = kind === "news" ? "news" : kind === "waitlist" ? (wantsNews ? "both" : "waitlist") : wantsNews ? "both" : "brochure";')
p.write_text(s)
print('ok')
