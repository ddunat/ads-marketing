# Meta Ads audit: 2026-10-12 (read-only, Windsor.ai)

## AU: 449816980394949 (AUD)
- Not live since 2026-04-05. Lifetime total, Mar 2025–Apr 2026: about A$44.7k spend, 192 pixel leads, CPL about A$233.
- Every ad set: OUTCOME_LEADS, optimising for offsite conversions (pixel 821976388791436, LEAD event), traffic sent to a website landing page.
- Best ads (CPL):
  - Pre Slab (image): A$159
  - Pre Purchase – Brick Crack (video): A$164
  - Roof Defect + Client: A$168
  - Roof Void: A$190
- Worst ads:
  - Frame Collapse: A$1.7k for 2 leads
  - Construction Stages: A$7.4k for 21 leads, and only 81 landing page views from 2,102 clicks
  - Leaks video: A$403, 0 leads
- Landing pages:
  - inspection.dcinspect.com.au/home-869758 (pre-purchase): landing page view → lead about 2.3%
  - /home-8356-3538 (construction): about 1.5%, CPL A$351
- UTMs: missing on almost every ad. The one ad that has them is malformed.
- GHL AU: 238 Google opportunities created since 14 Jul, 39.5% won.

## HR: 1386746812476820 (EUR)
- 180 days:
  - €27.5k spend, 1,670 leads, blended CPL €16.48.
  - The instant-form campaign alone ran at €14.72 CPL.
- Last 30 days: €7.5k, 376 leads, CPL €19.95. Frequency is 3.81, so the audience is getting fatigued.
- Wasted spend:
  - Epoxy campaign: €2.65k for 0 leads. 92% of its clicks came from Audience Network.
  - The pixel Lead event (pixel 608006939071812) never fires on the GHL funnel.
- Top ads by CPL:
  - Pipe Leak: €13.6
  - Wall Rising Damp (image): €14.0 over 180 days, but €22.3 in the last 30 days
  - Video Leaks: €14.3
  - Mould: €15.4
  - Video Rising Damp: €17.9
- Copy: almost every ad uses the same text, "Prijavite se za besplatnu ponudu! 👌".
- Cheapest placements and audiences: Facebook feed €13.45. Women aged 55+ cost about €12 per lead.
- Instant form: click → lead 5.2%.
- GHL HR, last 90 days:
  - 608 Meta opportunities, 40 won (6.6%), about €336 per job.
  - 546 of them are still in "New Leads – Facebook", so the real booking rate is unknown. 6.6% is a floor.
  - Only about 71–87% of the leads Meta counts show up in GHL.

## Measurement gaps
1. Booked jobs aren't sent back to Meta (no CAPI or offline Schedule/Purchase events) in either account.
2. GHL pipeline stages aren't kept up to date. There's no "Booked" stage with a timestamp.
3. The pixel Lead event doesn't fire on GHL funnel pages (HR). The AU web funnels have very low landing page view → lead rates.
4. UTMs are missing or broken.
5. Leads go missing between Meta and GHL (13–29% a month).
