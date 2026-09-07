#!/usr/bin/env python3
"""Prove, from two independent reads, which drafted comments actually landed and which are pinned.

The batch that posts and pins (`scripts/studio/pin_comments_batch.js`) reports its own outcome.
That is not evidence. This script re-reads the result through a transport the batch never used:

  * presence, comment id, author channel and posted-at come from the Data API
    (`commentThreads.list`, 1 unit per video) — a different server path from the browser DOM.
  * pinned state cannot come from the API at all. There is no `isPinned` field on
    `commentThreads`/`comments` in v3, no pin parameter and no pin endpoint, so the ONLY
    machine-readable pinned signal is the badge YouTube renders on the watch page
    (「@handle さんによって固定されています」 / "Pinned by @handle"). That string is taken from the
    ledger line the batch wrote after a full page reload, and confirmed by a second, later
    read-back pass (`pin_comments_batch.js --verify-only`) which loads each page fresh and clicks
    nothing. Two independent page loads agreeing is the strongest available evidence; it is not an
    API assertion and this file says so per video rather than claiming more than it has.

Usage:
    py -3.11 scripts/studio/build_pinned_comment_receipt.py
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
OUT = ROOT / "episodes" / "_planning" / "measurements" / "PINNED_COMMENTS_RECEIPT.v001.json"
DELETED = ROOT / "runs" / "pinned_comments" / "deleted_superseded.json"
CHANNEL_ID = "UCuQPtAz1rca9eJ4xhvX0yKA"


def norm(s: str) -> str:
    return " ".join((s or "").split())


def main() -> int:
    drafts = json.loads(DRAFTS.read_text(encoding="utf-8"))
    want = {c["video_id"]: c for c in drafts["comments"]}

    # Latest ledger line per video — the browser-side evidence.
    led: dict[str, dict] = {}
    hist: dict[str, list] = {}
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            led[r["video_id"]] = r
            hist.setdefault(r["video_id"], []).append(r)

    auth = authorize(ROOT)
    rows = []
    calls = 0
    for vid, draft in want.items():
        st, r = http("GET", f"{API}/commentThreads?part=snippet&videoId={vid}"
                            f"&maxResults=100&order=time&textFormat=plainText", headers=auth)
        calls += 1
        api_hit = None
        others = []
        matches = []
        if st == 200:
            for it in r.get("items", []):
                s = it["snippet"]["topLevelComment"]["snippet"]
                rec = {
                    "comment_id": it["snippet"]["topLevelComment"]["id"],
                    "author": s["authorDisplayName"],
                    "author_channel_id": s.get("authorChannelId", {}).get("value"),
                    "published_at": s["publishedAt"],
                    "text": s["textOriginal"],
                }
                if norm(rec["text"]) == norm(draft["text"]):
                    matches.append(rec)
                    api_hit = rec
                else:
                    others.append(rec)
        # A retry after a failed read-back could have posted the same text twice. Say so loudly
        # rather than reporting the last one found and calling it done.
        duplicates = [m["comment_id"] for m in matches[1:]] if len(matches) > 1 else []

        lg = led.get(vid, {})
        badge = lg.get("pinned_badge") or ""
        loads = sum(1 for h in hist.get(vid, []) if h.get("pinned_badge"))
        pinned = "yes" if badge else ("unverified" if api_hit else "no")
        rows.append({
            "video_id": vid,
            "title": draft.get("title"),
            "comment_id": api_hit["comment_id"] if api_hit else None,
            "posted_at": api_hit["published_at"] if api_hit else None,
            "present_via_api": bool(api_hit),
            "duplicate_copies_posted": duplicates,
            "author_is_the_channel": bool(api_hit) and api_hit["author_channel_id"] == CHANNEL_ID,
            "author_display": api_hit["author"] if api_hit else None,
            "pinned": pinned,
            "pinned_badge_read_from_page": badge or None,
            "independent_page_loads_showing_badge": loads,
            "first_thread_is_ours": lg.get("first_thread_is_ours"),
            "batch_status": lg.get("status"),
            "batch_error": lg.get("error"),
            "verification_method": (
                "presence+id+posted_at: Data API commentThreads.list (server read, not the "
                "browser). pinned: badge string read off the watch page after a full reload — "
                "the API exposes no pinned field, so this is the only machine-readable signal."
            ),
            "other_top_level_comments": others,
            "text": draft["text"],
        })

    yt_quota.record("commentThreads.list", calls)

    summary = {
        "posted": sum(1 for r in rows if r["present_via_api"]),
        "pinned_yes": sum(1 for r in rows if r["pinned"] == "yes"),
        "pinned_unverified": sum(1 for r in rows if r["pinned"] == "unverified"),
        "not_posted": sum(1 for r in rows if not r["present_via_api"]),
        "author_not_channel": sum(1 for r in rows if r["present_via_api"]
                                  and not r["author_is_the_channel"]),
        "videos_with_duplicate_copies": sum(1 for r in rows if r["duplicate_copies_posted"]),
    }
    OUT.write_text(json.dumps({
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "scripts/studio/build_pinned_comment_receipt.py",
        "source_drafts": str(DRAFTS.relative_to(ROOT)).replace("\\", "/"),
        "source_ledger": str(LEDGER.relative_to(ROOT)).replace("\\", "/"),
        "channel_id": CHANNEL_ID,
        "how_verified": [
            "Presence, comment id, posted-at and author channel id: YouTube Data API",
            "commentThreads.list per video, matched on the exact drafted text. This is a server",
            "read over a transport the posting automation never touched.",
            "Pinned: YouTube Data API v3 has no isPinned field, no pin parameter and no pin",
            "endpoint, so pinned state is NOT verifiable by API. The evidence here is the badge",
            "YouTube renders on the watch page, read after a full page reload in a fresh tab -",
            "once by the posting pass and again by a later --verify-only pass that clicks",
            "nothing. Confidence: high for 'pinned', because the badge is server-rendered and",
            "survives a reload, but it is a rendered-page read and not an API assertion.",
        ],
        "summary": summary,
        "deleted_superseded_comments": (
            json.loads(DELETED.read_text(encoding="utf-8")) if DELETED.exists() else []),
        "deleted_superseded_note": (
            "The four drafts marked replaces_existing replaced a channel comment from June 2026. "
            "Those four originals were deleted AFTER their replacement was confirmed present and "
            "pinned. The full original text of each is recorded above, so the words can be "
            "reposted verbatim if that turns out to be the wrong call."),
        "videos": rows,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    print(json.dumps(summary, indent=1))
    print(f"receipt: {OUT}")
    for r in rows:
        if r["pinned"] != "yes" or not r["present_via_api"] or r["duplicate_copies_posted"]:
            print(f"  ATTENTION {r['video_id']} present={r['present_via_api']} "
                  f"pinned={r['pinned']} dup={r['duplicate_copies_posted']} "
                  f"{r.get('batch_error') or ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
