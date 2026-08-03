#!/usr/bin/env python3
"""Refuse to start a Shorts render that is going to fail. Checks the four things that have failed.

Every one of these cost a full render before it was found, because Remotion only reports the
problem after the bundle is built and the first frames are attempted:

  1. A GENERATE plate with no delivered image.
  2. An image with no matching *_depth.png. Every Short plate goes through the WebGL depth
     component, so a missing map aborts the render with "Could not load ..._depth.png". 378 maps
     were missing for shorts 100-120 and 604 more for 121-165; both were found the hard way.
  3. public_min out of sync. That pruned 8.9 GB mirror exists because Remotion copies the entire
     public dir into every bundle and the real one is 262 GB — but it is a DERIVED artefact, and
     a render bundled from a stale mirror fails exactly like a missing file. It was built once
     before the depth maps existed and cost a second render.
  4. The composition not registered in Root.tsx, which fails as "composition not found" only after
     bundling.

Usage:
  py -3.11 scripts/preflight_short_render.py 132 133 134
  py -3.11 scripts/preflight_short_render.py 100-120 --fix-mirror
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
PUB = ROOT / "remotion" / "public" / "shorts"
MIRROR = ROOT / "remotion" / "public_min" / "shorts"
DATA = ROOT / "remotion" / "src" / "data"
RTX = ROOT / "remotion" / "src" / "Root.tsx"


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
    ap.add_argument("shorts", nargs="+", help="e.g. 132 133 134  or  100-120")
    ap.add_argument("--fix-mirror", action="store_true",
                    help="re-sync public_min from public/shorts instead of just reporting it")
    a = ap.parse_args()
    want: set[int] = set()
    for s in a.shorts:
        want |= parse_range(s)

    designs: dict[int, dict] = {}
    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for s in d["shorts"]:
            n = int(s["short_id"].replace("short", ""))
            if n in want:
                designs[n] = s

    rtx = RTX.read_text(encoding="utf-8")
    problems: list[str] = []
    stale_mirror: list[Path] = []

    for n in sorted(want):
        sid = f"short{n}"
        s = designs.get(n)
        if not s:
            problems.append(f"{sid}: no design found")
            continue

        gen = [p for p in s["plates"] if p.get("source") == "GENERATE"]
        for p in gen:
            img = PUB / sid / f"{sid}_{p['n']:02d}.png"
            if not img.exists():
                problems.append(f"{sid}: plate {p['n']} has no delivered image ({img.name})")
                continue
            if not img.with_name(img.stem + "_depth.png").exists():
                problems.append(f"{sid}: {img.name} has no depth map - the WebGL plate will abort")

        # Compare the WHOLE short directory, not a list of file kinds. Enumerating kinds was wrong
        # twice in a row: first it missed the staged fx/*.mp4 clips (render 404'd on fx_03.mp4),
        # then it missed short<NN>_ctathumb.jpg (404 again). The mirror is a derived copy, so the
        # only correct test is "does it contain everything the real directory does".
        for src in (PUB / sid).rglob("*"):
            if not src.is_file():
                continue
            m = MIRROR / src.relative_to(PUB)
            if not m.exists() or m.stat().st_size != src.stat().st_size:
                stale_mirror.append(src)

        if not (DATA / f"{sid}.ts").exists():
            problems.append(f"{sid}: not assembled (remotion/src/data/{sid}.ts missing)")
        if f'"Short-{sid}-yt"' not in rtx:
            problems.append(f"{sid}: composition Short-{sid}-yt is not registered in Root.tsx")
        if f'"ShortThumb-{sid}"' not in rtx:
            problems.append(f"{sid}: cover Still ShortThumb-{sid} is not registered in Root.tsx")

    if stale_mirror:
        if a.fix_mirror:
            for src in stale_mirror:
                # mirror the path RELATIVE to public/shorts so fx/ subdirectories survive; using
                # src.parent.name alone would flatten fx clips into the short's root and the
                # render would still 404 on them
                dst = MIRROR / src.relative_to(PUB)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            print(f"re-synced {len(stale_mirror)} files into the pruned mirror")
        else:
            problems.append(f"public_min is stale for {len(stale_mirror)} files "
                            f"- re-run with --fix-mirror")

    print(f"checked {len(want)} shorts")
    if not problems:
        print("PASS: safe to bundle and render")
        return 0
    print(f"\nFAIL: {len(problems)} problem(s) that would abort the render\n")
    for p in problems[:40]:
        print(f"  {p}")
    if len(problems) > 40:
        print(f"  ... and {len(problems) - 40} more")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
