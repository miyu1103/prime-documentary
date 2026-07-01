#!/usr/bin/env python3
"""Check whether EP19 hero stills are ready for final assembly.

Read-only by default. It verifies the exact selected path expected by the EP19
final builder: EP19-IMG-001.png through EP19-IMG-092.png.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-019-varsityblues"
EPDIR = ROOT / "episodes" / EP
SELECTED = Path("H:/pd-media") / "episodes" / EP / "05_visuals" / "selected"
REPORT = EPDIR / "08_edit" / "image_readiness.v001.json"
EXPECTED = 92
MIN_LONG_EDGE = 3840
ASPECT = 16 / 9
ASPECT_TOLERANCE = 0.025


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def png_dims(path: Path) -> tuple[int, int] | None:
    try:
        data = path.open("rb").read(24)
    except OSError:
        return None
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def check() -> dict:
    rows = []
    hard_fail = 0
    for i in range(1, EXPECTED + 1):
        image_id = f"EP19-IMG-{i:03d}"
        path = SELECTED / f"{image_id}.png"
        dims = png_dims(path)
        problems = []
        if not path.exists():
            problems.append("missing")
        elif dims is None:
            problems.append("not_png_or_unreadable")
        else:
            w, h = dims
            if max(w, h) < MIN_LONG_EDGE:
                problems.append(f"long_edge_below_{MIN_LONG_EDGE}")
            if abs((w / h) - ASPECT) > ASPECT_TOLERANCE:
                problems.append("aspect_not_16x9")
        if problems:
            hard_fail += 1
        rows.append(
            {
                "image_id": image_id,
                "path": str(path).replace("\\", "/"),
                "exists": path.exists(),
                "dimensions": list(dims) if dims else None,
                "ok": not problems,
                "problems": problems,
            }
        )
    return {
        "episode_id": EP,
        "status": "PASS" if hard_fail == 0 else "FAIL",
        "selected_dir": str(SELECTED).replace("\\", "/"),
        "expected": EXPECTED,
        "ok_count": EXPECTED - hard_fail,
        "fail_count": hard_fail,
        "requirements": {
            "format": "png",
            "long_edge_min_px": MIN_LONG_EDGE,
            "aspect": "16:9",
            "r3_visual_rules": [
                "no real-person likeness",
                "no real university logo/crest/mascot",
                "no real landmark",
                "no readable institutional marks",
            ],
        },
        "images": rows,
        "created_at": now(),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write-report", action="store_true")
    args = ap.parse_args()
    result = check()
    if args.write_report:
        REPORT.parent.mkdir(exist_ok=True)
        REPORT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"EP19 image readiness: {result['status']} ({result['ok_count']}/{result['expected']} ok)")
        if result["status"] != "PASS":
            missing = [row["image_id"] for row in result["images"] if not row["ok"]][:12]
            print("first failing slots:", ", ".join(missing))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
