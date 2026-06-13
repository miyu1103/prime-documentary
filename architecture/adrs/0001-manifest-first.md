# ADR — Manifest-first episode state

- Status: Accepted
- Date: 2026-06-13

## Decision

Use a structured episode manifest and event log rather than folder existence or filenames as operational state.

## Rationale

Enables validation, resumption, dependency invalidation, and machine-readable status.

## Consequences

Requires schema migration discipline and reconciliation tooling.

## Review trigger

Review only when measured production evidence shows the trade-off is no longer valid.
