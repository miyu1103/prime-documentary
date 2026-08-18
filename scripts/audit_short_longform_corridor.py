#!/usr/bin/env python3
"""Measure, for every PUBLIC Short on the channel, what actually points at a long-form today.

Read-only. Nothing here writes to YouTube.

Three surfaces are checked, and each is reported as measured, not assumed:
  1. DESCRIPTION  - every youtube.com/watch?v= or youtu.be/ id found, classified against the
                    channel's own index (our long-form / our Short / off-channel), plus whether
                    the link is inside the first three lines (the part mobile shows uncollapsed).
  2. COMMENTS     - commentThreads.list per Short, looking for a top-level comment authored by
                    the channel itself and whether that comment carries a long-form link.
                    HONEST LIMIT: the Data API exposes no "isPinned" field on a comment thread.
                    "Owner comment present" is the strongest thing the API can establish; pin
                    state must come from Studio or be treated as unknown.
  3. END SCREENS / CARDS - the Data API has no endpoint for either, at any part=. Additionally
                    YouTube does not render end screens or info cards on Shorts at all, so for a
                    <=180s vertical video this surface is structurally empty. Reported as such
                    rather than left blank.

The Short -> long-form mapping is recovered from the repo, not guessed from titles:
    remotion/src/data/short<NNN>.ts        episodeId: '<EPID>'
    runs/new_shorts/schedule/*.result.json  short<NNN> -> uploaded YouTube id
    episodes/<EPID>/**/*.json               contains the long-form's YouTube id
Anything that cannot be resolved through that chain is reported as UNRESOLVED, never linked to a
plausible-looking episode.

Quota: videos.list ceil(n/50) units + 1 unit per Short for commentThreads.list.

Usage:
  py -3.11 scripts/audit_short_longform_corridor.py            # descriptions only, ~4 units
  py -3.11 scripts/audit_short_longform_corridor.py --comments # + 1 unit per public Short
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yt_channel_index import authorize, fetch_videos, http, iso_seconds, list_video_ids  # noqa: E402
import yt_quota as Q  # noqa: E402

DATA = ROOT / "remotion" / "src" / "data"
CHANNEL_ID = "UCuQPtAz1rca9eJ4xhvX0yKA"
OUT = ROOT / "runs" / "_cache" / "short_corridor_audit.json"

LINK = re.compile(r"(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)([A-Za-z0-9_-]{11})")
SHORT_TS = re.compile(r"^(short\d+[a-z]?)\.ts$")


def short_to_episode() -> dict[str, str]:
    """short id -> episode id, from the Remotion data module each Short was rendered from."""
    out: dict[str, str] = {}
    for f in sorted(DATA.glob("short*.ts")):
        m = SHORT_TS.match(f.name)
        if not m:
            continue
        t = f.read_text("utf-8", errors="replace")
        e = re.search(r"episodeId:\s*['\"]([^'\"]+)['\"]", t)
        if e:
            out[m.group(1)] = e.group(1)
    return out


def short_to_video() -> dict[str, str]:
    """short id -> uploaded YouTube id, from the receipts written at schedule/upload time."""
    out: dict[str, str] = {}
    srcs = list((ROOT / "runs" / "new_shorts" / "schedule").glob("short*.result.json")) + \
        list((ROOT / "episodes").rglob("short*_youtube_schedule_result*.json")) + \
        list((ROOT / "runs" / "new_shorts").rglob("short*.result.json"))
    for p in srcs:
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


def episode_to_longform(long_ids: set[str]) -> dict[str, str]:
    """episode id -> its long-form YouTube id, by finding the id written into the episode dir."""
    out: dict[str, str] = {}
    for ep_dir in sorted((ROOT / "episodes").glob("PD-2026-*")):
        hits: dict[str, int] = {}
        for j in list(ep_dir.rglob("*.json")) + list(ep_dir.rglob("*.md")):
            if "short" in j.name.lower():
                continue
            try:
                txt = j.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for lid in long_ids:
                if lid in txt:
                    hits[lid] = hits.get(lid, 0) + 1
        if hits:
            out[ep_dir.name] = max(hits, key=lambda k: hits[k])
            if len(hits) > 1:
                out[ep_dir.name + "__ambiguous"] = json.dumps(hits)
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--comments", action="store_true", help="also read commentThreads (1u each)")
    args = ap.parse_args()

    auth = authorize(ROOT)
    ids = list_video_ids(auth)
    V = fetch_videos(auth, ids)
    Q.record("videos.list", (len(ids) + 49) // 50)

    dur = {i: iso_seconds(v["contentDetails"]["duration"]) for i, v in V.items()}
    priv = {i: v["status"]["privacyStatus"] for i, v in V.items()}
    shorts = {i for i in V if dur[i] <= 180}
    longs = {i for i in V if dur[i] > 180}
    pub_long = {i for i in longs if priv[i] == "public"}
    pub_short = sorted((i for i in shorts if priv[i] == "public"),
                       key=lambda i: V[i]["snippet"]["publishedAt"])

    ep_of_short = short_to_episode()
    vid_of_short = short_to_video()
    long_of_ep = episode_to_longform(pub_long | (longs - pub_long))
    short_of_vid = {v: s for s, v in vid_of_short.items()}

    print(f"channel index {len(V)} videos | shorts {len(shorts)} (public {len(pub_short)}) | "
          f"long-forms {len(longs)} (public {len(pub_long)})")
    print(f"repo mapping: {len(ep_of_short)} short->episode, {len(vid_of_short)} short->videoId, "
          f"{len([k for k in long_of_ep if not k.endswith('__ambiguous')])} episode->longform\n")

    rows = []
    for vid in pub_short:
        sn = V[vid]["snippet"]
        desc = sn.get("description", "")
        head = "\n".join(desc.splitlines()[:3])
        found = LINK.findall(desc)
        head_found = LINK.findall(head)
        to_long = [f for f in found if f in pub_long]
        head_long = [f for f in head_found if f in pub_long]
        to_priv_long = [f for f in found if f in longs and f not in pub_long]
        sid = short_of_vid.get(vid)
        ep = ep_of_short.get(sid) if sid else None
        expect = long_of_ep.get(ep) if ep else None
        rows.append({
            "video": vid, "short": sid, "episode": ep,
            "title": sn["title"],
            "publishedAt": sn["publishedAt"],
            "desc_lines": len(desc.splitlines()),
            "links_all": found,
            "links_to_public_longform": to_long,
            "link_in_first_3_lines": bool(head_long),
            "links_to_private_longform": to_priv_long,
            "expected_longform": expect,
            "expected_is_public": expect in pub_long if expect else None,
            "link_matches_expected": bool(expect and expect in to_long),
            "resolution": ("ok" if expect else
                           ("no_short_id" if not sid else
                            ("no_episode" if not ep else "no_longform_for_episode"))),
        })

    if args.comments:
        for r in rows:
            st, cr = http("GET", "https://www.googleapis.com/youtube/v3/commentThreads"
                          f"?part=snippet&videoId={r['video']}&maxResults=20&order=relevance",
                          headers=auth)
            Q.record("commentThreads.list")
            if st != 200:
                r["comments"] = {"error": st,
                                 "reason": (cr.get("error", {}).get("errors", [{}])[0]
                                            .get("reason", ""))}
                continue
            items = cr.get("items", [])
            own = []
            for it in items:
                s = it["snippet"]["topLevelComment"]["snippet"]
                if s.get("authorChannelId", {}).get("value") == CHANNEL_ID:
                    txt = s.get("textOriginal", "")
                    own.append({"text": txt[:300], "links": LINK.findall(txt),
                                "publishedAt": s.get("publishedAt")})
            r["comments"] = {
                "total_threads": cr.get("pageInfo", {}).get("totalResults", len(items)),
                "owner_comments": len(own),
                "owner_comment_links_longform": sorted(
                    {l for c in own for l in c["links"] if l in pub_long}),
                "first_thread_is_owner": bool(items) and (
                    items[0]["snippet"]["topLevelComment"]["snippet"]
                    .get("authorChannelId", {}).get("value") == CHANNEL_ID),
                "samples": own[:2],
            }

    # ---- summary ---------------------------------------------------------------------------
    n = len(rows)
    linked = [r for r in rows if r["links_to_public_longform"]]
    head_linked = [r for r in rows if r["link_in_first_3_lines"]]
    correct = [r for r in rows if r["link_matches_expected"]]
    unresolved = [r for r in rows if r["resolution"] != "ok"]
    wrong = [r for r in rows if r["expected_longform"] and r["links_to_public_longform"]
             and not r["link_matches_expected"]]
    nolink = [r for r in rows if not r["links_to_public_longform"]]

    print("=" * 78)
    print(f"PUBLIC SHORTS                                   {n}")
    print(f"  description links to SOME public long-form    {len(linked)}")
    print(f"    ...and that link is in the first 3 lines    {len(head_linked)}")
    print(f"    ...and it is the Short's OWN parent episode {len(correct)}")
    print(f"  links to a long-form that is NOT its parent   {len(wrong)}")
    print(f"  no link to any public long-form               {len(nolink)}")
    print(f"  parent episode UNRESOLVED from the repo       {len(unresolved)}")
    if args.comments:
        oc = [r for r in rows if r.get("comments", {}).get("owner_comments")]
        ocl = [r for r in rows if r.get("comments", {}).get("owner_comment_links_longform")]
        print(f"  owner comment present                         {len(oc)}")
        print(f"    ...carrying a public long-form link         {len(ocl)}")
    print("  end screens / cards                           N/A: Shorts render neither, and the")
    print("                                                Data API exposes no endpoint for them")
    print("=" * 78)

    if nolink:
        print("\nNO LONG-FORM LINK (these are the gap):")
        for r in nolink:
            print(f"  {r['video']}  {str(r['short']):<10} {r['resolution']:<24} "
                  f"exp={r['expected_longform'] or '-'}  {r['title'][:46]}")
    if wrong:
        print("\nLINKS TO A DIFFERENT EPISODE THAN THE REPO SAYS:")
        for r in wrong:
            print(f"  {r['video']}  {r['short']}  has={r['links_to_public_longform']} "
                  f"expected={r['expected_longform']}  {r['title'][:40]}")
    if unresolved:
        print("\nPARENT NOT RECOVERABLE FROM REPO:")
        for r in unresolved:
            print(f"  {r['video']}  {str(r['short']):<10} {r['resolution']:<24} "
                  f"ep={r['episode'] or '-'}  {r['title'][:46]}")

    OUT.write_text(json.dumps({"rows": rows, "long_of_ep": long_of_ep,
                               "pub_long": sorted(pub_long)}, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\nwrote {OUT}")
    print(f"quota after this run: {Q.spent_today()} spent, {Q.remaining()} remaining")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
