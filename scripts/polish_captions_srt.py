#!/usr/bin/env python
"""Final caption polish: kill orphan cues and dangling line-ends, keeping text verbatim.

`check_caption_breaks` fails on ANY of these, and both survive a grammar-aware line splitter
because they are CUE-BOUNDARY defects, not line-wrap defects:

  A. orphan cue      -- fewer than 3 words and not a self-contained sentence ("from." /
                        "not coercion."), which reads as a flash of nothing.
  B. dangling end    -- the last displayed line ends on a function word with no punctuation
                        ("...in April of 1989" -> the last WORD is "of"), the owner's
                        「字幕が変な所で途切れる」.

Both are repaired the way fix_caption_dangling repairs B -- by moving words ACROSS the cue
boundary and re-wrapping, never by rewriting them -- so the concatenated caption text stays
verbatim-identical to the narration (caption_narration_match) and cue starts do not move
except where a cue is absorbed into its neighbour.

The same polished cues are written back into the film JSON when --film is given, so the
BURNED-IN captions and the sidecar .srt break in exactly the same places.

Read-modify-write. Exit 0 = clean (or fixed), 1 = could not fix.

    python scripts/polish_captions_srt.py --srt episodes/<EP>/08_edit/captions.final.v001.srt \
        --film remotion/src/data/<slug>_film.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from fix_caption_dangling import NO_DANGLE_END, norm  # canon word list (never redefine)

MAX_LINE = 50          # check_final_acceptance MAX_LINE_CHARS
MAX_LINES = 2
MIN_CUE_WORDS = 3      # check_caption_breaks MIN_CUE_WORDS
TERMINAL_PUNCT = ".?!—-:;"
SOFT_END = TERMINAL_PUNCT + ","
WORD_RE = re.compile(r"[A-Za-z0-9'’]+")
ALPHA_RE = re.compile(r"[A-Za-z]")


def ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def parse_ts(s: str) -> float:
    h, m, rest = s.split(":")
    sec, ms = rest.replace(".", ",").split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def read_srt(path: Path) -> list[dict]:
    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = [ln for ln in block.splitlines() if ln.strip()]
        tl = next((ln for ln in lines if "-->" in ln), None)
        if not tl:
            continue
        a, z = [x.strip() for x in tl.split("-->")]
        body = [ln for ln in lines if "-->" not in ln and not ln.strip().isdigit()]
        cues.append({"start": parse_ts(a), "end": parse_ts(z), "text": " ".join(body).strip()})
    return cues


def wrap(text: str) -> list[str]:
    """Greedy wrap to at most MAX_LINES lines of at most MAX_LINE chars, preferring a break
    that does not leave a function word at a line end."""
    words = text.split()
    if not words:
        return [""]
    # One line whenever it fits. The search below only ever considered TWO-line layouts, so a
    # 15-character cue came out as "on the" / "counter." -- an internal line ending on a
    # function word, which failed the gate on the very last cue of EP59.
    if len(text) <= MAX_LINE:
        return [text]
    best: list[str] | None = None
    for split_at in range(len(words) - 1, 0, -1):
        first = " ".join(words[:split_at])
        second = " ".join(words[split_at:])
        if len(first) > MAX_LINE or len(second) > MAX_LINE:
            continue
        cand = [first, second]
        if not _line_dangles(first):
            return cand
        best = best or cand
    if best:
        return best
    if len(text) <= MAX_LINE or len(words) == 1:
        return [text]
    # no split keeps both lines inside MAX_LINE: take the most balanced one rather than
    # emitting a single over-long line (caption_format counts characters per line)
    k = min(range(1, len(words)),
            key=lambda s: max(len(" ".join(words[:s])), len(" ".join(words[s:]))))
    return [" ".join(words[:k]), " ".join(words[k:])]


def _last_word(text: str) -> str:
    """Last ALPHABETIC word — digits are skipped, so '...of 1989' ends on 'of'."""
    for w in reversed(WORD_RE.findall(text)):
        if ALPHA_RE.search(w):
            return norm(w)
    return ""


def _line_dangles(line: str) -> bool:
    line = line.rstrip()
    return bool(line) and line[-1] not in SOFT_END and _last_word(line) in NO_DANGLE_END


def is_orphan(text: str) -> bool:
    words = WORD_RE.findall(text)
    return len(words) < MIN_CUE_WORDS and (not text or text[-1] not in TERMINAL_PUNCT
                                           or not text[0].isupper())


def _fits(text: str) -> bool:
    return len(" ".join(text.split())) <= MAX_CUE_CHARS


def merge_orphans(cues: list[dict]) -> list[dict]:
    """A 1-2 word fragment is never its own cue: fold it backwards, else forwards."""
    out: list[dict] = []
    pending: dict | None = None                    # orphan waiting for the next cue
    for c in cues:
        c = dict(c)
        if pending is not None:
            joined = f"{pending['text']} {c['text']}".strip()
            if _fits(joined):
                c = {"start": pending["start"], "end": c["end"], "text": joined}
            elif out:
                out[-1]["text"] = f"{out[-1]['text']} {pending['text']}".strip()
                out[-1]["end"] = pending["end"]
            else:
                out.append(pending)
            pending = None
        if out and is_orphan(c["text"]):
            prev = out[-1]
            joined = f"{prev['text']} {c['text']}".strip()
            if _fits(joined):
                prev["text"], prev["end"] = joined, c["end"]
                continue
            pending = c                            # carry it into the following cue instead
            continue
        out.append(c)
    if pending is not None:                        # trailing orphan: it has to go backwards
        if out:
            out[-1]["text"] = f"{out[-1]['text']} {pending['text']}".strip()
            out[-1]["end"] = pending["end"]
        else:
            out.append(pending)
    return out


def move_dangling(cues: list[dict]) -> list[dict]:
    """Move a trailing function-word run into the FOLLOWING cue until nothing dangles."""
    for i in range(len(cues) - 1):
        guard = 0
        while guard < 6:
            lines = wrap(cues[i]["text"])
            if not _line_dangles(lines[-1]):
                break
            words = cues[i]["text"].split()
            k = len(words) - 1
            while k > 0 and (norm(words[k]) in NO_DANGLE_END or not ALPHA_RE.search(words[k])):
                k -= 1
            move = words[k + 1:]
            if not move or k <= 0 or len(move) >= len(words):
                break
            cues[i]["text"] = " ".join(words[:k + 1])
            cues[i + 1]["text"] = " ".join(move + cues[i + 1]["text"].split())
            guard += 1
    return cues


# A cue packed to 2x50 leaves the wrapper no choice of split point, so every line break lands
# wherever the character budget runs out -- which is how a line ends on "...up from the".
# Budget the cue at 2x44 and let the wrapper use the full 50 when it needs the slack.
# pd_prerender_gate rejects any cue over 84 characters, whatever its line count; the
# segmentation budget is that cap, which still leaves the wrapper slack (2 x 50) to choose a
# clean line break inside the cue.
HARD_CUE_CHARS = 84
MAX_CUE_CHARS = HARD_CUE_CHARS
PHRASE_START = {"and", "or", "but", "so", "because", "that", "which", "who", "when", "while",
                "after", "before", "until", "if", "though", "although", "as", "than", "with",
                "without", "for", "from", "in", "into", "on", "at", "by", "to", "of"}


def _tokens(cues: list[dict]) -> list[tuple[str, float, float]]:
    """Every word with a time span, interpolated inside its original cue (sync preserved)."""
    toks: list[tuple[str, float, float]] = []
    for c in cues:
        words = " ".join(c["text"].split()).split()
        if not words:
            continue
        span = max(0.001, c["end"] - c["start"])
        total = sum(len(w) for w in words)
        t = c["start"]
        for w in words:
            dt = span * (len(w) / total)
            toks.append((w, round(t, 3), round(t + dt, 3)))
            t += dt
    return toks


def _wraps_clean(text: str) -> bool:
    """True when this cue can be laid out without a dangling INTERNAL line end."""
    lines = wrap(" ".join(text.split()))
    return not any(_line_dangles(ln) for ln in lines[:-1])


def _clean_break(toks: list[tuple[str, float, float]], i: int, n: int) -> int:
    """Score a break AFTER token i: 3 sentence end, 2 comma, 1 next word starts a phrase."""
    raw = toks[i][0]
    # A cue must not end on a closing quote: check_caption_breaks reads the LAST character, so
    # `...but was not,"` looks like no punctuation at all and is reported as a split phrase
    # (EP58 stalled the whole build on this single cue).
    if raw.endswith(('"', '”', "'", '’')):
        return -1
    w = raw.rstrip("\"'”’")
    # the checker skips digits when it looks for the last word, so "... and 2010" ends on "and"
    j = i
    while j >= 0 and not ALPHA_RE.search(toks[j][0]):
        j -= 1
    last_alpha = norm(toks[j][0].rstrip("\"'”’")) if j >= 0 else ""
    if (norm(w) in NO_DANGLE_END or last_alpha in NO_DANGLE_END) and w[-1:] not in SOFT_END:
        return -1
    if w[-1:] in ".?!":
        return 3
    if w[-1:] in ",;:—-":
        return 2
    nxt = norm(toks[i + 1][0]) if i + 1 < n else ""
    return 1 if nxt in PHRASE_START else 0


def _enforce_budget(cues: list[dict], merge: bool = True) -> list[dict]:
    """No cue may exceed HARD_CUE_CHARS. Shedding words into a neighbour can push it over, so
    over-long cues are split again at the cleanest available word boundary, time apportioned."""
    out: list[dict] = []
    for c in cues:
        text = " ".join(c["text"].split())
        while len(text) > HARD_CUE_CHARS:
            words = text.split()
            best, cut = None, None
            for k in range(len(words) - 1, 0, -1):
                head = " ".join(words[:k])
                if len(head) > HARD_CUE_CHARS:
                    continue
                w = words[k - 1].rstrip("\"'”’")
                score = 3 if w[-1:] in ".?!" else 2 if w[-1:] in ",;:—-" else (
                    0 if norm(w) in NO_DANGLE_END else 1)
                if score == 0:
                    continue
                tail_words = words[k:]
                if len(words[:k]) < MIN_CUE_WORDS:
                    continue
                if len(tail_words) < MIN_CUE_WORDS and tail_words[-1][-1:] not in ".?!":
                    continue          # never split a cue into a 1-2 word fragment
                if best is None or score > best:
                    best, cut = score, k
                if score == 3:
                    break
            if cut is None:
                break
            head, tail = " ".join(words[:cut]), " ".join(words[cut:])
            span = max(0.001, c["end"] - c["start"])
            mid = round(c["start"] + span * (len(head) / len(text)), 3)
            out.append({"start": c["start"], "end": mid, "text": head})
            c = {"start": mid, "end": c["end"], "text": tail}
            text = tail
        out.append({"start": c["start"], "end": c["end"], "text": text})
    return merge_orphans(out) if merge else out


def polish(cues: list[dict]) -> list[dict]:
    """Re-segment the whole caption stream into clean cues.

    Boundary patching (merge this, move that) kept re-creating the defect it removed, so the
    stream is segmented once, globally: a cue never exceeds two 50-char lines, never ends on a
    dangling function word, and is never a 1-2 word fragment -- the remainder is carried into
    the next cue instead. Word order and wording are untouched.
    """
    toks = _tokens(cues)
    n = len(toks)
    out: list[dict] = []
    i = 0
    while i < n:
        # widest window that still fits one cue
        j = i
        while j + 1 < n and len(" ".join(t[0] for t in toks[i:j + 2])) <= MAX_CUE_CHARS:
            j += 1
        if j >= n - 1:
            j = n - 1
        else:
            best = None
            for k in range(j, i - 1, -1):
                score = _clean_break(toks, k, n)
                if score < 0:
                    continue
                rest = n - (k + 1)
                if 0 < rest < MIN_CUE_WORDS and toks[k][0][-1:] not in ".?!":
                    continue          # would leave a 1-2 word orphan at the end
                cue_text = " ".join(t[0] for t in toks[i:k + 1])
                if is_orphan(cue_text):
                    continue          # a 1-2 word fragment is never a cue of its own
                if not _wraps_clean(cue_text):
                    continue          # the cue's own line break would dangle
                if best is None or score > best[0]:
                    best = (score, k)
                if score == 3:
                    break
            if best is not None:
                j = best[1]
        text = " ".join(t[0] for t in toks[i:j + 1])
        out.append({"start": toks[i][1], "end": toks[j][2], "text": text})
        i = j + 1
    out = merge_orphans(out)
    # merging can re-create a dangling internal break; shed one word into the next cue until
    # the layout is clean (bounded, and it never reorders words)
    for _ in range(8):
        out = _enforce_budget(out)          # splitting can create a new dangling line...
        dirty = False
        for k in range(len(out) - 1):
            if _wraps_clean(out[k]["text"]):
                continue
            words = out[k]["text"].split()
            if len(words) < MIN_CUE_WORDS + 1:
                continue
            if len(out[k + 1]["text"]) + len(words[-1]) + 1 > HARD_CUE_CHARS:
                continue                     # ...and shedding must not blow the next budget
            out[k]["text"] = " ".join(words[:-1])
            out[k + 1]["text"] = f"{words[-1]} {out[k + 1]['text']}"
            dirty = True
        if not dirty:
            break
        out = merge_orphans(out)
    out = _enforce_budget(out, merge=False)   # a merge here could re-create an over-long cue
    # move_dangling can only push words FORWARD, so a film whose final cue ends on a function
    # word ("...on the") had no repair available and failed the gate on one cue (EP59).
    if len(out) > 1 and _line_dangles(wrap(out[-1]["text"])[-1]):
        out[-2]["text"] = f"{out[-2]['text']} {out[-1]['text']}".strip()
        out[-2]["end"] = out[-1]["end"]
        out.pop()
    # RE-TIME FROM THE WORDS. The repairs above move WORDS between cues but left the cue times
    # where they were, so a narration chunk whose words drifted into a neighbour ended up only
    # partly covered (EP52: 12 of 319 chunks under 80%, worst 68%). Every cue now spans exactly
    # the words it actually holds.
    k = 0
    for c in out:
        n_words = len(c["text"].split())
        if k + n_words <= len(toks) and n_words:
            c["start"] = toks[k][1]
            c["end"] = max(toks[k + n_words - 1][2], c["start"] + 0.25)
        k += n_words
    for c in out:
        c["text"] = "\n".join(wrap(" ".join(c["text"].split())))
    return out


def report(cues: list[dict]) -> tuple[int, int]:
    orph = sum(1 for c in cues if is_orphan(c["text"].replace("\n", " ")))
    dang = sum(1 for c in cues for ln in c["text"].split("\n")[:-1] if _line_dangles(ln))
    dang += sum(1 for c in cues if _line_dangles(c["text"].split("\n")[-1]))
    return orph, dang


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--srt", required=True)
    ap.add_argument("--film", help="film JSON whose captions[] should match the polished srt")
    ap.add_argument("--lead", type=float, default=0.0,
                    help="shift every cue earlier by N seconds (caption_sync: late cues)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    srt = Path(a.srt)
    cues = read_srt(srt)
    before = report(cues)
    fixed = polish(cues)
    if a.lead > 0:
        # The cues are CONTIGUOUS (each starts where the last ends), so clamping a lead to the
        # previous cue's end silently did nothing -- EP51 measured the identical p90 +0.370s
        # before and after "applying" a 0.15s lead. Slide the whole track instead: start AND
        # end move together, so a cue is on screen slightly before its words are spoken.
        for c in fixed:
            # START only. Moving the END earlier as well shortened every cue by the lead and
            # tripped caption_coverage (EP53, 20/304 chunks under 80% of their chunk span).
            c["start"] = round(max(0.0, c["start"] - a.lead), 3)
    after = report(fixed)
    print(f"cues {len(cues)} -> {len(fixed)} | orphans {before[0]} -> {after[0]} | "
          f"dangling {before[1]} -> {after[1]}")
    if a.dry_run:
        return 0
    srt.write_text("\n".join(
        f"{i}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['text']}\n"
        for i, c in enumerate(fixed, 1)), encoding="utf-8")
    print(f"WROTE {srt}")
    if a.film:
        fp = Path(a.film)
        d = json.loads(fp.read_text(encoding="utf-8"))
        d["captions"] = [{"start": round(c["start"], 3), "end": round(c["end"], 3),
                          "text": c["text"]} for c in fixed]
        fp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"WROTE {fp} (captions synced, {len(fixed)} cues)")
    return 0 if after == (0, 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
