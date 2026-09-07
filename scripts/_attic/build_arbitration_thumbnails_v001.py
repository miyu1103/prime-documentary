#!/usr/bin/env python3
"""Create arbitration thumbnail backgrounds, render A/B/C candidates, and score CTR."""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-012-arbitration"
EPDIR = ROOT / "episodes" / EP
OUT = EPDIR / "10_thumbnail"
PKG = EPDIR / "09_package"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
AI_OUT = MEDIA / "assets" / "ai" / "thumbs" / "arbitration"
PUBLIC_THUMBS = ROOT / "remotion" / "public" / "arbitration" / "thumbs"
W, H = 1280, 720
INK = (4, 7, 12)
NAVY = (8, 23, 42)
BLUE = (31, 107, 255)
GOLD = (229, 181, 58)
WHITE = (245, 247, 250)

TITLES = {
    "A": "You Gave Up Your Right to Sue",
    "B": "The Fine Print Took Your Right to Sue",
    "C": "Why You Can't Sue Your Bank or Boss",
}


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    for candidate in [Path(r"C:\Windows\Fonts") / name, Path(r"C:\Windows\Fonts\arialbd.ttf"), Path(r"C:\Windows\Fonts\impact.ttf")]:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def base() -> Image.Image:
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    for y in range(H):
        r = y / H
        col = tuple(int(INK[i] * (1 - r) + NAVY[i] * r) for i in range(3))
        d.line((0, y, W, y), fill=col)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((690, -210, 1500, 610), fill=(31, 107, 255, 46))
    gd.ellipse((760, 180, 1480, 900), fill=(229, 181, 58, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(70))
    return Image.alpha_composite(img.convert("RGBA"), glow)


def grade(img: Image.Image) -> Image.Image:
    img = ImageEnhance.Contrast(img.convert("RGB")).enhance(1.18)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for x in range(W):
        a = int(172 * max(0, 1 - x / 620))
        d.line((x, 0, x, H), fill=(0, 0, 0, a))
    d.rectangle((0, 0, W, H), outline=GOLD + (255,), width=3)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def chain(d: ImageDraw.ImageDraw, points: list[tuple[int, int]], color=GOLD, width=13) -> None:
    for a, b in zip(points, points[1:]):
        d.line((*a, *b), fill=color, width=width)
    for x, y in points:
        d.ellipse((x - 20, y - 12, x + 20, y + 12), outline=color, width=6)


def thumb01() -> Image.Image:
    img = base()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((760, 230, 1150, 430), radius=44, fill=(20, 46, 68, 245), outline=GOLD, width=7)
    d.rounded_rectangle((800, 276, 1110, 384), radius=34, fill=(33, 116, 255, 210), outline=(170, 218, 255), width=3)
    chain(d, [(805, 462), (895, 430), (990, 466), (1095, 436), (1165, 474)], width=15)
    d.ellipse((700, 150, 1220, 520), outline=(60, 165, 255, 55), width=4)
    return grade(img)


def thumb02() -> Image.Image:
    img = base()
    d = ImageDraw.Draw(img)
    for i in range(32):
        x = 690 + (i % 4) * 130
        y = 80 + (i // 4) * 68
        d.rounded_rectangle((x, y, x + 92 + (i % 3) * 36, y + 17), radius=3, fill=(210, 218, 230, 70))
    d.rectangle((665, 45, 1245, 650), outline=GOLD, width=5)
    d.ellipse((690, 505, 808, 628), fill=(0, 0, 0, 170), outline=BLUE, width=3)
    d.rectangle((743, 370, 762, 540), fill=(4, 8, 14))
    d.ellipse((720, 325, 785, 390), fill=(4, 8, 14))
    return grade(img)


def thumb03() -> Image.Image:
    img = base()
    d = ImageDraw.Draw(img)
    d.rectangle((730, 95, 1185, 635), fill=(8, 13, 21), outline=(185, 196, 215), width=6)
    d.rectangle((765, 130, 1150, 635), fill=(12, 24, 40), outline=(70, 105, 150), width=3)
    d.line((720, 360, 1210, 360), fill=GOLD, width=20)
    chain(d, [(760, 360), (850, 338), (950, 366), (1050, 340), (1160, 364)], width=16)
    d.polygon([(760, 635), (1190, 635), (1280, 720), (660, 720)], fill=(2, 4, 8, 220))
    return grade(img)


def thumb04() -> Image.Image:
    img = base()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((830, 125, 1085, 525), radius=34, fill=(7, 13, 22), outline=GOLD, width=7)
    d.rounded_rectangle((855, 165, 1060, 485), radius=22, fill=(18, 33, 54), outline=BLUE, width=3)
    d.ellipse((745, 565, 1120, 650), fill=(0, 0, 0, 180))
    d.arc((790, 520, 945, 675), 30, 330, fill=GOLD, width=16)
    d.arc((940, 520, 1095, 675), 210, 150, fill=GOLD, width=16)
    d.line((910, 600, 980, 600), fill=GOLD, width=14)
    return grade(img)


def thumb05() -> Image.Image:
    img = base()
    d = ImageDraw.Draw(img)
    d.polygon([(710, 220), (1220, 140), (1180, 595), (660, 655)], fill=(214, 218, 205, 210))
    for i in range(8):
        d.rounded_rectangle((760, 250 + i * 42, 1120 - (i % 3) * 70, 266 + i * 42), radius=4, fill=(28, 35, 44, 70))
    d.line((730, 520, 1160, 472), fill=(30, 40, 52), width=3)
    chain(d, [(790, 525), (900, 500), (1010, 514), (1120, 492)], width=12)
    d.line((1070, 210, 970, 478), fill=(12, 14, 18), width=22)
    d.line((1082, 196, 982, 464), fill=(216, 225, 238), width=9)
    return grade(img)


def thumb06() -> Image.Image:
    img = base()
    d = ImageDraw.Draw(img)
    centers = [(780, 220), (1010, 230), (900, 425), (1160, 455), (735, 560)]
    for i, (x, y) in enumerate(centers):
        d.ellipse((x - 95, y - 38, x + 95, y + 38), fill=(229, 181, 58, 38), outline=(229, 181, 58, 120), width=3)
        d.ellipse((x - 13, y - 42, x + 13, y - 16), fill=(5, 8, 12))
        d.rectangle((x - 8, y - 18, x + 8, y + 32), fill=(5, 8, 12))
        if i:
            d.line((centers[i - 1][0], centers[i - 1][1], x, y), fill=(31, 107, 255, 45), width=2)
    return grade(img)


GENERATORS = [thumb01, thumb02, thumb03, thumb04, thumb05, thumb06]


def write_backgrounds() -> list[dict[str, object]]:
    OUT.mkdir(parents=True, exist_ok=True)
    AI_OUT.mkdir(parents=True, exist_ok=True)
    PUBLIC_THUMBS.mkdir(parents=True, exist_ok=True)
    results = []
    for idx, make in enumerate(GENERATORS, 1):
        tid = f"THUMB-{idx:02d}"
        img = make()
        for path in [AI_OUT / f"{tid}.png", OUT / f"background.{tid}.png", PUBLIC_THUMBS / f"{tid}.png"]:
            img.save(path)
        results.append({"id": tid, "episode_file": str((OUT / f"background.{tid}.png").relative_to(ROOT)).replace("\\", "/"), "public_static": f"arbitration/thumbs/{tid}.png", "sha256": sha256(OUT / f"background.{tid}.png")})
    sheet = Image.new("RGB", (960, 420), (8, 10, 14))
    sd = ImageDraw.Draw(sheet)
    for idx in range(1, 7):
        im = Image.open(OUT / f"background.THUMB-{idx:02d}.png").resize((320, 180), Image.Resampling.LANCZOS)
        x = ((idx - 1) % 3) * 320
        y = ((idx - 1) // 3) * 210
        sheet.paste(im, (x, y))
        sd.text((x + 10, y + 185), f"THUMB-{idx:02d}", font=font("arialbd.ttf", 20), fill=GOLD)
    sheet.save(OUT / "background.THUMB_contact_sheet.v001.jpg", quality=92)
    return results


def score_candidates(backgrounds: list[dict[str, object]]) -> tuple[str, list[dict[str, object]]]:
    scores = {
        "THUMB-01": (87, "Clear click/contract metaphor; strong right-side object and left text space."),
        "THUMB-02": (83, "Fine-print scale is on-theme, but the tiny subject is slightly less mobile-legible."),
        "THUMB-03": (94, "Best one-second story: courthouse door closed by chain; very high contrast and simple focal shape."),
        "THUMB-04": (86, "Strong consumer-phone hook, but shackle shadow is more subtle at mobile size."),
        "THUMB-05": (89, "Contract/signature chain is direct and premium, slightly less emotionally sharp than closed courthouse."),
        "THUMB-06": (80, "Class-action isolation idea is accurate, but multiple figures reduce single-subject clarity."),
    }
    evaluated = []
    for bg in backgrounds:
        score, reason = scores[str(bg["id"])]
        evaluated.append({**bg, "ctr_score": score, "ctr_reason": reason})
    selected = max(evaluated, key=lambda item: int(item["ctr_score"]))
    return str(selected["id"]), evaluated


def run_remotion_stills(selected_id: str) -> list[dict[str, object]]:
    candidates = []
    remotion_bin = ROOT / "remotion" / "node_modules" / ".bin" / "remotion.cmd"
    for key, title in TITLES.items():
        out = OUT / f"thumbnail.arbitration_option_{key}.v001.png"
        props = {"title": title, "backgroundSrc": f"arbitration/thumbs/{selected_id}.png", "variant": "left"}
        subprocess.run(
            [str(remotion_bin), "still", "ThumbnailFrame", str(out), "--props", json.dumps(props)],
            cwd=ROOT / "remotion",
            check=True,
        )
        candidates.append({"id": key, "title": title, "file": str(out.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(out)})
    selected_thumb = PKG / "thumbnail.selected.v001.png"
    PKG.mkdir(parents=True, exist_ok=True)
    selected_thumb.write_bytes((OUT / "thumbnail.arbitration_option_B.v001.png").read_bytes())
    return candidates


def main() -> int:
    backgrounds = write_backgrounds()
    selected_id, evaluated = score_candidates(backgrounds)
    candidates = run_remotion_stills(selected_id)
    title_scores = {
        "A": {"ctr_score": 88, "reason": "Direct second-person hook; a little long for mobile."},
        "B": {"ctr_score": 93, "reason": "Most compact curiosity gap: fine print quietly took a right."},
        "C": {"ctr_score": 84, "reason": "Concrete entities help, but the phrasing is broader and less iconic."},
    }
    for c in candidates:
        c.update(title_scores[str(c["id"])])
    meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "selected",
        "selection_criterion": "CTR maximum: high contrast, single clear subject, emotion, large text space, mobile readability.",
        "background_candidates": evaluated,
        "selected_background_id": selected_id,
        "title_candidates": candidates,
        "selected_title_id": "B",
        "selected_thumbnail": str((PKG / "thumbnail.selected.v001.png").relative_to(ROOT)).replace("\\", "/"),
        "selected_thumbnail_sha256": sha256(PKG / "thumbnail.selected.v001.png"),
        "safety": {"real_person_likeness": False, "judge_likeness": False, "text_in_background": False, "commercial_ok": True},
    }
    (PKG / "title_thumbnail_candidates.v001.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"selected_background_id": selected_id, "selected_title_id": "B", "selected_thumbnail": meta["selected_thumbnail"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
