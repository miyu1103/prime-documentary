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
import statistics
import sys
from datetime import datetime, timezone
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
# A cue may not stay on screen longer than this. check_final_acceptance.MAX_CUE_SECONDS is a
# HARD 7.0 s and EP65 marmet failed acceptance on ONE 7.8 s cue -- produced here, not by the
# aligner: this file re-segments from word tokens and takes the WIDEST window that fits the
# character budget, so two short sentences separated by a designed hold or a section gap fold
# into a single cue whose span covers the silence between them. Nothing in this file measured
# time until now. 6.8 s leaves 0.2 s of margin under the gate. It can only ever make a cue
# SHORTER, so it cannot introduce a violation of any other caption rule: a 2x50 cue is at most
# 100 characters, and 100 / 6.8 = 14.7 cps, far under the 27 cps ceiling.
MAX_CUE_SECONDS = 6.8
GATE_CUE_SECONDS = 7.0        # the hard ceiling itself, used only by the final safety trim
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
    # Use this file's own _last_word -- the SAME extraction check_caption_breaks._last_word
    # performs -- rather than normalising the whole token. On "901(a)(2)" the whole-token form
    # normalises to "901a2", which is not a function word, while both gates read the last
    # alphabetic run "a", which IS one: the repairer allowed a break the gate then failed on
    # (EP66 cue 322, "...Sections 303(c) and 901(a)(2)" | "of the Code violate..."). This makes
    # the repairer STRICTER in exactly the direction the gate measures, so it can only ever
    # remove a failure, never create one.
    last_alpha = _last_word(toks[j][0]) if j >= 0 else ""
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
        while (j + 1 < n
               and len(" ".join(t[0] for t in toks[i:j + 2])) <= MAX_CUE_CHARS
               # ...and the cue must not outlast MAX_CUE_SECONDS on screen. Without this the
               # window is widened on characters alone and happily swallows a 4-5 s designed
               # hold (EP66) or a 1.8 s section gap, which is how a 74-character cue ends up
               # 8.6 s long and fails check_caption_format.
               and toks[j + 1][2] - toks[i][1] <= MAX_CUE_SECONDS):
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
    # FINAL SAFETY. Nothing leaves this function longer than the gate allows. The window bound
    # in the segmenter prevents nearly all of it, but merge_orphans may still fold a 1-2 word
    # fragment across a designed hold -- and an orphan cue is a hard gate failure too, so the
    # merge is kept and the cue END is trimmed instead. Trimming an end never moves a start:
    # audio sync and the 0.60 s caption lead are untouched, the caption just leaves earlier.
    for c in out:
        if c["end"] - c["start"] > GATE_CUE_SECONDS:
            c["end"] = round(c["start"] + MAX_CUE_SECONDS, 3)
    for c in out:
        c["text"] = "\n".join(wrap(" ".join(c["text"].split())))
    return out


GATE_CPS = 27.0        # check_final_acceptance MAX_CPS -- the hard reading-speed ceiling
CPS_MARGIN = 0.94      # aim under the gate so millisecond rounding cannot land back on it
MIN_CUE_SECONDS = 0.8  # gen_captions_forced MIN_CUE_SECONDS; no cue may flash
RUN_TOUCH_SECONDS = 0.35   # cues closer together than this are one contiguous run of speech


def _chars(c: dict) -> int:
    return sum(len(ln) for ln in c["text"].split("\n"))


