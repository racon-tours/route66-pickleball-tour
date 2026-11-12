#!/usr/bin/env python3
"""brochure-crops.py — cut the web imagery out of the Kimp e-brochure.

Source: Canva design "V1-pickle.dot.tours-E - Brochure" (DAHY1W9EAGI), exported as
PNG pages at 3264 px wide (p1.png ... p10.png). The brochure is the reference build
for the Route 66 tour look (brand guide v2.0, Part B).

Usage:  python3 tools/brochure-crops.py <dir-with-p1..p10.png>
Writes width-stepped WebP files into assets/img/r66/.

Left out on purpose: hotel snapshots (named properties not under contract), the cover
swimmers and the Chicago reception couple (AI-looking faces, brand guide open item).
"""
import sys, os
from PIL import Image, ImageFilter, ImageDraw

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img', 'r66')
os.makedirs(OUT, exist_ok=True)

# slug: (page, (x0, y0, x1, y1) as fractions of the page, output widths, feather)
CROPS = {
    'road-coach':   (1,  (0.012, 0.700, 0.988, 0.985), (800, 1400, 2000), False),
    'pier':         (2,  (0.620, 0.020, 0.970, 0.260), (500, 900), False),
    'chicago':      (4,  (0.010, 0.885, 0.600, 0.985), (800, 1400), False),
    'stlouis':      (5,  (0.220, 0.820, 0.780, 0.985), (800, 1400), False),
    'courts':       (6,  (0.220, 0.800, 0.775, 0.970), (800, 1400), False),
    'cadillac':     (7,  (0.240, 0.800, 0.770, 0.975), (800, 1400), False),
    'bluehole':     (8,  (0.250, 0.700, 0.760, 0.900), (800, 1400), False),
    'flagstaff':    (9,  (0.010, 0.260, 0.660, 0.540), (800, 1400, 2000), False),
    'santamonica':  (10, (0.010, 0.520, 0.990, 0.985), (800, 1400, 2000), False),
    'winslow':      (2,  (0.600, 0.340, 0.950, 0.640), (400, 700), False),
}

for slug, (page, (a, b, c, d), widths, feather) in CROPS.items():
    path = os.path.join(SRC, f'p{page}.png')
    if slug == 'santamonica' and os.path.exists(os.path.join(SRC, 'p10-clean.png')):
        path = os.path.join(SRC, 'p10-clean.png')   # extra pier removed (fix-santamonica-pier.py)
    im = Image.open(path).convert('RGB')
    W, H = im.size
    crop = im.crop((round(a * W), round(b * H), round(c * W), round(d * H)))
    if feather:  # soft oval edge so the card sits on the page's own parchment
        mask = Image.new('L', crop.size, 0)
        m = int(min(crop.size) * 0.04)
        ImageDraw.Draw(mask).rounded_rectangle((m, m, crop.width - m, crop.height - m), radius=m * 3, fill=255)
        crop = crop.convert('RGBA'); crop.putalpha(mask.filter(ImageFilter.GaussianBlur(m)))
    for w in widths:
        w = min(w, crop.width)
        r = crop.resize((w, round(crop.height * w / crop.width)), Image.LANCZOS)
        r.save(os.path.join(OUT, f'{slug}-{w}.webp'), 'WEBP', quality=80, method=6)
        print(f'{slug}-{w}.webp', r.size)
