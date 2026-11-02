# CODEX HANDOFF — EP20 The Gardner Museum Heist (PD-2026-020-gardner)

> The single design document Codex reads to BUILD the episode. Claude owns the LEFT side
> (topic/research/claims/script) — done and LOCKED. Codex owns the RIGHT side
> (scenes -> images -> narration -> music -> motion -> edit -> render -> thumbnails).
> Build the FIRST render to satisfy the whole acceptance table. Numbers, not adjectives.

## 0. HARD CONSTRAINTS (do not cross)
- **R2 UNSOLVED case.** NEVER name or imply the guilt of any LIVING person. The FBI never publicly named
  the thieves; the men sometimes called the likely robbers were named by journalists, not the FBI. Use only
  "suspect / person of interest / investigated / theory / never charged with the theft." The night guard was
  investigated but never charged AND was himself a victim — never imply he was complicit.
- **No real-person likeness** anywhere. **No real museum interior/exterior, logo, or identifiable architecture**
  (build archetypal gallery imagery). **No authentic reproductions of the stolen artworks** — use empty gilded
  frames / draped canvases / silhouettes. Symbolic reconstruction only; nothing looks like authentic footage.
- "$500 million" is an ESTIMATE (works unsaleable; museum is "the only buyer"); never state as market value.
  "Largest" is an attributed characterization (FBI: largest property crime in U.S. history; museum: largest art heist).
- No publish, no external upload, no paid API without owner approval + idempotency + budget check.
- Render LOCAL CPU libx264, quality-first; NEVER NVENC. Heavy media -> H:\pd-media\episodes\PD-2026-020-gardner\.

## 1. BINDING SPEC + ACCEPTANCE
- Canonical spec: **docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md** (binding). Build to rows 1-16.
- "Done" = the independent gate exits 0 (not your opinion):
  ```
  ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 20 --json
  ```
- Duration profile: **mid, target 30:00** (runtime band 27-33; narration ~26-27 min).

## 2. LOCKED INPUTS (DO NOT REWRITE)
- Script: episodes/PD-2026-020-gardner/03_script/script.en.v001.md (~4,550 words; [VO:] only; "#" lines = production notes).
- Annotated: 03_script/script.annotated.v001.json (73 spans, claim_ids + visual_intent).
- Claims (R2 wording locks): 01_research/claims.v001.json (15 claims). Sources: 01_research/sources.v001.json (11).
- **R2 WORDING LOCKS (must hold in every caption / on-screen text / thumbnail):** unsolved; nothing recovered;
  never name/imply guilt of a living person; FBI never named the thieves; believed thieves named by journalists
  not FBI; $500M = estimate; "largest" attributed; "suspect/person of interest/never charged" hedges only.

## 3. STRUCTURE & TIMING
- Hook ~0:00-0:08 fast highlight montage -> Opening (the empty frames) -> Body (Act 1 The Night / Act 2 The
  Treasure / Act 3 The Hunt / Act 4 The Mystery) -> Ending, per the script timecodes.
- Gold BrandOpening lands AFTER the hook; BrandEndcard at tail. OP/ED canonical = remotion/src/components/Bookends.tsx
  (OPENING_SEC 3.5 / ENDCARD_SEC 9; do not fork). Drive EP20 through CasePremiumFromRoughCut (register in Root.tsx if needed).

## 4. VOICE (row 2)
- ElevenLabs master, VOICE_ID nPczCjzI2devNBz1zQrb, eleven_multilingual_v2, stability 0.35, similarity 0.80,
  style 0, speaker_boost on. Speak ONLY [VO:] lines; ignore "#" lines; strip [CLM-xxxx]. SAPI/local FORBIDDEN in final.

## 5. CAPTIONS (rows 3-4)
- Force-align to the rendered ElevenLabs audio (verbatim). 1 cue = 1 breath group. <=2 lines, <=42 chars/line,
  1.0-6.0s, <=17 cps, >=2-frame gaps, brand font, bottom-safe, drop-shadow, coverage >=95%.

