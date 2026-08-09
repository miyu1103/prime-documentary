# -*- coding: utf-8 -*-
"""
Search the PD archive shelf across ALL ingest ledgers (every agent/source) in seconds.

Queries the centralized rights ledger H:\\pd-media\\assets\\archive\\_ledger\\*.jsonl
(contract: CONTRACT.md in the same folder) by free-text keywords + optional filters,
printing file path, title, license and theme for each hit.

Usage:
  python scripts/search_archive.py courtroom 1950s --theme courtroom_justice
  python scripts/search_archive.py "post office" --source ia --license pd
  python scripts/search_archive.py train --kind video --limit 50
  python scripts/search_archive.py --theme japan --stats
"""
from __future__ import annotations

import argparse
import json
import re
import os
import time
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEDGER_DIR = r"H:\pd-media\assets\archive\_ledger"
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".mpeg", ".mpg"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".webp"}
AUDIO_EXT = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"}


QC_DIR = r"H:\pd-media\assets\archive\_qc"
VERDICT_FILE = os.path.join(QC_DIR, "archive_verdicts.jsonl")

# Titles that pass the relevance gate but are a person talking to camera, not a picture.
# Measured on the courtroom_justice contact sheet: 4 of 24 sampled items (a podcast, a
# Daubert lecture, "Court to Court", "Justice At All Costs") — 387 MB of talking head
# that would land in a cut as a dead shot.
TALKING_HEAD = ("podcast", "lecture", "webinar", "interview", "seminar", "symposium",
                "conference", "panel discussion", "presentation", "vlog", "livestream",
                "live stream", "sermon", "keynote", "testimonial", "extended version",
                "full episode", "episode ")
RE_TERM = "{}(?:s|es|'s|s')?"


# Words too common to identify a subject on their own. A query term from this set can
# add weight, but it can never be the ONLY reason a result is offered — that is how
# "county courthouse exterior" surfaced a suburban house (it matched "exterior").
# Mirrors the ingest gate's relevance-v5 weak-only cap (CONTRACT 4-v5-j).
WEAK_TERMS = {
    "exterior", "interior", "building", "buildings", "view", "views", "city", "street",
    "night", "day", "close", "shot", "scene", "man", "woman", "men", "women", "people",
    "person", "old", "new", "american", "america", "house", "home", "room", "light",
    "dark", "water", "sky", "road", "car", "time", "place", "work", "hand", "hands",
    "front", "back", "side", "top", "video", "footage", "background", "modern",
    "historic", "large", "small", "long", "short", "white", "black", "red", "blue",
}
FEEDBACK = os.path.join(LEDGER_DIR, "shot_feedback.jsonl")
LAST_QUERY = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runs", "qc",
    "_last_shot_query.json")


