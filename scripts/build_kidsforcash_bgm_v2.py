"""Build a 4-layer audio bed aligned to the EP38 CaseFilm timeline (NEW narration 543.5s)
and mux it into the CaseFilm render. Film layout = hook(8.033) + OP(3.5) + narration(543.5)
+ ED(9). Narration starts at OFF=11.533s. Music: hook sting -> per-act beds (ducked by VO)
-> outro over the endcard. Ambience: constant -18dB. Two-pass loudnorm to -14 LUFS.
Usage: py -3.11 scripts/build_kidsforcash_bgm_v2.py <render_in.mp4> <final_out.mp4>"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-038-kidsforcash"
IDX = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
VO = ROOT / "remotion" / "public" / "kidsforcash" / "narration_master.mp3"
LIB = Path(r"E:/pd-media/library")
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
OFF = 11.533           # hook(8.033) + OPENING_SEC(3.5): narration/body start in the film
ENDCARD = 9.0
MUS = LIB / "music"
AMB = LIB / "ambience"


def probe(f):
    r = subprocess.run([FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    return float(r.stdout.strip())


def sec(d, name):
    for c in d["chunks"]:
        if c["section"] == name:
            return c["start"] + OFF, c["end"] + OFF
    return None


def main() -> int:
    render = Path(sys.argv[1]); out = Path(sys.argv[2])
    if not render.exists():
        print(f"MISSING render {render}", file=sys.stderr); return 2
    total = probe(render)
    d = json.loads(IDX.read_text("utf-8"))
    a1, a1e = sec(d, "ACT1"); a2, a2e = sec(d, "ACT2"); a3, a3e = sec(d, "ACT3")
    a4, a4e = sec(d, "ACT4"); ed, ede = sec(d, "ENDING")
    # per-window music bed (file, start, end, vol) across the FILM timeline
    bgm = [
        (MUS / "hook/mus_20260614_hook_glass_air_bed_v1.mp3", 0.0, OFF + 6, 0.34),
        (MUS / "opening/mus_20260614_opening_measured_arpeggio_v1.mp3", OFF + 6, a1 + 56, 0.24),
        (MUS / "tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3", a1 + 56, a2, 0.22),
        (MUS / "tension_build/mus_20260614_tension_build_courtroom_horizon_v2.mp3", a2, a2 + 72, 0.22),
        (MUS / "reveal/mus_20260614_reveal_hidden_system_clicks_v1.mp3", a2 + 72, a3, 0.22),
        (MUS / "somber/mus_20260614_somber_ledger_of_ash_v1.mp3", a3, a4, 0.18),
        (MUS / "reveal/mus_20260614_reveal_hidden_system_clicks_v2.mp3", a4, a4 + 88, 0.22),
        (MUS / "reveal/mus_20260614_reveal_verdict_at_dawn_v1.mp3", a4 + 88, ed, 0.24),
        (MUS / "outro/mus_20260614_outro_last_frame_v1.mp3", ed, total, 0.24),
    ]
    amb = [
        (AMB / "amb_tension_drone.mp3", 0.0, a1),
        (AMB / "amb_empty_hallway.mp3", a1, a1 + 88),
        (AMB / "amb_institutional_drone.mp3", a1 + 88, a3),
        (AMB / "amb_night_window.mp3", a3, a4),
        (AMB / "amb_courtroom_room_tone.mp3", a4, ed),
        (AMB / "amb_light_wind.mp3", ed, total),
    ]
    for grp in (bgm, amb):
        for row in grp:
            if not row[0].exists():
                print(f"MISSING {row[0]}", file=sys.stderr); return 2

    inputs = ["-i", str(VO)]
    parts = [f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(OFF*1000)}|{int(OFF*1000)},apad,atrim=0:{total:.3f},asplit=2[vo][vokey]"]
    idx = 1; labels = []
    for k, (p, s, e, v) in enumerate(bgm):
        inputs += ["-i", str(p)]; dur = max(0.1, e - s); lab = f"m{k}"
        parts.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{dur:.3f},"
                     f"afade=t=in:st=0:d=1.5,afade=t=out:st={max(0,dur-2):.3f}:d=2.0,volume={v:.3f},"
                     f"adelay={int(s*1000)}|{int(s*1000)}[{lab}]")
        labels.append(f"[{lab}]"); idx += 1
    parts.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:dropout_transition=0[music_raw]")
    parts.append("[music_raw][vokey]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=320:makeup=1[music]")
    amb_labels = []
    for k, (p, s, e) in enumerate(amb):
        inputs += ["-i", str(p)]; dur = max(0.1, e - s); lab = f"a{k}"
        parts.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,aloop=loop=-1:size=2000000,"
                     f"atrim=0:{dur:.3f},afade=t=in:st=0:d=1.0,afade=t=out:st={max(0,dur-1.5):.3f}:d=1.5,"
                     f"volume=0.126,adelay={int(s*1000)}|{int(s*1000)}[{lab}]")
        amb_labels.append(f"[{lab}]"); idx += 1
    parts.append("".join(amb_labels) + f"amix=inputs={len(amb_labels)}:normalize=0:dropout_transition=0[amb]")
    parts.append(f"[vo][music][amb]amix=inputs=3:normalize=0:weights=1.0 0.9 0.8:dropout_transition=0,atrim=0:{total:.3f}[pre]")
    fg = ";".join(parts)

    work = out.parent / "_bgm_pre.wav"
    r = subprocess.run([FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", fg,
                        "-map", "[pre]", "-ar", "48000", "-ac", "2", str(work)], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:], file=sys.stderr); return 3
    # 2-pass loudnorm to -14
    m = subprocess.run([FFMPEG, "-hide_banner", "-i", str(work), "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    js = json.loads(m[m.rfind("{"):m.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}"
          f":measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    r2 = subprocess.run([FFMPEG, "-y", "-hide_banner", "-i", str(render), "-i", str(work),
                         "-af", ln, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                         "-c:a", "aac", "-b:a", "256k", "-shortest", str(out)], capture_output=True, text=True)
    work.unlink(missing_ok=True)
    if r2.returncode != 0:
        print(r2.stderr[-2000:], file=sys.stderr); return 4
    print(f"WROTE {out} ({probe(out):.1f}s, 4-layer mix @ -14 LUFS)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
