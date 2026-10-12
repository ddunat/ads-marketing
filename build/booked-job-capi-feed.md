# Booked-job feed to Meta (Conversions API): both accounts

Decision 2026-10-12: optimise campaigns for **Lead**. Booked and paid jobs are sent back as **standard events** to condition the pixel (Jeremy). Switch optimisation to Schedule only at a sustained 30–50 bookings/week per ad set.
Build it in GHL workflows; the API token here can't create workflows.

## One-time setup per account
1. Meta Events Manager → the pixel → Settings → Conversions API → **Generate access token**.
   - AU pixel `821976388791436`
   - HR pixel `608006939071812`
2. In each GHL sub-account: Settings → Integrations → Facebook. Make sure the right ad account and pixel are connected.
   - AU: sub-account `YGgCKbEtY4u8fRX0Zvfo`, Meta ad account `449816980394949`.
   - HR: sub-account `fSPTLOI7MAzy9VUHFa2k`, Meta ad account `1386746812476820`.
3. Pipelines → add the stage **Booked** to the lead pipeline, if it's missing. The **HR pipeline has none** today.
   - HR also needs "No answer 1/2/3" stages, used for real (546 leads are sitting in "New Leads – Facebook").
   - **Never** reuse one account's pixel or token in the other sub-account.

## Workflow 1: "CAPI – Booked → Schedule"
- **Trigger:** Pipeline Stage Changed → pipeline = lead pipeline, stage = **Booked**.
- **Action:** Facebook Conversion API (the native GHL workflow action):
  - Pixel ID: that account's pixel. Access token: from step 1.
  - Event name: **Schedule** (standard event, not custom).
  - Action source: **system_generated** (CRM event).
  - Event ID: `{{opportunity.id}}-schedule` (de-duplication).
  - User data: email, phone, first name, last name, city/suburb, and `fbclid`/`fbc` if captured (GHL hashes these).
- Allow re-entry: **off**.

## Workflow 2: "CAPI – Paid → Purchase"
- **Trigger:** Opportunity Status Changed → **Won**. Or, if invoices are paid through GHL, use **Invoice Paid / Payment Received** instead. Pick one so a job never fires twice.
- **Action:** Facebook Conversion API:
  - Event name: **Purchase** (standard).
  - Value: `{{opportunity.monetary_value}}` (or the invoice total). Currency: **AUD** (AU) / **EUR** (HR).
  - Event ID: `{{opportunity.id}}-purchase`.
  - User data as in workflow 1.
- Allow re-entry: **off**.

## Check it works
1. Events Manager → Test events. Move a test opportunity to Booked, then to Won.
2. Expect one Schedule and one Purchase, each showing value and currency.
3. Then delete the test opportunity.
4. Check **Event Match Quality** after 48h. Aim for 6+; it rises when email and phone are both passed.

## Data hygiene this depends on
- The opportunity **value** must be filled in when a job is booked: the price by property size (AU) or the quote (HR).
- Staff must actually move cards to Booked and Won. If they don't, the feed sends nothing.
