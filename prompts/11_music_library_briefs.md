# 11 — Music Library Briefs (Suno)

Reusable music library for the US court-case channel (decisions/0002 §C). Generate **once**,
register in `library/music/music_registry.v001.json`, then auto-select per scene.

Brand sound: **cinematic, restrained, neutral-authoritative**. Never melodramatic; music loses
to narration (docs/07). Instrumental only (no vocals/lyrics). Target ~8 categories × ~6 tracks
(≈48) + 15–20 short SFX. Use Suno "instrumental" mode. Tag each with mood/bpm/energy/loopable.

Per-track registry fields to fill after generation: `track_id` (MUS-NNNN / SFX-NNNN), `category`,
`mood`, `function`, `bpm`, `energy` (1–5), `duration_sec`, `loopable`, `suno_prompt`,
`content_hash`, `rights_basis` (Suno terms, commercial), `verified_at`.

> Suno tips: put each line in the **Style/description** box, toggle **Instrumental ON**, leave the
> lyrics box empty. Make 1–2 takes per prompt, keep the best. The BPMs are varied on purpose so the
> library doesn't sound samey.

## Categories (≈6 each; vary key/tempo for variety, keep the family coherent)

### hook (energy 3–4 — tense cold-open, leaves room for a spoken question)
1. "Cold-open underscore, sparse felt piano + low sub pulse, one slow rising synth swell, tense but restrained, no melody, leaves space for narration, 78 BPM, cinematic, instrumental."
2. "Minimal ticking percussion + distant string drone, suspense without resolution, electric-blue cinematic mood, 80 BPM, loopable bed, instrumental."
3. "Single low piano note motif + airy tension pad + slow heartbeat sub, ominous curiosity, 72 BPM, sparse, instrumental, no vocals."
4. "Muted pulse + faint metallic shimmer + unresolved minor drone, 'something is wrong' cold open, 84 BPM, loopable, instrumental."
5. "Dark ambient riser bed, low brass swell under a thin high line, building dread with no payoff, 76 BPM, instrumental, no vocals."
6. "Stark clock-like pulse + deep sub + distant pad, tense documentary intro, 88 BPM, leaves room for voice, instrumental."

### opening (energy 3 — confident, measured 'we will explain')
1. "Title-sequence underscore, measured piano arpeggio + warm low strings, confident and clear, 90 BPM, builds slightly then settles, instrumental."
2. "Steady mid-tempo pulse + clean piano + soft strings, purposeful, 96 BPM, instrumental, no vocals."
3. "Warm establishing theme, plucked strings + low pad + light percussion, authoritative calm, 88 BPM, instrumental."
4. "Cinematic intro bed, rising piano figure + sustained cello, beginning a serious story, 92 BPM, instrumental, no vocals."
5. "Measured documentary opener, soft mallets + low strings + gentle sub, neutral confidence, 94 BPM, loopable, instrumental."
6. "Clean modern explainer intro, minimal piano + airy synth + subtle pulse, premium and restrained, 90 BPM, instrumental."

### explainer_bed (energy 2 — unobtrusive, sits under narration, loopable)
1. "Neutral explainer bed, soft sustained pads + gentle pulse, no strong melody, sits under narration, 85 BPM, fully loopable, long and even, instrumental."
2. "Minimal warm drone + slow piano notes, calm and steady, leaves space for voice, 80 BPM, loopable, instrumental, no vocals."
3. "Soft ticking pulse + low pad + faint texture, forward motion without distraction, 88 BPM, loopable, instrumental."
4. "Ambient piano bed, sparse repeated motif + warm sub, patient and neutral, 82 BPM, loopable, instrumental."
5. "Gentle mallet pattern + sustained strings, light momentum, low under narration, 90 BPM, loopable, instrumental, no vocals."
6. "Subtle electronic bed, muted pulse + airy pad + soft bass, modern documentary underscore, 86 BPM, loopable, instrumental."

### tension_build (energy 4 — controlled crescendo, no big payoff)
1. "Slow-building tension, layered strings + rising arpeggio + soft timpani, controlled crescendo, 95 BPM, no resolution, instrumental."
2. "Escalating pulse + low brass swell + ticking percussion, stakes rising, 100 BPM, instrumental, no vocals."
3. "Minor-key string ostinato + growing sub + faint dissonance, mounting unease, 92 BPM, instrumental."
4. "Pulsing synth + tremolo strings building density, pressure without release, 104 BPM, instrumental, no vocals."
5. "Dark cinematic build, low piano stabs + rising drone + soft snare hits, tension toward a reveal, 98 BPM, instrumental."
6. "Layered arpeggio + accelerating pulse + low brass, taut restrained build, 96 BPM, no payoff, instrumental."

