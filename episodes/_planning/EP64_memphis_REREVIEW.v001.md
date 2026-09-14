# EP64 · MEMPHIS LIGHT, GAS & WATER DIVISION v. CRAFT — ADVERSARIAL RE-REVIEW v001

**Target:** `episodes/_planning/EP64_memphis_script.en.v002.md` (429 lines, 5,364 spoken words, 30:28 at 176 w/finished-min)
**Standard:** `docs/PD_SCREENPLAY_STANDARD.v001.md` §16 (R1–R15) · **Prior grade:** `EP64_memphis_FILM_BIBLE.v001.md` §19 = 4 PASS / 11 FAIL on v001
**Also weighed:** `EP64_memphis_FACTS_LEDGER.v001.md` · `episodes/PD-2026-064-memphis/01_research/fact_recheck.v001.md` · `episodes/_planning/measurements/EP64_memphis_RAW.md` · `episodes/PD-2026-064-memphis/episode_spec.v001.json` (notes read in full) · `episodes/_planning/DEEP_RESEARCH_FINDINGS.v001.md`
**Brief:** *try to refute the claim that v002 meets the screenplay standard.* This document is written against the script, not for it.

> **判定（日本語・一段落）**
> v002 は v001 から確実に良くなった（15項目中 **9 PASS / 6 FAIL**、v001 は 4/11）。機械ゲートも全緑である（`check_script_craft` PASS・`check_script_length` PASS）。**それでも水準には届いていない。**理由は三つ。(1) §19 が名指しした8つの断定文だけが消され、**同じ種類の断定が16箇所以上そのまま残っている**（R3）。(2) §19 R10 の修正（多数意見の反論2つを92%より前へ移す）が、**その後ろにあった Stevens の締め2段落を92%線の外へ押し出した**——修正が新しい違反を作った（R10 = 規格 §12 の [MUST]）。(3) 反対意見の数字を28%へ前倒しした R5 の移設は、**位置は直ったが機能は直っていない**——最強の反論が提示された直後（次の一文）に潰されるため、判決前に観客が電力会社側を保持している時間がゼロである。加えて、**ENDING の最後の二つの断定（L413・L421）が、帰属なしで多数意見の枠を採っている**。事実の誤りは3件（うち1件は HOOK の第一文）。すべて小さく、局所的で、再取材は不要である。

---

## 0. What this review is not re-litigating

`fact_recheck.v001.md` did a mechanical verbatim sweep of 98 quotation-bearing lines against the RAW opinion and I did not repeat it. Two things about that file matter here, though:

1. **It is one edit stale.** `fact_recheck.v001.md` is timestamped 12:53; `script.en.v002.md` is 12:55. Its one blocking item (§4.1, L171 — the stray `,.` and the truncated extended-payment plan) **has since been fixed in the file** (§1.12 below). Nothing else it quotes has drifted.
2. **It verified quotations, not narration.** Every defect in §1.9, §1.10, §2 and §4 of this document lives in sentences the script wrote itself. A verbatim matcher cannot see them by construction. That is the gap this review occupies — and it is where the three factual errors are.

---

# 1. Did the repairs land? — verified against the current text, line by line

Method: `grep` against the file for every retired string; the current wording quoted from the file, not from a changelog.

## 1.1 The three record-fills — CONFIRMED ABSENT BY SEARCH

| String | Hits in v002 | Status |
|---|---:|---|
| `The judge was uncomfortable` | **0** | **RESOLVED** |
| `that detail survived for a reason` | **0** | **RESOLVED** |
| `The seller had told them` / `It was running` (HOOK meter dating) | **0 / 0** | **RESOLVED** — see 1.1c |

**(a) RF-1 · the §15 disqualifier.** v002 L199–L201: *"The judge then expressed a hope. His word, in quotation marks, in the opinion. He hoped that credit in the amount of thirty-five dollars be issued to reimburse the Crafts…"* / *"Terminations which should have been unnecessary. That is the trial judge, ruling for the utility."* Conduct only, no interior. **RESOLVED.** §19 was right that the replacement is stronger than what it replaced.

**(b) RF-2.** v002 L81 is now the two words *"Missed work."* and nothing else. **RESOLVED.**

**(c) RF-3 · the HOOK's meter dating.** The retired sentences are gone, but the repair **replaced them with a different, and worse, first line.** v002 L19: *"Two meters on one wall."* The record (`RAW` line 33, ML-17) is *"two separate gas and electric meters and only one water meter serving the premises"* — i.e. **two gas meters and two electric meters**, which ML-21 confirms by having the Crafts hire a contractor *"to combine the meters into one gas and one electric meter."* There were four gas/electric meters plus one water meter. **The film's first spoken sentence understates the count by half**, and the film contradicts itself 47 seconds later at L43 (*"two separate gas and electric meters and only one water meter"*). The direction 【M001 two meters bolted side by side】 commissions the same error as a plate, and it has already propagated: `EP64_memphis_beats.v001.json` HOOK beat 2 is a kinetic card reading **`TWO METERS. / ONE WALL.`** — i.e. the error is scheduled to be burned into on-screen type. Nothing in the record says anything about a wall.
**Verdict: NOT RESOLVED — the dating error was replaced by a counting error, in the highest-exposure eight seconds of the film.**

## 1.2 The other two record-fills (RF-4, RF-5)

| String | Hits | Status |
|---|---:|---|
| `Neither will this film` | 0 | **RESOLVED** — v002 L71 stops at *"The Court never resolves it."* |
| `The meters were fixed` / `The two bills were one bill` | 0 / 0 | **RESOLVED** at L239, which now runs ML-91 verbatim (*"…as the double-meter problem has been clarified during this litigation. Nor do respondents aver that there is a present threat of termination of service."*) |

**But RF-5's frame came back at the last sentence of the film.** L421: *"Three courts, four years, **two irreconcilable accounts of one set of meters** — all out of what happened at the other end of that line."* RF-5 was removed because saying the *meters* were the thing put right silently adopts the majority over footnote 7, whose subject is **accounts**, not hardware (FILM_BIBLE §3.1, ML-117). L421 does the same thing in the film's final summarising sentence, at 99.4%, in the narrator's voice, and it does it with the word *accounts* used in its other sense in the same breath. **REGRESSED (different sentence, same defect).**

## 1.3 The eight tone/villain strings (§19 R8, fact_recheck §2.3)

`The courts are open` · `Sue us` · `who might listen` · `as a rumour` · `costs more than the wrong` · `vagueness is deliberate` · `hinge of the whole case` · `A hearing before a shutoff` → **all 8 return 0 hits. RESOLVED.** L133 now carries the ML-33 instruction verbatim in narration, which is the right fix and removes the discretion reading of the meter reader.

## 1.4 §19 R2 — the controlling idea spoken aloud

Both flagged passages are gone. OP L29 is now *"The Supreme Court affirmed the judgment below. Three Justices dissented, and their account of the same record is printed in the same volume."* ENDING L413 is now *"What the case settled fits on the page the utility was already mailing. Where. During which hours of the day. And before whom…"* **RESOLVED as to R2** — but L413 introduced a new problem of a different class (§4a.4 below), and the OP replacement introduced a retention problem (§2.3).

