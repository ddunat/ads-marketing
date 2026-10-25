# AU carousels round 1 (2026-10-25): 10 static carousels, Meta lead form

David asked for static carousel ads built the same way as the HR ones, using the Meta lead form. He wanted 5 pre-purchase and 5 construction, with prices shown on construction only ($3,095). Audiences: first home buyers, investors, auction buyers and private-sale buyers. **Strict target: cost per lead ≤ A$30.**

- Copy and Jeremy scores are in `copy.json` (conversation 4efb7880). Card specs are in `au-*/carousel.json`, the 40 Arcads images in `img-ai/`, and the review strips in `strips/`.
- Card images for Meta are in `sites/public/img/au-*-card{1..5}.jpg`. Meta fetched them from raw.githubusercontent.com at commit d0322dd, because Windsor file upload and Railway weren't reachable from this session. Meta keeps its own copy once the ad is created.
- Structure (Jeremy): one ad per ad set, so every angle gets spend, and construction in its own campaign. Every ad set is A$10/day, Melbourne 50 km, ages 25–65, FB + IG feeds/stories/reels, no Audience Network. Campaigns and ad sets are active; the ads are paused, so nothing spends until David approves a card on the AU desk.
- Form: the existing AU form `753250670189751` ("Lead Form").
- **Gap: AU GHL has no Facebook lead-form connection.** Leads stay in Meta Leads Center until David connects it in GHL, or until a Zapier relay is built.
- **GST:** if $3,095 is ex GST, the construction ads have to show $3,404.50.

| Key | Campaign | Ad set | Ad (paused) | Jeremy |
|---|---|---|---|---|
| au-p1-first-home | 120253063944870220 (Pre-purchase) | 120253063946990220 | 120253063953830220 | 9 |
| au-p2-investors | 〃 | 120253063954900220 | 120253063967190220 | 8.5 |
| au-p3-auction | 〃 | 120253063955440220 | 120253063968830220 | 9 |
| au-p4-cooling-off | 〃 | 120253063956260220 | 120253063976040220 | 9 |
| au-p5-same-day | 〃 | 120253063957290220 | 120253063977790220 | 9 |
| au-c6-pre-plaster | 120253063946060220 (Construction) | 120253063959460220 | 120253063979570220 | 9 |
| au-c7-frame | 〃 | 120253063960410220 | 120253063992560220 | 8.5 |
| au-c8-handover | 〃 | 120253063961110220 | 120253063995780220 | 9 |
| au-c9-independent | 〃 | 120253063962110220 | 120253064000390220 | 9 |
| au-c10-package | 〃 | 120253063962540220 | 120253064004930220 | 8.5 |
