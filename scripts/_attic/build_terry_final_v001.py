#!/usr/bin/env python3
"""Build PD-2026-006 Terry final local package render.

Uses approved ElevenLabs narration master. No upload and no publish.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-006-terry"
EPDIR = ROOT / "episodes" / EP
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EPM = MEDIA / "episodes" / EP
REMOTION = ROOT / "remotion"
VISUAL = EPM / "08_edit" / "terry_visual_v001.mp4"
OUT_MEDIA = EPM / "08_edit" / "terry_final_v001.mp4"
NARR_MASTER = EPM / "06_voice" / "master" / "vc_master_v001.mp3"
NARR_SLOW = EPM / "06_voice" / "master" / "vc_master_v001_slowed_672s.mp3"
NARR_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
CAPTIONS = EPDIR / "08_edit" / "captions.final.v001.srt"
QC_REPO = EPDIR / "08_edit" / "renders" / "final.v001.qc.json"
YOUTUBE_META = EPDIR / "09_package" / "youtube_meta.v001.json"
TOTAL_SEC = 678.0
NARR_TARGET_SEC = 672.0
FFMPEG = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
FFPROBE = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe")
if not FFMPEG.exists():
    FFMPEG = Path("ffmpeg")
if not FFPROBE.exists():
    FFPROBE = Path("ffprobe")
NPX = shutil.which("npx.cmd") or shutil.which("npx") or "npx"


def run(cmd: list[str | os.PathLike[str]], desc: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    print(f">> {desc}")
    p = subprocess.run([str(x) for x in cmd], cwd=str(cwd) if cwd else None, capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print((p.stdout or "")[-1800:])
        print((p.stderr or "")[-3200:])
        raise RuntimeError(desc)
    return p


def duration(path: Path) -> float:
    p = run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], f"probe {path.name}")
    return float(p.stdout.strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def ts_srt(t: float) -> str:
    t = max(0.0, t)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - math.floor(t)) * 1000))
    if ms == 1000:
        s += 1
        ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def clean_vo(text: str) -> str:
    text = re.sub(r"\[CLM-[0-9]{4}\]", "", text)
    text = re.sub(r"^\[VO:\]\s*", "", text.strip())
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_vo_chunks() -> list[str]:
    body = (EPDIR / "03_script" / "script.en.v001.md").read_text("utf-8")
    chunks = [clean_vo(line) for line in body.splitlines() if line.strip().startswith("[VO:]")]
    if not chunks:
        raise RuntimeError("No [VO:] chunks found")
    return chunks


def atempo_filters(value: float) -> str:
    parts: list[float] = []
    remaining = value
    while remaining > 2.0:
        parts.append(2.0)
        remaining /= 2.0
    while remaining < 0.5:
        parts.append(0.5)
        remaining /= 0.5
    parts.append(remaining)
    return ",".join(f"atempo={part:.9f}" for part in parts)


def slow_narration() -> float:
    src_dur = duration(NARR_MASTER)
    atempo = src_dur / NARR_TARGET_SEC
    NARR_SLOW.parent.mkdir(parents=True, exist_ok=True)
    run([
        FFMPEG,
        "-y",
        "-i",
        NARR_MASTER,
        "-filter:a",
        f"{atempo_filters(atempo)},alimiter=limit=0.92",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-c:a",
        "libmp3lame",
        "-b:a",
        "192k",
        NARR_SLOW,
    ], f"slow ElevenLabs narration {src_dur:.1f}s -> {NARR_TARGET_SEC:.1f}s")
    return duration(NARR_SLOW)


def split_caption_parts(text: str) -> list[str]:
    words = text.split()
    parts: list[str] = []
    cur: list[str] = []
    for word in words:
        trial = " ".join(cur + [word])
        if cur and (len(cur) >= 8 or len(trial) > 46):
            parts.append(" ".join(cur))
            cur = []
        cur.append(word)
        if re.search(r"[.?!]$", word) or (word.endswith(",") and len(cur) >= 5):
            parts.append(" ".join(cur))
            cur = []
    if cur:
        parts.append(" ".join(cur))
    return parts


def write_captions() -> None:
    chunks = parse_vo_chunks()
    index = json.loads(NARR_INDEX.read_text("utf-8"))["chunks"]
    scale = NARR_TARGET_SEC / float(index[-1]["end"])
    CAPTIONS.parent.mkdir(parents=True, exist_ok=True)
    cues: list[str] = []
    cue = 1
    for text, item in zip(chunks, index):
        start = float(item["start"]) * scale
        end = float(item["end"]) * scale
        parts = split_caption_parts(text)
        weights = [max(1, len(part.split())) for part in parts]
        total = sum(weights)
        cursor = start
        for part, weight in zip(parts, weights):
            dur = max(1.15, (end - start) * weight / total)
            part_end = min(end, cursor + dur)
            if part_end <= cursor:
                part_end = cursor + 0.8
            cues.append(f"{cue}\n{ts_srt(cursor)} --> {ts_srt(part_end)}\n{part}\n")
            cue += 1
            cursor = part_end
    CAPTIONS.write_text("\n".join(cues), encoding="utf-8")
    print(f"captions={CAPTIONS} cues={cue - 1}")


def render_visual_if_needed() -> None:
    if VISUAL.exists() and VISUAL.stat().st_size > 1024 * 1024:
        print(f"visual exists -> {VISUAL}")
        return
    VISUAL.parent.mkdir(parents=True, exist_ok=True)
    run([
        NPX,
        "remotion",
        "render",
        "src/terry_index.tsx",
        "TerryPremium",
        str(VISUAL),
        "--codec=h264",
        "--crf=16",
        "--pixel-format=yuv420p",
        "--overwrite",
    ], "render TerryPremium visual", cwd=REMOTION)


def music_file() -> Path:
    preferred = MEDIA / "library" / "music" / "explainer_bed" / "mus_20260614_explainer_bed_soft_explainer_v2.mp3"
    if preferred.exists():
        return preferred
    found = sorted((MEDIA / "library" / "music").rglob("*.mp3"))
    if not found:
        raise FileNotFoundError("No library music found")
    return found[0]


def ffmpeg_subtitles_filter() -> str:
    path = CAPTIONS.resolve().as_posix().replace(":", r"\:")
    style = "FontName=Trebuchet MS,FontSize=20,PrimaryColour=&H00F5F7FA,OutlineColour=&H99000000,BorderStyle=1,Outline=2,Shadow=0,MarginV=42"
    return f"subtitles='{path}':force_style='{style}'"


def mux_final() -> None:
    OUT_MEDIA.parent.mkdir(parents=True, exist_ok=True)
    music = music_file()
    run([
        FFMPEG,
        "-y",
        "-i",
        VISUAL,
        "-i",
        NARR_SLOW,
        "-stream_loop",
        "-1",
        "-i",
        music,
        "-filter_complex",
        "[1:a]volume=1.0[n];[2:a]atrim=0:678,volume=0.095,afade=t=in:st=0:d=3,afade=t=out:st=672:d=5[m];[n][m]amix=inputs=2:duration=longest:dropout_transition=0,loudnorm=I=-14:TP=-1.5:LRA=11:linear=false,alimiter=limit=0.93[a]",
        "-vf",
        ffmpeg_subtitles_filter(),
        "-map",
        "0:v",
        "-map",
        "[a]",
        "-t",
        f"{TOTAL_SEC:.3f}",
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "15",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-ar",
        "48000",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        OUT_MEDIA,
    ], "mux final render with captions, ElevenLabs VO, and library music")


def write_package_and_qc(narr_dur: float) -> dict:
    final_dur = duration(OUT_MEDIA)
    q = {
        "schema_version": "final_qc_v1",
        "episode_id": EP,
        "revision": "v001",
        "render": "artifact://episodes/PD-2026-006-terry/08_edit/terry_final_v001.mp4",
        "render_actual_path": str(OUT_MEDIA),
        "sha256": sha256(OUT_MEDIA),
        "duration_seconds": round(final_dur, 3),
        "target_duration_seconds": TOTAL_SEC,
        "video": "Remotion TerryPremium, approved AI stills only, symbolic reconstruction labels on AI/symbolic reenactment scenes",
        "audio": {
            "narration": "ElevenLabs channel voice slowed to fit timeline",
            "narration_master": "artifact://episodes/PD-2026-006-terry/06_voice/master/vc_master_v001.mp3",
            "narration_slowed": "artifact://episodes/PD-2026-006-terry/06_voice/master/vc_master_v001_slowed_672s.mp3",
            "narration_slowed_seconds": round(narr_dur, 3),
            "music": str(music_file()),
        },
        "captions": "artifact://episodes/PD-2026-006-terry/08_edit/captions.final.v001.srt",
        "thumbnail": "artifact://episodes/PD-2026-006-terry/10_thumbnail/thumbnail_option_01.v001.png",
        "title": "A Cop Can Search You Without a Warrant - Here's the Catch",
        "synthetic_content_disclosure_required": True,
        "upload_performed": False,
        "publish_performed": False,
        "approval_ids": ["APR-0001", "APR-0002", "APR-0003"],
        "qc_status": "pass_with_warnings",
        "warnings": [
            "No publish/upload approval; package is local final-ready only.",
            "Caption timing is derived from ElevenLabs chunk timings and uniform slowdown, not Whisper word-level forced alignment.",
            "Synthetic-content disclosure is required because symbolic AI reconstructions are used.",
        ],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    QC_REPO.parent.mkdir(parents=True, exist_ok=True)
    QC_REPO.write_text(json.dumps(q, indent=2) + "\n", encoding="utf-8")
    YOUTUBE_META.parent.mkdir(parents=True, exist_ok=True)
    YOUTUBE_META.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "episode_id": EP,
                "revision": "v001",
                "status": "package_ready_no_publish",
                "title": q["title"],
                "thumbnail": "episodes/PD-2026-006-terry/10_thumbnail/thumbnail_option_01.v001.png",
                "video": "artifact://episodes/PD-2026-006-terry/08_edit/terry_final_v001.mp4",
                "video_sha256": q["sha256"],
                "synthetic_content_disclosure_required": True,
                "contains_ai_symbolic_reconstruction": True,
                "upload_performed": False,
                "publish_performed": False,
                "approval_ids": q["approval_ids"],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"qc={QC_REPO}")
    print(f"youtube_meta={YOUTUBE_META}")
    return q


def main() -> None:
    if not NARR_MASTER.exists():
        raise FileNotFoundError(NARR_MASTER)
    render_visual_if_needed()
    narr_dur = slow_narration()
    write_captions()
    mux_final()
    q = write_package_and_qc(narr_dur)
    print(json.dumps({"render": str(OUT_MEDIA), "sha256": q["sha256"], "duration_seconds": q["duration_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
