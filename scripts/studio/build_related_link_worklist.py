#!/usr/bin/env python3
"""Regenerate the Short -> long-form related-link worklist from the live channel.

The v001 worklist (`runs/_cache/related_link_worklist.json`) had no generator in the repository:
it was produced once, by hand, on 2026-08-07, and it went stale the moment the next long-form
went public. Twenty-three of its rows say "(no destination)" while the destination was in fact
already recorded elsewhere. This script replaces that hand step so the list can be rebuilt any
day, and so `related_link_batch.js` -- whose allowlist IS this file -- can never be pointed at a
hand-typed list.

A destination is only emitted when it can be justified, and the justification is written into the
row as `destination_source`:

    legacy+description  the map in runs/_cache/legacy_short_destinations.json and the youtu.be
                        link in the Short's own live description name the same video. Two
                        independent sources agreeing.
    description         only the Short's own live description names a long-form.
    legacy              only the legacy map names one.

A Short with no justified destination is emitted under `unresolved` with the reason, never with a
guess. A destination that is not public is emitted under `not_yet_public`: Studio cannot select a
private video in the related-video picker, so those rows have to wait for the long-form to go up.

Read-only against YouTube: videos.list and search.list only. Roughly 300 quota units, all of it
in the shared channel index.

    py -3.11 scripts/studio/build_related_link_worklist.py            # writes v002 json + md
    py -3.11 scripts/studio/build_related_link_worklist.py --dry-run  # prints, writes nothing
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from yt_channel_index import authorize, fetch_videos, iso_seconds, list_video_ids  # noqa: E402

OUT_JSON = ROOT / "runs" / "_cache" / "related_link_worklist.v002.json"
OUT_MD = ROOT / "episodes" / "_planning" / "SHORTS_RELATED_LINK_WORKLIST.v002.md"
LEDGER = ROOT / "runs" / "related_link" / "ledger.jsonl"
LEGACY = ROOT / "runs" / "_cache" / "legacy_short_destinations.json"
V001 = ROOT / "runs" / "_cache" / "related_link_worklist.json"

SHORT_MAX_SEC = 185           # YouTube's Shorts ceiling is 3 minutes; a little slack for rounding
LINK_RE = re.compile(r"(?:youtu\.be/|watch\?v=)([A-Za-z0-9_-]{11})")


def already_linked() -> dict[str, str]:
    """short id -> long-form id, for rows this channel has already been proved to carry."""
    out: dict[str, str] = {}
    if not LEDGER.exists():
        return out
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("status") in ("VERIFIED", "ALREADY_SET"):
            out[r["short_video_id"]] = r["longform_video_id"]
        else:
            out.pop(r.get("short_video_id", ""), None)
    return out


def short_numbers() -> dict[str, int]:
    """short id -> the local short number, where a previous list recorded one."""
    out: dict[str, int] = {}
    if V001.exists():
        for r in json.loads(V001.read_text(encoding="utf-8")):
            if r.get("short_video_id"):
                out[r["short_video_id"]] = r["short"]
    if LEGACY.exists():
        for n, r in json.loads(LEGACY.read_text(encoding="utf-8")).items():
            if r.get("short_video_id"):
                out.setdefault(r["short_video_id"], int(n))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="print the summary, write nothing")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    auth = authorize(ROOT)
    vids = fetch_videos(auth, list_video_ids(auth))
    shorts = {i: v for i, v in vids.items()
              if iso_seconds(v["contentDetails"]["duration"]) <= SHORT_MAX_SEC}
    longs = {i: v for i, v in vids.items() if i not in shorts}
    print(f"{len(vids)} videos | {len(shorts)} shorts | {len(longs)} long-forms")

    legacy = json.loads(LEGACY.read_text(encoding="utf-8")) if LEGACY.exists() else {}
    legacy_by_short = {r["short_video_id"]: r.get("longform")
                       for r in legacy.values() if r.get("short_video_id")}
    numbers = short_numbers()
    linked = already_linked()

    eligible, not_yet_public, unresolved = [], [], []
    for sid, sv in sorted(shorts.items(), key=lambda kv: numbers.get(kv[0], 9999)):
        desc_ids = [d for d in LINK_RE.findall(sv["snippet"].get("description", ""))
                    if d in longs]
        leg = legacy_by_short.get(sid)
        if leg and leg in desc_ids:
            dest, src = leg, "legacy+description"
        elif desc_ids:
            dest, src = desc_ids[0], "description"
        elif leg:
            dest, src = leg, "legacy"
        else:
            unresolved.append({"short": numbers.get(sid), "short_video_id": sid,
                               "reason": "no destination in the legacy map or the description",
                               "short_title": sv["snippet"]["title"]})
            continue

        row = {
            "short": numbers.get(sid),
            "short_video_id": sid,
            "short_title": sv["snippet"]["title"],
            "short_privacy": sv["status"]["privacyStatus"],
            "longform_video_id": dest,
            "longform_title": longs[dest]["snippet"]["title"],
            "longform_privacy": longs[dest]["status"]["privacyStatus"],
            "destination_source": src,
            "already_linked": linked.get(sid) == dest,
        }
        (eligible if row["longform_privacy"] == "public" else not_yet_public).append(row)

    todo = [r for r in eligible if not r["already_linked"]]
    print(f"eligible {len(eligible)} (already linked {len(eligible) - len(todo)}, to do {len(todo)}) | "
          f"waiting on a private long-form {len(not_yet_public)} | unresolved {len(unresolved)}")
    by_src: dict[str, int] = {}
    for r in eligible:
        by_src[r["destination_source"]] = by_src.get(r["destination_source"], 0) + 1
    print("destination provenance:", "  ".join(f"{k}={v}" for k, v in sorted(by_src.items())))
    for r in todo:
        print(f"  TODO short{str(r['short']):<5} {r['short_video_id']} -> {r['longform_video_id']} "
              f"[{r['destination_source']}] {r['longform_title'][:48]}")
    for r in unresolved:
        print(f"  UNRESOLVED short{str(r['short']):<5} {r['short_video_id']}  {r['short_title'][:52]}")

    if args.dry_run:
        print("\n--dry-run: nothing written")
        return 0

    payload = {
        "schema_version": "related_link_worklist.v002",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "eligible": eligible,
        "not_yet_public": not_yet_public,
        "unresolved": unresolved,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT_JSON.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(OUT_JSON)

    lines = [
        "# Short -> long-form related link, worklist v002",
        "",
        f"Generated {payload['generated_at']} by `scripts/studio/build_related_link_worklist.py`",
        "from the live channel. Do not edit by hand: `related_link_batch.js` uses the JSON beside",
        "this file as its allowlist, so a hand edit here changes nothing and misleads the reader.",
        "",
        f"| # | short | short id | -> long-form | source | linked already | long-form title |",
        "|---:|---|---|---|---|---|---|",
    ]
    for r in eligible:
        lines.append(f"| {r['short']} | short{r['short']} | `{r['short_video_id']}` | "
                     f"`{r['longform_video_id']}` | {r['destination_source']} | "
                     f"{'yes' if r['already_linked'] else '**no**'} | {r['longform_title'][:56]} |")
    if not_yet_public:
        lines += ["", "## Waiting on a long-form that is not public yet", "",
                  "Studio cannot select a private video in the picker.", "",
                  "| short id | long-form | privacy |", "|---|---|---|"]
        lines += [f"| `{r['short_video_id']}` | `{r['longform_video_id']}` | {r['longform_privacy']} |"
                  for r in not_yet_public]
    if unresolved:
        lines += ["", "## No justified destination", "",
                  "Neither the legacy map nor the Short's own description names a long-form.",
                  "Nothing is guessed for these.", "",
                  "| short id | title |", "|---|---|"]
        lines += [f"| `{r['short_video_id']}` | {r['short_title'][:70]} |" for r in unresolved]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\nwritten: {OUT_JSON.relative_to(ROOT)}")
    print(f"written: {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
