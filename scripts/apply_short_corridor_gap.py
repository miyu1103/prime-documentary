#!/usr/bin/env python3
"""Put the house "FULL CASE" block on the Shorts that measurably do not have one.

Scope is deliberately tiny. scripts/audit_short_longform_corridor.py measured 58 public Shorts and
found 52 already carry a first-line link to their own parent long-form. This writes only the
remainder whose parent is established from a repo receipt, and refuses the rest.

The block matches the format already on the other 52, verbatim:

    ▶ FULL CASE: <long-form title>
    https://www.youtube.com/watch?v=<id>
    <blank>
    <the description that was already there>

SAFETY, each one enforced in code rather than by intention:
  * part=snippet only. The `status` object is never constructed and never sent, so
    privacyStatus and publishAt have no path into the request body.
  * videos.update REPLACES the snippet, so title, categoryId, tags, defaultLanguage and
    defaultAudioLanguage are read back from the API and re-sent byte-identical. The tool
    asserts title equality after the write.
  * LOCK: refuses any video whose publishedAt or status.publishAt is on/after 2026-08-10.
  * refuses a destination that is not public (a link nobody can open is worse than none).
  * refuses if the description already contains the destination id.
  * every target is re-fetched after the write and diffed against what was staged.

Usage:
  py -3.11 scripts/apply_short_corridor_gap.py                 # stage + print, writes nothing
  py -3.11 scripts/apply_short_corridor_gap.py --apply
  py -3.11 scripts/apply_short_corridor_gap.py --apply --only dedDocuyCUM
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yt_channel_index import authorize, fetch_videos, http  # noqa: E402
import yt_quota as Q  # noqa: E402

API = "https://www.googleapis.com/youtube/v3"
LOCK_FROM = datetime(2026, 8, 10, 0, 0, tzinfo=timezone.utc)
RECEIPTS = ROOT / "runs" / "short_funnel"

# short video id -> (destination long-form id, the repo receipt that establishes the mapping)
TARGETS = {
    "dedDocuyCUM": ("bYcqabvvxak",
                    "episodes/PD-2026-006-terry/09_package/short06_youtube_publish_result.v002.json"
                    " (short) + episodes/PD-2026-006-terry/09_package/"
                    "youtube_publish_result.v003.json (long-form)"),
    "L8iKnBSVXKg": ("XWYWAgkExH4",
                    "episodes/PD-2026-007-riley/09_package/short07_youtube_publish_result.v003.json"
                    " (short) + episodes/PD-2026-007-riley/09_package/final_delivery.v006.json"),
    "m33s6uFmXao": ("zE3nCUlUmLY",
                    "episodes/PD-2026-008-carpenter/09_package/"
                    "short08_youtube_publish_result.v002.json (short) + "
                    "episodes/PD-2026-008-carpenter/09_package/youtube_meta.v002.json"),
    "aFPyMf3ugrA": ("_8DaMu8_yFw",
                    "episodes/PD-2026-050-centralpark/09_package/"
                    "short54_youtube_schedule_result.v001.json (short); long-form established by "
                    "102-content-word overlap between the published description and "
                    "episodes/PD-2026-050-centralpark/03_script/script.en.v001.md, against 24-49 "
                    "for three control episodes"),
}


def iso(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    only = {x for x in args.only.split(",") if x}

    auth = authorize(ROOT)
    want = [v for v in TARGETS if not only or v in only]
    need = want + [TARGETS[v][0] for v in want]
    V = fetch_videos(auth, need, part="snippet,status")
    Q.record("videos.list")

    staged, refused = [], []
    for vid in want:
        dest, receipt = TARGETS[vid]
        s, d = V.get(vid), V.get(dest)
        if not s:
            refused.append((vid, "short not on channel")); continue
        if not d:
            refused.append((vid, f"destination {dest} not on channel")); continue

        # --- lock window -------------------------------------------------------------------
        for who, obj in (("short", s), ("destination", d)):
            pa = obj["status"].get("publishAt") or obj["snippet"]["publishedAt"]
            if iso(pa) >= LOCK_FROM:
                refused.append((vid, f"{who} sits at {pa}, on/after the 2026-08-10 lock"))
                break
        else:
            if d["status"]["privacyStatus"] != "public":
                refused.append((vid, f"destination {dest} is "
                                     f"{d['status']['privacyStatus']}, not public")); continue
            if s["status"]["privacyStatus"] != "public":
                refused.append((vid, f"short is {s['status']['privacyStatus']}")); continue
            old = s["snippet"].get("description", "")
            if dest in old:
                refused.append((vid, "description already contains the destination id")); continue

            block = (f"▶ FULL CASE: {d['snippet']['title']}\n"
                     f"https://www.youtube.com/watch?v={dest}\n\n")
            staged.append({
                "video": vid, "dest": dest, "receipt": receipt,
                "title": s["snippet"]["title"],
                "dest_title": d["snippet"]["title"],
                "old_description": old,
                "new_description": block + old,
                "snippet_out": {
                    "title": s["snippet"]["title"],
                    "description": block + old,
                    "categoryId": s["snippet"].get("categoryId", "27"),
                    **({"tags": s["snippet"]["tags"]} if s["snippet"].get("tags") else {}),
                    **({"defaultLanguage": s["snippet"]["defaultLanguage"]}
                       if s["snippet"].get("defaultLanguage") else {}),
                    **({"defaultAudioLanguage": s["snippet"]["defaultAudioLanguage"]}
                       if s["snippet"].get("defaultAudioLanguage") else {}),
                },
                "before": {"privacyStatus": s["status"]["privacyStatus"],
                           "publishAt": s["status"].get("publishAt"),
                           "title": s["snippet"]["title"],
                           "tags": s["snippet"].get("tags", []),
                           "categoryId": s["snippet"].get("categoryId")},
            })

    print(f"staged {len(staged)} | refused {len(refused)}")
    for vid, why in refused:
        print(f"  REFUSED {vid}: {why}")
    for t in staged:
        print(f"\n  {t['video']}  ->  {t['dest']}")
        print(f"    short : {t['title'][:66]}")
        print(f"    dest  : {t['dest_title'][:66]}")
        print(f"    adds  : {t['new_description'].splitlines()[0]}")
        print(f"    desc  : {len(t['old_description'])} -> {len(t['new_description'])} chars")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    plan = RECEIPTS / f"corridor_gap.{stamp}.plan.json"
    plan.write_text(json.dumps(staged, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nplan -> {plan}")

    if not args.apply:
        print("dry run. nothing written. re-run with --apply")
        return 0

    results = []
    for t in staged:
        st, r = http("PUT", f"{API}/videos?part=snippet",
                     headers=auth, body={"id": t["video"], "snippet": t["snippet_out"]})
        Q.record("videos.update")
        ok = st == 200
        results.append({"video": t["video"], "http": st,
                        "error": None if ok else json.dumps(r)[:300]})
        print(f"  {'WROTE  ' if ok else 'FAILED '} {t['video']}  HTTP {st}"
              + ("" if ok else f"  {json.dumps(r)[:200]}"))
        if not ok:
            print("  stopping at first failure so the rest can be retried cleanly")
            break

    # ---- independent re-read -----------------------------------------------------------
    print("\nre-fetching every target and comparing against the staged copy:")
    written = [t for t in staged if any(x["video"] == t["video"] and x["http"] == 200
                                        for x in results)]
    if written:
        after = fetch_videos(auth, [t["video"] for t in written], part="snippet,status")
        Q.record("videos.list")
        allgood = True
        for t in written:
            a = after[t["video"]]
            checks = {
                "description matches staged": a["snippet"]["description"] == t["new_description"],
                "destination link present": t["dest"] in a["snippet"]["description"],
                "link on line 2": (a["snippet"]["description"].splitlines() + ["", ""])[1]
                == f"https://www.youtube.com/watch?v={t['dest']}",
                "title unchanged": a["snippet"]["title"] == t["before"]["title"],
                "tags unchanged": a["snippet"].get("tags", []) == t["before"]["tags"],
                "categoryId unchanged": a["snippet"].get("categoryId")
                == t["before"]["categoryId"],
                "privacyStatus unchanged": a["status"]["privacyStatus"]
                == t["before"]["privacyStatus"],
                "publishAt unchanged": a["status"].get("publishAt") == t["before"]["publishAt"],
            }
            bad = [k for k, v in checks.items() if not v]
            allgood &= not bad
            print(f"  {t['video']}  {'ALL 8 CHECKS PASS' if not bad else 'MISMATCH: ' + ', '.join(bad)}")
        print("\nverdict:", "every write verified by independent re-read" if allgood
              else "MISMATCHES ABOVE - treat as not landed")

    rec = RECEIPTS / f"corridor_gap.{stamp}.result.json"
    rec.write_text(json.dumps({"results": results}, indent=2), encoding="utf-8")
    print(f"receipt -> {rec}")
    print(f"ledger: {Q.spent_today()} spent, {Q.remaining()} remaining")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
