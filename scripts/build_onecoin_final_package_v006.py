#!/usr/bin/env python3
"""Package OneCoin v006 editorial review cut.

No upload, publish, schedule, channel change, paid API call, or external send.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-017-onecoin"
EPDIR = ROOT / "episodes" / EP
PACKAGE = EPDIR / "09_package"
RENDERS = EPDIR / "08_edit" / "renders"
OUT = Path("H:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v006.mp4")
QC = RENDERS / "final.v006.qc.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v004.editorial_v006.srt"
SELECTED_THUMB = PACKAGE / "thumbnail.selected.v001.png"
EVENTS = EPDIR / "events" / "events.jsonl"


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


def build_package() -> dict:
    for path in [OUT, QC, CAPTIONS, SELECTED_THUMB, PACKAGE / "youtube_meta.v005.json", PACKAGE / "rights_manifest.v005.json"]:
        if not path.exists():
            raise FileNotFoundError(path)
    generated = now()
    qc = read_json(QC)
    final_sha = sha256(OUT)
    thumb_sha = sha256(SELECTED_THUMB)

    youtube_meta = read_json(PACKAGE / "youtube_meta.v005.json")
    youtube_meta.update(
        {
            "revision": "v006",
            "status": "editorial_review_ready_runtime_override_not_uploaded",
            "video_actual_path": str(OUT).replace("\\", "/"),
            "video_sha256": final_sha,
            "captions_sidecar": rel(CAPTIONS),
            "thumbnail": rel(SELECTED_THUMB),
            "thumbnail_sha256": thumb_sha,
            "render_revision": "v006",
            "audio_mix_revision": "v004_editorial_v006",
            "voice_provider": "elevenlabs_master_reused_no_new_api_call",
            "editorial_override": "20.48 minute cut approved by user direction for tempo, sound, and readability over 30-minute runtime",
            "publish_gate": "closed",
            "upload_performed": False,
            "publish_performed": False,
            "schedule_performed": False,
            "created_at": generated,
        }
    )
    write_json(PACKAGE / "youtube_meta.v006.json", youtube_meta)

    rights = read_json(PACKAGE / "rights_manifest.v005.json")
    rights.update(
        {
            "revision": "v006",
            "generated_at": generated,
            "status": "conditional_editorial_review_runtime_override",
            "render_revision": "v006",
            "audio_mix_revision": "v004_editorial_v006",
            "voice_provider": "elevenlabs_master_reused_no_new_api_call",
        }
    )
    rights["assets"] = [
        {
            "asset_id": f"{EP}-final-render-v006",
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
            "asset_id": f"{EP}-captions-v004-editorial-v006",
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
    write_json(PACKAGE / "rights_manifest.v006.json", rights)

    delivery = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v006",
        "generated_at": generated,
        "status": "editorial_review_ready_runtime_override",
        "active_script_revision": "v001",
        "source_package_revision": "v005",
        "final_video": str(OUT).replace("\\", "/"),
        "video": str(OUT).replace("\\", "/"),
        "video_sha256": final_sha,
        "duration_seconds": qc["duration_seconds"],
        "runtime_band_pass": qc["runtime_band_pass"],
        "editorial_override": "Runtime intentionally shorter than 27-33 minute gate after owner feedback: faster hook, natural narration, clearer captions, denser visuals.",
        "thumbnail": rel(SELECTED_THUMB),
        "thumbnail_sha256": thumb_sha,
        "captions": rel(CAPTIONS),
        "youtube_meta": rel(PACKAGE / "youtube_meta.v006.json"),
        "rights_manifest": rel(PACKAGE / "rights_manifest.v006.json"),
        "owner_review_request": rel(PACKAGE / "OWNER_REVIEW_REQUEST.v006.md"),
        "external_side_effects": {"upload": False, "publish": False, "schedule": False, "paid_api": False},
        "remaining_hard_stops": [
            "editorial owner review",
            "title/thumbnail approval",
            "same-day legal and fact re-check before public scheduling",
            "public scheduling approval",
        ],
    }
    write_json(PACKAGE / "final_delivery.v006.json", delivery)

    review = f"""# OWNER REVIEW REQUEST v006 - OneCoin Editorial Cut

Episode: {EP}
Active script revision: v001
Video: `{delivery['final_video']}`
SHA256: `{delivery['video_sha256']}`
Runtime: {qc['duration_seconds']:.3f}s / {qc['duration_seconds'] / 60:.2f}min
Voice: ElevenLabs master reused from v002, contract voice ID nPczCjzI2devNBz1zQrb

