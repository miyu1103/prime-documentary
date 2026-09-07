#!/usr/bin/env python3
"""Build the posting queue for the v2 TikTok account.

Why this exists: every one of v1's 152 captions ended with the identical two lines --
"Full case on YouTube: @primedocumentarystudio" and the same four hashtags -- and every one of
those videos got zero views. An identical footer repeated 152 times is a spam signal on its own,
independent of what the videos contain. See docs/PD_TIKTOK_ACCOUNT_V2.v001.md.

So this rewrites the queue:

  * the opening order is the ten Shorts that actually earned views on YouTube, best first
  * hashtags are chosen from what the caption is about, three or four of them, never one fixed set
  * the YouTube call-to-action appears on roughly one post in three, in five different wordings

The video files and the first line of every caption are untouched - those were never the problem.

Usage:
    py -3.11 scripts/tiktok/build_queue_v2.py            # writes tt_queue_v2.json, prints a sample
    py -3.11 scripts/tiktok/build_queue_v2.py --check    # report only, write nothing
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# The v1 queue, kept as the immutable source. tt_queue.json is what the poster reads and this
# builder overwrites it, so reading from there would feed the builder its own output - which is
# exactly how the "cover" field went missing once already.
SRC = Path("C:/temp/studio_auto/tt_queue.v1_captions.json")
DST = Path("C:/temp/studio_auto/tt_queue_v2.json")

# Proven on YouTube, best first. Measured 2026-08-16; the caption/title join is approximate,
# so treat this as an ordering, not as an exact performance table.
OPENERS = ["27", "99", "39", "66", "95", "55", "86", "93", "54", "28"]

# keyword found in the caption -> tags for that subject. First match wins, so put the specific
# subjects above the general ones.
TOPIC_TAGS: list[tuple[tuple[str, ...], list[str]]] = [
    (("warrant", "search", "door", "knock"), ["#knowyourrights", "#police", "#supremecourt"]),
    (("traffic stop", "pulled over", "car", "driving"), ["#police", "#knowyourrights", "#dashcam"]),
    (("confess", "interrogat", "questioning"), ["#truecrime", "#justice", "#interrogation"]),
    (("innocent", "exonerat", "wrongful", "receipt", "proof"), ["#wrongfulconviction", "#justice", "#truecrime"]),
    (("execution", "death penalty", "condemned", "fire"), ["#deathpenalty", "#truecrime", "#justice"]),
    (("forfeit", "seiz", "take his", "took the money", "property"), ["#civilforfeiture", "#knowyourrights", "#law"]),
    (("crypto", "exchange", "billion", "vanished", "bitcoin"), ["#crypto", "#fraud", "#truestory"]),
    (("fraud", "investors", "ponzi", "business was one big lie", "sold"), ["#fraud", "#truestory", "#wallstreet"]),
    (("submarine", "dive", "hull", "vessel"), ["#oceangate", "#documentary", "#deepsea"]),
    (("plane", "parachute", "hijack", "tail"), ["#unsolved", "#mystery", "#aviation"]),
    (("phone", "location", "data", "cell"), ["#privacy", "#surveillance", "#knowyourrights"]),
    (("torture", "beat", "jail", "prisoner"), ["#truecrime", "#police", "#justice"]),
    (("school", "student", "campus"), ["#firstamendment", "#school", "#knowyourrights"]),
]

# Used only when nothing in TOPIC_TAGS matches. Deliberately subject-neutral: a rotation that
# can stamp "#supremecourt" onto a story about a crypto exchange is worse than a generic tag.
FALLBACK_TAGS = [
    ["#truecrime", "#truestory", "#documentary"],
    ["#truestory", "#history", "#documentary"],
    ["#documentary", "#truecrime", "#storytime"],
    ["#truecrime", "#documentary", "#history"],
]

# One post in three carries a call-to-action, and never the same sentence twice in a row.
CTA = [
    "The whole case is on my YouTube: @primedocumentarystudio",
    "Full episode on YouTube - @primedocumentarystudio",
    "I covered the entire case on YouTube (@primedocumentarystudio)",
    "There is a full documentary on this: YouTube @primedocumentarystudio",
    "More of these on YouTube: @primedocumentarystudio",
]


def hook(caption: str) -> str:
    """The first line - the part that was never the problem, minus a stray full stop.

    Several titles were pasted in with a period already on the end, giving "?." and "!.".
    """
    line = caption.split("\n")[0].strip()
    if line.endswith(("?.", "!.", "..")):
        line = line[:-1]
    return line


def tags_for(caption: str, index: int) -> list[str]:
    low = caption.lower()
    for keys, tags in TOPIC_TAGS:
        if any(k in low for k in keys):
            return tags
    return FALLBACK_TAGS[index % len(FALLBACK_TAGS)]


def build() -> list[dict]:
    src = json.loads(SRC.read_text(encoding="utf-8"))
    by_id = {str(x["short"]).zfill(2): x for x in src}

    # Owner decision 2026-08-16: post the whole library in number order, short01 first,
    # rather than leading with the ten that did best on YouTube. OPENERS is kept for reference.
    order = sorted(src, key=lambda x: int(str(x["short"])))
    assert len(order) == len(by_id), "duplicate short numbers in the source queue"

    out = []
    for i, item in enumerate(order):
        parts = [hook(item["caption"])]
        if i % 3 == 0:
            parts.append(CTA[(i // 3) % len(CTA)])
        parts.append(" ".join(tags_for(item["caption"], i)))
        # Carry every field through. An earlier version of this builder emitted only
        # short/file/caption and silently dropped "cover" - and a post that goes up without a
        # cover cannot be given one afterwards, it has to be deleted and re-uploaded.
        row = dict(item)
        row["short"] = str(item["short"]).zfill(2)
        row["caption"] = "\n".join(parts)
        out.append(row)
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report only, write nothing")
    a = ap.parse_args()

    rows = build()
    missing = [r["short"] for r in rows if not Path(r["file"]).exists()]
    no_cover = [r["short"] for r in rows if not r.get("cover") or not Path(r["cover"]).exists()]
    if no_cover:
        print(f"  WITHOUT A USABLE COVER: {len(no_cover)} -> {no_cover[:10]}")
    else:
        print("  every row has a cover file on disk")
    footers = {r["caption"].split("\n")[-1] for r in rows}
    with_cta = sum(1 for r in rows if "youtube" in r["caption"].lower())

    print(f"queue={len(rows)}  missing files={len(missing)}  "
          f"distinct hashtag lines={len(footers)}  posts carrying a CTA={with_cta}")
    if missing:
        print("  MISSING:", missing[:10])
    print("\nfirst five, as they will be posted:\n")
    for r in rows[:5]:
        print(f"--- short{r['short']}")
        print(r["caption"])
        print()

    if a.check:
        print("(--check: nothing written)")
        return 0
    DST.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {DST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