## 1.5 §19 R4 — one recognition

Three of the four `⟨HELD⟩`-plus-assertion clusters are gone. **RESOLVED**, with an erosion noted at §3-R4.

## 1.6 §19 R5 — the dissent's operating material moved forward

Moved. L135–L143 now sit at **23.2%–25.5% (7:04–7:56)**, ahead of the judgment at 70.9%. **RESOLVED as to position. NOT RESOLVED as to function** — this is §2.1, the largest finding in this document.

## 1.7 §19 R6 — the motif installed as directions

Eight directions exist. **PARTIALLY RESOLVED** — they are present but not in order, one state is used twice, one act has none, and the final state's content is undefined. §2.2.

## 1.8 §19 R9 — the vertical ladder

Rungs 1–4 are at 3.8% / 23.5% / 33.2% / 34.7%, matching FILM_BIBLE §4.1. Rung 5 (ML-104, the assumption itself) is at 84.9%. **PARTIALLY RESOLVED** — see §3-R9: the bottom rung is rebutted 1.6 percentage points after it lands, so it never stands.

## 1.9 §19 R10 — nothing new after 92%

ML-116 moved 95.02% → **83.54%**; ML-115 moved 93.32% → **86.50%**. Both fixed. **And the fix pushed three previously-compliant beats out past the line.** Measured, both revisions:

| Beat | v001 | v002 | |
|---|---:|---:|---|
| ML-122 (*"they did obtain counsel and thereafter they encountered no billing problems"*) | 89.52% | **91.98%** | sentence now straddles the line |
| ML-110 (75-word dissent quotation) | 90.20% | **92.65%** | **now outside** |
| ML-111 (62-word dissent closing) | 91.56% | **94.24%** | **now outside** |
| ML-115 | 93.32% | 86.50% | fixed |
| ML-116 | 95.02% | 83.54% | fixed |

**394 words (2:14) of the film sit after the 92% line. 190 of them — everything from L397 — are ACT_5 material appearing for the first time.** The ENDING itself (204 words) is clean; every fact in it is recycled. **NOT RESOLVED. This is §12 [MUST] and DEEP_RESEARCH R-14 [MUST], and it is a defect the repair created.** §2.4.

## 1.10 §19 R14 — the record's silence

The two flagged fills are gone. Two others were not looked for and are still there, and one is a factual error:

- **L197** — *"Nobody was substantially deprived — except, possibly, **the only two people still in the case**."* The sentence it is glossing (ML-48, RAW line 43) reads *"[n]one of the **individual plaintiffs** [was] deprived…"* — plural. ML-29 says the action was filed by *"the Crafts and other MLG&W customers."* At the District Court judgment the Crafts were **not** the only two people in the case; the film's own source sentence proves it. **NOT RESOLVED — a new unsupported claim, delivered as the act's punchline.**
- **L321** — *"And then, inside the reasoning that got there, one more sentence. **It is the one that almost never gets quoted.**"* A claim about how this case is discussed elsewhere. Nothing in the record, the ledger or the contract supports it. This is the **same species** as the deleted *"This is the most common way the case gets told wrong"* (§19 R3-8, confirmed absent). The pass deleted the string and kept the move. **REGRESSED.**
- **L207** — *"…the notice had been rewritten and the thirty-five dollars had been paid."* ML-51 (December 1974) says only *"instituted some new procedures which will give more definitive and adequate notice."* "Rewritten" is the film's word; the rewritten notice is ML-46, a fact of 1978, not of 1974. **PARTIALLY RESOLVED — mild overstatement, and it pre-empts the ACT_5 state-7 beat.**

## 1.11 §19 S2 — the impossible timecodes

**RESOLVED, and well.** Every declared window now matches its own word count at 176 w/min to within ±2.6 seconds:

| | HOOK | OP | ACT_1 | ACT_2 | ACT_3 | ACT_4 | ACT_5 | ENDING |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| words | 22 | 51 | 716 | 1,181 | 755 | 1,108 | 1,327 | 204 |
| declared | 8s | 17s | 246s | 400s | 258s | 379s | 453s | 69s |
| need @176 | 7.5 | 17.4 | 244.1 | 402.6 | 257.4 | 377.7 | 452.4 | 69.5 |

One inconsistency survives: **the header (L11) says the measured runtime is 30:23; the section table's own last boundary is 30:30 and the word count gives 30:28.** A 7-second disagreement between a file and itself, in the one number the assembly thread will read. Fix the header.

## 1.12 fact_recheck §4.1 — the NEEDS SOURCE item

**RESOLVED in the file, after the recheck was written.** L171 now reads: *"In March 1973 the utility began an extended payment plan, which the trial judge called a generous program. Customers able to demonstrate financial hardship could pay one-half of a past due bill, with the balance in equal installments over the next three bills. The plaintiffs in this action were participants in the plan."* The stray `,.` is gone (0 hits) and the balance clause is restored. One word short of the ledger: the opinion's *"to pay **only** one-half"* — *only* is the word that stops a listener hearing the plan as forgiveness. Cheap to restore.

## 1.13 One deletion nobody recorded

v001 carried ML-60: *"And it refused to let a utility's own rulebook override the exception. A public utility should not be able to coerce a customer to pay a disputed claim."* It is **gone from v002**, and it appears in no changelog: not in §19's delete list, not in `fact_recheck` §2.1–§2.3, not in the §2.2 restoration table. A ✓ VERBATIM ledger row was dropped silently. It is the one Tennessee-law line that says a utility may not use the cutoff as leverage, and it is the natural companion to ML-59, which the script does keep at L255. **Either restore it or record the decision.** More important than the line itself: **the change inventory in `fact_recheck` §2 is not complete**, so "resolved 8, restored 5, removed 8" cannot be treated as the full diff.

---

# 2. Defects the repairs introduced

## 2.1 R5 — the relocation fixed the position and destroyed the function

The brief asks whether the film now spends *so long* on the utility's case that the turn feels unearned. **Measured: the opposite is true, and it is worse.**

| Block | Content | Clock | Length |
|---|---|---|---|
| pro-utility | L129–L143: the doorstep exception · the 30-day clock · 2,000 cutoffs a month · 11,216 in six months · PHONE 523-0711 printed on the notice · 30–40 people who can each stop the meter reader | 6:30–7:56 | **86s** |
| demolition | L145–L165: what the notice actually said · *pay or face termination* · the two flyers · no assurance the Crafts got the one that mentions disputes | 7:56–9:18 | 82s |
| pro-utility | L167–L173: the four-rung ladder · the right to bring a representative · the generous programme · *"not a case about a utility that offered nothing"* | 9:18–10:07 | 49s |
| demolition | L175–L185: 33,000 complaints · never written down · *word of mouth referral* · the statute that exempted this utility | 10:07–11:11 | 64s |

