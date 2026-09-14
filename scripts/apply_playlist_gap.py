#!/usr/bin/env python3
"""Close the measured playlist gap, in evidence order, stopping the moment quota runs out.

scripts/audit_playlist_coverage.py measured four public playlists holding 50 of the 56 public
long-forms. Six long-forms belong to no playlist. This places the ones that are allowed to move
and refuses the one that is not.

Every task carries the reason it is in this order, and tasks run strictly one at a time so a
403 quotaExceeded costs one task and not a half-written playlist.

LOCK: anything published or scheduled on/after 2026-08-10 is refused, checked against the live
`status` object rather than a local list.

SAFETY: playlistItems.insert and playlists.update only. No video resource is written, so no
video's privacyStatus or publishAt is reachable from this file at all. Nothing is deleted and
no existing item is removed.

Usage:
  py -3.11 scripts/apply_playlist_gap.py
  py -3.11 scripts/apply_playlist_gap.py --apply [--max-tasks N]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yt_channel_index import authorize, fetch_videos, http  # noqa: E402
import yt_quota as Q  # noqa: E402

API = "https://www.googleapis.com/youtube/v3"
LOCK_FROM = datetime(2026, 8, 10, 0, 0, tzinfo=timezone.utc)
RECEIPTS = ROOT / "runs" / "short_funnel"

SYSTEM = "PLfPI0t-nSRxw"
FORFEIT = "PLd04glUie5rg"
FRAUD = "PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P"
POLICE = "PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9"

# (kind, playlist, payload, why-this-rank)
TASKS = [
    ("add", FRAUD, "dNhu-IJUc5k",
     "EP60 Surfside (repo: episodes/PD-2026-060-surfside/09_package/youtube_schedule_result"
     ".v001.json). Money-and-institutions is the theme that produced 4 of the channel's 7 "
     "long-form subscribers, so an orphan in that spine is placed before anything else. The "
     "playlist's own description already promises 'the warnings nobody acted on'."),
    ("add", FRAUD, "Wo-SvvGsv8g",
     "EP59 robo-signing (episodes/PD-2026-059-robosigning/.../youtube_schedule_result.v001.json)."
     " A bank, not the government, takes the house - so it belongs in Fraud/Finance and NOT in "
     "The Forfeiture Files, whose title promises government takings."),
    ("add", SYSTEM, "PfdEpNQyaQQ",
     "EP54 Curtis Flowers (episodes/PD-2026-054-flowers/.../youtube_schedule_result.v002.json). "
     "Six trials by one prosecutor is the purest statement of this playlist's premise."),
    ("add", SYSTEM, "4FlCaOVpln0",
     "EP56 Post Office Horizon (episodes/PD-2026-056-postoffice/.../youtube_schedule_result"
     ".v002.json). Wrongful prosecutions manufactured by an accounting system."),
    ("add", SYSTEM, "Iw-EPUD2nHg",
     "EP55 Burge (episodes/PD-2026-055-burge/.../youtube_schedule_result.v002.json). Filed under "
     "wrongful convictions rather than Police Power on the measurement that Police Power's 24 "
     "episodes have produced 0 subscribers while this playlist has produced 2."),
    ("desc", SYSTEM, None,
     "The description opens 'Eight cases' and the playlist already held nine before today's "
     "adds. A count that contradicts the shelf is the one thing a browsing viewer can check."),
    ("first", POLICE, "bSnyfsulna8",
     "Position 0 is the recruiter. Police Power currently opens on tpAKfHKuwqY: 14 views, 41.6% "
     "APV. bSnyfsulna8 has 108 views at 39.6% APV - 7.7x the reach for 2 points of retention. "
     "Last because it is an optimisation, not a gap."),
]

NEW_SYSTEM_DESC = (
    "Twelve cases the system never answered for: men who spent decades in prison for crimes they "
    "did not commit, confessions taken in rooms with no camera, a judge who was paid by the jail "
    "he sent children to, evidence that stayed buried, and disappearances still open after fifty "
    "years.\n\n"
    "Watch in order - the wrongful convictions first, then the cases nobody ever closed."
)


def iso(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--max-tasks", type=int, default=99)
    args = ap.parse_args()

    auth = authorize(ROOT)
    vids = [t[2] for t in TASKS if t[0] in ("add", "first") and t[2]]
    V = fetch_videos(auth, vids, part="snippet,status")
    Q.record("videos.list")

    plan, refused = [], []
    for kind, pl, payload, why in TASKS:
        if kind in ("add", "first"):
            v = V.get(payload)
            if not v:
                refused.append((payload, "not on channel")); continue
            pa = v["status"].get("publishAt") or v["snippet"]["publishedAt"]
            if iso(pa) >= LOCK_FROM:
                refused.append((payload, f"published/scheduled {pa}, on or after the "
                                         f"2026-08-10 lock")); continue
            if v["status"]["privacyStatus"] != "public":
                refused.append((payload, f"{v['status']['privacyStatus']}, not public")); continue
        plan.append({"kind": kind, "playlist": pl, "video": payload, "why": why,
                     "title": V[payload]["snippet"]["title"] if payload in V else ""})

    print(f"planned {len(plan)} tasks | refused {len(refused)}\n")
    for v, wh in refused:
        print(f"  REFUSED {v}: {wh}")
    for n, t in enumerate(plan, 1):
        print(f"\n{n}. {t['kind'].upper():<6} {t['playlist']}  {t['video'] or ''}  "
              f"{t['title'][:50]}")
        print(f"   cost 50u. {t['why']}")
    print(f"\ntotal cost if all run: {50 * len(plan)} units")

    if not args.apply:
        print("\ndry run. nothing written.")
        return 0

    done, stopped = [], None
    for t in plan[:args.max_tasks]:
        if t["kind"] == "add":
            st, r = http("POST", f"{API}/playlistItems?part=snippet", headers=auth, body={
                "snippet": {"playlistId": t["playlist"],
                            "resourceId": {"kind": "youtube#video", "videoId": t["video"]}}})
            Q.record("playlistItems.insert")
        elif t["kind"] == "desc":
            st, cur = http("GET", f"{API}/playlists?part=snippet&id={t['playlist']}", headers=auth)
            Q.record("playlistItems.list")
            if st != 200:
                stopped = ("desc-read", st, cur); break
            sn = cur["items"][0]["snippet"]
            st, r = http("PUT", f"{API}/playlists?part=snippet", headers=auth, body={
                "id": t["playlist"],
                "snippet": {"title": sn["title"], "description": NEW_SYSTEM_DESC,
                            **({"defaultLanguage": sn["defaultLanguage"]}
                               if sn.get("defaultLanguage") else {})}})
            Q.record("videos.update")           # playlists.update is also 50
        else:  # first
            st, li = http("GET", f"{API}/playlistItems?part=snippet&playlistId={t['playlist']}"
                                 f"&maxResults=50", headers=auth)
            Q.record("playlistItems.list")
            if st != 200:
                stopped = ("first-read", st, li); break
            item = next((i for i in li["items"]
                         if i["snippet"]["resourceId"]["videoId"] == t["video"]), None)
            if not item:
                stopped = ("first-missing", 0, t["video"]); break
            st, r = http("PUT", f"{API}/playlistItems?part=snippet", headers=auth, body={
                "id": item["id"],
                "snippet": {"playlistId": t["playlist"], "position": 0,
                            "resourceId": {"kind": "youtube#video", "videoId": t["video"]}}})
            Q.record("videos.update")

        ok = st in (200, 201)
        print(f"  {'OK  ' if ok else 'FAIL'} {t['kind']:<6} {t['playlist']} {t['video'] or ''} "
              f"HTTP {st}" + ("" if ok else f"  {json.dumps(r)[:200]}"))
        if not ok:
            stopped = (t["kind"], st, r)
            print("  stopping here; remaining tasks are unattempted and can be resumed")
            break
        done.append(t)

    # ---- independent re-read of the playlists we touched -----------------------------
    print("\nre-reading every playlist that was touched:")
    for pid in dict.fromkeys(t["playlist"] for t in done):
        st, p = http("GET", f"{API}/playlists?part=snippet,contentDetails&id={pid}", headers=auth)
        st2, li = http("GET", f"{API}/playlistItems?part=snippet&playlistId={pid}"
                              f"&maxResults=50", headers=auth)
        Q.record("playlistItems.list", 2)
        got = [i["snippet"]["resourceId"]["videoId"] for i in li.get("items", [])]
        want_add = [t["video"] for t in done if t["kind"] == "add" and t["playlist"] == pid]
        missing = [v for v in want_add if v not in got]
        line = f"  {pid}  {p['items'][0]['contentDetails']['itemCount']} items"
        line += "  adds present" if not missing else f"  MISSING {missing}"
        if any(t["kind"] == "first" and t["playlist"] == pid for t in done):
            wanted = next(t["video"] for t in done
                          if t["kind"] == "first" and t["playlist"] == pid)
            line += f"  | position 0 = {got[0]} " + ("(as intended)" if got[0] == wanted
                                                     else f"MISMATCH, wanted {wanted}")
        if any(t["kind"] == "desc" and t["playlist"] == pid for t in done):
            line += "  | description " + ("updated" if p["items"][0]["snippet"]["description"]
                                          == NEW_SYSTEM_DESC else "MISMATCH")
        print(line)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    (RECEIPTS / f"playlist_gap.{stamp}.json").write_text(
        json.dumps({"done": done, "stopped": stopped, "refused": refused},
                   indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(done)}/{len(plan)} tasks landed. receipt in {RECEIPTS}")
    if stopped:
        print("stopped on:", stopped[0], "HTTP", stopped[1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
