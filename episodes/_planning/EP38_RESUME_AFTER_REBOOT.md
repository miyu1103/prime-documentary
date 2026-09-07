# EP38 Kids for Cash — RESUME after Windows restart (AE fix)

**Why reboot:** After Effects 2026 hangs on launch (engine init deadlock, no window, needs a
Windows restart — verified: not crash-dialog, not prefs, not licensing). Owner chose to reboot
so AE can be used for premium hero inserts. This session ends at reboot; a NEW session resumes
from this file.

## STATE AT REBOOT (all in repo, persists)
- **Canonical CaseFilm pipeline WORKS.** Latest render: `episodes/PD-2026-038-kidsforcash/08_edit/kidsforcash_casefilm.v001.mp4` (video, 16917f @30fps, 9:24) → BGM-muxed: **`08_edit/kidsforcash_final_bgm.v002.mp4`** (4-layer -14 LUFS). This is the current best cut.
- Composition registered: `Ep38KidsForCash` in `remotion/src/Root.tsx` (imports `src/data/kidsforcash_film.json`). Render: `cd remotion && npx remotion render Ep38KidsForCash <out> --concurrency=4 --timeout=120000`.
- Fonts wired: `remotion/src/load-fonts.ts` (CSS @font-face Oswald/Anton/Archivo — do NOT use delayRender, it timed out the render).
- **Fixes already in v002:** restored dropped Act3 narration (Kenzakoski death — was a JP-annotation extraction bug in `gen_kidsforcash_narration.py`); 27 varied figures (7 kinds, 29% coverage) via `build_kidsforcash_figures.py`; brightened stills (gamma0.58+br1.12, in public/kidsforcash/img + 04_scenes/generated_images); **LightSweep REMOVED** from CaseFilm.tsx (owner: "上からの光いらん"); captions re-gen (worst 26.9cps); thumbnails (09_package, 3 gates pass); structure_4part (narration_index.v002.json OPENING marker); factory clip-QC manifest (05_visuals).
- Narration: master 543.5s at `remotion/public/kidsforcash/narration_master.mp3` (+ H:/.../06_voice/master/vc_master_v001.mp3 + public/kidsforcash/narration.mp3). word_timings.v001.json regenerated. narration_index v001 (builder reads this) + v002 (gate reads, has OPENING).

## NEXT STEPS (post-reboot, in order)
1. **Verify AE launches**: `"/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.com" -r <a jsx that quits>`. If it opens/quits cleanly, AE is healthy.
2. **Render 7 AE hero clips**: scripts saved in `episodes/_planning/ae_hero/` (build_hero.jsx, cfg_*.jsx, run_hero.sh, render_all_heroes.sh). **FIX PATHS FIRST**: run_hero.sh/render_all_heroes.sh point at the OLD scratchpad dir (wiped on reboot) — repoint them to `episodes/_planning/ae_hero/` and output to `remotion/public/kidsforcash/ae/hero_<name>.mp4` (1920x1080, 30fps, H.264). Heroes: money(S07), waiver(S22), verdict(S16,"28 YEARS"), title(S03/S12), ninety(S03), inventory(S08), families(S15,"$200M+"). Fonts Oswald/Anton (`td.font="Anton"`), match H.264 template by substring, kill lingering AfterFX before aerender. See memory [[reference_after_effects_automation]].
3. **Insert AE clips into CaseFilm**: add them as `kind:"footage"` (or a dedicated hero cut) in `remotion/public/kidsforcash/film_data.v001.json` + `src/data/kidsforcash_film.json` at the matching hero beats (money ~film 208s, verdict ~469s, etc. = narration time + 11.533 offset). CaseFilm plays footage cuts via staticFile.
4. **Re-render** Ep38KidsForCash → **BGM mux** `py -3.11 scripts/build_kidsforcash_bgm_v2.py <render> <final>` → **gate**.

## REMAINING GATE FAILS — measured on v002 (2026-07-15 gate run, RESULT: FAIL)
7 hard fails. Everything else (structure, motion_energy 48.0, animation_density 0.3%,
motion_density 28.3%/7 forms, bgm_present, loudness -14.0, caption match 100%/sync,
op_ed_bookends, thumbnails, footage_diversity 0.47) PASSED.
- **caption_integrity** ⚠️REAL BUG: "no burned narration captions in the render — film-timed captions json MISSING; non-kinetic caption tag ABSENT; data.captions not mounted (film captions[]=260)". film_data HAS 260 captions but CaseFilm isn't rendering them into the video. The SRT-vs-narration checks pass (they read the file), but the actual MP4 has no burned subs. FIX: mount `data.captions` in CaseFilm.tsx caption layer / emit film-timed captions json. Do this in the re-render pass.
- **footage_utilization**: 15/56 staged clips referenced 0 times (graduation_cap_toss, stack_of_hundred_dollar_bills, open_briefcase_of_cash, courthouse_steps x2, empty_chair_spotlight_grief …). → wire them into cuts or unstage them.
- **arc_nonrepeat**: 62/81 cut assets reused from OTHER episodes (forfeiture/cotton/kyllo/katz/unlock…). → need NEW footage not used before (SDXL/SVD — owner approved SDXL) or fresh factory pulls.
- **sound_layers**: no `06_audio/audio_provenance.v*.json` (build_case_film_audio.py never run). The ad-hoc bgm mux gives audible BGM but no provenance. → needs a `[VO:]`-annotated script for build_case_film_audio.py.
- **runtime_band**: NOTE — did NOT fail this run (body 551s). But total 9:24 is still under the 11.5-12.5 standard; owner may still want it longer. Re-check after edits.
- **preflight_receipt**: run `preflight_render_gate.py` BEFORE the next render.
- **probe_receipt**: run `check_final_acceptance.py <ep> --probe <60-90s slice.mp4>` first.

## GATE COMMAND
`PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe scripts/check_final_acceptance.py PD-2026-038-kidsforcash --render <final.mp4>` (slow ~12min; whisper+motion analysis).

## ROOT-CAUSE LESSON (already in memory [[feedback_start_from_canon_pipeline]])
The long rework spiral came from NOT starting on the canonical CaseFilm pipeline + acceptance gate. Now on-canon. Start every long-form here.
