"""Forced-align PD-2026-004-ftx captions against the narration master.

Whisper supplies word timestamps from the actual audio. The displayed text stays
the approved narration text from voice_plan.v001.json, so captions match the
script while timing follows the spoken voice.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-004-ftx"
VOICE_PLAN = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
TIMING = ROOT / "episodes" / EP / "08_edit" / "timing.v001.json"
OUT = ROOT / "episodes" / EP / "08_edit" / "captions.v002.srt"
MAX_WORDS = 7
MAX_CHARS = 42


def norm(word: str) -> str:
    return re.sub(r"[^a-z0-9]", "", word.lower())


def srt_ts(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s += 1
        ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def transcribe(master: Path) -> list[dict]:
    from faster_whisper import WhisperModel

    print("loading faster-whisper small.en (cpu/int8)")
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(
        str(master),
        word_timestamps=True,
        vad_filter=False,
        beam_size=5,
        language="en",
        condition_on_previous_text=False,
    )
    words: list[dict] = []
    for segment in segments:
        for w in segment.words or []:
            token = w.word.strip()
            n = norm(token)
            if n:
                words.append({"word": token, "norm": n, "start": float(w.start), "end": float(w.end)})
    print(f"whisper words: {len(words)}")
    return words


def script_tokens(text: str) -> list[str]:
    return text.replace("—", "—").replace(" allow_negative", " allow negative").split()


def split_lines(tokens: list[str]) -> list[tuple[str, int, int]]:
    lines: list[tuple[str, int, int]] = []
    cur: list[tuple[str, int]] = []
    for i, word in enumerate(tokens):
        trial = " ".join([x for x, _ in cur] + [word])
        if cur and (len(cur) >= MAX_WORDS or len(trial) > MAX_CHARS):
            lines.append((" ".join(x for x, _ in cur), cur[0][1], cur[-1][1]))
            cur = []
        cur.append((word, i))
        if re.search(r"[.?!]$", word) or word.endswith("—") or (word.endswith(",") and len(cur) >= 4):
            lines.append((" ".join(x for x, _ in cur), cur[0][1], cur[-1][1]))
            cur = []
    if cur:
        lines.append((" ".join(x for x, _ in cur), cur[0][1], cur[-1][1]))
    return lines


def align_chunk(tokens: list[str], chunk_words: list[dict], start: float, end: float) -> list[tuple[float, float]]:
    times: list[tuple[float, float] | None] = [None] * len(tokens)
    j = 0
    for i, token in enumerate(tokens):
        tn = norm(token)
        if not tn:
            continue
        found = None
        for k in range(j, min(j + 6, len(chunk_words))):
            wn = chunk_words[k]["norm"]
            if wn == tn or (len(tn) >= 4 and wn.startswith(tn[:4])) or (len(wn) >= 4 and tn.startswith(wn[:4])):
                found = k
                break
        if found is None and j < len(chunk_words):
            found = j
        if found is not None:
            times[i] = (chunk_words[found]["start"], chunk_words[found]["end"])
            j = found + 1

    known = [(i, t) for i, t in enumerate(times) if t is not None]
    for i, value in enumerate(times):
        if value is not None:
            continue
        if known:
            prev_known = max((k for k in known if k[0] < i), default=None)
            next_known = min((k for k in known if k[0] > i), default=None)
            if prev_known and next_known:
                frac = (i - prev_known[0]) / max(1, next_known[0] - prev_known[0])
                t = prev_known[1][1] + frac * (next_known[1][0] - prev_known[1][1])
            else:
                frac = (i + 0.5) / max(1, len(tokens))
                t = start + frac * (end - start)
        else:
            frac = (i + 0.5) / max(1, len(tokens))
            t = start + frac * (end - start)
        times[i] = (float(t), float(t) + 0.28)
    return [t for t in times if t is not None]


def main() -> int:
    voice_plan = json.loads(VOICE_PLAN.read_text("utf-8"))
    timing = json.loads(TIMING.read_text("utf-8"))
    media = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
    master = media / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
    if not master.exists():
        raise FileNotFoundError(master)

    words = transcribe(master)
    scene_by_chunk = {scene["chunk_id"]: scene for scene in timing["scenes"]}
    entries: list[tuple[int, float, float, str]] = []
    n = 1
    for chunk in voice_plan["chunks"]:
        scene = scene_by_chunk.get(chunk["chunk_id"])
        if not scene:
            continue
        start = float(scene["start"])
        end = float(scene["end"])
        chunk_words = [
            word
            for word in words
            if start - 0.35 <= (word["start"] + word["end"]) / 2 <= end + 0.35
        ]
        tokens = script_tokens(chunk["spoken_text"])
        if not tokens:
            continue
        token_times = align_chunk(tokens, chunk_words, start, end)
        for line, a, b in split_lines(tokens):
            s = max(start, token_times[a][0] - 0.03)
            e = min(end, token_times[b][1] + 0.06)
            if e <= s:
                e = min(end, s + 0.55)
            entries.append((n, s, e, line))
            n += 1

    fixed: list[tuple[int, float, float, str]] = []
    for n, s, e, line in entries:
        if fixed and s < fixed[-1][2] + 0.02:
            s = fixed[-1][2] + 0.02
        if e <= s:
            e = s + 0.5
        fixed.append((n, s, e, line))

    OUT.write_text(
        "\n".join(f"{n}\n{srt_ts(s)} --> {srt_ts(e)}\n{text}\n" for n, s, e, text in fixed),
        encoding="utf-8",
    )
    print(f"wrote {OUT.relative_to(ROOT)} ({len(fixed)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
