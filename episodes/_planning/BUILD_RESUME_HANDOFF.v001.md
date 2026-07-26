# EP50/51/52 BUILD — resume HANDOFF (v001, 2026-07-26)

Lets any session RESUME the EP50/51/52 build campaign (overnight, GPU-serial). Read memory `MEMORY.md` first, especially [[feedback-thread-retro-20260725]] (the pipeline root causes + fixes) and `pd-ep50/51/52-status`. Repo `C:\Users\aab15\Documents\prime-documentary`, media `H:\pd-media`, git branch `claude/vibrant-archimedes-2mmr5h`.

## ★ THE FIXED PIPELINE (apply to ALL THREE episodes — this is why EP50's first build failed)
EP50 shipped-then-failed the owner watch-through (紙芝居/warp/no-faces/no-stock/4-line-captions/repetitive/missing-opening/flicker). Root causes + fixes (details in the retro memory + `EP50_VISUAL_REBUILD_SPEC.v001.md`):
1. **Warp/scanline:** `build_centralpark_film.py` had `treatments = ["depth","scan",...]`. FIXED → `["bleed","duotone","focus"]` (parallax motion, NO warp). When cloning for EP51/52 build scripts, use the SAME treatment set. Never use depth/scan/card.
2. **2-line captions:** `build_captions` now splits >84-char cues via `_split_caption_text`. Keep this in the EP51/52 build scripts.
3. **紙芝居:** do NOT fill factory with Ken-Burns-on-stills (that IS the 紙芝居). Use REAL stock (`H:/pd-media/assets/stock/video`, 74 clips) + i2v motion. Lower still-share from ~41% → ≤~20%. Add MORE motion cuts.
4. **Faces + variety:** generate diverse SDXL at **MAX QUALITY** (4K: base 1536x864 → hires-fix Latent 3072x1728 → R-ESRGAN 4x → 3840x2160, 34 steps; owner: "SDXL使う際は最高品質で"). Generic anonymized people (NOT real living defendants) + diverse scene types (not monotone dark rooms).
5. **Keep the gold BrandOpening** (do NOT trim it away). Cold-open-from-0:00 is DE-PRIORITIZED.
6. **AE density:** more figure/AE beats than 36/61min.
7. Run ONE SDXL generator at a time (a race left 25/36 low-q); kill old process (verify wmic) before relaunch; skip-guard checks height>=2000.
8. **GATE: watch the WHOLE runtime yourself before showing the owner** — a defect-frame scan is NOT enough (this is the repeated miss).

## STATE (2026-07-26, live)
### EP50 centralpark (61-min, first flagship) — REBUILDING
- narration ✅ master `H:/pd-media/episodes/PD-2026-050-centralpark/06_voice/master/vc_master_v001.mp3` (3643s), index `06_audio/narration_index.v001.json`.
- stills ✅ 860 @ H:/pd-media/assets/ai/centralpark/S*.png (real). factory 485 (real files but static Ken-Burns), motion 170.
- NEW rebuild assets (MAX-Q 4K): **P01-P36 people/faces DONE**; **V01-V48 diverse scenes GENERATING** (`scripts/gen_centralpark_scenes_sdxl.py`, chained after people). Both → H:/pd-media/assets/ai/centralpark/ + remotion/public/centralpark/img/.
- build script `scripts/build_centralpark_film.py`: warp-fix + caption-fix APPLIED. film.json → `remotion/src/data/centralpark_film.json`.
- REMAINING: (a) i2v real motion from stills/people (Wan; driver ref `C:/Users/aab15/ae-demo/comfy_wan.py`, ComfyUI :8188) — replace static factory with motion; (b) select real stock (74 clips) into pools; (c) update asset_manifest to inject P/V + stock + motion, raise motion / lower still-share, more AE; (d) rebuild film.json (build_centralpark_film.py); (e) re-render (`npx remotion render CaseFilm out/centralpark.mp4 --public-dir=public_slim`, redirect stdout to a LOG file, include ALL public assets incl narration mp3); (f) BGM (build_centralpark_bgm_real.py) → AE composite (scripts/ae/composite_centralpark_hero.py) → KEEP opening (no trim); (g) FULL-runtime watch QC.
### EP52 morton (30-min) — assets mostly real, factory stubbed
- narration ✅ (1785.8s, 319 chunks, all Brian). stills ✅ 215 real 4K. motion ✅ 43 real i2v. faces ✅ T01-T03. **factory ❌ 227/240 are 11KB black stubs** (13 real: Texas houses/courthouse/gavel/capitol). FIX with real stock + i2v (NOT Ken-Burns). Then build with the fixed pipeline (clone build_centralpark_film.py → morton; treatments/captions fixes; keep opening).
### EP51 willingham (20-min) — stills only, rest pending Codex
- narration ✅ (1208.8s, 218 chunks, all Brian). stills ✅ 150 real 4K. motion/factory: owner said Codex is generating them — **AUDIT by file-size/luma before trusting** (Codex ships black stubs). Then build with the fixed pipeline.

