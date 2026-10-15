---
name: ad-ops
description: Daily check of live DC Building Inspectors Meta ads against Jeremy's kill/scale rule. Pauses losers automatically (David approved this), proposes budget increases for winners on the Ad Desk, and reports. Use when the daily ops routine fires or David asks "how are the ads doing", "kill the losers" or "what should we scale".
---

# ad-ops: daily kill / scale

David approved: **pause losers automatically; scaling is only ever proposed** (Ad Desk → Budget tab). Never raise a budget yourself, never enable an ad, never create campaigns.

## Data (per account, never mixed)
- **Meta (Windsor `facebook`), per ad**, last 7 days and lifetime: `ad_id`, `ad_name`, `adset_id`, `campaign_id`, spend, leads, and the ad's status. AU is `449816980394949`; HR is `1386746812476820`.
  - Windsor caches data and this plan has no hourly refresh. Use `date_preset` ranges ending yesterday and say so in the summary.
- **Bookings per ad (GHL via Windsor `gohighlevel`):**
  - Use opportunities and contacts tagged `booked-meta`, joined to the ad by the contact's `landing_page` / `lp-<key>` tag and `utm_content`.
  - Only ads with their own landing page can be judged on bookings. Others fall back to CPL against the account's 30-day median.
- **The desk cards** (`cards` collection on the account's Ad Desk) map `ad_id` to the card.

## Rules, AU (target $50 per booked inspection, `build/cost-per-booking-plan.md`)
- **Too early to judge:** live < 72 hours, or lifetime spend < $100. Do nothing.
- **Kill, i.e. pause automatically:**
  - lifetime spend ≥ $150 with 0 bookings; or
  - lifetime spend ≥ $300 and cost per booking > $100.
  - Before pausing, re-read the ad's current state. Pause with Windsor `pause_ad`.
  - Then update its desk card: `status: "paused"`, `paused_at`, and `paused_reason` (one plain sentence with the numbers, e.g. "Spent $162 with no bookings (rule: cut at $150 with none)").
  - If the card is missing, still pause and say so in the summary.
- **Scale, i.e. propose only:**
  - Trigger: last 7 days ≥ 2 bookings at ≤ $50 each, and the ad has been live ≥ 72 hours.
  - Write `proposals/<date>-<ad_id>` on the desk with:
    - `account`, `title` ("Scale A2: $41 per booking")
    - `target_type` `campaign` if the campaign uses campaign budget (AU does), else `adset`; plus `target_id` and `target_name`
    - `current_amount` and `proposed_amount` in cents: +20%, rounded to whole dollars, at most +30%
    - `currency`, `reason`, `metrics: {spend, bookings, cost_per_booking}`, `status: "pending"`, `created_at`
  - One open proposal per campaign/ad set at a time. If one is still pending, update its numbers instead of adding another.
  - Don't propose again within 48 hours of an applied change (Jeremy: let it settle).
- **Never edit a live winner's creative while scaling.**
- **Only desk-approved ads run.** If you find an active ad in either account with no desk card (e.g. an old pre-desk ad someone switched back on), pause it and say so in the summary.

## Rules, HR (target €15–20 per booked job, David 2026-10-15; judge against €20)
Same logic as AU, in EUR, scaled to the HR target:
- **Too early to judge:** live < 72 hours, or lifetime spend < €40. Do nothing.
- **Kill, i.e. pause automatically:**
  - lifetime spend ≥ €60 with 0 bookings; or
  - lifetime spend ≥ €120 and cost per booking > €40.
  - Same steps as AU: re-read state, `pause_ad`, update the HR desk card with `paused_reason` in plain English with the numbers.
- **Scale, i.e. propose only:** last 7 days ≥ 2 bookings at ≤ €20 each, live ≥ 72 hours. `target_type` `adset` unless the HR campaign uses campaign budget. Same proposal format, `currency` EUR, written to the HR desk.
- HR bookings come from the HR GHL sub-account (`fSPTLOI7MAzy9VUHFa2k`). Until HR booking tags (`booked-meta`) are flowing, fall back to CPL against the account's 30-day median and say so.

## Output
- **A short summary in the session:** per account, the ads checked, paused (with reason), proposed, and too-early-to-judge, plus anything that needs David.
- **Note "killed this week" counts** for the weekly make-ad run. Store them in the desk db `stats/<YYYY-WW>`: `{killed_au, killed_hr, updated_at}`.
