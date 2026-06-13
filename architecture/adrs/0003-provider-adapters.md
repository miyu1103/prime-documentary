# ADR — Provider-neutral core

- Status: Accepted
- Date: 2026-06-13

## Decision

All external tools are behind adapters; core objects contain neutral concepts.

## Rationale

Prevents lock-in and supports fallback/testing.

## Consequences

Adapter development is additional work.

## Review trigger

Review only when measured production evidence shows the trade-off is no longer valid.
