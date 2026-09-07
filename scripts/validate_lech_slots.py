#!/usr/bin/env python
"""Validate EP40 Lech slot contract."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPDIR = ROOT / "episodes" / "PD-2026-040-lech"
SLOTS = EPDIR / "03_script" / "lech_slots.v001.json"
STUB = EPDIR / "03_script" / "lech_slots.stub.v001.json"


def wc(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)?", text))


def fail(field: str, rule: str, actual=None) -> dict:
    return {"field": field, "rule": rule, "actual": actual}


def main() -> int:
    path = SLOTS if SLOTS.exists() else STUB
    if not path.exists():
        print("FAIL validate_lech_slots: no slots file")
        return 1
    data = json.loads(path.read_text(encoding="utf-8"))
    v = []
    if data.get("schema_version") != "lech_slots.v1":
        print(json.dumps([fail("schema_version", "must be lech_slots.v1", data.get("schema_version"))], indent=2))
        return 2
    for k, expected in {"episode_id": "PD-2026-040-lech", "slug": "lech"}.items():
        if data.get(k) != expected:
            v.append(fail(k, "fixed_value", data.get(k)))
    if data.get("wpm_assumed") != 178.1:
        v.append(fail("wpm_assumed", "fixed 178.1", data.get("wpm_assumed")))
    if len(data.get("title_candidates", [])) != 2:
        v.append(fail("title_candidates", "length 2"))
    for i, item in enumerate(data.get("title_candidates", [])):
        text = str(item.get("text") or "")
        if not 1 <= len(text) <= 60:
            v.append(fail(f"title_candidates[{i}].text", "length 1..60", len(text)))
    if len(data.get("thumb_headlines", [])) != 3:
        v.append(fail("thumb_headlines", "length 3"))
    for i, item in enumerate(data.get("thumb_headlines", [])):
        text = str(item.get("text") or "")
        if item.get("concept_id") != f"T{i + 1}" or text != text.upper() or not 1 <= wc(text) <= 4:
            v.append(fail(f"thumb_headlines[{i}]", "T1..T3, uppercase, 1..4 words", item))
    if len(data.get("acts", [])) != 4:
        v.append(fail("acts", "length 4"))
    if len(data.get("beats", [])) != 23:
        v.append(fail("beats", "length 23", len(data.get("beats", []))))
    if len(data.get("figures", [])) != 17:
        v.append(fail("figures", "length 17", len(data.get("figures", []))))
    starts = [11.6, 131.5, 303.6, 477.4]
    for i, act in enumerate(data.get("acts", [])):
        if round(float(act.get("start_sec", -1)), 1) != starts[i]:
            v.append(fail(f"acts[{i}].start_sec", "timeline", act.get("start_sec")))
        title_card = str(act.get("title_card") or "")
        if title_card != title_card.upper() or not 1 <= len(title_card) <= 28:
            v.append(fail(f"acts[{i}].title_card", "uppercase length 1..28", title_card))
    hook_words = sum(wc(x) for x in data.get("hook", {}).get("lines", []))
    target_sum = sum(data.get("act_word_targets", [])) + data.get("ed_word_target", 0) + hook_words
    if target_sum != data.get("narration_total_words"):
        v.append(fail("narration_total_words", "targets_plus_hook_words", target_sum))
    actual_total = hook_words + sum(wc(a.get("narration", "")) for a in data.get("acts", []))
    for i, (act, target) in enumerate(zip(data.get("acts", []), data.get("act_word_targets", []))):
        actual = wc(act.get("narration", ""))
        if not (target * 0.92 <= actual <= target * 1.08):
            v.append(fail(f"acts[{i}].narration", "word target +/-8%", actual))
    ed_words = wc(data.get("ed", {}).get("payoff_line", "")) + wc(data.get("ed", {}).get("cta_line", "")) + wc(data.get("ed", {}).get("question_line", ""))
    actual_total += ed_words
    if actual_total != data.get("narration_total_words"):
        v.append(fail("narration_total_words", "must equal measured hook+acts+ed words", actual_total))
    if not 2048 <= actual_total <= 2226:
        v.append(fail("narration_total_words", "measured total must be 2048..2226", actual_total))
    if not (data.get("ed_word_target", 0) * 0.80 <= ed_words <= data.get("ed_word_target", 0) * 1.20):
        v.append(fail("ed", "word target loose +/-20%", ed_words))
    ed = data.get("ed", {})
    if path == SLOTS:
        for key, limit in {"payoff_line": 180, "cta_line": 140, "question_line": 120, "next_hook": 120}.items():
            value = str(ed.get(key) or "")
            if not 1 <= len(value) <= limit:
                v.append(fail(f"ed.{key}", f"length 1..{limit}", len(value)))
    if not str(ed.get("question_line") or "").rstrip().endswith("?"):
        v.append(fail("ed.question_line", "must end with ?", ed.get("question_line")))
    facts = data.get("facts", {})
    if set(facts) != {f"F{i:02d}" for i in range(1, 10)}:
        v.append(fail("facts", "must contain exactly F01..F09", sorted(facts)))
    beat_starts = [float(b.get("start", -1)) for b in data.get("beats", [])]
    beat_ends = [float(b.get("end", -1)) for b in data.get("beats", [])]
    if any(e <= s for s, e in zip(beat_starts, beat_ends)) or any(beat_starts[i] < beat_ends[i - 1] for i in range(1, len(beat_starts))):
        v.append(fail("beats", "positive, monotonically increasing non-overlapping windows"))
    acc = data.get("accuracy_lock", {})
    if acc.get("is_supreme_court_decision") is not False:
        v.append(fail("accuracy_lock.is_supreme_court_decision", "must be false", acc.get("is_supreme_court_decision")))
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_lech_accuracy.py"), "--json"], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        v.append(fail("accuracy_lock", "check_lech_accuracy failed", r.stdout[-1000:]))
    if path == SLOTS:
        script = EPDIR / "03_script" / "script.en.v003.md"
        if not script.exists():
            v.append(fail("script.en.v003.md", "required when production slots exist"))
        else:
            sr = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_script_length.py"), str(script), "--json"], cwd=ROOT, capture_output=True, text=True)
            if sr.returncode != 0:
                v.append(fail("script_length", "check_script_length failed", sr.stdout[-1000:]))
    if v:
        print(json.dumps(v, ensure_ascii=False, indent=2))
        return 1
    print(f"PASS validate_lech_slots: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
