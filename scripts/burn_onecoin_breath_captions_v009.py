#!/usr/bin/env python3
"""Burn v009 breath-pause captions over the v008 viewing cut.

This avoids a full Remotion re-render when only burned captions and caption
readability changed. It performs no upload, publish, schedule, or external API
calls.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-017-onecoin"
EPDIR = ROOT / "episodes" / EP
MEDIA = Path("H:/pd-media")
SOURCE_VIDEO = MEDIA / "episodes" / EP / "07_edit" / "v008.mp4"
SOURCE_AUDIO = ROOT / "remotion" / "public" / "onecoin" / "audio" / "onecoin_final_mix_v009.wav"
CAPTIONS_JSON = EPDIR / "08_edit" / "captions.v006.editorial_v009.json"
CAPTIONS_ASS = EPDIR / "08_edit" / "captions.v006.editorial_v009.ass"
OUT = MEDIA / "episodes" / EP / "07_edit" / "v009.mp4"
QC = EPDIR / "08_edit" / "renders" / "final.v009.qc.json"
EVENTS = EPDIR / "events" / "events.jsonl"

FFMPEG = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
FFPROBE = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe")
if not FFMPEG.exists():
    FFMPEG = Path("ffmpeg")
if not FFPROBE.exists():
    FFPROBE = Path("ffprobe")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def capture(cmd: list[str | Path]) -> str:
    p = subprocess.run([str(x) for x in cmd], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout)[-2000:])
    return p.stdout


def duration(path: Path) -> float:
    return float(capture([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).strip())


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
            ]
        )
    )


def ass_ts(seconds: float) -> str:
    cs = int(round(seconds * 100))
    h, rem = divmod(cs, 360000)
    m, rem = divmod(rem, 6000)
    s, c = divmod(rem, 100)
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"


def ass_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", "(").replace("}", ")").replace("\n", "\\N")


def write_ass() -> int:
    data = json.loads(CAPTIONS_JSON.read_text(encoding="utf-8"))
    cues = data["cues"]
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Arial,42,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1.6,0,2,260,260,82,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    for cue in cues:
        lines.append(
            f"Dialogue: 0,{ass_ts(float(cue['start']))},{ass_ts(float(cue['end']))},Caption,,0,0,0,,{ass_text(cue['text'])}\n"
        )
    CAPTIONS_ASS.write_text("".join(lines), encoding="utf-8")
    return len(cues)


def burn() -> None:
    if not SOURCE_VIDEO.exists():
        raise FileNotFoundError(SOURCE_VIDEO)
    if not SOURCE_AUDIO.exists():
        raise FileNotFoundError(SOURCE_AUDIO)
    if not CAPTIONS_JSON.exists():
        raise FileNotFoundError(CAPTIONS_JSON)
    cue_count = write_ass()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".tmp.mp4")
    if tmp.exists():
        tmp.unlink()
    ass_path = CAPTIONS_ASS.as_posix().replace(":", "\\:")
    vf = f"drawbox=x=0:y=860:w=iw:h=220:color=black@1.0:t=fill,ass='{ass_path}'"
    total = duration(SOURCE_AUDIO)
    subprocess.run(
        [
            str(FFMPEG),
            "-y",
            "-i",
            str(SOURCE_VIDEO),
            "-i",
            str(SOURCE_AUDIO),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-t",
            f"{total:.3f}",
            "-vf",
            vf,
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
            str(tmp),
        ],
        check=True,
    )
    tmp.replace(OUT)
    write_qc(cue_count)
    update_manifest()
    append_event(cue_count)


def write_qc(cue_count: int) -> None:
    data = ffprobe_json(OUT)
    dur = float(data["format"]["duration"])
    video = next(s for s in data["streams"] if s["codec_type"] == "video")
    audio = next(s for s in data["streams"] if s["codec_type"] == "audio")
    QC.parent.mkdir(parents=True, exist_ok=True)
    QC.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "episode_id": EP,
                "revision": "v009",
                "created_at": now(),
                "file": str(OUT).replace("\\", "/"),
                "sha256": sha256(OUT),
                "source_video": str(SOURCE_VIDEO).replace("\\", "/"),
                "source_audio": str(SOURCE_AUDIO).replace("\\", "/"),
                "duration_seconds": dur,
                "runtime_band_pass": 27 * 60 <= dur <= 33 * 60,
                "editorial_override": "shorter runtime approved by user for tempo, sound, and readability",
                "caption_method": "v009 breath-pause cues burned over v008 base with lower-caption mask",
                "caption_cues": cue_count,
                "video": video,
                "audio": audio,
                "upload_performed": False,
                "publish_performed": False,
                "schedule_performed": False,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def update_manifest() -> None:
    manifest_path = EPDIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["state"] = "editorial_v009_caption_burn_ready"
    active = manifest.setdefault("active_revisions", {})
    active.update(
        {
            "roughcut": "v009",
            "onecoin_roughcut": "v009",
            "onecoin_captions": "v009",
            "audio_mix": "v006_editorial_v009",
            "captions": "v006_editorial_v009",
            "final_render": "v009",
            "final_qc": "v009",
        }
    )
    artifacts = manifest.setdefault("artifacts", [])
    artifacts[:] = [a for a in artifacts if a.get("revision") != "v009" or a.get("artifact_type") not in {"final_render", "final_render_qc"}]
    artifacts.append(
        {
            "artifact_id": "PD-2026-017-onecoin-final-render-v009",
            "artifact_type": "final_render",
            "revision": "v009",
            "uri": "artifact://H:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v009.mp4",
            "checksum": sha256(OUT),
            "status": "candidate",
            "rights_status": "conditional",
            "qc_status": "editorial_runtime_override",
        }
    )
    artifacts.append(
        {
            "artifact_id": "PD-2026-017-onecoin-final-qc-v009",
            "artifact_type": "final_render_qc",
            "revision": "v009",
            "uri": "artifact://episodes/PD-2026-017-onecoin/08_edit/renders/final.v009.qc.json",
            "checksum": sha256(QC),
            "status": "candidate",
            "rights_status": "conditional",
            "qc_status": "pending_acceptance_runtime_override",
        }
    )
    manifest["updated_at"] = now()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(cue_count: int) -> None:
    with EVENTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(
            json.dumps(
                {
                    "ts": now(),
                    "episode_id": EP,
                    "stage": "render",
                    "event": "editorial_v009_caption_burn_ready",
                    "revision": "v009",
                    "actor": "codex",
                    "caption_cues": cue_count,
                    "external_api_calls": False,
                    "upload_publish_schedule": False,
                },
                ensure_ascii=False,
            )
            + "\n"
        )


def main() -> int:
    burn()
    print(json.dumps({"video": str(OUT), "sha256": sha256(OUT), "qc": str(QC)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
