#!/usr/bin/env python
"""Re-categorize the Asset Factory shelf into theme sub-folders for easy retrieval.

Adds `theme` + `subcategory` to every asset_manifest entry (derived from subtype by
keyword rules) and moves each file into `<media>/assets/factory/<category>/<theme>/`.
Manifest `path` is updated in lockstep so importer/select/validator keep working.

Safe by design:
  - SAME-VOLUME move (fast metadata rename on H:, not a 221GB copy).
  - Idempotent: skips files already under their theme folder.
  - Backs up the manifest to assets/asset_manifest.v001.prereorg.bak.json before writing.
  - Default DRY-RUN (prints plan only). Pass --apply to move + rewrite manifest.

Usage:
  .venv/Scripts/python.exe scripts/recategorize_factory.py            # dry-run
  .venv/Scripts/python.exe scripts/recategorize_factory.py --apply    # do it
"""
from __future__ import annotations
import sys, os, json, shutil, argparse, collections

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "assets", "asset_manifest.v001.json")
BACKUP = os.path.join(ROOT, "assets", "asset_manifest.v001.prereorg.bak.json")
MEDIA_ROOT = os.environ.get("PD_MEDIA_ROOT", r"H:\pd-media")

# Ordered (substring, theme) rules applied to subtype. First match wins -> put
# specific before general. Covers the 190 background subtypes + future ones.
RULES: list[tuple[str, str]] = [
    # legal / judiciary
    ("court", "legal_court"), ("gavel", "legal_court"), ("jury", "legal_court"),
    ("justice", "legal_court"), ("judge", "legal_court"), ("law_", "legal_court"),
    ("law_books", "legal_court"), ("law_library", "legal_court"), ("constitution", "legal_court"),
    ("witness", "legal_court"), ("scales", "legal_court"), ("balance_scale", "legal_court"),
    ("capitol", "legal_court"), ("supreme_court", "legal_court"), ("federal_building", "legal_court"),
    ("white_house", "legal_court"), ("bank_building_columns", "legal_court"),
    # civic / voting / protest
    ("ballot", "civic_voting"), ("voting", "civic_voting"), ("voting_booth", "civic_voting"),
    ("protest", "civic_voting"), ("flag", "civic_voting"),
    # crime / police / prison
    ("police", "crime_police"), ("prison", "crime_police"), ("jail", "crime_police"),
    ("evidence", "crime_police"), ("crime_scene", "crime_police"), ("interrogation", "crime_police"),
    ("handcuff", "crime_police"), ("badge", "crime_police"), ("barbed_wire", "crime_police"),
    ("one_way_mirror", "crime_police"), ("case_files", "crime_police"), ("ambulance", "crime_police"),
    # forensics / dna
    ("dna", "forensics_dna"), ("fingerprint", "forensics_dna"), ("blood", "forensics_dna"),
    # medical / lab
    ("medical", "medical_lab"), ("hospital", "medical_lab"), ("lab", "medical_lab"),
    ("test_tube", "medical_lab"), ("centrifuge", "medical_lab"), ("operating", "medical_lab"),
    ("pills", "medical_lab"), ("ekg", "medical_lab"), ("microscope", "medical_lab"),
    ("glassware", "medical_lab"),
    # finance / money
    ("money", "finance_money"), ("cash", "finance_money"), ("dollar", "finance_money"),
    ("gold_bar", "finance_money"), ("vault", "finance_money"), ("safe", "finance_money"),
    ("stock", "finance_money"), ("trading", "finance_money"), ("wall_street", "finance_money"),
    ("bull", "finance_money"), ("bitcoin", "finance_money"), ("credit_card", "finance_money"),
    ("briefcase", "finance_money"),
    # property / home
    ("house", "property_home"), ("picket_fence", "property_home"), ("for_sale", "property_home"),
    ("suburb", "property_home"), ("moving_truck", "property_home"), ("moving_boxes", "property_home"),
    ("demolition", "property_home"), ("main_street", "property_home"), ("rural_road", "property_home"),
    # school / youth
    ("school", "school_youth"), ("graduation", "school_youth"), ("playground", "school_youth"),
    # surveillance / tech
    ("surveillance", "surveillance_tech"), ("cctv", "surveillance_tech"), ("camera", "surveillance_tech"),
    ("cell_tower", "surveillance_tech"), ("smartphone", "surveillance_tech"), ("phone", "surveillance_tech"),
    ("binary", "surveillance_tech"), ("circuit", "surveillance_tech"), ("server", "surveillance_tech"),
    ("data_center", "surveillance_tech"), ("data_flow", "surveillance_tech"), ("fiber_optic", "surveillance_tech"),
    ("satellite", "surveillance_tech"), ("world_map", "surveillance_tech"), ("globe", "surveillance_tech"),
    ("hacker", "surveillance_tech"), ("radio_tower", "surveillance_tech"), ("security_monitor", "surveillance_tech"),
    ("technology_abstract", "surveillance_tech"),
    # documents / paper
    ("document", "documents_paper"), ("contract", "documents_paper"), ("paperwork", "documents_paper"),
    ("newspaper", "documents_paper"), ("typewriter", "documents_paper"), ("quill", "documents_paper"),
    ("wax_seal", "documents_paper"), ("magnifying_glass", "documents_paper"), ("shredded", "documents_paper"),
    ("burning_paper", "documents_paper"),
    # urban / night
    ("city", "urban_night"), ("skyline", "urban_night"), ("drone", "urban_night"),
    ("traffic", "urban_night"), ("subway", "urban_night"), ("train", "urban_night"),
    ("airport", "urban_night"), ("parking_garage", "urban_night"), ("bridge", "urban_night"),
    ("highway", "urban_night"), ("rooftop", "urban_night"), ("office", "urban_night"),
    ("boardroom", "urban_night"), ("warehouse", "urban_night"), ("elevator", "urban_night"),
    ("stadium", "urban_night"),
    # nature / landscape
    ("mountain", "nature_landscape"), ("forest", "nature_landscape"), ("ocean", "nature_landscape"),
    ("tree", "nature_landscape"), ("desert", "nature_landscape"), ("snow", "nature_landscape"),
    ("storm", "nature_landscape"), ("harbor", "nature_landscape"), ("lighthouse", "nature_landscape"),
    ("cemetery", "nature_landscape"), ("church", "nature_landscape"),
    # atmosphere / symbolic
    ("shadow", "atmosphere_symbolic"), ("silhouette", "atmosphere_symbolic"), ("mirror", "atmosphere_symbolic"),
    ("broken_window", "atmosphere_symbolic"), ("chair", "atmosphere_symbolic"), ("clock", "atmosphere_symbolic"),
    ("candle", "atmosphere_symbolic"), ("padlock", "atmosphere_symbolic"), ("chains", "atmosphere_symbolic"),
    ("keys", "atmosphere_symbolic"), ("hands", "atmosphere_symbolic"), ("chess", "atmosphere_symbolic"),
    ("fireplace", "atmosphere_symbolic"), ("spotlight", "atmosphere_symbolic"), ("rotary_phone", "atmosphere_symbolic"),
    ("rain_on", "atmosphere_symbolic"), ("rain_street", "atmosphere_symbolic"),
    # specific mop-ups (were falling to misc_background)
    ("government_building", "legal_court"),
    ("old_library_archive", "documents_paper"), ("library", "documents_paper"),
    ("abandoned_factory", "urban_night"), ("atm", "finance_money"),
    ("tv_static", "surveillance_tech"), ("empty_road", "nature_landscape"),
    ("umbrella", "atmosphere_symbolic"), ("desk_lamp", "atmosphere_symbolic"),
    ("concrete_wall", "atmosphere_symbolic"), ("moody", "atmosphere_symbolic"),
    ("dark_cinematic", "abstract"), ("abstract", "abstract"),
    # fx category buckets (light/vfx/particle/texture/loops)
    ("loop", "abstract_loop"),
]

