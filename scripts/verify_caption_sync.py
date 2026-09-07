#!/usr/bin/env python3
r"""Independent caption-sync gate — catches LATE / drifting captions before they ship.

The owner's #1 recurring defect is captions that arrive AFTER the narration, worse in the
back half (progressive drift). scripts/gen_captions_forced.py fixes the ROOT CAUSE by aligning
each narration chunk inside its own known [start,end] window (drift-free). This script is the
INDEPENDENT GATE that would have CAUGHT that defect automatically, so it can never re-ship.

It does NOT trust the .srt's own timestamps (those came from the aligner under test) and it does
NOT trust faster-whisper's full-file word timestamps (they drift LATE over an 11-min file — the
very bug we guard against). Instead it re-derives DRIFT-FREE ground-truth word onsets exactly the
way gen_captions_forced.align_windowed does: decode the master once to 16 kHz mono float32, slice
per narration_index.v001 chunk window, transcribe EACH window in isolation with medium.en
(word_timestamps), and offset word times by the window start. Every word time is therefore locally
accurate and cross-chunk drift cannot accumulate — a trustworthy yardstick to measure the .srt.

For each SRT cue it finds the ground-truth onset of the cue's FIRST spoken word (matched by
normalized text against the windowed word stream) and computes:

    lag = cue_start - true_onset      (POSITIVE = caption LATE; NEGATIVE = caption leads/early)

A caption LEADING its word by up to ~0.8 s reads fine (and gen_captions_forced deliberately biases
early). A caption that LAGS is the defect. It reports median/p75/p90 lag, % of cues late by >0.15 s,
and a PER-MINUTE median-lag table that exposes a late-and-worsening back half (drift). It also scans
segmentation: a cue that ENDS on a dangling function word with no trailing punctuation is a
mid-phrase cut (the owner's "変な所で途切れてる").

Usage:
  py -3.11 scripts/verify_caption_sync.py --ep PD-2026-032-carsearch
  py -3.11 scripts/verify_caption_sync.py --ep PD-2026-032-carsearch --srt <path> --master <path>
  py -3.11 scripts/verify_caption_sync.py --ep PD-2026-032-carsearch --model small.en   # faster dev

Exit code 0 = PASS, non-zero = FAIL (or a hard error such as a missing file). Read-only: it never
writes into the episode; it may cache the ground-truth transcription under the OS temp dir keyed by
the master's identity so re-runs (and the acceptance gate) don't re-transcribe 11 minutes each time.

check_final_acceptance.check_caption_sync() imports this module and calls evaluate(epdir); the dict
keys below (ok / skipped / reason / lag_p50 / exact_pct / late_pct / segment_drift /
function_word_line_ends / problems) are that contract — keep them stable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from statistics import median
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-032-carsearch"
DEFAULT_MODEL = "medium.en"  # matches gen_captions_forced.py's aligner model (word-timing accuracy)
SAMPLE_RATE = 16000

# --- PASS/FAIL thresholds (a caption LEADING its word is GOOD, not a failure) --------------------
# lag > 0  => caption is LATE (the defect). lag < 0 => caption leads/early (fine up to LEAD_OK).
FAIL_P90_LAG = 0.35          # FAIL if the 90th-percentile lag exceeds +0.35 s (tail of late cues)
FAIL_MEDIAN_LAG = 0.10       # FAIL if the median lag exceeds +0.10 s (systematic lateness)
FAIL_SEGMENT_DRIFT = 0.50    # FAIL if ANY per-minute median lag exceeds +0.50 s (progressive drift)
LATE_TOL = 0.15              # a cue whose lag exceeds this is counted "LATE" (late_pct)
EXACT_TOL = 0.15             # |lag| within this is counted "on the word" (exact_pct)
LEAD_OK = 0.80               # leading (negative lag) up to this is acceptable, reported not failed
MIN_MATCHED_FRACTION = 0.60  # if fewer cues match ground-truth than this, reliability is degraded

# Function words a caption line must NOT end on with no trailing punctuation: it leaves the phrase
# dangling and reads as a mid-phrase cut. (Superset of gen_captions_forced._NO_DANGLE_END so this
# gate stays at least as strict as the producer.)
_NO_DANGLE_END = {
    "a", "an", "the",
    "of", "to", "in", "on", "at", "for", "with", "from", "by", "as", "into", "onto",
    "over", "under", "than", "up", "out", "off", "about", "against", "between", "through",
    "and", "or", "but", "nor", "so", "yet",
    "is", "are", "was", "were", "be", "been", "being", "am",
    "has", "have", "had", "do", "does", "did",
    "will", "would", "can", "could", "shall", "should", "may", "might", "must",
    "my", "your", "his", "her", "its", "our", "their",
    "that", "this", "these", "those", "who", "which", "whose", "whom",
    "if", "when", "because", "while", "after", "before", "since", "until", "unless",
    "although", "though", "whether", "no", "not",
}
_TRAIL = "\"')]}”’"                 # trailing quotes/brackets ignored when reading final punctuation
_END_PUNCT = set(".?!,:;—-")        # a line ending in any of these is a clean break (not dangling)


def norm(w: str) -> str:
    """Normalize a token to its comparable core (lowercase alphanumerics only)."""
    return re.sub(r"[^a-z0-9]", "", w.lower())


# ---------------------------------------------------------------------------------------------
# SRT parsing
# ---------------------------------------------------------------------------------------------

_TS = re.compile(r"(\d\d):(\d\d):(\d\d)[,.](\d{1,3})\s*-->\s*(\d\d):(\d\d):(\d\d)[,.](\d{1,3})")


def _ts_to_seconds(h: str, m: str, s: str, ms: str) -> float:
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def parse_srt(path: Path) -> list[dict[str, Any]]:
    """Parse an .srt into cues: [{'start', 'end', 'lines': [str,...]}] in file order."""
    cues: list[dict[str, Any]] = []
    text = path.read_text(encoding="utf-8", errors="ignore").strip()
    for block in re.split(r"\n\s*\n", text):
        raw_lines = [ln for ln in block.splitlines() if ln.strip()]
        ts_line = next((ln for ln in raw_lines if "-->" in ln), None)
        if not ts_line:
            continue
        mt = _TS.search(ts_line)
        if not mt:
            continue
        start = _ts_to_seconds(mt[1], mt[2], mt[3], mt[4])
        end = _ts_to_seconds(mt[5], mt[6], mt[7], mt[8])
        body = [ln for ln in raw_lines if "-->" not in ln and not ln.strip().isdigit()]
        if body:
            cues.append({"start": start, "end": end, "lines": body})
    return cues


# ---------------------------------------------------------------------------------------------
# ground-truth word onsets (drift-free windowed transcription)
# ---------------------------------------------------------------------------------------------

def load_windows(ep_dir: Path) -> list[tuple[float, float]]:
    """Per-chunk (start, end) windows in the master, spoken order, from narration_index.v001.json.
    Returns [] if the file is absent or carries no usable numeric windows."""
    p = ep_dir / "06_audio" / "narration_index.v001.json"
    if not p.exists():
        return []
    try:
        chunks = (json.loads(p.read_text("utf-8")) or {}).get("chunks", [])
    except Exception:  # noqa: BLE001 - malformed index -> treat as no windows (caller warns/falls back)
        return []
    wins: list[tuple[float, float]] = []
    for c in chunks:
        s, e = c.get("start"), c.get("end")
        if isinstance(s, (int, float)) and isinstance(e, (int, float)) and e > s:
            wins.append((float(s), float(e)))
    return wins


def _decode_master(master: Path):
    """Decode the whole master once to a 16 kHz mono float32 numpy array (no temp files)."""
    import numpy as np
    raw = subprocess.run(
        ["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(master),
         "-ar", str(SAMPLE_RATE), "-ac", "1", "-f", "f32le", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def _cache_key(master: Path, windows: list[tuple[float, float]], model: str) -> str:
    st = master.stat()
    sig = f"{master.resolve()}|{st.st_size}|{int(st.st_mtime)}|{model}|{windows!r}"
    return hashlib.sha256(sig.encode("utf-8")).hexdigest()[:32]


def _load_whisper(model_name: str, what: str):
    """CUDA when the box has it, CPU otherwise. The ground truth is the same either way --
    only the wall clock changes (a 61-min master is ~2.5h on cpu/int8, minutes on the 4090).
    Set PD_WHISPER_DEVICE=cpu to force the old path."""
    from faster_whisper import WhisperModel
    import os
    want = os.environ.get("PD_WHISPER_DEVICE", "auto").lower()
    if want in ("auto", "cuda"):
        try:
            m = WhisperModel(model_name, device="cuda", compute_type="float16")
            # Constructing the model does NOT touch cuBLAS -- the missing-DLL error surfaces on
            # the first encode, i.e. 20 minutes into a gate run (EP51, 2026-07-30). Smoke-test
            # one second of silence here so the fallback happens before any real work.
            import numpy as _np
            list(m.transcribe(_np.zeros(16000, dtype=_np.float32), beam_size=1)[0])
            print(f"loading faster-whisper {model_name} (cuda/float16) for {what}...")
            return m
        except Exception as e:
            if want == "cuda":
                raise
            print(f"  cuda unavailable ({str(e)[:80]}); falling back to cpu/int8")
    print(f"loading faster-whisper {model_name} (cpu/int8) for {what}...")
    return WhisperModel(model_name, device="cpu", compute_type="int8")


def transcribe_windowed(master: Path, windows: list[tuple[float, float]],
                        model_name: str) -> list[dict[str, Any]]:
    """Transcribe each master window IN ISOLATION (drift-free) and return absolute word times:
    [{'n': normalized, 'start': abs_sec, 'end': abs_sec}, ...] in spoken order. Mirrors
    gen_captions_forced.transcribe_windowed."""
    audio = _decode_master(master)
    fw = _load_whisper(model_name, f"{len(windows)} windowed segments")
    words: list[dict[str, Any]] = []
    for (ws, we) in windows:
        a = audio[max(0, int(ws * SAMPLE_RATE)):int(we * SAMPLE_RATE)]
        if a.size < SAMPLE_RATE // 8:  # < 0.125 s -> silence-only window
            continue
        segs, _ = fw.transcribe(a, word_timestamps=True, vad_filter=False,
                                beam_size=5, language="en")
        for s in segs:
            for w in (s.words or []):
                words.append({"n": norm(w.word), "start": ws + w.start, "end": ws + w.end})
    print(f"  ground-truth words (windowed): {len(words)}")
    return words


def transcribe_wholefile(master: Path, model_name: str) -> list[dict[str, Any]]:
    """Fallback: transcribe the WHOLE master at once. faster-whisper's word timestamps DRIFT LATE
    over a long file, so onset lags measured this way are LESS reliable (the caller warns)."""
    fw = _load_whisper(model_name, "WHOLE-FILE transcription (fallback)")
    segs, _ = fw.transcribe(str(master), word_timestamps=True, vad_filter=False,
                            beam_size=5, language="en")
    words: list[dict[str, Any]] = []
    for s in segs:
        for w in (s.words or []):
            words.append({"n": norm(w.word), "start": w.start, "end": w.end})
    print(f"  ground-truth words (whole-file, drift-prone): {len(words)}")
    return words


def ground_truth_words(master: Path, windows: list[tuple[float, float]], model_name: str,
                       use_cache: bool) -> tuple[list[dict[str, Any]], bool]:
    """Return (word_stream, windowed). windowed=True when the drift-free per-window path was used.
    Caches the stream under the OS temp dir keyed by the master's identity + model + windows."""
    windowed = bool(windows)
    cache_path: Optional[Path] = None
    if use_cache:
        key = _cache_key(master, windows, model_name)
        cache_path = Path(tempfile.gettempdir()) / "pd_capsync_cache" / f"{key}.json"
        if cache_path.exists():
            try:
                blob = json.loads(cache_path.read_text("utf-8"))
                print(f"  (reusing cached ground-truth: {cache_path})")
                return blob["words"], bool(blob.get("windowed", windowed))
            except Exception:  # noqa: BLE001 - corrupt cache -> recompute
                pass
    words = transcribe_windowed(master, windows, model_name) if windowed \
        else transcribe_wholefile(master, model_name)
    if cache_path is not None:
        try:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps({"windowed": windowed, "words": words}), "utf-8")
        except Exception:  # noqa: BLE001 - caching is best-effort, never fatal
            pass
    return words, windowed


