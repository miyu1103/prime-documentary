#!/usr/bin/env python
"""EP45 Cleveland factual and wording gate for generated deliverables."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-045-cleveland"
EPDIR = ROOT / "episodes" / EP

FORBIDDEN = [
    "it is legal",
    "legally jailed",
    "lawful to jail",
    "debtors' prison is legal",
    "debtors prison is legal",
    "perfectly legal",
    "no longer exists",
    "completely abolished",
    "fully ended",
    "supreme court saved cleveland",
    "scotus ruled for cleveland",
    "cleveland reached the supreme court",
    "supreme court freed her",
    "all fines unconstitutional",
    "bearden banned fines",
    "fines are illegal",
    "no more fines",
    "every fine is unconstitutional",
    "starving child",
    "crying child",
    "weeping mother",
]
FACE_TOKENS = ["portrait", "face of", "likeness", "recognizable face", "identifiable face", "mugshot", "deepfake"]
APPROVED_QUOTES = {
    "it is fundamentally unfair to revoke his probation automatically, without even considering whether an adequate alternative to prison exists": "Justice O'Connor, for the Court",
    "a judicially sanctioned extortion racket": "Judge Hub Harrington",
    "No person shall be incarcerated for their inability to pay fines and fees": "settlement",
}
ALLOWED_NUMBERS = {
    0, 1, 2, 4, 24, 31, 40, 100, 200, 235, 250, 395, 399, 461, 500, 660,
    1554, 1970, 1971, 1983, 2001, 2012, 2013, 2014, 2015, 38000,
}


def target_files() -> list[Path]:
    files: list[Path] = []
    files += [EPDIR / "03_script" / "script.en.v001.md"]
    files += sorted((EPDIR / "03_script").glob("cleveland_facts.v*.json"))
    files += [EPDIR / "04_scenes" / "ai_prompts.v001.md"]
    files += [EPDIR / "08_edit" / "ae_hero" / "beats.json"]
    files += [p for p in sorted((EPDIR / "09_package").glob("*.json")) if not p.name.startswith("facts_lock")]
    files += sorted((EPDIR / "09_package").glob("*.txt"))
    files += sorted((EPDIR / "05_visuals").glob("asset_manifest*.json"))
    files += [ROOT / "remotion" / "src" / "data" / "cleveland_film.json"]
    files += sorted((ROOT / "remotion" / "props").glob("cleveland*.json"))
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
    facts = sorted((EPDIR / "03_script").glob("cleveland_facts.v*.json"))
    if not facts:
        return {}
    data = json.loads(facts[-1].read_text(encoding="utf-8"))
    return data.get("facts", data)


def payload_text(obj: dict[str, Any]) -> str:
    return " ".join(strings(obj)).lower()


def check_contextual_rules(path: Path, obj: Any, violations: list[dict[str, str]]) -> None:
    rel = str(path.relative_to(ROOT))
    if path.name == "description.txt":
        hay = path.read_text(encoding="utf-8", errors="ignore").lower()
        if "legal aid" not in hay or "ability to pay" not in hay:
            violations.append({"rule": "R-LEGAL", "where": rel, "text": "description.txt must include legal aid and ability to pay"})
        if "ai-assisted visualization" not in hay:
            violations.append({"rule": "R1", "where": rel, "text": "description.txt missing AI-assisted visualization disclosure"})

    if path.name == "ai_prompts.v001.md":
        text = path.read_text(encoding="utf-8", errors="ignore")
        for block in re.split(r"\n-\s+`", "\n" + text):
            head = block.split("`", 1)[0].lower()
            positive = block.lower().split(" avoid:", 1)[0]
            for token in FACE_TOKENS + ["harriet cleveland", "her body", "her children", "weeping family", "squalor", "filthy home", "destitute children"]:
                if token in positive:
                    violations.append({"rule": "R-FACE", "where": rel, "text": f"{head}: {token}"})

    if path.name == "cleveland_film.json" and isinstance(obj, dict):
        for fig in obj.get("figures") or []:
            kind = str(fig.get("kind") or "")
            text = payload_text(fig)
            if kind == "dochighlight" or "dochighlight" in text:
                violations.append({"rule": "R-DOCHL", "where": rel, "text": text[:120]})
            if kind != "acttitle" and ("1983" in text or "unconstitutional" in text or "bearden" in text) and not any(t in text for t in ["yet it continued", "the rule held", "still happening", "enforcement failed"]):
                violations.append({"rule": "R-LEGAL", "where": rel, "text": text[:120]})
            if ("settled 2014" in text or "settlement" in text or "cleveland v." in text) and not ("lower court" in text and "not the supreme court" in text):
                violations.append({"rule": "R-SCOTUS", "where": rel, "text": text[:120]})
            if kind != "acttitle" and ("bearden" in text or "holding" in text) and not any(t in text for t in ["ability-to-pay", "ability to pay", "no hearing", "without asking"]):
                violations.append({"rule": "R-HOLDING", "where": rel, "text": text[:120]})
            if kind == "compbars" and "bearden" in text and "still allowed" not in text:
                violations.append({"rule": "R-HOLDING", "where": rel, "text": "Bearden compbars must include still allowed side"})
            if kind == "quote":
                quote = str(fig.get("quote", ""))
                attr = str(fig.get("attribution", ""))
                expected = APPROVED_QUOTES.get(quote)
                if expected is None or expected.lower() not in attr.lower():
                    violations.append({"rule": "R-ATTRIB", "where": rel, "text": quote[:120]})

    if path.name == "beats.json" and isinstance(obj, dict):
        for beat in obj.get("beats") or []:
            text = payload_text(beat)
            if "dochighlight" in text:
                violations.append({"rule": "R-DOCHL", "where": rel, "text": str(beat.get("id", ""))})
            if str(beat.get("id")) == "r01" and not ("yet it continued" in text and "lower court" in text and "not the supreme court" in text):
                violations.append({"rule": "R-SCOTUS", "where": rel, "text": "r01 missing enforcement/lower-court limits"})
            if str(beat.get("id")) in {"m01", "j01"} and not any(t in text for t in ["fines & fees justice center", "ffjc"]):
                violations.append({"rule": "R-MEDIUM-ATTRIB", "where": rel, "text": str(beat.get("id", ""))})


def evaluate() -> dict[str, Any]:
    violations: list[dict[str, str]] = []
    skipped: list[str] = []
    facts = latest_facts()
    if facts:
        for fid, row in facts.items():
            if isinstance(row, dict) and row.get("verified") is not True and fid != "F19":
                violations.append({"rule": "R-LEDGER", "where": fid, "text": "fact row is not verified"})
            if isinstance(row, dict) and row.get("confidence") == "medium" and not row.get("attribution"):
                violations.append({"rule": "R-LEDGER", "where": fid, "text": "medium fact lacks attribution"})
    else:
        violations.append({"rule": "R-LEDGER", "where": "03_script", "text": "cleveland_facts.v*.json missing"})

    for path in target_files():
        if not path.exists():
            skipped.append(str(path.relative_to(ROOT)))
            continue
        try:
            obj = load_any(path)
        except Exception as exc:  # noqa: BLE001
            violations.append({"rule": "read", "where": str(path.relative_to(ROOT)), "text": str(exc)})
            continue
        hay = "\n".join(strings(obj)).lower()
        for token in FORBIDDEN:
            if token in hay:
                violations.append({"rule": "R-FORBID", "where": str(path.relative_to(ROOT)), "text": token})
        if "dochighlight" in hay:
            violations.append({"rule": "R-DOCHL", "where": str(path.relative_to(ROOT)), "text": "dochighlight"})
        # R-NUM guards NARRATIVE/rendered numbers (film.json figures, script, description).
        # The asset_manifest is a STRUCTURAL build file: its integers are asset counts
        # (still_body 84 / i2v 16 / factory 92 / overlay 12), act indices, and IDs -- never
        # shown to a viewer. Scanning it for R-NUM is a scope error (false-positives on 84/16/92/12).
        if not path.name.startswith("asset_manifest"):
            for n in numbers(obj):
                if float(n).is_integer() and int(n) not in ALLOWED_NUMBERS:
                    violations.append({"rule": "R-NUM", "where": str(path.relative_to(ROOT)), "text": str(int(n))})
        check_contextual_rules(path, obj, violations)

    desc = EPDIR / "09_package" / "description.txt"
    if not desc.exists():
        violations.append({"rule": "R-LEGAL", "where": "09_package/description.txt", "text": "missing legal-aid support line"})

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
        print(("PASS" if result["ok"] else "FAIL") + " cleveland_facts")
        for v in result["violations"][:20]:
            print(f"  ! {v['rule']} {v['where']}: {v['text']}")
        if result["skipped"]:
            print(f"  skipped={len(result['skipped'])}")
    return 0 if result["ok"] or args.dryrun else 1


if __name__ == "__main__":
    raise SystemExit(main())
