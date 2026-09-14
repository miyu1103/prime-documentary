#!/usr/bin/env python3
r"""Independent caption-COVERAGE gate — catches SKIPPED / DROPPED captions before they ship.

verify_caption_sync.py measures caption TIMING (are cues on the spoken word, or late/drifting?).
It does NOT notice when a whole line of narration has NO caption at all: a cue that was dropped,
merged away, or truncated leaves a silent stretch of speech with nothing on screen. That is the
owner's recurring "字幕とナレが一致しない / 字幕が抜けている" defect, and a timing gate can pass
with a caption simply missing. This gate is the COMPLEMENT: it measures COVERAGE.

Method (no audio, no transcription — purely geometric and therefore deterministic):
  * narration_index.v00N.json gives every spoken chunk's own [start, end] window in the master
    (drift-free ground truth for WHERE speech is — the same windows the sync gate trusts).
  * The .srt gives the caption cue intervals actually shown on screen.
  * For each narration chunk we intersect every cue with the chunk window, take the UNION of those
    clipped intervals, and divide by the chunk's duration -> caption_time_coverage in [0, 1].
  * A chunk whose coverage falls below MIN_COVERAGE (~80%) has a dropped/skipped caption: a real
    span of narration is playing with no words on screen. We FAIL and report every such chunk.
  * We also FAIL if the .srt ends more than TAIL_MAX_GAP seconds before the last narration chunk
    ends — the classic "captions stop before the video does" truncation.

Natural sentence-boundary pauses inside a chunk are silence, so healthy chunks sit around 82-90%
coverage, not 100%; the ~80% floor is below that band yet a single dropped ~1.5-3 s cue in a
16-30 s chunk removes ~8-15 points and trips it. We do NOT lower the floor to make an episode pass.

Usage:
  py -3.11 scripts/verify_caption_coverage.py --ep PD-2026-031-unlock
  py -3.11 scripts/verify_caption_coverage.py --ep PD-2026-031-unlock --dry-run
  py -3.11 scripts/verify_caption_coverage.py --ep PD-2026-031-unlock --json out.json
  py -3.11 scripts/verify_caption_coverage.py --selftest

Exit code 0 = PASS or --dry-run (or honest SKIP when the artifact is absent, e.g. on the SSD);
1 = FAIL or a usage error. Read-only: it never writes into the episode. evaluate(epdir) returns a
dict compatible with check_final_acceptance (keys: check, ok, hard, reason, [skipped], plus numbers).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-031-unlock"

# --- PASS/FAIL thresholds -----------------------------------------------------------------------
# Fraction of a narration chunk's [start,end] window that must be covered by caption cues. Below
# this, a caption was dropped/skipped and speech plays with nothing on screen. Healthy chunks run
# ~0.82-0.90 (sentence-boundary silence is uncovered by design); 0.80 sits just under that band.
MIN_COVERAGE = 0.80
# The .srt may not end more than this many seconds before the LAST narration chunk ends, or the
# captions were truncated (they stop before the video does).
TAIL_MAX_GAP = 2.0
EPS = 1e-6

_TS = re.compile(r"(\d\d):(\d\d):(\d\d)[,.](\d{1,3})\s*-->\s*(\d\d):(\d\d):(\d\d)[,.](\d{1,3})")


def _ts_to_seconds(h: str, m: str, s: str, ms: str) -> float:
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def parse_srt_intervals(path: Path) -> list[tuple[float, float]]:
    """Return caption cue [start, end] intervals (seconds), in file order, from an .srt.

    Only the timestamps matter for coverage, so we scan every ``-->`` line directly and ignore the
    text bodies. Malformed / zero-length cues are dropped.
    """
    text = path.read_text(encoding="utf-8", errors="ignore")
    out: list[tuple[float, float]] = []
    for m in _TS.finditer(text):
        start = _ts_to_seconds(m[1], m[2], m[3], m[4])
        end = _ts_to_seconds(m[5], m[6], m[7], m[8])
        if end > start:
            out.append((start, end))
    return out


def resolve_srt(ep_dir: Path, override: Optional[str]) -> Path:
    """Locate the shipped caption .srt (mirrors verify_caption_sync.resolve_srt).

    Prefers 08_edit/captions.final.v001.srt, then the highest captions.final.v*.srt, then any
    non-proxy .srt whose last cue ends latest. Returns the default path (which may not exist) when
    nothing is found, so the caller can report a clear SKIP.
    """
    if override:
        return Path(override)
    edit = ep_dir / "08_edit"
    default = edit / "captions.final.v001.srt"
    if default.exists():
        return default
    finals = sorted(edit.glob("captions.final.v*.srt"))
    if finals:
        return finals[-1]
    others = [p for p in edit.glob("*.srt")
              if "review_proxy" not in p.name and p.stat().st_size > 0]
    if others:
        def _last_end(p: Path) -> float:
            ends = _TS.findall(p.read_text("utf-8", errors="ignore"))
            return max((_ts_to_seconds(e[4], e[5], e[6], e[7]) for e in ends), default=0.0)
        return max(others, key=_last_end)
    return default


def resolve_index(ep_dir: Path, override: Optional[str]) -> Path:
    """Locate the narration index carrying per-chunk [start,end] windows.

    Prefers the highest narration_index.v*.json under 06_audio (they share identical windows here;
    the highest revision is the current one). Returns the v001 default path when none is found.
    """
    if override:
        return Path(override)
    audio = ep_dir / "06_audio"
    cands = sorted(audio.glob("narration_index.v*.json"))
    if cands:
        return cands[-1]
    return audio / "narration_index.v001.json"


def load_windows(index_path: Path) -> list[dict[str, Any]]:
    """Return spoken-order chunk descriptors [{chunk_id, section, start, end, dur}] with valid
    numeric windows, or [] if the index is absent/malformed/window-less."""
    if not index_path.exists():
        return []
    try:
        chunks = (json.loads(index_path.read_text("utf-8")) or {}).get("chunks", [])
    except Exception:  # noqa: BLE001 - malformed index -> no windows (caller SKIPs honestly)
        return []
    out: list[dict[str, Any]] = []
    for c in chunks:
        s, e = c.get("start"), c.get("end")
        if isinstance(s, (int, float)) and isinstance(e, (int, float)) and e > s:
            out.append({
                "chunk_id": c.get("chunk_id", "?"),
                "section": c.get("section", ""),
                "start": float(s),
                "end": float(e),
                "dur": float(e) - float(s),
            })
    return out


def covered_seconds(window: tuple[float, float], cues: list[tuple[float, float]]) -> float:
    """Union length (seconds) of the caption cues intersected with ``window`` = [ws, we]."""
    ws, we = window
    clipped: list[tuple[float, float]] = []
    for cs, ce in cues:
        a = max(cs, ws)
        b = min(ce, we)
        if b > a:
            clipped.append((a, b))
    if not clipped:
        return 0.0
    clipped.sort()
    total = 0.0
    cur_start, cur_end = clipped[0]
    for a, b in clipped[1:]:
        if a > cur_end:
            total += cur_end - cur_start
            cur_start, cur_end = a, b
        elif b > cur_end:
            cur_end = b
    total += cur_end - cur_start
    return total


# ---------------------------------------------------------------------------------------------
# core evaluation (importable by check_final_acceptance)
# ---------------------------------------------------------------------------------------------

def evaluate(epdir: Path, srt: Optional[str] = None, index: Optional[str] = None) -> dict[str, Any]:
    """Measure per-chunk caption coverage and tail truncation. Never raises, never sys.exit.

    Returns a dict compatible with check_final_acceptance:
      {check, ok, hard, reason, [skipped], min_coverage, min_coverage_chunk, tail_gap,
       total_chunks, uncovered_chunks, uncovered, srt, index}
    A missing artifact (e.g. media on the SSD) yields {"ok": True, "hard": False, "skipped": True}.
    """
    epdir = Path(epdir)
    srt_path = resolve_srt(epdir, srt)
    index_path = resolve_index(epdir, index)

    if not index_path.exists():
        return {"check": "caption_coverage", "ok": True, "hard": False, "skipped": True,
                "reason": f"narration index not found (nothing to measure): {index_path}"}
    windows = load_windows(index_path)
    if not windows:
        return {"check": "caption_coverage", "ok": True, "hard": False, "skipped": True,
                "reason": f"no usable narration windows in {index_path}"}
    if not srt_path.exists():
        return {"check": "caption_coverage", "ok": True, "hard": False, "skipped": True,
                "reason": f"caption .srt not found (nothing to measure): {srt_path}"}
    cues = parse_srt_intervals(srt_path)
    if not cues:
        # SRT present but empty/unparseable while narration exists => a real, hard coverage failure.
        return {"check": "caption_coverage", "ok": False, "hard": True,
                "reason": f"0 caption cues parsed from {srt_path} but {len(windows)} narration "
                          f"chunk(s) exist (captions entirely missing)",
                "total_chunks": len(windows), "uncovered_chunks": len(windows),
                "min_coverage": 0.0, "srt": str(srt_path), "index": str(index_path)}

    uncovered: list[dict[str, Any]] = []
    min_cov = 1.0
    min_cov_chunk = ""
    for w in windows:
        cov_s = covered_seconds((w["start"], w["end"]), cues)
        ratio = cov_s / w["dur"] if w["dur"] > 0 else 0.0
        if ratio < min_cov:
            min_cov = ratio
            min_cov_chunk = w["chunk_id"]
        if ratio < MIN_COVERAGE - EPS:
            uncovered.append({
                "chunk_id": w["chunk_id"],
                "section": w["section"],
                "start": round(w["start"], 3),
                "end": round(w["end"], 3),
                "coverage": round(ratio, 4),
                "covered_sec": round(cov_s, 3),
                "dur_sec": round(w["dur"], 3),
            })

    srt_end = max(e for _, e in cues)
    last_narr_end = max(w["end"] for w in windows)
    tail_gap = last_narr_end - srt_end  # positive => srt stops before narration ends

    problems: list[str] = []
    if uncovered:
        ex = ", ".join(f"{u['chunk_id']}({u['coverage']*100:.0f}%)" for u in uncovered[:6])
        problems.append(f"{len(uncovered)}/{len(windows)} narration chunk(s) below "
                        f"{MIN_COVERAGE*100:.0f}% caption coverage (dropped/skipped captions): {ex}")
    if tail_gap > TAIL_MAX_GAP + EPS:
        problems.append(f"captions end {tail_gap:.2f}s before the last narration chunk "
                        f"(srt ends {srt_end:.2f}s, narration ends {last_narr_end:.2f}s > "
                        f"{TAIL_MAX_GAP:.1f}s tolerance)")

    ok = not problems
    return {
        "check": "caption_coverage",
        "ok": ok,
        "hard": True,
        "reason": ("every narration chunk is captioned; no dropped captions" if ok
                   else "; ".join(problems)),
        "srt": str(srt_path),
        "index": str(index_path),
        "total_chunks": len(windows),
        "uncovered_chunks": len(uncovered),
        "min_coverage": round(min_cov, 4),
        "min_coverage_chunk": min_cov_chunk,
        "tail_gap": round(tail_gap, 3),
        "srt_end": round(srt_end, 3),
        "narration_end": round(last_narr_end, 3),
        "uncovered": uncovered,
    }


# ---------------------------------------------------------------------------------------------
# reporting
# ---------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] caption_coverage: {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("CAPTION COVERAGE REPORT  (per-chunk caption-time coverage; no audio needed)")
    print("=" * 78)
    print(f"  srt          : {r.get('srt')}")
    print(f"  index        : {r.get('index')}")
    print(f"  chunks       : {r.get('total_chunks')}")
    print(f"  min coverage : {r.get('min_coverage', 0.0)*100:.1f}%  "
          f"(chunk {r.get('min_coverage_chunk', '?')})   floor {MIN_COVERAGE*100:.0f}%")
    print(f"  tail gap     : {r.get('tail_gap', 0.0):+.2f}s  "
          f"(srt_end {r.get('srt_end', 0.0):.2f}s vs narration_end {r.get('narration_end', 0.0):.2f}s; "
          f"tolerance {TAIL_MAX_GAP:.1f}s)")
    uncovered = r.get("uncovered", [])
    if uncovered:
        print(f"\n  UNCOVERED chunks ({len(uncovered)}) — narration playing with no caption:")
        print("    chunk    | section | window            | coverage")
        print("    ---------+---------+-------------------+---------")
        for u in uncovered[:20]:
            print(f"    {u['chunk_id']:<8} | {u['section']:<7} | "
                  f"{u['start']:7.2f}-{u['end']:7.2f} | {u['coverage']*100:5.1f}% "
                  f"({u['covered_sec']:.1f}/{u['dur_sec']:.1f}s)")
    print("\n" + "-" * 78)
    if r.get("ok"):
        print("  RESULT: PASS  — every narration chunk is captioned above the coverage floor")
    else:
        print("  RESULT: FAIL")
        for p in str(r.get("reason", "")).split("; "):
            print(f"    - {p}")
    print("-" * 78)


def _atomic_write_json(path: Path, obj: dict[str, Any]) -> None:
    """Write ``obj`` as JSON atomically (temp file in the same dir, then os.replace)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=2, default=str)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------------------------------------