# ---------------------------------------------------------------------------------------------
# alignment: caption words -> ground-truth onsets (sequential, drift-proof)
# ---------------------------------------------------------------------------------------------

def _match_onsets(cap_words: list[str], gt: list[dict[str, Any]]) -> list[Optional[float]]:
    """Align the caption word stream (normalized, spoken order) to the ground-truth word stream and
    return each caption word's true onset (gt start), or None if it has no confident match.

    Uses difflib.SequenceMatcher — a proper order-preserving sequence alignment — NOT a greedy
    cursor. A greedy cursor permanently desyncs after a single whisper drop/insert (it is exactly
    the global-drift failure gen_captions abandoned for per-window alignment); SequenceMatcher finds
    the longest matching runs and recurses around them, so ~30 dropped/added whisper words never
    cascade. Matching is on NORMALIZED text only, so a shifted/late .srt cannot fool it: the
    ground-truth onset stays put and the induced lag is exposed.
    """
    import difflib
    gt_norm = [w["n"] for w in gt]
    times: list[Optional[float]] = [None] * len(cap_words)
    sm = difflib.SequenceMatcher(a=cap_words, b=gt_norm, autojunk=False)
    for i, j, n in sm.get_matching_blocks():
        for k in range(n):
            times[i + k] = gt[j + k]["start"]
    return times


