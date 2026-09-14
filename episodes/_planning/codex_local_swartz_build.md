TASK: Build Prime Documentary EP23 ("The Internet's Own Boy" / Aaron Swartz) into a FINISHED, GATE-ACCEPTED
final video, fully autonomously. Run the entire right-process to completion WITHOUT pausing for approval. Stop
ONLY when the independent acceptance gate passes (accepted final.mp4 + thumbnails), or at a genuine blocker you
cannot fix after real attempts.

REPO: C:\Users\aab15\Documents\prime-documentary
EPISODE: PD-2026-023-swartz  |  PROFILE: mid, target ~30:00 (runtime band 27-33)  |  RISK: R3 + SENSITIVE (death by suicide)

==================================================================================================
THE ONE RULE (this is how we stop the endless rework — read it twice)
==================================================================================================
"Done" is NOT your opinion. "Done" = this command exits 0 with every gate satisfied:
    ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 23 --json
You MUST run it, read the JSON, and if ANY gate fails or warns, FIX the cause and RUN IT AGAIN.
Loop build -> measure -> fix -> re-measure until it exits 0. Do NOT ask for approval between loops.
Do NOT declare success until the real file passes. Self-reported "looks good" is rejected.

==================================================================================================
SENSITIVE-TOPIC GUARDRAILS (R3 + suicide) — these override everything; a violation = STOP, do not ship
==================================================================================================
- The death is in the narration ONCE, with the locked wording. It must NOT appear anywhere else — not in a
  caption beyond that one aligned cue, not in an image, not in a thumbnail, not in the title/description.
- NEVER "committed suicide". NO method, location, note, scene, or reenactment, in any modality.
- NO single-cause narrative: no caption/on-screen text/thumbnail/metadata may state that the prosecution, MIT,
  or any person "caused" his death. That causation lives ONLY in the family's attributed statement in the script.
- The "988 Suicide & Crisis Lifeline — call or text 988" lower-third renders at the marked beats and goes in the
  description (localize per region). The CTA stays quiet and respectful.
- No real-person likeness (especially not Aaron Swartz). No self-harm/death imagery in any still or thumbnail.
- THE "35 YEARS" never appears unqualified (theoretical stacked maximum + ~6-month plea + Kerr critique, together).
If you catch yourself about to break any of these, STOP that path and do it the safe way.

==================================================================================================
PRE-FLIGHT (do this BEFORE building anything; if a check fails, STOP and report — do not improvise)
==================================================================================================
[ ] script + annotated exist and are LOCKED: episodes/PD-2026-023-swartz/03_script/script.en.v001.md and
    script.annotated.v001.json (49 spans). Do NOT rewrite a single word.
[ ] validate_episode.py 23 prints RESULT: PASS (it does now). If it does not, STOP.
[ ] all 54 stills generated: H:\pd-media\episodes\PD-2026-023-swartz\05_visuals\selected\EP23-IMG-001.png …
    EP23-IMG-054.png . If any are missing, list which and STOP (do not substitute random images).
[ ] ElevenLabs API key present and reachable (narration required; see step A).
[ ] remotion.config.ts has canonical values (png / libx264 -crf 16 / yuv420p / bt709 / aac 320k / all cores /
    angle). If not, fix that ONE file first.
[ ] OP/ED component exists: remotion/src/components/Bookends.tsx (do NOT fork it).
[ ] check_final_acceptance.py runs for episode 23 (even if it fails — confirm it executes).

==================================================================================================
SOURCES OF TRUTH — obey exactly, numbers not adjectives (do not improvise, do not reinterpret)
==================================================================================================
1. episodes/_planning/codex_prompt_swartz.md           <- master design doc. Build to all of it.
2. docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md              <- binding acceptance table, rows 1-16.
3. episodes/PD-2026-023-swartz/03_script/script.en.v001.md   <- narration ([VO:] only) + "# [PRODUCTION ...]" notes. LOCKED.
4. .../03_script/script.annotated.v001.json            <- 49 spans, claim_ids + visual_intent.
5. .../01_research/claims.v001.json                    <- 18 R3 + safe-handling wording locks. Never contradict.
6. .../04_scenes/codex_image_prompts.v001.md           <- the 54 stills to generate (one image each).
If two sources seem to conflict: spec v2 wins, then the master design doc; then pick the stricter / safer reading
and note it in the final report. Ask NOTHING.

