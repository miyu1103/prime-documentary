#!/usr/bin/env python3
"""EP45 cleveland: replace the baked narration with the authoritative master VO and add a
ducked 2-layer BGM + ambience bed, two-pass loudnorm to -14 LUFS, mux into the CaseFilm render.

Film layout = hook(8.0) + OPENING(3.5) + narration(~715.6) + ENDCARD(9). Body/VO starts at
OFF = 11.5s (hookSeconds + OPENING_SEC). Section windows come from the real narration_index
(body-relative; +OFF -> film time). Beds are looped to fill their window, ducked under VO via
sidechain. Never overwrites the input render.

Usage: python scripts/build_cleveland_bgm.py <render_in.mp4> <final_out.mp4>
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
IDX = ROOT / "episodes" / "PD-2026-045-cleveland" / "06_audio" / "narration_index.v001.json"
VO = Path(r"H:/pd-media/episodes/PD-2026-045-cleveland/06_voice/master/vc_master_v001.mp3")
LIB = Path(r"H:/pd-media/library")
MUS = LIB / "music"
AMB = LIB / "ambience"
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
OFF = 8.0 + 3.5   # hookSeconds + OPENING_SEC


def probe(f):
    r = subprocess.run([FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main() -> int:
    render = Path(sys.argv[1]); out = Path(sys.argv[2])
    if not render.exists():
        print(f"MISSING render {render}", file=sys.stderr); return 2
    if not VO.exists():
        print(f"MISSING master voice {VO}", file=sys.stderr); return 2
    if out.resolve() == render.resolve() or out.exists():
        print("REFUSING to overwrite input/existing output", file=sys.stderr); return 2
    total = probe(render)
    print(f"[render] {render.name} dur={total:.2f}s  VO master={probe(VO):.2f}s  OFF={OFF:.2f}")

    d = json.loads(IDX.read_text("utf-8"))
    sb = {}
    for c in d["chunks"]:
        s = c["section"]; sb.setdefault(s, [1e9, -1e9])
        sb[s][0] = min(sb[s][0], c["start"]); sb[s][1] = max(sb[s][1], c["end"])

    def fs(name):
        return sb[name][0] + OFF
    # EP45 cleveland is a 3-act film (HOOK/OP/ACT_1/ACT_2/ACT_3/ENDING) -- no ACT_4.
    a1, a2, a3 = fs("ACT_1"), fs("ACT_2"), fs("ACT_3")
    e0 = fs("ENDING")
    vo_end = d["chunks"][-1]["end"] + OFF
    mid3e = (a3 + e0) / 2   # ACT_3 (doctrinal core) is the longest act -> split it

    bgm = [
        (MUS / "hook/mus_20260614_hook_glass_air_bed_v1.mp3", 0.0, OFF, 0.28),
        (MUS / "opening/mus_20260614_opening_measured_arpeggio_v1.mp3", OFF, a1, 0.22),
        (MUS / "tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3", a1, a2, 0.20),
        (MUS / "somber/mus_20260614_somber_ledger_of_ash_v1.mp3", a2, a3, 0.18),
        (MUS / "reveal/mus_20260614_reveal_verdict_at_dawn_v1.mp3", a3, mid3e, 0.21),
        (MUS / "tension_build/mus_20260614_tension_build_courtroom_horizon_v2.mp3", mid3e, e0, 0.20),
        (MUS / "reveal/mus_20260614_reveal_verdict_at_dawn_v2.mp3", e0, vo_end, 0.22),
        (MUS / "outro/mus_20260614_outro_last_frame_v1.mp3", vo_end, total, 0.24),
    ]
    amb = [
        (AMB / "amb_institutional_drone.mp3", 0.0, a1),
        (AMB / "amb_courtroom_room_tone.mp3", a1, a2),
        (AMB / "amb_night_window.mp3", a2, a3),
        (AMB / "amb_office_hum.mp3", a3, e0),
        (AMB / "amb_night_window.mp3", e0, vo_end),
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

    work = out.parent / "_cleveland_bgm_pre.wav"
    print("[mix] building bed ...", flush=True)
    r = subprocess.run([FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", fg,
                        "-map", "[pre]", "-ar", "48000", "-ac", "2", str(work)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:], file=sys.stderr); return 3
    print("[loudnorm] pass1 ...", flush=True)
    m = subprocess.run([FFMPEG, "-hide_banner", "-i", str(work), "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    js = json.loads(m[m.rfind("{"):m.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}"
          f":measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}"
          f":offset={js['target_offset']}:linear=true")
    print("[mux] pass2 + mux ...", flush=True)
    r2 = subprocess.run([FFMPEG, "-y", "-hide_banner", "-i", str(render), "-i", str(work),
                         "-af", ln, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                         "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest", str(out)],
                        capture_output=True, text=True)
    work.unlink(missing_ok=True)
    if r2.returncode != 0:
        print(r2.stderr[-3000:], file=sys.stderr); return 4
    print(f"WROTE {out}  ({probe(out):.1f}s, master VO + BGM @ -14 LUFS)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

