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
import subprocess
import sys
from pathlib import Path

# Channel standard finished runtime (VIDEO_RULES §10): 11.5-12.5 minutes.
DEFAULT_LO_SECONDS = 690.0  # 11.5 min
DEFAULT_HI_SECONDS = 750.0  # 12.5 min


def probe_duration_seconds(path: Path) -> float:
    """Return container duration in seconds via ffprobe (raises on failure)."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(out.stdout)["format"]["duration"])


def main() -> int:
    ap = argparse.ArgumentParser(description="Assert render runtime is inside the target band.")
    ap.add_argument("video", help="path to the rendered .mp4")
    ap.add_argument("--lo", type=float, default=DEFAULT_LO_SECONDS, help="band low (seconds)")
    ap.add_argument("--hi", type=float, default=DEFAULT_HI_SECONDS, help="band high (seconds)")
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

    ok = args.lo <= dur <= args.hi
    if args.json:
        print(json.dumps({
            "check": "runtime_band",
            "video": str(path),
            "duration_seconds": round(dur, 2),
            "duration_minutes": round(dur / 60.0, 2),
            "band_seconds": [args.lo, args.hi],
            "status": "PASS" if ok else "FAIL",
        }, ensure_ascii=False))
    else:
        print(f"runtime: {dur:.2f}s = {dur / 60.0:.2f}min   "
              f"band: {args.lo:.0f}-{args.hi:.0f}s ({args.lo / 60:.1f}-{args.hi / 60:.1f}min)")
        print("RESULT:", "PASS" if ok else
              f"FAIL ({'short' if dur < args.lo else 'long'} by "
              f"{abs(dur - (args.lo if dur < args.lo else args.hi)):.1f}s)")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
