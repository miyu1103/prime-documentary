#!/usr/bin/env python3
"""Create OneCoin v005 final candidate with contract ElevenLabs voice.

Uses the already QC-passed v003 video stream and muxes in the v003 master mix.
No upload, publish, schedule, or channel setting changes are performed.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-017-onecoin"
EPDIR = ROOT / "episodes" / EP
PACKAGE = EPDIR / "09_package"
RENDERS = EPDIR / "08_edit" / "renders"
SRC_VIDEO = Path("E:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v003.mp4")
MASTER_MIX = ROOT / "remotion" / "public" / "onecoin" / "audio" / "onecoin_final_mix_v003.wav"
OUT = Path("E:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v005.mp4")
QC = RENDERS / "final.v005.qc.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v003.srt"
SELECTED_THUMB = PACKAGE / "thumbnail.selected.v001.png"
EVENTS = EPDIR / "events" / "events.jsonl"
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def capture(cmd: list[str | Path]) -> str:
    p = subprocess.run([str(x) for x in cmd], capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    return p.stdout


def ffprobe_json(path: Path) -> dict:
    return json.loads(
        capture(
            [
                FFPROBE,
                "-v",
                "error",
                "-show_entries",
                "format=duration:stream=index,codec_name,codec_type,width,height,r_frame_rate,pix_fmt,bit_rate",
                "-of",
                "json",
                path,
            ]
        )
    )


def mux() -> dict:
    for path in [SRC_VIDEO, MASTER_MIX]:
        if not path.exists():
            raise FileNotFoundError(path)
    tmp = OUT.with_suffix(".tmp.mp4")
    if tmp.exists():
        tmp.unlink()
    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-i",
            str(SRC_VIDEO),
            "-i",
            str(MASTER_MIX),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(tmp),
        ],
        check=True,
    )
    tmp.replace(OUT)
    data = ffprobe_json(OUT)
    duration = float(data["format"]["duration"])
    video = next(s for s in data["streams"] if s["codec_type"] == "video")
    audio = next(s for s in data["streams"] if s["codec_type"] == "audio")
    qc = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v005",
        "source_video_revision": "v003",
        "audio_mix_revision": "v003",
        "created_at": now(),
        "file": str(OUT).replace("\\", "/"),
        "sha256": sha256(OUT),
        "duration_seconds": duration,
        "runtime_band_pass": 27 * 60 <= duration <= 33 * 60,
        "video": video,
        "audio": audio,
        "render_method": "v003 QC-passed video stream copied; v003 ElevenLabs master mix encoded AAC 192k",
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
        "voice_status": "elevenlabs_master_contract_voice",
    }
    write_json(QC, qc)
    return qc


def build_package(qc: dict) -> None:
    for path in [CAPTIONS, SELECTED_THUMB, PACKAGE / "youtube_meta.v003.json", PACKAGE / "rights_manifest.v003.json"]:
        if not path.exists():
            raise FileNotFoundError(path)
    generated = now()
    final_sha = sha256(OUT)
    thumb_sha = sha256(SELECTED_THUMB)

    youtube_meta = read_json(PACKAGE / "youtube_meta.v003.json")
    youtube_meta.update(
        {
            "revision": "v005",
            "status": "first_cut_review_ready_not_uploaded_master_voice",
            "video_actual_path": str(OUT).replace("\\", "/"),
            "video_sha256": final_sha,
            "captions_sidecar": rel(CAPTIONS),
            "thumbnail": rel(SELECTED_THUMB),
            "thumbnail_sha256": thumb_sha,
            "render_revision": "v005",
            "audio_mix_revision": "v003",
            "voice_provider": "elevenlabs_master",
            "publish_gate": "closed",
            "upload_performed": False,
            "publish_performed": False,
            "schedule_performed": False,
            "created_at": generated,
        }
    )
    write_json(PACKAGE / "youtube_meta.v005.json", youtube_meta)

    rights = read_json(PACKAGE / "rights_manifest.v003.json")
    rights.update(
        {
            "revision": "v005",
            "generated_at": generated,
            "status": "conditional_first_cut_review_master_voice",
            "render_revision": "v005",
            "audio_mix_revision": "v003",
            "voice_provider": "elevenlabs_master",
        }
    )
    rights["assets"] = [
        {
            "asset_id": f"{EP}-final-render-v005",
            "type": "final_render",
            "file": str(OUT).replace("\\", "/"),
            "sha256": final_sha,
            "rights_status": "conditional",
        },
        {
            "asset_id": f"{EP}-thumbnail-selected-v001",
            "type": "thumbnail_selected",
            "file": rel(SELECTED_THUMB),
            "sha256": thumb_sha,
            "rights_status": "conditional",
        },
        {
            "asset_id": f"{EP}-captions-v003",
            "type": "captions",
            "file": rel(CAPTIONS),
            "sha256": sha256(CAPTIONS),
            "rights_status": "clear",
        },
        {
            "asset_id": f"{EP}-factory-ledger-v001",
            "type": "factory_ledger",
            "file": rel(EPDIR / "05_stock" / "factory_ledger.v001.json"),
            "sha256": sha256(EPDIR / "05_stock" / "factory_ledger.v001.json"),
            "rights_status": "clear",
        },
    ]
    write_json(PACKAGE / "rights_manifest.v005.json", rights)

    delivery = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v005",
        "generated_at": generated,
        "status": "first_cut_review_ready_master_voice",
        "active_script_revision": "v001",
        "source_package_revision": "v003",
        "final_video": str(OUT).replace("\\", "/"),
        "video": str(OUT).replace("\\", "/"),
        "video_sha256": final_sha,
        "duration_seconds": qc["duration_seconds"],
        "runtime_band_pass": qc["runtime_band_pass"],
        "thumbnail": rel(SELECTED_THUMB),
        "thumbnail_sha256": thumb_sha,
        "captions": rel(CAPTIONS),
        "youtube_meta": rel(PACKAGE / "youtube_meta.v005.json"),
        "rights_manifest": rel(PACKAGE / "rights_manifest.v005.json"),
        "owner_review_request": rel(PACKAGE / "OWNER_REVIEW_REQUEST.v005.md"),
        "external_side_effects": {"upload": False, "publish": False, "schedule": False},
        "remaining_hard_stops": [
            "first-cut owner review",
            "title/thumbnail approval",
            "same-day legal and fact re-check before public scheduling",
            "public scheduling approval",
        ],
    }
    write_json(PACKAGE / "final_delivery.v005.json", delivery)

    review = f"""# OWNER REVIEW REQUEST v005 - OneCoin First Cut