### somber (energy 2 — dignified human-cost moment, not maudlin)
1. "Somber reflective underscore, lone piano + cello, dignified not maudlin, 65 BPM, sparse, instrumental."
2. "Quiet mournful strings + distant piano, weight of a human cost, 60 BPM, instrumental, no vocals."
3. "Slow felt-piano theme + low drone, restrained sorrow, 62 BPM, sparse, instrumental."
4. "Lone cello line + soft pad, dignified melancholy, 58 BPM, instrumental, no vocals."
5. "Minimal piano + warm low strings, reflective and still, 64 BPM, instrumental."
6. "Sparse ambient elegy, single sustained string + faint piano, quiet gravity, 56 BPM, loopable, instrumental."

### reveal (energy 4–5 — clear resolution, the 'hidden system clicks')
1. "Reveal sting + bed, clear harmonic resolution, warm brass-pad swell + tasteful synth, 90 BPM, 8–12s sting plus sustained tail, instrumental."
2. "Bright resolving chord swell + soft percussion lift, the 'it clicks' moment, 92 BPM, instrumental, no vocals."
3. "Uplifting pad bloom + low brass + shimmer, insight landing, 88 BPM, sting plus tail, instrumental."
4. "Warm major resolution, strings open up + gentle sub drop, satisfying realization, 94 BPM, instrumental, no vocals."
5. "Cinematic reveal, rising piano + brass swell + airy shimmer, clarity and weight, 90 BPM, instrumental."
6. "Soft triumphant pad + clean synth motif resolving, restrained payoff, 96 BPM, instrumental, no vocals."

### outro (energy 3 — resolved end-card, subscribe / next-episode CTA)
1. "End-card underscore, hopeful resolved chords, piano + strings + soft pulse, subscribe/next feel, 92 BPM, clean ending, instrumental."
2. "Warm closing theme, gentle piano + low strings + light pulse, satisfying wrap, 90 BPM, instrumental, no vocals."
3. "Resolved mid-tempo bed, plucked strings + warm pad, forward-looking close, 94 BPM, instrumental."
4. "Calm uplifting outro, soft mallets + sustained strings, 'see you next time', 88 BPM, instrumental, no vocals."
5. "Clean modern end-card, minimal piano + airy synth + soft sub, premium close, 92 BPM, loopable tail, instrumental."
6. "Gentle hopeful resolution, piano arpeggio + warm low brass, dignified ending, 90 BPM, instrumental."

### ambience (energy 1 — room tone / texture, near-subliminal, loopable)
1. "Neutral room-tone bed, very low drone + faint noise, almost subliminal, no rhythm, fully loopable, instrumental."
2. "Tense interrogation drone, low sustained hum + faint metallic air, cold and still, loopable, instrumental, no vocals."
3. "Courtroom ambience texture, soft low rumble + distant space, neutral, loopable, instrumental."
4. "Dust-and-air swell, airy high texture + faint sub, a breather between cuts, loopable, instrumental."
5. "Dark suspense drone, deep sustained pad + subtle dissonance, glue under tension, loopable, instrumental, no vocals."
6. "Warm neutral texture bed, gentle low pad + faint shimmer, calm glue for explainer sections, loopable, instrumental."

## SFX (15–20 short one-shots, <2s unless noted)
- whoosh transition (short / medium), UI tick, soft impact/thud, paper rustle, gavel knock (subtle, non-cartoonish), camera-shutter for stills, low boom for chapter card, riser (2–3s) into reveal, fine "data" blip for diagrams, page-turn, clock tick loop (3s), subtle stamp/seal, quiet binder/lock, light dust/air swell, soft sub drop for hook end.

> SFX may be generated via ElevenLabs (automated, in-plan) instead of Suno; either way register
> with rights metadata.

> Note: Suno-origin tracks are **ingested assets** with rights metadata (not assumed programmatic;
> docs/07). Keep masters backed up off the single SSD (docs/34).
