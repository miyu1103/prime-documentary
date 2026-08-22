#!/usr/bin/env python3
r"""Re-download the stock clips that died with the H: drive, by id, into the live shelf.

WHAT HAPPENED. `D:\\pd-media-browse` holds symlinks whose targets are all under
`H:\\pd-media\\assets\\factory\\...`. H: is dead, so every one of those files is gone. Measured
2026-08-22: `Length 0, Attributes ReparsePoint, Target ... exists: False`.

WHY THIS IS RECOVERABLE. Each symlink is named `<source>__<id>__<slug>.mp4`. The id is the
provider's media id, both API keys are in `.env`, and both licences permit commercial use. So the
browse tree is not a record of a loss -- it is a shopping list.

WHAT IS ACTUALLY MISSING (measured 2026-08-22, unique ids, checked against the ledger):

    pexels  video   9,376 ids   1,434 already on the shelf   7,942 to fetch
    pixabay video   6,331 ids     130 already on the shelf   6,201 to fetch
                                                            ------
                                                            14,143 clips, about 285 GB

Images are NOT in scope: 100,460 of them are also missing, and the owner chose videos first
(2026-08-22) because that is what the timeline is short of.

WHY ONE SCRIPT FOR BOTH. This was `recover_pexels_shelf.py`. Adding a sibling for Pixabay would
have copied the browse scan, the theme mapping, the tier placement, the ledger row and the lock
-- five things that then drift apart (rule 18). Only four things actually differ per provider,
and they live in SOURCES below.

WHAT IT WRITES.
  media   <tier>\\<theme>\\<source>__<id>__<slug>.mp4   -- the roomiest tier, same rule as the ingest
  ledger  E:\\pd-archive\\_ledger\\<source>.jsonl        -- one row per file, the shape
          `search_archive.py` already reads, so recovered clips become searchable immediately

RATE LIMITS. Pexels allows 200 requests/hour; only the metadata call counts, the file comes from
a CDN. Pixabay allows 100 requests per 60 seconds. The defaults are deliberate -- being throttled
costs more time than waiting. The two providers have separate limits and separate locks, so they
can and should run at the same time.

SAFE TO RE-RUN. Resumable by design: a clip already on disk with a non-zero size is skipped.

Usage:
    py -3.11 scripts/recover_stock_shelf.py --source pexels  --plan
    py -3.11 scripts/recover_stock_shelf.py --source pixabay --write
    py -3.11 scripts/recover_stock_shelf.py --source pexels  --want-ep76 --write
"""
from __future__ import annotations

import argparse
import atexit
import hashlib
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
BROWSE = Path(r"D:\pd-media-browse")
sys.path.insert(0, str(ROOT / "scripts"))
from ingest_archive_sources import TIERS  # noqa: E402 -- the shelf owns its own tier table

# Every root the shelf spans. Was a single hard-coded D:\pd-archive, which is how
# already_have() below went blind: measured 2026-08-22 it reported 1,399 clips already
# recovered while the ledger knew 1,434, because D: is not the whole shelf (D: 39,867
# files / 605 GB, E: 5,510 files / 160 GB). Anything that landed on E: would have been
# downloaded a second time.
SHELVES = [Path(t["root"]) for t in TIERS]
LEDGER_DIR = Path(r"E:\pd-archive\_ledger")


def _pexels_files(meta: dict) -> list[dict]:
    return [f for f in meta.get("video_files", []) if f.get("link")]


def _pexels_title(meta: dict, slug: str) -> str:
    return slug.replace("-", " ")[:120]


def _pixabay_files(meta: dict) -> list[dict]:
    """Pixabay returns a dict of named renditions, not a list. Flatten it to the same shape."""
    hits = meta.get("hits") or []
    if not hits:
        return []
    out = []
    for v in (hits[0].get("videos") or {}).values():
        if v.get("url"):
            out.append({"width": v.get("width", 0), "height": v.get("height", 0),
                        "link": v["url"]})
    return out


def _pixabay_title(meta: dict, slug: str) -> str:
    """The browse slug for pixabay is the literal string "id" -- the title lives in the tags."""
    hits = meta.get("hits") or []
    return (hits[0].get("tags", "") if hits else "")[:120] or slug


