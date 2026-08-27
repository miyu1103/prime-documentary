#!/usr/bin/env python3
"""Ask archive.org which COLLECTION each held item sits in, and decide from that.

A title tells you what an uploader called a file. A collection tells you where the archive put
it, and that is the only rights signal on archive.org that the uploader does not control. This
reads `collection`, `creator`, `licenseurl` and `mediatype` for every row the ledger is holding
under `reindex_basis == "uploader_asserted_licenseurl"`, caches the answers, and sorts them:

  free      : in a collection the archive itself curates as public domain / government output
  paywalled : in a collection that is explicitly other people's copyrighted work
  eyes      : neither -- a person has to look at it

Nothing is written back to the ledger here. This produces the evidence; `apply_ia_collection_
verdicts.py` is what changes decisions, so the network step can be re-run without touching data.

    py -3.11 scripts/audit_ia_collections.py                 # fetch + classify
    py -3.11 scripts/audit_ia_collections.py --show eyes 40  # look at a bucket
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest_archive_sources import LEDGER_DIR  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "runs" / "_cache" / "ia_collections.json"

# Collections archive.org itself curates. Membership is set by the archive, not the uploader.
FREE_COLLECTIONS = {
    "prelinger", "prelingerarchives", "nasa", "nasa_techdocs", "jplvideos",
    "usnationalarchives", "us_national_archives", "universal_newsreels", "newsreels",
    "gov_docs", "usgovernmentdocuments", "us_house_of_representatives", "c-span",
    "publicresource", "public_resource", "librarycongress", "library_of_congress",
    "nationalscreeningroom", "fedflix", "nara", "usdoj", "smithsonian",
    "computerchronicles", "openbeelden", "sfarchives",
    # measured 2026-08-27 in the held set: federal output and state-archive digitisation
    "us_congress", "usgovfilms", "usnavybumedhistoryoffice", "medicalheritagelibrary",
    "californiarevealed", "californiastatearchives", "wwiiarchive",
}
# Collections that are, by their own description, other people's copyrighted work.
PAY_COLLECTIONS = {
    "feature_films", "featurefilms", "film_noir", "classic_tv", "television",
    "tv", "tvarchive", "tvnews", "movies_and_films", "vhsvault", "betamax",
    "musicandarts", "etree", "audio_music", "911_tv_archive", "artsandmusicvideos",
    "sillyfilms", "animationandcartoons_other", "moviesandfilms",
    # measured 2026-08-27: named rights holders whose uploads carry their own copyright
    "unicornriot-archive", "lost-telecourses", "mirrortube", "davidwoodarchive",
    "culturalandacademicfilms",
}

# Not a rights problem -- a channel problem. `deemphasize` is archive.org's own flag for
# material it does not want surfaced, and `fringe`/`offcenter`/`jan6archives` are conspiracy
# and insurrection footage. PD's standing rule is grow the channel and never get banned;
# none of this belongs in a documentary about American institutions regardless of licence.
UNSAFE_COLLECTIONS = {
    "deemphasize", "fringe", "offcenter", "jan6archives", "conspiracy",
}

# Municipal public-access recordings. The uploader IS the city, so the licence is set by the
# rights holder -- but a US municipality's work is not federal public domain, so this is not
# the same guarantee as usgovfilms. Kept separate so the decision is made once, in the open.
PUBLIC_ACCESS_COLLECTIONS = {
    "east-grand-forks-mn", "community_media", "channelalbany",
    "belmontcommunitymovingimagearchive",
}


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
            if r.get("reindex_basis") == "uploader_asserted_licenseurl":
                out.append(r)
    return out


def fetch(ident: str, cache: dict) -> dict:
    if ident in cache:
        return cache[ident]
    url = f"https://archive.org/metadata/{ident}"
    try:
        with urllib.request.urlopen(url, timeout=30) as fh:
            md = json.load(fh)
        meta = md.get("metadata", {}) or {}
        colls = meta.get("collection", [])
        colls = [colls] if isinstance(colls, str) else list(colls)
        rec = {"collection": [str(c).lower() for c in colls],
               "creator": str(meta.get("creator", "") or "")[:120],
               "mediatype": str(meta.get("mediatype", "") or ""),
               "licenseurl": str(meta.get("licenseurl", "") or "")}
    except Exception as exc:
        rec = {"error": str(exc)[:80]}
    cache[ident] = rec
    return rec


def classify(rec: dict) -> tuple[str, str]:
    if "error" in rec:
        return "eyes", "metadata unavailable: " + rec["error"]
    colls = set(rec.get("collection") or [])
    unsafe = colls & UNSAFE_COLLECTIONS
    if unsafe:
        return "unsafe", sorted(unsafe)[0]
    pay = colls & PAY_COLLECTIONS
    if pay:
        return "paywalled", sorted(pay)[0]
    pub = colls & PUBLIC_ACCESS_COLLECTIONS
    if pub:
        return "public_access", sorted(pub)[0]
    free = colls & FREE_COLLECTIONS
    if free:
        return "free", sorted(free)[0]
    return "eyes", ",".join(sorted(colls)[:3]) or "(no collection)"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", nargs=2, metavar=("BUCKET", "N"), default=None)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    CACHE.parent.mkdir(parents=True, exist_ok=True)
    cache = json.loads(CACHE.read_text("utf-8")) if CACHE.exists() else {}
    rows = held_rows()
    if args.limit:
        rows = rows[:args.limit]
    print(f"{len(rows)} held row(s); {len(cache)} already cached")

    buckets: dict[str, list] = collections.defaultdict(list)
    for i, r in enumerate(rows, 1):
        ident = r.get("id") or ""
        before = ident in cache
        rec = fetch(ident, cache)
        b, why = classify(rec)
        buckets[b].append({"id": ident, "title": r.get("title"), "theme": r.get("theme"),
                           "why": why, "file_path": r.get("file_path")})
        if not before:
            time.sleep(0.15)
            if i % 50 == 0:
                CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
                print(f"  {i}/{len(rows)} fetched")
    CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")

    verdicts = ROOT / "runs" / "ia_collection_verdicts.v001.json"
    verdicts.write_text(json.dumps(buckets, ensure_ascii=False, indent=1), encoding="utf-8")
    print()
    for b in ("free", "public_access", "paywalled", "unsafe", "eyes"):
        print(f"  {b:10s} {len(buckets[b]):4d}")
    print(f"\nwrote {verdicts.relative_to(ROOT)}")

    if args.show:
        b, n = args.show[0], int(args.show[1])
        seen = collections.Counter(x["why"] for x in buckets[b])
        for why, cnt in seen.most_common(20):
            print(f"  {cnt:4d}  {why[:70]}")
        print()
        for x in buckets[b][:n]:
            print(f"  [{x['why'][:26]:26s}] {(x['title'] or '')[:70]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
