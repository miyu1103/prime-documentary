"""Forced-align Flash Crash captions to the actual render mix.

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
EP = "PD-2026-018-flashcrash"
EPDIR = ROOT / "episodes" / EP
SCRIPT = EPDIR / "03_script" / "script.en.v001.md"
VOICE_MASTER = Path(r"H:\pd-media\episodes\PD-2026-018-flashcrash\06_voice\master\vc_master_v001.mp3")
FINAL_MIX = ROOT / "remotion" / "public" / "flashcrash" / "audio" / "flashcrash_mix_v001.wav"
VOICE = FINAL_MIX if FINAL_MIX.exists() else VOICE_MASTER
OUT_SRT = EPDIR / "08_edit" / "captions.v001.srt"
OUT_JSON = EPDIR / "08_edit" / "captions.v001.json"
OUT_META = EPDIR / "06_audio" / "caption_alignment.v001.json"
OUT_TS = ROOT / "remotion" / "src" / "data" / "flashcrash_captions.ts"
BREATHE_GAP_SEC = 0.42
MIN_BREATHE_WORDS = 3
MAX_CUE_WORDS = 12
MAX_CUE_CHARS = 74
MAX_CUE_DURATION = 5.4
MIN_CUE_DURATION = 0.72
MIN_CUE_GAP = 0.04
MAX_CPS = 24.0
WEAK_TRAILING_WORDS = {"and", "or", "of", "the", "a", "an", "to", "in", "with", "for", "as", "that", "this", "it"}


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


def should_breath_break(prev: Token, token: Token) -> bool:
    if prev.end is None or token.start is None:
        return False
    return float(token.start) - float(prev.end) >= BREATHE_GAP_SEC


def is_sentence_end(raw: str) -> bool:
    return bool(re.search(r"[.!?]$", raw))


def is_soft_end(raw: str) -> bool:
    return bool(re.search(r"[,;:]$", raw))


def emit_cue(cur: list[Token], cues: list[dict[str, float | str]]) -> None:
    if not cur:
        return
    text = wrap_two_lines(cue_plain(cur))
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        cur.clear()
        return
    start = float(cur[0].start or 0.0)
    end = float(cur[-1].end or (start + 0.8))
    duration = end - start
    if duration < MIN_CUE_DURATION:
        end = start + MIN_CUE_DURATION
    if duration > MAX_CUE_DURATION and len(cur) >= 2:
        mid = max(1, len(cur) // 2)
        emit_cue(cur[:mid], cues)
        emit_cue(cur[mid:], cues)
        cur.clear()
        return
    cues.append({"start": round(start, 3), "end": round(end, 3), "text": text})
    cur.clear()


def build_cues(tokens: list[Token]) -> list[dict[str, float | str]]:
    cues: list[dict[str, float | str]] = []
    cur: list[Token] = []

    def emit_current(carry_weak: bool = False) -> None:
        nonlocal cur
        if carry_weak and len(cur) > 3 and norm_word(cur[-1].raw) in WEAK_TRAILING_WORDS:
            carry = [cur.pop()]
            emit_cue(cur, cues)
            cur = carry
        else:
            emit_cue(cur, cues)

    def duration_of(items: list[Token]) -> float:
        if not items:
            return 0.0
        return float(items[-1].end or 0.0) - float(items[0].start or 0.0)

    for index, token in enumerate(tokens):
        if cur:
            prev = cur[-1]
            if should_breath_break(prev, token) and len(cur) >= MIN_BREATHE_WORDS:
                emit_current()

        trial = cur + [token]
        trial_text = cue_plain(trial)
        duration = duration_of(trial)
        if cur and (
            len(trial_text) > MAX_CUE_CHARS
            or len(trial) > MAX_CUE_WORDS
            or duration > MAX_CUE_DURATION
        ):
            emit_current(carry_weak=True)

        cur.append(token)
        plain = cue_plain(cur)
        dur = duration_of(cur)
        next_token = tokens[index + 1] if index + 1 < len(tokens) else None
        next_gap = (float(next_token.start) - float(token.end)) if next_token and next_token.start is not None and token.end is not None else 0.0
        if is_sentence_end(token.raw) and len(cur) >= 4 and dur >= 0.72:
            emit_current()
        elif is_soft_end(token.raw) and len(cur) >= 5 and dur >= 1.2 and next_gap >= 0.16:
            emit_current()
        elif next_gap >= BREATHE_GAP_SEC and len(cur) >= MIN_BREATHE_WORDS:
            emit_current()
        elif (len(plain) >= MAX_CUE_CHARS and len(cur) >= 5) or len(cur) >= MAX_CUE_WORDS or dur >= MAX_CUE_DURATION:
            emit_current(carry_weak=True)

    emit_current()

    for i in range(len(cues) - 1):
        body = str(cues[i]["text"]).replace("\n", " ").replace(" ", "")
        readable_min = max(MIN_CUE_DURATION, len(body) / MAX_CPS)
        cues[i]["end"] = round(max(float(cues[i]["start"]) + readable_min, float(cues[i]["end"])), 3)

    polished: list[dict[str, float | str]] = []
    for cue in cues:
        cue["text"] = wrap_two_lines(" ".join(str(cue["text"]).replace("\n", " ").split()))
        if str(cue["text"]).strip():
            polished.append(cue)

    merged: list[dict[str, float | str]] = []
    for cue in polished:
        words = str(cue["text"]).replace("\n", " ").split()
        if merged and len(words) <= 2:
            prev = merged[-1]
            gap = float(cue["start"]) - float(prev["end"])
            combined_text = f"{str(prev['text']).replace(chr(10), ' ')} {' '.join(words)}"
            combined_words = combined_text.split()
            combined_duration = float(cue["end"]) - float(prev["start"])
            if gap <= 0.22 and len(combined_words) <= 14 and len(combined_text) <= 86 and combined_duration <= 6.8:
                prev["text"] = wrap_two_lines(combined_text)
                prev["end"] = cue["end"]
                continue
        merged.append(cue)
    polished = merged

    for cue in polished:
        body = str(cue["text"]).replace("\n", " ")
        readable_min = max(MIN_CUE_DURATION, len(body) / MAX_CPS)
        cue["end"] = round(max(float(cue["end"]), float(cue["start"]) + readable_min), 3)

    for i in range(len(polished) - 1):
        i_end = float(polished[i]["end"])
        n_start = float(polished[i + 1]["start"])
        min_next = i_end + MIN_CUE_GAP
        if n_start < min_next:
            polished[i + 1]["start"] = min_next
            if float(polished[i + 1]["end"]) <= float(polished[i + 1]["start"]):
                polished[i + 1]["end"] = round(min_next + MIN_CUE_DURATION, 3)

    return polished


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
    cues = [cue for cue in cues if str(cue["text"]).strip()]
    blocks = []
    for i, cue in enumerate(cues, start=1):
        blocks.append(f"{i}\n{ts_srt(float(cue['start']))} --> {ts_srt(float(cue['end']))}\n{cue['text']}\n")
    OUT_SRT.write_text("\n".join(blocks), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "method": "faster-whisper-small.en-final-mix-word-timestamps",
                "timeline": "final_mix",
                "voice": str(VOICE),
                "cues": cues,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    OUT_TS.write_text(
        "export type FlashCrashCaptionCue = {\n"
        "  start: number;\n"
        "  end: number;\n"
        "  text: string;\n"
        "};\n\n"
        f"export const FLASHCRASH_CAPTIONS: FlashCrashCaptionCue[] = {json.dumps(cues, indent=2, ensure_ascii=False)};\n",
        encoding="utf-8",
    )
    OUT_META.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "voice": str(VOICE),
                "timeline": "final_mix" if VOICE == FINAL_MIX else "voice_master",
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
