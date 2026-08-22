#!/usr/bin/env python3
"""Schedule EP39 frazier to YouTube (private, auto-publish at publishAt).

Guards (fail closed): APR-0001 approved + video sha256 match + channel allowlist.
Flow: resumable private upload -> set thumbnail -> schedule (status.publishAt) ->
upload English caption. Writes 09_package/youtube_schedule_result.v001.json.

    py -3.11 scripts/schedule_frazier.py --dry-run
    py -3.11 scripts/schedule_frazier.py
"""
from __future__ import annotations
import argparse, json, sys, time
import urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import sha256_file, get_channel_id, upload_chunks  # reuse verified helpers

EP = "PD-2026-039-frazier"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
META_PATH = PKG / "youtube_meta.v001.json"
APR_PATH = EPDIR / "approvals" / "APR-0001.json"
VIDEO_FILE = Path("E:/pd-media/episodes/PD-2026-039-frazier/08_edit/frazier_final_bgm.v002_ae.mp4")
THUMB_FILE = PKG / "thumbnail.selected.v003.png"
CAPTION_FILE = EPDIR / "08_edit" / "captions.final.v001.srt"
EXPECTED_HASH = "8a7aa7144871a663a04097bb170c8e6bce8e49df57d4fb1cb0abd3315859559c"
PUBLISH_AT = "2026-07-24T03:00:00Z"
SCHEDULED_LOCAL = "2026-07-24T12:00:00+09:00"
CHANNEL_ALLOWLIST = {"UCuQPtAz1rca9eJ4xhvX0yKA"}


def req_json(url, token, data=None, headers=None, method=None):
    r = urllib.request.Request(url, data=data,
        headers={"Authorization": f"Bearer {token}", **(headers or {})}, method=method)
    with urllib.request.urlopen(r, timeout=120) as resp:
        raw = resp.read().decode()
        return json.loads(raw) if raw else {}


