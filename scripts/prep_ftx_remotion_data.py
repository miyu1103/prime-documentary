"""Prepare Remotion public assets and TS data for PD-2026-004-ftx."""

from __future__ import annotations

import json
import math
import re
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-004-ftx"
MEDIA = Path(r"H:\pd-media")
VIS = MEDIA / "episodes" / EP / "05_visuals"
UPSCALED = VIS / "upscaled_4x_v001"
SDXL_HQ = VIS / "sdxl_coverage_hq_v001"
SDXL_EXPANSION = VIS / "sdxl_expansion_v001"
REMOTION_PUBLIC = ROOT / "remotion" / "public" / "ftx"
REMOTION_MOTION_PUBLIC = ROOT / "remotion" / "public" / "ftx_motion"
REMOTION_DATA = ROOT / "remotion" / "src" / "data" / "ftx_premium.ts"
TIMING = ROOT / "episodes" / EP / "08_edit" / "timing.v001.json"
SVD_MANIFEST = VIS / "svd_motion_v001" / "svd_motion_manifest.v001.json"

# SVD can make fake in-frame lettering swim or melt. Keep these as graded
# stills with camera motion rather than using the generated clip.
MOTION_EXCLUDE = {"COV-3007"}
USE_SVD_MOTION = False
MAX_SHOT_SEC = 8.0

SECTION_ASSETS: dict[str, list[str]] = {
    "00_hook": ["COV-0001", "COV-0004", "COV-0003", "COV-0002"],
    "01_cold_open": ["H03-code-vault-coins", "COV-0101", "COV-0102", "COV-0103", "COV-0104", "THUMB-A-dissolving-vault"],
    "02_opening": ["H05-balance-scale-safe", "COV-0201", "COV-0202", "COV-0203", "COV-0204"],
    "actI_trust": ["H06-boardroom-beanbag", "H07-controller-boardroom", "H08-money-to-skyscraper", "H09-two-towers-wall", "H10-secret-door-green-light", "COV-1001", "COV-1002", "COV-1003", "COV-1004", "COV-1005", "COV-1006", "COV-1007", "COV-1008"],
    "actII_code": ["H12-red-barrier-coin", "H13-exception-gate-vault", "H14-secret-siphon", "H15-scrubs-phone-savings", "COV-2001", "COV-2002", "COV-2003", "COV-2005", "COV-2006", "COV-2007", "COV-2008", "H03-code-vault-coins"],
    "actIII_run": ["H17-bank-run-crowd", "H20-crater-missing-gold", "THUMB-A-dissolving-vault", "COV-3001", "COV-3002", "COV-3003", "COV-3005", "COV-3007", "COV-3008", "H08-money-to-skyscraper", "H10-secret-door-green-light"],
    "actIV_trial": ["H21-courthouse-dawn", "H22-empty-witness-stand", "COV-4001", "COV-4002", "COV-4003", "COV-4004", "H23-gavel-verdict"],
    "actV_verdict": ["H23-gavel-verdict", "H25-prison-door-fall", "COV-4001", "COV-4004", "COV-4005", "COV-4002", "COV-4003", "H21-courthouse-dawn", "H22-empty-witness-stand"],
    "ending": ["H26-key-coin-custody", "H28-ledger-old-fraud", "COV-5001", "COV-5003", "COV-5004", "THUMB-B-hooded-code", "H20-crater-missing-gold"],
}

SECTION_TEXT = {
    "00_hook": ["WITHDRAWAL FROZEN", "3:00 A.M."],
    "01_cold_open": ["THE MONEY WAS ALREADY GONE", "$8 BILLION"],
    "02_opening": ["THE PROMISE", "YOUR MONEY IS STILL YOURS"],
    "actI_trust": ["THE TRUST MACHINE", "TWO COMPANIES"],
    "actII_code": ["ALLOW NEGATIVE", "THE SECRET DOOR"],
    "actIII_run": ["THE RUN", "TRUST EVAPORATES"],
    "actIV_trial": ["DID HE KNOW?", "THE TRIAL"],
    "actV_verdict": ["GUILTY", "ALL SEVEN COUNTS"],
    "ending": ["NOT YOUR KEYS", "NOT YOUR COINS"],
}

CHUNK_SECTION: dict[str, str] = {
    **{f"VC-{i:04d}": "actI_trust" for i in range(7, 14)},
    **{f"VC-{i:04d}": "actII_code" for i in range(14, 24)},
    **{f"VC-{i:04d}": "actIII_run" for i in range(24, 31)},
    **{f"VC-{i:04d}": "actIV_trial" for i in range(31, 34)},
    **{f"VC-{i:04d}": "actV_verdict" for i in range(34, 40)},
    **{f"VC-{i:04d}": "ending" for i in range(40, 45)},
}

