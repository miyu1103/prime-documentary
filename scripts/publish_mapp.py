#!/usr/bin/env python3
"""Set thumbnail and publish the Mapp video to PUBLIC. Guarded (APR-0004, hash, thumbnail).
Owner durably authorized (APR-0004 + '公開で' + '任せる', 2026-06-18). Mirrors publish_episode.py."""
from __future__ import annotations
import argparse, hashlib, json, sys, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

VIDEO_ID      = "An0to4U0hJQ"
EXPECTED_HASH = "d153a16f08f74e0322190267d2640f88a45629dfbe69bea21d355c4f957b6abe"
VIDEO_FILE    = Path(r"H:\pd-media\episodes\PD-2026-003-mapp\08_edit\mapp_premium_v002.mp4")
THUMB_FILE    = ROOT / "remotion" / "out" / "thumb_mapp_a.png"
EPISODE_DIR   = ROOT / "episodes" / "PD-2026-003-mapp"
APR_PATH      = EPISODE_DIR / "approvals" / "APR-0004.json"
META_PATH     = EPISODE_DIR / "09_package" / "youtube_meta.v001.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def upload_thumbnail(token: str, video_id: str, thumb_path: Path) -> None:
    data = thumb_path.read_bytes()
    url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails?videoId={video_id}&uploadType=media"
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "image/png"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        json.loads(resp.read().decode())


def set_public_with_meta(token: str, video_id: str, meta: dict) -> None:
    payload = {"id": video_id,
        "snippet": {"title": meta["title"], "description": meta["description"], "tags": meta.get("tags", []),
            "categoryId": "27", "defaultLanguage": "en", "defaultAudioLanguage": "en"},
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}
    req = urllib.request.Request("https://www.googleapis.com/youtube/v3/videos?part=snippet,status",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="PUT")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
    if result.get("status", {}).get("privacyStatus") != "public":
        raise RuntimeError(f"Expected public, got: {result.get('status', {}).get('privacyStatus')}")


def main(argv: list[str]) -> int:
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    p = argparse.ArgumentParser(); p.add_argument("--dry-run", action="store_true"); args = p.parse_args(argv)
    apr = json.loads(APR_PATH.read_text(encoding="utf-8"))
    if apr.get("decision") != "approved":
        print("BLOCKED: APR-0004 not approved"); return 1
    print("APR-0004 approved")
    if sha256_file(VIDEO_FILE) != EXPECTED_HASH:
        print("BLOCKED: hash mismatch"); return 1
    print("SHA256 verified")
    if not THUMB_FILE.exists():
        print(f"BLOCKED: thumbnail not found: {THUMB_FILE}"); return 1
    print(f"thumbnail found ({THUMB_FILE.stat().st_size//1024} KB)")
    if args.dry_run:
        print("[dry-run] guards passed; no changes."); return 0
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    env = load_env(); token = _access_token(env); print("access token obtained")
    try:
        upload_thumbnail(token, VIDEO_ID, THUMB_FILE); print("thumbnail set")
    except urllib.error.HTTPError as exc:
        print(f"thumbnails.set HTTP {exc.code} — set manually in Studio if needed")
    set_public_with_meta(token, VIDEO_ID, meta)
    url = f"https://www.youtube.com/watch?v={VIDEO_ID}"
    print(f"PUBLISHED public!\n  URL: {url}")
    (EPISODE_DIR / "events" / "publish_v002.json").write_text(json.dumps(
        {"episode_id": "PD-2026-003-mapp", "event": "published", "video_id": VIDEO_ID, "url": url,
         "privacy": "public", "thumbnail": THUMB_FILE.name, "approval_ref": "APR-0004"}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
