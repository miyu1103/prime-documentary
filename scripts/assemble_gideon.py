#!/usr/bin/env python3
r"""Assemble the PD-2026-002-gideon first cut: burn captions + layer the cue-sheet audio.

The GideonAnimatic Remotion render (remotion/out/gideon_animatic.mp4) is already the full
694.4s timeline (S001 hook -> S028 end-card), aligned 1:1 to the narration master. This script:
  1) builds a single music bed by sequencing the cue-sheet regions (bespoke Suno beats +
     library reuse for opening/strain/somber), each looped to fill its region with fades;
  2) lays a subliminal ambience drone under the whole thing (never-silent rule);
  3) mixes narration (on top) + music + ambience  (normalize=0 keeps levels);
  4) burns captions.v001.srt and muxes to the final cut on the media SSD.

SFX one-shots + per-scene ambience swaps from the cue sheet are a v002 polish pass (documented
in QC); this first cut delivers narration + sequenced music + ambience. Idempotent.
    py -3.11 scripts/assemble_gideon.py
"""
from __future__ import annotations
import json, subprocess, sys, tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO = Path(__file__).resolve().parents[1]
MEDIA = Path(json.loads((REPO / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EP = "PD-2026-002-gideon"
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"

ANIMATIC = REPO / "remotion/out/gideon_animatic.mp4"
NARR = MEDIA / "episodes" / EP / "06_voice/master/vc_master_v001.mp3"
SRT = REPO / "episodes" / EP / "08_edit/captions.v001.srt"
EP_MUSIC = MEDIA / "episodes" / EP / "07_music"
LIB = MEDIA / "library"
OUT_DIR = MEDIA / "episodes" / EP / "08_edit"
OUT = OUT_DIR / "gideon_v001.mp4"

BGM_VOL = 0.16
AMB_VOL = 0.05
TOTAL = 694.411

# (track, start_sec, end_sec, label) — region starts are narration-chunk starts (timing.v001.json)
REGIONS = [
    (EP_MUSIC / "mus_gideon_hook_pencil.mp3",                                   0.0,     42.695,  "hook S001-S002"),
    (LIB / "music/opening/mus_20260614_opening_measured_arpeggio_v1.mp3",       42.695,  98.981,  "opening S003"),
    (LIB / "music/explainer_bed/mus_20260614_explainer_bed_soft_explainer_v1.mp3", 98.981, 145.823, "explainer S004-S005"),
    (EP_MUSIC / "mus_gideon_wall_betts.mp3",                                    145.823, 308.766, "wall S006-S012"),
    (EP_MUSIC / "mus_gideon_reveal_verdict.mp3",                                308.766, 457.838, "reveal S013-S019"),
    (LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3", 457.838, 500.603, "strain S020-S021"),
    (LIB / "music/somber/mus_20260614_somber_ledger_of_ash_v1.mp3",            500.603, 531.412, "somber S022"),
    (LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3", 531.412, 599.98, "strain S023-S024"),
    (EP_MUSIC / "mus_gideon_outro.mp3",                                         599.98,  TOTAL,   "outro S025-S028"),
]
AMBIENCE = LIB / "ambience/amb_institutional_drone.mp3"


def run(cmd, desc):
    print(f"\n>> {desc}")
    r = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print((r.stderr or "")[-2500:])
        raise RuntimeError(f"FAILED ({r.returncode}): {desc}")


def probe(path):
    r = subprocess.run([FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    for p in [ANIMATIC, NARR, SRT, AMBIENCE, *[r[0] for r in REGIONS]]:
        if not p.exists():
            raise FileNotFoundError(p)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"animatic {probe(ANIMATIC):.1f}s | narration {probe(NARR):.1f}s | target {TOTAL:.1f}s")

    tmp = Path(tempfile.gettempdir()) / "pd_gideon"
    tmp.mkdir(exist_ok=True)

    # ── 1. music bed: each region looped to fill, faded, delayed, amix(normalize=0) ──────────
    music = tmp / "music_bed.m4a"
    inputs, filt, labels = [], [], []
    for i, (track, start, end, _lbl) in enumerate(REGIONS):
        dur = end - start
        inputs += ["-stream_loop", "-1", "-i", str(track)]
        fo = max(dur - 1.2, 0.1)
        delay = int(start * 1000)
        filt.append(
            f"[{i}:a]atrim=0:{dur:.3f},afade=t=in:st=0:d=1.2,"
            f"afade=t=out:st={fo:.3f}:d=1.2,adelay={delay}|{delay}[m{i}]"
        )
        labels.append(f"[m{i}]")
    filt.append(f"{''.join(labels)}amix=inputs={len(REGIONS)}:normalize=0:dropout_transition=0[bed]")
    run([FFMPEG, "-y", *inputs, "-filter_complex", ";".join(filt),
         "-map", "[bed]", "-t", f"{TOTAL:.3f}", "-c:a", "aac", "-b:a", "192k", str(music)],
        "music bed (9 regions)")

    # ── 2. mixed audio: narration + music*vol + ambience*vol ─────────────────────────────────
    audio = tmp / "mix.m4a"
    run([FFMPEG, "-y",
         "-i", str(NARR),
         "-i", str(music),
         "-stream_loop", "-1", "-i", str(AMBIENCE),
         "-filter_complex",
         f"[1:a]volume={BGM_VOL}[mus];"
         f"[2:a]atrim=0:{TOTAL:.3f},volume={AMB_VOL}[amb];"
         f"[0:a]volume=1.0[narr];"
         f"[narr][mus][amb]amix=inputs=3:normalize=0:duration=longest:dropout_transition=0,"
         f"afade=t=out:st={TOTAL-2.0:.3f}:d=2.0[a]",
         "-map", "[a]", "-t", f"{TOTAL:.3f}", "-c:a", "aac", "-b:a", "192k", str(audio)],
        "final audio mix (narration + music + ambience)")

    # ── 3. burn captions + mux ───────────────────────────────────────────────────────────────
    srt_path = SRT.as_posix().replace(":", "\\:")
    style = ("FontName=Trebuchet MS,FontSize=22,PrimaryColour=&H00F5F7FA,"
             "OutlineColour=&H000A0A0C,BackColour=&H80000000,Bold=0,Outline=2,Shadow=1,MarginV=40")
    tmp_out = OUT.with_suffix(".tmp.mp4")
    run([FFMPEG, "-y",
         "-i", str(ANIMATIC), "-i", str(audio),
         "-vf", f"subtitles='{srt_path}':force_style='{style}'",
         "-map", "0:v", "-map", "1:a",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
         "-t", f"{TOTAL:.3f}", str(tmp_out)],
        "burn captions + mux")
    tmp_out.replace(OUT)

    print(f"\n>> {OUT}")
    print(f"   {OUT.stat().st_size/1_048_576:.1f} MB  target={TOTAL:.0f}s  actual={probe(OUT):.1f}s")


if __name__ == "__main__":
    main()
