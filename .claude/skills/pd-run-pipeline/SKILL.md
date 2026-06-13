---
name: pd-run-pipeline
description: Runs or plans the PD production pipeline from the current episode state, respecting approvals, budgets, dependencies, retries and dry-run mode.
---

# Run PD Pipeline

## Required behavior

1. Read the episode manifest and current event log.
2. Validate manifest and active revisions.
3. Detect stale dependencies and incomplete external requests.
4. Determine runnable stages from the state machine.
5. Check autonomy policy, approval status, WIP limits and budget.
6. In dry-run mode, show all planned jobs, costs, side effects and stop conditions without executing providers.
7. In execution mode, enqueue only allowed jobs.
8. Record idempotency keys and provider request IDs.
9. Validate outputs before state transition.
10. Stop at approval boundaries.
11. Produce a status report with completed, running, blocked, failed and next jobs.

## Never

- Skip invalid states.
- Retry indefinitely.
- Re-run a succeeded paid job without checking idempotency.
- Publish publicly without current approval.
- Hide partial failures.

## Output

- Current state
- Jobs run or planned
- Costs
- Artifacts
- Warnings
- Approval requests
- Next state
