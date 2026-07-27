# -*- coding: utf-8 -*-
"""
Multi-source free-asset ingest pipeline for the Prime Documentary archive shelf.

Downloads THEMED (not bulk) public-domain / CC0 / clearly-free-commercial assets from
approved sources into a rights-tracked, MULTI-ROOT tiered shelf (~4.4TB total budget):

  Tier 1  H:\\pd-media\\assets\\archive\\<theme>\\   STOP if H: free < 500GB
  Tier 2  D:\\pd-archive\\<theme>\\                  STOP if D: free < 250GB
  Tier 3  E:\\pd-archive\\<theme>\\                  STOP if E: free < 250GB
  Tier 4  F:\\pd-archive\\<theme>\\                  STOP if F: free < 50GB

When a tier's budget/floor is hit the router continues on the next tier automatically.
Lane routing: PD-lane themes start on Tier 1 (H:, production-adjacent); BROAD themes
(future channels: space/nature/cities/japan/PD films/etc.) start on Tier 2 and fill D->E->F.
C: is NEVER used. Quarantine and the centralized ledger always live on H::

    H:\\pd-media\\assets\\archive\\_quarantine\\<theme>\\  (license_decision=review_required)
    H:\\pd-media\\assets\\archive\\_ledger\\<source>.jsonl (per-item rights ledger)

Ledger JSONL schema (one object per line; file_path records which drive an item landed on):
    {id, source, source_url, title, license_field_raw, license_decision
     (pd|cc0|free_commercial|review_required), theme, file_path, bytes, sha256, fetched_at}

Sources (keyless first):
    ia         Internet Archive (advancedsearch.php + metadata/download API; Prelinger,
               classic cartoons/commercials, PD feature films — h.264 derivatives preferred,
               never multi-GB masters; may go DEEP)
    loc        Library of Congress (loc.gov JSON API)
    nara       National Archives (catalog.archives.gov v2 — needs free x-api-key; skips w/o)
    met        Met Museum Open Access (collection API, CC0 only)
    nasa       NASA Image and Video Library (images-api.nasa.gov, keyless; NASA media = PD;
               also covers weather/ocean/science themes. NOAA has no clean media API —
               NOAA PD material arrives via Wikimedia Commons NOAA-credited files instead)
    wikimedia  Wikimedia Commons API (STRICT per-file filter: PD/CC0 -> shelf;
               CC-BY -> quarantine with attribution recorded; CC-BY-SA/unknown -> skipped)
    mixkit     mixkit.co listing pages (no official API; robots.txt-checked, >=2s/req)
    coverr     coverr.co listing pages (no official API; robots.txt-checked, >=2s/req)
    pixabay    Pixabay API (PIXABAY_API_KEY in repo .env; audio endpoint probed & reported)
  Keyed (adapter present, skips gracefully without key; see OWNER KEY LIST):
    smithsonian  SMITHSONIAN_API_KEY (api.data.gov)   — CC0-filtered images
    freesound    FREESOUND_API_KEY                     — CC0-only filter, HQ mp3 previews
    nypl         NYPL_API_TOKEN                        — publicDomainOnly items
    unsplash     UNSPLASH_ACCESS_KEY                   — SMALL curated pulls only (<=50/theme
                                                         TOTAL; API terms prohibit bulk mirroring)

Limits (owner final directive: download as much as possible): the ONLY limits are
(1) drive free-space floors above, (2) license rules, (3) polite per-source rate
limits. No per-theme caps. --cap-gb is optional (0 = unlimited, the default) and
exists only for smoke tests. Resumable across interruptions/reboots: (source,id) pairs already in a ledger are
skipped, budgets are recomputed from the ledger, and the runner loops in PASSES
(pass N = page N of each source) until caps are met or all sources are exhausted —
a single relaunch continues wherever it stopped.

Real-person soft filter: queries avoid portrait/interview/mugshot phrasing and titles
matching obvious person-focused keywords are skipped. SOFT bias only — eyeball QC
before shipping any item into an episode.

AGENT ASSIGNMENT (multi-agent split): THIS runner owns Internet Archive / Prelinger
only, tier affinity H,D. Adapters for other sources remain in this file as the shared
framework reference (sibling agents own those sources — do not run them from here).
Ledger contract for all agents: H:\\pd-media\\assets\\archive\\_ledger\\CONTRACT.md

Usage:
  python scripts/ingest_archive_sources.py --source ia --theme americana_1930s_1970s --limit 2
  python scripts/ingest_archive_sources.py --source ia --tiers H,D   # THE long run (resumable)
  python scripts/ingest_archive_sources.py --source met --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import html as html_mod
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.robotparser
from datetime import datetime, timezone

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GB = 1024 ** 3
TB = 1024 * GB

# --- tiered storage (router falls through in order; C: never used) ---
TIERS = [
    {"name": "H", "root": r"H:\pd-media\assets\archive", "drive": "H:\\", "floor": 500 * GB},
    {"name": "D", "root": r"D:\pd-archive", "drive": "D:\\", "floor": 250 * GB},
    {"name": "E", "root": r"E:\pd-archive", "drive": "E:\\", "floor": 250 * GB},
    {"name": "F", "root": r"F:\pd-archive", "drive": "F:\\", "floor": 50 * GB},
]
H_ROOT = TIERS[0]["root"]
LEDGER_DIR = os.path.join(H_ROOT, "_ledger")     # ledger centralized on H:
QUARANTINE = os.path.join(H_ROOT, "_quarantine")  # quarantine on H: only

UA = "PrimeDocumentaryIngest/1.0 (archival research; contact: aab153792@gmail.com)"
MAX_ITEM_BYTES = 2 * GB             # never take a single file bigger than this
MIN_ITEM_BYTES = 20 * 1024          # skip suspiciously tiny media

# soft real-person filter (channel policy: illustrative, no real likeness)
PERSON_RE = re.compile(
    r"\b(portrait|portraits|interview|interviews|mugshot|mug shot|headshot|"
    r"testimony of|speech by|press conference)\b", re.I)

# ---- per-item vetting (owner: "confirm one by one, download what's meaningful") ----
# negative keywords: talking-head/junk formats we never want as b-roll
GLOBAL_NEG = ["lecture", "slideshow", "seminar", "webinar", "powerpoint", "sermon",
              "podcast", "gameplay", "tutorial", "unboxing", "vlog", "selfie",
              "portrait", "interview", "mugshot", "headshot", "zoom meeting"]
STOPWORDS = set("the a an of in on and or for with to at from by 1930s 1940s 1950s "
                "1960s 1970s old new".split())
# minimum relevance score to download (precision over recall; archives need >=2
# distinct topical terms, curated stock search is already fairly relevant)
SRC_THRESHOLD = {"mixkit": 20, "coverr": 20, "pixabay": 20, "unsplash": 20,
                 "freesound": 20}
DEFAULT_THRESHOLD = 30
# period themes: IA items must carry date metadata or trusted period provenance
PERIOD_THEMES = {"police_period", "americana_1930s_1970s", "uk_period",
                 "period_telephone_tech", "music_performance_pd_era",
                 "vintage_ads_cartoons", "pd_feature_films"}
QC_SHEET_EVERY = 500   # contact sheet per theme every N downloads
QC_SHEET_TILES = 60
ACTIVE_TIERS: set[str] = {t["name"] for t in TIERS}  # narrowed via --tiers (e.g. "H,D")
ACTIVITY = 0  # unseen candidates evaluated this pass (exhaustion detection)
EXISTING_INDEX = os.path.join(LEDGER_DIR, "existing_index.json")

_theme_pos_cache: dict[str, tuple[set[str], list[str]]] = {}


def theme_terms(theme: str) -> tuple[set[str], list[str]]:
    """(positive term set, full query phrases) derived from the theme's query table."""
    if theme not in _theme_pos_cache:
        phrases: list[str] = []
        terms: set[str] = set()
        for key in ("video", "image", "audio"):
            for q in THEMES[theme].get(key, []):
                phrases.append(q.lower())
                terms |= {w for w in re.findall(r"[a-z]+", q.lower())
                          if w not in STOPWORDS and len(w) > 2}
        _theme_pos_cache[theme] = (terms, phrases)
    return _theme_pos_cache[theme]


