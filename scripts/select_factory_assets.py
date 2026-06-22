# -*- coding: utf-8 -*-
"""
Select candidate Asset Factory assets from assets/asset_manifest.v001.json.
Operationalizes the asset-first workflow: given a sceneType / mood / category / keyword,
return matching AF-* ids + paths so a Scene Plan / Shot Recipe can pick from the shelf
BEFORE generating anything new.

Usage:
  python scripts/select_factory_assets.py --scene-type explanation --limit 20
  python scripts/select_factory_assets.py --category light_assets
  python scripts/select_factory_assets.py --query "smoke" --kind video
  python scripts/select_factory_assets.py --theme legal_court --kind video   # theme b-roll
  python scripts/select_factory_assets.py --subtype courtroom_interior
  python scripts/select_factory_assets.py --themes                           # list themes + counts
"""
from __future__ import annotations
import sys, os, json, argparse

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(REPO, "assets", "asset_manifest.v001.json")

# coarse category -> sceneType affinity (used until per-asset compatibleSceneTypes is enriched)
CAT_SCENE = {
    "backgrounds": ["explanation", "place_intro", "company_profile", "character_profile",
                    "problem_statement", "summary", "abstract_emotion", "chapter_title",
                    "opening_hook", "ending", "transition_bridge", "evidence_board", "quote"],
    "light_assets": ["opening_hook", "turning_point", "ending", "emotional_pause", "chapter_title",
                     "abstract_emotion", "quote"],
    "particle_assets": ["opening_hook", "emotional_pause", "abstract_emotion", "ending",
                        "silent_hold", "chapter_title"],
    "vfx_overlays": ["turning_point", "abstract_emotion", "transition_bridge", "opening_hook",
                     "emotional_pause"],
    "texture_assets": ["chapter_title", "quote", "evidence_board", "explanation", "summary"],
    "loops": ["explanation", "abstract_emotion", "transition_bridge", "data_reveal", "summary"],
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene-type", default="")
    ap.add_argument("--category", default="")
    ap.add_argument("--theme", default="", help="theme folder e.g. legal_court, crime_police, finance_money")
    ap.add_argument("--subtype", default="", help="exact subtype e.g. courtroom_interior")
    ap.add_argument("--query", default="")
    ap.add_argument("--kind", default="", help="image|video")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--themes", action="store_true", help="list all themes with counts and exit")
    a = ap.parse_args()

    if not os.path.exists(MAN):
        print("manifest not found:", MAN); return 2
    assets = json.load(open(MAN, encoding="utf-8")).get("assets", [])

    if a.themes:
        import collections
        by = collections.Counter(f"{x.get('type')}/{x.get('theme','(none)')}" for x in assets)
        print(f"{len(assets)} assets across {len(by)} category/theme groups:")
        for k, n in sorted(by.items()):
            print(f"  {n:6}  {k}")
        return 0

    def ok(x):
        if a.category and x.get("type") != a.category:
            return False
        if a.theme and x.get("theme") != a.theme:
            return False
        if a.subtype and x.get("subtype") != a.subtype:
            return False
        if a.kind and x.get("kind") != a.kind:
            return False
        if a.query and a.query.lower() not in (x.get("subtype", "") + " " + " ".join(x.get("tags", []))).lower():
            return False
        if a.scene_type:
            st = x.get("compatibleSceneTypes") or CAT_SCENE.get(x.get("type"), [])
            if a.scene_type not in st:
                return False
        return True

    hits = [x for x in assets if ok(x)]
    hits = hits[: a.limit]
    if a.json:
        print(json.dumps([{"id": x["id"], "path": x["path"], "kind": x.get("kind"),
                           "license": x.get("license")} for x in hits], ensure_ascii=False, indent=1))
    else:
        print(f"{len(hits)} match (of {len(assets)} in shelf)")
        for x in hits:
            print(f"  {x['id']:<16} {x.get('kind','?'):<6} {x.get('theme','-'):<18} {x['path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
