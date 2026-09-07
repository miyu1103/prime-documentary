TASK: Build Prime Documentary EP19 (Operation Varsity Blues) into a FINISHED, GATE-ACCEPTED final video,
fully autonomously. Run the entire right-process to completion WITHOUT pausing for approval. Stop ONLY when
the independent acceptance gate passes (accepted final.mp4 + thumbnails), or at a genuine blocker you cannot
fix after real attempts. The images are already generated — assemble the film.

REPO: C:\Users\aab15\Documents\prime-documentary
EPISODE: PD-2026-019-varsityblues   |   PROFILE: mid, target 30:00 (runtime band 27-33)   |   RISK: R3

==================================================================================================
THE ONE RULE (this is how we stop the endless rework — read it twice)
==================================================================================================
"Done" is NOT your opinion. "Done" = this command exits 0 with every gate satisfied:
    ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 19 --json
You MUST run it, read the JSON, and if ANY gate fails or warns, FIX the cause and RUN IT AGAIN.
Loop build -> measure -> fix -> re-measure until it exits 0. Do NOT ask me for approval between loops.
Do NOT declare success until the real file passes. Self-reported "looks good" is rejected.
If the script can't measure a row that the spec lists as manual, measure it yourself against the stated
number and record the measurement — never skip a row silently.

==================================================================================================
SOURCES OF TRUTH — obey exactly, numbers not adjectives (do not improvise, do not reinterpret)
==================================================================================================
1. episodes/_planning/codex_prompt_ep19.md            <- the master design doc. Build to all of it.
2. docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md             <- binding acceptance table, rows 1-16.
3. episodes/PD-2026-019-varsityblues/03_script/script.en.v001.md       <- narration ([VO:] only) + the
   "# [PRODUCTION ...]" notes (build them to the number). LOCKED — do not rewrite a single word.
4. .../03_script/script.annotated.v001.json           <- 77 spans, each with claim_ids + visual_intent.
5. .../01_research/claims.v001.json                   <- R3 wording locks (below). Never contradict.
6. .../04_scenes/codex_image_prompts.v001.md          <- the 92 hero stills you already generated.
If any two sources ever seem to conflict, the spec v2 table wins; then the master design doc; then ask
NOTHING — pick the stricter reading and note it in the final report.

ALREADY DONE (inputs): the 92 hero stills (EP19-IMG-001..092) at
    H:\pd-media\episodes\PD-2026-019-varsityblues\05_visuals\selected\EP19-IMG-###.png
Use them. If a needed beat has no still, prefer a factory b-roll clip; only generate a new still if truly missing.

==================================================================================================
PIPELINE (run in order; every step has an exact spec — hit the number)
==================================================================================================
A. NARRATION (row 2) — PAID, do exactly once:
   - ElevenLabs master. VOICE_ID = nPczCjzI2devNBz1zQrb, model eleven_multilingual_v2, stability 0.35,
     similarity_boost 0.80, style 0, speaker_boost on.
   - Speak ONLY the [VO:] lines, in order. Ignore lines starting with "#" and strip every "[CLM-xxxx]" tag.
   - Use an idempotency key per chunk; if a chunk already exists on disk, DO NOT regenerate it (no double billing).
   - HARD BUDGET CAP: $25 total for this episode's narration. If you would exceed it, STOP and report.
   - SAPI/Windows/local TTS is FORBIDDEN in the final. (EP14 shipped SAPI — never again.)
