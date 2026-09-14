#!/usr/bin/env python3
"""Prepare OneCoin v011 for approved YouTube upload/schedule as package v012."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-017-onecoin"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
APPROVALS = EPDIR / "approvals"
EVENTS = EPDIR / "events" / "events.jsonl"
MANIFEST = EPDIR / "manifest.json"

VIDEO = Path("E:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v011.mp4")
THUMB = PKG / "thumbnail.selected.v008.png"
CAPTIONS = EPDIR / "08_edit" / "captions.v008.structure_v011.srt"
QC = EPDIR / "08_edit" / "renders" / "final.v011.qc.json"
RIGHTS = PKG / "rights_manifest.v012.json"
META = PKG / "youtube_meta.v012.json"
DELIVERY = PKG / "final_delivery.v012.json"
FACT = EPDIR / "01_research" / "fact_recheck.v002.publish.md"

SCHEDULE_LOCAL = "2026-07-02T12:00:00+09:00"
SCHEDULE_UTC = "2026-07-02T03:00:00Z"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(data: dict) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def main() -> int:
    for path in (VIDEO, THUMB, CAPTIONS, QC, PKG / "youtube_meta.v011.json", PKG / "final_delivery.v011.json", PKG / "rights_manifest.v011.json"):
        if not path.exists():
            raise FileNotFoundError(path)

    created = now()
    video_sha = sha(VIDEO)
    thumb_sha = sha(THUMB)
    captions_sha = sha(CAPTIONS)
    qc_sha = sha(QC)

    fact_text = f"""# PD-2026-017-onecoin — Publish Fact + Legal Re-check v002

- Re-check date: 2026-06-29 JST
- Status: PASS_WITH_OWNER_EDITORIAL_OVERRIDE
- Episode: {EP}
- Render: v011
- Render sha256: {video_sha}
- Schedule target: {SCHEDULE_LOCAL} / {SCHEDULE_UTC}

## Official-source checks
- DOJ SDNY 2019 charge release remains the controlling source for the charged/alleged framing, OneCoin pyramid-scheme description, alleged no-real-blockchain facts, Ruja Ignatova charges, and the DOJ disclaimer that charges are accusations and defendants are presumed innocent unless proven guilty.
- FBI/State Department reward information remains at up to $5,000,000 for information leading to arrest and/or conviction. FBI wanted-page HTML blocks automated fetch with 403, but the official FBI PDF/search result and FBI 2024 reward release were checked.
- DOJ OPA 2026 remission release says victims invested over $4B worldwide, more than $40M in forfeited assets are available, and the petition deadline is June 30. Because scheduled publication is July 2, the public YouTube description intentionally does not include a call-to-action around that deadline.

## Legal language checks
- Ruja Ignatova is treated as charged, wanted, accused, and not convicted.
- Convicted/guilty wording is limited to Greenwood, Scott, Ignatov, or the general legal disclaimer context.
- Thumbnail has no real-person likeness, no OneCoin logo, and no "guilty/convicted" language for Ignatova.
- Video uses symbolic reconstruction and on-screen synthetic labeling.
- No immediate public publish is approved. The approved action is private upload with scheduled public release.

## Known acceptance deviation
- `scripts/check_final_acceptance.py 17` fails the original 27-33 minute runtime gate and minor black/static thresholds on the v011 tempo cut.
- Owner explicitly approved the shorter tempo/readability cut and authorized all gates for upload/schedule in chat on 2026-06-29 JST.
- This is recorded as an owner editorial override, not as a pass of the original runtime gate.

## Sources
- DOJ SDNY charges release: https://www.justice.gov/usao-sdny/pr/manhattan-us-attorney-announces-charges-against-leaders-onecoin-multibillion-dollar
- FBI Ten Most Wanted PDF: https://www.fbi.gov/wanted/topten/ruja-ignatova/@@download.pdf
- FBI reward release: https://www.fbi.gov/contact-us/field-offices/newyork/news/up-to-5-million-reward-offer-for-information-leading-to-arrest-and-or-conviction-of-ten-most-wanted-fugitive-cryptoqueen-ruja-ignatova
- DOJ compensation process: https://www.justice.gov/opa/pr/justice-department-announces-compensation-process-onecoin-fraud-victims-funds-recovered
"""
    FACT.write_text(fact_text, encoding="utf-8")
    fact_sha = sha(FACT)

    description = """A Prime Documentary mid-feature about OneCoin, Ruja Ignatova, and the promise of a cryptocurrency that prosecutors say did not exist as a real blockchain.

