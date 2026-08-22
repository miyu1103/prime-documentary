#!/usr/bin/env python3
"""Build v011 using the canonical BrandOpening after the 8-second hook."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-017-onecoin"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
MEDIA = Path("E:/pd-media")
OUT_DIR = MEDIA / "episodes" / EP / "07_edit"

SOURCE = OUT_DIR / "v009.mp4"
OPENING_CLIP = OUT_DIR / "onecoin_brand_opening_v011.mp4"
ENDING_CARD = EPDIR / "08_edit" / "renders" / "v010_structure" / "ending_card.v010.png"
ENDING_MUSIC = MEDIA / "library" / "music" / "outro" / "mus_20260614_outro_last_frame_v2.mp3"
OUT = OUT_DIR / "v011.mp4"
QC = EPDIR / "08_edit" / "renders" / "final.v011.qc.json"
EVENTS = EPDIR / "events" / "events.jsonl"

SRC_CAPTIONS = EPDIR / "08_edit" / "captions.v006.editorial_v009.srt"
OUT_CAPTIONS = EPDIR / "08_edit" / "captions.v008.structure_v011.srt"

HOOK_SEC = 8.0
OPENING_SEC = 3.5
ENDING_SEC = 6.0

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
        raise RuntimeError((p.stderr or p.stdout)[-2400:])
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


def srt_seconds(ts: str) -> float:
    h, m, rest = ts.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def srt_ts(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def shift_captions() -> int:
    text = SRC_CAPTIONS.read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n", text.strip())
    out_blocks: list[str] = []
    index = 1
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 3 or "-->" not in lines[1]:
            continue
        start_s, end_s = [part.strip() for part in lines[1].split("-->")]
        start = srt_seconds(start_s)
        end = srt_seconds(end_s)
        if start >= HOOK_SEC:
            start += OPENING_SEC
            end += OPENING_SEC
        out_blocks.append(f"{index}\n{srt_ts(start)} --> {srt_ts(end)}\n" + "\n".join(lines[2:]))
        index += 1
    OUT_CAPTIONS.write_text("\n\n".join(out_blocks) + "\n", encoding="utf-8")
    return index - 1


def build_video() -> None:
    for path in [SOURCE, OPENING_CLIP, ENDING_CARD, ENDING_MUSIC, SRC_CAPTIONS]:
        if not path.exists():
            raise FileNotFoundError(path)
    source_duration = duration(SOURCE)
    tmp = OUT.with_suffix(".tmp.mp4")
    if tmp.exists():
        tmp.unlink()
    filter_complex = (
        f"[0:v]trim=0:{HOOK_SEC:.3f},setpts=PTS-STARTPTS[hookv];"
        f"[0:a]atrim=0:{HOOK_SEC:.3f},asetpts=PTS-STARTPTS[hooka];"
        f"[1:v]trim=0:{OPENING_SEC:.3f},setpts=PTS-STARTPTS,fps=30,format=yuv420p[openv];"
        f"anullsrc=r=48000:cl=stereo,atrim=0:{OPENING_SEC:.3f},asetpts=PTS-STARTPTS[opena];"
        f"[0:v]trim=start={HOOK_SEC:.3f}:end={source_duration:.3f},setpts=PTS-STARTPTS[mainv];"
        f"[0:a]atrim=start={HOOK_SEC:.3f}:end={source_duration:.3f},asetpts=PTS-STARTPTS[maina];"
        f"[2:v]trim=0:{ENDING_SEC:.3f},setpts=PTS-STARTPTS,fps=30,format=yuv420p,fade=t=in:st=0:d=0.6,fade=t=out:st={ENDING_SEC - 1.0:.3f}:d=1.0[endv];"
        f"[3:a]atrim=0:{ENDING_SEC:.3f},asetpts=PTS-STARTPTS,volume=0.055,afade=t=out:st={ENDING_SEC - 1.0:.3f}:d=1.0[enda];"
        f"[hookv][hooka][openv][opena][mainv][maina][endv][enda]concat=n=4:v=1:a=1[v][a]"
    )
    subprocess.run(
        [
            str(FFMPEG),
            "-y",
            "-i",
            str(SOURCE),
            "-i",
            str(OPENING_CLIP),
            "-loop",
            "1",
            "-t",
            f"{ENDING_SEC:.3f}",
            "-i",
            str(ENDING_CARD),
            "-i",
            str(ENDING_MUSIC),
            "-filter_complex",
            filter_complex,
            "-map",
            "[v]",
            "-map",
            "[a]",
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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def write_qc(caption_count: int) -> None:
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
                "revision": "v011",
                "created_at": now(),
                "file": str(OUT).replace("\\", "/"),
                "sha256": sha256(OUT),
                "source_video": str(SOURCE).replace("\\", "/"),
                "opening_clip": str(OPENING_CLIP).replace("\\", "/"),
                "duration_seconds": dur,
                "runtime_band_pass": 27 * 60 <= dur <= 33 * 60,
                "structure": {
                    "hook": {"start": 0.0, "end": HOOK_SEC},
                    "opening": {"start": HOOK_SEC, "end": HOOK_SEC + OPENING_SEC, "type": "canonical_brand_opening"},
                    "main": {"start": HOOK_SEC + OPENING_SEC, "end": dur - ENDING_SEC},
                    "ending": {"start": dur - ENDING_SEC, "end": dur},
                },
                "caption_sidecar": rel(OUT_CAPTIONS),
                "caption_cues": caption_count,
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


def update_package() -> None:
    thumb = PKG / "thumbnail.selected.v008.png"
    base = json.loads((PKG / "youtube_meta.v010.json").read_text(encoding="utf-8"))
    base.update(
        {
            "revision": "v011",
            "status": "editorial_review_ready_canonical_opening_v011",
            "video_actual_path": str(OUT).replace("\\", "/"),
            "video_sha256": sha256(OUT),
            "captions_sidecar": rel(OUT_CAPTIONS),
            "render_revision": "v011",
            "structure_revision": "v011",
            "chapters": [
                {"time": "00:00", "seconds": 0.0, "title": "Hook: there was no coin"},
                {"time": "00:08", "seconds": 8.0, "title": "Opening: Prime Documentary"},
                {"time": "00:11", "seconds": 11.5, "title": "The promise"},
                {"time": "07:07", "seconds": 427.94, "title": "The crack"},
                {"time": "14:32", "seconds": 873.39, "title": "The void"},
                {"time": "18:55", "seconds": 1136.45, "title": "Coda: still missing"},
                {"time": "20:04", "seconds": 1203.8, "title": "Ending"},
            ],
            "created_at": now(),
        }
    )
    desc = base.get("description", "")
    desc = re.sub(
        r"Chapters:\n[\s\S]*?\n\nReview gates remain closed:",
        "Chapters:\n00:00 Hook: there was no coin\n00:08 Opening: Prime Documentary\n00:11 The promise\n07:07 The crack\n14:32 The void\n18:55 Coda: still missing\n20:04 Ending\n\nReview gates remain closed:",
        desc,
    )
    base["description"] = desc
    (PKG / "youtube_meta.v011.json").write_text(json.dumps(base, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    rights = json.loads((PKG / "rights_manifest.v010.json").read_text(encoding="utf-8"))
    rights.update({"revision": "v011", "generated_at": now(), "status": "editorial_pending_owner_schedule_canonical_opening_v011", "render_revision": "v011"})
    for asset in rights.get("assets", []):
        if asset.get("type") == "final_render":
            asset.update({"asset_id": f"{EP}-final-render-v011", "file": str(OUT).replace("\\", "/"), "sha256": sha256(OUT)})
        if asset.get("type") == "captions":
            asset.update({"asset_id": f"{EP}-captions-v008-structure-v011", "file": rel(OUT_CAPTIONS), "sha256": sha256(OUT_CAPTIONS)})
    (PKG / "rights_manifest.v011.json").write_text(json.dumps(rights, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    qc = json.loads(QC.read_text(encoding="utf-8"))
    delivery = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v011",
        "generated_at": now(),
        "status": "editorial_review_ready_canonical_brand_opening",
        "active_script_revision": "v001",
        "final_video": str(OUT).replace("\\", "/"),
        "video": str(OUT).replace("\\", "/"),
        "video_sha256": sha256(OUT),
        "duration_seconds": qc["duration_seconds"],
        "runtime_band_pass": qc["runtime_band_pass"],
        "structure": qc["structure"],
        "thumbnail": rel(thumb),
        "thumbnail_sha256": sha256(thumb),
        "captions": rel(OUT_CAPTIONS),
        "youtube_meta": rel(PKG / "youtube_meta.v011.json"),
        "rights_manifest": rel(PKG / "rights_manifest.v011.json"),
        "owner_review_request": rel(PKG / "OWNER_REVIEW_REQUEST.v011.md"),
        "external_side_effects": {"upload": False, "publish": False, "schedule": False, "paid_api": False},
    }
    (PKG / "final_delivery.v011.json").write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (PKG / "OWNER_REVIEW_REQUEST.v011.md").write_text(
        f"""# OWNER REVIEW REQUEST v011 - OneCoin Canonical Opening Cut

