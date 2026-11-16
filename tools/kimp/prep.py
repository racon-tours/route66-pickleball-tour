"""Turn the Kimp export images into web assets for the sandbox build.
Images with AI-generated photorealistic faces (9, 12, 16, 21) are deliberately not used."""
from PIL import Image, ImageFilter
import numpy as np, pathlib
src = pathlib.Path('assets'); out = pathlib.Path('web'); out.mkdir(exist_ok=True)
def f(n): return next(src.glob(f'image{n}_254_176.*'))
def save(im, name, w, q=80):
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(out / f'{name}.webp', 'WEBP', quality=q, method=6); print(name, im.size)

# parchment textures
save(Image.open(f(0)).convert('RGB'), 'parchment', 941, 70)
save(Image.open(f(1)).convert('RGBA'), 'paper-torn', 1200, 78)
save(Image.open(f(3)).convert('RGB'), 'paper-wide', 1376, 72)
save(Image.open(f(5)).convert('RGBA'), 'paper-card', 800, 75)
save(Image.open(f(8)).convert('RGB'), 'paper-plain', 600, 70)

# hero: remove the baked-in text/badge from the centre band
h = np.asarray(Image.open(f(2)).convert('RGB')).astype(float)
H, W, _ = h.shape
x0, x1 = int(W * .285), int(W * .715)
L, R = h[:, x0 - 6:x0].mean(1), h[:, x1:x1 + 6].mean(1)
t = np.linspace(0, 1, x1 - x0)[None, :, None]
band = L[:, None, :] * (1 - t) + R[:, None, :] * t
# blend towards a deep green in the middle, like the design's gradient
green = np.array([22, 74, 44], float)
mid = np.sin(np.pi * t) ** 1.2
band = band * (1 - .85 * mid) + green * (.85 * mid)
h2 = h.copy(); h2[:, x0:x1] = band
img = Image.fromarray(h2.clip(0, 255).astype('uint8'))
# soften the seams
mask = Image.new('L', (W, H), 0); m = np.zeros((H, W), 'uint8'); m[:, x0 - 30:x0 + 30] = 255; m[:, x1 - 30:x1 + 30] = 255
blur = img.filter(ImageFilter.GaussianBlur(14)); img.paste(blur, (0, 0), Image.fromarray(m).filter(ImageFilter.GaussianBlur(10)))
save(img, 'hero', 1920, 78)

# cut-outs (keep alpha)
save(Image.open(f(4)).convert('RGBA'), 'pier-sign', 1300, 80)
save(Image.open(f(7)).convert('RGBA'), 'bus-top', 640, 82)
save(Image.open(f(17)).convert('RGBA'), 'paddles', 420, 82)
save(Image.open(f(18)).convert('RGBA'), 'quarry', 900, 80)
save(Image.open(f(22)).convert('RGBA'), 'canyon', 1100, 78)
save(Image.open(f(23)).convert('RGBA'), 'pier-sunset', 1100, 78)
v = Image.open(f(15)).convert('RGBA'); vw, vh = v.size
for name, box in {'vignette-ranch': (vw // 2, 0, vw, vh // 2), 'vignette-bus': (vw // 2, vh // 2, vw, vh)}.items():
    c = v.crop(box); c = c.crop(c.getbbox()); save(c, name, 900, 80)

# photos (no AI faces)
save(Image.open(f(6)).convert('RGB'), 'coach-boarding', 800, 80)
for n, name in {10: 'card-stlouis', 11: 'card-grandlake', 13: 'card-albuquerque', 14: 'card-flagstaff',
                19: 'comfort-hotel', 20: 'comfort-coach'}.items():
    save(Image.open(f(n)).convert('RGB'), name, 900, 78)
