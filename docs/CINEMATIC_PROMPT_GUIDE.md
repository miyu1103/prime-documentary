# Cinematic prompt & motion guide (EP2+ — make AI assets look premium, not cheap)

Owner note 2026-06-15: Runway and Midjourney-animate clips in EP1 looked cheap. Root causes and the
fix, with reusable prompt recipes. Pairs with `decisions/0004` §C (source priority) and `0007`
(4090/finishing). Applies from EP2.

## Why AI clips look "cheap" (and the principle)
1. **Generic prompts** → generic output. Cinematic detail must be specified.
2. **Over-reliance on big AI motion** → warping/morphing faces/edges = the #1 "AI slop" tell.
3. **No color grade / grain** → flat, mismatched, video-game look.

**Principle: premium = a highly detailed cinematic SOURCE + SUBTLE, controlled motion + a consistent
grade.** Big flashy motion reads cheap; restraint reads expensive. Quality comes more from source
detail + subtlety + grade than from the tool's raw power. Diversify motion — don't lean on one tool.

## A0. Midjourney MAX-quality protocol (obsess over image beauty)
The prompt is only half of it. To get gorgeous, premium stills:
- **Latest model** (V8.x) at **highest quality/HD**; web UI: low–moderate **Stylization** for cinematic
  control (too high = generic-pretty), or **`--style raw`** for photographic control. **`--ar 16:9`**.
- **Name a cinematic look** (huge beauty lift): e.g. *"chiaroscuro film-noir lighting,"* *"volumetric
  light,"* *"shot on Kodak Vision3, anamorphic,"* *"A24 cinematic,"* *"Roger Deakins-style motivated
  lighting."* Add **lens + film stock + grade** every time.
- **Curate hard:** generate several, keep the **single best**; reroll weak ones. One stunning > four ok.
- **Lock a brand `--sref`:** make one style-anchor image, reuse its `--sref` across the whole episode
  so every still shares a premium, cohesive look (replaces the still-unset `<SREF>`).
- **Upscale + finish:** MJ upscale (Subtle) → optional 4K via local Topaz/4090 → **brand LUT grade +
  grain** on everything. This removes the last of the "cheap" feel.
- **Avoid the cheap tells:** oversaturation, HDR glow, plastic skin, flat front-lighting, generic
  stock look, busy clutter. Prefer deep contrast, one motivated light, negative space.

## A. Still prompt recipe (Midjourney / SDXL) — the quality base
Order: **subject + specific detail → shot/composition → lens/camera → lighting → mood/atmosphere →
film stock/grade → style → quality tags → params**.

Template:
```
[subject, concrete detail], [shot type & composition], shot on [camera/lens, e.g. ARRI Alexa, 35mm,
shallow depth of field], [lighting: motivated, directional, soft/hard], [mood/atmosphere: haze,
dust, volumetric light], [film look: Kodak Portra / teal-and-amber / cinematic color grade],
[style: photoreal documentary OR stylized symbolic], highly detailed, cinematic, 8k, --ar 16:9 --style raw
```
Avoid (negatives / SDXL): plastic skin, oversaturated, generic stock, watermark, text artifacts,
extra limbs, warped geometry, low detail, HDR glow.

Miranda example (symbolic, no real likeness):
```
An empty 1960s interrogation room at night, one hard overhead lamp over a bare steel table,
low-angle wide shot, shot on ARRI 35mm shallow depth of field, hard motivated key light with deep
falloff, drifting dust in the beam, cold blue with crushed blacks, cinematic film grade, highly
detailed, symbolic reconstruction not documentary footage, no people --ar 16:9 --style raw
```
Pino example: keep the locked Pino via the reference; same cinematic lighting/grade language.

## B. Motion recipe by tool (keep it SUBTLE)
- **Midjourney animate:** feed the high-quality still; prefer **low motion** for realism; prompt one
  gentle move + atmosphere: `slow cinematic push-in, drifting dust, subtle light flicker, stable,
  photoreal, no warping`. High motion on complex scenes = morphing = cheap.
- **Runway (Gen-3/4):** use the still as **first frame**; specify **one clear camera move + subtle
  subject motion**, short and controlled: `slow dolly-in, gentle parallax, cinematic, photoreal,
  stable, no morphing, no warping`. Use camera-control presets where available; short durations.
- **SDXL + SVD / AnimateDiff (local 4090, free):** subtle **loops** (drifting smoke, shimmering
  light, slight sway); low-motion bucket; then **RIFE frame-interpolate** to smooth.
- **Depth-parallax in Remotion (free):** depth map → 2.5D push/parallax on any detailed still — the
  **most reliable premium motion, zero warping**. Default for static subjects (rooms, documents,
  portraits).

## C. Which motion tool per shot (diversify — don't rely on Runway alone)
- **Organic motion** (smoke / water / fire / crowd / weather) → MJ-animate / Runway / SVD (they do
  organic well, subtle settings).
- **Static subject that needs life** (room, document, portrait, object) → **depth-parallax +
  animated overlays** (no warp risk). Often better than a generated clip.
- **Designed / graphic** (data, numbers, text, diagrams, maps) → **Remotion** animation.
- **One hero dramatic camera move** → Runway with explicit, restrained camera control.

## D. Finishing makes it premium (automated, 0007 §B)
Apply uniformly: **brand color-grade LUT + grain + vignette** across all sources; **RIFE
interpolation** for smoothness; auto-upscale/denoise low-res sources. This alone removes most of the
"cheap" feel and unifies mixed tools.

## E. Rule of thumb
If a clip looks cheap: (1) is the **source** detailed/cinematic? (2) is the **motion subtle** (not
warping)? (3) is the **grade** applied? Fix in that order. Prefer **depth-parallax + overlays** over
big generated motion whenever the subject is static.
