#!/usr/bin/env python3
r"""Independent cross-episode NON-reuse gate — catches footage/image duplication ACROSS episodes.

The owner's recurring defect (memory: "Footage diversity") is that the SAME stock footage /
image is reused from one episode to the next ("素材の被り 話またぎ"), so the channel's videos
start to look interchangeable. This is the INDEPENDENT GATE that would catch that automatically
before an episode ships, so it can never re-ship.

WHAT IT MEASURES: CONTENT, NOT NAMES (2026-08-12)
-------------------------------------------------
The question this gate exists to answer is "does the viewer see the same picture twice across two
episodes". That is a question about BYTES. It is answered with bytes.

For the target episode we take the assets that are ACTUALLY PLACED IN THE CUT — every ``src`` in
its ``*_film.json`` ``cuts`` (that is what the viewer sees, not the wider unused pool) — resolve
each one to the file the renderer actually reads under ``remotion/public/``, and compare its
sha256 against the sha256 of every media file owned by a DIFFERENT episode. Identical bytes under
two episodes is a cross-episode REUSE and the gate FAILS, naming the asset and the episode(s) it
is shared with. Different bytes are not a reuse, however similar the two filenames are.

The comparison universe is every file placed in the CUT of every OTHER episode: each other
``remotion/src/data/*_film.json``, its cut ``src`` resolved to a real file under
``remotion/public/``, attributed to its ``episode_id``. It is deliberately NOT a walk of
``remotion/public/<slug>/`` -- that walk sweeps in ``rejected/``, ``factory_pruned_offtopic/`` and
superseded ``factory_unverified_v*/`` staging, i.e. clips another episode THREW AWAY and its
viewers never saw. Failing an episode for those is a false alarm. The full reasoning, and the
measurement showing the old walk matched nothing at all, is in ``build_content_universe``.

HOW IT STAYS CHEAP (the size pre-filter is exact, not an approximation)
-----------------------------------------------------------------------
Byte-identical files ALWAYS have identical sizes, so a target file whose size appears nowhere in
the universe cannot possibly be a reuse and is never opened. Only files that collide on exact size
are hashed. Measured on EP65 marmet: ~9,700 universe files stat'ed in seconds, a handful share a
size with one of marmet's 330 cut assets, and ~2 GB is hashed instead of the 323 GB the public
tree holds. The filter changes the cost, never the answer.
A reference that cannot be resolved to a readable file is reported as UNVERIFIED and is never
counted as a reuse: no bytes were read, so no claim about the bytes can honestly be made. The
count is printed and returned so it can never become a silent hole. If NOTHING could be read the
gate skips rather than certifying anything.

FALSE-GREEN GUARD
-----------------
A "no reuse" verdict is only trustworthy if there was a substantial library to compare against.
If the comparison universe has fewer than MIN_PRIOR_EPISODES distinct other episodes OR fewer than
MIN_FINGERPRINTS files, a green result is meaningless, so the gate FAILS (exit 1) with an explicit
"comparison set too small" reason instead of falsely certifying uniqueness.
(A genuine reuse is reported as FAIL regardless of universe size — finding a collision already
proves the set was non-empty.)

Usage:
  py -3.11 scripts/check_arc_nonrepeat.py --ep PD-2026-031-unlock
  py -3.11 scripts/check_arc_nonrepeat.py --ep PD-2026-031-unlock --dry-run   # report, always exit 0
  py -3.11 scripts/check_arc_nonrepeat.py --selftest                          # RED fixture + real run
  py -3.11 scripts/check_arc_nonrepeat.py --ep PD-2026-031-unlock --json out.json

Exit codes: 0 = PASS (or --dry-run, or artifact-absent skip), 1 = FAIL / usage error.

check_final_acceptance can import this module and call ``evaluate(epdir)``; the returned dict keys
(check / ok / hard / reason / skipped / reused / prior_episodes / universe_fingerprints /
target_assets / reused_count) are the stable contract. ``evaluate`` NEVER calls sys.exit and never
raises on missing inputs — it returns a skip dict so the caller cannot crash.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-031-unlock"
CHECK_NAME = "arc_nonrepeat"

# Media extensions that count as a reusable visual asset.
MEDIA_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".mov", ".webm", ".m4v"}

# public/ subdirectories that are NOT episodes (shared pools / scratch) — excluded from attribution
# so a reuse is never mis-blamed on a utility folder.
NON_EPISODE_DIRS = {
    "assets", "clips", "approved", "sample", "_motiontest", "pd", "real", "shorts",
}

# False-green guard thresholds. A "no reuse" verdict below EITHER floor is not trustworthy.
MIN_PRIOR_EPISODES = 10     # need at least this many distinct OTHER episodes to certify uniqueness
MIN_FINGERPRINTS = 200      # ...and at least this many distinct fingerprints in the universe


# ---------------------------------------------------------------------------------------------
# fingerprinting helpers
# ---------------------------------------------------------------------------------------------

def fingerprint(src: str) -> Optional[str]:
    """NAME-ONLY heuristic. **This is not the gate's verdict** — see ``evaluate``, which compares
    sha256. Reduce an asset reference to a comparable name: the lowercased basename, stripped of
    any leading ``<slug>/`` folder so the SAME stock file collides across episodes. Returns None
    for empty / non-string input.

    Its ONLY remaining consumer is ``select_factory_assets.used_basenames()``, which uses it to
    AVOID picking a shelf clip whose name is already spoken for. Over-matching there is harmless
    (it merely picks a different clip); over-matching in a ship gate blocks an episode, which is
    why the gate no longer uses it.
    """
    if not isinstance(src, str) or not src.strip():
        return None
    norm = src.strip().replace("\\", "/").lower()
    base = os.path.basename(norm)
    # Many generated episode-local assets intentionally use slot names such as
    # S01.png or M01_rife.mp4 under each episode folder. Those are not shared
    # stock identifiers; comparing only the basename makes every episode look
    # like a reuse. Keep the folder for those slot-style generated assets, while
    # preserving basename matching for real shared stock clips (AF-BG-..., etc.).
    #
    # ============================ READ THIS BEFORE EDITING ============================
    # DO NOT ADD A LETTER TO THE PATTERN BELOW TO FIX A FALSE POSITIVE. It will not work,
    # and the attempt is the bug this list has now produced twice.
    #
    #   2026-08-02  P01.png..P## (the per-episode PEOPLE plates) were missing, so every
    #               episode that had them looked like it reused six assets from the three
    #               episodes before it. Verified: burge/willingham/morton/norfolk P01.png
    #               have four different sha256 and four different byte sizes -- same slot
    #               name, different pictures. A letter was added. The SHAPE was not fixed.
    #   2026-08-12  R015..R132 (the per-episode RECONSTRUCTION plates) were missing, and
    #               EP65 marmet was blocked by 15 phantom "reuses from PD-2026-067-ramirez".
    #               Verified again: marmet R015 is 12,228,247 bytes, ramirez R015 is
    #               7,198,680 -- and all 15 differ in both size and sha256. marmet owns 94
    #               R-plates, ramirez 34; the 15 flagged were exactly their name-intersection,
    #               which is what independent per-episode slot counters always look like.
    #
    # The list was never the fix, because a per-episode SLOT NAME is not evidence about
    # content in either direction. It produced false ALARMS (different pictures, same slot)
    # and it also HID real reuse (an exempted name whose bytes genuinely were copied from
    # another episode was waived through unread). The gate now reads the bytes, so a new
    # plate family needs NO change here and NO change anywhere else: R was never added.
    # If you are here because a gate fired, go read ``evaluate`` and check the sha256 --
    # if the bytes match, it is a real reuse and the answer is to change the picture.
    # ==================================================================================
    if re.match(r"^(s\d{2,3}|p\d{2,3}|m\d{1,3}_rife|f\d{3}.*)\.(png|jpg|jpeg|webp|mp4|mov|webm|m4v)$", base):
        return norm
    return base


def _load_film(path: Path) -> Optional[dict[str, Any]]:
    """Load a *_film.json, returning the dict or None if unreadable / not a film with cuts."""
    try:
        d = json.loads(path.read_text("utf-8"))
    except Exception:  # noqa: BLE001 - malformed json is simply skipped from the universe
        return None
    if isinstance(d, dict) and isinstance(d.get("cuts"), list):
        return d
    return None


def _film_fingerprints(film: dict[str, Any]) -> set[str]:
    """Distinct fingerprints for every asset actually placed in a film's cuts."""
    fps: set[str] = set()
    for cut in film.get("cuts", []):
        if not isinstance(cut, dict):
            continue
        fp = fingerprint(cut.get("src"))
        if fp:
            fps.add(fp)
    return fps


