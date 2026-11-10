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

## Google reviews carousel
- `reviews-godaddy.html` (~22k characters) is a separate GoDaddy HTML section. Reviews are copied word for word from the Google Business Profile (10 Nov 2026); add new ones to the REVIEWS list in the script. Section height: about 880 px desktop, 770 px phone.

## Homepage sections (Naše usluge, Što provjeravamo, Česta pitanja, Kontaktirajte nas)
- `dcinspect-eu-sections-godaddy.html` (~37k characters): one GoDaddy HTML section replacing the four old ones. Keep GoDaddy's map section below it.
- Every internal link from the old homepage is kept, as full https://dcinspect.eu/... URLs with target="_top". Edit `sections-source.html`, then `python3 build_godaddy_lite.py sections-source.html dcinspect-eu-sections-godaddy.html`.
- The enquiry form opens WhatsApp or email with the message filled in (no server needed). Photos are attached in WhatsApp/email.
