#!/usr/bin/env python3
"""Build the Theranos final v006 package records.

No upload, publish, schedule, paid API, or media generation is performed.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from hashlib import sha256 as _sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-015-theranos"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
FINAL_VIDEO = Path("H:/pd-media/episodes/PD-2026-015-theranos/08_edit/renders/final/theranos_premium_final_v005.mp4")
CAPTIONS = EPDIR / "08_edit" / "captions.v001.srt"
ACCEPTANCE = EPDIR / "08_edit" / "renders" / "final.v005.acceptance.json"
THUMB = PKG / "thumbnail.selected.v001.png"
NARR_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
AUDIO_MIX = EPDIR / "06_audio" / "audio_mix.v001.json"
FACTORY_TS = ROOT / "remotion" / "src" / "data" / "theranos_factory_assets.ts"
STOCK_LEDGER = EPDIR / "05_stock" / "stock_ledger.v001.json"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"

TITLE = "When Does a Bold Promise Become a Crime? The Rise and Fall of Theranos"
SHORT_TITLE = "When Does a Bold Promise Become a Crime?"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = _sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def ffprobe(path: Path) -> dict[str, Any]:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        text=True,
        encoding="utf-8",
    )
    return json.loads(out)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def mmss(seconds: float) -> str:
    s = int(seconds)
    return f"{s // 60:02d}:{s % 60:02d}"


def factory_assets() -> list[dict[str, Any]]:
    text = FACTORY_TS.read_text(encoding="utf-8")
    match = re.search(r"export const THERANOS_FACTORY_ASSETS: TheranosFactoryAsset\[] = (\[.*\]);", text, re.S)
    return json.loads(match.group(1)) if match else []


def chapters() -> list[dict[str, str]]:
    return [
        {"time": "00:00", "title": "Hook: promise, verdict, sentence"},
        {"time": "00:12", "title": "A drop, a valuation, a collapse"},
        {"time": "01:35", "title": "Act I: the blood-testing pitch"},
        {"time": "03:37", "title": "Act II: investigation and collapse"},
        {"time": "05:26", "title": "Act III: failure or fraud"},
        {"time": "07:10", "title": "The verdict count by count"},
        {"time": "08:42", "title": "Act IV: where the legal line is"},
        {"time": "10:04", "title": "Finale: the series question"},
        {"time": "11:36", "title": "Endcard"},
    ]


def tags() -> list[str]:
    return [
        "Theranos",
        "Elizabeth Holmes",
        "corporate fraud",
        "startup fraud",
        "wire fraud",
        "investor fraud",
        "Silicon Valley",
        "true crime documentary",
        "business documentary",
        "Prime Documentary",
    ]


def write_rights_manifest(video_sha: str, captions_sha: str, thumb_sha: str, final_duration: float) -> Path:
    rights = load_json(PKG / "rights_manifest.v001.json")
    rights.update(
        {
            "revision": "v006",
            "generated_at": now(),
            "status": "final_candidate_rights_registered_pending_owner_and_R3_legal_review",
            "commercial_use_ok_for_review_package": True,
            "commercial_use_ok_for_public_release": "pending_R3_legal_review",
            "public_release_gate": "closed_until_APR-0002_APR-0003_APR-0004_APR-0005_APR-0006",
            "final_video": {
                "path": str(FINAL_VIDEO).replace("\\", "/"),
                "sha256": video_sha,
                "duration_seconds": round(final_duration, 2),
                "acceptance": rel(ACCEPTANCE),
                "acceptance_sha256": sha256(ACCEPTANCE),
            },
            "thumbnail": {
                "selected_id": "B",
                "selected_title": SHORT_TITLE,
                "selected_thumbnail_text": "DREAM OR CRIME?",
                "selected_file": rel(THUMB),
                "selected_sha256": thumb_sha,
                "selected_background": "THUMB-02.png",
                "reason": "Best current combination of story clarity, mobile legibility, rights safety, and brand fit.",
            },
            "narration": {
                "kind": "elevenlabs_master_mix",
                "provider": "ElevenLabs",
                "voice_id": "nPczCjzI2devNBz1zQrb",
                "narration_index": rel(NARR_INDEX),
                "audio_mix": rel(AUDIO_MIX),
                "captions": rel(CAPTIONS),
                "captions_sha256": captions_sha,
                "public_release_allowed": "pending_owner_APR-0004",
                "note": "Final render uses the approved ElevenLabs master-derived mix; no regeneration was performed.",
            },
        }
    )
    rights["assets"] = [
        item
        for item in rights.get("assets", [])
        if "review_proxy" not in json.dumps(item, sort_keys=True).lower()
    ]

    stock = load_json(STOCK_LEDGER)
    factory_rows = [
        item
        for item in stock.get("assets", [])
        if item.get("asset_type") == "factory_stock" and str(item.get("asset_id", "")).startswith(f"{EP}-AF-")
    ]
    existing_ids = {item.get("asset_id") for item in rights.get("assets", [])}
    for item in factory_rows:
        if item["asset_id"] not in existing_ids:
            rights.setdefault("assets", []).append(item)

    rights.setdefault("final_package_notes", []).extend(
        [
            "Final render is a candidate for owner/R3 legal review only; no upload, schedule, or publish approval is implied.",
            "Factory and stock visuals are generic illustrative material, not evidence of Theranos facilities, devices, people, or logos.",
        ]
    )
    out = PKG / "rights_manifest.v006.json"
    write_json(out, rights)
    return out


def write_youtube_meta(video_sha: str, captions_sha: str, thumb_sha: str) -> Path:
    description = (
        "Theranos promised a blood-testing revolution. The legal question is narrower and harder: "
        "when does a bold business promise become criminal fraud?\n\n"
        "This episode follows the record: the investor-fraud counts that produced convictions, "
        "the patient counts that resulted in acquittals, and the counts with no verdict. "
        "Acquittal is not treated as exoneration; the distinction is the point.\n\n"
        "Visual note: this video uses licensed stock/factory media, AI-generated symbolic reconstructions, "
        "and motion design. No real-person likeness of Elizabeth Holmes, Ramesh Balwani, or any other real person is intended.\n\n"
        "Public upload remains blocked until owner approval and R3 legal/rights review are recorded for the exact final hashes."
    )
    data = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v006",
        "status": "final_candidate_owner_review_required",
        "title": TITLE,
        "description": description,
        "chapters": chapters(),
        "tags": tags(),
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
        "thumbnail": rel(THUMB),
        "selected_thumbnail_sha256": thumb_sha,
        "video_actual_path": str(FINAL_VIDEO).replace("\\", "/"),
        "video_sha256": video_sha,
        "captions_sidecar": rel(CAPTIONS),
        "captions_sha256": captions_sha,
        "captions_burned_in": True,
        "synthetic_content_disclosure_required": True,
        "contains_ai_symbolic_reconstruction": True,
        "privacy_status_target": "private",
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
        "publish_gate": "closed",
        "blocking_requirements": [
            "APR-0002 owner approval for exact final video hash",
            "APR-0003 title/thumbnail approval",
            "APR-0004 final narration release approval",
            "APR-0005 R3 legal/rights review",
            "APR-0006 upload/publish/schedule approval",
        ],
        "created_at": now(),
    }
    out = PKG / "youtube_meta.v006.json"
    write_json(out, data)
    (PKG / "title.v006.txt").write_text(TITLE + "\n", encoding="utf-8")
    write_json(PKG / "chapters.v006.json", {"episode_id": EP, "revision": "v006", "chapters": chapters()})
    write_json(PKG / "tags.v006.json", {"episode_id": EP, "revision": "v006", "tags": tags()})
    return out


def write_final_delivery(video_sha: str, captions_sha: str, thumb_sha: str, probe: dict[str, Any], rights: Path, meta: Path) -> Path:
    acc = load_json(ACCEPTANCE)
    data = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v006",
        "status": "final_candidate_owner_review_required",
        "generated_at": now(),
        "final_video": str(FINAL_VIDEO).replace("\\", "/"),
        "final_video_exists": FINAL_VIDEO.exists(),
        "final_video_sha256": video_sha,
        "ffprobe": probe,
        "runtime_seconds": round(float(probe["format"]["duration"]), 2),
        "runtime_mmss": mmss(float(probe["format"]["duration"])),
        "selected_thumbnail": rel(THUMB),
        "selected_thumbnail_sha256": thumb_sha,
        "captions": rel(CAPTIONS),
        "captions_sha256": captions_sha,
        "youtube_meta": rel(meta),
        "rights_manifest": rel(rights),
        "acceptance": rel(ACCEPTANCE),
        "acceptance_sha256": sha256(ACCEPTANCE),
        "acceptance_status": acc.get("status"),
        "acceptance_results": acc.get("results", []),
        "audio_mix": rel(AUDIO_MIX),
        "narration_index": rel(NARR_INDEX),
        "composition": "TheranosPremium",
        "render_command": "npx remotion render TheranosPremium <final.mp4> --codec=h264 --crf=16",
        "external_side_effects": {
            "upload": False,
            "publish": False,
            "schedule": False,
            "paid_api": False,
        },
        "owner_stop_point": "Final candidate is ready. STOP for owner approval and R3 legal/rights review before any upload/publish/schedule.",
    }
    out = PKG / "final_delivery.v006.json"
    write_json(out, data)
    return out


def write_review_packets(video_sha: str, captions_sha: str, thumb_sha: str, final_delivery: Path, rights: Path, meta: Path) -> tuple[Path, Path, Path]:
    fd_sha = sha256(final_delivery)
    rights_sha = sha256(rights)
    meta_sha = sha256(meta)
    acc_sha = sha256(ACCEPTANCE)
    fd = load_json(final_delivery)
    legal = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v006",
        "created_at": now(),
        "status": "final_R3_legal_rights_review_required",
        "public_release_recommendation": "do_not_publish_until_APR-0005_and_APR-0006_are_recorded_for_exact_hashes",
        "external_side_effects": {"paid_api": False, "upload": False, "publish": False, "schedule": False},
        "exact_targets": {
            "final_video": str(FINAL_VIDEO).replace("\\", "/"),
            "final_video_sha256": video_sha,
            "final_delivery": rel(final_delivery),
            "final_delivery_sha256": fd_sha,
            "acceptance": rel(ACCEPTANCE),
            "acceptance_sha256": acc_sha,
            "youtube_meta": rel(meta),
            "youtube_meta_sha256": meta_sha,
            "rights_manifest": rel(rights),
            "rights_manifest_sha256": rights_sha,
            "thumbnail": rel(THUMB),
            "thumbnail_sha256": thumb_sha,
            "captions": rel(CAPTIONS),
            "captions_sha256": captions_sha,
        },
        "hard_gate_summary": fd["acceptance_results"],
        "r3_review_points": [
            "Investor-fraud convictions are stated as verdict facts only.",
            "Patient counts remain ACQUITTED/not guilty; three counts remain NO VERDICT/mistrial.",
            "Acquittal is not framed as exoneration or proof that the technology worked.",
            "No real-person likeness, real footage, Theranos logo, real Edison device, magazine cover, or specific facility is used as such.",
            "All AI visuals remain labelled symbolic reconstruction in-video.",
            "Factory/stock materials are generic illustrative assets with provenance in rights_manifest.v006.",
        ],
    }
    legal_json = PKG / "legal_rights_review_packet.v006.json"
    write_json(legal_json, legal)
    legal_md = PKG / "legal_rights_review_packet.v006.md"
    legal_md.write_text(
        "# Theranos v006 R3 Legal/Rights Review Packet\n\n"
        f"- Final video: `{str(FINAL_VIDEO).replace(chr(92), '/')}`\n"
        f"- Final video SHA-256: `{video_sha}`\n"
        f"- Acceptance: `{rel(ACCEPTANCE)}` / `{acc_sha}` / PASS\n"
        f"- Final delivery: `{rel(final_delivery)}` / `{fd_sha}`\n"
        f"- Rights manifest: `{rel(rights)}` / `{rights_sha}`\n"
        f"- YouTube metadata: `{rel(meta)}` / `{meta_sha}`\n\n"
        "STOP: public release requires APR-0005 legal/rights approval and APR-0006 publish/schedule approval for these exact hashes.\n",
        encoding="utf-8",
    )

    owner = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v006",
        "created_at": now(),
        "status": "owner_review_required",
        "gate": "final_candidate_owner_review_plus_R3_legal_rights_review",
        "public_release_allowed": False,
        "external_side_effects": {"paid_api": False, "upload": False, "publish": False, "schedule": False},
        "final_video": {
            "path": str(FINAL_VIDEO).replace("\\", "/"),
            "sha256": video_sha,
            "duration": fd["runtime_seconds"],
            "duration_mmss": fd["runtime_mmss"],
        },
        "acceptance": {"path": rel(ACCEPTANCE), "sha256": acc_sha, "status": "PASS"},
        "thumbnail": {"path": rel(THUMB), "sha256": thumb_sha, "selected": "B / DREAM OR CRIME?"},
        "youtube_meta": {"path": rel(meta), "sha256": meta_sha, "title": TITLE, "privacy_status_target": "private"},
        "captions": {"path": rel(CAPTIONS), "sha256": captions_sha, "burned_in": True},
        "rights_manifest": {"path": rel(rights), "sha256": rights_sha, "status": "R3_review_required"},
        "final_delivery": {"path": rel(final_delivery), "sha256": fd_sha},
        "approval_needed": [
            "APR-0002 first/final review approval for exact final video hash",
            "APR-0003 title and thumbnail approval",
            "APR-0004 final ElevenLabs narration release approval",
            "APR-0005 dedicated R3 legal/rights review",
            "APR-0006 upload/publish/schedule approval",
        ],
    }
    owner_json = PKG / "OWNER_REVIEW_REQUEST.v006.json"
    write_json(owner_json, owner)
    owner_md = PKG / "OWNER_REVIEW_REQUEST.v006.md"
    owner_md.write_text(
        "# OWNER_REVIEW_REQUEST v006 - Theranos Final Candidate\n\n"
        f"- Final video: `{str(FINAL_VIDEO).replace(chr(92), '/')}`\n"
        f"- SHA-256: `{video_sha}`\n"
        f"- Runtime: `{fd['runtime_seconds']}s` (`{fd['runtime_mmss']}`)\n"
        f"- Acceptance: PASS (`{rel(ACCEPTANCE)}`)\n"
        f"- Title: `{TITLE}`\n"
        f"- Thumbnail: `{rel(THUMB)}` / `{thumb_sha}`\n\n"
        "Required approvals before any upload/publish/schedule: APR-0002, APR-0003, APR-0004, APR-0005, APR-0006.\n",
        encoding="utf-8",
    )

    approval = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v006",
        "created_at": now(),
        "status": "drafts_only_not_approved",
        "important": "These are approval drafts only. They do not authorize upload, schedule, public release, paid API use, or publication.",
        "external_side_effects": {"paid_api": False, "upload": False, "publish": False, "schedule": False},
        "drafts": [
            {"draft_id": "APR-0002-DRAFT", "gate": "final_review_video", "decision": "pending_owner_decision", "target_revision": "v006", "video": str(FINAL_VIDEO).replace("\\", "/"), "video_sha256": video_sha, "owner_review_request": rel(owner_json), "owner_review_request_sha256": sha256(owner_json)},
            {"draft_id": "APR-0003-DRAFT", "gate": "title_thumbnail", "decision": "pending_owner_decision", "target_revision": "v006", "title": TITLE, "thumbnail": rel(THUMB), "thumbnail_sha256": thumb_sha, "youtube_meta": rel(meta), "youtube_meta_sha256": meta_sha},
            {"draft_id": "APR-0004-DRAFT", "gate": "final_narration_release", "decision": "pending_owner_decision", "target_revision": "v006", "narration_index": rel(NARR_INDEX), "audio_mix": rel(AUDIO_MIX), "provider": "ElevenLabs"},
            {"draft_id": "APR-0005-DRAFT", "gate": "legal_rights", "decision": "pending_owner_or_legal_decision", "target_revision": "v006", "legal_rights_review_packet": rel(legal_json), "legal_rights_review_packet_sha256": sha256(legal_json), "rights_manifest": rel(rights), "rights_manifest_sha256": rights_sha},
            {"draft_id": "APR-0006-DRAFT", "gate": "publish_schedule", "decision": "pending_owner_decision", "target_revision": "v006", "video": str(FINAL_VIDEO).replace("\\", "/"), "video_sha256": video_sha, "final_delivery": rel(final_delivery), "final_delivery_sha256": fd_sha, "youtube_meta": rel(meta), "youtube_meta_sha256": meta_sha, "rights_manifest": rel(rights), "rights_manifest_sha256": rights_sha},
        ],
    }
    approval_json = PKG / "approval_drafts.v006.json"
    write_json(approval_json, approval)
    (PKG / "approval_drafts.v006.md").write_text(
        "# Theranos Approval Drafts v006\n\n"
        "Drafts only. No upload, schedule, public release, or paid API use is authorized.\n\n"
        f"- APR-0002: final video `{video_sha}`\n"
        f"- APR-0003: title/thumbnail `{thumb_sha}`\n"
        "- APR-0004: final ElevenLabs narration release\n"
        f"- APR-0005: R3 legal/rights packet `{sha256(legal_json)}`\n"
        f"- APR-0006: publish/schedule for final_delivery `{fd_sha}`\n",
        encoding="utf-8",
    )
    return owner_json, legal_json, approval_json


def update_manifest(files: dict[str, Path], video_sha: str) -> None:
    manifest = load_json(MANIFEST)
    manifest["state"] = "owner_review_required"
    active = manifest.setdefault("active_revisions", {})
    active.update(
        {
            "captions_final": "v001",
            "audio_mix": "v001",
            "final_acceptance": "v005",
            "youtube_meta": "v006",
            "rights_manifest": "v006",
            "final_delivery": "v006",
            "owner_review_request": "v006",
            "approval_drafts": "v006",
            "legal_rights_review_packet": "v006",
            "chapters": "v006",
            "tags": "v006",
            "title": "v006",
        }
    )
    artifacts = manifest.setdefault("artifacts", [])
    def add_artifact(kind: str, revision: str, path: Path, status: str = "candidate", qc: str = "pass") -> None:
        artifacts.append(
            {
                "artifact_id": f"{EP}-{kind}-{revision}",
                "artifact_type": kind,
                "revision": revision,
                "uri": f"artifact://{rel(path)}" if path.is_relative_to(ROOT) else str(path).replace("\\", "/"),
                "checksum": sha256(path),
                "status": status,
                "rights_status": "conditional",
                "qc_status": qc,
            }
        )
    add_artifact("final_delivery", "v006", files["final_delivery"])
    add_artifact("youtube_metadata", "v006", files["youtube_meta"])
    add_artifact("rights_manifest", "v006", files["rights_manifest"])
    add_artifact("owner_review_request", "v006", files["owner_review_request"])
    add_artifact("approval_drafts", "v006", files["approval_drafts"])
    add_artifact("legal_rights_review_packet", "v006", files["legal_packet"])
    add_artifact("final_acceptance", "v005", ACCEPTANCE)
    manifest["updated_at"] = now()
    manifest["warnings"] = [
        warning
        for warning in manifest.get("warnings", [])
        if "Current review_proxy v006 is 624.96s" not in warning
    ]
    manifest.setdefault("warnings", []).append(
        f"Final candidate v006 rendered and independently accepted: {str(FINAL_VIDEO).replace(chr(92), '/')} sha256={video_sha}; public release remains blocked by APR-0002..APR-0006 including R3 legal review."
    )
    write_json(MANIFEST, manifest)


def append_event(video_sha: str, fd: Path) -> None:
    event = {
        "ts": now(),
        "episode_id": EP,
        "stage": "final_package",
        "event": "final_candidate_v006_packaged_owner_stop",
        "revision": "v006",
        "actor": "codex",
        "video": str(FINAL_VIDEO).replace("\\", "/"),
        "video_sha256": video_sha,
        "final_delivery": rel(fd),
        "acceptance": rel(ACCEPTANCE),
        "note": "Theranos final candidate packaged after independent acceptance PASS. No upload, schedule, publish, or paid API action performed. STOP for owner approvals APR-0002..APR-0006 and R3 legal review.",
    }
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    if not FINAL_VIDEO.exists():
        raise FileNotFoundError(FINAL_VIDEO)
    acc = load_json(ACCEPTANCE)
    if acc.get("status") != "PASS":
        raise RuntimeError("Acceptance JSON is not PASS")
    video_sha = sha256(FINAL_VIDEO)
    captions_sha = sha256(CAPTIONS)
    thumb_sha = sha256(THUMB)
    probe = ffprobe(FINAL_VIDEO)
    duration = float(probe["format"]["duration"])
    rights = write_rights_manifest(video_sha, captions_sha, thumb_sha, duration)
    meta = write_youtube_meta(video_sha, captions_sha, thumb_sha)
    final_delivery = write_final_delivery(video_sha, captions_sha, thumb_sha, probe, rights, meta)
    owner, legal, approval = write_review_packets(video_sha, captions_sha, thumb_sha, final_delivery, rights, meta)
    files = {
        "rights_manifest": rights,
        "youtube_meta": meta,
        "final_delivery": final_delivery,
        "owner_review_request": owner,
        "legal_packet": legal,
        "approval_drafts": approval,
    }
    update_manifest(files, video_sha)
    append_event(video_sha, final_delivery)
    print(json.dumps({"status": "OK", "video_sha256": video_sha, "final_delivery": rel(final_delivery)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



