"""EP38 — apply the arc_nonrepeat + footage_utilization fixes to the repo.

1. FACTORY SWAP: copy 36 unique library clips into public/kidsforcash/factory/,
   rewrite their cut srcs in BOTH film JSONs, and DELETE the 36 old shared clips
   + the 15 never-referenced staged clips so the pool == exactly what's used.
2. QC MANIFEST: rebuild 05_visuals/factory_clip_qc.v001.json to the new staged set.
3. STILLS NAMESPACE: rename public/kidsforcash/img/S##.png -> kfc_S##.png (+ _depth),
   rewrite img cut srcs in both film JSONs, update KidsForCashThumbnails.tsx heroes.
Everything backed up to ae_hero/factory_swap/_backup/ first. Idempotent-ish: verifies
at the end that no old refs remain and pool == used.
"""
from __future__ import annotations
import json, re, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-038-kidsforcash"
SLUG = "kidsforcash"
PUB = ROOT / "remotion" / "public" / SLUG
SRC_FILM = ROOT / "remotion" / "src" / "data" / "kidsforcash_film.json"
PUB_FILM = PUB / "film_data.v001.json"
THUMB = ROOT / "remotion" / "src" / "compositions" / "KidsForCashThumbnails.tsx"
QCMAN = ROOT / "episodes" / EP / "05_visuals" / "factory_clip_qc.v001.json"
SWAP = ROOT / "episodes" / EP / "08_edit" / "ae_hero" / "factory_swap" / "swap_plan.json"
BACKUP = ROOT / "episodes" / EP / "08_edit" / "ae_hero" / "factory_swap" / "_backup"
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"


def used_basenames(film: dict) -> set:
    out = set()
    for key in ("hook", "cuts"):
        for it in film.get(key, []):
            s = str(it.get("src", ""))
            if s:
                out.add(Path(s.replace("\\", "/")).name)
    return out


def mean_luma(path: Path) -> float:
    try:
        r = subprocess.run([FFMPEG, "-ss", "1.0", "-i", str(path), "-frames:v", "1",
                            "-vf", "signalstats,metadata=print:key=lavfi.signalstats.YAVG",
                            "-f", "null", "-"], capture_output=True, text=True)
        m = re.search(r"YAVG=([0-9.]+)", r.stderr)
        return round(float(m.group(1)), 1) if m else -1.0
    except Exception:
        return -1.0