def load_feedback() -> dict:
    """`source:id` -> net score adjustment from earlier picks and rejections."""
    adj: dict = {}
    if not os.path.exists(FEEDBACK):
        return adj
    with open(FEEDBACK, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            key = f"{r.get('source')}:{r.get('id')}"
            adj[key] = adj.get(key, 0) + (15 if r.get("verdict") == "pick" else -25)
    return adj


VIDEO_RES = os.path.join(LEDGER_DIR, "video_resolution.json")
_VRES: dict | None = None


def load_video_resolution() -> dict:
    """(source:id) -> {w, h} for shelf video, from build_video_resolution_index.py.

    The ledgers carry no width or height for any of the 31,156 videos, so nothing could
    tell 4K from 320x240 -- and 1,770 of the 2,280 archival videos are below 720p. A shot
    spec written without this cites SD footage by accident."""
    global _VRES
    if _VRES is None:
        try:
            with open(VIDEO_RES, encoding="utf-8", errors="replace") as fh:
                _VRES = json.load(fh)
        except OSError:
            _VRES = {}
    return _VRES


def apply_feedback(raw: int, key: str, feedback: dict) -> int:
    """Re-rank a candidate by earlier picks — but only one that is already a candidate.

    The bonus was being added to the raw score unconditionally, and a pick is recorded
    against the shot it was made for. Four clips picked once for "prison cell block
    corridor" were therefore scoring 15 on every shot ever run, and topped the results for
    "bank branch interior counter", "foreclosure sign house" and "checkout till transaction"
    — three shots whose raw score for them is 0.

    A pick says "this was the right choice among relevant results", never "this is relevant
    to everything". So feedback moves a candidate up or down; it cannot create or destroy
    relevance that the words do not support."""
    if raw <= 0:
        return raw
    return raw + feedback.get(key, 0)


DF_CACHE = os.path.join(LEDGER_DIR, "title_df.json")
DF_MAX_AGE = 24 * 3600
_DF: dict = {}
_DF_TOTAL = 0


def load_df() -> tuple[dict, int]:
    """word -> how many shelf titles contain it. Cached; rebuilt when a day old.

    This is what tells "vault" apart from "door" without anyone maintaining a list.
    """
    global _DF, _DF_TOTAL
    if _DF:
        return _DF, _DF_TOTAL
    fresh = (os.path.exists(DF_CACHE)
             and (time.time() - os.path.getmtime(DF_CACHE)) < DF_MAX_AGE)
    if fresh:
        try:
            blob = json.load(open(DF_CACHE, encoding="utf-8"))
            _DF, _DF_TOTAL = blob["df"], blob["total"]
            return _DF, _DF_TOTAL
        except Exception:
            pass
    df: dict = {}
    total = 0
    for fn in sorted(os.listdir(LEDGER_DIR)):
        if not fn.endswith(".jsonl") or fn.startswith("rejects") or fn.endswith(
                ("_dedup_removed.jsonl", "_candidates.jsonl")):
            continue
        with open(os.path.join(LEDGER_DIR, fn), encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                total += 1
                for w in set(re.findall(r"[a-z][a-z'\-]+", str(rec.get("title", "")).lower())):
                    df[w] = df.get(w, 0) + 1
    _DF, _DF_TOTAL = df, max(total, 1)
    try:
        with open(DF_CACHE, "w", encoding="utf-8") as fh:
            json.dump({"df": df, "total": _DF_TOTAL}, fh)
    except OSError:
        pass
    return _DF, _DF_TOTAL


def is_common(word: str) -> bool:
    """True when the word is too widespread on this shelf to identify anything."""
    df, total = load_df()
    return df.get(word, 0) > total * 0.004      # ~400 of 100,000 titles


def kind_of(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in VIDEO_EXT:
        return "video"
    if ext in IMAGE_EXT:
        return "image"
    if ext in AUDIO_EXT:
        return "audio"
    return "other"


def load_verdicts() -> dict:
    """(theme, source) -> verdict, from the owner's eyeball pass on the contact sheets.

    Filenames and relevance scores cannot tell an on-topic clip from an off-topic one
    (pd-factory-shelf-mislabeled). A human verdict can, so once it exists it outranks
    every machine signal here: `unusable` rows are not offered at all.
    """
    out = {}
    if not os.path.exists(VERDICT_FILE):
        return out
    with open(VERDICT_FILE, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            v = (r.get("verdict") or "").strip().lower()
            if v:
                out[(r.get("theme", ""), r.get("source", ""))] = v
    return out


def load_quarantined() -> set:
    """`source:id` of everything quarantine_ban_risk.py pulled off the shelf.

    The source ledgers are append-only and written by live ingest lanes, so a
    quarantined row is still in them. Without this the search would keep offering an
    extremist speech or a news broadcast by its old path — and a builder that resolves
    paths loosely could still stage it.
    """
    path = os.path.join(LEDGER_DIR, "ban_risk_quarantine.jsonl")
    out = set()
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            key = f"{r.get('source')}:{r.get('id')}"
            if r.get("action") == "quarantine":
                out.add(key)
            elif r.get("action") == "undo":
                out.discard(key)
    return out


def shot_score(rec: dict, words: list[str], bigrams: list[str], people_filter: bool) -> int:
    """Rank a ledger row against a shot description.

    Bigrams weigh more than words because ambiguity is per-word, not per-phrase:
    "post office" and "main street" name a subject that "post" and "street" cannot
    (the ingest gate's relevance-v5 lesson, CONTRACT 4-v5-k).
    """
    title = str(rec.get("title", "")).lower()
    extra = " ".join([str(rec.get("theme", "")),
                      " ".join(rec.get("matched_keywords", []) or []),
                      os.path.basename(rec.get("file_path", ""))]).lower()
    # The query's rarest word is its anchor. Everything else is corroboration.
    rare = [w for w in words if not is_common(w) and w not in WEAK_TERMS]
    anchor_hit = False
    anchor_terms = 0          # how many distinctive query words landed in the title
    phrase_hit = False        # a distinctive two-word phrase landed in the title
    score = 0
    for b in bigrams:
        b_rare = any(not is_common(w) and w not in WEAK_TERMS for w in b.split())
        if b in title:
            score += 30 if b_rare else 8
            if b_rare:
                anchor_hit = True
                phrase_hit = True
        elif b in extra:
            score += 10 if b_rare else 3
    for wd in words:
        pat = RE_TERM.format(re.escape(wd))
        common = is_common(wd) or wd in WEAK_TERMS
        if re.search(rf"\b{pat}\b", title):
            score += 5 if common else 12
            if not common:
                anchor_hit = True
                anchor_terms += 1
        elif re.search(rf"\b{pat}\b", extra):
            score += 2 if common else 4
    # One distinctive word is not enough. Rarity on this shelf does not mean the word
    # names a subject: "closing" appears in only 96 of 189,498 titles purely because the
    # catalogue is written in nouns, so it read as distinctive and let a garage door win
    # a bank-vault search. Demand that TWO of the query's distinctive words show up, or
    # one plus a distinctive phrase -- a coincidence has to happen twice.
    if len(rare) >= 2 and anchor_terms < 2 and not phrase_hit:
        score = min(score, 10)
    elif len(rare) == 1 and not anchor_hit:
        score = min(score, 10)
    if score and people_filter and any(t in title for t in TALKING_HEAD):
        score -= 40
    return score


def record_feedback(pick: str | None, reject: str | None) -> int:
    """Attach a human verdict to the previous --shot result set.

    Indices refer to the numbered list that --shot printed, which is stashed in
    LAST_QUERY. This is the only signal in the whole system that comes from someone
    actually looking, so it outranks the computed score on the next run.
    """
    if not os.path.exists(LAST_QUERY):
        print("no previous --shot query to annotate")
        return 2
    prev = json.load(open(LAST_QUERY, encoding="utf-8"))
    rows = prev.get("rows", [])

    def idxs(spec):
        out = []
        for part in (spec or "").split(","):
            part = part.strip()
            if part.isdigit() and 1 <= int(part) <= len(rows):
                out.append(int(part) - 1)
        return out

    n = 0
    for verdict, spec in (("pick", pick), ("reject", reject)):
        for i in idxs(spec):
            r = rows[i]
            line = json.dumps({"verdict": verdict, "shot": prev.get("shot"),
                               "source": r.get("source"), "id": r.get("id"),
                               "title": r.get("title"), "path": r.get("path")},
                              ensure_ascii=False) + "\n"
            fd = os.open(FEEDBACK, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
            try:
                os.write(fd, line.encode("utf-8"))
            finally:
                os.close(fd)
            n += 1
            print(f"  {verdict:6} #{i+1} {str(r.get('title'))[:60]}")
    print(f"recorded {n} verdict(s) -> {FEEDBACK}")
    print("these now outrank the computed score for those items")
    return 0


def build_sheet(rows, shot: str) -> None:
    """Hand the results to the existing contact-sheet builder rather than drawing a
    second one (CLAUDE invariant 14: extend the existing path, do not clone it)."""
    import subprocess
    # The title becomes a FILENAME downstream. An unsanitised one ("shot: prison cell
    # block corridor") made Windows write the PNG into an NTFS alternate data stream on
    # a 0-byte file called "shot" — the builder reported success and the image was
    # unreachable. Slug it here, and pin the output path explicitly.
    safe = re.sub(r"[^A-Za-z0-9]+", "_", shot).strip("_").lower()[:48] or "shot"
    sel = {"title": f"shot_{safe}",
           "items": [{"path": r["path"],
                      "label": f"#{i+1} s{r['score']} {r['source']} | {str(r['title'])[:44]}"}
                     for i, r in enumerate(rows)]}
    os.makedirs(os.path.dirname(LAST_QUERY), exist_ok=True)
    sel_path = os.path.join(os.path.dirname(LAST_QUERY), "_shot_selection.json")
    with open(sel_path, "w", encoding="utf-8") as fh:
        json.dump(sel, fh, ensure_ascii=False, indent=1)
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "build_footage_contact_sheet.py")
    print(f"\nbuilding contact sheet for {len(rows)} candidates ...")
    out_png = os.path.join(os.path.dirname(LAST_QUERY), f"shot_{safe}_contact.png")
    p = subprocess.run([sys.executable, script, "--from-json", sel_path, "--out", out_png],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(p.stdout.strip() or p.stderr.strip()[:400])
    if os.path.exists(out_png):
        print(f"  verified on disk: {out_png} ({os.path.getsize(out_png)/1024:.0f} KB)")
    else:
        print(f"  WARNING: builder reported success but {out_png} is not on disk")


def main() -> int:
    ap = argparse.ArgumentParser(description="Search PD archive ledgers")
    ap.add_argument("keywords", nargs="*", help="free-text terms (ANDed, case-insensitive; "
                    "matched against title, id, matched_keywords, theme, filename)")
    ap.add_argument("--theme", help="exact theme filter")
    ap.add_argument("--source", help="source filter (ia, loc, nasa, wikimedia, ...)")
    ap.add_argument("--license", dest="license_", help="pd | cc0 | free_commercial | review_required")
    ap.add_argument("--kind", choices=["video", "image", "audio"], help="media kind by extension")
    ap.add_argument("--missing", action="store_true", help="only rows whose file is missing on disk")
    ap.add_argument("--limit", type=int, default=30, help="max rows printed (default 30)")
    ap.add_argument("--paths-only", action="store_true", help="print file paths only (pipeable)")
    ap.add_argument("--stats", action="store_true", help="print per-theme/source/license counts only")
    ap.add_argument("--shot", help="shot description, ranked instead of ANDed "
                    '(e.g. --shot "courthouse exterior dusk"). Use this when writing '
                    "shot specs: it scores titles, drops talking heads and rows the "
                    "owner marked unusable, and only offers files that exist on disk")
    ap.add_argument("--md", action="store_true",
                    help="print markdown table rows, ready to paste into a design doc")
    ap.add_argument("--include-unusable", action="store_true",
                    help="also offer theme/source rows the owner marked unusable")
    ap.add_argument("--include-quarantined", action="store_true",
                    help="also offer files sitting in _quarantine (pending owner review)")
    ap.add_argument("--keep-talking-heads", action="store_true",
                    help="disable the podcast/lecture/interview penalty in --shot")
    ap.add_argument("--sheet", action="store_true",
                    help="build a labeled contact sheet of the results so they can be "
                         "eyeballed before anything is written into a shot spec")
    ap.add_argument("--weak-ok", action="store_true",
                    help="do not cap results that matched only common words")
    ap.add_argument("--pick", help="comma indices from the last --shot result to mark KEPT")
    ap.add_argument("--reject", help="comma indices from the last --shot result to mark REJECTED")
    args = ap.parse_args()

    if not os.path.isdir(LEDGER_DIR):
        print(f"no ledger dir: {LEDGER_DIR}")
        return 2

    if args.pick or args.reject:
        return record_feedback(args.pick, args.reject)
    terms = [t.lower() for t in args.keywords]
    verdicts = load_verdicts()
    quarantined = load_quarantined()
    feedback = load_feedback()
    shot_words: list[str] = []
    shot_bigrams: list[str] = []
    if args.shot:
        toks = [w for w in re.findall(r"[a-z][a-z'\-]+", args.shot.lower()) if len(w) > 2]
        shot_words = toks
        shot_bigrams = [f"{toks[i]} {toks[i+1]}" for i in range(len(toks) - 1)]
    hits = []
    stats: dict[str, int] = {}
    skipped_unusable = 0
    skipped_quarantined = 0
    skipped_in_quarantine = 0
    for fn in sorted(os.listdir(LEDGER_DIR)):
        if not fn.endswith(".jsonl") or fn.startswith("rejects") or fn.endswith(
                ("_dedup_removed.jsonl", "_candidates.jsonl")):
            continue
        if args.source and fn != f"{args.source.lower()}.jsonl":
            continue
        with open(os.path.join(LEDGER_DIR, fn), encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if args.theme and rec.get("theme") != args.theme:
                    continue
                if args.license_ and rec.get("license_decision") != args.license_:
                    continue
                fp = rec.get("file_path", "")
                if args.kind and kind_of(fp) != args.kind:
                    continue
                if args.missing and os.path.exists(fp):
                    continue
                if f"{rec.get('source')}:{rec.get('id')}" in quarantined:
                    skipped_quarantined += 1
                    continue
                # Anything sitting in _quarantine is awaiting owner review and is not
                # supply. Found the hard way: a search for "holocaust trial" returned a
                # Zündel-trial recording that the ingest lane had quarantined for being
                # sub-SD — the file was off the shelf but the search still offered it.
                if not args.include_quarantined and "_quarantine" in fp.lower():
                    skipped_in_quarantine += 1
                    continue
                if not args.include_unusable and verdicts.get(
                        (rec.get("theme", ""), rec.get("source", ""))) == "unusable":
                    skipped_unusable += 1
                    continue
                if args.shot:
                    sc = shot_score(rec, shot_words, shot_bigrams,
                                    not args.keep_talking_heads)
                    sc = apply_feedback(
                        sc, f"{rec.get('source')}:{rec.get('id')}", feedback)
                    floor = 0 if args.weak_ok else 15
                    if sc <= floor:
                        continue
                    # Score BEFORE stat(): existence-checking all ~142k rows first meant
                    # 142k stat calls across four drives while the ingest lanes are
                    # writing, and the query took minutes. Scoring is free by comparison
                    # and leaves only a few hundred rows to verify.
                    # A shot spec that cites a missing file produces a silent fallback to
                    # generic footage later (EP21-24 failure 3), so unverifiable rows are
                    # not candidates at all.
                    if not os.path.exists(fp):
                        continue
                    hits.append(dict(rec, _score=sc))
                    continue
                blob = " ".join([str(rec.get("title", "")), str(rec.get("id", "")),
                                 " ".join(rec.get("matched_keywords", []) or []),
                                 rec.get("theme", ""), os.path.basename(fp)]).lower()
                if all(t in blob for t in terms):
                    hits.append(rec)
                    for k in (f"theme:{rec.get('theme')}", f"source:{rec.get('source')}",
                              f"license:{rec.get('license_decision')}",
                              f"kind:{kind_of(fp)}"):
                        stats[k] = stats.get(k, 0) + 1
    if args.stats:
        print(f"{len(hits)} matching items")
        for k in sorted(stats):
            print(f"  {k:42} {stats[k]}")
        return 0
    if args.shot:
        hits.sort(key=lambda r: -r.get("_score", 0))
    if args.md:
        shown = hits[:args.limit]
        print("| score | subject (real title) | source | kind | license | path |")
        print("|---:|---|---|---|---|---|")
        for rec in shown:
            fp = rec.get("file_path", "")
            title = str(rec.get("title", "")).replace("|", "/")[:60]
            print(f"| {rec.get('_score', '-')} | {title} | {rec.get('source')} | "
                  f"{kind_of(fp)} | {rec.get('license_decision')} | `{fp}` |")
        # The source column is not decoration: a pexels/pixabay row comes off the older
        # factory shelf, whose filenames are the search query and measured ~50% wrong.
        # Those need an eyeball before they enter a shot spec; archive rows carry the
        # source's own title.
        if any(r.get("source") in ("pexels", "pixabay", "factory") for r in shown):
            print("\n> Rows from pexels/pixabay come off the factory shelf — the label is "
                  "the download query, verified ~50% wrong. Eyeball before staging.")
        print(f"\n<!-- {len(hits)} candidates on the shelf"
              + (f"; {skipped_unusable} rows skipped as owner-marked unusable"
                 if skipped_unusable else "") + " -->")
        return 0
    if args.shot:
        shown = hits[:args.limit]
        rows = [{"n": i + 1, "score": r.get("_score"), "source": r.get("source"),
                 "id": r.get("id"), "title": r.get("title"),
                 "path": r.get("file_path", "")} for i, r in enumerate(shown)]
        os.makedirs(os.path.dirname(LAST_QUERY), exist_ok=True)
        with open(LAST_QUERY, "w", encoding="utf-8") as fh:
            json.dump({"shot": args.shot, "rows": rows}, fh, ensure_ascii=False, indent=1)
        vres = load_video_resolution()
        sd_offered = 0
        for r in rows:
            wh = vres.get(f"{r['source']}:{r['id']}")
            tag = ""
            if wh:
                tag = f"  [{wh['w']}x{wh['h']}]"
                if wh["h"] < 720:
                    tag += " SD"
                    sd_offered += 1
            print(f"[{r['n']:2d}] s{r['score']:>3} {r['source']:>9} | "
                  f"{str(r['title'])[:62]}{tag}")
            print(f"      {r['path']}")
        if sd_offered:
            print(f"  ! {sd_offered} of these are below 720p — 1,770 of the 2,280 archival "
                  f"videos are, and an SD insert in a 1080p cut is visible to the viewer")
        print(f"-- {len(hits)} hits"
              + (f"; {skipped_quarantined} ban-risk" if skipped_quarantined else "")
              + (f"; {skipped_in_quarantine} in _quarantine" if skipped_in_quarantine else "")
              + (f"; {skipped_unusable} owner-marked-unusable" if skipped_unusable else "")
              + " withheld")
        if args.sheet:
            build_sheet(rows, args.shot)
        print("\nafter looking: "
              "python scripts/search_archive.py --pick 1,3 --reject 2,4")
        return 0
    for rec in hits[:args.limit]:
        if args.paths_only:
            print(rec.get("file_path", ""))
        else:
            mb = rec.get("bytes", 0) / 1e6
            print(f"[{rec.get('source'):>9}|{rec.get('license_decision'):>15}|"
                  f"{rec.get('theme', ''):22}|{mb:7.1f}MB] {str(rec.get('title', ''))[:60]}")
            print(f"    {rec.get('file_path', '')}")
    print(f"-- {len(hits)} hits total"
          + (f", showing first {args.limit}" if len(hits) > args.limit else "")
          + (f"; {skipped_quarantined} ban-risk row(s) withheld" if skipped_quarantined else "")
          + (f"; {skipped_in_quarantine} row(s) in _quarantine awaiting review"
             if skipped_in_quarantine else "")
          + (f"; {skipped_unusable} owner-marked-unusable row(s) withheld"
             if skipped_unusable else ""))
    if args.sheet:
        # --sheet used to be reachable only through --shot. That is the phrase-search path,
        # and it is the one measured to undercount badly (`underground parking garage` -> 3
        # hits where plain `garage` -> 45). So the only selection you could actually look at
        # was the one you are told not to select from. Keyword results get a sheet too.
        label = " ".join(args.keywords) or args.theme or args.query or "archive"
        rows = [{"score": 0, "source": r.get("source", ""), "title": r.get("title", ""),
                 "path": r.get("file_path", "")} for r in hits[:args.limit]]
        rows = [r for r in rows if r["path"]]
        if rows:
            build_sheet(rows, label)
        else:
            print("no rows with a path; no sheet built")
    return 0


if __name__ == "__main__":
    sys.exit(main())
