# CODEX HANDOFF — EP21 D.B. Cooper (PD-2026-021-dbcooper)

> The single design document Codex reads to BUILD the episode. Claude owns the LEFT side
> (topic/research/claims/script) — done and LOCKED. Codex owns the RIGHT side
> (scenes -> images -> narration -> music -> motion -> edit -> render -> thumbnails).
> Build the FIRST render to satisfy the whole acceptance table. Numbers, not adjectives.

## 0. HARD CONSTRAINTS (do not cross)
- **R2 UNSOLVED case.** The FBI never charged, identified, or confirmed any suspect. NEVER assert or imply
  any named person "was D.B. Cooper." Suspects were proposed by relatives/authors/teams, NOT the FBI.
  Never accuse a living person; do not state a living/deceased status that isn't confirmed.
- **No real-person likeness** anywhere — the hijacker is ALWAYS faceless (from behind, shadow, silhouette);
  no real crew/suspect/agent faces. **No real airline / Boeing / FBI logos or seals. No readable text in
  images. No fake-1971 news-footage look.** Symbolic reconstruction only.
- No publish, no external upload, no paid API without owner approval + idempotency + budget check.
- Render LOCAL CPU libx264, quality-first; NEVER NVENC. Heavy media -> H:\pd-media\episodes\PD-2026-021-dbcooper\.

## 1. BINDING SPEC + ACCEPTANCE
- Build to the one-pass acceptance table (rows: voice/captions/runtime/BGM/loudness/black-frame/motion/hook/thumbnails).
- "Done" = these all exit 0 on the REAL file (not your opinion); loop build->measure->fix until green:
  ```
  ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 21 --json
  ./.venv/Scripts/python.exe scripts/check_dynamics.py 21
  ./.venv/Scripts/python.exe scripts/check_runtime_band.py <render.mp4>
  ```
- Duration profile: **mid, target 30:00** (runtime band 27-33; narration ~25-26 min at the real ~173-wpm voice).

## 2. LOCKED INPUTS (DO NOT REWRITE)
- Script: episodes/PD-2026-021-dbcooper/03_script/script.en.v001.md (~4,400 words; [VO:] only; "#" lines = production notes).
- Annotated: 03_script/script.annotated.v001.json (claim-linked spans + visual_intent).
- Claims (R2 wording locks): 01_research/claims.v001.json (15 claims). Sources: 01_research/sources.v001.json (10).
- Image prompts: 04_scenes/codex_image_prompts.v001.md (46 Codex prompts, one per scene).
- **R2 WORDING LOCKS (hold in every caption / on-screen text / thumbnail):** UNSOLVED, never "solved";
  never assert anyone "was D.B. Cooper"; FBI never confirmed any suspect (suspects proposed by third
  parties); alias = "Dan Cooper", "D.B." = a press mix-up; jump = "a little after 8 p.m." over "southwestern
  Washington"; passengers "about 36"; four parachutes; $200,000 in $20s; 1980 money find ~$5,800 at Tena Bar
  (serials matched, only cash recovered); 2016 = SUSPENDED, not solved.

## 3. STRUCTURE & TIMING
- Hook ~0:00-0:08 fast flash-forward montage (EP21-IMG-001..006, ~2s cuts) -> Opening (The Man Who Wasn't
  There) -> Body (Act 1 The Quiet Hijacking / Act 2 The Vanishing / Act 3 The Manhunt / Act 4 The One Clue)
  -> Ending (The Open Door), per the script timecodes.
- Gold BrandOpening lands AFTER the hook; BrandEndcard at tail. OP/ED canonical = remotion/src/components/Bookends.tsx
  (OPENING_SEC 3.5 / ENDCARD_SEC 9; do NOT fork). Drive EP21 through CasePremiumFromRoughCut (register in Root.tsx if needed).

## 4. VOICE (acceptance row 2)
- ElevenLabs master, VOICE_ID nPczCjzI2devNBz1zQrb, eleven_multilingual_v2, stability 0.35, similarity 0.80,
  style 0, speaker_boost on. Speak ONLY [VO:] lines; strip [CLM-xxxx]; ignore "#" lines. SAPI/local FORBIDDEN.
  Idempotency per chunk (skip existing — no double billing). Narration budget cap $25; exceed => STOP.

