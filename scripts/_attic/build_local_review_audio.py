#!/usr/bin/env python3
"""Build local review narration, captions, and Remotion audio wiring data.

This is a no-cost, local-only bridge for episodes that are not yet approved for
paid ElevenLabs generation. It uses Windows SAPI, fits each VO chunk to the
existing rough-cut shot duration, and labels outputs as review_proxy.
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


ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
FPS = 30
OPENING_SEC = 3.5
ENDCARD_SEC = 9.0


EPISODES = {
    "lange": {
        "episode": "PD-2026-014-lange",
        "roughcut": ROOT / "remotion/src/data/lange_roughcut.ts",
        "public_audio": "lange/audio/review_proxy_mix_v001.mp3",
        "caption_const": "LANGE_CAPTIONS",
        "caption_type": "LangeCaption",
        "caption_ts": ROOT / "remotion/src/data/lange_captions.ts",
        "voice": "Microsoft Zira Desktop",
    },
    "theranos": {
        "episode": "PD-2026-015-theranos",
        "roughcut": ROOT / "remotion/src/data/theranos_roughcut.ts",
        "public_audio": "theranos/audio/review_proxy_mix_v001.mp3",
        "caption_const": "THERANOS_CAPTIONS",
        "caption_type": "TheranosCaption",
        "caption_ts": ROOT / "remotion/src/data/theranos_captions.ts",
        "voice": "Microsoft Zira Desktop",
        "shot_order": [
            "SPN-0001",
            "SPN-0002",
            "SPN-0003",
            "SPN-0004",
            "SPN-0005",
            "SPN-0023",
            "SPN-0006",
            "SPN-0007",
            "SPN-0008",
            "SPN-0009",
            "SPN-0010",
            "SPN-0011",
            "SPN-0012",
            "SPN-0024",
            "SPN-0013",
            "SPN-0014",
            "SPN-0015",
            "SPN-0016",
            "SPN-0017",
            "SPN-0018",
            "SPN-0019",
            "SPN-0020",
            "SPN-0021",
            "SPN-0022",
        ],
        "merge_adjacent_chunks": [[13, 14]],
    },
}


def run(cmd: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=True, text=True, capture_output=capture)


def dur(path: Path) -> float:
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture=True)
    return float((r.stdout or "0").strip() or 0)


def sha_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def clean_vo(line: str) -> str:
    text = re.sub(r"^\[VO:\]\s*", "", line.strip())
    text = re.sub(r"\[CLM-[0-9]{4}\]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_script(epdir: Path) -> list[dict]:
    script = epdir / "03_script/script.en.v001.md"
    chunks: list[dict] = []
    section = "unknown"
    for raw in script.read_text("utf-8").splitlines():
        line = raw.strip()
        if line.startswith("## "):
            section = re.sub(r"\s+[-—].*$", "", line[3:].strip())
            continue
        if not line.startswith("[VO:]"):
            continue
        text = clean_vo(line)
        chunk_id = f"VC-{len(chunks) + 1:04d}"
        chunks.append(
            {
                "chunk_id": chunk_id,
                "section": section,
                "spoken_text": text,
                "text_sha256": sha_text(text),
                "source": "script.en.v001.md",
            }
        )
    return chunks


def parse_roughcut(path: Path) -> dict:
    text = path.read_text("utf-8")
    match = re.search(r"export const [A-Z_]+: RoughCutData = (\{.*\});\s*$", text, re.S)
    if not match:
        raise RuntimeError(f"Could not parse roughcut data: {path}")
    return json.loads(match.group(1))


def apply_chunk_merges(chunks: list[dict], merges: list[list[int]] | None) -> list[dict]:
    if not merges:
        return chunks
    merge_map = {tuple(pair) for pair in merges}
    out: list[dict] = []
    i = 0
    while i < len(chunks):
        one_based = i + 1
        pair = next((pair for pair in merge_map if pair[0] == one_based), None)
        if pair:
            j = pair[1] - 1
            if j != i + 1 or j >= len(chunks):
                raise RuntimeError(f"Only adjacent valid chunk merges are supported: {pair}")
            merged_text = f"{chunks[i]['spoken_text']} {chunks[j]['spoken_text']}"
            out.append(
                {
                    **chunks[i],
                    "chunk_id": f"{chunks[i]['chunk_id']}+{chunks[j]['chunk_id']}",
                    "section": chunks[i]["section"],
                    "spoken_text": merged_text,
                    "text_sha256": sha_text(merged_text),
                    "merged_from": [chunks[i]["chunk_id"], chunks[j]["chunk_id"]],
                }
            )
            i += 2
        else:
            out.append(chunks[i])
            i += 1
    for idx, chunk in enumerate(out, 1):
        chunk["chunk_id"] = f"VC-{idx:04d}"
    return out


def atempo_filter(ratio: float) -> str:
    ratio = max(0.25, min(4.0, ratio))
    parts: list[float] = []
    while ratio < 0.5:
        parts.append(0.5)
        ratio /= 0.5
    while ratio > 2.0:
        parts.append(2.0)
        ratio /= 2.0
    parts.append(ratio)
    return ",".join(f"atempo={x:.6f}" for x in parts)


def synthesize_sapi(text: str, out_wav: Path, voice: str) -> None:
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        text_path = td_path / "text.txt"
        text_path.write_text(text, "utf-8")
        ps_path = td_path / "synth.ps1"
        ps_path.write_text(
            """
