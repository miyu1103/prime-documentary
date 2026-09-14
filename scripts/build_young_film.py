#!/usr/bin/env python
"""Build remotion/src/data/young_film.json for EP42 from an asset manifest."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-042-young"
SLUG = "young"
FPS = 30
DEFAULT_ASSETS = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.stub.v001.json"
DEFAULT_NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.stub.v001.json"
DEFAULT_OUT = ROOT / "remotion" / "src" / "data" / "young_film.json"
PUB_FILM = ROOT / "remotion" / "public" / "young_dryrun" / "film_data.v001.json"
BUILD_MANIFEST = ROOT / "episodes" / EP / "04_scenes" / "young_build_manifest.v001.json"
BEATSHEET = ROOT / "episodes" / EP / "04_scenes" / "young_beatsheet.v001.json"
DEFAULT_SRT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"
CAPTIONS_JSON = ROOT / "remotion" / "src" / "data" / "young_captions.v001.json"

SECTION_TARGETS = {
    "HOOK": (5, 2, 6),
    "OP": (0, 0, 7),
    "ACT_1": (14, 4, 15),
    "ACT_2": (12, 5, 13),
    "ACT_3": (28, 10, 31),
    "ACT_4": (16, 5, 16),
    "ENDING": (18, 6, 20),
}
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ENDING"]
VALID_KINDS = {"numberticker", "stat", "votetally", "timeline", "quote", "kinetic", "lowerthird", "acttitle", "compbars", "mechanism", "dochighlight", "regionmap", "pindropmap"}
NO_DANGLE_END = {"a", "an", "the", "of", "to", "in", "on", "at", "for", "from", "by", "out", "with", "and", "or", "that", "who", "which", "is", "are", "was", "were", "be", "can", "as", "her", "into", "while", "because", "its", "my", "your", "their"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def srt_ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def sentences(text: str) -> list[str]:
    protected = (
        text.replace("U.S.", "U<S>")
        .replace("v.", "v<dot>")
        .replace("Mr.", "Mr<dot>")
        .replace("Sgt.", "Sgt<dot>")
    )
    parts = [p.strip() for p in re.split(r"(?<=[.?!])\s+", protected) if p.strip()]
    return [p.replace("U<S>", "U.S.").replace("v<dot>", "v.").replace("Mr<dot>", "Mr.").replace("Sgt<dot>", "Sgt.") for p in parts]


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", text))


def wrap_lines(text: str, limit: int = 50) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur: list[str] = []
    for word in words:
        trial = " ".join([*cur, word])
        if cur and len(trial) > limit:
            lines.append(" ".join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(" ".join(cur))
    for i in range(len(lines) - 1):
        while True:
            words = lines[i].split()
            if not (words and words[-1].lower().strip("'’") in NO_DANGLE_END):
                break
            moved = words.pop()
            trial = f"{moved} {lines[i + 1]}".strip()
            if words and len(trial) <= limit:
                lines[i] = " ".join(words)
                lines[i + 1] = trial
            else:
                break
    return lines


def split_long_sentence(text: str, limit: int = 96) -> list[str]:
    if len(text) <= limit:
        return format_caption_piece(text)
    clauses = [p.strip() for p in re.split(r"(?<=[,;:—])\s+", text) if p.strip()]
    if len(clauses) <= 1:
        clauses = text.split()
    out: list[str] = []
    cur = ""
    for clause in clauses:
        trial = f"{cur} {clause}".strip()
        if cur and len(trial) > limit:
            out.append(cur)
            cur = clause
        else:
            cur = trial
    if cur:
        out.append(cur)
    formatted: list[str] = []
    for p in out:
        formatted.extend(format_caption_piece(p))
    return formatted


def format_caption_piece(text: str) -> list[str]:
    lines = wrap_lines(text)
    if len(lines) > 2:
        return [lines[0], "\n".join(wrap_lines(" ".join(lines[1:])))]
    if len(lines) == 2:
        first_words = lines[0].split()
        carry: list[str] = []
        while first_words and first_words[-1].lower().strip("'’") in NO_DANGLE_END:
            carry.insert(0, first_words.pop())
        if carry and first_words:
            second = " ".join([*carry, lines[1]])
            return [" ".join(first_words), "\n".join(wrap_lines(second))]
    return ["\n".join(lines)]


def repair_caption_pieces(pieces: list[str], limit: int = 110) -> list[str]:
    repaired: list[str] = []
    for piece in pieces:
        words = re.findall(r"[A-Za-z0-9'’]+", piece)
        combined = (repaired[-1] + " " + piece).replace("\n", " ") if repaired else ""
        wrapped = wrap_lines(combined) if combined else []
        if len(words) < 3 and repaired and len(combined) <= limit and len(wrapped) <= 2:
            repaired[-1] = "\n".join(wrapped)
        else:
            if len(words) < 3 and piece[:1].islower() and piece.rstrip().endswith((".", "?", "!", ";", ":")):
                piece = piece[:1].upper() + piece[1:]
            repaired.append(piece)
    return repaired


def split_long_duration_cues(cues: list[dict]) -> list[dict]:
    out: list[dict] = []
    for cue in cues:
        dur = float(cue["end"]) - float(cue["start"])
        lines = str(cue["text"]).split("\n")
        if dur > 7.0 and len(lines) > 1:
            total_words = max(1, sum(word_count(x) for x in lines))
            t = float(cue["start"])
            for i, line in enumerate(lines):
                z = float(cue["end"]) if i == len(lines) - 1 else t + dur * word_count(line) / total_words
                out.append({"start": round(t, 3), "end": round(z, 3), "text": line})
                t = z
        else:
            out.append(cue)
    return out


def merge_short_cues(cues: list[dict]) -> list[dict]:
    out: list[dict] = []
    for cue in cues:
        dur = float(cue["end"]) - float(cue["start"])
        if out and dur < 0.9:
            combined_text = f"{out[-1]['text']} {cue['text']}".replace("\n", " ")
            wrapped = wrap_lines(combined_text)
            combined_dur = float(cue["end"]) - float(out[-1]["start"])
            if len(wrapped) <= 2 and combined_dur <= 7.0:
                out[-1] = {**out[-1], "end": cue["end"], "text": "\n".join(wrapped)}
                continue
            prev_lines = str(out[-1]["text"]).split("\n")
            tail_text = f"{prev_lines[-1]} {cue['text']}".strip()
            tail_wrapped = wrap_lines(tail_text)
            if len(prev_lines) > 1 and len(tail_wrapped) <= 2:
                prev = out.pop()
                prev_start = float(prev["start"])
                prev_end = float(prev["end"])
                prev_dur = prev_end - prev_start
                first_text = "\n".join(prev_lines[:-1])
                first_words = max(1, word_count(first_text))
                tail_words = max(1, word_count(prev_lines[-1]))
                split_at = prev_start + prev_dur * first_words / (first_words + tail_words)
                out.append({**prev, "end": round(split_at, 3), "text": first_text})
                out.append({"start": round(split_at, 3), "end": cue["end"], "text": "\n".join(tail_wrapped)})
                continue
        out.append(cue)
    return out


def build_captions(narr: dict) -> tuple[list[dict], float]:
    cues: list[dict] = []
    for c in narr["chunks"]:
        text = str(c.get("text") or c.get("spoken_text") or "").strip()
        if not text:
            continue
        pieces: list[str] = []
        for sentence in sentences(text) or [text]:
            pieces.extend(split_long_sentence(sentence))
        pieces = repair_caption_pieces(pieces)
        total_words = max(1, sum(word_count(p) for p in pieces))
        start = float(c["start"])
        end = float(c["end"])
        span = max(0.9, end - start)
        t = start
        for i, piece in enumerate(pieces):
            if i == len(pieces) - 1:
                z = end
            else:
                z = t + span * word_count(piece) / total_words
            cues.append({"start": round(t, 3), "end": round(z, 3), "text": piece})
            t = z
    cues = merge_short_cues(split_long_duration_cues(cues))
    return cues, max(c["end"] for c in cues)


def write_srt(cues: list[dict], out: Path) -> None:
    lines = []
    for i, c in enumerate(cues, 1):
        lines += [str(i), f"{srt_ts(c['start'])} --> {srt_ts(c['end'])}", *str(c["text"]).split("\n"), ""]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def section_windows(narr: dict, total: float) -> dict[str, tuple[float, float]]:
    starts = {}
    ends = {}
    for c in narr["chunks"]:
        sec = c["section"]
        starts.setdefault(sec, float(c["start"]))
        ends[sec] = max(float(c["end"]), ends.get(sec, 0.0))
    windows = {}
    for i, sec in enumerate(SECTION_ORDER):
        if sec not in starts:
            continue
        nxt = next((s for s in SECTION_ORDER[i + 1:] if s in starts), None)
        windows[sec] = (starts[sec], starts[nxt] if nxt else total)
    return windows


def public_items(manifest: dict, key: str, role: str | None = None) -> list[str]:
    items = manifest.get(key) or []
    if role:
        items = [x for x in items if x.get("role") == role]
    out = [str(x["public_path"]) for x in items if x.get("public_path")]
    if len(out) != len(set(out)):
        raise SystemExit(f"duplicate public_path in {key}")
    return out


def take(q: deque[str], n: int, label: str) -> list[str]:
    if len(q) < n:
        raise SystemExit(f"not enough {label}: need {n}, have {len(q)}")
    return [q.popleft() for _ in range(n)]


def repeated(pool: list[str], n: int, cap: int) -> list[str]:
    out = []
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
        raise SystemExit(f"unable to allocate {n} assets with cap {cap}")
    return out


def make_cuts(windows: dict[str, tuple[float, float]], manifest: dict) -> list[dict]:
    stills = public_items(manifest, "stills", "body")
    factory_q = deque(public_items(manifest, "factory"))
    motion_pool = public_items(manifest, "motion")
    still_need = sum(ns for nf, nm, ns in SECTION_TARGETS.values())
    motion_need = sum(nm for nf, nm, ns in SECTION_TARGETS.values())
    still_pool = repeated(stills, still_need, 2)
    motion_items = repeated(motion_pool, motion_need, 2)
    still_q = deque(still_pool)
    motion_q = deque(motion_items)
    cuts = []
    treatments = ["depth", "scan", "duotone", "focus"]
    treat_i = 0
    for sec in SECTION_ORDER:
        if sec not in windows:
            continue
        nf, nm, ns = SECTION_TARGETS[sec]
        if nf + nm + ns == 0:
            continue
        s, e = windows[sec]
        seq = []
        fac = take(factory_q, nf, "factory")
        mot = take(motion_q, nm, "motion")
        sti = take(still_q, ns, "still")
        fi = mi = si = 0
        pattern = ["F", "S", "M", "F", "S", "F"]
        while fi < len(fac) or mi < len(mot) or si < len(sti):
            slot = pattern[(len(seq)) % len(pattern)]
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
        weights = [3.0 if kind == "img" else 3.343 for kind, _ in seq]
        scale = (e - s) / sum(weights)
        t = s
        for kind, src in seq:
            raw = 3.0 if kind == "img" else 3.343
            dur = round(raw * scale, 3)
            cut = {"id": f"cut-{len(cuts):03d}", "start": round(t, 3), "dur": dur, "kind": kind, "src": src, "seed": f"young-{len(cuts):03d}", "act": sec}
            if kind == "img":
                cut["treatment"] = treatments[treat_i % len(treatments)]
                treat_i += 1
            else:
                cut["treatment"] = "footage"
            cuts.append(cut)
            t += dur
        if cuts:
            cuts[-1]["dur"] = round(e - cuts[-1]["start"], 3)
    return cuts


def make_hook(manifest: dict) -> list[dict]:
    stills = public_items(manifest, "stills", "body")
    picks = stills[:6]
    dur = round(8.0 / len(picks), 3)
    hook = []
    t = 0.0
    for i, src in enumerate(picks):
        d = round(8.0 - t, 3) if i == len(picks) - 1 else dur
        hook.append({"start": round(t, 3), "dur": d, "kind": "img", "src": src, "seed": f"young-hook-{i:02d}"})
        t += d
    return hook


def K(lines, emph=None, style="maskslide"):
    d = {"kind": "kinetic", "lines": lines, "style": style}
    if emph:
        d["emphasisWords"] = emph
    return d


def figure_payloads() -> list[dict]:
    return [
        K(["THE WRONG HOUSE"], ["WRONG"], "emphasis"),
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction"},
        {"kind": "mechanism", "mechanism": "closingdoor"},
        {"kind": "acttitle", "title": "THE WRONG DOOR", "kicker": "ACT ONE", "index": 1},
        {"kind": "stat", "value": 12, "label": "about twelve officers"},
        {"kind": "lowerthird", "primary": "a search warrant, signed by a judge"},
        K(["THE WRONG HOUSE"], ["WRONG"], "wordpop"),
        {"kind": "mechanism", "mechanism": "closingdoor"},
        {"kind": "timeline", "events": [{"year": "Feb 2019", "text": "wrong address"}]},
        {"kind": "acttitle", "title": "THE TAPE", "kicker": "ACT TWO", "index": 2},
        {"kind": "timeline", "events": [{"year": "Dec 2020", "text": "footage airs"}]},
        {"kind": "numberticker", "value": 16, "suffix": " months", "label": "COPA"},
        {"kind": "numberticker", "value": 100, "suffix": " alleged", "label": "oversight flags"},
        K(["ALLEGED", "NOT PROVEN"], ["ALLEGED"], "emphasis"),
        {"kind": "lowerthird", "primary": "police-oversight investigation"},
        {"kind": "acttitle", "title": "THE COMMAND", "kicker": "ACT THREE", "index": 3},
        {"kind": "timeline", "events": [{"year": "Aug 1998", "text": "entry"}, {"year": "Jun 2006", "text": "decision"}]},
        {"kind": "numberticker", "value": 5, "suffix": " seconds", "label": "three to five"},
        {"kind": "votetally", "majority": 5, "dissent": 4, "label": "Supreme Court 2006"},
        {"kind": "quote", "quote": "still a command", "attribution": "Justice Scalia, for the majority"},
        {"kind": "stat", "value": 4, "label": "Part IV - Kennedy did not join"},
        K(["STILL A COMMAND"], ["COMMAND"], "emphasis"),
        {"kind": "lowerthird", "primary": "SECTION 1983", "secondary": "the civil remedy"},
        {"kind": "mechanism", "mechanism": "gears"},
        {"kind": "mechanism", "mechanism": "faultsplit"},
        {"kind": "acttitle", "title": "THE REACH", "kicker": "ACT FOUR", "index": 4},
        {"kind": "stat", "value": 2.9, "prefix": "$", "suffix": "M", "decimals": 1, "label": "reported - no finding of fault"},
        K(["A SETTLEMENT", "NOT A FINDING"], ["NOT"], "emphasis"),
        {"kind": "numberticker", "value": 10, "suffix": "-4", "label": "voted down"},
        {"kind": "stat", "value": 5, "suffix": "-3", "label": "Police Board - Wolinski"},
        K(["STILL LEGAL"], ["LEGAL"], "wordpop"),
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction"},
        K(["IT WAS", "YOUR DOOR"], ["YOUR"], "emphasis"),
        {"kind": "mechanism", "mechanism": "closingdoor"},
    ]


def place_figures(windows: dict[str, tuple[float, float]], total: float) -> list[dict]:
    section_counts = [("HOOK", 3), ("ACT_1", 7), ("ACT_2", 6), ("ACT_3", 11), ("ACT_4", 6), ("ENDING", 4)]
    payloads = deque(figure_payloads())
    figures = []
    dur = 5.4
    for sec, count in section_counts:
        s, e = windows[sec]
        lo = s + (4.0 if sec == "HOOK" else 3.0)
        hi = e - 7.0
        if sec == "ENDING":
            hi = min(hi, total - 12.5)
        span = max(dur + 0.5, hi - lo)
        for i in range(count):
            start = lo + (span * (i + 0.5) / count) - dur / 2
            payload = payloads.popleft()
            if payload["kind"] not in VALID_KINDS:
                raise SystemExit(f"invalid figure kind {payload['kind']}")
            figures.append({"start": round(start, 3), "end": round(start + dur, 3), **payload})
    figures.sort(key=lambda x: x["start"])
    return figures


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    ap.add_argument("--narr", type=Path, default=DEFAULT_NARR)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--captions", type=Path, default=DEFAULT_SRT)
    args = ap.parse_args()
    manifest = load_json(args.assets)
    narr = load_json(args.narr)
    captions, total = build_captions(narr)
    windows = section_windows(narr, total)
    cuts = make_cuts(windows, manifest)
    hook = make_hook(manifest)
    figures = place_figures(windows, total)
    write_srt(captions, args.captions)
    CAPTIONS_JSON.write_text(json.dumps(captions, ensure_ascii=False, indent=2), encoding="utf-8")
    film = {
        "episode_id": EP,
        "fps": FPS,
        "narration": "young_dryrun/audio/silence.m4a",
        "narrationSeconds": round(total, 3),
        "hookSeconds": 8.0,
        "hookLine": "You have the wrong house.",
        "hook": hook,
        "cuts": cuts,
        "captions": captions,
        "graphics": [],
        "figures": figures,
        "overlays": [x["public_path"] for x in manifest.get("overlay", []) if x.get("public_path")],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")
    PUB_FILM.parent.mkdir(parents=True, exist_ok=True)
    PUB_FILM.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")

    uses = Counter(c["src"] for c in cuts)
    still_time = sum(c["dur"] for c in cuts if c["kind"] == "img")
    motion_time = sum(c["dur"] for c in cuts if c["kind"] != "img")
    report = {
        "cuts": len(cuts),
        "factory": sum(1 for c in cuts if "/factory/" in c["src"].replace("\\", "/")),
        "motion": sum(1 for c in cuts if "/motion/" in c["src"].replace("\\", "/")),
        "stills": sum(1 for c in cuts if c["kind"] == "img"),
        "distinct_assets": len(uses),
        "first_use_share": round(len(uses) / len(cuts), 4),
        "still_time_share": round(still_time / total, 4),
        "motion_time_share": round(motion_time / total, 4),
        "figures": len(figures),
    }
    BUILD_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    BUILD_MANIFEST.write_text(json.dumps({"episode_id": EP, "producer": "scripts/build_young_film.py", "inputs": {"assets": str(args.assets), "narr": str(args.narr)}, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    BEATSHEET.write_text(json.dumps({"schema_version": "young_beatsheet.v1", "episode_id": EP, "figures": figures, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())