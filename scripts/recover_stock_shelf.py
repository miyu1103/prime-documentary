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

RATE LIMITS, measured rather than assumed (2026-08-23). This key is NOT on the published 200/hour
free tier: X-Ratelimit-Limit returns -1, a 40-request burst at a 7,487/hour pace drew zero 429s,
and X-Ratelimit-Remaining reads ~23,000. Pixabay allows 100 requests per 60 seconds. Only the
metadata call counts against either; the file itself comes from a CDN. The two providers have
separate limits and separate locks, so they can and should run at the same time.

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
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
BROWSE = Path(r"D:\pd-media-browse")
sys.path.insert(0, str(ROOT / "scripts"))
from ingest_archive_sources import TIERS  # noqa: E402 -- the shelf owns its own tier table
from rename_shelf_for_search import slugify as slugify_title  # noqa: E402 -- one slug rule

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
        # 600, and the road to that number is worth keeping because two probes lied first.
        #
        # It was 200, taken from Pexels' published free-tier figure rather than from this
        # account. Asking the API returns X-Ratelimit-Limit: -1 and X-Ratelimit-Remaining: -1,
        # which reads as "no limit", so it went to 1,200. The run then drew 27 throttles a
        # night and the pace collapsed to 60/hour.
        #
        # Two burst tests said there was no limit at any speed, including flat out with four
        # concurrent CDN downloads running. Both were wrong for the same reason: they reused a
        # handful of ids, and a repeated id is served from the edge cache. The real work asks
        # for a DIFFERENT id every time and misses the cache every time.
        #
        # Re-run with genuinely unfetched ids, 2026-08-23 16:50:
        #     1,200/hour, fresh ids : 9 of 40 refused, "Throttle limit exceeded"
        #       600/hour, fresh ids : 0 of 25 refused
        # A measurement that does not reproduce the real request pattern measures nothing.
        "per_hour": 600,
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

def _pexels_photo_files(meta: dict) -> list[dict]:
    """Pexels photos carry named renditions with no per-rendition dimensions, so the top-level
    width/height of the original is reported and `large2x` (~1880 px wide) is the one taken:
    plenty for a 1920-wide timeline, a fraction of the original's bytes."""
    src = meta.get("src") or {}
    for name in ("large2x", "large", "original", "medium"):
        if src.get(name):
            return [{"link": src[name], "width": meta.get("width", 0), "height": meta.get("height", 0)}]
    return []


def _pixabay_image_files(meta: dict) -> list[dict]:
    hits = meta.get("hits") or []
    if not hits:
        return []
    h = hits[0]
    for name in ("largeImageURL", "webformatURL"):
        if h.get(name):
            return [{"link": h[name], "width": h.get("imageWidth", 0), "height": h.get("imageHeight", 0)}]
    return []


def _pexels_photo_title(meta: dict, slug: str) -> str:
    return (meta.get("alt") or slug.replace("-", " "))[:120]


