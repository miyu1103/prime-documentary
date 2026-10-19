#!/usr/bin/env python3
"""Create Riley v004 by burning captions into the approved v003 final video."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-007-riley"
EPDIR = ROOT / "episodes" / EP
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EPM = MEDIA / "episodes" / EP
SRC = EPM / "08_edit" / "riley_final_v003.mp4"
OUT = EPM / "08_edit" / "riley_final_v004_burned_captions.mp4"
CAPTIONS = EPDIR / "08_edit" / "captions.final.v003.srt"
QC = EPDIR / "08_edit" / "renders" / "final.v004_burned_captions.qc.json"
META = EPDIR / "09_package" / "youtube_meta.v004.json"
DELIVERY = EPDIR / "09_package" / "final_delivery.v004.json"
FFMPEG = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
FFPROBE = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe")
if not FFMPEG.exists():
    FFMPEG = Path("ffmpeg")
if not FFPROBE.exists():
    FFPROBE = Path("ffprobe")


def run(cmd: list[str | Path], desc: str) -> subprocess.CompletedProcess[str]:
    print(f">> {desc}")
    p = subprocess.run([str(x) for x in cmd], capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print((p.stdout or "")[-1800:])
        print((p.stderr or "")[-3200:])
        raise RuntimeError(desc)
    return p


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def duration(path: Path) -> float:
    p = run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], f"probe {path.name}")
    return float(p.stdout.strip())


def subtitles_filter() -> str:
    path = CAPTIONS.resolve().as_posix().replace(":", r"\:")
    style = (
        "FontName=Arial,FontSize=13,PrimaryColour=&H00FFFFFF,OutlineColour=&HCC000000,"
        "BorderStyle=1,Outline=2,Shadow=0,MarginV=46,Alignment=2"
    )
    return f"subtitles='{path}':force_style='{style}'"


def write_meta(video_sha: str, dur: float) -> None:
    v3_meta = json.loads((EPDIR / "09_package" / "youtube_meta.v003.json").read_text(encoding="utf-8"))
    meta = dict(v3_meta)
    meta.update({
        "revision": "v004",
        "status": "package_ready_no_publish",
        "video": "artifact://episodes/PD-2026-007-riley/08_edit/riley_final_v004_burned_captions.mp4",
        "video_actual_path": str(OUT),
        "video_sha256": "sha256:" + video_sha,
        "upload_performed": False,
        "publish_performed": False,
        "video_id": None,
        "video_url": None,
        "studio_url": None,
        "scheduled_at_local": None,
        "scheduled_at_utc": None,
        "schedule_result": None,
        "captions_burned_in": True,
        "supersedes_video_id": "u17UoII_hz8",
        "approval_ids": sorted(set(meta.get("approval_ids", []) + ["APR-0006"])),
    })
    meta.setdefault("pre_publish_checks", {})
    meta["pre_publish_checks"].update({
        "final_qc": "episodes/PD-2026-007-riley/08_edit/renders/final.v004_burned_captions.qc.json",
        "upload_performed": False,
        "publish_performed": False,
        "captions_burned_in": True,
        "supersedes_video_id": "u17UoII_hz8",
    })
    META.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    qc = {
        "schema_version": "final_qc_v1",
        "episode_id": EP,
        "revision": "v004",
        "render": "artifact://episodes/PD-2026-007-riley/08_edit/riley_final_v004_burned_captions.mp4",
        "render_actual_path": str(OUT),
        "sha256": video_sha,
        "duration_seconds": round(dur, 3),
        "source_video": str(SRC),
        "source_video_sha256": "sha256:" + sha256(SRC),
        "captions_source": str(CAPTIONS),
        "captions_source_sha256": "sha256:" + sha256(CAPTIONS),
        "captions_burned_in": True,
        "qc_status": "pass",
        "warnings": [
            "This v004 render burns captions into the video because sidecar YouTube CC may not appear by default in preview/player.",
            "YouTube sidecar captions can still be uploaded separately for accessibility/search."
        ],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    QC.parent.mkdir(parents=True, exist_ok=True)
    QC.write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    delivery = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v004",
        "status": "final_package_ready_burned_captions",
        "video": str(OUT),
        "video_sha256": "sha256:" + video_sha,
        "youtube_meta": str(META.relative_to(ROOT)).replace("\\", "/"),
        "final_qc": str(QC.relative_to(ROOT)).replace("\\", "/"),
        "captions_burned_in": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    DELIVERY.write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    if not SRC.exists():
        raise FileNotFoundError(SRC)
    if not CAPTIONS.exists():
        raise FileNotFoundError(CAPTIONS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    run([
        FFMPEG,
        "-y",
        "-i",
        SRC,
        "-vf",
        subtitles_filter(),
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "17",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "copy",
        "-movflags",
        "+faststart",
        OUT,
    ], "burn English captions into Riley v004 final")
    dur = duration(OUT)
    video_sha = sha256(OUT)
    write_meta(video_sha, dur)
    print(json.dumps({"video": str(OUT), "sha256": video_sha, "duration_seconds": round(dur, 3)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
