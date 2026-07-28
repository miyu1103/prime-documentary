#!/usr/bin/env python3
r"""Independent per-image-cut brightness gate — catches INDIVIDUAL dark cuts.

check_body_luma() (in check_final_acceptance.py) floors the brightness of the WHOLE render:
it samples one frame every ~2s and fails only when the *median* frame is dark or too many
frames overall fall below YAVG 30. That whole-render median can PASS while the hero still
images the owner actually needs to read are each individually murky, because bright factory
b-roll (courtroom, law library, city lights) lifts the global median. The owner's recurring
complaint is exactly that: "画面が暗くて画像が見えない" — the *pictures* are too dark to see.

This gate measures brightness PER CUT instead of per render. It reads the cutlist
(remotion/src/data/<slug>_film.json `cuts[]`: each cut's start/dur/kind), maps every cut to its
absolute timestamp in the render (accounting for the canonical Hook + Bookend Opening that
CaseFilm.tsx prepends before the body — cut 0 does NOT sit at render second 0), grabs the
MID-FRAME of each cut with ffmpeg signalstats (the most-settled point, away from transition
edges), and reports how many cuts are dark. It FAILS if:

  * more than DARK_FRAC_MAX of ALL visual cuts have mean YAVG < DARK_YAVG, OR
  * more than DARK_FRAC_MAX of the hero IMAGE cuts (kind=="img") are that dark — a render can
    pad its overall fraction with bright b-roll while leaving every hero still unreadable, so
    the image cuts get their own first-class floor (this is check_*IMAGE*_cut_luma), OR
  * there is any SUSTAINED RUN of > DARK_RUN_MAX consecutive dark cuts (a concentrated dark
    stretch the owner sits through even if the global fraction looks acceptable).

Calibration (measured on the owner-flagged EP31 render unlock_final.v002.mp4, 208 cuts):
    ALL cuts   : median YAVG 46.9,  47% < 45
    IMAGE cuts : median YAVG 35.1,  76% < 45   <- the hero stills are the culprit
    FOOTAGE    : median YAVG 75.0,  27% < 45
The floor DARK_YAVG=45 with DARK_FRAC_MAX=12% flags that render decisively on both the
all-cut fraction (47% >> 12%) and the image-cut fraction (76% >> 12%).

Usage:
  py -3.11 scripts/check_image_cut_luma.py --ep PD-2026-031-unlock
  py -3.11 scripts/check_image_cut_luma.py --ep PD-2026-031-unlock --render <path.mp4>
  py -3.11 scripts/check_image_cut_luma.py --ep PD-2026-031-unlock --dry-run
  py -3.11 scripts/check_image_cut_luma.py --selftest
  py -3.11 scripts/check_image_cut_luma.py --ep PD-2026-031-unlock --json out.json

Exit codes: 0 = PASS (or --dry-run / --selftest ok), 1 = FAIL or usage error, 3 = skipped
(could not measure because the render is not in the repo, e.g. it lives on the SSD).

check_final_acceptance can import this module and call evaluate(epdir); the returned dict
({"check","ok","hard","reason", ...numbers}) is that contract — keep the keys stable.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from statistics import median
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-031-unlock"

# --- render timeline geometry (mirrors remotion/src/compositions/CaseFilm.tsx) ------------------
# CaseFilm renders: Hook (hookSeconds) -> Bookend Opening (OPENING_SEC) -> Body(cuts) -> Endcard.
# Each cut's Sequence `from` is RELATIVE to the Body start, so a cut's absolute render time is
# (hook + opening) + cut.start. OPENING_SEC is the canonical constant from components/Bookends.tsx
# (unchanging per the design spec); a film json may override it via an "openingSeconds" key.
OPENING_SEC = 3.5

# --- PASS/FAIL thresholds (calibrated on the dark EP31 render; do NOT weaken to pass a target) --
DARK_YAVG = 45.0        # a cut whose mid-frame mean luma (0..255) is below this is "too dark to read"
DARK_FRAC_MAX = 0.12    # FAIL if more than 12% of cuts (all, or image-only) are that dark
DARK_RUN_MAX = 4        # FAIL on any run of > 4 (i.e. >=5) consecutive dark cuts (sustained darkness)
MIN_MEASURED = 6        # if a present render yields fewer than this many samples, measurement failed
NO_CUTLIST_SAMPLE_SEC = 2.0   # fallback: with no film cutlist, treat one frame every ~2s as a "cut"


# ---------------------------------------------------------------------------------------------
# path / cutlist resolution
# ---------------------------------------------------------------------------------------------

def _load_json(p: Path) -> Optional[dict]:
    """Read a UTF-8 JSON file, or None if missing/malformed (never raises)."""
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 - missing/corrupt -> caller treats as absent
        return None


def _slug(ep: str) -> str:
    """PD-2026-031-unlock -> 'unlock' (everything after the PD-YYYY-NNN- prefix)."""
    parts = ep.split("-")
    return "-".join(parts[3:]) if len(parts) > 3 else ep


def resolve_film(epdir: Path, override: Optional[str]) -> Optional[Path]:
    """Locate the <slug>_film.json cutlist for this episode, or None if not present."""
    if override:
        p = Path(override)
        return p if p.exists() else None
    data_dir = ROOT / "remotion" / "src" / "data"
    direct = data_dir / f"{_slug(epdir.name)}_film.json"
    if direct.exists():
        return direct
    # fall back: any *_film.json whose episode_id matches this episode
    for cand in sorted(data_dir.glob("*_film.json")):
        d = _load_json(cand)
        if d and d.get("episode_id") == epdir.name:
            return cand
    return None


def resolve_render(epdir: Path, override: Optional[str]) -> Optional[Path]:
    """Locate the final render mp4. Prefer an explicit path, then the newest *final*.mp4 under
    08_edit/renders, then final_delivery.v*.json. Returns None if none exist in the repo (e.g. the
    render only lives on the SSD) so the caller can skip honestly."""
    if override:
        p = Path(override)
        return p if p.exists() else None
    renders = epdir / "08_edit" / "renders"
    finals = [p for p in renders.glob("*final*.mp4") if p.is_file()]
    if finals:
        # newest by version string then mtime (v002 > v001)
        return max(finals, key=lambda p: (p.name, p.stat().st_mtime))
    for fd in reversed(sorted(epdir.glob("09_package/final_delivery.v*.json"))):
        d = _load_json(fd) or {}
        fv = d.get("final_video")
        if fv:
            p = Path(str(fv).replace("file://", ""))
            if p.exists():
                return p
    return None


def build_cuts(film: Optional[dict], render_dur: float) -> tuple[list[dict[str, Any]], float, bool]:
    """Return (cuts, offset_sec, from_cutlist).

    From a film json: cuts carry absolute mid-times computed with the Hook+Opening offset.
    Without a cutlist: synthesize one pseudo-cut every NO_CUTLIST_SAMPLE_SEC across the whole
    render (offset 0) so the gate degrades honestly instead of skipping."""
    if film and isinstance(film.get("cuts"), list) and film["cuts"]:
        fps = float(film.get("fps") or 30.0)
        hook = float(film.get("hookSeconds") or 0.0)
        opening = float(film.get("openingSeconds", OPENING_SEC))
        offset = (round(hook * fps) + round(opening * fps)) / fps
        cuts: list[dict[str, Any]] = []
        for i, c in enumerate(film["cuts"]):
            start = c.get("start")
            dur = c.get("dur")
            if not isinstance(start, (int, float)) or not isinstance(dur, (int, float)):
                continue
            cuts.append({
                "index": i,
                "kind": str(c.get("kind", "?")),
                "start": float(start),
                "dur": float(dur),
                "mid": offset + float(start) + float(dur) / 2.0,
            })
        return cuts, offset, True
    # fallback: uniform sampling, each sample is a "cut"
    cuts = []
    t = NO_CUTLIST_SAMPLE_SEC / 2.0
    i = 0
    while t < render_dur:
        cuts.append({"index": i, "kind": "sample", "start": t, "dur": NO_CUTLIST_SAMPLE_SEC,
                     "mid": t})
        t += NO_CUTLIST_SAMPLE_SEC
        i += 1
    return cuts, 0.0, False


# ---------------------------------------------------------------------------------------------
# measurement
# ---------------------------------------------------------------------------------------------

def _probe_duration(path: Path) -> float:
    """Render duration in seconds (0.0 if ffprobe fails)."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, check=True).stdout.strip()
        return float(out)
    except Exception:  # noqa: BLE001
        return 0.0


