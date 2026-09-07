#!/usr/bin/env python3
"""Fetch the facts section of shortlisted opinions so a human can judge the story.

The search API returns a snippet that is usually the caption block — court name, docket
number, judge — which says nothing about what happened. This pulls the opinion text itself
and extracts the part where the court narrates the events, so the shortlist becomes
readable without opening twenty tabs.

Heuristic, and stated as such: courts do not tag their facts section. We take the first
run of prose after the caption that contains past-tense event language, cutting at the
point where the legal analysis starts ("We review", "The standard of review", etc.).

    py -3.11 scripts/fetch_caselaw_facts.py --top 12
    py -3.11 scripts/fetch_caselaw_facts.py --clusters 4778177 10612573
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEAS = ROOT / "episodes" / "_planning" / "measurements"
API = "https://www.courtlistener.com/api/rest/v4/opinions/"
DEFAULT_INPUTS = [MEAS / "CASELAW_HARVEST.json", MEAS / "CASELAW_HARVEST_B.json"]
DEFAULT_OUT = MEAS / "CASELAW_FACTS.md"

ANALYSIS_START = re.compile(
    r"\b(we review|standard of review|the standard of review|analysis\b|discussion\b|"
    r"we begin (our|by)|for the (foregoing|above) reasons|it is well[- ]settled|"
    r"we now turn|conclusion\b)", re.I)
CAPTION_END = re.compile(
    r"\b(OPINION|PER CURIAM|MEMORANDUM|delivered the opinion|for the Court|"
    r"Circuit Judge|District Judge|J\.,|JUSTICE\b)", re.I)
EVENT = re.compile(
    r"\b(seiz\w+|arrest\w+|stopp?ed|search\w+|shot|killed|died|convict\w+|sentenc\w+|"
    r"pleaded|pled|testif\w+|confess\w+|filed|took|home|house|daughter|son|wife|"
    r"husband|mother|father|child|police|officer|deputy|agent)\b", re.I)


def load_token() -> str:
    """Read COURTLISTENER_TOKEN from environment or .env. Never logged."""
    tok = os.environ.get("COURTLISTENER_TOKEN", "").strip()
    if tok:
        return tok
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("COURTLISTENER_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("COURTLISTENER_TOKEN not found in environment or .env")


def get(url: str, token: str, timeout: int) -> dict:
    """GET with backoff. Their endpoints throttle in bursts; 429 is a wait, not a failure."""
    headers = {"Authorization": f"Token {token}", "User-Agent": "PD-research/1.0"}
    for i, wait in enumerate([10, 30, 60, 0]):
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(url, headers=headers), timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 502, 503, 504) or wait == 0:
                raise
            ra = e.headers.get("Retry-After")
            pause = int(ra) if (ra or "").isdigit() else wait
            print(f"    HTTP {e.code} — waiting {pause}s", flush=True)
            time.sleep(pause)
    raise RuntimeError("unreachable")


def facts_of(text: str, max_chars: int) -> str:
    """Pull the narrative part out of an opinion. Heuristic; see module docstring.

    Opinions that came from a PDF arrive hard-wrapped at ~80 columns, so a paragraph is a
    run of short lines separated by a blank line — never one long line. An earlier version
    collapsed blank lines first and then looked for lines over 120 characters, which found
    nothing in 8 of 10 opinions. Paragraph boundaries are therefore resolved before any
    whitespace is normalised.
    """
    text = re.sub(r"<[^>]+>", " ", text or "")
    if not text.strip():
        return ""
    m = list(CAPTION_END.finditer(text[:6000]))
    body = text[m[-1].end():] if m else text
    chunks = re.split(r"\n[ \t]*\n", body)
    if len(chunks) < 3:  # no blank lines at all: treat the whole thing as one block
        chunks = [body]
    paras = []
    for ch in chunks:
        p = re.sub(r"\s+", " ", ch).strip()
        if len(p) > 120:
            paras.append(p)
    out: list[str] = []
    for p in paras:
        if ANALYSIS_START.search(p) and out:
            break
        if EVENT.search(p) or out:
            out.append(p)
        if sum(len(x) for x in out) > max_chars:
            break
    return " ".join(out)[:max_chars].strip()


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inputs", nargs="*", default=[str(p) for p in DEFAULT_INPUTS])
    ap.add_argument("--clusters", nargs="*", type=int, default=[],
                    help="explicit cluster ids; otherwise the top scorers are used")
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--max-chars", type=int, default=1800)
    ap.add_argument("--sleep", type=float, default=3.0)
    ap.add_argument("--timeout", type=int, default=90)
    ap.add_argument("--output", default=str(DEFAULT_OUT))
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    rows: list[dict] = []
    for p in a.inputs:
        path = Path(p)
        if path.exists():
            rows.extend(json.loads(path.read_text(encoding="utf-8")).get("candidates") or [])
    if not rows:
        print("no candidates loaded", file=sys.stderr)
        return 2

    sys.path.insert(0, str(ROOT / "scripts"))
    from shortlist_caselaw_topics import existing_topics, story_score  # same ranking

    made = existing_topics()
    seen: set[int] = set()
    ranked: list[dict] = []
    for c in rows:
        cid = int(c.get("cluster_id") or 0)
        if cid in seen:
            continue
        seen.add(cid)
        s, why, hit = story_score(c, made)
        ranked.append(dict(c, story_score=s, already_made=hit))
    ranked.sort(key=lambda c: -c["story_score"])

    picked = ([c for c in ranked if c["cluster_id"] in set(a.clusters)]
              if a.clusters else ranked[:a.top])
    if a.dry_run:
        for c in picked:
            print(f"{c['story_score']:>6.1f}  {c['case_name'][:70]}")
        print(f"\n(dry run — would fetch {len(picked)} opinions)")
        return 0

    out = Path(a.output)
    if out.exists() and not a.force:
        print(f"{out} exists; pass --force", file=sys.stderr)
        return 2

    token = load_token()
    lines = ["# CASE-LAW FACTS — 上位候補の「何が起きたか」",
             "",
             "Fetched by `scripts/fetch_caselaw_facts.py` from the opinion text itself. The "
             "facts section is located heuristically — courts do not tag it — so read the "
             "linked opinion before trusting any sentence here. Nothing below is verified for "
             "broadcast; it is here so a human can decide which case is a film.",
             ""]
    for i, c in enumerate(picked, 1):
        print(f"[{i}/{len(picked)}] {c['case_name'][:60]}", flush=True)
        body = ""
        try:
            d = get(API + "?" + urllib.parse.urlencode(
                {"cluster": c["cluster_id"], "fields": "plain_text,html_with_citations"}),
                token, a.timeout)
            for op in (d.get("results") or []):
                body = op.get("plain_text") or op.get("html_with_citations") or ""
                if body:
                    break
        except Exception as e:
            body = ""
            print(f"    fetch failed: {str(e)[:90]}")
        facts = facts_of(body, a.max_chars)
        lines += [f"## {i}. {c['case_name']}", "",
                  f"- {c['lane_label']}",
                  f"- {c['court']} · {c['date_filed']} · cites {c['cite_count']}",
                  f"- {c['url']}",
                  f"- story score **{c['story_score']}**"
                  + (f" · ⚠ 既出の疑い: {c['already_made']}" if c["already_made"] else ""),
                  ""]
        lines += [facts if facts else "_(opinion text not available via API — open the link)_", ""]
        time.sleep(a.sleep)

    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    tmp.replace(out)
    try:
        shown = out.relative_to(ROOT)
    except ValueError:
        shown = out
    print(f"\nwrote {shown}  ({len(picked)} opinions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
