# HR round 1 (2026-10-15): Instant Form video ads

David: "new ads, with the facebook form attached… analyse my existing ads, pick my winners and create some killer ads with those themes… consult Jeremy and Alex." No landing page for HR.

## Winners (HR account, last 30 days, all in "DC Building Inspectors HR" / Adv Plus, Instant Form)
| Ad | Spend | Leads | CPL |
|---|---|---|---|
| Video Leaks | €2,442 | 134 | €18.2 (volume winner) |
| Pipe Leak | €323 | 19 | €17.0 |
| Coughing (smell-of-damp copy) | €74 | 5 | €14.8 (early) |
| Mould | €382 | 19 | €20.1 |
| Video Leaks, new copy | €561 | 27 | €20.8 |
| Video Rising Damp | €612 | 29 | €21.1 |
| Wall Rising Damp (image) | €2,914 | 125 | €23.3 (was €14 over 180 days: fatigued) |

## Setup
- **Form:** `2898956873609451` ("Untitled form 6/2/25, 9:17 PM-copy"). Every winning ad's leads in GHL HR carry this form id (`contact_first_attribution_medium_id`).
- **Page:** 658374350686787. **Ad set:** Adv Plus `120227138979370195` (campaign `120227138979360195`). The existing ads stay untouched; the generic-copy Video Leaks is the control.
- **CTA:** GET_QUOTE ("Zatražite ponudu").

## Guarantee (Jeremy, 2026-10-15; David to confirm on the desk)
- **Lead (A, B only):** "Ako ne pronađemo izvor curenja vode, detekciju ne plaćate." Scoped to active water-pipe leaks. Not for moisture-source / mould / rising-damp diagnosis. Fine print for the form/confirmation: active water leaks only, normal access needed; if no leak is active on the day, one free reschedule.
- **Secondary:** "Hitno curenje? Dolazimo isti dan." (capacity-dependent, so not a guarantee).
- **C** uses the same-day written report as its risk reversal instead.
- Never in ads: prices, health claims about mould ("zdravlje", coughing, children), the Zagreb base.

## The three ads (Jeremy scores)
| Key | Angle | Kaleidoscope | Score |
|---|---|---|---|
| hr-a1-bez-plocica | Find the leak without breaking tiles + guarantee + same-day urgent visit | remix of Video Leaks | 9 |
| hr-b1-racun-za-vodu | Hidden leak: rising water bill / ceiling stain / neighbour below | remix of Pipe Leak | 8 |
| hr-c1-plijesan | Mould keeps coming back: the source is behind the wall (thermal proof) | new (from Coughing signal) | 9.5 (after rewrite from 7.5) |

Copy is in `copy.json`; spoken scripts in `scripts.json`.

## Production notes
- HeyGen v3 returns no caption file for Croatian. Captions come from the script, timed with an Arcads (ElevenLabs) transcription.
- David's cloned voice is an English voice. It said "kurenje" for "curenje". Scripts sent to HeyGen respell `c` as `ts` where needed; captions keep the correct spelling.
- Proof shot: David's thermal photo (Drive "Construction Defect Photos/themral.jpg"). B-roll: moisture meter on a wall (Drive `14eG9VaHrTOmysGg4eCnmAhyiDRQ218eu`, 1.0–4.1s, checked: no faces, numbers or signage).

## Meta (created paused 2026-10-15, on the HR desk for approval)
| Key | Video id | Ad id |
|---|---|---|
| hr-a1-bez-plocica | 2151669585386810 | 120254265466600195 |
| hr-b1-racun-za-vodu | 1322515779905037 | 120254265467940195 |
| hr-c1-plijesan | 1104090375540864 | 120254265471460195 |
