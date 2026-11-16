import re, base64, json, sys, pathlib, html
src = next(pathlib.Path('.').glob('*.svg'))
s = src.read_text()
out = pathlib.Path('assets'); out.mkdir(exist_ok=True)

# images
imgs = {}
for m in re.finditer(r'<image id="([^"]+)"[^>]*?width="([\d.]+)" height="([\d.]+)"[^>]*?(?:xlink:)?href="data:image/(\w+);base64,([^"]+)"', s):
    iid, w, h, ext, data = m.groups()
    ext = 'jpg' if ext == 'jpeg' else ext
    fn = out / f'{iid}.{ext}'
    fn.write_bytes(base64.b64decode(data))
    imgs[iid] = dict(file=str(fn), w=float(w), h=float(h), kb=fn.stat().st_size // 1024)

# patterns -> image
pats = {}
for m in re.finditer(r'<pattern id="([^"]+)"[^>]*>(.*?)</pattern>', s, re.S):
    pid, body = m.groups()
    u = re.search(r'href="#([^"]+)"', body)
    if u: pats[pid] = u.group(1)

# shapes using patterns
uses = []
for m in re.finditer(r'<(rect|path)([^>]*?)fill="url\(#([^)]+)\)"([^>]*)/?>', s):
    tag, a1, pid, a2 = m.groups()
    attrs = a1 + a2
    g = lambda k: (re.search(rf'\b{k}="([^"]+)"', attrs) or [None, None])[1]
    uses.append(dict(tag=tag, id=g('id'), x=g('x'), y=g('y'), w=g('width'), h=g('height'),
                     tr=g('transform'), rx=g('rx'), pattern=pid, image=pats.get(pid)))

# texts
texts = []
for m in re.finditer(r'<text([^>]*)>(.*?)</text>', s, re.S):
    attrs, body = m.groups()
    g = lambda k: (re.search(rf'\b{k}="([^"]+)"', attrs) or [None, None])[1]
    spans = re.findall(r'<tspan[^>]*?x="([\d.]+)" y="([\d.]+)"[^>]*>(.*?)</tspan>', body, re.S)
    txt = ' '.join(html.unescape(t) for _, _, t in spans)
    y = float(spans[0][1]) if spans else 0
    x = float(spans[0][0]) if spans else 0
    texts.append(dict(y=round(y), x=round(x), font=g('font-family'), size=g('font-size'), weight=g('font-weight'),
                      fill=g('fill'), ls=g('letter-spacing'), id=g('id'), text=txt))
texts.sort(key=lambda t: (t['y'], t['x']))
json.dump(dict(images=imgs, uses=uses, texts=texts), open('design.json', 'w'), indent=1)
print(len(imgs), 'images;', len(uses), 'pattern fills;', len(texts), 'texts')
for t in texts:
    print(t['y'], t['x'], t['font'], t['size'], t['weight'], t['fill'], '|', t['text'][:140])
