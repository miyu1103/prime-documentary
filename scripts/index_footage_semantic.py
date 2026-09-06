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

The same argument applies to STILL images, and for them it is worse. Measured 2026-09-06: of the
19,378 assets behind the eleven themes the eye review marked QUARANTINE, 5,887 of 6,157 videos
(95.6%) were already findable here by meaning — and 0 of 13,221 images were, because this indexer
globbed *.mp4 and *.mov only. For a picture, the theme label was the ONLY way in, and those are
the labels that were found rotten ("police_modern" holds zero real police). `--images` closes
that: same model, same space, a separate index so the clip index is never disturbed.

This is a SEARCH tool, not a gate. Being findable here does not make an asset usable — run
`build_asset_usability.py --path <file>` before putting anything on screen.

Output (resumable, written incrementally):
    runs/footage_semantic/embeddings.npy   float32 [N, 512], L2-normalised   (clips)
    runs/footage_semantic/paths.json       the N clip paths, same order
    runs/footage_semantic/state.json       progress, so a killed run resumes
    runs/footage_semantic/images_*.{npy,json}                                (--images)

Usage:
  py -3.10 scripts/index_footage_semantic.py --build            # or resume  (clips)
  py -3.10 scripts/index_footage_semantic.py --build --images   # or resume  (stills)
  py -3.10 scripts/index_footage_semantic.py --query "handcuffs closing on wrists" --top 12
  py -3.10 scripts/index_footage_semantic.py --query "a courthouse exterior" --images

py -3.10, not 3.11: torch lives in the 3.10 interpreter (2.0.1+cu118, CUDA available). 3.11 has
no torch at all, so --build there dies on import.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# factory is stock backgrounds, VFX, particles and light assets - 11,442 of its 15,683 clips are
# literally in a folder called "backgrounds". Indexing only that is why 165 documentary queries
# ("water spraying from a fire hose", "front porch of a small house") came back with a median score
# of 0.298 and a best of 0.342: the pictures being searched were never of those things. archive/ and
# stock/ are the real-footage shelves and belong in the same index.
# ai_video/ is deliberately left out - it is generated material and must not enter documentary
# b-roll through a search that cannot tell the difference.
# The ingest contract (E:\pd-media\assets\archive\_ledger\CONTRACT.md) routes downloads to the
# first storage tier above its free-space floor, so the library is spread over four drives. Only
# H: was ever indexed, which left 15,527 rights-cleared clips - courtroom_justice,
# government_buildings, decision_rooms, household_loss, bench_to_line - invisible to every search.
# That, not the queries, is why 165 documentary lookups peaked at 0.342.
SHELVES = [Path(r"E:\pd-media\assets\factory"),
           Path(r"E:\pd-media\assets\archive"),
           Path(r"E:\pd-media\assets\stock"),
           Path(r"D:\pd-archive"),
           Path(r"E:\pd-archive"),
           Path(r"F:\pd-archive")]
SHELF = SHELVES[0]   # kept for anything still importing the old name
OUT = ROOT / "runs" / "footage_semantic"
MODEL = "openai/clip-vit-base-patch32"
BATCH = 32

VIDEO_EXTS = ("*.mp4", "*.mov")
IMAGE_EXTS = ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.tif", "*.tiff", "*.bmp")

# _quarantine is where the ingest scripts put anything they could not clear:
# license_decision=review_required. An unreviewed asset must never become bindable, because
# binding is what puts it on screen. _ledger/_qc are bookkeeping, not media.
# The ai_* directories are generated material: the header above says ai_video is "deliberately
# left out", but until 2026-09-06 nothing in the code did that -- the exclusion lived only in the
# comment. It happened to be true (0 of the 30,470 indexed clip paths were ai_video) and would
# have quietly stopped being true on the next rebuild.
SKIP_PARTS = ("_quarantine", "_ledger", "_qc")
SKIP_PREFIXES = ("ai_video", "ai_image", "ai_gen", "synthetic")


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


def _excluded(p: Path) -> bool:
    for part in p.parts:
        if part in SKIP_PARTS:
            return True
        if part.lower().startswith(SKIP_PREFIXES):
            return True
    return False


def media_paths(exts: tuple[str, ...]) -> list[str]:
    out: set[str] = set()
    for shelf in SHELVES:
        if not shelf.is_dir():
            continue
        for ext in exts:
            for p in shelf.rglob(ext):
                if _excluded(p):
                    continue
                out.add(str(p))
    return sorted(out)


def clip_paths() -> list[str]:
    """Kept as its own name: other tools import it."""
    return media_paths(VIDEO_EXTS)


def load_image(path: str):
    """Open a shelf still at roughly CLIP's input size. Returns None on anything unreadable.

    `draft` makes libjpeg decode a large JPEG at a reduced scale, which is most of the speed on a
    shelf whose stills run to 6000 px. Truncated files are NOT forced to load: sixteen of them are
    known (docs/shelf/image_integrity.v001.jsonl) and a half-decoded picture embeds as grey, which
    would then answer to every washed-out query. They are skipped and counted instead.
    """
    from PIL import Image
    try:
        im = Image.open(path)
        try:
            im.draft("RGB", (448, 448))
        except Exception:
            pass
        im = im.convert("RGB")
        im.thumbnail((448, 448))
        return im
    except Exception:
        return None


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


