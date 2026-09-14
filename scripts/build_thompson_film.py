#!/usr/bin/env python3
r"""Build remotion/src/data/thompson_film.json (EP41 PD-2026-041-thompson).

Adapted from build_lech_film.py / build_frazier_film.py. Key differences for thompson:

  * MIX (anti-紙芝居): EP40 lech shipped 100% stills and FAILED animation_mix. thompson
    interleaves REAL MOTION factory footage as the MAJORITY of screen time so
    check_animation_mix passes (still-share <= 0.45 of TIME, motion-coverage >= 0.45).
    Footage cuts (kind:"footage") route to <OffthreadVideo>; stills (kind:"img") Ken-Burns.
  * Stills come from 36 visually-QC'd SDXL scenes (see EP41_thompson_asset_map.v001.json);
    variants are rotated so no single PNG is used > 2x (asset_reuse cap) and first-use is high.
  * Factory clips come from runs/qc/thompson_factory_selected.v001.json (each visually QC'd
    on a contact sheet, EP39/EP40 clips excluded). Each factory clip used exactly once (cap 1).
  * figures[] are DESIGNED MG beats anchored to the MEASURED narration timing, ledger-only
    facts (Connick v. Thompson), only FigureBeats.tsx kinds, short emphasisWords (no 文字切れ).
  * captions[] are the measured narration chunks verbatim (real audio timing, real text).

No paid calls. Does NOT render. Copies selected stills + narration into remotion/public/thompson.
"""
from __future__ import annotations

import json
import shutil
import sys
from collections import Counter, deque
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-041-thompson"
SLUG = "thompson"
FPS = 30

ASSET_MAP = ROOT / "episodes" / "_planning" / "EP41_thompson_asset_map.v001.json"
NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
FACTORY_SEL = ROOT / "runs" / "qc" / "thompson_factory_selected.v001.json"
H_STILL = Path("E:/pd-media/assets/ai/thompson")
H_MASTER = Path("E:/pd-media/episodes/PD-2026-041-thompson/06_voice/master/vc_master_v001.mp3")

PUB_IMG = ROOT / "remotion" / "public" / "thompson" / "img"
PUB_FAC = ROOT / "remotion" / "public" / "thompson" / "factory"
PUB_NARR = ROOT / "remotion" / "public" / "thompson" / "narration.mp3"
OUT_FILM = ROOT / "remotion" / "src" / "data" / "thompson_film.json"
PUB_FILM = ROOT / "remotion" / "public" / "thompson" / "film_data.v001.json"
MANIFEST = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
SRT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"

# Valid FigureBeats.tsx kinds actually used here (all confirmed present in the component).
VALID_KINDS = {"numberticker", "stat", "kinetic", "timeline", "quote", "acttitle",
               "lowerthird", "mechanism", "dochighlight", "compbars", "bar", "highlightring", "spotlight"}
STILL_TREATS = ["duotone", "scan", "focus", "depth", "bleed"]

# Mix targets (TIME share). check_animation_mix caps still-share at 0.45; keep margin.
STILL_TIME_TARGET = 0.37     # aim ~37% of body is stills => footage ~63%
STILL_SHARE_HARD = 0.45
MIN_CUT = 2.2
MAX_CUT = 6.0


def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------- captions / windows
def _is_orphan(t: str) -> bool:
    """Mirror check_caption_breaks orphan rule: <3 word-tokens AND (no terminal punct OR
    does not start with an uppercase LETTER). e.g. '2003.' is an orphan (leading digit)."""
    import re as _re
    words = _re.findall(r"[A-Za-z0-9']+", t)
    return len(words) < 3 and (not t or t[-1] not in ".?!—-:;" or not t[0].isupper())


def build_captions(narr: dict):
    cues = []
    for c in narr["chunks"]:
        t = str(c.get("text", "")).strip()
        if not t:
            continue
        cues.append({"start": round(float(c["start"]), 3), "end": round(float(c["end"]), 3), "text": t})
    # Merge any orphan-ish short cue FORWARD into the next cue (keeps real audio timing,
    # avoids a standalone fragment like '2003.' that check_caption_breaks flags).
    merged = []
    i = 0
    while i < len(cues):
        c = cues[i]
        if _is_orphan(c["text"]) and i + 1 < len(cues):
            nxt = cues[i + 1]
            merged.append({"start": c["start"], "end": nxt["end"],
                           "text": (c["text"] + " " + nxt["text"]).strip()})
            i += 2
        else:
            merged.append(c)
            i += 1
    total = max(c["end"] for c in merged)
    return merged, float(total)


