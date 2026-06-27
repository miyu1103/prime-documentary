#!/usr/bin/env python3
"""Stage approved factory assets for TheranosPremium and record provenance."""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-015-theranos"
MANIFEST = ROOT / "assets" / "asset_manifest.v001.json"
LEDGER = ROOT / "episodes" / EP / "05_stock" / "stock_ledger.v001.json"
OUT_TS = ROOT / "remotion" / "src" / "data" / "theranos_factory_assets.ts"
PUBLIC_ROOT = ROOT / "remotion" / "public" / "theranos" / "factory"
MEDIA_FACTORY = Path("H:/pd-media/assets")


SELECTED = [
    {
        "id": "AF-BG-1999",
        "role": "bg",
        "use_scenes": ["SPN-0004", "SPN-0008", "SPN-0019"],
        "notes": "lab glassware/test tubes; generic illustrative medical-lab texture, no Theranos device claim",
    },
    {
        "id": "AF-BG-25748",
        "role": "bg",
        "use_scenes": ["SPN-0001", "SPN-0004"],
        "notes": "blood-vial plate used symbolically, not a real Theranos sample or device",
    },
    {
        "id": "AF-BG-7274",
        "role": "bg",
        "use_scenes": ["SPN-0009", "SPN-0019"],
        "notes": "generic microscope close-up for diagnostic-stakes scenes",
    },
    {
        "id": "AF-BG-9898",
        "role": "bg",
        "use_scenes": ["SPN-0012", "SPN-0018"],
        "notes": "balance-scale brass plate for legal boundary / intent concept",
    },
    {
        "id": "AF-BG-0467",
        "role": "bg",
        "use_scenes": ["SPN-0013", "SPN-0014", "SPN-0024"],
        "notes": "empty courtroom-desk plate; general court illustration only",
    },
    {
        "id": "AF-BG-0468",
        "role": "bg",
        "use_scenes": ["SPN-0013", "SPN-0014"],
        "notes": "alternate empty courtroom interior for verdict sequence; general court illustration only",
    },
    {
        "id": "AF-BG-0470",
        "role": "bg",
        "use_scenes": ["SPN-0024", "SPN-0015"],
        "notes": "alternate court plate for prosecution/defense and split-verdict nuance",
    },
    {
        "id": "AF-BG-10161",
        "role": "bg",
        "use_scenes": ["SPN-0007", "SPN-0010", "SPN-0023"],
        "notes": "paper-file plate for documents/investigation scenes",
    },
    {
        "id": "AF-BG-12719",
        "role": "bg",
        "use_scenes": ["SPN-0005", "SPN-0010"],
        "notes": "stock-report plate for valuation/collapse scenes",
    },
    {
        "id": "AF-BG-2000",
        "role": "bg",
        "use_scenes": ["SPN-0004", "SPN-0008"],
        "notes": "generic laboratory glassware variation; symbolic only, no real Theranos device claim",
    },
    {
        "id": "AF-BG-2001",
        "role": "bg",
        "use_scenes": ["SPN-0009", "SPN-0019"],
        "notes": "generic laboratory plate for diagnostic-stakes scenes; symbolic only",
    },
    {
        "id": "AF-LIGHT-0220",
        "role": "light",
        "use_scenes": ["SPN-0013"],
        "notes": "god-rays light accent for verdict release",
    },
    {
        "id": "AF-LIGHT-2059",
        "role": "light",
        "use_scenes": ["SPN-0001", "SPN-0005", "SPN-0020"],
        "notes": "blue light leak for cold documentary finish",
    },
    {
        "id": "AF-VFX-0001",
        "role": "vfx",
        "use_scenes": ["SPN-0013", "SPN-0014"],
        "notes": "smoke overlay for verdict atmosphere, kept subtle",
    },
    {
        "id": "AF-PART-0268",
        "role": "particle",
        "use_scenes": ["SPN-0007", "SPN-0010", "SPN-0012", "SPN-0013"],
        "notes": "floating dust overlay for depth",
    },
    {
        "id": "AF-TEX-0027",
        "role": "texture",
        "use_scenes": ["SPN-0011", "SPN-0012", "SPN-0018", "SPN-0020"],
        "notes": "dark marble texture for sober legal/series-summary cards",
    },
]


def is_allowed(asset: dict) -> bool:
    license_name = str(asset.get("license", "")).lower()
    return "pexels" in license_name or "pixabay" in license_name or "allowed" in license_name


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))["assets"]
    by_id = {item["id"]: item for item in manifest}
    existing = json.loads(LEDGER.read_text(encoding="utf-8"))
    existing_assets = existing.setdefault("assets", [])
    existing["assets"] = [
        item
        for item in existing_assets
        if not (
            item.get("asset_type") == "factory_stock"
            and str(item.get("asset_id", "")).startswith(f"{EP}-AF-")
        )
    ]
    existing_assets = existing["assets"]
    now = datetime.now(timezone.utc).isoformat()

    staged: list[dict] = []
    for selected in SELECTED:
        asset = by_id[selected["id"]]
        if not is_allowed(asset):
            raise RuntimeError(f"License is not allowed for {asset['id']}: {asset.get('license')}")
        src = MEDIA_FACTORY / asset["path"]
        if not src.exists():
            raise FileNotFoundError(src)
        source_rel = Path(asset["path"])
        rel_public = Path(*source_rel.parts[1:]) if source_rel.parts and source_rel.parts[0] == "factory" else source_rel
        dst = PUBLIC_ROOT / rel_public
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

        static_path = f"theranos/factory/{rel_public.as_posix()}"
        staged_item = {
            "id": asset["id"],
            "role": selected["role"],
            "subtype": asset.get("subtype"),
            "kind": asset.get("kind"),
            "staticPath": static_path,
            "useScenes": selected["use_scenes"],
            "sha256": asset.get("sha256"),
        }
        staged.append(staged_item)

        ledger_id = f"{EP}-{asset['id']}"
        existing_assets.append(
            {
                "asset_id": ledger_id,
                "asset_type": "factory_stock",
                "factory_asset_id": asset["id"],
                "role": selected["role"],
                "span_id": selected["use_scenes"],
                "file": f"assets/{asset['path']}",
                "remotion_static_file": static_path,
                "source": asset.get("source"),
                "source_url": asset.get("sourceUrl"),
                "author": "not_provided_in_factory_manifest",
                "license": asset.get("license"),
                "commercial_use": "allowed",
                "retrieved_at": "recorded from asset_manifest.v001.json; inventory dated 2026-06-23",
                "ledger_recorded_at": now,
                "sha256": asset.get("sha256"),
                "bytes": asset.get("bytes"),
                "use_scene": selected["use_scenes"],
                "usage_notes": selected["notes"],
                "r3_notes": "generic illustrative/symbolic stock only; not Theranos real footage, device, logo, facility, or person likeness",
            }
        )

    LEDGER.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_TS.write_text(
        "export type TheranosFactoryAsset = {\n"
        "  id: string;\n"
        "  role: 'bg' | 'light' | 'vfx' | 'particle' | 'texture';\n"
        "  subtype: string;\n"
        "  kind: string;\n"
        "  staticPath: string;\n"
        "  useScenes: string[];\n"
        "  sha256: string;\n"
        "};\n"
        f"export const THERANOS_FACTORY_ASSETS: TheranosFactoryAsset[] = {json.dumps(staged, indent=2, ensure_ascii=False)};\n",
        encoding="utf-8",
    )
    print(f"staged={len(staged)} public_root={PUBLIC_ROOT}")
    print(f"ledger={LEDGER}")
    print(f"data={OUT_TS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
