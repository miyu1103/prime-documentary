#!/usr/bin/env python3
r"""Independent PER-WINDOW flat-spot gate — catches 紙芝居 / frozen stretches that a
motion_energy *average* can hide.

WHY THIS EXISTS (EP34 rolin §5/§7). `motion_energy` (check_final_acceptance.check_motion_energy)
floors the BODY's *within-shot mean / p10* — a single aggregate over the whole body. A render can
clear that average and STILL contain a dead 6-12s slideshow stretch, because a lot of genuine
motion elsewhere pulls the mean up. The owner keeps seeing exactly that ("アニメがまた少ない /
紙芝居"). This gate measures SUSTAINED motion PER SLIDING WINDOW so a local flat spot fails even when
the global average is healthy. It is deliberately layered on top of motion_energy, not a replacement.

WHAT IT ENFORCES (EP34 §5 cadence AND-definition + §7 sustained-motion floor):
  1. 12s WINDOW FLOOR (§5.1, §7): every sliding 12s body window must carry within-shot sustained
     motion >= WINDOW_12S_MIN (8). "within-shot" = boundary ForcefulCut spikes are EXCLUDED (a hard
     cut is a huge one-frame inter-frame difference that would otherwise inflate a frozen window).
  2. NO STATIC-STILLS-ONLY 12s WINDOW (§5.2): every 12s window must contain at least one sustained
     motion entity (>= 1 kinetic second). A window with ZERO kinetic seconds is a static-stills-only
     window and FAILS.
  3. NO STATIC HOLD > 4s (§5.3, §7): a run of consecutive frames whose motion stays below a
     near-still threshold for longer than STATIC_HOLD_MAX_S (4.0s) is a frozen hold and FAILS (the
     timestamp is reported so a human can jump to it).
  4. 60s KINETIC COVERAGE (§5): every sliding 60s body window must have kinetic coverage
     >= KINETIC_COVERAGE_MIN (0.40 -> >= 24s of the 60s actually moving).

It measures motion the SAME WAY as the existing gate so the numbers are directly comparable: it
reuses scripts/measure_motion_energy.per_frame_yavg (ffmpeg tblend=difference -> signalstats YAVG,
0..255) and the same cut-masking helpers (keep_mask / cut_times_from_film / detect_spike_times,
CUT_GUARD_FRAMES=8). fps comes from ffprobe.

BODY definition. Like check_final_acceptance, the designed-calm bookends are excluded so they are not
scored as slideshow: when the episode's remotion/src/data/<slug>_film.json is resolvable, the body is
the contiguous span AFTER the cold-open hook + gold BrandOpening title and BEFORE the trailing
BrandEndcard outro — [hookSeconds + BOOKEND_OP_SEC, dur - BOOKEND_ED_SEC]. When the film-data cannot
be resolved (e.g. a synthetic fixture or an ad-hoc --render), the WHOLE video is analyzed and the
report says so.

Read-only. Probes the mp4 with ffmpeg/ffprobe; no writes, no paid calls, no upload.

Usage:
  .venv/Scripts/python.exe scripts/check_flat_windows.py --ep PD-2026-034-rolin
  .venv/Scripts/python.exe scripts/check_flat_windows.py --ep PD-2026-034-rolin --render H:/.../final.mp4
  .venv/Scripts/python.exe scripts/check_flat_windows.py --render some.mp4        # ad-hoc, whole video

Exit 0 = PASS, non-zero = FAIL (or a hard error such as a missing / unmeasurable render).

check_final_acceptance can wire this as a HARD media gate via its _ext_gate() helper; evaluate(epdir,
render) returns the stable check-dict contract (check / ok / hard / reason / skipped / ...).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
EPDIR = ROOT / "episodes"

# --------------------------------------------------------------------------- #
# Threshold constants (documented). All on the measure_motion_energy YAVG scale #
# (0..255 mean inter-frame pixel change). Calibration reference points:         #
#   slideshow episode body mean ~3.5  ;  dynamic MotionSample body mean ~46.6   #
#   (from check_final_acceptance's motion_energy calibration).                  #
#   treatment optical-flow bands (EP34 §7): low-speed depth dolly ~7-10,        #
#   dual-layer parallax ~9-13, playhead/object-move/particles ~14-20,           #
#   L3 physics-sim / crowd particles ~14-24.                                    #
# --------------------------------------------------------------------------- #
WINDOW_12S_S = 12.0             # §5.1/§7 sliding-window length (seconds)
WINDOW_12S_HOP_S = 1.0          # slide granularity — overlapping windows catch a flat spot that a
                                # non-overlapping 12s boundary (motion_energy's segment_means) straddles
WINDOW_12S_MIN = 8.0            # §5.1/§7: a 12s window's within-shot SUSTAINED motion must clear this
                                # (>> slideshow 3.5; a slow depth dolly ~7-10 alone barely clears, which
                                # is why §7 also requires an active co-motion layer — measured elsewhere)
WINDOW_TRIM_TOP_FRAC = 0.05     # per window, drop the top 5% of frames before averaging -> "sustained"
                                # value (removes any residual boundary-transition spike the cut-mask missed)
WINDOW_MIN_KEPT_S = 4.0         # a window must retain this many un-masked seconds to be judged (else it is
                                # a hyper-cut region -> reported, not silently skipped)

STATIC_HOLD_MAX_S = 4.0         # §5.3/§7: no frozen still held longer than this
NEAR_STILL_YAVG = 2.0           # a frame with inter-frame change below this is "near-still". A truly frozen
                                # still / solid color emits YAVG ~0 (identical decoded frames); even a slow
                                # Ken Burns / depth dolly sits ~7-10, so 2.0 cleanly separates a genuine
                                # freeze from slow-but-alive motion (no false freeze flag on live content).

KINETIC_WINDOW_S = 60.0         # §5: 60s coverage window
KINETIC_WINDOW_HOP_S = 5.0      # slide granularity for 60s windows
KINETIC_COVERAGE_MIN = 0.40     # §5: >= 40% of the 60s (>= 24s) must be kinetic
KINETIC_YAVG = 8.0              # a SECOND counts "kinetic" if its within-shot local motion >= this. Same
                                # scale as WINDOW_12S_MIN: slideshow (3.5) is non-kinetic, real object
                                # movement / parallax / particles (9-20) is kinetic.

# Bookend spans excluded from the body (match check_final_acceptance BOOKEND_OP_SEC / BOOKEND_ED_SEC so
# the two gates score the same designed-calm regions out).
BOOKEND_OP_SEC = 3.5            # gold BrandOpening title (lands after the hook)
BOOKEND_ED_SEC = 9.0            # BrandEndcard outro (trailing, designed calm)


# --------------------------------------------------------------------------- #
# reuse measure_motion_energy (identical motion measurement + cut-masking)     #
# --------------------------------------------------------------------------- #
def _load_mme():
    """Import scripts/measure_motion_energy.py so YAVG + cut-masking match the existing gate."""
    spec = importlib.util.spec_from_file_location(
        "measure_motion_energy", str(Path(__file__).resolve().parent / "measure_motion_energy.py"))
    if spec is None or spec.loader is None:
        raise ImportError("measure_motion_energy.py not found next to this script")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_json(p: Path) -> Optional[dict]:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 - missing/corrupt -> treat as absent
        return None


def ffprobe_fps(path: Path) -> float:
    """Video-stream frame rate (frames/sec) from r_frame_rate, defaulting to 30."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=r_frame_rate", "-of", "default=nw=1:nk=1", str(path)],
            capture_output=True, text=True, check=True)
        txt = out.stdout.strip()
        if "/" in txt:
            num, den = txt.split("/", 1)
            return float(num) / float(den) if float(den) else 30.0
        return float(txt) if txt else 30.0
    except Exception:  # noqa: BLE001
        return 30.0