def _yavg_at(path: Path, t: float) -> Optional[float]:
    """Mean luma (YAVG, 0..255) of the frame at absolute time `t`, via a fast input seek +
    single-frame signalstats. None if ffmpeg produced no reading."""
    try:
        proc = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{max(0.0, t):.3f}", "-i", str(path),
             "-frames:v", "1", "-vf", "signalstats,metadata=print:file=-", "-f", "null", "-"],
            capture_output=True, text=True, check=True)
    except Exception:  # noqa: BLE001 - one bad seek shouldn't abort the whole scan
        return None
    m = re.findall(r"lavfi\.signalstats\.YAVG=([0-9.]+)", proc.stdout + proc.stderr)
    return float(m[0]) if m else None


def _measure(path: Path, cuts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Attach a 'yavg' reading to each cut (mid-frame). Cuts with no reading are dropped."""
    out: list[dict[str, Any]] = []
    for c in cuts:
        v = _yavg_at(path, c["mid"])
        if v is not None:
            d = dict(c)
            d["yavg"] = v
            out.append(d)
    return out


def _longest_dark_run(measured: list[dict[str, Any]]) -> int:
    """Longest run of consecutive dark cuts, in render order."""
    best = run = 0
    for c in measured:
        if c["yavg"] < DARK_YAVG:
            run += 1
            best = max(best, run)
        else:
            run = 0
    return best


def _frac(part: int, whole: int) -> float:
    return part / whole if whole else 0.0


# ---------------------------------------------------------------------------------------------
# core evaluation (importable; NEVER calls sys.exit, NEVER crashes the caller)
# ---------------------------------------------------------------------------------------------

def evaluate(epdir: Path, render: Optional[str] = None, film: Optional[str] = None) -> dict[str, Any]:
    """Measure per-cut brightness and return a result dict compatible with check_final_acceptance.

    Skips honestly (ok=True, skipped=True) when the render is not in the repo. Fails closed
    (ok=False, hard=True) when the render IS present but cannot be measured — we never pass what
    we cannot see. Deterministic: no clock/random; ffmpeg readings are fixed for a fixed input.
    """
    epdir = Path(epdir)
    render_path = resolve_render(epdir, render)
    if render_path is None:
        return {"check": "image_cut_luma", "ok": True, "hard": False, "skipped": True,
                "reason": "render mp4 not in repo (likely on SSD) — nothing to measure"}

    dur = _probe_duration(render_path)
    film_path = resolve_film(epdir, film)
    film_data = _load_json(film_path) if film_path else None
    cuts, offset, from_cutlist = build_cuts(film_data, dur if dur > 0 else 1e9)
    if not cuts:
        return {"check": "image_cut_luma", "ok": False, "hard": True,
                "reason": f"no cuts to measure (film={film_path}, dur={dur:.1f}s)",
                "render": str(render_path)}

    measured = _measure(render_path, cuts)
    if len(measured) < MIN_MEASURED:
        # render exists but ffmpeg gave us almost nothing -> fail closed (do NOT fake green).
        return {"check": "image_cut_luma", "ok": False, "hard": True,
                "reason": (f"only {len(measured)}/{len(cuts)} cut frames measured "
                           f"(ffmpeg/signalstats unavailable?) — cannot verify brightness"),
                "render": str(render_path)}

    dark = [c for c in measured if c["yavg"] < DARK_YAVG]
    img = [c for c in measured if c["kind"] == "img"]
    img_dark = [c for c in img if c["yavg"] < DARK_YAVG]

    all_vals = [c["yavg"] for c in measured]
    all_frac = _frac(len(dark), len(measured))
    img_frac = _frac(len(img_dark), len(img))
    run = _longest_dark_run(measured)
    med = median(all_vals)
    img_med = median([c["yavg"] for c in img]) if img else None

    problems: list[str] = []
    if all_frac > DARK_FRAC_MAX:
        problems.append(f"{all_frac*100:.0f}% of {len(measured)} cuts < YAVG {DARK_YAVG:.0f} "
                        f"(> {DARK_FRAC_MAX*100:.0f}% dark; median {med:.0f})")
    if img and img_frac > DARK_FRAC_MAX:
        problems.append(f"{img_frac*100:.0f}% of {len(img)} HERO IMAGE cuts < YAVG {DARK_YAVG:.0f} "
                        f"(median {img_med:.0f}) — hero stills too dark to read")
    if run > DARK_RUN_MAX:
        problems.append(f"sustained dark run of {run} consecutive cuts "
                        f"(> {DARK_RUN_MAX}) — a concentrated unwatchable stretch")

    # timestamps of the darkest cuts, for the report (mm:ss @ yavg)
    dark_sorted = sorted(dark, key=lambda c: c["yavg"])
    dark_stamps = [{"cut": c["index"], "kind": c["kind"],
                    "t": round(c["mid"], 1), "yavg": round(c["yavg"], 1)}
                   for c in dark_sorted[:15]]

    ok = not problems
    return {
        "check": "image_cut_luma",
        "ok": ok,
        "hard": True,
        "reason": (f"per-cut brightness OK: median YAVG {med:.0f}, {all_frac*100:.0f}% of "
                   f"{len(measured)} cuts dark (<= {DARK_FRAC_MAX*100:.0f}%), longest dark run {run}"
                   if ok else "dark cuts: " + "; ".join(problems)),
        "render": str(render_path),
        "film": str(film_path) if film_path else None,
        "from_cutlist": from_cutlist,
        "offset_sec": round(offset, 3),
        "cuts_total": len(cuts),
        "cuts_measured": len(measured),
        "median_yavg": round(med, 1),
        "image_cuts": len(img),
        "image_median_yavg": round(img_med, 1) if img_med is not None else None,
        "dark_yavg_floor": DARK_YAVG,
        "dark_count": len(dark),
        "dark_frac": round(all_frac, 3),
        "image_dark_count": len(img_dark),
        "image_dark_frac": round(img_frac, 3),
        "longest_dark_run": run,
        "dark_stamps": dark_stamps,
    }


# ---------------------------------------------------------------------------------------------
# reporting
# ---------------------------------------------------------------------------------------------

def _mmss(t: float) -> str:
    return f"{int(t) // 60:d}:{int(t) % 60:02d}"


def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("PER-IMAGE-CUT LUMA REPORT")
    print("=" * 78)
    print(f"  render        : {r.get('render')}")
    print(f"  cutlist       : {r.get('film')}  (from_cutlist={r.get('from_cutlist')})")
    print(f"  body offset   : +{r.get('offset_sec')}s (Hook + Bookend Opening before body)")
    print(f"  cuts measured : {r.get('cuts_measured')}/{r.get('cuts_total')}")
    print(f"  median YAVG   : all {r.get('median_yavg')}   image-only {r.get('image_median_yavg')}"
          f"   (dark floor < {r.get('dark_yavg_floor')})")
    print(f"  dark cuts     : all {r.get('dark_count')}/{r.get('cuts_measured')} "
          f"({r.get('dark_frac', 0)*100:.0f}%)   "
          f"image {r.get('image_dark_count')}/{r.get('image_cuts')} "
          f"({r.get('image_dark_frac', 0)*100:.0f}%)   "
          f"[fail > {DARK_FRAC_MAX*100:.0f}%]")
    print(f"  longest run   : {r.get('longest_dark_run')} consecutive dark "
          f"[fail > {DARK_RUN_MAX}]")
    if r.get("dark_stamps"):
        print("\n  darkest cuts (timestamp @ YAVG):")
        for d in r["dark_stamps"]:
            print(f"    cut #{d['cut']:>3} {d['kind']:<7} {_mmss(d['t'])} (t={d['t']}s) "
                  f"-> YAVG {d['yavg']}")
    print("\n" + "-" * 78)
    if r["ok"]:
        print("  RESULT: PASS — individual cuts are bright enough to see")
    else:
        print(f"  RESULT: FAIL — {r['reason']}")
    print("-" * 78)


def _atomic_write_json(path: Path, obj: dict[str, Any]) -> None:
    """Write JSON atomically (temp file + os.replace) so a reader never sees a partial file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=2, default=str)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


