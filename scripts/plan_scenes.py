#!/usr/bin/env python
"""U1 - Shotlist generator: annotated script -> per-span sourcing/keyword sheet.

Read-only, deterministic, NO network. Derives, for every span of the verified annotated
script, a shot row with: estimated seconds, suggested asset source, a MOTION treatment
(so nothing is left static / 'shoboi'), search keywords (feed for free-stock search in U2),
on-screen text (telop), priority and a rights note. AI images (Codex/SDXL) are first-class
and may be used liberally; stock VIDEO is preferred where real motion reads more authentically.

Output: episodes/<ep>/04_scenes/shotlist.v001.json (validated against schemas/shotlist.schema.json).
Default is a dry-run summary; pass --write to persist (atomic). This is a sourcing aid for
humans/Codex, NOT an approval artifact and NOT a state transition.

Usage:
    .venv/Scripts/python.exe scripts/plan_scenes.py 11           # dry-run summary
    .venv/Scripts/python.exe scripts/plan_scenes.py 11 --write   # write the shotlist
    .venv/Scripts/python.exe scripts/plan_scenes.py PD-2026-011-mahanoy --write
"""
from __future__ import annotations
import sys, os, json, re, glob, hashlib, tempfile
from typing import Any
from jsonschema import Draft202012Validator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPDIR = os.path.join(ROOT, "episodes")
WPM = 150  # words-per-minute narration pace (matches validate_episode.py)

# Production-jargon tokens: if a visual_intent phrase contains one, it is a note, not a subject.
_JARGON = ("symbolic", "rights-clean", "rights clean", "ai-disclosed", "ai disclosed", "disclosed",
           "no real", "no face", "no-face", "motif", "remotion", "verbatim", "stock", "placeholder",
           "censor", "blur", "no readable", "no brand", "non-branded", "generic icons")
# Shot-content hint sets (lowercased substring match on visual_intent).
_GRAPHIC = ("graph", "timeline", "diagram", "data", "map", "scale", "citation", "u.s. ", "u. s.",
            "verdict board", "count-by-count", "chart", "bracket", "lower third", "5-4", "5–4",
            "8-1", "8–1", "9-0", "9–0", "$9b", "$0", "network diagram", "animation")
_ARCHIVAL = ("portrait", "constitution", "archival", "official portrait", "1960s", "1963", "1967",
             "fingerprint", "parchment", "bill of rights")
_REAL = ("officer", "police", "patrol", "car", "phone", "smartphone", "garage", "door", "courthouse",
         "courtroom", "crowd", "blood", "swab", "cheek", "lab", "hands", "hand", "street", "store",
         "convenience", "contract", "sign", "office", "building", "city", "night", "booking", "pharmacy",
         "drugstore", "vial", "needle", "drop of blood", "tap", "tapping", "scrolling", "screen")
_HERO = ("cold open", "hook", "montage", "cover", "magazine", "dramatic", "fortress", "surreal", "halo")


def resolve(arg: str) -> str:
    if os.path.isdir(os.path.join(EPDIR, arg)):
        return arg
    hits = [os.path.basename(p) for p in glob.glob(os.path.join(EPDIR, f"PD-*-{int(arg):03d}-*"))] \
        if arg.isdigit() else []
    if not hits:
        hits = [os.path.basename(p) for p in glob.glob(os.path.join(EPDIR, f"*{arg}*")) if os.path.isdir(p)]
    if len(hits) == 1:
        return hits[0]
    raise SystemExit(f"Could not resolve episode '{arg}'. Matches: {hits}")


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z']+", text or ""))


def keywords_from_intent(visual_intent: str) -> list[str]:
    """Turn a free-text visual_intent into a few clean stock-search phrases (deterministic)."""
    if not visual_intent:
        return []
    s = re.sub(r"\([^)]*\)", " ", visual_intent)          # drop parenthetical production notes
    s = s.replace("—", ";").replace(" - ", ";")       # em-dash / dash -> phrase break
    out: list[str] = []
    for chunk in re.split(r"[;,.]", s):
        phrase = chunk.strip().strip("\"'").strip()
        if not phrase:
            continue
        low = phrase.lower()
        if any(j in low for j in _JARGON):                 # a production note, not a subject
            continue
        phrase = re.sub(r"^(a |an |the )", "", phrase, flags=re.I).strip("\"' ")
        phrase = re.sub(r"\s+", " ", phrase)
        if not phrase:
            continue
        words = phrase.split(" ")
        if len(words) > 7:
            phrase = " ".join(words[:7])
        if phrase.lower() not in [o.lower() for o in out]:
            out.append(phrase)
        if len(out) >= 6:
            break
    return out


_CITATION = re.compile(r"\bU\.?\s?S\.?\b|\d+\s?[-–]\s?\d+|§|\bv\.\b|\b(19|20)\d{2}\b")


def classify(visual_intent: str, narrative_function: str, on_screen_text: list[str]) -> tuple[str, str]:
    """Return (suggested_asset_type, motion). Images are NEVER static.

    AI images (Codex/SDXL) are first-class and the default B-roll so the video never collapses
    into static typography ('shoboi'). Only inherently graphic beats (citations, votes, data,
    timelines, maps) become motion_graphic; real, filmable scenes prefer stock video.
    """
    vi = (visual_intent or "").lower()
    nf = (narrative_function or "").lower()
    if not visual_intent:
        # No director hint: a citation/vote telop -> animated graphic; otherwise an AI B-roll image.
        if any(_CITATION.search(t or "") for t in (on_screen_text or [])):
            return "motion_graphic", "graphic_anim"
        return "ai_image", "ken_burns"
    if any(h in vi for h in _GRAPHIC):
        return "motion_graphic", "graphic_anim"
    if any(h in vi for h in _ARCHIVAL):
        return "archival_pd", "ken_burns"
    if any(h in vi for h in _REAL):
        return "stock_video", "video_native"              # prefer real motion for real scenes
    if "hook_cold_open" in nf or any(h in vi for h in _HERO):
        return "ai_image", "parallax"                     # showpiece AI image, made to move
    return "ai_image", "ken_burns"                          # AI images are fine as default B-roll


