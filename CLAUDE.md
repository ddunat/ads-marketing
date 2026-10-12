# DC Building Inspectors: Meta Ads engine

Start here: read `PLAN.md` (decisions, pipeline, gates), then `research/`. Every ad is built to `research/acq-ad-playbook.md` (ACQ handbook checklist) and then scored by Jeremy (`research/jeremy-rubric.md`).

- Two Meta ad accounts, never mixed: AU `449816980394949`, HR `1386746812476820`. Access is through the Windsor.ai `facebook` connector.
- GHL sub-accounts: AU `YGgCKbEtY4u8fRX0Zvfo`, HR `fSPTLOI7MAzy9VUHFa2k`.
- Arcads brand: DC Building Inspectors `4bdc3af2-9a92-40e0-a844-8fb35c64e3c4`.
- HeyGen: base `https://api.heygen.com`. The network proxy injects the API key on every request, so `HEYGEN_API_KEY` may be unset in the shell (that's fine). `GET /v2/avatars` often 502s; use `GET /v2/avatar_group.list?include_public=false` then `/v2/avatar_group/<id>/avatars`.
  - David's avatar "David in a black shirt": use the motion look `b6820f0449eb4e3aab591fc44c75fcce` (group "David" `e4d7f0347f844b12a4f36fa6282aa877`). Photo looks: `389a1d384e5f425b87feed5f055b1fb4`, `0ec9b568ce384f1791a9bf9d56cb7cc5`.
  - Linked voice: `fe2230b3ddee436fb50c6ebc9b44f1e5` ("David - Voice"). The "David Teeth" group uses another clone, `a6a5b9eefab0495390be965878a0415e`.
- Ad Desks (claude.ai artifacts, source in `desks/`): AU https://claude.ai/artifact/5H47w3oGCLjeMoXJv1HiNJ · HR https://claude.ai/artifact/J8BNLzkpTd6GRcSiw8ng2Z. See "Ad Desk" in PLAN.md for the card format.
- Jeremy AI: MCP server `jeremy` in `.mcp.json` (https://persona-mcp.utari.ai/mcp/). The token comes from the environment secret `JEREMY_TOKEN`; never write it into the repo. Needs `persona-mcp.utari.ai` in the environment's allowed domains. Fallback: Claude in Chrome on David's computer, or a paste loop. Pass mark is 8/10.
- Never publish without David's approval on the Ad Desk for that account. On approval, the ad goes live immediately in the test ad set.
- David is the director. He subcontracts the inspections and does not inspect himself. Never write "your inspector", "I inspect" or anything else implying he does the inspection; use "we", "our team" or "David Dunat, Director". Inspections are done by BPC registered subcontractors and qualified trades: say "BPC registered building inspectors and qualified trades". DBU-66182 is David's own registration, so only attach it to his name.
- Compliance: never "VBA registered". Use "BPC registered building inspector, DBU-66182" (Building and Plumbing Commission, Victoria). No builder names or signage. Guarantee wording: "Your report the same day we inspect, or your money back." Full refund, no exclusions. No Meta personal-attribute framing.