def resolve_target_film(data_dir: Path, ep: str) -> Optional[tuple[Path, dict[str, Any], set[str]]]:
    """Find the target episode's film json under ``data_dir`` from an --ep slug.

    Matches on episode_id equality OR on the film's core slug (``unlock`` from ``unlock_film.json``)
    appearing as the tail of ``ep`` (so ``PD-2026-031-unlock`` and ``unlock`` both resolve). Returns
    (path, film_dict, target_labels) or None. ``target_labels`` is every name that identifies the
    target (episode_id + core slug + raw ep) so it is excluded from the comparison universe.
    """
    ep_tail = ep.split("-")[-1].lower()
    for path in sorted(data_dir.glob("*_film.json")):
        film = _load_film(path)
        if film is None:
            continue
        core = path.name[:-len("_film.json")].lower()
        eid = str(film.get("episode_id") or "")
        if eid == ep or (core and (core == ep_tail or core == ep.lower())):
            labels = {x for x in (eid, core, ep, ep.lower()) if x}
            return path, film, labels
    return None


def build_universe(data_dir: Path, public_dir: Path,
                   target_labels: set[str]) -> tuple[dict[str, set[str]], set[str]]:
    """Build the comparison universe: a map ``fingerprint -> {episode labels that own it}`` drawn
    from every OTHER film json and every OTHER public/<slug>/ media file. The target's own labels
    are excluded from ownership so the target never compares against itself. Returns
    (fp_to_eps, other_episodes)."""
    fp_to_eps: dict[str, set[str]] = {}
    other_eps: set[str] = set()

    def add(fp: Optional[str], label: str) -> None:
        if not fp or not label or label in target_labels:
            return
        fp_to_eps.setdefault(fp, set()).add(label)
        other_eps.add(label)

    # source 1: other film jsons (assets actually cut into other episodes)
    if data_dir.is_dir():
        for path in sorted(data_dir.glob("*_film.json")):
            film = _load_film(path)
            if film is None:
                continue
            label = str(film.get("episode_id") or path.name[:-len("_film.json")])
            for fp in _film_fingerprints(film):
                add(fp, label)

    # source 2: public/<slug>/ media files (where shared factory stock physically lives)
    if public_dir.is_dir():
        for slug_dir in sorted(p for p in public_dir.iterdir() if p.is_dir()):
            slug = slug_dir.name.lower()
            if slug in NON_EPISODE_DIRS:
                continue
            for f in slug_dir.rglob("*"):
                if f.is_file() and f.suffix.lower() in MEDIA_EXTS:
                    add(str(f.relative_to(public_dir)).replace("\\", "/").lower(), slug)

    return fp_to_eps, other_eps


