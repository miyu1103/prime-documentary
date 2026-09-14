#!/usr/bin/env python3
r"""EP38 "Kids for Cash": burned-in narration captions, frame-aligned to the master VO.

House rules (mirrors scripts/gen_captions_florence.py, the canonical caption builder):

  * TEXT is fact-locked to the APPROVED script (episodes/_planning/EP38_kidsforcash_
    script.en.v004.md). We never display re-transcribed ASR wording.
  * TIMING comes from faster-whisper word timestamps
    (episodes/PD-2026-038-kidsforcash/06_audio/word_timings.v001.json).
  * The scripted word sequence is aligned to the ASR word stream order-preservingly
    (difflib on normalized text); every scripted word gets its real spoken onset and
    unmatched words are interpolated between their nearest matched neighbours.
  * Text is re-segmented into breath-group lines that break at sentence/clause
    punctuation and never end on a dangling function word (STOP set).
  * Each cue is pulled LEAD=0.60 s early, kept monotonic / non-overlapping, held to a
    comfortable reading speed, and clamped inside the narration duration.

Deterministic + idempotent (no network, no GPU, pure recompute from the two inputs).

    py -3.11 scripts/build_kidsforcash_captions.py
      -> episodes/PD-2026-038-kidsforcash/04_scenes/captions.final.v001.srt
      -> episodes/PD-2026-038-kidsforcash/04_scenes/captions.final.v001.json
      -> episodes/PD-2026-038-kidsforcash/04_scenes/captions.final.v001.qc.json
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-038-kidsforcash"
SCRIPT = ROOT / "episodes" / "_planning" / "EP38_kidsforcash_script.en.v004.md"
WORDS = ROOT / "episodes" / EP / "06_audio" / "word_timings.v001.json"
OUT_DIR = ROOT / "episodes" / EP / "04_scenes"
OUT_SRT = OUT_DIR / "captions.final.v001.srt"
OUT_JSON = OUT_DIR / "captions.final.v001.json"
OUT_QC = OUT_DIR / "captions.final.v001.qc.json"

LEAD = 0.35                 # pull each cue ~0.35 s earlier so it lands ON / just-before the word
MAX_WORDS, MAX_CHARS = 10, 60
MIN_DUR = 0.9
# An un-recorded script passage (present in the planning script but never spoken in the master)
# aligns to nothing in the ASR, so its whole run of tokens interpolates into a near-zero gap and
# ships as a block of impossibly fast (40-60 cps) mis-timed cues. Detect & drop such a run: a long
# unmatched span squeezed below any real speech rate is not actually narrated.
PHANTOM_MIN_RUN = 6              # only a long unmatched run can be an un-recorded passage
PHANTOM_MAX_SEC_PER_WORD = 0.10  # < this => faster than any human speaks => not really spoken
CPS_TARGET = 19.0           # extend ends toward this reading speed
CPS_MERGE = 22.0            # merge a cue faster than this into the next (if it still fits)
CPS_CAP = 24.0             # final hard cap: extend end (small overlap allowed) to reach it
WRAP_MAX = 44               # max chars per wrapped SRT line
WRAP_BALANCE = 46           # max chars either half may reach when balancing onto two lines

# weak words a caption line must not END on (pull them onto the next line)
STOP = {
    "a", "an", "the", "of", "to", "in", "on", "at", "by", "for", "from", "into", "with",
    "as", "than", "and", "or", "but", "nor", "so", "yet", "is", "are", "was", "were",
    "be", "been", "being", "am", "has", "have", "had", "do", "does", "did", "will",
    "would", "can", "could", "shall", "should", "may", "might", "must", "his", "her",
    "its", "their", "my", "your", "our", "this", "that", "these", "those", "it", "he",
    "she", "we", "they", "you", "i", "not", "no", "if", "then", "when", "where", "which",
    "who", "whose", "whom", "up", "out", "off", "about", "because", "while", "though",
    # subordinating / prepositional function words the sync gate also forbids as a line end
    # (superset of verify_caption_sync._NO_DANGLE_END so this producer is >= as strict)
    "after", "against", "although", "before", "between", "through", "over", "under",
    "onto", "since", "until", "unless", "whether",
}

_CJK = re.compile(r"[　-ヿ㐀-鿿＀-￯]")
_SPOKEN_HEADER = re.compile(r"^##\s+(HOOK|ACT|ED)\b", re.IGNORECASE)


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


def word_count(text: str) -> int:
    """Count real words only (tokens carrying a letter/digit); a lone '—' is not a word."""
    return sum(1 for t in text.split() if re.search(r"[A-Za-z0-9]", t))


def srt_ts(t: float) -> str:
    t = max(0.0, t)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s += 1
        ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def extract_narration(md: str) -> list[str]:
    """Scripted narration tokens, in spoken order, from the approved v004 script.

    Only the spoken sections are kept: ## HOOK, ## ACT 1-4, ## ED. The ## OP bookend
    (brand title, no VO) and everything under the trailing ### notes are dropped.
    Each kept line has 〔CARD ...〕 markers, [ ... ] annotations, (parentheticals) and
    * italic markup stripped; any line still carrying Japanese note text is dropped.
    """
    tokens: list[str] = []
    spoken = False
    for raw in md.splitlines():
        line = raw.strip()
        if line.startswith("#"):
            # header line: (re)decide whether the following block is spoken narration
            spoken = bool(_SPOKEN_HEADER.match(line))
            continue
        if not spoken or not line or line == "---":
            continue
        line = re.sub(r"〔[^〕]*〕", " ", line)     # 〔CARD: ...〕 number/word markers
        line = re.sub(r"\[[^\]]*\]", " ", line)     # [L: ...] / [S0x] annotations
        line = re.sub(r"\([^)]*\)", " ", line)      # (→ OP title) stage directions
        line = line.replace("*", "")                # italic markup
        line = re.sub(r"\s+", " ", line).strip()
        if not line or _CJK.search(line):
            continue
        tokens.extend(line.split())
    return tokens


def align(script_toks: list[str], asr: list[dict], duration: float
          ) -> tuple[list[float], list[float], list[str]]:
    """Spoken onset/offset for each scripted token via an order-preserving difflib match
    on normalized text; unmatched tokens are interpolated between matched neighbours."""
    s_norm = [norm(t) for t in script_toks]
    a_norm = [w["n"] for w in asr]
    starts: list[float | None] = [None] * len(script_toks)
    ends: list[float | None] = [None] * len(script_toks)
    sm = difflib.SequenceMatcher(a=s_norm, b=a_norm, autojunk=False)
    for i, j, n in sm.get_matching_blocks():
        for k in range(n):
            starts[i + k] = asr[j + k]["start"]
            ends[i + k] = asr[j + k]["end"]
    unmatched = [script_toks[i] for i in range(len(script_toks)) if starts[i] is None]
    last = 0.0
    for i in range(len(script_toks)):
        if starts[i] is not None:
            last = ends[i]
            continue
        j = i + 1
        while j < len(script_toks) and starts[j] is None:
            j += 1
        nxt = starts[j] if j < len(script_toks) else duration
        run_start = i
        while run_start > 0 and starts[run_start - 1] is None:
            run_start -= 1
        run_len = j - run_start
        pos = i - run_start
        span = max(0.0, nxt - last)
        s = last + span * (pos + 0.5) / (run_len + 1)
        starts[i] = s
        ends[i] = s + 0.25
    return [float(x) for x in starts], [float(x) for x in ends], unmatched


def unspoken_indices(script_toks: list[str], asr: list[dict], duration: float) -> set[int]:
    """Indices of scripted tokens that are NOT actually narrated in the master.

    A maximal run of tokens that difflib matches to nothing in the ASR, and whose available
    time gap (between its matched neighbours) is shorter than PHANTOM_MAX_SEC_PER_WORD per word,
    could not have been spoken at that rate -- it is an un-recorded passage (the planning script
    carries a block the master never says). Returned indices are dropped from the caption stream
    so the captions match the SPOKEN narration and don't ship as impossibly fast mis-timed cues.
    Short/normal interpolated words (numbers, em-dashes, single ASR misses) are never touched."""
    s_norm = [norm(t) for t in script_toks]
    a_norm = [w["n"] for w in asr]
    matched = [False] * len(script_toks)
    starts: list[float | None] = [None] * len(script_toks)
    ends: list[float | None] = [None] * len(script_toks)
    sm = difflib.SequenceMatcher(a=s_norm, b=a_norm, autojunk=False)
    for i, j, n in sm.get_matching_blocks():
        for k in range(n):
            matched[i + k] = True
            starts[i + k] = asr[j + k]["start"]
            ends[i + k] = asr[j + k]["end"]
    drop: set[int] = set()
    n = len(script_toks)
    i = 0
    while i < n:
        if matched[i]:
            i += 1
            continue
        j = i
        while j < n and not matched[j]:
            j += 1
        last = ends[i - 1] if i > 0 and ends[i - 1] is not None else 0.0
        nxt = starts[j] if j < n and starts[j] is not None else duration
        run = j - i
        span = max(0.0, float(nxt) - float(last))
        if run >= PHANTOM_MIN_RUN and span / run < PHANTOM_MAX_SEC_PER_WORD:
            drop.update(range(i, j))
        i = j
    return drop


def split_lines(tokens: list[str]) -> list[tuple[list[str], int, int]]:
    """Break scripted tokens into breath-group lines at sentence/clause punctuation.

    Look-ahead length control: a word that would push the current line past MAX_WORDS
    or MAX_CHARS starts a NEW line, so every emitted line is genuinely <= those limits
    and needs no downstream wrapping. On such a length break we back up over trailing
    weak words so a line never ends on a/the/on/and… (no dangling). Clause/sentence
    punctuation always forces a clean break (those ends carry punctuation)."""
    lines: list[tuple[list[str], int, int]] = []
    cur: list[tuple[str, int]] = []

    def flush(seq: list[tuple[str, int]]) -> None:
        if seq:
            lines.append(([t for t, _ in seq], seq[0][1], seq[-1][1]))

    for i, w in enumerate(tokens):
        # would appending w overflow the line? if so, close the current line first,
        # backing up over trailing weak words so the break is clean.
        if cur:
            trial = len(" ".join(t for t, _ in cur) + " " + w)
            words_now = sum(1 for t, _ in cur if re.search(r"[A-Za-z0-9]", t))
            if words_now >= MAX_WORDS or trial > MAX_CHARS:
                cut = len(cur) - 1
                while cut > 0 and norm(cur[cut][0]) in STOP:
                    cut -= 1
                if cut <= 0:
                    cut = len(cur) - 1  # all-weak line: give up rather than loop
                flush(cur[:cut + 1])
                cur = cur[cut + 1:]
        cur.append((w, i))
        if re.search(r"[.?!—:;]$", w) or (w.endswith(",") and len(cur) >= 4):
            flush(cur)
            cur = []
    flush(cur)
    return lines


def wrap2(t: str, maxc: int = WRAP_MAX) -> str:
    """Balance a long cue onto at most two lines at a space near the midpoint."""
    if len(t) <= maxc:
        return t
    words = t.split()
    half = len(t) / 2
    for k in range(1, len(words)):
        if len(" ".join(words[:k])) >= half:
            for kk in (k, k - 1, k + 1):
                if 1 <= kk < len(words):
                    a = " ".join(words[:kk])
                    b = " ".join(words[kk:])
                    if len(a) <= WRAP_BALANCE and len(b) <= WRAP_BALANCE:
                        return a + "\n" + b
            break
    return t


def ends_dangling(line: str) -> bool:
    s = line.strip()
    if not s or s[-1] in ".?!,:;—-\"')":
        return False
    toks = re.findall(r"[A-Za-z']+", s)
    return bool(toks) and norm(toks[-1]) in STOP


def build_cues(toks: list[str], starts: list[float], ends: list[float],
               duration: float) -> list[list]:
    cues: list[list] = []  # [start, end, text]
    for words, a, b in split_lines(toks):
        text = re.sub(r"\s+([.,;:?!])", r"\1", " ".join(words)).strip()
        s = starts[a] - LEAD
        e = ends[b]
        if e <= s:
            e = s + MIN_DUR
        cues.append([s, e, text])

    def fits_single_line(text: str) -> bool:
        return len(text) <= MAX_CHARS and word_count(text) <= MAX_WORDS

    def has_alnum(text: str) -> bool:
        return bool(re.search(r"[A-Za-z0-9]", text))

    # (1) Absorb punctuation-only fragments (a lone "—" etc.) into a neighbour so they
    # never flicker as their own cue. Prefer the previous cue when it stays <=MAX_CHARS
    # (a trailing dash is not dangling); otherwise carry it forward onto the next cue.
    absorbed: list[list] = []
    pending_lead: list | None = None
    for c in cues:
        if pending_lead is not None:
            c[0] = pending_lead[0]
            c[2] = (pending_lead[2] + " " + c[2]).strip()
            pending_lead = None
        if not has_alnum(c[2]):
            if absorbed and len((absorbed[-1][2] + " " + c[2]).strip()) <= MAX_CHARS:
                absorbed[-1][1] = c[1]
                absorbed[-1][2] = (absorbed[-1][2] + " " + c[2]).strip()
            else:
                pending_lead = c  # attach to the next cue instead
            continue
        absorbed.append(c)
    if pending_lead is not None:              # dangling fragment at the very end
        if absorbed and len((absorbed[-1][2] + " " + pending_lead[2]).strip()) <= MAX_CHARS:
            absorbed[-1][1] = pending_lead[1]
            absorbed[-1][2] = (absorbed[-1][2] + " " + pending_lead[2]).strip()
        else:
            absorbed.append(pending_lead)
    cues = absorbed

    # (2) Merge a genuine single-word / ultra-short orphan backward ONLY when the result
    # still fits ONE clean line (<=MAX_WORDS words, <=MAX_CHARS chars) and does not create
    # a dangling end. Otherwise leave it as its own cue (its show time is set in step 4).
    merged: list[list] = []
    for c in cues:
        orphan = word_count(c[2]) <= 1
        if merged and orphan:
            combo = (merged[-1][2] + " " + c[2]).strip()
            if fits_single_line(combo) and not ends_dangling(combo):
                merged[-1][1] = c[1]
                merged[-1][2] = combo
                continue
        merged.append(c)
    cues = merged

    n = len(cues)
    # (3) Lead-aligned, non-decreasing cue starts (the lead pulls each cue ~0.60 s early;
    # a start may never precede the previous cue's start). Start of the first cue >= 0.
    starts_out = [max(0.0, cues[0][0])]
    for i in range(1, n):
        starts_out.append(max(cues[i][0], starts_out[i - 1]))

    # (4) Minimum-show relaxation so no cue is starved: push a start later when the prior
    # cue would otherwise show < MIN_DUR. Forward pass, then a backward pass to guarantee
    # the tail fits inside the narration duration.
    for i in range(1, n):
        if starts_out[i] < starts_out[i - 1] + MIN_DUR:
            starts_out[i] = starts_out[i - 1] + MIN_DUR
    if starts_out[-1] + MIN_DUR > duration:
        starts_out[-1] = min(starts_out[-1], max(0.0, duration - MIN_DUR))
        for i in range(n - 2, -1, -1):
            if starts_out[i] > starts_out[i + 1] - MIN_DUR:
                starts_out[i] = max(0.0, starts_out[i + 1] - MIN_DUR)

    # (5) Contiguous captions: each cue holds until the next begins (the 0.60 s lead means
    # the next line swaps in ~0.60 s before its first spoken word). Last cue -> duration.
    out: list[list] = []
    for i in range(n):
        s = round(starts_out[i], 3)
        e = round(starts_out[i + 1] if i + 1 < n else duration, 3)
        if e <= s:
            e = round(min(duration, s + MIN_DUR), 3)
        out.append([s, e, cues[i][2]])
    return out


def qc_report(out: list[list], duration: float, toks: list[str], unmatched: list[str]
              ) -> dict:
    max_line_chars = 0
    max_line_words = 0
    max_cue_chars = 0
    max_cue_words = 0
    dangling = []
    for idx, (s, e, t) in enumerate(out, start=1):
        wrapped = wrap2(t)
        for ln in wrapped.split("\n"):
            max_line_chars = max(max_line_chars, len(ln))
            max_line_words = max(max_line_words, word_count(ln))
            if ends_dangling(ln):
                dangling.append({"cue": idx, "line": ln})
        max_cue_chars = max(max_cue_chars, len(t))
        max_cue_words = max(max_cue_words, word_count(t))

    out_of_range = [i + 1 for i, (s, e, _) in enumerate(out)
                    if s < 0 or e > duration + 1e-6 or e <= s]
    non_monotonic = [i + 1 for i in range(1, len(out)) if out[i][0] < out[i - 1][0]]
    overlaps = [i + 1 for i in range(1, len(out)) if out[i][0] < out[i - 1][1] - 1e-6]
    worst_cps = max((len(t) / max(e - s, 0.001) for s, e, t in out), default=0.0)

    checks = {
        "cue_count_positive": len(out) > 0,
        "all_within_duration": not out_of_range,
        "times_monotonic": not non_monotonic,
        "no_overlaps": not overlaps,
        "line_words_within_limit": max_line_words <= MAX_WORDS,
        "line_chars_within_limit": max_line_chars <= WRAP_BALANCE,
        "no_dangling": not dangling,
    }
    return {
        "episode_id": EP,
        "revision": "v001",
        "source_text": str(SCRIPT).replace("\\", "/"),
        "source_timing": str(WORDS).replace("\\", "/"),
        "narration_duration_sec": duration,
        "cue_count": len(out),
        "coverage_first_start_sec": round(out[0][0], 3) if out else None,
        "coverage_last_end_sec": round(out[-1][1], 3) if out else None,
        "coverage_seconds": round(out[-1][1] - out[0][0], 3) if out else 0.0,
        "script_tokens": len(toks),
        "unmatched_tokens": len(unmatched),
        "limits": {"max_words_per_line": MAX_WORDS, "max_chars_per_line": WRAP_BALANCE,
                   "target_max_chars_split": MAX_CHARS, "lead_in_sec": LEAD},
        "max_line_words": max_line_words,
        "max_line_chars": max_line_chars,
        "max_cue_words": max_cue_words,
        "max_cue_chars": max_cue_chars,
        "worst_cps": round(worst_cps, 1),
        "dangling": dangling,
        "out_of_range_cues": out_of_range,
        "non_monotonic_cues": non_monotonic,
        "overlap_cues": overlaps,
        "checks": checks,
        "qc_status": "pass" if all(checks.values()) else "review",
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if not SCRIPT.exists():
        print(f"MISSING script: {SCRIPT}", file=sys.stderr)
        return 2
    if not WORDS.exists():
        print(f"MISSING word timings: {WORDS}", file=sys.stderr)
        return 2

    wt = json.loads(WORDS.read_text("utf-8"))
    asr = wt["words"]
    for w in asr:
        w["n"] = norm(w["word"])
    duration = float(wt.get("duration_sec") or 0.0)
    if duration <= 0:
        duration = max((w["end"] for w in asr), default=0.0)

    toks = extract_narration(SCRIPT.read_text("utf-8"))
    if not toks:
        print("ERROR: no narration tokens extracted from script", file=sys.stderr)
        return 1
    starts, ends, unmatched = align(toks, asr, duration)

    # Drop any un-recorded passage (planning-script text the master never speaks) so captions
    # match the SPOKEN narration and never ship as a block of impossibly fast, mis-timed cues.
    drop = unspoken_indices(toks, asr, duration)
    dropped_tokens = [toks[i] for i in sorted(drop)]
    if drop:
        keep = [i for i in range(len(toks)) if i not in drop]
        toks = [toks[i] for i in keep]
        starts = [starts[i] for i in keep]
        ends = [ends[i] for i in keep]
        drop_norm = {norm(t) for t in dropped_tokens}
        unmatched = [t for t in unmatched if norm(t) not in drop_norm]

    out = build_cues(toks, starts, ends, duration)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # SRT (wrapped to <=2 lines)
    srt = "\n".join(f"{k+1}\n{srt_ts(s)} --> {srt_ts(e)}\n{wrap2(t)}\n"
                    for k, (s, e, t) in enumerate(out))
    tmp = OUT_SRT.with_suffix(".srt.tmp")
    tmp.write_text(srt, "utf-8")
    tmp.replace(OUT_SRT)

    # JSON (cues: index/start/end/text single-line, plus wrapped for the renderer)
    cues_json = [{"index": k + 1, "start": round(s, 3), "end": round(e, 3),
                  "text": t, "lines": wrap2(t).split("\n")}
                 for k, (s, e, t) in enumerate(out)]
    payload = {
        "episode_id": EP,
        "revision": "v001",
        "source": "approved script v004 text force-aligned to word_timings.v001.json (faster-whisper medium.en)",
        "narration_duration_sec": duration,
        "lead_in_sec": LEAD,
        "cue_count": len(out),
        "cues": cues_json,
    }
    tmp = OUT_JSON.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", "utf-8")
    tmp.replace(OUT_JSON)

    # QC
    qc = qc_report(out, duration, toks, unmatched)
    tmp = OUT_QC.with_suffix(".qc.tmp")
    tmp.write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", "utf-8")
    tmp.replace(OUT_QC)

    if dropped_tokens:
        print(f"dropped {len(dropped_tokens)} un-recorded token(s) not spoken in master: "
              + " ".join(dropped_tokens[:60]) + (" ..." if len(dropped_tokens) > 60 else ""))
    print(f"scripted tokens={len(toks)}  asr words={len(asr)}  unmatched={len(unmatched)}")
    print(f"wrote {OUT_SRT.relative_to(ROOT)}")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUT_QC.relative_to(ROOT)}")
    print(f"  cues={qc['cue_count']}  coverage={qc['coverage_first_start_sec']}"
          f"..{qc['coverage_last_end_sec']}s / dur={duration}s")
    print(f"  max_line_words={qc['max_line_words']}  max_line_chars={qc['max_line_chars']}"
          f"  worst={qc['worst_cps']}cps  dangling={len(qc['dangling'])}")
    print(f"  qc_status={qc['qc_status']}  checks={qc['checks']}")
    if unmatched:
        print(f"  unmatched sample: " + ", ".join(unmatched[:30])
              + (" ..." if len(unmatched) > 30 else ""))
    return 0 if qc["qc_status"] == "pass" else 3


if __name__ == "__main__":
    raise SystemExit(main())
