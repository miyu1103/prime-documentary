#!/usr/bin/env python3
"""Build PD-2026-006 Terry v002 local remake.

Uses approved narration. Rebuilds visuals from 180 v002 symbolic plates.
No upload and no publish.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-006-terry"
EPDIR = ROOT / "episodes" / EP
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EPM = MEDIA / "episodes" / EP
LIB = MEDIA / "library"
REMOTION = ROOT / "remotion"
PUBLIC_TERRY = REMOTION / "public" / "terry"
SDXL_HQ_V002 = EPM / "05_visuals" / "sdxl_hq_v002_180"
VISUAL = EPM / "08_edit" / "terry_visual_v002.mp4"
OUT_MEDIA = EPM / "08_edit" / "terry_final_v002.mp4"
NARR_MASTER = EPM / "06_voice" / "master" / "vc_master_v001.mp3"
NARR_SLOW = EPM / "06_voice" / "master" / "vc_master_v001_slowed_672s_for_v002.mp3"
NARR_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
CAPTIONS = EPDIR / "08_edit" / "captions.final.v002.srt"
QC_REPO = EPDIR / "08_edit" / "renders" / "final.v002.qc.json"
CONTACT_SHEET = EPDIR / "08_edit" / "renders" / "final.v002.contact_sheet.jpg"
RIGHTS = EPDIR / "09_package" / "rights_manifest.v002.json"
DELIVERY = EPDIR / "09_package" / "final_delivery.v002.json"
EVENTS = EPDIR / "events" / "events.jsonl"
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
    print(f">> {desc}", flush=True)
    p = subprocess.run([str(x) for x in cmd], cwd=str(cwd) if cwd else None, capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print((p.stdout or "")[-1800:])
        print((p.stderr or "")[-3600:])
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


def prepare_public_images() -> list[Path]:
    if not SDXL_HQ_V002.exists():
        raise FileNotFoundError(SDXL_HQ_V002)
    generated = [p for p in sorted(SDXL_HQ_V002.rglob("*.png")) if "rejected_initial" not in p.parts]
    if len(generated) < 180:
        raise RuntimeError(f"Expected 180 v002 plates, found {len(generated)} under {SDXL_HQ_V002}")
    for src in generated:
        rel = src.relative_to(SDXL_HQ_V002)
        dst = PUBLIC_TERRY / "v002" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)
    print(f"copied_or_verified_images={len(generated)} -> {PUBLIC_TERRY / 'v002'}", flush=True)
    return generated


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
    print(f"captions={CAPTIONS} cues={cue - 1}", flush=True)


def render_visual() -> None:
    VISUAL.parent.mkdir(parents=True, exist_ok=True)
    total_frames = int(TOTAL_SEC * 30)
    seq_dir = VISUAL.parent / "terry_visual_v002_sequence"
    seq_dir.mkdir(parents=True, exist_ok=True)

    def frame_file(frame: int) -> Path:
        return seq_dir / f"element-{frame:05d}.jpeg"

    def render_range(start: int, end: int) -> None:
        tmp_dir = seq_dir.parent / f"terry_visual_v002_sequence_tmp_{start:05d}_{end:05d}"
        if tmp_dir.exists():
            shutil.rmtree(tmp_dir)
        run([
            NPX,
            "remotion",
            "render",
            "src/terry_index.tsx",
            "TerryPremium",
            tmp_dir,
            "--frames",
            f"{start}-{end}",
            "--sequence",
            "--image-format",
            "jpeg",
            "--jpeg-quality",
            "95",
            "--concurrency",
            "1",
            "--timeout",
            "600000",
        ], f"Remotion render TerryPremium image sequence frames {start}-{end}", cwd=REMOTION)
        moved = 0
        for src in sorted(tmp_dir.glob("element-*.jpeg")):
            m = re.search(r"element-0*([0-9]+)\.jpeg$", src.name)
            if not m:
                raise RuntimeError(f"Unexpected sequence filename: {src.name}")
            dst = frame_file(int(m.group(1)))
            shutil.move(str(src), dst)
            moved += 1
        shutil.rmtree(tmp_dir)
        expected = end - start + 1
        if moved != expected:
            raise RuntimeError(f"Expected {expected} frames for {start}-{end}, moved {moved}")

    chunk = 800
    cursor = 0
    while cursor < total_frames:
        if frame_file(cursor).exists():
            cursor += 1
            continue
        end = min(total_frames - 1, cursor + chunk - 1)
        while end > cursor and frame_file(end).exists():
            end -= 1
        render_range(cursor, end)
        cursor = end + 1
    missing = [i for i in range(total_frames) if not frame_file(i).exists()]
    if missing:
        raise RuntimeError(f"Missing sequence frames: {missing[:10]} total={len(missing)}")
    joined = VISUAL.with_suffix(".sequence.mp4")
    run([
        FFMPEG,
        "-y",
        "-framerate",
        "30",
        "-start_number",
        "0",
        "-i",
        str(seq_dir / "element-%05d.jpeg"),
        "-frames:v",
        str(total_frames),
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "17",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        joined,
    ], "encode Remotion image sequence")
    joined.replace(VISUAL)


def make_music(tmp: Path) -> Path:
    tracks = [
        LIB / "music/hook/mus_20260614_hook_glass_air_bed_v2.mp3",
        LIB / "music/opening/mus_20260614_opening_measured_arpeggio_v2.mp3",
        LIB / "music/explainer_bed/mus_20260614_explainer_bed_soft_explainer_v2.mp3",
        LIB / "music/reveal/mus_20260614_reveal_verdict_at_dawn_v2.mp3",
        LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v2.mp3",
        LIB / "music/somber/mus_20260614_somber_ledger_of_ash_v2.mp3",
        LIB / "music/outro/mus_20260614_outro_last_frame_v2.mp3",
    ]
    weights = [0.075, 0.105, 0.25, 0.13, 0.18, 0.145, 0.115]
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    cur = 0.0
    for i, (track, weight) in enumerate(zip(tracks, weights)):
        if not track.exists():
            raise FileNotFoundError(track)
        dur = TOTAL_SEC * weight if i < len(tracks) - 1 else TOTAL_SEC - cur
        inputs += ["-stream_loop", "-1", "-i", str(track)]
        delay = int(cur * 1000)
        filters.append(
            f"[{i}:a]atrim=0:{dur:.3f},afade=t=in:st=0:d=1.1,"
            f"afade=t=out:st={max(dur-1.2, 0.1):.3f}:d=1.2,adelay={delay}|{delay}[m{i}]"
        )
        labels.append(f"[m{i}]")
        cur += dur
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0,volume=0.18[music]")
    out = tmp / "music.m4a"
    run([FFMPEG, "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[music]", "-t", f"{TOTAL_SEC:.3f}", "-c:a", "aac", "-b:a", "192k", out], "music bed")
    return out


def make_sfx(tmp: Path) -> Path:
    cues = [
        (0.7, "sfx_sub_drop.mp3", 0.44),
        (28.0, "sfx_soft_impact.mp3", 0.34),
        (78.0, "sfx_whoosh_medium.mp3", 0.25),
        (96.0, "sfx_ui_tick.mp3", 0.25),
        (138.5, "sfx_page_turn.mp3", 0.22),
        (174.5, "sfx_binder_lock.mp3", 0.28),
        (203.0, "sfx_stamp_seal.mp3", 0.34),
        (302.0, "sfx_low_boom.mp3", 0.31),
        (326.5, "sfx_gavel_knock.mp3", 0.36),
        (430.0, "sfx_binder_lock.mp3", 0.28),
        (491.0, "sfx_dust_swell.mp3", 0.24),
        (598.0, "sfx_riser_2s.mp3", 0.24),
        (654.0, "sfx_data_blip.mp3", 0.24),
    ]
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    for i, (t, name, gain) in enumerate(cues):
        path = LIB / "sfx" / name
        if not path.exists():
            raise FileNotFoundError(path)
        inputs += ["-i", str(path)]
        delay = int(t * 1000)
        filters.append(f"[{i}:a]volume={gain},adelay={delay}|{delay}[s{i}]")
        labels.append(f"[s{i}]")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0,volume=0.58[sfx]")
    out = tmp / "sfx.m4a"
    run([FFMPEG, "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[sfx]", "-t", f"{TOTAL_SEC:.3f}", "-c:a", "aac", "-b:a", "160k", out], "sfx bed")
    return out


def ffmpeg_subtitles_filter() -> str:
    path = CAPTIONS.resolve().as_posix().replace(":", r"\:")
    style = (
        "FontName=Trebuchet MS,FontSize=21,PrimaryColour=&H00F5F7FA,"
        "OutlineColour=&H99000000,BorderStyle=1,Outline=2,Shadow=0,MarginV=40"
    )
    return f"subtitles='{path}':force_style='{style}'"


def final_mix(music: Path, sfx: Path) -> None:
    amb = LIB / "ambience/amb_night_window.mp3"
    if not amb.exists():
        amb = LIB / "ambience/amb_institutional_drone.mp3"
    fc = (
        f"[3:a]atrim=0:{TOTAL_SEC:.3f},volume=0.035[amb];"
        "[1:a]volume=1.0[vo];[2:a]volume=0.88[mus];[4:a]volume=0.72[sfx];"
        "[vo][mus][amb][sfx]amix=inputs=4:normalize=0:duration=longest:dropout_transition=0,"
        f"loudnorm=I=-14:TP=-1.5:LRA=11:linear=false,alimiter=limit=0.93,afade=t=out:st={TOTAL_SEC-2:.3f}:d=2[a]"
    )
    OUT_MEDIA.parent.mkdir(parents=True, exist_ok=True)
    tmp_out = OUT_MEDIA.with_suffix(".tmp.mp4")
    run([
        FFMPEG,
        "-y",
        "-i",
        VISUAL,
        "-i",
        NARR_SLOW,
        "-i",
        music,
        "-stream_loop",
        "-1",
        "-i",
        amb,
        "-i",
        sfx,
        "-filter_complex",
        fc,
        "-map",
        "0:v",
        "-map",
        "[a]",
        "-vf",
        f"eq=contrast=1.04:saturation=1.03:gamma=0.99,{ffmpeg_subtitles_filter()}",
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
        "-ar",
        "48000",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        tmp_out,
    ], "final mix + captions")
    tmp_out.replace(OUT_MEDIA)


def make_video_contact_sheet() -> None:
    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    run([
        FFMPEG,
        "-y",
        "-i",
        OUT_MEDIA,
        "-vf",
        "fps=1/34,scale=320:-1,tile=5x4",
        "-frames:v",
        "1",
        "-q:v",
        "3",
        CONTACT_SHEET,
    ], "video contact sheet")


def audio_probe_tail() -> str:
    p = subprocess.run(
        [str(FFMPEG), "-hide_banner", "-i", OUT_MEDIA, "-af", "volumedetect", "-f", "null", "NUL"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return (p.stderr or "")[-2200:]


def write_rights(generated: list[Path]) -> None:
    assets: list[dict] = []
    for i, path in enumerate(generated, start=1):
        rel = path.relative_to(EPM / "05_visuals")
        assets.append({
            "asset_id": f"PD-2026-006-terry-V002-IMG-{i:03d}",
            "type": "image",
            "scene": path.parent.name,
            "description": "AI-generated local SDXL symbolic reconstruction plate for EP6 Terry v002; no real-person likeness intended; not authentic footage.",
            "file": f"artifact://episodes/{EP}/05_visuals/{rel.as_posix()}",
            "producer": "Codex orchestration + local A1111 SDXL on owner RTX4090",
            "license": "Owner-local AI generation; commercial use subject to local model/license assumptions; disclose as AI-generated symbolic reconstruction.",
            "rights_holder": "Prime Documentary",
            "content_hash": "sha256:" + sha256(path),
            "needs_verification": False,
            "ai_disclosure_required": True,
            "synthetic_content_disclosure_required": True,
            "qc_status": "accepted_for_local_review_cut",
        })
    audio_sources = [
        NARR_SLOW,
        LIB / "music/hook/mus_20260614_hook_glass_air_bed_v2.mp3",
        LIB / "music/opening/mus_20260614_opening_measured_arpeggio_v2.mp3",
        LIB / "music/explainer_bed/mus_20260614_explainer_bed_soft_explainer_v2.mp3",
        LIB / "music/reveal/mus_20260614_reveal_verdict_at_dawn_v2.mp3",
        LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v2.mp3",
        LIB / "music/somber/mus_20260614_somber_ledger_of_ash_v2.mp3",
        LIB / "music/outro/mus_20260614_outro_last_frame_v2.mp3",
        LIB / "ambience/amb_night_window.mp3",
        LIB / "sfx/sfx_sub_drop.mp3",
        LIB / "sfx/sfx_soft_impact.mp3",
        LIB / "sfx/sfx_whoosh_medium.mp3",
        LIB / "sfx/sfx_ui_tick.mp3",
        LIB / "sfx/sfx_page_turn.mp3",
        LIB / "sfx/sfx_binder_lock.mp3",
        LIB / "sfx/sfx_stamp_seal.mp3",
        LIB / "sfx/sfx_low_boom.mp3",
        LIB / "sfx/sfx_gavel_knock.mp3",
        LIB / "sfx/sfx_dust_swell.mp3",
        LIB / "sfx/sfx_riser_2s.mp3",
        LIB / "sfx/sfx_data_blip.mp3",
    ]
    for i, path in enumerate(audio_sources, start=1):
        if not path.exists():
            continue
        assets.append({
            "asset_id": f"PD-2026-006-terry-V002-AUD-{i:03d}",
            "type": "audio_source",
            "scene": "all",
            "description": f"Audio source used in v002 mix: {path.name}",
            "file": str(path),
            "producer": "Prime Documentary library reuse" if "library" in str(path) else "ElevenLabs approved narration reused locally",
            "license": "Rights-tracked reusable source",
            "rights_holder": "Prime Documentary",
            "content_hash": "sha256:" + sha256(path),
            "needs_verification": False,
        })
    assets.append({
        "asset_id": "PD-2026-006-terry-V002-RENDER-001",
        "type": "render",
        "scene": "all",
        "description": "Local v002 remake render with 180 AI symbolic reconstruction plates and Remotion motion; not uploaded or published.",
        "file": f"artifact://episodes/{EP}/08_edit/terry_final_v002.mp4",
        "producer": "Remotion + FFmpeg",
        "license": "Composite render from rights-tracked inputs",
        "rights_holder": "Prime Documentary",
        "content_hash": "sha256:" + sha256(OUT_MEDIA),
        "needs_verification": False,
        "ai_disclosure_required": True,
        "synthetic_content_disclosure_required": True,
    })
    RIGHTS.parent.mkdir(parents=True, exist_ok=True)
    RIGHTS.write_text(json.dumps({
        "schema_version": "rights_manifest_v1",
        "episode_id": EP,
        "revision": "v002",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "local_remake_ready_no_upload",
        "notes": "All v002 visuals are symbolic reconstruction; YouTube synthetic-content disclosure required before any publish/update. No upload performed.",
        "assets": assets,
        "verification_required": [],
    }, indent=2, ensure_ascii=False) + "\n", "utf-8")


def write_package_and_qc(narr_dur: float, generated: list[Path]) -> None:
    final_dur = duration(OUT_MEDIA)
    q = {
        "schema_version": "final_qc_v1",
        "episode_id": EP,
        "revision": "v002",
        "render": f"artifact://episodes/{EP}/08_edit/terry_final_v002.mp4",
        "render_actual_path": str(OUT_MEDIA),
        "sha256": sha256(OUT_MEDIA),
        "duration_seconds": round(final_dur, 3),
        "target_duration_seconds": TOTAL_SEC,
        "video": "Remotion TerryPremium v002, 180 local SDXL symbolic hero plates, crossfades, pan/zoom, light motion",
        "audio": {
            "narration": "Approved ElevenLabs master reused and slowed to fit timeline",
            "narration_master": f"artifact://episodes/{EP}/06_voice/master/vc_master_v001.mp3",
            "narration_slowed": f"artifact://episodes/{EP}/06_voice/master/{NARR_SLOW.name}",
            "narration_slowed_seconds": round(narr_dur, 3),
            "music": "Prime Documentary reusable library multi-bed mix",
            "sfx": "Prime Documentary reusable library spot SFX",
        },
        "captions": f"artifact://episodes/{EP}/08_edit/captions.final.v002.srt",
        "contact_sheet": f"artifact://episodes/{EP}/08_edit/renders/final.v002.contact_sheet.jpg",
        "image_plate_count": len(generated),
        "synthetic_content_disclosure_required": True,
        "contains_ai_symbolic_reconstruction": True,
        "upload_performed": False,
        "publish_performed": False,
        "qc_status": "pass_with_warnings",
        "warnings": [
            "No upload or publish was performed.",
            "Caption timing is derived from ElevenLabs chunk timings and uniform slowdown, not Whisper word-level forced alignment.",
            "Synthetic-content disclosure is required because symbolic AI reconstructions are used.",
        ],
        "audio_probe_tail": audio_probe_tail(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    QC_REPO.parent.mkdir(parents=True, exist_ok=True)
    QC_REPO.write_text(json.dumps(q, indent=2, ensure_ascii=False) + "\n", "utf-8")
    DELIVERY.parent.mkdir(parents=True, exist_ok=True)
    DELIVERY.write_text(json.dumps({
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v002",
        "status": "local_remake_ready_no_upload",
        "render": q["render"],
        "render_actual_path": q["render_actual_path"],
        "video_sha256": q["sha256"],
        "duration_seconds": q["duration_seconds"],
        "rights_manifest": f"artifact://episodes/{EP}/09_package/rights_manifest.v002.json",
        "qc_report": f"artifact://episodes/{EP}/08_edit/renders/final.v002.qc.json",
        "contact_sheet": q["contact_sheet"],
        "image_plate_count": len(generated),
        "title_current": "A Cop Can Search You Without a Warrant - Here's the Catch",
        "synthetic_content_disclosure_required": True,
        "contains_ai_symbolic_reconstruction": True,
        "upload_performed": False,
        "publish_performed": False,
        "created_at": q["created_at"],
    }, indent=2, ensure_ascii=False) + "\n", "utf-8")
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    EVENTS.open("a", encoding="utf-8").write(json.dumps({
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": "final_v002_180_hero_shots_rendered",
        "episode_id": EP,
        "render": str(OUT_MEDIA),
        "sha256": q["sha256"],
        "image_plate_count": len(generated),
        "upload_performed": False,
        "publish_performed": False,
    }, ensure_ascii=False) + "\n")
    print(json.dumps({"render": str(OUT_MEDIA), "sha256": q["sha256"], "duration_seconds": q["duration_seconds"]}, indent=2), flush=True)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if not NARR_MASTER.exists():
        raise FileNotFoundError(NARR_MASTER)
    generated = prepare_public_images()
    narr_dur = slow_narration()
    write_captions()
    render_visual()
    with tempfile.TemporaryDirectory(prefix="pd_terry_v002_") as td:
        tmp = Path(td)
        music = make_music(tmp)
        sfx = make_sfx(tmp)
        final_mix(music, sfx)
    make_video_contact_sheet()
    write_rights(generated)
    write_package_and_qc(narr_dur, generated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
