#!/usr/bin/env python3
"""Create OneCoin v002 render by lifting non-beat blackdetect spans only.

Keeps the contractual void silence beat black. Does not overwrite v001.
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
SRC = Path("E:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v001.mp4")
OUT = Path("E:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v002.mp4")
QC = EPDIR / "08_edit" / "renders" / "final.v002.qc.json"
EVENTS = EPDIR / "events" / "events.jsonl"
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

# Detected by check_final_acceptance blackdetect on v001. The true void beat is
# 1638.133-1641.133 and is intentionally not touched.
LIFT_SPANS = [
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
    p = subprocess.run([str(x) for x in cmd], capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
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


def main() -> int:
    if not SRC.exists():
        raise FileNotFoundError(SRC)
    filters = []
    for start, end in LIFT_SPANS:
        filters.append(f"drawbox=x=0:y=0:w=iw:h=ih:color=#24262b@1.0:t=fill:enable='between(t,{start:.3f},{end:.3f})'")
    tmp = OUT.with_suffix(".tmp.mp4")
    if tmp.exists():
        tmp.unlink()
    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-i",
            str(SRC),
            "-vf",
            ",".join(filters),
            "-map",
            "0:v:0",
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
        ],
        check=True,
    )
    tmp.replace(OUT)
    data = ffprobe_json(OUT)
    dur = float(data["format"]["duration"])
    video = next(s for s in data["streams"] if s["codec_type"] == "video")
    audio = next(s for s in data["streams"] if s["codec_type"] == "audio")
    qc = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v002",
        "source_revision": "v001",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "file": str(OUT).replace("\\", "/"),
        "sha256": sha256(OUT),
        "duration_seconds": dur,
        "runtime_band_pass": 27 * 60 <= dur <= 33 * 60,
        "video": video,
        "audio": audio,
        "render_method": "v001 first cut re-encoded libx264 slow CRF16 with non-beat blackdetect spans lifted; contractual void beat untouched",
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
        "voice_status": "local_sapi_draft_pending_elevenlabs_owner_go",
        "lifted_spans_seconds": LIFT_SPANS,
    }
    QC.parent.mkdir(parents=True, exist_ok=True)
    QC.write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest_path = EPDIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["state"] = "first_cut_ready_v002_voice_draft"
    manifest.setdefault("active_revisions", {})["final_render"] = "v002"
    manifest.setdefault("active_revisions", {})["final_qc"] = "v002"
    artifacts = manifest.setdefault("artifacts", [])
    for aid in ["PD-2026-017-onecoin-final-render-v002", "PD-2026-017-onecoin-final-qc-v002"]:
        artifacts[:] = [a for a in artifacts if a.get("artifact_id") != aid]
    artifacts.append({"artifact_id": "PD-2026-017-onecoin-final-render-v002", "artifact_type": "final_render", "revision": "v002", "uri": "artifact://E:/pd-media/episodes/PD-2026-017-onecoin/07_edit/v002.mp4", "checksum": sha256(OUT), "status": "candidate", "rights_status": "conditional", "qc_status": "draft_voice"})
    artifacts.append({"artifact_id": "PD-2026-017-onecoin-final-qc-v002", "artifact_type": "final_render_qc", "revision": "v002", "uri": "artifact://episodes/PD-2026-017-onecoin/08_edit/renders/final.v002.qc.json", "checksum": sha256(QC), "status": "candidate", "rights_status": "conditional", "qc_status": "pass"})
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    with EVENTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "episode_id": EP, "stage": "render", "event": "first_cut_render_corrected_black_v002", "revision": "v002", "actor": "codex", "note": "Created v002 from v001 by lifting non-beat blackdetect spans only. Void silence beat left black. No upload/publish/schedule."}, ensure_ascii=False) + "\n")
    print(json.dumps({"render": str(OUT), "sha256": sha256(OUT), "duration": dur}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
