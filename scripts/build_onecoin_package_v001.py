#!/usr/bin/env python3
"""Build OneCoin first-cut review package.

Creates local package sidecars only. It does not upload, publish, schedule, or
change channel settings.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-017-onecoin"
EPDIR = ROOT / "episodes" / EP
PACKAGE = EPDIR / "09_package"
THUMBS = EPDIR / "10_thumbnail"
RENDERS = EPDIR / "08_edit" / "renders"
ROUGH = ROOT / "remotion" / "src" / "data" / "onecoin_roughcut.ts"
FINAL = Path("H:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v001.mp4")
QC = RENDERS / "final.v001.qc.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v001.srt"
AUDIO_QC = EPDIR / "08_edit" / "audio_mix.v001.qc.json"
SELECTED_THUMB = PACKAGE / "thumbnail.selected.v001.png"


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
    m = re.search(r"export const ONECOIN_ROUGHCUT: RoughCutData = (\{.*\});", text, re.S)
    if not m:
        raise RuntimeError("Could not parse onecoin_roughcut.ts")
    return json.loads(m.group(1))


def ts(t: float) -> str:
    m = int(t // 60)
    s = int(t % 60)
    return f"{m:02d}:{s:02d}"


def chapters() -> list[dict]:
    audio = json.loads(AUDIO_QC.read_text(encoding="utf-8"))
    bounds = audio["chapter_bounds"]
    labels = [
        ("cold_open", "Cold open: nothing"),
        ("the_promise", "The promise"),
        ("the_crack", "The crack"),
        ("the_void", "The void"),
        ("coda", "Coda: still missing"),
    ]
    return [{"time": ts(bounds[key][0]), "seconds": round(bounds[key][0], 3), "title": title} for key, title in labels]


def build_thumbnail_candidates() -> dict:
    PACKAGE.mkdir(parents=True, exist_ok=True)
    selected = THUMBS / "thumbnail.onecoin_option_A.v001.png"
    if not selected.exists():
        raise FileNotFoundError(selected)
    shutil.copy2(selected, SELECTED_THUMB)
    options = [
        {
            "id": "A",
            "thumbnail_text": "THERE WAS NO COIN",
            "file": rel(THUMBS / "thumbnail.onecoin_option_A.v001.png"),
            "role": "selected_review_candidate",
            "rationale": "Most direct promise of the film; no real-person likeness.",
        },
        {
            "id": "B",
            "thumbnail_text": "SHE VANISHED",
            "file": rel(THUMBS / "thumbnail.onecoin_option_B.v001.png"),
            "role": "alternate",
            "rationale": "Strong mystery angle, still avoids a real face.",
        },
        {
            "id": "C",
            "thumbnail_text": "$4 BILLION. GONE.",
            "file": rel(THUMBS / "thumbnail.onecoin_option_C.v001.png"),
            "role": "alternate",
            "rationale": "High-stakes money angle with symbolic ledger background.",
        },
    ]
    data = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "status": "owner_review_required_not_approved",
        "selected_option": "A",
        "selected_thumbnail": rel(SELECTED_THUMB),
        "selected_thumbnail_sha256": sha256(SELECTED_THUMB),
        "selected_youtube_title": "There Was No Coin: The $4 Billion OneCoin Story",
        "options": options,
        "guardrails": [
            "No real-person likeness.",
            "No OneCoin brand mark.",
            "No 'guilty' or 'convicted' language for Ruja Ignatova.",
            "Manual owner approval required before upload.",
        ],
    }
    write_json(PACKAGE / "title_thumbnail_candidates.v001.json", data)
    return data


def description(chapter_rows: list[dict]) -> str:
    ch = "\n".join(f"{row['time']} {row['title']}" for row in chapter_rows)
    return f"""A Prime Documentary mid-feature about OneCoin, Ruja Ignatova, and the promise of a cryptocurrency that prosecutors say did not exist as a real blockchain.

