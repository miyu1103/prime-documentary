#!/usr/bin/env python3
"""Render OneCoin v008 editorial cut.

This render intentionally follows the user's editorial override: shorter runtime,
natural-speed narration, faster hook, denser visuals. It performs no upload,
publish, scheduling, or external API calls.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-017-onecoin"
EPDIR = ROOT / "episodes" / EP
REMOTION = ROOT / "remotion"
ROUGH = REMOTION / "src" / "data" / "onecoin_roughcut.ts"
BOOKENDS = REMOTION / "src" / "components" / "Bookends.tsx"
AUDIO = REMOTION / "public" / "onecoin" / "audio" / "onecoin_final_mix_v008.wav"
MEDIA = Path("E:/pd-media")
OUT_DIR = MEDIA / "episodes" / EP / "07_edit"
CHAPTER_DIR = OUT_DIR / "chapters_v008"
CHUNK_DIR = OUT_DIR / "chapter_chunks_v008"
VISUAL_CONCAT = OUT_DIR / "onecoin_visual_concat_v008.mp4"
FINAL = OUT_DIR / "v008.mp4"
QC = EPDIR / "08_edit" / "renders" / "final.v008.qc.json"
EVENTS = EPDIR / "events" / "events.jsonl"
LOG = OUT_DIR / "render_onecoin_v008.log"
SILENCE_SPAN_ID = "SPN-0043"
EDITORIAL_OPENING_AFTER_SPAN_ID = "SPN-0003"

FFMPEG = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
FFPROBE = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe")
if not FFMPEG.exists():
    FFMPEG = Path("ffmpeg")
if not FFPROBE.exists():
    FFPROBE = Path("ffprobe")
NPX = shutil.which("npx.cmd") or shutil.which("npx") or "npx"


def run(cmd: list[str | os.PathLike[str]], desc: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    print(f">> {desc}", flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8", errors="replace") as log:
        log.write(f"\n\n## {datetime.now(timezone.utc).isoformat()} {desc}\n")
        log.write(" ".join(str(x) for x in cmd) + "\n")
        p = subprocess.run(
            [str(x) for x in cmd],
            cwd=str(cwd) if cwd else None,
            encoding="utf-8",
            errors="replace",
            stdout=log,
            stderr=subprocess.STDOUT,
        )
    if p.returncode != 0:
        print(f"failed; see {LOG}", flush=True)
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
    return json.loads(
        capture(
            [
                FFPROBE,
                "-v",
                "error",
                "-show_entries",
                "format=duration:stream=index,codec_name,codec_type,width,height,r_frame_rate,pix_fmt,bit_rate",
                "-of",
                "json",
                path,
            ],
            f"ffprobe {path.name}",
        )
    )


def parse_roughcut() -> dict:
    text = ROUGH.read_text(encoding="utf-8")
    m = re.search(r"export const ONECOIN_ROUGHCUT: RoughCutData = (\{.*\});", text, re.S)
    if not m:
        raise RuntimeError("Could not parse onecoin_roughcut.ts")
    return json.loads(m.group(1))


def parse_bookends() -> tuple[float, float]:
    text = BOOKENDS.read_text(encoding="utf-8")
    opening = float(re.search(r"OPENING_SEC\s*=\s*([0-9.]+)", text).group(1))
    endcard = float(re.search(r"ENDCARD_SEC\s*=\s*([0-9.]+)", text).group(1))
    return opening, endcard


def scheduled_rows() -> tuple[list[dict], float]:
    data = parse_roughcut()
    if data.get("timelineMode") != "editorial":
        raise RuntimeError("v008 requires onecoin_roughcut.ts timelineMode='editorial'")
    _, endcard = parse_bookends()
    rows: list[dict] = []
    cursor = 0.0
    for shot in data["shots"]:
        dur = 3.0 if shot["spanId"] == SILENCE_SPAN_ID else float(shot["seconds"])
        rows.append({**shot, "start": cursor, "dur": dur, "end": cursor + dur})
        cursor += dur
    cursor += endcard
    return rows, cursor


def chapter_ranges(fps: int) -> tuple[list[dict], int, float]:
    rows, total_sec = scheduled_rows()
    order = ["cold_open", "the_promise", "the_crack", "the_void", "coda"]
    starts: dict[str, float] = {}
    for row in rows:
        starts.setdefault(row["chapterId"], float(row["start"]))
    total_frames = max(1, round(total_sec * fps))
    ranges: list[dict] = []
    for i, chapter in enumerate(order):
        start = round(starts[chapter] * fps)
        end = (round(starts[order[i + 1]] * fps) - 1) if i + 1 < len(order) else total_frames - 1
        ranges.append({"chapter": chapter, "start": start, "end": end, "frames": end - start + 1})
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

        chunk_size = 900
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
            run(
                [
                    NPX,
                    "remotion",
                    "render",
                    "src/index.ts",
                    "OneCoinPremium",
                    chunk_path,
                    f"--frames={cursor}-{chunk_end}",
                    "--codec=h264",
                    "--crf=12",
                    "--pixel-format=yuv420p",
                    "--concurrency=1",
                    "--timeout=120000",
                    "--muted",
                    "--overwrite",
                ],
                f"render OneCoinPremium v008 chapter {i}/5 {item['chapter']} chunk {chunk_index} frames {cursor}-{chunk_end}",
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
    list_file = CHAPTER_DIR / "concat_v008.txt"
    list_file.write_text("".join(f"file '{p.as_posix()}'\n" for p in chapters), encoding="utf-8")
    tmp = VISUAL_CONCAT.with_suffix(".tmp.mp4")
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-map", "0:v:0", "-c", "copy", tmp], "concat v008 chapter visuals")
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
            "-t",
            f"{total:.3f}",
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "16",
            "-vf",
            "scale=in_range=pc:out_range=tv,format=yuv420p",
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
        "final v008 libx264 slow crf16 mux",
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
        "revision": "v008",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "file": str(FINAL).replace("\\", "/"),
        "sha256": sha256(FINAL),
        "duration_seconds": dur,
        "runtime_band_pass": 27 * 60 <= dur <= 33 * 60,
        "editorial_override": "shorter runtime approved by user for tempo, sound, and readability",
        "video": video,
        "audio": audio,
        "render_method": "Remotion full-timeline frame-range chunks, FFmpeg concat, final libx264 slow CRF16 yuv420p AAC 192k",
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
        "voice_status": "approved ElevenLabs contract voice reused from v002; no new API call",
    }
    QC.parent.mkdir(parents=True, exist_ok=True)
    QC.write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"final": str(FINAL), "duration_seconds": dur, "sha256": qc["sha256"]}, indent=2), flush=True)


def update_manifest() -> None:
    manifest_path = EPDIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["state"] = "editorial_v008_rendered_pending_owner_review"
    active = manifest.setdefault("active_revisions", {})
    active["final_render"] = "v008"
    active["final_qc"] = "v008"
    artifacts = manifest.setdefault("artifacts", [])
    for aid in ["PD-2026-017-onecoin-final-render-v006", "PD-2026-017-onecoin-final-qc-v006", "PD-2026-017-onecoin-final-render-v007", "PD-2026-017-onecoin-final-qc-v007", "PD-2026-017-onecoin-final-render-v008", "PD-2026-017-onecoin-final-qc-v008"]:
        artifacts[:] = [a for a in artifacts if a.get("artifact_id") != aid]
    artifacts.append(
        {
            "artifact_id": "PD-2026-017-onecoin-final-render-v008",
            "artifact_type": "final_render",
            "revision": "v008",
            "uri": "artifact://E:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v008.mp4",
            "checksum": sha256(FINAL),
            "status": "candidate",
            "rights_status": "conditional",
            "qc_status": "editorial_runtime_override",
        }
    )
    artifacts.append(
        {
            "artifact_id": "PD-2026-017-onecoin-final-qc-v008",
            "artifact_type": "final_render_qc",
            "revision": "v008",
            "uri": "artifact://episodes/PD-2026-017-onecoin/08_edit/renders/final.v008.qc.json",
            "checksum": sha256(QC),
            "status": "candidate",
            "rights_status": "conditional",
            "qc_status": "pending_acceptance_runtime_override",
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
        "event": "editorial_v008_rendered",
        "revision": "v008",
        "actor": "codex",
        "note": "Rendered shorter OneCoin editorial cut v008. Natural-speed narration, 8.0s hook, no post-hook opening silence, cleaner captions and faster visual turnover. No upload/publish/schedule.",
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
        chapters = sorted(p for p in CHAPTER_DIR.glob("*.mp4") if re.match(r"\d\d_", p.name))
        if len(chapters) != 5:
            raise RuntimeError("Expected 5 chapter renders")
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
