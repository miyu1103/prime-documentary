#!/usr/bin/env python3
"""PREFLIGHT gate: are the SOURCE stills too dark to survive `check_image_cut_luma`?

`check_image_cut_luma.py` measures the finished mp4. By then the stills are baked in and the
only remedy is another full render — which is how EP34 burned three passes chasing "the
darkness" before finding its cause. This measures the same quantity on the PNGs, before a
frame is rendered, so a too-dark image set is caught while it is still cheap to fix (lift in
the compositor, or fix the generation brief).

Thresholds are taken from `check_image_cut_luma.py` so the two cannot drift apart. The one
deliberate difference: the run limit here is stricter by one, because consecutive SOURCE
stills usually become consecutive CUTS, and landing exactly on the acceptance limit leaves no
margin for the cut list to make it worse.

Measured on EP60 at first run: 38 of 179 images (21.2%) below the floor, against a 12% cap.

    py -3.11 scripts/check_source_image_luma.py PD-2026-060-surfside
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def _pd_media_root() -> Path:
    """The media root, resolved -- never assumed.

    FIXED 2026-08-22. This file hardcoded H:/pd-media. That drive stopped being enumerated by
    Windows around the 2026-08-16 reboot and config/storage.local.json was repointed to E:\pd-media
    on 2026-08-17. Rule 14: no OS-absolute path is a source of truth. The literal below is kept only
    as a last-resort fallback so an unconfigured checkout behaves as it used to instead of crashing.
    """
    import json as _json
    _cfg = Path(__file__).resolve().parents[1] / "config" / "storage.local.json"
    try:
        return Path(_json.loads(_cfg.read_text(encoding="utf-8"))["roots"]["media"]["path"])
    except Exception:
        return Path("H:/pd-media")


PD_MEDIA = _pd_media_root()


ROOT = Path(__file__).resolve().parents[1]

DARK_YAVG = 45.0        # same constant as check_image_cut_luma.DARK_YAVG
DARK_FRAC_MAX = 0.12    # same cap
DARK_RUN_MAX = 3        # acceptance allows 4; one tighter here, see docstring
MIN_MEASURED = 20       # below this the set is a stub, not an image plan
THUMB = (320, 180)      # measuring a downscale is ~40x faster and moves the mean <0.5


def _image_dirs(epdir: Path) -> list[Path]:
    """Where an episode's stills actually live, render-truth first."""
    short = epdir.name.split("-")[-1]
    cands = [
        ROOT / "remotion" / "public" / short / "img",
        epdir / "04_scenes" / "generated_images" / "codex_v001",
        epdir / "04_scenes" / "generated_images",
        PD_MEDIA / "assets" / "ai" / short,
    ]
    return [d for d in cands if d.is_dir()]


def _luma(path: Path) -> float | None:
    try:
        from PIL import Image
    except ImportError:
        return None
    try:
        im = Image.open(path).convert("L")
        im.thumbnail(THUMB)
        px = im.tobytes()
        return sum(px) / len(px) if px else None
    except Exception:
        return None


def measure(epdir: Path) -> dict:
    """Mean luma of every still, plus the three quantities the acceptance gate cares about."""
    dirs = _image_dirs(epdir)
    if not dirs:
        return {"skipped": True, "reason": "no image directory yet"}
    src = dirs[0]
    pngs = sorted(p for p in src.glob("*.png") if not p.stem.endswith("_depth"))
    if len(pngs) < MIN_MEASURED:
        return {"skipped": True,
                "reason": f"only {len(pngs)} stills in {src} (need >= {MIN_MEASURED})"}

    rows: list[tuple[str, float]] = []
    for p in pngs:
        v = _luma(p)
        if v is None:
            return {"skipped": True, "reason": "Pillow unavailable or images unreadable"}
        rows.append((p.stem, v))

    dark = [(n, v) for n, v in rows if v < DARK_YAVG]
    frac = len(dark) / len(rows)

    def _ord(name: str) -> tuple:
        m = re.match(r"([A-Za-z]+)(\d+)", name)
        return (m.group(1), int(m.group(2))) if m else (name, 0)

    run = best = 0
    best_at = ""
    for n, v in sorted(rows, key=lambda r: _ord(r[0])):
        if v < DARK_YAVG:
            run += 1
            if run > best:
                best, best_at = run, n
        else:
            run = 0

    vals = sorted(v for _, v in rows)
    median = vals[len(vals) // 2]
    return {"skipped": False, "dir": str(src), "measured": len(rows),
            "dark": len(dark), "dark_fraction": round(frac, 3),
            "median_luma": round(median, 1),
            "min_luma": round(vals[0], 1), "max_luma": round(vals[-1], 1),
            "longest_dark_run": best, "longest_dark_run_ends_at": best_at,
            "darkest": [{"id": n, "luma": round(v, 1)}
                        for n, v in sorted(dark, key=lambda x: x[1])[:15]]}


def evaluate(epdir: Path) -> dict:
    """Preflight adapter: {ok, hard, reason, skipped}."""
    m = measure(Path(epdir))
    if m.get("skipped"):
        return {"ok": True, "hard": False, "skipped": True, "reason": m["reason"]}
    problems = []
    if m["dark_fraction"] > DARK_FRAC_MAX:
        problems.append(
            f"{m['dark']}/{m['measured']} stills below luma {DARK_YAVG:.0f} "
            f"= {m['dark_fraction']*100:.1f}% (cap {DARK_FRAC_MAX*100:.0f}%)")
    if m["longest_dark_run"] > DARK_RUN_MAX:
        problems.append(
            f"{m['longest_dark_run']} consecutive dark stills ending at "
            f"{m['longest_dark_run_ends_at']} (cap {DARK_RUN_MAX})")
    if problems:
        darkest = ", ".join(f"{d['id']}={d['luma']}" for d in m["darkest"][:5])
        return {"ok": False, "hard": True, "skipped": False,
                "reason": "; ".join(problems) + f". Darkest: {darkest}. "
                          "Lift in the compositor or fix the generation brief -- "
                          "check_image_cut_luma will fail the render otherwise."}
    return {"ok": True, "hard": True, "skipped": False,
            "reason": f"{m['measured']} stills, median luma {m['median_luma']}, "
                      f"{m['dark_fraction']*100:.1f}% dark, longest run "
                      f"{m['longest_dark_run']}"}


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode", help="episode slug, e.g. PD-2026-060-surfside")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    epdir = ROOT / "episodes" / a.episode
    if not epdir.is_dir():
        print(f"episode not found: {epdir}", file=sys.stderr)
        return 2
    m = measure(epdir)
    r = evaluate(epdir)
    if a.json:
        print(json.dumps({"measure": m, "evaluate": r}, ensure_ascii=False, indent=2))
    else:
        if m.get("skipped"):
            print(f"SKIP  {m['reason']}")
            return 0
        print(f"dir            {m['dir']}")
        print(f"measured       {m['measured']} stills")
        print(f"luma           median {m['median_luma']} / min {m['min_luma']} / max {m['max_luma']}")
        print(f"dark (<{DARK_YAVG:.0f})     {m['dark']} = {m['dark_fraction']*100:.1f}%  "
              f"(cap {DARK_FRAC_MAX*100:.0f}%)")
        print(f"longest run    {m['longest_dark_run']}  (cap {DARK_RUN_MAX})")
        if m["darkest"]:
            print("darkest        " + ", ".join(f"{d['id']}={d['luma']}" for d in m["darkest"][:10]))
        print(f"\n{'PASS' if r['ok'] else 'FAIL'}  {r['reason']}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
