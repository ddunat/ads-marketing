# Daily Google Ads keyword review — routine prompt

Create this at **claude.ai → Routines → New**:

- **Schedule:** daily, 07:49 Melbourne
- **Connector:** attach **Windsor.ai** (this is the step the API cannot do — without it the routine
  runs and silently does nothing)
- **Notifications:** push on
- **Prompt:** everything below the line

---

Run today's Google Ads keyword review for DC Building Inspectors (Melbourne pre-purchase building
& pest inspections). Account 538-044-4374 — pass as `accounts: ["5380444374"]`. Campaign
"Building Inspection Leads - DAVID DUNAT", campaign_id 22176911422. Target cost per conversion $70.
Daily budget $250.

FIRST load Windsor: ToolSearch `select:mcp__Windsor_ai__get_data,mcp__Windsor_ai__execute_action`.
If the tools will not load, or calls fail as unauthorised, report in one line that Windsor.ai needs
reconnecting in claude.ai Settings > Connectors, and stop. Do not use Search Atlas as a substitute —
account 538-044-4374 is not connected there, and the nearest account has not synced since January.

## 1. Performance
`get_data` connector `google_ads`, fields `["date","impressions","clicks","spend","conversions"]`,
last 8 days, filter `[["campaign_id","eq","22176911422"]]`. Report the daily table plus 7-day CPC,
CPA, CTR and conversion rate against the $70 target. The ad schedule is Mon–Fri only (Saturday
removed 7 Oct after five Saturdays cost $243.66 per conversion; Friday runs at −20%), so missing
Saturday and Sunday rows are correct, not a fault. Yesterday's figures mature for a day or two —
never read a same-day number as final.

## 2. Search terms — add negatives automatically
Fields `["search_term","clicks","spend","conversions","impressions"]`, last 3 days, filters
`[["campaign_id","eq","22176911422"],["clicks","gt",0]]`.

David approved automatic negatives for clear junk: competitor brands and named competitor
inspectors; real-estate agencies; wrong services (mould, roofing, energy ratings, gas compliance,
valuations, smoke alarms, concrete testing, water-damage restoration); permits, certificates, VCAT;
training courses; "open for inspection" browsing; anywhere outside Melbourne metro.

`execute_action`, action `push_negative_keywords`, account `"5380444374"`, params
`{level:"campaign", campaign_id:"22176911422", keywords:[{text, match_type}]}`.
PHRASE for multi-word brands, BROAD for distinctive single tokens.

**Never negate services DC sells:** pre-purchase, building & pest, timber pest/termite,
PCI/handover, practical completion, frame/stage, pre-slab, dilapidation, waterproofing, apartment,
pre-settlement, pre-auction.

**Never negate Melbourne suburbs** — Cranbourne, Frankston, Berwick, Pakenham, Werribee, Brunswick,
Bayside, Melton, Clyde North and the rest are good traffic.

**Never negate DC's own brand** — "dc building inspectors", "dc inspections", "david dunat", brand +
"reviews". These are the cheapest clicks in the account.

**Keep negatives narrow.** A single-word BROAD negative can silently block a service DC sells.
`concrete` and `bathroom` were added BROAD by something else and had to be removed on 6 Oct because
they blocked pre-slab and bathroom-waterproofing enquiries. Prefer the specific phrase over the
bare word.

**Do not negate generic service language on a hunch that it is a brand.** "professional inspection
services" looked like a competitor and was nearly negated on 30 Sep; it converted on 1 Oct. If a
term is plausibly a customer describing what they want, leave it and note it for tomorrow.
`house report` and `unit inspection` were left alone on 6 Oct for the same reason.

## 3. Verify every write — and two traps that make a correct write look broken

Never report a change as done on the API success message alone: it reported "Added 12" when 11 were
new, and "Added 2" when 1 was new.

**Trap A — Windsor caches an identical `get_data` query.** If the read-back uses the *same*
parameters as a read made before the write, you get the pre-write snapshot and the change looks like
it failed. On 6 Oct this made a successful removal of `concrete` and `bathroom` look like a failure.
Always vary the read-back — a different `date_preset`, or a narrow filter on just the affected
terms — so it is a fresh pull.

**Trap B — the `in` filter does not match multi-word criterion text.** Verifying `i spect` with an
`in` filter wrongly showed it missing. For multi-word terms, pull the full criterion list and grep it.

Read back with fields
`["campaign_criterion_keyword_text","campaign_criterion_keyword_match_type","campaign_criterion_negative","campaign_id"]`.
That pull is large and gets written to a file: use `jq` on it, guard nulls before `ascii_downcase`,
and note `campaign_criterion_negative` comes back as the strings "True"/"False". **Include a term
you did not touch as a control.** Report how many were genuinely new.

## 4. Keywords
Fields `["keyword_text","clicks","spend","conversions","impressions"]`, last 14 days, same campaign
filter.

**Never remove a positive keyword.** David's rule, 6 Oct: pause only, and only when genuinely
required. Pausing (`update_keywords`, status `paused`, keyed on `keyword_criterion_id`) is
reversible and keeps the conversion history that matters.

Only **flag** a keyword after 7+ days of meaningful spend with zero conversions, and ask David
before pausing it. Never recommend pausing a keyword that converted recently: `building inspector
melbourne` looked dead for six days, then produced 11 conversions and became a top performer.
Conversions lag clicks by days, so zero today may convert this week.

On watch, both at zero, neither to be touched: `building inspection near me`, `pre purchase
inspections`.

## 5. Removing a negative
Needs its criterion id. Pull field `criterion_id` — **not** `campaign_criterion_criterion_id`, which
returns null — alongside `campaign_criterion_keyword_text`. Then `execute_action`
`remove_negative_keywords` with `level: "campaign"`, `campaign_id` and `criterion_ids`. Verify per
Trap A. Reversible by re-adding the text and match type.

## 6. Report
Numbers first, then what changed and the verification result, then recommendations and why. Be
direct about what is not working, including earlier calls of your own that turned out wrong.

## Constraints
Edits only in Google Ads via Windsor, never Search Atlas. Do **not** turn on Search Partners or
Display. Only account 538-044-4374. Do not change the daily budget, pause the campaign, or pause a
keyword without asking David first.

## Windsor gotchas
`keyword_text`, not `keyword` (`keyword` is a Keyword Planner field and cannot combine with cost
metrics) · `ad_group_id`, not `adgroup_id` · append `T` to any `date_preset` or today is silently
excluded · `google_ads` returns `{result:[...]}`, `gohighlevel` returns `{data:[...]}`.

## Open decisions to re-raise while unresolved
- `concrete inspector` — held back as David's call because DC does pre-slab work.
- The $9,959 of non-Google marketing spend in September — the largest unexamined number in the business.

## Bidding (confirmed 21 Oct)
Bid strategy is Maximise conversions with a $70 target CPA (`campaign_maximize_conversions_target_cpa_micros` = 70000000).
Budget is not the constraint: budget-lost impression share is 0% while ~71–79% is lost to rank. Do not recommend raising the
budget; the lever is the target CPA. David approved (21 Oct) a one-week test at $80 from Mon 26 Oct, applied only if Wed–Fri
21–23 Oct each spend under $150. **Applied and verified 26 Oct: target is now $80** — judge daily CPA against $80
this week. Compare 26–30 Oct against 19–23 Oct at $70 ($763.45, 85 clicks, 12 conversions, $63.62 each), then ask David
whether to keep $80, step to $90, or revert. Judge on leads that close, not cost per conversion alone.
