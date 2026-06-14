"""Orchestrate Miranda research: fetch sources, build registry + graded claim ledger.

This replaces the placeholder ``gen_sources`` / ``gen_claims`` for PD-2026-001 with
real, cited research. Claims are authored from the primary opinion (384 U.S. 436)
and graded by source quality; the live fetch supplies durable citation metadata
(accessed_at, content_hash) per docs/28 §9. Fetched text is untrusted data.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..budget import BudgetLedger
from .fetcher import FetchResult, Transport, fetch
from .providers import (
    COURTLISTENER_CLUSTER_API,
    OYEZ_CASE_URL,
    build_courtlistener_source,
    build_oyez_source,
)

CL_SOURCE_ID = "SRC-0001"
OYEZ_SOURCE_ID = "SRC-0002"


def acquire(
    *,
    accessed_at: str,
    token: str | None,
    cache_dir: Path,
    budget: BudgetLedger | None = None,
    transport: Transport | None = None,
    dry_run: bool = False,
) -> tuple[FetchResult, FetchResult]:
    """Fetch the CourtListener opinion record and the Oyez case record."""
    cl = fetch(
        COURTLISTENER_CLUSTER_API,
        accessed_at=accessed_at,
        token=token,
        cache_dir=cache_dir,
        budget=budget,
        transport=transport,
        dry_run=dry_run,
    )
    oyez = fetch(
        OYEZ_CASE_URL,
        accessed_at=accessed_at,
        token=None,  # Oyez needs no auth
        cache_dir=cache_dir,
        budget=budget,
        transport=transport,
        dry_run=dry_run,
    )
    return cl, oyez


def build_sources(cl: FetchResult, oyez: FetchResult) -> list[dict[str, Any]]:
    return [
        build_courtlistener_source(cl, CL_SOURCE_ID),
        build_oyez_source(oyez, OYEZ_SOURCE_ID),
    ]


def build_research_plan(episode_id: str, revision: str) -> dict[str, Any]:
    return {
        "research_plan_id": f"RP-{episode_id}",
        "episode_id": episode_id,
        "revision": revision,
        "central_question": (
            "Why must US police read the Miranda warning, and what system does it protect?"
        ),
        "subquestions": [
            {"id": "SQ1", "question": "What exactly did Miranda v. Arizona hold?", "importance": "critical"},
            {"id": "SQ2", "question": "On what constitutional basis (which Amendment)?", "importance": "critical"},
            {"id": "SQ3", "question": "What are the required warnings, in substance?", "importance": "major"},
            {"id": "SQ4", "question": "Which cases were consolidated and who decided it?", "importance": "major"},
            {"id": "SQ5", "question": "What happened to Ernesto Miranda himself?", "importance": "supporting"},
            {"id": "SQ6", "question": "How is the holding applied today (the 'system')?", "importance": "supporting"},
        ],
        "query_tracks": [
            {"type": "primary", "queries": ["384 U.S. 436", "Miranda v. Arizona full opinion"]},
            {"type": "counterevidence", "queries": ["Miranda dissent Harlan White", "criticism of Miranda warning"]},
            {"type": "chronology", "queries": ["Miranda arrest 1963", "Miranda decided June 13 1966", "Miranda retrial"]},
            {"type": "current", "queries": ["Miranda warning current law", "Dickerson v. United States 2000"]},
        ],
        "source_requirements": [
            "Each critical claim cites the primary opinion (384 U.S. 436).",
            "At least one institutional source corroborates the holding.",
        ],
        "volatile_facts": [],
        "stop_conditions": [
            "Every critical subquestion is answered by the primary opinion.",
            "No critical claim relies on a single non-independent secondary source.",
        ],
        "provenance": {"producer": "research:miranda-adapter", "derived_from": "topic"},
    }


def build_claim_ledger(episode_id: str, revision: str, sources: list[dict[str, Any]]) -> dict[str, Any]:
    """Author the graded claim ledger and run research QC against the sources."""
    claims: list[dict[str, Any]] = [
        {
            "claim_id": "CLM-0001",
            "normalized_claim": (
                "In Miranda v. Arizona (1966) the Supreme Court held that the prosecution may not "
                "use statements from custodial interrogation unless it shows that procedural "
                "safeguards effective to secure the Fifth Amendment privilege were used."
            ),
            "importance": "critical",
            "sensitivity": "low",
            "grade": "A",
            "source_ids": [CL_SOURCE_ID],
            "evidence_locations": ["Opinion of the Court (Warren, C.J.), holding"],
            "counterevidence": ["Harlan, J. and White, J. dissented from the rule's scope."],
            "confidence": 0.99,
            "allowed_wording": [
                "The Court ruled that confessions from custodial questioning can't be used unless the suspect was first warned of their rights."
            ],
            "prohibited_wording": [
                "The Court banned all police interrogation.",
                "Miranda made confessions illegal.",
            ],
            "temporal_scope": "1966-present",
            "geographic_scope": "United States",
            "units": "",
            "status": "approved",
            "notes": "Core holding; primary source.",
        },
        {
            "claim_id": "CLM-0002",
            "normalized_claim": (
                "Miranda v. Arizona was decided on June 13, 1966 by a 5-4 vote, with the majority "
                "opinion written by Chief Justice Earl Warren."
            ),
            "importance": "critical",
            "sensitivity": "low",
            "grade": "A",
            "source_ids": [CL_SOURCE_ID, OYEZ_SOURCE_ID],
            "evidence_locations": ["Syllabus / decision date", "Oyez: decision"],
            "counterevidence": [],
            "confidence": 0.98,
            "allowed_wording": ["In a narrow 5-4 decision in 1966, Chief Justice Warren wrote for the Court."],
            "prohibited_wording": ["The decision was unanimous."],
            "temporal_scope": "1966",
            "geographic_scope": "United States",
            "units": "",
            "status": "approved",
            "notes": "Date/vote/author.",
        },
        {
            "claim_id": "CLM-0003",
            "normalized_claim": (
                "The decision rests on the Fifth Amendment privilege against compelled self-incrimination."
            ),
            "importance": "major",
            "sensitivity": "low",
            "grade": "A",
            "source_ids": [CL_SOURCE_ID],
            "evidence_locations": ["Opinion of the Court, constitutional basis"],
            "counterevidence": [],
            "confidence": 0.97,
            "allowed_wording": ["The ruling is grounded in the Fifth Amendment right against self-incrimination."],
            "prohibited_wording": ["The ruling is based on the Second Amendment."],
            "temporal_scope": "1966-present",
            "geographic_scope": "United States",
            "units": "",
            "status": "approved",
            "notes": "Constitutional basis.",
        },
        {
            "claim_id": "CLM-0004",
            "normalized_claim": (
                "Before custodial interrogation a suspect must be warned: of the right to remain silent; "
                "that anything said can be used against them in court; of the right to an attorney; and "
                "that if they cannot afford one, an attorney will be appointed."
            ),
            "importance": "major",
            "sensitivity": "low",
            "grade": "A",
            "source_ids": [CL_SOURCE_ID],
            "evidence_locations": ["Opinion of the Court, required warnings"],
            "counterevidence": [],
            "confidence": 0.98,
            "allowed_wording": ["The Court spelled out the four warnings police must give."],
            "prohibited_wording": ["The warning must be read word-for-word from a single official script."],
            "temporal_scope": "1966-present",
            "geographic_scope": "United States",
            "units": "",
            "status": "approved",
            "notes": "The four warnings.",
        },
        {
            "claim_id": "CLM-0005",
            "normalized_claim": (
                "The 1966 decision resolved four consolidated cases: Miranda v. Arizona, Vignera v. "
                "New York, Westover v. United States, and California v. Stewart."
            ),
            "importance": "major",
            "sensitivity": "low",
            "grade": "A",
            "source_ids": [CL_SOURCE_ID],
            "evidence_locations": ["Syllabus, consolidated cases"],
            "counterevidence": [],
            "confidence": 0.95,
            "allowed_wording": ["Miranda actually bundled four separate cases into one ruling."],
            "prohibited_wording": [],
            "temporal_scope": "1966",
            "geographic_scope": "United States",
            "units": "",
            "status": "approved",
            "notes": "Consolidated cases.",
        },
        {
            "claim_id": "CLM-0006",
            "normalized_claim": (
                "Ernesto Miranda was arrested in Phoenix, Arizona in 1963 and confessed during "
                "interrogation without being told of his rights; the Supreme Court reversed that "
                "conviction, and he was later retried and convicted again on other evidence."
            ),
            "importance": "supporting",
            "sensitivity": "medium",
            "grade": "B",
            "source_ids": [CL_SOURCE_ID, OYEZ_SOURCE_ID],
            "evidence_locations": ["Opinion, facts (No. 759)", "Oyez: facts of the case"],
            "counterevidence": [],
            "confidence": 0.92,
            "allowed_wording": [
                "Miranda's original conviction was overturned; at a new trial he was convicted again on other evidence."
            ],
            "prohibited_wording": [
                "Miranda was found innocent.",
                "Miranda went free because of the ruling.",
            ],
            "temporal_scope": "1963-1967",
            "geographic_scope": "Arizona, United States",
            "units": "",
            "status": "approved",
            "notes": "Real person; state charged/convicted status accurately (docs/32). Not exonerated by the ruling.",
        },
        {
            "claim_id": "CLM-0007",
            "normalized_claim": (
                "Justices Harlan and White each wrote dissents arguing the majority's rule went beyond "
                "what the Constitution and precedent required."
            ),
            "importance": "supporting",
            "sensitivity": "low",
            "grade": "A",
            "source_ids": [CL_SOURCE_ID],
            "evidence_locations": ["Dissenting opinions (Harlan, J.; White, J.)"],
            "counterevidence": [],
            "confidence": 0.95,
            "allowed_wording": ["Four justices dissented, warning the rule would hamper law enforcement."],
            "prohibited_wording": [],
            "temporal_scope": "1966",
            "geographic_scope": "United States",
            "units": "",
            "status": "approved",
            "notes": "Dissents (balance).",
        },
        {
            "claim_id": "CLM-0008",
            "normalized_claim": (
                "The required advisement became known as the 'Miranda warning' and is now a routine "
                "part of US custodial arrests."
            ),
            "importance": "context",
            "sensitivity": "low",
            "grade": "B",
            "source_ids": [OYEZ_SOURCE_ID],
            "evidence_locations": ["Oyez: significance / conclusion"],
            "counterevidence": [],
            "confidence": 0.9,
            "allowed_wording": ["That scripted advisement is what we now call the Miranda warning."],
            "prohibited_wording": [],
            "temporal_scope": "1966-present",
            "geographic_scope": "United States",
            "units": "",
            "status": "approved",
            "notes": "The 'system' payoff / naming.",
        },
    ]

    qc = compute_qc(claims, sources)
    return {
        "schema_version": "1.0.0",
        "episode_id": episode_id,
        "revision": revision,
        "claims": claims,
        "qc": qc,
    }


def compute_qc(claims: list[dict[str, Any]], sources: list[dict[str, Any]]) -> dict[str, Any]:
    """Critical claims must each cite a direct, well-graded source (rules/15, docs/32)."""
    by_id = {s["source_id"]: s for s in sources}
    findings: list[str] = []
    critical_supported = True
    for c in claims:
        if c["importance"] != "critical":
            continue
        cited = [by_id[sid] for sid in c["source_ids"] if sid in by_id]
        strong = [s for s in cited if s["directness"] >= 4]
        if not strong or c["grade"] not in {"A", "B"}:
            critical_supported = False
            findings.append(f"{c['claim_id']}: no direct, well-graded source.")

    # Note (don't fail) if a cited source's content could not be fetched live.
    for s in sources:
        if s.get("content_hash") is None:
            findings.append(
                f"{s['source_id']}: live content not captured (no durable hash); recheck before publish."
            )

    status = "pass" if (critical_supported and not findings) else ("warn" if critical_supported else "fail")
    return {
        "critical_supported": critical_supported,
        "e_claims_in_script_allowed": False,
        "status": status,
        "findings": findings,
    }
