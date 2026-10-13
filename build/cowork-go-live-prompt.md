# Cowork prompt: put the A2 landing page live (GHL + Meta + Zapier)

Paste everything below the line into Claude Cowork with Claude in Chrome connected. Be signed in to GoHighLevel, Meta Events Manager, Railway and Zapier in Chrome.

---

You're setting up lead handling for DC Building Inspectors' new Meta ad landing page (https://go.dcinspect.com.au/auction). Work in my Chrome with Claude in Chrome. I'm signed in to everything.

The full specs are in the GitHub repo `ddunat/ads-marketing` (branch `master`): `build/ghl-nurture.md` has every SMS/email word for word, and `build/ghl-chrome-handoff.md` has the context. If you can't open the repo, use the details below; they're enough.

**Hard rules**
- GHL **AU sub-account only**: location `YGgCKbEtY4u8fRX0Zvfo`. Never touch the HR sub-account (`fSPTLOI7MAzy9VUHFa2k`).
- Don't delete or edit any existing workflow, pipeline, form, calendar or contact. Only create new things.
- Save every new workflow as **Draft**. Don't publish anything until Part E says so.
- Never write "VBA registered". Never imply David inspects (he's the director). The guarantee wording is exactly: "Your report the same day we inspect, or your money back."
- Every SMS ends with "Reply STOP to opt out".
- Before any irreversible click (publish, delete, send to real contacts), stop and ask me.

## Part A: Pipeline (GHL → Opportunities → Pipelines)
1. Create the pipeline **Meta Leads AU** with stages: New Lead, Contact Attempted, Engaged, Booked, Inspection Completed, Report Sent, Paid, Long Term Nurture.
2. Add these lost reasons (Settings → Opportunities → Lost reasons) if missing: Booked Elsewhere, Auction Passed, Price, No Response.
3. Create these contact custom fields if they don't exist: Property Type, Bedrooms, Buying Stage, Suburb, Lead Temp, Landing Page, UTM Source, UTM Campaign, UTM Content, Event ID.

## Part B: Workflow 1, "Meta LP lead in" (Automation → Workflows → new → start from scratch)
1. **Trigger:** Inbound Webhook. Copy its **webhook URL**.
2. Don't map fields yet. First post this test payload to the URL from a browser tool, or ask me to and I'll have Claude send it:
   `{"first_name":"TEST","phone":"+61400000000","email":"test+lp@dcinspect.com.au","property_type":"House","bedrooms":"3","stage":"Auction date set","suburb":"Brunswick","lead_temp":"hot","service":"pre-purchase","landing_page":"lp-a2-auction","tags":["meta-lead","lp-a2-auction","pre-purchase","hot"],"source":"Meta ad: A2 auction","event_id":"test-1","utm_source":"fb","utm_campaign":"test","utm_content":"a2"}`
   Then map the fields from the sample.
3. **Create/Update Contact:** first name, phone, email, plus the custom fields above. Add tags from `tags`, plus `{{suburb}}`.
4. **Create Opportunity:** pipeline Meta Leads AU, stage New Lead. Name `{{first_name}}, {{suburb}}, {{landing_page}}`. Source `{{source}}`. Value: leave blank.
5. **Internal notification**, broadcast (no round robin): SMS + app notification to **Annie, Kim and David** at the same time: "New Meta lead {{lead_temp}}: {{first_name}}, {{suburb}}, {{stage}}. Call now: {{phone}}". Whoever calls first sets themselves as contact owner and moves the opportunity to Contact Attempted.
6. **If/Else on Lead Temp = hot:**
   - **Hot branch:** build the hot sequence from `build/ghl-nurture.md` (0 min SMS, 15 min SMS, 1 h email, 3 h SMS, 24 h SMS, 48 h email, 72 h SMS). Booking link: https://dcinspect.com.au/online-bookings
   - **Warm branch:** the warm sequence (day 0, 1, 3, 7, 14, 30).
   - If you can't read the repo, the first SMS is: "Hi {{first_name}}, it's the team at DC Building Inspectors. Thanks for your enquiry. Book your pre-purchase inspection here: https://dcinspect.com.au/online-bookings. Your report the same day we inspect, or your money back. Reply STOP to opt out." Build that, then stop and ask me for the rest.
7. **Stop rules** (workflow settings / goal events):
   - Contact replies: stop the workflow and notify the contact owner.
   - Opportunity moves to Booked or later: stop.
   - DND/STOP: stop.
8. Save as **Draft**.

## Part C: Workflow 2, "Website booking in"
1. **Trigger:** a second Inbound Webhook. Copy its URL. The test payload is:
   `{"order":"C-TEST0001","total":649,"first_name":"TEST","last_name":"Booking","phone":"+61400000000","email":"test+lp@dcinspect.com.au","service":"TEST Pre-Purchase","when":"Monday 2:30PM","payment":"Test","suburb":"Coburg","postcode":"3058","source":"GoDaddy online booking"}`
2. **Find contact** by email, then by phone.
3. **If the contact has tag `meta-lead`:**
   - move their Meta Leads AU opportunity to **Booked**
   - add tag `booked-meta`
4. **Else:**
   - add tag `booked-organic`
   - don't create anything in Meta Leads AU
5. In both branches, remove the contact from Workflow 1 (stops the nurture).
6. Save as **Draft**.

## Part D: Railway + Meta + Zapier
1. **Railway:** railway.com → project **dc-landing-pages** → service **landing-au** → Variables. Add:
   - `GHL_WEBHOOK_URL` = Workflow 1 URL
   - `GHL_BOOKING_WEBHOOK_URL` = Workflow 2 URL
   It redeploys automatically.
2. **Meta Events Manager:** pixel **821976388791436** → Settings → Conversions API → **Generate access token**. In Railway, add variable `META_CAPI_TOKEN` with that token. Don't paste the token anywhere else.
3. **Zapier:** open https://mcp.zapier.com/api/v1/connect-auth/App235435CLIAPI?accountId=12615392 and create an **API by Zapier** connection:
   - auth: custom header `x-booking-token` = `WsbKNg-VLu89_D_zrMDZQ_6hiAAEGZ6N`
   - allowed domain (if asked): `landing-au-production.up.railway.app`
   - name: **Railway booking relay**

## Part E: Report back, then wait
Tell me:
- both webhook URLs
- whether all Railway variables are saved
- whether the Zapier connection exists
- anything you couldn't build exactly as specified

**Don't publish the GHL workflows yet.** I'll have Claude send one test lead and one test booking first. After I confirm, publish both workflows and delete the TEST contact.
