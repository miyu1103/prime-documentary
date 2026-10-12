#!/usr/bin/env python3
"""Replace an already-published Short with a bolder-thumbnail version (re-upload + supersede).

YouTube cannot swap a video file or reliably change a Shorts feed thumbnail (the feed uses the
first frame). So for each already-public Short we: upload a NEW coverfirst render (new bold
thumbnail baked into the 0.7s cover frame) as public, set the (now <2MB) thumbnail via API,
then privatize the OLD public video. Same title/description/tags — only the thumbnail changes.

Usage: python scripts/replace_short_thumbnail.py --short 06|07|08 [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id, sha256_file, upload_chunks

OUT = ROOT / "remotion" / "out"

CONFIG: dict[str, dict] = {
    "06": {
        "ep": "PD-2026-006-terry",
        "old_video_id": "HN08oQ9F1YA",
        "rev": "v002",
        "title": "Police Can Stop & Frisk You Without an Arrest #Shorts",
        "description": (
            "Police can stop you and pat you down — even without arresting you.\n"
            "No warrant. No proof of a crime. All they need is \"reasonable suspicion.\"\n"
            "In 1968, the Supreme Court allowed it 8-1, and \"stop and frisk\" was born (Terry v. Ohio).\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #SupremeCourt #Law #StopAndFrisk #FourthAmendment #Police #Rights #Documentary"
        ),
        "tags": ["Shorts", "Supreme Court", "Law", "Stop and Frisk", "Fourth Amendment", "Police", "Rights", "Documentary"],
        "video_sha256": "ba6a8688a2f067d63255d80d25efe0c2e6634c22160984753322420b9b729aef",
        "thumb_sha256": "fde38dd65b8c9204a82344907cac8e8fc6f83ec1a6c2dd2d6929e26c3b169913",
    },
    "07": {
        "ep": "PD-2026-007-riley",
        "old_video_id": "N3IBMcnhH6k",
        "rev": "v003",
        "title": "Police Need a Warrant to Search Your Phone #Shorts",
        "description": (
            "For centuries, police could search the things you carried when you were arrested.\n"
            "But the Supreme Court said a smartphone is different.\n\n"
            "In Riley v. California (2014), the Court ruled 9-0 that police generally need a warrant before searching your phone.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #SupremeCourt #Privacy #FourthAmendment #RileyVCalifornia #Law #Smartphones #Documentary"
        ),
        "tags": ["Shorts", "Supreme Court", "Privacy", "Fourth Amendment", "Riley v California", "Law", "Smartphone Privacy", "Documentary"],
        "video_sha256": "2d786585abb4a10ee9c8dd607e274b1f771da618807fb6730caedf0cda49d13b",
        "thumb_sha256": "492c1c6a7a9f4f2175f171f20496b480177882f6bd993adc1d664223a6e37129",
    },
    "08": {
        "ep": "PD-2026-008-carpenter",
        "old_video_id": "w2H89cH_cv8",
        "rev": "v002",
        "title": "Police Tracked His Phone for 127 Days — No Warrant? #Shorts",
        "description": (
            "Your phone quietly logs where you go. Police wanted 127 days of one man's location history — without a warrant.\n\n"
            "In Carpenter v. United States (2018), the Supreme Court ruled 5-4 that police generally need a warrant to get your long-term cell-phone location records.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #SupremeCourt #Privacy #FourthAmendment #Carpenter #Law #Documentary"
        ),
        "tags": ["Shorts", "Supreme Court", "Privacy", "Fourth Amendment", "Carpenter v United States", "Cell Phone Location", "Law", "Documentary"],
        "video_sha256": "41af0606791a0253d706e316b7df51c6a73f507f79867f9c7c6b33396176e04d",
        "thumb_sha256": "424433aa87f6319d173e6a485e2d4c92e10184d8436a82796b9868611e658b7a",
    },
}


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def initiate_upload(token: str, file_size: int, cfg: dict) -> str:
    snippet = {
        "title": cfg["title"],
        "description": cfg["description"],
        "tags": cfg["tags"],
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
    }
    status = {
        "privacyStatus": "public",
        "selfDeclaredMadeForKids": False,
        "containsSyntheticMedia": True,
        "license": "youtube",
        "embeddable": True,
        "publicStatsViewable": True,
    }
    body = json.dumps({"snippet": snippet, "status": status}).encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4",
            "X-Upload-Content-Length": str(file_size),
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        upload_url = resp.headers.get("Location", "")
    if not upload_url.startswith("https://www.googleapis.com/"):
        raise RuntimeError(f"Unexpected upload URL host: {upload_url[:80]}")
    return upload_url


def set_thumbnail(token: str, video_id: str, thumb: Path) -> dict:
    req = urllib.request.Request(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        data=thumb.read_bytes(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "image/png"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_state(token: str, video_id: str) -> dict:
    req = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={video_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def compact(state: dict) -> dict:
    items = state.get("items") or []
    item = items[0] if items else {}
    st = item.get("status", {})
    pr = item.get("processingDetails", {})
    sn = item.get("snippet", {})
    return {
        "id": item.get("id"),
        "title": sn.get("title"),
        "privacyStatus": st.get("privacyStatus"),
        "uploadStatus": st.get("uploadStatus"),
        "processingStatus": pr.get("processingStatus"),
    }


def wait_for_processing(token: str, video_id: str) -> tuple[dict, str]:
    state: dict = {}
    ps = "unknown"
    for _ in range(16):
        state = get_state(token, video_id)
        ps = compact(state).get("processingStatus") or "unknown"
        if ps in {"succeeded", "failed", "terminated"}:
            break
        time.sleep(10)
    return state, ps


def set_private(token: str, video_id: str) -> dict:
    body = json.dumps({
        "id": video_id,
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": True,
            "license": "youtube",
            "embeddable": True,
            "publicStatsViewable": True,
        },
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/videos?part=status",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8"},
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--short", required=True, choices=sorted(CONFIG))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    cfg = CONFIG[args.short]
    short_id = f"short{args.short}"
    video = OUT / f"{short_id}_yt_coverfirst.mp4"
    thumb = OUT / f"{short_id}_thumb.png"
    pkg = ROOT / "episodes" / cfg["ep"] / "09_package"
    result_path = pkg / f"{short_id}_youtube_publish_result.{cfg['rev']}.json"

    if result_path.exists():
        raise RuntimeError(f"Refusing duplicate: {result_path.relative_to(ROOT)} exists")
    for p in (video, thumb):
        if not p.exists():
            raise RuntimeError(f"Missing artifact: {p}")
    av, at = sha256_file(video), sha256_file(thumb)
    if av != cfg["video_sha256"]:
        raise RuntimeError(f"Video hash mismatch: expected {cfg['video_sha256']} actual {av}")
    if at != cfg["thumb_sha256"]:
        raise RuntimeError(f"Thumb hash mismatch: expected {cfg['thumb_sha256']} actual {at}")
    print(f"OK {short_id}: new video+thumb verified; will replace old {cfg['old_video_id']}")
    print(f"OK title: {cfg['title']}")
    if args.dry_run:
        print("DRY_RUN_OK no external writes performed")
        return 0

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted")

    upload_url = initiate_upload(token, video.stat().st_size, cfg)
    print(f"OK upload started ({video.stat().st_size/1e6:.1f} MB)")
    new_id = upload_chunks(upload_url, token, video)
    if not new_id:
        raise RuntimeError("Upload returned no video_id")
    print(f"OK new public video_id={new_id}")

    thumb_status = thumb_error = None
    try:
        thumb_status = set_thumbnail(token, new_id, thumb)
        print("OK thumbnail set via API")
    except urllib.error.HTTPError as e:
        thumb_error = {"code": e.code, "reason": str(e.reason), "body": e.read().decode("utf-8", errors="replace")}
        print(f"WARN thumbnail set HTTP {e.code}; cover frame is baked in")

    state, ps = wait_for_processing(token, new_id)
    new_compact = compact(state)
    if new_compact.get("privacyStatus") != "public":
        raise RuntimeError(f"New upload not public: {new_compact.get('privacyStatus')!r}")

    old_before = get_state(token, cfg["old_video_id"])
    set_private(token, cfg["old_video_id"])
    old_after = get_state(token, cfg["old_video_id"])
    print(f"OK old {cfg['old_video_id']} privacy -> {compact(old_after).get('privacyStatus')}")

    now = datetime.now(timezone.utc).isoformat()
    result = {
        "schema_version": "1.0.0",
        "episode_id": cfg["ep"],
        "short_id": short_id,
        "platform": "youtube",
        "revision": cfg["rev"],
        "reason": "bolder, more legible thumbnail (owner feedback); re-upload + supersede",
        "video_id": new_id,
        "watch": f"https://youtu.be/{new_id}",
        "studio": f"https://studio.youtube.com/video/{new_id}/edit",
        "channel_id": channel_id,
        "privacy": new_compact.get("privacyStatus"),
        "title": cfg["title"],
        "description": cfg["description"],
        "tags": cfg["tags"],
        "video_file": str(video.relative_to(ROOT)).replace("\\", "/"),
        "video_sha256": "sha256:" + cfg["video_sha256"],
        "thumbnail_file": str(thumb.relative_to(ROOT)).replace("\\", "/"),
        "thumbnail_sha256": "sha256:" + cfg["thumb_sha256"],
        "thumbnail_set": thumb_status is not None,
        "thumbnail_status": thumb_status,
        "thumbnail_error": thumb_error,
        "cover_frame_baked_in": True,
        "cover_frame_duration_sec": 0.7,
        "supersedes_video_id": cfg["old_video_id"],
        "superseded_video_state_before": old_before,
        "superseded_video_state_after": old_after,
        "madeForKids": False,
        "containsSyntheticMedia": True,
        "external_upload": True,
        "public_publish": True,
        "owner_instruction": "投稿済みのサムネを派手で読みやすく差し替えて",
        "published_at": now,
        "youtube_state_compact": new_compact,
        "youtube_state": state,
    }
    write_json(result_path, result)
    print(json.dumps({
        "short": short_id,
        "new_video_id": new_id,
        "watch": f"https://youtu.be/{new_id}",
        "old_video_id": cfg["old_video_id"],
        "old_privacy_after": compact(old_after).get("privacyStatus"),
        "thumbnail_set": thumb_status is not None,
        "result": str(result_path.relative_to(ROOT)).replace("\\", "/"),
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
