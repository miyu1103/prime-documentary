"""Host-allowlisted HTTP for provider adapters (injectable transport for tests).

Secrets travel only in request headers built here; they are never logged or persisted.
Paid operations must go through `require_confirmed` (rules/11).
"""
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from typing import Any
from urllib.parse import urlparse

# transport(method, url, headers, body_bytes, timeout) -> (status, body_bytes, content_type)
Transport = Callable[..., "tuple[int, bytes, str]"]

ALLOWED_HOSTS: frozenset[str] = frozenset(
    {
        "www.courtlistener.com",
        "courtlistener.com",
        "api.elevenlabs.io",
        "api.dev.runwayml.com",
        "api.runwayml.com",
        "oauth2.googleapis.com",
        "www.googleapis.com",
    }
)
MAX_BYTES = 16_000_000
_TIMEOUT = 30.0
_UA = "PrimeDocumentary-providers/0.1"


class PreflightError(RuntimeError):
    pass


class ProviderError(RuntimeError):
    pass


class PaidOperationNotConfirmed(RuntimeError):
    """A paid/side-effect operation was attempted without explicit confirmation (rules/11)."""


def preflight(url: str) -> str:
    p = urlparse(url)
    if p.scheme != "https":
        raise PreflightError(f"scheme {p.scheme!r} not allowed (https only)")
    host = (p.hostname or "").lower()
    if host not in ALLOWED_HOSTS:
        raise PreflightError(f"host {host!r} not on the provider allowlist")
    return host


def require_confirmed(confirmed: bool, what: str) -> None:
    if not confirmed:
        raise PaidOperationNotConfirmed(
            f"{what}: refusing — paid/side-effect operation requires explicit owner "
            f"confirmation and a budget (rules/11). Pass confirmed=True only after approval."
        )


def _urllib_transport(method: str, url: str, headers: dict[str, str], body: bytes | None, timeout: float):
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (allowlisted)
            data = resp.read(MAX_BYTES + 1)
            ctype = resp.headers.get_content_type() if resp.headers else ""
            return resp.status, data, ctype
    except urllib.error.HTTPError as exc:
        try:
            data = exc.read(MAX_BYTES + 1)
        except Exception:  # pragma: no cover
            data = b""
        return exc.code, data, "application/json"


def request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json_body: Any | None = None,
    form_body: dict[str, str] | None = None,
    transport: Transport | None = None,
    timeout: float = _TIMEOUT,
) -> tuple[int, Any]:
    """Make an allowlisted request. Returns (status, parsed_json_or_text)."""
    preflight(url)
    h = {"User-Agent": _UA, "Accept": "application/json", **(headers or {})}
    body: bytes | None = None
    if json_body is not None:
        body = json.dumps(json_body).encode("utf-8")
        h.setdefault("Content-Type", "application/json")
    elif form_body is not None:
        body = urllib.parse.urlencode(form_body).encode("utf-8")
        h.setdefault("Content-Type", "application/x-www-form-urlencoded")
    transport = transport or _urllib_transport
    status, raw, _ctype = transport(method, url, h, body, timeout)
    if len(raw) > MAX_BYTES:
        raise ProviderError(f"response from {url} exceeds {MAX_BYTES} bytes")
    text = raw.decode("utf-8", errors="replace")
    try:
        parsed: Any = json.loads(text) if text else None
    except (json.JSONDecodeError, ValueError):
        parsed = text
    return status, parsed
