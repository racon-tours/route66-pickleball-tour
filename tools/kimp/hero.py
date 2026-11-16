from PIL import Image, ImageFilter
import numpy as np
im = Image.open(next(__import__('pathlib').Path('assets').glob('image2_254_176.*'))).convert('RGB')
W, H = im.size
im = im.crop((24, 22, W - 24, H - 22)); W, H = im.size
a = np.asarray(im).astype(float)
x0, x1 = int(W * .22), int(W * .80)
# heavy blur of the whole picture, used only as the base under the centre band
b = np.asarray(im.filter(ImageFilter.GaussianBlur(90))).astype(float)
green = np.array([18, 66, 38], float)
xs = np.arange(W)[None, :, None]
# weight: 0 outside band, rising smoothly to 1 at centre
t = np.clip((xs - x0) / (x1 - x0), 0, 1)
inside = ((xs >= x0) & (xs <= x1)).astype(float)
r0, r1 = .12, .88
w_band = np.clip(np.minimum(t / r0, (1 - t) / (1 - r1)), 0, 1)
w_band = (3 * w_band**2 - 2 * w_band**3) * inside
base = b * (1 - .9) + green * .9
out = a * (1 - w_band) + base * w_band
Image.fromarray(out.clip(0, 255).astype('uint8')).resize((1600, round(H * 1600 / W)), Image.LANCZOS) \
    .save('web/hero.webp', 'WEBP', quality=78, method=6)
print('ok')
