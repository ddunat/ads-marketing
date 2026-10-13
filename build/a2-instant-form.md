# A2 Instant Form challenger (Jeremy, 2026-10-13)

The Hydra test: the **same A2 hook** runs to two destinations at once. Judge on **cost per booked inspection only**.

## Campaign setup
| Arm | Destination | Share of spend | Campaign |
|---|---|---|---|
| Page (control) | go.dcinspect.com.au/auction | ~60% | existing Leads campaign |
| Instant Form (challenger) | Meta lead form, **Higher intent** | ~40% | separate Leads campaign, "Instant forms" conversion location |

- Run the test for at least 2 weeks.
- One test at a time. The call-ad challenger waits until this test ends, then gets 20–30% of spend.
- Bookings come from the GoDaddy booking email → Schedule (CAPI). Both arms end at the same event, so the comparison is fair.
- GHL tags: `instant-form` vs `lp-a2-auction`. Bookings: `booked-meta` (Meta lead history) vs `booked-organic`.

## Form: Higher intent (review screen before submit)
**Intro (headline):** Bidding at auction this week?
**Intro (description):** Answer 5 quick questions and we'll send through this week's inspection times for your property. Your report the same day we inspect, or your money back.

**Questions** (same order as the page; the stage answer drives hot/warm routing in GHL):
1. What are you buying? House / Apartment or unit / Townhouse
2. How many bedrooms? 1–2 / 3 / 4 / 5+
3. Where are you up to? Auction date set / Signed, cooling-off running / Making an offer this week / Just looking for now
4. Property suburb (short answer)
5. First name, phone, email (prefill)

**Privacy policy:** dcinspect.com.au privacy page. "We only use your details to arrange your inspection."

**Thank-you screen:**
- Headline: Thanks, your enquiry is with our team.
- Description: The fastest way to lock in a time is to book online now. If your auction is this Saturday, book today so your report is in hand before you bid.
- Button: "Book online now" → `https://dcinspect.com.au/online-bookings?utm_source=meta&utm_medium=instant_form&utm_campaign=a2-auction`

## GHL
- Use the native Facebook lead form integration into the AU sub-account.
- Map the answers to the same custom fields as the page webhook.
- Add tags `meta-lead`, `instant-form`, plus `hot`/`warm` from the stage answer.
- Then run the same Workflow 1 path: opportunity → broadcast to the callers → hot/warm sequence.
- Instant-form leads are colder, so the 5-minute call and the SMS sequence carry more of the conversion.

## Expectations
- CPL roughly 30–50% cheaper than the page.
- Lower lead-to-book rate.
- The net cost per booking is unknown until tested.
