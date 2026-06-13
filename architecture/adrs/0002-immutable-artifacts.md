# ADR — Immutable artifact revisions

- Status: Accepted
- Date: 2026-06-13

## Decision

Approved or referenced artifacts are never overwritten; new revisions supersede old ones.

## Rationale

Preserves auditability and allows exact approvals and rollback.

## Consequences

Consumes more storage; retention policies are required.

## Review trigger

Review only when measured production evidence shows the trade-off is no longer valid.
