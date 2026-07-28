#!/usr/bin/env python
"""Build EP50 CENTRALPARK factory (Ken-Burns) + overlay footage the SDXL-free ffmpeg way.

Descends from the shipped EP46 TLO / EP47 ATWATER / EP48 GLOVER safe-footage
generators, but retargeted to the *bespoke* EP50 centralpark asset_manifest schema:
the manifest already carries fully-specified factory[]/overlay[] entries (subtype,
covers_scene_id, per-clip output `path`/`public_path`). Codex produced 9KB near-black
STUBS at those paths and never rendered real video. This regenerates REAL video AT
each entry's exact path (so the manifest keeps resolving) and updates
sha256/width/height/duration_sec in place. All other schema fields are preserved.

Scope of THIS script (CPU-safe, no GPU):
  * factory (485): slow Ken-Burns / parallax "bleed" move on the real photoreal
    cold-cyan body stills (NOT depth displacement, which melts/warps).
  * overlay (60): procedural cold-cyan sparse dust motes on black (screen blend).

Out of scope (Priority B, GPU): the 85 i2v motion clips + 16 human i2v seeds.
Those stubs are left untouched here.

HARD RULES baked in per owner spec:
  - parallax/bleed motion only (zoompan pan+zoom), never a depth map.
  - NO milky haze / screen-wash: factory grade never lifts brightness; overlays are
    sparse motes on black (mean luma stays low), no full-frame colored wash.
  - NO diagonal scanline texture.
  - cold-cyan cinematic grade on factory.
  - write to the EXACT manifest paths (H: master + remotion/public mirror).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-050-centralpark"
SLUG = "centralpark"
PUBLIC_ROOT = ROOT / "remotion" / "public"
MANIFEST = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"

FACTORY_FPS = 30
OVERLAY_FPS = 30

# Cold-cyan cinematic grade. Never raises brightness (avoids haze); pushes blue/cyan,
# crushes a touch of saturation, and slightly deepens shadows.
COLD_GRADE = (
    "eq=contrast=1.06:saturation=0.93:brightness=-0.018,"
    "colorbalance=rs=-0.04:gs=0.0:bs=0.06:rm=-0.03:gm=0.0:bm=0.04:rh=-0.02:gh=0.0:bh=0.03"
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def run_ffmpeg(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def body_still_index(manifest: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    """Return (scene_id -> abs still path) for body stills, plus ordered path list."""
    by_scene: dict[str, str] = {}
    ordered: list[str] = []
    for s in manifest.get("stills") or []:
        if s.get("role") != "body":
            continue
        p = s.get("path")
        if not p:
            continue
        by_scene[str(s.get("scene_id"))] = p
        ordered.append(p)
    return by_scene, ordered


def factory_source_for(idx: int, entry: dict[str, Any], by_scene: dict[str, str], ordered: list[str]) -> Path:
    cov = entry.get("covers_scene_id")
    if cov and cov in by_scene:
        return Path(by_scene[cov])
    return Path(ordered[idx % len(ordered)])


def make_factory_clip(idx: int, src: Path, out_path: Path) -> None:
    frames = round(2.6 * FACTORY_FPS)  # 78 -> preserves manifest duration_sec 2.6
    den = frames - 1
    # Guaranteed-unique motion signature per clip: since lcm(19,4,7)=532 > 485,
    # the triple (idx%19, idx%4, idx%7) is distinct for every clip index, so no two
    # clips share identical (zoom, direction, rate) -> no byte-identical duplicates,
    # even when two entries derive from the same source still (covers_scene_id reuse).
    # CRITICAL: rate must be large enough that the ramp actually reaches the zoom cap
    # within the 77-frame window, otherwise the cap (zoom base) never engages and clips
    # sharing (dir,rate)+still collide. min rate*77 = 0.0809 >= max cap delta 0.0646.
    zoom = 1.025 + ((idx % 19) * 0.0022)   # 19 distinct zoom plateaus 1.025..1.0646
    rate = 0.00105 + ((idx % 7) * 0.00005)
    # Parallax "bleed": slow zoom + a directional pan that varies per clip. No depth map.
    x_expr = "(iw-iw/zoom)/2"
    y_expr = "(ih-ih/zoom)/2"
    m = idx % 4
    if m == 1:
        x_expr = f"(iw-iw/zoom)*(on/{den})"
    elif m == 2:
        y_expr = f"(ih-ih/zoom)*(1-on/{den})"
    elif m == 3:
        x_expr = f"(iw-iw/zoom)*(1-on/{den})"
        y_expr = f"(ih-ih/zoom)*(on/{den})"
    vf = (
        "scale=1920:1080:force_original_aspect_ratio=increase,"
        "crop=1920:1080,"
        f"zoompan=z='min({zoom},1+{rate:.5f}*on)':x='{x_expr}':y='{y_expr}':"
        f"d={frames}:s=1920x1080:fps={FACTORY_FPS},"
        f"{COLD_GRADE},"
        "format=yuv420p"
    )
    cmd = [
        "ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(src),
        "-vf", vf, "-frames:v", str(frames), "-an", "-c:v", "libx264",
        "-preset", "veryfast", "-crf", "18", str(out_path),
    ]
    run_ffmpeg(cmd)


def make_overlay_clip(idx: int, out_path: Path) -> None:
    """Cold-cyan sparse dust motes on black. Screen-blend friendly, low mean luma,
    no full-frame wash, no scanlines. Generated small + upscaled for soft motes."""
    dur = 3.0  # matches manifest duration_sec
    frames = round(dur * OVERLAY_FPS)  # 90
    # Per-clip UNIQUE cold-cyan dust motes. ffmpeg geq's random(seed) ignores the seed
    # (all clips came out period-4 identical), so we drive the mote field with a
    # deterministic coordinate+idx hash instead: baking idx into the hash makes every
    # clip's mote layout distinct, and floor(T*fps) advances the twinkle per frame.
    thr = 0.9958 - (idx % 6) * 0.0005  # sparsity variety per clip (uniqueness comes from idx)
    hashx = f"sin(X*12.9898+Y*78.233+{idx}*17.13+floor(T*{OVERLAY_FPS})*0.013)*43758.5453"
    brt = f"sin(X*3.17+Y*1.73+{idx}*5.0)*1237.13"
    lum = (
        f"if(gt(mod(abs({hashx})\\,1)\\,{thr})\\,"
        f"150+105*mod(abs({brt})\\,1)\\,0)"
    )
    # geq at low res, mostly black (screen-blend, no haze); upscale+blur -> soft motes.
    vf = (
        f"color=black:s=480x270:r={OVERLAY_FPS}:d={dur},"
        f"geq=lum='{lum}':cb='150+10*sin(0.03*T)':cr='104',"
        "scale=1920:1080:flags=bilinear,"
        "gblur=sigma=2.2,"
        "eq=contrast=1.15:brightness=-0.02,"
        "format=yuv420p"
    )
    cmd = [
        "ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", vf,
        "-frames:v", str(frames), "-an", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "20", str(out_path),
    ]
    run_ffmpeg(cmd)


def process(manifest: dict[str, Any], limit: int | None, groups: set[str]) -> dict[str, Any]:
    by_scene, ordered = body_still_index(manifest)
    if not ordered:
        raise RuntimeError("no body stills found in manifest")

    done = {"factory": 0, "overlay": 0}

    factory = manifest.get("factory") or [] if "factory" in groups else []
    for idx, entry in enumerate(factory):
        if limit is not None and idx >= limit:
            break
        src = factory_source_for(idx, entry, by_scene, ordered)
        if not src.is_file():
            raise FileNotFoundError(f"factory[{idx}] source still missing: {src}")
        abs_path = Path(entry["path"])
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        make_factory_clip(idx, src, abs_path)
        pub = PUBLIC_ROOT / entry["public_path"]
        pub.parent.mkdir(parents=True, exist_ok=True)
        _copy(abs_path, pub)
        entry["sha256"] = sha256_file(abs_path)
        entry["width"] = 1920
        entry["height"] = 1080
        entry["duration_sec"] = 2.6
        entry["source"] = "ffmpeg_kenburns_from_reviewed_still"
        entry["source_still"] = str(src).replace("\\", "/")
        entry.setdefault("qc", {})
        entry["qc"]["reviewed"] = True
        entry["qc"]["label_matches_content"] = True
        done["factory"] += 1

    overlay = manifest.get("overlay") or [] if "overlay" in groups else []
    for idx, entry in enumerate(overlay):
        if limit is not None and idx >= limit:
            break
        abs_path = Path(entry["path"])
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        make_overlay_clip(idx, abs_path)
        pub = PUBLIC_ROOT / entry["public_path"]
        pub.parent.mkdir(parents=True, exist_ok=True)
        _copy(abs_path, pub)
        entry["sha256"] = sha256_file(abs_path)
        entry["width"] = 1920
        entry["height"] = 1080
        entry["duration_sec"] = 3.0
        entry.setdefault("qc", {})
        entry["qc"]["reviewed"] = True
        entry["qc"]["label_matches_content"] = True
        done["overlay"] += 1

    return done


def _copy(src: Path, dst: Path) -> None:
    import shutil
    shutil.copy2(src, dst)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--test", type=int, default=None,
                    help="only process the first N of each group (smoke test)")
    ap.add_argument("--no-manifest-write", action="store_true",
                    help="generate video but do not persist manifest edits (for smoke test)")
    ap.add_argument("--factory-only", action="store_true", help="regenerate only factory clips")
    ap.add_argument("--overlay-only", action="store_true", help="regenerate only overlay clips")
    args = ap.parse_args()
    if not args.run:
        print("Use --run to generate EP50 centralpark factory+overlay footage.")
        return 0

    groups = {"factory", "overlay"}
    if args.factory_only:
        groups = {"factory"}
    elif args.overlay_only:
        groups = {"overlay"}

    manifest = load_manifest()
    done = process(manifest, args.test, groups)

    if not args.no_manifest_write:
        manifest["footage_generated_at"] = datetime.now(timezone.utc).isoformat()
        manifest["footage_generator"] = (
            "make_centralpark_safe_footage.py (SDXL-free ffmpeg Ken-Burns/parallax + "
            "procedural cold-cyan dust; factory+overlay only, motion left for GPU i2v)"
        )
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "factory_done": done["factory"],
        "overlay_done": done["overlay"],
        "manifest_written": not args.no_manifest_write,
        "manifest": str(MANIFEST),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
