#!/usr/bin/env python
"""Caption BREAK-QUALITY gate: captions must not split mid-phrase.

Owner, repeatedly: 「字幕がいつも変なところで途切れていた」.

Root cause is in the generator, not the timing: `gen_captions_case.py` cuts cues at
``MAX_WORDS, MAX_CHARS = 7, 42`` -- a purely mechanical word/char count with no syntactic
awareness. Real damage seen in EP38's shipped SRT:

    24  "...ends with a warning and a ride"
    25  "home."                                  <- orphan cue, phrase split
    27  "A child was handed a form giving up the right"
    28  "to a lawyer -"                          <- "the right | to a lawyer" split
    33  "...taught to trust the adults"
    34  "in the room, signed away..."            <- "the adults | in the room" split

`verify_caption_sync` / `fix_caption_dangling` already catch one class -- a LINE ending on
a function word -- and repair it after the fact. Two classes were unguarded, which is why
the defect kept shipping:

  A. ORPHAN CUE      -- a cue of 1-2 words that is not a complete sentence ("home.").
  B. CUE-BOUNDARY SPLIT -- a cue that ends with no punctuation while the next cue starts
     lowercase, i.e. one breath group chopped in two.

This gate measures all three so the defect is blocked BEFORE render instead of patched
after. It reuses `fix_caption_dangling.NO_DANGLE_END` rather than redefining the word list,
so the two can never drift apart.

Read-only. Exit 0 = PASS, 1 = FAIL.

Usage:
    python scripts/check_caption_breaks.py <captions.srt>
    python scripts/check_caption_breaks.py <captions.srt> --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    sys.stdout.reconfigure(encoding="utf-8")  # cp932 guard (Windows)
except Exception:
    pass

try:  # single source of truth for the function-word list
    from fix_caption_dangling import NO_DANGLE_END
except Exception:  # pragma: no cover - keep the gate usable if that script moves
    NO_DANGLE_END = {"a", "an", "the", "of", "to", "in", "on", "at", "for", "with", "and", "or",
                     "that", "who", "which", "is", "are", "was", "were", "my", "your", "their"}

CHECK_NAME = "caption_breaks"

MIN_CUE_WORDS = 3            # fewer words is an orphan unless it completes a sentence
TERMINAL_PUNCT = ".?!—-:;"   # a cue may end here; comma is weaker but allowed
SOFT_END = TERMINAL_PUNCT + ","
MAX_BAD_SHARE = 0.05         # <=5% of cues may end mid-phrase (rounding/edge cases)


def parse_srt(path: Path) -> list[dict]:
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip())
    cues = []
    for b in blocks:
        lines = [l for l in b.split("\n") if l.strip()]
        if len(lines) < 2:
            continue
        ts = next((l for l in lines if "-->" in l), None)
        if ts is None:
            continue
        text_lines = lines[lines.index(ts) + 1:]
        if text_lines:
            cues.append({"idx": len(cues) + 1, "lines": text_lines,
                         "text": " ".join(text_lines).strip()})
    return cues


def _last_word(s: str) -> str:
    # Digits count as word characters: "...the winter of 1989" ends on "1989", not on "of".
    # The letters-only pattern misread it and flagged a legitimate year-ending cue as a
    # dangling function word (EP82, 2026-08-25).
    w = re.findall(r"[A-Za-z0-9'’]+", s)
    return w[-1].lower() if w else ""


def evaluate_srt(path: Path) -> dict:
    cues = parse_srt(path)
    if not cues:
        return {"check": CHECK_NAME, "ok": True, "skipped": True,
                "reason": f"no cues parsed from {path.name}"}

    dangling_lines, orphans, boundary_splits = [], [], []

    for i, c in enumerate(cues):
        text = c["text"]

        # A. line ends on a function word with no punctuation (within a multi-line cue)
        for ln in c["lines"][:-1]:
            if ln.rstrip() and ln.rstrip()[-1] not in SOFT_END and _last_word(ln) in NO_DANGLE_END:
                dangling_lines.append({"cue": c["idx"], "line": ln.strip()})

        # B. orphan cue
        words = re.findall(r"[A-Za-z0-9'’]+", text)
        if len(words) < MIN_CUE_WORDS and (not text or text[-1] not in TERMINAL_PUNCT
                                           or not text[0].isupper()):
            orphans.append({"cue": c["idx"], "text": text})

        # C. cue ends mid-phrase: no punctuation AND the next cue continues lowercase
        if i + 1 < len(cues):
            nxt = cues[i + 1]["text"]
            ends_open = text and text[-1] not in SOFT_END
            continues = nxt[:1].islower()
            if ends_open and continues:
                sev = "hard" if _last_word(text) in NO_DANGLE_END else "soft"
                boundary_splits.append({"cue": c["idx"], "severity": sev,
                                        "end": " ".join(text.split()[-4:]),
                                        "next": " ".join(nxt.split()[:4])})

    hard_splits = [b for b in boundary_splits if b["severity"] == "hard"]
    bad_share = (len(dangling_lines) + len(orphans) + len(hard_splits)) / len(cues)
    ok = not dangling_lines and not orphans and not hard_splits and bad_share <= MAX_BAD_SHARE

    return {
        "check": CHECK_NAME,
        "ok": ok,
        "srt": str(path),
        "cues": len(cues),
        "dangling_lines": dangling_lines,
        "orphan_cues": orphans,
        "boundary_splits_hard": hard_splits,
        "boundary_splits_soft": len(boundary_splits) - len(hard_splits),
        "bad_share": round(bad_share, 4),
        "max_bad_share": MAX_BAD_SHARE,
    }


def _find_srt(epdir: Path) -> Path | None:
    cands = sorted(epdir.glob("08_edit/*.srt")) + sorted(epdir.glob("04_scenes/*.srt"))
    final = [p for p in cands if "final" in p.name]
    pool = final or cands
    return max(pool, key=lambda p: p.stat().st_mtime) if pool else None


def evaluate(epdir: Path) -> dict:
    """PREFLIGHT adapter for preflight_render_gate._run_ext_gate."""
    epdir = Path(epdir)
    srt = _find_srt(epdir)
    if srt is None:
        return {"ok": True, "skipped": True, "reason": "no .srt yet"}
    r = evaluate_srt(srt)
    if r.get("skipped"):
        return {"ok": True, "skipped": True, "reason": r.get("reason", "")}
    if r["ok"]:
        reason = f"{r['cues']} cues, no mid-phrase breaks [{srt.name}]"
    else:
        bits = []
        if r["dangling_lines"]:
            bits.append(f"{len(r['dangling_lines'])} line(s) end on a function word")
        if r["orphan_cues"]:
            ex = ", ".join(f'"{o["text"]}"' for o in r["orphan_cues"][:3])
            bits.append(f"{len(r['orphan_cues'])} orphan cue(s) [{ex}]")
        if r["boundary_splits_hard"]:
            b = r["boundary_splits_hard"][0]
            bits.append(f"{len(r['boundary_splits_hard'])} cue(s) split mid-phrase "
                        f'(e.g. "...{b["end"]}" | "{b["next"]}...")')
        reason = "; ".join(bits) + f" [{srt.name}]"
    return {"ok": r["ok"], "hard": True, "skipped": False, "reason": reason, **r}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("srt", type=Path)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if not a.srt.exists():
        print(f"FAIL {CHECK_NAME}: no such file {a.srt}")
        return 1
    r = evaluate_srt(a.srt)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["ok"] else 1
    if r.get("skipped"):
        print(f"WARN {CHECK_NAME}: {r['reason']}")
        return 0
    print(f"{'PASS' if r['ok'] else 'FAIL'} {CHECK_NAME}: {r['cues']} cues, "
          f"bad share {r['bad_share']:.1%} (cap {r['max_bad_share']:.0%})")
    for d in r["dangling_lines"][:5]:
        print(f"  ! cue {d['cue']:>4} line ends on a function word: \"{d['line']}\"")
    for o in r["orphan_cues"][:5]:
        print(f"  ! cue {o['cue']:>4} orphan: \"{o['text']}\"")
    for b in r["boundary_splits_hard"][:5]:
        print(f"  ! cue {b['cue']:>4} splits a phrase: \"...{b['end']}\" | \"{b['next']}...\"")
    extra = (len(r["dangling_lines"]) + len(r["orphan_cues"])
             + len(r["boundary_splits_hard"]) - 15)
    if extra > 0:
        print(f"  ... and ~{extra} more")
    if r["boundary_splits_soft"]:
        print(f"  (soft: {r['boundary_splits_soft']} cues continue into the next without "
              f"punctuation but do not end on a function word)")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
