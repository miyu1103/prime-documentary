#!/usr/bin/env python3
"""Stage curated Asset Factory assets for Titan Premium.

Copies rights-allowed factory assets into remotion/public/titan/factory and writes
an episode ledger plus a typed Remotion data module. The source of truth remains
assets/asset_manifest.v001.json; this script only stages review/edit assets.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
MANIFEST = ROOT / "assets" / "asset_manifest.v001.json"
DEST = ROOT / "remotion" / "public" / "titan" / "factory"
DATA = ROOT / "remotion" / "src" / "data" / "titan_factory_assets.ts"
LEDGER = ROOT / "episodes" / "PD-2026-016-titan" / "05_stock" / "factory_ledger.v001.json"

ALLOWED = {"Pexels License", "Pixabay Content License", "cc0", "royalty_free", "generated_owned"}
REQUESTS = [
    ("nature_landscape", "ocean_horizon_moody", "video", 4),
    ("nature_landscape", "storm_clouds_dramatic", "video", 2),
    ("nature_landscape", "harbor", "video", 2),
    ("vfx", "ink_in_water", "video", 4),
    ("vfx", "smoke_on_black_background", "video", 2),
    ("surveillance_tech", "server_room_blue", "video", 3),
    ("surveillance_tech", "world_map_dark_glowing", "video", 2),
    ("surveillance_tech", "satellite_earth_at_night", "video", 2),
    ("atmosphere_symbolic", "clock_ticking_macro", "video", 2),
    ("atmosphere_symbolic", "single_chair_empty_room", "video", 2),
    ("atmosphere_symbolic", "candle_in_dark", "video", 2),
    ("documents_paper", "documents_on_desk", "image", 3),
    ("documents_paper", "magnifying_glass_on_document", "image", 2),
    ("texture", "old_paper_texture", "image", 2),
    ("finance_money", "stack_of_hundred_dollar_bills", "image", 3),
    ("finance_money", "open_briefcase_of_cash", "image", 2),
    ("light", "caustics_water_light", "video", 2),
    ("particle", "static_noise_particles", "video", 2),
]


def first_matches(assets: list[dict[str, Any]], subtype: str, kind: str, used: set[str], limit: int) -> list[dict[str, Any]]:
    return [
        asset
        for asset in assets
        if asset.get("subtype") == subtype
        and asset.get("kind") == kind
        and asset.get("license") in ALLOWED
        and asset.get("id") not in used
    ][:limit]


def main() -> int:
    assets = json.loads(MANIFEST.read_text("utf-8"))["assets"]
    staged: list[dict[str, Any]] = []
    used: set[str] = set()
    missing_requests: list[str] = []
    DEST.mkdir(parents=True, exist_ok=True)

    for group, subtype, kind, limit in REQUESTS:
        matches = first_matches(assets, subtype, kind, used, limit)
        if not matches:
            missing_requests.append(f"{subtype}:{kind}")
        for asset in matches:
            used.add(asset["id"])
            src = MEDIA / "assets" / asset["path"]
            dst = DEST / Path(asset["path"]).name
            if not src.exists():
                missing_requests.append(f"missing_file:{asset['id']}")
                continue
            shutil.copy2(src, dst)
            staged.append(
                {
                    "id": asset["id"],
                    "group": group,
                    "subtype": subtype,
                    "kind": kind,
                    "license": asset.get("license"),
                    "source": asset.get("source"),
                    "sourceUrl": asset.get("sourceUrl"),
                    "sha256": asset.get("sha256"),
                    "bytes": asset.get("bytes"),
                    "src": f"titan/factory/{dst.name}",
                }
            )

    groups: dict[str, list[str]] = {}
    for item in staged:
        groups.setdefault(item["subtype"], []).append(item["src"])
        groups.setdefault(item["group"], []).append(item["src"])

    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "episode_id": "PD-2026-016-titan",
                "revision": "v001",
                "kind": "factory_ledger",
                "assets": staged,
                "missing_requests": missing_requests,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        "utf-8",
    )
    DATA.write_text(
        "export const TITAN_FACTORY = "
        + json.dumps(groups, indent=2, ensure_ascii=False)
        + " as const;\n"
        + "export const TITAN_FACTORY_LEDGER = "
        + json.dumps(staged, indent=2, ensure_ascii=False)
        + " as const;\n",
        "utf-8",
    )
    print(f"staged={len(staged)} dest={DEST}")
    print(f"data={DATA.relative_to(ROOT)} ledger={LEDGER.relative_to(ROOT)}")
    if missing_requests:
        print("missing_requests=" + ",".join(missing_requests))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
