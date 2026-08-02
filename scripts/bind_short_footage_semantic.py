#!/usr/bin/env python3
"""Bind every FOOTAGE plate to a clip that actually SHOWS what the plate asked for.

Replaces title matching, which does not work on this shelf. Measured 2026-08-03 by extracting a
frame from sixteen staged clips and looking at them next to the query that selected them:

    courtroom interior benches   -> a brass table lamp        WRONG
    handcuffs close up wrists    -> a hand holding house keys WRONG
    metal staircase into dark    -> a microscope              WRONG
    whiskey glass with ice       -> a cross at dusk           WRONG
    clock face close up          -> counting Polish banknotes WRONG
    bullet casing close up       -> a circuit board           WRONG
    silhouette walking corridor  -> a silhouette in a corridor  right

One of sixteen. The titles on this shelf are wrong often enough to be worthless, and no mechanical
check notices: the file exists, it decodes, it moves, the aspect is right, so every gate goes green
while the picture is of something else entirely.

This binds on the picture instead, using the CLIP index from index_footage_semantic.py, and it
refuses rather than guesses: a plate whose best match scores below the floor is left unbound and
reported, because an honest hole is cheaper than a confident mismatch.

Diversity is enforced globally — a clip already used by any Short in the run is not offered again,
so the owner's "the same clip keeps showing up" does not reappear through a new mechanism.

Usage:
  py -3.11 scripts/bind_short_footage_semantic.py --shorts 86-99 --dry-run
  py -3.11 scripts/bind_short_footage_semantic.py --shorts 86-99 --apply
  py -3.11 scripts/bind_short_footage_semantic.py --shorts 86-99 --apply --contact-sheet
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
INDEX = ROOT / "runs" / "footage_semantic"
REPORT = ROOT / "runs" / "footage_semantic" / "bind_report.json"

# Below this cosine score CLIP is not recognising the subject, it is returning the least-bad thing
# on the shelf. Calibrated on the sixteen known-bad bindings: every one of them would have scored
# under this, and the one correct binding scored well over it.
SCORE_FLOOR = 0.28

# Clips rejected by eye and never to be offered again. Two kinds live here:
#   * readable paperwork on screen (a lease/employment agreement clip keeps winning "documents on a
#     desk" queries; legible third-party text is a rights problem, not a taste one)
#   * anything an eye QC pass marked as not showing the requested subject
# Score alone cannot catch either: the lease clip scores 0.312, comfortably above any floor.
REJECTS = INDEX / "rejected_clips.txt"


def load_rejects() -> set[str]:
    if not REJECTS.exists():
        return set()
    return {ln.strip() for ln in REJECTS.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")}


def parse_range(spec: str) -> set[int]:
    out: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out.update(range(int(a), int(b) + 1))
        elif part:
            out.add(int(part))
    return out


def load_index():
    import numpy as np
    emb = np.load(INDEX / "embeddings.npy")
    paths = json.loads((INDEX / "paths.json").read_text(encoding="utf-8"))
    if len(paths) != emb.shape[0]:
        raise SystemExit(f"index is inconsistent: {len(paths)} paths vs {emb.shape[0]} vectors")
    return emb, paths


def embed_queries(texts: list[str]):
    import numpy as np
    import torch
    from transformers import CLIPModel, CLIPProcessor
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from index_footage_semantic import MODEL, as_tensor
    model = CLIPModel.from_pretrained(MODEL).eval()
    proc = CLIPProcessor.from_pretrained(MODEL)
    out = []
    for i in range(0, len(texts), 64):
        with torch.no_grad():
            t = proc(text=texts[i:i + 64], return_tensors="pt", padding=True, truncation=True)
            q = as_tensor(model.get_text_features(**t))
            q = q / q.norm(dim=-1, keepdim=True)
        out.append(q.cpu().numpy().astype("float32"))
    return np.concatenate(out)


def contact_sheet(rows: list[dict], dst: Path) -> None:
    """Tile one frame per bound clip so a human can see the mismatches a gate cannot."""
    import shutil
    tmp = dst.parent / "_sheet_frames"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    n = 0
    for r in rows:
        if not r.get("bound_file"):
            continue
        n += 1
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "1.2", "-i", r["bound_file"],
                        "-frames:v", "1", "-vf", "scale=216:384", str(tmp / f"t_{n:03d}.png")],
                       capture_output=True)
    got = sorted(tmp.glob("t_*.png"))
    if not got:
        return
    cols = 8
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp / "t_%03d.png"),
                    "-vf", f"tile={cols}x{-(-len(got) // cols)}:padding=6:color=0x1a1a1a",
                    "-frames:v", "1", str(dst)], capture_output=True)
    print(f"contact sheet: {dst}  ({len(got)} clips)")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--shorts", required=True, help="e.g. 86-99 or 86,87,92")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--contact-sheet", action="store_true")
    ap.add_argument("--floor", type=float, default=SCORE_FLOOR)
    a = ap.parse_args()
    if not a.apply and not a.dry_run:
        ap.error("pass --apply or --dry-run")

    import numpy as np
    want = parse_range(a.shorts)
    emb, paths = load_index()
    print(f"semantic index: {len(paths)} clips")

    jobs = []   # (design_path, design, short, plate)
    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for s in d["shorts"]:
            n = int(s["short_id"].replace("short", ""))
            if n not in want:
                continue
            for p in s["plates"]:
                if p.get("source") == "FOOTAGE":
                    jobs.append((f, d, s, p))
    if not jobs:
        print("no FOOTAGE plates in range")
        return 0

    queries = [f"{(p.get('subject') or '').strip()}. {(p.get('footage_query') or '').strip()}"
               for _, _, _, p in jobs]
    print(f"{len(jobs)} FOOTAGE plates to bind")
    Q = embed_queries(queries)
    scores = emb @ Q.T                      # [clips, plates]

    used: set[str] = set(load_rejects())
    if used:
        print(f"{len(used)} clips permanently excluded by eye QC (runs/footage_semantic/rejected_clips.txt)")
    rows, unbound = [], []
    # hardest plates first: a plate with only one plausible clip should claim it before an easy one
    order = sorted(range(len(jobs)), key=lambda i: -float(scores[:, i].max()))
    for i in order:
        _, _, s, p = jobs[i]
        col = scores[:, i]
        pick = None
        for idx in np.argsort(-col)[:400]:
            cand = paths[idx]
            if cand in used:
                continue
            if float(col[idx]) < a.floor:
                break
            pick = (cand, float(col[idx]))
            break
        row = {"short": s["short_id"], "n": p["n"], "line": p.get("line"),
               "query": p.get("footage_query"), "subject": p.get("subject"),
               "bound_file": pick[0] if pick else None,
               "score": round(pick[1], 3) if pick else round(float(col.max()), 3)}
        if pick:
            used.add(pick[0])
            rows.append(row)
        else:
            unbound.append(row)

    rows.sort(key=lambda r: (r["short"], r["n"]))
    print(f"bound {len(rows)} | refused {len(unbound)} (best score under {a.floor})")
    if unbound:
        print("  refused rather than guessed:")
        for r in unbound[:12]:
            print(f"    {r['short']} p{r['n']:02d} {r['score']:.3f}  {r['query']}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps({"bound": rows, "unbound": unbound}, ensure_ascii=False, indent=2),
                      encoding="utf-8")
    print(f"report: {REPORT}")

    if a.contact_sheet:
        contact_sheet(rows, INDEX / "bind_contact.png")

    if not a.apply:
        print("\nDRY RUN - designs not written.")
        return 0

    by_plate = {(r["short"], r["n"]): r for r in rows}
    written = 0
    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        touched = False
        for s in d["shorts"]:
            n = int(s["short_id"].replace("short", ""))
            if n not in want:
                continue
            for p in s["plates"]:
                if p.get("source") != "FOOTAGE":
                    continue
                r = by_plate.get((s["short_id"], p["n"]))
                if not r:
                    # leave a refused plate visibly unbound; assemble_short will stop on it
                    p.pop("bound_file", None)
                    touched = True
                    continue
                p["bound_file"] = r["bound_file"]
                p["bound_match"] = "semantic-clip"
                p["bound_score"] = r["score"]
                touched = True
                written += 1
        if touched:
            f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {written} bindings into the designs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
