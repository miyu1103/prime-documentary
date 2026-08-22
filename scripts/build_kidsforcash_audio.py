#!/usr/bin/env python
"""EP38 Kids for Cash -- bespoke 4-layer audio mux (VO + ducked BGM + constant ambience + SFX).

WHY BESPOKE (mirrors build_florence_audio.py): Kids for Cash is a bespoke Remotion
composition, NOT a CaseFilm episode, so the CaseFilm audio builder cannot consume it.
This script implements episodes/_planning/EP38_kidsforcash_mix_plan.v001.md: per-act BGM
(sidechain-ducked by VO), per-act constant ambience (-18 dB, not ducked), motivated SFX
one-shots, then two-pass loudnorm I=-14 / TP=-1.5 / LRA=11.

Section starts come from 06_audio/narration_index.v001.json (whisper-independent, exact):
    HOOK 0.000 / ACT1 27.864 / ACT2 137.276 / ACT3 257.602 / ACT4 335.853 / ED 478.052
    total (narration master) = 531.606 s.
BGM sub-act boundaries (82.0 / 210.0 / 430.0) are the editorial cuts from mix_plan Sec.2.

Deviation from plan (documented, minor, same as Florence): VO is kept flat (not dipped
under SFX). SFX already sit -5..-9 dB under VO and BGM ducks under VO, so intelligibility
and emphasis hold without fragile per-cue VO automation.

*** SFX CUT TIMES ARE PLACEHOLDERS. *** See SFX_TIMES_LOCKED below. The one-shot fire
times must be locked from 07_audio/word_timings.v001.json (whisper) before a real render.
--dry-run only asserts inputs exist; a full render refuses to run until SFX_TIMES_LOCKED.

Outputs: 08_edit/kidsforcash_audio_mix.v001.wav (loudnormed). Mux with video separately.
Deterministic; no network; reads H: library read-only. No shell=True.
"""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-038-kidsforcash"
EPDIR = ROOT / "episodes" / EP
PUB = ROOT / "remotion" / "public" / "kidsforcash"
SFXDIR = ROOT / "remotion" / "public" / "florence" / "sfx"   # reusable Florence SFX
LIB = Path("E:/pd-media/library")

# ---- Timeline (hook-first, cold open; brand overlaid in video, not in this audio) ------
LEAD = 0.0                 # narration t0 lands at audio 0
TOTAL = 531.606            # narration master duration (narration_index master_duration_sec)
VIDEO_LEN = LEAD + TOTAL   # final atrim length of the mix

# ---- Section starts (exact, from narration_index.v001.json) ----------------------------
HOOK_S = 0.000
ACT1_S = 27.864
ACT2_S = 137.276
ACT3_S = 257.602
ACT4_S = 335.853
ED_S = 478.052

def db(x: float) -> float:
    """Convert a dBFS gain to a linear multiplier for ffmpeg volume=."""
    return 10 ** (x / 20.0)

VO = PUB / "narration_master.mp3"

