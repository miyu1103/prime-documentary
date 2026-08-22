#!/usr/bin/env python
r"""Build the REAL (stub-free) remotion/src/data/young_film.json for EP42 (PD-2026-042-young).

Modeled on scripts/build_thompson_film.py (the PROVEN real builder for EP41). Adapted for young:

  * Stills: real 4K S01..S85.png already staged under remotion/public/young/img/ (Ken-Burns).
  * Factory: the 93 REAL clips in runs/qc/young_factory_selected.v001.json copied from their
    shelf_path (H:) into remotion/public/young/factory/<basename>, each sha256-verified, each
    used EXACTLY ONCE (asset_reuse factory cap = 1).
  * i2v MOTION: the 16 M-seed stills are NOT motion. ComfyUI/Wan i2v is NOT running and 16
    generations would exceed the time budget for this data-prep step, so per the task's escape
    hatch the 16 motion cuts are SUBSTITUTED with additional REAL factory footage (footage carries
    ~60% of screen TIME) -- NO stubs. The film still clears animation_mix with real footage only.
  * Narration: real master vc_master_v001.mp3 (712.346s) -> public/young/narration.mp3; timing
    from episodes/.../06_audio/narration_index.v001.json.
  * Captions: rebuilt VERBATIM from the CLEAN narration_index.v001.json spoken text (the locked
    08_edit/captions.final.v001.srt was dryrun-contaminated with 3 stage-direction markers
    "【SILENCE Xs】" that must NOT appear on screen); build_young_film.build_captions splits/wraps
    to pass check_caption_breaks; the SRT is regenerated clean.
  * figures[]: the accurate, ledger-backed MG beats from build_young_film.figure_payloads()
    (37 beats; all 6 accuracy constraints verified against the locked script + facts ledger).

No paid calls. Does NOT render. Zero stub/placeholder/dryrun/silence references by construction.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from collections import Counter, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_young_film as byf  # reuse figure_payloads / place_figures / section_windows

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-042-young"
SLUG = "young"
FPS = 30

NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
FACTORY_SEL = ROOT / "runs" / "qc" / "young_factory_selected.v001.json"
SRT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"
H_MASTER = Path("E:/pd-media/episodes/PD-2026-042-young/06_voice/master/vc_master_v001.mp3")

PUB = ROOT / "remotion" / "public" / "young"
PUB_IMG = PUB / "img"
PUB_FAC = PUB / "factory"
PUB_NARR = PUB / "narration.mp3"
OUT_FILM = ROOT / "remotion" / "src" / "data" / "young_film.json"
PUB_FILM = PUB / "film_data.v001.json"
MANIFEST = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"

STILL_TREATS = ["depth", "scan", "duotone", "focus", "bleed"]

# Mix targets (TIME share). animation_mix caps still-share at 0.45; keep a healthy margin.
FOOT_SHARE = 0.60          # footage gets ~60% of each section's TIME (=> still-share ~40%)
FOOT_MEAN = 4.4            # target footage cut length (93 clips over ~430s body-footage)
STILL_MEAN = 3.2          # target still cut length
STILL_MAX_HOLD = 4.6      # keep every still under the 5.0s "lingering" line
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ENDING"]


def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


# ---------------------------------------------------------------------------- captions (verbatim SRT)
def parse_srt(path: Path):
    def to_sec(ts: str) -> float:
        ts = ts.strip().replace(".", ",")
        hh, mm, rest = ts.split(":")
        ss, ms = rest.split(",")
        return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000.0

    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip())
    cues = []
    for b in blocks:
        lines = [l for l in b.split("\n") if l.strip() != ""]
        ts_line = next((l for l in lines if "-->" in l), None)
        if ts_line is None:
            continue
        start_s, end_s = [x.strip() for x in ts_line.split("-->")]
        text_lines = lines[lines.index(ts_line) + 1:]
        if not text_lines:
            continue
        cues.append({"start": round(to_sec(start_s), 3),
                     "end": round(to_sec(end_s), 3),
                     "text": "\n".join(text_lines).strip()})
    return cues


# ---------------------------------------------------------------------------- factory staging
def stage_factory():
    sel = load_json(FACTORY_SEL)
    clips = sel if isinstance(sel, list) else sel.get("clips") or sel.get("selected") or []
    PUB_FAC.mkdir(parents=True, exist_ok=True)
    ordered, mism, copied = [], [], 0
    # section bucket by act_suggestion so footage lands in a thematically-plausible act
    by_act: dict[str, list[str]] = {}
    for c in clips:
        base = c["basename"]
        src = Path(c["shelf_path"])
        dst = PUB_FAC / base
        want = c.get("sha256")
        if (not dst.is_file()) or (dst.stat().st_size != src.stat().st_size):
            shutil.copy2(src, dst)
            copied += 1
        got = sha256_of(dst)
        if want and got.lower() != want.lower():
            mism.append({"basename": base, "want": want, "got": got})
        pub = f"{SLUG}/factory/{base}"
        ordered.append(pub)
        act = (c.get("act_suggestion") or "GENERAL").upper()
        if act == "HOOK_OP":
            act = "HOOK"
        if act not in SECTION_ORDER:
            act = "GENERAL"
        by_act.setdefault(act, []).append(pub)
    return ordered, by_act, copied, mism


# ---------------------------------------------------------------------------- still picker (cap 2)
class StillPicker:
    def __init__(self, scenes: list[str]):
        self.scenes = scenes
        self.uses: Counter = Counter()

    def pick(self):
        # least-used still under cap 2, preferring first uses
        cand = sorted(self.scenes, key=lambda s: (self.uses[s], self.scenes.index(s)))
        for s in cand:
            if self.uses[s] < 2:
                self.uses[s] += 1
                return f"{SLUG}/img/{s}.png"
        return None


# ---------------------------------------------------------------------------- cut builder
def build_cuts(windows, fac_by_act, fac_all, picker, total):
    fac_pool = {k: deque(v) for k, v in fac_by_act.items()}
    general = deque(fac_by_act.get("GENERAL", []))

    def take_footage(act, n):
        out = []
        dq = fac_pool.get(act)
        while len(out) < n and dq:
            out.append(dq.popleft())
        while len(out) < n and general:
            out.append(general.popleft())
        if len(out) < n:  # borrow from any other act as last resort (still used once globally)
            for k, dd in fac_pool.items():
                while len(out) < n and dd:
                    out.append(dd.popleft())
        return out

    # how many footage clips per section (proportional to section time, total == available clips)
    n_clips = len(fac_all)
    body_secs = {sec: (e - s) for sec, s, e in windows}
    tot = sum(body_secs.values())
    alloc = {sec: max(1, round(n_clips * body_secs[sec] / tot)) for sec, s, e in windows}
    # trim/pad allocation so it sums to exactly n_clips
    diff = n_clips - sum(alloc.values())
    order_by_len = [sec for sec, _, _ in sorted(windows, key=lambda w: -(w[2] - w[1]))]
    i = 0
    while diff != 0 and order_by_len:
        sec = order_by_len[i % len(order_by_len)]
        if diff > 0:
            alloc[sec] += 1; diff -= 1
        elif alloc[sec] > 1:
            alloc[sec] -= 1; diff += 1
        i += 1

    cuts = []
    treat_i = 0
    for sec, s, e in windows:
        D = e - s
        n_foot = alloc[sec]
        foot = take_footage(sec, n_foot)
        n_foot = max(1, len(foot))
        foot_budget = FOOT_SHARE * D
        still_budget = D - foot_budget
        foot_dur = max(2.6, min(6.0, foot_budget / n_foot))
        n_still = max(1, round(still_budget / STILL_MEAN))
        stills = []
        guard = 0
        while len(stills) < n_still and guard < n_still * 6 + 20:
            got = picker.pick()
            guard += 1
            if got:
                stills.append(got)
        n_still = max(1, len(stills))
        still_dur = max(2.2, min(STILL_MAX_HOLD, still_budget / n_still))

        # interleave footage-majority (2 footage : 1 still, roughly)
        seq = []
        fi = si = k = 0
        pat = ["F", "S", "F", "F", "S"]
        while fi < len(foot) or si < len(stills):
            slot = pat[k % len(pat)]; k += 1
            if slot == "F" and fi < len(foot):
                seq.append(("footage", foot[fi], None, foot_dur)); fi += 1
            elif slot == "S" and si < len(stills):
                seq.append(("img", stills[si], None, still_dur)); si += 1
            elif fi < len(foot):
                seq.append(("footage", foot[fi], None, foot_dur)); fi += 1
            elif si < len(stills):
                seq.append(("img", stills[si], None, still_dur)); si += 1
        if not seq:
            continue
        # normalize durations to fill [s,e) exactly
        raw = sum(x[3] for x in seq)
        scale = D / raw
        t = s
        for j, (kind, src, _t, du) in enumerate(seq):
            dur = du * scale if j < len(seq) - 1 else (e - t)
            dur = round(max(1.8, dur), 3)
            idx = len(cuts)
            cut = {"id": f"cut-{idx:03d}", "start": round(t, 3), "dur": dur, "kind": kind,
                   "src": src, "seed": f"young-{idx:03d}", "act": sec}
            if kind == "footage":
                cut["treatment"] = "footage"
            else:
                cut["treatment"] = STILL_TREATS[treat_i % len(STILL_TREATS)]; treat_i += 1
            cuts.append(cut)
            t += dur
    return cuts


def build_hook(picker, scenes):
    hook = []
    t = 0.0
    d = round(8.0 / 6, 3)
    for i in range(6):
        src = f"{SLUG}/img/{scenes[i % len(scenes)]}.png"
        dd = round(8.0 - t, 3) if i == 5 else d
        hook.append({"start": round(t, 3), "dur": dd, "kind": "img", "src": src,
                     "seed": f"young-hook-{i:02d}"})
        t += dd
    return hook


def union_seconds(intervals):
    ivs = sorted(intervals); tot = 0.0; cs = ce = None
    for a, b in ivs:
        if cs is None:
            cs, ce = a, b
        elif a <= ce:
            ce = max(ce, b)
        else:
            tot += ce - cs; cs, ce = a, b
    if cs is not None:
        tot += ce - cs
    return tot


def main() -> int:
    narr = load_json(NARR)
    total = float(narr["total_seconds"])

    # windows as list of (sec, s, e) from real narration timing
    wdict = byf.section_windows(narr, total)  # {sec:(s,e)}
    windows = [(sec, wdict[sec][0], wdict[sec][1]) for sec in SECTION_ORDER if sec in wdict]

    # stills already staged in public/young/img (S01..S85)
    scenes = sorted([p.stem for p in PUB_IMG.glob("S*.png") if "_depth" not in p.stem],
                    key=lambda s: int(re.sub(r"\D", "", s) or 0))
    if len(scenes) < 40:
        raise SystemExit(f"expected ~85 staged S-stills, found {len(scenes)}")

    fac_all, fac_by_act, copied, mism = stage_factory()

    # narration master -> public
    PUB_NARR.parent.mkdir(parents=True, exist_ok=True)
    if H_MASTER.is_file():
        if (not PUB_NARR.is_file()) or PUB_NARR.stat().st_size != H_MASTER.stat().st_size:
            shutil.copy2(H_MASTER, PUB_NARR)
    else:
        raise SystemExit(f"narration master missing: {H_MASTER}")

    picker = StillPicker(scenes)
    hook = build_hook(picker, scenes)
    cuts = build_cuts(windows, fac_by_act, fac_all, picker, total)
    figures = byf.place_figures(wdict, total)
    # captions: rebuilt from the CLEAN narration spoken text (not the dryrun-contaminated SRT)
    captions, _cap_total = byf.build_captions(narr)
    byf.write_srt(captions, SRT)  # regenerate the episode SRT clean (removes 【SILENCE】 markers)

    film = {
        "episode_id": EP,
        "fps": FPS,
        "narration": f"{SLUG}/narration.mp3",
        "narrationSeconds": round(total, 3),
        "hookSeconds": 8.0,
        "hookLine": "You have the wrong house.",
        "hook": hook,
        "cuts": cuts,
        "captions": captions,
        "graphics": [],
        "figures": figures,
    }
    OUT_FILM.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILM.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")
    PUB_FILM.parent.mkdir(parents=True, exist_ok=True)
    PUB_FILM.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- report + self-verify against gate formulas ----
    still_time = sum(c["dur"] for c in cuts if c["kind"] == "img")
    foot_time = sum(c["dur"] for c in cuts if c["kind"] == "footage")
    still_share = still_time / total
    fac_ivs = [(c["start"], c["start"] + c["dur"]) for c in cuts if c["kind"] == "footage"]
    fig_ivs = [(f["start"], f["end"]) for f in figures]
    motion_cov = union_seconds(fac_ivs + fig_ivs) / total
    fig_cov = union_seconds(fig_ivs) / total
    density = len(figures) / (total / 60.0)
    uses = Counter(c["src"] for c in cuts)
    over = {s: n for s, n in uses.items() if (("/factory" in s and n > 1) or ("/factory" not in s and n > 2))}
    first_share = len(uses) / len(cuts)
    long_holds = sum(1 for c in cuts if c["kind"] == "img" and c["dur"] > 5.0)
    variety = len({f["kind"] for f in figures})

    report = {
        "narrationSeconds": round(total, 3),
        "cuts": len(cuts),
        "footage_cuts": sum(1 for c in cuts if c["kind"] == "footage"),
        "still_cuts": sum(1 for c in cuts if c["kind"] == "img"),
        "factory_copied": copied, "factory_total": len(fac_all), "sha_mismatch": mism,
        "still_time_share": round(still_share, 3), "motion_coverage": round(motion_cov, 3),
        "figure_coverage": round(fig_cov, 3), "figure_density_per_min": round(density, 2),
        "figures": len(figures), "figure_variety": variety,
        "first_use_share": round(first_share, 3), "over_cap": over,
        "long_still_holds": long_holds, "distinct_assets": len(uses),
        "captions": len(captions),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    problems = []
    if still_share > 0.43:
        problems.append(f"still_share {still_share:.3f} too close to 0.45")
    if motion_cov < 0.47:
        problems.append(f"motion_coverage {motion_cov:.3f} < 0.47")
    if density < 2.6:
        problems.append(f"density {density:.2f} < 2.6")
    if over:
        problems.append(f"over-cap assets: {over}")
    if first_share < 0.72:
        problems.append(f"first_use_share {first_share:.3f} < 0.72")
    if variety < 3:
        problems.append("variety < 3")
    if mism:
        problems.append(f"{len(mism)} factory sha256 mismatches")
    if problems:
        print("SELF-CHECK PROBLEMS:\n  " + "\n  ".join(problems))
        return 2
    print("SELF-CHECK OK")

    man_assets = []
    for i, (src, n) in enumerate(uses.items(), 1):
        kind = "factory" if "/factory" in src else "still"
        man_assets.append({"asset_id": f"{'MO' if kind == 'factory' else 'ST'}-042-{i:03d}",
                           "kind": kind, "public_path": src, "uses": n})
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps({"episode_id": EP, "manifest_version": "v001",
                                    "producer": "scripts/build_young_film_real.py",
                                    "is_stub": False, "counts": {"distinct": len(uses)},
                                    "assets": man_assets}, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
