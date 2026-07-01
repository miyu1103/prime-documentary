#!/usr/bin/env python
"""Assert that a rendered episode video lands inside the target runtime band.

Closes a QC blind spot: the review/final render QC only checks `duration_positive`,
so a short cut (~10.4 min) PASSes even though the channel standard is an
11.5-12.5 minute finished runtime (VIDEO_RULES §10). EP14 (lange) and EP15
(theranos) both fell short and EP14 had to stretch its hook at the last moment.
This gate makes the runtime window enforceable BEFORE a render is accepted.

Read-only: probes the file with ffprobe; performs no writes and no external
paid calls. Exit code 0 = inside band (PASS), 1 = outside band or error (FAIL).

Usage:
    .venv/Scripts/python.exe scripts/check_runtime_band.py <video.mp4>
    .venv/Scripts/python.exe scripts/check_runtime_band.py <video.mp4> --lo 690 --hi 750
    .venv/Scripts/python.exe scripts/check_runtime_band.py <video.mp4> --json
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Channel standard finished runtime (VIDEO_RULES §10): 11.5-12.5 minutes.
DEFAULT_LO_SECONDS = 690.0  # 11.5 min
DEFAULT_HI_SECONDS = 750.0  # 12.5 min
ROOT = Path(__file__).resolve().parent.parent
EPDIR = ROOT / "episodes"


def probe_duration_seconds(path: Path) -> float:
    """Return container duration in seconds via ffprobe (raises on failure)."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(out.stdout)["format"]["duration"])


def infer_band_from_render_path(path: Path) -> tuple[float, float] | None:
    normalized = str(path).replace("\\", "/")
    match = re.search(r"episodes/(PD-\d{4}-\d{3}-[^/]+)/", normalized)
    if not match:
        return None
    manifest = EPDIR / match.group(1) / "manifest.json"
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except Exception:
        return None
    target = data.get("target_duration_minutes")
    if not target:
        return None
    if target >= 45:
        return 3300.0, 3900.0
    if target >= 20:
        return 1620.0, 1980.0
    return DEFAULT_LO_SECONDS, DEFAULT_HI_SECONDS


def main() -> int:
    ap = argparse.ArgumentParser(description="Assert render runtime is inside the target band.")
    ap.add_argument("video", help="path to the rendered .mp4")
    ap.add_argument("--lo", type=float, default=None, help="band low (seconds)")
    ap.add_argument("--hi", type=float, default=None, help="band high (seconds)")
    ap.add_argument("--json", action="store_true", help="emit a JSON result line")
    args = ap.parse_args()

    path = Path(args.video)
    if not path.is_file():
        print(f"FAIL: file not found: {path}", file=sys.stderr)
        return 1

    try:
        dur = probe_duration_seconds(path)
    except (subprocess.CalledProcessError, KeyError, ValueError) as exc:
        print(f"FAIL: could not probe duration ({exc})", file=sys.stderr)
        return 1

    inferred = infer_band_from_render_path(path)
    lo = args.lo if args.lo is not None else (inferred[0] if inferred else DEFAULT_LO_SECONDS)
    hi = args.hi if args.hi is not None else (inferred[1] if inferred else DEFAULT_HI_SECONDS)
    ok = lo <= dur <= hi
    if args.json:
        print(json.dumps({
            "check": "runtime_band",
            "video": str(path),
            "duration_seconds": round(dur, 2),
            "duration_minutes": round(dur / 60.0, 2),
            "band_seconds": [lo, hi],
            "status": "PASS" if ok else "FAIL",
        }, ensure_ascii=False))
    else:
        print(f"runtime: {dur:.2f}s = {dur / 60.0:.2f}min   "
              f"band: {lo:.0f}-{hi:.0f}s ({lo / 60:.1f}-{hi / 60:.1f}min)")
        print("RESULT:", "PASS" if ok else
              f"FAIL ({'short' if dur < lo else 'long'} by "
              f"{abs(dur - (lo if dur < lo else hi)):.1f}s)")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
