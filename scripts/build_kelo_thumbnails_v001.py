#!/usr/bin/env python3
"""Build Kelo thumbnail candidates from pre-generated AI backgrounds."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-010-kelo"
EPDIR = ROOT / "episodes" / EP
THUMB_DIR = EPDIR / "10_thumbnail"
PACKAGE_DIR = EPDIR / "09_package"
REMOTION_THUMBS = ROOT / "remotion" / "public" / "kelo" / "thumbs"
SOURCE_THUMBS = Path("H:/pd-media/assets/ai/thumbs/kelo")
SELECTED_BACKGROUND = "THUMB-02.png"


BACKGROUND_SCORES = [
    {
        "id": "THUMB-01",
        "file": "H:/pd-media/assets/ai/thumbs/kelo/THUMB-01.png",
        "scores": {"browse_stop": 23, "story_clarity": 22, "mobile_legibility": 23, "rights_safety": 25, "total": 93},
        "assessment": "Strong symbolic house-versus-demolition image; less immediate than option 02 because the demolition threat is farther from the house.",
    },
    {
        "id": "THUMB-02",
        "file": "H:/pd-media/assets/ai/thumbs/kelo/THUMB-02.png",
        "scores": {"browse_stop": 25, "story_clarity": 25, "mobile_legibility": 23, "rights_safety": 25, "total": 98},
        "assessment": "Selected. The small home under a looming wrecking ball communicates the stakes instantly, with no real-person likeness and enough negative space for bold text.",
    },
    {
        "id": "THUMB-03",
        "file": "H:/pd-media/assets/ai/thumbs/kelo/THUMB-03.png",
        "scores": {"browse_stop": 21, "story_clarity": 20, "mobile_legibility": 24, "rights_safety": 25, "total": 90},
        "assessment": "Clean public/private contrast, but the emotional event is less obvious at small sizes.",
    },
    {
        "id": "THUMB-04",
        "file": "H:/pd-media/assets/ai/thumbs/kelo/THUMB-04.png",
        "scores": {"browse_stop": 22, "story_clarity": 22, "mobile_legibility": 21, "rights_safety": 25, "total": 90},
        "assessment": "Moody and safe, but busier and less instantly legible than option 02.",
    },
    {
        "id": "THUMB-05",
        "file": "H:/pd-media/assets/ai/thumbs/kelo/THUMB-05.png",
        "scores": {"browse_stop": 18, "story_clarity": 17, "mobile_legibility": 24, "rights_safety": 25, "total": 84},
        "assessment": "Safe legal-document mood, but too abstract for a high-CTR browse surface.",
    },
    {
        "id": "THUMB-06",
        "file": "H:/pd-media/assets/ai/thumbs/kelo/THUMB-06.png",
        "scores": {"browse_stop": 19, "story_clarity": 19, "mobile_legibility": 23, "rights_safety": 25, "total": 86},
        "assessment": "Good aftermath symbolism, but lacks the immediate conflict shown in option 02.",
    },
]


TITLE_OPTIONS = [
    {
        "id": "A",
        "title": "THEY TOOK HER HOME",
        "variant": "left",
        "scores": {"curiosity": 24, "accuracy": 24, "mobile_legibility": 24, "emotional_stakes": 24, "total": 96},
        "assessment": "Direct and emotional; strong, but slightly less audience-involving than option B.",
    },
    {
        "id": "B",
        "title": "YOUR HOME FOR A DEVELOPER?",
        "variant": "left",
        "scores": {"curiosity": 25, "accuracy": 25, "mobile_legibility": 23, "emotional_stakes": 25, "total": 98},
        "assessment": "Selected. Turns the Kelo holding into an immediate viewer-facing question while staying neutral and factual.",
    },
    {
        "id": "C",
        "title": "THE 5-4 TAKING",
        "variant": "left",
        "scores": {"curiosity": 22, "accuracy": 25, "mobile_legibility": 25, "emotional_stakes": 21, "total": 93},
        "assessment": "Accurate and short, but less concrete for non-legal viewers.",
    },
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str | Path], cwd: Path) -> None:
    args = [str(x) for x in cmd]
    if args and args[0] == "npm":
        args[0] = "npm.cmd"
    subprocess.run(args, cwd=cwd, check=True)


def main() -> int:
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    REMOTION_THUMBS.mkdir(parents=True, exist_ok=True)

    for src in sorted(SOURCE_THUMBS.glob("THUMB-*.png")):
        shutil.copy2(src, REMOTION_THUMBS / src.name)

    selected_background_static = f"kelo/thumbs/{SELECTED_BACKGROUND}"
    rendered = []
    for option in TITLE_OPTIONS:
        out_name = f"thumbnail.kelo_option_{option['id']}.v001.png"
        out_path = THUMB_DIR / out_name
        props_path = THUMB_DIR / f"thumbnail.kelo_option_{option['id']}.props.json"
        props = {
            "title": option["title"],
            "backgroundSrc": selected_background_static,
            "variant": option["variant"],
        }
        props_path.write_text(json.dumps(props, indent=2) + "\n", encoding="utf-8")
        run(
            [
                "npm",
                "run",
                "still",
                "--",
                "ThumbnailFrame",
                str(out_path),
                f"--props={props_path}",
                "--overwrite",
            ],
            ROOT / "remotion",
        )
        rendered.append(
            {
                **option,
                "file": str(out_path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256(out_path),
                "background_static": selected_background_static,
            }
        )

    selected = next(item for item in rendered if item["id"] == "B")
    selected_path = PACKAGE_DIR / "thumbnail.selected.v001.png"
    shutil.copy2(ROOT / selected["file"], selected_path)

    meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "slug": "kelo",
        "revision": "v001",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "selected_private_upload_candidate",
        "selection": {
            "selected_id": selected["id"],
            "selected_title": selected["title"],
            "selected_file": str(selected_path.relative_to(ROOT)).replace("\\", "/"),
            "selected_sha256": sha256(selected_path),
            "selected_background": SELECTED_BACKGROUND,
            "reason": selected["assessment"],
        },
        "background_selection": {
            "selected_background": SELECTED_BACKGROUND,
            "criteria": {
                "browse_stop": "Immediate visual interruption in the feed.",
                "story_clarity": "Viewer can infer home versus redevelopment without reading metadata.",
                "mobile_legibility": "Enough dark/quiet space for the title overlay.",
                "rights_safety": "No real-person likeness, judge likeness, or authentic document impersonation.",
            },
            "options": BACKGROUND_SCORES,
        },
        "title_options": rendered,
        "rights_gate": {
            "real_person_likeness": False,
            "judge_likeness": False,
            "deepfake": False,
            "symbolic_ai_reconstruction": True,
            "commercial_use_ok": True,
        },
    }
    meta_path = PACKAGE_DIR / "title_thumbnail_candidates.v001.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"selected={selected_path} sha256={meta['selection']['selected_sha256']}")
    print(f"meta={meta_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
