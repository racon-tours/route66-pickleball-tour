# Kimp design build (sandbox)

Home page rebuilt to Kimp's Figma design "pickle.dot.tours_Route66pickleballtour.com_AN_05-NOV-26_V1_R4"
(our copy is in Mike's Figma drafts). Copy comes from the site, not from the design file.

- `extract.py` — reads Figma's SVG export of the page frame: images + every text layer.
- `prep.py` / `hero.py` — turn the export's images into `assets/kimp/*.webp`; hero has Kimp's baked-in text removed.
  Images with AI-generated photorealistic faces are deliberately left out.
- `build.py source-copy-index.html ../../index.html kimp.css` — writes the page. Edit `kimp.css` for look,
  `source-copy-index.html` (or the Copy Deck flow) for words, then rebuild.
