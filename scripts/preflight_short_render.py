#!/usr/bin/env python3
"""Refuse to start a Shorts render that is going to fail. Checks known render aborts.

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
  5. A referenced audio/kinetic/CTA file missing, or audio older than its line/timing contract.

Usage:
  py -3.11 scripts/preflight_short_render.py 132 133 134
  py -3.11 scripts/preflight_short_render.py 100-120 --fix-mirror
"""
from __future__ import annotations

import argparse
import json
import re
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
    # The mirror exists to keep the bundle small, but --fix-mirror only ever ADDS, so after enough
    # batches it held 175 Shorts and 58 GB - and bundling copies the whole thing, so a render died
    # with ENOSPC needing 58 GB against 43 GB free. --prune-mirror drops the Shorts not in this
    # batch; they are derived copies and --fix-mirror puts them back on demand.
    ap.add_argument("--platform", choices=["yt", "tiktok"], default="yt",
                    help="tiktok skips the 58s ceiling: that limit is YouTube Shorts' 60s rule, "
                         "and TikTok accepts up to ten minutes. 13 finished Shorts were blocked "
                         "from their TikTok render by a constraint that does not apply to TikTok.")
    ap.add_argument("--prune-mirror", action="store_true",
                    help="remove mirrored Shorts outside this batch before syncing")
    ap.add_argument("--fix-mirror", action="store_true",
                    help="re-sync public_min from public/shorts instead of just reporting it")
    a = ap.parse_args()
    platform = a.platform
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
        if s:
            gen = [p for p in s["plates"] if p.get("source") in {"GENERATE", "REUSE"}]
            for p in gen:
                img = PUB / sid / f"{sid}_{p['n']:02d}.png"
                if not img.exists():
                    problems.append(f"{sid}: plate {p['n']} has no delivered image ({img.name})")
                    continue
                if not img.with_name(img.stem + "_depth.png").exists():
                    problems.append(f"{sid}: {img.name} has no depth map - the WebGL plate will abort")
        else:
            # Shorts 33-43 predate the consolidated short_designs JSON. Their assembled
            # TypeScript is the machine contract: resolve every img('NN') reference and require
            # both the plate and its depth map. This preserves the same abort-prevention gate
            # without inventing a fake design document merely to satisfy this preflight.
            data_file = DATA / f"{sid}.ts"
            data_text = data_file.read_text(encoding="utf-8") if data_file.is_file() else ""
            # Both call shapes are in use: img('01') in the older files, and img(1) where the data
            # file pads the number itself. Reading only the quoted form declared short82 to have no
            # plate contract at all - it has 49 plates and every depth map beside them.
            legacy_refs = sorted({
                ref.zfill(2)
                for ref in re.findall(r"\bimg\(\s*['\"]?(\d+)['\"]?\s*\)", data_text)
            })
            if not legacy_refs:
                problems.append(f"{sid}: no design found and no legacy img() plate contract")
            for ref in legacy_refs:
                img = PUB / sid / f"{sid}_{ref}.png"
                if not img.exists():
                    problems.append(f"{sid}: legacy plate {ref} is missing ({img.name})")
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

        data_file = DATA / f"{sid}.ts"
        if not data_file.exists():
            problems.append(f"{sid}: not assembled (remotion/src/data/{sid}.ts missing)")
        else:
            data_text = data_file.read_text(encoding="utf-8")
            refs = set(re.findall(rf"['\"](shorts/{sid}/[^'\"]+)['\"]", data_text))
            for ref in sorted(refs):
                if not (ROOT / "remotion" / "public" / ref).is_file():
                    problems.append(f"{sid}: referenced public asset is missing: {ref}")

            audio = PUB / sid / "audio" / f"{sid}_final_mix_v002_en_us.mp3"
            timing = DATA / f"{sid}_timing.ts"
            line_files = list((ROOT / "episodes").glob(
                f"PD-2026-*/09_package/{sid}_lines.v001.json"))
            if audio.is_file() and timing.is_file():
                newer_than = [timing, *line_files]
                if any(path.stat().st_mtime > audio.stat().st_mtime for path in newer_than):
                    problems.append(f"{sid}: audio is older than its timing/line contract")
            total_match = re.search(r"TOTAL_SEC\s*=\s*([0-9.]+)",
                                    timing.read_text(encoding="utf-8") if timing.is_file() else "")
            if platform == "yt" and total_match and float(total_match.group(1)) > 58.0:
                problems.append(f"{sid}: duration {total_match.group(1)}s exceeds 58s")
        if f'"Short-{sid}-yt"' not in rtx:
            problems.append(f"{sid}: composition Short-{sid}-yt is not registered in Root.tsx")
        if f'"ShortThumb-{sid}"' not in rtx:
            problems.append(f"{sid}: cover Still ShortThumb-{sid} is not registered in Root.tsx")

    if a.prune_mirror and MIRROR.is_dir():
        keep = {f"short{n}" for n in want}
        freed = 0
        for d in [x for x in MIRROR.iterdir() if x.is_dir() and x.name not in keep]:
            freed += sum(f.stat().st_size for f in d.rglob("*") if f.is_file())
            shutil.rmtree(d)
        if freed:
            print(f"pruned {freed/1e9:.1f} GB of mirrored Shorts outside this batch")

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
