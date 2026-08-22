#!/usr/bin/env python3
"""One screen: what the channel has decided, what it is measuring, and what you must not touch.

WHY THIS EXISTS
---------------
Before starting work a thread is told to read `CLAUDE.md`, `docs/PD_CANON.md`,
`docs/HANDOVER.md`, `.claude/rules/`, `PD_ONE_PASS_PRODUCTION_SPEC.v2` and
`PD_EDITORIAL_DIRECTION.v002`. Measured 2026-08-23: **141,335 characters.** Ten of the numbers
in them contradicted each other, because the same figure was written into prose in more than
one place. Prose cannot be kept consistent by intention at that size.

So the numbers moved into `config/pd_experiments.v001.json` and this prints them. The prose
stays -- it carries the reasoning, which a machine cannot produce -- but it stops being the
place a number is looked up.

NOT A DUPLICATE OF `daily_status.py`. That one measures the publishing machine (Shorts stock,
quota, TikTok queue) and tells you the next command. This one measures the *decisions*:
experiments, their read dates, their locks, and which decisions have expired. Neither reads
the other's numbers.

Usage:
    py -3.11 scripts/pd_brief.py
"""
from __future__ import annotations

import datetime as dt
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import pd_experiments  # noqa: E402
import check_decisions  # noqa: E402

JST = dt.timezone(dt.timedelta(hours=9))
BAR = "-" * 78


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    now = dt.datetime.now(JST)
    reg = pd_experiments.load()
    print(f"=== PD BRIEF — {now:%Y-%m-%d %H:%M} JST ===")
    print("Numbers below are the register's only copy. If prose disagrees, this wins.\n")

    print(BAR)
    print("THE NUMBERS THAT DECIDE THE MONTH")
    print(BAR)
    b = reg["measured_baselines"]
    for key in ("long_form_thumbnail_impressions_28d", "long_form_ctr_pct_median",
                "long_form_videos_below_2pct_ctr", "long_form_videos_statistically_readable",
                "long_form_lifetime_views_median"):
        v = b[key]
        print(f"  {key:<44} {v['value']}")
    print(f"\n  Read the source line before quoting any of these:")
    print(f"  config/pd_experiments.v001.json -> measured_baselines")
    print(f"\n  INSTRUMENT WARNING: {b['instrument_disagreement']['what']} —")
    print(f"    {b['instrument_disagreement']['values']}")
    print(f"    -> {b['instrument_disagreement']['resolution']}")

    print(f"\n{BAR}")
    print("EXPERIMENTS")
    print(BAR)
    for exp in reg["experiments"]:
        if exp["status"] in ("completed", "cancelled"):
            continue
        r = exp.get("read_on", "-")
        try:
            days = (dt.date.fromisoformat(r) - now.date()).days
            when = f"{r} (in {days} d)" if days >= 0 else f"{r} !! DUE {-days} d ago"
        except ValueError:
            when = r
        print(f"  [{exp['status']:<7}] {exp['experiment_id']:<26} read {when}")
        print(f"             {exp.get('owner_visible_name','')}")
    dues = pd_experiments.due()
    if dues:
        print("\n  !! DUE NOW — read these before starting anything else:")
        for e in dues:
            print(f"     {e['experiment_id']}  ({e.get('receipt','no receipt path recorded')})")

    print(f"\n{BAR}")
    print("DO NOT TOUCH")
    print(BAR)
    for kind in pd_experiments.KINDS:
        lk = pd_experiments.locks(kind)
        if lk:
            print(f"  {len(lk):>3} video id(s) locked against a {kind} change   "
                  f"(--locks {kind} to list)")
    print("  Enforced: scripts/apply_title_batch.py refuses before its first write.")
    print("  NOT enforced: a change made by hand in the Studio UI. Nothing can see that.")
    for s in reg.get("stopped", []):
        print(f"\n  STOPPED {s['what']} ({s['decided_at']})")
        print(f"    why:  {s['measurement']}")
        print(f"    cost if this was wrong: {s['cost_of_being_wrong']}")
    for k in reg.get("not_stopped_and_why", []):
        print(f"\n  KEEP  {k['what']}")
        print(f"    why:  {k['why']}")

    print(f"\n{BAR}")
    print("DECISIONS")
    print(BAR)
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = check_decisions.main()
    for line in buf.getvalue().splitlines():
        if line.startswith(("EXPIRED", "MISSING")) or line.startswith(("12 ", "11 ")) or \
           " decision(s):" in line:
            print("  " + line)
    if rc == 0:
        print("  no decision is expired or undated (LEGACY ones listed by --legacy)")
    else:
        print("  py -3.11 scripts/check_decisions.py    # the full list and what to write")

    print(f"\n{BAR}")
    print("NEXT")
    print(BAR)
    print("  py -3.11 scripts/handover_snapshot.py      # what the machine is doing right now")
    print("  py -3.11 scripts/daily_status.py           # publishing stock, quota, next command")
    print("  docs/HANDOVER.md                           # the narrative — reasons, not numbers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
