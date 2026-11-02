#!/usr/bin/env python
"""EP44 Tekoh factual and wording gate for generated deliverables."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-044-tekoh"
EPDIR = ROOT / "episodes" / EP

FORBIDDEN = re.compile(
    r"miranda is dead|miranda (is )?(abolished|overturned|overruled|gone|struck down)|"
    r"(overturn|overturned|overrule|overruled|reverse|reversed|struck down|kill|killed|end|ended) miranda|"
    r"police (need not|no longer (need|have) to|do ?n.?t (need|have) to) (read|give|recite|warn)|"
    r"no (need|longer need) to read (you )?(your )?rights|"
    r"\b9-0\b|9 to 0|nine to (zero|nothing)|\bunanimous\b|"
    r"no immunity|full victory|total victory|won outright|case closed|case is over|"
    r"sexual assault|sex crime|sex offen|\brape\b|molest|assault victim|\bthe victim\b|"
    r"guilty of|actually guilty|he did it|the crime he committed",
    re.IGNORECASE,
)
BANNED_PORTRAIT = re.compile(
    r"\bportrait\b|\bmugshot\b|likeness of|"
    r"face of (tekoh|terence|vega|carlos|alito|kagan|breyer|sotomayor|roberts|thomas|gorsuch|kavanaugh|barrett)|"
    r"recognizable (real )?person|identifiable face|deepfake",
    re.IGNORECASE,
)
VOTE63 = re.compile(r"\b6\s*[–-]\s*3\b|6 to 3|six to three", re.IGNORECASE)
VOTE_SCOPE = ("one door closed", "exclusion stays open", "reversed", "remanded", "narrow", "not the death of miranda", "miranda stands")
LEDGER_VALUES = {1, 2, 3, 6, 134, 384, 436, 597, 1966, 1983, 2000, 2014, 2022}


def target_files() -> list[Path]:
    files: list[Path] = []
    files += sorted((EPDIR / "03_script").glob("tekoh_facts.v*.json"))
    files += [EPDIR / "04_scenes" / "ai_prompts.v001.md"]
    files += [EPDIR / "08_edit" / "ae_hero" / "beats.json"]
    files += [p for p in sorted((EPDIR / "09_package").glob("*.json")) if not p.name.startswith("facts_lock")]
    files += sorted((EPDIR / "09_package").glob("*.txt"))
    files += sorted((EPDIR / "05_visuals").glob("asset_manifest*.json"))
    files += [ROOT / "remotion" / "src" / "data" / "tekoh_film.json"]
    files += sorted((ROOT / "remotion" / "props").glob("tekoh*.json"))
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
    facts = sorted((EPDIR / "03_script").glob("tekoh_facts.v*.json"))
    if not facts:
        return {}
    data = json.loads(facts[-1].read_text(encoding="utf-8"))
    return data.get("facts", data)


def has_miranda_survival_payload(paths: list[Path]) -> bool:
    for path in paths:
        if not path.exists():
            continue
        try:
            text = "\n".join(strings(load_any(path))).lower()
        except Exception:
            continue
        if "exclusion stays open" in text or "miranda stands" in text or "dickerson stands" in text:
            return True
    return False


def check_numbers(where: str, obj: Any, violations: list[dict]) -> None:
    if isinstance(obj, dict):
        for key, val in obj.items():
            if key in {"start", "end", "dur", "fps", "width", "height", "x", "y", "w", "h"}:
                continue
            check_numbers(where, val, violations)
    elif isinstance(obj, list):
        for val in obj:
            check_numbers(where, val, violations)
    elif isinstance(obj, int) and obj not in LEDGER_VALUES:
        violations.append({"rule": "R-LEDGER", "where": where, "text": f"unapproved number {obj}"})


def evaluate() -> dict:
    violations: list[dict] = []
    skipped: list[str] = []
    facts = latest_facts()
    if facts:
        for fid, row in facts.items():
            if isinstance(row, dict) and not row.get("verified", False):
                violations.append({"rule": "facts_verified", "where": fid, "text": "fact row is not verified"})
    else:
        violations.append({"rule": "R-LEDGER", "where": "03_script", "text": "tekoh_facts.v*.json missing"})

    for path in target_files():
        if not path.exists():
            skipped.append(str(path.relative_to(ROOT)))
            continue
        try:
            obj = load_any(path)
        except Exception as exc:  # noqa: BLE001
            violations.append({"rule": "read", "where": str(path.relative_to(ROOT)), "text": str(exc)})
            continue
        hay = "\n".join(strings(obj))
        rel = str(path.relative_to(ROOT))
        for match in FORBIDDEN.finditer(hay):
            prefix = hay[max(0, match.start() - 64):match.start()].lower()
            if "not " in prefix[-24:] or "does not " in prefix[-32:] or "did not " in prefix[-32:]:
                continue
            violations.append({"rule": "R-FORBID", "where": rel, "text": match.group(0)})
        if path.name != "ai_prompts.v001.md" and BANNED_PORTRAIT.search(hay):
            violations.append({"rule": "R-PORTRAIT", "where": rel, "text": BANNED_PORTRAIT.search(hay).group(0)})

        if path.name == "ai_prompts.v001.md":
            for block in re.split(r"\n-\s+`", "\n" + path.read_text(encoding="utf-8", errors="ignore")):
                head = block.split("`", 1)[0].lower()
                body = block
                positive = re.split(r"\s+Avoid:\s+", body, maxsplit=1, flags=re.IGNORECASE)[0]
                if BANNED_PORTRAIT.search(positive):
                    violations.append({"rule": "R-FACE", "where": rel, "text": head})

        if path.name == "tekoh_film.json" and isinstance(obj, dict):
            check_numbers(rel, obj.get("figures") or [], violations)
            for fig in obj.get("figures") or []:
                fig_text = " ".join(strings(fig)).lower()
                if fig.get("kind") == "dochighlight":
                    violations.append({"rule": "R-DOCHIGHLIGHT", "where": path.name, "text": "dochighlight is banned for EP44"})
                if VOTE63.search(fig_text) and not any(t in fig_text for t in VOTE_SCOPE):
                    violations.append({"rule": "R-VOTE63", "where": path.name, "text": fig_text[:140]})
                if fig.get("kind") == "quote":
                    quote = str(fig.get("quote", ""))
                    attr = str(fig.get("attribution", ""))
                    if "kagan" not in attr.lower():
                        violations.append({"rule": "R-ATTRIB", "where": path.name, "text": quote})
        if path.name == "beats.json" and isinstance(obj, dict):
            check_numbers(rel, obj.get("beats") or [], violations)
            for beat in obj.get("beats") or []:
                text = " ".join(strings(beat)).lower()
                if VOTE63.search(text) and not any(t in text for t in VOTE_SCOPE):
                    violations.append({"rule": "R-VOTE63", "where": rel, "text": beat.get("id", "")})

    output_targets = [EPDIR / "08_edit" / "ae_hero" / "beats.json", ROOT / "remotion" / "src" / "data" / "tekoh_film.json"]
    if any(p.exists() for p in output_targets) and not has_miranda_survival_payload(target_files()):
        violations.append({"rule": "R-SCOPE", "where": "deliverables", "text": "missing Miranda/exclusion survival payload"})

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
        print(("PASS" if result["ok"] else "FAIL") + " tekoh_facts")
        for v in result["violations"][:20]:
            print(f"  ! {v['rule']} {v['where']}: {v['text']}")
        if result["skipped"]:
            print(f"  skipped={len(result['skipped'])}")
    return 0 if result["ok"] or args.dryrun else 1


if __name__ == "__main__":
    raise SystemExit(main())

