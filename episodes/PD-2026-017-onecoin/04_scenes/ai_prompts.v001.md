# EP17 「ONECOIN / NOTHING」 — SDXL Hero Prompt Pack (MAX quality)

> Generation: local A1111 :7860 / **juggernautXL** (driven by Claude per reference_sdxl_launch).
> Output → `H:\pd-media\episodes\PD-2026-017-onecoin\05_stock\hero\` → QC → usable only → register in `05_stock/usable_assets.v001.json` + global `assets/asset_manifest.v001.json` (license=generated, sourceTool=sdxl, sha256, disclosure=true).
> Binds to `docs/PD_ONE_PASS_PRODUCTION_SPEC.v1.md` row 5: every used still **upscaled to long edge ≥ 3840 px**, denoised, brand-graded. No real-person likeness (invariant 11). No in-image text (captions/titles are Remotion).

## GENERATION RULES (all cuts)

**BASE_SUFFIX** (append to every prompt):
`, cinematic documentary still, dramatic chiaroscuro lighting, photorealistic, ultra detailed, volumetric light, atmospheric haze, subtle film grain, shallow depth of field, anamorphic, masterpiece, ultra high resolution, 16:9`

**Per-movement color** (append the matching one):
- PROMISE (gold): `, deep black background with warm gold and amber rim light, opulent, seductive`
- CRACK (white): `, cold fluorescent white and pale blue light, clinical, sterile, uneasy`
- VOID / Coda (black): `, near-black palette, a single cold light source, void, emptiness`

**NEG** (fixed, all cuts):
`text, letters, words, watermark, logo, signature, caption, brand markings, identifiable face, recognizable real person, celebrity likeness, portrait of a specific person, deformed, mutated, extra fingers, extra limbs, bad anatomy, bad hands, low quality, lowres, blurry, jpeg artifacts, cartoon, anime, illustration, 3d render look, oversaturated, cluttered, ugly`

**MAX-quality params**: size `1344x768` (SDXL 16:9) · steps `40` · cfg `5.5` · sampler `DPM++ 2M Karras` · **Hires.fix ON**: upscaler `R-ESRGAN 4x+`, hires steps `15`, denoise `0.35`, upscale-by `2.0` (→ 2688x1536) · then **post-upscale to long edge ≥ 3840** (R-ESRGAN / Topaz). **6 variations per prompt** → QC → keep best 1–2. Faces (if any) only as silhouettes / turned away / out of focus — never identifiable.

---

## MOVEMENT 1 — THE PROMISE (gold)

**T-IMG-001 / arena, full & golden** — Motion: ken_burns_in · shots: SPN-0001
`a vast concert arena from above, bathed in warm golden light, thousands of out-of-focus people standing and cheering toward a distant bright stage, haze, lens flare`

**T-IMG-003 / the coin with a hole** — Motion: slow_rotate · cold open + recurs
`a single ornate gold coin with a perfectly round hole bored through its center, suspended in black, one shaft of light passing through the empty hole, macro, reflective`

**T-IMG-004 / gold cascade into a briefcase** — Motion: parallax_down
`a cascade of crisp hundred-dollar bills falling in slow motion into an open briefcase, warm seductive golden light, wealth, abundance`

**T-IMG-005 / the woman at the podium (no likeness)** — Motion: slow_push · recurs
`the backlit silhouette of a woman in a long gown standing alone at a podium on a huge stage, gold rim light, face unreadable in shadow, commanding, no visible features`

**T-IMG-006 / the paperwork** — Motion: ken_burns
`close on official-looking documents and a magnifying glass on a dark desk, a fountain pen signing a contract, warm light cooling at the edges, shallow focus`

**T-IMG-007 / the believers** — Motion: ken_burns_in · recurs (ambient gold)
`a crowd of ordinary people lit by warm gold light, faces lifted and hopeful, phones raised filming a bright unseen stage, reverent, not foolish`

**T-IMG-AUX-1 / the packages (educational tiers)** — Motion: ken_burns · optional
`a row of sealed premium boxes of increasing size on a dark shelf, gold foil edges, like luxury product tiers, one spotlit, aspirational`

---

## MOVEMENT 2 — THE CRACK (white)

**T-IMG-008 / the analyst who looks** — Motion: slow_push · recurs (ambient white)
`a lone analyst seen from behind, lit only by a cold computer monitor in a dark room, rain streaking a window, tense, isolated, no visible face`

**T-IMG-009 / the fabricated ledger** — Motion: macro_drift
`a close-up of hands typing numbers into a glowing spreadsheet in a dark room, the figures clearly invented not calculated, cold blue screen light on the keys`

**T-IMG-010 / the regulators warn** — Motion: ken_burns
`an official government warning letter with an embossed seal and letterhead on a desk, a rubber stamp coming down, cold authoritative light, bureaucratic`

**T-IMG-011 / the cost of looking** — Motion: slow_push
`a single empty wooden chair in a bare cold room, one shaft of pale window light, absence, isolation, melancholic`

**T-IMG-016 / the warnings ignored** — Motion: slow_push · spare
`the lone silhouette of a figure at a podium under a single light, while around it stacks of unopened warning letters pile up unread in the cold dark, certain, oblivious`

---

## MOVEMENT 3 — THE VOID (black)

**T-IMG-012 / the vanishing** — Motion: slow_push
`an empty private-jet airstair under a single cold white airport light at night, no figure, no luggage, the stair leading up into darkness, desolate`

**T-IMG-002 / the empty arena** — Motion: slow_push · callback to T-IMG-001
`the same vast arena now dark and abandoned, every seat empty, one cold spotlight on a bare stage where someone once stood, dust in the beam, silence`

**T-IMG-013 / still wanted (blank face)** — Motion: slow_push_in
`a single FBI-style wanted poster pinned in darkness under one harsh light, the photograph area left as a featureless dark silhouette with no face, official, cold`

**T-IMG-014 / the void** — Motion: slow_unfurl · the silence beat / black water
`black ink slowly unfurling and dispersing into deep black water, a faint blue glow swallowed, then stillness, abstract, suffocating, void`

---

## CODA (white light)

**T-IMG-015 / the empty corridor** — Motion: slow_push · recurs (ambient coda)
`a long empty airport corridor flooded with cold white light, polished floor, no people, vanishing-point perspective, lonely, antiseptic`

**T-IMG-AUX-2 / the empty next page** — Motion: page_turn · pairs with MG-LEDGER
`an open ledger book of blank faintly glowing pages on black, a hand turning a page to reveal another blank page, nothing written anywhere, cold light`

---

## MOTION GRAPHICS (Remotion code, NOT SDXL — for Codex)
- **MG-LEDGER** — the empty ledger: rows that should fill but never do; a chain of links that dissolves into nothing. The film's central recurring motif.
- **MG-TREE** — MLM growth: a branching tree of glowing nodes multiplying exponentially into a pyramid, then going dark all at once.
- **MG-BARS** — "raised" (a gold bar filling to >$4B) beside "real value" (a bar that never leaves zero).
- **MG-BLACK** — the held black silence beat at the void reveal (all layers cut).

---

*Build target: ~16 hero stills × 6 variations → QC → ~1–2 keepers each (~20–28 usable) + 4 motion graphics. Recurrence of motifs (ledger, coin-with-a-hole, arena, podium silhouette) is intentional and on-brand for a 30-min auteur film. All symbolic, disclosed, no likeness.*
