"""Tests for the animatic review store (schema, atomic save + backup, ids, state history)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "review"))

import store  # noqa: E402
from pd_factory.schema_validation import SchemaValidationError  # noqa: E402

META = {"fps": 30, "duration_seconds": 745.0, "duration_frames": 22350, "composition_id": "Animatic"}
NOW = "2026-06-14T12:00:00+09:00"


def test_format_timecode():
    assert store.format_timecode(79.5) == "00:01:19.500"
    assert store.format_timecode(0) == "00:00:00.000"
    assert store.format_timecode(3661.25) == "01:01:01.250"


def test_new_review_is_valid():
    doc = store.new_review(META, now=NOW)
    store.validate_review(doc)
    assert doc["player_state"]["fps"] == 30
    assert doc["review_state"] == "not_started"


def test_markers_and_comments_increment_and_validate():
    doc = store.new_review(META, now=NOW)
    m1 = store.add_marker(doc, marker_type="boring", frame=1200, seconds=40.0, fps=30, now=NOW)
    m2 = store.add_marker(doc, marker_type="blocker", frame=1500, seconds=50.0, fps=30, severity="blocker", now=NOW)
    assert (m1["marker_id"], m2["marker_id"]) == ("MRK-0001", "MRK-0002")
    c1 = store.add_comment(doc, category="pacing", severity="needs_fix", frame=1215, seconds=40.5, fps=30,
                           original_comment_ja="この場面は少し長い。", marker_id="MRK-0001", now=NOW)
    assert c1["comment_id"] == "CMT-0001"
    assert c1["original_comment_ja"] == "この場面は少し長い。" and c1["instruction_en"] is None
    store.validate_review(doc)  # must remain schema-valid


def test_save_atomic_and_backup(tmp_path: Path):
    p = tmp_path / "animatic_review.v001.json"
    store.BACKUP_DIR = tmp_path / "backups"
    doc = store.new_review(META, now=NOW)
    store.save_atomic(doc, path=p, now=NOW)
    assert p.exists() and json.loads(p.read_text(encoding="utf-8"))["review_state"] == "not_started"
    # second save backs up the previous file
    store.add_marker(doc, marker_type="unclear", frame=100, seconds=3.3, fps=30, now=NOW)
    store.save_atomic(doc, path=p, now="2026-06-14T12:05:00+09:00")
    backups = list((tmp_path / "backups").glob("*.json"))
    assert len(backups) == 1


def test_load_or_init_keeps_existing(tmp_path: Path):
    p = tmp_path / "r.json"
    doc = store.new_review(META, now=NOW)
    store.add_comment(doc, category="visual", severity="minor", frame=10, seconds=0.3, fps=30,
                      original_comment_ja="x", now=NOW)
    store.save_atomic(doc, path=p, backup=False, now=NOW)
    loaded = store.load_or_init(META, path=p)
    assert len(loaded["comments"]) == 1  # existing comments not dropped


def test_state_history():
    doc = store.new_review(META, now=NOW)
    store.set_review_state(doc, "first_pass", now=NOW)
    store.set_review_state(doc, "second_pass", now=NOW)
    assert [h["to"] for h in doc["state_history"]] == ["first_pass", "second_pass"]
    store.set_review_state(doc, "second_pass", now=NOW)  # no-op
    assert len(doc["state_history"]) == 2


def test_invalid_marker_type_rejected():
    doc = store.new_review(META, now=NOW)
    doc["markers"].append({"marker_id": "MRK-0001", "marker_type": "NOPE", "frame": 1, "seconds": 1,
                           "timecode": "00:00:01.000", "fps": 30, "created_at": NOW})
    with pytest.raises(SchemaValidationError):
        store.validate_review(doc)