## 5. CAPTIONS (rows 3-4)
- Force-align to the rendered ElevenLabs audio (verbatim). 1 cue = 1 BREATH GROUP. <=2 lines, <=42 chars/line,
  1.0-6.0s, <=17 cps, >=2-frame gaps. **POSITION = lower 10-15% (bottom-safe), NEVER centered/high.** Brand font, drop-shadow, coverage >=95%.

## 6. MUSIC / BGM (row 1)
- Continuous library bed, one track per chapter; ducked under VO to an AUDIBLE floor ~ -22 LUFS (NEVER to
  silence); no silent stretch >25s; integrated -16..-12 LUFS.

## 7. IMAGES — Codex generation ONLY (row 5) — SDXL NOT used
- Generate the 46 prompts in 04_scenes/codex_image_prompts.v001.md, ONE image per prompt (no candidate pool);
  regenerate only a shot that fails its §0/§3. Long edge >= 3840 px, 16:9; brand palette (black/navy +
  electric-blue #1F6BFF + gold #E5B53A + silver). No face/likeness, no real airline/FBI logo/seal, no readable
  text, no fake-1971-footage. Register every used still in the rights manifest (AI-disclosed symbolic reconstruction).

## 8. MOTION / DYNAMICS / ABUNDANT MATERIAL (row 7-8) — fixes weak/static/"kaku"
- NO static image; NO frame held >2s; NO naked hard cut. Ken Burns >=6%/parallax on every still; designed
  0.3-0.5s crossfades; OVERLAP sequences so there is no 1-frame black; carry motion THROUGH the cut (no
  velocity reset); Trail motion blur on fast moves; >=1 hero/organic (SVD/2.5D) motion shot per 60s; average
  shot <= ~6s. Use the 221GB factory shelf abundantly: >=1 distinct clip per ~25-30s, factory layer across
  >=40% of the timeline, every span >=1 layer, no clip reused >3x. (scripts/select_factory_assets.py
  --theme crime/aviation/forest/1970s.) Emit 08_edit/asset_usage_report.json + 08_edit/motion_report.json
  (check_dynamics.py reads them; missing report = automatic fail).

## 9. DEDICATED SUBSCRIBE+LIKE CTA (~29:10-29:35)
- Build EXACTLY to the "# [PRODUCTION - DEDICATED CTA BEAT ...]" note in the script (gold SUBSCRIBE pill
  spring d14/s120 0.45s; gold underline wipe Easing.out(cubic) 0.5s; white LIKE thumb pop spring d10/s140,
  FILLS gold on the spoken word "theory" with 6% pulse + Trail spark; navy vignette; hold ~5s; ease out 0.4s;
  soft click SFX; music dips ~3 dB, bed audible). NO real YouTube logo. PD brand styling.

## 10. THUMBNAILS (rows 11-13)
- >=3 variants as Remotion <Still> @1280x720 from the image library (NO face, NO real logo, NO real-footage
  look). Loud: UPPERCASE <=3-4 words, very high contrast black/navy + gold #E5B53A or electric #1F6BFF,
  white/silver text, legible at 320px. Title <=60 chars; A/B. Headline ideas: "STILL MISSING" / "$200,000 GONE" /
  "WHO WAS HE?". Pick a selected; DO NOT upload.

## 11. VOICE/CRAFT (no AI feel) + RETENTION
- The script is written to first-rate, de-AI standard (em-dash 3.8/1k, varied openings). Do NOT rewrite it.
  Cold-open question (who was he / did he survive) is paid off across the acts and the ending; re-hooks each
  act; earned Like/comment ask (theory) in the CTA.

## 12. DEFINITION OF DONE (then STOP for owner)
- check_final_acceptance.py 21 + check_dynamics.py 21 + runtime band all exit 0; manual rows measured -> 0 violations.
- Self-audit report (each gate -> measured value). manifest state = edit_review (NOT published). Commit ONLY EP21's files.
- First-cut -> title/thumbnail -> pre-publish review -> scheduling = owner gates. PUBLISH is an owner gate.
- The full build prompt is episodes/_planning/codex_local_ep21_build.md.
