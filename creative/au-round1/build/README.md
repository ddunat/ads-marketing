# AU round 1 build notes

## A2 "Auction Saturday" control
- HeyGen video `940583717513446681afb4ba4fb765b2`, request in `a2-heygen-request.json`.
- Post-production (ffmpeg):
  - **hflip:** the HeyGen look is mirrored, so the shirt logo read backwards. Flip every render from this look.
  - Burned-in captions and overlays from `a2.ass`.
  - Brickwork cutaway at 5.78–10.18s: Drive `10fwwDN9d-itvUX5LGTSke380FHWn0Ktn`, clip 0–4.4s.
  - 2.5s end card: a screenshot of the landing-page form.
- **Compliance:** cut the brickwork clip before 4.5s. After that a wheelie bin with a house number ("32") is visible.
- Renders are not committed (see `.gitignore`). Final file: `renders/A2-control-v2.mp4`, 23.3s, 1080x1920.
- **Landing page mismatch:** the page still says "400+ 5-star reviews"; the ad says 529 at 4.9★. The landing gate fails until the GHL page fixes are done.

## A2 v5 (2026-10-12), Jeremy's finished-edit review
- **v4 scored 7.5.** The deduction was landing-page congruency, a launch blocker. Jeremy expects 8.5 after the fixes below.

**Done in v5:**
- Opens on real house B-roll (Drive `1J6QNe2CwBPLHshbBKpxklJnzyTcUPede`, 3.0–4.7s) with a push-in. David's VO starts at frame 0; cut to his face at 1.6s.
- Report-ready notification (`template/report-notification.html`, recorded with Playwright) plays under the guarantee punch at 2.6–5.5s, so the guarantee is shown, not just said. The 4:12 time is illustrative; swap in a real screenshot if David supplies one.
- The CTA mirrors the hook: re-voiced to "Inspect first. Tap below." (HeyGen `50feb9698b1f498cbdb356e1cd90d7ea`), with an "INSPECT FIRST." punch.
- The dead beat is filled: a "BPC REGISTERED INSPECTOR · DBU-66182" chip under the Google proof card.

**Left for challengers:** the open loop, the 4:5 feed cut, and statics. Exception: a Google proof-card static should be made now (80% video / 20% image).

**Still blocking launch:** the GHL page fix. It must say 529 reviews at 4.9★, with a headline matching the guarantee line word for word.

## A2 v6 (2026-10-14): compliance fix
- The proof-card chip changed from "BPC REGISTERED INSPECTOR · DBU-66182" to **"BPC REGISTERED INSPECTORS"**. Inspections are done by BPC registered subcontractors; DBU-66182 is David's own registration and is only shown next to his name (CLAUDE.md).
- Everything else is identical to v5. Render: `renders/A2-control-v6.mp4` (gitignored). This is the version to upload, not v5.
