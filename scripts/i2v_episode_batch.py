#!/usr/bin/env python
"""Generic per-episode Wan i2v batch (replaces the hard-coded i2v_centralpark_batch.py).

Drives C:/Users/aab15/ae-demo/comfy_wan.py over an episode's i2v source stills and collects
frames into ae-demo/wan_frames_<slug>_<stem>/.

RESUME CORRECTNESS (the EP50 bug that cost a day -- feedback-no-render-churn #2):
the skip-check MUST look at the directory comfy_wan actually writes,
`ae-demo/wan_frames_<prefix>/`, NOT ComfyUI/output/wanout/<prefix> (which never exists as a
dir -- frames land there as flat files). Checking the wrong path meant NOTHING was ever
skipped, so every ComfyUI crash-restart regenerated all finished clips from scratch.

CHUNKING (feedback-no-render-churn #6): Wan leaks VRAM and hard-crashes roughly every
20-30 clips. Set I2V_MAX=N so this exits after N non-skipped clips; the driving chain then
restarts ComfyUI FRESH before the next chunk, which preempts the leak-crash entirely.

Usage:
  py -3.11 scripts/i2v_episode_batch.py --slug willingham [--kinds M,P] [--dry-run]
  I2V_MAX=12 py -3.11 scripts/i2v_episode_batch.py --slug willingham

Exit 0 always when it did useful work or had nothing to do; the chain decides when to stop
based on the on-disk frame-dir count, never on this script's word.
"""
from __future__ import annotations

import argparse
import glob
import os
import subprocess
import sys
from pathlib import Path

DRIVER = r"C:/Users/aab15/ae-demo/comfy_wan.py"
AE_DEMO = Path(r"C:/Users/aab15/ae-demo")
AI_ROOT = Path("H:/pd-media/assets/ai")
MIN_FRAMES = 40          # a finished clip is 81 frames; <40 means it died mid-write

PERSON_PROMPT = (
    "subtle natural human motion, the person breathes and shifts slightly, tiny head movement, "
    "living cinematic documentary shot, camera very slowly pushes in, shallow depth of field")
SCENE_PROMPT = (
    "subtle cinematic camera motion, slow push-in or drift, atmospheric living environment, "
    "gentle light flicker, documentary footage, no morphing")


def motion_prompt(stem: str) -> str:
    """P## are faces/people; M##_src are scene plates."""
    return PERSON_PROMPT if stem.upper().startswith("P") else SCENE_PROMPT


def frame_dir(slug: str, stem: str) -> Path:
    return AE_DEMO / f"wan_frames_{slug}_{stem}"


def is_done(slug: str, stem: str) -> bool:
    d = frame_dir(slug, stem)
    return d.exists() and len(list(d.glob("*.png"))) >= MIN_FRAMES


def source_dir(slug: str) -> Path:
    """The archive is authoritative, but it lives on a removable drive.

    2026-08-16: H: was not attached and EVERY i2v plan pointed at H:/pd-media/assets/ai/<slug>.
    The same plates are also staged render-visible under remotion/public/<slug>/img -- that is
    what the film actually reads, and for these four episodes the two sets are the same files.
    Measured on openfields: 191 png in the public dir, 191 declared in asset_manifest.v003.
    Falling back keeps the pipeline running on a drive-out day; it does not invent inputs, and
    the archive stays authoritative the moment it is back.
    """
    ai = AI_ROOT / slug
    if ai.is_dir():
        return ai
    local = Path(__file__).resolve().parents[1] / "remotion" / "public" / slug / "img"
    if local.is_dir():
        print(f"[i2v] archive {ai} unavailable -- reading the render-visible copies in {local}")
        return local
    raise SystemExit(f"no source dir: neither {ai} nor {local}")


