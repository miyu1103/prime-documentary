# Midjourney prompts — episode-specific stills (PD-2026-001-miranda, v001)

Episode-specific imagery referenced by `scene_plan.v001.json` as `MJ-EP:*`. Generic reusable
motifs (`MOT:*`) come from the shared library (`prompts/12_visual_motif_library_prompts.md`),
not here. Owner generates in Midjourney; **Claude views the 4-up and recommends the best pick**
(criteria: composition / `--sref` match / no breakage / scene-intent / symbolic-not-real).

Rules: stylized & symbolic, **never photoreal-as-evidence** (invariant 11). Anything touching the
real person/case is a **clearly symbolic reconstruction with no real likeness** (docs/32). Replace
`<SREF>` with the locked brand style-reference seed. `--ar 16:9` unless noted. Palette: black/navy +
electric blue + silver + gold.

| Asset id | Scenes | Notes |
|---|---|---|
| MJ-EP:constitution-fifth-amendment | S002, S014 | symbolic, no real document facsimile needed |
| MJ-EP:interrogation-room-symbolic | S004 | **reconstruction, no real likeness** |
| MJ-EP:courtroom-1960s-symbolic | S007 | empty/symbolic, no identifiable people |
| MJ-EP:miranda-warning-card | S016 | object still of a generic rights card |
| MJ-EP:retrial-symbolic | S018 | **symbolic only, no real likeness** |

## Prompts

### MJ-EP:constitution-fifth-amendment  (S002 / S014)
"Close-up of an aged constitutional parchment, the words 'nor shall be compelled' faintly legible in old script, candle-warm key light with cold electric-blue rim, gold edge, deep navy background, shallow depth of field, symbolic of the Fifth Amendment, no modern objects --ar 16:9 --sref <SREF>"

### MJ-EP:interrogation-room-symbolic  (S004) — reconstruction, no real likeness
"An empty 1960s-style interrogation room at night, a single hard overhead lamp on a bare metal table and one empty chair, long shadows, cold blue light with deep black, nobody present, tense and quiet, cinematic, symbolic reconstruction — not documentary footage, no people, no faces --ar 16:9 --sref <SREF>"

### MJ-EP:courtroom-1960s-symbolic  (S007)
"A symbolic mid-century American courtroom interior, empty judge's bench and wooden rail in dramatic chiaroscuro, dust in a shaft of cold light, gold accents, no identifiable people, restrained and authoritative --ar 16:9 --sref <SREF>"

### MJ-EP:miranda-warning-card  (S016)
"Macro still of a worn printed 'rights' card held in shadow, generic typed lines (not legible as any real text), electric-blue and gold tone, shallow focus, symbolic of a recited police warning, no logos, no real insignia --ar 16:9 --sref <SREF>"

### MJ-EP:retrial-symbolic  (S018) — symbolic only, no real likeness
"A symbolic image of a second trial: two faint overlapping courtroom silhouettes, an hourglass or a gavel doubled, cold blue with a single gold thread, sense of 'reversed, then again', fully abstract, no real people, no faces --ar 16:9 --sref <SREF>"

> After generation: save the chosen still to the SSD media tree
> (`artifact://episodes/PD-2026-001-miranda/05_visuals/approved/...`) and register it in
> `library/visual/visual_registry.v001.json` only if it is reusable; episode-specific picks stay
> with the episode. Record `content_hash`, `--sref`, `rights_basis`, `verified_at`.