def _cue_words(cue: dict[str, Any]) -> list[str]:
    """Normalized spoken words of a cue in order (drops pure punctuation tokens)."""
    return [norm(w) for ln in cue["lines"] for w in ln.split() if norm(w)]


def _dangling_end(cue: dict[str, Any]) -> Optional[str]:
    """If the cue's LAST line ends on a dangling function word with no trailing punctuation, return
    that word (the offending mid-phrase break); else None."""
    last = cue["lines"][-1].strip()
    toks = last.split()
    if not toks:
        return None
    tok = toks[-1]
    core = tok.rstrip(_TRAIL)
    if core and core[-1] in _END_PUNCT:
        return None  # clean break: ends in . ? ! , : ; — -
    return tok if norm(tok) in _NO_DANGLE_END else None


def _pct(part: int, whole: int) -> float:
    return 100.0 * part / whole if whole else 0.0


def _percentile(sorted_vals: list[float], q: float) -> float:
    """Linear-interpolated percentile (q in [0,1]) of a pre-sorted list."""
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    pos = q * (len(sorted_vals) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(sorted_vals) - 1)
    frac = pos - lo
    return sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac


# ---------------------------------------------------------------------------------------------
# path resolution (episode -> srt / master), mirrors gen_captions_forced
# ---------------------------------------------------------------------------------------------

