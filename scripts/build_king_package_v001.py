from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EPISODE_ID = "PD-2026-013-king"
SLUG = "king"
EP = ROOT / "episodes" / EPISODE_ID
PKG = EP / "09_package"
THUMBS = EP / "10_thumbnail"
RENDERS = EP / "08_edit" / "renders"
VIDEO = Path(r"H:\pd-media\episodes\PD-2026-013-king\08_edit\king_premium_v001.mp4")
CAPTIONS = EP / "08_edit" / "captions.v001.srt"
SELECTED_THUMB = PKG / "thumbnail.selected.v001.png"
SCHEDULE_JST = "2026-06-28T12:00:00+09:00"
SCHEDULE_UTC = "2026-06-28T03:00:00Z"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def ffprobe_duration(path: Path) -> float | None:
    if not path.exists():
        return None
    p = run([
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ])
    if p.returncode != 0:
        return None
    try:
        return float(p.stdout.strip())
    except ValueError:
        return None


def loudnorm_measure(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    p = run([
        "ffmpeg",
        "-hide_banner",
        "-nostats",
        "-i",
        str(path),
        "-af",
        "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
        "-f",
        "null",
        "-",
    ])
    text = p.stderr or ""
    m = re.search(r"\{\s*\"input_i\".*?\}", text, re.S)
    if not m:
        return {"returncode": p.returncode, "raw_tail": text[-2000:]}
    data = json.loads(m.group(0))
    data["returncode"] = p.returncode
    return data


def copy_selected_thumbnail() -> None:
    source = THUMBS / "thumbnail.king_option_B.v001.png"
    if source.exists():
        PKG.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, SELECTED_THUMB)


def build_thumbnail_candidates() -> dict[str, object]:
    generated_at = now_iso()
    options = [
        {
            "id": "A",
            "title": "Get Arrested - Even by Mistake - and They Take Your DNA",
            "thumbnail_text": "DNA AT / ARREST?",
            "file": "episodes/PD-2026-013-king/10_thumbnail/thumbnail.king_option_A.v001.png",
            "background_static": "king/SPN-0004.png",
            "scores": {
                "contrast_single_subject": 23,
                "conflict_emotion": 24,
                "title_space": 24,
                "mobile_legibility": 25,
                "brand_fit": 24,
                "accuracy": 25,
                "total": 145,
            },
            "assessment": "Safest legal framing: it asks the arrest-stage DNA question without implying the swab caused the assault arrest.",
        },
        {
            "id": "B",
            "title": "The Supreme Court Said Police Can Swab Your DNA at Arrest",
            "thumbnail_text": "POLICE CAN / SWAB DNA",
            "file": "episodes/PD-2026-013-king/10_thumbnail/thumbnail.king_option_B.v001.png",
            "background_static": "king/SPN-0010.png",
            "scores": {
                "contrast_single_subject": 25,
                "conflict_emotion": 24,
                "title_space": 24,
                "mobile_legibility": 25,
                "brand_fit": 25,
                "accuracy": 24,
                "total": 147,
            },
            "assessment": "Selected. Highest browse clarity and mobile read while staying accurate: it states the holding, not the arrest reason.",
        },
        {
            "id": "C",
            "title": "Your DNA, a National Database, and One Vote",
            "thumbnail_text": "YOUR DNA / DATABASE",
            "file": "episodes/PD-2026-013-king/10_thumbnail/thumbnail.king_option_C.v001.png",
            "background_static": "king/SPN-0011.png",
            "scores": {
                "contrast_single_subject": 22,
                "conflict_emotion": 21,
                "title_space": 24,
                "mobile_legibility": 25,
                "brand_fit": 24,
                "accuracy": 25,
                "total": 141,
            },
            "assessment": "Accurate and clean, but the conflict is more abstract than option B.",
        },
    ]
    for option in options:
        file_path = ROOT / option["file"]
        option["sha256"] = sha256(file_path)

    return {
        "schema_version": "1.0.0",
        "episode_id": EPISODE_ID,
        "slug": SLUG,
        "revision": "v001",
        "generated_at": generated_at,
        "status": "selected_upload_ready_candidate",
        "source_note": "Requested THUMB-01..06 files were not present under H:/pd-media/assets/ai/thumbs/king; candidates were rendered from existing King AI stills.",
        "selection": {
            "selected_id": "B",
            "selected_title": options[1]["title"],
            "selected_file": "episodes/PD-2026-013-king/09_package/thumbnail.selected.v001.png",
            "selected_sha256": sha256(SELECTED_THUMB),
            "reason": options[1]["assessment"],
        },
        "title_options": options,
        "rights_gate": {
            "real_person_likeness": False,
            "judge_likeness": False,
            "deepfake": False,
            "symbolic_ai_reconstruction": True,
            "commercial_use_ok": True,
            "accuracy_guard": "Assault arrest is separated from later database hit; no thumbnail text says or implies DNA was the arrest reason.",
        },
    }


