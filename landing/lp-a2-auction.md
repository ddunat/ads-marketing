# Landing page: A2 "Auction Saturday" control (Jeremy 8.5 → 9 with fixes applied)
Proposed URL: `inspection.dcinspect.com.au/auction`. Build it in GHL by cloning `/home-869758`, so pixel 821976388791436 and the tracking carry over.
Visual reference: `lp-a2-auction.html` (also published as a claude.ai artifact).

**Congruency rule:** the page mirrors the control ad word for word. No "Report Before Dark" here; it's a challenger variable, tested as an ad and page pair.

## Above the fold
- **Eyebrow:** BIDDING AT AUCTION THIS WEEK?
- **H1:** Your report the same day we inspect, or your money back.
- **Sub:** No cooling-off at a Victorian auction. Inspect first, then bid knowing exactly what you're buying.
- **Proof row:** ★ 4.9 · 529 Google reviews · BPC registered building inspector (DBU-66182)
- The survey starts immediately below.

**Removed from the old page:**
- 400+ reviews
- 6,500+ inspections
- "Registered/Qualified Inspectors"
- "30 seconds to check availability"

## Survey (same as `build/au-lead-forms.md` pre-purchase)
- One question per screen, progress bar, partial submits on.
- Questions:
  1. What are you buying?
  2. How many bedrooms?
  3. Where are you up to? (Auction date set / Signed, cooling-off running / Making an offer this week / Just looking for now)
  4. Property suburb
  5. First name, mobile and email (all required)
- **Routing:**
  - Hot answers (auction date set / signed) go to `/thankyou-book`, with "Need it this week? Lock in your inspection time now →" linking to online bookings.
  - Everyone else goes to `/thankyou`.
- **The pixel Lead must fire on BOTH thank-you pages.** Verify in Events Manager → Test events before launch.

## Below the form
- **How it works:**
  1. Book.
  2. We inspect: building & timber pest, every defect photographed and itemised.
  3. Report the same day, or your money back.
- **Anchor line:** "One defect found after settlement costs more than every inspection on this page."
- **Price table:**

  | Property | Price |
  |---|---|
  | 1–2 bed apartment | $550 |
  | 3 bed | $605 |
  | 4 bed | $649 |
  | 5 bed | $847 |
  | House on stumps | $726 |

  Price stays **below** the form, never above the fold.
- **FAQ:**
  - What if the report isn't same day? → "You get a full refund."
  - Can you inspect before Saturday? → "Yes, where availability allows. Book now and you'll see this week's remaining slots. Auction-week inspections go first."
  - Is pest included? → "Yes. Building and timber pest in one inspection and one report."
- **Repeat CTA:** "Inspect first: check this week's times."
- **Sticky mobile bar:** "Same-day report or your money back · Check times".
  - Show it only once the form is scrolled past.
  - **Never over the survey's last steps or the keyboard.**

## Pre-launch checks
- Lead fires on both thank-you pages.
- The sticky bar doesn't cover the submit button on steps 4–5.
- PageSpeed mobile load under about 2.5s: compress images, remove unused sections from the clone.

## Photos (Jeremy follow-up: 8.5 → est. 9.0–9.5 if mobile load stays under ~2.3s)
Order: hero → form → Google proof card → how it works (defect photo at step 2, report-ready phone at step 3) → price → FAQ → final CTA.
- **Hero (Jeremy option D, est. +0.2–0.3):** David portrait card (`img/david-hero.webp`, 11 KB, a calm frame from the A2 HeyGen video, black shirt, mirrored to match the ad). Mobile: 112×136 rounded card under the sub, with name, ★ 4.9 · 529 and BPC beside it, and the form's first option at ~590px. Desktop (≥900px): 300×367 card in the right column beside the headline. Never a big full-width hero photo (it pushes the form off-screen, -0.3 to -0.5) and never a house/defect photo as the hero (it breaks congruency with the ad). Only one avatar still.
- **Baseline to beat:** current Google Ads landing conversion is 5%.
- **Under the form:** Google proof card, 4.9 · 529 reviews + BPC DBU-66182 chip (pure CSS, no image).
- **Step 2:** defect photo (`img/defect.webp`, from the Drive crack footage). **Swap for 2–3 real report page screenshots with annotated defects, address blurred**, once David supplies them.
- **Step 3:** report-ready notification (`img/notif.webp`).
- **Never:** stock photos, house clipart, smiling families.
- **Speed:** WebP, `loading="lazy"` below the fold, width/height set. Test on a real phone on 4G before launch.
- **Measure:** snapshot the conversion rate by source before the photos go live so the lift can be proved.
