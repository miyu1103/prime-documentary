# -*- coding: utf-8 -*-
"""
MODERN-WEB free-asset ingest adapter for the Prime Documentary archive shelf.

Sibling of scripts/ingest_archive_sources.py (archival/gov/museum lane). This
adapter owns the MODERN sources only, and IMPORTS the sibling's plumbing
(Net politeness+robots, Ledger, validate_media, relevance scoring, contact
sheets) instead of re-implementing it (rule: no duplicate implementation).

Sources (this lane):
    mixkit         mixkit.co listing pages — VIDEO only. No official API; polite
                   parse, robots.txt-checked, >=2s/request. Mixkit License
                   (free commercial) -> free_commercial.
    coverr         coverr.co search pages — VIDEO only. Same politeness rules.
                   Coverr License (free commercial) -> free_commercial.
    pixabay_extra  Pixabay API (PIXABAY_API_KEY in repo .env): videos + images
                   for themes NOT already covered by the factory shelf, plus a
                   probe of the (undocumented) audio endpoint. Source-ID dedup
                   against the existing factory shelf (assets/asset_manifest
                   _srcId values, largely Pexels/Pixabay) is MANDATORY and runs
                   PRE-download — no bandwidth wasted on items we already own.
    unsplash       UNSPLASH_ACCESS_KEY — skips gracefully without key. Unsplash
                   API terms PROHIBIT bulk mirroring: hard cap 50/theme TOTAL
                   (cumulative vs ledger), download_location pinged, and the
                   curated-pull nature is recorded in license_field_raw.
    freesound      FREESOUND_API_KEY — skips gracefully without key. CC0-ONLY
                   filter (license:"Creative Commons 0"); HQ mp3 previews.

Storage (tier affinity of THIS lane):
    media       D:\\pd-archive\\<theme>\\        HARD GUARD: stop when D: free < 250GB
    quarantine  H:\\pd-media\\assets\\archive\\_quarantine\\<theme>\\  (review_required)
    ledgers     H:\\pd-media\\assets\\archive\\_ledger\\{mixkit,coverr,pixabay_extra,
                unsplash,freesound}.jsonl   (shared dir with the archival lane;
                the Ledger loads ALL *.jsonl there, so (source,id) and sha256
                dedup work across BOTH lanes and across restarts)
    C: is NEVER written.

Ledger JSONL schema (one object per line):
    {id, source, source_url, title, license_field_raw, license_decision,
     theme, file_path, bytes, sha256, fetched_at, relevance_score,
     matched_keywords}                       (+ kind; + usage_tag for audio)

Filename convention (OWNER DIRECTIVE, binding): every saved media file is
    <source>__<id>__<title-slug>.<ext>
ASCII lowercase-hyphen slug of the title, max 60 chars; theme = folder;
license = ledger; Windows-safe; name collisions append -2, -3, ...
e.g. mixkit__4432__aerial-tokyo-shibuya-crossing-night.mp4

Factory dedup index: built once per run from assets/asset_manifest.v001.json
(+ stock STOCK_MANIFEST files if present) and cached as
H:\\pd-media\\assets\\archive\\_ledger\\existing_index.json
    {generated_at, counts, ids: {"pixabay": ["i_123","v_456",...],
     "pexels": [...]}, sha256: [...]}
Factory sha256 values are also seeded into the run's content-dedup set.

Quality floors (enforced via the shared validate_media):
    video >=480p (prefer 720p+ via best-file choice), 5s..30min; audio >=128kbps
    or lossless; images long edge >=1200px (textures 1920px — Pixabay items are
    only taken for that theme when fullHD/original URLs are available).
    Corrupt/failed files are deleted and logged to rejects.jsonl.

Per-item vetting: person-filter + metadata relevance score (threshold 20 for
these curated-search sources), recorded as relevance_score/matched_keywords.
Rejects go to rejects.jsonl, never the main ledger.

AUDIO themes (sfx_environment, sfx_mechanical, sfx_human_movement,
ambience_beds, bgm_general) are Pixabay/Freesound only per owner directive and
carry usage_tag (sfx | sfx_foley | ambience | bgm) for the channel SFX audit.

Limits: NO per-theme caps — run until sources are exhausted at their query
sets or the D: free-space floor is hit. Resumable: relaunching with the same
command continues where it stopped (pass N == page N of each source).

Usage:
  python scripts/ingest_modern_web.py --source mixkit --theme ocean_nature --limit 2
  python scripts/ingest_modern_web.py --source all              # full resumable run
  python scripts/ingest_modern_web.py --source all --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import html as html_mod
import json
import os
import re
import shutil
import sys
import urllib.parse
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)

# CONTRACT §5 append safety: the lane name is read at framework import time and
# selects `rejects_web.jsonl`, so it must be set BEFORE the import below.
os.environ.setdefault("PD_INGEST_LANE", "web")

import ingest_archive_sources as base  # noqa: E402  shared plumbing (see docstring)

REPO = base.REPO
GB = base.GB
LEDGER_DIR = base.LEDGER_DIR
QUARANTINE = base.QUARANTINE
NET = base.NET
log = base.log

# Lane-local network policy: the shared Net.download waits up to 300s on a
# silent socket (cdn.freesound.org stalls mid-stream were measured costing
# 5min/item). This lane uses (30s connect, 90s read) and ONE retry instead.
# Patched on base.Net for THIS process only — sibling lanes are separate
# interpreters and keep their own policy.
def _download_with_retry(self, url: str, dest: str, *,
                         headers: dict | None = None) -> tuple[int, str]:
    last_err: Exception | None = None
    for attempt in (1, 2):
        self._wait(url)
        h = hashlib.sha256()
        n = 0
        try:
            with self.s.get(url, stream=True, timeout=(30, 90),
                            headers=headers or {}) as r:
                r.raise_for_status()
                tmp = dest + ".part"
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(1024 * 512):
                        f.write(chunk)
                        h.update(chunk)
                        n += len(chunk)
                        if n > base.MAX_ITEM_BYTES:
                            raise ValueError(f"file exceeds MAX_ITEM_BYTES: {url}")
            os.replace(tmp, dest)
            return n, h.hexdigest()
        except ValueError:
            raise                       # size cap: no point retrying
        except Exception as e:  # noqa: BLE001
            last_err = e
            if attempt == 1:
                log(f"  dl-retry after {e.__class__.__name__}: {url[:80]}")
    raise last_err  # type: ignore[misc]


base.Net.download = _download_with_retry

RULE_VERSION = "relevance-v5+floors-source-aware (CONTRACT 2026-07-28)"

D_ROOT = r"D:\pd-archive"
D_DRIVE = "D:\\"
D_FLOOR = 250 * GB                       # binding hard guard for this lane
EXISTING_INDEX = os.path.join(LEDGER_DIR, "existing_index.json")
FACTORY_MANIFESTS = [
    os.path.join(REPO, "assets", "asset_manifest.v001.json"),
    r"H:\pd-media\assets\stock\STOCK_MANIFEST.json",
    r"H:\pd-media\assets\stock\images\STOCK_MANIFEST.json",
    r"H:\pd-media\assets\stock\video\STOCK_MANIFEST.json",
    r"H:\pd-media\assets\stock\audio\STOCK_MANIFEST.json",
]

# ------------------------------------------------------------------ themes ----
# Video/image themes reuse the sibling's curated query tables (base.THEMES).
# 429 circuit breaker (2026-08-01). Three lane restarts inside ten minutes made this
# lane replay page 1 of every mixkit query three times over, and mixkit started
# answering 429. Retrying a host that is already refusing us, once per pass, is exactly
# the impoliteness CONTRACT 8 forbids and risks turning a soft limit into a hard ban.
# After RATE_LIMIT_TRIP consecutive 429s a source sits out the rest of the run; the
# next launch starts it clean.
RATE_LIMIT_TRIP = 5
_rate_limited: dict[str, int] = {}


def note_rate_limit(source: str, err: BaseException) -> None:
    if "429" in str(err) or "Too Many Requests" in str(err):
        _rate_limited[source] = _rate_limited.get(source, 0) + 1
        if _rate_limited[source] == RATE_LIMIT_TRIP:
            log(f"  {source}: {RATE_LIMIT_TRIP} consecutive 429s — backing off for the "
                f"rest of this run (relaunch to retry)")
    else:
        _rate_limited.pop(source, None)


def rate_limited(source: str) -> bool:
    return _rate_limited.get(source, 0) >= RATE_LIMIT_TRIP


VIDEO_THEMES = [
    'hands_and_transactions',
    'bank_and_branch',
    'household_loss',
    'market_machinery',
    'goods_in_motion',
    'selling_floor',
    'decision_rooms',
    'bench_to_line',
    'business_corporate',
    'economy_crisis',
    'courtroom_justice',
    'prison_jail',
    'government_buildings',
    'police_modern',
    'money_banking',
    'small_town',
    'newspapers_printing',
    'science_tech',
    'ocean_nature',
    'wildlife_animals',
    'world_cities',
    'japan',
    'landscapes_timelapse',
    'textures_backgrounds',
]

# Audio themes are new to this lane; registered into base.THEMES so the shared
# relevance scorer works. usage_tag feeds the channel's SFX audit.
AUDIO_THEMES: dict[str, dict[str, list[str]]] = {
    "sfx_environment": {
        "audio": ["rain on window", "thunder rumble distant", "wind through trees",
                  "fire crackling fireplace", "river stream water flowing",
                  "ocean waves shore", "birds forest morning", "crickets night"],
    },
    "sfx_mechanical": {
        "audio": ["door creak old hinge", "metal clank impact", "typewriter keys",
                  "camera shutter click", "clock ticking mechanism",
                  "car engine start", "train passing rails", "telephone ring vintage",
                  "keyboard typing", "switch click mechanical"],
    },
    "sfx_human_movement": {
        "audio": ["footsteps concrete", "footsteps gravel", "footsteps wood floor",
                  "footsteps stairs echo", "paper rustle page turn", "paper crumple",
                  "door open close", "door slam", "knock on door",
                  "writing pen on paper", "cloth fabric movement"],
    },
    "ambience_beds": {
        "audio": ["room tone quiet interior", "city ambience distant traffic",
                  "office room ambience", "night ambience quiet", "dark drone ambience",
                  "underground tunnel ambience", "suspense drone atmosphere"],
    },
    "bgm_general": {
        "audio": ["cinematic tension underscore", "dark ambient background",
                  "melancholic piano instrumental", "documentary background music",
                  "orchestral dramatic build", "mysterious investigation music"],
    },
}
USAGE_TAG = {"sfx_environment": "sfx", "sfx_mechanical": "sfx",
             "sfx_human_movement": "sfx_foley", "ambience_beds": "ambience",
             "bgm_general": "bgm"}
AUDIO_ONLY_SOURCES = {"pixabay_extra", "freesound"}   # owner: audio via these only

# ---- STRONG terms for THIS lane's themes (CONTRACT §4 relevance-v5-j/k) ----
# The weak-only cap requires >=1 STRONG term or a full query phrase. The
# framework's WEAK_TERMS list (built for archival titles) contains almost the
# whole modern-stock and SFX vocabulary — "ocean", "waves", "city", "rain",
# "wind", "door", "ambience" are all weak — so WITHOUT these entries every
# legitimate stock clip and CC0 field recording in this lane caps at 15 and is
# discarded. Ambiguity is domain-relative (contract §4-v5-k): for `ocean_nature`
# "ocean waves" IS the subject matter, and for `sfx_environment` so is "rain".
# Kept lane-local (merged into base.STRONG_EXTRA at import) rather than edited
# into the shared file, which sibling lanes are actively rewriting.
LANE_STRONG: dict[str, list[str]] = {
    "ocean_nature": ["ocean", "ocean waves", "sea waves", "crashing waves",
                     "breaking waves", "coral reef", "underwater", "coastline",
                     "shoreline", "seascape", "surf", "tide", "lagoon", "atoll",
                     "kelp", "sea cliffs", "aerial coast"],
    "wildlife_animals": ["wildlife", "deer", "elephant", "lion", "savanna",
                         "flock", "herd", "wolf", "birdsong", "eagle", "fox",
                         "bison", "zebra", "giraffe", "antelope", "safari",
                         "bear", "owl", "whale", "dolphin"],
    # "city" is the DOMAIN term here (contract §4-v5-k: ambiguity is per-word and
    # domain-relative), and city PROPER NOUNS are unmistakable. Bare "street" is
    # deliberately NOT promoted — that is the v5-j trap ("Street Fighter Mix").
    "world_cities": ["city", "urban", "skyline", "cityscape", "downtown",
                     "metropolis", "city skyline", "city street", "city lights",
                     "city at night", "city traffic", "aerial city", "old town",
                     "subway", "traffic", "boulevard", "plaza", "timelapse",
                     "rooftops", "crosswalk", "intersection", "street traffic",
                     "tokyo", "london", "paris", "new york", "mexico city",
                     "berlin", "rome", "madrid", "istanbul", "shanghai",
                     "hong kong", "dubai", "singapore", "bangkok"],
    "japan": ["japan", "japanese", "tokyo", "kyoto", "osaka", "mount fuji",
              "torii", "shrine", "pagoda", "shinto", "shinkansen", "ryokan",
              "tokyo street", "kyoto temple", "neon street", "temple"],
    "landscapes_timelapse": ["timelapse", "time-lapse", "canyon", "dunes",
                             "waterfall", "glacier", "valley", "summit",
                             "peaks", "plateau", "fjord", "alpine", "sunrise",
                             "sunset", "mountain landscape", "desert canyon"],
    "textures_backgrounds": ["bokeh", "grunge", "marble", "parchment",
                             "ink in water", "paper texture", "wall texture",
                             "stone texture", "marble texture", "smoke background",
                             "gradient", "concrete", "canvas", "film grain"],
    "science_tech": ["circuit board", "circuitry", "microchip", "semiconductor",
                     "mainframe", "observatory", "telescope", "robot", "robotic",
                     "laboratory", "server rack", "data center", "electronics",
                     "microscope", "vintage computer"],
    "small_town": ["storefront", "clapboard", "rural road", "diner",
                   "grain silo", "church steeple"],
    "money_banking": ["banknote", "dollar bills", "currency", "coins",
                      "safe deposit", "ticker", "gold bars", "money counting"],
    "police_modern": ["police", "patrol", "siren", "crime scene", "police car",
                      "police tape", "squad car", "emergency lights", "bodycam"],
    # ---- AUDIO themes: terse SFX titles live or die on these ----
    "sfx_environment": ["rain", "rainfall", "thunder", "thunderstorm", "downpour",
                        "drizzle", "wind", "gust", "campfire", "crackling",
                        "fireplace", "bonfire", "stream", "creek", "brook",
                        "waterfall", "surf", "crickets", "birdsong",
                        "dawn chorus", "cicadas", "seagulls", "leaves rustling"],
    "sfx_mechanical": ["door", "doorknob", "creak", "hinge", "latch", "clank",
                       "clatter", "typewriter", "shutter", "ratchet", "engine",
                       "motor", "gears", "switch", "lever", "keyboard", "typing",
                       "telephone", "dial", "clock", "ticking", "mechanism",
                       "metal impact", "door slam", "train horn"],
    "sfx_human_movement": ["footsteps", "footstep", "walking", "gravel",
                           "stairs", "staircase", "page turn", "paper rustle",
                           "crumple", "knock", "cloth", "fabric", "rustle",
                           "shuffle", "boots", "writing"],
    "ambience_beds": ["room tone", "roomtone", "ambience", "atmosphere", "drone",
                      "ambient bed", "tunnel", "underground", "suspense",
                      "air conditioning", "refrigerator hum", "background ambience"],
    "bgm_general": ["cinematic", "underscore", "instrumental", "piano",
                    "orchestral", "soundtrack", "melancholic", "suspenseful",
                    "documentary music", "background music", "ambient music",
                    "tension"],
}

for _t, _q in AUDIO_THEMES.items():
    base.THEMES.setdefault(_t, {"video": [], "image": [], "audio": _q["audio"]})
for _t, _terms in LANE_STRONG.items():
    base.STRONG_EXTRA.setdefault(_t, [])
    base.STRONG_EXTRA[_t] += [t for t in _terms
                              if t not in base.STRONG_EXTRA[_t]]
base._theme_pos_cache.clear()      # STRONG_EXTRA feeds theme_terms(); drop cache
base.SRC_THRESHOLD.setdefault("pixabay_extra", 20)
base.HOST_INTERVAL.setdefault("pixabay.com", 1.0)
base.HOST_INTERVAL.setdefault("api.unsplash.com", 1.0)
base.HOST_INTERVAL.setdefault("freesound.org", 1.0)

ALL_THEMES = VIDEO_THEMES + list(AUDIO_THEMES)
PASS = 1  # pass N == page N of each paginated source (set by main loop)


# ------------------------------------------------------- relevance (shared) ----
# Scoring lives in base.relevance() — since 2026-07-28 it anchors word
# boundaries at BOTH ends (so "court" no longer matches "courtesy"/"courtyard")
# and enforces a TITLE gate (>=1 positive term in the TITLE, not merely the
# description). This lane DELEGATES to it (no second implementation) and adds
# exactly one lane-specific nuance:
#   AUDIO items are scored on terse filenames ("rumble.wav", "Foley_take_03"),
#   where the subject matter lives in the TAG list. For audio we therefore feed
#   `title + tags` as the title argument, so the tag list can satisfy the title
#   gate. Video/image titles are descriptive and pass title-only, unchanged.
def score_item(theme: str, title: str, desc: str = "",
               tag_text: str = "") -> tuple[int, list[str], list[str], bool]:
    """(score, matched, negative_hits, title_ok) via the shared scorer."""
    title_text = f"{title} {tag_text}".strip() if tag_text else title
    return base.relevance(theme, title_text, desc)


# --------------------------------------------------- factory shelf dedup ----
def build_existing_index() -> dict:
    """(Re)build the factory-shelf source-ID index used for MANDATORY
    pre-download dedup (the shelf is largely Pexels/Pixabay). Cached as
    existing_index.json next to the ledgers so sibling lanes can reuse it."""
    newest_src = max((os.path.getmtime(p) for p in FACTORY_MANIFESTS
                      if os.path.exists(p)), default=0.0)
    if os.path.exists(EXISTING_INDEX) and os.path.getmtime(EXISTING_INDEX) >= newest_src:
        try:
            with open(EXISTING_INDEX, encoding="utf-8") as f:
                return json.load(f)
        except Exception:  # noqa: BLE001
            pass
    ids: dict[str, set[str]] = {}
    shas: set[str] = set()
    n_assets = 0
    for mp in FACTORY_MANIFESTS:
        if not os.path.exists(mp):
            continue
        try:
            with open(mp, encoding="utf-8") as f:
                doc = json.load(f)
        except Exception as e:  # noqa: BLE001
            log(f"existing-index: cannot parse {mp}: {e}")
            continue
        if isinstance(doc, list):
            assets = doc
        else:
            assets = doc.get("assets") or doc.get("items") or []
        if isinstance(assets, dict):
            assets = list(assets.values())
        for a in assets:
            if not isinstance(a, dict):
                continue
            n_assets += 1
            src_id = str(a.get("_srcId", "") or a.get("srcId", "") or "")
            m = re.match(r"(pexels|pixabay)_([iva])_(\d+)", src_id)
            if m:
                ids.setdefault(m.group(1), set()).add(f"{m.group(2)}_{m.group(3)}")
            sha = str(a.get("sha256", "") or "").replace("sha256:", "")
            if len(sha) == 64:
                shas.add(sha)
    idx = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "from": [p for p in FACTORY_MANIFESTS if os.path.exists(p)],
           "counts": {k: len(v) for k, v in ids.items()} | {"assets_scanned": n_assets,
                                                            "sha256": len(shas)},
           "ids": {k: sorted(v) for k, v in ids.items()},
           "sha256": sorted(shas)}
    os.makedirs(LEDGER_DIR, exist_ok=True)
    tmp = EXISTING_INDEX + ".part"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(idx, f)
    os.replace(tmp, EXISTING_INDEX)
    log(f"existing-index rebuilt: {idx['counts']}")
    return idx


FACTORY_PIXABAY: set[str] = set()   # {"i_123", "v_456"} — filled in main()


def pixabay_dup(ledger: base.Ledger, kind_prefix: str, num_id: str) -> bool:
    """MANDATORY pre-download source-ID dedup for Pixabay: this lane's ledger,
    the archival lane's pixabay.jsonl, and the factory shelf index."""
    nid = f"{kind_prefix}_{num_id}"
    return (ledger.seen("pixabay_extra", nid)
            or ledger.seen("pixabay", num_id)          # archival-lane records
            or ledger.seen("pixabay", nid)
            or nid in FACTORY_PIXABAY)


