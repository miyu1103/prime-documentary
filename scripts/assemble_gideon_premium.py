#!/usr/bin/env python3
r"""Premium assembly for PD-2026-002-gideon (0004 §E four layers + §C SFX density + grade).

Takes the GideonPremium Remotion render (remotion/out/gideon_premium.mp4 — moving stage, real
assets, clips, labels, grain) and finishes it to the 0004 bar:
  - four-layer audio: narration (top) + sequenced music bed + continuous ambience + SFX layer,
    plus a short featured excerpt of the REAL 1963 oral-argument audio at the S013 beat;
  - SFX density: a cue at every shot boundary (shot counts from shotlist.v001) + curated emphasis
    hits (gavel/stamp/riser/sub-drop/boom) → ~110 cues (0004 floor 60-100+);
  - brand colour-grade (subtle teal-shadow / warm-highlight + gentle contrast) applied uniformly;
  - burn captions.v001.srt; output to the media SSD.
    py -3.11 scripts/assemble_gideon_premium.py
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

VIDEO = REPO / "remotion/out/gideon_premium.mp4"
NARR = MEDIA / "episodes" / EP / "06_voice/master/vc_master_v001.mp3"
SRT = REPO / "episodes" / EP / "08_edit/captions.v001.srt"
EPM = MEDIA / "episodes" / EP / "07_music"
REAL = MEDIA / "episodes" / EP / "05_visuals/real"
LIB = MEDIA / "library"
SFXD = LIB / "sfx"
OUT = MEDIA / "episodes" / EP / "08_edit" / "gideon_premium_v001.mp4"
TOTAL = 694.411

# music regions (start,end,track) — same plan as the cue sheet
REGIONS = [
    (EPM / "mus_gideon_hook_pencil.mp3", 0.0, 42.695),
    (LIB / "music/opening/mus_20260614_opening_measured_arpeggio_v1.mp3", 42.695, 98.981),
    (LIB / "music/explainer_bed/mus_20260614_explainer_bed_soft_explainer_v1.mp3", 98.981, 145.823),
    (EPM / "mus_gideon_wall_betts.mp3", 145.823, 308.766),
    (EPM / "mus_gideon_reveal_verdict.mp3", 308.766, 457.838),
    (LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3", 457.838, 500.603),
    (LIB / "music/somber/mus_20260614_somber_ledger_of_ash_v1.mp3", 500.603, 531.412),
    (LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3", 531.412, 599.98),
    (EPM / "mus_gideon_outro.mp3", 599.98, TOTAL),
]
AMB = LIB / "ambience/amb_institutional_drone.mp3"
ARG = REAL / "gideon_oral_argument_19630115_part1.mp3"

# per-scene shot counts (from shotlist.v001.md) — used to place a transition SFX per shot boundary
SHOTS = {"S001":3,"S002":5,"S003":6,"S004":4,"S005":3,"S006":5,"S007":3,"S008":3,"S009":4,"S010":4,
         "S011":5,"S012":4,"S013":4,"S014":3,"S015":4,"S016":5,"S017":4,"S018":4,"S019":2,"S020":4,
         "S021":3,"S022":5,"S023":4,"S024":5,"S025":3,"S026":3,"S027":3,"S028":4}
CYCLE = ["sfx_whoosh_short.mp3","sfx_ui_tick.mp3","sfx_soft_impact.mp3","sfx_page_turn.mp3","sfx_data_blip.mp3"]
# curated emphasis hits (scene_id -> at scene-relative 0, file, gain)
EMPH = {
    "S001":[("end","sfx_sub_drop.mp3",0.9),("start","sfx_riser_2s.mp3",0.7)],
    "S004":[("start","sfx_gavel_knock.mp3",0.8)],
    "S007":[("start","sfx_gavel_knock.mp3",0.9),("end","sfx_stamp_seal.mp3",0.8)],
    "S013":[("start","sfx_riser_2s.mp3",0.7)],
    "S014":[("end","sfx_riser_2s.mp3",0.9)],
    "S015":[("start","sfx_low_boom.mp3",0.8)],
    "S018":[("start","sfx_low_boom.mp3",0.9)],
    "S021":[("end","sfx_stamp_seal.mp3",0.9),("start","sfx_gavel_knock.mp3",0.7)],
    "S028":[("end","sfx_low_boom.mp3",0.8)],
}


def run(cmd, desc):
    print(f"\n>> {desc}")
    r = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print((r.stderr or "")[-2500:]); raise RuntimeError(f"FAILED: {desc}")


def probe(p):
    r = subprocess.run([FFPROBE,"-v","quiet","-show_entries","format=duration","-of","csv=p=0",str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def build_cues(timing):
    """Return list of (file_path, t_seconds, gain)."""
    cues = []
    scenes = timing["scenes"]
    starts = {s["scene_id"]: s["start"] for s in scenes}
    order = [s["scene_id"] for s in scenes]
    ci = 0
    for i, s in enumerate(scenes):
        sid = s["scene_id"]
        start = s["start"]
        end = starts[order[i+1]] if i+1 < len(order) else TOTAL
        n = SHOTS.get(sid, 3)
        # transition SFX at each shot boundary within the scene
        for k in range(n):
            t = start + (end - start) * k / n
            f = SFXD / CYCLE[ci % len(CYCLE)]; ci += 1
            cues.append((f, round(t, 3), 0.45))
        # emphasis hits
        for where, fname, gain in EMPH.get(sid, []):
            t = start + 0.2 if where == "start" else max(end - 1.6, start)
            cues.append((SFXD / fname, round(t, 3), gain))
    return cues


def main():
    for p in [VIDEO, NARR, SRT, AMB, ARG, *[r[0] for r in REGIONS]]:
        if not p.exists():
            raise FileNotFoundError(p)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    timing = json.loads((REPO / "episodes" / EP / "08_edit/timing.v001.json").read_text("utf-8"))
    print(f"video {probe(VIDEO):.1f}s | narration {probe(NARR):.1f}s | target {TOTAL:.1f}s")
    tmp = Path(tempfile.gettempdir()) / "pd_gideon_premium"; tmp.mkdir(exist_ok=True)

    # 1) music bed
    music = tmp / "music.m4a"; inp=[]; filt=[]; lab=[]
    for i,(tr,st,en) in enumerate(REGIONS):
        dur=en-st; inp+=["-stream_loop","-1","-i",str(tr)]; d=int(st*1000); fo=max(dur-1.2,0.1)
        filt.append(f"[{i}:a]atrim=0:{dur:.3f},afade=t=in:st=0:d=1.2,afade=t=out:st={fo:.3f}:d=1.2,adelay={d}|{d}[m{i}]"); lab.append(f"[m{i}]")
    filt.append(f"{''.join(lab)}amix=inputs={len(REGIONS)}:normalize=0:dropout_transition=0[bed]")
    run([FFMPEG,"-y",*inp,"-filter_complex",";".join(filt),"-map","[bed]","-t",f"{TOTAL:.3f}","-c:a","aac","-b:a","192k",str(music)],"music bed")

    # 2) SFX bed (~110 cues)
    cues = build_cues(timing); print(f"   SFX cues: {len(cues)}")
    sfx = tmp / "sfx.m4a"; inp=[]; filt=[]; lab=[]
    for i,(f,t,g) in enumerate(cues):
        inp+=["-i",str(f)]; d=int(t*1000)
        filt.append(f"[{i}:a]volume={g},adelay={d}|{d}[s{i}]"); lab.append(f"[s{i}]")
    filt.append(f"{''.join(lab)}amix=inputs={len(cues)}:normalize=0:dropout_transition=0[sfx]")
    run([FFMPEG,"-y",*inp,"-filter_complex",";".join(filt),"-map","[sfx]","-t",f"{TOTAL:.3f}","-c:a","aac","-b:a","160k",str(sfx)],f"SFX bed ({len(cues)} cues)")

    # 3) final mix + grade + captions
    srt = SRT.as_posix().replace(":", "\\:")
    style=("FontName=Trebuchet MS,FontSize=22,PrimaryColour=&H00F5F7FA,OutlineColour=&H000A0A0C,"
           "BackColour=&H80000000,Bold=0,Outline=2,Shadow=1,MarginV=40")
    grade="eq=contrast=1.06:saturation=1.05:gamma=0.98,colorbalance=rs=-0.04:bs=0.05:rh=0.04:bh=-0.03"
    arg_win=54.0  # feature ~10s of real argument at S013 (308.766), low under VO
    tmp_out=OUT.with_suffix(".tmp.mp4")
    run([FFMPEG,"-y",
         "-i",str(VIDEO),"-i",str(NARR),"-i",str(music),"-stream_loop","-1","-i",str(AMB),"-i",str(ARG),"-i",str(sfx),
         "-filter_complex",
         f"[3:a]atrim=0:{TOTAL:.3f},volume=0.05[amb];"
         f"[4:a]atrim=40:50,volume=0.16,afade=t=in:st=0:d=1,afade=t=out:st=8:d=2,adelay=309000|309000[arg];"
         f"[2:a]volume=0.16[mus];[5:a]volume=0.5[sfx];[1:a]volume=1.0[narr];"
         f"[narr][mus][amb][arg][sfx]amix=inputs=5:normalize=0:duration=longest:dropout_transition=0,"
         f"afade=t=out:st={TOTAL-2.0:.3f}:d=2.0[a]",
         "-map","0:v","-map","[a]",
         "-vf",f"{grade},subtitles='{srt}':force_style='{style}'",
         "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",
         "-c:a","aac","-b:a","192k","-t",f"{TOTAL:.3f}",str(tmp_out)],"final mix + grade + captions")
    tmp_out.replace(OUT)
    print(f"\n>> {OUT}\n   {OUT.stat().st_size/1_048_576:.1f} MB  target={TOTAL:.0f}s  actual={probe(OUT):.1f}s")


if __name__ == "__main__":
    main()
