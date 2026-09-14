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
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import pd_experiments  # noqa: E402
import check_decisions  # noqa: E402

JST = dt.timezone(dt.timedelta(hours=9))
BAR = "-" * 78


def compact() -> int:
    """A few lines, printed automatically at session start. Loud only when a person is needed.

    Nobody should have to remember to run this, and nobody should have to read a screenful of
    it every time. It prints the number that decides the month and what may not be touched,
    and shouts only when an experiment is due or a decision has outlived its own review date.
    """
    reg = pd_experiments.load()
    b = reg["measured_baselines"]
    ctr = b["long_form_ctr_pct_median"]["value"]
    views = b["long_form_lifetime_views_median"]["value"]
    print(f"PD  long-form CTR {ctr}% (median) | lifetime views per film {views} (median)")

    locked = len(pd_experiments.locks("title"))
    if locked:
        nxt = min((e["read_on"] for e in reg["experiments"]
                   if str(e.get("read_on", "")).startswith("20")), default="-")
        print(f"    {locked} video ids locked: no retitle, no new thumbnail. Next read {nxt}.")
        print("    apply_title_batch.py refuses them. A change made by hand in Studio is unseen.")

    dues = pd_experiments.due()
    if dues:
        print("    !! DUE NOW: " + ", ".join(e["experiment_id"] for e in dues))

    bad = [r for r in check_decisions.scan() if r["state"] in ("EXPIRED", "MISSING")]
    if bad:
        print("    !! decisions needing a date: "
              + ", ".join(f"{r['path'].name} ({r['state']})" for r in bad))

    stopped = ", ".join(s["what"] for s in reg.get("stopped", []))
    if stopped:
        print(f"    stopped, do not restart: {stopped}")
    print("    py -3.11 scripts/pd_brief.py --full   # the numbers, their sources, and why")
    return 0


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if "--full" not in sys.argv:
        return compact()
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
    # scan() rather than main(): main() parses sys.argv, and this module has its own flags.
    rows = check_decisions.scan()
    counts = Counter(r["state"] for r in rows)
    print(f"  {len(rows)} decision(s): " +
          ", ".join(f"{n} {s.lower()}" for s, n in sorted(counts.items())))
    for r in rows:
        if r["state"] in ("EXPIRED", "MISSING"):
            print(f"  {r['state']:<7} {r['path'].name}")
    if counts.get("EXPIRED") or counts.get("MISSING"):
        print("  py -3.11 scripts/check_decisions.py    # the full list and what to write")
    else:
        print("  nothing expired, nothing new left undated "
              "(pre-2026-08-23 ones are LEGACY: --legacy lists them)")

    print(f"\n{BAR}")
    print("NEXT")
    print(BAR)
    print("  py -3.11 scripts/handover_snapshot.py      # what the machine is doing right now")
    print("  py -3.11 scripts/daily_status.py           # publishing stock, quota, next command")
    print("  docs/HANDOVER.md                           # the narrative — reasons, not numbers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
