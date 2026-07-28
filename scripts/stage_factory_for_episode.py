#!/usr/bin/env python
"""Stage real factory footage into remotion/public/<slug>/factory/ for an episode.

Wraps the existing, ledger-backed `select_factory_assets.py` (never re-implements selection:
that tool already corrects the 40%-wrong filename labels, honours --exclude-used for
cross-episode footage diversity, and emits the labelled contact sheet that makes the
mandatory eyeball QC possible). This script only PLANS the theme mix, COPIES, and
CONTENT-CHECKS.

WHY IT CONTENT-CHECKS ON COPY (failure F-14): EP52 morton had 227 of 240 staged factory
clips written as ~11KB, 2.6s, luma-1.0 BLACK video. They passed every filename and count
check and would have gone straight into the film. Here a clip is only staged after a decoded
frame proves it has picture.

Usage:
  py -3.11 scripts/stage_factory_for_episode.py --slug morton \\
      --plan legal_court:60,crime_police:45,documents_paper:35,urban_night:30,atmosphere_symbolic:30 \\
      [--exclude-used] [--dry-run]

Nothing existing is deleted: previously staged files stay where they are. Anything unusable
is simply not referenced, because the manifest builder re-derives the pool from content.
"""
from __future__ import annotations

import argparse
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "remotion" / "public"
MEDIA_FACTORY_ROOT = Path("H:/pd-media/assets")
SELECTOR = ROOT / "scripts" / "select_factory_assets.py"
MIN_OK_BYTES = 50_000
MIN_LUMA = 8.0
OVERSELECT = 2.0            # ask for more than needed; dark/dup/missing ones are dropped
OVERLAY_CLASS_PREFIXES = ("AF-LIGHT", "AF-PART", "AF-VFX")   # screen-blend plates, not b-roll

# Ledger tiers worth staging. `weak` means the ledger could NOT recover a real provider title
# for the file, so its theme is still just the download QUERY -- and the download query is the
# thing that is 40% wrong. Measured on legal_court (2026-07-29): every tier=match item was
# genuinely on-theme ("scale of justice", "lady justice statue", "a serious lawyer"), while the
# tier=weak items all carried recovered_title "id" and turned out to be a BMW dashboard, a wine
# glass, a Byzantine church, a bedroom, a ski lodge and a Christmas dinner table -- all labelled
# `courtroom_interior`. Ten of ten were wrong. Never stage `weak`.
GOOD_TIERS = ("match", "match:dual_subject", "cross_theme->here")
UNKNOWN_TITLES = {"", "id", "none", "null"}


def sample_times(path: Path) -> list[float]:
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", str(path)], capture_output=True, text=True, timeout=30)
        d = float(r.stdout.strip() or 0)
    except Exception:
        d = 0.0
    if d <= 0:
        return [0.5]
    return [min(0.15, d * 0.05), d * 0.5, max(0.0, d - 0.15)]

EPISODES = {p.name.split("-", 3)[-1]: p.name for p in sorted((ROOT / "episodes").glob("PD-*"))}


def mean_luma(path: Path, at: float = 0.5) -> float:
    try:
        from PIL import Image
    except ImportError:
        return -1.0
    try:
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{at}", "-i", str(path),
                            "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                           capture_output=True, timeout=60)
        if not r.stdout:
            return -1.0
        b = Image.open(io.BytesIO(r.stdout)).convert("L").resize((64, 36)).tobytes()
        return sum(b) / len(b)
    except Exception:
        return -1.0


