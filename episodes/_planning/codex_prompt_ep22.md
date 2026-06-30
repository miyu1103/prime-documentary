# CODEX HANDOFF — EP22 Michael Milken: Genius, or the Face of Greed? (PD-2026-022-milken)

> The single design document Codex reads to BUILD the episode. Claude owns the LEFT side
> (topic/research/claims/script) — done and LOCKED. Codex owns the RIGHT side
> (scenes -> images -> narration -> music -> motion -> edit -> render -> thumbnails).
> Build the FIRST render to satisfy the whole acceptance table. Numbers, not adjectives.

## 0. HARD CONSTRAINTS (do not cross) — R3, LIVING + PARDONED
- **LIVING person who PLEADED GUILTY and was later PARDONED.** Strictly record-based and neutral.
  - NEVER say "convicted at trial", "convicted of insider trading", or "convicted of racketeering/RICO." He did
    NOT go to trial; there is no standalone insider-trading or RICO conviction.
  - ALWAYS distinguish **CHARGED** (98-count indictment, 1989, incl. RICO) from **PLEADED** (SIX felony counts,
    April 1990: securities/reporting, conspiracy, mail fraud, tax). Charges are accusations, not findings; the
    RICO charge and the other 92 counts were DROPPED.
  - The **2020 pardon is clemency, NOT innocence/exoneration**: the guilty plea STANDS and the pardon did NOT
    lift the SEC **lifetime industry ban**. (The White House line "pleaded guilty in 1989" is imprecise — the
    plea was April 1990; never repeat the 1989 date as the plea date.)
  - The **genius-vs-greed** debate is **ATTRIBUTED** ("critics argue / defenders argue") — never narrated as
    settled fact, in VO, captions, on-screen text, or thumbnails.
- **No real-person likeness** anywhere (not Milken, Boesky, any official/president/raider/supporter). **No real
  logos or seals** (Drexel/SEC/DOJ/White House/YouTube/presidential). **No readable text in images** (Remotion
  adds all text). **No real artwork/building interior/landmark.** Symbolic reconstruction only; nothing looks
  like authentic footage or an authentic record.
- "~$600 million" = **$200M fine + $400M restitution fund** (1990 criminal resolution); later civil settlements
  are separate — do not fold them in. Sentenced to 10 years, reduced; **served about 2 years**.
- No publish, no external upload, no paid API without owner approval + idempotency + budget check.
- Render LOCAL CPU libx264, quality-first; NEVER NVENC. Heavy media -> H:\pd-media\episodes\PD-2026-022-milken\.

## 1. BINDING SPEC + ACCEPTANCE
- Canonical spec: **docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md** (binding for EP19+). Build to rows 1-16.
- "Done" = the independent gate exits 0 (not your opinion):
  ```
  ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 22 --json
  ```
- Duration profile: **mid, target 30:00** (runtime band 27-33; narration ~24-26 min at the measured ~173 wpm,
  filled to runtime with the hook montage, OP/ED bookends, music beats, and the CTA hold).

## 2. LOCKED INPUTS (DO NOT REWRITE)
- Script: episodes/PD-2026-022-milken/03_script/script.en.v001.md (~4,223 words; [VO:] only; "#" lines = production notes).
- Annotated: 03_script/script.annotated.v001.json (71 spans, claim_ids + visual_intent).
- Claims (R3 wording locks): 01_research/claims.v001.json (13 claims). Sources: 01_research/sources.v001.json (11).
- **R3 WORDING LOCKS (must hold in every caption / on-screen text / thumbnail):** pleaded guilty (never convicted
  at trial); pleaded to SIX felonies (no insider-trading/RICO conviction); CHARGED (98) vs PLEADED (6), RICO + 92
  dropped; ~$600M = $200M fine + $400M restitution; SEC lifetime ban remains; 2020 pardon = clemency not innocence;
  genius-vs-greed attributed only.

## 3. STRUCTURE & TIMING (per the script timecodes)
- Hook ~0:00-0:08 fast highlight montage (EP22-IMG-001..006, ~2s cuts) -> Opening (The Two-Sided Man) ->
  Body (Act 1 The Idea / Act 2 The Empire / Act 3 The Fall / Act 4 The Reckoning & the Forgiveness) -> Ending
  (Your Verdict) + dedicated CTA beat.
- Gold BrandOpening lands AFTER the hook; BrandEndcard at tail. OP/ED canonical = remotion/src/components/Bookends.tsx
  (OPENING_SEC 3.5 / ENDCARD_SEC 9; DO NOT fork). Drive EP22 through CasePremiumFromRoughCut (register in Root.tsx if needed).

## 4. VOICE (row 2)
- ElevenLabs master, VOICE_ID nPczCjzI2devNBz1zQrb, eleven_multilingual_v2, stability 0.35, similarity 0.80,
  style 0, speaker_boost on. Speak ONLY [VO:] lines; ignore "#" lines; strip [CLM-xxxx]. SAPI/local FORBIDDEN in final.
- HARD BUDGET CAP for narration: $25. Idempotency key per chunk; never double-bill an existing chunk.