The strongest fact the utility has — **the phone number was printed on the notice and forty people could each stop the cutoff** (L143) — is answered by the **very next spoken line**: L145 *"And this is what the notice itself said."* Zero separation. §19's own diagnosis of v001 was *"ACT_2 は…同じ幕の中で即座に崩している ため、助走として機能していない"* — **that diagnosis is still true of v002.** The material moved 54 percentage points earlier and kept the identical knock-down rhythm. Worse, the new placement uses the dissent's best fact as the **set-up line for the majority's punchline**, which is an adoption of the majority by structure (see §4a.3).

Consequences that follow:

- **The audience holds the utility's case for 86 seconds, ending at 7:56. The judgment arrives at 21:44.** For thirteen minutes and forty-eight seconds before the verdict, nothing is standing on the utility's side. §4.1 of the standard — *"反論を最強の形で述べてから倒す"* — requires the audience to still believe it when the turn comes.
- **ACT_5's staging now contradicts the film.** L355 (76.6%, 23:20): *"Now the dissent, and it is not a footnote."* The dissent has by then already spoken twice at length — at 23.2%–25.5% (7:04–7:56) and at 43.6% (13:17, L215). The line announces an arrival that happened sixteen minutes earlier.
- The single-line reminder §19 commissioned (L361, *"The number on the notice, and the thirty or forty people who answered it, are in the dissent's opening pages"*) does its job, and is not enough on its own to reanimate a case that was knocked over at 7:56.

**Cheapest fix that preserves the relocation:** move the demolition of the phone number — L145 through L153 — **after** the ladder/plan block, so ACT_2 runs *mechanism → utility at full strength (L129–L173, ~4 minutes unanswered) → the single collapse at L175–L185*. That is the shape FILM_BIBLE §5.2 actually drew (28–33% strength, 33% collapse). v002 built the parts and shuffled them.

## 2.2 R6 — the eight states are installed, but not as a sequence

Order of appearance in the file, with position:

`1` (0.9%) → `3` (3.8%) → `5` (11.6%) → `2` (19.1%) → `6` (20.3%) → `4` (29.8%) → **`6` again** (59.6%) → `7` (75.9%) → `8` (99.9%)

Four defects, all checkable:

