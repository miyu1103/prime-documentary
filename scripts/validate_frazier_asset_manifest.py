#!/usr/bin/env python3
"""Assert EP39 asset-manifest integrity; strict mode requires final Wan delivery."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "episodes/PD-2026-039-frazier/05_visuals/asset_manifest.v001.json"
PUBLIC = ROOT / "remotion/public"

TOP_KEYS = {"episode_id", "manifest_version", "generated_at", "status", "producer", "counts", "caps", "assets", "overlays"}
ASSET_KEYS = {
    "asset_id", "kind", "max_uses", "public_path", "abs_path", "source_path",
    "scene_code", "act", "variant", "depth_map", "width", "height", "long_edge_px",
    "duration_sec", "fps", "frames", "sha256", "bytes", "median_luma", "af_id",
    "theme", "subtype", "saw", "tags", "source", "license", "reviewed", "on_theme",
    "qc", "stub",
}
OVERLAY_KEYS = {"overlay_id", "category", "public_path", "duration_sec", "fps", "blend_hint", "sha256", "af_id"}
ID_RE = re.compile(r"^(ST|FC|MO)-039-(\d{3})$")
SCENE_RE = re.compile(r"^S(?:0[1-9]|[1-4][0-9]|50)$")
CAPS = {"still": 2, "factory": 1, "motion": 2}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def validate(path: Path, allow_partial: bool) -> dict:
    d = json.loads(path.read_text(encoding="utf-8"))
    assert set(d) == TOP_KEYS, (set(d) - TOP_KEYS, TOP_KEYS - set(d))
    assert d["episode_id"] == "PD-2026-039-frazier"
    assert d["manifest_version"] == "v001"
    assert d["status"] in ({"partial", "final"} if allow_partial else {"final"}), d["status"]
    assert d["caps"] == CAPS
    assets = d["assets"]
    overlays = d["overlays"]
    assert all(set(x) == ASSET_KEYS for x in assets)
    assert all(set(x) == OVERLAY_KEYS for x in overlays)

    ids = [x["asset_id"] for x in assets]
    assert len(ids) == len(set(ids))
    by_prefix: dict[str, list[int]] = defaultdict(list)
    for asset_id in ids:
        m = ID_RE.fullmatch(asset_id)
        assert m, asset_id
        by_prefix[m.group(1)].append(int(m.group(2)))
    for values in by_prefix.values():
        assert sorted(values) == list(range(1, len(values) + 1)), values

    counts = Counter(x["kind"] for x in assets)
    assert set(counts) <= set(CAPS)
    assert counts["factory"] >= 90, counts
    assert counts["still"] >= 75, counts
    if not allow_partial:
        assert counts["motion"] >= 18, counts
    scenes = {x["scene_code"] for x in assets}
    assert len(scenes) >= 45, len(scenes)
    assert all(SCENE_RE.fullmatch(x["scene_code"]) for x in assets)
    still_scene_counts = Counter(x["scene_code"] for x in assets if x["kind"] == "still")
    assert not [s for s, n in still_scene_counts.items() if n >= 4], still_scene_counts

    for x in assets:
        kind = x["kind"]
        assert x["max_uses"] == CAPS[kind]
        f = PUBLIC / x["public_path"]
        assert f.is_file(), f
        assert sha256(f) == x["sha256"], f
        assert f.stat().st_size == x["bytes"], f
        assert x["reviewed"] is True and x["on_theme"] is True
        assert x["qc"] == {"pass": True, "notes": x["qc"]["notes"]}
        assert x["stub"] is False
        assert isinstance(x["tags"], list) and x["tags"]
        if kind == "still":
            assert x["public_path"].startswith("frazier/img/")
            assert x["long_edge_px"] >= 3840
            assert x["depth_map"]
            assert (PUBLIC / x["depth_map"]).is_file(), x["depth_map"]
            assert x["source"] == "codex_imagegen"  # explicit owner override: no SDXL
        elif kind == "factory":
            assert x["public_path"].startswith("frazier/factory/")
            assert x["saw"] and x["af_id"] and x["theme"] and x["subtype"]
            assert x["source"] == "factory_shelf"
        else:
            assert x["public_path"].startswith("frazier/motion/")
            assert x["frames"] >= 41 and x["width"] >= 1280 and x["height"] >= 720
            assert x["source"] == "wan22_a14b_i2v"

    overlay_ids = [x["overlay_id"] for x in overlays]
    assert len(overlays) >= 30 and len(overlay_ids) == len(set(overlay_ids))
    assert overlay_ids == [f"OV-039-{i:03d}" for i in range(1, len(overlays) + 1)]
    for x in overlays:
        assert x["category"] in {"light_assets", "particle_assets", "vfx_overlays", "loops"}
        assert x["public_path"].startswith("frazier/overlay/")
        f = PUBLIC / x["public_path"]
        assert f.is_file(), f
        assert sha256(f) == x["sha256"], f

    expected_counts = {
        "still": counts["still"], "factory": counts["factory"], "motion": counts["motion"],
        "total": len(assets), "overlays": len(overlays), "distinct_scene_codes": len(scenes),
    }
    assert d["counts"] == expected_counts, (d["counts"], expected_counts)
    assert counts["factory"] + counts["still"] * 2 + counts["motion"] * 2 >= 226
    assert len(assets) / 226 >= 0.70
    return expected_counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", nargs="?", type=Path, default=DEFAULT)
    ap.add_argument("--allow-partial", action="store_true", help="validate completed real assets without waiving strict final mode")
    args = ap.parse_args()
    counts = validate(args.manifest, args.allow_partial)
    print(f"PASS {args.manifest} counts={json.dumps(counts, sort_keys=True)} mode={'partial' if args.allow_partial else 'final'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