def rebalance_cps(cues: list[dict]) -> tuple[list[dict], int, int]:
    """C. impossible reading speed -- give a starved cue its time back from inside its own run.

    `check_final_acceptance.check_caption_format` hard-fails a cue whose chars/second exceeds
    MAX_CPS 27.0. EP67 delivered four of them: 28, 34, 68 and 123 cps, the last being 69
    characters in 0.562 s, which is not a speed any narrator produced. It is a forced-alignment
    artefact -- whisper front-loads a long spelled-out number ("three thousand, nine hundred and
    thirty-six dollars and eighty-eight cents") onto the words it is confident about and leaves
    the tail almost no window, while the neighbouring cue inside the SAME narration chunk sits
    at 8-11 cps with seconds to spare.

    The repair takes the time from where it actually is. Around each violating cue this grows
    the SHORTEST run of touching cues whose aggregate rate clears the gate, then re-divides that
    run's own span in proportion to characters. Therefore:
      * the run's first start and last end do not move -- nothing outside the run changes, the
        0.60 s lead on the run's opening cue is preserved, and total coverage is identical;
      * no text is rewritten, re-wrapped, or moved between cues, so caption_narration_match
        cannot change (it compares tokens only);
      * cues stay ordered, non-overlapping and inside MAX_CUE_SECONDS.
    A cue already under the gate is never touched, so a file with no violation comes out
    byte-identical -- verified against the shipped srts of EP62-EP66.
    """
    n = len(cues)
    out = [dict(c) for c in cues]
    fixed = unfixable = 0
    i = 0
    while i < n:
        d = out[i]["end"] - out[i]["start"]
        ch = _chars(out[i])
        if d > 0 and ch / d <= GATE_CPS:
            i += 1
            continue
        lo = hi = i
        ok = False
        # Grow outward one touching cue at a time and stop the moment the whole run can be read
        # at the gate rate. The smallest run wins, so a local artefact stays local.
        while True:
            span = out[hi]["end"] - out[lo]["start"]
            total = sum(_chars(c) for c in out[lo:hi + 1])
            if span > 0 and total / span <= GATE_CPS * CPS_MARGIN:
                ok = True
                break
            grew = False
            if lo > 0 and out[lo]["start"] - out[lo - 1]["end"] <= RUN_TOUCH_SECONDS:
                lo -= 1
                grew = True
            if hi + 1 < n and out[hi + 1]["start"] - out[hi]["end"] <= RUN_TOUCH_SECONDS:
                hi += 1
                grew = True
            if not grew:
                break
        if not ok:
            unfixable += 1
            i += 1
            continue
        s, e = out[lo]["start"], out[hi]["end"]
        span = e - s
        k = hi - lo + 1
        chars = [_chars(c) for c in out[lo:hi + 1]]
        total = sum(chars)
        floor = min(MIN_CUE_SECONDS, span / k)   # a run too short for the floor shares evenly
        spare = span - floor * k
        cur = s
        for j, ch_j in enumerate(chars):
            width = min(floor + (spare * ch_j / total if total else spare / k), MAX_CUE_SECONDS)
            c = out[lo + j]
            c["start"] = round(cur, 3)
            cur = min(cur + width, e)
            c["end"] = round(cur, 3)
        out[hi]["end"] = round(e, 3)
        fixed += k
        i = hi + 1
    return out, fixed, unfixable


def cps_violations(cues: list[dict]) -> list[tuple[int, float]]:
    """Indices and rates of every cue over the hard gate. Measurement, not repair."""
    bad: list[tuple[int, float]] = []
    for i, c in enumerate(cues):
        d = c["end"] - c["start"]
        if d <= 0 or _chars(c) / d > GATE_CPS:
            bad.append((i, _chars(c) / d if d > 0 else float("inf")))
    return bad


def report(cues: list[dict]) -> tuple[int, int]:
    orph = sum(1 for c in cues if is_orphan(c["text"].replace("\n", " ")))
    dang = sum(1 for c in cues for ln in c["text"].split("\n")[:-1] if _line_dangles(ln))
    dang += sum(1 for c in cues if _line_dangles(c["text"].split("\n")[-1]))
    return orph, dang


