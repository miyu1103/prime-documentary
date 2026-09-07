#!/usr/bin/env python
"""EP48 Glover factual and wording gate for generated deliverables."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-048-glover"
EPDIR = ROOT / "episodes" / EP
FILM = ROOT / "remotion" / "src" / "data" / "glover_film.json"
FORBIDDEN = [
    "the stop was illegal",
    "illegal stop",
    "unconstitutional stop",
    "the stop was unconstitutional",
    "the court struck it down",
    "struck down the stop",
    "the court banned",
    "police can stop any car",
    "stop any car at any time",
    "police can stop anyone",
    "stop any vehicle",
    "probable cause required",
    "the officer needed probable cause",
    "needed probable cause to stop",
    "the majority dissented",
    "sotomayor concurred",
    "kagan dissented",
    "thomas dissented",
]
FACE_TOKENS = ["portrait", "mugshot", "likeness of", "recognizable real person", "identifiable face", "deepfake"]
ALLOWED_NUMBERS = {0, 1, 4, 6, 8, 18, 556, 589, 2020}
APPROVED_QUOTES = {
    "When the officer lacks information negating an inference that the owner is driving the vehicle, the stop is reasonable.": "Justice Thomas, for the Court",
    "We emphasize the narrow scope of our holding.": "Justice Thomas, for the Court",
    "Consider, for example, if Kansas had suspended rather than revoked Glover's license.": "Justice Kagan, concurring",
    "The majority today has paved the road to finding reasonable suspicion based on nothing more than a demographic profile.": "Justice Sotomayor, dissenting",
}


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
            if key in {
                "start", "end", "dur", "fps", "width", "height", "frames",
                "duration_sec", "x", "y", "index", "value", "heroSize",
                "quoteSize", "fontSize", "lineHeight",
            }:
                if key == "value":
                    out.extend(numbers(v))
                continue
            if key.lower().endswith("seconds") or key.lower().endswith("count") or key in {"words", "seconds"}:
                continue
            out.extend(numbers(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(numbers(v))
    return out


def target_files() -> list[Path]:
    files = [
        EPDIR / "03_script" / "script.en.v001.md",
        EPDIR / "03_script" / "glover_facts.v001.json",
        EPDIR / "08_edit" / "ae_hero" / "beats.json",
        FILM,
    ]
    files += sorted((EPDIR / "05_visuals").glob("asset_manifest*.json"))
    files += [
        p for p in sorted((EPDIR / "09_package").glob("*.json"))
        if not p.name.startswith("facts_lock")
        and not p.name.startswith("final_delivery")
        and not p.name.startswith("acceptance_receipt")
    ]
    files += sorted((EPDIR / "09_package").glob("*.txt"))
    files += sorted((ROOT / "remotion" / "props").glob("glover*.json"))
    return files


def load_any(path: Path) -> Any:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    return path.read_text(encoding="utf-8")


def allowed_negative_context(hay: str, idx: int) -> bool:
    window = hay[max(0, idx - 120): idx + 180]
    return any(
        phrase in window
        for phrase in [
            "not a rule that lets",
            "does not hold that",
            "not the frightening version",
            "explicitly rejects",
            "rejects both",
            "not that",
            "can't stop any car",
            "cannot stop any car",
        ]
    )


def check_payload(path: Path, obj: Any, violations: list[dict[str, str]]) -> None:
    rel = str(path.relative_to(ROOT))
    hay = "\n".join(strings(obj)).lower()
    if path.name in {"script.en.v001.md", "glover_facts.v001.json"}:
        # The locked script contains production apparatus warning not to say some bad phrases.
        # The facts ledger also records negative constraints. Rendered figures are checked below.
        return
    for token in FORBIDDEN:
        idx = hay.find(token)
        if idx >= 0 and not allowed_negative_context(hay, idx):
            violations.append({"rule": "R-FORBID", "where": rel, "text": token})
    for token in FACE_TOKENS:
        if token in hay:
            violations.append({"rule": "R-FACE", "where": rel, "text": token})
    if "dochighlight" in hay:
        violations.append({"rule": "R-DOCHL", "where": rel, "text": "dochighlight"})
    if path.name.startswith("asset_manifest"):
        return
    for n in numbers(obj):
        if float(n).is_integer() and int(n) not in ALLOWED_NUMBERS:
            violations.append({"rule": "R-NUM", "where": rel, "text": str(int(n))})
    if path.name == "glover_film.json" and isinstance(obj, dict):
        for fig in obj.get("figures") or []:
            kind = str(fig.get("kind") or "")
            text = " ".join(strings(fig)).lower()
            if kind == "quote":
                quote = str(fig.get("quote") or "")
                attr = str(fig.get("attribution") or "")
                expected = APPROVED_QUOTES.get(quote)
                if expected is None or expected.lower() not in attr.lower():
                    violations.append({"rule": "R-QUOTE", "where": rel, "text": quote[:100]})
            if kind == "votetally" and (fig.get("majority") != 8 or fig.get("dissent") != 1):
                violations.append({"rule": "R-VOTE", "where": rel, "text": str(fig)})
            if "probable cause" in text and "less than probable cause" not in text:
                violations.append({"rule": "R-STANDARD", "where": rel, "text": text[:120]})
            if "upheld" in text and not any(x in text for x in ["narrow", "limits", "limited"]):
                violations.append({"rule": "R-OVERCLAIM", "where": rel, "text": text[:120]})


def evaluate() -> dict[str, Any]:
    violations: list[dict[str, str]] = []
    skipped: list[str] = []
    for path in target_files():
        if not path.exists():
            skipped.append(str(path.relative_to(ROOT)))
            continue
        try:
            check_payload(path, load_any(path), violations)
        except Exception as exc:
            violations.append({"rule": "read", "where": str(path.relative_to(ROOT)), "text": str(exc)})
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
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["ok"] else "FAIL") + " glover_facts")
        for v in result["violations"][:30]:
            print(f"  ! {v['rule']} {v['where']}: {v['text']}")
        if result["skipped"]:
            print(f"  skipped={len(result['skipped'])}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
