#!/usr/bin/env python3
"""Audit and optionally clean internal release-gate text from YouTube descriptions."""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id

OUT = ROOT / "episodes" / "_planning" / "youtube_description_audit.latest.json"

EXACT_REMOVALS = [
    "Public upload remains blocked until owner approval and R3 legal/rights review are recorded for the exact final hashes.",
    "Public upload remains blocked until owner approval and R3 legal/rights review are recorded for exact final hashes.",
]

SUSPICIOUS_PATTERNS = [
    re.compile(r"public upload remains blocked", re.I),
    re.compile(r"public release remains blocked", re.I),
    re.compile(r"owner approval", re.I),
    re.compile(r"owner review", re.I),
    re.compile(r"R3 legal", re.I),
    re.compile(r"legal/rights review", re.I),
    re.compile(r"final candidate", re.I),
    re.compile(r"review[- ]proxy", re.I),
    re.compile(r"no upload, schedule, publish", re.I),
    re.compile(r"approval required", re.I),
]


def request_json(url: str, token: str, data: bytes | None = None, method: str = "GET") -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    if data is not None:
        headers["Content-Type"] = "application/json; charset=UTF-8"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def channel_uploads_playlist(token: str) -> str:
    data = request_json("https://www.googleapis.com/youtube/v3/channels?part=contentDetails&mine=true", token)
    items = data.get("items") or []
    if not items:
        raise RuntimeError("No YouTube channel found for this token")
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]


def list_upload_ids(token: str, playlist_id: str, limit: int | None) -> list[str]:
    ids: list[str] = []
    page = ""
    while True:
        params = {"part": "contentDetails", "playlistId": playlist_id, "maxResults": "50"}
        if page:
            params["pageToken"] = page
        data = request_json("https://www.googleapis.com/youtube/v3/playlistItems?" + urllib.parse.urlencode(params), token)
        for item in data.get("items") or []:
            video_id = item.get("contentDetails", {}).get("videoId")
            if video_id:
                ids.append(video_id)
                if limit and len(ids) >= limit:
                    return ids
        page = data.get("nextPageToken") or ""
        if not page:
            return ids


def get_videos(token: str, ids: list[str]) -> list[dict]:
    out: list[dict] = []
    for i in range(0, len(ids), 50):
        params = {"part": "snippet,status", "id": ",".join(ids[i : i + 50]), "maxResults": "50"}
        data = request_json("https://www.googleapis.com/youtube/v3/videos?" + urllib.parse.urlencode(params), token)
        out.extend(data.get("items") or [])
    return out


def clean_description(description: str) -> tuple[str, list[str]]:
    cleaned = description
    actions: list[str] = []
    for text in EXACT_REMOVALS:
        if text in cleaned:
            cleaned = cleaned.replace(text, "")
            actions.append(f"removed exact text: {text}")
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned, actions


def suspicious_hits(description: str) -> list[str]:
    return [pattern.pattern for pattern in SUSPICIOUS_PATTERNS if pattern.search(description)]


def update_description(token: str, video: dict, description: str) -> dict:
    snippet = video["snippet"]
    body = {
        "id": video["id"],
        "snippet": {
            "title": snippet["title"],
            "description": description,
            "categoryId": snippet.get("categoryId", "27"),
            "tags": snippet.get("tags", []),
            "defaultLanguage": snippet.get("defaultLanguage"),
            "defaultAudioLanguage": snippet.get("defaultAudioLanguage"),
        },
    }
    body["snippet"] = {k: v for k, v in body["snippet"].items() if v is not None}
    return request_json(
        "https://www.googleapis.com/youtube/v3/videos?part=snippet",
        token,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        method="PUT",
    )


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply exact safe removals.")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args(argv)

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    playlist_id = channel_uploads_playlist(token)
    ids = list_upload_ids(token, playlist_id, args.limit)
    videos = get_videos(token, ids)

    report = {
        "schema_version": "1.0.0",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "channel_id": channel_id,
        "uploads_playlist_id": playlist_id,
        "video_count": len(videos),
        "apply": args.apply,
        "findings": [],
        "updated": [],
    }
    for video in videos:
        snippet = video.get("snippet", {})
        status = video.get("status", {})
        desc = snippet.get("description", "")
        cleaned, actions = clean_description(desc)
        remaining_hits = suspicious_hits(cleaned)
        original_hits = suspicious_hits(desc)
        item = {
            "video_id": video.get("id"),
            "title": snippet.get("title"),
            "privacyStatus": status.get("privacyStatus"),
            "publishAt": status.get("publishAt"),
            "original_hits": original_hits,
            "safe_cleanup_actions": actions,
            "remaining_hits_after_safe_cleanup": remaining_hits,
            "watch": f"https://youtu.be/{video.get('id')}",
            "studio": f"https://studio.youtube.com/video/{video.get('id')}/edit",
        }
        if original_hits or actions:
            report["findings"].append(item)
        if args.apply and actions and cleaned != desc:
            updated = update_description(token, video, cleaned)
            report["updated"].append({"video_id": video.get("id"), "title": snippet.get("title"), "actions": actions, "response_id": updated.get("id")})
            print(f"UPDATED {video.get('id')} {snippet.get('title')}: {', '.join(actions)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"checked={len(videos)} findings={len(report['findings'])} updated={len(report['updated'])} report={OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
