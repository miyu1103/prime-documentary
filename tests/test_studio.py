from __future__ import annotations

from datetime import datetime, timezone

import pytest

from pd_factory.episode_repo import EpisodeRepoError
from pd_factory.pipeline import SCHEMA_DIR
from pd_factory.schema_validation import validate_data
from pd_factory.studio import (
    MIN_THEME_LENGTH,
    StudioError,
    build_topic,
    create_and_run,
    init_episode_from_theme,
    slugify,
)

NOW = datetime(2026, 6, 13, 9, 30, 0, tzinfo=timezone.utc)


def test_build_topic_is_schema_valid_and_uses_theme():
    topic = build_topic("Why pencils are yellow", now=NOW)
    validate_data(topic, SCHEMA_DIR / "topic.schema.json")
    assert topic["subject"] == "Why pencils are yellow"
    assert topic["topic_id"].startswith("TOP-20260613-")
    # A seed is honestly unscored, not a fabricated "great" topic.
    assert topic["scores"]["total"] == 0
    assert topic["status"] == "candidate"


def test_build_topic_rejects_too_short():
    with pytest.raises(StudioError):
        build_topic("ab", now=NOW)
    assert MIN_THEME_LENGTH == 3


@pytest.mark.parametrize(
    "raw,expected",
    [("Why Pencils Are Yellow", "why-pencils-are-yellow"), ("   ", "episode"), ("日本語", "episode")],
)
def test_slugify(raw, expected):
    assert slugify(raw) == expected


def test_init_episode_writes_valid_topic_and_runnable_manifest(tmp_path):
    repo = init_episode_from_theme(tmp_path / "ep", "The economics of cardboard", now=NOW)
    manifest = repo.read_manifest()
    validate_data(manifest, SCHEMA_DIR / "episode-manifest.schema.json")
    # Manifest is cleared to "approved" so the existing pipeline gate passes.
    assert manifest["state"] == "approved"
    assert manifest["active_revisions"] == {"topic": "v001"}
    assert repo.artifact_exists("00_topic", "topic", "v001")


def test_init_episode_refuses_non_empty_target(tmp_path):
    target = tmp_path / "ep"
    target.mkdir()
    (target / "stray.txt").write_text("x", encoding="utf-8")
    with pytest.raises(EpisodeRepoError):
        init_episode_from_theme(target, "Anything here", now=NOW)


def test_create_and_run_produces_view_with_script_scenes_qc(tmp_path):
    view = create_and_run(tmp_path / "runs", "How glass is made", now=NOW)
    assert view.theme == "How glass is made"
    assert "script" in view.produced and "qc_report" in view.produced
    assert view.script.get("spans"), "script should contain spans"
    assert view.scene_plan.get("scenes"), "scene plan should contain scenes"
    # Placeholder research must still be flagged not-publishable.
    assert view.qc["result"] == "pass_with_warnings"
    codes = {f["code"] for f in view.qc["findings"]}
    assert {"CLAIM_UNSUPPORTED", "SOURCES_PLACEHOLDER"} <= codes


def test_create_and_run_isolates_each_invocation(tmp_path):
    runs = tmp_path / "runs"
    v1 = create_and_run(runs, "Topic one")
    v2 = create_and_run(runs, "Topic two")
    assert v1.episode_id != v2.episode_id
    # Two distinct workspaces, nothing overwritten.
    assert len(list(runs.iterdir())) == 2
