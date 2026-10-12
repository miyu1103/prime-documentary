#!/usr/bin/env python3
"""Technical QC and labelled contact sheets for EP72 Lac-Megantic plates."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageStat


NAME_RE = re.compile(r"^L(?P<num>\d{3})\.png$")
EXPECTED = [f"L{number:03d}.png" for number in range(1, 121)]


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def parse_size(value: str) -> tuple[int, int]:
    width, height = value.lower().split("x", 1)
    return int(width), int(height)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--contact-dir", type=Path, required=True)
    parser.add_argument("--expected-size", type=parse_size)
    parser.add_argument("--semantic-status", default="pending_human_contact_sheet_review")
    args = parser.parse_args()

    files = sorted(args.dir.glob("*.png"), key=lambda path: path.name.lower())
    names = {path.name for path in files}
    missing = sorted(set(EXPECTED) - names)
    extra = sorted(names - set(EXPECTED))
    invalid_names = sorted(path.name for path in files if not NAME_RE.fullmatch(path.name))
    corrupt: list[dict[str, str]] = []
    bad_format: list[dict[str, object]] = []
    bad_dimensions: list[dict[str, object]] = []
    bad_mode: list[dict[str, object]] = []
    rows: list[dict[str, object]] = []
    hashes: dict[str, list[str]] = {}

    for path in files:
        try:
            with Image.open(path) as image:
                image.load()
                entry = {
                    "name": path.name,
                    "format": image.format,
                    "width": image.width,
                    "height": image.height,
                    "mode": image.mode,
                    "icc": bool(image.info.get("icc_profile")),
                    "mean_luma": round(ImageStat.Stat(image.convert("L")).mean[0], 3),
                    "bytes": path.stat().st_size,
                    "sha256": digest(path),
                }
                if image.format != "PNG":
                    bad_format.append(entry)
                if args.expected_size and image.size != args.expected_size:
                    bad_dimensions.append(entry)
                if image.mode != "RGB":
                    bad_mode.append(entry)
                rows.append(entry)
                hashes.setdefault(str(entry["sha256"]), []).append(path.name)
        except Exception as exc:
            corrupt.append({"name": path.name, "error": str(exc)})

    exact_duplicates = sorted(sorted(group) for group in hashes.values() if len(group) > 1)
    args.contact_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default(size=24)
    contact_files: list[str] = []
    for start in range(1, 121, 20):
        selected = [args.dir / f"L{number:03d}.png" for number in range(start, min(start + 20, 121))]
        selected = [path for path in selected if path.exists()]
        tile_width, tile_height, label_height, columns = 384, 216, 30, 5
        row_count = (len(selected) + columns - 1) // columns
        sheet = Image.new(
            "RGB",
            (columns * tile_width, row_count * (tile_height + label_height)),
            "#111318",
        )
        draw = ImageDraw.Draw(sheet)
        for index, path in enumerate(selected):
            with Image.open(path) as image:
                contained = ImageOps.contain(
                    image.convert("RGB"),
                    (tile_width, tile_height),
                    method=Image.Resampling.LANCZOS,
                )
                thumb = Image.new("RGB", (tile_width, tile_height), "black")
                thumb.paste(
                    contained,
                    ((tile_width - contained.width) // 2, (tile_height - contained.height) // 2),
                )
            x = (index % columns) * tile_width
            y = (index // columns) * (tile_height + label_height)
            sheet.paste(thumb, (x, y))
            draw.rectangle(
                (x, y + tile_height, x + tile_width, y + tile_height + label_height),
                fill="#111318",
            )
            draw.text((x + 8, y + tile_height + 2), path.stem, fill="white", font=font)
        end = min(start + 19, 120)
        output = args.contact_dir / f"lacmegantic_L{start:03d}-L{end:03d}.jpg"
        sheet.save(output, "JPEG", quality=90, optimize=True)
        contact_files.append(str(output))

    errors = (
        missing
        + extra
        + invalid_names
        + corrupt
        + bad_format
        + bad_dimensions
        + bad_mode
        + exact_duplicates
    )
    report = {
        "episode_id": "PD-2026-072-lacmegantic",
        "scope": "image_generation_only",
        "source_order": "episodes/_planning/EP72_lacmegantic_CODEX_BATCH_A.v001.md",
        "source_order_sha256": digest(
            Path(__file__).resolve().parents[1]
            / "episodes"
            / "_planning"
            / "EP72_lacmegantic_CODEX_BATCH_A.v001.md"
        ),
        "output_dir": str(args.dir),
        "expected_files": len(EXPECTED),
        "actual_files": len(files),
        "expected_size": list(args.expected_size) if args.expected_size else None,
        "size_counts": {
            f"{width}x{height}": sum(
                1 for row in rows if row["width"] == width and row["height"] == height
            )
            for width, height in sorted({(int(row["width"]), int(row["height"])) for row in rows})
        },
        "missing": missing,
        "extra": extra,
        "invalid_names": invalid_names,
        "corrupt": corrupt,
        "bad_format": bad_format,
        "bad_dimensions": bad_dimensions,
        "bad_mode": bad_mode,
        "exact_duplicate_groups": exact_duplicates,
        "icc_embedded_count": sum(bool(row["icc"]) for row in rows),
        "mean_luma_min": min((row["mean_luma"] for row in rows), default=None),
        "mean_luma_max": max((row["mean_luma"] for row in rows), default=None),
        "total_bytes": sum(int(row["bytes"]) for row in rows),
        "files": rows,
        "contact_sheets": contact_files,
        "technical_status": "pass" if not errors and len(files) == len(EXPECTED) else "fail",
        "semantic_status": args.semantic_status,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary = {key: report[key] for key in (
        "episode_id", "output_dir", "expected_files", "actual_files", "expected_size", "size_counts",
        "missing", "extra", "invalid_names", "corrupt", "bad_format", "bad_dimensions",
        "bad_mode", "exact_duplicate_groups", "icc_embedded_count", "mean_luma_min",
        "mean_luma_max", "total_bytes", "contact_sheets", "technical_status", "semantic_status",
    )}
    print(json.dumps(summary, indent=2))
    return 0 if report["technical_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
