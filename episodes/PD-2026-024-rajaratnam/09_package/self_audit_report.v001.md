# PD-2026-024-rajaratnam Self-Audit Report

Final gate command:

```powershell
.\.venv\Scripts\python.exe scripts\check_final_acceptance.py 24 --json
```

Result: PASS, exit code 0.

Final video: `H:\pd-media\episodes\PD-2026-024-rajaratnam\08_edit\v001.mp4`

Final SHA-256: `f82918b214cee1c6caf30116fecdd245ddaf7f67c4f41864312d9e06dd6e2047`

## Gate Measurements

- Runtime: 1716.7s / 28.61 min, OK, within 27-33 min band.
- Render: 1920x1080 H.264, libx264 slow, CRF 16, yuv420p, BT.709, AAC 320k, OK.
- NVENC: not used, OK.
- Narration: ElevenLabs master present, provider contains `elevenlabs`, OK.
- Narration budget: estimated $8.04 of $25 cap, OK.
- Captions: 562 cues, last cue 1707.686s, 99.47% coverage, OK.
- Caption format: 0 strict violations; min duration 1.000s, max duration 4.932s, max CPS 16.44, 0 gap violations, OK.
- BGM: continuous six-cue Suno-origin library bed, total silence 0s, longest silence 0s, OK.
- Loudness: -14.3 LUFS integrated, OK.
- Motion: frozen total 0.0s, longest freeze 0.0s, OK.
- Black frames: black total 0.0s, longest black 0.0s, OK.
- Images: 42 Codex AI-generated hero stills, minimum long edge 3840px, OK.
- Visual hard rules: reviewed final S031-S042 contact sheet after replacing theme-mismatched stills; no real-person likeness, real logos/seals/landmarks, or readable text intentionally used.
- Factory layer: 72 staged factory clips, full-timeline blended factory bed measured at 1623.533s over 1716.7s final runtime, 94.57% coverage, OK.
- Factory reuse: 144 concat entries, 72 distinct factory clips, max reuse 2, OK.
- Structure: first 8s hook, BrandOpening at 8.0-11.5s, BrandEndcard in final 9s, CTA animation from roughly final 30s to final 5s, OK.
- Thumbnails: 3 candidates at 1280x720 plus selected thumbnail, OK.
- Rights manifest: 121 assets registered; visual origin is `Codex AI-generated still`, OK.
- Legal/publish boundary: no upload, no scheduling, no R2 legal review marked complete, OK.

## Additional Checks

- `scripts\check_runtime_band.py` with 1620-1980s band: PASS.
- `scripts\check_dynamics.py`: PASS for freeze, black, and silence.
- `npm run typecheck` in `remotion`: PASS.
- `scripts\validate_episode.py 24`: PASS during preflight.
