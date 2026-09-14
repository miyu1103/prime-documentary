#!/usr/bin/env python
"""Stage EP56 Post Office A-side public assets."""
from __future__ import annotations

import json

from build_postoffice_asset_manifest import build_manifest, evaluate, stage_assets


if __name__ == "__main__":
    stage_assets()
    data = build_manifest()
    errors = evaluate(data)
    print(("PASS" if not errors else "FAIL") + " postoffice_stage_assets")
    print(json.dumps(data.get("counts"), ensure_ascii=False))
    for err in errors[:120]:
        print(f"  ! {err}")
    raise SystemExit(0 if not errors else 1)
