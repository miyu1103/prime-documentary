"""Provider-specific acquisition for the Miranda episode (decision 0002 §7).

Each provider turns a :class:`FetchResult` into a provider-NEUTRAL source record
that validates against ``schemas/source.schema.json``. Parsing is defensive: a
shape we don't recognize degrades to a still-valid record with a note, rather than
crashing the run (the published citation 384 U.S. 436 is real regardless of API).
"""
from __future__ import annotations

import json
from typing import Any

from .fetcher import FetchResult

# --- Acquisition targets (stable, deterministic, public) --------------------
# CourtListener cluster API for the Miranda opinion. The stable identifier is the
# reporter citation 384 U.S. 436 (docs/28 §9); cluster 107252 is CourtListener's
# access handle, verified 2026-06-14 by resolving the citation redirect
# (https://www.courtlistener.com/c/U.S./384/436/ -> /opinion/107252/miranda-v-arizona/).
# The REST API requires a token (401 otherwise); without one we degrade to a valid
# citation with no durable hash and QC warns (recheck before publish).
COURTLISTENER_CLUSTER_API = "https://www.courtlistener.com/api/rest/v4/clusters/107252/"
COURTLISTENER_OPINION_URL = "https://www.courtlistener.com/opinion/107252/miranda-v-arizona/"
# Oyez case record: October Term 1965, docket 759.
OYEZ_CASE_URL = "https://api.oyez.org/cases/1965/759"


def _safe_json(text: str) -> Any:
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return None


def build_courtlistener_source(result: FetchResult, source_id: str) -> dict[str, Any]:
    """Primary source: the U.S. Reports opinion (CourtListener cluster API)."""
    data = _safe_json(result.text) if result.ok else None
    reference = "https://www.courtlistener.com/opinion/107252/miranda-v-arizona/"
    publication_date = "1966-06-13"
    if isinstance(data, dict):
        absolute_url = data.get("absolute_url")
        if absolute_url:
            reference = f"https://www.courtlistener.com{absolute_url}"
        publication_date = data.get("date_filed") or publication_date

    note = "CourtListener cluster 107252 for 384 U.S. 436 (citation verified via /c/ redirect)."
    if not result.ok:
        note += (
            f" (live fetch returned HTTP {result.status}; the published citation remains "
            "valid but a durable content hash was not captured — add COURTLISTENER_TOKEN.)"
        )

    return {
        "schema_version": "1.0.0",
        "source_id": source_id,
        "title": "Miranda v. Arizona, 384 U.S. 436 (1966) — full opinion (CourtListener)",
        "author": "Supreme Court of the United States (opinion of the Court by Warren, C.J.)",
        "organization": "Free Law Project / CourtListener",
        "publication_date": publication_date,
        "accessed_at": result.accessed_at,
        "reference": reference,
        "source_type": "primary",
        "authority": 5,
        "directness": 5,
        "independence": 5,
        "recency": 5,
        "bias_or_interest": "Primary judicial record; CourtListener is a neutral redistributor.",
        "relevant_locations": [
            "Syllabus",
            "Opinion of the Court (Warren, C.J.)",
            "Dissents (Harlan, J.; White, J.)",
        ],
        "quotation_note": "Public-domain U.S. government work; short attributed quotes are safe.",
        "rights_note": "Opinion text is public domain. Cite CourtListener as the access source.",
        # Only a successful (2xx) response is a durable hash of the actual document; an
        # error body (e.g. a 401 JSON) must not masquerade as captured content.
        "content_hash": result.content_hash if result.ok else None,
        "notes": note,
    }


def build_oyez_source(result: FetchResult, source_id: str) -> dict[str, Any]:
    """Institutional corroborating source: Oyez case record."""
    data = _safe_json(result.text) if result.ok else None
    name = "Miranda v. Arizona"
    href = "https://www.oyez.org/cases/1965/759"
    if isinstance(data, dict):
        name = data.get("name") or name
        href = data.get("href") or href
        if href.startswith("https://api.oyez.org"):
            href = href.replace("https://api.oyez.org", "https://www.oyez.org")

    note = "Oyez case summary, decision and oral-argument record."
    if not result.ok:
        note += f" (live fetch returned HTTP {result.status}.)"

    return {
        "schema_version": "1.0.0",
        "source_id": source_id,
        "title": f"{name} — Oyez case record",
        "author": None,
        "organization": "Oyez (IIT Chicago-Kent College of Law / Cornell LII / Justia)",
        "publication_date": None,
        "accessed_at": result.accessed_at,
        "reference": href,
        "source_type": "institutional",
        "authority": 4,
        "directness": 3,
        "independence": 4,
        "recency": 4,
        "bias_or_interest": "Educational legal database; secondary summary of the primary record.",
        "relevant_locations": ["Facts of the case", "Question", "Conclusion"],
        "quotation_note": "Summarize; do not copy long passages.",
        "rights_note": "Metadata/summary reference only; do not redistribute full content.",
        "content_hash": result.content_hash if result.ok else None,
        "notes": note,
    }
