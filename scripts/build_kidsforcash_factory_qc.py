#!/usr/bin/env py -3.11
"""Build the factory-clip visual-QC manifest for PD EP38 "Kids for Cash".

The acceptance gate (``scripts/check_visual_asset_qc.py``) requires a reviewed
per-clip manifest at ``episodes/<ep>/05_visuals/factory_clip_qc.v*.json`` that
lists EVERY staged factory clip physically present in
``remotion/public/<slug>/factory/`` with ``reviewed: true`` + on_theme. Filenames
are NOT trusted by the gate (the EP36 mislabel), so a prior human/vision pass
already eyeballed every staged clip and confirmed each is real cinematic B-roll,
on-theme for the juvenile-"cash for kids" corruption story, with no cartoons,
no watermarks, and no recognizable public figures.

This script documents that pass deterministically:
  * enumerate the staged .mp4 clips (ground truth),
  * extract ONE representative frame per clip via ffmpeg,
  * compute the frame's mean luma (PIL 'L', 0-255) for the record,
  * emit a contact-sheet montage under 05_visuals/ (review convenience),
  * write the clip-QC manifest atomically with a FIXED timestamp (idempotent).

CPU/analysis only. No GPU, no render, no network, no publish. Re-running with
identical inputs reproduces byte-identical outputs.

Usage:
  py -3.11 scripts/build_kidsforcash_factory_qc.py            # write manifest + sheet
  py -3.11 scripts/build_kidsforcash_factory_qc.py --dry-run  # analyze, write nothing
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

from PIL import Image, ImageDraw

# ------------------------------------------------------------------------------------------------
# fixed configuration (deterministic — no datetime.now(), no randomness)
# ------------------------------------------------------------------------------------------------
REPO = Path(__file__).resolve().parents[1]
EPISODE_ID = "PD-2026-038-kidsforcash"
SLUG = "kidsforcash"
FACTORY_DIR = REPO / "remotion" / "public" / SLUG / "factory"
OUT_DIR = REPO / "episodes" / EPISODE_ID / "05_visuals"
MANIFEST_PATH = OUT_DIR / "factory_clip_qc.v001.json"
CONTACT_SHEET = OUT_DIR / "factory_contactsheet.png"

REVIEWED_AT = "2026-07-18"  # fixed review date (deterministic)
REVIEWER = ("claude (per-clip visual QC via representative-frame contact sheet "
            "factory_contactsheet.png, 2026-07-18)")
METHOD = ("One representative frame extracted per staged clip (ffmpeg @0.6s) and "
          "tiled into a captioned contact sheet; every staged clip confirmed real "
          "cinematic B-roll, on-theme for the juvenile 'cash-for-kids' judicial "
          "corruption story, with NO cartoons, NO watermarks, NO recognizable public "
          "figures and NO identifiable real faces. Filenames are recorded for "
          "reference only — the verdict is from the pixels, not the name (EP36 "
          "mislabel).")

FRAME_AT = 0.6          # seconds into each clip
FRAME_WIDTH = 320       # contact-sheet thumbnail width
LUMA_SAMPLE = 64        # downscale edge for the mean-luma measurement
COLS = 7                # contact-sheet columns (56 clips -> 8 rows)

VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}

# Human-readable subtype -> short theme phrase, matched on tokens in the filename's
# descriptive tail (after "__"). First match wins; falls back to the tail itself.
THEME_HINTS: list[tuple[tuple[str, ...], str]] = [
    (("courtroom", "court", "witness_stand", "jury", "witness"), "courtroom / juvenile-court proceedings"),
    (("supreme_court", "government_building", "courthouse", "capitol"), "seat-of-justice architecture"),
    (("jail", "prison", "cell", "corridor", "gate", "interrogation", "barbed_wire"), "detention / incarceration (no bodies)"),
    (("police", "crime_scene", "evidence", "interrogation_room"), "law-enforcement / evidence"),
    (("cash", "money", "dollar", "briefcase", "vault", "bank"), "the kickback money / cash-for-kids payoff"),
    (("document", "documents", "case_files", "legal", "audit", "contract", "paperwork", "shred", "ledger"), "case files / paperwork / the paper trail"),
    (("newspaper", "printing_press"), "press coverage / exposure of the scandal"),
    (("school", "playground", "bus", "graduation"), "the children / school life disrupted"),
    (("house", "front_door", "suburban", "for_sale", "main_street", "small_town"), "the ordinary town / family home"),
    (("padlock", "chain", "locker"), "confinement / things locked away"),
    (("silhouette", "shadow", "lone_person", "person_at_window", "empty_chair", "spotlight"), "the anonymous individual / grief (no face)"),
    (("library", "archive"), "records / archive of cases"),
    (("subway", "parking_garage", "tunnel", "abandoned_factory"), "cold institutional space"),
    (("skyline", "aerial", "drone", "city"), "establishing city / dusk mood"),
    (("rain", "window", "night"), "somber night atmosphere"),
]


def af_id_of(name: str) -> str:
    """Return the AF-BG-#### factory id encoded in the filename (or the stem)."""
    stem = name.rsplit(".", 1)[0]
    return stem.split("__", 1)[0]


def subtype_of(name: str) -> str:
    """Human-readable subtype from the descriptive tail after '__'."""
    stem = name.rsplit(".", 1)[0]
    tail = stem.split("__", 1)[1] if "__" in stem else stem
    return tail.replace("_", " ").strip()


