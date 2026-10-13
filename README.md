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
