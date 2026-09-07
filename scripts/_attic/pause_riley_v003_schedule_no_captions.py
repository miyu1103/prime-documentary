#!/usr/bin/env python3
"""Pause Riley v003 YouTube schedule because subtitles need to be burned in."""
from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

EP = "PD-2026-007-riley"
EPDIR = ROOT / "episodes" / EP
META = EPDIR / "09_package" / "youtube_meta.v003.json"
RESULT = EPDIR / "09_package" / "youtube_schedule_paused.v003.json"
EVENTS = EPDIR / "events" / "events.jsonl"


def request_json(url: str, token: str, data: bytes | None = None, method: str | None = None) -> dict:
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8"},
        method=method,
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    meta = json.loads(META.read_text(encoding="utf-8"))
    video_id = meta["video_id"]
    token = _access_token(load_env())
    before = request_json(f"https://www.googleapis.com/youtube/v3/videos?part=status&id={video_id}", token)
    body = {
        "id": video_id,
        "status": {
            "privacyStatus": "private",
            "publishAt": None,
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": True,
            "license": "youtube",
            "embeddable": True,
            "publicStatsViewable": True,
        },
    }
    after_update = request_json(
        "https://www.googleapis.com/youtube/v3/videos?part=status",
        token,
        data=json.dumps(body).encode("utf-8"),
        method="PUT",
    )
    after = request_json(f"https://www.googleapis.com/youtube/v3/videos?part=status,processingDetails&id={video_id}", token)
    now = datetime.now(timezone.utc).isoformat()
    out = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v003",
        "action": "pause_schedule_for_burned_captions_rebuild",
        "video_id": video_id,
        "before": before,
        "after_update": after_update,
        "after": after,
        "delete_performed": False,
        "paused_at": now,
    }
    RESULT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    meta["status"] = "paused_for_burned_captions_v004"
    meta["scheduled_at_local"] = None
    meta["scheduled_at_utc"] = None
    meta["publish_at_platform"] = None
    meta["caption_fix_required"] = "burned_captions_required_because_youtube_cc_not_visible_by_default"
    meta["schedule_pause_result_v003"] = str(RESULT.relative_to(ROOT)).replace("\\", "/")
    META.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "event": "youtube_schedule_paused_for_burned_captions",
            "episode_id": EP,
            "stage": "caption_fix",
            "revision": "v003",
            "actor": "codex",
            "video_id": video_id,
            "detail": "Paused Riley v003 schedule because owner reported subtitles not visible; v004 will use burned-in captions.",
            "pause_result": str(RESULT.relative_to(ROOT)).replace("\\", "/"),
            "ts": now,
        }, ensure_ascii=False) + "\n")
    print(json.dumps({"video_id": video_id, "paused": True, "result": str(RESULT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
