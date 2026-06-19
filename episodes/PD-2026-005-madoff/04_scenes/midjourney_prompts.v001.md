# PD-2026-005-madoff — Midjourney Hero Prompts v001

Owner generates these; Claude/Codex then views the 4-up and recommends the single best pick per the selection criteria. Charts, diagrams, number cards, timeline, quote/citation cards and captions are NOT here — those are Remotion (see remotion_plan).

## Global rules (apply to EVERY prompt)
- Style: cinematic symbolic noir, dark + gold/amber palette, low-key single-source light, deep shadows, volumetric haze, fine film grain.
- **NO pink anywhere.** No neon/candy colors. The only cold color is reserved for "THE LINE" (Remotion), so keep stills warm-dark.
- **Faceless / no real-person likeness**: anonymous silhouettes, backs of heads, hands, figures in shadow only. No recognizable faces. No text in image.
- Aspect/flags suffix for all: `--ar 16:9 --style raw --sref [LOCK_AFTER_H01] --no text, watermark, logos, faces, likeness, pink`
- Pipeline: generate H01–H03 first, pick the strongest, **lock its --sref seed**, then run the rest with that sref for unity. SDXL mass-produces coverage variants from the chosen heroes.

---

## Section 00_hook — THE LINE / two ways of seeing
- **H01** (sref candidate): `a lone silhouetted figure standing before a vast dark wall, studying a single glowing rising line of light, empty cavernous room, gold rim light, volumetric haze, cinematic, ominous calm --ar 16:9 --style raw`
- **H02** (sref candidate): `extreme close on a pair of hands holding a single printed financial statement, warm gold desk lamp, deep shadow, dust motes, film noir --ar 16:9 --style raw`
- **H03** (sref candidate): `a crowd of faceless silhouettes turned toward a distant warm glow, one silhouette turned the other way, backlit, gold and black, isolation --ar 16:9 --style raw`

## Section 01_opening — trust pouring in
- **H04**: `symbolic streams of golden coins flowing from small institutional buildings (a bank, a columned university, a charity) toward a single calm silhouette, dark stage, spotlight, allegorical --ar 16:9`
- **H05**: `a towering golden name-plate on a dark marble wall, reverent low angle, brass and shadow, prestige and authority, no text legible --ar 16:9`

## Section actI_trust — the respectable name & the club
- **H06**: `vintage stock-trading floor at rest, empty desks and dead terminals bathed in amber dusk, long shadows, heritage and decay --ar 16:9`
- **H07**: `an exclusive dark wooden door with a single brass handle, a velvet rope, warm light leaking from the gap, invitation-only mood --ar 16:9`
- **H08**: `a smooth golden ascending ribbon of light rising effortlessly through a dark void, serene, hypnotic, 'too good' --ar 16:9`
- **H09**: `silhouetted professional figures in suits lowering their guard, shoulders relaxing, gold light washing over them, subtle naivety --ar 16:9`
- **H10**: `a single question mark formed by light suspended in a dark room, contemplative, gold on black --ar 16:9`

## Section actII_system — the hidden machine
- **H11**: `cash disappearing into a plain bank vault drawer instead of a trading desk, misdirection, amber spotlight, noir --ar 16:9`
- **H12**: `an empty trading desk with monitors switched off, a thin layer of dust, the ghost of activity, melancholy gold light --ar 16:9`
- **H13**: `a closed circle of faceless hands passing golden coins from one to the next, conveyor of deception, dark loop, allegory of a Ponzi scheme --ar 16:9`
- **H14**: `towering stacks of printed account statements drifting like falling leaves in a dark hall, fabricated paper, gold edges --ar 16:9`
- **H15**: `a grand bank vault door swung open to reveal absolute emptiness, single shaft of cold-warm light, shock of nothing --ar 16:9`

## Section actIII_math — the analyst vs the watchdog
- **H16**: `a lone silhouette at a small desk with a calculator and a pinned chart annotated by hand, midnight, single lamp, obsessive focus --ar 16:9`
- **H17**: `a single warning envelope traveling down a long dark institutional corridor toward an enormous closed bureaucratic facade, futility --ar 16:9`
- **H18**: `a pile of unopened warning letters at the base of a colossal government-style stone building, ignored, cold dawn, gold accents --ar 16:9`
- **H19**: `a vast empty watchtower / guard post with the light off, the watchdog asleep metaphor, brass and shadow, dereliction --ar 16:9`

## Section actIV_collapse — the run, the reckoning, the recovery
- **H20**: `a stampede of faceless silhouettes rushing toward a single teller window during a panic, 2008 financial crisis mood, dark, desperate, amber --ar 16:9`
- **H21**: `a vault drained dry, last coins rolling away into shadow, the moment the money runs out --ar 16:9`
- **H22**: `a stark federal courthouse exterior at dusk, columns and long steps, a lone silhouette ascending, gravity and consequence, NY federal courthouse framing --ar 16:9`
- **H23**: `a heavy prison door closing on darkness, a thin bar of warm light narrowing to nothing, finality --ar 16:9`
- **H24**: `golden coins flowing partly BACK out of shadow into open empty hands, partial restitution, bittersweet warm light, recovery --ar 16:9`

## Section ending — the takeaway
- **H25**: `two lines of light side by side in a dark void — one perfectly smooth and rising, one jagged and real — quiet revelation, gold and a single cold accent --ar 16:9`
- **H26**: `a single silhouette pausing to look back at a glowing 'too perfect' line, a beat of doubt, contemplative, gold on black --ar 16:9`

---

## SDXL coverage notes (mass-produced from locked sref)
- For each hero, generate 2–4 alt angles/compositions for B-roll/parallax (Ken Burns).
- Maintain the locked sref + dark/gold palette; **never introduce pink**; keep all figures faceless.
- Selection criteria (Claude/Codex): composition, sref consistency, no anatomical/structural breakage, scene-intent match, must read as SYMBOLIC reconstruction (not authentic footage, invariant 11).