def priority_for(narrative_function: str, has_visual: bool) -> str:
    nf = (narrative_function or "").lower()
    if any(k in nf for k in ("hook", "ruling", "event_turn", "reveal", "thesis", "next_episode", "reveal")):
        return "A"
    return "B" if has_visual else "C"


def rights_note_for(asset_type: str) -> str:
    if asset_type == "ai_image":
        return "AI image (Codex/SDXL) - use freely; no real-person likeness (inv.11); AI-disclosed; always apply motion (never static)."
    if asset_type in ("stock_video", "stock_image"):
        return "Commercial-use only; log source/author/license/date/scene/sha256; no unauthorized sources; ambiguous rights -> review, do not auto-place."
    if asset_type == "archival_pd":
        return "Public-domain / CC0 only; verify and attribute."
    return "Coded in Remotion; no external rights."


def build(ann: dict[str, Any]) -> dict[str, Any]:
    span_to_chapter: dict[str, str] = {}
    for ch in ann.get("chapters", []):
        for sid in ch.get("span_ids", []):
            span_to_chapter[sid] = ch["chapter_id"]
    shots = []
    by_type: dict[str, int] = {}
    total_sec = 0.0
    ai_seq = 0
    for sp in ann["spans"]:
        vi = sp.get("visual_intent", "")
        nf = sp.get("narrative_function", "")
        secs = round(word_count(sp.get("text", "")) / WPM * 60.0, 1)
        total_sec += secs
        atype, motion = classify(vi, nf, sp.get("on_screen_text", []))
        if atype == "ai_image":                 # weave in real footage (~1/3) so it's not all stills
            ai_seq += 1
            if ai_seq % 3 == 0:
                atype, motion = "stock_video", "video_native"
        by_type[atype] = by_type.get(atype, 0) + 1
        shot: dict[str, Any] = {
            "span_id": sp["span_id"],
            "chapter_id": span_to_chapter.get(sp["span_id"]),
            "narrative_function": nf or "unspecified",
            "estimated_seconds": secs,
            "suggested_asset_type": atype,
            "motion": motion,
            "priority": priority_for(nf, bool(vi)),
            "search_keywords": keywords_from_intent(vi),
            "on_screen_text": sp.get("on_screen_text", []),
            "rights_note": rights_note_for(atype),
        }
        if vi:
            shot["visual_intent"] = vi
        shots.append(shot)
    return {
        "shots": shots,
        "totals": {
            "shot_count": len(shots),
            "estimated_total_seconds": round(total_sec, 1),
            "by_asset_type": by_type,
        },
    }


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--write" in sys.argv[1:]
    if not args:
        raise SystemExit("usage: plan_scenes.py <episode-number-or-id> [--write]")
    ep = resolve(args[0])
    b = os.path.join(EPDIR, ep)
    ann_path = os.path.join(b, "03_script", "script.annotated.v001.json")
    if not os.path.exists(ann_path):
        raise SystemExit(f"missing annotated script: {ann_path}")
    raw = open(ann_path, "rb").read()
    ann = json.loads(raw)
    body = build(ann)
    doc = {
        "schema_version": "1.0.0",
        "episode_id": ann["episode_id"],
        "revision": "v001",
        "generated_from": "03_script/script.annotated.v001.json",
        "source_annotated_sha256": "sha256:" + hashlib.sha256(raw).hexdigest(),
        **body,
    }
    schema = json.load(open(os.path.join(ROOT, "schemas", "shotlist.schema.json"), encoding="utf-8"))
    errs = [f"{list(e.path)} {e.message}" for e in Draft202012Validator(schema).iter_errors(doc)]
    if errs:
        print("SCHEMA ERRORS:")
        for e in errs:
            print("  ", e)
        return 1

    t = doc["totals"]
    print(f"Episode: {ep}")
    print(f"Shots: {t['shot_count']}   est. total: {t['estimated_total_seconds']/60:.1f} min")
    print(f"By source: {t['by_asset_type']}")
    pri = {p: sum(1 for s in doc['shots'] if s['priority'] == p) for p in ('A', 'B', 'C')}
    print(f"Priority:  A={pri['A']} B={pri['B']} C={pri['C']}")
    print("\nFirst shots (span | source | motion | ~sec | keywords):")
    for s in doc["shots"][:6]:
        kw = "; ".join(s["search_keywords"][:3]) or "(motion-graphic / telop)"
        print(f"  {s['span_id']} | {s['suggested_asset_type']:<13} | {s['motion']:<12} | {s['estimated_seconds']:>4}s | {kw}")

    out = os.path.join(b, "04_scenes", "shotlist.v001.json")
    if write:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(out), suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        os.replace(tmp, out)
        print(f"\nWROTE {os.path.relpath(out, ROOT)}")
    else:
        print(f"\n(dry-run) would write {os.path.relpath(out, ROOT)} - pass --write to persist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
