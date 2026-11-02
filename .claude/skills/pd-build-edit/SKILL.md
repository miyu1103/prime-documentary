---
name: pd-build-edit
description: Builds or plans a Remotion + FFmpeg review timeline from approved assets, narration, music, subtitles, motion templates and citations. (2026-08-23 - the editor is Remotion, not DaVinci; CLAUDE.md section 11 retired DaVinci on 2026-06-20 and this description was still advertising it in every session's skill list.)
---

# PD Edit Assembly

## Read first

- `docs/PD_ONE_PASS_PRODUCTION_SPEC.v3.md` (the editor is Remotion + FFmpeg;
  `docs/08_EDITING_DAVINCI_AUTOMATION.md` is kept only as the record of the retired path)
- active scene plan
- approved assets
- narration and cue sheets

## Procedure

1. Validate all required media and checksums.
2. Build a provider-neutral edit plan.
3. Establish timing from narration and semantic anchors.
4. Map primary and secondary visuals.
5. Apply motion templates while avoiding repetitive patterns.
6. Place music, ambience, SFX and ducking instructions.
7. Import subtitles, lower thirds, sources and disclosures.
8. Add issue and review markers.
9. Build the timeline in Remotion and mux with FFmpeg (`build_case_film_generic.py`); do not hand-roll an ffmpeg assembly. The DaVinci scripting path was retired 2026-06-20 and is kept only as the record.
10. Render a review version.
11. Run missing-media, black-frame, sync, subtitle, audio and technical QC.
12. Produce a change set for failed ranges only.

## Safety

- Do not overwrite the master project without versioning.
- Do not assume a UI action succeeded without validation.
- Do not proceed to final render with offline media.

## Output

- edit plan
- timeline/project revision
- review render
- markers
- edit QC
- repair jobs