# ------------------------------------------------------------ storage/take ----
def slugify(text: str, maxlen: int = 60) -> str:
    """OWNER filename convention: ASCII lowercase-hyphen slug, max 60 chars."""
    text = (text or "").encode("ascii", "ignore").decode("ascii").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return (text[:maxlen].rstrip("-")) or "untitled"


def dest_path(root: str, source: str, item_id: str, title: str, ext: str) -> str:
    """`<source>__<id>__<title-slug>.<ext>` (Windows-safe; collisions -> `-2`)."""
    sid = re.sub(r"[^A-Za-z0-9_-]+", "", str(item_id)) or "noid"
    stem = f"{source}__{sid}__{slugify(title)}"
    dest = os.path.join(root, f"{stem}.{ext}")
    n = 2
    while os.path.exists(dest) or os.path.exists(dest + ".part"):
        dest = os.path.join(root, f"{stem}-{n}.{ext}")
        n += 1
    return dest

def pick_root(theme: str, decision: str) -> str | None:
    """D:\\pd-archive\\<theme> for shelf items (None once D: free <= 250GB);
    quarantine for review_required lives on H: like the sibling lane."""
    if decision == "review_required":
        if base.drive_free(base.TIERS[0]["drive"]) <= base.TIERS[0]["floor"]:
            log("  skip quarantine item: H: free-space floor reached")
            return None
        return os.path.join(QUARANTINE, theme)
    if not os.path.isdir(D_DRIVE) or base.drive_free(D_DRIVE) <= D_FLOOR:
        return None
    return os.path.join(D_ROOT, theme)


