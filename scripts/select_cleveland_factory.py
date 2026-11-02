#!/usr/bin/env python
"""EP45 factory-footage verification helpers."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-045-cleveland"
MANIFEST = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
PRIOR_PUBLIC = [ROOT / "remotion" / "public" / s / "factory" for s in ("frazier", "lech", "thompson", "cleveland", "cleveland")]
PRIOR_SELECTED = [
    ROOT / "runs" / "qc" / "cleveland_factory_selected.v001.json",
    ROOT / "runs" / "qc" / "cleveland_factory_selected.v001.json",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def prior_shas() -> set[str]:
    out: set[str] = set()
    for folder in PRIOR_PUBLIC:
        if not folder.is_dir():
            continue
        for p in folder.iterdir():
            if p.is_file() and p.suffix.lower() in {".mp4", ".mov", ".webm"}:
                out.add(sha256_file(p))
    for jp in PRIOR_SELECTED:
        if not jp.exists():
            continue
        data = json.loads(jp.read_text(encoding="utf-8"))
        rows = data if isinstance(data, list) else data.get("factory", [])
        for row in rows:
            if isinstance(row, dict) and row.get("sha256"):
                out.add(str(row["sha256"]))
    return out


def verify_no_prior_overlap() -> int:
    if not MANIFEST.exists():
        print(f"FAIL missing {MANIFEST}")
        return 1
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    prior = prior_shas()
    overlaps = []
    for item in data.get("factory", []):
        sha = item.get("sha256")
        if sha and sha in prior:
            overlaps.append({"asset_id": item.get("asset_id"), "sha256": sha, "public_path": item.get("public_path")})
    result = {"ok": not overlaps, "prior_sha_count": len(prior), "overlaps": overlaps}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-no-prior-overlap", action="store_true")
    args = ap.parse_args()
    if args.verify_no_prior_overlap:
        return verify_no_prior_overlap()
    print("No selection phase implemented here. Use --verify-no-prior-overlap after asset_manifest.v001.json exists.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

