# AU landing-page forms: qualifying questions (approved 2026-10-12)

Scored 8/10 by Jeremy (conversation `809d18b5-6d1f-410a-b9f0-358647e4d345`). David: contact details required.
These are GHL surveys, so this has to be done in the GHL builder: the API token here has no forms/funnels scope.

## Survey settings for both forms
- One question per screen, with the progress bar on.
- **Partial submits ON.** A partial goes to the CRM for follow-up but must **not** fire the pixel Lead. Only `/thankyou` fires Lead.
- Ends on `https://inspection.dcinspect.com.au/thankyou` (unchanged).
- Map every answer to a contact custom field (names below) so the sales team, workflows and CAPI can use it.

## Pre-purchase: inspection.dcinspect.com.au/home-869758 (survey `p38bDK53Y1AubQ0Ogopw`)
| # | Question | Type | Options | Required | Custom field |
|---|---|---|---|---|---|
| 1 | What are you buying? | Single choice | House / Apartment or unit / Townhouse | Yes | `pp_property_type` |
| 2 | How many bedrooms? | Single choice | 1–2 / 3 / 4 / 5+ | Yes | `pp_bedrooms` |
| 3 | Where are you up to? | Single choice | Signed, cooling-off running / Auction date set / Making an offer this week / Just looking for now | Yes | `pp_stage` |
| 4 | Property suburb | Address autocomplete if available, else text | | Yes | `property_suburb` |
| 5 | First name · Mobile · Email | Contact | | All yes | standard |

Notes:
- The current timeline question is stored under the field key `how_many_beds`. Replace it rather than reuse it, so the old data doesn't get mixed in.
- Keep "Just looking for now". Jeremy: cutting it makes tyre-kickers lie and poisons the hot bucket. Route it to nurture, not a same-day call.
- **Email required** is David's call. Jeremy's rule: if drop-off clusters on the last step after ~2 weeks, make email optional again.

## Construction: inspection.dcinspect.com.au/home-8356-3538 (survey `W3Szcw3yRDozoJnHunhS`)
| # | Question | Type | Options | Required | Custom field |
|---|---|---|---|---|---|
| 1 | Where's your build up to? | Single choice | Not started yet / Slab or frame stage / Lock-up to fixing / Finished, handover coming | Yes | `nb_build_stage` |
| 2 | What do you need? | Single choice | All stages package / One stage only / Handover (PCI) inspection / Something specific | Yes | `nb_service` |
| 3 | When is your next stage or handover due? | Single choice | This week / 2–4 weeks / 1–3 months / Not sure | Yes | `nb_next_stage_due` |
| 4 | Build suburb | Address autocomplete if available, else text | | Yes | `property_suburb` |
| 5 | Builder's name | Text | | **No** (call prep only, never used in ads) | `nb_builder` |
| 6 | Full name · Mobile · Email | Contact | | All yes | standard |

## Thank-you page: hot buckets get the booking link (Jeremy's biggest upgrade)
- Show "Need it this week? Lock in your inspection time now →" linking to `dcinspect.com.au/online-bookings` **only** when:
  - `pp_stage` = Signed, cooling-off running **or** Auction date set, **or**
  - `nb_next_stage_due` = This week.
- GHL route: survey "redirect on submit" rules (conditional redirect), sending hot answers to `/thankyou-book` (a copy of `/thankyou` plus the booking block).
- **Both thank-you pages must fire the pixel Lead.**
- The online-booking confirmation must fire **Purchase with value + AUD**. Verify it in Events Manager → Test events.

## Call priority (GHL workflow on form submit)
| Bucket | Answers | Action |
|---|---|---|
| Hot | Signed / Auction date set / This week | Instant SMS + call task within 5 min |
| Warm | Making an offer this week / 2–4 weeks | Call same day |
| Cold | Just looking / 1–3 months / Not sure | Nurture sequence, no same-day call, tag `nurture` |

## Page fixes found while checking (needed for Jeremy's congruency score)
- **Proof:**
  - Pages say "400+ 5-star reviews". Use **529 Google reviews, 4.9★** to match the ads.
  - Inspection counts disagree: 6,500+ on one page, 10,500+ on the other. Pick one true number.
  - "Registered/Qualified Inspectors" → "BPC registered building inspector (DBU-66182)".
- **Wording:**
  - Typo: "Same day report GURANTEED" in the pre-purchase FAQ.
  - The guarantee line should read exactly: "Your report the same day we inspect, or your money back."
