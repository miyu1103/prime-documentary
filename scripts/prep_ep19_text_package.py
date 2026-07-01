#!/usr/bin/env python3
"""Prepare EP19 title, thumbnail copy, chapters, and acceptance draft."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-019-varsityblues"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(name: str, data: dict) -> None:
    PKG.mkdir(exist_ok=True)
    (PKG / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    title_options = [
        {
            "option": "A",
            "title": "The Side Door: Operation Varsity Blues",
            "length": 39,
            "thumbnail_headline": "THE SIDE DOOR",
            "promise": "Explains Singer's side-door scheme without implying trial convictions or child knowledge.",
        },
        {
            "option": "B",
            "title": "They Bought the Side Door Into College",
            "length": 39,
            "thumbnail_headline": "BOUGHT NOT EARNED",
            "promise": "Focuses on the paid guarantee and taken-seat theme.",
        },
        {
            "option": "C",
            "title": "$25M to Get Into Elite Colleges",
            "length": 32,
            "thumbnail_headline": "$25M TO GET IN",
            "promise": "Direct money hook, honest to the charged scheme and script.",
        },
    ]
    write_json(
        "title_thumbnail_plan.v001.json",
        {
            "episode_id": EP,
            "revision": "v001",
            "status": "copy_ready_visual_render_pending",
            "selected_recommendation": "A",
            "title_options": title_options,
            "thumbnail_requirements": {
                "size": "1280x720",
                "variants_required": 3,
                "style": "black/navy high contrast with gold #E5B53A or electric #1F6BFF accent",
                "r3_locks": [
                    "no real-person likeness",
                    "no real university logos/crests/mascots/landmarks",
                    "do not say convicted at trial",
                    "do not imply children's knowledge",
                    "universities are victims, not defendants",
                ],
            },
            "created_at": now(),
        },
    )
    write_json(
        "chapters.v001.json",
        {
            "episode_id": EP,
            "revision": "v001",
            "status": "draft_ready_pending_final_render_timecheck",
            "chapters": [
                {"time": "00:00", "title": "The Side Door"},
                {"time": "00:08", "title": "The Three Doors"},
                {"time": "02:50", "title": "The Fixer"},
                {"time": "08:30", "title": "The Two Machines"},
                {"time": "15:45", "title": "The Families and the Taken Seat"},
                {"time": "22:30", "title": "The Reckoning"},
                {"time": "27:40", "title": "What the Scandal Did Not Touch"},
            ],
            "note": "Chapter times come from locked script markers and must be rechecked against final rendered runtime.",
            "created_at": now(),
        },
    )
    write_json(
        "acceptance_report.draft.v001.json",
        {
            "episode_id": EP,
            "revision": "v001",
            "status": "draft_pending_images_thumbnails_final_render",
            "known_pass_now": {
                "voice_provider": "elevenlabs",
                "captions_file": "episodes/PD-2026-019-varsityblues/08_edit/captions.v001.srt",
                "captions_format": "max line chars 42; max cps measured 16.21",
                "audio_mix": "H:/pd-media/episodes/PD-2026-019-varsityblues/08_edit/varsityblues_final_mix.v001.wav",
                "audio_loudness_precheck": "-14.3 LUFS",
                "factory_assets_staged": 64,
            },
            "known_pending": [
                "92 final hero images in selected directory",
                "final.mp4 render",
                "3 thumbnail PNGs plus selected",
                "independent check_final_acceptance.py 19 --json exit 0",
                "owner R3 legal/rights review before publish",
            ],
            "created_at": now(),
        },
    )
    print("EP19 text/package drafts prepared.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
