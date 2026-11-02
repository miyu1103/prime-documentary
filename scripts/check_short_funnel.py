#!/usr/bin/env python
"""Refuse to schedule a Short that cannot send anyone to the long-form.

Measured on 2026-08-02: 46 published Shorts, 4,391 views, and NOT ONE of them carried a link
to a long-form. Shorts convert at 0.77 subscribers per 1,000 views and long-form at 3.67, so
every one of those views was worth 4.8x less than it needed to be. The corridor was described
in docs/PD_SHORTS_TO_LONGFORM_FUNNEL.v001.md and built in code, and it still did not reach the
published videos, because nothing refused to publish without it.

This is that refusal. It reads one machine-readable record per short --

    episodes/<EPID>/09_package/short<NNN>_funnel.v001.json

-- and fails closed on anything missing. It is wired into schedule_short_youtube.py ahead of the
upload, so a short with a broken corridor cannot be scheduled even in --dry-run.

    python scripts/check_short_funnel.py --short 182
    python scripts/check_short_funnel.py --all
    python scripts/check_short_funnel.py --demo-fail     # proves the gate rejects

Exit 0 = every checked short can carry a viewer to its episode. Exit 1 = at least one cannot.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKLIST = ROOT / "episodes" / "_planning" / "SHORTS_RELATED_VIDEO_WORKLIST.v001.md"

YT_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
CTA_SCRIM = 0.46          # 0.72 crushed the picture; Short.tsx uses 0.46
CTA_TITLE_MAX = 40        # longer than this and the band wraps over the loop tail
LONG_TITLE_MAX = 60

# Words that carry no meaning when checking whether a short answers its own standing question.
STOP = {
    "the", "a", "an", "and", "or", "but", "if", "of", "to", "in", "on", "at", "for", "with",
    "that", "this", "it", "is", "was", "are", "were", "be", "been", "do", "did", "does",
    "what", "who", "whom", "whose", "why", "how", "when", "where", "which", "there", "their",
    "them", "they", "you", "your", "his", "her", "its", "one", "so", "as", "by", "from", "not",
    "no", "any", "all", "still", "even", "ever", "after", "before", "than", "then", "about",
}


def _fail(problems: list[str], cond: bool, msg: str) -> None:
    if not cond:
        problems.append(msg)


def _content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z']{3,}", text.lower()) if w not in STOP}


def check_record(rec: dict, spoken: str | None, worklist: str) -> list[str]:
    """Return a list of problems. Empty list means the corridor is complete."""
    p: list[str] = []
    nnn = rec.get("short")

    # --- layer 5: the loop -------------------------------------------------------------
    _fail(p, rec.get("loop") is True, "loop is not true -- every short in this channel loops")
    join = (rec.get("loop_join") or "").strip()
    _fail(p, len(join) >= 20,
          "loop_join is missing or too vague to build from: the last beat must resolve into "
          "frame 0, and 'fade to black' is not a loop")
    detail = (rec.get("second_watch_detail") or "").strip()
    _fail(p, len(detail) >= 10,
          "second_watch_detail is missing -- SHORTS_METHOD rule 5 requires one element that "
          "reads differently on the second pass")

    # --- the standing question: the reason anyone opens the description ----------------
    q = (rec.get("funnel_question_left_for_longform") or "").strip()
    _fail(p, bool(q), "funnel_question_left_for_longform is empty -- nothing pulls the viewer on")
    _fail(p, q.endswith("?"), "funnel_question_left_for_longform is not a question")
    if q and spoken is not None:
        qw, sw = _content_words(q), _content_words(spoken)
        missing = qw - sw
        _fail(p, bool(missing),
              "the standing question is answered inside the short itself (every content word of "
              "it already appears in the spoken lines) -- the corridor is closed, re-cut it")

    # --- layer 1: description line 1 ---------------------------------------------------
    title = (rec.get("funnel_long_title") or "").strip()
    _fail(p, bool(title), "funnel_long_title is empty -- a bare URL does not get clicked")
    _fail(p, len(title) <= LONG_TITLE_MAX,
          f"funnel_long_title is {len(title)} chars, over the {LONG_TITLE_MAX} the first line holds")
    vid = (rec.get("funnel_long_video_id") or "").strip()
    _fail(p, bool(YT_ID.match(vid)),
          "funnel_long_video_id is not an 11-character YouTube id -- the long-form must exist as "
          "at least a private upload BEFORE its short can be scheduled")
    line1 = (rec.get("description_line_1") or "").strip()
    _fail(p, line1.startswith("▶ FULL CASE:"),
          "description_line_1 does not start with '▶ FULL CASE:' -- the description collapses "
          "and line 2 is never read")
    _fail(p, title in line1, "description_line_1 does not carry funnel_long_title")

    # --- layer 2: the in-video card ----------------------------------------------------
    cta = rec.get("cta") or {}
    _fail(p, bool((cta.get("ctaHeadline") or "").strip()), "cta.ctaHeadline is empty")
    ct = (cta.get("ctaLongTitle") or "").strip()
    _fail(p, bool(ct), "cta.ctaLongTitle is empty")
    _fail(p, len(ct) <= CTA_TITLE_MAX,
          f"cta.ctaLongTitle is {len(ct)} chars, over {CTA_TITLE_MAX}; it wraps over the loop tail")
    _fail(p, bool((cta.get("ctaLongThumbSrc") or "").strip()), "cta.ctaLongThumbSrc is empty")
    _fail(p, cta.get("scrim") == CTA_SCRIM,
          f"cta.scrim is {cta.get('scrim')!r}, must be {CTA_SCRIM} (0.72 crushed the picture)")
    _fail(p, cta.get("fake_button") is False,
          "cta.fake_button must be recorded false -- nothing in a Short is tappable, so a "
          "button-shaped card is a lie to the viewer")

    # --- layer 3: the pinned comment ---------------------------------------------------
    pin = (rec.get("pinned_comment") or "").strip()
    _fail(p, bool(pin), "pinned_comment is empty")
    if pin and q:
        _fail(p, q in pin, "pinned_comment does not carry the standing question verbatim")
    if pin and vid:
        _fail(p, vid in pin, "pinned_comment does not carry the long-form video id")

    # --- layer 4: the Studio related-video worklist (not settable by API) ---------------
    _fail(p, f"short{nnn}" in worklist,
          f"no row for short{nnn} in {WORKLIST.name} -- layer 4 is manual and is forgotten "
          "unless it is written down")
    return p


def _load_spoken(rec: dict) -> str | None:
    ep, nnn = rec.get("episode_id"), rec.get("short")
    if not ep or not nnn:
        return None
    f = ROOT / "episodes" / ep / "09_package" / f"short{nnn}_lines.v001.json"
    if not f.is_file():
        return None
    try:
        lines = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return None
    return " ".join(str(l.get("text", "")) for l in lines if isinstance(l, dict))


def _records(which: list[int] | None) -> list[Path]:
    found = sorted((ROOT / "episodes").glob("PD-*/09_package/short*_funnel.v001.json"))
    if which is None:
        return found
    keep = {f"short{n}_funnel.v001.json" for n in which}
    return [p for p in found if p.name in keep]


DEMO_BAD = {
    "short": 999, "episode_id": "PD-9999-999-demo", "loop": False, "loop_join": "fade out",
    "second_watch_detail": "", "funnel_question_left_for_longform": "who knows",
    "funnel_long_title": "", "funnel_long_video_id": "", "description_line_1": "watch the full case",
    "cta": {"ctaHeadline": "", "ctaLongTitle": "", "ctaLongThumbSrc": "", "scrim": 0.72,
            "fake_button": True},
    "pinned_comment": "",
}


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--short", type=int, action="append", help="short number; repeatable")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--demo-fail", action="store_true",
                    help="run the gate against a deliberately broken record and prove it rejects")
    a = ap.parse_args(argv)

    worklist = WORKLIST.read_text(encoding="utf-8") if WORKLIST.is_file() else ""

    if a.demo_fail:
        problems = check_record(DEMO_BAD, spoken=None, worklist=worklist)
        print(f"[funnel] DEMO: deliberately broken record produced {len(problems)} problem(s):")
        for x in problems:
            print(f"    - {x}")
        ok = len(problems) >= 10
        print("[funnel] DEMO RESULT:", "the gate rejects as designed" if ok else
              "THE GATE IS DECORATION -- it passed a record with nothing in it")
        return 0 if ok else 1

    if not a.short and not a.all:
        ap.error("pass --short N (repeatable), --all, or --demo-fail")

    paths = _records(None if a.all else a.short)
    if not paths:
        print("[funnel] no funnel record found for the requested short(s) -- write "
              "episodes/<EPID>/09_package/short<NNN>_funnel.v001.json first", file=sys.stderr)
        return 1

    bad = 0
    for path in paths:
        rec = json.loads(path.read_text(encoding="utf-8"))
        problems = check_record(rec, _load_spoken(rec), worklist)
        tag = f"short{rec.get('short')}"
        if problems:
            bad += 1
            print(f"[funnel] {tag}: FAIL ({len(problems)})")
            for x in problems:
                print(f"    - {x}")
        else:
            print(f"[funnel] {tag}: ok -- loop closed, 5 layers present, "
                  f"corridor points at {rec.get('funnel_long_video_id')}")
    print(f"[funnel] {len(paths) - bad}/{len(paths)} short(s) can carry a viewer to their episode")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
