---
name: make-ad
description: Build the weekly batch of DC Building Inspectors Meta video ads, each with its own landing page, end to end, and drop them on the Ad Desks for David's approval. Use when the weekly routine fires, or when David asks for "the next ad", "a new ad", "this week's ads" or "an ad about X".
---

# make-ad: weekly ad + landing page factory

David only reviews the finished ad and landing page on the Ad Desk. Everything before that is yours, in this order.
A2 (auction, AU) is the reference build. Every new ad should be as good as A2 v6 + `go.dcinspect.com.au/auction`.

## 0. Read first (every run)
- `CLAUDE.md`: compliance. Never "VBA"; David is **Director** and doesn't inspect; say "BPC registered building inspectors and qualified trades"; DBU-66182 only next to David's name. Guarantee wording is exact: "Your report the same day we inspect, or your money back."
- `PLAN.md`: decisions, desk card format, "Weekly ad factory".
- `research/acq-ad-playbook.md` (ACQ checklist + frameworks) and `research/jeremy-rubric.md`.
- `build/cost-per-booking-plan.md`: the $50 target and kill/scale rule.
- `creative/au-round1/build/README.md`: what A2 learned (v1→v6).
- `creative/template/TEXT-SPEC.md`: caption and text rules.

## 1. How many ads, and which angles
- **Targets per week:**
  - AU: 3 new ads, in the AU account (Meta `449816980394949`).
  - HR: 2 new ads, in the HR account (Meta `1386746812476820`).
  - Never mix the two accounts.
- **Batch size:**
  - Count the ads the ops routine killed in the last 7 days, per account. Read them from the desk db `stats/<YYYY-WW>`, written by the daily `ad-ops` routine, or count cards with `status: "paused"` and a `paused_reason` from this week.
  - Build that many replacements, capped at the target.
  - Always build at least 1 per account.
  - If nothing was killed and the account already runs ≥ 6 ads in test, build 1.
- **Data:** Windsor `facebook` per ad, last 14 and 30 days: spend, leads, CPL. GHL bookings by `landing_page` tag and `booked-meta` (Windsor `gohighlevel`). Rank live ads by cost per booked inspection, falling back to CPL when bookings < 2.
- **Kaleidoscope rule:** ~80% remixes of the current winner (new hook, new opening, new B-roll, same promise), ~20% new angles from the playbook frameworks. Before scripting, ask Jeremy to vet the angle list (one message for the whole batch).
- Don't repeat an angle that was killed in the last 30 days unless the hook is materially different.

## 2. Script and copy (per ad)
- Write the following to the A2 shape (see `creative/au-round1/drafts-v2.md`):
  - the hook (said in the first 2s, with the guarantee or the core promise)
  - 22–26s of VO, "we" voice
  - one proof beat (4.9 · 529 Google reviews for AU)
  - the CTA "Tap below"
  - primary text, headline and description, plus the CTA enum (LEARN_MORE by default)
- **Jeremy loop** (MCP `jeremy`, `send_message`):
  - Send the script and copy, apply his fixes, re-send.
  - Stop at ≥ 8/10. At most 3 rounds.
  - If it's still under 8, drop that ad and say so in the run summary. Never post an ad under 8.
- **HR:**
  - Write natural Croatian (not translated English), with HR facts from `sites/landers/markets.json` (`hr`).
  - Card notes must say David is the native-language check.
  - **HR ads use the Meta Instant Form, not a landing page** (David, 2026-10-15: "we have had great success with this"). Form `2898956873609451` on page `658374350686787`, ad set Adv Plus `120227138979370195`. `create_ad` with `creative.object_story_spec.video_data.call_to_action = {"type":"GET_QUOTE","value":{"lead_gen_form_id":"2898956873609451","link":"http://fb.me/"}}`. Skip section 4 for HR; the desk card's `landing` gate notes the form instead.
  - HR facts (David, 2026-10-15): 13 five-star Google reviews; 25+ years combined experience; global leak detection and building consultancy experience; thermal imaging, moisture meters, CCTV drain cameras, pipe locators, tracer gas, acoustic detection; repairs of moisture problems. Croatia-wide; never mention the Zagreb base. No prices. Phone 099 208 0227. Offer: find leaks without breaking tiles; same-day visit for urgent leaks.
  - HR guarantee (Jeremy, pending David's OK on the desk): "Ako ne pronađemo izvor curenja vode, detekciju ne plaćate." Active water leaks only; never on mould/damp/rising-damp ads (use the same-day written report there). No mould health claims.
  - **Voice:** David's clone is an English voice. Send HeyGen the script with every `c` respelled `ts` (keep č/ć). Then transcribe the audio (Arcads `arcads_transcribe`, srt) and re-render any take with a misheard key word. HeyGen gives no Croatian captions: build the SRT from the script with the transcription's timing (`creative/template/srt_from_script.py`, or by hand).
  - **Images (David, 2026-10-15): never reuse the same photo across ads. Make new ones in Arcads** (`arcads_generate_image_nano_banana`, model `nano-banana-2-1`, product DC Building Inspectors). Prompt for photorealistic phone photos of Croatian homes, no people's faces, no text, no logos. AI images illustrate the problem or the method only: never a fake meter/thermal reading, never an AI person presented as our technician, never a fake result. Real photos (David's thermal shot, meter readings) are the only proof images.
  - Static carousels: `creative/template/build_carousel.py` (spec format in its docstring); create with `link_data.child_attachments[]` (picture URL + the lead form on every card).
  - Reference build: `creative/hr-round1/`.