param([string]$TextPath, [string]$OutPath, [string]$VoiceName)
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
try { $s.SelectVoice($VoiceName) } catch {}
$s.Rate = -1
$s.Volume = 100
$text = Get-Content -LiteralPath $TextPath -Raw -Encoding UTF8
$s.SetOutputToWaveFile($OutPath)
$s.Speak($text)
$s.Dispose()
""".strip(),
            "utf-8",
        )
        run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps_path), str(text_path), str(out_wav), voice])


def split_caption_lines(words: list[str]) -> list[tuple[int, int, str]]:
    lines: list[tuple[int, int, str]] = []
    cur: list[tuple[int, str]] = []
    for i, word in enumerate(words):
        trial = " ".join([w for _, w in cur] + [word])
        if cur and (len(cur) >= 9 or len(trial) > 58):
            lines.append((cur[0][0], cur[-1][0], " ".join(w for _, w in cur)))
            cur = []
        cur.append((i, word))
        if re.search(r"[.?!]$", word) or (word.endswith(",") and len(cur) >= 5):
            lines.append((cur[0][0], cur[-1][0], " ".join(w for _, w in cur)))
            cur = []
    if cur:
        lines.append((cur[0][0], cur[-1][0], " ".join(w for _, w in cur)))
    return lines


def timestamp(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s += 1
        ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_captions(timed_chunks: list[dict]) -> list[dict]:
    out: list[dict] = []
    idx = 1
    for chunk in timed_chunks:
        words = chunk["spoken_text"].split()
        if not words:
            continue
        usable_start = chunk["start"] + 0.08
        usable_end = chunk["end"] - 0.08
        span = max(0.8, usable_end - usable_start)
        for first, last, line in split_caption_lines(words):
            start = usable_start + span * (first / max(1, len(words)))
            end = usable_start + span * ((last + 1) / max(1, len(words)))
            if end - start < 0.7:
                end = start + 0.7
            out.append({"index": idx, "start": round(start, 3), "end": round(min(end, chunk["end"] - 0.02), 3), "text": line})
            idx += 1
    for i in range(1, len(out)):
        if out[i]["start"] < out[i - 1]["end"]:
            out[i]["start"] = round(out[i - 1]["end"] + 0.001, 3)
        if out[i]["end"] <= out[i]["start"]:
            out[i]["end"] = round(out[i]["start"] + 0.55, 3)
    return out


def write_captions(entries: list[dict], epdir: Path, cfg: dict) -> None:
    edit = epdir / "08_edit"
    edit.mkdir(parents=True, exist_ok=True)
    srt = edit / "captions.review_proxy.v001.srt"
    srt.write_text("\n".join(f"{e['index']}\n{timestamp(e['start'])} --> {timestamp(e['end'])}\n{e['text']}\n" for e in entries), "utf-8")
    (edit / "captions.review_proxy.v001.json").write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", "utf-8")
    ts_text = f"export type {cfg['caption_type']} = {{id: string; start: number; end: number; text: string}};\n"
    ts_text += f"export const {cfg['caption_const']}: {cfg['caption_type']}[] = "
    ts_text += json.dumps(
        [{"id": f"CAP-{e['index']:04d}", **{k: e[k] for k in ("start", "end", "text")}} for e in entries],
        ensure_ascii=False,
        indent=2,
    )
    ts_text += ";\n"
    cfg["caption_ts"].write_text(ts_text, "utf-8")


def build_episode(slug: str, dry_run: bool) -> None:
    cfg = EPISODES[slug]
    ep = cfg["episode"]
    epdir = ROOT / "episodes" / ep
    roughcut = parse_roughcut(cfg["roughcut"])
    shots_by_id = {shot["spanId"]: shot for shot in roughcut["shots"]}
    shots = [shots_by_id[span_id] for span_id in cfg.get("shot_order", [shot["spanId"] for shot in roughcut["shots"]])]
    chunks = apply_chunk_merges(parse_script(epdir), cfg.get("merge_adjacent_chunks"))
    if len(chunks) != len(shots):
        raise RuntimeError(f"{ep}: VO chunks ({len(chunks)}) != roughcut shots ({len(shots)})")
    targets = [float(shot["seconds"]) for shot in shots]
    voice_plan = {
        "episode_id": ep,
        "revision": "review_proxy.v001",
        "provider": "local_windows_sapi",
        "voice": cfg["voice"],
        "external_api": False,
        "paid": False,
        "chunks": [{**chunk, "target_seconds": round(targets[i], 3)} for i, chunk in enumerate(chunks)],
    }
    audio_dir = epdir / "06_audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    (audio_dir / "voice_plan.review_proxy.v001.json").write_text(json.dumps(voice_plan, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"{ep}: chunks={len(chunks)} target_audio={sum(targets) + OPENING_SEC + ENDCARD_SEC:.3f}s dry_run={dry_run}")
    if dry_run:
        return

    work = MEDIA / "episodes" / ep / "06_voice" / "review_proxy_v001"
    fit_dir = work / "fitted"
    work.mkdir(parents=True, exist_ok=True)
    fit_dir.mkdir(parents=True, exist_ok=True)
    timed: list[dict] = []
    cursor = 0.0
    concat_lines: list[str] = []
    silence_open = fit_dir / "_opening_silence.wav"
    silence_end = fit_dir / "_endcard_silence.wav"
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=22050:cl=mono", "-t", str(OPENING_SEC), str(silence_open)])
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=22050:cl=mono", "-t", str(ENDCARD_SEC), str(silence_end)])
    for i, chunk in enumerate(chunks):
        raw = work / f"{chunk['chunk_id']}.wav"
        fitted = fit_dir / f"{chunk['chunk_id']}.wav"
        if not raw.exists() or raw.stat().st_size < 2048:
            synthesize_sapi(chunk["spoken_text"], raw, cfg["voice"])
        raw_dur = dur(raw)
        target = targets[i]
        ratio = raw_dur / target if target > 0 else 1
        audio_filter = f"{atempo_filter(ratio)},apad,atrim=0:{target:.6f},asetpts=PTS-STARTPTS"
        run(["ffmpeg", "-y", "-i", str(raw), "-filter:a", audio_filter, "-ar", "22050", str(fitted)])
        fitted_dur = dur(fitted)
        timed.append({**chunk, "file": fitted.name, "start": round(cursor, 3), "end": round(cursor + fitted_dur, 3), "seconds": round(fitted_dur, 3), "raw_seconds": round(raw_dur, 3), "target_seconds": round(target, 3)})
        concat_lines.append(f"file '{fitted.as_posix()}'\n")
        cursor += fitted_dur
        if i == 0:
            concat_lines.append(f"file '{silence_open.as_posix()}'\n")
            cursor += OPENING_SEC
    concat_lines.append(f"file '{silence_end.as_posix()}'\n")
    cursor += ENDCARD_SEC
    concat = fit_dir / "_concat.txt"
    concat.write_text("".join(concat_lines), "utf-8")
    out_media = MEDIA / "episodes" / ep / "07_audio" / "review_proxy_mix_v001.mp3"
    out_media.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c:a", "libmp3lame", "-b:a", "192k", str(out_media)])
    public = ROOT / "remotion/public" / cfg["public_audio"]
    public.parent.mkdir(parents=True, exist_ok=True)
    public.write_bytes(out_media.read_bytes())
    narration_index = {
        "episode_id": ep,
        "revision": "review_proxy.v001",
        "provider": "local_windows_sapi",
        "voice": cfg["voice"],
        "audio": {
            "media_path": str(out_media),
            "remotion_public_src": cfg["public_audio"],
            "seconds": round(dur(out_media), 3),
            "sha256": "sha256:" + hashlib.sha256(out_media.read_bytes()).hexdigest(),
        },
        "chunks": timed,
    }
    (audio_dir / "narration_index.review_proxy.v001.json").write_text(json.dumps(narration_index, indent=2, ensure_ascii=False) + "\n", "utf-8")
    entries = build_captions(timed)
    write_captions(entries, epdir, cfg)
    qc = {
        "episode_id": ep,
        "revision": "review_proxy.v001",
        "audio_seconds": narration_index["audio"]["seconds"],
        "expected_visual_seconds": round(sum(targets) + OPENING_SEC + ENDCARD_SEC, 3),
        "caption_count": len(entries),
        "external_api": False,
        "paid": False,
    }
    (MEDIA / "episodes" / ep / "07_audio" / "review_proxy_qc.v001.json").write_text(json.dumps(qc, indent=2) + "\n", "utf-8")
    print(json.dumps(qc, indent=2))


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", choices=sorted(EPISODES))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    build_episode(args.slug, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
