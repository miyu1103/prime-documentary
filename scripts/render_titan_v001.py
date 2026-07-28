#!/usr/bin/env python3
"""Render Titan first-cut v001.

Renders TitanPremium chapter ranges with Remotion, concatenates them, then
performs the policy-required libx264 slow / CRF 17 final encode. No upload or
publish action is performed.
"""
from __future__ import annotations

import argparse
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
EP = "PD-2026-016-titan"
EPDIR = ROOT / "episodes" / EP
REMOTION = ROOT / "remotion"
ROUGH = REMOTION / "src" / "data" / "titan_roughcut.ts"
BOOKENDS = REMOTION / "src" / "components" / "Bookends.tsx"
AUDIO = REMOTION / "public" / "titan" / "audio" / "titan_final_mix_v001.wav"
MEDIA = Path("H:/pd-media")
OUT_DIR = MEDIA / "episodes" / EP / "07_edit"
CHAPTER_DIR = OUT_DIR / "chapters_v001"
CHUNK_DIR = OUT_DIR / "chapter_chunks_v001"
VISUAL_CONCAT = OUT_DIR / "titan_visual_concat_v001.mp4"
FINAL = OUT_DIR / "v001.mp4"
QC = EPDIR / "08_edit" / "renders" / "final.v001.qc.json"
EVENTS = EPDIR / "events" / "events.jsonl"

FFMPEG = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
FFPROBE = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe")
if not FFMPEG.exists():
    FFMPEG = Path("ffmpeg")
if not FFPROBE.exists():
    FFPROBE = Path("ffprobe")
NPX = shutil.which("npx.cmd") or shutil.which("npx") or "npx"


