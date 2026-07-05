# -*- coding: utf-8 -*-
"""Stage themed factory b-roll into remotion/public/<slug>/factory for CaseFilm.

build_case_film_assets.py READS whatever .mp4 clips are already staged there; it does
NOT select them. This picks video clips per theme, sampled EVENLY across each theme's
sorted list (so we don't grab near-duplicate consecutive subtypes), copies them from the
shelf (H:/pd-media/assets/<manifest path>) into remotion/public/<slug>/factory, and
keeps them distinct -> satisfies factory_used + footage_diversity before assembly.

Usage: python scripts/stage_case_factory_assets.py --slug hinton
"""
from __future__ import annotations
import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from factory_themes import theme_of  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "asset_manifest.v001.json"
SHELF = Path("H:/pd-media/assets")   # manifest paths are relative to here

# per-episode theme -> how many distinct clips to stage (total ~ runtime/7s worth, denser than needed)
PLANS = {
    "hinton": {  # death row / ballistics / courtroom / alibi warehouse / night
        "crime_police": 22, "legal_court": 20, "forensics_dna": 12, "medical_lab": 8,
        "documents_paper": 12, "urban_night": 14, "atmosphere_symbolic": 6, "property_home": 2,
    },
    "forfeiture": {  # already staged by parallel thread; kept for reference/re-stage
        "property_home": 20, "crime_police": 18, "legal_court": 20, "finance_money": 14,
        "documents_paper": 14, "urban_night": 10,
    },
    "cotton": {  # eyewitness / lineup / DNA lab / courtroom / prison — DYNAMIC only (no atmosphere/featureless)
        "crime_police": 24, "legal_court": 22, "forensics_dna": 16, "medical_lab": 12,
        "documents_paper": 12, "urban_night": 10,
    },
    "carsearch": {  # traffic stops / highways / suburban driveways / courthouse / warrants+rental / phone
        "crime_police": 44, "urban_night": 38, "property_home": 32, "legal_court": 24,
        "documents_paper": 20, "surveillance_tech": 14, "nature_landscape": 6,
    },
}


# design rule: exclude featureless / near-static b-roll (row 8 "featureless除去" + the
# 紙芝居 promise). Drop clips whose subtype reads as a texture / empty room / still-life /
# sky / fog / gradient — they register as near-still and violate "motion on every cut".
FEATURELESS = ("texture", "wall", "empty", "still_life", "gradient", "pattern", "backdrop",
               "fog", "haze", "sky", "clouds", "bokeh", "abstract", "aerial_static",
               "ink_pot", "cubicle", "wallpaper", "surface", "blank", "dark_cinematic_background",
               "moody_atmosphere", "atmosphere")


# shelf labels are unreliable: some clips are mislabeled stock (an "evidence_bag" that is
# actually a cartoon cowboy, a "judge_gavel" that is a water-mill, a "boardroom" that is a
# family picnic...). Visual QC catches them; block the offending AF-BG ids by exact file id
# so a re-stage never pulls them back. Add ids here as QC finds more.
BLOCK_IDS = {
    # round 1 (cartoon cowboy, christmas house, plants, plastic hand, caterpillar,
    # water-mill, espresso, kettle, clover, family picnic)
    "AF-BG-18184", "AF-BG-20442", "AF-BG-22740", "AF-BG-23178", "AF-BG-44978",
    "AF-BG-6293", "AF-BG-6864", "AF-BG-6997", "AF-BG-7265", "AF-BG-7871",
    # round 2 (cartoon shoppers, dancers, landscapes, apocalyptic city, spider, cartoon ref)
    "AF-BG-18183", "AF-BG-22739", "AF-BG-23555", "AF-BG-23578", "AF-BG-32035",
    "AF-BG-43124", "AF-BG-6292", "AF-BG-6996", "AF-BG-7870", "AF-BG-20443", "AF-BG-38113",
    # round 3 (coffee-cup graphic, planet, snow/sun-orb, birds, singing woman, house-in-field,
    # sunset hills, covered bridge, cabin bedrooms x2, honeycomb, cloudy sky, horseback statue,
    # CG building) — mislabeling is spread across ALL subtypes on this shelf, not clustered
    "AF-BG-11655", "AF-BG-14909", "AF-BG-15894", "AF-BG-15906", "AF-BG-16364",
    "AF-BG-20989", "AF-BG-2139", "AF-BG-23034", "AF-BG-23174", "AF-BG-29846",
    "AF-BG-32345", "AF-BG-34476", "AF-BG-4899", "AF-BG-63128", "AF-BG-6598",
    # round 4 (leaves, coffee-cup, planet, fire-orb, near-black x5, singing woman, houses x2,
    # honeycomb, cabin, equestrian statues x2, purple dusk, mountains, palms, gavel-macro-black)
    "AF-BG-10025", "AF-BG-11805", "AF-BG-14784", "AF-BG-16117", "AF-BG-17528",
    "AF-BG-20441", "AF-BG-22901", "AF-BG-25662", "AF-BG-28714", "AF-BG-32168",
    "AF-BG-3361", "AF-BG-38179", "AF-BG-3983", "AF-BG-39989", "AF-BG-62427",
    "AF-BG-63004", "AF-BG-6840", "AF-BG-7266", "AF-LIGHT-3018",
}

