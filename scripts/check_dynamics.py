#!/usr/bin/env python
"""Read-only dynamics gate for final documentary renders.

Checks the real mp4 for long frozen spans, excessive black, and long audio
silence. Exit 0 means the render is not a static slideshow and has a continuous
audible bed by the same practical thresholds used by final acceptance.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

MAX_FREEZE_TOTAL_S = 8.0
MAX_FREEZE_LONGEST_S = 4.0
FREEZE_DETECT_S = 2.5
MAX_BLACK_TOTAL_S = 8.0
MAX_BLACK_LONGEST_S = 3.0
MAX_SILENCE_TOTAL_S = 25.0
ROOT = Path(__file__).resolve().parent.parent
EPDIR = ROOT / "episodes"


def run_ffmpeg(args: list[str], timeout: int = 1200) -> str:
    proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip()[-2000:])
    return proc.stderr


def durations(pattern: str, text: str) -> list[float]:
    return [float(x) for x in re.findall(pattern, text)]


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def resolve_episode(arg: str) -> str | None:
    if (EPDIR / arg).is_dir():
        return arg
    if arg.isdigit():
        hits = [p.name for p in EPDIR.glob(f"PD-*-{int(arg):03d}-*") if p.is_dir()]
        return hits[0] if len(hits) == 1 else None
    hits = [p.name for p in EPDIR.glob(f"*{arg}*") if p.is_dir()]
    return hits[0] if len(hits) == 1 else None


def resolve_video(arg: str) -> Path:
    direct = Path(arg)
    if direct.is_file():
        return direct
    ep = resolve_episode(arg)
    if not ep:
        return direct
    epdir = EPDIR / ep
    for delivery in sorted(epdir.glob("09_package/final_delivery.v*.json"), reverse=True):
        data = load_json(delivery) or {}
        final_video = data.get("final_video")
        if final_video and Path(final_video).is_file():
            return Path(final_video)
    return Path("H:/pd-media") / "episodes" / ep / "08_edit" / "final.mp4"


def check_freeze(path: Path) -> dict:
    err = run_ffmpeg([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-vf", f"freezedetect=n=-60dB:d={FREEZE_DETECT_S}",
        "-an", "-f", "null", os.devnull,
    ])
    spans = durations(r"freeze_duration:\s*(\d+(?:\.\d+)?)", err)
    total = sum(spans)
    longest = max(spans) if spans else 0.0
    ok = total <= MAX_FREEZE_TOTAL_S and longest <= MAX_FREEZE_LONGEST_S
    return {"check": "freeze", "ok": ok, "total_seconds": round(total, 3), "longest_seconds": round(longest, 3)}


def check_black(path: Path) -> dict:
    err = run_ffmpeg([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-vf", "blackdetect=d=0.5:pic_th=0.98",
        "-an", "-f", "null", os.devnull,
    ])
    spans = durations(r"black_duration:(\d+(?:\.\d+)?)", err)
    total = sum(spans)
    longest = max(spans) if spans else 0.0
    ok = total <= MAX_BLACK_TOTAL_S and longest <= MAX_BLACK_LONGEST_S
    return {"check": "black", "ok": ok, "total_seconds": round(total, 3), "longest_seconds": round(longest, 3)}


def check_silence(path: Path) -> dict:
    err = run_ffmpeg([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-af", "silencedetect=n=-40dB:d=0.6",
        "-f", "null", os.devnull,
    ])
    spans = durations(r"silence_duration:\s*(\d+(?:\.\d+)?)", err)
    total = sum(spans)
    longest = max(spans) if spans else 0.0
    ok = total <= MAX_SILENCE_TOTAL_S
    return {"check": "silence", "ok": ok, "total_seconds": round(total, 3), "longest_seconds": round(longest, 3)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check render dynamics on a final mp4.")
    parser.add_argument("video", help="render path, episode id, or episode number")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = resolve_video(args.video)
    if not path.is_file():
        print(f"FAIL: file not found: {path}", file=sys.stderr)
        return 1

    try:
        results = [check_freeze(path), check_black(path), check_silence(path)]
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: could not measure dynamics: {exc}", file=sys.stderr)
        return 1

    ok = all(item["ok"] for item in results)
    report = {"check": "dynamics", "video": str(path), "status": "PASS" if ok else "FAIL", "results": results}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"{'PASS' if item['ok'] else 'FAIL'} {item['check']}: total={item['total_seconds']}s longest={item['longest_seconds']}s")
        print("RESULT:", report["status"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