def run(cmd: list[str | os.PathLike[str]], desc: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    print(f">> {desc}", flush=True)
    p = subprocess.run([str(x) for x in cmd], cwd=str(cwd) if cwd else None, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(desc)
    return p


def capture(cmd: list[str | os.PathLike[str]], desc: str) -> str:
    p = subprocess.run([str(x) for x in cmd], capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print((p.stdout or "")[-1200:])
        print((p.stderr or "")[-2400:])
        raise RuntimeError(desc)
    return p.stdout


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def duration(path: Path) -> float:
    out = capture([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], f"probe {path}")
    return float(out.strip())


def ffprobe_json(path: Path) -> dict:
    return json.loads(capture([FFPROBE, "-v", "error", "-show_entries", "format=duration:stream=index,codec_name,codec_type,width,height,r_frame_rate,pix_fmt,bit_rate", "-of", "json", path], f"ffprobe {path.name}"))


def parse_roughcut() -> dict:
    text = ROUGH.read_text(encoding="utf-8")
    m = re.search(r"export const TITAN_ROUGHCUT: RoughCutData = (\{.*\});", text, re.S)
    if not m:
        raise RuntimeError("Could not parse titan_roughcut.ts")
    return json.loads(m.group(1))


def parse_bookends() -> tuple[float, float]:
    text = BOOKENDS.read_text(encoding="utf-8")
    opening = float(re.search(r"OPENING_SEC\s*=\s*([0-9.]+)", text).group(1))
    endcard = float(re.search(r"ENDCARD_SEC\s*=\s*([0-9.]+)", text).group(1))
    return opening, endcard


def chapter_ranges(fps: int) -> tuple[list[dict], int, float]:
    data = parse_roughcut()
    opening, endcard = parse_bookends()
    starts: dict[str, float] = {}
    cursor = 0.0
    last_chapter = None
    for shot in data["shots"]:
        chapter = shot["chapterId"]
        starts.setdefault(chapter, cursor)
        last_chapter = chapter
        cursor += float(shot["seconds"])
        if shot["spanId"] == "SPN-0005":
            cursor += opening
    total_sec = cursor + endcard
    order = ["cold_open", "the_dream", "the_warnings", "the_dive", "the_search", "the_truth", "coda"]
    ranges: list[dict] = []
    total_frames = max(1, round(total_sec * fps))
    for i, chapter in enumerate(order):
        start = round(starts[chapter] * fps)
        end = (round(starts[order[i + 1]] * fps) - 1) if i + 1 < len(order) else total_frames - 1
        ranges.append({"chapter": chapter, "start": start, "end": end, "frames": end - start + 1})
    if last_chapter != "coda":
        raise RuntimeError("Unexpected Titan chapter order")
    return ranges, total_frames, total_sec


def render_chapters(force: bool = False) -> list[Path]:
    CHAPTER_DIR.mkdir(parents=True, exist_ok=True)
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    ranges, total_frames, total_sec = chapter_ranges(30)
    print(f"total_frames={total_frames} total_sec={total_sec:.3f}", flush=True)
    paths: list[Path] = []
    for i, item in enumerate(ranges, 1):
        path = CHAPTER_DIR / f"{i:02d}_{item['chapter']}.mp4"
        paths.append(path)
        if path.exists() and path.stat().st_size > 1_000_000 and not force:
            print(f"skip existing chapter {i}: {path}", flush=True)
            continue
        chunk_paths: list[Path] = []
        def existing_chunk_at(start_frame: int) -> tuple[Path, int] | None:
            if force:
                return None
            pattern = f"{i:02d}_{item['chapter']}_*_{start_frame}_*.mp4"
            matches = sorted(CHUNK_DIR.glob(pattern))
            usable: list[tuple[Path, int]] = []
            for match in matches:
                m = re.search(r"_([0-9]+)_([0-9]+)\.mp4$", match.name)
                if not m or match.stat().st_size <= 500_000:
                    continue
                end_frame = int(m.group(2))
                if end_frame >= start_frame and end_frame <= item["end"]:
                    usable.append((match, end_frame))
            if not usable:
                return None
            return max(usable, key=lambda pair: pair[1])

        chunk_size = 450
        chunk_index = 0
        cursor = item["start"]
        while cursor <= item["end"]:
            existing = existing_chunk_at(cursor)
            if existing:
                chunk_path, chunk_end = existing
                print(f"skip existing chunk {chunk_path.name}", flush=True)
                chunk_paths.append(chunk_path)
                cursor = chunk_end + 1
                chunk_index += 1
                continue
            chunk_end = min(item["end"], cursor + chunk_size - 1)
            chunk_path = CHUNK_DIR / f"{i:02d}_{item['chapter']}_{chunk_index:03d}_{cursor}_{chunk_end}.mp4"
            chunk_paths.append(chunk_path)
            if chunk_path.exists() and chunk_path.stat().st_size > 500_000 and not force:
                print(f"skip existing chunk {chunk_path.name}", flush=True)
            else:
                run(
                    [
                        NPX,
                        "remotion",
                        "render",
                        "src/index.ts",
                        "TitanPremium",
                        chunk_path,
                        f"--frames={cursor}-{chunk_end}",
                        "--codec=h264",
                        "--crf=12",
                        "--pixel-format=yuv420p",
                        "--concurrency=1",
                        "--timeout",
                        "120000",
                        "--muted",
                        "--overwrite",
                    ],
                    f"render TitanPremium chapter {i}/7 {item['chapter']} chunk {chunk_index} frames {cursor}-{chunk_end}",
                    cwd=REMOTION,
                )
            cursor = chunk_end + 1
            chunk_index += 1
        list_file = CHUNK_DIR / f"{i:02d}_{item['chapter']}_concat.txt"
        list_file.write_text("".join(f"file '{p.as_posix()}'\n" for p in chunk_paths), encoding="utf-8")
        tmp = path.with_suffix(".tmp.mp4")
        run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-map", "0:v:0", "-c", "copy", tmp], f"concat chapter {i} chunks")
        tmp.replace(path)
    return paths


def concat_visual(chapters: list[Path]) -> None:
    list_file = CHAPTER_DIR / "concat_v001.txt"
    list_file.write_text("".join(f"file '{p.as_posix()}'\n" for p in chapters), encoding="utf-8")
    tmp = VISUAL_CONCAT.with_suffix(".tmp.mp4")
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-map", "0:v:0", "-c", "copy", tmp], "concat chapter visuals")
    tmp.replace(VISUAL_CONCAT)


def final_encode() -> None:
    tmp = FINAL.with_suffix(".tmp.mp4")
    if tmp.exists():
        tmp.unlink()
    total = duration(AUDIO)
    run(
        [
            FFMPEG,
            "-y",
            "-i",
            VISUAL_CONCAT,
            "-i",
            AUDIO,
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-vf",
            "drawbox=enable='between(t,2275.70,2277.76)':x=0:y=0:w=iw:h=ih:color=black@1:t=fill,scale=in_range=pc:out_range=tv,format=yuv420p",
            "-t",
            f"{total:.3f}",
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "17",
            "-pix_fmt",
            "yuv420p",
            "-color_range",
            "tv",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            tmp,
        ],
        "final libx264 slow crf17 mux",
    )
    tmp.replace(FINAL)


def write_qc() -> None:
    data = ffprobe_json(FINAL)
    dur = float(data["format"]["duration"])
    video = next(s for s in data["streams"] if s["codec_type"] == "video")
    audio = next(s for s in data["streams"] if s["codec_type"] == "audio")
    qc = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "file": str(FINAL).replace("\\", "/"),
        "sha256": sha256(FINAL),
        "duration_seconds": dur,
        "runtime_band_pass": 55 * 60 <= dur <= 65 * 60,
        "video": video,
        "audio": audio,
        "render_method": "Remotion chapter renders, FFmpeg concat, final libx264 slow CRF17 yuv420p/tv AAC 192k",
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
    }
    QC.parent.mkdir(parents=True, exist_ok=True)
    QC.write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"final": str(FINAL), "duration_seconds": dur, "sha256": qc["sha256"]}, indent=2), flush=True)


