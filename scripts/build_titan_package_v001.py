#!/usr/bin/env python3
"""Build Titan first-cut review package.

Creates local package sidecars only. It does not upload, publish, schedule, or
change channel settings.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-016-titan"
EPDIR = ROOT / "episodes" / EP
MANIFEST = EPDIR / "manifest.json"
PACKAGE = EPDIR / "09_package"
RENDERS = EPDIR / "08_edit" / "renders"
ROUGH = ROOT / "remotion" / "src" / "data" / "titan_roughcut.ts"
CAPTIONS_DATA = ROOT / "remotion" / "src" / "data" / "titan_captions.ts"
FINAL = Path("H:/pd-media/episodes/PD-2026-016-titan/07_edit/v001.mp4")
QC = RENDERS / "final.v001.qc.json"
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


def chapters() -> list[dict]:
    data = parse_roughcut()
    starts: dict[str, float] = {}
    cursor = 0.0
    for shot in data["shots"]:
        starts.setdefault(shot["chapterId"], cursor)
        cursor += float(shot["seconds"])
        if shot["spanId"] == "SPN-0005":
            cursor += 3.5
    labels = [
        ("cold_open", "Hook: the sound"),
        ("the_dream", "Opening: the dream"),
        ("the_warnings", "The warnings"),
        ("the_dive", "The dive"),
        ("the_search", "The search"),
        ("the_truth", "The truth"),
        ("coda", "Coda: what remains"),
    ]
    return [{"time": ts(starts[key]), "seconds": round(starts[key], 3), "title": title} for key, title in labels]


def active_caption_sidecars(manifest: dict) -> tuple[str, Path, Path, Path]:
    active = manifest.get("active_revisions", {})
    rev = active.get("captions") or active.get("captions_srt") or "v001"
    return (
        rev,
        EPDIR / "08_edit" / f"captions.{rev}.srt",
        EPDIR / "08_edit" / f"captions.{rev}.json",
        EPDIR / "08_edit" / f"captions.{rev}.qc.json",
    )


def description(chapter_rows: list[dict]) -> str:
    ch = "\n".join(f"{row['time']} {row['title']}" for row in chapter_rows)
    return f"""A one-hour Prime Documentary feature on the Titan submersible disaster: the dream sold to passengers, the warnings around the carbon-fiber hull, the final dive, the search, and the official conclusion that the loss was preventable.

This is an educational documentary. Visuals are symbolic reconstructions, stock atmosphere, documents, and motion graphics. They are not authentic footage of the incident, do not depict the real passengers or crew, and do not show the implosion or remains.

Chapters:
{ch}

Review gates remain closed: first-cut review, title/thumbnail approval, same-day pre-publish fact re-check, and public scheduling approval are still required before any upload or publication."""


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    caption_rev, captions_srt, captions_json, captions_qc = active_caption_sidecars(manifest)
    for path in [FINAL, QC, captions_srt, captions_json, captions_qc, CAPTIONS_DATA, THUMB_META, THUMB]:
        if not path.exists():
            raise FileNotFoundError(path)
    PACKAGE.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    qc = json.loads(QC.read_text(encoding="utf-8"))
    caption_qc = json.loads(captions_qc.read_text(encoding="utf-8"))
    if caption_qc.get("qc_status") != "pass" or caption_qc.get("text_exact_match_to_script") is not True:
        raise RuntimeError(f"Caption QC is not safe for packaging: {captions_qc}")
    thumb_meta = json.loads(THUMB_META.read_text(encoding="utf-8"))
    chapter_rows = chapters()
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

    (PACKAGE / "title.v001.txt").write_text(title + "\n", encoding="utf-8")
    (PACKAGE / "description.v001.md").write_text(desc + "\n", encoding="utf-8")
    write_json(PACKAGE / "chapters.v001.json", chapter_rows)
    write_json(PACKAGE / "tags.v001.json", tags)

    youtube_meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
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
        "captions_revision": caption_rev,
        "captions_sidecar": rel(captions_srt),
        "captions_qc": rel(captions_qc),
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
    write_json(PACKAGE / "youtube_meta.v001.json", youtube_meta)

    rights = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
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
            {"asset_id": f"{EP}-final-render-v001", "type": "final_render", "file": str(FINAL).replace("\\", "/"), "sha256": sha256(FINAL), "rights_status": "conditional"},
            {"asset_id": f"{EP}-thumbnail-v002", "type": "thumbnail_selected", "file": rel(THUMB), "sha256": sha256(THUMB), "rights_status": "conditional"},
            {"asset_id": f"{EP}-captions-{caption_rev}", "type": "captions", "file": rel(captions_srt), "sha256": sha256(captions_srt), "rights_status": "clear"},
        ],
        "notes": [
            "No real-person likeness or deepfake is intentionally used.",
            "No brand marks are intentionally used in generated visuals.",
            "Implosion beat is black plus silence; no graphic depiction is used.",
            "Final same-day pre-publish fact re-check is still required before public scheduling.",
        ],
    }
    write_json(PACKAGE / "rights_manifest.v001.json", rights)

    delivery = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "generated_at": now,
        "status": "first_cut_review_ready",
        "video": str(FINAL).replace("\\", "/"),
        "video_sha256": sha256(FINAL),
        "duration_seconds": qc["duration_seconds"],
        "runtime_band_pass": qc["runtime_band_pass"],
        "thumbnail": rel(THUMB),
        "thumbnail_sha256": sha256(THUMB),
        "captions_revision": caption_rev,
        "captions": rel(captions_srt),
        "captions_qc": rel(captions_qc),
        "youtube_meta": rel(PACKAGE / "youtube_meta.v001.json"),
        "rights_manifest": rel(PACKAGE / "rights_manifest.v001.json"),
        "owner_review_request": rel(PACKAGE / "OWNER_REVIEW_REQUEST.v001.md"),
        "external_side_effects": {"upload": False, "publish": False, "schedule": False},
    }
    write_json(PACKAGE / "final_delivery.v001.json", delivery)

    review = f"""# OWNER REVIEW REQUEST v001 — Titan First Cut