def select(theme: str, limit: int, ep: str, exclude_used: bool, by_subtype: bool = False) -> list[dict]:
    flag = "--subtype" if by_subtype else "--theme"
    cmd = [sys.executable, str(SELECTOR), flag, theme, "--kind", "video",
           "--limit", str(limit), "--json", "--no-sheet"]
    if ep:
        cmd += ["--ep", ep]
    if exclude_used:
        cmd += ["--exclude-used"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = r.stdout or ""
    # The selector prints banners that also contain "[" (e.g. "[theme=legal_court] ledger
    # tiers: ..."), so anchor on a line that is exactly "[" -- the start of the JSON array.
    lines = out.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.strip() == "["), None)
    if start is None:
        print(f"  [warn] selector returned no JSON for theme {theme}: {(r.stderr or out)[-200:]}")
        return []
    try:
        return json.loads("\n".join(lines[start:]))
    except json.JSONDecodeError as e:
        print(f"  [warn] selector JSON unparseable for {theme}: {e}")
        return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--plan", required=True,
                    help="name:count,... of THEMES, or of SUBTYPES with --by-subtype")
    ap.add_argument("--by-subtype", action="store_true",
                    help="--plan names are subtypes (e.g. police_interrogation_room_empty:20). "
                         "Themes are too coarse to match a case: on EP54 they returned big-city "
                         "skylines and 18th-century quills for a 1996 small-town Mississippi "
                         "story. Curate subtypes from FACTORY_SUBTYPE_INVENTORY.v001.md, which "
                         "lists each subtype's match-verdict count and its REAL sample titles.")
    ap.add_argument("--exclude-used", action="store_true",
                    help="skip clips already used by other episodes (footage diversity)")
    ap.add_argument("--allow-weak", action="store_true",
                    help="also stage tier=weak items (their theme is the unverified download "
                         "query; 10/10 sampled were off-topic). Not recommended.")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    ep = EPISODES.get(a.slug)
    if not ep:
        raise SystemExit(f"unknown slug {a.slug}")
    dest = PUBLIC / a.slug / "factory"
    if not a.dry_run:
        dest.mkdir(parents=True, exist_ok=True)

    plan: list[tuple[str, int]] = []
    for part in a.plan.split(","):
        theme, _, n = part.partition(":")
        plan.append((theme.strip(), int(n)))

    already = {p.name for p in dest.iterdir()} if dest.is_dir() else set()
    staged_total = dark = missing = dup = overlay_class = weak_dropped = 0
    per_theme: dict[str, int] = {}

    for theme, want in plan:
        rows = select(theme, int(want * OVERSELECT * 3) + 20, ep, a.exclude_used, a.by_subtype)
        n_raw = len(rows)
        if not a.allow_weak:
            rows = [r for r in rows
                    if r.get("tier") in GOOD_TIERS
                    and str(r.get("recovered_title") or "").strip().lower() not in UNKNOWN_TITLES]
            weak_dropped += n_raw - len(rows)
        got = 0
        for row in rows:
            if got >= want:
                break
            rel = str(row.get("path") or "")
            src = MEDIA_FACTORY_ROOT / rel
            if not src.exists():
                missing += 1
                continue
            name = src.name
            if name in already:
                dup += 1
                continue
            # AF-LIGHT / AF-PART / AF-VFX are screen-blend plates, not b-roll. EP54's whole
            # 218-clip cut pool was these, so most of the film's "video" was abstract light
            # effects. Never stage them as footage.
            if any(k in name for k in OVERLAY_CLASS_PREFIXES):
                overlay_class += 1
                continue
            if src.stat().st_size < MIN_OK_BYTES:
                dark += 1
                continue
            # head/mid/tail: a clip that fades to black at an end is a black hole as a cut
            lums = [x for x in (mean_luma(src, t) for t in sample_times(src)) if x >= 0]
            if not lums or min(lums) < MIN_LUMA:
                dark += 1
                continue
            if a.dry_run:
                got += 1
                already.add(name)
                continue
            shutil.copy2(src, dest / name)
            already.add(name)
            got += 1
        per_theme[theme] = got
        staged_total += got
        print(f"  {theme:<22} staged {got}/{want}  (candidates {len(rows)})")

    print(f"[{a.slug}] factory staged={staged_total} "
          f"(skipped: weak-tier={weak_dropped} dark/stub={dark} overlay-class={overlay_class} "
          f"missing={missing} already-present={dup})")
    print(f"[{a.slug}] per-theme: {per_theme}")
    if a.dry_run:
        print("(dry-run) nothing copied")
    else:
        print(f"NEXT: py -3.11 scripts/build_asset_manifest_motionfirst.py --slug {a.slug}")
        print(f"      then py -3.11 scripts/pd_preflight.py --slug {a.slug}")
    print("REMINDER: the audited labels are ~70% right. Eyeball the contact sheet for this "
          "episode's factory pool before it ships (scripts/build_footage_contact_sheet.py).")
    return 0 if staged_total else 1


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
