#!/usr/bin/env python3
r"""Independent VISUAL-ASSET QC gate — catches a MISLABELED factory clip and a DARK/SAMEY hero-still
set BEFORE ship. Standalone module; check_final_acceptance wires it via ``evaluate(epdir)``.

WHY THIS EXISTS (EP36 williams post-mortem)
-------------------------------------------
EP36 shipped with a MISLABELED factory b-roll clip in the VERY FIRST shot: the file was named
``AF-BG-25521__city_surveillance_camera_dome.mp4`` but the footage was actually a Belgrade Orthodox
CATHEDRAL — an off-theme dome that read as a religious building, not surveillance tech. The b-roll
selection trusted the FILENAME/subtype label and skipped the mandatory per-clip visual QC, so nothing
ever looked at the pixels. Separately, the AI-generated hero stills for the case are chronically too
DARK (crushed, unreadable subject) and too SAMEY (a set of near-identical moody frames). None of the
existing acceptance gates catch either failure. This is that gate.

DESIGN PRINCIPLE — ENFORCE that QC HAPPENED, don't fake vision in pure code
---------------------------------------------------------------------------
A real vision model may be unavailable at gate runtime, and we must NEVER trust a factory filename
again. So for the factory clips the gate does NOT try to judge content from Python; it REQUIRES a
human/vision-reviewed clip-QC MANIFEST that records, per clip, WHAT THE REVIEWER ACTUALLY SAW and an
``on_theme`` verdict — and FAILS if any staged clip is missing from the manifest or is not marked
reviewed+on_theme. As a build convenience the module can GENERATE a contact sheet (one representative
frame per staged clip, via ffmpeg) so a human/vision reviewer can fill the manifest quickly.

For the hero STILLS the gate measures the ACTUAL staged PNGs (remotion/public/<slug>/img/*.png), not
any stale film_data json: per-still median luma (darkness) + a perceptual-hash near-duplicate score
(variety). These are cheap, objective pixel stats — no content judgement — so they run in pure code.

WHAT IT CHECKS (two independent HARD sub-checks; either can fail the gate)
-------------------------------------------------------------------------
1. FACTORY-CLIP QC MANIFEST REQUIRED. The staged factory clips are the video files physically in
   ``remotion/public/<slug>/factory/`` (ground truth — we do NOT trust film_data, which may be stale,
   nor the filenames, which is exactly what burned EP36). The gate requires a reviewed manifest at
   ``episodes/<ep>/05_visuals/factory_clip_qc.v*.json`` (latest version wins) that lists EVERY staged
   clip with ``reviewed: true`` + ``on_theme: true``. FAIL if any staged clip is missing from the
   manifest (unreviewed) or is present but not on_theme (e.g. ``on_theme:false`` / ``verdict:reject``
   — a rejected clip must be REMOVED from the staging dir, not left in). No factory dir -> that
   sub-check is skipped (non-blocking); no manifest while clips ARE staged -> FAIL.

2. STAGED-STILL LUMA + VARIETY. Over remotion/public/<slug>/img/*.png (excluding ``*_depth.png``
   depth maps): compute each still's median luma; a still is "dark" if median luma < DARK_LUMA_FLOOR.
   FAIL if the dark fraction exceeds MAX_DARK_FRACTION. Compute a perceptual-hash near-duplicate score
   (16x16 zero-mean grayscale cosine similarity between every pair); a still is a "near-dup" if its
   peak similarity to any other still >= NEARDUP_SIM. variety_score = 1 - near_dup_fraction. FAIL if
   variety_score < MIN_VARIETY. No stills -> this sub-check is skipped (non-blocking).

CALIBRATION (measured 2026-07-11 over all remotion/public/<slug>/img/*.png)
---------------------------------------------------------------------------
Per-still median luma on a 0-255 scale (PIL "L"), resized to 64x64; dark = median luma < 45.
  slug         n   med-luma  dark%   max-pair-sim   variety   note
  williams <-  30   36.0     76.7%   0.725          1.00      EP36 reject (brightest of the batch, still 77% dark)
  cotton       40   22.5     87.5%   0.739          1.00
  hinton       40   17.7     85.0%   0.778          1.00
  hinders      68   20.8     89.7%   0.855          1.00
  rolin        68   17.9     95.6%   0.692          1.00      (animation-rich ref, but stills still very dark)
  tyler        68   17.9     95.6%   0.762          1.00      (animation-rich ref, but stills still very dark)
  carsearch    40   14.8    100.0%   0.737          1.00      (animation-rich ref, but stills still very dark)
  unlock       42   12.2     97.6%   1.000          0.81      has 4 true duplicate pairs (near-dup flagged)
The whole current back-catalogue trends TOO DARK — a systemic AI-still exposure problem the owner
flagged. The DARK_LUMA_FLOOR = 45 is a forward-looking quality bar: a documentary hero still should
have a readable subject (median luma >= 45). williams has 76.7% of stills below it (>> the 40% dark
allowance) -> FAIL on darkness. Its stills are NOT near-duplicates (peak pair-sim 0.725 < 0.90), so it
PASSES variety and fails on darkness + the missing manifest — the expected EP36 verdict. NEARDUP_SIM =
0.90 sits above the busiest legitimate pair (rodriguez 0.857) and below the true dups (unlock 1.000).
MIN_VARIETY = 0.60 fails a set where >40% of stills have a near-twin (a genuinely samey batch); the
GREEN selftest fixture uses properly-exposed, distinct stills to prove the gate PASSES when the stills
are good.

Usage:
  py -3.11 scripts/check_visual_asset_qc.py --ep PD-2026-036-williams
  py -3.11 scripts/check_visual_asset_qc.py --ep williams --contact-sheet   # build the review sheet
  py -3.11 scripts/check_visual_asset_qc.py --selftest                      # RED (fail) + GREEN (pass)

Exit codes: 0 = PASS (or artifact-absent skip), 1 = FAIL / usage error.

check_final_acceptance imports this module and calls ``evaluate(epdir)``; the returned dict keys
(check / ok / hard / reason / skipped / factory / stills / floors) are the stable contract.
``evaluate`` NEVER calls sys.exit and never raises on missing inputs — it returns a skip dict so the
caller cannot crash.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

try:
    import numpy as np
    from PIL import Image, ImageDraw
    _HAVE_IMAGING = True
except Exception:  # noqa: BLE001 - imaging stack absent -> stills sub-check skips gracefully
    _HAVE_IMAGING = False

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIR = ROOT / "remotion" / "public"
DEFAULT_EP = "PD-2026-036-williams"
CHECK_NAME = "visual_asset_qc"

# ---- HARD thresholds (see the module docstring CALIBRATION table for the measured numbers) --------
DARK_LUMA_FLOOR = 45.0     # per-still median luma (0-255); below this a hero still is "too dark"
MAX_DARK_FRACTION = 0.40   # FAIL if more than this fraction of stills are dark (williams 0.767)
NEARDUP_SIM = 0.90         # 16x16 zero-mean grayscale cosine; >= this => two stills are near-duplicates
MIN_VARIETY = 0.60         # variety_score = 1 - near_dup_fraction; FAIL below this (williams 1.00)

VIDEO_EXTS = (".mp4", ".mov", ".webm", ".mkv", ".m4v")
_LUMA_SIZE = 64            # stills resized to 64x64 for the median-luma measurement
_PHASH_SIZE = 16           # stills resized to 16x16 for the perceptual-hash similarity measurement


# ------------------------------------------------------------------------------------------------
# path resolution
# ------------------------------------------------------------------------------------------------

def _slug_of(name: str) -> str:
    """Episode folder / id -> public-asset slug (strip a leading PD-YYYY-NNN- prefix), mirroring
    check_final_acceptance so this gate resolves the SAME remotion/public/<slug>/ pool."""
    return re.sub(r"^PD-\d{4}-\d{3}-", "", str(name))


def _load(p: Path) -> Optional[dict[str, Any]]:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 - unreadable/malformed json -> treat as absent
        return None
    return d if isinstance(d, dict) else None


def resolve_manifest(epdir: Path) -> Optional[Path]:
    """Latest episodes/<ep>/05_visuals/factory_clip_qc.v*.json, or None."""
    cands = sorted((epdir / "05_visuals").glob("factory_clip_qc.v*.json"))
    return cands[-1] if cands else None


def staged_factory_clips(factory_dir: Path) -> list[Path]:
    """The factory video files physically staged in remotion/public/<slug>/factory/ (ground truth —
    we enumerate real files rather than trust film_data or the filenames' semantics)."""
    if not factory_dir.is_dir():
        return []
    return sorted(p for p in factory_dir.iterdir()
                  if p.is_file() and p.suffix.lower() in VIDEO_EXTS)


def staged_stills(img_dir: Path) -> list[Path]:
    """The hero-still PNGs in remotion/public/<slug>/img/, excluding *_depth.png depth maps."""
    if not img_dir.is_dir():
        return []
    return sorted(p for p in img_dir.glob("*.png") if not p.name.endswith("_depth.png"))


# ------------------------------------------------------------------------------------------------
# sub-check 1: factory-clip QC manifest
# ------------------------------------------------------------------------------------------------

def _norm_verdict_entry(e: dict[str, Any]) -> tuple[bool, bool]:
    """Return (reviewed, on_theme) for a manifest clip entry, tolerant of a few spellings.
    A clip counts as on_theme ONLY if reviewed is true, on_theme is true, and it is not rejected."""
    reviewed = bool(e.get("reviewed"))
    verdict = str(e.get("verdict") or "").strip().lower()
    if verdict in {"reject", "rejected", "off_theme", "off-theme"}:
        return reviewed, False
    if verdict in {"accept", "accepted", "keep", "on_theme", "on-theme", "approved"}:
        return reviewed, True
    # fall back to the boolean on_theme field
    return reviewed, bool(e.get("on_theme"))


def evaluate_factory(factory_dir: Path, manifest_path: Optional[Path]) -> dict[str, Any]:
    """Require a reviewed clip-QC manifest that clears EVERY staged factory clip as on_theme."""
    staged = staged_factory_clips(factory_dir)
    if not staged:
        return {"skipped": True, "ok": True,
                "reason": f"no staged factory clips under {factory_dir} — factory QC not applicable",
                "staged_count": 0}

    staged_names = [p.name for p in staged]
    if manifest_path is None:
        return {"skipped": False, "ok": False,
                "reason": (f"no clip-QC manifest (episodes/<ep>/05_visuals/factory_clip_qc.v*.json) "
                           f"— per-clip visual QC was SKIPPED for {len(staged)} staged factory clips; "
                           f"filenames are NOT trusted (EP36 mislabel). Run --contact-sheet, then fill "
                           f"the manifest."),
                "staged_count": len(staged), "manifest": None,
                "unreviewed": staged_names, "off_theme": []}

    man = _load(manifest_path)
    entries: dict[str, dict[str, Any]] = {}
    if man and isinstance(man.get("clips"), list):
        for e in man["clips"]:
            if isinstance(e, dict) and e.get("filename"):
                entries[str(e["filename"])] = e

    unreviewed: list[str] = []
    off_theme: list[str] = []
    reviewed_ok: list[str] = []
    for name in staged_names:
        e = entries.get(name)
        if e is None:
            unreviewed.append(name)
            continue
        reviewed, on_theme = _norm_verdict_entry(e)
        if not reviewed:
            unreviewed.append(name)
        elif not on_theme:
            off_theme.append(name)
        else:
            reviewed_ok.append(name)

    # clips recorded in the manifest but no longer staged (e.g. rejected + removed) — informational
    extra = sorted(set(entries) - set(staged_names))

    if unreviewed or off_theme:
        parts = []
        if off_theme:
            parts.append(f"{len(off_theme)} staged clip(s) marked OFF-THEME/rejected but still in the "
                         f"factory dir: {off_theme[:5]}")
        if unreviewed:
            parts.append(f"{len(unreviewed)} staged clip(s) NOT reviewed in the manifest: "
                         f"{unreviewed[:5]}")
        return {"skipped": False, "ok": False, "reason": "; ".join(parts),
                "staged_count": len(staged), "manifest": str(manifest_path),
                "reviewed_ok": len(reviewed_ok), "unreviewed": unreviewed, "off_theme": off_theme,
                "manifest_only": extra}
    return {"skipped": False, "ok": True,
            "reason": f"all {len(staged)} staged factory clips reviewed + on_theme in "
                      f"{manifest_path.name}",
            "staged_count": len(staged), "manifest": str(manifest_path),
            "reviewed_ok": len(reviewed_ok), "unreviewed": [], "off_theme": [],
            "manifest_only": extra}


# ------------------------------------------------------------------------------------------------
# sub-check 2: staged-still luma + variety
# ------------------------------------------------------------------------------------------------

def _still_features(p: Path) -> Optional[tuple[float, "np.ndarray"]]:
    """(median_luma, phash_vector) for a still, or None if it can't be read.
    median_luma: median of the 64x64 grayscale (PIL 'L' = ITU-R 601 luma), 0-255.
    phash_vector: 16x16 grayscale, zero-mean, L2-normalized (so a dot product == cosine similarity)."""
    try:
        g = Image.open(p).convert("L")
    except Exception:  # noqa: BLE001
        return None
    small = np.asarray(g.resize((_LUMA_SIZE, _LUMA_SIZE)), dtype=np.float64)
    med = float(np.median(small))
    ph = np.asarray(g.resize((_PHASH_SIZE, _PHASH_SIZE)), dtype=np.float64).flatten()
    ph = ph - ph.mean()
    n = np.linalg.norm(ph)
    ph = ph / n if n > 0 else ph
    return med, ph


def evaluate_stills(img_dir: Path) -> dict[str, Any]:
    """Median-luma darkness + perceptual-hash variety over the staged hero stills."""
    if not _HAVE_IMAGING:
        return {"skipped": True, "ok": True, "reason": "numpy/PIL not available — stills QC skipped",
                "still_count": 0}
    stills = staged_stills(img_dir)
    if not stills:
        return {"skipped": True, "ok": True,
                "reason": f"no hero stills under {img_dir} — stills QC not applicable",
                "still_count": 0}

    lumas: list[float] = []
    vecs: list["np.ndarray"] = []
    dark_files: list[str] = []
    for p in stills:
        f = _still_features(p)
        if f is None:
            continue
        med, ph = f
        lumas.append(med)
        vecs.append(ph)
        if med < DARK_LUMA_FLOOR:
            dark_files.append(p.name)
    if not lumas:
        return {"skipped": True, "ok": True,
                "reason": f"no readable stills under {img_dir} — stills QC not applicable",
                "still_count": 0}

    n = len(lumas)
    larr = np.array(lumas)
    dark_fraction = float((larr < DARK_LUMA_FLOOR).mean())

    # perceptual-hash near-duplicate detection: peak cosine similarity of each still to any OTHER still.
    V = np.vstack(vecs)                 # (n, 256) unit rows
    S = V @ V.T                         # (n, n) cosine-similarity matrix
    np.fill_diagonal(S, -1.0)           # ignore self-similarity
    peak = S.max(axis=1) if n > 1 else np.array([-1.0])
    near_dup_mask = peak >= NEARDUP_SIM
    near_dup_fraction = float(near_dup_mask.mean()) if n > 1 else 0.0
    variety_score = round(1.0 - near_dup_fraction, 3)
    max_pair_sim = float(peak.max()) if n > 1 else 0.0
    mean_pair_sim = float(S[np.triu_indices(n, 1)].mean()) if n > 1 else 0.0

    problems: list[str] = []
    if dark_fraction > MAX_DARK_FRACTION:
        problems.append(f"{dark_fraction*100:.1f}% of {n} stills are too dark (median luma < "
                        f"{DARK_LUMA_FLOOR:.0f}) > {MAX_DARK_FRACTION*100:.0f}% allowance")
    if variety_score < MIN_VARIETY:
        problems.append(f"variety {variety_score:.2f} < {MIN_VARIETY:.2f} "
                        f"({int(round(near_dup_fraction*n))}/{n} stills are near-duplicates "
                        f"(pair-sim >= {NEARDUP_SIM})")

    common = {
        "skipped": False, "still_count": n,
        "dark_fraction": round(dark_fraction, 3), "dark_count": len(dark_files),
        "dark_files": dark_files[:10],
        "median_luma_overall": round(float(np.median(larr)), 1),
        "min_luma": round(float(larr.min()), 1), "max_luma": round(float(larr.max()), 1),
        "variety_score": variety_score, "near_dup_count": int(near_dup_mask.sum()),
        "max_pair_sim": round(max_pair_sim, 3), "mean_pair_sim": round(mean_pair_sim, 3),
    }
    if problems:
        return {**common, "ok": False, "reason": "; ".join(problems)}
    return {**common, "ok": True,
            "reason": (f"stills OK: {dark_fraction*100:.1f}% dark (<= {MAX_DARK_FRACTION*100:.0f}%), "
                       f"variety {variety_score:.2f} (>= {MIN_VARIETY:.2f})")}


# ------------------------------------------------------------------------------------------------
# core evaluation (importable by check_final_acceptance)
# ------------------------------------------------------------------------------------------------

def evaluate(epdir: Path, *, public_root: Optional[Path] = None) -> dict[str, Any]:
    """Visual-asset QC gate. ``epdir`` is the episode directory (its ``.name`` is the episode id,
    e.g. ``episodes/PD-2026-036-williams``). NEVER raises, NEVER calls sys.exit.

    Two independent HARD sub-checks — the gate FAILS if EITHER fails:
      1. factory: a reviewed clip-QC manifest must clear every staged factory clip as on_theme.
      2. stills : the staged hero stills must not be mostly-dark or mostly near-duplicates.
    A sub-check whose inputs are absent is SKIPPED (non-blocking). If BOTH sub-checks are skipped the
    whole gate is a non-blocking skip.

    Returns a dict compatible with check_final_acceptance:
      {"check", "ok", "hard", "reason", "factory": {...}, "stills": {...}, "floors": {...},
       optional "skipped"}."""
    epdir = Path(epdir)
    public_root = Path(public_root) if public_root is not None else PUBLIC_DIR
    slug = _slug_of(epdir.name)
    pub = public_root / slug
    factory_dir = pub / "factory"
    img_dir = pub / "img"

    factory = evaluate_factory(factory_dir, resolve_manifest(epdir))
    stills = evaluate_stills(img_dir)

    floors = {
        "dark_luma_floor": DARK_LUMA_FLOOR, "max_dark_fraction": MAX_DARK_FRACTION,
        "neardup_sim": NEARDUP_SIM, "min_variety": MIN_VARIETY,
    }

    # whole-gate skip only if BOTH sub-checks had no inputs to look at
    if factory.get("skipped") and stills.get("skipped"):
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"no factory clips and no hero stills under {pub} — nothing to QC",
                "factory": factory, "stills": stills, "floors": floors}

    problems: list[str] = []
    if not factory.get("skipped") and not factory.get("ok"):
        problems.append("FACTORY: " + factory["reason"])
    if not stills.get("skipped") and not stills.get("ok"):
        problems.append("STILLS: " + stills["reason"])

    common = {"check": CHECK_NAME, "hard": True, "factory": factory, "stills": stills,
              "floors": floors, "episode_id": epdir.name, "public_dir": str(pub)}
    if problems:
        return {**common, "ok": False, "reason": "visual-asset QC failed — " + " | ".join(problems)}
    ok_bits = []
    if not factory.get("skipped"):
        ok_bits.append(f"factory: {factory['reason']}")
    if not stills.get("skipped"):
        ok_bits.append(f"stills: {stills['reason']}")
    return {**common, "ok": True, "reason": "visual-asset QC OK — " + " | ".join(ok_bits)}


