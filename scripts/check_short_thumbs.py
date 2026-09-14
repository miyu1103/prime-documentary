"""Read-only: check thumbnail state of the Shorts videos. No writes, no cost.

Prints, per video: privacy, the thumbnail URLs YouTube reports, and whether a custom
(maxres/standard/high) thumbnail appears set vs auto-generated. Also fetches each
thumbnail URL with a HEAD-like GET to confirm it actually resolves.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

VIDEOS = {
    "06": "dedDocuyCUM", "07": "L8iKnBSVXKg", "08": "m33s6uFmXao",
    "09": "rdOeETe0LXI", "10": "U6Z_eQ2nnp8", "11": "t8L1u3McD7o",
    "12": "N7J7pcDt4lY", "13": "jqupXgWwL54",
}


def get(url: str, token: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def head(url: str) -> int:
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except Exception as e:  # noqa: BLE001
        return getattr(e, "code", -1)


def main() -> int:
    token = _access_token(load_env())
    ids = ",".join(VIDEOS.values())
    data = get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails&id={ids}", token)
    by_id = {it["id"]: it for it in data.get("items", [])}
    for short, vid in VIDEOS.items():
        it = by_id.get(vid)
        if not it:
            print(f"short{short} {vid}: NOT FOUND")
            continue
        sn = it["snippet"]; st = it["status"]
        thumbs = sn.get("thumbnails", {})
        keys = sorted(thumbs.keys())
        maxres = thumbs.get("maxres", {}).get("url") or thumbs.get("standard", {}).get("url") or thumbs.get("high", {}).get("url")
        dur = it["contentDetails"]["duration"]
        code = head(maxres) if maxres else None
        print(f"short{short} {vid}  privacy={st.get('privacyStatus')} dur={dur}")
        print(f"   thumb sizes: {keys}")
        print(f"   best url: {maxres}  -> GET {code}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
