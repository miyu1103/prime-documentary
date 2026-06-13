"""Deterministic stage generators for the vertical-slice MVP.

No LLM, no network, no external calls. Each generator derives its output from
upstream artifacts only. Where real research/evidence does not exist yet, output
is an explicitly-flagged PLACEHOLDER and is never presented as a verified fact
(invariants 1, 10, 11). The final QC report marks such episodes not-publishable.
"""
from __future__ import annotations

from typing import Any, Callable

from .provenance import now_iso

WPS = 2.5  # ~150 words/minute narration pace, used for rough timing only.


def _words(text: str) -> int:
    return max(1, len(text.split()))


def _seconds(text: str, floor: float = 0.5) -> float:
    return round(max(floor, _words(text) / WPS), 2)


# -- generators ---------------------------------------------------------------
def gen_research_plan(episode_id: str, revision: str, up: dict, rev: dict) -> dict:
    topic = up["topic"]
    return {
        "research_plan_id": f"RP-{episode_id}",
        "episode_id": episode_id,
        "revision": revision,
        "central_question": topic["central_question"],
        "subquestions": [
            {"id": "SQ1", "question": f"What is the established account of: {topic['subject']}?", "importance": "critical"},
            {"id": "SQ2", "question": f"What is the strongest counter-evidence to the angle: {topic['angle']}?", "importance": "major"},
            {"id": "SQ3", "question": "What are the key numbers, dates, units and their sources?", "importance": "supporting"},
        ],
        "query_tracks": [
            {"type": "primary", "queries": [topic["subject"]]},
            {"type": "counterevidence", "queries": [f"criticism of {topic['angle']}"]},
            {"type": "numbers", "queries": ["official statistics", "primary dataset"]},
        ],
        "source_requirements": ["At least one primary or official source per critical claim."],
        "volatile_facts": [],
        "stop_conditions": [
            "Every critical subquestion has at least one independent source.",
            "No critical claim relies on a single non-independent source.",
        ],
        "provenance": {"producer": "pipeline:mvp", "derived_from": "topic"},
    }


def gen_sources(episode_id: str, revision: str, up: dict, rev: dict) -> list:
    # Placeholder registry: the MVP does not crawl the web. Real research must
    # replace these before any claim can be graded as supported.
    return [
        {
            "schema_version": "1.0.0",
            "source_id": "SRC-0001",
            "title": "PLACEHOLDER — replace with a real, verified source",
            "author": None,
            "organization": None,
            "publication_date": None,
            "accessed_at": now_iso(),
            "reference": "about:blank#placeholder",
            "source_type": "unknown",
            "authority": 1,
            "directness": 1,
            "independence": 1,
            "bias_or_interest": "Unknown — placeholder pending real research.",
            "relevant_locations": ["(pending)"],
            "rights_note": "No rights cleared. Placeholder only; not for publication.",
            "content_hash": None,
            "notes": "Auto-generated placeholder for vertical-slice architecture validation.",
        }
    ]


def gen_claims(episode_id: str, revision: str, up: dict, rev: dict) -> dict:
    topic = up["topic"]
    return {
        "schema_version": "1.0.0",
        "episode_id": episode_id,
        "revision": revision,
        "claims": [
            {
                "claim_id": "CLM-0001",
                "normalized_claim": f"Central claim about {topic['subject']} (pending verification).",
                "importance": "critical",
                "sensitivity": "low",
                "grade": "C",
                "source_ids": ["SRC-0001"],
                "evidence_locations": ["(pending)"],
                "counterevidence": [],
                "confidence": 0.2,
                "allowed_wording": [],
                "prohibited_wording": ["Stated as an established fact."],
                "temporal_scope": "",
                "geographic_scope": "",
                "units": "",
                "status": "needs_research",
                "notes": "Placeholder claim; not publishable until backed by a real source.",
            }
        ],
        "qc": {
            "critical_supported": False,
            "e_claims_in_script_allowed": False,
            "status": "warn",
            "findings": ["Critical claim CLM-0001 has no verified source (placeholder)."],
        },
    }


def gen_thesis(episode_id: str, revision: str, up: dict, rev: dict) -> dict:
    topic = up["topic"]
    return {
        "thesis_id": f"TH-{episode_id}",
        "episode_id": episode_id,
        "revision": revision,
        "common_belief": f"People assume {topic['subject']} is straightforward.",
        "hidden_structure": topic.get("surprise") or "A hidden system explains the surprise.",
        "final_thesis": f"{topic['viewer_promise']} This episode argues that the angle '{topic['angle']}' reframes how the subject should be understood.",
        "viewer_promise": topic["viewer_promise"],
        "stakes": topic.get("stakes") or "Why this matters to the viewer.",
        "counterargument": "The strongest opposing view must be addressed before publication.",
        "claim_ids": ["CLM-0001"],
        "risk_class": topic.get("risk_class", "R0"),
        "status": "draft",
    }


