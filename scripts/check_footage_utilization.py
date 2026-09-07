#!/usr/bin/env python3
r"""Independent footage-utilization gate — proves staged/downloaded footage was actually USED.

The owner's recurring defect is "DL素材が1つも使われない": B-roll footage is staged/downloaded
into the render pool but the cutlist never references it, so the finished film ignores the very
clips that were pulled for it (紙芝居 / repeated stills instead of the intended motion b-roll).

This is the INDEPENDENT GATE that would have CAUGHT that automatically. It does NOT trust any
"selection plan" claim about what *should* be used — it measures the REAL relationship between two
concrete artifacts:

  * the STAGED POOL = the media files actually present in the render's public folder
        remotion/public/<slug>/factory/*.{mp4,mov,webm,mkv}   (downloaded/factory b-roll footage)
        remotion/public/<slug>/img/*.{png,jpg,jpeg,webp}      (Codex/AI stills)
  * the REFERENCES  = every "src" the cutlist remotion/src/data/<slug>_film.json points at FROM AN
        ARRAY THAT CaseFilm ACTUALLY RENDERS onto the screen — the hook shots (`hook`) and the cut
        list (`cuts`). References are matched by file BASENAME. Src values buried anywhere else in
        the JSON (a decoy/junk array, a "pool" manifest, dead metadata) are IGNORED on purpose: a
        clip only counts as "used" if it is placed on screen by a rendered array, not merely named
        somewhere in the file. This closes the junk-array hole (listing every clip in an unrendered
        array to fake 100% utilization).

It then reports used/total for footage and for images, the overall utilization, and the EXACT list
of staged clips referenced zero times.

FAIL (hard, ship-blocking) when either:
  * ANY staged footage clip is referenced 0 times  (the owner's "downloaded footage never used"), OR
  * overall utilization < UTIL_THRESHOLD (~80%): most of what was staged is dead weight.

Unused *images* alone do not fail (a couple of unused stills is normal spare coverage); they are
reported for visibility. If the pool folders are absent (media lives on the SSD, not in the repo)
the gate SKIPS honestly — it never fakes green and never crashes the caller.

Usage:
  py -3.11 scripts/check_footage_utilization.py --ep PD-2026-031-unlock
  py -3.11 scripts/check_footage_utilization.py --ep PD-2026-031-unlock --dry-run
  py -3.11 scripts/check_footage_utilization.py --ep PD-2026-031-unlock --json out.json
  py -3.11 scripts/check_footage_utilization.py --selftest

Exit codes: 0 = PASS or --dry-run or --selftest-ok ; 1 = FAIL or usage error ; 3 = SKIP (unmeasurable).

check_final_acceptance imports evaluate(epdir) and reads the dict contract below (check / ok / hard /
reason / skipped / utilization / footage_total / footage_used / footage_unused / img_* ). Keep stable.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-031-unlock"
GATE_NAME = "footage_utilization"

UTIL_THRESHOLD = 0.80  # overall used/total must be >= this (owner's ~80% intent). NOT a knob to relax.

VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".avif"}

# Only these TOP-LEVEL cutlist arrays are actually rendered by CaseFilm.tsx as staged-media shots
# (hook.map -> PunchShot src=h.src ; cuts.map -> Shot cut.src). captions/graphics/figures carry no
# pool src (they are procedural). A clip named in ANY OTHER key does NOT appear on screen and must
# NOT count as "used". Restricting collection to these arrays is what closes the junk-array hole.
RENDERED_SRC_ARRAYS = ("hook", "cuts")


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------

def slug_of(ep_name: str) -> str:
    """PD-2026-031-unlock -> 'unlock' ; PD-2026-032-carsearch -> 'carsearch' (everything after
    the 3rd hyphen, so multi-word slugs survive)."""
    parts = ep_name.split("-")
    return "-".join(parts[3:]) if len(parts) > 3 else ep_name


def _read_json(path: Path) -> Optional[dict[str, Any]]:
    """Read a JSON file as UTF-8 (the repo's film JSONs contain non-cp932 bytes). None on failure."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 - malformed/missing -> caller decides (skip, not crash)
        return None


def collect_src_basenames(node: Any, out: set[str]) -> None:
    """Collect the basename of every "src" string found under `node` (recursing INTO the given
    subtree only). Callers pass an individual rendered shot/cut item, so nested src (e.g. a layered
    shot) is still captured, but siblings outside the passed subtree are never seen."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "src" and isinstance(v, str) and v.strip():
                out.add(Path(v.replace("\\", "/")).name)
            else:
                collect_src_basenames(v, out)
    elif isinstance(node, list):
        for item in node:
            collect_src_basenames(item, out)


def collect_rendered_references(doc: Any, out: set[str]) -> None:
    """Collect src basenames ONLY from the top-level arrays CaseFilm actually renders on screen
    (RENDERED_SRC_ARRAYS). A src that lives anywhere else in the cutlist — a decoy array, a pool
    manifest, dead metadata — is intentionally NOT collected, so a clip cannot be counted as "used"
    unless a rendered shot points at it. This is the junk-array-hole close."""
    if not isinstance(doc, dict):
        return
    for key in RENDERED_SRC_ARRAYS:
        arr = doc.get(key)
        if isinstance(arr, list):
            for item in arr:
                collect_src_basenames(item, out)


def resolve_film_json(root: Path, slug: str, ep_name: str,
                      override: Optional[Path]) -> Optional[Path]:
    """Locate the cutlist for this episode. Prefer <slug>_film.json; else any *_film.json whose
    episode_id matches; else the public film_data snapshot. Returns None if nothing exists."""
    if override:
        return override if override.exists() else None
    direct = root / "remotion" / "src" / "data" / f"{slug}_film.json"
    if direct.exists():
        return direct
    data_dir = root / "remotion" / "src" / "data"
    if data_dir.exists():
        for cand in sorted(data_dir.glob("*_film.json")):
            d = _read_json(cand)
            if d and d.get("episode_id") == ep_name:
                return cand
    snapshot = root / "remotion" / "public" / slug / "film_data.v001.json"
    if snapshot.exists():
        return snapshot
    return None


def list_pool(folder: Path, exts: set[str]) -> list[str]:
    """Sorted basenames of media files (by extension) directly inside `folder`. [] if absent."""
    if not folder.is_dir():
        return []
    return sorted(p.name for p in folder.iterdir()
                  if p.is_file() and p.suffix.lower() in exts)


# ---------------------------------------------------------------------------------------------
# core evaluation (importable by check_final_acceptance)
# ---------------------------------------------------------------------------------------------

def evaluate(epdir: Path, *, root: Optional[Path] = None,
             film_json: Optional[Path] = None, public_dir: Optional[Path] = None,
             threshold: float = UTIL_THRESHOLD) -> dict[str, Any]:
    """Measure how much of the staged render pool the cutlist actually references.

    NEVER raises and NEVER calls sys.exit. Returns a dict with the stable contract:
      check, ok, hard, reason, and (when measured) utilization, footage_total/used/unused,
      img_total/used/unused, total, used, threshold, film_json, pool_dir.
    When the pool or cutlist is not in the repo (e.g. media on SSD) returns
      {ok: True, hard: False, skipped: True, reason: ...} so the caller stays green-neutral.
    """
    epdir = Path(epdir)
    root = Path(root) if root is not None else ROOT
    ep_name = epdir.name
    slug = slug_of(ep_name)

    film = film_json if film_json is not None else resolve_film_json(root, slug, ep_name, None)
    if film is None or not Path(film).exists():
        return {"check": GATE_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"cutlist not found (remotion/src/data/{slug}_film.json absent) — "
                          f"nothing to measure in-repo"}
    film = Path(film)

    pool_dir = Path(public_dir) if public_dir is not None else (root / "remotion" / "public" / slug)
    footage_pool = list_pool(pool_dir / "factory", VIDEO_EXTS)
    # Derived sidecars are NOT independent content stills and must not count toward the
    # "was it used on screen?" denominator: a `<name>_depth.png` displacement map reaches the
    # screen through its base image's DepthImage (path auto-derived via depthSrcOf, never a
    # standalone cut src), and a contact sheet is a QC artifact, not a render asset. Excluding
    # them only shrinks the denominator (utilization can rise, never fall) — no other episode can
    # newly fail. The 0.80 threshold is untouched.
    img_pool = [n for n in list_pool(pool_dir / "img", IMAGE_EXTS)
                if not n.lower().endswith("_depth.png")
                and not n.lower().startswith("contact_sheet")]

    if not footage_pool and not img_pool:
        return {"check": GATE_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"no staged pool found under {pool_dir} (media likely on SSD) — "
                          f"cannot measure utilization in-repo"}

    doc = _read_json(film)
    if doc is None:
        return {"check": GATE_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"cutlist {film} could not be parsed as JSON"}

    referenced: set[str] = set()
    collect_rendered_references(doc, referenced)

    footage_unused = [f for f in footage_pool if f not in referenced]
    img_unused = [f for f in img_pool if f not in referenced]
    footage_used = len(footage_pool) - len(footage_unused)
    img_used = len(img_pool) - len(img_unused)
    total = len(footage_pool) + len(img_pool)
    used = footage_used + img_used
    utilization = (used / total) if total else 0.0

    problems: list[str] = []
    # (1) the owner's exact defect: staged footage that the film never touches.
    if footage_pool and footage_unused:
        ex = ", ".join(footage_unused[:6]) + (" ..." if len(footage_unused) > 6 else "")
        problems.append(f"{len(footage_unused)}/{len(footage_pool)} staged footage clip(s) "
                        f"referenced 0 times: {ex}")
    # (2) most of the staged pool is dead weight.
    if total and utilization < threshold:
        problems.append(f"overall utilization {utilization*100:.0f}% "
                        f"({used}/{total}) < {threshold*100:.0f}% threshold")

    ok = not problems
    reason = ("all staged footage used; utilization "
              f"{utilization*100:.0f}% ({used}/{total})") if ok else "; ".join(problems)

    return {
        "check": GATE_NAME,
        "ok": ok,
        "hard": True,  # ship-blocking: an unused-footage film is the owner's real defect
        "reason": reason,
        "film_json": str(film),
        "pool_dir": str(pool_dir),
        "threshold": threshold,
        "utilization": round(utilization, 4),
        "total": total,
        "used": used,
        "footage_total": len(footage_pool),
        "footage_used": footage_used,
        "footage_unused": footage_unused,
        "img_total": len(img_pool),
        "img_used": img_used,
        "img_unused": img_unused,
    }


# ---------------------------------------------------------------------------------------------
# reporting / CLI
# ---------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("FOOTAGE UTILIZATION REPORT")
    print("=" * 78)
    print(f"  cutlist   : {r['film_json']}")
    print(f"  pool dir  : {r['pool_dir']}")
    print(f"  footage   : {r['footage_used']}/{r['footage_total']} staged clips referenced")
    print(f"  images    : {r['img_used']}/{r['img_total']} staged stills referenced")
    print(f"  overall   : {r['used']}/{r['total']} = {r['utilization']*100:.1f}% "
          f"(threshold {r['threshold']*100:.0f}%)")
    if r["footage_unused"]:
        print(f"\n  UNUSED FOOTAGE ({len(r['footage_unused'])}) — the owner's 'DL素材が使われない' defect:")
        for f in r["footage_unused"]:
            print(f"    - {f}")
    if r["img_unused"]:
        print(f"\n  unused images ({len(r['img_unused'])}) — informational, not a failure:")
        for f in r["img_unused"]:
            print(f"    - {f}")
    print("\n" + "-" * 78)
    print(f"  RESULT: {'PASS' if r['ok'] else 'FAIL'} — {r['reason']}")
    print("-" * 78)


def _atomic_write_json(path: Path, obj: dict[str, Any]) -> None:
    """Write JSON atomically (temp file in same dir + os.replace)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def _build_pool(troot: Path, slug: str, footage: list[str], imgs: list[str]) -> None:
    """Stage a synthetic render pool (factory footage + img stills) under troot."""
    pool = troot / "remotion" / "public" / slug
    (pool / "factory").mkdir(parents=True)
    (pool / "img").mkdir(parents=True)
    (troot / "remotion" / "src" / "data").mkdir(parents=True, exist_ok=True)
    for f in footage:
        (pool / "factory" / f).write_bytes(b"\x00")
    for f in imgs:
        (pool / "img" / f).write_bytes(b"\x00")


def _selftest() -> int:
    """(a) RED FIXTURE = the EXACT gaming probe: a pool whose downloaded footage is UNUSED, but the
        cutlist hides a reference to every clip inside a NON-rendered junk array to fake 100%
        utilization. The naive whole-tree collector is fooled (proved inline); the gate must FAIL.
    (b) GREEN case: a pool whose clips are genuinely placed in hook/cuts must PASS.
    (c) then run evaluate() on the real TEST EPISODE and print the actual numbers."""
    print("=" * 78)
    print("SELFTEST (a): RED FIXTURE — junk-array probe: unused footage hidden in an unrendered "
          "array to fake utilization must FAIL")
    print("=" * 78)
    with tempfile.TemporaryDirectory() as td:
        troot = Path(td)
        slug = "red"
        ep = "PD-2026-999-red"
        footage = [f"AF-BG-{i:04d}__clip.mp4" for i in range(5)]
        imgs = [f"PD-2026-999-S{i:03d}-IMG-{i:03d}.png" for i in range(1, 6)]
        _build_pool(troot, slug, footage, imgs)
        # Rendered arrays (hook/cuts) reference ONLY 1 image + 1 footage clip. The OTHER 4 footage
        # clips + 4 images are dead weight — but a DECOY array names every single staged clip so a
        # whole-tree "src anywhere" collector would score 100% and wave it through.
        film = {
            "episode_id": ep,
            "hook": [{"src": f"{slug}/img/{imgs[0]}"}],
            "cuts": [{"type": "footage", "src": f"{slug}/factory/{footage[0]}"}],
            # >>> the gaming payload: an unrendered junk array claiming every clip is "used" <<<
            "asset_pool": [{"src": f"{slug}/factory/{f}"} for f in footage]
                          + [{"src": f"{slug}/img/{i}"} for i in imgs],
        }
        _atomic_write_json(troot / "remotion" / "src" / "data" / f"{slug}_film.json", film)

        # Prove the probe truly exercises the hole: the naive whole-tree collector IS fooled.
        naive: set[str] = set()
        collect_src_basenames(film, naive)
        naive_all = all(f in naive for f in footage) and all(i in naive for i in imgs)
        print(f"  naive whole-tree collector sees all {len(naive)} clips as 'referenced' "
              f"(would fake 100%): {naive_all}")

        r = evaluate(troot / "episodes" / ep, root=troot)
        red_ok_false = (r.get("ok") is False) and not r.get("skipped")
        # the probe must be defeated for the RIGHT reason: the hidden footage is reported unused
        caught_unused = len(r.get("footage_unused") or []) == 4
        red_pass = red_ok_false and naive_all and caught_unused
        print(f"  ok={r.get('ok')}  skipped={r.get('skipped')}  reason={r.get('reason')}")
        print(f"  footage_unused={r.get('footage_unused')}  utilization={r.get('utilization')}")
        print(f"\n  RED-FIXTURE: {'PASS' if red_pass else 'FAIL'} "
              f"(gate {'correctly failed the gamed input' if red_pass else 'did NOT defeat the probe'})")

    print("\n" + "=" * 78)
    print("SELFTEST (b): GREEN case — clips genuinely placed in hook/cuts must PASS")
    print("=" * 78)
    green_pass = False
    with tempfile.TemporaryDirectory() as td:
        troot = Path(td)
        slug = "grn"
        ep = "PD-2026-998-grn"
        footage = [f"AF-BG-{i:04d}__clip.mp4" for i in range(4)]
        imgs = [f"PD-2026-998-S{i:03d}-IMG-{i:03d}.png" for i in range(1, 5)]
        _build_pool(troot, slug, footage, imgs)
        cuts = [{"type": "footage", "src": f"{slug}/factory/{f}"} for f in footage] \
             + [{"type": "still", "src": f"{slug}/img/{i}"} for i in imgs]
        film = {"episode_id": ep, "hook": [{"src": f"{slug}/img/{imgs[0]}"}], "cuts": cuts}
        _atomic_write_json(troot / "remotion" / "src" / "data" / f"{slug}_film.json", film)
        g = evaluate(troot / "episodes" / ep, root=troot)
        green_pass = (g.get("ok") is True) and not g.get("skipped") \
            and not (g.get("footage_unused") or [])
        print(f"  ok={g.get('ok')}  skipped={g.get('skipped')}  reason={g.get('reason')}")
        print(f"  GREEN-CASE: {'PASS' if green_pass else 'FAIL'}")

    print("\n" + "=" * 78)
    print(f"SELFTEST (c): REAL EPISODE — evaluate({DEFAULT_EP})")
    print("=" * 78)
    real = evaluate(ROOT / "episodes" / DEFAULT_EP)
    _print_report(real)

    return 0 if (red_pass and green_pass) else 1


def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(
        description="Footage-utilization gate: FAIL if staged footage is unused or utilization < ~80%.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug (PD-YYYY-NNN-name)")
    ap.add_argument("--dry-run", action="store_true",
                    help="resolve paths and print what WOULD be measured, then exit 0")
    ap.add_argument("--json", default=None, metavar="PATH",
                    help="also write the raw result dict to PATH (atomic)")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED-FIXTURE self-check then evaluate the real test episode")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    ep_dir = ROOT / "episodes" / args.ep
    if not ep_dir.exists():
        print(f"[ERROR] episode dir not found: {ep_dir}")
        return 1

    if args.dry_run:
        slug = slug_of(args.ep)
        film = resolve_film_json(ROOT, slug, args.ep, None)
        pool_dir = ROOT / "remotion" / "public" / slug
        print(f"[DRY-RUN] episode : {args.ep}")
        print(f"[DRY-RUN] slug    : {slug}")
        print(f"[DRY-RUN] cutlist : {film if film else '(not found in repo)'}")
        print(f"[DRY-RUN] pool    : {pool_dir}")
        print(f"[DRY-RUN]   factory clips: {len(list_pool(pool_dir / 'factory', VIDEO_EXTS))}")
        print(f"[DRY-RUN]   img stills   : {len(list_pool(pool_dir / 'img', IMAGE_EXTS))}")
        print("[DRY-RUN] no measurement performed; exit 0")
        return 0

    r = evaluate(ep_dir)
    _print_report(r)
    if args.json:
        _atomic_write_json(Path(args.json), r)
        print(f"\n[json] wrote {args.json}")

    if r.get("skipped"):
        return 3
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
