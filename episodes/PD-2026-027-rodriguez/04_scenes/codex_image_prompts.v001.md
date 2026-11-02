# PD-2026-027-rodriguez — Codex Image Prompts v001 (EARLY / pre-script parallel batch)

Rodriguez v. United States, 575 U.S. 348 (2015). Just after midnight in March 2012 in Nebraska, an officer stopped Dennys Rodriguez for briefly veering onto the shoulder, checked him out, and issued a **written warning** — the traffic stop's business was done. Then the officer held him another seven-to-eight minutes, waiting for backup, and walked a **drug-sniffing K-9** around the car; the dog alerted and drugs were found. The Supreme Court held 6–3 (Ginsburg, maj.) that a traffic stop's authority ends when the tasks tied to the traffic infraction are — or reasonably should be — completed; **prolonging the stop even a few minutes for a dog sniff, without independent reasonable suspicion, is an unlawful seizure.** The mission of the stop defines its limit; the clock is the whole case.

**Status: EARLY batch so image generation can run in parallel with scripting.** Scene IDs may shift when the annotated script locks; these HERO images are stable to the story. This is the third of the "surveillance vs. privacy" mini-series (Kyllo = the home / walls; Katz = the person / no walls; Rodriguez = **time** — how long the state may hold you).

Primary image pipeline: **Codex image generation first.** Local SDXL/SVD only for bulk variants under the same rights/QC rules. No paid API or external upload is authorized by this file.

## Global Rules

- Aspect: 16:9, 1920×1080 target. Stills must survive slow push, **2.5D parallax / floating-card treatment**, and crop (clean negative space top and lower-third for Remotion text).
- Style: museum-grade cinematic symbolic noir documentary. Black / deep navy base (`#0A0A0C` / `#0B1A2B`), **electric-blue signal `#1F6BFF`**, silver highlights `#C8CDD6`, restrained **muted gold accent `#E5B53A`** (sparingly), controlled contrast, subtle film grain. Mood: a lonely two-lane highway at midnight, cold headlight beams, breath-cold air, the quiet dread of waiting on the shoulder.
- **Police lights**: you MAY show restrained **red-and-blue light spill** on wet asphalt and car bodies as motivated light — but **NEVER a full-screen color wash or flashing yellow bloom.** Keep it low, reflected, cinematic. No garish strobe.
- People: **faceless** — silhouettes, backs, torsos, hands on a wheel, POV only. **No identifiable likeness** of Dennys Rodriguez, Officer Struble, or Justices Ginsburg / Thomas / Alito.
- Text: **do not generate any text, letters, numbers, signs, plates, badges, readable documents, watermarks, or captions inside images.** Remotion adds all text. (No dates, no legal standards, no license plates, no clock numerals.)
- The dog: render the K-9 as a **working police dog silhouette or partial view**, alert and tense, never cute, never attacking — neutral and procedural.
- Disclosure: every reenactment/location/object image is **symbolic reconstruction**, rights-registered before edit use. Never look like authentic dashcam/archival footage.
- Negative: face, facial features, portrait, recognizable person, police badge/logo, readable sign/number/plate, watermark, text, gore, weapon glamor, aggressive attacking dog, distorted hands, extra fingers, over-processed HDR, cartoon, neon candy colors, full-screen light wash.

## Quality Bar (a selected still must pass ALL)

- Composition: clear subject hierarchy, intentional negative space for overlays, mobile-readable focal point (72% of views are mobile).
- Lighting: motivated source (headlights, streetlight, restrained patrol light), controlled contrast, no flat stock look, no muddy black crush.
- Material detail: believable asphalt, rain, car chrome, breath-fog, dog fur, worn upholstery; no plastic AI sheen.
- Narrative duty: the image must explain, locate, symbolize, or build tension for its exact beat.
- Safety: no identifiable person, no logos/text/plates, no authentic-footage illusion.
- Editability: works with 2.5D/parallax/floating-card, has crop room, does not fight captions/lower-thirds.
- Neighbor fit: not redundant with adjacent shots; change scale, angle, brightness, or subject.

