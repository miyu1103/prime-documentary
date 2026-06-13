from __future__ import annotations

import json
from pathlib import Path

import pytest

from pd_factory.episode_repo import EpisodeRepoError
from pd_factory.pipeline import (
    SCHEMA_DIR,
    STAGES,
    PipelineError,
    init_episode_from_topic,
    run_pipeline,
)
from pd_factory.schema_validation import validate_data

ROOT = Path(__file__).resolve().parents[1]
SOURCE_EPISODE = ROOT / "examples" / "episode"
STAGE_NAMES = [s.name for s in STAGES]


@pytest.fixture()
def repo(tmp_path):
    return init_episode_from_topic(tmp_path / "ep", SOURCE_EPISODE)


def _revalidate_all(repo):
    """Independently re-validate every active artifact against its schema."""
    for spec in STAGES:
        rev = repo.read_manifest()["active_revisions"][spec.name]
        data = repo.read_artifact(spec.folder, spec.stem, rev)
        schema = SCHEMA_DIR / spec.schema_file
        if spec.is_list:
            for item in data:
                validate_data(item, schema)
        else:
            validate_data(data, schema)


def test_full_run_produces_and_validates_all_stages(repo):
    result = run_pipeline(repo)
    assert result.by_action("produced") == STAGE_NAMES
    active = repo.read_manifest()["active_revisions"]
    for name in STAGE_NAMES:
        assert active[name] == "v001"
    assert active["topic"] == "v001"  # input never bumped
    _revalidate_all(repo)


def test_state_is_capped_honestly_at_script_draft(repo):
    run_pipeline(repo)
    # Placeholder research must not let the episode claim a verified/scene state.
    assert repo.read_manifest()["state"] == "script_draft"


def test_qc_gate_flags_placeholder_research(repo):
    run_pipeline(repo)
    qc = repo.read_artifact("08_qc", "qc_report", "v001")
    assert qc["result"] == "pass_with_warnings"
    codes = {f["code"] for f in qc["findings"]}
    assert {"CLAIM_UNSUPPORTED", "SOURCES_PLACEHOLDER"} <= codes


def test_resume_is_idempotent(repo):
    run_pipeline(repo)
    second = run_pipeline(repo)
    assert second.by_action("skipped") == STAGE_NAMES
    assert second.by_action("produced") == []
    active = repo.read_manifest()["active_revisions"]
    assert all(active[name] == "v001" for name in STAGE_NAMES)


def test_partial_rerun_invalidates_downstream_only(repo):
    run_pipeline(repo)
    result = run_pipeline(repo, from_stage="claims")
    produced = result.by_action("produced")
    # claims and everything depending (directly or transitively) on it recompute.
    assert "claims" in produced
    assert "thesis" in produced and "script" in produced and "qc_report" in produced
    # Upstream of claims is untouched.
    assert "research_plan" not in produced and "sources" not in produced
    active = repo.read_manifest()["active_revisions"]
    assert active["research_plan"] == "v001"
    assert active["sources"] == "v001"
    assert active["claims"] == "v002"
    assert active["thesis"] == "v002"
    assert active["qc_report"] == "v002"


def test_old_revisions_are_immutable_and_superseded(repo):
    run_pipeline(repo)
    run_pipeline(repo, from_stage="claims")
    # Both revisions exist on disk (nothing overwritten).
    assert repo.artifact_exists("01_research", "claims", "v001")
    assert repo.artifact_exists("01_research", "claims", "v002")
    artifacts = repo.read_manifest()["artifacts"]
    claims_entries = {a["revision"]: a["status"] for a in artifacts if a["artifact_type"] == "claims"}
    assert claims_entries["v001"] == "superseded"
    assert claims_entries["v002"] == "candidate"


def test_write_refuses_to_overwrite_existing_revision(repo):
    run_pipeline(repo)
    with pytest.raises(EpisodeRepoError):
        repo.write_artifact(
            folder="02_thesis", stem="thesis", revision="v001",
            data={"x": 1}, provenance={"checksum": "pending"},
        )


def test_pipeline_refuses_unapproved_topic(tmp_path):
    repo = init_episode_from_topic(tmp_path / "ep", SOURCE_EPISODE)
    manifest = repo.read_manifest()
    manifest["state"] = "screening"
    repo.write_manifest(manifest)
    with pytest.raises(PipelineError):
        run_pipeline(repo)


def test_events_log_records_every_stage(repo):
    run_pipeline(repo)
    lines = repo.events_path.read_text(encoding="utf-8").strip().splitlines()
    events = [json.loads(line) for line in lines]
    stage_events = [e for e in events if e["type"] == "stage" and e["action"] == "produced"]
    assert {e["stage"] for e in stage_events} == set(STAGE_NAMES)
