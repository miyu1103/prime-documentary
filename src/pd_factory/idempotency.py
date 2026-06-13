from __future__ import annotations
import hashlib
import json
from collections.abc import Mapping, Sequence
from typing import Any

def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value)}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_canonical(x) for x in value]
    return value

def make_idempotency_key(
    *, stage: str, episode_id: str, input_revisions: list[str],
    config_revision: str, provider_profile: str | None = None,
) -> str:
    payload = {
        "stage": stage,
        "episode_id": episode_id,
        "input_revisions": sorted(input_revisions),
        "config_revision": config_revision,
        "provider_profile": provider_profile,
    }
    raw = json.dumps(_canonical(payload), ensure_ascii=False, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()
