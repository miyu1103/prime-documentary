#!/usr/bin/env python3
"""Stage curated Asset Factory assets for Miranda Premium."""
from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
MANIFEST = ROOT / "assets" / "asset_manifest.v001.json"
DEST = ROOT / "remotion" / "public" / "miranda" / "factory"
DATA = ROOT / "remotion" / "src" / "data" / "miranda_factory_assets.ts"
LEDGER = ROOT / "episodes" / "PD-2026-001-miranda" / "05_stock" / "factory_ledger.v001.json"

ALLOWED = {"Pexels License", "Pixabay Content License", "cc0", "royalty_free", "generated_owned"}
REQUESTS = [
    ("crime_police", "police_interrogation_room_empty", "video", 2),
    ("crime_police", "one_way_mirror_room", "video", 2),
    ("crime_police", "jail_cell_bars", "video", 2),
    ("crime_police", "prison_corridor", "video", 2),
    ("crime_police", "police_badge_close_up", "video", 1),
    ("crime_police", "police_car_lights_night", "video", 2),
    ("crime_police", "case_files_stack_desk", "video", 1),
    ("legal_court", "supreme_court_building", "video", 2),
    ("legal_court", "courtroom_interior", "video", 2),
    ("legal_court", "judge_gavel_wooden", "video", 1),
    ("legal_court", "us_constitution_document", "video", 2),
    ("legal_court", "law_library_books", "video", 2),
    ("atmosphere_symbolic", "clock_ticking_macro", "video", 2),
    ("atmosphere_symbolic", "single_chair_empty_room", "video", 2),
    ("atmosphere_symbolic", "long_shadow_of_a_person", "video", 2),
    ("light", "god_rays", "video", 2),
    ("light", "light_leak_overlay", "video", 2),
    ("light", "police_strobe_red_and_blue", "video", 2),
    ("vfx", "smoke_on_black", "video", 2),
    ("vfx", "fog_rolling", "video", 1),
    ("particle", "dust_motes_sunlight", "video", 2),
    ("particle", "floating_dust_in_light_beam", "video", 2),
    ("texture", "parchment_texture", "image", 2),
    ("texture", "old_paper_texture", "image", 2),
    ("texture", "film_grain_texture", "image", 1),
    ("loop", "looping_light_rays", "video", 1),
    ("loop", "atmospheric_loop", "video", 1),
]


def main() -> int:
    assets = json.loads(MANIFEST.read_text("utf-8"))["assets"]
    staged = []
    used = set()
    DEST.mkdir(parents=True, exist_ok=True)
    for group, subtype, kind, limit in REQUESTS:
        matches = [
            a for a in assets
            if a.get("subtype") == subtype
            and a.get("kind") == kind
            and a.get("license") in ALLOWED
            and a.get("id") not in used
        ][:limit]
        for a in matches:
            used.add(a["id"])
            src = MEDIA / "assets" / a["path"]
            dst = DEST / Path(a["path"]).name
            if src.exists():
                shutil.copy2(src, dst)
                item = {
                    "id": a["id"],
                    "group": group,
                    "subtype": subtype,
                    "kind": kind,
                    "license": a.get("license"),
                    "source": a.get("source"),
                    "sourceUrl": a.get("sourceUrl"),
                    "sha256": a.get("sha256"),
                    "src": f"miranda/factory/{dst.name}",
                }
                staged.append(item)
            else:
                print(f"WARN missing {src}")
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps({"episode_id": "PD-2026-001-miranda", "assets": staged}, indent=2, ensure_ascii=False) + "\n", "utf-8")
    groups: dict[str, list[str]] = {}
    for item in staged:
        groups.setdefault(item["subtype"], []).append(item["src"])
        groups.setdefault(item["group"], []).append(item["src"])
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(
        "export const MIRANDA_FACTORY = " + json.dumps(groups, indent=2, ensure_ascii=False) + " as const;\n"
        "export const MIRANDA_FACTORY_LEDGER = " + json.dumps(staged, indent=2, ensure_ascii=False) + " as const;\n",
        "utf-8",
    )
    print(f"staged={len(staged)} dest={DEST}")
    print(f"data={DATA.relative_to(ROOT)} ledger={LEDGER.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
