# PD-2026-075-lahaina — Pre-Publish Fact Re-Verification Packet (v001)

- **Episode:** PD-2026-075-lahaina — the Lahaina fire, Maui, 8 August 2023 (30 min)
- **Risk class:** **R3** — at least 102 real deaths three years ago; living families; **litigation
  that is still moving and that will move again during this film's publication month**; and a topic
  that shares its search terms with an active conspiracy audience.
- **Produced by:** Claude (Opus 5, Claude Code), 2026-08-21, by live retrieval
- **Binds to:** `episodes/_planning/EP75_lahaina_script.en.v001.md`,
  `EP75_lahaina_FACTS_LEDGER.v001.md` + `.v002.md`,
  `episodes/PD-2026-075-lahaina/episode_spec.v001.json`
- **Status:** **NOT CLEARED FOR PUBLISH.** Six items require resolution before the render, and §3's
  settlement block requires re-verification on the day of publish — not once, but every time the
  packaging or the schedule is touched.

> This packet is the *preparation* for the R3 pre-publish gate, not the gate itself. §6 is what the
> publish-day check has to cover.

---

## 1. What was actually read, and what was not

**Read in full text, across the research session and this one:**

| source | how |
|---|---|
| `SRC-0001` FSRI Phase Two — **all 84 findings and recommendations**, Appendix 6.1 | read in full, 2026-08-21 |
| `SRC-0002` / `SRC-0003` the Attorney General's own Phase Two and Phase One press decks | read in full |
| `SRC-0004` County of Maui / MFD with ATF — origin-and-cause news release, 3 October 2024 | read in full |
| `SRC-0005` HI-EMA's own outdoor warning siren page | read |
| **`SRC-0009` FSRI Phase One — the comprehensive timeline report** | **read in full text 2026-08-21** (figshare deposit; `ag.hawaii.gov` 403s. **The PDF's font encoding shifts every character down 29 code points and turns every digit into a control character** — an undecoded read shows a timeline report with no numbers in it) |
| `SRC-0012` Maui Now, 13 February 2026 · `SRC-0013` Honolulu Star-Advertiser, 16 August 2026 | fetched and read 2026-08-21 |

**NOT read, and the film says so (AB-05, revised):**

| not read | consequence |
|---|---|
| `SRC-0010` Phase Three, the Forward-Looking Report (14 January 2025) | The film makes no claim about what has been recommended for the future beyond Finding 37's own recommendation text |
| `SRC-0011` the full MFD/ATF Origin and Cause Report | **Every causation row is from the County's own release of it** (LH-11, LH-14, LH-16, LH-17), quoted and dated. A row that turns out to be the County paraphrasing ATF would be a defect |
| The online 12,000-line composite timeline dataset | Not needed; Phase One's narrative carries every time the film uses |
| Any interview with a resident or survivor | **The film contains no survivor account. Deliberate**, and it is why ⛔-07 is absolute |

---

## 2. The six items that must be resolved BEFORE the render

| # | item | why it cannot wait |
|---|---|---|
| **R-1** | **The morning ignition minute.** The County/ATF release says **06:34** (LH-11); Phase One's own summary says **06:35** (LH-223). The script narrates 06:34 and attributes it. **Confirm no figure card, caption or on-screen text anywhere in the build carries 06:35**, and that no card puts both on screen | A figure card with a contested minute is a factual defect burned into the picture |
| **R-2** | **The rekindle minute.** The County says "approximately **14:52**" (LH-13); Phase One's reference points put the PM fire at **14:55** (LH-220, LH-230). **Both are in the script, each attributed to its own source.** Confirm no card merges them into one number and no card presents either as the other's | Two sources, two numbers, one picture — this is exactly how a third claim gets invented |
| **R-3** | **⛔-02 in the picture.** Finding 37 ("one siren operable within the burn perimeter") and the fact that the sirens were not activated are **two facts from two sources**. Confirm **no figure card, caption or thumbnail puts them on the same card**, and that the word *failed* appears nowhere in the built `film.json` | The script is clean. The picture is where this fails |
| **R-4** | **No generated glyph anywhere.** Every document, form, log, screen, alert and noticeboard plate in the image order is blank by design — `H024 H025 H031 H038 H084 H088 H112 H113 H114 H120 H122 H124 H128 H129`. **Confirm on the delivered plates, not on the order.** `fabricated_record` is a ship-blocking class | Discovered after render, this costs a re-render |
| **R-5** | **No number on screen that is not a ledger row (⛔-10).** In particular: no acreage, no structure count, no measured wind speed, no siren count other than Finding 37's, and **no death toll other than the County's "at least 102" with its date** | The narration is clean; figure cards are generated separately and are where a stray number enters |
| **R-6** | **The ACT_3 grade.** The afternoon of 8 August is `S` — **grey-brown, not orange**. Confirm no staged clip and no colour pass puts a warm hero light on it | Not a craft preference: an orange grade falsifies the film's central visual fact, and the film argues from what the day looked like |

---

## 3. SECONDARY rows that carry weight — re-check before publish

These are narrated and none is from a primary document. Each needs one independent confirmation.

| row | claim | where it lands | priority |
|---|---|---|---|
| **LH-38** | **The head of the county emergency management agency said he did not regret not sounding the sirens, gave his reason, and resigned the following day citing health reasons** | ACT_5 | **HIGHEST — see below** |
| LH-05 | More than 400 sirens statewide, about 80 on Maui; four in the Lahaina area, all sited by the shore | ACT_1 and ACT_5 | high |
| LH-37 | The County sued four carriers in May 2024; says it sent at least 14 alert messages; says all 21 West Maui towers experienced total failure | ACT_3 | high |
| LH-110 | The death-toll revisions, and the 102nd death confirmed June 2024 | ACT_4 uses **only the County's "at least 102" (LH-19, primary)** | medium |
| LH-111, LH-112, LH-114 | The $4.037 bn settlement; the February 2026 intervention ruling; the June 2026 award notices | ACT_5 | high |
| **LH-115, LH-116** | **No payment has been made; the fee appeal is pending at the Hawaiʻi Supreme Court** | ACT_5 | **VOLATILE — §3.1** |

### 3.1 The one that will be wrong before this film publishes

**`LH-115` is a statement about a live appeal.** As of **2026-08-21** no settlement payment had been
made and the fee appeal had been at the Hawaiʻi Supreme Court since 5 August 2026. Counsel expected a
ruling **as early as September 2026** (LH-116). **This film is scheduled to publish into that window.**

The script is written so that this ages honestly: it says *"As of August twenty twenty-six, no payment
has been made"* — the date is spoken, in the sentence, so a later ruling makes the film **dated, not
false**. That is the mitigation, and it is deliberate.

**It is not a substitute for the check.** ⛔-11 requires §10 of ledger v002 to be re-verified:

1. before the packaging is written,
2. before the video is scheduled,
3. and again if the schedule slips.

### 3.2 RESOLVED 2026-08-21 — the quote was re-read, not cut

**`LH-38` is the only place this film quotes a living, identifiable individual's words about the
decision** — and `SRC-0006` is marked in the ledger as **"search summaries only — not read in a
primary record."** The film attributes it by role, dates it, states that he resigned the next day, and
states that he has not been charged with any offence, which is what `forbidden_claims` requires.

**RESOLUTION.** The first option was taken. `SRC-0014` — CBS News, "Maui emergency chief resigns
following criticism of wildfire response", 18 August 2023 — was **fetched and read on 2026-08-21**,
and ledger v002 §12 replaces `LH-38` with four rows read in that source: `LH-120` (the three-word
answer, "I do not"), `LH-121` (his stated reason, verbatim), `LH-122` (the resignation the next day,
17 August, health reasons) and `LH-123` (the absence of any charge). **The script now carries the two
quotations verbatim instead of the paraphrase**, and v001's clause that the sirens "are used
primarily for tsunamis" — which is **not** in the read source — has been **removed from the script and
barred from narration**.

**What is still open here:** nothing for this row. The alternative below is recorded because it was
the fallback and because it remains true — if any doubt arises about the quotation at publish, it can
still be cut without touching the film's argument.

- retrieve the statement from a named outlet's own page or from the recorded news conference and
  upgrade the row **(DONE)**, **or**
- **cut the quotation** and keep only the fact that the sirens were not activated, which the film's
  argument does not depend on.

**The film's argument survives the cut.** Finding 38 carries that beat, and it is primary.

---

## 4. Living persons — the exposure map

| person | status in the film | check |
|---|---|---|
| **The emergency-management administrator** | **Never named.** Appears as "the head of the county's emergency management agency", quoted, dated, with his resignation and the fact that he has not been charged in the same passage | Confirm no caption, figure card or description names him |
| **The EOC director, the duty officer and the EOC staff** (named in Phase One) | **Not in the film at all**, by name or by description | Confirm ⛔-17 holds in the built film |
| **The police officer at the gate** | Narrated as an **action**, never as a biography, never named | Confirm no caption identifies him |
| **The ladder-company operator whose house burned** (Phase One p.63) | **Deliberately not narrated.** It is a true, moving, sourced detail about a real identifiable person's private loss, and the film does not need it | Confirm it has not been reintroduced in a later revision |
| **The fire chief and assistant chief** (LH-14, LH-15) | Quoted **by role**, from the County's own release, dated | Confirm no name appears on a card |
| **The Attorney General** (LH-91) | Quoted from her own published deck; **named on screen with office and date**, which is correct for a public official quoting herself in an official capacity | Confirm the on-screen attribution carries the office and the date, not just the name |
| **Any of the 102 who died** | **None named, none shown, none characterised.** No burned vehicle presented as occupied | Confirm on the delivered plates and in the built cuts — image order §6 |
| **Residents of Lahaina** | No individual appears | Confirm no plate resolves as a specific real person |

---

## 5. The conspiracy-adjacency check — specific to this episode

No other PD episode has needed this section. It is not optional here.

1. **No question is raised and left open.** Sweep the built film for any span where the narration
   poses something the next ninety seconds do not answer.
2. **The banned register does not appear** in narration, captions, cards, title, thumbnail or
   description: *some say*, *many believe*, *questions remain*, *we may never know*, *the official
   story*, *what they don't want you to know*.
3. **The cause is stated plainly, early, and attributed** — ACT_2, from the County and ATF, with the
   classification **Accidental**. Confirm it survives into the description above the fold, because the
   description is where a viewer arriving from that material lands first.
4. **No plate contains anything that could read as a beam, a directed energy source or an unexplained
   light.** The image order bars it; confirm it on the delivered images.

---

## 5.5 THE SCRIPT MEASURED AGAINST THE WRITTEN STANDARD — 25/25, and one named deviation

Run 2026-08-21 against the **delivered narration index**, not against the markdown, so what is
measured is what the voice actually says. The standard is in four places and each row names its own:

| source | item | result |
|---|---|---|
| `episode_spec.v002` | `script_words` in [4900, 5400] | **5,338** |
| `episode_spec.v002` | `section_vocabulary` exact and in order | HOOK / OP / ACT_1–5 / ENDING |
| `episode_spec.v002` | runtime in [1740, 1920] | **1,866.4 s = 31:06** |
| spec v3 row 9 | hook voiced from frame 0 | first chunk starts **0.000 s** |
| spec v3 row 9 | hook ≈ 0:20 | **20.266 s** |
| spec v3 row 9 | hook does not summarise the outcome | no toll, no outcome word in the hook |
| spec v3 row 10 | four-part spine | present |
| spec v3 row 10 | ending carries one specific ask | the state's own instruction, not "subscribe" |
| spec v3 row 16 | a question opened in the first 8 s and held | the hook's last clause; answered in ACT_2 |
| spec v3 row 16 | re-hooks every 2–3 min | **10** marked |
| spec v3 row 17 | every factual span links to a claim id | **221 spoken lines, all cited** |
| spec v3 row 17 | every cited id exists in a ledger | **109 distinct ids, all resolve** |
| spec v3 row 18 | a living person carries their legal status in the same breath | quoted, dated, resignation, "has not been charged" |
| spec v3 §6.6 | not sized with `check_script_length` | header states the measured figures instead |
| rule 09 | no production direction reaches the voice | **0 of 357 chunks contain a bracket** |
| rule 09 | no LLM used as a source | none cited |
| rule 09 | figures carry unit and date | the toll is the County's own phrasing with its date |
| ⛔-01 | no counterfactual about the sirens | the only counterfactual-shaped sentence is the one that **denies** it (AB-01) |
| ⛔-02 | Finding 37 and the non-activation never in one sentence | separate paragraphs, separate sources |
| ⛔-03 | the sirens are never said to have failed | the only "failed" in the film is household plumbing |
| ⛔-04 | no open question, no conspiracy register | **zero** of the six barred phrases |
| ⛔-07 | no victim named or characterised | the word does not appear |
| ⛔-08 | never says a power cut stopped the water | Finding 21 quoted verbatim instead |
| ⛔-12 | the word *paradise* never appears | zero |
| ⛔-16 | 14:17 travels with LH-15 and LH-85 | both in the same ACT_3 passage |

**25/25.**

**The instrument lied twice before it agreed, and both are worth recording.** The ⛔-01 check first
fired on *"And not one of them says that sounding the siren would have changed the outcome"* — the
sentence the film bible §14 **requires**, because it is the declared absence. A bare regex for a
counterfactual cannot tell an assertion from its denial. Corrected to look for a negation cue in the
same sentence, it still failed — because the shell heredoc that wrote the checker had turned its two
`\b` word boundaries into literal **backspace bytes (0x08)**, so the negation pattern could never
match anything. **Both times the script was right and the measurement was wrong**, which is the whole
reason a failing check gets read before it gets believed.

### 5.6 The one deviation, named rather than hidden

`PD_ONE_PASS_PRODUCTION_SPEC.v3` §5 item 1 asks for `EPnn_FILM_BIBLE.vNNN.md` **+
`script.annotated.vNNN`**. **This episode has no annotated script.** Measured before writing that
down: the newest annotated script in the repository is **EP31**, and **EP62, EP66, EP69, EP70, EP71
and EP72 all have zero** — including EP72, which is this episode's reference build. The convention
stopped about forty episodes ago and the manual still names it, the same way it still names a
`03_script` directory no recent episode has.

**This is deliberate, not an oversight, and the argument is that an annotated script would add
nothing the record does not already hold**: `narration_index.v001.json` carries all 357 chunks with
their section and their exact spoken text, and every spoken line in the markdown carries its ledger
row id one line beneath it. A second representation would be a second thing to drift.

**The cost is real and is stated here**: `verify_script_lint.py` and `verify_script_structure.py`
both look for that artefact and therefore **SKIP** on this episode — and on every episode since EP62.
`check_script_craft.py`, which reads the file where it actually lives, ran and passed every
mechanical gate.

## 6. What the publish-day check must cover

1. **R-1 through R-6, re-run against the rendered file**, not the script.
2. **§3.1 re-verified live.** The settlement status is the one fact in this film that changes without
   anybody touching the film.
3. **§3.2 resolved** — the `LH-38` quote either upgraded to a read source or cut.
4. The title, the thumbnail text and the description **read cold, in isolation**, against ⛔-01,
   ⛔-03 and ⛔-04. `check_packaging_claims.py --package` run against the real
   `09_package/youtube_meta.v001.json`.
5. That the film still states its own absences out loud: **no finding says sounding the siren would
   have changed the outcome** (AB-01), no individual is named as having decided (AB-02), and the
   acreage and measured wind speed are not in the record read (AB-06).
6. §5, item by item.

---

## 7. Rows deliberately excluded, so their absence is not read as an oversight

| row | why it is not in the film |
|---|---|
| LH-06 | The July 2020 monthly test in which only 58 of the island's 70-plus sirens worked. **SECONDARY, and it would function as an implied cause** — a maintenance story the record does not connect to 8 August. ⛔-13 |
| LH-100 / early toll figures | The toll was revised repeatedly. The film uses the County's own "at least 102" with its date and no other figure. ⛔-10 |
| The water-rights and stream-diversion dispute | Real, documented, and **not sourced in this ledger** (AB-07). It cannot be narrated from these files, and as colour it would be an implied cause. ⛔-09 |
| Phase One's own closing paragraphs on climate change | The report says it; **the film does not**, because `forbidden_claims` bars collapsing causation into any single factor, and quoting the report's framing would do exactly that |
| The named EOC and dispatch personnel in Phase One | ⛔-17. Roles, not names |
| The ladder operator's destroyed home | §4. A real person's private loss, not needed by the argument |
