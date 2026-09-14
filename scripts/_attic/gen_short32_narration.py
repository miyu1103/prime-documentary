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
EP = "PD-2026-032-carsearch"
SHORT = "short32"
MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
GAP = 1.20  # tightened toward the doc's "speedy cuts / short silences" intent; narration body is the real length driver

SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True},
    "building": {"stability": 0.50, "similarity_boost": 0.82, "style": 0.26, "use_speaker_boost": True},
    "intense": {"stability": 0.44, "similarity_boost": 0.84, "style": 0.36, "use_speaker_boost": True},
}

# (line_id, delivery, spoken_text) — EP32 "Can the police search your car?" (Carroll 1925 + Collins 2018).
# WORDING LOCKS (do not deviate): automobile exception since 1925 (Carroll); a car is not a house =
# probable cause, no warrant, on the spot. Probable cause is NOT a hunch and being pulled over is NOT
# permission. Search scope = wherever the object sought could fit. Collins v. Virginia = 2018, EIGHT to ONE
# (not 7-1); driveway pressed against the home = "curtilage" = part of the home. The quote "extends no
# further than the automobile itself" is ATTRIBUTED to the Court (Sotomayor, majority). No real-person
# likeness. Neutral / advertiser-safe.
LINES: list[tuple[str, str, str]] = [
    ("L1", "intense", "The police can search your car without a warrant — and they have for a hundred years. But there's one place they still can't follow it."),
    ("L2", "building", "It goes back to 1925 and a Prohibition bootlegger named Carroll. Agents tore open his seats and found sixty-eight bottles of whisky — no warrant. The Court said a car isn't a house: it can be driven off before a warrant is ever signed. So with probable cause, police can search it on the spot."),
    ("L3", "building", "But probable cause is the catch. Being pulled over isn't permission, and a hunch isn't enough — an officer needs a real, specific reason. And the search only reaches where the thing they're after could fit. Chasing a stolen television doesn't let them open a pill bottle."),
    ("L4", "intense", "Then came Virginia. An officer walked up a driveway, lifted a tarp off a motorcycle he believed was stolen, and confirmed it. In 2018, by eight to one, the Supreme Court said no. The driveway hugging your home is curtilage — part of the house — and the car-search power stops there. It extends, the Court said, no further than the car itself."),
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
    master = media_root() / "episodes" / EP / "06_voice" / "master" / "short32_vc_master_en_us_v002.mp3"
    master.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
                    "-c:a", "libmp3lame", "-b:a", "192k", str(master)], check=True, capture_output=True)

    idx = ROOT / "episodes" / EP / "06_audio" / "short32_narration_index.v002.en_us.json"
    idx.parent.mkdir(parents=True, exist_ok=True)
    idx.write_text(json.dumps({"short_id": SHORT, "episode_id": EP, "voice_id": VOICE_ID, "model_id": MODEL,
                               "estimated_cost_usd": est, "total_seconds": round(dur(master), 2),
                               "master": str(master), "lines": windows}, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"master -> {master} ({dur(master):.2f}s)")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