## 3. Video
1. **HeyGen v3** (the proxy injects the key; v2 is shut off after 2026-10-31):
   - `POST https://api.heygen.com/v3/videos` with `{"type":"avatar","avatar_id":"b6820f0449eb4e3aab591fc44c75fcce","voice_id":"fe2230b3ddee436fb50c6ebc9b44f1e5","script":"…","aspect_ratio":"9:16","title":"<key>"}`.
   - Poll `GET https://api.heygen.com/v3/videos/<id>` until `status` is `completed`.
   - Download `video_url` (plain) and `subtitle_url` (SRT). If the v3 field names differ, read the error message and adapt; the v2 fallback is `POST /v2/video/generate` with `talking_photo` while it still works.
   - Downloads come from `files2.heygen.ai`, which is in the allowed domains.
2. **B-roll:**
   - Pick only from `creative/library/broll.json`, inside each clip's `safe` window.
   - Download with the Google Drive MCP (`download_file_content`, then decode the base64 into the scratchpad).
   - New clips: add them to the library only after checking a contact sheet for number plates, house numbers, faces, agency or builder signage, and customer details. Anything unchecked never goes in an ad.
3. **Spec:** write `creative/<batch>/<key>/video.json` (schema at the top of `creative/template/build_video.py`):
   - hook boxes for 0–2s
   - B-roll under the "problem" lines
   - the proof card (`creative/template/assets/proofcard-au.png`) under the reviews line, with `caption_top` for that window
   - `notif` + punch "SAME-DAY REPORT / {OR YOUR MONEY BACK}" on the guarantee line
   - end card `creative/template/assets/endcard_rec.mp4`
   - Build it: `python3 creative/template/build_video.py <spec>`.
4. **QA:** look at the `-sheet.jpg` and these frames:
   - the logo reads correctly (`hflip: true` for David's look)
   - the hook text is on screen at 0s
   - captions don't cover the face or the proof card
   - no private details anywhere
   - Fix the spec and rebuild until it's clean.

## 4. Landing page (one per ad, always)
1. **Spec:** write `sites/landers/<market>-<slug>.json`, copying `sites/landers/au-auction.json`:
   - The **headline must be the ad's promise word for word** (Jeremy's congruency rule).
   - The eyebrow is the ad's hook question.
   - `path` = `/<slug>`, `key` = `lp-<adkey>`, plus a `hot` regex for the stage answers that mean "needs it this week".
   - Steps are 4 qualifying questions; the market adds the contact step.
   - VSL: optional; reuse `/img/a2-vsl.mp4` only if it fits the angle.
2. `python3 sites/build_landers.py` (fails on TODOs or missing fields).
3. **Jeremy scores the page** (send the spec text): ≥ 8 to pass, at most 3 rounds.
4. Commit and push to `master`. Railway (`dc-landing-pages`/`landing-au`) deploys on push. Check the deploy with Railway `list-deployments` and `get-logs`, which should show `listening on 3000`.
5. **Smoke test the live page:**
   - Use the private Zapier workflow `test-lp-lead-once` (`01a1367d-c691-70c9-9ec5-16a1820f38d0`).
   - Update its draft to GET the new page and POST a TEST lead (name "TEST delete", email `test+<key>@dcinspect.com.au`, mobile 0400000000), then `run_workflow_draft`.
   - Pass = page 200 with form + pixel, and `/api/lead` returns `{"ok":true}`.
   - This cloud session can't reach go.dcinspect.* directly; Zapier can.

## 5. Meta ad (paused) + desk card
1. Copy the final mp4 and a thumbnail to `sites/public/img/<key>.mp4` / `<key>-thumb.jpg`, commit, push, and wait for the deploy.
2. Windsor `facebook`:
   - `create_ad_video` with `video_url=https://go.dcinspect.<tld>/img/<key>.mp4`.
   - Then `create_ad`, status **paused**:
     - `page_id` 100943435016413 (AU)
     - the video id and thumbnail
     - the copy
     - `link` = page URL + `?utm_source=meta&utm_medium=paid&utm_campaign=<campaign>&utm_content=<key>`
3. **Ad set (David's choice: reuse existing campaigns):**
   - AU → the best current ad set in "Building Inspections - Construction & Pre Purchase" (A2 went into "Warm Leads - Facebook + Instagram", `120240471624270220`).
   - HR → the best active HR ad set by cost per lead over the last 14 days.
   - Never create campaigns or change budgets here.
4. **Desk card** (Ad Desk AU https://claude.ai/artifact/5H47w3oGCLjeMoXJv1HiNJ, HR https://claude.ai/artifact/J8BNLzkpTd6GRcSiw8ng2Z):
   - Upload the video and thumbnail to the desk's asset store (Artifact publish `asset:true` with `file_paths`; read the artifact first).
   - Then `ArtifactData` `set` into `cards/<key>` with every field in PLAN.md "Ad Desk": `jeremy_score`, `jeremy_notes`, all six `gates` with notes, `landing_url`, `ad_id`, `adset_name`, `status: "review"`, `created_at`.
   - The landing page link is how David reviews the page.

## 6. Finish
- **Commit everything** except renders: specs, landers, notes in `creative/<batch>/README.md`.
- **Run summary in the session:**
  - each ad's Jeremy scores (ad + page)
  - the desk links
  - anything skipped and why
  - anything David must do (DNS, connector, missing facts)
- **Never:**
  - publish or enable an ad (David approves on the desk)
  - spend money or change budgets
  - submit leads with real customer details
  - put customer report content or addresses in the repo
