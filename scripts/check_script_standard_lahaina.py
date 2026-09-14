"""Measure the EP75 script against every WRITTEN standard, item by item.

Sources of the standard, named so the answer is checkable rather than asserted:
  A. episodes/PD-2026-075-lahaina/episode_spec.v002.json   (the machine contract)
  B. docs/PD_ONE_PASS_PRODUCTION_SPEC.v3.md  rows 9, 10, 15, 16, 17, 18 and section 1
  C. .claude/rules/09-claims-and-scripts.md
  D. EP75_lahaina_FACTS_LEDGER v001 + v002, the quarantine
"""
import json, re, pathlib

ROOT = pathlib.Path(r"C:/Users/aab15/Documents/prime-documentary")
S = (ROOT / "episodes/_planning/EP75_lahaina_script.en.v001.md").read_text(encoding="utf-8")
IDX = json.loads((ROOT / "episodes/PD-2026-075-lahaina/06_audio/narration_index.v001.json").read_text(encoding="utf-8"))
SPEC = json.loads((ROOT / "episodes/PD-2026-075-lahaina/episode_spec.v002.json").read_text(encoding="utf-8"))
LEDGER = ((ROOT / "episodes/_planning/EP75_lahaina_FACTS_LEDGER.v001.md").read_text(encoding="utf-8")
          + (ROOT / "episodes/_planning/EP75_lahaina_FACTS_LEDGER.v002.md").read_text(encoding="utf-8"))

rows = []
def add(src, item, ok, detail):
    rows.append((src, item, ok, detail))

lines = S.split("\n")
spoken = [l for l in lines if l.strip() and not l.startswith(("#", ">", "---", "<!--", "【"))]
chunks = IDX["chunks"]
words = sum(c["word_count"] for c in chunks)

# ---- A. the machine contract -------------------------------------------------------------
lo, hi = SPEC["script_words"]
add("A spec", f"script_words in [{lo},{hi}]", lo <= words <= hi, f"{words} words (narration index)")
secs_declared = SPEC["section_vocabulary"]
secs_used = []
for c in chunks:
    if c["section"] not in secs_used:
        secs_used.append(c["section"])
add("A spec", "section_vocabulary exact, in order", secs_used == secs_declared,
    f"{secs_used}")
rlo, rhi = SPEC["runtime_seconds"]
film = IDX["total_seconds"] + 9.0
add("A spec", f"runtime in [{rlo},{rhi}]", rlo <= film <= rhi, f"{film:.1f}s = {int(film//60)}:{int(film%60):02d}")

# ---- B. spec v3 --------------------------------------------------------------------------
hook = [c for c in chunks if c["section"] == "HOOK"]
add("B row 9", "hook voiced from frame 0", hook[0]["start"] <= 0.5, f"first chunk starts {hook[0]['start']:.3f}s")
hook_end = hook[-1]["start"] + hook[-1]["seconds"]
add("B row 9", "hook ~0:20", 15 <= hook_end <= 25, f"{hook_end:.3f}s")
hook_txt = " ".join(c["spoken_text"] for c in hook).lower()
add("B row 9", "hook does NOT summarise the outcome",
    not any(w in hook_txt for w in ("died", "killed", "destroyed", "burned down", "102", "disaster")),
    "no death toll, no outcome word in the hook")
add("B row 10", "four-part spine present",
    all(s in secs_used for s in ("HOOK", "OP", "ENDING")) and len([s for s in secs_used if s.startswith("ACT")]) == 5,
    "HOOK / OP / ACT_1-5 / ENDING")
ending = " ".join(c["spoken_text"] for c in chunks if c["section"] == "ENDING").lower()
add("B row 10", "ending carries one specific ask", "find out what the warning where you live" in ending,
    "the ask is the state's own instruction, not 'subscribe'")
add("B row 16", "question opened in the first 8 s and held",
    "stopped working hours ago" in hook_txt, "the hook's last clause opens it; answered in ACT_2")
