#!/usr/bin/env python3
"""Finalize the ALREADY-UPLOADED EP40 lech video (4uuY6G0LmHo).

The prior agent uploaded the private video successfully (video_id 4uuY6G0LmHo,
title matches, sha bound by APR-0002) but died before setting the thumbnail,
scheduling publishAt, and uploading the caption. Re-running schedule_lech.py
would create a DUPLICATE upload. This finalizer targets the existing id only:
set thumbnail -> schedule publishAt -> upload caption -> write result file.

    py -3.11 scripts/finalize_lech_existing_v001.py
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from schedule_lech import (
    set_thumbnail, schedule_publish, upload_caption, get_channel_id,
    EP, PKG, META_PATH, THUMB_FILE, CAPTION_FILE, PUBLISH_AT, SCHEDULED_LOCAL,
    CHANNEL_ALLOWLIST, EXPECTED_HASH, EPDIR,
)

VIDEO_ID = "4uuY6G0LmHo"


def main():
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    for f in (THUMB_FILE, META_PATH, CAPTION_FILE):
        if not f.exists():
            print(f"BLOCKED: missing {f}"); return 1
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    env = load_env(); token = _access_token(env)
    ch = get_channel_id(token)
    if ch not in CHANNEL_ALLOWLIST:
        print(f"BLOCKED: channel {ch} not allowlisted"); return 1
    print(f"OK channel {ch} | targeting existing video {VIDEO_ID}")

    thumb_ok = False
    try:
        set_thumbnail(token, VIDEO_ID); thumb_ok = True; print("OK thumbnail set")
    except Exception as e:
        print(f"WARN thumbnail: {str(e)[:160]}")
    try:
        schedule_publish(token, VIDEO_ID); print(f"OK scheduled publishAt={PUBLISH_AT}")
    except Exception as e:
        print(f"WARN schedule (retry once): {str(e)[:160]}")
        time.sleep(5)
        schedule_publish(token, VIDEO_ID); print(f"OK scheduled publishAt={PUBLISH_AT} (retry)")
    cap_ok = False; cap_err = None
    for _ in range(3):
        try:
            upload_caption(token, VIDEO_ID); cap_ok = True; print("OK caption uploaded"); break
        except Exception as e:
            cap_err = str(e)[:160]; time.sleep(15)
    if not cap_ok:
        print(f"WARN caption not uploaded (add in Studio): {cap_err}")

    result = {"schema_version": "1.0.0", "episode_id": EP, "mode": "scheduled",
        "video_id": VIDEO_ID, "watch": f"https://youtu.be/{VIDEO_ID}",
        "studio": f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        "channel_id": ch, "privacy": "private", "publishAt": PUBLISH_AT,
        "scheduled_at_local": SCHEDULED_LOCAL, "title": meta["title"],
        "category_id": str(meta.get("category_id", "27")),
        "video_sha256": "sha256:" + EXPECTED_HASH, "thumbnail_file": THUMB_FILE.name,
        "thumbnail_set": thumb_ok, "captions_uploaded": cap_ok, "caption_error": cap_err,
        "approval_ref": "APR-0002", "supersedes": "APR-0001", "external_upload": True,
        "note": "finalized existing upload; prior agent uploaded then died before scheduling"}
    (PKG / "youtube_schedule_result.v001.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (EPDIR / "events").mkdir(exist_ok=True)
    (EPDIR / "events" / "schedule_v001.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSCHEDULED  {result['watch']}  publishAt {PUBLISH_AT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
