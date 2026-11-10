# dcinspect.eu scroll section (HR / EN)

- `dcinspect-eu-godaddy.html` is the paste-ready file. Copy all of it into a GoDaddy **HTML** section. All images are embedded (~1.1 MB).
- Top part: a scroll-through-the-house viewer. Inside GoDaddy's embed it scrolls within its own box, then the page carries on. On a normal page it pins to the screen.
- `source.html` is the same page with image placeholders (`__IMG_name__`). `walk/` holds the before/after image pairs, `img/` the older single images. `parts/` holds the walkthrough CSS/HTML/JS.
- Repair costs: edit `data-min` / `data-max` on each `<div class="sc">` scene. Totals recalculate.
- Costs are placeholder ranges. Replace with real figures before going live. Have a native speaker check the Croatian.

## Hero only
- `dcinspect-eu-hero-godaddy.html` is just the scroll-through-the-house viewer, to replace the site hero. `hero-source.html` is its editable source.

## GoDaddy 51,200-character limit
- `dcinspect-eu-hero-godaddy-lite.html` (~40k characters) is the one to paste into GoDaddy. Images load from jsDelivr, which serves this public repo's files, pinned to commit 292fec4.
- Rebuild after edits: `python3 build_godaddy_lite.py <commit-with-the-images>`.
- Keep this branch (or merge it) so the pinned commit stays on GitHub.
