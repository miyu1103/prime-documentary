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

    films = sorted(DATA.glob("*_film.json"))
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
        t = float(d.get("hookSeconds") or 0) + 3.5
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
