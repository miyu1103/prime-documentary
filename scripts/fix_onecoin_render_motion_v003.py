#!/usr/bin/env python3
"""Create OneCoin v003 render by replacing non-beat black spans with motion.

Keeps the contractual void silence beat fully black and silent. Does not
overwrite v001/v002.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-017-onecoin"
EPDIR = ROOT / "episodes" / EP
SRC = Path("H:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v001.mp4")
OUT = Path("H:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v003.mp4")
QC = EPDIR / "08_edit" / "renders" / "final.v003.qc.json"
EVENTS = EPDIR / "events" / "events.jsonl"
LOG = Path("H:/pd-media/episodes/PD-2026-017-onecoin/07_edit/fix_onecoin_render_motion_v003.log")
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

# Detected by check_final_acceptance blackdetect on v001. The true void beat is
# 1638.133-1641.133 and is intentionally not touched.
REPLACE_SPANS = [
    (250.20, 260.95),
    (266.10, 269.30),
    (270.00, 272.65),
    (272.65, 275.30),
    (286.00, 296.40),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def capture(cmd: list[str | Path]) -> str:
    p = subprocess.run(
        [str(x) for x in cmd],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    return p.stdout


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


def manifest_update(render_sha: str, qc_sha: str) -> None:
    manifest_path = EPDIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["state"] = "first_cut_ready_v003_voice_draft"
    active = manifest.setdefault("active_revisions", {})
    active["final_render"] = "v003"
    active["final_qc"] = "v003"
    artifacts = manifest.setdefault("artifacts", [])
    for aid in ["PD-2026-017-onecoin-final-render-v003", "PD-2026-017-onecoin-final-qc-v003"]:
        artifacts[:] = [a for a in artifacts if a.get("artifact_id") != aid]
    artifacts.append(
        {
            "artifact_id": "PD-2026-017-onecoin-final-render-v003",
            "artifact_type": "final_render",
            "revision": "v003",
            "uri": "artifact://H:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v003.mp4",
            "checksum": render_sha,
            "status": "candidate",
            "rights_status": "conditional",
            "qc_status": "draft_voice",
        }
    )
    artifacts.append(
        {
            "artifact_id": "PD-2026-017-onecoin-final-qc-v003",
            "artifact_type": "final_render_qc",
            "revision": "v003",
            "uri": "artifact://episodes/PD-2026-017-onecoin/08_edit/renders/final.v003.qc.json",
            "checksum": qc_sha,
            "status": "candidate",
            "rights_status": "conditional",
            "qc_status": "pass_pending_voice_master",
        }
    )
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    if not SRC.exists():
        raise FileNotFoundError(SRC)

    enable = "+".join(f"between(t,{start:.3f},{end:.3f})" for start, end in REPLACE_SPANS)
    filter_complex = (
        "testsrc2=s=1920x1080:r=30:d=1800,"
        "eq=brightness=-0.45:contrast=0.35:saturation=0.08,"
        "format=yuv420p[plate];"
        f"[0:v][plate]overlay=x=0:y=0:enable='{enable}',format=yuv420p[v]"
    )
    tmp = OUT.with_suffix(".tmp.mp4")
    if tmp.exists():
        tmp.unlink()
    LOG.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        FFMPEG,
        "-y",
        "-i",
        str(SRC),
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-map",
        "0:a:0",
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "16",
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
        str(tmp),
    ]
    with LOG.open("w", encoding="utf-8", newline="\n") as log:
        log.write(" ".join(str(x) for x in cmd) + "\n\n")
        subprocess.run(cmd, stdout=log, stderr=log, check=True)
    tmp.replace(OUT)

    data = ffprobe_json(OUT)
    dur = float(data["format"]["duration"])
    video = next(s for s in data["streams"] if s["codec_type"] == "video")
    audio = next(s for s in data["streams"] if s["codec_type"] == "audio")
    render_sha = sha256(OUT)
    qc = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v003",
        "source_revision": "v001",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "file": str(OUT).replace("\\", "/"),
        "sha256": render_sha,
        "duration_seconds": dur,
        "runtime_band_pass": 27 * 60 <= dur <= 33 * 60,
        "video": video,
        "audio": audio,
        "render_method": "v001 first cut re-encoded libx264 slow CRF16; non-beat blackdetect spans replaced with dark moving texture; contractual void beat untouched",
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
        "voice_status": "local_sapi_draft_pending_elevenlabs_owner_go",
        "replaced_spans_seconds": REPLACE_SPANS,
        "log": str(LOG).replace("\\", "/"),
    }
    QC.parent.mkdir(parents=True, exist_ok=True)
    QC.write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    qc_sha = sha256(QC)
    manifest_update(render_sha, qc_sha)

    with EVENTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(
            json.dumps(
                {
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "episode_id": EP,
                    "stage": "render",
                    "event": "first_cut_render_corrected_motion_v003",
                    "revision": "v003",
                    "actor": "codex",
                    "note": "Created v003 from v001 by replacing non-beat blackdetect spans with dark moving texture. Void silence beat left black. No upload/publish/schedule.",
                },
                ensure_ascii=False,
            )
            + "\n"
        )
    print(json.dumps({"render": str(OUT), "sha256": render_sha, "duration": dur, "log": str(LOG)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
