---
name: pd-resume
description: Safely resumes an interrupted or failed PD episode by reconciling state, artifacts, provider side effects, leases, hashes and stale dependencies.
---

# PD Resume Workflow

## Procedure

1. Read manifest, event log, job store and active leases.
2. Detect the last confirmed successful state.
3. Identify jobs that were running at interruption.
4. For each external request, query status before retrying.
5. Verify output files and checksums.
6. Release expired leases only after side-effect reconciliation.
7. Mark incomplete/corrupt artifacts appropriately.
8. Recompute stale dependencies.
9. Check budget reservations and actual usage.
10. Create the minimum safe set of jobs to continue.
11. Run in dry-run first unless the request explicitly authorizes execution.

## Output

- reconciled state
- completed external side effects
- artifacts reused
- jobs retried
- jobs blocked
- cost implications
- next state
