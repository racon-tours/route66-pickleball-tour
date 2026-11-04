/** HTML for the club sign-up flow (clubs get a tracked short link, not a page). Brand: Guide v1.3 tokens. */
import { ClubRecord, esc, discountText, CODE_SUFFIX, TERMS_VERSION, normCodePrefix, STATES } from "./clubs.mts";
import type { Signup } from "../functions/club-signup.mts";

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
.hero{position:relative;color:var(--white);background:var(--green);}
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
input[type=text],input[type=email],input[type=tel]{width:100%;font:400 1rem Merriweather,serif;padding:.75rem .9rem;border:2px solid var(--green);background:var(--white)}
.field{display:grid;gap:.35rem}
.hint{font-size:15px;color:var(--muted);margin:0}
.ok{color:var(--green-line);font-weight:700}.bad{color:#B3261E;font-weight:700}
.step{background:var(--white);border-left:6px solid var(--optic);padding:1.4rem 1.4rem 1.6rem;margin:1.2rem 0;box-shadow:0 1px 0 var(--rule)}
.step h2{font-size:1.5rem}
.prefix{display:flex;align-items:stretch;flex-wrap:wrap}.prefix input{flex:1 1 10rem;min-width:0;width:auto}.prefix span{display:flex;align-items:center;padding:.5rem .7rem;background:var(--green);color:var(--white);font:700 1rem 'Barlow Condensed';overflow-wrap:anywhere}
h1,h2,p,label{overflow-wrap:break-word}
.check{display:flex;gap:.7rem;align-items:flex-start}.check input{margin-top:.45rem;width:20px;height:20px;flex:none}
footer{padding:2rem 0 3rem;font-size:15px;color:var(--muted)}
footer.pdt-foot .pdt-grid{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-start;gap:1.5rem 2.5rem}
footer.pdt-foot .pdt-legal{flex:1 1 280px;order:1;margin:0;font-size:10px;line-height:1.6;letter-spacing:.01em}
footer.pdt-foot .pdt-right{flex:0 1 auto;order:2;margin-left:auto;display:flex;flex-direction:column;align-items:flex-end;text-align:right;gap:.75rem}
footer.pdt-foot .pdt-right nav{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:.4rem 1.1rem}
footer.pdt-foot .sot-phone{margin:0;font-weight:700;font-size:clamp(1.2rem,3vw,1.5rem);line-height:1.2;letter-spacing:.01em}
footer.pdt-foot .sot-phone a{text-decoration:none}
footer.pdt-foot .pdt-logo{width:220px;max-width:100%;height:auto;display:block}
@media (max-width:640px){footer.pdt-foot .pdt-right{order:0;align-items:flex-start;text-align:left}footer.pdt-foot .pdt-right nav{justify-content:flex-start}}
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

const FOOT = `<footer class="pdt-foot">
  <div class="wrap pdt-grid">
    <p class="pdt-legal">Pickle Dot Tours | St. Louis, MO USA<br>CA Registered Seller of Travel CST 2175274-50<br>WA Seller of Travel UBI 606297094<br>FL Seller of Travel Pending<br>Registration as a Seller of Travel does not constitute approval by the State of California.<br>&copy; 2026 Nichols &amp; Company</p>
    <div class="pdt-right">
      <nav aria-label="Footer"><a href="mailto:hello@pickle.tours">hello@pickle.tours</a> <a href="https://pickle.tours/terms">Terms</a> <a href="https://pickle.tours/privacy">Privacy</a></nav>
      <p class="sot-phone"><a href="tel:+18887743465">Call or text 1-888-774-DINK</a></p>
      <img class="pdt-logo" src="/assets/pdt-wordmark-green.png" alt="Pickle Dot Tours" width="640" height="164">
    </div>
  </div>
</footer>`;

/** Four-step sign-up: A slug, B code, C terms, D mailing list. */
export function joinPage(c: ClubRecord, open: boolean, error?: string) {
  const name = esc(c.club_name);
  const prefix = normCodePrefix(c.suggested_code);
  const closed = open ? "" : `<div class="notice">Sign-up opens once the club agreement is final. You can look around — we'll email you when it's ready.</div>`;
  const body = `${closed}
<header class="hero"><div class="wrap">
  <div class="marks">${clubMark(c)}<span class="x">×</span><img src="/assets/route66-pickleball-tour-logo.png" alt="Route 66 Pickleball Tour" width="87" height="96"></div>
  <h1>Set up ${name}'s club link</h1>
  <p>Four quick steps. When you finish, your club link goes live and your members' code starts working at booking.</p>
</div></header>
<main class="wrap">
${error ? `<p class="bad" role="alert" style="margin-top:1.4rem">${esc(error)}</p>` : ""}
<form method="POST" action="/api/club-register" id="join">
  <input type="hidden" name="token" value="${esc(c.token)}">
  <div class="step"><p class="label">Step A</p><h2>Choose your club link</h2>
    <div class="prefix"><span>route66pickleballtour.com/</span><input type="text" name="slug" id="slug" value="${esc(c.suggested_slug)}" required maxlength="40" autocapitalize="none" spellcheck="false"></div>
    <p class="hint" id="slug-msg">Letters, numbers and dashes. Put this link in your member emails; it takes members to the tour and lets us credit your club.</p></div>
  <div class="step"><p class="label">Step B</p><h2>Choose your members' code</h2>
    <div class="prefix"><input type="text" name="code" id="code" value="${esc(prefix)}" required maxlength="14" style="text-transform:uppercase"><span>${CODE_SUFFIX}</span></div>
    <p class="hint" id="code-msg">Members type this at checkout to save ${esc(discountText())}.</p></div>
  <div class="step"><p class="label">Step C</p><h2>Agree to the referral terms</h2>
    <p>Your members save ${esc(discountText())}. The club earns $250 for every member who books with your code and travels, when your club link or code goes out in at least one member email that month ($150 otherwise). We handle every booking and payment.</p>
    <p><a href="/club-terms.html" target="_blank" rel="noopener">Read the Club Referral Agreement</a> (version ${TERMS_VERSION}).</p>
    <div class="field"><label class="label" for="sn">Your name</label><input type="text" id="sn" name="signer_name" required autocomplete="name" value="${esc(c.contact_name ?? "")}"></div>
    <div class="field"><label class="label" for="st">Your title at the club</label><input type="text" id="st" name="signer_title" required></div>
    <div class="field"><label class="label" for="se">Your email</label><input type="email" id="se" name="signer_email" required autocomplete="email" value="${esc(c.contact_email ?? "")}"></div>
    <label class="check"><input type="checkbox" name="agree" value="yes" required><span>I'm authorized to act for ${name}, and the club agrees to the Club Referral Agreement.</span></label></div>
  <div class="step"><p class="label">Step D</p><h2>Stay in the loop</h2>
    <label class="check"><input type="checkbox" name="optin" value="yes" checked><span>Send me club partner updates — departure news, member flyers and booking-day reminders. Unsubscribe anytime.</span></label></div>
  <p style="margin:2rem 0 3rem"><button class="btn dark" type="submit" ${open ? "" : "disabled"}>Activate our link</button></p>
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
  return shell(`Set up ${c.club_name}'s club link`, body, { noindex: true });
}

export function donePage(c: ClubRecord, url: string) {
  const r = c.registration!;
  const body = `<header class="hero"><div class="wrap">
  <span class="script">You're live!</span>
  <h1>${esc(c.club_name)} is on Route 66.</h1>
  <p>Your club link: <a style="color:var(--optic)" href="${esc(url)}">${esc(url.replace(/^https?:\/\//, ""))}</a></p>
  <div class="codebox"><span class="label">Members' code</span><b>${esc(r.code)}</b></div>
  <p>Mike will email your final member flyer and email graphic, with this link and code on them, to ${esc(r.signer_email)}. Questions? Call 1-888-774-DINK.</p>
  </div></header>${FOOT}`;
  return shell(`${c.club_name} is live`, body, { noindex: true });
}

export function notFound() {
  return shell("Page not found | Route 66 Pickleball Tour", `<header class="hero"><div class="wrap">
  <h1>That exit isn't on our map.</h1><p>The page you're after doesn't exist (or isn't live yet).</p>
  <p><a class="btn" href="/">Back to the tour</a></p></div></header>${FOOT}`, { noindex: true });
}

/** Self-serve registration (/clubs/register), linked from the MailerLite welcome email. */
export function registerPage(v: Signup, open: boolean, error?: string, blocked = false) {
  if (blocked) {
    return shell("Not available in your state yet | Route 66 Pickleball Tour", `<header class="hero"><div class="wrap">
  <h1>We're not there yet.</h1>
  <p>Thanks, ${esc(v.contact_name || "friend")}. The club referral program isn't available to clubs in ${esc(STATES[v.state] ?? v.state)} yet.
  You're on our club list, so we'll email you as soon as it opens there.</p>
  <p><a class="btn" href="/">See the tour</a></p></div></header>${FOOT}`, { noindex: true });
  }
  const closed = open ? "" : `<div class="notice">Registration isn't open yet. We'll email you when it is.</div>`;
  const opt = (code: string) => `<option value="${code}"${v.state === code ? " selected" : ""}>${esc(STATES[code])}</option>`;
  const f = (id: keyof Signup, label: string, type = "text", extra = "") =>
    `<div class="field"><label class="label" for="${id}">${label}</label><input type="${type}" id="${id}" name="${id}" value="${esc(v[id])}" ${extra}></div>`;
  const body = `${closed}
<header class="hero"><div class="wrap">
  <div class="marks"><img src="/assets/route66-pickleball-tour-logo.png" alt="Route 66 Pickleball Tour" width="87" height="96"></div>
  <h1>Register for club referral commission</h1>
  <p>Your members save ${esc(discountText())} on the Route 66 Pickleball Tour, and your club earns $250 for every member who books with your code and travels. Three short steps; we email your member flyer, newsletter graphic, link and code once they're set up.</p>
</div></header>
<main class="wrap">
${error ? `<p class="bad" role="alert" style="margin-top:1.4rem">${esc(error)}</p>` : ""}
<form method="POST" action="/api/club-signup" id="reg">
  <p style="display:none"><label>Leave blank <input name="bot-field"></label></p>
  <div class="step"><p class="label">Step 1</p><h2>Your club</h2>
    ${f("club_name", "Club name", "text", 'required maxlength="120" autocomplete="organization"')}
    <div class="field"><label class="label" for="short">Short name for your link and code</label>
      <div class="prefix"><input type="text" id="short" name="short" value="${esc(v.short)}" required maxlength="14" autocapitalize="characters" spellcheck="false" style="text-transform:uppercase"><span>${CODE_SUFFIX}</span></div>
      <p class="hint" id="short-msg">3–14 letters or numbers, e.g. ABQE. Your members' code becomes ABQE${CODE_SUFFIX} and your link route66pickleballtour.com/abqe.</p></div>
    ${f("website", "Club website (optional)", "text", 'maxlength="200" autocomplete="url"')}
  </div>
  <div class="step"><p class="label">Step 2</p><h2>Address and contact</h2>
    ${f("address_1", "Street address", "text", 'required maxlength="200" autocomplete="address-line1"')}
    ${f("city", "City", "text", 'required maxlength="80" autocomplete="address-level2"')}
    <div class="field"><label class="label" for="state">State</label>
      <select id="state" name="state" required style="font:400 1rem Merriweather,serif;padding:.75rem .9rem;border:2px solid var(--green);background:var(--white)">
        <option value="">Choose…</option>${Object.keys(STATES).map(opt).join("")}</select></div>
    ${f("zip", "ZIP code", "text", 'required inputmode="numeric" maxlength="10" autocomplete="postal-code"')}
    ${f("contact_name", "Your name", "text", 'required maxlength="120" autocomplete="name"')}
    ${f("contact_title", "Your title at the club", "text", 'required maxlength="120" autocomplete="organization-title"')}
    ${f("email", "Your email", "email", 'required maxlength="200" autocomplete="email"')}
    ${f("phone", "Phone", "tel", 'required maxlength="40" autocomplete="tel"')}
  </div>
  <div class="step"><p class="label">Step 3</p><h2>Agree to the referral terms</h2>
    <p>Your members save ${esc(discountText())} with your code. The club earns $250 for every member who books with it and travels, when your club link or code goes out in at least one member email that month ($150 otherwise), paid after the trip. We handle every booking and payment.</p>
    <p><a href="/club-terms.html" target="_blank" rel="noopener">Read the Club Referral Agreement</a> (version ${TERMS_VERSION}).</p>
    <label class="check"><input type="checkbox" name="agree" value="yes" required><span>I'm authorized to act for this club, and the club agrees to the Club Referral Agreement.</span></label></div>
  <p style="margin:2rem 0 3rem"><button class="btn dark" type="submit" ${open ? "" : "disabled"}>Register our club</button></p>
</form>
<script>
(function(){
  var s=document.getElementById('short'),m=document.getElementById('short-msg'),tm;
  function check(){var v=s.value.toUpperCase().replace(/[^A-Z0-9]/g,'');if(!v)return;
    fetch('/api/club-check?kind=code&value='+encodeURIComponent(v)).then(function(r){return r.json()}).then(function(j){
      m.className='hint '+(j.ok?'ok':'bad');m.textContent=j.ok?(j.value+' and route66pickleballtour.com/'+j.value.replace(/${CODE_SUFFIX}$/,'').toLowerCase()+' are available.'):j.message;}).catch(function(){})}
  s.addEventListener('input',function(){clearTimeout(tm);tm=setTimeout(check,350)});
})();
</script>
</main>${FOOT}`;
  return shell("Register your club | Route 66 Pickleball Tour", body, { noindex: true });
}

export function registeredPage(clubName = "Your club", email = "") {
  return shell("You're registered | Route 66 Pickleball Tour", `<header class="hero"><div class="wrap">
  <span class="script">You're in!</span>
  <h1>${esc(clubName)} is registered.</h1>
  <p>We're setting up your members' code now. Your member flyer, newsletter graphic, club link and code will arrive by email${email ? ` at ${esc(email)}` : ""}, usually within a business day.</p>
  <p>Questions? Call or text 1-888-774-DINK.</p>
  <p><a class="btn" href="/">See the tour</a></p></div></header>${FOOT}`, { noindex: true });
}
