# PD-2026-008 Carpenter — Image Quality Gate v001

Status: mandatory before any image asset is accepted.  
Scope: all Codex-generated images, local SDXL stills, SVD/AnimateDiff first frames, and any derived variants.

## Standard

The bar is not "usable documentary B-roll." Each accepted still must be strong enough to stand alone as a deliberate cinematic image: clear subject, disciplined composition, rich light, controlled color, tactile detail, no accidental clutter, no model artifacts, and no factual or rights ambiguity.

In practical terms: if a frame looks like generic AI stock, a demo prompt result, a distorted tech wallpaper, or a merely decorative background, reject it.

## Non-Negotiable Rejects

- Identifiable likeness of Timothy Carpenter or any real person connected to the case.
- Any claim that a generated scene is authentic footage or evidence.
- Store logos, carrier logos, readable brand marks, badges, seals, or hallucinated legal text.
- Wrong vote count, wrong point count, or any generated text inside image pixels.
- Sensationalized robbery imagery, weapons aimed at camera, blood, gore, or editorialized police framing.
- AI telltales: malformed hands, warped phone geometry, melted towers, inconsistent shadows, plastic skin, fake HDR glow, over-sharpened texture, smeared faces, incoherent map details.
- Composition with no narrative job.

## Acceptance Score

Accept only assets scoring at least 92/100, with no safety failure.

| category | points | requirement |
|---|---:|---|
| Narrative responsibility | 15 | The image immediately supports the exact scene beat and does not merely look atmospheric. |
| Composition | 15 | Strong focal hierarchy, clean silhouette, intentional negative space for Remotion text, no edge distractions. |
| Lighting | 15 | Deep navy/black base, motivated electric-blue rim, restrained gold accent, believable shadow direction. |
| Material detail | 10 | Phone glass, paper, desk, city grid, or architecture has tactile realism without noise or overprocessing. |
| Brand fit | 10 | Matches `remotion/src/brand.ts`: black/navy/electric-blue/gold/silver. |
| Factual safety | 10 | No invented specifics, logos, readable text, real-person likeness, or misleading authenticity. |
| Editability | 10 | Works at 16:9, has crop room, survives slow push/parallax, and leaves safe text zones. |
| Technical quality | 10 | Sharp where intended, no compression artifacts, no anatomy/device/model defects. |
| Neighbor contrast | 5 | Does not duplicate the visual density, angle, or subject of adjacent shots. |

## Candidate Policy

- Hero images: generate 8 candidates minimum, select 2, then refine once.
- Tier A images: generate 6 candidates minimum.
- Tier B images: generate 4 candidates minimum.
- Tier C images: generate 2 candidates minimum.
- If the best candidate scores below 92, revise the prompt or visual mode. Do not "settle."
- If a concept fails twice, switch to Remotion graphics, object macro, or abstraction rather than forcing a weak image.

## Prompt Direction

Use "museum-grade" as an internal quality bar, but prompts should remain concrete:

- Start with subject/action/setting, not style words.
- Specify camera, lens, composition, light direction, materials, and negative space.
- Use brand color as lighting and production design, not as a flat color wash.
- Avoid "cyberpunk", "futuristic UI", "stock photo", "dramatic police scene", and "courtroom drama" cliches.
- Keep text out of the image. All captions, dates, counts, citations, and labels are Remotion overlays.

## Review Procedure

1. Register each candidate with scene/shot ID, generator, prompt, seed, model, timestamp, and provisional rights status.
2. Run automated checks: resolution, aspect ratio, NSFW, face detection, OCR/text, logo/watermark, duplicate, color histogram, blur, and crop safety.
3. Human review every reenactment-like or real-person-adjacent still.
4. Mark each candidate as `accept`, `revise`, or `reject`.
5. Rights-register only accepted assets for edit assembly.

## High-Risk Shots

- SH004 / SH107: anonymous hand-phone hero images. Must feel intimate and premium without becoming product advertising.
- SH012: generic electronics storefront. Must avoid real logos and avoid sensational robbery framing.
- SH014 / SH018 / SH033 / SH037 / SH042: document/object macros. Must contain no readable text and no fake official seals.
- SH050 / SH095: public-life phone visuals. Must avoid identifiable faces, private information, ads, and real station branding.
- SH062: court exterior. Must be generic/inspired; do not imply authentic Supreme Court footage.

