#!/usr/bin/env python3
r"""Upload PD-2026-002-gideon to YouTube as PRIVATE (public is a separate human step), set the
click thumbnail. Reuses the resumable-upload helpers from upload_episode.py.

Guards (same as upload_episode): APR-0004 approved + SHA256 match + channel allowlist + force private.
    py -3.11 scripts/upload_gideon.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import get_channel_id, initiate_upload, upload_chunks, sha256_file, CHANNEL_ALLOWLIST  # reuse

EP = "PD-2026-002-gideon"
EPDIR = ROOT / "episodes" / EP
META = EPDIR / "09_package" / "youtube_meta.v001.json"
APR = EPDIR / "approvals" / "APR-0004.json"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
VIDEO = MEDIA / "episodes" / EP / "08_edit" / "gideon_premium_v001.mp4"
THUMB = ROOT / "remotion" / "out" / "thumb_click_a.png"


def set_thumbnail(token: str, video_id: str, png: Path):
    url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}"
    req = urllib.request.Request(url, data=png.read_bytes(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "image/png"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    apr = json.loads(APR.read_text("utf-8"))
    if apr.get("decision") != "approved":
        print(f"BLOCKED: APR-0004 decision={apr.get('decision')!r}"); return 1
    print("✓ APR-0004 approved (publish authorization, private upload)")
    if not VIDEO.exists():
        print(f"BLOCKED: missing {VIDEO}"); return 1
    expected = json.loads(META.read_text("utf-8"))["safety_checklist"]["final_cut_hash"]
    print(f"  verifying SHA256 of {VIDEO.name} ({VIDEO.stat().st_size/1e6:.0f} MB)…")
    actual = sha256_file(VIDEO)
    if actual != expected:
        print(f"BLOCKED: hash mismatch\n  expected {expected}\n  actual   {actual}"); return 1
    print("✓ SHA256 matches approved hash")
    meta = json.loads(META.read_text("utf-8"))

    if args.dry_run:
        print("\n[dry-run] guards passed; no upload."); return 0

    env = load_env(); token = _access_token(env)
    ch = get_channel_id(token)
    if ch not in CHANNEL_ALLOWLIST:
        print(f"BLOCKED: channel {ch!r} not allowlisted"); return 1
    print(f"✓ channel {ch}")

    upload_url = initiate_upload(token, meta, VIDEO.stat().st_size)
    print("✓ resumable session started; uploading (PRIVATE)…")
    video_id = upload_chunks(upload_url, token, VIDEO)
    print(f"✓ uploaded — video_id={video_id}  (PRIVATE)")

    try:
        set_thumbnail(token, video_id, THUMB)
        print("✓ click thumbnail set (thumb_click_a)")
    except Exception as e:
        print(f"! thumbnail set failed (set manually): {e}")

    # record the upload id
    (EPDIR / "09_package" / "upload_result.json").write_text(json.dumps(
        {"video_id": video_id, "visibility": "private",
         "url": f"https://studio.youtube.com/video/{video_id}/edit",
         "watch": f"https://youtu.be/{video_id}"}, indent=2) + "\n", "utf-8")
    print(f"\nPRIVATE: https://youtu.be/{video_id}\nStudio:  https://studio.youtube.com/video/{video_id}/edit")
    print("Public flip is the separate owner step (publish_episode / Studio).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
