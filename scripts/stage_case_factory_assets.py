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
    "cotton": {  # eyewitness / lineup / DNA lab / courtroom / prison
        "crime_police": 20, "legal_court": 20, "forensics_dna": 14, "medical_lab": 10,
        "documents_paper": 12, "urban_night": 12, "atmosphere_symbolic": 6, "surveillance_tech": 2,
    },
}


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
