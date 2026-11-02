#!/usr/bin/env python
"""Validate EP48 Glover asset manifest from the consumer side."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_glover_asset_manifest import evaluate


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", type=Path, required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.assets.is_file():
        print(f"FAIL glover_asset_manifest: missing {args.assets}")
        return 1
    data = json.loads(args.assets.read_text(encoding="utf-8"))
    errors = evaluate(data)
    result = {"ok": not errors, "asset_manifest": str(args.assets), "errors": errors, "counts": data.get("counts")}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if not errors else "FAIL") + f" glover_asset_manifest: {args.assets}")
        for err in errors[:40]:
            print(f"  ! {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
