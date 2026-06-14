"""Egress preflight: scheme/host allowlist and size cap (docs/28 §7, §11).

Acquiring a URL is also a security boundary. Nothing is fetched unless it passes
here. The allowlist is intentionally narrow — the first channel only needs the
public legal-record sources named in decision 0002 §7.
"""
from __future__ import annotations

from urllib.parse import urlparse

# Only these hosts may be fetched. Widen deliberately, never silently.
ALLOWED_HOSTS: frozenset[str] = frozenset(
    {
        "www.courtlistener.com",
        "courtlistener.com",
        "api.oyez.org",
        "www.oyez.org",
        "oyez.org",
    }
)
ALLOWED_SCHEMES: frozenset[str] = frozenset({"https"})

# Hard byte cap per response (docs/28 §7 file-size limits).
MAX_RESPONSE_BYTES: int = 8_000_000


class PreflightError(RuntimeError):
    """A URL was rejected before any network call was made."""


def preflight(url: str) -> str:
    """Validate ``url`` and return its host, or raise :class:`PreflightError`.

    No network access happens here; this only inspects the URL string.
    """
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise PreflightError(
            f"scheme {parsed.scheme!r} not allowed (only {sorted(ALLOWED_SCHEMES)})"
        )
    host = (parsed.hostname or "").lower()
    if host not in ALLOWED_HOSTS:
        raise PreflightError(f"host {host!r} is not on the egress allowlist")
    return host
