---
name: pd-generate-assets
description: Generates, registers, quality-checks and selectively regenerates PD visual assets from approved scene and shot specifications.
---

# PD Asset Generation

## Procedure

1. Validate active scene and shot revisions.
2. Compile provider-neutral visual specifications into provider requests.
3. Estimate GPU/provider cost and check budget.
4. Reuse approved library assets when appropriate.
5. Generate candidate assets by priority tier.
6. Register prompt, model profile, seed, dimensions, input hash and provider metadata.
7. Run technical, semantic, continuity, anachronism, text/watermark and safety QC.
8. Rank candidates relative to neighboring shots.
9. Approve or reject candidates with reasons.
10. For failures, apply the correct repair strategy rather than repeating identical requests.
11. Produce contact sheets and exception queue.
12. Mark downstream artifacts stale only when active asset revisions change.

## Never

- Treat generated output as approved without QC.
- Overwrite an approved asset.
- Regenerate every scene for one failure.
- Generate explanatory text inside the image when it can be added accurately in edit.

## Output

- registered candidates
- approved assets
- rejected assets and reasons
- regeneration jobs
- cost report
- visual QC report