# ---------------------------------------------------------------------------------------------
# core evaluation (importable by check_final_acceptance)
# ---------------------------------------------------------------------------------------------

_HASH_CHUNK = 1 << 20


def _sha256(path: Path) -> Optional[str]:
    """sha256 over a file's bytes, or None if it cannot be read (never raises)."""
    h = hashlib.sha256()
    try:
        with open(path, "rb") as fh:
            for block in iter(lambda: fh.read(_HASH_CHUNK), b""):
                h.update(block)
    except OSError:
        return None
    return h.hexdigest()


def resolve_asset(public_dir: Path, src: Any) -> Optional[Path]:
    """Resolve a film-json ``src`` to the file the renderer actually reads, or None if it is not
    a readable file. ``src`` is relative to ``remotion/public/`` (e.g. ``marmet/img/R015.png``)."""
    if not isinstance(src, str) or not src.strip():
        return None
    try:
        p = public_dir / src.strip().replace("\\", "/")
        return p if p.is_file() else None
    except OSError:
        return None


def _slug_to_episode_id(data_dir: Path) -> dict[str, str]:
    """``{"marmet": "PD-2026-065-marmet"}`` so a public/<slug>/ file is blamed on its episode id
    rather than on a bare folder name."""
    out: dict[str, str] = {}
    if not data_dir.is_dir():
        return out
    for path in sorted(data_dir.glob("*_film.json")):
        film = _load_film(path)
        if film is None:
            continue
        eid = str(film.get("episode_id") or "").strip()
        core = path.name[:-len("_film.json")].lower()
        if eid and core:
            out[core] = eid
    return out


