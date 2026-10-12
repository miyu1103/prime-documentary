#!/usr/bin/env python
"""INTRA-EPISODE asset reuse gate: stop the same picture coming back again and again.

Owner directive 2026-07-19: 「1動画に同じ素材はなるべく繰り返し使用しないで」.

`PD_ONE_PASS_PRODUCTION_SPEC.v2` row 7 already says "no single clip reused > 3x", but
nothing enforced it, so it drifted: EP38 kidsforcash runs 172 cuts off 81 distinct
assets (mean 2.12 uses) with 11 assets used 4x -- over the spec's own cap. Repetition
reads as "cheap AI slideshow", which is exactly the retention + YPP-policy risk in
[[pd-monetization-strategy]].

The cap is deliberately asymmetric, because the assets differ in cost:

  * FACTORY stock clips -- effectively free: an 11,443-clip library sits on
    E:/pd-media/assets/factory. There is no excuse to repeat one. CAP = 1.
  * i2v MOTION shots -- very expensive (~24-73 GPU-min each). CAP = 2.
  * SDXL STILLS -- cheap-ish but not free. CAP = 2.

Plus a whole-film floor: most cuts must be a FIRST use of their asset, so an episode
cannot satisfy per-asset caps while still feeling repetitive.

Read-only. No writes, no paid calls. Exit 0 = PASS, 1 = FAIL.

Usage:
    python scripts/check_asset_reuse.py <film.json>
    python scripts/check_asset_reuse.py <film.json> --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # cp932 guard (Windows)
except Exception:
    pass

CHECK_NAME = "asset_reuse"

MAX_USES_FACTORY = 1     # free + 11,443 available -> never repeat
MAX_USES_MOTION = 2      # i2v costs ~24-73 GPU-min per clip
MAX_USES_STILL = 2       # SDXL still
MIN_FIRST_USE_SHARE = 0.70   # >=70% of cuts must be the first appearance of their asset

ASSET_KEYS = ("image", "video", "src", "asset", "still", "clip", "file", "path")


def asset_of(cut: dict) -> str | None:
    for k in ASSET_KEYS:
        v = cut.get(k)
        if v:
            return str(v)
    return None


def kind_of(path: str) -> str:
    p = path.lower().replace("\\", "/")
    if "/factory" in p or re.search(r"\baf-bg-", p):
        return "factory"
    if p.endswith((".mp4", ".mov", ".webm")) or "ai_video" in p or "_rife" in p:
        return "motion"
    return "still"


CAPS = {"factory": MAX_USES_FACTORY, "motion": MAX_USES_MOTION, "still": MAX_USES_STILL}


def evaluate_film(film_path: Path) -> dict:
    data = json.loads(film_path.read_text(encoding="utf-8"))
    cuts = data.get("cuts") or []
    assets = [a for a in (asset_of(c) for c in cuts) if a]
    if not assets:
        return {"check": CHECK_NAME, "ok": True, "skipped": True,
                "reason": f"no resolvable assets on cuts in {film_path.name}"}

    uses = Counter(assets)
    first_uses = len(uses)
    first_use_share = first_uses / len(assets)

    violations = []
    for path, n in uses.most_common():
        k = kind_of(path)
        if n > CAPS[k]:
            violations.append({"asset": path, "kind": k, "uses": n, "cap": CAPS[k]})

    ok = not violations and first_use_share >= MIN_FIRST_USE_SHARE

    by_kind = Counter(kind_of(a) for a in uses)
    return {
        "check": CHECK_NAME,
        "ok": ok,
        "film": str(film_path),
        "cuts_with_asset": len(assets),
        "distinct_assets": first_uses,
        "mean_uses": round(len(assets) / first_uses, 2),
        "first_use_share": round(first_use_share, 3),
        "min_first_use_share": MIN_FIRST_USE_SHARE,
        "caps": CAPS,
        "distinct_by_kind": dict(by_kind),
        "violations": violations,
        "worst": [{"asset": p, "uses": n} for p, n in uses.most_common(5)],
    }


def _find_film(epdir: Path) -> Path | None:
    slug = epdir.name.split("-")[-1]
    root = epdir.parent.parent
    cands = list((root / "remotion/src/data").glob(f"*{slug}*film*.json"))
    cands += list(epdir.glob("04_scenes/*film*.json"))
    return max(cands, key=lambda p: p.stat().st_size) if cands else None


def evaluate(epdir: Path) -> dict:
    """PREFLIGHT adapter for preflight_render_gate._run_ext_gate."""
    epdir = Path(epdir)
    film = _find_film(epdir)
    if film is None:
        return {"ok": True, "skipped": True, "reason": "no film.json yet"}
    r = evaluate_film(film)
    if r.get("skipped"):
        return {"ok": True, "skipped": True, "reason": r.get("reason", "")}
    if r["ok"]:
        reason = (f"{r['distinct_assets']} distinct over {r['cuts_with_asset']} cuts "
                  f"(mean {r['mean_uses']}x, first-use {r['first_use_share']:.0%})")
    else:
        v = r["violations"]
        head = "; ".join(f"{Path(x['asset']).name} {x['uses']}x>{x['cap']}" for x in v[:4])
        reason = (f"{len(v)} asset(s) over cap [{head}]" if v else "")
        if r["first_use_share"] < MIN_FIRST_USE_SHARE:
            reason += (f" | first-use share {r['first_use_share']:.0%} < "
                       f"{MIN_FIRST_USE_SHARE:.0%} (mean {r['mean_uses']}x per asset)")
    return {"ok": r["ok"], "hard": True, "skipped": False, "reason": reason.strip(" |"), **r}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("film", type=Path)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if not a.film.exists():
        print(f"FAIL {CHECK_NAME}: no such film {a.film}")
        return 1
    r = evaluate_film(a.film)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["ok"] else 1
    if r.get("skipped"):
        print(f"WARN {CHECK_NAME}: {r['reason']}")
        return 0
    print(f"{'PASS' if r['ok'] else 'FAIL'} {CHECK_NAME}: "
          f"{r['distinct_assets']} distinct assets over {r['cuts_with_asset']} cuts "
          f"(mean {r['mean_uses']}x)")
    print(f"  first-use share {r['first_use_share']:.0%} (floor {MIN_FIRST_USE_SHARE:.0%})")
    print(f"  caps  factory {MAX_USES_FACTORY} | motion {MAX_USES_MOTION} | still {MAX_USES_STILL}")
    for v in r["violations"][:12]:
        print(f"  ! {v['kind']:7} {v['uses']}x (cap {v['cap']})  {v['asset'][-60:]}")
    if len(r["violations"]) > 12:
        print(f"  ... and {len(r['violations']) - 12} more")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
