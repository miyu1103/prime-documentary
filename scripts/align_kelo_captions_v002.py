"""Forced-align Kelo captions to the fitted narration and write v002 captions.

The locked script text is preserved. Only cue timing and line wrapping change.
"""
from __future__ import annotations

import difflib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from faster_whisper import WhisperModel


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-010-kelo"
EPDIR = ROOT / "episodes" / EP
SCRIPT = EPDIR / "03_script" / "script.en.v001.md"
VOICE = Path(r"H:\pd-media\episodes\PD-2026-010-kelo\06_voice\master\vc_master_v001_fit_631s.wav")
OUT_SRT = EPDIR / "08_edit" / "captions.v002.srt"
OUT_JSON = EPDIR / "08_edit" / "captions.v002.json"
OUT_META = EPDIR / "06_audio" / "caption_alignment.v002.json"
OUT_TS = ROOT / "remotion" / "src" / "data" / "kelo_captions.ts"


@dataclass
class Token:
    raw: str
    norm: str
    start: float | None = None
    end: float | None = None


def clean_vo(line: str) -> str:
    text = re.sub(r"^\[VO:\]\s*", "", line.strip())
    text = re.sub(r"\s*(?:\[CLM-[0-9]{4}\]\s*)+", ". ", text)
    text = re.sub(r"([.?!])\s*\.", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def script_text() -> str:
    chunks = [clean_vo(line) for line in SCRIPT.read_text("utf-8").splitlines() if line.strip().startswith("[VO:]")]
    if not chunks:
        raise RuntimeError("No [VO:] chunks found")
    return " ".join(chunks)


def norm_word(word: str) -> str:
    word = word.lower().replace("’", "'")
    word = re.sub(r"^['\"“”‘’]+|['\"“”‘’]+$", "", word)
    word = re.sub(r"[^a-z0-9']+", "", word)
    aliases = {
        "kilo": "kelo",
        "kelos": "kelo",
        "takings": "taking",
        "condemnations": "condemnation",
    }
    return aliases.get(word, word)


def tokenize(text: str) -> list[Token]:
    tokens: list[Token] = []
    for raw in re.findall(r"[A-Za-z0-9][A-Za-z0-9'’.-]*|[—–-]", text):
        n = norm_word(raw)
        if n:
            tokens.append(Token(raw=raw, norm=n))
    return tokens


def transcribe_words() -> list[Token]:
    if not VOICE.exists():
        raise FileNotFoundError(VOICE)
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        str(VOICE),
        language="en",
        beam_size=5,
        word_timestamps=True,
        vad_filter=False,
        condition_on_previous_text=True,
    )
    words: list[Token] = []
    for segment in segments:
        for word in segment.words or []:
            n = norm_word(word.word)
            if not n:
                continue
            words.append(Token(raw=word.word.strip(), norm=n, start=float(word.start), end=float(word.end)))
    if not words:
        raise RuntimeError("Whisper produced no word timestamps")
    return words


