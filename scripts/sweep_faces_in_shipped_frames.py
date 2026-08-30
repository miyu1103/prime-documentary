"""Mechanical face sweep over an episode's already-extracted shipped frames.

WHY THIS EXISTS. On 2026-08-31, EP73 uri was read twice by eleven separate readers. The FIRST
read of sheets 39-56 listed twelve defects and did not mention cut-0205 at all. The SECOND read
found it: a young man in a blazer, centre-frame, facing camera, sharply lit, held about two
seconds, then again in tight profile. It is exactly the class of thing that closes the door under
config/ship_policy.v001.json, and it survived a full tile-by-tile human read.

MEASURED VERDICT, 2026-08-31: NOT GOOD ENOUGH TO OVERRIDE A HUMAN READ. Do not treat a hit
as evidence and do not treat silence as clearance. The numbers, on the two episodes it was built
for:

  uri         1,466 frames -> 240 hits. It DID find the real one (cut0205), but ranked it 105th.
              The top hit by face size, 238px, is frozen pipework at a gas plant. Second, 197px,
              is a snowy porch with a white plastic chair. Both opened and confirmed: no face.
  lacmegantic 1,430 frames -> 276 hits. Re-ranked by persistence (a held portrait should hit
              several sample points of the SAME cut, texture noise only one), the top result --
              224px across 4 of 4 points at 14:55 -- is WHITE SMOKE CURLING ON BLACK. Opened and
              confirmed: no face. The human reader of that range had already called it correctly.

So it is precise at neither end of its own ranking, and a static textured shot persists exactly
like a held portrait does. Haar cascades were trained on photographic portraits; documentary
B-roll of smoke, pipes, chairs and ballast trips them constantly.

WHAT IT IS STILL WORTH: running it costs a couple of minutes and it did surface a genuine miss
once. Use it as a nudge to re-open a handful of frames, never as a gate, never as a reason to
shorten a read. If it is ever to become a gate it needs a real face detector (a DNN model with a
confidence score), not a cascade.

Eyes miss faces too -- cut0205 survived a full tile-by-tile human read and was caught only on the
second pass. The answer to that is a second reader, not this.

    py -3.11 scripts/sweep_faces_in_shipped_frames.py --slug uri [--min-px 44] [--json OUT]

Reads runs/qc/shipped_frames/<slug>/frames/*.jpg, which check_shipped_frames has already written,
so it costs no decode of the master. Prints one line per frame that carries a face big enough to
register, sorted by face size -- biggest first, because a big face is the one that matters.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001
    pass

import cv2  # type: ignore

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--min-px", type=int, default=44,
                    help="ignore faces whose box is smaller than this (default 44px on a "
                         "960-wide frame, i.e. roughly 1/22 of frame height)")
    ap.add_argument("--json", help="also write the hits here")
    a = ap.parse_args()

    frames_dir = ROOT / "runs" / "qc" / "shipped_frames" / a.slug / "frames"
    frames = sorted(frames_dir.glob("*.jpg"))
    if not frames:
        print(f"no frames in {frames_dir} -- run check_shipped_frames --sheets-only first")
        return 2

    front = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    prof = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")

    hits: list[dict] = []
    for i, f in enumerate(frames):
        img = cv2.imread(str(f))
        if img is None:
            continue
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grey = cv2.equalizeHist(grey)
        boxes = []
        for cc, kind in ((front, "frontal"), (prof, "profile")):
            for (x, y, w, h) in cc.detectMultiScale(grey, scaleFactor=1.08, minNeighbors=6,
                                                    minSize=(a.min_px, a.min_px)):
                boxes.append((int(w), int(h), kind, int(x), int(y)))
        # the mirrored pass: the profile cascade only detects one direction
        flipped = cv2.flip(grey, 1)
        for (x, y, w, h) in prof.detectMultiScale(flipped, scaleFactor=1.08, minNeighbors=6,
                                                  minSize=(a.min_px, a.min_px)):
            boxes.append((int(w), int(h), "profile-r", int(img.shape[1] - x - w), int(y)))
        if not boxes:
            continue
        boxes.sort(reverse=True)
        w, h, kind, x, y = boxes[0]
        m = re.match(r"(\d+)m(\d+)s_\d+__(\w+?)_p(\d+)", f.name)
        tc = f"{int(m.group(1))}:{m.group(2)}" if m else "?"
        hits.append({"frame": f.name, "timecode": tc, "cut": m.group(3) if m else "?",
                     "face_px": h, "kind": kind, "x": x, "y": y, "faces": len(boxes),
                     "path": str(f.relative_to(ROOT)).replace("\\", "/")})
        if (i + 1) % 200 == 0:
            print(f"  ...{i+1}/{len(frames)} frames, {len(hits)} hit(s) so far", flush=True)

    hits.sort(key=lambda r: -r["face_px"])
    print(f"\n{a.slug}: {len(frames)} frame(s) swept, {len(hits)} carrying a face >= {a.min_px}px")
    print("biggest first -- OPEN THESE BEFORE SIGNING ANYTHING:\n")
    for r in hits[:40]:
        print(f"  {r['face_px']:3d}px {r['kind']:9s} {r['timecode']:>6s}  {r['cut']:12s} {r['frame']}")
    if len(hits) > 40:
        print(f"  ... and {len(hits)-40} more below {hits[39]['face_px']}px")
    print("\nA hit is NOT a defect. A back-turned extra, a crowd, a poster and a reflection all "
          "trip this.\nWhat it buys you is that a HELD PORTRAIT cannot hide in 1,000 frames "
          "unnoticed.")
    if a.json:
        Path(a.json).write_text(json.dumps(
            {"slug": a.slug, "frames_swept": len(frames), "min_px": a.min_px, "hits": hits},
            indent=1), encoding="utf-8")
        print(f"\nwrote {a.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
