#!/usr/bin/env python3
r"""Apply SUBSCRIBE_HEADER_BATCH.v001.json to LIVE videos (videos.update, snippet only).

This is the write half of scripts/stage_subscribe_header_batch.py. It is a near-copy of
scripts/apply_description_batch.py, kept separate so the two batches cannot share a receipt
and silently skip each other's videos.

Safety, in the order it matters:

1. **status is never sent.** part=snippet only. privacyStatus and publishAt are not in the
   request body and therefore cannot move. A past-dated publishAt has published a video
   immediately and publicly on this channel once already; this path cannot repeat that.
2. **Full-snippet round trip.** videos.update?part=snippet CLEARS any snippet field the
   request omits, so the live snippet is fetched and resent verbatim with only `description`
   replaced. title, tags, categoryId and defaultLanguage keep their live values.
3. **Staleness fence.** The live description is re-read at write time and compared with
   `description_before`. If anyone edited the video since staging, the item is refused.
4. **Verify from the API, not from the request.** After the 200 the description is re-read
   and compared. The read is eventually consistent, so it retries before calling it a failure.
5. **Resumable.** Applied ids are recorded; re-running skips them.

Quota: 1 unit per read, 50 per write. A full pass over 56 long-forms is ~2,970 of 10,000.

    py -3.11 scripts/apply_subscribe_header_batch.py            # dry run (default)
    py -3.11 scripts/apply_subscribe_header_batch.py --apply
    py -3.11 scripts/apply_subscribe_header_batch.py --apply --limit 3
"""
from __future__ import annotations

import argparse
import json
import sys
import time
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
BATCH = ROOT / "episodes" / "_planning" / "measurements" / "SUBSCRIBE_HEADER_BATCH.v001.json"
RECEIPT = ROOT / "episodes" / "_planning" / "measurements" / "SUBSCRIBE_HEADER_APPLY.v001.json"
CHANNEL_ID = "UCuQPtAz1rca9eJ4xhvX0yKA"
SPACING_S = 1.5
MAX_DESCRIPTION_CHARS = 5000


def load_env() -> dict:
    env = {}
    for line in ENV.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def token() -> str:
    env = load_env()
    data = urllib.parse.urlencode({
        "client_id": env["YOUTUBE_CLIENT_ID"],
        "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": env["YOUTUBE_REFRESH_TOKEN"],
        "grant_type": "refresh_token"}).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def get_video(tok: str, vid: str) -> dict | None:
    req = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id={vid}",
        headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        items = json.loads(r.read().decode()).get("items", [])
    return items[0] if items else None


def put_description(tok: str, vid: str, snippet: dict, text: str):
    body = {"id": vid, "snippet": {**snippet, "description": text}}
    body["snippet"].pop("thumbnails", None)
    body["snippet"].pop("localized", None)
    assert "status" not in body, "status must never be sent"
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/videos?part=snippet",
        data=json.dumps(body).encode("utf-8"), method="PUT",
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def normalise(text: str) -> str:
    return (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    done: dict = {}
    if RECEIPT.is_file():
        done = {r["video_id"]: r
                for r in json.loads(RECEIPT.read_text(encoding="utf-8")).get("applied", [])}

    items = batch["items"]
    if args.only:
        items = [i for i in items if i["video_id"] in set(args.only)]

    tok = token()
    applied, skipped, failed = [], [], []
    reads = writes = 0

    for item in items:
        vid, title = item["video_id"], item["title"][:48]
        if args.limit is not None and len([a for a in applied if not a.get("dry_run")]) >= args.limit:
            break
        if vid in done:
            skipped.append((vid, "already applied"))
            continue
        after = item["description_after"]
        if len(after) > MAX_DESCRIPTION_CHARS:
            failed.append((vid, f"{len(after)} chars over the 5000 cap"))
            continue

        live = get_video(tok, vid)
        reads += 1
        if live is None:
            failed.append((vid, "video not found"))
            continue
        if live["status"]["privacyStatus"] != "public":
            # The batch is public back-catalogue only. A non-public video here means the
            # channel state moved under us; refuse rather than touch a scheduled item.
            skipped.append((vid, f"no longer public ({live['status']['privacyStatus']})"))
            continue
        snippet = live["snippet"]
        if normalise(snippet.get("description")) == normalise(after):
            skipped.append((vid, "live already matches"))
            continue
        if normalise(snippet.get("description")) != normalise(item["description_before"]):
            skipped.append((vid, "STALE - live description changed since staging"))
            continue

        if not args.apply:
            print(f"DRY  {vid}  {title:50} {item['chars_before']:>5} -> {item['chars_after']:<5} "
                  f"[{item['header_tier']}]")
            applied.append({"video_id": vid, "dry_run": True})
            continue

        status, body = put_description(tok, vid, snippet, after)
        writes += 1
        ok = status == 200
        if ok:
            for attempt in range(4):
                check = get_video(tok, vid)
                reads += 1
                if normalise((check or {}).get("snippet", {}).get("description")) == \
                        normalise(after):
                    break
                time.sleep(2 * (attempt + 1))
            else:
                ok = False
                body = {"error": "read-back did not match after 4 attempts"}
        if ok:
            applied.append({
                "video_id": vid, "title": item["title"], "header_tier": item["header_tier"],
                "chars_before": item["chars_before"], "chars_after": item["chars_after"],
                "applied_at": datetime.now(timezone.utc).isoformat(),
            })
            print(f"OK   {vid}  {title:50} {item['chars_before']:>5} -> {item['chars_after']}",
                  flush=True)
        else:
            failed.append((vid, f"HTTP {status} {json.dumps(body)[:140]}"))
            print(f"FAIL {vid}  {title:50} HTTP {status}", flush=True)
            break  # quota or auth: every later item would fail the same way
        time.sleep(SPACING_S)

    for vid, why in skipped:
        print(f"skip {vid}  {why}")
    n_applied = len([a for a in applied if not a.get("dry_run")])
    print(f"\napplied={n_applied} dry={len(applied) - n_applied} "
          f"skipped={len(skipped)} failed={len(failed)}")
    print(f"quota this run: {reads} reads + {writes} writes x50 = {reads + writes * 50} units")
    for vid, why in failed:
        print(f"  FAILED {vid}: {why}")

    if args.apply:
        prev = json.loads(RECEIPT.read_text(encoding="utf-8")).get("applied", []) \
            if RECEIPT.is_file() else []
        RECEIPT.write_text(json.dumps({
            "schema_version": "1.0.0",
            "generator": "scripts/apply_subscribe_header_batch.py",
            "channel_id": CHANNEL_ID,
            "source_batch": str(BATCH.relative_to(ROOT).as_posix()),
            "last_run_at": datetime.now(timezone.utc).isoformat(),
            "quota_units_last_run": reads + writes * 50,
            "applied": prev + [a for a in applied if not a.get("dry_run")],
            "skipped": [{"video_id": v, "reason": w} for v, w in skipped],
            "failed": [{"video_id": v, "reason": w} for v, w in failed],
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"receipt: {RECEIPT}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
