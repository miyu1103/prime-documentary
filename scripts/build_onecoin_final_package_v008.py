#!/usr/bin/env python3
"""Build OneCoin v008 package with owner-review-ready schedule target (no actual upload/schedule)."""
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
OUT = Path("E:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v008.mp4")
QC = RENDERS / "final.v008.qc.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v005.editorial_v008.srt"
SELECTED_THUMB = PACKAGE / "thumbnail.selected.v008.png"
THUMB_CANDIDATES = PACKAGE / "title_thumbnail_candidates.v008.json"
YOUTUBE_META_SRC = PACKAGE / "youtube_meta.v008.json"
RIGHTS_SRC = PACKAGE / "rights_manifest.v008.json"
OWNER_REVIEW = PACKAGE / "OWNER_REVIEW_REQUEST.v008.md"
EVENTS = EPDIR / "events" / "events.jsonl"
SCHEDULE_JST = "2026-07-02T12:00:00+09:00"
SCHEDULE_UTC = "2026-07-02T03:00:00Z"
TITLE = "There Was No Coin: $4 Billion in Empty Promises"
CHAPTERS = [
    {"time": "00:00", "seconds": 0.0, "title": "Hook: there was no coin"},
    {"time": "00:08", "seconds": 8.0, "title": "The promise"},
    {"time": "07:04", "seconds": 424.44, "title": "The crack"},
    {"time": "14:29", "seconds": 869.89, "title": "The void"},
    {"time": "18:52", "seconds": 1132.95, "title": "Coda: still missing"},
]
CHAPTER_DESCRIPTION = """Chapters:
00:00 Hook: there was no coin
00:08 The promise
07:04 The crack
14:29 The void
18:52 Coda: still missing"""
SCHEDULE_NOTE = "Planned private release schedule (owner-approved): 2026-07-02 12:00 JST (03:00 UTC). No upload/schedule has been performed in this revision."


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


def normalize_description(text: str) -> str:
    before, _, after = text.partition("Chapters:")
    tail = "Review gates remain closed: editorial review, title/thumbnail approval, same-day legal/fact re-check, and public scheduling approval are still required before any upload or publication."
    return before.rstrip() + "\n\n" + CHAPTER_DESCRIPTION + "\n\n" + tail + "\n\n" + SCHEDULE_NOTE


