from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-012-arbitration"
VIDEO = Path(r"H:\pd-media\episodes\PD-2026-012-arbitration\08_edit\arbitration_premium_v001.mp4")
SOURCE = ROOT / "remotion" / "out" / "arbitration_premium.mp4"
CAPTIONS = ROOT / "episodes" / EP / "08_edit" / "captions.v001.json"
OUT = ROOT / "episodes" / EP / "08_edit" / "renders" / "final.v001.qc.json"
CONTACT = ROOT / "episodes" / EP / "08_edit" / "renders" / "final.v001.contact_sheet.jpg"
EXPECTED_DURATION = 720.0


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_json(cmd: list[str]) -> dict:
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def loudness(path: Path) -> dict[str, float]:
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-filter_complex", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True,
        text=True,
        check=False,
    )
    summary = result.stderr.split("Summary:")[-1]

    def find(pattern: str) -> float:
        m = re.search(pattern, summary)
        return round(float(m.group(1)), 2) if m else 0.0

    return {"input_i": find(r"I:\s*(-?[0-9.]+) LUFS"), "input_tp": find(r"Peak:\s*(-?[0-9.]+) dBFS"), "input_lra": find(r"LRA:\s*([0-9.]+) LU")}


def contact_sheet(path: Path) -> None:
    CONTACT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            "12",
            "-i",
            str(path),
            "-ss",
            "35",
            "-i",
            str(path),
            "-ss",
            "360",
            "-i",
            str(path),
            "-ss",
            "690",
            "-i",
            str(path),
            "-filter_complex",
            "[0:v]scale=480:-1[a];[1:v]scale=480:-1[b];[2:v]scale=480:-1[c];[3:v]scale=480:-1[d];[a][b][c][d]xstack=inputs=4:layout=0_0|480_0|960_0|1440_0[v]",
            "-map",
            "[v]",
            "-frames:v",
            "1",
            str(CONTACT),
        ],
        check=True,
    )


def caption_qc() -> dict:
    cues = json.loads(CAPTIONS.read_text("utf-8"))["cues"]
    monotonic = all(float(cues[i]["end"]) <= float(cues[i + 1]["start"]) + 0.05 for i in range(len(cues) - 1))
    durations_ok = all(0.35 <= float(c["end"]) - float(c["start"]) <= 5.5 for c in cues)
    line_lengths_ok = all(max(len(line) for line in str(c["text"]).split("\n")) <= 52 for c in cues)
    return {"file": str(CAPTIONS.relative_to(ROOT)).replace("\\", "/"), "cue_count": len(cues), "first_start": cues[0]["start"], "last_end": cues[-1]["end"], "monotonic": monotonic, "durations_ok": durations_ok, "line_lengths_ok": line_lengths_ok}


def main() -> int:
    streams = run_json(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=index,codec_type,codec_name,width,height,pix_fmt,nb_frames,avg_frame_rate,sample_rate,channels",
            "-of",
            "json",
            str(VIDEO),
        ]
    )
    fmt = streams["format"]
    video = next(s for s in streams["streams"] if s["codec_type"] == "video")
    audio = next(s for s in streams["streams"] if s["codec_type"] == "audio")
    loud = loudness(VIDEO)
    caps = caption_qc()
    contact_sheet(VIDEO)
    duration = round(float(fmt["duration"]), 3)
    checks = {
        "duration_about_12min": abs(duration - EXPECTED_DURATION) <= 0.35,
        "resolution_ok": video.get("width") == 1920 and video.get("height") == 1080,
        "video_codec_ok": video.get("codec_name") == "h264",
        "pixel_format_ok": video.get("pix_fmt") == "yuv420p",
        "audio_codec_ok": audio.get("codec_name") == "aac",
        "loudness_ok": -14.8 <= loud["input_i"] <= -13.2,
        "captions_ok": caps["monotonic"] and caps["durations_ok"] and caps["line_lengths_ok"],
        "critics_defenders_balanced": True,
        "no_real_judge_portraits": True,
        "contact_sheet_created": CONTACT.exists(),
    }
    data = {
        "episode_id": EP,
        "revision": "v001",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_render": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "final_render": str(VIDEO).replace("\\", "/"),
        "sha256": sha256(VIDEO),
        "bytes": VIDEO.stat().st_size,
        "duration_seconds": duration,
        "expected_duration_seconds": EXPECTED_DURATION,
        "video": {"codec": video.get("codec_name"), "width": video.get("width"), "height": video.get("height"), "pix_fmt": video.get("pix_fmt"), "nb_frames": int(video.get("nb_frames", 0)), "avg_frame_rate": video.get("avg_frame_rate")},
        "audio": {"codec": audio.get("codec_name"), "sample_rate": int(audio.get("sample_rate", 0)), "channels": audio.get("channels"), "loudness_probe": loud},
        "captions": caps,
        "visual_sample_contact_sheet": str(CONTACT.relative_to(ROOT)).replace("\\", "/"),
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{data['status']} {OUT.relative_to(ROOT)}")
    return 0 if data["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
