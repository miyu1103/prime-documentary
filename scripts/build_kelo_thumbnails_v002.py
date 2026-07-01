#!/usr/bin/env python3
"""Build brighter, series-consistent Kelo thumbnail candidates."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-010-kelo"
EPDIR = ROOT / "episodes" / EP
THUMB_DIR = EPDIR / "10_thumbnail"
PACKAGE_DIR = EPDIR / "09_package"
REMOTION_THUMBS = ROOT / "remotion" / "public" / "kelo" / "thumbs"
SOURCE_THUMBS = Path("H:/pd-media/assets/ai/thumbs/kelo")
SELECTED_BACKGROUND = "THUMB-02.png"

OPTIONS = [
    {
        "id": "A",
        "headlineTop": "YOUR HOME",
        "headlineBottom": "TAKEN?",
        "badge": "FOR A DEVELOPER",
        "variant": "taken",
        "score": 98,
        "assessment": "Selected. Shorter and more readable than v001, while the enlarged brighter house/wrecking-ball image carries the Kelo-specific private-development threat.",
    },
    {
        "id": "B",
        "headlineTop": "HOME",
        "headlineBottom": "FOR SALE?",
        "badge": "BY THE GOVERNMENT",
        "variant": "developer",
        "score": 92,
        "assessment": "Provocative but a little less precise than option A.",
    },
    {
        "id": "C",
        "headlineTop": "THE 5-4",
        "headlineBottom": "TAKING",
        "badge": "SUPREME COURT",
        "variant": "vote",
        "score": 91,
        "assessment": "Very legal and compact, but less viewer-facing at browse size.",
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


def make_contact_sheet(paths: list[Path], out: Path) -> None:
    thumbs = []
    for path in paths:
        img = Image.open(path).convert("RGB").resize((426, 240), Image.Resampling.LANCZOS)
        thumbs.append((path.stem, img))
    sheet = Image.new("RGB", (426 * len(thumbs), 276), (8, 8, 10))
    draw = ImageDraw.Draw(sheet)
    for i, (label, img) in enumerate(thumbs):
        x = i * 426
        sheet.paste(img, (x, 0))
        draw.text((x + 12, 248), label, fill=(245, 247, 250))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=92)


def main() -> int:
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    REMOTION_THUMBS.mkdir(parents=True, exist_ok=True)
    for src in sorted(SOURCE_THUMBS.glob("THUMB-*.png")):
        shutil.copy2(src, REMOTION_THUMBS / src.name)

    rendered = []
    rendered_paths = []
    for option in OPTIONS:
        out_path = THUMB_DIR / f"thumbnail.kelo_option_{option['id']}.v002.png"
        props_path = THUMB_DIR / f"thumbnail.kelo_option_{option['id']}.v002.props.json"
        props = {
            "backgroundSrc": f"kelo/thumbs/{SELECTED_BACKGROUND}",
            "headlineTop": option["headlineTop"],
            "headlineBottom": option["headlineBottom"],
            "badge": option["badge"],
            "variant": option["variant"],
        }
        props_path.write_text(json.dumps(props, indent=2) + "\n", encoding="utf-8")
        run(["npm", "run", "still", "--", "KeloThumbnailFrame", out_path, f"--props={props_path}", "--overwrite"], ROOT / "remotion")
        rendered_paths.append(out_path)
        rendered.append(
            {
                **option,
                "file": str(out_path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256(out_path),
                "background": str((SOURCE_THUMBS / SELECTED_BACKGROUND)).replace("\\", "/"),
            }
        )

    selected = rendered[0]
    selected_path = PACKAGE_DIR / "thumbnail.selected.v002.png"
    shutil.copy2(ROOT / selected["file"], selected_path)
    contact = THUMB_DIR / "thumbnail_contact_sheet.v002.jpg"
    make_contact_sheet(rendered_paths, contact)

    meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "slug": "kelo",
        "revision": "v002",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "selected_private_upload_candidate",
        "selection": {
            "selected_id": selected["id"],
            "selected_title": f"{selected['headlineTop']} {selected['headlineBottom']}",
            "selected_file": str(selected_path.relative_to(ROOT)).replace("\\", "/"),
            "selected_sha256": sha256(selected_path),
            "selected_background": SELECTED_BACKGROUND,
            "reason": selected["assessment"],
        },
        "design_changes_from_v001": [
            "Zoomed and brightened the symbolic house/wrecking-ball background so the image reads larger on mobile.",
            "Shortened the headline from a long question to a two-line browse headline.",
            "Restored stronger series continuity with blue eyebrow, gold rule, gold border, white/gold headline hierarchy, and PRIME DOCUMENTARY footer.",
        ],
        "title_options": rendered,
        "contact_sheet": str(contact.relative_to(ROOT)).replace("\\", "/"),
        "rights_gate": {
            "real_person_likeness": False,
            "judge_likeness": False,
            "deepfake": False,
            "symbolic_ai_reconstruction": True,
            "commercial_use_ok": True,
        },
    }
    meta_path = PACKAGE_DIR / "title_thumbnail_candidates.v002.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"selected={selected_path.relative_to(ROOT)} sha256={meta['selection']['selected_sha256']}")
    print(f"contact={contact.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
