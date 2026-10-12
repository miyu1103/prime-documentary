#!/usr/bin/env python3
"""Put every Short and its long-form into the SAME playlist, so YouTube is told they belong together.

Why this and not just a description link: the repo's own analytics read shows PLAYLIST traffic at
19.6 minutes per view against 0.16 for Shorts, on 1.1% of views. A shared playlist also
manufactures a co-watch edge, which is the input the suggested-video graph actually runs on — and
100% of our current suggested traffic is borrowed from other channels' videos.

One playlist per episode ("<long-form title> — full case + shorts"), long-form first so the
playlist opens on the destination.

SAFETY: creates and appends only. Never deletes, never reorders an existing playlist, never
touches video status. --dry-run is the default.

Quota: playlists.insert 50, playlistItems.insert 50 each. Budget before running.

Usage:
  py -3.11 scripts/pair_short_playlists.py
  py -3.11 scripts/pair_short_playlists.py --apply --limit 5
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "remotion" / "src" / "data"
RUNS = ROOT / "runs" / "short_funnel"
CHANNEL_ALLOWLIST = {"UCuQPtAz1rca9eJ4xhvX0yKA"}


def load_env() -> dict:
    env = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def http(method: str, url: str, *, headers=None, form=None, body=None):
    data = urllib.parse.urlencode(form).encode() if form else (
        json.dumps(body).encode() if body is not None else None)
    h = dict(headers or {})
    if body is not None:
        h["Content-Type"] = "application/json"
    try:
        with urllib.request.urlopen(
                urllib.request.Request(url, data=data, method=method, headers=h), timeout=40) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def short_to_episode() -> dict[str, str]:
    out = {}
    for f in sorted(DATA.glob("short*.ts")):
        if f.name.endswith("_timing.ts"):
            continue
        m = re.search(r"episodeId:\s*'([^']+)'", f.read_text("utf-8", errors="replace"))
        if m:
            out[f.stem] = m.group(1)
    return out


def video_id_of_short() -> dict[str, str]:
    out = {}
    for p in list((ROOT / "runs" / "new_shorts" / "schedule").glob("short*.result.json")) + \
             list((ROOT / "episodes").rglob("short*_youtube_schedule_result.v001.json")):
        m = re.match(r"(short\d+[a-z]?)", p.name)
        if not m:
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        vid = d.get("video_id") or d.get("videoId") or (d.get("response") or {}).get("id")
        if isinstance(vid, str) and len(vid) == 11:
            out.setdefault(m.group(1), vid)
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    snap = sorted(RUNS.glob("metadata_backup.*.json"))
    if not snap:
        sys.exit("run scripts/backup_short_metadata.py first")
    rows = {r["id"]: r for r in json.loads(snap[-1].read_text(encoding="utf-8"))}
    longs = {i: r for i, r in rows.items() if r["duration_sec"] > 185 and r["privacy"] == "public"}

    ep_of_short, vid_of_short = short_to_episode(), video_id_of_short()
    ep_long = {}
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

    # group the public Shorts by the long-form they feed
    groups: dict[str, list[tuple[str, str]]] = {}
    for sid, vid in sorted(vid_of_short.items()):
        r = rows.get(vid)
        if not r or r["privacy"] != "public" or r["duration_sec"] > 185:
            continue
        lid = ep_long.get(ep_of_short.get(sid, ""), None)
        if lid:
            groups.setdefault(lid, []).append((sid, vid))

    if args.limit:
        groups = dict(list(groups.items())[:args.limit])
    total_items = sum(1 + len(v) for v in groups.values())
    print(f"{len(groups)} playlists to create, {total_items} items to add "
          f"(~{len(groups)*50 + total_items*50} quota units)")
    for lid, members in groups.items():
        print(f"  {longs[lid]['title'][:52]:<54} <- {', '.join(s for s, _ in members)}")

    if not args.apply:
        print("\nDRY RUN — nothing written. Re-run with --apply.")
        return 0

    env = load_env()
    st, tk = http("POST", "https://oauth2.googleapis.com/token", form={
        "client_id": env["YOUTUBE_CLIENT_ID"], "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": env["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"})
    if st != 200:
        sys.exit(f"token failed HTTP {st}")
    auth = {"Authorization": f"Bearer {tk['access_token']}"}

    st, existing = http("GET", "https://www.googleapis.com/youtube/v3/playlists"
                        "?part=id,snippet&mine=true&maxResults=50", headers=auth)
    by_title = {p["snippet"]["title"]: p["id"] for p in existing.get("items", [])}

    made, added, failed, receipts = 0, 0, 0, []
    for lid, members in groups.items():
        title = (longs[lid]["title"][:80] + " — full case + shorts")[:150]
        pid = by_title.get(title)
        if not pid:
            st, pl = http("POST", "https://www.googleapis.com/youtube/v3/playlists?part=snippet,status",
                          headers=auth, body={
                              "snippet": {"title": title,
                                          "description": "The full case, followed by the short cuts from it."},
                              "status": {"privacyStatus": "public"}})
            if st != 200:
                print(f"  playlist FAILED {st}: {pl.get('error', {}).get('message','')[:100]}")
                failed += 1
                continue
            pid = pl["id"]
            made += 1
        for vid in [lid] + [v for _, v in members]:      # long-form first
            st, res = http("POST", "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet",
                           headers=auth, body={"snippet": {
                               "playlistId": pid,
                               "resourceId": {"kind": "youtube#video", "videoId": vid}}})
            if st == 200:
                added += 1
            else:
                failed += 1
                print(f"  add {vid} FAILED {st}: {res.get('error', {}).get('message','')[:90]}")
        receipts.append({"playlist": pid, "title": title, "longform": lid,
                         "shorts": [v for _, v in members]})
        print(f"  {title[:60]:<62} {len(members)+1} items")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (RUNS / f"playlists.{stamp}.json").write_text(
        json.dumps({"created": made, "items_added": added, "failed": failed, "playlists": receipts},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\ncreated {made} playlists, added {added} items, failed {failed}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