def resolve_srt(ep_dir: Path, override: Optional[str]) -> Path:
    if override:
        return Path(override)
    default = ep_dir / "08_edit" / "captions.final.v001.srt"
    if default.exists():
        return default
    # else: highest captions.final.v*.srt, else any non-proxy .srt with the latest end time
    finals = sorted((ep_dir / "08_edit").glob("captions.final.v*.srt"))
    if finals:
        return finals[-1]
    others = [p for p in (ep_dir / "08_edit").glob("*.srt")
              if "review_proxy" not in p.name and p.stat().st_size > 0]
    if others:
        def _last_end(p: Path) -> float:
            ends = _TS.findall(p.read_text("utf-8", errors="ignore"))
            return max((_ts_to_seconds(e[4], e[5], e[6], e[7]) for e in ends), default=0.0)
        return max(others, key=_last_end)
    return default  # non-existent; caller reports a clear error


def resolve_master(ep_dir: Path, override: Optional[str]) -> Path:
    if override:
        return Path(override)
    slug = ep_dir.name
    cfg = ROOT / "config" / "storage.local.json"
    media_root = Path(json.loads(cfg.read_text("utf-8"))["roots"]["media"]["path"])
    master_dir = media_root / "episodes" / slug / "06_voice" / "master"
    cands = sorted(master_dir.glob("vc_master_v*.mp3"))
    if cands:
        return cands[-1]
    return master_dir / "vc_master_v001.mp3"


# ---------------------------------------------------------------------------------------------
# core evaluation (importable by check_final_acceptance.check_caption_sync)
# ---------------------------------------------------------------------------------------------