Reject & regenerate if any appear: visible face, badge/logo/plate/text artifact, mangled hands, glamorized weapon, attacking dog, full-screen wash/strobe, period anachronism (reenactment is **~2012, present-day-adjacent**), fake dashcam authenticity, generic stock look, weak visual role.

## Hero Image Prompts

| ID | Beat | Priority | Candidate Count | Prompt |
|---|---|---:|---:|---|
| COD-S001-stop-on-dark-highway | Hook | A | 10 | A single car pulled onto the shoulder of an empty two-lane highway just after midnight, cold headlight beams cutting the dark ahead, faint restrained red-and-blue light reflected low on wet asphalt behind it, vast lonely night, no faces, no plates, museum-grade cinematic still, wide negative space |
| COD-S002-stopwatch-macro | Hook | A | 10 | Extreme macro of an old analog stopwatch hand sweeping in cold low light, electric-blue rim and one gold reflection, the seconds that decide a right, deep shadow, no readable numerals, tense symbolic still |
| COD-S003-headlights-two-lane | Act1 | A | 8 | A desolate rural two-lane road at night from a low angle, twin headlight cones and a single distant streetlight, breath-cold haze, no cars-with-faces, period-neutral, deep navy and gold, cinematic reconstruction |
| COD-S004-hands-on-wheel | Act1 | A | 8 | Anonymous hands resting on a steering wheel at night, dashboard glow below, faint red-and-blue light washing softly across the knuckles from behind, tension and stillness, no face, tactile realism, no readable dash text |
| COD-S005-warning-slip-handed | Act1 | A | 8 | A single folded paper slip passed between two anonymous hands through a car window at night, the "mission complete" of a written warning, no readable text on the paper, cold blue and warm interior glow, symbolic still |
| COD-S006-patrol-car-behind | Act1 | B | 6 | A patrol car stopped behind a vehicle on a dark shoulder, its light bar glowing restrained red-and-blue reflected on wet road (no full wash), seen from a respectful distance, no logos, no faces, cinematic night composition |
| COD-S007-the-waiting | Act2 | A | 10 | A car sitting alone on the shoulder with its hazard glow while empty dark highway stretches away, the dead time of waiting after the stop should have ended, a clock-like tension in the stillness, no faces, cold navy, generous negative space |
| COD-S008-k9-silhouette | Act2 | A | 10 | A working police dog in silhouette, alert and tense on a leash beside a dark car at night, procedural and neutral (never attacking, never cute), backlit by cold headlights, no face of a handler, no logos, museum-grade tension |
| COD-S009-dog-circling-car | Act2 | A | 8 | Low wide shot of a leashed police dog and an anonymous officer's legs circling a stopped car on a dark road, restrained blue-red light on the paint, the sniff in progress, no faces, no plates, cinematic reconstruction |
| COD-S010-line-crossed-in-time | Act2 | A | 8 | A symbolic thin electric-blue line drawn across a dark road with a car just past it, the moment a lawful stop becomes an unlawful seizure — a line made of time, not distance, minimalist premium composition, no text |
| COD-S011-courthouse-colonnade | Act3 | A | 8 | A symbolic marble courthouse colonnade at dusk, tall fluted columns receding, cold navy sky, one shaft of gold light between pillars, monumental and severe, no readable inscriptions, no identifiable real building, museum-grade architecture |
| COD-S012-six-three-division | Act3 | A | 8 | Abstract symbolic composition of a clean line splitting a dark marble surface, one side lit electric blue, the other muted gold, a six-versus-three tension rendered purely as light and division, no text, no numbers, minimalist metaphor |
| COD-S013-mission-of-the-stop | Act3 | A | 6 | A single sheet of paper (a traffic warning) resting under a hard light beside a set of car keys, the narrow "mission" of the stop, cold shadow, no readable text, precise editorial still |
| COD-S014-modern-everyday-stop | Act4 | A | 10 | Present-day: an ordinary car on a suburban night street with faint restrained patrol-light reflections, the universal everyday traffic stop, quiet unease about how long it can last, no faces, no plates, no logos, premium cinematic still |
| COD-S015-open-road-rights | Tease/End | A | 8 | An empty highway vanishing toward a cold blue horizon at first light, taillights of a single car receding, freedom and the limits of state power, no faces, no text, resonant closing still with lower-third space |