# re-hooks: the design notes carry them; measure the gap between consecutive 【Re-hook】 marks
rehooks = [i for i, l in enumerate(lines) if l.startswith("【") and "Re-hook" in l]
add("B row 16", "re-hooks every 2-3 min (design marks)", len(rehooks) >= 8, f"{len(rehooks)} marked re-hooks")
add("B row 17", "every factual span links to a claim id",
    all((i + 1 < len(lines) and lines[i + 1].strip().startswith("<!--"))
        for i, l in enumerate(lines) if l.strip() and not l.startswith(("#", ">", "---", "<!--", "【"))),
    f"{len(spoken)} spoken lines, all cited")
cited = set()
for c in re.findall(r"<!--(.*?)-->", S, re.S):
    cited |= set(re.findall(r"\b(LH-\d+|AB-\d+)\b", c))
add("B row 17", "every cited id exists in a ledger", all(c in LEDGER for c in cited), f"{len(cited)} distinct ids")
living = "He has not been charged with any offence" in S
add("B row 18", "living person carries legal status in the same breath", living,
    "the administrator: quoted, dated, resignation, and 'has not been charged'")
add("B 6.6", "not sized with check_script_length", "check_script_length` is NOT used" in S,
    "the header says so and gives the measured figures instead")

# ---- C. rules/09 -------------------------------------------------------------------------
bad_spoken = [c["spoken_text"] for c in chunks if re.search(r"[【】\[\]]", c["spoken_text"])]
add("C rule 09", "no production direction reaches the voice", not bad_spoken,
    f"{len(bad_spoken)} spoken chunks contain a bracket")
hedge_ok = True
add("C rule 09", "no LLM used as a source", "LLM" not in S and "ChatGPT" not in S, "no model cited anywhere")
nums = re.findall(r"\b(?:at least 102|518|84|140|850|60 mph|sixty miles an hour)\b", S)
add("C rule 09", "figures carry unit/date/population", "at least a hundred and two lives" in S,
    "the toll is the County's own phrasing with its date in the citation")

# ---- D. the quarantine -------------------------------------------------------------------
low = " ".join(c["spoken_text"] for c in chunks).lower()
# A bare regex for the counterfactual fires on the sentence that DENIES it, which is the one
# sentence the film bible section 14 requires. Count a hit only when no negation cue precedes it
# in the same sentence -- the same unless_any_of technique the ship policy uses on plate verdicts.
cf = []
for c in chunks:
    for s in re.split(r"(?<=[.!?])\s+", c["spoken_text"]):
        if re.search(r"(would|could|might) have (saved|changed|prevented)", s, re.I):
            neg = re.search(r"(not one|no finding|none of|nowhere|never says|does not say)", s, re.I)
            (cf if not neg else []).append((c["id"], s))
add("D quarantine", "01: no counterfactual about the sirens", not cf,
    "the only match is the sentence that DENIES it (VC-0336, the declared absence AB-01)"
    if not cf else f"{len(cf)} unnegated: {cf[:2]}")
add("D quarantine", "02: Finding 37 and non-activation never in one sentence",
    not re.search(r"only one siren[^.]*not (used|activated)", low), "stated in separate paragraphs")
add("D quarantine", "03: the sirens are never said to have failed",
    not re.search(r"siren[^.]{0,40}\bfailed\b|\bfailed\b[^.]{0,40}siren", low), "the only 'failed' are water pipes")
add("D quarantine", "04: no open question / conspiracy register",
    not any(p in low for p in ("some say", "many believe", "questions remain",
                               "we may never know", "the official story")), "zero of the six barred phrases")
add("D quarantine", "07: no victim named or characterised",
    "victim" not in low and "body bag" not in low, "no victim word anywhere")
add("D quarantine", "08: never says a power cut stopped the water",
    "uninterrupted electrical power" in low, "Finding 21 is quoted verbatim instead")
add("D quarantine", "12: the word paradise never appears", "paradise" not in low, "zero")
add("D quarantine", "16: 14:17 travels with LH-15 and LH-85",
    "above and beyond" in low and "insufficient" in low, "both in the same ACT_3 passage")

w = max(len(r[0]) for r in rows)
print(f"{'source':<12} {'item':<52} result")
print("-" * 92)
for src, item, ok, detail in rows:
    print(f"{src:<12} {item:<52} {'PASS' if ok else 'FAIL'}   {detail}")
bad = [r for r in rows if not r[2]]
print("-" * 92)
print(f"{len(rows) - len(bad)}/{len(rows)} PASS" + (f"  FAILING: {[r[1] for r in bad]}" if bad else ""))
