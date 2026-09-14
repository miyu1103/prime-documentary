#!/usr/bin/env python3
"""Find real human faces in the archive clips BEFORE they are built into a film.

Why this exists. EP65 marmet was rendered, muxed, graded and taken all the way to the scheduling
command before anyone saw that one of its nine archive clips is a real person sitting alone
against a bare wall, face sharp and centred, smiling to camera -- twice, at 0:47 and 18:22. The
age cannot be settled from the footage, which is itself disqualifying: nobody can show it is not a
minor, and an identifiable real minor is one of the four categories that must never be published.

Nothing caught it earlier because nothing was looking:

  - the filename is "woman_sitting_on_a_chair_while_reading_a_magazine", so the keyword pass that
    compares forbidden_subjects against source filenames reported clean
  - the pool QC had opened contact sheets of the clips and ACCEPTED this one
  - every machine gate measures motion, luma, diversity and duration; a real face passes all of them

It was found by reading frames of the finished render, which costs a two-hour re-render to act on.
This moves the same question to the pool, where acting on it costs nothing.

Scope is deliberately archive footage only (remotion/public/<slug>/factory). Generated plates and
the i2v motion built from them may show people -- the owner permits depicted persons and forbids
only real-person likeness -- so scanning them would produce noise, not safety.

    py -3.11 scripts/check_pool_faces.py --slug marmet
    py -3.11 scripts/check_pool_faces.py --slug marmet --json runs/qc/marmet_pool_faces.v001.json

A detection is not a verdict. It says "a human face is on screen here, go and look". The reviewer
records the decision in runs/qc/<slug>_clip_verdicts.v001.json, which every later stage reads.
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

ROOT = Path(__file__).resolve().parents[1]

SAMPLES = 8          # frames per clip; a face that appears in none of eight is not the subject
MIN_FACE_SHARE = 0.0004  # 0.04% of frame: a 40x40 face at 1080 lines. Calibrated against the
                         # marmet clip, whose face measures 0.132% -- the first floor was set
                         # ABOVE the real case and would have reported it clean.
MIN_NEIGHBORS = 3        # the vote threshold at which that known positive is actually found


def sample_frames(path: Path, n: int):
    """n frames spread across the clip, as BGR arrays. Empty when the clip cannot be opened."""
    import cv2

    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        return []
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    out = []
    if total <= 0:
        ok, img = cap.read()
        cap.release()
        return [(0.0, img)] if ok else []
    for i in range(n):
        idx = int(total * (i + 0.5) / n)
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, img = cap.read()
        if ok and img is not None:
            out.append((idx / fps if fps else 0.0, img))
    cap.release()
    return out


def faces_in(img) -> list[tuple[int, int, int, int]]:
    import cv2

    gray = cv2.equalizeHist(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    out: list[tuple[str, int, int, int, int]] = []
    # Four cascades, because one is not enough: the marmet subject is found by the frontal
    # detectors and missed by profile, while upper-body fires five times more strongly than the
    # face does. A person can be identifiable with their face turned away.
    for xml, name in (("haarcascade_frontalface_default.xml", "face"),
                      ("haarcascade_frontalface_alt2.xml", "face"),
                      ("haarcascade_profileface.xml", "profile"),
                      ("haarcascade_upperbody.xml", "upper-body")):
        cascade = cv2.CascadeClassifier(cv2.data.haarcascades + xml)
        if cascade.empty():
            continue
        found = cascade.detectMultiScale(gray, scaleFactor=1.05,
                                         minNeighbors=MIN_NEIGHBORS, minSize=(20, 20))
        out.extend((name, *(int(v) for v in f)) for f in found)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--pool", default="factory",
                    help="subdirectory of remotion/public/<slug> to scan (default factory)")
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--samples", type=int, default=SAMPLES)
    a = ap.parse_args()

    try:
        import cv2  # noqa: F401
    except ImportError:
        # "I could not look" is not "there is nothing there". Say so and fail rather than
        # reporting a clean pool nobody examined.
        print("[pool-faces] REFUSED: OpenCV is not importable, so no face check was performed.",
              file=sys.stderr)
        print("             Run with py -3.11, which has cv2.", file=sys.stderr)
        return 2

    pool = ROOT / "remotion" / "public" / a.slug / a.pool
    clips = sorted(pool.glob("*.mp4"))
    if not clips:
        print(f"[pool-faces] no clips in {pool.relative_to(ROOT)}")
        return 0

    verdicts_p = ROOT / "runs" / "qc" / f"{a.slug}_clip_verdicts.v001.json"
    known: dict = {}
    if verdicts_p.is_file():
        try:
            v = json.loads(verdicts_p.read_text(encoding="utf-8"))
            known = dict(v.get("rejected") or {})
            for k in (v.get("reviewed_faces") or {}):
                known.setdefault(k, "face reviewed and accepted")
        except Exception:  # noqa: BLE001
            known = {}

    rows, flagged = [], []
    for c in clips:
        hits = []
        for t, img in sample_frames(c, a.samples):
            fh, fw = img.shape[0], img.shape[1]
            for (kind, x, y, w, h) in faces_in(img):
                share = (w * h) / float(fw * fh)
                if share >= MIN_FACE_SHARE:
                    hits.append({"at_seconds": round(t, 2), "kind": kind,
                                 "face_share": round(share, 5)})
        row = {"clip": c.name, "frames_sampled": a.samples,
               "detections": sorted(hits, key=lambda d: -d["face_share"])[:6],
               "max_face_share": round(max((h["face_share"] for h in hits), default=0.0), 5)}
        rows.append(row)
        mark = "  "
        if hits:
            if c.name in known:
                mark = "..";  row["already_judged"] = known[c.name][:90]
            else:
                mark = "!!";  flagged.append(row)
        print(f"{mark} {c.name[:64]:64s} faces={len(hits):2d}  max={row['max_face_share']:.4f}"
              + (f"  [judged: {known[c.name][:40]}]" if c.name in known else ""))

    out = {"schema_version": "pool_faces.v001", "slug": a.slug, "pool": a.pool,
           "min_face_share": MIN_FACE_SHARE, "clips": rows,
           "unjudged_with_faces": [r["clip"] for r in flagged]}
    dest = Path(a.json_out) if a.json_out else ROOT / "runs" / "qc" / f"{a.slug}_pool_faces.v001.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n[pool-faces] {len(clips)} clip(s) scanned, {len(flagged)} carry an unjudged human face")
    try:
        _disp = dest.relative_to(ROOT)
    except ValueError:
        _disp = dest
    print(f"[pool-faces] report -> {_disp}")
    if flagged:
        print("[pool-faces] A DETECTION IS NOT A VERDICT. Open these and decide:")
        for r in flagged:
            d = r["detections"][0]
            print(f"    {r['clip']}")
            print(f"      largest {d.get('kind', 'face')} {d['face_share']*100:.3f}% of frame "
                  f"at {d['at_seconds']:.1f}s ({len(r['detections'])} detection(s) shown)")
        print("[pool-faces] Record each decision in "
              f"runs/qc/{a.slug}_clip_verdicts.v001.json -- under 'rejected' with the reason, or "
              f"under 'reviewed_faces' if the person is not identifiable and the clip stays.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