def section_windows(narr: dict, total: float):
    order = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ENDING"]
    starts = {}
    for c in narr["chunks"]:
        starts.setdefault(c["section"], float(c["start"]))
    wins = []
    for i, sec in enumerate(order):
        s = starts[sec]
        e = starts[order[i + 1]] if i + 1 < len(order) else total
        wins.append((sec, s, e))
    return wins


def srt_ts(t: float) -> str:
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(cues):
    lines = []
    for i, c in enumerate(cues, 1):
        lines += [str(i), f"{srt_ts(c['start'])} --> {srt_ts(c['end'])}", c["text"], ""]
    SRT.parent.mkdir(parents=True, exist_ok=True)
    SRT.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------- still variant picker
class StillPicker:
    """Copies stills on demand and rotates variants so no PNG file is used > 2x (cap)."""

    def __init__(self, scenes: dict):
        self.scenes = scenes
        self.file_uses: Counter = Counter()
        self.copied: set[str] = set()
        PUB_IMG.mkdir(parents=True, exist_ok=True)

    def variants(self, scene: str):
        # base then _02 then _03 that exist on H:
        out = []
        for suff in ["", "_02", "_03"]:
            f = f"{scene}{suff}.png"
            if (H_STILL / f).is_file():
                out.append(f)
        return out

    def pick(self, scene: str, treat_lock=None):
        """Return (public_path, treatment) picking the least-used unfilled variant (cap 2)."""
        cands = self.variants(scene)
        if not cands:
            raise SystemExit(f"no image files for scene {scene}")
        cands.sort(key=lambda f: self.file_uses[f])
        chosen = None
        for f in cands:
            if self.file_uses[f] < 2:
                chosen = f
                break
        if chosen is None:
            return None  # scene exhausted (all variants at cap)
        self.file_uses[chosen] += 1
        src = H_STILL / chosen
        dst = PUB_IMG / chosen
        if chosen not in self.copied:
            if (not dst.is_file()) or dst.stat().st_size != src.stat().st_size:
                shutil.copy2(src, dst)
            self.copied.add(chosen)
        treat = treat_lock or (self.scenes.get(scene, {}) or {}).get("treat_lock")
        return f"thompson/img/{chosen}", treat


# ---------------------------------------------------------------------------- factory pools
def load_factory():
    if not FACTORY_SEL.is_file():
        raise SystemExit(f"factory manifest missing: {FACTORY_SEL} (factory-selection agent not done)")
    data = load_json(FACTORY_SEL)
    clips = data if isinstance(data, list) else data.get("clips") or data.get("selected") or []
    by_act: dict[str, list] = {}
    seen = set()
    for c in clips:
        pub = c.get("public_path") or f"thompson/factory/{c['basename']}"
        if pub in seen:
            continue
        abs_p = ROOT / "remotion" / "public" / pub
        if not abs_p.is_file():
            continue  # skip clips that were not actually copied
        seen.add(pub)
        act = (c.get("act_suggestion") or c.get("act") or "GENERAL").upper()
        if act not in {"HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ENDING"}:
            act = "GENERAL"
        by_act.setdefault(act, []).append(pub)
    return by_act


# ---------------------------------------------------------------------------- cut builder
def tile(seq, s, e):
    """Equal-weight tiling of [s,e) so time-share == count-share (footage majority by count)."""
    n = len(seq)
    span = e - s
    base = span / n
    cuts = []
    t = s
    for i, item in enumerate(seq):
        dur = base if i < n - 1 else (e - t)
        dur = max(MIN_CUT, min(MAX_CUT, dur))
        cuts.append((round(t, 3), round(dur, 3), item))
        t += dur
    # fix drift so last cut ends exactly at e
    if cuts:
        st, _, it = cuts[-1]
        cuts[-1] = (st, round(e - st, 3), it)
    return cuts


FOOT_SHARE = 0.60          # footage gets ~60% of each section's TIME (=> still-share ~40%)
FOOT_MEAN = 3.9            # target footage cut length
STILL_MEAN = 3.3          # target still cut length


