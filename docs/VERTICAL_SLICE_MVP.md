# Vertical-Slice MVP — Runnable Pipeline

- Status: implemented (Phase 1–2 of the takeover plan)
- Added: 2026-06-13
- Scope: prove the system architecture end-to-end, not produce a publishable episode.

This is the first executable slice requested by `START_HERE.md` and
`BOOTSTRAP_PROMPT.txt` §E. It composes the existing reference-core invariants
(idempotency, budget, schema validation, approval, artifact URIs) into a runnable
chain. It performs **no network, no LLM, no paid calls, and no upload.**

## The chain

```
approved topic
  → research_plan → sources → claims → thesis → script
  → scene_plan → asset_plan → voice_plan → edit_plan → qc_report
```

Each stage writes an immutable, revisioned artifact (`vNNN`) plus a provenance
sidecar (`*.meta.json`), registers it in `manifest.json`, and appends to
`events.jsonl`.

## How to run

```bash
make demo            # runs the whole chain on a throwaway episode under runs/
make test            # 18 unit tests (9 core + 9 pipeline)
make validate        # whole-package validation

# Or directly against any episode directory that has 00_topic + manifest.json:
PYTHONPATH=src python -m pd_factory.cli run   <episode_dir>
PYTHONPATH=src python -m pd_factory.cli run   <episode_dir> --from claims   # partial rerun
PYTHONPATH=src python -m pd_factory.cli status <episode_dir>
```

## Properties demonstrated (mapped to invariants)

| Property | How | Invariant |
|---|---|---|
| Immutable revisions | `EpisodeRepo.write_artifact` refuses to overwrite an existing `vNNN` | 6 |
| Provenance + hashes | provenance sidecar with producer, input revisions, idempotency key, sha256 | 7 |
| Resumability | a stage with a matching stored idempotency key is **skipped** | 8 |
| Idempotency keys | `make_idempotency_key(stage, episode, input_revisions, config)` | 5, 8 |
| Downstream invalidation | a stage's key includes upstream input revisions, so a changed upstream forces dependents to recompute | 12 |
| Budget gating | every stage reserves/commits against the manifest budget ledger (cost 0 for local stubs) | 5 |
| Schema validation | each artifact validated against its `schemas/*.schema.json` (arrays per-item) | — |
| Approval gate respected | the pipeline refuses to run unless the manifest state is `approved` or later; it never self-approves a topic | 2 (human gate) |
| "Generated ≠ usable" | research is placeholder, so the final QC report returns `pass_with_warnings` and marks the episode **not publishable** until real sources replace placeholders | 1, 13 |

## Honest limitations (by design)

- Generators are **deterministic stubs** derived from the topic's own fields. They
  invent no facts; placeholder sources/claims are explicitly flagged
  (invariants 1, 10, 11).
- On-disk `manifest.state` advances only to `script_draft`. It does **not** claim
  `script_verified` / `scene_planned`, because real fact-checking has not run. The
  downstream draft artifacts (scene/asset/voice/edit/qc) are produced to prove the
  architecture, and the QC gate reports that the episode is gated on research.
- `manifest.state` uses the reconciled superset enum, which now matches both the
  schema and the `EpisodeState` code model (audit gap **G1**, resolved — see the
  resolution log in `reports/TAKEOVER_AUDIT_2026-06-13.md`). One editorial question
  remains for the owner: whether to collapse `audio_ready` vs `voice_ready`/
  `music_ready` into a single canonical model.

## New modules

- `src/pd_factory/provenance.py` — canonical JSON, content hashing, provenance records.
- `src/pd_factory/episode_repo.py` — immutable artifact store, manifest I/O, event log.
- `src/pd_factory/generators.py` — deterministic per-stage generators.
- `src/pd_factory/pipeline.py` — orchestrator (run, resume, partial rerun) + CLI helpers.
- `src/pd_factory/cli.py` — `run` / `status` subcommands (extended).
- `scripts/run_demo.py`, `tests/test_pipeline.py`.

## Next highest-value action

Reconcile the episode-state enums (G1), then replace `gen_sources`/`gen_claims` with
a real research adapter behind the `docs/28` web-safety policy — the first point where
external input and prompt-injection defenses must be enforced.
