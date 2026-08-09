#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""What the archive shelf can actually supply — the doc the design phase reads.

The shelf is filed by THEME, but a theme is the download query, not a subject, and a
query cannot match a case (commit a85f672d: "Select footage by subtype, not theme").
`weather_disasters` is 4,860 items of which 358 GB is one flood survey; `courtroom_justice`
holds Nuremberg reels next to a podcast talking head. So a shot spec written against
theme names asks for footage that does not exist, and the build then quietly falls back
to generic clips — EP21-24 failure (3): downloaded material that never reaches the cut.

This inventory indexes the shelf by SUBJECT, extracted from the sources' real titles,
and carries the owner's visual verdicts (`_qc\\archive_verdicts.jsonl`) so a killed
theme/source stops being offered. It is the counterpart to
FACTORY_SUBTYPE_INVENTORY.v001.md, which covers only the older factory shelf.

Usage:
    python scripts/build_archive_inventory.py
    python scripts/build_archive_inventory.py --min-count 5 --max-subjects 400
Output:
    episodes/_planning/ARCHIVE_SHELF_INVENTORY.v001.md
"""
from __future__ import annotations

import argparse
import collections
import datetime
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shelf import shelf_rows  # noqa: E402  the one definition of "on the shelf"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER_DIR = r"H:\pd-media\assets\archive\_ledger"
QC_DIR = r"H:\pd-media\assets\archive\_qc"
VERDICTS = os.path.join(QC_DIR, "archive_verdicts.jsonl")
ABSENT = os.path.join(LEDGER_DIR, "absent_index.json")

# Not stock. rejects/candidates were never taken; *_removed, purged and quarantine are
# records of things taken and then deleted, and a purge row repeats its source row's id,
# so counting the file adds the same item twice.
NOT_STOCK = ("purged.jsonl", "ban_risk_quarantine.jsonl", "shot_feedback.jsonl",
             "factory_rename.progress.jsonl", "factory.jsonl")
OUT = os.path.join(ROOT, "episodes", "_planning", "ARCHIVE_SHELF_INVENTORY.v001.md")

VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".mpeg", ".mpg", ".m4v"}
AUDIO_EXT = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".aif", ".aiff"}

# Words that carry no subject: grammar, archival boilerplate, and the container words
# every catalogue title repeats ("reel 3 of part 2, collection, no. 73").
STOP = set("""
a an the and or of in on at to for with from by into over under about as is are was were
be been being this that these those it its his her their our your my no not new
film films footage reel reels part parts no vol volume collection series program programs
copy print scene scenes shot shots view views image images photo photograph photographs
picture pictures video videos clip clips version full unknown untitled misc general
ca circa c19 c20 nd sd hd 4k 8k mm inch page pages plate plates sheet item items
digital transfer master edited unedited outtakes outtake raw stock library archive archives
wav mp3 mp4 aif aiff flac jpg jpeg tif tiff png rgb
taken showing shows showed various unidentified misc extra
```
""".split()) | {"", "-", "&"}

RE_WORD = re.compile(r"[a-z][a-z'\-]+")


def kind_of(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in VIDEO_EXT:
        return "video"
    if ext in AUDIO_EXT:
        return "audio"
    return "image"


def load_shelf() -> list[dict]:
    """The archive shelf, factory reported separately. Rule lives in shelf.py."""
    recs = list(shelf_rows(include_factory=False))
    print(f"  shelf {len(recs):,} rows")
    return recs


def load_verdicts() -> dict[tuple[str, str], dict]:
    """(theme, source) -> {verdict, note}. Absent file = nothing judged yet."""
    out: dict[tuple[str, str], dict] = {}
    if not os.path.exists(VERDICTS):
        return out
    with open(VERDICTS, encoding="utf-8", errors="replace") as fh:
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
                out[(r.get("theme", ""), r.get("source", ""))] = {
                    "verdict": v, "note": r.get("note", "")}
    return out


def phrases(title: str) -> list[str]:
    """Unigrams + bigrams of meaningful words. Bigrams first: ambiguity is per-word,
    so 'post office' and 'main street' identify a subject where 'post' and 'street'
    cannot (the ingest gate learned this the hard way — CONTRACT 4-v5-k)."""
    words = [w for w in RE_WORD.findall(title.lower()) if w not in STOP and len(w) > 2]
    out = [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]
    out += words
    return out


def md_escape(s: str) -> str:
    return s.replace("|", "/").replace("\n", " ").strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--min-count", type=int, default=6,
                    help="minimum items for a subject to be listed (default 6)")
    ap.add_argument("--max-subjects", type=int, default=350)
    args = ap.parse_args()

    recs = load_shelf()
    if not recs:
        print(f"no ledger rows in {LEDGER_DIR}")
        return 2
    verdicts = load_verdicts()

    # ---- theme x source supply table -------------------------------------------
    supply: dict[tuple[str, str], dict] = {}
    for r in recs:
        key = (r.get("theme") or "_unthemed", r.get("source") or "?")
        s = supply.setdefault(key, {"n": 0, "bytes": 0, "video": 0, "image": 0,
                                    "audio": 0, "titles": []})
        s["n"] += 1
        s["bytes"] += r.get("bytes", 0) or 0
        s[kind_of(r.get("file_path", ""))] += 1
        if len(s["titles"]) < 3:
            t = str(r.get("title", "")).strip()
            if t and t.lower() not in [x.lower() for x in s["titles"]]:
                s["titles"].append(t[:52])

    # ---- subject index ----------------------------------------------------------
    subj: dict[str, dict] = {}
    for r in recs:
        theme = r.get("theme") or "_unthemed"
        src = r.get("source") or "?"
        if verdicts.get((theme, src), {}).get("verdict") == "unusable":
            continue                      # a killed row is not supply
        fp = r.get("file_path", "")
        k = kind_of(fp)
        seen = set()
        for p in phrases(str(r.get("title", ""))):
            if p in seen:
                continue
            seen.add(p)
            e = subj.setdefault(p, {"n": 0, "video": 0, "image": 0, "audio": 0,
                                    "themes": collections.Counter(),
                                    "th_kind": collections.defaultdict(collections.Counter),
                                    "ex": collections.defaultdict(list)})
            e["n"] += 1
            e[k] += 1
            e["themes"][theme] += 1
            e["th_kind"][k][theme] += 1
            # Candidates are kept PER KIND. A shared pool filled up with freesound rows
            # and left video subjects ("water", "forest") illustrated by an .mp3 —
            # a table that cites the wrong medium is not a table anyone will trust.
            if len(e["ex"][k]) < 8:
                e["ex"][k].append((theme, fp))

    def example(e: dict, want_kind: str) -> str:
        cands = e["ex"].get(want_kind) or []
        if not cands:
            for k in ("video", "image", "audio"):
                if e["ex"].get(k):
                    cands = e["ex"][k]
                    break
        if not cands:
            return ""
        top = e["th_kind"][want_kind].most_common(1)
        if top:
            for t, fp in cands:
                if t == top[0][0]:
                    return fp
        return cands[0][1]

    def themes_of(e: dict, kind: str | None = None) -> str:
        c = e["th_kind"][kind] if kind else e["themes"]
        return ", ".join(f"{t}:{n}" for t, n in c.most_common(2))

    kept = sorted((p for p, e in subj.items() if e["n"] >= args.min_count),
                  key=lambda p: -subj[p]["n"])[:args.max_subjects]
    kept_video = sorted((p for p, e in subj.items() if e["video"] >= 3),
                        key=lambda p: -subj[p]["video"])[:args.max_subjects]

    total_gb = sum((r.get("bytes", 0) or 0) for r in recs) / 1e9
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        w = f.write
        w(f"# Archive shelf — what it can actually supply ({now})\n\n")
        w(f"{len(recs):,} items / {total_gb:,.0f} GB across {len({k[0] for k in supply})} "
          f"themes, {len({k[1] for k in supply})} sources.\n\n")
        w("**Read this before writing shot specs.** A theme name is the download query, "
          "not a subject — asking a shot spec for `weather_disasters` gets 358 GB of one "
          "flood survey. Search by SUBJECT (section 2), and only from rows section 1 "
          "marks `good`/`mixed`.\n\n")
        w("```\n"
          "python scripts/search_archive.py --shot \"courthouse exterior dusk\" --kind video\n"
          "python scripts/search_archive.py --shot \"prison corridor\" --md    # paste-ready rows\n"
          "python scripts/qc_archive_contact_sheets.py --theme <theme>          # look before you trust\n"
          "```\n\n")
        w("Filenames are `<source>__<id>__<title-slug>.<ext>` and 53,333/53,567 conform, "
          "but a name is NOT evidence: NOAA titles are survey codes and 27k NYPL scans all "
          "read `new-york-city-directory`. The verdicts below come from eyeballing the "
          "labeled sheets in `H:\\pd-media\\assets\\archive\\_qc\\<theme>\\`.\n\n")

        w("## 1. Supply and verdicts (theme x source)\n\n")
        if not verdicts:
            w("> No verdicts recorded yet — run the contact sheets, fill "
              "`_qc\\verdicts.template.jsonl`, save it as `_qc\\archive_verdicts.jsonl`. "
              "Until then every row is UNJUDGED and must not be trusted blind.\n\n")
        w("| theme | source | items | GB | video/image/audio | verdict | real titles |\n")
        w("|---|---|---:|---:|---|---|---|\n")
        for (theme, src), s in sorted(supply.items(), key=lambda kv: (kv[0][0], -kv[1]["n"])):
            v = verdicts.get((theme, src), {})
            vd = v.get("verdict", "—")
            note = f" ({md_escape(v['note'])})" if v.get("note") else ""
            w(f"| {theme} | {src} | {s['n']:,} | {s['bytes']/1e9:.1f} | "
              f"{s['video']}/{s['image']}/{s['audio']} | {vd}{note} | "
              f"{md_escape('; '.join(s['titles']))} |\n")

        # Footage first: the shelf holds 53k items but only ~4.8k are video, and a cut
        # starves for movement, not for stills (feedback_ken_burns_is_kamishibai — stills
        # with a zoom read as 紙芝居). So the design phase needs the video table first.
        w(f"\n## 2a. MOVING FOOTAGE by subject — {len(kept_video)} subjects with >= 3 clips\n\n")
        w("This is the scarce resource. Take stills only when no clip exists.\n\n")
        w("| subject | clips | top themes (clips only) | example clip |\n|---|---:|---|---|\n")
        for p in kept_video:
            e = subj[p]
            w(f"| {md_escape(p)} | {e['video']} | {md_escape(themes_of(e, 'video'))} | "
              f"`{md_escape(os.path.basename(example(e, 'video')))}` |\n")

        w(f"\n## 2b. Everything by subject — {len(kept)} subjects with >= {args.min_count} "
          "items\n\n")
        w("Search these words, not theme names. `themes` tells you which shelf folder "
          "holds them; `example` is a representative real file.\n\n")
        w("| subject | items | video | image | audio | top themes | example |\n")
        w("|---|---:|---:|---:|---:|---|---|\n")
        for p in kept:
            e = subj[p]
            dom = max(("video", e["video"]), ("image", e["image"]), ("audio", e["audio"]),
                      key=lambda kv: kv[1])[0]
            w(f"| {md_escape(p)} | {e['n']:,} | {e['video']} | {e['image']} | {e['audio']} | "
              f"{md_escape(themes_of(e))} | `{md_escape(os.path.basename(example(e, dom)))}` |\n")

        w("\n## 3. Known name-vs-content traps\n\n")
        w("| source | trap |\n|---|---|\n")
        w("| noaa | Titles are survey codes (`20260130aC0894545w340345n`). "
          "Nothing about the frame is knowable from the name — must be eyeballed. |\n")
        w("| nypl | 27k scans share the title `new-york-city-directory`; the subject index "
          "cannot separate them. Treat as page scans, not footage. |\n")
        w("| ia | Real titles, but talking-head lectures/podcasts pass the relevance gate "
          "(measured 4/24 on the courtroom_justice sheet). Check before staging. |\n")
        w("| factory (older shelf) | Filenames are the SEARCH QUERY, verified ~50% wrong. "
          "Use `select_factory_assets.py` + FACTORY_SUBTYPE_INVENTORY.v001.md, never the name. |\n")
    print(f"wrote {OUT}")
    print(f"  {len(recs):,} items, {len(supply)} theme x source rows, "
          f"{len(kept)} subjects, {len(verdicts)} verdicts applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