# coarse fallback per top-level category when no subtype rule matched
CAT_FALLBACK = {
    "backgrounds": "misc_background",
    "light_assets": "light",
    "vfx_overlays": "vfx",
    "particle_assets": "particle",
    "texture_assets": "texture",
    "loops": "abstract_loop",
}


def derive_theme(category: str, subtype: str) -> str:
    s = (subtype or "").lower()
    # fx categories keep their own bucket as the theme (they are decoration, not b-roll)
    if category in ("light_assets", "vfx_overlays", "particle_assets", "texture_assets", "loops"):
        return CAT_FALLBACK[category]
    for kw, theme in RULES:
        if kw in s:
            return theme
    return CAT_FALLBACK.get(category, "misc")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="move files + rewrite manifest (default: dry-run)")
    args = ap.parse_args()

    m = json.load(open(MANIFEST, encoding="utf-8"))
    E = m["assets"]
    plan = collections.Counter()
    moves: list[tuple[str, str, dict, str, str]] = []  # (src_abs, dst_abs, entry, new_path, theme)
    already = 0
    for e in E:
        cat = e.get("type")
        theme = derive_theme(cat, e.get("subtype"))
        path = e.get("path") or ""                       # e.g. factory/backgrounds/AF-BG-1__x.jpg
        parts = path.split("/")
        if len(parts) < 3:
            continue
        # detect if already under a theme folder: factory/<cat>/<theme>/<file>
        if len(parts) >= 4 and parts[2] == theme:
            already += 1
            plan[f"{cat}/{theme}"] += 1
            continue
        fname = parts[-1]
        new_path = f"factory/{cat}/{theme}/{fname}"
        src_abs = os.path.join(MEDIA_ROOT, "assets", *path.split("/"))
        dst_abs = os.path.join(MEDIA_ROOT, "assets", *new_path.split("/"))
        moves.append((src_abs, dst_abs, e, new_path, theme))
        plan[f"{cat}/{theme}"] += 1

    print(f"manifest entries: {len(E)} | to move: {len(moves)} | already placed: {already}")
    print("\n=== plan: files per category/theme ===")
    for k, v in sorted(plan.items()):
        print(f"  {v:6}  {k}")
    # report any 'misc' (unmapped backgrounds) so coverage can be improved
    misc = [e.get("subtype") for e in E if derive_theme(e.get("type"), e.get("subtype")) in ("misc", "misc_background") and e.get("type") == "backgrounds"]
    if misc:
        c = collections.Counter(misc)
        print(f"\n!! UNMAPPED backgrounds subtypes ({len(c)} distinct) -> fell back to misc_background:")
        for s, n in c.most_common():
            print(f"   {n:5}  {s}")

    if not args.apply:
        print("\n(DRY-RUN) no files moved, manifest unchanged. Pass --apply to execute.")
        return

    # backup manifest first
    if not os.path.exists(BACKUP):
        shutil.copy2(MANIFEST, BACKUP)
        print(f"\nbacked up manifest -> {os.path.relpath(BACKUP, ROOT)}")
    moved = miss = 0
    for src_abs, dst_abs, e, new_path, theme in moves:
        os.makedirs(os.path.dirname(dst_abs), exist_ok=True)
        if os.path.exists(src_abs):
            if not os.path.exists(dst_abs):
                shutil.move(src_abs, dst_abs)
            moved += 1
        elif os.path.exists(dst_abs):
            moved += 1                                    # already moved (resume)
        else:
            miss += 1
            continue
        e["path"] = new_path
        e["theme"] = theme
        e["subcategory"] = e.get("subtype")
    # also stamp theme on entries that were already placed
    for e in E:
        if "theme" not in e:
            e["theme"] = derive_theme(e.get("type"), e.get("subtype"))
            e["subcategory"] = e.get("subtype")
    json.dump(m, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nAPPLIED: moved {moved}, missing-src {miss}. manifest rewritten with theme/subcategory.")


if __name__ == "__main__":
    main()
