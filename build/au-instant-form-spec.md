# AU Instant Form rebuild (Jeremy, 2026-11-02)

Replaces form 753250670189751 ("Lead Form") on the AU carousels. Meta forms can't be edited after publishing, so this is a **new form** (Ads Manager → the ad → Instant form → Create form, or Meta Business Suite → Instant forms → Create). None of our connected tools can create Instant Forms, so David builds it once (about 10 minutes), then Claude swaps it into the AU ads.

**Step 0, first:** connect the form to GHL (AU sub-account → Settings → Integrations → Facebook → Lead forms). Some "junk" is just leads nobody worked in Meta Leads Center.

## Form settings
- **Name:** `AU pre-purchase · Higher intent · Nov 2026`
- **Form type:** **Higher intent** (adds a review screen before submit). Not "More volume".
- **Intro (greeting) on:**
  - Headline: `Book your same-day building & pest inspection`
  - Text: `This form books a pre-purchase building and timber pest inspection in Melbourne. Your report the same day we inspect, or your money back. Takes under a minute.`

## Questions, in this order
1. **What are you buying?** (multiple choice) House / Apartment or unit / Townhouse
2. **Property suburb** (short answer, typed — not pre-filled)
3. **Where are you up to?** (multiple choice, with conditional logic)
   - Making an offer this week
   - Auction date set
   - Signed, cooling-off running
   - Just starting to look → **ends the form** (conditional logic: go to the "not yet" ending; no contact fields)
4. **When do you need the inspection?** (multiple choice) This week / Next week / In 2+ weeks (follow up softly; not a block)
5. Contact (pre-fill): **First name, Phone number, Email**
- **Phone verification:** turn on SMS/phone verification if the account offers it.

## Privacy
- Link: `https://dcinspect.com.au/privacy-policy` (use the site's real privacy page URL).

## Endings
- **Qualified:** `Thanks! We'll call you with inspection times.` (Only promise a response window you actually hit.) Button: `Call us` → 0483 936 872, or View website → dcinspect.com.au.
- **"Just starting to look":** `No problem. When you're ready to make an offer, come back and book; your report arrives the same day we inspect, or your money back.` Button: View website.

## After it's published
Send Claude the new form ID (or just say "new form is live") and Claude swaps it into the AU carousel ads, paused as they are now, and updates the desk cards.
