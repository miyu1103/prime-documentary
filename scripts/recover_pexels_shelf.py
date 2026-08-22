#!/usr/bin/env python3
"""Re-download the Pexels clips that died with the H: drive, by id, into the live shelf.

WHAT HAPPENED. `D:\\pd-media-browse` holds 19,041 zero-byte symlinks whose targets are all under
`H:\\pd-media\\assets\\factory\\...`. H: is dead, so every one of those files is gone. Measured
2026-08-22: `Length 0, Attributes ReparsePoint, Target ... exists: False`.

WHY THIS IS RECOVERABLE. Each symlink is named `pexels__<id>__<slug>.mp4`. The id is the Pexels
video id, `PEXELS_API_KEY` is set in `.env`, and the Pexels licence permits commercial use. So the
browse tree is not a record of a loss -- it is a shopping list.

WHY A NEW SCRIPT. `ingest_modern_web.py` ingests by SOURCE and THEME and does not list pexels among
its sources; `build_factory_library.py` builds by QUERY and writes its ledger to the dead H: path.
Neither can fetch a specific id. Recovering a known id set is a capability that did not exist, so
this is not a second implementation of either (`.claude/rules/18`).

WHAT IT WRITES.
  media   D:\\pd-archive\\<theme>\\pexels__<id>__<slug>.mp4      -- the live shelf
  ledger  E:\\pd-archive\\_ledger\\pexels.jsonl                   -- one row per file, the shape
          `search_archive.py` already reads, so recovered clips become searchable immediately

RATE LIMIT. The Pexels free tier allows 200 requests/hour and 20,000/month. Only the metadata call
counts; the file download comes from a CDN. The default pacing is 200/hour and it is deliberate --
being throttled costs more time than waiting.

SAFE TO RE-RUN. Resumable by design: a clip already on disk with a non-zero size is skipped, and the
ledger is rebuilt from disk rather than appended blindly, so a re-run cannot duplicate a row.

Usage:
    py -3.11 scripts/recover_pexels_shelf.py --plan                     # what would be fetched
    py -3.11 scripts/recover_pexels_shelf.py --ids-file <file> --write
    py -3.11 scripts/recover_pexels_shelf.py --want-ep76 --write        # this episode's registers
"""
from __future__ import annotations

import argparse
import atexit
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

ROOT = Path(__file__).resolve().parents[1]
BROWSE = Path(r"D:\pd-media-browse")
SHELF = Path(r"D:\pd-archive")
LEDGER = Path(r"E:\pd-archive\_ledger\pexels.jsonl")
API = "https://api.pexels.com/videos/videos/{id}"
LICENCE = ("Pexels License -- free for commercial and non-commercial use, no attribution "
           "required, identifiable persons may not be used for anything defamatory")

NAME = re.compile(r"^pexels__(\d+)__(.+)\.mp4$", re.I)

# EP76's registers, and the registers its episode_spec bars. Only used with --want-ep76.
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


def api_key() -> str:
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("PEXELS_API_KEY"):
                v = line.split("=", 1)[1].strip().strip('"').strip("'")
                if v:
                    return v
    v = os.environ.get("PEXELS_API_KEY", "")
    if not v:
        raise SystemExit("[recover] no PEXELS_API_KEY in .env or environment")
    return v


def theme_for(p: Path) -> str:
    """The theme the clip was shelved under, taken from the browse tree it was linked from."""
    parts = [x for x in p.parts if x not in ("factory_browse", "stock_browse", "_mislabeled")]
    for part in reversed(parts[:-1]):
        if part not in (BROWSE.name, BROWSE.drive, "\\"):
            return re.sub(r"[^a-z0-9_]+", "_", part.lower()).strip("_") or "misc"
    return "misc"


def candidates(want_ep76: bool) -> list[tuple[str, str, str]]:
    """(id, slug, theme) for every dead symlink, newest-first by id so recent stock comes back first."""
    out, seen = [], set()
    for p in BROWSE.rglob("*.mp4"):
        m = NAME.match(p.name)
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


def already_have() -> set[str]:
    have = set()
    for p in SHELF.rglob("pexels__*.mp4"):
        m = NAME.match(p.name)
        if m and p.stat().st_size > 0:
            have.add(m.group(1))
    return have


