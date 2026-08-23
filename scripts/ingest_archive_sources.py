# -*- coding: utf-8 -*-
"""
Multi-source free-asset ingest pipeline for the Prime Documentary archive shelf.

Downloads THEMED (not bulk) public-domain / CC0 / clearly-free-commercial assets from
approved sources into a rights-tracked, MULTI-ROOT tiered shelf (~4.4TB total budget):

  Tier 1  H:\\pd-media\\assets\\archive\\<theme>\\   STOP if H: free < 500GB
          (historical: H: died, and TIERS below no longer contains this root)
  Tier 2  D:\\pd-archive\\<theme>\\                  STOP if D: free < 250GB
  Tier 3  E:\\pd-archive\\<theme>\\                  STOP if E: free < 250GB
  Tier 4  F:\\pd-archive\\<theme>\\                  STOP if F: free < 50GB

When a tier's budget/floor is hit the router continues on the next tier automatically.
Lane routing: PD-lane themes start on Tier 1 (H:, production-adjacent); BROAD themes
(future channels: space/nature/cities/japan/PD films/etc.) start on Tier 2 and fill D->E->F.
C: is NEVER used. Quarantine and the centralized ledger always live on H::

    E:\\pd-media\\assets\\archive\\_quarantine\\<theme>\\  (license_decision=review_required)
    E:\\pd-media\\assets\\archive\\_ledger\\<source>.jsonl (per-item rights ledger)

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
Ledger contract for all agents: E:\\pd-media\\assets\\archive\\_ledger\\CONTRACT.md

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
# 2026-08-20: THE H: TIER IS GONE AND IS NOT COMING BACK. The plain Samsung T7 that
# carried it failed its USB interface -- proven by swapping only the drive in a port and
# cable that the T7 Shield then used successfully, twice. It draws bus power (the LED
# lights) and never enumerates, so the controller is dead and the ledger it held -- 39,092
# licensed videos, and the provenance for 88,850 catalogued assets whose files went with
# it -- is unrecoverable by any means available here.
#
# The router already fell through to D/E/F, so the FILES had somewhere to go. Only the
# LEDGER was pinned to tier 0, which meant a dead tier 0 took the whole shelf's memory with
# it. That is the same single-point-of-failure the media root had, and it is fixed the same
# way: the ledger lives on the roomiest surviving drive, and no tier is load-bearing for it.
TIERS = [
    {"name": "E", "root": r"E:\pd-archive", "drive": "E:\\", "floor": 250 * GB},
    {"name": "D", "root": r"D:\pd-archive", "drive": "D:\\", "floor": 250 * GB},
    {"name": "F", "root": r"F:\pd-archive", "drive": "F:\\", "floor": 50 * GB},
]
LEDGER_ROOT = r"E:\pd-archive"                   # 1,081 GB free at the time of the move
LEDGER_DIR = os.path.join(LEDGER_ROOT, "_ledger")
QUARANTINE = os.path.join(LEDGER_ROOT, "_quarantine")

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
              "portrait", "interview", "mugshot", "headshot", "zoom meeting",
              # live-reject finding 2026-07-28: a video-game stream ("SoulCalibur
              # Street Fighter Mix ... Season 19 Episode 21", 428MB) cleared the
              # gate on weak terms alone
              "video game", "street fighter", "soulcalibur", "twitch", "speedrun",
              "let's play", "esports", "walkthrough", "emulator", "rom hack"]
STOPWORDS = set("the a an of in on and or for with to at from by 1930s 1940s 1950s "
                "1960s 1970s old new".split())

# ---- relevance-v3 (2026-07-28): FALSE-NEGATIVE fix from the gov lane ----
# A single unambiguous domain term scored only 15 and silently discarded prime
# material (Nuremberg / Yokohama / Yamashita / Milch trial footage). Unambiguous
# terms now weigh +30 so ONE strong term clears the >=30 threshold WITHOUT
# lowering the threshold. Weak terms (common English words that appear in any
# archival title) stay at +15 and still need corroboration.
WEAK_TERMS = set("""
high street post office red door bell shop village city town main new old film movie
home water night light day world land sea air house building room car train station
machine music band hall book paper wall stone block cell bar line board box american
british england britain london chicago japan tokyo kyoto rural urban aerial night
close macro dark abstract background texture wind rain storm clouds birds forest
mountain desert river ocean waves coast reef island bridge tower park square market
school church fair county state federal national public private modern vintage retro
period silent western feature classic scene view interior exterior street-level
production process assembly equipment technology science research industrial
performance recording concert orchestra jazz band commercial advertisement poster
label product picture image photo video audio sound ambience noise hum rumble echo
""".split())
# extra unambiguous domain terms per theme (not present in the query table but
# unmistakable subject matter — the gov lane's recovered material lives here)
STRONG_EXTRA: dict[str, list[str]] = {
    "courtroom_justice": ["nuremberg", "tribunal", "courtroom", "courthouse", "judiciary",
                          "defendant", "prosecution", "verdict", "testimony", "arraignment",
                          "yamashita", "milch", "indictment", "adjudication",
                          # recovered from live reject titles (2026-07-28): prime
                          # courtroom material whose titles use trade vocabulary
                          "cross-examination", "perjury", "subpoena", "acquittal",
                          "mistrial", "habeas", "litigation", "deposition", "plaintiff",
                          "appellate", "prosecutor", "attorney", "jury", "juror"],
    "prison_jail": ["penitentiary", "incarceration", "inmate", "alcatraz", "sing-sing",
                    "reformatory", "cellblock", "warden"],
    "police_period": ["constabulary", "gendarmerie", "patrolman", "squad-car"],
    "police_modern": ["swat", "dispatcher", "cruiser"],
    "newspapers_printing": ["linotype", "letterpress", "typesetting", "pressroom", "newsroom"],
    "uk_highstreet_postoffice": ["postbox", "sub-postmaster", "royal-mail", "greengrocer",
                                 "haberdashery", "pillar-box"],
    "navy_harbor": ["shipyard", "drydock", "quayside", "stevedore", "battleship", "frigate"],
    "laboratory_forensics": ["forensic", "spectrometer", "centrifuge", "petri", "microscope"],
    "government_buildings": ["capitol", "statehouse", "parliament", "chancery"],
    "period_telephone_tech": ["switchboard", "telegraph", "teletype", "rotary-dial"],
    "money_banking": ["bullion", "mint", "vault", "bourse", "clearinghouse"],
    "war_history": ["newsreel", "artillery", "regiment", "battalion", "armistice"],
    "space_nasa": ["apollo", "gemini", "nebula", "orbiter", "cosmonaut", "launchpad"],
    # BIGRAMS: ambiguity is per-WORD, not per-phrase. "city"/"street"/"american"
    # are weak alone, but "american city"/"main street" are unmistakable subject
    # matter. Without these the weak-only cap discarded genuine period material
    # ("Dynamic American City", Prelinger 1956). term_hits() matches across
    # hyphen or space, so "high-street" and "high street" both hit.
    "americana_1930s_1970s": ["american city", "main street", "small town", "drive-in",
                              "soda fountain", "five-and-dime", "streetcar", "trolley",
                              "steam locomotive", "assembly line", "roadside"],
    "small_town": ["small town", "main street", "town square", "water tower",
                   "county fair", "village green"],
    "chicago_city": ["elevated train", "elevated railway", "chicago river", "skyline"],
    "uk_period": ["high street", "british railway", "steam railway"],
}
STRONG_EXTRA["uk_highstreet_postoffice"] += ["high street", "post office", "royal mail",
                                            "corner shop", "village shop"]
STRONG_EXTRA["navy_harbor"] += ["naval shipyard", "harbor docks", "dry dock"]
STRONG_EXTRA["newspapers_printing"] += ["printing press", "printing house", "front page"]
STRONG_EXTRA["money_banking"] += ["bank vault", "stock exchange", "trading floor",
                                  "cash register"]
STRONG_EXTRA["government_buildings"] += ["city hall", "supreme court", "capitol dome"]
STRONG_EXTRA["period_telephone_tech"] += ["telephone switchboard", "rotary telephone",
                                          "telephone booth"]
STRONG_EXTRA["laboratory_forensics"] += ["crime lab", "chemistry lab", "test tube"]
# sense guards: a term match is CANCELLED when the surrounding phrase is a different
# sense (the both-end boundary alone cannot catch these multi-word senses)
SENSE_GUARDS: dict[str, list[str]] = {
    "trial": [r"trial run", r"clinical trial", r"sea trial", r"field trial",
              r"trial and error", r"time trial", r"trial by fire"],
    "court": [r"tennis court", r"basketball court", r"food court", r"courting",
              r"court(?:s|ing)? (?:her|him|a lady)", r"courtesy", r"courtyard"],
    "cell": [r"cell (?:phone|biology|division|culture)", r"blood cell", r"stem cell",
             r"fuel cell", r"solar cell"],
    "bar": [r"bar (?:graph|chart)", r"crow ?bar", r"candy bar", r"sand ?bar"],
    "mint": [r"mint (?:leaf|leaves|tea|condition|green)", r"peppermint", r"spearmint"],
    "vault": [r"pole vault", r"vaulted ceiling"],
    "block": [r"block (?:party|chain)", r"engine block", r"building blocks"],
    "post": [r"post ?war", r"post ?production", r"fence post", r"post ?script",
             r"post ?graduate", r"lamp ?post", r"goal ?post"],
    "mail": [r"mail ?order", r"chain ?mail", r"e-?mail"],
    # Added 2026-08-10 from measurement, not from imagination: these are the senses
    # actually sitting in the MATCH tier of the factory shelf, where the selector
    # trusts them. Counts are match-tier items whose title carries the wrong sense.
    # The right sense is deliberately left alone -- the Wall Street bull, the scales
    # of justice, the electric chair and a bank vault all still match.
    "bull": [r"bull (?:terrier|riding|rider|fighting|fight)", r"pit ?bull",
             r"rodeo", r"bull in (?:a )?(?:field|pasture)"],          # 41: rodeo, dogs
    "globe": [r"(?:desk|table|vintage|antique|decorative|wooden|snow) globe",
              r"globe (?:ornament|decoration)", r"snow ?globe"],       # 33: ornaments
    "blood": [r"blood (?:pressure|sugar|orange|moon)", r"bloodhound"], # 31: BP monitors
    "chair": [r"(?:office|dining|deck|beach|high|rocking) chair",
              r"wheel ?chair", r"arm ?chair"],                         # 12: furniture
    "case": [r"(?:guitar|phone|pencil|camera|display|glasses) case",
             r"book ?case", r"stair ?case", r"case study"],            # 8: containers
    "scale": [r"(?:kitchen|bathroom|weighing) scale", r"fish scale",
              r"scale model", r"(?:full|large|small).scale"],          # 4: cooking, models
    "bank": [r"(?:river|canal|fog|snow|cloud|sand|grass|grassy|steep|muddy) ?banks?",
             r"bank of (?:a )?(?:river|fog|cloud|snow)", r"riverbank"],  # 1: riverbank
}
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
        terms |= {t.lower() for t in STRONG_EXTRA.get(theme, [])}
        _theme_pos_cache[theme] = (terms, phrases)
    return _theme_pos_cache[theme]


def term_weight(theme: str, term: str) -> int:
    """+30 for unambiguous domain terms (ONE clears the >=30 threshold), +15 for weak
    common-English terms that need corroboration. relevance-v3, gov-lane finding."""
    if term in STRONG_EXTRA.get(theme, []):
        return 30
    return 15 if term in WEAK_TERMS else 30


def sense_ok(term: str, text: str) -> bool:
    """False when the match is a different sense of the word (guard phrases).

    A plural falls back to the guards written for the singular. SENSE_GUARDS is
    keyed by term and several theme vocabularies carry the plural as its own entry,
    so the guard written for "scale" was never consulted for "scales" -- measured,
    that is how a kitchen scale stayed in the match tier under legal_court. The
    same hole left "cells" (blood cells), "bars" (candy bar), "chairs" and "lights"
    unguarded while every one of their singulars was covered."""
    guards = SENSE_GUARDS.get(term)
    if guards is None and term.endswith("es"):
        guards = SENSE_GUARDS.get(term[:-2])
    if guards is None and term.endswith("s"):
        guards = SENSE_GUARDS.get(term[:-1])
    return not any(re.search(p, text) for p in guards or [])


def term_hits(term: str, text: str) -> bool:
    """Whole-word match anchored at BOTH ends, allowing plural/possessive suffixes.

    CRITICAL (bug found by the gov lane 2026-07-28): a leading-only boundary
    (`\\bcourt`) matches "courtesy"/"courtyard" in archival boilerplate and admitted
    clearly off-theme items at exactly the threshold. Both ends must be anchored.
    "courts"/"trials"/"prison's" pass; "courtesy"/"courtyard" do not.

    Multi-word terms match across hyphen OR space ("cross-examination" finds
    "Cross Examination" — a live reject title that was prime courtroom material)."""
    core = r"[-\s]+".join(re.escape(p) for p in re.split(r"[-\s]+", term) if p)
    return re.search(rf"\b{core}(?:s|es|'s|s')?\b", text) is not None


def relevance(theme: str, title: str, desc: str = "") -> tuple[int, list[str], list[str], bool]:
    """Score 0-100 from item metadata vs theme keywords.
    Returns (score, matched, neg_hits, title_ok).

    +15 per distinct positive term (cap 60), +25 if a full query phrase appears,
    -25 per negative keyword. `title_ok` is the TITLE-RELEVANCE GATE: an item must
    carry >=1 positive term in its TITLE, not merely somewhere in the description —
    description-only matches are archival boilerplate, not subject matter."""
    t_low = (title or "").lower()
    low = f"{title} {desc}".lower()
    pos, phrases = theme_terms(theme)
    matched = sorted({t for t in pos if term_hits(t, low) and sense_ok(t, low)})
    title_matched = [t for t in matched if term_hits(t, t_low) and sense_ok(t, t_low)]
    score = min(60, sum(term_weight(theme, t) for t in matched))
    phrase_ok = any(p in low for p in phrases)
    if phrase_ok:
        score += 25
    # WEAK-ONLY CAP (live-reject finding 2026-07-28): two weak common words summed to
    # exactly the threshold and admitted a 428MB video-game stream ("SoulCalibur
    # Street Fighter Mix...") into uk_highstreet_postoffice. An item must carry >=1
    # STRONG domain term or a full query phrase; weak words alone can never clear 30.
    # Encoded in the score (not a 5th return value) to keep this function's signature
    # stable for the sibling lanes that import it.
    if not phrase_ok and not any(term_weight(theme, t) >= 30 for t in matched):
        score = min(score, 15)
    negs = [n for n in GLOBAL_NEG if n in low]
    score -= 25 * len(negs)
    return max(0, min(100, score)), matched, negs, bool(title_matched)


LANE = os.environ.get("PD_INGEST_LANE", "ia")  # per-lane reject file (append safety)


def atomic_append(path: str, line: str) -> None:
    """Concurrency-safe append for files shared across parallel lanes.

    4 lanes appending to one handle produced torn/interleaved JSON lines. Opening
    with os.O_APPEND and issuing ONE write() of a single <4KB line is atomic on
    Windows and POSIX; combined with per-lane reject files (merged on read) there
    is no interleaving window left."""
    data = (line.rstrip("\n") + "\n").encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)


_VERDICTS: dict | None = None


def theme_source_unusable(theme: str, source: str) -> bool:
    """True when the owner has looked at this theme/source on a contact sheet and ruled
    it out. Read fresh from `_qc/archive_verdicts.jsonl`, cached for the process.

    Added to the base 2026-08-09 so all lanes share one gate. Previously only the
    science/museum lane checked, which is why a running lane kept re-fetching material
    that had already been reviewed and deleted."""
    global _VERDICTS
    if _VERDICTS is None:
        _VERDICTS = {}
        path = os.path.normpath(os.path.join(LEDGER_DIR, "..", "_qc",
                                             "archive_verdicts.jsonl"))
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        r = json.loads(line)
                    except Exception:
                        continue
                    if (r.get("verdict") or "").lower() == "unusable":
                        _VERDICTS[(r.get("theme"), r.get("source"))] = True
        except OSError:
            pass
    return (theme, source) in _VERDICTS


_MEETING = None


def is_meeting_recording(title: str) -> bool:
    """True for a gavel-to-gavel recording of a proceeding — council session, hearing,
    sermon. Unusable as b-roll at any length: a fixed camera on a dais for two hours.

    Shares its word list with scripts/purge_meeting_recordings.py so the rule that deletes
    and the rule that blocks stay identical. Checked before download, so there is no byte
    count yet and the purge tool's size floor is not applied here."""
    global _MEETING
    if _MEETING is None:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from purge_meeting_recordings import MEETING_TERMS, STRONG
            _MEETING = tuple(MEETING_TERMS) + tuple(STRONG)
        except Exception:
            _MEETING = ()
    if not _MEETING:
        return False
    t = " " + " ".join((title or "").lower().split()) + " "
    return any(k in t for k in _MEETING)


