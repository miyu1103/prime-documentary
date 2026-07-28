#!/usr/bin/env python3
"""Build Titan v003 review package sidecars.

No upload, publish, schedule, or channel setting change is performed.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-016-titan"
REV = "v003"
EPDIR = ROOT / "episodes" / EP
MANIFEST = EPDIR / "manifest.json"
PACKAGE = EPDIR / "09_package"
ROUGH = ROOT / "remotion" / "src" / "data" / "titan_roughcut.ts"
PLAN = EPDIR / "08_edit" / "renders" / "recut_plan.v002.json"
FINAL = Path("H:/pd-media/episodes/PD-2026-016-titan/07_edit/v003.mp4")
QC = EPDIR / "08_edit" / "renders" / "final.v003.qc.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v003.srt"
CAPTIONS_QC = EPDIR / "08_edit" / "captions.v003.qc.json"
THUMB_META = PACKAGE / "title_thumbnail_candidates.v002.json"
THUMB = PACKAGE / "thumbnail.selected.v002.png"


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


def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_roughcut() -> dict:
    text = ROUGH.read_text(encoding="utf-8")
    m = re.search(r"export const TITAN_ROUGHCUT: RoughCutData = (\{.*\});", text, re.S)
    if not m:
        raise RuntimeError("Could not parse titan_roughcut.ts")
    return json.loads(m.group(1))


def ts(t: float) -> str:
    m = int(t // 60)
    s = int(t % 60)
    return f"{m:02d}:{s:02d}"


def map_source_time(plan: dict, source_time: float) -> float:
    for item in plan["timeline"]:
        if item["type"] == "source" and item["source_start"] <= source_time <= item["source_end"]:
            return round(item["output_start"] + (source_time - item["source_start"]), 3)
    raise RuntimeError(f"Could not map source time {source_time}")


def chapters(plan: dict) -> list[dict]:
    data = parse_roughcut()
    starts: dict[str, float] = {}
    cursor = 0.0
    for shot in data["shots"]:
        starts.setdefault(shot["chapterId"], cursor)
        cursor += float(shot["seconds"])
        if shot["spanId"] == "SPN-0005":
            cursor += 3.5
    rows = [
        {"seconds": 0.0, "title": "Hook: the sound"},
        {"seconds": 9.8, "title": "Opening: Pure Waste"},
        {"seconds": map_source_time(plan, starts["the_dream"]), "title": "The dream"},
        {"seconds": map_source_time(plan, starts["the_warnings"]), "title": "The warnings"},
        {"seconds": map_source_time(plan, starts["the_dive"]), "title": "The dive"},
        {"seconds": map_source_time(plan, starts["the_search"]), "title": "The search"},
        {"seconds": map_source_time(plan, starts["the_truth"]), "title": "The truth"},
        {"seconds": map_source_time(plan, starts["coda"]), "title": "Ending: what remains"},
    ]
    return [{"time": ts(row["seconds"]), "seconds": row["seconds"], "title": row["title"]} for row in rows]


def description(chapter_rows: list[dict]) -> str:
    ch = "\n".join(f"{row['time']} {row['title']}" for row in chapter_rows)
    return f"""A Prime Documentary feature on the Titan submersible disaster: the dream sold to passengers, the warnings around the carbon-fiber hull, the final dive, the search, and the official conclusion that the loss was preventable.

This review cut uses a tighter structure: a short hook, a dedicated opening title, the main documentary body, and a restrained ending. Visuals are symbolic reconstructions, stock atmosphere, documents, and motion graphics. They are not authentic footage of the incident, do not depict the real passengers or crew, and do not show the implosion or remains.

Chapters:
{ch}

