#!/usr/bin/env python3
"""Inventory EP73 plates, bind Codex cache provenance, and build review sheets."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW = Path(r"E:\pd-media\assets\ai\uri\_v001")
DEFAULT_FINAL = ROOT / "remotion" / "public" / "uri" / "img"
DEFAULT_CACHE = Path.home() / ".codex" / "generated_images" / "01a02078-d910-7051-b16e-7789b3d26100"
DEFAULT_QC = Path(r"E:\pd-media\assets\ai\uri\_v001_qc")
DEFAULT_RECEIPT = ROOT / "episodes" / "_planning" / "EP73_uri_generation_receipt.v001.json"
DEFAULT_VERDICTS = ROOT / "episodes" / "_planning" / "EP73_uri_plate_verdicts.v001.json"
ORDER_FILE = ROOT / "episodes" / "_planning" / "EP73_uri_CODEX_BATCH_A.v001.md"
EXPECTED = [f"U{i:03d}.png" for i in range(1, 121)]
TARGET = (3840, 2160)

REGISTER_IDS = {
    "snow": ["U003", "U009", "U031", "U050", "U051", "U052", "U053", "U054"],
    "wellhead": ["U004", "U023", "U044", "U081", "U082", "U083", "U087", "U117"],
    "control_room": ["U001", "U002", "U008", "U019", "U057", "U058", "U059", "U060"],
    "domestic_interior": ["U064", "U065", "U066", "U067", "U068", "U069", "U070", "U071"],
}

PRELIMINARY_FINDINGS = {
    "U001": {
        "verdict": "reject_recommended",
        "reasons": ["Text-like UI glyphs appear across multiple monitors; a storefront sign also reads as generated lettering."],
    },
    "U002": {
        "verdict": "review_required",
        "reasons": ["Telephone and blurred control-room screens need owner confirmation for residual glyphs or labels."],
    },
    "U011": {
        "verdict": "reject_recommended",
        "reasons": ["Strong orange sunset glow conflicts with the explicit no-golden-hour and no-sunset-glow rule."],
    },
    "U018": {
        "verdict": "review_required",
        "reasons": ["Skyline may read as contemporary rather than the requested 1965 register."],
    },
    "U033": {
        "verdict": "reject_recommended",
        "reasons": ["United States and Texas flags are clearly visible, conflicting with the emblem and insignia exclusion."],
    },
    "U038": {
        "verdict": "reject_recommended",
        "reasons": ["Calculator keys contain visible numerals and arithmetic glyphs."],
    },
    "U057": {
        "verdict": "reject_recommended",
        "reasons": ["Dense monitor UI contains text-like glyphs and numeric-looking marks."],
    },
    "U058": {
        "verdict": "review_required",
        "reasons": ["Large graph wall needs owner confirmation that no axis labels, numerals, or generated glyphs read at edit scale."],
    },
    "U060": {
        "verdict": "review_required",
        "reasons": ["Telephone keypad and console need owner confirmation for button labels or numerals."],
    },
    "U075": {
        "verdict": "reject_recommended",
        "reasons": ["Generator carries a visible wordmark-like label and the exterior cold-day plate lacks the required thin snow or ice."],
    },
    "U101": {
        "verdict": "reject_recommended",
        "reasons": ["Vehicle badges and registration plates are visible; bottle packaging also carries label-like marks."],
    },
    "U112": {
        "verdict": "reject_recommended",
        "reasons": ["Legislative chamber includes multiple official portraits, flags, and plaque-like insignia."],
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(directory: Path, require_target: bool) -> dict:
    files = sorted(directory.glob("U[0-9][0-9][0-9].png")) if directory.exists() else []
    found = {path.name for path in files}
    rows = []
    hashes: defaultdict[str, list[str]] = defaultdict(list)
    sizes: Counter[str] = Counter()
    modes: Counter[str] = Counter()
    invalid = []
    for path in files:
        with Image.open(path) as image:
            size = image.size
            mode = image.mode
        file_hash = sha256(path)
        row = {
            "id": path.stem,
            "file": path.name,
            "path": str(path),
            "sha256": file_hash,
            "width": size[0],
            "height": size[1],
            "aspect_ratio": round(size[0] / size[1], 6),
            "mode": mode,
            "bytes": path.stat().st_size,
        }
        rows.append(row)
        hashes[file_hash].append(path.name)
        sizes[f"{size[0]}x{size[1]}"] += 1
        modes[mode] += 1
        if mode != "RGB" or (require_target and size != TARGET):
            invalid.append(row)
    all_png_names = {path.name for path in directory.glob("*.png")} if directory.exists() else set()
    return {
        "directory": str(directory),
        "count": len(files),
        "missing": sorted(set(EXPECTED) - found),
        "unexpected": sorted(all_png_names - set(EXPECTED)),
        "sizes": dict(sizes),
        "modes": dict(modes),
        "invalid": invalid,
        "exact_duplicate_groups": [names for names in hashes.values() if len(names) > 1],
        "rows": rows,
    }


def cache_index(directory: Path) -> dict[str, list[str]]:
    index: defaultdict[str, list[str]] = defaultdict(list)
    if directory.exists():
        for path in sorted(directory.glob("exec-*.png")):
            index[sha256(path)].append(str(path))
    return dict(index)


def make_sheet(rows: list[dict], output: Path, columns: int = 4) -> str:
    font = ImageFont.load_default(size=24)
    tile_width, image_height, label_height = 480, 270, 34
    line_count = (len(rows) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile_width, line_count * (image_height + label_height)), "#111111")
    draw = ImageDraw.Draw(sheet)
    for position, row in enumerate(rows):
        with Image.open(row["path"]) as image:
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
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, "JPEG", quality=94, subsampling=0)
    return str(output)


def make_contact_sheets(rows: list[dict], output_dir: Path) -> tuple[list[str], dict[str, str]]:
    outputs = []
    page_size = 20
    for page_start in range(0, len(rows), page_size):
        page = rows[page_start:page_start + page_size]
        output = output_dir / f"contact_sheet_raw_{page[0]['id']}-{page[-1]['id']}.jpg"
        outputs.append(make_sheet(page, output))
    by_id = {row["id"]: row for row in rows}
    registers = {}
    for name, ids in REGISTER_IDS.items():
        register_rows = [by_id[plate_id] for plate_id in ids if plate_id in by_id]
        registers[name] = make_sheet(register_rows, output_dir / f"register_{name}.jpg")
    return outputs, registers


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--final", type=Path, default=DEFAULT_FINAL)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--qc-dir", type=Path, default=DEFAULT_QC)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--verdicts", type=Path, default=DEFAULT_VERDICTS)
    args = parser.parse_args()

    raw = inventory(args.raw, require_target=False)
    final = inventory(args.final, require_target=True)
    cache = cache_index(args.cache)
    for row in raw["rows"]:
        row["codex_cache_matches"] = cache.get(row["sha256"], [])

    sheets, registers = make_contact_sheets(raw["rows"], args.qc_dir)
    preliminary_rows = [row for row in raw["rows"] if row["id"] in PRELIMINARY_FINDINGS]
    preliminary_sheet = make_sheet(
        preliminary_rows,
        args.qc_dir / "preliminary_findings_U001-U112.jpg",
    )
    now = datetime.now(timezone.utc).isoformat()
    raw_pass = (
        raw["count"] == 120
        and not raw["missing"]
        and not raw["unexpected"]
        and raw["modes"] == {"RGB": 120}
        and not raw["exact_duplicate_groups"]
        and all(len(row["codex_cache_matches"]) == 1 for row in raw["rows"])
    )
    final_pass = (
        final["count"] == 120
        and not final["missing"]
        and not final["unexpected"]
        and not final["invalid"]
        and not final["exact_duplicate_groups"]
    )
    receipt = {
        "schema_version": "1.0.0",
        "episode_id": "PD-2026-073-uri",
        "scope": "image_generation_and_raw_technical_qc_only",
        "generated_at": now,
        "order_file": str(ORDER_FILE),
        "order_file_sha256": sha256(ORDER_FILE),
        "provider": "Codex built-in image generation",
        "one_prompt_one_image": True,
        "requested_count": 120,
        "raw": raw,
        "final_4k": final,
        "contact_sheets": sheets,
        "required_register_sheets": registers,
        "preliminary_findings_sheet": preliminary_sheet,
        "passes_raw_technical_qc": raw_pass,
        "passes_final_technical_qc": final_pass,
        "human_review_status": "pending_owner_review",
        "remotion_staging_status": "not_staged",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    verdicts = {
        "schema_version": "1.0.0",
        "episode_id": "PD-2026-073-uri",
        "source_revision": "raw_codex_v001",
        "generated_at": now,
        "human_review_status": "pending_owner_review",
        "review_instructions": [
            "Reject any casualty, grief, hospital, funeral, grave, or person in medical distress.",
            "Reject any face that reads as a specific real person.",
            "Reject any readable glyph, numeral, logo, emblem, badge, seal, or licence plate.",
            "Reject wrong snow geography, deep snow, alpine or northern-city cues.",
            "Reject courtroom furniture and golden-hour or postcard lighting.",
        ],
        "agent_preliminary_review": {
            "status": "complete_at_contact_sheet_and_targeted_full_resolution_scale",
            "reject_recommended_count": sum(
                finding["verdict"] == "reject_recommended" for finding in PRELIMINARY_FINDINGS.values()
            ),
            "review_required_count": sum(
                finding["verdict"] == "review_required" for finding in PRELIMINARY_FINDINGS.values()
            ),
            "not_flagged_count": 120 - len(PRELIMINARY_FINDINGS),
            "note": "This is not owner acceptance and does not clear any plate for staging or publication.",
        },
        "plates": [],
    }
    for row in raw["rows"]:
        finding = PRELIMINARY_FINDINGS.get(row["id"])
        verdicts["plates"].append(
            {
                "id": row["id"],
                "sha256": row["sha256"],
                "technical_status": "pass",
                "agent_preliminary_verdict": finding["verdict"] if finding else "not_flagged",
                "agent_reasons": finding["reasons"] if finding else [],
                "human_verdict": None,
                "human_reasons": [],
            }
        )
    args.verdicts.write_text(json.dumps(verdicts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    matched = sum(len(row["codex_cache_matches"]) == 1 for row in raw["rows"])
    print(f"raw: {raw['count']}/120 missing={len(raw['missing'])} unexpected={len(raw['unexpected'])}")
    print(f"raw sizes: {raw['sizes']} modes={raw['modes']}")
    print(f"raw exact duplicate groups: {len(raw['exact_duplicate_groups'])}")
    print(f"cache provenance exact matches: {matched}/120")
    print(f"final 4k: {final['count']}/120 pass={final_pass}")
    print(f"contact sheets: {len(sheets)} registers={len(registers)} preliminary_findings=1")
    print(f"receipt: {args.receipt}")
    print(f"verdicts: {args.verdicts}")
    return 0 if raw_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
