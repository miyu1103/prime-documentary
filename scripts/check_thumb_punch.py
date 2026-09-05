#!/usr/bin/env python
"""Is a thumbnail plate as loud as the ones this channel actually won with?

WHY THIS EXISTS. On 2026-08-23 an image order was written that said "deep black palette, vast
empty dark negative space". Codex obeyed it exactly and returned 29 plates that measure:

    brightness 19.1   contrast 33.4   bright pixels 0.7%   dark pixels 85.9%   saturation 11.5

Against the two plates the channel actually converted with:

    016-titan   3.14% : brightness 66.7  contrast 77.5  bright 9.8%  dark 55.0%  saturation 73.5
    017-onecoin 3.71% : brightness 49.8  contrast 70.6  bright 4.7%  dark 66.6%  saturation 36.2

The new set is a THIRD as bright, a FIFTH as saturated and has a TENTH of the bright area. It
is not a quieter version of the winners. It is a different kind of image: a dark still-life
with no light source in the frame. The owner said it looked underwhelming before any of this
was measured, and the measurement agrees.

The two winners both have a strong COLOURED PRACTICAL LIGHT inside the frame -- cyan and green
god-rays behind a submarine, a gold key light on a coin -- and a subject that fills a large
part of the picture. That is what "vast empty dark negative space" removed.

    py -3.11 scripts/check_thumb_punch.py <file-or-directory>
    py -3.11 scripts/check_thumb_punch.py --demo     # winners pass, the 29 fail

WHAT IT CANNOT DO. It measures light and colour, not meaning. A loud plate that says nothing
still fails at feed size, and only a person shrinking it to 168x94 can catch that. Run
scripts/thumb_feed_sheet.py as well and look.
"""
from __future__ import annotations

import argparse
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Bands derived from the two winners, widened so a plate does not have to imitate them.
BANDS = {
    "brightness": (42.0, 78.0),
    "contrast":   (60.0, 95.0),
    "bright_pct": (3.0, 16.0),
    "dark_pct":   (35.0, 72.0),
    "saturation": (30.0, 85.0),
}


def measure(path: Path) -> dict:
    from PIL import Image, ImageStat
    im = Image.open(path).convert("RGB").resize((320, 180))
    g = im.convert("L")
    px = list(g.getdata())
    st = ImageStat.Stat(g)
    small = im.resize((80, 45))
    sat = statistics.mean(max(c) - min(c) for c in small.getdata())
    return {
        "brightness": st.mean[0],
        "contrast": st.stddev[0],
        "bright_pct": sum(1 for v in px if v > 200) / len(px) * 100,
        "dark_pct": sum(1 for v in px if v < 40) / len(px) * 100,
        "saturation": sat,
    }


def verdict(m: dict) -> list[str]:
    out = []
    for k, (lo, hi) in BANDS.items():
        v = m[k]
        if v < lo:
            out.append(f"{k} {v:.1f} < {lo}")
        elif v > hi:
            out.append(f"{k} {v:.1f} > {hi}")
    return out


def run(paths: list[Path]) -> int:
    files = []
    for p in paths:
        files.extend(sorted(p.rglob("*.png")) + sorted(p.rglob("*.jpg")) if p.is_dir() else [p])
    if not files:
        print("no images"); return 1
    bad = 0
    print(f"{'file':34s} {'bright':>7s} {'contr':>7s} {'lit%':>6s} {'dark%':>6s} {'sat':>6s}  verdict")
    for f in files:
        m = measure(f)
        fails = verdict(m)
        bad += bool(fails)
        name = f"{f.parent.name}/{f.stem}"[-34:]
        print(f"{name:34s} {m['brightness']:7.1f} {m['contrast']:7.1f} {m['bright_pct']:6.1f} "
              f"{m['dark_pct']:6.1f} {m['saturation']:6.1f}  "
              + ("PASS" if not fails else "FAIL: " + "; ".join(fails)))
    print(f"\n{len(files) - bad} of {len(files)} inside the winners' bands")
    return 1 if bad else 0


def demo() -> int:
    """Prove the bands separate the winners from the flat set."""
    win = [ROOT / "episodes/PD-2026-016-titan/09_package/thumbnail.selected.v002.png",
           ROOT / "episodes/PD-2026-017-onecoin/09_package/thumbnail.selected.v008.png"]
    flat = Path(r"E:\pd-media\05_visuals\thumbs")
    ok = True
    for p in win:
        if not p.exists():
            print("missing winner", p); ok = False; continue
        f = verdict(measure(p))
        print(("PASS " if not f else "FAIL ") + p.parent.parent.name + ("" if not f else f"  {f}"))
        if f:
            ok = False
    if flat.exists():
        fs = sorted(flat.rglob("*.png"))
        failed = sum(1 for f in fs if verdict(measure(f)))
        print(f"the 2026-08-23 set: {failed} of {len(fs)} FAIL")
        if fs and failed < len(fs) * 0.8:
            print("the bands are not separating anything -- they are decoration"); ok = False
    print("demo: bands separate the winners from the flat set" if ok else "demo: FAILED")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", type=Path)
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    if not a.paths:
        ap.error("give a file or a directory, or --demo")
    return run(a.paths)


if __name__ == "__main__":
    sys.exit(main())
