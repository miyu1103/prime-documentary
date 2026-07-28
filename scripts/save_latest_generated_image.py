from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image


GEN_ROOT = Path(r"C:/Users/aab15/.codex/generated_images")
MEDIA_ROOT = Path(r"H:/pd-media/assets/ai/tekoh")
PUBLIC_ROOT = Path(r"C:/Users/aab15/Documents/prime-documentary/remotion/public/tekoh/img")


def latest_png(root: Path) -> Path:
    candidates = [p for p in root.rglob("*.png") if p.is_file()]
    if not candidates:
        raise SystemExit(f"no generated png found under {root}")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def save_resized(src: Path, dest: Path, overwrite: bool) -> None:
    if dest.exists() and not overwrite:
        raise SystemExit(f"exists: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        out = im.convert("RGB").resize((3840, 2160), Image.Resampling.LANCZOS)
        out.save(dest, quality=95, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("asset_id", help="Still id, e.g. S08")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    asset_id = args.asset_id
    if re.fullmatch(r"s\d{2}", asset_id, flags=re.IGNORECASE):
        asset_id = asset_id.upper()
    src = latest_png(GEN_ROOT)
    dests = [MEDIA_ROOT / f"{asset_id}.png", PUBLIC_ROOT / f"{asset_id}.png"]
    for dest in dests:
        save_resized(src, dest, args.overwrite)

    print(f"source={src}")
    for dest in dests:
        with Image.open(dest) as im:
            print(f"{dest} {im.size}")


if __name__ == "__main__":
    main()