def reject_log(source: str, item_id: str, theme: str, reason: str,
               score: int = -1, matched=None, negs=None, title: str = "") -> None:
    """Per-item rejects log (skipped items do NOT enter the main ledger).

    Writes to a PER-LANE file `rejects_<lane>.jsonl` (merged on read) via an
    atomic append. `title` is REQUIRED in practice: without reject titles,
    false negatives are invisible — the failure direction that silently discarded
    prime material (gov lane, 2026-07-28)."""
    try:
        os.makedirs(LEDGER_DIR, exist_ok=True)
        atomic_append(os.path.join(LEDGER_DIR, f"rejects_{LANE}.jsonl"), json.dumps({
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source": source, "id": str(item_id)[:200], "title": str(title)[:300],
            "theme": theme, "reason": reason, "score": score,
            "matched": matched or [], "neg": negs or []}, ensure_ascii=False))
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
    # ------------------------------------------------------------------ place-neutral
    # Added 2026-08-23. Measured against the 25,758 commercially-licensed videos on the
    # shelf, these five registers were the thin ones: night road 41, window light 107,
    # clock 118, corridor 212, anonymous crowd 324, against 700-2,700 for rain, sky, water,
    # fog, hands, paper and texture.
    #
    # Every query here obeys the rule EP71 paid for: TIGHT FRAMING TRAVELS, A WIDE SHOT
    # CARRIES ITS PLACE WITH IT. A raindrop on glass, a lamp in fog and an anonymous hand
    # are the same object anywhere on earth; a hillside, a street or a building are not.
    # EP71's first query set asked a global stock shelf for places and 3 of 56 clips
    # survived contact-sheet review. The replacement asked for objects and 38 of 112 did.
    # So: no city, no country, no architecture, no signage, no faces. Close, and anonymous.
    "night_road_lamp": {
        "video": ["street lamp glow night", "headlights passing in the dark",
                  "wet asphalt reflection night", "single lamp in fog",
                  "car light streaks long exposure", "rain on road at night",
                  "traffic light reflection wet street", "kerb at night in rain"],
        "image": ["street lamp at night", "wet asphalt at night", "headlight trails"],
        "audio": [],
    },
    "window_interior_light": {
        "video": ["sunlight through blinds", "curtain moving in breeze",
                  "dust floating in a sunbeam", "light moving across an empty wall",
                  "rain on a window from inside", "shadow moving on a floor",
                  "lamp in a dark room", "morning light on a table"],
        "image": ["light through blinds", "dust in sunlight", "empty room window light"],
        "audio": [],
    },
    "clock_and_waiting": {
        "video": ["clock second hand close up", "wall clock ticking",
                  "wristwatch close up", "calendar page turning",
                  "hourglass sand falling", "digital clock numbers changing",
                  "empty chairs in a waiting room"],
        "image": ["clock face close up", "wristwatch macro", "hourglass sand"],
        "audio": [],
    },
    "corridor_and_stairs": {
        "video": ["empty corridor walking", "stairwell looking up",
                  "footsteps on concrete stairs", "fluorescent corridor lights",
                  "a door closing at the end of a hallway", "handrail close up",
                  "elevator doors closing"],
        "image": ["empty corridor", "stairwell from below", "handrail detail"],
        "audio": [],
    },
    "anonymous_crowd": {
        "video": ["crowd walking blurred", "silhouettes of people backlit",
                  "commuters in slow motion", "feet walking on pavement",
                  "shoulders passing in a crowd", "people crossing out of focus",
                  "hands in a crowd"],
        "image": ["blurred crowd", "silhouette of a person backlit", "feet on pavement"],
        "audio": [],
    },
    # Added 2026-08-21 for EP74 itaewon. The local shelf holds 14,663 videos -- verified
    # by counting the files on E:, D: and F:, which match the ledger row for row, so the
    # index is not the problem: roughly half the video archive went with the H: drive.
    # Nothing left in it answers "a Korean hillside backstreet at night". Pixabay does --
    # probed 2026-08-21, "seoul night", "korea street", "night alley", "neon alley",
    # "wet street night" and "crowd night street" each return the 500-item display cap.
    #
    # EXCLUDED ON PURPOSE, learned from this episode's own footage review: bare "alley"
    # returns the BOTANICAL sense (avenues of trees in parks) and bare "station" returns
    # the International Space Station. Both are paired here or left out.
    "itaewon_korea_night": {
        "video": [
                  'seoul',
                  'seoul night',
                  'seoul street',
                  'seoul street night',
                  'korea street',
                  'korean street',
                  'korea night',
                  'korean night street',
                  'seoul subway',
                  'subway seoul',
                  'korean alleyway',
                  'korea alleyway',
                  'night alley',
                  'narrow street night',
                  'neon alley',
                  'neon street night',
                  'wet street night',
                  'rain street night',
                  'asian street night',
                  'night market street',
                  'crowd night street',
                  'crowded street night',
                  'pedestrian night street',
                  'shop shutter street',
                  'street food stall night',
                  'underground station stairs',
                  'subway escalator crowd',
                  'turnstile station',
                  'cctv camera street',
                  'traffic cone barrier',
                  'police barrier street',
                  'empty alley morning',
                  'street cleaning morning',
                  'korean signage street',
                  # WAVE 2, 2026-08-22. Wave 1 gave 453 clips -> 603 candidates -> 378 for a
                  # content verdict -> 261 after a title triage, against 265 DISTINCT required
                  # and before one frame had been opened. Four short is no margin when EP71
                  # measured a comparable sample at 50% off-register. This wave targets what
                  # the scene plan asks for and wave 1 under-supplied: the slope, the stairs,
                  # the queue outside a bar, the scooter, the barrier, the state's rooms.
                  'itaewon',
                  'hongdae',
                  'gangnam street',
                  'myeongdong',
                  'busan street',
                  'korea alley night',
                  'seoul rain',
                  'seoul crowd',
                  'seoul alley',
                  'korean restaurant street',
                  'korean bar street',
                  'korean convenience store',
                  'backstreet night',
                  'back alley night',
                  'narrow lane night',
                  'steep street',
                  'sloped street',
                  'hill street night',
                  'stairs street night',
                  'alley stairs',
                  'night street lamp',
                  'street lamp rain',
                  'vending machine street',
                  'scooter street night',
                  'motorbike alley',
                  'delivery scooter night',
                  'crowd walking night',
                  'people crossing night',
                  'umbrella rain night',
                  'pedestrian crossing night',
                  'queue outside bar',
                  'bar entrance night',
                  'korean police',
                  'police korea',
                  'emergency lights night',
                  'ambulance night street',
                  'cctv pole street',
                  'street barrier night',
                  'hazard cone night',
                  'road cone night',
                  'office corridor empty',
                  'government office korea',
                  'court corridor',
                  'empty meeting room',
                  'waiting room chairs',
                  'hearing room empty',
        ],
        "image": ["seoul street", "korea street night", "neon alley"],
        "audio": [],
    },
    'uk_highstreet_postoffice': {
        'video': ['british high street', 'post office britain', 'england village shops'],
        'image': ['british high street shops', 'royal mail post office', 'red postbox england'],
        'audio': ['british street ambience', 'shop bell door'],
    },
    'courtroom_justice': {
        'video': ['gavel on wooden desk', 'empty jury box seats', 'judge in robe', 'attorney reading case files', 'court hearing room', 'stack of legal papers', 'signing document with pen', 'courtroom', 'courthouse', 'trial court judicial', 'judge gavel close up', 'empty jury box', 'witness stand courtroom', 'courthouse steps walking', 'lawyer walking with briefcase', 'law library shelves', 'signing legal document hands'],
        'image': ['courtroom interior', 'courthouse architecture', 'scales of justice gavel', 'jury box empty seats', 'judge bench gavel', 'law books shelf', 'legal documents stack desk', 'courthouse steps columns'],
        'audio': ['courtroom ambience', 'gavel knock wood'],
    },
    'prison_jail': {
        'video': ['handcuffs on wrists', 'person being arrested', 'prison guard tower', 'inmate walking corridor', 'prison', 'penitentiary', 'jail cell block', 'prison razor wire fence', 'cell door closing', 'prison yard walking', 'handcuffs close up', 'prison visitation room', 'prison corridor walking'],
        'image': ['prison corridor cells', 'penitentiary building', 'jail bars', 'razor wire prison fence', 'handcuffs on table', 'empty prison cell bunk', 'prison watchtower', 'barred window light'],
        'audio': ['prison door slam', 'metal door clang echo'],
    },
    'police_period': {
        'video': ['police 1950s', 'police patrol vintage', 'law enforcement 1960s'],
        'image': ['police station vintage', 'patrol car 1950s', 'police call box'],
        'audio': ['vintage police siren', 'police radio chatter'],
    },
    'police_modern': {
        'video': ['sheriff badge close up', 'sheriff patrol vehicle', 'sealed evidence bag', 'fingerprint card ink', 'police evidence room', 'seized property storage', 'police car night lights', 'police patrol city', 'traffic stop at night', 'police body camera view', 'evidence bag gloves', 'fingerprint scanning', 'patrol car dashboard driving', 'police interview room'],
        'image': ['police car lights night', 'police tape crime scene', 'police badge close up', 'evidence bags table', 'interrogation room table', 'patrol car door emblem'],
        'audio': ['police siren city', 'radio dispatch static'],
    },
    'americana_1930s_1970s': {
        'video': ['main street 1950s', 'american factory 1940s', 'trains railroad 1950s', 'diner drive-in 1950s', 'american city street 1930s'],
        'image': ['main street storefronts 1950s', 'railroad steam locomotive', 'american diner neon sign', 'factory assembly line 1940s'],
        'audio': ['steam train whistle', 'diner ambience 1950s'],
    },
    # 2026-08-20. EP70 wronghouse needs an American suburban / federal-courthouse / 1973
    # register, and measuring the surviving shelf for it returned Copenhagen, a Japanese
    # pagoda, Mexican desert highways and 3D chroma-key offices -- 5 of 5 sampled contact
    # sheets a total loss. The broad theme queries ('small town america', 'rural town street')
    # then fetched Africa, beaches and a business meeting: 267 items, 21 reaching candidates,
    # none on register.
    #
    # These queries are NOT invented. They are the SUBTYPE NAMES of the lost factory shelf,
    # read out of the surviving catalogue , which recorded
    # 141 EP70-relevant video subtypes at ~50 clips each -- front_door_house 57,
    # government_building_exterior 57, rural_road_america 56, police_badge_close_up 55,
    # vintage_typewriter 54, american_suburb_aerial 53, courthouse_steps 52,
    # documents_on_desk 52, law_library_books 52, white_picket_fence 50,
    # small_town_main_street 49, for_sale_sign_yard 49, long_shadow_of_a_person 49.
    # That shelf was built from these phrases and it worked; the files died with H:, the
    # vocabulary did not. A subject is the unit that retrieves footage. A word is not.
    'ep70_american_suburb': {
        'video': ['front door house', 'american suburb aerial', 'white picket fence',
                  'suburban house exterior', 'for sale sign yard', 'small town main street',
                  'rural road america', 'empty road sunset', 'highway night long exposure',
                  'moving boxes empty room', 'rain on window night', 'long shadow of a person',
                  'lone person silhouette walking', 'foggy forest', 'lone tree in field',
                  'sun through trees forest'],
        'image': ['front door house', 'american suburb aerial', 'white picket fence',
                  'suburban house exterior', 'small town main street', 'rural road america'],
        'audio': [],
    },
    'ep70_federal_court': {
        'video': ['courthouse steps', 'government building exterior', 'law library books',
                  'documents on desk', 'office interior dark', 'contract paperwork signing',
                  'us constitution document', 'police badge close up', 'prison corridor',
                  'vintage typewriter', 'vintage film camera', 'newspaper macro'],
        'image': ['courthouse steps', 'government building exterior', 'law library books',
                  'documents on desk', 'us constitution document', 'vintage typewriter'],
        'audio': [],
    },
    'small_town': {
        'video': ['small town america', 'rural town street', 'county fair town', 'rural highway driving night', 'gas station at night', 'suburban street driving', 'mailbox rural road', 'porch of old house'],
        'image': ['small town main street', 'water tower town', 'rural church town square', 'rural mailbox road', 'gas station sign dusk', 'modest suburban house'],
        'audio': ['small town ambience birds', 'church bells distant'],
    },
    'newspapers_printing': {
        'video': ['newspaper printing press', 'linotype newsroom', 'newspaper production', 'printing press running', 'newspaper rolling off press', 'typing on typewriter', 'stack of newspapers'],
        'image': ['printing press machinery', 'newspaper front page press', 'linotype machine', 'newspaper stack close up', 'typewriter keys'],
        'audio': ['printing press machine', 'typewriter keys newsroom'],
    },
    'uk_period': {
        'video': ['london 1950s', 'britain 1960s street', 'england industrial 1940s'],
        'image': ['london street 1950s', 'british railway station period', 'england town 1930s'],
        'audio': ['big ben chimes', 'steam railway station ambience'],
    },
    'chicago_city': {
        'video': ['chicago city', 'chicago elevated train', 'chicago skyline street'],
        'image': ['chicago skyline', 'chicago elevated railway', 'chicago river bridges'],
        'audio': ['elevated train rumble', 'city wind traffic'],
    },
    'navy_harbor': {
        'video': ['navy ships harbor', 'naval shipyard', 'harbor docks cargo'],
        'image': ['navy warship harbor', 'shipyard cranes docks', 'lighthouse harbor'],
        'audio': ['ship horn harbor', 'seagulls dock water'],
    },
    'laboratory_forensics': {
        'video': ['laboratory science equipment', 'chemistry lab research', 'microscope lab'],
        'image': ['laboratory glassware equipment', 'microscope close up', 'test tubes chemistry'],
        'audio': ['laboratory equipment hum', 'glass beaker clink'],
    },
    'government_buildings': {
        'video': ['public hearing room', 'city council meeting', 'notary stamp document', 'capitol government building', 'washington dc buildings', 'city hall architecture', 'state capitol exterior', 'federal building entrance', 'government office corridor', 'flag pole government building', 'city council chamber'],
        'image': ['capitol dome architecture', 'government building columns', 'supreme court building', 'state capitol dome', 'federal courthouse facade', 'government office corridor', 'official seal wall'],
        'audio': ['marble hall footsteps echo', 'flag rope flagpole wind'],
    },
    'period_telephone_tech': {
        'video': ['telephone switchboard', 'rotary telephone', 'telegraph communication vintage'],
        'image': ['rotary telephone vintage', 'switchboard operator equipment', 'telephone booth old'],
        'audio': ['rotary dial telephone', 'telephone ring vintage bell'],
    },
    # Added 2026-08-02 for the planned finance/business channel. Measured gap: the shelf
    # holds 496 clips matching "money" and 233 matching "stock", but zero for bankruptcy,
    # foreclosure, eviction, unemployment or a queue — the generic nouns are plentiful and
    # the SCENES a finance story is actually told in are missing.
    # Prime Finance / Prime Business, from two agents that measured the shelf before
    # proposing (2026-08-02). Both reported the same structural hole: the shelf is rich in
    # WIDE and AMBIENT - offices, towers, ports, highways - and near-empty on HANDS,
    # TRANSACTIONS and close human action. Every "hands doing a task" probe came back zero.
    # That is the register a company or money story needs to stop feeling like a stock reel,
    # so those queries are listed first.
    'hands_and_transactions': {
        'video': ['hands counting banknotes desk', 'thumb pressing calculator keys', 'hand signing cheque', 'fingers sorting coins tray', 'hand stamping passport document', 'wiping counter shop hands', 'hands tying parcel string', 'gloved hands sorting mail', 'hand turning key lock', 'hands folding newspaper', 'pouring coffee diner counter', 'hand writing on clipboard', 'hands assembling electronics parts', 'gloved hands quality inspection',
                  'worker stocking shelves store', 'checkout scanning groceries',
                  'receipt printing till closeup', 'hands calculator spreadsheet desk',
                  'handheld scanner beeping box', 'badge tapped door reader',
                  'hands flipping file pages', 'rubber stamp hitting paper',
                  'shredder eating documents closeup', 'filing cabinet drawer opening',
                  'cash drawer opening bills', 'hands opening cardboard parcel',
                  'screwdriver assembling small device'],
        'image': ['handwritten ledger page closeup', 'redacted memo black lines',
                  'stacked bankers boxes room', 'hand written price tag'],
    },
    'bank_and_branch': {
        'video': ['counting money machine bills', 'money counter machine banknotes', 'hands stacking banknotes', 'bank passbook stamped', 'coin sorting machine tray', 'cash register drawer bell', 'money changer booth window', 'currency exchange counter city', 'passbook stamped counter', 'security camera bank ceiling', 'bank teller window counter', 'queue outside bank doors',
                  'closed shutters bank entrance', 'vault door wheel turning',
                  'empty bank lobby chairs', 'armored truck loading cash',
                  'night deposit slot wall', 'safe deposit box drawer'],
        'image': ['bank teller window vintage', 'crowd outside bank doors',
                  'vault door open interior', 'bank branch closed sign'],
    },
    'household_loss': {
        'video': ['eviction notice posted door', 'foreclosure sign lawn house', 'boarded window shop closed', 'repossession notice paper', 'rent notice envelope hand', 'utility meter dial spinning', 'thermostat dial cold house', 'ramen packet cheap meal', 'bus stop waiting rain', 'laundromat washing machines', 'second hand shop interior', 'garage sale front lawn', 'eviction notice taped door', 'foreclosure sign front lawn',
                  'empty supermarket shelves aisle', 'price tag being replaced',
                  'unpaid bills envelope stack', 'overflowing mailbox letters closeup',
                  'car towed away street', 'keys handed over doorway',
                  'boarded up shop window', 'empty living room moving',
                  'pawn shop window display', 'fuel pump numbers spinning'],
        'image': ['eviction notice on door', 'foreclosure sign suburban house',
                  'bare supermarket shelves wide', 'pile of overdue bills'],
    },
    'market_machinery': {
        # 'stock chart crashing down' / 'red declining graph screen' / 'market index falling
                  # display' were tried and removed within the hour: on pixabay the tag lists
                  # carry 'wolf down' and 'to come down', so a chamois, a red panda, a goat and
                  # a giraffe all entered market_machinery on the word 'down'. Direction words
                  # are worthless as search terms here; name the object instead.
                  'video': ['stock ticker board display', 'financial data screen closeup', 'trading terminal screens', 'green numbers screen scrolling', 'graph line rising screen', 'graph line falling screen', 'telephone handset desk office', 'clock second hand macro', 'newspaper financial pages', 'calculator tape printing', 'ticker tape scrolling board', 'wall of monitors charts',
                  'trader desk six screens', 'empty trading desks dark',
                  'phones ringing trading desk', 'printer spitting trade tickets',
                  'crypto mining rigs rows', 'cooling fans data hall',
                  'fiber optic cables closeup'],
        'image': ['mechanical ticker board digits', 'trading pit crowd overhead',
                  'dealing room desks screens', 'stock certificate engraved paper'],
    },
    'goods_in_motion': {
        'video': ['conveyor parcels moving overhead', 'barcode scanner red beam', 'shipping label printer', 'stacked crates warehouse dark', 'container yard aerial rows', 'truck driving night highway rain', 'railway freight cars passing', 'pallet racking warehouse aisle', 'parcels sliding sorting chute',
                  'warehouse worker scanning parcel', 'forklift lifting pallet',
                  'wooden crate shipping stencil', 'truck reversing loading dock',
                  'delivery driver knocking door', 'parcel left on doorstep',
                  'courier bicycle city traffic', 'gantry crane lifting container night',
                  'cargo ship anchored offshore', 'excavator open pit mine'],
        'image': ['shipping manifest paperwork', 'stacked parcels sorting depot',
                  'empty pallet stack yard', 'cargo bill of lading document'],
    },
    'selling_floor': {
        'video': ['price gun labelling product', 'shopping basket handheld aisle', 'butcher counter display', 'bakery counter morning', 'newsagent kiosk street', 'vending machine coins', 'shop bell door opening', 'clearance sale clothing rack', 'shop window mannequin display',
                  'department store escalator moving', 'shutter closing shop front',
                  'shopkeeper opening shutters morning', 'chairs stacked closed restaurant',
                  'queue of people outside shop', 'market stall vendor customer',
                  'empty strip mall parking', 'auctioneer gavel warehouse sale'],
        'image': ['vintage department store interior', 'closing down sale window sign',
                  'empty shop interior fixtures removed', 'mail order catalog pages'],
    },
    'decision_rooms': {
        'video': ['conference table papers scattered', 'gavel auction podium', 'name plates conference table', 'coffee cups after meeting', 'clock boardroom wall', 'handshake silhouette window', 'lift doors closing office', 'empty boardroom chairs table', 'shareholder meeting seated hall',
                  'microphones on press podium', 'photographers cameras flashing crowd',
                  'audience applauding dark auditorium', 'projector slide dark room',
                  'hand drawing whiteboard diagram', 'abandoned desks dusty office',
                  'workers picket line placards', 'wrecking ball hitting building',
                  'janitor cleaning empty office', 'office lights turning off'],
        'image': ['bankruptcy court filing document', 'share certificate engraved paper',
                  'internal memo typed letter', 'vintage billboard roadside'],
    },
    'bench_to_line': {
        'video': ['welding sparks close up', 'lathe turning metal', 'circuit board soldering iron', 'sewing machine fabric factory', 'glass bottles filling line', 'packaging machine sealing', 'quality control weighing scale', 'garage workbench prototype tools', 'clay model prototype hands',
                  'cleanroom worker white suit', 'bakery production line oven',
                  'stainless steel brewery tanks', 'bottles moving fast conveyor',
                  'robot arm spraying car body', 'barcode label printer machine'],
        'image': ['workbench hand tools overhead', 'patent drawing technical diagram',
                  'factory blueprint sheet closeup', 'product prototype foam model'],
    },
    'business_corporate': {
        'video': ['boardroom meeting table', 'business handshake deal', 'corporate headquarters lobby',
                  'office workers walking corridor', 'presentation to investors', 'glass skyscraper low angle',
                  'commuters business district morning', 'data center server aisle', 'server racks blinking',
                  'earnings call phone desk', 'executive signing contract', 'open plan office night'],
        'image': ['boardroom empty table', 'corporate headquarters facade', 'business district skyline',
                  'server room racks', 'office desk documents'],
    },
    'economy_crisis': {
        'video': ['closed store shutter', 'boarded up storefront', 'foreclosure sign house',
                  'eviction notice door', 'unemployment line queue', 'empty shopping mall',
                  'abandoned factory interior', 'stock market crash screen', 'falling chart red screen',
                  'bank queue people waiting', 'for sale sign yard', 'empty office cubicles'],
        'image': ['boarded storefront', 'foreclosure sign', 'empty mall interior',
                  'abandoned factory', 'unemployment queue'],
    },
    'money_banking': {
        'video': ['stock ticker tape close up', 'trading floor shouting', 'candlestick chart screen', 'credit card payment terminal', 'atm withdrawal night', 'invoice paperwork desk', 'supermarket checkout scanner', 'retail store aisle', 'seized cash on table', 'auction gavel bidding', 'safe deposit box opened', 'bank teller counter', 'bank vault money', 'printing money mint', 'stock exchange trading floor', 'bank vault door opening', 'counting cash bundles', 'safe deposit boxes', 'cash in envelope hands', 'atm at night'],
        'image': ['bank vault door', 'dollar bills currency', 'bank building classical', 'bundled cash stacks', 'safe deposit box wall'],
        'audio': ['coins counting cash register', 'cash register bell vintage'],
    },
    'space_nasa': {
        'video': ['earth from space', 'rocket launch', 'moon surface apollo'],
        'image': ['nebula galaxy', 'earth from orbit', 'rocket launchpad'],
        'audio': ['rocket launch rumble', 'space radio static beep'],
    },
    'ocean_nature': {
        'video': ['ocean waves', 'underwater coral reef', 'coastline cliffs aerial'],
        'image': ['ocean waves aerial', 'coral reef underwater', 'sea cliffs coast'],
        'audio': ['ocean waves shore', 'underwater ambience'],
    },
    'weather_disasters': {
        'video': ['storm clouds timelapse', 'hurricane storm', 'lightning storm night'],
        'image': ['storm supercell clouds', 'lightning strike', 'flood street aftermath'],
        'audio': ['thunder storm rain', 'wind howling storm'],
    },
    'wildlife_animals': {
        'video': ['wildlife birds flock', 'deer forest wildlife', 'lions savanna wildlife'],
        'image': ['birds wildlife nature', 'deer forest', 'elephant savanna'],
        'audio': ['birdsong forest morning', 'wolves howling night'],
    },
    'world_cities': {
        'video': ['city skyline timelapse', 'street traffic night city', 'european old town street'],
        'image': ['city skyline night', 'old town europe street', 'market street world'],
        'audio': ['city traffic ambience', 'subway station ambience'],
    },
    'japan': {
        'video': ['japan street tokyo', 'kyoto temple japan', 'japan rural train'],
        'image': ['kyoto temple', 'tokyo neon street night', 'mount fuji landscape'],
        'audio': ['japanese temple bell', 'tokyo street ambience'],
    },
    'vintage_ads_cartoons': {
        'video': ['television commercial', 'animated cartoon', 'advertising film'],
        'image': ['vintage advertisement poster', 'retro product label'],
        'audio': ['vintage radio jingle', 'old advertisement music'],
        'ia_collections': ['classic_cartoons', 'Classic_TV_Commercials', 'prelinger'],
    },
    'pd_feature_films': {
        'video': ['feature film', 'film noir', 'western film', 'silent film'],
        'image': ['movie poster vintage', 'cinema theater marquee'],
        'audio': ['film projector running'],
        'ia_collections': ['feature_films', 'film_noir', 'silent_films'],
    },
    'war_history': {
        'video': ['world war newsreel', 'military training film', 'aircraft carrier wartime'],
        'image': ['tanks military ww2', 'warplanes formation', 'battleship guns'],
        'audio': ['artillery distant rumble', 'air raid siren'],
    },
    'science_tech': {
        'video': ['data center corridor', 'server rack lights close up', 'network cables bundle', 'algorithm code screen scrolling', 'forensic technician gloves', 'dna test tubes rack', 'crime lab analysis', 'file cabinet drawer', 'vintage computer technology', 'electronics circuit assembly', 'industrial robot machine', 'forensic lab technician', 'microscope examination lab', 'dna sequencing machine', 'evidence testing laboratory'],
        'image': ['circuit board macro', 'vintage computer mainframe', 'telescope observatory', 'forensic laboratory bench', 'microscope slide close up'],
        'audio': ['computer beeps retro', 'machine hum electronics'],
    },
    'landscapes_timelapse': {
        'video': ['timelapse clouds mountains', 'sunset timelapse', 'desert canyon aerial'],
        'image': ['mountain landscape peaks', 'desert dunes', 'waterfall forest'],
        'audio': ['mountain wind ambience', 'river stream flowing'],
    },
    'textures_backgrounds': {
        'video': ['ink in water', 'smoke background dark', 'bokeh lights abstract'],
        'image': ['old paper texture', 'grunge wall texture', 'marble stone texture'],
        'audio': [],
    },
    'music_performance_pd_era': {
        'video': ['orchestra performance', 'jazz band 1940s', 'concert hall music'],
        'image': ['orchestra vintage', 'gramophone record player', 'concert hall interior'],
        'audio': ['vinyl crackle 78rpm', 'vintage orchestra recording'],
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


# Archival sources hold irreplaceable material that modern-stock floors would delete:
# 1940s telecine derivatives are often 240-360p and PD features run past 30 minutes.
# Their floors are looser, and sub-SD-but-unique footage is QUARANTINED for owner
# review rather than destroyed (live finding: the 480p floor deleted "NUREMBERG AND
# MAUTHAUSEN" at 240p, the 30-min cap deleted "Cross Examination" (1932) at 62 min).
ARCHIVAL_SOURCES = {"ia", "loc", "nara", "nasa", "wikimedia", "noaa", "nypl",
                    "smithsonian", "met"}


def validate_media(path: str, kind: str, theme: str,
                   source: str = "") -> tuple[str, str]:
    """Technical floors (owner vetting layer). Returns (verdict, reason) where
    verdict is "ok" | "reject" | "quarantine".

    video  : decodes, >=5s; height >=480 (stock) / >=360 (archival), 240-359p
             archival -> quarantine; max 30min (stock) / 120min (archival),
             `pd_feature_films` exempt from the maximum entirely
    audio  : decodes, >=1s, >=128kbps or lossless codec
    image  : decodes, long edge >=1200px (>=1920px for textures_backgrounds)"""
    archival = source in ARCHIVAL_SOURCES
    try:
        if os.path.getsize(path) < MIN_ITEM_BYTES:
            return "reject", "too-small-file"
        if kind in ("video", "audio"):
            info = ffprobe_json(path)
            fmt = info.get("format", {})
            dur = float(fmt.get("duration", 0) or 0)
            if kind == "video":
                heights = [int(s.get("height", 0) or 0) for s in info.get("streams", [])
                           if s.get("codec_type") == "video"]
                h = max(heights) if heights else 0
                if h <= 0:
                    return "reject", "no-video-stream"
                # ARCHIVAL: an item that already passed the relevance gate is
                # irreplaceable -- it is NEVER deleted for a quality floor, only
                # quarantined for owner review. (2026-07-28 regression: this was
                # first written as a 360-479p quarantine BAND, so <360p fell through
                # to the reject above and destroyed 7 items incl. the Nuremberg /
                # Mauthausen reel and the German doctors' trial. A band is not a
                # floor -- there must be no delete path below the quarantine range.)
                if archival:
                    if h < 480:
                        return "quarantine", f"archival-sub-sd({h}p)"
                    if dur < 5:
                        return "quarantine", f"archival-very-short({dur:.1f}s)"
                    max_s = 7200 if theme != "pd_feature_films" else 0
                    if max_s and dur > max_s:
                        return "quarantine", f"archival-very-long({dur/60:.0f}min)"
                    return "ok", "ok"
                if h < 480:
                    return "reject", f"video-below-480p({h})"
                if dur < 5:
                    return "reject", f"video-too-short({dur:.1f}s)"
                if dur > 1800:
                    return "reject", f"video-too-long({dur/60:.0f}min)"
            else:
                if dur < 1:
                    return "reject", "audio-too-short"
                br = int(fmt.get("bit_rate", 0) or 0)
                codecs = [s.get("codec_name", "") for s in info.get("streams", [])
                          if s.get("codec_type") == "audio"]
                lossless = any(c.startswith(("pcm", "flac", "alac")) for c in codecs)
                if not lossless and br and br < 128000:
                    return "reject", f"audio-below-128k({br})"
            return "ok", "ok"
        if kind == "image":
            from PIL import Image
            with Image.open(path) as im:
                im.verify()
            with Image.open(path) as im:
                long_edge = max(im.size)
            floor = 1920 if theme == "textures_backgrounds" else 1200
            if long_edge < floor:
                return "reject", f"image-below-{floor}px({long_edge})"
            return "ok", "ok"
        return "ok", "ok"
    except Exception as e:  # noqa: BLE001
        return "reject", f"decode-fail:{e.__class__.__name__}"


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
        self.shelf_shas: set[str] = set()    # only items physically on the archive shelf
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
            if not fn.endswith(".jsonl") or fn.startswith("rejects") or fn.endswith(
                    ("_dedup_removed.jsonl", "_candidates.jsonl")):
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
                    # budgets/themes/retro-sweep count ONLY items that live on the
                    # archive shelf itself — catalog ledgers of PRE-EXISTING holdings
                    # (e.g. factory.jsonl written by the dedup-index agent) still feed
                    # the dedup sets above but must not pollute accounting.
                    fp = str(rec.get("file_path", ""))
                    roots = [t["root"] for t in TIERS] + [QUARANTINE]
                    if not any(fp.lower().startswith(r.lower()) for r in roots):
                        continue
                    if rec.get("sha256"):
                        self.shelf_shas.add(rec["sha256"])
                    b = int(rec.get("bytes", 0))
                    t = rec.get("theme", "?")
                    self.theme_bytes[t] = self.theme_bytes.get(t, 0) + b
                    self.theme_items[t] = self.theme_items.get(t, 0) + 1
                    self.total_bytes += b
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
        # source IDs: flat "source_ids" ({"src:id": path} / list) OR nested
        # "ids" ({"pexels": [id,...] | {id: path}}) — the dedup-index agent uses "ids"
        sid = idx.get("source_ids", {})
        self.existing_ids = {k.lower() for k in (sid if isinstance(sid, list) else sid.keys())}
        for src, ids in (idx.get("ids", {}) or {}).items():
            ids = ids if isinstance(ids, (list, set)) else ids.keys()
            self.existing_ids |= {f"{src}:{i}".lower() for i in ids}
        log(f"existing-holdings index loaded: {len(self.existing_shas)} shas, "
            f"{len(self.existing_ids)} source-ids")
        retro = self.shelf_shas & self.existing_shas
        if retro:
            log(f"RETRO SWEEP: {len(retro)} already-ingested shelf items collide with "
                f"existing holdings (summary + sample in rejects.jsonl; files kept)")
            reject_log("retro", f"{len(retro)}-collisions", "-",
                       "dup_existing_retro_sha_summary",
                       matched=sorted(retro)[:20])  # sample, never 10k+ spam lines

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

    def claimed_by_other_process(self, source: str, sha: str, item_id: str) -> bool:
        """Re-read THIS source's ledger right before recording, to catch an item a
        CONCURRENT process ingested since we loaded ours.

        Each process holds its own in-memory dedup sets, so two lanes running the
        same source both pass the sha check and both write (2026-07-28: two recovery
        processes each downloaded "Big Picture: Military Justice", 122MB twice).
        Re-reading only the source's own ledger is cheap and closes the window."""
        path = os.path.join(LEDGER_DIR, f"{source}.jsonl")
        try:
            for line in open(path, encoding="utf-8", errors="replace"):
                try:
                    other = json.loads(line)
                except Exception:
                    continue
                if other.get("sha256") == sha or str(other.get("id")) == str(item_id):
                    return True
        except OSError:
            return False
        return False

    def record(self, rec: dict) -> None:
        self.done.add((rec["source"], str(rec["id"])))
        self.shas.add(rec["sha256"])
        self.shelf_shas.add(rec["sha256"])
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
        # atomic single-write append: ledgers are shared across concurrently
        # running lanes/processes, same torn-line risk that hit rejects.jsonl
        atomic_append(os.path.join(LEDGER_DIR, f"{rec['source']}.jsonl"),
                      json.dumps(rec, ensure_ascii=False))


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
    if theme_source_unusable(theme, source):
        reject_log(source, item_id, theme, "owner-verdict-unusable", title=title)
        return False
    if is_meeting_recording(title):
        reject_log(source, item_id, theme, "meeting-recording", title=title)
        return False
    ACTIVITY += 1
    if f"{source}:{item_id}".lower() in ledger.existing_ids:
        reject_log(source, item_id, theme, "dup_existing_id", title=title)
        return False
    if PERSON_RE.search(title or ""):
        reject_log(source, item_id, theme, "person-filter", title=title)
        return False
    # per-item metadata relevance gate (owner: no blind query-dumps)
    score, matched, negs, title_ok = relevance(theme, title, desc)
    threshold = SRC_THRESHOLD.get(source, DEFAULT_THRESHOLD)
    if score < threshold:
        reject_log(source, item_id, theme, f"relevance<{threshold}", score, matched, negs,
                   title=title)
        return False
    if not title_ok:  # title-relevance gate — description-only matches are boilerplate
        reject_log(source, item_id, theme, "title-irrelevant", score, matched, negs,
                   title=title)
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
        reject_log(source, item_id, theme, f"download-fail:{e.__class__.__name__}", score,
                   title=title)
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
        reject_log(source, item_id, theme, "dup-sha256", score, title=title)
        return False
    if sha in ledger.existing_shas:  # content already in factory/stock holdings
        log(f"  dup-existing-sha, removed: {fname[:70]}")
        os.remove(dest)
        reject_log(source, item_id, theme, "dup_existing_sha", score, title=title)
        return False
    if ledger.claimed_by_other_process(source, sha, item_id):
        log(f"  dup-concurrent-process, removed: {fname[:70]}")
        os.remove(dest)
        reject_log(source, item_id, theme, "dup_concurrent_process", score, title=title)
        return False
    verdict, why = validate_media(dest, kind, theme, source)
    if verdict == "reject":
        log(f"  reject ({why}), removed: {fname[:70]}")
        os.remove(dest)
        reject_log(source, item_id, theme, f"tech:{why}", score, title=title)
        return False
    quarantine_reason = ""
    if verdict == "quarantine":
        # irreplaceable archival material below the modern floor: keep it, but for
        # owner review only — never silently into the main shelf, never deleted
        qroot = os.path.join(QUARANTINE, theme)
        os.makedirs(qroot, exist_ok=True)
        qdest = os.path.join(qroot, os.path.basename(dest))
        # Cross-device move: the shelf lives on D:/E:/F: but quarantine is ALWAYS on H:
        # (CONTRACT 1), and os.replace cannot cross a Windows volume — it raises
        # OSError 18 (EXDEV). That killed the whole source: the noaa lane died on its
        # first sub-floor TIF and stayed dead for 18 hours while its siblings ran on.
        shutil.move(dest, qdest)
        dest, decision, quarantine_reason = qdest, "review_required", why
        log(f"  quarantined ({why}): {fname[:66]}")
    ledger.record({
        "id": str(item_id), "source": source, "source_url": source_url, "title": title,
        "license_field_raw": license_raw[:500], "license_decision": decision,
        "theme": theme, "file_path": dest, "bytes": nbytes, "sha256": sha,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "relevance_score": score, "matched_keywords": matched[:12],
        **({"quarantine_reason": quarantine_reason} if quarantine_reason else {}),
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
                reject_log("ia", ident, theme, "period-no-date-provenance",
                           title=str(meta.get("title", ident)))
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


def selftest_floors() -> int:
    """Prove the technical-floor policy from the code itself. Run before/after any
    floor edit: `--selftest`. Exists because the archival quarantine was first
    written as a 360-479p BAND while <360p still deleted -- the spec and the code
    disagreed and 7 irreplaceable items were destroyed before anyone measured it."""
    cases = [  # (name, height, dur_s, source, expected_verdict)
        ("archival 144p", 144, 600, "ia", "quarantine"),
        ("archival 240p", 240, 600, "ia", "quarantine"),
        ("archival 360p", 360, 600, "ia", "quarantine"),
        ("archival 480p", 480, 600, "ia", "ok"),
        ("archival 62min", 480, 3720, "ia", "ok"),
        ("archival 3h", 480, 10800, "ia", "quarantine"),
        ("archival 2s", 480, 2, "ia", "quarantine"),
        ("stock 240p", 240, 600, "mixkit", "reject"),
        ("stock 480p", 480, 600, "mixkit", "ok"),
        ("stock 45min", 480, 2700, "mixkit", "reject"),
    ]
    global ffprobe_json
    orig_probe, orig_size = ffprobe_json, os.path.getsize
    fails = 0
    for name, h, d, src, want in cases:
        ffprobe_json = (lambda p, _h=h, _d=d: {
            "streams": [{"codec_type": "video", "height": _h}],
            "format": {"duration": _d}})
        os.path.getsize = lambda p: 10 ** 7  # type: ignore[assignment]
        got, why = validate_media("x.mp4", "video", "courtroom_justice", src)
        ok = got == want
        fails += not ok
        log(f"  {'PASS' if ok else 'FAIL'} {name:16} -> {got:10} ({why})")
    ffprobe_json = orig_probe
    os.path.getsize = orig_size  # type: ignore[assignment]
    # the invariant that actually matters: archival video never has a delete path
    log("SELFTEST: " + ("ALL PASS" if not fails else f"{fails} FAILED"))
    return 1 if fails else 0


def code_fingerprint() -> str:
    """mtime + hash of this file, logged at startup so a STALE PROCESS running
    pre-fix code is detectable from its own log (2026-07-28: a run launched before
    a floor fix kept deleting archival items for 40 minutes while the fixed code
    sat on disk -- nothing in its log revealed which version it was executing)."""
    path = os.path.abspath(__file__)
    try:
        raw = open(path, "rb").read()
        return (f"{os.path.basename(path)} mtime="
                f"{datetime.fromtimestamp(os.path.getmtime(path)).strftime('%m-%d %H:%M:%S')} "
                f"sha1={hashlib.sha1(raw).hexdigest()[:12]}")
    except OSError:
        return "unknown"


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
    ap.add_argument("--selftest", action="store_true",
                    help="prove the technical-floor policy and exit")
    args = ap.parse_args()
    if args.selftest:
        return selftest_floors()
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
    log(f"CODE: {code_fingerprint()}")   # stale-process detector
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