def ffprobe_duration(path: Path) -> Optional[float]:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
            capture_output=True, text=True, check=True)
        return float(json.loads(out.stdout)["format"]["duration"])
    except Exception:  # noqa: BLE001
        return None


def resolve_render(epdir: Path, override: Optional[str]) -> Optional[Path]:
    """Explicit --render wins; else the newest 09_package/final_delivery.v*.json final_video
    (mirrors check_final_acceptance.resolve_render)."""
    if override:
        return Path(override)
    for p in reversed(sorted(epdir.glob("09_package/final_delivery.v*.json"))):
        d = _load_json(p) or {}
        fv = d.get("final_video")
        if fv:
            return Path(str(fv).replace("file://", ""))
    return None


def resolve_body(epdir: Path, dur: float) -> tuple[float, float, Optional[dict], str]:
    """Return (body_lo, body_hi, film_dict_or_None, note).

    With film-data: body = [hookSeconds + OP, dur - ED] (hook cold-open + gold BrandOpening title +
    trailing BrandEndcard excluded). Without it: the whole video is analyzed (note says so)."""
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", epdir.name) if epdir else ""
    fdata = ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"
    film = _load_json(fdata) if fdata.is_file() else None
    if film is not None:
        hook = float(film.get("hookSeconds") or 0.0)
        lo = hook + BOOKEND_OP_SEC
        hi = max(lo + 1.0, dur - BOOKEND_ED_SEC)
        return lo, min(hi, dur), film, (f"body [{lo:.1f}s, {min(hi, dur):.1f}s] "
                                        f"(hook {hook:.1f}s + OP {BOOKEND_OP_SEC:.1f}s + "
                                        f"ED {BOOKEND_ED_SEC:.1f}s excluded, from {fdata.name})")
    return 0.0, dur, None, f"whole video [0.0s, {dur:.1f}s] (no film-data for slug '{slug}'; bookends not excluded)"


