#!/usr/bin/env python
"""EP46 TLO factory-footage selection and verification helpers."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from factory_themes import theme_of
from select_factory_assets import used_basenames

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-046-tlo"
MANIFEST = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
SHELF_MANIFEST = ROOT / "assets" / "asset_manifest.v001.json"
FACTORY_PUBLIC = ROOT / "remotion" / "public" / "tlo" / "factory"
OVERLAY_PUBLIC = ROOT / "remotion" / "public" / "tlo" / "overlay"
FACTORY_SELECTION = ROOT / "episodes" / EP / "05_stock" / "factory_selection.v001.json"
OVERLAY_SELECTION = ROOT / "episodes" / EP / "05_stock" / "overlay_selection.v001.json"
FACTORY_QC = ROOT / "episodes" / EP / "05_visuals" / "factory_clip_qc.v001.json"
PRIOR_PUBLIC = [ROOT / "remotion" / "public" / s / "factory" for s in ("frazier", "lech", "thompson", "cleveland")]
PRIOR_SELECTED = [
    ROOT / "runs" / "qc" / "frazier_factory_selected.v001.json",
    ROOT / "runs" / "qc" / "lech_factory_selected.v001.json",
    ROOT / "runs" / "qc" / "thompson_factory_selected.v001.json",
    ROOT / "runs" / "qc" / "cleveland_factory_selected.v001.json",
]
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}
MEDIA_ROOT = Path("H:/pd-media/assets")

# Conservative first pass: no children, no identifiable people, no courtroom actors.
FACTORY_SUBTYPE_ORDER = [
    "school_hallway_empty",
    "empty_playground_at_dusk",
    "witness_stand_empty",
    "jury_box_empty",
    "courtroom_empty_wide",
    "supreme_court_building",
    "courthouse_steps",
    "courtroom_gavel_block_macro",
    "judge_gavel_wooden",
    "law_library_books",
    "federal_building_columns_night",
    "government_building_exterior",
    "american_flag_waving",
    "voting_booth_curtain",
    "subway_tunnel_empty",
    "city_skyline_dusk",
    "empty_boardroom_at_night",
]
OVERLAY_SUBTYPE_ORDER = [
    "dust_particles",
    "floating_dust",
    "light_leak",
    "soft_light_rays",
    "film_grain",
    "subtle_noise",
    "vintage_typewriter",
]
BANNED_NAME_PARTS = {
    "child",
    "children",
    "student",
    "teacher",
    "person_",
    "person-",
    "portrait",
    "face",
    "crowd",
    "protest",
    "hospital",
    "prison",
    "jail",
    "booking",
    "cell",
    "dog",
    "cat",
    "buddha",
    "yoga",
    "money",
    "cash",
    "newspaper",
    "constitution",
    "wanted_poster",
    "signing",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _load_shelf() -> list[dict[str, Any]]:
    data = json.loads(SHELF_MANIFEST.read_text(encoding="utf-8"))
    return [x for x in data.get("assets", []) if isinstance(x, dict)]


def _source_path(asset: dict[str, Any]) -> Path:
    raw = Path(str(asset.get("path") or ""))
    if raw.is_absolute():
        return raw
    return MEDIA_ROOT / raw


def _fresh_video_assets() -> list[dict[str, Any]]:
    used = used_basenames(EP)
    out: list[dict[str, Any]] = []
    for asset in _load_shelf():
        if asset.get("kind") != "video":
            continue
        src = _source_path(asset)
        if src.suffix.lower() not in VIDEO_EXTS:
            continue
        if src.name.lower() in used:
            continue
        lowered = src.name.lower()
        if any(part in lowered for part in BANNED_NAME_PARTS):
            continue
        out.append(asset)
    return out


def _pick_by_subtypes(subtypes: list[str], count: int, *, category: str | None = None) -> list[dict[str, Any]]:
    picked: list[dict[str, Any]] = []
    seen: set[str] = set()
    by_subtype = {subtype: [] for subtype in subtypes}
    for asset in _fresh_video_assets():
        subtype = str(asset.get("subtype") or "")
        if subtype not in by_subtype:
            continue
        if category and asset.get("type") != category:
            continue
        src = _source_path(asset)
        if not src.is_file():
            continue
        by_subtype[subtype].append(asset)
    for subtype in subtypes:
        for asset in by_subtype[subtype]:
            src = _source_path(asset)
            sha = sha256_file(src)
            if sha in seen:
                continue
            row = dict(asset)
            row["_source"] = src
            row["_sha256"] = sha
            picked.append(row)
            seen.add(sha)
            if len(picked) == count:
                return picked
    return picked


def _replace_dir_contents(target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    old = [p for p in target.iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXTS]
    if not old:
        return
    backup = target.parent / f"_{target.name}_backup_{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    backup.mkdir(parents=True, exist_ok=False)
    for path in old:
        shutil.move(str(path), str(backup / path.name))


def _stage_assets(picked: list[dict[str, Any]], target: Path, prefix: str) -> list[dict[str, Any]]:
    _replace_dir_contents(target)
    rows: list[dict[str, Any]] = []
    for i, asset in enumerate(picked, 1):
        src = Path(asset["_source"])
        dst = target / f"{prefix}{i:03d}__{src.name}"
        shutil.copy2(src, dst)
        rows.append({
            "asset_id": f"TLO-{prefix}{i:03d}" if prefix == "F" else f"TLO-{prefix}{i:02d}",
            "index": i,
            "source_id": asset.get("id"),
            "source_path": str(src).replace("\\", "/"),
            "public_path": str(dst.relative_to(ROOT / "remotion" / "public")).replace("\\", "/"),
            "filename": dst.name,
            "subtype": asset.get("subtype"),
            "theme": theme_of(asset.get("subtype"), asset.get("type")),
            "license": asset.get("license"),
            "sha256": asset["_sha256"],
        })
    return rows


def select_assets() -> int:
    factory = _pick_by_subtypes(FACTORY_SUBTYPE_ORDER, 92)
    overlay = _pick_by_subtypes(OVERLAY_SUBTYPE_ORDER, 12)
    if len(factory) != 92:
        print(f"FAIL selected factory {len(factory)} != 92")
        return 1
    if len(overlay) != 12:
        print(f"FAIL selected overlay {len(overlay)} != 12")
        return 1
    factory_rows = _stage_assets(factory, FACTORY_PUBLIC, "F")
    overlay_rows = _stage_assets(overlay, OVERLAY_PUBLIC, "O")
    FACTORY_SELECTION.parent.mkdir(parents=True, exist_ok=True)
    OVERLAY_SELECTION.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    FACTORY_SELECTION.write_text(json.dumps({
        "episode_id": EP,
        "generated_at": now,
        "selection_policy": "fresh-only existing Asset Factory video, conservative TLO subtypes, copied not moved",
        "count": len(factory_rows),
        "clips": factory_rows,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OVERLAY_SELECTION.write_text(json.dumps({
        "episode_id": EP,
        "generated_at": now,
        "selection_policy": "fresh-only overlay/support video, copied not moved",
        "count": len(overlay_rows),
        "clips": overlay_rows,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    FACTORY_QC.parent.mkdir(parents=True, exist_ok=True)
    FACTORY_QC.write_text(json.dumps({
        "episode_id": EP,
        "generated_at": now,
        "review_method": "contact-sheet first-frame visual review; reject and restage any clip with people, children, readable text, watermark, off-theme content, or label mismatch",
        "clips": [{
            "filename": row["filename"],
            "reviewed": False,
            "on_theme": False,
            "verdict": "pending",
            "observed_content": "",
            "notes": "pending visual contact-sheet review",
        } for row in factory_rows],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"factory": len(factory_rows), "overlay": len(overlay_rows), "factory_selection": str(FACTORY_SELECTION), "overlay_selection": str(OVERLAY_SELECTION), "factory_qc": str(FACTORY_QC)}, ensure_ascii=False, indent=2))
    return 0


def prior_shas() -> set[str]:
    out: set[str] = set()
    for folder in PRIOR_PUBLIC:
        if not folder.is_dir():
            continue
        for p in folder.iterdir():
            if p.is_file() and p.suffix.lower() in {".mp4", ".mov", ".webm"}:
                out.add(sha256_file(p))
    for jp in PRIOR_SELECTED:
        if not jp.exists():
            continue
        data = json.loads(jp.read_text(encoding="utf-8"))
        rows = data if isinstance(data, list) else data.get("factory", [])
        for row in rows:
            if isinstance(row, dict) and row.get("sha256"):
                out.add(str(row["sha256"]))
    return out


def verify_no_prior_overlap() -> int:
    if not MANIFEST.exists():
        print(f"FAIL missing {MANIFEST}")
        return 1
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    prior = prior_shas()
    overlaps = []
    for item in data.get("factory", []):
        sha = item.get("sha256")
        if sha and sha in prior:
            overlaps.append({"asset_id": item.get("asset_id"), "sha256": sha, "public_path": item.get("public_path")})
    result = {"ok": not overlaps, "prior_sha_count": len(prior), "overlaps": overlaps}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--select", action="store_true")
    ap.add_argument("--verify-no-prior-overlap", action="store_true")
    args = ap.parse_args()
    if args.select:
        return select_assets()
    if args.verify_no_prior_overlap:
        return verify_no_prior_overlap()
    print("Use --select to stage EP46 TLO factory/overlay candidates, or --verify-no-prior-overlap after asset_manifest.v001.json exists.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