def align(script_tokens: list[Token], heard_tokens: list[Token]) -> dict[str, int | float]:
    script_norm = [t.norm for t in script_tokens]
    heard_norm = [t.norm for t in heard_tokens]
    matcher = difflib.SequenceMatcher(None, script_norm, heard_norm, autojunk=False)
    matched = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for si, hj in zip(range(i1, i2), range(j1, j2)):
                script_tokens[si].start = heard_tokens[hj].start
                script_tokens[si].end = heard_tokens[hj].end
                matched += 1
        elif tag == "replace" and (i2 - i1) == (j2 - j1):
            for si, hj in zip(range(i1, i2), range(j1, j2)):
                ratio = difflib.SequenceMatcher(None, script_norm[si], heard_norm[hj]).ratio()
                if ratio >= 0.72:
                    script_tokens[si].start = heard_tokens[hj].start
                    script_tokens[si].end = heard_tokens[hj].end
                    matched += 1

    known = [i for i, token in enumerate(script_tokens) if token.start is not None and token.end is not None]
    if not known:
        raise RuntimeError("No script words matched transcription")

    first = known[0]
    for i in range(0, first):
        width = max(0.16, (script_tokens[first].start or 0.0) / max(1, first + 1))
        script_tokens[i].start = max(0.0, (script_tokens[first].start or 0.0) - width * (first - i))
        script_tokens[i].end = min(script_tokens[first].start or 0.0, script_tokens[i].start + width * 0.82)

    last_known = known[-1]
    for i in range(last_known + 1, len(script_tokens)):
        prev_end = script_tokens[i - 1].end or 0.0
        script_tokens[i].start = prev_end + 0.035
        script_tokens[i].end = script_tokens[i].start + 0.22

    known = [i for i, token in enumerate(script_tokens) if token.start is not None and token.end is not None]
    for left, right in zip(known, known[1:]):
        if right - left <= 1:
            continue
        left_end = script_tokens[left].end or 0.0
        right_start = script_tokens[right].start or left_end
        gap = max(0.02, right_start - left_end)
        missing = right - left - 1
        slot = gap / (missing + 1)
        for offset, si in enumerate(range(left + 1, right), start=1):
            start = left_end + slot * (offset - 0.5)
            script_tokens[si].start = start
            script_tokens[si].end = min(right_start, start + max(0.12, slot * 0.75))

    prev_end = 0.0
    for token in script_tokens:
        token.start = max(prev_end, float(token.start or prev_end))
        token.end = max(token.start + 0.08, float(token.end or token.start + 0.18))
        prev_end = token.end
    return {"script_words": len(script_tokens), "heard_words": len(heard_tokens), "matched_words": matched, "match_ratio": round(matched / len(script_tokens), 4)}


def cue_plain(tokens: list[Token]) -> str:
    text = " ".join(token.raw for token in tokens)
    text = re.sub(r"\s+([,.;:?!])", r"\1", text)
    text = re.sub(r"\s+(['’])s\b", r"\1s", text)
    text = text.replace(" — ", " - ")
    return text


def wrap_two_lines(text: str) -> str:
    if len(text) <= 42:
        return text
    words = text.split()
    best: tuple[int, int] | None = None
    for i in range(1, len(words)):
        left = " ".join(words[:i])
        right = " ".join(words[i:])
        if len(left) > 42 or len(right) > 42 or len(right) < 8:
            continue
        score = abs(len(left) - len(right)) + max(len(left), len(right))
        if best is None or score < best[0]:
            best = (score, i)
    if best is None:
        return text
    i = best[1]
    return " ".join(words[:i]) + "\n" + " ".join(words[i:])


def build_cues(tokens: list[Token]) -> list[dict[str, float | str]]:
    cues: list[dict[str, float | str]] = []
    cur: list[Token] = []

    def flush() -> None:
        nonlocal cur
        if not cur:
            return
        text = wrap_two_lines(cue_plain(cur))
        start = float(cur[0].start or 0.0)
        end = float(cur[-1].end or start + 0.8)
        if end - start < 0.72:
            end = start + 0.72
        cues.append({"start": round(start, 3), "end": round(end, 3), "text": text})
        cur = []

    for token in tokens:
        trial = cur + [token]
        trial_text = cue_plain(trial)
        duration = (float(trial[-1].end or 0.0) - float(trial[0].start or 0.0)) if trial else 0.0
        ends_clause = bool(re.search(r"[,.;:?!]$", token.raw))
        if cur and (len(trial_text) > 74 or len(trial) > 12 or (duration > 3.35 and not ends_clause)):
            flush()
        cur.append(token)
        plain = cue_plain(cur)
        dur = float(cur[-1].end or 0.0) - float(cur[0].start or 0.0)
        punct = bool(re.search(r"[.?!]$", token.raw))
        soft = bool(re.search(r"[,;:]$", token.raw))
        if (punct and dur >= 0.9) or (soft and len(cur) >= 5 and dur >= 1.15) or (len(plain) >= 62 and len(cur) >= 5):
            flush()
    flush()

    for i in range(len(cues) - 1):
        cues[i]["end"] = min(float(cues[i]["end"]), max(float(cues[i]["start"]) + 0.55, float(cues[i + 1]["start"]) - 0.035))
    return polish_cues(cues)


