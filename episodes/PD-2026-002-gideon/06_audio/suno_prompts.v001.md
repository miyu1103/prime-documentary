# Suno prompts — PD-2026-002-gideon (v001)

House sound (match the 21-track library): cinematic documentary underscore, piano + strings / warm
pads, restrained and tasteful, **instrumental (no vocals)**, sits under narration, neutral-authoritative.
Master target −14 LUFS; beds run −18…−22 LUFS ducked under VO (I handle mastering/ducking).

## How to use
1. In Suno: paste the **Style** text, turn **Instrumental ON**, set the length, generate 2 variants.
2. Download everything to `H:\pd-media\downloads\inbox` (no renaming). I'll route + register each in the
   music library with rights (`suno_commercial`, owner-generated, hash, date).
3. **You do NOT have to generate the "reuse" rows** — we already own those. Minimum to generate = the
   1 GAP track (#1). The others are optional "fresh EP2 signature" tracks so this episode does not
   sound identical to Miranda — generate as many or few as you like.

---

## Cue → music map (what plays where)

| Cue | Scenes | Reuse from library (default) | Generate fresh? |
|---|---|---|---|
| hook_bed | S001–S002 | MUS-0001 / MUS-0002 (hook) | optional → **#2** |
| opening_bed | S003–S005 | MUS-0003 / MUS-0004 (opening) | reuse |
| tension / the wall | S006–S012 | MUS-0007 / MUS-0008 (tension_build) | optional → **#3** |
| reveal / the 9–0 ruling | S013–S018 | MUS-0013/0014/0015 (reveal "verdict at dawn") | optional → **#4** |
| **expansion → strain** | S020–S024 | (no exact match) | **#1 — GENERATE (gap)** |
| outro | S025–S028 | MUS-0016 / MUS-0017 (outro) | reuse |
| ambience (×4 beds) | all | MUS-0018..0021 (room-tone + paper) | reuse |

---

## Prompts to generate

### #1 — `gideon_expansion_strain`  ★ MUST (fills the only real gap), ~2:30, instrumental
**Style:**
`Cinematic documentary underscore in two halves. First half: hopeful and expansive — warm strings and gentle piano, a sense of a promise spreading outward across the whole country, quietly uplifting. Second half: the same theme turns weary and unresolved — the chord never fully lands, a faint unease and weight settles in, suggesting a promise that is real but underfunded and unfinished. Restrained, tasteful, no vocals, no drums build to a climax, 80 BPM, leaves space under narration, long sustained tail.`

### #2 — `gideon_hook_pencil`  (optional fresh hook), ~2:00, instrumental
**Style:**
`Cold-open documentary underscore, very sparse and tense. A single delicate recurring tick like a pencil tapping on paper or a soft pizzicato, over a low sub-bass pulse and faint cold air texture. Curious and suspenseful, no melody, leaves wide space for a spoken question, 76 BPM, restrained, instrumental, no vocals.`

### #3 — `gideon_wall_betts`  (optional tension variant — "the wall"), ~2:00, instrumental
**Style:**
`Slow-building cinematic tension. Heavy low strings and distant timpani over a cold, immovable sustained drone — the feeling of standing before an immense stone wall that blocks the way. Controlled, oppressive, gradually rising but with NO release or payoff (the obstacle holds), 92 BPM, instrumental, no vocals, sits under narration.`

### #4 — `gideon_unanimous_reveal`  (optional payoff — the 9–0 ruling), ~1:50, instrumental
**Style:**
`Dignified triumphant reveal underscore. A warm full resolution of brass-like pads and strings with bright but tasteful piano, the clean satisfying sense of a unanimous, just verdict landing — hopeful and resolved, NOT bombastic or action-movie. Builds to one clear harmonic payoff then a long warm sustained tail, 88 BPM, instrumental, no vocals.`

### #5 — `gideon_outro_pencil_reprise`  (optional fresh outro), ~2:30, instrumental
**Style:**
`End-card documentary underscore, hopeful and resolved. Warm piano and strings with a soft pulse, gently reprising a simple delicate motif (a nod to the pencil), subscribe / next-episode CTA feel, clean confident ending, 92 BPM, instrumental, no vocals, sustained final chord.`

---

## After you download
- Drop all variants in `H:\pd-media\downloads\inbox`; tell me "music in."
- I'll audition them, pick the best take per cue, route to the library + SSD `07_music/`, and register
  rights + content hash. Reused tracks are already cleared.
