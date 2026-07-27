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
import sys
import urllib.parse
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)

import ingest_archive_sources as base  # noqa: E402  shared plumbing (see docstring)

REPO = base.REPO
GB = base.GB
LEDGER_DIR = base.LEDGER_DIR
QUARANTINE = base.QUARANTINE
NET = base.NET
log = base.log

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
VIDEO_THEMES = ["ocean_nature", "wildlife_animals", "world_cities", "japan",
                "landscapes_timelapse", "textures_backgrounds", "science_tech",
                "small_town", "money_banking", "police_modern"]

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

for _t, _q in AUDIO_THEMES.items():
    base.THEMES.setdefault(_t, {"video": [], "image": [], "audio": _q["audio"]})
base.SRC_THRESHOLD.setdefault("pixabay_extra", 20)
base.HOST_INTERVAL.setdefault("pixabay.com", 1.0)
base.HOST_INTERVAL.setdefault("api.unsplash.com", 1.0)
base.HOST_INTERVAL.setdefault("freesound.org", 1.0)

ALL_THEMES = VIDEO_THEMES + list(AUDIO_THEMES)
PASS = 1  # pass N == page N of each paginated source (set by main loop)


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
              usage_tag: str | None = None, desc: str = "",
              dl_headers: dict | None = None) -> bool:
    """Vet -> download -> validate -> ledger (this lane's contract schema).
    Mirrors the sibling take() flow but writes matched_keywords/usage_tag and
    routes storage to D: only. Returns True if ingested."""
    if ledger.seen(source, item_id):
        return False
    if base.PERSON_RE.search(title or ""):
        base.reject_log(source, item_id, theme, "person-filter")
        return False
    score, matched, negs = base.relevance(theme, f"{title} {desc}")
    threshold = base.SRC_THRESHOLD.get(source, base.DEFAULT_THRESHOLD)
    if score < threshold:
        base.reject_log(source, item_id, theme, f"relevance<{threshold}",
                        score, matched, negs)
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
                        f"download-fail:{e.__class__.__name__}", score)
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
        base.reject_log(source, item_id, theme, "dup-sha256", score)
        return False
    ok, why = base.validate_media(dest, kind, theme)
    if not ok:
        log(f"  reject ({why}), removed: {fname[:70]}")
        os.remove(dest)
        base.reject_log(source, item_id, theme, f"tech:{why}", score)
        return False
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
                base.reject_log("mixkit", vid, theme, f"license-not-free:{lic[:80]}")
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
                base.reject_log("pixabay_extra", f"v_{vid}", theme, "dup-source-id")
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
                base.reject_log("pixabay_extra", f"i_{pid}", theme, "dup-source-id")
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
            fs_desc = (f"{snd.get('description', '')} "
                       f"{' '.join(snd.get('tags', []) or [])}")[:600]
            if take_item(ledger, source="freesound", item_id=sid,
                         title=snd.get("name", ""), source_url=snd.get("url", ""),
                         download_url=url, kind="audio", theme=theme,
                         license_raw=lic, decision="cc0", default_ext="mp3",
                         dry_run=dry_run, usage_tag=USAGE_TAG[theme], desc=fs_desc):
                got += 1
    return got


ADAPTERS = {"mixkit": src_mixkit, "coverr": src_coverr,
            "pixabay_extra": src_pixabay_extra,
            "unsplash": src_unsplash, "freesound": src_freesound}
SOURCE_ORDER = ["mixkit", "coverr", "pixabay_extra", "unsplash", "freesound"]


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
    args = ap.parse_args()

    base.load_env()
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
