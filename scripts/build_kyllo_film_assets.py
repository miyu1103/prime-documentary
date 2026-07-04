#!/usr/bin/env python3
r"""Stage EP25 Kyllo film assets + build a HIGH-VARIETY, no-repeat cut list.

v002 (owner feedback: "reuses the same assets too much / no hook"):
- draws factory from a large pool scanned from public/kyllo/factory (dozens of clips),
- classifies each clip by filename theme and maps it to the right act,
- picks cuts with a no-repeat rule (least-used, not seen in the last N cuts) so neighbours
  and near-neighbours never look alike,
- emits an 8-second cold-open HOOK montage (the most striking shots) played BEFORE the
  brand opening, so the film opens on a hook -> opening -> body -> endcard.

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
PUB = ROOT / "remotion" / "public" / "kyllo"
FOOT_DIR = PUB / "factory"
OUT = PUB / "film_data.v001.json"

def imgname(n: int) -> str:
    hits = sorted(IMG_SRC.glob(f"COD-S{n:03d}-*.png"))
    return hits[0].name if hits else ""

# each still assigned to ONE primary act (reduces reuse)
IMG_SECTION = {
    "HOOK": [1, 2], "OPENING": [16, 17],
    "ACT I": [3, 4, 5, 6, 18], "ACT II": [7, 8, 9, 19, 20, 22, 23],
    "ACT III": [10, 11, 12, 24, 25, 26], "ACT IV": [13, 21, 27, 28, 29], "ENDING": [14, 15],
}
# factory theme keywords allowed per act (a clip may serve several acts; spacing handles reuse)
SECTION_THEMES = {
    "HOOK": ["thermal", "infrared", "heat", "house", "reveal", "glow", "night_sky", "surveillance"],
    "OPENING": ["house", "home", "window", "curtain", "porch", "suburb", "winter", "snow", "night", "moon", "fog"],
    "ACT I": ["surveillance", "camera", "cctv", "security", "car", "headlight", "dashboard", "thermal", "scan", "radar", "street", "night", "infrared"],
    "ACT II": ["door", "window", "curtain", "lock", "key", "porch", "house", "home", "wall", "rain", "fog"],
    "ACT III": ["court", "gavel", "marble", "pillar", "supreme", "document", "paper", "ledger", "archive", "blueprint", "flag", "capitol", "monument", "map"],
    "ACT IV": ["drone", "aerial", "data", "server", "technology", "circuit", "fiber", "network", "satellite", "radar", "sensor", "city", "skyline", "scan"],
    "ENDING": ["home", "door", "house", "night", "sky", "moon", "forest", "dawn", "bokeh", "light_ray", "particle"],
}
DUR_CYCLE = [3.0, 3.6, 3.2, 4.0, 3.4, 2.8]
MIN_GAP = 22  # don't reuse an asset within this many cuts


def parse_srt(path: Path):
    cues = []
    for b in re.split(r"\n\s*\n", path.read_text("utf-8").strip()):
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
            cues.append({"start": round(s, 3), "end": round(e, 3), "text": text})
    return cues


def norm_section(sec: str) -> str:
    sec = sec.upper()
    for k in SECTION_THEMES:
        if sec.startswith(k):
            return k
    return "ACT I"


def section_at(t, chunks):
    for c in chunks:
        if c["start"] <= t < c["end"]:
            return norm_section(c["section"])
    return norm_section(chunks[-1]["section"])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    (PUB / "img").mkdir(parents=True, exist_ok=True)
    FOOT_DIR.mkdir(parents=True, exist_ok=True)
    for p in sorted(IMG_SRC.glob("COD-S*.png")):
        shutil.copy2(p, PUB / "img" / p.name)
    shutil.copy2(MASTER, PUB / "narration.mp3")

    # factory already staged in FOOT_DIR by the shell step; classify by filename theme
    foot_files = sorted(f.name for f in FOOT_DIR.glob("*.mp4"))
    def foot_themes(fn):
        low = fn.lower()
        return [kw for themes in SECTION_THEMES.values() for kw in themes if kw in low]

    # build per-section asset pools: images (primary) + themed factory
    pools = {}
    for sec, themes in SECTION_THEMES.items():
        imgs = [("img", f"img/{imgname(n)}") for n in IMG_SECTION.get(sec, []) if imgname(n)]
        foots = [("foot", f"factory/{fn}") for fn in foot_files if any(kw in fn.lower() for kw in themes)]
        pools[sec] = imgs + foots

    idx = json.loads(INDEX.read_text("utf-8"))
    chunks = idx["chunks"]
    T = max(c["end"] for c in chunks)
    cues = parse_srt(SRT)

    # still treatments: 'card' (the diagonal 2.5D) is RARE; others carry the variety
    IMG_TREAT = ['bleed', 'scan', 'duotone', 'focus', 'bleed', 'duotone', 'card', 'scan', 'focus', 'bleed', 'duotone', 'scan']
    ALL_IMG = [("img", f"img/{imgname(n)}") for n in range(1, 30) if imgname(n)]
    ALL_FOOT = [("foot", f"factory/{fn}") for fn in foot_files]
    KIND = ['img', 'foot', 'img', 'foot', 'foot']  # ~40% stills, 60% factory; both high-variety
    used = {}      # src -> times used
    last = {}      # src -> last cut index

    def pick(primary, allpool, i):
        def key(a):
            return (used.get(a[1], 0), last.get(a[1], -999))
        for p in (primary, allpool):
            elig = [a for a in p if i - last.get(a[1], -999) > MIN_GAP]
            if elig:
                return sorted(elig, key=key)[0]
        return sorted(allpool, key=key)[0]

    cuts = []
    t = 0.0; di = 0; img_ct = 0; last_treat = None
    while t < T - 0.4:
        sec = section_at(t, chunks)
        i = len(cuts)
        want = KIND[i % len(KIND)]
        if want == "img":
            sec_imgs = [a for a in pools[sec] if a[0] == "img"]
            kind, src = pick(sec_imgs, ALL_IMG, i)
        else:
            # factory draws from the WHOLE 80-clip pool so every clip gets used and
            # nothing clusters (stills carry the specific beat; factory is the motion/variety layer)
            kind, src = pick(ALL_FOOT, ALL_FOOT, i)
        dur = DUR_CYCLE[di % len(DUR_CYCLE)]; di += 1
        if t + dur > T:
            dur = round(T - t, 3)
        if kind == "foot":
            treatment = "factory"
        else:
            treatment = IMG_TREAT[img_ct % len(IMG_TREAT)]; img_ct += 1
            if treatment == last_treat:
                treatment = IMG_TREAT[img_ct % len(IMG_TREAT)]; img_ct += 1
            last_treat = treatment
        cuts.append({
            "start": round(t, 3), "dur": round(dur, 3),
            "kind": "footage" if kind == "foot" else "img",
            "src": f"kyllo/{src}", "seed": f"kyllo-{i}", "treatment": treatment,
        })
        used[src] = used.get(src, 0) + 1
        last[src] = i
        t += dur

    # 8s cold-open HOOK: the most striking, fast (~1.3s) cuts, no narration
    hero = [1, 6, 5, 27, 19, 10]  # thermal reveal, heat scan, device, drone-thermal, heat-presence, courthouse
    hook_cuts = []
    ht = 0.0
    for n in hero:
        nm = imgname(n)
        if nm:
            hook_cuts.append({"start": round(ht, 3), "dur": 1.34, "kind": "img", "src": f"kyllo/img/{nm}", "seed": f"hook-{n}"})
            ht += 1.34

    # GRAPHICS BEATS: the DESIGNED on_screen_text per span (script.annotated), rendered as
    # big kinetic-typography / motion-graphics moments, timed to the span's narration chunk.
    # spans (SPN-000N) map 1:1, in order, to narration chunks (VC-000N).
    ann = json.loads((ROOT / "episodes" / EP / "03_script" / "script.annotated.v001.json").read_text("utf-8"))
    spans = ann.get("spans", [])
    beats = []
    for i, ch in enumerate(chunks):
        if i >= len(spans):
            break
        ost = spans[i].get("on_screen_text") or []
        if not ost:
            continue
        bs = ch["start"]
        be = min(ch["end"] - 0.3, bs + 5.6)  # punchy hold, then fade; not the whole span
        if be - bs < 1.4:
            be = min(ch["end"] - 0.1, bs + 1.4)
        beats.append({"start": round(bs, 3), "end": round(be, 3), "lines": [s for s in ost if s.strip()]})

    data = {
        "episode_id": EP, "fps": FPS,
        "narration": "kyllo/narration.mp3", "narrationSeconds": round(T, 3),
        "hookSeconds": round(ht, 3),
        "hookLine": "The police scanned his home—from the street.",
        "hook": hook_cuts,
        "cuts": cuts, "captions": cues, "graphics": beats,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
    (ROOT / "remotion" / "src" / "data" / "kyllo_film.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")

    imgs = sum(1 for c in cuts if c["kind"] == "img")
    foots = sum(1 for c in cuts if c["kind"] == "factory")
    distinct = len(set(c["src"] for c in cuts))
    maxreuse = max(used.values()) if used else 0
    print(f"factory pool={len(foot_files)}  cuts={len(cuts)} (img={imgs} factory={foots})  distinct_assets={distinct}  max_reuse={maxreuse}  hook={len(hook_cuts)}cuts/{ht:.1f}s  narration={T:.1f}s cues={len(cues)}")
    print(f"wrote {OUT.relative_to(ROOT)} + src/data/kyllo_film.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
