#!/usr/bin/env python
"""Stage EP49 Strieff factory and overlay assets from the Asset Factory shelf.

This is a non-generative step. It copies already-controlled shelf media into
remotion/public/strieff and writes the exact selection JSON consumed by
build_strieff_asset_manifest.py. It never overwrites a different existing file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
from factory_themes import theme_of  # noqa: E402
from select_factory_assets import used_basenames  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-049-strieff"
SLUG = "strieff"
GLOBAL_MANIFEST = ROOT / "assets" / "asset_manifest.v001.json"
SHELF = Path("E:/pd-media/assets")
PUBLIC = ROOT / "remotion" / "public" / SLUG
STOCK = ROOT / "episodes" / EP / "05_stock"
VISUALS = ROOT / "episodes" / EP / "05_visuals"

FACTORY_SUBTYPE_PLAN = {
    # Court / law: keep this architectural and object-led, not theatrical.
    "courtroom_empty_wide": 6,
    "courtroom_interior": 6,
    "courthouse_steps": 4,
    "supreme_court_building": 4,
    "law_library_books": 4,
    "law_books_spines_macro": 3,
    "witness_stand_empty": 2,
    "jury_box_empty": 2,
    "bank_building_columns": 3,
    "government_building_exterior": 3,
    # Stop / warrant / carceral context.
    "police_car_lights_night": 8,
    "police_station_at_night": 4,
    "police_interrogation_room_empty": 4,
    "prison_corridor": 4,
    "jail_cell_bars": 3,
    "evidence_locker_shelves": 5,
    "police_badge_close_up": 3,
    "crime_scene_tape_night": 3,
    "prison_yard_fence": 2,
    # Paper trail / record search.
    "documents_on_desk": 5,
    "case_files_stack_desk": 3,
    "old_library_archive": 4,
    "stacked_legal_documents": 3,
    "vintage_typewriter": 3,
    "newspaper_printing_press": 2,
}
OVERLAY_PLAN = {
    "light_assets": 5,
    "particle_assets": 3,
    "vfx_overlays": 2,
    "loops": 2,
}
assert sum(FACTORY_SUBTYPE_PLAN.values()) == 93
assert sum(OVERLAY_PLAN.values()) == 12

FEATURELESS = (
    "wall",
    "empty_room",
    "gradient",
    "pattern",
    "wallpaper",
    "surface",
    "blank",
    "sky",
    "clouds",
    "bokeh",
    "flower",
    "food",
    "coffee",
    "animal",
    "wedding",
    "party",
    "beach",
    "mountain",
)
SUBTYPE_BLOCK = {
    "evidence_bag",
    "drug_lab",
    "cash_counting",
    "one_way_mirror_room",
    "lady_justice_statue",  # often symbolic stock that reads theatrical/off-topic.
    "us_constitution_document",  # risks readable pseudo-text.
}

VISUAL_BLOCK_IDS = {
    # First Strieff contact-sheet pass: visually off-topic or too person/food/nature/fantasy-led.
    "AF-BG-14190", "AF-BG-14208", "AF-BG-10014", "AF-BG-10033", "AF-BG-33661",
    "AF-BG-5463", "AF-BG-16371", "AF-BG-37222", "AF-BG-31859", "AF-BG-3837",
    "AF-BG-31942", "AF-BG-29842", "AF-BG-38113", "AF-BG-22900", "AF-BG-22917",
    "AF-BG-26319", "AF-BG-26335", "AF-BG-15016", "AF-BG-36487", "AF-BG-14905",
    "AF-BG-6848", "AF-BG-23570", "AF-BG-38348", "AF-BG-32160", "AF-BG-32175",
    "AF-BG-6745", "AF-BG-4893", "AF-BG-62994", "AF-BG-63133", "AF-BG-16118",
    "AF-BG-8243", "AF-BG-1292", "AF-BG-30342", "AF-BG-14466", "AF-BG-36138",
    "AF-BG-14328", "AF-BG-20985", "AF-BG-11420", "AF-BG-11121", "AF-BG-40852",
    "AF-BG-62446", "AF-BG-3779", "AF-BG-25193", "AF-BG-51985", "AF-BG-5601",
    "AF-BG-46950", "AF-BG-48710",
    # Overlay first pass.
    "AF-LIGHT-3406", "AF-PART-5420", "AF-PART-6048",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_assets() -> list[dict[str, Any]]:
    return json.loads(GLOBAL_MANIFEST.read_text(encoding="utf-8"))["assets"]


def dynamic_enough(item: dict[str, Any]) -> bool:
    st = str(item.get("subtype", "")).lower()
    name = Path(str(item.get("path", ""))).name.lower()
    asset_id = str(item.get("id") or "")
    if asset_id in VISUAL_BLOCK_IDS:
        return False
    if st in SUBTYPE_BLOCK:
        return False
    return not any(token in st or token in name for token in FEATURELESS)


def even_sample(items: list[dict[str, Any]], count: int) -> list[dict[str, Any]]:
    if count >= len(items):
        return items
    step = len(items) / count
    return [items[min(len(items) - 1, int(i * step))] for i in range(count)]


def pick_factory(assets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    used = used_basenames(EP)
    by_subtype: dict[str, list[dict[str, Any]]] = {}
    for item in assets:
        if item.get("kind") != "video":
            continue
        basename = Path(str(item.get("path", ""))).name
        if basename.lower() in used:
            continue
        if not dynamic_enough(item):
            continue
        subtype = str(item.get("subtype") or "")
        if subtype in FACTORY_SUBTYPE_PLAN:
            by_subtype.setdefault(subtype, []).append(item)
    for rows in by_subtype.values():
        rows.sort(key=lambda x: str(x.get("id")))

    picks: list[dict[str, Any]] = []
    seen: set[str] = set()
    for subtype, count in FACTORY_SUBTYPE_PLAN.items():
        rows = by_subtype.get(subtype, [])
        selected = even_sample(rows, count)
        if len(selected) < count:
            raise SystemExit(f"not enough factory assets for {subtype}: need {count}, have {len(selected)}")
        for item in selected:
            basename = Path(str(item["path"])).name
            if basename in seen:
                raise SystemExit(f"duplicate factory basename selected: {basename}")
            seen.add(basename)
            picks.append(item)
    return picks


def pick_overlays(assets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_type: dict[str, list[dict[str, Any]]] = {}
    for item in assets:
        if item.get("kind") != "video":
            continue
        if str(item.get("id") or "") in VISUAL_BLOCK_IDS:
            continue
        typ = str(item.get("type") or "")
        if typ not in OVERLAY_PLAN:
            continue
        subtype = str(item.get("subtype") or "").lower()
        if any(token in subtype for token in ("green", "chromakey", "fireflies", "pollen", "lantern", "forest")):
            continue
        by_type.setdefault(typ, []).append(item)
    for rows in by_type.values():
        rows.sort(key=lambda x: (str(x.get("subtype")), str(x.get("id"))))

    picks: list[dict[str, Any]] = []
    seen: set[str] = set()
    for typ, count in OVERLAY_PLAN.items():
        rows = by_type.get(typ, [])
        selected = even_sample(rows, count)
        if len(selected) < count:
            raise SystemExit(f"not enough overlay assets for {typ}: need {count}, have {len(selected)}")
        for item in selected:
            basename = Path(str(item["path"])).name
            if basename in seen:
                raise SystemExit(f"duplicate overlay basename selected: {basename}")
            seen.add(basename)
            picks.append(item)
    return picks


def copy_one(item: dict[str, Any], subdir: str, dry_run: bool) -> tuple[Path, bool]:
    src = SHELF / str(item["path"])
    dst = PUBLIC / subdir / Path(str(item["path"])).name
    if not src.is_file():
        raise FileNotFoundError(src)
    if dry_run:
        return dst, False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if sha256_file(src) != sha256_file(dst):
            raise RuntimeError(f"refusing to overwrite different existing file: {dst}")
        return dst, False
    shutil.copy2(src, dst)
    return dst, True


def entry(item: dict[str, Any], dst: Path, group: str, index: int) -> dict[str, Any]:
    src = SHELF / str(item["path"])
    return {
        "asset_id": f"STRF-{'F' if group == 'factory' else 'O'}{index:02d}",
        "source_asset_id": item.get("id"),
        "path": dst.as_posix(),
        "public_path": f"{SLUG}/{group}/{dst.name}",
        "source_path": src.as_posix(),
        "sha256": sha256_file(src),
        "kind": item.get("kind"),
        "theme": theme_of(item.get("subtype", ""), item.get("type")),
        "type": item.get("type"),
        "subtype": item.get("subtype"),
        "license": item.get("license"),
        "source": item.get("source"),
        "sourceUrl": item.get("sourceUrl"),
        "commercial_use": True,
        "ai_disclosure_required": False,
        "qc": {
            "reviewed": False,
            "label_matches_content": None,
            "has_readable_text": None,
            "has_identifiable_face": None,
            "notes": "selected from Asset Factory; review contact sheet before final approval",
        },
    }


def extract_frame(video: Path, out: Path) -> bool:
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-ss",
        "1.0",
        "-i",
        str(video),
        "-frames:v",
        "1",
        "-vf",
        "scale=512:288:force_original_aspect_ratio=increase,crop=512:288",
        str(out),
    ]
    return subprocess.run(cmd, check=False).returncode == 0 and out.is_file()


def contact_sheet(items: list[dict[str, Any]], out: Path, columns: int = 6) -> None:
    if not items:
        return
    thumb_w, thumb_h, label_h = 512, 288, 42
    rows = math.ceil(len(items) / columns)
    sheet = Image.new("RGB", (columns * thumb_w, rows * (thumb_h + label_h)), (12, 12, 14))
    draw = ImageDraw.Draw(sheet)
    with tempfile.TemporaryDirectory(prefix="strieff_frames_") as td:
        tmp = Path(td)
        for idx, item in enumerate(items):
            video = Path(str(item["path"]))
            frame = tmp / f"{idx:03d}.jpg"
            x = (idx % columns) * thumb_w
            y = (idx // columns) * (thumb_h + label_h)
            if extract_frame(video, frame):
                with Image.open(frame) as im:
                    thumb = ImageOps.fit(im.convert("RGB"), (thumb_w, thumb_h), Image.Resampling.LANCZOS)
            else:
                thumb = Image.new("RGB", (thumb_w, thumb_h), (38, 16, 16))
                draw.text((x + 16, y + 120), "FRAME FAILED", fill=(255, 210, 210))
            sheet.paste(thumb, (x, y))
            draw.rectangle((x, y + thumb_h, x + thumb_w, y + thumb_h + label_h), fill=(24, 24, 28))
            label = f"{item['asset_id']} {item.get('source_asset_id')} {item.get('subtype')}"
            draw.text((x + 10, y + thumb_h + 8), label[:76], fill=(232, 232, 238))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=90)


def write_selection(factory: list[dict[str, Any]], overlay: list[dict[str, Any]]) -> None:
    STOCK.mkdir(parents=True, exist_ok=True)
    VISUALS.mkdir(parents=True, exist_ok=True)
    (STOCK / "factory_selection.v001.json").write_text(
        json.dumps(
            {
                "schema_version": "strieff_factory_selection.v1",
                "episode_id": EP,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "factory": factory,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (STOCK / "overlay_selection.v001.json").write_text(
        json.dumps(
            {
                "schema_version": "strieff_overlay_selection.v1",
                "episode_id": EP,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "overlay": overlay,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    contact_sheet(factory, VISUALS / "strieff_factory_contact_sheet.v001.jpg")
    contact_sheet(overlay, VISUALS / "strieff_overlay_contact_sheet.v001.jpg", columns=4)


def prune_unselected(factory: list[dict[str, Any]], overlay: list[dict[str, Any]]) -> int:
    keep = {
        "factory": {Path(str(item["public_path"])).name for item in factory},
        "overlay": {Path(str(item["public_path"])).name for item in overlay},
    }
    removed = 0
    for subdir in ("factory", "overlay"):
        folder = (PUBLIC / subdir).resolve()
        expected_parent = (PUBLIC / subdir).resolve()
        if folder != expected_parent or not str(folder).startswith(str(PUBLIC.resolve())):
            raise RuntimeError(f"refusing unsafe prune path: {folder}")
        if not folder.is_dir():
            continue
        for path in folder.iterdir():
            if path.is_file() and path.suffix.lower() in {".mp4", ".mov", ".webm", ".mkv", ".m4v"}:
                if path.name not in keep[subdir]:
                    path.unlink()
                    removed += 1
    return removed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--prune-unselected", action="store_true")
    args = parser.parse_args()

    assets = load_assets()
    factory_picks = pick_factory(assets)
    overlay_picks = pick_overlays(assets)
    copied = 0
    factory_rows = []
    overlay_rows = []
    for i, item in enumerate(factory_picks, 1):
        dst, did_copy = copy_one(item, "factory", args.dry_run)
        copied += int(did_copy)
        factory_rows.append(entry(item, dst, "factory", i))
    for i, item in enumerate(overlay_picks, 1):
        dst, did_copy = copy_one(item, "overlay", args.dry_run)
        copied += int(did_copy)
        overlay_rows.append(entry(item, dst, "overlay", i))

    pruned = 0
    if not args.dry_run:
        write_selection(factory_rows, overlay_rows)
        if args.prune_unselected:
            pruned = prune_unselected(factory_rows, overlay_rows)
    result = {
        "ok": True,
        "dry_run": args.dry_run,
        "factory": len(factory_rows),
        "overlay": len(overlay_rows),
        "newly_copied": copied,
        "pruned_unselected": pruned,
        "public": PUBLIC.as_posix(),
        "factory_contact_sheet": (VISUALS / "strieff_factory_contact_sheet.v001.jpg").as_posix(),
        "overlay_contact_sheet": (VISUALS / "strieff_overlay_contact_sheet.v001.jpg").as_posix(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
