# -*- coding: utf-8 -*-
"""Retrofit the existing factory/ + stock/ shelves into the archive ledger system.

ADDITIVE ONLY — never renames, moves, or modifies original files. Outputs:

  1. H:\\pd-media\\assets\\archive\\_ledger\\factory.jsonl   (CONTRACT.md schema)
  2. H:\\pd-media\\assets\\archive\\_ledger\\stock.jsonl     (CONTRACT.md schema)
  3. D:\\pd-media-browse\\factory_browse\\<theme>\\<source>__<id>__<title-slug>.<ext>
     D:\\pd-media-browse\\stock_browse\\<theme>\\...
     (NTFS symlinks -> H: originals, zero copies. H: itself is exFAT and supports
      neither hardlinks nor symlinks, so the browse tree cannot live on H:.
      Pointer note: H:\\pd-media\\assets\\FACTORY_BROWSE_LOCATION.txt)
  4. H:\\pd-media\\assets\\archive\\_ledger\\factory_backfill_queue.json
     (deliberately .json, NOT .jsonl: ingest agents load every *.jsonl in _ledger
      and would crash on records without source/id keys)

Metadata sources, in order:
  a. assets/asset_manifest.v001.json  — covers ALL 88,740 factory files (source,
     _srcId, sourceUrl, license, sha256, bytes). Titles derived from the sourceUrl
     slug (real provider titles). ~34 slugless URLs queued for API backfill.
  b. H:\\pd-media\\assets\\stock\\STOCK_MANIFEST.json — 20 of 234 stock files.
     The other 214 embed provider ids in the filename (pexels_i_123.jpg) and are
     queued for API backfill (title/canonical URL).
  c. `backfill` subcommand — Pexels (paced ~20 s/req, limit ~200/hr) and Pixabay
     (paced 0.7 s/req) lookups for the queue only. Resumable; 404 => marked gone.

Theme correction (the evidence_bag=cartoon incident): the ledger records BOTH
`original_dir_theme` (derived from the shelf subtype via scripts/factory_themes.py)
and the corrected `theme`. Corrected = theme derived from the REAL provider title
when it matches a theme rule; else the subtype theme with theme_source
"subtype_unverified". Browse view uses the corrected theme. Originals never move.

relevance_score (retrofit semantics): min(60, 20 + 15 * len(matched_keywords)),
where matched_keywords = tokens shared between the ingest query (subtype) and the
real provider title. 20 = curated-stock-search floor per CONTRACT.md §4.

Usage:
  python scripts/retrofit_factory_ledger.py smoke                 # 50-file end-to-end
  python scripts/retrofit_factory_ledger.py build                 # both ledgers + queue
  python scripts/retrofit_factory_ledger.py link                  # browse hardlinks (idempotent)
  python scripts/retrofit_factory_ledger.py backfill [--max-requests N]
  python scripts/retrofit_factory_ledger.py verify [--sample 50]
  python scripts/retrofit_factory_ledger.py stats
Nightly resume (safe to re-run any time):
  python scripts/retrofit_factory_ledger.py backfill && python scripts/retrofit_factory_ledger.py link
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.request
import urllib.error

REPO = r"C:\Users\aab15\Documents\prime-documentary"
ASSETS_ROOT = r"H:\pd-media\assets"
FACTORY_ROOT = os.path.join(ASSETS_ROOT, "factory")
STOCK_ROOT = os.path.join(ASSETS_ROOT, "stock")
LEDGER_DIR = os.path.join(ASSETS_ROOT, "archive", "_ledger")
FACTORY_LEDGER = os.path.join(LEDGER_DIR, "factory.jsonl")
STOCK_LEDGER = os.path.join(LEDGER_DIR, "stock.jsonl")
QUEUE_PATH = os.path.join(LEDGER_DIR, "factory_backfill_queue.json")
LOG_PATH = os.path.join(LEDGER_DIR, "retrofit_factory.log")
# H: is exFAT — it supports neither hardlinks nor symlinks (both verified 2026-07-27:
# os.link/os.symlink => WinError 1). The browse tree therefore lives on D: (NTFS) as
# SYMLINKS to the H: originals: zero data duplication, transparent to Explorer/tools.
# A pointer file is left at H:\pd-media\assets\FACTORY_BROWSE_LOCATION.txt.
BROWSE_ROOT = r"D:\pd-media-browse"
BROWSE = {"factory": os.path.join(BROWSE_ROOT, "factory_browse"),
          "stock": os.path.join(BROWSE_ROOT, "stock_browse")}
BROWSE_POINTER = os.path.join(ASSETS_ROOT, "FACTORY_BROWSE_LOCATION.txt")
STATE_PATH = {"factory": os.path.join(LEDGER_DIR, "factory_browse_state.json"),
              "stock": os.path.join(LEDGER_DIR, "stock_browse_state.json")}
MANIFEST = os.path.join(REPO, "assets", "asset_manifest.v001.json")
STOCK_MANIFEST = os.path.join(STOCK_ROOT, "STOCK_MANIFEST.json")

sys.path.insert(0, os.path.join(REPO, "scripts"))
from factory_themes import RULES, theme_of  # noqa: E402

_STOP = {"the", "and", "with", "for", "from", "into", "over", "under", "near",
         "close", "up", "shot", "view", "photo", "video", "background", "dark",
         "black", "white", "blue", "red", "old", "macro"}


def log(msg: str) -> None:
    line = f"{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {msg}"
    print(line, flush=True)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def load_env_keys() -> dict:
    keys = {}
    p = os.path.join(REPO, ".env")
    if os.path.isfile(p):
        for line in open(p, encoding="utf-8", errors="replace"):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                keys[k.strip()] = v.strip().strip('"').strip("'")
    return keys


def slugify(text: str, max_len: int = 70) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    if len(s) > max_len:
        s = s[:max_len].rsplit("-", 1)[0] or s[:max_len]
    return s or "untitled"


def title_from_url(url: str | None) -> str | None:
    """Real provider title from a Pexels/Pixabay canonical URL slug."""
    if not url:
        return None
    m = re.search(r"/(?:photo|video|photos|videos|illustrations|vectors)/"
                  r"([^/]*?[a-z][^/]*?)-(\d+)/?$", url)
    if m:
        return m.group(1).replace("-", " ")
    return None


def theme_from_text(text: str | None) -> str | None:
    """Apply the factory_themes RULES to free text (title/depicts)."""
    if not text:
        return None
    norm = "_" + re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_") + "_"
    for kw, theme in RULES:
        if kw in norm:
            return theme
    return None


def tokens(text: str | None) -> set:
    return {t for t in re.split(r"[^a-z0-9]+", (text or "").lower())
            if len(t) > 2 and t not in _STOP}


def relevance(subtype: str | None, title: str | None) -> tuple[int, list]:
    matched = sorted(tokens(subtype) & tokens(title))
    return min(60, 20 + 15 * len(matched)), matched


def iso_mtime(path: str) -> str:
    try:
        ts = os.path.getmtime(path)
    except OSError:
        ts = time.time()
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def atomic_write(path: str, data: str) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(data)
    os.replace(tmp, path)


def write_jsonl(path: str, records: list) -> None:
    atomic_write(path, "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))


def read_jsonl(path: str) -> list:
    if not os.path.isfile(path):
        return []
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


# ---------------------------------------------------------------- factory build

def build_factory(limit: int = 0) -> tuple[list, list]:
    man = json.load(open(MANIFEST, encoding="utf-8"))["assets"]
    records, queue, skipped = [], [], 0
    for r in man:
        rel = r["path"].replace("/", "\\")
        if rel.startswith("artifact:") or not rel.lower().startswith("factory\\"):
            skipped += 1
            continue
        fp = os.path.join(ASSETS_ROOT, rel)
        category = r.get("type") or rel.split("\\")[1]
        subtype = r.get("subtype") or ""
        source = r.get("source") or "unknown"
        src_id_raw = r.get("_srcId") or ""
        m = re.match(r"^(?:pexels|pixabay)_[iv]_(\d+)$", src_id_raw)
        native_id = m.group(1) if m else r["id"]  # generated: manifest id is native
        url = r.get("sourceUrl") or ""
        kind = r.get("kind") or "image"
        title = title_from_url(url)
        pending = False
        if title:
            provenance = "source_url_slug"
        elif r.get("sourcePrompt"):
            title = r["sourcePrompt"]
            provenance = "prompt" if source in ("sdxl", "local_a1111") else "query_fallback"
            pending = source in ("pexels", "pixabay")
        else:
            title, provenance, pending = "untitled", "none", source in ("pexels", "pixabay")
        original_theme = theme_of(subtype, category)
        if category == "backgrounds":
            t_theme = theme_from_text(title) if provenance in ("source_url_slug", "prompt") else None
            theme = t_theme or original_theme
            theme_source = "title" if t_theme else "subtype_unverified"
        else:
            theme, theme_source = original_theme, "category"
        score, matched = relevance(subtype, title if provenance == "source_url_slug" else None)
        sha = (r.get("sha256") or "").removeprefix("sha256:")
        lic = r.get("license") or ""
        decision = ("free_commercial" if lic in ("Pexels License", "Pixabay Content License")
                    else "free_commercial" if lic == "generated_owned" else "review_required")
        rec = {
            "id": str(native_id), "source": source, "source_url": url, "title": title,
            "license_field_raw": lic, "license_decision": decision, "theme": theme,
            "file_path": fp, "bytes": int(r.get("bytes") or 0), "sha256": sha,
            "fetched_at": iso_mtime(fp), "relevance_score": score,
            "matched_keywords": matched,
            # extra fields (allowed by CONTRACT.md; do not rename the core ones)
            "ledger": "factory", "manifest_id": r["id"], "category": category,
            "subtype": subtype, "kind": kind, "original_dir_theme": original_theme,
            "theme_source": theme_source, "title_provenance": provenance,
            "backfill_pending": pending,
        }
        records.append(rec)
        if pending:
            queue.append({"ledger": "factory", "key": r["id"], "source": source,
                          "kind": kind, "native_id": str(native_id), "status": "pending"})
        if limit and len(records) >= limit:
            break
    log(f"factory build: {len(records)} records ({skipped} non-shelf manifest rows skipped), "
        f"{len(queue)} queued for API title backfill")
    return records, queue


# ------------------------------------------------------------------ stock build

_HOST_SOURCE = [("pexels.com", "pexels"), ("pixabay.com", "pixabay"),
                ("wikimedia.org", "wikimedia"), ("oyez", "oyez"),
                ("amazonaws.com", "oyez")]


def build_stock(limit: int = 0) -> tuple[list, list]:
    sman = json.load(open(STOCK_MANIFEST, encoding="utf-8")) if os.path.isfile(STOCK_MANIFEST) else []
    by_rel = {}
    for x in sman:
        rel = x["file"].replace("/", "\\")
        rel = rel[len("assets\\"):] if rel.lower().startswith("assets\\") else rel
        by_rel[rel.lower()] = x
    records, queue = [], []
    for dp, _dn, fn in os.walk(STOCK_ROOT):
        for f in sorted(fn):
            if f.lower() == "stock_manifest.json":
                continue
            fp = os.path.join(dp, f)
            rel = os.path.relpath(fp, ASSETS_ROOT)  # stock\images\x.jpg
            man = by_rel.get(rel.lower())
            stem, ext = os.path.splitext(f)
            kind = {"images": "image", "video": "video", "audio": "audio"}.get(
                rel.split("\\")[1] if "\\" in rel else "", "image")
            fm = re.match(r"^(pexels|pixabay)_([iv])_(\d+)$", stem)
            if man:
                url = man.get("source_url") or ""
                source = next((s for h, s in _HOST_SOURCE if h in url), "unknown")
                native_id = None
                mm = re.search(r"(?:pexels-photo-|photos/|videos/)(\d+)", url)
                if mm:
                    native_id = mm.group(1)
                title = man.get("depicts") or stem.replace("_", " ")
                lic = man.get("license") or ""
                ll = lic.lower()
                decision = ("cc0" if "cc0" in ll else
                            "pd" if "public domain" in ll else
                            "free_commercial" if source in ("pexels", "pixabay") else
                            "review_required")
                theme = theme_from_text(title) or theme_from_text(stem) or ("audio" if kind == "audio" else "misc")
                score, matched = relevance(stem, title)
                rec_id = str(native_id or stem)
                sha = (man.get("sha256") or "").removeprefix("sha256:")
                bts = int(man.get("bytes") or os.path.getsize(fp))
                provenance, pending = "stock_manifest_depicts", False
                attribution = man.get("attribution") or ""
            elif fm:
                source = fm.group(1)
                kind = "video" if fm.group(2) == "v" else kind
                rec_id, url, title = fm.group(3), "", "untitled"
                lic = ("Pexels License (inferred from filename provenance; API backfill pending)"
                       if source == "pexels" else
                       "Pixabay Content License (inferred from filename provenance; API backfill pending)")
                decision = "free_commercial"
                theme, provenance, pending = "misc", "none", True
                score, matched = 20, []
                sha = sha256_file(fp)
                bts = os.path.getsize(fp)
                attribution = ""
            else:
                source, rec_id, url = "unknown", stem, ""
                title = stem.replace("_", " ")
                lic, decision = "(no provenance record found; retrofit)", "review_required"
                theme = theme_from_text(title) or ("audio" if kind == "audio" else "misc")
                provenance, pending = "filename", False
                score, matched = 20, []
                sha = sha256_file(fp)
                bts = os.path.getsize(fp)
                attribution = ""
            rec = {
                "id": rec_id, "source": source, "source_url": url, "title": title,
                "license_field_raw": lic, "license_decision": decision, "theme": theme,
                "file_path": fp, "bytes": bts, "sha256": sha,
                "fetched_at": iso_mtime(fp), "relevance_score": score,
                "matched_keywords": matched,
                "ledger": "stock", "manifest_id": rel, "category": "stock",
                "subtype": stem, "kind": kind, "original_dir_theme": theme,
                "theme_source": "title" if provenance != "none" else "pending",
                "title_provenance": provenance, "backfill_pending": pending,
                "attribution": attribution,
            }
            records.append(rec)
            if pending:
                queue.append({"ledger": "stock", "key": rel, "source": source,
                              "kind": kind, "native_id": rec_id, "status": "pending"})
            if limit and len(records) >= limit:
                log(f"stock build (limited): {len(records)} records")
                return records, queue
    log(f"stock build: {len(records)} records, {len(queue)} queued for API backfill")
    return records, queue


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ----------------------------------------------------------------- browse links

def link_name(rec: dict) -> str:
    ext = os.path.splitext(rec["file_path"])[1].lower()
    title = rec["title"] if not rec.get("backfill_pending") else "untitled"
    return f"{rec['source']}__{rec['id']}__{slugify(title)}{ext}"


_LINK_MODE = {"mode": None}  # "hardlink" | "symlink", decided on first success


def make_link(src: str, dst: str) -> bool:
    """Create dst as a hardlink (preferred) or symlink to src. True if created."""
    if _LINK_MODE["mode"] in (None, "hardlink"):
        try:
            os.link(src, dst)
            _LINK_MODE["mode"] = "hardlink"
            return True
        except OSError:
            if _LINK_MODE["mode"] == "hardlink":
                raise
    os.symlink(src, dst)
    _LINK_MODE["mode"] = "symlink"
    return True


def cmd_link(which: list, limit: int = 0) -> None:
    try:
        if not os.path.isfile(BROWSE_POINTER):
            with open(BROWSE_POINTER, "w", encoding="utf-8") as f:
                f.write("The factory/stock browse view (readable-named links, organized by theme)\n"
                        f"lives at {BROWSE_ROOT}\\ .\n"
                        "It is NOT on H: because H: is exFAT, which supports no hardlinks/symlinks.\n"
                        "The links are NTFS symlinks pointing back to the originals on H: (zero copies).\n"
                        "Rebuild any time: python scripts/retrofit_factory_ledger.py link\n")
    except OSError:
        pass
    for name in which:
        ledger_path = FACTORY_LEDGER if name == "factory" else STOCK_LEDGER
        records = read_jsonl(ledger_path)
        if limit:
            records = records[:limit]
        if not records:
            log(f"link[{name}]: ledger empty/missing, skip")
            continue
        state = {}
        if os.path.isfile(STATE_PATH[name]):
            state = json.load(open(STATE_PATH[name], encoding="utf-8"))
        browse = BROWSE[name]
        os.makedirs(browse, exist_ok=True)
        created = kept = renamed = missing = errors = 0
        for i, rec in enumerate(records):
            src = rec["file_path"]
            key = rec.get("manifest_id") or f"{rec['source']}:{rec['id']}"
            if not os.path.isfile(src):
                missing += 1
                continue
            tdir = os.path.join(browse, rec["theme"])
            os.makedirs(tdir, exist_ok=True)
            base = link_name(rec)
            desired = os.path.join(tdir, base)
            old = state.get(key)
            if old and os.path.normcase(old) != os.path.normcase(desired):
                # title/theme changed since last run (e.g. backfill landed): re-link
                try:
                    if os.path.isfile(old) and os.path.samefile(old, src):
                        os.unlink(old)
                        renamed += 1
                except OSError:
                    pass
            final = None
            stem, ext = os.path.splitext(desired)
            for n in range(1, 30):
                cand = desired if n == 1 else f"{stem}-{n}{ext}"
                if os.path.lexists(cand):
                    try:
                        if os.path.samefile(cand, src):
                            final = cand
                            kept += 1
                            break
                    except OSError:
                        pass
                    continue  # name taken by another file -> try -n suffix
                try:
                    make_link(src, cand)
                    final = cand
                    created += 1
                except OSError as e:
                    log(f"link[{name}] ERROR {src} -> {cand}: {e}")
                    errors += 1
                    final = None
                break
            if final:
                state[key] = final
            if (i + 1) % 5000 == 0:
                log(f"link[{name}]: {i + 1}/{len(records)} (created {created}, kept {kept})")
                atomic_write(STATE_PATH[name], json.dumps(state))
        atomic_write(STATE_PATH[name], json.dumps(state))
        log(f"link[{name}] DONE mode={_LINK_MODE['mode']}: created {created}, kept {kept}, "
            f"re-linked {renamed}, missing-src {missing}, errors {errors}, total {len(records)}")


# -------------------------------------------------------------------- backfill

def _http_json(url: str, headers: dict) -> tuple[int, dict | None]:
    req = urllib.request.Request(url, headers={
        "User-Agent": "PrimeDocumentaryIngest/1.0 (archival research; contact: aab153792@gmail.com)",
        **headers})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:  # noqa: BLE001
        log(f"backfill http error {url}: {e}")
        return -1, None


def lookup(source: str, kind: str, native_id: str, keys: dict) -> tuple[str, dict | None]:
    """Returns (status, info) — status ok|gone|ratelimited|error."""
    if source == "pexels":
        base = (f"https://api.pexels.com/videos/videos/{native_id}" if kind == "video"
                else f"https://api.pexels.com/v1/photos/{native_id}")
        code, js = _http_json(base, {"Authorization": keys.get("PEXELS_API_KEY", "")})
        if code == 200 and js:
            url = js.get("url") or ""
            title = title_from_url(url) or js.get("alt") or ""
            return "ok", {"url": url, "title": title,
                          "raw": f"Pexels License; photographer={js.get('photographer') or js.get('user', {}).get('name', '')}"}
        if code == 404:
            return "gone", None
        if code == 429:
            return "ratelimited", None
        return "error", None
    if source == "pixabay":
        base = (f"https://pixabay.com/api/videos/?key={keys.get('PIXABAY_API_KEY', '')}&id={native_id}"
                if kind == "video" else
                f"https://pixabay.com/api/?key={keys.get('PIXABAY_API_KEY', '')}&id={native_id}")
        code, js = _http_json(base, {})
        if code == 200 and js:
            hits = js.get("hits") or []
            if not hits:
                return "gone", None
            h = hits[0]
            url = h.get("pageURL") or ""
            title = title_from_url(url) or (h.get("tags") or "").replace(",", " ")
            return "ok", {"url": url, "title": title,
                          "raw": f"Pixabay Content License; tags={h.get('tags', '')}"}
        if code == 404 or code == 400:
            return "gone", None
        if code == 429:
            return "ratelimited", None
        return "error", None
    return "error", None


def cmd_backfill(max_requests: int = 0) -> None:
    if not os.path.isfile(QUEUE_PATH):
        log("backfill: no queue file — run build first")
        return
    queue = json.load(open(QUEUE_PATH, encoding="utf-8"))
    pending = [q for q in queue if q.get("status") == "pending"]
    if not pending:
        log("backfill: queue empty — nothing to do")
        return
    keys = load_env_keys()
    ledgers = {"factory": read_jsonl(FACTORY_LEDGER), "stock": read_jsonl(STOCK_LEDGER)}
    index = {ln: {r.get("manifest_id"): r for r in recs} for ln, recs in ledgers.items()}
    done = 0
    last_pexels = 0.0
    stop = False
    for q in pending:
        if stop or (max_requests and done >= max_requests):
            break
        if q["source"] == "pexels":
            wait = 20.0 - (time.time() - last_pexels)  # ~180/hr < 200/hr Pexels cap
            if wait > 0:
                time.sleep(wait)
            last_pexels = time.time()
        else:
            time.sleep(0.7)  # Pixabay ~100/min cap, stay well under
        status, info = lookup(q["source"], q["kind"], q["native_id"], keys)
        done += 1
        if status == "ratelimited":
            log(f"backfill: {q['source']} rate limited after {done} requests — stopping (resume later)")
            stop = True
            continue
        if status == "error":
            log(f"backfill: transient error {q['source']}:{q['native_id']} — kept pending")
            continue
        rec = index[q["ledger"]].get(q["key"])
        if rec is None:
            q["status"] = "orphan"
            continue
        if status == "gone":
            q["status"] = "gone"
            rec["backfill_pending"] = False
            rec["title_provenance"] = "gone_from_provider"
            continue
        rec["title"] = info["title"] or rec["title"]
        rec["source_url"] = info["url"] or rec["source_url"]
        rec["license_field_raw"] = info["raw"]
        rec["title_provenance"] = "api_backfill"
        rec["backfill_pending"] = False
        t_theme = theme_from_text(rec["title"])
        if t_theme and rec.get("category") in ("backgrounds", "stock"):
            rec["theme"] = t_theme
            rec["theme_source"] = "title"
        rec["relevance_score"], rec["matched_keywords"] = relevance(rec.get("subtype"), rec["title"])
        q["status"] = "done"
        if done % 25 == 0:
            log(f"backfill: {done} requests processed")
            write_jsonl(FACTORY_LEDGER, ledgers["factory"])
            write_jsonl(STOCK_LEDGER, ledgers["stock"])
            atomic_write(QUEUE_PATH, json.dumps(queue, indent=1))
    write_jsonl(FACTORY_LEDGER, ledgers["factory"])
    write_jsonl(STOCK_LEDGER, ledgers["stock"])
    atomic_write(QUEUE_PATH, json.dumps(queue, indent=1))
    left = sum(1 for q in queue if q.get("status") == "pending")
    log(f"backfill DONE this run: {done} requests, {left} still pending. "
        f"Run `link` next to apply real titles to browse names.")


# ------------------------------------------------------------- verify & stats

def cmd_verify(sample: int = 50) -> None:
    rng = random.Random(7)
    for name, path in (("factory", FACTORY_LEDGER), ("stock", STOCK_LEDGER)):
        recs = read_jsonl(path)
        if not recs:
            log(f"verify[{name}]: ledger missing")
            continue
        picks = rng.sample(recs, min(sample, len(recs)))
        ok_sha = bad_sha = ok_link = bad_link = missing = 0
        state = json.load(open(STATE_PATH[name], encoding="utf-8")) if os.path.isfile(STATE_PATH[name]) else {}
        for r in picks:
            fp = r["file_path"]
            if not os.path.isfile(fp):
                missing += 1
                continue
            if r.get("sha256"):
                if sha256_file(fp) == r["sha256"]:
                    ok_sha += 1
                else:
                    bad_sha += 1
                    log(f"verify[{name}] SHA MISMATCH: {fp}")
            key = r.get("manifest_id") or f"{r['source']}:{r['id']}"
            lp = state.get(key)
            if lp and os.path.isfile(lp) and os.path.samefile(lp, fp):
                ok_link += 1
            else:
                bad_link += 1
        log(f"verify[{name}]: sample {len(picks)} — sha ok {ok_sha} / bad {bad_sha}, "
            f"link ok {ok_link} / bad-or-missing {bad_link}, missing files {missing}")


def cmd_stats() -> None:
    for name, path in (("factory", FACTORY_LEDGER), ("stock", STOCK_LEDGER)):
        recs = read_jsonl(path)
        if not recs:
            continue
        themes: dict[str, int] = {}
        prov: dict[str, int] = {}
        corrected = pending = 0
        for r in recs:
            themes[r["theme"]] = themes.get(r["theme"], 0) + 1
            prov[r.get("title_provenance", "?")] = prov.get(r.get("title_provenance", "?"), 0) + 1
            if r.get("theme_source") == "title" and r["theme"] != r.get("original_dir_theme"):
                corrected += 1
            if r.get("backfill_pending"):
                pending += 1
        log(f"stats[{name}]: {len(recs)} records; title provenance {prov}; "
            f"theme corrected vs shelf label: {corrected}; backfill pending: {pending}")
        for t, c in sorted(themes.items(), key=lambda kv: -kv[1]):
            log(f"  theme {t}: {c}")
    if os.path.isfile(QUEUE_PATH):
        queue = json.load(open(QUEUE_PATH, encoding="utf-8"))
        st: dict[str, int] = {}
        for q in queue:
            st[q["status"]] = st.get(q["status"], 0) + 1
        log(f"stats[queue]: {st}")


# ------------------------------------------------------------------------ main

def cmd_build(limit: int = 0, smoke_dir: str | None = None) -> None:
    frecs, fq = build_factory(limit)
    srecs, sq = build_stock(limit if limit else 0)
    if smoke_dir:
        os.makedirs(smoke_dir, exist_ok=True)
        write_jsonl(os.path.join(smoke_dir, "factory.smoke.jsonl"), frecs)
        write_jsonl(os.path.join(smoke_dir, "stock.smoke.jsonl"), srecs)
        log(f"smoke build written to {smoke_dir} (NOT into _ledger)")
        return
    os.makedirs(LEDGER_DIR, exist_ok=True)
    write_jsonl(FACTORY_LEDGER, frecs)
    write_jsonl(STOCK_LEDGER, srecs)
    # Merge queue with any prior statuses (resumable, don't lose done/gone marks)
    prior = {}
    if os.path.isfile(QUEUE_PATH):
        for q in json.load(open(QUEUE_PATH, encoding="utf-8")):
            prior[(q["ledger"], q["key"])] = q["status"]
    queue = fq + sq
    for q in queue:
        q["status"] = prior.get((q["ledger"], q["key"]), q["status"])
    atomic_write(QUEUE_PATH, json.dumps(queue, indent=1))
    log(f"build DONE: factory {len(frecs)}, stock {len(srecs)}, queue {len(queue)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("build")
    p.add_argument("--limit", type=int, default=0)
    p = sub.add_parser("link")
    p.add_argument("--ledger", choices=["factory", "stock", "all"], default="all")
    p.add_argument("--limit", type=int, default=0)
    p = sub.add_parser("backfill")
    p.add_argument("--max-requests", type=int, default=0)
    p = sub.add_parser("verify")
    p.add_argument("--sample", type=int, default=50)
    sub.add_parser("stats")
    sub.add_parser("smoke")
    a = ap.parse_args()
    if a.cmd == "build":
        cmd_build(a.limit)
    elif a.cmd == "link":
        cmd_link(["factory", "stock"] if a.ledger == "all" else [a.ledger], a.limit)
    elif a.cmd == "backfill":
        cmd_backfill(a.max_requests)
    elif a.cmd == "verify":
        cmd_verify(a.sample)
    elif a.cmd == "stats":
        cmd_stats()
    elif a.cmd == "smoke":
        # 50-file end-to-end: ledger rows to a scratch dir, then REAL links for those
        scratch = os.environ.get("RETROFIT_SMOKE_DIR") or os.path.join(
            os.environ.get("TEMP", "."), "retrofit_smoke")
        frecs, _ = build_factory(50)
        os.makedirs(scratch, exist_ok=True)
        write_jsonl(os.path.join(scratch, "factory.smoke.jsonl"), frecs)
        # link probe on ONE file first (hardlink preferred, symlink fallback)
        probe_src = frecs[0]["file_path"]
        os.makedirs(BROWSE["factory"], exist_ok=True)
        probe_dst = os.path.join(BROWSE["factory"],
                                 "_link_probe" + os.path.splitext(probe_src)[1])
        if os.path.lexists(probe_dst):
            os.unlink(probe_dst)
        make_link(probe_src, probe_dst)
        same = os.path.samefile(probe_src, probe_dst)
        log(f"smoke: link probe mode={_LINK_MODE['mode']} ok={same} ({probe_dst})")
        os.unlink(probe_dst)
        # verify sha on 5 of the 50
        bad = 0
        for r in frecs[:5]:
            if r["sha256"] and sha256_file(r["file_path"]) != r["sha256"]:
                bad += 1
                log(f"smoke SHA MISMATCH {r['file_path']}")
        log(f"smoke: sha spot-check 5 files, mismatches={bad}")
        for r in frecs[:3]:
            log("smoke sample: " + json.dumps(r, ensure_ascii=False)[:300])
        log("smoke DONE (no _ledger files touched)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
