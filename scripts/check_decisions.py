#!/usr/bin/env python3
"""Every decision must carry the date it gets re-read and the number that revokes it.

WHY THIS EXISTS
---------------
The problem is not that decisions get made. It is that dead ones keep binding. On 2026-08-23,
while auditing exactly this, `decisions/0011-AE-FROM-EP77.md` was added -- a twelfth binding
document, with no date on which anyone would ask whether it was still right. Of the twelve,
zero declared one. Nothing in the repository could tell a fresh session which decisions were
still alive, so all twelve read as permanently binding and the reading cost grows forever.

A decision with a review date expires by itself. Nobody has to have the argument again.

WHAT IS REQUIRED, AND FROM WHEN
-------------------------------
Two lines in the header block of `decisions/*.md`:

    **Review by:** 2026-11-01
    **Revoke if:** long-form CTR has not exceeded 2.0% (scripts/_yt_studio_video_ctr.*.json)

`Revoke if` must name a measurable thing. "if it stops working" is not a revoke condition.
This tool cannot judge that -- it only checks the line exists -- so the honesty is yours.

**The requirement applies to decisions accepted on or after 2026-08-23.** The eleven earlier
ADRs are reported as LEGACY and do not fail the check. This is scoping a new rule forward, the
same move ADR-0011 itself makes ("EP77 and later"); it is not a threshold being weakened to
make something pass. Backfilling them is a real piece of work and is listed by `--legacy`.

Usage:
    py -3.11 scripts/check_decisions.py             # the whole register
    py -3.11 scripts/check_decisions.py --legacy    # only the undated pre-cutoff ones

Exit codes: 0 clear, 1 a decision on/after the cutoff is missing its fields,
            2 a decision is past its own review date and still binding.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "decisions"
JST = dt.timezone(dt.timedelta(hours=9))

# Decisions accepted on or after this date must carry Review by / Revoke if.
CUTOFF = dt.date(2026, 8, 23)

RE_REVIEW = re.compile(r"\*\*Review by:\*\*\s*(\d{4}-\d{2}-\d{2})")
RE_REVOKE = re.compile(r"\*\*Revoke if:\*\*\s*(\S.*)")
RE_STATUS = re.compile(r"\*\*Status:\*\*\s*(.+)")
RE_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def accepted_on(text: str) -> dt.date | None:
    """The date in the Status line -- the only date in these files that means 'decided'."""
    m = RE_STATUS.search(text)
    if not m:
        return None
    d = RE_DATE.search(m.group(1))
    return dt.date.fromisoformat(d.group(1)) if d else None


def scan() -> list[dict]:
    today = dt.datetime.now(JST).date()
    out = []
    for p in sorted(DECISIONS.glob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        acc = accepted_on(text)
        rev = RE_REVIEW.search(text)
        rvk = RE_REVOKE.search(text)
        review = dt.date.fromisoformat(rev.group(1)) if rev else None
        if review and review <= today:
            state = "EXPIRED"
        elif rev and rvk:
            state = "OK"
        elif acc is None or acc < CUTOFF:
            state = "LEGACY"
        else:
            state = "MISSING"
        out.append({"path": p, "accepted": acc, "review": review,
                    "revoke": rvk.group(1).strip() if rvk else None, "state": state})
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--legacy", action="store_true", help="only the undated pre-cutoff decisions")
    a = ap.parse_args()

    rows = scan()
    if a.legacy:
        rows = [r for r in rows if r["state"] == "LEGACY"]
        for r in rows:
            print(f"LEGACY  accepted {r['accepted'] or '?'}  {r['path'].name}")
        print(f"\n{len(rows)} decision(s) with no review date. Backfilling these is real work; "
              f"they do not fail the check.")
        return 0

    for r in rows:
        extra = ""
        if r["state"] == "EXPIRED":
            extra = f"  review date {r['review']} has passed and it still binds"
        elif r["state"] == "OK":
            extra = f"  review {r['review']}"
        print(f"{r['state']:<7} {r['path'].name}{extra}")

    expired = [r for r in rows if r["state"] == "EXPIRED"]
    missing = [r for r in rows if r["state"] == "MISSING"]
    legacy = [r for r in rows if r["state"] == "LEGACY"]
    print(f"\n{len(rows)} decision(s): {len(rows)-len(expired)-len(missing)-len(legacy)} ok, "
          f"{len(legacy)} legacy, {len(missing)} missing, {len(expired)} expired")

    if expired:
        print("\nEXPIRED means the decision passed its own review date. Re-read it, then either "
              "set a new Review by or change Status to Superseded. Do not just move the date.")
        return 2
    if missing:
        print(f"\nA decision accepted on or after {CUTOFF} must carry both lines:\n"
              "    **Review by:** YYYY-MM-DD\n"
              "    **Revoke if:** <a measurable condition, with the file or command that measures it>")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
