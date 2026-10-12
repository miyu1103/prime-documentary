#!/usr/bin/env python3
"""Build PD-2026-007 Riley final v002 local package render.

Renders the revised Remotion RileyPremium structure:
hook -> branded opening -> main story -> ending/endcard.
No YouTube write happens in this script.
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
EP = "PD-2026-007-riley"
EPDIR = ROOT / "episodes" / EP
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EPM = MEDIA / "episodes" / EP

REMOTION = ROOT / "remotion"
VISUAL = EPM / "08_edit" / "riley_visual_v002.mp4"
OUT_MEDIA = EPM / "08_edit" / "riley_final_v002.mp4"
NARR_MASTER = EPM / "06_voice" / "master" / "vc_master_v001.mp3"
NARR_FIT = EPM / "06_voice" / "master" / "vc_master_v002_fit_640s.wav"
NARR_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
CAPTIONS = EPDIR / "08_edit" / "captions.final.v002.srt"
QC_REPO = EPDIR / "08_edit" / "renders" / "final.v002.qc.json"
YOUTUBE_META = EPDIR / "09_package" / "youtube_meta.v002.json"
FINAL_DELIVERY = EPDIR / "09_package" / "final_delivery.v002.json"
THUMBNAILS = EPDIR / "09_package" / "thumbnail_candidates.v001.json"

TOTAL_SEC = 646.0
NARR_TARGET_SEC = 640.0
APPROVAL_ID = "APR-0004"
TITLE = "The Supreme Court Case That Put a Warrant on Your Phone"
THUMB_ASSET_ID = "PD-2026-007-THUMB-001"
FFMPEG = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
FFPROBE = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe")
if not FFMPEG.exists():
    FFMPEG = Path("ffmpeg")
if not FFPROBE.exists():
    FFPROBE = Path("ffprobe")
NPX = shutil.which("npx.cmd") or shutil.which("npx") or "npx"


def run(cmd: list[str | os.PathLike[str]], desc: str) -> subprocess.CompletedProcess[str]:
    print(f">> {desc}")
    p = subprocess.run([str(x) for x in cmd], capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print((p.stdout or "")[-1800:])
        print((p.stderr or "")[-3200:])
        raise RuntimeError(desc)
    return p


def run_in(cmd: list[str | os.PathLike[str]], desc: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    print(f">> {desc}")
    p = subprocess.run([str(x) for x in cmd], cwd=str(cwd), capture_output=True, encoding="utf-8", errors="replace")
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
    return re.sub(r"\s+", " ", text).strip()


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


def fit_narration() -> float:
    src_dur = duration(NARR_MASTER)
    atempo = src_dur / NARR_TARGET_SEC
    NARR_FIT.parent.mkdir(parents=True, exist_ok=True)
    run([
        FFMPEG,
        "-y",
        "-i",
        NARR_MASTER,
        "-filter:a",
        f"aresample=48000,asetpts=PTS-STARTPTS,{atempo_filters(atempo)},alimiter=limit=0.92",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-c:a",
        "pcm_s16le",
        NARR_FIT,
    ], f"fit ElevenLabs narration through PCM {src_dur:.1f}s -> {NARR_TARGET_SEC:.1f}s")
    return duration(NARR_FIT)


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
            dur = max(1.05, (end - start) * weight / total)
            part_end = min(end, cursor + dur)
            if part_end <= cursor:
                part_end = cursor + 0.8
            cues.append(f"{cue}\n{ts_srt(cursor)} --> {ts_srt(part_end)}\n{part}\n")
            cue += 1
            cursor = part_end
    CAPTIONS.write_text("\n".join(cues), encoding="utf-8")
    print(f"captions={CAPTIONS} cues={cue - 1}")


def music_file() -> Path:
    preferred = MEDIA / "library" / "music" / "reveal" / "mus_20260614_reveal_hidden_system_clicks_v2.mp3"
    if preferred.exists():
        return preferred
    fallback = MEDIA / "library" / "music" / "explainer_bed" / "mus_20260614_explainer_bed_soft_explainer_v2.mp3"
    if fallback.exists():
        return fallback
    found = sorted((MEDIA / "library" / "music").rglob("*.mp3"))
    if not found:
        raise FileNotFoundError("No library music found")
    return found[0]


def render_visual_if_needed() -> None:
    if VISUAL.exists() and VISUAL.stat().st_size > 1024 * 1024:
        print(f"visual exists -> {VISUAL}")
        return
    VISUAL.parent.mkdir(parents=True, exist_ok=True)
    run_in([
        NPX,
        "remotion",
        "render",
        "src/riley_index.tsx",
        "RileyPremium",
        str(VISUAL),
        "--codec=h264",
        "--crf=16",
        "--pixel-format=yuv420p",
        "--overwrite",
    ], "render revised RileyPremium visual v002", cwd=REMOTION)


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
        NARR_FIT,
        "-stream_loop",
        "-1",
        "-i",
        music,
        "-filter_complex",
        f"[1:a]volume=1.0[n];[2:a]atrim=0:{TOTAL_SEC:.3f},volume=0.082,afade=t=in:st=0:d=3,afade=t=out:st={TOTAL_SEC-5:.3f}:d=5[m];[n][m]amix=inputs=2:duration=longest:dropout_transition=0,loudnorm=I=-14:TP=-1.5:LRA=11:linear=false,alimiter=limit=0.93[a]",
        "-map",
        "0:v",
        "-map",
        "[a]",
        "-t",
        f"{TOTAL_SEC:.3f}",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-ar",
        "48000",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        OUT_MEDIA,
    ], "mux Riley final v002 render with ElevenLabs VO, library music, and sidecar captions")


def selected_thumbnail() -> dict:
    data = json.loads(THUMBNAILS.read_text("utf-8"))
    for item in data.get("candidates", []):
        if item.get("asset_id") == THUMB_ASSET_ID:
            return item
    raise RuntimeError(f"Missing thumbnail candidate {THUMB_ASSET_ID}")


def description() -> str:
    return (
        "A police officer arrests you and takes the phone from your pocket. Can he open it without a warrant?\n\n"
        "This episode explains Riley v. California, the 2014 Supreme Court case that changed how the Fourth Amendment applies to the device most people carry everywhere. The Court had to decide whether a phone is just another item in your pocket, or something different in kind: messages, photos, location history, apps, and the private record of a life.\n\n"
        "We trace David Riley's traffic stop, the older search-incident-to-arrest rule, the unanimous Supreme Court decision, and why the phrase \"get a warrant\" became the new baseline for phone searches after arrest.\n\n"
        "This is an educational documentary, not legal advice.\n\n"
        "Visual note: this video uses AI-generated symbolic reconstructions and motion graphics. They are not authentic footage, and no real-person likeness is intended.\n\n"
        "Next episode: the location trail your phone leaves behind.\n\n"
        "Chapters:\n"
        "00:00 Can police open your phone?\n"
        "00:28 Opening: a phone is not a pocket\n"
        "01:12 David Riley's arrest\n"
        "03:14 The old pocket-search rule\n"
        "05:41 Get a warrant\n"
        "08:37 Why smartphones changed the rule\n"
        "10:03 The edge of protection\n"
        "10:37 Next: location records"
    )


def write_package_and_qc(narr_dur: float) -> dict:
    thumb = selected_thumbnail()
    final_dur = duration(OUT_MEDIA)
    video_sha = sha256(OUT_MEDIA)
    q = {
        "schema_version": "final_qc_v1",
        "episode_id": EP,
        "revision": "v002",
        "render": "artifact://episodes/PD-2026-007-riley/08_edit/riley_final_v002.mp4",
        "render_actual_path": str(OUT_MEDIA),
        "sha256": video_sha,
        "duration_seconds": round(final_dur, 3),
        "target_duration_seconds": TOTAL_SEC,
        "visual_source": str(VISUAL),
        "structure": {
            "hook": "00:00-00:28",
            "opening": "00:28-01:12, includes branded opening bumper",
            "main_body": "01:12-10:03, case facts, old rule, ruling, meaning",
            "ending": "10:03-10:46, edge of protection and next-episode bridge",
        },
        "audio": {
            "narration": "ElevenLabs channel voice fit to final timeline",
            "narration_master": "artifact://episodes/PD-2026-007-riley/06_voice/master/vc_master_v001.mp3",
            "narration_fit": "artifact://episodes/PD-2026-007-riley/06_voice/master/vc_master_v002_fit_640s.wav",
            "narration_fit_seconds": round(narr_dur, 3),
            "music": str(music_file()),
        },
        "captions_sidecar": "artifact://episodes/PD-2026-007-riley/08_edit/captions.final.v002.srt",
        "thumbnail": thumb["file"],
        "thumbnail_sha256": thumb["content_hash"],
        "title": TITLE,
        "synthetic_content_disclosure_required": True,
        "upload_performed": False,
        "publish_performed": False,
        "approval_ids": ["APR-0001", "APR-0002", APPROVAL_ID],
        "qc_status": "pass_with_warnings",
        "warnings": [
            "Captions are generated as a sidecar SRT and should be uploaded to YouTube as an English caption track.",
            "Caption timing is derived from ElevenLabs chunk timings, not Whisper word-level forced alignment.",
            "Synthetic-content disclosure is required because symbolic AI reconstructions are used.",
            "Upload/publish is handled by a separate guarded script.",
        ],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    QC_REPO.parent.mkdir(parents=True, exist_ok=True)
    QC_REPO.write_text(json.dumps(q, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v002",
        "status": "package_ready_no_publish",
        "title": TITLE,
        "description": description(),
        "tags": [
            "Riley v California",
            "Riley v. California",
            "Fourth Amendment",
            "phone search",
            "cell phone warrant",
            "search incident to arrest",
            "Supreme Court cases",
            "constitutional law",
            "privacy rights",
            "criminal procedure",
            "digital privacy",
            "Prime Documentary",
        ],
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
        "thumbnail": thumb["file"],
        "selected_thumbnail": thumb["file"],
        "selected_thumbnail_sha256": thumb["content_hash"],
        "video": "artifact://episodes/PD-2026-007-riley/08_edit/riley_final_v002.mp4",
        "video_actual_path": str(OUT_MEDIA),
        "video_sha256": "sha256:" + video_sha,
        "synthetic_content_disclosure_required": True,
        "contains_ai_symbolic_reconstruction": True,
        "upload_performed": False,
        "publish_performed": False,
        "approval_ids": ["APR-0001", "APR-0002", APPROVAL_ID],
        "pre_publish_checks": {
            "rights_manifest": "episodes/PD-2026-007-riley/09_package/rights_manifest.v001.json",
            "final_qc": "episodes/PD-2026-007-riley/08_edit/renders/final.v002.qc.json",
            "synthetic_content_disclosure_required": True,
            "publish_approval_required": True,
            "upload_performed": False,
            "publish_performed": False,
        },
    }
    YOUTUBE_META.parent.mkdir(parents=True, exist_ok=True)
    YOUTUBE_META.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    delivery = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v002",
        "status": "final_package_ready",
        "title": TITLE,
        "video": str(OUT_MEDIA),
        "video_sha256": "sha256:" + video_sha,
        "thumbnail": thumb["file"],
        "thumbnail_sha256": thumb["content_hash"],
        "youtube_meta": str(YOUTUBE_META.relative_to(ROOT)).replace("\\", "/"),
        "final_qc": str(QC_REPO.relative_to(ROOT)).replace("\\", "/"),
        "approval_ids": ["APR-0001", "APR-0002", APPROVAL_ID],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    FINAL_DELIVERY.write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"qc={QC_REPO}")
    print(f"youtube_meta={YOUTUBE_META}")
    print(f"final_delivery={FINAL_DELIVERY}")
    return q


def main() -> None:
    if not NARR_MASTER.exists():
        raise FileNotFoundError(NARR_MASTER)
    render_visual_if_needed()
    narr_dur = fit_narration()
    write_captions()
    mux_final()
    q = write_package_and_qc(narr_dur)
    print(json.dumps({"render": str(OUT_MEDIA), "sha256": q["sha256"], "duration_seconds": q["duration_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
