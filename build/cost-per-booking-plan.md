# Cost per booked inspection: $120 → $50 (Jeremy, 2026-10-12)

**Maths:** cost per booked = CPL ÷ lead-to-book rate.
- Today: $120 booked ≈ $36 CPL at ~30% lead-to-book.
- Target: CPL $20–25 **and** lead-to-book 45–55%, which gives $40–55 booked. Both have to move; one lever alone can't get there.
- Jeremy: $50 is the aggressive end. Even $75 is a 9–13% acquisition cost on a $550–$847 job.

**Levers, in order:**
1. **Speed to lead (free):** a human call within 5 minutes, with Saturday morning covered. Without it the number plateaus at $80–90. *Owner not decided yet.*
2. **Optimisation event:** fire **Schedule** on the website booking confirmation page (dcinspect.com.au/online-bookings), as browser pixel + server CAPI with a shared event_id. Then optimise toward Schedule.
   - This conflicts with the earlier ruling: Lead optimisation until 30–50 bookings a week, because Meta needs ~50 events a week per ad set to exit learning. At $50 per booking that's ~$2,500 a week.
   - **Proposal:** fire Schedule now so the data builds up. Switch the optimisation event once volume supports it, or test a Schedule-optimised ad set alongside the Lead one.
3. **CPL:** a $50 cost-per-result goal on the Schedule-optimised campaign. Creative volume of 10–15 ads in the same hook family, varying the openings, defect footage, report photos and proof cards.
4. **Page/form:** already fine (5% conversion). Report photos and the VSL are in.
5. **Nurture:** the 72h hot SMS sequence (`ghl-nurture.md`) converts leads we've already paid for.

**Test order:**
- **Week 1:** speed to lead + Schedule event.
- **Week 2:** Schedule-optimised campaign with the $50 cost goal + the creative batch.
- Judge nothing before 72h.

**Kill/scale per ad:**
- **Judge:** only after $100–150 spend (2–3× target).
- **Scale:** at ≤ $50 booked, raise budget 10–30% a day. If cost rises after a raise, wait 48h before acting.
- **Kill:** $150 spent with no booking near target. Cut it and move the budget to winners and a fresh test.
- Never edit a live winner while scaling.
