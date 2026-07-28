#!/usr/bin/env python3
"""Build OneCoin v003 first-cut package pointers.

Reuses the v001 title/thumbnail package, but points delivery/youtube/rights
sidecars at the v003 corrected render. No upload, publish, schedule, or channel
setting changes are performed.
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
FINAL = Path("H:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v003.mp4")
QC = RENDERS / "final.v003.qc.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v001.srt"
SELECTED_THUMB = PACKAGE / "thumbnail.selected.v001.png"
EVENTS = EPDIR / "events" / "events.jsonl"


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


def read_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    for path in [FINAL, QC, CAPTIONS, SELECTED_THUMB, PACKAGE / "youtube_meta.v001.json", PACKAGE / "rights_manifest.v001.json"]:
        if not path.exists():
            raise FileNotFoundError(path)

    now = datetime.now(timezone.utc).isoformat()
    qc = read_json(QC)
    final_sha = sha256(FINAL)
    thumb_sha = sha256(SELECTED_THUMB)

    youtube_meta = read_json(PACKAGE / "youtube_meta.v001.json")
    youtube_meta.update(
        {
            "revision": "v003",
            "status": "first_cut_review_ready_not_uploaded_voice_draft",
            "video_actual_path": str(FINAL).replace("\\", "/"),
            "video_sha256": final_sha,
            "thumbnail": rel(SELECTED_THUMB),
            "thumbnail_sha256": thumb_sha,
            "captions_sidecar": rel(CAPTIONS),
            "publish_gate": "closed",
            "upload_performed": False,
            "publish_performed": False,
            "schedule_performed": False,
            "created_at": now,
            "source_package_revision": "v001",
            "render_revision": "v003",
        }
    )
    write_json(PACKAGE / "youtube_meta.v003.json", youtube_meta)

    rights = read_json(PACKAGE / "rights_manifest.v001.json")
    rights.update(
        {
            "revision": "v003",
            "generated_at": now,
            "status": "conditional_first_cut_review_voice_draft",
            "source_package_revision": "v001",
            "render_revision": "v003",
        }
    )
    rights["assets"] = [
        {
            "asset_id": f"{EP}-final-render-v003",
            "type": "final_render",
            "file": str(FINAL).replace("\\", "/"),
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
            "asset_id": f"{EP}-captions-v001",
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
    write_json(PACKAGE / "rights_manifest.v003.json", rights)

    delivery = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v003",
        "generated_at": now,
        "status": "first_cut_review_ready_voice_draft",
        "active_script_revision": "v001",
        "source_package_revision": "v001",
        "final_video": str(FINAL).replace("\\", "/"),
        "video": str(FINAL).replace("\\", "/"),
        "video_sha256": final_sha,
        "duration_seconds": qc["duration_seconds"],
        "runtime_band_pass": qc["runtime_band_pass"],
        "thumbnail": rel(SELECTED_THUMB),
        "thumbnail_sha256": thumb_sha,
        "youtube_meta": rel(PACKAGE / "youtube_meta.v003.json"),
        "rights_manifest": rel(PACKAGE / "rights_manifest.v003.json"),
        "owner_review_request": rel(PACKAGE / "OWNER_REVIEW_REQUEST.v003.md"),
        "external_side_effects": {"upload": False, "publish": False, "schedule": False},
        "hard_stop": "ElevenLabs master narration remains blocked pending explicit owner GO.",
    }
    write_json(PACKAGE / "final_delivery.v003.json", delivery)

    review = f"""# OWNER REVIEW REQUEST v003 — OneCoin First Cut

Episode: {EP}
Active script revision: v001
Video: `{delivery['final_video']}`
SHA256: `{delivery['video_sha256']}`
Runtime: {qc['duration_seconds']:.3f}s
Runtime band pass: {qc['runtime_band_pass']}

## Review Focus
- Story structure: cold open -> promise -> crack -> void -> unresolved coda.
- Legal language: Ruja Ignatova is charged/wanted/alleged, not convicted.
- Dignity: victims remain the moral center; no mocking believers.
- Visuals: symbolic AI stills, factory stock, and Remotion graphics; no real-person likeness.
- Audio: this first cut uses local SAPI draft narration for timing. ElevenLabs master is still blocked pending owner GO.
- Thumbnail/title: selected review candidate remains option A, `{youtube_meta['title']}` / `THERE WAS NO COIN`.

## Gates Still Closed
- No ElevenLabs paid call has been made.
- No upload, publish, schedule, or channel setting change has been performed.
- Title/thumbnail approval is still required.
- Same-day DOJ/FBI fact re-check and legal review are still required before public scheduling.
"""
    (PACKAGE / "OWNER_REVIEW_REQUEST.v003.md").write_text(review, encoding="utf-8")

    manifest_path = EPDIR / "manifest.json"
    manifest = read_json(manifest_path)
    active = manifest.setdefault("active_revisions", {})
    active.update(
        {
            "final_render": "v003",
            "final_qc": "v003",
            "youtube_meta": "v003",
            "rights_manifest": "v003",
            "final_delivery": "v003",
            "owner_review_request": "v003",
        }
    )
    manifest["state"] = "first_cut_packaged_v003_voice_draft"
    artifacts = manifest.setdefault("artifacts", [])
    new_artifacts = [
        ("PD-2026-017-onecoin-youtube-meta-v003", "youtube_meta", "v003", "artifact://episodes/PD-2026-017-onecoin/09_package/youtube_meta.v003.json", sha256(PACKAGE / "youtube_meta.v003.json"), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-rights-manifest-v003", "rights_manifest", "v003", "artifact://episodes/PD-2026-017-onecoin/09_package/rights_manifest.v003.json", sha256(PACKAGE / "rights_manifest.v003.json"), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-final-delivery-v003", "final_delivery", "v003", "artifact://episodes/PD-2026-017-onecoin/09_package/final_delivery.v003.json", sha256(PACKAGE / "final_delivery.v003.json"), "candidate", "conditional", "draft_voice"),
        ("PD-2026-017-onecoin-owner-review-request-v003", "owner_review_request", "v003", "artifact://episodes/PD-2026-017-onecoin/09_package/OWNER_REVIEW_REQUEST.v003.md", sha256(PACKAGE / "OWNER_REVIEW_REQUEST.v003.md"), "candidate", "conditional", "pass"),
    ]
    ids = {a[0] for a in new_artifacts}
    artifacts[:] = [a for a in artifacts if a.get("artifact_id") not in ids]
    for aid, atype, rev, uri, checksum, status, rights_status, qc_status in new_artifacts:
        artifacts.append({"artifact_id": aid, "artifact_type": atype, "revision": rev, "uri": uri, "checksum": checksum, "status": status, "rights_status": rights_status, "qc_status": qc_status})
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    with EVENTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(
            json.dumps(
                {
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "episode_id": EP,
                    "stage": "package",
                    "event": "first_cut_package_built",
                    "revision": "v003",
                    "actor": "codex",
                    "note": "Built OneCoin v003 first-cut package sidecars. No upload/publish/schedule. Voice is local SAPI draft pending ElevenLabs owner GO.",
                },
                ensure_ascii=False,
            )
            + "\n"
        )

    print(json.dumps({"delivery": rel(PACKAGE / "final_delivery.v003.json"), "video": delivery["final_video"], "sha256": final_sha}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
