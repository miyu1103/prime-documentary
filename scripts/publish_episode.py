#!/usr/bin/env python3
"""Set thumbnail and publish video to public.

Guards: APR-0004 approved, video_id confirmed, SHA256 verified.
Usage: python3.11 scripts/publish_episode.py [--dry-run]
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

VIDEO_ID      = "PjGEqW6F9WM"
EXPECTED_HASH = "20e926fb71c204ba40b5d6539f24d499b706cd820a215bc0b6d453758275d651"
VIDEO_FILE    = Path(r"H:\pd-media\episodes\PD-2026-001-miranda\07_edit\sample\sample_v021.mp4")
THUMB_FILE    = ROOT / "remotion" / "out" / "thumb_final.png"
APR_PATH      = ROOT / "episodes" / "PD-2026-001-miranda" / "approvals" / "APR-0004.json"
EPISODE_DIR   = ROOT / "episodes" / "PD-2026-001-miranda"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def upload_thumbnail(token: str, video_id: str, thumb_path: Path) -> None:
    data = thumb_path.read_bytes()
    url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails?videoId={video_id}&uploadType=media"
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "image/png",
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode(errors="replace")
        raise RuntimeError(
            f"thumbnails.set failed: HTTP {exc.code}\n{err_body[:400]}"
        ) from exc
    if "items" not in body and "kind" not in body:
        raise RuntimeError(f"Thumbnail upload unexpected response: {body}")


def set_public_with_meta(token: str, video_id: str, meta: dict) -> None:
    payload = {
        "id": video_id,
        "snippet": {
            "title": meta["title"],
            "description": meta["description"],
            "tags": meta.get("tags", []),
            "categoryId": "27",  # Education
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }
    body = json.dumps(payload).encode("utf-8")
    url = "https://www.googleapis.com/youtube/v3/videos?part=snippet,status"
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }, method="PUT")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
    privacy = result.get("status", {}).get("privacyStatus", "?")
    if privacy != "public":
        raise RuntimeError(f"Expected public, got: {privacy}")
    returned_title = result.get("snippet", {}).get("title", "")
    if returned_title != meta["title"]:
        raise RuntimeError(f"Title mismatch: expected {meta['title']!r}, got {returned_title!r}")


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    # Guard: APR-0004
    apr = json.loads(APR_PATH.read_text(encoding="utf-8"))
    if apr.get("decision") != "approved":
        print("BLOCKED: APR-0004 not approved"); return 1
    print("✓ APR-0004 approved")

    # Guard: SHA256
    print(f"  Verifying SHA256…")
    if sha256_file(VIDEO_FILE) != EXPECTED_HASH:
        print("BLOCKED: hash mismatch"); return 1
    print("✓ SHA256 verified")

    # Guard: thumbnail exists
    if not THUMB_FILE.exists():
        print(f"BLOCKED: thumbnail not found: {THUMB_FILE}"); return 1
    thumb_kb = THUMB_FILE.stat().st_size // 1024
    print(f"✓ thumbnail found ({thumb_kb} KB)")

    if args.dry_run:
        print("\n[dry-run] All guards passed. No changes made.")
        return 0

    meta_path = EPISODE_DIR / "09_package" / "youtube_meta.v003.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    env = load_env()
    token = _access_token(env)
    print("✓ access token obtained")

    # Upload thumbnail (may fail on channels below ~1,000 subs — continue anyway)
    print("  Uploading thumbnail…")
    thumb_ok = False
    try:
        upload_thumbnail(token, VIDEO_ID, THUMB_FILE)
        thumb_ok = True
        print("✓ thumbnail set")
    except RuntimeError as exc:
        if "404" in str(exc):
            print(f"⚠ thumbnails.set: API returned 404 (channel not yet eligible).")
            print(f"  → Upload manually in YouTube Studio: {THUMB_FILE}")
        else:
            raise

    # Publish: update title, description, tags, and set privacy to public
    print(f"  Title     : {meta['title']}")
    print(f"  Tags      : {len(meta.get('tags', []))} tags")
    print(f"  Desc lines: {len(meta['description'].splitlines())}")
    print("  Setting video to public…")
    set_public_with_meta(token, VIDEO_ID, meta)
    print(f"✓ Published!")
    print(f"  URL: https://www.youtube.com/watch?v={VIDEO_ID}")

    # Record
    record = {
        "episode_id": "PD-2026-001-miranda",
        "event": "published",
        "video_id": VIDEO_ID,
        "url": f"https://www.youtube.com/watch?v={VIDEO_ID}",
        "privacy": "public",
        "thumbnail": THUMB_FILE.name,
        "thumbnail_via_api": thumb_ok,
        "published_at": "2026-06-15T00:00:00Z",
        "approval_ref": "APR-0004",
    }
    out = EPISODE_DIR / "events" / "publish_v021.json"
    out.write_text(json.dumps(record, indent=2, ensure_ascii=False))
    print(f"  record: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
