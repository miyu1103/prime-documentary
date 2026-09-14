# Claim ledgers — what they are for, and how to build the next one

**Canon:** `episodes/PD-2026-062-greene/01_research/claims.v001.json` (first one since EP37).
**Schema:** `schemas/claim-ledger.schema.json` · **Sources:** `schemas/source.schema.json`
**Written 2026-08-12.**

---

## 1. Why the file exists

`verify_onscreen_text.py` is the **only `factual_support` detector on the ship path**
(`scripts/pd_ship_policy.py`), and `factual_support` is one of the four classes allowed to stop a
ship. It reads `01_research/claims.v*.json`, builds a corpus out of the **grade-A claims only**, and
fails the render if any number, quotation, case citation or attributed name burned into the frame
does not trace to that corpus.

If the file is absent the gate **skips**. Until 2026-08-12 the receipt wrote that skip as `true`:
**84 receipts across 19 episodes carry a green that measured nothing.** The gate was never broken.
The episodes simply stopped feeding it.

## 2. The one rule that makes a ledger worth having

> **A claim is traced to a PRIMARY SOURCE, or it is recorded as unsupported. It is never copied
> from the script.**

Back-filling a ledger out of the episode's own script turns the skip into a pass and manufactures
exactly the false green the check exists to prevent: the script would be compared against a
restatement of itself, every token would match, and the receipt would say `true` for a second
reason that isn't a measurement. Two agents refused to build a ledger that way on 2026-08-11 and
**they were right.**

A claim the sources do not support goes in at **grade E** with `status: needs_research` or
`blocked`. Grade E is outside the corpus, so any on-screen text resting on it **fails**. That is
the feature. A red gate on an unsupported claim is the whole point.

`scripts/verify_claim_evidence.py` enforces this mechanically: every grade-A claim must carry a
quoted span in `evidence_locations` that occurs **verbatim** in a primary-source capture you name
on the command line. A claim that quotes nothing, or quotes something the source does not contain,
is reported and the run exits 1. It has a `--selftest` that proves it rejects both.

## 3. Grades, and what each one can do

| Grade | Means | Can it verify on-screen text? |
|---|---|---|
| **A** | A sentence of the primary source says it, and the quote is in `evidence_locations` | **Yes** — this is the corpus |
| **B** | True, but rests on a *verified absence* or a *synthesis of two passages* — no sentence can be quoted for it | **No, by design** |
| **E** | The sources do not support it | **No** — and anything resting on it goes red |

Grade B is not a demotion, it is an honest label. "The opinion never says what became of the three
tenants" is true and important, and there is no sentence to quote for it. Which means **a burned
number that asserts an absence (a stat card reading `0`) cannot be verified by this gate** — see §6.

## 4. Fields the gate actually reads

Only these grade-A fields form the corpus (`_CORPUS_FIELDS` in `verify_onscreen_text.py`):

`normalized_claim` · `allowed_wording` · `evidence_locations` · `counterevidence` · `notes` ·
`temporal_scope` · `geographic_scope` · `units`

`prohibited_wording` is **deliberately excluded** — wording the research forbade must never bless
an on-screen number. Put the primary-source quotation in `evidence_locations`, formatted
`"<locator> | \"<verbatim quote>\""`. That is what makes both gates work off the same string:
`verify_claim_evidence` proves the quote is real, `verify_onscreen_text` uses it as evidence.

## 5. How to build the next one (about an hour)

1. **Find the capture.** The primary source must already be on disk from research —
   `episodes/_planning/measurements/EP<NN>_<slug>_RAW.md` for a case episode. If there is no
   capture, there is no ledger; go get the source first.
2. **Start from the research ledger, never the script.**
   `episodes/_planning/EP<NN>_<slug>_FACTS_LEDGER.v001.md` already has the rows and their loci.
   One claim per row. Carry the row id into `notes` as `[research ledger row GL-nn]` so a reviewer
   can walk back.
3. **Grade honestly.** Quotable sentence → A. Verified absence or synthesis → B. Nothing behind it
   → E with `status: blocked` or `needs_research` and a `notes` line saying what would close it.
   The fact re-check packet (`01_research/fact_recheck.v*.md` §"Still open") is where the grade-E
   rows come from — those are already itemised for you.
4. **Prove it:**
   `py -3.11 scripts/verify_claim_evidence.py --ep <EPID> --source <capture>` → must be 0 untraced.
5. **Run the gate for real:**
   `py -3.11 scripts/verify_onscreen_text.py --ep <EPID>` → read the violations. Each one is a
   burned token no source supports. Fix the **frame**, not the ledger.
6. **Prove the ledger still bites.** Point the gate at a deliberately bad film
   (`--film <red_fixture.json>` with an invented figure, a fabricated quote and a mis-dated
   citation). If a fabrication passes, the ledger is too loose. Do this before trusting the green.
7. `qc.critical_supported` is `false` whenever any grade-E claim exists. Do not set it `true` to
   make a file look finished.

## 6. What this still does not catch (measured on greene, 2026-08-12)

The greene red fixture caught an invented `$1,200,000`, a fabricated quotation (44% overlap), a
mis-dated `GREENE v. LINDSEY · 1979`, an invented `JUSTICE MARSHALL`, and an invented
`2,300,000 EVICTIONS A YEAR`. It **missed** two things, and both are properties of
`verify_onscreen_text`, not of the ledger:

- **A small-integer vote tally.** A burned `6-3` passed, because `6` and `3` occur all over the
  corpus inside reporter citations and footnote numbers. greene's own quarantine Q-13 forbids
  exactly that tally. **A human still has to look at vote counts.**
- **A recombined citation.** `MULLANE v. HOFFMAN` passed: party words are checked one at a time,
  and both *Mullane* and *Hoffman* (from *North Laramie Land Co. v. Hoffman*) are legitimately in
  the corpus. The **pair** is never checked.

Also, by construction: a stat card burning `0` to assert that the record contains nothing rests on
a grade-B verified absence and **will always fail**. Either accept it as a recorded deviation with
an owner APR, or say it on screen without a digit. Do not promote the absence to grade A to make
the number pass — that is manufacturing evidence for a number, which is the thing the gate exists
to stop.
