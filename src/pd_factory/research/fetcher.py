"""Idempotent, budgeted, allowlisted HTTP GET for research acquisition.

Design (decision 0002 §10.4, docs/28):
- preflight() gates every URL (scheme/host/size).
- A disk cache keyed by sha256(url) makes fetches idempotent: a cached URL costs
  no network call and no budget (rules/11 — a retry must not duplicate cost).
- A BudgetLedger reservation gates *new* network calls.
- The Authorization header (CourtListener token) is NEVER written to cache, logs,
  or provenance (rules/03 secrets).
- The transport is injectable so tests never touch the network.
"""
from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from ..budget import BudgetLedger
from .preflight import MAX_RESPONSE_BYTES, PreflightError, preflight

# transport(url, headers, timeout) -> (status, body_bytes, content_type[, final_url])
Transport = Callable[[str, dict[str, str], float], "tuple"]

_USER_AGENT = "PrimeDocumentary-research/0.1 (+https://prime-documentary.local)"
_TIMEOUT_S = 30.0
# Cost units are "requests", gated by a request budget (not USD): these APIs are free
# but rate-limited, so we bound how many live calls one run may make.
_COST_PER_REQUEST = 1.0


class FetchError(RuntimeError):
    pass


@dataclass(frozen=True)
class FetchResult:
    url: str
    status: int
    content_type: str
    byte_len: int
    content_hash: str | None
    accessed_at: str
    from_cache: bool
    text: str
    final_url: str = ""

    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300

    @property
    def reference_url(self) -> str:
        """The URL a citation should point to (post-redirect when known)."""
        return self.final_url or self.url


def _cache_key(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def _urllib_transport(url: str, headers: dict[str, str], timeout: float) -> tuple[int, bytes, str, str]:
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (host allowlisted in preflight)
            body = resp.read(MAX_RESPONSE_BYTES + 1)
            ctype = resp.headers.get_content_type() if resp.headers else "application/octet-stream"
            final_url = resp.geturl() or url  # post-redirect URL (citation -> opinion)
            # The final URL must also be on the allowlist (a redirect can't escape it).
            preflight(final_url)
            return resp.status, body, ctype, final_url
    except urllib.error.HTTPError as exc:  # 4xx/5xx: capture status, no body trust
        body = b""
        try:
            body = exc.read(MAX_RESPONSE_BYTES + 1)
        except Exception:  # pragma: no cover - defensive
            pass
        return exc.code, body, "application/octet-stream", url


def fetch(
    url: str,
    *,
    accessed_at: str,
    token: str | None = None,
    cache_dir: Path,
    budget: BudgetLedger | None = None,
    transport: Transport | None = None,
    dry_run: bool = False,
) -> FetchResult:
    """Fetch ``url`` once. Returns a :class:`FetchResult`.

    Raises :class:`PreflightError` if the URL is not allowlisted, or
    :class:`FetchError` on oversize/dry-run-write violations.
    """
    host = preflight(url)  # raises before any side effect
    cache_dir = Path(cache_dir)
    cache_path = cache_dir / f"{_cache_key(url)}.json"

    if cache_path.exists():
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        return FetchResult(
            url=url,
            status=cached["status"],
            content_type=cached["content_type"],
            byte_len=cached["byte_len"],
            content_hash=cached["content_hash"],
            accessed_at=cached["accessed_at"],
            from_cache=True,
            text=cached["text"],
            final_url=cached.get("final_url", url),
        )

    if dry_run:
        # Dry-run must not perform external writes/reads (rules/11).
        raise FetchError(f"dry_run: refusing live fetch of {url} (no cache present)")

    if budget is not None:
        budget.reserve(_COST_PER_REQUEST)

    transport = transport or _urllib_transport
    # Auth header is built here and never persisted anywhere downstream.
    headers = {"User-Agent": _USER_AGENT, "Accept": "application/json, text/plain, */*"}
    if host.endswith("courtlistener.com") and token:
        headers["Authorization"] = f"Token {token}"

    out = transport(url, headers, _TIMEOUT_S)
    status, body, ctype = out[0], out[1], out[2]
    final_url = out[3] if len(out) > 3 else url

    if len(body) > MAX_RESPONSE_BYTES:
        raise FetchError(f"response from {url} exceeds {MAX_RESPONSE_BYTES} bytes")

    if budget is not None:
        budget.commit(_COST_PER_REQUEST)

    content_hash = "sha256:" + hashlib.sha256(body).hexdigest() if body else None
    text = body.decode("utf-8", errors="replace")

    cache_dir.mkdir(parents=True, exist_ok=True)
    # NB: never persist request headers / token.
    cache_path.write_text(
        json.dumps(
            {
                "url": url,
                "final_url": final_url,
                "status": status,
                "content_type": ctype,
                "byte_len": len(body),
                "content_hash": content_hash,
                "accessed_at": accessed_at,
                "text": text,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return FetchResult(
        url=url,
        status=status,
        content_type=ctype,
        byte_len=len(body),
        content_hash=content_hash,
        accessed_at=accessed_at,
        from_cache=False,
        text=text,
        final_url=final_url,
    )
