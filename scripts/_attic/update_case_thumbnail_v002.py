#!/usr/bin/env python3
"""Replace a scheduled/uploaded PD case video's thumbnail with the v002 CTR design.

Reads the episode's youtube_schedule_result to get the video_id, verifies the channel is
allowlisted, and calls thumbnails.set with 09_package/thumbnail.selected.v002.png. Idempotent
in effect (setting the same image twice is harmless); records the swap in the result json.

    python scripts/update_case_thumbnail_v002.py --ep kyllo|katz|rodriguez [--dry-run]
"""
from __future__ import annotations
import argparse, json, mimetypes, ssl, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id, sha256_file

EPMAP = {"kyllo": "PD-2026-025-kyllo", "katz": "PD-2026-026-katz", "rodriguez": "PD-2026-027-rodriguez"}


def set_thumbnail(token, vid, path, max_fail=12):
    """thumbnails.set with retry — the local network drops SSL intermittently. The call is
    idempotent (same image), so re-sending after a drop is safe."""
    ct = mimetypes.guess_type(path.name)[0] or "image/png"
    data = path.read_bytes()
    fails = 0
    while True:
        req = urllib.request.Request(f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
                                     data=data, method="POST",
                                     headers={"Authorization": f"Bearer {token}", "Content-Type": ct})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode())
        except (urllib.error.URLError, ssl.SSLError, TimeoutError, ConnectionError, OSError) as e:
            fails += 1
            if fails > max_fail:
                raise RuntimeError(f"thumbnail set aborted after {fails} network failures: {e}")
            wait = min(2 ** fails, 30)
            print(f"  net drop on thumbnail set — retry {fails} in {wait}s ({type(e).__name__})")
            time.sleep(wait)


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True, choices=sorted(EPMAP))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    ep = EPMAP[args.ep]
    pkg = ROOT / "episodes" / ep / "09_package"
    result = pkg / "youtube_schedule_result.v001.json"
    thumb = pkg / "thumbnail.selected.v002.png"
    if not result.exists():
        raise RuntimeError(f"no schedule result yet: {result} (schedule the video first)")
    if not thumb.exists():
        raise RuntimeError(f"missing {thumb}")
    if thumb.stat().st_size >= 2 * 1024 * 1024:
        raise RuntimeError("thumbnail >= 2MB")
    res = json.loads(result.read_text("utf-8"))
    vid = res["video_id"]
    print(f"OK {ep}: video_id={vid} thumb={thumb.name} ({thumb.stat().st_size/1024:.0f} KB)")
    if args.dry_run:
        print("DRY_RUN_OK no external writes")
        return 0
    token = _access_token(load_env())
    ch = get_channel_id(token)
    if ch not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"channel {ch} not allowlisted")
    set_thumbnail(token, vid, thumb)
    print("OK thumbnail replaced with v002")
    res["thumbnail_v002_set"] = True
    res["thumbnail_v002_sha256"] = "sha256:" + sha256_file(thumb)
    res["thumbnail_v002_set_at"] = datetime.now(timezone.utc).isoformat()
    result.write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"RESULT updated {result.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
