#!/usr/bin/env python3
"""Generate arc_used_fingerprints.json (sha256 + pHash + content-tag) for the shipped VISUAL
assets of the upstream arc episodes EP33 (tyler) and EP34 (rolin), per EP35 DESIGN [OG-0.5].

Visual assets only. Audio/music/ambience stems are produced in the separate 06_audio lane and
are intentionally OUT OF SCOPE here.

pHash = 64-bit DCT perceptual hash (hand-rolled with Pillow + numpy, since `imagehash` is not
installed). Computed for still images only; videos carry sha256 + content-tag (frame pHash needs
ffmpeg extraction and is not required by the design for exact-dup / content-tag reuse detection).
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(r"C:/Users/aab15/Documents/prime-documentary")
PUBLIC = ROOT / "remotion" / "public"
OUT = ROOT / "episodes" / "PD-2026-035-hinders" / "01_research" / "arc_used_fingerprints.json"

EPISODES = {
    "tyler": "PD-2026-033-tyler",
    "rolin": "PD-2026-034-rolin",
}

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".m4v", ".gif"}
VISUAL_EXTS = IMAGE_EXTS | VIDEO_EXTS


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _dct_1d(a: np.ndarray) -> np.ndarray:
    n = a.shape[-1]
    k = np.arange(n)
    basis = np.cos(np.pi * (2 * k[None, :] + 1) * k[:, None] / (2 * n))
    return a @ basis.T


def phash_64(path: Path) -> str | None:
    """Standard 32x32 -> DCT -> top-left 8x8 (drop DC) -> median threshold -> 64-bit hex."""
    try:
        img = Image.open(path).convert("L").resize((32, 32), Image.LANCZOS)
    except Exception:
        return None
    arr = np.asarray(img, dtype=np.float64)
    d = _dct_1d(_dct_1d(arr.T).T)          # 2-D DCT
    block = d[:8, :8]
    flat = block.flatten()
    med = np.median(flat[1:])              # exclude DC term from the median
    bits = (flat > med).astype(np.uint8)
    val = 0
    for b in bits:
        val = (val << 1) | int(b)
    return f"{val:016x}"


def content_tag(basename: str, kind: str) -> str | None:
    stem = os.path.splitext(basename)[0]
    if "__" in stem:                       # factory: AF-BG-0666__government_building_exterior
        return stem.split("__", 1)[1].lower()
    if kind == "hero":                     # rolin: hero_signswap / tyler hero/equitybar
        return stem.lower().replace("hero_", "")
    if kind == "depth_map":
        base = stem[:-6] if stem.endswith("_depth") else stem
        return f"{base.lower()}::depthmap"
    return None                            # generated stills carry no semantic tag in the filename


def classify(rel: str, basename: str) -> str:
    low = rel.lower()
    if "/factory/" in low:
        return "factory"
    if "/hero" in low or basename.lower().startswith("hero"):
        return "hero"
    if basename.lower().endswith("_depth.png"):
        return "depth_map"
    if basename.lower().startswith("contact_sheet"):
        return "contact_sheet"
    if "/img/" in low:
        return "generated_still"
    return "other"


def collect(slug: str, episode_id: str) -> list[dict]:
    base = PUBLIC / slug
    rows: list[dict] = []
    for f in sorted(base.rglob("*")):
        if not f.is_file():
            continue
        ext = f.suffix.lower()
        if ext not in VISUAL_EXTS:
            continue
        rel = f.relative_to(ROOT).as_posix()
        kind = classify(rel, f.name)
        rows.append({
            "episode": episode_id,
            "path": rel,
            "basename": f.name,
            "kind": kind,
            "ext": ext.lstrip("."),
            "content_tag": content_tag(f.name, kind),
            "sha256": sha256_of(f),
            "phash": phash_64(f) if ext in IMAGE_EXTS else None,
        })
    return rows


def main() -> int:
    assets: list[dict] = []
    per_ep: dict[str, int] = {}
    for slug, eid in EPISODES.items():
        rows = collect(slug, eid)
        per_ep[eid] = len(rows)
        assets.extend(rows)

    kinds: dict[str, int] = {}
    tags: dict[str, int] = {}
    for a in assets:
        kinds[a["kind"]] = kinds.get(a["kind"], 0) + 1
        if a["content_tag"]:
            tags[a["content_tag"]] = tags.get(a["content_tag"], 0) + 1

    n_phash = sum(1 for a in assets if a["phash"])
    payload = {
        "schema_version": "1.0.0",
        "artifact": "arc_used_fingerprints",
        "purpose": ("Cross-episode arc NON-reuse ledger (sha256 + pHash + content-tag) for the "
                    "shipped VISUAL assets of upstream arc episodes EP33/EP34, per EP35 "
                    "PD-2026-035-hinders DESIGN [OG-0.5]. Enables sha256 exact-dup and content-tag "
                    "semantic-reuse checks across the 3-episode forfeiture arc."),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "generator": "scripts/gen_arc_fingerprints.py (run from scratchpad copy)",
        "phash": {
            "algorithm": "dct-phash-64bit",
            "pipeline": "L / resize 32x32 LANCZOS / 2-D DCT / top-left 8x8 / median(excl DC) threshold",
            "bits": 64,
            "hamming_reuse_threshold": 6,
            "note": "still images only; videos carry sha256 + content-tag (frame pHash out of scope)",
        },
        "scope_note": ("VISUAL assets only. Audio/music/ambience stems are produced in the separate "
                       "06_audio lane and are intentionally OUT OF SCOPE in this ledger."),
        "note_consumer": ("The implemented gate scripts/check_arc_nonrepeat.py computes basename "
                          "fingerprints on-the-fly and does NOT read this file. This ledger is the "
                          "DESIGN [OG-0.5] preflight artifact (sha+pHash+content-tag) for owner "
                          "review and a future check_arc_footage_nonoverlap preflight."),
        "episodes": list(EPISODES.values()),
        "counts": {
            "total_assets": len(assets),
            "per_episode": per_ep,
            "by_kind": dict(sorted(kinds.items())),
            "images_with_phash": n_phash,
            "distinct_content_tags": len(tags),
        },
        "assets": assets,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, OUT)
    print(f"WROTE {OUT}")
    print(f"  total_assets = {len(assets)}  per_episode = {per_ep}")
    print(f"  by_kind = {dict(sorted(kinds.items()))}")
    print(f"  images_with_phash = {n_phash}  distinct_content_tags = {len(tags)}")

    # integrity self-checks
    shas = [a["sha256"] for a in assets]
    dupe_sha = len(shas) - len(set(shas))
    print(f"  duplicate-sha entries within EP33+EP34 = {dupe_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