# ---------------------------------------------------------------------------------------------
# selftest: RED fixture (known-bad -> must FAIL) then real episode numbers
# ---------------------------------------------------------------------------------------------

def _make_solid_clip(path: Path, color: str, seconds: float) -> bool:
    """Render a solid-colour test clip with ffmpeg lavfi. Returns True on success."""
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-f", "lavfi", "-i", f"color=c={color}:s=320x240:r=30:d={seconds}",
             "-pix_fmt", "yuv420p", str(path)],
            capture_output=True, check=True)
        return path.exists()
    except Exception:  # noqa: BLE001
        return False


def _selftest() -> int:
    print("=" * 78)
    print("SELFTEST — RED FIXTURE (synthetic known-bad input must report ok=False)")
    print("=" * 78)
    red_ok: Optional[bool] = None
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        ep = tmp / "PD-9999-999-redfixture"
        (ep / "08_edit" / "renders").mkdir(parents=True)
        clip = ep / "08_edit" / "renders" / "red_final.v001.mp4"
        # a fully BLACK clip = every cut mid-frame is YAVG ~0 => 100% dark, must FAIL. Use >=
        # MIN_MEASURED cuts so the fixture exercises the real dark-fraction path, not fail-closed.
        n = MIN_MEASURED + 2  # 8 cuts
        if not _make_solid_clip(clip, "black", 2.0 * n + 1):
            print("  [SETUP] ffmpeg could not synthesize the black test clip — cannot run RED fixture")
            print("RED-FIXTURE: FAIL")
            return 1
        # a matching cutlist (no Hook/Opening offset) of 2s image cuts.
        film = {"episode_id": ep.name, "fps": 30, "hookSeconds": 0, "openingSeconds": 0,
                "cuts": [{"start": 2.0 * i, "dur": 2.0, "kind": "img"} for i in range(n)]}
        film_path = tmp / "red_film.json"
        film_path.write_text(json.dumps(film), encoding="utf-8")
        r = evaluate(ep, film=str(film_path))
        red_ok = bool(r.get("ok")) and not r.get("skipped")
        print(f"  black-clip result: ok={r.get('ok')} skipped={r.get('skipped')} "
              f"reason={r.get('reason')}")
        print(f"  dark_frac={r.get('dark_frac')} image_dark_frac={r.get('image_dark_frac')} "
              f"median_yavg={r.get('median_yavg')}")
        red_pass = (r.get("ok") is False) and not r.get("skipped")
        print("RED-FIXTURE: PASS" if red_pass else "RED-FIXTURE: FAIL")

        # sanity companion: a bright (grey ~ YAVG 128) clip with the same cutlist must PASS.
        bright = ep / "08_edit" / "renders" / "bright_final.v001.mp4"
        if _make_solid_clip(bright, "gray", 2.0 * n + 1):
            rb = evaluate(ep, render=str(bright), film=str(film_path))
            print(f"  [sanity] grey-clip result: ok={rb.get('ok')} median_yavg={rb.get('median_yavg')}"
                  f" (expect PASS/bright)")

    print("\n" + "=" * 78)
    print(f"SELFTEST — REAL EPISODE ({DEFAULT_EP}) actual numbers")
    print("=" * 78)
    real_epdir = ROOT / "episodes" / DEFAULT_EP
    if not real_epdir.exists():
        print(f"  [skip] {real_epdir} not found")
        return 0 if red_pass else 1
    rr = evaluate(real_epdir)
    _print_report(rr)
    return 0 if red_pass else 1