# ------------------------------------------------------------------ lead measurement
# THE LEAD IS MEASURED OUT OF THE FILE. IT IS NEVER TRUSTED FROM A SIDECAR.
#
# captions.final.vNNN.lead.json is written HERE and read by nothing else, while
# build_case_film_generic.write_srt REGENERATES the entire srt from narration_index.v001.json at
# raw chunk timings on every film build and never touches that sidecar. _finish_episode.sh runs
# the builder at step [4/7] and this polish at step [4b], in that order -- so after any film
# rebuild the lead actually present in the srt is 0.0 while the sidecar still claims whatever it
# last claimed. A hand-patched sidecar is correct for exactly one run and wrong after the next
# build.
#
# Measured 2026-08-11 over the eight queued episodes: five sidecars disagreed with their own srt,
# in BOTH directions -- greene claimed 0.25 with 0.0 in the file, correa 0.25 / 0.0, openfields
# 0.6 / 0.0, hyatt 0.0 / 0.6. Captions are burned into the render; they cannot be fixed after it.
#
# So the lead is read out of the srt itself: for every narration chunk whose first word also
# opens a cue, chunk start minus that cue start; the median of those pairs is the lead. The
# sidecar is still written -- as a RECORD of what was measured. An output, never an input.
LEAD_TOL = 0.05                  # a pair agrees with the median within this many seconds
MIN_LEAD_MATCHES = 8             # ...and there must be at least this many pairs
MIN_LEAD_MATCH_FRACTION = 0.25   # ...covering at least this share of the narration chunks
MIN_LEAD_AGREE_FRACTION = 0.60   # ...of which at least this share agree with the median


def narration_index_for(srt: Path) -> Path | None:
    """<ep>/08_edit/captions.final.vNNN.srt -> <ep>/06_audio/narration_index.v*.json, latest."""
    found = sorted((srt.parent.parent / "06_audio").glob("narration_index.v*.json"))
    return found[-1] if found else None


def _lead_words(text: str) -> list[str]:
    """The comparable word stream, with authoring markers removed from BOTH sides.

    EP77 keybridge writes its claim links inline in the script -- "...an order to stop the
    traffic. <!-- KB-113 -->" -- and 103 of its narration chunks carry one. Those markers were
    stripped out of the captions on 2026-08-27 so they could not be burned into the picture,
    but they are still in the narration index, which is the record of what was written rather
    than of what was spoken. Comparing the two streams then measured 5,030 narration words
    against 4,768 cue words, matched 1 chunk of 358, and reported "this srt does not belong to
    this narration index" -- which was false. The srt belonged to it; one side had been cleaned
    and the other had not, and the difference is exactly the 262 words of marker text.

    Normalising here rather than editing the index is deliberate: the index is bound to the
    audio and to per-chunk sha sidecars, and a marker is authoring metadata that was never
    spoken. Episodes with no markers are unaffected -- the regex finds nothing to remove.
    """
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    return [w.lower() for w in WORD_RE.findall(text)]


def measure_lead(cues: list[dict], narr: dict) -> tuple[float | None, dict]:
    """How much lead is ALREADY baked into these cues, measured against the narration index.

    Returns (lead, diagnostics). `lead` is None when it cannot be measured honestly, which is a
    real defect and never a reason to substitute a constant: it means this srt does not belong to
    this narration index. EP67 ramirez was exactly that on 2026-08-11 -- its v001 srt was written
    before the script was extended, so it carries 4,070 of the narration index's 4,518 words and
    ends 152.8 s early. A naive median over text-matched pairs calls that a 50.2 s "lead", and
    applying it would drag every caption fifty seconds out of sync with the voice.

    Two guards separate a lead from a structural offset:
      * enough of the narration must line up (MIN_LEAD_MATCHES / MIN_LEAD_MATCH_FRACTION), and
      * the offset must be CONSTANT (MIN_LEAD_AGREE_FRACTION within LEAD_TOL of the median).
    A stale revision fails the first, because the word streams diverge after the first insertion;
    a drifting alignment fails the second, because its offsets form a staircase, not a line.
    """
    cue_words: list[str] = []
    opens: dict[int, int] = {}          # word index in the stream -> the cue that starts there
    for i, c in enumerate(cues):
        opens.setdefault(len(cue_words), i)
        cue_words.extend(_lead_words(c["text"].replace("\n", " ")))
    narr_words: list[str] = []
    deltas: list[float] = []
    chunks = 0
    for ch in narr.get("chunks", []):
        words = _lead_words(str(ch.get("text") or ch.get("spoken_text") or ""))
        if not words:
            continue
        chunks += 1
        pos = len(narr_words)
        narr_words.extend(words)
        i = opens.get(pos)
        if i is None:
            continue                    # this chunk starts mid-cue: nothing to compare it to
        k = min(4, len(words))
        if cue_words[pos:pos + k] != words[:k]:
            continue                    # the two word streams have drifted apart by here
        deltas.append(round(float(ch["start"]) - cues[i]["start"], 3))
    diag: dict = {"narration_chunks": chunks, "narration_words": len(narr_words),
                  "cue_words": len(cue_words), "matched_pairs": len(deltas),
                  "streams_identical": cue_words == narr_words}
    if not deltas:
        diag["reason"] = ("not one narration chunk opens a cue -- this srt does not belong to "
                          "this narration index")
        return None, diag
    med = round(statistics.median(deltas), 3)
    agree = sum(1 for d in deltas if abs(d - med) <= LEAD_TOL)
    diag.update({"median": med, "agree": agree,
                 "agree_fraction": round(agree / len(deltas), 3),
                 "min": min(deltas), "max": max(deltas)})
    if len(deltas) < max(MIN_LEAD_MATCHES, MIN_LEAD_MATCH_FRACTION * chunks):
        diag["reason"] = (f"only {len(deltas)} of {chunks} narration chunks line up with a cue "
                          f"start -- this srt does not belong to this narration index")
        return None, diag
    if agree / len(deltas) < MIN_LEAD_AGREE_FRACTION:
        diag["reason"] = (f"the offset is not a constant lead: only {agree} of {len(deltas)} "
                          f"matched pairs sit within {LEAD_TOL}s of the median {med}s")
        return None, diag
    return med, diag