def initiate_upload(token, meta, size):
    snippet = {"title": meta["title"], "description": meta["description"],
               "tags": meta.get("tags", []), "categoryId": str(meta.get("category_id", "27")),
               "defaultLanguage": "en", "defaultAudioLanguage": "en"}
    body = json.dumps({"snippet": snippet,
        "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False}}).encode()
    r = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=body, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json",
        "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)}, method="POST")
    with urllib.request.urlopen(r, timeout=30) as resp:
        return resp.headers.get("Location", "")


def set_thumbnail(token, video_id):
    data = THUMB_FILE.read_bytes()
    r = urllib.request.Request(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        data=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "image/png"}, method="POST")
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.loads(resp.read().decode())


def schedule_publish(token, video_id):
    body = json.dumps({"id": video_id,
        "status": {"privacyStatus": "private", "publishAt": PUBLISH_AT, "selfDeclaredMadeForKids": False}}).encode()
    return req_json("https://www.googleapis.com/youtube/v3/videos?part=status", token,
                    data=body, headers={"Content-Type": "application/json"}, method="PUT")


def upload_caption(token, video_id):
    boundary = f"frazier_caption_{int(time.time())}"
    metadata = {"snippet": {"videoId": video_id, "language": "en", "name": "English", "isDraft": False}}
    body = b"".join([f"--{boundary}\r\n".encode(),
        b"Content-Type: application/json; charset=UTF-8\r\n\r\n",
        json.dumps(metadata).encode(), b"\r\n", f"--{boundary}\r\n".encode(),
        b"Content-Type: application/octet-stream\r\n\r\n", CAPTION_FILE.read_bytes(), b"\r\n",
        f"--{boundary}--\r\n".encode()])
    return req_json("https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
                    token, data=body, headers={"Content-Type": f"multipart/related; boundary={boundary}"}, method="POST")


def main(argv):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    # Guard 1: APR
    if not APR_PATH.exists():
        print("BLOCKED: APR-0001.json not found."); return 1
    apr = json.loads(APR_PATH.read_text(encoding="utf-8"))
    if apr.get("decision") != "approved":
        print(f"BLOCKED: APR-0001 decision={apr.get('decision')!r}"); return 1
    if apr.get("decided_by") != "owner":
        print(f"BLOCKED: APR-0001 decided_by={apr.get('decided_by')!r}"); return 1
    print("OK APR-0001 approved by owner")
    # Guard 2: files
    for f in (VIDEO_FILE, THUMB_FILE, META_PATH, CAPTION_FILE):
        if not f.exists(): print(f"BLOCKED: missing {f}"); return 1
    # Guard 3: hash
    print(f"  verifying sha256 ({VIDEO_FILE.stat().st_size/1e6:.0f} MB)...")
    actual = sha256_file(VIDEO_FILE)
    if actual != EXPECTED_HASH:
        print(f"BLOCKED: hash mismatch\n  expected {EXPECTED_HASH}\n  actual   {actual}"); return 1
    apr_sha = apr.get("content_hash", apr.get("video_sha256", "")).replace("sha256:", "")
    if apr_sha != EXPECTED_HASH:
        print("BLOCKED: APR sha does not match render sha"); return 1
    print("OK sha256 matches APR")
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))

    env = load_env(); token = _access_token(env)
    print("OK access token")
    ch = get_channel_id(token)
    if ch not in CHANNEL_ALLOWLIST:
        print(f"BLOCKED: channel {ch} not allowlisted"); return 1
    print(f"OK channel {ch}")

    if args.dry_run:
        print("\n[dry-run] all guards + auth + channel verified. No upload performed.")
        print(f"[dry-run] would upload {VIDEO_FILE.name}, thumb={THUMB_FILE.name}, publishAt={PUBLISH_AT}, caption={CAPTION_FILE.name}.")
        return 0

    size = VIDEO_FILE.stat().st_size
    print(f"  initiating resumable upload ({size/1e6:.0f} MB) ...")
    up_url = initiate_upload(token, meta, size)
    if not up_url.startswith("https://www.googleapis.com/"):
        print(f"BLOCKED: bad upload url {up_url[:60]}"); return 1
    video_id = upload_chunks(up_url, token, VIDEO_FILE)
    if not video_id:
        print("FAIL: no video_id after upload"); return 1
    print(f"OK uploaded video_id={video_id} (private)")

    thumb_ok = False
    try:
        set_thumbnail(token, video_id); thumb_ok = True; print("OK thumbnail set")
    except Exception as e:
        print(f"WARN thumbnail: {str(e)[:120]}")
    try:
        schedule_publish(token, video_id); print(f"OK scheduled publishAt={PUBLISH_AT}")
    except Exception as e:
        print(f"WARN schedule (retry once): {str(e)[:120]}")
        time.sleep(5)
        schedule_publish(token, video_id); print(f"OK scheduled publishAt={PUBLISH_AT} (retry)")
    cap_ok = False; cap_err = None
    for attempt in range(3):
        try:
            upload_caption(token, video_id); cap_ok = True; print("OK caption uploaded"); break
        except Exception as e:
            cap_err = str(e)[:150]; time.sleep(15)
    if not cap_ok:
        print(f"WARN caption not uploaded (add in Studio): {cap_err}")

    result = {"schema_version": "1.0.0", "episode_id": EP, "mode": "scheduled",
        "video_id": video_id, "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "channel_id": ch, "privacy": "private", "publishAt": PUBLISH_AT,
        "scheduled_at_local": SCHEDULED_LOCAL, "title": meta["title"], "category_id": str(meta.get("category_id", "27")),
        "video_sha256": "sha256:" + EXPECTED_HASH, "thumbnail_file": THUMB_FILE.name, "thumbnail_set": thumb_ok,
        "captions_uploaded": cap_ok, "caption_error": cap_err,
        "approval_ref": "APR-0001", "external_upload": True}
    (PKG / "youtube_schedule_result.v001.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (EPDIR / "events").mkdir(exist_ok=True)
    (EPDIR / "events" / "schedule_v001.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSCHEDULED  {result['watch']}  publishAt {PUBLISH_AT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