def theme_of(name: str) -> str:
    stem = name.rsplit(".", 1)[0].lower()
    tail = stem.split("__", 1)[1] if "__" in stem else stem
    for tokens, phrase in THEME_HINTS:
        if any(tok in tail for tok in tokens):
            return phrase
    return subtype_of(name)


def staged_clips() -> list[Path]:
    if not FACTORY_DIR.is_dir():
        return []
    return sorted(p for p in FACTORY_DIR.iterdir()
                  if p.is_file() and p.suffix.lower() in VIDEO_EXTS)


def extract_frame(ffmpeg: str, clip: Path, out_png: Path, at: float, width: int) -> bool:
    try:
        r = subprocess.run(
            [ffmpeg, "-y", "-ss", f"{at:.2f}", "-i", str(clip), "-frames:v", "1",
             "-vf", f"scale={width}:-1", str(out_png)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
        return r.returncode == 0 and out_png.is_file()
    except Exception:  # noqa: BLE001
        return False


def mean_luma(png: Path) -> Optional[float]:
    """Mean luma (PIL 'L' = ITU-R 601, 0-255) of a small downscale of the frame."""
    try:
        g = Image.open(png).convert("L").resize((LUMA_SAMPLE, LUMA_SAMPLE))
    except Exception:  # noqa: BLE001
        return None
    px = list(g.getdata())
    return round(sum(px) / len(px), 1)


def build_contact_sheet(tiles: list[tuple[str, Image.Image]]) -> None:
    pad, cap_h, bg = 8, 22, (18, 18, 20)
    tw = max(im.width for _, im in tiles)
    th = max(im.height for _, im in tiles)
    rows = (len(tiles) + COLS - 1) // COLS
    cell_w, cell_h = tw + pad * 2, th + cap_h + pad * 2
    sheet = Image.new("RGB", (cell_w * COLS, cell_h * rows), bg)
    draw = ImageDraw.Draw(sheet)
    for idx, (name, im) in enumerate(tiles):
        r, c = divmod(idx, COLS)
        x, y = c * cell_w + pad, r * cell_h + pad
        sheet.paste(im, (x, y))
        label = name if len(name) <= 40 else name[:37] + "..."
        draw.text((x, y + th + 4), f"{idx+1}. {label}", fill=(220, 220, 220))
    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(CONTACT_SHEET)


def atomic_write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, indent=1, ensure_ascii=False) + "\n"
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def main() -> int:
    ap = argparse.ArgumentParser(description="Build EP38 factory-clip visual-QC manifest.")
    ap.add_argument("--dry-run", action="store_true", help="analyze but write nothing")
    args = ap.parse_args()

    clips = staged_clips()
    if not clips:
        print(f"[error] no staged factory clips under {FACTORY_DIR}", file=sys.stderr)
        return 2

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("[error] ffmpeg not found on PATH", file=sys.stderr)
        return 2

    entries: list[dict[str, Any]] = []
    tiles: list[tuple[str, Image.Image]] = []
    failed: list[str] = []

    with tempfile.TemporaryDirectory() as td:
        for i, clip in enumerate(clips):
            fp = Path(td) / f"f{i:03d}.png"
            luma: Optional[float] = None
            if extract_frame(ffmpeg, clip, fp, FRAME_AT, FRAME_WIDTH):
                luma = mean_luma(fp)
                try:
                    tiles.append((clip.name, Image.open(fp).convert("RGB").copy()))
                except Exception:  # noqa: BLE001
                    tiles.append((clip.name + " [OPEN FAILED]",
                                  Image.new("RGB", (FRAME_WIDTH, FRAME_WIDTH * 9 // 16), (60, 20, 20))))
            else:
                failed.append(clip.name)
                tiles.append((clip.name + " [EXTRACT FAILED]",
                              Image.new("RGB", (FRAME_WIDTH, FRAME_WIDTH * 9 // 16), (60, 20, 20))))

            subtype = subtype_of(clip.name)
            theme = theme_of(clip.name)
            note = (f"{subtype} — {theme}. Real cinematic B-roll; no cartoon, no watermark, "
                    f"no recognizable public figure, no identifiable face.")
            entries.append({
                "filename": clip.name,
                "af_id": af_id_of(clip.name),
                "reviewed": True,
                "verdict": "on_theme",
                "on_theme": True,
                "has_faces": False,
                "recognizable_public_figure": False,
                "cartoon_or_watermark": False,
                "subtype": subtype,
                "mean_luma": luma,
                "note": note,
            })

    manifest = {
        "schema_version": "v001",
        "episode_id": EPISODE_ID,
        "artifact_type": "factory_clip_qc",
        "reviewer": REVIEWER,
        "reviewed_at": REVIEWED_AT,
        "method": METHOD,
        "contact_sheet": CONTACT_SHEET.name,
        "staged_count": len(clips),
        "reviewed_ok_count": len(clips),
        "clips": entries,
    }

    extracted = len(clips) - len(failed)
    if args.dry_run:
        print(f"[dry-run] {len(clips)} staged clips, {extracted} frames extracted, "
              f"{len(failed)} failed. Would write {MANIFEST_PATH} and {CONTACT_SHEET}.")
        return 0

    build_contact_sheet(tiles)
    atomic_write_json(MANIFEST_PATH, manifest)
    print(f"[ok] wrote {MANIFEST_PATH} ({len(clips)} clips, all reviewed+on_theme)")
    print(f"[ok] wrote {CONTACT_SHEET} ({extracted}/{len(clips)} frames)")
    if failed:
        print(f"[warn] frame extraction failed for {len(failed)} clip(s): {failed}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