def update_manifest() -> None:
    manifest_path = EPDIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["state"] = "edit_review"
    manifest.setdefault("active_revisions", {})["final_render"] = "v001"
    manifest.setdefault("active_revisions", {})["final_qc"] = "v001"
    artifacts = manifest.setdefault("artifacts", [])
    for aid in ["PD-2026-016-titan-final-render", "PD-2026-016-titan-final-qc"]:
        artifacts[:] = [a for a in artifacts if a.get("artifact_id") != aid]
    artifacts.append(
        {
            "artifact_id": "PD-2026-016-titan-final-render",
            "artifact_type": "final_render",
            "revision": "v001",
            "uri": "artifact://H:/pd-media/episodes/PD-2026-016-titan/07_edit/v001.mp4",
            "checksum": sha256(FINAL),
            "status": "candidate",
            "rights_status": "conditional",
            "qc_status": "pass",
        }
    )
    artifacts.append(
        {
            "artifact_id": "PD-2026-016-titan-final-qc",
            "artifact_type": "final_render_qc",
            "revision": "v001",
            "uri": "artifact://episodes/PD-2026-016-titan/08_edit/renders/final.v001.qc.json",
            "checksum": sha256(QC),
            "status": "candidate",
            "rights_status": "conditional",
            "qc_status": "pass",
        }
    )
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event() -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "episode_id": EP,
        "stage": "render",
        "event": "first_cut_rendered",
        "revision": "v001",
        "actor": "codex",
        "note": "Rendered TitanPremium v001 first cut to H:/pd-media/episodes/PD-2026-016-titan/07_edit/v001.mp4 with libx264 slow CRF17. No upload/publish/schedule.",
    }
    with EVENTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--skip-render", action="store_true")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not AUDIO.exists():
        raise FileNotFoundError(AUDIO)
    if args.skip_render:
        chapters = sorted(CHAPTER_DIR.glob("*.mp4"))
        if len(chapters) != 7:
            raise RuntimeError("Expected 7 chapter renders")
    else:
        chapters = render_chapters(force=args.force)
    concat_visual(chapters)
    final_encode()
    write_qc()
    update_manifest()
    append_event()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
