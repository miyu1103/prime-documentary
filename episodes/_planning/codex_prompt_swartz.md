# CODEX HANDOFF — EP23 "The Internet's Own Boy" / Aaron Swartz (PD-2026-023-swartz)

> The single design document Codex reads to BUILD the episode. Claude owns the LEFT side
> (topic/research/claims/script) — done and LOCKED. Codex owns the RIGHT side
> (scenes -> images -> narration -> music -> motion -> edit -> render -> thumbnails).
> Build the FIRST render to satisfy the whole acceptance table. Numbers, not adjectives.

## 0. HARD CONSTRAINTS (do not cross)
- **R3 + SENSITIVE — death by suicide.** SAFE-HANDLING IS ABSOLUTE:
  - The death is stated in narration ONCE, with the locked wording ("died by suicide on January 11, 2013, at
    age 26"). NEVER add it anywhere else. NEVER "committed suicide." NO method, NO location, NO note, NO scene,
    NO reenactment in audio, caption, image, thumbnail, or metadata.
  - **NO single-cause narrative.** Do NOT state, in any caption / on-screen text / thumbnail / description, that
    the prosecution (or MIT, or any person) "caused" his death. Causation language belongs only to the family's
    attributed statement, exactly as written in the script. Foreground systemic issues, not one villain.
  - The **988 Suicide & Crisis Lifeline — call or text 988** lower-third appears on-screen at the marked beats
    and in the description (localize per region). The CTA is QUIET and respectful — this episode ends on a death.
- **No real-person likeness** anywhere — above all no likeness of Aaron Swartz, and none of any prosecutor,
  judge, official, or family member. People are anonymous (behind/cropped/silhouette/hands).
- **No real logos/seals/buildings** (Reddit, MIT, JSTOR, Creative Commons, YouTube, Wikipedia, DOJ/court seals,
  real Capitol/courthouse/MIT campus). Build archetypal equivalents. **No readable text** baked into any image.
- **No self-harm/death imagery** of any kind in any still or thumbnail (see 04_scenes §0). Symbolic only.
- WORDING LOCKS (must hold in every caption / on-screen text / thumbnail): co-authored RSS 1.0 as a teenager
  (NOT invented RSS); KEY COLLABORATOR on Markdown (NOT co-created); helped build the technical layer of
  Creative Commons (NOT founded); Reddit CO-OWNER via the Infogami merger (co-founder DISPUTED); he was CHARGED,
  never tried or convicted; JSTOR settled CIVILLY and did NOT want charges; MIT "neutral"; Carmen Ortiz's
  "Stealing is stealing..." is the prosecution's ATTRIBUTED position; "Aaron's Law" was proposed and NEVER
  passed; the CFAA was not meaningfully reformed.
- **THE "35 YEARS":** never show it unqualified. It is the THEORETICAL stacked statutory maximum, always paired
  on-screen and in narration with the ~6-month plea signal (per attorney Elliot Peters) and the scholarly
  critique (Orin Kerr) that the maximum wildly overstates realistic exposure.
- No publish, no external upload, no paid API beyond the narration cap without owner approval + idempotency +
  budget check. Render LOCAL CPU libx264, quality-first; NEVER NVENC. Heavy media ->
  H:\pd-media\episodes\PD-2026-023-swartz\ .

## 1. BINDING SPEC + ACCEPTANCE
- Canonical spec: **docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md** (binding). Build to rows 1-16.
- "Done" = the independent gate exits 0 (not your opinion):
  ```
  ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 23 --json
  ```
- Duration profile: **mid, target ~30:00** (runtime band 27-33; narration ~28-29 min at the ElevenLabs pace).

## 2. LOCKED INPUTS (DO NOT REWRITE)
- Script: episodes/PD-2026-023-swartz/03_script/script.en.v001.md (~4,889 words; [VO:] only; "#" lines = production notes).
- Annotated: 03_script/script.annotated.v001.json (49 spans, 7 chapters, claim_ids + visual_intent).
- Claims (R3 wording + safe-handling locks): 01_research/claims.v001.json (18 claims). Sources: 01_research/sources.v001.json (14).
- Image library: 04_scenes/codex_image_prompts.v001.md (54 MEGA-PROMPTS; its Hard Rules / Style Bible /
  Universal Negative / Quality Bar are binding).

## 3. STRUCTURE & TIMING
- Hook ~0:00-0:08 fast symbolic flash-forward (EP23-IMG-001..006, ~1.3s cuts) -> rest of hook (the question) ->
  Opening (the gap, thesis + promise + the 988 content note) -> Body (Act 1 The Builder / Act 2 The Activist /
  Act 3 The Download / Act 4 The Weight) -> Ending (The Open Door) + the dedicated quiet Subscribe+Like CTA,
  per the script timecodes.
- Gold BrandOpening lands AFTER the hook (not frame 0); BrandEndcard at tail. OP/ED canonical =
  remotion/src/components/Bookends.tsx (OPENING_SEC 3.5 / ENDCARD_SEC 9; do NOT fork). Drive EP23 through
  CasePremiumFromRoughCut (register in Root.tsx if needed). The final endcard holds the 988 line + "In memory of
  Aaron Swartz, 1986-2013."

## 4. VOICE (row 2)
- ElevenLabs master, VOICE_ID nPczCjzI2devNBz1zQrb, eleven_multilingual_v2, stability 0.35, similarity 0.80,
  style 0, speaker_boost on. Speak ONLY [VO:] lines; ignore "#" lines; strip [CLM-xxxx]. SAPI/local FORBIDDEN in
  the final. Deliver the death line and the ending unhurried and gentle; do not dramatize.

## 5. CAPTIONS (rows 3-4)
- Force-align to the rendered ElevenLabs audio (verbatim). 1 cue = 1 breath group. <=2 lines, <=42 chars/line,
  1.0-6.0s, <=17 cps, >=2-frame gaps, brand font, bottom-safe (lower 10-15%, never centered/high), drop-shadow,
  coverage >=95%. The 988 lower-third must never be occluded by a caption at the marked beats.

## 6. MUSIC / BGM (row 1)
- Continuous library bed, one track per chapter. Duck under VO to an AUDIBLE FLOOR ~ -22 LUFS — the bed MUST
  stay audible under narration; never duck to silence. No silent stretch > 25s. Integrated -16..-12 LUFS. The
  ending track is restrained and warm, not maudlin; lift gently into the "and yet" hope beat (IMG-051..053).

## 7. IMAGES — Codex generation (row 5) — see 04_scenes/codex_image_prompts.v001.md
- **Generate every numbered MEGA-PROMPT (EP23-IMG-001..054), exactly ONE image per prompt** (NO candidate pool);
  regenerate only a specific shot that fails §0/§3. Output >= 3840 px long edge, 16:9; brand palette
  (black/navy + electric-blue #1F6BFF + gold #E5B53A + silver).
- Reject any still with a face/likeness, ANY self-harm/death imagery, a real logo/seal/building, readable text,
  or anatomy errors. Register every used still in the rights manifest (origin=Codex AI, AI-disclosed).

## 8. MOTION / EDIT (row 8) — fixes weak animation / stutter / boring stills
- NO static image; NO frame held > 2s; NO naked hard cut. Ken Burns >= 6% / parallax on EVERY still; hero beats
  get SVD/organic motion + light/particle overlays (the feeds-of-light and locked-vs-open-archive motifs).
  Designed transitions 0.3-0.5s crossfade; OVERLAP Sequences by the transition length (no 1-frame black/jump);
  carry motion through the cut (no velocity reset = the "kaku"); Trail motion blur on fast moves (hook montage,
  the download streams). Average shot <= ~6s, but let the ending breathe (slower, longer holds, still <=2s freeze
  rule via slow continuous Ken Burns).
- Abundant material (row 7): factory shelf densely — >= 1 distinct clip per ~30s; every span >= 1 layer; no clip
  reused > 3x. scripts/select_factory_assets.py --theme tech/legal/crime/finance (use what fits a justice/tech
  elegy: servers, courtrooms-generic, libraries, code-abstract, city-night).

## 9. DEDICATED SUBSCRIBE+LIKE CTA (~29:20-29:50) — QUIET (ends on a death)
- Build exactly to the "# [PRODUCTION - DEDICATED SUBSCRIBE+LIKE CTA BEAT ...]" note in the script: gold
  SUBSCRIBE pill spring d14/s120 0.45s; gold underline wipe under "remembered" Easing.out(cubic) 0.5s; white
  LIKE thumb pop spring d10/s140, FILLS gold on the word "like" with a gentle 6% pulse + soft spark/Trail; soft
  navy vignette; hold ~5s; ease out 0.4s; very soft click SFX; music dips ~3 dB but the bed stays audible. NO
  real YouTube logo. Keep it understated and warm. Keep the 988 line present in the description card.

## 10. THUMBNAILS (rows 11-13) — loud but NEVER morbid or exploitative
- >= 3 variants as Remotion <Still> at 1280x720, backgrounds from the image library (locked vs open archive /
  open door / feeds-of-light — NO face, NO real logo/seal/building, NO self-harm/death imagery, NO readable
  baked text). "Loud" via contrast and a short UPPERCASE headline <= 3-4 words, gold #E5B53A or electric #1F6BFF
  accent, white/silver text, legible at 320px. Title <= 60 chars; A/B title x thumb. Headline ideas (respectful):
  "WHO OWNS KNOWLEDGE?" / "13 FELONIES" / "THE OPEN DOOR" / "HE TRIED TO FREE IT". AVOID anything that sensationalizes
  the death. Pick a selected; DO NOT upload.

## 11. RETENTION / LIKE-RATE (row 16) — engineered in the script
- Cold-open question ("who owns knowledge?" / "both true at once") is paid off in the Ending (the open door /
  "all of us"). Re-hooks ~every 2-3 min (the builder montage, the SOPA win, the closet, the "was this
  proportional?" turn). Earned, quiet Like ask in the CTA ("more people should sit with what happened"). Keep
  the edit tight so retention stays flat-to-rising; let only the ending slow down.

## 12. DEFINITION OF DONE (then STOP for owner)
- check_final_acceptance.py 23 exits 0; rows 4,5,7,8,11,12,13,15,16 measured -> 0 violations; check_dynamics.py
  and check_runtime_band.py on the render exit 0.
- First-cut -> title/thumbnail -> pre-publish review -> scheduling = owner gates, in order. Final-script approval
  APR-0001 is currently PENDING. Before publish, complete the DEDICATED R3 legal/rights + safe-handling review,
  compute durable source content_hash, re-verify facts, and confirm the safe-handling and 35-years locks hold in
  the rendered file. Do NOT treat the script as owner-approved until APR-0001 flips.