SOURCES: dict[str, dict] = {
    "pexels": {
        "url": "https://api.pexels.com/videos/videos/{id}",
        "key_env": "PEXELS_API_KEY",
        "auth": "header",                     # Authorization: <key>
        "files": _pexels_files,
        "title": _pexels_title,
        "page_url": lambda m: m.get("url", ""),
        "per_hour": 200,                      # provider limit, not a preference
        "licence": ("Pexels License -- free for commercial and non-commercial use, no "
                    "attribution required, identifiable persons may not be used for "
                    "anything defamatory"),
        "licence_field": "Pexels License",
    },
    "pixabay": {
        "url": "https://pixabay.com/api/videos/?key={key}&id={id}",
        "key_env": "PIXABAY_API_KEY",
        "auth": "query",                      # the key is already in the url
        "files": _pixabay_files,
        "title": _pixabay_title,
        "page_url": lambda m: ((m.get("hits") or [{}])[0].get("pageURL", "")),
        "per_hour": 3000,                     # provider allows 100/60s; 50/min leaves headroom
        "licence": "Pixabay Content License -- free for commercial use, no attribution required",
        "licence_field": "Pixabay Content License",
    },
}

# EP76's registers, and the registers its episode_spec bars. Only used with --want-ep76, and only
# meaningful for pexels: pixabay browse names carry no title, so nothing would ever match.
WANT = re.compile(
    r"(concrete|cement|rust|corro|rebar|reinforc|crack|peel|spall|"
    r"bridge|viaduct|overpass|flyover|tunnel|asphalt|guardrail|crash-barrier|"
    r"highway|motorway|freeway|traffic|road|lane|wheel|tyre|tire|"
    r"scaffold|weld|steel|girder|crane|container|cargo|freight|dock|harbou?r|shipyard|"
    r"worker|construction|engineer|inspect|"
    r"paper|document|folder|binder|archive|typewriter|desk|office|writ|stamp|ledger|"
    r"corridor|hallway|stair|"
    r"rain|fog|mist|cloud|overcast|dust|wet|puddle|texture|grain)")
BAR = re.compile(
    r"(venice|venezia|gondola|tuscan|toscana|cypress|amalfi|colosseum|"
    r"beach|palm|tropical|resort|sunset|golden|desert|snow|ski|"
    r"money|banknote|dollar|crypto|blockchain|stock-market|candlestick|"
    r"gavel|handcuff|prison|funeral|grave|hospital|ambulance|police|"
    r"newspaper|wallpaper|flag|christmas|wedding|handshake|"
    r"space|nasa|galaxy|planet|astronaut|"
    r"abstract|neon|hyperspace|futuristic|bokeh|glitter|confetti|kaleidoscop|"
    r"digital-animation|computer-generated|3d-render)")


def name_re(source: str) -> re.Pattern[str]:
    return re.compile(rf"^{source}__(\d+)__(.+)\.mp4$", re.I)


def api_key(source: str) -> str:
    var = SOURCES[source]["key_env"]
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith(var):
                v = line.split("=", 1)[1].strip().strip('"').strip("'")
                if v:
                    return v
    v = os.environ.get(var, "")
    if not v:
        raise SystemExit(f"[recover] no {var} in .env or environment")
    return v


def theme_for(p: Path) -> str:
    """The theme the clip was shelved under, taken from the browse tree it was linked from."""
    parts = [x for x in p.parts if x not in ("factory_browse", "stock_browse", "_mislabeled")]
    for part in reversed(parts[:-1]):
        if part not in (BROWSE.name, BROWSE.drive, "\\"):
            return re.sub(r"[^a-z0-9_]+", "_", part.lower()).strip("_") or "misc"
    return "misc"


def candidates(source: str, want_ep76: bool) -> list[tuple[str, str, str]]:
    """(id, slug, theme) for every dead symlink, newest-first by id so recent stock comes back first."""
    pat = name_re(source)
    out, seen = [], set()
    for p in BROWSE.rglob(f"{source}__*.mp4"):
        m = pat.match(p.name)
        if not m:
            continue
        vid, slug = m.group(1), m.group(2)
        if vid in seen:
            continue
        low = p.name.lower()
        if want_ep76 and (not WANT.search(low) or BAR.search(low)):
            continue
        seen.add(vid)
        out.append((vid, slug, theme_for(p)))
    out.sort(key=lambda r: -int(r[0]))
    return out


