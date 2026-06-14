"""
scripts/assemble_v011.py
Assembles sample_v011.mp4 for PD-2026-001-miranda.

Changes from v010:
  - Narration: 06_voice/master/vc_master_v001.mp3 (voice_plan text, 577.6s)
  - SRT: subs_vc_v001.srt (249 entries matching new narration)

Structure: [Hook 30s] [Opening 6s] [Main ~547s] [Endcard 10s] ≈ 593s
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO        = Path(__file__).resolve().parents[1]
REMOTION    = REPO / "remotion"
MUSIC_DIR   = Path(r"H:\pd-media\downloads\music")
EDIT_DIR    = Path(r"H:\pd-media\episodes\PD-2026-001-miranda\07_edit\sample")
FFMPEG      = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE     = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"

OPENING_MP4 = REMOTION / "out" / "opening.mp4"
ANIMATIC_MP4 = REMOTION / "out" / "animatic_motion.mp4"
NARR_MP3    = Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_voice\master\vc_master_v001.mp3")
SRT_IN      = EDIT_DIR / "subs_vc_v001.srt"
OUT_MP4     = EDIT_DIR / "sample_v011.mp4"

HOOK_END_SEC  = 30.0
OPENING_SEC   = 6.0
ENDCARD_SEC   = 10.0
NARR_TAIL_SEC = 5.0
BGM_VOL       = 0.10

BGM_TRACKS = [
    MUSIC_DIR / "mus_20260614_hook_glass_air_bed_v1.mp3",
    MUSIC_DIR / "mus_20260614_somber_ledger_of_ash_v1.mp3",
    MUSIC_DIR / "mus_20260614_outro_last_frame_v2.mp3",
    MUSIC_DIR / "mus_20260614_ambience_empty_hall_v1.mp3",
]


def run(cmd: list[str], desc: str = "", cwd: Path | None = None) -> None:
    print(f"\n▶ {desc}")
    r = subprocess.run(
        cmd, capture_output=True,
        encoding="utf-8", errors="replace",
        cwd=str(cwd) if cwd else None,
    )
    if r.returncode != 0:
        print((r.stderr or "")[-2000:])
        raise RuntimeError(f"FAILED ({r.returncode}): {desc}")
    if r.stdout and r.stdout.strip():
        print(r.stdout[-400:])


def probe_duration(path: Path) -> float:
    r = subprocess.run(
        [FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def main() -> None:
    for p in [OPENING_MP4, ANIMATIC_MP4, NARR_MP3, SRT_IN, *BGM_TRACKS]:
        if not p.exists():
            raise FileNotFoundError(p)
    EDIT_DIR.mkdir(parents=True, exist_ok=True)

    anim_dur  = probe_duration(ANIMATIC_MP4)
    narr_dur  = probe_duration(NARR_MP3)
    main_dur  = (narr_dur - HOOK_END_SEC - OPENING_SEC) + NARR_TAIL_SEC
    main_dur  = max(0.0, min(main_dur, anim_dur - HOOK_END_SEC))
    total_dur = HOOK_END_SEC + OPENING_SEC + main_dur + ENDCARD_SEC

    print(f"Hook:      {HOOK_END_SEC}s")
    print(f"Opening:   {OPENING_SEC}s")
    print(f"Main:      {main_dur:.1f}s  (narr {narr_dur:.1f}s + {NARR_TAIL_SEC}s tail)")
    print(f"Endcard:   {ENDCARD_SEC}s")
    print(f"Total:     {total_dur:.1f}s")

    tmp = Path(tempfile.gettempdir()) / "pd_v011"
    tmp.mkdir(exist_ok=True)

    # ── 1. Endcard ─────────────────────────────────────────────────────────
    endcard = tmp / "endcard.mp4"
    shutil.copy2(Path(r"C:\Windows\Fonts\impact.ttf"), tmp / "impact.ttf")
    shutil.copy2(Path(r"C:\Windows\Fonts\trebuc.ttf"), tmp / "trebuc.ttf")
    run([
        FFMPEG, "-y",
        "-f", "lavfi",
        "-i", f"color=color=0x0A0A0C:s=1920x1080:r=30:d={ENDCARD_SEC}",
        "-vf", (
            "drawtext=fontfile=impact.ttf"
            ":text=PRIME DOCUMENTARY"
            ":fontsize=80:fontcolor=E5B53A"
            ":x=(w-text_w)/2:y=(h-text_h)/2-60,"
            "drawtext=fontfile=trebuc.ttf"
            ":text=Subscribe for more documentary deep-dives"
            ":fontsize=30:fontcolor=C8CDD6"
            ":x=(w-text_w)/2:y=(h-text_h)/2+40"
        ),
        "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-an",
        str(endcard),
    ], "endcard", cwd=tmp)

    # ── 2. Extract hook + main ─────────────────────────────────────────────
    hook_mp4 = tmp / "hook.mp4"
    main_mp4 = tmp / "main.mp4"
    run([
        FFMPEG, "-y", "-i", str(ANIMATIC_MP4),
        "-t", str(HOOK_END_SEC), "-c:v", "copy", "-an",
        str(hook_mp4),
    ], "extract hook")
    run([
        FFMPEG, "-y",
        "-ss", str(HOOK_END_SEC), "-t", f"{main_dur:.3f}",
        "-i", str(ANIMATIC_MP4),
        "-c:v", "copy", "-an",
        str(main_mp4),
    ], f"extract main ({main_dur:.1f}s)")

    # ── 3. SRT: original timing — narration at t=0, no shift ──────────────
    srt_shifted = SRT_IN

    # ── 4. Concat BGM ─────────────────────────────────────────────────────
    bgm_full = tmp / "bgm_full.mp3"
    bgm_in   = [arg for t in BGM_TRACKS for arg in ("-i", str(t))]
    n        = len(BGM_TRACKS)
    run([
        FFMPEG, "-y", *bgm_in,
        "-filter_complex",
        f"{''.join(f'[{i}:a]' for i in range(n))}concat=n={n}:v=0:a=1[bgm]",
        "-map", "[bgm]", "-c:a", "libmp3lame", "-b:a", "192k",
        str(bgm_full),
    ], "BGM concat")

    # ── 5. Video concat: hook + opening + main + endcard ──────────────────
    concat_txt = tmp / "concat.txt"
    concat_txt.write_text(
        f"file '{hook_mp4.as_posix()}'\n"
        f"file '{OPENING_MP4.as_posix()}'\n"
        f"file '{main_mp4.as_posix()}'\n"
        f"file '{endcard.as_posix()}'\n",
        encoding="utf-8",
    )
    video_raw = tmp / "video_raw.mp4"
    run([
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c:v", "copy", "-an",
        str(video_raw),
    ], "video concat")

    # ── 6. Burn subtitles ─────────────────────────────────────────────────
    video_subbed = tmp / "video_subbed.mp4"
    srt_path = srt_shifted.as_posix().replace(":", "\\:")
    style = (
        "FontName=Trebuchet MS,FontSize=22,PrimaryColour=&H00F5F7FA,"
        "OutlineColour=&H000A0A0C,BackColour=&H80000000,"
        "Bold=0,Outline=2,Shadow=1,MarginV=40"
    )
    run([
        FFMPEG, "-y",
        "-i", str(video_raw),
        "-vf", f"subtitles='{srt_path}':force_style='{style}'",
        "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-an",
        str(video_subbed),
    ], "subtitle burn-in")

    # ── 7. Final audio mix ────────────────────────────────────────────────
    run([
        FFMPEG, "-y",
        "-i", str(video_subbed),
        "-i", str(NARR_MP3),
        "-i", str(bgm_full),
        "-filter_complex", (
            f"[2:a]volume={BGM_VOL}[bgm];"
            "[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=3[a]"
        ),
        "-map", "0:v", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(OUT_MP4),
    ], "final audio mix")

    size_mb = OUT_MP4.stat().st_size / 1_048_576
    print(f"\n✓ {OUT_MP4}")
    print(f"  {size_mb:.1f} MB  {total_dur:.0f}s  "
          f"(hook {HOOK_END_SEC:.0f}s + opening {OPENING_SEC}s + "
          f"main {main_dur:.0f}s + endcard {ENDCARD_SEC:.0f}s)")


if __name__ == "__main__":
    main()
