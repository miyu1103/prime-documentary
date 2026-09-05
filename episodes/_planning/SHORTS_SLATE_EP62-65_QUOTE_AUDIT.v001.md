# SHORTS_SLATE EP62–65 v001 — QUOTATION AUDIT v001

**Audited:** 2026-08-04 · **Target:** `episodes/_planning/SHORTS_SLATE_EP62-65.v001.md` (`short259`–`short270`)
**Method:** mechanical extraction + normalised word-boundary substring match against the primary-source
captures. Nothing hand-picked. **The slate was not edited.** Every fix below is a recommendation.

**Sources matched against**

| Shorts | Source file(s) |
|---|---|
| `short259` `short260` `short261` | `measurements/EP62_greene_RAW.md` (*Greene v. Lindsey*, 456 U.S. 444) |
| `short262` `short263` `short264` | `measurements/EP63_correa_RAW.md` (*Correa v. Hospital San Francisco*, 69 F.3d 1184) |
| `short265` `short266` `short267` | `measurements/EP64_memphis_RAW.md` (*Memphis Light v. Craft*, 436 U.S. 1) |
| `short268` `short269` `short270` | `measurements/EP65_marmet_RAW.md` + `measurements/EP65_brown_remand_RAW.md` |

---

## 1. Headline

**The slate is not clean. Five quotation defects, all in the last three episodes' worth of shorts.**

- **2 ALTERED** — a word of the writer's is sitting inside a sentence of the court's.
- **1 ALTERED (telop)** — a quoted cover headline whose words are not the quote's words.
- **2 NOT FOUND** — quoted cover headlines that are paraphrase presented as quotation.

Plus **3 material truncations** that pass the ELISION-ONLY rule and still change what the reader is told,
and **9 claim defects** that are not quotations at all (§5–§6).

**The worst one is `short267`, and it is the same shape as the long-form failures.**

> Slate: *"would retain the option to terminate service after affording **the notice and hearing required**."*
> Source: "…petitioners would retain the option to terminate service after affording **this opportunity and
> concluding that the amount billed was justly due**." (436 U.S. at 18–19, Part IV-B)

Nine words of the Court's sentence were replaced with six of the writer's. And this is the sentence the
short is *built on* — it is the "mandatory final content beat" of the whole piece, and it carries no
ledger ID (the correct row, **ML-76**, quotes it right).