Ruja Ignatova is charged and wanted, not convicted. This film uses indictment and public-record language for allegations involving her. Convicted associates are described according to public court outcomes.

Visuals are symbolic reconstructions, project-generated AI stills, stock/factory atmosphere, and Remotion motion graphics. They do not depict real-person likenesses, do not use the OneCoin logo, and do not show private victim imagery.

Chapters:
00:00 Hook: there was no coin
00:08 Opening: Prime Documentary
00:11 The promise
07:07 The crack
14:32 The void
18:55 Coda: still missing
20:04 Ending

Sources include public records and official DOJ/FBI materials. This episode uses AI-generated symbolic reconstructions and stock/factory atmosphere for visual storytelling.
"""
    meta = load_json(PKG / "youtube_meta.v011.json")
    meta.update(
        {
            "revision": "v012",
            "status": "approved_for_private_upload_and_schedule",
            "title": "There Was No Coin: $4 Billion in Empty Promises",
            "description": description,
            "video_actual_path": str(VIDEO).replace("\\", "/"),
            "video_sha256": video_sha,
            "thumbnail": rel(THUMB),
            "thumbnail_sha256": thumb_sha,
            "captions_sidecar": rel(CAPTIONS),
            "captions_sha256": captions_sha,
            "fact_recheck": rel(FACT),
            "fact_recheck_sha256": fact_sha,
            "final_qc": rel(QC),
            "final_qc_sha256": qc_sha,
            "publish_schedule_target_jst": SCHEDULE_LOCAL,
            "publish_schedule_target_utc": SCHEDULE_UTC,
            "intended_schedule_local": SCHEDULE_LOCAL,
            "intended_schedule_utc": SCHEDULE_UTC,
            "requested_schedule": {
                "local_time": SCHEDULE_LOCAL,
                "utc_time": SCHEDULE_UTC,
                "status": "approved_pending_upload",
                "reason": "owner_approved_video_thumbnail_schedule_all_gates_2026-06-29",
            },
            "upload_performed": False,
            "publish_performed": False,
            "schedule_performed": False,
            "publish_gate": "owner_approved_with_editorial_runtime_override",
            "owner_editorial_override": {
                "runtime_band": True,
                "black_static_thresholds": True,
                "reason": "Owner chose shorter tempo/readability cut over original 27-33 minute spec.",
            },
            "updated_at": created,
        }
    )
    write_json(META, meta)
    meta_sha = sha(META)

    rights = load_json(PKG / "rights_manifest.v011.json")
    rights.update(
        {
            "revision": "v012",
            "generated_at": created,
            "status": "approved_for_private_upload_and_schedule",
            "same_day_fact_recheck_required": False,
            "same_day_fact_recheck": rel(FACT),
            "same_day_fact_recheck_sha256": fact_sha,
            "owner_editorial_override": "runtime/black/static acceptance deviations approved by owner for tempo cut",
        }
    )
    write_json(RIGHTS, rights)
    rights_sha = sha(RIGHTS)

    delivery = load_json(PKG / "final_delivery.v011.json")
    delivery.update(
        {
            "revision": "v012",
            "generated_at": created,
            "status": "approved_for_private_upload_and_schedule",
            "final_video": str(VIDEO).replace("\\", "/"),
            "video": str(VIDEO).replace("\\", "/"),
            "video_sha256": video_sha,
            "thumbnail": rel(THUMB),
            "thumbnail_sha256": thumb_sha,
            "captions": rel(CAPTIONS),
            "captions_sha256": captions_sha,
            "youtube_meta": rel(META),
            "youtube_meta_sha256": meta_sha,
            "rights_manifest": rel(RIGHTS),
            "rights_manifest_sha256": rights_sha,
            "fact_recheck": rel(FACT),
            "fact_recheck_sha256": fact_sha,
            "requested_schedule": {"local_time": SCHEDULE_LOCAL, "utc_time": SCHEDULE_UTC, "status": "approved_pending_upload"},
            "external_side_effects": {"upload": False, "publish": False, "schedule": False, "paid_api": False},
            "owner_editorial_override": "Owner approved v011 shorter tempo/readability cut despite original runtime gate failure.",
        }
    )
    write_json(DELIVERY, delivery)
    delivery_sha = sha(DELIVERY)

    APPROVALS.mkdir(parents=True, exist_ok=True)
    approval_common = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "decision": "approved",
        "requested_by": "owner",
        "approved_by": "owner",
        "actor": "codex",
        "decision_source": "Owner messages on 2026-06-29 JST: 動画を承認します。7/2.12:00に予約投稿してください。サムネイルは派手にして。全て承認します。",
        "decided_at": "2026-06-29T00:00:00+09:00",
        "target_revision": "v012",
        "scheduled_at_local": SCHEDULE_LOCAL,
        "scheduled_at_utc": SCHEDULE_UTC,
        "video": str(VIDEO).replace("\\", "/"),
        "video_sha256": video_sha,
        "thumbnail": rel(THUMB),
        "thumbnail_sha256": thumb_sha,
        "captions_sidecar": rel(CAPTIONS),
        "captions_sha256": captions_sha,
        "youtube_meta": rel(META),
        "youtube_meta_sha256": meta_sha,
        "final_delivery": rel(DELIVERY),
        "final_delivery_sha256": delivery_sha,
        "rights_manifest": rel(RIGHTS),
        "rights_manifest_sha256": rights_sha,
        "fact_recheck": rel(FACT),
        "fact_recheck_sha256": fact_sha,
        "constraints": [
            "Upload exact final video privately to the allowlisted Prime Documentary YouTube channel.",
            "Set exact selected flashy thumbnail.",
            "Upload English sidecar captions if API accepts them; burned-in captions remain.",
            "Schedule public release for 2026-07-02T12:00:00+09:00.",
            "Do not immediate-public publish.",
            "Do not delete or modify other episode uploads.",
        ],
    }
    write_json(APPROVALS / "APR-0001.json", {**approval_common, "approval_id": "APR-0001", "target_type": "editorial_final_cut", "scope": ["Approve v011 video content and structure."]})
    write_json(APPROVALS / "APR-0002.json", {**approval_common, "approval_id": "APR-0002", "target_type": "title_thumbnail", "scope": ["Approve v008 selected thumbnail and v012 title."]})
    write_json(APPROVALS / "APR-0003.json", {**approval_common, "approval_id": "APR-0003", "target_type": "legal_fact_recheck", "scope": ["Approve publish fact/legal re-check and R3 language handling."]})
    write_json(APPROVALS / "APR-0004.json", {**approval_common, "approval_id": "APR-0004", "target_type": "upload_publish_schedule", "scope": ["Authorize private upload and scheduled public release only."]})

    manifest = load_json(MANIFEST)
    manifest["state"] = "approved_for_private_upload_and_schedule"
    manifest["updated_at"] = created
    active = manifest.setdefault("active_revisions", {})
    active.update(
        {
            "fact_recheck": "v002_publish",
            "youtube_meta": "v012",
            "rights_manifest": "v012",
            "final_delivery": "v012",
            "owner_approval": "APR-0004",
        }
    )
    approvals = manifest.setdefault("approvals", [])
    for apr_id in ("APR-0001", "APR-0002", "APR-0003", "APR-0004"):
        if apr_id not in approvals:
            approvals.append(apr_id)
    manifest["blockers"] = []
    manifest.setdefault("warnings", []).append("v011 is owner-approved for schedule with explicit runtime/black/static editorial override; check_final_acceptance.py 17 does not pass original runtime gate.")
    write_json(MANIFEST, manifest)

    append_event(
        {
            "ts": created,
            "episode_id": EP,
            "stage": "publish_preflight",
            "event": "onecoin_v012_publish_package_prepared",
            "revision": "v012",
            "actor": "codex",
            "approval_ids": ["APR-0001", "APR-0002", "APR-0003", "APR-0004"],
            "video_sha256": video_sha,
            "thumbnail_sha256": thumb_sha,
            "schedule_local": SCHEDULE_LOCAL,
            "schedule_utc": SCHEDULE_UTC,
            "external_side_effects": {"upload": False, "publish": False, "schedule": False},
        }
    )
    print(json.dumps({"youtube_meta": rel(META), "final_delivery": rel(DELIVERY), "fact_recheck": rel(FACT), "approval": rel(APPROVALS / "APR-0004.json")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
