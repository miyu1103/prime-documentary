"""Vertical-slice pipeline orchestrator.

Composes the reference-core invariants into a runnable chain:

    topic -> research_plan -> sources -> claims -> thesis -> script
          -> scene_plan -> asset_plan -> voice_plan -> edit_plan -> qc_report

Properties demonstrated:
- Immutable, revisioned artifacts with provenance + checksums (invariants 6, 7).
- Per-stage JSON Schema validation (invariant 13 is a separate gate; this is shape).
- Idempotent resume: an up-to-date stage is skipped (invariant 8).
- Partial rerun + downstream invalidation: a stage's idempotency key includes its
  upstream input revisions, so a changed upstream forces dependents to recompute
  (invariant 12).
- No network, no LLM, no paid calls, no upload.
"""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .budget import BudgetLedger, BudgetPolicy
from .episode_repo import EpisodeRepo, EpisodeRepoError, next_revision
from .generators import GENERATORS
from .idempotency import make_idempotency_key
from .provenance import make_provenance
from .schema_validation import validate_data

CONFIG_REVISION = "pipeline-mvp-1"
PRODUCER = "pipeline:mvp"
STAGE_COST_USD = 0.0  # local compute only

# On-disk manifest state uses the reconciled superset enum (audit gap G1, resolved
# 2026-06-13) that now matches both schemas/episode-manifest.schema.json and the
# code-level EpisodeState in domain.py.
MANIFEST_STATE_ORDER = [
    "idea", "screening", "approved", "pre_research", "researching", "research_ready",
    "thesis_ready", "outline_ready", "script_draft", "script_review", "script_verified",
    "scene_planned", "asset_plan_ready", "assets_generating", "assets_ready",
    "audio_generating", "audio_ready", "voice_ready", "music_ready",
    "edit_assembly", "edit_review", "finalizing", "package_ready", "publish_approved",
    "uploading", "scheduled", "published", "analytics_active", "analytics_reviewed",
    "archived",
]
_READY_FOR_RESEARCH = MANIFEST_STATE_ORDER.index("approved")


@dataclass(frozen=True)
class StageSpec:
    name: str
    folder: str
    stem: str
    schema_file: str
    inputs: tuple[str, ...]
    is_list: bool = False
    # Furthest manifest state this stage can justify (None = no advance).
    state: str | None = None


SCHEMA_DIR = Path(__file__).resolve().parents[2] / "schemas"

STAGES: tuple[StageSpec, ...] = (
    StageSpec("research_plan", "01_research", "research_plan", "research-plan.schema.json", ("topic",), state="researching"),
    StageSpec("sources", "01_research", "sources", "source.schema.json", ("research_plan",), is_list=True, state="researching"),
    StageSpec("claims", "01_research", "claims", "claim-ledger.schema.json", ("topic", "sources", "research_plan"), state="research_ready"),
    StageSpec("thesis", "02_thesis", "thesis", "thesis.schema.json", ("topic", "claims"), state="thesis_ready"),
    StageSpec("script", "03_script", "script.annotated", "script-annotated.schema.json", ("topic", "thesis", "claims"), state="script_draft"),
    StageSpec("scene_plan", "04_scenes", "scene_plan", "scene-plan.schema.json", ("script",)),
    StageSpec("asset_plan", "05_assets", "asset_plan", "asset-plan.schema.json", ("scene_plan",)),
    StageSpec("voice_plan", "06_audio", "voice_plan", "voice-plan.schema.json", ("script",)),
    StageSpec("edit_plan", "07_edit", "edit_plan", "edit-plan.schema.json", ("scene_plan", "asset_plan", "voice_plan")),
    StageSpec("qc_report", "08_qc", "qc_report", "qc-report.schema.json", ("claims", "script", "scene_plan", "sources")),
)

