#!/usr/bin/env python3
"""Generate SHORT #24 (Raj Rajaratnam / "his own voice") vertical-short narration with the channel voice.

US-market English VO. Voice = channel voice, model = multilingual v2. Paid ElevenLabs (pre-authorized).
Source: episodes/_planning/SHORTS_EP19-24.md SHORT #24.

R2 / sensitive: convicted at trial. WORDING LOCKS (do not deviate):
  - Convicted at a JURY TRIAL = stateable as fact; he did NOT plead guilty (fought it and lost) —
    never "admitted guilt."
  - "longest insider-trading sentence" is ATTRIBUTED to prosecutors/press and time-bound to 2011.
  - Profit hedged → anchor to the ~$54M forfeiture, not a single flat profit figure.
  - The Goldman director (Gupta) is a SEPARATE case; tippers were charged separately.
  - No verbatim wiretap dialogue. No real-person likeness.
No real-person likeness in visuals (handled elsewhere). Idempotent: existing non-empty chunks are skipped.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-033-tyler"
SHORT = "short33"
MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
GAP = 0.72  # shorter inter-line silence — owner felt the pace was slow (premium EP33 retune)

# speed 1.09 = a touch faster delivery (ElevenLabs voice_settings, range 0.7–1.2) so it doesn't drag.
SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True, "speed": 1.08},
    "building": {"stability": 0.50, "similarity_boost": 0.82, "style": 0.26, "use_speaker_boost": True, "speed": 1.09},
    "intense": {"stability": 0.44, "similarity_boost": 0.84, "style": 0.36, "use_speaker_boost": True, "speed": 1.10},
}

# (line_id, delivery, spoken_text) — EP33 Tyler v. Hennepin County (home-equity theft). US-market English.
# WORDING LOCKS (do not deviate, per EP33 §1 FACTS LOCKED):
#   - Tyler v. Hennepin County = 2023, NINE to ZERO, Chief Justice Roberts wrote it.
#   - Numbers (grade A, may state): 94 years old; debt ~$15,000 (principal ~$2,300 + interest/penalties);
#     condo SOLD for $40,000; county KEPT the whole $40,000; surplus ~$25,000 taken.
#   - Holding: keeping the surplus beyond the debt is a TAKING without just compensation (FIFTH Amendment).
#     The Court did NOT decide the Eighth Amendment (excessive fines). Do not say the 8th was violated.
#   - Roberts quote verbatim (comma): "render unto Caesar what is Caesar's, but no more."
#   - Say "most states already required the surplus be returned" — do NOT burn the specific "36 states".
#   - "home equity theft" is the critics'/advocacy term — attribute ("what critics call"). No real-person
#     likeness (94-yo woman anonymous in visuals). Government neutral.
LINES: list[tuple[str, str, str]] = [
    ("L1", "intense", "You owe the county fifteen thousand dollars. They take your home, sell it for forty thousand — and keep every last dollar. Can they really do that?"),
    ("L2", "building", "That's what happened to Geraldine Tyler. At ninety-four, she owed about fifteen thousand in property taxes and penalties on her old condo. Hennepin County, Minnesota seized it, sold it for forty thousand — and kept the entire amount, including roughly twenty-five thousand that had nothing to do with the debt."),
    ("L3", "building", "The Constitution's Fifth Amendment says if the government takes your property, it has to pay for it. That extra twenty-five thousand was hers, not the county's. Keeping it, her lawyers said, was the government taking far more than it was owed."),
    ("L4", "intense", "In 2023, the Supreme Court agreed — nine to zero. Chief Justice Roberts wrote that a taxpayer must render unto Caesar what is Caesar's, but no more. Pocketing the surplus was an unconstitutional taking. Most states already banned what critics call home equity theft — now it's the rule everywhere."),
    ("L5", "calm", "Watch the full story on the channel. Follow for more."),
]


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
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


def idem(text: str, cid: str) -> str:
    material = json.dumps({"short_id": SHORT, "chunk_id": cid, "model": MODEL, "voice_id": VOICE_ID,
                           "text_sha256": hashlib.sha256(text.encode()).hexdigest()}, sort_keys=True)
    return "sha256:" + hashlib.sha256(material.encode()).hexdigest()


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    dry = "--dry-run" in sys.argv
    env = load_env()
    key = env.get("ELEVENLABS_API_KEY")
    chars = sum(len(t) for _, _, t in LINES)
    est = round(chars / 1000 * 0.30, 3)
    print(f"short={SHORT} lines={len(LINES)} chars={chars} est=${est:.3f}")
    if dry:
        for lid, dlv, t in LINES:
            print(f"  {lid} {dlv:8s} {len(t):3d}ch  {t[:28]}...")
        return 0
    if not key:
        print("ERROR: ELEVENLABS_API_KEY missing")
        return 1

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
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  {lid} ERR {e}")

    silence = draft / "_silence.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(GAP),
                    "-c:a", "libmp3lame", "-b:a", "192k", str(silence)], check=True, capture_output=True)
    concat = draft / "_concat.txt"
    lines_txt: list[str] = []
    windows = []
    cursor = 0.0
    for i, (lid, dlv, text) in enumerate(LINES, 1):
        path = draft / f"{SHORT}_{lid}.mp3"
        d = dur(path)
        windows.append({"id": lid, "chunk_id": lid, "delivery": dlv, "text": text,
                        "start": round(cursor, 3), "end": round(cursor + d, 3), "seconds": d,
                        "idempotency_key": idem(text, lid)})
        lines_txt.append(f"file '{path.as_posix()}'\n")
        cursor += d
        if i != len(LINES):
            lines_txt.append(f"file '{silence.as_posix()}'\n")
            cursor += GAP
    concat.write_text("".join(lines_txt), "utf-8")
    master = media_root() / "episodes" / EP / "06_voice" / "master" / "short33_vc_master_en_us_v002.mp3"
    master.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
                    "-c:a", "libmp3lame", "-b:a", "192k", str(master)], check=True, capture_output=True)

    idx = ROOT / "episodes" / EP / "06_audio" / "short33_narration_index.v002.en_us.json"
    idx.parent.mkdir(parents=True, exist_ok=True)
    idx.write_text(json.dumps({"short_id": SHORT, "episode_id": EP, "voice_id": VOICE_ID, "model_id": MODEL,
                               "estimated_cost_usd": est, "total_seconds": round(dur(master), 2),
                               "master": str(master), "lines": windows}, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"master -> {master} ({dur(master):.2f}s)")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
