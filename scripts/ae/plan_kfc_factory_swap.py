"""EP38 — plan the factory-clip swap for arc_nonrepeat + footage_utilization.

Replaces the 36 SHARED factory clips (used by other episodes → arc_nonrepeat FAIL)
with UNIQUE-to-EP38 clips picked from the H:\ library, theme-matched by subtype.
Keeps the 5 already-unique used clips. Emits a swap plan + extracts one QC frame
per NEW candidate for eyeball review (never trust filenames — EP36 cathedral lesson).

Outputs:
  08_edit/ae_hero/factory_swap/swap_plan.json      old_basename -> new (path, af_id, subtype)
  08_edit/ae_hero/factory_swap/qc_frames/<afid>.jpg
  08_edit/ae_hero/factory_swap/contact.png         montage for a single eyeball pass
"""
from __future__ import annotations
import json, os, re, glob, subprocess, sys
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-038-kidsforcash"
FILM = ROOT / "remotion" / "src" / "data" / "kidsforcash_film.json"
LIBDIR = Path(r"E:/pd-media/assets/factory/backgrounds")
OUT = ROOT / "episodes" / EP / "08_edit" / "ae_hero" / "factory_swap"
QC = OUT / "qc_frames"
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
STOP = {"the", "a", "an", "of", "at", "in", "on", "and", "with", "empty", "night", "dark", "wide"}


def subtype(name: str) -> str:
    m = re.search(r"__(.+)\.mp4$", name, re.I)
    return (m.group(1).replace("_", " ").strip().lower() if m else "")


def toks(s: str) -> set:
    return {w for w in re.split(r"\s+", s) if w and w not in STOP}


def build_taken() -> set:
    taken = set()
    for p in glob.glob(str(ROOT / "remotion/src/data/*_film.json")):
        if "kidsforcash" in p:
            continue
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        for c in d.get("cuts", []):
            n = Path(str(c.get("src", ""))).name
            if n.upper().startswith("AF-BG"):
                taken.add(n.lower())
    for d in glob.glob(str(ROOT / "remotion/public/*")):
        slug = Path(d).name
        if slug == "kidsforcash" or not os.path.isdir(d):
            continue
        for f in glob.glob(d + "/**/*", recursive=True):
            n = Path(f).name
            if n.upper().startswith("AF-BG"):
                taken.add(n.lower())
    return taken


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    QC.mkdir(parents=True, exist_ok=True)
    film = json.loads(FILM.read_text(encoding="utf-8"))
    fac = [(i, c) for i, c in enumerate(film["cuts"]) if c.get("kind") == "footage"]
    used = sorted(set(Path(c["src"]).name for _, c in fac))
    taken = build_taken()
    shared = [u for u in used if u.lower() in taken]
    keep = [u for u in used if u.lower() not in taken]
    print(f"[plan] factory cuts={len(fac)} used={len(used)} shared(replace)={len(shared)} unique(keep)={len(keep)}")

    # unique-available library index by subtype
    lib = glob.glob(str(LIBDIR / "AF-BG-*.mp4"))
    idx = {}          # subtype -> [names]
    avail = {}        # name -> path
    for f in lib:
        n = Path(f).name
        if n.lower() in taken:
            continue
        avail[n] = f
        idx.setdefault(subtype(n), []).append(n)
    print(f"[plan] library={len(lib)} unique-available={len(avail)} distinct subtypes={len(idx)}")

    # match each shared clip -> a unique clip: exact subtype, else best token overlap
    plan = {}
    picked = set()
    def pick(st):
        # exact subtype
        for n in idx.get(st, []):
            if n not in picked:
                return n
        # token-overlap best
        want = toks(st)
        best, bestscore = None, 0
        for cand_st, names in idx.items():
            score = len(want & toks(cand_st))
            if score > bestscore:
                for n in names:
                    if n not in picked:
                        best, bestscore = n, score
                        break
        return best

    unmatched = []
    for u in shared:
        st = subtype(u)
        n = pick(st)
        if not n:
            unmatched.append(u); continue
        picked.add(n)
        af = n.split("__")[0]
        plan[u] = {"new_name": n, "af_id": af, "subtype": subtype(n),
                   "old_subtype": st, "path": avail[n]}

    print(f"[plan] matched={len(plan)} unmatched={len(unmatched)}")
    for u in unmatched:
        print("  UNMATCHED:", u, "::", subtype(u), file=sys.stderr)

    (OUT / "swap_plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")

    # extract one QC frame per new clip
    for u, info in plan.items():
        out = QC / f"{info['af_id']}.jpg"
        if out.exists():
            continue
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", "1.0", "-i", info["path"],
                        "-frames:v", "1", "-vf", "scale=480:-1", str(out)], capture_output=True)
    frames = sorted(str(p) for p in QC.glob("*.jpg"))
    print(f"[plan] QC frames extracted: {len(frames)}")
    # contact sheet montage (6 cols)
    if frames:
        lst = OUT / "_frames.txt"
        # use ffmpeg tile
        n = len(frames)
        cols = 6
        rows = (n + cols - 1) // cols
        inputs = []
        for f in frames:
            inputs += ["-i", f]
        filt = f"tile={cols}x{rows}:margin=6:padding=6"
        # pad frames to same size first via scale
        streams = "".join(f"[{i}:v]scale=480:270:force_original_aspect_ratio=decrease,pad=480:270:(ow-iw)/2:(oh-ih)/2,drawtext=text='{Path(frames[i]).stem}':x=6:y=6:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.5[v{i}];" for i in range(n))
        concat = "".join(f"[v{i}]" for i in range(n)) + f"xstack=inputs={n}:layout=" if False else ""
        # simpler: use tile via concat of scaled frames
        filt2 = streams + "".join(f"[v{i}]" for i in range(n)) + f"vstack=inputs={n}" if False else ""
        # fall back to montage grid with tile filter
        cmd = [FFMPEG, "-y", "-loglevel", "error", *inputs,
               "-filter_complex", streams + "".join(f"[v{i}]" for i in range(n)) + f"tile={cols}x{rows}:margin=6:padding=6[out]",
               "-map", "[out]", "-frames:v", "1", str(OUT / "contact.png")]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print("[plan] contact sheet failed:", r.stderr[-400:], file=sys.stderr)
        else:
            print("[plan] contact ->", OUT / "contact.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
