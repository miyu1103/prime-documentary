from __future__ import annotations
import hashlib
import json
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import Any


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value)}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_canonical(x) for x in value]
    return value


def canonical_json(value: Any) -> str:
    """Stable JSON text: sorted keys, compact separators, UTF-8 preserved."""
    return json.dumps(_canonical(value), ensure_ascii=False, separators=(",", ":"))


def content_hash(value: Any) -> str:
    """sha256 of the canonical JSON form of a JSON-serializable value."""
    raw = canonical_json(value).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_provenance(
    *,
    artifact_id: str,
    artifact_type: str,
    revision: str,
    producer: str,
    input_revisions: dict[str, str],
    idempotency_key: str,
    checksum: str,
    cost_amount: float,
    cost_currency: str,
) -> dict[str, Any]:
    """Provenance sidecar record (invariant 7).

    Kept beside the artifact rather than embedded, because stage schemas use
    additionalProperties:false and must not be polluted with operational metadata.
    """
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "revision": revision,
        "producer": producer,
        "input_revisions": dict(sorted(input_revisions.items())),
        "idempotency_key": idempotency_key,
        "checksum": checksum,
        "cost": {"amount": cost_amount, "currency": cost_currency},
        "created_at": now_iso(),
    }
