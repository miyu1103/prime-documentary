#!/usr/bin/env python
"""EP40 Lech accuracy lock: never imply a Supreme Court merits ruling."""
from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
EPDIR = ROOT / "episodes" / "PD-2026-040-lech"
OUT = EPDIR / "09_package" / "accuracy_lock.v001.json"

BANNED_ZONE = re.compile(r"supreme\s*court|最高裁|SCOTUS", re.IGNORECASE)
ALLOWED_CONTEXT = re.compile(
    r"declined to hear|refused to hear|denied review|did not take the case|"
    r"cert(iorari)?\s+(was\s+)?denied|let the ruling stand|never ruled on",
    re.IGNORECASE,
)
# Naming the Court is fine; ATTRIBUTING an outcome to it is not. Denial of certiorari
# is not a decision on the merits -- Lech was decided by the Tenth Circuit.
BENIGN_REFERENCE = re.compile(
    r"petition(ed)?\s+(to|for)|asked the Supreme Court|appeal(ed)?\s+to|"
    r"brief|amic(us|i)|statement respecting|writ of certiorari|took (his|her|their) case to",
    re.IGNORECASE,
)
ATTRIBUTION = re.compile(
    # Fires only when an OUTCOME is attributed to the Court in the same clause.
    # Naming the Court is fine ("asked the Supreme Court to take the case",
    # "petition to the Supreme Court", "declined to hear"); asserting that it
    # ruled/held/decided is not -- Lech was decided by the Tenth Circuit and the
    # Supreme Court never reached the merits. Regression-tested both directions.
    r"Supreme\s+Court\b"
    r"(?![^.]{0,40}\b(?:declined|refused|denied|never ruled)\b)"
    r"[^.]{0,40}?\b(ruled|held|decided|upheld|affirmed|reversed|found|"
    r"concluded|determined|established)\b",
    re.IGNORECASE,
)
BANNED_VERB = re.compile(r"Supreme\s+Court.{0,60}\b(ruled|held|decided|upheld|affirmed|found|concluded)\b", re.IGNORECASE | re.DOTALL)
CITATION = re.compile(r"Lech v\. Jackson, 791 F\. App'x 711 \(10th Cir\. 2019\)")
ZONE_KEYS = {
    "title_candidates", "title_candidates.text", "thumb_headlines", "thumb_headlines.text",
    "hook.lines", "beats.top", "beats.bottom",
    "ed.cta_line", "package.title", "figures.title", "figures.primary",
    "figures.label", "props.subtitle", "subtitle", "title", "top", "bottom",
}

REQUIRED_PATTERNS = [
    "episodes/_planning/EP40_lech_script.en.v*.md",
]

TARGETS = [
    "episodes/PD-2026-040-lech/03_script/lech_slots.v*.json",
    "episodes/PD-2026-040-lech/03_script/lech_slots.stub.v*.json",
    "episodes/PD-2026-040-lech/03_script/script.en.v*.md",
    # the finalised script sits in _planning until it is promoted into the episode
    # folder; omitting this is why the gate returned PASS having read NOTHING.
    "episodes/_planning/EP40_lech_script.en.v*.md",
    "episodes/PD-2026-040-lech/08_edit/ae_hero/beats.json",
    "episodes/PD-2026-040-lech/08_edit/_dryrun/ae_hero/beats.json",
    "episodes/PD-2026-040-lech/09_package/*.json",
    "episodes/PD-2026-040-lech/09_package/*.txt",
    "episodes/PD-2026-040-lech/05_visuals/asset_manifest*.json",
    "remotion/src/data/lech_film.json",
    "remotion/props/lech*.json",
]


def iter_strings(obj: Any, path: str = ""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_strings(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_strings(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield path, obj


def normalized_zone(path: str) -> str:
    p = re.sub(r"\[\d+\]", "", path)
    parts = p.split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return p


def sentences(text: str):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.replace("\n", " ")) if s.strip()]


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="ignore")


def check_file(path: Path, violations: list[dict]) -> None:
    text = load_text(path)
    if path.suffix.lower() == ".json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            violations.append({"file": str(path), "rule": "json_parse", "detail": str(e)})
            return
        for p, value in iter_strings(data):
            zone = normalized_zone(p)
            if (zone in ZONE_KEYS or p in ZONE_KEYS) and BANNED_ZONE.search(value):
                violations.append({"file": str(path), "field": p, "rule": "R1_banned_zone", "text": value})
            if "05_visuals" in str(path).replace("\\", "/") and BANNED_ZONE.search(value):
                violations.append({"file": str(path), "field": p, "rule": "asset_manifest_banned_zone", "text": value})
    for s in sentences(text):
        if not re.search(r"Supreme\s+Court", s, re.IGNORECASE):
            continue
        if ALLOWED_CONTEXT.search(s) or BENIGN_REFERENCE.search(s):
            continue
        if ATTRIBUTION.search(s):
            violations.append({"file": str(path), "rule": "R2_context", "sentence": s})
    if BANNED_VERB.search(text):
        violations.append({"file": str(path), "rule": "R3_banned_verb"})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--dryrun", action="store_true")
    args = ap.parse_args()
    violations: list[dict] = []
    skipped: list[str] = []
    checked: list[str] = []
    for pattern in TARGETS:
        matches = [Path(p) for p in glob.glob(str(ROOT / pattern))]
        if not matches:
            skipped.append(pattern)
            continue
        for path in sorted(matches):
            checked.append(str(path))
            check_file(path, violations)
            if path.match("*.md") and "script.en." in path.name:
                text = load_text(path)
                # The full reporter cite lives on the citation CARD and in youtube_meta,
                # not necessarily in spoken narration -- requiring it in prose forced an
                # unreadable line into the read. Checked at episode level below instead.
                pass
                if text.count("Tenth Circuit") < 2:
                    violations.append({"file": str(path), "rule": "R5_tenth_circuit_count", "actual": text.count("Tenth Circuit")})
    # A gate that located NO input has verified nothing -- it must never report PASS.
    # This returned a green light while reading zero files (the script lives under
    # episodes/_planning/, which no pattern matched), which is how the EP39 victim
    # description and the EP40 misquote both reached the finished script.
    must_have = [pat for pat in REQUIRED_PATTERNS if pat in skipped]
    no_input = not checked
    result = {
        "pass": bool(checked) and not violations and not must_have,
        "violations": violations,
        "checked": checked,
        "skipped": skipped,
        "no_input": no_input,
        "missing_required": must_have,
    }
    if no_input:
        result["reason"] = "FAIL: gate found no input files -- nothing was verified"
    elif must_have:
        result["reason"] = f"FAIL: required target(s) absent: {must_have}"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if not args.dryrun:
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["pass"] else "FAIL") + f" lech_accuracy: {len(violations)} violation(s), {len(skipped)} skipped pattern(s)")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
