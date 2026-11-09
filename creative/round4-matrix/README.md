# Round 4 (weekly run 8–9 Nov 2026): first Angle Matrix batch

One new matrix cell per account, 3 versions each, each angle in its own paused ad set (copied from the account's lead-form ad set). Copy and Jeremy loop: `drafts.md`; card specs: `*/carousel.json`; images: `img-ai/` (Arcads nano-banana-2-1, no faces, readings, signage or plates; Q3 parked-car plates blurred).

| Version | Cell | Meta ad | Jeremy |
|---|---|---|---|
| HR N1 "Curi susjedu ispod vas?" | Problem aware × Approval | 120254710030450195 | 9 |
| HR N2 "Susjed kaže da mu curi?" | same | 120254710044140195 | 8.5 |
| HR N3 "Curi u zgradi?" | same | 120254710048370195 | 9 (7.5 → 9) |
| AU Q1 same-day proof | Product aware × Safety (real Google reviews) | 120253333568670220 | 9 |
| AU Q2 clarity proof | same | 120253333572100220 | 8.5 |
| AU Q3 short-notice proof | same | 120253333579930220 | 9.5 |

- Ad sets (paused): HR 120254709983390195 "HR · Angle R4: susjed ispod" (Adv Plus copy, campaign budget); AU 120253333461670220 "AU · Angle R4: review proof" (P1 lead-form copy, A$10/day).
- HR uses Instant Form 2898956873609451. AU uses the OLD form 753250670189751 as a placeholder only: the desk cards say hold until the new Higher-intent form ID is swapped in (Jeremy: duplicate onto the new form rather than edit in place).
- Review quotes are word for word from public Google reviews (first name + initial; David OK'd 5 Nov). Reviews that credit David with the inspection were skipped (David never inspects).
- Build notes: Windsor's file upload host is blocked by this environment's network, so card images went to Meta via Arcads signed URLs (upload → register → fresh get_asset right before create_ad; links expire in 12 h).
- `creative/template/build_carousel.py` gained optional `hsize`/`top` keys for CTA/quote cards (defaults unchanged).
