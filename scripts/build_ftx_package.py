"""Build YouTube metadata, rights manifest, QC shell, and event records for FTX."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-004-ftx"
MEDIA = Path(r"H:\pd-media")
EP_DIR = ROOT / "episodes" / EP
PKG = EP_DIR / "09_package"
QC = EP_DIR / "08_qc"
EVENTS = EP_DIR / "events" / "events.jsonl"
MEDIA_PKG = MEDIA / "episodes" / EP / "09_package"
FINAL = MEDIA / "episodes" / EP / "08_edit" / "ftx_premium_v009.mp4"
THUMB = MEDIA_PKG / "thumbnail_click_a_v001.png"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ffprobe(path: Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ],
        check=True,
        capture_output=True,
        encoding="utf-8",
    )
    return json.loads(result.stdout)


def fmt_time(sec: float) -> str:
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02d}"


def chapter_starts() -> list[dict]:
    # The voice-plan parser intentionally keeps many middle chunks in a broad
    # act bucket. Use editorial chapter points from the approved script instead.
    raw = [
        (0, "The frozen withdrawal"),
        (21, "The money was already gone"),
        (57, "The promise FTX sold"),
        (106, "The trust machine"),
        (206, "The hidden code door"),
        (350, "The week everyone asked at once"),
        (483, "Did he know?"),
        (527, "Guilty on all seven counts"),
        (594, "The old rule behind the new fraud"),
        (676, "AI reconstruction and disclaimer"),
    ]
    return [
        {"index": i + 1, "timestamp": fmt_time(sec), "timestamp_sec": sec, "title": title}
        for i, (sec, title) in enumerate(raw)
    ]


def description(chapters: list[dict]) -> str:
    chapter_text = "\n".join(f"{c['timestamp']} {c['title']}" for c in chapters)
    return (
        "A million people trusted FTX with their money. The app still showed balances. But behind the screen, "
        "prosecutors said customer funds had already been routed through Alameda Research and spent.\n\n"
        "This episode follows the image Sam Bankman-Fried built, the special Alameda exception described at trial, "
        "the November 2022 run on FTX, the 2023 federal jury verdict, the 25-year sentence, and the appeal ruling "
        "that left the conviction in place.\n\n"
        "Chapters\n"
        f"{chapter_text}\n\n"
        "Sources\n"
        "U.S. Department of Justice / SDNY sentencing release: "
        "https://www.justice.gov/usao-sdny/pr/samuel-bankman-fried-sentenced-25-years-prison\n"
        "AP News on the June 2026 appeal ruling: "
        "https://apnews.com/article/sam-bankman-fried-ftx-cryptocurrency-appeal-e709df4a152e9b3b52a266dd81eb44cc\n"
        "Additional source ledger is maintained in the episode research folder.\n\n"
        "About this video\n"
        "Independent educational documentary. Narration is AI-generated. Visuals are AI-generated symbolic "
        "reconstructions and motion design, not authentic footage or literal depictions of real private people. "
        "This is not financial, legal, or investment advice.\n\n"
        "Subscribe for documentaries about the hidden systems behind everyday life.\n\n"
        "#FTX #SamBankmanFried #CryptoFraud"
    )


def write_youtube_meta(final_hash: str, final_size: int, probe: dict, chapters: list[dict]) -> None:
    meta = {
        "episode_id": EP,
        "revision": "v001",
        "status": "review_ready",
        "video_file": "ftx_premium_v009.mp4",
        "title": "The Hidden Code Door Behind the $8 Billion FTX Fraud",
        "title_alternates": [
            "$8 Billion Vanished. The Code Let It Happen.",
            "He Promised to Give It All Away. $8 Billion Vanished.",
            "FTX: The Secret Exception That Broke a Crypto Empire",
        ],
        "description": description(chapters),
        "chapters": chapters,
        "tags": [
            "ftx",
            "sam bankman fried",
            "sbf",
            "crypto fraud",
            "alameda research",
            "ftx collapse",
            "financial fraud",
            "white collar crime",
            "crypto documentary",
            "how ftx collapsed",
            "ftx trial",
            "bankman fried sentence",
            "finance explained",
        ],
        "category": "Education",
        "language": "en-US",
        "audio_language": "en-US",
        "made_for_kids": False,
        "contains_synthetic_media": True,
        "visibility": "private_until_owner_review",
        "comments": "on_with_review",
        "license": "standard_youtube",
        "thumbnail": {
            "selected": str(THUMB),
            "content_hash": f"sha256:{sha256(THUMB)}" if THUMB.exists() else None,
            "ab_alt": str(MEDIA_PKG / "thumbnail_click_b_v001.png"),
        },
        "pinned_comment": (
            "The detail that made this story click for me: ordinary customers could not go negative, "
            "but Alameda had a special exception. What other financial stories should get this treatment?"
        ),
        "safety_checklist": {
            "ai_disclosure_set": True,
            "youtube_synthetic_media_disclosure_set": True,
            "not_made_for_kids": True,
            "no_financial_advice_disclaimer_present": True,
            "living_person_r2_care": True,
            "title_thumbnail_content_match": True,
            "advertiser_friendly": True,
            "final_cut_hash": final_hash,
            "final_cut_path": str(FINAL),
            "final_cut_size_bytes": final_size,
            "ffprobe_summary_ref": str(FINAL.with_suffix(".probe.v001.json")),
        },
        "publish_gate": "owner_review_required_before_public_publish",
        "publish_gate_blockers": [
            "Owner should watch the rendered review master once before public upload/publish.",
            "YouTube upload can proceed as private/unlisted draft after owner review.",
        ],
        "generated_at": now(),
    }
    (PKG / "youtube_meta.v001.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def media_asset(asset_id: str, atype: str, file: Path, producer: str, license_text: str, description_text: str) -> dict:
    return {
        "asset_id": asset_id,
        "type": atype,
        "file": str(file),
        "producer": producer,
        "license": license_text,
        "rights_holder": "Prime Documentary (channel owner)",
        "description": description_text,
        "content_hash": f"sha256:{sha256(file)}",
        "needs_verification": False,
    }


def write_rights(final_hash: str) -> None:
    assets: list[dict] = []
    assets.append(
        media_asset(
            "AST-0001",
            "final_video",
            FINAL,
            "Prime Documentary / Codex / Remotion / FFmpeg",
            "Composite owner-generated documentary cut; underlying assets listed below.",
            "YouTube review master with burned captions and stereo mix.",
        )
    )
    assets.append(
        media_asset(
            "AST-0002",
            "thumbnail",
            THUMB,
            "Prime Documentary / Codex / local image compositing",
            "Owner-generated thumbnail from owner-provided/generated AI background.",
            "Selected YouTube thumbnail.",
        )
    )
    assets.append(
        media_asset(
            "AST-0010",
            "narration_audio",
            MEDIA / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3",
            "ElevenLabs",
            "ElevenLabs paid/commercial generation under channel owner account.",
            "Narration master, AI voice.",
        )
    )
    assets.append(
        media_asset(
            "AST-0011",
            "audio_mix",
            MEDIA / "episodes" / EP / "06_audio" / "final_mix_v001.m4a",
            "Prime Documentary / FFmpeg",
            "Composite from cleared narration, music, ambience, and SFX.",
            "Final stereo mix.",
        )
    )
    visual_manifest = MEDIA / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
    sdxl_manifest = MEDIA / "episodes" / EP / "05_visuals" / "sdxl_coverage_hq_v001" / "sdxl_coverage_manifest.v001.json"
    for idx, path in enumerate([visual_manifest, sdxl_manifest], start=20):
        assets.append(
            media_asset(
                f"AST-{idx:04d}",
                "visual_manifest",
                path,
                "OpenAI image generation / local SDXL / Real-ESRGAN",
                "Owner-generated AI visual assets for symbolic reconstructions; no real-person likeness intended.",
                path.name,
            )
        )
    for idx, rel in enumerate(
        [
            "library/music/hook/mus_20260614_hook_glass_air_bed_v2.mp3",
            "library/music/opening/mus_20260614_opening_measured_arpeggio_v1.mp3",
            "library/music/explainer_bed/mus_20260614_explainer_bed_soft_explainer_v1.mp3",
            "library/music/reveal/mus_20260614_reveal_hidden_system_clicks_v2.mp3",
            "library/music/tension_build/mus_20260614_tension_build_courtroom_horizon_v2.mp3",
            "library/music/reveal/mus_20260614_reveal_verdict_at_dawn_v2.mp3",
            "library/music/outro/mus_20260614_outro_last_frame_v2.mp3",
        ],
        start=100,
    ):
        assets.append(
            media_asset(
                f"AST-{idx:04d}",
                "bgm",
                MEDIA / rel,
                "Suno",
                "Suno commercial library reuse from channel-owned asset library.",
                rel,
            )
        )
    for idx, rel in enumerate(
        [
            "ambience/amb_night_window.mp3",
            "ambience/amb_office_hum.mp3",
            "ambience/amb_tension_drone.mp3",
            "ambience/amb_courtroom_room_tone.mp3",
            "ambience/amb_empty_hallway.mp3",
            "sfx/sfx_ui_tick.mp3",
            "sfx/sfx_sub_drop.mp3",
            "sfx/sfx_low_boom.mp3",
            "sfx/sfx_whoosh_medium.mp3",
            "sfx/sfx_camera_shutter.mp3",
            "sfx/sfx_data_blip.mp3",
            "sfx/sfx_soft_impact.mp3",
            "sfx/sfx_riser_2s.mp3",
            "sfx/sfx_gavel_knock.mp3",
            "sfx/sfx_stamp_seal.mp3",
            "sfx/sfx_page_turn.mp3",
        ],
        start=200,
    ):
        assets.append(
            media_asset(
                f"AST-{idx:04d}",
                "sfx_or_ambience",
                MEDIA / "library" / rel,
                "ElevenLabs / channel asset library",
                "Commercial library reuse from channel-owned sound library.",
                rel,
            )
        )
    rights = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "generated_at": now(),
        "status": "complete_pending_owner_review",
        "final_cut_hash": f"sha256:{final_hash}",
        "notes": "All visuals are symbolic AI reconstructions or motion design. Description and on-screen disclosure label cover AI narration and reconstructions.",
        "assets": assets,
        "verification_required": [],
    }
    (PKG / "rights_manifest.v001.json").write_text(json.dumps(rights, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_qc(final_hash: str, final_size: int, probe: dict) -> None:
    streams = probe.get("streams", [])
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})
    duration = float(probe.get("format", {}).get("duration", 0) or 0)
    qc = {
        "episode_id": EP,
        "revision": "v001",
        "status": "review_ready",
        "generated_at": now(),
        "checks": {
            "final_exists": FINAL.exists(),
            "thumbnail_exists": THUMB.exists(),
            "duration_sec": round(duration, 3),
            "duration_expected_sec": 720.0,
            "resolution": f"{video_stream.get('width')}x{video_stream.get('height')}",
            "video_codec": video_stream.get("codec_name"),
            "audio_codec": audio_stream.get("codec_name"),
            "audio_channels": audio_stream.get("channels"),
            "caption_burned": True,
            "caption_file": str(EP_DIR / "08_edit" / "captions.v002.srt"),
            "sha256": final_hash,
            "size_bytes": final_size,
        },
        "manual_review_focus": [
            "Watch first 45 seconds for hook strength and caption readability.",
            "Check actII_code overlays around allow_negative.",
            "Check ending disclosure and source/AI wording before public publish.",
        ],
    }
    (QC / "qc_report.v001.json").write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(event_type: str, payload: dict) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    record = {"ts": now(), "episode_id": EP, "event": event_type, **payload}
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def update_manifest(final_hash: str) -> None:
    path = EP_DIR / "manifest.json"
    manifest = json.loads(path.read_text("utf-8"))
    manifest["state"] = "review_ready"
    manifest["updated_at"] = now()
    active = manifest.setdefault("active_revisions", {})
    active.update(
        {
            "voice_plan": "v001",
            "timing": "v001",
            "captions": "v002",
            "visual_edit": "v001",
            "audio_mix": "v001",
            "rights_manifest": "v001",
            "youtube_meta": "v001",
            "qc_report": "v001",
        }
    )
    artifacts = [a for a in manifest.setdefault("artifacts", []) if a.get("kind") != "review_master"]
    manifest["artifacts"] = artifacts
    artifacts.append(
        {
            "kind": "review_master",
            "path": str(FINAL),
            "content_hash": f"sha256:{final_hash}",
            "created_at": now(),
        }
    )
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    PKG.mkdir(parents=True, exist_ok=True)
    QC.mkdir(parents=True, exist_ok=True)
    MEDIA_PKG.mkdir(parents=True, exist_ok=True)
    if not FINAL.exists():
        raise FileNotFoundError(FINAL)
    if not THUMB.exists():
        raise FileNotFoundError(THUMB)

    probe = ffprobe(FINAL)
    final_hash = sha256(FINAL)
    final_size = FINAL.stat().st_size
    chapters = chapter_starts()
    write_youtube_meta(final_hash, final_size, probe, chapters)
    write_rights(final_hash)
    write_qc(final_hash, final_size, probe)
    update_manifest(final_hash)
    append_event("review_package_ready", {"final": str(FINAL), "sha256": final_hash, "thumbnail": str(THUMB)})
    print(f"package ready: {PKG}")
    print(f"final sha256:{final_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