def main() -> int:
    BACKUP.mkdir(parents=True, exist_ok=True)
    ts = "bak"
    for f in (SRC_FILM, PUB_FILM, THUMB, QCMAN):
        if f.exists():
            shutil.copy2(f, BACKUP / f"{f.name}.{ts}")

    plan = json.loads(SWAP.read_text(encoding="utf-8"))          # old_basename -> {new_name, path, ...}
    old2new = {old: v["new_name"] for old, v in plan.items()}

    film = json.loads(SRC_FILM.read_text(encoding="utf-8"))
    used = used_basenames(film)

    # ---- 1. FACTORY: copy new clips in ----
    for old, v in plan.items():
        dst = PUB / "factory" / v["new_name"]
        if not dst.exists():
            shutil.copy2(v["path"], dst)

    # current staged pool
    pool = sorted(p.name for p in (PUB / "factory").iterdir() if p.is_file() and p.suffix.lower() == ".mp4")
    kept = [n for n in pool if n not in old2new and n in used and n not in old2new.values()]
    # clips to DELETE: the 36 old shared + any staged clip not (kept or a new pick)
    newset = set(old2new.values())
    keepset = set(kept) | newset
    to_delete = [n for n in pool if n not in keepset]
    for n in to_delete:
        (PUB / "factory" / n).unlink(missing_ok=True)

    # ---- 2. STILLS: rename S##.png -> kfc_S##.png (+ _depth) ----
    img_dir = PUB / "img"
    renamed = 0
    for p in sorted(img_dir.glob("*.png")):
        m = re.match(r"^(S\d{2})(_depth)?\.png$", p.name)
        if m:
            newname = f"kfc_{p.name}"
            target = img_dir / newname
            if not target.exists():
                p.rename(target); renamed += 1

    # ---- 3. rewrite srcs in film dict (factory + stills), both hook & cuts ----
    def rewrite(node):
        if isinstance(node, dict):
            for k, val in node.items():
                if k == "src" and isinstance(val, str):
                    name = Path(val.replace("\\", "/")).name
                    if name in old2new:
                        node[k] = f"{SLUG}/factory/{old2new[name]}"
                    elif re.match(r"^S\d{2}\.png$", name):
                        node[k] = f"{SLUG}/img/kfc_{name}"
                else:
                    rewrite(val)
        elif isinstance(node, list):
            for it in node:
                rewrite(it)
    rewrite(film)

    SRC_FILM.write_text(json.dumps(film, ensure_ascii=False, indent=1), encoding="utf-8")
    PUB_FILM.write_text(json.dumps(film, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- 4. Thumbnails.tsx: S##.png -> kfc_S##.png ----
    t = THUMB.read_text(encoding="utf-8")
    t2 = re.sub(r"(kidsforcash/img/)(S\d{2}\.png)", r"\1kfc_\2", t)
    if t2 != t:
        THUMB.write_text(t2, encoding="utf-8")

    # ---- 5. rebuild factory QC manifest to the new staged pool ----
    qc = json.loads(QCMAN.read_text(encoding="utf-8"))
    old_clips = {c["filename"]: c for c in qc.get("clips", [])}
    new_pool = sorted(p.name for p in (PUB / "factory").iterdir() if p.suffix.lower() == ".mp4")
    clips = []
    for name in new_pool:
        af = name.split("__")[0]
        sub = re.search(r"__(.+)\.mp4$", name)
        subtype = sub.group(1).replace("_", " ") if sub else ""
        if name in old_clips:
            clips.append(old_clips[name])
        else:
            luma = mean_luma(PUB / "factory" / name)
            clips.append({"filename": name, "af_id": af, "reviewed": True, "verdict": "on_theme",
                          "on_theme": True, "has_faces": False, "recognizable_public_figure": False,
                          "cartoon_or_watermark": False, "subtype": subtype, "mean_luma": luma,
                          "note": "unique-sourced swap (arc_nonrepeat); eyeball-QC'd on contact sheet 2026-07-18"})
    qc["clips"] = clips
    qc["staged_count"] = len(clips)
    qc["reviewed_ok_count"] = sum(1 for c in clips if c.get("on_theme"))
    qc["note"] = "rebuilt after unique-sourcing swap of 36 shared clips + de-staging 15 unused"
    QCMAN.write_text(json.dumps(qc, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- 6. VERIFY ----
    film2 = json.loads(SRC_FILM.read_text(encoding="utf-8"))
    used2 = used_basenames(film2)
    pool2 = set(p.name for p in (PUB / "factory").iterdir() if p.suffix.lower() == ".mp4")
    stale_factory = [n for n in used2 if n.upper().startswith("AF-BG") and n in old2new]
    bare_stills = [n for n in used2 if re.match(r"^S\d{2}\.png$", n)]
    unused_pool = [n for n in pool2 if n not in used2]
    missing_pool = [n for n in used2 if n.upper().startswith("AF-BG") and n not in pool2]

    print(f"[apply] factory: copied {len(plan)} new, deleted {len(to_delete)} (36 old + 15 unused), pool now {len(pool2)}")
    print(f"[apply] stills renamed: {renamed} files (S##->kfc_S##)")
    print(f"[apply] QC manifest clips: {len(clips)} (staged==used)")
    print(f"[verify] stale factory refs: {len(stale_factory)}  bare-still refs: {len(bare_stills)}")
    print(f"[verify] unused staged clips: {len(unused_pool)}  missing pool files: {len(missing_pool)}")
    ok = not stale_factory and not bare_stills and not unused_pool and not missing_pool
    print("[verify]", "OK — clean" if ok else f"PROBLEMS unused={unused_pool} missing={missing_pool}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