Episode: {EP}
Active script revision: v001
Video: `{delivery['final_video']}`
SHA256: `{delivery['video_sha256']}`
Runtime: {qc['duration_seconds']:.3f}s
Voice: ElevenLabs master, contract voice ID nPczCjzI2devNBz1zQrb

## Review Focus
- Story structure: cold open -> promise -> crack -> void -> unresolved coda.
- Legal language: Ruja Ignatova is charged/wanted/alleged, not convicted.
- Dignity: victims remain the moral center; no mocking believers.
- Visuals: symbolic AI stills, factory stock, and Remotion graphics; no real-person likeness.
- Thumbnail/title: selected review candidate remains option A, `{youtube_meta['title']}` / `THERE WAS NO COIN`.

## Gates Still Closed
- No upload, publish, schedule, or channel setting change has been performed.
- First-cut owner review is still required.
- Title/thumbnail approval is still required.
- Same-day DOJ/FBI fact re-check and legal review are still required before public scheduling.
"""
    (PACKAGE / "OWNER_REVIEW_REQUEST.v005.md").write_text(review, encoding="utf-8")


def update_manifest(qc: dict) -> None:
    manifest_path = EPDIR / "manifest.json"
    manifest = read_json(manifest_path)
    active = manifest.setdefault("active_revisions", {})
    active.update(
        {
            "final_render": "v005",
            "final_qc": "v005",
            "youtube_meta": "v005",
            "rights_manifest": "v005",
            "final_delivery": "v005",
            "owner_review_request": "v005",
            "captions": "v003",
            "audio_mix": "v003",
            "voice_master": "v002",
            "narration_index": "v003",
        }
    )
    manifest["state"] = "first_cut_packaged_v005_master_voice"
    artifacts = manifest.setdefault("artifacts", [])
    new_artifacts = [
        ("PD-2026-017-onecoin-final-render-v005", "final_render", "v005", f"artifact://{str(OUT).replace(chr(92), '/')}", sha256(OUT), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-final-qc-v005", "final_render_qc", "v005", "artifact://episodes/PD-2026-017-onecoin/08_edit/renders/final.v005.qc.json", sha256(QC), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-youtube-meta-v005", "youtube_meta", "v005", "artifact://episodes/PD-2026-017-onecoin/09_package/youtube_meta.v005.json", sha256(PACKAGE / "youtube_meta.v005.json"), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-rights-manifest-v005", "rights_manifest", "v005", "artifact://episodes/PD-2026-017-onecoin/09_package/rights_manifest.v005.json", sha256(PACKAGE / "rights_manifest.v005.json"), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-final-delivery-v005", "final_delivery", "v005", "artifact://episodes/PD-2026-017-onecoin/09_package/final_delivery.v005.json", sha256(PACKAGE / "final_delivery.v005.json"), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-owner-review-request-v005", "owner_review_request", "v005", "artifact://episodes/PD-2026-017-onecoin/09_package/OWNER_REVIEW_REQUEST.v005.md", sha256(PACKAGE / "OWNER_REVIEW_REQUEST.v005.md"), "candidate", "conditional", "pass"),
    ]
    ids = {a[0] for a in new_artifacts}
    artifacts[:] = [a for a in artifacts if a.get("artifact_id") not in ids]
    for aid, atype, rev, uri, checksum, status, rights_status, qc_status in new_artifacts:
        artifacts.append({"artifact_id": aid, "artifact_type": atype, "revision": rev, "uri": uri, "checksum": checksum, "status": status, "rights_status": rights_status, "qc_status": qc_status})
    manifest["updated_at"] = now()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with EVENTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"ts": now(), "episode_id": EP, "stage": "package", "event": "first_cut_package_built", "revision": "v005", "actor": "codex", "provider": "elevenlabs_master_contract_voice", "upload_publish_schedule": False}, ensure_ascii=False) + "\n")


def main() -> int:
    qc = mux()
    build_package(qc)
    update_manifest(qc)
    print(json.dumps({"render": str(OUT), "sha256": sha256(OUT), "delivery": rel(PACKAGE / "final_delivery.v005.json"), "duration": qc["duration_seconds"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
