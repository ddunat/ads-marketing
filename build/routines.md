# Routines to create (claude.ai → Code → Routines → New routine)

Create both routines yourself in the claude.ai Routines screen. Routines created by Claude from a session can't carry your connectors, and both of these need them.

**Settings for both:**
- **Repository:** `ddunat/ads-marketing`, branch `master`.
- **Environment:** the same one this project uses. It has the HeyGen key, the Jeremy token and the allowed domains.
- **Connectors:** Windsor.ai, Google Drive, Zapier, Railway.
- **New session each run:** yes.
- **Notifications:** on.

---

## 1. Weekly ad factory
**Schedule:** every Monday at 1:47am, Melbourne time. Ads are on your desks before 8am.

**Prompt:**

You are running the weekly ad factory for DC Building Inspectors (repo ddunat/ads-marketing, branch master). David approved this routine on 2026-10-14. He only reviews the finished ads and landing pages on his Ad Desks, so everything before that is yours.

Do this:
1. `git checkout master && git pull`.
2. Read CLAUDE.md and PLAN.md ("Weekly ad factory").
3. Invoke the `make-ad` skill (`.claude/skills/make-ad/SKILL.md`) and follow it exactly. That means:
   - Decide the batch from last week's results: up to 3 AU + 2 HR, replacing the ads the daily check killed, at least 1 per account.
   - Pick angles with the Kaleidoscope rule and get Jeremy (MCP server `jeremy`) to vet them.
   - Per ad: script and copy until Jeremy scores ≥ 8, HeyGen v3 video, the templated edit, its own landing page (Jeremy ≥ 8), deploy, smoke test, a PAUSED Meta ad, and the Ad Desk card.
4. Skip HR if `sites/landers/markets.json` still has TODO values or `go.dcinspect.eu` isn't live yet, and say why.
5. If a connector you need (Windsor.ai, Google Drive, Zapier, Railway, Jeremy) isn't available, do every step you can, then stop and say exactly what was missing.

Hard rules:
- Never enable an ad, change a budget or create a campaign.
- Never put customer details or report contents in the repo.
- Never mix the AU and HR accounts.
- Follow CLAUDE.md compliance: David is Director, BPC wording, exact guarantee, no VBA.

Finish with a short summary for David:
- each ad's Jeremy scores (ad and page)
- the desk links: AU https://claude.ai/artifact/5H47w3oGCLjeMoXJv1HiNJ, HR https://claude.ai/artifact/J8BNLzkpTd6GRcSiw8ng2Z
- anything skipped and anything he must do

---

## 2. Daily ad check (kill / scale)
**Schedule:** every day at 7:47am, Melbourne time.

**Prompt:**

You are running the daily ad check for DC Building Inspectors (repo ddunat/ads-marketing, branch master). David approved this on 2026-10-14: pause losers automatically, only ever propose budget increases.

Do this:
1. `git checkout master && git pull`.
2. Read CLAUDE.md.
3. Invoke the `ad-ops` skill (`.claude/skills/ad-ops/SKILL.md`) and follow it exactly, for AU (Meta 449816980394949) and HR (Meta 1386746812476820) separately.
   - Pause ads that hit the kill rule, and update their Ad Desk cards with the reason.
   - Write budget proposals for winners to the desk's `proposals` collection.
   - Record the week's kill counts in the desk db `stats/<YYYY-WW>`.

Hard rules:
- Never raise a budget, enable an ad or create anything in Meta.
- HR is report-only until David sets an HR target.

Finish with a 5-line summary: paused (with reasons), proposed, too early to judge, and anything David must do.