==================================================================================================
PIPELINE (run in order; every step has an exact spec — hit the number)
==================================================================================================
A. NARRATION (row 2) — PAID, do exactly once:
   - ElevenLabs master. VOICE_ID = nPczCjzI2devNBz1zQrb, model eleven_multilingual_v2, stability 0.35,
     similarity_boost 0.80, style 0, speaker_boost on. Speak ONLY [VO:] lines, in order; ignore "#" lines; strip
     every "[CLM-xxxx]" tag. Deliver the death line and the ending gently and unhurried.
   - Idempotency key per chunk; if a chunk already exists on disk, DO NOT regenerate it (no double billing).
   - HARD BUDGET CAP: $25 total for this episode's narration. If you would exceed it, STOP and report.
   - SAPI/Windows/local TTS is FORBIDDEN in the final.
B. CAPTIONS (rows 3-4): force-align to the RENDERED ElevenLabs audio (verbatim, not pasted from script). 1 cue =
   1 breath group. <=2 lines, <=42 chars/line, 1.0-6.0s, <=17 cps, >=2-frame gaps. Burned-in brand font,
   bottom-safe (lower 10-15%, never centered/high), drop-shadow. Coverage >=95%. Do not let a caption occlude the
   988 lower-third at the marked beats.
C. MUSIC/BGM (row 1): continuous library bed, one track per chapter. Duck under VO to an AUDIBLE FLOOR ~ -22 LUFS;
   NEVER duck to silence. No silent stretch > 25s. Final integrated -16..-12 LUFS. Ending track restrained/warm.
D. MOTION/EDIT (row 8): NO static image; NO frame held > 2s; NO naked hard cut. Every still: Ken Burns >= 6% or
   parallax; hero beats get SVD/organic motion + light/particle overlays. Designed 0.3-0.5s crossfades; OVERLAP
   Sequences by the transition length (no 1-frame black/jump); carry motion through the cut (no "kaku"); Trail
   blur on fast moves. Average shot <= ~6s; let the ending breathe with slow continuous moves (no hard freeze).
E. ABUNDANT MATERIAL (row 7): factory shelf densely — >= 1 distinct factory clip per ~30s; every span >= 1 layer;
   no clip reused > 3x. scripts/select_factory_assets.py --theme tech/legal/crime/finance .
F. STRUCTURE/OP-ED (rows 9-10): Hook ~0:08 fast montage (EP23-IMG-001..006) -> hook question -> Opening (the gap
   + 988 content note) -> Body (Act 1 Builder / Act 2 Activist / Act 3 The Download / Act 4 The Weight) ->
   Ending (The Open Door) per the script timecodes. Gold BrandOpening AFTER the hook; BrandEndcard at tail; OP/ED
   = Bookends.tsx (OPENING_SEC 3.5 / ENDCARD_SEC 9; DO NOT fork). Final endcard holds the 988 line + "In memory of
   Aaron Swartz, 1986-2013." Register CasePremiumFromRoughCut in Root.tsx if needed and drive EP23 through it.
G. CTA BEAT (~29:20-29:50): build the dedicated QUIET Subscribe+Like animation EXACTLY to the
   "# [PRODUCTION - DEDICATED SUBSCRIBE+LIKE CTA BEAT ...]" note (gold SUBSCRIBE pill spring d14/s120 0.45s; gold
   underline wipe Easing.out(cubic) 0.5s; white LIKE thumb pop spring d10/s140, FILLS gold on the word "like" with
   a gentle 6% pulse + soft spark/Trail; soft navy vignette; hold ~5s; ease out 0.4s; very soft click SFX; music
   dips ~3 dB but bed stays audible). NO real YouTube logo. Keep it understated.
