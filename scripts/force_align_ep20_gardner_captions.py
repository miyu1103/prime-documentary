#!/usr/bin/env python3
"""Force-align EP20 captions to the actual ElevenLabs narration master."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-020-gardner"
EPDIR = ROOT / "episodes" / EP
AUDIO = Path("H:/pd-media/episodes/PD-2026-020-gardner/06_audio/master_elevenlabs_v001/voice_master.v001.wav")
NARRATION_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
REVISION = "v003"
CAPTIONS_SRT = EPDIR / "08_edit" / f"captions.{REVISION}.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / f"captions.{REVISION}.json"
CAPTIONS_QC = EPDIR / "08_edit" / f"captions.{REVISION}.qc.json"
WORDS_CACHE = EPDIR / "08_edit" / "whisper_words.v001.json"
MAX_TOTAL_CHARS = 78
MAX_WORDS = 14
MAX_CHARS = 42
MIN_DUR = 1.0
MAX_DUR = 6.0
MAX_CPS = 17.0
MIN_GAP = 2 / 30


def norm_word(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def norm_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def srt_ts(t: float) -> str:
    ms = max(0, int(round(t * 1000)))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def load_rows() -> list[dict[str, Any]]:
    rows = json.loads(NARRATION_INDEX.read_text(encoding="utf-8"))["chunks"]
    if len(rows) != 73:
        raise RuntimeError(f"expected 73 narration chunks, got {len(rows)}")
    return rows


def transcribe_words() -> list[dict[str, Any]]:
    from faster_whisper import WhisperModel

    if WORDS_CACHE.exists():
        data = json.loads(WORDS_CACHE.read_text(encoding="utf-8"))
        words = data.get("words", [])
        if words:
            print(f"using cached whisper_words={len(words)}", flush=True)
            return words
    if not AUDIO.exists():
        raise FileNotFoundError(AUDIO)
    print("loading faster-whisper small.en cpu/int8", flush=True)
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segments, _info = model.transcribe(str(AUDIO), word_timestamps=True, vad_filter=False, beam_size=5, language="en")
    words: list[dict[str, Any]] = []
    for segment in segments:
        for word in segment.words or []:
            text = word.word.strip()
            n = norm_word(text)
            if n:
                words.append({"word": text, "norm": n, "start": float(word.start), "end": float(word.end)})
    print(f"whisper_words={len(words)}", flush=True)
    WORDS_CACHE.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "source_audio": str(AUDIO).replace("\\", "/"),
                "method": "faster-whisper small.en word_timestamps",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "words": words,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return words


def fit_two_lines(tokens: list[str]) -> str:
    one = " ".join(tokens)
    if len(one) <= MAX_CHARS:
        return one
    best: tuple[int, int] | None = None
    for i in range(1, len(tokens)):
        a = " ".join(tokens[:i])
        b = " ".join(tokens[i:])
        if len(a) <= MAX_CHARS and len(b) <= MAX_CHARS:
            score = abs(len(a) - len(b))
            if best is None or score < best[0]:
                best = (score, i)
    if best:
        i = best[1]
        return " ".join(tokens[:i]) + "\n" + " ".join(tokens[i:])

    # Fallback for rare long clauses: keep the first line legal and let the
    # greedy breath-group splitter shorten subsequent cues.
    cur: list[str] = []
    rest: list[str] = []
    for token in tokens:
        trial = " ".join(cur + [token])
        if cur and len(trial) > MAX_CHARS:
            rest.append(token)
        elif rest:
            rest.append(token)
        else:
            cur.append(token)
    return " ".join(cur) + ("\n" + " ".join(rest) if rest else "")


def split_breath_groups(tokens: list[str], word_times: list[tuple[float, float]]) -> list[tuple[list[str], int, int]]:
    groups: list[tuple[list[str], int, int]] = []
    start = 0
    n = len(tokens)
    while start < n:
        best_break: int | None = None
        best_score = -1.0
        end = start
        while end < n:
            seg = tokens[start : end + 1]
            text = " ".join(seg)
            dur = max(0.05, word_times[end][1] - word_times[start][0])
            chars = len(text)
            words = len(seg)
            if end > start:
                prev_gap = max(0.0, word_times[end][0] - word_times[end - 1][1])
            else:
                prev_gap = 0.0

            over = (
                chars > MAX_TOTAL_CHARS
                or words > MAX_WORDS
                or dur > MAX_DUR - 0.15
                or (dur > 0 and chars / dur > MAX_CPS and words >= 5)
                or any(len(line) > MAX_CHARS for line in fit_two_lines(seg).split("\n"))
            )
            if over:
                cut = best_break if best_break is not None and best_break >= start else max(start, end - 1)
                groups.append((tokens[start : cut + 1], start, cut))
                start = cut + 1
                break

            gap_after = max(0.0, word_times[end + 1][0] - word_times[end][1]) if end + 1 < n else 0.0
            terminal = bool(re.search(r"[.?!]$", tokens[end]))
            comma = tokens[end].endswith(",")
            dash = tokens[end].endswith("—") or tokens[end] == "—"
            min_readable = dur >= MIN_DUR and chars >= 12

            score = -1.0
            if min_readable and gap_after >= 0.42:
                score = 100 + gap_after
            elif min_readable and terminal and gap_after >= 0.18:
                score = 85 + gap_after
            elif min_readable and gap_after >= 0.30:
                score = 75 + gap_after
            elif min_readable and (comma or dash) and gap_after >= 0.16 and words >= 5:
                score = 55 + gap_after
            elif min_readable and terminal and words >= 5:
                score = 42

            if score > best_score:
                best_score = score
                best_break = end

            natural_stop = min_readable and (
                gap_after >= 0.48
                or (terminal and gap_after >= 0.22)
                or (words >= 10 and gap_after >= 0.30)
            )
            if natural_stop:
                groups.append((seg, start, end))
                start = end + 1
                break

            end += 1
        else:
            groups.append((tokens[start:n], start, n - 1))
            start = n
    return groups


def merge_orphan_cues(cues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = cues
    for _ in range(2):
        out: list[dict[str, Any]] = []
        for cue in merged:
            if not out:
                out.append(cue)
                continue
            prev = out[-1]
            if prev.get("span_id") != cue.get("span_id"):
                out.append(cue)
                continue
            prev_text = str(prev["text"]).replace("\n", " ")
            cur_text = str(cue["text"]).replace("\n", " ")
            combined_tokens = (prev_text + " " + cur_text).split()
            combined = fit_two_lines(combined_tokens)
            dur = float(cue["end"]) - float(prev["start"])
            chars = len(combined.replace("\n", ""))
            gap = float(cue["start"]) - float(prev["end"])
            prev_small = len(prev_text.split()) <= 5 or len(prev_text) <= 24
            cur_small = len(cur_text.split()) <= 5 or len(cur_text) <= 24
            can_merge = (
                (prev_small or cur_small or gap <= 0.25)
                and chars <= MAX_TOTAL_CHARS
                and dur <= MAX_DUR
                and dur > 0
                and chars / dur <= MAX_CPS
                and len(combined.split("\n")) <= 2
                and all(len(line) <= MAX_CHARS for line in combined.split("\n"))
            )
            if can_merge:
                prev["text"] = combined
                prev["end"] = cue["end"]
            else:
                out.append(cue)
        merged = out
    for i, cue in enumerate(merged, 1):
        cue["index"] = i
    return merged


def align_chunk(row: dict[str, Any], whisper_words: list[dict[str, Any]]) -> list[tuple[float, float]]:
    tokens = row["text"].split()
    start = float(row["voice_start"])
    end = float(row["voice_end"])
    centers = [w for w in whisper_words if start - 0.45 <= (w["start"] + w["end"]) / 2 <= end + 0.45]
    times: list[tuple[float, float] | None] = [None] * len(tokens)
    wi = 0
    for ti, token in enumerate(tokens):
        target = norm_word(token)
        if not target:
            continue
        found = None
        for offset in range(0, 8):
            idx = wi + offset
            if idx >= len(centers):
                break
            candidate = centers[idx]["norm"]
            prefix = target[: max(3, min(5, len(target)))]
            cp = candidate[: max(3, min(5, len(candidate)))]
            if candidate == target or candidate.startswith(prefix) or target.startswith(cp):
                found = idx
                break
        if found is None and wi < len(centers):
            found = wi
        if found is not None:
            w = centers[found]
            times[ti] = (max(start, float(w["start"])), min(end, float(w["end"])))
            wi = found + 1
    for ti, value in enumerate(times):
        if value is None:
            frac = (ti + 0.5) / max(1, len(tokens))
            t = start + frac * max(0.5, end - start)
            times[ti] = (t, min(end, t + 0.24))
    return [t for t in times if t is not None]


def build_cues(rows: list[dict[str, Any]], whisper_words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cues: list[dict[str, Any]] = []
    idx = 1
    for row in rows:
        tokens = row["text"].split()
        word_times = align_chunk(row, whisper_words)
        for seg_tokens, start_i, end_i in split_breath_groups(tokens, word_times):
            start = word_times[start_i][0]
            end = min(float(row["voice_end"]) + 0.18, word_times[end_i][1] + 0.16)
            line = fit_two_lines(seg_tokens)
            cues.append({"index": idx, "start": round(start, 3), "end": round(end, 3), "text": line, "span_id": row["span_id"]})
            idx += 1
    cues = merge_orphan_cues(cues)
    fixed: list[dict[str, Any]] = []
    previous_end = 0.0
    for cue in cues:
        cue["start"] = max(float(cue["start"]), previous_end + (MIN_GAP if fixed else 0.0))
        chars = len(str(cue["text"]).replace("\n", ""))
        readable_dur = min(MAX_DUR, max(MIN_DUR + 0.02, chars / 16.8))
        cue["end"] = max(float(cue["end"]), cue["start"] + readable_dur)
        cue["end"] = min(float(cue["end"]), cue["start"] + MAX_DUR)
        cue["start"] = round(cue["start"], 3)
        cue["end"] = round(cue["end"], 3)
        previous_end = cue["end"]
        fixed.append(cue)
    if fixed:
        final_target = min(float(rows[-1]["voice_end"]) + 1.95, float(fixed[-1]["start"]) + MAX_DUR)
        if final_target > float(fixed[-1]["end"]):
            fixed[-1]["end"] = round(final_target, 3)
    return fixed


def qc(rows: list[dict[str, Any]], cues: list[dict[str, Any]]) -> dict[str, Any]:
    script_text = " ".join(row["text"] for row in rows)
    caption_text = " ".join(cue["text"] for cue in cues)
    violations: list[str] = []
    for cue in cues:
        lines = cue["text"].split("\n")
        dur = float(cue["end"]) - float(cue["start"])
        chars = len(cue["text"].replace("\n", ""))
        if len(lines) > 2:
            violations.append("too_many_lines")
        if any(len(line) > MAX_CHARS for line in lines):
            violations.append("line_too_long")
        if dur < MIN_DUR or dur > MAX_DUR:
            violations.append("duration")
        if dur > 0 and chars / dur > MAX_CPS:
            violations.append("cps")
    overlaps = sum(1 for prev, cur in zip(cues, cues[1:]) if float(cur["start"]) < float(prev["end"]) + MIN_GAP - 0.001)
    return {
        "episode_id": EP,
        "revision": REVISION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_audio": str(AUDIO).replace("\\", "/"),
        "method": "faster-whisper-small.en-word-timestamps aligned to locked VO text; breath-gap grouped",
        "cue_count": len(cues),
        "last_caption_end": cues[-1]["end"] if cues else 0,
        "text_exact_match_to_script": norm_text(script_text) == norm_text(caption_text),
        "script_words": len(script_text.split()),
        "caption_words": len(caption_text.split()),
        "overlap_or_gap_violations": overlaps,
        "format_violations": len(violations),
        "qc_status": "pass" if norm_text(script_text) == norm_text(caption_text) and overlaps == 0 and not violations else "review",
    }


def write_outputs(rows: list[dict[str, Any]], cues: list[dict[str, Any]]) -> dict[str, Any]:
    CAPTIONS_SRT.write_text(
        "\n".join(f"{c['index']}\n{srt_ts(c['start'])} --> {srt_ts(c['end'])}\n{c['text']}\n" for c in cues),
        encoding="utf-8",
    )
    CAPTIONS_JSON.write_text(
        json.dumps({"episode_id": EP, "revision": REVISION, "alignment_method": "faster-whisper-small.en-word-timestamps aligned to locked VO text; breath-gap grouped", "cues": cues}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    report = qc(rows, cues)
    CAPTIONS_QC.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)
    return report


def main() -> int:
    rows = load_rows()
    words = transcribe_words()
    cues = build_cues(rows, words)
    report = write_outputs(rows, cues)
    return 0 if report["qc_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
