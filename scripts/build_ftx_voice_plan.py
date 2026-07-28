"""Build PD-2026-004-ftx voice_plan.v001.json from script.en.v002.md."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-004-ftx"
SCRIPT = ROOT / "episodes" / EP / "03_script" / "script.en.v002.md"
OUT = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
VOICE_ID = "nPczCjzI2devNBz1zQrb"
MODEL_ID = "eleven_multilingual_v2"


SECTION_MAP = {
    "FLASH-FORWARD HOOK": "00_hook",
    "COLD OPEN": "01_cold_open",
    "OPENING": "02_opening",
    "ACT I": "actI_trust",
    "ACT II": "actII_code",
    "ACT III": "actIII_run",
    "ACT IV": "actIV_verdict",
    "ENDING": "ending",
}


def clean_spoken(text: str) -> str:
    text = re.sub(r"\[[A-Z]+-\d{4}\]", "", text)
    text = re.sub(r"\[framing\]", "", text)
    text = re.sub(r"\[production:[^\]]+\]", "", text)
    text = re.sub(r"\*\((.*?)\)\*", r"\1", text)
    text = text.replace("**", "").replace("*", "")
    text = text.replace("allow_negative", "allow negative")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main() -> int:
    chunks = []
    section = "unknown"
    delivery = "calm"
    current_section_title = ""
    for raw in SCRIPT.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("## "):
            current_section_title = line[3:].split("—")[0].strip()
            for key, value in SECTION_MAP.items():
                if current_section_title.startswith(key):
                    section = value
                    break
            m = re.search(r"\[(calm|building|intense)\]", line)
            delivery = m.group(1) if m else ("intense" if section == "00_hook" else "calm")
            continue
        m = re.match(r"\*\*\[(calm|building|intense)\]\*\*", line)
        if m:
            delivery = m.group(1)
            continue
        if not line.startswith("[VO:]"):
            continue
        spoken = clean_spoken(line.removeprefix("[VO:]").strip())
        if not spoken:
            continue
        chunk_id = f"VC-{len(chunks) + 1:04d}"
        chunks.append(
            {
                "chunk_id": chunk_id,
                "section": section,
                "delivery": delivery,
                "spoken_text": spoken,
                "word_count": len(spoken.split()),
            }
        )
    plan = {
        "voice_plan_id": "VP-PD-2026-004-ftx-v001",
        "episode_id": EP,
        "source_script": "03_script/script.en.v002.md",
        "voice_id": VOICE_ID,
        "model_id": MODEL_ID,
        "target_runtime_sec": 720.0,
        "notes": [
            "Generated from script v002. CLM tags and production notes removed from spoken text.",
            "Final runtime should be hit by atempo after real narration duration is known.",
        ],
        "chunks": chunks,
    }
    OUT.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"chunks={len(chunks)} words={sum(c['word_count'] for c in chunks)} -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
