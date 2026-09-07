#!/usr/bin/env python
"""EP46 New Jersey v. T.L.O. factual and wording gate (the six accuracy constraints).

Cloned from scripts/check_cleveland_facts.py (EP45). Keeps the EP45 fixes: R-NUM SKIPS the
asset_manifest (structural counts) and skips the "index" key; acttitle is exempt from content
rules. Accuracy rules adapted to T.L.O.:
  R-OVERCLAIM  - reject "students have no rights" / "schools can search anything"; any card that
                 says "no warrant" / "no probable cause" must also frame that the 4A still applies.
  R-STANDARD   - reasonable suspicion, NOT probable-cause-required.
  R-VOTE       - the vote is 6-3.
  R-POLICE     - footnote 7: a higher standard can return once police are involved (school
                 officials only here).
  R-QUOTE      - only Justice White verbatim, attribution "Justice White, for the Court".
  R-MINOR/FACE - no face / portrait / likeness of the minor.
  R-DOCHL      - no dochighlight anywhere.
Exit 0 = PASS, 1 = FAIL, 2 = schema mismatch. CLI: --json.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-046-tlo"
EPDIR = ROOT / "episodes" / EP

# --- forbidden ASSERTIONS (case-insensitive substring). Curated to the declarative overclaim forms
# only, so the verbatim script's negated/hypothetical phrasings ("not no rights", "does not need
# probable cause", "still applies") are NOT swept in (see CODEX_B spec 2.1 note). ------------------
FORBIDDEN = [
    "students have no rights",
    "students have no fourth amendment rights",
    "the fourth amendment does not apply in school",
    "schools can search anything",
    "search anything they want",
    "search any student at any time",
    "students lose their rights at the schoolhouse door",
    "probable cause is required",
    "requires probable cause",
    "schools need probable cause",
    "reasonable suspicion is not enough",
    "5-4",
    "7-2",
    "9-0",
    "unanimous",
    "unanimously",
    "portrait of t.l.o.",
    "her face",
    "the girl's face",
    "glamorize",
]

# tokens that must never appear in a POSITIVE image prompt (the minor / a real face). Negatives
# ("Avoid: ... portrait ...") are excluded by splitting on " avoid:".
FACE_TOKENS = ["portrait", "face of", "mugshot", "deepfake", "her face", "the girl's face",
               "likeness of", "14-year-old girl shown", "her body"]

# White verbatim only (attribution must be exactly "Justice White, for the Court").
APPROVED_QUOTES = {
    "reasonable grounds for suspecting that the search will turn up evidence that the student has violated or is violating either the law or the rules of the school": "Justice White, for the Court",
    "reasonably related in scope to the circumstances which justified the interference in the first place": "Justice White, for the Court",
    "reasonably related to the objectives of the search and not excessively intrusive in light of the age and sex of the student and the nature of the infraction": "Justice White, for the Court",
}

# R-NUM allowed set (CODEX_B 2.2): 469 / 325 / 1985 / 1984 / 1982 / 15 / 8 / 6 / 3 / 14 / 2 / 7 / 1
# plus 0. Only NARRATIVE figure numbers are checked; the asset_manifest structural counts and the
# acttitle "index" are excluded.
ALLOWED_NUMBERS = {0, 1, 2, 3, 6, 7, 8, 14, 15, 325, 469, 1982, 1984, 1985}

# frames that carry the "the 4A still applies" / lowered-not-eliminated framing (R-OVERCLAIM).
APPLIES_FRAMES = ["applies", "schoolhouse door", "do not shed", "still applies", "not no rights"]


def target_files() -> list[Path]:
    files: list[Path] = []
    files += [EPDIR / "03_script" / "script.en.v001.md"]
    files += sorted((EPDIR / "03_script").glob("tlo_facts.v*.json"))
    files += [EPDIR / "04_scenes" / "ai_prompts.v001.md"]
    files += [EPDIR / "08_edit" / "ae_hero" / "beats.json"]
    files += [p for p in sorted((EPDIR / "09_package").glob("*.json")) if not p.name.startswith("facts_lock")]
    files += sorted((EPDIR / "09_package").glob("*.txt"))
    files += sorted((EPDIR / "05_visuals").glob("asset_manifest*.json"))
    files += [ROOT / "remotion" / "src" / "data" / "tlo_film.json"]
    files += sorted((ROOT / "remotion" / "props").glob("tlo*.json"))
    return files


def strings(obj: Any) -> list[str]:
    out: list[str] = []
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            out.extend(strings(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(strings(v))
    return out


def numbers(obj: Any) -> list[float]:
    out: list[float] = []
    if isinstance(obj, bool):
        return out
    if isinstance(obj, (int, float)):
        out.append(float(obj))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            key = str(k)
            if key in {"start", "end", "dur", "fps", "width", "height", "frames", "duration_sec", "x", "y", "index"}:
                continue  # structural (act "index", geometry) -- not viewer-facing factual figures
            if key.lower().endswith("size"):
                continue
            out.extend(numbers(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(numbers(v))
    return out


def load_any(path: Path) -> Any:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    return path.read_text(encoding="utf-8")


def latest_facts() -> tuple[dict[str, Any], str]:
    facts = sorted((EPDIR / "03_script").glob("tlo_facts.v*.json"))
    if not facts:
        return {}, ""
    data = json.loads(facts[-1].read_text(encoding="utf-8"))
    return data.get("facts", data), data.get("schema_version", "")


def payload_text(obj: dict[str, Any]) -> str:
    return " ".join(strings(obj)).lower()


def scan_hay(path: Path, obj: Any) -> str:
    """The haystack for the substring (R-FORBID / R-DOCHL) scan. Per CODEX_B 2.3, structural /
    machine fields are excluded so they cannot false-positive: the asset_manifest is scanned only
    via its human-authored tags / caption_hint / qc.notes (NOT timestamps / paths / sha256), and
    ai_prompts is scanned POSITIVES-ONLY (a negative "Avoid: glamorized drugs" is a safety cue, not
    a violation)."""
    if path.name.startswith("asset_manifest") and isinstance(obj, dict):
        parts: list[str] = []
        for arr_key in ("stills", "motion", "factory", "overlay"):
            for item in obj.get(arr_key) or []:
                if not isinstance(item, dict):
                    continue
                parts += [str(t) for t in (item.get("tags") or [])]
                if item.get("caption_hint"):
                    parts.append(str(item["caption_hint"]))
                qc = item.get("qc") or {}
                if isinstance(qc, dict) and qc.get("notes"):
                    parts.append(str(qc["notes"]))
        return "\n".join(parts).lower()
    if path.name == "ai_prompts.v001.md" and isinstance(obj, str):
        positives = [block.lower().split(" avoid:", 1)[0] for block in re.split(r"\n-\s+`", "\n" + obj)]
        return "\n".join(positives)
    return "\n".join(strings(obj)).lower()


def check_contextual_rules(path: Path, obj: Any, violations: list[dict[str, str]]) -> None:
    rel = str(path.relative_to(ROOT))
    if path.name == "description.txt":
        hay = path.read_text(encoding="utf-8", errors="ignore").lower()
        if ("student-rights" not in hay) and ("student rights" not in hay):
            violations.append({"rule": "R-OVERCLAIM", "where": rel, "text": "description.txt must include a student-rights explainer line"})
        if not any(t in hay for t in ["legal-aid", "legal aid", "civil-liberties", "civil liberties"]):
            violations.append({"rule": "R-OVERCLAIM", "where": rel, "text": "description.txt must point to a legal-aid / civil-liberties source"})
        if "ai-assisted visualization" not in hay:
            violations.append({"rule": "R1", "where": rel, "text": "description.txt missing AI-assisted visualization disclosure"})

    if path.name == "ai_prompts.v001.md":
        text = path.read_text(encoding="utf-8", errors="ignore")
        for block in re.split(r"\n-\s+`", "\n" + text):
            head = block.split("`", 1)[0].lower()
            positive = block.lower().split(" avoid:", 1)[0]
            for token in FACE_TOKENS:
                if token in positive:
                    violations.append({"rule": "R-FACE", "where": rel, "text": f"{head}: {token}"})
            # T.L.O. named as a person, with a face/portrait within 60 chars
            for m in re.finditer(r"t\.l\.o\.", positive):
                window = positive[m.end():m.end() + 60]
                if any(t in window for t in ["face", "portrait", "likeness", "depicted as a girl"]):
                    violations.append({"rule": "R-MINOR", "where": rel, "text": f"{head}: T.L.O. near face/portrait"})

    if path.name == "tlo_film.json" and isinstance(obj, dict):
        for fig in obj.get("figures") or []:
            kind = str(fig.get("kind") or "")
            text = payload_text(fig)
            if kind == "dochighlight" or "dochighlight" in text:
                violations.append({"rule": "R-DOCHL", "where": rel, "text": text[:120]})
            if kind == "acttitle":
                continue  # act cards are exempt from the content rules
            # R-OVERCLAIM: a card that says "no warrant" / "no probable cause" must frame that the
            # Fourth Amendment still applies (lowered, not eliminated).
            if ("no warrant" in text or "no probable cause" in text) and not any(f in text for f in APPLIES_FRAMES):
                violations.append({"rule": "R-OVERCLAIM", "where": rel, "text": text[:120]})
            # R-STANDARD: "no probable cause" must sit with "reasonable suspicion".
            if "no probable cause" in text and "reasonable suspicion" not in text:
                violations.append({"rule": "R-STANDARD", "where": rel, "text": text[:120]})
            # R-VOTE: the only allowed tally is 6-3.
            if kind == "votetally":
                if int(fig.get("majority", 0)) != 6 or int(fig.get("dissent", 0)) != 3:
                    violations.append({"rule": "R-VOTE", "where": rel, "text": f"majority={fig.get('majority')} dissent={fig.get('dissent')}"})
            # R-POLICE: footnote 7 payloads keep the "school officials only / higher standard" frame.
            if ("police" in text or "law enforcement" in text or "footnote 7" in text):
                if "higher standard" not in text or "school officials" not in text:
                    violations.append({"rule": "R-POLICE", "where": rel, "text": text[:120]})
            # R-QUOTE / R-ATTRIB: White verbatim only.
            if kind == "quote":
                quote = str(fig.get("quote", ""))
                attr = str(fig.get("attribution", ""))
                expected = APPROVED_QUOTES.get(quote)
                if expected is None or expected.lower() not in attr.lower():
                    violations.append({"rule": "R-ATTRIB", "where": rel, "text": quote[:120]})


def evaluate() -> dict[str, Any]:
    violations: list[dict[str, str]] = []
    skipped: list[str] = []
    facts, schema = latest_facts()
    if facts:
        if schema and schema != "tlo_facts.v1":
            return {"pass": False, "ok": False, "schema_mismatch": True,
                    "violations": [{"rule": "R-SCHEMA", "where": "03_script", "text": f"schema {schema} != tlo_facts.v1"}], "skipped": skipped}
        for fid, row in facts.items():
            if not isinstance(row, dict):
                continue
            if row.get("verified") is not True:
                violations.append({"rule": "R-LEDGER", "where": fid, "text": "fact row is not verified"})
            if row.get("confidence") == "medium" and not row.get("attribution"):
                violations.append({"rule": "R-LEDGER", "where": fid, "text": "medium fact lacks attribution"})
    else:
        violations.append({"rule": "R-LEDGER", "where": "03_script", "text": "tlo_facts.v*.json missing"})

    for path in target_files():
        if not path.exists():
            skipped.append(str(path.relative_to(ROOT)))
            continue
        try:
            obj = load_any(path)
        except Exception as exc:  # noqa: BLE001
            violations.append({"rule": "read", "where": str(path.relative_to(ROOT)), "text": str(exc)})
            continue
        hay = scan_hay(path, obj)
        for token in FORBIDDEN:
            # boundary-aware so a forbidden assertion is not matched INSIDE a larger, benign word
            # (e.g. "glamorize" must not fire on the anti-sensational "unglamorized"; the vote token
            # "7-2" must not fire inside a date like "2026-07-22").
            if re.search(r"(?<![A-Za-z0-9])" + re.escape(token) + r"(?![A-Za-z0-9])", hay):
                violations.append({"rule": "R-FORBID", "where": str(path.relative_to(ROOT)), "text": token})
        if "dochighlight" in hay:
            violations.append({"rule": "R-DOCHL", "where": str(path.relative_to(ROOT)), "text": "dochighlight"})
        # R-NUM guards NARRATIVE/rendered numbers only. The asset_manifest is a STRUCTURAL build file
        # (still_body 84 / i2v 16 / factory 92 / overlay 12 counts, act indices, ids) -- never shown
        # to a viewer -- so scanning it is a scope error (false-positives on 84/16/92/12).
        if not path.name.startswith("asset_manifest"):
            for n in numbers(obj):
                if float(n).is_integer() and int(n) not in ALLOWED_NUMBERS:
                    violations.append({"rule": "R-NUM", "where": str(path.relative_to(ROOT)), "text": str(int(n))})
        check_contextual_rules(path, obj, violations)

    desc = EPDIR / "09_package" / "description.txt"
    if not desc.exists():
        violations.append({"rule": "R-OVERCLAIM", "where": "09_package/description.txt", "text": "missing student-rights explainer / AI disclosure"})

    result = {"pass": not violations, "ok": not violations, "violations": violations, "skipped": skipped}
    out = EPDIR / "09_package" / "facts_lock.v001.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    result = evaluate()
    if result.get("schema_mismatch"):
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("SCHEMA-MISMATCH check_tlo_facts")
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["ok"] else "FAIL") + " check_tlo_facts")
        for v in result["violations"][:30]:
            print(f"  ! {v['rule']} {v['where']}: {v['text']}")
        if result["skipped"]:
            print(f"  skipped={len(result['skipped'])}: {result['skipped']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
