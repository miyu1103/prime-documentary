#!/usr/bin/env python3
r"""Measure MOTION ENERGY (how much the frame actually moves), not just 'not frozen'.

animation_density only measures the fraction of near-still time; a slow drift / Ken Burns /
weak parallax passes it while looking like a slideshow (Goodhart). This measures the average
inter-frame pixel change (a frame-difference / optical-flow proxy) via ffmpeg
`tblend=difference + signalstats(YAVG)`. Higher YAVG = more real motion. It reports the mean
and the 10th-percentile (sustained-low) energy over the BODY, so a positive LOWER BOUND can be
set — calibrated on a truly-dynamic reference (MotionSample) vs a slideshow.

EP32 §M1 hardening (2026-07-06): a hard cut / ForcefulCut transition produces a huge one-frame
inter-frame difference (a YAVG SPIKE). With ~314 hard cuts an episode, those spikes inflate the
plain body mean so a render that is FROZEN *between* cuts still clears the mean floor. Two fixes,
both implemented here and consumed by check_final_acceptance.py:
  (a) WITHIN-SHOT mean: mask +/- CUT_GUARD_FRAMES frames around every cut boundary before
      averaging, so only genuine intra-shot motion is scored. Cut boundaries are read from the
      episode's <slug>_film.json `cuts[].start` when available, else auto-detected as YAVG spikes.
  (b) PER-SEGMENT floor: slice the body into ~SEGMENT_WINDOW_S windows and require EACH window's
      within-shot mean to clear a floor, so a dead 30s stretch fails even if the global mean passes.

    py -3.11 scripts/measure_motion_energy.py <mp4> [--body-lo 11.5 --body-hi-from-end 9]
    py -3.11 scripts/measure_motion_energy.py <mp4> --film remotion/src/data/<slug>_film.json
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys

# EP32 §M1 calibration constants (shared with check_final_acceptance.py so the standalone probe
# and the gate agree). Raising/adding these only makes the motion floor STRICTER (invariant 15).
CUT_GUARD_FRAMES = 8          # mask +/-8 frames around each hard cut -> exclude the cut-difference spike
SEGMENT_WINDOW_S = 12.0       # per-segment window length (~12s) for the sustained-motion floor
SEGMENT_MIN_KEPT_SECONDS = 4.0  # a window must retain this many un-masked seconds to be scored


def per_frame_yavg(path: str) -> list[float]:
    # difference between consecutive frames -> signalstats YAVG per frame (0..255)
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", path,
         "-vf", "tblend=all_mode=difference,format=gray,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-",
         "-an", "-f", "null", os.devnull],
        capture_output=True, text=True, timeout=1800)
    return [float(x) for x in re.findall(r"lavfi\.signalstats\.YAVG=([0-9.]+)", out.stdout + out.stderr)]


def stats(vals: list[float]):
    if not vals:
        return None
    s = sorted(vals)
    n = len(s)
    mean = sum(s) / n
    p10 = s[max(0, int(0.10 * n))]
    p50 = s[n // 2]
    return {"mean": mean, "p10": p10, "p50": p50, "n": n}


# --------------------------------------------------------------------------- #
# EP32 §M1: within-shot masking + per-segment floor helpers                     #
# --------------------------------------------------------------------------- #
def cut_times_from_film(film: dict | None) -> list[float]:
    """Cut boundary start-times (seconds) from a <slug>_film.json `cuts` list."""
    times: list[float] = []
    for c in (film or {}).get("cuts") or []:
        t = c.get("start")
        if isinstance(t, (int, float)):
            times.append(float(t))
    return sorted(set(times))


def detect_spike_times(vals: list[float], fps: float, z: float = 6.0) -> list[float]:
    """Fallback cut detector when no film cut list is available: frame times whose YAVG
    spikes far above the robust baseline (a hard cut yields a large inter-frame difference).
    Uses median + z * (1.4826 * MAD) so it is not fooled by a few bright frames."""
    if not vals:
        return []
    s = sorted(vals)
    n = len(s)
    med = s[n // 2]
    mad = sorted(abs(v - med) for v in vals)[n // 2] or 1.0
    thr = med + z * 1.4826 * mad
    return [i / fps for i, v in enumerate(vals) if v > thr]


def keep_mask(n: int, fps: float, cut_times: list[float], guard: int = CUT_GUARD_FRAMES) -> list[bool]:
    """Boolean per-frame mask: False within +/-guard frames of any cut boundary."""
    keep = [True] * n
    for t in cut_times:
        c = int(round(t * fps))
        for i in range(max(0, c - guard), min(n, c + guard + 1)):
            keep[i] = False
    return keep


def within_shot_values(vals: list[float], fps: float, regions: list[tuple[float, float]],
                       cut_times: list[float], guard: int = CUT_GUARD_FRAMES) -> list[float]:
    """Body YAVG values with +/-guard frames around every cut removed (WITHIN-SHOT motion)."""
    n = len(vals)
    keep = keep_mask(n, fps, cut_times, guard)
    out: list[float] = []
    for lo, hi in regions:
        i0 = max(0, int(lo * fps))
        i1 = min(n, int(hi * fps))
        for i in range(i0, i1):
            if keep[i]:
                out.append(vals[i])
    return out


def segment_means(vals: list[float], fps: float, regions: list[tuple[float, float]],
                  cut_times: list[float], window_s: float = SEGMENT_WINDOW_S,
                  guard: int = CUT_GUARD_FRAMES) -> list[dict]:
    """Slice the body into ~window_s windows; each window's mean over its within-shot
    (cut-masked) frames. Windows retaining < SEGMENT_MIN_KEPT_SECONDS of un-masked frames are
    skipped (too little signal to judge). Returns [{start, mean, kept, n}] in time order."""
    n = len(vals)
    keep = keep_mask(n, fps, cut_times, guard)
    min_kept = int(SEGMENT_MIN_KEPT_SECONDS * fps)
    segs: list[dict] = []
    for lo, hi in regions:
        t = lo
        while t < hi - 1e-6:
            w_hi = min(hi, t + window_s)
            i0 = max(0, int(t * fps))
            i1 = min(n, int(w_hi * fps))
            kv = [vals[i] for i in range(i0, i1) if keep[i]]
            if len(kv) >= min_kept:
                segs.append({"start": round(t, 1), "mean": sum(kv) / len(kv),
                             "kept": len(kv), "n": i1 - i0})
            t = w_hi
    return segs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4")
    ap.add_argument("--fps", type=float, default=30.0)
    ap.add_argument("--body-lo", type=float, default=11.5, help="skip this many head seconds (hook+OP)")
    ap.add_argument("--body-hi-from-end", type=float, default=9.0, help="skip this many tail seconds (endcard)")
    ap.add_argument("--film", help="<slug>_film.json to read cut boundaries from (else auto-detect spikes)")
    args = ap.parse_args()
    y = per_frame_yavg(args.mp4)
    if not y:
        print("no YAVG parsed (ffmpeg filter unavailable?)"); return 1
    lo = int(args.body_lo * args.fps)
    hi = max(lo + 1, len(y) - int(args.body_hi_from_end * args.fps))
    body = y[lo:hi]
    full_s = stats(y); body_s = stats(body)
    # within-shot + per-segment (EP32 §M1)
    film = None
    if args.film and os.path.isfile(args.film):
        try:
            film = json.loads(open(args.film, encoding="utf-8").read())
        except Exception:
            film = None
    cut_times = cut_times_from_film(film) or detect_spike_times(y, args.fps)
    regions = [(args.body_lo, hi / args.fps)]
    ws_s = stats(within_shot_values(y, args.fps, regions, cut_times))
    segs = segment_means(y, args.fps, regions, cut_times)
    print(f"{os.path.basename(args.mp4)}")
    print(f"  FULL      mean={full_s['mean']:.2f} p10={full_s['p10']:.2f} p50={full_s['p50']:.2f} (frames {full_s['n']})")
    print(f"  BODY      mean={body_s['mean']:.2f} p10={body_s['p10']:.2f} p50={body_s['p50']:.2f} (frames {body_s['n']})")
    if ws_s:
        print(f"  WITHIN-SHOT mean={ws_s['mean']:.2f} p10={ws_s['p10']:.2f} p50={ws_s['p50']:.2f} "
              f"(frames {ws_s['n']}; {len(cut_times)} cut boundaries masked +/-{CUT_GUARD_FRAMES}f)")
    if segs:
        worst = min(segs, key=lambda s: s["mean"])
        print(f"  SEGMENTS  {len(segs)} x ~{SEGMENT_WINDOW_S:.0f}s; worst window mean={worst['mean']:.2f} @ {worst['start']:.0f}s")
    print("  (YAVG 0..255 of the inter-frame difference; higher = more real motion. p10 = sustained-low floor.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