def already_have(source: str) -> set[str]:
    """Ids already held: on disk under EVERY tier, and in the ledger under ANY naming.

    Two blind spots, both measured 2026-08-22.

    One hard-coded root: it reported 1,399 pexels clips recovered while the ledger knew
    1,434, because D: is not the whole shelf (D: 39,867 files, E: 5,510).

    One filename prefix: the browse tree names pixabay clips pixabay__<id>__id.mp4, but
    ingest_modern_web writes pixabay_extra__v_<id>__<tags>.mp4, so a disk scan for
    pixabay__* found 0 of the 130 clips the ledger already had -- 130 downloads paid for
    twice, and the second copy under a second name.

    Only .mp4 rows count. Pixabay reuses its numeric id space across images and videos,
    and an image row must never mask a video that really is missing.
    """
    pat = name_re(source)
    have = set()
    for shelf in SHELVES:
        if not shelf.exists():
            continue
        for p in shelf.rglob(f"{source}__*.mp4"):
            m = pat.match(p.name)
            if m and p.stat().st_size > 0:
                have.add(m.group(1))
    family = source.split("_")[0]
    for f in LEDGER_DIR.glob("*.jsonl"):
        if f.name.startswith("rejects") or not f.name.startswith(family):
            continue
        for line in f.open(encoding="utf-8", errors="replace"):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if not str(rec.get("file_path", "")).lower().endswith(".mp4"):
                continue
            digits = re.findall(r"\d+", str(rec.get("id", "")))
            if digits:
                have.add(digits[-1])
    return have


def pick_shelf() -> Path:
    """The roomiest tier with headroom, the same rule ingest_archive_sources uses.

    Hard-coding D: here was a second implementation of a decision the ingest already
    owns (rule 18), and the two had drifted: D: has 530 GB free against a 250 GB floor
    while E: has 1,490 GB, and the 14,143 videos still missing are about 285 GB.
    """
    for t in TIERS:
        if not os.path.isdir(t["drive"]):
            continue
        if shutil.disk_usage(t["drive"]).free > t["floor"]:
            return Path(t["root"])
    raise SystemExit("[recover] every tier is below its free-space floor; nothing written")