1. **The numbering is not the viewing order.** State 5 (the notice by the telephone) plays before state 2 (the notice with the white lower half), and state 4 plays after state 6. Standard §5: *"同じ物を、違う状態で、順番に見せる。状態の順序を先に決めてから台本を書く。"* A viewer cannot read 1→3→5→2→6→4 as a progression; it is a spreadsheet, not a story. (FILM_BIBLE §19 R6's own insertion table specified these positions, so v002 executed a flawed instruction faithfully. It is still a FAIL against the standard.)
2. **State 6 is used twice** (L125 and L279, *"motif state 6 returns"*). A state that returns unchanged is not a state change; it is a repeat, and it spends the payoff at 59.6% that the argument needs to be *new* at.
3. **An 8:57 hole in the middle.** Between state 4 (30.2%) and state 6's return (59.6%) the motif is absent for 29.4 percentage points. That covers the whole of ACT_3 — which carries **zero** `【】` directions of any kind across 755 words / 4:17 — and the first half of ACT_4. Directions per section: HOOK 2 · OP 0 · ACT_1 3 · ACT_2 3 · **ACT_3 0** · ACT_4 2 · ACT_5 2 · ENDING 3.
4. **The last image of the film has no defined content.** L427: 【motif state 8: the same envelope falls into the mailbox again. No narration.】 *The same* envelope as which one? If it holds the state-2 notice (white lower half), the image says the rewrite never happened — contradicting L207, L349 and state 7 (L351, *"this time there is type in the lower half"*). If it holds the state-7 notice, the loop's second meaning is *"now with the way out"*, which is a victory image the film is not allowed to make (FILM_BIBLE §5.3). **The single most important frame in the film is undetermined in the script.** Decide it in the direction, in words.

Also: **§19 S3's prescribed fix for ACT_4 was half-applied.** S3 said insert states 5 **and** 6 into ACT_4 to break up 1,065 words of consecutive quotation. State 5 went to ACT_1 instead; ACT_4 got state 6's repeat and one reset beat, and **grew to 1,108 words.**

## 2.3 The 8-second HOOK decision moved the film's hardest scene into the measured drop zone

`PD_SCREENPLAY_STANDARD` §16.5 settled HOOK length at 8 seconds; v002 complies (22 words, 7.5s, inside the 6–10s gate). But shrinking HOOK+OP from 234 words to 73 pulled the whole film forward by ~55 seconds, and **nobody re-measured what landed where.**

- **The contradiction scene now plays at 1:50–2:47.** FILM_BIBLE §8 placed it at 12% (≈3:40); in v001 it was at 11.9%; in v002 it is at **8.7%**. DEEP_RESEARCH's measured finding is that *"12/19 biggest post-minute cliffs at 80–180s = explanation blocks."* The film's most analytically demanding passage — *"There is a second account of the same events, inside the same opinion" / "Set the two side by side" / "The record does not agree with itself" / "That shape returns twice more"* — is now sitting exactly in that window.
- **The OP occupies 0:07–0:24 with docket metadata** (case name, argue/decide dates, author, disposition). DEEP_RESEARCH R-8: measured drops *"cluster at 11–24s"*, and *"concept-led opens 0.47–0.48 (worst)"*. §19 R2's replacement text is correct on craft and lands in the worst-measured seventeen seconds of a PD long-form.
- **§16.5 requires the 8-second HOOK to be taken from the longer version — *"新しい文を書かない"* (FILM_BIBLE §9.2, which nominates the existing closing sentences).** All three sentences of v002's HOOK are **new**: `Two meters on one wall.` / `Two bills, one letter apart.` / `After the final notice she telephoned and said she had already paid.` None appears in v001. That is how the meter-count error got in (§1.1c).
- **Promise-and-payoff, which §16.5 makes mandatory, is met for 2 of the 4 hook cuts.** M005 (the handset off its cradle) returns as motif state 5; M003 (two bills) returns as state 3 and verbally at L409. **M001 (two meters) and M002 (the turning disc) never return** as a direction anywhere in the script, and neither ID appears in `EP64_memphis_beats.v001.json`.
- **The film's first image is the object the bible refused.** FILM_BIBLE §3.1 rules the meters out as motif for three reasons, the first being *"メーターは直る"* — they get resolved at L239. The 8-second promise is therefore built on the one object in the film whose story ends in a fix, while the last image is the envelope. First image ≠ last image (§3-R11).
- **The HOOK names nobody.** Its first sentence is an object and its only human is an unattached *"she"* at 0:04. DEEP_RESEARCH R-8: *"loser signature = promo/sponsor/no-named-human up front"*; winners are *"declarative person + specific + incongruity."*

## 2.4 R10 — the reply-relocation pushed the dissent's closing out of bounds

Documented at §1.9. To restate the mechanism plainly: §19 measured only the two beats it happened to look at (ML-115, ML-116), moved them, and did not re-measure what filled the space behind them. ML-110 and ML-111 — **190 words, the two longest single quotations in ACT_5, both first appearances** — slid from 90.2%/91.6% to 92.65%/94.24%. The rule is a [MUST] in two documents. The fix is ~120 words of reordering: put ML-110 and ML-111 ahead of ML-107/ML-108 (L389/L391), which are the beats that can survive being late because they restate what the film already said about health and safety.

## 2.5 One deletion went further than §19 asked, and it was the guard rail

§19 R3-8 asked for the removal of *"This is the most common way the case gets told wrong, so here it is flat. A hearing before a shutoff is not the end of shutoffs."* The pass also deleted, without instruction, v001's preceding sentence: *"That is not a court switching off a power company. It is a court inserting one conversation into a schedule that can still end the same way."* That was the film's clearest plain-English statement of the limit. Deleting it is defensible under §7 (restraint) — but it is the sentence that most directly prevented the misreading §4b is about, and it went out unrecorded. Named here so the choice is a choice.

---

# 3. R1–R15 re-run fresh against v002

**Result: 9 PASS / 6 FAIL.** (v001: 4/11.) Machine gates for reference — `check_script_craft` **PASS** (emotion commands 0, AI-smell 0, you/1000w 0.93, questions 0, short sentences 31.6%, longest bare stretch 15.3s, specifics/min 11.22, quarantined claims 0); `check_script_length` **PASS** at 5,466 words with a flagged risk: *at the fast measured pace (237.4 wpm, seen on williams/florence) this lands at 23.0 min — under the floor.* Pin the voice speed before render.

### R1 — Can the controlling idea be said in one sentence? **PASS**
*A notice that does not tell you where to object is not notice; it is notification.* Everything converges on ML-68 at 59.6% (L277) and is held against ML-76 at 71.5% (L327). The theme is present and the film is built on it.

### R2 — Is that sentence absent from the script? **PASS**
Both v001 offenders are gone (§1.4). The nearest survivor is the Mullane standard restated as L271: *"Two halves. Tell them the thing is happening. And tell them they can object to it."* That is the Court's holding in plain words, not the film's thesis, and it is followed immediately by the factual application. Accepted. Watch L159 (§4a.4), which is closer to the line than anything else in the file.

### R3 — Delete every narrator conclusion; does the audience still arrive? **FAIL**
§19 named eight and eight were deleted. **The same move survives in at least sixteen places.** The pass was list-driven, not rule-driven.

| Line | Sentence | Why it is a conclusion, not a fact |
|---|---|---|
| L69 / L95 / L129 | *"Set the two side by side."* / *"Keep that sentence."* / *"Read the third step again."* | three direct commands to the viewer; the word-based second-person gate (0.93/1000) cannot see imperatives |
| **L129** | *"**There is a hearing buried inside it.**"* | neither opinion calls step (iii) a hearing; the Court held **no** opportunity was afforded. An interpretation, invented, delivered as observation |
| **L159** | *"Those are the words the Crafts needed on a piece of paper."* | asserts what the Crafts needed. ML-104 is three Justices saying precisely that they did not. Unattributed, at 29.4%, 55 points before the rebuttal |
| **L175** | *"And then the fact that decides it."* | tells the audience which fact decides the case. The holding (ML-83) rests on notice, not on the 33,000 |
| L175 | *"Thirty-three thousand disputes in a single year, in one American city."* | the record says *"high bill" complaints*; *disputes* and *in one American city* are the writer's |
| **L193** | *"The way they lost is the strangest page in the file."* | aesthetic verdict |
| **L197** | *"…except, possibly, the only two people still in the case."* | also factually wrong (§1.10) |
| L213 | *"In a document this careful, that word is load-bearing."* | instructs the audience how to read |
| **L309** | *"…and this is the sentence with the most bite in it."* | ranking |
| **L321** | *"It is the one that almost never gets quoted."* | claim about the world outside the record (§1.10) |
| L335 | *"The list of things the Court did not decide is longer than the list it did."* | unverified comparative |
| L347 | *"That is the size of the thing the Constitution was held to require."* | conclusion |
| **L355** | *"Now the dissent, and it is not a footnote."* | contradicted by the film's own structure (§2.1) |
| **L393** | *"Serious enough to sue over, or too small to be constitutional. Choose one."* | the narrator adopting the dissent's dilemma as decisive, and a fourth command to the viewer |
| **L399** | *"His closing is the sharpest paragraph either opinion produced."* | the narrator ranking the two opinions, at 94%, against ⛔-10 |
| **L413** | *"What the case settled fits on the page the utility was already mailing."* | the majority's burden analysis (ML-75) stated unattributed at 97.8%, when ML-110 disputes exactly that |

The five §19 explicitly protected (*"One house, one family…"*, *"Good faith there is a legal term…"*, *"Pay or face termination…"*, *"That shape returns twice more."*, *"Five times, said the majority…"*) are all still in and all still right. The problem is everything §19 did not enumerate.

### R4 — Is the recognition in one place? **PASS**, with an erosion
Mechanically yes: one `⟨HELD⟩`-plus-assertion cluster, at 45.6% (L219–L223). But the film **announces it at 2:45**: *"That shape returns twice more."* (L73) tells the audience that the money question will also be unresolved. §19 protected that line as §6 dramatic irony, and it is good irony — but it converts the 45.6% beat from a discovery into a promise being kept. Passing; the standard measures placement, and placement is correct.

### R5 — Was the other side stated at its strongest before the turn? **FAIL**
Position fixed, function not. Full evidence at §2.1. Decisive line: the utility's strongest fact (L143) is contradicted by L145, the very next sentence, 13:48 before the judgment.

### R6 — Can the motif's state changes be named in order? **FAIL**
1→3→5→2→6→4→6→7→8; state 6 twice; 8:57 with no motif; ACT_3 with no direction at all; state 8's content undefined. §2.2.

### R7 — Does every principal carry an unrepeatable detail? **PASS**
Mary Craft — missed work; telephoned after final notice and said she had paid. The employee — *"of uncertain authority" / "apparently without explanation or attempt at investigation."* The trial judge — wrote *hope*, in quotation marks, and then ruled for the utility; thirty-five dollars; *"terminations which should have been unnecessary."* Mullen — secretary-treasurer, 33,000 in 1973. Stevens — 523-0711; thirty or forty people; *"a paternalistic predicate that I cannot accept."* MLG&W — $2.50 a month, twice. Willie S. Craft and Powell are left as the record leaves them, correctly. §19 R7's condition was taken via option (a): the two counsel names are gone.

### R8 — Is anyone made a villain? **PASS**
All three tone defects removed; L133 now runs ML-33's instruction, which is the correct fix; *"Whatever else this case is, it is not a case about a utility that offered nothing"* survives at L173. Residual: *"The Crafts hired somebody and their man got it wrong"* (L63) is dismissive of the contractor, and *"in one American city"* (L175) editorialises. Neither makes a villain.

### R9 — Do the stakes rise vertically? **FAIL**
Rungs 1–4 at 3.8 / 23.5 / 33.2 / 34.7% — four rungs inside a 31-point window, then nothing for fifty points. **Rung 5, the assumption itself (ML-104, L381 at 84.9%), is rebutted at 86.5% by the majority's footnote (L383).** FILM_BIBLE §4.1 wrote *"語り手は何も足さない…この段は、直前の四段が積んであれば自動的に立つ"* — but the film does not add nothing after it; it adds the counter-argument 1.6 points later. The floor of the ladder is stepped on before the audience can stand on it. Reordering L383 to follow L385 (the reductio) would let rung 5 hold for one beat.

### R10 — Is there nothing new after 92%? **FAIL** ([MUST])
394 words / 2:14 past the line; 190 of them are ML-110 and ML-111 in first appearance. Created by the R10 repair itself. §1.9, §2.4.

### R11 — Does the ENDING return to the first image? **PASS**, with a named exception
It returns verbally and completely: L409 restates the two bills and the one-letter name; L419 restates the phone call in the HOOK's own words; L423 lands *"She was given no satisfaction."* The macro loop state 1 (0.9%) → state 8 (99.9%) closes.
**Exception:** the film's *literal* first image is 【M001 two meters bolted side by side】 and its literal last image is an envelope. The HOOK opens on the object FILM_BIBLE §3.1 explicitly refused as the motif, and that object never returns. Two of the four HOOK cuts (M001, M002) are unpaid promises.

### R12 — Can the three silences be named? **PASS**
Exactly three, all where §7.2 put them: **45.6%** after *"Nobody ever decided whether the Crafts owed the money…"*; **71.5%** after ML-76; **99.9%** after *"She was given no satisfaction."* Down from twelve. This is the cleanest repair in the pass.

### R13 — Is the contradicting record shown as contradicting? **PASS with three named exceptions**
Four collisions, all staged, none resolved, each attributed: L61+L63 vs L65+L67 (whose mistake), L211 vs L215 (the money), L363+L365 (how many terminations), L371+L373+L375 (whether she met authority). L219–L225 states the non-decision outright and L409–L411 restates it in the ENDING. **This remains the best thing in the script.** The three exceptions — all matters of ordering and emphasis rather than wording — are §4a below.

### R14 — Is the record's silence left silent? **FAIL**
The two flagged fills are gone. L197 is a new unsupported claim; L321 is the deleted meta-move surviving in a new sentence; L207 overstates ML-51. §1.10.

### R15 — Was it read aloud? **FAIL — not performed, and I cannot perform it**
Neither I nor the caller can listen. §5 is a substitute analysis, explicitly labelled as such. It is not a substitute for the reading, which §16 says must not be skipped and which the FILM_BIBLE already ordered specifically for ACT_4 and ACT_5.

---

# 4. The two things this episode cannot survive getting wrong

## 4a. The record contradicts itself — the words do not adopt a side. **The ordering and the emphasis do.**

**First, the concession, because it is large.** Every collision is stated with both accounts and neither adopted. `\bovercharg\w*` never attaches to the Crafts in the film's voice. ML-30 is cut before the *"had overcharged them"* clause. *possible* is retained at L211 and L411. The ⛔ sweep is clean. On the words, this is a model.

**Now the attack. A viewer takes away a shape, and four features of the shape lean one way.**

**4a.1 — Whose mistake: majority first, three times out of three, with asymmetric status.**

| | The majority's version | Footnote 7's version |
|---|---|---|
| L61–L67 | preceded by *"And then the sentence the first half of this case turns on"* — a build-up | preceded by *"There is a second account"* — a subordinate |
| framing | *"That is the majority's account."* | *"the Court quotes **the brief filed by the Crafts' own lawyers**"* — a party's self-interested assertion |
| plain-English gloss | *"The Crafts hired somebody and their man got it wrong."* — quotable, memorable | **none** |
| L69 | *"The **body** of the opinion says…"* | *"The **footnote** says…"* |
| L409 (ENDING) | *"The majority says a contractor the Crafts hired."* | *"A footnote quoting **their own brief** says the utility."* |

Three appearances; majority first every time; the majority gets the only colloquial restatement; the footnote's provenance is flagged as partisan on two of the three. Both descriptions are accurate. The *weighting* is not neutral, and a viewer who remembers one sentence will remember *"their man got it wrong."*
**Fix, cheap:** give footnote 7 a gloss of equal register (it can be as plain as *"That is the Crafts' account, and the Court printed it"*), and alternate the order — footnote first in the ENDING.

**4a.2 — The count: the majority's number is the film's number for twenty-two minutes.**
*"five times"* is spoken at **2:47** (L75) as bare narration, and the very next line uses it in the narrator's own voice — *"No month for any of **the five**"* (L77). The dissent's *"several occasions"* does not arrive until **24:59** (L363), and the balancing pair — *"Five times, said the majority. Several occasions, said the dissent."* — is one sentence at **25:05**. That is 22 minutes 18 seconds of *five* as fact against four seconds of *five* as one side's claim.
Worse: **the phrase is pre-spent.** *"On several occasions"* is already used at L79 (2:51) for a different fact — Mrs. Craft's trips downtown (ML-25, majority). By the time it becomes the dissent's competing count, the audience has heard it as ordinary narration. The collision is audible only to someone reading.
ML-118 does license *five*, attributed. **L77 is not attributed** — it attributes only the phrase *"During this period."* Add four words: *"No month for any of the majority's five."*

**4a.3 — The structure of ACT_2 uses the dissent as a straight man.**
L143 (the dissent's strongest fact) → L145 (the majority's answer), with nothing between. The dissent's evidence enters the film in the grammatical position of a set-up. This is the ordering adopting a side without a single word doing so. §2.1.

**4a.4 — The last two narrator judgments in the film are the majority's, unattributed.**
- **L413 (97.8%)** — *"What the case settled fits on the page the utility was already mailing."* That is ML-75's burden holding (*"Nor should 'some kind of hearing' prove burdensome"*) asserted as fact. ML-110 — which the film quotes 5 points earlier — is Stevens saying judges have *"no similar ability to balance the cost of scheduling thousands of billing conferences."* The film picks the majority, in its own voice, in the ENDING, where ⛔-10 says attribute every time.
- **L421 (99.4%)** — *"two irreconcilable accounts of **one set of meters**."* Meters, not accounts. §1.2.
- Add **L159 (29.4%)** — *"Those are the words the Crafts needed on a piece of paper"* — and the film's three most quotable narrator sentences all take the majority's side of a live dispute.

**Answer to the brief:** the words adopt neither. **The order, the glossing, the dwell time and the ENDING's two closing judgments adopt the majority.** Six small edits, none of them requiring a new fact, close it.

## 4b. A hearing before a shutoff is not the end of shutoffs

**The film gets the doctrine right and repeats it three times.** L327 runs ML-76 verbatim (22-word run, `after affording` occurs once in the whole opinion). L329 breaks it into three beats. L331 reads the schedule back instead of asserting the conclusion — which is the correct §19 R3-8 fix and works. L335–L343 lists what the Court did not do: no restoration, no injunction, no money, no class, no impartial decisionmaker, no written decision. L415 puts the limit inside the ENDING. Mechanically, `must now` / `cannot cut` / `can no longer` / `struck down` / `reversed` all return 0.

**So: does the ending leave a viewer believing the Crafts won something they did not? Three ways in which it can.**

1. **The word *affirmed*, twice, unglossed.** L29 at **0:17** — *"The Supreme Court affirmed the judgment below"* — before the viewer knows what the judgment below was. L319 at 70.9% — *"The judgment of the Court of Appeals is affirmed."* Both are correct and both read, to a general audience, as *the family won*. The film's own correction (L337–L343) is at 72.8–73.5% **and is never repeated.** By the ENDING, twenty-seven minutes and thirteen minutes have elapsed since the two *affirmed*s and seven minutes since the only line saying the Crafts personally got nothing.
2. **The ENDING's ledger is 41 words of gains, then 15 words of limit.** L413 lists four things the case settled and ends on *"obliged to hear the complaint before the meter reader arrives."* L415 answers with *"After that, the meter reader **may** still arrive."* *May* is a weaker word than ML-76's *would retain the option*: it reads as possibility, not as a preserved power. The gain is stated first, longer, and in the concrete; the limit is second, shorter, and modal.
3. **The film deleted, unprompted, the sentence that most bluntly blocked this reading** — v001's *"It is a court inserting one conversation into a schedule that can still end the same way"* (§2.5).

**And there is an opposite error, which is the one I would actually bet on.** The last spoken line is *"She was given no satisfaction."* and the last image is the envelope falling into the mailbox again. A viewer's emotional takeaway is **nothing changed** — which is a claim the record contradicts twice inside this same film (L205: the utility issued the credit and instituted new procedures before December 1974; L349: *"Petitioners have moved to clarify and regularize their notice procedure"*). Whether the loop means *nothing changed* or *now the way out is printed* depends entirely on which notice is inside the state-8 envelope, and **the script does not say** (§2.2.4).

**Verdict on 4b:** the film does not overclaim the win — it leaves the win and the loss both available and resolves neither, and its final image is the place where that ambiguity is decided. Three fixes: (a) attach one clause to L29 so the first *affirmed* cannot be heard as *the family collected* — the Court's own posture is enough (*"and sent the damages question back down undecided"* is already in the film at L339/L411); (b) restate at L413/L415 in the ENDING that no money was ordered, since it is not a new fact (L339, L411) and R10 permits recycling; (c) **specify the envelope.** The honest choice, and the one that keeps §5.3's trap shut, is the state-2 notice — the same blank lower half — with the state-7 rewrite already shown at 75.9% so the viewer holds both. Write it in the direction.

---

# 5. R15 — SUBSTITUTE SPOKEN-FORM ANALYSIS

> **Label, per the brief: this was NOT performed. Neither I nor the caller can listen.** What follows is a static analysis of features that damage a read, produced from the text. §16 of the standard says R15 must not be skipped, and the FILM_BIBLE ordered a stopwatch read of ACT_4 and ACT_5 specifically. **That reading is still outstanding and this section does not discharge it.**

## 5.0 Punctuation-anomaly sweep — the `,.` siblings

The `,.` the fact_recheck caught at L171 **is gone (0 hits).** I looked for its family across the spoken body: `,.` · `..` · ` ,` · ` .` · double spaces · `;.` · doubled words · doubled dashes. **All zero.** There are 0 parentheses and 4 colons. There is no second instance of that class of defect in the file.

## 5.1 The largest spoken-form problem: **there is not one quotation mark in the script**

`"` / `“` / `”` → **0 occurrences in 5,364 words.** Every one of the 98 quotation-bearing lines runs as bare narration. On the page a reader can infer the boundary; **a listener has no signal at all** for where the Court stops and the writer starts. This interacts directly with ⛔-10, which requires attribution every time the two accounts are mixed. Concretely:

| Line | The problem for the ear |
|---|---|
| **L61** | *"And then the sentence the first half of this case turns on. Because the contractor did not consolidate the meters properly…"* — the quotation opens mid-paragraph with no marker; attribution arrives only at L63, **after** the sentence has landed as narration |
| **L253** | *"So the answer was in Tennessee, and the Court went and got it. A company supplying electricity to the public has a right to cut off service…"* — *Trigg*, unannounced |
| **L133 → L121** | L133 is the writer's summary of step (iii) and L121 is step (iii) verbatim. Aurally they are the same voice saying nearly the same thing twice |

**Fix without adding words:** the direction layer already exists (`【】`). Add a voice/register direction at each quotation open, or adopt a single audible convention (a beat of silence, a filter, a second read pace) and mark it in the script.

## 5.2 Nine first-person voice shifts, eight of them unmarked

The reader must become Justice Stevens or the Court, with no notated change:

| Line | The pronoun | Marked? |
|---|---|---|
| L287 | *"**We** agree with the Court of Appeals…"* (the Court) | no |
| L343 | *"…**the Court wrote**, we do not decide whether…"* | **yes** — the only one |
| L357 | *"**In my judgment**, the Court's holding confuses and trivializes…"* | lead-in only |
| L359 | *"**I** have no quarrel with the Court's conclusion…"* | lead-in only |
| L379 | *"…even if **we** assumed that Division employees, like federal judges, are occasionally discourteous…"* | lead-in only |
| L381 | *"…a paternalistic predicate that **I** cannot accept."* | lead-in only |
| L397 | *"As judges **we** have experience in appraising…"* | lead-in only |
| L399 | *"**I** do not believe the Constitution requires the State…"* | lead-in only |
| **L401** | *"**I respectfully dissent.**"* — three words, alone, at 95.9% | **no** |

L401 is the exposed one. Read by the narrator with no register change and no attribution in the sentence, **the film's narrator appears to dissent from the film.** Either mark it or put the byline back in the line.

## 5.3 Sentences over ~25 words with no internal comma — 13

Nowhere for the reader to breathe. All are verbatim court prose, which is why they survived a quotation audit.

| Line | Words | |
|---|---:|---|
| **L199** | **44** | *"He hoped that credit in the amount of thirty-five dollars be issued to reimburse the Crafts for duplicate and unnecessary charges made and expenses incurred by them with respect to terminations which should have been unnecessary had effectual relief been afforded them as requested."* — **the worst line in the script to read aloud**, and it is the payoff of the trial-judge beat |
| **L359** | 39 | *"I have no quarrel with the Court's conclusion that as a matter of Tennessee law a customer has a legitimate claim of entitlement to continued utility services as long as the undisputed portions of his utility bills are paid."* |
| **L287** | 38 | *"We agree with the Court of Appeals that due process requires the provision of an opportunity for the presentation to a designated employee of a customer's complaint that he is being overcharged or charged for services not rendered."* |
| **L275** | 36 | *"Notice in a case of this kind does not comport with constitutional requirements when it does not advise the customer of the availability of a procedure for protesting a proposed termination of utility service as unjustified."* |
| L215 | 34 | *"The reference to duplicate charges apparently concerns the two dollars and fifty cents per month city service fee which was charged on each set of meters in the duplex until after they were consolidated."* |
| L253 | 34 | *"A company supplying electricity to the public has a right to cut off service to a customer for nonpayment of a just service bill and the company may adopt a rule to that effect."* |
| L141 | 32 | *"These employees also direct callers to credit counselors who are authorized to resolve disputes on a more permanent basis and who can set up extended payment plans for customers in financial difficulty."* |
| L67 | 30 | *"Not until after the action was filed were the Crafts able to discover that they continued to receive double computer billings because MLG&W failed to combine the two accounts properly."* |
| L391 | 29 | *"A potential loss of utility service sufficiently grievous to qualify as a constitutional deprivation can hardly be too petty to justify invoking the aid of counsel or the judiciary."* |
| L399 | 29 | *"I do not believe the Constitution requires the State to employ procedures that are so simple that every lay person can always act effectively without the assistance of counsel."* |
| L145 | 28 | *"The final notice contained in MLG&W's bills simply stated that payment was overdue and that service would be discontinued if payment was not made by a certain date."* |
| L299 | 26 | *"The opportunity for a meeting with a responsible employee empowered to resolve the dispute could be afforded well in advance of the scheduled date of termination."* |
| L309 | 26 | *"Equitable remedies are particularly unsuited to the resolution of factual disputes typically involving sums of money too small to justify engaging counsel or bringing a lawsuit."* |

Longest sentences overall: **L317, 63 words, 2 commas** (the holding) · **L381, 62 words** · **L397, 51 words** · seven at 42–46.

## 5.4 Sentences whose meaning depends on punctuation a listener cannot hear

| Line | |
|---|---|
| **L381** | *"**For** a homeowner surely need not be told how to complain…"* — *For* is the conjunction *because*. The ear parses *"For a homeowner"* as a prepositional phrase and is lost for four words. **This is the film's controlling idea in its negation**, the single most important sentence the opposition owns |
| **L197** | *"Nobody was substantially deprived — except, possibly, the only two people still in the case."* — the entire irony is carried by the dash |
| **L185** | *"…to be posted or otherwise available for convenient inspection by customers — but only for an independent utility district, as opposed to a utility division of a municipality."* — 44 words, one comma, the reversal on a dash at word 27 |
| **L159 / L183** | *"If there is any dispute concerning the amount due."* and *"Depending on the vagaries."* — deliberate fragments that repeat a phrase heard seconds before. Spoken cold they are unfinished sentences; the second is a dangling participle with no head |
| **L399** | *"It is an unfortunate fact that when the State assesses taxes or operates a utility, **it** occasionally overcharges the citizen."* — antecedent of *it* is ambiguous by ear |
| **L167** | *"Credit counselors **came** first. If those counselors **cannot** satisfy the customer, then the customer **is** referred to management personnel; generally the chief clerk in the department; then the supervisor in credit and collection."* — past → present inside one beat, plus a semicolon list |
| **L111** | *"…sued in both their official and personal capacities: the president and general manager, the vice president, members of the Board of Commissioners, and two employees who have had responsibility for terminating utility services."* — a five-item list after a colon |
| **L175** | *"…thirty-three thousand **high bill** complaints…"* — the opinion quotes *"high bill"*; without the quotes the ear may hear *high, bill complaints* |

Six sentences carry semicolons (L167, L295, L363, L381, L385 ×2). A semicolon is not audible.

## 5.5 `MLG&W`, `§`, and number style

- **`§` → 0 occurrences.** L111 spells it: *"not a person within the meaning of section 1983."* Correct.
- **`MLG&W` → 15 occurrences**, of which two are possessive (*MLG&W's*, L145 and L243). The name is expanded exactly twice, both in the first 4½ minutes (L27, L103), and never again. Whether the voice says *"em-el-gee-and-double-you"* or *"Memphis Light Gas and Water"* is undecided in the script; at 15 repetitions that decision is not cosmetic.
- **L57 — `a MLG&W meter reader`.** Verbatim from the opinion, and **wrong in the mouth**: spoken as an initialism it requires *an*. This is a v002 addition (v001 had *"a meter reader"*). Either expand it here or accept the stumble.
- **L37 — `1019 Alaska Street`.** A four-digit house number reads as *"one thousand and nineteen"* on most TTS. If the number stays (§6.2 says it should not), write it as *ten nineteen*.
- **L139 — `Phone 523-0711, information center.`** A seven-digit string mid-sentence.
- **Number runs.** Only one sentence carries three numerals — **L137**: *"During the six months from September 1973 through February 1974, there were 11,216 so-called delinquent cutoffs."* Two dates and a five-figure number in 16 words. It follows immediately after *"about 2,000 customers."* L421 carries three spoken numbers in a row: *"Three courts, four years, two irreconcilable accounts…"*
- **Style is inconsistent and will be voiced inconsistently.** `30 or 40` (L141) then `Thirty or forty` (L143) — same fact, one line apart. `2,000` (L137, L389) vs `thirty-three thousand` (L175) vs `11,216` (L137). `October 1972` (L43) vs `the twenty-second of February, 1977` (L235) vs `the thirtieth of December, 1974` (L205). Pick one convention before the caption file is generated, because these differences will show on screen.

## 5.6 Stacked proper nouns

- **`Memphis Light, Gas and Water Division`** — L27 and L103. Five words with an internal comma the reader must pause on, so the ear receives *Memphis Light* … *Gas and Water Division* as two things. It is unavoidable (it is the case name) but it should be read as one unit, and the script should say so.
- **L355** — *"Justice Stevens, with the Chief Justice and Justice Rehnquist, dissenting."* Three judicial titles in eleven words, one of them unnamed.
- **L111** — *"the president and general manager, the vice president, members of the Board of Commissioners, and two employees…"*
- **L175** — *"William T. Mullen, secretary-treasurer of MLG&W, testified…"* — a middle initial plus a hyphenated compound title plus an initialism in nine words.

## 5.7 Where a stopwatch read must actually happen

- **L199** (44 words, 0 commas) — the trial-judge payoff.
- **ACT_4, 15:29–21:48**, 1,108 words, ~20 consecutive quotations, one direction and one reset beat. §19 S3 flagged this section for a read and its prescribed fix was half-applied; the section got **longer**.
- **ACT_5's dissent block, L355–L401 = 23:20–29:14** — seven first-person shifts into Stevens, five semicolons, and two of the three longest sentences in the film.
- **17:05 → 24:59 carries no number and no date for 7:54.** `check_script_craft` passes it (its 90-second gate counts proper nouns, and the measured bare stretch is 15.3s), so this will not appear in any machine report. It is the section most at risk of the standard's §8 failure mode — *"上回ると資料になる"*.

---

# 6. Rulings on the two open items

## 6.1 ML-123 — **ADD IT, and fix quarantine row -08 in the same edit**

**Ruling: add ML-123 (DISSENT) and cross-reference it under ML-121 in §12.**

Reasons.

1. **What is uncovered is not decorative.** ML-102 begins at *"It is worth remembering…"*. The two sentences the script speaks at L373 — *"Mrs. Craft testified on direct examination that after being cut off she went to the Division's office with the record of her payments on one account. She was told that she had to pay on the other account as well."* — are **not in any row.** I confirmed them verbatim in `EP64_memphis_RAW.md` line 259, in dissent n. 7 (the opinion's own citation there is *Id., at 91* — App. 91, **the same page the majority cites for ML-28**). Those two sentences are the load-bearing half of the ML-121 collision: they are the dissent's evidence that Mrs. Craft *did* reach someone with authority. Invariant 1 does not permit 41 spoken words of that weight to rest on no row.
2. **It fixes the film's worst craft compromise.** The one line of actual human speech anywhere in this record is *"[w]ell, you have to pay on the other" bill* (ML-28). The script speaks it **nowhere**, in either opinion's version, because quarantine row -08's string `you have to pay on the other` is quoted so bare that `check_script_craft`'s substring matcher fires on any correct, attributed use — a defect the contract itself records and calls a **gate/ledger defect to be fixed in the gate or the ledger.** The script's workaround is to convert both appearances to reported speech (L91, L373). The cost is exactly what standard §7 says must never be paid: *"最良の台詞は既に書かれている。証言をそのまま鳴らす"* — the film's only quotable human sentence has been paraphrased out of existence to route around a tooling bug. Re-quote row -08 with enough surrounding words to be unambiguous (`told Mrs. Craft, apparently without explanation or attempt at investigation, "[w]ell, you have to pay on the other" bill`), add ML-123, and **restore the majority's direct speech at L91.** One ledger edit, three returns.
3. **It also exposes a staging error the recheck could not see.** The script places the employee's sentence at L91, immediately after 【motif state 5: the notice lies on the table beside the telephone, the handset off its cradle】 — so the image says the employee said it **on the telephone**. Both sources place it at the Division's **office**: dissent n. 7 says *"after being cut off she went to the Division's office"*, and the script itself says so at L373 and then says *"Same sentence. **Same office.**"* at L375. **The film contradicts its own staging.** Move state 5 to sit on L87 (the ML-27 phone-call finding, which is genuinely a phone call) and give L91 its own image, or move the employee beat.

## 6.2 ⛔-08 — **the names yes, the house number no**

**Ruling (recommendation; this is an owner call and must be recorded as an APR before build): speak the names, remove the street number from every on-screen element, and keep it spoken at most once inside the Court's own sentence.**

Reasons.

1. **The names are not severable from the case.** *Craft* is the caption. *Willie C. Craft* versus *Willie S. Craft* is the film's motif state 3, its HOOK, and its ENDING. A version that anonymises them has no story. They are on the first page of a published U. S. Supreme Court opinion; naming them is not disclosure.
2. **The number is severable, and the film already proves it.** *Alaska Street* is used without the number at L113 (*"the family on Alaska Street"*) and L165 (*"Which of them reached Alaska Street the record does not establish"*). The number appears once in narration (L37) and adds nothing the film uses.
3. **The on-screen version is the real exposure.** `EP64_memphis_beats.v001.json`, HOOK beat 1, is a lower third reading **`1019 Alaska Street, 1972`**. On-screen type is freeze-frameable and searchable; narration is not. 1019 Alaska Street is a real dwelling with present occupants who have nothing to do with this case, and the contract already forbids *"any real building… identifiable by signage or architecture"* — identifying it by street number is the same act by another route.
4. **Where I would keep it.** L37 quotes the Court's own opening sentence about them, and the beat that follows (*"That sentence belongs to the Court, and it is very nearly everything the Court says about them"*) depends on the sentence being **the Court's, entire**. So: leave L37 verbatim; **strike the number from the beats file and from every plate, telop and thumbnail**; change the lower third to `ALASKA STREET, MEMPHIS · 1972`.
5. **What to log.** Whatever the owner decides, `⛔-08` must move out of OWNER CALL to a recorded decision in the ledger and an APR entry, because `SHORTS_SLATE_EP62-65.v001.md` also puts `WILLIE C.` / `WILLIE S.` on screen with no decision behind it (that audit's §8). One ruling should bind both threads.

---

# 7. VERDICT

## **DOES NOT MEET THE STANDARD.**

**9 PASS / 6 FAIL** against R1–R15 — a real improvement on v001's 4/11, and every mechanical gate is green. It fails on six, including one **[MUST]** (R10, §12 of the standard and R-14 of `DEEP_RESEARCH_FINDINGS`), and it carries three factual defects that a quotation audit structurally cannot see.

**Blocking (must be fixed before `script_verified`):**

| # | Item | Where | Class |
|---|---|---|---|
| B1 | *"Two meters on one wall"* — the record has four gas/electric meters plus one water meter; the film contradicts itself at L43; already propagated to a kinetic card in the beats file | L19, 【M001】, beats HOOK | **fact** |
| B2 | *"the only two people still in the case"* — ML-48 says *individual plaintiffs*, plural | L197 | **fact** |
| B3 | *"It is the one that almost never gets quoted"* — a claim about the world outside the record; the deleted move surviving in a new sentence | L321 | **§15-adjacent / R14** |
| B4 | 190 words of first-appearance ACT_5 material past the 92% line, created by the R10 repair | L397, L399 | **[MUST]** |
| B5 | Motif state 8's content undefined — the film's final image can mean *nothing changed* or *the way out is now printed* | L427 | **R6 / 4b** |

**Named exceptions to carry forward if the owner ships without fixing them** (each defensible, none free): R3's sixteen surviving narrator conclusions · R5's 86-second unanswered window before a 13:48 gap to the judgment · R6's non-monotonic state order and the 8:57 motif hole with ACT_3 carrying no direction at all · R9's rung 5 rebutted 1.6 points after it lands · the four ordering/emphasis leanings toward the majority at §4a · the eight-second HOOK written from new sentences, opening on the object the bible refused, with two of four cuts never paid off · the header's own 30:23 / 30:30 disagreement · ML-60 deleted with no record · R15 not performed.

**What this costs to fix:** no new research, no new source, no re-derivation of `mandatory_stills` beyond the HOOK plates. B1–B3 are three sentences. B4 is a ~120-word reordering. B5 is one clause in a direction. §2.1's ACT_2 reshuffle is a block move of nine existing paragraphs. §4a is six small edits. Then the ledger edit at §6.1 and the owner ruling at §6.2 — and **then the stopwatch read of ACT_4 and ACT_5 that R15 has now been deferred on twice.**

---

*v001 · 2026-08-04 · adversarial re-review of `EP64_memphis_script.en.v002.md`. Every position figure is a word-percentage measured from the file, converted at the contract's 176 words per finished minute. Every retired string was checked by search against the current file, not against a changelog. No fact in this document comes from memory; the only primary source consulted is `episodes/_planning/measurements/EP64_memphis_RAW.md`. R15 was NOT performed and §5 is labelled as a substitute.*
