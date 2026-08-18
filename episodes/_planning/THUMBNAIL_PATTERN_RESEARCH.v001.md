# In-lane thumbnail-composition research (v001, direct, 2026-07-25)

Method: 12572 in-lane long/short videos (age>=30d, vpd>0) from the 62,410-row corpus, ranked by views/day (vpd, age-controlled CTR proxy). Downloaded + analyzed the top 160 (WINNERS) vs bottom 160 (FLOPS) thumbnails with OpenCV haar face detection + luma/HSV.

| metric | WINNERS (top 160) | FLOPS (bottom 160) | read |
|---|---|---|---|
| has a detectable face | 70.0% | 60.6% | faces skew to winners |
| face height (median, % of frame) | 14.9% | 26.8% | winners' faces are not bigger |
| face height p75 | 21.1% | 41.4% | top winners go large |
| face center X (%) | 51.0 | 50.6 | composition side |
| face center Y (%) | 31.5 | 41.3 | eyes-upper-third check |
| brightness (median luma 0-255) | 62.3 | 84.6 | winners darker/moodier |
| saturation (median) | 83.6 | 94.2 | color pop |

## Findings — the counterintuitive part
The winning pattern is NOT "biggest face." Measured, winners vs flops:
1. **Have a face** — 70% of winners vs 61% of flops (+9pt). Faces help.
2. **But a MODERATE, composed face, not a huge pasted one** — winners' face median 14.9% of frame (p75 21%); FLOPS are the ones with huge faces (median 26.8%, p75 41%). A giant face-filling head correlates with FLOPS (reads amateur/clickbait); a moderate face inside a composed cinematic scene correlates with WINNERS (reads premium).
3. **Face HIGH in frame** — winners' face center Y = 31.5% (eyes in the upper third); flops sit lower (41%).
4. **DARK & moody** — winners median luma 62 vs flops 85. Dark wins; bright loses.
5. **RESTRAINED color** — winners saturation 84 vs flops 94. Garish over-saturation is a flop signal.

## Spec for the all-thumbnail refresh (data-derived, honest)
- Emotive face PRESENT and clearly readable, but **composed at ~20-30% of frame height (a strong medium-close, not a face-filling 60%+ pasted head)**, in a cinematic scene.
- Eyes on the **upper third** (face center Y ~30-35%).
- **Dark, moody** grade (luma ~60), **restrained** saturation (~85, not garish).
- 2-4 word hook in negative space, never over the face.
- ★ TENSION WITH "ガッツリ顔": the data says a HUGE face is a FLOP signal in this lane. Recommended synthesis = a PROMINENT, emotive, well-lit face that dominates by LIGHT + expression, not by filling 70% of the frame — premium, not clickbait. Owner to confirm the size target.
- Caveat: haar detects frontal faces only; illustrative/¾ faces undercount, and vpd-winners skew to large channels — directional, not gospel. One analysis; worth a small A/B on our own channel once CTR is measurable (needs the Studio cookie).
