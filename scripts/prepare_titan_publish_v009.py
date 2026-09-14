#!/usr/bin/env python3
"""Prepare Titan v009 publish metadata and approval records.

No external API calls. This records the owner's current approvals for the exact
v008 cut and prepares publication metadata for a 2026-07-01 12:00 JST target.
Public scheduling remains blocked until a same-day fact re-check dated
2026-07-01 is present.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-016-titan"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
APPROVALS = EPDIR / "approvals"
RESEARCH = EPDIR / "01_research"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"

REV = "v009"
CUT_REV = "v008"
SCRIPT_REV = "v001"
SCHEDULE_LOCAL = "2026-07-01T12:00:00+09:00"
SCHEDULE_UTC = "2026-07-01T03:00:00Z"

VIDEO = Path("E:/pd-media/episodes/PD-2026-016-titan/07_edit/v008.mp4")
THUMB = PKG / "thumbnail.selected.v002.png"
CAPTIONS = EPDIR / "08_edit" / "captions.v008.srt"
FINAL_QC = EPDIR / "08_edit" / "renders" / "final.v008.qc.json"
CAPTION_QC = EPDIR / "08_edit" / "captions.v008.qc.json"
AUDIO_QC = EPDIR / "08_edit" / "audio_mix.v008.qc.json"

YOUTUBE_META = PKG / f"youtube_meta.{REV}.json"
FINAL_DELIVERY = PKG / f"final_delivery.{REV}.json"
RIGHTS = PKG / f"rights_manifest.{REV}.json"
FACT_RECHECK = RESEARCH / "fact_recheck.v002.md"
APR_PRIVATE = APPROVALS / "APR-0002.json"
APR_SCHEDULE = APPROVALS / "APR-0003.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")


def append_event(event: str, note: str) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "episode_id": EP,
        "stage": "publish_prep",
        "event": event,
        "revision": REV,
        "actor": "codex",
        "note": note,
    }
    with EVENTS.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def require_inputs() -> None:
    for path in (VIDEO, THUMB, CAPTIONS, FINAL_QC, CAPTION_QC, AUDIO_QC, MANIFEST, PKG / "youtube_meta.v008.json", PKG / "rights_manifest.v008.json"):
        if not path.exists():
            raise FileNotFoundError(path)
    final_qc = load_json(FINAL_QC)
    caption_qc = load_json(CAPTION_QC)
    audio_qc = load_json(AUDIO_QC)
    if final_qc.get("qc_status") != "pass":
        raise RuntimeError(f"final QC is not pass: {FINAL_QC}")
    if caption_qc.get("qc_status") != "pass":
        raise RuntimeError(f"caption QC is not pass: {CAPTION_QC}")
    if audio_qc.get("qc_status") != "pass":
        raise RuntimeError(f"audio QC is not pass: {AUDIO_QC}")
    if final_qc.get("sha256") != sha(VIDEO):
        raise RuntimeError("video hash mismatch against final QC")


def build_description() -> str:
    return """In June 2023, five people descended toward the Titanic inside the experimental Titan submersible. For four days, the world waited for a rescue. Investigators later concluded the loss was preventable.

This Prime Documentary feature follows the warning signs: the waiver, the uncertified design, the 2018 whistleblower dispute, the Marine Technology Society letter, the final dive, the search, and the official findings that came after.

Visual note: this film uses narration, documents, motion graphics, stock atmosphere, and symbolic AI-assisted reconstructions. The visuals are not authentic footage of the incident, do not depict the real passengers or crew, and do not show the implosion or remains.

Chapters:
00:00 Hook: the last sound
00:09 Opening: Pure Waste
00:46 The dream
09:27 The warnings
19:52 The dive
24:11 The search
29:23 The truth
34:50 Ending: what remains
"""


def build_fact_recheck(now: str) -> None:
    text = f"""# PD-2026-016-titan — Pre-Publish Fact Re-Check v002

- Episode: {EP}
- Built cut: {CUT_REV}
- Active script revision: {SCRIPT_REV}
- Re-check date: 2026-06-29 JST
- Status: current re-check completed, but this is **not** the required 2026-07-01 same-day publish re-check.

## Result

Current authoritative sources still support the episode's core claims: the USCG MBI report was released on 2025-08-05 and called the casualty preventable; the MTS CG-068 redacted PDF resolves and contains the "minor to catastrophic" wording; NTSB MIR-25-36 is now live and its probable-cause analysis is consistent with the episode's USCG-attributed hull/delamination framing.

## Important caveat