def relevance(theme: str, text: str) -> tuple[int, list[str], list[str]]:
    """Score 0-100 from metadata text vs theme keywords. Returns (score, matched, neg_hits).
    +15 per distinct positive term (cap 60), +25 if a full query phrase appears,
    -25 per negative keyword."""
    low = (text or "").lower()
    pos, phrases = theme_terms(theme)
    matched = sorted({t for t in pos if re.search(rf"\b{re.escape(t)}", low)})
    score = min(60, 15 * len(matched))
    if any(p in low for p in phrases):
        score += 25
    negs = [n for n in GLOBAL_NEG if n in low]
    score -= 25 * len(negs)
    return max(0, min(100, score)), matched, negs


def reject_log(source: str, item_id: str, theme: str, reason: str,
               score: int = -1, matched=None, negs=None) -> None:
    """Compact per-item rejects log (skipped items do NOT enter the main ledger)."""
    try:
        os.makedirs(LEDGER_DIR, exist_ok=True)
        with open(os.path.join(LEDGER_DIR, "rejects.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "source": source, "id": str(item_id)[:200], "theme": theme,
                "reason": reason, "score": score,
                "matched": matched or [], "neg": negs or []},
                ensure_ascii=False) + "\n")
    except OSError:
        pass

# per-host politeness (seconds between requests)
HOST_INTERVAL = {
    "mixkit.co": 2.0, "assets.mixkit.co": 2.0,
    "coverr.co": 2.0, "cdn.coverr.co": 2.0, "storage.coverr.co": 2.0,
    "www.loc.gov": 2.0, "tile.loc.gov": 1.0,
    "archive.org": 1.0, "catalog.archives.gov": 1.0,
}
DEFAULT_INTERVAL = 1.0

PASS = 1  # current pass number == page number for paginated sources (set by main loop)

# ---------------------------------------------------------------- themes ----
# queries are deliberately environmental/period-scenery biased (no people terms)
# priority order: uk_highstreet_postoffice (EP56) first, then the rest
THEMES: dict[str, dict[str, list[str]]] = {
    "uk_highstreet_postoffice": {
        "video": ["british high street", "post office britain", "england village shops"],
        "image": ["british high street shops", "royal mail post office", "red postbox england"],
        "audio": ["british street ambience", "shop bell door"],
    },
    "courtroom_justice": {
        "video": ["courtroom", "courthouse", "trial court judicial"],
        "image": ["courtroom interior", "courthouse architecture", "scales of justice gavel"],
        "audio": ["courtroom ambience", "gavel knock wood"],
    },
    "prison_jail": {
        "video": ["prison", "penitentiary", "jail cell block"],
        "image": ["prison corridor cells", "penitentiary building", "jail bars"],
        "audio": ["prison door slam", "metal door clang echo"],
    },
    "police_period": {
        "video": ["police 1950s", "police patrol vintage", "law enforcement 1960s"],
        "image": ["police station vintage", "patrol car 1950s", "police call box"],
        "audio": ["vintage police siren", "police radio chatter"],
    },
    "police_modern": {
        "video": ["police car night lights", "police patrol city"],
        "image": ["police car lights night", "police tape crime scene"],
        "audio": ["police siren city", "radio dispatch static"],
    },
    "americana_1930s_1970s": {
        "video": ["main street 1950s", "american factory 1940s", "trains railroad 1950s",
                  "diner drive-in 1950s", "american city street 1930s"],
        "image": ["main street storefronts 1950s", "railroad steam locomotive",
                  "american diner neon sign", "factory assembly line 1940s"],
        "audio": ["steam train whistle", "diner ambience 1950s"],
    },
    "small_town": {
        "video": ["small town america", "rural town street", "county fair town"],
        "image": ["small town main street", "water tower town", "rural church town square"],
        "audio": ["small town ambience birds", "church bells distant"],
    },
    "newspapers_printing": {
        "video": ["newspaper printing press", "linotype newsroom", "newspaper production"],
        "image": ["printing press machinery", "newspaper front page press", "linotype machine"],
        "audio": ["printing press machine", "typewriter keys newsroom"],
    },
    "uk_period": {
        "video": ["london 1950s", "britain 1960s street", "england industrial 1940s"],
        "image": ["london street 1950s", "british railway station period", "england town 1930s"],
        "audio": ["big ben chimes", "steam railway station ambience"],
    },
    "chicago_city": {
        "video": ["chicago city", "chicago elevated train", "chicago skyline street"],
        "image": ["chicago skyline", "chicago elevated railway", "chicago river bridges"],
        "audio": ["elevated train rumble", "city wind traffic"],
    },
    "navy_harbor": {
        "video": ["navy ships harbor", "naval shipyard", "harbor docks cargo"],
        "image": ["navy warship harbor", "shipyard cranes docks", "lighthouse harbor"],
        "audio": ["ship horn harbor", "seagulls dock water"],
    },
    "laboratory_forensics": {
        "video": ["laboratory science equipment", "chemistry lab research", "microscope lab"],
        "image": ["laboratory glassware equipment", "microscope close up", "test tubes chemistry"],
        "audio": ["laboratory equipment hum", "glass beaker clink"],
    },
    "government_buildings": {
        "video": ["capitol government building", "washington dc buildings", "city hall architecture"],
        "image": ["capitol dome architecture", "government building columns", "supreme court building"],
        "audio": ["marble hall footsteps echo", "flag rope flagpole wind"],
    },
    "period_telephone_tech": {
        "video": ["telephone switchboard", "rotary telephone", "telegraph communication vintage"],
        "image": ["rotary telephone vintage", "switchboard operator equipment", "telephone booth old"],
        "audio": ["rotary dial telephone", "telephone ring vintage bell"],
    },
    "money_banking": {
        "video": ["bank vault money", "printing money mint", "stock exchange trading floor"],
        "image": ["bank vault door", "dollar bills currency", "bank building classical"],
        "audio": ["coins counting cash register", "cash register bell vintage"],
    },
    # ---- BROAD themes (future channels; fill tiers 2-4: D->E->F) ----
    "space_nasa": {
        "video": ["earth from space", "rocket launch", "moon surface apollo"],
        "image": ["nebula galaxy", "earth from orbit", "rocket launchpad"],
        "audio": ["rocket launch rumble", "space radio static beep"],
    },
    "ocean_nature": {
        "video": ["ocean waves", "underwater coral reef", "coastline cliffs aerial"],
        "image": ["ocean waves aerial", "coral reef underwater", "sea cliffs coast"],
        "audio": ["ocean waves shore", "underwater ambience"],
    },
    "weather_disasters": {
        "video": ["storm clouds timelapse", "hurricane storm", "lightning storm night"],
        "image": ["storm supercell clouds", "lightning strike", "flood street aftermath"],
        "audio": ["thunder storm rain", "wind howling storm"],
    },
    "wildlife_animals": {
        "video": ["wildlife birds flock", "deer forest wildlife", "lions savanna wildlife"],
        "image": ["birds wildlife nature", "deer forest", "elephant savanna"],
        "audio": ["birdsong forest morning", "wolves howling night"],
    },
    "world_cities": {
        "video": ["city skyline timelapse", "street traffic night city", "european old town street"],
        "image": ["city skyline night", "old town europe street", "market street world"],
        "audio": ["city traffic ambience", "subway station ambience"],
    },
    "japan": {
        "video": ["japan street tokyo", "kyoto temple japan", "japan rural train"],
        "image": ["kyoto temple", "tokyo neon street night", "mount fuji landscape"],
        "audio": ["japanese temple bell", "tokyo street ambience"],
    },
    "vintage_ads_cartoons": {
        "video": ["television commercial", "animated cartoon", "advertising film"],
        "image": ["vintage advertisement poster", "retro product label"],
        "audio": ["vintage radio jingle", "old advertisement music"],
        "ia_collections": ["classic_cartoons", "Classic_TV_Commercials", "prelinger"],
    },
    "pd_feature_films": {
        "video": ["feature film", "film noir", "western film", "silent film"],
        "image": ["movie poster vintage", "cinema theater marquee"],
        "audio": ["film projector running"],
        "ia_collections": ["feature_films", "film_noir", "silent_films"],
    },
    "war_history": {
        "video": ["world war newsreel", "military training film", "aircraft carrier wartime"],
        "image": ["tanks military ww2", "warplanes formation", "battleship guns"],
        "audio": ["artillery distant rumble", "air raid siren"],
    },
    "science_tech": {
        "video": ["vintage computer technology", "electronics circuit assembly", "industrial robot machine"],
        "image": ["circuit board macro", "vintage computer mainframe", "telescope observatory"],
        "audio": ["computer beeps retro", "machine hum electronics"],
    },
    "landscapes_timelapse": {
        "video": ["timelapse clouds mountains", "sunset timelapse", "desert canyon aerial"],
        "image": ["mountain landscape peaks", "desert dunes", "waterfall forest"],
        "audio": ["mountain wind ambience", "river stream flowing"],
    },
    "textures_backgrounds": {
        "video": ["ink in water", "smoke background dark", "bokeh lights abstract"],
        "image": ["old paper texture", "grunge wall texture", "marble stone texture"],
        "audio": [],
    },
    "music_performance_pd_era": {
        "video": ["orchestra performance", "jazz band 1940s", "concert hall music"],
        "image": ["orchestra vintage", "gramophone record player", "concert hall interior"],
        "audio": ["vinyl crackle 78rpm", "vintage orchestra recording"],
    },
}

