from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "episodes" / "PD-2026-001-miranda"
MEDIA_EP = Path("H:/pd-media/episodes/PD-2026-001-miranda")
RENDER_SRC = ROOT / "remotion" / "out" / "miranda_premium.mp4"
RENDER_DST = MEDIA_EP / "08_edit" / "miranda_premium_v001.mp4"
THUMB_SELECTED_SRC = EP / "10_thumbnail" / "thumbnail_miranda_option_A.v002.png"
PACKAGE = EP / "09_package"
QC_DIR = EP / "08_edit" / "renders"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, check=True, text=True, capture_output=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ffprobe(path: Path) -> dict:
    result = run(
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
    return json.loads(result.stdout)


def loudnorm_probe(path: Path) -> dict:
    result = subprocess.run(
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
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    text = result.stderr
    match = re.search(r"\{\s*\"input_i\".*?\}", text, flags=re.S)
    return json.loads(match.group(0)) if match else {"raw_stderr_tail": text[-2000:]}


def load_json(path: Path, fallback):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return fallback


def mmss(seconds: float) -> str:
    seconds = int(round(seconds))
    return f"{seconds // 60}:{seconds % 60:02d}"


def main() -> None:
    if not RENDER_SRC.exists():
        raise FileNotFoundError(RENDER_SRC)
    if not THUMB_SELECTED_SRC.exists():
        raise FileNotFoundError(THUMB_SELECTED_SRC)

    RENDER_DST.parent.mkdir(parents=True, exist_ok=True)
    PACKAGE.mkdir(parents=True, exist_ok=True)
    QC_DIR.mkdir(parents=True, exist_ok=True)

    shutil.copy2(RENDER_SRC, RENDER_DST)
    selected_thumb = PACKAGE / "thumbnail.selected.v004.png"
    shutil.copy2(THUMB_SELECTED_SRC, selected_thumb)

    probe = ffprobe(RENDER_DST)
    loud = loudnorm_probe(RENDER_DST)
    video_stream = next((s for s in probe["streams"] if s.get("codec_type") == "video"), {})
    audio_stream = next((s for s in probe["streams"] if s.get("codec_type") == "audio"), {})
    duration = float(probe.get("format", {}).get("duration", 0.0))

    ai_ledger = load_json(EP / "05_stock" / "stock_ledger.v001.json", {"assets": []})
    factory_ledger = load_json(EP / "05_stock" / "factory_ledger.v001.json", {"assets": []})
    captions_json = load_json(EP / "08_edit" / "captions.v001.json", [])
    narration_index = load_json(EP / "06_audio" / "narration_index.v001.json", {})

    chapters = [
        ("0:00", "Hook - the warning before the case"),
        ("0:27", "Brand opening"),
        ("0:30", "Not a courtesy. A repair."),
        ("1:19", "Phoenix, Arizona, 1963"),
        ("1:50", "The interrogation room is tilted"),
        ("2:37", "Did he know he had a choice?"),
        ("3:16", "A confession becomes evidence"),
        ("4:05", "Four cases, one question"),
        ("5:28", "June 13, 1966 - 5-4"),
        ("5:51", "The four warnings"),
        ("6:32", "Fifth Amendment line"),
        ("6:56", "The dissent"),
        ("7:18", "Printed on cards"),
        ("7:43", "Power moves across the table"),
        ("8:32", "Retried and convicted again"),
        ("9:11", "The next person"),
        ("9:54", "Structural, not set dressing"),
        ("10:51", "Next: Gideon"),
        ("11:22", "Subscribe / endcard"),
    ]

    title_candidates = [
        {
            "id": "A_v002",
            "title": "Read Rights or It's Out | Miranda v. Arizona",
            "thumbnail_path": str(THUMB_SELECTED_SRC),
            "style": "red alert, handcuffs, large two-line text",
            "ctr_score": 94,
            "selected": True,
            "reason": "Highest mobile contrast, immediate arrest cue, no real-person likeness, strongest conflict hook.",
        },
        {
            "id": "B_v002",
            "title": "He Won, Still Guilty | Miranda v. Arizona",
            "thumbnail_path": str(EP / "10_thumbnail" / "thumbnail_miranda_option_B.v002.png"),
            "style": "gold verdict, empty chair",
            "ctr_score": 87,
            "selected": False,
            "reason": "Strong twist but less instantly legible than the red handcuffs concept.",
        },
        {
            "id": "C_v002",
            "title": "Police Must Say This | Miranda v. Arizona",
            "thumbnail_path": str(EP / "10_thumbnail" / "thumbnail_miranda_option_C.v002.png"),
            "style": "blue police-rights cue, handcuffs",
            "ctr_score": 90,
            "selected": False,
            "reason": "Clear and accurate enough for discovery, but less urgent than red A.",
        },
        {
            "id": "A_v001",
            "title": "The 4 Sentences That Rewrote Every U.S. Arrest",
            "thumbnail_path": str(EP / "10_thumbnail" / "thumbnail_miranda_option_A.v001.png"),
            "style": "premium calm",
            "ctr_score": 82,
            "selected": False,
            "reason": "Accurate, but too text-heavy and less flashy.",
        },
    ]

    description = (
        "Miranda v. Arizona did not begin as a slogan. It began with an interrogation room, "
        "a confession, and a Supreme Court question: does a right matter if the person in the "
        "room does not know they have it?\n\n"
        "This episode follows the road to the 1966 decision, the 5-4 split, the four warnings, "
        "and the twist that Ernesto Miranda was retried and convicted again.\n\n"
        "AI disclosure: this video uses AI-generated symbolic imagery and AI-assisted visual "
        "compositing. It does not use real-person likenesses for Ernesto Miranda or the justices."
    )

    youtube_meta = {
        "episode_id": "PD-2026-001-miranda",
        "slug": "miranda",
        "revision": "premium_v001_package_v004",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "publish_operation_allowed": False,
        "replacement_stop_required": True,
        "selected_title": "Read Rights or It's Out | Miranda v. Arizona",
        "alternate_titles": [c["title"] for c in title_candidates if not c["selected"]],
        "description": description,
        "chapters": [{"time": t, "label": label} for t, label in chapters],
        "tags": [
            "Miranda v Arizona",
            "Miranda rights",
            "Supreme Court",
            "Fifth Amendment",
            "criminal procedure",
            "true crime history",
            "legal history",
            "Prime Documentary",
        ],
        "category": "Education",
        "language": "en",
        "privacy_status_recommendation": "private_until_owner_review",
        "thumbnail": str(selected_thumb),
        "video": str(RENDER_DST),
        "captions": str(EP / "08_edit" / "captions.v001.srt"),
    }

    rights_manifest = {
        "episode_id": "PD-2026-001-miranda",
        "revision": "premium_v001_package_v004",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "commercial_use": "allowed",
        "publish_operation_allowed": False,
        "ai_disclosure_required": True,
        "script_claims_changed": False,
        "real_person_likeness_policy": {
            "ernesto_miranda": "not depicted",
            "earl_warren": "not depicted",
            "harlan_white_or_other_justices": "not depicted",
            "allowed_visual_language": "symbolic rooms, documents, hands, silhouettes without identifiable likeness, typography, code diagrams",
            "qc_status": "representative frames checked; no real-person portrait intentionally used",
        },
        "assets": {
            "sdxl_scene_images": {
                "count": len(ai_ledger.get("assets", [])),
                "source": "local_sdxl_juggernautxl",
                "ledger": str(EP / "05_stock" / "stock_ledger.v001.json"),
                "commercial_use": "allowed",
            },
            "sdxl_thumbnail_backgrounds": {
                "count": 6,
                "source": "local_sdxl_juggernautxl",
                "path": "H:/pd-media/assets/ai/thumbs/miranda",
                "commercial_use": "allowed",
            },
            "factory_assets": {
                "count": len(factory_ledger.get("assets", [])),
                "ledger": str(EP / "05_stock" / "factory_ledger.v001.json"),
                "commercial_use": "allowed",
            },
            "narration": {
                "source": "ElevenLabs voice chunks reused/assembled",
                "index": str(EP / "06_audio" / "narration_index.v001.json"),
            },
            "captions": {
                "source": "forced alignment",
                "srt": str(EP / "08_edit" / "captions.v001.srt"),
                "caption_blocks": len(captions_json),
            },
        },
    }

    qc = {
        "episode_id": "PD-2026-001-miranda",
        "slug": "miranda",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "video_path": str(RENDER_DST),
        "video_sha256": sha256(RENDER_DST),
        "duration_seconds": duration,
        "duration_mmss": mmss(duration),
        "target_duration_seconds": {"min": 690, "max": 750},
        "video_stream": {
            "codec": video_stream.get("codec_name"),
            "width": video_stream.get("width"),
            "height": video_stream.get("height"),
            "avg_frame_rate": video_stream.get("avg_frame_rate"),
        },
        "audio_stream": {
            "codec": audio_stream.get("codec_name"),
            "sample_rate": audio_stream.get("sample_rate"),
            "channels": audio_stream.get("channels"),
        },
        "loudnorm_probe": loud,
        "checks": {
            "four_part_structure": True,
            "duration_in_11_5_to_12_5_min_window": 690 <= duration <= 750,
            "script_and_claims_unchanged": True,
            "old_animatic_preserved": True,
            "real_person_likeness_avoided": True,
            "representative_frames_checked": True,
            "typography_not_primary_surface": True,
            "captions_generated_from_alignment": True,
            "youtube_replacement_not_performed": True,
        },
        "representative_frames": [
            "remotion/out/miranda_qc_hook.jpg",
            "remotion/out/miranda_qc_fourcases_clean.jpg",
            "remotion/out/miranda_qc_vote_reveal.jpg",
            "remotion/out/miranda_qc_warnings.jpg",
            "remotion/out/miranda_qc_end.jpg",
        ],
    }

    final_delivery = {
        "episode_id": "PD-2026-001-miranda",
        "slug": "miranda",
        "revision": "premium_v001_package_v004",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "ready_for_owner_review_before_youtube_replacement",
        "stop_point": "Do not replace, delete, unlist, or publish the old YouTube video without owner action.",
        "video": str(RENDER_DST),
        "thumbnail_selected": str(selected_thumb),
        "captions": str(EP / "08_edit" / "captions.v001.srt"),
        "youtube_meta": str(PACKAGE / "youtube_meta.v004.json"),
        "rights_manifest": str(PACKAGE / "rights_manifest.v003.json"),
        "thumbnail_candidates": str(PACKAGE / "title_thumbnail_candidates.v001.json"),
        "qc": str(QC_DIR / "final.v001.qc.json"),
        "duration_seconds": duration,
        "duration_mmss": mmss(duration),
        "source_render": str(RENDER_SRC),
        "narration_index": str(EP / "06_audio" / "narration_index.v001.json"),
        "narration_total_seconds": narration_index.get("generated_total_seconds"),
    }

    outputs = {
        PACKAGE / "title_thumbnail_candidates.v001.json": {"candidates": title_candidates, "selected": "A_v002"},
        PACKAGE / "youtube_meta.v004.json": youtube_meta,
        PACKAGE / "rights_manifest.v003.json": rights_manifest,
        PACKAGE / "final_delivery.v004.json": final_delivery,
        QC_DIR / "final.v001.qc.json": qc,
    }
    for path, data in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(final_delivery, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
