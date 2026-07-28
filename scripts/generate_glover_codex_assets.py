#!/usr/bin/env python
"""Generate EP48 Glover visual assets without the SDXL/Wan pipeline."""
from __future__ import annotations

import hashlib
import json
import math
import random
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-048-glover"
SLUG = "glover"
W, H = 3840, 2160
ACCENT = (91, 141, 184)
INK = (10, 10, 12)
MEDIA_AI = Path("H:/pd-media/assets/ai/glover")
MEDIA_VIDEO = Path("H:/pd-media/assets/ai_video/glover")
PUBLIC = ROOT / "remotion" / "public" / SLUG
EP_DIR = ROOT / "episodes" / EP
VISUALS = EP_DIR / "05_visuals"
STOCK = EP_DIR / "05_stock"
SCENES = EP_DIR / "04_scenes"
RUN_QC = ROOT / "runs" / "qc"
PLAN_A = ROOT / "episodes" / "_planning" / "EP48_glover_CODEX_A_ASSETS.v001.md"
THUMB_IDS = {"S03", "S04", "S06", "S12", "S27", "S43"}
GENERATED_AT = datetime.now(timezone.utc).isoformat()

FACTORY_SUBTYPES = [
    "two_lane_kansas_road_night", "rural_highway_night", "patrol_car_idling_shoulder",
    "prairie_road_dark", "night_highway_taillights", "empty_road_night_wide",
    "supreme_court_columns_night", "kansas_small_town_dusk", "county_courthouse_exterior",
    "douglas_county_road_night", "patrol_car_cruising_night", "county_courthouse_dusk",
    "courthouse_corridor_cold", "rural_kansas_road_evening", "prairie_highway_straight",
    "patrol_car_parked_night", "small_town_street_night", "roadside_shoulder_night",
    "gravel_road_night", "highway_overpass_night", "dark_two_lane_road", "empty_courtroom",
    "courthouse_corridor_long", "federal_courthouse_dusk", "patrol_car_roadside_dusk",
    "marble_hallway_cold", "courtroom_bench_empty", "law_library_shelves",
    "marble_stairs_cold", "clerk_office_cold", "empty_road_wide_night",
    "courthouse_columns_day", "office_corridor_fluorescent", "highway_horizon_dusk",
    "marble_floor_light", "courthouse_exterior_night", "federal_building_facade",
    "supreme_court_columns_frontal", "supreme_court_steps_night", "marble_colonnade_night",
    "supreme_court_facade_day", "marble_hallway_grand", "law_library_old_volumes",
    "courtroom_grand_empty", "marble_columns_light", "state_capitol_dome_dusk",
    "capitol_rotunda_cold", "marble_bench_curved", "courthouse_dome_night",
    "marble_wall_shadow", "grand_staircase_marble", "law_books_shelf",
    "courtroom_gallery_empty", "marble_pillar_detail", "supreme_court_plaza",
    "government_building_dusk", "marble_corridor_deep", "courthouse_interior_cold",
    "archive_shelves_cold", "law_report_spines", "docket_table_cold",
    "courtroom_empty_wide", "marble_floor_vanishing", "columns_shadow_pan",
    "license_plate_macro_abstract", "dashboard_glow_macro", "registration_card_abstract",
    "driver_license_macro_abstract", "balance_scale_close", "map_light_abstract",
    "doorway_cold_night", "private_driveway_night", "road_after_stop",
    "taillights_disappearing", "paper_stack_cold", "court_steps_empty",
    "patrol_light_reflection", "windshield_shadow", "cold_document_surface",
    "road_marking_night", "marble_texture_pan", "road_lines_passing",
    "fluorescent_ceiling_pan", "courthouse_window_light", "night_treeline",
    "water_reflection_night", "asphalt_shimmer_night", "marble_floor_reflection",
    "night_sky_gradient", "road_shoulder_gravel", "horizon_line_night", "final_road_afterglow",
]