# ------------------------------------------------------------------------------------------------
# contact-sheet builder (human/vision-review convenience — NOT part of the gate verdict)
# ------------------------------------------------------------------------------------------------

def _ffmpeg() -> Optional[str]:
    return shutil.which("ffmpeg")


def _extract_frame(ffmpeg: str, clip: Path, out_png: Path, at: float, width: int) -> bool:
    try:
        r = subprocess.run(
            [ffmpeg, "-y", "-ss", f"{at:.2f}", "-i", str(clip), "-frames:v", "1",
             "-vf", f"scale={width}:-1", str(out_png)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
        return r.returncode == 0 and out_png.is_file()
    except Exception:  # noqa: BLE001
        return False


def build_contact_sheet(epdir: Path, *, public_root: Optional[Path] = None,
                        cols: int = 5, thumb_w: int = 320, at: float = 0.6) -> dict[str, Any]:
    """Extract one representative frame per staged factory clip (via ffmpeg) and tile them into
    episodes/<ep>/05_visuals/factory_contactsheet.png with each clip's FILENAME captioned under its
    frame, so a human/vision reviewer can eyeball the pixels and fill the clip-QC manifest. This is a
    build convenience and does NOT affect the gate verdict."""
    epdir = Path(epdir)
    public_root = Path(public_root) if public_root is not None else PUBLIC_DIR
    slug = _slug_of(epdir.name)
    factory_dir = public_root / slug / "factory"
    clips = staged_factory_clips(factory_dir)
    out = epdir / "05_visuals" / "factory_contactsheet.png"

    if not _HAVE_IMAGING:
        return {"ok": False, "reason": "numpy/PIL not available — cannot compose contact sheet"}
    if not clips:
        return {"ok": False, "reason": f"no staged factory clips under {factory_dir}"}
    ff = _ffmpeg()
    if not ff:
        return {"ok": False, "reason": "ffmpeg not found on PATH — cannot extract frames"}

    pad, cap_h, bg = 8, 22, (18, 18, 20)
    tiles: list[tuple[str, "Image.Image"]] = []
    failed: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        for i, clip in enumerate(clips):
            fp = Path(td) / f"f{i:03d}.png"
            if _extract_frame(ff, clip, fp, at, thumb_w):
                try:
                    tiles.append((clip.name, Image.open(fp).convert("RGB").copy()))
                    continue
                except Exception:  # noqa: BLE001
                    pass
            failed.append(clip.name)
            ph = Image.new("RGB", (thumb_w, thumb_w * 9 // 16), (60, 20, 20))
            tiles.append((clip.name + "  [FRAME EXTRACT FAILED]", ph))

    if not tiles:
        return {"ok": False, "reason": "no frames could be extracted from any clip"}

    tw = max(im.width for _, im in tiles)
    th = max(im.height for _, im in tiles)
    rows = (len(tiles) + cols - 1) // cols
    cell_w = tw + pad * 2
    cell_h = th + cap_h + pad * 2
    sheet = Image.new("RGB", (cell_w * cols, cell_h * rows), bg)
    draw = ImageDraw.Draw(sheet)
    for idx, (name, im) in enumerate(tiles):
        r, c = divmod(idx, cols)
        x, y = c * cell_w + pad, r * cell_h + pad
        sheet.paste(im, (x, y))
        label = name if len(name) <= 46 else name[:43] + "..."
        draw.text((x, y + th + 4), f"{idx+1}. {label}", fill=(220, 220, 220))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    return {"ok": True, "path": str(out), "clips": len(clips), "extracted": len(clips) - len(failed),
            "failed": failed, "reason": f"contact sheet: {len(clips) - len(failed)}/{len(clips)} "
                                        f"frames -> {out}"}


# ------------------------------------------------------------------------------------------------
# reporting / CLI / selftest
# ------------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("VISUAL-ASSET QC REPORT")
    print("=" * 78)
    print(f"  episode   : {r.get('episode_id')}")
    print(f"  public    : {r.get('public_dir')}")
    f, s = r.get("factory", {}), r.get("stills", {})
    print("-" * 78)
    print("  FACTORY-CLIP QC MANIFEST")
    if f.get("skipped"):
        print(f"    [skip] {f.get('reason')}")
    else:
        print(f"    staged clips : {f.get('staged_count')}   manifest: {f.get('manifest')}")
        print(f"    reviewed_ok  : {f.get('reviewed_ok', 0)}  "
              f"unreviewed: {len(f.get('unreviewed', []))}  off_theme: {len(f.get('off_theme', []))}")
        print(f"    {'OK' if f.get('ok') else 'FAIL'}: {f.get('reason')}")
    print("-" * 78)
    print("  STAGED-STILL LUMA + VARIETY")
    if s.get("skipped"):
        print(f"    [skip] {s.get('reason')}")
    else:
        print(f"    stills       : {s.get('still_count')}   "
              f"median luma overall: {s.get('median_luma_overall')} "
              f"(min {s.get('min_luma')}, max {s.get('max_luma')})")
        print(f"    dark fraction: {s.get('dark_fraction', 0)*100:.1f}%  "
              f"({s.get('dark_count')} stills < luma {DARK_LUMA_FLOOR:.0f})  "
              f"[floor {MAX_DARK_FRACTION*100:.0f}%]")
        print(f"    variety score: {s.get('variety_score')}  "
              f"(near-dups {s.get('near_dup_count')}, max pair-sim {s.get('max_pair_sim')}, "
              f"mean {s.get('mean_pair_sim')})  [floor {MIN_VARIETY}]")
        print(f"    {'OK' if s.get('ok') else 'FAIL'}: {s.get('reason')}")
    print("-" * 78)
    print(f"  RESULT: {'PASS' if r.get('ok') else 'FAIL'}  — {r.get('reason')}")
    print("-" * 78)


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False, default=str)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def _make_still(path: Path, base: int, seed: int) -> None:
    """Write a synthetic PNG whose median luma ~= base with a distinct per-seed pattern (for the
    GREEN/RED selftest fixtures — bright+varied vs dark+samey)."""
    rng = np.random.default_rng(seed)
    h, w = 180, 320
    img = np.full((h, w, 3), base, dtype=np.float64)
    # distinct low-frequency structure per seed so the fixtures are genuinely different images
    yy, xx = np.mgrid[0:h, 0:w]
    fx, fy = 1 + seed % 5, 1 + (seed // 5) % 5
    img[..., seed % 3] += 30 * np.sin(2 * np.pi * (fx * xx / w + fy * yy / h) + seed)
    img += rng.normal(0, 6, img.shape)
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(path)


def _run_selftest() -> int:
    """(a) RED: a dark, samey still set + NO manifest MUST FAIL; (b) GREEN: bright, varied stills +
    a full reviewed manifest MUST PASS; (c) a real run on DEFAULT_EP."""
    if not _HAVE_IMAGING:
        print("numpy/PIL unavailable — cannot run the stills selftest fixtures")
        return 1

    print("=" * 78)
    print("SELFTEST (a): RED FIXTURE — dark + samey stills, NO manifest MUST fail")
    print("=" * 78)
    with tempfile.TemporaryDirectory() as td:
        troot = Path(td)
        pub = troot / "public"
        epdir = troot / "episodes" / "PD-9999-999-redtest"
        slug = "redtest"
        (pub / slug / "factory").mkdir(parents=True)
        (pub / slug / "img").mkdir(parents=True)
        (epdir / "05_visuals").mkdir(parents=True)
        # a staged factory clip with NO manifest -> factory sub-check must fail
        (pub / slug / "factory" / "AF-BG-0001__mislabeled_dome.mp4").write_bytes(b"\x00")
        # dark (base 18) + near-identical stills -> stills sub-check must fail on darkness (+ variety)
        for i in range(12):
            _make_still(pub / slug / "img" / f"S{i:03d}.png", base=18, seed=1)  # same seed => dupes
        red = evaluate(epdir, public_root=pub)
        red_ok = (red.get("ok") is False) and not red.get("skipped")
        _print_report(red)

        print("\n" + "=" * 78)
        print("SELFTEST (b): GREEN FIXTURE — bright + varied stills, full manifest MUST pass")
        print("=" * 78)
        pub2 = troot / "public2"
        epdir2 = troot / "episodes" / "PD-9999-998-greentest"
        slug2 = "greentest"
        (pub2 / slug2 / "factory").mkdir(parents=True)
        (pub2 / slug2 / "img").mkdir(parents=True)
        (epdir2 / "05_visuals").mkdir(parents=True)
        clip_names = [f"AF-BG-{i:04d}__scene_{i}.mp4" for i in range(3)]
        for cn in clip_names:
            (pub2 / slug2 / "factory" / cn).write_bytes(b"\x00")
        _atomic_write_json(epdir2 / "05_visuals" / "factory_clip_qc.v001.json", {
            "schema_version": "1.0.0", "episode_id": "PD-9999-998-greentest",
            "reviewed_by": "selftest-human", "reviewed_at": "2026-07-11",
            "clips": [{"filename": cn, "reviewed": True, "on_theme": True, "verdict": "accept",
                       "actual_content": f"what the reviewer SAW in {cn}"} for cn in clip_names],
        })
        # bright (base 150) + distinct per-seed patterns -> passes darkness AND variety
        for i in range(12):
            _make_still(pub2 / slug2 / "img" / f"S{i:03d}.png", base=150, seed=i + 1)
        green = evaluate(epdir2, public_root=pub2)
        green_ok = (green.get("ok") is True) and not green.get("skipped")
        _print_report(green)

    ok = red_ok and green_ok
    print(f"\nRED-FIXTURE:   {'PASS' if red_ok else 'FAIL'} "
          f"(gate {'correctly failed' if red_ok else 'DID NOT fail'} the dark/no-manifest fixture)")
    print(f"GREEN-FIXTURE: {'PASS' if green_ok else 'FAIL'} "
          f"(gate {'correctly passed' if green_ok else 'DID NOT pass'} the bright/reviewed fixture)")

    print("\n" + "=" * 78)
    print(f"SELFTEST (c): REAL run on {DEFAULT_EP}")
    print("=" * 78)
    _print_report(evaluate(ROOT / "episodes" / DEFAULT_EP))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(
        description="Independent VISUAL-ASSET QC gate: require a reviewed factory-clip QC manifest "
                    "(never trust filenames) and FAIL a dark / low-variety hero-still set.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode id or slug (e.g. PD-2026-036-williams)")
    ap.add_argument("--contact-sheet", action="store_true",
                    help="build episodes/<ep>/05_visuals/factory_contactsheet.png for manifest review")
    ap.add_argument("--dry-run", action="store_true", help="run and report, but always exit 0")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED (must fail) + GREEN (must pass) fixtures, then the real episode")
    ap.add_argument("--json", default=None, metavar="PATH", help="also write the raw result dict to PATH")
    args = ap.parse_args(argv)

    if args.selftest:
        return _run_selftest()

    epdir = ROOT / "episodes" / args.ep
    if args.contact_sheet:
        cs = build_contact_sheet(epdir)
        print(f"[contact-sheet] {'OK' if cs.get('ok') else 'FAIL'}: {cs.get('reason')}")

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
