#!/usr/bin/env python3
"""Build EP39 lightweight film manifest (for build_frazier_film.py) from the
reviewed asset_map: pick best still variants per scene (drop the 3rd near-dup),
map to the graded frazier/img/FRZ_* stills (+depth), and reuse the proven stub
factory/motion/overlay entries. Output feeds build_frazier_film.py --manifest."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "remotion" / "public"
ASSET_MAP = ROOT / "episodes/_planning/EP39_frazier_asset_map.v001.json"
STUB_MANIFEST = ROOT / "episodes/PD-2026-039-frazier/05_visuals/asset_manifest.stub.v001.json"
OUT = ROOT / "episodes/PD-2026-039-frazier/05_visuals/asset_manifest.real.v001.json"

ACT_RANK = {"HOOK": 0, "ACT I": 1, "ACT II": 2, "ACT III": 3, "ACT IV": 4, "ENDING": 5}


def parse_file(fname: str) -> tuple[str, int]:
    m = re.match(r"(S\d+)(?:_(\d+))?\.png$", fname)
    if not m:
        raise ValueError(f"bad still filename: {fname}")
    scene = m.group(1)
    variant = int(m.group(2)) if m.group(2) else 1
    return scene, variant


def public_of(scene: str, variant: int) -> tuple[str, str | None]:
    """Return (public_path, depth_public_path|None), verifying files exist.
    Prefer graded frazier/img/FRZ_S##_V##.png (+depth); fall back to the
    top-level mirror frazier/S##[_vv].png for gap-fill scenes not in img/."""
    frz = f"frazier/img/FRZ_{scene}_V{variant:02d}.png"
    if (PUBLIC / frz).is_file():
        depth = f"frazier/img/FRZ_{scene}_V{variant:02d}_depth.png"
        return frz, (depth if (PUBLIC / depth).is_file() else None)
    # top-level mirror (S01.png / S01_02.png)
    top = f"frazier/{scene}.png" if variant == 1 else f"frazier/{scene}_{variant:02d}.png"
    if (PUBLIC / top).is_file():
        return top, None
    raise FileNotFoundError(f"no still on disk for {scene} V{variant} (tried {frz}, {top})")


def main() -> int:
    amap = json.loads(ASSET_MAP.read_text(encoding="utf-8"))
    usable = amap["usable"]

    # group usable variants per scene
    by_scene: dict[str, list[dict]] = defaultdict(list)
    for e in usable:
        scene, variant = parse_file(e["file"])
        by_scene[scene].append({"scene": scene, "variant": variant, "assign": e["assign"], "file": e["file"]})

    # pick best <=2 variants per scene: drop the 3rd near-duplicate (variant 3),
    # keeping V01/V02. (S61_03 excluded per coordinator; it is a V03 -> already dropped.)
    picks: list[dict] = []
    for scene, variants in by_scene.items():
        keep = [v for v in variants if v["variant"] != 3]
        keep.sort(key=lambda v: v["variant"])
        picks.extend(keep)

    # deterministic act-order: (act_rank, scene_num, variant)
    def sort_key(p: dict):
        rank = ACT_RANK.get(p["assign"].strip(), 9)
        return (rank, int(p["scene"][1:]), p["variant"])

    picks.sort(key=sort_key)

    stills = []
    for i, p in enumerate(picks, 1):
        pub, depth = public_of(p["scene"], p["variant"])
        rank = ACT_RANK.get(p["assign"].strip(), 9)
        stills.append({
            "asset_id": f"ST-039-{i:03d}",
            "kind": "still",
            "max_uses": 2,
            "public_path": pub,
            "depth_map": depth,
            "scene_code": p["scene"],
            "act": rank,
            "variant": p["variant"],
            "assign": p["assign"],
            "qc": {"pass": True, "notes": "reviewed asset_map pick (best variant, V03 dropped)"},
        })

    # reuse proven stub factory/motion/overlay entries verbatim (real files on disk)
    stub = json.loads(STUB_MANIFEST.read_text(encoding="utf-8"))
    factory = [a for a in stub["assets"] if a["kind"] == "factory"]
    motion = [a for a in stub["assets"] if a["kind"] == "motion"]
    overlays = stub.get("overlays", [])

    # verify every referenced file exists
    missing = []
    for a in stills + factory + motion:
        if not (PUBLIC / a["public_path"]).is_file():
            missing.append(a["public_path"])
    for o in overlays:
        if not (PUBLIC / o["public_path"]).is_file():
            missing.append(o["public_path"])
    if missing:
        raise SystemExit(f"missing files on disk: {missing[:10]} ({len(missing)} total)")

    assets = stills + factory + motion
    payload = {
        "episode_id": "PD-2026-039-frazier",
        "manifest_version": "v001",
        "status": "real_stills_stub_footage",
        "counts": {
            "still": len(stills), "factory": len(factory), "motion": len(motion),
            "total": len(assets), "overlays": len(overlays),
            "distinct_scene_codes": len({a["scene_code"] for a in assets}),
        },
        "caps": {"still": 2, "factory": 1, "motion": 2},
        "assets": assets,
        "overlays": overlays,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(json.dumps(payload["counts"], ensure_ascii=False))
    # still act distribution
    from collections import Counter
    print("still acts:", dict(Counter(s["assign"] for s in stills)))
    print("sample still:", json.dumps(stills[0], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