# self-test: RED fixture (must fail) + real-episode probe
# ---------------------------------------------------------------------------------------------

def _selftest(real_ep: str) -> int:
    """Prove the gate can FAIL, then print the real episode's actual numbers.

    RED fixture: three 10 s narration chunks; the .srt fully captions chunks A and C but SKIPS
    chunk B entirely (a dropped caption). A correct coverage gate must report ok=False.
    """
    print("=" * 78)
    print("SELFTEST — RED FIXTURE (a known-bad input the gate MUST reject)")
    print("=" * 78)
    with tempfile.TemporaryDirectory() as td:
        ep = Path(td) / "PD-9999-999-redfixture"
        (ep / "06_audio").mkdir(parents=True)
        (ep / "08_edit").mkdir(parents=True)
        index = {
            "episode_id": "PD-9999-999-redfixture",
            "chunks": [
                {"chunk_id": "VC-0001", "section": "HOOK", "start": 0.0, "end": 10.0},
                {"chunk_id": "VC-0002", "section": "BODY", "start": 10.0, "end": 20.0},
                {"chunk_id": "VC-0003", "section": "BODY", "start": 20.0, "end": 30.0},
            ],
        }
        (ep / "06_audio" / "narration_index.v001.json").write_text(
            json.dumps(index), encoding="utf-8")
        # Captions for A (0-9) and C (20-29) only. Chunk B (10-20) gets NO cue -> 0% coverage.
        srt = (
            "1\n00:00:00,000 --> 00:00:09,000\nchunk A is captioned\n\n"
            "2\n00:00:20,000 --> 00:00:29,000\nchunk C is captioned\n"
        )
        (ep / "08_edit" / "captions.final.v001.srt").write_text(srt, encoding="utf-8")

        red = evaluate(ep)
        _print_report(red)
        red_ok = red.get("ok") is False and not red.get("skipped")
        b = next((u for u in red.get("uncovered", []) if u["chunk_id"] == "VC-0002"), None)
        red_ok = red_ok and b is not None and b["coverage"] == 0.0
        print(f"\nRED-FIXTURE: {'PASS' if red_ok else 'FAIL'} "
              f"(gate reported ok={red.get('ok')}, uncovered_chunks={red.get('uncovered_chunks')})")

    print("\n" + "=" * 78)
    print(f"SELFTEST — REAL EPISODE PROBE ({real_ep})")
    print("=" * 78)
    real = evaluate(ROOT / "episodes" / real_ep)
    _print_report(real)
    return 0 if red_ok else 1


# ---------------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------------

def main(argv: Optional[list[str]] = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(
        description="Independent caption-COVERAGE gate: FAIL if any narration chunk is under-"
                    "captioned (dropped cue) or the srt ends before the narration.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug")
    ap.add_argument("--srt", default=None, help="override caption .srt path")
    ap.add_argument("--index", default=None, help="override narration_index.v*.json path")
    ap.add_argument("--dry-run", action="store_true",
                    help="measure and print, write no --json file, always exit 0")
    ap.add_argument("--json", default=None, help="atomically write the result dict to this path")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED fixture (must fail) then probe the real episode")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest(args.ep)

    ep_dir = ROOT / "episodes" / args.ep
    if not ep_dir.exists():
        print(f"[ERROR] episode dir not found: {ep_dir}")
        return 1

    r = evaluate(ep_dir, srt=args.srt, index=args.index)
    _print_report(r)

    if args.json and not args.dry_run:
        _atomic_write_json(Path(args.json), r)
        print(f"\n  wrote {args.json}")

    if args.dry_run:
        return 0
    if r.get("skipped"):
        return 0  # honest skip (hard=False): nothing to measure, not a failure
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
