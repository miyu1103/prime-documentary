#!/usr/bin/env python3
"""Ensure YouTube videos are marked as AI/synthetic-media disclosed.

This is a post-upload safety net for Prime Documentary. Upload/publish scripts
should already send containsSyntheticMedia=True, but this script makes the
state explicit for existing or manually-touched videos.

Usage:
    py -3.11 scripts/ensure_youtube_ai_disclosure.py --ids VIDEO_ID [VIDEO_ID ...]
    py -3.11 scripts/ensure_youtube_ai_disclosure.py --from-known
    py -3.11 scripts/ensure_youtube_ai_disclosure.py --from-known --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

KNOWN_VIDEO_IDS = [
    "PjGEqW6F9WM",  # Miranda
    "ch2hQ5jhDmQ",  # Gideon
    "An0to4U0hJQ",  # Mapp
    "waA4XJ9bYcE",  # FTX
    "ShfRaePw-t4",  # Channel trailer
]


def api_get(token: str, url: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def api_put(token: str, url: str, body: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_videos(token: str, ids: list[str]) -> list[dict]:
    url = "https://www.googleapis.com/youtube/v3/videos?" + urllib.parse.urlencode(
        {"part": "snippet,status", "id": ",".join(ids)}
    )
    return api_get(token, url).get("items", [])


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", nargs="*", default=[], help="YouTube video IDs to update.")
    parser.add_argument("--from-known", action="store_true", help="Use the known Prime Documentary public videos.")
    parser.add_argument("--dry-run", action="store_true", help="Read and report only.")
    args = parser.parse_args(argv)

    ids = list(dict.fromkeys((KNOWN_VIDEO_IDS if args.from_known else []) + args.ids))
    if not ids:
        parser.error("Provide --ids or --from-known.")

    token = _access_token(load_env())
    items = load_videos(token, ids)
    found = {item["id"] for item in items}
    missing = [video_id for video_id in ids if video_id not in found]

    result = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "missing": missing,
        "videos": [],
    }

    for item in items:
        video_id = item["id"]
        status = item.get("status", {})
        desired_status = {
            "privacyStatus": status.get("privacyStatus", "private"),
            "license": status.get("license", "youtube"),
            "embeddable": True,
            "publicStatsViewable": True,
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": True,
        }
        entry = {
            "id": video_id,
            "title": item.get("snippet", {}).get("title", ""),
            "before": status,
            "desired": desired_status,
        }
        if not args.dry_run:
            updated = api_put(
                token,
                "https://www.googleapis.com/youtube/v3/videos?part=status",
                {"id": video_id, "status": desired_status},
            )
            entry["after_update_response"] = updated.get("status", {})
        result["videos"].append(entry)

    out = ROOT / "runs" / "studio_audit_20260619" / "ensure_ai_disclosure_result.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"result: {out.relative_to(ROOT)}")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