**The EP62 Stevens/O'Connor error did NOT propagate.** No Justice is named anywhere in the slate —
`grep -iE "stevens|o.connor|brennan|powell|rehnquist|burger"` returns nothing across all 491 lines. The
dissent is carried only by the telop `DISSENT`. (Note the flip side: `short261` therefore never tells the
viewer *whose* dissent it is, and `short267`'s hook says "one of them" without a name.)

---

## 2. Extraction count and method output

Script: `shorts_quote_audit.py` (scratchpad). It reads the slate, walks it line by line inside each
`### short<NNN>` block, and pulls **every** span of four classes — no selection by judgement.

```
TOTAL FRAGMENTS EXTRACTED: 212
by class : {'A': 66, 'B': 25, 'C': 69, 'D': 52}
by kind  : {'quoted': 52, 'telop': 81, 'blockquote-container': 52,
            'narration': 25, 'italic-in-blockquote': 2}
verdicts : {'EXACT': 48, 'ELISION ONLY': 5, 'MISS': 13,
            'NARRATION': 25, 'TELOP-CLAIM': 69, 'CONTAINER': 52}
```

- **Class A — claimed quotations (66).** Every span in quotation marks, every italicised span inside a
  `>` blockquote, and every telop/cover string that carries quotation marks. These get the four-way verdict.
- **Class B — narration (25).** Hook / Open loop / Payoff / L5 lines. Not judged as quotations; instead
  every maximal run of **≥5 words that appears verbatim in the source** is reported (§7).
- **Class C — unquoted telops (69).** The writer's own captions. Checked for numbers and names (§6).
- **Class D — blockquote containers (52).** `> GL-41 — *"…"*` whole lines. Structurally cannot match
  (they carry the row ID and the writer's lead-in); judged through their inner Class-A spans instead.

**Normalisation applied identically to both sides:** NFKC; curly→straight quotes; em/en/figure dashes→space;
`…`→space; hyphenated line breaks joined (`col-\nlect` → `collect`, `ex-\ntensive` → `extensive`); page
markers stripped **including ones glued to a word** (`\*\s?\d+`, so `the full development of a *391record`
→ `…a record`); footnote markers `[7]` stripped; editorial brackets `[` `]` removed so `[T]he` matches
`The` and `[and]` matches `and`; `§` and `&amp;` handled; **bare page-number lines removed from the
`correa` capture** (that capture prints ` 12 ` on its own line mid-sentence — without this, AS-01 came back
falsely ABSENT, the same defect class as your `*391record` probe); Brown II OCR corruptions mapped
(`uneonscionability`→`unconscionability`, `Brown 7`/`Broitm I`→`Brown I`, `eases`→`cases`,
`Marehio`→`Marchio`, `Mar-met`→`Marmet`); lowercase; all remaining punctuation → space; whitespace collapsed.

**One method bug found and fixed mid-audit, and it is worth recording.** The first pass used plain
substring containment. `"…empowered to delay cutoff."` is a literal substring of
`"…empowered to delay cutoffs for three days"`, so **a truncated word passed as EXACT**. Switching to
word-boundary matching (`" "+frag+" " in " "+src+" "`) turned that fragment from EXACT into ALTERED and
took the miss count from 10 to 13. A substring-only checker would have reported this slate as one defect
lighter than it is.

**Every ledger row ID cited by the slate exists.** All 40 ID citations (`GL-`/`CR-`/`AS-`/`HA-`/`PR-`/`PF-`/
`DM-`/`ML-`/`MB-`) resolve to a real row in the matching `*_FACTS_LEDGER.v001.md`, and every quoted span
matches the text of the row it claims — with the one exception in §3.2 (`ML-97`), where the slate diverges
from the ledger row as well as from the opinion. Ledger row counts loaded: greene 107, correa 177,
memphis 144, marmet 71.

---

## 3. THE DEFECTS — exact source wording, ready to apply

### 3.1 `short267` L292 — **ALTERED** — the majority's surviving-power sentence

| | |
|---|---|
| **Slate** | Majority, on what survives: the utility *"would retain the option to terminate service after affording **the notice and hearing required**."* |
| **Source** | "And petitioners **would retain the option to terminate service after affording this opportunity and concluding that the amount billed was justly due.**" — 436 U.S. at 18–19 (Part IV-B) |
| **Ledger** | **ML-76** quotes it correctly. The slate cites no ID for this line. |

The phrase "the notice and hearing required" appears nowhere in that sentence. (`notice and hearing`
occurs once in the whole opinion, in majority n.15 — "an artificial barrier between the notice and
hearing components" — a different sentence about a different thing.)

**Fix:** replace with the ML-76 text, and cite ML-76:
> ML-76 — Majority, on what survives: *"And petitioners would retain the option to terminate service after affording this opportunity and concluding that the amount billed was justly due."*

The short's **claim** is nonetheless correct — see the `short267` row in §5.

---

### 3.2 `short267` L290 — **ALTERED** — singular for plural, and the three-day limit deleted

| | |
|---|---|
| **Slate** | answered by *"30 or 40 Division employees, all of whom are empowered to delay **cutoff**."* |
| **Source** | "Calls to the listed phone number are answered by 30 or 40 Division employees, all of whom are empowered to delay **cutoffs for three days based on representations made by customers over the phone**." — 436 U.S. at 23 (Stevens, J., dissenting) |
| **Ledger** | **ML-97** has it right, plural and complete. |

Two problems in one fragment: `cutoffs` → `cutoff`, and the truncation deletes the limit. "Empowered to
delay cutoff" reads as an unlimited power; the dissent's actual claim is a three-day stay. Since this short
exists to make the dissent's "the system worked" case, the deletion cuts against the short's own argument.

**Fix:**
> ML-97 — …answered by *"30 or 40 Division employees, all of whom are empowered to delay cutoffs for three days based on representations made by customers over the phone."*

---

### 3.3 `short266` Cover L277 — **NOT FOUND** — a quoted headline nobody wrote

| | |
|---|---|
| **Slate** | **Cover:** headline `"PAY OR\nWE CUT YOU OFF"` |
| **Source** | Nothing resembling it. The nearest are: the Court of Appeals' "the MLG&W notice only warn[ed] the customer **to pay or face termination**" (436 U.S. at 13), and ML-39: the final notice "simply stated that payment was overdue and that service would be discontinued if payment was not made by a certain date." |

The quotation marks put the utility's voice in a sentence the record does not contain. The short's own
telop `PAY OR\nWE STOP` is unquoted and therefore fine — the cover is the problem.

**Fix:** either drop the quotation marks (`PAY OR\nWE CUT YOU OFF` as the writer's caption), or quote what
exists: `"PAY OR FACE\nTERMINATION"`.

---

### 3.4 `short261` Cover L153 — **NOT FOUND** — the dissent's image, in the writer's words, in quotes

| | |
|---|---|
| **Slate** | **Cover:** headline `"MAILBOXES\nGET ROBBED"` |
| **Source** | "It is no secret, after all, that **unattended mailboxes are subject to plunder by thieves**." — 456 U.S. at 460 (O'Connor, J., dissenting) |

The short's own title line "The dissent's answer: mailboxes get robbed" is unquoted narration and is fine.
The cover promotes the same paraphrase into a quotation.

**Fix:** drop the quotation marks, or use the telop that is already correct: `"PLUNDER\nBY THIEVES"`
(verdict EXACT, row 15 of the table).

---

### 3.5 `short263` Cover L206 — **ALTERED** — three words changed inside the quote

| | |
|---|---|
| **Slate** | **Cover:** headline `"A WONDERFUL\nWEASEL WORD"` |
| **Source** | "'Appropriate' is **one of the most wonderful weasel words in the dictionary**…" — 69 F.3d at 1192, quoting *Cleland v. Bronson Health Care Group*, 917 F.2d 266, 271 (6th Cir. 1990) |

`a` for `one of the most`, and `word` for `words`. The short's telop `A WEASEL WORD` is unquoted and fine.

**Fix:** `"MOST WONDERFUL\nWEASEL WORDS"`, or drop the quotation marks.

---

## 4. Material truncations — pass the rule, still mislead (3)

These are ELISION ONLY by the channel's rule (nothing added, nothing swapped) and I am **not** counting
them as defects. Each one nonetheless changes what a viewer is told, and each is fixable by restoring a
clause or adding `…`.

**4.1 `short261` GL-75 — the "11 States" count.**
Slate: *"at least 11 States authorizing notice in summary eviction proceedings solely by posting."*
Source continues: **"…or by leaving the notice at the tenant's residence."**
The dissent's 11 States allowed posting *or* leave-with-a-resident. The truncation makes them 11 States
that allowed posting alone — and `short261`'s payoff then says "eleven States allowed **exactly this
practice**", which the full sentence does not support. Ledger **GL-75** carries the full clause.

**4.2 `short260` GL-58.**
Slate ends: *"…has abandoned his interest in the apartment."*
Source continues: **"…such that mere pro forma notice might be held constitutionally adequate."**
The dropped clause is the whole legal point of the sentence.

**4.3 `short263` AS-04 — the screening test.**
Slate: *"reasonably calculated to identify critical medical conditions that may be afflicting symptomatic patients."*
Source continues: **"…and provides that level of screening uniformly to all those who present substantially
similar complaints."** The uniformity half is the half `short263`'s payoff is actually about. Restoring it
(or ending with `…`) costs four seconds and makes the short's own argument for it.

---

## 5. Claim locks — each verified against the source

| Short | The claim the short locks | Verdict |
|---|---|---|
| `short261` | "the vote count is **not in the document**" | **TRUE.** No vote tally anywhere in `EP62_greene_RAW.md`; grep for `5-4`/`6-3`/"joined the opinion" returns only statute citations. Matches **GL-65** and **Q-13**. |
| `short267` | the utility "retained the power to cut service after a hearing" | **TRUE.** 436 U.S. at 18–19 / **ML-76**. The *claim* is right; only the *quotation* of it is wrong (§3.1). |
| `short269` | "The Supreme Court never said the clause was valid" | **TRUE.** *Marmet* vacated and remanded (MB-50); Part II sends unconscionability back for Brown and Taylor (MB-49) and notes the state court never reached any non-public-policy ground for Marchio (MB-46). **MB-53** is the row for this proposition — the slate cites MB-34, which supports only "vacated". Minor mis-citation; recommend citing **MB-53** alongside. |
| `short269` | "two cases reversed and remanded, the third a certified question answered" | **TRUE.** Brown II disposition: "Case No. 35494, Reversed and remanded. Case No. 35546, Reversed and remanded. Case No. 35636, Certified question answered." |
| `short270` | "`PER CURIAM` is a mandatory telop… no named author and no recorded vote" | **TRUE.** MB-01 / ⛔-10. |
| `short259` | "never say the writs *were* torn off in these three cases" | **TRUE** and correctly observed — the record has servers describing Village West, not these tenants. |
| `short262` | "no line may say or imply that the wait caused her death" | **TRUE** and correctly stated (Q-03). No line in `short262` breaches it. |
| `short265` | "do not say the utility double-billed them, and do not say the Crafts hired a bad contractor" | **TRUE** (ML-117). But see §6.4 — the short breaches its own episode header on a different number. |

---

## 6. Claim defects that are not quotations (9)

**6.1 `short261` final telop `5–4? NOT IN THE OPINION` — contradicts its own lock, and the number is impossible.**
The lock two lines below reads: *"Never write '5–4' or '6–3'."* The telop writes `5–4` on screen in
40-point type. Worse, the dissent byline is O'Connor + the Chief Justice + Rehnquist — **three** dissenters
— so with a full bench 5–4 is arithmetically excluded by the document itself. A viewer who reads the telop
for half a second takes away "5–4". **Fix:** `THE VOTE IS NOT\nIN THE OPINION`, or `THREE JUSTICES\nDISSENTED` (GL-65).

**6.2 `short261` payoff: "the Court struck it down."**
EP62 ledger **Q-15** forbids exactly this: "Kentucky's law was struck down." The Court held posting under
§ 454.030, *as applied to these public-housing tenants*, constitutionally inadequate (GL-48/GL-63/GL-66);
it did not facially void the statute. **Fix:** "and the Court held it was not enough."

**6.3 `short261` payoff: "eleven States allowed exactly this practice at the time."** See §4.1 — the
dissent's 11 States allowed posting **or** leaving the notice with a resident.

**6.4 `short265` payoff + telop: "The power went off five times" / `NOBODY EVER DECIDED`.**
Two separate problems.
(a) The slate's own EP64 section header (L236) says the opinion contradicts itself on "how many
terminations there were (majority: five; dissent: 'several') — **the script may not pick a side**", and
then `short265` picks five. Ledger **ML-118** actually permits five *attributed to the Court*; the header
is what is wrong. **Fix the header**, not the short — or say "five times, the Court said."
(b) "to this day no court has ever decided whether they owed the money" and `NOBODY EVER DECIDED` assert
knowledge of post-1978 proceedings. The opinion left damages "for initial determination by the courts
below" (ML-86); ledger **○-01** is open and **⛔-05** forbids any ending for the family. **Fix:**
"and the Supreme Court never decided whether they owed the money."

**6.5 `short264` title, hook and cover badge: "not for the death".**
Title *"The money was not for her death. It was for the wait."*; hook *"Almost none of it was about how
she died"*; badge `NOT FOR THE DEATH`. True of the **$200,000** (PR-10 / DM-15, her suffering while
waiting) — but the **$500,000**, five sevenths of the award, was "for the pain, suffering, and mental
anguish experienced by the **survivors**" (PR-11), i.e. the family's grief at her death. The slate's own
EP63 lock (L163) states this correctly: "the damages affirmed were for her suffering while waiting **and
the family's grief**." The short's framing contradicts its own section lock. **Fix:** "$200,000 was for
the wait. $500,000 was for the seven people she left."

**6.6 `short270` telop `REVERSED` vs `short269` telop `VACATED`.**
*Marmet*'s disposition is **vacated** and remanded (MB-50); `short269` has it right. `short270` says
`REVERSED` and its payoff says "it got reversed for it". Defensible only by borrowing Brown II's own loose
wording ("reversed our opinion"), which is a state court describing what happened to it — not the U.S.
Reports disposition. Two shorts in the same episode giving the viewer two different dispositions is a
retention defect as well as a precision defect. **Fix:** `VACATED` in both, or `REVERSED` labelled as the
West Virginia court's own word.

**6.7 `short269` payoff: "four months later the state court gave up exactly one paragraph."**
Marmet 21 Feb 2012 → Brown II 13 June 2012 = **3 months 23 days**. And Brown II overruled *Syllabus Point
21 and its accompanying text*, not "a paragraph" — the short's own telop `ONE POINT\nOVERRULED` is the
right description. **Fix:** "less than four months later the state court gave up exactly one syllabus
point."

**6.8 `short262` cover `THEY NEVER CALLED HER` / title "It just never called her number".**
The opinion never says number 47 was not called. It says number 24 was being called at ~2:15 p.m. and that
she waited another 45–75 minutes and then left. Ledger **RQ-10** is explicit: "the gap between them is not
stated to be a queue position." This is an inference, and a fair one, but it is stated as fact on a cover
card. **Fix:** `HER NUMBER\nNEVER CAME` reads the same and is what the record supports.

**6.9 `short267` telop string is written three different ways.**
`THEN THEY CAN\nSTILL CUT IT` (Telops, L294) · `THEY CAN STILL CUT IT` (Lock, L299) · `THEY CAN STILL CUT
IT` (§6.5 second-watch, L450). Telop strings are the build contract for `short<NNN>.ts`; pick one.

**Also noted, outside the audit's remit:** the header (L6) says "Numbers up to `short181` are taken; this
slate reserves **182–193**", while the slate is `short259`–`short270` throughout.

---

## 7. Narration lines carrying verbatim source runs (Class B)

25 narration lines checked; **9** contain a run of ≥5 words that is verbatim in the source. All 9 are
either inside quotation marks or explicitly attributed ("the court's own phrase", "the court called that",
"one Justice wrote back"). **No unattributed lift.**

| Short | Verbatim run found in the source |
|---|---|
| 259 hook | `we had plenty of trouble` |
| 261 hook | `that unattended mailboxes are subject to plunder by thieves` |
| 261 payoff | `testimony of a handful of process servers` |
| 262 hook | `a sixty-five-year-old` |
| 262 payoff | `a high number and a cold shoulder` |
| 263 hook | `one of the most wonderful weasel words in the dictionary` |
| 264 payoff | `locking the barn door long after the horse` |
| 268 hook | `claims to collect late payments owed by the patient` |
| 270 hook | `and created from whole cloth` |

One advisory: `short261`'s hook renders the dissent as "it is no secret that unattended mailboxes are
subject to plunder by thieves", silently dropping **"after all"**. As written text this is narration; as
recorded VO it will be *heard* as a quotation. Either restore "after all" or don't lead with "one Justice
wrote back:".

---

## 8. Unquoted telops carrying a number or a name (Class C)

| Telop | Verdict |
|---|---|
| `1982` (short260) | ✓ decided 17 May 1982 |
| `1991` (short262) | ✓ the events; note the case is a 1995 decision, and `short260` uses the *decision* year while `short262` uses the *events* year — inconsistent convention across the slate |
| `11 STATES` (short261) | ✓ but the dissent says "**at least** 11 States" |
| `5–4? NOT IN THE OPINION` (short261) | ✗ §6.1 |
| `$200,000` `$500,000` `$700,000` `3 CHILDREN 4 GRANDCHILDREN` (short264) | ✓ all four in PR-10/PR-11/¶1 |
| `WILLIE C.` `WILLIE S.` (short265) | ✓ ML-19/ML-16 — **but** EP64 ledger **⛔-08** marks putting the Crafts' real names on screen an **OWNER CALL**, and the slate makes it without recording one. The hook also speaks the address-adjacent names. Raise it before build. |
| `2,000 A MONTH` (short267) | ✓ but the dissent says "**about** 2,000 customers" |
| `NOBODY EVER DECIDED` (short265) | ✗ §6.4(b) |
| `THEY NEVER CALLED HER` (short262 cover) | ✗ §6.8 |
| `NOT FOR THE DEATH` (short264 cover) | ✗ §6.5 |
| `REVERSED` (short270) | ✗ §6.6 |
| `DISSENT` ×2, `PER CURIAM` | ✓ |

---

## 9. Final tally

| Class | Count |
|---|---|
| Fragments extracted (mechanical, no hand-picking) | **212** |
| — Class A, claimed quotations judged | **66** |
| — Class B, narration lines scanned for ≥5-word verbatim runs | 25 |
| — Class C, unquoted telops checked for numbers/names | 69 |
| — Class D, blockquote containers (judged via inner spans) | 52 |
| **EXACT** | **48** |
| **ELISION ONLY** | **5** |
| **ALTERED** | **3** (§3.1, §3.2, §3.5) |
| **NOT FOUND** | **2** (§3.3, §3.4) |
| n/a — writer's own words in scare quotes, never attributed to a court | 8 |
| Material truncations (pass, still misleading) | 3 (§4) |
| Non-quotation claim defects | 9 (§6) |
| Ledger row IDs cited | 40 — **all exist, all say what the slate says**, except ML-97 (§3.2) |

**Defect density: 5 defects in 66 judged quotations = 7.6%.** For comparison, the long-form audit found 21
in a comparable body. The shorts slate is cleaner than the long-forms were — but it is not clean, and its
two worst fragments are on covers and on the one sentence `short267` was built to deliver.

---

## 10. Recommended order of application

1. **§3.1** `short267` ML-76 quote — this is the one that would have shipped a rewritten sentence of the
   Supreme Court on the payoff beat.
2. **§3.2** `short267` ML-97 — restore `cutoffs for three days`.
3. **§3.3 / §3.4 / §3.5** — three cover headlines: drop the quotation marks or use the real words.
4. **§6.1** `short261` — get `5–4` off the screen; it contradicts the short's own lock and the byline.
5. **§6.2, §6.4, §6.5, §6.6, §6.7, §6.8** — six claim corrections, all one-line rewrites.
6. **§4** — restore three truncated clauses (or mark them `…`).
7. **§6.9** and the §0.6 numbering line — build-contract hygiene before `short<NNN>.ts` is written.

---

## APPENDIX A — every Class-A fragment, with its verdict

Machine output, in slate order. `quoted` = span in quotation marks · `telop` = telop/cover string carrying
quotation marks · `italic-in-blockquote` = italicised span inside a `>` line. `L` = line number in
`SHORTS_SLATE_EP62-65.v001.md`.

| # | Short | Where | Fragment as the slate has it | Verdict |
|---|---|---|---|---|
| 1 | short259 | quoted L103 | Q. Were you aware of there being any problem with children ripping the Writs off? A. Oh, we had plenty of trouble. | EXACT |
| 2 | short259 | quoted L104 | Q. Did you ever see kids pulling them off? A. Yes. … Q. Where was that? A. Village West. | ELISION ONLY |
| 3 | short259 | quoted L105 | not infrequently | EXACT |
| 4 | short259 | quoted L105 | before they could have their intended effect. | EXACT |
| 5 | short259 | quoted L106 | merely posting notice on an apartment door does not satisfy minimum standards of due process. | EXACT |
| 6 | short259 | telop L112 | "PLENTY OF TROUBLE" | EXACT |
| 7 | short260 | quoted L128 | But if no one is at home at the time of that visit, as is apparently true in a 'good percentage' of cases, posting … | EXACT |
| 8 | short260 | quoted L129 | Neither the statute, nor the practice of the process servers, makes provision for even a second attempt at personal… | EXACT |
| 9 | short260 | quoted L130 | The failure to effect personal service on the first visit hardly suggests that the tenant has abandoned his interes… | EXACT *(material truncation — see §4)* |
| 10 | short260 | telop L132 | "A GOOD PERCENTAGE" | EXACT |
| 11 | short261 | quoted L146 | Today, the Court holds that the Constitution prefers the use of the Postal Service to posted notice. | EXACT |
| 12 | short261 | quoted L147 | It is no secret, after all, that unattended mailboxes are subject to plunder by thieves. | EXACT |
| 13 | short261 | quoted L148 | The sole ground for the Court's result is the scant and conflicting testimony of a handful of process servers in Ke… | EXACT |
| 14 | short261 | quoted L149 | at least 11 States authorizing notice in summary eviction proceedings solely by posting. | EXACT *(material truncation — see §4)* |
| 15 | short261 | telop L151 | "PLUNDER BY THIEVES" | EXACT |
| 16 | short261 | telop L153 | "MAILBOXES GET ROBBED" | **NOT FOUND** |
| 17 | short261 | quoted L156 | 5–4 | n/a — writer's own words in scare quotes, not attributed to the court |
| 18 | short261 | quoted L156 | 6–3 | n/a — writer's own words in scare quotes, not attributed to the court |
| 19 | short262 | quoted L178 | Ms. Gonzalez, a sixty-five-year-old widow, awoke … 'feeling real bad,' and experiencing 'chills, cold sweat, dizzin… | ELISION ONLY |
| 20 | short262 | quoted L179 | the jury heard testimony from which it could have concluded that Ms. Gonzalez went to the Hospital in critical cond… | EXACT |
| 21 | short262 | quoted L180 | would have ministered to her had she waited. | EXACT |
| 22 | short262 | telop L182 | "A HIGH NUMBER AND A COLD SHOULDER" | EXACT |
| 23 | short263 | quoted L199 | EMTALA requires an appropriate medical screening, but does not explain what constitutes one. The adjectival phrase … | EXACT |
| 24 | short263 | quoted L200 | 'Appropriate' is one of the most wonderful weasel words in the dictionary, and a great aid to the resolution of dis… | EXACT |
| 25 | short263 | quoted L201 | reasonably calculated to identify critical medical conditions that may be afflicting symptomatic patients. | EXACT *(material truncation — see §4)* |
| 26 | short263 | quoted L202 | The essence of this requirement is that there be some screening procedure, and that it be administered even-handedly. | EXACT |
| 27 | short263 | telop L204 | "APPROPRIATE" | EXACT |
| 28 | short263 | telop L206 | "A WONDERFUL WEASEL WORD" | **ALTERED** |
| 29 | short263 | quoted L207 | treat everyone the same | n/a — writer's own words in scare quotes, not attributed to the court |
| 30 | short264 | quoted L218 | assessed $200,000 in damages on the decedent's account (payable to the heirs). | EXACT |
| 31 | short264 | quoted L219 | $500,000 … for the pain, suffering, and mental anguish experienced by the survivors — $100,000 apiece for the three… | ELISION ONLY |
| 32 | short264 | quoted L220 | the woman described by one witness as the trunk of the family tree was cut down. | EXACT |
| 33 | short264 | quoted L221 | this motion is a classic example of a litigant locking the barn door long after the horse has bolted. | EXACT |
| 34 | short264 | quoted L222 | This was a waiver, pure and simple. | EXACT |
| 35 | short264 | telop L224 | "THE TRUNK OF THE FAMILY TREE" | EXACT |
| 36 | short264 | italic-in-blockquote L229 | on the decedent's account | EXACT |
| 37 | short265 | quoted L250 | they noticed that there were two separate gas and electric meters and only one water meter serving the premises. Th… | EXACT |
| 38 | short265 | quoted L251 | In 1973, the Crafts began receiving two bills: their regular bill, and a second bill with an account number in the … | EXACT |
| 39 | short265 | quoted L252 | Willie S. and Mary Craft, respondents here, reside at 1019 Alaska Street in Memphis. | EXACT |
| 40 | short265 | italic-in-blockquote L260 | the record does not agree with itself | n/a — writer's own words in scare quotes, not attributed to the court |
| 41 | short266 | quoted L271 | The 'final notice' contained in MLG&W's bills simply stated that payment was overdue and that service would be disc… | EXACT |
| 42 | short266 | quoted L272 | [T]he MLG&W notice fails to mention 'that a dispute concerning the amount due might be resolved through discussion … | EXACT |
| 43 | short266 | quoted L273 | recipients of a cutoff notice should be told where, during which hours of the day, and before whom disputed bills a… | EXACT |
| 44 | short266 | telop L277 | "PAY OR WE CUT YOU OFF" | **NOT FOUND** |
| 45 | short267 | quoted L289 | Each month the Division terminates the service of about 2,000 customers. | EXACT |
| 46 | short267 | quoted L290 | PHONE 523-0711 INFORMATION CENTER | EXACT |
| 47 | short267 | quoted L290 | 30 or 40 Division employees, all of whom are empowered to delay cutoff. | **ALTERED** |
| 48 | short267 | quoted L291 | In my judgment, the Court's holding confuses and trivializes the principle that the State may not deprive any perso… | EXACT |
| 49 | short267 | quoted L292 | would retain the option to terminate service after affording the notice and hearing required. | **ALTERED** |
| 50 | short267 | telop L294 | "CONFUSES AND TRIVIALIZES" | EXACT |
| 51 | short267 | quoted L299 | a hearing before shutoff means no shutoff | n/a — writer's own words in scare quotes, not attributed to the court |
| 52 | short268 | quoted L321 | The contracts included a clause requiring the parties to arbitrate all disputes, other than claims to collect late … | EXACT |
| 53 | short268 | quoted L322 | In each case, a family member of a patient requiring extensive nursing care had signed an agreement with a nursing … | EXACT |
| 54 | short268 | quoted L323 | the party filing the arbitration. | EXACT |
| 55 | short268 | quoted L331 | cynical | n/a — writer's own words in scare quotes, not attributed to the court |
| 56 | short268 | quoted L331 | cruel | n/a — writer's own words in scare quotes, not attributed to the court |
| 57 | short269 | quoted L342 | The decision of the State Supreme Court of Appeals must be vacated. | EXACT |
| 58 | short269 | quoted L343 | must consider whether, absent that general public policy, the arbitration clauses … are unenforceable under state c… | ELISION ONLY |
| 59 | short269 | quoted L344 | In accordance with the Supreme Court's mandate, we overrule Syllabus Point 21 of Brown I. We otherwise find that th… | EXACT |
| 60 | short269 | quoted L351 | vacate | n/a — writer's own words in scare quotes, not attributed to the court |
| 61 | short270 | quoted L362 | found unpersuasive this Court's interpretation of the FAA, calling it 'tendentious' … and 'created from whole cloth'. | ELISION ONLY |
| 62 | short270 | quoted L363 | The West Virginia court's interpretation of the FAA was both incorrect and inconsistent with clear instruction in t… | EXACT |
| 63 | short270 | quoted L364 | When this Court has fulfilled its duty to interpret federal law, a state court may not contradict or fail to implem… | EXACT |
| 64 | short270 | quoted L365 | a general, state, common-law, contract-law principle that is not specific to arbitration. | EXACT |
| 65 | short270 | telop L367 | "TENDENTIOUS" | EXACT |
| 66 | short270 | telop L367 | "CREATED FROM WHOLE CLOTH" | EXACT |

*Class D (52 blockquote containers) are the `> GL-41 — *"…"*` lines themselves: they carry a row ID and the
writer's lead-in as well as the quote, so the whole line can never match. Their inner quoted/italic spans
are rows 1–66 above. Class B (25) is §7. Class C (69) is §8.*

---

*Built 2026-08-04 by mechanical extraction and word-boundary matching over four primary-source captures and
four facts ledgers. The slate itself was not modified. Audit script: `shorts_quote_audit.py`; raw verdicts:
`shorts_quote_audit.json`.*
