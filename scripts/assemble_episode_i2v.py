#!/usr/bin/env python
"""Assemble finished Wan i2v frame-dirs into 1920x1080 mp4 motion clips (generic per episode).

Reads ae-demo/wan_frames_<slug>_<stem>/ and writes
  H:/pd-media/assets/ai_video/<slug>/motion/<stem>.mp4     (media master)
  remotion/public/<slug>/motion/<stem>.mp4                 (render-visible copy)

Idempotent: an existing, healthy output is skipped, so this is safe to run repeatedly while
i2v is still in flight. Generalised from assemble_centralpark_i2v.py.

Usage: py -3.11 scripts/assemble_episode_i2v.py --slug willingham [--fps-in 24] [--dry-run]
"""
from __future__ import annotations

import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _pd_media_root() -> Path:
    """The media root, resolved -- never assumed.

    FIXED 2026-08-22. This file hardcoded H:/pd-media. That drive stopped being enumerated by
    Windows around the 2026-08-16 reboot and config/storage.local.json was repointed to E:\pd-media
    on 2026-08-17. Rule 14: no OS-absolute path is a source of truth. The literal below is kept only
    as a last-resort fallback so an unconfigured checkout behaves as it used to instead of crashing.
    """
    import json as _json
    _cfg = Path(__file__).resolve().parents[1] / "config" / "storage.local.json"
    try:
        return Path(_json.loads(_cfg.read_text(encoding="utf-8"))["roots"]["media"]["path"])
    except Exception:
        return Path("H:/pd-media")


PD_MEDIA = _pd_media_root()


FF = shutil.which("ffmpeg") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
ROOT = Path(__file__).resolve().parents[1]
AE_DEMO = Path(r"C:/Users/aab15/ae-demo")
MIN_FRAMES = 40
MIN_OK_BYTES = 50_000


def assemble_one(frames: list[str], out: Path, fps_in: int) -> tuple[bool, str]:
    lst = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, dir=str(out.parent))
    try:
        for f in frames:
            lst.write(f"file '{f}'\n")
        lst.close()
        cmd = [FF, "-y", "-hide_banner", "-loglevel", "error", "-r", str(fps_in),
               "-f", "concat", "-safe", "0", "-i", lst.name,
               "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30",
               "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return (out.exists() and out.stat().st_size > MIN_OK_BYTES), r.stderr[-200:]
    finally:
        try:
            os.unlink(lst.name)
        except OSError:
            pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--fps-in", type=int, default=24, help="playback rate of the 81 Wan frames")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    out_dir = PD_MEDIA / "assets" / "ai_video" / a.slug / "motion"
    pub_dir = ROOT / "remotion" / "public" / a.slug / "motion"
    src_dirs = sorted(glob.glob(str(AE_DEMO / f"wan_frames_{a.slug}_*")))

    # The archive lives on a removable drive. On 2026-08-16 H: was not attached and this mkdir
    # raised FileNotFoundError('H:\\') as the FIRST statement of _finish_episode.sh step [1/7] --
    # so openfields and ramirez both died at `assemble failed` before a single frame was read,
    # and the whole render queue was blocked by a step that had nothing to do. There were zero
    # wan_frames_openfields_* and zero wan_frames_ramirez_* directories; hyatt's 15 were already
    # mp4. Nothing to assemble must cost nothing, and a missing archive must say so by name.
    if not a.dry_run:
        pub_dir.mkdir(parents=True, exist_ok=True)
        # Outstanding work is a frame dir whose mp4 is not already render-visible. hyatt's 15
        # were converted before the drive came out and all 15 sit in remotion/public/hyatt/motion,
        # so hyatt has nothing outstanding either -- asking the drive about them would refuse a
        # build over work that is already done.
        def _stem(d: str) -> str:
            return os.path.basename(d).replace(f"wan_frames_{a.slug}_", "")

        outstanding = [d for d in src_dirs if not (pub_dir / f"{_stem(d)}.mp4").exists()]
        if not outstanding:
            print(f"[i2v] nothing to assemble for {a.slug}: {len(src_dirs)} frame dir(s), "
                  f"{len(glob.glob(str(pub_dir / '*.mp4')))} clip(s) already render-visible in "
                  f"{pub_dir}. Not touching the archive drive.")
            return 0
        if not Path(f"{out_dir.drive}/").exists():
            # The render reads pub_dir, not the archive, so a detached drive must not stop the
            # build. Write the masters render-visible, and leave a note naming exactly what owes
            # a copy to the archive -- silent divergence between the two is the thing to avoid,
            # not the temporary absence of one of them.
            out_dir = pub_dir
            pending = ROOT / "runs" / "qc" / f"{a.slug}_i2v_archive_copy_pending.v001.txt"
            pending.parent.mkdir(parents=True, exist_ok=True)
            pending.write_text(
                f"{len(outstanding)} i2v master(s) for {a.slug} were written to {pub_dir} only.\n"
                f"The archive drive was not attached when they were made. Copy them to\n"
                f"H:/pd-media/assets/ai_video/{a.slug}/motion/ when it is back.\n"
                + "".join(f"  {os.path.basename(d)}\n" for d in outstanding),
                encoding="utf-8")
            print(f"[i2v] archive drive absent -- writing masters to {pub_dir} and recording the "
                  f"owed archive copy in {pending}")
        out_dir.mkdir(parents=True, exist_ok=True)

    made = skipped = partial = failed = 0
    for d in src_dirs:
        stem = os.path.basename(d).replace(f"wan_frames_{a.slug}_", "")
        frames = sorted(glob.glob(os.path.join(d, "*.png")))
        if len(frames) < MIN_FRAMES:
            partial += 1
            continue
        outp = out_dir / f"{stem}.mp4"
        if outp.exists() and outp.stat().st_size > MIN_OK_BYTES:
            skipped += 1
            if not a.dry_run and not (pub_dir / outp.name).exists():
                if outp.resolve() != (pub_dir / outp.name).resolve():
                    shutil.copy(outp, pub_dir / outp.name)
            continue
        if a.dry_run:
            print(f"  would assemble {stem} ({len(frames)} frames)")
            made += 1
            continue
        ok, err = assemble_one(frames, outp, a.fps_in)
        if ok:
            # With the archive detached out_dir IS pub_dir, and shutil.copy onto itself raises
            # SameFileError. Measured 2026-08-17: it killed the assembler on the FIRST clip of
            # every chunk, so openfields finished 53 conversions and only 10 mp4 reached the
            # render-visible pool. The i2v looked complete and the film would have been built
            # without 43 of its motion clips.
            if outp.resolve() != (pub_dir / outp.name).resolve():
                shutil.copy(outp, pub_dir / outp.name)
            made += 1
        else:
            failed += 1
            print(f"FAIL {stem}: {err}", flush=True)

    print(f"[{a.slug}] assembled={made} skipped={skipped} partial(in-flight)={partial} "
          f"failed={failed} (of {len(src_dirs)} frame-dirs)", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
