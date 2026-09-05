#!/usr/bin/env python3
"""Read the per-item licence for shelf rows that were held pending exactly that lookup.

WHY THIS EXISTS
---------------
`reindex_archive_shelf.py` correctly refused to guess: Freesound, Wikimedia, the Library of
Congress, NARA and Smithsonian all carry licences PER ITEM, so it set `review_required` and wrote
the reason into `reindex_basis`:

    8635  Freesound is PER-ITEM (CC0 / CC-BY / CC-BY-NC): the item licence must be re-read from the id
    5540  Wikimedia files carry per-file licences
    2724  Library of Congress items carry per-item rights
    2694  NARA holdings are mixed: federal records are PD, donated materials may carry rights
     751  Smithsonian Open Access is per-item

Measured 2026-09-02: **the lookup it asked for was never run.** 20,731 rows have been sitting at
`review_required` ever since, and every one of them still carries its source id, so the licence is
recoverable. This does the lookup.

THE RULE IT APPLIES
-------------------
Only **CC0 and public domain** become usable. CC-BY and anything stricter stays held, which is the
policy `ingest_archive_sources.py` already follows ("CC-BY -> quarantine, attribution recorded").
This tool does not loosen it: an item that needs attribution is not silently promoted.

Nothing is written to the ledger here -- this produces `runs/item_licence_verdicts.v001.json`, and
`apply_item_licence_verdicts.py` is what changes decisions. The network step is cached per source
and can be re-run any number of times without touching data.

    py -3.11 scripts/resolve_item_licences.py --source wikimedia --limit 5   # smoke
    py -3.11 scripts/resolve_item_licences.py --source freesound
    py -3.11 scripts/resolve_item_licences.py --source all
"""
from __future__ import annotations

import argparse
import collections
import glob
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest_archive_sources import LEDGER_DIR  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / "runs" / "_cache"
VERDICTS = ROOT / "runs" / "item_licence_verdicts.v001.json"
SOURCES = ("wikimedia", "freesound", "loc", "nara", "smithsonian")
UA = {"User-Agent": "PrimeDocumentary-rights-audit/1.0 (https://github.com/; documentary rights audit; contact via repository owner)"}

# Text that means "no rights reserved". Anything else -- CC-BY, CC-BY-SA, NC, ND, "rights
# advisory", "permission required" -- is NOT promoted, on purpose.
FREE_PAT = re.compile(
    r"\b(cc0|creativecommons\.org/publicdomain/zero|public domain mark|publicdomain/mark|"
    r"no known copyright|no known restrictions|public domain|pd-us|pdm)\b", re.I)
# Explicit blockers, checked first so "public domain" inside a longer caveat cannot win.
BLOCK_PAT = re.compile(
    r"\b(cc[- ]?by|noncommercial|non-commercial|\bnc\b|noderiv|\bnd\b|share[- ]?alike|"
    r"all rights reserved|rights advisory|permission|restricted|copyright(ed)?\b)", re.I)


def env(name: str) -> str:
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text("utf-8", errors="replace").splitlines():
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get(name, "")