# --------------------------------------------------------------------------- #
# per-window analysis                                                          #
# --------------------------------------------------------------------------- #
def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _per_second_local(y: list[float], fps: float, keep: list[bool],
                      lo: float, hi: float) -> dict[int, float]:
    """Within-shot local motion per integer second in [lo, hi): mean of that second's KEPT
    (cut-masked) frames. Seconds fully inside a masked cut zone (no kept frames) count as 0 (a cut
    boundary is a transition, not sustained kinetic content)."""
    n = len(y)
    out: dict[int, float] = {}
    for k in range(int(lo), int(hi)):
        i0, i1 = max(0, int(k * fps)), min(n, int((k + 1) * fps))
        kv = [y[i] for i in range(i0, i1) if keep[i]]
        out[k] = _mean(kv)  # 0.0 when no kept frames
    return out


def _static_holds(y: list[float], fps: float, lo: float, hi: float) -> list[dict[str, float]]:
    """Runs of consecutive frames (raw, in body) below NEAR_STILL_YAVG lasting > STATIC_HOLD_MAX_S.
    Raw (not cut-masked): a genuine freeze is a span of identical frames (YAVG ~0); a hard cut is a
    HIGH spike that naturally ends the run. Returns [{start, dur}] for over-limit holds."""
    n = len(y)
    i0, i1 = max(0, int(lo * fps)), min(n, int(hi * fps))
    holds: list[dict[str, float]] = []
    run_start: Optional[int] = None
    for i in range(i0, i1):
        if y[i] < NEAR_STILL_YAVG:
            if run_start is None:
                run_start = i
        else:
            if run_start is not None:
                dur = (i - run_start) / fps
                if dur > STATIC_HOLD_MAX_S:
                    holds.append({"start": run_start / fps, "dur": dur})
                run_start = None
    if run_start is not None:
        dur = (i1 - run_start) / fps
        if dur > STATIC_HOLD_MAX_S:
            holds.append({"start": run_start / fps, "dur": dur})
    return holds


