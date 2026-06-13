# Revisions and Staleness

- Approved artifacts are immutable.
- A semantic input change creates a new revision.
- Dependency edges determine stale propagation.
- Stale artifacts remain auditable but cannot pass downstream gates.
- Approval targets exact revision/hash and is invalidated when dependencies change.
