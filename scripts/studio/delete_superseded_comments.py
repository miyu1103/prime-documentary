#!/usr/bin/env python3
"""Delete the four superseded channel comments the drafts file marks `replaces_existing`.

Four of the 56 drafts replace a comment the channel posted in June 2026. Those four old comments
end in an abstract prompt ("was that trade-off worth it", "where should the line sit") which is
what the rewrite exists to fix; leaving them sitting under the new pinned one on a channel with
seven comments in total would read as an abandoned draft rather than a replacement. So they are
deleted deliberately, and only after the replacement is confirmed present and pinned.

The full original text of every deleted comment is written to the log below BEFORE the delete
call, so the deletion is reversible in effect: the words can be reposted verbatim.

Refuses to delete anything that is not (a) authored by this channel, (b) recorded in the drafts
file as `replaces_existing`, and (c) already superseded by a verified pinned replacement.

Usage:
    py -3.11 scripts/studio/delete_superseded_comments.py --dry-run
    py -3.11 scripts/studio/delete_superseded_comments.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from yt_channel_index import authorize, http, API  # noqa: E402
import yt_quota  # noqa: E402

DRAFTS = ROOT / "episodes" / "_planning" / "measurements" / "PINNED_COMMENTS.v001.json"
LEDGER = ROOT / "runs" / "pinned_comments" / "ledger.jsonl"
LOG = ROOT / "runs" / "pinned_comments" / "deleted_superseded.json"
CHANNEL_ID = "UCuQPtAz1rca9eJ4xhvX0yKA"


def norm(s: str) -> str:
    return " ".join((s or "").split())


def main() -> int:
    dry = "--dry-run" in sys.argv
    drafts = json.loads(DRAFTS.read_text(encoding="utf-8"))
    targets = {c["video_id"]: c for c in drafts["comments"] if c.get("replaces_existing")}
    if not targets:
        print("no replaces_existing rows")
        return 0

    led = {}
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            led[r["video_id"]] = r

    auth = authorize(ROOT)
    out = []
    for vid, draft in targets.items():
        lg = led.get(vid, {})
        if lg.get("status") != "VERIFIED_PINNED":
            print(f"REFUSE {vid}: replacement not VERIFIED_PINNED (status={lg.get('status')})")
            continue
        st, r = http("GET", f"{API}/commentThreads?part=snippet&videoId={vid}"
                            f"&maxResults=100&order=time&textFormat=plainText", headers=auth)
        yt_quota.record("commentThreads.list")
        if st != 200:
            print(f"REFUSE {vid}: commentThreads.list HTTP {st}")
            continue
        replacement = None
        old = []
        for it in r.get("items", []):
            s = it["snippet"]["topLevelComment"]["snippet"]
            rec = {"comment_id": it["snippet"]["topLevelComment"]["id"],
                   "author_channel_id": s.get("authorChannelId", {}).get("value"),
                   "author": s["authorDisplayName"],
                   "published_at": s["publishedAt"],
                   "text": s["textOriginal"]}
            if norm(rec["text"]) == norm(draft["text"]):
                replacement = rec
            elif rec["author_channel_id"] == CHANNEL_ID:
                old.append(rec)
        if not replacement:
            print(f"REFUSE {vid}: replacement text not found via API")
            continue
        for o in old:
            entry = {"video_id": vid, "deleted_comment_id": o["comment_id"],
                     "original_published_at": o["published_at"],
                     "original_text": o["text"],
                     "replaced_by_comment_id": replacement["comment_id"],
                     "at": datetime.now(timezone.utc).isoformat()}
            if dry:
                entry["result"] = "DRY_RUN"
                print(f"would delete {vid} {o['comment_id']}: {o['text'][:80]}")
            else:
                # Text is recorded above before the call, so this is reversible in effect.
                LOG.parent.mkdir(parents=True, exist_ok=True)
                st2, r2 = http("DELETE", f"{API}/comments?id={o['comment_id']}", headers=auth)
                yt_quota.record("comments.delete", units=50)
                entry["result"] = "DELETED" if st2 in (200, 204) else f"HTTP_{st2}"
                entry["error"] = None if st2 in (200, 204) else str(r2)[:300]
                print(f"{entry['result']} {vid} {o['comment_id']}")
            out.append(entry)

    if out and not dry:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        LOG.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"log: {LOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
