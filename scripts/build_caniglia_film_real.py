#!/usr/bin/env python
r"""Build the REAL (stub-free) remotion/src/data/caniglia_film.json for EP43 (PD-2026-043-caniglia).

Modeled on scripts/build_young_film_real.py (the PROVEN real builder used for EP42). Adapted for
caniglia:

  * Stills: the REAL 4K SDXL stills staged under remotion/public/caniglia/img/ (Ken-Burns). Only the
    stills that actually EXIST on disk are used -- the builder globs S*.png, so any missing block
    (S51-S55, which have not been generated yet) is simply never referenced. NO stub/placeholder.
  * Factory: the 93 REAL clips in runs/qc/caniglia_factory_selected.v001.json, already staged under
    remotion/public/caniglia/factory/<basename>, each sha256-verified, each used EXACTLY ONCE
    (asset_reuse factory cap = 1). Factory footage carries ~60% of screen TIME and, because it is
    interleaved across every section, it inherently COVERS the cut-slots that the missing stills
    (and the never-generated i2v motion clips) would otherwise have filled -- with REAL moving
    footage, not stubs.
  * i2v MOTION: the 16 M-seed stills are NOT motion videos and no real i2v mp4s exist. Per the EP42
    escape hatch the motion cuts are SUBSTITUTED with additional REAL factory footage -- NO stubs.
  * Narration: real master vc_master_v001.mp3 -> public/caniglia/narration.mp3; timing from
    episodes/.../06_audio/narration_index.v001.json (total 732.386s).
  * Captions: VERBATIM from the CLEAN narration spoken text (160 cues); the episode SRT is
    regenerated identically. (The real captions.final.v001.srt already passes check_caption_breaks.)
  * figures[]: designed MG beats -- all-lowercase kinds, NO 'dochighlight' (banned), variety >=3,
    ledger-backed against episodes/.../caniglia_facts.v001.json + the locked script, all 6 accuracy
    constraints held (see figure_payloads()).

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
import build_caniglia_film as bcf  # reuse section_windows / build_captions / write_srt

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-043-caniglia"
SLUG = "caniglia"
FPS = 30

NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
FACTORY_SEL = ROOT / "runs" / "qc" / "caniglia_factory_selected.v001.json"
SRT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"
H_MASTER = Path("E:/pd-media/episodes/PD-2026-043-caniglia/06_voice/master/vc_master_v001.mp3")

PUB = ROOT / "remotion" / "public" / "caniglia"
PUB_IMG = PUB / "img"
PUB_FAC = PUB / "factory"
PUB_NARR = PUB / "narration.mp3"
SLIM = ROOT / "remotion" / "public_slim" / "caniglia"
OUT_FILM = ROOT / "remotion" / "src" / "data" / "caniglia_film.json"
PUB_FILM = PUB / "film_data.v001.json"
MANIFEST = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"

STILL_TREATS = ["depth", "scan", "duotone", "focus", "bleed"]

FOOT_SHARE = 0.60          # footage gets ~60% of each section's TIME (=> still-share ~40%)
STILL_MEAN = 3.2
STILL_MAX_HOLD = 4.6
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ENDING"]


def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


# ---------------------------------------------------------------------------- factory staging
def stage_factory():
    sel = load_json(FACTORY_SEL)
    clips = sel if isinstance(sel, list) else sel.get("clips") or sel.get("selected") or []
    PUB_FAC.mkdir(parents=True, exist_ok=True)
    (SLIM / "factory").mkdir(parents=True, exist_ok=True)
    ordered, mism, copied = [], [], 0
    by_act: dict[str, list[str]] = {}
    for c in clips:
        base = c["basename"]
        src = Path(c["shelf_path"])
        dst = PUB_FAC / base
        want = c.get("sha256")
        if (not dst.is_file()) or (dst.stat().st_size != src.stat().st_size):
            shutil.copy2(src, dst)
            copied += 1
        # mirror into public_slim
        slim_dst = SLIM / "factory" / base
        if (not slim_dst.is_file()) or (slim_dst.stat().st_size != dst.stat().st_size):
            shutil.copy2(dst, slim_dst)
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
        if len(out) < n:
            for k, dd in fac_pool.items():
                while len(out) < n and dd:
                    out.append(dd.popleft())
        return out

    n_clips = len(fac_all)
    body_secs = {sec: (e - s) for sec, s, e in windows}
    tot = sum(body_secs.values())
    alloc = {sec: max(1, round(n_clips * body_secs[sec] / tot)) for sec, s, e in windows}
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
        raw = sum(x[3] for x in seq)
        scale = D / raw
        t = s
        for j, (kind, src, _t, du) in enumerate(seq):
            dur = du * scale if j < len(seq) - 1 else (e - t)
            dur = round(max(1.8, dur), 3)
            idx = len(cuts)
            cut = {"id": f"cut-{idx:03d}", "start": round(t, 3), "dur": dur, "kind": kind,
                   "src": src, "seed": f"{SLUG}-{idx:03d}", "act": sec}
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
                     "seed": f"{SLUG}-hook-{i:02d}"})
        t += dd
    return hook


# ---------------------------------------------------------------------------- figures (MG beats)
def K(lines, emph=None, style="maskslide"):
    d = {"kind": "kinetic", "lines": lines, "style": style}
    if emph:
        d["emphasisWords"] = emph
    return d


def figure_payloads() -> list[dict]:
    r"""Designed motion-graphics beats. All-lowercase kinds; NO 'dochighlight' (banned).
    Every fact traces to the ledger (caniglia_facts.v001.json) or the locked script.

    ACCURACY CONSTRAINTS (all held):
      1. NO flat "police can't enter the home" rule. The beats state the NARROW holding: the
         community-caretaking exception from Cady does not by itself reach into the home
         (mechanism closingdoor 'community caretaking at home'; 'NOT A WALL AROUND YOUR HOME').
      2. 9-0 is a VACATE-AND-REMAND, not a total win (votetally label 'one excuse closed -
         vacate and remand'; lowerthird 'sent back down / not final disposition').
      3. Cady is a CAR case, not a home case (lowerthird 'police-custody vehicle';
         compbars vehicle 1 / home 0; timeline '1973 Cady - car in custody / 2021 Caniglia - home').
      4. NO face is shown on any figure (lowerthird 'AI-assisted visualization / symbolic
         reconstruction'); figures are typographic/data cards only.
      5. 988 appears on NO figure (F14 is deliberately omitted from all beats).
      6. Citations are verbatim from the ledger (First Circuit 953 F.3d 112 (2020); Caniglia v.
         Strom 593 U.S. 194 (2021), No. 20-157; Cady v. Dombrowski) and warrant/consent/emergency
         aid are shown as STILL-OPEN doors, not as anything the Court decided.
    """
    return [
        K(["THE WELFARE CHECK"], ["WELFARE"], "emphasis"),
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction"},
        {"kind": "mechanism", "mechanism": "closingdoor", "label": "threshold"},
        {"kind": "acttitle", "title": "THE NIGHT", "kicker": "ACT ONE", "index": 1},
        {"kind": "timeline", "events": [{"year": "AUGUST 2015", "text": "Cranston, Rhode Island"}]},
        K(["MAKE SURE", "HE IS OK"], ["OK"], "wordpop"),
        {"kind": "lowerthird", "primary": "non-emergency welfare check", "secondary": "symbolic reconstruction"},
        {"kind": "lowerthird", "primary": "no crime alleged", "secondary": "a welfare check, not an arrest"},
        {"kind": "mechanism", "mechanism": "faultsplit", "left": "care", "right": "search"},
        {"kind": "acttitle", "title": "THE WELFARE CHECK", "kicker": "ACT TWO", "index": 2},
        {"kind": "stat", "value": 2, "label": "handguns seized - no warrant"},
        K(["NO WARRANT"], ["WARRANT"], "emphasis"),
        {"kind": "pindropmap", "pins": [{"x": 0.42, "y": 0.48, "label": "Cranston, RI"}]},
        {"kind": "lowerthird", "primary": "two handguns", "secondary": "logged into evidence"},
        {"kind": "lowerthird", "primary": "First Circuit", "secondary": "953 F.3d 112 (2020)"},
        {"kind": "acttitle", "title": "THE CAR RULE", "kicker": "ACT THREE", "index": 3},
        {"kind": "lowerthird", "primary": "Cady v. Dombrowski", "secondary": "police-custody vehicle"},
        {"kind": "compbars", "items": [{"label": "vehicle", "value": 1}, {"label": "home", "value": 0}]},
        {"kind": "timeline", "events": [{"year": "1973", "text": "Cady - car in custody"}, {"year": "2021", "text": "Caniglia - home"}]},
        {"kind": "regionmap", "label": "lower-court split", "pattern": "varied"},
        {"kind": "acttitle", "title": "THE THRESHOLD", "kicker": "THE COMMAND", "index": 4},
        {"kind": "timeline", "events": [{"year": "MAR 24 2021", "text": "argued"}, {"year": "MAY 17 2021", "text": "decided"}]},
        {"kind": "numberticker", "value": 7, "suffix": " weeks", "label": "argument to decision"},
        {"kind": "lowerthird", "primary": "Caniglia v. Strom", "secondary": "593 U.S. 194 (2021), No. 20-157"},
        {"kind": "quote", "quote": "very core", "attribution": "Florida v. Jardines"},
        {"kind": "votetally", "majority": 9, "dissent": 0, "label": "one excuse closed - vacate and remand"},
        K(["ONE EXCUSE", "CLOSED"], ["EXCUSE"], "emphasis"),
        {"kind": "mechanism", "mechanism": "closingdoor", "label": "community caretaking at home"},
        {"kind": "lowerthird", "primary": "warrant", "secondary": "still open"},
        {"kind": "lowerthird", "primary": "consent", "secondary": "still open"},
        {"kind": "lowerthird", "primary": "emergency aid", "secondary": "still open"},
        {"kind": "quote", "quote": "first among equals", "attribution": "Florida v. Jardines"},
        {"kind": "stat", "value": 3, "label": "separate concurrences"},
        {"kind": "lowerthird", "primary": "sent back down", "secondary": "not final disposition"},
        K(["NOT A WALL", "AROUND YOUR HOME"], ["NOT"], "emphasis"),
        {"kind": "mechanism", "mechanism": "faultsplit", "left": "help", "right": "carry out"},
        K(["WARRANT", "CONSENT", "EMERGENCY"], ["EMERGENCY"], "wordpop"),
        {"kind": "lowerthird", "primary": "what remained open", "secondary": "real emergency aid"},
        {"kind": "timeline", "events": [{"year": "after remand", "text": "hard questions remain"}]},
        {"kind": "mechanism", "mechanism": "closingdoor", "label": "a narrower key"},
        K(["THE DOOR", "IS STILL A DOOR"], ["DOOR"], "emphasis"),
    ]


def place_figures(windows: dict, total: float) -> list[dict]:
    """Distribute the payloads across the acts, non-overlapping, ~5.6s each, keeping clear of the
    endcard tail. Counts sum to 37; variety is ~12 distinct forms."""
    section_counts = [("HOOK", 3), ("ACT_1", 8), ("ACT_2", 8), ("ACT_3", 14), ("ENDING", 4)]
    payloads = deque(figure_payloads())
    figures = []
    dur = 5.6
    BANNED_KINDS = {"dochighlight"}
    for sec, count in section_counts:
        if sec not in windows:
            continue
        s, e = windows[sec]
        lo = s + (4.0 if sec == "HOOK" else 3.0)
        hi = e - 7.0
        if sec == "ENDING":
            hi = min(hi, total - 13.0)
        span = max(dur + 0.5, hi - lo)
        for i in range(count):
            if not payloads:
                break
            start = lo + (span * (i + 0.5) / count) - dur / 2
            payload = payloads.popleft()
            if payload["kind"] in BANNED_KINDS:
                raise SystemExit(f"banned figure kind {payload['kind']}")
            figures.append({"start": round(max(s, start), 3), "end": round(max(s, start) + dur, 3), **payload})
    figures.sort(key=lambda x: x["start"])
    return figures


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

    wdict = bcf.section_windows(narr, total)  # {sec:(s,e)}
    windows = [(sec, wdict[sec][0], wdict[sec][1]) for sec in SECTION_ORDER if sec in wdict]

    scenes = sorted([p.stem for p in PUB_IMG.glob("S*.png") if "_depth" not in p.stem],
                    key=lambda s: int(re.sub(r"\D", "", s) or 0))
    if len(scenes) < 40:
        raise SystemExit(f"expected ~80 staged S-stills, found {len(scenes)}")

    fac_all, fac_by_act, copied, mism = stage_factory()

    # narration master -> public + public_slim
    PUB_NARR.parent.mkdir(parents=True, exist_ok=True)
    if not H_MASTER.is_file():
        raise SystemExit(f"narration master missing: {H_MASTER}")
    if (not PUB_NARR.is_file()) or PUB_NARR.stat().st_size != H_MASTER.stat().st_size:
        shutil.copy2(H_MASTER, PUB_NARR)
    slim_narr = SLIM / "narration.mp3"
    slim_narr.parent.mkdir(parents=True, exist_ok=True)
    if (not slim_narr.is_file()) or slim_narr.stat().st_size != PUB_NARR.stat().st_size:
        shutil.copy2(PUB_NARR, slim_narr)

    picker = StillPicker(scenes)
    hook = build_hook(picker, scenes)
    cuts = build_cuts(windows, fac_by_act, fac_all, picker, total)
    figures = place_figures(wdict, total)
    captions, _cap_total = bcf.build_captions(narr)   # verbatim from clean narration
    bcf.write_srt(captions, SRT)                       # regenerate episode SRT identical/clean

    film = {
        "episode_id": EP,
        "fps": FPS,
        "narration": f"{SLUG}/narration.mp3",
        "narrationSeconds": round(total, 3),
        "hookSeconds": 8.0,
        "hookLine": "He set a gun on the dining table.",
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
        "distinct_stills_used": len({s for s in uses if "/img/" in s}),
        "captions": len(captions),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    problems = []
    if still_share > 0.43:
        problems.append(f"still_share {still_share:.3f} too close to 0.45")
    if motion_cov < 0.47:
        problems.append(f"motion_coverage {motion_cov:.3f} < 0.47")
    if fig_cov < 0.26:
        problems.append(f"figure_coverage {fig_cov:.3f} < 0.26 (motion_density floor 0.25)")
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
        man_assets.append({"asset_id": f"{'MO' if kind == 'factory' else 'ST'}-043-{i:03d}",
                           "kind": kind, "public_path": src, "uses": n})
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps({"episode_id": EP, "manifest_version": "v001",
                                    "producer": "scripts/build_caniglia_film_real.py",
                                    "is_stub": False, "counts": {"distinct": len(uses)},
                                    "assets": man_assets}, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
