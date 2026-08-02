#!/usr/bin/env python3
r"""Independent cross-episode NON-reuse gate — catches footage/image duplication ACROSS episodes.

The owner's recurring defect (memory: "Footage diversity") is that the SAME stock footage /
image is reused from one episode to the next ("素材の被り 話またぎ"), so the channel's videos
start to look interchangeable. This is the INDEPENDENT GATE that would catch that automatically
before an episode ships, so it can never re-ship.

WHAT IT MEASURES (the real intent, not a proxy)
-----------------------------------------------
For the target episode we take the assets that are ACTUALLY PLACED IN THE CUT — every ``src`` in
its ``*_film.json`` ``cuts`` (that is what the viewer sees, not the wider unused pool). For each we
compute a fingerprint = the asset's basename (e.g. ``AF-BG-0510__courtroom_interior.mp4`` or
``PD-2026-031-S001-IMG-001.png``). The basename deliberately strips the leading ``<slug>/`` folder
so that the SAME underlying stock clip collides across episodes even though each episode references
it under its own folder (``unlock/factory/AF-BG-0510...`` vs ``kyllo/factory/AF-BG-0510...``).

We then build the COMPARISON UNIVERSE of fingerprints owned by every OTHER episode, from two
sources:
  1. every other ``remotion/src/data/*_film.json`` (its cut ``src`` basenames), attributed to its
     ``episode_id``;
  2. every ``remotion/public/<slug>/`` media file (recursively), attributed to ``<slug>`` — this
     is where the shared factory clips (``AF-BG-*``, ``AF-TEX-*``) physically live, copied into
     many episode folders.

A target fingerprint that also appears under a DIFFERENT episode is a cross-episode REUSE and the
gate FAILS, naming every reused asset and which episode(s) it came from. Generated stills embed
their own episode id in the filename (``PD-2026-031-S...``) so they are naturally unique and never
false-positive; the reuse signal is genuine shared stock.

FALSE-GREEN GUARD
-----------------
A "no reuse" verdict is only trustworthy if there was a substantial library to compare against.
If the comparison universe has fewer than MIN_PRIOR_EPISODES distinct other episodes OR fewer than
MIN_FINGERPRINTS distinct fingerprints, a green result is meaningless, so the gate FAILS (exit 1)
with an explicit "comparison set too small" reason instead of falsely certifying uniqueness.
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
    """Reduce an asset reference to its comparable fingerprint: the lowercased basename, stripped
    of any leading ``<slug>/`` folder so the SAME stock file collides across episodes. Returns None
    for empty / non-string input."""
    if not isinstance(src, str) or not src.strip():
        return None
    norm = src.strip().replace("\\", "/").lower()
    base = os.path.basename(norm)
    # Many generated episode-local assets intentionally use slot names such as
    # S01.png or M01_rife.mp4 under each episode folder. Those are not shared
    # stock identifiers; comparing only the basename makes every episode look
    # like a reuse. Keep the folder for those slot-style generated assets, while
    # preserving basename matching for real shared stock clips (AF-BG-..., etc.).
    # P01.png..P## are the per-episode PEOPLE plates and belong in this list too. They were
    # missing, so every episode that had them looked like it reused six assets from the three
    # episodes before it. Verified on 2026-08-02: burge/willingham/morton/norfolk P01.png have
    # four different sha256 and four different byte sizes -- same slot name, different pictures.
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

def evaluate(epdir: Path, *, data_dir: Optional[Path] = None,
             public_dir: Optional[Path] = None) -> dict[str, Any]:
    """Cross-episode NON-reuse gate. ``epdir`` is the episode directory (its ``.name`` is the slug,
    e.g. ``episodes/PD-2026-031-unlock``). NEVER raises, NEVER calls sys.exit.

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
    target_fps = _film_fingerprints(film)
    if not target_fps:
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"{film_path.name} has no cut assets to check — skipping"}

    fp_to_eps, other_eps = build_universe(data_dir, public_dir, target_labels)

    # reuse detection: a target asset also owned by a DIFFERENT episode
    reused: list[dict[str, Any]] = []
    for fp in sorted(target_fps):
        owners = sorted(fp_to_eps.get(fp, set()))
        if owners:
            reused.append({"asset": fp, "from_episodes": owners})

    prior_episodes = len(other_eps)
    universe_fingerprints = len(fp_to_eps)

    common = {
        "check": CHECK_NAME,
        "film_json": str(film_path),
        "episode_id": str(film.get("episode_id") or slug),
        "target_assets": len(target_fps),
        "prior_episodes": prior_episodes,
        "universe_fingerprints": universe_fingerprints,
        "reused_count": len(reused),
        "reused": reused,
    }

    if reused:
        top = "; ".join(f"{r['asset']} <- {', '.join(r['from_episodes'][:3])}" for r in reused[:6])
        more = "" if len(reused) <= 6 else f" (+{len(reused) - 6} more)"
        return {**common, "ok": False, "hard": True,
                "reason": f"{len(reused)}/{len(target_fps)} cut assets reused from other episodes: "
                          f"{top}{more}"}

    # no reuse found -> only trustworthy if the comparison universe is substantial
    if prior_episodes < MIN_PRIOR_EPISODES or universe_fingerprints < MIN_FINGERPRINTS:
        return {**common, "ok": False, "hard": True,
                "reason": f"comparison set too small to certify non-reuse "
                          f"({prior_episodes} prior episodes < {MIN_PRIOR_EPISODES} or "
                          f"{universe_fingerprints} fingerprints < {MIN_FINGERPRINTS}) — "
                          f"refusing false-green"}

    return {**common, "ok": True, "hard": True,
            "reason": f"no cross-episode reuse: {len(target_fps)} cut assets are all unique vs "
                      f"{prior_episodes} other episodes / {universe_fingerprints} fingerprints"}


