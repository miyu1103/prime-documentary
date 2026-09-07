# PD-2026-007 Riley - Visual QC Plan v001

## Standard

The owner's image bar is intentionally high: each selected still should be strong enough to stand on
its own as a serious documentary image, not just as acceptable filler. For this episode, "good
enough" is a rejection category for hero and Tier A visuals.

## Hard Rejects

- Identifiable likeness of David Riley, Brima Wurie, a real justice, or any real person.
- Any image that reads as authentic footage or authentic evidence instead of symbolic reconstruction.
- Readable generated text, logos, app brands, watermarks, UI screenshots, real addresses, or license plates.
- Sensationalized crime imagery, gang signaling, gore, weapons pointed at the viewer, or guilt editorializing.
- AI artifacts: warped hands, distorted phones, fake glass reflections, duplicate objects, plastic skin, impossible shadows.
- Palette drift away from black/navy/electric-blue/gold or a stock-photo look.

## Scoring

Score each candidate 0-100 across:

- Concept clarity: the frame communicates the scene's purpose without narration.
- Composition: subject hierarchy, negative space for Remotion overlays, crop safety at 16:9 and thumbnail crops.
- Light and color: disciplined noir/legal-tech palette, controlled highlights, no muddy or oversaturated look.
- Material realism: believable glass, paper, fabric, metal, evidence bags, road surfaces.
- Emotional precision: tension, privacy, scale, or unease without melodrama.
- Editability: stable geometry, room for parallax, no important detail under captions.
- Neighbor contrast: not visually redundant with adjacent scenes.
- Rights and safety: no likeness, logos, readable data, or authentic-evidence implication.

## Acceptance Threshold

- Hero: 95+ or regenerate.
- Tier A: 92+ or regenerate.
- Tier B: 88+ or fallback to Remotion/object abstraction.
- Tier C: 85+ only if low prominence and clean.

An image below threshold can still be useful as a mood reference, but it must not be selected for the
cut. For repeated failures, change visual mode before lowering the standard.

## Review Workflow

1. Generate candidates into `H:/pd-media/episodes/PD-2026-007-riley/images/candidates/`.
2. Create contact sheets per scene with prompt id, seed/model, and candidate id.
3. Reject hard failures first.
4. Score remaining candidates against this plan.
5. Select only passing images into `H:/pd-media/episodes/PD-2026-007-riley/images/selected/`.
6. Register selected assets in `09_package/rights_manifest.v001.json` before edit use.
7. If a selected image later fails in motion/layout, demote it and regenerate or switch to Remotion.

## Episode-Specific Notes

- The strongest images should be object-led: phone, wallet, evidence table, phone booth, location
  trail. This lowers likeness risk while preserving cinematic weight.
- Legal and factual precision belongs in Remotion text, not generated pixels.
- The most important visual payoff is not a person; it is the phone becoming a life, then becoming a trail.
