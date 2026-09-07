"""Assemble the PD-2026-004-ftx premium review master.

Inputs are already produced separately:
- Remotion visual master, no audio
- final mixed stereo audio
- SRT captions

The output is a YouTube-ready MP4 with the finished stereo mix and forced-aligned
open captions. Captions are styled bottom-center per owner review preference.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-004-ftx"
MEDIA = Path(json.loads((ROOT / "config" / "storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

VIDEO = MEDIA / "episodes" / EP / "08_edit" / "ftx_visual_v007.mp4"
AUDIO = MEDIA / "episodes" / EP / "06_audio" / "final_mix_v001.m4a"
SRT = ROOT / "episodes" / EP / "08_edit" / "captions.v002.srt"
OUT = MEDIA / "episodes" / EP / "08_edit" / "ftx_premium_v009.mp4"


def run(cmd: list[str], desc: str) -> subprocess.CompletedProcess[str]:
    print(f">> {desc}")
    result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
    if result.returncode:
        print((result.stdout or "")[-2000:])
        print((result.stderr or "")[-4000:])
        raise RuntimeError(desc)
    return result


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ffprobe_json(path: Path) -> dict:
    result = run(
        [
            FFPROBE,
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ],
        f"probe {path.name}",
    )
    return json.loads(result.stdout)


def main() -> int:
    for path in [VIDEO, AUDIO, SRT]:
        if not path.exists():
            raise FileNotFoundError(path)
    OUT.parent.mkdir(parents=True, exist_ok=True)

    tmp = OUT.with_suffix(".tmp.mp4")
    if tmp.exists():
        tmp.unlink()
    escaped_srt = SRT.as_posix().replace(":", "\\:")
    style = ",".join(
        [
            "FontName=Arial",
            "FontSize=25",
            "PrimaryColour=&H00F8F8F8",
            "OutlineColour=&H00000000",
            "BackColour=&H9A000000",
            "BorderStyle=4",
            "Bold=0",
            "Outline=1",
            "Shadow=0",
            "Alignment=2",
            "MarginV=34",
        ]
    )

    run(
        [
            FFMPEG,
            "-y",
            "-i",
            str(VIDEO),
            "-i",
            str(AUDIO),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-vf",
            f"subtitles='{escaped_srt}':force_style='{style}'",
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
            "-shortest",
            str(tmp),
        ],
        "final captioned assembly",
    )
    tmp.replace(OUT)

    probe = ffprobe_json(OUT)
    info = {
        "episode_id": EP,
        "output": str(OUT),
        "sha256": sha256(OUT),
        "size_bytes": OUT.stat().st_size,
        "ffprobe": probe,
    }
    sidecar = OUT.with_suffix(".probe.v001.json")
    sidecar.write_text(json.dumps(info, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: info[k] for k in ["output", "sha256", "size_bytes"]}, indent=2, ensure_ascii=False))
    print(f"probe: {sidecar}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