def gen_script(episode_id: str, revision: str, up: dict, rev: dict) -> dict:
    topic = up["topic"]
    thesis = up["thesis"]
    spans = [
        {
            "span_id": "SPN-0001",
            "text": topic["central_question"],
            "claim_ids": ["CLM-0001"],
            "narrative_function": "hook",
            "pronunciation_keys": [],
            "visual_intent": "Open on a concrete, specific detail.",
            "on_screen_text": [],
        },
        {
            "span_id": "SPN-0002",
            "text": thesis["final_thesis"],
            "claim_ids": ["CLM-0001"],
            "narrative_function": "thesis",
            "pronunciation_keys": [],
            "visual_intent": "Reveal the underlying system.",
            "on_screen_text": [],
        },
    ]
    total = round(sum(_words(s["text"]) for s in spans) / WPS, 2)
    return {
        "schema_version": "1.0.0",
        "episode_id": episode_id,
        "revision": revision,
        "language": "en",
        "thesis": thesis["final_thesis"],
        "viewer_promise": thesis["viewer_promise"],
        "chapters": [
            {
                "chapter_id": "CH01",
                "title": "Opening",
                "function": "Pose the question and state the thesis.",
                "span_ids": [s["span_id"] for s in spans],
            }
        ],
        "spans": spans,
        "estimated_duration_seconds": max(1.0, total),
        "qc_status": "warn",
    }


_VISUAL_MODE = {"hook": "object", "thesis": "diagram"}


def gen_scene_plan(episode_id: str, revision: str, up: dict, rev: dict) -> dict:
    script = up["script"]
    scenes = []
    for i, span in enumerate(script["spans"], start=1):
        scenes.append(
            {
                "scene_id": f"S{i:03d}",
                "script_span_ids": [span["span_id"]],
                "purpose": f"Visualize: {span['narrative_function']}.",
                "primary_claim_id": (span["claim_ids"][0] if span["claim_ids"] else None),
                "emotional_function": "curiosity",
                "visual_mode": _VISUAL_MODE.get(span["narrative_function"], "diagram"),
                "duration_seconds": _seconds(span["text"]),
                "priority": "A",
                "required_assets": ["hero shot"],
                "continuity_refs": [],
                "transition_in": "cut",
                "transition_out": "cut",
                "on_screen_text": [],
                "source_sensitivity": "low",
                "human_review_required": False,
                "fallback_visual": "Clean object close-up plus an SVG diagram.",
            }
        )
    return {
        "schema_version": "1.0.0",
        "episode_id": episode_id,
        "revision": revision,
        "scenes": scenes,
        "coverage": {"all_script_spans_mapped": True, "orphan_scenes": []},
    }


def gen_asset_plan(episode_id: str, revision: str, up: dict, rev: dict) -> dict:
    scene_plan = up["scene_plan"]
    requirements = []
    for i, scene in enumerate(scene_plan["scenes"], start=1):
        requirements.append(
            {
                "requirement_id": f"REQ-{i:03d}",
                "scene_id": scene["scene_id"],
                "shot_id": None,
                "visual_mode": scene["visual_mode"],
                "priority": "A",
                "candidate_count": 3,
                "continuity_refs": [],
                "rights_class": "generated_illustration",
                "fallback": scene["fallback_visual"],
            }
        )
    return {
        "asset_plan_id": f"AP-{episode_id}",
        "episode_id": episode_id,
        "revision": revision,
        "requirements": requirements,
    }


def gen_voice_plan(episode_id: str, revision: str, up: dict, rev: dict) -> dict:
    script = up["script"]
    chunks = []
    for i, span in enumerate(script["spans"], start=1):
        chunks.append(
            {
                "chunk_id": f"VC-{i:04d}",
                "span_ids": [span["span_id"]],
                "spoken_text": span["text"],
                "context_before": "",
                "context_after": "",
                "pronunciation_keys": [],
                "target_seconds": _seconds(span["text"], floor=0.2),
                "emotion": "neutral",
                "revision_risk": "low",
            }
        )
    return {
        "voice_plan_id": f"VP-{episode_id}",
        "episode_id": episode_id,
        "script_revision": rev.get("script", "v001"),
        "voice_profile": "narrator_default",
        "mode": "draft",
        "chunks": chunks,
    }