## What Changed From v005
- Opening now arrives after the 8.2s hook instead of nearly two minutes in.
- Narration uses natural-speed ElevenLabs chunks; no 30-minute atempo stretching.
- Runtime is intentionally shorter for tempo and watchability.
- Captions are lighter on-screen and generated against the editorial timing.
- Promise chapter avoids overly dark hero rotation that triggered false black/dropout feel.

## Review Focus
- Tempo and first 60 seconds.
- Narration pace and listening comfort.
- Subtitle readability and perceived sync.
- Any remaining visual dropout or overly dark patches.
- Legal language: Ruja Ignatova is charged/wanted/alleged, not convicted.

## Gates Still Closed
- No upload, publish, schedule, channel setting change, or paid API call was performed.
- Editorial owner review is still required.
- Title/thumbnail approval is still required.
- Same-day DOJ/FBI fact re-check and legal review are still required before public scheduling.
"""
    (PACKAGE / "OWNER_REVIEW_REQUEST.v006.md").write_text(review, encoding="utf-8")
    return delivery


def update_manifest(delivery: dict) -> None:
    manifest_path = EPDIR / "manifest.json"
    manifest = read_json(manifest_path)
    active = manifest.setdefault("active_revisions", {})
    active.update(
        {
            "roughcut": "v006",
            "onecoin_roughcut": "v006",
            "final_render": "v006",
            "final_qc": "v006",
            "youtube_meta": "v006",
            "rights_manifest": "v006",
            "final_delivery": "v006",
            "owner_review_request": "v006",
            "captions": "v004_editorial_v006",
            "audio_mix": "v004_editorial_v006",
            "voice_master": "v002",
            "narration_index": "v003",
        }
    )
    manifest["state"] = "editorial_v006_packaged_pending_owner_review"
    artifacts = manifest.setdefault("artifacts", [])
    new_artifacts = [
        ("PD-2026-017-onecoin-final-render-v006", "final_render", "v006", f"artifact://{str(OUT).replace(chr(92), '/')}", sha256(OUT), "candidate", "conditional", "editorial_runtime_override"),
        ("PD-2026-017-onecoin-final-qc-v006", "final_render_qc", "v006", "artifact://episodes/PD-2026-017-onecoin/08_edit/renders/final.v006.qc.json", sha256(QC), "candidate", "conditional", "runtime_override_only"),
        ("PD-2026-017-onecoin-youtube-meta-v006", "youtube_meta", "v006", "artifact://episodes/PD-2026-017-onecoin/09_package/youtube_meta.v006.json", sha256(PACKAGE / "youtube_meta.v006.json"), "candidate", "conditional", "runtime_override"),
        ("PD-2026-017-onecoin-rights-manifest-v006", "rights_manifest", "v006", "artifact://episodes/PD-2026-017-onecoin/09_package/rights_manifest.v006.json", sha256(PACKAGE / "rights_manifest.v006.json"), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-final-delivery-v006", "final_delivery", "v006", "artifact://episodes/PD-2026-017-onecoin/09_package/final_delivery.v006.json", sha256(PACKAGE / "final_delivery.v006.json"), "candidate", "conditional", "runtime_override"),
        ("PD-2026-017-onecoin-owner-review-request-v006", "owner_review_request", "v006", "artifact://episodes/PD-2026-017-onecoin/09_package/OWNER_REVIEW_REQUEST.v006.md", sha256(PACKAGE / "OWNER_REVIEW_REQUEST.v006.md"), "candidate", "conditional", "pass"),
    ]
    ids = {a[0] for a in new_artifacts}
    artifacts[:] = [a for a in artifacts if a.get("artifact_id") not in ids]
    for aid, atype, rev, uri, checksum, status, rights_status, qc_status in new_artifacts:
        artifacts.append({"artifact_id": aid, "artifact_type": atype, "revision": rev, "uri": uri, "checksum": checksum, "status": status, "rights_status": rights_status, "qc_status": qc_status})
    manifest["updated_at"] = now()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with EVENTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"ts": now(), "episode_id": EP, "stage": "package", "event": "editorial_v006_package_built", "revision": "v006", "actor": "codex", "upload_publish_schedule": False}, ensure_ascii=False) + "\n")


def main() -> int:
    delivery = build_package()
    update_manifest(delivery)
    print(json.dumps({"render": str(OUT), "sha256": sha256(OUT), "delivery": rel(PACKAGE / "final_delivery.v006.json"), "duration": delivery["duration_seconds"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
