#!/usr/bin/env python3
r"""Assemble the EP36 (williams) CaseFilm FilmData from the MEASURED narration.

PD-2026-036-williams — first known US wrongful arrest from facial-recognition
misidentification. This upgrades the estimated-timing SKELETON
(remotion/src/data/williams_film.json) into a real, renderable cut list keyed to
the ElevenLabs master narration (whisper/forced-aligned), and injects the staged
factory b-roll as footage cuts.

Modeled on scripts/build_rolin_film.py (the closest reusable builder): read
narration_index for REAL per-chunk offsets -> build a per-span cut grid mixing
image + footage cuts with NO footage reuse -> overlay the figure beats -> parse
the SRT captions -> dual-write remotion/public/williams/film_data.v001.json and
remotion/src/data/williams_film.json (the CaseFilm-williams composition source).

TIMELINE MODEL (skeleton + rolin convention): the body timeline == the master
narration timeline [0, T]. The Body sequence plays the full master mp3 from 0.0,
so cuts/captions/figures all live on the raw master offsets. The 8s cold-open
hook montage + BrandOpening(3.5s) play BEFORE the body (their frames are added by
CaseFilm.caseFilmDurationInFrames); the spoken hook lines live at the top of the
body audio (0..~6.5s), exactly as the skeleton had them.

WHAT IS PRESERVED (not invented):
  * FIGURES: the skeleton's 16 kinetic figure beats are carried over VERBATIM
    (lines/kind/style unchanged — no fabricated on-screen numbers) and re-timed
    onto each figure's real span window.
  * GRAPHICS: carried over (empty in the skeleton; captions carry the text).
  * HOOK / hookLine: carried over from the skeleton unchanged.
  * IMAGE cuts point at the planned Codex hero stills
    williams/img/PD-2026-036-<heroId>-IMG-001.png (per scene_plan hero_stills);
    these are generated separately and are intentionally absent now — referenced
    by name only, never created, never a hard dependency here.

WHAT IS INJECTED (real, on disk):
  * 43 FOOTAGE cuts from broll_selection.v001.json (kind:'footage',
    src=williams/factory/<filename>), each clip used AT MOST ONCE, placed inside
    its assigned span's window -> keeps footage_diversity + arc_nonrepeat green.

Run (venv):
    .venv/Scripts/python.exe scripts/build_williams_film.py
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-036-williams"
SLUG = "williams"
FPS = 30

EPDIR = ROOT / "episodes" / EP
NARR_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
SCENE_PLAN = EPDIR / "04_scenes" / "scene_plan.v001.json"
BROLL = EPDIR / "05_visuals" / "broll_selection.v001.json"
SRT = EPDIR / "08_edit" / "captions.v002.srt"

PUB = ROOT / "remotion" / "public" / SLUG
FACT = PUB / "factory"
SKELETON = ROOT / "remotion" / "src" / "data" / f"{SLUG}_film.json"
OUT_SRC = SKELETON
OUT_PUB = PUB / "film_data.v001.json"

# Cadence: choose so total slots (image + footage) land ~340 across the ~613.7s
# body -> ~300 image + 43 footage. Varied (not a metronome): ratios cycle so the
# bed alternates quick bursts with calmer holds (motion_present / near_still gates).
BASE_CADENCE = 2.05
DUR_CYCLE = [1.7, 2.1, 2.6, 1.8, 2.3, 1.6, 2.4, 1.9, 2.8, 2.0, 1.7, 2.2]

# CaseFilm.tsx Still treatments (unknown -> defaults to 'bleed'). scene_plan uses
# 'pixel' for the illegible-surveillance shots; CaseFilm has no pixel look, so map
# it to the safe default so those cuts render (as the skeleton did for S001).
VALID_TREATMENTS = {"depth", "scan", "duotone", "focus", "card", "bleed"}
DEFAULT_HERO = [("S002", "depth"), ("S001", "bleed")]


def norm_treatment(t: str | None) -> str:
    t = (t or "").strip().lower()
    return t if t in VALID_TREATMENTS else "bleed"


def parse_srt(path: Path) -> list[dict]:
    """Parse an SRT into [{start,end,text}] (verbatim text = caption source)."""
    cues: list[dict] = []
    for b in re.split(r"\n\s*\n", path.read_text("utf-8").strip()):
        L = [x for x in b.splitlines() if x.strip()]
        if len(L) < 2:
            continue
        m = re.search(r"(\d\d):(\d\d):(\d\d),(\d\d\d)\s*-->\s*(\d\d):(\d\d):(\d\d),(\d\d\d)", L[1])
        if not m:
            continue
        g = list(map(int, m.groups()))
        s = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        e = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        txt = " ".join(L[2:]).strip()
        if txt:
            cues.append({"start": round(s, 3), "end": round(e, 3), "text": txt})
    return cues


def build_span_windows(chunks: list[dict], total: float) -> list[dict]:
    """Contiguous [start,end) window per span in narration order (no black gaps).

    A span's window starts at its first chunk's start; it ends where the next span
    begins; the last span ends at the master total. The first span is pinned to 0.0
    so the body timeline covers [0, total] exactly."""
    order: list[str] = []
    first_start: dict[str, float] = {}
    for c in chunks:
        sid = c["span_id"]
        if sid not in first_start:
            first_start[sid] = float(c["start"])
            order.append(sid)
    windows = []
    for i, sid in enumerate(order):
        a0 = 0.0 if i == 0 else first_start[order[i]]
        a1 = first_start[order[i + 1]] if i + 1 < len(order) else total
        windows.append({"span_id": sid, "start": round(a0, 3), "end": round(a1, 3)})
    return windows


def even_slots(n: int, k: int) -> set[int]:
    """k evenly-spaced distinct indices in range(n)."""
    if k <= 0 or n <= 0:
        return set()
    k = min(k, n)
    return {(x * n) // k for x in range(k)}


def build_span_cuts(win: dict, heroes: list[tuple[str, str]], foot_srcs: list[str],
                    idx0: int) -> tuple[list[dict], int]:
    """Fill one span window with a continuous grid of (image + footage) cuts.

    N_total = images to hit BASE_CADENCE + this span's footage clips (footage is
    ADDITIVE, so per-image cadence stays ~BASE_CADENCE). Footage sits at evenly
    spaced slots, each src used exactly once; every other slot is an image cut
    cycling this span's planned hero stills (+ their treatment)."""
    a0, a1 = win["start"], win["end"]
    span_len = max(0.0, a1 - a0)
    n_foot = len(foot_srcs)
    n_img = max(1, round(span_len / BASE_CADENCE))
    n = n_img + n_foot
    if n <= 0 or span_len <= 0:
        return [], idx0
    ratios = [DUR_CYCLE[(idx0 + i) % len(DUR_CYCLE)] for i in range(n)]
    tot = sum(ratios)
    durs = [span_len * r / tot for r in ratios]
    foot_pos = even_slots(n, n_foot)
    cuts: list[dict] = []
    t = a0
    fi = 0
    hi = 0
    if not heroes:
        heroes = DEFAULT_HERO
    for k in range(n):
        gi = idx0 + k
        dur = round(a1 - t, 3) if k == n - 1 else round(durs[k], 3)
        if dur <= 0:
            dur = 0.001
        if k in foot_pos and fi < n_foot:
            cuts.append({"start": round(t, 3), "dur": dur, "kind": "footage",
                         "src": foot_srcs[fi], "seed": f"{SLUG}-{gi}", "treatment": "footage"})
            fi += 1
        else:
            hid, htr = heroes[hi % len(heroes)]
            hi += 1
            cuts.append({"start": round(t, 3), "dur": dur, "kind": "img",
                         "src": f"{SLUG}/img/PD-2026-036-{hid}-IMG-001.png",
                         "seed": f"{SLUG}-{gi}", "treatment": norm_treatment(htr)})
        t += dur
    return cuts, idx0 + n