def pick_file(files: list[dict]) -> dict | None:
    """Largest file at or under 1920x1080. The shelf is cut into a 1920x1080 film; a 4K stock clip
    costs disk and decode time for detail the timeline throws away."""
    ok = [f for f in files if f.get("width") and f["width"] <= 1920 and f.get("height", 0) <= 1080
          and f.get("link")]
    if not ok:
        ok = [f for f in files if f.get("link")]
    if not ok:
        return None
    return max(ok, key=lambda f: (f.get("width", 0), f.get("height", 0)))


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def single_instance() -> None:
    """Refuse to start when another recovery is already appending to this ledger.

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
    """
    lock = LEDGER.parent / "pexels_recover.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise SystemExit(
            f"[recover] REFUSING TO START: {lock} exists, so another recovery is writing "
            f"this ledger. Two writers duplicate rows and burn the 200/hour Pexels budget "
            f"for no extra throughput. If you are certain none is running, delete that "
            f"file and re-run.")
    os.write(fd, f"{os.getpid()}".encode())
    os.close(fd)
    atexit.register(lambda: lock.unlink(missing_ok=True))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--ids-file", help="one pexels id per line; overrides the browse scan")
    ap.add_argument("--want-ep76", action="store_true",
                    help="only EP76's registers, and none the episode_spec bars")
    ap.add_argument("--limit", type=int, default=0, help="stop after N downloads (0 = all)")
    ap.add_argument("--per-hour", type=int, default=200, help="Pexels free tier is 200/hour")
    ap.add_argument("--plan", action="store_true", help="report and write nothing")
    ap.add_argument("--write", action="store_true", help="actually download")
    a = ap.parse_args()
    if not a.plan and not a.write:
        ap.error("give --plan or --write")

    rows = candidates(a.want_ep76)
    if a.ids_file:
        keep = {l.strip() for l in Path(a.ids_file).read_text(encoding="utf-8").splitlines() if l.strip()}
        rows = [r for r in rows if r[0] in keep]

    have = already_have()
    todo = [r for r in rows if r[0] not in have]
    print(f"[recover] browse manifest: {len(rows)} candidate(s)")
    print(f"[recover] already on the shelf: {len(rows) - len(todo)}")
    print(f"[recover] to fetch: {len(todo)}")
    if a.limit:
        todo = todo[:a.limit]
        print(f"[recover] --limit {a.limit} -> {len(todo)}")
    themes = {}
    for _, _, t in todo:
        themes[t] = themes.get(t, 0) + 1
    print(f"[recover] themes: {sorted(themes.items(), key=lambda x: -x[1])[:10]}")
    print(f"[recover] at {a.per_hour}/hour that is {len(todo) / max(a.per_hour, 1):.1f} hour(s)")
    if a.plan:
        print("[recover] --plan: nothing written")
        return 0

    single_instance()
    key = api_key()
    s = requests.Session()
    s.headers.update({"Authorization": key})
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    gap = 3600.0 / max(a.per_hour, 1)

    ok = fail = 0
    with LEDGER.open("a", encoding="utf-8") as led:
        for i, (vid, slug, theme) in enumerate(todo, 1):
            t0 = time.time()
            try:
                r = s.get(API.format(id=vid), timeout=30)
                if r.status_code == 429:
                    print("[recover] 429 -- backing off 10 min")
                    time.sleep(600)
                    r = s.get(API.format(id=vid), timeout=30)
                if r.status_code != 200:
                    print(f"  {vid} HTTP {r.status_code}")
                    fail += 1
                    continue
                meta = r.json()
                f = pick_file(meta.get("video_files", []))
                if not f:
                    print(f"  {vid} no usable file")
                    fail += 1
                    continue
                dest = SHELF / theme / f"pexels__{vid}__{slug}.mp4"
                dest.parent.mkdir(parents=True, exist_ok=True)
                tmp = dest.with_suffix(".part")
                with s.get(f["link"], stream=True, timeout=180) as dl:
                    dl.raise_for_status()
                    with tmp.open("wb") as fh:
                        for chunk in dl.iter_content(1 << 20):
                            fh.write(chunk)
                tmp.replace(dest)
                led.write(json.dumps({
                    "id": f"pexels_{vid}",
                    "source": "pexels",
                    "source_url": meta.get("url", ""),
                    "title": slug.replace("-", " ")[:120],
                    "license_field_raw": "Pexels License",
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
                    "license_basis": LICENCE,
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
    print(f"[recover] ledger -> {LEDGER}")
    print("[recover] NOT REVIEWED. footage_review_required is true: a person opens a labelled "
          "contact sheet before any of this enters a cut.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
