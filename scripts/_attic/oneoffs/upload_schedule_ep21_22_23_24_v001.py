#!/usr/bin/env python3
"""Upload and schedule EP21, EP22, EP23, and EP24.

This is intentionally one-off: the owner requested exact public schedules in
the current thread. It still verifies the real acceptance gate before each
external upload and records the resulting YouTube state in each episode package.
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id, sha256_file, upload_chunks


REV = "v001"
RESULT_NAME = f"youtube_schedule_result.owner_batch.{REV}.json"
IN_PROGRESS_NAME = f"youtube_upload_in_progress.owner_batch.{REV}.json"
STATUS_NAME = f"youtube_status_verify.owner_batch.{REV}.json"
CAPTION_RESULT_NAME = f"youtube_captions_result.owner_batch.{REV}.json"
THUMB_RESULT_NAME = f"youtube_thumbnail_result.owner_batch.{REV}.json"


EPISODES: list[dict[str, Any]] = [
    {
        "num": 21,
        "episode_id": "PD-2026-021-dbcooper",
        "video": r"E:\pd-media\episodes\PD-2026-021-dbcooper\08_edit\final.mp4",
        "captions": "episodes/PD-2026-021-dbcooper/08_edit/captions.v001.srt",
        "thumbnail": "episodes/PD-2026-021-dbcooper/09_package/thumbnail.selected.v001.png",
        "title": "D.B. Cooper: The Only Hijacking America Never Solved",
        "description": (
            "D.B. Cooper: The Only Hijacking America Never Solved\n\n"
            "A Prime Documentary episode about the 1971 hijacking, the vanished suspect, "
            "the money trail, and why the FBI suspended the case without naming or "
            "confirming who D.B. Cooper was.\n\n"
            "This episode uses symbolic reconstruction and editorial visuals. No "
            "AI-generated image should be treated as archival footage or photographic evidence."
        ),
        "tags": ["D.B. Cooper", "true crime documentary", "unsolved case", "Prime Documentary"],
        "schedule_local": "2026-07-06T12:00:00+09:00",
        "schedule_utc": "2026-07-06T03:00:00Z",
        "risk_note": "R2 unsolved: no named suspect asserted.",
    },
    {
        "num": 22,
        "episode_id": "PD-2026-022-milken",
        "video": r"E:\pd-media\episodes\PD-2026-022-milken\08_edit\final.mp4",
        "captions": "episodes/PD-2026-022-milken/08_edit/captions.v001.srt",
        "thumbnail": "episodes/PD-2026-022-milken/09_package/thumbnail.selected.v001.png",
        "title": "Michael Milken: Genius, or the Face of Greed?",
        "description_file": "episodes/PD-2026-022-milken/09_package/description.v001.md",
        "tags": ["Michael Milken", "Wall Street documentary", "finance documentary", "Prime Documentary"],
        "schedule_local": "2026-07-07T12:00:00+09:00",
        "schedule_utc": "2026-07-07T03:00:00Z",
        "risk_note": "R3 living public figure: charges and plea distinguished.",
    },
    {
        "num": 23,
        "episode_id": "PD-2026-023-swartz",
        "video": r"E:\pd-media\episodes\PD-2026-023-swartz\08_edit\final.motionfix.v001.mp4",
        "captions": "episodes/PD-2026-023-swartz/08_edit/captions.v001.srt",
        "thumbnail": "episodes/PD-2026-023-swartz/09_package/thumbnail.selected.v001.png",
        "title": "The Internet's Own Boy: Aaron Swartz",
        "description": (
            "The Internet's Own Boy: Aaron Swartz\n\n"
            "A Prime Documentary episode about open knowledge, the law, the JSTOR case, "
            "and the questions Aaron Swartz left behind.\n\n"
            "988 Suicide & Crisis Lifeline -- call or text 988\n\n"
            "This episode uses symbolic reconstruction and editorial visuals. No "
            "AI-generated image should be treated as archival footage or photographic evidence."
        ),
        "tags": ["Aaron Swartz", "internet history", "open knowledge", "Prime Documentary"],
        "schedule_local": "2026-07-08T12:00:00+09:00",
        "schedule_utc": "2026-07-08T03:00:00Z",
        "risk_note": "R3 sensitive: 988 included; no death details in metadata.",
        "sensitive_evidence": "episodes/PD-2026-023-swartz/09_package/EVIDENCE/sensitive_locks.safe_fix.v001.json",
    },
    {
        "num": 24,
        "episode_id": "PD-2026-024-rajaratnam",
        "video": r"E:\pd-media\episodes\PD-2026-024-rajaratnam\08_edit\v001.mp4",
        "captions": "episodes/PD-2026-024-rajaratnam/08_edit/captions.v001.srt",
        "thumbnail": "episodes/PD-2026-024-rajaratnam/09_package/thumbnail.selected.v001.png",
        "title": "The Wiretap That Cracked Wall Street",
        "description": (
            "The Wiretap That Cracked Wall Street\n\n"
            "A Prime Documentary episode about the Raj Rajaratnam insider-trading case, "
            "the wiretap evidence, the trial, and the legal fallout that reshaped Wall "
            "Street's view of information.\n\n"
            "This episode uses symbolic reconstruction and editorial visuals. No "
            "AI-generated image should be treated as archival footage or photographic evidence."
        ),
        "tags": ["Raj Rajaratnam", "Wall Street documentary", "insider trading case", "Prime Documentary"],
        "schedule_local": "2026-07-09T12:00:00+09:00",
        "schedule_utc": "2026-07-09T03:00:00Z",
        "risk_note": "R2 living convicted subject: conviction framed as case record.",
    },
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def sha(path: Path) -> str:
    return "sha256:" + sha256_file(path)


def append_event(epdir: Path, data: dict[str, Any]) -> None:
    events = epdir / "events" / "events.jsonl"
    events.parent.mkdir(parents=True, exist_ok=True)
    with events.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def run_final_gate(num: int) -> dict[str, Any]:
    cmd = [sys.executable, str(ROOT / "scripts" / "check_final_acceptance.py"), str(num), "--json"]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=1200)
    if proc.returncode != 0:
        raise RuntimeError(f"EP{num} final acceptance failed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    data = json.loads(proc.stdout)
    if data.get("status") != "PASS":
        raise RuntimeError(f"EP{num} final acceptance status is not PASS: {data.get('status')!r}")
    return data


def description_for(ep: dict[str, Any]) -> str:
    if ep.get("description_file"):
        return resolve_path(ep["description_file"]).read_text(encoding="utf-8").strip()
    return str(ep["description"]).strip()


def check_public_metadata(ep: dict[str, Any], description: str) -> None:
    title = ep["title"]
    if len(title) > 100:
        raise RuntimeError(f"{ep['episode_id']} title exceeds YouTube limit")
    internal_fragments = ["owner review required", "do not upload", "do not publish", "pending qc", "blocked"]
    combined = f"{title}\n{description}".lower()
    for frag in internal_fragments:
        if frag in combined:
            raise RuntimeError(f"{ep['episode_id']} metadata contains internal fragment: {frag}")
    if ep["num"] == 21:
        banned = ["was d.b. cooper", "was db cooper", "solved the case"]
        if any(x in combined for x in banned):
            raise RuntimeError("EP21 metadata violates unsolved-case lock")
    if ep["num"] == 22:
        banned = ["convicted at trial", "convicted of insider trading", "convicted of racketeering", "convicted of rico", "exonerated"]
        if any(x in combined for x in banned):
            raise RuntimeError("EP22 metadata violates Milken wording lock")
    if ep["num"] == 23:
        banned = ["committed suicide", "caused his death", "caused the death", "method", "note"]
        if any(x in combined for x in banned):
            raise RuntimeError("EP23 metadata violates safe-handling lock")
        if "988 suicide & crisis lifeline -- call or text 988" not in combined:
            raise RuntimeError("EP23 metadata missing required 988 line")
    if ep["num"] == 24:
        banned = ["gupta and rajaratnam", "the $7b profit", "longest sentence" ]
        if any(x in combined for x in banned):
            raise RuntimeError("EP24 metadata violates Rajaratnam wording lock")


def verify_sensitive_evidence(ep: dict[str, Any]) -> None:
    evidence = ep.get("sensitive_evidence")
    if not evidence:
        return
    data = load_json(resolve_path(evidence))
    if data.get("status") != "PASS":
        raise RuntimeError(f"{ep['episode_id']} sensitive lock evidence is not PASS")
    failed = [x for x in data.get("results", []) if not x.get("ok")]
    if failed:
        raise RuntimeError(f"{ep['episode_id']} sensitive lock failures: {failed}")


def upload_caption(token: str, video_id: str, captions: Path, slug: str) -> dict[str, Any]:
    boundary = f"{slug}_caption_{int(time.time())}"
    metadata = {"snippet": {"videoId": video_id, "language": "en", "name": "English", "isDraft": False}}
    body = b"".join(
        [
            f"--{boundary}\r\n".encode(),
            b"Content-Type: application/json; charset=UTF-8\r\n\r\n",
            json.dumps(metadata, ensure_ascii=False).encode("utf-8"),
            b"\r\n",
            f"--{boundary}\r\n".encode(),
            b"Content-Type: application/x-subrip\r\n\r\n",
            captions.read_bytes(),
            b"\r\n",
            f"--{boundary}--\r\n".encode(),
        ]
    )
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": f"multipart/related; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def set_thumbnail(token: str, video_id: str, path: Path) -> dict[str, Any]:
    content_type = mimetypes.guess_type(path.name)[0] or "image/png"
    req = urllib.request.Request(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        data=path.read_bytes(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": content_type},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_video_state(token: str, video_id: str) -> dict[str, Any]:
    req = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={video_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def initiate_upload(token: str, ep: dict[str, Any], description: str, file_size: int) -> str:
    snippet = {
        "title": ep["title"],
        "description": description.rstrip(),
        "tags": ep.get("tags", []),
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
    }
    status = {
        "privacyStatus": "private",
        "publishAt": ep["schedule_utc"],
        "selfDeclaredMadeForKids": False,
        "containsSyntheticMedia": True,
        "license": "youtube",
        "embeddable": True,
        "publicStatsViewable": True,
    }
    body = json.dumps({"snippet": snippet, "status": status}, ensure_ascii=False).encode("utf-8")
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
        raise RuntimeError(f"Unexpected upload URL: {upload_url[:80]}")
    return upload_url


def verify_preconditions(ep: dict[str, Any]) -> dict[str, Any]:
    epdir = ROOT / "episodes" / ep["episode_id"]
    pkg = epdir / "09_package"
    for name in (RESULT_NAME, IN_PROGRESS_NAME):
        if (pkg / name).exists():
            raise RuntimeError(f"{ep['episode_id']} already has {name}; refusing duplicate upload")
    video = resolve_path(ep["video"])
    captions = resolve_path(ep["captions"])
    thumbnail = resolve_path(ep["thumbnail"])
    for path in (video, captions, thumbnail):
        if not path.exists():
            raise RuntimeError(f"{ep['episode_id']} missing required file: {path}")
    gate = run_final_gate(ep["num"])
    description = description_for(ep)
    check_public_metadata(ep, description)
    verify_sensitive_evidence(ep)
    return {
        "episode_id": ep["episode_id"],
        "num": ep["num"],
        "title": ep["title"],
        "description": description,
        "video": video,
        "captions": captions,
        "thumbnail": thumbnail,
        "video_sha256": sha(video),
        "captions_sha256": sha(captions),
        "thumbnail_sha256": sha(thumbnail),
        "schedule_local": ep["schedule_local"],
        "schedule_utc": ep["schedule_utc"],
        "gate": gate,
    }


def write_metadata_snapshot(ep: dict[str, Any], verified: dict[str, Any]) -> None:
    epdir = ROOT / "episodes" / ep["episode_id"]
    pkg = epdir / "09_package"
    snapshot = {
        "episode_id": ep["episode_id"],
        "revision": REV,
        "status": "owner_requested_upload_schedule_ready",
        "title": ep["title"],
        "description": verified["description"],
        "tags": ep.get("tags", []),
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
        "made_for_kids": False,
        "contains_synthetic_media": True,
        "video_actual_path": str(verified["video"]).replace("\\", "/"),
        "video_sha256": verified["video_sha256"],
        "captions_sidecar": rel(verified["captions"]),
        "captions_sha256": verified["captions_sha256"],
        "thumbnail": rel(verified["thumbnail"]),
        "thumbnail_sha256": verified["thumbnail_sha256"],
        "intended_schedule_local": ep["schedule_local"],
        "intended_schedule_utc": ep["schedule_utc"],
        "risk_note": ep.get("risk_note"),
        "owner_current_thread_request": True,
        "upload_performed": False,
        "schedule_performed": False,
        "public_immediate_publish": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(pkg / f"youtube_meta.owner_batch.{REV}.json", snapshot)


def update_records(ep: dict[str, Any], verified: dict[str, Any], result: dict[str, Any], caption_result: dict[str, Any] | None, caption_error: str | None, state: dict[str, Any]) -> None:
    now = datetime.now(timezone.utc).isoformat()
    epdir = ROOT / "episodes" / ep["episode_id"]
    pkg = epdir / "09_package"
    video_id = result["video_id"]
    write_json(pkg / THUMB_RESULT_NAME, result["thumbnail_state"])
    write_json(
        pkg / CAPTION_RESULT_NAME,
        caption_result
        if caption_result is not None
        else {
            "episode_id": ep["episode_id"],
            "video_id": video_id,
            "uploaded": False,
            "error": caption_error,
            "caption_file": rel(verified["captions"]),
            "captions_burned_in": True,
        },
    )
    write_json(pkg / STATUS_NAME, state)
    write_json(pkg / RESULT_NAME, result)
    manifest_path = epdir / "manifest.json"
    if manifest_path.exists():
        manifest = load_json(manifest_path)
        manifest["state"] = "scheduled"
        manifest["video_id"] = video_id
        manifest["video_url"] = result["watch"]
        manifest["public_schedule_active"] = True
        manifest["updated_at"] = now
        manifest.setdefault("active_revisions", {})["youtube_schedule_result"] = REV
        write_json(manifest_path, manifest)
    append_event(
        epdir,
        {
            "ts": now,
            "episode_id": ep["episode_id"],
            "stage": "youtube_schedule",
            "event": "youtube_upload_scheduled",
            "revision": REV,
            "actor": "codex",
            "approval_source": "owner_current_thread_request",
            "video_id": video_id,
            "watch": result["watch"],
            "studio": result["studio"],
            "scheduled_at_local": ep["schedule_local"],
            "scheduled_at_utc": ep["schedule_utc"],
            "privacy": "private",
            "thumbnail_set": True,
            "captions_uploaded": caption_result is not None,
            "caption_error": caption_error,
        },
    )


def upload_one(token: str, channel_id: str, ep: dict[str, Any], verified: dict[str, Any]) -> dict[str, Any]:
    epdir = ROOT / "episodes" / ep["episode_id"]
    pkg = epdir / "09_package"
    upload_url = initiate_upload(token, ep, verified["description"], verified["video"].stat().st_size)
    print(f"OK EP{ep['num']} upload session started; uploading {verified['video'].stat().st_size / 1e6:.0f} MB", flush=True)
    video_id = upload_chunks(upload_url, token, verified["video"])
    if not video_id:
        raise RuntimeError(f"EP{ep['num']} upload returned no video_id")
    in_progress = {
        "episode_id": ep["episode_id"],
        "revision": REV,
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "status": "uploaded_before_thumbnail_caption_verify",
        "scheduled_at_local": ep["schedule_local"],
        "scheduled_at_utc": ep["schedule_utc"],
        "external_upload": True,
    }
    write_json(pkg / IN_PROGRESS_NAME, in_progress)
    thumb_state = set_thumbnail(token, video_id, verified["thumbnail"])
    print(f"OK EP{ep['num']} thumbnail set", flush=True)
    caption_result = None
    caption_error = None
    try:
        caption_result = upload_caption(token, video_id, verified["captions"], ep["episode_id"].split("-")[-1])
        print(f"OK EP{ep['num']} sidecar captions uploaded", flush=True)
    except Exception as exc:
        caption_error = str(exc)
        print(f"WARN EP{ep['num']} sidecar captions upload failed; burned-in captions remain: {caption_error}", flush=True)
    state = get_video_state(token, video_id)
    items = state.get("items") or []
    status = (items[0].get("status") if items else {}) or {}
    privacy = status.get("privacyStatus")
    publish_at = status.get("publishAt")
    if privacy != "private" or publish_at != ep["schedule_utc"]:
        raise RuntimeError(f"EP{ep['num']} schedule verification failed: privacy={privacy!r}, publishAt={publish_at!r}")
    result = {
        "schema_version": "1.0.0",
        "episode_id": ep["episode_id"],
        "revision": REV,
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "channel_id": channel_id,
        "privacy": privacy,
        "scheduled_at_local": ep["schedule_local"],
        "scheduled_at_utc": ep["schedule_utc"],
        "publish_at_platform": publish_at,
        "video_file": str(verified["video"]).replace("\\", "/"),
        "video_sha256": verified["video_sha256"],
        "thumbnail_file": rel(verified["thumbnail"]),
        "thumbnail_sha256": verified["thumbnail_sha256"],
        "thumbnail_set": True,
        "thumbnail_state": thumb_state,
        "caption_file": rel(verified["captions"]),
        "captions_sha256": verified["captions_sha256"],
        "captions_uploaded": caption_result is not None,
        "caption_error": caption_error,
        "metadata_snapshot": rel(pkg / f"youtube_meta.owner_batch.{REV}.json"),
        "final_acceptance_status": verified["gate"].get("status"),
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "madeForKids": False,
        "containsSyntheticMedia": True,
        "external_upload": True,
        "public_schedule_set": True,
        "public_immediate_publish": False,
        "youtube_state_after": state,
    }
    update_records(ep, verified, result, caption_result, caption_error, state)
    try:
        (pkg / IN_PROGRESS_NAME).unlink()
    except FileNotFoundError:
        pass
    return result


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", nargs="*", type=int, choices=[21, 22, 23, 24])
    args = parser.parse_args(argv)

    selected = [ep for ep in EPISODES if not args.only or ep["num"] in args.only]
    verified_items: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for ep in selected:
        verified = verify_preconditions(ep)
        write_metadata_snapshot(ep, verified)
        verified_items.append((ep, verified))
        print(
            f"OK EP{ep['num']} preflight: {ep['title']} | {ep['schedule_local']} | "
            f"{verified['video_sha256']}",
            flush=True,
        )
    if args.dry_run:
        print("DRY_RUN_OK no external YouTube writes performed", flush=True)
        return 0

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    print(f"OK channel allowlisted: {channel_id}", flush=True)
    results = []
    for ep, verified in verified_items:
        result = upload_one(token, channel_id, ep, verified)
        results.append(result)
        print(f"RESULT EP{ep['num']} {result['watch']} scheduled {ep['schedule_local']}", flush=True)
    print(json.dumps({"status": "scheduled", "results": results}, indent=2, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
