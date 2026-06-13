# Prime Documentary — Autonomous Studio Blueprint Edition 2

This is the **100-point, implementation-oriented edition** of the Prime Documentary production blueprint for Claude Code.

It contains:
- one massive master specification
- a concise project constitution (`CLAUDE.md`)
- a takeover/bootstrap prompt
- 42 detailed production and engineering documents
- machine-readable contracts and JSON Schemas
- Claude Code rules, skills, subagents and hook examples
- prompt library
- architecture decision records
- implementation backlog
- templates and runbooks
- a small executable Python reference core
- tests and whole-package validation

## Primary files

1. `START_HERE.md`
2. `CLAUDE.md`
3. `BOOTSTRAP_PROMPT.txt`
4. `PD_AUTONOMOUS_STUDIO_MASTER_SPEC_V2.md`
5. `VALIDATION_REPORT_V2.md`

## Goal

The target operating model is not “AI assists a human editor.” It is:

> Approved topics flow through research, evidence, script, scenes, assets, narration, music, assembly edit, quality control and private upload automatically. Humans make portfolio, high-risk, creative and public-release decisions. Failures are localized and resumable.

## Recommended use

Copy the package into the PD development repository, start Claude Code from the repository root, and submit `BOOTSTRAP_PROMPT.txt`. Require a no-change takeover audit before implementation.

## Validation

Run:

```bash
PYTHONPATH=src python scripts/validate_all_v2.py
```

The reference code is intentionally small. It demonstrates the required invariants and does not pretend to be the full production platform.

## Runnable vertical slice

A first executable pipeline composes the core invariants into the artifact chain
`topic → research_plan → sources → claims → thesis → script → scene_plan →
asset_plan → voice_plan → edit_plan → qc_report` (no network, no LLM, no upload):

```bash
make demo      # run the whole chain on a throwaway episode under runs/
make test      # unit tests (core + pipeline + studio/UI)
```

## Minimal studio UI

A one-screen web UI wraps the same pipeline: type a theme, click run, and read the
generated thesis / script / scene plan / QC verdict. It is a thin adapter over
`pd_factory.studio.create_and_run` — still no network, no LLM, no paid calls, no
upload. Episodes are written to throwaway workspaces under `runs/ui/` (gitignored),
and the QC gate keeps reporting the episode as not-publishable until real research
replaces the placeholders.

```bash
make ui        # serves http://127.0.0.1:8765  (Ctrl-C to stop)
```

Note: clicking "run" only clears the local *screening* gate so the pipeline may
execute. It is not a portfolio or publication approval — those human gates are
untouched (nothing here publishes).

See `docs/VERTICAL_SLICE_MVP.md` and the takeover audit in
`reports/TAKEOVER_AUDIT_2026-06-13.md`.
