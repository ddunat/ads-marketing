# Cowork prompt: HR setup for the weekly ad factory (go.dcinspect.eu)

Paste everything below the line into Claude Cowork with Claude in Chrome connected. Be signed in to your domain registrar for dcinspect.eu, GoHighLevel, Railway and Google (Business Profile / Maps) in Chrome.

---

You're setting up the Croatian (HR) side of DC Building Inspectors' Meta ad engine. HR is our leak detection business in Croatia. Every HR ad gets its own landing page on **go.dcinspect.eu** (hosted on Railway), and leads go into GoHighLevel. Work in my Chrome with Claude in Chrome. I'm signed in to everything.

The repo `ddunat/ads-marketing` (branch `master`) has the context:
- `sites/landers/markets.json` (`hr` section): the facts still marked TODO
- `build/ghl-nurture.md`: the AU version of the GHL build. Mirror it.

If you can't open the repo, the details below are enough.

**Hard rules**
- GHL **HR sub-account only**: location `fSPTLOI7MAzy9VUHFa2k`. Never touch the AU sub-account (`YGgCKbEtY4u8fRX0Zvfo`).
- Don't delete or edit any existing DNS record, workflow, pipeline, form, calendar or contact. Only add new things.
- Save every new GHL workflow as **Draft**.
- Never imply David inspects or does the work himself: he's the director. Use "mi", "naš tim" and "David Dunat, direktor".
- Customer-facing text is in natural Croatian. I'll check the wording myself before anything goes live.
- Every SMS ends with the Croatian opt-out line: "Odgovorite STOP za odjavu."
- Before any irreversible click (publish, delete, send to real contacts), stop and ask me.

## Part A: DNS for go.dcinspect.eu
1. Find where **dcinspect.eu** DNS is managed: check the registrar, or the nameservers via a WHOIS/DNS lookup site. Open that DNS panel.
2. Add exactly these two records. Leave every other record alone.

   | Type | Name / Host | Value | TTL |
   |---|---|---|---|
   | CNAME | `go` | `qv5ge8ea.up.railway.app` | default / 1 h |
   | TXT | `_railway-verify.go` | `railway-verify=10665d834e706462e3607e967cb51b7a4f8afd3c89be317b8bf39c9da97d6ac9` | default / 1 h |

   - Some panels add the domain automatically. If the host field shows `.dcinspect.eu` after it, enter only `go` and `_railway-verify.go`.
   - If Cloudflare manages the DNS, set the CNAME to **DNS only** (grey cloud), not proxied.
   - If a `go` record already exists, stop and tell me what it points to.
3. Check it: in Railway (railway.com → project **dc-landing-pages** → service **landing-au** → Settings → Networking), `go.dcinspect.eu` should turn green within about an hour. If it isn't green yet, tell me and move on.

## Part B: HR facts for the landing pages
Collect these and report them back word for word. Don't invent anything. If you can't find something, say so.
1. **Google rating and review count** for the HR business (Google Maps / Business Profile). Give the exact numbers and the listing name.
2. **Business details for the footer:** the legal company name, OIB, address (town is enough), phone, and the website/booking link Croatian customers use. Look on dcinspect.eu. Anything you can't find, ask me.
3. **Qualification line:** what we can truthfully say about who does the leak detection (e.g. certified equipment, qualified technicians, years in business). Take it from dcinspect.eu. Don't make anything up.
4. Suggest Croatian wording for:
   - the director label (default: "David Dunat, direktor")
   - a one-line rating line, e.g. "4,9 ★ · 87 Google recenzija" with the real numbers
   - the footer line

## Part C: GHL, HR sub-account (`fSPTLOI7MAzy9VUHFa2k`)
1. **Pipeline** (Opportunities → Pipelines): create **Meta Leads HR** with stages: Novi upit, Kontaktiran, U razgovoru, Termin dogovoren, Obavljeno, Izvještaj poslan, Plaćeno, Dugoročno praćenje.
2. **Contact custom fields** (create any that are missing): Property Type, Stage, Suburb, Lead Temp, Landing Page, UTM Source, UTM Campaign, UTM Content, Event ID.
3. **Workflow "Meta LP lead in HR"** (Automation → Workflows → new, from scratch):
   1. **Trigger:** Inbound Webhook. **Copy the webhook URL.**
   2. Send this test payload to the URL so the fields can be mapped. Use a browser request tool, or ask me and I'll have Claude send it:
      `{"first_name":"TEST","phone":"+385910000000","email":"test+hr@dcinspect.com.au","property_type":"Stan","stage":"Curi sada","suburb":"Zagreb","lead_temp":"hot","service":"leak-detection","landing_page":"lp-hr-test","tags":["meta-lead","lp-hr-test","leak-detection","hot"],"source":"Meta ad: HR test","event_id":"test-hr-1","utm_source":"meta","utm_campaign":"test","utm_content":"hr-test"}`
      Then map the fields from that sample.
   3. **Create/Update Contact:** first name, phone, email and the custom fields. Add the tags from `tags`.
   4. **Create Opportunity:** pipeline Meta Leads HR, stage Novi upit. Name `{{first_name}}, {{suburb}}, {{landing_page}}`. Source `{{source}}`.
   5. **Internal notification:** SMS + app notification to me (David), plus anyone else I name: "Novi Meta upit {{lead_temp}}: {{first_name}}, {{suburb}}, {{stage}}. Nazovite: {{phone}}". Ask me who else should get it.
   6. **First SMS to the lead, sent straight away.** Draft it in natural Croatian and show it to me before saving. Use this meaning: "Hi {{first_name}}, this is the DC Inspect team. Thanks for your enquiry about leak detection. We'll call you shortly to arrange a time." plus the opt-out line. If I give you a booking link, include it.
   7. **Follow-ups:** draft a short Croatian sequence and show it to me. Leave it disabled in the workflow until I approve it:
      - hot: 15 min SMS, 3 h SMS, 24 h SMS, 48 h email
      - warm: day 1, 3, 7, 14
   8. **Stop rules:**
      - stop when the contact replies, and notify the owner
      - stop when the opportunity reaches Termin dogovoren or later
      - stop on DND/STOP
   9. Save as **Draft**.

## Part D: Railway variable
railway.com → project **dc-landing-pages** → service **landing-au** → Variables. Add:
- `GHL_WEBHOOK_URL_HR` = the Part C webhook URL

`META_PIXEL_ID_HR` is already set. Don't change it or any other variable. The service redeploys by itself.

## Part E: Report back, then wait
Tell me:
1. DNS: the records added, and whether Railway shows go.dcinspect.eu as green
2. Every Part B fact, with its source, and the Croatian wording you suggest
3. The HR webhook URL, and whether `GHL_WEBHOOK_URL_HR` is saved
4. The Croatian SMS drafts, for my approval
5. Anything you couldn't do exactly as written

Then ask me: **"What's your target cost per booked HR job, in EUR?"**

Don't publish the GHL workflow. I'll have Claude send one test lead first, then I'll publish it.