def _windows_12s(y: list[float], fps: float, keep: list[bool], lo: float, hi: float,
                 local_by_sec: dict[int, float]) -> list[dict[str, Any]]:
    """Sliding 12s windows over the body. Each: within-shot SUSTAINED value (kept frames, top
    WINDOW_TRIM_TOP_FRAC dropped) + kinetic-second count. Returns [{start, end, sustained,
    kinetic_seconds, kept_s, judged}] in time order."""
    n = len(y)
    min_kept = int(WINDOW_MIN_KEPT_S * fps)
    starts: list[float] = []
    t = lo
    last = max(lo, hi - WINDOW_12S_S)
    while t < last - 1e-6:
        starts.append(round(t, 3))
        t += WINDOW_12S_HOP_S
    starts.append(round(last, 3))
    wins: list[dict[str, Any]] = []
    for s in starts:
        e = min(hi, s + WINDOW_12S_S)
        i0, i1 = max(0, int(s * fps)), min(n, int(e * fps))
        kv = sorted(y[i] for i in range(i0, i1) if keep[i])
        judged = len(kv) >= min_kept
        if kv:
            cut = max(1, int(len(kv) * (1.0 - WINDOW_TRIM_TOP_FRAC)))
            sustained = _mean(kv[:cut])
        else:
            sustained = 0.0
        kin = sum(1 for k in range(int(s), int(e)) if local_by_sec.get(k, 0.0) >= KINETIC_YAVG)
        wins.append({"start": s, "end": e, "sustained": sustained, "kinetic_seconds": kin,
                     "kept_s": len(kv) / fps, "judged": judged})
    return wins


def _windows_60s(local_by_sec: dict[int, float], lo: float, hi: float) -> list[dict[str, Any]]:
    """Sliding 60s windows over the body; each carries kinetic coverage = kinetic seconds / seconds."""
    secs = sorted(local_by_sec)
    if not secs:
        return []
    starts: list[float] = []
    t = lo
    last = max(lo, hi - KINETIC_WINDOW_S)
    while t < last - 1e-6:
        starts.append(round(t, 3))
        t += KINETIC_WINDOW_HOP_S
    starts.append(round(last, 3))
    wins: list[dict[str, Any]] = []
    for s in starts:
        e = min(hi, s + KINETIC_WINDOW_S)
        wsecs = [k for k in secs if s <= k < e]
        if not wsecs:
            continue
        kin = sum(1 for k in wsecs if local_by_sec[k] >= KINETIC_YAVG)
        wins.append({"start": s, "end": e, "coverage": kin / len(wsecs),
                     "kinetic_s": kin, "span_s": len(wsecs)})
    return wins