Review gates remain closed: first-cut review, title/thumbnail approval, same-day pre-publish fact re-check, and public scheduling approval are still required before any upload or publication."""


def main() -> int:
    for path in [FINAL, QC, CAPTIONS, CAPTIONS_QC, PLAN, THUMB_META, THUMB]:
        if not path.exists():
            raise FileNotFoundError(path)
    PACKAGE.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    qc = json.loads(QC.read_text(encoding="utf-8"))
    caption_qc = json.loads(CAPTIONS_QC.read_text(encoding="utf-8"))
    if caption_qc.get("qc_status") != "pass" or caption_qc.get("text_exact_match_to_script") is not True:
        raise RuntimeError("Caption QC is not pass")
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    thumb_meta = json.loads(THUMB_META.read_text(encoding="utf-8"))
    chapter_rows = chapters(plan)
    title = thumb_meta["selected_youtube_title"]
    desc = description(chapter_rows)
    tags = [
        "Titan submersible",
        "Titan disaster",
        "OceanGate Titan",
        "Titanic submersible",
        "deep sea documentary",
        "submersible disaster",
        "US Coast Guard report",
        "carbon fiber pressure hull",
        "Prime Documentary",
        "documentary feature",
    ]

    (PACKAGE / f"title.{REV}.txt").write_text(title + "\n", encoding="utf-8")
    (PACKAGE / f"description.{REV}.md").write_text(desc + "\n", encoding="utf-8")
    write_json(PACKAGE / f"chapters.{REV}.json", chapter_rows)
    write_json(PACKAGE / f"tags.{REV}.json", tags)

    youtube_meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": REV,
        "status": "first_cut_review_ready_not_uploaded",
        "title": title,
        "working_title": "Pure Waste — The Last Dive of the Titan",
        "description": desc,
        "chapters": chapter_rows,
        "tags": tags,
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
        "video_actual_path": str(FINAL).replace("\\", "/"),
        "video_sha256": sha256(FINAL),
        "thumbnail": rel(THUMB),
        "thumbnail_sha256": sha256(THUMB),
        "captions_revision": REV,
        "captions_sidecar": rel(CAPTIONS),
        "captions_qc": rel(CAPTIONS_QC),
        "synthetic_content_disclosure_required": True,
        "contains_ai_symbolic_reconstruction": True,
        "captions_burned_in": True,
        "privacy_status_target": "private_after_owner_upload_go",
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
        "publish_gate": "closed",
        "created_at": now,
    }
    write_json(PACKAGE / f"youtube_meta.{REV}.json", youtube_meta)

    rights = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": REV,
        "generated_at": now,
        "status": "conditional_first_cut_review",
        "summary": {
            "commercial_use_review_required": True,
            "real_person_likeness": False,
            "brand_marks_intended": False,
            "graphic_implosion_or_remains": False,
            "ai_symbolic_reconstruction": True,
            "stock_factory_broll_used": True,
            "on_screen_synthetic_label_present": True,
            "pre_publish_fact_recheck_required": True,
        },
        "assets": [
            {"asset_id": f"{EP}-final-render-{REV}", "type": "final_render", "file": str(FINAL).replace("\\", "/"), "sha256": sha256(FINAL), "rights_status": "conditional"},
            {"asset_id": f"{EP}-thumbnail-v002", "type": "thumbnail_selected", "file": rel(THUMB), "sha256": sha256(THUMB), "rights_status": "conditional"},
            {"asset_id": f"{EP}-captions-{REV}", "type": "captions", "file": rel(CAPTIONS), "sha256": sha256(CAPTIONS), "rights_status": "clear"},
        ],
        "notes": [
            "No real-person likeness or deepfake is intentionally used.",
            "No brand marks are intentionally used in generated visuals.",
            "Implosion beat is black plus silence; no graphic depiction is used.",
            "Final same-day pre-publish fact re-check is still required before public scheduling.",
        ],
    }
    write_json(PACKAGE / f"rights_manifest.{REV}.json", rights)

    delivery = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": REV,
        "generated_at": now,
        "status": "first_cut_review_ready",
        "video": str(FINAL).replace("\\", "/"),
        "video_sha256": sha256(FINAL),
        "duration_seconds": qc["duration_seconds"],
        "runtime_band_pass": qc["runtime_band_pass"],
        "thumbnail": rel(THUMB),
        "thumbnail_sha256": sha256(THUMB),
        "captions_revision": REV,
        "captions": rel(CAPTIONS),
        "captions_qc": rel(CAPTIONS_QC),
        "youtube_meta": rel(PACKAGE / f"youtube_meta.{REV}.json"),
        "rights_manifest": rel(PACKAGE / f"rights_manifest.{REV}.json"),
        "owner_review_request": rel(PACKAGE / f"OWNER_REVIEW_REQUEST.{REV}.md"),
        "external_side_effects": {"upload": False, "publish": False, "schedule": False},
    }
    write_json(PACKAGE / f"final_delivery.{REV}.json", delivery)

    review = f"""# OWNER REVIEW REQUEST {REV} — Titan Tight First Cut

