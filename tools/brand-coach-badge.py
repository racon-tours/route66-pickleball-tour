#!/Users/ibmike/.venvs/racon/bin/python3
"""
brand-coach-badge.py — replace the third-party coach nameplate in picklebus.png
with a Pickle Tours badge.

Two operations on the coach side panel:
  1. The lower model-number text is painted out using per-row colour sampled
     from clean panel to its left, with matched film grain and a feathered
     edge so the repair does not read as a flat patch.
  2. The manufacturer nameplate is covered by a Pickle Tours plaque — Pickle
     Green field, chrome-style edge, ball-and-cucumber mark in Optic Yellow,
     wordmark in Barlow Condensed Bold.

Output is a new master; the original file is never modified.
Run:  ./tools/brand-coach-badge.py
"""

import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MKTG = "/Users/ibmike/Desktop/N&Co/2 - pickle-tours/2-Marketing/Route66"
SRC = f"{MKTG}/picklebus.png"
OUT = f"{MKTG}/picklebus-branded.png"
MARK_SVG = f"{REPO}/assets/pickle-tours-mark.svg"
FONT = "/tmp/BarlowCondensed-Bold.ttf"

GREEN = (4, 66, 29)
OPTIC = (231, 251, 32)
CHROME = (214, 211, 200)

# measured regions in the 1024x1024 master
NAMEPLATE = (90, 244, 250, 288)      # plaque footprint (covers the badge)
MODELTEXT = (94, 289, 246, 332)      # region to paint out
SAMPLE_X = (58, 92)                  # clean panel column used for row colour

SS = 4  # supersample factor for the plaque


def ensure_font():
    """Barlow Condensed Bold is a webfont on this site, not a system font."""
    if not os.path.exists(FONT):
        url = ("https://github.com/google/fonts/raw/main/ofl/"
               "barlowcondensed/BarlowCondensed-Bold.ttf")
        subprocess.run(["curl", "-sL", "-o", FONT, url], check=True)
    return FONT


def paint_out(img):
    """Remove the model text by rebuilding panel paint row by row."""
    a = np.array(img).astype(np.float32)
    x0, y0, x1, y1 = MODELTEXT

    # grain profile from a clean patch (residual after removing row means)
    clean = a[300:330, 40:88, :3]
    grain = float((clean - clean.mean(axis=1, keepdims=True)).std())

    fill = a.copy()
    rng = np.random.default_rng(66)
    for y in range(y0, y1):
        base = np.median(a[y, SAMPLE_X[0]:SAMPLE_X[1], :3], axis=0)
        # panel brightens very slightly to the right; hold a gentle ramp
        ramp = np.linspace(0.0, 3.0, x1 - x0)[:, None]
        row = base[None, :] + ramp + rng.normal(0, grain, (x1 - x0, 3))
        fill[y, x0:x1, :3] = row

    # feathered mask so the repair edge is not a hard rectangle
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rectangle([x0, y0, x1 - 1, y1 - 1], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(3))
    mask = (np.array(m).astype(np.float32) / 255.0)[..., None]

    out = a * (1 - mask) + fill * mask
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def build_plaque(w, h):
    """Pickle Tours nameplate, rendered at SS scale then downsampled."""
    W, H = w * SS, h * SS
    p = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(p)
    r = 9 * SS

    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=r, fill=GREEN + (255,),
                        outline=CHROME + (255,), width=2 * SS)

    # soft top highlight — the panel is lit from above
    hl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    for i in range(H // 2):
        alpha = int(26 * (1 - i / (H / 2)))
        hd.line([(0, i), (W, i)], fill=(255, 255, 255, alpha))
    hlm = Image.new("L", (W, H), 0)
    ImageDraw.Draw(hlm).rounded_rectangle([0, 0, W - 1, H - 1], radius=r, fill=255)
    p.alpha_composite(Image.composite(hl, Image.new("RGBA", (W, H), (0, 0, 0, 0)), hlm))

    # mark
    mh = int(H * 0.66)
    subprocess.run(["rsvg-convert", "-h", str(mh), MARK_SVG, "-o", "/tmp/_mark.png"],
                   check=True)
    mark = Image.open("/tmp/_mark.png").convert("RGBA")
    mx = int(W * 0.055)
    my = (H - mark.height) // 2
    p.alpha_composite(mark, (mx, my))

    # wordmark, auto-fitted to the space remaining
    tx = mx + mark.width + int(W * 0.045)
    avail = W - tx - int(W * 0.055)
    text = "PICKLE TOURS"
    size = 4
    while True:
        f = ImageFont.truetype(FONT, size + 1)
        if d.textlength(text, font=f) > avail or size > H:
            break
        size += 1
    f = ImageFont.truetype(FONT, size)
    tw = d.textlength(text, font=f)
    bbox = d.textbbox((0, 0), text, font=f)
    d.text((tx + (avail - tw) / 2, (H - (bbox[3] - bbox[1])) / 2 - bbox[1]),
           text, font=f, fill=OPTIC + (255,))

    return p.resize((w, h), Image.LANCZOS)


def main():
    if not os.path.exists(SRC):
        sys.exit(f"source not found: {SRC}")
    img = Image.open(SRC).convert("RGB")
    ensure_font()
    img = paint_out(img)

    x0, y0, x1, y1 = NAMEPLATE
    w, h = x1 - x0, y1 - y0
    plaque = build_plaque(w, h)

    # photographic integration: the plaque is vector-crisp and the plate around
    # it is not. Soften to the photo's own edge acuity and match its grain,
    # otherwise it reads as a sticker laid on top of the picture.
    plaque = plaque.filter(ImageFilter.GaussianBlur(0.5))
    pa = np.array(plaque).astype(np.float32)
    rng = np.random.default_rng(66)
    pa[..., :3] += rng.normal(0, 2.4, pa[..., :3].shape)
    plaque = Image.fromarray(np.clip(pa, 0, 255).astype(np.uint8))

    # drop shadow, down and right to match the scene light
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x0 + 2, y0 + 3, x1 + 1, y1 + 2],
                                         radius=9, fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(2.5))

    canvas = img.convert("RGBA")
    canvas.alpha_composite(sh)
    canvas.alpha_composite(plaque, (x0, y0))
    canvas.convert("RGB").save(OUT)
    print(f"wrote {OUT}")
    print(f"plaque {w}x{h} at ({x0},{y0})  wordmark fitted")


if __name__ == "__main__":
    main()
