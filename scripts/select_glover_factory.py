#!/usr/bin/env python
"""Verify EP48 Glover generated factory loops do not reuse EP39-EP47 sha256 values."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-048-glover"
MANIFEST = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"


def collect_prior_sha() -> set[str]:
    out: set[str] = set()
    for ep_dir in (ROOT / "episodes").glob("PD-2026-0[3-4][0-9]-*"):
        try:
            ep_num = int(ep_dir.name.split("-")[2])
        except Exception:
            continue
        if not (39 <= ep_num <= 47):
            continue
        for path in list(ep_dir.glob("05_stock/stock_ledger*.json")) + list(ep_dir.glob("05_visuals/asset_manifest*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            for key in ["items", "stills", "factory", "motion", "overlay"]:
                for item in data.get(key, []) if isinstance(data, dict) else []:
                    if isinstance(item, dict) and item.get("sha256"):
                        out.add(str(item["sha256"]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-no-prior-overlap", action="store_true")
    args = ap.parse_args()
    if not args.verify_no_prior_overlap:
        print("Use --verify-no-prior-overlap")
        return 2
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    prior = collect_prior_sha()
    current = {str(item.get("sha256")) for item in data.get("factory", []) if item.get("sha256")}
    overlap = sorted(current & prior)
    print(f"{'PASS' if not overlap else 'FAIL'} glover_factory_prior_overlap checked={len(current)} overlap={len(overlap)}")
    for sha in overlap[:20]:
        print(f"  ! {sha}")
    return 0 if not overlap else 1


if __name__ == "__main__":
    raise SystemExit(main())
