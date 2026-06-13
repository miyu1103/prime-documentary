"""Real research acquisition adapter (decision 0002 §10, docs/28).

This package is the FIRST point where untrusted external input enters the system.
It isolates network egress behind:

- a host/scheme allowlist + size cap (preflight),
- an idempotency cache (re-runs do not re-fetch or re-spend),
- a request budget gate,
- treatment of all fetched bytes as untrusted DATA (never executed; see sanitize).

Core domain artifacts (source registry, claim ledger) stay provider-neutral; the
provider-specific payloads live behind the fetchers in :mod:`providers`.
"""
from __future__ import annotations

from .fetcher import FetchResult, fetch
from .preflight import PreflightError, preflight

__all__ = ["FetchResult", "fetch", "PreflightError", "preflight"]
