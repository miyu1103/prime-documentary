#!/usr/bin/env python
"""EP37 Florence — bespoke 4-layer audio mux (VO + ducked BGM + constant ambience + SFX).

WHY BESPOKE (not build_case_film_audio.py): Florence is a bespoke Remotion composition
(Florence.tsx), NOT a CaseFilm episode. It has no film_data.v001.json and a single-master
narration_index (no per-chunk timing), so the CaseFilm audio builder cannot consume it.
This script implements 06_audio/mix_plan.v001.md EXACTLY: per-act BGM (sidechain-ducked by
VO), per-act constant ambience (-18 dB, not ducked), 7 motivated SFX one-shots placed at
the assembly_spec cut times, then two-pass loudnorm I=-14 / TP=-1.5 / LRA=11.

Deviations from the plan (documented, minor): VO is kept flat (not dipped under duck_vo
SFX) — the SFX already sit -5..-9 dB under VO and BGM ducks further under the verdict cues,
so intelligibility + emphasis hold without fragile per-cue VO automation.

Outputs: 08_edit/florence_audio_mix.v001.wav (loudnormed). Mux with video separately.
Deterministic; no network; reads H: library read-only.
"""
from __future__ import annotations
import json, math, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-037-florence"
EPDIR = ROOT / "episodes" / EP
PUB = ROOT / "remotion" / "public" / "florence"
LIB = Path("E:/pd-media/library")
# Timeline: BrandOpening (3.5s) + 106-cut body (542.93s) + BrandEndcard (9s) = 555.43s.
# The narration/SFX/BGM/ambience all shift +LEAD so narration t0 lands at the body start
# (after the brand opening); the outro bed + endcard ambience carry the 9s endcard.
LEAD = 0.0                         # hook-first: narration starts at video 0 (cold open); brand overlaid after
BODY_LEN = 16288 / 30.0            # 542.9333s — the 106-cut narrated body
VIDEO_LEN = LEAD + BODY_LEN + 9.0  # 555.4333s — total incl. bookends (final atrim)
ENDCARD_END = BODY_LEN + 9.0       # 551.9333 body-time end for the outro bed / last ambience

def db(x: float) -> float:
    return 10 ** (x / 20.0)

VO = PUB / "narration_master.mp3"

