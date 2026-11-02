#!/usr/bin/env python
"""EP43 Caniglia factual and wording gate for generated deliverables."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-043-caniglia"
EPDIR = ROOT / "episodes" / EP

FORBIDDEN = [
    "full victory",
    "total victory",
    "complete victory",
    "total win",
    "won his case",
    "won outright",
    "case closed",
    "case is over",
    "case ended in his favor",
    "final win",
    "warrantless entry is illegal",
    "home is absolutely protected",
    "police can no longer enter",
    "no more welfare checks",
    "police cannot enter your home",
    "no warrantless entry into homes",
]
FACE_TOKENS = ["portrait", "face of", "likeness", "recognizable", "nude", "his body"]
# Verified verbatim fragments from Florida v. Jardines, 569 U.S. 1, 6 (2013) (Scalia, J.):
# "very core"       -> "At the very core of the Fourth Amendment stands the right of a man to retreat into his own home..."
# "first among equals" -> "when it comes to the Fourth Amendment, the home is first among equals."
# Both sit on the SAME page (569 U.S. at 6) already cited in the caniglia facts ledger C07; both attributed to Jardines, never to Payton.
APPROVED_QUOTES = {"very core": "Florida v. Jardines", "first among equals": "Florida v. Jardines"}


def target_files() -> list[Path]:
    files: list[Path] = []
    files += sorted((EPDIR / "03_script").glob("caniglia_facts.v*.json"))
    files += [EPDIR / "03_script" / "script.en.v001.md"]
    files += [EPDIR / "04_scenes" / "ai_prompts.v001.md"]
    files += [EPDIR / "08_edit" / "ae_hero" / "beats.json", EPDIR / "08_edit" / "_dryrun" / "ae_hero" / "beats.json"]
    files += [p for p in sorted((EPDIR / "09_package").glob("*.json")) if not p.name.startswith("facts_lock")]
    files += sorted((EPDIR / "09_package").glob("*.txt"))
    files += sorted((EPDIR / "05_visuals").glob("asset_manifest*.json"))
    files += [ROOT / "remotion" / "src" / "data" / "caniglia_film.json"]
    files += sorted((ROOT / "remotion" / "props").glob("caniglia*.json"))
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
    facts = sorted((EPDIR / "03_script").glob("caniglia_facts.v*.json"))
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
        violations.append({"rule": "R-LEDGER", "where": "03_script", "text": "caniglia_facts.v*.json missing"})

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
                idx = hay.find(token)
                prefix = hay[max(0, idx - 48):idx]
                if "did not say" in prefix or "does not say" in prefix or "not say" in prefix:
                    continue
                violations.append({"rule": "R-FORBID", "where": str(path.relative_to(ROOT)), "text": token})

        if path.name == "description.txt" and "988" not in hay:
            violations.append({"rule": "R-SENSITIVE", "where": str(path.relative_to(ROOT)), "text": "description.txt must include 988"})

        if path.name == "ai_prompts.v001.md":
            for block in re.split(r"\n-\s+`", "\n" + path.read_text(encoding="utf-8", errors="ignore")):
                head = block.split("`", 1)[0].lower()
                body = block.lower()
                positive = body.split(" avoid:", 1)[0]
                for token in FACE_TOKENS + ["edward caniglia"]:
                    if token in positive:
                        violations.append({"rule": "R-FACE", "where": str(path.relative_to(ROOT)), "text": f"{head}: {token}"})
                if head.startswith(("s41.png", "s42.png", "s43.png", "s44.png")):
                    if not any(t in positive for t in ["car", "vehicle", "tow", "trunk", "automobile"]):
                        violations.append({"rule": "R-CADY", "where": str(path.relative_to(ROOT)), "text": head})
                    home_words = any(t in positive for t in ["home", "house", "door", "porch"])
                    explicit_contrast = any(t in positive for t in ["not a home", "never a home", "not a house", "never a house"])
                    if home_words and not explicit_contrast:
                        violations.append({"rule": "R-CADY", "where": str(path.relative_to(ROOT)), "text": f"{head} mixes car prompt with home vocabulary"})

        if path.name == "caniglia_film.json" and isinstance(obj, dict):
            for fig in obj.get("figures") or []:
                fig_text = " ".join(strings(fig)).lower()
                if "988" in fig_text:
                    violations.append({"rule": "R-SENSITIVE", "where": path.name, "text": "988 appears in on-screen figure"})
                if any(t in fig_text for t in ["9-0", "9 to 0", "nine to nothing", "unanimous"]):
                    if not any(t in fig_text for t in ["vacate", "remand", "not a final", "one excuse", "sent back"]):
                        violations.append({"rule": "R-DISPO", "where": path.name, "text": fig_text[:120]})
                if ("cady" in fig_text or "dombrowski" in fig_text) and not any(t in fig_text for t in ["car", "vehicle", "tow", "trunk", "custody"]):
                    violations.append({"rule": "R-CADY", "where": path.name, "text": fig_text[:120]})
                if fig.get("kind") == "quote":
                    quote = str(fig.get("quote", ""))
                    attr = str(fig.get("attribution", ""))
                    if APPROVED_QUOTES.get(quote) != attr:
                        violations.append({"rule": "R-PAYTON", "where": path.name, "text": quote})
        if path.name == "beats.json" and isinstance(obj, dict):
            for beat in obj.get("beats") or []:
                text = " ".join(strings(beat)).lower()
                if "988" in text:
                    violations.append({"rule": "R-SENSITIVE", "where": str(path.relative_to(ROOT)), "text": beat.get("id", "")})
                if any(t in text for t in ["9-0", "9 to 0", "nine to nothing", "unanimous"]):
                    if not any(t in text for t in ["vacate", "remand", "not a final", "one excuse", "sent back"]):
                        violations.append({"rule": "R-DISPO", "where": str(path.relative_to(ROOT)), "text": beat.get("id", "")})
                if ("cady" in text or "dombrowski" in text) and not any(t in text for t in ["car", "vehicle", "tow", "trunk", "custody"]):
                    violations.append({"rule": "R-CADY", "where": str(path.relative_to(ROOT)), "text": beat.get("id", "")})

    desc = EPDIR / "09_package" / "description.txt"
    if not desc.exists():
        violations.append({"rule": "R-SENSITIVE", "where": "09_package/description.txt", "text": "missing 988 disclosure/support line"})

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
        print(("PASS" if result["ok"] else "FAIL") + " caniglia_facts")
        for v in result["violations"][:20]:
            print(f"  ! {v['rule']} {v['where']}: {v['text']}")
        if result["skipped"]:
            print(f"  skipped={len(result['skipped'])}")
    return 0 if result["ok"] or args.dryrun else 1


if __name__ == "__main__":
    raise SystemExit(main())