Ruja Ignatova is charged and wanted, not convicted. This film uses indictment/public-record language for allegations involving her. Convicted associates are described according to public court outcomes.

Visuals are symbolic reconstructions, project-generated AI stills, stock/factory atmosphere, and Remotion motion graphics. They do not depict real-person likenesses, do not use the OneCoin logo, and do not show private victim imagery.

Chapters:
{ch}

Review gates remain closed: ElevenLabs master narration, first-cut review, title/thumbnail approval, same-day legal/fact re-check, and public scheduling approval are still required before any upload or publication."""


def main() -> int:
    for path in [FINAL, QC, CAPTIONS, AUDIO_QC]:
        if not path.exists():
            raise FileNotFoundError(path)
    PACKAGE.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    qc = json.loads(QC.read_text(encoding="utf-8"))
    thumb_meta = build_thumbnail_candidates()
    chapter_rows = chapters()
    title = thumb_meta["selected_youtube_title"]
    desc = description(chapter_rows)
    tags = [
        "OneCoin",
        "Ruja Ignatova",
        "Missing Cryptoqueen",
        "Cryptoqueen",
        "crypto documentary",
        "cryptocurrency fraud",
        "financial crime documentary",
        "FBI most wanted",
        "Prime Documentary",
        "documentary",
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
        "working_title": "Nothing — The Woman Who Sold a Coin That Did Not Exist",
        "description": desc,
        "chapters": chapter_rows,
        "tags": tags,
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
        "video_actual_path": str(FINAL).replace("\\", "/"),
        "video_sha256": sha256(FINAL),
        "thumbnail": rel(SELECTED_THUMB),
        "thumbnail_sha256": sha256(SELECTED_THUMB),
        "captions_sidecar": rel(CAPTIONS),
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
            "ai_symbolic_reconstruction": True,
            "stock_factory_broll_used": True,
            "on_screen_synthetic_label_present": True,
            "pre_publish_legal_review_required": True,
            "same_day_fact_recheck_required": True,
            "voice_master_pending": True,
        },
        "assets": [
            {"asset_id": f"{EP}-final-render-v001", "type": "final_render", "file": str(FINAL).replace("\\", "/"), "sha256": sha256(FINAL), "rights_status": "conditional"},
            {"asset_id": f"{EP}-thumbnail-selected-v001", "type": "thumbnail_selected", "file": rel(SELECTED_THUMB), "sha256": sha256(SELECTED_THUMB), "rights_status": "conditional"},
            {"asset_id": f"{EP}-captions-v001", "type": "captions", "file": rel(CAPTIONS), "sha256": sha256(CAPTIONS), "rights_status": "clear"},
            {"asset_id": f"{EP}-factory-ledger-v001", "type": "factory_ledger", "file": rel(EPDIR / "05_stock" / "factory_ledger.v001.json"), "sha256": sha256(EPDIR / "05_stock" / "factory_ledger.v001.json"), "rights_status": "clear"},
        ],
        "notes": [
            "No real-person likeness or deepfake is intentionally used.",
            "No OneCoin logo or brand mark is intentionally used.",
            "Ruja Ignatova is described as charged/wanted/alleged, not convicted.",
            "The silence/void beat is black plus silence.",
            "Final same-day legal and fact re-check is still required before public scheduling.",
        ],
    }
    write_json(PACKAGE / "rights_manifest.v001.json", rights)

    delivery = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "generated_at": now,
        "status": "first_cut_review_ready_voice_draft",
        "final_video": str(FINAL).replace("\\", "/"),
        "video": str(FINAL).replace("\\", "/"),
        "video_sha256": sha256(FINAL),
        "duration_seconds": qc["duration_seconds"],
        "runtime_band_pass": qc["runtime_band_pass"],
        "thumbnail": rel(SELECTED_THUMB),
        "thumbnail_sha256": sha256(SELECTED_THUMB),
        "youtube_meta": rel(PACKAGE / "youtube_meta.v001.json"),
        "rights_manifest": rel(PACKAGE / "rights_manifest.v001.json"),
        "owner_review_request": rel(PACKAGE / "OWNER_REVIEW_REQUEST.v001.md"),
        "external_side_effects": {"upload": False, "publish": False, "schedule": False},
        "hard_stop": "ElevenLabs master narration remains blocked pending explicit owner GO.",
    }
    write_json(PACKAGE / "final_delivery.v001.json", delivery)

    review = f"""# OWNER REVIEW REQUEST v001 — OneCoin First Cut

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
- Thumbnail/title: selected review candidate is option A, `{title}` / `THERE WAS NO COIN`.

