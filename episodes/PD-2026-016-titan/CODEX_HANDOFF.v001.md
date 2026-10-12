# EP16 "TITAN" — Codex Handoff (right process)

**Episode:** `PD-2026-016-titan` · **State:** `script_verified` (validated PASS) · **Format:** feature (~58 min) · **Risk:** R2
**Owner of this brief:** Claude (left process) → **Codex (right process)** begins at scenes/assets.

> Claude has completed: topic, research (10 sources, 14 claims), verified script (6,266-word English master, FK 5.6, 0 filler, 14/14 claims), annotated script (107 spans / 7 chapters), shotlist, SDXL prompt pack (76 hero images), design bible. Validator: `./.venv/Scripts/python.exe scripts/validate_episode.py 16` → PASS.

## Inputs (read these, in order)
1. `03_script/script.en.v001.md` — narration master (the [VO:] lines are the truth).
2. `03_script/script.annotated.v001.json` — 107 spans w/ `visual_intent` (T-IMG refs) + `claim_ids`. sha256 in `manifest.json` + `04_scenes/shotlist.v001.json:source_annotated_sha256`.
3. `04_scenes/shotlist.v001.json` — per-span sourcing sheet (asset_type, motion, priority, est_seconds).
4. `04_scenes/ai_prompts.v001.md` — **76 SDXL hero prompts (T-IMG-001..076)** w/ BASE_SUFFIX, NEG, params.
5. `04_scenes/design_bible.v001.md` — three-layer visual system, audio design, dignity rules.
6. `01_research/{claims,sources}.v001.json` — every factual span is claim-linked; do not contradict.

## Non-negotiables (carry from CLAUDE.md + APR-0001)
- **No real-person likeness** of any of the five or Stockton Rush (invariant 11). NEG already enforces; never override.
- **No brand markings** (OceanGate / Logitech / Titanic operators). Keep symbolic.
- **Dignity:** moral center = Suleman (19). No graphic implosion/remains. The implosion beat is **total silence + black**, never imagery.
- All AI/stock is **illustrative/disclosed**, not "the actual event."
- No paid API without idempotency key + budget check (soft $150 / hard $300). **ElevenLabs master narration = owner GO required** (cost gate).

## Step 1 — Images (SDXL, local :7860, juggernautXL)
- Generate **T-IMG-001..076 × 6 variations** per `04_scenes/ai_prompts.v001.md` (append BASE_SUFFIX; fixed NEG; 1344×768; steps 34; cfg 5.5; DPM++ 2M Karras).
- Output → `H:\pd-media\episodes\PD-2026-016-titan\05_stock\hero\` → QC (`pd-generate-assets`) → keep ~1–2 best each (~90–120 usable).
- Register usable in `assets/asset_manifest.v001.json` / episode `05_stock/usable_assets.v001.json` (license=generated, sourceTool=sdxl, hash, disclosure).

## Step 2 — Factory b-roll (three-layer)
Pull per design_bible §4.1, copy to `remotion/public/titan/factory/`:
```
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme nature_landscape --kind video   # ocean_horizon_moody, storm_clouds, lighthouse_in_storm
./.venv/Scripts/python.exe scripts/select_factory_assets.py --query "ink in water" --kind video        # deep-sea / descent / implosion-approach
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme surveillance_tech --kind video      # satellite/world_map/server_room (search ops)
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme atmosphere_symbolic                  # clock_ticking_macro, empty_chair, candle, padlock_and_chain
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme documents_paper                      # contract/magnifying_glass/newspaper (waiver, warnings)
```
Layer: SDXL hero (meaning) × factory b-roll (establish/“間”) × code-graphics (data). 1–2 layers/cut.

## Step 3 — Code graphics (Remotion, not SDXL)
Depth gauge 0→3,800m vs Titanic depth · 96:00:00→00:00:00 countdown (reverses to “Day 1 already 0”) · warning timeline (2018 Lochridge / 2018-03-27 MTS / 2022 Dive-80 anomalies / 2025 USCG “preventable”) · carbon-fiber × pressure fatigue diagram. These live on the shotlist's `motion_graphic` spans.

## Step 4 — Remotion composition `TitanFeature`
- New composition (extend `Episode.tsx`/`RoughCut.tsx`); ~104,400 frames @30fps (58 min). Group by `chapter_id`.
- Drive from `RoughCutData`: shots from shotlist; **images NEVER static** (MovingImage Ken Burns / parallax; MovingVideo for b-roll). ImageShot cuts ~every 4.5s; distribute the ~90–120 hero stills + factory clips across all 107 spans.
- **Silence beat:** at the implosion span (the `[VO:] ...` in `the_dive`), cut ALL audio layers for a held black beat. Honor it.
- Long-render memory: render per-chapter then concat (Step 6).

## Step 5 — Audio (4 layers; narration master = tempo)
- **Narration (English):** SAPI draft first (free) for timing; **ElevenLabs master = owner GO (cost gate)**. Chunk from [VO:] spans → `06_audio/narration_index.v001.json`; forced-align → `08_edit/captions.v001.srt` + `remotion/src/data/titan_captions.ts`.
- **Music (Suno-origin, ingested as assets):** M1 awe → M2 low pulse → M3 deep drone → M4 mournful → M5 single line → Coda piano+silence.
- **Ambience:** ocean surface / deck / North-Atlantic wind / sub-low-freq / hull groan / sonar / comms static.
- **SFX:** bolt-tighten (cold open), sonar ping, the “banging” (false hope), message chime, controller click, clock tick, **total-silence cut at implosion**.
- Mix → `remotion/public/titan/audio/titan_final_mix_v001.mp3`; QC `08_edit/audio_mix.v001.qc.json`.

## Step 6 — Render (quality-first, do NOT switch to NVENC)
- `npx remotion render TitanFeature` per chapter → FFmpeg concat → re-encode `libx264 -preset slow -crf 17 -pix_fmt yuv420p`; mux audio `-c:a aac -b:a 192k`.
- Output → `H:\pd-media\episodes\PD-2026-016-titan\07_edit\v001.mp4` (+hash in manifest). Nightly batch (60 min × crf17 × slow = hours).

## Step 7 — Package + gates (DO NOT publish without owner)
- `pd-package`: title (working: **"Pure Waste — The Last Dive of the Titan"**), thumbnail (manual upload — thumbnails.set is API-blocked, PD-001), description, chapters, subtitles, rights_manifest.
- **Human gates remaining:** first-cut review → title/thumbnail → **pre-publish FACT RE-CHECK** (USCG wording, MTS exhibit URL, Rush-quote source) → public scheduling. `pd-publish` only after APR for the exact revision/hash.

## State path
`script_verified → scene_planned → asset_plan_ready → assets_generating → assets_ready → audio_generating → audio_ready → edit_assembly → edit_review → finalizing → package_ready → publish_approved → scheduled → published`
