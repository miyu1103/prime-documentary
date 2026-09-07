# PD-2026-006-terry - Codex Image Prompts v001

Primary image pipeline: Codex image generation first. Local SDXL/SVD may be used for bulk variants after the same rights/QC rules. No paid API or external upload is authorized by this file.

## Global Rules

- Aspect: 16:9, 1920x1080 target, generated stills suitable for slow push, parallax, or crop.
- Style: museum-grade cinematic symbolic noir documentary: each still must hold up as a standalone composition with intentional light, depth, texture, and narrative meaning. Black/deep navy base, electric-blue signal, muted gold accent, silver highlights, restrained contrast, subtle film grain.
- People: faceless anonymous silhouettes, backs, torsos, hands, POV only. No identifiable likeness of McFadden, Terry, Chilton, Warren, Douglas, or modern people.
- Text: do not generate text, letters, signs, logos, badges, readable documents, watermarks, or captions inside images. Remotion handles all text.
- Disclosure: all reenactment/location/object AI images are symbolic reconstruction and must be rights-registered before edit use.
- Negative: face, facial features, portrait, recognizable person, celebrity, police badge logo, readable sign, watermark, text, gore, weapon glamor, aiming gun, violence, distorted hands, extra fingers, overprocessed HDR, cartoon, neon candy colors.

## Quality Bar

No image is accepted as a mere placeholder. A selected still must pass all of these:

- Composition: clear subject hierarchy, intentional negative space for overlays, no accidental cropping, mobile-readable focal point.
- Lighting: motivated source, controlled contrast, no flat stock-photo lighting, no muddy black crush.
- Material detail: believable fabric, pavement, glass, rain, haze and grain; no plastic AI sheen.
- Narrative duty: the image must explain, locate, humanize, symbolize, or create tension for its exact scene.
- Safety: no identifiable person, no real-person likeness, no logos/text, no misleading authentic-footage look.
- Editability: works with 2.5D/parallax or Ken Burns, has crop room, and does not fight captions or lower-thirds.
- Neighbor fit: not visually redundant with adjacent shots; scale, angle, brightness or subject must change.

Reject and regenerate if any of these appear: visible face, badge/logo/text artifact, mangled hands, extra limbs, glamorized weapon, city-specific landmark not in the script, period anachronism, fake documentary-photo authenticity, generic stock look, or weak visual role.

## Hero Image Prompts

| ID | Scene | Priority | Candidate Count | Prompt |
|---|---|---:|---:|---|
| COD-S001-pov-street-stop | S001 | A | 8 | Present-day sidewalk from first-person POV, a police officer torso and hands only, no face, stopping the viewer at dusk, outer clothing pat-down implied but restrained, dark navy street, electric-blue rim light, muted gold streetlight, symbolic reconstruction, museum-grade cinematic documentary still |
| COD-S003-downtown-street-wide | S003 | A | 8 | 1963 downtown Cleveland symbolic street, storefront windows, wet pavement, anonymous pedestrians as distant silhouettes, no readable signs, no logos, brass streetlight, deep navy shadows, period cars only as soft shapes, museum-grade cinematic reconstruction |
| COD-S004-store-window-anonymous-wide | S004 | A | 8 | Two faceless anonymous men in 1960s coats walking past a single store window, wide shot from across the street, no faces, no readable signage, repeated-path feeling, muted gold window glow, navy shadows, museum-grade composition |
| COD-S005-observer-behind-shoulder | S005 | A | 8 | Behind-shoulder view of an anonymous plainclothes observer watching a storefront from a distance, face hidden, 1960s urban sidewalk, cinematic low-key lighting, subtle tension, no police badge, no readable signs, painterly depth without looking like fantasy |
| COD-S007-approach-hands-only | S007 | A | 8 | Close low-angle street moment, officer hands and coat sleeves only approaching two anonymous torsos, no faces, no weapons visible, neutral documentary tension, dark navy and gold lighting, precise composition |
| COD-S008-outer-clothing-patdown | S008 | A | 8 | Restrained close-up of hands patting the outside of a heavy coat, face out of frame, no visible weapon, no badge, symbolic reconstruction, low-key street light, fine grain, tactile museum-grade detail |
| COD-S012-unknown-person-silhouette | S012 | A | 6 | Abstract street encounter silhouette, officer at safe distance from unknown anonymous figure, no faces, no weapon, empty negative space between them, electric-blue edge light, neutral tone, gallery-quality composition |
| COD-S014-empty-sidewalk-night | S014 | B | 4 | Empty city sidewalk at night, rain-dark pavement, one thin line of streetlight, no people, reflective and tense, black navy gold palette, cinematic documentary texture, strong standalone atmosphere |
| COD-S018-coat-fabric-hands | S018 | A | 8 | Macro detail of heavy coat fabric and open hands near outer clothing, no face, no weapon, no pockets searched, tactile legal-boundary motif, low-key gold light and navy shadow, museum-grade material realism |
| COD-S022-modern-street-stop-wide | S022 | A | 8 | Modern urban street stop shown wide from behind, anonymous silhouettes only, no identifiable faces, no city landmarks, no logos, respectful neutral framing, electric-blue street reflections, symbolic reconstruction, premium documentary still |
| COD-S023-anonymous-sidewalk-crowd | S023 | A | 6 | Modern sidewalk crowd as faceless silhouettes moving through a narrow pool of light, one person paused at the edge, no police insignia, no faces, restrained documentary tension, excellent depth and negative space |
| COD-S024-modern-facts-montage | S024 | A | 8 | Contemporary street details montage still: shoes at curb, hand near jacket seam, storefront reflection, patrol light as abstract reflection only, no faces, no readable signs, neutral symbolic reconstruction, premium editorial composition |
| COD-S026-thin-line-sidewalk | S026 | A | 6 | Empty sidewalk seen from above, a thin electric-blue and gold line drawn along the concrete seam, night texture, quiet city atmosphere, symbolic legal line motif, gallery-quality minimalism |
| COD-S028-pocket-house-sidewalk-objects | S028 | B | 4 | Close-up still life of a coat pocket, a house key, a folded paper, and sidewalk texture, no logos, no text, physical-things motif, navy/gold light, precise still-life composition |
| COD-S029-phone-in-pocket-glow | S029 | A | 8 | Smartphone silhouette inside a jacket pocket glowing electric blue, hand nearby but not touching, no app icons, no readable screen, dark navy background, gold rim light, next-episode tease, premium cinematic object still |

## Local SDXL Variant Settings

- Model: RealVisXL V5 or JuggernautXL; choose one and keep it for the episode.
- Sampler: DPM++ 2M Karras, 32-40 steps, CFG 4.5-6.5.
- Base: 1344x768, upscale to 1920x1080.
- Seed policy: one locked seed family for the episode, with controlled offsets per scene.
- Selection: semantic match, no face/likeness, no text/logos, no anatomy issues, brand fit, editability, symbolic-not-authentic clarity.

## Coverage

The remaining scenes are Remotion graphics, diagrams, typography, or reuse/crop variants of the hero stills. Do not generate exact dates, legal standards, counters, or case citations in images.