## Gates Still Closed
- No ElevenLabs paid call has been made.
- No upload, publish, schedule, or channel setting change has been performed.
- Title/thumbnail approval is still required.
- Same-day DOJ/FBI fact re-check and legal review are still required before public scheduling.
"""
    (PACKAGE / "OWNER_REVIEW_REQUEST.v001.md").write_text(review, encoding="utf-8")

    manifest_path = EPDIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    active = manifest.setdefault("active_revisions", {})
    active.update({
        "thumbnail_candidates": "v001",
        "thumbnail": "v001",
        "youtube_meta": "v001",
        "rights_manifest": "v001",
        "final_delivery": "v001",
        "owner_review_request": "v001",
    })
    manifest["state"] = "first_cut_packaged_voice_draft"
    artifacts = manifest.setdefault("artifacts", [])
    new_artifacts = [
        ("PD-2026-017-onecoin-thumbnail-selected-v001", "thumbnail_selected", "v001", "artifact://episodes/PD-2026-017-onecoin/09_package/thumbnail.selected.v001.png", sha256(SELECTED_THUMB), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-title-thumbnail-candidates-v001", "title_thumbnail_candidates", "v001", "artifact://episodes/PD-2026-017-onecoin/09_package/title_thumbnail_candidates.v001.json", sha256(PACKAGE / "title_thumbnail_candidates.v001.json"), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-youtube-meta", "youtube_meta", "v001", "artifact://episodes/PD-2026-017-onecoin/09_package/youtube_meta.v001.json", sha256(PACKAGE / "youtube_meta.v001.json"), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-rights-manifest", "rights_manifest", "v001", "artifact://episodes/PD-2026-017-onecoin/09_package/rights_manifest.v001.json", sha256(PACKAGE / "rights_manifest.v001.json"), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-final-delivery", "final_delivery", "v001", "artifact://episodes/PD-2026-017-onecoin/09_package/final_delivery.v001.json", sha256(PACKAGE / "final_delivery.v001.json"), "candidate", "conditional", "draft_voice"),
        ("PD-2026-017-onecoin-owner-review-request", "owner_review_request", "v001", "artifact://episodes/PD-2026-017-onecoin/09_package/OWNER_REVIEW_REQUEST.v001.md", sha256(PACKAGE / "OWNER_REVIEW_REQUEST.v001.md"), "candidate", "conditional", "pass"),
    ]
    ids = {a[0] for a in new_artifacts}
    artifacts[:] = [a for a in artifacts if a.get("artifact_id") not in ids]
    for aid, atype, rev, uri, checksum, status, rights_status, qc_status in new_artifacts:
        artifacts.append({"artifact_id": aid, "artifact_type": atype, "revision": rev, "uri": uri, "checksum": checksum, "status": status, "rights_status": rights_status, "qc_status": qc_status})
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    events = EPDIR / "events" / "events.jsonl"
    with events.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "episode_id": EP, "stage": "package", "event": "first_cut_package_built", "revision": "v001", "actor": "codex", "note": "Built OneCoin first-cut package sidecars. No upload/publish/schedule. Voice is local SAPI draft pending ElevenLabs owner GO."}, ensure_ascii=False) + "\n")

    print(json.dumps({"delivery": rel(PACKAGE / "final_delivery.v001.json"), "video": delivery["final_video"], "thumbnail": rel(SELECTED_THUMB)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