Episode: {EP}
Active script revision: v001
Video: `{delivery['final_video']}`
SHA256: `{delivery['video_sha256']}`
Runtime: {qc['duration_seconds']:.3f}s / {qc['duration_seconds'] / 60:.2f}min

## Structure
- 00:00 Hook
- 00:08 Canonical Prime Documentary opening
- 00:11 Main body
- 18:55 Coda / ending movement
- 20:04 End slate

No upload, publish, schedule, paid API, or external API call was performed.
""",
        encoding="utf-8",
    )


def update_manifest() -> None:
    manifest_path = EPDIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["state"] = "editorial_v011_canonical_opening_ready"
    active = manifest.setdefault("active_revisions", {})
    active.update(
        {
            "final_render": "v011",
            "final_qc": "v011",
            "captions": "v008_structure_v011",
            "youtube_meta": "v011",
            "rights_manifest": "v011",
            "final_delivery": "v011",
            "owner_review_request": "v011",
        }
    )
    manifest["updated_at"] = now()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event() -> None:
    with EVENTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(
            json.dumps(
                {
                    "ts": now(),
                    "episode_id": EP,
                    "stage": "edit",
                    "event": "editorial_v011_canonical_opening_ready",
                    "revision": "v011",
                    "actor": "codex",
                    "external_api_calls": False,
                    "upload_publish_schedule": False,
                    "note": "Replaced custom opening card with canonical BrandOpening.",
                },
                ensure_ascii=False,
            )
            + "\n"
        )


def main() -> int:
    caption_count = shift_captions()
    build_video()
    write_qc(caption_count)
    update_package()
    update_manifest()
    append_event()
    print(json.dumps({"video": str(OUT), "sha256": sha256(OUT), "qc": str(QC)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