def take_item(ledger: base.Ledger, *, source: str, item_id: str, title: str,
              source_url: str, download_url: str, kind: str, theme: str,
              license_raw: str, decision: str, default_ext: str, dry_run: bool,
              usage_tag: str | None = None, desc: str = "", tag_text: str = "",
              dl_headers: dict | None = None) -> bool:
    """Vet -> download -> validate -> ledger (this lane's contract schema).
    Mirrors the sibling take() flow but writes matched_keywords/usage_tag and
    routes storage to D: only. Returns True if ingested."""
    if ledger.seen(source, item_id):
        return False
    if base.PERSON_RE.search(title or ""):
        base.reject_log(source, item_id, theme, "person-filter", title=title)
        return False
    score, matched, negs, title_ok = score_item(theme, title, desc, tag_text)
    threshold = base.SRC_THRESHOLD.get(source, base.DEFAULT_THRESHOLD)
    # CONTRACT §4-v3-g: reject rows MUST carry the title — without it the
    # false-negative direction is invisible (it is what exposed v3 and v5).
    if not title_ok:           # off-theme item riding on a long description
        base.reject_log(source, item_id, theme, "title-irrelevant",
                        score, matched, negs, title=title)
        return False
    if score < threshold:
        base.reject_log(source, item_id, theme, f"relevance<{threshold}",
                        score, matched, negs, title=title)
        return False
    root = pick_root(theme, decision)
    if root is None:
        return False
    os.makedirs(root, exist_ok=True)
    dest = dest_path(root, source, item_id, title,
                     base.ext_of(download_url, default_ext))
    fname = os.path.basename(dest)
    if dry_run:
        log(f"  DRY {decision:>15} s={score:3d} {theme:22} {title[:56]}"
            f"  <- {download_url[:80]}")
        return True
    try:
        nbytes, sha = NET.download(download_url, dest, headers=dl_headers)
    except Exception as e:  # noqa: BLE001
        log(f"  dl-fail: {e}")
        base.reject_log(source, item_id, theme,
                        f"download-fail:{e.__class__.__name__}", score,
                        title=title)
        for p in (dest, dest + ".part"):
            if os.path.exists(p):
                try:
                    os.remove(p)
                except OSError:
                    pass
        return False
    if sha in ledger.shas:   # content dedup across both lanes AND factory shelf
        log(f"  dup-sha, removed: {fname[:70]}")
        os.remove(dest)
        base.reject_log(source, item_id, theme, "dup-sha256", score, title=title)
        return False
    # CONTRACT §4.2: floors are SOURCE-AWARE and must never silently destroy what
    # the relevance gate approved — a "quarantine" verdict moves the file to H:
    # for owner review instead of deleting it.
    verdict, why = base.validate_media(dest, kind, theme, source)
    quarantine_reason = ""
    if verdict == "reject":
        log(f"  reject ({why}), removed: {fname[:70]}")
        os.remove(dest)
        base.reject_log(source, item_id, theme, f"tech:{why}", score, title=title)
        return False
    if verdict == "quarantine":
        q_root = os.path.join(QUARANTINE, theme)
        os.makedirs(q_root, exist_ok=True)
        q_dest = dest_path(q_root, source, item_id, title,
                           os.path.splitext(dest)[1].lstrip("."))
        # Cross-device move: the shelf lives on D:/E:/F: but quarantine is ALWAYS on H:
        # (CONTRACT 1), and os.replace cannot cross a Windows volume — it raises
        # OSError 18 (EXDEV). That killed the whole source: the noaa lane died on its
        # first sub-floor TIF and stayed dead for 18 hours while its siblings ran on.
        shutil.move(dest, q_dest)
        dest, fname = q_dest, os.path.basename(q_dest)
        decision, quarantine_reason = "review_required", why
        log(f"  QUARANTINE ({why}): {fname[:70]}")
    rec = {
        "id": str(item_id), "source": source, "source_url": source_url,
        "title": title, "license_field_raw": license_raw[:500],
        "license_decision": decision, "theme": theme, "file_path": dest,
        "bytes": nbytes, "sha256": sha,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "relevance_score": score, "matched_keywords": matched[:12], "kind": kind,
    }
    if usage_tag:
        rec["usage_tag"] = usage_tag
    if quarantine_reason:
        rec["quarantine_reason"] = quarantine_reason
    ledger.record(rec)
    log(f"  OK {decision:>15} s={score:3d} {nbytes/1e6:7.1f}MB {fname[:74]}")
    if ledger.theme_items.get(theme, 0) % base.QC_SHEET_EVERY == 0:
        base.build_contact_sheet(theme, ledger.recent.get(theme, []),
                                 ledger.theme_items.get(theme, 0))
    return True


