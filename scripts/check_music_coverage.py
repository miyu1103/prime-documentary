#!/usr/bin/env python3
r"""Independent music-coverage gate — catches long MUSIC-DEAD stretches before they ship.

A finished PD film must have a CONTINUOUS music bed under the whole runtime. When the bed
drops out for a long stretch the film reads as amateur (a bare voice over silence, the "抜けた"
feeling the owner keeps flagging). The existing check_final_acceptance.check_bgm only measures
TOTAL SILENCE with silencedetect at -40 dB — but during narration the mix is NEVER silent, so a
narration-only-yet-continuous-speech section (music removed, voice still talking) sails straight
through it. This gate measures the thing that check actually cannot: whether the LOW-FREQUENCY
MUSIC BED itself is present, everywhere, independent of the speech on top of it.

METHOD (why it measures the real intent, not a proxy):
A cinematic/documentary music bed carries sustained energy in a low sub-band (bass, kick, sub
pads, drones) at roughly 30-90 Hz. Human narration carries almost NO sustained energy that low
(a male fundamental sits ~100-150 Hz and is intermittent). So the 30-90 Hz band is a clean
"is the bed playing?" probe that a talking voice cannot fake. Empirically, on the real EP31
render the 30-90 Hz per-3s-window level sits at about -22 dBFS, while the episode's speech-only
narration master (a real negative control) never exceeds -32 dBFS in that same band. A window
threshold of -30 dBFS therefore separates "bed present" from "voice only / silence" with margin.
PD masters are all 2-pass loudness-normalized to -14 LUFS, so this absolute low-band floor is
stable across episodes.

Per 3-second window we compute the 30-90 Hz RMS in dBFS and mark the window music-present if it
clears the floor. We then report:
  * coverage%  = music-present windows / effective windows
  * largest_gap_s = longest run of consecutive music-dead windows
An intended ENDING FADE (a music-dead run that reaches the end of the film) is forgiven up to
FADE_FORGIVE_S; anything longer than that counts as a real gap. We FAIL if coverage is below
MIN_COVERAGE or any (non-fade) gap exceeds MAX_GAP_S.

The gate is deterministic (no clock/random), read-only (never writes into the episode), and
FAILS CLOSED: if the render cannot be decoded to a low band it reports ok=False rather than a
silent pass. When the render itself is not in the repo (e.g. it lives on the SSD) it SKIPS
honestly with ok=True/hard=False/skipped=True so it never crashes or fakes green for the caller.

Usage:
  py -3.11 scripts/check_music_coverage.py --ep PD-2026-031-unlock
  py -3.11 scripts/check_music_coverage.py --ep PD-2026-031-unlock --render <path.mp4>
  py -3.11 scripts/check_music_coverage.py --ep PD-2026-031-unlock --dry-run
  py -3.11 scripts/check_music_coverage.py --selftest        # RED fixture + real-episode numbers

Exit codes: 0 = PASS (or --dry-run), 1 = FAIL / usage error, 3 = SKIP (artifact not measurable).

check_final_acceptance can import this module and call evaluate(epdir); the returned dict keys
(check / ok / hard / reason / skipped / coverage_pct / largest_gap_s / ...) are that contract.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-031-unlock"

# --- measurement parameters (calibrated on the real EP31 render + its speech-only master) --------
LOW_BAND_LO_HZ = 30          # music bed sub-band lower edge (below speech fundamentals)
LOW_BAND_HI_HZ = 90          # music bed sub-band upper edge (below male fundamental ~100-150 Hz)
DECODE_SR = 1000             # Hz; Nyquist 500 >> 90 Hz band, tiny to decode for an 11-min film
WINDOW_S = 3.0               # analysis window (spec: per-3s window)
MUSIC_FLOOR_DBFS = -30.0     # window 30-90 Hz RMS above this => bed present (speech-only tops -32)

# --- PASS/FAIL thresholds ------------------------------------------------------------------------
MIN_COVERAGE = 0.85          # FAIL if music-present coverage < 85% of (fade-excluded) runtime
MAX_GAP_S = 15.0             # FAIL if any non-fade music-dead run exceeds 15 s
FADE_FORGIVE_S = 12.0        # forgive an ENDING music-dead run (fade-out) up to this many seconds


# ---------------------------------------------------------------------------------------------
# render resolution
# ---------------------------------------------------------------------------------------------

def resolve_render(ep_dir: Path, override: Optional[str]) -> Optional[Path]:
    """Return the render mp4 to measure, or None if none is present in the repo.

    Prefers 08_edit/renders/*final*.mp4, highest revision (v002 > v001). Falls back to any
    *.mp4 under 08_edit/renders. Returns None (not an error) when nothing is on disk — the
    render may live on the SSD, in which case the caller skips honestly.
    """
    if override:
        p = Path(override)
        return p if p.exists() else None
    rdir = ep_dir / "08_edit" / "renders"
    if not rdir.is_dir():
        return None
    finals = sorted(p for p in rdir.glob("*final*.mp4") if p.stat().st_size > 0)
    if finals:
        return finals[-1]
    anymp4 = sorted(p for p in rdir.glob("*.mp4") if p.stat().st_size > 0)
    return anymp4[-1] if anymp4 else None


# ---------------------------------------------------------------------------------------------
# low-band decode + per-window coverage
# ---------------------------------------------------------------------------------------------

def decode_low_band(path: Path):
    """Decode `path`'s audio band-passed to LOW_BAND_LO..HI Hz, mono, DECODE_SR, as float32.

    Raises subprocess.CalledProcessError if ffmpeg fails (no audio stream / undecodable) — the
    caller turns that into a fail-closed / skip result, never a silent pass.
    """
    import numpy as np
    raw = subprocess.run(
        ["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(path),
         "-af", f"highpass=f={LOW_BAND_LO_HZ},lowpass=f={LOW_BAND_HI_HZ}",
         "-ac", "1", "-ar", str(DECODE_SR), "-f", "f32le", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def window_levels_dbfs(samples) -> list[float]:
    """Per-WINDOW_S RMS level in dBFS of a mono float32 signal (trailing partial window dropped)."""
    import numpy as np
    n = int(WINDOW_S * DECODE_SR)
    if samples.size < n:
        return []
    k = samples.size // n
    frames = samples[:k * n].astype(np.float64).reshape(k, n)
    rms = np.sqrt(np.mean(frames * frames, axis=1))
    db = 20.0 * np.log10(rms + 1e-12)
    return [float(x) for x in db]


def _coverage_from_levels(levels: list[float]) -> dict[str, Any]:
    """Turn per-window dBFS levels into coverage%, largest non-fade gap, and the fade tail size.

    A trailing run of music-dead windows that reaches the end of the film is treated as an
    intended ENDING FADE and forgiven up to FADE_FORGIVE_S (removed from both numerator and
    denominator). Any music-dead run BEFORE that — or the portion of the tail beyond the
    forgiven fade — counts as a real gap.
    """
    total = len(levels)
    present = [lv > MUSIC_FLOOR_DBFS for lv in levels]

    # forgive the ending fade: walk backwards over contiguous music-dead windows up to the budget
    forgive_budget = int(round(FADE_FORGIVE_S / WINDOW_S))
    fade_windows = 0
    i = total - 1
    while i >= 0 and not present[i] and fade_windows < forgive_budget:
        fade_windows += 1
        i -= 1

    effective = present[: total - fade_windows] if fade_windows else present
    eff_n = len(effective)
    present_n = sum(1 for p in effective if p)
    coverage = (present_n / eff_n) if eff_n else 0.0

    # largest run of consecutive music-dead windows among effective windows
    largest_gap_windows = 0
    run = 0
    gaps: list[tuple[float, float]] = []  # (start_s, len_s)
    for idx, p in enumerate(effective):
        if not p:
            if run == 0:
                run_start = idx
            run += 1
            largest_gap_windows = max(largest_gap_windows, run)
        else:
            if run:
                gaps.append((run_start * WINDOW_S, run * WINDOW_S))
            run = 0
    if run:
        gaps.append((run_start * WINDOW_S, run * WINDOW_S))

    return {
        "total_windows": total,
        "effective_windows": eff_n,
        "present_windows": present_n,
        "coverage": coverage,
        "largest_gap_s": largest_gap_windows * WINDOW_S,
        "fade_forgiven_s": fade_windows * WINDOW_S,
        "gaps": gaps,
    }


# ---------------------------------------------------------------------------------------------
# core evaluation (importable by check_final_acceptance)
# ---------------------------------------------------------------------------------------------

def evaluate(epdir: Path, render: Optional[str] = None) -> dict[str, Any]:
    """Measure continuous music-bed coverage of the render and return a gate dict. Never raises,
    never calls sys.exit.

    Returns {'ok': True, 'hard': False, 'skipped': True, ...} when the render is not in the repo
    or its audio cannot be decoded to the low band (fail-closed only applies when the file IS
    present but broken). PASS/FAIL keys: check, ok, hard, reason, coverage_pct, largest_gap_s.
    """
    epdir = Path(epdir)
    render_path = resolve_render(epdir, render)
    if render_path is None:
        return {"check": "music_coverage", "ok": True, "hard": False, "skipped": True,
                "reason": f"no render mp4 found under {epdir/'08_edit'/'renders'} "
                          f"(likely on SSD) — skipping honestly"}

    try:
        samples = decode_low_band(render_path)
    except FileNotFoundError as exc:
        return {"check": "music_coverage", "ok": True, "hard": False, "skipped": True,
                "reason": f"ffmpeg unavailable ({exc}) — cannot measure, skipping"}
    except subprocess.CalledProcessError as exc:
        # render IS present but its audio would not band-pass decode -> fail closed, not silent pass
        err = (exc.stderr or b"").decode("utf-8", "ignore")[:200]
        return {"check": "music_coverage", "ok": False, "hard": True,
                "reason": f"could not decode low band from {render_path.name} "
                          f"(no/broken audio stream?): {err}"}

    levels = window_levels_dbfs(samples)
    if not levels:
        return {"check": "music_coverage", "ok": False, "hard": True,
                "reason": f"{render_path.name} decoded to < {WINDOW_S:.0f}s of audio — unmeasurable"}

    m = _coverage_from_levels(levels)
    coverage_pct = 100.0 * m["coverage"]

    problems: list[str] = []
    if m["coverage"] < MIN_COVERAGE:
        problems.append(f"coverage {coverage_pct:.1f}% < {MIN_COVERAGE*100:.0f}% "
                        f"(music bed missing over long stretches)")
    if m["largest_gap_s"] > MAX_GAP_S:
        problems.append(f"largest music-dead gap {m['largest_gap_s']:.0f}s > {MAX_GAP_S:.0f}s "
                        f"(reads as amateur / bed dropped out)")

    ok = not problems
    return {
        "check": "music_coverage",
        "ok": ok,
        "hard": True,
        "reason": (f"continuous bed: coverage {coverage_pct:.1f}%, "
                   f"largest gap {m['largest_gap_s']:.0f}s" if ok else "; ".join(problems)),
        "render": str(render_path),
        "band_hz": [LOW_BAND_LO_HZ, LOW_BAND_HI_HZ],
        "window_s": WINDOW_S,
        "floor_dbfs": MUSIC_FLOOR_DBFS,
        "coverage_pct": coverage_pct,
        "largest_gap_s": m["largest_gap_s"],
        "fade_forgiven_s": m["fade_forgiven_s"],
        "total_windows": m["total_windows"],
        "present_windows": m["present_windows"],
        "effective_windows": m["effective_windows"],
        "gaps": [[round(a, 1), round(b, 1)] for a, b in m["gaps"]],
        "problems": problems,
    }


# ---------------------------------------------------------------------------------------------
# reporting / atomic json
# ---------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("MUSIC COVERAGE REPORT  (30-90 Hz low-bed probe, per-3s window)")
    print("=" * 78)
    print(f"  render        : {r.get('render')}")
    print(f"  band / floor  : {LOW_BAND_LO_HZ}-{LOW_BAND_HI_HZ} Hz  >  {MUSIC_FLOOR_DBFS:.0f} dBFS")
    print(f"  windows       : {r.get('present_windows')}/{r.get('effective_windows')} present "
          f"(total {r.get('total_windows')}, ending fade forgiven {r.get('fade_forgiven_s'):.0f}s)")
    print(f"  coverage      : {r.get('coverage_pct', 0.0):.1f}%   (min {MIN_COVERAGE*100:.0f}%)")
    print(f"  largest gap   : {r.get('largest_gap_s', 0.0):.0f}s   (max {MAX_GAP_S:.0f}s)")
    if r.get("gaps"):
        shown = ", ".join(f"@{a:.0f}s for {b:.0f}s" for a, b in r["gaps"][:6])
        print(f"  music-dead runs: {shown}")
    print("-" * 78)
    if r.get("ok"):
        print("  RESULT: PASS  — a continuous music bed underlies the film")
    else:
        print("  RESULT: FAIL")
        for p in r.get("problems", []):
            print(f"    - {p}")
    print("-" * 78)


def _atomic_write_json(path: Path, obj: dict[str, Any]) -> None:
    """Write JSON atomically (temp file in the same dir + os.replace)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=2, default=str)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------------------------------------
# selftest: RED fixture (proves the gate can FAIL) + real-episode numbers
# ---------------------------------------------------------------------------------------------

def _write_wav_int16(path: Path, samples, sr: int) -> None:
    """Write a mono int16 PCM WAV (stdlib only) from a float array in [-1, 1]."""
    import wave
    import numpy as np
    pcm = np.clip(samples, -1.0, 1.0)
    pcm = (pcm * 32767.0).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def _selftest() -> int:
    """(a) synthesize a KNOWN-BAD input and assert the gate FAILs (red fixture);
    (b) run evaluate() on the real TEST episode and print the actual numbers."""
    import numpy as np
    print("=" * 78)
    print("SELFTEST — part (a): RED FIXTURE (known-bad synthetic audio must FAIL)")
    print("=" * 78)
    sr = 8000
    dur = 90.0
    t = np.arange(int(dur * sr)) / sr
    # 60 Hz sine bed everywhere (music-present), EXCEPT a 24 s dead stretch [33s,57s] that carries
    # ONLY a 2 kHz tone (no low-band energy) -> a music gap of 24 s (> 15 s) AND coverage ~73%.
    bed = 0.30 * np.sin(2 * np.pi * 60.0 * t)
    dead = (t >= 33.0) & (t < 57.0)
    bed[dead] = 0.30 * np.sin(2 * np.pi * 2000.0 * t[dead])  # high tone: killed by lowpass=90
    with tempfile.TemporaryDirectory() as td:
        red = Path(td) / "red_fixture.wav"
        _write_wav_int16(red, bed, sr)
        r = evaluate(Path(td), render=str(red))
        print(f"  synthesized : 90s bed with a 24s low-band-dead stretch [33-57s]")
        print(f"  coverage    : {r.get('coverage_pct'):.1f}%   largest_gap: {r.get('largest_gap_s'):.0f}s")
        print(f"  reason      : {r.get('reason')}")
        red_ok = (r.get("ok") is False) and (not r.get("skipped"))
        print(f"\n  RED-FIXTURE: {'PASS' if red_ok else 'FAIL'}  "
              f"(gate {'correctly reported ok=False' if red_ok else 'FAILED to catch the bad input'})")

    print("\n" + "=" * 78)
    print(f"SELFTEST — part (b): real TEST episode {DEFAULT_EP}")
    print("=" * 78)
    epdir = ROOT / "episodes" / DEFAULT_EP
    real = evaluate(epdir)
    _print_report(real)
    return 0 if red_ok else 1


# ---------------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------------

def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001 - non-reconfigurable stream is fine
        pass
    ap = argparse.ArgumentParser(
        description="Independent music-coverage gate: FAIL if the music bed drops out for long "
                    "stretches (coverage < 85% or any non-fade gap > 15s).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug")
    ap.add_argument("--render", default=None, help="override render mp4 (default newest *final*.mp4)")
    ap.add_argument("--dry-run", action="store_true",
                    help="resolve the render + print the plan without decoding audio (exit 0)")
    ap.add_argument("--json", nargs="?", const="-", default=None, metavar="PATH",
                    help="emit the result dict as JSON (to PATH atomically, or stdout if no PATH)")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED fixture then measure the real TEST episode")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    ep_dir = ROOT / "episodes" / args.ep
    if not ep_dir.exists():
        print(f"[ERROR] episode dir not found: {ep_dir}")
        return 1

    if args.dry_run:
        render_path = resolve_render(ep_dir, args.render)
        print(f"[DRY-RUN] episode      : {args.ep}")
        print(f"[DRY-RUN] render target: {render_path if render_path else '(none in repo — would SKIP)'}")
        print(f"[DRY-RUN] probe        : {LOW_BAND_LO_HZ}-{LOW_BAND_HI_HZ} Hz, {WINDOW_S:.0f}s windows, "
              f"floor {MUSIC_FLOOR_DBFS:.0f} dBFS")
        print(f"[DRY-RUN] thresholds   : coverage >= {MIN_COVERAGE*100:.0f}%, "
              f"largest gap <= {MAX_GAP_S:.0f}s, ending fade forgiven <= {FADE_FORGIVE_S:.0f}s")
        print("[DRY-RUN] no audio decoded, no files written.")
        return 0

    r = evaluate(ep_dir, render=args.render)
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
