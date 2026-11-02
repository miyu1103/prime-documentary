#!/usr/bin/env python3
"""Delete a SCHEDULED/private video from the Prime Documentary channel — fail-closed.

Needed for the back-catalogue re-master: a re-rendered episode has a new sha, but
schedule_<slug>.py's "finalize-if-exists" would re-grab the OLD private video by
title-match and re-publish the DEFECTIVE render. So the old scheduled video must be
DELETED first; only then does the schedule script fresh-upload the fixed file.

Guards (ALL must pass or it refuses):
  - video is on OUR channel (UCuQPtAz1rca9eJ4xhvX0yKA)
  - privacyStatus == "private"  (never delete a public video)
  - snippet.title starts with --expect-title-prefix  (never delete the wrong video)
Dry-run by default; pass --apply to actually delete.

    py -3.11 scripts/delete_scheduled_video.py --id VIDEO_ID --expect-title-prefix "They Hid the Evidence" [--apply]
"""
from __future__ import annotations
import argparse, json, sys, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

CHANNEL = "UCuQPtAz1rca9eJ4xhvX0yKA"


def api_get(token, url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main(argv):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--expect-title-prefix", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv)

    token = _access_token(load_env())
    d = api_get(token, "https://www.googleapis.com/youtube/v3/videos?" +
                urllib.parse.urlencode({"part": "snippet,status", "id": a.id}))
    items = d.get("items", [])
    if not items:
        print(f"BLOCKED: video {a.id} not found"); return 1
    it = items[0]
    ch = it["snippet"].get("channelId")
    priv = it["status"].get("privacyStatus")
    title = it["snippet"].get("title", "")
    print(f"  id={a.id} channel={ch} privacy={priv} title={title!r}")
    if ch != CHANNEL:
        print(f"BLOCKED: not our channel ({ch})"); return 1
    if priv != "private":
        print(f"BLOCKED: privacy is {priv!r}, refusing to delete a non-private video"); return 1
    if not title.startswith(a.expect_title_prefix):
        print(f"BLOCKED: title {title!r} does not start with {a.expect_title_prefix!r}"); return 1
    if not a.apply:
        print("DRY-RUN ok — all guards pass. Re-run with --apply to delete."); return 0
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/videos?" + urllib.parse.urlencode({"id": a.id}),
        headers={"Authorization": f"Bearer {token}"}, method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"DELETED {a.id} (HTTP {r.status})"); return 0
    except urllib.error.HTTPError as e:
        print(f"DELETE FAILED HTTP {e.code}: {e.read().decode()[:200]}"); return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
