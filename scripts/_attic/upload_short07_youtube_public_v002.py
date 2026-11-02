#!/usr/bin/env python3
"""Publish SHORT #7 Riley v002 with the thumbnail baked into the first frame.

YouTube Shorts does not reliably surface an API-uploaded custom image as the
Shorts thumbnail. This replacement keeps the same Short but adds a 0.7s cover
frame at the front, then privatizes the previous public upload after v002 is live.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import upload_short07_youtube_public as base
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

OLD_VIDEO_ID = "iW4mexjyeVM"
REVISION = "v002"

base.VIDEO = ROOT / "remotion" / "out" / "short07_yt_coverfirst.mp4"
base.EXPECTED_VIDEO = "7222ea604daf242e5ef236cf0afbac51c028b9be929f0343a7c543f9ae91f14b"
base.RESULT = base.PKG / f"short07_youtube_publish_result.{REVISION}.json"
base.STATUS_VERIFY = base.PKG / f"short07_youtube_status_verify.{REVISION}.json"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def set_private(token: str, video_id: str) -> dict:
    body = json.dumps(
        {
            "id": video_id,
            "status": {
                "privacyStatus": "private",
                "selfDeclaredMadeForKids": False,
                "containsSyntheticMedia": True,
                "license": "youtube",
                "embeddable": True,
                "publicStatsViewable": True,
            },
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/videos?part=status",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main(argv: list[str]) -> int:
    code = base.main(argv)
    if code != 0 or "--dry-run" in argv:
        return code

    token = _access_token(load_env())
    old_before = base.get_video_state(token, OLD_VIDEO_ID)
    private_result = set_private(token, OLD_VIDEO_ID)
    old_after = base.get_video_state(token, OLD_VIDEO_ID)
    result = json.loads(base.RESULT.read_text(encoding="utf-8"))
    result["revision"] = REVISION
    result["cover_frame_baked_in"] = True
    result["cover_frame_duration_sec"] = 0.7
    result["supersedes_video_id"] = OLD_VIDEO_ID
    result["superseded_video_private_result"] = private_result
    result["superseded_video_state_before"] = old_before
    result["superseded_video_state_after"] = old_after
    result["superseded_at"] = datetime.now(timezone.utc).isoformat()
    write_json(base.RESULT, result)
    print(
        json.dumps(
            {
                "replacement_video_id": result["video_id"],
                "replacement_watch": result["watch"],
                "old_video_id": OLD_VIDEO_ID,
                "old_privacy_after": base.compact_video_state(old_after).get("privacyStatus"),
                "result": str(base.RESULT.relative_to(ROOT)).replace("\\", "/"),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
