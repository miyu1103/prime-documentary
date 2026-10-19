#!/usr/bin/env python
"""One tile per distinct SOURCE, not per sampled frame.

The shipped-frame sheets carry ~4.7 frames of every cut, which is right when you are hunting
things that appear for a moment -- an invented clip, a card landing on a face. It is the wrong
unit when you are hunting the three defects that are properties of the CLIP itself:

  * a real identifiable minor
  * scraped third-party footage (a chyron, a watermark, another production's subtitles)
  * legible personal data of a real private individual

Those are in the source or they are not. Seeing the same clip five times does not make the
answer better; seeing every clip once does. On EP57 fieldtest that is 303 sources against 1420
frames -- a 4.7x reduction with FULL source coverage, which is what makes a one-reader pass
possible at all when no more reviewers are available.

    python scripts/build_per_source_sheet.py --slug fieldtest

It picks the widest-apart frames of each source (first and last sampled), preferring the later
one, since invented content and end-cards cluster late. Reuse it for the sheets, not another
tiler: it calls build_footage_contact_sheet.build_sheet.

LIMIT, STATED PLAINLY: this cannot see a defect that appears only in the seconds between the
sampled points of a clip. It is a source-coverage pass, not a frame-coverage pass, and a review
built on it must say so.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

FRAME = re.compile(r"^(\d+)m(\d+)s_(\d+)__cut(\d+)_p(\d+)\.jpg$")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--per-sheet", type=int, default=20)
    a = ap.parse_args()

    import json

    frames_dir = ROOT / "runs" / "qc" / "shipped_frames" / a.slug / "frames"
    if not frames_dir.is_dir():
        raise SystemExit(f"no frames at {frames_dir} -- run check_shipped_frames.py --sheets-only first")

    film = json.loads((ROOT / "remotion" / "src" / "data" / f"{a.slug}_film.json")
                      .read_text(encoding="utf-8"))
    by_cut = {}
    for i, c in enumerate(film["cuts"]):
        by_cut[i] = str(c.get("src", "")).split("/")[-1]

    # group every sampled frame by the source it came from
    per_src: dict[str, list[tuple[int, Path]]] = defaultdict(list)
    orphans = 0
    for p in sorted(frames_dir.glob("*.jpg")):
        m = FRAME.match(p.name)
        if not m:
            orphans += 1
            continue
        cut = int(m.group(4))
        src = by_cut.get(cut)
        if not src:
            orphans += 1
            continue
        per_src[src].append((int(m.group(5)), p))

    print(f"[per-source] {len(per_src)} distinct source(s) across "
          f"{sum(len(v) for v in per_src.values())} sampled frame(s)"
          + (f"; {orphans} frame(s) could not be mapped to a cut" if orphans else ""))

    out = ROOT / "runs" / "qc" / "shipped_frames" / f"{a.slug}_per_source"
    if out.exists():
        shutil.rmtree(out)
    (out / "frames").mkdir(parents=True)

    picked = []
    for src in sorted(per_src):
        # the latest sampled point: invented content and end-cards cluster late in a clip
        pct, p = max(per_src[src], key=lambda t: t[0])
        dst = out / "frames" / f"{len(picked):04d}__p{pct}__{src}.jpg"
        shutil.copy2(p, dst)
        picked.append(dst)

    from build_footage_contact_sheet import build_sheet

    sheets = []
    for i in range(0, len(picked), a.per_sheet):
        chunk = picked[i:i + a.per_sheet]
        sheet = out / f"{a.slug}_per_source_{i // a.per_sheet + 1:02d}.png"
        build_sheet(chunk, sheet,
                    title=f"{a.slug} — ONE FRAME PER SOURCE "
                          f"(sheet {i // a.per_sheet + 1}, sources "
                          f"{i + 1}-{min(i + a.per_sheet, len(picked))} of {len(picked)})")
        sheets.append(sheet)
        print(f"  {sheet.name}  ({len(chunk)} source(s))")

    print(f"[per-source] {len(sheets)} sheet(s) covering ALL {len(picked)} sources -> {out}")
    print("[per-source] NOTE: source coverage, not frame coverage. A defect visible only "
          "between a clip's sampled points is out of this pass's reach; say so in the review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
