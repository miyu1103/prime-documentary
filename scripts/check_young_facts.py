#!/usr/bin/env python
"""EP42 Young factual and wording gate for generated deliverables."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-042-young"
EPDIR = ROOT / "episodes" / EP

FORBIDDEN = ["no" + "-knock", "no knock", "un" + "constitutional", "she changed the law", "changed the law"]
APPROVED_QUOTES = {"still a command": "Justice Scalia, for the majority"}


def target_files() -> list[Path]:
    files: list[Path] = []
    files += sorted((EPDIR / "03_script").glob("young_facts.v*.json"))
    files += [EPDIR / "08_edit" / "ae_hero" / "beats.json", EPDIR / "08_edit" / "_dryrun" / "ae_hero" / "beats.json"]
    files += sorted((EPDIR / "09_package").glob("*.json"))
    files += sorted((EPDIR / "09_package").glob("*.txt"))
    files += sorted((EPDIR / "05_visuals").glob("asset_manifest*.json"))
    files += [ROOT / "remotion" / "src" / "data" / "young_film.json"]
    files += sorted((ROOT / "remotion" / "props").glob("young*.json"))
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


def load_any(path: Path) -> Any:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    return path.read_text(encoding="utf-8")


def latest_facts() -> dict:
    facts = sorted((EPDIR / "03_script").glob("young_facts.v*.json"))
    if not facts:
        return {}
    data = json.loads(facts[-1].read_text(encoding="utf-8"))
    return data.get("facts", data)


def evaluate() -> dict:
    violations: list[dict] = []
    skipped: list[str] = []
    facts = latest_facts()
    if facts:
        for fid, row in facts.items():
            if isinstance(row, dict) and not row.get("verified", False):
                violations.append({"rule": "facts_verified", "where": fid, "text": "fact row is not verified"})
    else:
        violations.append({"rule": "facts_missing", "where": "03_script", "text": "young_facts.v*.json missing"})

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
                violations.append({"rule": "forbidden_word", "where": str(path.relative_to(ROOT)), "text": token})

        if path.name == "young_film.json" and isinstance(obj, dict):
            for fig in obj.get("figures") or []:
                if fig.get("kind") == "quote":
                    quote = str(fig.get("quote", ""))
                    attr = str(fig.get("attribution", ""))
                    if APPROVED_QUOTES.get(quote) != attr:
                        violations.append({"rule": "quote_attribution", "where": path.name, "text": quote})
                if str(fig.get("prefix", "")) == "$" or "$" in " ".join(strings(fig)):
                    label = " ".join(strings(fig)).lower()
                    if "no finding of fault" not in label:
                        violations.append({"rule": "settlement_label", "where": path.name, "text": "money card lacks no finding of fault"})
                if "10-4" in " ".join(strings(fig)) or "10–4" in " ".join(strings(fig)):
                    if "voted down" not in " ".join(strings(fig)).lower():
                        violations.append({"rule": "reform_label", "where": path.name, "text": "10-4 lacks voted down"})
        if path.name == "beats.json" and isinstance(obj, dict):
            for beat in obj.get("beats") or []:
                text = " ".join(strings(beat)).lower()
                if "$" in text and "no finding of fault" not in text:
                    violations.append({"rule": "settlement_label", "where": str(path.relative_to(ROOT)), "text": beat.get("id", "")})
                if "10" in text and "4" in text and "still legal" in text and "rejected" not in text:
                    violations.append({"rule": "reform_label", "where": str(path.relative_to(ROOT)), "text": beat.get("id", "")})
    return {"ok": not violations, "violations": violations, "skipped": skipped}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--dryrun", action="store_true")
    args = ap.parse_args()
    result = evaluate()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["ok"] else "FAIL") + " young_facts")
        for v in result["violations"][:20]:
            print(f"  ! {v['rule']} {v['where']}: {v['text']}")
        if result["skipped"]:
            print(f"  skipped={len(result['skipped'])}")
    return 0 if result["ok"] or args.dryrun else 1


if __name__ == "__main__":
    raise SystemExit(main())