## 5. CAPTIONS (rows 3-4)
- Force-align to the rendered ElevenLabs audio (verbatim, NOT pasted from script). 1 cue = 1 breath group. <=2 lines,
  <=42 chars/line, 1.0-6.0s, <=17 cps, >=2-frame gaps, brand font, bottom-safe (lower 10-15%), drop-shadow, coverage >=95%.
- Captions must also honor the R3 locks (e.g. never let an auto-caption read "convicted"; verbatim from the VO, which is clean).

## 6. MUSIC / BGM (row 1)
- Continuous library bed, one track per chapter (8-category set). Duck under VO to a FLOOR ~ -22 LUFS — the bed
  MUST stay audible under narration; never duck to silence. No silent stretch > 25s. Integrated -16..-12 LUFS.

## 7. IMAGES — Codex generation (row 5) — see 04_scenes/codex_image_prompts.v001.md
- **Generate every numbered MEGA-PROMPT (EP22-IMG-001..074), exactly ONE image per prompt (74 total)** before edit;
  that file's Hard Rules / Style Bible / Universal Negative / Quality Bar are binding. Regenerate ONLY a failed shot.
- Output >= 3840 px long edge, 16:9; brand palette (black/midnight-navy + electric-blue #1F6BFF + gold #E5B53A + silver).
- Reject any still with a face/likeness, a real logo/seal, any readable text, a real artwork/landmark, or anatomy
  errors. Register every used still in the rights manifest (origin=Codex AI, AI-disclosed; no real-person likeness).

## 8. MOTION / EDIT (row 8) — fixes weak animation / stutter / boring stills
- NO static image; NO frame held > 2s; NO naked hard cut. Ken Burns >= 6% / parallax on every still; hero beats
  get SVD/organic motion + ink/particle overlays. Designed transitions 0.3-0.5s crossfade; OVERLAP Sequences by
  the transition length (no 1-frame black/jump); carry motion through the cut (no velocity reset = the "kaku");
  Trail motion blur on fast moves (hook montage, the tower of money, the indictment collapse). Average shot <= ~6s.
- Abundant material (row 7): factory shelf densely — >= 1 distinct clip per ~25-30s; every span >= 1 layer; factory
  layer across >=40% of the timeline; no clip reused > 3x. scripts/select_factory_assets.py --theme finance/legal/crime
  (trading floors, courthouses, money, vaults, 1980s textures, clinical/lab for Act 4).

## 9. DEDICATED SUBSCRIBE+LIKE CTA (~29:10–29:35)
- Build EXACTLY to the "# [PRODUCTION - DEDICATED CTA BEAT ...]" note in the script: gold SUBSCRIBE pill slides up
  from the lower third (spring damping 14 / stiffness 120, ~0.45s) + gold underline wipe (Easing.out(cubic), 0.5s);
  white outline thumbs-up LIKE icon pops in (spring damping 10 / stiffness 140) and, on the spoken word "like",
  FILLS solid gold with one 6% scale pulse + a soft particle spark (Trail motion blur); subtle navy vignette;
  hold ~5s; ease out 0.4s; one soft UI "click" SFX on the like-fill; music dips ~3 dB but the bed stays audible.
  NO real YouTube logo or real-person likeness; PD brand styling. Backdrop = EP22-IMG-074.

## 10. THUMBNAILS (rows 11-13)
- >= 3 variants as Remotion <Still> at 1280x720, backgrounds from the image library (split gold/blue figure /
  X-shaped desk / tower of money / pardon parchment beside the locked padlock — NO face, NO real logo/seal).
  "Loud": UPPERCASE headline <= 3-4 words, huge subject, very high contrast black/navy + gold #E5B53A or electric
  #1F6BFF accent, white/silver text, legible at 320px. Title <= 60 chars; A/B title x thumb.
- Headline ideas (all R3-safe; no "convicted"): "GENIUS OR GREED?" / "$550 MILLION. ONE YEAR." / "PARDONED, NOT
  CLEARED" / "98 CHARGES. 6 PLEAS." Pick a selected; DO NOT upload.

## 11. RETENTION / LIKE-RATE (row 16) — engineered in the script
- Cold-open question (genius or greed?) is paid off in the Ending and is the explicit Like/comment ask in the CTA;
  re-hooks every ~2-3 min (the $550M number, the "highly confident" letter, Boesky, the 98->6 collapse, the cancer
  turn, the pardon-vs-ban split). Keep the edit tight so retention stays flat-to-rising.

## 12. DEFINITION OF DONE (then STOP for owner)
- check_final_acceptance.py 22 exits 0; rows 4,5,7,8,11,12,13,15,16 measured -> 0 violations; check_dynamics.py and
  check_runtime_band.py on the render exit 0.
- First-cut -> title/thumbnail -> pre-publish review -> scheduling = owner gates, in order. Final-script approval
  APR-0001 is currently PENDING. **Before publish (R3): re-confirm the subject is living, and lock verbatim
  White House pardon-statement / court (indictment & plea) / SEC quotes on the live records.** Do not treat the
  script as owner-approved until APR-0001 flips. PUBLISH requires R-level legal review first.
