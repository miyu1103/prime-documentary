#!/usr/bin/env python3
"""Upload an approved episode to YouTube (private first).

Guards:
  - APR-0004 must exist and be approved
  - SHA256 of video file must match the approved hash
  - Visibility is forced to private (public scheduling is a separate human gate)
  - Channel ID must match CHANNEL_ALLOWLIST

Usage:
    python3.11 scripts/upload_episode.py
    python3.11 scripts/upload_episode.py --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

EPISODE_ID    = "PD-2026-001-miranda"
EPISODE_DIR   = ROOT / "episodes" / EPISODE_ID
META_PATH     = EPISODE_DIR / "09_package" / "youtube_meta.v003.json"
APR_PATH      = EPISODE_DIR / "approvals" / "APR-0004.json"
VIDEO_FILE    = Path(r"H:\pd-media\episodes\PD-2026-001-miranda\07_edit\sample\sample_v021.mp4")
EXPECTED_HASH = "20e926fb71c204ba40b5d6539f24d499b706cd820a215bc0b6d453758275d651"

CHANNEL_ALLOWLIST = {"UCuQPtAz1rca9eJ4xhvX0yKA"}  # Prime Documentary (renamed from Japan 2026-06-15)
CHUNK_SIZE        = 8 * 1024 * 1024               # 8 MB


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def get_channel_id(token: str) -> str:
    url = "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode())
    items = body.get("items", [])
    if not items:
        raise RuntimeError("No YouTube channel found for this token.")
    return items[0]["id"]


def initiate_upload(token: str, meta: dict, file_size: int) -> str:
    snippet = {
        "title": meta["title"],
        "description": meta["description"],
        "tags": meta.get("tags", []),
        "categoryId": "27",  # Education
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
    }
    body = json.dumps({
        "snippet": snippet,
        "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False},
    }).encode("utf-8")

    url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Upload-Content-Type": "video/mp4",
        "X-Upload-Content-Length": str(file_size),
    }, method="POST")

    with urllib.request.urlopen(req, timeout=30) as resp:
        upload_url = resp.headers.get("Location", "")

    if not upload_url.startswith("https://www.googleapis.com/"):
        raise RuntimeError(f"Unexpected upload URL host: {upload_url[:60]}")
    return upload_url


def upload_chunks(upload_url: str, token: str, video_path: Path) -> str:
    file_size = video_path.stat().st_size
    bytes_sent = 0

    with open(video_path, "rb") as f:
        while bytes_sent < file_size:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            chunk_end = bytes_sent + len(chunk) - 1
            req = urllib.request.Request(upload_url, data=chunk, headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "video/mp4",
                "Content-Range": f"bytes {bytes_sent}-{chunk_end}/{file_size}",
                "Content-Length": str(len(chunk)),
            }, method="PUT")

            try:
                with urllib.request.urlopen(req, timeout=300) as resp:
                    body = json.loads(resp.read().decode())
                    video_id = body.get("id", "")
                    bytes_sent += len(chunk)
                    print(f"  {bytes_sent / 1e6:.0f} MB / {file_size / 1e6:.0f} MB — upload complete")
                    return video_id
            except urllib.error.HTTPError as exc:
                if exc.code == 308:  # Resume Incomplete — normal for non-final chunks
                    bytes_sent += len(chunk)
                    pct = bytes_sent / file_size * 100
                    print(f"  {bytes_sent / 1e6:.0f} MB / {file_size / 1e6:.0f} MB ({pct:.0f}%)")
                    continue
                raise

    raise RuntimeError("Upload loop ended without a 200/201 response.")


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Verify guards only; do not upload.")
    args = parser.parse_args(argv)

    # ── Guard 1: APR-0004 ────────────────────────────────────────────────────
    if not APR_PATH.exists():
        print("BLOCKED: APR-0004.json not found. Publish approval required.")
        return 1
    apr = json.loads(APR_PATH.read_text(encoding="utf-8"))
    if apr.get("decision") != "approved":
        print(f"BLOCKED: APR-0004 decision={apr.get('decision')!r} — not approved.")
        return 1
    print("✓ APR-0004 approved")

    # ── Guard 2: video file exists ────────────────────────────────────────────
    if not VIDEO_FILE.exists():
        print(f"BLOCKED: video file not found: {VIDEO_FILE}")
        return 1

    # ── Guard 3: SHA256 ───────────────────────────────────────────────────────
    print(f"  Verifying SHA256 of {VIDEO_FILE.name} ({VIDEO_FILE.stat().st_size / 1e6:.0f} MB)…")
    actual = sha256_file(VIDEO_FILE)
    if actual != EXPECTED_HASH:
        print(f"BLOCKED: hash mismatch\n  expected: {EXPECTED_HASH}\n  actual:   {actual}")
        return 1
    print("✓ SHA256 verified")

    # ── Load meta ────────────────────────────────────────────────────────────
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))

    if args.dry_run:
        print("\n[dry-run] All guards passed. No upload performed.")
        return 0

    # ── Auth + channel check ─────────────────────────────────────────────────
    env = load_env()
    token = _access_token(env)
    print("✓ access token obtained")

    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        print(f"BLOCKED: channel {channel_id!r} not on allowlist {CHANNEL_ALLOWLIST}")
        return 1
    print(f"✓ channel confirmed: {channel_id}")

    # ── Initiate resumable upload ─────────────────────────────────────────────
    file_size = VIDEO_FILE.stat().st_size
    upload_url = initiate_upload(token, meta, file_size)
    print("✓ resumable upload session started")
    print(f"  uploading {file_size / 1e6:.0f} MB …")

    # ── Stream upload ────────────────────────────────────────────────────────
    video_id = upload_chunks(upload_url, token, VIDEO_FILE)

    if not video_id:
        print("✗ Upload succeeded but no video ID returned.")
        return 1

    url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"\n✓ Upload complete!")
    print(f"  video_id : {video_id}")
    print(f"  URL      : {url}  (private)")

    # ── Record result ────────────────────────────────────────────────────────
    result = {
        "episode_id": EPISODE_ID,
        "video_id": video_id,
        "url": url,
        "privacy": "private",
        "channel_id": channel_id,
        "file": VIDEO_FILE.name,
        "sha256": EXPECTED_HASH,
        "youtube_meta_revision": "v003",
        "approval_ref": "APR-0004",
        "uploaded_at": "2026-06-15T00:00:00Z",
    }
    result_path = EPISODE_DIR / "events" / "upload_v021.json"
    result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"  result   : {result_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
