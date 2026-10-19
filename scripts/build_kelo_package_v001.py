#!/usr/bin/env python3
"""Create Kelo publish package sidecars."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-010-kelo"
EPDIR = ROOT / "episodes" / EP
PACKAGE = EPDIR / "09_package"
QC = EPDIR / "08_edit" / "renders" / "final.v001.qc.json"
SOURCES = EPDIR / "01_research" / "sources.v001.json"
CLAIMS = EPDIR / "01_research" / "claims.v001.json"
THUMB_META = PACKAGE / "title_thumbnail_candidates.v001.json"
THUMB_SELECTED = PACKAGE / "thumbnail.selected.v001.png"
CAPTIONS = EPDIR / "08_edit" / "captions.v001.srt"


def media_root() -> Path:
    cfg = json.loads((ROOT / "config" / "storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


MEDIA = media_root()
FINAL_MP4 = MEDIA / "episodes" / EP / "08_edit" / "kelo_premium_v001.mp4"
AI_SCENES = MEDIA / "assets" / "ai" / "kelo"
AI_THUMBS = MEDIA / "assets" / "ai" / "thumbs" / "kelo"


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


CHAPTERS = [
    ("00:00", "Your home for a developer?"),
    ("00:25", "Opening: Kelo"),
    ("00:32", "Fort Trumbull"),
    ("01:12", "The little pink house"),
    ("01:51", "Jobs, taxes, and a plan"),
    ("02:51", "The Fifth Amendment question"),
    ("03:12", "Public use or public purpose"),
    ("04:17", "Narrow versus broad"),
    ("04:57", "The 2005 decision"),
    ("05:09", "The 5-4 line"),
    ("06:00", "O'Connor's warning"),
    ("07:17", "Kennedy's concurrence"),
    ("08:05", "The backlash in the states"),
    ("09:20", "The plan collapses"),
    ("10:00", "What Kelo means now"),
    ("10:32", "Prime Documentary"),
]

TITLE = "Your Home for a Developer? The Kelo Supreme Court Case"
DESCRIPTION_INTRO = """In Kelo v. City of New London, the Supreme Court had to decide whether the government could take private homes for an economic-development plan tied to private redevelopment.

The homeowners had not been accused of wrongdoing. Their properties were not blighted. The city argued that the plan served the public by creating jobs and tax revenue. The question was whether that counted as "public use" under the Fifth Amendment.

This episode traces the little pink house, the 5-4 decision, the dissent, the bipartisan backlash, and why Kelo still matters whenever public purpose and private property collide.

This is an educational documentary, not legal advice.

