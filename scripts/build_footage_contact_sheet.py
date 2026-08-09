#!/usr/bin/env python
"""Labeled contact sheet of an episode's IMAGE/FOOTAGE pool, for pre-render visual QC.

The factory shelf's labels are broken (evidence_bag == a cartoon): a machine gate
CANNOT tell an off-topic clip from an on-topic one, so a human eyeball on a LABELED
sheet is the only defense (EP32 postmortem D-contact / pd-factory-shelf-mislabeled).
`make_contact_sheets.py` tiles Midjourney variant quads on the SSD inbox; this instead
tiles the WHOLE staged pool for one episode with each source's FILENAME, so mislabeled /
off-topic / duplicated assets are caught BEFORE a long render is spent.

Discovers images from remotion/public/<slug>/img (fallback 05_visuals), or use --dir.
An explicit --dir can also review staged video by extracting a representative frame.
`--from-json` tiles an explicit, already-ordered SELECTION (what a picker chose, with
the picker's own per-item label) — that is how select_factory_assets.py forces the
eyeball step onto every theme pick.

Usage:
    python scripts/build_footage_contact_sheet.py --ep PD-2026-031-unlock
    python scripts/build_footage_contact_sheet.py --dir some/media/folder --out out.png
    python scripts/build_footage_contact_sheet.py --from-json runs/qc/.../selection.v001.json
Output: runs/qc/<slug>_footage_contact_NN.png  (one or more sheets)
"""
from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
EPISODES = ROOT / "episodes"
# .tif was missing until 2026-08-09, and its absence was not a cosmetic bug: a TIF fell
# through to the ffmpeg branch below, ffmpeg failed to seek 1s into a still, and the tile
# was drawn as a red UNREADABLE box. 2,953 items on the shelf are TIF -- 1,447 from the
# Library of Congress and 1,404 from Wikimedia -- so every contact sheet reviewed so far
# showed the archival half of those sources as blank red. Verdicts were recorded from
# those sheets. Four "Farm foreclosure sale - NARA" plates, exactly what Prime Finance was
# short of, sat behind red boxes on the foreclosure sheet.
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".gif", ".bmp"}
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv"}

COLS = 5
ROWS = 4                     # 20 tiles / sheet
THUMB_W = 360
LABEL_H = 22
PAD = 6


def _fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def resolve_slug(arg: str) -> tuple[str, Path | None]:
    p = EPISODES / arg
    if p.is_dir():
        return arg.split("-")[-1], p
    hits = sorted(d for d in EPISODES.glob("PD-2026-*") if d.is_dir() and arg in d.name)
    if hits:
        return hits[-1].name.split("-")[-1], hits[-1]
    return arg, None


def discover_media(
    ep_arg: str | None,
    dir_arg: str | None,
    media_kind: str,
    excludes: list[str],
) -> tuple[str, list[Path]]:
    allowed = IMG_EXT if media_kind == "image" else VIDEO_EXT if media_kind == "video" else IMG_EXT | VIDEO_EXT

    def wanted(p: Path) -> bool:
        return p.suffix.lower() in allowed and not any(x.lower() in p.name.lower() for x in excludes)

    if dir_arg:
        d = Path(dir_arg)
        if not d.is_dir():
            _fail(f"--dir not a directory: {d}")
        media = [p for p in sorted(d.rglob("*")) if wanted(p)]
        return d.name, media
    if not ep_arg:
        _fail("need --ep or --dir")
    slug, epdir = resolve_slug(ep_arg)
    roots = [ROOT / "remotion" / "public" / slug / "img",
             ROOT / "remotion" / "public" / slug]
    if epdir:
        roots.append(epdir / "05_visuals")
    imgs: list[Path] = []
    seen: set[str] = set()
    for r in roots:
        if not r.is_dir():
            continue
        for p in sorted(r.rglob("*")):
            if wanted(p) and "depth" not in p.name.lower() \
                    and p.name not in seen:
                imgs.append(p)
                seen.add(p.name)
        if imgs:
            break
    return slug, imgs


