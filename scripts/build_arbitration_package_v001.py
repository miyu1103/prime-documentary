from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-012-arbitration"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
QC = EPDIR / "08_edit" / "renders" / "final.v001.qc.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v001.srt"
THUMB_META = PKG / "title_thumbnail_candidates.v001.json"
THUMB = PKG / "thumbnail.selected.v001.png"
VIDEO = Path(r"H:\pd-media\episodes\PD-2026-012-arbitration\08_edit\arbitration_premium_v001.mp4")
SCHEDULE_LOCAL = "2026-06-27T12:00:00+09:00"
SCHEDULE_UTC = "2026-06-27T03:00:00Z"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def main() -> int:
    now = datetime.now(timezone.utc).isoformat()
    PKG.mkdir(parents=True, exist_ok=True)
    qc = json.loads(QC.read_text("utf-8"))
    thumb_meta = json.loads(THUMB_META.read_text("utf-8"))
    title_a = "You Gave Up Your Right to Sue — By Tapping 'I Agree'"
    title_b = "The Fine Print That Quietly Took Your Right to Sue"
    title_c = "Why You Probably Can't Sue Your Bank, Phone, or Boss"
    selected_title = title_b
    chapters = [
        ("0:00", "You tap I agree"),
        ("0:32", "Prime Documentary opening"),
        ("0:36", "The arbitration clause"),
        ("1:20", "The thirty-dollar case"),
        ("3:50", "The 1925 law and the waiver"),
        ("5:40", "Critics and defenders"),
        ("6:35", "2011: Concepcion"),
        ("8:05", "Epic Systems and work"),
        ("9:20", "What mandatory arbitration means now"),
        ("10:45", "The rights you can sign away"),
        ("11:50", "Next: DNA after arrest"),
    ]
    description = (
        "You tap \"I agree\" all the time. Buried in that fine print can be a clause that changes where disputes are heard, "
        "whether claims can be joined together, and what happens to small harms that are too expensive to fight alone.\n\n"
        "This episode explains AT&T Mobility v. Concepcion (2011), the Federal Arbitration Act, class-action waivers, and the later workplace extension in Epic Systems v. Lewis (2018). "
        "It treats the debate neutrally: critics' concern about what they call forced arbitration, and defenders' argument that arbitration can be faster, cheaper, and grounded in agreements.\n\n"
        "Chapters\n"
        + "\n".join(f"{t} {label}" for t, label in chapters)
        + "\n\nSources\n"
        "AT&T Mobility LLC v. Concepcion, 563 U.S. 333 (2011).\n"
        "Epic Systems Corp. v. Lewis, 584 U.S. 497 (2018).\n"
        "Federal Arbitration Act, 9 U.S.C. §§ 1-16.\n\n"
        "About this video\n"
        "Independent educational documentary. Narration is AI-generated with the channel voice. Visuals are symbolic reconstructions and rights-cleared/AI-assisted illustrative assets, not authentic footage or evidence. This is not legal advice.\n\n"
        "Previous: Mahanoy and off-campus student speech.\n"
        "Next: DNA after arrest.\n"
        "Subscribe for the hidden systems behind everyday life.\n\n"
        "#SupremeCourt #Arbitration #ClassAction #ConsumerRights"
    )
    tags = ["Supreme Court", "arbitration", "mandatory arbitration", "pre-dispute arbitration", "arbitration debate", "class action waiver", "AT&T Mobility v Concepcion", "Epic Systems v Lewis", "Federal Arbitration Act", "consumer rights", "employment law", "legal documentary", "Prime Documentary"]
    video_sha = sha256(VIDEO)
    thumb_sha = sha256(THUMB)
    files = {
        "title.v001.txt": selected_title + "\n",
        "description.v001.txt": description + "\n",
        "chapters.v001.json": json.dumps({"episode_id": EP, "revision": "v001", "chapters": [{"time": t, "title": label} for t, label in chapters]}, indent=2, ensure_ascii=False) + "\n",
        "tags.v001.json": json.dumps({"episode_id": EP, "revision": "v001", "tags": tags}, indent=2, ensure_ascii=False) + "\n",
    }
    for name, text in files.items():
        (PKG / name).write_text(text, encoding="utf-8")
    rights = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "generated_at": now,
        "status": "clear_for_owner_review_upload_preparation",
        "commercial_use": "allowed",
        "publication_gate": "closed_owner_must_upload_or_approve",
        "assertions": {
            "script_claims_unchanged": True,
            "claims_ledger_unchanged": True,
            "no_real_person_likeness": True,
            "no_judge_likeness_or_portraits": True,
            "ai_visuals_symbolic_not_evidence": True,
            "stock_visuals_symbolic_not_case_footage": True,
            "critics_forced_arbitration_term_attributed": True,
            "critics_defenders_balanced": True,
            "commercial_ok_assets_only": True,
            "elevenlabs_tts_owner_approved": True,
            "external_upload_not_performed": True,
        },
        "assets": [
            {"type": "final_render", "file": str(VIDEO).replace("\\", "/"), "sha256": video_sha},
            {"type": "narration", "provider": "ElevenLabs", "voice_id": "nPczCjzI2devNBz1zQrb", "model_id": "eleven_multilingual_v2", "license": "Paid TTS generated under owner approval for commercial channel use"},
            {"type": "thumbnail_selected", "file": rel(THUMB), "sha256": thumb_sha},
            {"type": "captions", "file": rel(CAPTIONS), "sha256": sha256(CAPTIONS)},
            {"type": "thumbnail_candidates", "file": rel(THUMB_META), "sha256": sha256(THUMB_META)},
        ],
    }
    (PKG / "rights_manifest.v001.json").write_text(json.dumps(rights, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    youtube_meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "status": "upload_ready_owner_stop",
        "title": selected_title,
        "title_candidates": {"A": title_a, "B": title_b, "C": title_c, "selected": "B"},
        "description_file": rel(PKG / "description.v001.txt"),
        "description": description,
        "tags": tags,
        "category_id": "27",
        "default_language": "en",
        "default_audio_language": "en",
        "made_for_kids": False,
        "contains_synthetic_media": True,
        "privacy": "private",
        "intended_schedule_local": SCHEDULE_LOCAL,
        "intended_schedule_utc": SCHEDULE_UTC,
        "publishAt": SCHEDULE_UTC,
        "publish_gate": "closed_owner_must_confirm_after_video_review",
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
        "video_actual_path": str(VIDEO),
        "video_sha256": video_sha,
        "thumbnail_file": rel(THUMB),
        "thumbnail_sha256": thumb_sha,
        "captions_sidecar": rel(CAPTIONS),
        "rights_manifest": rel(PKG / "rights_manifest.v001.json"),
        "final_qc": rel(QC),
        "thumbnail_candidates": rel(THUMB_META),
        "created_at": now,
    }
    (PKG / "youtube_meta.v001.json").write_text(json.dumps(youtube_meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    final_delivery = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "generated_at": now,
        "status": "upload_ready_owner_stop",
        "render": {"file": str(VIDEO), "sha256": video_sha, "duration_seconds": qc["duration_seconds"], "qc": rel(QC)},
        "thumbnail": thumb_meta,
        "youtube": {"meta": rel(PKG / "youtube_meta.v001.json"), "privacy": "private", "scheduled_at_local": SCHEDULE_LOCAL, "scheduled_at_utc": SCHEDULE_UTC, "upload_performed": False},
        "rights": rel(PKG / "rights_manifest.v001.json"),
        "captions": rel(CAPTIONS),
    }
    (PKG / "final_delivery.v001.json").write_text(json.dumps(final_delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest = json.loads((EPDIR / "manifest.json").read_text("utf-8"))
    manifest["state"] = "package_ready"
    manifest["updated_at"] = now
    manifest.setdefault("active_revisions", {}).update({"audio_mix": "v001", "captions": "v001", "final_qc": "v001", "thumbnail_candidates": "v001", "youtube_meta": "v001", "rights_manifest": "v001", "final_delivery": "v001"})
    note = f"Arbitration v001 package prepared for owner review. Upload/schedule is stopped before YouTube; target schedule {SCHEDULE_LOCAL} / {SCHEDULE_UTC}."
    if note not in manifest.setdefault("warnings", []):
        manifest["warnings"].append(note)
    (EPDIR / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (EPDIR / "events" / "events.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"event": "package_ready_owner_stop", "episode_id": EP, "revision": "v001", "video": str(VIDEO), "youtube_meta": rel(PKG / "youtube_meta.v001.json"), "ts": now}, ensure_ascii=False) + "\n")
    print(f"OK package v001 video={VIDEO} sha={video_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
