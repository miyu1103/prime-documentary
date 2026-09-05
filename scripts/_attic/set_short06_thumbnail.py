#!/usr/bin/env python3
"""Set the YouTube custom thumbnail for SHORT #6 with a compressed (<2MB) JPG.

The initial upload's PNG thumbnail exceeded YouTube's 2MB limit (HTTP 413). The flashy thumbnail
already shows via the baked-in cover frame; this also applies it to the watch page / search surfaces.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

VIDEO_ID = "HN08oQ9F1YA"
THUMB = ROOT / "remotion" / "out" / "short06_thumb.jpg"


def main() -> int:
    token = _access_token(load_env())
    req = urllib.request.Request(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={VIDEO_ID}",
        data=THUMB.read_bytes(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "image/jpeg"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        out = json.loads(resp.read().decode("utf-8"))
    print(json.dumps({"video_id": VIDEO_ID, "thumb": str(THUMB.name),
                      "kb": THUMB.stat().st_size // 1024, "set": True,
                      "etag": out.get("etag")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
