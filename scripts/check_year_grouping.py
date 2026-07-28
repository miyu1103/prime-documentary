#!/usr/bin/env python3
"""Preflight gate: catch the thousands-comma year bug BEFORE render.

The Remotion NumberTicker comma-groups by default, so a numberticker figure with
a 4-digit year value (1989, 2001, 2014, ...) renders as "1,989" / "2,001" — a
prominent, held on-screen defect (seen on EP46 tlo "1,985" and EP47 atwater
"2,001"). A `group` opt now exists on NumberTicker/FigureBeats; any year figure
MUST set group:false.

This gate scans a film.json's figures[] for numberticker entries whose integer
value looks like a year (1000-2999) and does NOT have group == false, and FAILS.

    py -3.11 scripts/check_year_grouping.py remotion/src/data/<slug>_film.json
Exit 0 = PASS, 1 = FAIL (a year figure would render with a comma).
"""
from __future__ import annotations
import json, sys
from pathlib import Path


def check(film_path: str) -> int:
    p = Path(film_path)
    if not p.exists():
        print(f"BLOCKED: film.json not found: {film_path}")
        return 1
    d = json.loads(p.read_text(encoding="utf-8"))
    figs = d.get("figures") or []
    bad = []
    for i, f in enumerate(figs):
        if (f.get("kind") or f.get("type")) != "numberticker":
            continue
        v = f.get("value")
        if not isinstance(v, int):
            continue
        # a year-like value that would get a thousands comma
        if 1000 <= v <= 2999 and f.get("group") is not False:
            bad.append((i, v, f.get("label")))
    if bad:
        print(f"FAIL check_year_grouping: {len(bad)} numberticker year figure(s) will render with a thousands comma (set group:false):")
        for i, v, label in bad:
            print(f"  figures[{i}] value={v} -> would render '{v:,}'  label={label!r}")
        return 1
    n = sum(1 for f in figs if (f.get("kind") or f.get("type")) == "numberticker")
    print(f"PASS check_year_grouping: {n} numberticker figure(s), 0 year-comma risks.")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) < 2:
        print("usage: check_year_grouping.py <film.json>")
        raise SystemExit(2)
    raise SystemExit(check(sys.argv[1]))