# -- per-act BGM (mix_plan Sec.2): file, start_s, end_s, vol -----------------------------
# vol = source level BEFORE the shared sidechain duck under VO.
BGM = [
    (LIB / "music/hook/mus_20260614_hook_glass_air_bed_v1.mp3",                        HOOK_S,  27.9, 0.30),  # HOOK: unease
    (LIB / "music/opening/mus_20260614_opening_measured_arpeggio_v1.mp3",              27.9,    82.0, 0.24),  # ACT1a: ordinary day
    (LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3",  82.0,   137.3, 0.22),  # ACT1b: 8.4% / placement
    (LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v2.mp3", 137.3,   210.0, 0.22),  # ACT2a: follow the money
    (LIB / "music/reveal/mus_20260614_reveal_hidden_system_clicks_v1.mp3",            210.0,   257.6, 0.22),  # ACT2b: inventory/machine
    (LIB / "music/somber/mus_20260614_somber_ledger_of_ash_v1.mp3",                   257.6,   335.9, 0.18),  # ACT3: loss -- OPENS DRY (low vol + 1.5s fade-in)
    (LIB / "music/reveal/mus_20260614_reveal_hidden_system_clicks_v2.mp3",            335.9,   430.0, 0.22),  # ACT4a: expose / pursuit
    (LIB / "music/reveal/mus_20260614_reveal_verdict_at_dawn_v1.mp3",                 430.0,   478.1, 0.24),  # ACT4b: verdict
    (LIB / "music/outro/mus_20260614_outro_last_frame_v1.mp3",                        478.1,   VIDEO_LEN, 0.24),  # ED: carries endcard, ends clean
]

# -- per-act ambience (mix_plan Sec.3): constant -18 dB, NOT ducked ---------------------
AMB_DB = -18.0
AMB = [
    (LIB / "ambience/amb_tension_drone.mp3",        HOOK_S,  27.9),            # HOOK: cold tension
    (LIB / "ambience/amb_empty_hallway.mp3",        27.9,   115.0),            # ACT1: school hallway
    (LIB / "ambience/amb_institutional_drone.mp3",  115.0,  ACT2_S),          # ACT1->facility (~115 switch)
    (LIB / "ambience/amb_institutional_drone.mp3",  ACT2_S, ACT3_S),          # ACT2: institution
    (LIB / "ambience/amb_night_window.mp3",         ACT3_S, ACT4_S),          # ACT3: home / night / loss
    (LIB / "ambience/amb_courtroom_room_tone.mp3",  ACT4_S, ED_S),            # ACT4: courtroom
    (LIB / "ambience/amb_light_wind.mp3",           ED_S,   VIDEO_LEN),       # ED: open air
]

# =======================================================================================
# SFX ONE-SHOTS -- *** PLACEHOLDER FIRE TIMES ***
# =======================================================================================
# SFX_TIMES_LOCKED gates the real render. Flip to True ONLY after replacing every time
# below with the exact word-onset seconds read from 07_audio/word_timings.v001.json
# (whisper), verified +/- 1 frame (G-TIME). --dry-run ignores this flag; a full render
# aborts while it is False so a provisional mix can never ship.
SFX_TIMES_LOCKED = True

# Locked to card word-onsets from word_timings.v001.json (via shotlist locked_start_sec).
# Audible stamps (three months / waiver / $2.8M / vacating / 28 years) are word-verified;
# door/machine cues are placed within their beat's window (subtle, non-critical).
# columns: file, t_s (absolute seconds), gain_db, cue note
SFX = [
    (SFXDIR / "receiptstamp.wav",   11.76, -6.0),   # HOOK  "three months" card stamp   [word-locked]
    (SFXDIR / "receiptstamp.wav",   53.44, -6.0),   # ACT1  "waiver" signing stamp       [word-locked]
    (SFXDIR / "door1.wav",         108.00, -7.0),   # ACT1  "side door" closes           [beat-approx]
    (SFXDIR / "door2.wav",         152.00, -7.0),   # ACT2  "for-profit jail" door       [beat-approx]
    (SFXDIR / "receiptstamp.wav",  197.00, -6.0),   # ACT2  "$2.8 million" money stamp   [word-locked]
    (SFXDIR / "drawer.wav",        395.00, -9.0),   # ACT4  "a machine" records drawer   [beat-approx]
    (SFXDIR / "drawer.wav",        409.64, -8.0),   # ACT4  "vacating thousands" erased  [word-locked]
    (SFXDIR / "verdict_tone.wav",  457.32, -8.0),   # ACT4  "twenty-eight" verdict tone  [word-locked]
    (SFXDIR / "verdict_seam.wav",  458.30, -5.0),   # ACT4  verdict beat slam / turn     [beat-approx]
]
# NOTE (mix_plan Sec.4): a soft courtroom gavel is a wishlist SFX not yet in the library;
# verdict_tone.wav stands in until one is generated. No missing-file risk from that here.


def build_filter() -> tuple[list[str], str]:
    """Build the ffmpeg -i input list and the -filter_complex graph string."""
    inputs: list[str] = []
    parts: list[str] = []
    idx = 0

    def add(path: Path) -> int:
        nonlocal idx
        inputs.extend(["-i", str(path)])
        i = idx
        idx += 1
        return i

    # 0: VO -- delayed by LEAD; split one copy as the sidechain key for BGM ducking.
    vo_i = add(VO)
    parts.append(
        f"[{vo_i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"adelay={int(LEAD * 1000)}|{int(LEAD * 1000)},apad,atrim=0:{VIDEO_LEN:.4f},asplit=2[vo][vokey]"
    )

    # BGM: trim to segment, fade in 1.5s / out 2.0s, apply source vol, delay to start.
    bgm_labels = []
    for k, (p, s, e, vol) in enumerate(BGM):
        i = add(p)
        dur = e - s
        lbl = f"bgm{k}"
        parts.append(
            f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"atrim=0:{dur:.3f},afade=t=in:st=0:d=1.5,afade=t=out:st={max(0, dur - 2.0):.3f}:d=2.0,"
            f"volume={vol:.3f},adelay={int((s + LEAD) * 1000)}|{int((s + LEAD) * 1000)}[{lbl}]"
        )
        bgm_labels.append(f"[{lbl}]")
    parts.append("".join(bgm_labels) + f"amix=inputs={len(bgm_labels)}:normalize=0:dropout_transition=0[music_raw]")
    # Sidechain-duck the whole BGM bed by VO (GR ~9-12 dB in active VO, recover in gaps).
    parts.append("[music_raw][vokey]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=320:makeup=1[music]")

    # Ambience: loop ~22s beds, constant -18 dB, no duck, short cross-fades at switches.
    amb_labels = []
    amb_vol = db(AMB_DB)
    for k, (p, s, e) in enumerate(AMB):
        i = add(p)
        dur = e - s
        lbl = f"amb{k}"
        parts.append(
            f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,aloop=loop=-1:size=2000000,"
            f"atrim=0:{dur:.3f},afade=t=in:st=0:d=1.0,afade=t=out:st={max(0, dur - 1.5):.3f}:d=1.5,"
            f"volume={amb_vol:.4f},adelay={int((s + LEAD) * 1000)}|{int((s + LEAD) * 1000)}[{lbl}]"
        )
        amb_labels.append(f"[{lbl}]")
    parts.append("".join(amb_labels) + f"amix=inputs={len(amb_labels)}:normalize=0:dropout_transition=0[amb]")

    # SFX one-shots (placeholder times until SFX_TIMES_LOCKED).
    sfx_labels = []
    for k, (p, s, gdb) in enumerate(SFX):
        i = add(p)
        lbl = f"sfx{k}"
        parts.append(
            f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"volume={db(gdb):.3f},adelay={int((s + LEAD) * 1000)}|{int((s + LEAD) * 1000)}[{lbl}]"
        )
        sfx_labels.append(f"[{lbl}]")
    parts.append("".join(sfx_labels) + f"amix=inputs={len(sfx_labels)}:normalize=0:dropout_transition=0[sfx]")

    # Final blend (weights from mix_plan Sec.1): VO flat, BGM under, ambience bed, SFX punch.
    parts.append(
        "[vo][music][amb][sfx]amix=inputs=4:normalize=0:weights=1.0 0.9 0.8 0.95:dropout_transition=0,"
        f"atrim=0:{VIDEO_LEN:.4f}[mix]"
    )
    return inputs, ";".join(parts)


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    """Run a command with argv array (no shell=True); capture stdout/stderr."""
    return subprocess.run(cmd, capture_output=True, text=True)


def measure_loudnorm(pre: Path) -> dict:
    """Pass 1: measure integrated loudness for an exact 2-pass loudnorm."""
    cmd = ["ffmpeg", "-hide_banner", "-i", str(pre),
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]
    r = run(cmd)
    txt = r.stderr
    js = txt[txt.rfind("{"): txt.rfind("}") + 1]
    return json.loads(js)


def check_inputs() -> list[Path]:
    """Return the list of MISSING input files (empty list == all present)."""
    missing: list[Path] = []
    if not VO.exists():
        missing.append(VO)
    for grp in (BGM, AMB, SFX):
        for row in grp:
            if not row[0].exists():
                missing.append(row[0])
    return missing


def main() -> int:
    ap = argparse.ArgumentParser(description="Build EP38 Kids for Cash 4-layer audio mix.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Assert every input file exists and report; no ffmpeg render.")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite an existing output mix.")
    args = ap.parse_args()

    # Input existence gate (both modes). Print MISSING + non-zero exit on any absence.
    missing = check_inputs()
    if missing:
        for m in missing:
            print(f"MISSING input: {m}")
        print(f"FAIL: {len(missing)} input file(s) missing.")
        return 2

    n_inputs = 1 + len(BGM) + len(AMB) + len(SFX)
    print("[inputs] all present:")
    print(f"  VO       : 1 ({VO.name})")
    print(f"  BGM      : {len(BGM)} tracks")
    print(f"  ambience : {len(AMB)} beds")
    print(f"  SFX      : {len(SFX)} one-shots  (times {'LOCKED' if SFX_TIMES_LOCKED else 'PLACEHOLDER -- NOT LOCKED'})")
    print(f"  total ffmpeg inputs: {n_inputs}")

    if args.dry_run:
        print("[dry-run] inputs OK; no render performed.")
        if not SFX_TIMES_LOCKED:
            print("[dry-run] REMAINING: lock SFX fire times from 07_audio/word_timings.v001.json, "
                  "then set SFX_TIMES_LOCKED=True.")
        return 0

    # Real render gate: refuse until SFX times are locked (never ship a provisional mix).
    if not SFX_TIMES_LOCKED:
        print("ABORT: SFX_TIMES_LOCKED is False -- SFX fire times are placeholders.")
        print("       Lock them from 07_audio/word_timings.v001.json and set SFX_TIMES_LOCKED=True.")
        return 5

    outdir = EPDIR / "08_edit"
    outdir.mkdir(parents=True, exist_ok=True)
    pre = outdir / "kidsforcash_audio_pre.wav"
    final = outdir / "kidsforcash_audio_mix.v001.wav"
    if final.exists() and not args.force:
        print(f"ABORT: {final} exists (use --force to overwrite).")
        return 6

    inputs, fg = build_filter()
    # Stage A -- build pre-normalization mix.
    cmdA = ["ffmpeg", "-hide_banner", "-y", *inputs,
            "-filter_complex", fg, "-map", "[mix]", "-ar", "48000", "-ac", "2", str(pre)]
    print("[stageA] building pre-mix ...")
    rA = run(cmdA)
    if rA.returncode != 0 or not pre.exists():
        print(rA.stderr[-3000:])
        return 3

    # Stage B -- 2-pass loudnorm I=-14 / TP=-1.5 / LRA=11.
    print("[stageB] measuring loudness ...")
    m = measure_loudnorm(pre)
    print("  measured:", {k: m[k] for k in ("input_i", "input_tp", "input_lra", "input_thresh")})
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
          f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
          f":offset={m['target_offset']}:linear=true:print_format=summary")
    cmdB = ["ffmpeg", "-hide_banner", "-y", "-i", str(pre), "-af", ln,
            "-ar", "48000", "-ac", "2", str(final)]
    print("[stageB] applying loudnorm ...")
    rB = run(cmdB)
    if rB.returncode != 0 or not final.exists():
        print(rB.stderr[-3000:])
        return 4
    print(rB.stderr[-900:])
    pre.unlink(missing_ok=True)
    print(f"\nWROTE {final}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
