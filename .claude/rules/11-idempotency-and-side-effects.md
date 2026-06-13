# Idempotency and Side Effects

- Every paid API request, upload, publish, file promotion, and destructive operation must declare an idempotency strategy.
- Store external request IDs and query provider state after timeouts before retrying.
- A retry may not silently duplicate cost or publication.
- Dry-run must not execute external writes.
- Side effects must be listed in function/docstring/contract and logged without secrets.
