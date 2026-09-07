#!/usr/bin/env python3
"""Build a structured PD-2026-005 Madoff first cut v003.

This replaces the weak v002 "video-like" proxy with a proper program structure:
HOOK -> branded OPENING -> BODY ACTS -> ENDING -> fixed end card.

No upload. No additional paid API calls. Uses already generated ElevenLabs chunks.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-005-madoff"
EPDIR = ROOT / "episodes" / EP
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EPM = MEDIA / "episodes" / EP
LIB = MEDIA / "library"
VOICE_DIR = EPM / "06_voice" / "draft"
SDXL_DIR = EPM / "05_visuals" / "sdxl_hq_v001_180"
OUT_REPO = EPDIR / "08_edit" / "renders" / "review.proxy.v003.mp4"
OUT_MEDIA = EPM / "08_edit" / "madoff_review_v003_structured.mp4"
OPENING_ASSET = ROOT / "remotion" / "out" / "opening.mp4"
OPENING_TRIM_START = 0.72
TARGET_TOTAL_SEC = 720.0
FFMPEG = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
FFPROBE = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe")
if not FFMPEG.exists():
    FFMPEG = Path("ffmpeg")
if not FFPROBE.exists():
    FFPROBE = Path("ffprobe")

W, H, FPS = 1920, 1080, 30
INK = (10, 10, 12)
NAVY = (11, 26, 43)
GOLD = (229, 181, 58)
GOLD2 = (248, 214, 130)
WHITE = (245, 247, 250)
SILVER = (200, 205, 214)
MUTED = (128, 135, 148)
RED = (134, 42, 34)


def run(cmd: list[str | os.PathLike[str]], desc: str) -> None:
    print(f">> {desc}")
    p = subprocess.run([str(c) for c in cmd], capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print((p.stderr or "")[-3000:])
        raise RuntimeError(desc)


def duration(path: Path) -> float:
    p = subprocess.run(
        [str(FFPROBE), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
    )
    return float(p.stdout.strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\impact.ttf" if bold else r"C:\Windows\Fonts\trebuc.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\georgiab.ttf" if bold else r"C:\Windows\Fonts\georgia.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size=size)
    return ImageFont.load_default()


F_HUGE = font(150, True)
F_TITLE = font(86, True)
F_CARD = font(62, True)
F_MED = font(38, True)
F_BODY = font(30, False)
F_SMALL = font(23, False)


def parse_script_chunks() -> list[dict[str, str]]:
    text = (EPDIR / "03_script" / "script.en.v001.md").read_text("utf-8")
    chunks: list[dict[str, str]] = []
    current = ""
    buf: list[str] = []
    no = 1

    def flush() -> None:
        nonlocal no, buf
        s = " ".join(x.strip() for x in buf if x.strip()).strip()
        buf = []
        if not s:
            return
        s = re.sub(r"\*([^*]+)\*", r"\1", s)
        chunks.append({"chunk_id": f"VC-{no:04d}", "section": current, "text": s})
        no += 1

    started = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            flush()
            started = True
            current = re.sub(r"\s+[-—].*$", "", line[3:].strip()).upper()
            continue
        if not started or not line or line.startswith("#") or line.startswith("- ") or line == "---":
            if started and not line:
                flush()
            continue
        buf.append(line)
    flush()
    return chunks


def make_audio(tmp: Path) -> tuple[Path, list[dict[str, float | str]], dict[str, tuple[float, float]], float, float, float]:
    chunks = parse_script_chunks()
    silence035 = tmp / "silence_035.mp3"
    silence_open = tmp / "silence_opening.mp3"
    opening_dur = max(0.1, duration(OPENING_ASSET) - OPENING_TRIM_START) if OPENING_ASSET.exists() else 3.5
    run([FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "0.35", "-c:a", "libmp3lame", "-b:a", "192k", silence035], "silence 0.35s")
    run([FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", f"{opening_dur:.3f}", "-c:a", "libmp3lame", "-b:a", "192k", silence_open], "brand opening silence")

    entries: list[str] = []
    index: list[dict[str, float | str]] = []
    section_ranges: dict[str, list[float]] = {}
    cursor = 0.0
    opening_insert_at = 0.0
    for i, c in enumerate(chunks):
        path = VOICE_DIR / f"{c['chunk_id']}.mp3"
        if not path.exists():
            raise FileNotFoundError(path)
        d = duration(path)
        # Keep the cold open short. The remaining "hook" narration becomes part of
        # the post-opening introduction instead of a long standalone hook.
        sec = "OPENING" if str(c["section"]) == "HOOK" and i >= 2 else str(c["section"])
        if i == 2:
            opening_insert_at = cursor
            entries.append(f"file '{silence_open.as_posix()}'\n")
            cursor += opening_dur
        entries.append(f"file '{path.as_posix()}'\n")
        index.append({"chunk_id": c["chunk_id"], "section": sec, "text": c["text"], "start": round(cursor, 3), "end": round(cursor + d, 3), "seconds": round(d, 3)})
        section_ranges.setdefault(sec, [cursor, cursor])
        section_ranges[sec][1] = cursor + d
        cursor += d
        if i != len(chunks) - 1:
            entries.append(f"file '{silence035.as_posix()}'\n")
            cursor += 0.35
    concat = tmp / "narration_concat.txt"
    concat.write_text("".join(entries), "utf-8")
    master = EPM / "06_voice" / "master" / "vc_master_v003_structured.mp3"
    master.parent.mkdir(parents=True, exist_ok=True)
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat, "-c:a", "libmp3lame", "-b:a", "192k", master], "structured narration master")
    ranges = {k: (round(v[0], 3), round(v[1], 3)) for k, v in section_ranges.items()}
    (EPDIR / "06_audio" / "narration_index.v003.json").write_text(json.dumps({
        "episode_id": EP,
        "voice_id": "nPczCjzI2devNBz1zQrb",
        "model_id": "eleven_multilingual_v2",
        "structure": "HOOK -> standard branded opening -> OPENING -> ACT 1 -> ACT 2 -> ACT 3 -> ACT 4 -> ENDING",
        "opening_insert_at": round(opening_insert_at, 3),
        "opening_duration": round(opening_dur, 3),
        "generated_total_seconds": round(duration(master), 3),
        "master": f"artifact://episodes/{EP}/06_voice/master/vc_master_v003_structured.mp3",
        "sections": ranges,
        "chunks": index,
    }, indent=2, ensure_ascii=False) + "\n", "utf-8")
    return master, index, ranges, opening_insert_at, opening_dur, duration(master)


def bg(seed: int = 0) -> Image.Image:
    img = Image.new("RGB", (W, H), INK)
    px = img.load()
    for y in range(H):
        for x in range(W):
            gx = (x - W * 0.62) / W
            gy = (y - H * 0.38) / H
            glow = max(0, 1 - math.sqrt(gx * gx * 3.6 + gy * gy * 5.4) * 2.4)
            vign = max(0, 1 - math.sqrt(((x - W / 2) / W) ** 2 + ((y - H / 2) / H) ** 2) * 1.7)
            stripe = 5 * math.sin((x + seed * 19) / 95) + 3 * math.sin((y + seed * 31) / 75)
            r = int(INK[0] + glow * 46 + vign * 5 + stripe)
            g = int(INK[1] + glow * 35 + vign * 4 + stripe)
            b = int(INK[2] + glow * 20 + vign * 7 + stripe)
            px[x, y] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    return img.filter(ImageFilter.GaussianBlur(0.35))


SDXL_PICK = {
    # Curated toward cleaner, higher-detail SDXL outputs; avoid noisy crowd/hand-heavy shots where possible.
    "hook_line": ["hook/H02_c05_*.png", "hook/B02_*.png", "hook/H01_c02_*.png"],
    "hook_crime": ["actIII/B16_*.png", "actIII/H16_c02_*.png", "hook/H03_c03_*.png"],
    "trust": ["opening/H05_c05_*.png", "opening/H05_c03_*.png", "opening/B04_*.png", "actI/H06_c05_*.png"],
    "private_club": ["actI/B05_*.png", "actI/H07_c05_*.png", "actI/H07_c02_*.png"],
    "no_trades": ["actII/B09_*.png", "actII/H11_c01_*.png", "actII/B10_*.png"],
    "ponzi": ["actII/H13_c02_*.png", "actII/H13_c04_*.png", "actII/B11_*.png"],
    "numbers": ["actII/H14_c01_*.png", "actII/H14_c05_*.png", "actII/B13_*.png", "actII/B14_*.png"],
    "math": ["actIII/B16_*.png", "actIII/B15_*.png", "actIII/H16_c04_*.png"],
    "warnings": ["actIII/B17_*.png", "actIII/H18_c01_*.png", "actIII/H18_c05_*.png"],
    "collapse": ["actIV/B19_*.png", "actIV/H20_c02_*.png", "actIV/H21_c03_*.png"],
    "court": ["actIV/H22_c03_*.png", "actIV/H22_c05_*.png", "actIV/B21_*.png"],
    "sentence": ["actIV/B22_*.png", "actIV/H23_c02_*.png", "actIV/H23_c05_*.png"],
    "lesson": ["ending/B23_*.png", "ending/B24_*.png", "ending/H25_c02_*.png", "ending/H26_c03_*.png"],
}


def cover_image(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGB")
    scale = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.Resampling.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H))
    im = im.filter(ImageFilter.GaussianBlur(0.15))
    return im


def sdxl_bg(kind: str, seed: int) -> Image.Image:
    choices: list[Path] = []
    for pat in SDXL_PICK.get(kind, []):
        choices.extend(sorted(SDXL_DIR.glob(pat)))
    if not choices:
        return bg(seed)
    p = choices[seed % len(choices)]
    im = cover_image(p)
    # Keep generated art visible, but normalize to the channel's gold/noir grade.
    im = ImageEnhance.Brightness(im).enhance(1.12)
    im = ImageEnhance.Contrast(im).enhance(1.18)
    im = ImageEnhance.Sharpness(im).enhance(1.18)
    im = ImageEnhance.Color(im).enhance(0.98)
    return im


def draw_brand(d: ImageDraw.ImageDraw, label: str, citation: str | None = None) -> None:
    d.text((58, 44), "PRIME DOCUMENTARY", font=F_SMALL, fill=(190, 168, 116))
    d.line((58, 80, 334, 80), fill=GOLD, width=2)
    d.text((58, 96), label.upper(), font=F_SMALL, fill=MUTED)
    if citation:
        d.rounded_rectangle((58, 964, 1110, 1023), radius=9, fill=(0, 0, 0, 170), outline=(129, 101, 47), width=1)
        d.text((80, 980), citation, font=F_SMALL, fill=SILVER)


def line_chart(d: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, jagged: bool = False, smooth_color=GOLD2) -> None:
    d.line((x0, y1, x1, y1), fill=(76, 68, 52), width=2)
    d.line((x0, y0, x0, y1), fill=(76, 68, 52), width=2)
    pts = []
    for i in range(110):
        t = i / 109
        x = x0 + t * (x1 - x0)
        if jagged:
            y = y1 - (0.22 + 0.55 * t + math.sin(t * 35) * 0.09 + math.sin(t * 77) * 0.035) * (y1 - y0)
        else:
            y = y1 - (0.16 + 0.68 * t + math.sin(t * 5) * 0.01) * (y1 - y0)
        pts.append((x, y))
    for w, c in [(18, (80, 56, 16)), (8, smooth_color), (3, (255, 239, 170))]:
        d.line(pts, fill=c, width=w, joint="curve")


def card(kind: str, title: str, subtitle: str, label: str, citation: str | None, out: Path, seed: int) -> None:
    img = bg(seed) if kind in {"brand_open", "endcard", "hook_line"} else sdxl_bg(kind, seed)
    d = ImageDraw.Draw(img, "RGBA")
    # Readability layer over SDXL art. Stronger on text-heavy cards, lighter on atmospheric shots.
    if kind not in {"brand_open", "endcard"}:
        d.rectangle((0, 0, W, H), fill=(0, 0, 0, 58))
        d.rectangle((0, 0, W, 260), fill=(0, 0, 0, 72))
        d.rectangle((0, 820, W, H), fill=(0, 0, 0, 68))
    draw_brand(d, label, citation)
    if kind == "hook_line":
        d.rounded_rectangle((330, 165, 1590, 780), radius=24, fill=(238, 224, 188, 244), outline=(176, 129, 42), width=5)
        d.text((425, 230), "Monthly Account Statement", font=F_BODY, fill=(34, 29, 20))
        d.rounded_rectangle((1160, 215, 1510, 260), radius=7, fill=(255, 248, 214, 220), outline=(168, 124, 42), width=1)
        d.text((1182, 225), "no down months", font=F_SMALL, fill=(55, 42, 24))
        d.line((410, 300, 1510, 300), fill=(115, 89, 44), width=3)
        for yy in [400, 480, 560, 640, 720]:
            d.line((455, yy, 1465, yy), fill=(132, 120, 95, 70), width=2)
        for xx in [560, 760, 960, 1160, 1360]:
            d.line((xx, 365, xx, 725), fill=(132, 120, 95, 55), width=2)
        line_chart(d, 455, 365, 1465, 725)
    elif kind == "hook_crime":
        line_chart(d, 250, 280, 1660, 620)
        d.rounded_rectangle((565, 655, 1355, 745), radius=18, fill=(6, 6, 8, 205), outline=GOLD, width=2)
        d.text((960, 700), "ONE MAN SAW A CRIME", font=F_CARD, fill=GOLD2, anchor="mm")
    elif kind == "brand_open":
        d.ellipse((820, 270, 1100, 550), outline=GOLD, width=8)
        d.text((960, 410), "PD", font=F_HUGE, fill=WHITE, anchor="mm")
        d.line((660, 610, 1260, 610), fill=GOLD, width=4)
        d.text((960, 675), "PRIME DOCUMENTARY", font=F_CARD, fill=WHITE, anchor="mm")
        d.text((960, 735), "MADOFF: THE PERFECT LINE", font=F_MED, fill=GOLD2, anchor="mm")
    elif kind == "trust":
        for x, s in [(430, 0.9), (650, 1.05), (900, 0.95), (1160, 1.08), (1420, 0.92)]:
            d.ellipse((x - 36 * s, 385 - 72 * s, x + 36 * s, 385), fill=(4, 4, 6))
            d.rounded_rectangle((x - 72 * s, 390, x + 72 * s, 730), radius=54, fill=(5, 5, 7))
        line_chart(d, 360, 170, 1560, 315)
    elif kind == "private_club":
        d.rounded_rectangle((680, 190, 1240, 900), radius=18, fill=(26, 20, 13), outline=(120, 90, 42), width=5)
        d.rectangle((720, 230, 1200, 900), fill=(14, 12, 10))
        d.ellipse((1135, 545, 1168, 578), fill=GOLD)
        d.line((420, 780, 1500, 780), fill=(108, 28, 24), width=12)
    elif kind == "no_trades":
        d.rounded_rectangle((450, 300, 1470, 760), radius=22, fill=(5, 6, 8), outline=(110, 91, 55), width=4)
        for x in range(520, 1400, 135):
            d.rectangle((x, 410, x + 90, 620), fill=(18, 22, 26), outline=(64, 64, 60), width=2)
    elif kind == "ponzi":
        cx, cy, r = 960, 530, 300
        for a in range(0, 360, 45):
            x = cx + math.cos(math.radians(a)) * r
            y = cy + math.sin(math.radians(a)) * r
            d.ellipse((x - 32, y - 32, x + 32, y + 32), fill=GOLD, outline=(255, 235, 170), width=4)
        for a in range(0, 360, 45):
            x1 = cx + math.cos(math.radians(a)) * r
            y1 = cy + math.sin(math.radians(a)) * r
            x2 = cx + math.cos(math.radians(a + 32)) * r
            y2 = cy + math.sin(math.radians(a + 32)) * r
            d.line((x1, y1, x2, y2), fill=(170, 128, 52), width=10)
        d.text((960, 500), "NEW MONEY", font=F_CARD, fill=WHITE, anchor="mm")
        d.text((960, 570), "PAYS OLD PAYOUTS", font=F_CARD, fill=GOLD2, anchor="mm")
    elif kind == "numbers":
        d.text((410, 365), "$65B", font=F_HUGE, fill=GOLD2, anchor="mm")
        d.text((410, 475), "statement illusion", font=F_BODY, fill=SILVER, anchor="mm")
        d.line((610, 410, 1235, 410), fill=GOLD, width=8)
        d.polygon([(1235, 410), (1188, 382), (1188, 438)], fill=GOLD)
        d.text((1505, 365), "$17.5B", font=F_HUGE, fill=WHITE, anchor="mm")
        d.text((1505, 475), "real principal", font=F_BODY, fill=SILVER, anchor="mm")
        d.text((960, 705), "THE GAP IS THE SCHEME", font=F_CARD, fill=GOLD2, anchor="mm")
    elif kind == "math":
        d.rounded_rectangle((470, 220, 1450, 805), radius=18, fill=(220, 210, 178), outline=(110, 82, 38), width=4)
        line_chart(d, 610, 360, 1310, 630)
        d.line((690, 420, 1220, 545), fill=RED, width=9)
    elif kind == "warnings":
        y = 575
        d.line((310, y, 1610, y), fill=GOLD, width=6)
        for i, year in enumerate(["2000", "2001", "2005", "2007", "2008"]):
            x = 310 + i * 325
            d.ellipse((x - 20, y - 20, x + 20, y + 20), fill=GOLD2)
            d.text((x, y - 72), year, font=F_MED, fill=SILVER, anchor="mm")
            d.text((x, y + 92), "warning", font=F_SMALL, fill=SILVER, anchor="mm")
    elif kind == "collapse":
        for i, x in enumerate(range(330, 1600, 115)):
            d.ellipse((x - 22, 455 + (i % 3) * 22, x + 22, 505 + (i % 3) * 22), fill=(8, 8, 10))
            d.rounded_rectangle((x - 42, 508 + (i % 3) * 22, x + 42, 780 + (i % 3) * 22), radius=36, fill=(7, 7, 9))
    elif kind == "court":
        for x in range(480, 1460, 165):
            d.rectangle((x, 310, x + 70, 790), fill=(46, 44, 42), outline=(154, 126, 72), width=3)
        d.polygon([(390, 310), (1530, 310), (1375, 180), (545, 180)], fill=(43, 41, 39), outline=GOLD)
    elif kind == "sentence":
        for x in range(520, 1410, 115):
            d.rectangle((x, 160, x + 38, 950), fill=(16, 17, 20))
            d.rectangle((x + 6, 160, x + 14, 950), fill=(79, 65, 44))
        d.text((960, 455), "150", font=F_HUGE, fill=GOLD2, anchor="mm")
        d.text((960, 610), "YEARS", font=F_HUGE, fill=WHITE, anchor="mm")
    elif kind == "lesson":
        line_chart(d, 240, 340, 850, 760, jagged=False)
        line_chart(d, 1070, 340, 1680, 760, jagged=True, smooth_color=(150, 180, 255))
        d.text((960, 180), "IF IT LOOKS PERFECT", font=F_TITLE, fill=WHITE, anchor="mm")
        d.text((960, 250), "ASK WHY", font=F_TITLE, fill=GOLD2, anchor="mm")
    elif kind == "endcard":
        d.ellipse((820, 255, 1100, 535), outline=GOLD, width=8)
        d.text((960, 395), "PD", font=F_HUGE, fill=WHITE, anchor="mm")
        d.text((960, 630), "PRIME DOCUMENTARY", font=F_TITLE, fill=WHITE, anchor="mm")
        d.text((960, 710), "SUBSCRIBE", font=F_CARD, fill=GOLD2, anchor="mm")
        d.text((960, 770), "New episodes every week", font=F_BODY, fill=SILVER, anchor="mm")
    else:
        d.text((960, 420), title, font=F_TITLE, fill=WHITE, anchor="mm")
        d.text((960, 510), subtitle, font=F_MED, fill=GOLD2, anchor="mm")
    title_kinds = {"numbers", "sentence", "lesson"}
    if title and kind in title_kinds:
        d.text((960, 132), title, font=F_TITLE, fill=WHITE, anchor="mm")
        if subtitle:
            d.text((960, 205), subtitle, font=F_BODY, fill=SILVER, anchor="mm")
    if kind != "hook_line":
        d.rounded_rectangle((1455, 54, 1840, 102), radius=8, fill=(0, 0, 0, 155), outline=(103, 84, 48), width=1)
        d.text((1475, 67), "symbolic reconstruction", font=F_SMALL, fill=SILVER)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, quality=94)


def make_scene_plan(ranges: dict[str, tuple[float, float]], opening_insert_at: float, opening_dur: float, narration_total: float) -> list[dict[str, float | str]]:
    scenes: list[dict[str, float | str]] = []
    hook_end = opening_insert_at
    scenes += [
        {"start": 0.0, "end": min(7.0, hook_end), "kind": "hook_line", "title": "", "subtitle": "", "label": "hook", "citation": "CLM-0006 - the too-perfect return line"},
        {"start": min(7.0, hook_end), "end": hook_end, "kind": "hook_crime", "title": "", "subtitle": "", "label": "hook", "citation": "symbolic reconstruction; not financial advice"},
        {"start": hook_end, "end": hook_end + opening_dur, "kind": "brand_open", "title": "", "subtitle": "", "label": "opening", "citation": None},
    ]

    def add_section(sec: str, defs: list[tuple[str, str, str, str, str | None]]) -> None:
        a, b = ranges[sec]
        step = (b - a) / len(defs)
        for i, (kind, title, subtitle, label, citation) in enumerate(defs):
            scenes.append({"start": a + i * step, "end": a + (i + 1) * step, "kind": kind, "title": title, "subtitle": subtitle, "label": label, "citation": citation})

    add_section("OPENING", [
        ("trust", "BERNARD MADOFF", "the trusted name and the chart that should have exposed him", "opening", "Dramatized symbolic reconstruction"),
    ])
    add_section("ACT 1", [
        ("trust", "THE NAME YOU COULD TRUST", "prestige was the engine", "act I", None),
        ("private_club", "THE PRIVATE CLUB", "invitation felt like proof", "act I", None),
        ("hook_line", "THE LINE STAYED SMOOTH", "good years, bad years, still up", "act I", "CLM-0006 - smooth returns"),
    ])
    add_section("ACT 2", [
        ("no_trades", "THE HIDDEN SYSTEM", "the investment story was not real", "act II", "Trustee findings"),
        ("ponzi", "THE PONZI LOOP", "new money paid old payouts", "act II", "CLM-0003 - Ponzi mechanism"),
        ("numbers", "$65B VS $17.5B", "the paper illusion versus real principal", "act II", "CLM-0004 - SIPA Trustee estimate"),
        ("ponzi", "THE FATAL MATH", "it could never stop growing", "act II", None),
    ])
    add_section("ACT 3", [
        ("math", "THE MAN WHO DID THE MATH", "smoothness was the evidence", "act III", "CLM-0005 / CLM-0006"),
        ("warnings", "THE WARNINGS", "specific, repeated, and missed", "act III", "CLM-0011 - SEC OIG report"),
        ("trust", "THE WATCHDOG SLEPT", "the system looked away", "act III", None),
    ])
    add_section("ACT 4", [
        ("collapse", "THE COLLAPSE", "2008 forced the arithmetic into the open", "act IV", None),
        ("no_trades", "NO VAULT TO OPEN", "there was nothing left to pay with", "act IV", None),
        ("court", "THE RECKONING", "guilty plea, not a trial", "act IV", "CLM-0001 / CLM-0007"),
        ("sentence", "150 YEARS", "a symbolic sentence", "act IV", "CLM-0002 - sentence"),
        ("numbers", "THE RECOVERY", "more was clawed back than expected", "act IV", "CLM-0009 - trustee recoveries"),
    ])
    add_section("ENDING", [
        ("lesson", "THE LESSON", "smoothness is not proof of safety", "ending", "not financial advice"),
    ])
    scenes.append({"start": narration_total, "end": narration_total + 9.0, "kind": "endcard", "title": "", "subtitle": "", "label": "endcard", "citation": None})
    return densify_scenes(scenes)


def densify_scenes(scenes: list[dict[str, float | str]]) -> list[dict[str, float | str]]:
    """Turn long static scenes into short documentary B-roll shots.

    This avoids the paper-theater feel without reintroducing jittery camera motion.
    The first shot in a section carries the big title/citation; follow-up shots use
    alternate SDXL stills with minimal/no text so subtitles stay readable.
    """
    alternates = {
        "hook_line": ["hook_line", "hook_crime", "hook_line"],
        "hook_crime": ["hook_crime", "math", "warnings"],
        "trust": ["trust", "private_club", "trust", "hook_line"],
        "private_club": ["private_club", "trust"],
        "no_trades": ["no_trades", "numbers", "no_trades"],
        "ponzi": ["ponzi", "numbers", "ponzi"],
        "numbers": ["numbers", "no_trades", "numbers"],
        "math": ["math", "hook_line", "warnings"],
        "warnings": ["warnings", "math", "trust"],
        "collapse": ["collapse", "no_trades", "collapse"],
        "court": ["court", "sentence"],
        "sentence": ["sentence", "court"],
        "lesson": ["lesson", "hook_line", "lesson"],
    }
    dense: list[dict[str, float | str]] = []
    for scene in scenes:
        kind = str(scene["kind"])
        start = float(scene["start"])
        end = float(scene["end"])
        dur = end - start
        if kind in {"brand_open", "endcard"} or dur <= 8.0:
            dense.append(scene)
            continue
        pieces = max(2, int(math.ceil(dur / 8.5)))
        step = dur / pieces
        kind_cycle = alternates.get(kind, [kind])
        for i in range(pieces):
            sub = dict(scene)
            sub["start"] = round(start + i * step, 3)
            sub["end"] = round(start + (i + 1) * step, 3)
            sub["kind"] = kind_cycle[i % len(kind_cycle)]
            sub["shot_index"] = i
            if i > 0:
                sub["title"] = ""
                sub["subtitle"] = ""
                sub["citation"] = None
            dense.append(sub)
    return dense


def render_visuals(tmp: Path, scenes: list[dict[str, float | str]]) -> Path:
    still_dir = EPM / "05_visuals" / "coded_madoff_v003_structured"
    seg_dir = tmp / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)
    segs = []
    for i, s in enumerate(scenes):
        dur = max(0.5, float(s["end"]) - float(s["start"]))
        out = seg_dir / f"{i+1:02d}.mp4"
        # Use the same opening language as prior episodes, but render episode-specific text.
        # Do not use the generic opening asset visually; use its audio separately.
        img = still_dir / f"{i+1:02d}_{s['kind']}.jpg"
        card(str(s["kind"]), str(s["title"]), str(s["subtitle"]), str(s["label"]), s["citation"] if s["citation"] else None, img, i + 20)
        frames = max(1, int(round(dur * FPS)))
        # Smooth center zoom only. Pan caused visible coordinate stepping.
        # Scale to 4K first so any frame-to-frame rounding is much less visible.
        vf = (
            "scale=3840:2160:force_original_aspect_ratio=increase:flags=lanczos,"
            "crop=3840:2160,"
            "zoompan="
            f"z='1+0.022*on/{max(frames-1, 1)}':"
            "x='iw/2-iw/zoom/2':"
            "y='ih/2-ih/zoom/2':"
            f"d={frames}:s=1920x1080:fps=30,"
            "unsharp=3:3:0.45:3:3:0.20,"
            "format=yuv420p"
        )
        run([FFMPEG, "-y", "-loop", "1", "-i", img, "-vf", vf, "-t", f"{dur:.3f}", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", out], f"scene {i+1:02d} {s['kind']}")
        segs.append(out)
    concat = tmp / "visual_concat.txt"
    concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), "utf-8")
    out = tmp / "visuals.mp4"
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat, "-c", "copy", out], "concat structured visuals")
    return out


def make_captions(index: list[dict[str, float | str]], out: Path) -> None:
    def ts(t: float) -> str:
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = int(t % 60)
        ms = int(round((t - int(t)) * 1000))
        if ms == 1000:
            s += 1
            ms = 0
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    blocks = []
    n = 1
    for c in index:
        text = str(c["text"])
        start = float(c["start"])
        end = float(c["end"])
        words = text.split()
        if not words:
            continue
        max_words = 8
        parts = [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
        span = max(0.8, (end - start) / len(parts))
        for i, part in enumerate(parts):
            a = start + i * span
            b = min(end, a + span * 0.92)
            blocks.append(f"{n}\n{ts(a)} --> {ts(b)}\n{part}\n")
            n += 1
    out.write_text("\n".join(blocks), "utf-8")


def make_music(tmp: Path, total: float) -> Path:
    tracks = [
        LIB / "music/hook/mus_20260614_hook_glass_air_bed_v1.mp3",
        LIB / "music/opening/mus_20260614_opening_measured_arpeggio_v1.mp3",
        LIB / "music/explainer_bed/mus_20260614_explainer_bed_soft_explainer_v1.mp3",
        LIB / "music/reveal/mus_20260614_reveal_hidden_system_clicks_v1.mp3",
        LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3",
        LIB / "music/somber/mus_20260614_somber_ledger_of_ash_v1.mp3",
        LIB / "music/outro/mus_20260614_outro_last_frame_v1.mp3",
    ]
    weights = [0.07, 0.08, 0.18, 0.23, 0.19, 0.13, 0.12]
    cur = 0.0
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    for i, (tr, w) in enumerate(zip(tracks, weights)):
        dur = total * w if i < len(tracks) - 1 else total - cur
        inputs += ["-stream_loop", "-1", "-i", str(tr)]
        delay = int(cur * 1000)
        filters.append(f"[{i}:a]atrim=0:{dur:.3f},afade=t=in:st=0:d=1.0,afade=t=out:st={max(dur-1.2,0.1):.3f}:d=1.2,adelay={delay}|{delay}[m{i}]")
        labels.append(f"[m{i}]")
        cur += dur
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0,volume=0.20[music]")
    out = tmp / "music.m4a"
    run([FFMPEG, "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[music]", "-t", f"{total:.3f}", "-c:a", "aac", "-b:a", "192k", out], "structured music bed")
    return out


def make_sfx(tmp: Path, scenes: list[dict[str, float | str]], total: float) -> Path:
    # SFX should punctuate story beats, not every B-roll cut.
    # Earlier versions triggered sounds on most image changes, which felt unnatural.
    emph = {
        "ponzi": "sfx_binder_lock.mp3",
        "numbers": "sfx_stamp_seal.mp3",
        "warnings": "sfx_sub_drop.mp3",
        "collapse": "sfx_low_boom.mp3",
        "court": "sfx_gavel_knock.mp3",
        "sentence": "sfx_sub_drop.mp3",
    }
    cues: list[tuple[Path, float, float]] = []
    last_kind_at: dict[str, float] = {}
    for s in scenes:
        a = float(s["start"])
        kind = str(s["kind"])
        if kind in {"brand_open", "endcard"}:
            continue
        # Only first shot of a split scene, and avoid repeating same SFX too close together.
        if int(s.get("shot_index", 0)) > 0:
            continue
        if kind not in emph:
            continue
        if kind in last_kind_at and a - last_kind_at[kind] < 28:
            continue
        last_kind_at[kind] = a
        offset = 0.35
        gain = 0.36
        if kind in {"collapse", "sentence"}:
            gain = 0.52
            offset = 0.15
        elif kind == "numbers":
            offset = 0.95
        elif kind == "ponzi":
            offset = 0.70
        elif kind == "warnings":
            offset = 0.55
        elif kind == "court":
            offset = 0.45
        cues.append((LIB / "sfx" / emph[kind], a + offset, gain))
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    for i, (f, t, g) in enumerate(cues):
        inputs += ["-i", str(f)]
        d = int(t * 1000)
        filters.append(f"[{i}:a]volume={g},adelay={d}|{d}[s{i}]")
        labels.append(f"[s{i}]")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0,volume=0.60[sfx]")
    out = tmp / "sfx.m4a"
    run([FFMPEG, "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[sfx]", "-t", f"{total:.3f}", "-c:a", "aac", "-b:a", "160k", out], f"structured sfx bed ({len(cues)} cues)")
    return out


def make_opening_audio(tmp: Path, opening_insert_at: float, opening_dur: float, total: float) -> Path:
    out = tmp / "opening_audio.m4a"
    if not OPENING_ASSET.exists():
        run([FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", f"{total:.3f}", "-c:a", "aac", "-b:a", "128k", out], "empty opening audio")
        return out
    delay = int(opening_insert_at * 1000)
    run([
        FFMPEG, "-y", "-ss", f"{OPENING_TRIM_START:.3f}", "-i", OPENING_ASSET,
        "-filter_complex",
        f"[0:a]atrim=0:{opening_dur:.3f},asetpts=PTS-STARTPTS,volume=1.0,adelay={delay}|{delay}[op]",
        "-map", "[op]", "-t", f"{total:.3f}", "-c:a", "aac", "-b:a", "160k", out
    ], "standard opening audio")
    return out


def finish(video: Path, narration: Path, music: Path, sfx: Path, captions: Path, opening_audio: Path, opening_insert_at: float, opening_dur: float, total: float) -> None:
    amb = LIB / "ambience/amb_institutional_drone.mp3"
    srt = captions.as_posix().replace(":", "\\:")
    style = "FontName=Trebuchet MS,FontSize=19,PrimaryColour=&H00F5F7FA,OutlineColour=&H00070709,BackColour=&H80000000,Outline=2,Shadow=1,MarginV=34"
    vf = f"eq=contrast=1.06:saturation=1.04:gamma=0.98,subtitles='{srt}':force_style='{style}'"
    fc = (
        f"[3:a]atrim=0:{total:.3f},volume=0.055[amb];"
        "[1:a]volume=1.0[vo];"
        f"[2:a]volume='if(between(t,{opening_insert_at:.3f},{opening_insert_at+opening_dur:.3f}),0,0.82)'[mus];"
        f"[4:a]volume='if(between(t,{opening_insert_at:.3f},{opening_insert_at+opening_dur:.3f}),0,0.72)'[sfx];"
        "[5:a]volume=1.0[op];"
        "[vo][mus][amb][sfx][op]amix=inputs=5:normalize=0:duration=longest:dropout_transition=0,"
        f"alimiter=limit=0.94,afade=t=out:st={max(total-2.0,1):.3f}:d=2[a]"
    )
    OUT_MEDIA.parent.mkdir(parents=True, exist_ok=True)
    pre_out = OUT_MEDIA.with_name(OUT_MEDIA.stem + ".preconform.mp4")
    tmp_out = OUT_MEDIA.with_suffix(".tmp.mp4")
    run([FFMPEG, "-y", "-i", video, "-i", narration, "-i", music, "-stream_loop", "-1", "-i", amb, "-i", sfx, "-i", opening_audio,
         "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-vf", vf,
         "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", pre_out], "structured final mix")
    actual = duration(pre_out)
    video_ratio = TARGET_TOTAL_SEC / actual
    audio_tempo = actual / TARGET_TOTAL_SEC
    run([
        FFMPEG, "-y", "-i", pre_out,
        "-filter_complex",
        f"[0:v]setpts={video_ratio:.9f}*PTS[v];[0:a]atempo={audio_tempo:.9f}[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-t", f"{TARGET_TOTAL_SEC:.3f}", "-movflags", "+faststart", tmp_out
    ], "conform to exactly 12:00")
    tmp_out.replace(OUT_MEDIA)
    try:
        pre_out.unlink()
    except OSError:
        pass
    OUT_REPO.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUT_MEDIA, OUT_REPO)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    with tempfile.TemporaryDirectory(prefix="pd_madoff_v003_") as td:
        tmp = Path(td)
        narration, index, ranges, opening_insert_at, opening_dur, narration_total = make_audio(tmp)
        scenes = make_scene_plan(ranges, opening_insert_at, opening_dur, narration_total)
        total = narration_total + 9.0
        captions = EPDIR / "08_edit" / "captions.review_proxy.v003.srt"
        make_captions(index, captions)
        video = render_visuals(tmp, scenes)
        music = make_music(tmp, total)
        sfx = make_sfx(tmp, scenes, total)
        opening_audio = make_opening_audio(tmp, opening_insert_at, opening_dur, total)
        finish(video, narration, music, sfx, captions, opening_audio, opening_insert_at, opening_dur, total)
    h = sha256(OUT_REPO)
    qc = {
        "episode_id": EP,
        "render": "08_edit/renders/review.proxy.v003.mp4",
        "sha256": h,
        "duration_seconds": round(duration(OUT_REPO), 3),
        "structure": "HOOK -> branded OPENING -> OPENING narration -> ACT 1 -> ACT 2 -> ACT 3 -> ACT 4 -> ENDING -> fixed end card",
        "audio": "ElevenLabs channel voice, structured pauses, library music, ambience, structured SFX",
        "visual": "chapter-specific coded noir graphics; not final SDXL/Runway photographic master",
        "external_upload_performed": False,
        "paid_generation_performed_this_run": False,
        "known_limitations": [
            "Still not final SDXL/Runway photographic footage.",
            "Captions are generated from chunk timing, not forced word alignment.",
            "This is a first-cut structure check, not publish master."
        ],
    }
    (EPDIR / "08_edit" / "renders" / "review.proxy.v003.qc.json").write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"OUT {OUT_REPO}")
    print(f"SHA256 {h}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