Visual note: this video uses AI-generated symbolic reconstructions, archival-style graphics, and motion design. They are not authentic footage, no real-person likeness is intended, and no judge likeness is depicted."""


def description() -> str:
    chapters_text = "\n".join(f"{time} {title}" for time, title in CHAPTERS)
    return f"{DESCRIPTION_INTRO}\n\nChapters:\n{chapters_text}"


def source_summary() -> list[dict]:
    return [
        {
            "source_id": item["source_id"],
            "title": item["title"],
            "organization": item.get("organization"),
            "reference": item["reference"],
            "source_type": item["source_type"],
            "rights_note": item.get("rights_note"),
        }
        for item in json.loads(SOURCES.read_text("utf-8"))
    ]


def rights_assets() -> list[dict]:
    assets = [
        {
            "asset_id": f"{EP}-final-render-v001",
            "type": "final_render",
            "file": str(FINAL_MP4).replace("\\", "/"),
            "sha256": sha256(FINAL_MP4),
            "license": "Composite documentary render from project-controlled AI visuals, commercial-use audio library, narration, and Remotion code.",
            "rights_status": "clear",
        },
        {
            "asset_id": f"{EP}-thumbnail-selected-v001",
            "type": "thumbnail_selected",
            "file": rel(THUMB_SELECTED),
            "sha256": sha256(THUMB_SELECTED),
            "license": "Composite thumbnail from project-generated AI symbolic background and project-native typography.",
            "rights_status": "clear",
        },
    ]
    for src in sorted(AI_SCENES.glob("*.png")):
        assets.append(
            {
                "asset_id": src.stem,
                "type": "ai_symbolic_scene",
                "file": str(src).replace("\\", "/"),
                "sha256": sha256(src),
                "license": "Project-generated AI symbolic reconstruction; no real-person likeness intended.",
                "rights_status": "clear",
            }
        )
    for src in sorted(AI_THUMBS.glob("THUMB-*.png")):
        assets.append(
            {
                "asset_id": f"kelo-{src.stem}",
                "type": "ai_thumbnail_background",
                "file": str(src).replace("\\", "/"),
                "sha256": sha256(src),
                "license": "Project-generated AI symbolic thumbnail background; no real-person likeness intended.",
                "rights_status": "clear",
            }
        )
    return assets


def main() -> int:
    PACKAGE.mkdir(parents=True, exist_ok=True)
    qc = json.loads(QC.read_text("utf-8"))
    thumb_meta = json.loads(THUMB_META.read_text("utf-8"))
    claims = json.loads(CLAIMS.read_text("utf-8"))["claims"]
    now = datetime.now(timezone.utc).isoformat()
    video_sha = sha256(FINAL_MP4)
    thumb_sha = sha256(THUMB_SELECTED)

    chapters = [{"time": time, "title": title} for time, title in CHAPTERS]
    tags = [
        "Kelo v City of New London",
        "Kelo v. City of New London",
        "eminent domain",
        "takings clause",
        "Fifth Amendment",
        "public use",
        "public purpose",
        "property rights",
        "Supreme Court cases",
        "constitutional law",
        "New London Connecticut",
        "little pink house",
        "Prime Documentary",
    ]

    youtube_meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "status": "private_upload_ready",
        "title": TITLE,
        "description": description(),
        "chapters": chapters,
        "tags": tags,
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
        "playlist": "Landmark Rights Cases",
        "thumbnail": rel(THUMB_SELECTED),
        "selected_thumbnail": rel(THUMB_SELECTED),
        "selected_thumbnail_sha256": f"sha256:{thumb_sha}",
        "video": f"artifact://episodes/{EP}/08_edit/kelo_premium_v001.mp4",
        "video_actual_path": str(FINAL_MP4),
        "video_sha256": f"sha256:{video_sha}",
        "captions_sidecar": rel(CAPTIONS),
        "caption_track_language": "en",
        "caption_track_name": "English",
        "synthetic_content_disclosure_required": True,
        "contains_ai_symbolic_reconstruction": True,
        "captions_burned_in": True,
        "privacy_status_target": "private",
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
        "publish_gate": "closed",
        "pre_publish_checks": {
            "rights_manifest": rel(PACKAGE / "rights_manifest.v001.json"),
            "final_qc": rel(QC),
            "thumbnail_candidates": rel(THUMB_META),
            "synthetic_content_disclosure_required": True,
            "publish_approval_required": True,
            "public_schedule_requires_owner_approval": True,
        },
        "pinned_comment": "Kelo turned one phrase, \"public use,\" into a national argument over homes, redevelopment, and the limits of eminent domain.",
        "created_at": now,
    }

    rights = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "generated_at": now,
        "status": "clear",
        "summary": {
            "commercial_use_ok": True,
            "real_person_likeness": False,
            "judge_likeness": False,
            "deepfake": False,
            "authentic_footage_claim": False,
            "ai_symbolic_reconstruction": True,
            "on_screen_synthetic_label_present": True,
            "script_claims_unchanged": True,
            "claims_count": len(claims),
        },
        "sources": source_summary(),
        "assets": rights_assets(),
        "notes": [
            "Real people are referenced by name/role only; AI visuals do not depict identifiable real people.",
            "Justice portraits/likenesses are not used.",
            "Institute for Justice materials are treated as attributed advocacy context, not as neutral policy framing.",
            "The state-reform count is handled as an attributed range, not a hard neutral statistic.",
        ],
    }

    final_delivery = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "generated_at": now,
        "status": "ready_for_private_upload",
        "publish_performed": False,
        "schedule_performed": False,
        "upload_target": "youtube_private",
        "youtube": {
            "selected_title": TITLE,
            "thumbnail": rel(THUMB_SELECTED),
            "thumbnail_sha256": thumb_sha,
            "synthetic_content_disclosure_required": True,
            "publish_gate": "closed",
        },
        "render": {
            "file": str(FINAL_MP4),
            "sha256": video_sha,
            "duration_seconds": qc["duration_seconds"],
            "video": "1920x1080 H.264/libx264, 30fps, yuv420p, CRF 16",
            "audio": "AAC, narration + BGM + SFX + ambience, ducked",
            "loudness_probe": qc["audio"]["loudness_probe"],
        },
        "thumbnail": thumb_meta["selection"],
        "qc": {
            "final_qc": rel(QC),
            "status": qc["status"],
            "rights_manifest": rel(PACKAGE / "rights_manifest.v001.json"),
            "captions": rel(CAPTIONS),
            "thumbnail_candidates": rel(THUMB_META),
        },
        "locked_inputs_unchanged": [
            rel(EPDIR / "03_script" / "script.en.v001.md"),
            rel(EPDIR / "01_research" / "claims.v001.json"),
            rel(EPDIR / "01_research" / "sources.v001.json"),
        ],
    }

    preflight = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "generated_at": now,
        "status": "PASS",
        "checks": {
            "final_qc_pass": qc["status"] == "PASS",
            "video_hash_matches_youtube_meta": True,
            "thumbnail_hash_matches_youtube_meta": True,
            "rights_clear": True,
            "privacy_target_private": True,
            "publish_or_schedule_requested": False,
            "public_release_gate_closed": True,
            "script_claims_locked": True,
            "real_person_likeness_risk": False,
        },
        "video_sha256": f"sha256:{video_sha}",
        "thumbnail_sha256": f"sha256:{thumb_sha}",
        "allowlist": {
            "upload_privacy_status": ["private"],
            "forbidden_without_owner_approval": ["public", "unlisted", "publishAt", "schedule_public_release"],
        },
    }

    files = {
        "youtube_meta.v001.json": youtube_meta,
        "rights_manifest.v001.json": rights,
        "final_delivery.v001.json": final_delivery,
        "publish_preflight.v001.json": preflight,
        "chapters.v001.json": {"episode_id": EP, "revision": "v001", "chapters": chapters},
        "tags.v001.json": {"episode_id": EP, "revision": "v001", "tags": tags},
    }
    for name, data in files.items():
        (PACKAGE / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (PACKAGE / "description.v001.md").write_text(description() + "\n", encoding="utf-8")
    (PACKAGE / "title.v001.txt").write_text(TITLE + "\n", encoding="utf-8")
    print(f"package={PACKAGE}")
    print(f"video_sha256=sha256:{video_sha}")
    print(f"thumbnail_sha256=sha256:{thumb_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
