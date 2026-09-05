#!/usr/bin/env python3
"""What is still owed to each episode by the image generator, measured from disk every time.

Compares the ORDER (`episodes/_planning/EP<NN>_<slug>_CODEX_PASTE/plates*.jsonl`) against the
DELIVERY directory and against what is actually staged for the render, and prints the missing
ids. A delivery report written from memory goes stale in minutes -- on 2026-08-25 one did, in
four, while Codex was still writing files.

`staged4K` is the column that matters for the render: `remotion/public/<slug>/img` is render
truth and its floor is 3840 px on the long edge. The delivery directory on the media drive
holds Codex's own 1672x941 output and is SUPPOSED to be under that -- the upscale writes the
4K copy into the staged directory. EP85 was reported as "86 images missing" when in fact all
186 were on disk at source size and only the upscale had not run, so both numbers are printed.

    py -3.11 scripts/report_plate_delivery.py
    py -3.11 scripts/report_plate_delivery.py --slug keybridge
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path(r"E:\pd-media\05_visuals")

EPISODES = {
    "keybridge": "EP77", "colgan": "EP78", "alaska261": "EP79", "concordia": "EP80",
    "station": "EP81", "valdez": "EP82", "max737": "EP83", "threemile": "EP84",
    "katrina": "EP85",
}
ID = re.compile(r"[A-Za-z]+\d+")


def ids_in(d: Path) -> set[str]:
    if not d.is_dir():
        return set()
    out = set()
    for p in d.glob("*.png"):
        if p.stem.endswith("_depth"):
            continue
        if ID.fullmatch(p.stem):
            out.add(p.stem)
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug")
    a = ap.parse_args()

    try:
        from PIL import Image
    except ImportError:
        Image = None

    for slug, ep in EPISODES.items():
        if a.slug and slug != a.slug:
            continue
        ordered: set[str] = set()
        for f in sorted((ROOT / "episodes" / "_planning").glob(f"{ep}_{slug}_CODEX_PASTE/plates*.jsonl")):
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    ordered.add(json.loads(line)["id"])
        # later order books add ids that are not in the paste exporter's jsonl
        for md in sorted((ROOT / "episodes" / "_planning").glob(f"{ep}_{slug}_CODEX_BATCH_*.md")):
            for m in re.finditer(r"^\|\s*([A-Z]\d{3})\s*\|", md.read_text(encoding="utf-8"), re.M):
                ordered.add(m.group(1))

        delivered = ids_in(MEDIA / slug / "img")
        staged_dir = ROOT / "remotion" / "public" / slug / "img"
        staged = ids_in(staged_dir)
        rejected = ids_in(staged_dir / "rejected")

        missing = sorted(ordered - delivered - staged)
        sizes = Counter()
        if Image is not None:
            for p in sorted((MEDIA / slug / "img").glob("*.png"))[:400]:
                if p.stem.endswith("_depth") or not ID.fullmatch(p.stem):
                    continue
                sizes[Image.open(p).size] += 1
        under4k = sum(n for (w, _), n in sizes.items() if w < 3840)

        print(f"{ep} {slug:<11} ordered={len(ordered):3}  delivered={len(delivered):3}  "
              f"staged4K={len(staged):3}  rejected={len(rejected):2}  MISSING={len(missing):3}"
              + (f"  [delivery copies at source size: {under4k}]" if under4k else ""))
        if missing:
            print(f"    {', '.join(missing[:24])}{' ...' if len(missing) > 24 else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
