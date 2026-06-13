---
name: pd-backup-verify
description: Verify backups by performing an isolated restore and reconciliation
---

# Procedure


1. Identify latest eligible backup and expected contents.
2. Restore into an isolated destination.
3. Validate schema and event log continuity.
4. Reconcile artifact hashes and manifests.
5. Open or validate a representative project artifact.
6. Generate status report.
7. Record RPO/RTO result and missing data.
8. Do not overwrite production during the test.


# Required report

- exact scope and revisions
- inputs inspected
- actions or proposed actions
- verification
- side effects and cost
- blockers
- rollback or disable path
