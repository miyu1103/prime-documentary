#!/usr/bin/env python3
"""Post the channel's own comment on each Short, carrying the question and the long-form link.

This is layer 3 of the funnel and the last one that could be automated. Layers 1, 2 and 5 (the
description's first line, the on-screen card, the loop structure) are already enforced by code.
Layer 4 (Studio's "Related video") has no API and stays manual.

Why a comment is worth the call: the description on a Short is collapsed to one line on mobile, so
a viewer who wants more has two obvious places to look — the description and the comments. Leaving
the comments empty wastes the second one.

Honest limit: the API can POST a comment as the channel but CANNOT pin it. `commentThreads.insert`
has no pin parameter and there is no separate pin endpoint. An owner comment carries the channel
badge and lands high, but "pinned" still needs one click in Studio. This tool does the writing;
pinning stays on the manual worklist next to the related-video setting.

What it posts, from the Short's own design:
    <funnel_question_left_for_longform>

    Full case here -> https://www.youtube.com/watch?v=<longform>

That question was written at design time as the thing the Short deliberately does not answer, so
the comment is not an advert — it is the unresolved half of what the viewer just watched.

Refuses, rather than posting something useless:
  * a Short with no known long-form destination
  * a destination that is not public (a link to a video nobody can open is worse than no link)
  * a Short that already has a comment from this channel (idempotent, safe to re-run)

Quota: commentThreads.insert costs 50 units. A full pass over 40 Shorts is 2,000 of 10,000.

Usage:
  py -3.11 scripts/post_short_funnel_comment.py                 # dry run, shows what it would post
  py -3.11 scripts/post_short_funnel_comment.py --apply
  py -3.11 scripts/post_short_funnel_comment.py --apply --only short86,short87
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
DATA = ROOT / "remotion" / "src" / "data"
RUNS = ROOT / "runs" / "short_funnel"
CHANNEL_ALLOWLIST = {"UCuQPtAz1rca9eJ4xhvX0yKA"}

sys.path.insert(0, str(Path(__file__).resolve().parent))
from yt_channel_index import authorize, fetch_videos, http, iso_seconds, list_video_ids  # noqa: E402
import yt_quota as q  # noqa: E402


def short_to_video() -> dict[str, str]:
    """short id -> uploaded video id, from the schedule receipts written at upload time."""
    out: dict[str, str] = {}
    for p in list((ROOT / "runs" / "new_shorts" / "schedule").glob("short*.result.json")) + \
             list((ROOT / "episodes").rglob("short*_youtube_schedule_result.*.json")):
        m = re.match(r"(short\d+[a-z]?)", p.name)
        if not m:
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        v = d.get("video_id") or d.get("videoId") or (d.get("response") or {}).get("id")
        if isinstance(v, str) and len(v) == 11:
            out.setdefault(m.group(1), v)
    return out


def questions() -> dict[str, str]:
    out: dict[str, str] = {}
    for f in sorted(DESIGNS.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for s in d.get("shorts", []):
            qtext = (s.get("funnel_question_left_for_longform") or "").strip()
            if s.get("short_id") and qtext:
                out[s["short_id"]] = qtext
    return out


def episode_of_short() -> dict[str, str]:
    out: dict[str, str] = {}
    for f in sorted(DATA.glob("short*.ts")):
        if f.name.endswith("_timing.ts"):
            continue
        m = re.search(r"episodeId:\s*'([^']+)'", f.read_text("utf-8", errors="replace"))
        if m:
            out[f.stem] = m.group(1)
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", help="comma-separated short ids")
    a = ap.parse_args()
    only = {x.strip() for x in a.only.split(",")} if a.only else None

    auth = authorize(ROOT)
    ids = list_video_ids(auth)
    V = fetch_videos(auth, ids)
    q.record("videos.list", -(-len(ids) // 50))

    longs = {i: v for i, v in V.items()
             if iso_seconds(v["contentDetails"]["duration"]) > 185
             and v["status"]["privacyStatus"] == "public"}
    ep_long: dict[str, str] = {}
    for ep_dir in sorted((ROOT / "episodes").glob("PD-2026-*")):
        for j in ep_dir.rglob("*.json"):
            if "short" in j.name.lower():
                continue
            try:
                txt = j.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for lid in longs:
                if lid in txt:
                    ep_long.setdefault(ep_dir.name, lid)

    vid_of, qs, ep_of = short_to_video(), questions(), episode_of_short()
    todo, skipped = [], []
    for sid, vid in sorted(vid_of.items()):
        if only and sid not in only:
            continue
        v = V.get(vid)
        if not v or iso_seconds(v["contentDetails"]["duration"]) > 185:
            continue
        lid = ep_long.get(ep_of.get(sid, ""), "")
        if not lid:
            skipped.append((sid, "destination not public yet")); continue
        if not qs.get(sid):
            skipped.append((sid, "design has no funnel question")); continue
        todo.append({"short": sid, "video": vid, "longform": lid, "q": qs[sid],
                     "title": v["snippet"]["title"][:44]})

    # already commented? one cheap read per video, and it makes the run idempotent
    have = set()
    for t in todo:
        st, r = http("GET", "https://www.googleapis.com/youtube/v3/commentThreads"
                            f"?part=snippet&maxResults=20&videoId={t['video']}", headers=auth)
        q.record("commentThreads.list" if "commentThreads.list" in q.UNITS else "videos.list")
        if st != 200:
            continue
        for item in r.get("items", []):
            sn = item["snippet"]["topLevelComment"]["snippet"]
            if sn.get("authorChannelId", {}).get("value") in CHANNEL_ALLOWLIST:
                have.add(t["short"])
    todo = [t for t in todo if t["short"] not in have]

    print(f"{len(vid_of)} uploaded Shorts | {len(todo)} need a funnel comment | "
          f"{len(have)} already have one | {len(skipped)} skipped")
    for s, why in skipped[:8]:
        print(f"  skip {s}: {why}")
    for t in todo[:6]:
        print(f"\n  {t['short']} -> {t['video']}  ({t['title']})")
        print(f"    {t['q'][:100]}")
        print(f"    Full case here -> https://www.youtube.com/watch?v={t['longform']}")

    if not a.apply or not todo:
        if not a.apply:
            print("\nDRY RUN - nothing posted.")
        return 0

    q.assert_budget(len(todo) * q.UNITS["commentThreads.insert"], what="the comment batch") \
        if "commentThreads.insert" in q.UNITS else None

    ok = fail = 0
    for t in todo:
        body = {"snippet": {"videoId": t["video"], "topLevelComment": {"snippet": {
            "textOriginal": f"{t['q']}\n\nFull case here → "
                            f"https://www.youtube.com/watch?v={t['longform']}"}}}}
        st, r = http("POST", "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet",
                     headers=auth, body=body)
        q.record("commentThreads.insert", units=50)
        if st == 200:
            ok += 1
            print(f"  posted on {t['short']} ({t['video']})")
        else:
            fail += 1
            print(f"  FAILED {t['short']} {st}: {r.get('error', {}).get('message', '')[:110]}")

    RUNS.mkdir(parents=True, exist_ok=True)
    print(f"\nposted {ok}, failed {fail}")
    print("NOTE: the API cannot pin. Pinning these is one click each in Studio, alongside the "
          "related-video setting.")
    return 0 if not fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
