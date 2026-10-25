# AU round 2 (weekly run, 25 Oct 2026)

## A4 "Cooling-off clock" (`au-a4-cooling-off`)
- **Why:** the daily check paused the A2 copy (A$266, 0 bookings). Jeremy: auction bidders are a small slice of the market. A4 keeps A2's guarantee and page shape but targets private-sale buyers who have already signed, using the real deadline of the Victorian cooling-off period.
- **Jeremy (conversation 6b2ddcb2):**
  - Ad: 7 → 9. Fixes applied: David no longer reads out the review count, the close says "proceed, renegotiate, or walk", the headline carries the promise, and the CTA ties to the clock.
  - Page: 8.5. Fix applied: the submit button now reads "Get my same-day inspection times".
  - Not applied: the "most reports take 3–5 business days" contrast, because it isn't verified.
- **Video:**
  - HeyGen v3 `3eab69f4d02efaea802e88f5c052dd0b` (720x1280, 25.8s), built by `build_video.py` from `video.json` to 29.9s with the end card.
  - HeyGen v3 returned no caption file. `a4.srt` takes its words from the script and its timing from an Arcads transcription, which misheard "Your report" as "You'll report".
  - B-roll (safe windows from `creative/library/broll.json`): brick efflorescence at 0–4.3s, verandah rot at 12.0–15.9s.
- **Page:** `sites/landers/au-cooling-off.json` → go.dcinspect.com.au/cooling-off.
  - Zapier smoke test (25 Oct): 200 with form, pixel, H1 and submit label; video served with range requests; `/api/lead` returned `{"ok":true,"hot":true}`.
  - The test lead "TEST delete" (test+lp-a4-cooling-off@dcinspect.com.au) is in GHL AU and should be deleted.
- **Meta:** video `1690736232837415`, uploaded from an Arcads signed URL. Ad `120253064290780220`, created **paused** in "Warm Leads - Facebook + Instagram" (`120240471624270220`). The campaign itself is paused.
- **Also fixed:** house on stumps is $715 (PLAN.md). Both the A2 and A4 pages had $726, which is the PCI price.
- **Open for David:**
  - one real Melbourne review quote for under the price table (Jeremy: page goes to 9)
  - the end-card form recording still shows the old website form
