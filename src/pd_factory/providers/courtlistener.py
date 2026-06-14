"""CourtListener adapter — free, token-gated. Research fetching lives in research/."""
from __future__ import annotations

from typing import Any

from .env import EnvStore
from .http import Transport, request

AUTH_CHECK_URL = "https://www.courtlistener.com/api/rest/v4/courts/?page_size=1"


def auth_check(env: EnvStore, *, transport: Transport | None = None) -> dict[str, Any]:
    """Minimal, free GET that proves the token works (no cost)."""
    token = env.get("COURTLISTENER_TOKEN")
    if not token:
        return {"provider": "courtlistener", "ok": False, "status": None, "detail": "COURTLISTENER_TOKEN not set"}
    status, body = request("GET", AUTH_CHECK_URL, headers={"Authorization": f"Token {token}"}, transport=transport)
    ok = status == 200
    detail = "token OK" if ok else f"HTTP {status}: {str(body)[:120]}"
    return {"provider": "courtlistener", "ok": ok, "status": status, "detail": detail}
