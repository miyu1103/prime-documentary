#!/usr/bin/env python
"""Resolve EP23 sensitive-lock blockers without paid API calls or publishing.

This keeps the existing ElevenLabs recording and removes the duplicate opening
suicide wording by muting that sentence inside SPN-0007. It also replaces the
caption-only unqualified "thirty-five years" cues with safer contextual text.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_ep23_swartz_final as ep23  # noqa: E402

EP = "PD-2026-023-swartz"
EPDIR = ROOT / "episodes" / EP
MEDIA = Path("H:/pd-media/episodes") / EP
MASTER_DIR = MEDIA / "06_audio" / "master_elevenlabs_v001"
SPN7 = MASTER_DIR / "wav" / "SPN-0007.wav"
VOICE_MASTER = MASTER_DIR / "voice_master.v001.wav"
CONCAT = MEDIA / "08_edit" / "_build_v001" / "voice_concat.txt"
FINAL_MP4 = MEDIA / "08_edit" / "final.mp4"
MIX_WAV = MEDIA / "08_edit" / "swartz_final_mix.v001.wav"
CAPTIONS_SRT = EPDIR / "08_edit" / "captions.v001.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / "captions.v001.json"
NARRATION_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
VOICE_META = EPDIR / "06_audio" / "voice_master.v001.json"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"
PKG = EPDIR / "09_package"

MUTE_START = 2.229667
MUTE_END = 5.304500
SAFE_SPN7_TEXT = (
    "One honest note before we begin. We are going to state that fact a single "
    "time, and with care, and we are not going to dwell on it or dramatize it. "
    "If you are struggling while you watch this, the number on your screen can "
    "help, any time of the day or night. Please use it."
)

CAPTION_REPLACEMENTS = {
    571: "The theoretical maximum was the headline number.",
    583: "somewhere around that theoretical ceiling",
    604: "of that figure wildly overstated",
}
CAPTION_DROP = {91, 92}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return "sha256:" + h.hexdigest()


def run(cmd: list[str | Path], label: str, timeout: int | None = None) -> None:
    print(f"== {label}", flush=True)
    subprocess.run([str(x) for x in cmd], cwd=ROOT, check=True, timeout=timeout)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def backup(paths: list[Path]) -> tuple[Path, Path]:
    media_backup = MEDIA / "_backup" / f"safe_handling_fix_{stamp()}"
    repo_backup = PKG / "EVIDENCE" / media_backup.name
    media_backup.mkdir(parents=True, exist_ok=True)
    repo_backup.mkdir(parents=True, exist_ok=True)
    for path in paths:
        if not path.exists():
            continue
        target_root = media_backup if str(path).lower().startswith(str(MEDIA).lower()) else repo_backup
        rel = path.relative_to(MEDIA) if target_root == media_backup else path.relative_to(EPDIR)
        dst = target_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dst)
    return media_backup, repo_backup


def mute_duplicate_opening_sentence() -> None:
    tmp = SPN7.with_suffix(".safe.tmp.wav")
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            SPN7,
            "-af",
            f"volume=enable='between(t,{MUTE_START:.6f},{MUTE_END:.6f})':volume=0",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            tmp,
        ],
        "mute duplicate suicide sentence in SPN-0007",
    )
    tmp.replace(SPN7)


def rebuild_voice_master() -> None:
    run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", CONCAT, "-c:a", "pcm_s16le", VOICE_MASTER],
        "rebuild EP23 voice master from existing chunks",
        timeout=7200,
    )


def parse_srt(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    cues: list[dict] = []
    for block in blocks:
        lines = block.splitlines()
        if len(lines) < 3 or "-->" not in lines[1]:
            continue
        cues.append({"index": int(lines[0]), "timing": lines[1], "text": "\n".join(lines[2:])})
    return cues


def write_srt(path: Path, cues: list[dict]) -> None:
    out = []
    for idx, cue in enumerate(cues, start=1):
        out.append(f"{idx}\n{cue['timing']}\n{cue['text']}\n")
    path.write_text("\n".join(out), encoding="utf-8")


def update_captions() -> None:
    cues = []
    for cue in parse_srt(CAPTIONS_SRT):
        old_index = cue["index"]
        if old_index in CAPTION_DROP:
            continue
        if old_index in CAPTION_REPLACEMENTS:
            cue["text"] = CAPTION_REPLACEMENTS[old_index]
        cues.append(cue)
    write_srt(CAPTIONS_SRT, cues)

    if CAPTIONS_JSON.exists():
        data = load_json(CAPTIONS_JSON)
        new_cues = []
        for cue in data.get("cues", []):
            old_index = int(cue.get("index", 0))
            if old_index in CAPTION_DROP:
                continue
            if old_index in CAPTION_REPLACEMENTS:
                cue["text"] = CAPTION_REPLACEMENTS[old_index]
            new_cues.append(cue)
        for idx, cue in enumerate(new_cues, start=1):
            cue["index"] = idx
        data["cues"] = new_cues
        data["safe_handling_fix"] = {
            "applied_at": now(),
            "caption_drop_original_indices": sorted(CAPTION_DROP),
            "caption_replacements_original_indices": sorted(CAPTION_REPLACEMENTS),
        }
        write_json(CAPTIONS_JSON, data)


def update_audio_metadata() -> None:
    for path in [NARRATION_INDEX, VOICE_META]:
        data = load_json(path)
        chunks = data.get("chunks", [])
        for chunk in chunks:
            if chunk.get("span_id") == "SPN-0007":
                chunk["text"] = SAFE_SPN7_TEXT
                chunk["safe_handling_audio_edit"] = {
                    "kind": "muted_duplicate_sentence",
                    "mute_start_seconds_in_chunk": MUTE_START,
                    "mute_end_seconds_in_chunk": MUTE_END,
                    "external_paid_call": False,
                    "reason": "Keep suicide wording only once, in SPN-0038.",
                }
        data["safe_handling_fix"] = {
            "applied_at": now(),
            "external_paid_call": False,
            "voice_master_sha256": sha256_file(VOICE_MASTER) if VOICE_MASTER.exists() else None,
        }
        write_json(path, data)


def update_manifest_and_events(media_backup: Path, repo_backup: Path, final_sha: str) -> None:
    manifest = load_json(MANIFEST)
    manifest["state"] = "edit_review"
    manifest["updated_at"] = now()
    manifest["blockers"] = []
    warnings = manifest.setdefault("warnings", [])
    note = (
        "EP23 safe-handling fix applied locally: duplicate opening suicide wording "
        "muted from existing ElevenLabs chunk; captions adjusted so 35-years text "
        "is not shown unqualified. No paid API, upload, scheduling, or publish."
    )
    if note not in warnings:
        warnings.append(note)
    manifest.setdefault("active_revisions", {})["captions"] = "v001"
    manifest.setdefault("active_revisions", {})["audio_mix"] = "v001"
    manifest.setdefault("active_revisions", {})["edit"] = "v001"
    write_json(MANIFEST, manifest)

    event = {
        "ts": now(),
        "episode_id": EP,
        "event": "safe_handling_fix_applied",
        "by": "codex",
        "revision": "v001",
        "external_paid_call": False,
        "final_video": str(FINAL_MP4).replace("\\", "/"),
        "final_video_sha256": final_sha,
        "media_backup": str(media_backup).replace("\\", "/"),
        "repo_backup": str(repo_backup).replace("\\", "/"),
        "resolved": [
            "duplicate suicide wording removed from opening audio/captions",
            "unqualified 35-years caption text removed from burned captions",
        ],
    }
    with EVENTS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def write_resolution_report(media_backup: Path, repo_backup: Path, final_sha: str) -> None:
    report = {
        "episode_id": EP,
        "status": "safe_handling_resolved_pending_independent_qc",
        "created_at": now(),
        "external_paid_call": False,
        "changes": [
            {
                "surface": "audio",
                "detail": f"Muted SPN-0007 {MUTE_START:.3f}-{MUTE_END:.3f}s to remove duplicate opening suicide wording.",
            },
            {
                "surface": "captions",
                "detail": "Dropped original cues 91-92 and replaced original cues 571/583/604 with safer non-standalone wording.",
            },
            {
                "surface": "final_video",
                "detail": "Rebuilt audio mix and remuxed existing silent motion video with refreshed burned captions.",
            },
        ],
        "final_video": str(FINAL_MP4).replace("\\", "/"),
        "final_video_sha256": final_sha,
        "media_backup": str(media_backup).replace("\\", "/"),
        "repo_backup": str(repo_backup).replace("\\", "/"),
        "publish_boundary": "No upload, scheduling, visibility change, or public release performed.",
    }
    write_json(PKG / "SAFE_HANDLING_RESOLUTION.v001.json", report)
    md = "\n".join(
        [
            "# EP23 Safe-Handling Resolution",
            "",
            f"Created: {report['created_at']}",
            "",
            "Status: resolved locally; independent QC still required.",
            "",
            "- External paid calls: no",
            "- Upload/publish/scheduling: no",
            "- Audio: muted duplicate opening suicide wording in SPN-0007.",
            "- Captions: removed the duplicate suicide cue and removed unqualified 35-years captions.",
            f"- Final video: `{report['final_video']}`",
            f"- Final SHA-256: `{final_sha}`",
            f"- Media backup: `{report['media_backup']}`",
            f"- Repo backup: `{report['repo_backup']}`",
            "",
        ]
    )
    (PKG / "SAFE_HANDLING_RESOLUTION.v001.md").write_text(md, encoding="utf-8")


def main() -> int:
    required = [SPN7, VOICE_MASTER, CONCAT, MIX_WAV, FINAL_MP4, CAPTIONS_SRT, NARRATION_INDEX, VOICE_META, MANIFEST]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise SystemExit(f"Missing required inputs: {missing}")

    media_backup, repo_backup = backup(
        [
            SPN7,
            VOICE_MASTER,
            MIX_WAV,
            FINAL_MP4,
            CAPTIONS_SRT,
            CAPTIONS_JSON,
            EPDIR / "08_edit" / "captions.v001.burn.ass",
            NARRATION_INDEX,
            VOICE_META,
            MANIFEST,
            EVENTS,
            PKG / "final_delivery.v001.json",
        ]
    )

    mute_duplicate_opening_sentence()
    rebuild_voice_master()
    update_audio_metadata()
    update_captions()
    total = ep23.build_mix()
    ep23.burn_and_mux(total)
    ep23.write_final_delivery(total)
    final_sha = sha256_file(FINAL_MP4)
    update_manifest_and_events(media_backup, repo_backup, final_sha)
    write_resolution_report(media_backup, repo_backup, final_sha)

    print(
        json.dumps(
            {
                "status": "safe_handling_fix_applied",
                "external_paid_call": False,
                "final_video": str(FINAL_MP4).replace("\\", "/"),
                "final_video_sha256": final_sha,
                "media_backup": str(media_backup).replace("\\", "/"),
                "repo_backup": str(repo_backup).replace("\\", "/"),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
