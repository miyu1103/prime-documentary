# EP21 Self-Audit Report

Episode: PD-2026-021-dbcooper
State: edit_review
Final video: H:/pd-media/episodes/PD-2026-021-dbcooper/08_edit/final.mp4
Generated: 2026-07-01T02:33:48+00:00

## Gate Results

- check_final_acceptance.py 21 --json: PASS, exit 0
- check_dynamics.py 21: PASS, exit 0
- check_runtime_band.py final.mp4: PASS, exit 0

## Measured Values

- Runtime: 1781.07 seconds = 29.68 minutes; required band 1620-1980 seconds.
- Resolution/codecs: 1920x1080 H.264/libx264, yuv420p, AAC audio.
- Loudness: -14.3 LUFS; required -16.0 to -12.0 LUFS.
- Voice: ElevenLabs master narration present; provider locked to elevenlabs.
- Captions: captions.v001.srt present; 492 cues; final cue at 1772 seconds; caption format gate passed.
- Caption visual fix: smaller unboxed subtitles; smarter two-line wraps; source-script word sequence verified against captions with no dropped words.
- Black frames: 0.0 seconds total, 0.0 seconds longest.
- Frozen frames/static holds: 2.7 seconds total, 2.7 seconds longest; within the 8.0/4.0 second gate.
- Audio silence: 0.0 seconds total.
- Hero images: 46 PNGs present; all long edge >= 3840 px.
- Factory assets: 64 staged and referenced in composition; gate requires >=39.
- Motion plan: average shot length 5.4 seconds, 0.42 second crossfades, Ken Burns/parallax planned across stills, no planned naked hard cuts.
- Thumbnails: 3 candidates plus selected thumbnail, all 1280x720.

## R2 / Legal Safety

- Case language remains UNSOLVED; no on-screen text or thumbnail asserts the case is solved.
- Thumbnails use: STILL MISSING, $200,000 GONE, WHO WAS HE?
- No upload, publish, thumbnail-set, privacy change, or scheduling action was performed.
- Owner pre-publish review remains required before any external release.

## Evidence

- episodes/PD-2026-021-dbcooper/09_package/EVIDENCE/final_acceptance.caption_fix.v005.stdout.txt
- episodes/PD-2026-021-dbcooper/09_package/EVIDENCE/dynamics.caption_fix.v005.stdout.txt
- episodes/PD-2026-021-dbcooper/09_package/EVIDENCE/runtime_band.caption_fix.v005.stdout.txt
- episodes/PD-2026-021-dbcooper/09_package/EVIDENCE/caption_visual_fix_render.v005.stdout.txt
