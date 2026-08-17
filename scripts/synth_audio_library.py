#!/usr/bin/env python3
"""Rebuild the audio library (SFX / ambience / music beds) by synthesis, at the paths the
4-layer mix actually dereferences.

2026-08-17. The pd-media SSD stopped being enumerated by Windows and took
H:\\pd-media\\library with it -- every SFX one-shot, every ambience bed and the three music
beds. Measured: not one of these files exists anywhere on C/D/E/F. Without them the [7/7]
mix step fails for every episode, so EP66-69 cannot finish and EP70/71 cannot start.

Everything here is generated from first principles with ffmpeg's lavfi sources -- sine,
noise, envelopes, filters. No sample library, no external download, no rights question.
The originals were themselves partly synthesized ("synthesized variants", VARIANT_POOLS).
Every bed and music cue is consumed with `-stream_loop -1`, so 60 s loop-friendly files
(noise-based or continuous drones, faded edges) are sufficient at any episode length.

House sound: muted, dark, low. SFX sit under narration (the mixer applies its own per-cue
gain), beds are quiet textures, music is a pad, not a melody. Nothing bright, nothing
rhythmic enough to fight the voice.

    py -3.11 scripts/synth_audio_library.py            # write all 35, skip existing
    py -3.11 scripts/synth_audio_library.py --force    # regenerate everything
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

LIB = Path("E:/pd-media/library")
FF = "ffmpeg"
AR = 48000

# name -> (subdir, filter_complex producing [out])
# One-shots are exact-length; beds/music are 60-64 s and loop cleanly (noise or continuous
# drones with edge fades that the -stream_loop overlap hides at the low levels they play at).
RECIPES: dict[str, tuple[str, str]] = {}


def R(name: str, sub: str, graph: str) -> None:
    RECIPES[name] = (sub, graph)


# ---- SFX one-shots ---------------------------------------------------------------------
# Booms: two detuned low sines, fast attack, exponential-feel decay, soft saturation.
R("sfx_low_boom.mp3", "sfx",
  "sine=f=52:d=1.6[a];sine=f=64:d=1.6[b];[a][b]amix=2,afade=t=in:d=0.005,"
  "afade=t=out:st=0.12:d=1.45,volume=6dB,alimiter=limit=0.7,lowpass=f=180[out]")
R("sfx_boom_v2_deep.mp3", "sfx",
  "sine=f=41:d=2.2[a];sine=f=49:d=2.2[b];[a][b]amix=2,afade=t=in:d=0.006,"
  "afade=t=out:st=0.15:d=2.0,volume=6dB,alimiter=limit=0.7,lowpass=f=140[out]")
# Sub drop: pitch falls 110->30 Hz over a second.
R("sfx_sub_drop.mp3", "sfx",
  "aevalsrc='0.8*sin(2*PI*(110-80*min(t,1))*t)':d=1.3:s=48000,afade=t=in:d=0.01,"
  "afade=t=out:st=0.6:d=0.7,lowpass=f=200[out]")
R("sfx_subdrop_v2_a.mp3", "sfx",
  "aevalsrc='0.8*sin(2*PI*(95-70*min(t,0.9))*t)':d=1.1:s=48000,afade=t=in:d=0.01,"
  "afade=t=out:st=0.5:d=0.6,lowpass=f=200[out]")
R("sfx_subdrop_v2_b.mp3", "sfx",
  "aevalsrc='0.8*sin(2*PI*(130-95*min(t,1.1))*t)':d=1.4:s=48000,afade=t=in:d=0.01,"
  "afade=t=out:st=0.7:d=0.7,lowpass=f=220[out]")
# Risers: noise swelling in level and brightness. The volume ramp does the "rise".
R("sfx_riser_2s.mp3", "sfx",
  "anoisesrc=c=pink:d=2.0:a=0.6,volume='0.05+0.95*(t/2)^2':eval=frame,"
  "highpass=f=500,lowpass=f=6000,afade=t=out:st=1.9:d=0.1[out]")
R("sfx_riser_v2_1s.mp3", "sfx",
  "anoisesrc=c=pink:d=1.0:a=0.6,volume='0.05+0.95*(t/1)^2':eval=frame,"
  "highpass=f=700,lowpass=f=6500,afade=t=out:st=0.92:d=0.08[out]")
R("sfx_riser_v2_3s.mp3", "sfx",
  "anoisesrc=c=pink:d=3.0:a=0.6,volume='0.05+0.95*(t/3)^2':eval=frame,"
  "highpass=f=400,lowpass=f=5500,afade=t=out:st=2.85:d=0.15[out]")
# Whooshes: a bell-shaped noise pass. Length variants; v2 = darker band.
R("sfx_whoosh_short.mp3", "sfx",
  "anoisesrc=c=white:d=0.5:a=0.7,bandpass=f=900:w=900,"
  "volume='sin(PI*t/0.5)':eval=frame[out]")
R("sfx_whoosh_medium.mp3", "sfx",
  "anoisesrc=c=white:d=0.9:a=0.7,bandpass=f=700:w=800,"
  "volume='sin(PI*t/0.9)':eval=frame[out]")
R("sfx_whoosh_v2_short.mp3", "sfx",
  "anoisesrc=c=pink:d=0.5:a=0.8,bandpass=f=500:w=600,"
  "volume='sin(PI*t/0.5)':eval=frame[out]")
R("sfx_whoosh_v2_med.mp3", "sfx",
  "anoisesrc=c=pink:d=1.0:a=0.8,bandpass=f=450:w=550,"
  "volume='sin(PI*t/1.0)':eval=frame[out]")
R("sfx_whoosh_v2_long.mp3", "sfx",
  "anoisesrc=c=pink:d=1.5:a=0.8,bandpass=f=400:w=500,"
  "volume='sin(PI*t/1.5)':eval=frame[out]")
# Impacts: a thump plus a tiny noise transient.
R("sfx_soft_impact.mp3", "sfx",
  "sine=f=95:d=0.5[t];anoisesrc=c=white:d=0.05:a=0.4,lowpass=f=900[c];"
  "[t][c]amix=2:duration=longest,afade=t=out:st=0.05:d=0.45,volume=4dB[out]")
R("sfx_impact_v2_tight.mp3", "sfx",
  "sine=f=120:d=0.28[t];anoisesrc=c=white:d=0.03:a=0.5,lowpass=f=1200[c];"
  "[t][c]amix=2:duration=longest,afade=t=out:st=0.03:d=0.25,volume=4dB[out]")
# Paper: shaped high noise. Page turn = two rustle strokes.
R("sfx_paper_rustle.mp3", "sfx",
  "anoisesrc=c=white:d=0.6:a=0.5,highpass=f=1800,lowpass=f=9000,"
  "volume='0.3+0.7*abs(sin(2*PI*7*t))':eval=frame,afade=t=out:st=0.45:d=0.15[out]")
R("sfx_page_turn.mp3", "sfx",
  "anoisesrc=c=white:d=0.45:a=0.5,highpass=f=1500,lowpass=f=8000,"
  "volume='if(lt(t,0.18),sin(PI*t/0.18),if(lt(t,0.24),0,sin(PI*(t-0.24)/0.21)))':eval=frame[out]")
# Clicks and mechanicals.
R("sfx_camera_shutter.mp3", "sfx",
  "anoisesrc=c=white:d=0.2:a=0.6,highpass=f=2500,"
  "volume='if(lt(t,0.012),1,if(lt(t,0.07),0,if(lt(t,0.085),0.8,0)))':eval=frame[out]")
R("sfx_binder_lock.mp3", "sfx",
  "anoisesrc=c=white:d=0.15:a=0.6,bandpass=f=3200:w=1500,"
  "volume='if(lt(t,0.012),1,if(lt(t,0.05),0.15,if(lt(t,0.06),0.7,0)))':eval=frame[out]")
R("sfx_stamp_seal.mp3", "sfx",
  "sine=f=110:d=0.35[t];anoisesrc=c=white:d=0.02:a=0.6,highpass=f=2000[c];"
  "[t][c]amix=2:duration=longest,afade=t=out:st=0.04:d=0.3,volume=4dB[out]")
R("sfx_gavel_knock.mp3", "sfx",
  "anoisesrc=c=white:d=0.25:a=0.8,bandpass=f=750:w=350,"
  "volume='exp(-18*t)':eval=frame,volume=6dB[out]")
R("sfx_clock_tick_loop.mp3", "sfx",
  "anoisesrc=c=white:d=10:a=0.7,bandpass=f=2600:w=900,"
  "volume='if(lt(mod(t,1.0),0.012),1,0)':eval=frame[out]")

# ---- ambience beds (60 s, loop under -stream_loop -1) ----------------------------------
R("amb_office_hum.mp3", "ambience",
  "anoisesrc=c=brown:d=60:a=0.5,lowpass=f=300[n];sine=f=120:d=60,volume=0.04[h];"
  "[n][h]amix=2:duration=first,volume=-18dB,afade=t=in:d=1,afade=t=out:st=59:d=1[out]")
R("amb_courtroom_room_tone.mp3", "ambience",
  "anoisesrc=c=pink:d=60:a=0.4,lowpass=f=450,volume=-22dB,"
  "afade=t=in:d=1,afade=t=out:st=59:d=1[out]")
R("amb_empty_hallway.mp3", "ambience",
  "anoisesrc=c=pink:d=60:a=0.45,lowpass=f=600,tremolo=f=0.1:d=0.35,volume=-20dB,"
  "afade=t=in:d=1,afade=t=out:st=59:d=1[out]")
R("amb_institutional_drone.mp3", "ambience",
  "sine=f=55:d=60[a];sine=f=110.7:d=60[b];sine=f=164:d=60[c];"
  "[a][b][c]amix=3,tremolo=f=0.1:d=0.25,lowpass=f=500,volume=-20dB,"
  "afade=t=in:d=2,afade=t=out:st=58:d=2[out]")
R("amb_tension_drone.mp3", "ambience",
  "sine=f=58:d=60[a];sine=f=61.5:d=60[b];anoisesrc=c=white:d=60:a=0.15,highpass=f=6000,volume=0.05[s];"
  "[a][b][s]amix=3,lowpass=f=4000,volume=-19dB,afade=t=in:d=2,afade=t=out:st=58:d=2[out]")
R("amb_night_window.mp3", "ambience",
  "anoisesrc=c=brown:d=60:a=0.4,lowpass=f=220,tremolo=f=0.1:d=0.3,volume=-20dB,"
  "afade=t=in:d=1,afade=t=out:st=59:d=1[out]")
R("amb_highway_traffic.mp3", "ambience",
  "anoisesrc=c=brown:d=60:a=0.5,lowpass=f=500,tremolo=f=0.1:d=0.3,volume=-17dB,"
  "afade=t=in:d=1,afade=t=out:st=59:d=1[out]")
R("amb_rain_street.mp3", "ambience",
  "anoisesrc=c=white:d=60:a=0.35,highpass=f=400,lowpass=f=8000,"
  "tremolo=f=11:d=0.15,volume=-20dB,afade=t=in:d=1,afade=t=out:st=59:d=1[out]")
R("amb_road_rumble_1920s.mp3", "ambience",
  "anoisesrc=c=brown:d=60:a=0.55,lowpass=f=160,tremolo=f=0.3:d=0.25,volume=-16dB,"
  "afade=t=in:d=1,afade=t=out:st=59:d=1[out]")
R("amb_engine_idle.mp3", "ambience",
  "sine=f=80:d=60,tremolo=f=13:d=0.4[e];anoisesrc=c=brown:d=60:a=0.3,lowpass=f=250[n];"
  "[e][n]amix=2,volume=-18dB,afade=t=in:d=1,afade=t=out:st=59:d=1[out]")

# ---- music beds (64 s pads; consumed under narration at low gain) ----------------------
# Hook: airy suspended chord (A add9), slow shimmer above it.
R("mus_20260614_hook_glass_air_bed_v2.mp3", "music/hook",
  "sine=f=220:d=64[a];sine=f=261.6:d=64[b];sine=f=329.6:d=64[c];sine=f=493.9:d=64[d];"
  "anoisesrc=c=white:d=64:a=0.08,highpass=f=7000,tremolo=f=0.2:d=0.5[s];"
  "[a][b][c][d][s]amix=5,tremolo=f=0.11:d=0.2,lowpass=f=5200,volume=-18dB,"
  "afade=t=in:d=3,afade=t=out:st=60:d=4[out]")
# Explainer: warm low pad, minor, almost static.
R("mus_20260614_explainer_bed_soft_explainer_v2.mp3", "music/explainer_bed",
  "sine=f=110:d=64[a];sine=f=164.8:d=64[b];sine=f=220:d=64[c];sine=f=277.2:d=64[d];"
  "[a][b][c][d]amix=4,tremolo=f=0.1:d=0.18,lowpass=f=1400,volume=-19dB,"
  "afade=t=in:d=3,afade=t=out:st=60:d=4[out]")
# Outro: darker, lower, slow swell.
R("mus_20260614_outro_last_frame_v2.mp3", "music/outro",
  "sine=f=82.4:d=64[a];sine=f=123.5:d=64[b];sine=f=164.8:d=64[c];"
  "[a][b][c]amix=3,tremolo=f=0.1:d=0.22,lowpass=f=900,volume=-18dB,"
  "afade=t=in:d=4,afade=t=out:st=58:d=6[out]")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    made = skipped = failed = 0
    for name, (sub, graph) in RECIPES.items():
        dest = LIB / sub / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.is_file() and dest.stat().st_size > 1000 and not a.force:
            skipped += 1
            continue
        cmd = [FF, "-y", "-v", "error", "-filter_complex", graph, "-map", "[out]",
               "-ar", str(AR), "-ac", "2", "-c:a", "libmp3lame", "-q:a", "2", str(dest)]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
        if r.returncode == 0 and dest.is_file() and dest.stat().st_size > 1000:
            made += 1
        else:
            failed += 1
            print(f"FAIL {name}: {(r.stderr or '').strip()[-160:]}")
    print(f"[synth] made={made} skipped={skipped} failed={failed} -> {LIB}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
