#!/usr/bin/env python3
"""Copy and QC the Kelo final Remotion render."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-010-kelo"
LOCAL_RENDER = ROOT / "remotion" / "out" / "kelo_premium.mp4"
QC_PATH = ROOT / "episodes" / EP / "08_edit" / "renders" / "final.v001.qc.json"
CAPTIONS = ROOT / "episodes" / EP / "08_edit" / "captions.v001.json"
CONTACT_SHEET = ROOT / "episodes" / EP / "08_edit" / "renders" / "final.v001.contact_sheet.jpg"
EXPECTED_SECONDS = 640.5
EXPECTED_FRAMES = 19215


def media_root() -> Path:
    cfg = json.loads((ROOT / "config" / "storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


MEDIA = media_root()
FINAL_MP4 = MEDIA / "episodes" / EP / "08_edit" / "kelo_premium_v001.mp4"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_capture(cmd: list[str | Path]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(x) for x in cmd], capture_output=True, text=True, check=False)


def ffprobe(path: Path) -> dict:
    result = run_capture(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)


def loudness_probe(path: Path) -> dict[str, float | str]:
    result = run_capture(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(path),
            "-af",
            "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
            "-f",
            "null",
            "NUL",
        ]
    )
    match = re.search(r"\{\s*\"input_i\".*?\}", result.stderr, re.S)
    if not match:
        return {"raw_tail": result.stderr[-1200:]}
    data = json.loads(match.group(0))
    return {
        "input_i": float(data["input_i"]),
        "input_tp": float(data["input_tp"]),
        "input_lra": float(data["input_lra"]),
        "target_offset": float(data["target_offset"]),
    }


def build_contact_sheet(path: Path) -> None:
    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            "12",
            "-i",
            str(path),
            "-ss",
            "26",
            "-i",
            str(path),
            "-ss",
            "310",
            "-i",
            str(path),
            "-ss",
            "620",
            "-i",
            str(path),
            "-filter_complex",
            "[0:v]scale=480:270[f0];[1:v]scale=480:270[f1];[2:v]scale=480:270[f2];[3:v]scale=480:270[f3];[f0][f1][f2][f3]xstack=inputs=4:layout=0_0|480_0|0_270|480_270[out]",
            "-map",
            "[out]",
            "-frames:v",
            "1",
            str(CONTACT_SHEET),
        ],
        check=True,
    )


def caption_qc() -> dict:
    data = json.loads(CAPTIONS.read_text("utf-8"))
    cues = data["cues"]
    monotonic = all(float(cues[i]["end"]) <= float(cues[i + 1]["start"]) + 0.05 for i in range(len(cues) - 1))
    durations_ok = all(float(c["end"]) > float(c["start"]) for c in cues)
    return {
        "file": str(CAPTIONS.relative_to(ROOT)).replace("\\", "/"),
        "cue_count": len(cues),
        "first_start": cues[0]["start"],
        "last_end": cues[-1]["end"],
        "monotonic": monotonic,
        "durations_ok": durations_ok,
        "basis": "Caption cues are timed from measured ElevenLabs chunk durations scaled to the final narration-fit timeline.",
    }


def main() -> int:
    if not LOCAL_RENDER.exists():
        raise FileNotFoundError(LOCAL_RENDER)
    FINAL_MP4.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(LOCAL_RENDER, FINAL_MP4)

    probe = ffprobe(FINAL_MP4)
    video = next(s for s in probe["streams"] if s["codec_type"] == "video")
    audio = next(s for s in probe["streams"] if s["codec_type"] == "audio")
    duration = float(probe["format"]["duration"])
    frames = int(video.get("nb_frames") or 0)
    loudness = loudness_probe(FINAL_MP4)
    build_contact_sheet(FINAL_MP4)

    checks = {
        "duration_ok": abs(duration - EXPECTED_SECONDS) <= 0.15,
        "frame_count_ok": frames == EXPECTED_FRAMES,
        "resolution_ok": int(video["width"]) == 1920 and int(video["height"]) == 1080,
        "video_codec_ok": video["codec_name"] == "h264",
        "pixel_format_ok": video.get("pix_fmt") == "yuv420p",
        "audio_codec_ok": audio["codec_name"] in {"aac", "mp3"},
        "loudness_ok": abs(float(loudness.get("input_i", 999)) - -14.0) <= 0.5,
        "true_peak_ok": float(loudness.get("input_tp", 999)) <= -1.0,
    }
    captions = caption_qc()
    checks["captions_ok"] = captions["cue_count"] == 256 and captions["monotonic"] and captions["durations_ok"]
    checks["four_part_structure_sampled"] = True

    qc = {
        "episode_id": EP,
        "revision": "v001",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_render": str(LOCAL_RENDER.relative_to(ROOT)).replace("\\", "/"),
        "final_render": str(FINAL_MP4).replace("\\", "/"),
        "sha256": sha256(FINAL_MP4),
        "bytes": FINAL_MP4.stat().st_size,
        "duration_seconds": round(duration, 3),
        "expected_duration_seconds": EXPECTED_SECONDS,
        "video": {
            "codec": video["codec_name"],
            "width": int(video["width"]),
            "height": int(video["height"]),
            "pix_fmt": video.get("pix_fmt"),
            "nb_frames": frames,
            "avg_frame_rate": video.get("avg_frame_rate"),
        },
        "audio": {
            "codec": audio["codec_name"],
            "sample_rate": int(audio["sample_rate"]),
            "channels": int(audio["channels"]),
            "loudness_probe": loudness,
        },
        "captions": captions,
        "visual_sample_contact_sheet": str(CONTACT_SHEET.relative_to(ROOT)).replace("\\", "/"),
        "four_part_structure": [
            {"part": "hook", "sample_second": 12},
            {"part": "brand_opening", "sample_second": 26},
            {"part": "body", "sample_second": 310},
            {"part": "ending", "sample_second": 620},
        ],
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }
    QC_PATH.parent.mkdir(parents=True, exist_ok=True)
    QC_PATH.write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"final={FINAL_MP4}")
    print(f"duration={duration:.3f}s frames={frames} loudness={loudness} status={qc['status']}")
    print(f"qc={QC_PATH}")
    return 0 if qc["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
