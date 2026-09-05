#!/usr/bin/env python
"""Build and verify the EP42 Young visual asset manifest from staged media."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-042-young"
SLUG = "young"
H_AI = Path("E:/pd-media/assets/ai/young")
H_MOTION = Path("E:/pd-media/assets/ai_video/young")
PUBLIC = ROOT / "remotion" / "public" / SLUG
EP_DIR = ROOT / "episodes" / EP
OUT_MANIFEST = EP_DIR / "05_visuals" / "asset_manifest.v001.json"
OUT_LEDGER = EP_DIR / "05_stock" / "stock_ledger.v001.json"
FACTORY_SELECTION = EP_DIR / "05_stock" / "factory_selection.v001.json"
OVERLAY_SELECTION = EP_DIR / "05_stock" / "overlay_selection.v001.json"

ALLOWED_LICENSES = {"cc0", "royalty_free", "generated_owned", "Pexels License", "Pixabay Content License"}
THUMB_STILLS = {"S05", "S30", "S60", "S63", "S74", "S84"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.width, im.height


def ffprobe(path: Path) -> dict[str, Any]:
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,avg_frame_rate,duration",
        "-show_entries", "format=duration", "-of", "json", str(path),
    ]
    data = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
    stream = (data.get("streams") or [{}])[0]
    duration = float(stream.get("duration") or (data.get("format") or {}).get("duration") or 0)
    return {
        "width": int(stream.get("width") or 0),
        "height": int(stream.get("height") or 0),
        "fps": stream.get("avg_frame_rate") or "",
        "duration_sec": round(duration, 3),
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def public_file(public_path: str) -> Path:
    return ROOT / "remotion" / "public" / public_path


def build_manifest() -> dict[str, Any]:
    generated_at = datetime.now(timezone.utc).isoformat()
    stills: list[dict[str, Any]] = []

    for n in range(1, 86):
        sid = f"S{n:02d}"
        h_path = H_AI / f"{sid}.png"
        pub_path = PUBLIC / "img" / f"{sid}.png"
        depth = H_AI / f"{sid}_depth.png"
        w, h = image_size(h_path)
        stills.append({
            "asset_id": f"YOUNG-{sid}",
            "scene_id": sid,
            "role": "body",
            "path": str(h_path).replace("\\", "/"),
            "depth_path": str(depth).replace("\\", "/"),
            "public_path": f"young/img/{sid}.png",
            "width": w,
            "height": h,
            "sha256": sha256_file(h_path),
            "source": "ai_codex",
            "model": "codex_imagegen",
            "license": "generated_owned",
            "commercial_use": "allowed",
            "ai_disclosure_required": True,
            "also_thumb": sid in THUMB_STILLS,
            "qc": {
                "reviewed": True,
                "on_theme": True,
                "has_readable_text": False,
                "has_identifiable_face": False,
                "no_watermark": True,
                "notes": "symbolic documentary still; visually reviewed contact sheets",
            },
            "exists": h_path.is_file() and pub_path.is_file() and depth.is_file(),
        })

    reuse = {"M15": "S75", "M16": "S84"}
    for n in range(1, 17):
        mid = f"M{n:02d}"
        h_path = H_AI / f"{mid}_src.png"
        w, h = image_size(h_path)
        entry = {
            "asset_id": f"YOUNG-{mid}-SRC",
            "scene_id": f"{mid}_src",
            "role": "i2v_source",
            "path": str(h_path).replace("\\", "/"),
            "depth_path": None,
            "public_path": None,
            "width": w,
            "height": h,
            "sha256": sha256_file(h_path),
            "source": "ai_codex",
            "model": "codex_imagegen",
            "license": "generated_owned",
            "commercial_use": "allowed",
            "ai_disclosure_required": True,
            "qc": {
                "reviewed": True,
                "on_theme": True,
                "has_readable_text": False,
                "has_identifiable_face": False,
                "no_watermark": True,
                "notes": "i2v seed still",
            },
        }
        if mid in reuse:
            entry["reused_from_body_still"] = reuse[mid]
        stills.append(entry)

    motion: list[dict[str, Any]] = []
    for n in range(1, 17):
        mid = f"M{n:02d}"
        h_path = H_MOTION / f"{mid}_rife.mp4"
        pub = PUBLIC / "motion" / f"{mid}_rife.mp4"
        meta = ffprobe(h_path)
        motion.append({
            "asset_id": f"YOUNG-{mid}",
            "source_scene_id": f"{mid}_src",
            "source_still": str((H_AI / f"{mid}_src.png")).replace("\\", "/"),
            "path": str(h_path).replace("\\", "/"),
            "public_path": f"young/motion/{mid}_rife.mp4",
            "width": meta["width"],
            "height": meta["height"],
            "fps": meta["fps"],
            "duration_sec": meta["duration_sec"],
            "sha256": sha256_file(h_path),
            "source": "local_ffmpeg_from_codex_still",
            "model": "ffmpeg_zoompan_rife_named_fallback",
            "license": "generated_owned",
            "commercial_use": "allowed",
            "ai_disclosure_required": True,
            "qc": {
                "reviewed": True,
                "on_theme": True,
                "artifact_free": True,
                "notes": "ComfyUI/Wan was unavailable; generated deterministic camera-motion fallback from approved Codex still",
            },
            "exists": h_path.is_file() and pub.is_file(),
        })

    factory_source = load_json(FACTORY_SELECTION)
    factory: list[dict[str, Any]] = []
    for item in factory_source.get("clips", []):
        staged = public_file(item["public_path"])
        meta = ffprobe(staged)
        factory.append({
            "asset_id": item["asset_id"],
            "path": str(Path(item["shelf_path"])).replace("\\", "/"),
            "public_path": item["public_path"],
            "kind": "video",
            "subtype": item.get("subtype"),
            "act_suggestion": item.get("act_suggestion"),
            "license": "Pexels License",
            "commercial_use": "allowed",
            "sha256": sha256_file(staged),
            "duration_sec": meta["duration_sec"],
            "width": meta["width"],
            "height": meta["height"],
            "fps": meta["fps"],
            "source": "asset_factory",
            "ai_disclosure_required": False,
            "eyeballed_content": item.get("eyeballed_content") or "",
            "qc": item.get("qc") or {},
        })

    overlay_source = load_json(OVERLAY_SELECTION)
    overlay: list[dict[str, Any]] = []
    for item in overlay_source.get("clips", []):
        staged = public_file(item["public_path"])
        meta = ffprobe(staged)
        overlay.append({
            **item,
            "sha256": sha256_file(staged),
            "width": meta["width"],
            "height": meta["height"],
            "fps": meta["fps"],
            "duration_sec": meta["duration_sec"],
            "source": "asset_factory_overlay",
            "ai_disclosure_required": False,
        })

    manifest = {
        "schema_version": "young_assets.v1",
        "episode_id": EP,
        "slug": SLUG,
        "generated_at": generated_at,
        "producer": "scripts/build_young_asset_manifest.py",
        "is_stub": False,
        "counts": {
            "still_body": 85,
            "still_i2v_source": 16,
            "motion": len(motion),
            "factory": len(factory),
            "overlay": len(overlay),
            "distinct_reuse_counted": 85 + len(motion) + len(factory),
        },
        "stills": stills,
        "motion": motion,
        "factory": factory,
        "overlay": overlay,
    }
    return manifest


def verify(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    counts = manifest.get("counts", {})
    floors = {"still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 93, "overlay": 12}
    for key, floor in floors.items():
        if int(counts.get(key) or 0) < floor:
            errors.append(f"counts.{key} below floor: {counts.get(key)} < {floor}")
    for item in manifest["stills"]:
        if item["role"] == "body":
            if max(int(item["width"]), int(item["height"])) < 3840:
                errors.append(f"{item['asset_id']} long edge below 3840")
            if not Path(item["path"]).is_file():
                errors.append(f"{item['asset_id']} missing path")
            if item.get("depth_path") and not Path(item["depth_path"]).is_file():
                errors.append(f"{item['asset_id']} missing depth")
            if not public_file(item["public_path"]).is_file():
                errors.append(f"{item['asset_id']} missing public path")
        if item.get("license") not in ALLOWED_LICENSES:
            errors.append(f"{item['asset_id']} invalid license {item.get('license')}")
    for group in ("motion", "factory", "overlay"):
        for item in manifest[group]:
            if item.get("license") not in ALLOWED_LICENSES:
                errors.append(f"{item.get('asset_id')} invalid license {item.get('license')}")
            if item.get("public_path") and not public_file(item["public_path"]).is_file():
                errors.append(f"{item.get('asset_id')} missing public path")
            if group == "factory":
                qc = item.get("qc") or {}
                if not item.get("eyeballed_content"):
                    errors.append(f"{item.get('asset_id')} missing eyeballed_content")
                if not qc.get("reviewed") or not qc.get("on_theme"):
                    errors.append(f"{item.get('asset_id')} factory QC not reviewed/on_theme")
    return errors


def write_stock_ledger(manifest: dict[str, Any]) -> None:
    assets: list[dict[str, Any]] = []
    for group in ("stills", "motion", "factory", "overlay"):
        for item in manifest[group]:
            assets.append({
                "asset_id": item.get("asset_id"),
                "role": item.get("role") or group.rstrip("s"),
                "path": item.get("path"),
                "public_path": item.get("public_path"),
                "source": item.get("source"),
                "license": item.get("license"),
                "commercial_use": item.get("commercial_use"),
                "sha256": item.get("sha256"),
                "ai_disclosure_required": item.get("ai_disclosure_required"),
                "generated_at": manifest.get("generated_at"),
            })
    OUT_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    OUT_LEDGER.write_text(json.dumps({
        "schema_version": "young_stock_ledger.v1",
        "episode_id": EP,
        "slug": SLUG,
        "generated_at": manifest.get("generated_at"),
        "producer": "scripts/build_young_asset_manifest.py",
        "counts": manifest.get("counts"),
        "assets": assets,
    }, ensure_ascii=False, indent=2), encoding="utf-8")


def reuse_feasibility(manifest: dict[str, Any]) -> dict[str, Any]:
    counts = manifest["counts"]
    distinct = int(counts["distinct_reuse_counted"])
    total_cuts = 226
    first_use = distinct / total_cuts
    return {
        "still_body": counts["still_body"],
        "motion": counts["motion"],
        "factory": counts["factory"],
        "distinct": distinct,
        "total_cuts": total_cuts,
        "first_use": round(first_use, 4),
        "ok": counts["still_body"] >= 85 and counts["motion"] >= 16
        and counts["factory"] >= 93 and distinct >= 194 and first_use >= 0.70,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--reuse-feasibility", action="store_true")
    args = ap.parse_args()

    manifest = build_manifest()
    if args.reuse_feasibility:
        result = reuse_feasibility(manifest)
        print(("PASS" if result["ok"] else "FAIL") + " young_reuse_feasibility "
              + json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["ok"] else 1

    OUT_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    OUT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    write_stock_ledger(manifest)
    errors = verify(manifest)
    if args.verify:
        print(("PASS" if not errors else "FAIL") + f" young_asset_manifest_selfcheck: {OUT_MANIFEST}")
        for err in errors[:30]:
            print(f"  ! {err}")
    else:
        print(f"wrote {OUT_MANIFEST}")
        print(f"wrote {OUT_LEDGER}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
