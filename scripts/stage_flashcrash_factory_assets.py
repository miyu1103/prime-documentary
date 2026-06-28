#!/usr/bin/env python3
"""Stage licensed factory assets for EP18 Flash Crash.

Copies selected shelf assets from H:/pd-media into remotion/public so Remotion
can render them, then writes a rights ledger and the TS data consumed by the
FlashCrashPremium composition. No network or paid provider calls.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-018-flashcrash"
SLUG = "flashcrash"
MANIFEST = ROOT / "assets" / "asset_manifest.v001.json"
DEST = ROOT / "remotion" / "public" / SLUG / "factory"
LEDGER = ROOT / "episodes" / EP / "05_stock" / "stock_ledger.v001.json"
TS = ROOT / "remotion" / "src" / "data" / "flashcrash_factory_assets.ts"

SELECTED: dict[str, str] = {
    # Background layer: finance, system infrastructure, legal aftermath, atmosphere.
    "AF-BG-0001": "background",
    "AF-BG-0002": "background",
    "AF-BG-0003": "background",
    "AF-BG-0004": "background",
    "AF-BG-0005": "background",
    "AF-BG-0006": "background",
    "AF-BG-0007": "background",
    "AF-BG-0008": "background",
    "AF-BG-0010": "background",
    "AF-BG-0011": "background",
    "AF-BG-0153": "background",
    "AF-BG-0154": "background",
    "AF-BG-0155": "background",
    "AF-BG-0156": "background",
    "AF-BG-0158": "background",
    "AF-BG-0159": "background",
    "AF-BG-0160": "background",
    "AF-BG-0925": "background",
    "AF-BG-0926": "background",
    "AF-BG-0927": "background",
    "AF-BG-0928": "background",
    "AF-BG-0929": "background",
    "AF-BG-0930": "background",
    "AF-BG-0932": "background",
    "AF-BG-0465": "background",
    "AF-BG-0466": "background",
    "AF-BG-0467": "background",
    "AF-BG-0468": "background",
    "AF-BG-0232": "background",
    "AF-BG-0233": "background",
    "AF-BG-0234": "background",
    "AF-BG-0235": "background",
    "AF-BG-0236": "background",
    "AF-BG-0237": "background",
    # Light/VFX/texture layers.
    "AF-LIGHT-0001": "light",
    "AF-LIGHT-0002": "light",
    "AF-LIGHT-0003": "light",
    "AF-LIGHT-0004": "light",
    "AF-LIGHT-0005": "light",
    "AF-LIGHT-0006": "light",
    "AF-LIGHT-0007": "light",
    "AF-LIGHT-0008": "light",
    "AF-VFX-0070": "vfx",
    "AF-VFX-0071": "vfx",
    "AF-VFX-0072": "vfx",
    "AF-VFX-0073": "vfx",
    "AF-VFX-0074": "vfx",
    "AF-VFX-0075": "vfx",
    "AF-VFX-0076": "vfx",
    "AF-VFX-0077": "vfx",
    "AF-TEX-0005": "texture",
    "AF-TEX-0006": "texture",
    "AF-TEX-0009": "texture",
    "AF-TEX-0010": "texture",
    "AF-TEX-0013": "texture",
    "AF-TEX-0014": "texture",
    "AF-TEX-0017": "texture",
    "AF-TEX-0018": "texture",
}

ALLOWED_LICENSES = {"Pexels License", "Pixabay Content License"}


def media_root() -> Path:
    cfg = json.loads((ROOT / "config" / "storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ts_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def main() -> int:
    media = media_root()
    source_root = media / "assets"
    assets = json.loads(MANIFEST.read_text(encoding="utf-8"))["assets"]
    by_id = {row["id"]: row for row in assets}

    staged = []
    staged_paths: set[Path] = set()
    for asset_id, layer in SELECTED.items():
        asset = by_id.get(asset_id)
        if not asset:
            raise RuntimeError(f"missing asset in manifest: {asset_id}")
        if asset.get("license") not in ALLOWED_LICENSES:
            raise RuntimeError(f"asset {asset_id} license not allowed: {asset.get('license')}")
        source = source_root / asset["path"]
        if not source.is_file():
            raise RuntimeError(f"missing asset file: {source}")
        dest = DEST / Path(asset["path"]).relative_to("factory")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        staged_paths.add(dest.resolve())
        actual_sha = sha256_file(dest)
        manifest_sha = str(asset.get("sha256", "")).replace("sha256:", "")
        if manifest_sha and actual_sha != manifest_sha:
            raise RuntimeError(f"sha256 mismatch for {asset_id}")
        rel_src = dest.relative_to(ROOT / "remotion" / "public").as_posix()
        staged.append(
            {
                "id": asset_id,
                "layer": layer,
                "kind": asset.get("kind"),
                "src": rel_src,
                "source_path": asset["path"],
                "source": asset.get("source"),
                "source_url": asset.get("sourceUrl"),
                "license": asset.get("license"),
                "sha256": f"sha256:{actual_sha}",
                "bytes": dest.stat().st_size,
                "r3_note": "Factory decoration only; no real-person depiction, no causation claim.",
            }
        )

    if DEST.exists():
        for existing in DEST.rglob("*"):
            if existing.is_file() and existing.resolve() not in staged_paths:
                existing.unlink()

    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "selection_policy": "licensed factory assets only; symbolic finance/tech/legal/atmosphere layers; no real-person likeness or exchange/logo focus",
                "required_minimum_for_28min": 37,
                "asset_count": len(staged),
                "assets": staged,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "export type FlashCrashFactoryAsset = {",
        "  id: string;",
        "  src: string;",
        "  kind: 'image' | 'video';",
        "  layer: 'background' | 'light' | 'texture' | 'vfx';",
        "};",
        "",
        "export const FLASHCRASH_FACTORY_ASSETS: FlashCrashFactoryAsset[] = [",
    ]
    for row in staged:
        lines.append(
            "  "
            + "{ "
            + f"id: {ts_quote(row['id'])}, "
            + f"src: {ts_quote(row['src'])}, "
            + f"kind: {ts_quote(row['kind'])}, "
            + f"layer: {ts_quote(row['layer'])} "
            + "},"
        )
    lines.append("];")
    lines.append("")
    TS.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({"staged": len(staged), "dest": str(DEST), "ledger": str(LEDGER)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
