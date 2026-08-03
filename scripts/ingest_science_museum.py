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
import shutil
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone

import requests

# --- framework v5 primitives (CONTRACT.md 4-v3/v5, 2, 5) -------------------
# Imported, NOT forked: term_hits/sense_ok/validate_media/atomic_append are the
# shared reference implementations, so future fixes to the boundary rule, sense
# guards and source-aware floors land here automatically. Only the QUERY-based
# scorer below is local (this adapter scores query->item, while the framework's
# relevance() scores theme-table->item).
os.environ.setdefault("PD_INGEST_LANE", "sci")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ingest_archive_sources import (  # noqa: E402
    WEAK_TERMS, SENSE_GUARDS, ARCHIVAL_SOURCES, term_hits, sense_ok,
    validate_media, atomic_append, reject_log as fw_reject_log)

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

MY_SOURCES = ["nasa", "noaa", "met", "smithsonian", "nypl", "rawpixel", "wikimedia"]
LANE = os.environ.get("PD_INGEST_LANE", "sci")

UA = "PrimeDocumentaryIngest/1.0 (archival research; contact: aab153792@gmail.com)"
MAX_ITEM_BYTES = 2 * GB
MIN_ITEM_BYTES = 15 * 1024
MIN_IMAGE_LONG_SIDE = 1200
MIN_VIDEO_HEIGHT = 480