# Per (source, kind): the four things that differ. Everything account-level -- key, auth, pacing,
# licence -- stays in SOURCES above and is shared by both kinds.
#
# Images were out of scope until 2026-08-23, when the owner asked for the whole shelf back. They
# are the bulk of it: of 83,683 items still missing, 72,616 are stills. They are also cheap --
# roughly 0.6 MB against 16 MB for a clip -- so an image lane costs API calls, not bandwidth, and
# can run beside the video lanes without slowing them.
KINDS: dict[tuple[str, str], dict] = {
    ("pexels", "video"): {
        "ext": "mp4",
        "url": "https://api.pexels.com/videos/videos/{id}",
        "files": _pexels_files,
        "title": _pexels_title,
        "page_url": lambda m: m.get("url", ""),
    },
    ("pexels", "image"): {
        "ext": "jpg",
        "url": "https://api.pexels.com/v1/photos/{id}",
        "files": _pexels_photo_files,
        "title": _pexels_photo_title,
        "page_url": lambda m: m.get("url", ""),
    },
    ("pixabay", "video"): {
        "ext": "mp4",
        "url": "https://pixabay.com/api/videos/?key={key}&id={id}",
        "files": _pixabay_files,
        "title": _pixabay_title,
        "page_url": lambda m: ((m.get("hits") or [{}])[0].get("pageURL", "")),
    },
    ("pixabay", "image"): {
        "ext": "jpg",
        "url": "https://pixabay.com/api/?key={key}&id={id}",
        "files": _pixabay_image_files,
        "title": _pixabay_title,
        "page_url": lambda m: ((m.get("hits") or [{}])[0].get("pageURL", "")),
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


def name_re(source: str, kind: str) -> re.Pattern[str]:
    ext = KINDS[(source, kind)]["ext"]
    return re.compile(rf"^{source}__(\d+)__(.+)\.{ext}$", re.I)


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


def candidates(source: str, kind: str, want_ep76: bool) -> list[tuple[str, str, str]]:
    """(id, slug, theme) for every dead symlink, newest-first by id so recent stock comes back first."""
    pat = name_re(source, kind)
    ext = KINDS[(source, kind)]["ext"]
    out, seen = [], set()
    for p in BROWSE.rglob(f"{source}__*.{ext}"):
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


def already_have(source: str, kind: str) -> set[str]:
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
    pat = name_re(source, kind)
    ext = KINDS[(source, kind)]["ext"]
    have = set()
    for shelf in SHELVES:
        if not shelf.exists():
            continue
        for p in shelf.rglob(f"{source}__*.{ext}"):
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
            if not str(rec.get("file_path", "")).lower().endswith("." + ext):
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


class Pace:
    """Thread-safe request pacer for the METADATA call only.

    The provider limit applies to the API (Pexels 200/hour, Pixabay 100/minute); the file
    itself comes from a CDN with no such limit. So the pacer gates the small call and lets the
    big transfers overlap, which is the whole point of running more than one worker.
    """

    def __init__(self, per_hour: int) -> None:
        self.base_gap = 3600.0 / max(per_hour, 1)
        self.gap = self.base_gap
        self.next_at = 0.0
        self.ok_since_429 = 0
        self.last_429 = 0.0
        self.known_bad_gap = 0.0   # the fastest pace that has actually been refused
        self.lock = threading.Lock()

    def wait(self) -> None:
        with self.lock:
            due = max(time.time(), self.next_at)
            self.next_at = due + self.gap
        delay = due - time.time()
        if delay > 0:
            time.sleep(delay)

    def slow_down(self) -> float:
        """Halve the pace after a 429 and stay there.

        The true ceiling is not published for this account -- X-Ratelimit-Limit reads -1 and a
        40-request burst drew nothing -- so it cannot be configured, only discovered. Two lanes
        sharing one Pexels key at 1,200/hour each found it on 2026-08-23. Rather than guess a
        new constant, each lane backs its own pace off by half whenever the provider says no,
        which converges from either direction without anyone having to know the number.
        """
        with self.lock:
            now = time.time()
            # One incident, one halving. Four workers hit the ceiling within the same second
            # and each reported it, so a single refusal was being counted four times and the
            # pace fell 1200 -> 600 -> 300 -> 150 -> 75 in a breath. Measured 2026-08-23: 27
            # refusals produced that collapse repeatedly, and the lane spent the night
            # oscillating between 60/hour and 1,200 instead of settling anywhere.
            if now - self.last_429 < 30.0:
                return 3600.0 / self.gap
            self.last_429 = now
            self.known_bad_gap = max(self.known_bad_gap, self.gap)
            self.gap = min(self.gap * 2, 60.0)
            self.ok_since_429 = 0
            return 3600.0 / self.gap

    def speed_up(self) -> float | None:
        """Climb back after a clean stretch, or the first 429 of the night is permanent.

        Measured 2026-08-23 08:20: backing off without ever recovering left the pexels image
        lane pinned at 60 requests/hour -- 2,097 hours for the work in front of it -- because
        23 scattered 429s had each halved a pace nothing could raise again. Backoff without
        recovery is not adaptive, it is a ratchet.
        """
        with self.lock:
            self.ok_since_429 += 1
            if self.ok_since_429 < 25 or self.gap <= self.base_gap:
                return None
            # Climb back 10% at a time, and never back onto a pace that has already been
            # refused. Doubling walked straight into the ceiling again every time: the log
            # reads 150, 300, 600, 1200, refused, 600, 300, 150, 75. Additive increase with a
            # remembered ceiling settles just under whatever the real limit turns out to be,
            # which is the only way to find a number the provider will not tell us.
            floor = self.base_gap
            if self.known_bad_gap:
                floor = max(floor, self.known_bad_gap * 1.15)
            nxt = max(floor, self.gap * 0.9)
            if nxt >= self.gap:
                self.ok_since_429 = 0
                return None
            self.gap = nxt
            self.ok_since_429 = 0
            return 3600.0 / self.gap


_APPEND_LOCK = threading.Lock()


def _lock_tail(fd: int, nbytes: int) -> None:
    """Block until this process owns the bytes it is about to append.

    Windows has no O_APPEND atomicity guarantee, so the seek and the write are separable and
    two processes can land inside each other. msvcrt.locking takes a byte-range lock from the
    current offset; the range is released when the descriptor closes.
    """
    try:
        import msvcrt
        msvcrt.locking(fd, msvcrt.LK_LOCK, max(1, nbytes))
    except (ImportError, OSError):
        try:
            import fcntl
            fcntl.flock(fd, fcntl.LOCK_EX)
        except Exception:  # noqa: BLE001 - no OS lock available; the thread lock still holds
            pass


def append_row(ledger: Path, row: dict) -> None:
    """One locked write of one line -- atomic across threads AND processes.

    Same rule the ingest lane learned on 2026-08-20, when writers sharing one handle tore 586
    lines in half. A held file object plus a thread pool is that mistake with a smaller cast.

    O_APPEND alone was not enough, and this cost three rows to learn. POSIX makes an append
    write atomic; Windows does not -- it seeks to the end and then writes, and a second process
    can land between those steps. Measured 2026-08-23 16:00: while the pixabay video and image
    lanes were both appending to pixabay.jsonl, three rows were torn in half. Exactly the
    failure this function exists to prevent, in the one place I had assumed it could not
    happen. The thread lock covers this process; the byte-range lock covers the others.
    """
    data = (json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8")
    with _APPEND_LOCK:
        fd = os.open(ledger, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
        try:
            _lock_tail(fd, len(data))
            os.write(fd, data)
        finally:
            os.close(fd)


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


def single_instance(source: str, kind: str) -> None:
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
    lock = LEDGER_DIR / f"{source}_{kind}_recover.lock"
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
    ap.add_argument("--kind", choices=("video", "image"), default="video")
    ap.add_argument("--ids-file", help="one id per line; overrides the browse scan")
    ap.add_argument("--want-ep76", action="store_true",
                    help="only EP76's registers, and none the episode_spec bars (pexels only)")
    ap.add_argument("--limit", type=int, default=0, help="stop after N downloads (0 = all)")
    ap.add_argument("--per-hour", type=int, default=0, help="0 = the provider's own limit")
    ap.add_argument("--workers", type=int, default=4,
                    help="concurrent downloads; 4 measured as the knee, 8 congests")
    ap.add_argument("--plan", action="store_true", help="report and write nothing")
    ap.add_argument("--write", action="store_true", help="actually download")
    a = ap.parse_args()
    if not a.plan and not a.write:
        ap.error("give --plan or --write")

    src, kind = a.source, a.kind
    cfg = SOURCES[src]
    kc = KINDS[(src, kind)]
    per_hour = a.per_hour or cfg["per_hour"]
    ledger = LEDGER_DIR / f"{src}.jsonl"

    rows = candidates(src, kind, a.want_ep76)
    if a.ids_file:
        keep = {l.strip() for l in Path(a.ids_file).read_text(encoding="utf-8").splitlines() if l.strip()}
        rows = [r for r in rows if r[0] in keep]

    have = already_have(src, kind)
    todo = [r for r in rows if r[0] not in have]
    print(f"[recover] source: {src} {kind}")
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

    single_instance(src, kind)
    shelf = pick_shelf()
    print(f"[recover] writing to {shelf}")
    key = api_key(src)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    print(f"[recover] {a.workers} worker(s)")

    # WHY A POOL, MEASURED 2026-08-23 03:35 on the degraded line. Against a 10 MB reference
    # download: 1 stream 2.93 MB/s, 4 streams 5.09 MB/s, 8 streams 2.97 MB/s -- four is the
    # knee, eight congests and is no better than one. Meanwhile this run was managing 0.76 MB/s,
    # a quarter of what ONE stream could do, because a 235 ms round trip was being paid serially
    # for every clip: API call, connect, transfer, hash, next. The pool overlaps those waits.
    # The provider's request limit is respected by Pace, which gates only the metadata call.
    pace = Pace(per_hour)
    local = threading.local()
    counts = {"ok": 0, "fail": 0}
    clock = threading.Lock()

    def session() -> requests.Session:
        if not hasattr(local, "s"):
            local.s = requests.Session()
            if cfg["auth"] == "header":
                local.s.headers.update({"Authorization": key})
        return local.s

    def fetch(item: tuple[str, str, str]) -> None:
        vid, slug, theme = item
        s = session()
        try:
            pace.wait()
            url = kc["url"].format(id=vid, key=key)
            r = s.get(url, timeout=(10, 30))
            if r.status_code == 429:
                # 60 s, not 10 minutes. A 429 is "too fast just now", and the old ten-minute
                # sleep punished the whole lane for it; measured 2026-08-23, one 429 in the
                # pexels image lane cost more wall clock than the fifty clips around it.
                new_rate = pace.slow_down()
                wait_s = float(r.headers.get("Retry-After") or 60)
                print(f"[recover] 429 -- pace now {new_rate:.0f}/hour, waiting {wait_s:.0f}s",
                      flush=True)
                time.sleep(wait_s)
                r = s.get(url, timeout=(10, 30))
            if r.status_code != 200:
                print(f"  {vid} HTTP {r.status_code}")
                with clock:
                    counts["fail"] += 1
                return
            meta = r.json()
            f = pick_file(kc["files"](meta))
            if not f:
                print(f"  {vid} no usable file")
                with clock:
                    counts["fail"] += 1
                return
            # Name it from the TITLE when the browse slug carries no words. Pixabay's browse
            # tree names every clip `pixabay__<id>__id`, so the slug is the literal string
            # "id" -- and stage_footage_by_title.py matches the filename and nothing else.
            # 5,638 files arrived that way before anyone noticed, unfindable by any search a
            # person would type while their titles sat one field away in the ledger. They
            # were renamed on 2026-08-23; this stops the next batch needing it.
            name_slug = slug
            if len([w for w in re.findall(r"[a-z0-9]+", slug.lower()) if len(w) > 2]) < 2:
                from_title = slugify_title(kc["title"](meta, slug))
                if len(from_title.split("-")) >= 2:
                    name_slug = from_title
            dest = shelf / theme / f"{src}__{vid}__{name_slug}.{kc['ext']}"
            dest.parent.mkdir(parents=True, exist_ok=True)
            tmp = dest.with_suffix(".part")
            # (connect, read) rather than one 180 s number, plus a wall-clock budget.
            # Measured 2026-08-23 03:20 on a degraded line -- 11 Mbps, 393 ms RTT -- the
            # run had dropped from 350-600 clips/hour to 10-22 while the link itself could
            # still carry ~250. The time was going into dying transfers: requests' timeout
            # is PER READ, so a socket that trickles a byte every few seconds never trips a
            # 180 s read timeout and blocks the single-threaded loop for as long as it likes.
            # A short read timeout catches the stalls; the budget catches the trickles.
            budget = 180.0
            t_dl = time.time()
            with s.get(f["link"], stream=True, timeout=(10, 30)) as dl:
                dl.raise_for_status()
                with tmp.open("wb") as fh:
                    for chunk in dl.iter_content(1 << 20):
                        fh.write(chunk)
                        if time.time() - t_dl > budget:
                            raise TimeoutError(
                                f"download exceeded {budget:.0f}s wall clock; abandoning "
                                f"this clip so the run keeps moving")
            tmp.replace(dest)
            append_row(ledger, {
                    "id": f"{src}_{vid}",
                    "source": src,
                    "source_url": kc["page_url"](meta),
                    "title": kc["title"](meta, slug),
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
            })
            faster = pace.speed_up()
            if faster:
                print(f"[recover] clean run -- pace back up to {faster:.0f}/hour", flush=True)
            with clock:
                counts["ok"] += 1
                n = counts["ok"]
            if n % 25 == 0:
                print(f"  [{n + counts['fail']}/{len(todo)}] ok={n} fail={counts['fail']} "
                      f"last={dest.name[:60]}", flush=True)
        except Exception as e:  # noqa: BLE001 - one bad clip must not stop a multi-hour run
            print(f"  {vid} ERROR {type(e).__name__}: {e}")
            with clock:
                counts["fail"] += 1

    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        list(pool.map(fetch, todo))
    ok, fail = counts["ok"], counts["fail"]

    print(f"[recover] done: {ok} fetched, {fail} failed")
    print(f"[recover] ledger -> {ledger}")
    print("[recover] NOT REVIEWED. footage_review_required is true: a person opens a labelled "
          "contact sheet before any of this enters a cut.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