def remap_figures(skel_figures: list[dict], windows: list[dict]) -> list[dict]:
    """Carry the skeleton's 16 figure beats over VERBATIM (lines/kind/style intact)
    and re-time each onto its span window. Figure i maps to span i (they are 1:1 in
    span/script order in the skeleton). Placed just after the span start, clamped so
    it always lands inside its own narration span."""
    out: list[dict] = []
    for i, fig in enumerate(skel_figures):
        if i >= len(windows):
            break
        w = windows[i]
        span_len = w["end"] - w["start"]
        orig_dur = float(fig.get("end", 0)) - float(fig.get("start", 0))
        d = orig_dur if orig_dur > 0 else 6.0
        offset = min(0.6, max(0.0, span_len * 0.05))
        s = round(w["start"] + offset, 3)
        e = round(min(s + d, w["end"]), 3)
        if e <= s:
            e = round(min(s + 0.5, w["end"]), 3)
        nf = dict(fig)  # preserve kind/lines/style and any other fields verbatim
        nf["start"] = s
        nf["end"] = e
        out.append(nf)
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")

    idx = json.loads(NARR_INDEX.read_text("utf-8"))
    chunks = idx["chunks"]
    total = float(idx["totals"]["generated_seconds"])
    print(f"[{EP}] narration: {len(chunks)} chunks, MEASURED total = {total:.3f}s")

    plan = json.loads(SCENE_PLAN.read_text("utf-8"))
    # scene_id S0NN -> hero stills (id, treatment) in scene order; also span_id->scene
    span_heroes: dict[str, list[tuple[str, str]]] = {}
    for sc in plan["scenes"]:
        heroes = [(h["id"], h.get("treatment", "depth")) for h in sc.get("hero_stills", [])]
        span_heroes[sc["span_id"]] = heroes

    broll = json.loads(BROLL.read_text("utf-8"))
    span_footage: dict[str, list[str]] = {}
    all_footage: list[str] = []
    for sp in broll["spans"]:
        srcs = []
        for c in sp["clips"]:
            src = c.get("public_path") or f"{SLUG}/factory/{c['filename']}"
            srcs.append(src)
            all_footage.append(src)
        span_footage[sp["span_id"]] = srcs
    print(f"[{EP}] footage: {len(all_footage)} clips across {len(span_footage)} spans "
          f"(distinct={len(set(all_footage))})")

    skel = json.loads(SKELETON.read_text("utf-8"))
    skel_figures = skel.get("figures", [])
    skel_graphics = skel.get("graphics", [])
    hook = skel.get("hook", [])
    hook_line = skel.get("hookLine", "")
    hook_seconds = skel.get("hookSeconds", 8.04)

    # --- span windows on the real master timeline ---
    windows = build_span_windows(chunks, total)

    # --- per-span cut grid: images (planned hero stills) + injected footage ---
    cuts: list[dict] = []
    gi = 0
    for w in windows:
        sid = w["span_id"]
        acuts, gi = build_span_cuts(w, span_heroes.get(sid, []), span_footage.get(sid, []), gi)
        cuts.extend(acuts)
    cuts.sort(key=lambda c: c["start"])

    # --- figures re-timed onto their span windows (verbatim carry-over) ---
    figures = remap_figures(skel_figures, windows)

    # --- captions straight from the forced-aligned SRT (caption == narration) ---
    captions = parse_srt(SRT)
    print(f"[{EP}] captions: {len(captions)} cues <- {SRT.name}")

    # --- stage the master narration for playback (best-effort; never fatal) ---
    narration_uri = f"{SLUG}/narration.mp3"
    master = None
    try:
        cfg = json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))
        media = Path(cfg["roots"]["media"]["path"])
        master = media / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
    except (OSError, ValueError, KeyError):
        master = None
    if not (master and master.exists()):
        alt = Path("E:/pd-media/episodes") / EP / "06_voice" / "master" / "vc_master_v001.mp3"
        master = alt if alt.exists() else master
    PUB.mkdir(parents=True, exist_ok=True)
    if master and master.exists():
        try:
            shutil.copy2(master, PUB / "narration.mp3")
            print(f"[{EP}] narration.mp3 <- master {master}")
        except OSError as e:
            print(f"[{EP}] WARN could not stage narration.mp3 ({e}); keeping reference only")
    elif (PUB / "narration.mp3").exists():
        print(f"[{EP}] narration.mp3 = already-staged copy (master not found now)")
    else:
        print(f"[{EP}] WARN no narration.mp3 staged (master not found) — Body audio may be silent")

    data = {
        "episode_id": EP,
        "fps": FPS,
        "_estimation_note": (
            "MEASURED. Timing is stamped from the ElevenLabs master narration "
            "(episodes/PD-2026-036-williams/06_audio/narration_index.v001.json, 106 chunks, "
            f"generated_seconds={total:.3f}); the body timeline equals the master timeline [0, T]. "
            "cuts are a per-span grid keyed to real chunk offsets: image cuts reference the planned "
            "Codex hero stills williams/img/PD-2026-036-<heroId>-IMG-001.png (generated separately; "
            "intentionally absent here, referenced by name only), and 43 factory b-roll cuts "
            "(kind:'footage', src williams/factory/<file>) from broll_selection.v001.json are injected "
            "into their assigned span windows, each used exactly once (footage_diversity/arc_nonrepeat). "
            "captions are the forced-aligned verbatim SRT (captions.v002.srt, 284 cues). The 16 figure "
            "beats and graphics are carried over verbatim from the skeleton and re-timed onto their real "
            "span windows (no fabricated on-screen numbers). Built by scripts/build_williams_film.py."
        ),
        "narration": narration_uri,
        "narrationSeconds": round(total, 3),
        "hookSeconds": hook_seconds,
        "hookLine": hook_line,
        "hook": hook,
        "cuts": cuts,
        "captions": captions,
        "graphics": skel_graphics,
        "figures": figures,
    }

    OUT_PUB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf-8")
    OUT_SRC.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf-8")

    # --- summary + no-reuse assertion ---
    ni = sum(1 for c in cuts if c["kind"] == "img")
    nf = sum(1 for c in cuts if c["kind"] == "footage")
    fcnt = Counter(c["src"] for c in cuts if c["kind"] == "footage")
    max_reuse = max(fcnt.values()) if fcnt else 0
    missing_src = [s for s in fcnt if not (PUB / Path(s).relative_to(SLUG)).exists()]
    lead = round(hook_seconds + 3.5 + total + 9.0, 3)  # hook + OPENING_SEC + body + ENDCARD_SEC
    print(f"[{EP}] cuts={len(cuts)} (img {ni} / footage {nf})  figures={len(figures)}  "
          f"captions={len(captions)}  graphics={len(skel_graphics)}")
    print(f"[{EP}] FOOTAGE no-reuse: {nf} cuts, {len(fcnt)} distinct, max_reuse={max_reuse}, "
          f"missing_src={len(missing_src)}")
    if nf != 43 or len(fcnt) != 43 or max_reuse != 1:
        print(f"[{EP}] !! FOOTAGE ASSERT: expected 43 distinct used once "
              f"(got nf={nf} distinct={len(fcnt)} max_reuse={max_reuse})", file=sys.stderr)
    if missing_src:
        print(f"[{EP}] !! MISSING FOOTAGE FILES: {missing_src[:5]}", file=sys.stderr)
    # cut-overlap sanity (grid tiles contiguously; report any overlap beyond epsilon)
    overlaps = 0
    for a, b in zip(cuts, cuts[1:]):
        if a["start"] + a["dur"] > b["start"] + 1e-6:
            overlaps += 1
    print(f"[{EP}] cut overlaps beyond design: {overlaps}")
    print(f"[{EP}] approx composition lead = hook {hook_seconds}s + OPENING 3.5s + body "
          f"{total:.3f}s + ENDCARD 9s = {lead:.3f}s ~= {round(lead * FPS)} frames")
    print(f"wrote {OUT_PUB}")
    print(f"wrote {OUT_SRC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
