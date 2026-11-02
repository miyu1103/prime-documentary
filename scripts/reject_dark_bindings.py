#!/usr/bin/env python3
"""Measure every bound clip and permanently reject the ones that render as black.

Found 2026-08-03 on the first 8-line render: short93 carried two black holes, 1.00 s and 1.87 s.
The cause was not the assembler and not a missing file — three of its bound clips are simply dark,
measuring 0.1, 0.8 and 7.7 mean luma out of 255. The semantic index had sampled one frame at 1.2 s,
so a clip that opens on black was indexed AS black, and a black embedding sits close to every
"dark", "night" and "shadow" query on the shelf.

Scores cannot catch this: a black frame can score 0.30 against "a dark corridor". Only luminance
can. So measure the clips that were actually chosen, write the failures to the permanent reject
list, and let the binder pick again.

Usage:
  py -3.11 scripts/reject_dark_bindings.py --shorts 86-99            # report only
  py -3.11 scripts/reject_dark_bindings.py --shorts 86-99 --apply    # write the reject list
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
REJECTS = ROOT / "runs" / "footage_semantic" / "rejected_clips.txt"

# Below this the clip reads as a hole on screen rather than as dark atmosphere. The three that
# shipped holes measured 0.1, 0.8 and 7.7; the darkest clip that looked fine measured 19.6.
LUMA_FLOOR = 14.0


def mean_luma(path: str) -> float:
    """Mean luminance over the first ~2 s, 0-255. -1 if the file will not decode."""
    import numpy as np
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-frames:v", "60",
                        "-vf", "scale=32:32", "-pix_fmt", "gray", "-f", "rawvideo", "-"],
                       capture_output=True)
    a = np.frombuffer(r.stdout, dtype=np.uint8)
    return float(a.mean()) if a.size else -1.0


def parse_range(spec: str) -> set[int]:
    out: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out.update(range(int(a), int(b) + 1))
        elif part:
            out.add(int(part))
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--shorts", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--floor", type=float, default=LUMA_FLOOR)
    a = ap.parse_args()

    want = parse_range(a.shorts)
    bound: dict[str, list[str]] = {}
    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for s in d["shorts"]:
            n = int(s["short_id"].replace("short", ""))
            if n not in want:
                continue
            for p in s["plates"]:
                bf = p.get("bound_file")
                if p.get("source") == "FOOTAGE" and bf:
                    bound.setdefault(bf, []).append(f"{s['short_id']} p{p['n']:02d}")

    print(f"measuring {len(bound)} distinct bound clips")
    paths = list(bound)
    with ThreadPoolExecutor(max_workers=8) as ex:
        lumas = list(ex.map(mean_luma, paths))

    dark = [(p, l) for p, l in zip(paths, lumas) if 0 <= l < a.floor]
    broken = [(p, l) for p, l in zip(paths, lumas) if l < 0]
    dark.sort(key=lambda t: t[1])
    print(f"too dark (<{a.floor}): {len(dark)} | undecodable: {len(broken)}")
    for p, l in dark:
        print(f"  {l:5.1f}  {', '.join(bound[p])}  {Path(p).name}")
    for p, _ in broken:
        print(f"  DECODE FAIL  {', '.join(bound[p])}  {Path(p).name}")

    if not a.apply:
        print("\nreport only - pass --apply to add these to the reject list")
        return 0

    existing = []
    if REJECTS.exists():
        existing = [ln.rstrip("\n") for ln in REJECTS.read_text(encoding="utf-8").splitlines()]
    have = {ln.strip() for ln in existing if ln.strip() and not ln.startswith("#")}
    added = [p for p, _ in dark + broken if p not in have]
    if added:
        REJECTS.write_text("\n".join(existing + added) + "\n", encoding="utf-8")
    print(f"\nadded {len(added)} clips to {REJECTS.name} (now {len(have) + len(added)} total)")
    print("re-run bind_short_footage_semantic.py --apply to pick replacements")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