The Rush quote source is confirmed as CBS/David Pogue and New York Magazine transcript wording: "safety just is pure waste." The v008 narration says "safety is just pure waste." This is semantically close but not verbatim. Because the current approved script/cut is v001/v008, publication should either accept this as a minor quote-order deviation or require a new script/audio/render revision before public release.

## Sources checked

- USCG press release, 2025-08-05: https://www.news.uscg.mil/Press-Releases/Article/4265651/coast-guard-marine-board-of-investigation-releases-report-on-titan-submersible/
- USCG exhibit CG-068, MTS letter redacted PDF: https://media.defense.gov/2024/Sep/20/2003551144/-1/-1/0/CG-068%20MARINE%20TECHNOLOGY%20SOCIETY%20LETTER%20TO%20OCEANGATE%20INC.%20MARCH%2027%2C%202018_REDACTED.PDF
- NTSB investigation page DCA23FM036: https://www.ntsb.gov/investigations/Pages/DCA23FM036.aspx
- NTSB MIR-25-36 PDF: https://www.ntsb.gov/investigations/AccidentReports/Reports/MIR2536.pdf
- CBS transcript: https://www.cbsnews.com/news/titanic-submersible-interview-transcript-with-oceangate-ceo-stockton-rush/
- New York Magazine transcript: https://nymag.com/intelligencer/2023/06/what-i-learned-on-a-titanic-submarine-expedition.html

