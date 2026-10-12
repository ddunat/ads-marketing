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
