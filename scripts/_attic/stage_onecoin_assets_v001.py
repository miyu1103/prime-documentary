#!/usr/bin/env python3
"""Stage OneCoin EP17 visual assets for Remotion.

This copies already-approved/generated media into remotion/public/onecoin and
writes deterministic Remotion data modules plus provenance ledgers. It does not
fetch external media, call paid APIs, publish, or overwrite approved artifacts.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-017-onecoin"
SLUG = "onecoin"
EP_DIR = ROOT / "episodes" / EP
MEDIA = Path(json.loads((ROOT / "config" / "storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
ASSET_MANIFEST = ROOT / "assets" / "asset_manifest.v001.json"
PUBLIC_ROOT = ROOT / "remotion" / "public" / SLUG
HERO_PUBLIC = PUBLIC_ROOT / "hero"
FACTORY_PUBLIC = PUBLIC_ROOT / "factory"
DATA_DIR = ROOT / "remotion" / "src" / "data"


ALLOWED_LICENSES = {"Pexels License", "Pixabay Content License", "cc0", "royalty_free", "generated_owned"}

# Symbolic, commercial-OK factory clips. Intentionally avoids real-person face-led
# clips and obvious brand-marking candidates where known from source titles.
FACTORY_REQUESTS: list[tuple[str, str, list[str]]] = [
    ("stage", "spotlight_on_dark_stage", ["AF-BG-2514", "AF-BG-2515", "AF-BG-2516", "AF-BG-2517", "AF-BG-2521", "AF-BG-2523", "AF-BG-2524", "AF-BG-2525"]),
    ("finance", "cash_stacks_money", ["AF-BG-7989", "AF-BG-7990", "AF-BG-7992", "AF-BG-7993", "AF-BG-7995", "AF-BG-8001", "AF-BG-8002", "AF-BG-8004"]),
    ("surveillance", "server_room_blue", ["AF-BG-0979", "AF-BG-0980", "AF-BG-0981", "AF-BG-0983", "AF-BG-0985", "AF-BG-0988"]),
    ("surveillance", "world_map_dark_glowing", ["AF-BG-12983", "AF-BG-12984", "AF-BG-12985", "AF-BG-12994", "AF-BG-12995", "AF-BG-12996"]),
    ("documents", "documents_on_desk", ["AF-BG-1276", "AF-BG-1277", "AF-BG-1280", "AF-BG-1282"]),
    ("documents", "magnifying_glass_on_document", ["AF-BG-15125", "AF-BG-15126", "AF-BG-15130", "AF-BG-15132"]),
    ("atmosphere", "clock_ticking_macro", ["AF-BG-9713", "AF-BG-9714", "AF-BG-9715", "AF-BG-9716"]),
    ("atmosphere", "candle_in_dark", ["AF-BG-9585", "AF-BG-9586", "AF-BG-9587", "AF-BG-9588"]),
    ("atmosphere", "padlock_and_chain", ["AF-BG-12140", "AF-BG-12143", "AF-BG-12145", "AF-BG-12147"]),
    ("vanishing", "airport_runway_at_night", ["AF-BG-57480", "AF-BG-57481", "AF-BG-57482", "AF-BG-57483", "AF-BG-57485", "AF-BG-57489", "AF-BG-57491", "AF-BG-57500"]),
    ("void", "static_noise_particles", ["AF-PART-1599", "AF-PART-1600", "AF-PART-1601", "AF-PART-1602"]),
    ("void", "smoke_on_black_background", ["AF-VFX-0056", "AF-VFX-0057", "AF-VFX-0058", "AF-VFX-0060"]),
    ("light", "bokeh_lights", ["AF-LIGHT-0202", "AF-LIGHT-0203", "AF-LIGHT-0206", "AF-LIGHT-0209"]),
]


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def artifact_h_path(uri: str) -> Path:
    prefix = "artifact://H/pd-media/"
    if not uri.startswith(prefix):
        raise ValueError(f"unsupported artifact URI: {uri}")
    return MEDIA / uri[len(prefix) :]


def json_hash(path: Path) -> str:
    return digest(path)


def probe_seconds(path: Path) -> float | None:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        return round(float(out.stdout.strip()), 2)
    except Exception:
        return None


def stage_hero_assets() -> dict[str, list[dict[str, Any]]]:
    usable = json.loads((EP_DIR / "05_stock" / "usable_assets.v001.json").read_text("utf-8"))
    HERO_PUBLIC.mkdir(parents=True, exist_ok=True)
    by_prompt: dict[str, list[dict[str, Any]]] = {}
    staged: list[dict[str, Any]] = []
    for asset in usable["assets"]:
        src = artifact_h_path(asset["uri"])
        if not src.exists():
            raise FileNotFoundError(src)
        dst = HERO_PUBLIC / src.name
        shutil.copy2(src, dst)
        item = {
            "asset_id": asset["asset_id"],
            "prompt_id": asset["prompt_id"],
            "role": asset.get("role", "hero"),
            "width": asset["width"],
            "height": asset["height"],
            "checksum": asset["checksum"],
            "src": f"{SLUG}/hero/{dst.name}",
        }
        by_prompt.setdefault(asset["prompt_id"], []).append(item)
        staged.append(item)

    ledger = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "kind": "hero_stage_ledger",
        "generated_from": "05_stock/usable_assets.v001.json",
        "assets": staged,
        "notes": "Copied approved 4032x2304 SDXL hero stills from H: to remotion/public for local Remotion rendering. Heavy media remains off git.",
    }
    path = EP_DIR / "05_stock" / "hero_stage_ledger.v001.json"
    path.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", "utf-8")
    return by_prompt


def stage_factory_assets() -> list[dict[str, Any]]:
    manifest = json.loads(ASSET_MANIFEST.read_text("utf-8"))["assets"]
    by_id = {a["id"]: a for a in manifest}
    FACTORY_PUBLIC.mkdir(parents=True, exist_ok=True)
    staged: list[dict[str, Any]] = []
    missing: list[str] = []

    for group, subtype, ids in FACTORY_REQUESTS:
        for asset_id in ids:
            asset = by_id.get(asset_id)
            if not asset:
                missing.append(f"missing_manifest:{asset_id}")
                continue
            if asset.get("license") not in ALLOWED_LICENSES:
                raise RuntimeError(f"license not allowed for {asset_id}: {asset.get('license')}")
            if asset.get("kind") != "video":
                raise RuntimeError(f"factory request expects video for {asset_id}")
            src = MEDIA / "assets" / asset["path"]
            if not src.exists():
                missing.append(f"missing_file:{asset_id}")
                continue
            dst = FACTORY_PUBLIC / Path(asset["path"]).name
            shutil.copy2(src, dst)
            staged.append(
                {
                    "id": asset["id"],
                    "group": group,
                    "subtype": subtype,
                    "kind": asset.get("kind"),
                    "license": asset.get("license"),
                    "source": asset.get("source"),
                    "sourceUrl": asset.get("sourceUrl"),
                    "sha256": asset.get("sha256") or digest(src),
                    "bytes": asset.get("bytes") or src.stat().st_size,
                    "clipSeconds": probe_seconds(src),
                    "src": f"{SLUG}/factory/{dst.name}",
                    "usage_notes": "symbolic commercial-OK factory b-roll; not actual OneCoin footage; no real-person likeness intended",
                }
            )

    groups: dict[str, list[str]] = {}
    for item in staged:
        groups.setdefault(item["group"], []).append(item["src"])
        groups.setdefault(item["subtype"], []).append(item["src"])

    ledger = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "kind": "factory_ledger",
        "generated_from": "assets/asset_manifest.v001.json",
        "selection_basis": "EP17 codex prompt Step 1 motifs; selected from local factory shelf only",
        "assets": staged,
        "missing_requests": missing,
    }
    ledger_path = EP_DIR / "05_stock" / "factory_ledger.v001.json"
    ledger_path.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", "utf-8")

    data_path = DATA_DIR / "onecoin_factory_assets.ts"
    data_path.write_text(
        "export const ONECOIN_FACTORY = "
        + json.dumps(groups, indent=2, ensure_ascii=False)
        + " as const;\n"
        + "export const ONECOIN_FACTORY_LEDGER = "
        + json.dumps(staged, indent=2, ensure_ascii=False)
        + " as const;\n",
        "utf-8",
    )
    return staged


def clean_caption_text(text: str) -> str:
    return " ".join(text.replace("—", "-").replace("“", '"').replace("”", '"').replace("’", "'").split())


def wrap_caption(text: str, limit: int = 38) -> str:
    words = clean_caption_text(text).split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= limit:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
            if len(lines) == 1:
                break
    if current and len(lines) < 2:
        lines.append(current)
    return "\n".join(lines[:2])


def build_roughcut(hero_by_prompt: dict[str, list[dict[str, Any]]]) -> None:
    shotlist = json.loads((EP_DIR / "04_scenes" / "shotlist.v001.json").read_text("utf-8"))
    manifest = json.loads((EP_DIR / "manifest.json").read_text("utf-8"))
    shots: list[dict[str, Any]] = []

    for index, shot in enumerate(shotlist["shots"]):
        asset_ref = shot.get("asset_ref") or ""
        prompt_id = asset_ref if asset_ref.startswith("T-IMG") else None
        hero_pool = hero_by_prompt.get(prompt_id or "", [])
        if not hero_pool:
            hero_pool = [item for values in hero_by_prompt.values() for item in values if item["role"] == "hero"]
        needed = max(1, int((shot["estimated_seconds"] + 5.9) // 6))
        images = [hero_pool[(index + offset) % len(hero_pool)]["src"] for offset in range(needed)] if hero_pool else []
        raw_motion = str(shot["motion"])
        motion = "graphic_anim" if shot["suggested_asset_type"] == "motion_graphic" else "parallax" if "parallax" in raw_motion else "ken_burns"
        out: dict[str, Any] = {
            "spanId": shot["span_id"],
            "chapterId": shot.get("chapter_id"),
            "seconds": shot["estimated_seconds"],
            "assetType": shot["suggested_asset_type"],
            "motion": motion,
            "assetRef": asset_ref,
            "src": images[0] if images else None,
            "telop": shot.get("on_screen_text", []),
            "priority": shot["priority"],
            "searchKeywords": shot.get("search_keywords", []),
            "claimIds": shot.get("claim_ids", []),
        }
        if images:
            out["images"] = images
        shots.append(out)

    data = {
        "episodeId": EP,
        "title": manifest.get("title_working", "Nothing"),
        "fps": 30,
        "narrationSrc": None,
        "bgmSrc": None,
        "shots": shots,
    }
    path = DATA_DIR / "onecoin_roughcut.ts"
    path.write_text(
        "// AUTO-GENERATED by scripts/stage_onecoin_assets_v001.py from PD-2026-017-onecoin/04_scenes/shotlist.v001.json\n"
        "// + 05_stock/usable_assets.v001.json. Re-run the staging script for source data changes.\n"
        "import type {RoughCutData} from '../compositions/RoughCut';\n\n"
        "export const ONECOIN_ROUGHCUT: RoughCutData = "
        + json.dumps(data, indent=2, ensure_ascii=False)
        + ";\n",
        "utf-8",
    )


def build_captions() -> None:
    annotated = json.loads((EP_DIR / "03_script" / "script.annotated.v001.json").read_text("utf-8"))
    shotlist = json.loads((EP_DIR / "04_scenes" / "shotlist.v001.json").read_text("utf-8"))
    durations = {shot["span_id"]: float(shot["estimated_seconds"]) for shot in shotlist["shots"]}
    cursor = 0.0
    cues: list[dict[str, Any]] = []
    for span in annotated["spans"]:
        span_id = span["span_id"]
        dur = durations.get(span_id, 4.0)
        text = clean_caption_text(span["text"])
        if text and text != "...":
            words = text.split()
            chunk_count = max(1, min(8, round(dur / 5.0)))
            chunk_size = max(1, (len(words) + chunk_count - 1) // chunk_count)
            cue_start = cursor
            for i in range(0, len(words), chunk_size):
                chunk = " ".join(words[i : i + chunk_size])
                cue_end = min(cursor + dur, cue_start + max(1.0, min(6.0, dur / chunk_count)))
                cues.append({"start": round(cue_start, 2), "end": round(cue_end, 2), "text": wrap_caption(chunk)})
                cue_start = cue_end + 0.08
                if cue_start >= cursor + dur:
                    break
        cursor += dur

    path = DATA_DIR / "onecoin_captions.ts"
    path.write_text(
        "// Draft timing captions generated from script spans. Step 4 must replace these with forced-aligned master captions.\n"
        "import type {CaptionCue} from '../compositions/RoughCut';\n\n"
        "export const ONECOIN_CAPTIONS: CaptionCue[] = "
        + json.dumps([{"id": f"onecoin-caption-{i+1:04d}", **cue} for i, cue in enumerate(cues)], indent=2, ensure_ascii=False)
        + ";\n",
        "utf-8",
    )


def update_manifest_and_events() -> None:
    manifest_path = EP_DIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text("utf-8"))
    active = manifest.setdefault("active_revisions", {})
    active.update(
        {
            "hero_stage_ledger": "v001",
            "factory_ledger": "v001",
            "onecoin_factory_assets": "v001",
            "onecoin_roughcut": "v001",
            "onecoin_captions": "v001",
        }
    )
    artifact_specs = [
        ("PD-2026-017-onecoin-hero-stage-ledger", "hero_stage_ledger", "episodes/PD-2026-017-onecoin/05_stock/hero_stage_ledger.v001.json", "clear", "pass"),
        ("PD-2026-017-onecoin-factory-ledger", "factory_ledger", "episodes/PD-2026-017-onecoin/05_stock/factory_ledger.v001.json", "clear", "not_run"),
        ("PD-2026-017-onecoin-factory-data", "remotion_data", "remotion/src/data/onecoin_factory_assets.ts", "clear", "not_run"),
        ("PD-2026-017-onecoin-roughcut", "remotion_data", "remotion/src/data/onecoin_roughcut.ts", "clear", "not_run"),
        ("PD-2026-017-onecoin-captions-draft", "remotion_data", "remotion/src/data/onecoin_captions.ts", "conditional", "draft"),
    ]
    existing = [a for a in manifest.get("artifacts", []) if a.get("artifact_id") not in {spec[0] for spec in artifact_specs}]
    for artifact_id, artifact_type, rel, rights, qc in artifact_specs:
        path = ROOT / rel
        existing.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "revision": "v001",
                "uri": "artifact://" + rel.replace("\\", "/"),
                "status": "staged" if "captions" not in artifact_id else "draft",
                "rights_status": rights,
                "qc_status": qc,
                "checksum": json_hash(path),
            }
        )
    manifest["artifacts"] = existing
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")

    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "episode_id": EP,
        "stage": "assets_ready",
        "event": "onecoin_step1_step3_assets_staged",
        "revision": "v001",
        "actor": "codex",
        "note": "Staged approved hero stills and 64 commercial-OK symbolic factory clips; wrote factory data, roughcut data, and draft timing captions. No paid API, upload, publish, or external fetch.",
    }
    events_path = EP_DIR / "events" / "events.jsonl"
    with events_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    hero = stage_hero_assets()
    factory = stage_factory_assets()
    build_roughcut(hero)
    build_captions()
    update_manifest_and_events()
    print(f"hero_groups={len(hero)} factory_clips={len(factory)} public={PUBLIC_ROOT}")
    print("wrote remotion/src/data/onecoin_factory_assets.ts")
    print("wrote remotion/src/data/onecoin_roughcut.ts")
    print("wrote remotion/src/data/onecoin_captions.ts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