def build_content_universe(data_dir: Path, public_dir: Path, target_labels: set[str],
                           ) -> tuple[dict[int, list[tuple[Path, str]]], set[str]]:
    """Every file placed in the CUT of an episode OTHER than the target, indexed by exact byte
    size: ``{size: [(path, owning_episode_label), ...]}``. STAT ONLY — nothing is hashed here.
    Hashing is deferred to the few files that collide with a target file's size, which is what
    keeps this affordable. Also returns the set of distinct other-episode labels.

    WHY THE UNIVERSE IS CUTS, AND NOT A WALK OF ``public/<slug>/`` (2026-08-12)
    --------------------------------------------------------------------------
    The gate asks whether the VIEWER sees the same picture in two episodes. It already holds the
    target to that standard ("assets ACTUALLY PLACED IN THE CUT ... not the wider unused pool").
    Symmetry is not optional: a clip that another episode REJECTED is not something the viewer
    saw there, so using it is not reuse.

    This is not a relaxation, because the walk never did anything. The original code fingerprinted
    a target cut as a BASENAME (``af-bg-2974__x.mp4``) but a public file as its FULL RELATIVE PATH
    (``flowers/factory/af-bg-2974__x.mp4``). Those namespaces cannot intersect except within one
    episode's own folder, which is excluded as the target's. Measured over all 45 film jsons on
    2026-08-12: the film-json half produced 738 matches and the public half produced ZERO. Its only
    real effect was to inflate ``universe_fingerprints`` to ~39,000 so the false-green guard was
    satisfied by files that could never be compared.

    Restoring it under content comparison was tried and is WRONG: it made EP65 marmet fail on 12
    clips whose bytes sit in ``flowers/rejected/...``, ``flowers/factory_pruned_offtopic/...`` and
    ``<slug>/factory_unverified_v001/...`` -- discarded staging, plus ``_ai/searched.mp4``. None of
    those are in any cut. Blocking an episode for reusing a clip another episode threw away is a
    false alarm, and it is the same mistake in a new costume: judging by where a file sits instead
    of by what the audience sees.

    ``select_factory_assets.used_basenames()`` still wants the wider staged pool, because AVOIDING
    a name at selection time is cheap and over-avoiding is harmless. It keeps using the name-based
    ``build_universe`` above. The selector may be conservative; a ship gate must be exact.
    """
    by_size: dict[int, list[tuple[Path, str]]] = {}
    other_eps: set[str] = set()
    seen: set[Path] = set()

    def add(path: Path, label: str) -> None:
        if not label or label in target_labels or path in seen:
            return
        try:
            size = path.stat().st_size
        except OSError:
            return
        seen.add(path)
        by_size.setdefault(size, []).append((path, label))
        other_eps.add(label)

    if data_dir.is_dir():
        for path in sorted(data_dir.glob("*_film.json")):
            film = _load_film(path)
            if film is None:
                continue
            core = path.name[:-len("_film.json")].lower()
            label = str(film.get("episode_id") or core)
            if label in target_labels or core in target_labels:
                continue
            for cut in film.get("cuts", []):
                if isinstance(cut, dict):
                    fp = resolve_asset(public_dir, cut.get("src"))
                    if fp is not None:
                        add(fp, label)

    return by_size, other_eps


# ---------------------------------------------------------------------------------------------
# THE SAME UNIVERSE, OFFERED TO THE SELECTOR (2026-08-12)
# ---------------------------------------------------------------------------------------------
# `evaluate` below DETECTS cross-episode reuse at ship time. `stage_footage_by_title.py` is where
# reuse is CREATED, and until today it excluded a candidate by ID PREFIX only
# (`name.split("__")[0]`), so it could not see the shelf's duplicate ingests: the same source file
# is present twice under two identifiers -- `AR-11490316__close_up_view_of_barbed_wire.mp4` here
# and `AF-BG-23315__barbed_wire_fence_sky.mp4` there -- and a name comparison of two different
# names finds nothing. Measured over all 46 film jsons on 2026-08-12: 524 content groups shared
# across two or more episodes, 1,272 reuse incidents, and 861 of those 1,272 (68%) share bytes but
# NOT filenames. That 68% was structurally invisible to every check the selector had.
#
# The class below is the SELECTOR'S half of this gate, deliberately built on the SAME
# `build_content_universe` the gate decides with, so the two cannot drift into disagreeing about
# what "another episode already used this" means. It adds only what a selector needs and a ship
# gate must not have:
#   * a persistent (path, size, mtime_ns) -> sha256 cache under runs/, because staging asks about
#     thousands of shelf candidates against a ~9.7k-file universe, repeatedly, across sessions;
#   * `owners_of()`, which answers for ONE candidate file that is not in any film json yet.
# `evaluate` deliberately does NOT use the cache: a ship gate reads the bytes it is certifying.
_HASH_CACHE_REL = Path("runs") / "cache" / "media_sha256.v001.json"