def aligned_sibling(srt: Path, narr: dict) -> Path | None:
    """A caption revision beside this one that DOES line up with this narration index.

    When the srt handed to this tool is stale, the useful thing to say is not "it is stale" but
    "vNNN next to it is the one the narration matches".
    """
    for p in sorted(srt.parent.glob("captions.final.v*.srt"), reverse=True):
        if p.resolve() == srt.resolve():
            continue
        try:
            lead, _ = measure_lead(read_srt(p), narr)
        except Exception:  # noqa: BLE001
            continue
        if lead is not None:
            return p
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--srt", required=True)
    ap.add_argument("--film", help="film JSON whose captions[] should match the polished srt")
    ap.add_argument("--lead", type=float, default=0.0,
                    help="the lead this srt must END UP with, in seconds. A DESTINATION, not an "
                         "increment: the lead already present is measured against the narration "
                         "index and only the difference is applied.")
    ap.add_argument("--narr", help="narration index to measure the lead against (default: the "
                                   "latest <ep>/06_audio/narration_index.v*.json)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    srt = Path(a.srt)
    cues = read_srt(srt)
    before = report(cues)
    fixed = polish(cues)
    # THE LEAD IS A DESTINATION, NOT AN INCREMENT, AND IT IS MEASURED RATHER THAN REMEMBERED.
    #
    # This block used to subtract `--lead` from every start on every run, and _finish_episode.sh
    # step 4b runs it every time an episode is finished -- so a second finish shifted the whole
    # track another 0.25 s early, a third another 0.25 s, with nothing recording that it had
    # happened. The first repair recorded the applied lead in a sidecar and applied only the
    # difference. That sidecar then went stale, because step [4/7] rebuilds the srt from the
    # narration index at raw chunk timings on every film build and does not know the sidecar
    # exists: measured 2026-08-11, five of the eight queued episodes had a sidecar that
    # disagreed with their own srt, in both directions.
    #
    # The lead present in the file is now MEASURED (see measure_lead above) and only the
    # difference from the requested value is applied. Any number of runs converges on the
    # requested lead, whatever happened to the file in between, and a second run in a row shifts
    # exactly 0.0.
    applied_path = srt.with_suffix(".lead.json")
    narr_p = Path(a.narr) if a.narr else narration_index_for(srt)
    if narr_p is None or not narr_p.is_file():
        looked = srt.parent.parent / "06_audio"
        print(f"lead: CANNOT MEASURE -- no narration_index.v*.json under {looked}. The lead is "
              f"measured against the narration, never assumed. Pass --narr.", file=sys.stderr)
        return 1
    narr = json.loads(narr_p.read_text(encoding="utf-8"))
    measured, diag = measure_lead(fixed, narr)
    if measured is None:
        print(f"lead: CANNOT MEASURE -- {diag.get('reason')}", file=sys.stderr)
        print(f"      {json.dumps(diag, ensure_ascii=False)}", file=sys.stderr)
        print(f"      srt {srt}", file=sys.stderr)
        print(f"      narration index {narr_p}", file=sys.stderr)
        alt = aligned_sibling(srt, narr)
        if alt is not None:
            print(f"      {alt.name} in the same directory DOES line up with this narration "
                  f"index. If that is the revision the film was built from, polish THAT file.",
                  file=sys.stderr)
        return 1
    delta = round(a.lead - measured, 3)
    if delta:
        for c in fixed:
            # START only. Moving the END earlier as well shortened every cue by the lead and
            # tripped caption_coverage (EP53, 20/304 chunks under 80% of their chunk span).
            #
            # But moving a start earlier LENGTHENS the cue by the lead, and polish() already ran
            # its own MAX_CUE_SECONDS safety trim before this point, so it cannot see the result.
            # Measured 2026-08-11 on EP66 openfields: a 6.7 s cue plus a 0.6 s lead became 7.3 s
            # and would have hard-failed check_caption_format (MAX_CUE_SECONDS 7.0) on a single
            # cue -- exactly the way EP65 marmet failed acceptance once before. So a start is
            # never dragged earlier than MAX_CUE_SECONDS before its own end. That cue simply
            # takes less lead; it is not cut short, and no other cue is affected.
            want = max(0.0, c["start"] - delta)
            if delta > 0:
                want = min(c["start"], max(want, c["end"] - MAX_CUE_SECONDS))
            else:
                # a NEGATIVE delta pushes captions LATER, which measuring the lead rather than
                # remembering it makes possible for the first time; it must not invert a cue
                want = min(want, c["end"] - 0.05)
            c["start"] = round(want, 3)
    print(f"lead: measured {measured}s in {srt.name} over {diag['matched_pairs']} of "
          f"{diag['narration_chunks']} narration chunks, requested {a.lead}s -> shifting {delta}s")
    # C. impossible reading speed. Runs AFTER the lead shift, because the shift moves whole cues
    # and the rebalance divides a run's span -- doing it in the other order would let the shift
    # re-starve a cue this just repaired. A file with no violation is untouched.
    pre = cps_violations(fixed)
    if pre:
        fixed, moved, stuck = rebalance_cps(fixed)
        post = cps_violations(fixed)
        worst_pre = max(r for _, r in pre)
        worst_post = max((r for _, r in post), default=0.0)
        print(f"cps: {len(pre)} cue(s) over the {GATE_CPS:.0f} gate (worst {worst_pre:.0f}) -> "
              f"{len(post)} (worst {worst_post:.0f}); re-divided {moved} cue(s) inside their own "
              f"runs, {stuck} had no run that clears the gate")
    after = report(fixed)
    print(f"cues {len(cues)} -> {len(fixed)} | orphans {before[0]} -> {after[0]} | "
          f"dangling {before[1]} -> {after[1]}")
    if a.dry_run:
        return 0
    srt.write_text("\n".join(
        f"{i}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['text']}\n"
        for i, c in enumerate(fixed, 1)), encoding="utf-8")
    final_lead, final_diag = measure_lead(fixed, narr)
    applied_path.write_text(json.dumps({
        "applied_lead": final_lead,
        "requested_lead": a.lead,
        "measured_before": measured,
        "shifted": delta,
        "srt": srt.name,
        "narration_index": narr_p.name,
        "matched_pairs": final_diag.get("matched_pairs"),
        "narration_chunks": final_diag.get("narration_chunks"),
        "unmeasurable_reason": final_diag.get("reason"),
        "measured_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "why": ("RECORD ONLY -- nothing reads this file back, and nothing should. applied_lead "
                "is MEASURED out of the srt that was just written: for every narration chunk "
                "whose first word opens a cue, chunk start minus cue start, median. It used to "
                "be an INPUT to the next run, and build_case_film_generic.write_srt rebuilds the "
                "srt at raw chunk timings on every film build without updating it, so it went "
                "stale on five of eight episodes at once and a hand-patched value would have "
                "been correct for a single run."),
    }, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE {srt}")
    print(f"WROTE {applied_path.name} (measured applied_lead {final_lead})")
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
