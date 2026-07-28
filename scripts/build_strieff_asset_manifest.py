#!/usr/bin/env python
"""Build and validate the EP49 Strieff asset manifest.

The image source for this run is Codex image generation, not SDXL. This script
never fabricates missing media: normal verification fails until all required
body stills, i2v source stills, motion clips, factory clips, and overlays exist.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
EPISODE_ID = "PD-2026-049-strieff"
SLUG = "strieff"
MEDIA_DIR = Path("H:/pd-media/assets/ai/strieff")
MOTION_DIR = Path("H:/pd-media/assets/ai_video/strieff")
PUBLIC_ROOT = ROOT / "remotion" / "public" / SLUG
PUBLIC_IMG_DIR = PUBLIC_ROOT / "img"
VISUALS_DIR = ROOT / "episodes" / EPISODE_ID / "05_visuals"
STOCK_DIR = ROOT / "episodes" / EPISODE_ID / "05_stock"
MANIFEST = VISUALS_DIR / "asset_manifest.v001.json"
STOCK_LEDGER = STOCK_DIR / "stock_ledger.v001.json"
THUMB_IDS = {"S01", "S05", "S15", "S30", "S37", "S47"}
EXPECTED_COUNTS = {"still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 93, "overlay": 12}
VALID_STILL_ROLES = {"body", "i2v_source", "reject"}
BANNED_ACCURACY = (
    "the stop was legal",
    "the stop was lawful",
    "the stop was constitutional",
    "exclusionary rule abolished",
    "exclusionary rule was abolished",
    "we are all harmed",
    "6-3",
    "8-3",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size


def mean_luma(path: Path) -> float:
    with Image.open(path) as im:
        gray = ImageOps.grayscale(im).resize((96, 54), Image.Resampling.LANCZOS)
        hist = gray.histogram()
    total = sum(hist)
    weighted = sum(value * count for value, count in enumerate(hist))
    return round(weighted / total, 2)


def body_ids() -> list[str]:
    return [f"S{i:02d}" for i in range(1, 86)]


def i2v_source_ids() -> list[str]:
    return [f"M{i:02d}_src" for i in range(1, 17)]


def make_depth(src: Path, dst: Path) -> None:
    with Image.open(src) as im:
        fitted = ImageOps.fit(im.convert("RGB"), (3840, 2160), Image.Resampling.LANCZOS)
        gray = ImageOps.grayscale(fitted).resize((960, 540), Image.Resampling.LANCZOS)
        gradient = Image.linear_gradient("L").resize(gray.size).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        depth = Image.blend(gray, gradient, 0.35).filter(ImageFilter.GaussianBlur(radius=5))
        depth = ImageOps.autocontrast(depth).resize((3840, 2160), Image.Resampling.BICUBIC)
        dst.parent.mkdir(parents=True, exist_ok=True)
        depth.save(dst)


def make_contact_sheet(ids: list[str], out_path: Path, columns: int = 5) -> None:
    existing = [asset_id for asset_id in ids if (MEDIA_DIR / f"{asset_id}.png").is_file()]
    if not existing:
        return
    thumb_w, thumb_h = 512, 288
    label_h = 34
    rows = (len(existing) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_w, rows * (thumb_h + label_h)), (16, 16, 18))
    draw = ImageDraw.Draw(sheet)
    for idx, asset_id in enumerate(existing):
        x = (idx % columns) * thumb_w
        y = (idx // columns) * (thumb_h + label_h)
        with Image.open(MEDIA_DIR / f"{asset_id}.png") as im:
            thumb = ImageOps.fit(im.convert("RGB"), (thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        draw.rectangle((x, y + thumb_h, x + thumb_w, y + thumb_h + label_h), fill=(24, 24, 28))
        draw.text((x + 12, y + thumb_h + 9), asset_id, fill=(230, 230, 235))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path, quality=92)


def still_entry(asset_id: str, role: str, errors: list[str]) -> dict[str, Any] | None:
    src = MEDIA_DIR / f"{asset_id}.png"
    public = PUBLIC_IMG_DIR / f"{asset_id}.png"
    depth = MEDIA_DIR / f"{asset_id}_depth.png"
    public_depth = PUBLIC_IMG_DIR / f"{asset_id}_depth.png"
    if not src.is_file():
        errors.append(f"missing image {src}")
        return None
    if not public.is_file():
        errors.append(f"missing public image {public}")
        return None
    width, height = image_size(src)
    public_width, public_height = image_size(public)
    if (width, height) != (3840, 2160):
        errors.append(f"{asset_id} media size {width}x{height}, expected 3840x2160")
    if (public_width, public_height) != (3840, 2160):
        errors.append(f"{asset_id} public size {public_width}x{public_height}, expected 3840x2160")
    if role == "body" and not depth.is_file():
        make_depth(src, depth)
    if role == "body" and depth.is_file() and not public_depth.is_file():
        public_depth.parent.mkdir(parents=True, exist_ok=True)
        public_depth.write_bytes(depth.read_bytes())
    entry: dict[str, Any] = {
        "asset_id": f"STRF-S{asset_id[1:]}" if role == "body" else f"STRF-MS{asset_id[1:3]}",
        "scene_id": asset_id,
        "role": role,
        "path": src.as_posix(),
        "public_path": f"{SLUG}/img/{asset_id}.png",
        "width": width,
        "height": height,
        "sha256": sha256(src),
        "mean_luma": mean_luma(src),
        "ai_disclosure_required": True,
        "generation_provider": "Codex built-in image_gen",
        "caption_hint": "symbolic AI-assisted visualization only",
        "tags": ["symbolic", SLUG, "no_face", "no_likeness", "no_readable_text"],
        "qc": {
            "reviewed": asset_id == "S01",
            "has_readable_text": False,
            "has_identifiable_face": False,
            "has_human_body": False,
            "has_displayed_drugs": False,
            "notes": "S01 visually inspected in Codex; remaining entries require review when generated." if asset_id == "S01" else "",
        },
    }
    if role == "body":
        entry["depth_path"] = depth.as_posix()
        entry["also_thumb"] = asset_id in THUMB_IDS
    return entry


def load_optional_items(path: Path, key: str) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    items = data.get(key)
    return items if isinstance(items, list) else []


def build() -> dict[str, Any]:
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)
    STOCK_DIR.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    stills: list[dict[str, Any]] = []
    for asset_id in body_ids():
        entry = still_entry(asset_id, "body", errors)
        if entry:
            stills.append(entry)
    for asset_id in i2v_source_ids():
        entry = still_entry(asset_id, "i2v_source", errors)
        if entry:
            stills.append(entry)

    factory = load_optional_items(STOCK_DIR / "factory_selection.v001.json", "factory")
    overlay = load_optional_items(STOCK_DIR / "overlay_selection.v001.json", "overlay")
    motion = []
    for i in range(1, 17):
        asset_id = f"STRF-M{i:02d}"
        path = MOTION_DIR / f"M{i:02d}_rife.mp4"
        public_path = f"{SLUG}/motion/M{i:02d}_rife.mp4"
        public = PUBLIC_ROOT / "motion" / f"M{i:02d}_rife.mp4"
        if path.is_file() and public.is_file():
            motion.append(
                {
                    "asset_id": asset_id,
                    "source_scene_id": f"MS{i:02d}",
                    "source_still": (MEDIA_DIR / f"M{i:02d}_src.png").as_posix(),
                    "path": path.as_posix(),
                    "public_path": public_path,
                    "sha256": sha256(path),
                    "ai_disclosure_required": True,
                    "generation_provider": "Codex image still + local i2v",
                    "qc": {"reviewed": False, "notes": ""},
                }
            )

    counts = {
        "still_body": len([x for x in stills if x.get("role") == "body"]),
        "still_i2v_source": len([x for x in stills if x.get("role") == "i2v_source"]),
        "motion": len(motion),
        "factory": len(factory),
        "overlay": len(overlay),
    }
    manifest = {
        "schema_version": "strieff_assets.v1",
        "episode_id": EPISODE_ID,
        "slug": SLUG,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "producer": "scripts/build_strieff_asset_manifest.py",
        "generation_provider": "Codex built-in image_gen",
        "sdxl_used": False,
        "is_stub": False,
        "counts": counts,
        "expected_counts": EXPECTED_COUNTS,
        "safety_locks": {
            "stop_was_illegal": True,
            "exclusionary_rule_not_abolished": True,
            "attenuation_only_reason_evidence_stayed": True,
            "vote_5_3": True,
            "scalia_seat_vacant_eight_justices": True,
            "no_living_private_person_likeness": True,
            "no_readable_case_text_in_images": True,
            "ai_disclosure_required": True,
        },
        "stills": stills,
        "factory": factory,
        "motion": motion,
        "overlay": overlay,
        "contact_sheets": [
            "episodes/PD-2026-049-strieff/05_visuals/strieff_body_contact_sheet.v001.jpg",
            "episodes/PD-2026-049-strieff/05_visuals/strieff_i2v_src_contact_sheet.v001.jpg",
        ],
        "errors": errors,
    }
    make_contact_sheet(body_ids(), VISUALS_DIR / "strieff_body_contact_sheet.v001.jpg")
    make_contact_sheet(i2v_source_ids(), VISUALS_DIR / "strieff_i2v_src_contact_sheet.v001.jpg", columns=4)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    STOCK_LEDGER.write_text(json.dumps(make_stock_ledger(manifest), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def make_stock_ledger(manifest: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for group in ("stills", "motion", "factory", "overlay"):
        for item in manifest.get(group) or []:
            rows.append(
                {
                    "asset_id": item.get("asset_id"),
                    "path": item.get("path"),
                    "public_path": item.get("public_path"),
                    "source": "ai_codex" if group in {"stills", "motion"} else "factory",
                    "license": "project-controlled" if group in {"stills", "motion"} else item.get("license", "unknown"),
                    "commercial_use": True if group in {"stills", "motion"} else item.get("commercial_use"),
                    "sha256": item.get("sha256"),
                    "ai_disclosure_required": item.get("ai_disclosure_required", False),
                }
            )
    return {"schema_version": "strieff_stock_ledger.v1", "episode_id": EPISODE_ID, "items": rows}


def strings(obj: Any) -> list[str]:
    out: list[str] = []
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            out.extend(strings(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(strings(v))
    return out


def evaluate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = list(data.get("errors") or [])
    if data.get("schema_version") != "strieff_assets.v1":
        errors.append(f"schema_version mismatch: {data.get('schema_version')}")
    if data.get("episode_id") != EPISODE_ID:
        errors.append(f"episode_id mismatch: {data.get('episode_id')}")
    if data.get("sdxl_used") is not False:
        errors.append("sdxl_used must be false")
    counts = data.get("counts") or {}
    for key, expected in EXPECTED_COUNTS.items():
        if counts.get(key) != expected:
            errors.append(f"counts.{key} expected {expected} got {counts.get(key)}")
    stills = data.get("stills") or []
    bad_roles = sorted({str(s.get("role")) for s in stills if s.get("role") not in VALID_STILL_ROLES})
    if bad_roles:
        errors.append(f"invalid still roles: {bad_roles}")
    also_thumb = {str(s.get("scene_id")) for s in stills if s.get("role") == "body" and s.get("also_thumb") is True}
    if also_thumb != THUMB_IDS:
        errors.append(f"also_thumb set {sorted(also_thumb)} != {sorted(THUMB_IDS)}")
    paths = [str(x.get("public_path")) for group in ("stills", "factory", "motion", "overlay") for x in (data.get(group) or []) if x.get("public_path")]
    dups = sorted([p for p, c in Counter(paths).items() if c > 1])
    if dups:
        errors.append(f"duplicate public_path: {dups[:5]}")
    lower = "\n".join(strings(data)).lower()
    for token in BANNED_ACCURACY:
        if token in lower:
            errors.append(f"banned wording present: {token}")
    for item in stills:
        public_path = item.get("public_path")
        if public_path and not (ROOT / "remotion" / "public" / str(public_path)).is_file():
            errors.append(f"missing public still {public_path}")
        if item.get("role") == "body":
            depth = item.get("depth_path")
            if not depth or not Path(str(depth)).is_file():
                errors.append(f"{item.get('scene_id')} missing depth_path {depth}")
        if int(item.get("width") or 0) != 3840 or int(item.get("height") or 0) != 2160:
            errors.append(f"{item.get('scene_id')} wrong size {item.get('width')}x{item.get('height')}")
    for item in data.get("motion") or []:
        public_path = str(item.get("public_path") or "")
        if not public_path.endswith("_rife.mp4"):
            errors.append(f"motion public_path must be *_rife.mp4: {public_path}")
        if public_path and not (ROOT / "remotion" / "public" / public_path).is_file():
            errors.append(f"missing public motion {public_path}")
    for item in data.get("factory") or []:
        public_path = str(item.get("public_path") or "").replace("\\", "/")
        if "/factory/" not in public_path:
            errors.append(f"factory public_path must include /factory/: {public_path}")
    for item in data.get("overlay") or []:
        public_path = str(item.get("public_path") or "").replace("\\", "/")
        if "/overlay/" not in public_path:
            errors.append(f"overlay public_path must include /overlay/: {public_path}")
    return errors


def reuse_feasibility(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    counts = data.get("counts") or {}
    if counts.get("still_body", 0) < 85:
        errors.append(f"still_body {counts.get('still_body')} < 85")
    if counts.get("motion", 0) < 16:
        errors.append(f"motion {counts.get('motion')} < 16")
    if counts.get("factory", 0) < 93:
        errors.append(f"factory {counts.get('factory')} < 93")
    distinct = int(counts.get("still_body", 0)) + int(counts.get("motion", 0)) + int(counts.get("factory", 0))
    if distinct < 194:
        errors.append(f"distinct {distinct} < 194")
    first_use = distinct / 226
    if first_use < 0.70:
        errors.append(f"first-use {first_use:.4f} < 0.70")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--reuse-feasibility", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    data = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() and (args.verify or args.reuse_feasibility) else build()
    errors = reuse_feasibility(data) if args.reuse_feasibility else evaluate(data)
    result = {"ok": not errors, "asset_manifest": str(MANIFEST), "counts": data.get("counts"), "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        label = "strieff_reuse_feasibility" if args.reuse_feasibility else "strieff_asset_manifest"
        print(("PASS" if result["ok"] else "FAIL") + f" {label}: {MANIFEST}")
        print(f"counts={result['counts']}")
        for err in errors[:40]:
            print(f"  ! {err}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
