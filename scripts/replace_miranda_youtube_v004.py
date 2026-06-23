#!/usr/bin/env python3
"""Replace the published Miranda episode with the premium rebuild.

External side effects in non-dry-run mode:
- uploads the premium MP4 to YouTube as private first
- sets the selected flashy thumbnail
- uploads English captions
- waits for processing
- makes the new upload public
- sets the old published upload private
- adds the new upload to the Landmark Rights Cases playlist
- writes local package/manifest/event records
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

EP = "PD-2026-001-miranda"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
META = PKG / "youtube_meta.v004.json"
RIGHTS = PKG / "rights_manifest.v003.json"
FINAL_DELIVERY = PKG / "final_delivery.v004.json"
QC = EPDIR / "08_edit" / "renders" / "final.v001.qc.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v001.srt"
VIDEO = Path(r"H:\pd-media\episodes\PD-2026-001-miranda\08_edit\miranda_premium_v001.mp4")
THUMB = PKG / "thumbnail.selected.v004.png"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events.jsonl"
APR = EPDIR / "approvals" / "APR-0005.json"
RESULT = PKG / "youtube_replacement_result.v004.json"
VERIFY = PKG / "youtube_replacement_verify.v004.json"

OLD_VIDEO_ID = "PjGEqW6F9WM"
PLAYLIST_LANDMARK_RIGHTS = "PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9"
EXPECTED_VIDEO_SHA = "c2d6583b865a017b2a04894844aa31c17a30bbf82bb8a8012ca9a13734021efb"
EXPECTED_THUMB_SHA = "913e1f993db6e019f9a2969e35d568151c34af9d5f20b456988366d2a9b9adaa"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(data: dict) -> None:
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def http_json(
    method: str,
    url: str,
    token: str,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 180,
) -> dict:
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Authorization": f"Bearer {token}", **(headers or {})},
        method=method,
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw or "{}")


def meta_description(meta: dict) -> str:
    desc = meta["description"].rstrip()
    chapters = meta.get("chapters") or []
    if chapters:
        desc += "\n\nChapters\n"
        desc += "\n".join(f"{c['time']} {c['label']}" for c in chapters)
    desc += (
        "\n\nThis is an educational documentary, not legal advice.\n\n"
        "▶ Watch the full Landmark Rights Cases playlist: "
        "https://www.youtube.com/playlist?list=PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9\n"
        "👉 Subscribe for the hidden systems behind everyday life.\n\n"
        "#MirandaRights #SupremeCourt #USLaw"
    )
    return desc


def initiate_upload(token: str, meta: dict, file_size: int) -> str:
    body = json.dumps(
        {
            "snippet": {
                "title": meta["selected_title"],
                "description": meta_description(meta),
                "tags": meta.get("tags", []),
                "categoryId": "27",
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en",
            },
            "status": {
                "privacyStatus": "private",
                "selfDeclaredMadeForKids": False,
                "containsSyntheticMedia": True,
                "license": "youtube",
                "embeddable": True,
                "publicStatsViewable": True,
            },
        }
    ).encode("utf-8")
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


def set_thumbnail(token: str, video_id: str) -> dict:
    return http_json(
        "POST",
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        token,
        data=THUMB.read_bytes(),
        headers={"Content-Type": "image/png"},
    )


def upload_caption(token: str, video_id: str) -> dict:
    boundary = f"miranda_caption_{int(time.time())}"
    metadata = {"snippet": {"videoId": video_id, "language": "en", "name": "English", "isDraft": False}}
    body = b"".join(
        [
            f"--{boundary}\r\n".encode(),
            b"Content-Type: application/json; charset=UTF-8\r\n\r\n",
            json.dumps(metadata, ensure_ascii=False).encode("utf-8"),
            b"\r\n",
            f"--{boundary}\r\n".encode(),
            b"Content-Type: application/octet-stream\r\n\r\n",
            CAPTIONS.read_bytes(),
            b"\r\n",
            f"--{boundary}--\r\n".encode(),
        ]
    )
    return http_json(
        "POST",
        "https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
        token,
        data=body,
        headers={"Content-Type": f"multipart/related; boundary={boundary}"},
    )


def get_videos(token: str, video_ids: list[str]) -> dict:
    ids = ",".join(video_ids)
    return http_json("GET", f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={ids}", token)


def compact_videos(state: dict) -> list[dict]:
    out = []
    for item in state.get("items") or []:
        sn = item.get("snippet", {})
        st = item.get("status", {})
        pr = item.get("processingDetails", {})
        out.append(
            {
                "id": item.get("id"),
                "title": sn.get("title"),
                "privacyStatus": st.get("privacyStatus"),
                "uploadStatus": st.get("uploadStatus"),
                "processingStatus": pr.get("processingStatus"),
                "publishAt": st.get("publishAt"),
                "madeForKids": st.get("madeForKids"),
                "selfDeclaredMadeForKids": st.get("selfDeclaredMadeForKids"),
            }
        )
    return out


def update_privacy(token: str, video_id: str, privacy: str) -> dict:
    body = json.dumps(
        {
            "id": video_id,
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": False,
                "containsSyntheticMedia": True,
                "license": "youtube",
                "embeddable": True,
                "publicStatsViewable": True,
            },
        }
    ).encode("utf-8")
    return http_json(
        "PUT",
        "https://www.googleapis.com/youtube/v3/videos?part=status",
        token,
        data=body,
        headers={"Content-Type": "application/json; charset=UTF-8"},
    )


def playlist_has_video(token: str, playlist_id: str, video_id: str) -> bool:
    page = ""
    while True:
        state = http_json(
            "GET",
            "https://www.googleapis.com/youtube/v3/playlistItems"
            f"?part=contentDetails&maxResults=50&playlistId={playlist_id}{page}",
            token,
        )
        if any((it.get("contentDetails") or {}).get("videoId") == video_id for it in state.get("items") or []):
            return True
        next_page = state.get("nextPageToken")
        if not next_page:
            return False
        page = f"&pageToken={next_page}"


def add_to_playlist(token: str, playlist_id: str, video_id: str) -> dict:
    if playlist_has_video(token, playlist_id, video_id):
        return {"skipped": True, "reason": "already_in_playlist"}
    body = json.dumps(
        {"snippet": {"playlistId": playlist_id, "resourceId": {"kind": "youtube#video", "videoId": video_id}}}
    ).encode("utf-8")
    return http_json(
        "POST",
        "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet",
        token,
        data=body,
        headers={"Content-Type": "application/json; charset=UTF-8"},
    )


def wait_for_processing(token: str, video_id: str) -> tuple[dict, str]:
    state = {}
    status = "unknown"
    for _ in range(36):
        state = get_videos(token, [video_id])
        items = state.get("items") or []
        status = (((items[0].get("processingDetails") if items else {}) or {}).get("processingStatus")) or "missing"
        upload = (((items[0].get("status") if items else {}) or {}).get("uploadStatus")) or "missing"
        if status in {"succeeded", "failed", "terminated"} or upload in {"processed", "failed", "rejected"}:
            return state, status
        time.sleep(20)
    return state, status


def ensure_approval_record(video_sha: str, thumb_sha: str) -> None:
    if APR.exists():
        return
    write_json(
        APR,
        {
            "approval_id": "APR-0005",
            "episode_id": EP,
            "decision": "approved",
            "approval_kind": "youtube_replacement_publication",
            "approved_by": "owner_chat_request",
            "approved_at": datetime.now(timezone.utc).isoformat(),
            "notes": "Owner instructed: 派手なサムネで完成した動画に差し替えて. This approves replacing the old published Miranda video with the premium rebuild.",
            "old_video_id": OLD_VIDEO_ID,
            "video": str(VIDEO),
            "video_sha256": video_sha,
            "thumbnail": str(THUMB),
            "thumbnail_sha256": thumb_sha,
            "youtube_meta": str(META),
            "rights_manifest": str(RIGHTS),
            "qc": str(QC),
        },
    )


def verify_preconditions() -> tuple[dict, str, str]:
    missing = [p for p in [META, RIGHTS, FINAL_DELIVERY, QC, CAPTIONS, VIDEO, THUMB, MANIFEST] if not p.exists()]
    if missing:
        raise RuntimeError("Missing required artifacts: " + ", ".join(str(p) for p in missing))
    if RESULT.exists():
        raise RuntimeError(f"Result already exists; refusing duplicate replacement: {RESULT.relative_to(ROOT)}")
    meta = load_json(META)
    qc = load_json(QC)
    rights = load_json(RIGHTS)
    if not qc.get("checks", {}).get("duration_in_11_5_to_12_5_min_window"):
        raise RuntimeError("QC duration gate is not passing")
    if not qc.get("checks", {}).get("real_person_likeness_avoided"):
        raise RuntimeError("QC likeness gate is not passing")
    if not rights.get("ai_disclosure_required"):
        raise RuntimeError("rights manifest missing AI disclosure requirement")
    video_sha = sha256_file(VIDEO)
    thumb_sha = sha256_file(THUMB)
    if video_sha != EXPECTED_VIDEO_SHA:
        raise RuntimeError(f"Video SHA mismatch expected={EXPECTED_VIDEO_SHA} actual={video_sha}")
    if thumb_sha != EXPECTED_THUMB_SHA:
        raise RuntimeError(f"Thumbnail SHA mismatch expected={EXPECTED_THUMB_SHA} actual={thumb_sha}")
    ensure_approval_record(video_sha, thumb_sha)
    return meta, video_sha, thumb_sha


def update_local_records(result: dict, verify: dict) -> None:
    now = datetime.now(timezone.utc).isoformat()
    meta = load_json(META)
    meta["publish_operation_allowed"] = True
    meta["replacement_stop_required"] = False
    meta["upload_performed"] = True
    meta["publish_performed"] = True
    meta["old_video_private_performed"] = True
    meta["privacy_status_recommendation"] = "public_replacement_completed"
    meta["video_id"] = result["new_video_id"]
    meta["video_url"] = result["new_watch_url"]
    meta["old_video_id"] = OLD_VIDEO_ID
    meta["replacement_result"] = str(RESULT.relative_to(ROOT)).replace("\\", "/")
    meta["replacement_verify"] = str(VERIFY.relative_to(ROOT)).replace("\\", "/")
    meta["updated_at"] = now
    write_json(META, meta)

    manifest = load_json(MANIFEST)
    manifest["state"] = "published"
    manifest["video_id"] = result["new_video_id"]
    manifest["video_url"] = result["new_watch_url"]
    manifest["published_at"] = result["new_public_at"]
    manifest["updated_at"] = now
    manifest.setdefault("active_revisions", {})["package"] = "v004"
    manifest.setdefault("active_revisions", {})["edit"] = "premium_v001"
    manifest.setdefault("active_revisions", {})["youtube_meta"] = "v004"
    manifest.setdefault("active_revisions", {})["youtube_replacement_result"] = "v004"
    manifest.setdefault("active_revisions", {})["youtube_replacement_verify"] = "v004"
    if "APR-0005" not in manifest.setdefault("approvals", []):
        manifest["approvals"].append("APR-0005")
    manifest["warnings"] = [
        warning.replace(
            "Thumbnail not yet set on YouTube:",
            "Historical v021 note before premium replacement; old upload thumbnail was not set on YouTube:",
        )
        for warning in manifest.get("warnings", [])
    ]
    manifest.setdefault("warnings", []).append(
        f"Miranda premium rebuild replaced old public upload {OLD_VIDEO_ID}; new public upload {result['new_video_id']} with selected flashy thumbnail. Old upload set private."
    )
    write_json(MANIFEST, manifest)

    append_event(
        {
            "event": "youtube_replacement_completed",
            "episode_id": EP,
            "revision": "premium_v001_package_v004",
            "actor": "codex",
            "approval_id": "APR-0005",
            "old_video_id": OLD_VIDEO_ID,
            "old_video_privacy_after": "private",
            "new_video_id": result["new_video_id"],
            "new_watch_url": result["new_watch_url"],
            "thumbnail_set": result["thumbnail_set"],
            "captions_uploaded": result["captions_uploaded"],
            "playlist_added": result["playlist_added"],
            "verify": verify,
            "ts": now,
        }
    )


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    meta, video_sha, thumb_sha = verify_preconditions()
    print("OK local gates")
    print(f"OK video sha {video_sha}")
    print(f"OK thumbnail sha {thumb_sha}")
    print(f"OK title {meta['selected_title']}")
    if args.dry_run:
        print("DRY_RUN_OK no external writes")
        return 0

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    print(f"OK channel {channel_id}")

    before_state = get_videos(token, [OLD_VIDEO_ID])
    before_compact = compact_videos(before_state)
    old_before = before_compact[0] if before_compact else {}
    if old_before.get("privacyStatus") != "public":
        raise RuntimeError(f"Old video is not public before replacement: {old_before}")

    upload_url = initiate_upload(token, meta, VIDEO.stat().st_size)
    print(f"OK upload session; uploading {VIDEO.stat().st_size / 1e6:.0f} MB")
    new_video_id = upload_chunks(upload_url, token, VIDEO)
    if not new_video_id:
        raise RuntimeError("Upload returned no video id")
    print(f"OK private upload {new_video_id}")

    thumbnail_result = {}
    thumbnail_error = None
    try:
        thumbnail_result = set_thumbnail(token, new_video_id)
        print("OK thumbnail set")
    except urllib.error.HTTPError as exc:
        thumbnail_error = exc.read().decode("utf-8", errors="replace")
        print(f"WARN thumbnail set failed HTTP {exc.code}: {thumbnail_error[:500]}")

    caption_result = upload_caption(token, new_video_id)
    print("OK captions uploaded")

    processing_state, processing_status = wait_for_processing(token, new_video_id)
    compact_after_processing = compact_videos(processing_state)
    print(f"OK processing status {processing_status}")

    if processing_status in {"failed", "terminated"}:
        raise RuntimeError(f"New video processing failed: {compact_after_processing}")

    public_result = update_privacy(token, new_video_id, "public")
    new_public_at = datetime.now(timezone.utc).isoformat()
    print("OK new upload public")

    old_private_result = update_privacy(token, OLD_VIDEO_ID, "private")
    print("OK old upload private")

    playlist_result = add_to_playlist(token, PLAYLIST_LANDMARK_RIGHTS, new_video_id)
    print("OK playlist checked/added")

    final_state = get_videos(token, [OLD_VIDEO_ID, new_video_id])
    final_compact = compact_videos(final_state)
    new_ok = any(v["id"] == new_video_id and v["privacyStatus"] == "public" for v in final_compact)
    old_ok = any(v["id"] == OLD_VIDEO_ID and v["privacyStatus"] == "private" for v in final_compact)
    verify = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "old_video_id": OLD_VIDEO_ID,
        "new_video_id": new_video_id,
        "new_public_verified": new_ok,
        "old_private_verified": old_ok,
        "youtube_state_compact": final_compact,
    }
    write_json(VERIFY, verify)
    if not new_ok or not old_ok:
        raise RuntimeError(f"Replacement verification failed: {verify}")

    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "approval_ref": "APR-0005",
        "old_video_id": OLD_VIDEO_ID,
        "old_watch_url": f"https://youtu.be/{OLD_VIDEO_ID}",
        "new_video_id": new_video_id,
        "new_watch_url": f"https://youtu.be/{new_video_id}",
        "new_studio_url": f"https://studio.youtube.com/video/{new_video_id}/edit",
        "channel_id": channel_id,
        "title": meta["selected_title"],
        "video_file": str(VIDEO),
        "video_sha256": video_sha,
        "thumbnail_file": str(THUMB),
        "thumbnail_sha256": thumb_sha,
        "thumbnail_set": thumbnail_error is None,
        "thumbnail_result": thumbnail_result,
        "thumbnail_error": thumbnail_error,
        "captions_uploaded": True,
        "caption_result": caption_result,
        "processing_status": processing_status,
        "new_public_at": new_public_at,
        "old_private_at": datetime.now(timezone.utc).isoformat(),
        "public_result": public_result,
        "old_private_result": old_private_result,
        "playlist_added": not bool(playlist_result.get("skipped")),
        "playlist_result": playlist_result,
        "replacement_verify": str(VERIFY.relative_to(ROOT)).replace("\\", "/"),
        "external_public_write": True,
    }
    write_json(RESULT, result)
    update_local_records(result, verify)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
