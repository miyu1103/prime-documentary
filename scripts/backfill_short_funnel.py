#!/usr/bin/env python3
"""Open the funnel on Shorts that are ALREADY PUBLISHED: put the long-form URL on line one of
the description.

Measured 2026-08-01/02, and the reason this is the first thing to run:
  * 46 public Shorts carry 4,391 views between them, and 0 of 46 link to their long-form.
  * A Short converts ~0.77 subscribers per 1,000 views; a long-form ~3.67. Every viewer moved
    across is worth roughly five.
  * These videos already exist and already have the audience. Nothing needs to be produced.

SAFETY (videos.update replaces the whole snippet — a partial write silently drops what it omits):
  * snapshot first: scripts/backup_short_metadata.py (already run; runs/short_funnel/)
  * title, tags, categoryId and the language fields are read back and re-sent unchanged
  * `status` is never sent, so publishAt cannot be disturbed
  * a Short whose destination is not PUBLIC is skipped, not linked to a dead page
  * a Short that already links out is skipped
  * --dry-run is the default; --apply is required to write

Usage:
  py -3.11 scripts/backfill_short_funnel.py
  py -3.11 scripts/backfill_short_funnel.py --apply --limit 3
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
WATCH = "https://www.youtube.com/watch?v={vid}"


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
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def secs(t: str) -> int:
    m = re.match(r"^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$", (t or "").strip())
    if not m or not any(m.groups()):
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


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
    """shortNN -> published video id, from the upload/schedule receipts on disk."""
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
    ap.add_argument("--apply", action="store_true", help="actually write (default is dry-run)")
    ap.add_argument("--limit", type=int, default=0, help="cap how many videos are touched")
    args = ap.parse_args()

    snap = sorted(RUNS.glob("metadata_backup.*.json"))
    if not snap:
        sys.exit("no metadata backup — run scripts/backup_short_metadata.py first")
    rows = {r["id"]: r for r in json.loads(snap[-1].read_text(encoding="utf-8"))}
    longs = {r["id"]: r for r in rows.values() if r["duration_sec"] > 185 and r["privacy"] == "public"}

    ep_of_short = short_to_episode()
    vid_of_short = video_id_of_short()

    # episode -> its public long-form, matched through the episode's own package receipts
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

    plan, skipped = [], []
    for short_id, vid in sorted(vid_of_short.items()):
        row = rows.get(vid)
        if not row or row["privacy"] != "public" or row["duration_sec"] > 185:
            skipped.append((short_id, vid, "not a public Short")); continue
        ep = ep_of_short.get(short_id)
        lid = ep_long.get(ep) if ep else None
        if not lid:
            skipped.append((short_id, vid, f"no public long-form for {ep}")); continue
        url = WATCH.format(vid=lid)
        head = "\n".join((row["description"] or "").splitlines()[:3])
        if lid in head:
            skipped.append((short_id, vid, "already links out")); continue
        block = f"▶ FULL CASE: {longs[lid]['title']}\n{url}\n\n"
        plan.append({"short": short_id, "video": vid, "title": row["title"],
                     "longform": lid, "new_description": block + (row["description"] or "")})
        if args.limit and len(plan) >= args.limit:
            break

    print(f"{len(plan)} Shorts will get a first-line link; {len(skipped)} skipped")
    for s in plan:
        print(f"  {s['short']:<9} {s['video']}  ->  {s['longform']}  {s['title'][:46]}")
    if skipped:
        print("\n  skipped:")
        for sid, vid, why in skipped[:12]:
            print(f"    {sid:<9} {vid}  {why}")
        if len(skipped) > 12:
            print(f"    ... {len(skipped)-12} more")

    if not args.apply:
        print("\nDRY RUN — nothing written. Re-run with --apply to write.")
        return 0

    auth_env = load_env()
    st, tk = http("POST", "https://oauth2.googleapis.com/token", form={
        "client_id": auth_env["YOUTUBE_CLIENT_ID"], "client_secret": auth_env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": auth_env["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"})
    if st != 200:
        sys.exit(f"token failed HTTP {st}")
    auth = {"Authorization": f"Bearer {tk['access_token']}"}

    ok = fail = 0
    receipts = []
    for s in plan:
        st, cur = http("GET", "https://www.googleapis.com/youtube/v3/videos"
                       f"?part=snippet,status&id={s['video']}", headers=auth)
        items = cur.get("items", [])
        if st != 200 or not items:
            print(f"  {s['short']} READ FAILED {st}"); fail += 1; continue
        v = items[0]
        if v["snippet"].get("channelId") not in CHANNEL_ALLOWLIST:
            print(f"  {s['short']} NOT ON ALLOWLISTED CHANNEL — skipped"); fail += 1; continue
        sn = v["snippet"]
        # re-send everything we read; omit `status` entirely so publishAt cannot be disturbed
        payload = {"id": s["video"], "snippet": {
            "title": sn["title"], "description": s["new_description"],
            "categoryId": sn.get("categoryId", "27"), "tags": sn.get("tags", []),
            **({"defaultLanguage": sn["defaultLanguage"]} if sn.get("defaultLanguage") else {}),
        }}
        st, res = http("PUT", "https://www.googleapis.com/youtube/v3/videos?part=snippet",
                       headers=auth, body=payload)
        if st == 200:
            ok += 1
            print(f"  {s['short']:<9} linked -> {s['longform']}")
            receipts.append({"short": s["short"], "video": s["video"], "longform": s["longform"],
                             "at": datetime.now(timezone.utc).isoformat()})
        else:
            fail += 1
            print(f"  {s['short']:<9} WRITE FAILED {st}: {res.get('error', {}).get('message', '')[:110]}")

    RUNS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (RUNS / f"backfill.{stamp}.json").write_text(
        json.dumps({"applied": receipts, "ok": ok, "failed": fail}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nlinked {ok}, failed {fail}  (~{ok*50} quota units used)")
    return 0 if not fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
