# DC Building Inspectors — Meta Ads Engine (AU + HR)

Status: planning · started 2026-10-12

## Goal
Run a steady flow of Meta video ads for two separate accounts. Each ad is produced, checked by gates, critiqued by Jeremy AI, then approved by David on mobile. Once approved, it publishes automatically.

| | AU | HR |
|---|---|---|
| Meta ad account | 449816980394949 | 1386746812476820 |
| GHL sub-account | YGgCKbEtY4u8fRX0Zvfo | fSPTLOI7MAzy9VUHFa2k |
| Market | Melbourne + metro | All of Croatia |
| Language / voice | English, Australian accent | Croatian, native |
| Budget | A$100/day (new) | €250/day (keep) |
| Baseline | No Meta data. Google leads close at ~10% | CPL €15–20, ~15% lead→booking, ~€350/job |
| Competitor research | Yes (AU only; never copy) | **None.** Original angles only |
| Ad desk | Ad Desk AU (new) | Ad Desk HR (new) |

The two accounts never share a desk, a card, an ad set or a publish call.

## Offer & proof (AU)
- Construction stages: Slab, Frame, Lock-up, Pre-plaster, Fixing (incl. waterproofing) at $600 each. PCI/Practical Completion $726. Premium PCI $1,490.
- Pre-purchase building & pest, priced by size: $550 (1–3 bed apt), $605 (2 bed), $605 (3 bed), $649 (4 bed), $715 (house on stumps), $847 (5 bed), Premium $1,375.
- Main differentiator: **same-day report, or you don't pay.**
  - Condition (David, 2026-10-12): whatever day the inspection happens, the report is sent that same day, or the client gets their money back.
  - Ad wording: "Your report the same day we inspect, or your money back."
  - Still to confirm with David: full refund or partial, and any exclusions (e.g. no access to the property).
- 529 Google reviews, 4.9★. BPC registered building inspector, DBU-66182 (never say "VBA registered").
- Tagline: "Inspect Confidently, Build Fearlessly"

## Offer & proof (HR)
- Leak detection, damp, and waterproofing. Topics: burst pipes, rising damp, balcony/terrace waterproofing, shower leaks, drainage leaks.
- Same-day report guarantee. 5★ on Google from 13 reviews.

## Brand rules for creative
- Logo only on hi-vis jackets and hard hats. Small and minimal. **No logo overlays on video.**
- Colours: #3483FA blue, #22C3FF cyan, #1E1E24 ink, #FAFBFF white. Font: Manrope.
- Voice: friendly, authoritative, reassuring, a touch of humour. Don't trash builders. Don't copy competitors.

## Pipeline: every ad passes 6 gates before David sees it
1. **Brief:** service × persona × angle × hook. Facts come only from the approved claims list above.
2. **Draft + self-score:** copy is scored against the Jeremy rubric (once captured). Below threshold, it gets rewritten.
3. **Jeremy AI critique:** score and line notes. Revise until it passes the threshold.
4. **Compliance:** ACL claims (no unprovable "best", "guaranteed", fear claims), Meta ad policy, no builder trashing, no competitor lines. A native-language check for HR.
5. **Production + video QA:** HeyGen talking heads / Arcads UGC and B-roll, 15–30s, 9:16 and 4:5. Checks: lip sync, accent, artefacts, caption spelling, logo rule, hook within the first 2s.
6. **Ad Desk:** a mobile card with the video, primary text, headline, CTA, landing URL, target ad set, Jeremy score and gate log. Approve → publishes to that account's test ad set. Reject or hold with a note → revise.

## Round-one matrix (3–5 angles × 3 hooks per service)
- AU pre-purchase B&P (FHB, home owners)
- AU construction stages (volume-builder FHB): Slab, Frame, Lock-up, Pre-plaster, Fixing/Waterproofing, PCI
- HR leak detection and waterproofing: burst pipes, rising damp, balcony, shower, drainage

## KPIs tracked per ad
Hook rate (3s views / impressions), hold rate, CTR, landing page view → lead, CPL, lead → booking, cost per booked job.
The "40–50%" dream target needs a named stage (see open questions).

