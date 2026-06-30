TASK: Build Prime Documentary EP24 "The Wiretap That Cracked Wall Street" (PD-2026-024-rajaratnam)
into a FINISHED, GATE-ACCEPTED final video, fully autonomously. Run the entire right-process to
completion WITHOUT pausing for approval. Stop ONLY when the independent acceptance gate exits 0
(accepted final.mp4 + >=3 thumbnails), or at a genuine blocker you cannot fix after real attempts.

REPO: C:\Users\aab15\Documents\prime-documentary   |   Python: ./.venv/Scripts/python.exe
EPISODE: PD-2026-024-rajaratnam   |   PROFILE: mid, target 30:00 (runtime band 27-33)   |   RISK: R2 (LIVING, CONVICTED at trial)
MEDIA (never commit): H:\pd-media\episodes\PD-2026-024-rajaratnam\

==================================================================================================
THE ONE RULE (this is how we stop endless rework — read it twice)
==================================================================================================
"Done" is NOT your opinion. "Done" = this command exits 0 with every gate satisfied:
    ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 24 --json
Run it, read the JSON, and if ANY gate fails or warns, FIX the cause and RUN IT AGAIN.
Loop build -> measure -> fix -> re-measure until exit 0. Do NOT ask for approval between loops.
A row the script lists as manual, you MUST measure yourself against the stated number and record it.

==================================================================================================
SOURCES OF TRUTH (obey exactly — numbers not adjectives; ask nothing)
==================================================================================================
1. episodes/_planning/codex_prompt_024_rajaratnam.md   <- MASTER DESIGN DOC. Build to ALL of it.
2. docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md              <- binding acceptance table, rows 1-16.
3. episodes/PD-2026-024-rajaratnam/03_script/script.en.v001.md          <- narration ([VO:] only). LOCKED. ~3,776 words.
4. .../03_script/script.annotated.v001.json            <- 53 spans (SPN-0001..SPN-0053), 6 chapters, claim_ids + visual_intent. annotated estimated 1510.4s (~25.2 min @150 wpm).
5. .../01_research/claims.v001.json                    <- 20 claims, R2 wording locks (Section 8 of the master doc). Never contradict.
6. .../04_scenes/codex_image_prompts.v001.md           <- per-scene image brief (the prompts you generate in Step 1).
7. .../manifest.json                                   <- state=script_verified, active_revisions all v001, APR-0001 PENDING.
If two sources conflict: spec v2 wins, then the master design doc, then the stricter reading; note it.

