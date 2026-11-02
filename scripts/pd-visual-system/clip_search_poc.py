#!/usr/bin/env python
"""PD Visual System — P04 Semantic Search PoC (OpenCLIP).

Embeds the representative frames produced by P03 (scene_index_poc) and lets you
search them with English text. Reuses the existing global GPU env (torch cu118 +
open_clip). Weights cache to D:\\PD_AI_Models\\clip. Read-only on media/thumbs.

Subcommands:
  build  : embed one representative frame (50%) per cut from the P03 scene DB
  query  : text -> top-k cuts
  eval   : run a query list (JSON/lines) -> results JSON for human review

Run with the GLOBAL env python (has open_clip + torch cu118):
  python scripts/pd-visual-system/clip_search_poc.py build
  python scripts/pd-visual-system/clip_search_poc.py query "courthouse exterior" -k 8
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time
from pathlib import Path

import numpy as np

MODEL = "ViT-B-32"
PRETRAINED = "laion2b_s34b_b79k"
CACHE_DIR = r"D:\PD_AI_Models\clip"


def _load_model():
    import torch
    import open_clip
    os.makedirs(CACHE_DIR, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, _, preprocess = open_clip.create_model_and_transforms(
        MODEL, pretrained=PRETRAINED, cache_dir=CACHE_DIR)
    tokenizer = open_clip.get_tokenizer(MODEL)
    model = model.to(device).eval()
    return model, preprocess, tokenizer, device


def _weight_file_sha() -> dict:
    """Locate the downloaded weight in CACHE_DIR and hash it (provenance)."""
    best = None
    for dp, _dn, fn in os.walk(CACHE_DIR):
        for f in fn:
            if f.endswith((".bin", ".safetensors", ".pt")):
                p = os.path.join(dp, f)
                sz = os.path.getsize(p)
                if best is None or sz > best[1]:
                    best = (p, sz)
    if not best:
        return {"weight_file": None}
    h = hashlib.sha256()
    with open(best[0], "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return {"weight_file": best[0], "weight_bytes": best[1], "weight_sha256": h.hexdigest()}


def cmd_build(args):
    from PIL import Image
    import torch
    con = sqlite3.connect(args.scene_db)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT cut_id, asset_id, thumb50, thumb25, thumb75 FROM cuts").fetchall()
    con.close()
    items = []
    for r in rows:
        thumb = r["thumb50"] or r["thumb25"] or r["thumb75"]
        if thumb and os.path.exists(thumb):
            items.append((r["cut_id"], r["asset_id"], thumb))
    print(f"cuts_with_thumb={len(items)} / total_cuts={len(rows)}")

    model, preprocess, _tok, device = _load_model()
    ids, assets, paths, vecs = [], [], [], []
    t0 = time.time()
    B = 64
    for i in range(0, len(items), B):
        batch = items[i:i + B]
        imgs = []
        keep = []
        for cid, aid, tp in batch:
            try:
                imgs.append(preprocess(Image.open(tp).convert("RGB")))
                keep.append((cid, aid, tp))
            except Exception as e:
                print(f"  skip {tp}: {e}", file=sys.stderr)
        if not imgs:
            continue
        with torch.no_grad():
            x = torch.stack(imgs).to(device)
            f = model.encode_image(x)
            f = f / f.norm(dim=-1, keepdim=True)
        f = f.cpu().numpy().astype("float32")
        for (cid, aid, tp), v in zip(keep, f):
            ids.append(cid); assets.append(aid); paths.append(tp); vecs.append(v)
        print(f"  embedded {len(ids)}/{len(items)} ({time.time()-t0:.1f}s)")

    vecs = np.stack(vecs) if vecs else np.zeros((0, 512), "float32")
    np.savez(args.index, ids=np.array(ids), assets=np.array(assets),
             paths=np.array(paths), vecs=vecs)
    manifest = {
        "model": MODEL, "pretrained": PRETRAINED, "dim": int(vecs.shape[1]) if len(vecs) else 512,
        "count": len(ids), "device": device, "built_sec": round(time.time() - t0, 2),
        "scene_db": args.scene_db, "index": args.index,
        **_weight_file_sha(),
    }
    Path(args.manifest).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("MANIFEST", json.dumps(manifest, indent=2))


def _search(index, model, tokenizer, device, text, k):
    import torch
    d = np.load(index, allow_pickle=True)
    vecs = d["vecs"]
    with torch.no_grad():
        t = tokenizer([text]).to(device)
        q = model.encode_text(t)
        q = (q / q.norm(dim=-1, keepdim=True)).cpu().numpy().astype("float32")[0]
    sims = vecs @ q
    order = np.argsort(-sims)[:k]
    return [(str(d["ids"][j]), str(d["assets"][j]), str(d["paths"][j]), float(sims[j])) for j in order]


def cmd_query(args):
    model, _pre, tokenizer, device = _load_model()
    res = _search(args.index, model, tokenizer, device, args.text, args.k)
    for rank, (cid, aid, path, s) in enumerate(res, 1):
        print(f"{rank:2d}. {s:.3f}  {aid}  [{cid}]  {path}")


def cmd_eval(args):
    model, _pre, tokenizer, device = _load_model()
    queries = [q.strip() for q in Path(args.queries).read_text(encoding="utf-8").splitlines() if q.strip()]
    out = {"model": MODEL, "pretrained": PRETRAINED, "k": args.k, "queries": []}
    for text in queries:
        res = _search(args.index, model, tokenizer, device, text, args.k)
        out["queries"].append({
            "query": text,
            "top": [{"rank": i + 1, "score": round(s, 3), "asset": aid, "cut": cid, "thumb": path}
                    for i, (cid, aid, path, s) in enumerate(res)],
        })
        print(f"[{text}] top1={res[0][1] if res else None} score={res[0][3]:.3f}" if res else f"[{text}] none")
    Path(args.out).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print("WROTE", args.out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", default=r"data\pd_vs_clip_index.npz")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("--scene-db", default=r"data\pd_vs_scene_index.sqlite")
    b.add_argument("--manifest", default=r"data\pd_vs_clip_manifest.json"); b.set_defaults(func=cmd_build)
    q = sub.add_parser("query"); q.add_argument("text"); q.add_argument("-k", type=int, default=8); q.set_defaults(func=cmd_query)
    e = sub.add_parser("eval"); e.add_argument("--queries", required=True); e.add_argument("--out", default=r"data\pd_vs_clip_eval.json")
    e.add_argument("-k", type=int, default=10); e.set_defaults(func=cmd_eval)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
