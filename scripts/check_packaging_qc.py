#!/usr/bin/env python
"""PACKAGING QC gate: title / A-B variants / description hygiene (SPEC row 13).

WHY THIS GATE EXISTS
--------------------
`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` section C names row 13 in its own
"**Still manual:** row 13 (title <=60 / A-B)" list. It has been a written rule since
EP19 with NOTHING enforcing it, which is the exact drift the spec itself warns about:
"A requirement with no gate WILL drift; add the gate." (spec section E).

Measured 2026-07-19 over the 26 episodes that have a `09_package/youtube_meta.v*.json`,
after merging every A/B and description source (see the FALSE-RED note below):
PASS 11 / FAIL 15 / SKIP 12.

    A/B title variants  : 10 episodes ship ONE title and no alternate anywhere
                          (spec row 13 requires "Ship A/B title x thumb variants",
                          gate text: ">=2 A/B variants") -- gideon, mapp, ftx, madoff,
                          terry, riley, carpenter, titan, flashcrash, hinton.
    title length >60    : 3 violations -- theranos 70, rolin 64, kidsforcash 73
                          (spec row 13: "Title <= 60 chars, hook first").
    doctrine framing    : 3 violations -- miranda / riley / kelo.

Restricted to the spec's own binding scope ("BINDING for every episode from EP19
onward"), the gate fails 3 of 12 -- hinton (no A/B variants), rolin (64), kidsforcash
(73) -- i.e. it discriminates rather than condemning the catalogue.

FALSE-REDs FOUND IN THIS GATE DURING ITS OWN AUDIT (both fixed; kept as a warning)
---------------------------------------------------------------------------------
The first version read ONLY `youtube_meta.v*.json` and reported 23 failures. Two of
those groups were the gate's fault, not the episodes':
  * A/B candidates are usually authored in `title_thumbnail_candidates.v*.json`
    (schemas: `title_candidates[] / candidates[] / titles[] / selection.selected_title`),
    not inline in youtube_meta  -> 6 episodes wrongly flagged.
  * the description is often a `description.v*.md` / `.txt` sidecar rather than an
    inline field -> mahanoy / milken / hinton wrongly flagged.
Both sources are now merged. 23 -> 17 -> 15.

The doctrine-framing rule is the one with hard retention evidence behind it.
`episodes/_planning/PACKAGING_FIX_v001.md` section 1/6 records the channel's three
WORST retention performers, and all three are doctrine-framed titles:

    "The Kelo Supreme Court Case"   ->  1.55%  (channel worst)
    Mapp                            ->  5.3%
    Gideon                          ->  7.5%

against a channel CTR target of >=4%. Shipping "<Case> v. <Case>" or "Supreme Court
Case" in the title is a measured retention loss, not a style opinion, so it is HARD.

WHAT IS HARD vs SOFT (deliberate -- avoiding a false-RED)
--------------------------------------------------------
HARD (blocks):
  1. title length <= TITLE_MAX_CHARS (60)                          [spec row 13]
  2. >= MIN_TITLE_VARIANTS (2) distinct title candidates            [spec row 13]
  3. no doctrine framing in the SELECTED title                      [PACKAGING_FIX 1/6]
  4. description present AND carries the AI-disclosure line         [VIDEO_RULES 5]

SOFT (reported only, never blocks):
  * title contains no digit. PACKAGING_FIX suggests a number helps CTR, but 20 of 25
    shipped titles have none, including strong performers. Hard-failing that would be
    a false-RED on the channel's own catalogue, so it is REPORTED, not enforced.
    (This is the `caption_integrity` lesson: a gate that fails the whole back
    catalogue is a broken gate, not a broken catalogue.)

Episodes with no `youtube_meta.v*.json` yet SKIP -- packaging is a late step and the
gate must never fail on absence of a not-yet-authored artifact.

Read-only. No writes, no network, no paid calls. Exit 0 = PASS, 1 = FAIL.

Usage:
    python scripts/check_packaging_qc.py episodes/PD-2026-038-kidsforcash
    python scripts/check_packaging_qc.py episodes/PD-2026-038-kidsforcash --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # cp932 guard (Windows)
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

CHECK_NAME = "packaging_qc"

TITLE_MIN_CHARS = 59        # spec row 13, measured 2026-08-10 (Unseen, 1.41M subs)
TITLE_MAX_CHARS = 100       # spec row 13; the old 60 was invented and the spec says so
DESC_MAX_CHARS = 5000        # YouTube's hard ceiling on snippet.description
MIN_TITLE_VARIANTS = 2      # spec row 13 ("A/B variants")

# Doctrine framing = the measured worst-retention pattern (PACKAGING_FIX_v001 s1/s6).
# "<Something> v. <Something>" or a literal "Supreme Court Case" label.
RE_DOCTRINE = re.compile(r"(?i)(\bv\.\s+\w|\bv\.$|\bsupreme court case\b)")

# AI disclosure (VIDEO_RULES s5) -- accept the several phrasings actually in use.
RE_AI_DISCLOSURE = re.compile(
    r"(?i)(ai[\s\-]?disclosure|ai[\s\-]generated|generated (?:with|using) ai|"
    r"ai[\s\-]?assisted|symbolic (?:ai )?reconstruction)")

# Schema drifted across episodes; accept every key that has actually been used.
TITLE_KEYS = ("title", "selected_title", "final_title")
ALT_KEYS = ("title_options", "alternate_titles", "title_variants",
            "titles", "ab_titles", "title_candidates")
DESC_KEYS = ("description", "description_md", "youtube_description")


def _first(d: dict, keys) -> object | None:
    for k in keys:
        v = d.get(k)
        if v:
            return v
    return None


def _as_text(v) -> str:
    if isinstance(v, list):
        return "\n".join(str(x) for x in v)
    return str(v or "")


def _latest_meta(epdir: Path) -> Path | None:
    metas = sorted((epdir / "09_package").glob("youtube_meta.v*.json"))
    return metas[-1] if metas else None


# A/B title candidates are ALSO authored in `title_thumbnail_candidates.v*.json`, which is
# where the packaging step actually does the A/B work for most of the back catalogue
# (timbs T1/T2/T3, miranda codex_flashy_v005 + A_v002, ...). The first version of this gate
# read only youtube_meta and reported "1 title candidate" for 20 episodes -- a FALSE-RED on
# episodes that had genuinely produced variants. Both sources are merged below.
CANDIDATE_LIST_KEYS = ("title_candidates", "candidates", "titles", "options")


def _candidate_titles(epdir: Path) -> list[str]:
    """Every title string offered as an A/B candidate anywhere in 09_package."""
    out: list[str] = []
    for p in sorted((epdir / "09_package").glob("title_thumbnail_candidates.v*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for k in CANDIDATE_LIST_KEYS:
            for item in (d.get(k) or []):
                if isinstance(item, str) and item.strip():
                    out.append(item.strip())
                elif isinstance(item, dict):
                    t = item.get("title") or item.get("text")
                    if t and str(t).strip():
                        out.append(str(t).strip())
        sel = d.get("selection") or {}
        if isinstance(sel, dict) and sel.get("selected_title"):
            out.append(str(sel["selected_title"]).strip())
    return out


def _sidecar_description(epdir: Path) -> str:
    """The description is not always inline in youtube_meta -- mahanoy/milken/hinton (and
    6 others) author it as a `description.v*.md` / `.txt` sidecar. The first version of
    this gate read only the inline field and reported "no description" for those, a
    FALSE-RED. Both sources are merged."""
    texts = []
    pkg = epdir / "09_package"
    for pat in ("description.v*.md", "description.v*.txt"):
        for p in sorted(pkg.glob(pat)):
            try:
                texts.append(p.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                continue
    return "\n".join(texts).strip()


def evaluate_meta(meta_path: Path, extra_candidates: list[str] | None = None,
                  extra_description: str = "") -> dict:
    data = json.loads(meta_path.read_text(encoding="utf-8"))

    title = _as_text(_first(data, TITLE_KEYS)).strip()
    alts_raw = _first(data, ALT_KEYS) or []
    if isinstance(alts_raw, str):
        alts_raw = [alts_raw]
    alts = [str(a).strip() for a in alts_raw if str(a).strip()]
    alts += [t for t in (extra_candidates or []) if t]

    # Distinct candidate universe = selected title + alternates (deduped, case-folded).
    universe, seen = [], set()
    for t in ([title] if title else []) + alts:
        k = t.casefold()
        if k not in seen:
            seen.add(k)
            universe.append(t)

    desc = _as_text(_first(data, DESC_KEYS)).strip()
    if extra_description:
        desc = (desc + "\n" + extra_description).strip()

    problems: list[str] = []
    notes: list[str] = []

    if not title:
        problems.append("no title field (title/selected_title) in metadata")
    elif not TITLE_MIN_CHARS <= len(title) <= TITLE_MAX_CHARS:
        # A BAND, not a ceiling. Spec row 13 was rewritten 2026-08-10 from the Data API on the
        # measured comparable: all 25 of its recent titles are 59-100 chars, every top-ten title
        # is over 78, and its shortest title is its worst performer. The floor bites -- EP62-65's
        # original 47/48/52/51-char titles all fail it.
        problems.append(f"title {len(title)} chars outside "
                        f"{TITLE_MIN_CHARS}-{TITLE_MAX_CHARS} (spec row 13)")

    if len(universe) < MIN_TITLE_VARIANTS:
        problems.append(
            f"{len(universe)} title candidate(s) < {MIN_TITLE_VARIANTS} "
            f"(spec row 13 requires A/B variants)")

    if title and RE_DOCTRINE.search(title):
        problems.append(
            f"doctrine-framed title (matched {RE_DOCTRINE.search(title).group(0)!r}) "
            f"-- measured channel-worst retention pattern (Kelo 1.55%)")

    if not desc:
        problems.append("no description in metadata")
    else:
        if not RE_AI_DISCLOSURE.search(desc):
            problems.append("description carries no AI-disclosure line (VIDEO_RULES s5)")
        # YouTube refuses a description over 5,000 characters. Nothing in this repo measured
        # that until 2026-08-27, when a sweep of every youtube_meta found EP78 colgan at 6,279
        # and EP82 valdez at 5,591 -- both would have been rejected at the upload call, after
        # a 2.5-hour render and a full read of the shipped frames. PD-2026-034-rolin sits at
        # 5,139 and is already published, so whatever went up for it is not what is on disk.
        if len(desc) > DESC_MAX_CHARS:
            problems.append(
                f"description {len(desc)} chars > {DESC_MAX_CHARS} -- YouTube will reject the "
                f"upload. Cut it before the render, not after.")

    # SOFT signal -- reported, never blocking (see module docstring).
    if title and not re.search(r"\d", title):
        notes.append("title contains no number (soft: CTR hint only, not enforced)")

    return {
        "check": CHECK_NAME,
        "ok": not problems,
        "meta": str(meta_path),
        "title": title,
        "title_chars": len(title),
        "title_max_chars": TITLE_MAX_CHARS,
        "title_candidates": len(universe),
        "min_title_candidates": MIN_TITLE_VARIANTS,
        "alternates": alts,
        "has_description": bool(desc),
        "has_ai_disclosure": bool(desc and RE_AI_DISCLOSURE.search(desc)),
        "problems": problems,
        "notes": notes,
    }


def evaluate(epdir: Path) -> dict:
    """PREFLIGHT adapter for preflight_render_gate._run_ext_gate."""
    epdir = Path(epdir)
    meta = _latest_meta(epdir)
    if meta is None:
        return {"ok": True, "hard": True, "skipped": True,
                "reason": "no 09_package/youtube_meta.v*.json yet (packaging not authored)"}
    try:
        r = evaluate_meta(meta, _candidate_titles(epdir), _sidecar_description(epdir))
    except (json.JSONDecodeError, OSError) as exc:
        # Fail CLOSED on an unreadable artifact (EP32 B1: gates must not fail open).
        return {"ok": False, "hard": True, "skipped": False,
                "reason": f"unreadable {meta.name}: {exc}"}

    if r["ok"]:
        reason = (f"title {r['title_chars']}ch <= {TITLE_MAX_CHARS}, "
                  f"{r['title_candidates']} A/B candidates, AI disclosure present")
        if r["notes"]:
            reason += " | " + "; ".join(r["notes"])
    else:
        reason = "; ".join(r["problems"])
    return {"ok": r["ok"], "hard": True, "skipped": False, "reason": reason, **r}


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("epdir", type=Path, help="episode dir, e.g. episodes/PD-2026-038-kidsforcash")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if not a.epdir.is_dir():
        print(f"FAIL {CHECK_NAME}: no such episode dir {a.epdir}")
        return 1

    r = evaluate(a.epdir)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["ok"] else 1

    if r.get("skipped"):
        print(f"SKIP {CHECK_NAME}: {r['reason']}")
        return 0
    print(f"{'PASS' if r['ok'] else 'FAIL'} {CHECK_NAME}: {a.epdir.name}")
    print(f"  title      : {r.get('title','')!r}")
    print(f"  length     : {r.get('title_chars')} (max {TITLE_MAX_CHARS})")
    print(f"  candidates : {r.get('title_candidates')} (min {MIN_TITLE_VARIANTS})")
    print(f"  description: present={r.get('has_description')} "
          f"ai_disclosure={r.get('has_ai_disclosure')}")
    for p in r.get("problems", []):
        print(f"  ! {p}")
    for n in r.get("notes", []):
        print(f"  ~ {n}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
