#!/usr/bin/env python
"""EP47 Atwater factual and wording gate for generated deliverables.

Cloned from check_cleveland_facts.py (EP45). Keeps the EP45 structural fixes
(asset_manifest excluded from R-NUM; index/geometry keys skipped; contextual
rules exempt kind=="acttitle"). Rules adapted to Atwater v. City of Lago Vista:

  C-1 R-DISPO : the arrest was UPHELD 5-4 (constitutional/allowed). Never "illegal".
  C-2/C-3 R-QUOTE : Souter verbatim -> "for the Court" (concession, yet permitted);
                    O'Connor verbatim -> "dissenting". Attribution neutral.
  C-4 : vote 5-4.  C-5/R1 R-FACE : no face/portrait/likeness; children symbolic.
  C-6 R-NUM : only ledger numbers {4,5,25,42,50,318,532,1983,2001} (+0,1,2 structural).
              1997 (A18) and child ages (A19) are medium -> never burned on screen.
  R-DOCHL : no dochighlight anywhere.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-047-atwater"
EPDIR = ROOT / "episodes" / EP

# Subject-anchored assertion forms ONLY. Do NOT add bare "illegal"/"unconstitutional":
# the narration verbatim ("is not that it was illegal", "call it unconstitutional")
# would be swept up as a false positive (see EP47 CODEX_B spec 2.1 note).
FORBIDDEN = [
    "the arrest was illegal",
    "illegal arrest",
    "unconstitutional arrest",
    "the arrest was unconstitutional",
    "the court struck it down",
    "struck down the arrest",
    "the court banned",
    "police cannot arrest you",
    "police can't arrest you for a ticket",
    "souter dissented",
    "o'connor wrote for the court",
    "o'connor, for the court",
    "the majority dissented",
    "poverty porn",
    "crying child",
    "weeping mother",
    "starving child",
]
FACE_TOKENS = ["portrait", "face of", "likeness", "recognizable face", "identifiable face", "mugshot", "deepfake"]
AGE_TOKENS = ["3-year-old", "5-year-old", "aged 3", "aged 5", "three-year-old", "five-year-old"]
APPROVED_QUOTES = {
    "atwater's claim to live free of pointless indignity and confinement clearly outweighs anything the city can raise against it specific to her case.":
        "Justice Souter, for the Court",
    "the court neglects the fourth amendment's express command in the name of administrative ease. in so doing, it cloaks the pointless indignity that gail atwater suffered with the mantle of reasonableness.":
        "Justice O'Connor, dissenting",
}
# Allowed viewer-facing factual numbers (EP47 ledger) + {0,1,2} structural magnitudes.
ALLOWED_NUMBERS = {0, 1, 2, 4, 5, 25, 42, 50, 318, 532, 1983, 2001}
# Structural / timing keys never shown to a viewer as a factual figure.
STRUCT_KEYS = {
    "start", "end", "dur", "fps", "width", "height", "frames", "duration_sec",
    "x", "y", "index", "hookseconds", "narrationseconds", "seconds", "duration",
}


def target_files() -> list[Path]:
    files: list[Path] = []
    files += [EPDIR / "03_script" / "script.en.v001.md"]
    files += sorted((EPDIR / "03_script").glob("atwater_facts.v*.json"))
    files += [EPDIR / "04_scenes" / "ai_prompts.v001.md"]
    files += [EPDIR / "08_edit" / "ae_hero" / "beats.json"]
    files += [p for p in sorted((EPDIR / "09_package").glob("*.json")) if not p.name.startswith("facts_lock")]
    files += sorted((EPDIR / "09_package").glob("*.txt"))
    files += sorted((EPDIR / "05_visuals").glob("asset_manifest*.json"))
    files += [ROOT / "remotion" / "src" / "data" / "atwater_film.json"]
    files += sorted((ROOT / "remotion" / "props").glob("atwater*.json"))
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
            if key.lower() in STRUCT_KEYS:
                continue  # structural (timing, act "index", geometry) -- not a displayed factual figure
            if key.lower().endswith("size"):
                continue  # typography/layout size, not a displayed factual number
            out.extend(numbers(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(numbers(v))
    return out


def load_any(path: Path) -> Any:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    return path.read_text(encoding="utf-8")


def latest_facts() -> dict[str, Any]:
    facts = sorted((EPDIR / "03_script").glob("atwater_facts.v*.json"))
    if not facts:
        return {}
    data = json.loads(facts[-1].read_text(encoding="utf-8"))
    return data.get("facts", data)


def payload_text(obj: dict[str, Any]) -> str:
    return " ".join(strings(obj)).lower()


def face_scan(hay: str, rel: str, violations: list[dict[str, str]]) -> None:
    # R-FACE: no "face"/"portrait" within 60 chars after "atwater"; no child ages.
    for m in re.finditer(r"atwater", hay):
        window = hay[m.end():m.end() + 60]
        if "face" in window or "portrait" in window:
            violations.append({"rule": "R-FACE", "where": rel, "text": window[:60]})
    for token in AGE_TOKENS:
        if token in hay:
            violations.append({"rule": "R-FACE", "where": rel, "text": token})


def check_contextual_rules(path: Path, obj: Any, violations: list[dict[str, str]]) -> None:
    rel = str(path.relative_to(ROOT))

    if path.name == "description.txt":
        hay = path.read_text(encoding="utf-8", errors="ignore").lower()
        if "ai-assisted visualization" not in hay:
            violations.append({"rule": "R1", "where": rel, "text": "description.txt missing AI-assisted visualization disclosure"})

    if path.name == "ai_prompts.v001.md":
        text = path.read_text(encoding="utf-8", errors="ignore")
        for block in re.split(r"\n-\s+`", "\n" + text):
            head = block.split("`", 1)[0].lower()
            positive = block.lower().split(" avoid:", 1)[0].split(" negative:", 1)[0]
            for token in FACE_TOKENS + ["gail atwater", "her body", "her children", "weeping mother", "crying child", "the mother's face"]:
                for m in re.finditer(re.escape(token), positive):
                    pre = positive[max(0, m.start() - 9):m.start()]
                    # legitimate safety negations ("no portrait", "without a face", "not a likeness")
                    if re.search(r"\b(no|without|not|never)\s+(a\s+|any\s+)?$", pre):
                        continue
                    violations.append({"rule": "R-FACE", "where": rel, "text": f"{head}: {token}"})

    if path.name == "atwater_film.json" and isinstance(obj, dict):
        for fig in obj.get("figures") or []:
            kind = str(fig.get("kind") or "")
            text = payload_text(fig)
            if kind == "dochighlight" or "dochighlight" in text:
                violations.append({"rule": "R-DOCHL", "where": rel, "text": text[:120]})
            # R-DATE: never burn 1997 as the decision year inside a figure payload (2001 is decided).
            if "1997" in text and any(w in text for w in ["decided", "decision", "the court held", "ruling"]):
                violations.append({"rule": "R-DATE", "where": rel, "text": text[:120]})
            if kind != "acttitle":
                disp = "arrest" in text and any(w in text for w in ["court", "held", "ruling", "stands"])
                vote = any(v in text for v in ["5-4", "5 / 4", "five to four"])
                if (disp or vote) and not any(w in text for w in ["upheld", "constitutional", "allowed", "could", "stands"]):
                    violations.append({"rule": "R-DISPO", "where": rel, "text": text[:120]})
            if kind == "quote":
                quote = str(fig.get("quote", ""))
                attr = str(fig.get("attribution", ""))
                if not attr.strip():
                    violations.append({"rule": "R-QUOTE", "where": rel, "text": "empty attribution"})
                expected = APPROVED_QUOTES.get(quote.strip().lower())
                if expected is None or expected.lower() not in attr.lower():
                    violations.append({"rule": "R-QUOTE", "where": rel, "text": quote[:120]})
                # C-2 concession: a Souter/majority payload quoting "pointless indignity"
                # must carry the "yet permitted/allowed" frame in the same payload.
                if ("for the court" in attr.lower() or "souter" in attr.lower()) and "pointless indignity" in quote.lower():
                    if not any(w in text for w in ["yet", "permitted", "allowed", "still"]):
                        violations.append({"rule": "R-QUOTE", "where": rel, "text": "Souter concession missing yet/permitted frame"})

    if path.name == "beats.json" and isinstance(obj, dict):
        for beat in obj.get("beats") or []:
            text = payload_text(beat)
            bid = str(beat.get("id", ""))
            layout = str(beat.get("layout", ""))
            if "dochighlight" in text or "dochighlight" in layout.lower():
                violations.append({"rule": "R-DOCHL", "where": rel, "text": bid})
            if "1997" in text and any(w in text for w in ["decided", "decision", "the court held", "ruling"]):
                violations.append({"rule": "R-DATE", "where": rel, "text": bid})
            if bid == "v01" and not ("the arrest stands" in text and "constitutional" in text):
                violations.append({"rule": "R-DISPO", "where": rel, "text": "v01 missing THE ARREST STANDS / constitutional"})
            if bid == "q01":
                attr = str(beat.get("attribution", "")).lower()
                if "dissent" not in attr:
                    violations.append({"rule": "R-QUOTE", "where": rel, "text": "q01 (O'Connor) must be attributed dissenting"})
            if bid == "q02" and "for the court" not in text:
                violations.append({"rule": "R-QUOTE", "where": rel, "text": "q02 (Souter) must be attributed for the Court"})


def evaluate() -> dict[str, Any]:
    violations: list[dict[str, str]] = []
    skipped: list[str] = []
    facts = latest_facts()
    if facts:
        for fid, row in facts.items():
            if isinstance(row, dict) and row.get("verified") is not True:
                violations.append({"rule": "R-LEDGER", "where": fid, "text": "fact row is not verified"})
            if isinstance(row, dict) and row.get("confidence") == "medium" and not row.get("attribution"):
                violations.append({"rule": "R-LEDGER", "where": fid, "text": "medium fact lacks attribution"})
    else:
        violations.append({"rule": "R-LEDGER", "where": "03_script", "text": "atwater_facts.v*.json missing"})

    for path in target_files():
        if not path.exists():
            skipped.append(str(path.relative_to(ROOT)))
            continue
        try:
            obj = load_any(path)
        except Exception as exc:  # noqa: BLE001
            violations.append({"rule": "read", "where": str(path.relative_to(ROOT)), "text": str(exc)})
            continue
        rel = str(path.relative_to(ROOT))
        hay = "\n".join(strings(obj)).lower()
        # STRUCTURAL/PROMPT files are excluded from the global forbidden/number sweeps:
        #  - asset_manifest*: its integers are asset counts (85/16/92/12) and widths, and its
        #    tags are structural -- never shown to a viewer (EP45 fix).
        #  - ai_prompts.v001.md: its "Avoid:" negative list and inline "no portrait/no face"
        #    safety negations legitimately NAME the banned things; scanning them globally is a
        #    scope error. ai_prompts is instead checked by its dedicated positive-prompt scan below.
        global_exempt = path.name.startswith("asset_manifest") or path.name == "ai_prompts.v001.md"
        if not global_exempt:
            for token in FORBIDDEN:
                if token in hay:
                    violations.append({"rule": "R-FORBID", "where": rel, "text": token})
            if "dochighlight" in hay:
                violations.append({"rule": "R-DOCHL", "where": rel, "text": "dochighlight"})
            for n in numbers(obj):
                if float(n).is_integer() and int(n) not in ALLOWED_NUMBERS:
                    violations.append({"rule": "R-NUM", "where": rel, "text": str(int(n))})
            face_scan(hay, rel, violations)
        check_contextual_rules(path, obj, violations)

    desc = EPDIR / "09_package" / "description.txt"
    if not desc.exists():
        violations.append({"rule": "R1", "where": "09_package/description.txt", "text": "missing AI-assisted visualization disclosure"})

    result = {"pass": not violations, "ok": not violations, "violations": violations, "skipped": skipped}
    out = EPDIR / "09_package" / "facts_lock.v001.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--dryrun", action="store_true")
    args = ap.parse_args()
    result = evaluate()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["ok"] else "FAIL") + " atwater_facts")
        for v in result["violations"][:20]:
            print(f"  ! {v['rule']} {v['where']}: {v['text']}")
        if result["skipped"]:
            print(f"  skipped={len(result['skipped'])}")
    return 0 if result["ok"] or args.dryrun else 1


if __name__ == "__main__":
    raise SystemExit(main())