Episode: {EP}
Active script revision: v001
Video: `{delivery['video']}`
SHA256: `{delivery['video_sha256']}`
Runtime: {qc['duration_seconds']:.3f}s
Runtime band pass: {qc['runtime_band_pass']}

## Review Focus
- Structure: ~10s hook -> dedicated opening title -> main body -> ending card.
- Pacing: long dialogue gaps capped at about 5s, with the deliberate opening and implosion silence preserved.
- Audio: ElevenLabs narration, BGM, ambience, SFX, and the implosion silence beat.
- Captions: v003 sidecar transformed from forced-aligned v002 captions; text exactly matches approved v001 narration.
- Dignity/rights: no real-person likeness, no brand marks intended, no graphic implosion/remains.
- Thumbnail/title: v002 selected for CTR review: `{title}` / `THEY WERE WARNED`.

## Gates Still Closed
- No upload, publish, schedule, or channel setting change has been performed.
- Title/thumbnail approval is still required.
- Same-day pre-publish fact re-check is still required before public scheduling.
"""
    (PACKAGE / f"OWNER_REVIEW_REQUEST.{REV}.md").write_text(review, encoding="utf-8")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    active = manifest.setdefault("active_revisions", {})
    active["final_delivery"] = REV
    active["youtube_meta"] = REV
    active["rights_manifest"] = REV
    active["owner_review_request"] = REV
    manifest["state"] = "package_ready"
    artifacts = manifest.setdefault("artifacts", [])
    new_artifacts = [
        (f"PD-2026-016-titan-youtube-meta-{REV}", "youtube_meta", REV, f"artifact://episodes/PD-2026-016-titan/09_package/youtube_meta.{REV}.json", sha256(PACKAGE / f"youtube_meta.{REV}.json"), "candidate", "conditional", "pass"),
        (f"PD-2026-016-titan-rights-manifest-{REV}", "rights_manifest", REV, f"artifact://episodes/PD-2026-016-titan/09_package/rights_manifest.{REV}.json", sha256(PACKAGE / f"rights_manifest.{REV}.json"), "candidate", "conditional", "pass"),
        (f"PD-2026-016-titan-final-delivery-{REV}", "final_delivery", REV, f"artifact://episodes/PD-2026-016-titan/09_package/final_delivery.{REV}.json", sha256(PACKAGE / f"final_delivery.{REV}.json"), "candidate", "conditional", "pass"),
        (f"PD-2026-016-titan-owner-review-request-{REV}", "owner_review_request", REV, f"artifact://episodes/PD-2026-016-titan/09_package/OWNER_REVIEW_REQUEST.{REV}.md", sha256(PACKAGE / f"OWNER_REVIEW_REQUEST.{REV}.md"), "candidate", "conditional", "pass"),
    ]
    ids = {a[0] for a in new_artifacts}
    artifacts[:] = [a for a in artifacts if a.get("artifact_id") not in ids]
    for aid, atype, rev, uri, checksum, status, rights_status, qc_status in new_artifacts:
        artifacts.append({"artifact_id": aid, "artifact_type": atype, "revision": rev, "uri": uri, "checksum": checksum, "status": status, "rights_status": rights_status, "qc_status": qc_status})
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "episode_id": EP,
        "stage": "package",
        "event": "first_cut_package_built",
        "revision": REV,
        "actor": "codex",
        "note": "Built v003 tight first-cut package. No upload/publish/schedule.",
    }
    with (EPDIR / "events" / "events.jsonl").open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(json.dumps({"delivery": rel(PACKAGE / f"final_delivery.{REV}.json"), "video": delivery["video"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
