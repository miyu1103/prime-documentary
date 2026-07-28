#!/usr/bin/env python3
"""EP48 Glover — weave REAL rights-cleared stock MOTION clips into the film at
narration-matched beats (owner 2026-07-24: "せっかくたくさんダウンロードしたんだから
意味のある所に使ってほしい"). Runs AFTER build_glover_film.py: it post-processes the
generated glover_film.json, replacing selected body cuts with stock footage cuts
placed over the narration line they illustrate. Stock cuts render through the
CaseFilm <Footage> path, which applies the unified navy/contrast grade + vignette
+ Ken-Burns push, so real stock sits tonally with the AI stills (color-match).

Idempotent-ish: operates on the freshly built film json. Re-run build_glover_film.py
first if you want a clean base, then run this.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STOCK_SRC = Path("H:/pd-media/assets/stock/video")
PUBDIR = ROOT / "remotion" / "public" / "glover" / "stock"
FILM_SRC = ROOT / "remotion" / "src" / "data" / "glover_film.json"
FILM_PUB = ROOT / "remotion" / "public" / "glover" / "film_data.v001.json"
FFMPEG = shutil.which("ffmpeg") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
SEG = 8.0  # trimmed clip length (frames > any default startFrom of 159)

# (source_file, seg_start_sec, [keyword substrings], min_start_sec, label)
# keyword matched (case-insensitive) against the FIRST caption cue whose start >= min_start.
# Clips vetted US-relevant by the stock audit; daytime establishers are fine as graded cutaways.
PLACEMENTS = [
    # --- ACT 1: the stop ---
    ("pixabay_v_31094.mp4",   3.0,  ["edge of a Kansas town"],                 0.0,   "suburban road/town establisher"),
    ("pixabay_v_12126.mp4",   6.0,  ["pickup truck goes by"],                  6.0,   "POV night driving (a truck goes by)"),
    ("pexels_v_36553218.mp4", 2.0,  ["types the truck's license plate"],       15.0,  "ANPR/plate-reader cameras (running the plate)"),
    ("pexels_v_7140928.mp4",  2.0,  ["the screen answers him"],                24.0,  "records database server racks"),
    ("pexels_v_29635453.mp4", 3.0,  ["your own driveway"],                     49.0,  "house + car in driveway (your own car)"),
    ("pixabay_v_320453.mp4",  1.0,  ["run your plate"],                        53.0,  "CCTV / surveillance camera"),
    ("pexels_v_10476430.mp4", 5.0,  ["pulls the truck over anyway"],           47.0,  "officer at patrol-car door, night (the stop) [PEOPLE]"),
    # --- transition to the legal question ---
    ("pexels_v_29188241.mp4", 4.0,  ["Supreme Court agreed to answer"],        82.0,  "US Supreme Court building"),
    ("pexels_v_5636977.mp4",  1.0,  ["the stop itself was allowed"],           90.0,  "gavel + scales (was the stop allowed)"),
    ("pexels_v_6101367.mp4",  1.0,  ["the Court gave its answer"],            102.0,  "judge striking gavel (the ruling) [PEOPLE]"),
    # --- ACT 2 recap: facts / patrol / plate / records ---
    ("pexels_v_6581288.mp4",  2.0,  ["was on patrol"],                       122.0,  "US police cruiser on patrol"),
    ("pixabay_v_10822.mp4",   1.0,  ["ran a routine check on the license"],   126.0,  "hands typing (running the check)"),
    ("pexels_v_7140928.mp4",  4.0,  ["the truck was registered to"],         139.0,  "registration record returns (database)"),
    ("pixabay_v_302857.mp4",  0.5,  ["serious or repeated pattern"],         149.0,  "night wrecked car + police lights (revoked-license stakes)"),
    ("pexels_v_5243246.mp4",  1.0,  ["lost the privilege to drive"],         154.0,  "jail cell bars (consequence)"),
    ("pixabay_v_12126.mp4",  12.0,  ["probably being driven by the man"],    169.0,  "POV night driving (the inference)"),
    ("pexels_v_10476430.mp4",12.0,  ["So he made the stop"],                 177.0,  "officer at patrol-car door (the stop) [PEOPLE]"),
    # --- ACT 2: the Fourth Amendment / standards ---
    ("pexels_v_8061661.mp4",  2.0,  ["Fourth Amendment protects you"],       226.0,  "Lady Justice + certificate (Fourth Amendment)"),
    ("pexels_v_29188235.mp4", 3.0,  ["highest court in the country"],        219.0,  "US Capitol (highest court establisher)"),
    ("pexels_v_5636967.mp4",  1.0,  ["it sits in between"],                  270.0,  "scales of justice (reasonable suspicion in between)"),
    # --- ruling / your car ending ---
    ("pexels_v_29188241.mp4", 10.0, ["the highest court in the country"],    219.0,  "US Supreme Court building (reuse)"),
    ("pexels_v_17040253.mp4", 2.0,  ["Prime Documentary"],                   110.0,  "US flag (section transition)"),
]


def probe(path: Path) -> float:
    r = subprocess.run([FFMPEG.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1.0


def transcode(src: Path, seg_start: float, dst: Path) -> None:
    if dst.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    dur = probe(src)
    ss = max(0.0, min(seg_start, max(0.0, dur - SEG - 0.2))) if dur > 0 else seg_start
    cmd = [FFMPEG, "-y", "-hide_banner", "-ss", f"{ss:.2f}", "-t", f"{SEG:.2f}", "-i", str(src),
           "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1",
           "-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-colorspace", "bt709", str(dst)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode or not dst.exists():
        raise SystemExit(f"transcode failed {src.name}: {r.stderr[-800:]}")


def main() -> int:
    film = json.loads(FILM_SRC.read_text(encoding="utf-8"))
    caps = film["captions"]
    cuts = film["cuts"]
    used_cut_ids: set[str] = set()
    report = []
    # unique source -> destination public path (dedupe transcodes by (file, seg_start))
    seg_key = {}
    for src_file, seg_start, keywords, min_start, label in PLACEMENTS:
        stem = Path(src_file).stem
        key = f"{stem}_{int(seg_start)}"
        dst = PUBDIR / f"{key}.mp4"
        if key not in seg_key:
            transcode(STOCK_SRC / src_file, seg_start, dst)
            seg_key[key] = f"glover/stock/{key}.mp4"
        pub = seg_key[key]
        # find caption
        cue = next((c for c in caps if c["start"] >= min_start - 0.01
                    and any(k.lower() in c["text"].lower() for k in keywords)), None)
        if cue is None:
            report.append((None, None, f"NO-CAPTION-MATCH {keywords}", label))
            continue
        t = cue["start"]
        # find a body cut covering t that isn't already replaced; else nearest unused
        idx = next((i for i, c in enumerate(cuts)
                    if c["start"] <= t < c["start"] + c["dur"] and c["id"] not in used_cut_ids), None)
        if idx is None:
            # nearest unused cut by start
            cand = sorted((i for i, c in enumerate(cuts) if c["id"] not in used_cut_ids),
                          key=lambda i: abs(cuts[i]["start"] - t))
            idx = cand[0] if cand else None
        if idx is None:
            report.append((t, None, "NO-FREE-CUT", label))
            continue
        c = cuts[idx]
        used_cut_ids.add(c["id"])
        c["src"] = pub
        c["kind"] = "footage"
        c["treatment"] = "footage"
        c["startFrom"] = 0
        c["stock"] = True
        c["stock_label"] = label
        report.append((round(t, 2), c["id"], pub, cue["text"][:70]))

    FILM_SRC.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")
    FILM_PUB.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"stock cuts woven: {len([r for r in report if r[1]])}")
    for t, cid, pub, txt in report:
        print(f"  t={t} cut={cid} :: {pub if isinstance(pub,str) else ''} | {txt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