## ORDER (GPU-serial, solo): EP50 (finish, proves pipeline) → EP51 (audit Codex motion/factory, then build) → EP52 (factory fix via real stock+i2v, then build) → EP53 → EP54 → EP55.
## SCOPE EXTENDED (owner 2026-07-26): build through EP55. EP53-55 are GATED on scripts — themes are being picked in the theme-selection thread (THEME_SELECTION_HANDOFF.v001.md); a script thread should write their 3×-checked scripts. Build each Ep as soon as its script + narration + assets exist. Do NOT wait idle — EP50/51/52 are buildable now; 53-55 follow as scripts land.
## CONSTRAINTS: one GPU job at a time (4090; VRAM crash = silent no-output); another session runs GPU-free CTR/theme work — coordinate SDXL/render windows. Max quality always. Don't schedule/publish without owner approval.

## ★ DEEP-RESEARCH GATES (2026-07-26, apply to EP50 opening + ALL of EP51-55)
Canon: `DEEP_RESEARCH_FINDINGS.v001.md` + memories pd-retention-rules / pd-opening-formula / pd-structure-template / pd-craft-checklist / pd-distribution-actions / pd-audience-profile. Real curves: `scripts/_yt_retention_curves.json`.
- OPENING (rules 1-3): cold-open, VO from frame 0, case-specific first frame, person+hard-specific+incongruity first sentence (never a question), name the human ≤0:15, crime+opposing-force ≤0:28, BUT-loop by ~0:32, THEN gold brand ≤5s audio-continuous fused with "This is the case of ___", post-brand = ONE escalating concrete. NO brand-first / thesis paragraph.
- RETENTION: NO explanation block 60-180s (no ≥20s person-action-free exposition before first payoff; fold context 1 sentence at a time). New-info beat ≤45s in first 2 min; emotional core ≤90s. Mid decay ≤1.5pt/min; no 90s+ without a number/name/date.
- REVEALS staircase: shock 0% → mid ~50% → MAIN reveal starts 65-85%, resolved by 92%; NO new facts after 92%.
- NO emotional imperatives ("Sit with that", "Hold that name") — evoke via specifics.
- AUDIENCE: 93% male, 91% 55+ → frame "man broken by the system / your rights", weighty not sensational; big captions (mobile 69% + older eyes); 97% first-time (zero brand trust).
- TITLES: stakes-gap numbers (minor→7-15yrs) > time-jump; ban "Exonerated after N years" (write as ongoing injustice).
- CODEX ONE-SHOT IMAGES (§5.5a): same motif ≤2/beat, reappearance needs visible state change, no mass similar variants, person ≥40%.
- PROCESS: liveness = PID exists + CPU-time increment + StartTime (NOT agent-"done"/file-exists/RAM); on FAIL/anomaly suspect the instrument, read raw data; "broken/exists" in memory = dated hearsay, verify the real artifact before acting; verbatim quotes not written until primary-record-checked.
