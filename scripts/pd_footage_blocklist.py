#!/usr/bin/env python
"""One reader for config/footage_blocklist.v001.json, used by every tool that enforces it.

Three tools enforced this list and each carried its own copy of the same six-line loader:
build_case_film_generic.py (refuses to emit a film), audit_films_vs_blocklist.py (reports films
already on disk) and prune_pool_by_blocklist.py (moves clips out of a staged pool). When the
list grew an episode scope on 2026-08-05 that would have been three places to change and three
chances to disagree, so the loader lives here once (CLAUDE.md invariant 14).

SCOPE, 2026-08-05. The file now has two arrays. `blocked` is HARD findings only -- third-party
production footage, a real identifiable minor, a real named person's identity captioned onto a
different real person, and legible personal data of a real private individual. `quality_deferred`
holds the 43 rows that were set aside so the channel could ship; they are accurate records of what
the shelf contains and they bind nothing. This loader reads `blocked` and nothing else.

WHAT CHANGED AND WHY. Ten shipped episodes recorded 108 visual-QC rejections against their own
masters. Most name a shelf clip that is wrong for every documentary -- an IRS Form 1040 with
readable field labels, a Tokyo patrol car, a scraped Rebel News report with its own chyron --
and those stay global. But some name a clip that is only wrong for ONE episode: handcuffs are
forbidden in EP55 burge and ordinary everywhere else, and the archive already returns nothing
for courtroom and handcuffs after 60 episodes, so a global ban costs real coverage. Worse, the
per-episode generated plates are numbered P01/P07/W066/F003 -- names that identify a completely
different picture in each of seven or eight episodes -- so blocking one globally would silently
remove unrelated images from unrelated films.

  * a row with no `episodes` key is GLOBAL: it binds in every episode (all pre-2026-08-05 rows).
  * a row with `episodes: [slug, ...]` binds ONLY for those episodes.

MATCHING. A cut's src is matched on its basename, the basename without its extension, and the
part before `__`, each also tried with the `AF-BG-` prefix stripped. That is a superset of the
matching the three tools did before, so no existing entry lost effect: `AR-4263` still matches
`AR-4263__ride_through_the_streets_of_london.mp4`, bare `9715` still matches
`AF-BG-9715__clock.mp4`, and `W066` now also matches `W066.mp4`.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCKLIST = ROOT / "config" / "footage_blocklist.v001.json"


def identifiers(src: str) -> set[str]:
    """Every name one asset can legitimately be blocked under."""
    base = str(src or "").replace("\\", "/").rsplit("/", 1)[-1]
    if not base:
        return set()
    stem = base.rsplit(".", 1)[0]
    out = {base, stem, base.split("__")[0], stem.split("__")[0]}
    out |= {x.replace("AF-BG-", "") for x in list(out)}
    return {x for x in out if x}


def load_blocked(slug: str | None = None, path: Path | None = None) -> dict[str, str]:
    """{identifier: 'label: reason'} for one episode.

    `slug=None` returns the GLOBAL rows only -- the rows that bind no matter which episode is
    being built. Pass the slug to add that episode's own scoped rows.
    """
    p = path or BLOCKLIST
    if not p.is_file():
        return {}
    doc = json.loads(p.read_text(encoding="utf-8"))
    # ONLY `blocked` binds. On 2026-08-05 the owner ruled that the shelf QC reject rate was one
    # the archive cannot sustain and the calendar was empty, so every finding that was a quality
    # judgement rather than a rights or safety one moved to `quality_deferred`. That key is a
    # record, not a rule: it is read here explicitly and discarded, so a future reader cannot
    # quietly start enforcing it by widening a `.get()`.
    doc.pop("quality_deferred", None)
    doc.pop("quality_deferred_note", None)
    blocked: dict[str, str] = {}
    for row in doc.get("blocked", []):
        scope = row.get("episodes")
        if scope is not None and (slug is None or slug not in scope):
            continue
        where = "global" if scope is None else f"episode-scoped to {', '.join(scope)}"
        for ident in row["ids"]:
            blocked[ident] = f"{row['label']} ({where}): {row['reason']}"
    return blocked


def reason_for(src: str, blocked: dict[str, str]) -> str | None:
    """The blocklist reason this src falls under, or None."""
    for ident in identifiers(src):
        why = blocked.get(ident)
        if why:
            return why
    return None


def hits(srcs, slug: str | None = None, path: Path | None = None) -> list[tuple[str, str]]:
    """[(basename, reason)] for every src that is blocked for this episode."""
    blocked = load_blocked(slug, path)
    out: list[tuple[str, str]] = []
    for src in srcs:
        why = reason_for(src, blocked)
        if why:
            out.append((str(src).replace("\\", "/").rsplit("/", 1)[-1], why))
    return out
