/** HTML for club pages, previews and the registration flow. Brand: Guide v1.3 tokens. */
import { ClubRecord, esc, discountText, CODE_SUFFIX, TERMS_VERSION, normCodePrefix } from "./clubs.mts";

const FONTS = `<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Barlow+Condensed:wght@600;700&family=Merriweather:ital,wght@0,400;0,700;1,400&family=Yesteryear&display=swap" rel="stylesheet">`;

const GTM_HEAD = `<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-M5XQRL26');</script>`;

const CSS = `
:root{--green:#04421D;--green-line:#1C6234;--optic:#E7FB20;--blue:#30BCED;--orange:#FC5130;--white:#FFFAFF;
--chalk:#F7F5EE;--ink:#14211F;--muted:#6B7A70;--rule:#DBD7CA}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--chalk);color:var(--ink);font:400 18px/1.75 Merriweather,Georgia,serif}
a{color:var(--green)}
.label{font:700 .95rem/1.4 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.14em}
h1,h2{font-family:'Alfa Slab One',serif;font-weight:400;line-height:1.1;margin:.2em 0 .4em}
.script{font-family:Yesteryear,cursive;font-size:clamp(28px,4vw,40px);color:var(--optic);line-height:1}
.wrap{max-width:62rem;margin:0 auto;padding:0 16px}
.notice{background:var(--orange);color:var(--white);text-align:center;padding:.7rem 16px;font:700 1rem/1.4 'Barlow Condensed',sans-serif;letter-spacing:.06em;text-transform:uppercase}
.hero{position:relative;color:var(--white);background:var(--green) url(/assets/img/route66-sign-flagstaff-1200.webp) center/cover;}
.hero::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,66,29,.82),rgba(4,66,29,.95))}
.hero .wrap{position:relative;padding:3rem 16px 3.5rem;display:grid;gap:1.6rem}
.marks{display:flex;align-items:center;gap:1.2rem;flex-wrap:wrap}
.marks img{height:96px;width:auto}
.clublogo{height:96px;max-width:200px;object-fit:contain;background:var(--white);padding:8px;border-radius:6px}
.monogram{height:96px;min-width:96px;padding:0 14px;display:grid;place-items:center;background:var(--white);color:var(--green);border-radius:6px;font:400 2rem 'Alfa Slab One',serif}
.x{font:700 1.6rem 'Barlow Condensed';color:var(--optic)}
.hero h1{font-size:clamp(2rem,5.5vw,3.6rem);margin:0}
.hero p{max-width:40rem;margin:0}
.codebox{display:inline-grid;gap:.2rem;background:var(--optic);color:var(--green);padding:1rem 1.4rem;box-shadow:5px 5px 0 var(--ink);justify-self:start}
.codebox b{font:400 clamp(2rem,6vw,3rem)/1 'Alfa Slab One',serif;letter-spacing:.04em}
section{padding:3rem 0;border-bottom:1px solid var(--rule)}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(13rem,1fr));gap:1rem;margin-top:1.4rem}
.fact{background:var(--white);border:2px solid var(--green);padding:1rem 1.2rem}
.fact .label{color:var(--green)}
.btn{display:inline-block;font:700 1.05rem/1 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.12em;text-decoration:none;border:0;cursor:pointer;
background:var(--optic);color:var(--green);padding:1rem 1.8rem;box-shadow:4px 4px 0 var(--ink)}
.btn.dark{background:var(--green);color:var(--optic)}
.btn:disabled{opacity:.45;cursor:not-allowed}
form.stack{display:grid;gap:1rem;max-width:36rem}
input[type=text],input[type=email]{width:100%;font:400 1rem Merriweather,serif;padding:.75rem .9rem;border:2px solid var(--green);background:var(--white)}
.field{display:grid;gap:.35rem}
.hint{font-size:15px;color:var(--muted);margin:0}
.ok{color:var(--green-line);font-weight:700}.bad{color:#B3261E;font-weight:700}
.step{background:var(--white);border-left:6px solid var(--optic);padding:1.4rem 1.4rem 1.6rem;margin:1.2rem 0;box-shadow:0 1px 0 var(--rule)}
.step h2{font-size:1.5rem}
.prefix{display:flex;align-items:stretch;flex-wrap:wrap}.prefix input{flex:1 1 10rem;min-width:0;width:auto}.prefix span{display:flex;align-items:center;padding:.5rem .7rem;background:var(--green);color:var(--white);font:700 1rem 'Barlow Condensed';overflow-wrap:anywhere}
h1,h2,p,label{overflow-wrap:break-word}
.check{display:flex;gap:.7rem;align-items:flex-start}.check input{margin-top:.45rem;width:20px;height:20px;flex:none}
footer{padding:2rem 0 3rem;font-size:15px;color:var(--muted)}
@media(max-width:600px){.marks img,.clublogo,.monogram{height:72px}.hero .wrap{padding:2rem 16px 2.6rem}}
`;

