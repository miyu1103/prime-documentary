#!/usr/bin/env python
"""Remove mid-phrase dangling caption line-ends WITHOUT touching timing.

verify_caption_sync flags a cue whose last displayed line ends on a function word with no
trailing punctuation (the owner's "字幕が変な所で切れる"). This is a LINE-WRAP defect, not a
timing one: fix it by moving the trailing function-word run to the FRONT of the next cue and
re-wrapping both cues to <=2 lines. Cue START times are unchanged (sync preserved) and the full
concatenated caption text is unchanged (verbatim-narration match preserved) -- only where the
words sit across the cue boundary and how each cue wraps into lines changes.

Usage:
    python scripts/fix_caption_dangling.py --ep PD-2026-034-rolin
    python scripts/fix_caption_dangling.py --ep rolin --dry-run
Rewrites the episode's newest 08_edit/*.srt in place (a .bak is written first).
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPISODES = ROOT / "episodes"
MAX_LINE = 44          # soft wrap width (chars)
MAX_LINES = 2

# Must match verify_caption_sync._NO_DANGLE_END (a line may not END on one of these w/o punctuation).
NO_DANGLE_END = {
    "a", "an", "the", "of", "to", "in", "on", "at", "for", "with", "from", "by", "as", "into", "onto",
    "over", "under", "than", "up", "out", "off", "about", "against", "between", "through",
    "and", "or", "but", "nor", "so", "yet",
    "is", "are", "was", "were", "be", "been", "being", "am", "has", "have", "had", "do", "does", "did",
    "will", "would", "can", "could", "shall", "should", "may", "might", "must",
    "my", "your", "his", "her", "its", "our", "their",
    "that", "this", "these", "those", "who", "which", "whose", "whom",
    "if", "when", "because", "while", "after", "before", "since", "until", "unless",
    "although", "though", "whether", "no", "not",
}
END_PUNCT = set(".?!,:;—-\"')")


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


def ends_dangling(line: str) -> bool:
    s = line.strip()
    if not s or s[-1] in END_PUNCT:
        return False
    toks = re.findall(r"[A-Za-z']+", s)
    return bool(toks) and norm(toks[-1]) in NO_DANGLE_END


def wrap(text: str) -> list[str]:
    """Wrap into <=MAX_LINES lines, each <=MAX_LINE where possible, preferring a break AFTER
    punctuation and never ending a non-final line on a dangling function word."""
    words = text.split()
    if not words:
        return [text]
    # try every single split point into 2 lines; pick the best legal one
    best = None
    for k in range(1, len(words)):
        l1 = " ".join(words[:k]); l2 = " ".join(words[k:])
        if ends_dangling(l1):
            continue
        score = (max(len(l1), len(l2)),               # prefer balanced/narrow
                 0 if l1.rstrip()[-1:] in END_PUNCT else 1,  # prefer break after punctuation
                 abs(len(l1) - len(l2)))
        cand = (score, [l1, l2])
        if best is None or cand[0] < best[0]:
            best = cand
    if best is not None and (len(text) > MAX_LINE or "\n" in text):
        l1, l2 = best[1]
        if len(l1) <= MAX_LINE or len(words) > 6:
            return [l1, l2]
    # single line fits (or no legal 2-way split found)
    if len(text) <= MAX_LINE:
        return [text]
    return best[1] if best else [text]


def parse(srt: str):
    cues = []
    for b in re.split(r"\n\s*\n", srt.strip()):
        lines = [l for l in b.splitlines() if l.strip()]
        ts = next((l for l in lines if "-->" in l), None)
        if not ts:
            continue
        idx = lines[0].strip() if lines[0].strip().isdigit() else ""
        body = [l for l in lines if "-->" not in l and not l.strip().isdigit()]
        cues.append({"idx": idx, "ts": ts, "text": " ".join(body).strip()})
    return cues


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    ep = a.ep if (EPISODES / a.ep).is_dir() else next(
        (d.name for d in sorted(EPISODES.glob("PD-2026-*")) if a.ep in d.name), a.ep)
    edit = EPISODES / ep / "08_edit"
    srts = [p for p in edit.glob("*.srt") if "proxy" not in p.name.lower()]
    if not srts:
        print(f"ERROR: no srt in {edit}", file=sys.stderr); return 1
    srt_p = sorted(srts, key=lambda p: (p.name, p.stat().st_size))[-1]
    cues = parse(srt_p.read_text(encoding="utf-8", errors="ignore"))

    fixed = 0
    for i in range(len(cues) - 1):
        # operate on the LAST line of the cue as it currently wraps
        cur_lines = wrap(cues[i]["text"])
        if not ends_dangling(cur_lines[-1]):
            continue
        # move the trailing dangling function-word run to the next cue
        words = cues[i]["text"].split()
        j = len(words)
        while j > 1 and norm(words[j - 1]) in NO_DANGLE_END:
            j -= 1
        moved = words[j:]
        if not moved:
            continue
        cues[i]["text"] = " ".join(words[:j])
        cues[i + 1]["text"] = " ".join(moved + cues[i + 1]["text"].split())
        fixed += 1
        print(f"  cue #{cues[i]['idx']}: moved trailing {moved} -> next cue")

    # Orphan merge (2026-08-25): the move above can strand one or two words as a cue of
    # their own ("What she" / "claim.") and check_caption_breaks rejects ANY such cue.
    # Fold an orphan into its predecessor; the predecessor keeps its start (sync preserved)
    # and inherits the orphan's end.
    TERM = ".?!—-:;"
    merged, morph = [], 0
    for c in cues:
        t = c["text"].strip()
        ws = re.findall(r"[A-Za-z0-9'’]+", t)
        if merged and len(ws) < 3 and (not t or t[-1] not in TERM or not t[:1].isupper()) \
           and len(merged[-1]["text"]) + len(t) + 1 <= 100:
            merged[-1]["text"] = (merged[-1]["text"] + " " + t).strip()
            merged[-1]["ts"] = (merged[-1]["ts"].split("-->")[0].rstrip()
                                + " --> " + c["ts"].split("-->")[1].strip())
            morph += 1
            # ascii-safe: an em-dash in the orphan text killed this print (and the whole
            # repair, leaving the srt unfixed) on a cp932 console, EP81 2026-08-25.
            safe = t.encode("ascii", "replace").decode()
            print(f"  cue #{c['idx']}: orphan {safe!r} merged into predecessor")
        else:
            merged.append(c)
    cues = merged
    fixed += morph

    if not fixed:
        print(f"{ep}: no dangling line-ends to fix ({srt_p.name})"); return 0

    out_lines = []
    for n, c in enumerate(cues, 1):
        wrapped = wrap(c["text"])[:MAX_LINES]
        out_lines.append(str(n)); out_lines.append(c["ts"]); out_lines.extend(wrapped); out_lines.append("")
    new = "\n".join(out_lines).strip() + "\n"

    if a.dry_run:
        print(f"{ep}: DRY-RUN would fix {fixed} dangling cue(s) in {srt_p.name}"); return 0
    shutil.copy2(srt_p, srt_p.with_suffix(".srt.bak"))
    srt_p.write_text(new, encoding="utf-8")
    print(f"{ep}: fixed {fixed} dangling cue(s) -> {srt_p.name} (.bak saved). Timing unchanged; text preserved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
