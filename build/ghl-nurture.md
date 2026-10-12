# GHL lead pipeline and nurture (Jeremy design, 2026-10-12)

Applies to every Meta ad landing page on Railway (`sites/`). Each page posts its lead to one GHL **Inbound Webhook** workflow in the AU sub-account (`YGgCKbEtY4u8fRX0Zvfo`).

## Webhook payload (from `sites/server.js`)
`first_name, phone (+61…), email, property_type, bedrooms, stage, suburb, lead_temp (hot|warm), service, landing_page, tags[], source, page, event_id, utm_source/medium/campaign/content, fbclid, submitted_at`

- Hot means stage = "Auction date set" or "Signed, cooling-off running". Each page sets its own hot rule in `LANDERS`.
- In the workflow, map the payload to the contact (name, phone, email) and to custom fields: property type, bedrooms, stage, suburb, lead temp, landing page, UTM fields.

## Pipeline "Meta Leads AU"
- **Stages:** New Lead → Contact Attempted → Engaged → Booked → Inspection Completed → Report Sent → Paid, plus **Long Term Nurture**.
- **Lost reasons** (use these instead of extra stages):
  - Booked Elsewhere
  - Auction Passed
  - Price
  - No Response

## Workflow 1: "Meta LP lead in"
1. **Trigger:** Inbound Webhook.
2. **Create/update contact.** Add tags from the payload, plus the stage and the suburb.
3. **Create opportunity** in Meta Leads AU at **New Lead**. Name it `{first_name}, {suburb}, {landing_page}`, with source = `source`.
4. **If/else on `lead_temp`:**
   - hot → Hot sequence
   - else → Warm sequence
5. **Internal notification** to the caller: SMS + app push with the name, suburb, stage and a tap-to-call link.

## Speed to lead
- **Business hours:** a human call attempt within **5 minutes**. Saturday morning needs cover, because that's auction day.
- **After hours:**
  - The instant SMS carries the booking link.
  - First call at **8:00 next business day**, with an SMS at 8:05.
  - Cooling-off leads that arrive late Friday can't wait until Tuesday, so the SMS has to do the selling.
- **Open question for David:** who owns the 5-minute call (an admin, a VA, or David)?

## Hot sequence (auction clock)
Every SMS ends with "Reply STOP to opt out" (Spam Act). Keep the guarantee wording exact.

| When | Channel | Copy |
|---|---|---|
| 0 min | SMS | Hi {first_name}, it's the team at DC Building Inspectors. Thanks for your enquiry. Book your pre-purchase inspection here: {booking_link}. Your report the same day we inspect, or your money back. |
| 5 min | Call | Human call attempt |
| 15 min (no answer) | SMS | Hi {first_name}, just tried your mobile. If you're bidding this weekend, book a time here and we'll do our best to get you inspected before auction day: {booking_link} |
| 1 h | Email | **Subject:** Your inspection before auction day, {suburb}. **Body:** 4.9★ from 529 Google reviews, what's covered (building + timber pest), the guarantee line verbatim, and the booking link. |
| 3 h | SMS + proof card image | 4.9 stars from 529 Google reviews. Same-day reports. Times here: {booking_link} |
| 24 h | SMS | Hi {first_name}, is your auction this Saturday? We still have pre-auction times for {suburb}. {booking_link} |
| 48 h | Email + blurred sample report page | **Subject:** What our report actually shows |
| 72 h | SMS | Last check-in from us, {first_name}. If you want the report in hand before you bid, book here: {booking_link} or reply CALL and we'll ring you. |

After 72 h the sequence stops. If the auction passes with no booking: Lost, Auction Passed, then the contact moves to the re-engagement track (auction buyers bid again).

## Warm sequence (days)

| Day | Channel | Copy |
|---|---|---|
| 0 | SMS | Hi {first_name}, it's the team at DC Building Inspectors. We'll give you a call shortly about your {property_type} in {suburb}. In the meantime you can book directly here: {booking_link} |
| 1 | Email | Trust build: reviews, what's inspected, the guarantee line. |
| 3 | SMS | Hi {first_name}, any questions about the inspection? Happy to run through what's covered. |
| 7 | Email | Sample report (blurred). |
| 14 | SMS | Still thinking it over, {first_name}? Your report the same day we inspect, so even late in your decision we can turn it around fast. {booking_link} |
| 30 | Email | **Subject:** Where did we lose you? One short line, no pitch: "reply and let us know what you're deciding on." |
| 30–90 | Email, monthly | Value touches. |

After 90 days the opportunity moves to Long Term Nurture.

## Stop rules
- **Appointment booked** (calendar event created): exit both sequences and move the opportunity to Booked.
- **Contact replied:** pause the automation and assign the conversation to the caller. Never auto-answer a human.
- **Opportunity moved past Engaged:** stop the nurture.
- **STOP reply:** DND (GHL native).
- **Auction date passed** (needs an auction-date field, which the forms don't capture yet): Lost, Auction Passed.

## Meta events (CAPI booked-job feed, pixel 821976388791436)
- **Lead:** already sent by the Railway server (Pixel + CAPI, same `event_id`, de-duplicated). Do **not** also send Lead from GHL.
- **Schedule:** when a calendar booking is created.
- **Purchase:** when the invoice is paid, with the actual amount as `value` (AUD).
- Wire Schedule and Purchase last, after testing, so test data doesn't pollute the pixel. Details are in `build/booked-job-capi-feed.md`.

## Flags
- The guarantee goes out in writing at scale. Confirm operations can honour it on every job.
- The BPC line can go into the emails as "BPC registered building inspectors and qualified trades".