function shell(title: string, body: string, opts: { noindex?: boolean; desc?: string } = {}) {
  return `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>${opts.desc ? `<meta name="description" content="${esc(opts.desc)}">` : ""}
${opts.noindex ? '<meta name="robots" content="noindex,nofollow">' : ""}
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="/assets/favicon-180.png">
${FONTS}<style>${CSS}</style>${GTM_HEAD}</head><body>${body}</body></html>`;
}

function clubMark(c: ClubRecord) {
  if (c.logo_url) return `<img class="clublogo" src="${esc(c.logo_url)}" alt="${esc(c.club_name)} logo">`;
  const initials = c.club_name.split(/\s+/).filter((w) => /^[A-Za-z0-9]/.test(w) && !/^(the|of|and|club|pickleball)$/i.test(w)).map((w) => w[0]).join("").slice(0, 3).toUpperCase() || "PB";
  return `<span class="monogram" aria-hidden="true">${esc(initials)}</span>`;
}

const FOOT = `<footer><div class="wrap">Tours are sold and operated by Nichols &amp; Company dba Pickle Dot Tours, 4303 McPherson Ave, St. Louis MO 63108 ·
<a href="https://pickle.tours/terms">Terms</a> · <a href="https://pickle.tours/privacy">Privacy</a> · 1-888-774-DINK</div></footer>`;

/** The club's landing page. mode=preview adds a not-public banner and swaps the form for a note. */
export function clubPage(c: ClubRecord, mode: "live" | "preview", joinHref?: string) {
  const code = c.registration?.code ?? c.suggested_code;
  const name = esc(c.club_name);
  const banner = mode === "preview"
    ? `<div class="notice">Private preview for ${name} — not public. ${joinHref ? `<a style="color:var(--optic)" href="${esc(joinHref)}">Finish sign-up to make it live →</a>` : ""}</div>` : "";
  const form = mode === "live"
    ? `<form class="stack" method="POST" action="/api/waitlist">
        <input type="hidden" name="club" value="${esc(code)}">
        <p style="display:none"><label>Leave blank <input name="bot-field"></label></p>
        <div class="field"><label class="label" for="email">Email</label><input type="email" id="email" name="email" required autocomplete="email"></div>
        <button class="btn dark" type="submit">Hold my club rate</button>
        <p class="hint">We'll email you the 2027 departures and remind you to use ${esc(code)} when booking opens.</p>
      </form>`
    : `<p class="hint">(Members will sign up here for departure dates and booking-day reminders.)</p>`;
  const body = `${banner}
<header class="hero"><div class="wrap">
  <div class="marks">${clubMark(c)}<span class="x">×</span><img src="/assets/route66-pickleball-tour-logo.png" alt="Route 66 Pickleball Tour" width="87" height="96"></div>
  <span class="script">Welcome, ${name} players</span>
  <h1>Get your kicks — and your dinks — on Route 66.</h1>
  <p>Ten days by motorcoach between Chicago and Santa Monica, playing pickleball the whole way. Your club has a members-only rate.</p>
  <div class="codebox"><span class="label">Your club code</span><b>${esc(code)}</b><span>Saves ${esc(discountText())} at booking</span></div>
</div></header>
<main class="wrap">
  <section>
    <p class="label" style="color:var(--green)">The trip</p>
    <h2>One road, ten court sessions, sixteen departures.</h2>
    <div class="facts">
      <div class="fact"><span class="label">Route</span><br>Chicago ⇄ Santa Monica, westbound and eastbound</div>
      <div class="fact"><span class="label">Play</span><br>Ten court sessions at clubs along the Mother Road</div>
      <div class="fact"><span class="label">Group</span><br>32 players per departure, coached and bracketed</div>
      <div class="fact"><span class="label">Stays</span><br>Historic hotels and resorts, all ground transport</div>
    </div>
    <p style="margin-top:1.6rem"><a class="btn" href="/">See the full tour</a></p>
  </section>
  <section>
    <p class="label" style="color:var(--green)">Booking opens soon</p>
    <h2>Lock in the ${name} rate.</h2>
    ${form}
  </section>
  <p class="hint" style="margin-top:1.4rem">${name} is a referral partner of Pickle Tours and does not sell or operate this tour. Club codes don't combine with other offers.</p>
</main>${FOOT}`;
  return shell(`${c.club_name} × Route 66 Pickleball Tour`, body, {
    noindex: mode === "preview",
    desc: `${c.club_name} members save with code ${code} on the Route 66 Pickleball Tour — ten days of pickleball from Chicago to Santa Monica.`,
  });
}

