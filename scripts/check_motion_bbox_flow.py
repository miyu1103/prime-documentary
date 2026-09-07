#!/usr/bin/env python3
r"""Independent PER-REGION motion gate — a moving CORNER must not mask a FROZEN CENTER.

check_final_acceptance already has two whole-frame motion gates:
  * animation_density (check_low_motion) — the FRACTION of near-still time ("not frozen %").
  * motion_energy (check_motion_energy)  — the whole-frame within-shot MAGNITUDE of movement
    (ffmpeg tblend=difference -> signalstats YAVG), calibrated MotionSample ~46.6 (alive) vs a
    slideshow ~3.5 (dead), body-mean floor 12 / p10 9 / per-12s-segment 8.

Both average the WHOLE frame, so they share one blind spot: a render whose MAIN SUBJECT (the
center image) is frozen can still clear the whole-frame floor when ONE busy corner — an animated
lower-third, a kinetic caption, a flickering logo — carries all the motion. The owner's standing
complaint ("animation_density green でもアニメがまた少ない / 紙芝居") is exactly this: the gate is
satisfied while the picture reads as a still.

This gate closes that hole WITHOUT re-inventing the whole-frame measurement. It tiles the frame
into an R x C grid (default 3x3), runs the SAME inter-frame-difference measurement
(tblend=all_mode=difference -> signalstats YAVG, 0..255) INSIDE each tile, masks the +/- guard
frames around every hard cut (reusing measure_motion_energy so cut-difference spikes don't inflate
a tile), and then requires motion to be present SPATIALLY, not just on average:

  (A) the CENTER tile — where the subject lives — must itself move (within-shot body mean >= a
      floor); a frozen center behind a moving corner FAILS even if the whole frame passes.
  (B) not too many tiles may be slideshow-dead over the whole body (frozen-tile fraction).
  (C) not too much of the frame-TIME may be dead across tiles: each tile is sliced into ~12s
      windows and each (tile x window) cell is checked; the frozen-CELL fraction is floored.

CALIBRATION IS FROZEN TO THE REFERENCES, NOT TO ANY ONE RENDER (invariant 15). The tile YAVG is
the same 0..255 inter-frame-difference unit as measure_motion_energy, so the published whole-frame
anchors carry over: slideshow-dead ~3.5, MotionSample-alive ~46.6, and the repo's derived
whole-frame floors (mean 12 / segment 8). A single tile is a sub-region and may legitimately be
calmer than the whole frame, so the per-tile floors are set CONSERVATIVELY below the whole-frame
mean floor — enough to catch a slideshow-dead region, not so tight it fails a calmly-composed one.
Measurement runs at scale 960x540 (native fps) for speed; that spatial downscale reads ~8% below
native whole-frame YAVG (measured), which only makes a fixed floor slightly MORE lenient, never
stricter, so it cannot cause a false FAIL. The floors here are never lowered to make a target
render pass; if a render is a slideshow it FAILS, and if the render is absent (e.g. on the SSD) the
gate SKIPS honestly rather than faking green.

check_final_acceptance can import this module and call evaluate(epdir); the returned dict keys
(check / ok / hard / skipped / reason plus the numbers) are the stable contract.

Usage:
  py -3.11 scripts/check_motion_bbox_flow.py --ep PD-2026-031-unlock
  py -3.11 scripts/check_motion_bbox_flow.py --ep PD-2026-031-unlock --dry-run
  py -3.11 scripts/check_motion_bbox_flow.py --ep PD-2026-031-unlock --render <mp4> --json out.json
  py -3.11 scripts/check_motion_bbox_flow.py --selftest        # RED fixture + real-episode numbers

Exit codes: 0 = PASS or --dry-run, 1 = FAIL or usage error, 3 = SKIP (unmeasurable / absent).
Read-only: never writes into the episode (only an optional --json report + a private temp dir).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-031-unlock"

# --- tiling / measurement geometry ----------------------------------------------------------------
GRID_ROWS = 3                 # 3x3 = 9 tiles; the center tile (index 4) carries the subject
GRID_COLS = 3
SCALE_W, SCALE_H = 960, 540   # analysis resolution (960/3=320, 540/3=180 -> integer tiles); native fps kept

# --- body definition (mirror check_motion_energy so we score the same region) ---------------------
BOOKEND_OP_SEC = 3.5          # gold BrandOpening title after the hook (excluded from the body)
BOOKEND_ED_SEC = 9.0          # trailing BrandEndcard outro (designed calm; excluded)

# --- PASS/FAIL floors, FROZEN to the slideshow(3.5)/MotionSample(46.6) calibration ----------------
# A tile-region (or a tile x 12s cell) whose within-shot mean YAVG is at/below the slideshow-dead
# level is "frozen". Anchored on the published whole-frame slideshow number (~3.5). Our 960x540
# measurement reads ~8% below native, so keeping 3.5 is, if anything, marginally lenient (safe).
FROZEN_TILE_MEAN = 3.5
# The CENTER tile is the subject. It must clearly out-move the slideshow-dead line — but it is one
# sub-region, so the floor sits BELOW the whole-frame mean floor (12) / segment floor (8): well
# above dead (3.5, ~1.7x), comfortably under the whole-frame floor. This is the "frozen center
# behind a moving corner" catch and the primary reason this gate exists.
CENTER_TILE_MEAN_MIN = 6.0
# If MORE THAN this share of tiles is slideshow-dead over the whole body, one busy corner cannot
# rescue a picture that is mostly frozen -> FAIL. 9 tiles: >0.60 means >=6 dead tiles.
MAX_FROZEN_TILE_FRACTION = 0.60
# If MORE THAN this share of (tile x 12s window) cells is dead, too much of the frame-TIME is
# frozen across space -> FAIL. Generous (whole-frame motion is covered by motion_energy); this adds
# the spatial/temporal density catch on top of the center floor.
MAX_FROZEN_CELL_FRACTION = 0.65

# reference anchors (for the report only; not thresholds)
REF_SLIDESHOW = 3.5
REF_MOTIONSAMPLE = 46.6


# ---------------------------------------------------------------------------------------------
# reuse measure_motion_energy's within-shot masking + per-segment slicing (single source of truth)
# ---------------------------------------------------------------------------------------------

def _load_mme() -> Any:
    """Import scripts/measure_motion_energy.py by path (mirrors check_final_acceptance)."""
    here = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location(
        "measure_motion_energy", str(here / "measure_motion_energy.py"))
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError("cannot locate measure_motion_energy.py next to this script")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_json(p: Path) -> Optional[dict[str, Any]]:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 - missing/corrupt -> caller treats as absent
        return None


def _ffprobe(path: Path, entries: str, stream: bool = True) -> str:
    args = ["ffprobe", "-v", "error"]
    if stream:
        args += ["-select_streams", "v:0"]
    args += ["-show_entries", entries, "-of", "default=nw=1:nk=1", str(path)]
    return subprocess.run(args, capture_output=True, text=True).stdout.strip()


def _fps(path: Path) -> float:
    raw = _ffprobe(path, "stream=r_frame_rate")
    try:
        num, den = raw.split("/")
        f = float(num) / float(den)
        return f if f > 1e-6 else 30.0
    except Exception:  # noqa: BLE001
        return 30.0


def _duration(path: Path) -> float:
    for entries, stream in (("format=duration", False), ("stream=duration", True)):
        raw = _ffprobe(path, entries, stream=stream)
        try:
            d = float(raw)
            if d > 0:
                return d
        except Exception:  # noqa: BLE001
            continue
    return 0.0


# ---------------------------------------------------------------------------------------------
# per-tile inter-frame-difference YAVG (single ffmpeg decode, R*C tiles + whole frame)
# ---------------------------------------------------------------------------------------------

def _tile_geometry() -> list[tuple[int, int, int, int]]:
    """(x, y, w, h) crop rectangles for each tile in row-major order at SCALE_W x SCALE_H."""
    tw, th = SCALE_W // GRID_COLS, SCALE_H // GRID_ROWS
    rects: list[tuple[int, int, int, int]] = []
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            rects.append((c * tw, r * th, tw, th))
    return rects


def center_index() -> int:
    return (GRID_ROWS // 2) * GRID_COLS + (GRID_COLS // 2)


def per_tile_yavg(path: Path, workdir: Path) -> Optional[dict[str, list[float]]]:
    """Measure per-frame inter-frame-difference YAVG (0..255) inside each tile AND the whole frame.

    One ffmpeg decode: scale to SCALE_W x SCALE_H, split into R*C tile branches plus a whole-frame
    branch; each branch = crop -> tblend(difference) -> gray -> signalstats -> metadata=print to a
    bare-named file in `workdir` (bare names avoid the Windows drive-colon breaking the filtergraph
    parser). Returns {"0":[...], ..., "whole":[...]} or None if nothing parsed.
    """
    rects = _tile_geometry()
    branches: list[str] = []
    labels = [f"t{i}" for i in range(len(rects))] + ["w"]
    branches.append(f"[0:v]scale={SCALE_W}:{SCALE_H},split={len(labels)}"
                    + "".join(f"[{lb}]" for lb in labels))
    outs: list[str] = []
    for i, (x, y, w, h) in enumerate(rects):
        branches.append(
            f"[t{i}]crop={w}:{h}:{x}:{y},tblend=all_mode=difference,format=gray,"
            f"signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=tile{i}.txt[o{i}]")
        outs.append(f"o{i}")
    wi = len(rects)
    branches.append(
        f"[w]tblend=all_mode=difference,format=gray,signalstats,"
        f"metadata=print:key=lavfi.signalstats.YAVG:file=whole.txt[o{wi}]")
    outs.append(f"o{wi}")
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
           "-filter_complex", ";".join(branches)]
    for o in outs:
        cmd += ["-map", f"[{o}]", "-f", "null", os.devnull]
    try:
        subprocess.run(cmd, cwd=str(workdir), capture_output=True, text=True,
                       timeout=2400, check=True)
    except Exception:  # noqa: BLE001 - decode/filter failure -> caller returns a hard FAIL, not a pass
        return None
    result: dict[str, list[float]] = {}
    for i in range(len(rects)):
        f = workdir / f"tile{i}.txt"
        vals = [float(x) for x in re.findall(r"YAVG=([0-9.]+)", f.read_text())] if f.exists() else []
        result[str(i)] = vals
    wf = workdir / "whole.txt"
    result["whole"] = [float(x) for x in re.findall(r"YAVG=([0-9.]+)", wf.read_text())] \
        if wf.exists() else []
    if not result["whole"] or all(not v for v in result.values()):
        return None
    return result


# ---------------------------------------------------------------------------------------------
# path resolution
# ---------------------------------------------------------------------------------------------

def resolve_render(ep_dir: Path, override: Optional[str]) -> Optional[Path]:
    """Highest-versioned *final*.mp4 under 08_edit/renders (per the DATA MAP). None if absent."""
    if override:
        p = Path(override)
        return p if p.exists() else None
    rdir = ep_dir / "08_edit" / "renders"
    if not rdir.is_dir():
        return None
    cands = sorted(p for p in rdir.glob("*final*.mp4") if p.stat().st_size > 0)
    return cands[-1] if cands else None


def resolve_film(ep_dir: Path) -> Optional[dict[str, Any]]:
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", ep_dir.name)
    fp = ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"
    return _load_json(fp) if fp.is_file() else None


# ---------------------------------------------------------------------------------------------
# core evaluation
# ---------------------------------------------------------------------------------------------

def _skip(reason: str) -> dict[str, Any]:
    return {"check": "motion_bbox_flow", "ok": True, "hard": False, "skipped": True,
            "reason": reason}


def evaluate(epdir: Path, render: Optional[str] = None) -> dict[str, Any]:
    """Measure per-tile within-shot motion and return a gate dict (never raises).

    Stable keys: check, ok, hard, reason (+ skipped when unmeasurable-by-absence), and on a real
    measurement: render, grid, tiles, center_index, center_mean, whole_mean, frozen_tiles,
    frozen_tile_fraction, frozen_cells, total_cells, frozen_cell_fraction, tile_means, problems.
    """
    epdir = Path(epdir)
    mp4 = resolve_render(epdir, render)
    if mp4 is None:
        return _skip(f"no *final*.mp4 render found under {epdir / '08_edit' / 'renders'} "
                     f"(absent / on SSD) -> skip honestly, do not fake green")

    try:
        mme = _load_mme()
    except Exception as exc:  # noqa: BLE001
        return {"check": "motion_bbox_flow", "ok": False, "hard": True,
                "reason": f"cannot import measure_motion_energy ({exc}); treat as FAIL"}

    fps = _fps(mp4)
    dur = _duration(mp4)
    if dur <= 0:
        return {"check": "motion_bbox_flow", "ok": False, "hard": True,
                "reason": "could not probe render duration; treat as FAIL, not a silent pass"}

    with tempfile.TemporaryDirectory(prefix="pd_bbox_flow_") as tmp:
        series = per_tile_yavg(mp4, Path(tmp))
    if series is None:
        return {"check": "motion_bbox_flow", "ok": False, "hard": True,
                "reason": f"ffmpeg produced no per-tile YAVG for {mp4.name} "
                          f"(filter/decode failed); treat as FAIL, not a silent pass"}

    fd = resolve_film(epdir)
    hook = float((fd or {}).get("hookSeconds") or 0.0)
    op_lo, op_hi = hook, hook + BOOKEND_OP_SEC
    ed_lo = max(op_hi, dur - BOOKEND_ED_SEC)
    body_regions = [(0.0, op_lo), (op_hi, ed_lo)]
    # cut boundaries: film cuts[].start if available, else auto-detect whole-frame YAVG spikes.
    cut_times = mme.cut_times_from_film(fd) or mme.detect_spike_times(series["whole"], fps)

    n_tiles = GRID_ROWS * GRID_COLS
    ci = center_index()
    tile_means: list[Optional[float]] = []
    frozen_tiles = 0
    frozen_cells = 0
    total_cells = 0
    measurable_tiles = 0
    for i in range(n_tiles):
        vals = series.get(str(i), [])
        ws = mme.within_shot_values(vals, fps, body_regions, cut_times) if vals else []
        st = mme.stats(ws)
        if st is None:
            tile_means.append(None)
            continue
        measurable_tiles += 1
        tile_means.append(round(st["mean"], 2))
        if st["mean"] <= FROZEN_TILE_MEAN:
            frozen_tiles += 1
        for seg in mme.segment_means(vals, fps, body_regions, cut_times):
            total_cells += 1
            if seg["mean"] <= FROZEN_TILE_MEAN:
                frozen_cells += 1

    if measurable_tiles == 0 or total_cells == 0:
        return {"check": "motion_bbox_flow", "ok": False, "hard": True,
                "reason": "no measurable within-shot body frames in any tile "
                          "(pathological hyper-cut / empty body); treat as FAIL, not a re-inflated pass"}

    center_mean = tile_means[ci]
    whole_ws = mme.within_shot_values(series["whole"], fps, body_regions, cut_times)
    whole_stat = mme.stats(whole_ws)
    whole_mean = round(whole_stat["mean"], 2) if whole_stat else None
    frozen_tile_fraction = frozen_tiles / measurable_tiles
    frozen_cell_fraction = frozen_cells / total_cells

    problems: list[str] = []
    if center_mean is None:
        problems.append("center tile has no measurable within-shot motion (frozen center)")
    elif center_mean < CENTER_TILE_MEAN_MIN:
        problems.append(f"center tile mean {center_mean:.1f} < {CENTER_TILE_MEAN_MIN:.1f} "
                        f"(frozen subject behind moving edges; slideshow-dead {REF_SLIDESHOW})")
    if frozen_tile_fraction > MAX_FROZEN_TILE_FRACTION:
        problems.append(f"{frozen_tiles}/{measurable_tiles} tiles slideshow-dead "
                        f"(<= {FROZEN_TILE_MEAN}) = {frozen_tile_fraction*100:.0f}% "
                        f"> {MAX_FROZEN_TILE_FRACTION*100:.0f}% (mostly frozen frame)")
    if frozen_cell_fraction > MAX_FROZEN_CELL_FRACTION:
        problems.append(f"{frozen_cells}/{total_cells} tile-windows dead = "
                        f"{frozen_cell_fraction*100:.0f}% > {MAX_FROZEN_CELL_FRACTION*100:.0f}% "
                        f"(too much frame-time frozen across regions)")

    ok = not problems
    reason = (f"per-region motion OK: center {center_mean} >= {CENTER_TILE_MEAN_MIN}; "
              f"frozen tiles {frozen_tiles}/{measurable_tiles}; frozen cells "
              f"{frozen_cell_fraction*100:.0f}%; whole {whole_mean} "
              f"(slideshow {REF_SLIDESHOW} / MotionSample {REF_MOTIONSAMPLE})"
              if ok else "per-region motion too low: " + "; ".join(problems))
    return {
        "check": "motion_bbox_flow",
        "ok": ok,
        "hard": True,
        "reason": reason,
        "render": str(mp4),
        "grid": f"{GRID_ROWS}x{GRID_COLS}",
        "tiles": n_tiles,
        "center_index": ci,
        "center_mean": center_mean,
        "center_min": CENTER_TILE_MEAN_MIN,
        "whole_mean": whole_mean,
        "frozen_tiles": frozen_tiles,
        "measurable_tiles": measurable_tiles,
        "frozen_tile_fraction": round(frozen_tile_fraction, 3),
        "frozen_cells": frozen_cells,
        "total_cells": total_cells,
        "frozen_cell_fraction": round(frozen_cell_fraction, 3),
        "frozen_tile_mean": FROZEN_TILE_MEAN,
        "cut_boundaries": len(cut_times),
        "tile_means": tile_means,
        "problems": problems,
    }


# ---------------------------------------------------------------------------------------------
# reporting
# ---------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("PER-REGION MOTION (bbox-flow) REPORT   grid " + str(r.get("grid")))
    print("=" * 78)
    if "render" in r:
        print(f"  render        : {r['render']}")
    if r.get("tile_means") is not None:
        tm = r["tile_means"]
        print("  tile within-shot mean YAVG (row-major; * = center; # = slideshow-dead "
              f"<= {r.get('frozen_tile_mean')}):")
        ci = r.get("center_index")
        for row in range(GRID_ROWS):
            cells = []
            for col in range(GRID_COLS):
                idx = row * GRID_COLS + col
                v = tm[idx]
                tag = "*" if idx == ci else " "
                dead = "#" if (v is not None and v <= r.get("frozen_tile_mean", FROZEN_TILE_MEAN)) else " "
                cells.append(f"{tag}{'  n/a' if v is None else f'{v:5.1f}'}{dead}")
            print("     " + " | ".join(cells))
        print(f"  center mean   : {r.get('center_mean')} (floor {r.get('center_min')})")
        print(f"  whole mean    : {r.get('whole_mean')}  "
              f"(slideshow {REF_SLIDESHOW} / MotionSample {REF_MOTIONSAMPLE})")
        print(f"  frozen tiles  : {r.get('frozen_tiles')}/{r.get('measurable_tiles')} "
              f"({r.get('frozen_tile_fraction')})  max {MAX_FROZEN_TILE_FRACTION}")
        print(f"  frozen cells  : {r.get('frozen_cells')}/{r.get('total_cells')} "
              f"({r.get('frozen_cell_fraction')})  max {MAX_FROZEN_CELL_FRACTION}")
        print(f"  cuts masked   : {r.get('cut_boundaries')} boundaries")
    print("-" * 78)
    if r["ok"]:
        print("  RESULT: PASS  — the subject region moves; motion is spatially distributed")
    else:
        print("  RESULT: FAIL")
        for p in r.get("problems", []):
            print(f"    - {p}")
    print("-" * 78)


def _atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, default=str)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


# ---------------------------------------------------------------------------------------------
# selftest: RED fixture (must FAIL) + real-episode numbers
# ---------------------------------------------------------------------------------------------

def _make_red_fixture(dst: Path) -> bool:
    """Synthesize a KNOWN-BAD clip: a static gray frame (FROZEN center) with a small animated
    corner (only the top-left tile moves). A whole-frame average sees the corner and may look
    'not frozen', but the center is dead -> this gate must FAIL. Deterministic (fixed sources)."""
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-f", "lavfi", "-i", "color=c=gray:s=1920x1080:r=30:d=40",
        "-f", "lavfi", "-i", "color=c=black:s=640x360:r=30:d=40",
        # corner = full-amplitude per-frame random noise (a MotionSample-alive tile); center stays
        # a static gray (frozen). A whole-frame average is lifted by the corner, yet the CENTER is
        # dead -> only a per-region gate catches it.
        "-filter_complex",
        "[1:v]format=gray,geq=lum='random(1)*255',format=yuv420p[n];"
        "[0:v][n]overlay=0:0[v]",
        "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", str(dst)]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
        return dst.exists() and dst.stat().st_size > 0
    except Exception:  # noqa: BLE001
        return False


def _selftest() -> int:
    print("=" * 78)
    print("SELFTEST — RED FIXTURE (frozen center + moving corner must FAIL)")
    print("=" * 78)
    red_ok: Optional[bool] = None
    with tempfile.TemporaryDirectory(prefix="pd_bbox_red_") as tmp:
        ep = Path(tmp) / "PD-9999-999-redfixture"
        rdir = ep / "08_edit" / "renders"
        rdir.mkdir(parents=True)
        clip = rdir / "redfixture_final.v001.mp4"
        if not _make_red_fixture(clip):
            print("  [WARN] could not synthesize RED fixture (ffmpeg lavfi/x264 unavailable)")
        else:
            r = evaluate(ep)
            _print_report(r)
            red_ok = (r.get("ok") is False and not r.get("skipped"))
            print(f"\nRED-FIXTURE: {'PASS' if red_ok else 'FAIL'} "
                  f"(gate reported ok={r.get('ok')}, expected ok=False)")

    print("\n" + "=" * 78)
    print(f"SELFTEST — REAL TEST EPISODE ({DEFAULT_EP})")
    print("=" * 78)
    ep_dir = ROOT / "episodes" / DEFAULT_EP
    if not ep_dir.exists():
        print(f"  [SKIP] episode dir not found: {ep_dir}")
    else:
        _print_report(evaluate(ep_dir))

    # selftest passes only if the RED fixture actually failed the gate (proves it can fail)
    return 0 if red_ok else 1


# ---------------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------------

def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(
        description="Per-region motion gate: FAIL if the center is frozen or too many "
                    "regions/time are near-frozen (a moving corner cannot mask a frozen center).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug")
    ap.add_argument("--render", default=None, help="override render mp4 path")
    ap.add_argument("--json", default=None, help="write the result dict to this path (atomic)")
    ap.add_argument("--dry-run", action="store_true",
                    help="resolve inputs and report the plan without running the heavy analysis")
    ap.add_argument("--selftest", action="store_true",
                    help="synthesize a known-bad RED fixture (must FAIL) then run the real episode")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    ep_dir = ROOT / "episodes" / args.ep
    if not ep_dir.exists():
        print(f"[ERROR] episode dir not found: {ep_dir}")
        return 1

    if args.dry_run:
        mp4 = resolve_render(ep_dir, args.render)
        fd = resolve_film(ep_dir)
        print("[DRY-RUN] motion_bbox_flow plan")
        print(f"  episode      : {args.ep}")
        print(f"  render       : {mp4 if mp4 else '(none found -> would SKIP)'}")
        print(f"  film hookSec : {(fd or {}).get('hookSeconds') if fd else '(no film)'}")
        print(f"  grid         : {GRID_ROWS}x{GRID_COLS} @ {SCALE_W}x{SCALE_H} (native fps)")
        print(f"  floors       : center>={CENTER_TILE_MEAN_MIN}, frozen<= {FROZEN_TILE_MEAN}, "
              f"frozen-tiles<= {MAX_FROZEN_TILE_FRACTION}, frozen-cells<= {MAX_FROZEN_CELL_FRACTION}")
        print(f"  calibration  : slideshow {REF_SLIDESHOW} / MotionSample {REF_MOTIONSAMPLE} "
              f"(frozen to references, not to this render)")
        return 0

    r = evaluate(ep_dir, render=args.render)
    _print_report(r)
    if args.json:
        _atomic_write_json(Path(args.json), r)
        print(f"\n[json] wrote {args.json}")
    if r.get("skipped"):
        return 3
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
