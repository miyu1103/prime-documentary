"""Build the EP81 Station raw Codex image receipt without modifying any plate."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
DEST = Path(r"E:\pd-media\05_visuals\station\img")
CACHE = Path(
    r"C:\Users\aab15\.codex\generated_images"
    r"\01a03413-1c47-7bf3-8bba-fdb2c4659f60"
)
ORDER = ROOT / "episodes/_planning/EP81_station_CODEX_BATCH_A.v001.md"
PASTE_ALL = ROOT / "episodes/_planning/EP81_station_CODEX_PASTE_ALL.txt"
PLATES = ROOT / "episodes/_planning/EP81_station_CODEX_PASTE/plates.v001.jsonl"
REPORT = ROOT / "episodes/PD-2026-081-station/05_visuals/codex_image_batch.v001.json"

SOURCE_COMMIT = "58775209c9a95c73d9b7fff5008950a587e3462c"
VISUAL_REJECTS = {
    "S017": "visible numerals and lettering on dartboards",
    "S063": "state-flag emblem conflicts with the shared no-emblem constraint",
    "S078": "visible stopwatch numerals",
    "S080": "generated exit-sign glyph conflicts with the no-lettering constraint",
    "S089": "legible EXIT lettering",
    "S098": "generated screen and device text/numerals",
    "S121": "generated console-screen text/numerals",
    "S122": "generated console-screen text/numerals",
    "S133": "state-flag emblem conflicts with the shared no-emblem constraint",
    "S135": "semantic mismatch: bridge engineering drawing instead of a relevant venue exhibit",
    "S143": "visible tape-measure numerals",
    "S156": "visible tape-measure numerals and form-like pseudo-writing",
    "S157": "visible tape-measure numerals",
    "S158": "floor-plan annotations render as generated text-like glyphs",
    "S164": "generated console-screen text/numerals",
}
OWNER_REVIEW = {
    "S062": "tiny person icons on the plan should be checked against the no-face constraint",
    "S115": "small badge-like truck detail may conflict with the no-markings constraint",
    "S126": "small badge-like apparatus details may conflict with the no-markings constraint",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    rows = [json.loads(line) for line in PLATES.read_text(encoding="utf-8").splitlines() if line]
    expected = {f"S{i:03d}.png" for i in range(1, 189)}
    destination_files = sorted(DEST.glob("S*.png"))
    destination_names = {path.name for path in destination_files}

    cache_by_hash: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(CACHE.glob("*.png")):
        cache_by_hash[sha256(path)].append(path)

    assets: list[dict[str, object]] = []
    corrupt: list[dict[str, str]] = []
    destination_by_hash: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        path = DEST / row["file"]
        if not path.is_file():
            continue
        digest = sha256(path)
        destination_by_hash[digest].append(path.name)
        try:
            with Image.open(path) as image:
                image.load()
                metadata = {
                    "width": image.width,
                    "height": image.height,
                    "format": image.format,
                    "mode": image.mode,
                }
        except Exception as exc:  # diagnostic path
            corrupt.append({"file": path.name, "error": str(exc)})
            continue
        matches = cache_by_hash.get(digest, [])
        assets.append(
            {
                "id": row["id"],
                "file": row["file"],
                "section": row["section"],
                "people_flag": "P" in row.get("flags", []),
                "sha256": digest,
                "bytes": path.stat().st_size,
                **metadata,
                "cache_file": str(matches[0]).replace("\\", "/") if len(matches) == 1 else None,
            }
        )

    dimensions = Counter(f"{a['width']}x{a['height']}" for a in assets)
    modes = Counter(str(a["mode"]) for a in assets)
    formats = Counter(str(a["format"]) for a in assets)
    wrong_ratio = [
        str(a["id"])
        for a in assets
        if abs(int(a["width"]) / int(a["height"]) - 16 / 9) > 0.002
    ]
    exact_duplicates = [names for names in destination_by_hash.values() if len(names) > 1]
    cache_mismatches = [str(a["id"]) for a in assets if a["cache_file"] is None]
    inventory = "\n".join(
        f"{a['file']}|{a['sha256']}|{a['bytes']}|{a['width']}x{a['height']}|{a['mode']}|{a['format']}"
        for a in assets
    )

    accepted = [
        row["id"]
        for row in rows
        if row["id"] not in VISUAL_REJECTS and row["id"] not in OWNER_REVIEW
    ]
    technical_pass = (
        len(assets) == 188
        and destination_names == expected
        and not corrupt
        and dimensions == {"1672x941": 188}
        and modes == {"RGB": 188}
        and formats == {"PNG": 188}
        and not wrong_ratio
        and not exact_duplicates
        and not cache_mismatches
    )

    report = {
        "schema_version": "1.0",
        "episode_id": "PD-2026-081-station",
        "recorded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "raw_generation_complete_visual_exceptions_pending_owner",
        "scope": "EP81 Station S001-S188 built-in image generation, exact-ID raw delivery, technical QC, cache provenance verification, and preliminary visual QC only",
        "source_contract": {
            "source_commit": SOURCE_COMMIT,
            "order_file": "episodes/_planning/EP81_station_CODEX_BATCH_A.v001.md",
            "order_file_sha256": sha256(ORDER),
            "instruction_file": "episodes/_planning/EP81_station_CODEX_PASTE_ALL.txt",
            "instruction_file_sha256": sha256(PASTE_ALL),
            "plates_file": "episodes/_planning/EP81_station_CODEX_PASTE/plates.v001.jsonl",
            "plates_file_sha256": sha256(PLATES),
            "batch_files": 24,
            "requested_ids": "S001-S188",
            "requested_count": 188,
            "people_flags": sum("P" in row.get("flags", []) for row in rows),
            "one_prompt_one_image": True,
            "required_aspect_ratio": "16:9",
            "accepted_raw_dimensions": ["1672x941", "3840x2160"],
        },
        "source_preflight": {
            "shared_negative_constraints": "pass",
            "prompt_coverage": "188/188",
            "prompt_diversity": "fail_with_owner_specified_repetition_retained",
            "near_duplicate_pairs": [
                "S042/S154",
                "S002/S148",
                "S001/S147",
                "S003/S151",
                "S023/S081",
                "S121/S164",
                "S065/S188",
                "S054/S140",
            ],
            "raw_identical_prompt_pairs": ["S042/S154"],
            "decision": "Generate the exact owner-specified commit without silently rewriting prompts; each ID received a separate generation call.",
        },
        "generation": {
            "provider": "Codex built-in image generation",
            "use_case": "historical-scene",
            "calls": 188,
            "outputs": 188,
            "automatic_retries": 0,
            "variants": 0,
            "overwrites": 0,
            "model_profile": "built-in provider metadata not exposed",
            "seed": "not exposed",
            "provider_cost": "not exposed by built-in tool",
            "raw_directory": "E:/pd-media/05_visuals/station/img",
            "cache_root": str(CACHE).replace("\\", "/"),
        },
        "technical_qc": {
            "status": "pass" if technical_pass else "fail",
            "files": len(assets),
            "missing_ids": sorted(expected - destination_names),
            "unexpected_ids": sorted(destination_names - expected),
            "corrupt": corrupt,
            "dimensions": dict(dimensions),
            "image_mode": dict(modes),
            "format": dict(formats),
            "wrong_aspect_ids": wrong_ratio,
            "exact_duplicate_groups": exact_duplicates,
            "cache_sha_matches": len(assets) - len(cache_mismatches),
            "cache_sha_mismatches": cache_mismatches,
            "total_bytes": sum(int(a["bytes"]) for a in assets),
            "inventory_sha256": hashlib.sha256(inventory.encode("utf-8")).hexdigest(),
        },
        "visual_qc": {
            "status": "exceptions_pending_owner",
            "method": "All 16 labelled contact sheets reviewed; suspected text, numeral, emblem, and semantic failures inspected at original resolution.",
            "contact_sheet_directory": "runs/qc/plate_sheets/station",
            "contact_sheets": 16,
            "accepted_without_flag": accepted,
            "reject_recommended": VISUAL_REJECTS,
            "owner_review": OWNER_REVIEW,
            "automatic_regeneration_performed": False,
            "staged_for_edit": False,
            "approved_for_use": False,
        },
        "assets": assets,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "report": str(REPORT),
                "technical_status": report["technical_qc"]["status"],
                "files": len(assets),
                "accepted_without_flag": len(accepted),
                "reject_recommended": len(VISUAL_REJECTS),
                "owner_review": len(OWNER_REVIEW),
                "cache_sha_matches": report["technical_qc"]["cache_sha_matches"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if technical_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
