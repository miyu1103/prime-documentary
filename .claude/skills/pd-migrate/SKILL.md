---
name: pd-migrate
description: Plans and implements safe PD schema, folder, manifest or state-machine migrations with inventory, backup, dry-run, validation and rollback.
---

# PD Migration Workflow

## Procedure

1. Inventory affected schemas, code, episodes, artifacts, tests and tools.
2. State the old and new contract.
3. Classify breaking vs non-breaking changes.
4. Design versioned migration and reverse/rollback plan.
5. Back up or snapshot affected data.
6. Implement a dry-run report.
7. Migrate a representative fixture first.
8. Validate references, hashes, approvals and state transitions.
9. Run golden episode regression.
10. Migrate remaining data in batches.
11. Produce completion and exception reports.

## Never

- Rewrite all episodes without a dry-run.
- Drop unknown fields silently.
- Preserve approvals when approved content changed.
- Delete old data before verification.