SECTION_OFFSET: dict[str, int] = {
    "00_hook": 0,
    "01_cold_open": 1,
    "02_opening": 2,
    "actI_trust": 3,
    "actII_code": 5,
    "actIII_run": 7,
    "actIV_trial": 2,
    "actV_verdict": 4,
    "ending": 1,
}

SECTION_EXPANSION_PREFIX: dict[str, str] = {
    "00_hook": "X-HOOK-",
    "01_cold_open": "X-COLD-",
    "02_opening": "X-OPEN-",
    "actI_trust": "X-TRUST-",
    "actII_code": "X-CODE-",
    "actIII_run": "X-RUN-",
    "actIV_trial": "X-TRIAL-",
    "actV_verdict": "X-VERDICT-",
    "ending": "X-END-",
}


def slug(path: Path) -> str:
    name = path.stem.replace("PD-2026-004-ftx-", "")
    return name


def collect_assets() -> dict[str, Path]:
    assets: dict[str, Path] = {}
    # Prefer upscaled/prepared assets when present, but also allow new SDXL stills
    # directly. export_asset() will crop/scale them to a full 16:9 Remotion source.
    for root in [SDXL_HQ, SDXL_EXPANSION, UPSCALED]:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.png")):
            assets[slug(path)] = path
    return assets


def export_asset(src: Path, name: str) -> str:
    REMOTION_PUBLIC.mkdir(parents=True, exist_ok=True)
    out = REMOTION_PUBLIC / f"{name}.jpg"
    if out.exists():
        return f"ftx/{out.name}"
    with Image.open(src) as im:
        im = im.convert("RGB")
        # Keep a premium 2K 16:9 source for smooth camera movement. Scale up
        # direct SDXL images when needed; never letterbox them into a black canvas.
        scale = max(2560 / im.width, 1440 / im.height)
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.Resampling.LANCZOS)
        left = (im.width - 2560) // 2
        top = (im.height - 1440) // 2
        im = im.crop((left, top, left + 2560, top + 1440))
        canvas = Image.new("RGB", (2560, 1440), (0, 0, 0))
        canvas.paste(im, (0, 0))
        canvas.save(out, quality=94, subsampling=1)
    return f"ftx/{out.name}"


def export_motion_clips() -> dict[str, str]:
    if not SVD_MANIFEST.exists():
        return {}
    REMOTION_MOTION_PUBLIC.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(SVD_MANIFEST.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for record in manifest.get("clips", []):
        if record.get("asset") in MOTION_EXCLUDE:
            continue
        src = Path(record["file"])
        if not src.exists():
            continue
        safe = re.sub(r"[^A-Za-z0-9_-]+", "_", f"{record['id']}_{record['asset']}") + ".mp4"
        dst = REMOTION_MOTION_PUBLIC / safe
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)
        out[record["asset"]] = f"ftx_motion/{safe}"
    return out


