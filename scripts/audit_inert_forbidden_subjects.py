#!/usr/bin/env python3
r"""Which shipped episodes carry footage that their own forbidden_subjects should have stopped?

WHY THIS EXISTS
---------------
Until 2026-08-21 `stage_footage_by_title.forbidden_hit` matched only single words. Every
forbidden subject written as a PHRASE -- "hong kong", "concert crowd", "european street",
"body bag", "steam locomotive" -- could never appear in the token list and could never fire.
Measured across every episode_spec on disk: **434 of 1,442 declared terms contain a space**,
30 %, and five episodes had no working term at all (weimer 12/12, correa 10/10, marmet 10/10,
greene 9/9, memphis 9/9).

The phrase matcher was fixed that day. This asks the retrospective question the main thread put
on 2026-08-22: **did anything actually get through while it was broken?**

It reads each episode's staged pool and its own spec, and reports clips whose ledger title or
staged name carries one of that episode's own MULTI-WORD forbidden subjects -- i.e. exactly the
class the old matcher could not see. Single-word terms are excluded from the report, because
those were always enforced and a hit there would be a different bug.

    py -3.11 scripts/audit_inert_forbidden_subjects.py
    py -3.11 scripts/audit_inert_forbidden_subjects.py --slug memphis

This reports. It changes nothing, stages nothing and deletes nothing. A hit is not proof the
clip reached the screen -- it proves the clip reached the POOL the builder draws from, which is
where EP64 memphis's sixteen rejected plates were when they were cut into a film.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from stage_footage_by_title import forbidden_hit, match_keys, title_words  # noqa: E402


def spec_for(ep_dir: Path) -> dict | None:
    specs = sorted(ep_dir.glob("episode_spec.v*.json"))
    if not specs:
        return None
    try:
        return json.loads(specs[-1].read_text(encoding="utf-8"))
    except Exception:
        return None


def staging_titles(slug: str) -> dict[str, str]:
    """{staged filename: ledger title} from the staging receipt, else {} ."""
    p = ROOT / "runs" / "qc" / f"{slug}_title_staging.v001.json"
    if not p.is_file():
        return {}
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    rows = d.get("rows") or d.get("staged") or (d if isinstance(d, list) else [])
    out = {}
    if isinstance(rows, dict):
        rows = list(rows.values())
    for r in rows:
        if isinstance(r, dict):
            k = r.get("staged_as") or r.get("name") or ""
            if k:
                out[k] = r.get("title") or r.get("ledger_title") or ""
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug")
    a = ap.parse_args()

    eps = sorted((ROOT / "episodes").glob("PD-*"))
    total_multi = total_hits = checked = 0
    findings: list[tuple[str, str, str, str]] = []

    for ep in eps:
        if not ep.is_dir():
            continue
        slug = ep.name.split("-", 3)[-1]
        if a.slug and slug != a.slug:
            continue
        spec = spec_for(ep)
        if not spec:
            continue
        forb = spec.get("forbidden_subjects") or []
        multi = frozenset(t for t in forb if " " in t)
        if not multi:
            continue
        pool = ROOT / "remotion" / "public" / slug / "factory"
        clips = sorted(pool.glob("*.mp4")) if pool.is_dir() else []
        if not clips:
            continue
        checked += 1
        total_multi += len(multi)
        titles = staging_titles(slug)
        for c in clips:
            hay = f"{titles.get(c.name, '')} {c.stem}"
            w = title_words(hay)
            hit = forbidden_hit(multi, w, match_keys(w))
            if hit:
                total_hits += 1
                findings.append((slug, hit, c.name[:64], titles.get(c.name, "")[:60]))

    print(f"episodes with a staged pool AND multi-word forbidden subjects: {checked}")
    print(f"multi-word terms across them: {total_multi}")
    print(f"clips in a pool carrying one of their own episode's phrase bans: {total_hits}\n")
    if not findings:
        print("No staged clip carries a phrase its own episode forbids.")
        print("That does not clear the period -- it says the pools ON DISK are clean now.")
        return 0
    by_slug: dict[str, list] = {}
    for s, hit, name, title in findings:
        by_slug.setdefault(s, []).append((hit, name, title))
    for s, rows in sorted(by_slug.items(), key=lambda x: -len(x[1])):
        print(f"[{s}] {len(rows)} clip(s)")
        for hit, name, title in rows[:8]:
            print(f'    {hit!r:24} {name}')
            if title:
                print(f'    {"":24} ledger title: {title}')
        if len(rows) > 8:
            print(f"    ... and {len(rows) - 8} more")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