def _cache_key(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/").lower()


class ContentIndex:
    """Byte-content index of every asset cut into an episode OTHER than the target.

    Usage (selector side)::

        idx = ContentIndex(target_labels={"openfields"})
        owners = idx.owners_of(Path(r"E:\\pd-media\\...\\clip.mp4"))   # [] means genuinely fresh
        idx.save()

    Nothing is hashed when the index is built. A candidate whose exact byte SIZE appears nowhere
    in the universe cannot be byte-identical to anything in it, so it is answered without opening
    either file -- that is what keeps the check affordable at harvesting scale. Only a size
    collision costs a hash, and every hash is remembered in ``runs/cache/media_sha256.v001.json``
    keyed by (path, size, mtime_ns), so a file whose bytes have not changed is hashed once ever.
    """

    def __init__(self, target_labels: set[str], *, data_dir: Optional[Path] = None,
                 public_dir: Optional[Path] = None, cache_path: Optional[Path] = None,
                 use_cache: bool = True) -> None:
        self.data_dir = Path(data_dir) if data_dir is not None else (ROOT / "remotion" / "src" / "data")
        self.public_dir = Path(public_dir) if public_dir is not None else (ROOT / "remotion" / "public")
        self.by_size, self.episodes = build_content_universe(
            self.data_dir, self.public_dir, set(target_labels))
        self.files = sum(len(v) for v in self.by_size.values())
        self.cache_path = Path(cache_path) if cache_path is not None else (ROOT / _HASH_CACHE_REL)
        self.use_cache = use_cache
        self._cache: dict[str, list] = self._load_cache() if use_cache else {}
        self._cache_dirty = False
        self.hashed_files = 0          # files actually read this run (cache misses)
        self.hashed_bytes = 0
        self.size_hits = 0             # candidates whose size collided, so a hash was needed
        self.checked = 0               # candidates asked about

    # -- cache -------------------------------------------------------------------------------
    def _load_cache(self) -> dict[str, list]:
        try:
            d = json.loads(self.cache_path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 - a missing or corrupt cache is simply an empty one
            return {}
        e = d.get("entries") if isinstance(d, dict) else None
        return e if isinstance(e, dict) else {}

    def sha256(self, path: Path) -> Optional[str]:
        """sha256 of ``path``, from the cache when (size, mtime_ns) still match. Never raises."""
        try:
            st = path.stat()
        except OSError:
            return None
        if self.use_cache:
            key = _cache_key(path)
            hit = self._cache.get(key)
            if (isinstance(hit, list) and len(hit) == 3
                    and hit[0] == st.st_size and hit[1] == st.st_mtime_ns):
                return str(hit[2])
        digest = _sha256(path)
        if digest is None:
            return None
        self.hashed_files += 1
        self.hashed_bytes += st.st_size
        if self.use_cache:
            self._cache[_cache_key(path)] = [st.st_size, st.st_mtime_ns, digest]
            self._cache_dirty = True
        return digest

    def save(self) -> Optional[Path]:
        """Persist the hash cache, MERGING with whatever another process wrote meanwhile.

        Merge rather than overwrite: several tools and agents run against this repo at once, and a
        last-writer-wins cache would throw away hours of another run's hashing.
        """
        if not (self.use_cache and self._cache_dirty):
            return None
        merged = dict(self._load_cache())
        merged.update(self._cache)
        _atomic_write_json(self.cache_path, {
            "schema_version": "media_sha256_cache.v001",
            "note": "path -> [size, mtime_ns, sha256]. Derived data: safe to delete, it rebuilds.",
            "entries": merged})
        self._cache = merged
        self._cache_dirty = False
        return self.cache_path

    # -- the question ------------------------------------------------------------------------
    def owners_of(self, path: Path) -> list[str]:
        """Episodes whose CUT contains a file byte-identical to ``path``. ``[]`` means fresh.

        An unreadable file returns ``[]``: this is a selector, and refusing to stage a clip we
        merely failed to stat would silently starve a pool. The ship gate is where an unreadable
        asset becomes UNVERIFIED and visible.
        """
        self.checked += 1
        try:
            size = Path(path).stat().st_size
        except OSError:
            return []
        bucket = self.by_size.get(size)
        if not bucket:
            return []                                   # no size match -> nothing is opened
        self.size_hits += 1
        mine = self.sha256(Path(path))
        if mine is None:
            return []
        owners: set[str] = set()
        for other, label in bucket:
            if label in owners:
                continue
            if self.sha256(other) == mine:
                owners.add(label)
        return sorted(owners)


def target_labels_for(slug: str, data_dir: Optional[Path] = None) -> set[str]:
    """Every label that identifies episode ``slug``, for exclusion from its own comparison
    universe. An episode with no film json yet (the normal case while its footage is still being
    harvested) contributes its slug alone."""
    data_dir = Path(data_dir) if data_dir is not None else (ROOT / "remotion" / "src" / "data")
    if data_dir.is_dir():
        resolved = resolve_target_film(data_dir, slug)
        if resolved is not None:
            return resolved[2]
    return {slug, slug.lower()}


def evaluate(epdir: Path, *, data_dir: Optional[Path] = None,
             public_dir: Optional[Path] = None) -> dict[str, Any]:
    """Cross-episode NON-reuse gate, decided on CONTENT (sha256). ``epdir`` is the episode
    directory (its ``.name`` is the slug, e.g. ``episodes/PD-2026-031-unlock``). NEVER raises,
    NEVER calls sys.exit.

    Returns a dict compatible with check_final_acceptance:
      {"check", "ok", "hard", "reason", ... , optionally "skipped": True}
    A missing target film json (e.g. data on SSD / not in repo) returns a non-blocking skip
    ({"ok": True, "hard": False, "skipped": True}). A genuine reuse OR a too-small comparison set
    returns {"ok": False, "hard": True}.
    """
    epdir = Path(epdir)
    slug = epdir.name
    data_dir = Path(data_dir) if data_dir is not None else (ROOT / "remotion" / "src" / "data")
    public_dir = Path(public_dir) if public_dir is not None else (ROOT / "remotion" / "public")

    if not data_dir.is_dir():
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"film-data dir not present (skipping): {data_dir}"}

    resolved = resolve_target_film(data_dir, slug)
    if resolved is None:
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"no *_film.json resolves to episode '{slug}' under {data_dir} "
                          f"(assets may be on SSD) — skipping"}
    film_path, film, target_labels = resolved
    target_srcs = sorted({str(c.get("src")) for c in film.get("cuts", [])
                          if isinstance(c, dict) and c.get("src")})
    if not target_srcs:
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"{film_path.name} has no cut assets to check — skipping"}

    # resolve every cut asset to bytes on disk; what cannot be read is UNVERIFIED, never "reused"
    target_files: dict[Path, str] = {}
    unverified: list[str] = []
    for src in target_srcs:
        p = resolve_asset(public_dir, src)
        if p is None:
            unverified.append(src)
        else:
            target_files.setdefault(p, src)
    if not target_files:
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"none of {film_path.name}'s {len(target_srcs)} cut assets resolve to a "
                          f"readable file under {public_dir} — cannot compare content, skipping"}

    by_size, other_eps = build_content_universe(data_dir, public_dir, target_labels)

    # EXACT size pre-filter: byte-identical implies size-identical, so anything whose size is
    # absent from the universe cannot be a reuse and is never opened.
    tsize: dict[Path, int] = {}
    for p in target_files:
        try:
            tsize[p] = p.stat().st_size
        except OSError:
            unverified.append(target_files[p])
    candidates = {p: by_size[s] for p, s in tsize.items() if s in by_size}

    uni_hash: dict[Path, Optional[str]] = {}
    hashed_bytes = 0
    reused: list[dict[str, Any]] = []
    for p in sorted(candidates):
        th = _sha256(p)
        if th is None:
            unverified.append(target_files[p])
            continue
        hashed_bytes += tsize[p]
        owners: set[str] = set()
        for q, label in candidates[p]:
            if q not in uni_hash:
                uni_hash[q] = _sha256(q)
                try:
                    hashed_bytes += q.stat().st_size
                except OSError:
                    pass
            if uni_hash[q] is not None and uni_hash[q] == th:
                owners.add(label)
        if owners:
            reused.append({"asset": target_files[p], "sha256": th,
                           "from_episodes": sorted(owners)})

    prior_episodes = len(other_eps)
    universe_fingerprints = sum(len(v) for v in by_size.values())
    unverified_set = sorted(set(unverified))
    verified = len(target_srcs) - len(unverified_set)

    common = {
        "check": CHECK_NAME,
        "film_json": str(film_path),
        "episode_id": str(film.get("episode_id") or slug),
        "target_assets": len(target_srcs),
        "verified_assets": max(verified, 0),
        "unverified_assets": unverified_set,
        "unverified_count": len(unverified_set),
        "prior_episodes": prior_episodes,
        "universe_fingerprints": universe_fingerprints,
        "hashed_megabytes": round(hashed_bytes / 1e6, 1),
        "reused_count": len(reused),
        "reused": reused,
    }
    unver = (f"; {len(unverified_set)} reference(s) UNVERIFIED (no readable file)"
             if unverified_set else "")

    if reused:
        top = "; ".join(f"{r['asset']} <- {', '.join(r['from_episodes'][:3])}" for r in reused[:6])
        more = "" if len(reused) <= 6 else f" (+{len(reused) - 6} more)"
        return {**common, "ok": False, "hard": True,
                "reason": f"{len(reused)}/{len(target_srcs)} cut assets are byte-identical to an "
                          f"asset in another episode: {top}{more}{unver}"}

    # no reuse found -> only trustworthy if the comparison universe is substantial
    if prior_episodes < MIN_PRIOR_EPISODES or universe_fingerprints < MIN_FINGERPRINTS:
        return {**common, "ok": False, "hard": True,
                "reason": f"comparison set too small to certify non-reuse "
                          f"({prior_episodes} prior episodes < {MIN_PRIOR_EPISODES} or "
                          f"{universe_fingerprints} files < {MIN_FINGERPRINTS}) — "
                          f"refusing false-green"}

    return {**common, "ok": True, "hard": True,
            "reason": f"no cross-episode reuse: {len(target_srcs)} cut assets share no bytes with "
                      f"{prior_episodes} other episodes / {universe_fingerprints} files{unver}"}


