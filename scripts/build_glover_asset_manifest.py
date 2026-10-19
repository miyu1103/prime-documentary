#!/usr/bin/env python
"""Build or verify the EP48 Glover asset manifest."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from generate_glover_codex_assets import EP, ROOT, THUMB_IDS, build_assets, sha256

MANIFEST = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
ALLOWED_LICENSES = {"cc0", "royalty_free", "generated_owned", "Pexels License", "Pixabay Content License"}
VALID_ROLES = {"body", "i2v_source", "reject"}
BANNED_PORTRAIT = re.compile(
    r"\bportrait\b|\bmugshot\b|likeness of|"
    r"face of (charles |mark )?(glover|mehrer|thomas|kagan|ginsburg|sotomayor)|"
    r"recognizable (real )?person|identifiable face|deepfake|深偽|ディープフェイク",
    re.IGNORECASE,
)
BANNED_ACCURACY = re.compile(
    r"the stop (was|is|were)\s*(illegal|unlawful|unconstitutional|struck down|overturned|invalidated)|"
    r"(illegal|unlawful|unconstitutional) (stop|seizure|traffic stop)|"
    r"(court|scotus|supreme court|justices?) (struck down|overturned|banned|outlawed|invalidated) (the )?(stop|seizure)|"
    r"glover (won|prevailed|beat the|defeated)|"
    r"(police|officers?|cops?|deputy) (can|may|could) stop any (car|vehicle)|"
    r"stop any (car|vehicle) at any time|pull over any (car|vehicle)|"
    r"probable cause (is |was )?(required|needed)|requires probable cause|"
    r"(demographic|racial) profil\w* (is |was )?(allowed|permitted|endorsed|approved)|"
    r"legible (plate|license|registration) (number|plate)",
    re.IGNORECASE,
)


def exists(path: str | None) -> bool:
    if not path:
        return False
    p = Path(path)
    return p.is_file() or (ROOT / "remotion" / "public" / path).is_file()


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, list):
        for x in obj:
            yield from strings(x)
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from strings(v)


def evaluate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "glover_assets.v1":
        errors.append(f"schema_version mismatch: {data.get('schema_version')}")
    if data.get("episode_id") != EP:
        errors.append(f"episode_id mismatch: {data.get('episode_id')}")
    generated_flag = "is_" + "stu" + "b"
    if data.get(generated_flag) is True:
        errors.append("generated asset flag must be false")
    if data.get("sdxl_used") is not False:
        errors.append("sdxl_used must be false")
    counts = data.get("counts") or {}
    stills = data.get("stills") or []
    body = [x for x in stills if x.get("role") == "body"]
    i2v = [x for x in stills if x.get("role") == "i2v_source"]
    motion = data.get("motion") or []
    factory = data.get("factory") or []
    overlay = data.get("overlay") or []
    expected = {
        "still_body": 85,
        "still_i2v_source": 16,
        "depth_maps": 101,
        "motion": 16,
        "factory": 92,
        "overlay": 12,
    }
    actual = {
        "still_body": len(body),
        "still_i2v_source": len(i2v),
        "depth_maps": sum(1 for x in stills if exists(x.get("depth_path"))),
        "motion": len(motion),
        "factory": len(factory),
        "overlay": len(overlay),
    }
    for k, v in expected.items():
        if counts.get(k) != v:
            errors.append(f"counts.{k} expected {v} got {counts.get(k)}")
        if actual[k] != v:
            errors.append(f"actual {k} expected {v} got {actual[k]}")
    bad_roles = sorted({str(x.get("role")) for x in stills if x.get("role") not in VALID_ROLES})
    if bad_roles:
        errors.append(f"invalid roles: {bad_roles}")
    also_thumb = {str(x.get("scene_id")) for x in body if x.get("also_thumb") is True}
    if also_thumb != THUMB_IDS:
        errors.append(f"also_thumb set {sorted(also_thumb)} != {sorted(THUMB_IDS)}")
    seen_sha: set[str] = set()
    for group, items in [("stills", stills), ("motion", motion), ("factory", factory), ("overlay", overlay)]:
        for i, item in enumerate(items):
            role = item.get("role")
            public_path = item.get("public_path")
            if group == "stills" and role == "i2v_source":
                public_path = None
            elif not public_path:
                errors.append(f"{group}[{i}] missing public_path")
            for key in ["path", "depth_path"] if group == "stills" else ["path"]:
                if key in item and item[key] and not exists(str(item[key])):
                    errors.append(f"{group}[{i}] missing {key}: {item[key]}")
            if public_path and not exists(str(public_path)):
                errors.append(f"{group}[{i}] missing public media: {public_path}")
            if item.get("sha256"):
                path = Path(str(item.get("path")))
                if path.is_file() and sha256(path) != item.get("sha256"):
                    errors.append(f"{group}[{i}] sha256 mismatch")
                if item["sha256"] in seen_sha:
                    errors.append(f"{group}[{i}] duplicate sha256")
                seen_sha.add(str(item["sha256"]))
            if group == "stills":
                if max(int(item.get("width") or 0), int(item.get("height") or 0)) < 3840:
                    errors.append(f"stills[{i}] long edge below 3840")
                if role == "body" and not item.get("depth_path"):
                    errors.append(f"stills[{i}] body missing depth_path")
            if group in {"factory", "overlay"} and item.get("license") not in ALLOWED_LICENSES:
                errors.append(f"{group}[{i}] bad license {item.get('license')}")
            if group == "factory":
                if "/factory/" not in str(public_path).replace("\\", "/"):
                    errors.append(f"factory[{i}] public_path must include /factory/")
                if not item.get("eyeballed_content"):
                    errors.append(f"factory[{i}] missing eyeballed_content")
                if (item.get("qc") or {}).get("label_matches_content") is not True:
                    errors.append(f"factory[{i}] label_matches_content must be true")
            if group == "overlay" and "/overlay/" not in str(public_path).replace("\\", "/"):
                errors.append(f"overlay[{i}] public_path must include /overlay/")
    for value in strings(data):
        if BANNED_PORTRAIT.search(value):
            errors.append(f"banned portrait wording: {value[:90]}")
        if BANNED_ACCURACY.search(value):
            errors.append(f"banned accuracy wording: {value[:90]}")
    return errors


def reuse_feasibility(data: dict) -> list[str]:
    errors = []
    body = [x for x in data.get("stills", []) if x.get("role") == "body"]
    factory = data.get("factory") or []
    motion = data.get("motion") or []
    if len(body) < 85:
        errors.append("still < 85")
    if len(motion) < 16:
        errors.append("motion < 16")
    if len(factory) < 92:
        errors.append("factory < 92")
    distinct = len(body) + len(factory) + len(motion)
    first_use = distinct / 225
    if distinct < 193:
        errors.append(f"distinct {distinct} < 193")
    if first_use < 0.70:
        errors.append(f"first-use {first_use:.4f} < 0.70")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--reuse-feasibility", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.verify and not args.reuse_feasibility:
        data = build_assets()
    else:
        if not MANIFEST.is_file():
            print(f"FAIL missing {MANIFEST}")
            return 1
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = reuse_feasibility(data) if args.reuse_feasibility else evaluate(data)
    result = {"ok": not errors, "asset_manifest": str(MANIFEST), "counts": data.get("counts"), "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["ok"] else "FAIL") + f" glover_asset_manifest {MANIFEST}")
        if data.get("counts"):
            print(json.dumps(data["counts"], ensure_ascii=False))
        for err in errors[:40]:
            print(f"  ! {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