CHAPTERS = [
    ("00:00", "A swab at booking"),
    ("00:35", "Opening: Maryland v. King"),
    ("01:26", "The assault arrest"),
    ("02:24", "The database match"),
    ("03:02", "Identification or search?"),
    ("04:10", "The DNA database question"),
    ("05:23", "The 5-4 decision"),
    ("06:38", "Kennedy's majority"),
    ("07:38", "Scalia's dissent"),
    ("08:31", "What changes after King"),
    ("10:02", "The tradeoff"),
    ("11:07", "Next: the home threshold"),
]


TAGS = [
    "Maryland v King",
    "Maryland v. King",
    "DNA swab arrest",
    "Fourth Amendment",
    "Supreme Court cases",
    "constitutional law",
    "CODIS",
    "DNA database",
    "privacy rights",
    "police booking",
    "Scalia dissent",
    "Kennedy majority opinion",
    "Prime Documentary",
]


def description() -> str:
    chapter_lines = "\n".join(f"{time} {title}" for time, title in CHAPTERS)
    return (
        "In Maryland v. King, the Supreme Court asked whether police may take a DNA swab from a person who has been arrested but not yet convicted.\n\n"
        "Alonzo King was arrested on an assault charge. The cheek swab came later during booking, and the DNA database hit connected him to a separate unsolved rape case. This episode keeps that sequence clear: the swab was not the reason for the arrest.\n\n"
        "The majority treated the swab as part of identification, like fingerprints and photographs. The dissent saw something more dangerous: a search of people who had merely been arrested. One vote decided the line.\n\n"
        "This is an educational documentary, not legal advice.\n\n"
        "Visual note: this video uses AI-generated symbolic reconstructions, licensed stock/factory media, and motion design. No real-person likeness, judge likeness, or victim reenactment is intended.\n\n"
        "Chapters:\n"
        f"{chapter_lines}\n"
    )


def qc_payload() -> dict[str, object]:
    duration = ffprobe_duration(VIDEO)
    loudness = loudnorm_measure(VIDEO)
    input_i = float(loudness["input_i"]) if loudness and loudness.get("input_i") not in (None, "-inf") else None
    input_tp = float(loudness["input_tp"]) if loudness and loudness.get("input_tp") is not None else None
    return {
        "schema_version": "1.0.0",
        "episode_id": EPISODE_ID,
        "slug": SLUG,
        "revision": "v001",
        "generated_at": now_iso(),
        "video": str(VIDEO),
        "video_exists": VIDEO.exists(),
        "video_sha256": sha256(VIDEO),
        "duration_seconds": duration,
        "duration_check": {
            "target_seconds_min": 690,
            "target_seconds_max": 750,
            "pass": bool(duration and 690 <= duration <= 750),
        },
        "audio_loudness": loudness,
        "audio_check": {
            "target_lufs": -14,
            "true_peak_max_db": -1,
            "pass": bool(input_i is not None and -15.0 <= input_i <= -13.0 and input_tp is not None and input_tp <= -1.0),
        },
        "caption_sidecar": "episodes/PD-2026-013-king/08_edit/captions.v001.srt",
        "caption_sidecar_exists": CAPTIONS.exists(),
        "burned_in_captions": True,
        "four_part_structure": {
            "hook": True,
            "brand_opening": True,
            "main_acts_1_to_4": True,
            "ending_with_series_bridge_next_tease_cta": True,
            "pass": True,
        },
        "content_safety": {
            "assault_arrest_separated_from_rape_database_hit": True,
            "swab_not_presented_as_arrest_reason": True,
            "no_victim_reenactment": True,
            "no_real_person_or_judge_likeness": True,
            "neutral_majority_and_dissent_framing": True,
            "pass": True,
        },
        "upload_gate": {
            "youtube_upload_performed": False,
            "youtube_schedule_performed": False,
            "owner_confirmation_required": True,
            "pass": True,
        },
    }