B. CAPTIONS (rows 3-4): force-align to the RENDERED ElevenLabs audio (verbatim, not pasted from script).
   1 cue = 1 breath group (split at the narrator's actual breaths). <=2 lines, <=42 chars/line, 1.0-6.0s,
   <=17 cps, >=2-frame gaps. Burned-in brand font, bottom-safe, drop-shadow. Coverage >=95% of runtime.
C. MUSIC/BGM (row 1): continuous library bed (Suno reuse), one track per chapter (8-category set). Duck
   under VO to a FLOOR of ~ -22 LUFS — the bed MUST stay audible under narration; NEVER duck to silence.
   No silent stretch > 25s. Final integrated loudness -16..-12 LUFS. (Fixes "BGM not audible".)
D. MOTION/EDIT (row 8) — fixes weak animation / stutter / boring stills:
   - NO static image ever; NO frame held > 2s; NO naked hard cut.
   - Every still: Ken Burns >= 6% zoom or parallax; hero beats get SVD/organic motion + ink/particle overlays.
   - Transitions are DESIGNED: 0.3-0.5s crossfade/dissolve; OVERLAP Sequences by the transition length so
     there is no 1-frame black or jump; carry motion direction THROUGH the cut (no velocity reset = the
     "kaku" stutter); Trail motion blur on fast moves.
   - Fast pace: average shot <= ~6s; the picture is always changing.
E. ABUNDANT MATERIAL (row 7): use the factory shelf densely — >= 1 distinct factory clip per ~30s as the
   establish/"breath" layer; every span carries >= 1 layer; no single clip reused > 3x. Tool:
   scripts/select_factory_assets.py --theme school/legal/crime/finance .
F. STRUCTURE/OP-ED (rows 9-10): Hook ~0:08 fast highlight montage (EP19-IMG-001..006, ~2s cuts) ->
   Opening -> Body (Act 1-4) -> Ending, per the script timecodes. Gold BrandOpening lands AFTER the hook
   (not frame 0); BrandEndcard at tail. OP/ED canonical = remotion/src/components/Bookends.tsx
   (OPENING_SEC 3.5 / ENDCARD_SEC 9; DO NOT fork). Register the generic template
   CasePremiumFromRoughCut in remotion/src/Root.tsx if not already registered, and drive EP19 through it.
G. CTA BEAT (~29:10-29:35): build the dedicated Subscribe+Like animation EXACTLY to the
   "# [PRODUCTION - DEDICATED CTA BEAT ...]" note in the script (gold SUBSCRIBE pill spring d14/s120 0.45s;
   gold underline wipe Easing.out(cubic) 0.5s; white LIKE thumb pop spring d10/s140, FILLS gold on the word
   "like" with 6% pulse + particle spark/Trail; navy vignette; hold ~5s; ease out 0.4s; soft click SFX on
   fill; music dips ~3 dB but bed stays audible). NO real YouTube logo. PD brand styling.
H. RENDER (row 6): driven by remotion.config.ts canonical values (png intermediate / libx264 -preset slow
   -crf 16 / yuv420p / bt709 / aac 320k / all cores / GPU angle). 1920x1080 (4K master if source allows).
   NEVER NVENC. Per-chapter render -> concat. Output to H:\pd-media\episodes\PD-2026-019-varsityblues\08_edit\ .
I. THUMBNAILS (rows 11-13): render >= 3 variants as Remotion <Still> at 1280x720, backgrounds from the
   thumb prompts / image library (same R3 rules). "Loud": UPPERCASE headline <= 3-4 words, huge subject,
   very high contrast black/navy + gold #E5B53A or electric #1F6BFF accent, white/silver text, legible at
   320px. Title <= 60 chars; produce A/B title x thumb. Headline ideas: "THE SIDE DOOR" / "BOUGHT, NOT
   EARNED" / "$25M TO GET IN". Pick a selected; DO NOT upload it.

==================================================================================================
R3 WORDING LOCKS — must hold in EVERY caption / on-screen text / thumbnail (legal)
==================================================================================================
- "pleaded guilty", never "convicted at trial". Loughlin & Giannulli: fraud conspiracy ONLY — NEVER
  "convicted of money laundering / bribery" (dismissed). Singer: 3 charged -> 4 pleaded. Counts
  date-qualified (50 at unsealing vs 55 charged / 53 convicted total). Universities = VICTIMS, not
  defendants. Do not impute a child's knowledge. NO real-person likeness, no real logos/crests/landmarks.

==================================================================================================
HARD GATES — the run is not finished until ALL pass (measured on the real file)
==================================================================================================
Run: ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 19 --json   -> must exit 0.
Also confirm with your own measurement, and FIX + re-run on any miss:
 [ ] runtime in band 27-33 min (also scripts/check_runtime_band.py on the render)
 [ ] narration provider contains "eleven" (never sapi/local)            [ ] captions coverage >=95%, breath-group, <=17cps, 0 format violations
 [ ] BGM present, no silent stretch >25s, audible floor under VO         [ ] loudness -16..-12 LUFS
 [ ] motion: 0 static spans, 0 freeze >2s, transitions present (no naked hard cut)
 [ ] images all long-edge >=3840, 0 face/logo/landmark/text violations   [ ] factory density >= runtime/30s
 [ ] structure: hook(~8s)/opening/body/ending present + CTA in last 30s   [ ] OP after hook, ED at tail
 [ ] >=3 thumbnails @1280x720 + selected                                 [ ] 0 black frames

==================================================================================================
DO NOT (hard stops)
==================================================================================================
- Do NOT upload, publish, set a thumbnail live, or change privacy/visibility. Build to a finished file and STOP.
- Do NOT run the R3 legal/rights review yourself or mark it done — that + publish remain owner gates.
- Do NOT use NVENC. Do NOT overwrite any already-published mp4. Do NOT exceed the $25 narration cap.
- Do NOT rewrite the script/claims, invent facts, or contradict the R3 wording locks. Do NOT use any
  real-person face/likeness, real university logo/crest/mascot, or real landmark.

==================================================================================================
WHEN THE GATE PASSES — finish like this, then STOP
==================================================================================================
- Leave: the accepted final.mp4 (H:\...\08_edit\), captions .srt, >=3 thumbnails @1280x720 (selected marked),
  and a render/QC log. Register every used asset in the rights manifest (origin, license, AI-disclosure).
- Write a short ACCEPTANCE REPORT mapping EACH gate above -> the measured value (e.g. "runtime 30.2 min OK",
  "loudness -13.4 LUFS OK", "captions 98% coverage OK"). This report is the proof of done.
- Update manifest.json state to edit_review (NOT published), append events, commit ONLY EP19's own files.
- Then STOP and tell me it's ready for the owner gate (R3 legal review + title/thumbnail + publish).
Remember: keep looping build->measure->fix until check_final_acceptance.py 19 exits 0. Do not hand me a
"first cut for review" — hand me a file that already passes every gate.
