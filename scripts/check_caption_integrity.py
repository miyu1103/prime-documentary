#!/usr/bin/env python3
r"""Independent CAPTION-INTEGRITY gate — catches a render that SHOWS no burned narration captions,
or whose kinetic on-screen text just echoes / collides with the narration captions, BEFORE render.

WHY THIS EXISTS (EP36 williams post-mortem)
-------------------------------------------
EP36 williams shipped (nearly) with NO burned-in narration captions. The existing caption gates all
passed because they only confirm the SRT *sidecar* file exists (``08_edit/captions.v*.srt``) — they
never verify the composition actually RENDERS a burned caption track on top of the picture. A code-
driven premium composition (WilliamsFilm-style) can carry a perfectly good SRT on disk and still burn
nothing into the frame. Separately, the on-screen KINETIC emphasis text and the burned captions
collided at the BOTTOM of the frame (same safe-zone band) and, worse, the kinetic phrases were mostly
verbatim echoes of the narration line playing at that instant — double text, redundant reading.

This gate reads COMPOSITION + BEATSHEET + CAPTION DATA (not rendered pixels) so it fails CHEAPLY,
before the expensive render. It never inspects the video file. Two independent sub-checks, ANDed:

SUB-CHECK 1 — BURNED-CAPTION PRESENCE (hard)
--------------------------------------------
Confirm the composition that renders this episode actually wires a burned NARRATION-caption track.
Two accepted wirings:
  (A) code-driven / film-timed JSON: a ``remotion/src/data/<slug>_captions*.json`` cue file EXISTS,
      AND the episode's composition tsx IMPORTS that json (the imported identifier is USED below the
      import, i.e. not dead) AND renders a non-kinetic caption component (a ``*Caption(s)`` JSX tag
      that is NOT ``KineticCaptions`` — e.g. ``<BurnedCaptions/>``). This is exactly WilliamsFilm.
  (B) CaseFilm data path: the resolved composition references ``data.captions`` AND the episode's
      ``<slug>_film.json`` carries a NON-EMPTY ``captions[]`` array (CaseFilm's ``<Captions cues=…>``).
If NEITHER wiring is present -> FAIL "no burned narration captions in the render". (Note: a
``<slug>_film.json`` with a captions[] array does NOT rescue a code-driven comp that never renders it
— that was the exact williams near-miss: williams_film.json HAS captions[], but WilliamsFilm renders
BurnedCaptions from the JSON, not data.captions. Wiring (B) only counts when the render comp is the
CaseFilm-style one that actually mounts data.captions.)

SUB-CHECK 2 — KINETIC <-> CAPTION REDUNDANCY & COLLISION (hard)
--------------------------------------------------------------
Parse the beatsheet beats' ``onscreen`` kinetic text and the narration caption cues (film-timed JSON
preferred, else ``08_edit/captions.v*.srt``). For every beat that carries on-screen kinetic text,
compute how much that kinetic phrase echoes the narration caption(s) playing in the SAME time window
[start_s, start_s+dur_s]. Per-beat similarity =
      max( token-containment , best-per-cue difflib ratio )
  - token-containment (asymmetric) = |kinetic_tokens ∩ window_caption_tokens| / |kinetic_tokens|
      = the fraction of the on-screen words the narrator is ALSO speaking in that window. Asymmetric
        on purpose: a short kinetic phrase ("A MACHINE LOOKING AT ONE") lifted verbatim out of a long
        spoken sentence is a full echo even though a symmetric ratio over the whole block is diluted.
  - best-per-cue difflib ratio = max over overlapping cues of SequenceMatcher(normalized) ratio
      = catches a kinetic phrase that mirrors ONE specific cue almost word-for-word.
A beat is REDUNDANT when that similarity > SIM_REDUNDANT (0.60). We report the redundant count and
the redundant FRACTION over all onscreen-bearing beats. FAIL when the fraction >
MAX_REDUNDANT_FRACTION (0.40) — i.e. when a large share of the kinetic text merely re-reads the
caption. COLLISION: if the kinetic on-screen captions are anchored to the BOTTOM band (same as the
burned captions) while burned captions are present, the two text tracks physically overlap -> FAIL.
Bottom-anchoring is read from (i) any onscreen beat carrying ``anchor:"bottom"`` (beat or props), and
(ii) a code scan of the render comp + the episode's ``components/<slug>/`` dir for ``KineticCaptions``
usages whose ``anchor`` attribute is ``"bottom"`` OR ABSENT (KineticCaptions defaults to bottom).

CALIBRATION (measured 2026-07-11 on PD-2026-036-williams, the FIXED cut)
-----------------------------------------------------------------------
  williams: burned captions -> PRESENT (WilliamsFilm imports williams_captions.v003.json + renders
            <BurnedCaptions/>) -> sub-check 1 PASS.
  williams: 111 beats carry onscreen kinetic text; 18 (16.2%) echo the caption at SIM>0.60, which is
            below the 40% fail line -> not egregious. Kinetic captions were all moved to anchor="top"
            (WilliamsScene / WilliamsFactoryCut / MgWithCaption) while BurnedCaptions sit at the
            bottom -> NO collision. -> sub-check 2 PASS. Overall williams PASS.
Thresholds sit above williams' measured 16.2% (fraction floor 0.40) so the FIXED cut passes, while a
comp that dropped BurnedCaptions, or bottom-anchored the kinetic text, or whose kinetic beats all
re-read the narration, FAILS. (RED selftest fixtures exercise each of those failure modes.)

Usage:
  py -3.11 scripts/check_caption_integrity.py --ep PD-2026-036-williams
  py -3.11 scripts/check_caption_integrity.py --ep williams --json out.json
  py -3.11 scripts/check_caption_integrity.py --selftest   # RED fixtures (must FAIL) + GREEN + real run

Exit codes: 0 = PASS (or artifact-absent skip), 1 = FAIL / usage error.

check_final_acceptance imports this module and calls ``evaluate(epdir)``; the returned dict keys
(check / ok / hard / reason / skipped / burned_present / redundant_fraction / redundant_beats /
onscreen_beats / collision / floors) are the stable contract. ``evaluate`` NEVER calls sys.exit and
never raises on missing inputs — it returns a skip dict so the caller cannot crash.
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "remotion" / "src" / "data"
COMP_DIR = ROOT / "remotion" / "src" / "compositions"
DEFAULT_EP = "PD-2026-036-williams"
CHECK_NAME = "caption_integrity"

# ---- HARD thresholds (see the module docstring CALIBRATION note for the measured williams numbers) --
SIM_REDUNDANT = 0.60          # per-beat kinetic<->caption similarity above which the beat "echoes" the caption
MAX_REDUNDANT_FRACTION = 0.40  # max share of onscreen beats that may echo the caption before we FAIL
                               # (williams measured 0.162 — passes; an all-echo cut -> ~1.0 -> fails)


# ------------------------------------------------------------------------------------------------
# path / artifact resolution
# ------------------------------------------------------------------------------------------------

def _slug_of(name: str) -> str:
    """Episode folder / slug -> the core slug (strip a leading PD-YYYY-NNN- prefix), mirroring the
    rest of the suite so this gate resolves the SAME <slug>_captions.json / <Slug>Film.tsx."""
    return re.sub(r"^PD-\d{4}-\d{3}-", "", str(name))


def _read(p: Path) -> Optional[str]:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:  # noqa: BLE001
        return None


def _load_json(p: Path) -> Optional[Any]:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 - unreadable/malformed -> treat as absent
        return None


def resolve_beatsheet(epdir: Path) -> Optional[Path]:
    """Latest episodes/<ep>/04_scenes/premium_beatsheet.v*.json, or None."""
    cands = sorted((epdir / "04_scenes").glob("premium_beatsheet.v*.json"))
    return cands[-1] if cands else None


def resolve_captions_json(data_dir: Path, slug: str) -> Optional[Path]:
    """Latest film-timed remotion/src/data/<slug>_captions*.json, or None. Only *.json (film-timed
    cue tables) — the CaseFilm *_captions.ts typed sources are a different, non-film-timed artifact."""
    tail = slug.split("-")[-1].lower()
    cands = sorted(data_dir.glob(f"{slug}_captions*.json")) or sorted(data_dir.glob(f"{tail}_captions*.json"))
    return cands[-1] if cands else None


def resolve_film_json(data_dir: Path, slug: str) -> Optional[Path]:
    """The CaseFilm <slug>_film.json (for the data.captions[] wiring path), or None."""
    tail = slug.split("-")[-1].lower()
    for cand in (data_dir / f"{slug}_film.json", data_dir / f"{tail}_film.json"):
        if cand.is_file():
            return cand
    return None


def resolve_compositions(comp_dir: Path, slug: str, epname: str) -> list[Path]:
    """Find the composition tsx(s) that render this episode. A comp qualifies if its filename carries
    the episode slug tail (e.g. WilliamsFilm.tsx for 'williams'), OR its body references the episode's
    beatsheet / captions json / film json. We keep ALL candidates and OR the burned-caption signal
    across them (thumbnails etc. simply contribute nothing)."""
    tail = slug.split("-")[-1].lower()
    epslug = epname.replace("\\", "/")
    out: list[Path] = []
    if not comp_dir.is_dir():
        return out
    for p in sorted(comp_dir.glob("*.tsx")):
        stem = p.stem.lower()
        name_match = bool(tail) and tail in stem
        txt = _read(p) or ""
        body = txt.replace("\\", "/")
        content_match = (
            f"{slug}_captions" in txt or f"{tail}_captions" in txt
            or f"{slug}_film" in txt or f"{tail}_film" in txt
            or f"{epslug}/04_scenes/premium_beatsheet" in body
            or f"/{slug}/04_scenes/premium_beatsheet" in body
        )
        if name_match or content_match:
            out.append(p)
    root_tsx = comp_dir.parent / "Root.tsx"
    root_txt = _read(root_tsx) or ""
    tail_title = tail[:1].upper() + tail[1:]
    if (
        root_tsx.is_file()
        and (
            f"{tail}Film" in root_txt
            or f"Ep{epname.split('-')[2].lstrip('0')}{tail_title}" in root_txt
            or f"id=\"Ep" in root_txt and f"{tail_title}" in root_txt and "<CaseFilm" in root_txt
        )
        and root_tsx not in out
    ):
        out.append(root_tsx)
    return out


# ------------------------------------------------------------------------------------------------
# SUB-CHECK 1 — burned narration caption presence
# ------------------------------------------------------------------------------------------------

# JSX caption tags, EXCLUDING KineticCaptions (which renders the kinetic ONSCREEN emphasis text, not
# the narration cue track). A non-kinetic caption tag == a burned narration-caption layer.
_CAPTION_TAG_RE = re.compile(r"<([A-Za-z][A-Za-z0-9]*Captions?)\b")


def _comp_renders_burned_caption(txt: str, captions_json: Optional[Path]) -> tuple[bool, bool, bool]:
    """(via_json, imports_json_and_used, renders_noncaption_tag) for one comp's source text.

    via_json is True when the film-timed captions JSON EXISTS, the comp imports it AND uses the
    imported identifier (not dead), AND the comp renders a non-kinetic caption JSX tag."""
    # (a) a non-kinetic caption component is rendered?
    non_kinetic_tag = any(m.group(1) != "KineticCaptions" for m in _CAPTION_TAG_RE.finditer(txt))
    # (b) the film-timed captions JSON is imported AND its identifier is used below the import.
    imports_used = False
    if captions_json is not None:
        stem = captions_json.name
        # match:  import <ident> from '.../<file>.json'
        m = re.search(r"import\s+([A-Za-z_$][\w$]*)\s+from\s+['\"][^'\"]*"
                      + re.escape(stem.replace(".json", "")) + r"[^'\"]*['\"]", txt)
        if m:
            ident = m.group(1)
            # used again anywhere after the import line?
            imports_used = len(re.findall(r"\b" + re.escape(ident) + r"\b", txt)) >= 2
    via_json = bool(captions_json) and imports_used and non_kinetic_tag
    return via_json, imports_used, non_kinetic_tag


def _comp_uses_datacaptions(txt: str) -> bool:
    """CaseFilm-style wiring: the comp mounts ``data.captions`` (``<Captions cues={data.captions}/>``)."""
    return "data.captions" in txt


def _renders_casefilm_engine(txt: str, comp_dir: Path) -> bool:
    """A thin per-episode wrapper that renders ``<CaseFilm data={...}/>`` INHERITS the shared
    engine's burned ``<Captions cues={data.captions}/>`` layer. The literal ``data.captions`` lives
    in CaseFilm.tsx, not the wrapper — so confirm the engine actually mounts it. This is what keeps
    data-driven CaseFilm episodes (forfeiture, rolin, kidsforcash…) from false-failing the gate."""
    if not (re.search(r"<CaseFilm\b", txt) or "component={CaseFilm}" in txt):
        return False
    comp_dir = Path(comp_dir)
    engine_candidates = [
        comp_dir / "CaseFilm.tsx",
        comp_dir / "compositions" / "CaseFilm.tsx",
    ]
    return any("data.captions" in (_read(engine) or "") for engine in engine_candidates)


def evaluate_burned_presence(comps: list[Path], captions_json: Optional[Path],
                             film_json: Optional[Path]) -> dict[str, Any]:
    """Sub-check 1. Returns {present, path, wiring, ...} — never raises."""
    via_json_hit: Optional[str] = None
    datacap_hit: Optional[str] = None
    any_non_kinetic = False
    for p in comps:
        txt = _read(p) or ""
        via_json, _imports_used, non_kinetic = _comp_renders_burned_caption(txt, captions_json)
        any_non_kinetic = any_non_kinetic or non_kinetic
        if via_json and via_json_hit is None:
            via_json_hit = str(p)
        if (_comp_uses_datacaptions(txt) or _renders_casefilm_engine(txt, p.parent)) and datacap_hit is None:
            datacap_hit = str(p)

    # CaseFilm data path only counts if the render comp mounts data.captions AND film json has cues.
    film_captions_n = 0
    if film_json is not None:
        fj = _load_json(film_json)
        if isinstance(fj, dict) and isinstance(fj.get("captions"), list):
            film_captions_n = len(fj["captions"])
    casefilm_ok = bool(datacap_hit) and film_captions_n > 0

    if via_json_hit:
        return {"present": True, "wiring": "film_timed_json", "comp": via_json_hit,
                "captions_json": str(captions_json) if captions_json else None,
                "reason": f"burned narration captions wired (imports {Path(str(captions_json)).name if captions_json else '?'} "
                          f"+ renders a burned caption layer in {Path(via_json_hit).name})"}
    if casefilm_ok:
        return {"present": True, "wiring": "casefilm_data_captions", "comp": datacap_hit,
                "film_captions": film_captions_n,
                "reason": f"burned narration captions wired (CaseFilm data.captions[{film_captions_n}] "
                          f"mounted in {Path(datacap_hit).name})"}
    # not present — build a precise diagnostic
    bits = []
    bits.append("film-timed captions json " + ("exists" if captions_json else "MISSING"))
    bits.append("non-kinetic caption tag " + ("rendered" if any_non_kinetic else "ABSENT"))
    bits.append("data.captions " + ("mounted" if datacap_hit else "not mounted")
                + f" (film captions[]={film_captions_n})")
    return {"present": False, "wiring": None, "comp": (str(comps[0]) if comps else None),
            "captions_json": str(captions_json) if captions_json else None,
            "reason": "no burned narration captions in the render — " + "; ".join(bits)}


# ------------------------------------------------------------------------------------------------
# SUB-CHECK 2 — kinetic <-> caption redundancy & collision
# ------------------------------------------------------------------------------------------------

def _norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _toks(s: str) -> list[str]:
    return [t for t in _norm(s).split() if t]


def _parse_srt(txt: str) -> list[dict[str, Any]]:
    """Minimal SRT -> [{start,end,text}] (seconds). Best-effort; malformed blocks are skipped."""
    def sec(ts: str) -> float:
        ts = ts.strip().replace(",", ".")
        h, m, s = ts.split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)
    cues: list[dict[str, Any]] = []
    for block in re.split(r"\n\s*\n", txt.strip()):
        lines = [ln for ln in block.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue
        tl = next((ln for ln in lines if "-->" in ln), None)
        if not tl:
            continue
        try:
            a, b = tl.split("-->")
            start, end = sec(a), sec(b)
        except Exception:  # noqa: BLE001
            continue
        text = " ".join(lines[lines.index(tl) + 1:])
        if text:
            cues.append({"start": start, "end": end, "text": text})
    return cues


def load_caption_cues(captions_json: Optional[Path], epdir: Path) -> tuple[list[dict[str, Any]], Optional[str]]:
    """Prefer the film-timed captions JSON; else the latest 08_edit/captions*.srt. Returns (cues, src)."""
    if captions_json is not None:
        data = _load_json(captions_json)
        if isinstance(data, list):
            cues = [{"start": float(c.get("start", 0)), "end": float(c.get("end", 0)),
                     "text": str(c.get("text", ""))}
                    for c in data if isinstance(c, dict) and c.get("text")]
            if cues:
                return cues, str(captions_json)
    srts = sorted((epdir / "08_edit").glob("captions*.srt"))
    if srts:
        txt = _read(srts[-1])
        if txt:
            cues = _parse_srt(txt)
            if cues:
                return cues, str(srts[-1])
    return [], None


def _window_block(cues: list[dict[str, Any]], s0: float, s1: float) -> str:
    return " ".join(c["text"] for c in cues if c["start"] < s1 and c["end"] > s0)


def _beat_similarity(kinetic: str, cues: list[dict[str, Any]], s0: float, s1: float) -> float:
    """max(token-containment over the overlapping caption block, best per-cue difflib ratio)."""
    ktoks = _toks(kinetic)
    if not ktoks:
        return 0.0
    block = _window_block(cues, s0, s1)
    ctoks = set(_toks(block))
    containment = sum(1 for t in ktoks if t in ctoks) / len(ktoks)
    best_ratio = 0.0
    nk = _norm(kinetic)
    for c in cues:
        if c["start"] < s1 and c["end"] > s0:
            best_ratio = max(best_ratio, difflib.SequenceMatcher(None, nk, _norm(c["text"])).ratio())
    return max(containment, best_ratio)


def _beat_times(b: dict[str, Any], fps: float) -> tuple[float, float]:
    s0 = b.get("start_s")
    dur = b.get("dur_s")
    if s0 is None:
        s0 = float(b.get("start_frame", 0)) / fps
    if dur is None:
        dur = float(b.get("dur_frames", 0)) / fps
    return float(s0), float(s0) + float(dur or 0.0)


def _beat_onscreen_text(b: dict[str, Any]) -> str:
    on = b.get("onscreen")
    if isinstance(on, list):
        return " ".join(str(x) for x in on if x)
    if isinstance(on, str):
        return on
    return ""


def _bottom_anchored_kinetic(beats: list[dict[str, Any]], comps: list[Path],
                             comp_dir: Path, slug: str) -> tuple[bool, list[str]]:
    """Is the kinetic ONSCREEN caption track anchored to the BOTTOM band (colliding with burned
    captions at the bottom)? Sources: (i) beat/props anchor=='bottom'; (ii) code scan of the render
    comp + components/<slug>/ for <KineticCaptions ...> whose anchor attr is 'bottom' or ABSENT
    (KineticCaptions defaults to bottom)."""
    evidence: list[str] = []
    # (i) beat-level anchor
    for b in beats:
        if not _beat_onscreen_text(b):
            continue
        a = b.get("anchor")
        pa = (b.get("props") or {}).get("anchor") if isinstance(b.get("props"), dict) else None
        if str(a).lower() == "bottom" or str(pa).lower() == "bottom":
            evidence.append(f"beat {b.get('beat')} anchor=bottom")
    # (ii) code scan
    tail = slug.split("-")[-1].lower()
    scan_files = list(comps)
    comp_subdir = comp_dir.parent / "components" / tail
    if comp_subdir.is_dir():
        scan_files += sorted(comp_subdir.glob("*.tsx"))
    for p in scan_files:
        txt = _read(p) or ""
        for m in re.finditer(r"<KineticCaptions\b([^>]*)>", txt, re.DOTALL):
            attrs = m.group(1)
            am = re.search(r"anchor\s*=\s*['\"]([a-zA-Z]+)['\"]", attrs)
            anchor = am.group(1).lower() if am else "bottom"  # default is bottom
            if anchor == "bottom":
                evidence.append(f"{p.name}: KineticCaptions anchor={'absent(default bottom)' if not am else 'bottom'}")
    return (len(evidence) > 0), evidence


def evaluate_redundancy(beats: list[dict[str, Any]], cues: list[dict[str, Any]], fps: float,
                        burned_present: bool, comps: list[Path], comp_dir: Path,
                        slug: str) -> dict[str, Any]:
    """Sub-check 2. Returns redundancy fraction + collision. Never raises."""
    onscreen_beats = 0
    redundant = 0
    examples: list[dict[str, Any]] = []
    for b in beats:
        kt = _beat_onscreen_text(b)
        if not kt:
            continue
        onscreen_beats += 1
        s0, s1 = _beat_times(b, fps)
        sim = _beat_similarity(kt, cues, s0, s1)
        if sim > SIM_REDUNDANT:
            redundant += 1
            if len(examples) < 6:
                examples.append({"beat": b.get("beat"), "sim": round(sim, 2), "kinetic": kt[:60],
                                 "caption": _window_block(cues, s0, s1)[:60]})
    frac = (redundant / onscreen_beats) if onscreen_beats else 0.0

    bottom, evidence = _bottom_anchored_kinetic(beats, comps, comp_dir, slug)
    collision = bool(bottom and burned_present)

    problems: list[str] = []
    if cues and frac > MAX_REDUNDANT_FRACTION:
        problems.append(f"{redundant}/{onscreen_beats} ({frac*100:.0f}%) kinetic beats just echo the "
                        f"caption (>{MAX_REDUNDANT_FRACTION*100:.0f}% at sim>{SIM_REDUNDANT})")
    if collision:
        problems.append("kinetic on-screen text is BOTTOM-anchored, colliding with the bottom burned "
                        "captions (" + "; ".join(evidence[:3]) + ")")
    return {
        "onscreen_beats": onscreen_beats,
        "redundant_beats": redundant,
        "redundant_fraction": round(frac, 3),
        "collision": collision,
        "collision_evidence": evidence[:5],
        "cues_available": bool(cues),
        "examples": examples,
        "problems": problems,
    }


# ------------------------------------------------------------------------------------------------
# core evaluation (importable by check_final_acceptance)
# ------------------------------------------------------------------------------------------------

def evaluate(epdir: Path, *, data_dir: Optional[Path] = None,
             comp_dir: Optional[Path] = None) -> dict[str, Any]:
    """Caption-integrity gate. ``epdir`` is the episode directory (its ``.name`` is the episode id,
    e.g. ``episodes/PD-2026-036-williams``). NEVER raises, NEVER calls sys.exit.

    Returns a dict compatible with check_final_acceptance:
      {"check","ok","hard","reason", burned_present, redundant_fraction, redundant_beats,
       onscreen_beats, collision, floors, optional "skipped"}
    Missing artifacts (no beatsheet/composition — assets on SSD / not a premium comp) -> non-blocking
    skip. No burned captions, egregious echo, or a bottom collision -> {"ok": False, "hard": True}."""
    epdir = Path(epdir)
    data_dir = Path(data_dir) if data_dir is not None else DATA_DIR
    comp_dir = Path(comp_dir) if comp_dir is not None else COMP_DIR
    slug = _slug_of(epdir.name)

    bs_path = resolve_beatsheet(epdir)
    comps = resolve_compositions(comp_dir, slug, epdir.name)
    if bs_path is None and not comps:
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"no premium beatsheet or composition resolves to '{slug}' — "
                          f"not a code-driven premium episode (skipping)"}

    captions_json = resolve_captions_json(data_dir, slug)
    film_json = resolve_film_json(data_dir, slug)

    # ---- sub-check 1: burned caption presence ----
    burned = evaluate_burned_presence(comps, captions_json, film_json)

    # ---- sub-check 2: redundancy & collision ----
    beats: list[dict[str, Any]] = []
    fps = 30.0
    if bs_path is not None:
        bs = _load_json(bs_path)
        if isinstance(bs, dict):
            meta = bs.get("meta") or {}
            fps = float(meta.get("fps") or 30) or 30.0
            b = bs.get("beats")
            if isinstance(b, list):
                beats = [x for x in b if isinstance(x, dict)]
    cues, cues_src = load_caption_cues(captions_json, epdir)
    red = evaluate_redundancy(beats, cues, fps, burned["present"], comps, comp_dir, slug)

    floors = {"sim_redundant": SIM_REDUNDANT, "max_redundant_fraction": MAX_REDUNDANT_FRACTION}
    common = {
        "check": CHECK_NAME,
        "episode_id": slug,
        "composition": [str(p) for p in comps],
        "beatsheet": str(bs_path) if bs_path else None,
        "captions_source": cues_src,
        "burned_present": burned["present"],
        "burned_wiring": burned["wiring"],
        "onscreen_beats": red["onscreen_beats"],
        "redundant_beats": red["redundant_beats"],
        "redundant_fraction": red["redundant_fraction"],
        "collision": red["collision"],
        "collision_evidence": red["collision_evidence"],
        "redundancy_examples": red["examples"],
        "floors": floors,
    }

    problems: list[str] = []
    if not burned["present"]:
        problems.append(burned["reason"])
    problems.extend(red["problems"])

    if problems:
        return {**common, "ok": False, "hard": True,
                "reason": "caption integrity failed: " + "; ".join(problems)}

    # PASS — assemble an informative reason (note when redundancy could not be scored)
    red_note = (f"kinetic echo {red['redundant_beats']}/{red['onscreen_beats']} "
                f"({red['redundant_fraction']*100:.0f}%) <= {MAX_REDUNDANT_FRACTION*100:.0f}%"
                if cues else "kinetic echo unscored (no caption cues found)")
    return {**common, "ok": True, "hard": True,
            "reason": (f"caption integrity OK: burned narration captions present "
                       f"({burned['wiring']}); {red_note}; no bottom collision")}


# ------------------------------------------------------------------------------------------------
# reporting / CLI / selftest
# ------------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("CAPTION-INTEGRITY REPORT")
    print("=" * 78)
    print(f"  episode      : {r.get('episode_id')}")
    print(f"  composition  : {', '.join(Path(p).name for p in r.get('composition', [])) or '(none)'}")
    print(f"  captions src : {r.get('captions_source')}")
    print(f"  burned CAPS  : {'PRESENT' if r.get('burned_present') else 'ABSENT'}  "
          f"(wiring={r.get('burned_wiring')})")
    print(f"  kinetic echo : {r.get('redundant_beats')}/{r.get('onscreen_beats')} beats "
          f"= {r.get('redundant_fraction', 0)*100:.1f}%   "
          f"(floor {r['floors']['max_redundant_fraction']*100:.0f}% at sim>{r['floors']['sim_redundant']})")
    print(f"  collision    : {r.get('collision')}  {r.get('collision_evidence') or ''}")
    if r.get("redundancy_examples"):
        print("  echo samples :")
        for ex in r["redundancy_examples"]:
            print(f"     [{ex['sim']}] '{ex['kinetic']}'  vs  '{ex['caption']}'")
    print("-" * 78)
    print(f"  RESULT: {'PASS' if r.get('ok') else 'FAIL'}  — {r.get('reason')}")
    print("-" * 78)


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False, default=str)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


# ---- selftest fixture builders ----

def _write(p: Path, txt: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt, encoding="utf-8")


_CAPS = [
    {"start": 1.0, "end": 3.0, "text": "A blurry photo. A computer's guess."},
    {"start": 3.0, "end": 6.0, "text": "An innocent father was arrested for a crime he did not commit."},
    {"start": 6.0, "end": 9.0, "text": "The technology is already looking at your face."},
]


def _beatsheet(onscreen_pairs: list[list[str]]) -> dict[str, Any]:
    beats = []
    for i, on in enumerate(onscreen_pairs):
        beats.append({"beat": i + 1, "kind": "hero", "component": "Scene",
                      "start_frame": int((1.0 + i * 3.0) * 30), "dur_frames": 90,
                      "start_s": 1.0 + i * 3.0, "dur_s": 3.0, "onscreen": on})
    return {"meta": {"fps": 30, "projected_runtime_frames": 300}, "beats": beats}


def _comp_tsx(*, import_caps: bool, burned_tag: bool, kinetic_anchor: Optional[str],
              use_datacaptions: bool, caps_stem: str) -> str:
    lines = ["import React from 'react';",
             "import {AbsoluteFill} from 'remotion';",
             "import {KineticCaptions} from '../components/motionkit';",
             "import beatsheet from '../../../episodes/EP/04_scenes/premium_beatsheet.v001.json';"]
    if import_caps:
        lines.append(f"import caps from '../data/{caps_stem}';")
    body = []
    if kinetic_anchor is None:
        body.append("      <KineticCaptions lines={onScreen} />")  # absent -> default bottom
    else:
        body.append(f'      <KineticCaptions lines={{onScreen}} anchor="{kinetic_anchor}" />')
    if burned_tag and import_caps:
        body.append("      <BurnedCaptions cues={caps} />")
    if use_datacaptions:
        body.append("      <Captions cues={data.captions} />")
    lines += ["const BurnedCaptions = ({cues}) => <div>{cues.length}</div>;",
              "export const Film = ({onScreen, data}) => (",
              "  <AbsoluteFill>",
              *body,
              "  </AbsoluteFill>",
              ");"]
    return "\n".join(lines) + "\n"


def _make_fixture(td: Path, ep: str, *, import_caps: bool, burned_tag: bool,
                  kinetic_anchor: Optional[str], use_datacaptions: bool,
                  onscreen_pairs: list[list[str]], with_caps_json: bool) -> tuple[Path, Path, Path]:
    slug = _slug_of(ep)
    data_dir = td / "remotion" / "src" / "data"
    comp_dir = td / "remotion" / "src" / "compositions"
    epdir = td / "episodes" / ep
    caps_name = f"{slug}_captions.json"
    if with_caps_json:
        _write(data_dir / caps_name, json.dumps(_CAPS))
    _write(epdir / "04_scenes" / "premium_beatsheet.v001.json", json.dumps(_beatsheet(onscreen_pairs)))
    comp = _comp_tsx(import_caps=import_caps, burned_tag=burned_tag, kinetic_anchor=kinetic_anchor,
                     use_datacaptions=use_datacaptions, caps_stem=caps_name)
    comp = comp.replace("episodes/EP/", f"episodes/{ep}/")
    _write(comp_dir / f"{slug.capitalize()}Film.tsx", comp)
    return epdir, data_dir, comp_dir


def _run_selftest() -> int:
    """RED-A (no burned captions) MUST fail; RED-B (all-echo + bottom collision) MUST fail;
    GREEN (burned present, low echo, top anchor) MUST pass; then a real run on DEFAULT_EP."""
    results: list[tuple[str, bool]] = []
    with tempfile.TemporaryDirectory() as _td:
        td = Path(_td)

        print("=" * 78)
        print("SELFTEST RED-A: composition renders NO burned narration captions -> MUST FAIL")
        print("=" * 78)
        ep = "PD-9999-901-reda"
        epdir, dd, cd = _make_fixture(
            td, ep, import_caps=False, burned_tag=False, kinetic_anchor="top",
            use_datacaptions=False, with_caps_json=False,
            onscreen_pairs=[["A DETROIT SUBURB"], ["JANUARY 2020"], ["A NEW RULE"]])
        ra = evaluate(epdir, data_dir=dd, comp_dir=cd)
        ra_ok = (ra.get("ok") is False) and not ra.get("skipped")
        print(f"  ok={ra.get('ok')} burned_present={ra.get('burned_present')} reason: {ra.get('reason')}")
        results.append(("RED-A", ra_ok))

        print("\n" + "=" * 78)
        print("SELFTEST RED-B: burned present BUT kinetic all-echoes caption + BOTTOM collision -> MUST FAIL")
        print("=" * 78)
        ep = "PD-9999-902-redb"
        epdir, dd, cd = _make_fixture(
            td, ep, import_caps=True, burned_tag=True, kinetic_anchor=None,  # anchor absent -> bottom
            use_datacaptions=False, with_caps_json=True,
            onscreen_pairs=[["A blurry photo. A computer's guess."],
                            ["An innocent father was arrested for a crime he did not commit."],
                            ["The technology is already looking at your face."]])
        rb = evaluate(epdir, data_dir=dd, comp_dir=cd)
        rb_ok = (rb.get("ok") is False) and not rb.get("skipped")
        print(f"  ok={rb.get('ok')} burned_present={rb.get('burned_present')} "
              f"redundant_fraction={rb.get('redundant_fraction')} collision={rb.get('collision')}")
        print(f"  reason: {rb.get('reason')}")
        results.append(("RED-B", rb_ok))

        print("\n" + "=" * 78)
        print("SELFTEST GREEN: burned present, kinetic distinct from narration, TOP anchor -> MUST PASS")
        print("=" * 78)
        ep = "PD-9999-903-green"
        epdir, dd, cd = _make_fixture(
            td, ep, import_caps=True, burned_tag=True, kinetic_anchor="top",
            use_datacaptions=False, with_caps_json=True,
            onscreen_pairs=[["DETROIT, MICHIGAN"], ["16 MINUTES"], ["EVERY STATE"]])
        gr = evaluate(epdir, data_dir=dd, comp_dir=cd)
        gr_ok = (gr.get("ok") is True) and not gr.get("skipped")
        print(f"  ok={gr.get('ok')} burned_present={gr.get('burned_present')} "
              f"redundant_fraction={gr.get('redundant_fraction')} collision={gr.get('collision')}")
        print(f"  reason: {gr.get('reason')}")
        results.append(("GREEN", gr_ok))

    all_ok = all(ok for _, ok in results)
    print("\n" + "-" * 78)
    for name, ok in results:
        print(f"  {name}: {'PASS' if ok else 'FAIL'} (gate {'behaved as required' if ok else 'DID NOT behave as required'})")
    print("-" * 78)

    print("\n" + "=" * 78)
    print(f"SELFTEST REAL run on {DEFAULT_EP}")
    print("=" * 78)
    _print_report(evaluate(ROOT / "episodes" / DEFAULT_EP))
    return 0 if all_ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(
        description="Independent CAPTION-INTEGRITY gate: FAIL a render with no burned narration "
                    "captions, or whose kinetic on-screen text echoes / collides with the captions.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode id or slug (e.g. PD-2026-036-williams)")
    ap.add_argument("--dry-run", action="store_true", help="run and report, but always exit 0")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED (must fail) + GREEN (must pass) fixtures, then the real episode")
    ap.add_argument("--json", default=None, metavar="PATH", help="also write the raw result dict to PATH")
    args = ap.parse_args(argv)

    if args.selftest:
        return _run_selftest()

    epdir = ROOT / "episodes" / args.ep
    r = evaluate(epdir)
    _print_report(r)
    if args.json:
        _atomic_write_json(Path(args.json), r)
        print(f"  wrote {args.json}")
    if args.dry_run:
        return 0
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
