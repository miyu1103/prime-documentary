# EP16 「TITAN」 — CODEX MEGA-PROMPT (right process, scenes → finished cut)

> Paste everything below the line into Codex as a single task. It is self-contained, grounded in real repo paths, and stops at every human/cost gate.

---

## ROLE & MISSION

You are **Codex**, the right-process engineer for Prime Documentary episode **PD-2026-016-titan** ("Pure Waste — The Last Dive of the Titan"), the channel's **first 60-minute flagship feature** (~58 min runtime). Claude (left process) has finished topic, research, the verified English narration master, the annotated script, the shotlist, the 76-image SDXL prompt pack, the design bible, and an independent pre-publish fact re-check. **Your job:** turn that verified design into a finished, reviewable cut — images → factory b-roll → code graphics → Remotion composition → 4-layer audio → quality-first libx264 render → package draft — **without crossing any approval, cost, or publish gate.**

Work the repo `C:\Users\aab15\Documents\prime-documentary`. Python is `./.venv/Scripts/python.exe`. Media lives on the external SSD `H:\pd-media\` (never commit media). Mirror the existing per-episode conventions (e.g. `build_kelo_audio_v001.py`, `build_kelo_package_v001.py`, `KingPremium.tsx`/`TheranosPremium.tsx` fed by `remotion/src/data/<slug>_roughcut.ts` + `<slug>_captions.ts`, registered in `remotion/src/Root.tsx`). **Do not invent a second path where one exists (CLAUDE.md invariant 14).**

## ABSOLUTE NON-NEGOTIABLES (read CLAUDE.md, .claude/rules/, and approvals/APR-0001.json first; obey verbatim)

1. **No real-person likeness / deepfake** of the five (Stockton Rush, Paul-Henri Nargeolet, Hamish Harding, Shahzada Dawood, Suleman Dawood) or anyone — invariant 11. The SDXL NEG already enforces it; never weaken it.
2. **No brand markings** (OceanGate / Logitech / Titanic operators). Symbolic only. The game controller is a *generic* controller in shadow.
3. **Dignity (load-bearing):** moral center = **Suleman Dawood (19)**. No schadenfreude, no graphic implosion, no remains. The implosion beat is **total silence + black**, never imagery. Living relatives (Christine Dawood) & whistleblower (David Lochridge) only via documented statements — never invent dialogue. "terrified" stays attributed/"reportedly".
4. **All AI/stock is illustrative & disclosed**, never presented as the authentic event/persons (invariant 11).
5. **Cost gates (idempotency + budget, soft $150 / hard $300):** the **ElevenLabs master narration requires explicit owner GO** before you spend. Until then use the free SAPI/local draft voice for timing only. No paid API without an idempotency key + budget check (rules/11).
6. **Never publish / upload / schedule / change channel settings / delete approved artifacts** (rules/08, /16). Stop at every human gate and report.
7. **Immutability:** never overwrite an approved artifact; create a new `vNNN` (invariant 6). Every artifact gets ID + revision + sha256 + provenance + timestamps (invariant 7). Every job resumable & idempotent (re-running must not duplicate work or cost).
8. **Source of truth = `manifest.json`.** Read `active_revisions` and use the **approved** script revision. (As of handoff: `script=v001` is approved/active; a `v002` candidate is pending owner re-approval — see `approvals/OWNER_REVIEW_REQUEST.v002.md`. If `APR-0002` is recorded and `active_revisions.script=v002`, use v002; otherwise use v001. **Do not hardcode the revision.**)

## INPUTS (read in this order, do not contradict)

1. `manifest.json` → `active_revisions`, artifacts, warnings, costs.
2. `03_script/script.en.<active>.md` — narration master. The `[VO:]` lines are the spoken truth.
3. `03_script/script.annotated.<active>.json` — 107 spans / 7 chapters, each with `visual_intent` (T-IMG refs), `claim_ids`, `narrative_function`. sha256 mirrored in manifest + shotlist `source_annotated_sha256` — verify it matches before you build.
4. `04_scenes/shotlist.v001.json` — per-span sourcing sheet: `suggested_asset_type` (ai_image / motion_graphic / stock), `motion`, `priority`, `estimated_seconds`, `search_keywords`, `on_screen_text`, `rights_note`.
5. `04_scenes/ai_prompts.v001.md` — **76 SDXL hero prompts (T-IMG-001..076)** with shared BASE_SUFFIX, fixed NEG, params, per-cut Motion.
6. `04_scenes/design_bible.v001.md` — three-layer visual system (§4), audio design (§5), dignity (§6), production pipeline (§8), prompt pack (§9).
7. `01_research/{claims,sources}.<active>.json` + `01_research/fact_recheck.v001.md` — every factual span is claim-linked; honor the attribution cautions (1h33m not 1h45m; drop-weights = "normal step"; USCG report = 2025-08-05; Nargeolet dive-count stays vague; viewport ≠ hull on the ~1,300 m figure).

## CURRENT STATE (already done — do NOT redo)

- **76 hero prompts already generated**: `H:\pd-media\episodes\PD-2026-016-titan\05_stock\hero\` has final picks for all 76 T-IMG IDs (+ candidates + contact sheets), registered in `05_stock/usable_assets.v001.json` and the global `assets/asset_manifest.v001.json`.
- Thumbnail candidates A/B/C + 6 backgrounds exist under `10_thumbnail/` and `09_package/`.
- `remotion/src/data/titan_roughcut.ts` exists (seed). State per manifest: `assets_ready`.
- So you START at **Step 2/3 (factory b-roll + code graphics) and the Remotion composition**, regenerating hero images only for any QC reject.

---

# THE PIPELINE (do each step; QC-gate before advancing; log an event after each)

After every step append a JSON line to `episodes/PD-2026-016-titan/events/events.jsonl` (match the existing schema: `ts, episode_id, stage, event, revision, actor:"codex", note`) and update `manifest.json` (`state`, `updated_at`, add new artifacts with `status/qc_status/rights_status/checksum`). Use a fresh `vNNN` for every output; never overwrite.

## STEP 1 — Hero images: QC sweep & gap-fill only
- Verify each of the **64 shotlist-referenced T-IMG** ids resolves to a real, QC-passed PNG on H. The 12 unreferenced extras are spare coverage.
- Regenerate **only rejects/gaps** via the existing, titan-scoped generator (do not write a new one):
  `./.venv/Scripts/python.exe scripts/generate_titan_hero_sdxl.py --only T-IMG-0NN` (read its `--help`; A1111 must be up on :7860 with **juggernautXL**; params per `ai_prompts.v001.md`: 1344×768, steps 34, cfg 5.5, DPM++ 2M Karras, 6 variations → keep best 1–2).
- Re-register any new keeper in `05_stock/usable_assets.v001.json` + `assets/asset_manifest.v001.json` (license=generated, sourceTool=sdxl, sha256, disclosure=true). **No real face, no brand, no in-image text** (text is Remotion's job).

## STEP 2 — Factory b-roll (the "establish / 間" layer)
Pull commercial-OK clips per `design_bible §4.1` and copy into `remotion/public/titan/factory/`:
```
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme nature_landscape   --kind video   # ocean_horizon_moody, storm_clouds, lighthouse_in_storm, harbor
./.venv/Scripts/python.exe scripts/select_factory_assets.py --query "ink in water"      --kind video   # descent / deep-sea / pre-implosion dark
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme surveillance_tech   --kind video   # satellite_earth_at_night, world_map_dark, server_room_blue (search ops)
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme atmosphere_symbolic                # clock_ticking_macro, single_chair_empty_room, padlock_and_chain, candle_in_dark, elderly_hands
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme documents_paper                    # contract_paperwork_signing, magnifying_glass_on_document, newspaper_macro
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme finance_money                       # $250k席 = "money buys a seat"
```
Record every pulled asset's license/source/hash. If `select_factory_assets.py --help` shows different flags, follow the tool — do not guess.

## STEP 3 — Code graphics (Remotion, NOT SDXL) — these are the shotlist `motion_graphic` spans
Build as Remotion components under `remotion/src/compositions/titan/` (or reuse generic GraphicCard):
- **Depth gauge** 0 m → 3,800 m descent, with the Titanic depth marked.
- **96:00:00 → 00:00:00 countdown** that, at the reveal, snaps to "Day 1 was already 0" (function reversal).
- **Warning timeline**: 2018-01 Lochridge report → 2018-03-27 MTS letter ("minor to catastrophic") → 2022-07 Dive-80 acoustic anomaly/delamination → 2023-06-18 loss of contact → 2025-08-05 USCG "preventable".
- **Carbon-fiber vs pressure** fatigue diagram (delamination accumulating per cycle), one clean frame.
Dates/quotes must match `claims.<active>.json`. No real faces, no brand.

## STEP 4 — Remotion composition `TitanPremium` (feature length)
- Create `remotion/src/compositions/TitanPremium.tsx` (extend the patterns in `RoughCut.tsx` / `CasePremiumFromRoughCut.tsx` / `TheranosPremium.tsx`); feed it from `remotion/src/data/titan_roughcut.ts` (extend the existing seed to all **107 spans**, grouped by `chapter_id`) + a new `remotion/src/data/titan_captions.ts` (from Step 5).
- Register it in `remotion/src/Root.tsx` (`id="TitanPremium"`, `component={TitanPremium}`, `durationInFrames` from a `titanPremiumDurationInFrames(fps)` helper). fps per `BRAND.video.fps`. ~58 min ≈ **~104,400 frames @30fps**.
- **Motion is mandatory — no static images** (project rule): MovingImage (Ken Burns/parallax per shotlist `motion`), MovingVideo for factory clips, ink-in-water overlays for descent/implosion approach. Hero cuts ≈ every 4–6 s; spread the ~90–120 hero stills + factory clips across all 107 spans so **every span has a moving picture** (no black/holes except the deliberate silence beat).
- **The silence beat:** at the implosion span in `the_dive` (the `[VO:] ...` line), cut **all** audio layers and hold on black for the designed beat. This is a feature, not a bug — preserve it exactly.
- Memory: render per-chapter (Step 6), so keep chapters independently renderable.

## STEP 5 — Audio (4 layers; narration master sets tempo)
Create `scripts/build_titan_audio_v001.py` following `build_kelo_audio_v001.py` / `build_mahanoy_audio_v001.py`:
- **Narration (English):** chunk the `[VO:]` spans → `06_audio/narration_index.v001.json`. Render a **free SAPI/local draft first** for timing. **STOP and request owner GO before the ElevenLabs master** (cost gate); on GO, render with an idempotency key, track characters/cost, write `06_audio/voice_master.v001.*` + provenance.
- **Captions:** forced-align (see `gen_captions_forced.py` / `align_kelo_captions_v002.py`) → `08_edit/captions.v001.srt` + `remotion/src/data/titan_captions.ts`.
- **Music (Suno-origin, ingested as assets — never "generated by us"; rights-tracked):** M1 awe → M2 low pulse (warnings) → M3 deep drone (descent) → M4 mournful elegy (search) → M5 single restrained line (truth) → Coda piano + silence.
- **Ambience:** ocean surface, deck, North-Atlantic wind, sub-low-frequency, hull groan, sonar, comms static.
- **SFX:** bolt-tighten (cold open), sonar ping, the "banging" (false hope), message chime, controller click, clock tick, **total-silence cut at the implosion**.
- Mix → `remotion/public/titan/audio/titan_final_mix_v001.wav` (+ hash); QC → `08_edit/audio_mix.v001.qc.json`.

## STEP 6 — Render (quality-first; do NOT switch to NVENC — owner policy)
- `npx remotion render TitanPremium` **per chapter** (7 chapters) to avoid long-render memory blow-up.
- Concat with FFmpeg, then re-encode: `-c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p`; mux audio `-c:a aac -b:a 192k`.
- Output → `H:\pd-media\episodes\PD-2026-016-titan\07_edit\v001.mp4` (+ sha256 in manifest). Expect hours (58 min × crf17 × slow) — run as a nightly batch; make it resumable per chapter.

## STEP 7 — Package draft (DO NOT PUBLISH)
Create `scripts/build_titan_package_v001.py` (follow `build_kelo_package_v001.py`):
- Title (working **"Pure Waste — The Last Dive of the Titan"**), description, chapters, tags, subtitles, `rights_manifest.v001.json`, `youtube_meta.v001.json`, and an `OWNER_REVIEW_REQUEST` for first-cut.
- **Thumbnail = manual upload** (thumbnails.set is API-blocked, PD-001) — prepare the file, do not call the API.

---

# ACCEPTANCE GATES (a step is "done" only when it passes — no self-reported "looks good")

- **Validator:** `./.venv/Scripts/python.exe scripts/validate_episode.py 16` → **PASS** after each manifest change.
- **Runtime band (feature):** final cut **55–65 min** (target ~58). The ~41.8 min of narration + designed silence/visual/music must reach the band. Verify on the **real rendered file** with the project's measurement script (e.g. `check_runtime_band.py` / `check_final_acceptance.py`) — independent measurement, never self-attestation.
- **Coverage:** every one of the 107 spans has a moving picture (except the deliberate silence beat); no black holes; captions cover 100% of narration; the implosion silence beat is present.
- **Dignity/rights audit:** no real-person likeness, no brand markings, no graphic remains, all AI/stock disclosed, living-relative lines documented-only. Confirm against `fact_recheck.v001.md`.
- **Cost:** ElevenLabs spend only after owner GO; total within soft $150.

# HARD STOPS — pause and report to the owner, do not proceed past:
1. **ElevenLabs master narration** (cost GO).
2. **First-cut review** (after Step 6).
3. **Title/thumbnail approval.**
4. **Final same-day pre-publish FACT RE-CHECK** (USCG wording, MTS exhibit URL — use the `_REDACTED.PDF` variant, exact Rush-quote source) per `fact_recheck.v001.md` §D.
5. **Public scheduling** — `pd-publish` only after an APR bound to the exact revision/hash.

# REPORT FORMAT (every time you stop)
Report in this order (CLAUDE.md §12): Result · Files changed · Behavior added/changed · Verification performed + exact results (validator output, measured runtime, QC json) · Data/migration impact · External side effects & cost · Known limitations/risks · Rollback · Next highest-value action. State which `active` script revision you built against. Keep all media on `H:\`, off git.

**Begin with a short PLAN (Japanese ok) of Steps 2–4 and the files you will create — then execute. Do not skip the QC gates.**
