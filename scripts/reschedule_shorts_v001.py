#!/usr/bin/env python3
"""Move an already-scheduled Short to a different publishAt (no re-upload, no delete).

The videos stay private and keep their video_id, thumbnail, description and title; only
status.publishAt changes. Use this when a batch was booked onto the wrong days — deleting and
re-uploading would burn quota and mint new IDs for no reason.

Owner instruction 2026-07-30: the three new Shorts must run on CONSECUTIVE days in NUMBER order,
not split across a backfilled gap. short60 -> 8/22, short63 -> 8/23, short66 -> 8/24.

Rewrites the two receipts that record the date so nothing on disk disagrees with the channel:
  runs/new_shorts/schedule/short<NN>.result.json
  episodes/<EP>/09_package/short<NN>_youtube_schedule_result.v001.json

    py -3.11 scripts/reschedule_shorts_v001.py --dry-run
    py -3.11 scripts/reschedule_shorts_v001.py
"""
from __future__ import annotations
import argparse, json, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

CHANNEL_ALLOWLIST = {"UCuQPtAz1rca9eJ4xhvX0yKA"}
RESULTS = ROOT / "runs" / "new_shorts" / "schedule"
EP_BY_N = {60: "PD-2026-053-norfolk", 63: "PD-2026-054-flowers", 66: "PD-2026-055-burge"}

# (short number, video_id, new publishAt UTC) — 12:00 JST = 03:00Z
MOVES = [
    (63, "qvjB7RvpuUc", "2026-08-23T03:00:00Z"),
    (60, "9r2CrlG5IlU", "2026-08-22T03:00:00Z"),
    (66, "xhoGSk8JA5c", "2026-08-24T03:00:00Z"),
]


def get(tok, vid):
    r = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part=status,snippet&id={vid}",
        headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(r, timeout=60) as resp:
        items = json.loads(resp.read().decode())["items"]
    if not items:
        raise RuntimeError(f"video {vid} not found")
    return items[0]


def channel_id(tok):
    r = urllib.request.Request("https://www.googleapis.com/youtube/v3/channels?part=id&mine=true",
                               headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode())["items"][0]["id"]


def set_publish_at(tok, vid, when):
    body = json.dumps({"id": vid, "status": {"privacyStatus": "private", "publishAt": when,
                                             "selfDeclaredMadeForKids": False}}).encode()
    r = urllib.request.Request("https://www.googleapis.com/youtube/v3/videos?part=status", data=body,
                               headers={"Authorization": f"Bearer {tok}",
                                        "Content-Type": "application/json"}, method="PUT")
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode())


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    for _, _, when in MOVES:
        if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", when):
            raise RuntimeError(f"bad publishAt {when}")

    tok = _access_token(load_env())
    ch = channel_id(tok)
    if ch not in CHANNEL_ALLOWLIST:
        print(f"BLOCKED: channel {ch} not allowlisted"); return 1
    print(f"OK channel {ch}")

    for n, vid, when in MOVES:
        v = get(tok, vid)
        cur = v["status"].get("publishAt", "-")
        priv = v["status"]["privacyStatus"]
        title = v["snippet"]["title"][:52]
        print(f"  short{n} {vid} [{priv}] {cur} -> {when}   {title}")
        if priv != "private":
            print(f"  BLOCKED: short{n} is {priv}, not private — refusing to touch a live video")
            return 1
        if args.dry_run:
            continue
        set_publish_at(tok, vid, when)
        for p in (RESULTS / f"short{n}.result.json",
                  ROOT / "episodes" / EP_BY_N[n] / "09_package" / f"short{n}_youtube_schedule_result.v001.json"):
            if p.exists():
                d = json.loads(p.read_text(encoding="utf-8"))
                d["publishAt"] = when
                p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                print(f"      receipt updated: {p.relative_to(ROOT)}")

    if args.dry_run:
        print("[dry-run] nothing changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
