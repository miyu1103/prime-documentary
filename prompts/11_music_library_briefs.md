# 11 — Music Library Briefs (Suno)

Reusable music library for the US court-case channel (decisions/0002 §C). Generate **once**,
register in `library/music/music_registry.v001.json`, then auto-select per scene.

Brand sound: **cinematic, restrained, neutral-authoritative**. Never melodramatic; music loses
to narration (docs/07). Instrumental only (no vocals/lyrics). Target ~8 categories × ~6 tracks
(≈50) + 15–20 short SFX. Use Suno "instrumental" mode. Tag each with mood/bpm/energy/loopable.

Per-track registry fields to fill after generation: `track_id` (MUS-NNNN / SFX-NNNN), `category`,
`mood`, `function`, `bpm`, `energy` (1–5), `duration_sec`, `loopable`, `suno_prompt`,
`content_hash`, `rights_basis` (Suno terms, commercial), `verified_at`.

## Categories (target ~6 each; vary key/tempo for variety, keep the family coherent)

### hook (energy 3–4)
- "Cold-open underscore, sparse piano + low sub pulse, single rising synth swell, tense but restrained, no melody, leaves space for a spoken question, 70–85 BPM, cinematic documentary."
- "Minimal ticking percussion + distant string drone, suspense without resolution, electric-blue cinematic mood, 80 BPM, loopable bed."

### opening (energy 3)
- "Title-sequence underscore, measured piano arpeggio + warm low strings, confident and clear, sense of 'we will explain', 90 BPM, builds slightly then settles, instrumental."

### explainer_bed (energy 2)
- "Neutral explainer bed, soft sustained pads + gentle pulse, unobtrusive, sits under narration, no strong melody, 85 BPM, fully loopable, long and even."

### tension_build (energy 4)
- "Slow-building tension, layered strings + rising arpeggio + soft timpani, courtroom stakes, controlled crescendo, 95 BPM, no big payoff (the reveal handles that)."

### somber (energy 2)
- "Somber reflective underscore, lone piano + cello, dignified not maudlin, for a human-cost moment, 65 BPM, sparse."

### reveal (energy 4–5)
- "Reveal sting + bed, a clear harmonic resolution, warm brass-pad swell + bright but tasteful synth, the 'hidden system clicks' moment, 90 BPM, 8–12s usable sting plus a sustained tail."

### outro (energy 3)
- "End-card underscore, hopeful resolved chords, piano + strings + soft pulse, subscribe/next-episode CTA feel, 92 BPM, clean ending, instrumental."

### ambience (energy 1)
- "Neutral room-tone / texture bed, very low drone + faint noise, almost subliminal, to glue cuts, no rhythm, fully loopable."

## SFX (15–20 short one-shots, <2s unless noted)
- whoosh transition (short / medium), UI tick, soft impact/thud, paper rustle, gavel knock (subtle, non-cartoonish), camera-shutter for stills, low boom for chapter card, riser (2–3s) into reveal, fine "data" blip for diagrams, page-turn, clock tick loop (3s), subtle stamp/seal, quiet binder/lock, light dust/air swell, soft sub drop for hook end.

> Note: Suno-origin tracks are **ingested assets** with rights metadata (not assumed programmatic;
> docs/07). Keep masters backed up off the single SSD (docs/34).
