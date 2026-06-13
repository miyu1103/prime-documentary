"""Runway adapter — hero video clips. auth_check reads credits; generation is paid (gated)."""
from __future__ import annotations

from typing import Any

from ..budget import BudgetLedger
from ..idempotency import make_idempotency_key
from .env import EnvStore
from .http import Transport, request, require_confirmed

# Runway API (verify endpoint + version header against docs/33 before relying on it).
ORG_URL = "https://api.dev.runwayml.com/v1/organization"
API_VERSION = "2024-11-06"


def _headers(key: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {key}", "X-Runway-Version": API_VERSION}


def auth_check(env: EnvStore, *, transport: Transport | None = None) -> dict[str, Any]:
    """Minimal read: organization / credit balance. No generation, no cost."""
    key = env.get("RUNWAY_API_KEY")
    if not key:
        return {"provider": "runway", "ok": False, "status": None, "detail": "RUNWAY_API_KEY not set"}
    status, body = request("GET", ORG_URL, headers=_headers(key), transport=transport)
    ok = status == 200
    credits = body.get("creditBalance") if ok and isinstance(body, dict) else None
    detail = (f"credits: {credits}" if credits is not None else "auth OK") if ok else f"HTTP {status}"
    return {"provider": "runway", "ok": ok, "status": status, "detail": detail}


def generate_video(
    env: EnvStore,
    *,
    episode_id: str,
    shot_id: str,
    prompt: str,
    confirmed: bool,
    budget: BudgetLedger,
    transport: Transport | None = None,
) -> dict[str, Any]:
    """PAID. Thin gated frame; execution disabled during access-prep (rules/11, 0002 §5 budget-cap)."""
    require_confirmed(confirmed, "Runway generate_video")
    key = make_idempotency_key(
        stage="runway_clip", episode_id=episode_id, input_revisions=[shot_id],
        config_revision="runway-v1", provider_profile="gen",
    )
    raise NotImplementedError(
        f"Runway generation frame ready (idempotency={key}). Per-episode Runway budget must be set "
        "from the monthly plan tier (0002 §5) and the owner must confirm before any credits are spent."
    )