Episode: {EP}
Active script revision: v001
Video: `{delivery['video']}`
SHA256: `{delivery['video_sha256']}`
Runtime: {qc['duration_seconds']:.3f}s
Runtime band pass: {qc['runtime_band_pass']}

## Review Focus
- Story structure: hook -> opening -> warnings/dive/search/truth -> coda.
- Audio: ElevenLabs narration, BGM, ambience, SFX, and the implosion silence beat.
- Captions: burned-in captions use {caption_rev}, forced-aligned to the master narration audio, with exact text match to the approved v001 narration text.
- Dignity/rights: no real-person likeness, no brand marks intended, no graphic implosion/remains.
- Thumbnail/title: v002 selected for CTR review: `{title}` / `THEY WERE WARNED`.

## Gates Still Closed
- No upload, publish, schedule, or channel setting change has been performed.
- Title/thumbnail approval is still required.
- Same-day pre-publish fact re-check is still required before public scheduling.
"""
    (PACKAGE / "OWNER_REVIEW_REQUEST.v001.md").write_text(review, encoding="utf-8")

    active = manifest.setdefault("active_revisions", {})
    active["thumbnail_candidates"] = "v002"
    active["thumbnail"] = "v002"
    active["captions"] = caption_rev
    active["captions_srt"] = caption_rev
    active["captions_json"] = caption_rev
    active["titan_captions"] = caption_rev
    active["youtube_meta"] = "v001"
    active["rights_manifest"] = "v001"
    active["final_delivery"] = "v001"
    active["owner_review_request"] = "v001"
    manifest["state"] = "package_ready"
    artifacts = manifest.setdefault("artifacts", [])
    new_artifacts = [
        ("PD-2026-016-titan-thumbnail-selected-v002", "thumbnail_selected", "v002", "artifact://episodes/PD-2026-016-titan/09_package/thumbnail.selected.v002.png", sha256(THUMB), "candidate", "conditional", "pass"),
        ("PD-2026-016-titan-title-thumbnail-candidates-v002", "title_thumbnail_candidates", "v002", "artifact://episodes/PD-2026-016-titan/09_package/title_thumbnail_candidates.v002.json", sha256(THUMB_META), "candidate", "conditional", "pass"),
        ("PD-2026-016-titan-youtube-meta", "youtube_meta", "v001", "artifact://episodes/PD-2026-016-titan/09_package/youtube_meta.v001.json", sha256(PACKAGE / "youtube_meta.v001.json"), "candidate", "conditional", "pass"),
        ("PD-2026-016-titan-rights-manifest", "rights_manifest", "v001", "artifact://episodes/PD-2026-016-titan/09_package/rights_manifest.v001.json", sha256(PACKAGE / "rights_manifest.v001.json"), "candidate", "conditional", "pass"),
        ("PD-2026-016-titan-final-delivery", "final_delivery", "v001", "artifact://episodes/PD-2026-016-titan/09_package/final_delivery.v001.json", sha256(PACKAGE / "final_delivery.v001.json"), "candidate", "conditional", "pass"),
        ("PD-2026-016-titan-owner-review-request", "owner_review_request", "v001", "artifact://episodes/PD-2026-016-titan/09_package/OWNER_REVIEW_REQUEST.v001.md", sha256(PACKAGE / "OWNER_REVIEW_REQUEST.v001.md"), "candidate", "conditional", "pass"),
        (f"PD-2026-016-titan-captions-{caption_rev}", "captions", caption_rev, f"artifact://episodes/PD-2026-016-titan/08_edit/captions.{caption_rev}.srt", sha256(captions_srt), "candidate", "clear", "pass"),
        (f"PD-2026-016-titan-captions-json-{caption_rev}", "captions_json", caption_rev, f"artifact://episodes/PD-2026-016-titan/08_edit/captions.{caption_rev}.json", sha256(captions_json), "candidate", "clear", "pass"),
        (f"PD-2026-016-titan-captions-qc-{caption_rev}", "caption_qc", caption_rev, f"artifact://episodes/PD-2026-016-titan/08_edit/captions.{caption_rev}.qc.json", sha256(captions_qc), "candidate", "clear", "pass"),
        (f"PD-2026-016-titan-captions-remotion-data-{caption_rev}", "captions_data", caption_rev, "artifact://remotion/src/data/titan_captions.ts", sha256(CAPTIONS_DATA), "candidate", "clear", "pass"),
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
        "revision": "v001",
        "actor": "codex",
        "note": f"Built first-cut package sidecars and v002 CTR thumbnail using captions {caption_rev}. No upload/publish/schedule.",
    }
    events = EPDIR / "events" / "events.jsonl"
    with events.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(json.dumps({"delivery": rel(PACKAGE / "final_delivery.v001.json"), "video": delivery["video"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
