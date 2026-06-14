"""ElevenLabs adapter — narration. auth_check is free; generation is paid (gated)."""
from __future__ import annotations

from typing import Any

from ..budget import BudgetLedger
from ..idempotency import make_idempotency_key
from .env import EnvStore
from .http import Transport, request, require_confirmed

VOICES_URL = "https://api.elevenlabs.io/v1/voices"
TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
# Rough metered cost basis (USD per 1k characters) — verify against the active plan (docs/33).
USD_PER_1K_CHARS = 0.30


def auth_check(env: EnvStore, *, transport: Transport | None = None) -> dict[str, Any]:
    """Free: list voices. Proves the API key works without spending characters."""
    key = env.get("ELEVENLABS_API_KEY")
    if not key:
        return {"provider": "elevenlabs", "ok": False, "status": None, "detail": "ELEVENLABS_API_KEY not set"}
    status, body = request("GET", VOICES_URL, headers={"xi-api-key": key}, transport=transport)
    ok = status == 200
    n = len(body.get("voices", [])) if ok and isinstance(body, dict) else 0
    return {"provider": "elevenlabs", "ok": ok, "status": status, "detail": (f"{n} voices" if ok else f"HTTP {status}")}


def estimate_cost_usd(text: str) -> float:
    return round(len(text) / 1000.0 * USD_PER_1K_CHARS, 4)


def generate_speech(
    env: EnvStore,
    *,
    episode_id: str,
    chunk_id: str,
    text: str,
    confirmed: bool,
    budget: BudgetLedger,
    transport: Transport | None = None,
) -> dict[str, Any]:
    """PAID. Thin gated frame (rules/11): preflight + idempotency + budget + confirm.

    Execution is intentionally NOT wired during access-prep; it is enabled on the owner's
    cost go-ahead. Calling without confirmation raises; with confirmation it still refuses
    until generation is explicitly enabled, so no characters are ever spent by accident.
    """
    require_confirmed(confirmed, "ElevenLabs generate_speech")
    voice_id = env.require("ELEVENLABS_VOICE_ID")
    key = make_idempotency_key(
        stage="tts", episode_id=episode_id, input_revisions=[chunk_id],
        config_revision="elevenlabs-v1", provider_profile=voice_id,
    )
    budget.reserve(estimate_cost_usd(text))  # raises BudgetExceeded past the hard limit
    raise NotImplementedError(
        f"ElevenLabs generation frame ready (idempotency={key}, est=${estimate_cost_usd(text)}) "
        "but execution is disabled until the owner confirms cost and we wire the binary fetch."
    )
