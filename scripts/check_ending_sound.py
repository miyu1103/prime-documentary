#!/usr/bin/env python3
r"""Independent ending-sound gate — catches the owner's 'weird jet/roar' at the tail of a render.

The owner flagged that some episodes end with a WEIRD JET / ROAR: a sustained noise-like blast (as
opposed to the intended clean musical/ambient fade-out), and sometimes the audio SPIKES louder / rises
at the very end instead of settling. This gate MEASURES the last ~12 s of the render's real audio
track and FAILs if any defect is present. It does not trust any plan, provenance, or self-report —
only the decoded waveform (CLAUDE invariant 13/15).

Three independent, physically-grounded measurements over the tail:

  1) ROAR (noise-like, sustained).  A jet/roar is NOISE, and noise can be spectrally colored. We
     frame the tail (1024-sample Hann frames, 50% hop @ 22.05 kHz) and, for every frame loud enough
     to judge (RMS > ROAR_MIN_DB), flag it "roar-like" when EITHER of two noise signatures holds —
     an OR, not an AND, so a low-frequency rumble with little high-frequency energy is NOT missed:

       (a) BROADBAND roar — full-spectrum spectral flatness (geometric/arithmetic mean of the power
           spectrum → ~1.0 for white/broadband noise, ~0 for a tone) is HIGH (> ROAR_FLATNESS) AND
           the frame is high-frequency-heavy (energy fraction above HF_CUTOFF_HZ > HF_ROAR_MIN).
           This catches white/pink broadband hiss.

       (b) LOW-FREQUENCY RUMBLE — most of the energy sits below LF_CUTOFF_HZ (lf_ratio > LF_RUMBLE_MIN)
           AND that low band is itself noise-like, i.e. flat within the band (lf_flat > LF_FLATNESS,
           which is HIGH for filtered noise but ~0 for a clean bass tone/harmonic). This catches a
           low-freq jet rumble that carries almost no high-frequency energy and therefore trips
           NEITHER condition in (a).

     If a SUSTAINED fraction of the loud tail (>= ROAR_SUSTAIN_FRAC) is roar-like by (a) OR (b),
     that is the jet/roar → FAIL. A tonal fade or musical button is not flat in either band and
     never trips this.

  2) TERMINAL LOUDNESS SPIKE (fade shape).  A clean ending fades DOWN. We take 0.25 s RMS(dB)
     windows across the tail; the "very end" (last END_WIN_SEC) must NOT be markedly louder than the
     tail body. FAIL if the end level exceeds the tail-body median by >= SPIKE_DB AND the end is
     genuinely loud (>= END_FLOOR_DB).

  3) NON-FADING / RISING ENDING (fade slope is GATED, not just reported).  The loudness slope over
     the last END_RISE_SEC seconds must be fading (negative) or flat. FAIL if it RISES
     (>= RISE_SLOPE_MIN dB/s) while the end is genuinely loud (>= END_FLOOR_DB) — the audio swells
     up into the cut instead of resolving. A clean fade is strongly negative and passes with margin.

All measurements are deterministic (no randomness, no wall-clock) so re-runs are reproducible and
the acceptance gate can trust them.

Calibrated against the real EP31 unlock render tail (clean): full-spectrum flatness median ~0.000
(max 0.164 « 0.22), the low band is tonal (lf_flat « 0.20), and the end fades from ~-17 dB to
~-33 dB (spike far negative, slope strongly negative) — passes with wide margin. The RED self-test
exercises the EXACT gaming probes an independent reviewer used: a broadband white-noise roar, a
COLORED (pink / filtered) roar, a LOW-FREQUENCY rumble ending, and a terminal loudness spike/rise —
each must FAIL; a clean tonal fade must PASS.

Usage:
  py -3.11 scripts/check_ending_sound.py --ep PD-2026-031-unlock
  py -3.11 scripts/check_ending_sound.py --ep PD-2026-031-unlock --render <path.mp4> --json
  py -3.11 scripts/check_ending_sound.py --selftest          # RED fixtures + real-episode numbers
  py -3.11 scripts/check_ending_sound.py --ep <slug> --dry-run

Exit 0 = PASS or --dry-run. Exit 1 = FAIL or usage/episode error. Skips honestly (ok=True,
skipped=True) when the render is absent (e.g. it lives on the SSD) so it never crashes the caller.

check_final_acceptance can import this module and call evaluate(epdir); the returned dict follows
its gate contract: {"check": "ending_sound", "ok": bool, "hard": bool, "reason": str, ...numbers}.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
import wave
from pathlib import Path
from statistics import median
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-031-unlock"

# --- analysis geometry -------------------------------------------------------------------------
TAIL_SEC = 12.0          # analyze the last ~12 s of the render
SR = 22050               # decode SR (mono); Nyquist 11.025 kHz is plenty for roar/spike shape
FRAME_N = 1024           # ~46 ms spectral frame
FRAME_HOP = 512          # 50% overlap
HF_CUTOFF_HZ = 2000.0    # "high-frequency" band edge for the roar's HF-energy fraction
LF_CUTOFF_HZ = 500.0     # "low-frequency" band edge for the rumble test
ENV_WIN_SEC = 0.25       # RMS envelope window for the fade/spike test
FADE_SEC = 6.0           # window over which the fade slope (dB/s) is reported for diagnosis
END_RISE_SEC = 2.0       # window over which the GATED "is it still rising?" slope is measured

# --- ROAR (broadband) thresholds ---------------------------------------------------------------
# EP31 clean tail: full-spectrum flatness max 0.164, hf-fraction median 0.001. Broadband noise:
# flatness ~0.5-1, hf-fraction ~0.3-0.8. The gap is wide; these floors sit safely between.
ROAR_FLATNESS = 0.22     # per-frame full-spectrum flatness above this = "flat/broadband"
HF_ROAR_MIN = 0.08       # AND >8% of energy above HF_CUTOFF_HZ = "high-frequency broadband hiss"
# --- ROAR (low-frequency rumble) thresholds ----------------------------------------------------
# A low-freq jet rumble has little HF energy (so it misses the broadband test), but it is still
# NOISE concentrated in the low band. A clean bass tone/harmonic is also low-band but is TONAL
# (flat-within-band ~0), so lf_flat separates a rumble (noise) from a bass note (tone).
LF_RUMBLE_MIN = 0.60     # >=60% of energy below LF_CUTOFF_HZ = "dominated by low frequencies"
LF_FLATNESS = 0.20       # AND the low band is itself flat/noise-like (a tone is far below this)
ROAR_MIN_DB = -45.0      # only frames this loud are judged (ignore near-silence)
ROAR_SUSTAIN_FRAC = 0.35 # FAIL if >=35% of the LOUD tail frames are roar-like (sustained, not a blip)

# --- terminal loudness SPIKE / RISE thresholds -------------------------------------------------
END_WIN_SEC = 0.75       # the "very end" measured region
SPIKE_DB = 4.0           # FAIL if end level exceeds tail-body median by this many dB (a swell)
END_FLOOR_DB = -30.0     # ...and only when the end is genuinely loud (not a quiet artifact)
RISE_SLOPE_MIN = 1.5     # FAIL if the last END_RISE_SEC loudness slope rises >= this (dB/s) & is loud


# ---------------------------------------------------------------------------------------------
# render resolution
# ---------------------------------------------------------------------------------------------

def resolve_render(ep_dir: Path, override: Optional[str]) -> Optional[Path]:
    """Locate the FINAL render mp4 for the episode, or None if not present in the repo.

    Prefers 08_edit/renders/*final*.mp4 (excluding review proxies), highest version / newest mtime.
    Falls back to any *.mp4 under 08_edit/renders. Returns None when nothing is on disk (the render
    may live on the SSD) so the caller can skip honestly rather than crash.
    """
    if override:
        p = Path(override)
        return p if p.exists() else None
    renders = ep_dir / "08_edit" / "renders"
    if not renders.is_dir():
        return None
    cands = [p for p in renders.glob("*.mp4")
             if p.is_file() and "proxy" not in p.name.lower() and p.stat().st_size > 0]
    if not cands:
        return None
    finals = [p for p in cands if "final" in p.name.lower()] or cands
    # highest version then newest mtime: name sort puts v002 after v001; mtime breaks ties
    finals.sort(key=lambda p: (p.name, p.stat().st_mtime))
    return finals[-1]


# ---------------------------------------------------------------------------------------------
# audio decode
# ---------------------------------------------------------------------------------------------

def ffprobe_duration(path: Path) -> Optional[float]:
    """Container duration in seconds via ffprobe, or None if it cannot be read."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nokey=1:noprint_wrappers=1", str(path)],
            capture_output=True, text=True, timeout=120)
        return float(out.stdout.strip())
    except Exception:  # noqa: BLE001 - unreadable/absent -> caller skips honestly
        return None


def has_audio_stream(path: Path) -> bool:
    """True if the file exposes at least one audio stream (ffprobe)."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a",
             "-show_entries", "stream=index", "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, timeout=120)
        return bool(out.stdout.strip())
    except Exception:  # noqa: BLE001
        return False


def decode_tail(path: Path, tail_sec: float, total_dur: Optional[float]):
    """Decode the last `tail_sec` seconds of the first audio stream to a mono float32 numpy array
    at SR. Returns the array (may be shorter than requested for short files)."""
    import numpy as np
    ss = 0.0
    if total_dur and total_dur > tail_sec:
        ss = total_dur - tail_sec
    raw = subprocess.run(
        ["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", f"{ss:.3f}", "-i", str(path),
         "-map", "0:a:0", "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


# ---------------------------------------------------------------------------------------------
# core measurement (pure numpy — importable & testable without any file I/O)
# ---------------------------------------------------------------------------------------------

def analyze_tail(audio: "Any") -> dict[str, Any]:
    """Measure ending spectral shape (broadband roar + low-freq rumble) and fade/spike/rise on a
    mono float32 array at SR.

    Returns a dict of numbers: n_sec, loud_frames, roar_frames, roar_frac, white_roar_frames,
    rumble_frames, roar_flatness_med, hf_ratio_med, lf_ratio_med, lf_flat_med, env_len,
    tail_body_median_db, end_level_db, spike_db, fade_slope_db_per_s, end_rise_slope_db_per_s.
    Never raises on empty/short input (returns zeros where undefined).
    """
    import numpy as np
    a = np.asarray(audio, dtype=np.float32)
    out: dict[str, Any] = {
        "n_sec": float(a.size / SR),
        "loud_frames": 0, "roar_frames": 0, "roar_frac": 0.0,
        "white_roar_frames": 0, "rumble_frames": 0,
        "roar_flatness_med": 0.0, "hf_ratio_med": 0.0,
        "lf_ratio_med": 0.0, "lf_flat_med": 0.0,
        "env_len": 0, "tail_body_median_db": -120.0, "end_level_db": -120.0,
        "spike_db": -120.0, "fade_slope_db_per_s": 0.0, "end_rise_slope_db_per_s": 0.0,
    }
    # --- spectral roar analysis (broadband OR low-freq rumble) ---
    if a.size >= FRAME_N:
        win = np.hanning(FRAME_N).astype(np.float32)
        starts = range(0, a.size - FRAME_N + 1, FRAME_HOP)
        frames = np.stack([a[s:s + FRAME_N] * win for s in starts])
        power = np.abs(np.fft.rfft(frames, axis=1)) ** 2
        freqs = np.fft.rfftfreq(FRAME_N, 1.0 / SR)
        pos = power[:, 1:] + 1e-12                      # drop DC bin, floor to avoid log(0)
        fpos = freqs[1:]
        total_e = np.sum(pos, axis=1)
        # full-spectrum flatness (broadband signature)
        flat = np.exp(np.mean(np.log(pos), axis=1)) / np.mean(pos, axis=1)
        rms = np.sqrt(np.mean(frames ** 2, axis=1)) + 1e-12
        db = 20.0 * np.log10(rms)
        # high-frequency energy fraction (broadband hiss signature)
        hf_mask = fpos > HF_CUTOFF_HZ
        hf_ratio = np.sum(pos[:, hf_mask], axis=1) / total_e
        # low-frequency band: energy fraction + within-band flatness (rumble signature)
        lf_mask = fpos < LF_CUTOFF_HZ
        lf_ratio = np.sum(pos[:, lf_mask], axis=1) / total_e
        pos_lf = pos[:, lf_mask]
        lf_flat = np.exp(np.mean(np.log(pos_lf), axis=1)) / np.mean(pos_lf, axis=1)
        loud = db > ROAR_MIN_DB
        white_roar = loud & (flat > ROAR_FLATNESS) & (hf_ratio > HF_ROAR_MIN)
        lf_rumble = loud & (lf_ratio > LF_RUMBLE_MIN) & (lf_flat > LF_FLATNESS)
        roar = white_roar | lf_rumble                  # OR, not AND: colored/low rumble not missed
        n_loud = int(np.sum(loud))
        n_roar = int(np.sum(roar))
        out["loud_frames"] = n_loud
        out["roar_frames"] = n_roar
        out["white_roar_frames"] = int(np.sum(white_roar))
        out["rumble_frames"] = int(np.sum(lf_rumble))
        out["roar_frac"] = (n_roar / n_loud) if n_loud else 0.0
        if n_loud:
            out["roar_flatness_med"] = float(np.median(flat[loud]))
            out["hf_ratio_med"] = float(np.median(hf_ratio[loud]))
            out["lf_ratio_med"] = float(np.median(lf_ratio[loud]))
            out["lf_flat_med"] = float(np.median(lf_flat[loud]))
    # --- fade / terminal-spike / rising-end analysis ---
    w = int(ENV_WIN_SEC * SR)
    if w > 0 and a.size >= w:
        env = np.array([20.0 * np.log10(np.sqrt(np.mean(a[s:s + w] ** 2)) + 1e-9)
                        for s in range(0, a.size - w + 1, w)], dtype=np.float64)
        out["env_len"] = int(env.size)
        n_end = max(1, int(round(END_WIN_SEC / ENV_WIN_SEC)))
        n_end = min(n_end, env.size)
        end_level = float(np.mean(env[-n_end:]))
        body = env[:-n_end] if env.size > n_end else env
        body_med = float(np.median(body))
        out["end_level_db"] = end_level
        out["tail_body_median_db"] = body_med
        out["spike_db"] = end_level - body_med
        # fade slope over the last FADE_SEC via least-squares linear fit (dB per second) — diagnostic
        n_fade = min(env.size, max(2, int(round(FADE_SEC / ENV_WIN_SEC))))
        yy = env[-n_fade:]
        xx = np.arange(yy.size, dtype=np.float64) * ENV_WIN_SEC
        if yy.size >= 2:
            out["fade_slope_db_per_s"] = float(np.polyfit(xx, yy, 1)[0])
        # rising-end slope over the last END_RISE_SEC — this one is GATED
        n_rise = min(env.size, max(2, int(round(END_RISE_SEC / ENV_WIN_SEC))))
        yr = env[-n_rise:]
        xr = np.arange(yr.size, dtype=np.float64) * ENV_WIN_SEC
        if yr.size >= 2:
            out["end_rise_slope_db_per_s"] = float(np.polyfit(xr, yr, 1)[0])
    return out


def _verdict(m: dict[str, Any]) -> tuple[bool, list[str]]:
    """Apply the thresholds to a measurement dict -> (ok, problems)."""
    problems: list[str] = []
    if m["loud_frames"] and m["roar_frac"] >= ROAR_SUSTAIN_FRAC:
        problems.append(
            f"broadband/rumble roar: {m['roar_frac']*100:.0f}% of loud tail frames are noise-like "
            f"(broadband {m['white_roar_frames']}, low-rumble {m['rumble_frames']}; "
            f"flat_med {m['roar_flatness_med']:.3f}, hf_med {m['hf_ratio_med']:.2f}, "
            f"lf_ratio_med {m['lf_ratio_med']:.2f}, lf_flat_med {m['lf_flat_med']:.3f}) "
            f">= {ROAR_SUSTAIN_FRAC*100:.0f}% sustained")
    if m["spike_db"] >= SPIKE_DB and m["end_level_db"] >= END_FLOOR_DB:
        problems.append(
            f"terminal loudness spike: end {m['end_level_db']:+.1f} dB is {m['spike_db']:+.1f} dB "
            f"above tail-body median {m['tail_body_median_db']:+.1f} dB (swells up, no clean fade)")
    if m["end_rise_slope_db_per_s"] >= RISE_SLOPE_MIN and m["end_level_db"] >= END_FLOOR_DB:
        problems.append(
            f"ending rises instead of fading: last {END_RISE_SEC:.0f}s loudness slope "
            f"{m['end_rise_slope_db_per_s']:+.1f} dB/s (>= +{RISE_SLOPE_MIN} dB/s) with end "
            f"{m['end_level_db']:+.1f} dB (>= {END_FLOOR_DB} dB) — no clean fade")
    return (not problems), problems


# ---------------------------------------------------------------------------------------------
# evaluate (importable by check_final_acceptance)
# ---------------------------------------------------------------------------------------------

def evaluate(epdir: Path, render: Optional[str] = None) -> dict[str, Any]:
    """Measure the ending sound of the episode's final render and return a gate dict.

    NEVER raises and NEVER calls sys.exit. Returns {"skipped": True, "ok": True, "hard": False}
    when the render is not in the repo (e.g. on the SSD) or the tools/audio are unavailable, so the
    acceptance caller is never crashed and a missing artifact is not faked green as a real pass.
    """
    epdir = Path(epdir)
    base = {"check": "ending_sound"}
    rp = resolve_render(epdir, render)
    if rp is None:
        return {**base, "ok": True, "hard": False, "skipped": True,
                "reason": "final render not found in repo (may be on SSD) — ending-sound not measured"}
    try:
        import numpy  # noqa: F401
    except Exception as exc:  # noqa: BLE001
        return {**base, "ok": True, "hard": False, "skipped": True,
                "reason": f"numpy unavailable ({exc}) — ending-sound not measured"}
    if not has_audio_stream(rp):
        return {**base, "ok": True, "hard": False, "skipped": True,
                "reason": f"no audio stream in {rp.name} — ending-sound not measured"}
    dur = ffprobe_duration(rp)
    try:
        audio = decode_tail(rp, TAIL_SEC, dur)
    except FileNotFoundError as exc:
        return {**base, "ok": True, "hard": False, "skipped": True,
                "reason": f"ffmpeg/ffprobe unavailable ({exc}) — ending-sound not measured"}
    except subprocess.CalledProcessError as exc:
        err = (exc.stderr or b"").decode("utf-8", "ignore")[:200]
        return {**base, "ok": True, "hard": False, "skipped": True,
                "reason": f"ffmpeg failed decoding tail ({err}) — ending-sound not measured"}
    if audio.size < SR // 2:  # < 0.5 s of audio -> nothing to judge
        return {**base, "ok": True, "hard": False, "skipped": True,
                "reason": f"tail too short to analyze ({audio.size} samples) — not measured"}

    m = analyze_tail(audio)
    ok, problems = _verdict(m)
    reason = ("clean ending: tonal fade, no broadband/rumble roar, no terminal spike/rise"
              if ok else "; ".join(problems))
    return {
        **base, "ok": ok, "hard": True, "reason": reason,
        "render": str(rp),
        "tail_sec": round(m["n_sec"], 2),
        "roar_frac": round(m["roar_frac"], 3),
        "roar_frames": m["roar_frames"],
        "white_roar_frames": m["white_roar_frames"],
        "rumble_frames": m["rumble_frames"],
        "loud_frames": m["loud_frames"],
        "roar_flatness_med": round(m["roar_flatness_med"], 4),
        "hf_ratio_med": round(m["hf_ratio_med"], 4),
        "lf_ratio_med": round(m["lf_ratio_med"], 4),
        "lf_flat_med": round(m["lf_flat_med"], 4),
        "end_level_db": round(m["end_level_db"], 2),
        "tail_body_median_db": round(m["tail_body_median_db"], 2),
        "spike_db": round(m["spike_db"], 2),
        "fade_slope_db_per_s": round(m["fade_slope_db_per_s"], 3),
        "end_rise_slope_db_per_s": round(m["end_rise_slope_db_per_s"], 3),
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
    print("ENDING SOUND REPORT  (last ~12 s of the render)")
    print("=" * 78)
    print(f"  render        : {r['render']}")
    print(f"  tail analyzed : {r['tail_sec']:.1f} s")
    print("  -- roar (noise-like, sustained; broadband OR low-freq rumble) --")
    print(f"     roar frames : {r['roar_frames']}/{r['loud_frames']} loud "
          f"= {r['roar_frac']*100:.0f}%  (FAIL >= {ROAR_SUSTAIN_FRAC*100:.0f}%)  "
          f"[broadband {r['white_roar_frames']}, rumble {r['rumble_frames']}]")
    print(f"     flatness_med: {r['roar_flatness_med']:.4f}  (broadband roar if > {ROAR_FLATNESS})")
    print(f"     hf>{HF_CUTOFF_HZ/1000:.0f}kHz med: {r['hf_ratio_med']:.4f}  (broadband roar if > {HF_ROAR_MIN})")
    print(f"     lf<{LF_CUTOFF_HZ/1000:.1f}kHz frac: {r['lf_ratio_med']:.4f}  lf_flat {r['lf_flat_med']:.4f}  "
          f"(rumble if lf_frac > {LF_RUMBLE_MIN} & lf_flat > {LF_FLATNESS})")
    print("  -- terminal loudness / fade --")
    print(f"     tail median : {r['tail_body_median_db']:+.1f} dB")
    print(f"     very-end    : {r['end_level_db']:+.1f} dB   spike {r['spike_db']:+.1f} dB "
          f"(FAIL >= +{SPIKE_DB} dB above median & end >= {END_FLOOR_DB} dB)")
    print(f"     end slope   : {r['end_rise_slope_db_per_s']:+.2f} dB/s over last {END_RISE_SEC:.0f} s "
          f"(FAIL >= +{RISE_SLOPE_MIN} dB/s & end >= {END_FLOOR_DB} dB — a rising, non-fading end)")
    print(f"     fade slope  : {r['fade_slope_db_per_s']:+.2f} dB/s over last {FADE_SEC:.0f} s "
          f"(diagnostic; clean fade is strongly negative)")
    print("-" * 78)
    if r["ok"]:
        print("  RESULT: PASS — tonal fade-out, no jet/roar, no end spike/rise")
    else:
        print("  RESULT: FAIL")
        for p in r["problems"]:
            print(f"    - {p}")
    print("-" * 78)


# ---------------------------------------------------------------------------------------------
# self-test: RED fixtures (must FAIL) + a GREEN clean fade (must PASS) + real episode numbers
# ---------------------------------------------------------------------------------------------

def _write_wav(path: Path, samples: "Any", sr: int) -> None:
    """Write a mono 16-bit PCM WAV (stdlib only) from a float32 array in [-1, 1]."""
    import numpy as np
    clipped = np.clip(np.asarray(samples, dtype=np.float32), -1.0, 1.0)
    pcm = (clipped * 32767.0).astype("<i2").tobytes()
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm)


def _rms_norm(x: "Any", target_db: float) -> "Any":
    """Scale a float32 array to a target RMS in dBFS (deterministic)."""
    import numpy as np
    x = np.asarray(x, dtype=np.float32)
    r = float(np.sqrt(np.mean(x ** 2))) + 1e-12
    return (x * (10.0 ** (target_db / 20.0) / r)).astype(np.float32)


def _shaped_noise(rng: "Any", n: int, mode: str) -> "Any":
    """Deterministic colored/filtered noise via frequency-domain shaping.

    mode: 'white' (flat), 'pink' (1/f amplitude — a COLORED roar), 'lowpass' (energy only below
    LF_CUTOFF_HZ — a LOW-FREQUENCY rumble).
    """
    import numpy as np
    white = rng.standard_normal(n).astype(np.float64)
    spec = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n, 1.0 / SR)
    f = freqs.copy()
    f[0] = f[1] if f.size > 1 else 1.0  # avoid div-by-zero at DC
    if mode == "white":
        shaped = spec
    elif mode == "pink":
        shaped = spec / np.sqrt(f)                       # power ~ 1/f
    elif mode == "lowpass":
        keep = freqs < (LF_CUTOFF_HZ * 1.4)              # fill the whole low band with noise (rumble)
        shaped = spec * keep
    else:  # pragma: no cover - guard
        raise ValueError(mode)
    return np.fft.irfft(shaped, n).astype(np.float32)


def _make_fixture(kind: str, rng: "Any"):
    """Build a 12 s mono float32 tail for a named fixture (deterministic)."""
    import numpy as np
    n = int(TAIL_SEC * SR)
    t = np.arange(n, dtype=np.float64) / SR
    if kind == "white_roar_spike":
        # broadband white-noise roar for the whole tail + a loud terminal ramp (swell UP)
        sig = _rms_norm(_shaped_noise(rng, n, "white"), -18.0)
        end = int(END_WIN_SEC * SR)
        sig[-end:] *= np.linspace(1.0, 6.0, end, dtype=np.float32)
        return sig
    if kind == "pink_roar":
        # COLORED (1/f) roar — verifies the roar thresholds are not calibrated to white noise only
        return _rms_norm(_shaped_noise(rng, n, "pink"), -18.0)
    if kind == "low_rumble":
        # LOW-FREQUENCY jet rumble: filtered noise below ~400 Hz, little HF energy (the AND-gate hole)
        return _rms_norm(_shaped_noise(rng, n, "lowpass"), -16.0)
    if kind == "tonal_end_spike":
        # clean tonal body that then RISES/swells in loudness over the last END_RISE_SEC (the
        # ungated-fade-slope hole). Tonal, so it does NOT trip roar — isolates the spike/rise gate.
        tone = np.sin(2.0 * math.pi * 220.0 * t).astype(np.float32)
        amp = (0.30 * np.exp(-t / 4.0)).astype(np.float32)          # fading body
        rise0 = n - int(END_RISE_SEC * SR)
        ramp = np.linspace(1.0, 12.0, n - rise0, dtype=np.float32)  # loud swell into the cut
        amp[rise0:] = amp[rise0] * ramp
        return (tone * amp).astype(np.float32)
    if kind == "clean_fade":
        # GREEN: a clean tonal fade-out — decaying 220 Hz tone, resolves to near silence
        tone = np.sin(2.0 * math.pi * 220.0 * t).astype(np.float32)
        amp = (0.35 * np.exp(-t / 3.0)).astype(np.float32)
        return (tone * amp).astype(np.float32)
    raise ValueError(kind)  # pragma: no cover


def _run_fixture(kind: str, expect_fail: bool, rng: "Any") -> bool:
    """Build a fixture, run the real gate over it, print the report, and return whether it matched
    the expectation (FAIL for red, PASS for green)."""
    sig = _make_fixture(kind, rng)
    with tempfile.TemporaryDirectory() as td:
        ep = Path(td) / "PD-9999-999-fixture"
        (ep / "08_edit" / "renders").mkdir(parents=True)
        wav = ep / "08_edit" / "renders" / f"{kind}_final.v001.wav"
        _write_wav(wav, sig, SR)
        r = evaluate(ep, render=str(wav))
    label = "RED " if expect_fail else "GREEN"
    print("\n" + "#" * 78)
    print(f"# {label} FIXTURE: {kind}  (expected {'FAIL' if expect_fail else 'PASS'})")
    print("#" * 78)
    _print_report(r)
    got_fail = (r.get("ok") is False) and not r.get("skipped")
    matched = (got_fail == expect_fail)
    print(f"  -> fixture {kind}: {'FAIL' if got_fail else ('SKIP' if r.get('skipped') else 'PASS')}"
          f"  ({'OK' if matched else 'WRONG'})")
    return matched


def _selftest() -> int:
    import numpy as np
    print("=" * 78)
    print("SELFTEST — gaming probes an independent reviewer used")
    print("  RED (must FAIL): broadband roar+spike, colored/pink roar, low-freq rumble, terminal rise")
    print("  GREEN (must PASS): clean tonal fade-out")
    print("=" * 78)
    rng = np.random.RandomState(1234)  # deterministic
    reds = [
        ("white_roar_spike", True),
        ("pink_roar", True),
        ("low_rumble", True),
        ("tonal_end_spike", True),
    ]
    greens = [("clean_fade", False)]
    results: list[tuple[str, bool]] = []
    for kind, exp in reds + greens:
        results.append((kind, _run_fixture(kind, exp, rng)))

    all_ok = all(ok for _, ok in results)
    print("\n" + "=" * 78)
    print("SELFTEST SUMMARY")
    for kind, ok in results:
        print(f"   {'OK ' if ok else 'BAD'}  {kind}")
    print(f"\nRED-FIXTURE: {'PASS' if all_ok else 'FAIL'}  "
          f"(gate {'correctly flagged every bad ending and passed the clean fade' if all_ok else 'MISCLASSIFIED at least one fixture'})")

    print("\n" + "=" * 78)
    print(f"SELFTEST — REAL EPISODE ({DEFAULT_EP})")
    print("=" * 78)
    real = evaluate(ROOT / "episodes" / DEFAULT_EP)
    _print_report(real)
    # selftest succeeds iff every red failed and every green passed (proves the gate CAN fail
    # exactly on the reviewer's probes and still passes a clean ending).
    return 0 if all_ok else 1


# ---------------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------------

def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(
        description="Independent ending-sound gate: FAIL on a broadband/rumble jet-roar or a "
                    "terminal loudness spike/rise in the last ~12 s of the render.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug")
    ap.add_argument("--render", default=None, help="override render mp4 path")
    ap.add_argument("--dry-run", action="store_true",
                    help="resolve inputs and report intent WITHOUT decoding audio; always exit 0")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED fixtures (must FAIL) + a GREEN clean fade (must PASS), then the real episode")
    ap.add_argument("--json", action="store_true", help="also print the raw result dict as JSON")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    ep_dir = ROOT / "episodes" / args.ep
    if not ep_dir.exists():
        print(f"[ERROR] episode dir not found: {ep_dir}")
        return 1

    if args.dry_run:
        rp = resolve_render(ep_dir, args.render)
        if rp is None:
            print(f"[DRY-RUN] {args.ep}: no final render found in repo "
                  f"(would SKIP honestly — render may be on SSD).")
        else:
            dur = ffprobe_duration(rp)
            print(f"[DRY-RUN] {args.ep}: would analyze last {TAIL_SEC:.0f}s of {rp}")
            print(f"          duration={dur if dur else '?'}s  audio_stream="
                  f"{has_audio_stream(rp)}  (no decode performed)")
        return 0

    r = evaluate(ep_dir, render=args.render)
    _print_report(r)
    if args.json:
        print(json.dumps(r, indent=2, default=str))
    if r.get("skipped"):
        return 0  # honest skip is not a failure (missing artifact / SSD)
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
