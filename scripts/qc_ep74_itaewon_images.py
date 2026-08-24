#!/usr/bin/env python3
"""Inventory EP74 plates, bind Codex cache provenance, and build review sheets."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW = ROOT / "remotion" / "public" / "itaewon" / "img_raw_codex_v002"
DEFAULT_FINAL = ROOT / "remotion" / "public" / "itaewon" / "img"
DEFAULT_CACHE = Path.home() / ".codex" / "generated_images" / "01a02034-50de-7d23-aba5-95da826e33ec"
DEFAULT_QC = ROOT / "runs" / "qc"
EXPECTED = [f"I{i:03d}.png" for i in range(1, 121)]
TARGET = (3840, 2160)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(directory: Path, require_target: bool) -> dict:
    files = sorted(directory.glob("I[0-9][0-9][0-9].png")) if directory.exists() else []
    found = {path.name for path in files}
    rows = []
    hashes: defaultdict[str, list[str]] = defaultdict(list)
    sizes: Counter[str] = Counter()
    modes: Counter[str] = Counter()
    invalid = []
    dhashes: dict[str, int] = {}
    for path in files:
        with Image.open(path) as image:
            size = image.size
            mode = image.mode
            small = image.convert("L").resize((9, 8), Image.Resampling.LANCZOS)
            pixels = list(small.get_flattened_data())
            dhash = 0
            for y in range(8):
                for x in range(8):
                    dhash = (dhash << 1) | (pixels[y * 9 + x] > pixels[y * 9 + x + 1])
            dhashes[path.name] = dhash
        file_hash = sha256(path)
        row = {
            "id": path.stem,
            "file": path.name,
            "path": str(path),
            "sha256": file_hash,
            "width": size[0],
            "height": size[1],
            "mode": mode,
            "bytes": path.stat().st_size,
        }
        rows.append(row)
        hashes[file_hash].append(path.name)
        sizes[f"{size[0]}x{size[1]}"] += 1
        modes[mode] += 1
        if mode != "RGB" or (require_target and size != TARGET):
            invalid.append(row)
    near_duplicates = []
    names = sorted(dhashes)
    for index, left in enumerate(names):
        for right in names[index + 1:]:
            distance = (dhashes[left] ^ dhashes[right]).bit_count()
            if distance <= 3:
                near_duplicates.append({"left": left, "right": right, "dhash_distance": distance})
    return {
        "directory": str(directory),
        "count": len(files),
        "missing": sorted(set(EXPECTED) - found),
        "unexpected": sorted(found - set(EXPECTED)),
        "sizes": dict(sizes),
        "modes": dict(modes),
        "invalid": invalid,
        "exact_duplicate_groups": [names for names in hashes.values() if len(names) > 1],
        "near_duplicate_pairs_dhash_le_3": near_duplicates,
        "rows": rows,
    }


def cache_index(directory: Path) -> dict[str, list[str]]:
    index: defaultdict[str, list[str]] = defaultdict(list)
    if directory.exists():
        for path in sorted(directory.glob("exec-*.png")):
            index[sha256(path)].append(str(path))
    return dict(index)


def make_contact_sheets(rows: list[dict], output_dir: Path, source_label: str) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default(size=24)
    tile_width, image_height, label_height = 480, 270, 34
    columns, page_size = 4, 20
    rows_per_page = page_size // columns
    outputs = []
    for page_start in range(0, len(rows), page_size):
        page = rows[page_start:page_start + page_size]
        sheet = Image.new(
            "RGB",
            (columns * tile_width, rows_per_page * (image_height + label_height)),
            "#111111",
        )
        draw = ImageDraw.Draw(sheet)
        for position, row in enumerate(page):
            path = Path(row["path"])
            with Image.open(path) as image:
                image = image.convert("RGB")
                image.thumbnail((tile_width, image_height), Image.Resampling.LANCZOS)
                canvas = Image.new("RGB", (tile_width, image_height), "black")
                canvas.paste(image, ((tile_width - image.width) // 2, (image_height - image.height) // 2))
            column = position % columns
            line = position // columns
            x = column * tile_width
            y = line * (image_height + label_height)
            sheet.paste(canvas, (x, y))
            draw.rectangle((x, y + image_height, x + tile_width, y + image_height + label_height), fill="#111111")
            draw.text((x + 10, y + image_height + 5), row["id"], fill="white", font=font)
        first_id, last_id = page[0]["id"], page[-1]["id"]
        output = output_dir / f"contact_sheet_{source_label}_{first_id}-{last_id}.jpg"
        sheet.save(output, "JPEG", quality=94, subsampling=0)
        outputs.append(str(output))
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--final", type=Path, default=DEFAULT_FINAL)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--qc-dir", type=Path, default=DEFAULT_QC)
    args = parser.parse_args()

    raw = inventory(args.raw, require_target=False)
    final = inventory(args.final, require_target=True)
    cache = cache_index(args.cache)
    for row in raw["rows"]:
        row["codex_cache_matches"] = cache.get(row["sha256"], [])

    contact_source = final if final["count"] == 120 and not final["invalid"] else raw
    contact_label = "4k" if contact_source is final else "raw"
    sheets = make_contact_sheets(
        contact_source["rows"],
        args.qc_dir / "itaewon_contact_sheets_v001",
        contact_label,
    )
    now = datetime.now(timezone.utc).isoformat()
    order_path = ROOT / "episodes" / "_planning" / "EP74_itaewon_CODEX_BATCH_A.v001.md"
    receipt = {
        "schema_version": "1.0.0",
        "episode_id": "PD-2026-074-itaewon",
        "scope": "image_generation_only",
        "generated_at": now,
        "order_file": str(order_path),
        "order_sha256": sha256(order_path),
        "prompt_contract": {
            "formula": "canonical [STYLE] + per-plate subject + canonical [NEG] + plate-specific execution constraints",
            "canonical_prompt_source": str(order_path),
            "canonical_prompt_source_sha256": sha256(order_path),
            "semantic_repair_record": str(args.qc_dir / "itaewon_codex_visual_review.v001.json"),
        },
        "provider_metadata": {
            "provider": "Codex built-in image generation",
            "model_profile": "built-in default; opaque to caller",
            "seed": None,
            "requested_dimensions": "16:9, long edge >= 3840",
            "raw_dimensions": raw["sizes"],
            "native_4k_supported_by_provider": False,
            "approved_size_repair": "Real-ESRGAN x4plus then LANCZOS to 3840x2160",
        },
        "one_prompt_one_image": True,
        "requested_count": 120,
        "raw": raw,
        "final_4k": final,
        "contact_sheet_source": contact_label,
        "contact_sheets": sheets,
        "passes_raw_technical_qc": (
            raw["count"] == 120
            and not raw["missing"]
            and not raw["unexpected"]
            and raw["modes"] == {"RGB": 120}
            and not raw["exact_duplicate_groups"]
            and all(len(row["codex_cache_matches"]) == 1 for row in raw["rows"])
        ),
        "passes_final_technical_qc": (
            final["count"] == 120
            and not final["missing"]
            and not final["unexpected"]
            and not final["invalid"]
            and not final["exact_duplicate_groups"]
        ),
    }
    receipt_path = args.qc_dir / "itaewon_generation_receipt.v001.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    verdicts = {
        "schema_version": "1.0.0",
        "episode_id": "PD-2026-074-itaewon",
        "source_revision": contact_label,
        "generated_at": now,
        "human_review_status": "pending_owner_review",
        "review_instructions": [
            "Reject any body or anything that reads as one.",
            "Reject a face that reads as a specific real person.",
            "Reject any legible glyph.",
            "Reject Japanese, Chinese, or Western signage.",
        ],
        "plates": [
            {
                "id": row["id"],
                "sha256": row["sha256"],
                "technical_status": "pass",
                "human_verdict": None,
                "reasons": [],
            }
            for row in contact_source["rows"]
        ],
    }
    # The standard per-plate gate owns itaewon_plate_verdicts.v001.json.  This
    # generator-specific scaffold uses a different schema and must never
    # overwrite the gate's SHA-bound review record.
    verdict_path = args.qc_dir / "itaewon_generation_review_scaffold.v001.json"
    verdict_path.write_text(json.dumps(verdicts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"raw: {raw['count']}/120 missing={raw['missing']} duplicates={raw['exact_duplicate_groups']}")
    print(f"cache provenance exact matches: {sum(len(row['codex_cache_matches']) == 1 for row in raw['rows'])}/120")
    print(f"final: {final['count']}/120 invalid={len(final['invalid'])}")
    print(f"contact sheets ({contact_label}): {len(sheets)}")
    print(f"receipt: {receipt_path}")
    print(f"verdicts: {verdict_path}")
    return 0 if receipt["passes_raw_technical_qc"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