_STAGE_BY_NAME = {s.name: s for s in STAGES}
# Folder/stem to locate any artifact_type (topic included) for reading inputs.
_LOCATION: dict[str, tuple[str, str]] = {"topic": ("00_topic", "topic")}
_LOCATION.update({s.name: (s.folder, s.stem) for s in STAGES})


class PipelineError(RuntimeError):
    pass


def _validate(spec: StageSpec, data: Any) -> None:
    schema_path = SCHEMA_DIR / spec.schema_file
    if spec.is_list:
        if not isinstance(data, list):
            raise PipelineError(f"{spec.name}: expected a list artifact")
        for item in data:
            validate_data(item, schema_path)
    else:
        validate_data(data, schema_path)


def _advance_state(manifest: dict, target: str | None) -> str | None:
    if target is None:
        return None
    current = manifest["state"]
    if MANIFEST_STATE_ORDER.index(target) > MANIFEST_STATE_ORDER.index(current):
        manifest["state"] = target
        return target
    return None


def _register_artifact(manifest: dict, *, episode_id: str, atype: str, revision: str, uri: str, checksum: str) -> None:
    for entry in manifest["artifacts"]:
        if entry["artifact_type"] == atype and entry["status"] == "candidate":
            entry["status"] = "superseded"
    manifest["artifacts"].append(
        {
            "artifact_id": f"{episode_id}:{atype}:{revision}",
            "artifact_type": atype,
            "revision": revision,
            "uri": uri,
            "checksum": checksum,
            "status": "candidate",
        }
    )


@dataclass
class StageResult:
    name: str
    action: str  # "produced" | "skipped"
    revision: str
    checksum: str | None = None
    idempotency_key: str | None = None


@dataclass
class RunResult:
    episode_id: str
    final_state: str
    results: list[StageResult] = field(default_factory=list)

    def by_action(self, action: str) -> list[str]:
        return [r.name for r in self.results if r.action == action]


