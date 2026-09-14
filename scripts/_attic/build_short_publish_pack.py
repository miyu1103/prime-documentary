#!/usr/bin/env python3
"""Compose a Short's title / description / pinned comment so every one of them LINKS to its
long-form — and refuse to emit a pack whose destination is not public.

Why this exists (measured 2026-08-01/02):
  * 43 long-forms are public; a Short is watched by a median of 56 people and the long-form it
    points at by 24. The funnel is not flowing.
  * Long-form converts ~3.67 subscribers per 1,000 views against 0.77 on Shorts, so moving a
    viewer across is worth roughly 5x.
  * Yet `schedule_short_youtube.py`'s descriptions say "Watch the full story on the channel."
    and contain NO url. The repo's own research says the same: 0/40 descriptions interlink.

What can and cannot be automated (checked against the Data API surface):
  * description + title + tags .... API-settable. This script writes them.
  * pinned comment ................ the API can INSERT a comment as the channel, but PINNING is
                                    not exposed. The text is emitted here; pinning is 1 click.
  * Shorts "Related video" link ... not in the API at all. Studio-only, ~30 s per video, and it
                                    is the ONLY 1-tap native path out of a Short, so it is listed
                                    as a required manual step rather than quietly skipped.

Usage:
  py -3.11 scripts/build_short_publish_pack.py --short 82 --ep PD-2026-001-miranda \
      --longform cQFql7tT1fE --hook "He won at the Supreme Court and went to prison anyway"
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "scripts" / "_yt_audit.json"
WATCH = "https://www.youtube.com/watch?v={vid}"


def dur_seconds(txt: str) -> int:
    m = re.match(r"^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$", (txt or "").strip())
    if not m or not any(m.groups()):
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def load_longform(vid: str) -> dict:
    if not AUDIT.exists():
        sys.exit("no scripts/_yt_audit.json — run scripts/yt_full_audit.py first")
    rows = json.loads(AUDIT.read_text(encoding="utf-8"))
    hit = next((r for r in rows if r.get("id") == vid), None)
    if not hit:
        sys.exit(f"{vid} is not on the channel (audit has {len(rows)} videos)")
    if hit.get("privacy") != "public":
        sys.exit(f"REFUSING: {vid} is '{hit.get('privacy')}', not public. A Short must never point "
                 f"at a destination the viewer cannot open — that is a dead funnel.")
    if dur_seconds(hit.get("duration")) <= 185:
        sys.exit(f"REFUSING: {vid} is {hit.get('duration')} — that is a Short, not a long-form.")
    return hit


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--short", required=True)
    ap.add_argument("--ep", required=True)
    ap.add_argument("--longform", required=True, help="video id of the PUBLIC long-form this Short feeds")
    ap.add_argument("--hook", required=True, help="the Short's one-line hook (becomes the title)")
    ap.add_argument("--question", default="", help="question for the pinned comment; drives replies")
    ap.add_argument("--tags", default="")
    args = ap.parse_args()

    lf = load_longform(args.longform)
    url = WATCH.format(vid=args.longform)
    title = f"{args.hook.rstrip('.')} #Shorts"
    if len(title) > 100:
        sys.exit(f"title is {len(title)} chars; YouTube caps at 100. Shorten the hook.")

    # The link goes on LINE ONE. On Shorts the description is behind a tap, so anything below the
    # first couple of lines is effectively invisible.
    description = (
        f"▶ FULL CASE: {lf['title']}\n{url}\n\n"
        f"{args.hook.rstrip('.')}.\n\n"
        f"Prime Documentary covers the cases that quietly decide what the state may do to you. "
        f"The full episode is linked above.\n\n"
        + (args.tags or "#Shorts #SupremeCourt #Law #CriminalJustice #Documentary")
    )
    question = args.question or "Would this have gone the same way in your state?"
    pinned = f"{question}\n\nFull case here → {url}"

    pack = {
        "short_id": f"short{args.short}",
        "episode_id": args.ep,
        "longform": {"video_id": args.longform, "title": lf["title"], "privacy": lf["privacy"], "url": url},
        "title": title,
        "description": description,
        "pinned_comment": pinned,
        "manual_steps_required": [
            "Studio > this Short > Edit > Related video -> set to the long-form above "
            "(NOT in the Data API; the only 1-tap path out of a Short)",
            "Pin the comment below (the API can post it, but cannot pin it)",
        ],
    }
    out = ROOT / "episodes" / args.ep / "09_package" / f"short{args.short}_publish_pack.v001.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"destination OK: {lf['title']}  [{lf['privacy']}, {lf.get('duration')}]")
    print(f"\nTITLE ({len(title)} chars)\n  {title}")
    print(f"\nDESCRIPTION\n" + "\n".join("  " + l for l in description.splitlines()))
    print(f"\nPINNED COMMENT\n" + "\n".join("  " + l for l in pinned.splitlines()))
    print(f"\nMANUAL, every time:")
    for s in pack["manual_steps_required"]:
        print(f"  - {s}")
    print(f"\nwrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
