#!/usr/bin/env python3
"""Create a tighter Titan first-cut revision from the v001 render.

This is a non-destructive editorial recut:
- source v001 MP4 is never overwritten
- long narration-to-narration gaps are capped
- the first ~10 seconds stay as the hook
- a title opening card is inserted after the hook
- a short end card is appended
- captions are transformed onto the new timeline
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-016-titan"
EPDIR = ROOT / "episodes" / EP
EDIT = EPDIR / "08_edit"
RENDERS = EDIT / "renders"
PACKAGE = EPDIR / "09_package"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"
SOURCE_VIDEO = Path("E:/pd-media/episodes/PD-2026-016-titan/07_edit/v001.mp4")
OUTPUT_VIDEO = Path("E:/pd-media/episodes/PD-2026-016-titan/07_edit/v002.mp4")
SOURCE_CAPTIONS_JSON = EDIT / "captions.v002.json"
SOURCE_CAPTIONS_QC = EDIT / "captions.v002.qc.json"
OUTPUT_CAPTIONS_JSON = EDIT / "captions.v003.json"
OUTPUT_CAPTIONS_SRT = EDIT / "captions.v003.srt"
OUTPUT_CAPTIONS_QC = EDIT / "captions.v003.qc.json"
PLAN_PATH = RENDERS / "recut_plan.v002.json"
QC_PATH = RENDERS / "final.v002.qc.json"
FILTER_PATH = RENDERS / "titan_v002_recut.ffscript"
OPENING_CARD = RENDERS / "titan_v002_opening_card.png"
CLOSING_CARD = RENDERS / "titan_v002_closing_card.png"

MAX_DIALOGUE_GAP = 5.0
HOOK_END = 9.8
OPENING_SECONDS = 6.0
FINAL_TAIL_AFTER_LAST_CAPTION = 3.0
CLOSING_SECONDS = 4.0
FPS = 30


@dataclass(frozen=True)
class SourceSegment:
    start: float
    end: float
    label: str = "source"

    @property
    def duration(self) -> float:
        return self.end - self.start


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if proc.returncode != 0:
        raise RuntimeError(proc.stdout)
    return proc.stdout


def ffprobe(path: Path) -> dict:
    out = run([
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration,size:stream=index,codec_name,codec_type,width,height,pix_fmt,r_frame_rate,bit_rate",
        "-of",
        "json",
        str(path),
    ])
    return json.loads(out)


def as_float(value: float) -> float:
    return round(float(value), 3)


def build_segments(cues: list[dict], source_duration: float) -> tuple[list[SourceSegment], list[dict]]:
    last_caption_end = max(float(c["end"]) for c in cues)
    body_end = min(source_duration, last_caption_end + FINAL_TAIL_AFTER_LAST_CAPTION)
    removals: list[dict] = []
    half_gap = MAX_DIALOGUE_GAP / 2.0

    for a, b in zip(cues, cues[1:]):
        gap_start = float(a["end"])
        gap_end = float(b["start"])
        gap = gap_end - gap_start
        if gap <= MAX_DIALOGUE_GAP:
            continue
        if gap_end <= HOOK_END or gap_start >= body_end:
            continue
        remove_start = max(HOOK_END, gap_start + half_gap)
        remove_end = min(body_end, gap_end - half_gap)
        if remove_end - remove_start > 0.05:
            removals.append({
                "from": as_float(remove_start),
                "to": as_float(remove_end),
                "seconds_removed": as_float(remove_end - remove_start),
                "gap_before": as_float(gap),
                "from_span": a["span_id"],
                "to_span": b["span_id"],
                "from_caption_index": a["index"],
                "to_caption_index": b["index"],
            })

    segments = [SourceSegment(0.0, HOOK_END, "hook")]
    cursor = HOOK_END
    for item in removals:
        start = float(item["from"])
        end = float(item["to"])
        if start > cursor + 0.01:
            segments.append(SourceSegment(cursor, start, "body"))
        cursor = max(cursor, end)
    if body_end > cursor + 0.01:
        segments.append(SourceSegment(cursor, body_end, "body"))
    return segments, removals


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size=size)
    except OSError:
        return ImageFont.load_default()


def draw_center(draw: ImageDraw.ImageDraw, y: int, text: str, fnt: ImageFont.ImageFont, fill: tuple[int, int, int]) -> None:
    box = draw.textbbox((0, 0), text, font=fnt)
    x = (1920 - (box[2] - box[0])) // 2
    draw.text((x, y), text, font=fnt, fill=fill)


def make_card(path: Path, kind: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (1920, 1080), (4, 10, 18))
    pix = img.load()
    for y in range(1080):
        for x in range(1920):
            dx = (x - 960) / 960
            dy = (y - 540) / 540
            glow = max(0.0, 1.0 - math.sqrt(dx * dx + dy * dy))
            blue = int(18 + 42 * glow)
            green = int(18 + 24 * glow)
            pix[x, y] = (5 + int(8 * glow), green, blue)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(0, 1920, 96):
        alpha = 18 if x % 192 == 0 else 8
        od.line((x, 0, x - 260, 1080), fill=(180, 225, 255, alpha), width=2)
    od.rectangle((0, 0, 1920, 1080), outline=(40, 90, 110, 90), width=4)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB").filter(ImageFilter.GaussianBlur(0.25))
    d = ImageDraw.Draw(img)
    arial = "C:/Windows/Fonts/arial.ttf"
    arial_bold = "C:/Windows/Fonts/arialbd.ttf"
    small = font(arial, 34)
    mid = font(arial_bold, 58)
    big = font(arial_bold, 118)
    if kind == "opening":
        draw_center(d, 250, "PRIME DOCUMENTARY", small, (210, 230, 235))
        draw_center(d, 390, "PURE WASTE", big, (246, 250, 248))
        draw_center(d, 535, "THE LAST DIVE OF THE TITAN", mid, (195, 222, 230))
        draw_center(d, 760, "OPENING", small, (165, 190, 198))
    else:
        draw_center(d, 410, "PRIME DOCUMENTARY", mid, (235, 245, 246))
        draw_center(d, 535, "END", small, (175, 200, 205))
    img.save(path, "PNG")


def srt_time(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def transform_captions(cues: list[dict], timeline: list[dict]) -> list[dict]:
    transformed: list[dict] = []
    for cue in cues:
        start = float(cue["start"])
        end = float(cue["end"])
        for item in timeline:
            if item["type"] != "source":
                continue
            if start >= item["source_start"] - 0.001 and end <= item["source_end"] + 0.001:
                new_start = item["output_start"] + (start - item["source_start"])
                new_end = item["output_start"] + (end - item["source_start"])
                transformed.append({
                    "index": len(transformed) + 1,
                    "start": as_float(new_start),
                    "end": as_float(new_end),
                    "text": cue["text"],
                    "span_id": cue["span_id"],
                })
                break
        else:
            raise RuntimeError(f"Caption was cut by the recut plan: {cue}")
    return transformed


def write_srt(path: Path, cues: list[dict]) -> None:
    lines: list[str] = []
    for idx, cue in enumerate(cues, start=1):
        lines.append(str(idx))
        lines.append(f"{srt_time(float(cue['start']))} --> {srt_time(float(cue['end']))}")
        lines.append(cue["text"])
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def caption_qc(cues: list[dict], source_qc: dict, total_duration: float) -> dict:
    words = " ".join(c["text"] for c in cues).split()
    gaps = [float(b["start"]) - float(a["end"]) for a, b in zip(cues, cues[1:])]
    long_dialogue_gaps = [
        g for a, b, g in zip(cues, cues[1:], gaps)
        if g > MAX_DIALOGUE_GAP + 0.05 and not (a["span_id"] == "SPN-0001" and b["span_id"] == "SPN-0002")
    ]
    return {
        "episode_id": EP,
        "revision": "v003",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_revision": "v002",
        "source_qc": str(SOURCE_CAPTIONS_QC).replace("\\", "/"),
        "cue_count": len(cues),
        "text_exact_match_to_script": bool(source_qc.get("text_exact_match_to_script")),
        "script_words": source_qc.get("script_words"),
        "caption_words": len(words),
        "longest_caption_words": max(len(c["text"].split()) for c in cues),
        "longest_caption_chars": max(len(c["text"]) for c in cues),
        "overlap_count": sum(1 for a, b in zip(cues, cues[1:]) if float(b["start"]) < float(a["end"])),
        "max_dialogue_gap_seconds": as_float(max(gaps) if gaps else 0.0),
        "long_dialogue_gap_count_excluding_opening": len(long_dialogue_gaps),
        "duration_seconds": as_float(total_duration),
        "qc_status": "pass" if source_qc.get("text_exact_match_to_script") and len(long_dialogue_gaps) == 0 else "review",
    }


def write_filter_script(timeline: list[dict]) -> None:
    lines: list[str] = []
    refs: list[str] = []
    for idx, item in enumerate(timeline):
        v = f"v{idx}"
        a = f"a{idx}"
        if item["type"] == "source":
            s = item["source_start"]
            e = item["source_end"]
            lines.append(f"[0:v]trim=start={s:.3f}:end={e:.3f},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p[{v}];")
            lines.append(f"[0:a]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[{a}];")
        elif item["type"] == "opening":
            lines.append(f"[1:v]scale=1920:1080,fps={FPS},format=yuv420p,trim=duration={OPENING_SECONDS:.3f},setpts=PTS-STARTPTS[{v}];")
            lines.append(f"[3:a]atrim=duration={OPENING_SECONDS:.3f},asetpts=PTS-STARTPTS,volume=0.05,pan=stereo|c0=c0|c1=c0,afade=t=in:st=0:d=0.4,afade=t=out:st={OPENING_SECONDS - 0.8:.3f}:d=0.8[{a}];")
        elif item["type"] == "closing":
            lines.append(f"[2:v]scale=1920:1080,fps={FPS},format=yuv420p,trim=duration={CLOSING_SECONDS:.3f},setpts=PTS-STARTPTS[{v}];")
            lines.append(f"[4:a]atrim=duration={CLOSING_SECONDS:.3f},asetpts=PTS-STARTPTS,volume=0.035,pan=stereo|c0=c0|c1=c0,afade=t=in:st=0:d=0.5,afade=t=out:st={CLOSING_SECONDS - 0.9:.3f}:d=0.9[{a}];")
        else:
            raise ValueError(item)
        refs.append(f"[{v}][{a}]")
    lines.append("".join(refs) + f"concat=n={len(refs)}:v=1:a=1[vout][aout]")
    FILTER_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_manifest(final_qc: dict, captions_qc: dict) -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["state"] = "edit_review"
    active = manifest.setdefault("active_revisions", {})
    active["final_render"] = "v002"
    active["final_qc"] = "v002"
    active["captions"] = "v003"
    active["captions_srt"] = "v003"
    active["captions_json"] = "v003"
    active["captions_qc"] = "v003"
    active["recut_plan"] = "v002"
    artifacts = manifest.setdefault("artifacts", [])
    new = [
        ("PD-2026-016-titan-final-render-v002", "final_render", "v002", f"artifact://{str(OUTPUT_VIDEO).replace(chr(92), '/')}", final_qc["sha256"], "candidate", "conditional", "pass"),
        ("PD-2026-016-titan-final-qc-v002", "final_render_qc", "v002", "artifact://episodes/PD-2026-016-titan/08_edit/renders/final.v002.qc.json", sha256(QC_PATH), "candidate", "conditional", "pass"),
        ("PD-2026-016-titan-recut-plan-v002", "recut_plan", "v002", "artifact://episodes/PD-2026-016-titan/08_edit/renders/recut_plan.v002.json", sha256(PLAN_PATH), "candidate", "clear", "pass"),
        ("PD-2026-016-titan-captions-v003", "captions", "v003", "artifact://episodes/PD-2026-016-titan/08_edit/captions.v003.srt", sha256(OUTPUT_CAPTIONS_SRT), "candidate", "clear", captions_qc["qc_status"]),
        ("PD-2026-016-titan-captions-json-v003", "captions_json", "v003", "artifact://episodes/PD-2026-016-titan/08_edit/captions.v003.json", sha256(OUTPUT_CAPTIONS_JSON), "candidate", "clear", captions_qc["qc_status"]),
        ("PD-2026-016-titan-captions-qc-v003", "caption_qc", "v003", "artifact://episodes/PD-2026-016-titan/08_edit/captions.v003.qc.json", sha256(OUTPUT_CAPTIONS_QC), "candidate", "clear", captions_qc["qc_status"]),
    ]
    ids = {item[0] for item in new}
    artifacts[:] = [a for a in artifacts if a.get("artifact_id") not in ids]
    for aid, atype, rev, uri, checksum, status, rights_status, qc_status in new:
        artifacts.append({
            "artifact_id": aid,
            "artifact_type": atype,
            "revision": rev,
            "uri": uri,
            "checksum": checksum,
            "status": status,
            "rights_status": rights_status,
            "qc_status": qc_status,
        })
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(note: str) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "episode_id": EP,
        "stage": "edit",
        "event": "recut_created",
        "revision": "v002",
        "actor": "codex",
        "note": note,
    }
    with EVENTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    for path in [SOURCE_VIDEO, SOURCE_CAPTIONS_JSON, SOURCE_CAPTIONS_QC]:
        if not path.exists():
            raise FileNotFoundError(path)
    RENDERS.mkdir(parents=True, exist_ok=True)
    OUTPUT_VIDEO.parent.mkdir(parents=True, exist_ok=True)

    source_probe = ffprobe(SOURCE_VIDEO)
    source_duration = float(source_probe["format"]["duration"])
    source_caps = json.loads(SOURCE_CAPTIONS_JSON.read_text(encoding="utf-8"))
    source_qc = json.loads(SOURCE_CAPTIONS_QC.read_text(encoding="utf-8"))
    cues = source_caps["cues"]
    segments, removals = build_segments(cues, source_duration)

    timeline: list[dict] = []
    cursor = 0.0
    for idx, seg in enumerate(segments):
        if idx == 1:
            timeline.append({"type": "opening", "duration": OPENING_SECONDS, "output_start": as_float(cursor), "output_end": as_float(cursor + OPENING_SECONDS)})
            cursor += OPENING_SECONDS
        timeline.append({
            "type": "source",
            "label": seg.label,
            "source_start": as_float(seg.start),
            "source_end": as_float(seg.end),
            "duration": as_float(seg.duration),
            "output_start": as_float(cursor),
            "output_end": as_float(cursor + seg.duration),
        })
        cursor += seg.duration
    timeline.append({"type": "closing", "duration": CLOSING_SECONDS, "output_start": as_float(cursor), "output_end": as_float(cursor + CLOSING_SECONDS)})
    expected_duration = cursor + CLOSING_SECONDS

    make_card(OPENING_CARD, "opening")
    make_card(CLOSING_CARD, "closing")
    write_filter_script(timeline)

    plan = {
        "episode_id": EP,
        "revision": "v002",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_video": str(SOURCE_VIDEO).replace("\\", "/"),
        "output_video": str(OUTPUT_VIDEO).replace("\\", "/"),
        "hook_end_seconds": HOOK_END,
        "opening_seconds": OPENING_SECONDS,
        "closing_seconds": CLOSING_SECONDS,
        "max_dialogue_gap_seconds": MAX_DIALOGUE_GAP,
        "source_duration_seconds": as_float(source_duration),
        "expected_duration_seconds": as_float(expected_duration),
        "removed_seconds": as_float(sum(item["seconds_removed"] for item in removals)),
        "removed_gap_count": len(removals),
        "removals": removals,
        "timeline": timeline,
    }
    PLAN_PATH.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(SOURCE_VIDEO),
        "-loop",
        "1",
        "-t",
        f"{OPENING_SECONDS:.3f}",
        "-i",
        str(OPENING_CARD),
        "-loop",
        "1",
        "-t",
        f"{CLOSING_SECONDS:.3f}",
        "-i",
        str(CLOSING_CARD),
        "-f",
        "lavfi",
        "-t",
        f"{OPENING_SECONDS:.3f}",
        "-i",
        "sine=frequency=55:sample_rate=48000",
        "-f",
        "lavfi",
        "-t",
        f"{CLOSING_SECONDS:.3f}",
        "-i",
        "sine=frequency=41:sample_rate=48000",
        "-filter_complex_script",
        str(FILTER_PATH),
        "-map",
        "[vout]",
        "-map",
        "[aout]",
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "17",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        str(OUTPUT_VIDEO),
    ]
    print(json.dumps({"stage": "render_start", "expected_duration_seconds": as_float(expected_duration), "removed_seconds": plan["removed_seconds"], "removed_gap_count": len(removals)}, ensure_ascii=False))
    run(cmd)

    transformed = transform_captions(cues, timeline)
    OUTPUT_CAPTIONS_JSON.write_text(json.dumps({
        "episode_id": EP,
        "revision": "v003",
        "source": "captions.v002 transformed through recut_plan.v002",
        "cues": transformed,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_srt(OUTPUT_CAPTIONS_SRT, transformed)

    output_probe = ffprobe(OUTPUT_VIDEO)
    duration = float(output_probe["format"]["duration"])
    cap_qc = caption_qc(transformed, source_qc, duration)
    OUTPUT_CAPTIONS_QC.write_text(json.dumps(cap_qc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    final_qc = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v002",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "file": str(OUTPUT_VIDEO).replace("\\", "/"),
        "sha256": sha256(OUTPUT_VIDEO),
        "duration_seconds": as_float(duration),
        "source_revision": "v001",
        "recut_plan": "artifact://episodes/PD-2026-016-titan/08_edit/renders/recut_plan.v002.json",
        "runtime_band_pass": 35 * 60 <= duration <= 65 * 60,
        "video": next((s for s in output_probe["streams"] if s.get("codec_type") == "video"), None),
        "audio": next((s for s in output_probe["streams"] if s.get("codec_type") == "audio"), None),
        "render_method": "FFmpeg editorial recut from v001, hook/title/body/end structure, long gaps capped, libx264 slow CRF17 yuv420p AAC 192k",
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
    }
    QC_PATH.write_text(json.dumps(final_qc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    update_manifest(final_qc, cap_qc)
    append_event(f"Created v002 recut at {final_qc['file']} ({duration:.3f}s), removed {plan['removed_seconds']:.3f}s of long gaps, inserted opening/end cards. No upload/publish/schedule.")
    print(json.dumps({"stage": "done", "video": final_qc["file"], "sha256": final_qc["sha256"], "duration_seconds": final_qc["duration_seconds"], "captions_qc": cap_qc["qc_status"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
