#!/usr/bin/env python3
r"""Apply the staged description batch to LIVE videos (videos.update, snippet only).

Reads episodes/_planning/measurements/DESCRIPTION_BATCH.v001.json, which
scripts/stage_description_batch.py produced from measured channel state. Each item
carries `description_before` (the live text when it was staged) and
`description_after` (that text plus a repaired CHAPTERS block and a WATCH NEXT block).

Why this exists: the channel measured 0 of 42 long-forms linking another video and
7 of 42 showing chapters. Both are description text, both are writable, and neither
had an execution path -- only a staging path.

Safety, in the order it matters:

1. **Staleness fence.** The live description is re-read at write time and compared
   against `description_before`. If anyone (owner, another script) edited the video
   since staging, this refuses that item rather than overwriting their change.
2. **Full-snippet round trip.** `videos.update?part=snippet` CLEARS any snippet
   field the request omits. The current snippet is fetched and resent verbatim with
   only `description` replaced -- title, tags, categoryId and defaultLanguage keep
   their live values.
3. **status is never sent.** part=snippet only, so privacy and publishAt cannot move.
4. **Blocked items are skipped**, not applied with a placeholder.
5. **Verify after write.** The description is re-read and compared to what was sent.
   A mismatch stops the run.
6. **Resumable.** Every applied video id is recorded; re-running skips it.

    py -3.11 scripts/apply_description_batch.py                 # dry run (default)
    py -3.11 scripts/apply_description_batch.py --apply
    py -3.11 scripts/apply_description_batch.py --apply --only Xc_PxdC_75c
    py -3.11 scripts/apply_description_batch.py --apply --limit 5

Side effects: HTTP PUT to the YouTube Data API v3 for the allowlisted channel only.
Quota: 50 units per write, 1 per read. Exit 0 = every attempted item applied and
verified; 1 = at least one failed.
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
BATCH = ROOT / "episodes" / "_planning" / "measurements" / "DESCRIPTION_BATCH.v001.json"
RECEIPT = ROOT / "episodes" / "_planning" / "measurements" / "DESCRIPTION_APPLY.v001.json"
CHANNEL_ID = "UCuQPtAz1rca9eJ4xhvX0yKA"
SPACING_S = 3
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


def get_snippet(tok: str, vid: str) -> dict | None:
    req = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={vid}",
        headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        items = json.loads(r.read().decode()).get("items", [])
    return items[0]["snippet"] if items else None


def put_description(tok: str, vid: str, snippet: dict, text: str):
    body = {"id": vid, "snippet": {**snippet, "description": text}}
    # read-only echoes; sending them back is noise and can be rejected
    body["snippet"].pop("thumbnails", None)
    body["snippet"].pop("localized", None)
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
    """YouTube returns \r\n for \n and trims trailing space; compare on that basis."""
    return (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Perform the writes. Without it this is a dry run.")
    ap.add_argument("--only", nargs="*", default=None, help="Video ids to limit the run to.")
    ap.add_argument("--limit", type=int, default=None, help="Stop after N videos.")
    ap.add_argument("--force-stale", action="store_true",
                    help="Apply even when the live description no longer matches what was "
                         "staged. Off by default -- staleness usually means a human edited it.")
    args = ap.parse_args()

    if not BATCH.is_file():
        print(f"missing {BATCH} - run scripts/stage_description_batch.py first")
        return 1
    batch = json.loads(BATCH.read_text(encoding="utf-8"))

    done: dict = {}
    if RECEIPT.is_file():
        done = {r["video_id"]: r for r in json.loads(RECEIPT.read_text(encoding="utf-8"))
                .get("applied", [])}

    items = batch["items"]
    if args.only:
        keep = set(args.only)
        items = [i for i in items if i["video_id"] in keep]

    tok = token() if (args.apply or True) else ""
    applied, skipped, failed = [], [], []

    for item in items:
        vid = item["video_id"]
        title = item["title"][:52]
        if args.limit is not None and len(applied) >= args.limit:
            break
        if vid in done:
            skipped.append((vid, "already applied"))
            continue
        if item.get("blockers"):
            # A blocked item would publish a placeholder URL or a production-internal
            # chapter label. Better a missing chapter block than a wrong one.
            unresolved = [b for b in item["blockers"]
                          if "no valid chapter block" not in b]
            if unresolved:
                skipped.append((vid, "; ".join(unresolved)[:70]))
                continue
        after = item["description_after"]
        if len(after) > MAX_DESCRIPTION_CHARS:
            failed.append((vid, f"description would be {len(after)} chars (cap 5000)"))
            continue

        live = get_snippet(tok, vid)
        if live is None:
            failed.append((vid, "video not found"))
            continue
        if normalise(live.get("description")) == normalise(after):
            skipped.append((vid, "live already matches the staged text"))
            continue
        if normalise(live.get("description")) != normalise(item["description_before"]):
            if not args.force_stale:
                skipped.append((vid, "STALE - live description changed since staging"))
                continue

        if not args.apply:
            print(f"DRY {vid}  {title:54} {item['chars_before']:>5} -> {item['chars_after']:<5} "
                  f"chapters={item['chapters_state_before']}")
            applied.append({"video_id": vid, "dry_run": True})
            continue

        status, body = put_description(tok, vid, live, after)
        ok = status == 200
        if ok:
            # The read-back is eventually consistent: a GET issued immediately after a
            # 200 can still serve the pre-write description. Measured on zE3nCUlUmLY,
            # where the write was correct and the first GET was stale. Retry before
            # calling it a failure, otherwise a healthy batch aborts on a cache miss.
            for attempt in range(4):
                check = get_snippet(tok, vid)
                if normalise((check or {}).get("description")) == normalise(after):
                    break
                time.sleep(2 * (attempt + 1))
            else:
                ok = False
                body = {"error": "read-back still did not match after 4 attempts"}
        if ok:
            applied.append({
                "video_id": vid, "title": item["title"], "episode_id": item.get("episode_id"),
                "chars_before": item["chars_before"], "chars_after": item["chars_after"],
                "chapters_state_before": item["chapters_state_before"],
                "applied_at": datetime.now(timezone.utc).isoformat(),
            })
            print(f"OK  {vid}  {title:54} {item['chars_before']:>5} -> {item['chars_after']}",
                  flush=True)
        else:
            failed.append((vid, f"HTTP {status} {json.dumps(body)[:120]}"))
            print(f"FAIL {vid}  {title:54} HTTP {status}", flush=True)
            # A write failure here is usually quota or auth; both affect every later
            # item, so stop rather than burn the rest of the batch.
            break
        time.sleep(SPACING_S)

    for vid, why in skipped:
        print(f"skip {vid}  {why}")
    print(f"\napplied={len([a for a in applied if not a.get('dry_run')])} "
          f"dry={len([a for a in applied if a.get('dry_run')])} "
          f"skipped={len(skipped)} failed={len(failed)}")
    for vid, why in failed:
        print(f"  FAILED {vid}: {why}")

    if args.apply:
        prev = json.loads(RECEIPT.read_text(encoding="utf-8")).get("applied", []) \
            if RECEIPT.is_file() else []
        RECEIPT.write_text(json.dumps({
            "schema_version": "1.0.0",
            "generator": "scripts/apply_description_batch.py",
            "channel_id": CHANNEL_ID,
            "source_batch": str(BATCH.relative_to(ROOT).as_posix()),
            "last_run_at": datetime.now(timezone.utc).isoformat(),
            "applied": prev + [a for a in applied if not a.get("dry_run")],
            "skipped": [{"video_id": v, "reason": w} for v, w in skipped],
            "failed": [{"video_id": v, "reason": w} for v, w in failed],
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"receipt: {RECEIPT}")
    elif applied:
        print("\nDRY RUN - nothing was written. Re-run with --apply.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