def collect_sources(slug: str, kinds: list[str]) -> list[Path]:
    ai = source_dir(slug)
    out: list[Path] = []
    for k in kinds:
        out += sorted(Path(p) for p in glob.glob(str(ai / f"{k}*.png")))
    # stable, de-duplicated
    seen, uniq = set(), []
    for p in out:
        if p.name not in seen:
            seen.add(p.name)
            uniq.append(p)
    return uniq


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--kinds", default="M,P", help="comma-separated filename prefixes to i2v")
    ap.add_argument("--only", default=None, help="substring filter on the source filename")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=704)
    ap.add_argument("--length", type=int, default=81)
    ap.add_argument("--steps", type=int, default=30)
    ap.add_argument("--shift", type=float, default=8.0)
    ap.add_argument("--cfg", type=float, default=5.0)
    # A clip measures ~206s on the 4090. Anything past 3x that means ComfyUI died underneath
    # us and comfy_wan is polling a corpse -- observed 2026-07-29, the batch hung forever and
    # the robust chain could never take its next turn (silent stall, failure F-03).
    # PROMPT OVERRIDE. The built-in SCENE_PROMPT asks for an "atmospheric living
    # environment" and comfy_wan negates "static, motionless" -- together they invite Wan to
    # POPULATE the frame. Measured on EP61 weimer 2026-08-04: W012 ("cold water over stones,
    # no bank, no sky") came back with a dog in a blue harness on a leash and a person walking;
    # W045 ("a cassette recorder beside a notepad") grew a hand. An episode whose spec forbids
    # 12 subject classes and 7 real likenesses cannot let the generator add subjects it was
    # never shown. These let the episode say what may move.
    ap.add_argument("--seed-base", type=int, default=1000,
                    help="seed = seed_base + index; change it to RE-ROLL a clip that came back "
                         "with invented content instead of re-running the same trajectory")
    ap.add_argument("--prompt", default=None,
                    help="override the built-in motion prompt for every clip in this run")
    ap.add_argument("--neg", default=None,
                    help="override comfy_wan negative prompt for every clip in this run")
    ap.add_argument("--clip-timeout", type=int, default=600,
                    help="seconds before a single clip is abandoned and the batch exits")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    kinds = [k.strip() for k in a.kinds.split(",") if k.strip()]
    imgs = collect_sources(a.slug, kinds)
    if a.only:
        # Comma-separated list, not a single substring. EP61 weimer converts a NAMED subset of
        # its commissioned stills to motion (65 of 150); one substring cannot express that, and
        # a second driver script would be a duplicate implementation of this one. A value with
        # no comma behaves exactly as before.
        wants = [w.strip() for w in a.only.split(",") if w.strip()]
        imgs = [p for p in imgs if any(w in p.name for w in wants)]

    todo = [p for p in imgs if not is_done(a.slug, p.stem)]
    done_already = len(imgs) - len(todo)
    i2v_max = int(os.environ.get("I2V_MAX", "0")) or None
    print(f"i2v[{a.slug}]: {len(imgs)} sources, {done_already} already done, {len(todo)} to do"
          + (f" (chunk max {i2v_max})" if i2v_max else ""), flush=True)

    if a.dry_run:
        for p in todo[: (i2v_max or len(todo))]:
            print(f"  would run {p.name} -> {frame_dir(a.slug, p.stem)}")
        return 0

    done = 0
    for i, img in enumerate(todo):
        stem = img.stem
        prefix = f"{a.slug}_{stem}"
        cmd = ["py", "-3.11", DRIVER, "--image", str(img), "--prompt", a.prompt or motion_prompt(stem),
               "--prefix", prefix, "--w", str(a.width), "--h", str(a.height),
               "--length", str(a.length), "--steps", str(a.steps), "--shift", str(a.shift),
               "--cfg", str(a.cfg), "--seed", str(a.seed_base + i)]
        if a.neg:
            cmd += ["--neg", a.neg]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=a.clip_timeout)
            tail = (r.stdout + r.stderr)[-200:].replace("\n", " ")
        except subprocess.TimeoutExpired:
            # ComfyUI is almost certainly dead; exit so the chain restarts it FRESH rather
            # than blocking forever on a socket nobody is listening to.
            print(f"[{done + 1}/{len(todo)}] {stem} TIMEOUT after {a.clip_timeout}s "
                  f"-- assuming ComfyUI died; exiting so the chain can restart it", flush=True)
            return 0
        ok = is_done(a.slug, stem)
        done += 1
        print(f"[{done}/{len(todo)}] {stem} {'ok' if ok else 'FAIL: ' + tail}", flush=True)
        if i2v_max and done >= i2v_max:
            print(f"CHUNK done ({done}) -- exiting so the chain can restart ComfyUI fresh", flush=True)
            break
    print(f"DONE ran {done}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
