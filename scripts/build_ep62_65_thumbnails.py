#!/usr/bin/env python3
"""Composite the EP62-65 thumbnails: the commissioned plate plus its headline and kicker.

check_final_acceptance fails an episode with fewer than three 1280x720 candidates and no selection.
All four episodes have their plates and their wording already -- the plates were ordered with the
upper third left clear and a brightness override, and 04_scenes/thumb_prompts.v001.md carries the
kicker and the two-line headline for each. This puts one on the other.

Deliberately not Remotion: these are static compositions of an image and two text blocks, and a
bundle takes longer than the render. The type follows the design doc -- headline uppercase, two
lines maximum, cap height at least 78 px at 1280x720; kicker a filled tag of three words or fewer.

    py scripts/build_ep62_65_thumbnails.py            # all four
    py scripts/build_ep62_65_thumbnails.py --slug greene
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
W, H = 1280, 720
GOLD, RED, BLUE, WHITE = "#E5B53A", "#D22628", "#1F6BFF", "#F2F0EA"

# An optional 5th element on a row places the type somewhere other than the default top-left
# block. Keys (all optional):
#   crop (x, y, w) native pixels cropped off the plate BEFORE the 16:9 fit -- reframes the picture
#   gain float      multiply every pixel by this and clip at 255, AFTER the resize and BEFORE cap.
#                   The canonical [STYLE] the body plates were commissioned under says "low
#                   contrast, low-key", which is right for a film and wrong for a thumbnail: it is
#                   why every greene/correa candidate came out grey. The T00x plates for EP66-69
#                   were ordered under a thumbnail-only [TSTYLE] (one hard key, high contrast,
#                   bright) and need no gain; a body plate pressed into thumbnail service does.
#   cap  int        roll every pixel down until the 99.9th percentile luma sits at this value
#   box  (x0,y0,x1,y1) at 1280x720: the type lives inside this rectangle and the full-width scrim
#                   is not drawn. Default (0,0,1280,720) reproduces the original layout exactly.
#   scrim (frac, alpha) | None   the black wash under the type. Default (0.66, 120) reproduces the
#                   original layout. A plate whose upper band was commissioned EMPTY does not need
#                   two thirds of itself darkened -- that is what made the marmet 01-04 set dull --
#                   so those rows pass a shallower, or no, scrim. Ignored when `box` is set.
# `cap` exists because check_thumb_subject_luma measures the dark ring around EVERY core brighter
# than 200, not just around the glyphs. A pale institutional wall sits at 206 and is itself a core
# whose ring is equally pale, so an otherwise perfect bright plate scores outline 0 and hard-fails.
# Capping the picture at 195 leaves the burned-in headline as the only bright core in the frame.
R234_LAYOUT = {"crop": (600, 300, 3200), "cap": 185, "box": (470, 0, 1280, 720)}

# The same `cap`, with no reframing, for any plate the THUMBNAIL BRIEF deliberately made bright:
# EP67-69 were commissioned with "the bottom third the brightest part of the picture", so the desk /
# the concrete / the machined steel all sit above 200 and are themselves cores with bright rings.
# Measured 2026-08-11 on the first build of thumbnail.selected.v001: outline scored 0 for ramirez,
# pinto and hyatt while subject luma and text height passed comfortably. Capping the PICTURE leaves
# the burned-in headline as the only core over 200 and the outline becomes measurable again.
# openfields is NOT capped -- its plates are flat overcast and it passed at outline 20 uncapped.
CAP_ONLY = {"cap": 185}

# plate, kicker, headline lines, accent[, layout] -- all from each episode's thumb_prompts.v001.md
SPEC: dict[str, tuple[str, list[tuple]]] = {   # row = (plate, kicker, headline, accent[, layout])
    # 2026-08-11 re-order of greene and correa. Both sets were built before the font fix (so every
    # one of them is Arial Bold, not Anton) and every plate in both is a body plate shot under the
    # low-contrast [STYLE] -- opening all nine candidates, they are uniformly grey rooms and grey
    # doors. Neither episode has a PACKAGING document, so the wording below is written here, from
    # each episode's FACTS_LEDGER, and every claim is cited in the comment above its row.
    #
    # greene row 1 is the only plate in 316 that puts a legible human face next to the object the
    # case is about: G271 is a woman at her own front door with nothing on it. The type goes in a
    # right-hand box so it does not land on her face -- the marmet R234 arrangement, which is the
    # standard this channel has agreed on.
    "greene": ("PD-2026-062-greene", [
        # GL-24 (their account): they "did not learn of the eviction proceedings until they were
        # served with writs of possession". Badge: service was made by posting on the door, which
        # is the Kentucky practice the case is about.
        # "SHE NEVER KNEW" needs three lines in a 580px column; at a pitch tight enough to
        # leave room for the badge the glyphs collide. Two short words hold the same claim, fit at
        # the 248 ceiling, and leave the bar clear space underneath.
        ("G271", "POSTED ON THE DOOR", ["NEVER TOLD"], GOLD,
         {"gain": 1.30, "box": (620, 0, 1280, 720)}),
        # the original row 1, kept as a candidate: now in Anton and lifted out of the grey
        ("G242", "STILL SERVED", ["NOBODY", "WAS HOME"], GOLD, {"gain": 1.18}),
        # opinion n.7 (App. 80, 82): process servers described children at Village West pulling
        # posted writs off the doors.
        ("G204", "CHILDREN TOOK THEM", ["TAPED", "TO THE DOOR"], RED, {"gain": 1.25}),
        ("G220", "THAT WAS SERVICE", ["THIS COUNTED", "AS NOTICE"], GOLD, {"gain": 1.45}),
    ]),
    # correa row 1: C001 is the only plate that holds the ticket AND the room full of people
    # waiting in one frame. The scrim is pulled back to the top half so the waiting room keeps its
    # own light below the type instead of being washed flat, which is what made the old set dull.
    "correa": ("PD-2026-063-correa", [
        # CR-09 (verbatim): "a Hospital employee assigned the patient a number (forty-seven)".
        # CR-11 (verbatim): at roughly 2:15 p.m. "he heard an attendant calling patient number
        # twenty-four for treatment." Two separate facts, no shared content word.
        ("C001", "THEY CALLED 24", ["NUMBER 47"], GOLD, {"gain": 1.35, "scrim": (0.50, 135)}),
        # CR-14: she was never seen by a physician at HSF -- no examination, no vital signs, no chart.
        ("C221", "SHE WAS NEVER SEEN", ["NUMBER", "47"], RED, {"gain": 1.30, "scrim": (0.46, 130)}),
        # CR-14 again for the record ("utter inability to produce any records"); TL-12 for the span.
        ("C227", "TWO HOURS", ["NO RECORD", "AT ALL"], GOLD, {"gain": 1.35, "scrim": (0.58, 130)}),
        ("C239", "NEVER EXAMINED", ["NOBODY", "SAID NO"], BLUE, {"gain": 1.40}),
    ]),
    "memphis": ("PD-2026-064-memphis", [
        # M208 first: the plate review ACCEPTed it as the only candidate meeting all three
        # requirements and FLAGged M219 because the sheets occupy the upper third. Opening both
        # agrees -- M219 never shows the two bills the hook is about.
        ("M208", "TWO METER SETS", ["BOTH WERE", "RUNNING"], GOLD),
        ("M219", "ONE HOUSE", ["ONE LETTER", "APART"], GOLD),
        ("M209", "SAME HOUSE", ["TWO BILLS", "EVERY MONTH"], RED),
        ("M235", "AFTER FINAL NOTICE", ["GIVEN NO", "SATISFACTION"], BLUE),
    ]),
    # 2026-08-11 re-order. The four R217-R224 plates were all text over a blurred sheet of
    # paper -- the "サムネが地味" reject class -- and R224 also repeated its own headline in its
    # kicker. EP65_marmet_CODEX_THUMBS.v001.md sec.4.3 replaces them with six pictures whose
    # kickers each add a SECOND fact the headline does not state (zero content-word overlap).
    # R234 additionally carries a layout: the plate is reframed so the man sits left and the
    # headline gets the bare right wall, instead of being stamped across his face.
    "marmet": ("PD-2026-065-marmet", [
        ("R234", "AUTHORITY NEVER DECIDED", ["SIGNED FOR", "SOMEONE ELSE"], GOLD, R234_LAYOUT),
        ("R238", "NO EXCEPTIONS",           ["ONE FORM", "WAS DIFFERENT"],  RED),
        ("R237", "NOTHING WAS ORDERED",     ["VACATED,", "NOT UPHELD"],     BLUE),
        ("R236", "IN THE CAPTION",          ["ONLY ONE", "PATIENT NAMED"],  GOLD),
        ("R239", "WEST VIRGINIA SAID",      ["CREATED FROM", "WHOLE CLOTH"], GOLD),
        ("R235", "SAME SENTENCE",           ["EVERY DISPUTE", "BUT ONE"],   BLUE),
    ]),
    # 2026-08-11 EP66-69. Plates and wording from each episode's
    # `episodes/_planning/EP6*_*_PACKAGING.v001.md` §2 variant list. Row 1 is what ships: build()
    # copies made[0] to thumbnail.selected, so the selection is the FIRST row, not the best-named.
    # Every kicker below carries a SECOND fact with zero content-word overlap with its headline
    # (see `_check_badge_overlap`, which fails the build rather than trusting the eye).
    #
    # openfields uses L255-L260, not T001-T006: this episode's thumbnail plates were ordered inside
    # its own L-series (BATCH_B §5 "THUMB"), and all six are `accept` in
    # runs/qc/openfields_plate_verdicts.v001.json after the batch-D reshoot.
    "openfields": ("PD-2026-066-openfields", [
        # L256 is the trail camera strapped to a trunk -- the only plate where the picture IS the
        # story the title tells, and 78 DAYS is the same case as the title's suffix (PA-13).
        ("L256", "NOBODY WAS TOLD", ["78 DAYS"],            GOLD),
        ("L255", "GATED. POSTED.",  ["ENTERED", "ANYWAY"],  RED),
        ("L258", "NO CONSENT",      ["NO", "WARRANT"],      BLUE),
        ("L259", "SINCE 2013",      ["15 TO 22", "TIMES"],  GOLD),
    ]),
    "ramirez": ("PD-2026-067-ramirez", [
        ("T002", "NO OTHER CHECK",  ["NAME", "ONLY"],           RED,  CAP_ONLY),
        ("T001", "FIRST AND LAST",  ["A TERRORIST", "LIST"],    GOLD, CAP_ONLY),
        ("T003", "6,332 FILES",     ["NEVER", "SENT"],          GOLD, CAP_ONLY),
        ("T005", "ONE CHECK EACH",  ["8,185", "NAMES"],         BLUE, CAP_ONLY),
    ]),
    # pinto T003 is a REJECT in runs/qc/pinto_plate_verdicts.v001.json (it is the whole car
    # underside side-on, with no machinist's rule and no differential-to-tank gap) and is being
    # regenerated; T004 is the accepted framing that does carry the rule across the gap.
    "pinto": ("PD-2026-068-pinto", [
        ("T006", "IT WAS ROLLOVER",   ["WRONG", "MEMO"],           RED,  CAP_ONLY),
        ("T004", "BEHIND THE AXLE",   ["9 OR 10", "INCHES"],       GOLD, CAP_ONLY),
        ("T001", "NOT ONE PINTO",     ["11 MILLION", "CARS"],      GOLD, CAP_ONLY),
        ("T005", "EXCLUDED AT TRIAL", ["NEVER IN", "EVIDENCE"],    BLUE, CAP_ONLY),
    ]),
    # hyatt T003 = the rod through the box-section web, recommended by the plate reviewer as the
    # one frame where the picture is the story; it is also hero object H1+H2 in one still.
    # 2026-08-11: the designed headline "A NUT AND A WASHER" wraps to two lines, and two lines of
    # Anton at 248 cover the beam, the rod and the nut -- the plate stops being a picture and
    # becomes a text card, which throws away the reason T003 was chosen. "DOUBLED" is one line at
    # the same ink height (PACKAGING §2 measured it at 218 px), leaves the whole assembly visible,
    # and is the federal report's own word for what the change did, used twice as a conclusion.
    "hyatt": ("PD-2026-069-hyatt", [
        ("T003", "114 PEOPLE",     ["DOUBLED"],                  GOLD, CAP_ONLY),
        ("T001", "SAME STEEL",     ["ONE ROD", "TWO RODS"],      RED,  CAP_ONLY),
        ("T005", "NOBODY CHECKED", ["NEVER", "CALCULATED"],      GOLD, CAP_ONLY),
        ("T004", "AS BUILT",       ["68 REQUIRED", "18.6 THERE"], BLUE, CAP_ONLY),
    ]),
}

# Several EP62-65 thumbnails shipped with the badge repeating the headline word for word
# ("NO RECORD AT ALL" over a badge reading "NO RECORD"), which wastes the only place a second fact
# can go. The rule is zero CONTENT-word overlap; function words and pure punctuation do not count.
_STOPWORDS = {"a", "an", "and", "the", "of", "to", "in", "on", "at", "for", "is", "was", "were",
              "it", "its", "no", "not", "or", "but", "as", "be", "by", "with", "one", "two"}


def _words(s: str) -> set[str]:
    import re as _re
    return {w for w in _re.findall(r"[A-Za-z0-9][A-Za-z0-9,.']*", s.upper())
            if w.lower() not in _STOPWORDS}


def check_badge_overlap() -> list[str]:
    """Every (headline, kicker) pair must share no content word. Returns the violations."""
    bad = []
    for slug, (_epid, rows) in SPEC.items():
        for row in rows:
            plate, kicker, head = row[0], row[1], row[2]
            shared = _words(" ".join(head)) & _words(kicker)
            if shared:
                bad.append(f"{slug}/{plate}: headline {' '.join(head)!r} and badge {kicker!r} "
                           f"share {sorted(shared)}")
    return bad


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    # 2026-08-11: the repo ships remotion/public/fonts/Anton.ttf and Oswald.ttf -- NOT
    # "Anton-Regular.ttf" / "Oswald-Bold.ttf". Every thumbnail built before today therefore fell
    # through to Arial Bold. Arial is wide, so marmet R234 and R239 missed the 150px ink floor at
    # every line break; Anton clears it at the same line width. Real names first, old names kept.
    for name in (("Anton.ttf", "Anton-Regular.ttf", "Oswald-Bold.ttf", "arialbd.ttf", "arial.ttf")
                 if bold else ("Oswald.ttf", "Oswald-Regular.ttf", "arial.ttf")):
        for d in (ROOT / "remotion/public/fonts", Path("C:/Windows/Fonts")):
            p = d / name
            if p.is_file():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def build(slug: str, epid: str, plate: str, kicker: str, headline: list[str],
          accent: str, n: int, layout: dict | None = None) -> Path | None:
    src = Path(f"H:/pd-media/assets/ai/{slug}/{plate}.png")
    if not src.is_file():
        print(f"  {plate}: plate missing"); return None
    im = Image.open(src).convert("RGB")
    layout = layout or {}
    if "crop" in layout:
        cx, cy, cw = layout["crop"]
        im = im.crop((cx, cy, cx + cw, cy + round(cw * H / W)))
    # cover-crop to 16:9 then down to 1280x720
    tw, th = W / H, im.width / im.height
    if th > tw:
        nw = int(im.height * tw)
        im = im.crop(((im.width - nw) // 2, 0, (im.width + nw) // 2, im.height))
    else:
        nh = int(im.width / tw)
        im = im.crop((0, (im.height - nh) // 2, im.width, (im.height + nh) // 2))
    im = im.resize((W, H), Image.LANCZOS)

    if "gain" in layout:
        # The body [STYLE] is "low contrast, low-key". That is the right instruction for a film and
        # the wrong one for a thumbnail, and it is why every greene and correa candidate came out
        # grey. These plates cannot be re-commissioned from here (the GPU is busy and long-form
        # images are Codex's), so the exposure is lifted at composite time instead. Scale-and-clip,
        # not a curve: it keeps the relative tones and simply moves the whole picture up.
        # A LINEAR multiply is the wrong shape here and measurably fails: it drags the
        # highlights past 200, which makes the picture itself a bright core with a bright ring, and
        # check_thumb_subject_luma scored outline 0 on both episodes (greene v009, correa v006,
        # measured 2026-08-11). Combining it with `cap` does not help either -- cap rescales by
        # 185/peak, which cancels the gain almost exactly. So: raise the MIDTONES with a gamma and
        # hold the ceiling under the gate's 200 core threshold with a hard clip. The picture gets
        # brighter, the burned-in headline stays the only core, and the outline stays measurable.
        import numpy as np
        arr = np.asarray(im, dtype=np.float64) / 255.0
        arr = np.power(arr, 1.0 / float(layout["gain"])) * 255.0
        im = Image.fromarray(np.clip(arr, 0, 196).astype("uint8"), "RGB")

    if "cap" in layout:
        # See R234_LAYOUT: leave the burned-in headline as the only core brighter than 200 so the
        # outline gate can find a dark ring around it. Scaling (rather than clipping) keeps the
        # tonal relationships, so the picture stays bright instead of turning grey.
        import numpy as np
        arr = np.asarray(im, dtype=np.float64)
        peak = float(np.percentile(0.299 * arr[..., 0] + 0.587 * arr[..., 1]
                                   + 0.114 * arr[..., 2], 99.9))
        if peak > layout["cap"]:
            arr = arr * (layout["cap"] / peak)
        # scaling the 99.9th percentile still leaves a handful of speculars above 200; ONE of them
        # is a core with a bright ring and drags the whole outline measurement to 0. Clip the tail.
        im = Image.fromarray(np.clip(arr, 0, 198).astype("uint8"), "RGB")

    d = ImageDraw.Draw(im, "RGBA")
    bx0, by0, bx1, by1 = layout.get("box", (0, 0, W, H))
    if "box" not in layout:
        # a scrim under the type only, so the picture keeps its own light
        scrim = layout.get("scrim", (0.66, 120))
        if scrim:
            frac, alpha = scrim
            d.rectangle([0, 0, W, int(H * frac)], fill=(0, 0, 0, alpha))

    # thumb_subject_luma measures the tallest connected bright component and wants >= 150 px at
    # 1280, so the headline has to be physically tall, not merely "big". Shrinking to fit the
    # width fought that: marmet's "THE DEATH CLAIM" pushed the size down to 132, whose ink
    # measures 97 px, and acceptance failed. Wrapping to one more line shortens every line, which
    # lets the type be LARGER. Try two lines and three, keep the tallest ink that fits.
    words = " ".join(headline).split()
    # default box (0,0,W,H) reproduces the original constants exactly: MARGIN 40, MAXW 1200,
    # first baseline at 26, vertical budget H-26-88 for the lines above the kicker bar.
    MARGIN, MAXW, MAXLINES = bx0 + 40, (bx1 - bx0) - 80, 3
    TOP, VBUDGET = by0 + 26, (by1 - by0) - 26 - 88

    def splits(ws: list[str], maxlines: int) -> list[list[str]]:
        """Every way to break these words into 1..maxlines contiguous lines.

        Greedy filling always produced "ONE KNOCK" / "WAS ENOUGH" for greene, and the width of
        the second line capped the size 5px under the floor. A headline is four or five words,
        so the whole search space is a few dozen options -- measure them instead of guessing.
        """
        out: list[list[str]] = [[" ".join(ws)]]
        n = len(ws)
        for i in range(1, n):
            out.append([" ".join(ws[:i]), " ".join(ws[i:])])
            if maxlines >= 3:
                for j in range(i + 1, n):
                    out.append([" ".join(ws[:i]), " ".join(ws[i:j]), " ".join(ws[j:])])
        return out

    # A narrow right-hand box cannot hold three lines at the 150px ink floor AND the badge at the
    # default 0.94 pitch: greene G271 fitted at 214, and the badge was drawn at y=724, four pixels
    # off the bottom of the frame -- silently throwing away the only place the second fact lives.
    # Anton's cap height is ~0.73 of its size, so 0.94 is loose leading; a row that needs the room
    # can tighten it. Default unchanged, so every existing row composes exactly as before.
    PITCH = layout.get("pitch", 0.94)
    best: tuple[int, list[str], int] | None = None
    for lines in splits(words, MAXLINES):
        for size in range(248, 96, -2):   # 2px steps: a 4px step landed marmet R234 on ink 149/150
            f = font(size)
            if max(d.textlength(l, font=f) for l in lines) > MAXW:
                continue
            if len(lines) * int(size * PITCH) > VBUDGET:
                continue
            ink = max(f.getbbox(l)[3] - f.getbbox(l)[1] for l in lines)
            if best is None or ink > best[2]:
                best = (size, lines, ink)
            break
    if best is None:
        print(f"  {plate}: headline does not fit at any size"); return None
    size, lines, ink = best
    if ink < 150:
        print(f"  {plate}: WARNING ink {ink}px < 150px floor -- acceptance will fail this")
    fh = font(size)
    y, bottom = TOP, TOP
    for line in lines:
        d.text((MARGIN, y), line, font=fh, fill=WHITE,
               stroke_width=max(14, size // 14), stroke_fill=(0, 0, 0, 235))
        # Anton's ink runs well past 0.94*size, so a fixed pitch put the kicker bar THROUGH the
        # last line. Track where the ink actually ends and hang the bar off that.
        bottom = max(bottom, y + fh.getbbox(line)[3] + max(14, size // 14))
        y += int(size * PITCH)
    y = bottom - 10
    # Last-resort clamp: a badge drawn past the bottom edge is never the right answer. If the ink
    # still overruns, pull the bar back inside the frame rather than composing it off-canvas.
    y = min(y, H - 88)

    fk = font(46)
    while d.textlength(kicker, font=fk) + 40 > MAXW and fk.size > 22:
        fk = font(fk.size - 2)          # a narrow box must not push the tag off the frame
    kw = d.textlength(kicker, font=fk)
    d.rectangle([MARGIN + 8, y + 10, MARGIN + 8 + kw + 40, y + 10 + 68], fill=accent)
    d.text((MARGIN + 28, y + 22), kicker, font=fk, fill="#0B0B0B")

    out_dir = ROOT / "episodes" / epid / "09_package"
    out_dir.mkdir(parents=True, exist_ok=True)
    # Invariant 6: never overwrite an existing candidate. marmet 01-04.v001 are the retired
    # blurred-paper set and stay on disk to compare against, so a re-run lands on the next free
    # revision instead of clobbering them.
    r = 1
    while (out_dir / f"thumbnail.{slug}.{n:02d}.v{r:03d}.png").exists():
        r += 1
    out = out_dir / f"thumbnail.{slug}.{n:02d}.v{r:03d}.png"
    im.save(out)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", choices=sorted(SPEC))
    a = ap.parse_args()
    for slug in ([a.slug] if a.slug else list(SPEC)):
        epid, rows = SPEC[slug]
        print(f"=== {slug}")
        made = []
        for i, row in enumerate(rows, 1):
            plate, kicker, head, accent = row[:4]
            p = build(slug, epid, plate, kicker, head, accent, i,
                      row[4] if len(row) > 4 else None)
            if p:
                made.append(p)
                print(f"  {p.name}  <- {plate}  {' / '.join(head)}")
        if made:
            # Invariant 6: an approved artefact is never overwritten. The uploader takes the
            # HIGHEST thumbnail.selected.v*.png, so a new revision is what ships and the earlier
            # selection stays on disk to compare against.
            n = 1
            while (made[0].parent / f"thumbnail.selected.v{n:03d}.png").exists():
                n += 1
            sel = made[0].parent / f"thumbnail.selected.v{n:03d}.png"
            shutil.copy2(made[0], sel)
            print(f"  selected -> {sel.name}  <- {made[0].name}  ({len(made)} candidate(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
