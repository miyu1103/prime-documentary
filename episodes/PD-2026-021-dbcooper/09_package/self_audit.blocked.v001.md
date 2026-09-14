# EP21 Self Audit - Blocked Before Final Render

Status: BLOCKED, not gate-accepted.

Episode: `PD-2026-021-dbcooper` - D.B. Cooper: The Only Hijacking America Never Solved.

## Completed

- Preflight read the locked script inputs: 61 `[VO:]` rows and 61 annotated spans.
- ElevenLabs narration completed: 61/61 chunks OK, provider `elevenlabs`, voice ID `nPczCjzI2devNBz1zQrb`.
- Voice master built: `H:/pd-media/episodes/PD-2026-021-dbcooper/06_audio/master_elevenlabs_v001/voice_master.v001.wav`.
- Audio mix built with continuous BGM: `H:/pd-media/episodes/PD-2026-021-dbcooper/08_edit/dbcooper_final_mix.v001.wav`.
- Captions built: `episodes/PD-2026-021-dbcooper/08_edit/captions.v001.srt`, 492 cues, no local format violations.
- Factory shelf staged: 64 assets, referenced by `remotion/src/compositions/DBCooperPremium.tsx`.
- Factory shelf is balanced across 8 buckets: aviation, forest, crime/police, documents, money, urban night, surveillance, atmosphere.
- Remotion roughcut scaffold written: `remotion/src/data/dbcooper_roughcut.ts`.
- Pre-render reports written: `08_edit/asset_usage_report.json`, `08_edit/motion_report.json`, and `05_stock/image_preflight.v001.json`.

## Measurements

- Voice/audio duration: 1547.358 seconds, 25.79 minutes.
- Audio loudness: -14.2 LUFS integrated, LRA 2.1.
- Caption last end: 1538.358 seconds.
- Caption format violations: 0.

## Blockers

Hero images are incomplete in `H:/pd-media/episodes/PD-2026-021-dbcooper/05_visuals/selected`.

Found: `EP21-IMG-001.png` only.

Missing: `EP21-IMG-002.png` through `EP21-IMG-046.png`.

The found image is `1672x941`, below the required 4K long-edge image gate. It should be replaced by Codex app output at the required size.

`approvals/APR-0001.json` currently says `decision: pending`, while the operating prompt says approved. I did not rewrite the script or approval file. Publish/upload remains blocked.

## Gate Result

`scripts/check_final_acceptance.py 21 --json` currently exits 1.

Hard failures:

- `render_present`: final render not found.
- `thumbnail_ready`: 0 thumbnails at 1280x720, selected=NO.

Passing checks already available:

- `voice_is_master`
- `captions_final`
- `caption_format`
- `factory_used`

`check_dynamics.py 21` now resolves to `H:/pd-media/episodes/PD-2026-021-dbcooper/08_edit/final.mp4`; it still fails until that file exists.

`check_runtime_band.py` now infers the mid-profile band from the render path's episode manifest when `--lo/--hi` are not supplied.

## Next Required Action

Place all 46 final 4K hero stills into:

```text
H:/pd-media/episodes/PD-2026-021-dbcooper/05_visuals/selected
```

Then rerun:

```powershell
.venv\Scripts\python.exe scripts\build_ep21_dbcooper_final.py
.venv\Scripts\python.exe scripts\check_final_acceptance.py 21 --json
.venv\Scripts\python.exe scripts\check_dynamics.py 21
.venv\Scripts\python.exe scripts\check_runtime_band.py H:\pd-media\episodes\PD-2026-021-dbcooper\08_edit\final.mp4
```

Do not upload, publish, or change visibility before the owner publish gate.