RATE = {"nasa": 0.8, "noaa": 1.0, "met": 0.4, "smithsonian": 1.0, "wikimedia": 1.0,
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
# CONTRACT §4.1: metadata-rich archives >= 30. Every source in this lane is a
# metadata-rich archive. 30 is also what makes the weak-only cap (4-v5-j) bite:
# weak common words cap at 15 and can therefore never clear the gate, while ONE
# strong domain term (+30, 4-v3-e) still passes without lowering the threshold.
THRESHOLD = {"nasa": 30, "noaa": 30, "met": 30, "smithsonian": 30, "nypl": 30, "wikimedia": 30,
             "rawpixel": 30}

# ---------------------------------------------------------------------------
# themed query plans: (theme, query, extra) per source
# ---------------------------------------------------------------------------
# Theme gating (2026-08-01). The owner's directive is to download material that is
# actually usable, and the contact-sheet review measured what is not: noaa's
# weather_disasters slice is 4,856 items / ~360 GB of straight-down flood-survey plates
# that are 85-90% dead weight as b-roll, while the SAME source's ocean_nature and
# wildlife_animals slices graded good. So the filter is per-theme, not per-source.
ONLY_THEMES: set[str] = set()
SKIP_THEMES: set[str] = set()


def theme_allowed(theme: str) -> bool:
    if ONLY_THEMES and theme not in ONLY_THEMES:
        return False
    return theme not in SKIP_THEMES


# NASA video is switched off (2026-08-01). Measured: 626 clips = 318 GB = 90% of
# everything nasa has fetched, and the clips are launch broadcasts, ISO b-roll strings,
# crew training in Kazakhstan and "Space to Ground" news episodes, averaging 508 MB.
# None of that cuts into an episode about a wrongful conviction. The 6,681 stills cost
# 36.7 GB total and DO earn their place — Earth from orbit, city lights at night and
# launch frames work as establishing and transition beats. So: stills yes, video no.
NASA_QUERIES = [
    # (theme, query, media_types)
    ("space_nasa", "nebula", "image"),
    ("space_nasa", "galaxy", "image"),
    ("space_nasa", "earth from space", "image"),
    ("space_nasa", "rocket launch", "image"),
    ("space_nasa", "international space station", "image"),
    ("space_nasa", "moon surface", "image"),
    ("space_nasa", "mars surface", "image"),
    ("space_nasa", "solar flare", "image"),
    ("space_nasa", "aurora", "image"),
    ("space_nasa", "spacewalk", "image"),
    ("space_nasa", "saturn rings", "image"),
    ("space_nasa", "jupiter", "image"),
    ("space_nasa", "apollo lunar surface", "image"),
    ("space_nasa", "satellite orbit", "image"),
    ("space_nasa", "space shuttle launch", "image"),
    ("weather_disasters", "hurricane from space", "image"),
    ("weather_disasters", "typhoon satellite", "image"),
    ("weather_disasters", "wildfire smoke satellite", "image"),
    ("weather_disasters", "storm system", "image"),
    ("weather_disasters", "dust storm satellite", "image"),
    ("ocean_nature", "ocean from space", "image"),
    ("ocean_nature", "phytoplankton bloom", "image"),
    ("ocean_nature", "coral reef", "image"),
    ("ocean_nature", "sea ice", "image"),
    ("science_tech", "wind tunnel", "image"),
    ("science_tech", "laboratory research", "image"),
    ("science_tech", "robotics", "image"),
    ("science_tech", "mission control", "image"),
    ("science_tech", "supercomputer", "image"),
    ("science_tech", "clean room spacecraft", "image"),
    ("science_tech", "telescope", "image"),
    ("landscapes_timelapse", "earth time lapse", "image"),
    ("landscapes_timelapse", "city lights at night", "image"),
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


def probe_floors(path: str, kind: str, theme: str,
                 source: str) -> tuple[str, str]:
    """SOURCE-AWARE technical floors (CONTRACT §2). Returns (verdict, detail)
    where verdict is "ok" | "reject" | "quarantine".

    Every source in this lane is archival (NASA/NOAA/Met/Smithsonian/NYPL), so
    sub-SD historical footage is QUARANTINED for owner review, never deleted —
    a technical floor must not destroy what the relevance gate just approved.
    Delegates to the shared validate_media() so floor policy stays in one place.
    """
    verdict, reason = validate_media(path, kind, theme, source)
    info = ffprobe(path)
    dims = ""
    if info:
        vs = [s for s in info.get("streams", []) if s.get("codec_type") == "video"]
        if vs:
            dims = (f"{max(int(s.get('width') or 0) for s in vs)}x"
                    f"{max(int(s.get('height') or 0) for s in vs)}")
    return verdict, (dims if verdict == "ok" and dims else reason)


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
        self.session_skip: set[tuple[str, str]] = set()  # relevance rejects, this run
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
        key = (source, str(item_id))
        return key in self.known_ids or key in self.session_skip

    def add(self, source: str, item_id: str, sha: str | None):
        self.known_ids.add((source, str(item_id)))
        if sha:
            self.known_sha.add(sha)

    def ledger(self, source: str, rec: dict):
        path = os.path.join(LEDGER_DIR, f"{source}.jsonl")
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # Terminal reasons blacklist an id permanently; a RELEVANCE reject must not,
    # or a future gate improvement can never re-admit it (CONTRACT 4-v3-h: the
    # resumable run is what re-evaluates false negatives organically).
    RELEVANCE_REASONS = ("title-irrelevant", "relevance<", "negative")

    def reject(self, source: str, item_id: str, reason: str, extra: dict | None = None,
               *, title: str = "", theme: str = "", score: int = -1,
               matched=None, negs=None):
        """Per-lane, atomically-appended reject row (CONTRACT §5).

        TITLE IS REQUIRED: without reject titles the false-negative direction of
        the gate is invisible — that is what hid prime material until 4-v3-g.
        """
        fw_reject_log(source, item_id, theme, reason, score=score,
                      matched=matched, negs=negs, title=title)
        if extra:  # keep lane-specific diagnostics (urls, dims) alongside
            atomic_append(os.path.join(LEDGER_DIR, f"rejects_{LANE}_detail.jsonl"),
                          json.dumps({"ts": utcnow(), "source": source,
                                      "id": str(item_id)[:200], "title": title[:300],
                                      "reason": reason, **extra}, ensure_ascii=False))
        if any(reason.startswith(r) for r in self.RELEVANCE_REASONS):
            self.session_skip.add((source, str(item_id)))  # this run only
        else:
            self.known_ids.add((source, str(item_id)))  # terminal: never retry


# ---------------------------------------------------------------------------
# relevance scoring (precision-first)
# ---------------------------------------------------------------------------
# Latin plurals the shared suffix rule does not cover (nebula->nebulae). Kept as
# explicit aliases rather than a blanket optional "e", which would let "car"
# match "care". Alias hits count as the base term.
LATIN_PLURAL = {"nebula": "nebulae", "aurora": "aurorae", "supernova": "supernovae",
                "larva": "larvae", "alga": "algae", "formula": "formulae",
                "antenna": "antennae"}

# STRONG bigrams / unmistakable domain terms for THIS lane's themes (CONTRACT
# 4-v5-k: ambiguity is per-WORD — "ocean"/"storm"/"space" are weak alone, but
# "coral reef"/"solar flare"/"space shuttle" are unmistakable subject matter).
STRONG_EXTRA_SCI: dict[str, list[str]] = {
    "space_nasa": ["nebula", "galaxy", "spacewalk", "spacecraft", "orbiter",
                   "apollo", "gemini", "cosmonaut", "launchpad", "space shuttle",
                   "space station", "rocket launch", "solar flare", "lunar surface",
                   "mars surface", "saturn rings", "earth from space", "satellite orbit",
                   "international space station", "aurora", "moon surface"],
    "weather_disasters": ["hurricane", "typhoon", "tornado", "waterspout", "cyclone",
                          "wildfire", "blizzard", "lightning", "dust storm",
                          "storm system", "storm clouds", "hurricane damage"],
    # single words that are unmistakable SUBJECT matter for this shelf even though
    # the framework's generic WEAK_TERMS marks them weak (4-v3-e allows per-theme
    # STRONG_EXTRA): a bare "reef"/"coral" photo is exactly what ocean_nature is.
    "ocean_nature": ["coral reef", "phytoplankton", "hydrothermal vent", "kelp forest",
                     "submersible", "deep sea", "sea ice", "research vessel",
                     "ocean waves", "seascape", "coral", "reef", "atoll", "lagoon"],
    "wildlife_animals": ["whale", "dolphin", "seabird", "sea turtle", "shark",
                         "butterfly", "kelp", "seal", "fish school", "bird study",
                         "animal study", "bird specimen"],
    "science_tech": ["wind tunnel", "mission control", "supercomputer", "telescope",
                     "clean room", "robotics", "microscope", "telegraph", "sundial",
                     "celestial globe", "scientific instrument", "weather balloon",
                     "radar dome", "laboratory research", "rocket engine"],
    "laboratory_forensics": ["forensic", "spectrometer", "centrifuge", "petri",
                             "microscope", "chemistry laboratory", "crime lab"],
    "landscapes_timelapse": ["glacier", "arctic ice", "river delta", "time lapse",
                             "coastline", "lighthouse", "city lights", "hudson river",
                             "mountain landscape", "landscape painting"],
    "textures_backgrounds": ["marbled paper", "textile fragment", "wallpaper design",
                             "ornament pattern", "embroidery", "gold decorative"],
    "americana_1930s_1970s": ["american city", "main street", "courthouse", "courtroom",
                              "allegory of justice", "new york street", "wall street"],
}


def query_terms(query: str) -> list[str]:
    """Query split into scoreable terms: the full phrase (strong, per 4-v5-k)
    plus its individual words minus stopwords."""
    words = [t for t in dict.fromkeys(re.split(r"[^a-z0-9]+", query.lower()))
             if t and t not in STOPWORDS]
    phrase = " ".join(w for w in re.split(r"[^a-z0-9]+", query.lower())
                      if w and w not in STOPWORDS)
    terms = list(words)
    if " " in phrase and phrase not in terms:
        terms.insert(0, phrase)
    return terms


def term_weight_sci(theme: str, term: str) -> int:
    """+30 unambiguous domain term (ONE clears the threshold), +15 weak common word.

    CONTRACT 4-v3-e / 4-v5-j-k. Multi-word terms are strong by construction.
    """
    t = term.lower()
    if " " in t or t in STRONG_EXTRA_SCI.get(theme, []):
        return 30
    # WEAK_TERMS lists singulars; a plural query word ("lights", "clouds") is the
    # same weak common word and must not score 30 by escaping the lookup.
    variants = {t, t[:-1] if t.endswith("s") else t + "s"}
    if t.endswith("es"):
        variants.add(t[:-2])
    return 15 if variants & WEAK_TERMS else 30


def _hits(term: str, text: str) -> bool:
    """Framework both-end boundary + sense guards, plus this lane's Latin plurals."""
    if term_hits(term, text) and sense_ok(term, text):
        return True
    alt = LATIN_PLURAL.get(term)
    return bool(alt) and term_hits(alt, text) and sense_ok(term, text)


def score_item(source: str, query: str, title: str, desc: str,
               theme: str = "") -> tuple[int, list[str], str | None]:
    """Returns (score, matched_keywords, reject_reason|None).

    CONTRACT 4-v3/v5 applied to this lane's query-based matching:
      * both-end word boundaries + sense guards (imported term_hits/sense_ok)
      * TITLE-relevance gate: >=1 positive term must appear in the TITLE
      * strong-term weighting (+30) so one unambiguous term clears the threshold
      * WEAK-ONLY CAP at 15: weak common words alone can never clear the gate
    """
    title = title or ""
    text = f"{title} {desc or ''}"
    low, t_low = text.lower(), title.lower()
    if NEG_RE.search(text):
        return -100, ["<negative>"], "negative"
    matched = [t for t in query_terms(query) if _hits(t, low)]
    title_hits = [t for t in matched if _hits(t, t_low)]
    score = min(60, sum(term_weight_sci(theme, t) for t in matched))
    # weak-only cap (4-v5-j): without >=1 strong term, weak words cannot reach 30
    if matched and not any(term_weight_sci(theme, t) >= 30 for t in matched):
        score = min(score, 15)
    if score >= THRESHOLD[source] and not title_hits:
        return score, matched, "title-irrelevant"
    return score, matched, None


def accept(source: str, score: int) -> bool:
    return score >= THRESHOLD[source]


# ---------------------------------------------------------------------------
# shelf write (download -> validate -> dedup -> ledger)
# ---------------------------------------------------------------------------
def take_item(st: State, *, source: str, item_id: str, title: str, url: str,
              kind: str, theme: str, source_url: str, license_raw: str,
              license_decision: str, score: int, matched: list[str],
              est_bytes: int = 30 * 1024 * 1024, dry_run=False,
              file_id: str | None = None, force_ext: str | None = None) -> bool:
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
    ext = force_ext or os.path.splitext(urllib.parse.urlparse(url).path)[1].lower() or \
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
        st.reject(source, item_id, "download-fail:empty-or-tiny", {"url": url},
                  title=title, theme=theme, score=score, matched=matched)
        return False
    verdict, detail = probe_floors(dest, kind, theme, source)
    if verdict == "quarantine":
        # CONTRACT §2: a technical floor must NEVER destroy what the relevance
        # gate approved. Sub-SD archival material goes to owner review instead.
        qdir = os.path.join(QUARANTINE, theme)
        os.makedirs(qdir, exist_ok=True)
        qdest = os.path.join(qdir, os.path.basename(dest))
        # Cross-device move: the shelf lives on D:/E:/F: but quarantine is ALWAYS on H:
        # (CONTRACT 1), and os.replace cannot cross a Windows volume — it raises
        # OSError 18 (EXDEV). That killed the whole source: the noaa lane died on its
        # first sub-floor TIF and stayed dead for 18 hours while its siblings ran on.
        shutil.move(dest, qdest)
        dest, license_decision = qdest, "review_required"
        log(f"    QUAR {source}/{item_id} {detail} -> {qdest}")
    elif verdict != "ok":
        os.remove(dest)
        st.reject(source, item_id, f"tech:{detail}", {"url": url, "bytes": n},
                  title=title, theme=theme, score=score, matched=matched)
        return False
    sha = sha256_file(dest)
    if sha in st.known_sha:
        os.remove(dest)
        st.reject(source, item_id, "dup-sha256", {"sha256": sha},
                  title=title, theme=theme, score=score, matched=matched)
        return False
    rec = {"id": str(item_id), "source": source, "source_url": source_url,
           "title": title, "license_field_raw": license_raw,
           "license_decision": license_decision, "theme": theme,
           "file_path": dest, "bytes": n, "sha256": sha, "fetched_at": utcnow(),
           "relevance_score": score, "matched_keywords": matched}
    if verdict == "quarantine":
        rec["quarantine_reason"] = detail
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
        if not theme_allowed(theme):
            continue
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
                        st.reject("nasa", nid, "license:copyright-notice",
                              title=title, theme=theme)
                        continue
                    score, matched, why = score_item("nasa", query, title, desc,
                                                     theme)
                    if why or not accept("nasa", score):
                        st.reject("nasa", nid, why or "relevance<30", title=title,
                                  theme=theme, score=score, matched=matched)
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
        if not theme_allowed(theme):
            continue
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
                    score, matched, why = score_item("noaa", query, ftitle, desc,
                                                     theme)
                    if why or not accept("noaa", score):
                        st.reject("noaa", ftitle, why or "relevance<30", title=ftitle,
                                  theme=theme, score=score, matched=matched)
                        st.known_ids.add(("noaa", ftitle))
                        continue
                    kind = "video" if ii.get("mime", "").startswith("video") \
                        else "image"
                    iw, ih = ii.get("width", 0), ii.get("height", 0)
                    if kind == "image":
                        # pre-download floor (saves the fetch); archival images keep
                        # the 1200px floor per CONTRACT §2, 1920 for textures.
                        floor = 1920 if theme == "textures_backgrounds" else \
                            MIN_IMAGE_LONG_SIDE
                        if max(iw, ih) < floor:
                            st.reject("noaa", ftitle,
                                      f"tech:image-below-{floor}px({max(iw, ih)})",
                                      title=ftitle, theme=theme, score=score,
                                      matched=matched)
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
        if not theme_allowed(theme):
            continue
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
            score, matched, why = score_item("met", query, title, desc, theme)
            if why or not accept("met", score):
                st.reject("met", oid, why or "relevance<30", title=title,
                          theme=theme, score=score, matched=matched)
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
        if not theme_allowed(theme):
            continue
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
                score, matched, why = score_item("smithsonian", query, title, desc,
                                                 theme)
                if why or not accept("smithsonian", score):
                    st.reject("smithsonian", rid, why or "relevance<30", title=title,
                              theme=theme, score=score, matched=matched)
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
        if not theme_allowed(theme):
            continue
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
                score, matched, why = score_item("nypl", query, title, "", theme)
                if why or not accept("nypl", score):
                    st.reject("nypl", uuid, why or "relevance<30", title=title,
                              theme=theme, score=score, matched=matched)
                    st.known_ids.add(("nypl", uuid))
                    continue
                img_id = res.get("imageID")
                if not img_id:
                    continue
                # IIIF pre-check: read the TRUE master size before downloading.
                # images.nypl.org?t=g 404s whenever the master is small, which
                # burned a slow request per item; info.json is ~0.3s and also
                # lets us reject below-floor scans without any download. We take
                # full/full (native size) — NYPL's IIIF supports sizeAboveFull
                # but that is upscaling, never real detail, so we never use it.
                info = get_json(
                    f"https://iiif.nypl.org/iiif/2/{urllib.parse.quote(str(img_id))}"
                    f"/info.json", tries=1, timeout=30)
                time.sleep(RATE["nypl"])
                if not info:
                    st.reject("nypl", uuid, "download-fail:iiif-info-unavailable",
                              {"image_id": img_id}, title=title, theme=theme,
                              score=score, matched=matched)
                    continue
                iw, ih = int(info.get("width") or 0), int(info.get("height") or 0)
                if max(iw, ih) < MIN_IMAGE_LONG_SIDE:
                    st.reject("nypl", uuid,
                              f"tech:image-below-{MIN_IMAGE_LONG_SIDE}px"
                              f"({max(iw, ih)})", {"image_id": img_id},
                              title=title, theme=theme, score=score,
                              matched=matched)
                    continue
                url = (f"https://iiif.nypl.org/iiif/2/"
                       f"{urllib.parse.quote(str(img_id))}/full/full/0/default.jpg")
                if take_item(
                        st, source="nypl", item_id=uuid, title=title, url=url,
                        kind="image", theme=theme, force_ext=".jpg",
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
            if not theme_allowed(theme):
                continue
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
                score, matched, why = score_item("rawpixel", query, title, "", theme)
                if why or not accept("rawpixel", score):
                    st.reject("rawpixel", rid, why or "relevance<30", title=title,
                              theme=theme, score=score, matched=matched)
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


# Wikimedia Commons (added 2026-08-03 for Prime Finance / Prime Business).
# Measured before building: Openverse caps anonymous use at 200 requests a day, which is
# 4,000 items and seven days to fill one channel, and its shelf-eligible slice is only the
# cc0/pdm licences. Commons has no such cap and its finance/industry holdings are deep.
# What it does NOT have is video - "filetype:video stock exchange" returns 45 files, mostly
# foreign listing ceremonies - so this adapter asks for bitmaps only and the video shortfall
# stays with the stock lanes.
# Licence policy is stricter than the API's: CONTRACT 3 puts CC-BY in quarantine, so rather
# than fetch and quarantine at volume, only extmetadata License in {pd, cc0} is downloaded.
WIKIMEDIA_QUERIES = [
    # Second wave (2026-08-03). The stock lanes exhausted at 118 queries; Commons has no
    # such ceiling and no API key, so depth here is the cheapest remaining supply. Two-word
    # heads chosen deliberately - the adapter searches on the first two words.
    ("factory_manufacturing", "steel works"),
    ("factory_manufacturing", "iron foundry"),
    ("factory_manufacturing", "shipbuilding yard"),
    ("factory_manufacturing", "locomotive works"),
    ("factory_manufacturing", "cotton mill"),
    ("factory_manufacturing", "flour mill"),
    ("factory_manufacturing", "sugar refinery"),
    ("factory_manufacturing", "brick works"),
    ("factory_manufacturing", "glass works"),
    ("factory_manufacturing", "paper mill"),
    ("factory_manufacturing", "tannery workers"),
    ("factory_manufacturing", "printing works"),
    ("factory_manufacturing", "automobile plant"),
    ("factory_manufacturing", "aircraft factory"),
    ("factory_manufacturing", "munitions factory"),
    ("factory_manufacturing", "power station"),
    ("factory_manufacturing", "oil refinery"),
    ("factory_manufacturing", "coal mine"),
    ("factory_manufacturing", "quarry workers"),
    ("goods_in_motion", "goods yard"),
    ("goods_in_motion", "freight depot"),
    ("goods_in_motion", "dock workers"),
    ("goods_in_motion", "harbour crane"),
    ("goods_in_motion", "cargo hold"),
    ("goods_in_motion", "canal barge"),
    ("goods_in_motion", "grain elevator"),
    ("goods_in_motion", "delivery wagon"),
    ("goods_in_motion", "mail sorting"),
    ("goods_in_motion", "railway station platform"),
    ("retail_commerce", "general store"),
    ("retail_commerce", "market hall"),
    ("retail_commerce", "butcher shop"),
    ("retail_commerce", "bakery shop"),
    ("retail_commerce", "pharmacy interior"),
    ("retail_commerce", "hardware store"),
    ("retail_commerce", "shopping arcade"),
    ("retail_commerce", "street market"),
    ("retail_commerce", "advertising billboard"),
    ("retail_commerce", "shop assistant"),
    ("bank_and_branch", "savings bank"),
    ("bank_and_branch", "banking hall"),
    ("bank_and_branch", "money changer"),
    ("bank_and_branch", "pawn shop"),
    ("bank_and_branch", "insurance office"),
    ("stock_market_exchange", "commodity exchange"),
    ("stock_market_exchange", "corn exchange"),
    ("stock_market_exchange", "wool exchange"),
    ("stock_market_exchange", "financial district"),
    ("stock_market_exchange", "wall street"),
    ("money_banking", "gold mining"),
    ("money_banking", "coin collection"),
    ("money_banking", "paper money"),
    ("money_banking", "tax office"),
    ("decision_rooms", "trade union"),
    ("decision_rooms", "labour strike"),
    ("decision_rooms", "workers meeting"),
    ("decision_rooms", "company office"),
    ("decision_rooms", "typing pool"),
    ("business_corporate", "telephone exchange operators"),
    ("business_corporate", "counting house"),
    ("business_corporate", "drawing office"),
    ("business_corporate", "warehouse office"),
    ("economy_crisis", "abandoned factory"),
    ("economy_crisis", "derelict mill"),
    ("economy_crisis", "empty shop"),
    ("economy_crisis", "ghost town"),
    ("household_loss", "tenement housing"),
    ("household_loss", "slum housing"),
    ("household_loss", "rationing queue"),
    ("household_loss", "pawnbroker window"),
    ("depression_hardship", "bread line unemployed"),
    ("depression_hardship", "soup kitchen depression"),
    ("depression_hardship", "hooverville shacks"),
    ("depression_hardship", "migrant worker family farm security"),
    ("depression_hardship", "sharecropper cabin"),
    ("depression_hardship", "unemployed men street"),
    ("depression_hardship", "dust bowl farm abandoned"),
    ("depression_hardship", "works progress administration workers"),
    ("stock_market_exchange", "stock exchange trading floor"),
    ("stock_market_exchange", "new york stock exchange interior"),
    ("stock_market_exchange", "stock ticker machine"),
    ("stock_market_exchange", "board of trade pit"),
    ("stock_market_exchange", "brokerage office customers"),
    ("stock_market_exchange", "stock certificate"),
    ("bank_and_branch", "bank teller window"),
    ("bank_and_branch", "bank interior counter"),
    ("bank_and_branch", "bank vault door"),
    ("bank_and_branch", "bank run depositors crowd"),
    ("bank_and_branch", "savings bank passbook"),
    ("money_banking", "banknote printing press"),
    ("money_banking", "coin minting press"),
    ("money_banking", "gold bullion bars"),
    ("money_banking", "treasury building exterior"),
    ("factory_manufacturing", "assembly line automobile factory"),
    ("factory_manufacturing", "steel mill blast furnace"),
    ("factory_manufacturing", "textile mill spinning"),
    ("factory_manufacturing", "foundry molten metal pouring"),
    ("factory_manufacturing", "machine shop lathe workers"),
    ("factory_manufacturing", "cannery production line women"),
    ("factory_manufacturing", "factory smokestacks industrial"),
    ("factory_manufacturing", "shipyard workers welding"),
    ("factory_manufacturing", "coal miners underground"),
    ("retail_commerce", "department store interior"),
    ("retail_commerce", "grocery store shelves interior"),
    ("retail_commerce", "shop window display"),
    ("retail_commerce", "market stall vendor"),
    ("retail_commerce", "five and ten cent store"),
    ("retail_commerce", "supermarket checkout"),
    ("goods_in_motion", "longshoremen loading cargo"),
    ("goods_in_motion", "railroad freight yard"),
    ("goods_in_motion", "warehouse goods stacked"),
    ("goods_in_motion", "cargo ship dock crane"),
    ("goods_in_motion", "truck loading dock freight"),
    ("decision_rooms", "boardroom meeting table"),
    ("decision_rooms", "labor strike picket line"),
    ("decision_rooms", "shareholders meeting hall"),
    ("decision_rooms", "employment office men waiting"),
    ("business_corporate", "office clerks typing pool"),
    ("business_corporate", "adding machine bookkeeping"),
    ("business_corporate", "punch card tabulating machine"),
    ("business_corporate", "office building interior desks"),
    ("economy_crisis", "closed factory abandoned"),
    ("economy_crisis", "farm foreclosure auction"),
    ("economy_crisis", "eviction furniture sidewalk"),
    ("economy_crisis", "boarded storefront closed"),
]
WM_API = "https://commons.wikimedia.org/w/api.php"
# Painting / print / sculpture markers. Kept narrow: "portrait" and "collection" are
# deliberately absent because they appear on genuine press photography too.
ARTWORK_RE = re.compile(
    r"\b(oil on canvas|painting|painted by|lithograph|engraving|etching|watercolou?r|"
    r"drawing|sketch|woodcut|aquatint|mezzotint|sculpture|statue|art institute|"
    r"kunstmuseum|mnar|national gallery|museum of art|art museum|"
    r"\bmet dp\d|artwork|illustration by)\b", re.I)
WM_MAX_PER_QUERY = 1000         # 55 queries x 1000 = 55,000 candidates before filtering


def run_wikimedia(st: State, limit: int, dry_run: bool) -> int:
    taken = 0
    for theme, query in WIKIMEDIA_QUERIES:
        if not theme_allowed(theme):
            continue
        offset, seen_titles = 0, []
        while offset < WM_MAX_PER_QUERY:
            # Search on the first two words, score on the full phrase. Commons ANDs every
            # term, so the precise phrasing that makes a good relevance query makes a
            # terrible search: "bread line unemployed" finds 7 files, "bread line" finds
            # 2,648; "assembly line automobile factory" 41 against 18,245. Cast wide here
            # and let score_item's title gate do the discriminating.
            broad = " ".join(query.split()[:2])
            data = get_json(WM_API, params={
                "action": "query", "format": "json", "list": "search",
                "srsearch": f"filetype:bitmap {broad}", "srlimit": 50,
                "sroffset": offset, "srnamespace": 6})
            time.sleep(RATE["wikimedia"])
            hits = ((data or {}).get("query") or {}).get("search") or []
            if not hits:
                break
            seen_titles += [h["title"] for h in hits]
            offset += 50
        # imageinfo takes up to 50 titles at once - one request per 25 keeps URLs short
        for i in range(0, len(seen_titles), 25):
            batch = [t for t in seen_titles[i:i + 25] if not st.has("wikimedia", t)]
            if not batch:
                continue
            info = get_json(WM_API, params={
                "action": "query", "format": "json", "prop": "imageinfo",
                "iiprop": "url|size|extmetadata", "titles": "|".join(batch)})
            time.sleep(RATE["wikimedia"])
            pages = ((info or {}).get("query") or {}).get("pages") or {}
            for page in pages.values():
                if limit and taken >= limit:
                    return taken
                title = page.get("title", "")
                ii = (page.get("imageinfo") or [{}])[0]
                url = ii.get("url")
                if not url:
                    continue
                em = ii.get("extmetadata") or {}
                lic = str((em.get("License") or {}).get("value", "")).lower().strip()
                lic_name = str((em.get("LicenseShortName") or {}).get("value", ""))
                if lic not in ("pd", "cc0"):
                    st.reject("wikimedia", title, f"license-not-shelf-eligible:{lic or 'unknown'}",
                              title=title, theme=theme, score=-1, matched=[])
                    st.known_ids.add(("wikimedia", title))
                    continue
                desc = re.sub(r"<[^>]+>", " ",
                              str((em.get("ImageDescription") or {}).get("value", "")))
                cats = str((em.get("Categories") or {}).get("value", ""))
                hay = f"{title} {desc} {cats}".lower()
                # The phrase we actually searched for has to be IN the file. Searching two
                # words to get volume let "Bread-rolls.jpg" in on the word "bread" alone;
                # requiring "bread line" keeps the Bowery photographs and drops the bakery.
                if broad.lower() not in hay.replace("-", " "):
                    st.reject("wikimedia", title, f"phrase-absent:{broad}", title=title,
                              theme=theme, score=-1, matched=[])
                    st.known_ids.add(("wikimedia", title))
                    continue
                # Commons is half museum. A painting OF a bread line is not a record of
                # one, and the owner's earlier verdict on met was explicit: artwork scans
                # are unusable for these channels.
                if ARTWORK_RE.search(hay):
                    st.reject("wikimedia", title, "artwork-not-photograph", title=title,
                              theme=theme, score=-1, matched=[])
                    st.known_ids.add(("wikimedia", title))
                    continue
                score, matched, why = score_item("wikimedia", query, title,
                                                 f"{desc} {cats}", theme)
                if why or not accept("wikimedia", score):
                    st.reject("wikimedia", title, why or "relevance<30", title=title,
                              theme=theme, score=score, matched=matched)
                    st.known_ids.add(("wikimedia", title))
                    continue
                if take_item(
                        st, source="wikimedia", item_id=title, title=title,
                        url=url, kind="image", theme=theme,
                        source_url=f"https://commons.wikimedia.org/wiki/{title.replace(' ', '_')}",
                        license_raw=f"{lic_name} (extmetadata License={lic})",
                        license_decision="cc0" if lic == "cc0" else "pd",
                        score=score, matched=matched,
                        est_bytes=ii.get("size") or (12 << 20), dry_run=dry_run):
                    taken += 1
        log(f"  wikimedia [{theme}] '{query}' ({len(seen_titles)} candidates) "
            f"cumulative taken={taken}")
    return taken


ADAPTERS = {"nasa": run_nasa, "noaa": run_noaa, "met": run_met,
            "wikimedia": run_wikimedia,
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
    ap.add_argument("--theme", default="",
                    help="comma list: ingest ONLY these themes")
    ap.add_argument("--skip-theme", default="",
                    help="comma list: skip these themes (e.g. weather_disasters)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    global ONLY_THEMES, SKIP_THEMES
    ONLY_THEMES = {t.strip() for t in args.theme.split(",") if t.strip()}
    SKIP_THEMES = {t.strip() for t in args.skip_theme.split(",") if t.strip()}
    if ONLY_THEMES or SKIP_THEMES:
        log(f"theme gate: only={sorted(ONLY_THEMES) or 'all'} skip={sorted(SKIP_THEMES) or 'none'}")

    load_env()
    os.makedirs(QUARANTINE, exist_ok=True)
    sources = MY_SOURCES if args.source == "all" else \
        [s.strip() for s in args.source.split(",") if s.strip() in MY_SOURCES]
    st = State()
    log(f"=== ingest_science_museum start sources={sources} "
        f"limit={args.limit or 'NONE'} dry_run={args.dry_run} ===")
    # CODE FINGERPRINT: a running process does not announce its code version, so a
    # worker launched before a fix keeps executing stale code invisibly (the IA
    # lane burned 40 minutes that way). Log file mtime+sha1 for THIS module AND the
    # imported framework so any log line can be tied to the code that produced it.
    import hashlib
    for tag, path in (("lane", os.path.abspath(__file__)),
                      ("framework", os.path.join(REPO, "scripts",
                                                 "ingest_archive_sources.py"))):
        try:
            raw = open(path, "rb").read()
            log(f"CODE: {tag}={os.path.basename(path)} "
                f"mtime={datetime.fromtimestamp(os.path.getmtime(path)).isoformat(timespec='seconds')} "
                f"sha1={hashlib.sha1(raw).hexdigest()[:12]} bytes={len(raw)}")
        except OSError as e:
            log(f"CODE: {tag} fingerprint unavailable ({e})")
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
