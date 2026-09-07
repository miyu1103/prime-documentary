#!/usr/bin/env python
"""Retitle the 3 highest-leverage published videos (PACKAGING_FIX_v001, owner-approved).

Owner approved 2026-07-19: titles only, no thumbnail changes.

SAFETY: videos.update REPLACES the whole snippet, so a partial body silently wipes
description/tags/categoryId/defaultLanguage. This script fetches the CURRENT snippet,
changes ONLY `title`, and sends everything else back byte-identical. The pre-change
snippet of every video is written to a rollback file BEFORE any write.

Dry-run by default. Pass --apply to write.

    python scripts/retitle_packaging_v001.py            # dry run
    python scripts/retitle_packaging_v001.py --apply
    python scripts/retitle_packaging_v001.py --rollback <backup.json>
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"
OUTDIR = ROOT / "episodes" / "_planning"

# (video_id, episode, current title as measured, new title)
# --- wave 2 (2026-07-19): ACCURACY DEFECTS found by PACKAGING_ACCURACY_REVIEW_v001.
# These three are live and factually wrong; the repo's own verified facts contradict two
# of them. Fixed under the owner's standing "run it to completion" authorization.
CHANGES_ACCURACY = [
    ("XWYWAgkExH4", "EP007 riley (MISLABELLED as Carpenter)",
     "Police Pulled 127 Days of His Location",
     "Police Took His Phone. Then They Opened It."),
    ("YhEJHK279f8", "EP028 forfeiture (title contradicts fact_recheck)",
     "They Took Their House Over $40 — and Never Charged Anyone",
     "Their Son Was Charged. The City Came for His Parents' House."),
    ("ch2hQ5jhDmQ", "EP002 gideon (reversed: he WON 9-0)",
     "He Had No Lawyer — So He Beat the Supreme Court",
     "He Had No Lawyer. So He Wrote the Supreme Court in Pencil."),
]

CHANGES = [
    ("tpAKfHKuwqY", "EP027 rodriguez",
     "How Long Can the Police Keep You at a Traffic Stop?",
     "The Traffic Stop Was Over. Then the Dog Arrived."),
    ("bYcqabvvxak", "EP006 terry",
     "Police Searched Him With No Warrant",
     "Police Can Stop and Frisk You Without Arresting You"),
    ("Sz8zPUoBANM", "EP014 lange",
     "Your Front Door Won't Stop the Police",
     "He Drove Home Honking. The Police Followed Him Inside."),
]

# Fields videos.update accepts on snippet. Anything present on the current snippet and
# listed here is echoed back unchanged; `title` is the only value we alter.
SNIPPET_KEYS = ("title", "description", "tags", "categoryId",
                "defaultLanguage", "defaultAudioLanguage")


def load_env() -> dict:
    env = {}
    for line in ENV.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def http(method, url, token=None, body=None, form=None):
    data = None
    headers = {}
    if form:
        data = urllib.parse.urlencode(form).encode()
    elif body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def token() -> str:
    env = load_env()
    st, b = http("POST", "https://oauth2.googleapis.com/token", form={
        "client_id": env["YOUTUBE_CLIENT_ID"], "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": env["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"})
    if st != 200:
        raise SystemExit(f"token refresh failed {st}: {b.get('error')}")
    return b["access_token"]


def fetch(tok, vid):
    st, b = http("GET", f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={vid}", tok)
    if st != 200 or not b.get("items"):
        raise SystemExit(f"fetch failed for {vid}: {st} {json.dumps(b)[:200]}")
    return b["items"][0]["snippet"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually write (default: dry run)")
    ap.add_argument("--accuracy", action="store_true",
                    help="wave 2: fix the three factually-wrong live titles")
    ap.add_argument("--rollback", type=Path, help="restore titles from a backup json")
    a = ap.parse_args()
    tok = token()

    if a.rollback:
        data = json.loads(a.rollback.read_text(encoding="utf-8"))
        for row in data["videos"]:
            snip = fetch(tok, row["video_id"])
            body = {k: snip[k] for k in SNIPPET_KEYS if k in snip}
            body["title"] = row["title_before"]
            st, b = http("PUT", "https://www.googleapis.com/youtube/v3/videos?part=snippet",
                         tok, body={"id": row["video_id"], "snippet": body})
            print(f"{'OK ' if st == 200 else 'ERR'} {row['video_id']} -> {row['title_before']!r}"
                  + ("" if st == 200 else f"  {json.dumps(b)[:160]}"))
        return 0

    backup = {"generated_at": datetime.now(timezone.utc).isoformat(),
              "source": "PACKAGING_FIX_v001", "videos": []}

    todo = CHANGES_ACCURACY if a.accuracy else CHANGES
    for vid, ep, expected_now, new_title in todo:
        snip = fetch(tok, vid)
        cur = snip.get("title", "")
        print(f"\n{ep}  {vid}")
        print(f"  now : {cur}")
        print(f"  new : {new_title}")
        if cur != expected_now:
            print(f"  !! current title differs from the proposal's baseline "
                  f"({expected_now!r}). SKIPPING -- re-check before changing.")
            continue
        if len(new_title) > 100:
            print("  !! title exceeds YouTube's 100-char limit. SKIPPING.")
            continue
        backup["videos"].append({
            "video_id": vid, "episode": ep,
            "title_before": cur, "title_after": new_title,
            "snippet_before": snip,
        })
        if not a.apply:
            print("  (dry run -- no write)")
            continue
        body = {k: snip[k] for k in SNIPPET_KEYS if k in snip}
        body["title"] = new_title
        st, b = http("PUT", "https://www.googleapis.com/youtube/v3/videos?part=snippet",
                     tok, body={"id": vid, "snippet": body})
        if st != 200:
            print(f"  ERROR {st}: {json.dumps(b)[:240]}")
            continue
        got = b.get("snippet", {}).get("title", "")
        print(f"  applied -> {got!r}  {'OK' if got == new_title else 'MISMATCH'}")
        desc_ok = b.get("snippet", {}).get("description", "") == snip.get("description", "")
        print(f"  description preserved: {desc_ok}")

    if backup["videos"]:
        tag = "accuracy" if a.accuracy else "v001"
        p = OUTDIR / (f"packaging_retitle_backup.{tag}.json" if a.apply
                      else f"packaging_retitle_dryrun.{tag}.json")
        p.write_text(json.dumps(backup, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nwrote {p}")
        if a.apply:
            print(f"rollback:  python scripts/retitle_packaging_v001.py --rollback {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
