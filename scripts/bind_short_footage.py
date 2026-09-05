#!/usr/bin/env python3
"""Bind every FOOTAGE plate to a real archive clip, by LEDGER TITLE, and record the rights.

Two things make this harder than a search:

  * Filenames lie. AF-BG-34700__padlock_and_chain.mp4 is titled "handcuffs under police lights";
    AF-BG-8133__bank_vault_door.mp4 is titled "an empty cell of a prison". Only the ledger title
    describes the content, and roughly half the ledger rows have the literal string "id" as their
    title, so those clips are unreachable by search at all.
  * 9:16 is brutal. A centre crop of a 16:9 frame keeps 31.6% of the width, so a wide shot is
    unusable however well its title reads. Measured on 220 crime/police clips: only 27% survive.

So a candidate must clear BOTH the title match and a measured crop/motion/exposure test before it
is written into a design. Anything that clears neither is left unbound and reported, rather than
silently filled with something wrong.

Writes into each plate: `bound_file`, `bound_title`, `bound_license`, `bound_source`, plus the
measured `centre_energy` / `motion` / `luma`. Never overwrites an existing binding unless --force.

Usage:
  py -3.11 scripts/bind_short_footage.py --dry-run
  py -3.11 scripts/bind_short_footage.py [--limit 100] [--force]
"""
from __future__ import annotations

import argparse
import glob
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
LEDGER = r"E:\pd-media\assets\archive\_ledger\*.jsonl"
CACHE = Path(r"E:\pd-media\assets\archive\_qc\vertical_index.jsonl")
USABLE = {"free_commercial", "pd", "cc0"}
W, H = 128, 72

MIN_CENTRE, MIN_MOTION, LUMA = 0.38, 0.8, (28, 200)


def ledger_rows() -> list[dict]:
    seen, out = set(), []
    for f in sorted(glob.glob(LEDGER)):
        for line in open(f, encoding="utf-8", errors="replace"):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            p, t = d.get("file_path"), (d.get("title") or "")
            if (not p or p in seen or d.get("kind") != "video"
                    or d.get("license_decision") not in USABLE
                    or t in ("", "id")):        # ~half the ledger has a useless title
                continue
            seen.add(p)
            out.append({"path": p, "title": t, "license": d["license_decision"],
                        "source": d.get("source"), "theme": d.get("theme")})
    return out


def measure(path: str) -> dict | None:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf",
                        f"select='not(mod(n\\,15))',scale={W}:{H}", "-vsync", "0",
                        "-frames:v", "6", "-pix_fmt", "gray", "-f", "rawvideo", "-"],
                       capture_output=True)
    a = np.frombuffer(r.stdout, dtype=np.uint8)
    k = len(a) // (W * H)
    if k < 2:
        return None
    f = a[:k * W * H].reshape(k, H, W).astype(np.int16)
    gy = np.abs(np.diff(f, axis=1)).sum(axis=0)
    gx = np.abs(np.diff(f, axis=2)).sum(axis=0)
    det = np.zeros((H, W))
    det[:gy.shape[0], :] += gy
    det[:, :gx.shape[1]] += gx
    cw = int(round(H * 9 / 16)); x0 = (W - cw) // 2
    return {"centre_energy": round(float(det[:, x0:x0 + cw].sum() / (det.sum() or 1)), 4),
            "motion": round(float(np.abs(np.diff(f, axis=0)).mean()), 3),
            "luma": round(float(f[:, :, x0:x0 + cw].mean()), 1)}


def luma_of(m: dict) -> float | None:
    """index_archive_vertical.py wrote `luma_crop`; this script writes `luma`. Read either."""
    v = m.get("luma", m.get("luma_crop"))
    return float(v) if v is not None else None


def usable(m: dict | None) -> bool:
    if not m:
        return False
    lu = luma_of(m)
    return bool(lu is not None and m.get("centre_energy", 0) >= MIN_CENTRE
                and m.get("motion", 0) >= MIN_MOTION and LUMA[0] <= lu <= LUMA[1])


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    rows = ledger_rows()
    print(f"{len(rows):,} commercially-usable video clips with a real title")

    cache: dict[str, dict] = {}
    if CACHE.exists():
        for line in CACHE.open(encoding="utf-8"):
            try:
                r = json.loads(line)
                cache[r["file_path"]] = r
            except Exception:
                pass
    print(f"{len(cache):,} already measured")

    # footage_diversity allows a generic symbol to appear twice across the catalogue; forbidding
    # reuse entirely left 246 of 562 plates unbound, because queries like "judge using a gavel"
    # match exactly one clip in the whole ledger. Cap at 2 uses instead of 1.
    REUSE_CAP = 2
    used: dict[str, int] = {}
    bound = unbound = skipped = 0
    report: list[str] = []
    files = sorted(DESIGNS.glob("*.json"))
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        dirty = False
        for s in d["shorts"]:
            for p in (s.get("plates") or []):
                if not p or p.get("source") != "FOOTAGE":
                    continue
                if p.get("bound_file") and not args.force:
                    skipped += 1
                    used[p["bound_file"]] = used.get(p["bound_file"], 0) + 1
                    continue
                if args.limit and bound >= args.limit:
                    continue
                q = (p.get("footage_query") or "").lower().split()
                if not q:
                    unbound += 1
                    continue
                cands = [r for r in rows if all(w in r["title"].lower() for w in q)]
                if not cands:                      # relax to any-word when AND finds nothing
                    cands = [r for r in rows if any(w in r["title"].lower() for w in q)][:60]
                picked = None
                for c in cands:
                    if used.get(c["path"], 0) >= REUSE_CAP or not Path(c["path"]).exists():
                        continue
                    m = cache.get(c["path"])
                    if m is None:
                        mm = measure(c["path"])
                        if mm is None:
                            continue
                        m = {**c, "file_path": c["path"], **mm}
                        cache[c["path"]] = m
                        with CACHE.open("a", encoding="utf-8") as fh:
                            fh.write(json.dumps(m, ensure_ascii=False) + "\n")
                    if usable(m):
                        picked = (c, m)
                        break
                if not picked:
                    unbound += 1
                    report.append(f"{s['short_id']} n{p['n']}: no crop-safe clip for "
                                  f"{p.get('footage_query')!r} ({len(cands)} title matches)")
                    continue
                c, m = picked
                used[c["path"]] = used.get(c["path"], 0) + 1
                p.update({"bound_file": c["path"], "bound_title": c["title"],
                          "bound_license": c["license"], "bound_source": c["source"],
                          "centre_energy": m["centre_energy"], "motion": m["motion"],
                          "luma": luma_of(m)})
                bound += 1
                dirty = True
        if dirty and not args.dry_run:
            f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nbound {bound}, already bound {skipped}, UNBOUND {unbound}")
    if report:
        print(f"\nplates left unbound ({len(report)}) — these fall through to GENERATE:")
        for x in report[:25]:
            print("  " + x)
        if len(report) > 25:
            print(f"  ... {len(report)-25} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
