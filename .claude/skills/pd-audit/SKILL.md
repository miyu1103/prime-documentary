---
name: pd-audit
description: Audits the current PD repository before implementation. Use when starting work, inheriting an existing codebase, or checking architectural gaps and risks.
---

# PD Repository Audit

## Read first

- `CLAUDE.md`
- `PD_CLAUDE_CODE_MASTER_BLUEPRINT.md`
- `docs/01_AUTONOMY_AND_ARCHITECTURE.md`
- `docs/10_DATA_MODEL_AND_STATE_MACHINE.md`
- `docs/15_IMPLEMENTATION_ROADMAP.md`

## Procedure

1. Inventory the repository, excluding generated caches and secrets.
2. Identify executable entry points, configs, schemas, databases, tests and provider integrations.
3. Search for duplicate implementations, TODOs, placeholders, hardcoded paths, API keys, UI automation and destructive operations.
4. Map existing modules to PD stages.
5. Determine which source is currently treated as truth: files, DB, filenames, spreadsheets or memory.
6. Check whether jobs are resumable and idempotent.
7. Check approval boundaries and public-publish safeguards.
8. Check schema/version/migration support.
9. Run safe read-only or test commands where available.
10. Produce a gap analysis against Phase 1, L3 and L4.

## Output

- Executive conclusion
- Current architecture
- Implemented capability matrix
- Missing capability matrix
- Critical risks
- Existing assets worth preserving
- Technical debt
- Recommended first vertical slice
- Ordered implementation plan
- Tests and rollback
- Explicit assumptions

Do not modify files unless the user explicitly includes implementation in the request.