def build_package() -> dict:
    for path in [OUT, QC, CAPTIONS, SELECTED_THUMB, THUMB_CANDIDATES, YOUTUBE_META_SRC, RIGHTS_SRC]:
        if not path.exists():
            raise FileNotFoundError(path)

    generated = now()
    qc = read_json(QC)
    final_sha = sha256(OUT)
    thumb_sha = sha256(SELECTED_THUMB)
    thumb_candidates = read_json(THUMB_CANDIDATES)
    thumb_selected_option = ""
    if isinstance(thumb_candidates, dict):
        thumb_selected_option = thumb_candidates.get("selected_option") or thumb_candidates.get("selected") or ""
    if not thumb_selected_option:
        thumb_selected_option = "A"

    youtube_meta = read_json(YOUTUBE_META_SRC)
    youtube_meta.update(
        {
            "revision": "v008",
            "status": "editorial_review_ready_runtime_override_with_schedule_ready",
            "title": TITLE,
            "description": normalize_description(youtube_meta["description"]),
            "chapters": CHAPTERS,
            "thumbnail": rel(SELECTED_THUMB),
            "thumbnail_sha256": thumb_sha,
            "video_actual_path": str(OUT).replace("\\", "/"),
            "video_sha256": final_sha,
            "captions_sidecar": rel(CAPTIONS),
            "publish_schedule_target_jst": SCHEDULE_JST,
            "publish_schedule_target_utc": SCHEDULE_UTC,
            "requested_schedule": {
                "jst": SCHEDULE_JST,
                "utc": SCHEDULE_UTC,
                "status": "requested_pending_owner_confirmation",
                "reason": "user_approved_schedule_request",
            },
            "pre_publish_checks": {
                "rights_manifest": rel(PACKAGE / "rights_manifest.v008.json"),
                "final_qc": rel(QC),
                "thumbnail_candidates": rel(THUMB_CANDIDATES),
                "synthetic_content_disclosure_required": True,
                "upload_approval_required": True,
                "public_schedule_requires_owner_approval": True,
            },
            "target_schedule_after_owner_approval": {"jst": SCHEDULE_JST, "utc": SCHEDULE_UTC},
            "privacy_status_target": "private_after_owner_upload_go",
            "upload_performed": False,
            "publish_performed": False,
            "schedule_performed": False,
            "publish_gate": "closed_until_owner_review",
            "editorial_override": youtube_meta.get("editorial_override", "") + " / schedule target attached for owner execution.",
            "created_at": generated,
        }
    )

    write_json(PACKAGE / "youtube_meta.v008.json", youtube_meta)

    rights = read_json(RIGHTS_SRC)
    rights.update(
        {
            "revision": "v008",
            "generated_at": generated,
            "status": "editorial_pending_owner_schedule",
            "target_release_schedule": {"jst": SCHEDULE_JST, "utc": SCHEDULE_UTC},
            "selected_thumbnail": rel(SELECTED_THUMB),
            "selected_thumbnail_sha256": thumb_sha,
            "thumbnail_candidates": rel(THUMB_CANDIDATES),
            "publish_schedule_requested": True,
        }
    )
    for asset in rights.get("assets", []):
        if asset.get("type") == "thumbnail_selected":
            asset.update(
                {
                    "file": rel(SELECTED_THUMB),
                    "sha256": thumb_sha,
                    "asset_id": f"{EP}-thumbnail-selected-v008",
                    "rights_status": "conditional",
                }
            )
            break
    write_json(PACKAGE / "rights_manifest.v008.json", rights)

    delivery = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v008",
        "generated_at": generated,
        "status": "editorial_review_ready_runtime_override_ready_for_owner_schedule_request",
        "active_script_revision": "v001",
        "source_package_revision": "v008",
        "final_video": str(OUT).replace("\\", "/"),
        "video": str(OUT).replace("\\", "/"),
        "video_sha256": final_sha,
        "duration_seconds": qc["duration_seconds"],
        "runtime_band_pass": qc["runtime_band_pass"],
        "editorial_override": "Runtime intentionally shorter than 27-33 minute gate after owner feedback.",
        "thumbnail": rel(SELECTED_THUMB),
        "thumbnail_sha256": thumb_sha,
        "thumbnail_candidates": rel(THUMB_CANDIDATES),
        "captions": rel(CAPTIONS),
        "youtube_meta": rel(PACKAGE / "youtube_meta.v008.json"),
        "rights_manifest": rel(PACKAGE / "rights_manifest.v008.json"),
        "owner_review_request": rel(OWNER_REVIEW),
        "requested_schedule": {
            "jst": SCHEDULE_JST,
            "utc": SCHEDULE_UTC,
            "status": "requested",
            "gate": "owner_review_and_legal_cleared",
            "requested_by": "owner_after_approval",
        },
        "thumbnail_selected_option": thumb_selected_option,
        "external_side_effects": {
            "upload": False,
            "publish": False,
            "schedule": False,
            "paid_api": False,
        },
        "remaining_hard_stops": [
            "editorial owner review",
            "title/thumbnail approval",
            "same-day legal and fact re-check before public scheduling",
            "public scheduling approval",
        ],
    }
    write_json(PACKAGE / "final_delivery.v008.json", delivery)

    review = f"""# OWNER REVIEW REQUEST v008 - OneCoin Editorial Cut

Episode: {EP}
Active script revision: v001
Video: `{delivery['final_video']}`
SHA256: `{delivery['video_sha256']}`
Runtime: {qc['duration_seconds']:.3f}s / {qc['duration_seconds'] / 60:.2f}min
Planned public schedule (approval required): {SCHEDULE_JST} / {SCHEDULE_UTC}
Voice: ElevenLabs master reused from v002, contract voice ID nPczCjzI2devNBz1zQrb
Thumbnail candidate selected for this draft: Option {thumb_selected_option}

## What Changed From v007
- Thumbnail set re-rendered with a brighter/faster visual set (v008) for stronger CTR.
- Meta now includes planned schedule window: 2026-07-02 12:00 JST (03:00 UTC).
- No upload/schedule/public API call was performed.

## Review Focus
- Tempo and first 60 seconds.
- Narration pace and subtitle readability.
- Thumbnail legality: no real-person likeness / no OneCoin logo / no criminal finality language on Ruja.

## Gates Still Closed
- No upload, publish, schedule, channel setting change, or paid API call was performed.
- Title/thumbnail approval is still required.
- Same-day DOJ/FBI fact re-check and legal review are still required before public scheduling.
"""
    OWNER_REVIEW.write_text(review, encoding="utf-8")

    return delivery