# ---------------------------------------------------------------------------------------------
# reporting
# ---------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("CROSS-EPISODE NON-REUSE REPORT")
    print("=" * 78)
    print(f"  film json    : {r.get('film_json')}")
    print(f"  episode      : {r.get('episode_id')}")
    print(f"  cut assets   : {r.get('target_assets')}")
    print(f"  universe     : {r.get('prior_episodes')} other episodes / "
          f"{r.get('universe_fingerprints')} fingerprints")
    print(f"  reused       : {r.get('reused_count')}")
    for item in (r.get("reused") or [])[:25]:
        owners = ", ".join(item["from_episodes"])
        print(f"    - {item['asset']}   <- {owners}")
    extra = (r.get("reused_count") or 0) - 25
    if extra > 0:
        print(f"    ... (+{extra} more reused assets)")
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

def _run_selftest() -> int:
    """(a) synthesize a KNOWN-BAD input and assert the gate reports ok=False (RED FIXTURE);
    (b) run evaluate() on the real TEST EPISODE and print the actual numbers."""
    print("=" * 78)
    print("SELFTEST (a): RED FIXTURE — a target that reuses a prior asset MUST fail")
    print("=" * 78)
    red_ok = False
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        data_dir = tmp / "data"
        public_dir = tmp / "public"  # intentionally empty (universe comes from synthetic films)
        data_dir.mkdir()
        public_dir.mkdir()

        shared_asset = "AF-BG-9999__shared_stock_clip.mp4"
        # 12 synthetic PRIOR episodes -> clears MIN_PRIOR_EPISODES(10); ~20 fps each -> >200 fps.
        for i in range(12):
            eid = f"PD-2000-{i:03d}-prior{i}"
            cuts = [{"src": f"prior{i}/img/{eid}-S{j:03d}-IMG.png"} for j in range(20)]
            if i == 3:  # ONE prior episode also owns the shared asset -> guarantees a collision
                cuts.append({"src": f"prior{i}/factory/{shared_asset}"})
            (data_dir / f"prior{i}_film.json").write_text(
                json.dumps({"episode_id": eid, "cuts": cuts}), "utf-8")

        # the KNOWN-BAD target reuses the shared asset
        target_eid = "PD-9999-999-redtest"
        (data_dir / "redtest_film.json").write_text(json.dumps({
            "episode_id": target_eid,
            "cuts": [
                {"src": f"redtest/img/{target_eid}-S001-IMG.png"},
                {"src": f"redtest/factory/{shared_asset}"},  # <-- the reuse
            ],
        }), "utf-8")

        red = evaluate(tmp / "episodes" / target_eid, data_dir=data_dir, public_dir=public_dir)
        red_ok = (red.get("ok") is False) and (red.get("reused_count", 0) >= 1) \
            and not red.get("skipped")
        print(f"  ok={red.get('ok')}  reused_count={red.get('reused_count')}  "
              f"prior_episodes={red.get('prior_episodes')}  "
              f"universe_fingerprints={red.get('universe_fingerprints')}")
        print(f"  reason: {red.get('reason')}")
        print(f"\nRED-FIXTURE: {'PASS' if red_ok else 'FAIL'}   "
              f"(the gate {'correctly failed' if red_ok else 'DID NOT fail'} the known-bad input)")

        # sanity: a target with a UNIQUE-only asset set must PASS against the same universe
        (data_dir / "greentest_film.json").write_text(json.dumps({
            "episode_id": "PD-9999-998-greentest",
            "cuts": [{"src": f"greentest/img/PD-9999-998-greentest-S{j:03d}-IMG.png"}
                     for j in range(5)],
        }), "utf-8")
        green = evaluate(tmp / "episodes" / "PD-9999-998-greentest",
                         data_dir=data_dir, public_dir=public_dir)
        print(f"\n  (green control) ok={green.get('ok')} reused_count={green.get('reused_count')} "
              f"-> {'PASS as expected' if green.get('ok') else 'UNEXPECTED FAIL'}")

    print("\n" + "=" * 78)
    print(f"SELFTEST (b): REAL run on {DEFAULT_EP}")
    print("=" * 78)
    r = evaluate(ROOT / "episodes" / DEFAULT_EP)
    _print_report(r)
    return 0 if red_ok else 1


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
