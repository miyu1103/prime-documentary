"""Validate one generated Shorts image batch and build a labeled contact sheet.

This is intentionally image-only: it reads the authoritative prompt brief, checks the
expected PNG set on disk, verifies the delivery format, rejects exact byte duplicates,
and creates a review contact sheet without touching any render or release state.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BRIEF = ROOT / "episodes" / "_planning" / "SHORTS_CODEX_PROMPTS.v001.md"
SHORTS_ROOT = ROOT / "remotion" / "public" / "shorts"
NAME_RE = re.compile(r"^short\d+_\d{2}\.png$")


def expected_names(short: str) -> list[str]:
    text = BRIEF.read_text(encoding="utf-8")
    match = re.search(
        rf"(?ms)^## {re.escape(short)}\b.*?(?=^## short\d+\b|\Z)", text
    )
    if not match:
        raise RuntimeError(f"brief section not found: {short}")
    names = re.findall(r"^### `([^`]+\.png)`", match.group(0), flags=re.MULTILINE)
    if not names:
        raise RuntimeError(f"no expected PNG names found: {short}")
    if len(names) != len(set(names)):
        raise RuntimeError(f"duplicate expected filenames in brief: {short}")
    return names


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate(short: str, names: list[str]) -> tuple[list[Path], dict[str, str]]:
    directory = SHORTS_ROOT / short
    actual = sorted(p.name for p in directory.glob("*.png") if NAME_RE.match(p.name))
    missing = sorted(set(names) - set(actual))
    unexpected = sorted(set(actual) - set(names))
    if missing or unexpected:
        raise RuntimeError(f"coverage mismatch missing={missing} unexpected={unexpected}")

    paths = [directory / name for name in names]
    hashes: dict[str, str] = {}
    seen: dict[str, str] = {}
    for path in paths:
        with Image.open(path) as image:
            if image.format != "PNG":
                raise RuntimeError(f"not PNG: {path.name} ({image.format})")
            if image.size != (1080, 1920):
                raise RuntimeError(f"wrong dimensions: {path.name} {image.size}")
            if image.mode != "RGB":
                raise RuntimeError(f"wrong mode: {path.name} {image.mode}")
            if not image.info.get("icc_profile"):
                raise RuntimeError(f"missing ICC profile: {path.name}")
        digest = sha256(path)
        if digest in seen:
            raise RuntimeError(f"exact duplicate: {path.name} == {seen[digest]}")
        seen[digest] = path.name
        hashes[path.name] = digest
    return paths, hashes


def build_contact_sheet(short: str, paths: list[Path]) -> Path:
    destination = SHORTS_ROOT / short / f"{short}_contact_sheet.png"
    if destination.exists():
        raise RuntimeError(f"refusing to overwrite contact sheet: {destination}")

    width, height = 1840, 960
    columns = 8
    rows = math.ceil(len(paths) / columns)
    margin_x, margin_y = 28, 28
    gap_x, gap_y = 12, 18
    cell_w = (width - 2 * margin_x - (columns - 1) * gap_x) // columns
    cell_h = (height - 2 * margin_y - (rows - 1) * gap_y) // rows
    label_h = 30
    thumb_h = cell_h - label_h
    canvas = Image.new("RGB", (width, height), (13, 17, 24))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=18)

    icc_profile = None
    for index, path in enumerate(paths):
        with Image.open(path) as image:
            if icc_profile is None:
                icc_profile = image.info.get("icc_profile")
            image = image.convert("RGB")
            image.thumbnail((cell_w, thumb_h), Image.Resampling.LANCZOS)
            col, row = index % columns, index // columns
            cell_x = margin_x + col * (cell_w + gap_x)
            cell_y = margin_y + row * (cell_h + gap_y)
            image_x = cell_x + (cell_w - image.width) // 2
            image_y = cell_y
            canvas.paste(image, (image_x, image_y))
            label = path.stem
            box = draw.textbbox((0, 0), label, font=font)
            label_x = cell_x + (cell_w - (box[2] - box[0])) // 2
            draw.text((label_x, cell_y + thumb_h + 4), label, fill=(235, 239, 245), font=font)

    canvas.save(destination, format="PNG", optimize=True, icc_profile=icc_profile)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--short", required=True, help="e.g. short111")
    parser.add_argument("--contact-sheet", action="store_true")
    args = parser.parse_args()

    names = expected_names(args.short)
    paths, hashes = validate(args.short, names)
    contact = build_contact_sheet(args.short, paths) if args.contact_sheet else None
    print(f"short={args.short}")
    print(f"expected={len(names)} present={len(paths)} missing=0 unexpected=0")
    print(f"dimensions=1080x1920 mode=RGB icc=present exact_duplicates=0")
    print(f"unique_sha256={len(set(hashes.values()))}")
    if contact:
        with Image.open(contact) as image:
            print(f"contact_sheet={contact} size={image.width}x{image.height}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