# ---------------------------------------------------------------------------------------------
# reporting
# ---------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("CROSS-EPISODE NON-REUSE REPORT (content / sha256)")
    print("=" * 78)
    print(f"  film json    : {r.get('film_json')}")
    print(f"  episode      : {r.get('episode_id')}")
    print(f"  cut assets   : {r.get('target_assets')} "
          f"({r.get('verified_assets')} read, {r.get('unverified_count')} unverified)")
    print(f"  universe     : {r.get('prior_episodes')} other episodes / "
          f"{r.get('universe_fingerprints')} files")
    print(f"  bytes hashed : {r.get('hashed_megabytes')} MB (size pre-filter)")
    print(f"  reused       : {r.get('reused_count')}")
    for item in (r.get("reused") or [])[:25]:
        owners = ", ".join(item["from_episodes"])
        print(f"    - {item['asset']}  sha256={str(item.get('sha256'))[:16]}..   <- {owners}")
    extra = (r.get("reused_count") or 0) - 25
    if extra > 0:
        print(f"    ... (+{extra} more reused assets)")
    for u in (r.get("unverified_assets") or [])[:10]:
        print(f"    ? UNVERIFIED (no readable file, no content claim made): {u}")
    print("-" * 78)
    print(f"  RESULT: {'PASS' if r.get('ok') else 'FAIL'}  — {r.get('reason')}")
    print("-" * 78)


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write JSON atomically (temp file in the same dir, then os.replace)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False, default=str)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


