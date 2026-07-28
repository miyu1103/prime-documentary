#!/usr/bin/env python3
"""Produce the end-screen work order for YouTube Studio. No API writes, none possible.

End screens are the one lever in this program that CANNOT be automated. The
YouTube Data API exposes no end-screen resource at all: `videos.list` rejects
`part=endScreens` and `part=cards` with HTTP 400 `unknownPart`, and there is no
`endScreens.insert`/`update` endpoint in any API version. The refusal is recorded
as live evidence in `api_capability_probes` inside DISTRIBUTION_STATE.v001.json
rather than asserted from documentation.

So this script emits a click-path work order instead: every public long-form,
ordered by measured views (highest impressions first, because an end screen only
earns anything on impressions the video already has), with the exact two targets
to select per video.

Outputs:
  episodes/_planning/END_SCREENS_WORK_ORDER.v001.md
  episodes/_planning/measurements/END_SCREENS.v001.json

Exit code: 0 always (this is a planning artifact, not a gate).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "distribution" / "series_clusters.v001.json"
STATE = ROOT / "episodes" / "_planning" / "measurements" / "DISTRIBUTION_STATE.v001.json"
ANALYTICS = ROOT / "scripts" / "_yt_analytics.json"
OUT_MD = ROOT / "episodes" / "_planning" / "END_SCREENS_WORK_ORDER.v001.md"
OUT_JSON = ROOT / "episodes" / "_planning" / "measurements" / "END_SCREENS.v001.json"

# An end screen element must sit inside the last 20 seconds and be at least 5s long.
END_SCREEN_WINDOW_SECONDS = 20
MIN_ELEMENT_SECONDS = 5


def load_analytics() -> dict[str, dict]:
    if not ANALYTICS.exists():
        return {}
    data = json.loads(ANALYTICS.read_text(encoding="utf-8"))
    cols = data.get("per_video", {}).get("cols", [])
    return {row[0]: dict(zip(cols, row)) for row in data.get("per_video", {}).get("rows", [])}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    state = json.loads(STATE.read_text(encoding="utf-8"))
    analytics = load_analytics()
    videos = {v["video_id"]: v for v in state["videos"]}

    cluster_of: dict[str, tuple[dict, int, str]] = {}
    for playlist in config["playlists"]:
        order = playlist["order"]
        for index, entry in enumerate(order):
            cluster_of[entry["video_id"]] = (playlist, entry["pos"], order[(index + 1) % len(order)]["video_id"])

    rows: list[dict] = []
    for video_id, (playlist, position, sibling_id) in cluster_of.items():
        video = videos.get(video_id)
        if video is None:
            continue
        sibling = videos.get(sibling_id, {})
        stats = analytics.get(video_id, {})
        duration = video["duration_seconds"]
        rows.append({
            "video_id": video_id,
            "title": video["title"],
            "views": video["views"],
            "average_view_percentage": stats.get("averageViewPercentage"),
            "duration_seconds": duration,
            "cluster": playlist["key"],
            "playlist_title": playlist["title"],
            "playlist_id": playlist.get("existing_playlist_id"),
            "playlist_position": position,
            "slot_1_video_id": sibling_id,
            "slot_1_title": sibling.get("title", sibling_id),
            "slot_1_reason": (
                "next case in the series - manufactures the co-watch edge the "
                "suggested feed currently borrows from other channels"
                if position < len(playlist["order"])
                else "loops back to the playlist entry point so the session continues"
            ),
            "slot_2_target": playlist["title"],
            "element_window": f"{max(duration - END_SCREEN_WINDOW_SECONDS, 0)}s - {duration}s",
            "studio_url": f"https://studio.youtube.com/video/{video_id}/editor",
        })

    rows.sort(key=lambda r: (-r["views"], r["title"]))

    report = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "scripts/plan_end_screens.py",
        "api_settable": False,
        "api_readable": False,
        "api_evidence": [
            probe for probe in state.get("api_capability_probes", [])
            if "endScreens" in probe.get("probe", "") or "cards" in probe.get("probe", "")
        ],
        "videos": len(rows),
        "estimated_minutes": len(rows) * 3,
        "rows": rows,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines: list[str] = []
    add = lines.append
    add("# END SCREENS - Studio work order v001")
    add("")
    add("## Can this be scripted? No - verified, not assumed")
    add("")
    for probe in report["api_evidence"]:
        add(f"- `{probe['probe']}` -> HTTP **{probe['http_status']}** "
            f"(`{probe.get('error_reason')}`): {probe['conclusion']}")
    add("- There is no `endScreens` or `cards` resource in the YouTube Data API v3 "
        "at any part name, and no write endpoint exists. End screens are settable "
        "only through YouTube Studio (web) or the YouTube Studio mobile app.")
    add("- Consequence: this is the one item on the distribution list that stays "
        "owner-manual no matter how much tooling is built.")
    add("")
    add("## What to click, per video")
    add("")
    add("1. Open the Studio link in the table.")
    add("2. **Editor -> End screen -> Apply to video** (or *+ Element* if one already exists).")
    add("3. Element 1 = **Video -> Specific video** -> paste the slot-1 id.")
    add("4. Element 2 = **Playlist** -> pick the slot-2 playlist.")
    add(f"5. Drag both elements into the last {END_SCREEN_WINDOW_SECONDS} seconds "
        f"(YouTube requires each element to run at least {MIN_ELEMENT_SECONDS}s and to "
        f"sit inside the final {END_SCREEN_WINDOW_SECONDS}s).")
    add("6. **Save**.")
    add("")
    add("Do the first video, then use **Apply template from video** on the rest and "
        "only swap element 1 - it turns a ~3-minute job into ~45 seconds per video.")
    add("")
    add(f"- videos: **{len(rows)}**")
    add(f"- rough effort: **{report['estimated_minutes']} minutes** at 3 min each, "
        "less with the template shortcut")
    add("- ordering: highest views first. An end screen converts impressions the video "
        "already gets; putting the same 2 minutes into a video with 1 view returns "
        "roughly nothing.")
    add("")
    add("## Priority order")
    add("")
    add("| # | views | APV | video | slot 1 (specific video) | slot 2 (playlist) | window | Studio |")
    add("|---|---|---|---|---|---|---|---|")
    for index, row in enumerate(rows, 1):
        apv = f"{row['average_view_percentage']:.1f}%" if row["average_view_percentage"] else "-"
        add(f"| {index} | {row['views']} | {apv} | {row['title'][:38].replace('|', '/')} "
            f"(`{row['video_id']}`) | {row['slot_1_title'][:32].replace('|', '/')} "
            f"(`{row['slot_1_video_id']}`) | {row['slot_2_target'][:28]} | "
            f"{row['element_window']} | [edit]({row['studio_url']}) |")
    add("")
    add("## Why these targets")
    add("")
    add("Slot 1 is always the next video in the same series playlist, and the last "
        "video in each playlist points back at position 1. That closes each cluster "
        "into a loop, which is the point: DEEP_RESEARCH_FINDINGS v001 section 5 found "
        "that 100% of measured suggested traffic arrives from other channels' videos, "
        "so the channel has no co-watch edges of its own. End screens and playlists "
        "are the only two mechanisms that create them.")
    add("")
    add("## Rollback")
    add("")
    add("End screens are removable in Studio (Editor -> End screen -> delete element) "
        "and removing one restores the previous state exactly. There is no viewer-facing "
        "record and no effect on the video file, its id, or its watch history.")
    add("")
    add("## Prerequisite")
    add("")
    add("Slot 2 needs the playlists to exist. Run the playlist plan first, or slot 2 "
        "can only offer the two playlists that exist today.")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(rows)} videos in the work order, ~{report['estimated_minutes']} minutes")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
