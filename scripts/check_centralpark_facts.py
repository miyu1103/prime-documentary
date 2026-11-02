#!/usr/bin/env python
"""EP50 Central Park (The Exonerated Five) factual + wording gate (BLOCKING).

Cloned from check_cleveland_facts.py. Encodes the EP50 seven-constraint discipline
(CODEX_B section 2). Accuracy gate is this ONE script; output 09_package/facts_lock.v001.json.

  R-INNOCENCE  never imply the five were involved; Armstrong only as a REJECTED view.
  R-VICTIM     Trisha Meili / "the jogger" clinical only, no injury detail / imagery.
  R-REYES      established facts only; no Gonzalez-murder month; CP22 needs "believed to".
  R-NUM        figures/AE/thumb/props numbers in the ledger allowed-set; hedged never firm.
  R-FACE       no portrait/face/likeness/mugshot of the five, Meili, Reyes.
  R-DOCHL      dochighlight used ZERO times (kind / beats / layout names).
  R-QUOTE      quoted strings must be verbatim-locked (APPROVED_QUOTES); none locked yet.

Structure exclusions kept 1:1 from the cleveland source (EP45 fix): asset_manifest*.json
is R-NUM exempt (structural counts); start/end/dur/fps/width/height/frames/x/y/index and
*size keys are structural; contextual rules fire when kind != "acttitle". EP50 adds:
script.en.v001.md is R-NUM exempt (narration verbatim). Missing files are logged to skipped[].
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-050-centralpark"
EPDIR = ROOT / "episodes" / EP

# R-FORBID: subject-anchored assertions ONLY. NEVER add the bare words
# attacked/confession/rape/wilding -- they appear in legitimate verbatim context
# (CODEX_B section 2.1 note) and would false-FAIL the caption/script verbatim.
FORBIDDEN = [
    "the five were involved",
    "they were involved",
    "the boys attacked",
    "the five attacked",
    "the teens did it",
    "possibly guilty",
    "may still be guilty",
    "guilty after all",
    "they were wilding",
    "30 hours",
]

FACE_TOKENS = ["portrait", "face of", "likeness", "recognizable face",
               "identifiable face", "mugshot", "deepfake"]
# person-ification of protected real people (R-FACE / R2)
PERSON_TOKENS = ["antron mccray", "kevin richardson", "yusef salaam",
                 "raymond santana", "korey wise", "kharey wise", "trisha meili",
                 "patricia meili", "matias reyes"]

# No verified-verbatim quote is locked yet -> quoted strings are forbidden entirely.
# When the citation pass locks a line, add it here as {verbatim_lower: attribution}.
APPROVED_QUOTES: dict[str, str] = {}

# R-NUM ledger allowed-set (integers). Years group:false; big figures group:true.
ALLOWED_NUMBERS = {
    0, 1, 2, 4, 5, 6, 7, 12, 13, 16, 14, 15, 17, 19, 33,
    1989, 1990, 1991, 2002, 2003, 2012, 2014, 2016, 2019, 2022, 2023,
    85000, 3900000, 7100000, 12200000, 41000000, 6000000000,
}
# medium-confidence CP-IDs that must never be burned firm (R-HEDGE).
MEDIUM_CP = {"CP06", "CP08", "CP17", "CP20", "CP22", "CP28", "CP31", "CP35"}
HEDGE_WORDS = ["~", "roughly", "reportedly", "about", "at least", "believed to", "as much as"]


def target_files() -> list[Path]:
    files: list[Path] = []
    files += [EPDIR / "03_script" / "script.en.v001.md"]
    files += sorted((EPDIR / "03_script").glob("centralpark_facts.v*.json"))
    files += [EPDIR / "04_scenes" / "ai_prompts.v001.md"]
    files += [EPDIR / "08_edit" / "ae_hero" / "beats.json"]
    files += [p for p in sorted((EPDIR / "09_package").glob("*.json")) if not p.name.startswith("facts_lock")]
    files += sorted((EPDIR / "09_package").glob("*.txt"))
    files += sorted((EPDIR / "05_visuals").glob("asset_manifest*.json"))
    files += [ROOT / "remotion" / "src" / "data" / "centralpark_film.json"]
    files += sorted((ROOT / "remotion" / "props").glob("centralpark*.json"))
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
    structural_keys = {
        "start", "end", "dur", "fps", "width", "height", "frames",
        "duration_sec", "durationInFrames", "duration_frames",
        "duration_frames_provisional", "duration_sec_with_bookends",
        "narrationSeconds", "hookSeconds", "openingSeconds", "endcardSeconds",
        "film_offset_sec", "x", "y", "index", "cx", "cy", "r",
    }
    if isinstance(obj, bool):
        return out
    if isinstance(obj, (int, float)):
        out.append(float(obj))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            key = str(k)
            if key in structural_keys:
                continue  # structural (geometry / act index) -- not viewer-facing
            if key.lower().endswith("size"):
                continue  # typography size, not a displayed factual number
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
    facts = sorted((EPDIR / "03_script").glob("centralpark_facts.v*.json"))
    if not facts:
        return {}
    data = json.loads(facts[-1].read_text(encoding="utf-8"))
    if isinstance(data, dict) and "ledger" in data:
        return {row["id"]: row for row in data["ledger"] if isinstance(row, dict) and row.get("id")}
    return data.get("facts", data)


def payload_text(obj: dict[str, Any]) -> str:
    return " ".join(strings(obj)).lower()


def has_hedge(text: str) -> bool:
    return any(h in text for h in HEDGE_WORDS)


def is_guardrail_text(text: str) -> bool:
    t = text.lower()
    return any(marker in t for marker in (
        "do not", "never imply", "never state", "not state", "forbidden",
        "guardrail", "do_not_state_as_fact", "pending final fact-verification",
    ))


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
            positive = block.lower().split(" avoid:", 1)[0].split("negative", 1)[0]
            for token in FACE_TOKENS + PERSON_TOKENS:
                if token in positive:
                    violations.append({"rule": "R-FACE", "where": rel, "text": f"{head}: {token}"})

    # figures[] (film.json) contextual scan
    if path.name == "centralpark_film.json" and isinstance(obj, dict):
        for fig in obj.get("figures") or []:
            kind = str(fig.get("kind") or "")
            text = payload_text(fig)
            if kind == "dochighlight" or "dochighlight" in text:
                violations.append({"rule": "R-DOCHL", "where": rel, "text": text[:120]})
            if kind == "quote":
                q = str(fig.get("quote", "")).strip().lower()
                attr = str(fig.get("attribution", ""))
                if q not in APPROVED_QUOTES or not attr.strip():
                    violations.append({"rule": "R-QUOTE", "where": rel, "text": q[:120]})
            _payload_constraints(rel, kind, text, fig, violations)

    # AE beats contextual scan
    if path.name == "beats.json" and isinstance(obj, dict):
        for beat in obj.get("beats") or []:
            layout = str(beat.get("layout") or "")
            text = payload_text(beat)
            if "dochighlight" in text or layout.lower() == "dochighlight":
                violations.append({"rule": "R-DOCHL", "where": rel, "text": str(beat.get("id", ""))})
            # quoted strings in AE beats
            if '"' in text or "“" in text:
                violations.append({"rule": "R-QUOTE", "where": rel,
                                   "text": f"{beat.get('id')}: quote mark present, no verbatim lock"})
            _payload_constraints(rel, "acttitle" if layout == "ACT_TITLE_CARD" else layout,
                                 text, beat, violations)


def _payload_constraints(rel: str, kind: str, text: str, obj: dict, violations: list[dict[str, str]]) -> None:
    """Shared R-INNOCENCE / R-VICTIM / R-REYES payload discipline. Skips act-title chrome."""
    if kind.lower() in {"acttitle", "act_title_card"}:
        return
    mentions_five = any(t in text for t in ["the five", "the boys", "the teens", "the children",
                                            "mccray", "richardson", "salaam", "santana", "wise"])
    # R-INNOCENCE: five-payload must not assert involvement/guilt without attribution/rejection
    if mentions_five:
        for bad in ["attacked her", "they did it", "were guilty", "are guilty",
                    "committed the attack", "the five attacked", "the boys attacked"]:
            if bad in text:
                violations.append({"rule": "R-INNOCENCE", "where": rel, "text": text[:120]})
                break
    if "armstrong" in text and not any(t in text for t in
                                       ["rejected", "did not adopt", "did not prevail",
                                        "stayed vacated", "remain vacated", "counter-narrative"]):
        violations.append({"rule": "R-INNOCENCE", "where": rel, "text": "Armstrong without rejection frame"})
    # R-VICTIM
    if ("meili" in text or "the jogger" in text):
        for bad in ["raped", "bludgeoned", "skull", "blood loss", "her injuries", "graphic"]:
            if bad in text:
                violations.append({"rule": "R-VICTIM", "where": rel, "text": text[:120]})
                break
    # R-REYES
    if "reyes" in text:
        if "gonzalez" in text and re.search(r"\b(january|february|march|april|may|june|july|august|"
                                            r"september|october|november|december)\b", text):
            violations.append({"rule": "R-REYES", "where": rel, "text": "Gonzalez murder month asserted"})
        if ("two days" in text or "april 17" in text) and "believed to" not in text:
            violations.append({"rule": "R-REYES", "where": rel, "text": "CP22 prior-park claim without 'believed to'"})


def evaluate() -> dict[str, Any]:
    violations: list[dict[str, str]] = []
    skipped: list[str] = []
    facts = latest_facts()
    if facts:
        for fid, row in facts.items():
            if isinstance(row, dict) and row.get("verified") is not True:
                violations.append({"rule": "R-LEDGER", "where": fid, "text": "fact row is not verified"})
            if isinstance(row, dict) and row.get("confidence") == "medium" and not row.get("source") and not row.get("attribution"):
                violations.append({"rule": "R-LEDGER", "where": fid, "text": "medium fact lacks source/attribution"})
    else:
        skipped.append("03_script/centralpark_facts.v*.json (ledger not yet transcribed)")

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
            offenders = [s for s in strings(obj) if token in s.lower() and not is_guardrail_text(s)]
            if offenders:
                violations.append({"rule": "R-FORBID", "where": rel, "text": token})
        if "dochighlight" in hay:
            violations.append({"rule": "R-DOCHL", "where": rel, "text": "dochighlight"})
        # R-NUM: exempt asset_manifest (structural counts) and the narration verbatim script.
        num_exempt = path.name.startswith("asset_manifest") or path.name == "script.en.v001.md"
        if not num_exempt:
            for n in numbers(obj):
                if float(n).is_integer() and int(n) not in ALLOWED_NUMBERS:
                    violations.append({"rule": "R-NUM", "where": rel, "text": str(int(n))})
        check_contextual_rules(path, obj, violations)

    result = {"pass": not violations, "ok": not violations,
              "violations": violations, "skipped": skipped}
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
        print(("PASS" if result["ok"] else "FAIL") + " centralpark_facts")
        for v in result["violations"][:20]:
            print(f"  ! {v['rule']} {v['where']}: {v['text']}")
        if result["skipped"]:
            print(f"  skipped={len(result['skipped'])}")
    return 0 if result["ok"] or args.dryrun else 1


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
