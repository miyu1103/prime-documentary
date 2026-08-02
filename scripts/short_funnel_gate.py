#!/usr/bin/env python3
"""Refuse to call a Short 'published' until every path to its long-form actually exists.

WHY A GATE AND NOT A CHECKLIST (measured 2026-08-01/02):
  * 43 long-forms are public. A Short is watched by a median of 56 people; the long-form it
    points at, by 24. The funnel is not flowing.
  * Long-form converts ~3.67 subs / 1,000 views vs 0.77 on Shorts — moving a viewer across is
    worth roughly 5x, and it is the only lever that reaches 1,000 subscribers this decade.
  * Every path was already known and none was built: 0/40 descriptions interlink, long-form
    pinned comments zero, 2 playlists across 7 videos, Related-video links 0/38.
    Intention has had months and delivered zero. So this is a gate.

WHAT IT CHECKS (live, against the channel — never a local manifest):
  1. the destination exists, is PUBLIC, and is a long-form (not another Short)
  2. the Short's description carries the destination URL in the first 3 lines
     (on Shorts the description is behind a tap; line 20 is invisible)
  3. the Short and the long-form share a playlist  -> manufactures a co-watch edge
  4. a comment carrying the URL exists on the Short
  5. the Related-video link is set  -> NOT exposed by the Data API, so it cannot be read.
     It is recorded as an explicit owner attestation with a timestamp; without it the gate
     fails. An unverifiable step is not a skippable step.

Usage:
  py -3.11 scripts/short_funnel_gate.py --video <shortVideoId> --longform <longVideoId>
  py -3.11 scripts/short_funnel_gate.py --video ... --longform ... --attest-related-video
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
RECEIPTS = ROOT / "runs" / "short_funnel"
CHANNEL_ALLOWLIST = {"UCuQPtAz1rca9eJ4xhvX0yKA"}


def load_env() -> dict:
    env = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def http(method: str, url: str, *, headers=None, form=None):
    data = urllib.parse.urlencode(form).encode() if form else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def token(env: dict) -> str:
    st, body = http("POST", "https://oauth2.googleapis.com/token", form={
        "client_id": env["YOUTUBE_CLIENT_ID"], "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": env["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"})
    if st != 200:
        sys.exit(f"token failed HTTP {st}: {body.get('error')}")
    return body["access_token"]


def iso_secs(d: str) -> int:
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def video(auth, vid: str) -> dict:
    st, b = http("GET", "https://www.googleapis.com/youtube/v3/videos"
                 f"?part=snippet,status,contentDetails&id={vid}", headers=auth)
    items = b.get("items", [])
    if st != 200 or not items:
        sys.exit(f"could not read {vid} (HTTP {st})")
    return items[0]


def playlists_containing(auth, vid: str) -> set[str]:
    """Every playlist of ours that holds this video."""
    out, page = set(), ""
    st, mine = http("GET", "https://www.googleapis.com/youtube/v3/playlists"
                    f"?part=id,snippet&mine=true&maxResults=50", headers=auth)
    for pl in mine.get("items", []):
        pid, tok = pl["id"], ""
        while True:
            st2, items = http("GET", "https://www.googleapis.com/youtube/v3/playlistItems"
                              f"?part=contentDetails&maxResults=50&playlistId={pid}{tok}", headers=auth)
            if any(i["contentDetails"]["videoId"] == vid for i in items.get("items", [])):
                out.add(pid)
                break
            nxt = items.get("nextPageToken")
            if not nxt:
                break
            tok = f"&pageToken={nxt}"
    return out


def comments_with_url(auth, vid: str, url: str) -> int:
    st, b = http("GET", "https://www.googleapis.com/youtube/v3/commentThreads"
                 f"?part=snippet&videoId={vid}&maxResults=100", headers=auth)
    n = 0
    for t in b.get("items", []):
        txt = t["snippet"]["topLevelComment"]["snippet"].get("textOriginal", "")
        if url in txt or url.split("v=")[-1] in txt:
            n += 1
    return n


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True, help="the Short's video id")
    ap.add_argument("--longform", required=True, help="the long-form it must feed")
    ap.add_argument("--attest-related-video", action="store_true",
                    help="owner confirms the Studio Related-video link is set (unreadable via API)")
    args = ap.parse_args()

    auth = {"Authorization": f"Bearer {token(load_env())}"}
    short, long_ = video(auth, args.video), video(auth, args.longform)
    if short["snippet"]["channelId"] not in CHANNEL_ALLOWLIST:
        sys.exit("video is not on the allowlisted channel")
    url = f"https://www.youtube.com/watch?v={args.longform}"
    desc = short["snippet"].get("description", "")
    head = "\n".join(desc.splitlines()[:3])

    checks = []
    checks.append(("destination is public",
                   long_["status"]["privacyStatus"] == "public",
                   long_["status"]["privacyStatus"]))
    checks.append(("destination is a long-form",
                   iso_secs(long_["contentDetails"]["duration"]) > 185,
                   long_["contentDetails"]["duration"]))
    checks.append(("URL in the first 3 description lines",
                   (url in head) or (args.longform in head),
                   repr(head[:70])))
    sp, lp = playlists_containing(auth, args.video), playlists_containing(auth, args.longform)
    checks.append(("shares a playlist with the long-form", bool(sp & lp),
                   f"short in {len(sp)} playlist(s), long-form in {len(lp)}, shared {len(sp & lp)}"))
    n = comments_with_url(auth, args.video, url)
    checks.append(("a comment carries the URL", n > 0, f"{n} comment(s)"))
    checks.append(("Related-video link set (owner attestation)",
                   args.attest_related_video,
                   "attested" if args.attest_related_video else "NOT attested — Studio > Edit > Related video"))

    print(f"SHORT     {args.video}  {short['snippet']['title'][:60]}")
    print(f"LONG-FORM {args.longform}  {long_['snippet']['title'][:60]}\n")
    ok = True
    for label, passed, detail in checks:
        ok &= bool(passed)
        print(f"  [{'PASS' if passed else 'FAIL'}] {label:<42} {detail}")

    RECEIPTS.mkdir(parents=True, exist_ok=True)
    receipt = RECEIPTS / f"{args.video}.funnel.json"
    receipt.write_text(json.dumps({
        "short": args.video, "longform": args.longform, "url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "checks": [{"check": c, "pass": bool(p), "detail": str(d)} for c, p, d in checks],
        "result": "PASS" if ok else "FAIL",
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nRESULT: {'PASS' if ok else 'FAIL'}   receipt -> {receipt.relative_to(ROOT)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
