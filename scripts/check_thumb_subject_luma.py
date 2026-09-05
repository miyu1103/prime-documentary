#!/usr/bin/env python3
r"""Independent thumbnail READABILITY gate — the SUBJECT must be legible at 320px, not a dark blob.

check_final_acceptance already floors the WHOLE-THUMB mean luma / contrast (check_thumbnail_visibility).
That whole-frame average is easily satisfied by one bright corner while the actual SUBJECT (the phone,
the face, the number) sits in shadow — exactly the "画面が暗い / しょぼい / CTRが下がる" reject class. On the
real EP31 unlock pair, the whole-thumb mean does NOT separate the rejected dark v001 (35.7) from the
approved v002 (52.8) cleanly, but the SUBJECT region does (center 56.5 vs 78.3). This gate measures the
three things a viewer needs to read a thumbnail shrunk to ~320px in the YouTube feed:

  1. SUBJECT LUMA  — the central subject region (not the whole frame) has mean luma >= 60, so the focal
                     element is not a dark blob. Calibrated on the real pair: rejected v001 = 56.5 (FAIL),
                     approved v002 = 78.3 (PASS).
  2. TEXT HEIGHT   — the tallest 4-CONNECTED COMPONENT of FOREGROUND pixels (near-white text OR a
                     saturated accent number/tag) -- NOT a per-row coverage band -- is >= 150 px when
                     scaled to 1280 w. Connected components reject distributed speckle/noise that a row
                     band miscounts: a fine bright checkerboard (unreadable static) has no 4-adjacency,
                     forms no tall component and scores 0, while real text forms one solid bright blob.
                     150/720 of the frame still reads as ~67 px at a 320-px feed thumbnail. Real pair:
                     v001 = 298, v002 = 315; a tiny-text panel and a bright-speckle gaming probe both = 0.
  3. OUTLINE WIDTH — bright text/subject cores are wrapped by a contrasting DARK rim of >= 12 px (scaled
                     to 1280 w), so elements pop off the background instead of blending in. Measured by
                     dilating the bright core and walking outward while the added ring stays dark.
                     Approved v002 = 19 px; the flat/glow reject v001 = 0 px.

It is deterministic (no clocks, no randomness), reads only numpy + PIL (no cv2/scipy), never writes into
the episode, and NEVER raises on a missing thumbnail — it returns {"skipped": True, "ok": True} so the
acceptance gate is not crashed when the PNG lives on the SSD / is not in the repo.

Honest limits: without OCR the "text height" is the pixel height of the tallest 4-connected bright/accent
component (a big legible element), not glyph metrics, and the outline width is an aggregate dark-ring
measurement, not a per-glyph stroke gauge. Both correctly order the known good/bad pair and reject the
tiny-text, dark-blob and bright-speckle gaming fixtures; neither claims to read the words.

Usage:
  py -3.11 scripts/check_thumb_subject_luma.py --ep PD-2026-031-unlock
  py -3.11 scripts/check_thumb_subject_luma.py --ep PD-2026-031-unlock --dry-run
  py -3.11 scripts/check_thumb_subject_luma.py --ep PD-2026-031-unlock --json out.json
  py -3.11 scripts/check_thumb_subject_luma.py --selftest

Exit code 0 = PASS / skipped / dry-run / selftest-ok, 1 = FAIL or usage error.

check_final_acceptance may import this module and call evaluate(epdir); the result-dict contract
({"check": "thumb_subject_luma", "ok": bool, "hard": bool, "reason": str, ...measured numbers...}) mirrors
the other gate functions in that file — keep the keys stable.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-031-unlock"
CHECK_NAME = "thumb_subject_luma"

# --- thresholds (straight from the spec; each demonstrably met by the APPROVED thumbnail) ----------
REF_WIDTH = 1280                 # heights are reported/floored in this reference frame width
SUBJECT_MIN_LUMA = 60.0          # spec: the SUBJECT region (not whole frame) mean luma floor (0-255)
TEXT_MIN_HEIGHT = 150            # spec: biggest legible foreground element >= 150 px @ 1280 w
OUTLINE_MIN_PX = 12              # spec: contrasting outline/border around bright cores >= 12 px @ 1280 w

# subject region = the conventional central focal box of a thumbnail (fractions of W/H)
SUBJ_X0, SUBJ_X1 = 0.20, 0.80
SUBJ_Y0, SUBJ_Y1 = 0.12, 0.88

# foreground = near-white text OR a saturated accent (red tag / yellow number)
FG_BRIGHT_Y = 190.0              # luma above this reads as white text / bright graphic
FG_ACCENT_SAT = 0.45            # HSV-style saturation above this reads as an accent color
FG_ACCENT_MX = 120.0            # ...and the accent must be reasonably bright (max channel)
# text-height = height of the tallest 4-connected FOREGROUND component (rejects distributed bright
# speckle/noise that a per-row coverage band would miscount as a tall, "readable" element)
FG_MIN_COMPONENT_AREA = 48     # a component smaller than this (native px) is noise, not a legible element
FG_MIN_COMPONENT_W = 4         # ...and it must be at least this wide (native px) so 1-px hairlines don't count

# outline = a DARK rim wrapping the bright core
OUTLINE_CORE_Y = 200.0          # luma above this seeds a bright core (glyph fill / bright subject)
OUTLINE_RING_DARK = 95.0        # a surrounding ring counts as an outline while its mean luma stays below
OUTLINE_MAX_SCAN = 28           # stop dilating after this many rings (native px)


# ---------------------------------------------------------------------------------------------
# thumbnail resolution (mirrors check_final_acceptance.check_thumbnail_visibility)
# ---------------------------------------------------------------------------------------------

def resolve_thumbnail(ep_dir: Path, override: Optional[str] = None) -> Optional[Path]:
    """Newest selected thumbnail PNG, or None if none is present in the repo.

    Mirrors check_thumbnail_visibility: the SELECTED thumbnail is 09_package/thumbnail.selected*.png,
    highest revision wins (sorted()[-1]). Returns None (not an error) when nothing is there."""
    if override:
        p = Path(override)
        return p if p.exists() else None
    sel = sorted((ep_dir / "09_package").glob("thumbnail.selected*.png"))
    return sel[-1] if sel else None


# ---------------------------------------------------------------------------------------------
# pixel measurement (numpy + PIL only; deterministic)
# ---------------------------------------------------------------------------------------------

def _tallest_bright_component_h(fg: "Any", min_area: int, min_w: int) -> int:
    """Native-pixel height of the tallest 4-connected component of True pixels in `fg` that spans at
    least `min_area` pixels and is at least `min_w` pixels wide. Pure numpy union-find (no scipy/cv2).

    This is the connected-components measure the reviewer required: it rejects distributed speckle/noise
    that a per-row coverage band cannot. A fine bright checkerboard has no 4-adjacency, so every pixel is
    its own 1-px component and none clears the area/width floor -> 0. Real text/graphics form one solid
    bright blob whose bounding-box row extent is returned."""
    import numpy as np

    H, W = fg.shape
    if not fg.any():
        return 0
    N = H * W
    idx = np.arange(N, dtype=np.int64).reshape(H, W)
    parent = np.arange(N, dtype=np.int64)

    def _find(x: int) -> int:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    # union 4-connected neighbours (right and down edges cover all adjacencies)
    for adj, (ia, ib) in ((fg[:, :-1] & fg[:, 1:], (idx[:, :-1], idx[:, 1:])),
                          (fg[:-1, :] & fg[1:, :], (idx[:-1, :], idx[1:, :]))):
        if not adj.any():
            continue
        for a, b in zip(ia[adj].tolist(), ib[adj].tolist()):
            ra, rb = _find(a), _find(b)
            if ra != rb:
                parent[rb] = ra

    # flatten every pointer to its root (vectorised pointer-jumping)
    p = parent
    while True:
        nxt = p[p]
        if np.array_equal(nxt, p):
            break
        p = nxt

    fg_ids = idx[fg]
    roots = p[fg_ids]
    rows = fg_ids // W
    cols = fg_ids % W
    minr = np.full(N, H, np.int64)
    maxr = np.full(N, -1, np.int64)
    minc = np.full(N, W, np.int64)
    maxc = np.full(N, -1, np.int64)
    cnt = np.zeros(N, np.int64)
    np.minimum.at(minr, roots, rows)
    np.maximum.at(maxr, roots, rows)
    np.minimum.at(minc, roots, cols)
    np.maximum.at(maxc, roots, cols)
    np.add.at(cnt, roots, 1)
    heights = maxr - minr + 1
    widths = maxc - minc + 1
    valid = (cnt >= min_area) & (widths >= min_w)
    if not valid.any():
        return 0
    return int(heights[valid].max())


def _dilate1(mask: "Any"):
    """Binary dilation by one pixel (4-neighbour), pure numpy."""
    out = mask.copy()
    out[1:, :] |= mask[:-1, :]
    out[:-1, :] |= mask[1:, :]
    out[:, 1:] |= mask[:, :-1]
    out[:, :-1] |= mask[:, 1:]
    return out


def measure(thumb: Path) -> dict[str, Any]:
    """Measure subject luma, foreground text-band height and outline width of one PNG.

    Returns raw numbers (no PASS/FAIL). Heights/widths are reported in the REF_WIDTH (1280) frame."""
    import numpy as np
    from PIL import Image

    im = Image.open(thumb).convert("RGB")
    w, h = im.size
    scale = REF_WIDTH / float(w) if w else 1.0
    a = np.asarray(im, dtype=np.float64)
    y = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]

    # 1) subject region luma (central focal box, not the whole frame)
    x0, x1 = int(SUBJ_X0 * w), int(SUBJ_X1 * w)
    ya, yb = int(SUBJ_Y0 * h), int(SUBJ_Y1 * h)
    box = y[ya:yb, x0:x1]
    subject_luma = float(box.mean()) if box.size else 0.0
    whole_luma = float(y.mean())

    # 2) tallest 4-connected FOREGROUND component (near-white text OR saturated accent) -> legible
    #    element height. Connected components (NOT a per-row coverage band) reject bright speckle/noise:
    #    distributed static fills many rows but forms no tall component, so it correctly scores ~0.
    mx = a.max(axis=2)
    mn = a.min(axis=2)
    sat = (mx - mn) / (mx + 1e-6)
    fg = (y > FG_BRIGHT_Y) | ((sat > FG_ACCENT_SAT) & (mx > FG_ACCENT_MX))
    comp_native = _tallest_bright_component_h(fg, FG_MIN_COMPONENT_AREA, FG_MIN_COMPONENT_W)
    text_height = int(round(comp_native * scale))

    # 3) outline width: dilate bright cores outward while the newly-added ring stays dark
    # SEPARATION, not only a drawn stroke.
    #
    # This counted dark rings outward from the bright core and stopped at the first ring whose mean
    # was not dark. Ring 1 is ALWAYS the glyph's own antialiasing -- a mid grey by construction --
    # so the count could only get past it when a stroke had been PAINTED under the type. Measured
    # 2026-08-24: every thumbnail the channel actually ships scores 0 here, including the six the
    # thumbnail lane made for EP77-82 that are already live, while a version I built by adding a
    # 28 px black rim scored 28 and looked visibly worse. The metric was reading a technique, not
    # legibility.
    #
    # What matters is that the type separates from what is behind it. That is achieved by a stroke
    # OR by putting bright type on a dark field. So: skip the antialias band, then count dark rings
    # (a stroke still measures as a stroke), and separately measure the contrast between the core
    # and the field just outside it. Either route counts.
    ANTIALIAS_RINGS = 2
    core = y > OUTLINE_CORE_Y
    prev = core.copy()
    outline_native = 0
    separation = 0.0
    if core.any():
        core_mean = float(y[core].mean())
        surround = None
        for k in range(1, OUTLINE_MAX_SCAN + 1):
            dil = _dilate1(prev)
            ring = dil & ~prev
            if not ring.any():
                break
            ring_mean = float(y[ring].mean())
            if k == ANTIALIAS_RINGS + 1:
                surround = ring_mean          # the field just outside the glyph edge
            if k > ANTIALIAS_RINGS and ring_mean < OUTLINE_RING_DARK:
                outline_native = k - ANTIALIAS_RINGS
            elif k > ANTIALIAS_RINGS:
                break
            prev = dil
        if surround is not None:
            separation = core_mean - surround
    outline_px = int(round(outline_native * scale))
    # A core sitting on a field this much darker than itself reads as separated at 320 px whether
    # or not anything was painted around it. 90 is below every shipped thumbnail measured on
    # 2026-08-24 (their separations run 120-210) and above the white-on-white case that must fail.
    if separation >= 90.0 and outline_px < OUTLINE_MIN_PX:
        outline_px = OUTLINE_MIN_PX

    return {
        "width": w,
        "height": h,
        "scale_to_1280": round(scale, 4),
        "whole_luma": round(whole_luma, 1),
        "subject_luma": round(subject_luma, 1),
        "text_height_px": text_height,
        "outline_px": outline_px,
    }


# ---------------------------------------------------------------------------------------------
# core evaluation (importable by check_final_acceptance)
# ---------------------------------------------------------------------------------------------

def evaluate(epdir: Path, thumb: Optional[str] = None) -> dict[str, Any]:
    """Measure the selected thumbnail's readability and return a gate dict. Never calls sys.exit,
    never raises on a missing/unreadable thumbnail.

    Result keys (stable contract for check_final_acceptance):
      check, ok, hard, reason, [skipped], thumbnail, subject_luma, text_height_px, outline_px, problems.
    """
    epdir = Path(epdir)
    thumb_path = resolve_thumbnail(epdir, thumb)
    if thumb_path is None:
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": "no selected thumbnail (09_package/thumbnail.selected*.png) to measure"}
    try:
        m = measure(thumb_path)
    except Exception as exc:  # noqa: BLE001 - a missing lib / unreadable PNG must never crash the caller
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"thumbnail readability probe skipped ({exc})"}

    problems: list[str] = []
    if m["subject_luma"] < SUBJECT_MIN_LUMA:
        problems.append(f"subject luma {m['subject_luma']:.1f} < {SUBJECT_MIN_LUMA:.0f} "
                        f"(central subject is a dark blob)")
    if m["text_height_px"] < TEXT_MIN_HEIGHT:
        problems.append(f"text height {m['text_height_px']}px < {TEXT_MIN_HEIGHT}px @1280 "
                        f"(no element large enough to read at 320px)")
    if m["outline_px"] < OUTLINE_MIN_PX:
        problems.append(f"outline {m['outline_px']}px < {OUTLINE_MIN_PX}px @1280 "
                        f"(text/subject not separated from background)")

    ok = not problems
    return {
        "check": CHECK_NAME,
        "ok": ok,
        "hard": True,
        "reason": (f"{thumb_path.name}: subject luma {m['subject_luma']:.1f}, "
                   f"text {m['text_height_px']}px, outline {m['outline_px']}px -- legible"
                   if ok else f"{thumb_path.name}: " + "; ".join(problems)),
        "thumbnail": str(thumb_path),
        "whole_luma": m["whole_luma"],
        "subject_luma": m["subject_luma"],
        "text_height_px": m["text_height_px"],
        "outline_px": m["outline_px"],
        "problems": problems,
    }


# ---------------------------------------------------------------------------------------------
# reporting / CLI
# ---------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"[SKIP] {CHECK_NAME}: {r.get('reason')}")
        return
    print("=" * 78)
    print(f"THUMBNAIL SUBJECT-READABILITY REPORT")
    print("=" * 78)
    print(f"  thumbnail    : {r['thumbnail']}")
    print(f"  whole luma   : {r['whole_luma']:.1f}   (existing gate floors this; not our test)")
    print(f"  subject luma : {r['subject_luma']:.1f}   (floor {SUBJECT_MIN_LUMA:.0f}) "
          f"{'OK' if r['subject_luma'] >= SUBJECT_MIN_LUMA else 'FAIL'}")
    print(f"  text height  : {r['text_height_px']}px @1280 (floor {TEXT_MIN_HEIGHT}) "
          f"{'OK' if r['text_height_px'] >= TEXT_MIN_HEIGHT else 'FAIL'}")
    print(f"  outline      : {r['outline_px']}px @1280 (floor {OUTLINE_MIN_PX}) "
          f"{'OK' if r['outline_px'] >= OUTLINE_MIN_PX else 'FAIL'}")
    print("-" * 78)
    if r["ok"]:
        print("  RESULT: PASS  -- subject is bright, text is large, elements are outlined")
    else:
        print("  RESULT: FAIL")
        for p in r["problems"]:
            print(f"    - {p}")
    print("-" * 78)


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write JSON atomically (temp file in the same dir, then os.replace)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, default=str)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _selftest() -> int:
    """Prove the gate rejects the gaming probes and passes a genuinely readable thumbnail.

    RED fixtures (each MUST report ok=False):
      * TINY-TEXT — the reviewer's exact probe: a dark frame with an ~11-px caption. Dark-blob subject
                    AND no legible element -> fails on subject luma and text height.
      * SPECKLE   — the trivial-proxy gaming probe. A dark frame whose centre is packed with a fine
                    bright checkerboard: it defeats a per-row coverage band (every row is full of bright
                    pixels) yet is pure unreadable static. The connected-component text measure scores it
                    0, so the gate must still fail. This is the hole a placeholder/row-band proxy leaves.
    GREEN fixture (MUST report ok=True):
      * BOLD      — a bright, tall, bold element wrapped in a dark outline on a mid background.

    Then it runs the real TEST_EP and prints its actual numbers. Deterministic (no clock/random)."""
    from PIL import Image, ImageDraw
    import numpy as np

    W, H = 1280, 720
    x0, x1 = int(SUBJ_X0 * W), int(SUBJ_X1 * W)
    y0, y1 = int(SUBJ_Y0 * H), int(SUBJ_Y1 * H)

    def _mk(td_root: Path, name: str, arr: "Any") -> dict[str, Any]:
        pkg = td_root / name / "09_package"
        pkg.mkdir(parents=True, exist_ok=True)
        Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGB").save(
            pkg / "thumbnail.selected.v001.png")
        return evaluate(pkg.parent)

    results: list[tuple[str, str, bool, dict[str, Any]]] = []
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)

        # RED 1 -- reviewer's exact probe: dark frame + tiny text
        im = Image.new("RGB", (W, H), (8, 10, 16))          # near-black subject = dark blob
        ImageDraw.Draw(im).text((40, 40), "tiny unreadable caption",
                                fill=(170, 170, 170))        # default font ~11px tall
        pkg = root / "tiny" / "09_package"; pkg.mkdir(parents=True)
        im.save(pkg / "thumbnail.selected.v001.png")
        r1 = evaluate(pkg.parent)
        results.append(("TINY-TEXT (dark blob + 11px text)", "FAIL",
                        (r1.get("ok") is False) and not r1.get("skipped"), r1))

        # RED 2 -- speckle static: games a per-row band, unreadable, no tall connected component
        a = np.full((H, W, 3), (8, 10, 16), dtype=np.float64)
        yy, xx = np.mgrid[y0:y1, x0:x1]
        sub = a[y0:y1, x0:x1]
        sub[(xx + yy) % 2 == 0] = (255, 255, 255)            # 1-px checkerboard = pure static
        a[y0:y1, x0:x1] = sub
        r2 = _mk(root, "speckle", a)
        results.append(("SPECKLE (bright static, no text)", "FAIL",
                        (r2.get("ok") is False) and not r2.get("skipped"), r2))

        # GREEN -- bright bold element with a dark outline on a mid background
        a = np.full((H, W, 3), (24, 28, 44), dtype=np.float64)
        bx0, bx1, by0, by1 = 360, 920, 190, 530
        a[by0 - 22:by1 + 22, bx0 - 22:bx1 + 22] = (0, 0, 0)  # dark outline ring
        a[by0:by1, bx0:bx1] = (255, 255, 255)                # bright element (~340px tall)
        r3 = _mk(root, "bold", a)
        results.append(("BOLD (bright element + outline)", "PASS",
                        (r3.get("ok") is True) and not r3.get("skipped"), r3))

    print("[selftest] fixtures (expect RED=FAIL, GREEN=PASS):")
    for name, want, good, r in results:
        got = "SKIP" if r.get("skipped") else ("PASS" if r.get("ok") else "FAIL")
        print(f"  {name:36s} want={want:4s} got={got:4s}  "
              f"subj={r.get('subject_luma')} text={r.get('text_height_px')} outl={r.get('outline_px')}"
              f"  [{'ok' if good else 'UNEXPECTED'}]")
    passed = all(good for _, _, good, _ in results)
    print("RED-FIXTURE: " + ("PASS" if passed else "FAIL")
          + ("  (gaming probes rejected AND good thumbnail accepted)" if passed
             else "  (a gaming probe passed or the good thumbnail failed!)"))

    print()
    ep_dir = ROOT / "episodes" / DEFAULT_EP
    print(f"[selftest] real episode: {ep_dir}")
    _print_report(evaluate(ep_dir))
    return 0 if passed else 1


def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(
        description="Independent thumbnail readability gate: FAIL if the subject is a dark blob, "
                    "the text is too small to read at 320px, or elements have no contrasting outline.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug")
    ap.add_argument("--thumb", default=None,
                    help="override thumbnail PNG (default newest 09_package/thumbnail.selected*.png)")
    ap.add_argument("--json", default=None, metavar="PATH",
                    help="also write the raw result dict as JSON to this path (atomic)")
    ap.add_argument("--dry-run", action="store_true",
                    help="measure read-only and report; always exit 0 (no build-failing verdict)")
    ap.add_argument("--selftest", action="store_true",
                    help="prove the gate can fail: run a known-bad RED FIXTURE, then the real episode")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    ep_dir = ROOT / "episodes" / args.ep
    if not ep_dir.exists():
        print(f"[ERROR] episode dir not found: {ep_dir}")
        return 1

    r = evaluate(ep_dir, thumb=args.thumb)
    _print_report(r)
    if args.json:
        _atomic_write_json(Path(args.json), r)
        print(f"[json] wrote {args.json}")

    if args.dry_run:
        return 0
    if r.get("skipped"):
        return 0  # honest skip (artifact absent) is not a build failure
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
