#!/usr/bin/env python3
"""Render OneCoin thumbnail candidates v008 (flashier variant)."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-017-onecoin"
EPDIR = ROOT / "episodes" / EP
THUMB_DIR = EPDIR / "10_thumbnail"
PACKAGE_DIR = EPDIR / "09_package"
REMOTION_DIR = ROOT / "remotion"

OPTION_OPTIONS = [
    {
        "id": "A",
        "title": "There Was No Coin",
        "headline": "THERE WAS\nNO COIN",
        "kicker": "MILLIONS BELIEVED",
        "composition_id": "OneCoinThumb-A",
        "output": THUMB_DIR / "thumbnail.onecoin_option_A.v008.png",
        "background": "onecoin/hero/T-IMG-003.png",
    },
    {
        "id": "B",
        "title": "She Vanished",
        "headline": "SHE\nVANISHED",
        "kicker": "STILL ON THE FBI'S LIST",
        "composition_id": "OneCoinThumb-B",
        "output": THUMB_DIR / "thumbnail.onecoin_option_B.v008.png",
        "background": "onecoin/hero/T-IMG-012.png",
    },
    {
        "id": "C",
        "title": "$4 Billion. Gone.",
        "headline": "$4 BILLION.\nGONE.",
        "kicker": "ONECOIN",
        "composition_id": "OneCoinThumb-C",
        "output": THUMB_DIR / "thumbnail.onecoin_option_C.v008.png",
        "background": "onecoin/hero/T-IMG-002.png",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def run_still(comp_id: str, out: Path) -> None:
    args = [
        "npm.cmd",
        "run",
        "still",
        "--",
        comp_id,
        str(out),
        "--overwrite",
    ]
    subprocess.run(args, cwd=REMOTION_DIR, check=True)


def copy_selected_thumbnail(options: list[dict], selected_index: int = 0) -> Path:
    selected = options[selected_index]
    source_file = ROOT / selected["file"]
    selected_file = PACKAGE_DIR / "thumbnail.selected.v008.png"
    if not source_file.exists():
        raise FileNotFoundError(source_file)
    shutil.copy2(source_file, selected_file)
    return selected_file


def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_options() -> list[dict]:
    rendered = []
    for option in OPTION_OPTIONS:
        option["output"].parent.mkdir(parents=True, exist_ok=True)
        run_still(option["composition_id"], option["output"])
        rendered.append(
            {
                "id": option["id"],
                "title": option["title"],
                "thumbnail_text": option["headline"].replace("\n", " "),
                "kicker": option["kicker"],
                "file": str(option["output"].relative_to(ROOT)).replace("\\", "/"),
                "background": option["background"],
                "sha256": sha256(option["output"]),
            }
        )
    return rendered


def build_package() -> None:
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    options = render_options()
    selected = options[0]
    selected_path = copy_selected_thumbnail(options, 0)
    selected_sha = sha256(selected_path)

    title_meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v008",
        "status": "owner_review_required_not_approved",
        "selected_option": selected["id"],
        "selected_thumbnail": str(selected_path.relative_to(ROOT)).replace("\\", "/"),
        "selected_thumbnail_sha256": sha256(selected_path),
        "selected_title": selected["title"],
        "options": [
            {
                **option,
                "composition_id": OPTION_OPTIONS[i]["composition_id"],
                "selected": option["id"] == selected["id"],
            }
            for i, option in enumerate(options)
        ],
        "generated_at": now(),
        "design_tone": "flashy_high_contrast",
        "guardrails": [
            "No real-person likeness.",
            "No OneCoin logo.",
            "No 'guilty' or 'convicted' language for Ruja Ignatova.",
            "Manual owner approval required before upload.",
            "Uppercase, browse-safe, 4-word+ headline composition preserved.",
        ],
    }
    write_json(PACKAGE_DIR / "title_thumbnail_candidates.v008.json", title_meta)
    print(f"selected={selected_path}")
    print(f"sha={selected_sha}")


def main() -> int:
    build_package()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