def pick_file(files: list[dict]) -> dict | None:
    """Largest rendition inside a 1920x1080 frame; if none fits, the SMALLEST available.

    Two corrections, both measured 2026-08-22 on the first live pixabay fetch.

    The cap was width<=1920 AND height<=1080, which no PORTRAIT clip can ever satisfy --
    1080x1920 fails on height. Shorts are 9:16, so vertical stock is wanted, not excluded.
    The cap is now on the long and short edge, which accepts both orientations.

    The fallback took the LARGEST when nothing fit, which is backwards and expensive:
    pixabay 359377 is a 2160x3840 source, and that rule pulled 197.8 MB for a clip the
    timeline scales down anyway. Over 5,663 remaining pixabay videos that is the
    difference between a 285 GB job and a terabyte one.
    """
    linked = [f for f in files if f.get("link") and f.get("width")]
    if not linked:
        return None

    def edges(f: dict) -> tuple[int, int]:
        w, h = int(f.get("width", 0)), int(f.get("height", 0))
        return max(w, h), min(w, h)

    fits = [f for f in linked if edges(f)[0] <= 1920 and edges(f)[1] <= 1080]
    if fits:
        return max(fits, key=lambda f: edges(f)[0] * edges(f)[1])
    return min(linked, key=lambda f: edges(f)[0] * edges(f)[1])


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def single_instance(source: str) -> None:
    """Refuse to start when another recovery is already appending to this source's ledger.

    Measured 2026-08-22 16:11: TWO copies of this script were running against
    pexels.jsonl -- "--want-ep76 --per-hour 200 --write" (09:55) and "--write" (11:29),
    whose candidate list CONTAINS the first list. This is the same shape that tore 586
    lines and destroyed 117 rows in reindex_archive_shelf.py on 2026-08-20; that script
    grew a lock, this one was missed. Nothing was torn here because every row is written
    and flushed one short line at a time, but already_have() is read ONCE at start, so the
    two todo lists overlap and the same id can be fetched twice and written twice.

    It also buys nothing. Pexels allows 200 requests/hour; two copies pacing at 200/hour
    each hit 429 and back off. Measured throughput with both running was 44-155 rows/hour,
    the throughput of ONE copy, for twice the monthly API budget.

    The lock is PER SOURCE. pexels and pixabay have separate limits and separate ledger
    files, so blocking one on the other would cost days for no safety.
    """
    lock = LEDGER_DIR / f"{source}_recover.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise SystemExit(
            f"[recover] REFUSING TO START: {lock} exists, so another {source} recovery is "
            f"writing this ledger. Two writers duplicate rows and burn the API budget for "
            f"no extra throughput. If you are certain none is running, delete that file "
            f"and re-run.")
    os.write(fd, f"{os.getpid()}".encode())
    os.close(fd)
    atexit.register(lambda: lock.unlink(missing_ok=True))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=sorted(SOURCES), default="pexels")
    ap.add_argument("--ids-file", help="one id per line; overrides the browse scan")
    ap.add_argument("--want-ep76", action="store_true",
                    help="only EP76's registers, and none the episode_spec bars (pexels only)")
    ap.add_argument("--limit", type=int, default=0, help="stop after N downloads (0 = all)")
    ap.add_argument("--per-hour", type=int, default=0, help="0 = the provider's own limit")
    ap.add_argument("--plan", action="store_true", help="report and write nothing")
    ap.add_argument("--write", action="store_true", help="actually download")
    a = ap.parse_args()
    if not a.plan and not a.write:
        ap.error("give --plan or --write")

    src = a.source
    cfg = SOURCES[src]
    per_hour = a.per_hour or cfg["per_hour"]
    ledger = LEDGER_DIR / f"{src}.jsonl"

    rows = candidates(src, a.want_ep76)
    if a.ids_file:
        keep = {l.strip() for l in Path(a.ids_file).read_text(encoding="utf-8").splitlines() if l.strip()}
        rows = [r for r in rows if r[0] in keep]

    have = already_have(src)
    todo = [r for r in rows if r[0] not in have]
    print(f"[recover] source: {src}")
    print(f"[recover] browse manifest: {len(rows)} candidate(s)")
    print(f"[recover] already on the shelf: {len(rows) - len(todo)}")
    print(f"[recover] to fetch: {len(todo)}")
    if a.limit:
        todo = todo[:a.limit]
        print(f"[recover] --limit {a.limit} -> {len(todo)}")
    themes: dict[str, int] = {}
    for _, _, t in todo:
        themes[t] = themes.get(t, 0) + 1
    print(f"[recover] themes: {sorted(themes.items(), key=lambda x: -x[1])[:10]}")
    print(f"[recover] at {per_hour}/hour that is {len(todo) / max(per_hour, 1):.1f} hour(s)")
    if a.plan:
        print("[recover] --plan: nothing written")
        return 0

    single_instance(src)
    shelf = pick_shelf()
    print(f"[recover] writing to {shelf}")
    key = api_key(src)
    s = requests.Session()
    if cfg["auth"] == "header":
        s.headers.update({"Authorization": key})
    ledger.parent.mkdir(parents=True, exist_ok=True)
    gap = 3600.0 / max(per_hour, 1)

    ok = fail = 0
    with ledger.open("a", encoding="utf-8") as led:
        for i, (vid, slug, theme) in enumerate(todo, 1):
            t0 = time.time()
            try:
                url = cfg["url"].format(id=vid, key=key)
                r = s.get(url, timeout=30)
                if r.status_code == 429:
                    print("[recover] 429 -- backing off 10 min")
                    time.sleep(600)
                    r = s.get(url, timeout=30)
                if r.status_code != 200:
                    print(f"  {vid} HTTP {r.status_code}")
                    fail += 1
                    continue
                meta = r.json()
                f = pick_file(cfg["files"](meta))
                if not f:
                    print(f"  {vid} no usable file")
                    fail += 1
                    continue
                dest = shelf / theme / f"{src}__{vid}__{slug}.mp4"
                dest.parent.mkdir(parents=True, exist_ok=True)
                tmp = dest.with_suffix(".part")
                with s.get(f["link"], stream=True, timeout=180) as dl:
                    dl.raise_for_status()
                    with tmp.open("wb") as fh:
                        for chunk in dl.iter_content(1 << 20):
                            fh.write(chunk)
                tmp.replace(dest)
                led.write(json.dumps({
                    "id": f"{src}_{vid}",
                    "source": src,
                    "source_url": cfg["page_url"](meta),
                    "title": cfg["title"](meta, slug),
                    "license_field_raw": cfg["licence_field"],
                    "license_decision": "free_commercial",
                    "theme": theme,
                    "file_path": str(dest),
                    "bytes": dest.stat().st_size,
                    "sha256": sha256(dest),
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                    "relevance_score": 0,
                    "matched_keywords": [],
                    "recovery_note": ("re-downloaded after the H: drive died; the browse symlink "
                                      "at D:/pd-media-browse carried the id"),
                    "license_basis": cfg["licence"],
                    "width": f.get("width"), "height": f.get("height"),
                }, ensure_ascii=False) + "\n")
                led.flush()
                ok += 1
                if ok % 25 == 0:
                    print(f"  [{i}/{len(todo)}] ok={ok} fail={fail} last={dest.name[:60]}")
            except Exception as e:  # noqa: BLE001 - one bad clip must not stop a 9-hour run
                print(f"  {vid} ERROR {type(e).__name__}: {e}")
                fail += 1
            wait = gap - (time.time() - t0)
            if wait > 0:
                time.sleep(wait)

    print(f"[recover] done: {ok} fetched, {fail} failed")
    print(f"[recover] ledger -> {ledger}")
    print("[recover] NOT REVIEWED. footage_review_required is true: a person opens a labelled "
          "contact sheet before any of this enters a cut.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
