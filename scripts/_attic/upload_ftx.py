#!/usr/bin/env python3
"""Upload PD-2026-004-ftx to YouTube as PRIVATE, then optionally publish.

Guards:
- APR-0004 must approve the exact v009 final-cut hash.
- Upload is forced private first.
- Channel must match the Prime Documentary allowlist.
- Selected click thumbnail is uploaded after the video insert.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id, initiate_upload, sha256_file, upload_chunks

EP = "PD-2026-004-ftx"
EPDIR = ROOT / "episodes" / EP
META = EPDIR / "09_package" / "youtube_meta.v001.json"
APR = EPDIR / "approvals" / "APR-0004.json"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
VIDEO = MEDIA / "episodes" / EP / "08_edit" / "ftx_premium_v009.mp4"
THUMB = MEDIA / "episodes" / EP / "09_package" / "thumbnail_click_a_v001.png"
EVENTS_DIR = EPDIR / "events"
UPLOAD_RESULT = EPDIR / "09_package" / "upload_result.json"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def expected_hash(meta: dict) -> str:
    value = meta["safety_checklist"]["final_cut_hash"]
    return value.removeprefix("sha256:")


def set_thumbnail(token: str, video_id: str, png: Path) -> dict:
    url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}"
    req = urllib.request.Request(
        url,
        data=png.read_bytes(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "image/png"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode())


def publish_public(token: str, video_id: str) -> dict:
    body = json.dumps(
        {
            "id": video_id,
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
                "containsSyntheticMedia": True,
            },
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/videos?part=status",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--public", action="store_true", help="Flip to public after private upload succeeds.")
    args = parser.parse_args(argv)

    if not APR.exists():
        print(f"BLOCKED: missing approval {APR}")
        return 1
    apr = json.loads(APR.read_text("utf-8"))
    if apr.get("decision") != "approved":
        print(f"BLOCKED: APR-0004 decision={apr.get('decision')!r}")
        return 1
    print("APR-0004 approved")

    if not META.exists():
        print(f"BLOCKED: missing metadata {META}")
        return 1
    meta = json.loads(META.read_text("utf-8"))

    if not VIDEO.exists():
        print(f"BLOCKED: missing video {VIDEO}")
        return 1
    if not THUMB.exists():
        print(f"BLOCKED: missing thumbnail {THUMB}")
        return 1

    expected = expected_hash(meta)
    print(f"verifying SHA256 of {VIDEO.name} ({VIDEO.stat().st_size / 1e6:.0f} MB)...")
    actual = sha256_file(VIDEO)
    if actual != expected:
        print(f"BLOCKED: hash mismatch\n  expected {expected}\n  actual   {actual}")
        return 1
    if apr.get("content_hash", "").removeprefix("sha256:") != actual:
        print("BLOCKED: approval hash does not match final cut")
        return 1
    print("SHA256 verified")

    if args.dry_run:
        print("\n[dry-run] guards passed; no upload.")
        print(f"title: {meta['title']}")
        print(f"thumbnail: {THUMB}")
        print(f"publish_public_after_upload: {args.public}")
        return 0

    env = load_env()
    token = _access_token(env)
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        print(f"BLOCKED: channel {channel_id!r} not allowlisted")
        return 1
    print(f"channel confirmed: {channel_id}")

    upload_url = initiate_upload(token, meta, VIDEO.stat().st_size)
    print(f"resumable session started; uploading PRIVATE ({VIDEO.stat().st_size / 1e6:.0f} MB)...")
    video_id = upload_chunks(upload_url, token, VIDEO)
    if not video_id:
        print("Upload completed but no video_id was returned.")
        return 1
    print(f"uploaded private: {video_id}")

    thumb_status = "set"
    thumb_error = None
    try:
        set_thumbnail(token, video_id, THUMB)
        print("thumbnail set")
    except (urllib.error.HTTPError, urllib.error.URLError, RuntimeError) as exc:
        thumb_status = "failed"
        thumb_error = str(exc)
        print(f"thumbnail set failed; set manually if needed: {exc}")

    visibility = "private"
    if args.public:
        publish_public(token, video_id)
        visibility = "public"
        print("visibility set to public")

    result = {
        "episode_id": EP,
        "video_id": video_id,
        "visibility": visibility,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "channel_id": channel_id,
        "file": str(VIDEO),
        "sha256": actual,
        "youtube_meta_revision": "v001",
        "approval_ref": "APR-0004",
        "thumbnail_status": thumb_status,
        "thumbnail_error": thumb_error,
        "uploaded_at": now_utc(),
    }
    UPLOAD_RESULT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", "utf-8")
    EVENTS_DIR.mkdir(parents=True, exist_ok=True)
    (EVENTS_DIR / "upload_v009.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", "utf-8")
    with (EVENTS_DIR / "events.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"event": "uploaded", "stage": "published" if args.public else "uploading", **result}, ensure_ascii=False) + "\n")

    print(f"\nWatch:  https://youtu.be/{video_id}")
    print(f"Studio: https://studio.youtube.com/video/{video_id}/edit")
    print(f"Result: {UPLOAD_RESULT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