## Additional Hero Prompts — density + variety (11–12 min cut; footage carries the rest)

| ID | Beat | Priority | Candidate Count | Prompt |
|---|---|---:|---:|---|
| COD-S016-wet-asphalt-lights | Act1 | A | 8 | Macro of wet night asphalt reflecting restrained red-and-blue light into soft abstract pools, lane paint catching a cold gleam, moody procedural texture, no text, strong standalone atmosphere |
| COD-S017-clock-on-dash | Act2 | A | 8 | Close-up of a dim dashboard clock glow in a dark car (no readable numerals), electric-blue cast, the minutes ticking past the mission, tense macro, no text |
| COD-S018-leash-and-hand | Act2 | B | 6 | A taut leash in an anonymous gloved hand at night, tension in the line, cold blue rim light, the K-9 implied off-frame, no face, no logo, tactile still |
| COD-S019-side-mirror-lights | Act2 | A | 8 | View in a car's side mirror of restrained red-and-blue patrol light behind at night, the anxious glance backward, cold navy, no plates, no faces, cinematic framing with reflection depth |
| COD-S020-empty-shoulder-cones | Act2 | B | 6 | A lonely highway shoulder at night with a single reflective marker and gravel, headlight spill and dark fields beyond, the place where the waiting happened, no people, museum-grade minimalism |
| COD-S021-courtroom-interior | Act3 | A | 8 | A dignified empty courtroom interior in low key, a long dark bench and tall windows, one cold shaft of light across the floor, monumental and neutral, no people, no readable text or seals |
| COD-S022-hourglass-seizure | Act3 | A | 6 | A symbolic hourglass in cold low key, sand of electric-blue light running low, the constitutional limit measured in time, deep navy void, no text, elegant metaphor still |
| COD-S023-scales-time-vs-power | Act3 | B | 6 | A minimalist balance scale, a small stopwatch on one pan and a small badge-shaped shadow on the other (no readable logo), the balance between a citizen's time and state authority, no faces, no text |
| COD-S024-dashcam-frame-symbolic | Act4 | A | 8 | A symbolic reconstruction evoking a night dashcam view down a dark road with restrained light spill (clearly stylized, NOT authentic footage), vignette and grain, no readable overlays, no plates, no faces, cinematic |
| COD-S025-taillights-recede | Act4 | B | 6 | A single car's taillights receding into a dark highway, the stop over, freedom resumed, cold navy with two warm-red points, no text, resonant still with negative space |
| COD-S026-first-light-horizon | Ending | A | 6 | A bare highway under a cold navy-to-grey dawn, one distant streetlight fading, quiet and open, the case that limited how long the state can hold you, no faces, generous space for the end tag |

## Local SDXL Variant Settings (only if bulk variants are needed)

- Model: RealVisXL V5 or JuggernautXL — pick one and keep it for the whole episode.
- Sampler: DPM++ 2M Karras, 32–40 steps, CFG 4.5–6.5. Base 1344×768 → upscale 1920×1080.
- One locked seed family per episode with controlled per-scene offsets.
- Selection: semantic match, no face/likeness, no text/logos/plates, no anatomy issues, brand fit, editability, symbolic-not-authentic clarity, restrained patrol light (no full wash).

## Coverage / Handoff Notes

- These ~26 heroes cover the hook, four acts, and a resonant open-road ending with distinct anchors; footage from the factory shelf (highway, headlights, night road) carries roughly half the shots.
- Do NOT generate exact dates, legal standards, plates, clock numerals, or case citations in images — Remotion owns all text.
- Signature beats are the lonely highway stop + the stopwatch + the K-9 silhouette (S001, S002, S008) — generate the most candidates there (10 each).
- Continuity with EP25/EP26: same palette and grain. Restrained red-and-blue is the only new color note; keep it low and reflected — never a full-screen wash (owner style-lock).
