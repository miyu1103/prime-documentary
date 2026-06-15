"""
scripts/assemble_v013.py
v012 からの変更:
  - ANIM_SAFE_END=615  t>=625s でアニマティックがイントロにループバックするため
  - アニマティック末尾を freeze-last-frame で 674.3s まで延ばす（tpad clone）
  - BGM を apad で total_dur+2 まで延長し amix duration=longest に変更 → 末尾無音解消
  - -shortest 廃止、代わりに -t total_dur でハードカット
  - SRT: subs_vc_v002.srt（文節境界分割・文字数比例タイミング、243 entries）
"""
from __future__ import annotations
import subprocess, sys, tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO          = Path(__file__).resolve().parents[1]
REMOTION      = REPO / "remotion"
MUSIC_DIR     = Path(r"H:\pd-media\downloads\music")
EDIT_DIR      = Path(r"H:\pd-media\episodes\PD-2026-001-miranda\07_edit\sample")
FFMPEG        = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE       = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"

COLD_OPEN_MP4 = REMOTION / "out" / "cold_open.mp4"
OPENING_MP4   = REMOTION / "out" / "opening.mp4"
ANIMATIC_MP4  = REMOTION / "out" / "animatic_motion.mp4"
NARR_MP3      = Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_voice\master\vc_master_v002.mp3")
SRT_IN        = EDIT_DIR / "subs_vc_v002.srt"
OUT_MP4       = EDIT_DIR / "sample_v021.mp4"

HOOK_SEC      = 20.0
OPENING_SEC   =  6.0
ENDCARD_SEC   = 10.0
NARR_TAIL_SEC =  4.0   # ナレーション終了後の短い余韻（すぐフェードアウト）
ANIM_SAFE_END = 643.0  # S023(チャンネル登録カード)開始直前まで — アニマティック再レンダ後 total=674s
BGM_VOL       = 0.18

BGM_TRACKS = [
    MUSIC_DIR / "mus_20260614_hook_glass_air_bed_v1.mp3",
    MUSIC_DIR / "mus_20260614_somber_ledger_of_ash_v1.mp3",
    MUSIC_DIR / "mus_20260614_outro_last_frame_v2.mp3",
    MUSIC_DIR / "mus_20260614_ambience_empty_hall_v1.mp3",
]