# ---------------------------------------------------------------------------------------------
# selftest: RED fixture (must FAIL) + real run
# ---------------------------------------------------------------------------------------------

def _mkfile(p: Path, data: bytes) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def _fixture(tmp: Path) -> tuple[Path, Path]:
    """12 prior episodes, each with 20 real files on disk AND in its cuts (240 > MIN_FINGERPRINTS,
    12 > MIN_PRIOR_EPISODES), so a green verdict clears the false-green guard honestly."""
    data_dir = tmp / "data"
    public_dir = tmp / "public"
    data_dir.mkdir()
    public_dir.mkdir()
    for i in range(12):
        eid = f"PD-2000-{i:03d}-prior{i}"
        cuts = []
        for j in range(20):
            rel = f"prior{i}/img/{eid}-S{j:03d}-IMG.png"
            _mkfile(public_dir / rel, os.urandom(2048 + i * 64 + j))
            cuts.append({"src": rel})
        (data_dir / f"prior{i}_film.json").write_text(
            json.dumps({"episode_id": eid, "cuts": cuts}), "utf-8")
    return data_dir, public_dir


def _stage_into_cut(data_dir: Path, public_dir: Path, prior: str, rel: str, data: bytes) -> None:
    """Write real bytes into a PRIOR episode and put them in that episode's CUT -- which is what
    'the viewer saw it there' means, and therefore what the universe is built from."""
    _mkfile(public_dir / rel, data)
    fp = data_dir / f"{prior}_film.json"
    film = json.loads(fp.read_text("utf-8"))
    film["cuts"].append({"src": rel})
    fp.write_text(json.dumps(film), "utf-8")


def _case(name: str, why: str, data_dir: Path, public_dir: Path, slug: str,
          cuts: list[str], expect_ok: bool) -> bool:
    """Run one fixture through evaluate() and assert the verdict is the required one."""
    eid = f"PD-9999-999-{slug}"
    (data_dir / f"{slug}_film.json").write_text(
        json.dumps({"episode_id": eid, "cuts": [{"src": c} for c in cuts]}), "utf-8")
    r = evaluate(Path("episodes") / eid, data_dir=data_dir, public_dir=public_dir)
    got = bool(r.get("ok")) and not r.get("skipped")
    passed = (got == expect_ok)
    print(f"\n  [{name}] {why}")
    print(f"    required ok={expect_ok}  ->  ok={r.get('ok')} "
          f"reused_count={r.get('reused_count')} skipped={bool(r.get('skipped'))} "
          f"universe={r.get('prior_episodes')} eps / {r.get('universe_fingerprints')} files")
    print(f"    reason: {r.get('reason')}")
    for item in (r.get("reused") or []):
        print(f"      - {item['asset']}  sha256={item['sha256'][:16]}..  "
              f"<- {', '.join(item['from_episodes'])}")
    print(f"    {'PASS' if passed else 'FAIL'} -- the gate "
          f"{'behaved as required' if passed else 'DID NOT behave as required'}")
    return passed


