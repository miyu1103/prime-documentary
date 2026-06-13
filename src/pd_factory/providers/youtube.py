"""YouTube adapter — publish. auth_check reads channel info; upload is a gated side effect."""
from __future__ import annotations

from typing import Any

from ..idempotency import make_idempotency_key
from .env import EnvStore
from .http import Transport, ProviderError, request, require_confirmed

TOKEN_URL = "https://oauth2.googleapis.com/token"
CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&mine=true"


def _access_token(env: EnvStore, *, transport: Transport | None = None) -> str:
    status, body = request(
        "POST",
        TOKEN_URL,
        form_body={
            "client_id": env.require("YOUTUBE_CLIENT_ID"),
            "client_secret": env.require("YOUTUBE_CLIENT_SECRET"),
            "refresh_token": env.require("YOUTUBE_REFRESH_TOKEN"),
            "grant_type": "refresh_token",
        },
        transport=transport,
    )
    if status != 200 or not isinstance(body, dict) or "access_token" not in body:
        raise ProviderError(f"token refresh failed: HTTP {status}")
    return body["access_token"]


def auth_check(env: EnvStore, *, transport: Transport | None = None) -> dict[str, Any]:
    """Read-only: refresh-token -> access-token -> channels.list(mine). No upload, no cost."""
    if not env.present("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"):
        return {"provider": "youtube", "ok": False, "status": None, "detail": "YOUTUBE_* not fully set"}
    try:
        token = _access_token(env, transport=transport)
    except ProviderError as exc:
        return {"provider": "youtube", "ok": False, "status": None, "detail": str(exc)}
    status, body = request("GET", CHANNELS_URL, headers={"Authorization": f"Bearer {token}"}, transport=transport)
    ok = status == 200
    title = None
    if ok and isinstance(body, dict) and body.get("items"):
        title = body["items"][0].get("snippet", {}).get("title")
    return {"provider": "youtube", "ok": ok, "status": status, "detail": (f"channel: {title}" if ok else f"HTTP {status}")}


def upload_video(
    env: EnvStore,
    *,
    episode_id: str,
    package_revision: str,
    confirmed: bool,
    channel_allowlist_id: str,
    transport: Transport | None = None,
) -> dict[str, Any]:
    """SIDE EFFECT (publish). Thin gated frame; private-first; allowlist + exact-revision approval
    required (rules/03, rules/16, 0002 §7). Execution disabled during access-prep."""
    require_confirmed(confirmed, "YouTube upload_video")
    key = make_idempotency_key(
        stage="yt_upload", episode_id=episode_id, input_revisions=[package_revision],
        config_revision="youtube-v1", provider_profile=channel_allowlist_id,
    )
    raise NotImplementedError(
        f"YouTube upload frame ready (idempotency={key}). Requires: channel on allowlist, "
        "publish approval for the exact package revision/hash, privacy=private first (0002 §7)."
    )