# whole subtypes whose clips are reliably mislabeled junk on this shelf (every sampled clip
# was off-topic: cartoon characters, food, dancers, landscapes). Dropped entirely for cotton.
SUBTYPE_BLOCK = {
    "evidence_bag", "one_way_mirror_room", "boardroom_table_dark",
    "lady_justice_statue", "us_constitution_document",
}


def _blocked(x) -> bool:
    name = Path(str(x.get("path", ""))).name
    fid = name.split("__", 1)[0]
    st = str(x.get("subtype", "")).lower()
    return fid in BLOCK_IDS or st in SUBTYPE_BLOCK


def _dynamic(x) -> bool:
    st = str(x.get("subtype", "")).lower()
    name = str(x.get("path", "")).lower()
    return not any(k in st or k in name for k in FEATURELESS)


def even_sample(items: list, n: int) -> list:
    if n >= len(items):
        return items
    step = len(items) / n
    return [items[int(i * step)] for i in range(n)]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, choices=list(PLANS))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    plan = PLANS[a.slug]
    assets = json.loads(MANIFEST.read_text(encoding="utf-8"))["assets"]
    # index videos by theme
    by_theme: dict[str, list] = {}
    for x in assets:
        if x.get("kind") != "video":
            continue
        if not _dynamic(x):   # design rule: drop featureless / near-static b-roll
            continue
        if _blocked(x):       # visual-QC blocklist: mislabeled off-topic stock
            continue
        th = theme_of(x.get("subtype", ""))
        by_theme.setdefault(th, []).append(x)
    for th in by_theme:
        by_theme[th].sort(key=lambda x: x["id"])

    dest = ROOT / "remotion" / "public" / a.slug / "factory"
    dest.mkdir(parents=True, exist_ok=True)
    staged, missing, per = 0, 0, {}
    seen: set[str] = set()
    for theme, count in plan.items():
        pool = by_theme.get(theme, [])
        picks = even_sample(pool, count)
        got = 0
        for x in picks:
            name = Path(x["path"]).name
            if name in seen:
                continue
            seen.add(name)
            src = SHELF / x["path"]
            dst = dest / name
            if a.dry_run:
                got += 1
                continue
            if dst.exists() and dst.stat().st_size > 1024:
                got += 1
                continue
            if not src.exists():
                missing += 1
                continue
            shutil.copy2(src, dst)
            got += 1
            staged += 1
        per[theme] = got
    total_on_disk = len([p for p in dest.glob("*.mp4")])
    print(f"[{a.slug}] plan={sum(plan.values())} per-theme={per} newly_copied={staged} "
          f"missing_src={missing} total_on_disk={total_on_disk} dest={dest}")
    # diversity sanity: distinct subtypes
    subtypes = {Path(p).stem.split('__', 1)[-1] for p in dest.glob('*.mp4')}
    print(f"distinct_subtype_labels={len(subtypes)} (footage_diversity wants variety); dir={dest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
