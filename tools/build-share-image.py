"""Build the link-preview (Open Graph) image for route66pickleballtour.com.

Usage: python3 tools/build-share-image.py <PassionOne-Bold.ttf> <BarlowCondensed-Bold.ttf>
Writes assets/route66-pickleball-tour-share.png (1200x630) from assets/route66-pickleball-tour-logo.png.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PASSION, BARLOW = sys.argv[1], sys.argv[2]

GREEN = (4, 66, 29)        # Pickle Green #04421D
OPTIC = (231, 251, 32)     # Optic Yellow #E7FB20
WHITE = (255, 250, 255)    # #FFFAFF
W, H = 1200, 630

img = Image.new("RGB", (W, H), GREEN)
d = ImageDraw.Draw(img)

# Shield on the left
shield = Image.open(ROOT / "assets/route66-pickleball-tour-logo.png").convert("RGBA")
sh = 500
sw = round(shield.width * sh / shield.height)
shield = shield.resize((sw, sh), Image.LANCZOS)
img.paste(shield, (70, (H - sh) // 2), shield)

# Text block on the right
x = 70 + sw + 60
maxw = W - x - 60

def fit(text, path, size):
    while True:
        f = ImageFont.truetype(path, size)
        if d.textlength(text, font=f) <= maxw or size <= 20:
            return f
        size -= 2

lines = [
    ("ROUTE 66", PASSION, 112, OPTIC),
    ("PICKLEBALL TOUR", PASSION, 112, OPTIC),
    ("CHICAGO – SANTA MONICA", BARLOW, 46, WHITE),
    ("11 DAYS · MARCH–OCTOBER 2027", BARLOW, 46, WHITE),
]
fonts = [fit(t, p, s) for t, p, s, _ in lines]
gaps = [0, 4, 34, 8]
heights = [f.getbbox(t)[3] - f.getbbox(t)[1] for (t, *_), f in zip(lines, fonts)]
total = sum(heights) + sum(gaps)
y = (H - total) // 2
for (t, _, _, c), f, h, g in zip(lines, fonts, heights, gaps):
    y += g
    d.text((x, y - f.getbbox(t)[1]), t, font=f, fill=c)
    y += h

out = ROOT / "assets/route66-pickleball-tour-share.png"
img.save(out, optimize=True)
print(out, img.size)