# ---------------------------------------------------------------- adapters ----
_MIXKIT_TRIED: set[tuple[str, int]] = set()   # (category slug, pass) 404/dup cache


def _mixkit_slugs(theme: str) -> list[str]:
    """Mixkit categories are single tags — full query slugs mostly 404.
    Candidates: full query slug first, then each significant query word."""
    out: list[str] = []
    for q in base.THEMES[theme]["video"]:
        words = [w for w in re.findall(r"[a-z0-9]+", q.lower())
                 if w not in base.STOPWORDS and len(w) > 2]
        for cand in ["-".join(words)] + words:
            if cand and cand not in out:
                out.append(cand)
    return out


def _jsonld_videos(text: str) -> list[dict]:
    """VideoObject entries from a page's JSON-LD blocks (title/license/url)."""
    vids: list[dict] = []
    for m in re.finditer(
            r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
            text, re.S):
        try:
            doc = json.loads(m.group(1))
        except Exception:  # noqa: BLE001
            continue
        stack = [doc]
        while stack:
            node = stack.pop()
            if isinstance(node, list):
                stack.extend(node)
            elif isinstance(node, dict):
                if node.get("@type") == "VideoObject":
                    vids.append(node)
                stack.extend(v for v in node.values()
                             if isinstance(v, (list, dict)))
    return vids


