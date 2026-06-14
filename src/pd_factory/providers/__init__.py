"""External provider adapters (decisions/0002 §7, docs/33).

Each adapter reads its secret from the git-ignored `.env` (never committed; rules/03),
exposes a FREE/minimal `auth_check()` (no paid side effect), and gates every paid or
publishing operation behind explicit confirmation + a budget (rules/11, docs/24).

Adapters are intentionally thin: provider-specific payloads stay here; core domain code
stays provider-neutral. Network egress is host-allowlisted and the transport is injectable
so tests never hit the network.
"""
from __future__ import annotations

from .env import EnvStore, load_env
from .http import (
    PaidOperationNotConfirmed,
    PreflightError,
    ProviderError,
    request,
)

__all__ = [
    "EnvStore",
    "load_env",
    "request",
    "PreflightError",
    "ProviderError",
    "PaidOperationNotConfirmed",
]