/** Four-step sign-up: A slug, B code, C terms, D mailing list. */
export function joinPage(c: ClubRecord, open: boolean, error?: string) {
  const name = esc(c.club_name);
  const prefix = normCodePrefix(c.suggested_code);
  const closed = open ? "" : `<div class="notice">Sign-up opens once the club agreement is final. You can look around — we'll email you when it's ready.</div>`;
  const body = `${closed}
<header class="hero"><div class="wrap">
  <div class="marks">${clubMark(c)}<span class="x">×</span><img src="/assets/route66-pickleball-tour-logo.png" alt="Route 66 Pickleball Tour" width="87" height="96"></div>
  <h1>Set up ${name}'s club page</h1>
  <p>Four quick steps. When you finish, your page goes live and your members' code starts working at booking.</p>
</div></header>
<main class="wrap">
${error ? `<p class="bad" role="alert" style="margin-top:1.4rem">${esc(error)}</p>` : ""}
<form method="POST" action="/api/club-register" id="join">
  <input type="hidden" name="token" value="${esc(c.token)}">
  <div class="step"><p class="label">Step A</p><h2>Choose your page address</h2>
    <div class="prefix"><span>route66pickleballtour.com/</span><input type="text" name="slug" id="slug" value="${esc(c.suggested_slug)}" required maxlength="40" autocapitalize="none" spellcheck="false"></div>
    <p class="hint" id="slug-msg">Letters, numbers and dashes.</p></div>
  <div class="step"><p class="label">Step B</p><h2>Choose your members' code</h2>
    <div class="prefix"><input type="text" name="code" id="code" value="${esc(prefix)}" required maxlength="14" style="text-transform:uppercase"><span>${CODE_SUFFIX}</span></div>
    <p class="hint" id="code-msg">Members type this at checkout to save ${esc(discountText())}.</p></div>
  <div class="step"><p class="label">Step C</p><h2>Agree to the referral terms</h2>
    <p><a href="/club-terms.html" target="_blank" rel="noopener">Read the Club Referral Agreement</a> (version ${TERMS_VERSION}).</p>
    <div class="field"><label class="label" for="sn">Your name</label><input type="text" id="sn" name="signer_name" required autocomplete="name" value="${esc(c.contact_name ?? "")}"></div>
    <div class="field"><label class="label" for="st">Your title at the club</label><input type="text" id="st" name="signer_title" required></div>
    <div class="field"><label class="label" for="se">Your email</label><input type="email" id="se" name="signer_email" required autocomplete="email" value="${esc(c.contact_email ?? "")}"></div>
    <label class="check"><input type="checkbox" name="agree" value="yes" required><span>I'm authorized to act for ${name}, and the club agrees to the Club Referral Agreement.</span></label></div>
  <div class="step"><p class="label">Step D</p><h2>Stay in the loop</h2>
    <label class="check"><input type="checkbox" name="optin" value="yes" checked><span>Send me club partner updates — departure news, member flyers and booking-day reminders. Unsubscribe anytime.</span></label></div>
  <p style="margin:2rem 0 3rem"><button class="btn dark" type="submit" ${open ? "" : "disabled"}>Make our page live</button></p>
</form>
<script>
(function(){
  var t=document.querySelector('[name=token]').value;
  function check(kind,el,msg,fmt){var v=el.value;if(!v){return}
    fetch('/api/club-check?kind='+kind+'&value='+encodeURIComponent(v)+'&token='+t).then(function(r){return r.json()}).then(function(j){
      msg.className='hint '+(j.ok?'ok':'bad');msg.textContent=j.ok?fmt(j.value)+' is available.':j.message;}).catch(function(){})}
  var s=document.getElementById('slug'),sm=document.getElementById('slug-msg'),c=document.getElementById('code'),cm=document.getElementById('code-msg'),tm;
  s.addEventListener('input',function(){clearTimeout(tm);tm=setTimeout(function(){check('slug',s,sm,function(v){return 'route66pickleballtour.com/'+v})},350)});
  c.addEventListener('input',function(){clearTimeout(tm);tm=setTimeout(function(){check('code',c,cm,function(v){return v})},350)});
  check('slug',s,sm,function(v){return 'route66pickleballtour.com/'+v});check('code',c,cm,function(v){return v});
})();
</script>
</main>${FOOT}`;
  return shell(`Set up ${c.club_name}'s club page`, body, { noindex: true });
}

export function donePage(c: ClubRecord, url: string) {
  const r = c.registration!;
  const body = `<header class="hero"><div class="wrap">
  <span class="script">You're live!</span>
  <h1>${esc(c.club_name)} is on Route 66.</h1>
  <p>Your page: <a style="color:var(--optic)" href="${esc(url)}">${esc(url.replace(/^https?:\/\//, ""))}</a></p>
  <div class="codebox"><span class="label">Members' code</span><b>${esc(r.code)}</b></div>
  <p>Mike will email your final member flyer and email graphic, with this address and code on them, to ${esc(r.signer_email)}. Questions? Call 1-888-774-DINK.</p>
  <p><a class="btn" href="${esc(url)}">View your page</a></p>
</div></header>${FOOT}`;
  return shell(`${c.club_name} is live`, body, { noindex: true });
}

export function notFound() {
  return shell("Page not found | Route 66 Pickleball Tour", `<header class="hero"><div class="wrap">
  <h1>That exit isn't on our map.</h1><p>The page you're after doesn't exist (or isn't live yet).</p>
  <p><a class="btn" href="/">Back to the tour</a></p></div></header>${FOOT}`, { noindex: true });
}