def load_selection(json_path: str) -> tuple[str, list[Path], dict[str, str]]:
    """Read an explicit, already-ordered selection written by a picker.

    Accepts either a bare list or an object with `items`. Each item needs a path
    (`abs_path` or `path`) and may carry `label` — the picker's own verdict, which is
    what makes the sheet reviewable (`match`, `cross_theme->here`, `off_label`...).
    Returns (title, media paths, path -> label).
    """
    p = Path(json_path)
    if not p.is_file():
        _fail(f"--from-json not a file: {p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    items = data.get("items", []) if isinstance(data, dict) else data
    title = (data.get("title") if isinstance(data, dict) else None) or p.stem
    media: list[Path] = []
    labels: dict[str, str] = {}
    for it in items:
        raw = it.get("abs_path") or it.get("path") if isinstance(it, dict) else it
        if not raw:
            continue
        mp = Path(str(raw))
        media.append(mp)
        if isinstance(it, dict) and it.get("label"):
            labels[str(mp)] = str(it["label"])
    if not media:
        _fail(f"--from-json has no items with a path: {p}")
    return str(title), media, labels


def load_frame(media_path: Path) -> Image.Image:
    if media_path.suffix.lower() in IMG_EXT:
        return Image.open(media_path).convert("RGB")
    proc = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", "1", "-i", str(media_path),
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return Image.open(io.BytesIO(proc.stdout)).convert("RGB")


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:  # noqa: BLE001
            continue
    return ImageFont.load_default()


def build_sheet(images: list[Path], out: Path, title: str,
                labels: dict[str, str] | None = None) -> None:
    labels = labels or {}
    two_line = bool(labels)
    label_h = LABEL_H * 2 if two_line else LABEL_H
    thumb_h = int(THUMB_W * 9 / 16)
    cell_w = THUMB_W + PAD
    cell_h = thumb_h + label_h + PAD
    head = 34
    W = COLS * cell_w + PAD
    H = head + ROWS * cell_h + PAD
    canvas = Image.new("RGB", (W, H), (18, 18, 22))
    draw = ImageDraw.Draw(canvas)
    draw.text((PAD, 8), title, fill=(235, 235, 240), font=_font(20))
    f_lbl = _font(12)
    unreadable: list[tuple[str, str]] = []
    for i, img_path in enumerate(images):
        r, c = divmod(i, COLS)
        x = PAD + c * cell_w
        y = head + r * cell_h
        try:
            im = load_frame(img_path)
            im.thumbnail((THUMB_W, thumb_h))
            tile = Image.new("RGB", (THUMB_W, thumb_h), (0, 0, 0))
            tile.paste(im, ((THUMB_W - im.width) // 2, (thumb_h - im.height) // 2))
            canvas.paste(tile, (x, y))
        except Exception as e:  # noqa: BLE001
            # Swallowing the reason is how the missing .tif extension survived: the sheet
            # showed red boxes, a red box read as "bad file", and nobody learned that one
            # decoder was failing on 2,953 items at once. Collect and report.
            unreadable.append((img_path.name, f"{type(e).__name__}: {str(e)[:70]}"))
            draw.rectangle([x, y, x + THUMB_W, y + thumb_h], fill=(60, 20, 20))
            draw.text((x + 6, y + 6), "UNREADABLE", fill=(255, 180, 180), font=f_lbl)
        lbl = img_path.name
        if len(lbl) > 52:
            lbl = lbl[:24] + "…" + lbl[-24:]
        draw.rectangle([x, y + thumb_h, x + THUMB_W, y + thumb_h + label_h], fill=(30, 30, 36))
        draw.text((x + 4, y + thumb_h + 4), lbl, fill=(210, 210, 220), font=f_lbl)
        extra = labels.get(str(img_path))
        if extra:
            if len(extra) > 58:
                extra = extra[:57] + "…"
            # verdict line: red when the picker itself flagged the item
            warn = any(k in extra for k in ("off_label", "cross_theme", "no_ledger", "unaudited"))
            draw.text((x + 4, y + thumb_h + 4 + LABEL_H), extra,
                      fill=(255, 170, 120) if warn else (150, 220, 160), font=f_lbl)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
    if unreadable:
        by_reason: dict[str, int] = {}
        for _, why in unreadable:
            by_reason[why.split(":")[0]] = by_reason.get(why.split(":")[0], 0) + 1
        print(f"  !! {len(unreadable)}/{len(images)} tiles could not be decoded — a sheet "
              f"reviewed with these is a sheet reviewed blind")
        for reason, n in sorted(by_reason.items(), key=lambda kv: -kv[1]):
            print(f"     {n:4}  {reason}")
        for name, why in unreadable[:3]:
            print(f"     e.g. {name[:64]}  ({why})")


def main() -> int:
    ap = argparse.ArgumentParser(description="Labeled contact sheet of an episode's image or video pool.")
    ap.add_argument("--ep", help="episode id / slug / substring")
    ap.add_argument("--dir", help="explicit media folder (overrides --ep discovery)")
    ap.add_argument("--out", help="output path for a single sheet (else runs/qc/<slug>_footage_contact_NN.png)")
    ap.add_argument("--media", choices=("image", "video", "all"), default="image",
                    help="media type to include (default: image)")
    ap.add_argument("--exclude-substring", action="append", default=[],
                    help="exclude files whose name contains this text (repeatable)")
    ap.add_argument("--from-json",
                    help="explicit selection JSON (items[].abs_path/path + optional .label) — "
                         "tiles exactly what a picker chose, in its order, with its labels")
    ap.add_argument("--out-dir", help="directory for numbered sheets (default runs/qc/)")
    a = ap.parse_args()

    labels: dict[str, str] = {}
    if a.from_json:
        slug, images, labels = load_selection(a.from_json)
    else:
        slug, images = discover_media(a.ep, a.dir, a.media, a.exclude_substring)
    if not images:
        _fail(f"no {a.media} media found for '{a.ep or a.dir}' (assets may be on the SSD; pass --dir)")

    out_dir = Path(a.out_dir) if a.out_dir else ROOT / "runs" / "qc"
    per = COLS * ROWS
    sheets = [images[i:i + per] for i in range(0, len(images), per)]
    written: list[Path] = []
    for idx, chunk in enumerate(sheets, 1):
        out = (Path(a.out) if (a.out and len(sheets) == 1)
               else out_dir / f"{slug}_footage_contact_{idx:02d}.png")
        kind_label = "selection" if a.from_json else f"{a.media} pool"
        build_sheet(chunk, out, f"{slug} — {kind_label}  (sheet {idx}/{len(sheets)}, {len(images)} total)",
                    labels)
        written.append(out)
        print(f"  wrote {out}  ({len(chunk)} tiles)")
    print(f"[footage-contact] {len(images)} media files across {len(written)} labeled sheet(s).")
    print("  目視QC: 場違い素材(棚ラベル破損)・被り・題材不一致・4K割れ・画面内テキストを確認。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