def make_shots(timing: dict, public_assets: dict[str, str], motion_assets: dict[str, str]) -> list[dict]:
    shots = []
    scenes = timing["scenes"]
    section_counts: dict[str, int] = {}
    used_assets: set[str] = set()
    last_asset: str | None = None
    last_section: str | None = None
    for scene_index, scene in enumerate(scenes):
        section = CHUNK_SECTION.get(scene.get("chunk_id"), scene["section"])
        start = float(scene["start"])
        narration_end = float(scene["end"])
        next_start = float(scenes[scene_index + 1]["start"]) if scene_index + 1 < len(scenes) else narration_end
        # Visuals should cover the breath/gap before the next narration chunk. Otherwise Remotion
        # reveals the composition background, which reads as an unintended black flash.
        end = max(narration_end, next_start)
        scene_dur = max(0.12, end - start)
        segment_count = max(1, math.ceil(scene_dur / MAX_SHOT_SEC))
        segment_dur = scene_dur / segment_count
        expansion_prefix = SECTION_EXPANSION_PREFIX.get(section)
        expansion = sorted(key for key in public_assets if expansion_prefix and key.startswith(expansion_prefix))
        pool = SECTION_ASSETS.get(section, SECTION_ASSETS["ending"]) + expansion
        for segment_index in range(segment_count):
            seg_start = start + segment_dur * segment_index
            base = section_counts.get(section, 0)
            ordered = pool[base % len(pool) :] + pool[: base % len(pool)]
            asset_key = next((key for key in ordered if key not in used_assets and key in public_assets), None)
            if asset_key is None:
                asset_key = next((key for key in ordered if key != last_asset and key in public_assets), ordered[0])
            section_counts[section] = base + 1
            used_assets.add(asset_key)
            src = public_assets.get(asset_key) or public_assets.get(pool[0])
            video_src = motion_assets.get(asset_key) if USE_SVD_MOTION else None
            kind = "image"
            overlay = None
            if segment_index == 0 and section != last_section and section in SECTION_TEXT:
                overlay = SECTION_TEXT[section]
            if "allow negative" in scene["spoken_text"].lower() and segment_index == 0:
                kind = "code"
                overlay = ["ALLOW_NEGATIVE", "TRUE"]
            if "guilty." == scene["spoken_text"].lower().strip() and segment_index == 0:
                kind = "stamp"
                overlay = ["GUILTY"]
            if "it isn't" in scene["spoken_text"].lower() and "theft" in scene["spoken_text"].lower() and segment_index == 0:
                kind = "quote"
                overlay = ["IT ISN'T CRYPTO.", "IT'S THEFT."]
            shots.append(
                {
                    "id": f"SH-{len(shots) + 1:04d}",
                    "section": section,
                    "fromSec": round(seg_start, 3),
                    "durationSec": round(segment_dur, 3),
                    "src": src,
                    "videoSrc": video_src,
                    "kind": kind,
                    "overlay": overlay,
                }
            )
            last_asset = asset_key
        last_section = section
    content_end = float(timing["content_end_sec"])
    last_scene_end = max(float(scene["end"]) for scene in timing["scenes"])
    if content_end > last_scene_end + 0.2:
        ending_expansion_prefix = SECTION_EXPANSION_PREFIX.get("ending")
        ending_expansion = sorted(
            key for key in public_assets if ending_expansion_prefix and key.startswith(ending_expansion_prefix)
        )
        ending_pool = SECTION_ASSETS["ending"] + ending_expansion
        final_dur = content_end - last_scene_end
        final_count = max(1, math.ceil(final_dur / MAX_SHOT_SEC))
        final_segment_dur = final_dur / final_count
        for final_index in range(final_count):
            base = section_counts.get("ending", 0)
            ordered = ending_pool[base % len(ending_pool) :] + ending_pool[: base % len(ending_pool)]
            ending_key = next((key for key in ordered if key not in used_assets and key in public_assets), None)
            if ending_key is None:
                ending_key = next((key for key in ordered if key != last_asset and key in public_assets), ordered[0])
            section_counts["ending"] = base + 1
            used_assets.add(ending_key)
            shots.append(
                {
                    "id": f"SH-FINAL-HOLD-{final_index + 1:02d}",
                    "section": "ending",
                    "fromSec": round(last_scene_end + final_segment_dur * final_index, 3),
                    "durationSec": round(final_segment_dur, 3),
                    "src": public_assets.get(ending_key),
                    "videoSrc": motion_assets.get(ending_key) if USE_SVD_MOTION else None,
                    "kind": "image",
                    "overlay": ["AI RECONSTRUCTION", "DOCUMENTARY EXPLAINER"] if final_index == 0 else None,
                }
            )
            last_asset = ending_key
    endcard_start = content_end
    # final breath has already been included in content_end; fill the end region with recap if no narration.
    shots.append(
        {
            "id": "SH-ENDCARD",
            "section": "endcard",
            "fromSec": round(endcard_start, 3),
            "durationSec": 9.0,
            "src": None,
            "videoSrc": None,
            "kind": "endcard",
            "overlay": None,
        }
    )
    return shots


def main() -> int:
    assets = collect_assets()
    public_assets = {key: export_asset(path, re.sub(r"[^A-Za-z0-9_-]+", "_", key)) for key, path in assets.items()}
    motion_assets = export_motion_clips()
    timing = json.loads(TIMING.read_text(encoding="utf-8"))
    shots = make_shots(timing, public_assets, motion_assets)
    # Keep old channel bookend background available.
    src_banner = ROOT / "remotion" / "public" / "banner_sunrise.png"
    if src_banner.exists():
        shutil.copy2(src_banner, REMOTION_PUBLIC / "banner_sunrise.png")
    REMOTION_DATA.write_text(
        "// AUTO-GENERATED by scripts/prep_ftx_remotion_data.py\n"
        "export type FtxShot = {id: string; section: string; fromSec: number; durationSec: number; src: string | null; videoSrc: string | null; kind: string; overlay: string[] | null};\n"
        f"export const FTX_DURATION_SEC = {timing['total_with_endcard_sec']};\n"
        f"export const FTX_SHOTS: FtxShot[] = {json.dumps(shots, ensure_ascii=False, indent=2)};\n",
        encoding="utf-8",
    )
    print(f"assets={len(public_assets)} motion={len(motion_assets)} shots={len(shots)} -> {REMOTION_DATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
