#!/usr/bin/env python
"""Create the initial EP44 Tekoh working files from locked planning inputs.

This script has no external side effects. It creates missing EP44 directories,
copies the locked script into the episode workspace, extracts the asset prompts
from the A handoff, and writes a timing estimate narration_index for local build
validation until the real voice index replaces it.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-044-tekoh"
SLUG = "tekoh"
EPDIR = ROOT / "episodes" / EP
PLAN = ROOT / "episodes" / "_planning"
SCRIPT_SRC = PLAN / "EP44_tekoh_script.en.v001.md"
SPEC_SRC = PLAN / "EP44_tekoh_PRODUCTION_SPEC.v001.json"
A_PROMPT = PLAN / "EP44_tekoh_CODEX_A_ASSETS.v001.md"

SECTION_SECONDS = {
    "HOOK": 33.0,
    "OP": 46.2,
    "ACT_1": 77.5,
    "ACT_2": 150.9,
    "ACT_3": 212.6 + 74.8,
    "ENDING": 111.2,
}

STYLE = (
    "cinematic documentary still, 4k, premium legal documentary tone, cold interrogation teal, "
    "controlled contrast, natural materials, shallow depth of field, symbolic objects only"
)
NEG = (
    "people, faces, portraits, likenesses, readable text, real documents, judge likenesses, "
    "law enforcement portrait, medical procedure, patients, allegation details, logos, watermark"
)


def mkdirs() -> None:
    for rel in [
        "00_topic",
        "01_research",
        "03_script",
        "04_scenes",
        "05_visuals",
        "05_stock",
        "06_audio",
        "08_edit/ae_hero",
        "09_package",
        "approvals",
        "events",
    ]:
        (EPDIR / rel).mkdir(parents=True, exist_ok=True)


def write_if_missing(path: Path, text: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def copy_script() -> bool:
    return write_if_missing(EPDIR / "03_script" / "script.en.v001.md", SCRIPT_SRC.read_text(encoding="utf-8"))


def facts_doc() -> dict:
    return {
        "schema_version": "tekoh_facts.v1",
        "episode_id": EP,
        "source": "episodes/_planning/EP44_tekoh_script.en.v001.md plus Supreme Court opinion cross-check",
        "facts": {
            "F01": {"value": "2022-06-23", "unit": "date", "verified": True, "claim_id": "C01", "quote": "decided June 23, 2022"},
            "F02": {"value": "Vega v. Tekoh, 597 U.S. 134 (2022), No. 21-499", "unit": "case_citation", "verified": True, "claim_id": "C01", "quote": "Vega v. Tekoh, 597 U.S. 134 (2022), No. 21-499"},
            "F03": {"value": "6-3; reversed and remanded", "unit": "vote_disposition", "verified": True, "claim_id": "C02/C10", "quote": "6-3; reversed and remanded"},
            "F04": {"value": "Justice Samuel Alito wrote for the majority", "unit": "attribution", "verified": True, "claim_id": "C03", "quote": "Alito, for six of nine"},
            "F05": {"value": "Justice Elena Kagan dissented, joined by Breyer and Sotomayor", "unit": "attribution", "verified": True, "claim_id": "C04", "quote": "Kagan, joined by Breyer and Sotomayor"},
            "F06": {"value": "Miranda v. Arizona, 384 U.S. 436 (1966)", "unit": "case_citation", "verified": True, "claim_id": "C22", "quote": "Miranda v. Arizona, 384 U.S. 436 (1966)"},
            "F07": {"value": "Dickerson v. United States (2000)", "unit": "case_name", "verified": True, "claim_id": "C23", "quote": "Dickerson v. United States (2000)"},
            "F08": {"value": "42 U.S.C. section 1983", "unit": "statute", "verified": True, "claim_id": "C08", "quote": "Section 1983"},
            "F09": {"value": "2014 medical center, Los Angeles", "unit": "setting", "verified": True, "claim_id": "C11/C13", "quote": "2014, inside a medical center in Los Angeles"},
            "F10": {"value": "Los Angeles County sheriff's deputy Carlos Vega", "unit": "participant", "verified": True, "claim_id": "C12", "quote": "Carlos Vega"},
            "F11": {"value": 2, "unit": "civil_trials", "verified": True, "claim_id": "C16", "quote": "Twice, federal juries heard his civil case"},
            "F12": {"value": "acquitted", "unit": "criminal_verdict", "verified": True, "claim_id": "C14", "quote": "They acquitted him"},
            "F13": {"value": "Ninth Circuit reversed and remanded", "unit": "appellate_disposition", "verified": True, "claim_id": "C17", "quote": "It sent the case back"},
            "F14": {"value": "a fence, not the ground", "unit": "doctrinal_metaphor", "verified": True, "claim_id": "C06/C24", "quote": "A fence. Not the ground it stands on."},
            "F15": {"value": "Miranda violation standing alone is not section 1983 damages", "unit": "holding_scope", "verified": True, "claim_id": "C05/C07", "quote": "the deputy could not be made to pay money damages simply because the warning had been left out"},
            "F16": {"value": "Today, the Court strips individuals of the ability to seek a remedy for violations of the right recognized in Miranda.", "unit": "dissent_quote", "verified": True, "claim_id": "C20/C21", "quote": "Justice Kagan dissent"},
        },
    }


def section_of_heading(line: str) -> str | None:
    if "HOOK" in line:
        return "HOOK"
    if "OPENING" in line:
        return "OP"
    if "ACT 1" in line:
        return "ACT_1"
    if "ACT 2" in line:
        return "ACT_2"
    if "ACT 3" in line:
        return "ACT_3"
    if "ENDING" in line:
        return "ENDING"
    return None


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", text))


def narration_index() -> dict:
    sections: dict[str, list[dict]] = {k: [] for k in SECTION_SECONDS}
    current: str | None = None
    silence_re = re.compile(r"\[SILENCE\s+(\d+)\s+[—-]\s+([0-9.]+)s", re.IGNORECASE)
    for raw in SCRIPT_SRC.read_text(encoding="utf-8").splitlines():
        if raw.startswith("## "):
            current = section_of_heading(raw)
            continue
        if current is None:
            continue
        sm = silence_re.search(raw)
        if sm:
            sections[current].append({"kind": "silence", "seconds": float(sm.group(2)), "text": ""})
            continue
        if raw.startswith(">"):
            text = raw.lstrip("> ").strip()
            if text:
                sections[current].append({"kind": "speech", "text": text})

    chunks: list[dict] = []
    cursor = 0.0
    idx = 1
    for sec, total_sec in SECTION_SECONDS.items():
        items = sections[sec]
        silence_total = sum(float(i.get("seconds", 0)) for i in items if i["kind"] == "silence")
        speech_words = sum(word_count(i["text"]) for i in items if i["kind"] == "speech")
        speech_sec = max(0.1, total_sec - silence_total)
        for item in items:
            if item["kind"] == "silence":
                dur = float(item["seconds"])
                chunks.append({"id": f"VC-{idx:04d}", "section": sec, "start": round(cursor, 3), "end": round(cursor + dur, 3), "text": "", "type": "silence"})
            else:
                dur = speech_sec * word_count(item["text"]) / max(1, speech_words)
                chunks.append({"id": f"VC-{idx:04d}", "section": sec, "start": round(cursor, 3), "end": round(cursor + dur, 3), "text": item["text"], "type": "speech"})
            cursor += dur
            idx += 1
    return {
        "schema_version": "pd_narration_index.v1",
        "episode_id": EP,
        "source": "estimated_from_locked_script_until_master_voice_replaces_this",
        "audio_path": "tekoh/audio/narration_master.v001.mp3",
        "duration_sec": round(cursor, 3),
        "chunks": chunks,
    }


def extract_prompts() -> str:
    entries_by_name: dict[str, str] = {}
    lines = A_PROMPT.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines[:-1]):
        m = re.match(r"^-\s+`((?:S\d{2}|M\d{2}_src)\.png)`\s*$", line.strip())
        if not m:
            continue
        prompt = lines[i + 1].strip()
        if "Avoid:" not in prompt:
            continue
        prompt = prompt.replace("[STYLE]", STYLE).replace("[NEG]", NEG)
        entries_by_name[m.group(1)] = prompt
    entries = sorted(entries_by_name.items())
    body = [e for e in entries if e[0].startswith("S")]
    motion = [e for e in entries if e[0].startswith("M")]
    if len(body) != 85 or len(motion) != 16:
        raise SystemExit(f"prompt extraction mismatch: body={len(body)} i2v={len(motion)}")
    out = [
        "# EP44 Tekoh AI prompts v001",
        "",
        "All prompts are symbolic. Do not render real-person faces, likenesses, readable documents, or underlying allegation details.",
        "",
    ]
    for name, prompt in entries:
        out += [f"- `{name}`", prompt, ""]
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    mkdirs()
    changed = []
    if copy_script():
        changed.append("03_script/script.en.v001.md")
    if write_if_missing(EPDIR / "03_script" / "tekoh_facts.v001.json", json.dumps(facts_doc(), ensure_ascii=False, indent=2) + "\n"):
        changed.append("03_script/tekoh_facts.v001.json")
    if write_if_missing(EPDIR / "06_audio" / "narration_index.v001.json", json.dumps(narration_index(), ensure_ascii=False, indent=2) + "\n"):
        changed.append("06_audio/narration_index.v001.json")
    if write_if_missing(EPDIR / "04_scenes" / "ai_prompts.v001.md", extract_prompts()):
        changed.append("04_scenes/ai_prompts.v001.md")
    manifest = {
        "episode_id": EP,
        "slug": SLUG,
        "state": "asset_plan_ready",
        "source_script": "episodes/_planning/EP44_tekoh_script.en.v001.md",
        "production_spec": "episodes/_planning/EP44_tekoh_PRODUCTION_SPEC.v001.json",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "approvals": [],
    }
    if write_if_missing(EPDIR / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"):
        changed.append("manifest.json")
    event = {"ts": datetime.now(timezone.utc).isoformat(), "event": "tekoh_bootstrap", "producer": "scripts/bootstrap_tekoh_episode.py", "changed": changed}
    events = EPDIR / "events" / "events.jsonl"
    events.parent.mkdir(parents=True, exist_ok=True)
    if changed and not events.exists():
        events.write_text(json.dumps(event, ensure_ascii=False) + "\n", encoding="utf-8")
        changed.append("events/events.jsonl")
    print(json.dumps({"episode_id": EP, "changed": changed}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
