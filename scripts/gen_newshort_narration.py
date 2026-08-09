#!/usr/bin/env python3
"""Synthesize a new-shorts VO (short38..short43) with the channel voice.

Modeled byte-for-byte on scripts/gen_short35_narration.py (same VOICE_ID, model, voice_settings,
GAP, ducking-friendly output). The L1..L5 line text is reconstructed from the design-estimate
timing file remotion/src/data/short<NN>_timing.ts (captions grouped by LINE_WINDOWS), which
concatenates exactly to the plan.v001.json narration_script — so the locked wording is preserved.
Delivery arc mirrors short35: L1 intense / L2 building / L3 building / L4 intense / L5 calm.

Writes:
  H:/pd-media/episodes/<ep>/06_voice/draft/short<NN>/en_us/short<NN>_L?.mp3  (idempotent chunks)
  H:/pd-media/episodes/<ep>/06_voice/master/short<NN>_vc_master_en_us_v002.mp3
  episodes/<ep>/06_audio/short<NN>_narration_index.v002.en_us.json   (consumed by build_short_mix.py)

Usage: gen_newshort_narration.py --short 38 --ep PD-2026-036-williams [--dry-run]
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
GAP = 0.72
SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True, "speed": 1.08},
    "building": {"stability": 0.50, "similarity_boost": 0.82, "style": 0.26, "use_speaker_boost": True, "speed": 1.09},
    "intense": {"stability": 0.44, "similarity_boost": 0.84, "style": 0.36, "use_speaker_boost": True, "speed": 1.10},
}
DELIVERY = {"L1": "intense", "L2": "building", "L3": "building", "L4": "intense", "L5": "calm"}


def _json_array_after(text: str, marker: str):
    i = text.index(marker)
    eq = text.index("=", i)          # skip past the `: Type[]` annotation
    j = text.index("[", eq)
    depth = 0
    for k in range(j, len(text)):
        if text[k] == "[":
            depth += 1
        elif text[k] == "]":
            depth -= 1
            if depth == 0:
                return json.loads(text[j:k + 1])
    raise ValueError("array not closed for " + marker)


def reconstruct_lines(short: str) -> list[tuple[str, str, str]]:
    tf = (ROOT / "remotion" / "src" / "data" / f"short{short}_timing.ts").read_text("utf-8")
    windows = _json_array_after(tf, "LINE_WINDOWS")
    caps = _json_array_after(tf, f"SHORT{short}_CAPTIONS")
    lines = []
    for w in windows:
        words = [c["word"] for c in caps if w["start"] <= c["startSec"] < w["end"] + 1e-6]
        # include a caption exactly at/after the last window's end
        text = " ".join(words).strip()
        lines.append((w["id"], DELIVERY.get(w["id"], "building"), text))
    # safety: any caption not captured (edge) append to nearest last line
    return lines


def load_env() -> dict:
    env = {}
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text("utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def media_root() -> Path:
    cfg = json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


def dur(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True)
    try:
        return round(float(r.stdout.strip()), 3)
    except Exception:
        return 0.0


def idem(short: str, text: str, cid: str) -> str:
    material = json.dumps({"short_id": f"short{short}", "chunk_id": cid, "model": MODEL, "voice_id": VOICE_ID,
                           "text_sha256": hashlib.sha256(text.encode()).hexdigest()}, sort_keys=True)
    return "sha256:" + hashlib.sha256(material.encode()).hexdigest()


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--short", required=True)
    ap.add_argument("--ep", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--gap", type=float, default=GAP,
                    help=f"inter-line silence seconds (default {GAP}). Lower it (e.g. 0.30) to tighten "
                         "a short toward the <=40s method target without re-synthesizing.")
    ap.add_argument("--text-json", default=None,
                    help="optional path to a JSON list [{id,delivery,text}] of trimmed line text; "
                         "overrides reconstruct-from-timing so a shortened script can be synthesized. "
                         "Delete the stale draft chunk mp3s first so the new text is re-synthesized.")
    ap.add_argument("--voice-stage", choices=("draft", "master"), default="master",
                    help="write the assembled voice as a review draft or approved master")
    args = ap.parse_args()
    SHORT = f"short{args.short}"
    EP = args.ep
    gap = args.gap
    if args.text_json:
        spec = json.loads(Path(args.text_json).read_text("utf-8"))
        LINES = [(d["id"], d.get("delivery", DELIVERY.get(d["id"], "building")), d["text"].strip()) for d in spec]
    else:
        LINES = reconstruct_lines(args.short)
    chars = sum(len(t) for _, _, t in LINES)
    est = round(chars / 1000 * 0.30, 3)
    print(f"short={SHORT} ep={EP} lines={len(LINES)} chars={chars} est=${est:.3f}")
    for lid, dlv, t in LINES:
        print(f"  {lid} {dlv:8s} {len(t):3d}ch  {t[:60]}")
    if args.dry_run:
        return 0
    env = load_env()
    key = env.get("ELEVENLABS_API_KEY")
    if not key:
        print("ERROR: ELEVENLABS_API_KEY missing"); return 1

    draft = media_root() / "episodes" / EP / "06_voice" / "draft" / SHORT / "en_us"
    draft.mkdir(parents=True, exist_ok=True)
    made = skipped = failed = 0
    for lid, dlv, text in LINES:
        out = draft / f"{SHORT}_{lid}.mp3"
        if out.exists() and out.stat().st_size > 2048:
            skipped += 1
            continue
        body = json.dumps({"text": text, "model_id": MODEL, "voice_settings": SETTINGS[dlv]}).encode("utf-8")
        req = urllib.request.Request(TTS.format(vid=VOICE_ID), data=body,
                                     headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
                                     method="POST")
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                out.write_bytes(r.read())
            print(f"  {lid} {dlv:8s} {len(text):3d}ch -> {out.stat().st_size//1024}KB {dur(out):.2f}s")
            made += 1
            time.sleep(0.35)
        except urllib.error.HTTPError as e:
            failed += 1
            print(f"  {lid} HTTP {e.code}: {e.read().decode(errors='replace')[:240]}")
        except Exception as e:
            failed += 1
            print(f"  {lid} ERR {e}")

    silence = draft / "_silence.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(gap),
                    "-c:a", "libmp3lame", "-b:a", "192k", str(silence)], check=True, capture_output=True)
    concat = draft / "_concat.txt"
    lines_txt, windows = [], []
    cursor = 0.0
    for i, (lid, dlv, text) in enumerate(LINES, 1):
        path = draft / f"{SHORT}_{lid}.mp3"
        d = dur(path)
        windows.append({"id": lid, "chunk_id": lid, "delivery": dlv, "text": text,
                        "start": round(cursor, 3), "end": round(cursor + d, 3), "seconds": d,
                        "idempotency_key": idem(args.short, text, lid)})
        lines_txt.append(f"file '{path.as_posix()}'\n")
        cursor += d
        if i != len(LINES):
            lines_txt.append(f"file '{silence.as_posix()}'\n")
            cursor += gap
    concat.write_text("".join(lines_txt), "utf-8")
    if args.voice_stage == "draft":
        master = draft / f"{SHORT}_vc_draft_en_us_v002.mp3"
    else:
        master = media_root() / "episodes" / EP / "06_voice" / "master" / f"{SHORT}_vc_master_en_us_v002.mp3"
    master.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
                    "-c:a", "libmp3lame", "-b:a", "192k", str(master)], check=True, capture_output=True)

    idx = ROOT / "episodes" / EP / "06_audio" / f"{SHORT}_narration_index.v002.en_us.json"
    idx.parent.mkdir(parents=True, exist_ok=True)
    idx.write_text(json.dumps({"short_id": SHORT, "episode_id": EP, "voice_stage": args.voice_stage,
                               "voice_id": VOICE_ID, "model_id": MODEL,
                               "estimated_cost_usd": est, "total_seconds": round(dur(master), 2),
                               "master": str(master), "lines": windows}, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"master -> {master} ({dur(master):.2f}s)")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
