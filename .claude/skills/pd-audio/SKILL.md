---
name: pd-audio
description: Creates narration chunks, generates draft or master voice, checks pronunciation and seams, selects music and builds audio cue sheets.
---

# PD Audio Workflow

## Procedure

1. Confirm whether the script is draft or approved.
2. Use draft voice before final approval; use master voice only after approval.
3. Chunk by semantic completeness, chapter, emotional change and revision risk.
4. Apply pronunciation dictionary and spoken-text normalization.
5. Generate with idempotency and usage logging.
6. Validate exact script coverage, pronunciation, audio integrity, loudness and seams.
7. Regenerate only failed chunks.
8. Search the rights-cleared music library by chapter function and energy curve.
9. Prefer reuse over unnecessary new generation.
10. Create music and SFX cue sheets with dialogue masking constraints.
11. Record rights and provider evidence.

## Output

- narration chunks
- draft/master narration
- alignment data
- audio QC
- music cue sheet
- SFX/ambience cue sheet
- rights records