def build(limit: int | None, workers: int, images: bool = False, device: str = "auto") -> int:
    import numpy as np
    from concurrent.futures import ThreadPoolExecutor
    from PIL import Image
    import torch
    from transformers import CLIPModel, CLIPProcessor

    # the shelf holds scans and 6000 px stills; the default bomb guard refuses some of them
    Image.MAX_IMAGE_PIXELS = 300_000_000

    OUT.mkdir(parents=True, exist_ok=True)
    pre = "images_" if images else ""
    paths_file = OUT / f"{pre}paths.json"
    emb_file = OUT / f"{pre}embeddings.npy"
    state_file = OUT / f"{pre}state.json"
    noun = "still" if images else "clip"

    all_clips = media_paths(IMAGE_EXTS if images else VIDEO_EXTS)
    if limit:
        all_clips = all_clips[:limit]
    done: list[str] = []
    embs: list = []
    if paths_file.exists() and emb_file.exists():
        done = json.loads(paths_file.read_text(encoding="utf-8"))
        embs = [np.load(emb_file)]
        print(f"resuming: {len(done)} {noun}s already embedded")
    todo = [c for c in all_clips if c not in set(done)]
    print(f"shelf {len(all_clips)} {noun}s | to do {len(todo)}")
    if not todo:
        return 0

    dev = ("cuda" if torch.cuda.is_available() else "cpu") if device == "auto" else device
    print(f"loading {MODEL} on {dev} (first run downloads ~600 MB)")
    model = CLIPModel.from_pretrained(MODEL).eval().to(dev)
    proc = CLIPProcessor.from_pretrained(MODEL)

    tmp = Path(tempfile.mkdtemp(prefix="clipidx_"))
    processed = 0
    unreadable = 0
    try:
        for start in range(0, len(todo), BATCH):
            chunk = todo[start:start + BATCH]
            imgs = []
            keep = []
            if images:
                # a still IS the frame -- no ffmpeg, no temp file, no brightest-of-three
                with ThreadPoolExecutor(max_workers=workers) as ex:
                    for c, im in zip(chunk, ex.map(load_image, chunk)):
                        if im is None:
                            unreadable += 1
                            continue
                        imgs.append(im)
                        keep.append(c)
            else:
                frames: list[tuple[str, Path]] = []
                with ThreadPoolExecutor(max_workers=workers) as ex:
                    futs = {ex.submit(grab_frame, c, tmp / f"f{i}.jpg"): (c, tmp / f"f{i}.jpg")
                            for i, c in enumerate(chunk)}
                    for fut in futs:
                        c, dst = futs[fut]
                        if fut.result():
                            frames.append((c, dst))
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
                inp = proc(images=imgs, return_tensors="pt").to(dev)
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
    print(f"indexed {len(done)} {noun}s"
          + (f" | {unreadable} unreadable, skipped" if unreadable else ""))
    return 0


def _sheet(text: str, hits: list[tuple[float, str]]) -> None:
    """Tile the hits so a person can SEE whether the index answered the question.

    Reuses build_footage_contact_sheet.py --from-json, the same way sample_theme_sheets.py does.
    A retrieval score is not evidence that the picture is right; the sheet is.
    """
    import re
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "query"
    sel = ROOT / "runs" / "qc" / f"semantic_query_{slug}.json"
    sel.parent.mkdir(parents=True, exist_ok=True)
    sel.write_text(json.dumps({"slug": f"q_{slug}", "items": [
        {"abs_path": p, "label": f"{s:.3f}"} for s, p in hits]}), encoding="utf-8")
    out = ROOT / "runs" / "qc" / f"semantic_query_{slug}.png"
    # encoding="utf-8" is load-bearing on this machine, not decoration. With text=True the reader
    # thread decodes the child with the locale codec (cp932 here), and the sheet builder prints a
    # Japanese QC reminder. The UnicodeDecodeError is raised INSIDE that thread, where run() never
    # sees it: it returns returncode 0 with stdout=None. Success, and the output gone.
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_footage_contact_sheet.py"),
                        "--from-json", str(sel), "--out", str(out)],
                       capture_output=True, encoding="utf-8", errors="replace")
    print((r.stdout or "").strip() or (r.stderr or "").strip())
    if r.returncode != 0:
        print(f"  sheet FAILED (exit {r.returncode})")
        return
    print(f"  sheet: {out}")


def query(text: str, top: int, images: bool = False, sheet: bool = False) -> int:
    import numpy as np
    import torch
    from transformers import CLIPModel, CLIPProcessor

    pre = "images_" if images else ""
    emb = np.load(OUT / f"{pre}embeddings.npy")
    paths = json.loads((OUT / f"{pre}paths.json").read_text(encoding="utf-8"))
    model = CLIPModel.from_pretrained(MODEL).eval()
    proc = CLIPProcessor.from_pretrained(MODEL)
    with torch.no_grad():
        t = proc(text=[text], return_tensors="pt", padding=True)
        q = as_tensor(model.get_text_features(**t))
        q = (q / q.norm(dim=-1, keepdim=True)).cpu().numpy().astype("float32")[0]
    scores = emb @ q
    hits = [(float(scores[i]), paths[i]) for i in np.argsort(-scores)[:top]]
    for s, p in hits:
        print(f"  {s:.3f}  {p}")
    if sheet:
        _sheet(text, hits)
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
    ap.add_argument("--images", action="store_true",
                    help="the stills index instead of the clip index")
    ap.add_argument("--device", default="auto", choices=("auto", "cuda", "cpu"))
    ap.add_argument("--sheet", action="store_true",
                    help="tile the hits into a contact sheet -- LOOK at it, the score is not proof")
    a = ap.parse_args()
    if a.build:
        return build(a.limit, a.workers, a.images, a.device)
    if a.query:
        return query(a.query, a.top, a.images, a.sheet)
    ap.error("pass --build or --query")


if __name__ == "__main__":
    raise SystemExit(main())
