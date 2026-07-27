# -*- coding: utf-8 -*-
"""
GOV-ARCHIVES ingest adapter: NARA + Library of Congress + UK National Archives.

Companion to scripts/ingest_archive_sources.py (the shared-framework ingester run
by the foundation agent). This adapter owns the three government-archive sources
and is safe to run concurrently with it: both write per-source JSONL ledgers into
the same H: ledger directory and both dedup on (source, id) + sha256 across ALL
ledgers found there (this script additionally re-reads sibling ledgers
incrementally during long runs).

Sources (all keyless; verified live 2026-07-27):
    nara  National Archives (US). The keyed api/v2 path serves the SPA HTML to
          anonymous clients, but the catalog website's own public backend
          `catalog.archives.gov/proxy/records/search` returns identical v2 JSON
          without a key. CloudFront intermittently answers with the SPA HTML on
          a pooled connection — so NARA requests use a FRESH connection each
          time plus a JSON-body guard with backoff retries (measured 8/8 OK).
          License: useRestriction "Unrestricted" -> pd (US federal record);
          anything else / missing -> review_required (quarantine).
    loc   Library of Congress loc.gov JSON API (fo=json). Rights text gated:
          "public domain" -> pd, "no known restrictions" -> free_commercial,
          else review_required. Film/video mp4 derivatives + IIIF pct:100 stills.
    ukna  UK National Archives Discovery API. VERIFIED METADATA-ONLY: the full
          endpoint list at /API/v1/docs contains search/records/fileauthorities/
          repository routes and NO media or download endpoint; digitised-record
          downloads go through the website basket (bot-gated, paid). Therefore
          this adapter ships ZERO media files and instead records digitised open
          TNA candidates (id, reference, dates, OGL attribution text) into
          `_ledger/ukna_candidates.jsonl` for a future keyed/manual route.
          OGL v3.0 attribution text is recorded per candidate.

Storage contract (owner directives, binding):
    media       E:\\pd-archive\\<theme>\\           HARD STOP if E: free < 250GB
    quarantine  H:\\pd-media\\assets\\archive\\_quarantine\\<theme>\\  (review_required)
    ledgers     H:\\pd-media\\assets\\archive\\_ledger\\{nara,loc,ukna}.jsonl
    log         H:\\pd-media\\assets\\archive\\_ledger\\ingest_gov.log  (--log-file)
    C: is never written (repo code excepted).

Ledger JSONL schema (one object per line):
    {id, source, source_url, title, license_field_raw,
     license_decision (pd|cc0|free_commercial|review_required), theme, file_path,
     bytes, sha256, fetched_at, relevance_score, matched_keywords}
    (+ attribution_text on UKNA/OGL rows.)
    Aligned with _ledger/CONTRACT.md v1 (2026-07-27): schema field names, filename
    convention (§4b), reject reasons (§5), 3-layer dedup incl. existing_index.json
    shape + mtime reload + retroactive sha sweep (§6), QC contact sheets (§7).

Filename convention (owner directive 2026-07-27, applied from first download):
    <source>__<id>__<title-slug>.<ext>
    ASCII slug of the title, lowercase-hyphens, max 60 chars; collisions -2, -3...
    e.g. nara__98765-1__pacific-fleet-norfolk-harbor-1944.mp4

Per-item vetting order (precision over recall; rejects -> _ledger/rejects.jsonl):
    1. resume/dedup skip on (source, id) across ALL ledgers + existing_index.json
    2. soft real-person filter on the title (environmental scenery preferred)
    3. metadata relevance score 0-100 vs theme keyword/negative sets (gate >= 30)
    4. drive floors (E: 250GB shelf / H: 500GB quarantine)
    5. download (2GB single-file cap) -> sha256 content dedup
    6. technical floors via ffprobe/PIL: video decodes, >=480p (720p derivative
       preferred at selection time), 5s-30min; images decode, long edge >=1200px.
       Corrupt/short/small files are deleted and logged.

Politeness: <=1 request/s per API host (www.loc.gov 2s), streaming downloads,
contact e-mail in the User-Agent. Resumable at any point; the run may span days.

Usage:
    py -3.11 scripts/ingest_gov_archives.py --source nara --theme courtroom_justice --limit 2 --passes 1
    py -3.11 scripts/ingest_gov_archives.py --source all --theme all --log-file H:\\pd-media\\assets\\archive\\_ledger\\ingest_gov.log
    py -3.11 scripts/ingest_gov_archives.py --sweep-existing-index   # retroactive sha sweep
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
import unicodedata
import urllib.parse
from datetime import datetime, timezone

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

GB = 1024 ** 3

SHELF_ROOT = r"E:\pd-archive"
SHELF_DRIVE = "E:\\"
SHELF_FLOOR = 250 * GB                      # owner hard guard: stop below this
H_ARCHIVE = r"H:\pd-media\assets\archive"
LEDGER_DIR = os.path.join(H_ARCHIVE, "_ledger")
QUARANTINE = os.path.join(H_ARCHIVE, "_quarantine")
QUAR_DRIVE = "H:\\"
QUAR_FLOOR = 500 * GB                       # matches the shared framework's H: floor
CONTRACT_MD = os.path.join(LEDGER_DIR, "CONTRACT.md")
EXISTING_INDEX = os.path.join(LEDGER_DIR, "existing_index.json")   # CONTRACT §6.3
CANDIDATES_PATH = os.path.join(LEDGER_DIR, "ukna_candidates.jsonl")

UA = "PrimeDocumentaryIngest/1.0 (archival research; contact: aab153792@gmail.com)"  # CONTRACT §8
MAX_ITEM_BYTES = 2 * GB
MIN_ITEM_BYTES = 20 * 1024
DEFAULT_THRESHOLD = 30                      # relevance gate (tuned for precision)
LEDGER_REFRESH_S = 120                      # re-read sibling ledgers this often
EMPTY_PASS_STOP = 4                         # consecutive empty passes = exhausted
QC_SHEET_EVERY = 500                        # CONTRACT §7: contact sheet cadence
QC_SHEET_TILES = 60
QC_DIR = os.path.join(H_ARCHIVE, "_qc")
NARA_VIDEO_PER_RECORD = 2                   # reels per moving-image record
NARA_IMAGES_PER_RECORD = 4                  # scans per photographic record

# per-host politeness (seconds between requests; <=1 req/s everywhere)
HOST_INTERVAL = {
    "www.loc.gov": 2.0, "tile.loc.gov": 1.0,
    "catalog.archives.gov": 1.0,
    "discovery.nationalarchives.gov.uk": 1.0,
}
DEFAULT_INTERVAL = 1.0
# hosts that need a fresh TCP connection per request (NARA CloudFront serves the
# SPA HTML instead of JSON on pooled connections — measured 0/6 pooled, 8/8 fresh)
FRESH_HOSTS = {"catalog.archives.gov"}

OGL_ATTRIBUTION = ("Contains public sector information licensed under the Open "
                   "Government Licence v3.0. Source: The National Archives (UK), {ref}.")

LOG_FILE = ""   # set from --log-file
PASS = 1        # current runner pass == page number of each paginated source

# soft real-person filter (channel policy: environmental/period scenery preferred)
# Two-part filter. Part 1 is plain phrase matching (case-insensitive). Part 2
# catches "<honorific> <Name>" — the honorific is case-insensitive but the name
# must be Capitalised, so the case-sensitive part cannot be folded into re.I.
# Place-name words after an honorific (King Street, General Store, Queen's Park)
# are excluded so UK/small-town scenery is not lost to the soft bias.
_HONORIFIC = (r"president|vice president|first lady|prince|princess|king|queen|"
              r"duke|duchess|senator|congressman|governor|ambassador|admiral|"
              r"mayor|chief justice|dr|mr|mrs|miss")
_NOT_A_NAME = (r"Street|St\b|Road|Rd\b|Lane|Square|Avenue|Ave\b|Store|Stores|"
               r"Motors|Hospital|Park|Bridge|Building|Buildings|Theatre|Theater|"
               r"Hotel|Cross|County|City|Docks|Dock|Wharf|Harbour|Harbor|Hall|"
               r"House|Palace|Highway|Hill|Gate|Yard|Works|School|College|Church")
PERSON_RE = re.compile(
    r"(?i:\b(portrait|portraits|interview|interviews|mugshot|mug shot|headshot|"
    r"testimony of|speech by|press conference|remarks (at|to|by|in|on)|"
    r"address (to|by) the|visit (of|by) (the )?(president|prince|princess|king|"
    r"queen|secretary))\b)"
    r"|\bclose-up of [A-Z]"
    # honorific + Capitalised name, unless a place word sits before OR after the
    # name ("King Street", "Queen Victoria Street" -> scenery, not a person)
    # \b after the name prevents [a-z]+ from backtracking past the lookahead
    rf"|(?i:\b({_HONORIFIC})\b)\.? (?!(?:{_NOT_A_NAME})\b)[A-Z][a-z]+\b"
    rf"(?!\s+(?:{_NOT_A_NAME})\b)")

# negative keywords: talking-head/junk formats and archival document scans that
# make no b-roll (gov catalogs are full of textual case files with jpg scans)
GLOBAL_NEG = [
    "lecture", "slideshow", "seminar", "webinar", "sermon", "podcast",
    "interview", "portrait", "mugshot", "headshot",
    "docket", "transcript of", "petition for", "muster roll", "index to",
    "census schedule", "pension file", "affidavit", "deposition",
    # person-focused political footage (identifiable-individual soft bias)
    "president", "vice president", "first lady", "senator", "congressman",
    "remarks", "swearing-in",
]
STOPWORDS = set("the a an of in on and or for with to at from by 1930s 1940s "
                "1950s 1960s 1970s old new view views scene scenes".split())

# ---------------------------------------------------------------- themes ----
# Queries are environmental/period-scenery biased. "video"/"image" feed NARA
# (typeOfMaterials-filtered) and LOC (online-format-filtered); "ukna" feeds the
# Discovery candidates lane; "kw" adds positive relevance terms; "neg" adds
# theme-local negative terms.
THEMES: dict[str, dict[str, list[str]]] = {
    "courtroom_justice": {
        "video": ["courtroom", "courthouse", "trial court"],
        "image": ["courtroom interior", "courthouse building", "county courthouse"],
        "kw": ["judge", "gavel", "justice", "judicial", "tribunal", "verdict",
               "sentencing", "jury", "prosecution", "defendant", "war crimes trial"],
        # non-courtroom senses of the strong term "trial" / of "court"
        "neg": ["tennis court", "basketball court", "squash court", "courtyard",
                "trial run", "clinical trial", "field trial", "sea trial",
                "trial flight", "test trial"],
    },
    "prison_jail": {
        "video": ["prison", "penitentiary", "jail"],
        "image": ["prison cell block", "penitentiary building", "county jail building"],
        "kw": ["cell", "inmate", "warden", "reformatory", "correctional"],
        "neg": [],
    },
    "police_period": {
        "video": ["police patrol", "police department", "traffic police"],
        "image": ["police station", "police patrol wagon", "police call box"],
        "kw": ["patrolman", "precinct", "constable", "squad car"],
        "neg": [],
    },
    "americana_1930s_1970s": {
        "video": ["main street", "county fair", "drive-in theater", "soda fountain",
                  "railroad depot"],
        "image": ["main street storefronts", "diner neon sign", "gas station 1950",
                  "railroad steam locomotive"],
        "kw": ["diner", "storefront", "jukebox", "roadside", "downtown", "depot"],
        "neg": [],
    },
    "small_town": {
        "video": ["small town", "rural town street", "village main street"],
        "image": ["small town main street", "town square", "general store", "water tower town"],
        "kw": ["courthouse square", "church", "barbershop", "hardware store"],
        "neg": [],
    },
    "newspapers_printing": {
        "video": ["newspaper printing", "printing press", "newspaper plant"],
        "image": ["printing press machinery", "linotype machine", "newsboy newspapers"],
        "kw": ["linotype", "typesetting", "pressroom", "newsprint", "composing room"],
        "neg": [],
    },
    "war_history": {
        "video": ["combat film", "military training film", "invasion landing",
                  "aircraft carrier operations"],
        "image": ["tanks advancing", "warplanes formation", "artillery battery",
                  "troops landing craft"],
        "kw": ["infantry", "battalion", "bomber", "battlefield", "convoy", "wartime"],
        "neg": [],
    },
    "government_buildings": {
        "video": ["capitol building", "federal building", "washington monuments"],
        "image": ["united states capitol", "supreme court building", "state capitol dome",
                  "city hall building"],
        "kw": ["capitol", "dome", "columns", "facade", "federal", "courthouse"],
        "neg": [],
    },
    "chicago_city": {
        "video": ["chicago street", "chicago elevated"],
        "image": ["chicago skyline", "chicago river bridges", "chicago elevated railway"],
        "kw": ["chicago", "loop", "michigan avenue", "lakefront", "stockyards"],
        "neg": [],
    },
    "navy_harbor": {
        "video": ["navy ships harbor", "naval shipyard", "fleet at anchor"],
        "image": ["navy warship harbor", "shipyard cranes", "battleship deck",
                  "harbor docks cargo"],
        "kw": ["destroyer", "cruiser", "drydock", "pier", "anchorage", "tugboat"],
        "neg": [],
    },
    "period_telephone_tech": {
        "video": ["telephone switchboard", "telephone exchange", "telegraph office"],
        "image": ["telephone switchboard operators", "telephone lineman poles",
                  "telegraph equipment"],
        "kw": ["switchboard", "rotary", "operator", "bell system", "telegraph"],
        "neg": [],
    },
    "money_banking": {
        "video": ["bank vault", "bureau engraving printing money", "stock exchange"],
        "image": ["bank building", "bank vault door", "printing currency",
                  "treasury building"],
        "kw": ["currency", "mint", "teller", "vault", "treasury", "dollar"],
        "neg": ["river bank", "banks of the"],
    },
    "world_cities": {
        "video": ["city street traffic", "aerial view city", "harbor city skyline"],
        "image": ["city skyline aerial", "european city street", "city market street"],
        "kw": ["boulevard", "skyline", "plaza", "rooftops", "metropolis"],
        "neg": [],
    },
    "japan": {
        "video": ["japan city street", "tokyo street", "japanese village"],
        "image": ["tokyo street", "japan temple", "mount fuji", "japanese harbor"],
        "kw": ["japan", "japanese", "tokyo", "kyoto", "osaka", "yokohama"],
        "neg": [],
    },
    "uk_highstreet_postoffice": {
        "video": ["london street scene", "england village street"],
        "image": ["london shops street", "england post office", "english village high street"],
        "ukna": ["high street", "post office", "village shop front"],
        "kw": ["high street", "post office", "postbox", "shopfront", "village",
               "london", "england", "british"],
        "neg": [],
    },
    "uk_period": {
        "video": ["london street", "england railway station", "british industry film"],
        "image": ["london street 1940", "british railway station", "england town street"],
        "ukna": ["street scene photograph", "railway station photograph", "london photographs"],
        "kw": ["london", "england", "britain", "british", "railway", "underground",
               "thames"],
        "neg": [],
    },
}
NARA_THEMES = set(THEMES) - {"uk_highstreet_postoffice"}   # NARA is US-centric
LOC_THEMES = set(THEMES)
UKNA_THEMES = {t for t, cfg in THEMES.items() if cfg.get("ukna")}

_theme_terms_cache: dict[str, tuple[set[str], list[str]]] = {}


def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    if LOG_FILE:
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except OSError:
            pass


def theme_terms(theme: str) -> tuple[set[str], list[str]]:
    """(positive term set, full query phrases) from the theme's queries + kw."""
    if theme not in _theme_terms_cache:
        cfg = THEMES[theme]
        phrases: list[str] = []
        terms: set[str] = set()
        for key in ("video", "image", "ukna"):
            for q in cfg.get(key, []):
                phrases.append(q.lower())
                terms |= {w for w in re.findall(r"[a-z]+", q.lower())
                          if w not in STOPWORDS and len(w) > 2}
        for kw in cfg.get("kw", []):
            phrases.append(kw.lower())
            terms |= {w for w in re.findall(r"[a-z]+", kw.lower())
                      if w not in STOPWORDS and len(w) > 2}
        _theme_terms_cache[theme] = (terms, phrases)
    return _theme_terms_cache[theme]


