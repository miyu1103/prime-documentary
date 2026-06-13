"""Application layer for the minimal "theme -> pipeline -> view" studio UI.

This is the thin orchestration the owner asked for: a human types a theme,
clicks run, and sees the resulting script / scene plan / QC verdict. It only
composes the existing reference core:

    init_episode_from_theme  -> seed an episode workspace from a theme
    run_pipeline             -> the existing vertical-slice orchestrator
    EpisodeView              -> a read-only projection for rendering

Safety properties preserved (no new capability is introduced here):
- No network, no LLM, no paid calls, no upload — same as the demo pipeline.
- The generators stay deterministic stubs; placeholders remain explicit and the
  QC gate still reports the episode as not-publishable until real research runs.
- Clicking "run" only clears the local *screening* gate so the pipeline may
  execute on a throwaway workspace under runs/. It is NOT a portfolio approval
  and NOT a publication approval; those human gates are untouched (nothing here
  publishes, and topic.status stays "candidate").
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .episode_repo import EpisodeRepo, EpisodeRepoError
from .pipeline import SCHEMA_DIR, run_pipeline
from .provenance import now_iso
from .schema_validation import validate_data

MIN_THEME_LENGTH = 3
MAX_THEME_LENGTH = 200


class StudioError(RuntimeError):
    """A user-facing problem (e.g. an unusable theme). Safe to show verbatim."""


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "episode"


def _seq3(text: str) -> str:
    """Deterministic 3-digit sequence derived from the theme (000-999)."""
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"{int(digest[:6], 16) % 1000:03d}"


def build_topic(theme: str, *, now: datetime | None = None) -> dict[str, Any]:
    """Build a schema-valid topic *brief* from a free-text theme.

    The brief is a planning seed, not researched fact: scores are zero (no demand
    analysis was done) and status is "candidate". The pipeline's deterministic
    generators turn it into explicitly-flagged placeholders downstream.
    """
    theme = theme.strip()
    if len(theme) < MIN_THEME_LENGTH:
        raise StudioError(f"テーマは{MIN_THEME_LENGTH}文字以上で入力してください。")
    if len(theme) > MAX_THEME_LENGTH:
        raise StudioError(f"テーマは{MAX_THEME_LENGTH}文字以内で入力してください。")
    now = now or datetime.now(timezone.utc)
    seq = _seq3(theme)
    return {
        "schema_version": "1.0.0",
        "topic_id": f"TOP-{now:%Y%m%d}-{seq}",
        "subject": theme,
        "angle": "hidden system",
        "central_question": f"What hidden system explains the truth behind: {theme}?",
        "viewer_promise": (
            f"The viewer will understand the hidden chain of decisions and "
            f"incentives behind {theme}."
        ),
        "surprise": "The visible thing matters less than the system that produced it.",
        "stakes": "The same system shapes choices the viewer makes every day.",
        "target_audience": "English-speaking general knowledge and documentary viewers",
        "differentiation": "Connects the parts into one causal narrative.",
        # No demand/quality scoring was performed for a free-text seed; report zeros
        # rather than invent numbers (invariant: never fabricate unverified facts).
        "scores": {
            "demand": 0, "clickability": 0, "retention": 0, "evergreen": 0,
            "differentiation": 0, "visual": 0, "sources": 0, "series": 0,
            "monetization": 0, "efficiency": 0, "risk_deduction": 0, "total": 0,
        },
        "risk_class": "R0",
        "recommendation": "candidate",
        "status": "candidate",
    }


def init_episode_from_theme(target_dir: Path, theme: str, *, now: datetime | None = None) -> EpisodeRepo:
    """Seed a fresh episode workspace (00_topic + manifest) from a theme.

    Refuses to clobber a non-empty target. The manifest is created in state
    "approved" so the existing pipeline may run locally; see the module docstring
    for why this is a screening clearance, not a portfolio/publication approval.
    """
    target_dir = Path(target_dir)
    if target_dir.exists() and any(target_dir.iterdir()):
        raise EpisodeRepoError(f"target episode dir is not empty: {target_dir}")
    topic = build_topic(theme, now=now)
    validate_data(topic, SCHEMA_DIR / "topic.schema.json")

    (target_dir / "00_topic").mkdir(parents=True, exist_ok=True)
    (target_dir / "00_topic" / "topic.v001.json").write_text(
        json.dumps(topic, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    slug = slugify(topic["subject"])
    seq = topic["topic_id"].rsplit("-", 1)[-1]
    created = (now or datetime.now(timezone.utc)).strftime("%Y")
    manifest = {
        "schema_version": "1.0.0",
        "episode_id": f"PD-{created}-{seq}-{slug}",
        "topic_id": topic["topic_id"],
        "slug": slug,
        "title_working": topic["subject"],
        "state": "approved",
        "risk_class": topic["risk_class"],
        "production_tier": "B",
        "autonomy_level": 3,
        "target_language": "en",
        "target_duration_minutes": 24,
        "active_revisions": {"topic": "v001"},
        "artifacts": [],
        "approvals": [],
        "costs": {
            "estimated": {"amount": 0, "currency": "USD"},
            "actual": {"amount": 0, "currency": "USD"},
            "soft_limit": {"amount": 100, "currency": "USD"},
            "hard_limit": {"amount": 200, "currency": "USD"},
        },
        "warnings": [],
        "blockers": [],
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    repo = EpisodeRepo(target_dir)
    repo.write_manifest(manifest)
    return repo


@dataclass
class EpisodeView:
    """Read-only projection of a finished run, ready for rendering."""

    episode_id: str
    theme: str
    final_state: str
    produced: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    thesis: dict[str, Any] = field(default_factory=dict)
    script: dict[str, Any] = field(default_factory=dict)
    scene_plan: dict[str, Any] = field(default_factory=dict)
    qc: dict[str, Any] = field(default_factory=dict)


def _read_active(repo: EpisodeRepo, manifest: dict, name: str, folder: str, stem: str) -> dict:
    rev = manifest["active_revisions"].get(name)
    if rev is None:
        return {}
    return repo.read_artifact(folder, stem, rev)


def create_and_run(runs_dir: Path, theme: str, *, now: datetime | None = None) -> EpisodeView:
    """Seed an isolated episode under runs_dir, run the pipeline, and project it.

    Each call gets its own timestamped workspace so concurrent themes never
    collide and nothing is overwritten.
    """
    now = now or datetime.now(timezone.utc)
    slug = slugify(theme.strip()) if theme.strip() else "episode"
    workspace = Path(runs_dir) / f"{slug}-{now:%Y%m%d-%H%M%S-%f}"
    repo = init_episode_from_theme(workspace, theme, now=now)
    result = run_pipeline(repo)
    manifest = repo.read_manifest()
    return EpisodeView(
        episode_id=result.episode_id,
        theme=theme.strip(),
        final_state=result.final_state,
        produced=result.by_action("produced"),
        skipped=result.by_action("skipped"),
        thesis=_read_active(repo, manifest, "thesis", "02_thesis", "thesis"),
        script=_read_active(repo, manifest, "script", "03_script", "script.annotated"),
        scene_plan=_read_active(repo, manifest, "scene_plan", "04_scenes", "scene_plan"),
        qc=_read_active(repo, manifest, "qc_report", "08_qc", "qc_report"),
    )