def build_cuts(windows, still_pools, hook_seq, picker: StillPicker, fac_by_act, total):
    fac_pool = {k: deque(v) for k, v in fac_by_act.items()}
    general = deque(fac_by_act.get("GENERAL", []))

    def take_footage(act, n):
        out = []
        dq = fac_pool.get(act)
        while len(out) < n and dq:
            out.append(dq.popleft())
        while len(out) < n and general:
            out.append(general.popleft())
        if len(out) < n:  # borrow from any other act pool as last resort
            for k, dd in fac_pool.items():
                while len(out) < n and dd:
                    out.append(dd.popleft())
        return out

    cuts = []
    treat_i = 0
    for sec, s, e in windows:
        D = e - s
        pool = still_pools.get(sec, [])
        foot_budget = FOOT_SHARE * D
        still_budget = D - foot_budget
        n_foot = max(1, round(foot_budget / FOOT_MEAN))
        foot = take_footage(sec, n_foot)
        n_foot = max(1, len(foot))
        foot_dur = max(2.5, min(6.0, foot_budget / n_foot))
        n_still = max(1, round(still_budget / STILL_MEAN))
        stills = []
        pi = guard = 0
        while len(stills) < n_still and pool and guard < n_still * 8 + 20:
            got = picker.pick(pool[pi % len(pool)]); pi += 1; guard += 1
            if got:
                stills.append(got)
        n_still = max(1, len(stills))
        still_dur = max(2.2, min(4.8, still_budget / n_still))
        # interleave footage-majority order
        seq = []
        fi = si = k = 0
        pat = ["F", "S", "F", "F", "S"]
        while fi < len(foot) or si < len(stills):
            slot = pat[k % len(pat)]; k += 1
            if slot == "F" and fi < len(foot):
                seq.append(("footage", foot[fi], None, foot_dur)); fi += 1
            elif slot == "S" and si < len(stills):
                seq.append(("still", stills[si][0], stills[si][1], still_dur)); si += 1
            elif fi < len(foot):
                seq.append(("footage", foot[fi], None, foot_dur)); fi += 1
            elif si < len(stills):
                seq.append(("still", stills[si][0], stills[si][1], still_dur)); si += 1
        if not seq:
            continue
        # lay sequentially from s; normalize durations to fill [s,e) exactly
        raw = sum(x[3] for x in seq)
        scale = D / raw
        t = s
        for j, (kind, src, treat, du) in enumerate(seq):
            dur = du * scale if j < len(seq) - 1 else (e - t)
            dur = round(max(1.8, dur), 3)
            idx = len(cuts)
            if kind == "footage":
                cuts.append({"id": f"cut-{idx:03d}", "start": round(t, 3), "dur": dur, "kind": "footage",
                             "src": src, "treatment": "footage", "seed": f"thompson-{idx:03d}", "act": sec})
            else:
                tr = treat or STILL_TREATS[treat_i % len(STILL_TREATS)]; treat_i += 1
                cuts.append({"id": f"cut-{idx:03d}", "start": round(t, 3), "dur": dur, "kind": "img",
                             "src": src, "treatment": tr, "seed": f"thompson-{idx:03d}", "act": sec})
            t += dur
    return cuts


# ---------------------------------------------------------------------------- figures (MG beats)
def K(lines, emph=None, style="maskslide"):
    d = {"kind": "kinetic", "lines": lines, "style": style}
    if emph:
        d["emphasisWords"] = emph
    return d


def NUM(value, label, suffix=None, prefix=None):
    d = {"kind": "numberticker", "value": value, "label": label}
    if suffix:
        d["suffix"] = suffix
    if prefix:
        d["prefix"] = prefix
    return d


def STAT(value, label, suffix=None, prefix=None):
    d = {"kind": "stat", "value": value, "label": label}
    if suffix:
        d["suffix"] = suffix
    if prefix:
        d["prefix"] = prefix
    return d


