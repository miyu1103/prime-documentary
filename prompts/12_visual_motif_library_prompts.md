# 12 — Reusable Visual Motif Prompts (Midjourney)

Generic, brand-consistent motifs reused across all episodes (decisions/0002 §B/§G). Generate
**once**, register in `library/visual/visual_registry.v001.json`, auto-select via `select_motif`.

Brand look: **stylized / symbolic, NEVER photoreal-as-evidence** (invariant 11). Palette
**black / deep navy + electric blue + silver + gold accent**. All motifs share one
`--sref <BRAND_SREF_ID>` so the channel looks unified; `--ar 16:9` unless noted. Claude views
the 4-up and recommends the single best pick (composition / --sref match / no breakage / intent
/ symbolic-not-real).

> Replace `<SREF>` with the channel's locked Midjourney style-reference seed before generating.

## Core legal motifs (16:9, symbolic, dark cinematic)
- `gavel` — "a single judge's gavel resting on a sound block, dramatic side light, deep navy and black, gold rim light, minimal symbolic, volumetric haze, --ar 16:9 --sref <SREF>"
- `courtroom_empty` — "empty American courtroom at dusk, symmetrical, long shadows, electric-blue window light, no people, restrained, --ar 16:9 --sref <SREF>"
- `scales_of_justice` — "scales of justice as a clean silhouette, gold and silver, black background, single key light, symbolic not literal, --ar 16:9 --sref <SREF>"
- `document_seal` — "a close-up of an official document with a wax/embossed seal, shallow depth, gold accent, navy tone, symbolic of law, --ar 16:9 --sref <SREF>"
- `jail_bars_light` — "light falling through prison bars onto a bare floor, high contrast, cold blue + warm sliver, no figure, somber, --ar 16:9 --sref <SREF>"
- `constitution_parchment` — "aged parchment with handwritten script, candle-lit, gold edge, extreme shallow focus, symbolic of founding law, --ar 16:9 --sref <SREF>"

## "Hidden system" / conceptual (for the channel's signature angle)
- `network_system` — "abstract network of glowing electric-blue nodes and lines over black, a hidden system made visible, minimal, --ar 16:9 --sref <SREF>"
- `gears_machine` — "interlocking metal gears in dramatic chiaroscuro, silver and gold, symbolic of an institutional machine, --ar 16:9 --sref <SREF>"
- `domino_cause` — "a line of toppling dominoes in dramatic light, cause-and-effect symbol, navy + gold, --ar 16:9 --sref <SREF>"
- `spotlight_void` — "a single hard spotlight on an empty stage in darkness, isolation / scrutiny, --ar 16:9 --sref <SREF>"

## Texture / breather / transition (often loopable or as parallax plates)
- `map_texture_us` — "stylized dark map texture of the United States, faint electric-blue topographic lines on black, no labels, --ar 16:9 --sref <SREF>"
- `paper_grain` — "subtle aged paper grain, near-black with faint gold flecks, full-frame texture, --ar 16:9 --sref <SREF>"
- `dust_light` — "floating dust motes in a shaft of cold light, black background, atmospheric breather, --ar 16:9 --sref <SREF>"
- `negative_space_blue` — "minimal deep-navy gradient with a single faint electric-blue horizon glow, lots of negative space for text, --ar 16:9 --sref <SREF>"

## Vertical variants (for thumbnails / mobile, --ar 2:3)
- `gavel_portrait`, `scales_portrait`, `network_portrait` — same prompts with `--ar 2:3`.

> Each motif: generate, pick best (Claude recommends), save to SSD, register with `motif_id`,
> `orientation`, `sref`, `content_hash`, `rights_basis`, `verified_at`. Episode-specific imagery
> (the actual case, people-as-symbol, specific places) is NOT here — it lives per episode.
