"""Build the master-narration + 4-layer BGM mix for EP39 frazier and mux it into
the CaseFilm render, REPLACING the baked (705s, out-of-sync) narration with the
authoritative master (716.29s == film narrationSeconds).

Film layout = hook(8.04) + OPENING(3.5) + narration(716.289) + ENDCARD(9).
Narration/body starts at OFF = 11.54s. Section windows come from the real
narration_index (body-relative; +OFF -> film time). Music beds are LOOPED to
fill their window (no gaps), ducked under VO via sidechain. Ambience = constant
low bed. Two-pass loudnorm to -14 LUFS. Never overwrites the input render.

Usage: python scripts/build_frazier_bgm.py <render_in.mp4> <final_out.mp4>
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
IDX = ROOT / "episodes" / "PD-2026-039-frazier" / "06_audio" / "narration_index.v001.json"
VO = Path(r"E:/pd-media/episodes/PD-2026-039-frazier/06_voice/master/vc_master_v001.mp3")
LIB = Path(r"E:/pd-media/library")
MUS = LIB / "music"
AMB = LIB / "ambience"
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
OFF = 8.04 + 3.5       # hookSeconds + OPENING_SEC -> film time offset of the VO body


def probe(f):
    r = subprocess.run([FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main() -> int:
    render = Path(sys.argv[1]); out = Path(sys.argv[2])
    if not render.exists():
        print(f"MISSING render {render}", file=sys.stderr); return 2
    if out.resolve() == render.resolve():
        print("REFUSING to overwrite the input render", file=sys.stderr); return 2
    if out.exists():
        print(f"REFUSING to overwrite existing output {out}", file=sys.stderr); return 2
    total = probe(render)
    print(f"[render] {render.name} dur={total:.2f}s  VO master={probe(VO):.2f}s  OFF={OFF:.2f}")

    d = json.loads(IDX.read_text("utf-8"))
    sb = {}
    for c in d["chunks"]:
        s = c["section"]; sb.setdefault(s, [1e9, -1e9])
        sb[s][0] = min(sb[s][0], c["start"]); sb[s][1] = max(sb[s][1], c["end"])
    # film-time section starts
    def fs(name):  # section start in film time
        return sb[name][0] + OFF
    a1, a2, a3, a4, ed = fs("ACT_I"), fs("ACT_II"), fs("ACT_III"), fs("ACT_IV"), fs("ENDING")
    vo_end = d["chunks"][-1]["end"] + OFF   # == endcard start

    # music beds across the FILM timeline (file, start, end, vol) - looped to fill
    bgm = [
        (MUS / "hook/mus_20260614_hook_glass_air_bed_v1.mp3", 0.0, 22.0, 0.30),
        (MUS / "opening/mus_20260614_opening_measured_arpeggio_v1.mp3", 22.0, a1, 0.22),
        (MUS / "tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3", a1, a2, 0.20),
        (MUS / "tension_build/mus_20260614_tension_build_courtroom_horizon_v2.mp3", a2, (a2 + a3) / 2, 0.20),
        (MUS / "reveal/mus_20260614_reveal_hidden_system_clicks_v1.mp3", (a2 + a3) / 2, a3, 0.20),
        (MUS / "reveal/mus_20260614_reveal_verdict_at_dawn_v1.mp3", a3, (a3 + a4) / 2, 0.21),
        (MUS / "somber/mus_20260614_somber_ledger_of_ash_v1.mp3", (a3 + a4) / 2, a4, 0.18),
        (MUS / "somber/mus_20260614_somber_ledger_of_ash_v2.mp3", a4, a4 + 120, 0.18),
        (MUS / "reveal/mus_20260614_reveal_hidden_system_clicks_v2.mp3", a4 + 120, ed - 40, 0.20),
        (MUS / "reveal/mus_20260614_reveal_verdict_at_dawn_v2.mp3", ed - 40, vo_end, 0.22),
        (MUS / "outro/mus_20260614_outro_last_frame_v1.mp3", vo_end, total, 0.24),
    ]
    amb = [
        (AMB / "amb_institutional_drone.mp3", 0.0, a1),
        (AMB / "amb_courtroom_room_tone.mp3", a1, a3),
        (AMB / "amb_office_hum.mp3", a3, a4),
        (AMB / "amb_night_window.mp3", a4, vo_end),
        (AMB / "amb_light_wind.mp3", vo_end, total),
    ]
    for grp in (bgm, amb):
        for row in grp:
            if not row[0].exists():
                print(f"MISSING {row[0]}", file=sys.stderr); return 2

    inputs = ["-i", str(VO)]
    parts = [f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(OFF*1000)}|{int(OFF*1000)},"
             f"apad,atrim=0:{total:.3f},asplit=2[vo][vokey]"]
    idx = 1; mlabels = []
    for k, (p, s, e, v) in enumerate(bgm):
        dur = max(0.1, e - s); lab = f"m{k}"; inputs += ["-i", str(p)]
        parts.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                     f"aloop=loop=-1:size=2000000000,atrim=0:{dur:.3f},"
                     f"afade=t=in:st=0:d=1.5,afade=t=out:st={max(0, dur-2):.3f}:d=2.0,"
                     f"volume={v:.3f},adelay={int(s*1000)}|{int(s*1000)}[{lab}]")
        mlabels.append(f"[{lab}]"); idx += 1
    parts.append("".join(mlabels) + f"amix=inputs={len(mlabels)}:normalize=0:dropout_transition=0[music_raw]")
    parts.append("[music_raw][vokey]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=320:makeup=1[music]")
    alabels = []
    for k, (p, s, e) in enumerate(amb):
        dur = max(0.1, e - s); lab = f"a{k}"; inputs += ["-i", str(p)]
        parts.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                     f"aloop=loop=-1:size=2000000000,atrim=0:{dur:.3f},"
                     f"afade=t=in:st=0:d=1.0,afade=t=out:st={max(0, dur-1.5):.3f}:d=1.5,"
                     f"volume=0.12,adelay={int(s*1000)}|{int(s*1000)}[{lab}]")
        alabels.append(f"[{lab}]"); idx += 1
    parts.append("".join(alabels) + f"amix=inputs={len(alabels)}:normalize=0:dropout_transition=0[amb]")
    parts.append(f"[vo][music][amb]amix=inputs=3:normalize=0:weights=1.0 0.9 0.8:dropout_transition=0,"
                 f"atrim=0:{total:.3f}[pre]")
    fg = ";".join(parts)

    work = out.parent / "_frazier_bgm_pre.wav"
    print("[mix] building 4-layer bed ...", flush=True)
    r = subprocess.run([FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", fg,
                        "-map", "[pre]", "-ar", "48000", "-ac", "2", str(work)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:], file=sys.stderr); return 3
    print("[loudnorm] pass1 measure ...", flush=True)
    m = subprocess.run([FFMPEG, "-hide_banner", "-i", str(work), "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    js = json.loads(m[m.rfind("{"):m.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}"
          f":measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}"
          f":offset={js['target_offset']}:linear=true")
    print("[mux] pass2 + mux into video ...", flush=True)
    r2 = subprocess.run([FFMPEG, "-y", "-hide_banner", "-i", str(render), "-i", str(work),
                         "-af", ln, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                         "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest", str(out)],
                        capture_output=True, text=True)
    work.unlink(missing_ok=True)
    if r2.returncode != 0:
        print(r2.stderr[-3000:], file=sys.stderr); return 4
    print(f"WROTE {out}  ({probe(out):.1f}s, master VO + 4-layer BGM @ -14 LUFS)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
