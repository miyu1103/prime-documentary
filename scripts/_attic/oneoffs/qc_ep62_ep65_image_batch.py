"""Final filesystem QC for the EP62-EP65 Codex image batch."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageStat


EPISODES = {
    "greene": {"prefix": "G", "main_end": 225, "total_end": 226, "thumbs": [220, 221, 222, 226]},
    "correa": {"prefix": "C", "main_end": 226, "total_end": 227, "thumbs": [221, 222, 223, 227]},
    "memphis": {"prefix": "M", "main_end": 218, "total_end": 219, "thumbs": [208, 209, 210, 219]},
    "marmet": {"prefix": "R", "main_end": 223, "total_end": 224, "thumbs": [217, 218, 219, 224]},
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(r"E:\pd-media\assets\ai"))
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("runs/imagegen/ep62_ep65_final_qc.v001.json"),
    )
    args = parser.parse_args()

    report: dict[str, object] = {
        "expected_main_total": 892,
        "expected_unique_total": 896,
        "episodes": {},
        "invalid_files": [],
        "exact_duplicate_groups": [],
        "thumbnail_luminance": {},
    }
    hashes: dict[str, list[str]] = defaultdict(list)

    for slug, cfg in EPISODES.items():
        prefix = str(cfg["prefix"])
        main_end = int(cfg["main_end"])
        total_end = int(cfg["total_end"])
        folder = args.root / slug
        expected = {f"{prefix}{number:03d}.png" for number in range(1, total_end + 1)}
        actual = {
            path.name
            for path in folder.iterdir()
            if path.is_file() and path.name.startswith(prefix) and path.suffix.lower() == ".png"
        }
        episode_result = {
            "main_count": sum(f"{prefix}{number:03d}.png" in actual for number in range(1, main_end + 1)),
            "requested_unique_count": len(expected & actual),
            "present_top_level_count": len(actual),
            "missing": sorted(expected - actual),
            "out_of_scope_extras": sorted(actual - expected),
        }
        report["episodes"][slug] = episode_result

        for name in sorted(expected & actual):
            path = folder / name
            problems: list[str] = []
            try:
                with Image.open(path) as image:
                    if image.format != "PNG":
                        problems.append(f"format={image.format}")
                    if image.size != (3840, 2160):
                        problems.append(f"size={image.size[0]}x{image.size[1]}")
            except Exception as exc:  # pragma: no cover - diagnostic path
                problems.append(f"open_error={exc}")
            if problems:
                report["invalid_files"].append({"path": str(path), "problems": problems})
            hashes[sha256(path)].append(str(path))

        for number in cfg["thumbs"]:
            asset_id = f"{prefix}{int(number):03d}"
            path = folder / f"{asset_id}.png"
            with Image.open(path) as image:
                grey = image.convert("L")
                stats = ImageStat.Stat(grey)
            mean = round(stats.mean[0], 2)
            stddev = round(stats.stddev[0], 2)
            report["thumbnail_luminance"][asset_id] = {
                "mean": mean,
                "stddev": stddev,
                "passes_minimum": mean >= 33.0 and stddev >= 40.0,
                "meets_target": mean >= 38.0 and stddev >= 45.0,
            }

    report["exact_duplicate_groups"] = [paths for paths in hashes.values() if len(paths) > 1]
    report["actual_requested_unique_total"] = sum(
        int(item["requested_unique_count"]) for item in report["episodes"].values()
    )
    report["actual_present_top_level_total"] = sum(
        int(item["present_top_level_count"]) for item in report["episodes"].values()
    )
    report["has_out_of_scope_extras"] = any(
        item["out_of_scope_extras"] for item in report["episodes"].values()
    )
    report["passes"] = (
        report["actual_requested_unique_total"] == report["expected_unique_total"]
        and not report["invalid_files"]
        and not report["exact_duplicate_groups"]
        and all(not item["missing"] for item in report["episodes"].values())
        and all(item["passes_minimum"] for item in report["thumbnail_luminance"].values())
    )

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passes"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
