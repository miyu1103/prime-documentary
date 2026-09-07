#!/usr/bin/env python
"""Technical QC for EP44 Tekoh stills."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-044-tekoh"
MANIFEST = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-resolution", action="store_true")
    args = ap.parse_args()
    if not MANIFEST.exists():
        print(f"FAIL missing {MANIFEST}")
        return 1
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    for item in data.get("stills", []):
        if item.get("role") != "body":
            continue
        path = Path(str(item.get("path") or ""))
        if not path.is_file():
            errors.append(f"{item.get('asset_id')} missing {path}")
            continue
        try:
            with Image.open(path) as im:
                if max(im.size) < 3840:
                    errors.append(f"{item.get('asset_id')} long edge {max(im.size)} < 3840")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{item.get('asset_id')} unreadable image: {exc}")
    print(("PASS" if not errors else "FAIL") + f" tekoh_stills_resolution checked={len([x for x in data.get('stills', []) if x.get('role') == 'body'])}")
    for err in errors[:30]:
        print(f"  ! {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
