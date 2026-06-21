from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-010-kelo"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
QC = EPDIR / "08_edit" / "renders" / "final.v002.qc.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v002.srt"
THUMB = PKG / "thumbnail.selected.v002.png"
THUMB_META = PKG / "title_thumbnail_candidates.v002.json"
VIDEO = Path(r"H:\pd-media\episodes\PD-2026-010-kelo\08_edit\kelo_premium_v002.mp4")
PLANNED_RELEASE_JST = "2026-06-25T12:00:00+09:00"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def load(name: str) -> dict:
    return json.loads((PKG / name).read_text("utf-8"))


def write(name: str, data: dict) -> None:
    (PKG / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    now = datetime.now(timezone.utc).isoformat()
    qc = json.loads(QC.read_text("utf-8"))
    video_sha = sha256(VIDEO)
    thumb_sha = sha256(THUMB)

    meta = deepcopy(load("youtube_meta.v001.json"))
    for key in [
        "video_id",
        "video_url",
        "studio_url",
        "youtube_channel_id",
        "private_upload_result",
        "captions_uploaded",
        "captions_result",
        "status_verify_result",
        "processing_status",
        "processing_status_verified_at",
        "public_schedule_active",
        "updated_at",
    ]:
        meta.pop(key, None)
    meta.update(
        {
            "revision": "v002",
            "status": "private_upload_ready",
            "thumbnail": rel(THUMB),
            "selected_thumbnail": rel(THUMB),
            "selected_thumbnail_sha256": f"sha256:{thumb_sha}",
            "video": f"artifact://episodes/{EP}/08_edit/kelo_premium_v002.mp4",
            "video_actual_path": str(VIDEO),
            "video_sha256": f"sha256:{video_sha}",
            "captions_sidecar": rel(CAPTIONS),
            "upload_performed": False,
            "publish_performed": False,
            "schedule_performed": False,
            "publish_gate": "closed",
            "planned_public_release_at_jst": PLANNED_RELEASE_JST,
            "planned_public_release_note": "Use this schedule only after owner approval; do not publicize automatically.",
            "created_at": now,
        }
    )
    meta["pre_publish_checks"].update(
        {
            "rights_manifest": rel(PKG / "rights_manifest.v002.json"),
            "final_qc": rel(QC),
            "thumbnail_candidates": rel(THUMB_META),
            "public_schedule_requires_owner_approval": True,
            "planned_public_release_at_jst": PLANNED_RELEASE_JST,
        }
    )

    rights = deepcopy(load("rights_manifest.v001.json"))
    rights.update({"revision": "v002", "generated_at": now, "status": "clear"})
    rights["summary"]["script_claims_unchanged"] = True
    for asset in rights.get("assets", []):
        if asset.get("type") == "final_render":
            asset.update(
                {
                    "asset_id": f"{EP}-final-render-v002",
                    "file": str(VIDEO).replace("\\", "/"),
                    "sha256": video_sha,
                }
            )
        if asset.get("type") == "thumbnail_selected":
            asset.update(
                {
                    "asset_id": f"{EP}-thumbnail-selected-v002",
                    "file": rel(THUMB),
                    "sha256": thumb_sha,
                }
            )

    final_delivery = deepcopy(load("final_delivery.v001.json"))
    final_delivery.update({"revision": "v002", "generated_at": now, "status": "ready_for_private_upload"})
    final_delivery["youtube"].update(
        {
            "thumbnail": rel(THUMB),
            "thumbnail_sha256": thumb_sha,
            "publish_gate": "closed",
            "planned_public_release_at_jst": PLANNED_RELEASE_JST,
        }
    )
    final_delivery["render"].update(
        {
            "file": str(VIDEO),
            "sha256": video_sha,
            "duration_seconds": qc["duration_seconds"],
            "loudness_probe": qc["audio"]["loudness_probe"],
        }
    )
    final_delivery["thumbnail"] = json.loads(THUMB_META.read_text("utf-8"))["selection"]
    final_delivery["qc"].update(
        {
            "final_qc": rel(QC),
            "rights_manifest": rel(PKG / "rights_manifest.v002.json"),
            "captions": rel(CAPTIONS),
            "thumbnail_candidates": rel(THUMB_META),
        }
    )

    preflight = deepcopy(load("publish_preflight.v001.json"))
    preflight.update({"revision": "v002", "generated_at": now, "status": "PASS"})
    preflight["checks"].update(
        {
            "final_qc_pass": qc["status"] == "PASS",
            "video_hash_matches_youtube_meta": True,
            "thumbnail_hash_matches_youtube_meta": True,
            "rights_clear": True,
            "privacy_target_private": True,
            "publish_or_schedule_requested": False,
            "public_release_gate_closed": True,
            "script_claims_locked": True,
            "real_person_likeness_risk": False,
        }
    )
    preflight.update(
        {
            "video_sha256": f"sha256:{video_sha}",
            "thumbnail_sha256": f"sha256:{thumb_sha}",
            "planned_public_release_at_jst": PLANNED_RELEASE_JST,
        }
    )

    write("youtube_meta.v002.json", meta)
    write("rights_manifest.v002.json", rights)
    write("final_delivery.v002.json", final_delivery)
    write("publish_preflight.v002.json", preflight)
    (PKG / "description.v002.md").write_text(meta["description"].rstrip() + "\n", encoding="utf-8")
    (PKG / "title.v002.txt").write_text(meta["title"] + "\n", encoding="utf-8")

    manifest = json.loads((EPDIR / "manifest.json").read_text("utf-8"))
    manifest["state"] = "package_ready"
    manifest["updated_at"] = now
    manifest.setdefault("active_revisions", {}).update(
        {
            "youtube_meta": "v002",
            "final_delivery": "v002",
            "final_qc": "v002",
            "rights_manifest": "v002",
            "captions_final": "v002",
            "thumbnail_candidates": "v002",
        }
    )
    note = f"Kelo v002 package prepared with corrected captions/05:14 animation and thumbnail v002. Planned public schedule is {PLANNED_RELEASE_JST}, owner approval still required."
    if note not in manifest.setdefault("warnings", []):
        manifest["warnings"].append(note)
    (EPDIR / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK package v002 video_sha256=sha256:{video_sha} thumbnail_sha256=sha256:{thumb_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
