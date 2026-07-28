"""Build click-focused thumbnails for PD-2026-004-ftx."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-004-ftx"
MEDIA = Path(r"H:\pd-media")
VIS = MEDIA / "episodes" / EP / "05_visuals" / "upscaled_4x_v001" / "openai_heroes"
OUT_DIR = MEDIA / "episodes" / EP / "09_package"
W, H = 1280, 720


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        Path(r"C:\Windows\Fonts") / name,
        Path(r"C:\Windows\Fonts\arialbd.ttf"),
        Path(r"C:\Windows\Fonts\arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


FONT_BLACK = font("ariblk.ttf", 118)
FONT_BIG = font("ariblk.ttf", 102)
FONT_MED = font("arialbd.ttf", 42)
FONT_SMALL = font("arialbd.ttf", 28)


def cover(src: Path) -> Image.Image:
    with Image.open(src) as im:
        im = im.convert("RGB")
    scale = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.Resampling.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def fit_font(text: str, base: ImageFont.FreeTypeFont, max_width: int, min_size: int = 54) -> ImageFont.FreeTypeFont:
    size = getattr(base, "size", 100)
    while size >= min_size:
        fnt = ImageFont.truetype(base.path, size=size) if hasattr(base, "path") else base
        dummy = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        if text_size(dummy, text, fnt)[0] <= max_width:
            return fnt
        size -= 4
    return ImageFont.truetype(base.path, size=min_size) if hasattr(base, "path") else base


def draw_shadowed(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt: ImageFont.ImageFont, fill: str) -> None:
    x, y = xy
    for dx, dy, alpha in [(6, 8, 180), (3, 4, 220)]:
        draw.text((x + dx, y + dy), text, font=fnt, fill=(0, 0, 0, alpha))
    draw.text((x, y), text, font=fnt, fill=fill)


def add_scrim(img: Image.Image, stronger: bool) -> Image.Image:
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pix = overlay.load()
    for x in range(W):
        left = max(0, 245 - int(x * (245 / 850)))
        bottom = max(0, 130 - int(abs(x - W * 0.45) * 0.18))
        for y in range(H):
            vertical = int(90 * (y / H))
            alpha = min(255, left + vertical + bottom + (30 if stronger else 0))
            pix[x, y] = (1, 5, 13, alpha)
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def render(slot: str, bg: Path, line1: str, line2: str, kicker: str, sub: str) -> Path:
    img = cover(bg).filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=2))
    img = add_scrim(img, stronger=slot == "A")
    draw = ImageDraw.Draw(img)

    # Accent rails and small brand mark.
    gold = "#f2b84b"
    cyan = "#5fe0ff"
    white = "#f7f7f4"
    draw.rectangle((0, H - 95, W, H - 88), fill=gold)
    draw.rectangle((0, 0, 18, H), fill=(242, 184, 75, 210))
    draw.rounded_rectangle((1085, 40, 1228, 82), radius=4, fill=(4, 9, 20, 210), outline=gold, width=2)
    draw.text((1104, 49), "PRIME DOC", font=FONT_SMALL, fill=white)

    draw.text((64, 82), kicker, font=FONT_SMALL, fill=cyan)
    f1 = fit_font(line1, FONT_BLACK, 760, 72)
    f2 = fit_font(line2, FONT_BIG, 760, 72)
    draw_shadowed(draw, (60, 152), line1, f1, white)
    y2 = 152 + text_size(draw, line1, f1)[1] + 18
    draw_shadowed(draw, (60, y2), line2, f2, gold)
    draw.rounded_rectangle((64, 570, 770, 632), radius=6, fill=(4, 9, 20, 220), outline=(255, 255, 255, 70), width=1)
    draw.text((88, 583), sub, font=FONT_MED, fill=white)

    out = OUT_DIR / f"thumbnail_click_{slot.lower()}_v001.png"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, quality=96)
    return out


def main() -> int:
    a = VIS / "PD-2026-004-ftx-THUMB-A-dissolving-vault.png"
    b = VIS / "PD-2026-004-ftx-THUMB-B-hooded-code.png"
    for p in [a, b]:
        if not p.exists():
            raise FileNotFoundError(p)
    outputs = [
        render("A", a, "$8B", "VANISHED", "FTX COLLAPSE", "THE HIDDEN CODE DOOR"),
        render("B", b, "THE $8B", "BACKDOOR", "FTX TRIAL", "CUSTOMER MONEY WAS NOT SAFE"),
    ]
    manifest = {
        "episode_id": EP,
        "revision": "v001",
        "selected": "thumbnail_click_a_v001.png",
        "alternates": [p.name for p in outputs],
        "files": [
            {"file": str(p), "sha256": sha256(p), "size_bytes": p.stat().st_size}
            for p in outputs
        ],
    }
    out = OUT_DIR / "thumbnail_manifest.v001.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
