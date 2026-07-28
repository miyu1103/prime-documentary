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

EPISODE_DIRS = {p.name.split("-", 3)[-1]: p.name for p in (ROOT / "episodes").glob("PD-*")}


def scan(dirpath: Path, exts: tuple[str, ...]) -> list[Path]:
    if not dirpath.is_dir():
        return []
    return sorted(p for p in dirpath.iterdir() if p.suffix.lower() in exts and p.is_file())


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
    factory = scan(base / "factory", (".mp4", ".mov", ".webm"))
    overlay = scan(base / "overlay", (".mp4", ".mov", ".webm"))

    stills: list[dict] = []
    people: list[dict] = []
    rejected: list[dict] = []          # everything excluded, with the measured reason
    skipped_src = 0
    for p in imgs:
        rel = f"{slug}/img/{p.name}"
        head = p.stem[0].upper()
        if head == "M":                      # i2v source plate -- its motion clip is the asset
            skipped_src += 1
            continue
        if p.stat().st_size < MIN_OK_BYTES:
            rejected.append({"public_path": rel, "reason": f"stub {p.stat().st_size}B"})
            continue
        if check_content:
            lum = mean_luma(p)
            if 0 <= lum < MIN_LUMA:
                rejected.append({"public_path": rel, "reason": f"near-black luma {lum:.1f}"})
                continue
        if head in ("P", "F"):
            people.append(entry(slug, "PPL", len(people) + 1, p, rel,
                                role="visible_face", scene_id=p.stem))
        else:
            stills.append(entry(slug, "S", len(stills) + 1, p, rel,
                                role="body", scene_id=p.stem))

    def videos(paths, kind, sub, allow_dark: bool = False):
        """Returns (kept, demoted). Near-black clips are DEMOTED to overlay, never dropped
        silently: particle/light-leak assets are legitimately dark and belong on the screen
        blend layer, while black stubs are simply unusable. Both leave the cut pool."""
        kept, demoted = [], []
        for p in paths:
            rel = f"{slug}/{sub}/{p.name}"
            if p.stat().st_size < MIN_OK_BYTES:
                rejected.append({"public_path": rel, "reason": f"stub {p.stat().st_size}B"})
                continue
            if check_content and not allow_dark:
                lum = mean_luma(p, at=0.5)
                if lum < 0:
                    rejected.append({"public_path": rel, "reason": "undecodable"})
                    continue
                if lum < MIN_LUMA:
                    demoted.append(entry(slug, "O", len(demoted) + 1, p, rel,
                                         kind_="video", blend_hint="screen",
                                         demoted_from=sub, mean_luma=round(lum, 2)))
                    continue
            kept.append(entry(slug, kind, len(kept) + 1, p, rel, kind_="video"))
        return kept, demoted

    motion_e, motion_dark = videos(motion, "M", "motion")
    factory_e, factory_dark = videos(factory, "F", "factory")
    overlay_e, _ = videos(overlay, "O", "overlay", allow_dark=True)
    overlay_e += motion_dark + factory_dark

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
                   "factory": len(factory_e), "overlay": len(overlay_e),
                   "rejected": len(rejected)},
        "stills": stills + people,     # people are stills too; role distinguishes them
        "people": people,
        "motion": motion_e,
        "factory": factory_e,
        "overlay": overlay_e,
        "rejected": rejected,          # kept for audit: what was excluded and why
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
          f"factory={len(factory_e)} overlay={len(overlay_e)} rejected={len(rejected)} "
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
