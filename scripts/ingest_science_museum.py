# -*- coding: utf-8 -*-
"""
SCIENCE / MUSEUM ingest adapter for the Prime Documentary free-asset archive shelf.

Sibling of scripts/ingest_archive_sources.py (which handles IA/LOC/stock/etc.).
This adapter owns the science + museum sources:

    nasa         NASA Image and Video Library (images-api.nasa.gov, keyless, PD)
                 images + video, themed queries (space/weather/science/ocean/timelapse)
    noaa         NOAA public-domain media. NOAA's own photolib.noaa.gov has no clean
                 public API (OrangeLogic asset bank), so NOAA PD material is ingested
                 via Wikimedia Commons file search restricted to NOAA-credited files
                 with a STRICT per-file license check (PD/CC0 only -> shelf).
    met          Met Museum Open Access (collectionapi.metmuseum.org, keyless).
                 Only objects with isPublicDomain=true (CC0) are taken.
    smithsonian  Smithsonian Open Access (api.si.edu). Needs a free api.data.gov key
                 (env DATA_GOV_API_KEY or SMITHSONIAN_API_KEY). Skips gracefully
                 without it; CC0-usage media only.
    nypl         NYPL Digital Collections (api.repo.nypl.org). Needs a free token
                 (env NYPL_API_TOKEN). Skips gracefully without it; public-domain
                 captures only.
    rawpixel     rawpixel.com public-domain boards. No official API; their internal
                 /api/v1/search returns 403 to non-browser clients (Cloudflare).
                 The adapter probes once per run and SKIPS with a note unless the
                 probe succeeds; if it ever succeeds, pulls are small + curated.

Storage (tier affinity for this adapter; C: is NEVER used):
    Tier A  F:\\pd-archive\\<theme>\\      STOP using F: when free < 50 GB
    Tier B  D:\\pd-archive\\<theme>\\      STOP using D: when free < 250 GB
When both floors are hit the run stops cleanly. Quarantine + ledgers stay on H::

    H:\\pd-media\\assets\\archive\\_quarantine\\<theme>\\
    H:\\pd-media\\assets\\archive\\_ledger\\{nasa,noaa,met,smithsonian,nypl,rawpixel}.jsonl

Ledger JSONL schema (one object per line):
    {id, source, source_url, title, license_field_raw,
     license_decision (pd|cc0|review_required), theme, file_path, bytes, sha256,
     fetched_at, relevance_score, matched_keywords}
Rejects (corrupt / below technical floor / license fail) are logged to
    H:\\pd-media\\assets\\archive\\_ledger\\rejects.jsonl

Quality gates (per item, precision-first):
  * relevance score from title/description keyword match vs the themed query;
    below-threshold items are skipped and never downloaded
  * soft bias away from identifiable-individual portraits / ceremony photos
    (negative keyword list; NASA crew portraits etc. are skipped)
  * technical floors: images >= 1200 px on the long side, video height >= 480,
    every file ffprobe-validated after download; corrupt files deleted + logged
  * dedup: (source,id) pairs already in ANY ledger are skipped before download;
    sha256 collisions against all ledgers (and existing_index.json if present)
    are deleted + logged after download
  * polite rates per source; resumable — a relaunch continues where it stopped

Usage:
  py -3.11 scripts/ingest_science_museum.py --source nasa --limit 3      # smoke
  py -3.11 scripts/ingest_science_museum.py --source all                 # full run
  py -3.11 scripts/ingest_science_museum.py --source met --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GB = 1024 ** 3

# --- storage tiers for this adapter (F: primary, D: overflow; C: never) ---
TIERS = [
    {"name": "F", "root": r"F:\pd-archive", "drive": "F:\\", "floor": 50 * GB},
    {"name": "D", "root": r"D:\pd-archive", "drive": "D:\\", "floor": 250 * GB},
]
H_ROOT = r"H:\pd-media\assets\archive"
LEDGER_DIR = os.path.join(H_ROOT, "_ledger")
QUARANTINE = os.path.join(H_ROOT, "_quarantine")
REJECTS_PATH = os.path.join(LEDGER_DIR, "rejects.jsonl")
EXISTING_INDEX = os.path.join(H_ROOT, "existing_index.json")

MY_SOURCES = ["nasa", "noaa", "met", "smithsonian", "nypl", "rawpixel"]

UA = "PrimeDocumentaryIngest/1.0 (archival research; contact: aab153792@gmail.com)"
MAX_ITEM_BYTES = 2 * GB
MIN_ITEM_BYTES = 15 * 1024
MIN_IMAGE_LONG_SIDE = 1200
MIN_VIDEO_HEIGHT = 480

RATE = {"nasa": 0.8, "noaa": 1.0, "met": 0.4, "smithsonian": 1.0,
        "nypl": 1.0, "rawpixel": 3.0}

# soft bias away from identifiable-individual portraits / people-centric shots
NEG_RE = re.compile(
    r"\b(portrait|portraits|headshot|mugshot|mug shot|interview|press conference|"
    r"award ceremony|awards ceremony|group photo|official photo|posing|poses for|"
    r"signing ceremony|swearing.in|administrator [A-Z]|astronaut candidate|"
    r"crew portrait|class photo|delegation|congress(?:man|woman)|senator|"
    r"in memoriam|memorial service|retirement)\b", re.I)

STOPWORDS = set(
    "the a an of in on and or for with to at from by over under into is are was "
    "were view views image photo photograph new old".split())
KW_POINTS = 15
THRESHOLD = {"nasa": 15, "noaa": 30, "met": 15, "smithsonian": 15, "nypl": 30,
             "rawpixel": 15}

# ---------------------------------------------------------------------------
# themed query plans: (theme, query, extra) per source
# ---------------------------------------------------------------------------
NASA_QUERIES = [
    # (theme, query, media_types)
    ("space_nasa", "nebula", "image"),
    ("space_nasa", "galaxy", "image"),
    ("space_nasa", "earth from space", "image,video"),
    ("space_nasa", "rocket launch", "image,video"),
    ("space_nasa", "international space station", "image,video"),
    ("space_nasa", "moon surface", "image,video"),
    ("space_nasa", "mars surface", "image,video"),
    ("space_nasa", "solar flare", "image,video"),
    ("space_nasa", "aurora", "image,video"),
    ("space_nasa", "spacewalk", "image,video"),
    ("space_nasa", "saturn rings", "image"),
    ("space_nasa", "jupiter", "image"),
    ("space_nasa", "apollo lunar surface", "image,video"),
    ("space_nasa", "satellite orbit", "image,video"),
    ("space_nasa", "space shuttle launch", "image,video"),
    ("weather_disasters", "hurricane from space", "image,video"),
    ("weather_disasters", "typhoon satellite", "image"),
    ("weather_disasters", "wildfire smoke satellite", "image"),
    ("weather_disasters", "storm system", "image,video"),
    ("weather_disasters", "dust storm satellite", "image"),
    ("ocean_nature", "ocean from space", "image,video"),
    ("ocean_nature", "phytoplankton bloom", "image"),
    ("ocean_nature", "coral reef", "image"),
    ("ocean_nature", "sea ice", "image,video"),
    ("science_tech", "wind tunnel", "image,video"),
    ("science_tech", "laboratory research", "image"),
    ("science_tech", "robotics", "image,video"),
    ("science_tech", "mission control", "image,video"),
    ("science_tech", "supercomputer", "image"),
    ("science_tech", "clean room spacecraft", "image,video"),
    ("science_tech", "telescope", "image,video"),
    ("landscapes_timelapse", "earth time lapse", "image,video"),
    ("landscapes_timelapse", "city lights at night", "image,video"),
    ("landscapes_timelapse", "glacier", "image"),
    ("landscapes_timelapse", "desert from space", "image"),
    ("landscapes_timelapse", "river delta satellite", "image"),
]

NOAA_QUERIES = [
    # (theme, query, commons filetype filter)
    ("ocean_nature", "coral reef", "bitmap"),
    ("ocean_nature", "deep sea", "bitmap"),
    ("ocean_nature", "ocean waves", "bitmap"),
    ("ocean_nature", "research vessel", "bitmap"),
    ("ocean_nature", "submersible", "bitmap"),
    ("ocean_nature", "hydrothermal vent", "bitmap"),
    ("ocean_nature", "kelp forest", "bitmap"),
    ("weather_disasters", "tornado", "bitmap"),
    ("weather_disasters", "hurricane damage", "bitmap"),
    ("weather_disasters", "lightning", "bitmap"),
    ("weather_disasters", "flood", "bitmap"),
    ("weather_disasters", "waterspout", "bitmap"),
    ("weather_disasters", "storm clouds", "bitmap"),
    ("weather_disasters", "blizzard snow", "bitmap"),
    ("wildlife_animals", "whale", "bitmap"),
    ("wildlife_animals", "dolphin", "bitmap"),
    ("wildlife_animals", "seal", "bitmap"),
    ("wildlife_animals", "sea turtle", "bitmap"),
    ("wildlife_animals", "shark", "bitmap"),
    ("wildlife_animals", "seabird", "bitmap"),
    ("wildlife_animals", "fish school", "bitmap"),
    ("landscapes_timelapse", "coastline aerial", "bitmap"),
    ("landscapes_timelapse", "lighthouse", "bitmap"),
    ("landscapes_timelapse", "arctic ice", "bitmap"),
    ("science_tech", "weather balloon", "bitmap"),
    ("science_tech", "radar dome", "bitmap"),
    ("laboratory_forensics", "laboratory", "bitmap"),
    ("weather_disasters", "tornado", "video"),
    ("ocean_nature", "deep sea", "video"),
    ("wildlife_animals", "whale", "video"),
]

MET_QUERIES = [
    ("textures_backgrounds", "ornament pattern"),
    ("textures_backgrounds", "textile fragment"),
    ("textures_backgrounds", "wallpaper design"),
    ("textures_backgrounds", "marbled paper"),
    ("textures_backgrounds", "gold decorative"),
    ("ocean_nature", "seascape"),
    ("ocean_nature", "ship storm sea"),
    ("ocean_nature", "naval battle"),
    ("landscapes_timelapse", "landscape painting"),
    ("landscapes_timelapse", "hudson river"),
    ("landscapes_timelapse", "mountain landscape"),
    ("wildlife_animals", "bird study"),
    ("wildlife_animals", "horse painting"),
    ("wildlife_animals", "animal study"),
    ("science_tech", "scientific instrument"),
    ("science_tech", "celestial globe"),
    ("science_tech", "astronomical"),
    ("science_tech", "sundial"),
    # period American material fits the existing shelf theme created by the
    # sibling IA ingest (americana_1930s_1970s holds the shelf's period lane)
    ("americana_1930s_1970s", "american city street"),
    ("americana_1930s_1970s", "american courtroom"),
    ("americana_1930s_1970s", "allegory of justice"),
]

SMITHSONIAN_QUERIES = [
    ("science_tech", "laboratory apparatus"),
    ("science_tech", "microscope"),
    ("science_tech", "telegraph"),
    ("laboratory_forensics", "forensic"),
    ("laboratory_forensics", "chemistry laboratory"),
    ("wildlife_animals", "bird specimen"),
    ("wildlife_animals", "butterfly"),
    ("space_nasa", "spacecraft"),
    ("space_nasa", "rocket engine"),
    ("textures_backgrounds", "pattern design"),
    ("americana_1930s_1970s", "american factory"),
    ("americana_1930s_1970s", "courthouse"),
]

NYPL_QUERIES = [
    ("americana_1930s_1970s", "new york street"),
    ("americana_1930s_1970s", "courthouse"),
    ("landscapes_timelapse", "landscape"),
    ("ocean_nature", "harbor ships"),
    ("textures_backgrounds", "ornament"),
]

RAWPIXEL_QUERIES = [
    ("textures_backgrounds", "vintage texture"),
    ("wildlife_animals", "vintage animal illustration"),
    ("ocean_nature", "vintage ocean"),
]

# ---------------------------------------------------------------------------
# infra helpers
# ---------------------------------------------------------------------------
_session = requests.Session()
_session.headers["User-Agent"] = UA


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def free_bytes(drive: str) -> int:
    try:
        import shutil as _sh
        return _sh.disk_usage(drive).free
    except OSError:
        return 0


def pick_root(est_bytes: int) -> str | None:
    """Return a tier root with room for est_bytes, honoring floors."""
    for t in TIERS:
        if not os.path.isdir(t["drive"]):
            continue
        if free_bytes(t["drive"]) - est_bytes > t["floor"]:
            return t["root"]
    return None


def get(url: str, *, params=None, timeout=60, tries=3, headers=None):
    last = None
    for i in range(tries):
        try:
            r = _session.get(url, params=params, timeout=timeout, headers=headers)
            if r.status_code == 200:
                return r
            if r.status_code in (403, 404, 410):
                return r  # caller decides; no point retrying
            last = f"http {r.status_code}"
        except requests.RequestException as e:  # noqa: PERF203
            last = repr(e)
        time.sleep(2.0 * (i + 1))
    log(f"    GET failed ({last}): {url[:120]}")
    return None


def get_json(url: str, **kw):
    r = get(url, **kw)
    if r is None or r.status_code != 200:
        return None
    try:
        return r.json()
    except ValueError:
        return None


def safe_name(s: str, maxlen=70) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_")
    return s[:maxlen] or "untitled"


def title_slug(s: str, maxlen=60) -> str:
    """OWNER convention: ASCII lowercase-hyphen slug of the title, max 60."""
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return (s[:maxlen].rstrip("-")) or "untitled"


def shelf_filename(source: str, item_id: str, title: str, ext: str) -> str:
    """Self-describing name: <source>__<id>__<title-slug>.<ext>."""
    sid = safe_name(str(item_id), 60)
    return f"{source}__{sid}__{title_slug(title)}{ext.lower()}"


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ffprobe(path: str) -> dict | None:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-print_format", "json",
             "-show_streams", "-show_format", path],
            capture_output=True, text=True, timeout=120)
        if out.returncode != 0:
            return None
        return json.loads(out.stdout)
    except Exception:
        return None


def probe_floors(path: str, kind: str) -> tuple[bool, str]:
    """Validate decode + technical floors. kind: image|video."""
    info = ffprobe(path)
    if not info or not info.get("streams"):
        return False, "ffprobe_failed"
    vstreams = [s for s in info["streams"] if s.get("codec_type") == "video"]
    if not vstreams:
        return False, "no_video_stream"
    w = max(int(s.get("width") or 0) for s in vstreams)
    h = max(int(s.get("height") or 0) for s in vstreams)
    if kind == "image":
        if max(w, h) < MIN_IMAGE_LONG_SIDE:
            return False, f"image_below_floor_{w}x{h}"
    else:
        if h < MIN_VIDEO_HEIGHT:
            return False, f"video_below_floor_{w}x{h}"
        dur = float(info.get("format", {}).get("duration") or 0)
        if dur <= 0.5:
            return False, "video_no_duration"
    return True, f"{w}x{h}"


def download(url: str, dest: str, max_bytes=MAX_ITEM_BYTES) -> int | None:
    """Stream url to dest via .part; return bytes or None."""
    part = dest + ".part"
    try:
        with _session.get(url, stream=True, timeout=120) as r:
            if r.status_code != 200:
                return None
            cl = r.headers.get("content-length")
            if cl and int(cl) > max_bytes:
                return None
            n = 0
            with open(part, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    n += len(chunk)
                    if n > max_bytes:
                        f.close()
                        os.remove(part)
                        return None
                    f.write(chunk)
        os.replace(part, dest)
        return n
    except (requests.RequestException, OSError):
        if os.path.exists(part):
            try:
                os.remove(part)
            except OSError:
                pass
        return None


# ---------------------------------------------------------------------------
# ledger / dedup state
# ---------------------------------------------------------------------------
class State:
    def __init__(self):
        self.known_ids: set[tuple[str, str]] = set()
        self.known_sha: set[str] = set()
        os.makedirs(LEDGER_DIR, exist_ok=True)
        for fn in os.listdir(LEDGER_DIR):
            if not fn.endswith(".jsonl"):
                continue
            with open(os.path.join(LEDGER_DIR, fn), encoding="utf-8") as f:
                for line in f:
                    try:
                        rec = json.loads(line)
                    except ValueError:
                        continue
                    if rec.get("id") and rec.get("source"):
                        self.known_ids.add((rec["source"], str(rec["id"])))
                    if rec.get("sha256"):
                        self.known_sha.add(rec["sha256"])
        if os.path.isfile(EXISTING_INDEX):
            try:
                idx = json.load(open(EXISTING_INDEX, encoding="utf-8"))
                items = idx if isinstance(idx, list) else idx.get("items", [])
                for rec in items:
                    if isinstance(rec, dict):
                        if rec.get("sha256"):
                            self.known_sha.add(rec["sha256"])
                        if rec.get("id") and rec.get("source"):
                            self.known_ids.add((rec["source"], str(rec["id"])))
            except Exception as e:
                log(f"existing_index.json unreadable: {e!r}")
        log(f"state: {len(self.known_ids)} known ids, {len(self.known_sha)} known sha")

    def has(self, source: str, item_id: str) -> bool:
        return (source, str(item_id)) in self.known_ids

    def add(self, source: str, item_id: str, sha: str | None):
        self.known_ids.add((source, str(item_id)))
        if sha:
            self.known_sha.add(sha)

    def ledger(self, source: str, rec: dict):
        path = os.path.join(LEDGER_DIR, f"{source}.jsonl")
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def reject(self, source: str, item_id: str, reason: str, extra: dict | None = None):
        rec = {"id": item_id, "source": source, "reason": reason,
               "fetched_at": utcnow()}
        if extra:
            rec.update(extra)
        with open(REJECTS_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self.known_ids.add((source, str(item_id)))  # don't retry within/between runs


# ---------------------------------------------------------------------------
# relevance scoring (precision-first)
# ---------------------------------------------------------------------------
def score_item(source: str, query: str, title: str, desc: str) -> tuple[int, list[str]]:
    text = f"{title} {desc}".lower()
    if NEG_RE.search(text):
        return -100, ["<negative>"]
    matched = []
    for tok in {t for t in re.split(r"[^a-z0-9]+", query.lower())
                if t and t not in STOPWORDS}:
        if tok in text or (tok.endswith("s") and tok[:-1] in text) or (tok + "s") in text:
            matched.append(tok)
    return KW_POINTS * len(matched), matched


def accept(source: str, score: int) -> bool:
    return score >= THRESHOLD[source]


# ---------------------------------------------------------------------------
# shelf write (download -> validate -> dedup -> ledger)
# ---------------------------------------------------------------------------
def take_item(st: State, *, source: str, item_id: str, title: str, url: str,
              kind: str, theme: str, source_url: str, license_raw: str,
              license_decision: str, score: int, matched: list[str],
              est_bytes: int = 30 * 1024 * 1024, dry_run=False,
              file_id: str | None = None) -> bool:
    """Returns True if the item landed on the shelf."""
    if dry_run:
        log(f"    DRY {source}/{item_id} score={score} -> {theme} :: {title[:60]}")
        return True
    if license_decision == "review_required":
        root = QUARANTINE
    else:
        root = pick_root(est_bytes)
        if root is None:
            raise StorageFull()
    ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower() or \
        (".jpg" if kind == "image" else ".mp4")
    tdir = os.path.join(root, theme)
    os.makedirs(tdir, exist_ok=True)
    base = shelf_filename(source, file_id or item_id, title, ext)
    dest = os.path.join(tdir, base)
    n_coll = 1
    while os.path.exists(dest):  # collision: append -2, -3, ...
        n_coll += 1
        stem, e = os.path.splitext(base)
        dest = os.path.join(tdir, f"{stem}-{n_coll}{e}")
    n = download(url, dest)
    if n is None or n < MIN_ITEM_BYTES:
        if os.path.exists(dest):
            os.remove(dest)
        st.reject(source, item_id, "download_failed_or_tiny", {"url": url})
        return False
    ok, detail = probe_floors(dest, kind)
    if not ok:
        os.remove(dest)
        st.reject(source, item_id, detail, {"url": url, "bytes": n})
        return False
    sha = sha256_file(dest)
    if sha in st.known_sha:
        os.remove(dest)
        st.reject(source, item_id, "sha_dup", {"sha256": sha})
        return False
    rec = {"id": str(item_id), "source": source, "source_url": source_url,
           "title": title, "license_field_raw": license_raw,
           "license_decision": license_decision, "theme": theme,
           "file_path": dest, "bytes": n, "sha256": sha, "fetched_at": utcnow(),
           "relevance_score": score, "matched_keywords": matched}
    st.ledger(source, rec)
    st.add(source, item_id, sha)
    log(f"    OK  {source}/{item_id} {n/1e6:.1f}MB {detail} -> {dest}")
    return True


class StorageFull(Exception):
    pass


# ---------------------------------------------------------------------------
# source adapters — each returns count of new shelf items
# ---------------------------------------------------------------------------
def run_nasa(st: State, limit: int, dry_run: bool) -> int:
    taken = 0
    for theme, query, media_types in NASA_QUERIES:
        for media_type in media_types.split(","):
            page = 1
            while True:
                if limit and taken >= limit:
                    return taken
                data = get_json("https://images-api.nasa.gov/search", params={
                    "q": query, "media_type": media_type,
                    "page": page, "page_size": 100})
                time.sleep(RATE["nasa"])
                if not data:
                    break
                items = data.get("collection", {}).get("items", [])
                if not items:
                    break
                for it in items:
                    if limit and taken >= limit:
                        return taken
                    meta = (it.get("data") or [{}])[0]
                    nid = meta.get("nasa_id")
                    if not nid or st.has("nasa", nid):
                        continue
                    title = meta.get("title") or nid
                    desc = (meta.get("description") or "") + " " + \
                        " ".join(meta.get("keywords") or [])
                    if "copyright" in desc.lower():
                        st.reject("nasa", nid, "copyright_notice_in_description")
                        continue
                    score, matched = score_item("nasa", query, title, desc)
                    if not accept("nasa", score):
                        st.known_ids.add(("nasa", nid))  # session-only skip
                        continue
                    coll = get_json(
                        f"https://images-assets.nasa.gov/{media_type}/"
                        f"{urllib.parse.quote(nid)}/collection.json")
                    time.sleep(RATE["nasa"])
                    if not coll:
                        continue
                    urls = [u.replace("http://", "https://") for u in coll
                            if isinstance(u, str)]
                    if media_type == "image":
                        prefs = ["~orig.jpg", "~orig.png", "~large.jpg",
                                 "~orig.tif", "~medium.jpg"]
                    else:
                        prefs = ["~orig.mp4", "~large.mp4", "~medium.mp4",
                                 "~mobile.mp4"]
                    url = next((u for p in prefs for u in urls
                                if u.lower().endswith(p)), None)
                    if not url:
                        continue
                    est = 40 << 20 if media_type == "image" else 400 << 20
                    if take_item(
                            st, source="nasa", item_id=nid, title=title, url=url,
                            kind=media_type, theme=theme,
                            source_url=f"https://images.nasa.gov/details/{nid}",
                            license_raw=f"NASA Image and Video Library "
                                        f"(center={meta.get('center', '?')}); "
                                        f"NASA media generally not copyrighted",
                            license_decision="pd", score=score, matched=matched,
                            est_bytes=est, dry_run=dry_run):
                        taken += 1
                total = data.get("collection", {}).get("metadata", {}) \
                    .get("total_hits", 0)
                if page * 100 >= min(total, 10000) or page >= 100:
                    break
                page += 1
        log(f"  nasa [{theme}] '{query}' cumulative taken={taken}")
    return taken


COMMONS_API = "https://commons.wikimedia.org/w/api.php"
PD_LIC_RE = re.compile(r"\b(public domain|pd-|cc0|no restrictions)\b", re.I)


def run_noaa(st: State, limit: int, dry_run: bool) -> int:
    taken = 0
    for theme, query, ftype in NOAA_QUERIES:
        offset = 0
        while True:
            if limit and taken >= limit:
                return taken
            data = get_json(COMMONS_API, params={
                "action": "query", "format": "json", "list": "search",
                "srnamespace": 6, "srlimit": 50, "sroffset": offset,
                "srsearch": f'NOAA {query} filetype:{ftype}'})
            time.sleep(RATE["noaa"])
            if not data or "query" not in data:
                break
            hits = data["query"].get("search", [])
            if not hits:
                break
            titles = [h["title"] for h in hits
                      if not st.has("noaa", h["title"])]
            # batch imageinfo for up to 20 titles at a time
            for i in range(0, len(titles), 20):
                batch = titles[i:i + 20]
                if not batch:
                    continue
                info = get_json(COMMONS_API, params={
                    "action": "query", "format": "json",
                    "titles": "|".join(batch), "prop": "imageinfo",
                    "iiprop": "url|size|mime|extmetadata"})
                time.sleep(RATE["noaa"])
                if not info:
                    continue
                for page_obj in info.get("query", {}).get("pages", {}).values():
                    if limit and taken >= limit:
                        return taken
                    ftitle = page_obj.get("title", "")
                    ii = (page_obj.get("imageinfo") or [{}])[0]
                    if not ii.get("url"):
                        continue
                    em = ii.get("extmetadata", {})

                    def emv(k):
                        return re.sub(r"<[^>]+>", " ",
                                      str(em.get(k, {}).get("value", "")))
                    lic = f"{emv('LicenseShortName')} | {emv('License')}"
                    credit = f"{emv('Credit')} {emv('Artist')}"
                    desc = emv("ImageDescription")
                    if not PD_LIC_RE.search(lic):
                        st.known_ids.add(("noaa", ftitle))
                        continue  # PD/CC0 only for this shelf
                    if "noaa" not in (credit + " " + ftitle + " " + desc).lower():
                        st.known_ids.add(("noaa", ftitle))
                        continue  # source purity: NOAA-credited only
                    score, matched = score_item("noaa", query, ftitle, desc)
                    if not accept("noaa", score):
                        st.known_ids.add(("noaa", ftitle))
                        continue
                    kind = "video" if ii.get("mime", "").startswith("video") \
                        else "image"
                    if kind == "image" and \
                            max(ii.get("width", 0), ii.get("height", 0)) < \
                            MIN_IMAGE_LONG_SIDE:
                        st.known_ids.add(("noaa", ftitle))
                        continue
                    dec = "cc0" if re.search(r"cc0", lic, re.I) else "pd"
                    if take_item(
                            st, source="noaa", item_id=ftitle,
                            file_id=os.path.splitext(
                                ftitle.replace("File:", ""))[0],
                            title=os.path.splitext(
                                ftitle.replace("File:", ""))[0],
                            url=ii["url"], kind=kind, theme=theme,
                            source_url=ii.get("descriptionurl", ""),
                            license_raw=lic.strip(), license_decision=dec,
                            score=score, matched=matched,
                            est_bytes=ii.get("size", 20 << 20),
                            dry_run=dry_run):
                        taken += 1
            offset += 50
            if offset >= data["query"].get("searchinfo", {}).get("totalhits", 0) \
                    or offset >= 5000:
                break
        log(f"  noaa [{theme}] '{query}' ({ftype}) cumulative taken={taken}")
    return taken


def run_met(st: State, limit: int, dry_run: bool) -> int:
    taken = 0
    base = "https://collectionapi.metmuseum.org/public/collection/v1"
    for theme, query in MET_QUERIES:
        data = get_json(f"{base}/search",
                        params={"q": query, "hasImages": "true"})
        time.sleep(RATE["met"])
        ids = (data or {}).get("objectIDs") or []
        for oid in ids:
            if limit and taken >= limit:
                return taken
            if st.has("met", oid):
                continue
            obj = get_json(f"{base}/objects/{oid}")
            time.sleep(RATE["met"])
            if not obj:
                continue
            if not obj.get("isPublicDomain") or not obj.get("primaryImage"):
                st.known_ids.add(("met", str(oid)))
                continue
            title = obj.get("title") or f"met_{oid}"
            desc = " ".join(str(obj.get(k) or "") for k in
                            ("objectName", "medium", "culture", "period",
                             "artistDisplayName", "classification")) + " " + \
                " ".join(t.get("term", "") for t in (obj.get("tags") or []))
            score, matched = score_item("met", query, title, desc)
            if not accept("met", score):
                st.known_ids.add(("met", str(oid)))
                continue
            if take_item(
                    st, source="met", item_id=oid, title=title,
                    url=obj["primaryImage"], kind="image", theme=theme,
                    source_url=obj.get("objectURL", ""),
                    license_raw="isPublicDomain=true (Met Open Access CC0)",
                    license_decision="cc0", score=score, matched=matched,
                    est_bytes=25 << 20, dry_run=dry_run):
                taken += 1
        log(f"  met [{theme}] '{query}' ({len(ids)} candidates) "
            f"cumulative taken={taken}")
    return taken


def run_smithsonian(st: State, limit: int, dry_run: bool) -> int:
    key = os.environ.get("DATA_GOV_API_KEY") or \
        os.environ.get("SMITHSONIAN_API_KEY")
    if not key:
        log("  smithsonian: NO KEY (DATA_GOV_API_KEY / SMITHSONIAN_API_KEY) "
            "-> skipped; see OWNER KEY LIST")
        return 0
    taken = 0
    base = "https://api.si.edu/openaccess/api/v1.0/search"
    for theme, query in SMITHSONIAN_QUERIES:
        start = 0
        while True:
            if limit and taken >= limit:
                return taken
            data = get_json(base, params={
                "api_key": key, "q": f'{query} AND online_media_type:"Images"',
                "start": start, "rows": 100})
            time.sleep(RATE["smithsonian"])
            rows = (data or {}).get("response", {}).get("rows", [])
            if not rows:
                break
            for row in rows:
                if limit and taken >= limit:
                    return taken
                rid = row.get("id")
                if not rid or st.has("smithsonian", rid):
                    continue
                content = row.get("content", {})
                dnr = content.get("descriptiveNonRepeating", {})
                media = dnr.get("online_media", {}).get("media", [])
                cc0 = [m for m in media
                       if (m.get("usage", {}).get("access") == "CC0"
                           and m.get("type") == "Images")]
                if not cc0:
                    st.known_ids.add(("smithsonian", rid))
                    continue
                url = cc0[0].get("content") or cc0[0].get("idsId")
                if not url or not str(url).startswith("http"):
                    continue
                title = row.get("title") or rid
                desc = json.dumps(content.get("freetext", {}))[:2000]
                score, matched = score_item("smithsonian", query, title, desc)
                if not accept("smithsonian", score):
                    st.known_ids.add(("smithsonian", rid))
                    continue
                if take_item(
                        st, source="smithsonian", item_id=rid, title=title,
                        url=url, kind="image", theme=theme,
                        source_url=dnr.get("record_link", "") or
                        dnr.get("guid", ""),
                        license_raw="online_media usage.access=CC0",
                        license_decision="cc0", score=score, matched=matched,
                        est_bytes=25 << 20, dry_run=dry_run):
                    taken += 1
            start += 100
            if start >= (data or {}).get("response", {}).get("rowCount", 0):
                break
        log(f"  smithsonian [{theme}] '{query}' cumulative taken={taken}")
    return taken


def run_nypl(st: State, limit: int, dry_run: bool) -> int:
    token = os.environ.get("NYPL_API_TOKEN")
    if not token:
        log("  nypl: NO KEY (NYPL_API_TOKEN) -> skipped; see OWNER KEY LIST")
        return 0
    taken = 0
    hdrs = {"Authorization": f'Token token="{token}"'}
    for theme, query in NYPL_QUERIES:
        page = 1
        while True:
            if limit and taken >= limit:
                return taken
            data = get_json(
                "https://api.repo.nypl.org/api/v2/items/search",
                params={"q": query, "publicDomainOnly": "true",
                        "page": page, "per_page": 50}, headers=hdrs)
            time.sleep(RATE["nypl"])
            resp = (data or {}).get("nyplAPI", {}).get("response", {})
            results = resp.get("result", [])
            if isinstance(results, dict):
                results = [results]
            if not results:
                break
            for res in results:
                if limit and taken >= limit:
                    return taken
                uuid = res.get("uuid")
                if not uuid or st.has("nypl", uuid):
                    continue
                title = res.get("title") or uuid
                score, matched = score_item("nypl", query, title, "")
                if not accept("nypl", score):
                    st.known_ids.add(("nypl", uuid))
                    continue
                img_id = res.get("imageID")
                if not img_id:
                    continue
                url = (f"https://images.nypl.org/index.php?id={img_id}&t=g")
                if take_item(
                        st, source="nypl", item_id=uuid, title=title, url=url,
                        kind="image", theme=theme,
                        source_url=res.get("itemLink", ""),
                        license_raw="publicDomainOnly=true (NYPL)",
                        license_decision="pd", score=score, matched=matched,
                        est_bytes=15 << 20, dry_run=dry_run):
                    taken += 1
            total = int(resp.get("numResults", 0) or 0)
            if page * 50 >= total:
                break
            page += 1
        log(f"  nypl [{theme}] '{query}' cumulative taken={taken}")
    return taken


def run_rawpixel(st: State, limit: int, dry_run: bool) -> int:
    # No official API. Probe their internal search endpoint once; it is
    # Cloudflare-protected (403 for non-browser clients as of 2026-07).
    probe = get("https://www.rawpixel.com/api/v1/search",
                params={"freecc0": 1, "page": 1, "pagesize": 5}, tries=1)
    if probe is None or probe.status_code != 200:
        code = probe.status_code if probe is not None else "conn_error"
        log(f"  rawpixel: search endpoint not accessible ({code}); no bulk "
            f"API and Cloudflare bot protection -> skipped (curated manual "
            f"pulls only, per source policy)")
        return 0
    taken = 0
    try:
        for theme, query in RAWPIXEL_QUERIES:
            data = get_json("https://www.rawpixel.com/api/v1/search",
                            params={"freecc0": 1, "query": query,
                                    "page": 1, "pagesize": 20})
            time.sleep(RATE["rawpixel"])
            results = (data or {}).get("results", [])
            for res in results:
                if taken >= (limit or 60):  # small curated pulls only
                    return taken
                rid = str(res.get("id", ""))
                if not rid or st.has("rawpixel", rid):
                    continue
                lic = str(res.get("metadata", {}).get("licenses", "")) or \
                    str(res.get("license", ""))
                if not re.search(r"cc0|public", lic, re.I):
                    continue
                url = res.get("image_opengraph") or res.get("image_1300")
                if not url:
                    continue
                title = res.get("image_title") or res.get("name") or rid
                score, matched = score_item("rawpixel", query, title, "")
                if not accept("rawpixel", score):
                    continue
                if take_item(
                        st, source="rawpixel", item_id=rid, title=title,
                        url=url, kind="image", theme=theme,
                        source_url=res.get("url", ""),
                        license_raw=lic, license_decision="cc0",
                        score=score, matched=matched, dry_run=dry_run):
                    taken += 1
    except Exception as e:
        log(f"  rawpixel: aborted ({e!r})")
    return taken


ADAPTERS = {"nasa": run_nasa, "noaa": run_noaa, "met": run_met,
            "smithsonian": run_smithsonian, "nypl": run_nypl,
            "rawpixel": run_rawpixel}


# ---------------------------------------------------------------------------
def load_env():
    envp = os.path.join(REPO, ".env")
    if os.path.isfile(envp):
        for line in open(envp, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--source", default="all",
                    help=f"comma list or 'all' ({','.join(MY_SOURCES)})")
    ap.add_argument("--limit", type=int, default=0,
                    help="max NEW shelf items per source (0 = unlimited)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    load_env()
    os.makedirs(QUARANTINE, exist_ok=True)
    sources = MY_SOURCES if args.source == "all" else \
        [s.strip() for s in args.source.split(",") if s.strip() in MY_SOURCES]
    st = State()
    log(f"=== ingest_science_museum start sources={sources} "
        f"limit={args.limit or 'NONE'} dry_run={args.dry_run} ===")
    for t in TIERS:
        log(f"tier {t['name']}: free={free_bytes(t['drive'])/GB:.0f}GB "
            f"floor={t['floor']/GB:.0f}GB")
    totals = {}
    for src in sources:
        log(f"--- source: {src} ---")
        t0 = time.time()
        try:
            totals[src] = ADAPTERS[src](st, args.limit, args.dry_run)
        except StorageFull:
            log(f"!!! storage floors hit during {src}; stopping run")
            totals[src] = "storage_full"
            break
        except Exception as e:
            log(f"!!! {src} crashed: {e!r}")
            totals[src] = f"error:{e!r}"
        log(f"--- {src} done: {totals[src]} new items "
            f"in {(time.time()-t0)/60:.1f} min ---")
    log(f"=== finished: {totals} ===")


if __name__ == "__main__":
    main()