## Open dependencies
- Jeremy AI (jeremy.utari.ai) can't be reached from this cloud environment (DNS doesn't resolve). Until it can be, use a paste loop or a browser bridge.
- HeyGen: connected (2026-10-12). Avatar and voice ids are in CLAUDE.md.
- Pixel/CAPI and GHL → Meta booked-job passback still need verifying.

## Decisions (2026-10-12)
- Jeremy AI pass mark: **8/10 or higher**. Every hook, script, ad copy, landing page, campaign structure and HR tone gets Jeremy's input.
- The 40–50% target applies to **lead → booked job**.
- Talking heads: HeyGen with David's custom avatar "David in a black shirt". Everything else: Arcads.
- Each ad gets its own Meta landing page. Base the layout on the existing GHL landing pages. Jeremy reviews each page before it goes to David.
- On approval, the ad goes live **immediately** in that account's test ad set.
- Structure: one testing campaign per account (budget set at campaign level), then winners move to a scaling campaign. Confirm with Jeremy.
- Real footage comes from the Google Drive social folders already used for the Draft Desks.
- Deadline: as soon as possible (today if we can). Blocked until Jeremy AI and HeyGen are connected.

## Connection setup (needed)
- Network allowed domains: jeremy.utari.ai, utari.ai, api.heygen.com, upload.heygen.com, dcinspect.com.au, inspection.dcinspect.com.au, dcinspect.eu, www.facebook.com
- Environment secret: HEYGEN_API_KEY (and JEREMY_API_KEY if Utari provides an API)

## Decisions (2026-10-12, round 2)
- HR leads: the team calls instantly or same day. The CRM still needs a "Booked" stage and no-answer stages that are actually used, or the booking rate can't be measured.
- **Must do:** send booked jobs from GHL back to Meta via the Conversions API, for both accounts. Use a GHL workflow per sub-account (trigger: opportunity enters Booked / Won), with Schedule as the booking event and Purchase plus job value as the paid event.
  - AU: pixel 821976388791436
  - HR: pixel 608006939071812, plus the HR lead-form page 658374350686787
- AU landing pages: David leans toward no prices. Put this to Jeremy, then A/B test.
- Epoxy campaign stays off.
- Placements: Facebook and Instagram feeds, stories and reels only. Exclude Audience Network (92% accidental clicks on Epoxy).

## Ad Desk (built 2026-10-12)
- AU: https://claude.ai/artifact/5H47w3oGCLjeMoXJv1HiNJ (Meta 449816980394949)
- HR: https://claude.ai/artifact/J8BNLzkpTd6GRcSiw8ng2Z (Meta 1386746812476820)
- Source: `desks/desk-template.html`, built into `ad-desk-au.html` / `ad-desk-hr.html` with sed.
- How it works:
  1. Claude creates each ad **paused** in that account's test ad set (Windsor `create_ad_video` → `create_ad`).
  2. Claude writes a card to the desk's db collection `cards` (one doc per ad).
  3. David approves → the page calls Windsor `execute_action` `enable_ad` as David → card status becomes `live`.
- Approve is disabled unless:
  - `account` matches the desk;
  - `ad_id` is set;
  - `jeremy_score` ≥ 8;
  - every gate passes: `brief`, `self_score`, `jeremy`, `compliance`, `video_qa`, `landing`.
- Card fields:
  - Ad and creative: `title`, `service`, `angle`, `format`, `hook`, `primary_text`, `headline`, `description`, `cta` (Meta enum, e.g. LEARN_MORE), `landing_url`.
  - Placement: `account`, `adset_name`, `ad_id`.
  - Media: `video_url`, `thumb_url` (upload to the desk's asset store).
  - Review: `jeremy_score`, `jeremy_notes`, `gates.{key}.{pass,note}`.
  - Tracking: `status` (review|live|paused|held|rejected|check), `created_at`.
- Hold/Reject write `decision.note`. Claude reads held and rejected cards and revises.
- `check` means the approval got no answer from Windsor, so verify the ad in Ads Manager.
