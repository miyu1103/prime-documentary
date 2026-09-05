#!/usr/bin/env python3
r"""Independent stem-loudness gate — VO must sit clearly above the music bed.

The owner's recurring audio defect is a music bed that swims up over the narration (or a
mixed delivery that ships too quiet / too hot). This gate measures INTEGRATED loudness
(EBU R128, ffmpeg's ebur128) and fails on two distinct failure modes depending on what
artifacts the episode actually has:

  STEM MODE (both a VO stem AND a music/bed stem exist as separate files under 06_audio):
    Measure integrated LUFS of each stem and FAIL if
      * the VO does NOT sit at least ~VO_OVER_MUSIC_MIN_LU (8 LU) above the music bed, or
      * the music bed is louder than ~MUSIC_MAX_LUFS (-20 LUFS) in absolute terms.
    This directly measures the INTENT ("voice clearly above the bed"), stem-vs-stem, so a
    bed that was mixed too hot cannot ship.

  MIX MODE (only the mixed final render exists — the normal PD CaseFilm case, where the
  video renders VO-only and BGM is mixed in post from the H: library, leaving no episode-
  local music stem to compare against):
    We cannot honestly compute a stem ratio (there is no separate bed file), so we SKIP the
    ratio honestly and instead measure the mixed render's overall integrated loudness against
    the delivery band (target -14 LUFS, band -16..-12) and gate on that.

It never trusts a self-reported number: it re-measures the actual audio bytes with ffmpeg.
It never crashes the caller — a missing/undecodable artifact returns a skip, not an exception.

Honest limitation: in MIX MODE the true VO-vs-bed ratio is NOT measured (you cannot separate
a bed back out of a finished mix), so a mix whose overall loudness is in-band but whose bed is
still too hot would pass here. That ratio is only enforced when real per-stem files exist. This
gate also does not judge spectral masking, ducking dynamics, or per-scene dips — only integrated
loudness (the ship-blocking, measurable delivery property).

Usage:
  py -3.11 scripts/check_stem_loudness.py --ep PD-2026-031-unlock
  py -3.11 scripts/check_stem_loudness.py --ep PD-2026-031-unlock --dry-run
  py -3.11 scripts/check_stem_loudness.py --ep PD-2026-031-unlock --json out.json
  py -3.11 scripts/check_stem_loudness.py --selftest

Exit codes: 0 = PASS or --dry-run (plan only, no measurement); 1 = FAIL or usage error.

check_final_acceptance can import this module and call evaluate(epdir); the returned dict
follows its gate contract: {"check","ok","hard","reason", ...extra numbers...}, with
{"ok": True, "hard": False, "skipped": True, "reason": ...} when nothing is measurable.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import struct
import subprocess
import sys
import tempfile
import wave
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-031-unlock"

# --- thresholds (named, not magic; do not weaken to make a target pass) --------------------------
VO_OVER_MUSIC_MIN_LU = 8.0     # VO integrated LUFS must be >= this many LU ABOVE the music stem
MUSIC_MAX_LUFS = -20.0         # music stem integrated LUFS must be <= this (louder bed = FAIL)
MIX_TARGET_LUFS = -14.0        # delivery target for the mixed render
MIX_LO_LUFS = -16.0            # mixed render must be within [MIX_LO, MIX_HI]
MIX_HI_LUFS = -12.0

_I_RE = re.compile(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS")

# stem discovery: filename hints (case-insensitive substring match on the stem's name)
_VO_HINTS = ("vo", "voice", "narr", "vox", "dialog", "speech")
_MUSIC_HINTS = ("music", "bgm", "bed", "score", "bass", "track")
_AUDIO_EXT = (".wav", ".flac", ".mp3", ".m4a", ".aac", ".ogg", ".opus")


# ---------------------------------------------------------------------------------------------
# loudness measurement (EBU R128 integrated, via ffmpeg ebur128) — reads the real bytes
# ---------------------------------------------------------------------------------------------

def measure_lufs(path: Path, timeout: int = 900) -> Optional[float]:
    """Integrated loudness (LUFS) of `path`'s first audio stream, or None if unmeasurable.

    Uses the same ebur128 summary line as check_final_acceptance.check_loudness so the two
    gates agree on the number. Returns None (never raises) when ffmpeg is missing, the file
    has no decodable audio, or no `I: .. LUFS` summary is produced.
    """
    try:
        out = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
             "-map", "0:a:0?", "-af", "ebur128=framelog=quiet", "-f", "null", os.devnull],
            capture_output=True, text=True, timeout=timeout)
    except Exception:  # noqa: BLE001 - ffmpeg missing / spawn failure -> unmeasurable
        return None
    m = _I_RE.findall(out.stderr)
    if not m:
        return None
    try:
        val = float(m[-1])
    except ValueError:
        return None
    if not math.isfinite(val):  # ebur128 can print -inf/-70 for silence; treat -inf as unusable
        return None
    return val


# ---------------------------------------------------------------------------------------------
# artifact discovery (episode-local only — no H: library, which is pre-duck source, not a stem)
# ---------------------------------------------------------------------------------------------

def _stem_dirs(epdir: Path) -> list[Path]:
    """Directories where per-stem audio would live if a stem export exists."""
    a = epdir / "06_audio"
    return [a / "stems", a / "mix" / "stems", a / "07_mix", a / "music"]


def _audio_files(d: Path) -> list[Path]:
    if not d.is_dir():
        return []
    return sorted(p for p in d.iterdir()
                  if p.is_file() and p.suffix.lower() in _AUDIO_EXT)


def _pick(files: list[Path], hints: tuple[str, ...]) -> Optional[Path]:
    """Highest-versioned file whose name contains any hint (case-insensitive)."""
    hit = [p for p in files if any(h in p.name.lower() for h in hints)]
    return sorted(hit)[-1] if hit else None


def find_vo_stem(epdir: Path) -> Optional[Path]:
    """A dedicated VO/voice/narration stem file, else the narration master (the pure VO)."""
    for d in _stem_dirs(epdir):
        p = _pick(_audio_files(d), _VO_HINTS)
        if p:
            return p
    masters = sorted((epdir / "06_audio" / "narration" / "raw").glob("narration_master.v*.mp3"))
    return masters[-1] if masters else None


def find_music_stem(epdir: Path) -> Optional[Path]:
    """A dedicated music/BGM/bed stem file rendered for THIS episode, or None.

    Only episode-local stems count. The H: music library holds pre-duck, pre-loudnorm source
    tracks, not the bed as it sits in the mix, so measuring those would misrepresent the ratio.
    """
    for d in _stem_dirs(epdir):
        p = _pick(_audio_files(d), _MUSIC_HINTS)
        if p:
            return p
    return None


def find_mix_render(epdir: Path) -> Optional[Path]:
    """Highest-versioned mixed final render (*final*.mp4) under 08_edit/renders."""
    renders = epdir / "08_edit" / "renders"
    if not renders.is_dir():
        return None
    finals = sorted(p for p in renders.glob("*final*.mp4") if p.is_file())
    return finals[-1] if finals else None


# ---------------------------------------------------------------------------------------------
# core evaluation (importable by check_final_acceptance)
# ---------------------------------------------------------------------------------------------

def evaluate(epdir: Path) -> dict[str, Any]:
    """Measure stem/ mix loudness and return a check_final_acceptance-compatible gate dict.

    Never calls sys.exit and never raises on missing inputs. Keys:
      check, ok, hard, reason, mode, and (when measured) vo_stem, music_stem, vo_lufs,
      music_lufs, margin_lu, mix_render, mix_lufs. Absent artifact -> skipped/ok honest skip.
    """
    epdir = Path(epdir)
    vo = find_vo_stem(epdir)
    music = find_music_stem(epdir)

    # -------- STEM MODE: both a VO stem and a music stem exist -> measure the real ratio -------
    if vo is not None and music is not None:
        vo_lufs = measure_lufs(vo)
        music_lufs = measure_lufs(music)
        if vo_lufs is None or music_lufs is None:
            missing = "VO" if vo_lufs is None else "music"
            return {"check": "stem_loudness", "ok": True, "hard": False, "skipped": True,
                    "mode": "stem", "vo_stem": str(vo), "music_stem": str(music),
                    "reason": f"stems present but {missing} stem was unmeasurable "
                              f"(ffmpeg/ebur128 gave no integrated LUFS)"}
        margin = vo_lufs - music_lufs
        problems: list[str] = []
        if margin < VO_OVER_MUSIC_MIN_LU:
            problems.append(f"VO only {margin:+.1f} LU above music "
                            f"(need >= {VO_OVER_MUSIC_MIN_LU:.0f} LU; bed too loud vs voice)")
        if music_lufs > MUSIC_MAX_LUFS:
            problems.append(f"music bed {music_lufs:.1f} LUFS is louder than "
                            f"{MUSIC_MAX_LUFS:.0f} LUFS (absolute bed too hot)")
        ok = not problems
        reason = (f"VO {vo_lufs:.1f} LUFS sits {margin:+.1f} LU above music "
                  f"{music_lufs:.1f} LUFS; bed within absolute limit" if ok
                  else "; ".join(problems))
        return {"check": "stem_loudness", "ok": ok, "hard": True, "mode": "stem",
                "reason": reason, "vo_stem": str(vo), "music_stem": str(music),
                "vo_lufs": vo_lufs, "music_lufs": music_lufs, "margin_lu": margin}

    # -------- MIX MODE: no music stem -> gate the mixed render's overall loudness ---------------
    mix = find_mix_render(epdir)
    if mix is None:
        return {"check": "stem_loudness", "ok": True, "hard": False, "skipped": True,
                "mode": "none", "reason": "no music stem and no *final*.mp4 render present "
                                          "(nothing to measure — likely on SSD)"}
    mix_lufs = measure_lufs(mix)
    if mix_lufs is None:
        return {"check": "stem_loudness", "ok": True, "hard": False, "skipped": True,
                "mode": "mix", "mix_render": str(mix),
                "reason": f"mixed render present but unmeasurable via ebur128: {mix}"}
    ok = MIX_LO_LUFS <= mix_lufs <= MIX_HI_LUFS
    ratio_note = ("no separate music stem — VO-vs-bed ratio NOT measured (cannot unmix a "
                  "finished render); measuring overall delivery loudness only")
    reason = (f"mixed render {mix_lufs:.1f} LUFS within band "
              f"{MIX_LO_LUFS:.0f}..{MIX_HI_LUFS:.0f} (target {MIX_TARGET_LUFS:.0f}); {ratio_note}"
              if ok else
              f"mixed render {mix_lufs:.1f} LUFS OUTSIDE band "
              f"{MIX_LO_LUFS:.0f}..{MIX_HI_LUFS:.0f} (target {MIX_TARGET_LUFS:.0f}); {ratio_note}")
    return {"check": "stem_loudness", "ok": ok, "hard": True, "mode": "mix",
            "reason": reason, "mix_render": str(mix), "mix_lufs": mix_lufs,
            "ratio_measured": False}


# ---------------------------------------------------------------------------------------------
# reporting + atomic json
# ---------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    print("\n" + "=" * 74)
    print(f"STEM LOUDNESS GATE   (mode: {r.get('mode', '?')})")
    print("=" * 74)
    if r.get("mode") == "stem":
        if "vo_lufs" in r:
            print(f"  VO stem     : {r['vo_stem']}")
            print(f"                {r['vo_lufs']:.1f} LUFS")
            print(f"  music stem  : {r['music_stem']}")
            print(f"                {r['music_lufs']:.1f} LUFS")
            print(f"  VO above bed: {r['margin_lu']:+.1f} LU "
                  f"(need >= {VO_OVER_MUSIC_MIN_LU:.0f}; bed cap {MUSIC_MAX_LUFS:.0f} LUFS)")
        else:
            print(f"  VO stem     : {r.get('vo_stem')}")
            print(f"  music stem  : {r.get('music_stem')}")
    elif r.get("mode") == "mix":
        print(f"  mixed render: {r.get('mix_render')}")
        if "mix_lufs" in r:
            print(f"                {r['mix_lufs']:.1f} LUFS  "
                  f"(band {MIX_LO_LUFS:.0f}..{MIX_HI_LUFS:.0f}, target {MIX_TARGET_LUFS:.0f})")
        print("  note        : stem ratio SKIPPED (no separate music stem to compare)")
    print("-" * 74)
    if r.get("skipped"):
        print(f"  RESULT: SKIP (honest) — {r['reason']}")
    elif r.get("ok"):
        print(f"  RESULT: PASS — {r['reason']}")
    else:
        print(f"  RESULT: FAIL — {r['reason']}")
    print("-" * 74)


def _atomic_write_json(path: Path, obj: dict[str, Any]) -> None:
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
# selftest: RED fixture (known-bad stems -> must FAIL) + real TEST_EP measurement
# ---------------------------------------------------------------------------------------------

def _write_noise_wav(path: Path, amplitude: float, seconds: float = 2.0,
                     rate: int = 48000, seed: int = 0) -> None:
    """Write a deterministic white-noise mono WAV at a given peak amplitude (0..1).

    Deterministic (seeded LCG, no numpy/random import) so the fixture never flakes. A louder
    amplitude yields a higher integrated LUFS, letting us stage a known-bad stem balance.
    """
    n = int(seconds * rate)
    # simple deterministic LCG in [-1, 1]
    state = (seed * 2654435761 + 12345) & 0xFFFFFFFF
    frames = bytearray()
    peak = int(amplitude * 32767)
    for _ in range(n):
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        # map to [-1,1)
        x = (state / 0x3FFFFFFF) - 1.0
        frames += struct.pack("<h", max(-32768, min(32767, int(x * peak))))
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(bytes(frames))


def _selftest() -> int:
    print("SELFTEST — stem loudness gate\n")
    ok_all = True

    # (a) RED FIXTURE: synthesize a known-BAD stem balance in a temp episode.
    #     music noise is loud (amplitude 0.30) and VO is only slightly louder (0.40) -> both the
    #     8-LU margin AND the -20 LUFS bed cap are violated -> the gate MUST report ok=False.
    with tempfile.TemporaryDirectory() as td:
        ep = Path(td) / "PD-9999-redfixture"
        stems = ep / "06_audio" / "stems"
        stems.mkdir(parents=True, exist_ok=True)
        _write_noise_wav(stems / "vo_narration.wav", amplitude=0.40, seed=1)
        _write_noise_wav(stems / "music_bed.wav", amplitude=0.30, seed=2)
        red = evaluate(ep)
        print(f"  RED input  : {red.get('mode')} mode, "
              f"vo={red.get('vo_lufs')}, music={red.get('music_lufs')}, "
              f"margin={red.get('margin_lu')}")
        red_failed = (red.get("ok") is False and not red.get("skipped"))
        print("  RED-FIXTURE: PASS" if red_failed else "  RED-FIXTURE: FAIL")
        print(f"    reason: {red.get('reason')}")
        if not red_failed:
            ok_all = False

    # (a2) GREEN control: quiet bed, loud VO -> gate must PASS (proves it discriminates).
    with tempfile.TemporaryDirectory() as td:
        ep = Path(td) / "PD-9999-greenfixture"
        stems = ep / "06_audio" / "stems"
        stems.mkdir(parents=True, exist_ok=True)
        _write_noise_wav(stems / "vo_narration.wav", amplitude=0.50, seed=1)
        _write_noise_wav(stems / "music_bed.wav", amplitude=0.010, seed=2)
        grn = evaluate(ep)
        grn_passed = (grn.get("ok") is True and not grn.get("skipped"))
        print(f"\n  GREEN input: vo={grn.get('vo_lufs')}, music={grn.get('music_lufs')}, "
              f"margin={grn.get('margin_lu')}")
        print("  GREEN-CTRL : PASS" if grn_passed else "  GREEN-CTRL : FAIL")
        print(f"    reason: {grn.get('reason')}")
        if not grn_passed:
            ok_all = False

    # (b) REAL: run evaluate() on the actual TEST EPISODE and print the real numbers.
    print(f"\n  REAL episode: {DEFAULT_EP}")
    real = evaluate(ROOT / "episodes" / DEFAULT_EP)
    _print_report(real)

    print("\nSELFTEST " + ("OK" if ok_all else "FAILED"))
    return 0 if ok_all else 1


# ---------------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------------

def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(
        description="Stem-loudness gate: VO must sit >= 8 LU above the music bed; "
                    "else gate the mixed render's overall loudness to the delivery band.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug under episodes/")
    ap.add_argument("--dry-run", action="store_true",
                    help="resolve artifacts and print the plan; do not measure loudness")
    ap.add_argument("--json", metavar="PATH", default=None,
                    help="also write the result dict to PATH (atomic)")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED fixture + real TEST_EP measurement and exit")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    epdir = ROOT / "episodes" / args.ep
    if not epdir.exists():
        print(f"[ERROR] episode dir not found: {epdir}")
        return 1

    if args.dry_run:
        vo = find_vo_stem(epdir)
        music = find_music_stem(epdir)
        mix = find_mix_render(epdir)
        mode = "stem" if (vo and music) else ("mix" if mix else "none")
        print("DRY-RUN plan (no measurement):")
        print(f"  episode    : {args.ep}")
        print(f"  VO stem    : {vo if vo else '(none)'}")
        print(f"  music stem : {music if music else '(none — stem ratio will be skipped)'}")
        print(f"  mix render : {mix if mix else '(none)'}")
        print(f"  -> mode    : {mode}")
        if mode == "none":
            print("  -> would SKIP honestly (no measurable audio artifact in repo)")
        return 0

    r = evaluate(epdir)
    _print_report(r)
    if args.json:
        _atomic_write_json(Path(args.json), r)
        print(f"\nwrote {args.json}")

    if r.get("skipped"):
        return 0  # honest skip is not a failure
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
