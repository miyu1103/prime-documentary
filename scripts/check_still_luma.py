"""Fail a film BEFORE the render when a still it cuts in is too dark to be a picture.

Why this exists. EP76 morandi burned a full 2h36m render and died on its POST-RENDER GATE
with 4.43 s of black at 170.9-175.3 s. The cause was cut-0037, whose source was V010.png --
a plate the design ordered as "a plain matte near-black surface with faint horizontal grain,
evenly lit, entirely empty". The plate was correct. It was declared in `mandatory_stills`,
which means "this picture must reach the screen", so the builder cut it in as a standalone
4.4 s picture cut with nothing drawn over it.

Nothing in the pre-render path looks at still luma:
  * check_motion_saturation measures motion/ only -- it never sees a png
  * the pre-render gate counts cuts and shares
  * check_spec_satisfied asks whether mandatory stills reached a cut, not what is in them
A PIL mean-luma pass over the stills actually referenced by the film found it in one command.

The same run also carried V026.png, "a plain white ground with a single fine horizontal line
ruled across it, nothing else in frame", cut in at cut-0072. The black gate cannot see that
one at all, so this check is two-sided: a still that is nearly all black OR nearly all white
is a backdrop, not a picture, and a backdrop alone on screen is a hole in the film.

    py -3.11 scripts/check_still_luma.py --slug morandi
    py -3.11 scripts/check_still_luma.py --film remotion/src/data/morandi_film.json
    py -3.11 scripts/check_still_luma.py --selftest

Exit 0 = every still in a cut is a picture. Exit 1 = at least one is not.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageStat

ROOT = Path(__file__).resolve().parent.parent

# Measured on morandi's 52 distinct stills-in-cuts: the offender sat at mean 20.08 and the next
# darkest picture at 69.69. 45 is the midpoint of that gap and comfortably clear of both, so a
# genuinely dark night plate still passes while an empty ground does not.
DARK_MEAN = 45.0
BRIGHT_MEAN = 225.0
# A picture has variation in it. An evenly-lit empty ground has almost none, which is what
# separates "a dark photograph" from "a black card": V010 measured stdev 3.6.
FLAT_STDEV = 12.0


def measure(path: Path) -> tuple[float, float]:
    with Image.open(path) as im:
        g = im.convert("L")
        st = ImageStat.Stat(g)
        return st.mean[0], st.stddev[0]


def stills_in_cuts(film: dict) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for c in film.get("cuts") or []:
        src = str(c.get("src") or "")
        if src.lower().endswith(".png"):
            out.setdefault(Path(src).name, []).append(str(c.get("id")))
    return out


def resolve(name: str, slug: str) -> Path | None:
    for base in (ROOT / "remotion" / "public" / slug / "img",
                 ROOT / "remotion" / "public" / slug):
        p = base / name
        if p.is_file():
            return p
    return None


def run(film_path: Path, slug: str) -> int:
    film = json.loads(film_path.read_text(encoding="utf-8"))
    used = stills_in_cuts(film)
    if not used:
        print(f"[still-luma] {slug}: no still is cut into this film -- nothing to measure")
        return 0

    rows, missing = [], []
    for name, cuts in used.items():
        p = resolve(name, slug)
        if p is None:
            missing.append(name)
            continue
        mean, stdev = measure(p)
        rows.append((mean, stdev, name, cuts))
    rows.sort()

    bad = []
    for mean, stdev, name, cuts in rows:
        why = None
        if mean < DARK_MEAN and stdev < FLAT_STDEV:
            why = (f"mean {mean:.1f} < {DARK_MEAN} and stdev {stdev:.1f} < {FLAT_STDEV} "
                   f"-- an empty dark ground, not a picture")
        elif mean > BRIGHT_MEAN and stdev < FLAT_STDEV:
            why = (f"mean {mean:.1f} > {BRIGHT_MEAN} and stdev {stdev:.1f} < {FLAT_STDEV} "
                   f"-- an empty light ground, not a picture")
        if why:
            bad.append((name, cuts, why))

    print(f"[still-luma] {slug}: {len(rows)} distinct still(s) in cuts, "
          f"darkest {rows[0][0]:.1f}, brightest {rows[-1][0]:.1f}")
    for name, cuts, why in bad:
        print(f"  [FAIL] {name} in {', '.join(cuts)}: {why}")
    if missing:
        print(f"  [WARN] {len(missing)} still(s) named by a cut are not on disk: {missing[:4]}")

    if bad:
        print(f"[still-luma] {slug}: NOT SAFE TO RENDER -- {len(bad)} backdrop(s) are cut in as "
              f"pictures. Take them out of the still pool AND out of mandatory_stills (a plate "
              f"designed to hold nothing cannot satisfy a rule that means 'this picture must "
              f"reach the screen'), then rebuild the film.")
        return 1
    print(f"[still-luma] {slug}: every still in a cut is a picture. "
          f"This says nothing about WHAT it shows -- open the contact sheets.")
    return 0


def selftest() -> int:
    """Prove the check rejects a bad input and accepts a good one. Both directions."""
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        cases = [
            ("black_ground.png", Image.new("RGB", (256, 144), (18, 18, 20)), True),
            ("white_ground.png", Image.new("RGB", (256, 144), (243, 243, 240)), True),
            ("dark_photo.png", None, False),     # dark but textured -- must PASS
            ("normal_photo.png", None, False),
        ]
        import random
        rnd = random.Random(7)
        for name, img, should_fail in cases:
            if img is None:
                base = 30 if name.startswith("dark") else 130
                img = Image.new("RGB", (256, 144))
                img.putdata([(max(0, min(255, base + rnd.randint(-60, 60))),) * 3
                             for _ in range(256 * 144)])
            img.save(d / name)
            mean, stdev = measure(d / name)
            flagged = ((mean < DARK_MEAN or mean > BRIGHT_MEAN) and stdev < FLAT_STDEV)
            verdict = "PASS" if flagged == should_fail else "SELFTEST FAILED"
            if flagged != should_fail:
                ok = False
            print(f"  {verdict}  {name:18s} mean={mean:6.1f} stdev={stdev:5.1f} "
                  f"flagged={flagged} expected={should_fail}")
    print("[still-luma] selftest:", "all cases behaved as specified" if ok else "BROKEN")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug")
    ap.add_argument("--film", type=Path)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.slug and not a.film:
        ap.error("give --slug or --film")
    film = a.film or (ROOT / "remotion" / "src" / "data" / f"{a.slug}_film.json")
    if not film.is_file():
        print(f"[still-luma] no film json at {film}")
        return 1
    slug = a.slug or film.stem.replace("_film", "")
    return run(film, slug)


if __name__ == "__main__":
    sys.exit(main())
