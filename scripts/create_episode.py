#!/usr/bin/env python3
"""Create a safe Prime Documentary episode skeleton from a topic ID and slug."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPISODE_RE = re.compile(r"^PD-(\d{4})-(\d{3})-([a-z0-9-]+)$")
TOPIC_RE = re.compile(r"^TOP-\d{8}-\d{3}$")

SUBDIRS = [
    "00_topic", "01_research/sources", "01_research/notes", "02_story",
    "03_script", "04_scenes", "05_visuals/requests", "05_visuals/raw",
    "05_visuals/approved", "06_audio/narration", "06_audio/music",
    "06_audio/sfx", "07_edit", "08_package/thumbnail", "08_package/subtitles",
    "09_publish", "10_analytics", "approvals", "events", "logs", "tmp"
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("episode_id")
    parser.add_argument("topic_id")
    parser.add_argument("--root", type=Path, default=ROOT / "episodes")
    parser.add_argument("--title", default="")
    args = parser.parse_args()

    match = EPISODE_RE.fullmatch(args.episode_id)
    if not match:
        raise SystemExit("Invalid episode_id. Expected PD-YYYY-NNN-slug")
    if not TOPIC_RE.fullmatch(args.topic_id):
        raise SystemExit("Invalid topic_id. Expected TOP-YYYYMMDD-NNN")

    episode_dir = args.root / args.episode_id
    if episode_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing episode: {episode_dir}")

    for subdir in SUBDIRS:
        (episode_dir / subdir).mkdir(parents=True, exist_ok=False)

    now = datetime.now(timezone.utc).isoformat()
    manifest = {
        "schema_version": "1.0.0",
        "episode_id": args.episode_id,
        "topic_id": args.topic_id,
        "slug": match.group(3),
        "title_working": args.title,
        "state": "idea",
        "risk_class": "R0",
        "production_tier": "B",
        "autonomy_level": 3,
        "target_language": "en",
        "target_duration_minutes": 24,
        "active_revisions": {},
        "artifacts": [],
        "approvals": [],
        "costs": {
            "estimated": {"amount": 0, "currency": "USD"},
            "actual": {"amount": 0, "currency": "USD"},
            "soft_limit": {"amount": 100, "currency": "USD"},
            "hard_limit": {"amount": 200, "currency": "USD"}
        },
        "warnings": [],
        "blockers": [],
        "created_at": now,
        "updated_at": now
    }
    (episode_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (episode_dir / "events/events.jsonl").write_text(
        json.dumps({"event": "EPISODE_CREATED", "episode_id": args.episode_id, "at": now}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(episode_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
