#!/usr/bin/env python
"""Save one Codex built-in generated image as an EP58 Lejeune asset."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
MEDIA_DIR = Path("H:/pd-media/assets/ai/lejeune")
PUBLIC_IMG_DIR = ROOT / "remotion" / "public" / "lejeune" / "img"
VISUAL_DIR = ROOT / "episodes" / "PD-2026-058-lejeune" / "05_visuals"
PROGRESS = VISUAL_DIR / "builtin_imagegen_progress.v001.jsonl"
W, H = 3840, 2160


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def role_for(name: str) -> str:
    if name.startswith("S"):
        return "body"
    if name.startswith("M") and name.endswith("_src"):
        return "i2v_source"
    if name.startswith("T") and name.endswith("_face"):
        return "thumb_face"
    if name.startswith("F"):
        return "f_series_aux"
    raise SystemExit(f"unsupported asset id: {name}")


def existing_files() -> set[str]:
    if not PROGRESS.exists():
        return set()
    files: set[str] = set()
    for line in PROGRESS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            files.add(str(json.loads(line).get("file")))
        except json.JSONDecodeError:
            continue
    return files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("asset_id", help="S001, M01_src, T01_face, or F001")
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--quick-qc", default="")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    asset_id = args.asset_id.removesuffix(".png")
    file_name = f"{asset_id}.png"
    role = role_for(asset_id)
    src = args.source
    if not src.is_file():
        raise SystemExit(f"source not found: {src}")

    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    VISUAL_DIR.mkdir(parents=True, exist_ok=True)
    media = MEDIA_DIR / file_name
    public = PUBLIC_IMG_DIR / file_name if role in {"body", "i2v_source"} else None
    targets = [media] + ([public] if public is not None else [])
    if not args.force:
        for target in targets:
            if target is not None and target.exists():
                raise SystemExit(f"exists: {target}")

    with Image.open(src) as im:
        fitted = ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (W, H), Image.Resampling.LANCZOS)
        fitted.save(media, quality=95, optimize=True)
    if public is not None:
        public.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(media, public)

    digest = sha256(media)
    rec = {
        "file": file_name,
        "role": role,
        "source": str(src),
        "media": str(media),
        "public": str(public) if public is not None else None,
        "width": W,
        "height": H,
        "sha256": digest,
        "saved_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "qc_visual_quick": args.quick_qc,
    }
    if file_name not in existing_files() or args.force:
        with PROGRESS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(json.dumps({"file": file_name, "role": role, "media": str(media), "public": rec["public"], "sha256": digest[:16]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
