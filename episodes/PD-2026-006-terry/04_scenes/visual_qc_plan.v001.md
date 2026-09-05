# Visual QC Plan - PD-2026-006-terry v001

This episode uses symbolic reconstruction. The quality target is deliberately high: every selected still should be strong enough to pause on, crop into a thumbnail detail, or reuse as a premium brand asset without looking like filler.

## Acceptance Standard

An image is accepted only if it passes all gates:

1. Scene fit: supports the exact scene purpose in `scene_plan.v001.json`.
2. Visual role: identify, locate, explain, humanize, tension, symbolize, or reset attention.
3. Composition: clear focal hierarchy, strong silhouette or object shape, intentional negative space for captions.
4. Light and texture: motivated light, deep but readable shadows, believable fabric/glass/pavement/metal.
5. Brand fit: black/navy/electric-blue/gold/silver; restrained, advertiser-safe, no candy color.
6. Rights/safety: AI-disclosed, no real-person likeness, no faces, no logos, no generated text, no authentic-footage implication.
7. Technical: clean hands/body geometry, no extra limbs, no watermark, no compression artifacts, 16:9 crop-safe.
8. Editability: supports parallax/Ken Burns; important subject is not blocked by lower-third or captions.
9. Neighboring-shot diversity: differs from adjacent selected visuals in scale, angle, brightness, subject, or visual mode.

## Candidate Counts

- Hero / Tier A: 8 candidates minimum before selection.
- Tier A fallback rerun: 4 more candidates after prompt repair.
- Tier B: 4 candidates minimum.
- Remotion graphics: no AI image; verify exact text, citation, and animation timing in render.

## Hard Rejection

Reject immediately if any of these appear:

- identifiable face or portrait-like likeness,
- police badge/logo, readable signage, generated legal text, watermark, signature,
- weapon glamorization, aiming, violence, gore, or fearbait,
- modern objects in 1963 scenes unless deliberately abstracted and approved,
- real city landmark implying a location not stated in the script,
- photojournalistic framing that could be mistaken for authentic footage,
- AI anatomy defects, plastic skin, smeared hands, duplicated people,
- generic stock-photo look or visual that does not perform a narrative job.

## Selection Workflow

1. Generate the required candidate count for one prompt family.
2. Reject hard failures first.
3. Score survivors 1-5 on scene fit, composition, light, material detail, brand fit, safety, editability.
4. Keep the best 1-2 per hero prompt; mark alternates for crop/coverage only.
5. Compare against neighboring shots before final selection.
6. Register selected files in the rights manifest with origin, creator, license/rights basis, hash, prompt id, generated_at, verified_at, and AI disclosure.
7. If no candidate reaches the acceptance standard, repair the prompt or switch the visual mode. Do not lower the bar.

## Human Review Required

Human review is required before locking selected images for:

- S001 POV street stop,
- S003/S004/S005 1963 Cleveland reconstruction,
- S007/S008/S018 frisk/pat-down sequence,
- S022/S023/S024 modern street-stop montage.

These are the highest rights/safety risk because they can imply real people or real evidence if handled poorly.

## First-Cut Implication

No generated image is allowed into the first-cut render unless it is selected, rights-registered, and QC-marked pass or warn-with-owner-note. Temporary placeholders may be used only in a clearly marked internal animatic, not in an owner-facing first cut.
