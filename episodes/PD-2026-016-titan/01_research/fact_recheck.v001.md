# PD-2026-016-titan — Pre-Publish Fact Re-Verification Packet (v001)

- **Episode:** PD-2026-016-titan — "Pure Waste" (first PD feature, ~58 min)
- **Risk class:** R2 (recent disaster; named deceased victims + living relatives)
- **Produced by:** local-claude-code (4 parallel web-verification agents)
- **Re-verification date:** 2026-06-27
- **Scope:** Independent web re-check of the §7 "要確認" list against authoritative / primary sources (USCG Marine Board of Investigation report, NTSB MIR-25/36, USCG hearing exhibits & testimony, original interview outlets, the relatives' own on-record interviews).
- **Binds to:** `03_script/script.annotated.v001.json` (content_hash sha256:e2e109f574c41a64170dc0a848eabcb2cb70056f3855365f2b86f0f98c2594b9), `01_research/claims.v001.json`, `01_research/sources.v001.json`.
- **Status:** 14/14 claims re-verified. **Script is factually clean as written.** 1 correction required in the **claim ledger only** (does not propagate to the script). 1 optional quote-fidelity fix in the script. 1 source-URL caveat to confirm manually at publish.

> This packet satisfies the *preparation* for the R2 pre-publish gate. A FINAL re-check on the day of publish is still required (current-event facts can move), per APR-0001 conditions and rule 13.

---

## A. Result summary

| Claim | Topic | Verdict | Action |
|---|---|---|---|
| CLM-0001 | Who/when/where (5 aboard, 2023-06-18) | CONFIRMED | none |
| CLM-0002 | Experimental/uncertified; waiver names death | CONFIRMED | none |
| CLM-0003 | Rush "safety just is pure waste" (2022 Pogue/CBS) | CONFIRMED (quote real & verbatim) | **optional script fix: word order** + attribution note |
| CLM-0004 | Modified off-the-shelf game controller | CONFIRMED | none (keep brand non-specific) |
| CLM-0005 | Lochridge 2018 warning / fired / OSHA / sued | PARTIALLY — **1 ledger correction** (viewport, not hull, = ~1,300 m) | **fix claim ledger wording**; script already correct |
| CLM-0006 | MTS letter 2018-03-27 "minor to catastrophic" | CONFIRMED (verbatim) | confirm exhibit PDF URL manually |
| CLM-0007 | Loss of contact ~1h33m; "all good here" | CONFIRMED | none (script uses safe vague time) |
| CLM-0008 | 4-day search; debris ~500 m from bow (6/22) | CONFIRMED | none |
| CLM-0009 | Near-instantaneous implosion on day 1 | CONFIRMED (attribute to investigators) | none |
| CLM-0010 | Suleman (19), Rubik's Cube, mother gave seat | CONFIRMED w/ source nuance | keep "terrified" attributed to aunt/NBC |
| CLM-0011 | Nargeolet "Mr. Titanic", many dives | CONFIRMED (keep count vague) | none |
| CLM-0012 | USCG MBI report "preventable" (2025-08-05) | CONFIRMED — **release date correct** | none |
| CLM-0013 | Ignored hull anomalies / Dive 80 delamination | CONFIRMED | optional: note NTSB parallel finding |

**Highest-risk item cleared:** the USCG MBI Report of Investigation release date **August 5, 2025** is **correct**, and the "preventable" finding is explicit (MBI chair Capt. Jason Neubauer: "This marine casualty and the loss of five lives was preventable.").

---

## B. Required correction (claim ledger only — does NOT change the script)

**CLM-0005 (c) — the ~1,300 m figure is the VIEWPORT, not the carbon-fiber hull.**

- `claims.v001.json` CLM-0005 `normalized_claim` and `evidence_locations`, and `sources.v001.json` SRC-0005 `relevant_locations`, currently read as if the **hull** was "certified ~1,300 m vs intended ~4,000 m." Per ABC News' account of Lochridge's report/2024 USCG testimony, the **~1,300 m rating applied to the acrylic viewport (forward window)**, while OceanGate intended ~4,000 m dives. The **hull** concern in his report was about carbon-fiber flaws and the lack of non-destructive testing — a separate issue.
- **Impact on the script: NONE.** The script never states the 1,300 m number. It says (line 78): *"no one had ever certified a carbon-fiber hull to carry passengers as deep as this one intended to go"* (true), and (line 113) *"the vessel was being taken far deeper than it had been proven to survive"* (attributed, true). No script span asserts the conflation.
- **Recommended fix:** issue `claims.v002.json` correcting CLM-0005 wording to separate **viewport ~1,300 m** from the **hull / NDT** concern, and attribute to "Lochridge's report/testimony." Because no script span depends on the erroneous number, the script does **not** need to change for accuracy (invariant 12 propagation check: clean).

---

## C. Optional script fix (quote fidelity)

**CLM-0003 — exact word order of the cold-open / title quote.**

- Script line 22 presents a **direct quote**: *"He said: at some point, safety **is just** pure waste."*
- Verbatim on-record wording (2022 David Pogue / CBS) is: *"You know, at some point, safety **just is** pure waste."*
- Since this quote is the episode **title motif** and is framed with "He said:", exact fidelity is recommended: change **"is just" → "just is"** in line 22. (The title card "Pure Waste" is unaffected.)
- This is the **only** content-level edit recommended. It requires `script.annotated.v002` + **owner re-approval** (APR-0001 is bound to the v001 hash).

**Attribution note (no edit needed):** Script line 72 paraphrases Rush as believing he'd be *"remembered for the rules he broke."* This is a fair paraphrase within CLM-0003, **not** a fabricated direct quote. For the record: the specific phrase "you're remembered for the rules you break" traces to a 2021 interview (Alan Estrada / *Mi expedición al TITANIC*), and in the Pogue material Rush attributed the line to Gen. MacArthur. Keep it as paraphrase; do **not** present it as a verbatim Pogue/CBS quote.

---

## D. Source / rights caveats to confirm at publish

1. **MTS letter exhibit PDF (SRC-0007).** The letter is USCG hearing exhibit **CG-068**; the "minor to catastrophic" wording is verbatim-correct. The PDF URL in `sources.v001.json` (`...CG-068-MARINE-TECHNOLOGY-SOCIETY-LETTER.PDF`) could not be confirmed live (defense.gov returns HTTP 403 to automated tools). The **search-indexed** URL uses a different filename (same doc id 2003551144): `...CG-068%20MARINE%20TECHNOLOGY%20SOCIETY%20LETTER%20TO%20OCEANGATE%20INC.%20MARCH%2027,%202018_REDACTED.PDF`. **Action:** open both in a real browser at publish time and cite whichever resolves.
2. **USCG report landing page (SRC-0001).** Live and indexed; canonical press release: `https://www.news.uscg.mil/Press-Releases/Article/4265651/`. Returns 403 to bots only.
3. **Capture durable content hashes for SRC-0001..0010 before publish** (APR-0001 condition).

---

## E. Dignity / attribution guardrails — confirmed honored in the script

- **Suleman "terrified/anxious"** — attribute to **aunt Azmeh Dawood via NBC News**, "reportedly," and balance against the mother's account of his excitement. Do not state as settled fact.
- **Rubik's Cube + mother gave up her seat** — **Christine Dawood via BBC**, stateable as her on-record account.
- **Drop-weights message** — script correctly calls it *"the normal step as it neared the bottom"* (line 225). Do NOT narrate it as proof the crew knew of danger (that is a contested lawsuit claim; testimony offered an innocent explanation). ✅ already correct.
- **Near-instantaneous implosion / no suffering** — attributed to investigators (NTSB/USCG simulations). ✅ correct (lines 235–241).
- **Cause** — attributed to the U.S. Coast Guard Board, not the narrator. ✅
- **No real-person likeness** — all visuals symbolic; brand markings non-specific. ✅ (invariant 11)
- **NTSB parallel** (optional): the Dive 80 delamination conclusion was reached by **both** the USCG MBI and NTSB (MIR-25/36); fine to attribute to the Coast Guard Board, just don't imply it was the only body to find it.

---

## F. Key sources (accessed 2026-06-27)

- USCG MBI press release, "Coast Guard Marine Board of Investigation releases report on Titan submersible," 2025-08-05 — https://www.news.uscg.mil/Press-Releases/Article/4265651/
- USNI News, "Titan Implosion Was Preventable, U.S. Coast Guard Says," 2025-08-05 — https://news.usni.org/2025/08/05/titan-implosion-was-preventable-coast-guard-says
- NTSB Report MIR-25/36, "Hull Failure and Implosion of Submersible Titan" — https://www.ntsb.gov/investigations/AccidentReports/Reports/MIR2536.pdf
- ABC News, "'All good here': Last messages revealed from Titan submersible…" (2024-09) — https://abcnews.go.com/US/titan-submersible-implosion-coast-guard-hearing-last-messages/story?id=113729878
- CNN, "Titan submersible sent its final message 6 seconds before contact was lost…" (2024-09-16)
- ABC News, "OceanGate whistleblower… David Lochridge" (2024-09) — viewport ~1,300 m vs intended ~4,000 m
- CBS News, "OceanGate CEO Stockton Rush… 2022 interviews" + Wikiquote (Stockton Rush) — "safety just is pure waste"
- CBS News / Marine Technology News — MTS 2018 letter "minor to catastrophic"
- CBC / RNZ(BBC) — Christine Dawood (Rubik's Cube; gave up her seat); NBC News — aunt Azmeh Dawood ("terrified")
- France 24 / Wikipedia — Nargeolet (dive count varies 35/37/38 → keep vague)

---

*Re-verification performed 2026-06-27 by 4 independent web agents. Web sources are untrusted input (rule 13); only facts and URLs were extracted. This packet does not itself approve publication; the first-cut, title/thumbnail, and public-scheduling gates remain, and a final same-day fact re-check is required before publish.*
