# EP22 Self Audit Prefinal v001

Episode: PD-2026-022-milken
Profile: mid, target 30:00, acceptance band 27-33 minutes
Status at audit: audio_ready, final render blocked by incomplete hero images
Checked at: 2026-06-30T16:45:00Z

## Completed Before Final Render

- Script and annotated script present: 76 annotated spans, 76 VO chunks.
- ElevenLabs master narration generated with fixed voice/model settings.
- Audio mix generated with continuous BGM bed.
- Final captions generated from the locked VO text and chunk timings.
- Factory shelf staged: 64 assets under `remotion/public/milken/factory`.
- Remotion scaffold added: `remotion/src/compositions/MilkenPremium.tsx`.
- Rough-cut data written: `remotion/src/data/milken_roughcut.ts`.
- Thumbnail candidates built: 3 options plus selected thumbnail.
- Rights manifest drafted for currently available hero images, music, and factory shelf.
- Wait/finalize runner added: `scripts/run_ep22_final_after_images.py`.

## Acceptance Status

Command:

```powershell
.\.venv\Scripts\python.exe scripts\check_final_acceptance.py 22 --json
```

Current result: FAIL, as expected, because final render is not present.

Passing hard checks already measured:

- voice_is_master: PASS
- captions_final: PASS
- caption_format: PASS
- thumbnail_ready: PASS
- image_resolution for staged available images: PASS
- factory_used: PASS

Remaining hard blocker:

- render_present: FAIL until all 74 Codex hero images are available and final render is built.

## Image Status

Hero image source:

`H:/pd-media/episodes/PD-2026-022-milken/05_visuals/selected`

Required: EP22-IMG-001.png through EP22-IMG-074.png
Present at last check: 10/74

No local image generation was performed.

## Next Automatic Step

Run:

```powershell
.\.venv\Scripts\python.exe scripts\run_ep22_final_after_images.py --interval-seconds 60 --max-wait-minutes 240
```

When 74/74 images are present, the runner will:

1. Stage the hero images into `remotion/public/milken`.
2. Build thumbnails again from the complete image set.
3. Render the final video locally with FFmpeg/libx264.
4. Write `09_package/final_delivery.v001.json`.
5. Run `check_final_acceptance.py 22 --json`.
6. Save acceptance evidence under `09_package/EVIDENCE`.

## Boundaries Observed

- No upload.
- No publish or schedule.
- No visibility change.
- No local image generation for missing hero stills.
- No script or factual claim rewrite.