def _run_selftest() -> int:
    """Demonstrate the gate in BOTH directions on real bytes (a gate never shown to fail is
    decoration), then run it on the real test episode."""
    print("=" * 78)
    print("SELFTEST (a): both directions, on files that really exist")
    print("=" * 78)
    oks = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        data_dir, public_dir = _fixture(tmp)

        # RED 1 -- the same BYTES under a completely DIFFERENT name. Renaming a copied clip must
        # not launder it. The old basename gate could not see this at all.
        shared = os.urandom(50_000)
        _stage_into_cut(data_dir, public_dir, "prior3",
                        "prior3/factory/AF-BG-9999__shared_stock.mp4", shared)
        _mkfile(public_dir / "redrenamed/factory/ZZ-0001__innocent_new_name.mp4", shared)
        _mkfile(public_dir / "redrenamed/img/R001.png", os.urandom(9_000))
        oks.append(_case(
            "RED 1", "same bytes, DIFFERENT filename -> must FAIL", data_dir, public_dir,
            "redrenamed",
            ["redrenamed/factory/ZZ-0001__innocent_new_name.mp4", "redrenamed/img/R001.png"],
            expect_ok=False))

        # RED 2 -- the same BYTES under a per-episode SLOT name. P## was on the old exemption
        # list, so the old gate skipped it and waived a genuine copy through unread. This is the
        # false NEGATIVE the exemption list bought in exchange for its false positives.
        copied = os.urandom(40_000)
        _stage_into_cut(data_dir, public_dir, "prior5", "prior5/img/P01.png", copied)
        _mkfile(public_dir / "redslot/img/P01.png", copied)
        _mkfile(public_dir / "redslot/img/R002.png", os.urandom(9_100))
        oks.append(_case(
            "RED 2", "same bytes under an exempt SLOT name (P01.png) -> must FAIL",
            data_dir, public_dir, "redslot",
            ["redslot/img/P01.png", "redslot/img/R002.png"], expect_ok=False))

        # GREEN 1 -- the EP65 marmet case: the same slot name in two episodes, identical file
        # SIZE, different pictures. Names collide, bytes do not, so this is not a reuse. The
        # size match is deliberate: it forces the hash comparison to actually run.
        _stage_into_cut(data_dir, public_dir, "prior7", "prior7/img/R015.png", os.urandom(30_000))
        _mkfile(public_dir / "greenslot/img/R015.png", os.urandom(30_000))
        _mkfile(public_dir / "greenslot/img/R016.png", os.urandom(9_200))
        oks.append(_case(
            "GREEN 1", "same slot name AND same size, different bytes -> must PASS",
            data_dir, public_dir, "greenslot",
            ["greenslot/img/R015.png", "greenslot/img/R016.png"], expect_ok=True))

        # GREEN 2 -- a clip another episode REJECTED. Identical bytes, but the file sits in that
        # episode's rejected/ pile and is in no cut, so its viewers never saw it. Blocking on this
        # is the false alarm that a public/<slug>/ walk reintroduces; see build_content_universe.
        discarded = os.urandom(60_000)
        _mkfile(public_dir / "prior9/rejected/factory_blocked/AF-BG-4242__thrown_away.mp4",
                discarded)
        _mkfile(public_dir / "greenreject/factory/AF-BG-4242__thrown_away.mp4", discarded)
        _mkfile(public_dir / "greenreject/img/R003.png", os.urandom(9_300))
        oks.append(_case(
            "GREEN 2", "same bytes as a clip another episode REJECTED (in no cut) -> must PASS",
            data_dir, public_dir, "greenreject",
            ["greenreject/factory/AF-BG-4242__thrown_away.mp4", "greenreject/img/R003.png"],
            expect_ok=True))

    all_ok = all(oks)
    print(f"\n  SELFTEST (a): {'PASS' if all_ok else 'FAIL'} "
          f"({sum(oks)}/{len(oks)} required verdicts produced)")

    print("\n" + "=" * 78)
    print(f"SELFTEST (b): REAL run on {DEFAULT_EP}")
    print("=" * 78)
    r = evaluate(ROOT / "episodes" / DEFAULT_EP)
    _print_report(r)
    return 0 if all_ok else 1

# ---------------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------------

def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001 - reconfigure unavailable on some streams
        pass
    ap = argparse.ArgumentParser(
        description="Independent cross-episode NON-reuse gate: FAIL if the target episode reuses "
                    "footage/image assets that appear in a different episode.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug (e.g. PD-2026-031-unlock)")
    ap.add_argument("--dry-run", action="store_true",
                    help="run and report, but always exit 0 (never block)")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED fixture (must fail) then evaluate the real test episode")
    ap.add_argument("--json", default=None, metavar="PATH",
                    help="also write the raw result dict to PATH atomically")
    args = ap.parse_args(argv)

    if args.selftest:
        return _run_selftest()

    epdir = ROOT / "episodes" / args.ep
    r = evaluate(epdir)
    _print_report(r)
    if args.json:
        _atomic_write_json(Path(args.json), r)
        print(f"  wrote {args.json}")

    if args.dry_run:
        return 0
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
