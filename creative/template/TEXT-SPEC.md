# On-screen text template (Jeremy spec + ACQ handbook, 2026-10-12)
Applies to every video ad. Example: `creative/au-round1/build/a2-v3.ass`.

**Font:** Manrope ExtraBold (800). Files are in this folder; pass `fontsdir` to the ffmpeg subtitles filter. Colours: blue #3483FA, cyan #22C3FF, ink #1E1E24, white.

## Safe zones (9:16, 1080x1920)
- Top 12%: the platform's account-name overlay. Nothing goes here.
- Bottom 20%: platform buttons. Nothing goes here.
- Captions sit at roughly 55–75% of the height, below the chin. **Never cover the mouth.**

## Hook (first ~1.7s)
- Line 1: ALL CAPS on a blue box. Line 2: white on an ink box (e.g. "AUCTION THIS SATURDAY?" / "INSPECT FIRST.").
- Pop-in on the first frame: scale 106% → 100% over 3 frames.

## Running captions
- 2–4 word chunks, **sentence case**, about 96px. White, thin ink outline, soft shadow.
- Each chunk scale-pops 108% → 100%.
- **One highlight per chunk at most**, in cyan, on the word that matters.
- **Numbers and prices go in brand blue**, not cyan.

## Guarantee punch
- One timed full-width moment when the guarantee is spoken: ALL CAPS, white plus cyan, on an ink box, about 2–2.5s.
- **No persistent banners.**

## Proof card
- A native Google look: white rounded card, soft shadow, big "4.9", Google-yellow stars, "529 Google reviews · Melbourne".
- About 2.5s, timed to the spoken line. **No gold badge style.**
- Upgrade later: a real review snippet with first name and suburb, with consent.

## End card (3s)
- "PICK YOUR PROPERTY." in white, "LOCK YOUR TIME." in cyan.
- A phone mockup of the actual form, with a tap ring on the first option.
- The mockup must not show page claims that contradict the ad, e.g. the page's "400+ reviews". Frame below that line.

## Kaleidoscope
- Keep the template consistent across a batch, but make **one deliberate break per batch** (caption colour or hook treatment) so there's something to test.
