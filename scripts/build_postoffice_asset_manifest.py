#!/usr/bin/env python
"""Build or verify the EP56 Post Office A-side asset manifest.

This script is intentionally a producer-side boundary checker. It does not
fabricate missing factory, motion, or overlay rows as accepted assets; missing
media stays a hard failure until the A-side generation/selection work exists.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-056-postoffice"
SLUG = "postoffice"
PLAN = ROOT / "episodes" / "_planning" / "EP56_postoffice_CODEX_A_ASSETS.v001.md"
EP_DIR = ROOT / "episodes" / EP
SCENES = EP_DIR / "04_scenes"
VISUALS = EP_DIR / "05_visuals"
STOCK = EP_DIR / "05_stock"
MANIFEST = VISUALS / "asset_manifest.v001.json"
MEDIA_AI = Path("E:/pd-media/assets/ai/postoffice")
MEDIA_VIDEO = Path("E:/pd-media/assets/ai_video/postoffice")
PUBLIC = ROOT / "remotion" / "public" / SLUG

EXPECTED = {
    "still_body": 210,
    "still_i2v_source": 42,
    "motion": 42,
    "factory": 235,
    "overlay": 30,
    "thumb_face": 3,
}
THUMB_BODY_IDS = {"S001", "S057", "S106", "S173"}
VALID_ROLES = {"body", "i2v_source", "thumb_face", "reject"}
ALLOWED_LICENSES = {"cc0", "royalty_free", "generated_owned", "Pexels License", "Pixabay Content License"}
MOTION_FPS = 48
MOTION_MIN_FRAMES = 156

BANNED_TEXT = re.compile(
    r"thief|fraudster|criminal ceo|executives jailed|vennells convicted|jenkins guilty|"
    r"self-harm|noose|farewell note|dochighlight|milky haze|scanline|"
    r"post office logo|royal mail logo|fujitsu logo|itv logo|bbc logo|crown emblem",
    re.IGNORECASE,
)


def mkdirs() -> None:
    for path in [
        SCENES,
        VISUALS,
        STOCK,
        MEDIA_AI,
        MEDIA_VIDEO,
        PUBLIC / "img",
        PUBLIC / "factory",
        PUBLIC / "motion",
        PUBLIC / "overlay",
        PUBLIC / "thumb",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size


def ffprobe(path: Path) -> dict[str, Any]:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,avg_frame_rate,nb_frames,duration",
        "-of",
        "json",
        str(path),
    ]
    try:
        data = json.loads(subprocess.check_output(cmd, text=True))
        stream = (data.get("streams") or [{}])[0]
    except Exception:
        return {}
    fps_s = str(stream.get("avg_frame_rate") or "0/1")
    num, _, den = fps_s.partition("/")
    fps = float(num) / max(1.0, float(den or 1))
    duration = float(stream.get("duration") or 0)
    frames = int(stream.get("nb_frames") or round(duration * fps) or 0)
    return {
        "width": int(stream.get("width") or 0),
        "height": int(stream.get("height") or 0),
        "fps": round(fps, 3),
        "frames": frames,
        "duration_sec": round(duration, 3),
    }


def parse_json_entries(section_start: str, section_end: str, expected: int) -> list[dict[str, Any]]:
    text = PLAN.read_text(encoding="utf-8")
    start = text.index(section_start)
    end = text.index(section_end, start)
    raw_entries = re.findall(r"^\s*(\{[^\n]+\})\s*$", text[start:end], flags=re.MULTILINE)
    items = [json.loads(raw) for raw in raw_entries]
    if len(items) != expected:
        raise SystemExit(f"{section_start} expected {expected} entries, got {len(items)}")
    return items


def factory_specs() -> list[dict[str, Any]]:
    return parse_json_entries("## 4.4", "## 4.5", 235)


def motion_specs() -> list[dict[str, Any]]:
    return parse_json_entries("## 4.5", "## 4.6", 42)


def overlay_specs() -> list[dict[str, Any]]:
    return parse_json_entries("## 4.6", "# 5.", 30)


def read_prompt_files() -> set[str]:
    path = SCENES / "ai_prompts.v001.md"
    if not path.is_file():
        return set()
    return set(re.findall(r"^\s*-\s+`([^`]+\.png)`\s*$", path.read_text(encoding="utf-8-sig"), re.MULTILINE))


def still_entry(asset_id: str, role: str, file_name: str, public_path: str | None) -> dict[str, Any]:
    path = MEDIA_AI / file_name
    item: dict[str, Any] = {
        "asset_id": asset_id,
        "scene_id": asset_id.replace("POH-", "").replace("MS", "MS"),
        "role": role,
        "path": path.as_posix(),
        "public_path": public_path,
        "also_thumb": asset_id.removeprefix("POH-") in THUMB_BODY_IDS if role == "body" else False,
        "ai_disclosure_required": True,
        "qc": {
            "has_readable_text": False,
            "has_identifiable_real_person": False,
            "has_suicide_or_grief_imagery": False,
            "accepted_pending_visual_review": False,
        },
    }
    if path.is_file():
        width, height = image_size(path)
        item.update({"width": width, "height": height, "sha256": sha256(path)})
    return item


def build_stills() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for i in range(1, 211):
        sid = f"S{i:03d}"
        items.append(still_entry(f"POH-{sid}", "body", f"{sid}.png", f"postoffice/img/{sid}.png"))
    for i in range(1, 43):
        sid = f"MS{i:02d}"
        items.append(still_entry(f"POH-{sid}", "i2v_source", f"M{i:02d}_src.png", None))
    for i in range(1, 4):
        sid = f"T{i:02d}"
        items.append(still_entry(f"POH-{sid}", "thumb_face", f"T{i:02d}_face.png", None))
    return items


def load_selection(path: Path, key: str) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("items", data if isinstance(data, list) else [])
    return {str(item.get(key) or item.get("public_path")): item for item in rows if isinstance(item, dict)}


def build_factory() -> list[dict[str, Any]]:
    selected = load_selection(STOCK / "factory_selection.v001.json", "public_path")
    rows = []
    for idx, spec in enumerate(factory_specs(), start=1):
        public_path = spec["public_path"]
        base = selected.get(public_path, {})
        path = Path(str(base.get("path") or (PUBLIC / public_path.removeprefix("postoffice/"))))
        item = {
            "asset_id": base.get("asset_id") or f"POH-F{idx:03d}",
            **spec,
            "path": path.as_posix(),
            "origin": base.get("origin") or "unselected",
            "license": base.get("license"),
            "eyeballed_content": base.get("eyeballed_content"),
            "qc": base.get("qc") or {},
        }
        if path.is_file():
            item.update(ffprobe(path))
            item["sha256"] = sha256(path)
        rows.append(item)
    return rows


def build_motion() -> list[dict[str, Any]]:
    rows = []
    for spec in motion_specs():
        path = Path(spec["path"])
        item = {**spec, "ai_disclosure_required": True}
        if path.is_file():
            item.update(ffprobe(path))
            item["sha256"] = sha256(path)
        rows.append(item)
    return rows


def build_overlay() -> list[dict[str, Any]]:
    selected = load_selection(STOCK / "overlay_selection.v001.json", "public_path")
    rows = []
    for idx, spec in enumerate(overlay_specs(), start=1):
        public_path = spec["public_path"]
        base = selected.get(public_path, {})
        path = Path(str(base.get("path") or (PUBLIC / public_path.removeprefix("postoffice/"))))
        item = {
            "asset_id": base.get("asset_id") or f"POH-O{idx:02d}",
            **spec,
            "path": path.as_posix(),
            "origin": base.get("origin") or "unselected",
            "license": base.get("license"),
            "eyeballed_content": base.get("eyeballed_content"),
            "qc": base.get("qc") or {},
        }
        if path.is_file():
            item.update(ffprobe(path))
            item["sha256"] = sha256(path)
        rows.append(item)
    return rows


def stock_ledger(items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "postoffice_stock_ledger.v1",
        "episode_id": EP,
        "items": [
            {
                "asset_id": item.get("asset_id"),
                "path": item.get("path"),
                "source": "ai_codex" if item.get("ai_disclosure_required") else item.get("origin"),
                "origin": item.get("origin") or ("ai" if item.get("ai_disclosure_required") else None),
                "license": item.get("license") or ("generated_owned" if item.get("ai_disclosure_required") else None),
                "commercial_use": True,
                "sha256": item.get("sha256"),
                "ai_disclosure_required": bool(item.get("ai_disclosure_required")),
            }
            for item in items
        ],
    }


def build_manifest() -> dict[str, Any]:
    mkdirs()
    stills = build_stills()
    factory = build_factory()
    motion = build_motion()
    overlay = build_overlay()
    counts = {
        "still_body": len([x for x in stills if x["role"] == "body"]),
        "still_i2v_source": len([x for x in stills if x["role"] == "i2v_source"]),
        "motion": len(motion),
        "factory": len(factory),
        "overlay": len(overlay),
        "thumb_face": len([x for x in stills if x["role"] == "thumb_face"]),
    }
    manifest = {
        "schema_version": "postoffice_assets.v1",
        "episode_id": EP,
        "slug": SLUG,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "producer": "scripts/build_postoffice_asset_manifest.py",
        "is_stub": False,
        "counts": counts,
        "expected_counts": EXPECTED,
        "source_inputs": {"asset_spec": PLAN.relative_to(ROOT).as_posix()},
        "safety_locks": {
            "innocent_victims_framing": True,
            "no_real_person_likeness": True,
            "no_suicide_or_grief_imagery": True,
            "no_real_logo_or_readable_fake_text": True,
            "no_depth_path": True,
            "ai_disclosure_required": True,
        },
        "stills": stills,
        "motion": motion,
        "factory": factory,
        "overlay": overlay,
        "asset_mix_recalculation": {
            "total_cuts": 563,
            "still_cuts": 244,
            "factory_cuts": 235,
            "motion_cuts": 84,
            "distinct_sources": 487,
            "still_share": round(244 / 563, 4),
            "motion_coverage": round((235 + 84) / 563, 4),
            "first_use_share": round(487 / 563, 4),
            "avg_uses_per_source": round(563 / 487, 3),
        },
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (STOCK / "stock_ledger.v001.json").write_text(
        json.dumps(stock_ledger(stills + motion + factory + overlay), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def exists(path: str | None) -> bool:
    if not path:
        return False
    p = Path(path)
    return p.is_file() or (ROOT / "remotion" / "public" / path).is_file()


def collect_prior_sha() -> set[str]:
    out: set[str] = set()
    for ep_dir in (ROOT / "episodes").glob("PD-2026-0[3-5][0-9]-*"):
        try:
            ep_num = int(ep_dir.name.split("-")[2])
        except Exception:
            continue
        if not 39 <= ep_num <= 55:
            continue
        for path in list(ep_dir.glob("05_stock/stock_ledger*.json")) + list(ep_dir.glob("05_visuals/asset_manifest*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if isinstance(data, dict):
                for key in ["items", "stills", "factory", "motion", "overlay"]:
                    for item in data.get(key, []) or []:
                        if isinstance(item, dict) and item.get("sha256"):
                            out.add(str(item["sha256"]))
    return out


def evaluate(data: dict[str, Any], check_prior_overlap: bool = False) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "postoffice_assets.v1":
        errors.append(f"schema_version mismatch: {data.get('schema_version')}")
    if data.get("episode_id") != EP or data.get("slug") != SLUG:
        errors.append("episode identity mismatch")
    if data.get("is_stub") is not False:
        errors.append("is_stub must be false")
    if any("depth_path" in item for item in data.get("stills", []) + data.get("motion", [])):
        errors.append("depth_path must not exist")
    prompt_files = read_prompt_files()
    expected_prompt_files = {f"S{i:03d}.png" for i in range(1, 211)}
    expected_prompt_files |= {f"M{i:02d}_src.png" for i in range(1, 43)}
    expected_prompt_files |= {f"T{i:02d}_face.png" for i in range(1, 4)}
    if prompt_files and prompt_files != expected_prompt_files:
        errors.append(f"ai_prompts base set mismatch missing={len(expected_prompt_files - prompt_files)} extra={len(prompt_files - expected_prompt_files)}")
    stills = data.get("stills") or []
    groups = {"motion": data.get("motion") or [], "factory": data.get("factory") or [], "overlay": data.get("overlay") or []}
    actual = {
        "still_body": len([x for x in stills if x.get("role") == "body"]),
        "still_i2v_source": len([x for x in stills if x.get("role") == "i2v_source"]),
        "motion": len(groups["motion"]),
        "factory": len(groups["factory"]),
        "overlay": len(groups["overlay"]),
        "thumb_face": len([x for x in stills if x.get("role") == "thumb_face"]),
    }
    for key, expected in EXPECTED.items():
        if (data.get("counts") or {}).get(key) != expected:
            errors.append(f"counts.{key} expected {expected} got {(data.get('counts') or {}).get(key)}")
        if actual[key] != expected:
            errors.append(f"actual {key} expected {expected} got {actual[key]}")
    roles = {item.get("role") for item in stills}
    if not roles <= VALID_ROLES:
        errors.append(f"invalid roles: {sorted(str(x) for x in roles - VALID_ROLES)}")
    also_thumb = {item.get("scene_id").replace("POH-", "") for item in stills if item.get("also_thumb") is True}
    if also_thumb != THUMB_BODY_IDS:
        errors.append(f"also_thumb set {sorted(also_thumb)} != {sorted(THUMB_BODY_IDS)}")
    public_paths: list[str] = []
    seen_sha: set[str] = set()
    for group, items in [("stills", stills), *groups.items()]:
        for i, item in enumerate(items):
            role = item.get("role")
            public_path = item.get("public_path")
            if group == "stills" and role != "body" and public_path is not None:
                errors.append(f"stills[{i}] non-body public_path must be null")
            if group == "stills" and role == "body" and not public_path:
                errors.append(f"stills[{i}] body missing public_path")
            if group != "stills" and not public_path:
                errors.append(f"{group}[{i}] missing public_path")
            if public_path:
                public_paths.append(str(public_path))
                if not exists(str(public_path)):
                    errors.append(f"{group}[{i}] missing public media: {public_path}")
            path = item.get("path")
            if path and not exists(str(path)):
                errors.append(f"{group}[{i}] missing path: {path}")
            if item.get("sha256"):
                if item["sha256"] in seen_sha:
                    errors.append(f"{group}[{i}] duplicate sha256")
                seen_sha.add(str(item["sha256"]))
            if group == "stills" and role != "reject":
                if max(int(item.get("width") or 0), int(item.get("height") or 0)) < 3840:
                    errors.append(f"stills[{i}] long edge below 3840 or missing")
            if group == "factory":
                if "/factory/" not in str(public_path).replace("\\", "/"):
                    errors.append(f"factory[{i}] public_path must include /factory/")
                if item.get("origin") not in {"factory", "stock"}:
                    errors.append(f"factory[{i}] origin not selected")
                if item.get("license") not in ALLOWED_LICENSES:
                    errors.append(f"factory[{i}] bad license {item.get('license')}")
                if not item.get("eyeballed_content"):
                    errors.append(f"factory[{i}] missing eyeballed_content")
                if (item.get("qc") or {}).get("label_matches_content") is not True:
                    errors.append(f"factory[{i}] label_matches_content must be true")
            if group == "motion":
                if "/motion/" not in str(public_path).replace("\\", "/"):
                    errors.append(f"motion[{i}] public_path must include /motion/")
                if int(item.get("frames") or 0) < MOTION_MIN_FRAMES:
                    errors.append(f"motion[{i}] SHORT or missing frames={item.get('frames')}")
                if round(float(item.get("fps") or 0)) != MOTION_FPS:
                    errors.append(f"motion[{i}] fps expected 48 got {item.get('fps')}")
            if group == "overlay":
                if "/overlay/" not in str(public_path).replace("\\", "/"):
                    errors.append(f"overlay[{i}] public_path must include /overlay/")
                if item.get("origin") not in {"factory", "stock"}:
                    errors.append(f"overlay[{i}] origin not selected")
                if item.get("license") not in ALLOWED_LICENSES:
                    errors.append(f"overlay[{i}] bad license {item.get('license')}")
                if not item.get("eyeballed_content"):
                    errors.append(f"overlay[{i}] missing eyeballed_content")
    dup_public = [p for p, n in Counter(public_paths).items() if n > 1]
    if dup_public:
        errors.append(f"duplicate public_path: {dup_public[:5]}")
    text_blob = json.dumps(data, ensure_ascii=False)
    match = BANNED_TEXT.search(text_blob)
    if match:
        errors.append(f"banned wording present: {match.group(0)}")
    if check_prior_overlap:
        prior = collect_prior_sha()
        current = {str(item.get("sha256")) for item in groups["factory"] if item.get("sha256")}
        overlap = sorted(current & prior)
        if overlap:
            errors.append(f"factory prior sha overlap count={len(overlap)} first={overlap[:5]}")
    return errors


def reuse_feasibility(data: dict[str, Any]) -> list[str]:
    body_items = [x for x in data.get("stills", []) if x.get("role") == "body"]
    factory_items = data.get("factory") or []
    motion_items = data.get("motion") or []
    body = len([x for x in body_items if x.get("sha256")])
    factory = len([x for x in factory_items if x.get("sha256")])
    motion = len([x for x in motion_items if x.get("sha256")])
    distinct = body + factory + motion
    checks = {
        "still": (body, 210),
        "factory": (factory, 235),
        "motion": (motion, 42),
        "distinct": (distinct, 487),
    }
    errors = [f"{name} {got} < {want}" for name, (got, want) in checks.items() if got < want]
    first_use = distinct / 563
    avg_uses = 563 / max(1, distinct)
    if first_use < 0.70:
        errors.append(f"first-use {first_use:.4f} < 0.70")
    if avg_uses > 1.4:
        errors.append(f"avg-uses/source {avg_uses:.3f} > 1.4")
    if 244 / 563 > 0.45:
        errors.append("still_share exceeds 0.45")
    return errors


def load_manifest() -> dict[str, Any]:
    if not MANIFEST.is_file():
        raise SystemExit(f"missing {MANIFEST}")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--reuse-feasibility", action="store_true")
    ap.add_argument("--verify-no-prior-overlap", action="store_true")
    ap.add_argument("--stage", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    data = load_manifest() if (args.verify or args.reuse_feasibility or args.verify_no_prior_overlap) else build_manifest()
    if args.stage:
        stage_assets()
        data = build_manifest()

    if args.reuse_feasibility:
        errors = reuse_feasibility(data)
        label = "postoffice_reuse_feasibility"
    elif args.verify_no_prior_overlap:
        errors = evaluate(data, check_prior_overlap=True)
        label = "postoffice_factory_prior_overlap"
    else:
        errors = evaluate(data)
        label = "postoffice_asset_manifest"

    result = {"ok": not errors, "asset_manifest": str(MANIFEST), "counts": data.get("counts"), "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["ok"] else "FAIL") + f" {label}: {MANIFEST}")
        print(json.dumps(data.get("counts"), ensure_ascii=False))
        for err in errors[:120]:
            print(f"  ! {err}")
    return 0 if not errors else 1


def stage_assets() -> None:
    mkdirs()
    for i in range(1, 211):
        src = MEDIA_AI / f"S{i:03d}.png"
        dst = PUBLIC / "img" / src.name
        if src.is_file() and (not dst.is_file() or sha256(src) != sha256(dst)):
            shutil.copyfile(src, dst)
    for i in range(1, 4):
        src = MEDIA_AI / f"T{i:02d}_face.png"
        dst = PUBLIC / "thumb" / src.name
        if src.is_file() and (not dst.is_file() or sha256(src) != sha256(dst)):
            shutil.copyfile(src, dst)
    for i in range(1, 43):
        src = MEDIA_VIDEO / f"M{i:02d}_rife.mp4"
        dst = PUBLIC / "motion" / src.name
        if src.is_file() and (not dst.is_file() or sha256(src) != sha256(dst)):
            shutil.copyfile(src, dst)


if __name__ == "__main__":
    raise SystemExit(main())
