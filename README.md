# ads-marketing

Google Ads management for DC Building Inspectors (account 538-044-4374, campaign
"Building Inspection Leads - DAVID DUNAT", id 22176911422). Moved here from the
`claude/google-ads-review-uwxh6c` branch of `ddunat/DC-Inspect-App`.

| File | What it is |
|---|---|
| `ads-keyword-routine-prompt.md` | The daily 07:49 Melbourne keyword review: performance, search-term negatives, verification traps, keyword rules. The source of truth for the routine's prompt. |
| `ads-dashboard.html` | Scale-or-hold dashboard (LTGP : CAC ≥ 3:1 gate), published as a claude.ai Artifact with live Windsor.ai data. Omits the `<!doctype>` skeleton, which the Artifact platform supplies. |

## Change log
- **7 Oct 2026** — Saturday removed from the ad schedule (Mon–Fri only, Friday −20%).
- **9 Oct 2026** — negatives added (PHRASE): `first national`, `property evaluators`, `water leak detection`. All three verified live.
- **13 Oct 2026** — negatives added (BROAD): `buywiseinspections` (competitor domain, $30.58 click) and `buywise`. A PHRASE `buywise` already existed but cannot block the one-word domain search — negatives match whole words. Both verified live.
- **20 Oct 2026** — negative added (BROAD): `bhk` (Indian real-estate term for bedroom/hall/kitchen; "3 bhk house" was property browsing, not an inspection search). Verified live; brand term `dcinspect` confirmed not negated.
- **22 Oct 2026** — negative added (PHRASE): `australian property & building inspections` (competitor brand, $1.25 click). Verified live, but redundant: PHRASE `australian property & building` and `australian property and building` already existed — Google likely ignores the "&", so the older negatives may not be catching this variant. Brand control `dc building` confirmed not negated.
- **24 Oct 2026** — negative added (BROAD): `termguard` (termite-barrier product brand, $26.98 click — not an inspection search). Verified live and genuinely new; brand control `dc building` confirmed not negated.