def run(cmd: list[str], desc: str = "", cwd: Path | None = None) -> None:
    print(f"\n>> {desc}")
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
    for p in [COLD_OPEN_MP4, OPENING_MP4, ANIMATIC_MP4, NARR_MP3, SRT_IN, *BGM_TRACKS]:
        if not p.exists():
            raise FileNotFoundError(p)
    EDIT_DIR.mkdir(parents=True, exist_ok=True)

    narr_dur       = probe_duration(NARR_MP3)
    # ナレーションのうちフック+オープニング以降に使える秒数
    narr_main_avail = narr_dur - HOOK_SEC - OPENING_SEC
    # アニマティックはANIM_SAFE_ENDまでしか使わない
    anim_trim      = min(ANIM_SAFE_END, narr_main_avail)
    # アニマティック後: ナレーション継続 + BGMのみ余韻 を freeze-last-frame で吸収
    freeze_dur     = (narr_main_avail - anim_trim) + NARR_TAIL_SEC
    main_video_dur = anim_trim + freeze_dur          # = narr_main_avail + NARR_TAIL_SEC
    total_dur      = HOOK_SEC + OPENING_SEC + main_video_dur + ENDCARD_SEC

    print(f"narr_dur        : {narr_dur:.1f}s")
    print(f"anim_trim       : {anim_trim:.1f}s  (safe animatic)")
    print(f"freeze_dur      : {freeze_dur:.1f}s  (last-frame hold + tail)")
    print(f"main_video_dur  : {main_video_dur:.1f}s")
    print(f"endcard         : {ENDCARD_SEC}s")
    print(f"total           : {total_dur:.1f}s  ({total_dur/60:.1f} min)")

    tmp = Path(tempfile.gettempdir()) / "pd_v013"
    tmp.mkdir(exist_ok=True)

    import shutil
    for font_src, font_name in [
        (r"C:\Windows\Fonts\impact.ttf", "impact.ttf"),
        (r"C:\Windows\Fonts\trebuc.ttf", "trebuc.ttf"),
    ]:
        shutil.copy2(font_src, tmp / font_name)

    # ── 1. Endcard (20s) ─────────────────────────────────────────────────────
    endcard = tmp / "endcard.mp4"
    run([
        FFMPEG, "-y",
        "-f", "lavfi",
        "-i", f"color=color=0x0A0A0C:s=1920x1080:r=30:d={ENDCARD_SEC}",
        "-vf", (
            f"fade=t=in:st=0:d=0.5:color=black,"
            f"fade=t=out:st={ENDCARD_SEC - 0.8}:d=0.8:color=black,"
            "drawtext=fontfile=impact.ttf"
            ":text=PRIME DOCUMENTARY"
            ":fontsize=88:fontcolor=E5B53A@0.95"
            ":x=(w-text_w)/2:y=(h-text_h)/2-80,"
            "drawtext=fontfile=trebuc.ttf"
            ":text=New episodes every week"
            ":fontsize=32:fontcolor=C8CDD6@0.85"
            ":x=(w-text_w)/2:y=(h-text_h)/2+20,"
            "drawtext=fontfile=trebuc.ttf"
            ":text=Next - Gideon v. Wainwright"
            ":fontsize=26:fontcolor=8B929F@0.80"
            ":x=(w-text_w)/2:y=(h-text_h)/2+68"
        ),
        "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-an",
        str(endcard),
    ], "endcard", cwd=tmp)

    # ── 2a. Trim animatic to safe end (no tpad — separate filler is more reliable)
    main_mp4 = tmp / "main.mp4"
    run([
        FFMPEG, "-y",
        "-t", f"{anim_trim:.3f}",
        "-i", str(ANIMATIC_MP4),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-an",
        str(main_mp4),
    ], f"trim animatic {anim_trim:.1f}s")

    # ── 2b. Filler: アニマティック最終フレームのフリーズ (黒画面回避) ──────────
    last_frame = tmp / "last_frame.png"
    run([
        FFMPEG, "-y",
        "-sseof", "-0.5", "-i", str(main_mp4),
        "-frames:v", "1", str(last_frame),
    ], "extract last frame")
    filler_mp4 = tmp / "filler.mp4"
    run([
        FFMPEG, "-y",
        "-loop", "1", "-i", str(last_frame),
        "-t", f"{freeze_dur:.3f}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-an",
        str(filler_mp4),
    ], f"freeze filler {freeze_dur:.1f}s")

    # ── 3. Video concat: ColdOpen + Opening + Main + Filler + Endcard ─────────
    # filter_complex concat を使う: cold_open/opening は音声ストリームを持つが
    # main/filler/endcard は映像のみ。concat デマルチプレクサはストリーム数の
    # 不一致で途中停止するため filter_complex で明示的に v:0 のみ結合する。
    video_raw = tmp / "video_raw.mp4"
    segs = [COLD_OPEN_MP4, OPENING_MP4, main_mp4, filler_mp4, endcard]
    inputs = [arg for s in segs for arg in ("-i", str(s))]
    n = len(segs)
    fc = "".join(f"[{i}:v:0]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vout]"
    run([
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", fc,
        "-map", "[vout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-an",
        str(video_raw),
    ], "video concat")

    # ── 4. Burn subtitles ─────────────────────────────────────────────────────
    video_subbed = tmp / "video_subbed.mp4"
    srt_path = SRT_IN.as_posix().replace(":", "\\:")
    style = (
        "FontName=Trebuchet MS,FontSize=22,PrimaryColour=&H00F5F7FA,"
        "OutlineColour=&H000A0A0C,BackColour=&H80000000,"
        "Bold=0,Outline=2,Shadow=1,MarginV=40"
    )
    run([
        FFMPEG, "-y",
        "-i", str(video_raw),
        "-vf", f"subtitles='{srt_path}':force_style='{style}'",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-an",
        str(video_subbed),
    ], "subtitle burn-in")

    # ── 5. BGM concat ─────────────────────────────────────────────────────────
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

    # ── 6. Final audio mix ────────────────────────────────────────────────────
    # BGM を apad で total_dur+2 まで延長し amix duration=longest で結合
    # → ナレーション終了後もBGMが継続、エンドカードまで音途切れなし
    pad_to  = int(total_dur) + 2
    fade_st = narr_dur + NARR_TAIL_SEC - 3.0  # ナレーション終了直後からフェードアウト
    tmp_out = OUT_MP4.with_suffix(".tmp.mp4")
    run([
        FFMPEG, "-y",
        "-i", str(video_subbed),
        "-i", str(NARR_MP3),
        "-i", str(bgm_full),
        "-filter_complex", (
            f"[2:a]volume={BGM_VOL},"
            f"afade=t=out:st={fade_st:.1f}:d=3.5,"
            f"apad=whole_dur={pad_to}[bgm_padded];"
            "[1:a][bgm_padded]amix=inputs=2:duration=longest:dropout_transition=5[a]"
        ),
        "-map", "0:v", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-t", f"{total_dur:.3f}",
        str(tmp_out),
    ], "final audio mix")
    tmp_out.replace(OUT_MP4)

    size_mb = OUT_MP4.stat().st_size / 1_048_576
    actual_dur = probe_duration(OUT_MP4)
    print(f"\n>> {OUT_MP4}")
    print(f"   {size_mb:.1f} MB  expected={total_dur:.0f}s  actual={actual_dur:.1f}s")


if __name__ == "__main__":
    main()
