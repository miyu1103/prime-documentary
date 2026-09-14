#!/usr/bin/env python3
"""Stage the description + pinned-comment batch for every public long-form.

STAGING ONLY. Reads local files, writes local files, makes no network call and
has no publish path. The output is meant to be read line by line by the owner
before any of it reaches YouTube.

For each public long-form it produces:
  * `description_after` - the live description with (a) a repaired chapter block
    folded in where one is staged, and (b) a WATCH NEXT block naming the cluster
    sibling and the series playlist.
  * a unified diff against the live description, so a reviewer sees exactly what
    would change rather than having to compare two walls of text.
  * a pinned-comment draft for the video's cluster.

Placement rules (deliberate, per DEEP_RESEARCH_FINDINGS.v001 R-28):
  * the first two lines of the description are never touched - that is the text
    the feed surfaces;
  * an existing chapter block is replaced in place;
  * a new chapter block is inserted before the first "housekeeping" section
    (AI disclosure / visual note / sources / educational disclaimer), never at
    the top and never after the hashtags;
  * WATCH NEXT goes immediately after the chapter block.

Outputs:
  episodes/_planning/measurements/DESCRIPTION_BATCH.v001.json
  episodes/_planning/DESCRIPTION_BATCH.v001.md
  episodes/_planning/PINNED_COMMENTS.v001.md

Exit codes: 0 every video staged, 1 one or more could not be staged.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
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
CHAPTERS = ROOT / "episodes" / "_planning" / "measurements" / "CHAPTER_RESTORATION.v001.json"
OUT_JSON = ROOT / "episodes" / "_planning" / "measurements" / "DESCRIPTION_BATCH.v001.json"
OUT_MD = ROOT / "episodes" / "_planning" / "DESCRIPTION_BATCH.v001.md"
OUT_COMMENTS = ROOT / "episodes" / "_planning" / "PINNED_COMMENTS.v001.md"

YOUTUBE_DESCRIPTION_LIMIT = 5000

CHAPTER_HEADING_RE = re.compile(r"^\s*(?:[-—–]+\s*)?chapters?\s*[:\-—–]?\s*(?:[-—–]+)?\s*$", re.I)
TIMESTAMP_LINE_RE = re.compile(r"^\s*(?:\d{1,2}:)?\d{1,2}:\d{2}\b")
# Sections that must stay BELOW the chapter block.
HOUSEKEEPING_RE = re.compile(
    r"^\s*(?:[-—–]+\s*)?(?:ai disclosure|visual note|note on imagery|sources?|"
    r"this is an educational|disclaimer|about this (?:film|channel)|"
    r"▶|👉|#\w)", re.I,
)
PLACEHOLDER_LINE_RE = re.compile(r"chapters? (?:finalized|to be finalized|tbd|pending)", re.I)
SUPERSEDED_PLAYLIST_RE = re.compile(
    r"(?:watch|see)\s+the\s+full\s+.*playlist|youtube\.com/playlist\?", re.I
)


def executed_playlist_ids() -> dict[str, str]:
    """Playlist ids the executor actually created, keyed by cluster.

    Two clusters were `create_new`, so `series_clusters.v001.json` still carries
    `existing_playlist_id: null` for them. The live ids live in the execution
    state. Reading them here means the staged WATCH NEXT block links the real
    playlist instead of a placeholder, and does not require editing an approved
    config to record something the API already told us.
    """
    p = ROOT / "episodes" / "_planning" / "measurements" / "PLAYLIST_EXECUTION.v001.json"
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8")).get("playlist_ids", {}) or {}
    except Exception:
        return {}


def playlist_url(playlist_id: str | None) -> str:
    if not playlist_id:
        return "<PLAYLIST URL - fill in after the playlist is created>"
    return f"https://www.youtube.com/playlist?list={playlist_id}"


def strip_existing_chapters(lines: list[str]) -> tuple[list[str], int | None, list[str]]:
    """Remove an existing chapter block and any superseded playlist line.

    Returns (remaining_lines, insert_index, removal_notes). `insert_index` is
    recorded AFTER trailing blanks are trimmed - recording it before lets later
    trimming shift the index and drop the new block into the middle of the
    housekeeping section.
    """
    out: list[str] = []
    notes: list[str] = []
    insert_at: int | None = None
    index = 0
    while index < len(lines):
        line = lines[index]
        is_heading = bool(CHAPTER_HEADING_RE.match(line))
        is_stamp = bool(TIMESTAMP_LINE_RE.match(line))

        if is_heading or is_stamp:
            index += 1
            while index < len(lines) and (
                TIMESTAMP_LINE_RE.match(lines[index])
                or PLACEHOLDER_LINE_RE.search(lines[index])
                or (is_heading and not lines[index].strip())
            ):
                index += 1
            while out and not out[-1].strip():
                out.pop()
            if insert_at is None:
                insert_at = len(out)          # recorded only after trimming
            while index < len(lines) and not lines[index].strip():
                index += 1
            continue

        # A hand-written "watch the full <name> playlist" line is superseded by
        # the WATCH NEXT block; leaving it produces two playlist links, one of
        # which names a playlist that is about to be retitled.
        if SUPERSEDED_PLAYLIST_RE.search(line):
            notes.append(f"removed superseded playlist line: {line.strip()[:80]}")
            index += 1
            continue

        out.append(line)
        index += 1
    return out, insert_at, notes


def choose_insert_index(lines: list[str]) -> int:
    """Where a fresh chapter block goes: above the first housekeeping section."""
    for index, line in enumerate(lines):
        if index < 2:
            continue                      # never disturb the feed-visible opening
        if HOUSEKEEPING_RE.match(line):
            return index
    return len(lines)


def build_description(live: str, chapter_lines: list[str], watch_next: str) -> tuple[str, list[str]]:
    lines = live.splitlines()
    lines, chapter_index, notes = strip_existing_chapters(lines)

    block: list[str] = []
    if chapter_lines:
        block += ["CHAPTERS"] + list(chapter_lines) + [""]
    block += watch_next.splitlines() + [""]

    index = chapter_index if chapter_index is not None else choose_insert_index(lines)
    index = min(max(index, 2), len(lines))
    while index > 0 and not lines[index - 1].strip():
        index -= 1
    prefix = lines[:index]
    suffix = lines[index:]
    if prefix and prefix[-1].strip():
        prefix = prefix + [""]
    while suffix and not suffix[0].strip():
        suffix = suffix[1:]

    merged = prefix + block + suffix
    text = "\n".join(merged)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n", notes


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", nargs="*", default=None)
    args = parser.parse_args(argv)

    for path in (CONFIG, STATE, CHAPTERS):
        if not path.exists():
            print(f"missing {path}")
            return 1
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    state = json.loads(STATE.read_text(encoding="utf-8"))
    restoration = json.loads(CHAPTERS.read_text(encoding="utf-8"))

    videos = {v["video_id"]: v for v in state["videos"]}
    staged_chapters = {
        item["video_id"]: item
        for item in restoration["items"]
        if item["validation"]["youtube_valid"]
    }

    cluster_of: dict[str, dict] = {}
    sibling_of: dict[str, str] = {}
    for playlist in config["playlists"]:
        order = playlist["order"]
        for index, entry in enumerate(order):
            cluster_of[entry["video_id"]] = playlist
            sibling_of[entry["video_id"]] = order[(index + 1) % len(order)]["video_id"]

    live_descriptions = {}
    for video_id, video in videos.items():
        live_descriptions[video_id] = video.get("description_text")

    items: list[dict] = []
    unstaged: list[str] = []
    executed = executed_playlist_ids()
    for playlist in config["playlists"]:
        copy = config["copy"]["per_cluster"][playlist["key"]]
        live_id = playlist.get("existing_playlist_id") or executed.get(playlist["key"])
        list_url = playlist_url(live_id)
        for entry in playlist["order"]:
            video_id = entry["video_id"]
            if args.only and video_id not in set(args.only):
                continue
            video = videos.get(video_id)
            if video is None:
                unstaged.append(video_id)
                continue

            sibling_id = sibling_of[video_id]
            sibling = videos.get(sibling_id, {})
            fields = {
                "this_title": video["title"],
                "sibling_title": sibling.get("title", sibling_id),
                "sibling_url": f"https://youtu.be/{sibling_id}",
                "playlist_title": playlist["title"],
                "playlist_url": list_url,
            }
            watch_next = config["copy"]["watch_next_template"].format(**fields)
            pinned = copy["pinned_comment"].format(**fields)

            staged = staged_chapters.get(video_id)
            chapter_lines = staged["chapter_lines"] if staged else []
            live = live_descriptions.get(video_id)
            if live is None:
                unstaged.append(video_id)
                continue

            after, edit_notes = build_description(live, chapter_lines, watch_next)
            diff = list(difflib.unified_diff(
                live.splitlines(), after.splitlines(),
                fromfile=f"{video_id} LIVE", tofile=f"{video_id} STAGED", lineterm="",
            ))
            blockers: list[str] = []
            if len(after) > YOUTUBE_DESCRIPTION_LIMIT:
                blockers.append(f"description would be {len(after)} chars, over the "
                                f"{YOUTUBE_DESCRIPTION_LIMIT} limit")
            if not chapter_lines and not video["chapters"]["youtube_valid"]:
                blockers.append("no valid chapter block available - WATCH NEXT only")
            if staged and staged["repair"].get("labels_needing_authoring"):
                blockers.append(
                    "chapter labels still production-internal: "
                    + ", ".join(staged["repair"]["labels_needing_authoring"])
                )
            if live_id is None:
                blockers.append("playlist does not exist yet - the WATCH NEXT playlist "
                                "URL is a placeholder and must be filled in after "
                                "plan_series_playlists.py runs")

            items.append({
                "video_id": video_id,
                "title": video["title"],
                "episode_id": staged["episode_id"] if staged else None,
                "cluster": playlist["key"],
                "playlist_title": playlist["title"],
                "playlist_position": entry["pos"],
                "sibling_video_id": sibling_id,
                "sibling_title": fields["sibling_title"],
                "views": video["views"],
                "chapters_state_before": video["chapters"]["state"],
                "chapter_lines": chapter_lines,
                "watch_next_block": watch_next,
                "pinned_comment": pinned,
                "description_before": live,
                "description_after": after,
                "description_diff": diff,
                "edit_notes": edit_notes,
                "chars_before": len(live),
                "chars_after": len(after),
                "blockers": blockers,
                "watch_url": video["watch_url"],
                "studio_url": video["studio_url"],
            })

    report = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "scripts/stage_description_batch.py",
        "published": False,
        "design_revision": config["revision"],
        "summary": {
            "staged": len(items),
            "unstaged": len(unstaged),
            "with_chapter_repair": sum(1 for i in items if i["chapter_lines"]),
            "watch_next_only": sum(1 for i in items if not i["chapter_lines"]),
            "with_blockers": sum(1 for i in items if i["blockers"]),
        },
        "unstaged_video_ids": unstaged,
        "items": items,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ---- review sheet --------------------------------------------------------
    lines: list[str] = []
    add = lines.append
    add("# DESCRIPTION BATCH v001 - staged, nothing published")
    add("")
    add(f"- generated: `{report['generated_at']}`")
    add(f"- staged: **{report['summary']['staged']}** videos "
        f"({report['summary']['with_chapter_repair']} get a repaired chapter block, "
        f"{report['summary']['watch_next_only']} get WATCH NEXT only)")
    add(f"- rows carrying a blocker: **{report['summary']['with_blockers']}**")
    add("")
    add("Each entry shows a unified diff against the live description. `-` lines would "
        "be removed, `+` lines added. Nothing is applied by this script.")
    add("")
    add("| video id | cluster | pos | was | chapters | chars | blockers |")
    add("|---|---|---|---|---|---|---|")
    for item in items:
        add(f"| `{item['video_id']}` | {item['cluster']} | {item['playlist_position']} | "
            f"{item['chapters_state_before']} | {len(item['chapter_lines'])} | "
            f"{item['chars_before']}->{item['chars_after']} | {len(item['blockers'])} |")
    add("")
    for item in items:
        add(f"## {item['title']}")
        add("")
        add(f"- `{item['video_id']}` | {item['watch_url']} | Studio: {item['studio_url']}")
        add(f"- cluster **{item['cluster']}** position {item['playlist_position']}; "
            f"sibling = {item['sibling_title']} (`{item['sibling_video_id']}`)")
        for blocker in item["blockers"]:
            add(f"- BLOCKER: {blocker}")
        add("")
        add("```diff")
        for line in item["description_diff"]:
            add(line)
        add("```")
        add("")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---- pinned comments -----------------------------------------------------
    lines = []
    add = lines.append
    add("# PINNED COMMENTS v001 - drafts, nothing posted")
    add("")
    add("The Data API can POST a comment as the channel (`comments.insert`, a write - "
        "not performed by any script here) but there is **no API to pin one**. Pinning "
        "is a manual action in Studio or the mobile app, so each row below is a "
        "copy-paste-then-pin task.")
    add("")
    add(f"- drafts: {len(items)}, one per public long-form, grouped by cluster")
    add("")
    for playlist in config["playlists"]:
        cluster_items = [i for i in items if i["cluster"] == playlist["key"]]
        if not cluster_items:
            continue
        add(f"## {playlist['title']} ({len(cluster_items)} videos)")
        add("")
        add("Cluster template:")
        add("")
        add("```")
        for line in config["copy"]["per_cluster"][playlist["key"]]["pinned_comment"].splitlines():
            add(line)
        add("```")
        add("")
        for item in cluster_items:
            add(f"### {item['title']}")
            add("")
            add(f"- `{item['video_id']}` | {item['studio_url']}")
            add("")
            add("```")
            for line in item["pinned_comment"].splitlines():
                add(line)
            add("```")
            add("")
    OUT_COMMENTS.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"staged {report['summary']['staged']} descriptions "
          f"({report['summary']['with_blockers']} carry blockers), "
          f"{report['summary']['unstaged']} unstaged")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_COMMENTS}")
    return 1 if unstaged else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