==================================================================================================
PRE-FLIGHT (do BEFORE building; if a check fails, STOP and report — do not improvise)
==================================================================================================
[ ] script + annotated exist and are LOCKED (53 spans). Do NOT rewrite a single word.
[ ] 04_scenes/codex_image_prompts.v001.md exists. If MISSING, STOP and report (it is the per-scene
    image brief keyed to the 53 spans' visual_intent; do not invent random images).
[ ] ElevenLabs API key present and reachable (narration is required; Step 2).
[ ] remotion.config.ts has canonical values: png intermediate / libx264 -preset slow -crf 16 /
    yuv420p / bt709 / aac 320k / all cores / GPU angle. If not, fix that ONE file first.
[ ] OP/ED component exists: remotion/src/components/Bookends.tsx (OPENING_SEC 3.5 / ENDCARD_SEC 9; do NOT fork).
[ ] check_final_acceptance.py runs for episode 24 (even if it fails — confirm it executes).
[ ] validate_episode.py 24 still PASS at script stage.
Only after all pass do you start the pipeline.

==================================================================================================
PIPELINE (run in order; each step has an exact spec — hit the number)
==================================================================================================

STEP 1 — IMAGES (Codex generation only; SDXL NOT used) — do FIRST, before edit
  - Generate EVERY numbered MEGA-PROMPT in 04_scenes/codex_image_prompts.v001.md: ONE masterpiece prompt
    per scene -> EXACTLY 1 image per prompt. Regenerate ONLY a still that violates a hard rule.
  - Output: 16:9, long edge >= 3840 px. Palette: black/midnight-navy + electric-blue #1F6BFF + gold
    #E5B53A + silver.
  - HARD (reject + regenerate): NO real-person likeness (invariant 11); NO real logos/seals/landmarks/
    company marks (no Galleon/Intel/McKinsey/IBM/Goldman/SEC/FBI/court seals/identifiable buildings);
    NO readable text in image (Remotion adds text); no anatomy errors; nothing looks like an authentic
    photo/evidentiary record.
  - WRITE stills to: H:\pd-media\episodes\PD-2026-024-rajaratnam\05_visuals\selected\ (one per span/shot id).
  - Register every used still in the rights manifest (origin=Codex AI, AI-disclosed).

STEP 2 — NARRATION (row 2) — PAID, do EXACTLY once
  - ElevenLabs master. VOICE_ID = nPczCjzI2devNBz1zQrb, model eleven_multilingual_v2, stability 0.35,
    similarity_boost 0.80, style 0, speaker_boost on.
  - Speak ONLY the [VO:] lines, in order (SPN-0001..SPN-0053). Ignore "#" lines; strip every [CLM-xxxx] tag.
  - Idempotency key per chunk; if a chunk exists on disk, DO NOT regenerate (no double billing).
  - HARD BUDGET CAP: $25 for this episode's narration. If you would exceed it, STOP and report.
  - SAPI / Windows / local TTS is FORBIDDEN in the final (EP14 shipped SAPI — never again).
  - WRITE: 06_audio/narration_index.v001.json + 06_audio/voice_master.v001.* on H:\...\06_audio\.

STEP 3 — CAPTIONS (rows 3-4) — force-align to the RENDERED audio (verbatim, NOT pasted from script)
  - 1 cue = 1 breath group (split at the narrator's actual breaths). <=2 lines, <=42 chars/line,
    1.0-6.0s, <=17 cps, >=2-frame gaps. Position lower 10-15% (bottom-safe), NEVER centered/high.
    Brand font, drop-shadow. Coverage >= 95% of runtime.
  - WRITE: 08_edit/captions.v001.srt + remotion/src/data/rajaratnam_captions.ts.

STEP 4 — MUSIC / BGM (row 1) — continuous library bed (Suno-origin assets, rights-tracked)
  - ONE track per chapter (6 cues): cold_open near-silence/single-reel texture -> M1 rising confident
    (the_edge, gold) -> M2 intimate w/ cold thread (the_whisper) -> M3 low patient mechanical pulse
    (the_wire) -> M4 spare building to one resolved chord at the verdict (the_reckoning) -> M5 = M1
    returned, quieter (coda).
  - Duck under VO to an AUDIBLE FLOOR ~ -22 LUFS (bed MUST stay audible; NEVER duck to silence).
    No silent stretch > 25s. Final integrated loudness -16..-12 LUFS.
  - WRITE mix: remotion/public/rajaratnam/audio/rajaratnam_final_mix_v001.wav (+hash);
    QC -> 08_edit/audio_mix.v001.qc.json.

STEP 5 — FACTORY B-ROLL (row 7) — the establish / "breath" layer
  - scripts/select_factory_assets.py --theme finance / legal / crime / tech / surveillance_tech
    (trading floors, cash/gold, servers/data/world map, courthouse, recording gear, city at night).
  - >= 1 distinct factory clip per ~25-30s; factory layer across >= 40% of timeline; every span carries
    >= 1 layer; no single clip reused > 3x. Record license/source/hash per clip.
  - WRITE to: remotion/public/rajaratnam/factory/.

STEP 6 — REMOTION ASSEMBLY (rows 8-10) — motion mandatory, NO static
  - Feed from remotion/src/data/rajaratnam_roughcut.ts (all 53 spans grouped by chapter_id, color per the
    register table in master doc Section 2) + rajaratnam_captions.ts (Step 3). Drive through the existing
    premium-from-roughcut composition; register in remotion/src/Root.tsx if needed (id distinct from
    other episodes — avoid name collision). fps per BRAND.video.fps; ~30 min duration.
  - MOTION: NO static image; NO frame held > 2s; NO naked hard cut. Every still gets Ken Burns >= 6% zoom
    or parallax (Parallax.tsx/Motion.tsx). >= 1 hero/organic (SVD/2.5D) motion shot per 60s on marquee
    beats (grey room, reel turning, waveform->ice EXHIBIT, gold node web, verdict). Designed transitions
    0.3-0.5s crossfade; OVERLAP Sequences by the transition length (no 1-frame black/jump); carry motion
    THROUGH the cut (no velocity reset = "kaku"); Trail motion blur (@remotion/motion-blur) on fast moves.
    Average shot <= ~6s. Factory = MovingVideo. Every span has a moving picture.
  - STRUCTURE: HOOK = first ~8s of SPN-0001 (grey room, thumb on PLAY), fast -> THEN gold BrandOpening
    (Bookends.tsx; AFTER the hook, not frame 0) -> Body Act1 THE EDGE / Act2 THE WHISPER NETWORK /
    Act3 THE WIRE / Act4 THE RECKONING -> Coda -> BrandEndcard at tail. Re-hook every ~2-3 min by cutting
    back to the reel/grey-room/waveform motif.
  - CTA BEAT ~29:10-29:35 on SPN-0053: dedicated Subscribe+Like animation, PD brand styling, gold
    SUBSCRIBE + white LIKE that fills gold on the word "like", spark/Trail, music dips ~3 dB but bed stays
    audible. NO real YouTube logo.

STEP 7 — THUMBNAILS (rows 11-13) — render >= 3 as Remotion <Still> at 1280x720
  - Backgrounds from Step 1 stills (recorder/reel / waveform-to-ice / gold node-web tower). Loud: UPPERCASE
    headline <= 3-4 words, huge subject, very high contrast black/navy + gold #E5B53A or electric #1F6BFF,
    white/silver text, legible at 320px. Title <= 60 chars; A/B title x thumb. NO face/real logo/landmark.
  - Three headline concepts: A "CAUGHT ON TAPE" / B "THE $7B WIRE" / C "HIS OWN VOICE".
  - Pick a selected; DO NOT upload it.

STEP 8 — RENDER (row 6; quality-first CPU libx264; NEVER NVENC)
  - Driven by remotion.config.ts canonical values (png / libx264 -preset slow -crf 16 / yuv420p / bt709 /
    aac 320k / all cores / GPU angle). 1920x1080. Per-chapter render -> FFmpeg concat.
  - OUTPUT: H:\pd-media\episodes\PD-2026-024-rajaratnam\08_edit\v001.mp4 (+sha in manifest). Resumable per chapter.

==================================================================================================
R2 WORDING LOCKS — must hold in EVERY caption / on-screen text / thumbnail (legal; master doc Section 8)
==================================================================================================
- Conviction/sentence = FACT (jury verdict May 11, 2011, guilty on ALL 14 counts = 5 conspiracy + 9
  securities fraud; sentenced Oct 13, 2011 to 11 years). He did NOT plead guilty; convicted at trial.
- Conduct framed "the jury found / prosecutors proved / the government said / argued" (CLM-0017/0018).
- Superlative attributed + time-bound: "at the time, prosecutors called it the longest insider-trading
  sentence in American history" — never flat/undated/permanent (CLM-0004).
- Profit hedged + anchored to forfeiture: on screen "$53.8 million" / "more than fifty million dollars".
  Keep SEC $92,805,705 civil penalty DISTINCT from the $53,816,434 forfeiture + $10M fine; combined
  >$156.6M presented as a SUM (CLM-0005/0006/0007/0012). Never an invented flat profit number.
- Wiretap "first" = "widely described as / per the FBI and prosecutors"; 2nd Circuit upheld 2013 (CLM-0008/0009).
- Rajat Gupta STRICTLY SEPARATE: different case/jury, convicted June 2012, 2 years + $5M fine; NEVER merge
  Gupta's conduct/penalties with Rajaratnam's (CLM-0011). Tippers (Goel/Intel, Kumar/McKinsey, Moffat/IBM,
  Chiesi/New Castle) charged SEPARATELY; never merge a tipper's outcome with Rajaratnam's (CLM-0010).
- Memoir "Uneven Justice" (~2021) grade C: VERIFY title/date before voicing; "he says, to be fair" only.
- Any verbatim wiretap dialogue MUST be verified against the public trial record before voicing (the script
  quotes no specific call — do not add one) (CLM-0018).
- NO real-person likeness, NO real logos/seals/landmarks in any image (invariant 11).

==================================================================================================
HARD GATES — not finished until ALL pass (measured on the real file)
==================================================================================================
Run: ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 24 --json   -> must exit 0.
Also: ./.venv/Scripts/python.exe scripts/check_runtime_band.py  (on the render) -> 27-33 min.
If scripts/check_dynamics.py exists, run it too (motion gate) -> exit 0; if absent, the motion rows inside
check_final_acceptance.py are authoritative — do not skip the motion measurement.
Confirm with your own measurement and FIX + re-run on any miss:
 [ ] runtime in band 27-33 min
 [ ] narration provider contains "eleven" (never sapi/local)
 [ ] captions coverage >=95%, breath-group, <=17 cps, 0 format violations, bottom-safe
 [ ] BGM present, no silent stretch >25s, audible floor under VO
 [ ] loudness -16..-12 LUFS
 [ ] motion: 0 static spans, 0 freeze >2s, transitions present (no naked hard cut)
 [ ] images all long-edge >=3840, 0 face/real-logo/landmark/text violations
 [ ] factory density >= runtime/30s, layer across >=40% timeline, no clip reused >3x
 [ ] structure: hook(~8s)/opening/body/ending present + CTA in last 30s; OP after hook, ED at tail
 [ ] >=3 thumbnails @1280x720 + selected
 [ ] 0 black frames

==================================================================================================
BANNED FAILURE MODES (the exact things that caused past rework)
==================================================================================================
- SAPI/robot voice instead of ElevenLabs.            - Captions pasted from script (must be force-aligned).
- BGM dropping to silence under narration.            - Static images / frame held still / naked hard cuts ("kaku").
- Runtime below band (narration only, no real edit).  - Black frames / dead air.
- No thumbnails, or a face/real logo/landmark in one. - Merging Gupta's case/penalties with Rajaratnam's.
- Stating profit as one flat number.                  - Declaring "done" without the gate exit 0.

==================================================================================================
DO NOT (hard stops)
==================================================================================================
- Do NOT publish, upload, set a thumbnail live, or change privacy/visibility. Build a finished file and STOP.
- Do NOT run the pre-publish R2 LEGAL REVIEW yourself or mark it done. That + publish are OWNER gates.
- Do NOT use NVENC. Do NOT exceed the $25 narration cap. Do NOT overwrite an approved/published mp4.
- Do NOT rewrite the script/claims, invent facts, or contradict the R2 wording locks. Do NOT use any
  real-person face/likeness or any real logo/seal/landmark.

==================================================================================================
WHEN THE GATE PASSES — finish like this, then STOP
==================================================================================================
- Leave: accepted final.mp4 (H:\...\08_edit\v001.mp4), captions .srt, >=3 thumbnails @1280x720 (selected
  marked), render/QC log. Register every used asset in the rights manifest (origin, license, AI-disclosure).
- Write a SELF-AUDIT REPORT mapping EACH gate -> its measured value (e.g. "runtime 30.1 min OK",
  "loudness -13.2 LUFS OK", "captions 97% coverage OK", "0 black frames OK", "0 static spans OK"). This is the proof of done.
- Update manifest.json state to edit_review (NOT published); append events; commit ONLY EP24's own files.
- Then STOP and report: it is ready for the OWNER gates in order — (1) APR-0001 final-script approval,
  (2) first-cut, (3) title/thumbnail, (4) R2 PRE-PUBLISH LEGAL REVIEW (confirm memoir title/date, verify any
  wiretap quote against the trial record, confirm Gupta separation), (5) public scheduling bound to the exact
  revision/hash. Keep looping build->measure->fix until check_final_acceptance.py 24 exits 0. Hand over a file
  that already passes every gate, not a "first cut for review".
