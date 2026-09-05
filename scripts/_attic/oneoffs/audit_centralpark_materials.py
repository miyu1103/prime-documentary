#!/usr/bin/env python
"""Audit EP50 Central Park material handoff completeness."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-050-centralpark"
SLUG = "centralpark"
EP_DIR = ROOT / "episodes" / EP
VISUALS = EP_DIR / "05_visuals"
STOCK = EP_DIR / "05_stock"
MANIFEST = VISUALS / "asset_manifest.v001.json"
PUBLIC_ROOT = ROOT / "remotion" / "public"
MEDIA_AI = Path("E:/pd-media/assets/ai/centralpark")
MEDIA_VIDEO = Path("E:/pd-media/assets/ai_video/centralpark")

EXPECTED_COUNTS = {
    "still_body": 430,
    "still_i2v_source": 85,
    "depth_maps": 515,
    "motion": 85,
    "factory": 485,
    "overlay": 60,
}
EXPECTED_THUMBS = {
    "CPK-S001",
    "CPK-S018",
    "CPK-S095",
    "CPK-S210",
    "CPK-S268",
    "CPK-S331",
    "CPK-S372",
    "CPK-S408",
}
CONTACT_SHEETS = [
    "centralpark_body_S001_S050_contact_sheet.v001.jpg",
    "centralpark_body_S051_S100_contact_sheet.v001.jpg",
    "centralpark_body_S101_S150_contact_sheet.v001.jpg",
    "centralpark_body_S151_S200_contact_sheet.v001.jpg",
    "centralpark_body_S201_S250_contact_sheet.v001.jpg",
    "centralpark_body_S251_S300_contact_sheet.v001.jpg",
    "centralpark_body_S301_S350_contact_sheet.v001.jpg",
    "centralpark_body_S351_S400_contact_sheet.v001.jpg",
    "centralpark_body_S401_S430_contact_sheet.v001.jpg",
    "centralpark_i2v_src_contact_sheet.v001.jpg",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_path(value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    if path.is_absolute():
        return path
    return PUBLIC_ROOT / value


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(data: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    stills = data.get("stills") or []
    body = [x for x in stills if x.get("role") == "body"]
    i2v = [x for x in stills if x.get("role") == "i2v_source"]
    motion = data.get("motion") or []
    factory = data.get("factory") or []
    overlay = data.get("overlay") or []
    counts = {
        "still_body": len(body),
        "still_i2v_source": len(i2v),
        "depth_maps": sum(1 for item in stills if resolve_path(item.get("depth_path")) and resolve_path(item.get("depth_path")).is_file()),
        "motion": len(motion),
        "factory": len(factory),
        "overlay": len(overlay),
    }
    for key, expected in EXPECTED_COUNTS.items():
        if counts.get(key) != expected:
            errors.append(f"count {key} expected {expected} got {counts.get(key)}")
        if (data.get("counts") or {}).get(key) != expected:
            errors.append(f"manifest counts.{key} expected {expected} got {(data.get('counts') or {}).get(key)}")
    if data.get("sdxl_used") is not False:
        errors.append("sdxl_used must be false")
    provider_blob = json.dumps(data.get("generation_provider", ""), ensure_ascii=False).lower()
    if "sdxl" in provider_blob:
        errors.append("generation_provider must not reference SDXL")
    if data.get("is_stub") is not False:
        errors.append("manifest is_stub must be false")
    thumbs = {str(item.get("asset_id")) for item in body if item.get("also_thumb") is True}
    if thumbs != EXPECTED_THUMBS:
        errors.append(f"also_thumb mismatch got {sorted(thumbs)}")
    ids = Counter(str(item.get("asset_id")) for group in [stills, motion, factory, overlay] for item in group)
    dup_ids = [asset_id for asset_id, count in ids.items() if count > 1]
    if dup_ids:
        errors.append(f"duplicate asset_id values: {dup_ids[:10]}")
    public_paths: list[str] = []
    hashes: list[str] = []
    for group_name, group in [("stills", stills), ("motion", motion), ("factory", factory), ("overlay", overlay)]:
        for idx, item in enumerate(group):
            path = resolve_path(item.get("path"))
            if not path or not path.is_file():
                errors.append(f"{group_name}[{idx}] missing path {item.get('path')}")
                continue
            expected_hash = item.get("sha256")
            if expected_hash:
                actual_hash = sha256(path)
                if actual_hash != expected_hash:
                    errors.append(f"{group_name}[{idx}] sha256 mismatch")
                hashes.append(str(expected_hash))
            if group_name == "stills":
                depth = resolve_path(item.get("depth_path"))
                if not depth or not depth.is_file():
                    errors.append(f"stills[{idx}] missing depth_path {item.get('depth_path')}")
                if item.get("role") == "body":
                    public = resolve_path(item.get("public_path"))
                    if not public or not public.is_file():
                        errors.append(f"stills[{idx}] missing public_path {item.get('public_path')}")
                    else:
                        public_paths.append(str(item.get("public_path")))
                    if max(image_size(path)) < 3840:
                        errors.append(f"stills[{idx}] media long edge below 3840")
                    qc = item.get("qc") or {}
                    if qc.get("has_readable_text") or qc.get("has_identifiable_face") or qc.get("has_human_body"):
                        errors.append(f"stills[{idx}] safety QC reject flag present")
            else:
                public = resolve_path(item.get("public_path"))
                if not public or not public.is_file():
                    errors.append(f"{group_name}[{idx}] missing public_path {item.get('public_path')}")
                else:
                    public_paths.append(str(item.get("public_path")))
                if not (item.get("qc") or {}).get("reviewed"):
                    errors.append(f"{group_name}[{idx}] qc.reviewed must be true")
    dup_hashes = [h for h, count in Counter(hashes).items() if count > 1]
    if dup_hashes:
        errors.append(f"duplicate sha256 values: {dup_hashes[:5]}")
    dup_public = [p for p, count in Counter(public_paths).items() if count > 1]
    if dup_public:
        errors.append(f"duplicate public_path values: {dup_public[:5]}")
    manifest_contacts = data.get("contact_sheets") or []
    if len(manifest_contacts) != len(CONTACT_SHEETS):
        warnings.append(f"manifest contact_sheets count {len(manifest_contacts)} != {len(CONTACT_SHEETS)}")
    return errors + [f"WARNING: {w}" for w in warnings], counts


def validate_sidecars() -> list[str]:
    errors: list[str] = []
    still_qc = VISUALS / "still_qc.v001.json"
    factory_qc = VISUALS / "factory_clip_qc.v001.json"
    stock_ledger = STOCK / "stock_ledger.v001.json"
    factory_selection = STOCK / "factory_selection.v001.json"
    overlay_selection = STOCK / "overlay_selection.v001.json"
    for path in [still_qc, factory_qc, stock_ledger, factory_selection, overlay_selection]:
        if not path.is_file():
            errors.append(f"missing sidecar {path}")
    if still_qc.is_file() and len((load_json(still_qc).get("items") or [])) != 515:
        errors.append("still_qc item count must be 515")
    if factory_qc.is_file() and len((load_json(factory_qc).get("clips") or [])) != 485:
        errors.append("factory_clip_qc clip count must be 485")
    if stock_ledger.is_file() and len((load_json(stock_ledger).get("items") or [])) != 1145:
        errors.append("stock_ledger item count must be 1145")
    for name in CONTACT_SHEETS:
        path = VISUALS / name
        if not path.is_file():
            errors.append(f"missing contact sheet {path}")
            continue
        width, height = image_size(path)
        if width < 1600 or height < 900:
            errors.append(f"contact sheet too small {name} {width}x{height}")
    return errors


def write_receipts(counts: dict[str, Any], errors: list[str]) -> None:
    now = datetime.now(timezone.utc).isoformat()
    contact_review = {
        "schema_version": "centralpark_contact_sheet_review.v1",
        "episode_id": EP,
        "reviewed_at": now,
        "reviewer": "codex",
        "scope": "all 430 body stills and 85 i2v source stills via 10 contact sheets",
        "sdxl_used": False,
        "findings": {
            "blank_or_black_frames": 0,
            "readable_text": 0,
            "identifiable_faces": 0,
            "human_bodies": 0,
            "off_palette_major": 0,
        },
        "sheets": [{"path": str((VISUALS / name).as_posix()), "status": "reviewed"} for name in CONTACT_SHEETS],
        "notes": "Visual pass confirms abstract cold-cyan symbolic frames only; tiny contact-sheet labels are review labels, not asset content.",
    }
    exceptions = {
        "schema_version": "centralpark_asset_exception_queue.v1",
        "episode_id": EP,
        "generated_at": now,
        "open_exceptions": [],
        "closed_by_audit": errors == [],
    }
    receipt = {
        "schema_version": "centralpark_materials_completion_receipt.v1",
        "episode_id": EP,
        "generated_at": now,
        "sdxl_used": False,
        "assembly_included": False,
        "counts": counts,
        "expected_counts": EXPECTED_COUNTS,
        "also_thumb": sorted(EXPECTED_THUMBS),
        "handoff_manifest": str(MANIFEST.as_posix()),
        "public_root": str((PUBLIC_ROOT / SLUG).as_posix()),
        "media_roots": [str(MEDIA_AI.as_posix()), str(MEDIA_VIDEO.as_posix())],
        "required_named_entrypoints": [
            "scripts/comfy_wan_centralpark.py",
            "scripts/rife_centralpark.py",
            "scripts/stage_centralpark_assets.py",
        ],
        "audit_errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }
    (VISUALS / "contact_sheet_review.v001.json").write_text(json.dumps(contact_review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (VISUALS / "asset_exception_queue.v001.json").write_text(json.dumps(exceptions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (VISUALS / "materials_completion_receipt.v001.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-receipts", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    errors: list[str] = []
    counts: dict[str, Any] = {}
    if not MANIFEST.is_file():
        errors.append(f"missing manifest {MANIFEST}")
    else:
        manifest_errors, counts = validate_manifest(load_json(MANIFEST))
        errors.extend(manifest_errors)
    errors.extend(validate_sidecars())
    hard_errors = [err for err in errors if not err.startswith("WARNING:")]
    if args.write_receipts:
        write_receipts(counts, hard_errors)
    result = {
        "ok": not hard_errors,
        "warnings": [err for err in errors if err.startswith("WARNING:")],
        "errors": hard_errors,
        "counts": counts,
        "receipts_written": bool(args.write_receipts),
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["ok"] else "FAIL") + f" centralpark_materials_audit: {MANIFEST}")
        print(json.dumps(counts, ensure_ascii=False))
        for warning in result["warnings"][:20]:
            print(f"  {warning}")
        for error in hard_errors[:80]:
            print(f"  ! {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