def evaluate(ep_dir: Path, srt: Optional[str] = None, master: Optional[str] = None,
             model_name: str = DEFAULT_MODEL, use_cache: bool = True) -> dict[str, Any]:
    """Measure caption timing accuracy against drift-free ground-truth onsets and return a result
    dict. Never raises on missing inputs — returns {'skipped': True, ...} or {'ok': False, ...}.

    Result keys (stable contract used by check_final_acceptance.check_caption_sync):
      ok, skipped, reason, matched, total_cues, lag_p50, lag_p75, lag_p90, exact_pct, late_pct,
      segment_drift, function_word_line_ends, per_minute, problems, reliability.
    """
    ep_dir = Path(ep_dir)
    srt_path = resolve_srt(ep_dir, srt)
    if not srt_path.exists():
        return {"check": "caption_sync", "ok": False, "skipped": True,
                "reason": f"SRT not found: {srt_path}"}
    cues = parse_srt(srt_path)
    if not cues:
        return {"check": "caption_sync", "ok": False, "skipped": True,
                "reason": f"no cues parsed from {srt_path}"}

    master_path = resolve_master(ep_dir, master)
    if not master_path.exists():
        return {"check": "caption_sync", "ok": False, "skipped": True,
                "reason": f"master audio not found: {master_path}"}

    problems: list[str] = []
    windows = load_windows(ep_dir)
    if not windows:
        problems.append("narration_index.v001 windows missing -> whole-file transcription "
                        "(reduced reliability: whisper full-file timestamps drift LATE)")
    try:
        gt, windowed = ground_truth_words(master_path, windows, model_name, use_cache)
    except FileNotFoundError as exc:
        return {"check": "caption_sync", "ok": False, "skipped": True,
                "reason": f"ffmpeg/faster-whisper unavailable: {exc}"}
    except subprocess.CalledProcessError as exc:
        err = (exc.stderr or b"").decode("utf-8", "ignore")[:200]
        return {"check": "caption_sync", "ok": False, "skipped": True,
                "reason": f"ffmpeg failed decoding master: {err}"}
    reliability = "windowed" if windowed else "wholefile"
    if not gt:
        return {"check": "caption_sync", "ok": False, "skipped": True,
                "reason": f"ground-truth transcription produced no words from {master_path}"}

    # global sequential match of ALL caption words, then take each cue's first matched onset
    flat_words: list[str] = []
    cue_word_span: list[tuple[int, int]] = []  # [start,end) index into flat_words per cue
    for cue in cues:
        w = _cue_words(cue)
        cue_word_span.append((len(flat_words), len(flat_words) + len(w)))
        flat_words.extend(w)
    onsets = _match_onsets(flat_words, gt)

    lags: list[float] = []
    lag_by_minute: dict[int, list[float]] = {}
    matched = 0
    for cue, (a, b) in zip(cues, cue_word_span):
        onset = next((onsets[i] for i in range(a, b) if onsets[i] is not None), None)
        if onset is None:
            continue
        matched += 1
        lag = cue["start"] - onset
        lags.append(lag)
        lag_by_minute.setdefault(int(cue["start"] // 60), []).append(lag)

    total = len(cues)
    if matched == 0:
        return {"check": "caption_sync", "ok": False, "skipped": True,
                "reason": f"0/{total} cues matched ground-truth words (alignment failed)"}

    slags = sorted(lags)
    lag_p50 = _percentile(slags, 0.50)
    lag_p75 = _percentile(slags, 0.75)
    lag_p90 = _percentile(slags, 0.90)
    late = sum(1 for x in lags if x > LATE_TOL)
    exact = sum(1 for x in lags if abs(x) <= EXACT_TOL)
    lead = sum(1 for x in lags if x < -EXACT_TOL)
    late_pct = _pct(late, matched)
    exact_pct = _pct(exact, matched)
    lead_pct = _pct(lead, matched)

    per_minute = [{"minute": mnt, "n": len(v), "median": median(v)}
                  for mnt, v in sorted(lag_by_minute.items())]
    segment_drift = max((pm["median"] for pm in per_minute), default=0.0)

    dangling = [(idx + 1, w, cue["lines"][-1])
                for idx, cue in enumerate(cues) if (w := _dangling_end(cue))]
    fword_ends = len(dangling)

    matched_frac = matched / total

    # PASS/FAIL
    if lag_p90 > FAIL_P90_LAG:
        problems.append(f"p90 lag {lag_p90:+.3f}s > +{FAIL_P90_LAG:.2f}s (too many late cues)")
    if lag_p50 > FAIL_MEDIAN_LAG:
        problems.append(f"median lag {lag_p50:+.3f}s > +{FAIL_MEDIAN_LAG:.2f}s (systematically late)")
    drift_minutes = [pm for pm in per_minute if pm["median"] > FAIL_SEGMENT_DRIFT]
    if drift_minutes:
        worst = max(drift_minutes, key=lambda pm: pm["median"])
        problems.append(f"per-minute drift: minute {worst['minute']}:00 median "
                        f"{worst['median']:+.3f}s > +{FAIL_SEGMENT_DRIFT:.2f}s "
                        f"({len(drift_minutes)} late minute(s))")
    if fword_ends:
        ex = ", ".join(f"#{n} ...{w!r}" for n, w, _ln in dangling[:5])
        problems.append(f"{fword_ends} mid-phrase dangling break(s): {ex}")
    if matched_frac < MIN_MATCHED_FRACTION:
        problems.append(f"only {matched}/{total} cues matched ground-truth "
                        f"({matched_frac*100:.0f}% < {MIN_MATCHED_FRACTION*100:.0f}%): "
                        f"low-confidence measurement")

    ok = not problems
    return {
        "check": "caption_sync",
        "ok": ok,
        "reason": ("timing on-word; segmentation clean" if ok
                   else "; ".join(problems)),
        "srt": str(srt_path),
        "master": str(master_path),
        "reliability": reliability,
        "total_cues": total,
        "matched": matched,
        "lag_p50": lag_p50,
        "lag_p75": lag_p75,
        "lag_p90": lag_p90,
        "exact_pct": exact_pct,
        "late_pct": late_pct,
        "lead_pct": lead_pct,
        "segment_drift": segment_drift,
        "function_word_line_ends": fword_ends,
        "dangling": dangling,
        "per_minute": per_minute,
        "problems": problems,
    }


# ---------------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP/ERROR] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print(f"CAPTION SYNC REPORT  ({r['reliability']} ground-truth)")
    print("=" * 78)
    print(f"  srt          : {r['srt']}")
    print(f"  master       : {r['master']}")
    print(f"  cues matched : {r['matched']}/{r['total_cues']} "
          f"({_pct(r['matched'], r['total_cues']):.0f}%)")
    print("  lag = cue_start - true_onset   (POSITIVE = caption LATE; negative = leads/early)")
    print(f"  median lag   : {r['lag_p50']:+.3f}s   p75 {r['lag_p75']:+.3f}s   "
          f"p90 {r['lag_p90']:+.3f}s")
    print(f"  on-word (|lag|<= {EXACT_TOL:.2f}s): {r['exact_pct']:.0f}%    "
          f"leads (< -{EXACT_TOL:.2f}s): {r['lead_pct']:.0f}%    "
          f"LATE (> +{LATE_TOL:.2f}s): {r['late_pct']:.0f}%")
    print(f"  segmentation : {r['function_word_line_ends']} mid-phrase dangling break(s)")
    print("\n  per-minute median lag (exposes progressive drift / a late-worsening back half):")
    print("    minute |   n | median lag")
    print("    -------+-----+-----------")
    for pm in r["per_minute"]:
        flag = "  <-- DRIFT" if pm["median"] > FAIL_SEGMENT_DRIFT else ""
        print(f"    {pm['minute']:>4}:00 | {pm['n']:>3} | {pm['median']:+8.3f}s{flag}")
    if r.get("dangling"):
        print("\n  dangling cue endings (mid-phrase cut on a function word, no punctuation):")
        for n, w, ln in r["dangling"][:10]:
            print(f"    cue #{n}: ...ends on {w!r}   line={ln!r}")
    print("\n" + "-" * 78)
    if r["ok"]:
        print("  RESULT: PASS  — captions sit on/just-before the spoken word; no drift; clean breaks")
    else:
        print("  RESULT: FAIL")
        for p in r["problems"]:
            print(f"    - {p}")
    print("-" * 78)


def main(argv: Optional[list[str]] = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(
        description="Independent caption-sync gate: FAIL if captions lag/drift or break mid-phrase.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug")
    ap.add_argument("--srt", default=None,
                    help="override SRT path (default 08_edit/captions.final.v001.srt)")
    ap.add_argument("--master", default=None, help="override narration master audio path")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help="faster-whisper model for ground truth (medium.en matches the producer)")
    ap.add_argument("--no-cache", action="store_true",
                    help="do not reuse/write the cached ground-truth transcription")
    ap.add_argument("--json", action="store_true", help="also print the raw result dict as JSON")
    args = ap.parse_args(argv)

    ep_dir = ROOT / "episodes" / args.ep
    if not ep_dir.exists():
        print(f"[ERROR] episode dir not found: {ep_dir}")
        return 2

    r = evaluate(ep_dir, srt=args.srt, master=args.master, model_name=args.model,
                 use_cache=not args.no_cache)
    _print_report(r)
    if args.json:
        printable = {k: v for k, v in r.items() if k != "dangling"}
        print(json.dumps(printable, indent=2, default=str))

    if r.get("skipped"):
        return 3  # could not measure (missing file / no match) -> non-zero, clear message above
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
