#!/usr/bin/env python
"""Build a motion-first asset_manifest.v003.json by SCANNING what the render can actually see.

WHY IT SCANNES INSTEAD OF EDITING v001 (measured 2026-07-29):
  * EP56 postoffice's asset_manifest.v001.json lists 42 motion + 235 factory clips whose files
    DO NOT EXIST (ai_video/postoffice is empty, public/postoffice/{factory,motion,overlay} are
    empty). A manifest is a claim; only the filesystem is evidence. (feedback-verify-dont-assume)
  * EP52 morton / EP54 flowers have all 16 P## face stills staged under public/<slug>/img/ but
    ABSENT from v001, so the faces could never reach the people pool -- the exact gap the owner
    called out ("P##顔を人物プールに必ず入れる").

Classification by filename prefix under remotion/public/<slug>/:
  img/P*.png -> people (faces; injected into the film's still rotation and the cold open)
  img/F*.png -> people (visible_face variants)
  img/S*.png -> stills, role=body
  img/M*.png -> i2v SOURCE plates; excluded (their animated .mp4 lives in motion/)
  motion/*.mp4  -> motion   (i2v)
  factory/*.mp4 -> factory  (stock / staged real footage)
  overlay/*.mp4 -> overlay  (particles, light leaks; composited, never a cut)
  ae/*.webm     -> ae       (ADR-0011 After Effects plates; composited via aeBeats, never a cut)

Every entry is size-checked against the pre-render gate's own black-stub floor (50KB) AND
content-checked by sampling a real frame's mean luma, so a manifest that passes here cannot
fail the gate on asset integrity.

WHY CONTENT, NOT JUST SIZE (measured 2026-07-29): 227 of EP52 morton's 240 staged factory
clips are ~11KB 2.6s files whose frames are luma 1.0-1.8 -- genuinely BLACK video, not just
efficient encodes. Size alone flagged them, but only a decoded frame proves it. Separately,
EP54 flowers has AF-PART/AF-LIGHT particle and light-streak assets sitting in factory/;
they are near-black by design (they are meant to be SCREENED as overlays, never used as a
cut), so they are moved to the overlay pool rather than counted as footage.

Usage:
  py -3.11 scripts/build_asset_manifest_motionfirst.py --slug morton [--out <path>] [--dry-run]
      [--no-content-check]   (skip frame decoding; size-only, much faster, less safe)
"""
from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "remotion" / "public"
MIN_OK_BYTES = 50_000          # same floor as pd_prerender_gate.py MIN_IMG_BYTES
MIN_LUMA = 8.0                 # same floor as pd_prerender_gate.py MIN_LUMA
# Below MIN_LUMA, these two say whether anything is actually IN the frame. Measured on the four
# EP71 plates the old rule threw away (peak 45-108, sd 5-14) against EP52's dead ones (peak <10,
# sd <1). Deliberately generous: a plate has to be nearly featureless to be called dead.
DARK_PEAK_MIN = 30             # brightest pixels present anywhere in the frame
DARK_SPREAD_MIN = 2.0          # luma standard deviation
# Library families authored to be SCREENED over a picture, never to be the picture itself.
OVERLAY_CLASS_PREFIXES = ("AF-LIGHT", "AF-PART", "AF-VFX")

EPISODE_DIRS = {p.name.split("-", 3)[-1]: p.name for p in (ROOT / "episodes").glob("PD-*")}


def scan(dirpath: Path, exts: tuple[str, ...]) -> list[Path]:
    if not dirpath.is_dir():
        return []
    return sorted(p for p in dirpath.iterdir() if p.suffix.lower() in exts and p.is_file())


def video_duration(path: Path) -> float:
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", str(path)], capture_output=True, text=True, timeout=30)
        return float(r.stdout.strip() or 0)
    except Exception:
        return 0.0


def video_sample_times(path: Path) -> list[float]:
    """Head / mid / tail. A single mid sample misses clips that fade in and out of black."""
    d = video_duration(path)
    if d <= 0:
        return [0.5]
    return [min(0.15, d * 0.05), d * 0.5, max(0.0, d - 0.15)]


def dark_content(path: Path) -> tuple[int, float]:
    """(peak luma, luma stdev) of a still. Tells a designed dark plate from a dead render."""
    try:
        from PIL import Image, ImageStat
    except ImportError:
        return (0, 0.0)
    try:
        im = Image.open(path).convert("L")
        st = ImageStat.Stat(im)
        return (int(im.getextrema()[1]), round(float(st.stddev[0]), 2))
    except Exception:  # noqa: BLE001
        return (0, 0.0)


