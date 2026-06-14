"""Animatic review store — pure, testable logic (JSON is the source of truth, P0 spec §6).

No network, no server here. The server (serve.py) calls these. All writes are atomic
(temp + rename) and back up any existing review first (rules/14). JSON validates against
schemas/animatic-review.schema.json.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
from pd_factory.schema_validation import validate_data  # noqa: E402

SCHEMA = REPO_ROOT / "schemas" / "animatic-review.schema.json"
REVIEW_DIR = REPO_ROOT / "episodes" / "PD-2026-001-miranda" / "08_qc" / "reviews"
REVIEW_PATH = REVIEW_DIR / "animatic_review.v001.json"
DRAFT_PATH = REVIEW_DIR / "animatic_review.draft.v001.json"
BACKUP_DIR = REVIEW_DIR / "backups"

_ID_RE = re.compile(r"-(\d{4})$")


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def format_timecode(seconds: float) -> str:
    if seconds < 0:
        seconds = 0.0
    ms = int(round((seconds - int(seconds)) * 1000))
    s = int(seconds)
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}.{ms:03d}"


def next_id(prefix: str, items: list[dict[str, Any]], key: str) -> str:
    nums = [int(m.group(1)) for it in items if (m := _ID_RE.search(str(it.get(key, ""))))]
    return f"{prefix}-{(max(nums) + 1) if nums else 1:04d}"


def new_review(meta: dict[str, Any], *, now: str | None = None) -> dict[str, Any]:
    ts = now or now_iso()
    fps = float(meta.get("fps") or 30)
    return {
        "schema_version": "1.0.0",
        "review_id": "REV-PD-2026-001-miranda-ANIMATIC-001",
        "episode_id": "PD-2026-001-miranda",
        "episode_slug": "miranda",
        "composition_id": meta.get("composition_id", "Animatic"),
        "source_revision": meta.get("source_revision", {"script": "v001", "scene_plan": "v001", "animatic": "v001"}),
        "review_state": "not_started",
        "language": {"input": "ja-JP", "execution": "en-US"},
        "player_state": {
            "fps": fps,
            "duration_frames": meta.get("duration_frames"),
            "duration_seconds": meta.get("duration_seconds"),
            "current_frame": 0,
            "current_seconds": 0,
            "playback_rate": 1.0,
        },
        "session": {"started_at": ts, "updated_at": ts, "completed_at": None, "last_saved_at": None},
        "draft": {"active": False, "category": None, "severity": None, "original_comment_ja": "", "timecode": None, "frame": None, "seconds": None, "updated_at": None},
        "markers": [],
        "comments": [],
        "state_history": [],
        "save_status": {"last_result": None, "last_error": None},
    }


def validate_review(doc: dict[str, Any]) -> None:
    validate_data(doc, SCHEMA)


def load_or_init(meta: dict[str, Any], *, path: Path = REVIEW_PATH, now: str | None = None) -> dict[str, Any]:
    if path.exists():
        doc = json.loads(path.read_text(encoding="utf-8"))
        # P0: never drop existing comments/markers; keep current player metadata fresh.
        if meta.get("duration_seconds"):
            doc.setdefault("player_state", {})["duration_seconds"] = meta["duration_seconds"]
            doc["player_state"]["duration_frames"] = meta.get("duration_frames")
        return doc
    return new_review(meta, now=now)


def save_atomic(doc: dict[str, Any], *, path: Path = REVIEW_PATH, backup: bool = True, now: str | None = None) -> None:
    """Validate, back up any existing file, then write atomically (temp + rename)."""
    validate_review(doc)
    ts = now or now_iso()
    doc.setdefault("session", {})["last_saved_at"] = ts
    doc.setdefault("save_status", {})
    path.parent.mkdir(parents=True, exist_ok=True)
    if backup and path.exists():
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        stamp = ts.replace(":", "").replace("-", "").replace("+", "_")
        shutil.copy2(path, BACKUP_DIR / f"{path.stem}.{stamp}.json")
    tmp = path.with_suffix(path.suffix + ".partial")
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    doc["save_status"]["last_result"] = "ok"
    doc["save_status"]["last_error"] = None


def save_draft(draft: dict[str, Any], *, path: Path = DRAFT_PATH) -> None:
    """Lightweight, frequent autosave of the in-progress draft. No backup, no full validation."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".partial")
    tmp.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def add_marker(doc: dict[str, Any], *, marker_type: str, frame: float, seconds: float, fps: float,
               severity: str | None = None, scene_id: str | None = None, note_ja: str | None = None,
               now: str | None = None) -> dict[str, Any]:
    m = {
        "marker_id": next_id("MRK", doc["markers"], "marker_id"),
        "marker_type": marker_type,
        "severity": severity,
        "frame": frame,
        "seconds": seconds,
        "timecode": format_timecode(seconds),
        "fps": fps,
        "scene_id": scene_id,
        "note_ja": note_ja,
        "created_at": now or now_iso(),
    }
    doc["markers"].append(m)
    return m


def add_comment(doc: dict[str, Any], *, category: str, severity: str, frame: float, seconds: float,
                fps: float, original_comment_ja: str, marker_id: str | None = None,
                scene_id: str | None = None, nearby_reference: str | None = None,
                now: str | None = None) -> dict[str, Any]:
    ts = now or now_iso()
    c = {
        "comment_id": next_id("CMT", doc["comments"], "comment_id"),
        "marker_id": marker_id,
        "category": category,
        "severity": severity,
        "frame": frame,
        "seconds": seconds,
        "timecode": format_timecode(seconds),
        "fps": fps,
        "scene_id": scene_id,
        "nearby_reference": nearby_reference,
        "original_comment_ja": original_comment_ja,
        "instruction_en": None,
        "translation_status": "pending",
        "status": "open",
        "created_at": ts,
        "updated_at": ts,
    }
    doc["comments"].append(c)
    return c


def set_review_state(doc: dict[str, Any], to: str, *, reason: str = "owner_action", now: str | None = None) -> None:
    frm = doc.get("review_state")
    if frm == to:
        return
    doc["state_history"].append({"from": frm, "to": to, "changed_at": now or now_iso(), "reason": reason})
    doc["review_state"] = to
    if to == "completed":
        doc.setdefault("session", {})["completed_at"] = now or now_iso()