def update_manifest(delivery: dict) -> None:
    manifest_path = EPDIR / "manifest.json"
    manifest = read_json(manifest_path)
    active = manifest.setdefault("active_revisions", {})
    active.update(
        {
            "roughcut": "v008",
            "onecoin_roughcut": "v008",
            "final_render": "v008",
            "final_qc": "v008",
            "thumbnail_candidates": "v008",
            "thumbnail": "v008",
            "youtube_meta": "v008",
            "rights_manifest": "v008",
            "final_delivery": "v008",
            "owner_review_request": "v008",
        }
    )
    manifest["state"] = "editorial_v008_ready_for_owner_schedule_request"
    manifest["warnings"] = list(
        dict.fromkeys(
            [
                *manifest.get("warnings", []),
                "v008 adds schedule target fields to youtube_meta/final_delivery and updates title+thumbnail candidate selection.",
                "No upload, publish, or API scheduling action is performed in this revision.",
            ]
        )
    )
    artifacts = manifest.setdefault("artifacts", [])
    new_artifacts = [
        ("PD-2026-017-onecoin-youtube-meta-v008", "youtube_meta", "v008", "artifact://episodes/PD-2026-017-onecoin/09_package/youtube_meta.v008.json", sha256(PACKAGE / "youtube_meta.v008.json"), "candidate", "conditional", "runtime_override"),
        ("PD-2026-017-onecoin-rights-manifest-v008", "rights_manifest", "v008", "artifact://episodes/PD-2026-017-onecoin/09_package/rights_manifest.v008.json", sha256(PACKAGE / "rights_manifest.v008.json"), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-final-delivery-v008", "final_delivery", "v008", "artifact://episodes/PD-2026-017-onecoin/09_package/final_delivery.v008.json", sha256(PACKAGE / "final_delivery.v008.json"), "candidate", "conditional", "runtime_override"),
        ("PD-2026-017-onecoin-owner-review-request-v008", "owner_review_request", "v008", "artifact://episodes/PD-2026-017-onecoin/09_package/OWNER_REVIEW_REQUEST.v008.md", sha256(OWNER_REVIEW), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-thumbnail-selected-v008", "thumbnail_selected", "v008", "artifact://episodes/PD-2026-017-onecoin/09_package/thumbnail.selected.v008.png", sha256(SELECTED_THUMB), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-title-thumbnail-candidates-v008", "title_thumbnail_candidates", "v008", "artifact://episodes/PD-2026-017-onecoin/09_package/title_thumbnail_candidates.v008.json", sha256(THUMB_CANDIDATES), "candidate", "conditional", "pass"),
    ]
    ids = {a[0] for a in new_artifacts}
    artifacts[:] = [a for a in artifacts if a.get("artifact_id") not in ids]
    for aid, atype, rev, uri, checksum, status, rights_status, qc_status in new_artifacts:
        artifacts.append(
            {
                "artifact_id": aid,
                "artifact_type": atype,
                "revision": rev,
                "uri": uri,
                "checksum": checksum,
                "status": status,
                "rights_status": rights_status,
                "qc_status": qc_status,
            }
        )
    manifest["updated_at"] = now()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with EVENTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(
            json.dumps(
                {
                    "ts": now(),
                    "episode_id": EP,
                    "stage": "package",
                    "event": "editorial_v008_package_built",
                    "revision": "v008",
                    "actor": "codex",
                    "upload_publish_schedule": False,
                    "requested_schedule": {"jst": SCHEDULE_JST, "utc": SCHEDULE_UTC},
                },
                ensure_ascii=False,
            )
            + "\n"
        )


def main() -> int:
    delivery = build_package()
    update_manifest(delivery)
    print(json.dumps({"render": str(OUT), "sha256": sha256(OUT), "delivery": rel(PACKAGE / "final_delivery.v008.json"), "duration": delivery["duration_seconds"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
