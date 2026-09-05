#!/usr/bin/env python3
"""Build PD-2026-006 Terry first-cut review proxy.

No paid API, no upload, no publish. Narration is local Windows SAPI draft audio
only; replace with approved ElevenLabs master after owner approval.
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
PUBLIC_TERRY = REMOTION / "public" / "terry"
SELECTED = EPM / "05_visuals" / "selected"
VISUAL = EPM / "08_edit" / "terry_visual_v001.mp4"
OUT_MEDIA = EPM / "08_edit" / "terry_review_proxy_v001.mp4"
VOICE_DIR = EPM / "06_voice" / "draft_local"
NARR_WAV = VOICE_DIR / "terry_local_sapi_draft_v001.wav"
NARR_FIT = VOICE_DIR / "terry_local_sapi_draft_v001_fit.wav"
SCRIPT_TXT = VOICE_DIR / "terry_local_sapi_text_v001.txt"
CAPTIONS = EPDIR / "08_edit" / "captions.review_proxy.v001.srt"
QC_REPO = EPDIR / "08_edit" / "renders" / "review.proxy.v001.qc.json"
RENDER_REF = "artifact://episodes/PD-2026-006-terry/08_edit/terry_review_proxy_v001.mp4"
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
    chunks: list[str] = []
    for raw in body.splitlines():
        line = raw.strip()
        if line.startswith("[VO:]"):
            chunks.append(clean_vo(line))
    if not chunks:
        raise RuntimeError("No [VO:] chunks found")
    return chunks


def wrap_caption(text: str, max_chars: int = 78) -> str:
    words = text.split()
    lines: list[str] = []
    cur: list[str] = []
    for word in words:
        candidate = " ".join(cur + [word])
        if len(candidate) > max_chars and cur:
            lines.append(" ".join(cur))
            cur = [word]
        else:
            cur.append(word)
        if len(lines) == 2:
            break
    if cur and len(lines) < 2:
        lines.append(" ".join(cur))
    return "\n".join(lines)


def write_captions(chunks: list[str]) -> None:
    CAPTIONS.parent.mkdir(parents=True, exist_ok=True)
    weights = [max(5, len(c.split())) for c in chunks]
    total = sum(weights)
    cursor = 0.0
    cues: list[str] = []
    cue_id = 1
    for chunk, weight in zip(chunks, weights):
        dur = NARR_TARGET_SEC * weight / total
        # Split long paragraphs into readable caption cards without changing words.
        words = chunk.split()
        parts: list[str] = []
        part: list[str] = []
        for word in words:
            part.append(word)
            if len(" ".join(part)) >= 90:
                parts.append(" ".join(part))
                part = []
        if part:
            parts.append(" ".join(part))
        per = dur / max(1, len(parts))
        for part_text in parts:
            start = cursor
            end = min(NARR_TARGET_SEC, cursor + max(1.8, per))
            cues.append(f"{cue_id}\n{ts_srt(start)} --> {ts_srt(end)}\n{wrap_caption(part_text)}\n")
            cue_id += 1
            cursor = end
    CAPTIONS.write_text("\n".join(cues), encoding="utf-8")
    print(f"captions={CAPTIONS} cues={cue_id - 1}")


def prepare_public_images() -> list[Path]:
    PUBLIC_TERRY.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for src in sorted(SELECTED.rglob("*.png")):
        dst = PUBLIC_TERRY / src.name
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)
        copied.append(src)
    if len(copied) < 3:
        raise FileNotFoundError(f"Expected approved Terry images under {SELECTED}, found {len(copied)}")
    print(f"copied_or_verified_images={len(copied)} -> {PUBLIC_TERRY}")
    return copied


def render_visual() -> None:
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


def make_local_tts(chunks: list[str]) -> None:
    VOICE_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPT_TXT.write_text("\n\n".join(chunks), encoding="utf-8")
    ps = VOICE_DIR / "make_sapi_tts_v001.ps1"
    ps.write_text(
        "\n".join([
            "param([string]$TextPath,[string]$OutPath)",
            "Add-Type -AssemblyName System.Speech",
            "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer",
            "$synth.Rate = -1",
            "$synth.Volume = 100",
            "$synth.SetOutputToWaveFile($OutPath)",
            "$text = Get-Content -Raw -Encoding UTF8 $TextPath",
            "$synth.Speak($text)",
            "$synth.Dispose()",
        ]),
        encoding="utf-8",
    )
    run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps, SCRIPT_TXT, NARR_WAV], "generate local SAPI draft narration")
    src_dur = duration(NARR_WAV)
    atempo = src_dur / NARR_TARGET_SEC
    filters = atempo_filters(atempo)
    run([
        FFMPEG,
        "-y",
        "-i",
        NARR_WAV,
        "-filter:a",
        f"{filters},alimiter=limit=0.92",
        "-ar",
        "48000",
        "-ac",
        "2",
        NARR_FIT,
    ], f"fit local narration {src_dur:.1f}s -> {NARR_TARGET_SEC:.1f}s")


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
    return ",".join(f"atempo={p:.9f}" for p in parts)


def music_file() -> Path:
    candidates = [
        MEDIA / "library" / "music" / "explainer_bed" / "mus_20260614_explainer_bed_soft_explainer_v2.mp3",
        MEDIA / "library" / "music" / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v2.mp3",
        MEDIA / "library" / "music" / "ambience" / "mus_20260614_ambience_empty_hall_v2.mp3",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    found = sorted((MEDIA / "library" / "music").rglob("*.mp3"))
    if not found:
        raise FileNotFoundError("No library music found")
    return found[0]


def ffmpeg_subtitles_filter() -> str:
    path = CAPTIONS.resolve().as_posix().replace(":", r"\:")
    style = "FontName=Trebuchet MS,FontSize=20,PrimaryColour=&H00F5F7FA,OutlineColour=&H99000000,BorderStyle=1,Outline=2,Shadow=0,MarginV=42"
    return f"subtitles='{path}':force_style='{style}'"


def mux_review() -> None:
    OUT_MEDIA.parent.mkdir(parents=True, exist_ok=True)
    music = music_file()
    run([
        FFMPEG,
        "-y",
        "-i",
        VISUAL,
        "-i",
        NARR_FIT,
        "-stream_loop",
        "-1",
        "-i",
        music,
        "-filter_complex",
        "[1:a]volume=1.0[n];[2:a]atrim=0:678,volume=0.105,afade=t=in:st=0:d=3,afade=t=out:st=672:d=5[m];[n][m]amix=inputs=2:duration=longest:dropout_transition=0,alimiter=limit=0.93[a]",
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
        "16",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        OUT_MEDIA,
    ], "mux review proxy with captions, local draft VO, and library music")


def write_qc() -> dict:
    dur = duration(OUT_MEDIA)
    q = {
        "schema_version": "first_cut_qc_v1",
        "episode_id": EP,
        "revision": "v001",
        "render": "08_edit/renders/review.proxy.v001.mp4",
        "heavy_media_render": RENDER_REF,
        "render_actual_path": str(OUT_MEDIA),
        "sha256": sha256(OUT_MEDIA),
        "duration_seconds": round(dur, 3),
        "target_duration_seconds": TOTAL_SEC,
        "video": {
            "renderer": "Remotion TerryPremium",
            "codec_finish": "FFmpeg libx264 crf16 slow",
            "symbolic_reconstruction_label": "present on AI/symbolic street reenactment scenes",
            "no_real_person_likeness": True,
        },
        "audio": {
            "narration": "local Windows SAPI draft proxy, not ElevenLabs master",
            "paid_api_used": False,
            "music": str(music_file()),
        },
        "captions": {
            "source": "locked script.en.v001.md [VO:] lines",
            "file": "08_edit/captions.review_proxy.v001.srt",
            "timing": "approximate proxy timing; re-align after approved ElevenLabs master",
        },
        "rights": {
            "ai_images_registered": True,
            "synthetic_content_disclosure_required": True,
            "external_upload": False,
            "publish_ready": False,
        },
        "gate": {
            "status": "first_cut_review_ready",
            "next_required_approval": "owner first-cut approval before ElevenLabs paid narration/title-thumbnail/publish steps",
        },
        "warnings": [
            "Review proxy uses local draft TTS because ElevenLabs paid run requires explicit owner approval.",
            "Only approved/right-registered AI stills are included; high-risk human contact beats are Remotion graphics.",
            "Caption timing is approximate and must be force-aligned after final narration.",
        ],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    QC_REPO.parent.mkdir(parents=True, exist_ok=True)
    QC_REPO.write_text(json.dumps(q, indent=2) + "\n", encoding="utf-8")
    print(f"qc={QC_REPO}")
    return q


def main() -> None:
    chunks = parse_vo_chunks()
    prepare_public_images()
    write_captions(chunks)
    render_visual()
    make_local_tts(chunks)
    mux_review()
    qc = write_qc()
    print(json.dumps({"render": str(OUT_MEDIA), "sha256": qc["sha256"], "duration_seconds": qc["duration_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
