#!/usr/bin/env python3
"""Ask the live YouTube API what state specific videos are actually in.

A `publishAt` is not a schedule. On 2026-08-17 EP64 memphis carried a date, a thumbnail and a
caption track while `uploadStatus` was still `uploaded` and `processingStatus` still
`processing`, eleven hours after a force-kill interrupted its 1.7 GB transfer -- it would have
reached its slot broken. `pd_watchdog.py` asks this question every fifteen minutes, but only
about the videos its own `search` call happens to enumerate, and that enumeration is known to
drop rows (see docs/handover, uploads-playlist vs search disagreement).

This asks about ids you name, or about every episode that recorded a
`09_package/youtube_schedule_result.v001.json`. Cost is 1 quota unit per call (up to 50 ids).

    py -3.11 scripts/yt_video_status.py                  # every episode with a schedule receipt
    py -3.11 scripts/yt_video_status.py --id ABC,DEF     # specific ids
    py -3.11 scripts/yt_video_status.py --slug hyatt

Exit code 1 if any video examined is not `processed` / `succeeded`, or is missing entirely.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def receipts() -> list[tuple[str, str, str]]:
    """(slug, video_id, publishAt) for every episode carrying a schedule receipt.

    Returns EVERY id an episode ever recorded, newest revision first; `main` then reports the
    one the API actually returns. Neither `v001` nor "the highest revision" is the live video,
    and both wrong rules were measured on 2026-08-19:

      EP65 marmet carries FIVE receipts -- ks3bD1y8jME, ENEMRpoJsMM, Y_U9FuHhtt8, 0g-QFPWTLBE,
      m19yjXNVotk -- one per upload attempt. Only the LAST exists. Reading `v001` reported the
      episode MISSING while it was live and public.

      EP62 greene carries two, and the live one is `v001` (Atla22DlJcU, public). Its `v002`
      (ihjoBNXIoZ0) is a later-written receipt for an EARLIER slot whose upload died, and the
      API returns nothing for it. Reading the highest revision reported MISSING here.

    So revision order does not rank liveness in either direction, and this is the same class
    of defect the tool exists to catch: an instrument confidently describing a video that is
    not the one on the channel. Existence is asked, never inferred.
    """
    rows: list[tuple[str, str, str]] = []
    for ep in sorted((ROOT / "episodes").glob("PD-*")):
        for r in sorted((ep / "09_package").glob("youtube_schedule_result.v*.json"), reverse=True):
            d = json.loads(r.read_text(encoding="utf-8"))
            vid = d.get("video_id")
            if vid:
                rows.append((ep.name.split("-")[-1], vid, d.get("publishAt") or ""))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", help="comma-separated video ids")
    ap.add_argument("--slug", help="only this episode slug")
    args = ap.parse_args()

    if args.id:
        rows = [("(given)", v.strip(), "") for v in args.id.split(",") if v.strip()]
    else:
        rows = receipts()
        if args.slug:
            rows = [r for r in rows if r[0] == args.slug]
    if not rows:
        print("no video ids to check")
        return 1

    from yt_channel_index import authorize, http, API  # noqa: E402

    auth = authorize(ROOT)
    ids = [r[1] for r in rows]
    found: dict[str, dict] = {}
    for i in range(0, len(ids), 50):
        _, v = http("GET", f"{API}/videos?part=status,processingDetails,snippet"
                           f"&id={','.join(ids[i:i + 50])}", headers=auth)
        for it in v.get("items", []):
            found[it["id"]] = it

    # An episode with several receipts is one whose upload was retried. Report the id the API
    # returns; the others are dead attempts and saying so about each would be 40 lines of
    # noise about videos nobody is looking for. Only when NONE of an episode's ids exists is
    # there something wrong, and then the newest is named.
    if not args.id:
        keep: list[tuple[str, str, str]] = []
        for slug in dict.fromkeys(r[0] for r in rows):
            mine = [r for r in rows if r[0] == slug]
            live = [r for r in mine if r[1] in found]
            if live:
                keep.extend(live[:1])
                dead = len(mine) - len(live)
                if dead:
                    print(f"note: {slug} has {dead} dead upload attempt(s) on record; "
                          f"reporting {live[0][1]}, which the API returns")
            else:
                keep.append(mine[0])
        rows = keep

    bad = 0
    print(f"{'slug':<12} {'video':<13} {'upload':<11} {'processing':<11} {'privacy':<9} publishAt")
    print("-" * 100)
    for slug, vid, want in rows:
        it = found.get(vid)
        if it is None:
            print(f"{slug:<12} {vid:<13} {'MISSING':<11} {'-':<11} {'-':<9} "
                  f"receipt says {want} -- the API does not return this video")
            bad += 1
            continue
        s = it.get("status", {})
        p = it.get("processingDetails", {})
        up, pr = s.get("uploadStatus", "?"), p.get("processingStatus", "?")
        ok = up == "processed" and pr == "succeeded"
        mark = "" if ok else "   <-- NOT SHIPPABLE"
        if not ok:
            bad += 1
        print(f"{slug:<12} {vid:<13} {up:<11} {pr:<11} {s.get('privacyStatus','?'):<9} "
              f"{s.get('publishAt','(none)')}{mark}")
        if want and s.get("publishAt") and s["publishAt"][:16] != want[:16]:
            print(f"{'':<12} {'':<13} receipt wanted {want} but the channel says {s['publishAt']}")
            bad += 1

    print(f"\n{len(rows)} checked, {bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
