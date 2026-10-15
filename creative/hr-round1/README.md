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
| hr-d1-kapilarna-vlaga (carousel ×5) | n/a | 120254265547920195 (LIVE 2026-10-15) |
| hr-e1-tri-greske (carousel ×5) | n/a | 120254265669630195 |
| hr-e3-nakon-klika (carousel ×5) | n/a | 120254265670730195 |

## D1: rising damp carousel (David: "static carousel for rising damp… besplatna ponuda")
- Jeremy 7 → 8.5: card 1 leads with the pain ("Boja se ljušti uz pod?"), not the category; "besplatna ponuda" is the closer (card 5, headline, primary text), not the hook. Keep card text under ~20% of the area.
- Cards built with `creative/template/build_carousel.py` from `hr-d1-kapilarna-vlaga/carousel.json`. Images hosted at go.dcinspect.com.au/img/hr-d1-card{1..5}.jpg; the ad uses `link_data.child_attachments[].picture` + the lead form on each card.
- Photos: meter at the skirting + meter close-up (frames of Drive `14eG9V…`), thermal (`themral.jpg`), detection kit (Drive `IMG_6352.HEIC`).

## E1 / E3: more rising damp carousels (David: "create more carousels to do with kapilarna vlaga")
- Jeremy: E1 "3 greške" (regret: already painted/re-plastered) 8.5; E3 "što se događa nakon klika" (process transparency, expected to bring the best-qualified leads) 8.5.
- **Parked: E2 "znakovi" checklist (7/10).** Needs a real salt-line / peeling-skirting photo shot on site; without it the sign cards don't show the sign. Build it when David sends that photo.
- Dropped from Jeremy's E3 draft: "Traje 2 minute" (unverified form length) and "Sanacija uključena u rješenje" (could read as free repair).
