#!/usr/bin/env python3
r"""Procedurally synthesize a RIGHTS-FREE (owned) SFX + ambience palette with ffmpeg.

WHY THIS FILE EXISTS
--------------------
An adversarial critic found the reusable PD sound palette
(``E:\pd-media\library\sfx`` + ``\ambience``) is THIN and REPETITIVE: a handful
of one-shots (ui_tick / sub_drop / whoosh_short) are reused dozens of times per
episode -- an audible "cheap" tell. The fix is MORE VARIETY, generated in a way
whose rights are unambiguous: everything here is synthesized from first
principles with ffmpeg's own oscillators + noise generators + filters +
envelopes. There is no third-party sample, no model output, no paid API. WE OWN
THE OUTPUT outright (ffmpeg is LGPL/GPL tooling; generated tones/noise are not
copyrightable third-party content).

WHAT IT MAKES (all NEW names -- never overwrites the existing ElevenLabs assets)
--------------------------------------------------------------------------------
SFX one-shot variants (kills repetition by giving the builder pitched siblings):
  * 3 whoosh variants  (short/high, med/mid, long/low)
  * 2 riser variants   (1.2 s, 3.0 s)
  * boom + tight impact
  * 2 sub-drop variants (descending chirps, different depth/length)
  * 2 ui-tick pitch variants (hi / lo)
  * 2 data-blip pitch variants (hi / lo)
Ambience beds the EP32 script needs but the library is missing:
  * rain-on-street, night highway/traffic wash, engine idle hum,
    light wind, 1920s-road low rumble

LEVELS
------
Each file is measured (ffmpeg astats) then gain-normalized:
  * one-shot SFX  -> peak  ~ -18 dBFS  (headroom; the mix builder sets final gain)
  * ambience beds -> RMS   ~ -19 dBFS  (a clean, constant, loopable bed)
Both land in the requested -18..-20 dBFS band.

SAFETY / DETERMINISM
--------------------
No network, no paid API, no GPU. Idempotent: same inputs -> same bytes; every
noise source is seeded, every oscillator is analytic. Re-running rebuilds the
same files in place. Writes ONLY to the two library folders (new filenames).
Windows raw-string paths; storage root resolved from config/storage.local.json
with an ``E:\pd-media`` fallback (same contract as build_case_film_audio.py).

RUN
---
    python scripts/gen_sound_palette.py
    python scripts/gen_sound_palette.py --dry-run   # print plan, synthesize nothing
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
SR = 44100
MP3_BITRATE = "192k"
SFX_PEAK_TARGET_DB = -18.0
BED_RMS_TARGET_DB = -19.0
SCRATCH = Path(
    r"C:\Users\aab15\AppData\Local\Temp\claude\C--Users-aab15"
    r"\dd3cd437-aed4-4522-b996-2bfa474fda36\scratchpad"
)


def media_root() -> Path:
    cfg_path = ROOT / "config" / "storage.local.json"
    try:
        cfg = json.loads(cfg_path.read_text("utf-8"))
        return Path(cfg["roots"]["media"]["path"])
    except Exception:
        return Path(r"E:\pd-media")


def run(argv: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(argv, capture_output=True, text=True, check=False)


def ffprobe_duration(path: Path) -> Optional[float]:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", str(path)])
    try:
        return float(out.stdout.strip())
    except Exception:
        return None


def measure(path: Path) -> tuple[Optional[float], Optional[float]]:
    """Return (overall_peak_dB, overall_rms_dB) via ffmpeg astats."""
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
               "-af", "astats=measure_overall=Peak_level+RMS_level:measure_perchannel=none",
               "-f", "null", "-"])
    txt = out.stderr

    def last(label: str) -> Optional[float]:
        vals = re.findall(rf"{label}:\s*(-?\d+\.?\d*|-?inf)", txt)
        if not vals:
            return None
        v = vals[-1]
        try:
            return float(v)
        except ValueError:
            return None

    return last("Peak level dB"), last("RMS level dB")


# ============================================================================
# palette definition
# ----------------------------------------------------------------------------
# Each entry: (filename, category, duration_sec, lavfi_graph, seed_note)
# lavfi_graph is a complete filtergraph whose final (unlabeled) output is the
# sink -- passed as ONE argv token, so internal spaces/parens need no shell
# quoting.
# ============================================================================
def chirp_expr(f0: float, f1: float, dur: float, amp: float = 0.7) -> str:
    """Analytic linear-frequency-swept sine (phase = integral of instantaneous f)."""
    k = (f1 - f0) / (2.0 * dur)  # quadratic phase coefficient
    return f"{amp}*sin(2*PI*({f0}*t+{k:.5f}*t*t))"


def whoosh(dur: float, hp: float, lp: float, seed: int) -> str:
    return (
        f"anoisesrc=color=pink:seed={seed}:duration={dur}:amplitude=0.85,"
        f"highpass=f={hp},lowpass=f={lp},flanger=depth=3:speed=0.8,"
        f"afade=t=in:st=0:d={dur * 0.45:.3f}:curve=tri,"
        f"afade=t=out:st={dur * 0.45:.3f}:d={dur * 0.55:.3f}:curve=hsin"
    )


def riser(dur: float, seed: int) -> str:
    tone = chirp_expr(300.0, 2100.0, dur, amp=0.5)
    return (
        f"aevalsrc=exprs={tone}:duration={dur}:sample_rate={SR}[t];"
        f"anoisesrc=color=white:seed={seed}:duration={dur}:amplitude=0.5,"
        f"highpass=f=1800[n];"
        f"[t][n]amix=inputs=2:normalize=0,"
        f"afade=t=in:st=0:d={dur * 0.92:.3f}:curve=exp,"
        f"afade=t=out:st={dur - 0.08:.3f}:d=0.08"
    )


def boom(dur: float, sub_f: float, seed: int) -> str:
    return (
        f"sine=frequency={sub_f}:duration={dur},volume=0.9[b];"
        f"anoisesrc=color=brown:seed={seed}:duration=0.06:amplitude=0.7,"
        f"apad=pad_dur={dur}[k];"
        f"[b][k]amix=inputs=2:normalize=0,lowpass=f=220,"
        f"afade=t=in:st=0:d=0.006,"
        f"afade=t=out:st=0.08:d={dur - 0.08:.3f}:curve=exp"
    )


def impact(dur: float, seed: int) -> str:
    return (
        f"sine=frequency=95:duration={dur},volume=0.8[b];"
        f"anoisesrc=color=brown:seed={seed}:duration=0.04:amplitude=0.8,"
        f"apad=pad_dur={dur}[k];"
        f"[b][k]amix=inputs=2:normalize=0,lowpass=f=900,"
        f"afade=t=in:st=0:d=0.004,"
        f"afade=t=out:st=0.03:d={dur - 0.03:.3f}:curve=exp"
    )


def subdrop(dur: float, f0: float, f1: float) -> str:
    return (
        f"aevalsrc=exprs={chirp_expr(f0, f1, dur, amp=0.85)}:"
        f"duration={dur}:sample_rate={SR},lowpass=f=220,"
        f"afade=t=in:st=0:d=0.02,"
        f"afade=t=out:st={dur * 0.45:.3f}:d={dur * 0.55:.3f}:curve=hsin"
    )


def tick(dur: float, freq: float) -> str:
    return (
        f"sine=frequency={freq}:duration={dur},highpass=f=300,"
        f"afade=t=in:st=0:d=0.003,"
        f"afade=t=out:st=0.01:d={dur - 0.01:.3f}:curve=exp"
    )


def blip(dur: float, freq: float) -> str:
    return (
        f"sine=frequency={freq}:duration={dur}[a];"
        f"sine=frequency={freq * 2.0}:duration={dur},volume=0.3[b];"
        f"[a][b]amix=inputs=2:normalize=0,bandpass=f={freq}:width_type=o:w=2,"
        f"afade=t=in:st=0:d=0.005,"
        f"afade=t=out:st=0.05:d={dur - 0.05:.3f}:curve=exp"
    )


def amb_rain(dur: float, s1: int, s2: int) -> str:
    return (
        f"anoisesrc=color=white:seed={s1}:duration={dur}:amplitude=0.55,"
        f"highpass=f=1200,lowpass=f=8500,tremolo=f=0.2:d=0.15[hi];"
        f"anoisesrc=color=brown:seed={s2}:duration={dur}:amplitude=0.55,"
        f"lowpass=f=420[lo];"
        f"[hi][lo]amix=inputs=2:weights=0.7 0.55:normalize=0"
    )


def amb_highway(dur: float, s1: int, s2: int) -> str:
    return (
        f"anoisesrc=color=brown:seed={s1}:duration={dur}:amplitude=0.75,"
        f"lowpass=f=700,tremolo=f=0.1:d=0.35[low];"
        f"anoisesrc=color=pink:seed={s2}:duration={dur}:amplitude=0.4,"
        f"bandpass=f=1600:width_type=o:w=2[tire];"
        f"[low][tire]amix=inputs=2:weights=0.8 0.4:normalize=0"
    )


def amb_engine(dur: float, seed: int) -> str:
    return (
        f"sine=frequency=62:duration={dur},volume=0.8[a];"
        f"sine=frequency=124:duration={dur},volume=0.35[b];"
        f"anoisesrc=color=brown:seed={seed}:duration={dur}:amplitude=0.4,"
        f"lowpass=f=320[c];"
        f"[a][b][c]amix=inputs=3:normalize=0,tremolo=f=11:d=0.5,lowpass=f=380"
    )


def amb_wind(dur: float, seed: int) -> str:
    return (
        f"anoisesrc=color=pink:seed={seed}:duration={dur}:amplitude=0.7,"
        f"bandpass=f=520:width_type=o:w=2.2,tremolo=f=0.15:d=0.55,"
        f"flanger=depth=2:speed=0.3,lowpass=f=3200"
    )


def amb_road_1920(dur: float, seed: int) -> str:
    return (
        f"sine=frequency=45:duration={dur},volume=0.5[a];"
        f"anoisesrc=color=brown:seed={seed}:duration={dur}:amplitude=0.75,"
        f"lowpass=f=150[b];"
        f"[a][b]amix=inputs=2:normalize=0,tremolo=f=6:d=0.4,lowpass=f=210"
    )


# (filename, category, duration, graph, human_description)
PALETTE: list[tuple[str, str, float, str, str]] = [
    # --- whoosh variants (short/high, med/mid, long/low) ---
    ("sfx_whoosh_v2_short.mp3", "sfx", 0.55, whoosh(0.55, 1200, 9000, 101), "short high-pitched transition whoosh"),
    ("sfx_whoosh_v2_med.mp3",   "sfx", 1.00, whoosh(1.00, 500, 6000, 102),  "medium mid-pitched pass-by whoosh"),
    ("sfx_whoosh_v2_long.mp3",  "sfx", 1.80, whoosh(1.80, 180, 3500, 103),  "long low sweeping whoosh"),
    # --- riser variants ---
    ("sfx_riser_v2_1s.mp3",     "sfx", 1.20, riser(1.20, 111), "tight 1.2 s rising tension swell"),
    ("sfx_riser_v2_3s.mp3",     "sfx", 3.00, riser(3.00, 112), "long 3 s reveal riser"),
    # --- boom / impact ---
    ("sfx_boom_v2_deep.mp3",    "sfx", 1.80, boom(1.80, 46, 121), "deep cinematic bass boom"),
    ("sfx_impact_v2_tight.mp3", "sfx", 0.60, impact(0.60, 122),   "tight punchy low impact"),
    # --- sub-drop variants ---
    ("sfx_subdrop_v2_a.mp3",    "sfx", 1.40, subdrop(1.40, 88, 34),  "sub-drop A (88->34 Hz)"),
    ("sfx_subdrop_v2_b.mp3",    "sfx", 2.20, subdrop(2.20, 72, 26),  "sub-drop B deeper/longer (72->26 Hz)"),
    # --- ui-tick pitch variants ---
    ("sfx_tick_v2_hi.mp3",      "sfx", 0.18, tick(0.18, 1760), "high ui-tick"),
    ("sfx_tick_v2_lo.mp3",      "sfx", 0.22, tick(0.22, 880),  "low ui-tick"),
    # --- data-blip pitch variants ---
    ("sfx_blip_v2_hi.mp3",      "sfx", 0.30, blip(0.30, 1200), "high data-blip"),
    ("sfx_blip_v2_lo.mp3",      "sfx", 0.35, blip(0.35, 700),  "low data-blip"),
    # --- ambience beds the EP32 script needs (missing) ---
    ("amb_rain_street.mp3",        "ambience", 22.0, amb_rain(22.0, 201, 202),  "rain on a street"),
    ("amb_highway_traffic.mp3",    "ambience", 22.0, amb_highway(22.0, 211, 212), "night highway / traffic wash"),
    ("amb_engine_idle.mp3",        "ambience", 22.0, amb_engine(22.0, 221),      "car engine idle hum"),
    ("amb_light_wind.mp3",         "ambience", 22.0, amb_wind(22.0, 231),        "light wind"),
    ("amb_road_rumble_1920s.mp3",  "ambience", 22.0, amb_road_1920(22.0, 241),   "1920s-road low rumble"),
]


def synthesize(name: str, category: str, graph: str, lib: Path,
               dry_run: bool) -> dict:
    out_path = lib / category / name
    tmp = SCRATCH / f"_gen_{name}.wav"
    result = {"file": str(out_path), "category": category}
    if dry_run:
        result["status"] = "planned"
        return result

    # 1) synthesize raw wav from the lavfi graph
    r1 = run(["ffmpeg", "-y", "-f", "lavfi", "-i", graph,
              "-ac", "2", "-ar", str(SR), str(tmp)])
    if r1.returncode != 0 or not tmp.exists():
        result["status"] = "error"
        result["stderr_tail"] = r1.stderr[-600:]
        return result

    # 2) measure and compute normalization gain
    peak, rms = measure(tmp)
    if category == "ambience":
        ref, target = rms, BED_RMS_TARGET_DB
    else:
        ref, target = peak, SFX_PEAK_TARGET_DB
    gain_db = 0.0
    if ref is not None and ref > -120.0:
        gain_db = round(target - ref, 2)

    # 3) apply gain + encode mp3 (atomic-ish: ffmpeg writes final path directly)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    r2 = run(["ffmpeg", "-y", "-i", str(tmp), "-af", f"volume={gain_db}dB",
              "-ar", str(SR), "-ac", "2", "-c:a", "libmp3lame",
              "-b:a", MP3_BITRATE, str(out_path)])
    try:
        tmp.unlink()
    except OSError:
        pass
    if r2.returncode != 0 or not out_path.exists():
        result["status"] = "error"
        result["stderr_tail"] = r2.stderr[-600:]
        return result

    dur = ffprobe_duration(out_path)
    fpeak, frms = measure(out_path)
    result.update({
        "status": "ok",
        "duration_sec": round(dur, 3) if dur else None,
        "applied_gain_db": gain_db,
        "final_peak_db": fpeak,
        "final_rms_db": frms,
    })
    return result


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser(description="Synthesize a rights-free SFX + ambience palette with ffmpeg.")
    ap.add_argument("--dry-run", action="store_true", help="print the plan; synthesize nothing")
    args = ap.parse_args()

    lib = media_root() / "library"
    SCRATCH.mkdir(parents=True, exist_ok=True)

    print(f"library root: {lib}")
    print(f"palette: {len(PALETTE)} files "
          f"({sum(1 for _n, c, *_ in PALETTE if c == 'sfx')} sfx, "
          f"{sum(1 for _n, c, *_ in PALETTE if c == 'ambience')} ambience)")
    print("-" * 68)

    rows: list[dict] = []
    ok = 0
    for name, category, _dur, graph, desc in PALETTE:
        row = synthesize(name, category, graph, lib, args.dry_run)
        row["description"] = desc
        rows.append(row)
        if row["status"] == "ok":
            ok += 1
            print(f"OK   {category:9s} {name:28s} "
                  f"dur={row['duration_sec']}s peak={row['final_peak_db']}dB rms={row['final_rms_db']}dB")
        elif row["status"] == "planned":
            print(f"PLAN {category:9s} {name}")
        else:
            print(f"FAIL {category:9s} {name}: {row.get('stderr_tail', '')[:200]}")

    print("-" * 68)
    if args.dry_run:
        print(f"dry-run: {len(PALETTE)} files planned (nothing written)")
    else:
        print(f"synthesized {ok}/{len(PALETTE)} files into {lib}")
    return 0 if (args.dry_run or ok == len(PALETTE)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