# ---------------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------------

def main(argv: Optional[list[str]] = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(
        description="Independent per-image-cut brightness gate: FAIL if individual cuts are too dark.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug (dir under episodes/)")
    ap.add_argument("--render", default=None, help="explicit render mp4 (else newest 08_edit/renders/*final*.mp4)")
    ap.add_argument("--film", default=None, help="explicit <slug>_film.json cutlist path")
    ap.add_argument("--dry-run", action="store_true",
                    help="resolve inputs and report the plan without running ffmpeg (exit 0)")
    ap.add_argument("--json", nargs="?", const="-", default=None, metavar="PATH",
                    help="write the result dict as JSON to PATH (atomic), or '-' for stdout")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED fixture (known-bad must FAIL) then real-episode numbers")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    epdir = ROOT / "episodes" / args.ep
    if not epdir.exists():
        print(f"[ERROR] episode dir not found: {epdir}")
        return 1

    if args.dry_run:
        render_path = resolve_render(epdir, args.render)
        film_path = resolve_film(epdir, args.film)
        film_data = _load_json(film_path) if film_path else None
        dur = _probe_duration(render_path) if render_path else 0.0
        cuts, offset, from_cutlist = build_cuts(film_data, dur if dur > 0 else 1e9)
        n_img = sum(1 for c in cuts if c["kind"] == "img")
        print("[DRY-RUN] would measure per-cut brightness:")
        print(f"  episode   : {args.ep}")
        print(f"  render    : {render_path if render_path else 'NOT FOUND (would SKIP)'}")
        print(f"  duration  : {dur:.1f}s")
        print(f"  cutlist   : {film_path if film_path else 'NONE (would sample every 2s)'}")
        print(f"  from_cutlist={from_cutlist}  body_offset=+{offset:.3f}s")
        print(f"  cuts      : {len(cuts)} total ({n_img} image cuts)")
        print(f"  thresholds: dark<{DARK_YAVG:.0f} YAVG, fail if >{DARK_FRAC_MAX*100:.0f}% dark "
              f"or run >{DARK_RUN_MAX}")
        print("  (no ffmpeg measurement performed in --dry-run)")
        return 0

    r = evaluate(epdir, render=args.render, film=args.film)
    _print_report(r)
    if args.json is not None:
        if args.json == "-":
            print(json.dumps(r, indent=2, default=str))
        else:
            _atomic_write_json(Path(args.json), r)
            print(f"\n[json] wrote {args.json}")

    if r.get("skipped"):
        return 3
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