def mean_luma(path: Path, at: float | None = None) -> float:
    """Mean luma of one decoded frame, -1 if undecodable. Same metric as the pre-render gate."""
    try:
        from PIL import Image
    except ImportError:
        return -1.0
    try:
        if at is None:
            img = Image.open(path)
        else:
            r = subprocess.run(
                ["ffmpeg", "-v", "error", "-ss", f"{at}", "-i", str(path), "-frames:v", "1",
                 "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, timeout=60)
            if not r.stdout:
                return -1.0
            img = Image.open(io.BytesIO(r.stdout))
        b = img.convert("L").resize((64, 36)).tobytes()
        return sum(b) / len(b)
    except Exception:
        return -1.0


def entry(slug: str, kind: str, idx: int, path: Path, rel: str, **extra) -> dict:
    return {"asset_id": f"{slug.upper()[:3]}-{kind.upper()}-{idx:03d}",
            "path": str(path).replace("\\", "/"),
            "public_path": rel, "bytes": path.stat().st_size, **extra}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--episode-id", default=None)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-content-check", action="store_true",
                    help="skip frame decoding (size-only); faster but cannot catch black video")
    a = ap.parse_args()
    check_content = not a.no_content_check

    slug = a.slug
    ep = a.episode_id or EPISODE_DIRS.get(slug)
    if not ep:
        raise SystemExit(f"cannot resolve episode id for slug {slug}")
    base = PUBLIC / slug
    if not base.is_dir():
        raise SystemExit(f"no staged public dir {base} -- stage assets first")

    imgs = scan(base / "img", (".png", ".jpg", ".jpeg"))
    motion = scan(base / "motion", (".mp4", ".mov", ".webm"))

    # DEPTH COMPANIONS ARE RENDERER INPUTS, NEVER PICTURES (2026-08-25, EP75).
    # lahaina staged H0xx_depth.png beside its hero plates and ran i2v over them; this scan
    # then swept 73 depth PNGs into the stills pool and 62 depth MP4s into the motion pool,
    # and the film shipped 180 cuts -- 678 seconds -- of raw grayscale depth mattes as
    # picture, with every gate green. A depth map belongs in a "depth" prop, not a "src".
    def _split_depth(paths):
        keep = [p for p in paths if not p.stem.endswith("_depth")]
        dropped = [p for p in paths if p.stem.endswith("_depth")]
        return keep, dropped
    imgs, _depth_imgs = _split_depth(imgs)
    motion, _depth_motion = _split_depth(motion)
    for _p in _depth_imgs:
        rejected_depth = f"{slug}/img/{_p.name}"
        print(f"  [depth-companion] {rejected_depth} -- excluded: renderer input, never a picture")
    for _p in _depth_motion:
        print(f"  [depth-companion] {slug}/motion/{_p.name} -- excluded: renderer input, never a picture")
    factory = scan(base / "factory", (".mp4", ".mov", ".webm"))
    overlay = scan(base / "overlay", (".mp4", ".mov", ".webm"))
    # ADR-0011 (from EP77): an AE card is a PLATE and is "registered like any other asset".
    # Scanned exactly like the three video pools above; it is never a cut, it is composited by
    # CaseFilm's aeBeats layer. allow_dark is not a relaxation here -- an alpha plate is mostly
    # TRANSPARENT, so its decoded RGB luma is legitimately near zero and the black-video rule
    # (written for dead i2v renders) would demote every card ever made.
    ae = scan(base / "ae", (".webm", ".mov", ".mp4"))

    # Which plates ARE the people plates is declared by the episode, not guessed from a filename.
    declared_people: set[str] = set()
    declared_empty: set[str] = set()
    # THE HIGHEST REVISION, through the canonical resolver (invariant 14 -- imported, not
    # restated). oroville's real contract is v002 and this file was reading a superseded v001;
    # lahaina's v001 says people_plates=null while its v003 lists them, so a v001 reader builds
    # a film that thinks the episode has no faces in it.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from check_episode_spec import spec_path as _resolve_spec  # noqa: PLC0415
    spec_path = _resolve_spec(ROOT / "episodes" / ep)
    if spec_path.is_file():
        try:
            _spec = json.loads(spec_path.read_text(encoding="utf-8"))
            declared = _spec.get("people_plates", [])
            declared_people = {s for s in declared} | {Path(s).stem for s in declared}
            _empty = _spec.get("intentionally_empty_stills", [])
            declared_empty = {s for s in _empty} | {Path(s).stem for s in _empty}
        except Exception:
            declared_people = set()
            declared_empty = set()

    stills: list[dict] = []
    people: list[dict] = []
    rejected: list[dict] = []          # everything excluded, with the measured reason
    dark_by_design: list[dict] = []    # below the luma floor, but the frame carries content
    motion_source_candidates: list[Path] = []

    def add_still(p: Path) -> None:
        rel = f"{slug}/img/{p.name}"
        head = p.stem[0].upper()
        if p.stat().st_size < MIN_OK_BYTES:
            rejected.append({"public_path": rel, "reason": f"stub {p.stat().st_size}B"})
            return
        if check_content:
            lum = mean_luma(p)
            if 0 <= lum < MIN_LUMA:
                # A DARK PLATE AND A DEAD PLATE ARE NOT THE SAME PICTURE (2026-08-23, EP71).
                # Four oroville plates were rejected here at mean luma 0.0-1.0 -- and all four
                # are exactly what the image order asked for: "pure black field with a single
                # hand-drawn red boundary line, nothing else in frame". The film then failed its
                # own spec on four missing mandatory stills. EP52's genuinely dead plates were
                # flat: mean 1.0-1.8 with nothing in them. So measure the difference instead of
                # keeping a list of exceptions -- a designed dark plate HAS content, a dead one
                # does not.
                peak, spread = dark_content(p)
                if p.stem in declared_empty or p.name in declared_empty:
                    dark_by_design.append({"public_path": rel, "mean_luma": round(lum, 2),
                                           "peak_luma": peak, "stdev": spread,
                                           "note": "declared in episode_spec."
                                                   "intentionally_empty_stills"})
                    print(f"  [empty-by-order] {rel} mean={lum:.1f} peak={peak} sd={spread} "
                          f"-- kept because the spec declares it empty on purpose")
                elif peak >= DARK_PEAK_MIN and spread >= DARK_SPREAD_MIN:
                    dark_by_design.append({"public_path": rel, "mean_luma": round(lum, 2),
                                           "peak_luma": peak, "stdev": spread,
                                           "note": "dark by design: mean is below the floor but "
                                                   "the frame carries bright content"})
                    print(f"  [dark-by-design] {rel} mean={lum:.1f} peak={peak} sd={spread} "
                          f"-- kept; a flat dead render has neither")
                else:
                    rejected.append({"public_path": rel,
                                     "reason": f"near-black luma {lum:.1f} "
                                               f"(peak {peak}, sd {spread}: nothing in the frame)"})
                    return
        # People plates are DECLARED in episode_spec.people_plates. EP63/64/65 name theirs with the
        # episode prefix -- C211-C220, M198-M207, R207-R216 -- and the old P/F test reported all
        # three as having no faces at all. The prefix test stays as a fallback for older episodes.
        if p.name in declared_people or p.stem in declared_people or head in ("P", "F"):
            people.append(entry(slug, "PPL", len(people) + 1, p, rel,
                                role="visible_face", scene_id=p.stem))
        else:
            stills.append(entry(slug, "S", len(stills) + 1, p, rel,
                                role="body", scene_id=p.stem))

    for p in imgs:
        # Defer source plates until the motion file has passed content QC. A file merely existing
        # is not enough: if it fades to black and is demoted to overlay, the source still must be
        # restored as the safe fallback or a mandatory visual silently disappears from the film.
        # People plates are different: the film builder needs a still PEOPLE pool even when an
        # i2v derivative also exists. Deferring every P/F plate made all 29 safe Willingham face
        # stills disappear merely because matching P*.mp4 files were present, so the manifest
        # correctly refused to build with people=0. Keep declared/legacy people stills and let
        # the independently checked motion derivative coexist in the motion pool.
        is_people_plate = (
            p.name in declared_people
            or p.stem in declared_people
            or p.stem[0].upper() in ("P", "F")
        )
        # A plate the order asks to be EMPTY is the cut itself -- the word is composited over it
        # in Remotion. Its i2v derivative is near-black video, which lands in the overlay pool
        # (screened, never cut), so treating the plate as an i2v source leaves it in NO cut at
        # all and the film fails its own mandatory_stills (EP71 oroville O086, 2026-08-23).
        is_declared_empty = p.name in declared_empty or p.stem in declared_empty
        if ((base / "motion" / f"{p.stem}.mp4").is_file()
                and not is_people_plate and not is_declared_empty):
            motion_source_candidates.append(p)
            continue
        add_still(p)

    def videos(paths, kind, sub, allow_dark: bool = False):
        """Returns (kept, demoted). Anything unfit as a full-frame CUT is demoted to the
        overlay pool rather than dropped, so it stays available on the screen-blend layer.

        Two rules, both learned the hard way on EP54 (2026-07-29):
        * OVERLAY CLASS BY NAME. AF-LIGHT / AF-PART / AF-VFX are light leaks, particles and
          effect plates -- they are authored to be screened over a picture, never to BE the
          picture. EP54's entire 218-clip "factory" pool was these, so 68% of the film's
          video was abstract effects rather than documentary b-roll. Counts looked healthy;
          content was not.
        * MINIMUM luma across head/mid/tail, not one sample. AF-LIGHT-0498 measured 31.8 at
          the 0.5s sample and passed, but it fades from 8.2 to 2.2 at its ends -- on screen
          that is a 4.7s black hole, which is exactly what the post-render gate caught.
        """
        kept, demoted = [], []
        for p in paths:
            rel = f"{slug}/{sub}/{p.name}"
            if p.stat().st_size < MIN_OK_BYTES:
                rejected.append({"public_path": rel, "reason": f"stub {p.stat().st_size}B"})
                continue
            if not allow_dark and any(k in p.name for k in OVERLAY_CLASS_PREFIXES):
                demoted.append(entry(slug, "O", len(demoted) + 1, p, rel,
                                     kind_="video", blend_hint="screen",
                                     demoted_from=sub, reason="overlay-class asset"))
                continue
            if check_content and not allow_dark:
                lums = [mean_luma(p, at=t) for t in video_sample_times(p)]
                usable = [x for x in lums if x >= 0]
                if not usable:
                    rejected.append({"public_path": rel, "reason": "undecodable"})
                    continue
                if min(usable) < MIN_LUMA:
                    demoted.append(entry(slug, "O", len(demoted) + 1, p, rel,
                                         kind_="video", blend_hint="screen",
                                         demoted_from=sub, min_luma=round(min(usable), 2),
                                         reason="fades to black at an end"))
                    continue
            kept.append(entry(slug, kind, len(kept) + 1, p, rel, kind_="video"))
        return kept, demoted

    motion_e, motion_dark = videos(motion, "M", "motion")
    factory_e, factory_dark = videos(factory, "F", "factory")
    overlay_e, _ = videos(overlay, "O", "overlay", allow_dark=True)
    overlay_e += motion_dark + factory_dark
    ae_e, _ = videos(ae, "A", "ae", allow_dark=True)

    kept_motion_stems = {Path(row["public_path"]).stem for row in motion_e}
    for p in motion_source_candidates:
        if p.stem not in kept_motion_stems:
            add_still(p)
    skipped_src = sum(p.stem in kept_motion_stems for p in motion_source_candidates)

    manifest = {
        "schema_version": "asset_manifest.v003",
        "episode_id": ep,
        "slug": slug,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "producer": "scripts/build_asset_manifest_motionfirst.py",
        "is_stub": False,
        "source_of_truth": f"filesystem scan of remotion/public/{slug}",
        "content_checked": check_content,
        "counts": {"stills": len(stills), "people": len(people), "motion": len(motion_e),
                   "factory": len(factory_e), "overlay": len(overlay_e), "ae": len(ae_e),
                   "rejected": len(rejected)},
        "stills": stills + people,     # people are stills too; role distinguishes them
        "people": people,
        "motion": motion_e,
        "factory": factory_e,
        "overlay": overlay_e,
        "ae": ae_e,                    # ADR-0011 plates: composited by aeBeats, never a cut
        "rejected": rejected,          # kept for audit: what was excluded and why
        "dark_by_design": dark_by_design,  # below the luma floor and KEPT, with the measurement
    }

    # ---- readiness verdict against the pre-render gate's real thresholds ----
    problems: list[str] = []
    if not motion_e and not factory_e:
        problems.append("NO real video (motion+factory both empty) -- kamishibai, cannot build")
    if not people:
        problems.append("NO people/face stills -- the film would have no human faces")
    if not stills:
        problems.append("NO body stills")
    # cap-2 video reuse must be able to cover >=68% of a ~4.6s-cut plan for the full runtime
    cap_video = (len(motion_e) + len(factory_e)) * 2
    supports_min = cap_video / 0.68 * 4.6 / 60
    print(f"[{slug}] stills={len(stills)} people={len(people)} motion={len(motion_e)} "
          f"factory={len(factory_e)} overlay={len(overlay_e)} ae={len(ae_e)} rejected={len(rejected)} "
          f"(skipped {skipped_src} M-source plates)")
    print(f"[{slug}] video capacity at reuse<=2: {cap_video} cuts "
          f"-> supports up to ~{int(cap_video / 0.68)} total cuts / ~{supports_min:.1f} min")
    if rejected:
        by_reason: dict[str, int] = {}
        for r in rejected:
            key = r["reason"].split()[0]
            by_reason[key] = by_reason.get(key, 0) + 1
        print(f"  [rejected] {by_reason} e.g. {[r['public_path'] for r in rejected[:2]]}")
    for p in problems:
        print(f"  [PROBLEM] {p}")

    out = a.out or (ROOT / "episodes" / ep / "05_visuals" / "asset_manifest.v003.json")
    if a.dry_run:
        print(f"(dry-run) would write {out}")
        return 1 if problems else 0
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    return 1 if problems else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
