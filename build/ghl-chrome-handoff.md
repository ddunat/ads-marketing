# Handoff prompt: GHL changes via Claude in Chrome

Paste everything below the line into a Claude session **on David's computer**: either the Claude Desktop app, or `claude remote-control` run in a local clone of `ddunat/ads-marketing`. It needs the Claude in Chrome extension connected, with David signed in to GoHighLevel and Meta Events Manager in Chrome.

---

You're working in David Dunat's GoHighLevel (DC Building Inspectors) through Claude in Chrome.

Read these files from the GitHub repo `ddunat/ads-marketing` (branch `master`) first. They are the approved specs:
- `build/au-lead-forms.md`: AU form questions, survey settings, thank-you page logic, call-priority workflow, page fixes
- `build/booked-job-capi-feed.md`: booked and paid job events to Meta, for both sub-accounts
- `CLAUDE.md`: account ids and compliance rules

Hard rules:
- Two sub-accounts, never mixed:
  - AU `YGgCKbEtY4u8fRX0Zvfo`: pixel 821976388791436, AUD
  - HR `fSPTLOI7MAzy9VUHFa2k`: pixel 608006939071812, EUR
- Before editing the live AU surveys (`p38bDK53Y1AubQ0Ogopw` pre-purchase, `W3Szcw3yRDozoJnHunhS` construction), **duplicate each one** and keep the original as a backup.
- Don't delete anything, and don't touch any campaign, ad or budget in Ads Manager.
- Pages are live and taking leads. Make each change, preview it, then save. Don't leave a half-edited page published.
- Avoid clicking anything that raises a browser confirm dialog without warning David first.

Do this in order, and tick each step off as you go:
0. **First: lead plumbing for the Railway landing pages.** The pages now live on Railway, not GHL, so do NOT build `/auction` in GHL. Instead, follow `build/ghl-nurture.md`:
   - Create the "Meta Leads AU" pipeline and its lost reasons.
   - Build Workflow 1 with an **Inbound Webhook** trigger, plus the hot and warm sequences and the stop rules. Save them as **draft**.
   - Create (or pick) the booking calendar for pre-purchase inspections.
   - Also build Workflow 2 "Website booking in" (a second Inbound Webhook).
   - Report back to David: **both webhook URLs**. Callers are Annie, Kim and David, round robin. Claude sets these on Railway, then sends one test lead before publishing the workflow.
1. **AU surveys:** apply the question tables in `au-lead-forms.md`, with custom fields created and mapped:
   - one question per screen, progress bar on
   - partial submits on
   - contact fields required
2. **Thank-you pages:**
   - Create `/thankyou-book`: a copy of `/thankyou` plus a "Need it this week? Lock in your inspection time now →" block linking to dcinspect.com.au/online-bookings.
   - Add conditional redirects so the hot answers land there.
   - Confirm both pages fire the pixel Lead event (Meta Pixel Helper or Events Manager → Test events).
3. **Page fixes** on /home-869758 and /home-8356-3538:
   - 529 Google reviews, 4.9★
   - one true inspection count
   - "BPC registered building inspector (DBU-66182)"
   - fix "GURANTEED"
   - guarantee line exactly: "Your report the same day we inspect, or your money back."
4. **Call-priority workflow** (AU): hot, warm and cold buckets, as in the spec.
5. **Booked-job CAPI feed:** follow `booked-job-capi-feed.md` for AU, then HR.
   - Add the Booked stage where it's missing (HR).
   - David generates the CAPI access tokens in Events Manager himself. Ask him to paste each one straight into the GHL field; never into chat.
6. **Test:**
   - Submit one test lead per form; check it lands in the CRM with every field mapped.
   - Move a test opportunity to Booked, then Won; check the Schedule and Purchase events in Test events.
   - Delete the test contacts afterwards.
7. Report what was done, what was skipped and why, and anything GHL didn't allow. Commit a short log to `build/ghl-change-log.md` if you have the repo.
