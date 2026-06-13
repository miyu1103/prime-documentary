"""Treat fetched bytes as untrusted DATA (rules/13, docs/28 §7, §8).

We never execute, eval, or follow instructions found inside fetched content. These
helpers exist only to (a) flatten markup into plain text for excerpting and (b)
*flag* (not act on) text that looks like an embedded instruction, so reviewers can
see it. The system's defense is structural: source text is never routed to a
shell, tool call, or system prompt.
"""
from __future__ import annotations

import html
import re

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")

# Patterns that, if present in source text, are logged as suspicious but NEVER obeyed.
_INJECTION_MARKERS = (
    "ignore previous",
    "ignore the above",
    "disregard your instructions",
    "system prompt",
    "you are now",
    "run the following",
    "execute this",
    "api key",
    "password",
)


def flatten_html(raw: str) -> str:
    """Strip tags and collapse whitespace; returns plain text. No execution."""
    text = _TAG_RE.sub(" ", raw)
    text = html.unescape(text)
    return _WS_RE.sub(" ", text).strip()


def excerpt(text: str, max_len: int = 600) -> str:
    """Bound an evidence excerpt (docs/28 §8: pass excerpts, not full text)."""
    text = text.strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def scan_for_injection(text: str) -> list[str]:
    """Return any embedded-instruction markers found. For logging/review ONLY."""
    low = text.lower()
    return [m for m in _INJECTION_MARKERS if m in low]