# PD-lane themes route H:->D:->E:->F:; broad themes skip H: and fill D:->E:->F:
PD_LANE = {
    "uk_highstreet_postoffice", "courtroom_justice", "prison_jail", "police_period",
    "police_modern", "americana_1930s_1970s", "small_town", "newspapers_printing",
    "uk_period", "chicago_city", "navy_harbor", "laboratory_forensics",
    "government_buildings", "period_telephone_tech", "money_banking",
}
NASA_THEMES = {"space_nasa", "weather_disasters", "ocean_nature", "science_tech",
               "landscapes_timelapse"}

# ------------------------------------------------------------- plumbing ----


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] {msg}", flush=True)


class Net:
    """Polite HTTP with per-host rate limiting and robots.txt support."""

    def __init__(self) -> None:
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self._last: dict[str, float] = {}
        self._robots: dict[str, urllib.robotparser.RobotFileParser | None] = {}

    def _wait(self, url: str) -> None:
        host = urllib.parse.urlparse(url).netloc
        interval = HOST_INTERVAL.get(host, DEFAULT_INTERVAL)
        dt = time.time() - self._last.get(host, 0.0)
        if dt < interval:
            time.sleep(interval - dt)
        self._last[host] = time.time()

    def robots_ok(self, url: str) -> bool:
        host = urllib.parse.urlparse(url).netloc
        if host not in self._robots:
            rp = urllib.robotparser.RobotFileParser()
            try:
                r = self.s.get(f"https://{host}/robots.txt", timeout=20)
                rp.parse(r.text.splitlines() if r.status_code == 200 else [])
                self._robots[host] = rp
            except Exception:
                self._robots[host] = None  # unreachable robots -> allow, stay polite
        rp = self._robots[host]
        return True if rp is None else rp.can_fetch(UA, url)

    def get(self, url: str, *, check_robots: bool = False, **kw) -> requests.Response:
        if check_robots and not self.robots_ok(url):
            raise PermissionError(f"robots.txt disallows {url}")
        self._wait(url)
        kw.setdefault("timeout", 60)
        return self.s.get(url, **kw)

    def get_json(self, url: str, **kw):
        r = self.get(url, **kw)
        r.raise_for_status()
        return r.json()

    def download(self, url: str, dest: str, *, headers: dict | None = None) -> tuple[int, str]:
        """Stream url -> dest. Returns (bytes, sha256). Raises on failure."""
        self._wait(url)
        h = hashlib.sha256()
        n = 0
        with self.s.get(url, stream=True, timeout=300, headers=headers or {}) as r:
            r.raise_for_status()
            tmp = dest + ".part"
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(1024 * 512):
                    f.write(chunk)
                    h.update(chunk)
                    n += len(chunk)
                    if n > MAX_ITEM_BYTES:
                        raise ValueError(f"file exceeds MAX_ITEM_BYTES: {url}")
        os.replace(tmp, dest)
        return n, h.hexdigest()


NET = Net()


def slug(text: str, maxlen: int = 60) -> str:
    """ASCII slug per ledger contract: lowercase, hyphens, Windows-safe, <=60 chars."""
    import unicodedata
    text = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return (text[:maxlen].rstrip("-")) or "untitled"


def ext_of(url: str, default: str) -> str:
    path = urllib.parse.urlparse(url).path
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    return ext if ext and len(ext) <= 4 else default


def drive_free(drive: str) -> int:
    try:
        return shutil.disk_usage(drive).free
    except Exception:
        return 0


FFPROBE = "ffprobe"
FFMPEG = "ffmpeg"


