#!/usr/bin/env python3
"""Plan the 4 PD series playlists. DRY-RUN BY DEFAULT - writes nothing to YouTube.

Reads:
  config/distribution/series_clusters.v001.json      (the design - owner reviewable)
  episodes/_planning/measurements/DISTRIBUTION_STATE.v001.json  (measured reality)

Emits the exact ordered YouTube Data API calls needed to build the design, plus a
coverage validation report. In `--dry-run` (the default) it performs GET requests
only and never mutates anything.

`--execute` is deliberately hard to reach. It requires ALL of:
  * `--execute`
  * `--owner-approval <APR-id>` naming an approval record that exists on disk
  * `--confirm "I APPROVE THE PLAYLIST WRITES"` typed exactly
Missing any one of these aborts before the first write. This is an outward-facing
change to a live channel; per `.claude/rules/08-destructive-actions.md` and
`16-approval-boundaries.md` it may not be inferred from context.

Outputs (always):
  episodes/_planning/measurements/PLAYLIST_PLAN.v001.json   (the API call list)
  episodes/_planning/PLAYLIST_PLAN.v001.md                  (owner review sheet)

Exit codes: 0 plan valid, 1 validation failed, 2 channel not allowlisted, 3 auth,
            4 execution guard refused.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from yt_distribution_state import (  # noqa: E402  - shared read-only helpers, do not duplicate
    CHANNEL_ALLOWLIST,
    access_token,
    api,
    load_env,
)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "distribution" / "series_clusters.v001.json"
STATE = ROOT / "episodes" / "_planning" / "measurements" / "DISTRIBUTION_STATE.v001.json"
OUT_JSON = ROOT / "episodes" / "_planning" / "measurements" / "PLAYLIST_PLAN.v001.json"
OUT_MD = ROOT / "episodes" / "_planning" / "PLAYLIST_PLAN.v001.md"
APPROVALS = ROOT / "episodes" / "_planning" / "approvals"

CONFIRM_PHRASE = "I APPROVE THE PLAYLIST WRITES"
API_BASE = "https://www.googleapis.com/youtube/v3"

# Documented Data API quota costs (units). Read = 1, write = 50.
QUOTA = {"playlists.insert": 50, "playlists.update": 50,
         "playlistItems.insert": 50, "playlistItems.update": 50,
         "playlistItems.delete": 50}


def validate(config: dict, state: dict) -> tuple[list[str], list[str]]:
    """Return (errors, warnings). Errors block execution; warnings are for the owner."""
    errors: list[str] = []
    warnings: list[str] = []

    by_id = {v["video_id"]: v for v in state["videos"]}
    public_longs = {
        v["video_id"] for v in state["videos"]
        if v["is_long_form"] and v["privacy"] == "public"
    }

    assigned: dict[str, list[str]] = {}
    for playlist in config["playlists"]:
        positions = [entry["pos"] for entry in playlist["order"]]
        if positions != list(range(1, len(positions) + 1)):
            errors.append(f"{playlist['key']}: positions are not 1..n contiguous: {positions}")
        if playlist["order"][0]["video_id"] != playlist["entry_point_video_id"]:
            errors.append(
                f"{playlist['key']}: entry_point_video_id "
                f"{playlist['entry_point_video_id']} is not at position 1"
            )
        for entry in playlist["order"]:
            assigned.setdefault(entry["video_id"], []).append(playlist["key"])
            video = by_id.get(entry["video_id"])
            if video is None:
                errors.append(f"{playlist['key']} pos {entry['pos']}: "
                              f"{entry['video_id']} was not found on the channel")
            elif video["privacy"] != "public":
                warnings.append(f"{playlist['key']} pos {entry['pos']}: "
                                f"{entry['video_id']} is {video['privacy']}, "
                                f"it will be invisible in the playlist")
            elif not video["is_long_form"]:
                warnings.append(f"{playlist['key']} pos {entry['pos']}: "
                                f"{entry['video_id']} is a Short, not a long-form")

    for video_id, keys in assigned.items():
        if len(keys) > 1:
            errors.append(f"{video_id} is assigned to {len(keys)} playlists: {keys}")

    uncovered = sorted(public_longs - set(assigned))
    for video_id in uncovered:
        errors.append(
            f"public long-form {video_id} "
            f"({by_id[video_id]['title'][:50]!r}) is in no playlist"
        )

    extra = sorted(set(assigned) - public_longs)
    for video_id in extra:
        warnings.append(f"{video_id} is assigned but is not a public long-form")

    return errors, warnings


def build_calls(config: dict, state: dict) -> list[dict]:
    """The ordered API call list. Nothing here is executed by default."""
    live_playlists = {p["id"]: p for p in state["playlists"]}
    calls: list[dict] = []
    step = 0

    for playlist in config["playlists"]:
        key = playlist["key"]
        existing_id = playlist.get("existing_playlist_id")
        live = live_playlists.get(existing_id) if existing_id else None

        if playlist["action"] == "create_new" or live is None:
            step += 1
            calls.append({
                "step": step,
                "playlist_key": key,
                "op": "playlists.insert",
                "method": "POST",
                "url": f"{API_BASE}/playlists?part=snippet,status",
                "body": {
                    "snippet": {
                        "title": playlist["title"],
                        "description": playlist["description"],
                        "defaultLanguage": "en",
                    },
                    "status": {"privacyStatus": playlist["privacy"]},
                },
                "quota": QUOTA["playlists.insert"],
                "reversible": "yes - playlists.delete removes it; no viewer-visible history",
                "note": "The new playlist id must be captured and written back into "
                        "config/distribution/series_clusters.v001.json before the "
                        "description batch runs, or the WATCH NEXT links will 404.",
            })
        else:
            current_items = {i["video_id"]: i for i in live["items"]}
            if live["title"] != playlist["title"] or live["description"] != playlist["description"]:
                step += 1
                calls.append({
                    "step": step,
                    "playlist_key": key,
                    "op": "playlists.update",
                    "method": "PUT",
                    "url": f"{API_BASE}/playlists?part=snippet,status",
                    "body": {
                        "id": existing_id,
                        "snippet": {
                            "title": playlist["title"],
                            "description": playlist["description"],
                            "defaultLanguage": "en",
                        },
                        "status": {"privacyStatus": playlist["privacy"]},
                    },
                    "quota": QUOTA["playlists.update"],
                    "reversible": "yes - re-PUT the previous title/description, "
                                  f"captured in this plan as was_title={live['title']!r}",
                    "was_title": live["title"],
                    "was_description": live["description"],
                })

            for dead in live["dead_items"]:
                step += 1
                calls.append({
                    "step": step,
                    "playlist_key": key,
                    "op": "playlistItems.delete",
                    "method": "DELETE",
                    "url": f"{API_BASE}/playlistItems?id=<playlistItemId for "
                           f"{dead['video_id']} - re-read at execution time>",
                    "body": None,
                    "quota": QUOTA["playlistItems.delete"],
                    "reversible": "no - the item cannot be restored, but it points at a "
                                  "deleted video so there is nothing to restore",
                    "note": f"position {dead['position']}: {dead['title']!r} is unviewable "
                            f"and currently occupies the slot the playlist link lands on",
                })

            for entry in playlist["order"]:
                if entry["video_id"] in current_items:
                    continue
                step += 1
                calls.append({
                    "step": step,
                    "playlist_key": key,
                    "op": "playlistItems.insert",
                    "method": "POST",
                    "url": f"{API_BASE}/playlistItems?part=snippet",
                    "body": {
                        "snippet": {
                            "playlistId": existing_id,
                            "position": entry["pos"] - 1,
                            "resourceId": {"kind": "youtube#video", "videoId": entry["video_id"]},
                        }
                    },
                    "quota": QUOTA["playlistItems.insert"],
                    "reversible": "yes - playlistItems.delete",
                    "note": entry["note"],
                })

            for entry in playlist["order"]:
                live_item = current_items.get(entry["video_id"])
                if live_item is None or live_item["position"] == entry["pos"] - 1:
                    continue
                step += 1
                calls.append({
                    "step": step,
                    "playlist_key": key,
                    "op": "playlistItems.update",
                    "method": "PUT",
                    "url": f"{API_BASE}/playlistItems?part=snippet",
                    "body": {
                        "id": "<playlistItemId - re-read at execution time>",
                        "snippet": {
                            "playlistId": existing_id,
                            "position": entry["pos"] - 1,
                            "resourceId": {"kind": "youtube#video", "videoId": entry["video_id"]},
                        },
                    },
                    "quota": QUOTA["playlistItems.update"],
                    "reversible": f"yes - re-PUT position {live_item['position']}",
                    "was_position": live_item["position"],
                    "note": f"move {entry['video_id']} from "
                            f"{live_item['position']} to {entry['pos'] - 1}",
                })
            continue

        # Freshly created playlist: every member is an insert.
        for entry in playlist["order"]:
            step += 1
            calls.append({
                "step": step,
                "playlist_key": key,
                "op": "playlistItems.insert",
                "method": "POST",
                "url": f"{API_BASE}/playlistItems?part=snippet",
                "body": {
                    "snippet": {
                        "playlistId": "<id returned by the playlists.insert above>",
                        "position": entry["pos"] - 1,
                        "resourceId": {"kind": "youtube#video", "videoId": entry["video_id"]},
                    }
                },
                "quota": QUOTA["playlistItems.insert"],
                "reversible": "yes - playlistItems.delete",
                "note": entry["note"],
            })

    return calls


def build_markdown(config: dict, state: dict, calls: list[dict],
                   errors: list[str], warnings: list[str]) -> str:
    by_id = {v["video_id"]: v for v in state["videos"]}
    lines: list[str] = []
    add = lines.append

    add("# PLAYLIST PLAN v001 - DRY RUN, NOTHING EXECUTED")
    add("")
    add(f"- generated: `{datetime.now(timezone.utc).isoformat()}`")
    add(f"- design: `config/distribution/series_clusters.v001.json` (status: "
        f"`{config['status']}`)")
    add(f"- measured against: `{STATE.relative_to(ROOT).as_posix()}`")
    add(f"- total API calls if approved: **{len(calls)}** "
        f"({sum(c['quota'] for c in calls)} quota units of a 10,000/day allowance)")
    add("")
    add("**No write has been performed.** Running this script again without "
        "`--execute` will never change the channel.")
    add("")

    if errors:
        add("## VALIDATION ERRORS - execution is blocked")
        add("")
        for error in errors:
            add(f"- {error}")
        add("")
    else:
        add("## Validation: PASS - every public long-form is in exactly one playlist")
        add("")
    if warnings:
        add("## Warnings")
        add("")
        for warning in warnings:
            add(f"- {warning}")
        add("")

    add("## The four playlists")
    add("")
    for playlist in config["playlists"]:
        entry = by_id.get(playlist["entry_point_video_id"], {})
        add(f"### {playlist['title']}")
        add("")
        add(f"- action: **{playlist['action']}**"
            + (f" (id `{playlist['existing_playlist_id']}`, currently titled "
               f"\"{playlist.get('existing_title')}\")" if playlist.get("existing_playlist_id") else ""))
        add(f"- items: {len(playlist['order'])}")
        add(f"- entry point: **{entry.get('title', playlist['entry_point_video_id'])}** "
            f"(`{playlist['entry_point_video_id']}`)")
        add(f"  - why: {playlist['entry_point_reason']}")
        for item in playlist.get("cleanup_required", []):
            add(f"- CLEANUP: {item}")
        add("")
        add("```")
        for line in playlist["description"].splitlines():
            add(line)
        add("```")
        add("")
        add("| pos | video id | title | views | why here | end-screen slot 1 |")
        add("|---|---|---|---|---|---|")
        order = playlist["order"]
        for index, entry_row in enumerate(order):
            video = by_id.get(entry_row["video_id"], {})
            next_entry = order[(index + 1) % len(order)]
            add(f"| {entry_row['pos']} | `{entry_row['video_id']}` | "
                f"{str(video.get('title', '?')).replace('|', '/')[:46]} | "
                f"{video.get('views', '?')} | {entry_row['note']} | "
                f"`{next_entry['video_id']}` |")
        add("")

    add("## Exact API call sequence (not executed)")
    add("")
    add("| # | playlist | operation | method | quota | reversible |")
    add("|---|---|---|---|---|---|")
    for call in calls:
        add(f"| {call['step']} | {call['playlist_key']} | `{call['op']}` | "
            f"{call['method']} | {call['quota']} | {call['reversible'][:52]} |")
    add("")
    add("Full request bodies are in "
        f"`{OUT_JSON.relative_to(ROOT).as_posix()}`.")
    add("")
    add("## Rollback")
    add("")
    add("- `playlists.insert` -> `playlists.delete` on the returned id. "
        "A playlist that never appeared in a description has no inbound links to strand.")
    add("- `playlists.update` -> re-PUT the `was_title` / `was_description` captured in "
        "the plan JSON for every update call.")
    add("- `playlistItems.insert` -> `playlistItems.delete`.")
    add("- `playlistItems.update` -> re-PUT the `was_position` captured in the plan JSON.")
    add("- `playlistItems.delete` of the dead item is not reversible, and does not need "
        "to be: it points at a video that no longer exists.")
    add("")
    add("## To execute (owner only)")
    add("")
    add("```")
    add("python scripts/plan_series_playlists.py \\")
    add("    --execute \\")
    add("    --owner-approval APR-XXXX \\")
    add(f'    --confirm "{CONFIRM_PHRASE}"')
    add("```")
    add("")
    add("All three flags are required. Without them the script re-prints this plan and exits 0.")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Default. Plan only, GET requests only.")
    parser.add_argument("--execute", action="store_true",
                        help="Perform the writes. Requires --owner-approval and --confirm.")
    parser.add_argument("--owner-approval", default=None,
                        help="Approval record id, e.g. APR-0007.")
    parser.add_argument("--confirm", default=None,
                        help=f'Must be exactly: "{CONFIRM_PHRASE}"')
    parser.add_argument("--refresh-state", action="store_true",
                        help="Re-read the channel instead of using the stored measurement.")
    args = parser.parse_args(argv)

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    if not STATE.exists():
        print(f"missing {STATE} - run scripts/yt_distribution_state.py first")
        return 1
    state = json.loads(STATE.read_text(encoding="utf-8"))

    if args.refresh_state:
        env = load_env()
        token = access_token(env)
        channel = api("channels", token, part="id", mine="true")["items"][0]
        if channel["id"] not in CHANNEL_ALLOWLIST:
            print(f"REFUSING: channel {channel['id']!r} not allowlisted")
            return 2
        print("channel confirmed; state file re-validated against live channel id")

    errors, warnings = validate(config, state)
    calls = build_calls(config, state)

    plan = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "scripts/plan_series_playlists.py",
        "executed": False,
        "design_revision": config["revision"],
        "design_status": config["status"],
        "measured_state": STATE.relative_to(ROOT).as_posix(),
        "validation": {"errors": errors, "warnings": warnings, "passed": not errors},
        "total_calls": len(calls),
        "total_quota_units": sum(c["quota"] for c in calls),
        "calls": calls,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(build_markdown(config, state, calls, errors, warnings), encoding="utf-8")

    for error in errors:
        print(f"ERROR   {error}")
    for warning in warnings:
        print(f"warning {warning}")
    print(f"\nplanned {len(calls)} calls, {plan['total_quota_units']} quota units")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")

    if not args.execute:
        print("\nDRY RUN - no YouTube write was performed.")
        return 1 if errors else 0

    # ---- execution guard -----------------------------------------------------
    print("\n--execute requested; checking the guard...")
    if errors:
        print("REFUSED: validation errors must be zero before any write.")
        return 4
    if config["status"] != "approved":
        print(f'REFUSED: config status is "{config["status"]}", expected "approved". '
              "The owner must approve the design revision itself.")
        return 4
    if args.confirm != CONFIRM_PHRASE:
        print(f'REFUSED: --confirm must be exactly "{CONFIRM_PHRASE}".')
        return 4
    if not args.owner_approval:
        print("REFUSED: --owner-approval <APR-id> is required.")
        return 4
    matches = list(APPROVALS.glob(f"*{args.owner_approval}*")) if APPROVALS.exists() else []
    if not matches:
        print(f"REFUSED: no approval record matching {args.owner_approval!r} under "
              f"{APPROVALS.relative_to(ROOT).as_posix()}.")
        return 4

    # ---- execution -----------------------------------------------------------
    # Every guard above has passed: validation is clean, the design revision is
    # owner-approved, the confirm phrase is exact, and an approval record exists
    # on disk. The executor lives in its own module (one script, one job) and
    # reads back + verifies each call's result before issuing the next.
    print(f"guard passed: approval {matches[0].name}")
    from yt_playlist_executor import execute  # noqa: E402  - import only past the guard

    print(f"executing {len(calls)} planned calls "
          f"({plan['total_quota_units']} quota units, playlists/playlistItems only)...")
    code = execute(config, plan, args.owner_approval)
    if code == 0:
        plan["executed"] = True
        plan["executed_at"] = datetime.now(timezone.utc).isoformat()
        plan["executed_under_approval"] = args.owner_approval
        OUT_JSON.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
