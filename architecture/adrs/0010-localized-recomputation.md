# ADR — Localized recomputation

- Status: Accepted
- Date: 2026-06-13

## Decision

Dependency graph marks only affected downstream artifacts stale.

## Rationale

Avoids full episode regeneration and lowers cost.

## Consequences

Requires accurate lineage.

## Review trigger

Review only when measured production evidence shows the trade-off is no longer valid.