H. RENDER (row 6): driven by remotion.config.ts canonical values (png intermediate / libx264 -preset slow -crf 16
   / yuv420p / bt709 / aac 320k / all cores / GPU angle). 1920x1080 (4K master if source allows). NEVER NVENC.
   Per-chapter render -> concat. Output to H:\pd-media\episodes\PD-2026-023-swartz\08_edit\ .
I. THUMBNAILS (rows 11-13): render >= 3 variants as Remotion <Still> at 1280x720, backgrounds from the image
   library (locked-vs-open archive / open door / feeds-of-light — NO face, NO real logo/seal/building, NO
   self-harm/death imagery, NO readable baked text). UPPERCASE headline <= 3-4 words, high contrast, gold #E5B53A
   or electric #1F6BFF accent, legible at 320px. Respectful headlines only ("WHO OWNS KNOWLEDGE?" / "13 FELONIES" /
   "THE OPEN DOOR"). Title <= 60 chars; A/B title x thumb. Pick a selected; DO NOT upload.

==================================================================================================
HARD GATES — the run is not finished until ALL pass (measured on the real file)
==================================================================================================
Run: ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 23 --json   -> must exit 0. Also confirm with
your own measurement and FIX + re-run on any miss:
 [ ] runtime in band 27-33 min (scripts/check_runtime_band.py on the render)
 [ ] narration provider contains "eleven" (never sapi/local)
 [ ] captions coverage >=95%, breath-group, <=17cps, 0 format violations, bottom-safe
 [ ] BGM present, no silent stretch >25s, audible floor under VO, integrated -16..-12 LUFS
 [ ] motion (check_dynamics.py): 0 static spans, 0 freeze >2s, transitions present (no naked hard cut)
 [ ] images all long-edge >=3840, 0 face/likeness / 0 self-harm-death / 0 real-logo-seal-building / 0 text violations
 [ ] factory density >= runtime/30s
 [ ] structure: hook(~8s)/opening/body/ending present + quiet CTA in last ~40s
 [ ] OP after hook, ED at tail (988 + dedication on endcard)
 [ ] >=3 thumbnails @1280x720 + selected (no morbid/sensational thumbnail)
 [ ] 0 black frames
 [ ] SAFE-HANDLING self-check: death stated once; no method/location/note/scene anywhere; no single-cause claim
     in any caption/on-screen/thumbnail/metadata; "35 years" never unqualified; 988 present on-screen + description

==================================================================================================
DO NOT (hard stops)
==================================================================================================
- Do NOT upload, publish, set a thumbnail live, or change privacy/visibility. Build to a finished file and STOP.
- Do NOT run the pre-publish review yourself or mark it done — that + publish remain owner gates (R3 legal +
  safe-handling review required first).
- Do NOT use NVENC. Do NOT exceed the $25 narration cap. Do NOT overwrite any already-published mp4.
- Do NOT rewrite the script/claims, invent facts, or break a wording/safe-handling/35-years lock. Do NOT use any
  real-person likeness or any self-harm/death imagery.

==================================================================================================
WHEN THE GATE PASSES — finish like this, then STOP
==================================================================================================
- Leave: the accepted final.mp4 (H:\...\08_edit\), captions .srt, >=3 thumbnails @1280x720 (selected marked), a
  render/QC log, and a SELF-AUDIT REPORT mapping EACH gate above -> the measured value (e.g. "runtime 30.4 min OK",
  "loudness -13.1 LUFS OK", "captions 97% OK", "0 face/self-harm/logo/text violations OK", "death stated once OK",
  "988 on-screen + in description OK"). Register every used asset in the rights manifest (origin, license,
  AI-disclosure, no-likeness).
- Update manifest.json state to edit_review (NOT published), append events, commit ONLY EP23's own files.
- Then STOP and tell me it's ready for the owner gate (DEDICATED R3 legal + safe-handling review, fact/quote
  recheck, durable source hashes, title/thumbnail, publish). Hand me a file that already passes every gate.
