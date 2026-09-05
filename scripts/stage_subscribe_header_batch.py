#!/usr/bin/env python3
r"""Stage a subscribe-first header onto every PUBLIC long-form description.

Measured problem this exists to fix (2026-08-10, Studio + Data API, first-hand):

    subscribed viewers   26 of 9,662 views          0.27%  -- every view is a cold first contact
    long-form conversion 3.95 subs / 1,000 views    3.4x better than Shorts (1.16)
    the ask              4 of 5 sampled episodes never ask in narration at all, and the
                         end-card ask sits at the 30-minute mark while 43% are gone by 60s

The description is the one surface that is free to change, is read before the video is
watched, and needs no render. It currently opens with the story and buries any subscribe
line at the very bottom -- in 34 of 55 long-forms there is no subscribe line at all.

What this stages, and why each line is TRUE rather than a promise:

    line 1  "one of N full-length cases ... M of them posted in the last M days"
            N and M are counted from the live API at stage time, not asserted.
    line 2  "More are finished and already scheduled."
            Verified against status.publishAt: long-forms sit private with future
            publishAt values. This is the owner's true version of the rejected
            "we'll make a sequel" -- more of these EXIST, and more ARE COMING.
    line 3  the sub_confirmation link, on its own line so it is clickable at the top.

It also removes the old bottom-of-description subscribe boilerplate, because several
variants claim "one every week" while the measured cadence is near-daily, and a false
cadence next to a true one is worse than no second ask.

Writes episodes/_planning/measurements/SUBSCRIBE_HEADER_BATCH.v001.json for
scripts/apply_subscribe_header_batch.py. Read-only against YouTube (1 unit/50 videos).

    py -3.11 scripts/stage_subscribe_header_batch.py
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from yt_channel_index import authorize, fetch_videos, iso_seconds, list_video_ids  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "episodes" / "_planning" / "measurements" / "SUBSCRIBE_HEADER_BATCH.v001.json"
CHANNEL_ID = "UCuQPtAz1rca9eJ4xhvX0yKA"
SUB_URL = "https://www.youtube.com/@primedocumentarystudio?sub_confirmation=1"
MAX_CHARS = 5000
LONGFORM_MIN_SEC = 185

# Bottom-of-description subscribe boilerplate to strip. Matched on the whole stripped line.
BOILERPLATE = re.compile(
    r"^(?:\N{WHITE RIGHT POINTING BACKHAND INDEX}\s*)?"
    r"(?:If\b.*\bsubscribe\b.*|Subscribe (?:for|to)\b.*)$",
    re.IGNORECASE,
)

# Three descriptions sit within ~120 chars of the 5,000 cap. Their trailing source
# enumerations are the only compressible text; the header must not cost a source.
# 4FlCaOVpln0's live description is already truncated mid-word ("...of 2013.e"), which
# is what hitting the cap looks like.
SOURCE_TRIMS = {
    "Wo-SvvGsv8g": (
        "Sources: Cardoso v. Bank of America (D. Mass.); St. Petersburg Times (Marrero); "
        "Stephan depositions (2009, 2010); Fannie Mae v. Bradbury (Me.); DOJ; Florida AG; "
        "60 Minutes; Congressional Oversight Panel; Fed; GAO; CFPB; Nevada & Missouri AGs; "
        "CoreLogic; AP.",
        "Sources: Cardoso v. Bank of America (D. Mass.); Fannie Mae v. Bradbury (Me.); the "
        "Stephan depositions; DOJ; Fed; GAO; CFPB.",
    ),
    # Same video: without this it lands on exactly 5000, with no margin for however
    # YouTube counts a newline. The meaning of the notice is unchanged.
    "Wo-SvvGsv8g:disclaimer": (
        "Some imagery in this film is AI-assisted and symbolic; no real-person likeness is shown.",
        "Some imagery is AI-assisted and symbolic; no real-person likeness is shown.",
    ),
    "dNhu-IJUc5k": (
        "Sources: the NIST press release and NCST materials of 22 June 2026 and the "
        "investigators' NCST Advisory Committee deck of 9 September 2025; the October 2018 "
        "Morabito Consultants survey via NBC 6, The Real Deal and Commercial Observer; the "
        "November 2018 board minutes via the Miami Herald; the Wodnicki letter as transcribed "
        "by The Washington Post and NPR; CNN on the assessment and reserves; NBC News on the "
        "settlement; NPR on the grand jury report.",
        "Sources: NIST/NCST findings of 22 June 2026 and the NCST Advisory Committee deck of "
        "9 September 2025; the October 2018 Morabito Consultants survey; the November 2018 "
        "board minutes; the Wodnicki letter; the December 2021 Miami-Dade grand jury report.",
    ),
    "4FlCaOVpln0": (
        "Sources include: the Post Office Horizon IT Inquiry's Final Report Volume 1 by Sir Wyn "
        "Williams; Bates and Others v Post Office Ltd (No 6) [2019] EWHC 3408 (QB); Hamilton and "
        "Others v Post Office Ltd [2021] EWCA Crim 577; the Post Office (Horizon System) Offences "
        "Act 2024; Hansard; Ministry of Justice quashed-conviction management information and "
        "gov.uk redress data; the Second Sight interim report of 2013.e",
        "Sources: the Post Office Horizon IT Inquiry Final Report Vol. 1 (Sir Wyn Williams); "
        "Bates v Post Office Ltd (No 6) [2019] EWHC 3408 (QB); Hamilton v Post Office Ltd "
        "[2021] EWCA Crim 577; the Post Office (Horizon System) Offences Act 2024; MoJ and "
        "gov.uk redress data; Second Sight (2013).",
    ),
}


def clean_body(desc: str) -> tuple[str, list[str]]:
    """Strip subscribe boilerplate and empty section headers. Returns (body, notes)."""
    notes: list[str] = []
    lines = desc.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    kept: list[str] = []
    for ln in lines:
        s = ln.strip()
        if s and BOILERPLATE.match(s):
            notes.append(f"removed boilerplate: {s[:60]}")
            continue
        kept.append(ln)

    # A section header with nothing under it (measured on ch2hQ5jhDmQ: "Chapters" with no
    # chapters) reads as a broken description. Drop the header, keep everything else.
    out: list[str] = []
    for i, ln in enumerate(kept):
        s = ln.strip()
        if s.endswith("Chapters") and len(s) < 20:
            nxt = next((x.strip() for x in kept[i + 1:] if x.strip()), "")
            if not re.match(r"^\d{1,2}:\d{2}", nxt):
                notes.append("removed empty Chapters header")
                continue
        out.append(ln)

    body = "\n".join(out)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return body, notes


def main() -> int:
    auth = authorize(ROOT)
    ids = list_video_ids(auth)
    vids = fetch_videos(auth, ids)

    longs = [v for v in vids.values()
             if iso_seconds(v["contentDetails"]["duration"]) >= LONGFORM_MIN_SEC
             and v["status"]["privacyStatus"] == "public"]
    longs.sort(key=lambda v: v["snippet"]["publishedAt"])

    n = len(longs)
    cutoff = datetime.now(timezone.utc) - timedelta(days=28)
    recent = sum(1 for v in longs
                 if datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
                 >= cutoff)

    # "More are finished and already scheduled" must be checkable, not assumed.
    queued = [v for v in vids.values()
              if iso_seconds(v["contentDetails"]["duration"]) >= LONGFORM_MIN_SEC
              and v["status"]["privacyStatus"] != "public"
              and v["status"].get("publishAt")]
    if not queued:
        print("REFUSING: no scheduled long-forms, so 'more are finished and already "
              "scheduled' would not be true.")
        return 1

    # Three tiers of the same true statement. A handful of descriptions already sit within
    # ~100 chars of YouTube's 5,000 cap, so the widest header that still fits is used rather
    # than truncating the film's own text. Every tier keeps the two things that matter: more
    # of these already exist, and the link that acts on it.
    headers = [
        ("full",
         f"More like this already exist: this is one of {n} full-length cases on this channel, "
         f"{recent} of them posted in the last 28 days.\n"
         f"More are finished and already scheduled. Subscribing is what puts the next one in "
         f"front of you:\n{SUB_URL}"),
        ("compact",
         f"One of {n} full-length cases here - more are finished and already scheduled. "
         f"Subscribing is what puts the next one in front of you:\n{SUB_URL}"),
        ("mini",
         f"One of {n} cases here. More are finished and already scheduled - subscribe: {SUB_URL}"),
    ]
    for name, h in headers:
        print(f"[{name}] {len(h)} chars\n{h}\n")
    print(f"{n} long-forms, {recent} in the last 28d, {len(queued)} scheduled long-forms\n")

    items, over = [], []
    for v in longs:
        vid = v["id"]
        before = (v["snippet"].get("description") or "").replace("\r\n", "\n")
        body, notes = clean_body(before)
        for key in (vid, f"{vid}:disclaimer"):
            if key not in SOURCE_TRIMS:
                continue
            old, new = SOURCE_TRIMS[key]
            if old in body:
                body = body.replace(old, new)
                notes.append(f"compressed {key.split(':')[-1] if ':' in key else 'sources'} "
                             f"({len(old)} -> {len(new)} chars) for cap room")
            else:
                notes.append(f"TRIM {key} DID NOT MATCH - live text changed")
        for tier, header in headers:
            after = f"{header}\n\n{body}"
            if len(after) <= MAX_CHARS:
                break
        if len(after) > MAX_CHARS:
            over.append((vid, len(after)))
        if tier != "full":
            notes.append(f"used {tier} header ({len(before)}-char description near the 5000 cap)")
        items.append({
            "video_id": vid,
            "title": v["snippet"]["title"],
            "published_at": v["snippet"]["publishedAt"],
            "header_tier": tier,
            "chars_before": len(before),
            "chars_after": len(after),
            "notes": notes,
            "description_before": before,
            "description_after": after,
        })

    if over:
        for vid, ln in over:
            print(f"OVER CAP {vid}: {ln} chars")
        print("refusing to stage a batch that cannot be applied")
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "schema_version": "1.0.0",
        "generator": "scripts/stage_subscribe_header_batch.py",
        "channel_id": CHANNEL_ID,
        "staged_at": datetime.now(timezone.utc).isoformat(),
        "headers": {name: h for name, h in headers},
        "longform_count": n,
        "longforms_last_28d": recent,
        "scheduled_longforms": len(queued),
        "items": items,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"staged {len(items)} items -> {OUT}")
    print(f"chars: min {min(i['chars_after'] for i in items)} "
          f"max {max(i['chars_after'] for i in items)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