def gen_edit_plan(episode_id: str, revision: str, up: dict, rev: dict) -> dict:
    scene_plan = up["scene_plan"]
    asset_plan = up["asset_plan"]
    voice_plan = up["voice_plan"]
    req_by_scene: dict[str, list[str]] = {}
    for req in asset_plan["requirements"]:
        req_by_scene.setdefault(req["scene_id"], []).append(req["requirement_id"])
    chunk_by_span: dict[str, str] = {}
    for chunk in voice_plan["chunks"]:
        for span_id in chunk["span_ids"]:
            chunk_by_span[span_id] = chunk["chunk_id"]

    segments = []
    start = 0.0
    required: list[str] = []
    for i, scene in enumerate(scene_plan["scenes"], start=1):
        duration = float(scene["duration_seconds"])
        visual_ids = req_by_scene.get(scene["scene_id"], [])
        voice_ids = [chunk_by_span[s] for s in scene["script_span_ids"] if s in chunk_by_span]
        segments.append(
            {
                "segment_id": f"SEG-{i:03d}",
                "scene_id": scene["scene_id"],
                "start_seconds": round(start, 2),
                "duration_seconds": duration,
                "visual_asset_ids": visual_ids,
                "voice_chunk_ids": voice_ids,
                "motion_template": "ken_burns_subtle",
                "music_cue_ids": [],
                "markers": [],
            }
        )
        required.extend(visual_ids)
        required.extend(voice_ids)
        start += duration
    return {
        "edit_plan_id": f"EP-{episode_id}",
        "episode_id": episode_id,
        "revision": revision,
        "timeline": {
            "fps": 30,
            "width": 1920,
            "height": 1080,
            "start_timecode": "00:00:00:00",
            "template_version": "v1",
        },
        "segments": segments,
        "required_artifacts": sorted(set(required)),
    }


def gen_qc_report(episode_id: str, revision: str, up: dict, rev: dict) -> dict:
    claims = up["claims"]
    scene_plan = up["scene_plan"]
    findings = []
    if not claims["qc"]["critical_supported"]:
        findings.append(
            {
                "finding_id": "F001",
                "severity": "S2",
                "code": "CLAIM_UNSUPPORTED",
                "message": "Critical claim(s) lack a verified independent source; the episode is not publishable until real research replaces placeholders.",
                "location": "01_research/claims",
                "action": "research",
                "related_ids": [c["claim_id"] for c in claims["claims"]],
            }
        )
    if any(s["source_type"] == "unknown" for s in up.get("sources", [])):
        findings.append(
            {
                "finding_id": "F002",
                "severity": "S1",
                "code": "SOURCES_PLACEHOLDER",
                "message": "Source registry contains placeholder sources only.",
                "location": "01_research/sources",
                "action": "research",
                "related_ids": ["SRC-0001"],
            }
        )
    coverage_ok = scene_plan["coverage"]["all_script_spans_mapped"]
    if not coverage_ok:
        findings.append(
            {
                "finding_id": "F003",
                "severity": "S3",
                "code": "SCENE_COVERAGE_GAP",
                "message": "Not every script span is mapped to a scene.",
                "location": "04_scenes/scene_plan",
                "action": "regenerate",
                "related_ids": [],
            }
        )

    if any(f["action"] == "block" or f["severity"] in ("S4", "S5") for f in findings):
        result = "blocked"
    elif any(f["severity"] == "S3" for f in findings):
        result = "fail"
    elif findings:
        result = "pass_with_warnings"
    else:
        result = "pass"

    return {
        "qc_report_id": f"QC-{episode_id}-{revision}",
        "target_type": "episode_vertical_slice",
        "target_id": episode_id,
        "target_revision": revision,
        "gate": "vertical_slice_v1",
        "result": result,
        "findings": findings,
        "created_at": now_iso(),
        "validator_versions": {"pipeline": "mvp-1"},
    }


GeneratorFn = Callable[[str, str, dict, dict], Any]

GENERATORS: dict[str, GeneratorFn] = {
    "research_plan": gen_research_plan,
    "sources": gen_sources,
    "claims": gen_claims,
    "thesis": gen_thesis,
    "script": gen_script,
    "scene_plan": gen_scene_plan,
    "asset_plan": gen_asset_plan,
    "voice_plan": gen_voice_plan,
    "edit_plan": gen_edit_plan,
    "qc_report": gen_qc_report,
}
