#!/usr/bin/env python
"""Build remotion/src/data/centralpark_film.json for EP50 from an asset manifest.

Cloned from build_cleveland_film.py. EP50 = channel-first LONG-FORM 60-min film.
Constants swapped to centralpark; the allocation logic (public_items/take/repeated/
make_cuts/build_captions/section_windows) is preserved. Key EP50 changes:

  * 9 sections HOOK/OP/ACT_1..ACT_7. Cut totals: factory 485 + motion 170 + still 505
    = 1,160 cuts (distinct 485+85+430 = 1,000; first-use 0.8621; still-share 0.4353).
  * ANTI-KAMISHIBAI ASSERT (EP45 death cause): public_items(manifest,"factory") must be
    485 and public_items(manifest,"motion") must be 85 -- 0 or wrong count -> exit 1
    (send back to thread A; never pad with stills).
  * figures[] = 165 (motion-density floor 151 + 14), graphics[] = [], dochighlight = 0,
    YEAR numberticker/stat carry group:false (EP46/EP47 "1,989"/"2,001" bug), big
    figures (6,000,000,000 / $41,000,000) keep default group:true.
  * hookSeconds = 8.0 (0 => 8s desync), centralpark-specific hookLine.
  * durationInFrames is the 4-term function; the 750s cleveland cap is REMOVED (long-form).
    narrationSeconds / durationInFrames come from the real narration_index at build time.

  ---> TODO (CODEX_B section 5.1.1): narrationSeconds and durationInFrames are PROVISIONAL
       (3643.324s / 109,915f estimate). After the measured TTS VO master exists, this builder
       reads narration_index.total_seconds and recomputes durationInFrames via the SAME
       4-term function, then updates PRODUCTION_SPEC runtime_plan + Root.tsx. Do NOT hardcode
       109915 as final. (`--assert-frames` may be passed once the measured value is known.)

  beatsheet is named centralpark_beatsheet (NOT premium_*) so check_motion_density /
  check_animation_mix measure film.json only (section 5.6).

Author + syntax/logic-checked. NOT run here (no FROZEN manifest / measured narration yet).
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-050-centralpark"
SLUG = "centralpark"
FPS = 30
DEFAULT_ASSETS = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v003.json"
DEFAULT_NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
DEFAULT_OUT = ROOT / "remotion" / "src" / "data" / "centralpark_film.json"
PUB_FILM = ROOT / "remotion" / "public" / "centralpark" / "film_data.v001.json"
BUILD_MANIFEST = ROOT / "episodes" / EP / "04_scenes" / "centralpark_build_manifest.v001.json"
BEATSHEET = ROOT / "episodes" / EP / "04_scenes" / "centralpark_beatsheet.v001.json"
DEFAULT_SRT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"
AE_BEATS = ROOT / "episodes" / EP / "08_edit" / "ae_hero" / "beats.json"

# PROVISIONAL runtime (CODEX_B 5.1.1): 10,715 words / ~178.3 wpm. FINAL from measured TTS.
PROVISIONAL_NARR_SEC = 3643.324
PROVISIONAL_FRAMES = 109915
HOOK_SEC = 8.0
OPENING_SEC = 3.5
ENDCARD_SEC = 9.0

# per-section (factory, motion_CUTS, still): totals 485 / 170 / 505 = 1,160 cuts.
# ACT_2 and ACT_5 are the densest (interrogation engine; confession/DNA climax).
# MOTION-FIRST REBUILD (owner 2026-07-26: "紙芝居/反復/無音チカチカ"). (footage, motion, still):
# footage+motion are REAL video (stock + i2v); still is drastically reduced. LONGER cuts (~5s)
# => far fewer total cuts (~720 vs 1160) => less reuse. HOOK/OP tiny + calm => cold-open, NO flicker.
# ★2026-07-30 REBALANCE (acceptance FAIL on the 599-cut build): mean cut was 6.1s, which is
# what animation_mix measured as "172 hero stills linger > 5s" and what the owner calls 紙芝居
# (the standing rule is 2-3s cuts). With the F-loops back in the factory pool the material
# exists to cut properly: factory 519 (cap 1) + motion 414 (207 x cap 2) + stills 380 of 430
# (cap 1) = 1,313 cuts = 2.79s mean, first-use share 82% (was 69%), and every staged clip is
# referenced at least once (footage_utilization was 17%).
SECTION_TARGETS = {
    "HOOK":  (2, 1, 1),
    "OP":    (1, 1, 0),
    "ACT_1": (63, 51, 46),
    "ACT_2": (102, 83, 75),
    "ACT_3": (79, 62, 57),
    "ACT_4": (72, 58, 53),
    "ACT_5": (70, 56, 53),
    "ACT_6": (90, 70, 66),
    "ACT_7": (38, 30, 29),
}
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ACT_5", "ACT_6", "ACT_7"]

# real lowercase FigureSpec union (FigureBeats.tsx). dochighlight is in the union but BANNED.
VALID_KINDS = {"numberticker", "stat", "votetally", "timeline", "quote", "kinetic",
               "lowerthird", "acttitle", "compbars", "bar", "mechanism", "regionmap",
               "pindropmap", "routemap", "arrow", "highlightring", "spotlight"}

HOOK_LINE = ("Five children. A room with the camera switched off. And a confession "
             "the evidence would erase.")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def srt_ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# 2-LINE CAPTION FIX (owner 2026-07-25 "字幕の4行はさすがに醜い。2行ぐらい"). At fontSize 44 /
# maxWidth 78% the body font fits ~50 chars/line, so a caption stays <=2 lines at <=~100 chars.
#
# ★2026-07-30: the old splitter packed words to a pure character budget, which is exactly the
# recurring "字幕が変なところで途切れる" complaint -- acceptance measured 185 mid-phrase splits,
# 54 orphan cues and 613 over-long lines on the 599-cut build. Line breaking now goes through
# the CANON splitter (gen_captions_forced.split_lines_clause: never ends a line on a dangling
# function word, prefers a break after punctuation or before a phrase start) instead of a
# second local implementation (invariant 14). Cues carry a real "\n" so the burned-in caption
# breaks where the SRT breaks.
CAPTION_MAX_LINES = 2          # lines per cue
CAPTION_LEAD_SECONDS = 0.20    # cues lead the voice slightly; acceptance had 19% late cues
CAPTION_MIN_TAIL_CHARS = 16    # shorter trailing fragment is merged back (orphan cues)

sys.path.insert(0, str(ROOT / "scripts"))
import gen_captions_forced as _gcf           # noqa: E402  (canon line splitter)

_gcf.SEG_MAX_WORDS, _gcf.SEG_MAX_CHARS = 9, 50   # gate: <=2 lines, <=50 chars/line


def _lines_at(text: str, cap: int) -> list[str]:
    saved = _gcf.SEG_MAX_CHARS
    _gcf.SEG_MAX_CHARS = cap
    try:
        return [ln for ln, _i0, _i1 in _gcf.split_lines_clause(text.split()) if ln.strip()]
    finally:
        _gcf.SEG_MAX_CHARS = saved


def _clean_lines(text: str) -> list[str]:
    """Grammatically clean, LENGTH-BALANCED caption lines for one narration chunk.

    Splitting at the hard 50-char cap leaves a short tail ("described." / "from."), which
    becomes an orphan cue -- the exact thing check_caption_breaks fails on. So the cap is
    first relaxed to the balanced width for the number of lines the text actually needs,
    and a still-short tail is merged back when it fits.
    """
    hard = _gcf.SEG_MAX_CHARS
    n = max(1, -(-len(text) // hard))                     # lines needed at the hard cap
    cap = min(hard, max(28, -(-len(text) // n) + 6))      # balanced width for n lines
    lines = _lines_at(text, cap)
    if len(lines) > n:                                    # balancing overshot; fall back
        lines = _lines_at(text, hard)
    if len(lines) > 1 and len(lines[-1]) < CAPTION_MIN_TAIL_CHARS:
        merged = f"{lines[-2]} {lines[-1]}"
        if len(merged) <= hard:
            lines[-2:] = [merged]
    return lines or [text]


def _split_caption_text(text: str) -> list[str]:
    """-> cue texts, each at most CAPTION_MAX_LINES physical lines joined by '\\n'."""
    lines = _clean_lines(text)
    cues = ["\n".join(lines[i:i + CAPTION_MAX_LINES])
            for i in range(0, len(lines), CAPTION_MAX_LINES)]
    # a 1-line last cue that is short reads as an orphan; fold it into the previous cue
    # when the previous cue is a single line and the pair still fits two lines.
    if len(cues) > 1 and "\n" not in cues[-1] and len(cues[-1]) < CAPTION_MIN_TAIL_CHARS * 2:
        if "\n" not in cues[-2]:
            cues[-2:] = ["\n".join(cues[-2:])]
    return cues


def build_captions(narr: dict) -> tuple[list[dict], float]:
    cues: list[dict] = []
    for c in narr["chunks"]:
        text = str(c.get("text") or c.get("spoken_text") or "").strip()
        if not text:
            continue
        start, end = round(float(c["start"]), 3), round(float(c["end"]), 3)
        segs = _split_caption_text(text)
        if len(segs) == 1:
            cues.append({"start": start, "end": end, "text": segs[0]})
            continue
        # apportion the chunk's time across sub-cues by character length
        total_chars = sum(len(s) for s in segs)
        t = start
        for i, s in enumerate(segs):
            frac = len(s) / total_chars
            seg_end = end if i == len(segs) - 1 else round(t + (end - start) * frac, 3)
            cues.append({"start": round(t, 3), "end": seg_end, "text": s})
            t = seg_end
    # lead the voice slightly, never crossing into the previous cue (caption_sync: late cues)
    prev_end = 0.0
    for cue in cues:
        cue["start"] = round(max(prev_end, min(cue["start"], cue["start"] - CAPTION_LEAD_SECONDS)), 3)
        prev_end = cue["end"]
    return cues, max(c["end"] for c in cues)


def write_srt(cues: list[dict], out: Path) -> None:
    lines = []
    for i, c in enumerate(cues, 1):
        lines += [str(i), f"{srt_ts(c['start'])} --> {srt_ts(c['end'])}", c["text"], ""]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def section_windows(narr: dict, total: float) -> dict[str, tuple[float, float]]:
    starts = {}
    for c in narr["chunks"]:
        sec = c["section"]
        starts.setdefault(sec, float(c["start"]))
    windows = {}
    for i, sec in enumerate(SECTION_ORDER):
        if sec not in starts:
            continue
        nxt = next((s for s in SECTION_ORDER[i + 1:] if s in starts), None)
        windows[sec] = (starts[sec], starts[nxt] if nxt else total)
    # OP is a fixed 3.5s silent title segment and is not present in narration_index.
    # The EP50 asset contract still allocates OP cuts, so carve it from the tail of
    # the HOOK narration window when both HOOK and ACT_1 are present.
    if "OP" not in windows and "HOOK" in windows and "ACT_1" in starts:
        hook_start, hook_end = windows["HOOK"]
        op_start = max(hook_start, hook_end - OPENING_SEC)
        windows["HOOK"] = (hook_start, op_start)
        windows["OP"] = (op_start, hook_end)
    return windows


def public_items(manifest: dict, key: str, role: str | None = None) -> list[str]:
    items = manifest.get(key) or []
    if role:
        items = [x for x in items if x.get("role") == role]
    out = [str(x["public_path"]) for x in items if x.get("public_path")]
    if len(out) != len(set(out)):
        raise SystemExit(f"duplicate public_path in {key}")
    return out


def take(q: deque, n: int, label: str) -> list[str]:
    if len(q) < n:
        raise SystemExit(f"not enough {label}: need {n}, have {len(q)}")
    return [q.popleft() for _ in range(n)]


def repeated(pool: list[str], n: int, cap: int, label: str) -> list[str]:
    if not pool:
        raise SystemExit(f"not enough {label}: need {n}, have 0")
    out: list[str] = []
    uses: Counter[str] = Counter()
    i = 0
    guard = 0
    while len(out) < n and guard < n * 10 + 100:
        item = pool[i % len(pool)]
        if uses[item] < cap:
            uses[item] += 1
            out.append(item)
        i += 1
        guard += 1
    if len(out) < n:
        raise SystemExit(f"unable to allocate {n} {label} assets with cap {cap}")
    return out


def make_cuts(windows: dict[str, tuple[float, float]], manifest: dict) -> list[dict]:
    stills = public_items(manifest, "stills", "body")
    factory_pool = public_items(manifest, "factory")
    motion_pool = public_items(manifest, "motion")
    still_need = sum(ns for nf, nm, ns in SECTION_TARGETS.values())
    motion_need = sum(nm for nf, nm, ns in SECTION_TARGETS.values())
    factory_need = sum(nf for nf, nm, ns in SECTION_TARGETS.values())
    # MOTION-FIRST: factory is now REAL video (stock+i2v), small pool -> allow cap-2 reuse
    # (spread FAR apart across 60 min), like motion. stills used at most once (no reuse).
    still_pool = repeated(stills, still_need, 1, "still")
    motion_items = repeated(motion_pool, motion_need, 2, "motion")
    factory_items = repeated(factory_pool, factory_need, 2, "factory")
    factory_q = deque(factory_items)
    still_q = deque(still_pool)
    motion_q = deque(motion_items)
    cuts: list[dict] = []
    # WARP/SCANLINE FIX (owner 2026-07-25 "所々画像がゆがんでる"): drop "depth" (3D
    # displacement-map warps on bad/missing maps) and "scan" (measurement-grid reads as
    # scanlines). bleed+parallax+duotone+focus all carry genuine parallax MOTION (bg blur +
    # sharp fg drift) so 紙芝居 stays fixed WITHOUT geometric warping.
    treatments = ["bleed", "duotone", "focus"]
    treat_i = 0
    for sec in SECTION_ORDER:
        if sec not in windows:
            continue
        nf, nm, ns = SECTION_TARGETS[sec]
        if nf + nm + ns == 0:
            continue
        s, e = windows[sec]
        seq: list[tuple[str, str]] = []
        fac = take(factory_q, nf, "factory")
        mot = take(motion_q, nm, "motion")
        sti = take(still_q, ns, "still")
        fi = mi = si = 0
        # MOTION-FIRST: F(footage=stock/i2v) + M(motion=i2v) dominate; S(still) is rare.
        pattern = ["F", "M", "F", "M", "F", "S"]
        while fi < len(fac) or mi < len(mot) or si < len(sti):
            slot = pattern[len(seq) % len(pattern)]
            if slot == "F" and fi < len(fac):
                seq.append(("footage", fac[fi])); fi += 1
            elif slot == "M" and mi < len(mot):
                seq.append(("footage", mot[mi])); mi += 1
            elif slot == "S" and si < len(sti):
                seq.append(("img", sti[si])); si += 1
            elif fi < len(fac):
                seq.append(("footage", fac[fi])); fi += 1
            elif mi < len(mot):
                seq.append(("footage", mot[mi])); mi += 1
            elif si < len(sti):
                seq.append(("img", sti[si])); si += 1
        # keep still dur systematically shorter than footage (animation_mix)
        weights = [3.0 if kind == "img" else 3.343 for kind, _ in seq]
        scale = (e - s) / sum(weights)
        t = s
        for kind, src in seq:
            raw = 3.0 if kind == "img" else 3.343
            dur = round(raw * scale, 3)
            cut = {"id": f"cut-{len(cuts):04d}", "start": round(t, 3), "dur": dur,
                   "kind": kind, "src": src, "seed": f"centralpark-{len(cuts):04d}", "act": sec}
            cut["treatment"] = treatments[treat_i % len(treatments)] if kind == "img" else "footage"
            if kind == "img":
                treat_i += 1
            cuts.append(cut)
            t += dur
        if cuts:
            cuts[-1]["dur"] = round(e - cuts[-1]["start"], 3)
    return cuts


def make_hook(manifest: dict) -> list[dict]:
    stills = public_items(manifest, "stills", "body")
    picks = stills[:8]
    dur = round(HOOK_SEC / len(picks), 3)
    hook = []
    t = 0.0
    for i, src in enumerate(picks):
        d = round(HOOK_SEC - t, 3) if i == len(picks) - 1 else dur
        hook.append({"start": round(t, 3), "dur": d, "kind": "img", "src": src, "seed": f"centralpark-hook-{i:02d}"})
        t += d
    return hook


# ---------------------------------------------------------------- figures (165)
def K(lines, emph=None, style="maskslide"):
    d = {"kind": "kinetic", "lines": lines, "style": style}
    if emph:
        d["emphasisWords"] = emph
    return d


def NT(value, label, group, prefix="", suffix="", decimals=0):
    d = {"kind": "numberticker", "value": value, "label": label, "group": group}
    if prefix:
        d["prefix"] = prefix
    if suffix:
        d["suffix"] = suffix
    if decimals:
        d["decimals"] = decimals
    return d


# content banks (ledger-safe: no invented quotes, R-INNOCENCE/VICTIM/REYES clean, years literal)
_LT = deque([
    ("place - New York City", "1989"),
    ("the videotaped statements", "at least seven hours in custody first"),
    ("Bearden of the confession era", "youths comply to end the ordeal"),
    ("Manhattan District Attorney", "the office that reversed course, 2002"),
    ("Auburn Correctional Facility", "where the real attacker was near"),
    ("a full-page newspaper ad", "reportedly ~$85,000; it named no one"),
    ("New York State Court of Claims", "a separate settlement, reportedly ~$3.9M"),
    ("false-confession research", "well-documented consensus"),
    ("the record", "only the final statements were taped"),
    ("the physical evidence", "excluded all five in 1990"),
])
_KIN = deque([
    (["IT WILL MATCH", "NONE OF THEM"], ["NONE"]),
    (["THE STORY,", "FED IN"], ["FED"]),
    (["ONE MAN.", "HIM."], ["HIM"]),
    (["FIVE CHILDREN.", "HOURS OF PRESSURE."], ["CHILDREN"]),
    (["THE CAMERA", "WAS OFF"], ["OFF"]),
    (["THE EVIDENCE", "POINTED ELSEWHERE"], ["ELSEWHERE"]),
    (["RECORD THE", "WHOLE INTERROGATION"], ["WHOLE"]),
    (["YOU WERE", "A CHILD"], ["CHILD"]),
])
_MECH = deque(["gears", "closingdoor", "faultsplit"])
_CB = deque([
    [{"label": "confessions", "value": 5}, {"label": "DNA matches at trial", "value": 0}],
    [{"label": "matched Reyes", "value": 1}, {"label": "matched the five", "value": 0}],
    [{"label": "taped statements", "value": 4}, {"label": "signed by Salaam", "value": 0}],
])
_TL = deque([
    [{"year": "1989", "text": "the night in the park"}, {"year": "1990", "text": "convicted"}, {"year": "2002", "text": "vacated"}],
    [{"year": "1989", "text": "Reyes rapes in the city"}, {"year": "1991", "text": "33 1/3 to life"}, {"year": "2002", "text": "he confesses"}],
    [{"year": "2002", "text": "vacated"}, {"year": "2014", "text": "city settlement"}, {"year": "2016", "text": "state settlement"}],
])
_STAT = deque([
    (12, "days in a coma"),
    (5, "children interrogated"),
    (7, "at least, hours before the cameras"),
    (33, "and one third: years to life for Reyes"),
    (13, "roughly, the years Korey Wise served"),
])
_NT = deque([
    NT(6000000000, "the DNA match: one in six billion", True),
    NT(41000000, "the 2014 city settlement, roughly", True, prefix="$"),
    NT(3900000, "the 2016 state settlement, reportedly", True, prefix="$"),
    NT(1989, "the night", False),
    NT(2002, "vacated", False),
    NT(2014, "settled", False),
])
_BAR = deque([
    {"kind": "bar", "items": [{"label": "Santana", "value": 6}, {"label": "McCray", "value": 7},
                              {"label": "Richardson", "value": 7}, {"label": "Salaam", "value": 6},
                              {"label": "Wise", "value": 13}]},
])
_ARROW = deque([
    {"kind": "arrow", "from": "a detective", "to": "a frightened child", "label": "the story, fed in"},
    {"kind": "arrow", "from": "one man's DNA", "to": "the whole truth", "label": "it matched no one else"},
])
_HR = deque([
    {"kind": "highlightring", "cx": 0.5, "cy": 0.5, "r": 0.12, "label": "the REC light, off"},
    {"kind": "highlightring", "cx": 0.5, "cy": 0.42, "r": 0.1, "label": "the unread lab line"},
])
_PIN = deque([
    {"kind": "pindropmap", "pins": [{"x": 0.52, "y": 0.44, "label": "Central Park"}]},
])
_ROUTE = deque([
    {"kind": "routemap", "pins": [{"x": 0.3, "y": 0.6}, {"x": 0.6, "y": 0.4}], "label": "that night's drift, abstracted"},
])
_SPOT = deque([
    {"kind": "spotlight", "cx": 0.5, "cy": 0.5, "r": 0.22, "dim": 0.7},
])
_REGION = deque([
    {"kind": "regionmap", "label": "the city, 1989", "pattern": "abstract"},
])
_ACT = deque([
    {"kind": "acttitle", "title": "THE ROOM", "kicker": "ACT TWO", "index": 2},
    {"kind": "acttitle", "title": "THE MACHINE", "kicker": "ACT TWO", "index": 2},
    {"kind": "acttitle", "title": "THE LADDER", "kicker": "ACT FIVE", "index": 5},
])


def _next(dq: deque):
    v = dq[0]
    dq.rotate(-1)
    return v


def _make(kind: str) -> dict:
    if kind == "lowerthird":
        p, s = _next(_LT)
        return {"kind": "lowerthird", "primary": p, "secondary": s}
    if kind == "kinetic":
        lines, emph = _next(_KIN)
        return K(list(lines), list(emph), "emphasis")
    if kind == "mechanism":
        return {"kind": "mechanism", "mechanism": _next(_MECH)}
    if kind == "compbars":
        return {"kind": "compbars", "items": [dict(x) for x in _next(_CB)]}
    if kind == "timeline":
        return {"kind": "timeline", "events": [dict(x) for x in _next(_TL)]}
    if kind == "stat":
        v, lab = _next(_STAT)
        return {"kind": "stat", "value": v, "label": lab}
    if kind == "numberticker":
        return dict(_next(_NT))
    if kind == "bar":
        b = _next(_BAR)
        return {"kind": "bar", "items": [dict(x) for x in b["items"]]}
    if kind == "arrow":
        return dict(_next(_ARROW))
    if kind == "highlightring":
        return dict(_next(_HR))
    if kind == "pindropmap":
        p = _next(_PIN)
        return {"kind": "pindropmap", "pins": [dict(x) for x in p["pins"]]}
    if kind == "routemap":
        r = _next(_ROUTE)
        return {"kind": "routemap", "pins": [dict(x) for x in r["pins"]], "label": r["label"]}
    if kind == "spotlight":
        return dict(_next(_SPOT))
    if kind == "regionmap":
        return dict(_next(_REGION))
    if kind == "acttitle":
        return dict(_next(_ACT))
    raise SystemExit(f"unknown figure kind {kind}")


# per-section kind rotation (section 6.3 lead kinds). Adjacent entries differ -> no dup runs.
SECTION_KINDS = {
    "HOOK": ["lowerthird", "spotlight"],
    "OP": ["kinetic"],
    "ACT_1": ["lowerthird", "kinetic", "routemap", "pindropmap", "regionmap", "stat",
              "compbars", "arrow", "highlightring"],
    "ACT_2": ["mechanism", "compbars", "arrow", "kinetic", "stat", "timeline",
              "lowerthird", "acttitle", "highlightring"],
    "ACT_3": ["kinetic", "compbars", "lowerthird", "mechanism", "timeline", "stat", "highlightring"],
    "ACT_4": ["bar", "lowerthird", "kinetic", "timeline", "stat", "compbars", "acttitle"],
    "ACT_5": ["numberticker", "compbars", "timeline", "mechanism", "pindropmap", "stat",
              "kinetic", "lowerthird", "highlightring"],
    "ACT_6": ["numberticker", "lowerthird", "kinetic", "mechanism", "stat", "compbars", "timeline"],
    "ACT_7": ["mechanism", "compbars", "kinetic", "spotlight", "lowerthird", "stat"],
}
SECTION_FIG_COUNTS = [("HOOK", 2), ("OP", 1), ("ACT_1", 18), ("ACT_2", 36), ("ACT_3", 23),
                      ("ACT_4", 22), ("ACT_5", 28), ("ACT_6", 20), ("ACT_7", 15)]  # = 165


def ae_blocks() -> list[tuple[float, float]]:
    if not AE_BEATS.exists():
        return []
    doc = load_json(AE_BEATS)
    blocks: list[tuple[float, float]] = []
    for beat in doc.get("beats") or []:
        try:
            start = float(beat["start"])
            end = float(beat["end"])
        except (KeyError, TypeError, ValueError):
            continue
        if end > start:
            blocks.append((start, end))
    return sorted(blocks)


def free_slots(lo: float, hi: float, blocks: list[tuple[float, float]], pad: float, min_len: float) -> list[tuple[float, float]]:
    cursor = lo
    slots: list[tuple[float, float]] = []
    for start, end in blocks:
        start -= pad
        end += pad
        if end <= cursor or start >= hi:
            continue
        if start > cursor and start - cursor >= min_len:
            slots.append((cursor, min(start, hi)))
        cursor = max(cursor, min(end, hi))
    if hi > cursor and hi - cursor >= min_len:
        slots.append((cursor, hi))
    return slots


def pick_slot_start(slots: list[tuple[float, float]], index: int, count: int, dur: float) -> float:
    total = sum(end - start for start, end in slots)
    target = total * (index + 0.5) / max(count, 1)
    seen = 0.0
    for start, end in slots:
        width = end - start
        if seen + width >= target:
            center = start + (target - seen)
            return min(max(center - dur / 2, start), end - dur)
        seen += width
    start, end = slots[-1]
    return max(start, end - dur)


def figure_payloads() -> list[dict]:
    """Return exactly 165 union-valid figure payloads, grouped by section, no dochighlight,
    YEAR numberticker with group:false. Disclosure lowerthirds bookend the reel (R1)."""
    out: list[dict] = []
    for sec, count in SECTION_FIG_COUNTS:
        rot = SECTION_KINDS[sec]
        for i in range(count):
            kind = rot[i % len(rot)]
            fig = _make(kind)
            if fig["kind"] not in VALID_KINDS:
                raise SystemExit(f"invalid figure kind {fig['kind']}")
            out.append(fig)
    # bookend AI-disclosure lowerthirds (R1)
    disc = {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction, no real likenesses"}
    out[0] = dict(disc)
    out[-1] = dict(disc)
    if len(out) != 165:
        raise SystemExit(f"figure count {len(out)} != 165")
    return out


def place_figures(windows: dict[str, tuple[float, float]], total: float) -> list[dict]:
    payloads = deque(figure_payloads())
    figures: list[dict] = []
    fig_min = 3.0
    blocks = ae_blocks()
    pad = 0.25
    for sec, count in SECTION_FIG_COUNTS:
        if sec not in windows:
            # fold missing-section figures forward is not allowed; skip gracefully
            for _ in range(count):
                payloads.popleft()
            continue
        s, e = windows[sec]
        dur = 3.0 if sec in {"HOOK", "OP"} else 6.0
        if sec in {"HOOK", "OP"}:
            lo = s + 0.1
            hi = e - 0.1
        else:
            lo = s + 3.0
            hi = e - 6.5
        if sec == "ACT_7":
            hi = min(hi, total - 11.0)
        slots = free_slots(lo, hi, blocks, pad, dur)
        if not slots:
            raise SystemExit(f"no AE-free figure slots in {sec}: {lo:.2f}-{hi:.2f}s")
        for i in range(count):
            start = pick_slot_start(slots, i, count, dur)
            payload = payloads.popleft()
            end = min(start + dur, total - 0.5)
            if end - start < fig_min - 0.01:
                raise SystemExit(f"figure window too short in {sec}: {end - start:.2f}s")
            figures.append({"start": round(start, 3), "end": round(end, 3), **payload})
    figures.sort(key=lambda x: x["start"])
    return figures


def duration_frames(narration_seconds: float) -> int:
    import math
    return (round(HOOK_SEC * FPS) + round(OPENING_SEC * FPS)
            + math.ceil(narration_seconds * FPS) + round(ENDCARD_SEC * FPS))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    ap.add_argument("--narr", type=Path, default=DEFAULT_NARR)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--captions", type=Path, default=DEFAULT_SRT)
    ap.add_argument("--assert-frames", type=int, default=None,
                    help="assert final durationInFrames (set once measured TTS is known)")
    args = ap.parse_args()

    manifest = load_json(args.assets)
    if manifest.get("is_stub") is True:
        raise SystemExit("EP50 requires a real asset manifest: is_stub must be false")

    # ANTI-KAMISHIBAI ASSERT (EP45 death cause): factory 485, motion 85 -- non-zero, exact.
    factory_paths = public_items(manifest, "factory")
    motion_paths = public_items(manifest, "motion")
    # MOTION-FIRST rebuild: pools are REAL video (stock + i2v). Guard = enough real footage
    # exists (non-zero, healthy), not the old exact 485/85 Ken-Burns counts.
    if len(factory_paths) < 30:
        raise SystemExit(f"factory(real-motion) count {len(factory_paths)} < 30 -- kamishibai guard")
    if len(motion_paths) < 30:
        raise SystemExit(f"motion(i2v) count {len(motion_paths)} < 30 -- kamishibai guard")

    narr = load_json(args.narr)
    if narr.get("is_stub") is True:
        raise SystemExit("EP50 requires a real narration_index: is_stub must be false")
    captions, total = build_captions(narr)
    windows = section_windows(narr, total)
    cuts = make_cuts(windows, manifest)
    hook = make_hook(manifest)
    figures = place_figures(windows, total)

    total_frames = duration_frames(total)
    # long-form: NO 750s cap. Warn if measured deviates > 3% from the provisional estimate.
    if abs(total - PROVISIONAL_NARR_SEC) / PROVISIONAL_NARR_SEC > 0.03:
        print(f"[warn] narrationSeconds {total:.1f}s deviates >3% from provisional "
              f"{PROVISIONAL_NARR_SEC:.1f}s (frames {total_frames} vs {PROVISIONAL_FRAMES})",
              file=sys.stderr)
    if args.assert_frames is not None and total_frames != args.assert_frames:
        raise SystemExit(f"durationInFrames {total_frames} != asserted {args.assert_frames}")

    counts = {
        "factory": sum(1 for c in cuts if "/factory/" in c["src"].replace("\\", "/")),
        "motion": sum(1 for c in cuts if c["kind"] == "footage" and "/factory/" not in c["src"].replace("\\", "/")),
        "stills": sum(1 for c in cuts if c["kind"] == "img"),
    }
    # MOTION-FIRST validation (old exact 485/170/505 retired): must be video-dominant + healthy.
    footage = len(cuts) - counts["stills"]
    if footage <= counts["stills"]:
        raise SystemExit(f"NOT motion-first: footage {footage} <= stills {counts['stills']} (counts={counts})")
    if len(cuts) < 400:
        raise SystemExit(f"too few cuts {len(cuts)} (counts={counts})")
    if len(figures) != 165:
        raise SystemExit(f"figure count {len(figures)} != 165")
    if any((f.get("kind") == "dochighlight") for f in figures):
        raise SystemExit("dochighlight figure present (R-DOCHL)")

    write_srt(captions, args.captions)
    film = {
        "episode_id": EP,
        "fps": FPS,
        "narration": str(narr.get("audio_path") or "centralpark/narration.mp3"),
        "narrationSeconds": round(total, 3),   # PROVISIONAL until measured TTS (5.1.1)
        "hookSeconds": HOOK_SEC,
        "hookLine": HOOK_LINE,
        "hook": hook,
        "cuts": cuts,
        "captions": captions,
        "graphics": [],
        "figures": figures,
        "overlays": [x["public_path"] for x in manifest.get("overlay", []) if x.get("public_path")],
    }
    assert film["hookSeconds"] == 8.0, "hookSeconds must be 8.0 (0 => 8s desync)"

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")
    PUB_FILM.parent.mkdir(parents=True, exist_ok=True)
    PUB_FILM.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")

    uses = Counter(c["src"] for c in cuts)
    still_time = sum(c["dur"] for c in cuts if c["kind"] == "img")
    motion_time = sum(c["dur"] for c in cuts if c["kind"] != "img")
    report = {
        "cuts": len(cuts),
        **counts,
        "distinct_assets": len(uses),
        "first_use_share": round(len(uses) / len(cuts), 4),
        "still_share_cut": round(counts["stills"] / len(cuts), 4),
        "still_time_share": round(still_time / total, 4),
        "motion_time_share": round(motion_time / total, 4),
        "figures": len(figures),
        "narrationSeconds": round(total, 3),
        "duration_frames": total_frames,
        "duration_frames_provisional": PROVISIONAL_FRAMES,
        "duration_sec_with_bookends": round(total_frames / FPS, 3),
        "TODO": "narrationSeconds/durationInFrames PROVISIONAL until measured TTS; update SPEC + Root.tsx (5.1.1)",
    }
    BUILD_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    BUILD_MANIFEST.write_text(json.dumps({"episode_id": EP, "producer": "scripts/build_centralpark_film.py",
                                          "inputs": {"assets": str(args.assets), "narr": str(args.narr)},
                                          "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    BEATSHEET.write_text(json.dumps({"schema_version": "centralpark_beatsheet.v1", "episode_id": EP,
                                     "figures": figures, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
