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
    ap.add_argument("--query", default="")
    ap.add_argument("--kind", default="", help="image|video")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if not os.path.exists(MAN):
        print("manifest not found:", MAN); return 2
    assets = json.load(open(MAN, encoding="utf-8")).get("assets", [])

    def ok(x):
        if a.category and x.get("type") != a.category:
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
            print(f"  {x['id']:<16} {x.get('kind','?'):<6} {x['type']:<16} {x['path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
