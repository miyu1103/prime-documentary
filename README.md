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
