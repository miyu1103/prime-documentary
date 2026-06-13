---
name: pd-qc
description: Runs a comprehensive PD quality audit across topic, research, claims, script, scenes, assets, audio, edit, rights, package and automation integrity.
---

# PD Comprehensive QC

## Procedure

1. Identify the target episode and active revisions.
2. Load all gate checklists from `docs/12_QUALITY_GATES_AND_ACCEPTANCE.md`.
3. Validate schemas and cross references.
4. Check claim coverage and unsupported assertions.
5. Check scene coverage and asset completeness.
6. Check visual safety, continuity and misleading reconstruction risk.
7. Check narration coverage, pronunciation and audio integrity.
8. Check edit media, sync, subtitles, chapters, sources and technical render.
9. Check rights manifest and provider terms timestamps.
10. Check package promise against video content.
11. Check approval validity, budget and publishing safeguards.
12. Assign S0–S5 severity.
13. Produce repair jobs limited to affected artifacts.

## Output

- overall pass/fail
- blockers
- findings by stage
- severity
- evidence paths
- exact repair action
- downstream invalidations
- approval impact