FIGURE_ANCHORS = [
    # HOOK / OP  (all ledger: Connick v. Thompson facts)
    (1.2, K(["ONE SHEET", "OF PAPER"], ["ONE"], "emphasis")),
    (6.4, NUM(14, "HIDDEN", suffix=" YEARS")),
    (11.2, K(["THE BLOOD", "WAS NOT HIS"], ["NOT"], "emphasis")),
    (16.2, K(["THE HIGHEST COURT", "SAID: NO"], ["NO"], "wordpop")),
    (24.0, K(["CAN YOU MAKE", "THEM ANSWER?"], ["ANSWER"], "emphasis")),
    (34.5, STAT(18, "ERASED", suffix=" YEARS")),
    (41.5, NUM(14, "SPENT WAITING TO DIE", suffix=" YEARS")),
    # ACT 1 — The Choice
    (48.4, {"kind": "acttitle", "title": "THE CHOICE", "kicker": "ACT ONE", "index": 1}),
    (60.5, {"kind": "lowerthird", "primary": "ILLUSTRATIVE RECONSTRUCTION",
            "secondary": "AI-assisted visualization — not actual footage"}),
    (77.0, K(["NEW ORLEANS", "1984"], ["1984"], "emphasis")),
    (106.7, K(["THEY TRY THE", "ROBBERY FIRST"], ["FIRST"], "emphasis")),
    (134.1, K(["HE STAYS", "SILENT"], ["SILENT"], "wordpop")),
    (144.4, K(["THE BLOOD: TYPE B", "THOMPSON: TYPE O"], ["B", "O"], "maskslide")),
    (151.0, {"kind": "mechanism", "mechanism": "closingdoor"}),
    (157.5, NUM(14, "BURIED", suffix=" YEARS")),
    # ACT 2 — The Wait
    (170.4, {"kind": "acttitle", "title": "THE WAIT", "kicker": "ACT TWO", "index": 2}),
    (177.0, STAT(14, "ON DEATH ROW", suffix=" YEARS")),
    (185.0, NUM(18, "BEHIND BARS", suffix=" YEARS")),
    (200.0, {"kind": "mechanism", "mechanism": "gears"}),
    (213.6, K(["1994", "A MAN BEGINS TO DIE"], ["1994"], "emphasis")),
    (225.0, NUM(9, "A SECRET CARRIED", suffix=" YEARS")),
    (245.0, {"kind": "dochighlight", "rects": [{"x": 0.18, "y": 0.38, "w": 0.64, "h": 0.10}], "mode": "redact"}),
    (265.6, K(["EXECUTION SET", "MAY 20, 1999"], ["MAY 20"], "maskslide")),
    (284.0, K(["FOUND", "WITH WEEKS LEFT"], ["FOUND"], "wordpop")),
    # ACT 3 — The Verdict
    (303.4, {"kind": "acttitle", "title": "THE VERDICT", "kicker": "ACT THREE", "index": 3}),
    (315.7, K(["NOT", "GUILTY"], ["GUILTY"], "wordpop")),
    (340.0, K(["EIGHTEEN YEARS", "GONE"], ["GONE"], "emphasis")),
    (352.7, NUM(14, "THE JURY AWARDED", prefix="$", suffix=" MILLION")),
    (362.5, {"kind": "timeline", "events": [
        {"year": "2003", "text": "ACQUITTED"}, {"year": "2010", "text": "ARGUED"},
        {"year": "2011", "text": "DECIDED"}]}),
    (380.2, K(["FIVE TO FOUR", "THE COURT REVERSED"], ["FIVE", "FOUR"], "emphasis")),
    (390.5, NUM(0, "EVERY DOLLAR GONE", prefix="$")),
    (404.0, K(["ONE BURIED REPORT", "IS NOT A PATTERN"], ["PATTERN"], "emphasis")),
    (430.0, NUM(4, "PRIOR REVERSALS IN 10 YEARS")),
    (451.0, {"kind": "mechanism", "mechanism": "faultsplit"}),
    (471.8, NUM(4, "PROSECUTORS KNEW")),
    (482.0, K(["PERVASIVE", "STANDARD OPERATING PROCEDURE"], ["PERVASIVE"], "emphasis")),
    # ACT 4 — The Reach
    (495.9, {"kind": "acttitle", "title": "THE REACH", "kicker": "ACT FOUR", "index": 4}),
    (502.0, K(["THE RULE HAS A NAME", "BRADY"], ["BRADY"], "wordpop")),
    (521.0, K(["TYPE B", "BESIDE A MAN TYPE O"], ["B", "O"], "maskslide")),
    (541.0, {"kind": "dochighlight", "rects": [{"x": 0.30, "y": 0.34, "w": 0.40, "h": 0.30}], "mode": "box"}),
    (556.0, K(["A JURY SAID", "$14 MILLION"], ["MILLION"], "emphasis")),
    (570.0, K(["THE COURT SAID", "NOT ONE DOLLAR"], ["DOLLAR"], "wordpop")),
    # ENDING
    (607.4, K(["A FREE MAN", "EIGHTEEN YEARS GONE"], ["FREE"], "emphasis")),
    (626.0, {"kind": "lowerthird", "primary": "RESURRECTION AFTER EXONERATION",
             "secondary": "The place John Thompson built for other exonerated men"}),
    (636.8, K(["HE DIED", "IN 2017"], ["2017"], "emphasis")),
    (662.0, K(["THE HONEST ANSWER", "ALMOST NEVER"], ["NEVER"], "wordpop")),
    (694.0, K(["IF THIS STAYED", "WITH YOU"], ["YOU"], "emphasis")),
    (709.0, NUM(4, "JUSTICES REFUSED TO SIGN")),
]

