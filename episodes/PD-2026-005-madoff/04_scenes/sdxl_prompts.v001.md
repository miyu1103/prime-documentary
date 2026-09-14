# PD-2026-005-madoff — SDXL Image Prompts v001

Primary image pipeline = **SDXL, local (Windows RTX 4090, ComfyUI/API)**. Fully automatable by Codex — no manual Midjourney step. Supersedes midjourney_prompts.v001.md for this episode.

## Global generation settings (apply to all)
- Model: RealVisXL V5 or JuggernautXL (pick one, keep consistent for the whole episode).
- Sampler: DPM++ 2M Karras · Steps: 32–40 · CFG: 4.5–6.5
- Base resolution: 1344×768 (16:9) → upscale to 1920×1080 with R-ESRGAN/4x then downscale.
- **Consistency**: lock ONE seed family + the same model/VAE (and an optional style LoRA) across all shots for a unified look; vary composition via prompt, not model.
- Generate 3–4 candidates per shot; Codex/Claude selects best (composition, consistency, no anatomical/structural breakage, scene-intent, must read as SYMBOLIC — not authentic footage, invariant 11).

## Shared NEGATIVE prompt (every image)
`pink, magenta, neon, candy colors, text, words, letters, watermark, signature, logo, face, facial features, recognizable person, portrait likeness, deformed hands, extra fingers, mutated, lowres, jpeg artifacts, oversaturated, cartoon`

## Shared STYLE suffix (append to every positive)
`cinematic symbolic noir, dark and gold/amber palette, low-key single-source lighting, deep shadows, volumetric haze, fine film grain, faceless anonymous silhouettes, allegorical, high detail, 16:9`

## Positive prompts (per hero shot)
| ID | Section | Positive (prepend to STYLE suffix) |
|---|---|---|
| H01 | hook | a lone silhouetted figure before a vast dark wall studying a single glowing rising line of light, empty cavernous room, gold rim light |
| H02 | hook | extreme close-up of hands holding one printed financial statement, warm gold desk lamp, dust motes |
| H03 | hook | a crowd of faceless silhouettes facing a distant warm glow, one silhouette turned away, backlit |
| H04 | opening | symbolic streams of golden coins flowing from a small bank, a columned university and a charity toward a single calm silhouette on a dark stage |
| H05 | opening | a towering golden nameplate on dark marble, reverent low angle, brass and shadow, prestige |
| H06 | actI | a vintage stock-trading floor at rest, empty desks and dead terminals in amber dusk, long shadows |
| H07 | actI | an exclusive dark wooden door with a single brass handle and a velvet rope, warm light leaking from the gap |
| H08 | actI | a smooth golden ascending ribbon of light rising effortlessly through a dark void, hypnotic |
| H09 | actI | silhouetted figures in suits relaxing their posture as gold light washes over them, lowered guard |
| H10 | actI | a single glowing question mark of light suspended in a dark room |
| H11 | actII | cash disappearing into a plain bank vault drawer instead of a trading desk, amber spotlight |
| H12 | actII | an empty trading desk, monitors off, a thin layer of dust, melancholy gold light |
| H13 | actII | a closed circle of faceless hands passing golden coins one to the next, a deceptive loop |
| H14 | actII | towering stacks of printed account statements drifting like falling leaves in a dark hall, gold edges |
| H15 | actII | a grand bank vault door swung open revealing absolute emptiness, a single shaft of light |
| H16 | actIII | a lone silhouette at a small desk with a calculator and a hand-annotated chart, single lamp, midnight |
| H17 | actIII | a single warning envelope in a long dark institutional corridor before an enormous closed facade |
| H18 | actIII | a pile of unopened warning letters at the base of a colossal government-style stone building, cold dawn |
| H19 | actIII | a vast empty watchtower with its light off, dereliction, brass and shadow |
| H20 | actIV | a stampede of faceless silhouettes rushing toward a single teller window, 2008 panic, desperate amber |
| H21 | actIV | a drained vault, last coins rolling away into shadow |
| H22 | actIV | a stark federal courthouse exterior at dusk, columns and long steps, a lone silhouette ascending |
| H23 | actIV | a heavy prison door closing on darkness, a thin bar of warm light narrowing to nothing |
| H24 | actIV | golden coins flowing partly back out of shadow into open empty hands, bittersweet, partial restitution |
| H25 | ending | two lines of light side by side in a dark void, one perfectly smooth and rising, one jagged and real |
| H26 | ending | a single silhouette pausing to look back at a glowing too-perfect line, a beat of doubt |

## Coverage
- For each hero, generate 2–4 alt angles/compositions for B-roll/parallax (Ken Burns in Remotion).
- Keep the locked seed family + dark/gold palette; **never introduce pink**; all figures faceless.
- Charts/diagrams/number cards/timeline/quote+citation cards/captions remain Remotion (see remotion_plan), NOT SDXL.
