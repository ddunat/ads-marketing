# Cowork prompt: build the AU Higher-intent lead form

Paste everything below the line into a Cowork session on David's computer. It needs Claude in Chrome, and David signed in to Facebook (Business Suite / Ads Manager) and to GoHighLevel.

---

You're helping David Dunat (Director, DC Building Inspectors, Melbourne) build a new Meta Instant Form for his AU ads, then connect it to GoHighLevel. Use Claude in Chrome in my logged-in browser. Work in a new tab.

**Hard rules**
- AU only: ad account 449816980394949 ("DC Building Inspectors", AU), Facebook Page ID 100943435016413. Never touch the Croatian (HR) account 1386746812476820 or its forms.
- Don't edit, publish, unpause or delete any ad, ad set or campaign. Don't change any budget. Your only jobs are creating one new form and connecting forms to GHL.
- Don't delete or archive the old form 753250670189751 ("Lead Form").
- Wording: never write "VBA registered", and never say David inspects (say "we" or "our team"). Use the guarantee wording exactly as written below.
- If a screen asks for payment details, a password or 2FA, or anything here doesn't match what you see, stop and ask me.

**Part 1: connect Facebook lead forms to GHL (do this first)**
1. Open GoHighLevel and switch to the AU sub-account (location ID YGgCKbEtY4u8fRX0Zvfo, "DC Building Inspectors" Australia, not the Croatian one).
2. Go to Settings → Integrations → Facebook (or Settings → Integrations → Facebook & Instagram). If Facebook isn't connected, connect it and pick the page with ID 100943435016413.
3. Open the Lead forms / Facebook form mapping section. Enable syncing for form 753250670189751 now, and for the new form once you've created it in Part 2. Map first name, phone, email, and any custom questions to GHL fields if it asks.
4. Tell me what you saw and what you turned on.

**Part 2: create the new form**
In Meta Business Suite → All tools → Instant forms (or Ads Manager → Forms library) for page 100943435016413, click Create form and set it up exactly like this:

- **Form name:** `AU pre-purchase · Higher intent · Nov 2026`
- **Form type:** Higher intent (not "More volume")
- **Intro:** on
  - Headline: `Book your same-day building & pest inspection`
  - Description: `This form books a pre-purchase building and timber pest inspection in Melbourne. Your report the same day we inspect, or your money back. Takes under a minute.`
- **Questions, in this order:**
  1. Multiple choice, "What are you buying?": House / Apartment or unit / Townhouse
  2. Short answer, "Property suburb" (custom question, not pre-filled)
  3. Multiple choice, "Where are you up to?": Making an offer this week / Auction date set / Signed, cooling-off running / Just starting to look
     - Conditional logic: "Just starting to look" goes straight to a separate ending (below) and skips the contact fields. If conditional logic isn't offered, keep the option and tell me.
  4. Multiple choice, "When do you need the inspection?": This week / Next week / In 2+ weeks
  5. Contact fields (pre-filled): First name, Phone number, Email
  - Turn on phone number verification if it's offered.
- **Privacy policy:** link text `Privacy policy`. For the URL, find the real privacy page on dcinspect.com.au and use that; if there isn't one, stop and ask me.
- **Ending, qualified:** headline `Thanks! We'll call you with inspection times.` Button: Call business → ask me for the number before you publish (don't guess it). If calling isn't available, use View website → https://dcinspect.com.au
- **Ending, "Just starting to look":** headline `No problem.` Text: `When you're ready to make an offer, come back and book. Your report arrives the same day we inspect, or your money back.` Button: View website → https://dcinspect.com.au

Before you publish, show me a screenshot of the preview and wait for my OK. After I approve, publish it.

**Part 3: report back**
- Give me the new form's ID (the long number), and confirm it's syncing to the AU GHL sub-account (Part 1, step 3).
- Then I'll paste the ID into my Claude Code session, which swaps the new form into the AU carousel ads.