FIG_DUR = 4.6
FIG_GAP = 0.4
FIG_MIN = 2.8


def build_figures(total):
    anchors = sorted(FIGURE_ANCHORS, key=lambda x: x[0])
    figs = []
    for i, (start, payload) in enumerate(anchors):
        end = start + FIG_DUR
        if i + 1 < len(anchors):
            end = min(end, anchors[i + 1][0] - FIG_GAP)
        end = min(end, total - 0.4)
        if end - start < FIG_MIN:
            raise SystemExit(f"figure at {start} clamped below min ({end-start:.2f}s) — respace")
        if payload["kind"] not in VALID_KINDS:
            raise SystemExit(f"invalid figure kind {payload['kind']}")
        figs.append({"start": round(start, 3), "end": round(end, 3), **payload})
    for a, b in zip(figs, figs[1:]):
        if b["start"] < a["end"] - 1e-6:
            raise SystemExit(f"figure overlap {a['end']} > {b['start']}")
    return figs


def build_hook(hook_seq, picker):
    hook = []
    t = 0.0
    d = 2.0
    for i, scene in enumerate(hook_seq):
        got = picker.pick(scene)
        if not got:
            continue
        hook.append({"start": round(t, 3), "dur": d, "kind": "img", "src": got[0], "seed": f"hook-{i}"})
        t += d
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
    amap = load_json(ASSET_MAP)
    narr = load_json(NARR)
    scenes = amap["scenes"]
    still_pools = dict(amap["act_still_pools"])
    # give HOOK/OP their own still pools (hook teaser + thesis imagery)
    still_pools.setdefault("HOOK", ["S01", "S24", "S02", "S30"])
    still_pools.setdefault("OP", ["S13", "S05", "S31", "S45", "S06"])

    captions, total = build_captions(narr)
    windows = section_windows(narr, total)
    write_srt(captions)

    picker = StillPicker(scenes)
    fac_by_act = load_factory()

    hook = build_hook(amap["hook_sequence"], picker)
    cuts = build_cuts(windows, still_pools, amap["hook_sequence"], picker, fac_by_act, total)
    figures = build_figures(total)

    # copy narration master
    PUB_NARR.parent.mkdir(parents=True, exist_ok=True)
    if H_MASTER.is_file():
        if (not PUB_NARR.is_file()) or PUB_NARR.stat().st_size != H_MASTER.stat().st_size:
            shutil.copy2(H_MASTER, PUB_NARR)

    film = {
        "episode_id": EP,
        "fps": FPS,
        "narration": f"{SLUG}/narration.mp3",
        "narrationSeconds": round(total, 3),
        "hookSeconds": round(sum(h["dur"] for h in hook), 3),
        "hookLine": "They hid the proof for fourteen years.",
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

    # -------- report + self-verify against gate formulas --------
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
        "cuts": len(cuts), "footage_cuts": sum(1 for c in cuts if c["kind"] == "footage"),
        "still_cuts": sum(1 for c in cuts if c["kind"] == "img"),
        "still_time_share": round(still_share, 3), "motion_coverage": round(motion_cov, 3),
        "figure_coverage": round(fig_cov, 3), "figure_density_per_min": round(density, 2),
        "figures": len(figures), "figure_variety": variety,
        "first_use_share": round(first_share, 3), "over_cap": over, "long_still_holds": long_holds,
        "distinct_assets": len(uses),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    problems = []
    if still_share > STILL_SHARE_HARD - 0.02:
        problems.append(f"still_share {still_share:.3f} too close to {STILL_SHARE_HARD}")
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
    if long_holds > 8:
        problems.append(f"long_still_holds {long_holds} > 8")
    if variety < 3:
        problems.append("variety < 3")
    if problems:
        print("SELF-CHECK PROBLEMS:\n  " + "\n  ".join(problems))
        return 2
    print("SELF-CHECK OK")

    # manifest for provenance
    man_assets = []
    for i, (src, n) in enumerate(uses.items(), 1):
        kind = "factory" if "/factory" in src else "still"
        man_assets.append({"asset_id": f"{'MO' if kind=='factory' else 'ST'}-041-{i:03d}",
                           "kind": kind, "public_path": src, "uses": n})
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps({"episode_id": EP, "manifest_version": "v001",
                                    "producer": "scripts/build_thompson_film.py",
                                    "counts": {"distinct": len(uses)}, "assets": man_assets},
                                   ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
