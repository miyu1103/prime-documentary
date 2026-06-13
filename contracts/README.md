# PD Pipeline Contracts

Contracts define stage boundaries independently of any provider or implementation language.

Every stage contract must state:
- purpose
- input artifact types and revisions
- output artifact types
- preconditions
- deterministic validation
- quality validation
- side effects
- estimated cost
- idempotency key
- retry policy
- failure codes
- stale propagation
- approval requirement
- observability

A provider adapter may add raw metadata, but it may not change the core contract.