# --------------------------------------------------------------------------- #
# core evaluation (importable by check_final_acceptance via _ext_gate)          #
# --------------------------------------------------------------------------- #
def evaluate(epdir: Path, render: Optional[str] = None) -> dict[str, Any]:
    """Measure per-window sustained motion on the render and return the check-dict.

    Never raises on missing inputs: a missing render -> {'skipped': True}; an EXISTING but
    UNMEASURABLE render -> hard FAIL (fail-closed, matching check_final_acceptance's media gates).

    Stable keys (contract for check_final_acceptance._ext_gate): check, ok, hard, reason, skipped,
    plus flat_windows_12s / static_holds / low_coverage_60s counts and worst-offender details.
    """
    epdir = Path(epdir) if epdir else None
    path = resolve_render(epdir, render) if (epdir or render) else None
    if path is None or not Path(path).is_file():
        return {"check": "flat_windows", "ok": True, "hard": False, "skipped": True,
                "reason": f"final render not found (looked at {path}); nothing to measure"}
    path = Path(path)

    try:
        mme = _load_mme()
    except Exception as exc:  # noqa: BLE001
        return {"check": "flat_windows", "ok": False, "hard": True,
                "reason": f"measure_motion_energy unavailable ({exc}); treat as FAIL, not a silent pass"}

    dur = ffprobe_duration(path)
    if not dur or dur <= 1.0:
        return {"check": "flat_windows", "ok": False, "hard": True,
                "reason": f"could not probe a usable duration ({dur}); treat as FAIL, not a silent pass"}
    fps = ffprobe_fps(path)
    try:
        y = mme.per_frame_yavg(str(path))
    except Exception as exc:  # noqa: BLE001
        return {"check": "flat_windows", "ok": False, "hard": True,
                "reason": f"could not measure per-frame motion ({exc}); treat as FAIL, not a silent pass"}
    if not y:
        return {"check": "flat_windows", "ok": False, "hard": True,
                "reason": "no per-frame YAVG parsed (ffmpeg tblend/signalstats unavailable?); "
                          "treat as FAIL, not a silent pass"}

    body_lo, body_hi, film, body_note = resolve_body(epdir, dur) if epdir else (0.0, dur, None,
                                                                                f"whole video [0.0s, {dur:.1f}s] (ad-hoc --render)")
    body_hi = min(body_hi, len(y) / fps)
    if body_hi - body_lo < WINDOW_12S_S:
        # too short to slide a 12s window -> analyze whatever body exists, note it
        body_lo, body_hi = 0.0, min(dur, len(y) / fps)
        body_note += " [body < 12s -> analyzed whole clip]"

    cut_times = mme.cut_times_from_film(film) or mme.detect_spike_times(y, fps)
    keep = mme.keep_mask(len(y), fps, cut_times)
    local_by_sec = _per_second_local(y, fps, keep, body_lo, body_hi)

    wins12 = _windows_12s(y, fps, keep, body_lo, body_hi, local_by_sec)
    wins60 = _windows_60s(local_by_sec, body_lo, body_hi)
    holds = _static_holds(y, fps, body_lo, body_hi)

    judged12 = [w for w in wins12 if w["judged"]]
    flat12 = [w for w in judged12 if w["sustained"] < WINDOW_12S_MIN]
    static_only = [w for w in judged12 if w["kinetic_seconds"] == 0]
    low_cov = [w for w in wins60 if w["coverage"] < KINETIC_COVERAGE_MIN]

    problems: list[str] = []
    if flat12:
        worst = min(flat12, key=lambda w: w["sustained"])
        problems.append(f"{len(flat12)}/{len(judged12)} 12s window(s) sustained < {WINDOW_12S_MIN:.0f} "
                        f"(worst {worst['sustained']:.1f} @ {worst['start']:.0f}s)")
    if static_only:
        w = static_only[0]
        problems.append(f"{len(static_only)} static-stills-only 12s window(s) "
                        f"(0 kinetic seconds; first @ {w['start']:.0f}s)")
    if holds:
        w = max(holds, key=lambda h: h["dur"])
        problems.append(f"{len(holds)} static hold(s) > {STATIC_HOLD_MAX_S:.0f}s "
                        f"(longest {w['dur']:.1f}s @ {w['start']:.0f}s)")
    if low_cov:
        w = min(low_cov, key=lambda x: x["coverage"])
        problems.append(f"{len(low_cov)} 60s window(s) kinetic coverage < {KINETIC_COVERAGE_MIN*100:.0f}% "
                        f"(worst {w['coverage']*100:.0f}% @ {w['start']:.0f}s)")

    ok = not problems
    reason = ("clean: every 12s window sustained >= {:.0f}, no static-stills-only window, "
              "no hold > {:.0f}s, every 60s window kinetic coverage >= {:.0f}%".format(
                  WINDOW_12S_MIN, STATIC_HOLD_MAX_S, KINETIC_COVERAGE_MIN * 100)
              if ok else "flat/frozen stretches: " + "; ".join(problems))

    return {
        "check": "flat_windows", "ok": ok, "hard": True, "reason": reason,
        "render": str(path), "fps": round(fps, 3), "duration_s": round(dur, 2),
        "body": body_note, "cut_boundaries": len(cut_times),
        "windows_12s": len(judged12), "flat_windows_12s": len(flat12),
        "static_stills_only_windows": len(static_only),
        "static_holds": len(holds), "windows_60s": len(wins60), "low_coverage_60s": len(low_cov),
        # worst offenders (timestamps) so a human can jump straight to the flat spot
        "worst_12s": sorted(({"start": w["start"], "sustained": round(w["sustained"], 2),
                              "kinetic_seconds": w["kinetic_seconds"]} for w in judged12),
                            key=lambda w: w["sustained"])[:8],
        "worst_60s": sorted(({"start": w["start"], "coverage": round(w["coverage"], 3)} for w in wins60),
                            key=lambda w: w["coverage"])[:5],
        "holds": sorted(({"start": round(h["start"], 1), "dur": round(h["dur"], 1)} for h in holds),
                        key=lambda h: -h["dur"])[:8],
        "problems": problems,
    }


# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #
def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("FLAT-WINDOW REPORT (per-window sustained motion)")
    print("=" * 78)
    print(f"  render        : {r.get('render')}")
    print(f"  duration/fps  : {r.get('duration_s')}s @ {r.get('fps')}fps   cuts masked: {r.get('cut_boundaries')}")
    print(f"  {r.get('body')}")
    print(f"  thresholds    : 12s window sustained >= {WINDOW_12S_MIN:.0f}, no hold > {STATIC_HOLD_MAX_S:.0f}s, "
          f"60s coverage >= {KINETIC_COVERAGE_MIN*100:.0f}%  (near-still < {NEAR_STILL_YAVG:.1f}, kinetic >= {KINETIC_YAVG:.0f} YAVG)")
    print(f"  12s windows   : {r.get('windows_12s')} judged, {r.get('flat_windows_12s')} below floor, "
          f"{r.get('static_stills_only_windows')} static-stills-only")
    print(f"  static holds  : {r.get('static_holds')} over {STATIC_HOLD_MAX_S:.0f}s")
    print(f"  60s windows   : {r.get('windows_60s')} judged, {r.get('low_coverage_60s')} below coverage floor")
    if r.get("worst_12s"):
        print("\n  worst 12s windows (lowest sustained motion first):")
        print("    start |  sustained | kinetic_s")
        print("    ------+------------+----------")
        for w in r["worst_12s"]:
            flag = "  <-- FLAT" if w["sustained"] < WINDOW_12S_MIN else ""
            so = "  <-- STATIC-STILLS-ONLY" if w["kinetic_seconds"] == 0 else ""
            print(f"    {w['start']:>5.0f} | {w['sustained']:>10.2f} | {w['kinetic_seconds']:>8}{flag}{so}")
    if r.get("holds"):
        print("\n  static holds (frozen stretches > 4s):")
        for h in r["holds"]:
            print(f"    {h['dur']:>5.1f}s frozen @ {h['start']:.1f}s  <-- jump here")
    if r.get("worst_60s"):
        print("\n  worst 60s windows (lowest kinetic coverage first):")
        for w in r["worst_60s"]:
            flag = "  <-- LOW COVERAGE" if w["coverage"] < KINETIC_COVERAGE_MIN else ""
            print(f"    @ {w['start']:>5.0f}s : {w['coverage']*100:>3.0f}% kinetic{flag}")
    print("\n" + "-" * 78)
    if r["ok"]:
        print("  RESULT: PASS — sustained motion holds in every window; no frozen slideshow stretch")
    else:
        print("  RESULT: FAIL")
        for p in r["problems"]:
            print(f"    - {p}")
    print("-" * 78)


def main(argv: Optional[list[str]] = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(
        description="Per-window flat-spot gate: FAIL if any 12s/60s body window goes flat or a still "
                    "is held > 4s (catches 紙芝居 a motion_energy average misses).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=None, help="episode slug or number (e.g. PD-2026-034-rolin or 34)")
    ap.add_argument("--render", default=None, help="explicit path to the final .mp4 (else from final_delivery)")
    ap.add_argument("--json", action="store_true", help="also print the raw result dict as JSON")
    args = ap.parse_args(argv)

    epdir: Optional[Path] = None
    if args.ep:
        cand = EPDIR / args.ep
        if cand.is_dir():
            epdir = cand
        elif args.ep.isdigit():
            hits = sorted(EPDIR.glob(f"PD-*-{int(args.ep):03d}-*"))
            epdir = hits[0] if hits else None
        if epdir is None and args.render is None:
            print(f"[ERROR] episode dir not found for --ep {args.ep}")
            return 2

    if epdir is None and args.render is None:
        print("[ERROR] provide --ep and/or --render")
        return 2

    r = evaluate(epdir, render=args.render)
    _print_report(r)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))

    if r.get("skipped"):
        return 3  # could not measure (missing render) -> non-zero, clear message above
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
