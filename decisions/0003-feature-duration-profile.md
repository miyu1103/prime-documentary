# ADR-0003 — Feature-length duration profile for flagship episodes

- Status: Accepted
- Date: 2026-06-24
- Context owner: PD (local lead)
- Supersedes: none
- Related: CLAUDE.md invariant 15 (no silent weakening of validation), invariant 13 (generated output usability), `scripts/validate_episode.py`, `schemas/episode-manifest.schema.json`

## Context

PD standard episodes target ~10-12.8 minutes. `validate_episode.py` hard-coded a narration-duration QC band of `10.0 <= words/150 <= 12.8` minutes. EP16 (`PD-2026-016-titan`) is the first **feature** (≈60-minute flagship). Its narration is intentionally restrained — roughly 6,300 words (~42 narration-minutes at 150 wpm) — with the remaining runtime carried by *designed* silence and visual/music sequences (the cold-open hold, the total-silence beat at the implosion, descent sequences, the four-day search montage, coda holds). Under the old band, every feature would emit a misleading QC warning.

The episode-manifest schema is `additionalProperties: false`, so a new bespoke field (e.g. `duration_profile`) cannot be added without a schema migration. The schema already exposes `target_duration_minutes` (number, 1-180).

## Decision

1. Use the existing, schema-allowed `manifest.target_duration_minutes` as the feature signal.
2. In `validate_episode.py`, when `target_duration_minutes >= 20`, evaluate the narration band as `0.50 * target .. 1.05 * target` minutes (scaled to the planned runtime, allowing for designed silence). Otherwise keep the unchanged standard band `10.0 .. 12.8`.
3. This is a QC **warning** band only; it does not change pass/fail (schema/consistency/hash errors still fail). The standard gate for standard episodes is unchanged.

Rationale for the threshold and ratios: standard episodes set `target_duration_minutes` ≈ 12 (< 20), so they are unaffected. Features run at a deliberately slow pace with substantial non-narrated time; `0.50x` lower bound prevents a feature from being mostly silence, and `1.05x` upper bound prevents narration overflowing the planned runtime.

## Why this is NOT a silent weakening (invariant 15)

- The standard 10.0-12.8 band is preserved verbatim for standard episodes.
- The feature band is explicit, documented here and in code comments, and only activates when the manifest *declares* a feature-length target.
- No schema was loosened; no failing artifact was made to pass by lowering a gate. Schema validity, claim/span consistency, and the manifest↔annotated hash check are unchanged and still gate.

## Consequences

- `validate_episode.py PD-2026-016-titan` reports `PASS` (no spurious timing warning) while keeping all real checks.
- Future features set `target_duration_minutes` to the planned runtime and inherit the band.
- If feature pacing conventions change, revisit the 0.50/1.05 ratios here.

## Rollback

Revert the duration-band block in `scripts/validate_episode.py` to the single line `if not (10.0 <= dur <= 12.8):` and delete this ADR. No data migration is required (no stored artifact depends on the band).