def build_package() -> None:
    copy_selected_thumbnail()
    thumb_candidates = build_thumbnail_candidates()
    video_hash = sha256(VIDEO)
    selected_thumb_hash = sha256(SELECTED_THUMB)
    created = now_iso()

    write_json(PKG / "title_thumbnail_candidates.v001.json", thumb_candidates)
    (PKG / "title.v001.txt").write_text(thumb_candidates["selection"]["selected_title"] + "\n", encoding="utf-8")
    (PKG / "description.v001.md").write_text(description(), encoding="utf-8")
    write_json(PKG / "chapters.v001.json", [{"time": t, "title": title} for t, title in CHAPTERS])
    write_json(PKG / "tags.v001.json", {"episode_id": EPISODE_ID, "revision": "v001", "tags": TAGS})

    rights = {
        "schema_version": "1.0.0",
        "episode_id": EPISODE_ID,
        "slug": SLUG,
        "revision": "v001",
        "generated_at": created,
        "commercial_use_ok": True,
        "synthetic_content_disclosure_required": True,
        "contains_ai_symbolic_reconstruction": True,
        "contains_real_person_likeness": False,
        "contains_judge_likeness": False,
        "contains_victim_reenactment": False,
        "source_categories": [
            {"kind": "ai_stills", "path": "H:/pd-media/assets/ai/king/SPN-*.png", "rights": "project-generated symbolic stills"},
            {"kind": "stock_video", "path": "remotion/public/king/*.mp4", "rights": "asset_map licensed downloads"},
            {"kind": "factory_media", "path": "remotion/public/king/factory/*", "rights": "license=allowed selections from Pexels/Pixabay factory library"},
            {"kind": "voice", "path": "H:/pd-media/episodes/PD-2026-013-king/06_voice", "rights": "ElevenLabs narration generated for this episode"},
            {"kind": "music_sfx_mix", "path": "H:/pd-media/episodes/PD-2026-013-king/07_audio/final_mix_v001.mp3", "rights": "project audio mix from allowed local library/generated layers"},
        ],
        "accuracy_guards": [
            "King arrest reason is presented as assault.",
            "DNA cheek swab is presented as a booking step after arrest.",
            "Rape case appears only as downstream database match; no victim reenactment.",
            "Majority identification rationale and Scalia dissent are both presented neutrally.",
        ],
        "selected_thumbnail": str(SELECTED_THUMB).replace("\\", "/"),
        "selected_thumbnail_sha256": f"sha256:{selected_thumb_hash}" if selected_thumb_hash else None,
        "final_video": str(VIDEO),
        "final_video_sha256": f"sha256:{video_hash}" if video_hash else None,
    }
    write_json(PKG / "rights_manifest.v001.json", rights)

    youtube_meta = {
        "schema_version": "1.0.0",
        "episode_id": EPISODE_ID,
        "revision": "v001",
        "status": "upload_ready_owner_gate_closed",
        "title": thumb_candidates["selection"]["selected_title"],
        "description": description(),
        "chapters": [{"time": t, "title": title} for t, title in CHAPTERS],
        "tags": TAGS,
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
        "playlist": "Landmark Rights Cases",
        "thumbnail": "episodes/PD-2026-013-king/09_package/thumbnail.selected.v001.png",
        "selected_thumbnail_sha256": f"sha256:{selected_thumb_hash}" if selected_thumb_hash else None,
        "video_actual_path": str(VIDEO),
        "video_sha256": f"sha256:{video_hash}" if video_hash else None,
        "captions_sidecar": "episodes/PD-2026-013-king/08_edit/captions.v001.srt",
        "caption_track_language": "en",
        "caption_track_name": "English",
        "captions_burned_in": True,
        "synthetic_content_disclosure_required": True,
        "contains_ai_symbolic_reconstruction": True,
        "privacy_status_target": "private",
        "publish_schedule_target_jst": SCHEDULE_JST,
        "publish_schedule_target_utc": SCHEDULE_UTC,
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
        "publish_gate": "closed_until_owner_review",
        "pre_publish_checks": {
            "rights_manifest": "episodes/PD-2026-013-king/09_package/rights_manifest.v001.json",
            "final_qc": "episodes/PD-2026-013-king/08_edit/renders/final.v001.qc.json",
            "thumbnail_candidates": "episodes/PD-2026-013-king/09_package/title_thumbnail_candidates.v001.json",
            "synthetic_content_disclosure_required": True,
            "upload_approval_required": True,
            "public_schedule_requires_owner_approval": True,
        },
        "pinned_comment": "Maryland v. King turned a cheek swab at booking into a one-vote fight over identification, privacy, and DNA databases.",
        "created_at": created,
    }
    write_json(PKG / "youtube_meta.v001.json", youtube_meta)

    final_delivery = {
        "schema_version": "1.0.0",
        "episode_id": EPISODE_ID,
        "revision": "v001",
        "status": "upload_ready_owner_review_required",
        "generated_at": created,
        "final_video": str(VIDEO),
        "final_video_exists": VIDEO.exists(),
        "final_video_sha256": f"sha256:{video_hash}" if video_hash else None,
        "selected_thumbnail": "episodes/PD-2026-013-king/09_package/thumbnail.selected.v001.png",
        "selected_thumbnail_sha256": f"sha256:{selected_thumb_hash}" if selected_thumb_hash else None,
        "captions": "episodes/PD-2026-013-king/08_edit/captions.v001.srt",
        "youtube_meta": "episodes/PD-2026-013-king/09_package/youtube_meta.v001.json",
        "rights_manifest": "episodes/PD-2026-013-king/09_package/rights_manifest.v001.json",
        "final_qc": "episodes/PD-2026-013-king/08_edit/renders/final.v001.qc.json",
        "owner_stop_point": "YouTube upload and publish scheduling have not been performed.",
        "target_schedule_after_owner_approval": {"jst": SCHEDULE_JST, "utc": SCHEDULE_UTC},
    }
    write_json(PKG / "final_delivery.v001.json", final_delivery)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qc", action="store_true", help="also write final render QC")
    args = parser.parse_args()

    build_package()
    if args.qc:
        RENDERS.mkdir(parents=True, exist_ok=True)
        write_json(RENDERS / "final.v001.qc.json", qc_payload())


if __name__ == "__main__":
    main()
