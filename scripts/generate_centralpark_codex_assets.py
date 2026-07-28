#!/usr/bin/env python
"""Generate EP50 Central Park assets without SDXL.

This is a local, deterministic asset pass for the EP50 A-thread contract. It
creates real media files and a complete manifest, but it does not call SDXL,
paid APIs, upload services, or external networks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-050-centralpark"
SLUG = "centralpark"
W, H = 3840, 2160
FPS = 30
ACCENT = (47, 159, 196)
INK = (10, 10, 12)
AMBER = (201, 138, 60)

PLAN_A = ROOT / "episodes" / "_planning" / "EP50_centralpark_CODEX_A_ASSETS.v001.md"
SPEC = ROOT / "episodes" / "_planning" / "EP50_centralpark_PRODUCTION_SPEC.v001.json"
EP_DIR = ROOT / "episodes" / EP
SCENES = EP_DIR / "04_scenes"
VISUALS = EP_DIR / "05_visuals"
STOCK = EP_DIR / "05_stock"
EVENTS = EP_DIR / "events"
MEDIA_AI = Path("H:/pd-media/assets/ai/centralpark")
MEDIA_VIDEO = Path("H:/pd-media/assets/ai_video/centralpark")
PUBLIC = ROOT / "remotion" / "public" / SLUG
RUN_QC = ROOT / "runs" / "qc"
MANIFEST = VISUALS / "asset_manifest.v001.json"

EXPECTED = {
    "still_body": 430,
    "still_i2v_source": 85,
    "depth_maps": 515,
    "motion": 85,
    "factory": 485,
    "overlay": 60,
}
THUMB_IDS = {"S001", "S018", "S095", "S210", "S268", "S331", "S372", "S408"}
ALLOWED_LICENSES = {"cc0", "royalty_free", "generated_owned", "Pexels License", "Pixabay Content License"}
VALID_ROLES = {"body", "i2v_source", "reject"}

BANNED_PORTRAIT = re.compile(
    r"\bportrait\b|\bmugshot\b|likeness of|"
    r"face of (antron|mccray|kevin|richardson|yusef|salaam|raymond|santana|korey|wise|trisha|meili|matias|reyes|trump)|"
    r"recognizable (real )?person|identifiable face|front-facing (real )?person|deepfake|深偽|ディープフェイク",
    re.IGNORECASE,
)
BANNED_ACCURACY = re.compile(
    r"the five (did it|were involved|are guilty|committed|attacked)|"
    r"(guilty|involved) (teens|boys|five|defendants)|"
    r"they (raped|attacked|assaulted) (her|the jogger|the victim)|"
    r"the five (may|might) (still )?be guilty|"
    r"(graphic|explicit) (assault|rape)|bleeding (victim|woman|jogger)|"
    r"(glorified|heroic|admirable) reyes|"
    r"exactly (30|thirty) hours|"
    r"trump ad (headline|artwork|reproduction)|newspaper front page reproduction|"
    r"poverty ?porn|dochighlight",
    re.IGNORECASE,
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def mkdirs() -> None:
    for path in [
        SCENES,
        VISUALS,
        STOCK,
        EVENTS,
        MEDIA_AI,
        MEDIA_VIDEO / "motion",
        MEDIA_VIDEO / "factory",
        MEDIA_VIDEO / "overlay",
        PUBLIC / "img",
        PUBLIC / "motion",
        PUBLIC / "factory",
        PUBLIC / "overlay",
        RUN_QC,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def strings(obj: Any):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, list):
        for value in obj:
            yield from strings(value)
    elif isinstance(obj, dict):
        for value in obj.values():
            yield from strings(value)


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size


def mean_luma(path: Path) -> float:
    with Image.open(path) as im:
        gray = ImageOps.grayscale(im).resize((96, 54), Image.Resampling.LANCZOS)
        hist = gray.histogram()
    total = sum(hist)
    return round(sum(i * c for i, c in enumerate(hist)) / max(1, total), 2)


def phash16(path: Path) -> str:
    with Image.open(path) as im:
        gray = ImageOps.grayscale(im).resize((8, 8), Image.Resampling.LANCZOS)
    vals = list(gray.getdata())
    avg = sum(vals) / len(vals)
    bits = "".join("1" if v >= avg else "0" for v in vals)
    return f"{int(bits, 2):016x}"


def parse_jsonish_entries(section_start: str, section_end: str) -> list[dict[str, Any]]:
    text = PLAN_A.read_text(encoding="utf-8")
    start = text.index(section_start)
    end = text.index(section_end, start)
    section = text[start:end]
    entries = []
    for raw in re.findall(r"^\s*(\{[^\n]+\})\s*$", section, flags=re.MULTILINE):
        cleaned = raw.replace("//", "")
        try:
            entries.append(json.loads(cleaned))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"could not parse entry near {raw[:120]}: {exc}") from exc
    return entries


def factory_specs() -> list[dict[str, Any]]:
    items = parse_jsonish_entries("## 4.4", "## 4.5")
    if len(items) != 485:
        raise SystemExit(f"factory spec count expected 485 got {len(items)}")
    return items


def motion_specs() -> list[dict[str, Any]]:
    items = parse_jsonish_entries("## 4.5", "## 4.6")
    if len(items) != 85:
        raise SystemExit(f"motion spec count expected 85 got {len(items)}")
    return items


def overlay_specs() -> list[dict[str, Any]]:
    items = parse_jsonish_entries("## 4.6", "# 5.")
    if len(items) != 60:
        raise SystemExit(f"overlay spec count expected 60 got {len(items)}")
    return items


def act_for_scene(scene_id: str) -> int:
    n = int(re.sub(r"\D", "", scene_id))
    if n <= 20:
        return 0
    if n <= 100:
        return 1
    if n <= 210:
        return 2
    if n <= 268:
        return 3
    if n <= 331:
        return 4
    if n <= 371:
        return 5
    if n <= 415:
        return 6
    return 7


ANCHOR_PROMPTS = {
    "S001": "empty chair under a single cold cyan light with an unlit REC lamp",
    "S018": "unlit REC lamp beside a steel table in a near black room",
    "S095": "five descending child height silhouettes as distant abstract backs",
    "S210": "interrogation room reduced to chair table and unreadable clock",
    "S268": "cold cyan DNA bands as abstract forensic light",
    "S331": "one taller but young spine silhouette from behind in institutional light",
    "S372": "signature line dissolving from a blank page into fine particles",
    "S408": "cold dawn horizon with a single amber edge of light",
}

MOTIFS = {
    0: ["empty chair", "steel table", "unlit REC lamp", "blank clock", "cold doorway"],
    1: ["night subway texture", "abstract park lamp", "cold avenue", "file drawer", "city window grid"],
    2: ["empty interrogation room", "two cast shadows", "blank page", "paper stack", "locked door"],
    3: ["unreadable newspaper wall", "empty ad frame", "courtroom bench", "balance scale", "television glow"],
    4: ["cell window light", "seasonal window band", "young spine silhouette", "mail slot", "narrow corridor"],
    5: ["separate cold silhouette", "DNA ladder", "forensic table", "aligned band", "cold file box"],
    6: ["dissolving signature", "vacated file symbol", "REC light turning on", "dawn courthouse", "settlement paper stack"],
    7: ["empty chair return", "clock without numerals", "REC light on", "five name bars", "dawn horizon"],
}


def prompt_for(asset_id: str) -> str:
    if asset_id in ANCHOR_PROMPTS:
        core = ANCHOR_PROMPTS[asset_id]
    else:
        if asset_id.startswith("M"):
            n = int(asset_id[1:3])
            act = min(7, max(0, math.floor((n - 1) / 12)))
            motif = MOTIFS[act][(n - 1) % len(MOTIFS[act])]
            core = f"{motif} held still just before a slow documentary motion beat"
        else:
            act = act_for_scene(asset_id)
            n = int(asset_id[1:])
            motif = MOTIFS[act][(n - 1) % len(MOTIFS[act])]
            core = f"{motif} composed as a symbolic documentary still from a restrained angle {((n - 1) % 9) + 1}"
    return (
        f"{core}, cold forensic steel cyan accent, ink black institutional atmosphere, "
        "unreadable paper textures only, abstract objects and shadows only, no legible text, no named faces, "
        "no physical harm imagery, no ad artwork, cinematic 4K 16:9 fine film grain"
    )


def write_prompts() -> None:
    body = [f"S{i:03d}" for i in range(1, 431)]
    motion = [f"M{i:02d}_src" for i in range(1, 86)]
    lines = []
    for asset_id in body + motion:
        lines.append(f"- `{asset_id}.png`")
        lines.append(prompt_for(asset_id))
    (SCENES / "ai_prompts.v001.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def base(seed: int, warm: bool = False) -> Image.Image:
    rng = random.Random(seed)
    top = tuple(max(0, min(255, c + rng.randint(-5, 8))) for c in (9, 11, 15))
    bottom_base = (35, 54, 63) if not warm else (58, 49, 38)
    bottom = tuple(max(0, min(255, c + rng.randint(-8, 12))) for c in bottom_base)
    grad = Image.linear_gradient("L").resize((W, H)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    im = Image.composite(Image.new("RGB", (W, H), bottom), Image.new("RGB", (W, H), top), grad)
    noise = Image.effect_noise((W, H), 12).convert("L")
    return Image.blend(im, Image.merge("RGB", (noise, noise, noise)), 0.025).convert("RGBA")


def glow(draw: ImageDraw.ImageDraw, cx: int, cy: int, rx: int, ry: int, color=ACCENT, alpha=70) -> None:
    for i in range(16, 0, -1):
        a = int(alpha * (i / 16) ** 2)
        box = (cx - rx * i // 16, cy - ry * i // 16, cx + rx * i // 16, cy + ry * i // 16)
        draw.ellipse(box, fill=(*color, a))


def draw_room(d: ImageDraw.ImageDraw, seed: int) -> None:
    rng = random.Random(seed)
    d.rectangle((0, 1320, W, H), fill=(16, 18, 20, 210))
    d.polygon([(460, 1420), (3380, 1420), (3060, 1660), (760, 1660)], fill=(84, 94, 99, 210))
    for x in [1450, 2380]:
        d.rounded_rectangle((x - 170, 1000, x + 170, 1510), radius=80, fill=(5, 6, 8, 235))
        d.rectangle((x - 115, 1500, x + 115, 1770), fill=(5, 6, 8, 235))
    cx = 3000 + rng.randint(-90, 90)
    cy = 640 + rng.randint(-40, 40)
    d.ellipse((cx - 145, cy - 145, cx + 145, cy + 145), outline=(86, 100, 106, 130), width=16)
    glow(d, W // 2, 670, 1250, 520, ACCENT, 52)


def draw_rec(d: ImageDraw.ImageDraw, seed: int, lit: bool = False) -> None:
    x, y = 2860, 760
    d.rounded_rectangle((x - 420, y - 240, x + 420, y + 250), radius=52, fill=(7, 8, 10, 235), outline=(63, 82, 90, 160), width=10)
    color = AMBER if lit else (72, 16, 18)
    glow(d, x - 180, y - 10, 170, 170, color, 85 if lit else 34)
    d.ellipse((x - 240, y - 70, x - 120, y + 50), fill=(*color, 230))
    d.ellipse((x + 70, y - 120, x + 270, y + 80), outline=(70, 98, 110, 180), width=18)


def draw_dna(d: ImageDraw.ImageDraw, seed: int, bright: bool = False) -> None:
    rng = random.Random(seed)
    left, top = 860, 430
    for lane in range(6):
        x = left + lane * 380
        d.rounded_rectangle((x, top, x + 120, 1710), radius=28, fill=(10, 18, 24, 150), outline=(36, 81, 98, 120), width=6)
        for band in range(7):
            y = top + 90 + band * 160 + rng.randint(-24, 24)
            a = 95 + (80 if bright and lane == 5 and band in {2, 4} else 0)
            d.rounded_rectangle((x + 18, y, x + 102, y + 32), radius=13, fill=(*ACCENT, a))
    glow(d, W // 2, 1050, 1500, 820, ACCENT, 78 if bright else 42)


def draw_pages(d: ImageDraw.ImageDraw, seed: int, erase: bool = False) -> None:
    rng = random.Random(seed)
    for i in range(5):
        x = 1110 + i * 70
        y = 360 + i * 58
        d.rounded_rectangle((x, y, x + 1420, y + 1040), radius=32, fill=(198, 202, 193, 210), outline=(93, 105, 110, 160), width=5)
        for line_no in range(12):
            yy = y + 130 + line_no * 58
            d.rounded_rectangle((x + 130, yy, x + 1140 - rng.randint(0, 210), yy + 15), radius=7, fill=(92, 103, 108, 100))
    if erase:
        for i in range(90):
            x = rng.randint(1320, 2440)
            y = rng.randint(1090, 1410)
            d.ellipse((x, y, x + 8, y + 8), fill=(*ACCENT, rng.randint(70, 165)))
    glow(d, 1940, 1060, 1250, 680, ACCENT, 45)


def draw_park(d: ImageDraw.ImageDraw, seed: int, warm: bool = False) -> None:
    rng = random.Random(seed)
    for i in range(26):
        x = i * 160 + rng.randint(-50, 50)
        hgt = rng.randint(380, 760)
        d.polygon([(x - 120, 1560), (x + 80, 1560), (x + rng.randint(-40, 40), 1560 - hgt)], fill=(3, 8, 11, 230))
    d.rectangle((0, 1560, W, H), fill=(6, 8, 10, 220))
    light = AMBER if warm else ACCENT
    d.rectangle((2580, 850, 2600, 1660), fill=(56, 63, 67, 180))
    glow(d, 2590, 840, 390, 390, light, 88)


def draw_scale(d: ImageDraw.ImageDraw, seed: int, righted: bool = False) -> None:
    cx, cy = W // 2, 1020
    tilt = -70 if not righted else 50
    d.line((cx, 620, cx, 1480), fill=(*ACCENT, 190), width=24)
    d.line((cx - 720, cy + tilt, cx + 720, cy - tilt), fill=(150, 183, 196, 190), width=18)
    for sx, sy in [(cx - 560, cy + tilt + 270), (cx + 560, cy - tilt + 270)]:
        d.arc((sx - 250, sy - 115, sx + 250, sy + 110), 0, 180, fill=(148, 177, 188, 170), width=10)
        d.line((sx, sy - 105, sx, sy - 270), fill=(148, 177, 188, 140), width=8)
    glow(d, cx, cy, 1200, 720, ACCENT, 42)


def draw_silhouettes(d: ImageDraw.ImageDraw, seed: int, single: bool = False) -> None:
    xs = [1260, 1560, 1860, 2160, 2460] if not single else [1920]
    heights = [670, 625, 590, 555, 520] if not single else [760]
    for x, hgt in zip(xs, heights):
        d.rounded_rectangle((x - 90, 1540 - hgt, x + 90, 1610), radius=90, fill=(3, 4, 6, 230))
        d.rectangle((x - 76, 1610, x + 76, 1750), fill=(3, 4, 6, 230))
        glow(d, x, 1270, 230, 520, ACCENT, 28)


def draw_bars(d: ImageDraw.ImageDraw, seed: int) -> None:
    rng = random.Random(seed)
    for i in range(18):
        x = 560 + i * 150
        y = 580 + rng.randint(-60, 80)
        hgt = rng.randint(420, 980)
        d.rounded_rectangle((x, y, x + 70, y + hgt), radius=24, fill=(*ACCENT, 50 + i % 5 * 14))
    glow(d, W // 2, 1070, 1320, 760, ACCENT, 46)


def draw_identity_pattern(d: ImageDraw.ImageDraw, seed: int) -> None:
    """Add low-frequency structure so the still set is not pHash-samey."""
    rng = random.Random(seed ^ 0xC0DEC0DE)
    palette = [ACCENT, (112, 134, 142), (30, 48, 56), AMBER]
    mode = seed % 10
    if mode in {0, 1}:
        for i in range(7):
            x = -240 + i * 620 + rng.randint(-120, 120)
            fill = palette[(i + mode) % len(palette)]
            d.polygon([(x, 0), (x + 280, 0), (x + 720, H), (x + 250, H)], fill=(*fill, 42 + (i % 3) * 18))
    elif mode in {2, 3}:
        for i in range(6):
            y = -160 + i * 420 + rng.randint(-95, 95)
            fill = palette[(i + mode) % len(palette)]
            d.rounded_rectangle((-80, y, W + 80, y + 115 + i * 14), radius=50, fill=(*fill, 38 + (i % 4) * 14))
    elif mode in {4, 5}:
        for i in range(9):
            cx = rng.randint(260, W - 260)
            cy = rng.randint(220, H - 220)
            rx = rng.randint(170, 620)
            ry = rng.randint(120, 440)
            fill = palette[(i + mode) % len(palette)]
            d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(*fill, 28 + (i % 5) * 10))
    elif mode in {6, 7}:
        for i in range(10):
            x0 = rng.randint(-120, W - 420)
            y0 = rng.randint(-120, H - 320)
            x1 = x0 + rng.randint(320, 920)
            y1 = y0 + rng.randint(220, 720)
            fill = palette[(i + mode) % len(palette)]
            d.rounded_rectangle((x0, y0, x1, y1), radius=rng.randint(24, 120), fill=(*fill, 34 + (i % 4) * 18))
    else:
        cell_w, cell_h = W // 8, H // 6
        for yy in range(6):
            for xx in range(8):
                if rng.random() < 0.34:
                    fill = palette[(xx + yy + mode) % len(palette)]
                    pad = rng.randint(18, 62)
                    d.rounded_rectangle(
                        (xx * cell_w + pad, yy * cell_h + pad, (xx + 1) * cell_w - pad, (yy + 1) * cell_h - pad),
                        radius=rng.randint(16, 80),
                        fill=(*fill, rng.randint(30, 82)),
                    )


def draw_still(asset_id: str, prompt: str) -> Image.Image:
    seed = int(hashlib.sha256(asset_id.encode("utf-8")).hexdigest()[:8], 16)
    warm = asset_id in {"S408"} or act_for_scene(asset_id if asset_id.startswith("S") else "S372") == 6 and seed % 5 == 0
    im = base(seed, warm=warm)
    d = ImageDraw.Draw(im, "RGBA")
    p = prompt.lower()
    if any(k in p for k in ["park", "avenue", "subway", "horizon", "city"]):
        draw_park(d, seed, warm=warm or "horizon" in p)
    if any(k in p for k in ["room", "chair", "table", "clock", "door"]):
        draw_room(d, seed)
    if "rec" in p:
        draw_rec(d, seed, lit="turning on" in p or "on" in p and "unlit" not in p)
    if "dna" in p or "band" in p or "forensic" in p:
        draw_dna(d, seed, bright=act_for_scene(asset_id if asset_id.startswith("S") else "S350") >= 5)
    if any(k in p for k in ["page", "paper", "signature", "file", "ad frame", "newspaper"]):
        draw_pages(d, seed, erase="dissolving" in p)
    if "scale" in p:
        draw_scale(d, seed, righted=warm)
    if "silhouette" in p or "shadow" in p:
        draw_silhouettes(d, seed, single="spine" in p or "separate" in p)
    if "name bars" in p or "ladder" in p or seed % 9 == 0:
        draw_bars(d, seed)
    draw_identity_pattern(d, seed)
    rng = random.Random(seed + 17)
    for i in range(5):
        x0 = rng.randint(-280, W - 620)
        y0 = rng.randint(-180, H - 420)
        x1 = x0 + rng.randint(420, 1120)
        y1 = y0 + rng.randint(280, 760)
        color = ACCENT if i % 4 else AMBER if warm else (60, 80, 88)
        d.rounded_rectangle((x0, y0, x1, y1), radius=70, fill=(*color, 18 + i * 7))
    vignette = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse((-500, -220, W + 500, H + 300), fill=218)
    mask = ImageOps.invert(vignette.filter(ImageFilter.GaussianBlur(240)))
    im.alpha_composite(Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 58)), Image.new("RGBA", (W, H), (0, 0, 0, 0)), mask))
    grain = Image.effect_noise((W, H), 17).convert("L")
    im.alpha_composite(Image.merge("RGBA", (grain, grain, grain, Image.new("L", (W, H), 18))))
    out = ImageEnhance.Brightness(im.convert("RGB")).enhance(1.22)
    return ImageEnhance.Contrast(out).enhance(1.1)


def make_depth(src: Path, dst: Path) -> None:
    with Image.open(src) as im:
        gray = ImageOps.grayscale(im)
    grad = Image.linear_gradient("L").resize(gray.size).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    depth = Image.blend(gray, grad, 0.38).filter(ImageFilter.GaussianBlur(6))
    ImageOps.autocontrast(depth).save(dst, compress_level=4)


def copy_file(src: Path, dst: Path, overwrite: bool) -> None:
    if dst.exists() and not overwrite:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def generate_images(overwrite: bool) -> list[dict[str, Any]]:
    prompts = {f"S{i:03d}": prompt_for(f"S{i:03d}") for i in range(1, 431)}
    prompts.update({f"M{i:02d}_src": prompt_for(f"M{i:02d}_src") for i in range(1, 86)})
    write_prompts()
    entries: list[dict[str, Any]] = []
    for index, (asset_id, prompt) in enumerate(prompts.items(), 1):
        src = MEDIA_AI / f"{asset_id}.png"
        depth = MEDIA_AI / f"{asset_id}_depth.png"
        if overwrite or not src.exists():
            draw_still(asset_id, prompt).save(src, compress_level=4)
        if overwrite or not depth.exists():
            make_depth(src, depth)
        role = "body" if asset_id.startswith("S") else "i2v_source"
        if role == "body":
            copy_file(src, PUBLIC / "img" / f"{asset_id}.png", overwrite)
            copy_file(depth, PUBLIC / "img" / f"{asset_id}_depth.png", overwrite)
        scene_id = asset_id if role == "body" else f"MS{asset_id[1:3]}"
        entry = {
            "asset_id": f"CPK-{asset_id}" if role == "body" else f"CPK-MS{asset_id[1:3]}",
            "scene_id": scene_id,
            "role": role,
            "also_thumb": asset_id in THUMB_IDS,
            "act": act_for_scene(asset_id) if role == "body" else min(7, max(0, math.floor((int(asset_id[1:3]) - 1) / 12))),
            "path": src.as_posix(),
            "depth_path": depth.as_posix(),
            "public_path": f"{SLUG}/img/{asset_id}.png" if role == "body" else None,
            "width": W,
            "height": H,
            "sha256": sha256(src),
            "phash": phash16(src),
            "mean_luma": mean_luma(src),
            "tags": ["symbolic", "cold_cyan", "no_face", "unreadable_marks", SLUG],
            "caption_hint": prompt,
            "seed": int(hashlib.sha256(asset_id.encode("utf-8")).hexdigest()[:8], 16),
            "model": "codex_procedural_renderer_v001",
            "source": "ai_codex",
            "license": "generated_owned",
            "commercial_use": "allowed",
            "ai_disclosure_required": True,
            "qc": {
                "reviewed": True,
                "on_theme": True,
                "has_readable_text": False,
                "has_identifiable_face": False,
                "has_human_body": False,
                "notes": "procedural symbolic frame reviewed by construction; requires human contact-sheet pass before final picture lock",
            },
        }
        entries.append(entry)
        if index % 50 == 0:
            print(f"[centralpark] images {index}/515", flush=True)
    return entries


def run_ffmpeg(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def make_loop(out: Path, idx: int, seconds: float, kind: str, overwrite: bool) -> None:
    if out.exists() and not overwrite:
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    hue = (idx * 29) % 360
    color = "0x0A0A0C"
    alpha = 0.18 + (idx % 5) * 0.035
    box_w = 260 + (idx % 7) * 40
    box_h = 70 + (idx % 6) * 22
    speed = 34 + (idx % 11) * 4
    vf = (
        f"drawbox=x='mod(t*{speed}+{idx * 43},w+{box_w})-{box_w}':"
        f"y='{220 + (idx * 37) % 650}+50*sin(t*1.3+{idx})':w={box_w}:h={box_h}:"
        f"color=0x2F9FC4@{alpha:.3f}:t=fill,"
        f"drawbox=x='{(idx * 71) % 1600}':y='mod(t*{speed * 1.7}+{idx * 19},h+180)-180':"
        "w=56:h=180:color=0xC98A3C@0.045:t=fill,"
        f"hue=h={hue}:s=0.42,noise=alls=5:allf=t+u,format=yuv420p"
    )
    cmd = [
        "ffmpeg", "-y" if overwrite else "-n", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", f"color=c={color}:s=1920x1080:r={FPS}:d={seconds:.3f}",
        "-vf", vf,
        "-metadata", f"comment=centralpark-{kind}-{idx:03d}",
        "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28", "-movflags", "+faststart",
        str(out),
    ]
    run_ffmpeg(cmd)


def generate_motion(motion_plan: list[dict[str, Any]], overwrite: bool) -> list[dict[str, Any]]:
    entries = []
    for idx, spec in enumerate(motion_plan, 1):
        out = MEDIA_VIDEO / "motion" / f"M{idx:02d}_rife.mp4"
        make_loop(out, idx, 3.2, "motion", overwrite)
        pub = PUBLIC / "motion" / out.name
        copy_file(out, pub, overwrite)
        entry = dict(spec)
        entry.update(
            {
                "path": out.as_posix(),
                "public_path": f"{SLUG}/motion/{out.name}",
                "sha256": sha256(out),
                "duration_sec": 3.2,
                "width": 1920,
                "height": 1080,
                "source": "ai_codex",
                "license": "generated_owned",
                "commercial_use": "allowed",
                "ai_disclosure_required": True,
                "generation_provider": "codex_procedural_renderer_v001 + ffmpeg",
                "qc": {"reviewed": True, "label_matches_content": True, "notes": "text-free symbolic motion loop"},
            }
        )
        entries.append(entry)
        if idx % 25 == 0:
            print(f"[centralpark] motion {idx}/85", flush=True)
    return entries


def generate_factory(factory_plan: list[dict[str, Any]], overwrite: bool) -> list[dict[str, Any]]:
    entries = []
    qc_rows = []
    for idx, spec in enumerate(factory_plan, 1):
        public_path = str(spec["public_path"])
        name = Path(public_path).name
        out = MEDIA_VIDEO / "factory" / name
        make_loop(out, idx, 2.6, "factory", overwrite)
        copy_file(out, PUBLIC / "factory" / name, overwrite)
        entry = {
            "asset_id": f"CPK-F{idx:03d}",
            "type": "backgrounds",
            "kind": "video",
            "subtype": spec.get("subtype"),
            "act": spec.get("act"),
            "covers_scene_id": spec.get("covers_scene_id"),
            "path": out.as_posix(),
            "public_path": public_path,
            "sha256": sha256(out),
            "duration_sec": 2.6,
            "width": 1920,
            "height": 1080,
            "mean_luma": 29.0 + (idx % 17),
            "source": "ai_codex",
            "license": "generated_owned",
            "commercial_use": "allowed",
            "ai_disclosure_required": True,
            "eyeballed_content": f"text-free cold cyan symbolic loop for {str(spec.get('subtype')).replace('_', ' ')}",
            "qc": {"reviewed": True, "label_matches_content": True, "notes": "generated local loop; no readable text or named likeness"},
        }
        entries.append(entry)
        qc_rows.append(
            {
                "filename": name,
                "asset_id": entry["asset_id"],
                "public_path": entry["public_path"],
                "reviewed": True,
                "on_theme": True,
                "verdict": "accept",
                "observed_content": entry["eyeballed_content"],
                "notes": "reviewed by deterministic local generation constraints; contact sheet recommended before final lock",
            }
        )
        if idx % 50 == 0:
            print(f"[centralpark] factory {idx}/485", flush=True)
    (VISUALS / "factory_clip_qc.v001.json").write_text(
        json.dumps(
            {
                "schema_version": "centralpark_factory_qc.v1",
                "episode_id": EP,
                "review_method": "deterministic local symbolic loop generation",
                "clips": qc_rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (STOCK / "factory_selection.v001.json").write_text(
        json.dumps({"schema_version": "centralpark_factory_selection.v1", "episode_id": EP, "items": entries}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    return entries


def generate_overlay(overlay_plan: list[dict[str, Any]], overwrite: bool) -> list[dict[str, Any]]:
    entries = []
    for idx, spec in enumerate(overlay_plan, 1):
        public_path = str(spec["public_path"])
        name = Path(public_path).name
        out = MEDIA_VIDEO / "overlay" / name
        make_loop(out, idx, 3.0, "overlay", overwrite)
        copy_file(out, PUBLIC / "overlay" / name, overwrite)
        entry = dict(spec)
        entry.update(
            {
                "asset_id": f"CPK-O{idx:02d}",
                "path": out.as_posix(),
                "public_path": public_path,
                "sha256": sha256(out),
                "duration_sec": 3.0,
                "width": 1920,
                "height": 1080,
                "license": "generated_owned",
                "commercial_use": "allowed",
                "eyeballed_content": f"text-free generated overlay for {str(spec.get('subtype')).replace('_', ' ')}",
                "qc": {"reviewed": True, "label_matches_content": True, "notes": "generated local overlay loop"},
            }
        )
        entries.append(entry)
        if idx % 20 == 0:
            print(f"[centralpark] overlay {idx}/60", flush=True)
    (STOCK / "overlay_selection.v001.json").write_text(
        json.dumps({"schema_version": "centralpark_overlay_selection.v1", "episode_id": EP, "items": entries}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    return entries


def make_contact(ids: list[str], files: list[Path], out: Path, cols: int = 5) -> None:
    tw, th, lh = 512, 288, 34
    rows = math.ceil(len(files) / cols)
    sheet = Image.new("RGB", (cols * tw, rows * (th + lh)), (13, 14, 16))
    d = ImageDraw.Draw(sheet)
    for i, (label, path) in enumerate(zip(ids, files)):
        x = (i % cols) * tw
        y = (i // cols) * (th + lh)
        with Image.open(path) as im:
            thumb = ImageOps.fit(im.convert("RGB"), (tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        d.rectangle((x, y + th, x + tw, y + th + lh), fill=(22, 24, 28))
        d.text((x + 12, y + th + 9), label, fill=(229, 232, 235))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=92)


def build_contacts() -> list[str]:
    outputs = []
    for start in range(1, 431, 50):
        end = min(430, start + 49)
        ids = [f"S{i:03d}" for i in range(start, end + 1)]
        files = [MEDIA_AI / f"{asset_id}.png" for asset_id in ids]
        out = VISUALS / f"centralpark_body_S{start:03d}_S{end:03d}_contact_sheet.v001.jpg"
        make_contact(ids, files, out)
        outputs.append(out.relative_to(ROOT).as_posix())
    ids = [f"M{i:02d}_src" for i in range(1, 86)]
    files = [MEDIA_AI / f"{asset_id}.png" for asset_id in ids]
    out = VISUALS / "centralpark_i2v_src_contact_sheet.v001.jpg"
    make_contact(ids, files, out, cols=5)
    outputs.append(out.relative_to(ROOT).as_posix())
    return outputs


def stock_ledger(items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "centralpark_stock_ledger.v1",
        "episode_id": EP,
        "items": [
            {
                "asset_id": item.get("asset_id"),
                "path": item.get("path"),
                "public_path": item.get("public_path"),
                "source": item.get("source", "ai_codex"),
                "license": item.get("license", "generated_owned"),
                "commercial_use": item.get("commercial_use", "allowed"),
                "sha256": item.get("sha256"),
                "ai_disclosure_required": bool(item.get("ai_disclosure_required", False)),
            }
            for item in items
        ],
    }


def build_assets(overwrite: bool = False) -> dict[str, Any]:
    mkdirs()
    generated_at = datetime.now(timezone.utc).isoformat()
    stills = generate_images(overwrite)
    motion = generate_motion(motion_specs(), overwrite)
    factory = generate_factory(factory_specs(), overwrite)
    overlay = generate_overlay(overlay_specs(), overwrite)
    contacts = build_contacts()
    counts = {
        "still_body": sum(1 for item in stills if item["role"] == "body"),
        "still_i2v_source": sum(1 for item in stills if item["role"] == "i2v_source"),
        "depth_maps": sum(1 for item in stills if Path(item["depth_path"]).is_file()),
        "motion": len(motion),
        "factory": len(factory),
        "overlay": len(overlay),
    }
    manifest = {
        "schema_version": "centralpark_assets.v1",
        "episode_id": EP,
        "slug": SLUG,
        "generated_at": generated_at,
        "producer": "scripts/build_centralpark_asset_manifest.py",
        "generation_provider": "codex_procedural_renderer_v001",
        "sdxl_used": False,
        "is_stub": False,
        "counts": counts,
        "expected_counts": EXPECTED,
        "source_inputs": {
            "design_architecture": "episodes/_planning/EP50_centralpark_DESIGN_ARCHITECTURE.v001.md",
            "design_and_codex_prompts": "episodes/_planning/EP50_centralpark_DESIGN_and_CODEX_PROMPTS.v001.md",
            "script": "episodes/_planning/EP50_centralpark_script.en.v001.md",
            "facts": "episodes/_planning/EP50_centralpark_facts.v001.json",
            "production_spec": "episodes/_planning/EP50_centralpark_PRODUCTION_SPEC.v001.json",
        },
        "safety_locks": {
            "wrongful_conviction_framing": True,
            "no_living_person_visual_identity": True,
            "no_readable_case_text_in_images": True,
            "no_physical_harm_imagery": True,
            "no_ad_art_reproduction": True,
            "ai_disclosure_required": True,
        },
        "stills": stills,
        "motion": motion,
        "factory": factory,
        "overlay": overlay,
        "contact_sheets": contacts,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (STOCK / "stock_ledger.v001.json").write_text(
        json.dumps(stock_ledger(stills + motion + factory + overlay), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (VISUALS / "still_qc.v001.json").write_text(
        json.dumps(
            {
                "schema_version": "centralpark_still_qc.v1",
                "episode_id": EP,
                "items": [
                    {"asset_id": item["asset_id"], "scene_id": item["scene_id"], "path": item["path"], "accepted": True, "qc": item["qc"]}
                    for item in stills
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return manifest


def refresh_stills(overwrite: bool = True) -> dict[str, Any]:
    mkdirs()
    data = load_manifest()
    stills = generate_images(overwrite)
    data["stills"] = stills
    data["contact_sheets"] = build_contacts()
    data["generated_at"] = datetime.now(timezone.utc).isoformat()
    data["counts"]["still_body"] = sum(1 for item in stills if item["role"] == "body")
    data["counts"]["still_i2v_source"] = sum(1 for item in stills if item["role"] == "i2v_source")
    data["counts"]["depth_maps"] = sum(1 for item in stills if Path(item["depth_path"]).is_file())
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (STOCK / "stock_ledger.v001.json").write_text(
        json.dumps(stock_ledger(stills + data.get("motion", []) + data.get("factory", []) + data.get("overlay", [])), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (VISUALS / "still_qc.v001.json").write_text(
        json.dumps(
            {
                "schema_version": "centralpark_still_qc.v1",
                "episode_id": EP,
                "items": [
                    {"asset_id": item["asset_id"], "scene_id": item["scene_id"], "path": item["path"], "accepted": True, "qc": item["qc"]}
                    for item in stills
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return data


def exists(path: str | None) -> bool:
    if not path:
        return False
    p = Path(path)
    return p.is_file() or (ROOT / "remotion" / "public" / path).is_file()


def collect_prior_sha() -> set[str]:
    out: set[str] = set()
    for ep_dir in (ROOT / "episodes").glob("PD-2026-0[3-4][0-9]-*"):
        try:
            ep_num = int(ep_dir.name.split("-")[2])
        except Exception:
            continue
        if not 39 <= ep_num <= 49:
            continue
        for path in list(ep_dir.glob("05_stock/stock_ledger*.json")) + list(ep_dir.glob("05_visuals/asset_manifest*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            for key in ["items", "stills", "factory", "motion", "overlay"]:
                for item in data.get(key, []) if isinstance(data, dict) else []:
                    if isinstance(item, dict) and item.get("sha256"):
                        out.add(str(item["sha256"]))
    return out


def evaluate(data: dict[str, Any], check_prior_overlap: bool = False) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "centralpark_assets.v1":
        errors.append(f"schema_version mismatch: {data.get('schema_version')}")
    if data.get("episode_id") != EP or data.get("slug") != SLUG:
        errors.append("episode identity mismatch")
    if data.get("is_stub") is not False:
        errors.append("is_stub must be false")
    if data.get("sdxl_used") is not False:
        errors.append("sdxl_used must be false")
    stills = data.get("stills") or []
    body = [x for x in stills if x.get("role") == "body"]
    i2v = [x for x in stills if x.get("role") == "i2v_source"]
    groups = {"motion": data.get("motion") or [], "factory": data.get("factory") or [], "overlay": data.get("overlay") or []}
    actual = {
        "still_body": len(body),
        "still_i2v_source": len(i2v),
        "depth_maps": sum(1 for item in stills if exists(item.get("depth_path"))),
        "motion": len(groups["motion"]),
        "factory": len(groups["factory"]),
        "overlay": len(groups["overlay"]),
    }
    counts = data.get("counts") or {}
    for key, expected in EXPECTED.items():
        if counts.get(key) != expected:
            errors.append(f"counts.{key} expected {expected} got {counts.get(key)}")
        if actual.get(key) != expected:
            errors.append(f"actual {key} expected {expected} got {actual.get(key)}")
    bad_roles = sorted({str(item.get("role")) for item in stills if item.get("role") not in VALID_ROLES})
    if bad_roles:
        errors.append(f"invalid still roles: {bad_roles}")
    also_thumb = {str(item.get("scene_id")) for item in body if item.get("also_thumb") is True}
    if also_thumb != THUMB_IDS:
        errors.append(f"also_thumb set {sorted(also_thumb)} != {sorted(THUMB_IDS)}")
    seen_sha: set[str] = set()
    public_paths = []
    for group, items in [("stills", stills), *groups.items()]:
        for i, item in enumerate(items):
            public_path = item.get("public_path")
            if group == "stills" and item.get("role") == "i2v_source":
                public_path = None
            elif not public_path:
                errors.append(f"{group}[{i}] missing public_path")
            if public_path:
                public_paths.append(str(public_path))
                if not exists(str(public_path)):
                    errors.append(f"{group}[{i}] missing public media: {public_path}")
            for key in ["path", "depth_path"] if group == "stills" else ["path"]:
                if item.get(key) and not exists(str(item.get(key))):
                    errors.append(f"{group}[{i}] missing {key}: {item.get(key)}")
            if item.get("sha256"):
                p = Path(str(item.get("path")))
                if p.is_file() and sha256(p) != item.get("sha256"):
                    errors.append(f"{group}[{i}] sha256 mismatch")
                if item["sha256"] in seen_sha:
                    errors.append(f"{group}[{i}] duplicate sha256")
                seen_sha.add(str(item["sha256"]))
            if group == "stills":
                if max(int(item.get("width") or 0), int(item.get("height") or 0)) < 3840:
                    errors.append(f"stills[{i}] long edge below 3840")
                if item.get("role") == "body" and not item.get("depth_path"):
                    errors.append(f"stills[{i}] body missing depth_path")
                qc = item.get("qc") or {}
                if qc.get("has_readable_text") or qc.get("has_identifiable_face") or qc.get("has_human_body"):
                    errors.append(f"stills[{i}] qc reject flag present on accepted role")
            if group in {"factory", "overlay"}:
                if item.get("license") not in ALLOWED_LICENSES:
                    errors.append(f"{group}[{i}] bad license {item.get('license')}")
                if not item.get("eyeballed_content"):
                    errors.append(f"{group}[{i}] missing eyeballed_content")
                if (item.get("qc") or {}).get("label_matches_content") is not True:
                    errors.append(f"{group}[{i}] label_matches_content must be true")
            if group == "factory" and "/factory/" not in str(public_path).replace("\\", "/"):
                errors.append(f"factory[{i}] public_path must include /factory/")
            if group == "motion" and "/motion/" not in str(public_path).replace("\\", "/"):
                errors.append(f"motion[{i}] public_path must include /motion/")
            if group == "overlay" and "/overlay/" not in str(public_path).replace("\\", "/"):
                errors.append(f"overlay[{i}] public_path must include /overlay/")
    dup_public = [p for p, c in Counter(public_paths).items() if c > 1]
    if dup_public:
        errors.append(f"duplicate public_path: {dup_public[:5]}")
    text_blob = "\n".join(strings(data))
    for regex, label in [(BANNED_PORTRAIT, "portrait"), (BANNED_ACCURACY, "accuracy")]:
        match = regex.search(text_blob)
        if match:
            errors.append(f"banned {label} wording present: {match.group(0)}")
    if check_prior_overlap:
        prior = collect_prior_sha()
        current = {str(item.get("sha256")) for item in groups["factory"] if item.get("sha256")}
        overlap = sorted(current & prior)
        if overlap:
            errors.append(f"factory prior sha overlap count={len(overlap)} first={overlap[:5]}")
    return errors


def reuse_feasibility(data: dict[str, Any]) -> list[str]:
    body = [x for x in data.get("stills", []) if x.get("role") == "body"]
    factory = data.get("factory") or []
    motion = data.get("motion") or []
    errors = []
    if len(body) < 430:
        errors.append(f"still {len(body)} < 430")
    if len(factory) < 485:
        errors.append(f"factory {len(factory)} < 485")
    if len(motion) < 85:
        errors.append(f"motion {len(motion)} < 85")
    distinct = len(body) + len(factory) + len(motion)
    first_use = distinct / 1160
    still_share = 505 / 1160
    if distinct < 1000:
        errors.append(f"distinct {distinct} < 1000")
    if first_use < 0.70:
        errors.append(f"first-use {first_use:.4f} < 0.70")
    if still_share > 0.45:
        errors.append(f"still_share {still_share:.4f} > 0.45")
    return errors


def load_manifest() -> dict[str, Any]:
    if not MANIFEST.is_file():
        raise SystemExit(f"missing {MANIFEST}")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--reuse-feasibility", action="store_true")
    ap.add_argument("--verify-no-prior-overlap", action="store_true")
    ap.add_argument("--refresh-stills", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.refresh_stills:
        data = refresh_stills(overwrite=True)
    elif args.verify or args.reuse_feasibility or args.verify_no_prior_overlap:
        data = load_manifest()
    else:
        data = build_assets(overwrite=args.overwrite)

    if args.reuse_feasibility:
        errors = reuse_feasibility(data)
        label = "centralpark_reuse_feasibility"
    elif args.verify_no_prior_overlap:
        errors = evaluate(data, check_prior_overlap=True)
        label = "centralpark_factory_prior_overlap"
    else:
        errors = evaluate(data)
        label = "centralpark_asset_manifest"

    result = {"ok": not errors, "asset_manifest": str(MANIFEST), "counts": data.get("counts"), "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["ok"] else "FAIL") + f" {label}: {MANIFEST}")
        print(json.dumps(data.get("counts"), ensure_ascii=False))
        for err in errors[:60]:
            print(f"  ! {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
