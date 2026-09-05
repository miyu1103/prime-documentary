#!/usr/bin/env python3
"""Emit one design skeleton per public long-form, pre-filled with everything that can be MEASURED,
so the only work left on each is the creative part: the angle, the five spoken lines, and the
twenty-three shot motifs.

Everything below is filled from disk or from the channel — never assumed:
  * the destination long-form (id / title / privacy), refusing anything not public
  * how many more Shorts this episode needs to reach 3
  * what the EXISTING Short(s) already said, quoted verbatim from their caption tracks, so a new
    angle can be checked against them instead of guessed at
  * candidate lines from the episode's own verified script that carry a "surprise payload"
    (a number, an absolute, or a quotation) — the raw material for angles
  * archive footage that actually survives a 9:16 centre crop, from the vertical index
  * the era, which decides whether modern stock footage is usable at all

Usage: py -3.11 scripts/build_short_design_skeletons.py [--only PD-2026-016-titan]
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "episodes" / "_planning" / "short_designs"
DATA = ROOT / "remotion" / "src" / "data"
INDEX = Path(r"E:\pd-media\assets\archive\_qc\vertical_index.jsonl")

NUM = re.compile(r"(\$[\d,.]+|\b\d[\d,]*(?:\.\d+)?\s?(?:percent|%|years?|months?|days?|hours?|"
                 r"minutes?|dollars?|million|billion|thousand|times|cases?|people|convictions?)\b|\b\d{3,}\b)", re.I)
ABS = re.compile(r"\b(never|no one|nobody|not a single|zero|none of|no evidence|no warrant|"
                 r"no charges|without a warrant|to this day|has never)\b", re.I)
QUO = re.compile(r"[\u201c\"][^\u201d\"]{25,200}[\u201d\"]")


def latest(paths):
    p = sorted(paths)
    return p[-1] if p else None


def episode_script(ep: str) -> Path | None:
    d = ROOT / "episodes" / ep / "03_script"
    p = latest(d.glob("script.en.v*.md")) if d.exists() else None
    if p:
        return p
    n = int(ep.split("-")[2]); slug = ep.split("-", 3)[3]
    return latest((ROOT / "episodes" / "_planning").glob(f"EP{n}_{slug}_script.en.v*.md"))


def strip_apparatus(text: str) -> str:
    """Remove everything that is production instruction rather than spoken narration.

    The scripts interleave shot notes, claim tags and QC blocks with the VO, e.g.
    "[SHOT: T-IMG-039 the twilight zone] [VO:] It is worth understanding the place [CLM-0006]".
    Left in, they poison the candidate lines a design is authored from - the first skeleton pass
    surfaced three HTML comments and a shot list as "payload lines".
    """
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)          # html comments
    text = re.sub(r"\u3010.*?\u3011", " ", text, flags=re.S)      # 【 production notes 】
    text = re.sub(r"\u3014.*?\u3015", " ", text, flags=re.S)      # 〔 cards 〕
    text = re.sub(r"\((?:VIS|SFX|ANCHOR|OST|CARD|SILENCE)[^)]*\)", " ", text, flags=re.I)
    text = re.sub(r"\[(?:SHOT|CLM|VO|OST|CARD|TITLE|SILENCE|beat)[^\]]*\]", " ", text, flags=re.I)
    text = re.sub(r"\[[A-Z0-9\-\u2013 ,.:]{0,40}\]", " ", text)   # leftover bracket tags
    return text


def sentences(text: str):
    text = re.sub(r"\s+", " ", strip_apparatus(text))
    out = []
    for s in re.split(r"(?<=[.!?])\s+", text):
        s = s.strip()
        if not (40 < len(s) < 260):
            continue
        if re.search(r"[\[\]\u3010\u3011<>]|IMG-|WORD COUNT|check_script|PASS:|BLOCKER", s):
            continue
        # Scripts end with a self-check / revision log written in the same plain prose as the
        # narration, e.g. "Kept the day-count as six days across two facilities (claim 11)."
        # Those are editorial notes about the film, not lines from it, and they were surfacing
        # as candidate angles for EP37.
        if re.match(r"^(Kept|Added|Dropped|Replaced|Verified|Tightened|Removed|Reworked|Cut|"
                    r"Retained|Moved|Renamed|Swapped|Fixed|Confirmed|Checked|Pass \d)\b", s):
            continue
        if re.search(r"\b(claim \d|sensitivity R\d|Draft [AB]\b|cadence|per-facility|"
                     r"BLOCKER|verbatim quote|self-check)\b", s, re.I):
            continue
        if sum(ch.isascii() for ch in s) / max(1, len(s)) < 0.9:   # drop Japanese QC prose
            continue
        out.append(s)
    return out


def candidate_lines(path: Path, k: int = 18):
    raw = path.read_text(encoding="utf-8", errors="replace")
    # EP42 writes its narration as markdown blockquotes, so dropping ">" lines dropped the
    # entire script and that design came back with zero candidate lines. Strip the marker,
    # keep the line.
    keep = []
    for _l in raw.splitlines():
        s = _l.strip()
        if s.startswith(("#", "|", "-", "*", "`", "【", "〔")):
            continue
        keep.append(s.lstrip("> ").strip() if s.startswith(">") else s)
    body = "\n".join(keep)
    hits = []
    for s in sentences(body):
        sc = (2 if NUM.search(s) else 0) + (2 if ABS.search(s) else 0) + (3 if QUO.search(s) else 0)
        if sc >= 2:
            hits.append((sc, s))
    hits.sort(key=lambda x: -x[0])
    out, seen = [], set()
    for sc, s in hits:
        key = s[:60].lower()
        if key in seen:
            continue
        seen.add(key); out.append(s)
        if len(out) >= k:
            break
    return out


def existing_short_captions(short_id: str) -> list[str]:
    f = DATA / f"{short_id}_timing.ts"
    if not f.exists():
        return []
    t = f.read_text(encoding="utf-8", errors="replace")
    key = [k for k in re.findall(r"(SHORT\w+_CAPTIONS)", t)]
    if not key:
        return []
    i = t.index(key[0]); j = t.index("[", t.index("=", i)); d = 0
    for m in range(j, len(t)):
        d += (t[m] == "[") - (t[m] == "]")
        if d == 0:
            try:
                return [c["word"] for c in json.loads(t[j:m + 1])]
            except Exception:
                return []
    return []


def footage_pool(theme_hint: str, n: int = 14):
    if not INDEX.exists():
        return []
    rows = []
    for line in INDEX.open(encoding="utf-8"):
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r["centre_energy"] < 0.40 or r["motion"] < 0.8 or not (28 <= r["luma_crop"] <= 200):
            continue
        if r.get("title") in (None, "id"):     # ~half the ledger has a broken title
            continue
        rows.append(r)
    rows.sort(key=lambda r: -r["centre_energy"])
    return rows[:n]


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--only"); args = ap.parse_args()
    backup = latest((ROOT / "runs" / "short_funnel").glob("metadata_backup.*.json"))
    if not backup:
        raise SystemExit("run scripts/backup_short_metadata.py first")
    rows = json.loads(backup.read_text(encoding="utf-8"))
    # Accept a long-form that is scheduled but not yet public. The Short can be built now and
    # its funnel link attaches the day the destination goes live (daily_funnel_sync.py).
    # schedule_short_youtube.py still refuses to UPLOAD against a non-public destination, so
    # nothing can ship pointing at a video nobody can watch - that guard stays where it is.
    pub_long = [r for r in rows
                if r["duration_sec"] > 185
                and (r["privacy"] == "public" or r.get("publishAt"))]

    shorts_by_ep = defaultdict(list)
    for f in sorted(DATA.glob("short*.ts")):
        if f.name.endswith("_timing.ts"):
            continue
        m = re.search(r"episodeId:\s*'([^']+)'", f.read_text("utf-8", errors="replace"))
        if m:
            shorts_by_ep[m.group(1)].append(f.stem)

    ep_of = {}
    for ep_dir in sorted((ROOT / "episodes").glob("PD-2026-*")):
        for j in ep_dir.rglob("*.json"):
            if "short" in j.name.lower():
                continue
            try:
                txt = j.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for r in pub_long:
                if r["id"] in txt:
                    ep_of.setdefault(r["id"], ep_dir.name)

    OUT.mkdir(parents=True, exist_ok=True)
    pool = []   # obsolete: see bind_short_footage_semantic.py
    made = 0
    for r in sorted(pub_long, key=lambda a: -a["views"]):
        ep = ep_of.get(r["id"])
        if not ep or (args.only and ep != args.only):
            continue
        have = sorted(shorts_by_ep.get(ep, []))
        need = max(0, 3 - len(have))
        if not need:
            continue
        sc = episode_script(ep)
        doc = {
            "episode_id": ep,
            "slug": ep.split("-", 3)[3],
            "status": "SKELETON — angles and line plans not yet authored",
            "destination": {"video_id": r["id"], "title": r["title"],
                            "url": f"https://www.youtube.com/watch?v={r['id']}",
                            "privacy": r["privacy"], "views": r["views"]},
            "shorts_existing": have,
            "shorts_to_author": need,
            "existing_angles_do_not_repeat": {s: existing_short_captions(s) for s in have},
            "script": str(sc.relative_to(ROOT)) if sc else None,
            "candidate_payload_lines": candidate_lines(sc) if sc else [],
            "era_note": "SET THIS. Modern stock footage is only usable if the case is modern; a "
                        "1960s case dressed in present-day footage reads wrong.",
            "footage_candidates_crop_safe": [
                {"title": p["title"], "file": p["file_path"], "centre_energy": p["centre_energy"],
                 "motion": p["motion"], "luma": p.get("luma_crop")} for p in pool],
            "shorts": [{"short_id": None, "angle": None, "funnel_question_left_for_longform": None,
                        "lines": [{"id": f"L{i}", "delivery": d, "text": None, "claims": []}
                                  for i, d in enumerate(["intense", "building", "building",
                                                         "intense", "calm"], start=1)],
                        "plates": [{"n": i, "role": None, "subject": None,
                                    "source": "FOOTAGE|GENERATE", "prompt": None}
                                   for i in range(1, 24)]}
                       for _ in range(need)],
        }
        (OUT / f"{ep}.design.v001.json").write_text(
            json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        made += 1
    print(f"wrote {made} design skeletons -> {OUT.relative_to(ROOT)}")
    print("footage is bound at build time by bind_short_footage_semantic.py, not here")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
