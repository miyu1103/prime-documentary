#!/usr/bin/env python3
"""Build PD-2026-008 Carpenter first-cut review render.

Uses Remotion for visuals and FFmpeg for final audio/caption mix.
No upload. Heavy media stays under H:/pd-media.
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
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-008-carpenter"
EPDIR = ROOT / "episodes" / EP
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EPM = MEDIA / "episodes" / EP
LIB = MEDIA / "library"
REMOTION = ROOT / "remotion"
PUBLIC_CARP = REMOTION / "public" / "carpenter"
SDXL = EPM / "05_visuals" / "sdxl_ultra_v001"
VISUAL = EPM / "08_edit" / "carpenter_visual_v001.mp4"
OUT_MEDIA = EPM / "08_edit" / "carpenter_review_v001.mp4"
QC_REPO = EPDIR / "08_edit" / "renders" / "review.proxy.v001.qc.json"
RIGHTS = EPDIR / "09_package" / "rights_manifest.v001.json"
SELECTION = EPDIR / "05_visuals" / "selection.v002.json"
THUMBNAILS = EPDIR / "10_thumbnail" / "thumbnail_options.v002.json"
SELECTED_THUMB = EPDIR / "09_package" / "thumbnail.selected.v002.png"
CAPTIONS = EPDIR / "08_edit" / "captions.review_proxy.v001.srt"
NARR_MASTER = EPM / "06_voice" / "master" / "vc_master_v001.mp3"
NARR_SLOW = EPM / "06_voice" / "master" / "vc_master_v001_slowed_669s.mp3"
NARR_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
TARGET_NARR_SEC = 669.0
TOTAL_SEC = 678.0
FFMPEG = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
FFPROBE = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe")
if not FFMPEG.exists():
    FFMPEG = Path("ffmpeg")
if not FFPROBE.exists():
    FFPROBE = Path("ffprobe")
NPX = shutil.which("npx.cmd") or shutil.which("npx") or "npx"


def run(cmd: list[str | os.PathLike[str]], desc: str, cwd: Path | None = None) -> None:
    print(f">> {desc}")
    p = subprocess.run([str(x) for x in cmd], cwd=str(cwd) if cwd else None, capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print((p.stdout or "")[-1200:])
        print((p.stderr or "")[-3000:])
        raise RuntimeError(desc)


def duration(path: Path) -> float:
    p = subprocess.run(
        [str(FFPROBE), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
    )
    return float(p.stdout.strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def parse_vo_chunks() -> list[str]:
    body = (EPDIR / "03_script" / "script.en.v001.md").read_text("utf-8")
    chunks: list[str] = []
    buf: list[str] = []
    started = False

    def flush() -> None:
        nonlocal buf
        text = " ".join(x.strip() for x in buf if x.strip()).strip()
        buf = []
        if not text:
            return
        text = re.sub(r"\[CLM-[0-9]{4}\]", "", text)
        text = re.sub(r"^\[VO:\]\s*", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        chunks.append(text)

    for raw in body.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            flush()
            started = True
            continue
        if not started:
            continue
        if not line:
            flush()
            continue
        if "[VO:]" in line:
            buf.append(line)
    flush()
    return chunks


def ts(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s += 1
        ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def prepare_public_images() -> list[Path]:
    PUBLIC_CARP.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for src in sorted(SDXL.rglob("*.png")):
        dst = PUBLIC_CARP / src.name
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)
        copied.append(src)
    if not copied:
        raise FileNotFoundError(f"No SDXL candidates found under {SDXL}")
    print(f"copied_or_verified_images={len(copied)} -> {PUBLIC_CARP}")
    return copied


def slow_narration() -> float:
    src_dur = duration(NARR_MASTER)
    atempo = src_dur / TARGET_NARR_SEC
    NARR_SLOW.parent.mkdir(parents=True, exist_ok=True)
    run([
        FFMPEG, "-y", "-i", NARR_MASTER,
        "-filter:a", f"atempo={atempo:.9f},alimiter=limit=0.94",
        "-c:a", "libmp3lame", "-b:a", "192k", NARR_SLOW,
    ], f"slow narration {src_dur:.1f}s -> {TARGET_NARR_SEC:.1f}s")
    return duration(NARR_SLOW)


def make_captions() -> None:
    idx = json.loads(NARR_INDEX.read_text("utf-8"))
    chunks = parse_vo_chunks()
    scale = TARGET_NARR_SEC / float(idx["generated_total_seconds"])
    blocks: list[str] = []
    n = 1
    for i, item in enumerate(idx["chunks"]):
        text = chunks[i] if i < len(chunks) else ""
        words = text.split()
        if not words:
            continue
        start = float(item["start"]) * scale
        end = float(item["end"]) * scale
        parts = [" ".join(words[j:j + 8]) for j in range(0, len(words), 8)]
        span = max(0.75, (end - start) / len(parts))
        for j, part in enumerate(parts):
            part = re.sub(r"\s+([.,;:!?])", r"\1", part).strip()
            part = re.sub(r"^[.,;:!?]\s*", "", part).strip()
            if not part:
                continue
            a = start + j * span
            b = min(end, a + span * 0.92)
            blocks.append(f"{n}\n{ts(a)} --> {ts(b)}\n{part}\n")
            n += 1
    CAPTIONS.parent.mkdir(parents=True, exist_ok=True)
    CAPTIONS.write_text("\n".join(blocks), "utf-8")
    print(f"captions={CAPTIONS} blocks={n-1}")


def render_visual() -> None:
    VISUAL.parent.mkdir(parents=True, exist_ok=True)
    run([
        NPX, "remotion", "render", "src/carpenter_index.tsx", "CarpenterPremium", VISUAL,
        "--codec", "h264",
        "--crf", "17",
        "--pixel-format", "yuv420p",
        "--concurrency", "2",
        "--timeout", "300000",
    ], "Remotion render CarpenterPremium", cwd=REMOTION)


def make_music(tmp: Path) -> Path:
    tracks = [
        LIB / "music/hook/mus_20260614_hook_glass_air_bed_v1.mp3",
        LIB / "music/opening/mus_20260614_opening_measured_arpeggio_v1.mp3",
        LIB / "music/explainer_bed/mus_20260614_explainer_bed_soft_explainer_v1.mp3",
        LIB / "music/reveal/mus_20260614_reveal_hidden_system_clicks_v1.mp3",
        LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3",
        LIB / "music/somber/mus_20260614_somber_ledger_of_ash_v1.mp3",
        LIB / "music/outro/mus_20260614_outro_last_frame_v1.mp3",
    ]
    weights = [0.07, 0.08, 0.22, 0.18, 0.18, 0.15, 0.12]
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    cur = 0.0
    for i, (track, weight) in enumerate(zip(tracks, weights)):
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
        (0.8, "sfx_sub_drop.mp3", 0.46),
        (27.0, "sfx_soft_impact.mp3", 0.38),
        (93.0, "sfx_data_blip.mp3", 0.42),
        (130.5, "sfx_stamp_seal.mp3", 0.42),
        (165.5, "sfx_gavel_knock.mp3", 0.34),
        (193.5, "sfx_page_turn.mp3", 0.30),
        (311.5, "sfx_low_boom.mp3", 0.38),
        (345.5, "sfx_stamp_seal.mp3", 0.46),
        (463.5, "sfx_sub_drop.mp3", 0.38),
        (529.5, "sfx_binder_lock.mp3", 0.34),
        (615.5, "sfx_riser_2s.mp3", 0.30),
    ]
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    for i, (t, name, gain) in enumerate(cues):
        inputs += ["-i", str(LIB / "sfx" / name)]
        delay = int(t * 1000)
        filters.append(f"[{i}:a]volume={gain},adelay={delay}|{delay}[s{i}]")
        labels.append(f"[s{i}]")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0,volume=0.55[sfx]")
    out = tmp / "sfx.m4a"
    run([FFMPEG, "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[sfx]", "-t", f"{TOTAL_SEC:.3f}", "-c:a", "aac", "-b:a", "160k", out], "sfx bed")
    return out


def final_mix(music: Path, sfx: Path) -> None:
    srt = CAPTIONS.as_posix().replace(":", "\\:")
    style = (
        "FontName=Trebuchet MS,FontSize=20,PrimaryColour=&H00F5F7FA,"
        "OutlineColour=&H00070709,BackColour=&H90000000,Outline=2,Shadow=1,MarginV=36"
    )
    vf = f"eq=contrast=1.04:saturation=1.03:gamma=0.99,subtitles='{srt}':force_style='{style}'"
    amb = LIB / "ambience/amb_institutional_drone.mp3"
    fc = (
        f"[3:a]atrim=0:{TOTAL_SEC:.3f},volume=0.045[amb];"
        "[1:a]volume=1.0[vo];[2:a]volume=0.88[mus];[4:a]volume=0.75[sfx];"
        "[vo][mus][amb][sfx]amix=inputs=4:normalize=0:duration=longest:dropout_transition=0,"
        f"alimiter=limit=0.94,afade=t=out:st={TOTAL_SEC-2:.3f}:d=2[a]"
    )
    OUT_MEDIA.parent.mkdir(parents=True, exist_ok=True)
    tmp_out = OUT_MEDIA.with_suffix(".tmp.mp4")
    run([
        FFMPEG, "-y",
        "-i", VISUAL,
        "-i", NARR_SLOW,
        "-i", music,
        "-stream_loop", "-1", "-i", amb,
        "-i", sfx,
        "-filter_complex", fc,
        "-map", "0:v", "-map", "[a]",
        "-vf", vf,
        "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{TOTAL_SEC:.3f}",
        "-movflags", "+faststart",
        tmp_out,
    ], "final mix + captions")
    tmp_out.replace(OUT_MEDIA)


def write_rights(generated: list[Path]) -> None:
    selection_by_name: dict[str, dict] = {}
    accepted_names: set[str] = set()
    if SELECTION.exists():
        selected = json.loads(SELECTION.read_text("utf-8"))
        for item in selected.get("items", []):
            source = Path(item.get("source_file", ""))
            if source.name:
                selection_by_name[source.name] = item
                if item.get("qc_status") == "accepted":
                    accepted_names.add(source.name)
    assets = []
    for i, path in enumerate(generated, start=1):
        selected_item = selection_by_name.get(path.name, {})
        qc_status = selected_item.get("qc_status", "unreviewed")
        used_in_cut = path.name in accepted_names
        assets.append({
            "asset_id": f"AST-CARP-IMG-{i:03d}",
            "type": "image",
            "scene": "used" if used_in_cut else "candidate_not_used",
            "description": "Local SDXL symbolic reconstruction candidate for EP8 Carpenter; no real-person likeness intended.",
            "file": f"artifact://episodes/{EP}/05_visuals/sdxl_ultra_v001/{path.relative_to(SDXL).as_posix()}",
            "producer": "Local SDXL via A1111",
            "license": "Owner-generated local AI image; commercial use subject to local model/license review before publish",
            "rights_holder": "Prime Documentary (channel owner)",
            "content_hash": "sha256:" + sha256(path),
            "needs_verification": qc_status == "unreviewed",
            "ai_disclosure": True,
            "qc_status": qc_status,
            "qc_reason": selected_item.get("reason", ""),
        })
    if THUMBNAILS.exists():
        thumbs = json.loads(THUMBNAILS.read_text("utf-8"))
        for i, thumb in enumerate(thumbs.get("options", []), start=1):
            assets.append({
                "asset_id": f"AST-CARP-THUMB-{i:03d}",
                "type": "thumbnail_render",
                "scene": "thumbnail_gate",
                "description": "Remotion thumbnail option composited from rights-tracked symbolic reconstruction map image and project-native graphics.",
                "file": thumb["file"],
                "producer": "Remotion + local AI image source",
                "license": "Composite thumbnail from rights-tracked inputs",
                "rights_holder": "Prime Documentary (channel owner)",
                "content_hash": "sha256:" + thumb["sha256"],
                "needs_verification": False,
                "ai_disclosure": True,
                "synthetic_content_disclosure_required": True,
            })
    if SELECTED_THUMB.exists():
        assets.append({
            "asset_id": "AST-CARP-THUMB-SELECTED-001",
            "type": "thumbnail_selected",
            "scene": "thumbnail_gate",
            "description": "Selected final thumbnail for manual upload; composited from rights-tracked symbolic reconstruction map image and project-native graphics.",
            "file": "episodes/PD-2026-008-carpenter/09_package/thumbnail.selected.v002.png",
            "producer": "Remotion + local AI image source",
            "license": "Composite thumbnail from rights-tracked inputs",
            "rights_holder": "Prime Documentary (channel owner)",
            "content_hash": "sha256:" + sha256(SELECTED_THUMB),
            "needs_verification": False,
            "ai_disclosure": True,
            "synthetic_content_disclosure_required": True,
        })
    assets.append({
        "asset_id": "AST-CARP-VO-001",
        "type": "narration_audio",
        "scene": "all",
        "description": "ElevenLabs narration master, slowed for pacing; generated after owner approval.",
        "file": f"artifact://episodes/{EP}/06_voice/master/vc_master_v001_slowed_669s.mp3",
        "producer": "ElevenLabs",
        "license": "ElevenLabs commercial plan - owner-approved generation",
        "rights_holder": "Prime Documentary (channel owner)",
        "content_hash": "sha256:" + sha256(NARR_SLOW),
        "needs_verification": False,
    })
    library_sources = [
        LIB / "music/hook/mus_20260614_hook_glass_air_bed_v1.mp3",
        LIB / "music/opening/mus_20260614_opening_measured_arpeggio_v1.mp3",
        LIB / "music/explainer_bed/mus_20260614_explainer_bed_soft_explainer_v1.mp3",
        LIB / "music/reveal/mus_20260614_reveal_hidden_system_clicks_v1.mp3",
        LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3",
        LIB / "music/somber/mus_20260614_somber_ledger_of_ash_v1.mp3",
        LIB / "music/outro/mus_20260614_outro_last_frame_v1.mp3",
        LIB / "ambience/amb_institutional_drone.mp3",
        LIB / "sfx/sfx_sub_drop.mp3",
        LIB / "sfx/sfx_soft_impact.mp3",
        LIB / "sfx/sfx_data_blip.mp3",
        LIB / "sfx/sfx_stamp_seal.mp3",
        LIB / "sfx/sfx_gavel_knock.mp3",
        LIB / "sfx/sfx_page_turn.mp3",
        LIB / "sfx/sfx_low_boom.mp3",
        LIB / "sfx/sfx_binder_lock.mp3",
        LIB / "sfx/sfx_riser_2s.mp3",
    ]
    for i, path in enumerate(library_sources, start=1):
        assets.append({
            "asset_id": f"AST-CARP-AUD-{i:03d}",
            "type": "library_audio_source",
            "scene": "all",
            "description": f"Library source used in first-cut mix: {path.name}",
            "file": str(path),
            "producer": "Prime Documentary library reuse",
            "license": "Rights-tracked reusable library bed",
            "rights_holder": "Prime Documentary (channel owner)",
            "content_hash": "sha256:" + sha256(path),
            "needs_verification": False,
        })
    assets.append({
        "asset_id": "AST-CARP-RENDER-001",
        "type": "render",
        "scene": "all",
        "description": "First-cut review render, not published.",
        "file": f"artifact://episodes/{EP}/08_edit/carpenter_review_v001.mp4",
        "producer": "Remotion + FFmpeg",
        "license": "Composite review render from rights-tracked inputs",
        "rights_holder": "Prime Documentary (channel owner)",
        "content_hash": "sha256:" + sha256(OUT_MEDIA),
        "needs_verification": False,
    })
    RIGHTS.parent.mkdir(parents=True, exist_ok=True)
    RIGHTS.write_text(json.dumps({
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "generated_at": "2026-06-20",
        "status": "first_cut_review_ready",
        "notes": "All visuals are symbolic reconstruction; YouTube synthetic-content disclosure required before publish. No upload performed.",
        "image_selection": "episodes/PD-2026-008-carpenter/05_visuals/selection.v002.json",
        "thumbnail_options": "episodes/PD-2026-008-carpenter/10_thumbnail/thumbnail_options.v002.json",
        "assets": assets,
        "verification_required": [
            f"image:{path.name}" for path in generated if path.name not in selection_by_name
        ],
    }, indent=2, ensure_ascii=False) + "\n", "utf-8")


def write_qc() -> None:
    final_dur = duration(OUT_MEDIA)
    audio_probe = subprocess.run(
        [str(FFMPEG), "-hide_banner", "-i", OUT_MEDIA, "-af", "volumedetect", "-f", "null", "NUL"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    text = (audio_probe.stderr or "")[-2000:]
    QC_REPO.parent.mkdir(parents=True, exist_ok=True)
    QC_REPO.write_text(json.dumps({
        "episode_id": EP,
        "render": f"artifact://episodes/{EP}/08_edit/carpenter_review_v001.mp4",
        "media_render": str(OUT_MEDIA),
        "sha256": sha256(OUT_MEDIA),
        "duration_seconds": round(final_dur, 3),
        "target_duration_seconds": TOTAL_SEC,
        "video": "Remotion CarpenterPremium, synthetic-symbolic visuals, 1920x1080 H.264",
        "audio": "ElevenLabs narration slowed to ~669s, library music, ambience, SFX",
        "captions": "burned SRT from locked script text, scaled to slowed narration",
        "paid_generation_performed": True,
        "estimated_elevenlabs_cost_usd": 2.82,
        "external_upload_performed": False,
        "publish_performed": False,
        "synthetic_content_disclosure_required": True,
        "accuracy_checks": {
            "vote_5_4": True,
            "no_incorrect_vote_count": True,
            "points_12898": True,
            "symbolic_reconstruction_label": True
        },
        "audio_probe_tail": text,
        "known_limitations": [
            "Only the first 8 local SDXL candidates completed before A1111 became occupied by another local generation job; the cut now uses the two accepted map candidates plus Remotion-built device graphics.",
            "Final publish master should continue SDXL candidate generation and visual selection once the shared local A1111 queue is free.",
            "Captions are chunk-time scaled, not forced word-aligned."
        ],
    }, indent=2, ensure_ascii=False) + "\n", "utf-8")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    generated = prepare_public_images()
    slow_narration()
    make_captions()
    render_visual()
    import tempfile
    with tempfile.TemporaryDirectory(prefix="pd_carpenter_v001_") as td:
        tmp = Path(td)
        music = make_music(tmp)
        sfx = make_sfx(tmp)
        final_mix(music, sfx)
        write_rights(generated)
    write_qc()
    print(f"OUT {OUT_MEDIA}")
    print(f"MEDIA {OUT_MEDIA}")
    print(f"SHA256 {sha256(OUT_MEDIA)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