Generated at: {now}
"""
    FACT_RECHECK.write_text(text, encoding="utf-8")


def build_package(now: str) -> tuple[dict, dict, dict]:
    video_sha = sha(VIDEO)
    thumb_sha = sha(THUMB)
    captions_sha = sha(CAPTIONS)
    final_qc = load_json(FINAL_QC)
    caption_qc = load_json(CAPTION_QC)
    audio_qc = load_json(AUDIO_QC)

    meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": REV,
        "source_cut_revision": CUT_REV,
        "status": "owner_approved_private_upload_ready_public_schedule_blocked_pending_2026_07_01_fact_recheck",
        "title": "They Were Warned — The Last Dive of the Titan",
        "working_title": "Pure Waste - The Last Dive of the Titan",
        "description": build_description(),
        "chapters": load_json(PKG / "youtube_meta.v008.json").get("chapters", []),
        "tags": [
            "Titan submersible",
            "Titan disaster",
            "OceanGate Titan",
            "Titanic submersible",
            "deep sea documentary",
            "submersible disaster",
            "US Coast Guard report",
            "NTSB Titan report",
            "carbon fiber pressure hull",
            "Prime Documentary",
            "documentary feature",
        ],
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
        "made_for_kids": False,
        "containsSyntheticMedia": True,
        "synthetic_content_disclosure_required": True,
        "contains_ai_symbolic_reconstruction": True,
        "video_actual_path": str(VIDEO).replace("\\", "/"),
        "video_sha256": video_sha,
        "thumbnail": rel(THUMB),
        "thumbnail_sha256": thumb_sha,
        "captions_sidecar": rel(CAPTIONS),
        "captions_sha256": captions_sha,
        "captions_burned_in": True,
        "captions_qc": rel(CAPTION_QC),
        "audio_qc": rel(AUDIO_QC),
        "final_qc": rel(FINAL_QC),
        "requested_schedule": {
            "local_time": SCHEDULE_LOCAL,
            "utc_time": SCHEDULE_UTC,
            "timezone": "Asia/Tokyo",
            "status": "blocked_pending_final_same_day_fact_recheck",
        },
        "intended_schedule_local": SCHEDULE_LOCAL,
        "intended_schedule_utc": SCHEDULE_UTC,
        "privacy_status_target": "private_upload_first",
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
        "publish_gate": "blocked_pending_final_same_day_fact_recheck",
        "approval_ids": ["APR-0001", "APR-0002", "APR-0003"],
        "pre_publish_fact_recheck": rel(FACT_RECHECK),
        "known_publication_blockers": [
            "Final same-day fact re-check must be performed on 2026-07-01 before public scheduling/publish.",
            "Rush quote in v008 narration uses 'safety is just pure waste'; source transcript wording is 'safety just is pure waste'. Owner must accept this deviation or request a corrected cut before public release.",
        ],
        "created_at": now,
        "qc": {
            "final_qc_status": final_qc.get("qc_status"),
            "caption_qc_status": caption_qc.get("qc_status"),
            "audio_qc_status": audio_qc.get("qc_status"),
            "duration_seconds": final_qc.get("duration_seconds"),
        },
    }
    write_json(YOUTUBE_META, meta)

    delivery = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": REV,
        "source_cut_revision": CUT_REV,
        "generated_at": now,
        "status": "owner_approved_private_upload_ready_public_schedule_blocked_pending_2026_07_01_fact_recheck",
        "video": str(VIDEO).replace("\\", "/"),
        "video_sha256": video_sha,
        "duration_seconds": final_qc.get("duration_seconds"),
        "runtime_band_pass": final_qc.get("runtime_band_pass"),
        "thumbnail": rel(THUMB),
        "thumbnail_sha256": thumb_sha,
        "captions": rel(CAPTIONS),
        "captions_sha256": captions_sha,
        "youtube_meta": rel(YOUTUBE_META),
        "rights_manifest": rel(RIGHTS),
        "pre_publish_fact_recheck": rel(FACT_RECHECK),
        "approval_ids": ["APR-0001", "APR-0002", "APR-0003"],
        "requested_schedule": meta["requested_schedule"],
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
        "external_side_effects": {"upload": False, "publish": False, "schedule": False, "new_paid_api_calls": False},
        "known_publication_blockers": meta["known_publication_blockers"],
    }
    write_json(FINAL_DELIVERY, delivery)

    prev_rights = load_json(PKG / "rights_manifest.v008.json")
    rights = {
        **prev_rights,
        "revision": REV,
        "generated_at": now,
        "status": "owner_approved_conditional_pre_publish",
        "publication_gate": "blocked_pending_final_same_day_fact_recheck",
        "publication_approval": "APR-0003",
        "pre_publish_fact_recheck": rel(FACT_RECHECK),
        "assets": [
            {"asset_id": f"{EP}-final-render-{CUT_REV}", "type": "final_render", "file": str(VIDEO).replace("\\", "/"), "sha256": video_sha, "rights_status": "conditional"},
            {"asset_id": f"{EP}-captions-{CUT_REV}", "type": "captions", "file": rel(CAPTIONS), "sha256": captions_sha, "rights_status": "clear"},
            {"asset_id": f"{EP}-thumbnail-v002", "type": "thumbnail", "file": rel(THUMB), "sha256": thumb_sha, "rights_status": "conditional"},
        ],
    }
    rights.setdefault("notes", []).append("Owner approved the selected v002 thumbnail and v008 review cut on 2026-06-29; public scheduling remains blocked until the 2026-07-01 same-day fact re-check.")
    write_json(RIGHTS, rights)

    return meta, delivery, rights


def write_approvals(now: str, meta: dict) -> None:
    instruction = "Owner chat instruction on 2026-06-29: 全て承認するから7/1.12:00に予約投稿して。サムネイルはもうわかってるよね。承認するから完了させて。"
    common = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "requested_at": now,
        "requested_by": "codex",
        "decided_at": now,
        "decided_by": "owner",
    }
    apr2 = {
        **common,
        "approval_id": "APR-0002",
        "decision": "approved",
        "target_type": "package",
        "target_id": f"{EP}:{CUT_REV}:youtube_meta.{REV}",
        "target_revision": REV,
        "notes": (
            f"{instruction} Approves the v008 first cut, selected title/thumbnail pair, and private upload preparation/upload. "
            f"Bound hashes: script={SCRIPT_REV}; final_render={CUT_REV} {meta['video_sha256']}; "
            f"thumbnail=v002 {meta['thumbnail_sha256']}; youtube_meta={sha(YOUTUBE_META)}; "
            f"final_delivery={sha(FINAL_DELIVERY)}; rights_manifest={sha(RIGHTS)}. "
            "Does not by itself authorize public scheduling until APR-0003 conditions are satisfied."
        ),
        "conditions": [
            "Upload must be private first.",
            "No immediate public publish.",
            "Use the exact v008 video hash and v002 thumbnail hash recorded in this APR.",
        ],
        "expires_at": None,
        "evidence_snapshot_ref": f"artifact://{rel(FINAL_DELIVERY)}",
    }
    apr3 = {
        **common,
        "approval_id": "APR-0003",
        "decision": "approved_with_conditions",
        "target_type": "publish",
        "target_id": f"{EP}:{CUT_REV}:2026-07-01T12:00:00+09:00",
        "target_revision": REV,
        "notes": (
            f"{instruction} Owner explicitly requested scheduling for {SCHEDULE_LOCAL} ({SCHEDULE_UTC}). "
            f"Bound hashes: final_render={CUT_REV} {meta['video_sha256']}; thumbnail=v002 {meta['thumbnail_sha256']}; "
            f"youtube_meta={sha(YOUTUBE_META)}. Activation remains blocked until the final same-day pre-publish fact re-check "
            "is completed on 2026-07-01 and any quote-fidelity risk is accepted or corrected."
        ),
        "conditions": [
            "FINAL same-day fact re-check must be dated 2026-07-01 before public scheduling/publish.",
            "Rush quote deviation in v008 must be explicitly accepted for public release or corrected in a new cut.",
            "No immediate public publish; schedule only for the recorded timestamp.",
            "Channel ID must match allowlist.",
        ],
        "expires_at": "2026-07-01T12:00:00+09:00",
        "evidence_snapshot_ref": f"artifact://{rel(YOUTUBE_META)}",
    }
    write_json(APR_PRIVATE, apr2)
    write_json(APR_SCHEDULE, apr3)


def update_manifest(now: str, meta: dict, delivery: dict) -> None:
    manifest = load_json(MANIFEST)
    manifest["state"] = "publish_approved"
    manifest["updated_at"] = now
    active = manifest.setdefault("active_revisions", {})
    active.pop("owner_private_upload_approval", None)
    active.pop("owner_public_schedule_approval", None)
    active.update(
        {
            "youtube_meta": REV,
            "rights_manifest": REV,
            "final_delivery": REV,
            "pre_publish_fact_recheck": "v002",
        }
    )
    approvals = manifest.setdefault("approvals", [])
    for approval in ("APR-0001", "APR-0002", "APR-0003"):
        if approval not in approvals:
            approvals.append(approval)
    blockers = manifest.setdefault("blockers", [])
    for blocker in delivery["known_publication_blockers"]:
        if blocker not in blockers:
            blockers.append(blocker)
    artifacts = manifest.setdefault("artifacts", [])
    new_artifacts = [
        (f"{EP}-youtube-meta-{REV}", "youtube_meta", YOUTUBE_META, "conditional", "pass", "candidate"),
        (f"{EP}-final-delivery-{REV}", "final_delivery", FINAL_DELIVERY, "conditional", "pass", "candidate"),
        (f"{EP}-rights-manifest-{REV}", "rights_manifest", RIGHTS, "conditional", "pass", "candidate"),
        (f"{EP}-pre-publish-fact-recheck-v002", "pre_publish_fact_recheck", FACT_RECHECK, "conditional", "warn", "candidate", "v002"),
        (f"{EP}-approval-APR-0002", "approval", APR_PRIVATE, "clear", "pass", "approved", "v001"),
        (f"{EP}-approval-APR-0003", "approval", APR_SCHEDULE, "conditional", "warn", "approved", "v001"),
    ]
    ids = {item[0] for item in new_artifacts}
    artifacts[:] = [a for a in artifacts if a.get("artifact_id") not in ids]
    for item in new_artifacts:
        aid, atype, path, rights, qc, status = item[:6]
        artifact_revision = item[6] if len(item) > 6 else REV
        artifacts.append(
            {
                "artifact_id": aid,
                "artifact_type": atype,
                "revision": artifact_revision,
                "uri": f"artifact://{rel(path)}",
                "checksum": sha(path),
                "status": status,
                "rights_status": rights,
                "qc_status": qc,
            }
        )
    warnings = manifest.setdefault("warnings", [])
    warning = f"Owner approved Titan {CUT_REV} title/thumbnail/private-upload package and conditionally approved 2026-07-01 12:00 JST public schedule, but public scheduling is blocked until the 2026-07-01 same-day fact re-check and Rush quote deviation decision."
    if warning not in warnings:
        warnings.append(warning)
    write_json(MANIFEST, manifest)


def main() -> int:
    now = datetime.now(timezone.utc).isoformat()
    require_inputs()
    build_fact_recheck(now)
    meta, delivery, _rights = build_package(now)
    write_approvals(now, meta)
    update_manifest(now, meta, delivery)
    append_event("publish_package_prepared", f"Prepared {REV} publish metadata and APR-0002/APR-0003 for {CUT_REV}; schedule remains blocked pending 2026-07-01 fact re-check.")
    print(
        json.dumps(
            {
                "episode_id": EP,
                "revision": REV,
                "cut_revision": CUT_REV,
                "video_sha256": meta["video_sha256"],
                "thumbnail_sha256": meta["thumbnail_sha256"],
                "schedule_local": SCHEDULE_LOCAL,
                "schedule_utc": SCHEDULE_UTC,
                "public_schedule_gate": "blocked_pending_final_same_day_fact_recheck",
                "youtube_meta": rel(YOUTUBE_META),
                "final_delivery": rel(FINAL_DELIVERY),
                "apr_private": rel(APR_PRIVATE),
                "apr_schedule": rel(APR_SCHEDULE),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