def run_pipeline(
    repo: EpisodeRepo,
    *,
    from_stage: str | None = None,
    force: bool = False,
    actor: str = PRODUCER,
) -> RunResult:
    manifest = repo.read_manifest()
    episode_id = manifest["episode_id"]

    if MANIFEST_STATE_ORDER.index(manifest["state"]) < _READY_FOR_RESEARCH:
        raise PipelineError(
            f"episode {episode_id} is in state '{manifest['state']}'; the topic "
            "approval gate must be cleared (state 'approved' or later) before the "
            "pipeline may run. The pipeline never self-approves a topic (invariant: "
            "portfolio approval is a human gate)."
        )

    if from_stage is not None and from_stage not in _STAGE_BY_NAME:
        raise PipelineError(f"unknown stage: {from_stage}")

    active: dict[str, str] = dict(manifest["active_revisions"])
    costs = manifest["costs"]
    ledger = BudgetLedger(
        BudgetPolicy(
            soft_limit=float(costs["soft_limit"]["amount"]),
            hard_limit=float(costs["hard_limit"]["amount"]),
        ),
        committed=float(costs["actual"]["amount"]),
    )

    forced = False
    result = RunResult(episode_id=episode_id, final_state=manifest["state"])

    for spec in STAGES:
        if from_stage is not None and spec.name == from_stage:
            forced = True
        stage_force = force or forced

        # Resolve inputs from the *current* active revisions (downstream invalidation).
        input_revisions: dict[str, str] = {}
        up_data: dict[str, Any] = {}
        for dep in spec.inputs:
            if dep not in active:
                raise PipelineError(
                    f"stage '{spec.name}' requires input '{dep}', which has no active "
                    "revision yet. Run the pipeline from the start first."
                )
            input_revisions[dep] = active[dep]
            folder, stem = _LOCATION[dep]
            up_data[dep] = repo.read_artifact(folder, stem, active[dep])

        key = make_idempotency_key(
            stage=spec.name,
            episode_id=episode_id,
            input_revisions=[f"{k}:{v}" for k, v in input_revisions.items()],
            config_revision=CONFIG_REVISION,
        )

        current_rev = active.get(spec.name)
        if not stage_force and current_rev is not None and repo.artifact_exists(spec.folder, spec.stem, current_rev):
            prov = repo.read_provenance(spec.folder, spec.stem, current_rev)
            if prov is not None and prov.get("idempotency_key") == key:
                repo.append_event(
                    {"type": "stage", "stage": spec.name, "episode_id": episode_id,
                     "revision": current_rev, "action": "skipped", "idempotency_key": key}
                )
                result.results.append(StageResult(spec.name, "skipped", current_rev, idempotency_key=key))
                continue

        # Produce a new immutable revision.
        revision = next_revision(repo.existing_revisions(spec.folder, spec.stem))
        data = GENERATORS[spec.name](episode_id, revision, up_data, input_revisions)
        _validate(spec, data)

        ledger.reserve(STAGE_COST_USD)
        ledger.commit(STAGE_COST_USD)

        artifact_id = f"{episode_id}:{spec.name}:{revision}"
        # Provisional checksum for provenance; repo recomputes the authoritative one.
        prov = make_provenance(
            artifact_id=artifact_id, artifact_type=spec.name, revision=revision,
            producer=actor, input_revisions=input_revisions, idempotency_key=key,
            checksum="", cost_amount=STAGE_COST_USD, cost_currency="USD",
        )
        uri, checksum = repo.write_artifact(
            folder=spec.folder, stem=spec.stem, revision=revision, data=data, provenance={**prov, "checksum": "pending"}
        )
        # Rewrite provenance with the authoritative checksum (the artifact file itself
        # is immutable; the sidecar is operational metadata, not a graded artifact).
        prov["checksum"] = checksum
        (repo.root / spec.folder / f"{spec.stem}.{revision}.meta.json").write_text(
            json.dumps(prov, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        active[spec.name] = revision
        _register_artifact(manifest, episode_id=episode_id, atype=spec.name, revision=revision, uri=uri, checksum=checksum)
        advanced = _advance_state(manifest, spec.state)
        repo.append_event(
            {"type": "stage", "stage": spec.name, "episode_id": episode_id, "revision": revision,
             "action": "produced", "idempotency_key": key, "checksum": checksum,
             "input_revisions": input_revisions, "cost_usd": STAGE_COST_USD}
        )
        if advanced is not None:
            repo.append_event(
                {"type": "state", "episode_id": episode_id, "to": advanced,
                 "reason": f"stage {spec.name} produced", "actor": actor}
            )
        result.results.append(StageResult(spec.name, "produced", revision, checksum=checksum, idempotency_key=key))

    manifest["active_revisions"] = active
    manifest["costs"]["actual"] = {"amount": round(ledger.committed, 4), "currency": costs["actual"]["currency"]}
    repo.write_manifest(manifest)
    result.final_state = manifest["state"]
    return result


def init_episode_from_topic(target_dir: Path, source_episode: Path) -> EpisodeRepo:
    """Create a fresh working episode from an existing episode's topic + manifest.

    Copies only 00_topic and manifest.json; downstream stages are produced by the
    pipeline. Refuses to clobber a non-empty target.
    """
    target_dir = Path(target_dir)
    if target_dir.exists() and any(target_dir.iterdir()):
        raise EpisodeRepoError(f"target episode dir is not empty: {target_dir}")
    (target_dir / "00_topic").mkdir(parents=True, exist_ok=True)
    for path in (source_episode / "00_topic").glob("topic.v*.json"):
        shutil.copy2(path, target_dir / "00_topic" / path.name)
    manifest = json.loads((source_episode / "manifest.json").read_text(encoding="utf-8"))
    manifest["artifacts"] = []
    manifest["active_revisions"] = {k: v for k, v in manifest["active_revisions"].items() if k == "topic"}
    if MANIFEST_STATE_ORDER.index(manifest["state"]) < _READY_FOR_RESEARCH:
        manifest["state"] = "approved"
    (target_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return EpisodeRepo(target_dir)
