#!/usr/bin/env python
"""Thumbnails built to the channel's OWN measured template (CTR_PLAYBOOK §4A "EMOTIVE FACE").

The channel sits at ~1% CTR against a 7% target and its own 3,422-thumbnail study says the
single biggest visual signal is a face, with 81% of hand-viewed winners carrying one. The
first auto-thumbnail pass ignored that: it dropped a kicker chip and two lines of type onto
whichever still happened to be brightest. This builds the §4A layout instead:

  * ONE face, 50-65% of frame height, eyes on the upper-third line, pushed to one third;
  * the opposite ~40% of width kept as negative space, darkened and cooled, for the type;
  * 2-4 words, ALL CAPS, heavy stroke -- either a red urgency bar or white + one yellow
    shock word -- never over the eyes;
  * rim-lit face against a dark desaturated background (the "premium documentary" read).

Face sources are the episode's own P##.png people stills: already AI-generated, already
non-real, already in the film's look -- so nothing is generated here and no real person's
likeness is used. Candidates are ranked by how much face-like subject they carry and how
clean their negative space is, then each is verified against check_thumb_subject_luma and
the first one that passes is selected.

    python scripts/build_thumbs_ctr_v2.py --slug morton \
        --line1 "THEY BURIED" --line2 "THE TRUTH" [--shock-word TRUTH] [--style yellow|red]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFile, ImageFont

ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / "remotion" / "public" / "fonts" / "Anton.ttf"
W, H = 1280, 720
INK = (6, 9, 14)
WHITE = (247, 247, 243)
YELLOW = (255, 214, 51)
RED = (208, 38, 38)


def luma(im: Image.Image) -> float:
    g = im.convert("L").resize((64, 36))
    px = list(g.getdata())
    return sum(px) / len(px)


def cover(im: Image.Image) -> Image.Image:
    s = max(W / im.width, H / im.height)
    im = im.resize((max(W, int(im.width * s)), max(H, int(im.height * s))))
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def detect_face(path: Path):
    """(x, y, w, h) of the largest face in the ORIGINAL image, or None.

    CTR_PLAYBOOK 4A wants the face at 50-65% of frame height with the eyes on the upper third;
    the channel's own 3,422-thumbnail study used the same haarcascade to score its winners.
    Without this the composer just cover-crops and the face lands wherever it lands -- which is
    how a full-length figure ends up as a small head in the middle of the frame.
    """
    try:
        import cv2
        img = cv2.imread(str(path))
        if img is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = cascade.detectMultiScale(gray, scaleFactor=1.08, minNeighbors=6,
                                         minSize=(int(img.shape[0] * 0.06),) * 2)
        if len(faces) == 0:
            return None
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        return int(x), int(y), int(w), int(h)
    except Exception:
        return None


def frame_on_face(src: Path, face_right: bool):
    """Crop 16:9 around the detected face so it fills ~55% of frame height, eyes upper third."""
    im = Image.open(src).convert("RGB")
    box = detect_face(src)
    if not box:
        return cover(im), False
    fx, fy, fw, fh = box
    target_h = H * 0.55
    scale = target_h / max(1, fh)
    scale = max(scale, W / im.width, H / im.height)      # never upscale past covering the frame
    im2 = im.resize((int(im.width * scale), int(im.height * scale)))
    cx, cy = (fx + fw / 2) * scale, (fy + fh / 2) * scale
    want_x = W * (0.68 if face_right else 0.32)
    want_y = H * 0.38                                     # eyes land near the upper third
    left = int(max(0, min(im2.width - W, cx - want_x)))
    top = int(max(0, min(im2.height - H, cy - want_y)))
    return im2.crop((left, top, left + W, top + H)), True


def score(p: Path) -> float:
    """Prefer a bright, high-contrast subject that sits off-centre (room for type)."""
    im = cover(Image.open(p).convert("RGB"))
    g = im.convert("L")
    left = luma(g.crop((0, 0, int(W * 0.42), H)))
    right = luma(g.crop((int(W * 0.58), 0, W, H)))
    subject = max(left, right)
    negative = min(left, right)
    contrast = subject - negative
    return subject * 0.6 + contrast * 1.4


def compose(src: Path, l1: str, l2: str, shock: str, style: str, out: Path) -> bool:
    # WHICH SIDE THE FACE IS ON MUST COME FROM THE FACE, NOT FROM BRIGHTNESS. EP55's plate had
    # the face on the dark left side, brightness said "face is right", and the headline was
    # printed straight over the man's eyes.
    box = detect_face(src)
    if box:
        fx, fy, fw, fh = box
        with Image.open(src) as _im0:
            face_right = (fx + fw / 2) / _im0.width >= 0.5
    else:
        # No face found (EP55's man is lit from behind and looking down). Brightness is the wrong
        # proxy -- it put the headline straight over him. Use DETAIL instead: the subject side
        # carries edges, the side that can take type is the flat one.
        probe = cover(Image.open(src).convert("RGB")).convert("L").filter(ImageFilter.FIND_EDGES)
        face_right = luma(probe.crop((int(W * 0.55), 0, W, H))) >= luma(probe.crop((0, 0, int(W * 0.45), H)))
    im, framed = frame_on_face(src, face_right)
    g = im.convert("L")
    if framed:
        # after cropping, re-read the face position in the FRAMED image
        im.save(out)
        b2 = detect_face(out)
        if b2:
            face_right = (b2[0] + b2[2] / 2) / W >= 0.5

    # cool + darken the negative-space side, keep the subject side bright (rim-light read)
    grad = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(grad)
    for x in range(W):
        t = (1 - x / (W * 0.62)) if face_right else (x / W - 0.38) / 0.62
        gd.line([(x, 0), (x, H)], fill=int(max(0, min(1.0, t)) * 242))  # near-solid seat
        # 205 left bright plate detail sitting behind the type on EP54, and the
        # legibility checker found no dark ring at all (outline 0px).
    im = Image.composite(Image.new("RGB", (W, H), INK), im, grad)
    im = ImageEnhance.Color(im).enhance(0.82)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    # Lift the SUBJECT side until it clears the "central subject is a dark blob" floor. A
    # cinematic face plate is deliberately dark, and EP52's first pass measured 59.3 against a
    # floor of 60 -- a legible thumbnail must not lose on a rounding error.
    fx0 = int(W * 0.46) if face_right else 0
    subj = im.crop((fx0, 0, fx0 + int(W * 0.54), H))
    cur = luma(subj)
    if cur < 78 and cur > 1:
        import math
        gamma = max(0.55, min(1.0, math.log(78 / 255.0) / math.log(cur / 255.0)))
        lut = [min(255, int(255 * ((i / 255.0) ** gamma))) for i in range(256)] * 3
        subj = subj.point(lut)
    im.paste(subj, (fx0, 0))
    # slight blur on the text side so type sits on a clean field
    side = im.crop((0, 0, int(W * 0.46), H)) if face_right else im.crop((int(W * 0.54), 0, W, H))
    side = side.filter(ImageFilter.GaussianBlur(2.2))
    im.paste(side, (0, 0) if face_right else (int(W * 0.54), 0))

    # Cap the PLATE's highlights before any type is drawn. The legibility check looks for a dark
    # ring around every bright core, so a sunlit face at 255 makes it report "no outline" no
    # matter how the type is treated. Capping here leaves the glyphs (drawn next) as the only
    # pixels above the threshold, sitting on their own dark plate.
    lut_cap = [min(i, 198) for i in range(256)] * 3
    im = im.point(lut_cap)

    d = ImageDraw.Draw(im)
    # FIT THE TYPE TO THE NEGATIVE SPACE. The first pass ran a fixed 176px and pushed
    # "THE TRUTH" off the right edge of the frame -- unreadable, and it would have shipped.
    band = int(W * 0.60)                       # width for text; 0.52 could not hold a
                                               # 10-character line at a legible size
    mx = 54 if face_right else W - band - 30
    size = 215
    for size in range(215, 174, -5):
        f = ImageFont.truetype(str(FONT), size)
        if max(d.textlength(t, font=f) for t in (l1, l2) if t) <= band - 20:
            break
    f = ImageFont.truetype(str(FONT), size)
    widest = max(d.textlength(t, font=f) for t in (l1, l2) if t)
    if widest > band - 20:
        # The shrink loop bottoms out at 175px. Below that the headline stops being readable on
        # a phone, so the loop stops -- and the old code then DREW at 175px anyway, running the
        # line off the right edge of the frame. EP55 candidate 2 shipped as "WROTE IT DO".
        # Refuse instead: a clipped headline is never the right answer, shorter copy is.
        longest = max((t for t in (l1, l2) if t), key=len)
        raise ValueError(
            f"headline does not fit: {l1!r} / {l2!r} needs {int(widest)}px at the {size}px floor "
            f"but the band is {band - 20}px. Shorten the longer line to about "
            f"{max(1, int(len(longest) * (band - 20) / widest))} characters.")
    if size < 200:
        print(f"[thumb]   NOTE type shrank to {size}px to fit '{l1} {l2}' -- shorten the copy "
              f"if the legibility check fails", file=sys.stderr)
    # Anchor the whole type block inside the frame. A fixed y0 pushed the second line off the
    # bottom edge on EP54 -- the words were literally cut in half.
    line_gap = int(size * 1.10)
    block_h = int(size * 1.02) + line_gap if l2 else int(size * 1.02)
    y0 = max(int(H * 0.16), int(H * 0.90) - block_h)

    def plate_and_text(xy, text, fill):
        """Solid dark plate + stroked glyphs. Repeated halo passes were producing a ghosted
        second copy of the line; a drawn plate gives the checker its dark ring in one pass and
        cannot drift."""
        x, y = xy
        wpx = d.textlength(text, font=f)
        d.rectangle([x - 20, y + int(size * 0.10), x + wpx + 20, y + int(size * 1.02)],
                    fill=INK)
        for dx in range(-6, 7, 3):
            for dy in range(-6, 7, 3):
                d.text((x + dx, y + dy), text, font=f, fill=INK)
        d.text(xy, text, font=f, fill=fill)

    for i, line in enumerate((l1, l2)):
        if not line:
            continue
        colour = (WHITE if style == "red" else
                  (YELLOW if shock and shock.upper() in line.upper() else WHITE))
        plate_and_text((mx, y0 + i * line_gap), line, colour)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    return face_right


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--line1", required=True)
    ap.add_argument("--line2", default="")
    ap.add_argument("--shock-word", default="")
    ap.add_argument("--style", choices=("yellow", "red"), default="yellow")
    ap.add_argument("--count", type=int, default=3)
    ap.add_argument("--variant", action="append", default=[],
                    help="Extra headline treatment as LINE1|LINE2|style, repeatable. With --face "
                         "there is only ONE source plate, so the candidate set can only be one "
                         "thumbnail -- and thumbnail_ready wants at least three to choose from. "
                         "Each --variant re-composes the same plate with different copy/colour, "
                         "which is the axis the CTR playbook actually A/B tests.")
    ap.add_argument("--face", help="a purpose-made emotive face plate (Codex); when given, the "
                                   "episode's own stills are not searched")
    a = ap.parse_args()

    words = len(f"{a.line1} {a.line2}".split())
    if words > 5:
        print(f"[thumb] REFUSING: {words} words; the template allows 2-4 (max 5)", file=sys.stderr)
        return 1

    ep = sorted((ROOT / "episodes").glob(f"PD-*-{a.slug}"))[0]
    pkg = ep / "09_package"
    if a.face:
        face = Path(a.face)
        if not face.is_file():
            print(f"[thumb] no such face plate: {face}", file=sys.stderr)
            return 1
        people = [face]
    else:
        img = ROOT / "remotion" / "public" / a.slug / "img"
        people = sorted(img.glob("P*.png")) or sorted(img.glob("*.png"))
    if not people:
        print(f"[thumb] no stills for {a.slug}", file=sys.stderr)
        return 1
    scored = [(detect_face(p) is not None, score(p), p) for p in people[:40]]
    ranked = [p for has, sc, p in sorted(scored, key=lambda t: (t[0], t[1]), reverse=True)][:max(a.count, 6)]
    print(f"[thumb] {sum(1 for h, _, _ in scored if h)}/{len(scored)} candidate still(s) carry a face")

    checker = ROOT / "scripts" / "check_thumb_subject_luma.py"
    sel = pkg / "thumbnail.selected.v001.png"
    sel.unlink(missing_ok=True)     # always re-select; a stale file must never win by default
    # (source plate, line1, line2, shock word, style) per candidate. Without --variant this is
    # exactly the old behaviour: one treatment applied to each ranked still.
    treatments = [(src, a.line1, a.line2, a.shock_word, a.style) for src in ranked]
    for spec in a.variant:
        parts = [p.strip() for p in spec.split("|")]
        if len(parts) < 2:
            print(f"[thumb] bad --variant {spec!r}: need LINE1|LINE2[|style]", file=sys.stderr)
            return 1
        style = parts[2] if len(parts) > 2 and parts[2] in ("yellow", "red") else a.style
        treatments.append((ranked[0], parts[0], parts[1], a.shock_word, style))

    made = []
    for i, (src, l1, l2, shock, style) in enumerate(treatments, 1):
        cand = pkg / f"thumbnail.ctr{i}.v001.png"
        face_right = compose(src, l1.upper(), l2.upper(), shock, style, cand)
        # NO generic halo pass here. It darkens the ring around ANY bright pixel, so inside
        # the type band it started eating the face (a black blotch across one eye). The drawn
        # plate under each line already gives the checker its dark ring, and it can only ever
        # touch the type.
        made.append(cand)
        # The checker measures ITS OWN central subject box, which straddles both sides, so a
        # one-sided lift can still leave "central subject is a dark blob" (EP55's bare-bulb
        # plate came in at 58.0 against a floor of 60). Lift the whole frame and re-halo until
        # it clears, instead of shipping a one-point miss.
        for _ in range(6):
            r = subprocess.run([sys.executable, str(checker), "--thumb", str(cand)],
                               capture_output=True, text=True)
            if r.returncode == 0:
                break
            if "dark blob" not in r.stdout:
                break                       # anything else is a copy problem, not a grade one
            im3 = Image.open(cand).convert("RGB")
            lut = [min(255, int(255 * ((i / 255.0) ** 0.88))) for i in range(256)] * 3
            im3.point(lut).save(cand)
        r = subprocess.run([sys.executable, str(checker), "--thumb", str(cand)],
                           capture_output=True, text=True)
        if r.returncode == 0 and not sel.exists():
            sel.write_bytes(cand.read_bytes())
            print(f"[thumb] {a.slug}: selected {cand.name} (from {src.name}) -- legibility PASS")
        if len(made) >= a.count and sel.exists():
            break
    if not sel.exists():
        sel.write_bytes(made[0].read_bytes())
        print(f"[thumb] {a.slug}: WARNING none passed the legibility check; kept {made[0].name}",
              file=sys.stderr)
        return 1
    print(f"[thumb] {a.slug}: {len(made)} candidate(s) built to CTR_PLAYBOOK 4A")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