## 6. MUSIC / BGM (row 1)
- Continuous library bed, one track per chapter (8-category set). Duck under VO to a FLOOR ~ -22 LUFS — the bed
  MUST stay audible under narration; never duck to silence. No silent stretch > 25s. Integrated -16..-12 LUFS.

## 7. IMAGES — Codex generation (row 5) — APPENDIX A
- **Generate every numbered MEGA-PROMPT in 04_scenes/codex_image_prompts.v001.md (EP20-IMG-###)** before edit;
  candidate counts as listed; that file's Hard Rules / Style Bible / Universal Negative / Quality Bar are binding.
- Output >= 3840 px long edge, 16:9; brand palette (black/navy + electric-blue #1F6BFF + gold #E5B53A + silver).
- Reject any still with a face/likeness, the real museum, any real artwork reproduction, real logo/landmark,
  readable text, or anatomy errors. Register every used still in the rights manifest (origin=Codex AI, AI-disclosed).

## 8. MOTION / EDIT (row 8) — fixes weak animation / stutter / boring stills
- NO static image; NO frame held > 2s; NO naked hard cut. Ken Burns >= 6% / parallax on every still; hero beats
  get SVD/organic motion + ink/particle overlays. Designed transitions 0.3-0.5s crossfade; OVERLAP Sequences by
  the transition length (no 1-frame black/jump); carry motion through the cut (no velocity reset = the "kaku");
  Trail motion blur on fast moves. Fast pace: average shot <= ~6s.
- Abundant material (row 7): factory shelf densely — >= 1 distinct clip per ~30s; every span >= 1 layer; no clip
  reused > 3x. scripts/select_factory_assets.py --theme crime/legal/art/finance (use what fits a heist mystery).

## 9. DEDICATED SUBSCRIBE+LIKE CTA (~29:10-29:35)
- Build exactly to the "# [PRODUCTION - DEDICATED CTA BEAT ...]" note in the script (gold SUBSCRIBE pill spring
  d14/s120 0.45s; gold underline wipe Easing.out(cubic) 0.5s; white LIKE thumb pop spring d10/s140, FILLS gold on
  the word "like" with 6% pulse + spark/Trail; navy vignette; hold ~5s; ease out 0.4s; soft click SFX; music dips
  ~3 dB but bed stays audible). NO real YouTube logo. PD brand styling.

## 10. THUMBNAILS (rows 11-13)
- >= 3 variants as Remotion <Still> at 1280x720, backgrounds pre-generated by Codex (same R2 rules: empty frame /
  fake-cop silhouette / night gallery — NO real museum, NO real artwork, NO face). "Loud": UPPERCASE headline
  <= 3-4 words, huge subject, very high contrast black/navy + gold #E5B53A or electric #1F6BFF, white/silver text,
  legible at 320px. Title <= 60 chars; A/B title x thumb. Headline ideas: "STILL MISSING" / "$500M GONE" /
  "THE EMPTY FRAMES". Pick a selected; DO NOT upload.

## 11. RETENTION / LIKE-RATE (row 16) — engineered in the script
- Cold-open (fake cops + still missing) is paid off in Act 4 / Ending; re-hooks every ~2-3 min; earned Like ask in
  the CTA. Keep the edit tight so retention stays flat-to-rising.

## 12. DEFINITION OF DONE (then STOP for owner)
- check_final_acceptance.py 20 exits 0; rows 4,5,7,8,11,12,13,15,16 measured -> 0 violations.
- First-cut -> title/thumbnail -> pre-publish review -> scheduling = owner gates, in order. Final-script approval
  APR-0001 is currently PENDING. Before publish, confirm living/deceased status of any person of interest and lock
  verbatim FBI/DOJ quotes. Do not treat the script as owner-approved until APR-0001 flips.
