#!/usr/bin/env python3
r"""Stage EP25 Kyllo film assets + build a data-driven cut list for the MotionSample-style render.

Copies the 29 Codex stills and a handful of factory footage clips into the Remotion
public dir, copies the narration master, parses the forced-aligned SRT into caption
cues, and builds a section-aware cut list (image 2.5D cards + footage, ~3-4s cuts,
neighbours never identical) timed to the narration. Output JSON is read by the
`CaseFilm` Remotion composition.

    py -3.11 scripts/build_kyllo_film_assets.py
"""
from __future__ import annotations
import json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-025-kyllo"
FPS = 30
IMG_SRC = ROOT / "episodes" / EP / "04_scenes" / "generated_images" / "codex_v001"
INDEX = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
SRT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
MASTER = MEDIA / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
FACTORY = MEDIA / "assets" / "factory" / "backgrounds"
PUB = ROOT / "remotion" / "public" / "kyllo"
OUT = PUB / "film_data.v001.json"

# footage key -> factory filename
FOOTAGE = {
    "house_night": "AF-BG-1667__suburban_house_exterior_night.mp4",
    "snowy_street": "AF-BG-10712__snowy_street_night.mp4",
    "front_door": "AF-BG-17221__front_door_house.mp4",
    "surveillance": "AF-BG-17987__surveillance_camera_city.mp4",
    "drone_city": "AF-BG-13400__drone_city_aerial_night.mp4",
    "data_center": "AF-BG-1042__data_center.mp4",
    "server_room": "AF-BG-0979__server_room_blue.mp4",
    "tech_abstract": "AF-BG-1119__technology_abstract_blue.mp4",
    "rain_window": "AF-BG-1428__rain_on_window_night.mp4",
    "fog": "AF-BG-0212__moody_atmosphere_fog.mp4",
}

def img(n: int) -> str:
    # resolve COD-S0NN-*.png by number
    hits = sorted(IMG_SRC.glob(f"COD-S{n:03d}-*.png"))
    return hits[0].name if hits else ""

# section (as it appears in narration_index) -> ordered visual pool
# each entry: ("img", N) or ("foot", key)
POOLS = {
    "HOOK": [("img",1),("foot","house_night"),("img",2),("img",18)],
    "OPENING": [("img",16),("foot","snowy_street"),("img",8),("img",2)],
    "ACT I": [("img",3),("img",4),("img",5),("foot","surveillance"),("img",6),("img",18),("img",16),("img",7)],
    "ACT II": [("img",7),("img",19),("foot","front_door"),("img",9),("img",20),("img",21),("img",23),("img",8)],
    "ACT III": [("img",10),("img",24),("img",11),("img",25),("img",12),("img",26),("foot","fog")],
    "ACT IV": [("img",13),("foot","drone_city"),("img",27),("foot","data_center"),("img",28),("foot","tech_abstract"),("img",29),("img",21)],
    "ENDING": [("img",14),("foot","house_night"),("img",8),("img",1),("img",15)],
}
DUR_CYCLE = [3.2, 3.8, 3.4, 4.0, 3.6]  # deterministic cut-length variety (sec)


def parse_srt(path: Path):
    cues = []
    blocks = re.split(r"\n\s*\n", path.read_text("utf-8").strip())
    for b in blocks:
        lines = [x for x in b.splitlines() if x.strip()]
        if len(lines) < 2:
            continue
        m = re.search(r"(\d\d):(\d\d):(\d\d),(\d\d\d)\s*-->\s*(\d\d):(\d\d):(\d\d),(\d\d\d)", lines[1])
        if not m:
            continue
        g = list(map(int, m.groups()))
        s = g[0]*3600+g[1]*60+g[2]+g[3]/1000
        e = g[4]*3600+g[5]*60+g[6]+g[7]/1000
        text = " ".join(lines[2:]).strip()
        if text:
            cues.append({"start": round(s,3), "end": round(e,3), "text": text})
    return cues


def section_at(t: float, chunks):
    for c in chunks:
        if c["start"] <= t < c["end"]:
            return c["section"].upper()
    return chunks[-1]["section"].upper()


def norm_section(sec: str) -> str:
    for k in POOLS:
        if sec.startswith(k):
            return k
    return "ACT I"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    PUB.mkdir(parents=True, exist_ok=True)
    (PUB/"img").mkdir(exist_ok=True)
    (PUB/"footage").mkdir(exist_ok=True)

    # copy stills
    for p in sorted(IMG_SRC.glob("COD-S*.png")):
        shutil.copy2(p, PUB/"img"/p.name)
    # copy footage
    for key, fn in FOOTAGE.items():
        src = FACTORY / fn
        if src.exists():
            shutil.copy2(src, PUB/"footage"/f"{key}.mp4")
        else:
            print(f"  WARN missing footage {fn}")
    # copy narration
    shutil.copy2(MASTER, PUB/"narration.mp3")

    idx = json.loads(INDEX.read_text("utf-8"))
    chunks = idx["chunks"]
    T = max(c["end"] for c in chunks)
    cues = parse_srt(SRT)

    # build cut list across 0..T, section-aware, round-robin per pool, no identical neighbours
    cuts = []
    pool_ptr = {k: 0 for k in POOLS}
    t = 0.0
    di = 0
    last_src = None
    while t < T - 0.4:
        sec = norm_section(section_at(t, chunks))
        pool = POOLS[sec]
        # pick next asset in this pool that isn't identical to the previous cut
        asset = None
        for _ in range(len(pool)):
            cand = pool[pool_ptr[sec] % len(pool)]
            pool_ptr[sec] += 1
            kind, ref = cand
            src = f"img/{img(ref)}" if kind == "img" else f"footage/{ref}.mp4"
            if src != last_src and src != "img/":
                asset = (kind, src)
                break
        if asset is None:
            kind, ref = pool[pool_ptr[sec] % len(pool)]
            src = f"img/{img(ref)}" if kind == "img" else f"footage/{ref}.mp4"
            asset = (kind, src)
        kind, src = asset
        dur = DUR_CYCLE[di % len(DUR_CYCLE)]; di += 1
        if t + dur > T:
            dur = round(T - t, 3)
        treatment = "footage" if kind == "foot" else ("card" if di % 2 == 0 else "push")
        cuts.append({
            "start": round(t, 3),
            "dur": round(dur, 3),
            "kind": "footage" if kind == "foot" else "img",
            "src": src,
            "treatment": treatment,
            "seed": f"kyllo-{len(cuts)}",
        })
        last_src = src
        t += dur

    data = {
        "episode_id": EP,
        "fps": FPS,
        "narration": "kyllo/narration.mp3",
        "narrationSeconds": round(T, 3),
        "cuts": [{**c, "src": f"kyllo/{c['src']}"} for c in cuts],
        "captions": cues,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
    srcdata = ROOT / "remotion" / "src" / "data" / "kyllo_film.json"
    srcdata.parent.mkdir(parents=True, exist_ok=True)
    srcdata.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
    imgs = sum(1 for c in cuts if c["kind"] == "img")
    foots = sum(1 for c in cuts if c["kind"] == "footage")
    print(f"cuts={len(cuts)} (img={imgs} footage={foots}) narration={T:.1f}s cues={len(cues)}")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