def src_mixkit(ledger: base.Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Mixkit VIDEO category pages (no official API). robots.txt-checked, 2s/req.
    Parses the JSON-LD VideoObject blocks; only license '#videoFree' items are
    taken (free for commercial use under the Mixkit License)."""
    if theme not in VIDEO_THEMES:
        return 0
    got = 0
    for slug in _mixkit_slugs(theme):
        if got >= limit or ledger.run_full():
            break
        if (slug, PASS) in _MIXKIT_TRIED:
            continue
        _MIXKIT_TRIED.add((slug, PASS))
        page = f"https://mixkit.co/free-stock-video/{slug}/"
        if PASS > 1:
            page += f"?page={PASS}"
        try:
            r = NET.get(page, check_robots=True)
            if r.status_code == 404:
                continue
            r.raise_for_status()
            vids = _jsonld_videos(r.text)
        except PermissionError:
            raise
        except Exception as e:  # noqa: BLE001
            log(f"  mixkit page fail ({page}): {e}")
            note_rate_limit("mixkit", e)
            if rate_limited("mixkit"):
                return got
            continue
        for v in vids:
            if got >= limit or ledger.run_full():
                break
            url = v.get("contentUrl", "")
            lic = str(v.get("license", ""))
            title = str(v.get("name", "")).strip()
            m = re.search(r"/videos/(\d+)/", url) or re.search(r"-(\d+)-", url)
            if not url or not m:
                continue
            vid = m.group(1)
            if "#videoFree" not in lic:      # paid/other tier -> not ours
                base.reject_log("mixkit", vid, theme,
                                f"license-not-free:{lic[:80]}", title=title)
                continue
            if take_item(ledger, source="mixkit", item_id=vid, title=title or vid,
                         source_url=page, download_url=url, kind="video",
                         theme=theme,
                         license_raw=f"license={lic}; copyrightNotice="
                                     f"{v.get('copyrightNotice', '')} "
                                     f"(Mixkit License, free for commercial use)",
                         decision="free_commercial", default_ext="mp4",
                         dry_run=dry_run):
                got += 1
    return got


def src_coverr(ledger: base.Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Coverr VIDEO search pages (no official API). robots.txt-checked, 2s/req."""
    if theme not in VIDEO_THEMES:
        return 0
    got = 0
    for q in base.THEMES[theme]["video"]:
        if got >= limit or ledger.run_full():
            break
        page = ("https://coverr.co/s?q=" + urllib.parse.quote(q)
                + (f"&page={PASS}" if PASS > 1 else ""))
        try:
            r = NET.get(page, check_robots=True)
            r.raise_for_status()
            text = html_mod.unescape(r.text)
        except PermissionError:
            raise
        except Exception as e:  # noqa: BLE001
            log(f"  coverr page fail: {e}")
            note_rate_limit("coverr", e)
            if rate_limited("coverr"):
                return got
            continue
        # Coverr embeds its own (non-partner) videos as
        #   "mp4":"https://cdn.coverr.co/videos/coverr-<title-slug>-<id>/1080p.mp4"
        # iStock partner results live on media.istockphoto.com and are NOT free
        # -> host-restricted regex excludes them. "coverr-temp-*" and
        # "user-ai-generation-*" assets are site chrome / AI demos -> skipped.
        urls = re.findall(
            r'"mp4":"(https://cdn\.coverr\.co/videos/coverr-[^"]+?/1080p\.mp4[^"]*)"',
            text)
        uniq: list[str] = []
        for u in urls:
            u = u.replace("\\u0026", "&")
            if u not in uniq and "coverr-temp-" not in u:
                uniq.append(u)
        for u in uniq:
            if got >= limit or ledger.run_full():
                break
            m = re.search(r"/videos/(coverr-[^/?]+?)/1080p\.mp4", u)
            slug_full = m.group(1) if m else hashlib.sha1(u.encode()).hexdigest()[:16]
            mnum = re.search(r"-(\d+)$", slug_full)
            vid = mnum.group(1) if mnum else slug_full
            title = re.sub(r"^coverr-", "", re.sub(r"-\d+$", "", slug_full)) \
                .replace("-", " ")
            # 'coverr-premium-*' slugs look like Coverr's paid tier: license
            # uncertain -> quarantine (review_required), never the main shelf.
            premium = slug_full.startswith("coverr-premium-")
            if take_item(ledger, source="coverr", item_id=vid, title=title,
                         source_url=page, download_url=u, kind="video", theme=theme,
                         license_raw=("Coverr slug marked 'premium' — tier/license "
                                      "uncertain, review before use") if premium
                         else "Coverr License (free for commercial use, "
                              "no attribution required)",
                         decision="review_required" if premium
                         else "free_commercial", default_ext="mp4",
                         dry_run=dry_run):
                got += 1
    return got


PIXABAY_LICENSE = "Pixabay Content License (free commercial, no attribution)"


def src_pixabay_extra(ledger: base.Ledger, theme: str, limit: int,
                      dry_run: bool) -> int:
    """Pixabay videos+images for this lane's themes (+audio endpoint probe).
    Source-ID dedup vs factory shelf + BOTH lanes' ledgers runs PRE-download."""
    key = os.environ.get("PIXABAY_API_KEY", "")
    if not key:
        raise PermissionError("PIXABAY_API_KEY missing")
    got = 0
    if not hasattr(src_pixabay_extra, "_audio_probed"):
        src_pixabay_extra._audio_probed = True  # type: ignore[attr-defined]
        try:
            r = NET.get("https://pixabay.com/api/audio/",
                        params={"key": key, "q": "rain"})
            src_pixabay_extra._audio_ok = (r.status_code == 200)  # type: ignore[attr-defined]
            log(f"  pixabay AUDIO probe: HTTP {r.status_code} -> "
                f"{'audio API available!' if r.status_code == 200 else 'NO public audio API'}")
        except Exception as e:  # noqa: BLE001
            src_pixabay_extra._audio_ok = False  # type: ignore[attr-defined]
            log(f"  pixabay AUDIO probe failed: {e}")

    if theme in AUDIO_THEMES:
        if not getattr(src_pixabay_extra, "_audio_ok", False):
            return 0
        for q in AUDIO_THEMES[theme]["audio"]:
            if got >= limit or ledger.run_full():
                break
            try:
                data = NET.get_json("https://pixabay.com/api/audio/", params={
                    "key": key, "q": q, "per_page": 30, "page": PASS})
            except Exception as e:  # noqa: BLE001
                log(f"  pixabay audio search fail: {e}")
                continue
            for hit in data.get("hits", []):
                if got >= limit or ledger.run_full():
                    break
                aid = str(hit.get("id", ""))
                if not aid or pixabay_dup(ledger, "a", aid):
                    continue
                url = (hit.get("audio_url") or hit.get("download_url")
                       or hit.get("url", ""))
                if not url:
                    continue
                if take_item(ledger, source="pixabay_extra", item_id=f"a_{aid}",
                             title=(hit.get("tags") or hit.get("name") or aid)[:80],
                             source_url=hit.get("pageURL", ""), download_url=url,
                             kind="audio", theme=theme, license_raw=PIXABAY_LICENSE,
                             decision="free_commercial", default_ext="mp3",
                             dry_run=dry_run, usage_tag=USAGE_TAG[theme]):
                    got += 1
        return got

    # ---- videos ----
    for q in base.THEMES[theme].get("video", []):
        if got >= limit or ledger.run_full():
            break
        try:
            data = NET.get_json("https://pixabay.com/api/videos/", params={
                "key": key, "q": q, "safesearch": "true", "per_page": 50,
                "page": PASS})
        except Exception as e:  # noqa: BLE001
            log(f"  pixabay video search fail: {e}")
            continue
        for hit in data.get("hits", []):
            if got >= limit or ledger.run_full():
                break
            vid = str(hit["id"])
            if pixabay_dup(ledger, "v", vid):
                base.reject_log("pixabay_extra", f"v_{vid}", theme,
                                "dup_existing_id", title=hit.get("tags", "")[:80])
                continue
            files = hit.get("videos", {})
            best = files.get("large") or files.get("medium") or files.get("small") or {}
            if not best.get("url"):
                continue
            if take_item(ledger, source="pixabay_extra", item_id=f"v_{vid}",
                         title=(hit.get("tags", "") or vid)[:80],
                         source_url=hit.get("pageURL", ""), download_url=best["url"],
                         kind="video", theme=theme, license_raw=PIXABAY_LICENSE,
                         decision="free_commercial", default_ext="mp4",
                         dry_run=dry_run):
                got += 1
    # ---- images ----
    for q in base.THEMES[theme].get("image", []):
        if got >= limit or ledger.run_full():
            break
        try:
            data = NET.get_json("https://pixabay.com/api/", params={
                "key": key, "q": q, "image_type": "photo", "safesearch": "true",
                "min_width": 1200, "per_page": 50, "page": PASS})
        except Exception as e:  # noqa: BLE001
            log(f"  pixabay image search fail: {e}")
            continue
        for hit in data.get("hits", []):
            if got >= limit or ledger.run_full():
                break
            pid = str(hit["id"])
            if pixabay_dup(ledger, "i", pid):
                base.reject_log("pixabay_extra", f"i_{pid}", theme,
                                "dup_existing_id", title=hit.get("tags", "")[:80])
                continue
            url = hit.get("fullHDURL") or hit.get("imageURL") or ""
            if not url:
                if theme == "textures_backgrounds":
                    continue        # 1920px floor unreachable from largeImageURL
                url = hit.get("largeImageURL", "")
            if not url:
                continue
            if take_item(ledger, source="pixabay_extra", item_id=f"i_{pid}",
                         title=(hit.get("tags", "") or pid)[:80],
                         source_url=hit.get("pageURL", ""), download_url=url,
                         kind="image", theme=theme, license_raw=PIXABAY_LICENSE,
                         decision="free_commercial", default_ext="jpg",
                         dry_run=dry_run):
                got += 1
    return got


def src_unsplash(ledger: base.Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Unsplash — small CURATED pulls only (API terms prohibit bulk mirroring):
    hard cap 50/theme cumulative vs ledger. Skips gracefully without key."""
    key = os.environ.get("UNSPLASH_ACCESS_KEY", "")
    if not key:
        raise PermissionError("UNSPLASH_ACCESS_KEY missing "
                              "(free at unsplash.com/developers)")
    if theme in AUDIO_THEMES:
        return 0
    if not hasattr(src_unsplash, "_per_theme"):        # cumulative 50/theme cap
        per: dict[str, int] = {}
        lp = os.path.join(LEDGER_DIR, "unsplash.jsonl")
        if os.path.exists(lp):
            with open(lp, encoding="utf-8") as f:
                for line in f:
                    try:
                        per_theme = json.loads(line).get("theme", "?")
                        per[per_theme] = per.get(per_theme, 0) + 1
                    except Exception:  # noqa: BLE001
                        continue
        src_unsplash._per_theme = per  # type: ignore[attr-defined]
    already = src_unsplash._per_theme.get(theme, 0)  # type: ignore[attr-defined]
    limit = min(limit, max(0, 50 - already))
    if limit <= 0:
        return 0
    got = 0
    for q in base.THEMES[theme].get("image", [])[:2]:
        if got >= limit or ledger.run_full():
            break
        try:
            data = NET.get_json("https://api.unsplash.com/search/photos", params={
                "query": q, "per_page": 15, "page": PASS, "client_id": key})
        except Exception as e:  # noqa: BLE001
            log(f"  unsplash search fail: {e}")
            continue
        for ph in data.get("results", []):
            if got >= limit or ledger.run_full():
                break
            pid = ph["id"]
            url = (ph.get("urls") or {}).get("full") or (ph.get("urls") or {}).get("regular")
            if not url:
                continue
            ok = take_item(ledger, source="unsplash", item_id=pid,
                           title=(ph.get("alt_description") or ph.get("description")
                                  or pid)[:80],
                           source_url=(ph.get("links") or {}).get("html", ""),
                           download_url=url, kind="image", theme=theme,
                           license_raw="Unsplash License (free commercial; bulk "
                                       "mirroring prohibited — small curated pull)",
                           decision="free_commercial", default_ext="jpg",
                           dry_run=dry_run)
            if ok:
                got += 1
                src_unsplash._per_theme[theme] = (            # type: ignore[attr-defined]
                    src_unsplash._per_theme.get(theme, 0) + 1)  # type: ignore[attr-defined]
                dl = (ph.get("links") or {}).get("download_location")
                if dl and not dry_run:
                    try:                       # required by Unsplash API guidelines
                        NET.get(dl, params={"client_id": key})
                    except Exception:  # noqa: BLE001
                        pass
    return got


def src_freesound(ledger: base.Ledger, theme: str, limit: int, dry_run: bool) -> int:
    """Freesound — CC0-ONLY filter, HQ mp3 previews, usage_tag recorded.
    Skips gracefully without FREESOUND_API_KEY."""
    key = os.environ.get("FREESOUND_API_KEY", "")
    if not key:
        raise PermissionError("FREESOUND_API_KEY missing "
                              "(free at freesound.org/apiv2/apply)")
    if theme not in AUDIO_THEMES:
        return 0
    got = 0
    for q in AUDIO_THEMES[theme]["audio"]:
        if got >= limit or ledger.run_full():
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
            if got >= limit or ledger.run_full():
                break
            sid = str(snd["id"])
            lic = snd.get("license", "")
            if "publicdomain/zero" not in lic and "Creative Commons 0" not in lic:
                continue                                       # hard CC0 gate
            url = (snd.get("previews") or {}).get("preview-hq-mp3", "")
            if not url:
                continue
            # tags feed the TITLE gate (SFX names are terse: "rumble.wav");
            # the prose description only feeds the score.
            fs_tags = " ".join(snd.get("tags", []) or [])[:300]
            fs_desc = str(snd.get("description", ""))[:600]
            if take_item(ledger, source="freesound", item_id=sid,
                         title=snd.get("name", ""), source_url=snd.get("url", ""),
                         download_url=url, kind="audio", theme=theme,
                         license_raw=lic, decision="cc0", default_ext="mp3",
                         dry_run=dry_run, usage_tag=USAGE_TAG[theme],
                         desc=fs_desc, tag_text=fs_tags):
                got += 1
    return got


ADAPTERS = {"mixkit": src_mixkit, "coverr": src_coverr,
            "pixabay_extra": src_pixabay_extra,
            "unsplash": src_unsplash, "freesound": src_freesound}
# freesound first: the audio lane was the archive's blocker (owner priority);
# unsplash next (small curated pulls finish fast), then the big video sources.
SOURCE_ORDER = ["freesound", "unsplash", "mixkit", "coverr", "pixabay_extra"]


def retro_audit(dry_run: bool) -> int:
    """Re-score every item this lane has already shelved under the CORRECTED
    gate (both-end boundaries + title gate) and purge the failures.

    Fairness note: at ingest, mixkit/coverr/pixabay_extra/unsplash were scored
    on the title alone (desc=""), so title-only re-scoring reproduces their
    live gate exactly. Freesound alone also used tags/description, so its tags
    are re-fetched from the API (1 req/item, polite) before judging — otherwise
    terse SFX filenames would be purged unfairly.

    Failures: file deleted, tombstone row written to rejects.jsonl, record
    dropped from the ledger (ledger rewritten atomically)."""
    key = os.environ.get("FREESOUND_API_KEY", "")
    purged_items = purged_bytes = kept = 0
    for source in SOURCE_ORDER:
        path = os.path.join(LEDGER_DIR, f"{source}.jsonl")
        if not os.path.exists(path):
            continue
        keep_lines: list[str] = []
        s_purged = 0
        with open(path, encoding="utf-8") as f:
            records = [line for line in f if line.strip()]
        for line in records:
            try:
                rec = json.loads(line)
            except Exception:  # noqa: BLE001
                keep_lines.append(line)
                continue
            theme = rec.get("theme", "")
            title = rec.get("title", "")
            if theme not in base.THEMES:
                keep_lines.append(line)
                continue
            tag_text = ""
            if source == "freesound" and key:
                try:      # tags carried the meaning at ingest — refetch them
                    d = NET.get_json(
                        f"https://freesound.org/apiv2/sounds/{rec['id']}/",
                        params={"token": key, "fields": "tags,description"})
                    tag_text = " ".join(d.get("tags", []) or [])[:300]
                except Exception:  # noqa: BLE001
                    tag_text = ""
            score, matched, negs, title_ok = score_item(theme, title, "", tag_text)
            threshold = base.SRC_THRESHOLD.get(source, base.DEFAULT_THRESHOLD)
            reason = ("title-irrelevant" if not title_ok
                      else f"relevance<{threshold}" if score < threshold else "")
            if not reason:
                keep_lines.append(line)
                kept += 1
                continue
            fp = rec.get("file_path", "")
            nbytes = int(rec.get("bytes", 0) or 0)
            log(f"  PURGE [{source}] s={score:3d} {theme:20} {title[:48]} "
                f"({reason})")
            if not dry_run:
                try:
                    if fp and os.path.exists(fp):
                        os.remove(fp)
                except OSError as e:
                    log(f"    delete failed: {e}")
                base.reject_log(source, rec.get("id", ""), theme,
                                f"retro-audit:{reason}", score, matched, negs,
                                title=title)
                # CONTRACT §4-v3-d tombstone (full record + why it was removed)
                base.atomic_append(
                    os.path.join(LEDGER_DIR, f"{source}_dedup_removed.jsonl"),
                    json.dumps(dict(rec,
                                    removed_at=datetime.now(timezone.utc)
                                    .isoformat(timespec="seconds"),
                                    removal_reason=reason, rescore=score,
                                    rescore_matched=matched,
                                    rule_version=RULE_VERSION),
                               ensure_ascii=False))
            purged_items += 1
            purged_bytes += nbytes
            s_purged += 1
        if s_purged and not dry_run:
            tmp = path + ".part"
            with open(tmp, "w", encoding="utf-8") as f:
                f.writelines(keep_lines)
            os.replace(tmp, path)
        log(f"retro-audit [{source}]: {len(records)} records, {s_purged} purged")
    log(f"RETRO-AUDIT {'(dry-run) ' if dry_run else ''}total: {purged_items} "
        f"items purged, {purged_bytes/GB:.3f} GB reclaimed, {kept} kept")
    return 0


def robots_verdicts(sources: list[str]) -> dict[str, str]:
    """Log and return robots.txt verdicts for the scraped listing hosts."""
    checks = {"mixkit": "https://mixkit.co/free-stock-video/ocean/",
              "coverr": "https://coverr.co/s?q=ocean"}
    verdicts: dict[str, str] = {}
    for src, url in checks.items():
        if src not in sources:
            continue
        try:
            ok = NET.robots_ok(url)
        except Exception as e:  # noqa: BLE001
            ok, verdicts[src] = True, f"robots fetch error ({e}) -> proceed politely"
        verdicts[src] = verdicts.get(
            src, "ALLOW" if ok else "DISALLOW -> source skipped")
        log(f"robots.txt [{src}] {url} -> {verdicts[src]}")
    return verdicts


def main() -> int:
    global PASS
    ap = argparse.ArgumentParser(
        description="PD modern-web free-asset ingest (media on D:, ledger on H:)")
    ap.add_argument("--source", default="all",
                    help="all | comma list of: " + ",".join(ADAPTERS))
    ap.add_argument("--theme", default="all",
                    help="all | comma list of: " + ",".join(ALL_THEMES))
    ap.add_argument("--cap-gb", type=float, default=0.0,
                    help="optional TOTAL cap GB, cumulative (0 = unlimited)")
    ap.add_argument("--limit", type=int, default=1000,
                    help="max items per source per theme PER PASS (smoke: 2-3)")
    ap.add_argument("--passes", type=int, default=1000,
                    help="max passes (pass N reads page N of each source)")
    ap.add_argument("--dry-run", action="store_true", help="list, don't download")
    ap.add_argument("--retro-audit", action="store_true",
                    help="re-score already-shelved items under the corrected "
                         "gate, delete+tombstone failures, then exit")
    args = ap.parse_args()

    base.load_env()
    if args.retro_audit:
        return retro_audit(args.dry_run)
    os.makedirs(LEDGER_DIR, exist_ok=True)
    if os.path.isdir(D_DRIVE):
        os.makedirs(D_ROOT, exist_ok=True)
    sources = SOURCE_ORDER if args.source == "all" else \
        [s.strip() for s in args.source.split(",") if s.strip() in ADAPTERS]
    themes = ALL_THEMES if args.theme == "all" else \
        [t.strip() for t in args.theme.split(",") if t.strip() in ALL_THEMES]
    if not sources or not themes:
        log("nothing to do (bad --source/--theme)")
        return 2

    idx = build_existing_index()
    FACTORY_PIXABAY.update(idx.get("ids", {}).get("pixabay", []))
    ledger = base.Ledger(args.cap_gb)
    ledger.shas |= set(idx.get("sha256", []))   # content dedup vs factory shelf
    log(f"run start: sources={sources} themes={len(themes)} cap={args.cap_gb}GB "
        f"limit={args.limit}/src/theme/pass dry_run={args.dry_run}")
    log(f"resume state: {len(ledger.done)} items in shared ledgers; factory index: "
        f"{len(FACTORY_PIXABAY)} pixabay ids, {len(idx.get('sha256', []))} shas")
    log(f"D: free {base.drive_free(D_DRIVE)/GB:.0f}GB, floor {D_FLOOR/GB:.0f}GB "
        f"(hard guard)")
    verdicts = robots_verdicts(sources)
    for src, v in verdicts.items():
        if v.startswith("DISALLOW"):
            sources.remove(src)

    status: dict[str, str] = {s: "working" for s in sources}
    counts: dict[str, int] = {}
    active = list(sources)
    for pass_n in range(1, args.passes + 1):
        PASS = pass_n
        pass_new = 0
        log(f"===== PASS {pass_n} (sources: {active}) =====")
        for src in list(active):
            for theme in themes:
                if ledger.run_full() or pick_root(theme, "x") is None:
                    break
                try:
                    n = ADAPTERS[src](ledger, theme, args.limit, args.dry_run)
                    if n:
                        log(f"[p{pass_n}:{src}] theme={theme} +{n}")
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
        if ledger.run_full() or pick_root(themes[0], "x") is None:
            log("cap or D: free-space floor reached — stopping")
            break
        if pass_new == 0:
            log("no new items this pass — sources exhausted at current queries")
            break
        if not active:
            break

    log("=" * 70)
    log("SUMMARY (modern-web lane)")
    for src in SOURCE_ORDER:
        if src in counts or src in status:
            log(f"  {src:14} {counts.get(src, 0):5d} new items  "
                f"[{status.get(src, 'not selected')}]")
    log(f"  this run: {ledger.run_items} items, {ledger.run_bytes/GB:.2f} GB")
    for t in sorted(set(themes) & set(ledger.theme_items)):
        log(f"  theme {t:24} {ledger.theme_items[t]:5d} items "
            f"{ledger.theme_bytes[t]/GB:7.2f} GB (all lanes)")
    log("ledger: " + LEDGER_DIR)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("interrupted")
        sys.exit(130)
