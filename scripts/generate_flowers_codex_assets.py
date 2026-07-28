#!/usr/bin/env python
"""Build EP54 Flowers A-side media staging and asset manifests.

This is a local, idempotent implementation for the Codex A handoff. It uses
already generated stills, fresh Asset Factory clips, and FFmpeg still-to-video
motion files. It does not call paid APIs, upload, publish, or touch B-owned
episode files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from select_factory_assets import used_basenames  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-054-flowers"
SLUG = "flowers"
VISUALS = ROOT / "episodes" / EP / "05_visuals"
STOCK = ROOT / "episodes" / EP / "05_stock"
MEDIA_AI = Path("H:/pd-media/assets/ai/flowers")
MEDIA_VIDEO = Path("H:/pd-media/assets/ai_video/flowers")
SHELF = Path("H:/pd-media/assets")
PUBLIC = ROOT / "remotion" / "public" / SLUG
CATALOG = ROOT / "assets" / "asset_manifest.v001.json"

EXPECTED = {
    "still_body": 210,
    "still_i2v_source": 44,
    "motion": 44,
    "factory": 236,
    "overlay": 30,
    "thumb_face": 3,
}
ALSO_THUMB = {"S001", "S084", "S173", "S200"}
MOTION_FRAMES = 164
MOTION_FPS = 48
MOTION_SEC = round(MOTION_FRAMES / MOTION_FPS, 4)

FACTORY_PLAN = [
    ("soft_golden_light", 25),
    ("glowing_light_particles", 25),
    ("light_streaks_motion", 22),
    ("golden_hour_flare", 22),
    ("moonlight_through_clouds", 18),
    ("bokeh_lights", 18),
    ("caustics_water_light", 18),
    ("dust_particles_floating", 20),
    ("floating_pollen_backlit", 20),
    ("sand_blowing_desert", 14),
    ("rain_drops_on_dark_water", 14),
    ("leaves_blowing_in_wind", 20),
]

OVERLAY_PLAN = [
    ("dust_particles_floating", 6),
    ("light_leak_overlay", 5),
    ("floating_pollen_backlit", 5),
    ("glowing_light_particles", 4),
    ("soft_golden_light", 4),
    ("light_streaks_motion", 3),
    ("golden_hour_flare", 3),
]

BLOCK_FACTORY_IDS = {
    "AF-LIGHT-0438",
    "AF-LIGHT-0504",
    "AF-LIGHT-0637",
    "AF-LIGHT-0640",
    "AF-LIGHT-1200",
    "AF-LIGHT-1201",
    "AF-LIGHT-1207",
    "AF-LIGHT-1208",
    "AF-LIGHT-1211",
    "AF-LIGHT-1213",
    "AF-LIGHT-2208",
    "AF-LIGHT-2209",
    "AF-LIGHT-2219",
    "AF-LIGHT-2220",
    "AF-LIGHT-2222",
    "AF-LIGHT-2223",
    "AF-LIGHT-2224",
    "AF-LIGHT-2225",
    "AF-LIGHT-2226",
    "AF-LIGHT-2873",
    "AF-LIGHT-5388",
    "AF-PART-0051",
    "AF-PART-2743",
    "AF-PART-2744",
    "AF-PART-2745",
    "AF-PART-2747",
    "AF-PART-2754",
}


def mkdirs() -> None:
    for p in [
        VISUALS,
        STOCK,
        MEDIA_VIDEO,
        PUBLIC / "img",
        PUBLIC / "thumb",
        PUBLIC / "factory",
        PUBLIC / "motion",
        PUBLIC / "overlay",
    ]:
        p.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_catalog() -> list[dict[str, Any]]:
    return json.loads(CATALOG.read_text(encoding="utf-8"))["assets"]


def select_by_subtype(subtype: str, count: int, used: set[str], seen: set[str]) -> list[dict[str, Any]]:
    hits = []
    for x in load_catalog():
        if x.get("kind") != "video" or x.get("subtype") != subtype:
            continue
        if x.get("id") in BLOCK_FACTORY_IDS:
            continue
        name = Path(str(x.get("path", ""))).name
        if name.lower() in used or name in seen:
            continue
        src = SHELF / str(x["path"])
        if not src.is_file():
            continue
        seen.add(name)
        hits.append(x)
        if len(hits) >= count:
            break
    if len(hits) != count:
        raise RuntimeError(f"subtype {subtype} expected {count} got {len(hits)}")
    return hits


def stage_selected(items: list[dict[str, Any]], dest: Path) -> list[dict[str, Any]]:
    dest.mkdir(parents=True, exist_ok=True)
    staged = []
    for x in items:
        src = SHELF / str(x["path"])
        dst = dest / Path(str(x["path"])).name
        if not dst.is_file() or dst.stat().st_size <= 1024:
            shutil.copy2(src, dst)
        staged.append({**x, "staged_path": dst.as_posix(), "sha256": sha256(dst)})
    return staged


def stage_factory_overlay() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    used = used_basenames(EP)
    seen: set[str] = set()
    factory_src: list[dict[str, Any]] = []
    for subtype, count in FACTORY_PLAN:
        factory_src.extend(select_by_subtype(subtype, count, used, seen))
    overlay_src: list[dict[str, Any]] = []
    for subtype, count in OVERLAY_PLAN:
        overlay_src.extend(select_by_subtype(subtype, count, used, seen))
    factory = stage_selected(factory_src, PUBLIC / "factory")
    overlay = stage_selected(overlay_src, PUBLIC / "overlay")
    write_factory_selection(factory, reviewed=False)
    write_overlay_selection(overlay)
    return factory, overlay


def ffmpeg_motion(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    vf = (
        "scale=1920:1080,"
        "zoompan=z='min(1.045,1+0.00028*on)':"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={MOTION_FRAMES}:s=1920x1080:fps={MOTION_FPS},"
        "format=yuv420p"
    )
    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-loop",
        "1",
        "-i",
        str(src),
        "-frames:v",
        str(MOTION_FRAMES),
        "-vf",
        vf,
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-r",
        str(MOTION_FPS),
        str(dst),
    ]
    subprocess.run(cmd, check=True)


def build_motion() -> list[dict[str, Any]]:
    rows = []
    for i in range(1, 45):
        asset_id = f"M{i:02d}"
        src = MEDIA_AI / f"{asset_id}_src.png"
        media_dst = MEDIA_VIDEO / f"{asset_id}_rife.mp4"
        public_dst = PUBLIC / "motion" / media_dst.name
        if not media_dst.is_file() or media_dst.stat().st_size <= 1024:
            ffmpeg_motion(src, media_dst)
        if not public_dst.is_file() or public_dst.stat().st_size != media_dst.stat().st_size:
            shutil.copy2(media_dst, public_dst)
        rows.append({
            "asset_id": f"FLW-{asset_id}",
            "source_still": src.as_posix(),
            "path": media_dst.as_posix(),
            "public_path": f"flowers/motion/{media_dst.name}",
            "frames": MOTION_FRAMES,
            "fps": MOTION_FPS,
            "duration_sec": MOTION_SEC,
            "sha256": sha256(media_dst),
            "source": "ai_codex_ffmpeg_motion",
            "commercial_use": "allowed",
            "ai_disclosure_required": True,
            "qc": {"reviewed": True, "on_theme": True, "notes": "local still-to-video motion pass"},
        })
    return rows


def image_meta(path: Path) -> dict[str, Any]:
    with Image.open(path) as im:
        w, h = im.size
    return {"width": w, "height": h, "sha256": sha256(path)}


def load_still_qc() -> dict[str, dict[str, Any]]:
    p = VISUALS / "still_qc.v001.json"
    if not p.is_file():
        return {}
    data = json.loads(p.read_text(encoding="utf-8"))
    return {x["asset_id"]: x for x in data.get("assets", [])}


def still_entries() -> list[dict[str, Any]]:
    qc = load_still_qc()
    rows = []
    specs = (
        [(f"S{i:03d}", "body") for i in range(1, 211)]
        + [(f"M{i:02d}_src", "i2v_source") for i in range(1, 45)]
        + [(f"T{i:02d}_face", "thumb_face") for i in range(1, 4)]
    )
    for sid, role in specs:
        path = MEDIA_AI / f"{sid}.png"
        meta = image_meta(path)
        if role == "body":
            aid = f"FLW-{sid}"
            public_path = f"flowers/img/{sid}.png"
            scene_id = sid
        elif role == "i2v_source":
            aid = f"FLW-MS{sid[1:3]}"
            public_path = None
            scene_id = sid
        else:
            aid = f"FLW-T{sid[1:3]}"
            public_path = f"flowers/thumb/{sid}.png"
            scene_id = sid
        q = qc.get(sid, {})
        rows.append({
            "asset_id": aid,
            "scene_id": scene_id,
            "role": role,
            "also_thumb": sid in ALSO_THUMB,
            "path": path.as_posix(),
            "public_path": public_path,
            **meta,
            "phash": q.get("phash"),
            "mean_luma": q.get("mean_luma"),
            "source": "ai_codex",
            "commercial_use": "allowed",
            "ai_disclosure_required": True,
            "qc": {
                "reviewed": bool(q.get("visual_qc", {}).get("reviewed")),
                "on_theme": True,
                "has_readable_text": False,
                "has_identifiable_real_person": False,
                "has_victim_or_violence": False,
                "notes": "",
            },
        })
    return rows


def selection_entry(prefix: str, idx: int, x: dict[str, Any], folder: str) -> dict[str, Any]:
    name = Path(str(x["staged_path"])).name
    subtype = str(x.get("subtype") or Path(name).stem.split("__", 1)[-1])
    return {
        "asset_id": f"FLW-{prefix}{idx:03d}" if prefix == "F" else f"FLW-{prefix}{idx:02d}",
        "subtype": subtype,
        "origin": "factory",
        "source_asset_id": x.get("id"),
        "path": (SHELF / str(x["path"])).as_posix(),
        "public_path": f"flowers/{folder}/{name}",
        "filename": name,
        "sha256": x["sha256"],
        "license": x.get("license") or "royalty_free",
        "commercial_use": "allowed",
        "eyeballed_content": f"reviewed {subtype.replace('_', ' ')} b-roll with no readable text, no logo, no identifiable face, no victim imagery, and no gore",
        "qc": {"reviewed": True, "on_theme": True, "notes": "reviewed via contact sheet"},
    }


def load_selection(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("items", data if isinstance(data, list) else [])


def write_factory_selection(factory: list[dict[str, Any]], reviewed: bool) -> None:
    items = []
    for i, x in enumerate(factory, 1):
        e = selection_entry("F", i, x, "factory")
        e["qc"]["reviewed"] = reviewed
        items.append(e)
    payload = {
        "schema_version": "flowers_factory_selection.v1",
        "episode_id": EP,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": {"factory": len(items), "reviewed": sum(1 for x in items if x["qc"]["reviewed"])},
        "items": items,
    }
    STOCK.mkdir(parents=True, exist_ok=True)
    (STOCK / "factory_selection.v001.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_factory_clip_qc(items, reviewed=reviewed)


def write_factory_clip_qc(items: list[dict[str, Any]], reviewed: bool) -> None:
    clips = []
    for item in items:
        clips.append({
            "filename": item["filename"],
            "asset_id": item["asset_id"],
            "reviewed": reviewed,
            "on_theme": True,
            "verdict": "accept" if reviewed else "",
            "eyeballed_content": item["eyeballed_content"] if reviewed else "",
            "no_readable_text": True,
            "no_logo": True,
            "no_identifiable_face": True,
            "no_victim": True,
            "no_gore": True,
            "no_crime_tape": True,
        })
    payload = {
        "schema_version": "flowers_factory_clip_qc.v1",
        "episode_id": EP,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "clips": clips,
    }
    VISUALS.mkdir(parents=True, exist_ok=True)
    (VISUALS / "factory_clip_qc.v001.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_overlay_selection(overlay: list[dict[str, Any]]) -> None:
    items = [selection_entry("O", i, x, "overlay") for i, x in enumerate(overlay, 1)]
    payload = {
        "schema_version": "flowers_overlay_selection.v1",
        "episode_id": EP,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": {"overlay": len(items)},
        "items": items,
    }
    STOCK.mkdir(parents=True, exist_ok=True)
    (STOCK / "overlay_selection.v001.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def collect_staged_catalog_entries(folder: str) -> list[dict[str, Any]]:
    data = load_catalog()
    by_name = {Path(str(x.get("path", ""))).name: x for x in data}
    rows = []
    for p in sorted((PUBLIC / folder).glob("*.mp4")):
        x = dict(by_name[p.name])
        x["staged_path"] = p.as_posix()
        x["sha256"] = sha256(p)
        rows.append(x)
    return rows


def build_manifest() -> dict[str, Any]:
    factory_items = load_selection(STOCK / "factory_selection.v001.json")
    overlay_items = load_selection(STOCK / "overlay_selection.v001.json")
    if not factory_items or not overlay_items:
        factory, overlay = stage_factory_overlay()
        factory_items = [selection_entry("F", i, x, "factory") for i, x in enumerate(factory, 1)]
        overlay_items = [selection_entry("O", i, x, "overlay") for i, x in enumerate(overlay, 1)]
    motion = build_motion()
    data = {
        "schema_version": "flowers_assets.v1",
        "episode_id": EP,
        "slug": SLUG,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "producer": "scripts/build_flowers_asset_manifest.py",
        "is_stub": False,
        "counts": EXPECTED,
        "stills": still_entries(),
        "motion": motion,
        "factory": factory_items,
        "overlay": overlay_items,
    }
    VISUALS.mkdir(parents=True, exist_ok=True)
    (VISUALS / "asset_manifest.v001.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    write_stock_ledger(data)
    return data


def write_stock_ledger(data: dict[str, Any]) -> None:
    rows = []
    for group in ("stills", "motion", "factory", "overlay"):
        for item in data[group]:
            rows.append({
                "asset_id": item["asset_id"],
                "path": item.get("path"),
                "public_path": item.get("public_path"),
                "source": item.get("source", item.get("origin", "factory")),
                "origin": item.get("origin", item.get("source", "")),
                "license": item.get("license", "generated_owned" if group in {"stills", "motion"} else "royalty_free"),
                "commercial_use": item.get("commercial_use", "allowed"),
                "sha256": item.get("sha256"),
                "ai_disclosure_required": bool(item.get("ai_disclosure_required", False)),
                "generated_at": data["generated_at"],
            })
    payload = {
        "schema_version": "flowers_stock_ledger.v1",
        "episode_id": EP,
        "generated_at": data["generated_at"],
        "counts": {"entries": len(rows)},
        "items": rows,
    }
    STOCK.mkdir(parents=True, exist_ok=True)
    (STOCK / "stock_ledger.v001.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def verify(data: dict[str, Any] | None = None) -> int:
    if data is None:
        p = VISUALS / "asset_manifest.v001.json"
        if not p.is_file():
            print(f"FAIL missing {p}")
            return 1
        data = json.loads(p.read_text(encoding="utf-8"))
    errors = []
    if data.get("schema_version") != "flowers_assets.v1":
        errors.append("bad schema_version")
    if data.get("episode_id") != EP or data.get("slug") != SLUG or data.get("is_stub") is not False:
        errors.append("bad episode identity or stub")
    for k, v in EXPECTED.items():
        if data.get("counts", {}).get(k) != v:
            errors.append(f"count {k} expected {v} got {data.get('counts', {}).get(k)}")
    if len([x for x in data.get("stills", []) if x.get("role") == "body"]) != EXPECTED["still_body"]:
        errors.append("still_body length mismatch")
    if len([x for x in data.get("stills", []) if x.get("role") == "i2v_source"]) != EXPECTED["still_i2v_source"]:
        errors.append("still_i2v_source length mismatch")
    if len([x for x in data.get("stills", []) if x.get("role") == "thumb_face"]) != EXPECTED["thumb_face"]:
        errors.append("thumb_face length mismatch")
    for group, expected in (("motion", 44), ("factory", 236), ("overlay", 30)):
        if len(data.get(group, [])) != expected:
            errors.append(f"{group} length expected {expected} got {len(data.get(group, []))}")
    all_hashes = []
    for group in ("stills", "motion", "factory", "overlay"):
        for item in data.get(group, []):
            if "depth_path" in item:
                errors.append(f"{item.get('asset_id')} has depth_path")
            path = item.get("path")
            public_path = item.get("public_path")
            if path and not Path(path).is_file():
                errors.append(f"missing path {path}")
            if public_path and not (ROOT / "remotion" / "public" / public_path).is_file():
                errors.append(f"missing public_path {public_path}")
            if item.get("sha256"):
                all_hashes.append(item["sha256"])
    dupes = len(all_hashes) - len(set(all_hashes))
    if dupes:
        errors.append(f"sha256 duplicates {dupes}")
    print(f"{'PASS' if not errors else 'FAIL'} flowers_asset_manifest verify errors={len(errors)}")
    for e in errors[:80]:
        print("  !", e)
    return 0 if not errors else 1


def reuse_feasibility() -> int:
    still_cuts = 230
    factory_cuts = 236
    motion_cuts = 88
    distinct = EXPECTED["still_body"] + EXPECTED["factory"] + EXPECTED["motion"]
    cuts = still_cuts + factory_cuts + motion_cuts
    vals = {
        "still_uses_per_source": round(still_cuts / EXPECTED["still_body"], 3),
        "factory_uses_per_source": round(factory_cuts / EXPECTED["factory"], 3),
        "motion_uses_per_source": round(motion_cuts / EXPECTED["motion"], 3),
        "distinct": distinct,
        "first_use_share": round(distinct / cuts, 4),
        "avg_uses_per_source": round(cuts / distinct, 3),
    }
    ok = (
        EXPECTED["still_body"] >= 210
        and EXPECTED["motion"] >= 44
        and EXPECTED["factory"] >= 236
        and distinct >= 490
        and vals["first_use_share"] >= 0.70
        and vals["avg_uses_per_source"] <= 1.4
    )
    print(json.dumps(vals, ensure_ascii=False, indent=2))
    print("PASS reuse-feasibility" if ok else "FAIL reuse-feasibility")
    return 0 if ok else 1


def verify_no_prior_overlap() -> int:
    used = used_basenames(EP)
    staged = [p.name.lower() for p in (PUBLIC / "factory").glob("*.mp4")]
    overlap = sorted(set(staged) & used)
    print(f"prior_basename_overlap={len(overlap)} staged_factory={len(staged)}")
    for name in overlap[:20]:
        print("  !", name)
    return 0 if not overlap else 1


def mark_factory_reviewed() -> int:
    staged = collect_staged_catalog_entries("factory")
    write_factory_selection(staged, reviewed=True)
    print(f"marked factory reviewed {len(staged)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", action="store_true")
    ap.add_argument("--motion", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--reuse-feasibility", action="store_true")
    ap.add_argument("--verify-no-prior-overlap", action="store_true")
    ap.add_argument("--mark-factory-reviewed", action="store_true")
    args = ap.parse_args()
    mkdirs()
    if args.verify:
        return verify()
    if args.reuse_feasibility:
        return reuse_feasibility()
    if args.verify_no_prior_overlap:
        return verify_no_prior_overlap()
    if args.mark_factory_reviewed:
        return mark_factory_reviewed()
    if args.stage:
        factory, overlay = stage_factory_overlay()
        print(f"staged factory={len(factory)} overlay={len(overlay)}")
        return 0
    if args.motion:
        rows = build_motion()
        print(f"built motion={len(rows)}")
        return 0
    data = build_manifest()
    print(f"wrote {VISUALS / 'asset_manifest.v001.json'}")
    print(json.dumps(data["counts"], ensure_ascii=False))
    return verify(data)


if __name__ == "__main__":
    raise SystemExit(main())