def get_json(url: str, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as fh:
        return json.load(fh)


def held_rows() -> list[dict]:
    out = []
    for f in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl"))):
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("license_decision") != "review_required" or r.get("rights_verdict"):
                continue
            if r.get("source") in SOURCES and r.get("id"):
                out.append(r)
    return out


def verdict_from_text(text: str) -> tuple[str, str]:
    """A licence string in, (verdict, evidence) out. Blockers win over free words."""
    t = (text or "").strip()
    if not t:
        return "unknown", "(source returned no rights text)"
    # NARA answers in its own vocabulary rather than a licence name, so it is decided here
    # instead of by the licence regexes. Both statuses must read Unrestricted: "Undetermined"
    # is NARA saying nobody has checked, which is not a yes.
    if t.startswith("nara use="):
        low = t.lower()
        if "use=unrestricted" in low and "access=unrestricted" in low:
            return "free", t
        return "held", t
    if BLOCK_PAT.search(t):
        return "held", t[:150]
    if FREE_PAT.search(t):
        return "free", t[:150]
    return "unknown", t[:150]


# --- per-source lookups -------------------------------------------------------------------

def _wikimedia_paths() -> dict:
    """id -> file_path, read once. The lookup below needs the FILE, not the id."""
    out = {}
    for f in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl"))):
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("source") == "wikimedia" and r.get("id") and r.get("file_path"):
                out[r["id"]] = r["file_path"]
    return out


def look_wikimedia(ids: list[str], cache: dict) -> None:
    """Identify each file by the SHA1 of its own bytes, because the stored id is unusable.

    The ledger truncates the Commons title at 60 characters and normalises its punctuation
    ("File_10_Dollars_-_National_Commercial_Savings_Bank_Ltd._1924" for a file actually titled
    "10 Dollars - National Commercial & Savings Bank, Ltd. (...)"), so an exact title lookup and
    an allpages prefix search both returned NO MATCH when measured on 2026-09-02.

    The file itself is on disk, and Commons indexes uploads by SHA1: `list=allimages&aisha1=`
    answers with the real title and its licence. Three files tested that way matched on the first
    try and came back Public domain, CC0, Public domain. Note SHA1 -- the ledger stores SHA256,
    so this hashes the bytes again rather than reusing the recorded digest.
    """
    paths = _wikimedia_paths()
    for i in ids:
        if i in cache:
            continue
        p = paths.get(i)
        if not p or not os.path.exists(p):
            cache[i] = {"error": "file not on disk"}
            continue
        h = hashlib.sha1()
        try:
            with open(p, "rb") as fh:
                for block in iter(lambda: fh.read(1 << 20), b""):
                    h.update(block)
        except OSError as exc:
            cache[i] = {"error": str(exc)[:70]}
            continue
        url = ("https://commons.wikimedia.org/w/api.php?action=query&format=json"
               "&list=allimages&aiprop=extmetadata&aisha1=" + h.hexdigest())
        try:
            d = get_json(url)
            imgs = (d.get("query") or {}).get("allimages") or []
            if not imgs:
                cache[i] = {"licence": "", "note": "no Commons file has these bytes"}
            else:
                em = imgs[0].get("extmetadata") or {}
                lic = " ".join(str((em.get(k) or {}).get("value", "")) for k in
                               ("LicenseShortName", "UsageTerms", "License"))
                cache[i] = {"licence": lic, "title": str(imgs[0].get("title", ""))[:120]}
        except Exception as exc:
            cache[i] = {"error": str(exc)[:70]}
        # Commons throttles anonymous clients: 0.12 s got 3,901 x HTTP 429 after ~630 lookups
        # on 2026-09-02. Half a second is slower than the shelf needs and fast enough to finish.
        time.sleep(0.5)


def look_freesound(ids: list[str], cache: dict) -> None:
    key = env("FREESOUND_API_KEY")
    if not key:
        raise SystemExit("FREESOUND_API_KEY missing from .env")
    for i in ids:
        if i in cache:
            continue
        url = f"https://freesound.org/apiv2/sounds/{i}/?token={key}&fields=license,name"
        try:
            d = get_json(url)
            cache[i] = {"licence": str(d.get("license", ""))}
        except Exception as exc:
            cache[i] = {"error": str(exc)[:70]}
        time.sleep(0.12)


def look_loc(ids: list[str], cache: dict) -> None:
    for i in ids:
        if i in cache:
            continue
        try:
            d = get_json(f"https://www.loc.gov/item/{i}/?fo=json")
            item = d.get("item") or {}
            lic = " ".join(str(x) for x in (
                item.get("rights"), item.get("rights_advisory"),
                item.get("access_restricted"), item.get("rights_information")) if x)
            cache[i] = {"licence": lic}
        except Exception as exc:
            cache[i] = {"error": str(exc)[:70]}
        time.sleep(0.15)


def look_nara(ids: list[str], cache: dict) -> None:
    key = env("DATA_GOV_API_KEY")
    for i in ids:
        if i in cache:
            continue
        # /api/v2 returns the catalogue's HTML shell even with a valid x-api-key; /proxy is the
        # endpoint the catalogue's own front end calls and it answers JSON without a key.
        na = i.split("-")[0]
        url = f"https://catalog.archives.gov/proxy/records/search?naId={na}&limit=1"
        req = urllib.request.Request(url, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=30) as fh:
                d = json.load(fh)
            hits = ((d.get("body") or {}).get("hits") or {}).get("hits") or []
            rec = (hits[0].get("_source") or {}).get("record", {}) if hits else {}
            # NARA answers with its own controlled vocabulary, not a licence string:
            #   useRestriction.status    Unrestricted | Restricted | Undetermined
            #   accessRestriction.status same
            # Only Unrestricted on BOTH is a federal record free of restrictions. "Undetermined"
            # is not a yes -- it is NARA saying nobody has checked, which is where this shelf
            # already was.
            def st(field):
                v = rec.get(field)
                return str((v or {}).get("status", "")) if isinstance(v, dict) else str(v or "")
            u, a = st("useRestriction"), st("accessRestriction")
            cache[i] = {"licence": f"nara use={u or '?'} access={a or '?'}"}
        except Exception as exc:
            cache[i] = {"error": str(exc)[:70]}
        time.sleep(0.15)


def look_smithsonian(ids: list[str], cache: dict) -> None:
    key = env("DATA_GOV_API_KEY")
    for i in ids:
        if i in cache:
            continue
        url = (f"https://api.si.edu/openaccess/api/v1.0/content/{urllib.parse.quote(i)}"
               f"?api_key={key}")
        try:
            d = get_json(url)
            resp = d.get("response") or {}
            cont = (resp.get("content") or {})
            usage = json.dumps(cont.get("descriptiveNonRepeating", {}).get("metadata_usage", {}))
            cache[i] = {"licence": usage}
        except Exception as exc:
            cache[i] = {"error": str(exc)[:70]}
        time.sleep(0.15)


LOOKUPS = {"wikimedia": look_wikimedia, "freesound": look_freesound, "loc": look_loc,
           "nara": look_nara, "smithsonian": look_smithsonian}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="all", help="one of: " + ", ".join(SOURCES) + ", all")
    ap.add_argument("--limit", type=int, default=0, help="smoke-test on N rows per source")
    args = ap.parse_args()
    wanted = SOURCES if args.source == "all" else (args.source,)
    for w in wanted:
        if w not in SOURCES:
            sys.exit(f"unknown source {w!r}")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    rows = held_rows()
    by_src: dict[str, list[dict]] = collections.defaultdict(list)
    for r in rows:
        by_src[r["source"]].append(r)

    out: dict[str, list] = collections.defaultdict(list)
    if VERDICTS.exists():
        out.update(json.loads(VERDICTS.read_text("utf-8")))

    for src in wanted:
        items = by_src.get(src, [])
        if args.limit:
            items = items[:args.limit]
        if not items:
            print(f"{src:12s} nothing held")
            continue
        cpath = CACHE_DIR / f"licences_{src}.json"
        cache = json.loads(cpath.read_text("utf-8")) if cpath.exists() else {}
        print(f"{src:12s} {len(items)} row(s), {len(cache)} cached ...", flush=True)
        try:
            LOOKUPS[src]([r["id"] for r in items], cache)
        finally:
            cpath.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")

        tally = collections.Counter()
        fresh = [x for x in out.get(src, []) if False]  # replaced wholesale each run
        for r in items:
            rec = cache.get(r["id"]) or {}
            if "error" in rec:
                v, ev = "unknown", "lookup failed: " + rec["error"]
            else:
                v, ev = verdict_from_text(rec.get("licence", ""))
            tally[v] += 1
            fresh.append({"id": r["id"], "verdict": v, "evidence": ev,
                          "title": r.get("title"), "theme": r.get("theme")})
        out[src] = fresh
        print(f"{'':12s} free={tally['free']} held={tally['held']} unknown={tally['unknown']}")

    VERDICTS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nwrote {VERDICTS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