# Unambiguous, high-signal terms: ONE of these identifies the theme on its own
# (an archival title reading "WAR CRIMES TRIALS, NUREMBERG" is courtroom footage
# even though it matches a single keyword). Scored +30 instead of +15 so a lone
# strong term reaches the contract's >=30 archive threshold without lowering it.
# Measured need: 61 of 220 courtroom rejects were genuine trial footage at s=15.
STRONG_TERMS: dict[str, set[str]] = {
    "courtroom_justice": {"courtroom", "courthouse", "trial", "tribunal",
                          "verdict", "jury", "judiciary"},
    "prison_jail": {"prison", "penitentiary", "jail", "inmate", "reformatory",
                    "cellblock", "correctional"},
    "police_period": {"police", "patrolman", "constable", "precinct"},
    "newspapers_printing": {"linotype", "printing", "newsroom", "pressroom",
                            "newspaper"},
    "government_buildings": {"capitol", "courthouse", "statehouse"},
    "navy_harbor": {"shipyard", "harbor", "harbour", "drydock", "battleship",
                    "destroyer"},
    "period_telephone_tech": {"switchboard", "telegraph", "telephone"},
    "money_banking": {"vault", "mint", "treasury", "currency"},
    "chicago_city": {"chicago"},
    "japan": {"japan", "japanese", "tokyo", "kyoto", "yokohama"},
    "newspapers": set(),
    "war_history": {"battlefield", "artillery", "infantry", "bombardment"},
    "small_town": {"village"},
    "americana_1930s_1970s": {"storefront", "diner"},
    "uk_highstreet_postoffice": {"postbox", "high street", "post office"},
    "uk_period": {"london", "britain", "england"},
    "world_cities": {"skyline"},
}


