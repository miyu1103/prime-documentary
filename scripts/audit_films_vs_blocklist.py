#!/usr/bin/env python
"""Check every built film plan against the footage blocklist.

The builder now refuses to emit a film that names a blocked clip, but films built BEFORE that
guard existed are still on disk and some of them are rendered, uploaded and scheduled. This
answers the only question that matters after a clip is blocked: is it already inside something
that is going out?

    python scripts/audit_films_vs_blocklist.py

Exit 0 = no film references a blocked clip. Exit 1 = at least one does; the report names the
film, the clip, the reason, and the timecode so it can be judged rather than guessed at.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import pd_footage_blocklist

ROOT = Path(__file__).resolve().parents[1]
BLOCKLIST = pd_footage_blocklist.BLOCKLIST
DATA = ROOT / "remotion" / "src" / "data"


def main() -> int:
    if not BLOCKLIST.is_file():
        print(f"no blocklist at {BLOCKLIST}")
        return 0

    # THE RENDERED SNAPSHOTS TOO (added 2026-09-01). Auditing only remotion/src/data/*_film.json
    # answers a question nobody asked: what the film on the BENCH says. A film json is rebuilt
    # every time the finisher runs and can be rebuilt again afterwards by hand, so it drifts away
    # from the bytes that were actually rendered.
    # MEASURED: EP73 uri was reported CLEAN by this tool while the master on disk carried all five
    # clips blocked the day before -- three ABB nameplates, two Cyrillic cabinet placards and the
    # HollyFrontier wordmark on a tank. The bench film had been rebuilt clean at 11:45; the render
    # had finished at 06:05. The tool was reading a file five and a half hours younger than the
    # thing it was being trusted to describe.
    # episodes/*/08_edit/<slug>_film.rendered.json is written BY the render, so it is the only
    # film json that describes a master. It is now audited first and never skipped.
    films = sorted((ROOT / "episodes").glob("PD-*/08_edit/*_film.rendered.json")) + \
        sorted(DATA.glob("*_film.json"))
    bad = 0
    for film in films:
        try:
            d = json.loads(film.read_text(encoding="utf-8"))
        except Exception:
            continue
        # The film's own slug decides which rows apply: global rows plus the ones scoped to this
        # episode. Auditing every film against every episode's scoped rows would report EP55's
        # handcuff ban against films that are entitled to use handcuffs.
        slug = film.stem[: -len("_film")]
        blocked = pd_footage_blocklist.load_blocked(slug)
        # SPEC v2 row 9 (binds from EP66): `leadSeconds` moves the body to frame 0.
        # `is None`, not falsy -- EP66 declares 0.0. Absent, this is the old expression.
        _lead = d.get("leadSeconds")
        t = (float(d.get("hookSeconds") or 0) + 3.5) if _lead is None else float(_lead)
        hits = []
        for h in d.get("hook", []):
            why = pd_footage_blocklist.reason_for(h.get("src"), blocked)
            if why:
                hits.append((float(h.get("start") or 0), (h.get("src") or "").split("/")[-1], why))
        for c in d.get("cuts", []):
            base = (c.get("src") or "").split("/")[-1]
            why = pd_footage_blocklist.reason_for(c.get("src"), blocked)
            if why:
                hits.append((t, base, why))
            t += float(c.get("dur") or 0)
        if hits:
            bad += 1
            print(f"\n{film.stem}: {len(hits)} blocklisted cut(s)")
            for at, base, why in hits:
                print(f"  {int(at // 60):>3}:{int(at % 60):02d}  {base}")
                print(f"          {why}")

    print(f"\n{len(films)} film(s) checked, {bad} carrying a blocklisted clip")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