def polish_cues(cues: list[dict[str, float | str]]) -> list[dict[str, float | str]]:
    weak_endings = {"a", "an", "and", "as", "at", "by", "for", "from", "in", "of", "or", "that", "the", "to", "with"}
    for i in range(len(cues) - 1):
        text = str(cues[i]["text"]).replace("\n", " ")
        next_text = str(cues[i + 1]["text"]).replace("\n", " ")
        words = text.split()
        next_words = next_text.split()
        if not words or not next_words:
            continue
        end_norm = norm_word(words[-1])
        if end_norm not in weak_endings and not (len(next_words) <= 3 and len(words) + len(next_words) <= 13):
            continue
        merged = words + next_words
        if len(" ".join(merged)) > 84 or len(merged) > 14:
            continue
        best = max(1, min(len(merged) - 1, len(merged) // 2))
        for j in range(1, len(merged)):
            left = merged[:j]
            right = merged[j:]
            if not right or norm_word(left[-1]) in weak_endings:
                continue
            if len(" ".join(left)) > 42 or len(" ".join(right)) > 42:
                continue
            if abs(len(" ".join(left)) - len(" ".join(right))) < abs(len(" ".join(merged[:best])) - len(" ".join(merged[best:]))):
                best = j
        old_end = float(cues[i]["end"])
        total_start = float(cues[i]["start"])
        total_end = float(cues[i + 1]["end"])
        boundary = total_start + (total_end - total_start) * best / len(merged)
        cues[i]["text"] = wrap_two_lines(" ".join(merged[:best]))
        cues[i]["end"] = round(max(float(cues[i]["start"]) + 0.55, min(boundary, total_end - 0.55)), 3)
        cues[i + 1]["text"] = wrap_two_lines(" ".join(merged[best:]))
        cues[i + 1]["start"] = round(max(float(cues[i]["end"]) + 0.035, min(old_end, total_end - 0.55)), 3)
    for i in range(len(cues) - 1):
        words = str(cues[i]["text"]).replace("\n", " ").split()
        next_words = str(cues[i + 1]["text"]).replace("\n", " ").split()
        if not words or not next_words:
            continue
        if "-" not in words[-1] or len(" ".join([words[-1], *next_words])) > 92:
            continue
        cues[i]["text"] = wrap_two_lines(" ".join(words[:-1]))
        cues[i + 1]["text"] = wrap_two_lines(" ".join([words[-1], *next_words]))
        shift = min(0.42, max(0.16, (float(cues[i]["end"]) - float(cues[i]["start"])) / max(len(words), 1)))
        cues[i]["end"] = round(max(float(cues[i]["start"]) + 0.55, float(cues[i]["end"]) - shift), 3)
        cues[i + 1]["start"] = round(float(cues[i]["end"]) + 0.035, 3)
    return cues


def ts_srt(t: float) -> str:
    ms = max(0, int(round(t * 1000)))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_outputs(cues: list[dict[str, float | str]], stats: dict[str, int | float]) -> None:
    OUT_SRT.parent.mkdir(parents=True, exist_ok=True)
    blocks = []
    for i, cue in enumerate(cues, start=1):
        blocks.append(f"{i}\n{ts_srt(float(cue['start']))} --> {ts_srt(float(cue['end']))}\n{cue['text']}\n")
    OUT_SRT.write_text("\n".join(blocks), encoding="utf-8")
    OUT_JSON.write_text(json.dumps({"episode_id": EP, "method": "faster-whisper-small.en-word-timestamps", "cues": cues}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_TS.write_text(
        "export type KeloCaptionCue = {\n"
        "  start: number;\n"
        "  end: number;\n"
        "  text: string;\n"
        "};\n\n"
        f"export const KELO_CAPTIONS: KeloCaptionCue[] = {json.dumps(cues, indent=2, ensure_ascii=False)};\n",
        encoding="utf-8",
    )
    OUT_META.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "voice": str(VOICE),
                "outputs": {
                    "srt": str(OUT_SRT.relative_to(ROOT)).replace("\\", "/"),
                    "json": str(OUT_JSON.relative_to(ROOT)).replace("\\", "/"),
                    "remotion_data": str(OUT_TS.relative_to(ROOT)).replace("\\", "/"),
                },
                "stats": stats | {"cue_count": len(cues)},
                "script_locked": True,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    script_tokens = tokenize(script_text())
    heard_tokens = transcribe_words()
    stats = align(script_tokens, heard_tokens)
    cues = build_cues(script_tokens)
    write_outputs(cues, stats)
    print(f"OK captions_v002 cues={len(cues)} match={stats['match_ratio']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