# ── per-act BGM (mix_plan §2): file, start_s, end_s, vol ──────────────────────
BGM = [
    (LIB / "music/hook/mus_20260614_hook_glass_air_bed_v1.mp3",                    0.0,  18.7, 0.30),
    (LIB / "music/opening/mus_20260614_opening_measured_arpeggio_v1.mp3",         18.7,  35.0, 0.30),
    (LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3", 35.0, 115.4, 0.22),
    (LIB / "music/somber/mus_20260614_somber_ledger_of_ash_v1.mp3",             115.4, 258.9, 0.22),
    (LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v2.mp3", 285.0, 443.9, 0.22),  # Act III opens dry
    (LIB / "music/outro/mus_20260614_outro_last_frame_v1.mp3",                  480.0, ENDCARD_END, 0.24),  # outro soft+late, carries the endcard
]

# ── per-act ambience (mix_plan §3): constant −18 dB, not ducked ───────────────
AMB_DB = -18.0
AMB = [
    (LIB / "ambience/amb_rain_street.mp3",          0.0,  18.7),
    (LIB / "ambience/amb_highway_traffic.mp3",     18.7,  35.0),
    (LIB / "ambience/amb_night_window.mp3",        35.0, 115.4),
    (LIB / "ambience/amb_institutional_drone.mp3", 115.4, 258.9),
    (LIB / "ambience/amb_courtroom_room_tone.mp3", 258.9, 443.9),
    (LIB / "ambience/amb_night_window.mp3",        443.9, ENDCARD_END),  # Act IV + endcard bed
]

# ── SFX one-shots (cue sheet gains) placed at assembly_spec cut start times ────
SFX = [
    (PUB / "sfx/receiptstamp.wav",   0.00, -6.0),   # cut1 hook ReceiptStamp
    (PUB / "sfx/receiptstamp.wav",  99.60, -6.0),   # cut21 Act I ReceiptStamp
    (PUB / "sfx/warrant.wav",       63.64, -8.0),   # cut14 WarrantScreen
    (PUB / "sfx/drawer.wav",        91.14, -9.0),   # cut19 RecordsDrawer
    (PUB / "sfx/door1.wav",        115.82, -7.0),   # cut25 first intake door
    (PUB / "sfx/door2.wav",        177.42, -7.0),   # cut38 second facility door
    (PUB / "sfx/verdict_tone.wav", 401.50, -8.0),   # cut81 "April 2, 2012 · five to four"
    (PUB / "sfx/verdict_seam.wav", 405.50, -5.0),   # cut82 CONSTITUTIONAL slam
]

def build_filter() -> tuple[list[str], str]:
    inputs: list[str] = []
    parts: list[str] = []
    idx = 0
    def add(path: Path) -> int:
        nonlocal idx
        inputs.extend(["-i", str(path)])
        i = idx; idx += 1; return i

    # 0: VO — delayed by LEAD so narration t0 lands at the body start (after brand opening)
    vo_i = add(VO)
    parts.append(f"[{vo_i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                 f"adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad,atrim=0:{VIDEO_LEN:.4f},asplit=2[vo][vokey]")

    # BGM
    bgm_labels = []
    for k, (p, s, e, vol) in enumerate(BGM):
        i = add(p)
        dur = e - s
        lbl = f"bgm{k}"
        parts.append(
            f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"atrim=0:{dur:.3f},afade=t=in:st=0:d=1.5,afade=t=out:st={max(0,dur-2.0):.3f}:d=2.0,"
            f"volume={vol:.3f},adelay={int((s+LEAD)*1000)}|{int((s+LEAD)*1000)}[{lbl}]"
        )
        bgm_labels.append(f"[{lbl}]")
    parts.append("".join(bgm_labels) + f"amix=inputs={len(bgm_labels)}:normalize=0:dropout_transition=0[music_raw]")
    # sidechain-duck the whole BGM bed by VO (GR ~9-12 dB in active VO, recover in gaps)
    parts.append("[music_raw][vokey]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=320:makeup=1[music]")

    # Ambience (loop 22s beds, constant −18 dB, no duck)
    amb_labels = []
    amb_vol = db(AMB_DB)
    for k, (p, s, e) in enumerate(AMB):
        i = add(p)
        dur = e - s
        lbl = f"amb{k}"
        parts.append(
            f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,aloop=loop=-1:size=2000000,"
            f"atrim=0:{dur:.3f},afade=t=in:st=0:d=1.0,afade=t=out:st={max(0,dur-1.5):.3f}:d=1.5,"
            f"volume={amb_vol:.4f},adelay={int((s+LEAD)*1000)}|{int((s+LEAD)*1000)}[{lbl}]"
        )
        amb_labels.append(f"[{lbl}]")
    parts.append("".join(amb_labels) + f"amix=inputs={len(amb_labels)}:normalize=0:dropout_transition=0[amb]")

    # SFX one-shots
    sfx_labels = []
    for k, (p, s, gdb) in enumerate(SFX):
        i = add(p)
        lbl = f"sfx{k}"
        parts.append(
            f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"volume={db(gdb):.3f},adelay={int((s+LEAD)*1000)}|{int((s+LEAD)*1000)}[{lbl}]"
        )
        sfx_labels.append(f"[{lbl}]")
    parts.append("".join(sfx_labels) + f"amix=inputs={len(sfx_labels)}:normalize=0:dropout_transition=0[sfx]")

    # Final blend (weights from mix_plan §1)
    parts.append("[vo][music][amb][sfx]amix=inputs=4:normalize=0:weights=1.0 0.9 0.8 0.95:dropout_transition=0,"
                 f"atrim=0:{VIDEO_LEN:.4f}[mix]")
    return inputs, ";".join(parts)

def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)

def measure_loudnorm(pre: Path) -> dict:
    """Pass 1: measure integrated loudness for exact 2-pass normalization."""
    cmd = ["ffmpeg", "-hide_banner", "-i", str(pre),
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]
    r = run(cmd)
    txt = r.stderr
    js = txt[txt.rfind("{"): txt.rfind("}") + 1]
    return json.loads(js)

def main() -> int:
    for grp in (BGM, AMB, SFX):
        for row in grp:
            if not row[0].exists():
                print(f"MISSING input: {row[0]}", file=sys.stderr); return 2
    if not VO.exists():
        print(f"MISSING VO: {VO}", file=sys.stderr); return 2

    outdir = EPDIR / "08_edit"; outdir.mkdir(parents=True, exist_ok=True)
    pre = outdir / "florence_audio_pre.wav"
    final = outdir / "florence_audio_mix.v001.wav"

    inputs, fg = build_filter()
    # Stage A — build pre-normalization mix
    cmdA = ["ffmpeg", "-hide_banner", "-y", *inputs,
            "-filter_complex", fg, "-map", "[mix]", "-ar", "48000", "-ac", "2", str(pre)]
    print("[stageA] building pre-mix ...")
    rA = run(cmdA)
    if rA.returncode != 0 or not pre.exists():
        print(rA.stderr[-3000:], file=sys.stderr); return 3

    # Stage B — 2-pass loudnorm
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
        print(rB.stderr[-3000:], file=sys.stderr); return 4
    print(rB.stderr[-900:])
    pre.unlink(missing_ok=True)
    print(f"\nWROTE {final}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