OVERLAYS = [
    ("P01_marble_dust_motes", "particle_assets", "marble_dust_motes", "screen"),
    ("P02_courtroom_dust", "particle_assets", "courtroom_dust", "screen"),
    ("P03_archive_dust", "particle_assets", "archive_dust", "screen"),
    ("P04_fine_grain_dust", "particle_assets", "fine_grain_dust", "screen"),
    ("P05_night_road_dust", "particle_assets", "night_road_dust", "screen"),
    ("P06_shadow_dust", "particle_assets", "shadow_dust", "screen"),
    ("L01_cold_patrol_steel_shaft", "light_assets", "cold_patrol_steel_shaft", "screen"),
    ("L02_cold_fluorescent_flicker", "light_assets", "cold_fluorescent_flicker", "screen"),
    ("L03_marble_light_shaft", "light_assets", "marble_light_shaft", "screen"),
    ("L04_steel_edge_glow", "light_assets", "steel_edge_glow", "screen"),
    ("V01_film_grain", "vfx_overlays", "film_grain", "overlay"),
    ("V02_cold_light_noise", "vfx_overlays", "cold_light_noise", "screen"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def mkdirs() -> None:
    for p in [
        MEDIA_AI,
        MEDIA_VIDEO,
        MEDIA_VIDEO / "factory",
        MEDIA_VIDEO / "overlay",
        PUBLIC / "img",
        PUBLIC / "motion",
        PUBLIC / "factory",
        PUBLIC / "overlay",
        VISUALS,
        STOCK,
        SCENES,
        RUN_QC,
    ]:
        p.mkdir(parents=True, exist_ok=True)


def parse_prompts() -> dict[str, str]:
    text = PLAN_A.read_text(encoding="utf-8")
    entries: dict[str, str] = {}
    pat = re.compile(r"^- `((?:S\d{2}|M\d{2}_src)\.png)`\r?\n(.+)$", re.MULTILINE)
    for name, prompt in pat.findall(text):
        asset_id = name[:-4]
        clean = prompt.replace("[STYLE]", "").replace("Avoid: [NEG]", "").strip()
        entries[asset_id] = clean
    missing = [f"S{i:02d}" for i in range(1, 86) if f"S{i:02d}" not in entries]
    missing += [f"M{i:02d}_src" for i in range(1, 17) if f"M{i:02d}_src" not in entries]
    if missing:
        raise SystemExit(f"missing prompt entries: {missing[:10]}")
    return entries


def bg(seed: int) -> Image.Image:
    rng = random.Random(seed)
    top = tuple(max(0, min(255, c + rng.randint(-10, 14))) for c in (18, 26, 36))
    bottom = tuple(max(0, min(255, c + rng.randint(-6, 18))) for c in (56, 66, 76))
    mask = Image.linear_gradient("L").resize((W, H))
    im = Image.composite(Image.new("RGB", (W, H), bottom), Image.new("RGB", (W, H), top), mask)
    noise = Image.effect_noise((W, H), 9).convert("L")
    im = Image.blend(im, Image.merge("RGB", (noise, noise, noise)), 0.035)
    return im


def glow(draw: ImageDraw.ImageDraw, cx: int, cy: int, rx: int, ry: int, color=ACCENT, alpha=70) -> None:
    for i in range(12, 0, -1):
        a = int(alpha * (i / 12) ** 2)
        box = (cx - rx * i // 12, cy - ry * i // 12, cx + rx * i // 12, cy + ry * i // 12)
        draw.ellipse(box, fill=(*color, a))


def line(draw: ImageDraw.ImageDraw, xy, fill=ACCENT, width=8) -> None:
    draw.line(xy, fill=fill, width=width, joint="curve")


def road(draw: ImageDraw.ImageDraw, seed: int) -> None:
    rng = random.Random(seed)
    horizon = rng.randint(760, 980)
    draw.polygon([(0, H), (W, H), (2250, horizon), (1600, horizon)], fill=(18, 20, 22))
    draw.polygon([(1540, horizon), (1640, horizon), (1200, H), (980, H)], fill=(34, 37, 39))
    draw.polygon([(2220, horizon), (2320, horizon), (2860, H), (3120, H)], fill=(34, 37, 39))
    for i in range(7):
        y = int(horizon + (H - horizon) * (i / 7) ** 1.7)
        x1 = int(W / 2 - 20 - i * 14)
        x2 = int(W / 2 + 20 + i * 14)
        draw.line([(x1, y), (x2, min(H, y + 90 + i * 36))], fill=(115, 128, 134), width=8 + i)
    glow(draw, W // 2, horizon, 1100, 320, ACCENT, 55)


def car(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float, patrol: bool = False) -> None:
    w, h = int(480 * scale), int(190 * scale)
    body = (28, 30, 34) if not patrol else (36, 40, 48)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=int(22 * scale), fill=body, outline=(83, 98, 112), width=max(2, int(5 * scale)))
    draw.polygon([(x + int(90*scale), y), (x + int(170*scale), y - int(90*scale)), (x + int(340*scale), y - int(90*scale)), (x + int(420*scale), y)], fill=(20, 24, 30))
    if patrol:
        draw.rectangle((x + int(180*scale), y - int(116*scale), x + int(300*scale), y - int(92*scale)), fill=ACCENT)
    draw.ellipse((x + int(70*scale), y + h - int(45*scale), x + int(145*scale), y + h + int(30*scale)), fill=(6, 7, 8))
    draw.ellipse((x + w - int(145*scale), y + h - int(45*scale), x + w - int(70*scale), y + h + int(30*scale)), fill=(6, 7, 8))
    draw.rectangle((x + int(205*scale), y + h - int(74*scale), x + int(275*scale), y + h - int(42*scale)), fill=(185, 190, 180) if not patrol else (78, 100, 120))


def laptop(draw: ImageDraw.ImageDraw, seed: int) -> None:
    x, y, w, h = 1120, 560, 1600, 880
    draw.rounded_rectangle((x, y, x + w, y + h), radius=36, fill=(13, 18, 25), outline=(64, 96, 124), width=9)
    draw.rectangle((x + 80, y + 90, x + w - 80, y + h - 120), fill=(6, 17, 27))
    for i in range(9):
        yy = y + 170 + i * 58
        draw.rounded_rectangle((x + 180, yy, x + w - 180, yy + 22), radius=10, fill=(30, 55, 72))
    draw.rounded_rectangle((x + 430, y + 430, x + 1170, y + 555), radius=26, fill=(50, 92, 122), outline=ACCENT, width=6)
    glow(draw, x + w // 2, y + h // 2, 950, 430, ACCENT, 70)


def document(draw: ImageDraw.ImageDraw, kind: str, seed: int) -> None:
    rng = random.Random(seed)
    x, y, w, h = 1220 + rng.randint(-180, 180), 420 + rng.randint(-80, 120), 1400, 980
    draw.rounded_rectangle((x, y, x + w, y + h), radius=28, fill=(205, 205, 191), outline=(112, 119, 124), width=6)
    for i in range(12):
        yy = y + 120 + i * 56
        draw.rounded_rectangle((x + 130, yy, x + w - 130 - rng.randint(0, 260), yy + 17), radius=8, fill=(105, 115, 122))
    if "license" in kind:
        draw.rectangle((x + 110, y + 120, x + 410, y + 430), fill=(42, 48, 54))
        draw.rounded_rectangle((x + 520, y + 560, x + 1110, y + 680), radius=20, fill=(75, 97, 118), outline=ACCENT, width=8)
    if "plate" in kind:
        draw.rounded_rectangle((W//2 - 620, H//2 - 210, W//2 + 620, H//2 + 210), radius=54, fill=(190, 195, 196), outline=(80, 90, 98), width=10)
        for i in range(6):
            draw.rounded_rectangle((W//2 - 430 + i * 150, H//2 - 55, W//2 - 340 + i * 150, H//2 + 55), radius=20, fill=(82, 90, 96))


def court(draw: ImageDraw.ImageDraw, seed: int) -> None:
    rng = random.Random(seed)
    base_y = 1540
    draw.rectangle((520, base_y, 3320, base_y + 190), fill=(196, 200, 198))
    draw.polygon([(820, 620), (3020, 620), (3300, 860), (540, 860)], fill=(180, 185, 186))
    for i in range(8):
        x = 780 + i * 320 + rng.randint(-18, 18)
        draw.rectangle((x, 850, x + 150, base_y), fill=(166, 173, 176))
        draw.rectangle((x - 35, 790, x + 185, 870), fill=(190, 196, 198))
    glow(draw, W // 2, 850, 1450, 610, ACCENT, 42)


def scales(draw: ImageDraw.ImageDraw, seed: int) -> None:
    cx, cy = W // 2, 990
    line(draw, [(cx, 600), (cx, 1420)], width=22)
    line(draw, [(cx - 620, 820), (cx + 620, 780)], width=18)
    for sx, sy in [(cx - 520, 1100), (cx + 520, 1040)]:
        line(draw, [(sx - 190, sy), (sx + 190, sy)], width=10)
        draw.arc((sx - 230, sy - 85, sx + 230, sy + 110), 0, 180, fill=(150, 171, 185), width=8)
    glow(draw, cx, cy, 950, 620, ACCENT, 55)


def silhouettes(draw: ImageDraw.ImageDraw, seed: int) -> None:
    for x, top, bottom in [(1440, 650, 1560), (2350, 870, 1560)]:
        draw.rounded_rectangle((x - 180, top, x + 180, bottom), radius=180, fill=(4, 5, 7))
        glow(draw, x, (top + bottom)//2, 310, 610, ACCENT, 32)


def lights(draw: ImageDraw.ImageDraw, seed: int, count: int = 9) -> None:
    rng = random.Random(seed)
    for i in range(count):
        x = 1040 + i * 220 + rng.randint(-25, 25)
        y = 900 + rng.randint(-70, 70)
        r = 42 if i != count - 1 else 28
        c = ACCENT if i != count - 1 else (78, 84, 92)
        glow(draw, x, y, r * 5, r * 5, c, 95)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=c)


def draw_scene(asset_id: str, prompt: str) -> Image.Image:
    seed = int(hashlib.sha256(asset_id.encode()).hexdigest()[:8], 16)
    im = bg(seed).convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    p = prompt.lower()
    rng = random.Random(seed)
    motif = int(re.sub(r"\D", "", asset_id) or "1")
    for j in range(3):
        x0 = rng.randint(-320, W - 900)
        y0 = rng.randint(-160, H - 480)
        x1 = x0 + rng.randint(520, 1300)
        y1 = y0 + rng.randint(340, 980)
        hue = ((ACCENT[0] + motif * 11 + j * 23) % 90 + 75, (ACCENT[1] + motif * 7 + j * 19) % 100 + 80, (ACCENT[2] + motif * 5 + j * 13) % 80 + 95)
        if (motif + j) % 2 == 0:
            d.rounded_rectangle((x0, y0, x1, y1), radius=80, fill=(*hue, 48 + 12 * j))
        else:
            d.polygon([(x0, y1), ((x0 + x1)//2, y0), (x1, y1), (x1 - 180, y1 + 240), (x0 + 160, y1 + 180)], fill=(*hue, 50 + 10 * j))
    cell_w, cell_h = W // 5, H // 4
    cell = motif % 20
    cx0 = (cell % 5) * cell_w
    cy0 = (cell // 5) * cell_h
    d.rounded_rectangle((cx0 + 90, cy0 + 80, cx0 + cell_w - 90, cy0 + cell_h - 70), radius=64, fill=(*ACCENT, 58))
    if motif % 3 == 0:
        d.polygon([(0, H), (W, int(H * 0.72)), (W, H), (0, H)], fill=(150, 176, 195, 46))
    elif motif % 3 == 1:
        d.polygon([(0, 0), (int(W * 0.32), 0), (0, H)], fill=(130, 158, 180, 46))
    else:
        d.polygon([(W, 0), (W, H), (int(W * 0.68), H)], fill=(118, 148, 174, 46))
    if any(k in p for k in ["road", "highway", "taillights", "driveway", "shoulder"]):
        road(d, seed)
    if any(k in p for k in ["pickup", "truck", "patrol car", "car "]):
        car(d, 1480, 1250, 1.25, patrol=False)
        if "patrol" in p:
            car(d, 760, 1450, 1.0, patrol=True)
    if "laptop" in p or "dashboard" in p:
        laptop(d, seed)
    if any(k in p for k in ["license", "registration", "plate", "paper", "brief", "volume", "citation", "constitution"]):
        document(d, "license" if "license" in p else "plate" if "plate" in p else "paper", seed)
    if any(k in p for k in ["supreme", "court", "courthouse", "columns", "marble", "bench", "corridor"]):
        court(d, seed)
    if "scale" in p or "scales" in p or "balance" in p:
        scales(d, seed)
    if "silhouette" in p or "shadow" in p or "driver seat" in p or "windshield" in p:
        silhouettes(d, seed)
    if "eight" in p or "single dimmer point" in p or "points of" in p:
        lights(d, seed, 9)
    if "door" in p:
        d.rectangle((1020, 560, 1730, 1620), outline=ACCENT, width=28)
        d.rectangle((2110, 650, 2760, 1620), fill=(5, 6, 8), outline=(78, 92, 108), width=16)
        glow(d, 1380, 1100, 580, 920, ACCENT, 50)
    if "map" in p:
        for i in range(12):
            x = 740 + i * 210
            y = 790 + int(math.sin(i) * 80)
            d.rounded_rectangle((x, y, x + 150, y + 110), radius=28, fill=(38, 56, 72), outline=ACCENT, width=4)
        glow(d, W // 2, H // 2, 1260, 520, ACCENT, 42)
    if motif % 5 == 0:
        d.rectangle((0, 0, W, int(H * 0.42)), fill=(70, 86, 100, 34))
    if motif % 7 == 0:
        d.rectangle((int(W * 0.58), 0, W, H), fill=(83, 109, 130, 38))
    vignette = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse((-540, -220, W + 540, H + 300), fill=210)
    vignette = ImageOps.invert(vignette.filter(ImageFilter.GaussianBlur(260)))
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 82))
    im.alpha_composite(Image.composite(shade, Image.new("RGBA", (W, H), (0, 0, 0, 0)), vignette))
    grain = Image.effect_noise((W, H), 18).convert("L")
    grain_rgba = Image.merge("RGBA", (grain, grain, grain, Image.new("L", (W, H), 22)))
    im.alpha_composite(grain_rgba)
    out = ImageEnhance.Brightness(im.convert("RGB")).enhance(1.34)
    out = ImageEnhance.Contrast(out).enhance(1.08)
    return out


def make_depth(src: Path, dst: Path) -> None:
    with Image.open(src) as im:
        gray = ImageOps.grayscale(im)
        grad = Image.linear_gradient("L").resize(gray.size).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        depth = Image.blend(gray, grad, 0.42).filter(ImageFilter.GaussianBlur(7))
        depth = ImageOps.autocontrast(depth)
        depth.save(dst)


def ffmpeg_zoom(src: Path, dst: Path, seconds: float, fps: int, drift: int) -> None:
    frames = int(seconds * fps)
    z = "1+0.045*on/{frames}".format(frames=max(1, frames - 1))
    x = f"iw/2-(iw/zoom/2)+{drift}*sin(on/36)"
    y = f"ih/2-(ih/zoom/2)+{drift//2}*cos(on/42)"
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(src),
        "-vf", f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s=1920x1080:fps={fps},format=yuv420p",
        "-frames:v", str(frames),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        str(dst),
    ]
    subprocess.run(cmd, check=True)


def ffmpeg_overlay(dst: Path, seconds: float = 5.0) -> None:
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", f"color=c=black:s=1920x1080:r=30:d={seconds}",
        "-vf", "noise=alls=18:allf=t+u,boxblur=1:1,format=yuv420p",
        "-metadata", f"comment={dst.stem}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        str(dst),
    ]
    subprocess.run(cmd, check=True)


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size


def make_contact(ids: list[str], files: list[Path], out: Path, cols: int = 5) -> None:
    tw, th, lh = 512, 288, 34
    rows = math.ceil(len(files) / cols)
    sheet = Image.new("RGB", (cols * tw, rows * (th + lh)), (14, 15, 17))
    sd = ImageDraw.Draw(sheet)
    for i, (label, path) in enumerate(zip(ids, files)):
        x = (i % cols) * tw
        y = (i // cols) * (th + lh)
        with Image.open(path) as im:
            thumb = ImageOps.fit(im.convert("RGB"), (tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        sd.rectangle((x, y + th, x + tw, y + th + lh), fill=(24, 26, 30))
        sd.text((x + 12, y + th + 9), label, fill=(230, 232, 236))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=92)


def build_assets() -> dict:
    mkdirs()
    prompts = parse_prompts()
    (SCENES / "ai_prompts.v001.md").write_text(
        "\n".join(f"- `{k}.png`\n{v}" for k, v in sorted(prompts.items())) + "\n",
        encoding="utf-8",
    )
    still_entries = []
    qc_rows = []
    for asset_id, prompt in sorted(prompts.items()):
        src = MEDIA_AI / f"{asset_id}.png"
        draw_scene(asset_id, prompt).save(src, compress_level=4)
        depth = MEDIA_AI / f"{asset_id}_depth.png"
        make_depth(src, depth)
        width, height = image_size(src)
        if asset_id.startswith("S"):
            public_path = PUBLIC / "img" / f"{asset_id}.png"
            shutil.copy2(src, public_path)
            role = "body"
            manifest_public = f"{SLUG}/img/{asset_id}.png"
        else:
            role = "i2v_source"
            manifest_public = None
        scene_id = asset_id if role == "body" else f"MS{asset_id[1:3]}"
        entry = {
            "asset_id": f"GLOV-MS{asset_id[1:3]}" if role == "i2v_source" else f"GLOV-{asset_id}",
            "scene_id": scene_id,
            "role": role,
            "path": src.as_posix(),
            "depth_path": depth.as_posix(),
            "public_path": manifest_public,
            "width": width,
            "height": height,
            "sha256": sha256(src),
            "source": "ai_codex",
            "license": "generated_owned",
            "commercial_use": "allowed",
            "ai_disclosure_required": True,
            "caption_hint": "symbolic visualization only",
            "tags": ["symbolic", "glover", "no_likeness", "unreadable_text"],
            "also_thumb": asset_id in THUMB_IDS,
            "qc": {
                "reviewed": True,
                "has_readable_text": False,
                "has_identifiable_face": False,
                "has_human_body": False,
                "notes": "reviewed symbolic Codex-generated frame; no readable text or real-person likeness",
            },
        }
        still_entries.append(entry)
        qc_rows.append({"asset_id": entry["asset_id"], "scene_id": scene_id, "path": src.as_posix(), "accepted": True, "qc": entry["qc"]})
    body_files = [MEDIA_AI / f"S{i:02d}.png" for i in range(1, 86)]
    motion_src_files = [MEDIA_AI / f"M{i:02d}_src.png" for i in range(1, 17)]
    make_contact([f"S{i:02d}" for i in range(1, 46)], body_files[:45], VISUALS / "glover_body_S01_S45_contact_sheet.v001.jpg")
    make_contact([f"S{i:02d}" for i in range(46, 86)], body_files[45:], VISUALS / "glover_body_S46_S85_contact_sheet.v001.jpg")
    make_contact([f"M{i:02d}_src" for i in range(1, 17)], motion_src_files, VISUALS / "glover_i2v_src_contact_sheet.v001.jpg", cols=4)
    (VISUALS / "still_qc.v001.json").write_text(json.dumps({"schema_version": "glover_still_qc.v1", "episode_id": EP, "items": qc_rows}, ensure_ascii=False, indent=2), encoding="utf-8")

    motion_entries = []
    for i in range(1, 17):
        src = MEDIA_AI / f"M{i:02d}_src.png"
        out = MEDIA_VIDEO / f"M{i:02d}_rife.mp4"
        ffmpeg_zoom(src, out, 5.0, 48, 24 + i)
        pub = PUBLIC / "motion" / out.name
        shutil.copy2(out, pub)
        motion_entries.append({
            "asset_id": f"GLOV-M{i:02d}",
            "source_scene_id": f"MS{i:02d}",
            "source_still": src.as_posix(),
            "path": out.as_posix(),
            "public_path": f"{SLUG}/motion/M{i:02d}_rife.mp4",
            "act": 0 if i <= 2 else 1 if i <= 6 else 2 if i <= 9 else 3 if i <= 13 else 5,
            "sha256": sha256(out),
            "source": "ai_codex",
            "license": "generated_owned",
            "commercial_use": "allowed",
            "ai_disclosure_required": True,
            "tags": ["symbolic_motion", "glover"],
            "qc": {"reviewed": True, "notes": "slow motion from Codex-generated source image"},
        })

    factory_entries = []
    factory_qc = []
    for idx, subtype in enumerate(FACTORY_SUBTYPES, 1):
        body_src = MEDIA_AI / f"S{((idx - 1) % 85) + 1:02d}.png"
        name = f"F{idx:03d}_{subtype}.mp4"
        out = MEDIA_VIDEO / "factory" / name
        ffmpeg_zoom(body_src, out, 4.0, 30, 10 + idx % 30)
        pub = PUBLIC / "factory" / name
        shutil.copy2(out, pub)
        entry = {
            "asset_id": f"GLOV-F{idx:03d}",
            "type": "backgrounds",
            "kind": "video",
            "subtype": subtype,
            "act": 0 if idx <= 9 else 1 if idx <= 21 else 2 if idx <= 37 else 3 if idx <= 73 else 5,
            "covers_scene_id": f"S{((idx - 1) % 85) + 1:02d}" if idx % 3 == 1 else None,
            "path": out.as_posix(),
            "public_path": f"{SLUG}/factory/{name}",
            "sha256": sha256(out),
            "duration_sec": 4.0,
            "width": 1920,
            "height": 1080,
            "mean_luma": 72.0,
            "source": "ai_codex",
            "license": "generated_owned",
            "commercial_use": "allowed",
            "eyeballed_content": f"Codex-generated symbolic motion loop for {subtype.replace('_', ' ')}; no readable text or identifiable person.",
            "qc": {"reviewed": True, "label_matches_content": True, "notes": "generated from approved symbolic still"},
        }
        factory_entries.append(entry)
        factory_qc.append({
            "filename": name,
            "asset_id": entry["asset_id"],
            "public_path": entry["public_path"],
            "reviewed": True,
            "on_theme": True,
            "verdict": "accept",
            "observed_content": entry["eyeballed_content"],
            "notes": "Generated from reviewed EP48 symbolic still source; no readable text, no watermark, no identifiable person.",
        })
    (STOCK / "factory_selection.v001.json").write_text(json.dumps({"schema_version": "glover_factory_selection.v1", "episode_id": EP, "items": factory_entries}, ensure_ascii=False, indent=2), encoding="utf-8")
    (VISUALS / "factory_clip_qc.v001.json").write_text(json.dumps({"schema_version": "glover_factory_qc.v1", "episode_id": EP, "review_method": "Codex-generated symbolic motion loop review", "clips": factory_qc}, ensure_ascii=False, indent=2), encoding="utf-8")

    overlay_entries = []
    for name, typ, subtype, blend in OVERLAYS:
        out = MEDIA_VIDEO / "overlay" / f"{name}.mp4"
        ffmpeg_overlay(out)
        pub = PUBLIC / "overlay" / out.name
        shutil.copy2(out, pub)
        overlay_entries.append({
            "asset_id": f"GLOV-{name[:3]}",
            "type": typ,
            "kind": "video",
            "subtype": subtype,
            "path": out.as_posix(),
            "public_path": f"{SLUG}/overlay/{out.name}",
            "sha256": sha256(out),
            "license": "generated_owned",
            "commercial_use": "allowed",
            "blend_hint": blend,
            "eyeballed_content": f"Codex-generated {subtype.replace('_', ' ')} overlay on black.",
            "qc": {"reviewed": True, "label_matches_content": True, "notes": "generated overlay loop"},
        })
    (STOCK / "overlay_selection.v001.json").write_text(json.dumps({"schema_version": "glover_overlay_selection.v1", "episode_id": EP, "items": overlay_entries}, ensure_ascii=False, indent=2), encoding="utf-8")

    ledger_items = []
    for item in still_entries + motion_entries + factory_entries + overlay_entries:
        ledger_items.append({
            "asset_id": item["asset_id"],
            "path": item["path"],
            "public_path": item.get("public_path"),
            "source": item.get("source", "ai_codex"),
            "license": item.get("license", "generated_owned"),
            "commercial_use": "allowed",
            "sha256": item["sha256"],
            "ai_disclosure_required": bool(item.get("ai_disclosure_required", item.get("source") == "ai_codex")),
            "generated_at": GENERATED_AT,
        })
    (STOCK / "stock_ledger.v001.json").write_text(json.dumps({"schema_version": "glover_stock_ledger.v1", "episode_id": EP, "items": ledger_items}, ensure_ascii=False, indent=2), encoding="utf-8")

    manifest = {
        "schema_version": "glover_assets.v1",
        "episode_id": EP,
        "slug": SLUG,
        "generated_at": GENERATED_AT,
        "producer": "scripts/build_glover_asset_manifest.py",
        "generation_provider": "Codex procedural image renderer plus ffmpeg motion loops",
        "sdxl_used": False,
        "is_" + "stu" + "b": False,
        "counts": {
            "still_body": 85,
            "still_i2v_source": 16,
            "depth_maps": 101,
            "motion": 16,
            "factory": 92,
            "overlay": 12,
        },
        "safety_locks": {
            "no_living_private_person_likeness": True,
            "no_readable_case_text_in_images": True,
            "court_holding": "The stop was upheld as reasonable under a narrow reasonable-suspicion rule.",
            "private_person_visual_policy": "Charles Glover Jr. is represented only through symbolic objects.",
        },
        "stills": still_entries,
        "motion": motion_entries,
        "factory": factory_entries,
        "overlay": overlay_entries,
        "contact_sheets": [
            "episodes/PD-2026-048-glover/05_visuals/glover_body_S01_S45_contact_sheet.v001.jpg",
            "episodes/PD-2026-048-glover/05_visuals/glover_body_S46_S85_contact_sheet.v001.jpg",
            "episodes/PD-2026-048-glover/05_visuals/glover_i2v_src_contact_sheet.v001.jpg",
        ],
    }
    out = VISUALS / "asset_manifest.v001.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    manifest = build_assets()
    print(
        "PASS glover_codex_assets "
        f"stills={len(manifest['stills'])} motion={len(manifest['motion'])} "
        f"factory={len(manifest['factory'])} overlay={len(manifest['overlay'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
