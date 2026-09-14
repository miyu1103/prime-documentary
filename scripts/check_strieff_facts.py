#!/usr/bin/env python
"""EP49 Strieff factual and wording gate for generated deliverables.

Cloned from the EP45 check_cleveland_facts.py (keeping the EP45 structural fixes):
  * asset_manifest*.json is EXCLUDED from R-NUM (its ints are structural asset
    counts 85/16/93/12, never viewer-facing) -- if not path.name.startswith("asset_manifest").
  * numbers() skips structural keys (start/end/dur/fps/width/height/frames/
    duration_sec/x/y/index) and *size keys.
  * contextual rules only fire when kind != "acttitle" (act-title cards exempt).

EP49-specific accuracy 6-constraint rules (§2.3 of CODEX_B):
  R-LEGAL  the stop was ILLEGAL (never "legal"); the rule was narrowed, not abolished
  R-ATTEN  evidence comes in ONLY via the warrant / intervening circumstance
  R-VOTE   5-3, eight seated justices (Scalia vacant); never 6-3 / 8-3
  R-QUOTE  Sotomayor / Kagan verbatim, attributed "dissenting"; no "we are all harmed"
  R-FACE   no Edward Strieff face/portrait/likeness/body; drugs clinical only
  R-DOCHL  no dochighlight anywhere
  R-NUM    burned numbers in {0,1,2 (geometry), 3,4,5,8,232,579,2016}
  R-HEDGE  medium-confidence tokens (Douglas, docket 14-1373, 2006) never burned

VERBATIM SCRIPT EXEMPTION: script.en.v001.md and strieff_facts.v*.json are NOT
scanned for forbidden/context/number substrings (the locked verbatim narration
legitimately contains "the stop was not legal", "fruit of the poisonous tree",
"exclusionary rule", spoken years, etc.). The ledger file is still read
structurally for R-LEDGER. This mirrors how cleveland/glover skip the locked script.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-049-strieff"
EPDIR = ROOT / "episodes" / EP

# Subject-anchored assertion forms only. Per §2.1 note: NEVER add bare
# "legal"/"illegal"/"lawful stop"/"exclusionary rule" -- they collide with the
# verbatim narration ("an illegal stop" contains "legal stop") and with correct
# framings ("the stop was illegal"). Only forms that cannot appear in correct copy.
FORBIDDEN = [
    "the stop was legal",
    "a lawful stop",
    "the stop was lawful",
    "reasonable suspicion existed",
    "the police were allowed to stop",
    "exclusionary rule was abolished",
    "exclusionary rule abolished",
    "abolished the exclusionary rule",
    "struck down the exclusionary rule",
    "exclusionary rule was struck down",
    "the exclusionary rule no longer",
    "sotomayor, for the court",
    "kagan, for the court",
    "the majority dissented",
    "we are all harmed",
    "6-3",
    "six to three",
    "eight to three",
    "8-3",
]
# R-FACE: positive-prompt tokens that would produce a face/body/likeness of a real
# person, or sensationalize the drug. (Negative-prompt usage is allowed -- checked
# only in the positive half of each ai_prompts entry.)
FACE_TOKENS = [
    "portrait", "face of", "likeness", "recognizable face", "identifiable face",
    "mugshot", "deepfake", "his face", "edward strieff",
    "injecting", "needle", "drug use", "overdose", "syringe",
]
# R-HEDGE: medium-confidence tokens that must never be burned on screen.
HEDGE_TOKENS = ["douglas fackrell", "douglas", "14-1373", "2006"]
# R-QUOTE: verbatim dissent excerpts -> the ONLY approved attribution. Matched as a
# contiguous substring (case-insensitive) so trailing punctuation / surrounding
# words are tolerated. Sotomayor / Kagan are ALWAYS "dissenting".
APPROVED_QUOTES = {
    "it implies that you are not a citizen of a democracy but the subject of a carceral state, just waiting to be cataloged":
        "Justice Sotomayor, dissenting",
    "the white defendant in this case shows that anyone's dignity can be violated in this manner":
        "Justice Sotomayor, dissenting",
    "the officer's incentive to violate the constitution thus increases":
        "Justice Kagan, dissenting",
}
# geometry {0,1,2} + the allowed on-screen factual set {3,4,5,8,232,579,2016}.
ALLOWED_NUMBERS = {0, 1, 2, 3, 4, 5, 8, 232, 579, 2016}


def target_files() -> list[Path]:
    """On-screen deliverables scanned for strings/numbers. script.en.v001.md and
    strieff_facts.v*.json are DELIBERATELY excluded (verbatim script exemption)."""
    files: list[Path] = []
    files += [EPDIR / "04_scenes" / "ai_prompts.v001.md"]
    files += [EPDIR / "08_edit" / "ae_hero" / "beats.json"]
    files += [p for p in sorted((EPDIR / "09_package").glob("*.json")) if not p.name.startswith("facts_lock")]
    files += sorted((EPDIR / "09_package").glob("*.txt"))
    files += sorted((EPDIR / "05_visuals").glob("asset_manifest*.json"))
    files += [ROOT / "remotion" / "src" / "data" / "strieff_film.json"]
    files += sorted((ROOT / "remotion" / "props").glob("strieff*.json"))
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
    facts = sorted((EPDIR / "03_script").glob("strieff_facts.v*.json"))
    if not facts:
        return {}
    data = json.loads(facts[-1].read_text(encoding="utf-8"))
    if isinstance(data.get("facts"), dict):
        return data["facts"]
    if isinstance(data.get("ledger"), list):
        return {str(row.get("id")): row for row in data["ledger"] if isinstance(row, dict) and row.get("id")}
    return data


def payload_text(obj: dict[str, Any]) -> str:
    return " ".join(strings(obj)).lower()


def _quote_ok(quote: str, attr: str) -> bool:
    """True iff the quote contains an approved verbatim substring AND carries its
    mapped attribution. Unknown quotes / wrong attributions return False."""
    q = re.sub(r"\s+", " ", str(quote)).strip().lower()
    a = str(attr).lower()
    for verbatim, canonical in APPROVED_QUOTES.items():
        if verbatim in q:
            return canonical.lower() in a
    return False


def _accuracy_payload(kind: str, text: str, rel: str, violations: list[dict[str, str]]) -> None:
    """Shared R-LEGAL / R-ATTEN checks over one figure/beat payload's lower text.
    `kind` is the figure kind (e.g. 'quote') OR the AE layout ('VOTE_SPLIT')."""
    if kind in ("acttitle", "ACT_TITLE_CARD"):
        return  # act-title cards exempt (EP45 fix)
    # R-LEGAL: a payload about the stop's legality must frame it as illegal/conceded.
    if "stop" in text and ("legal" in text or "lawful" in text or "suspicion" in text):
        if not any(t in text for t in ["illegal", "unlawful", "conceded", "no reasonable suspicion", "should never have happened"]):
            violations.append({"rule": "R-LEGAL", "where": rel, "text": text[:120]})
    # R-LEGAL: the exclusionary rule was NARROWED, never abolished/struck down.
    if "exclusionary rule" in text and any(t in text for t in ["abolished", "struck down", "no longer"]):
        violations.append({"rule": "R-LEGAL", "where": rel, "text": text[:120]})
    # R-ATTEN: an EXPLANATORY payload that says the evidence is admitted must credit
    # the warrant / intervening circumstance. The vote card ('VOTE_SPLIT'/'votetally')
    # and kinetic titles just state the outcome, so they are exempt from this branch.
    if "evidence" in text and any(t in text for t in ["stay", "admit", "admissible"]) and kind not in ("kinetic", "votetally", "VOTE_SPLIT"):
        if not any(t in text for t in ["warrant", "intervening", "attenuat"]):
            violations.append({"rule": "R-ATTEN", "where": rel, "text": text[:120]})
    if "the search was legal because the stop was legal" in text:
        violations.append({"rule": "R-ATTEN", "where": rel, "text": text[:120]})


def check_contextual_rules(path: Path, obj: Any, violations: list[dict[str, str]]) -> None:
    rel = str(path.relative_to(ROOT))

    # description.txt must carry the AI-assisted disclosure line (R1 / R-FACE).
    if path.name == "description.txt":
        hay = path.read_text(encoding="utf-8", errors="ignore").lower()
        if "ai-assisted visualization" not in hay:
            violations.append({"rule": "R1", "where": rel, "text": "description.txt missing AI-assisted visualization disclosure"})

    # ai_prompts.v001.md: no face/body/likeness/drug-sensational tokens in the
    # POSITIVE half of any prompt (negative usage after "avoid:" is allowed).
    if path.name == "ai_prompts.v001.md":
        text = path.read_text(encoding="utf-8", errors="ignore")
        for block in re.split(r"\n-\s+`", "\n" + text):
            head = block.split("`", 1)[0].lower()
            positive = block.lower().split(" avoid:", 1)[0]
            for token in FACE_TOKENS:
                if token in positive:
                    violations.append({"rule": "R-FACE", "where": rel, "text": f"{head}: {token}"})
            # "Strieff" within 60 chars of face/portrait -> personification (C-5).
            for m in re.finditer(r"strieff", positive):
                window = positive[m.end():m.end() + 60]
                if "face" in window or "portrait" in window:
                    violations.append({"rule": "R-FACE", "where": rel, "text": f"{head}: strieff + face/portrait"})

    # strieff_film.json figures[] (R-DOCHL / R-LEGAL / R-ATTEN / R-VOTE / R-QUOTE).
    if path.name == "strieff_film.json" and isinstance(obj, dict):
        for fig in obj.get("figures") or []:
            kind = str(fig.get("kind") or "")
            text = payload_text(fig)
            if kind == "dochighlight" or "dochighlight" in text:
                violations.append({"rule": "R-DOCHL", "where": rel, "text": text[:120]})
            _accuracy_payload(kind, text, rel, violations)
            if kind == "votetally":
                if int(fig.get("majority", -1)) != 5 or int(fig.get("dissent", -1)) != 3:
                    violations.append({"rule": "R-VOTE", "where": rel, "text": f"votetally must be majority=5 dissent=3, got {fig.get('majority')}/{fig.get('dissent')}"})
            if kind == "quote":
                if not _quote_ok(fig.get("quote", ""), fig.get("attribution", "")):
                    violations.append({"rule": "R-QUOTE", "where": rel, "text": str(fig.get("quote", ""))[:120]})

    # AE beats.json (R-DOCHL / R-LEGAL / R-ATTEN / R-QUOTE / R-NUM digit scan).
    if path.name == "beats.json" and isinstance(obj, dict):
        for beat in obj.get("beats") or []:
            layout = str(beat.get("layout") or "")
            text = payload_text(beat)
            if "dochighlight" in text or layout.lower() == "dochighlight":
                violations.append({"rule": "R-DOCHL", "where": rel, "text": str(beat.get("id", ""))})
            _accuracy_payload(layout, text, rel, violations)
            # digit scan over the burned display strings (R-NUM for AE text fields).
            for fld in ("hero", "heroText", "main", "left", "right", "top", "bottom", "value"):
                val = beat.get(fld)
                if val is None:
                    continue
                for tok in re.findall(r"\d+", str(val)):
                    if int(tok) not in ALLOWED_NUMBERS:
                        violations.append({"rule": "R-NUM", "where": rel, "text": f"{beat.get('id', '')} {fld}={tok}"})
            if layout == "QUOTE_CARD":
                if not _quote_ok(beat.get("quote", ""), beat.get("attribution", "")):
                    violations.append({"rule": "R-QUOTE", "where": rel, "text": str(beat.get("id", ""))})


def evaluate() -> dict[str, Any]:
    violations: list[dict[str, str]] = []
    skipped: list[str] = []

    facts = latest_facts()
    if facts:
        for fid, row in facts.items():
            if isinstance(row, dict) and row.get("verified") is not True:
                violations.append({"rule": "R-LEDGER", "where": fid, "text": "fact row is not verified"})
    else:
        skipped.append("03_script/strieff_facts.v*.json (ledger not yet generated)")

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
        for token in FORBIDDEN:
            if token in hay:
                violations.append({"rule": "R-FORBID", "where": rel, "text": token})
        if "dochighlight" in hay:
            violations.append({"rule": "R-DOCHL", "where": rel, "text": "dochighlight"})
        # R-HEDGE: medium-confidence tokens must never be burned on screen.
        for token in HEDGE_TOKENS:
            if token in hay:
                violations.append({"rule": "R-HEDGE", "where": rel, "text": token})
        # R-NUM guards NARRATIVE/rendered numbers. asset_manifest is STRUCTURAL
        # (asset counts 85/16/93/12, act indices, IDs) -- scanning it is a scope
        # error (EP45 false-positives on 85/16/93/12), so it is excluded here.
        if not path.name.startswith("asset_manifest"):
            for n in numbers(obj):
                if float(n).is_integer() and int(n) not in ALLOWED_NUMBERS:
                    violations.append({"rule": "R-NUM", "where": rel, "text": str(int(n))})
        check_contextual_rules(path, obj, violations)

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
        print(("PASS" if result["ok"] else "FAIL") + " strieff_facts")
        for v in result["violations"][:20]:
            print(f"  ! {v['rule']} {v['where']}: {v['text']}")
        if result["skipped"]:
            print(f"  skipped={len(result['skipped'])}")
    return 0 if result["ok"] or args.dryrun else 1


if __name__ == "__main__":
    raise SystemExit(main())
