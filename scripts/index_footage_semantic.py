#!/usr/bin/env python3
"""Index the footage shelf by what is ON SCREEN, not by what the filename claims.

Why this exists, measured 2026-08-03 by looking at sixteen staged clips against the queries that
asked for them:

    "courtroom interior benches"   -> a brass table lamp on a desk
    "handcuffs close up wrists"    -> a hand holding house keys
    "metal staircase into dark"    -> a microscope
    "whiskey glass with ice"       -> a cross silhouetted at dusk
    "clock face close up"          -> hands counting Polish banknotes
    "bullet casing close up"       -> a circuit board

One of sixteen matched. The binder searches ledger TITLES, and the titles on this shelf are wrong
often enough to be useless — roughly half of them are literally the string "id". No mechanical
check catches this: the file exists, it decodes, it moves, it is the right aspect. Everything goes
green while the video shows the wrong thing.

So: embed a real frame from every clip with CLIP and match queries against the picture. Text and
image land in the same space, so "handcuffs closing on wrists" retrieves clips that actually show
that, whatever the file is called.

Output (resumable, written incrementally):
    runs/footage_semantic/embeddings.npy   float32 [N, 512], L2-normalised
    runs/footage_semantic/paths.json       the N clip paths, same order
    runs/footage_semantic/state.json       progress, so a killed run resumes

Usage:
  py -3.11 scripts/index_footage_semantic.py --build            # or resume
  py -3.11 scripts/index_footage_semantic.py --query "handcuffs closing on wrists" --top 12
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELF = Path(r"H:\pd-media\assets\factory")
OUT = ROOT / "runs" / "footage_semantic"
MODEL = "openai/clip-vit-base-patch32"
BATCH = 32


def as_tensor(out):
    """transformers 5.x returns a model-output object from get_*_features, 4.x returned a tensor.

    Both shapes have to work: pinning the library version is not worth it, and silently indexing
    with the wrong array would poison every future match.
    """
    for attr in ("image_embeds", "text_embeds", "pooler_output", "last_hidden_state"):
        v = getattr(out, attr, None)
        if v is not None:
            return v
    return out


def clip_paths() -> list[str]:
    return sorted(str(p) for p in SHELF.rglob("*.mp4"))


def grab_frame(clip: str, dst: Path) -> bool:
    """The brightest of three sample points. Fails quietly: a shelf this size has broken files.

    Sampling one frame at 1.2 s indexed clips that open on black as if the clip WERE black, and a
    black embedding then attracted every dark-sounding query. Three shorts in the first batch got
    clips measuring 0.1, 0.8 and 7.7 mean luma and rendered as holes of up to 1.87 s.
    """
    best, best_luma = None, -1.0
    for i, t in enumerate(("1.2", "3.5", "7.0")):
        cand = dst.with_name(f"{dst.stem}_{i}{dst.suffix}")
        r = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", t, "-i", clip, "-frames:v", "1",
             "-vf", "scale=224:224:force_original_aspect_ratio=increase,crop=224:224",
             str(cand)], capture_output=True)
        if r.returncode != 0 or not cand.exists() or cand.stat().st_size == 0:
            continue
        try:
            from PIL import Image
            luma = sum(Image.open(cand).convert("L").resize((16, 16)).getdata()) / 256.0
        except Exception:
            continue
        if luma > best_luma:
            best, best_luma = cand, luma
    if best is None:
        return False
    best.replace(dst)
    return True


def build(limit: int | None, workers: int) -> int:
    import numpy as np
    from concurrent.futures import ThreadPoolExecutor
    from PIL import Image
    import torch
    from transformers import CLIPModel, CLIPProcessor

    OUT.mkdir(parents=True, exist_ok=True)
    paths_file, emb_file, state_file = OUT / "paths.json", OUT / "embeddings.npy", OUT / "state.json"

    all_clips = clip_paths()
    if limit:
        all_clips = all_clips[:limit]
    done: list[str] = []
    embs: list = []
    if paths_file.exists() and emb_file.exists():
        done = json.loads(paths_file.read_text(encoding="utf-8"))
        embs = [np.load(emb_file)]
        print(f"resuming: {len(done)} clips already embedded")
    todo = [c for c in all_clips if c not in set(done)]
    print(f"shelf {len(all_clips)} clips | to do {len(todo)}")
    if not todo:
        return 0

    print(f"loading {MODEL} (first run downloads ~600 MB)")
    model = CLIPModel.from_pretrained(MODEL).eval()
    proc = CLIPProcessor.from_pretrained(MODEL)

    tmp = Path(tempfile.mkdtemp(prefix="clipidx_"))
    processed = 0
    try:
        for start in range(0, len(todo), BATCH):
            chunk = todo[start:start + BATCH]
            frames: list[tuple[str, Path]] = []
            with ThreadPoolExecutor(max_workers=workers) as ex:
                futs = {ex.submit(grab_frame, c, tmp / f"f{i}.jpg"): (c, tmp / f"f{i}.jpg")
                        for i, c in enumerate(chunk)}
                for fut in futs:
                    c, dst = futs[fut]
                    if fut.result():
                        frames.append((c, dst))
            if not frames:
                done.extend(chunk)
                continue
            imgs = []
            keep = []
            for c, dst in frames:
                try:
                    imgs.append(Image.open(dst).convert("RGB"))
                    keep.append(c)
                except Exception:
                    pass
            if not imgs:
                done.extend(chunk)
                continue
            with torch.no_grad():
                inp = proc(images=imgs, return_tensors="pt")
                v = as_tensor(model.get_image_features(**inp))
                v = v / v.norm(dim=-1, keepdim=True)
            embs.append(v.cpu().numpy().astype("float32"))
            done.extend(keep)
            processed += len(keep)
            if processed % (BATCH * 10) < BATCH:
                np.save(emb_file, np.concatenate(embs))
                paths_file.write_text(json.dumps(done), encoding="utf-8")
                state_file.write_text(json.dumps({"done": len(done), "shelf": len(all_clips)}),
                                      encoding="utf-8")
                print(f"  {len(done)}/{len(all_clips)}", flush=True)
    finally:
        if embs:
            np.save(emb_file, np.concatenate(embs))
            paths_file.write_text(json.dumps(done), encoding="utf-8")
            state_file.write_text(json.dumps({"done": len(done), "shelf": len(all_clips)}),
                                  encoding="utf-8")
        for f in tmp.glob("*"):
            f.unlink(missing_ok=True)
        tmp.rmdir()
    print(f"indexed {len(done)} clips")
    return 0


def query(text: str, top: int) -> int:
    import numpy as np
    import torch
    from transformers import CLIPModel, CLIPProcessor

    emb = np.load(OUT / "embeddings.npy")
    paths = json.loads((OUT / "paths.json").read_text(encoding="utf-8"))
    model = CLIPModel.from_pretrained(MODEL).eval()
    proc = CLIPProcessor.from_pretrained(MODEL)
    with torch.no_grad():
        t = proc(text=[text], return_tensors="pt", padding=True)
        q = as_tensor(model.get_text_features(**t))
        q = (q / q.norm(dim=-1, keepdim=True)).cpu().numpy().astype("float32")[0]
    scores = emb @ q
    for i in np.argsort(-scores)[:top]:
        print(f"  {scores[i]:.3f}  {paths[i]}")
    return 0


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--query")
    ap.add_argument("--top", type=int, default=10)
    a = ap.parse_args()
    if a.build:
        return build(a.limit, a.workers)
    if a.query:
        return query(a.query, a.top)
    ap.error("pass --build or --query")


if __name__ == "__main__":
    raise SystemExit(main())