def relevance(theme: str, text: str) -> tuple[int, list[str], list[str]]:
    """Score 0-100 from metadata text vs theme keywords (same formula as the
    shared framework: +15/distinct positive term cap 60, +25 full phrase,
    -25 per negative hit). Returns (score, matched_keywords, negative_hits)."""
    low = (text or "").lower()
    pos, phrases = theme_terms(theme)
    # NOTE: a leading-only \b (as in the shared framework) makes "court" match
    # "courtesy"/"courtyard" and silently admits off-theme items at exactly the
    # threshold. Anchor both ends, allowing plural/possessive suffixes.
    strong = STRONG_TERMS.get(theme, set())
    matched = sorted({t for t in pos | strong
                      if re.search(rf"\b{re.escape(t)}(?:s|es|'s)?\b", low)})
    score = min(60, sum(30 if t in strong else 15 for t in matched))
    if any(p in low for p in phrases):
        score += 25
    negs = [n for n in GLOBAL_NEG + THEMES[theme].get("neg", []) if n in low]
    score -= 25 * len(negs)
    return max(0, min(100, score)), matched, negs


def reject_log(source: str, item_id: str, theme: str, reason: str,
               score: int = -1, matched=None, negs=None, title: str = "") -> None:
    """Compact per-item rejects log (skips never enter the media ledgers).
    CONTRACT §5 fields plus `title` — without it, tuning a threshold means
    re-querying the APIs to find out what was actually thrown away."""
    try:
        os.makedirs(LEDGER_DIR, exist_ok=True)
        rec = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "source": source, "id": str(item_id)[:200], "theme": theme,
               "reason": reason, "score": score,
               "matched": matched or [], "neg": negs or []}
        if title:
            rec["title"] = title[:200]
        with open(os.path.join(LEDGER_DIR, "rejects.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass


# ------------------------------------------------------------- plumbing ----


class Net:
    """Polite HTTP: per-host rate limit, fresh-connection hosts, JSON guard."""

    def __init__(self) -> None:
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self._last: dict[str, float] = {}

    def _wait(self, url: str) -> None:
        host = urllib.parse.urlparse(url).netloc
        interval = HOST_INTERVAL.get(host, DEFAULT_INTERVAL)
        dt = time.time() - self._last.get(host, 0.0)
        if dt < interval:
            time.sleep(interval - dt)
        self._last[host] = time.time()

    def get(self, url: str, **kw) -> requests.Response:
        self._wait(url)
        kw.setdefault("timeout", 60)
        host = urllib.parse.urlparse(url).netloc
        if host in FRESH_HOSTS:
            headers = dict(self.s.headers)
            headers.update(kw.pop("headers", {}) or {})
            headers["Connection"] = "close"
            headers.setdefault("Accept", "application/json")
            return requests.get(url, headers=headers, **kw)
        return self.s.get(url, **kw)

    def get_json(self, url: str, retries: int = 3, **kw):
        """GET expecting a JSON body. Two retryable failure modes seen live:
        NARA's CloudFront serving the SPA HTML with HTTP 200, and loc.gov
        dropping connections mid-response (IncompleteRead)."""
        delay = 3.0
        last = ""
        for attempt in range(retries + 1):
            try:
                r = self.get(url, **kw)
                body = r.text.lstrip()
                if r.status_code == 200 and body.startswith(("{", "[")):
                    return r.json()
                last = f"HTTP {r.status_code} body[:40]={body[:40]!r}"
            except requests.RequestException as e:
                last = f"{e.__class__.__name__}: {str(e)[:120]}"
            if attempt < retries:
                time.sleep(delay)
                delay = min(delay * 2.5, 30.0)
        raise RuntimeError(f"no JSON after {retries + 1} tries: {url} ({last})")

    def download(self, url: str, dest: str, retries: int = 2) -> tuple[int, str]:
        """Stream url -> dest (atomic .part rename). Returns (bytes, sha256).
        Transient transport failures are retried from scratch (partial file
        discarded) so a multi-day run is not derailed by flaky connections."""
        last: Exception | None = None
        for attempt in range(retries + 1):
            self._wait(url)
            h = hashlib.sha256()
            n = 0
            tmp = dest + ".part"
            try:
                with self.s.get(url, stream=True, timeout=600) as r:
                    r.raise_for_status()
                    with open(tmp, "wb") as f:
                        for chunk in r.iter_content(1024 * 512):
                            f.write(chunk)
                            h.update(chunk)
                            n += len(chunk)
                            if n > MAX_ITEM_BYTES:
                                raise ValueError(f"file exceeds MAX_ITEM_BYTES: {url}")
                os.replace(tmp, dest)
                return n, h.hexdigest()
            except (requests.RequestException, OSError) as e:
                last = e
                if os.path.exists(tmp):
                    try:
                        os.remove(tmp)
                    except OSError:
                        pass
                if attempt < retries:
                    time.sleep(5.0 * (attempt + 1))
        raise last if last else RuntimeError(f"download failed: {url}")


NET = Net()


def title_slug(text: str, maxlen: int = 60) -> str:
    """ASCII lowercase-hyphen slug per the 2026-07-27 filename directive."""
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    text = re.sub(r"-{2,}", "-", text)
    return (text[:maxlen].rstrip("-")) or "untitled"


def id_slug(item_id: str) -> str:
    """CONTRACT §4b: ids get the same slugification as titles (LOC ids are URLs
    -> path tail first), no trim beyond 60."""
    s = str(item_id).rstrip("/")
    if s.startswith("http"):
        s = urllib.parse.urlparse(s).path.rstrip("/").rsplit("/", 1)[-1]
    s = title_slug(s, 60)
    return s if s != "untitled" else hashlib.sha1(str(item_id).encode()).hexdigest()[:16]


def dest_filename(root: str, source: str, item_id: str, title: str, ext: str) -> str:
    """<source>__<id>__<title-slug>.<ext>, collisions get -2, -3, ..."""
    base = f"{source}__{id_slug(item_id)}__{title_slug(title)}"
    dest = os.path.join(root, f"{base}.{ext}")
    k = 2
    while os.path.exists(dest) or os.path.exists(dest + ".part"):
        dest = os.path.join(root, f"{base}-{k}.{ext}")
        k += 1
    return dest


def ext_of(url: str, default: str) -> str:
    path = urllib.parse.urlparse(url).path
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    return ext if ext and len(ext) <= 4 else default


def drive_free(drive: str) -> int:
    try:
        return shutil.disk_usage(drive).free
    except Exception:
        return 0


def ffprobe_json(path: str) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
        capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout or "{}")


def validate_media(path: str, kind: str) -> tuple[bool, str]:
    """Technical floors. video: decodes, >=480p, 5s..30min. image: decodes,
    long edge >=1200px. Returns (ok, reason)."""
    try:
        if os.path.getsize(path) < MIN_ITEM_BYTES:
            return False, "too-small-file"
        if kind == "video":
            info = ffprobe_json(path)
            heights = [int(s.get("height", 0) or 0) for s in info.get("streams", [])
                       if s.get("codec_type") == "video"]
            if not heights or max(heights) < 480:
                return False, f"video-below-480p({max(heights) if heights else 0})"
            dur = float(info.get("format", {}).get("duration", 0) or 0)
            if dur < 5:
                return False, f"video-too-short({dur:.1f}s)"
            if dur > 1800:
                return False, f"video-too-long({dur/60:.0f}min)"
            return True, "ok"
        if kind == "image":
            from PIL import Image
            with Image.open(path) as im:
                im.verify()
            with Image.open(path) as im:
                long_edge = max(im.size)
            if long_edge < 1200:
                return False, f"image-below-1200px({long_edge})"
            return True, "ok"
        return False, f"unknown-kind:{kind}"
    except Exception as e:  # noqa: BLE001
        return False, f"decode-fail:{e.__class__.__name__}"


def build_contact_sheet(theme: str, files: list[str], count: int) -> None:
    """CONTRACT §7 sampled human QC: 6-col grid jpg (videos contribute one
    extracted frame) into H:\\...\\_qc\\<theme>\\sheet_<n>.jpg."""
    try:
        from PIL import Image
        qc_dir = os.path.join(QC_DIR, theme)
        os.makedirs(qc_dir, exist_ok=True)
        cell_w, cell_h, cols = 320, 180, 6
        tiles = []
        for fp in files[:QC_SHEET_TILES]:
            try:
                ext = os.path.splitext(fp)[1].lower()
                if ext in (".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".webp"):
                    im = Image.open(fp).convert("RGB")
                elif ext in (".mp4", ".mov", ".webm", ".mkv", ".avi", ".mpg"):
                    tmp = fp + ".qcframe.jpg"
                    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "3", "-i", fp,
                                    "-frames:v", "1", "-vf", f"scale={cell_w}:-2", tmp],
                                   capture_output=True, timeout=60)
                    if not os.path.exists(tmp):
                        continue
                    im = Image.open(tmp).convert("RGB")
                    os.remove(tmp)
                else:
                    continue
                im.thumbnail((cell_w, cell_h))
                tiles.append(im)
            except Exception:
                continue
        if not tiles:
            return
        rows = (len(tiles) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (16, 16, 16))
        for i, im in enumerate(tiles):
            sheet.paste(im, ((i % cols) * cell_w, (i // cols) * cell_h))
        out = os.path.join(qc_dir, f"sheet_{count:06d}.jpg")
        sheet.save(out, quality=82)
        log(f"  QC contact sheet written: {out} ({len(tiles)} tiles)")
    except Exception as e:  # noqa: BLE001
        log(f"  QC sheet fail ({theme}): {e}")


def retro_sha_sweep(index_shas: set[str]) -> int:
    """CONTRACT §6.3 retroactive sweep: delete this lane's already-kept files
    whose sha256 is in existing_index.json; tombstone in gov_dedup_removed.jsonl,
    log reason dup_existing_retro_sha, rewrite the ledgers atomically."""
    removed = 0
    if not index_shas:
        return 0
    for src in ADAPTERS:
        path = os.path.join(LEDGER_DIR, f"{src}.jsonl")
        if not os.path.exists(path):
            continue
        keep: list[str] = []
        hit = False
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except Exception:
                    keep.append(line)
                    continue
                if rec.get("sha256") in index_shas:
                    fp = rec.get("file_path") or ""
                    if fp and os.path.exists(fp):
                        try:
                            os.remove(fp)
                        except OSError:
                            keep.append(line)
                            continue
                    rec["removed_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
                    rec["removed_reason"] = "dup_existing_retro_sha"
                    with open(os.path.join(LEDGER_DIR, "gov_dedup_removed.jsonl"),
                              "a", encoding="utf-8") as t:
                        t.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    reject_log(src, rec.get("id", "?"), rec.get("theme", "?"),
                               "dup_existing_retro_sha")
                    removed += 1
                    hit = True
                else:
                    keep.append(line)
        if hit:
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                f.writelines(keep)
            os.replace(tmp, path)
    return removed


class Ledger:
    """Resume/dedup state across ALL per-source ledgers on H: (+ the
    existing_index.json holdings index, CONTRACT §6), with periodic incremental
    re-reads so long concurrent runs by sibling agents stay deduplicated."""

    def __init__(self) -> None:
        os.makedirs(LEDGER_DIR, exist_ok=True)
        self.done: set[tuple[str, str]] = set()
        self.shas: set[str] = set()
        self.index_ids: set[str] = set()     # existing_index "source:id" keys
        self.index_shas: set[str] = set()    # existing_index sha256 values
        self.offsets: dict[str, int] = {}
        self.run_items = 0
        self.run_bytes = 0
        self.theme_items: dict[str, int] = {}
        self.theme_bytes: dict[str, int] = {}
        self.theme_total: dict[str, int] = {}    # cumulative gov-lane kept/theme (QC)
        self.recent: dict[str, list[str]] = {}   # recent kept files/theme (QC sheets)
        self._last_refresh = 0.0
        self._index_mtime = -1.0
        self._tomb_offset = 0
        self.refresh(force=True)
        self.load_tombstones()
        self.load_existing_index()

    def _absorb(self, rec: dict) -> None:
        src = rec.get("source")
        if src:
            self.done.add((src, str(rec.get("id"))))
            if src in ADAPTERS:
                self.theme_total[rec.get("theme", "?")] = \
                    self.theme_total.get(rec.get("theme", "?"), 0) + 1
        if rec.get("sha256"):
            self.shas.add(rec["sha256"])

    def refresh(self, force: bool = False) -> None:
        """Incrementally tail-read every *.jsonl ledger (new files included)."""
        if not force and time.time() - self._last_refresh < LEDGER_REFRESH_S:
            return
        self._last_refresh = time.time()
        try:
            names = [n for n in os.listdir(LEDGER_DIR) if n.endswith(".jsonl")
                     and n not in ("rejects.jsonl", "ukna_candidates.jsonl",
                                   "gov_dedup_removed.jsonl")]
        except OSError:
            return
        for name in names:
            path = os.path.join(LEDGER_DIR, name)
            try:
                size = os.path.getsize(path)
                start = self.offsets.get(name, 0)
                if size <= start:
                    continue
                with open(path, encoding="utf-8", errors="replace") as f:
                    f.seek(start)
                    for line in f:
                        try:
                            self._absorb(json.loads(line))
                        except Exception:
                            continue
                    self.offsets[name] = f.tell()
            except OSError:
                continue
        if not force:   # tombstones can be appended mid-run by the retro sweep
            self.load_tombstones()

    # NOTE: an in-run retro-upgrade of already-ingested rows was implemented here
    # and REMOVED deliberately. A dedicated triage agent owns retro-triage of the
    # stored corpus and writes the same nara.jsonl in _ledger (it has already
    # recorded 50 rows incl. owner-unlock rules R5/*). Any whole-file rewrite from
    # this process would clobber that agent's concurrent writes, so this lane only
    # ever APPENDS to the ledger. New items get their triage rule at ingest time.

    def load_tombstones(self) -> int:
        """Deleted+tombstoned items must STAY deleted. Without this, resume/dedup
        reads only <source>.jsonl, so a purged item is re-downloaded on the next
        pass (measured: naId 16664 purged 16:24:48, re-fetched 16:29:59)."""
        path = os.path.join(LEDGER_DIR, "gov_dedup_removed.jsonl")
        if not os.path.exists(path):
            return 0
        n = 0
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                f.seek(self._tomb_offset)
                for line in f:
                    try:
                        rec = json.loads(line)
                    except Exception:
                        continue
                    if rec.get("source"):
                        self.done.add((rec["source"], str(rec.get("id"))))
                        n += 1
                    if rec.get("sha256"):
                        self.shas.add(rec["sha256"])
                self._tomb_offset = f.tell()
        except OSError:
            return 0
        if n:
            log(f"tombstones loaded: {n} removed ids added to the skip set")
        return n

    def load_existing_index(self) -> None:
        """CONTRACT §6.3: consume existing_index.json — shape
        {"built_at", "sha256": {hex: path} | [hex], "source_ids":
        {"source:id": path} | [keys], "weak_keys": ...}. Reload on mtime change;
        each (re)load triggers a retroactive sha sweep of this lane's ledgers."""
        try:
            mtime = os.path.getmtime(EXISTING_INDEX)
        except OSError:
            return
        if mtime == self._index_mtime:
            return
        try:
            data = json.load(open(EXISTING_INDEX, encoding="utf-8", errors="replace"))
        except Exception as e:  # noqa: BLE001
            log(f"existing_index.json unreadable ({e.__class__.__name__}); ignoring")
            return
        self._index_mtime = mtime
        if not isinstance(data, dict):
            log("existing_index.json: unexpected top-level type; ignoring")
            return
        shas = data.get("sha256") or {}
        self.index_shas = set(shas if isinstance(shas, list) else shas.keys())
        # contract shape: "source_ids" {"source:id": path} | [keys];
        # live 2026-07-28 shape: "ids" {source: [native ids]}
        sids = data.get("source_ids") or data.get("ids") or {}
        if isinstance(sids, dict) and any(isinstance(v, list) for v in sids.values()):
            self.index_ids = {f"{src}:{iid}".lower()
                              for src, lst in sids.items()
                              for iid in (lst if isinstance(lst, list) else [])}
        else:
            self.index_ids = {str(k).lower()
                              for k in (sids if isinstance(sids, list) else sids.keys())}
        log(f"existing_index.json loaded (mtime {mtime:.0f}): "
            f"{len(self.index_shas)} shas, {len(self.index_ids)} source ids")
        removed = retro_sha_sweep(self.index_shas)
        if removed:
            log(f"retroactive sweep: removed {removed} gov-lane duplicates "
                "(reason dup_existing_retro_sha)")

    def seen(self, source: str, item_id: str) -> bool:
        return (source, str(item_id)) in self.done

    def in_existing_index(self, source: str, item_id: str) -> bool:
        return f"{source}:{item_id}".lower() in self.index_ids

    def shelf_ok(self) -> bool:
        return drive_free(SHELF_DRIVE) > SHELF_FLOOR

    def record(self, rec: dict) -> None:
        self._absorb(rec)
        self.run_items += 1
        self.run_bytes += rec.get("bytes", 0)
        t = rec.get("theme", "?")
        self.theme_items[t] = self.theme_items.get(t, 0) + 1
        self.theme_bytes[t] = self.theme_bytes.get(t, 0) + rec.get("bytes", 0)
        self.recent.setdefault(t, []).append(rec["file_path"])
        self.recent[t] = self.recent[t][-QC_SHEET_TILES:]
        path = os.path.join(LEDGER_DIR, f"{rec['source']}.jsonl")
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if self.theme_total.get(t, 0) % QC_SHEET_EVERY == 0:   # CONTRACT §7
            build_contact_sheet(t, self.recent.get(t, []), self.theme_total.get(t, 0))


def take(ledger: Ledger, *, source: str, item_id: str, title: str, source_url: str,
         download_url: str, kind: str, theme: str, license_raw: str, decision: str,
         default_ext: str, dry_run: bool, desc: str = "",
         attribution_text: str = "", extra: dict | None = None) -> bool:
    """Vet -> download -> validate -> ledger. Returns True if ingested."""
    ledger.refresh()
    ledger.load_existing_index()
    if ledger.seen(source, item_id):
        return False
    if ledger.in_existing_index(source, item_id):   # CONTRACT §6.3 pre-download
        reject_log(source, item_id, theme, "dup_existing_id", title=title)
        return False
    if PERSON_RE.search(title or ""):
        reject_log(source, item_id, theme, "person-filter", title=title)
        return False
    score, matched, negs = relevance(theme, f"{title} {desc}")
    if score < DEFAULT_THRESHOLD:
        reject_log(source, item_id, theme, f"relevance<{DEFAULT_THRESHOLD}",
                   score, matched, negs, title=title)
        return False
    # The item must be ABOUT the theme, not merely mention it: at least one
    # positive term has to appear in the TITLE. Without this, an incidental word
    # in a long scope-and-content note is enough to clear the threshold (an
    # unrelated film scored exactly 30 on two scope-note words alone).
    if relevance(theme, title)[0] == 0:
        reject_log(source, item_id, theme, "title-irrelevant", score, matched, negs, title=title)
        return False
    if decision == "review_required":
        if drive_free(QUAR_DRIVE) <= QUAR_FLOOR:
            log("  skip quarantine item: H: free-space floor reached")
            return False
        root = os.path.join(QUARANTINE, theme)
    else:
        if not ledger.shelf_ok():
            return False
        root = os.path.join(SHELF_ROOT, theme)
    os.makedirs(root, exist_ok=True)
    dest = dest_filename(root, source, item_id, title, ext_of(download_url, default_ext))
    if dry_run:
        log(f"  DRY {decision:>15} s={score:3d} {theme:24} {title[:52]}  <- {download_url[:70]}")
        return True
    try:
        nbytes, sha = NET.download(download_url, dest)
    except Exception as e:  # noqa: BLE001
        log(f"  dl-fail: {e}")
        reject_log(source, item_id, theme, f"download-fail:{e.__class__.__name__}", score, title=title)
        for p in (dest, dest + ".part"):
            if os.path.exists(p):
                try:
                    os.remove(p)
                except OSError:
                    pass
        return False
    if sha in ledger.shas or sha in ledger.index_shas:
        reason = "dup_existing_sha" if sha in ledger.index_shas else "dup-sha256"
        log(f"  {reason}, removed: {os.path.basename(dest)[:70]}")
        os.remove(dest)
        reject_log(source, item_id, theme, reason, score, title=title)
        return False
    ok, why = validate_media(dest, kind)
    if not ok:
        log(f"  reject ({why}), removed: {os.path.basename(dest)[:70]}")
        os.remove(dest)
        reject_log(source, item_id, theme, f"tech:{why}", score, title=title)
        return False
    rec = {
        "id": str(item_id), "source": source, "source_url": source_url,
        "title": title, "license_field_raw": license_raw[:500],
        "license_decision": decision, "theme": theme, "file_path": dest,
        "bytes": nbytes, "sha256": sha,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "relevance_score": score, "matched_keywords": matched[:12],
    }
    if attribution_text:
        rec["attribution_text"] = attribution_text
    if extra:   # e.g. triage_rule + license_evidence: a decision never ships alone
        rec.update(extra)
    ledger.record(rec)
    log(f"  OK {decision:>15} s={score:3d} {nbytes/1e6:7.1f}MB {os.path.basename(dest)[:74]}")
    return True


# ------------------------------------------------- NARA rights triage ----
# Adopted from episodes/_planning/measurements/NARA_LICENSE_TRIAGE.v001.md §6
# (rules version nara-license-triage-v001). Measured basis: over 445 unique NARA
# moving-image records the "Restricted - Possibly / Copyright" flag is applied to
# 223/223 items of RG-111 series 13807 — a series-wide caution, NOT an item
# determination. ancestors[] is what actually carries provenance. Needs no extra
# API call: every field used already ships inside hits[]._source.record.

US_FEDERAL_CREATOR = (
    "department of defense", "department of the navy", "department of the army",
    "department of the air force", "office of the chief signal officer",
    "naval photographic center", "army pictorial", "signal corps",
    "united states marine corps", "marine corps", "coast guard",
    "department of justice", "federal bureau of investigation",
    "office of war information", "united states information agency",
    "department of state", "department of the interior", "department of agriculture",
    "national aeronautics and space administration", "works progress administration",
    "office of strategic services", "war department", "atomic energy commission",
    "environmental protection agency", "bureau of ",
)
THIRD_PARTY_LANG = (
    "newsreel", "courtesy of", "obtained from other sources", "proprietary rights",
    "copyright", "universal", "pathe", "pathé", "movietone", "hearst",
    "march of time", "paramount news", "cbs", "nbc", "abc news",
    "gift of", "donated by", "captured german", "captured enemy", "captured japanese",
    "licensed", "stock footage from",
)
SHOTLIST_LANG = (
    "newsreel", "captured enemy", "captured german", "captured japanese",
    "courtesy of", "stock shot from", "copyright",
)
HARD_CLAIM = (
    "is copyrighted", "copyright is retained", "copyright retained by",
    "may not be used for commercial", "not for commercial use",
    "commercial use is prohibited", "permission of the copyright owner is required",
    "written permission of the donor",
)
OK_STATUS = {"unrestricted", "undetermined", ""}
TRIAGE_VERSION = "nara-license-triage-v001"


def nara_license_decision(rec: dict) -> tuple[str, str, str]:
    """Returns (decision, rule_id, evidence). decision in {pd, review_required, reject}."""
    use = rec.get("useRestriction") or {}
    status = str(use.get("status", "")).strip()
    note = str(use.get("note", "") or "")
    spec = [str(s) for s in (use.get("specificUseRestrictions") or [])]
    anc = rec.get("ancestors") or []
    rgs = [a for a in anc if a.get("levelOfDescription") == "recordGroup"]
    colls = [a for a in anc if a.get("levelOfDescription") == "collection"]
    creators = [str(c.get("heading", "")) for a in anc for c in (a.get("creators") or [])]
    creators += [str(c.get("heading", "")) for c in (rec.get("creators") or [])]
    creator_s = " | ".join(creators)
    ev = "useRestriction=" + json.dumps(use, ensure_ascii=False)

    blob = " ".join([str(rec.get("title", "")), str(rec.get("scopeAndContentNote", "")),
                     " ".join(str(x) for x in (rec.get("generalNotes") or [])),
                     json.dumps(rec.get("contributors") or [], ensure_ascii=False),
                     json.dumps(rec.get("donors") or [], ensure_ascii=False),
                     str(rec.get("productionSeriesTitle", ""))]).lower()

    # R0 — affirmative claim or commercial bar anywhere in the rights fields.
    hay = (note + " " + " ".join(spec) + " " + blob).lower()
    for p in HARD_CLAIM:
        if p in hay:
            return "reject", "R0/explicit-claim", f'{ev}; hard-claim phrase "{p}"'
    if status.lower() == "restricted":
        return "reject", "R0/status-restricted", ev

    # R3 — provenance gates (a collection ancestor means DONATED third-party film).
    if colls:
        why = ", ".join(f'{c.get("collectionIdentifier")}: {c.get("title")}' for c in colls)
        return ("review_required", "R3/donated-collection",
                f"{ev}; donated collection ancestor [{why}]; creator {creator_s or '?'}")
    if not rgs:
        return "review_required", "R3/no-record-group", f"{ev}; no federal recordGroup ancestor"
    if not any(k in creator_s.lower() for k in US_FEDERAL_CREATOR):
        return ("review_required", "R3/creator-not-federal",
                f"{ev}; RG {rgs[0].get('recordGroupNumber')} but creator {creator_s or '?'}")

    tp = [k for k in THIRD_PARTY_LANG if k in blob]
    tp += [k for k in SHOTLIST_LANG if k in str(rec.get("shotList", "")).lower()]
    if tp:
        return ("review_required", "R3/third-party-content-language",
                f"{ev}; RG {rgs[0].get('recordGroupNumber')} but record describes "
                f"third-party material {tp} — agency-collected, not agency-created")

    # R3 — official-duty / custody guard: 17 U.S.C. 105 clears a work only if a US
    # federal employee MADE it. No production date + multi-year coverage span = an
    # accessioned compilation the agency merely collected (caught captured foreign
    # film that the metadata alone would have cleared).
    cs, ce = rec.get("coverageStartDate") or {}, rec.get("coverageEndDate") or {}
    span = (int(ce.get("year", 0)) - int(cs.get("year", 0))) if (cs and ce) else 0
    if not (rec.get("productionDates") or []) and span >= 1:
        return ("review_required", "R3/undated-multiyear-compilation",
                f"{ev}; RG {rgs[0].get('recordGroupNumber')}, no productionDate, "
                f"{span}-year coverage span {cs.get('year')}-{ce.get('year')}")

    # R3 — any surviving restriction flag (the RG-111 blanket case lands here).
    if status.lower() not in OK_STATUS:
        return ("review_required", "R3/restriction-flagged",
                f'{ev}; NARA flags status "{status}" spec={spec}')
    if spec:
        return "review_required", "R3/specific-use-restriction", f"{ev}; spec={spec}"
    if note:
        return "review_required", "R3/restriction-note", ev

    # R1 — US Government work.
    return ("pd", "R1/us-federal-record",
            f'{ev}; RG {rgs[0].get("recordGroupNumber")} "{rgs[0].get("title")}"; '
            f'creator {creator_s}; localId {rec.get("localIdentifier","")}; no donor or '
            f"collection ancestor; no third-party-content language — 17 U.S.C. 105")


# ------------------------------------------------------------- adapters ----
# Each adapter: (ledger, theme, limit, dry_run) -> media items ingested this call.
# Pagination: module-level PASS (runner pass N == result page N).


def src_nara(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """NARA via the catalog website's public backend (keyless v2 JSON):
    https://catalog.archives.gov/proxy/records/search
    typeOfMaterials pre-filters to Moving Images / Photographs so textual case
    files never enter the candidate pool. Unrestricted federal records -> pd."""
    if theme not in NARA_THEMES:
        return 0
    got = 0
    plans = [("Moving Images", "video", THEMES[theme].get("video", []), "mp4"),
             ("Photographs and other Graphic Materials", "image",
              THEMES[theme].get("image", []), "jpg")]
    for tom, kind, queries, dext in plans:
        for q in queries:
            if got >= limit or not ledger.shelf_ok():
                return got
            try:
                data = NET.get_json(
                    "https://catalog.archives.gov/proxy/records/search",
                    params={"q": q, "limit": 50, "page": PASS,
                            "availableOnline": "true", "typeOfMaterials": tom})
            except Exception as e:  # noqa: BLE001
                log(f"  nara search fail ({q!r}/{tom}): {e}")
                continue
            for h in data.get("body", {}).get("hits", {}).get("hits", []):
                if got >= limit or not ledger.shelf_ok():
                    return got
                rec = (h.get("_source", {}) or {}).get("record", {}) or {}
                naid = str(rec.get("naId", ""))
                if not naid:
                    continue
                use = rec.get("useRestriction", {})
                use_s = use if isinstance(use, str) else json.dumps(use)
                # evidence-based triage (nara-license-triage-v001): the
                # useRestriction flag is series boilerplate, ancestors[] carry
                # the actual provenance.
                decision, rule_id, evidence = nara_license_decision(rec)
                raw = f"useRestriction={use_s[:300]}; US federal record (NARA)"
                title = str(rec.get("title", "") or naid)
                if decision == "reject":
                    reject_log("nara", naid, theme, f"license:{rule_id}", title=title)
                    continue
                desc = str(rec.get("scopeAndContentNote", ""))[:900]
                exts = (".mp4", ".mov") if kind == "video" else (".jpg", ".jpeg", ".png")
                cands = []
                for obj in rec.get("digitalObjects", []) or []:
                    u = str(obj.get("objectUrl", "") or "")
                    if not u.lower().endswith(exts):
                        continue
                    size = int(obj.get("objectFileSize", 0) or 0)
                    if size and not (MIN_ITEM_BYTES < size <= MAX_ITEM_BYTES):
                        continue
                    cands.append((size, u, str(obj.get("objectId", "") or "")))
                if not cands:
                    continue
                # video: largest derivatives first (best chance of >=720p under
                # the 2GB cap); images: catalog order (scans are sequential)
                if kind == "video":
                    cands.sort(key=lambda c: -c[0])
                cap = NARA_VIDEO_PER_RECORD if kind == "video" else NARA_IMAGES_PER_RECORD
                for i, (_, u, obj_id) in enumerate(cands[:cap]):
                    if got >= limit:
                        break
                    item_id = f"{naid}-{obj_id or i + 1}"
                    if take(ledger, source="nara", item_id=item_id, title=title,
                            source_url=f"https://catalog.archives.gov/id/{naid}",
                            download_url=u, kind=kind, theme=theme,
                            license_raw=raw, decision=decision,
                            default_ext=dext, dry_run=dry_run, desc=desc,
                            extra={"triage_rule": rule_id,
                                   "license_evidence": f"{evidence} [{rule_id}; "
                                                       f"{TRIAGE_VERSION}]"}):
                        got += 1
    return got


_IIIF_RE = re.compile(r"(/iiif/[^#]+/full/)[^/]+(/0/default\.jpg)")
_WH_RE = re.compile(r"#h=(\d+)&w=(\d+)")


def _loc_files(detail: dict) -> list[dict]:
    """Flatten loc.gov item resources[].files[] (nested lists) into file dicts."""
    out: list[dict] = []
    for res in detail.get("resources", []) or []:
        files = res.get("files")
        for grp in files if isinstance(files, list) else []:
            for f in (grp if isinstance(grp, list) else [grp]):
                if isinstance(f, dict) and f.get("url"):
                    out.append(f)
    return out


def _loc_image_url(detail: dict, res: dict) -> str:
    """Pick the best still: largest JPEG derivative >=1200px, else the archival
    master TIFF (pnp masters are always high-res), else the IIIF full-size /
    largest thumbnail. Returns "" when nothing can clear the 1200px floor —
    which avoids downloading the 1024px derivatives LOC returns by default."""
    files = _loc_files(detail)
    jpegs = [(int(f.get("width") or 0), str(f["url"])) for f in files
             if "jpeg" in str(f.get("mimetype", "")).lower()]
    if jpegs:
        w, url = max(jpegs)
        if w >= 1200:
            return url
    for f in files:                        # master scan: dimensions unreported
        u = str(f["url"])
        if "tiff" in str(f.get("mimetype", "")).lower() or u.lower().endswith((".tif", ".tiff")):
            return u
    best_w, best_url = 0, ""
    for u in (res.get("image_url") or []):
        if ".jpg" not in u:
            continue
        m = _WH_RE.search(u)
        w = int(m.group(2)) if m else 0
        clean = _IIIF_RE.sub(r"\1pct:100\2", u.split("#", 1)[0])
        if "pct:100" in clean:             # IIIF full-size: always take it
            return clean
        if w >= best_w:
            best_w, best_url = w, clean
    return best_url if best_w >= 1200 else ""


def src_loc(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Library of Congress loc.gov JSON API (fo=json), film/video + photos.
    Rights text decides: public domain -> pd, no known restrictions ->
    free_commercial, else review_required (quarantine). Stills upgraded to
    IIIF /full/pct:100/ where the thumbnail is an IIIF derivative."""
    got = 0
    plans = [("video", "film,video", "video", "mp4"),
             ("image", "image", "image", "jpg")]
    for qkey, fmt, kind, dext in plans:
        for q in THEMES[theme].get(qkey, []):
            if got >= limit or not ledger.shelf_ok():
                return got
            try:
                data = NET.get_json("https://www.loc.gov/search/", params={
                    "q": q, "fo": "json", "fa": f"online-format:{fmt}",
                    "c": 40, "sp": PASS})
            except Exception as e:  # noqa: BLE001
                log(f"  loc search fail ({q!r}): {e}")
                continue
            for res in data.get("results", []) or []:
                if got >= limit or not ledger.shelf_ok():
                    return got
                item_url = str(res.get("id", ""))
                if not item_url.startswith("http") or "/item/" not in item_url:
                    continue
                if ledger.seen("loc", item_url):
                    continue
                if res.get("access_restricted"):
                    continue
                try:
                    detail = NET.get_json(item_url, params={"fo": "json"})
                except Exception:
                    continue
                item = detail.get("item", {}) or {}
                rights_bits: list[str] = []
                for k in ("rights_advisory", "rights_information", "rights"):
                    v = item.get(k)
                    if isinstance(v, list):
                        rights_bits += [str(x) for x in v]
                    elif v:
                        rights_bits.append(str(v))
                raw = " | ".join(rights_bits)
                low = raw.lower()
                if "public domain" in low:
                    decision = "pd"
                elif "no known restrictions" in low:
                    decision = "free_commercial"
                else:
                    decision = "review_required"
                url = ""
                if kind == "video":
                    mp4s = [(int(f.get("height") or 0), str(f["url"]))
                            for f in _loc_files(detail) if str(f["url"]).endswith(".mp4")]
                    if mp4s:
                        # prefer a >=720p derivative, else the tallest available
                        hd = [c for c in mp4s if c[0] >= 720]
                        url = min(hd)[1] if hd else max(mp4s)[1]
                    if not url:
                        for r2 in detail.get("resources", []) or []:
                            if str(r2.get("url", "")).endswith(".mp4"):
                                url = r2["url"]
                else:
                    url = _loc_image_url(detail, res)
                    if not url:
                        reject_log("loc", item_url, theme, "tech:image-below-1200px(metadata)")
                        continue
                if not url:
                    continue
                desc = " ".join(map(str, (res.get("description") or [])
                                    + (res.get("subject") or [])))[:900]
                if take(ledger, source="loc", item_id=item_url,
                        title=str(res.get("title", "")), source_url=item_url,
                        download_url=url, kind=kind, theme=theme,
                        license_raw=raw or "(no rights field)", decision=decision,
                        default_ext=dext, dry_run=dry_run, desc=desc):
                    got += 1
    return got


_ukna_candidate_ids: set[str] | None = None


def _ukna_seen_candidates() -> set[str]:
    global _ukna_candidate_ids
    if _ukna_candidate_ids is None:
        _ukna_candidate_ids = set()
        if os.path.exists(CANDIDATES_PATH):
            with open(CANDIDATES_PATH, encoding="utf-8", errors="replace") as f:
                for line in f:
                    try:
                        _ukna_candidate_ids.add(str(json.loads(line).get("id")))
                    except Exception:
                        continue
    return _ukna_candidate_ids


def src_ukna(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """UK National Archives Discovery API — METADATA ONLY (verified 2026-07-27:
    /API/v1/docs lists no media/download endpoint; digitised downloads are
    website-basket only, bot-gated and paid). Ships zero media; records
    digitised open TNA candidates with OGL attribution text into
    _ledger/ukna_candidates.jsonl so a future keyed/manual route can act."""
    if theme not in UKNA_THEMES:
        return 0
    seen = _ukna_seen_candidates()
    new = 0
    for q in THEMES[theme].get("ukna", []):
        if PASS > 100:   # documented sps.page range [0, 100]
            break
        try:
            data = NET.get_json(
                "https://discovery.nationalarchives.gov.uk/API/search/records",
                params={"sps.searchQuery": q, "sps.digitisedRecordsOnly": "true",
                        "sps.heldByCode": "TNA", "sps.resultsPageSize": 100,
                        "sps.page": PASS},
                headers={"Accept": "application/json"})
        except Exception as e:  # noqa: BLE001
            log(f"  ukna search fail ({q!r}): {e}")
            continue
        for rec in data.get("records", []) or []:
            rid = str(rec.get("id", ""))
            if not rid or rid in seen:
                continue
            title = str(rec.get("title", "") or "")
            score, matched, negs = relevance(theme, f"{title} {rec.get('description', '')}")
            if score < DEFAULT_THRESHOLD:
                continue
            ref = str(rec.get("reference", "") or "")
            row = {
                "id": rid, "source": "ukna",
                "source_url": f"https://discovery.nationalarchives.gov.uk/details/r/{rid}",
                "title": title[:300], "reference": ref,
                "covering_dates": str(rec.get("coveringDates", "") or ""),
                "held_by": [h for h in (rec.get("heldBy") or []) if isinstance(h, str)],
                "license_field_raw": "Crown copyright / OGL v3.0 candidate "
                                     "(digitised, open, held by TNA)",
                "license_decision": "review_required",
                "theme": theme, "file_path": None, "bytes": 0, "sha256": None,
                "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "relevance_score": score, "matched_keywords": matched[:12],
                "attribution_text": OGL_ATTRIBUTION.format(ref=ref or rid),
                "note": "metadata-only: Discovery API exposes no media download",
            }
            if not dry_run:
                with open(CANDIDATES_PATH, "a", encoding="utf-8") as f:
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
            seen.add(rid)
            new += 1
    if new:
        log(f"  ukna: +{new} metadata candidates ({theme}) -> {os.path.basename(CANDIDATES_PATH)} "
            "(0 media: Discovery API is metadata-only)")
    return 0   # never counts as media; the run's stop logic ignores candidates


ADAPTERS = {"nara": src_nara, "loc": src_loc, "ukna": src_ukna}


def retriage_nara(dry_run: bool = False) -> int:
    """DISABLED — kept as documentation of a measured dead end.

    A standalone re-triage pass would have to re-fetch each stored naId, but
    catalog.archives.gov answers per-naId lookups (`q=<naId>` and `naIds=<naId>`)
    with the SPA HTML rather than JSON: 30/30 failures over a 36-minute run,
    while the PAGED search used by src_nara keeps working. So the retro-upgrade
    Retro-triage of the STORED corpus is owned by the dedicated NARA triage
    agent, which writes the same nara.jsonl; this lane stays append-only so it
    can never clobber that agent's concurrent writes. New items are triaged at
    ingest time by src_nara.
    """
    log("retriage: not available in this lane. Per-naId lookups return SPA HTML "
        "(30/30 measured), and retro-triage of stored rows belongs to the "
        "dedicated NARA triage agent — this lane only appends.")
    return 0


# ----------------------------------------------------------------- main ----


_LOCK_FH = None


def acquire_lock() -> bool:
    """Single-instance guard so the nightly auto-resume task cannot start a second
    copy while a run is still going (double requests would break rate limits).
    Windows: exclusive msvcrt byte lock held for the process lifetime."""
    global _LOCK_FH
    os.makedirs(LEDGER_DIR, exist_ok=True)
    path = os.path.join(LEDGER_DIR, "ingest_gov.lock")
    try:
        fh = open(path, "a+")
        try:
            import msvcrt
            fh.seek(0)
            msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
        except ImportError:
            import fcntl
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        fh.seek(0)
        fh.truncate()
        fh.write(f"{os.getpid()} {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n")
        fh.flush()
        _LOCK_FH = fh   # keep open: closing releases the lock
        return True
    except OSError:
        return False


def main() -> int:
    global PASS, LOG_FILE
    ap = argparse.ArgumentParser(
        description="PD gov-archives ingest (NARA/LOC/UKNA -> E:\\pd-archive)")
    ap.add_argument("--source", default="all", help="all | comma list of: nara,loc,ukna")
    ap.add_argument("--theme", default="all", help="all | comma list of themes")
    ap.add_argument("--limit", type=int, default=1000,
                    help="max media items per source per theme PER PASS (smoke: 2-3)")
    ap.add_argument("--passes", type=int, default=100,
                    help="max runner passes (pass N reads result page N)")
    ap.add_argument("--dry-run", action="store_true", help="vet and list, no downloads")
    ap.add_argument("--log-file", default="",
                    help=r"append log copy here (long run: _ledger\ingest_gov.log)")
    ap.add_argument("--sweep-existing-index", action="store_true",
                    help="retroactive sha sweep against existing_index.json, then exit")
    ap.add_argument("--retriage-nara", action="store_true",
                    help="re-decide existing NARA rows with nara-license-triage-v001, "
                         "moving cleared items out of quarantine, then exit")
    args = ap.parse_args()
    LOG_FILE = args.log_file

    if args.sweep_existing_index:
        led = Ledger()   # loads existing_index.json and runs the retro sweep
        if not led.index_shas:
            log("sweep: existing_index.json absent or empty — nothing swept")
        return 0

    if args.retriage_nara:
        if not acquire_lock():
            log("retriage needs the lock (a run is live) — stop the worker first")
            return 1
        retriage_nara(dry_run=args.dry_run)
        return 0

    if not acquire_lock():
        log("another gov-archives run holds ingest_gov.lock — exiting "
            "(nightly auto-resume is a no-op while a run is live)")
        return 0

    if os.path.exists(CONTRACT_MD):
        log("CONTRACT.md present — this adapter is aligned with v1 (2026-07-27); "
            "re-verify manually if the contract version changes")

    sources = list(ADAPTERS) if args.source == "all" else \
        [s.strip() for s in args.source.split(",") if s.strip() in ADAPTERS]
    themes = list(THEMES) if args.theme == "all" else \
        [t.strip() for t in args.theme.split(",") if t.strip() in THEMES]
    if not sources or not themes:
        log("nothing to do (bad --source/--theme)")
        return 2

    ledger = Ledger()
    log(f"gov-archives run start: sources={sources} themes={len(themes)} "
        f"limit={args.limit}/src/theme/pass passes<={args.passes} dry_run={args.dry_run}")
    log(f"resume state: {len(ledger.done)} (source,id) pairs, {len(ledger.shas)} shas "
        f"across all ledgers; E: free {drive_free(SHELF_DRIVE)/GB:.0f}GB "
        f"(floor {SHELF_FLOOR/GB:.0f}GB), H: free {drive_free(QUAR_DRIVE)/GB:.0f}GB "
        f"(quarantine floor {QUAR_FLOOR/GB:.0f}GB)")

    counts: dict[str, int] = {}
    empty_streak = 0
    for pass_n in range(1, args.passes + 1):
        PASS = pass_n
        pass_new = 0
        if not ledger.shelf_ok():
            log("E: free-space floor reached — stopping (hard guard)")
            break
        log(f"===== PASS {pass_n} =====")
        for src in sources:
            fn = ADAPTERS[src]
            for theme in themes:
                if not ledger.shelf_ok():
                    break
                if src == "nara" and theme not in NARA_THEMES:
                    continue
                if src == "ukna" and theme not in UKNA_THEMES:
                    continue
                log(f"[p{pass_n}:{src}] theme={theme}")
                try:
                    n = fn(ledger, theme, args.limit, args.dry_run)
                    counts[src] = counts.get(src, 0) + n
                    pass_new += n
                except KeyboardInterrupt:
                    raise
                except Exception as e:  # noqa: BLE001
                    log(f"[{src}] theme={theme} error: {e}")
            if not ledger.shelf_ok():
                break
        ledger.load_existing_index()
        # A relaunch re-walks pages 1..N (already-ingested ids are skipped without
        # extra requests), so a SINGLE empty pass means nothing — only stop after
        # EMPTY_PASS_STOP consecutive empty passes deeper in the result pages.
        empty_streak = empty_streak + 1 if pass_new == 0 else 0
        if empty_streak >= EMPTY_PASS_STOP:
            log(f"{EMPTY_PASS_STOP} consecutive passes with no new media — "
                "sources exhausted at current queries; stopping")
            break

    log("=" * 70)
    log("SUMMARY (gov-archives lane)")
    for src in sources:
        log(f"  {src:6} {counts.get(src, 0):6d} new media items this run")
    log(f"  this run: {ledger.run_items} items, {ledger.run_bytes/GB:.2f} GB")
    for t in sorted(ledger.theme_items):
        log(f"  theme {t:26} {ledger.theme_items[t]:5d} items "
            f"{ledger.theme_bytes[t]/GB:7.2f} GB")
    log(f"  E: free now {drive_free(SHELF_DRIVE)/GB:.0f}GB; ledgers: {LEDGER_DIR}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("interrupted")
        sys.exit(130)
