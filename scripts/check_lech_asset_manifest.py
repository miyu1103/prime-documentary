#!/usr/bin/env python
"""Validate EP40 Lech asset manifest from the consumer side."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "remotion" / "public"
FFPROBE = shutil.which("ffprobe") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
BANNED_ZONE = re.compile(r"supreme\s*court|最高裁|SCOTUS", re.IGNORECASE)
MIN_COUNTS = {
    "still_body": 70,
    "still_ae": 15,
    "still_i2v_source": 16,
    "still_thumb": 9,
    "motion": 16,
    "factory": 85,
    "overlay": 12,
}


def iter_strings(obj: Any, path: str = ""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_strings(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_strings(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield path, obj


def public_exists(public_path: str) -> bool:
    return (PUBLIC / public_path).exists()


def probe_video(path: Path) -> dict:
    r = subprocess.run(
        [FFPROBE, "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate,nb_read_frames,duration", "-of", "json", str(path)],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "ffprobe failed")
    stream = json.loads(r.stdout)["streams"][0]
    num, den = str(stream.get("r_frame_rate") or "0/1").split("/")
    return {
        "width": int(stream.get("width") or 0),
        "height": int(stream.get("height") or 0),
        "fps": float(num) / float(den),
        "frames": int(stream.get("nb_read_frames") or 0),
        "duration": float(stream.get("duration") or 0.0),
    }


def check(args) -> tuple[int, dict]:
    path = Path(args.assets)
    violations: list[dict] = []
    if not path.exists():
        return 1, {"ok": False, "violations": [{"rule": "missing_manifest", "path": str(path)}]}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "lech_assets.v1":
        return 2, {"ok": False, "violations": [{"rule": "schema_version", "actual": data.get("schema_version")}]}
    for k, expected in {"episode_id": "PD-2026-040-lech", "slug": "lech"}.items():
        if data.get(k) != expected:
            violations.append({"rule": k, "actual": data.get(k), "expected": expected})

    stills = data.get("stills") or []
    role_counts = {
        "still_body": sum(1 for s in stills if s.get("role") == "body"),
        "still_ae": sum(1 for s in stills if s.get("role") == "ae"),
        "still_i2v_source": sum(1 for s in stills if s.get("role") == "i2v_source"),
        "still_thumb": sum(1 for s in stills if s.get("role") == "thumb"),
        "motion": len(data.get("motion") or []),
        "factory": len(data.get("factory") or []),
        "overlay": len(data.get("overlay") or []),
    }
    counts = data.get("counts") or {}
    for k, actual in role_counts.items():
        if counts.get(k) != actual:
            violations.append({"rule": "counts_match", "field": k, "actual": counts.get(k), "expected": actual})
        if actual < MIN_COUNTS[k]:
            violations.append({"rule": "min_count", "field": k, "actual": actual, "min": MIN_COUNTS[k]})

    sha_seen: set[str] = set()
    for coll_name in ("stills", "motion", "factory", "overlay"):
        for item in data.get(coll_name) or []:
            sha = item.get("sha256")
            if not sha:
                violations.append({"rule": "sha256_required", "asset_id": item.get("asset_id")})
            elif sha in sha_seen:
                violations.append({"rule": "sha256_unique", "sha256": sha, "asset_id": item.get("asset_id")})
            sha_seen.add(sha)

    for item in stills:
        role = item.get("role")
        pp = item.get("public_path")
        if role in ("body", "ae"):
            if not pp or not public_exists(pp):
                violations.append({"rule": "still_public_exists", "asset_id": item.get("asset_id"), "public_path": pp})
            if pp:
                depth = re.sub(r"\.[^.]+$", "_depth.png", pp)
                if not public_exists(depth):
                    violations.append({"rule": "depth_public_exists", "asset_id": item.get("asset_id"), "depth_path": depth})
        if role != "thumb" and max(int(item.get("width", 0)), int(item.get("height", 0))) < 3840:
            violations.append({"rule": "still_long_edge", "asset_id": item.get("asset_id")})
        qc = item.get("qc") or {}
        if (qc.get("has_readable_text") or qc.get("has_identifiable_face")) and role != "reject":
            violations.append({"rule": "qc_reject_required", "asset_id": item.get("asset_id"), "role": role})
        if pp and public_exists(pp):
            try:
                with Image.open(PUBLIC / pp) as im:
                    if role != "thumb" and max(im.size) < 3840:
                        violations.append({"rule": "actual_image_long_edge", "asset_id": item.get("asset_id"), "size": im.size})
            except Exception as e:
                violations.append({"rule": "image_open", "asset_id": item.get("asset_id"), "error": str(e)})

    for item in data.get("motion") or []:
        pp = item.get("public_path") or ""
        if not (pp.endswith(".mp4") and "_rife" in pp):
            violations.append({"rule": "motion_public_path", "asset_id": item.get("asset_id"), "public_path": pp})
        path = PUBLIC / pp
        if not path.exists():
            violations.append({"rule": "motion_public_exists", "asset_id": item.get("asset_id"), "public_path": pp})
            continue
        try:
            actual = probe_video(path)
            for key in ("width", "height", "frames"):
                if int(item.get(key, 0)) != actual[key]:
                    violations.append({"rule": f"motion_actual_{key}", "asset_id": item.get("asset_id"), "declared": item.get(key), "actual": actual[key]})
            if abs(float(item.get("fps", 0)) - actual["fps"]) > 0.01:
                violations.append({"rule": "motion_actual_fps", "asset_id": item.get("asset_id"), "declared": item.get("fps"), "actual": actual["fps"]})
            if abs(float(item.get("duration_sec", 0)) - actual["duration"]) > 0.04:
                violations.append({"rule": "motion_actual_duration", "asset_id": item.get("asset_id"), "declared": item.get("duration_sec"), "actual": actual["duration"]})
        except Exception as e:
            violations.append({"rule": "motion_probe", "asset_id": item.get("asset_id"), "error": str(e)})
    for item in data.get("factory") or []:
        pp = (item.get("public_path") or "").replace("\\", "/")
        if "/factory/" not in pp:
            violations.append({"rule": "factory_public_path", "asset_id": item.get("asset_id"), "public_path": pp})
        if not item.get("eyeballed_content"):
            violations.append({"rule": "factory_eyeballed_content", "asset_id": item.get("asset_id")})
        if not ((item.get("qc") or {}).get("label_matches_content") is True):
            violations.append({"rule": "factory_label_matches_content", "asset_id": item.get("asset_id")})
    for item in data.get("overlay") or []:
        pp = (item.get("public_path") or "").replace("\\", "/")
        if "/overlay/" not in pp or "/factory/" in pp:
            violations.append({"rule": "overlay_public_path", "asset_id": item.get("asset_id"), "public_path": pp})

    for p, value in iter_strings(data):
        if BANNED_ZONE.search(value):
            violations.append({"rule": "banned_zone", "field": p, "text": value})
    return (0 if not violations else 1), {"ok": not violations, "counts": role_counts, "violations": violations}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    code, result = check(args)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["ok"] else "FAIL") + f" lech_asset_manifest: {len(result['violations'])} violation(s)")
        for v in result["violations"][:20]:
            print(f"  ! {v}")
    return code


if __name__ == "__main__":
    sys.exit(main())