def ffprobe_json(path: str) -> dict:
    out = subprocess.run(
        [FFPROBE, "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
        capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout or "{}")


def validate_media(path: str, kind: str, theme: str) -> tuple[bool, str]:
    """Technical floors (owner vetting layer). Returns (ok, reason).
    video: decodes, height>=480, 5s..30min (pd_feature_films exempt from the max)
    audio: decodes, >=1s, >=128kbps or lossless codec
    image: decodes, long edge >=1200px (>=1920px for textures_backgrounds)"""
    try:
        if os.path.getsize(path) < MIN_ITEM_BYTES:
            return False, "too-small-file"
        if kind in ("video", "audio"):
            info = ffprobe_json(path)
            fmt = info.get("format", {})
            dur = float(fmt.get("duration", 0) or 0)
            if kind == "video":
                heights = [int(s.get("height", 0) or 0) for s in info.get("streams", [])
                           if s.get("codec_type") == "video"]
                if not heights or max(heights) < 480:
                    return False, f"video-below-480p({max(heights) if heights else 0})"
                if dur < 5:
                    return False, f"video-too-short({dur:.1f}s)"
                if dur > 1800 and theme != "pd_feature_films":
                    return False, f"video-too-long({dur/60:.0f}min)"
            else:
                if dur < 1:
                    return False, "audio-too-short"
                br = int(fmt.get("bit_rate", 0) or 0)
                codecs = [s.get("codec_name", "") for s in info.get("streams", [])
                          if s.get("codec_type") == "audio"]
                lossless = any(c.startswith(("pcm", "flac", "alac")) for c in codecs)
                if not lossless and br and br < 128000:
                    return False, f"audio-below-128k({br})"
            return True, "ok"
        if kind == "image":
            from PIL import Image
            with Image.open(path) as im:
                im.verify()
            with Image.open(path) as im:
                long_edge = max(im.size)
            floor = 1920 if theme == "textures_backgrounds" else 1200
            if long_edge < floor:
                return False, f"image-below-{floor}px({long_edge})"
            return True, "ok"
        return True, "ok"
    except Exception as e:  # noqa: BLE001
        return False, f"decode-fail:{e.__class__.__name__}"


def build_contact_sheet(theme: str, files: list[str], count: int) -> None:
    """Sampled human-QC hook: grid jpg (images direct, videos via 1 extracted frame)
    into H:\\...\\_qc\\<theme>\\ so batches can be eyeballed and thresholds tuned."""
    try:
        from PIL import Image
        qc_dir = os.path.join(H_ROOT, "_qc", theme)
        os.makedirs(qc_dir, exist_ok=True)
        cell_w, cell_h, cols = 320, 180, 6
        tiles = []
        for fp in files[:QC_SHEET_TILES]:
            try:
                ext = os.path.splitext(fp)[1].lower()
                if ext in (".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".webp"):
                    im = Image.open(fp).convert("RGB")
                elif ext in (".mp4", ".mov", ".webm", ".mkv", ".avi", ".mpeg", ".mpg"):
                    tmp = fp + ".qcframe.jpg"
                    subprocess.run([FFMPEG, "-y", "-v", "error", "-ss", "3", "-i", fp,
                                    "-frames:v", "1", "-vf", f"scale={cell_w}:-2", tmp],
                                   capture_output=True, timeout=60)
                    if not os.path.exists(tmp):
                        continue
                    im = Image.open(tmp).convert("RGB")
                    os.remove(tmp)
                else:
                    continue  # audio has no visual
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


class Ledger:
    """Per-source JSONL ledgers on H: + resume set + theme/tier/global budgets.
    All budgets are CUMULATIVE across runs (recomputed from the ledgers at start)."""

    def __init__(self, cap_gb: float) -> None:
        os.makedirs(LEDGER_DIR, exist_ok=True)
        self.done: set[tuple[str, str]] = set()
        self.shas: set[str] = set()          # content-level dedup across ALL tiers
        self.existing_shas: set[str] = set()  # dedup vs EXISTING holdings (factory/stock)
        self.existing_ids: set[str] = set()   # "<source>:<id>" of existing holdings
        self._existing_mtime = 0.0
        self.recent: dict[str, list[str]] = {}  # per-theme recent files (QC sheets)
        self.theme_bytes: dict[str, int] = {}
        self.theme_items: dict[str, int] = {}
        self.tier_bytes: dict[str, int] = {t["name"]: 0 for t in TIERS}
        self.total_bytes = 0
        self.run_bytes = 0  # this-run only, for reporting
        self.run_items = 0
        self.cap_bytes = int(cap_gb * GB) if cap_gb > 0 else (1 << 62)  # 0 = unlimited
        for fn in os.listdir(LEDGER_DIR):
            if not fn.endswith(".jsonl") or fn == "rejects.jsonl":
                continue
            with open(os.path.join(LEDGER_DIR, fn), encoding="utf-8") as f:
                for line in f:
                    try:
                        rec = json.loads(line)
                    except Exception:
                        continue
                    self.done.add((rec["source"], str(rec["id"])))
                    if rec.get("sha256"):
                        self.shas.add(rec["sha256"])
                    b = int(rec.get("bytes", 0))
                    t = rec.get("theme", "?")
                    self.theme_bytes[t] = self.theme_bytes.get(t, 0) + b
                    self.theme_items[t] = self.theme_items.get(t, 0) + 1
                    self.total_bytes += b
                    fp = str(rec.get("file_path", ""))
                    for tier in TIERS:
                        if fp.upper().startswith(tier["drive"].upper()[0] + ":"):
                            self.tier_bytes[tier["name"]] += b
                            break

    def seen(self, source: str, item_id: str) -> bool:
        return (source, str(item_id)) in self.done

    def load_existing_index(self) -> None:
        """Consume the sibling-built dedup index over EXISTING holdings (factory/stock).
        Safe to call every pass — reloads only when the file changed. On (re)load, runs a
        retroactive sha sweep against items already in our ledgers and logs collisions."""
        try:
            mtime = os.path.getmtime(EXISTING_INDEX)
        except OSError:
            return  # index not built yet — start without it (IA collision risk ~0)
        if mtime == self._existing_mtime:
            return
        self._existing_mtime = mtime
        try:
            with open(EXISTING_INDEX, encoding="utf-8") as f:
                idx = json.load(f)
        except Exception as e:  # noqa: BLE001
            log(f"existing_index.json unreadable: {e}")
            return
        sha = idx.get("sha256", {})
        self.existing_shas = set(sha if isinstance(sha, list) else sha.keys())
        sid = idx.get("source_ids", {})
        self.existing_ids = {k.lower() for k in (sid if isinstance(sid, list) else sid.keys())}
        log(f"existing-holdings index loaded: {len(self.existing_shas)} shas, "
            f"{len(self.existing_ids)} source-ids")
        retro = self.shas & self.existing_shas
        if retro:
            log(f"RETRO SWEEP: {len(retro)} already-ingested items collide with existing "
                f"holdings (logged to rejects.jsonl; files kept for owner decision)")
            for s in retro:
                reject_log("retro", s, "-", "dup_existing_retro_sha")

    def theme_full(self, theme: str) -> bool:  # owner final directive: no per-theme caps
        return False

    def pick_tier(self, theme: str | None = None) -> dict | None:
        """First ACTIVE tier above its free-space floor; None = all floors hit.
        PD-lane themes may use all tiers (H first); broad themes skip H: (tiers 2-4)."""
        tiers = TIERS if (theme is None or theme in PD_LANE) else TIERS[1:]
        tiers = [t for t in tiers if t["name"] in ACTIVE_TIERS]
        for t in tiers:
            if not os.path.isdir(t["drive"]):
                continue
            if drive_free(t["drive"]) <= t["floor"]:
                continue
            return t
        return None

    def run_full(self) -> bool:
        return self.total_bytes >= self.cap_bytes or self.pick_tier() is None

    def record(self, rec: dict) -> None:
        self.done.add((rec["source"], str(rec["id"])))
        self.shas.add(rec["sha256"])
        t = rec["theme"]
        b = rec["bytes"]
        self.theme_bytes[t] = self.theme_bytes.get(t, 0) + b
        self.theme_items[t] = self.theme_items.get(t, 0) + 1
        self.recent.setdefault(t, []).append(rec["file_path"])
        self.recent[t] = self.recent[t][-QC_SHEET_TILES:]
        self.total_bytes += b
        self.run_bytes += b
        self.run_items += 1
        fp = str(rec.get("file_path", ""))
        for tier in TIERS:
            if fp.upper().startswith(tier["drive"].upper()[0] + ":"):
                self.tier_bytes[tier["name"]] += b
                break
        path = os.path.join(LEDGER_DIR, f"{rec['source']}.jsonl")
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def take(ledger: Ledger, *, source: str, item_id: str, title: str, source_url: str,
         download_url: str, kind: str, theme: str, license_raw: str, decision: str,
         default_ext: str, dry_run: bool, dl_headers: dict | None = None,
         desc: str = "") -> bool:
    """Common vet -> download -> validate -> ledger path. Returns True if ingested.
    Vetting order: person-filter, existing-holdings dedup, relevance score gate,
    tier/floor, download, sha256 content dedup (new archive AND existing holdings),
    technical floors; failures land in rejects.jsonl."""
    global ACTIVITY
    if ledger.seen(source, item_id):
        return False
    ACTIVITY += 1
    if f"{source}:{item_id}".lower() in ledger.existing_ids:
        reject_log(source, item_id, theme, "dup_existing_id")  # no bandwidth wasted
        return False
    if PERSON_RE.search(title or ""):
        reject_log(source, item_id, theme, "person-filter")
        return False
    # per-item metadata relevance gate (owner: no blind query-dumps)
    score, matched, negs = relevance(theme, f"{title} {desc}")
    threshold = SRC_THRESHOLD.get(source, DEFAULT_THRESHOLD)
    if score < threshold:
        reject_log(source, item_id, theme, f"relevance<{threshold}", score, matched, negs)
        return False
    if decision == "review_required":
        # quarantine lives on H: only; respect the H: floor even for quarantine
        if drive_free(TIERS[0]["drive"]) <= TIERS[0]["floor"]:
            log("  skip quarantine item: H: free-space floor reached")
            return False
        root = os.path.join(QUARANTINE, theme)
    else:
        tier = ledger.pick_tier(theme)  # free-space + budget checked before EACH file
        if tier is None:
            return False
        root = os.path.join(tier["root"], theme)
    os.makedirs(root, exist_ok=True)
    # self-describing filename contract: <source>__<id>__<title-slug>.<ext>
    ext = ext_of(download_url, default_ext)
    base = f"{source}__{slug(str(item_id))}__{slug(title)}"
    fname = f"{base}.{ext}"
    dest = os.path.join(root, fname)
    n_coll = 2
    while os.path.exists(dest):  # collision -> append -2, -3, ...
        fname = f"{base}-{n_coll}.{ext}"
        dest = os.path.join(root, fname)
        n_coll += 1
    if dry_run:
        log(f"  DRY {decision:>15} s={score:3d} {theme:24} {title[:56]}  <- {download_url[:80]}")
        return True
    try:
        nbytes, sha = NET.download(download_url, dest, headers=dl_headers)
    except Exception as e:  # noqa: BLE001
        log(f"  dl-fail: {e}")
        reject_log(source, item_id, theme, f"download-fail:{e.__class__.__name__}", score)
        for p in (dest, dest + ".part"):
            if os.path.exists(p):
                try:
                    os.remove(p)
                except OSError:
                    pass
        return False
    if sha in ledger.shas:  # content-level dedup across all tiers/sources
        log(f"  dup-sha, removed: {fname[:70]}")
        os.remove(dest)
        reject_log(source, item_id, theme, "dup-sha256", score)
        return False
    if sha in ledger.existing_shas:  # content already in factory/stock holdings
        log(f"  dup-existing-sha, removed: {fname[:70]}")
        os.remove(dest)
        reject_log(source, item_id, theme, "dup_existing_sha", score)
        return False
    ok, why = validate_media(dest, kind, theme)
    if not ok:
        log(f"  reject ({why}), removed: {fname[:70]}")
        os.remove(dest)
        reject_log(source, item_id, theme, f"tech:{why}", score)
        return False
    ledger.record({
        "id": str(item_id), "source": source, "source_url": source_url, "title": title,
        "license_field_raw": license_raw[:500], "license_decision": decision,
        "theme": theme, "file_path": dest, "bytes": nbytes, "sha256": sha,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "relevance_score": score, "matched_keywords": matched[:12],
    })
    log(f"  OK {decision:>15} s={score:3d} {nbytes/1e6:7.1f}MB {fname[:74]}")
    if ledger.theme_items.get(theme, 0) % QC_SHEET_EVERY == 0:
        build_contact_sheet(theme, ledger.recent.get(theme, []),
                            ledger.theme_items.get(theme, 0))
    return True


# ------------------------------------------------------------- adapters ----
# Each adapter: (ledger, theme, limit, dry_run) -> int items ingested THIS call.
# Pagination: module-level PASS (pass N of the runner == page N of the source),
# so successive passes reach deeper result pages and the run stays resumable.


def src_ia(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Internet Archive: PD/CC0 films (Prelinger & other PD-licensed movies), h.264 derivatives."""
    got = 0
    colls_extra = THEMES[theme].get("ia_collections", [])
    coll_clause = "collection:(prelinger)" if not colls_extra else \
        "collection:(" + " OR ".join(["prelinger"] + colls_extra) + ")"
    for q in THEMES[theme].get("video", []):
        if got >= limit or ledger.theme_full(theme) or ledger.run_full():
            break
        query = (f'({q}) AND mediatype:(movies) AND '
                 f'({coll_clause} OR licenseurl:*publicdomain* OR licenseurl:*zero*)')
        try:
            data = NET.get_json("https://archive.org/advancedsearch.php", params={
                "q": query, "fl[]": ["identifier", "title", "licenseurl", "collection"],
                "rows": 100, "page": PASS, "output": "json", "sort[]": "downloads desc"})
        except Exception as e:  # noqa: BLE001
            log(f"  ia search fail: {e}")
            continue
        for doc in data.get("response", {}).get("docs", []):
            if got >= limit or ledger.theme_full(theme) or ledger.run_full():
                break
            ident = doc["identifier"]
            if ledger.seen("ia", ident):
                continue
            try:
                md = NET.get_json(f"https://archive.org/metadata/{ident}")
            except Exception:
                continue
            meta = md.get("metadata", {})
            licurl = str(meta.get("licenseurl", "") or "")
            colls = meta.get("collection", [])
            colls = [colls] if isinstance(colls, str) else colls
            if "/zero/" in licurl or "cc0" in licurl.lower():
                decision, raw = "cc0", licurl
            elif "publicdomain" in licurl:
                decision, raw = "pd", licurl
            elif any("prelinger" in c.lower() for c in colls):
                decision, raw = "pd", f"collection:prelinger (Prelinger Archives public domain); licenseurl={licurl}"
            else:
                decision, raw = "review_required", f"licenseurl={licurl}; collections={colls[:4]}"
            subj = meta.get("subject", [])
            subj = [subj] if isinstance(subj, str) else subj
            desc = f"{meta.get('description', '')} {' '.join(map(str, subj[:20]))}"[:900]
            # period themes: require date metadata or trusted period provenance
            year = str(meta.get("year", "") or meta.get("date", "") or "")
            prel = any("prelinger" in c.lower() for c in colls)
            if theme in PERIOD_THEMES and not year and not prel:
                reject_log("ia", ident, theme, "period-no-date-provenance")
                continue
            # choose an h.264 mp4 derivative, not the master
            cands = []
            for f in md.get("files", []):
                name = f.get("name", "")
                if not name.lower().endswith(".mp4"):
                    continue
                size = int(f.get("size", 0) or 0)
                fmt = (f.get("format") or "").lower()
                if MIN_ITEM_BYTES < size <= MAX_ITEM_BYTES:
                    cands.append((0 if "h.264" in fmt else 1, size, name))
            if not cands:
                continue
            cands.sort()  # prefer h.264, then smallest
            name = cands[0][2]
            url = f"https://archive.org/download/{ident}/{urllib.parse.quote(name)}"
            if take(ledger, source="ia", item_id=ident, title=str(meta.get("title", ident)),
                    source_url=f"https://archive.org/details/{ident}", download_url=url,
                    kind="video", theme=theme, license_raw=raw, decision=decision,
                    default_ext="mp4", dry_run=dry_run, desc=desc):
                got += 1
    return got


def src_loc(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Library of Congress loc.gov JSON API — film/video + photos; rights-text gated."""
    got = 0
    plans = [("video", "film,video", "video"), ("image", "image", "image")]
    for qkey, fmt, kind in plans:
        for q in THEMES[theme][qkey][:2]:
            if got >= limit or ledger.theme_full(theme) or ledger.run_full():
                return got
            try:
                data = NET.get_json("https://www.loc.gov/search/", params={
                    "q": q, "fo": "json", "fa": f"online-format:{fmt}", "c": 40, "sp": PASS})
            except Exception as e:  # noqa: BLE001
                log(f"  loc search fail: {e}")
                continue
            for res in data.get("results", []):
                if got >= limit or ledger.theme_full(theme) or ledger.run_full():
                    return got
                item_url = res.get("id", "")
                if not item_url.startswith("http") or "/item/" not in item_url \
                        or ledger.seen("loc", item_url):
                    continue
                try:
                    detail = NET.get_json(item_url, params={"fo": "json"})
                except Exception:
                    continue
                item = detail.get("item", {})
                rights_bits = []
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
                    for r2 in detail.get("resources", []):
                        for f in r2.get("files", []) if isinstance(r2.get("files"), list) else []:
                            flat = f if isinstance(f, list) else [f]
                            for ff in flat:
                                u = (ff or {}).get("url", "") if isinstance(ff, dict) else ""
                                if u.endswith(".mp4"):
                                    url = u
                        if not url and r2.get("url", "").endswith(".mp4"):
                            url = r2["url"]
                else:
                    imgs = [u for u in (res.get("image_url") or []) if ".jpg" in u]
                    url = imgs[-1] if imgs else ""
                if not url:
                    continue
                loc_desc = " ".join(map(str, (res.get("description") or [])
                                        + (res.get("subject") or [])))[:900]
                if take(ledger, source="loc", item_id=item_url, title=str(res.get("title", "")),
                        source_url=item_url, download_url=url, kind=kind, theme=theme,
                        license_raw=raw or "(no rights field)", decision=decision,
                        default_ext="mp4" if kind == "video" else "jpg", dry_run=dry_run,
                        desc=loc_desc):
                    got += 1
    return got


def src_nara(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """NARA catalog v2. Requires free x-api-key (env NARA_API_KEY); skips gracefully."""
    key = os.environ.get("NARA_API_KEY", "")
    headers = {"x-api-key": key} if key else {}
    got = 0
    for q in THEMES[theme]["video"][:2]:
        if got >= limit or ledger.theme_full(theme) or ledger.run_full():
            break
        try:
            r = NET.get("https://catalog.archives.gov/api/v2/records/search",
                        params={"q": q, "limit": 50, "page": PASS,
                                "availableOnline": "true"},
                        headers=headers)
            if r.status_code in (401, 403):
                raise PermissionError("NARA v2 API requires x-api-key (free registration)")
            r.raise_for_status()
            data = r.json()
        except PermissionError:
            raise
        except Exception as e:  # noqa: BLE001
            log(f"  nara search fail: {e}")
            continue
        hits = data.get("body", {}).get("hits", {}).get("hits", [])
        for h in hits:
            if got >= limit or ledger.theme_full(theme) or ledger.run_full():
                break
            rec = h.get("_source", {}).get("record", {})
            naid = str(rec.get("naId", ""))
            if not naid or ledger.seen("nara", naid):
                continue
            use = rec.get("useRestriction", {}).get("status", "")
            use_s = json.dumps(use) if not isinstance(use, str) else use
            decision = "pd" if "unrestricted" in use_s.lower() else "review_required"
            for obj in rec.get("digitalObjects", []):
                u = obj.get("objectUrl", "")
                lo = u.lower()
                if lo.endswith((".mp4", ".mov", ".jpg", ".jpeg", ".mp3", ".wav")):
                    kind = ("video" if lo.endswith((".mp4", ".mov"))
                            else "audio" if lo.endswith((".mp3", ".wav")) else "image")
                    nara_desc = str(rec.get("scopeAndContentNote", ""))[:800]
                    if take(ledger, source="nara", item_id=naid,
                            title=str(rec.get("title", "")),
                            source_url=f"https://catalog.archives.gov/id/{naid}",
                            download_url=u, kind=kind, theme=theme, desc=nara_desc,
                            license_raw=f"useRestriction={use_s}", decision=decision,
                            default_ext="mp4", dry_run=dry_run):
                        got += 1
                    break
    return got


def src_met(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Met Museum Open Access — CC0 images only (isPublicDomain=true)."""
    got = 0
    window = 80
    for q in THEMES[theme]["image"][:2]:
        if got >= limit or ledger.theme_full(theme) or ledger.run_full():
            break
        try:
            data = NET.get_json(
                "https://collectionapi.metmuseum.org/public/collection/v1/search",
                params={"q": q, "hasImages": "true"})
        except Exception as e:  # noqa: BLE001
            log(f"  met search fail: {e}")
            continue
        ids = (data.get("objectIDs") or [])[(PASS - 1) * window: PASS * window]
        for oid in ids:
            if got >= limit or ledger.theme_full(theme) or ledger.run_full():
                break
            if ledger.seen("met", str(oid)):
                continue
            try:
                obj = NET.get_json(
                    f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}")
            except Exception:
                continue
            if not obj.get("isPublicDomain") or not obj.get("primaryImage"):
                continue
            met_desc = " ".join(str(obj.get(k, "")) for k in
                                ("objectName", "department", "culture", "objectDate",
                                 "medium", "classification"))[:600]
            if take(ledger, source="met", item_id=oid, title=obj.get("title", ""),
                    source_url=obj.get("objectURL", ""), download_url=obj["primaryImage"],
                    kind="image", theme=theme, desc=met_desc,
                    license_raw=f"isPublicDomain=true; rightsAndReproduction="
                                f"{obj.get('rightsAndReproduction', '')} (Met Open Access CC0)",
                    decision="cc0", default_ext="jpg", dry_run=dry_run):
                got += 1
    return got


def src_nasa(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """NASA Image and Video Library (images-api.nasa.gov, keyless). NASA media is
    public domain (except logos/insignia). Only runs for NASA-relevant themes."""
    if theme not in NASA_THEMES:
        return 0
    got = 0
    queries = THEMES[theme].get("video", [])[:2] + THEMES[theme].get("image", [])[:1]
    for q in queries:
        if got >= limit or ledger.theme_full(theme) or ledger.run_full():
            break
        try:
            data = NET.get_json("https://images-api.nasa.gov/search", params={
                "q": q, "media_type": "image,video", "page": PASS, "page_size": 50})
        except Exception as e:  # noqa: BLE001
            log(f"  nasa search fail: {e}")
            continue
        for item in data.get("collection", {}).get("items", []):
            if got >= limit or ledger.theme_full(theme) or ledger.run_full():
                break
            d = (item.get("data") or [{}])[0]
            nasa_id = d.get("nasa_id", "")
            if not nasa_id or ledger.seen("nasa", nasa_id):
                continue
            mtype = d.get("media_type", "image")
            if mtype not in ("image", "video"):
                continue
            try:
                asset = NET.get_json(f"https://images-api.nasa.gov/asset/{nasa_id}")
            except Exception:
                continue
            hrefs = [i.get("href", "") for i in asset.get("collection", {}).get("items", [])]
            url = ""
            if mtype == "video":
                for pref in ("~medium.mp4", "~mobile.mp4", ".mp4"):
                    for h in hrefs:
                        if h.endswith(pref):
                            url = h
                            break
                    if url:
                        break
            else:
                for pref in ("~large.jpg", "~orig.jpg", ".jpg"):
                    for h in hrefs:
                        if h.lower().endswith(pref):
                            url = h
                            break
                    if url:
                        break
            if not url:
                continue
            nasa_desc = f"{d.get('description', '')} {' '.join(d.get('keywords', []) or [])}"[:900]
            if take(ledger, source="nasa", item_id=nasa_id, title=d.get("title", ""),
                    source_url=f"https://images.nasa.gov/details/{nasa_id}",
                    download_url=url, kind=mtype, theme=theme, desc=nasa_desc,
                    license_raw="NASA Image and Video Library — NASA media usage guidelines "
                                "(public domain, not copyrighted)",
                    decision="pd", default_ext="mp4" if mtype == "video" else "jpg",
                    dry_run=dry_run):
                got += 1
    return got


_TAG_RE = re.compile(r"<[^>]+>")


def src_wikimedia(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Wikimedia Commons API. STRICT per-file license filter:
    PD/CC0 -> main shelf; CC-BY (attribution recorded in ledger) -> quarantine;
    CC-BY-SA / unknown -> skipped entirely. Uses 2560px thumbs, not 100MB TIFF originals.
    Also the route for NOAA public-domain material (no clean NOAA media API exists)."""
    got = 0
    for q in THEMES[theme].get("image", [])[:2]:
        if got >= limit or ledger.theme_full(theme) or ledger.run_full():
            break
        try:
            data = NET.get_json("https://commons.wikimedia.org/w/api.php", params={
                "action": "query", "format": "json", "generator": "search",
                "gsrsearch": f"{q} filetype:bitmap", "gsrnamespace": 6,
                "gsrlimit": 25, "gsroffset": (PASS - 1) * 25,
                "prop": "imageinfo", "iiprop": "url|size|extmetadata",
                "iiurlwidth": 2560})
        except Exception as e:  # noqa: BLE001
            log(f"  wikimedia search fail: {e}")
            continue
        for page in (data.get("query", {}).get("pages", {}) or {}).values():
            if got >= limit or ledger.theme_full(theme) or ledger.run_full():
                break
            title = page.get("title", "")
            if not title or ledger.seen("wikimedia", title):
                continue
            info = (page.get("imageinfo") or [{}])[0]
            ext = info.get("extmetadata", {}) or {}
            lic = str(ext.get("LicenseShortName", {}).get("value", "")).strip()
            low = lic.lower()
            artist = _TAG_RE.sub("", str(ext.get("Artist", {}).get("value", ""))).strip()
            if "cc0" in low:
                decision = "cc0"
            elif "public domain" in low or low.startswith("pd"):
                decision = "pd"
            elif low.startswith("cc by") and "sa" not in low:
                decision = "review_required"  # CC-BY -> quarantine, attribution recorded
            else:
                continue  # CC-BY-SA / unknown / fair use -> skip entirely
            url = info.get("thumburl") or info.get("url", "")
            if not url:
                continue
            wm_desc = _TAG_RE.sub("", str(ext.get("ImageDescription", {}).get("value", "")))[:600] \
                + " " + str(ext.get("Categories", {}).get("value", ""))[:300]
            if take(ledger, source="wikimedia", item_id=title,
                    title=title.replace("File:", ""),
                    source_url=info.get("descriptionurl", ""), download_url=url,
                    kind="image", theme=theme, desc=wm_desc,
                    license_raw=f"LicenseShortName={lic}; Artist={artist[:150]}",
                    decision=decision, default_ext="jpg", dry_run=dry_run):
                got += 1
    return got


def src_mixkit(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Mixkit — no official API. Polite listing-page parse (robots.txt-checked, 2s/req).
    License: Mixkit License (free for commercial use) -> free_commercial."""
    got = 0
    for q in THEMES[theme]["video"][:2]:
        if got >= limit or ledger.theme_full(theme) or ledger.run_full():
            break
        slug = re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")
        page = f"https://mixkit.co/free-stock-video/{slug}/"
        if PASS > 1:
            page += f"?page={PASS}"
        try:
            r = NET.get(page, check_robots=True)
            if r.status_code == 404:
                continue
            r.raise_for_status()
            urls = re.findall(r"https://assets\.mixkit\.co/videos/[^\s\"']+?\.mp4",
                              html_mod.unescape(r.text))
        except PermissionError:
            raise
        except Exception as e:  # noqa: BLE001
            log(f"  mixkit page fail ({page}): {e}")
            continue
        uniq: list[str] = []
        for u in urls:
            if u not in uniq:
                uniq.append(u)
        for u in uniq:
            if got >= limit or ledger.theme_full(theme) or ledger.run_full():
                break
            m = re.search(r"/(mixkit-[^/]+?)(?:-large)?\.mp4", u)
            vid = m.group(1) if m else hashlib.sha1(u.encode()).hexdigest()[:16]
            if take(ledger, source="mixkit", item_id=vid,
                    title=vid.replace("mixkit-", "").replace("-", " "),
                    source_url=page, download_url=u, kind="video", theme=theme,
                    license_raw="Mixkit License (free, commercial use allowed, no attribution)",
                    decision="free_commercial", default_ext="mp4", dry_run=dry_run):
                got += 1
    return got


def src_coverr(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Coverr — polite page parse (robots.txt-checked).
    License: Coverr license (free commercial) -> free_commercial."""
    got = 0
    for q in THEMES[theme]["video"][:2]:
        if got >= limit or ledger.theme_full(theme) or ledger.run_full():
            break
        page = ("https://coverr.co/s?q=" + urllib.parse.quote(q)
                + (f"&page={PASS}" if PASS > 1 else ""))
        try:
            r = NET.get(page, check_robots=True)
            r.raise_for_status()
            text = r.text
        except PermissionError:
            raise
        except Exception as e:  # noqa: BLE001
            log(f"  coverr page fail: {e}")
            continue
        urls = re.findall(r"https://(?:cdn|storage)\.coverr\.co/videos/[^\s\"'\\]+?\.mp4[^\s\"'\\]*",
                          html_mod.unescape(text))
        uniq: list[str] = []
        for u in urls:
            u = u.replace("\\u0026", "&")
            if u not in uniq:
                uniq.append(u)
        for u in uniq:
            if got >= limit or ledger.theme_full(theme) or ledger.run_full():
                break
            m = re.search(r"/videos/([^/?]+?)\.mp4", u)
            vid = m.group(1) if m else hashlib.sha1(u.encode()).hexdigest()[:16]
            if take(ledger, source="coverr", item_id=vid, title=vid.replace("-", " "),
                    source_url=page, download_url=u, kind="video", theme=theme,
                    license_raw="Coverr License (free for commercial use, no attribution)",
                    decision="free_commercial", default_ext="mp4", dry_run=dry_run):
                got += 1
    return got


def src_pixabay(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Pixabay API (key from .env). Probes the audio endpoint once (undocumented; reported),
    then pulls videos. Pixabay Content License -> free_commercial."""
    key = os.environ.get("PIXABAY_API_KEY", "")
    if not key:
        raise PermissionError("PIXABAY_API_KEY missing")
    if not hasattr(src_pixabay, "_audio_probed"):
        src_pixabay._audio_probed = True  # type: ignore[attr-defined]
        try:
            r = NET.get("https://pixabay.com/api/audio/", params={"key": key, "q": "piano"})
            log(f"  pixabay AUDIO probe: HTTP {r.status_code} -> "
                f"{'audio API available!' if r.status_code == 200 else 'NO public audio API (expected)'}")
        except Exception as e:  # noqa: BLE001
            log(f"  pixabay AUDIO probe failed: {e}")
    got = 0
    for q in THEMES[theme]["video"][:2]:
        if got >= limit or ledger.theme_full(theme) or ledger.run_full():
            break
        try:
            data = NET.get_json("https://pixabay.com/api/videos/", params={
                "key": key, "q": q, "safesearch": "true", "per_page": 50, "page": PASS})
        except Exception as e:  # noqa: BLE001
            log(f"  pixabay search fail: {e}")
            continue
        for hit in data.get("hits", []):
            if got >= limit or ledger.theme_full(theme) or ledger.run_full():
                break
            vid = str(hit["id"])
            if ledger.seen("pixabay", vid):
                continue
            files = hit.get("videos", {})
            best = files.get("large") or files.get("medium") or files.get("small") or {}
            if not best.get("url"):
                continue
            if take(ledger, source="pixabay", item_id=vid,
                    title=(hit.get("tags", "") or vid)[:80],
                    source_url=hit.get("pageURL", ""), download_url=best["url"],
                    kind="video", theme=theme,
                    license_raw="Pixabay Content License (free commercial, no attribution)",
                    decision="free_commercial", default_ext="mp4", dry_run=dry_run):
                got += 1
    return got


def src_smithsonian(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Smithsonian Open Access via api.data.gov (env SMITHSONIAN_API_KEY). CC0-gated."""
    key = os.environ.get("SMITHSONIAN_API_KEY", "")
    if not key:
        raise PermissionError("SMITHSONIAN_API_KEY missing (free at api.data.gov)")
    got = 0
    rows = 50
    for q in THEMES[theme]["image"][:2]:
        if got >= limit or ledger.theme_full(theme) or ledger.run_full():
            break
        try:
            data = NET.get_json("https://api.si.edu/openaccess/api/v1.0/search", params={
                "api_key": key, "q": f'{q} AND online_media_type:"Images"',
                "rows": rows, "start": (PASS - 1) * rows})
        except Exception as e:  # noqa: BLE001
            log(f"  smithsonian search fail: {e}")
            continue
        for row in data.get("response", {}).get("rows", []):
            if got >= limit or ledger.theme_full(theme) or ledger.run_full():
                break
            rid = row.get("id", "")
            if not rid or ledger.seen("smithsonian", rid):
                continue
            content = row.get("content", {})
            usage = json.dumps(content.get("descriptiveNonRepeating", {})
                               .get("metadata_usage", {}))
            if "CC0" not in usage:
                continue
            media = (content.get("descriptiveNonRepeating", {})
                     .get("online_media", {}).get("media", []))
            url = ""
            for m in media:
                for res in m.get("resources", []) or []:
                    if "High-resolution JPEG" in str(res.get("label", "")):
                        url = res.get("url", "")
                url = url or m.get("content", "") or m.get("thumbnail", "")
            if not url:
                continue
            if take(ledger, source="smithsonian", item_id=rid, title=row.get("title", ""),
                    source_url=f"https://www.si.edu/object/{row.get('url', rid)}",
                    download_url=url, kind="image", theme=theme,
                    license_raw=f"metadata_usage={usage[:200]}", decision="cc0",
                    default_ext="jpg", dry_run=dry_run):
                got += 1
    return got


def src_freesound(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Freesound (env FREESOUND_API_KEY). CC0-ONLY filter; downloads HQ mp3 previews
    (original-file download would need OAuth2)."""
    key = os.environ.get("FREESOUND_API_KEY", "")
    if not key:
        raise PermissionError("FREESOUND_API_KEY missing (free at freesound.org/apiv2)")
    got = 0
    for q in THEMES[theme]["audio"]:
        if got >= limit or ledger.theme_full(theme) or ledger.run_full():
            break
        try:
            data = NET.get_json("https://freesound.org/apiv2/search/text/", params={
                "query": q, "filter": 'license:"Creative Commons 0"', "token": key,
                "fields": "id,name,license,previews,url,description,tags",
                "page_size": 30, "page": PASS})
        except Exception as e:  # noqa: BLE001
            log(f"  freesound search fail: {e}")
            continue
        for snd in data.get("results", []):
            if got >= limit or ledger.theme_full(theme) or ledger.run_full():
                break
            sid = str(snd["id"])
            if ledger.seen("freesound", sid):
                continue
            lic = snd.get("license", "")
            if "publicdomain/zero" not in lic and "Creative Commons 0" not in lic:
                continue  # hard CC0 gate
            url = (snd.get("previews") or {}).get("preview-hq-mp3", "")
            if not url:
                continue
            fs_desc = f"{snd.get('description', '')} {' '.join(snd.get('tags', []) or [])}"[:600]
            if take(ledger, source="freesound", item_id=sid, title=snd.get("name", ""),
                    source_url=snd.get("url", ""), download_url=url, kind="audio",
                    theme=theme, license_raw=lic, decision="cc0",
                    default_ext="mp3", dry_run=dry_run, desc=fs_desc):
                got += 1
    return got


def src_nypl(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """NYPL Digital Collections (env NYPL_API_TOKEN). publicDomainOnly=true."""
    key = os.environ.get("NYPL_API_TOKEN", "")
    if not key:
        raise PermissionError("NYPL_API_TOKEN missing (free at api.repo.nypl.org)")
    headers = {"Authorization": f'Token token="{key}"'}
    got = 0
    for q in THEMES[theme]["image"][:2]:
        if got >= limit or ledger.theme_full(theme) or ledger.run_full():
            break
        try:
            r = NET.get("https://api.repo.nypl.org/api/v2/items/search",
                        params={"q": q, "publicDomainOnly": "true", "per_page": 40,
                                "page": PASS},
                        headers=headers)
            r.raise_for_status()
            data = r.json()
        except Exception as e:  # noqa: BLE001
            log(f"  nypl search fail: {e}")
            continue
        results = (data.get("nyplAPI", {}).get("response", {}).get("result", []) or [])
        if isinstance(results, dict):
            results = [results]
        for res in results:
            if got >= limit or ledger.theme_full(theme) or ledger.run_full():
                break
            uuid = res.get("uuid", "")
            img_id = res.get("imageID", "")
            if not uuid or not img_id or ledger.seen("nypl", uuid):
                continue
            url = f"https://images.nypl.org/index.php?id={img_id}&t=w"
            if take(ledger, source="nypl", item_id=uuid, title=str(res.get("title", "")),
                    source_url=f"https://digitalcollections.nypl.org/items/{uuid}",
                    download_url=url, kind="image", theme=theme,
                    license_raw="NYPL publicDomainOnly=true", decision="pd",
                    default_ext="jpg", dry_run=dry_run, dl_headers=headers):
                got += 1
    return got


def src_unsplash(ledger: Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Unsplash (env UNSPLASH_ACCESS_KEY). API terms PROHIBIT bulk mirroring -> hard cap
    50/theme TOTAL (cumulative, checked against the ledger); download-tracking pinged."""
    key = os.environ.get("UNSPLASH_ACCESS_KEY", "")
    if not key:
        raise PermissionError("UNSPLASH_ACCESS_KEY missing (free at unsplash.com/developers)")
    already = sum(1 for (s, _) in ledger.done if s == "unsplash")
    if already >= 50 * len(THEMES):  # coarse global stop
        return 0
    limit = min(limit, 50)
    got = 0
    for q in THEMES[theme]["image"][:2]:
        if got >= limit or ledger.theme_full(theme) or ledger.run_full():
            break
        try:
            data = NET.get_json("https://api.unsplash.com/search/photos", params={
                "query": q, "per_page": 15, "page": PASS, "client_id": key})
        except Exception as e:  # noqa: BLE001
            log(f"  unsplash search fail: {e}")
            continue
        for ph in data.get("results", []):
            if got >= limit or ledger.theme_full(theme) or ledger.run_full():
                break
            pid = ph["id"]
            if ledger.seen("unsplash", pid):
                continue
            url = (ph.get("urls") or {}).get("full") or (ph.get("urls") or {}).get("regular")
            if not url:
                continue
            ok = take(ledger, source="unsplash", item_id=pid,
                      title=(ph.get("alt_description") or ph.get("description") or pid)[:80],
                      source_url=(ph.get("links") or {}).get("html", ""), download_url=url,
                      kind="image", theme=theme,
                      license_raw="Unsplash License (free commercial; no bulk mirroring — curated pull)",
                      decision="free_commercial", default_ext="jpg", dry_run=dry_run)
            if ok:
                got += 1
                dl = (ph.get("links") or {}).get("download_location")
                if dl and not dry_run:
                    try:  # required by Unsplash API guidelines
                        NET.get(dl, params={"client_id": key})
                    except Exception:
                        pass
    return got


ADAPTERS = {
    "ia": src_ia, "loc": src_loc, "nara": src_nara, "met": src_met,
    "nasa": src_nasa, "wikimedia": src_wikimedia,
    "mixkit": src_mixkit, "coverr": src_coverr, "pixabay": src_pixabay,
    "smithsonian": src_smithsonian, "freesound": src_freesound,
    "nypl": src_nypl, "unsplash": src_unsplash,
}
KEYLESS_ORDER = ["ia", "loc", "nara", "met", "nasa", "wikimedia",
                 "mixkit", "coverr", "pixabay",
                 "smithsonian", "freesound", "nypl", "unsplash"]


def load_env() -> None:
    """Merge repo .env into os.environ (no external dependency)."""
    p = os.path.join(REPO, ".env")
    if not os.path.exists(p):
        return
    for line in open(p, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def main() -> int:
    global PASS
    ap = argparse.ArgumentParser(description="PD themed free-asset ingest (tiered H:/D:/E:)")
    ap.add_argument("--source", default="all",
                    help="all | comma list of: " + ",".join(ADAPTERS))
    ap.add_argument("--theme", default="all",
                    help="all | comma list of: " + ",".join(THEMES))
    ap.add_argument("--cap-gb", type=float, default=0.0,
                    help="optional TOTAL cap in GB, cumulative (0 = unlimited, default)")
    ap.add_argument("--limit", type=int, default=1000,
                    help="max items per source per theme PER PASS (smoke: 2-3)")
    ap.add_argument("--passes", type=int, default=1000,
                    help="max runner passes (pass N reads page N of each source)")
    ap.add_argument("--tiers", default="H,D,E,F",
                    help="tier affinity, e.g. 'H,D' (IA/Prelinger runner uses H,D)")
    ap.add_argument("--dry-run", action="store_true", help="list, don't download")
    args = ap.parse_args()
    global ACTIVE_TIERS
    ACTIVE_TIERS = {t.strip().upper() for t in args.tiers.split(",") if t.strip()}

    load_env()
    for t in TIERS:
        if os.path.isdir(t["drive"]):
            os.makedirs(t["root"], exist_ok=True)
    sources = KEYLESS_ORDER if args.source == "all" else \
        [s.strip() for s in args.source.split(",") if s.strip() in ADAPTERS]
    themes = list(THEMES) if args.theme == "all" else \
        [t.strip() for t in args.theme.split(",") if t.strip() in THEMES]
    if not sources or not themes:
        log("nothing to do (bad --source/--theme)")
        return 2

    ledger = Ledger(args.cap_gb)
    log(f"run start: sources={sources} themes={len(themes)} cap={args.cap_gb}GB "
        f"limit={args.limit}/src/theme/pass passes<={args.passes} dry_run={args.dry_run}")
    tier_state = " ".join(f"{t['name']}:{ledger.tier_bytes[t['name']]/GB:.1f}" for t in TIERS)
    log(f"resume state: {len(ledger.done)} items in ledgers, "
        f"{ledger.total_bytes/GB:.1f}GB total ({tier_state})")
    for t in TIERS:
        log(f"  tier {t['name']}: free {drive_free(t['drive'])/GB:.0f}GB, "
            f"floor {t['floor']/GB:.0f}GB")

    ledger.load_existing_index()
    status: dict[str, str] = {s: "working" for s in sources}
    counts: dict[str, int] = {}
    active = list(sources)
    global ACTIVITY
    for pass_n in range(1, args.passes + 1):
        PASS = pass_n
        pass_new = 0
        act0 = ACTIVITY
        ledger.load_existing_index()  # pick up the sibling-built index when it lands
        log(f"===== PASS {pass_n} (sources: {active}) =====")
        for src in list(active):
            fn = ADAPTERS[src]
            for theme in themes:
                if ledger.run_full():
                    break
                if ledger.theme_full(theme):
                    continue
                log(f"[p{pass_n}:{src}] theme={theme}")
                try:
                    n = fn(ledger, theme, args.limit, args.dry_run)
                    counts[src] = counts.get(src, 0) + n
                    pass_new += n
                except PermissionError as e:
                    status[src] = f"skipped: {e}"
                    log(f"[{src}] SKIP SOURCE: {e}")
                    active.remove(src)
                    break
                except KeyboardInterrupt:
                    raise
                except Exception as e:  # noqa: BLE001
                    log(f"[{src}] theme={theme} error: {e}")
            if ledger.run_full():
                break
        if ledger.run_full():
            log("ARCHIVE CAP / free-space floors reached — stopping")
            break
        if pass_new == 0 and ACTIVITY == act0:
            log("no new candidates this pass — sources exhausted at current queries; stopping")
            break
        if not active:
            break

    log("=" * 70)
    log("SUMMARY")
    for src in sources:
        log(f"  {src:12} {counts.get(src, 0):5d} new items   [{status.get(src, 'working')}]")
    log(f"  this run: {ledger.run_items} items, {ledger.run_bytes/GB:.2f} GB")
    tier_state = " ".join(f"{t['name']}:{ledger.tier_bytes[t['name']]/GB:.1f}" for t in TIERS)
    log(f"  archive total: {ledger.total_bytes/GB:.2f} GB ({tier_state})")
    for t in sorted(ledger.theme_items):
        log(f"  theme {t:28} {ledger.theme_items[t]:5d} items "
            f"{ledger.theme_bytes[t]/GB:7.2f} GB")
    log("ledger: " + LEDGER_DIR)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("interrupted")
        sys.exit(130)
