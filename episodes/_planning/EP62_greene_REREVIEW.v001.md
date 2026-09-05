# EP62 · GREENE v. LINDSEY — ADVERSARIAL RE-REVIEW v001

**Target:** `episodes/_planning/EP62_greene_script.en.v003.md` **as it exists on disk now** (mtime 2026-08-04 12:52)
**Standard:** `docs/PD_SCREENPLAY_STANDARD.v001.md` §16 (R1–R15, BINDING)
**Design:** `episodes/_planning/EP62_greene_FILM_BIBLE.v001.md`
**Facts:** `EP62_greene_FACTS_LEDGER.v001.md` · primary `measurements/EP62_greene_RAW.md` · contract `episodes/PD-2026-062-greene/episode_spec.v001.json`
**Prior instruments re-adjudicated:** `EP62_greene_CRAFT_REVIEW.v001.md` (12 FAIL) · `episodes/PD-2026-062-greene/01_research/fact_recheck.v001.md` (7 open, 3 flags)

> **Brief (JP):** 「v003 は水準を満たした」という主張の**反証**を目的とした再レビュー。
> 前二回の指摘の**未消化・部分消化・移動しただけ**を現物照合で洗い、修理が**新たに作った**欠陥を探した。
> 結論：**DOES NOT MEET IT.** 新規/未解決の実害 **21件**（うち一次資料と食い違う引用 1件、
> 検証パケットの誤 LOCKED 1件、修理が作った文法破綻 2件、発注書に残った F1「7〜8人」 1件）。

> **This review's own honesty note.** I cannot listen to the script and neither can the reader,
> so §6 is labelled a **substitute** for R15 and claims nothing about a read-aloud having happened.
> Everything else below is quoted from the file it names. Where I could not settle a question with
> the primary source in front of me, the row says so.

---

## 0. What I measured, with the instrument stated

Narration = every non-empty line under a `##` heading that is not a heading, rule, bold metadata line,
`【】` direction or `⟨HELD⟩`; inline `【】`/`⟨HELD⟩` stripped; tokens counted only if they contain a
letter or digit (so bare `—` and `·` do not count as words).

| Measure | v003 header claims | Measured now | Verdict |
|---|---:|---:|---|
| Narration words | **5,225** | **5,239** | inside band [5,100–5,600] · header off by 14 |
| Runtime @176 wpm | **29:41** | **29:46** | inside `runtime_seconds` [1620,1920] |
| HOOK | 24 | 24 | — |
| OP | 25 | 25 | — |
| ACT_1 | 1,050 | 1,043 | −7 |
| ACT_2 | 617 | 614 | −3 |
| ACT_3 | 881 | 881 | — |
| **ACT_4** | **872** | **904** | **+32 ≈ +11 s** |
| ACT_5 | 1,544 | 1,537 | −7 |
| ENDING | 211 | 211 | — |
| Sentences | — | 408 | — |
| Short (≤6 w) | — | 128 = **31.4 %** | inside 20–35 % |
| `?` in narrator's voice | — | **0** (all 5 are inside deposition quotes) | PASS |
| `you / your` | — | 13 = **2.48 /1000 w** | inside ≤8 |
| `⟨HELD⟩` | 3 | **3** (L165, L293, L359) | count correct |
| `【】` directions | — | 14 | — |

**Finding 0-A · the header makes a false claim about itself.** L9 states:
*"Section windows re-derived from this file's measured word counts at 176 words per finished minute."*
ACT_4 is 904 words, which is 5:08, not the 4:58 its label allots. Every section window from
`ACT_5 (19:43–…)` onward is therefore ~11 seconds early, and `ENDING (28:29–29:41)` is wrong at both
ends. The windows were not re-derived from this file. This matters because the acceptance chain reads
section windows, and because the 92 % line for R10 is computed from them.

---

## 1. The provenance defect — this is the largest single finding

`fact_recheck.v001.md` was written at **12:48**. `EP62_greene_script.en.v003.md` was **modified at 12:52**.
The repairs for OPEN-1 through OPEN-7 were applied **in place, to v003**, four minutes after the packet
that certified v003 was written.

Consequences, all verifiable:

1. **The fact_recheck no longer describes a file that exists.** It measures "v003 (5,460 narration
   words)"; the v003 on disk is 5,239. It reports OPEN-1 as *"L73 — It is three sentences long"*;
   L73 now reads *"It is **two** sentences long"*. Roughly a dozen of its line numbers still land,
   which makes it look current and is worse than if none did.
2. **No v004 exists.** `CLAUDE.md` invariant 6 and `.claude/rules/12-revisions-and-staleness.md`
   require a new revision on a semantic input change. The packet's own §9 item 1–4 says the fixes
   produce "the resulting **v004**" and that the sweep must be re-run on it. Neither happened.
3. **The sweep in §0 of the packet was never re-run** (§9 item 4). The only mechanical verbatim
   instrument in this chain is now stale with respect to the text it certified — and §2 below shows
   it was already wrong about one passage before the edit.
4. **`manifest.json` was written at 12:52 with `"state": "script_verified"`.** Per `CLAUDE.md` §9 a
   state transition needs a quality-gate pass. The gate of record says
   *"PASS_WITH_7_OPEN_ITEMS … **Not clear for render until §6 is closed**"* and lists FLAG-1/2/3 as
   must-fix "in the same batch". FLAG-1, FLAG-2 and FLAG-3 are **not applied** (§3 below). The state
   was advanced past a gate that had not passed.
5. **`EP62_greene_beats.v001.json` (12:22)** predates both the packet and the edit and is stale.

None of this is a craft judgement. It is the record.

---

## 2. The craft review's 12 FAILs, re-adjudicated against the current text

Quotations are from the file as it is now. Line numbers are current v003.

### R2 — the narrator reads the theme aloud → **PARTIALLY RESOLVED**

- (a) L332 43-word thesis sentence: **RESOLVED.** L343 now stops at *"Not a rule about envelopes. A method."*
- (b) OP: **RESOLVED.** L33 is *"The case is about a piece of paper."*
- (c) *"Two words in that sentence carry the case."*: **NOT RESOLVED — the defect moved.**
  The order was: delete the preamble and *"place `**Well aware.**` alone."* Current text:

  > L163 `Well aware.`
  > L165 `⟨HELD⟩`
  > L167 `The people responsible for the notice knew the notice did not stay put.`

  v002 read *"Two words in that sentence carry the case. Well aware. The people responsible for the
  notice knew the notice did not stay put."* The preamble was cut and **the gloss was kept and promoted
  to its own line, immediately after the held silence.** The narrator now explains the recognition in
  the one place the standard reserves for saying nothing (§11: silence is *"認知の直後"*). A repair that
  relocates the explanation from before the beat to after it has not removed it.
- (d) *"Now the part that gets misremembered…"*: **RESOLVED** as a sentence — but see R3 below; the
  identical move survives at L189.
- (e) L167/L192 self-certification: **RESOLVED.**

### R3 — volume of narrator conclusions → **NOT RESOLVED**

The seven deletions listed in the craft review's table were made. The class was not cleared. Sentences
still doing the audience's work, all in the narrator's voice, all in the current file:

| Line | Sentence |
|---|---|
| L167 | *"The people responsible for the notice knew the notice did not stay put."* |
| **L189** | *"What the tenants themselves said was narrow, and it needs to be repeated exactly, because it is the single most likely thing to be got wrong about this case."* |
| L187 | *"That is the entire evidentiary base of this case, and how much weight it could bear became the argument that split the Court."* |
| L219 | *"The presumption was doing all the work."* |
| L225 | *"Which is how the sheriff's side had described the statute. The one the Supreme Court would later refuse."* |
| **L227** | *"Hold those two things together, because they are the strangest page in the file."* |
| **L231** | *"Its line is the sharpest sentence in the whole history of the case…"* |
| L239 | *"So this was not a hypothetical remedy invented by judges. It was a stamp, and another State was already buying them."* |
| **L245** | *"The people in the room are worth naming, because they tell you who thought this mattered."* |
| L257 | *"Two conditions, and the second is where this case lives."* |
| L277 | *"The apartment they were trying to take was the place they would have got the letter."* |
| L289 | *"Far from the ideal means. The majority, about its own preferred remedy."* |
| L315 | *"One read the words. The other read the depositions."* |
| L329 | *"The category was not the question. What the paper did was the question."* |
| L337 | *"That is where the two opinions stop talking to each other."* |
| L349 | *"Which leaves the case resting where it started: on the difference between what a procedure is written to do and what it was observed doing."* |

L189, L227 and L245 are the **same move** the craft review deleted at v002 L278 — the narrator
announcing what he is about to do, why he is doing it, and how the audience should hold it. All three
were present in v002 and **neither instrument flagged them.** L349 is FILM_BIBLE §1's subtitle couplet
(*紙の上では慎重で、現実では雑な手続き*) spoken in English, 20 seconds before the end.

### R4 — one recognition → **PARTIALLY RESOLVED**

The four surplus `⟨HELD⟩` marks were removed, which is what the review ordered. But the review's
diagnosis was that there were **five competing recognitions**, and only their silences were taken away;
the beats themselves are intact and two of them are now ten lines apart:

- L155–157 *"The Housing Authority told us." / … / "The Housing Authority's own staff had told the men doing the posting that the papers came off the doors."*
- L163–167 *"Well aware." / `⟨HELD⟩` / "The people responsible for the notice knew the notice did not stay put."*

Two flat institutional-knowledge statements inside twelve lines. The second no longer has a monopoly
on the moment.

### R5 — reveal the opposing case at full strength, then turn → **RESOLVED with a side effect**

The spoiler (*"That is the Court defending the practice it is about to hold inadequate."*) is gone.
The GL-70 passage is inserted at L267 immediately before the turn at L269. Both correct. Side effect at
§4-D and §4-E below.

### R6 — motif → **RESOLVED in the script, BROKEN downstream**

All seven states are present as `【】` and in order: L23 (1), L91 (2), L119 (3, on the reset beat),
L159 (4, immediately before the recognition), L197 (5), L297 (6), L361 (7), with the L351 callback to
state 1. Each sits on a beat that still exists — I checked each anchor line individually. **This part
of the second pass is genuinely good work.**

It does not survive contact with the image order. See §5 (R6/R11) and §8.

### R8 — no villain → **RESOLVED**

L242–243 deleted; *"ruled against them anyway"* replaced by L223 *"The judge wrote that down. Then he
ruled that the procedure was constitutionally sufficient…"*; *"kept posting them"* gone.

### R10 — no new fact in the ENDING → **RESOLVED for facts, one residue**

`seven or eight men` is gone from the script (L345 = *"a handful of men"*). *"The majority did not
weigh the servers' testimony…"* was moved to ACT_3 L171 as ordered. `and drove to the next address` was
moved out of narration into L355 `【the hand leaves frame; the walkway is empty】` as ordered.

Residue: L343 *"smaller than its **reputation**"* asserts a reputation the film never establishes, in
the last 72 seconds. Minor, but it is an unsupported assertion inside the 92 % window.

### R11 — the picture loop closes → **RESOLVED in the script, CONTRADICTED by the order**

L351 is now `【callback: motif 1 again — the paper taped flat, corners square. Same framing as HOOK.】`
The commissioned plate for that slot, `G209`, is written as *"The same door in full daylight, **entirely
bare with the tape gone too**, framed exactly as the first image of the film."* Those are opposite
images. See §8.

### R12 — three silences, each after the heavy line → **RESOLVED mechanically**

L165 after *"Well aware."*, L293 after the comparative-preference limit, L359 before the last image.
Count, order and side are all correct. The first is immediately undone by L167 (R2c).

### R13 — contradictions left as contradictions → **RESOLVED, with one the film still smooths**

All three ordered repairs landed: L185 adds the same deponent's exculpatory half with
*"The majority quoted the first half. The dissent quoted the second."*; L349 replaces *"described one"*
with *"did not describe it the same way as each other"*; L305 places *"The District Court had called the
same testimony undisputed."* directly after *scant and conflicting*. **This is the strongest section of
the second pass.**

Residual: the film restores the District Court's *"often removed **by other tenants**"* at L221 (F5-3)
having just spent ACT_3 quoting depositions that are **entirely about children**. The opinion carries
that mismatch; the film prints both halves and never notices it. §13 asks for the contradiction to be
shown, not merely both halves to appear 80 lines apart.

### R14 — the record's silences left silent → **PARTIALLY RESOLVED**

The Tuesday-morning paragraph and *"in the middle of a working day"* are gone; L123 now says
*"The record does not say what time of day the deputies came."* Correct.

**But L79 still says:** *"That is a conversation on a doorstep, **in daylight**, with a person who lives
there."* This is the identical daytime assumption that F4 removed twice, surviving 44 lines earlier in
the same act — and the film then explicitly contradicts itself at L123. Both instruments removed the
two instances they were pointed at and left the third. **NOT RESOLVED.**

### R15 — spoken form → **NOT RESOLVED**

`appellant` / `appellee` were removed from the narrator's prose (measured: 4 occurrences remain, all
inside quotations — L115, L193, L259, L283). The 11 state names moved to `【OST】` (L311, L313).
The docket number moved to `【OST】` (L243). *Weber* was restructured. Those are done.

Not done: the 81-word cluster of proper names at L245; the L125 quotation split, which produced an
ungrammatical sentence (§4-B); the 47-word restored Sixth Circuit sentence (§4-C); the 74-word statute
at L75 with no staging; and the two homophone families the review never listed. Full substitute
analysis at §6.

---

## 3. The fact_recheck's 7 open items and 3 flags, re-adjudicated

| # | Item | Verdict | Current text |
|---|---|---|---|
| OPEN-1 | *"three sentences long"* about a two-sentence statute | **RESOLVED** | L73: *"It is two sentences long and it is worth hearing in full…"* |
| OPEN-2 | *"four words long"* about a seven-word phrase | **RESOLVED** | L205: *"The Court's phrase for their position is thus without recourse in the state courts."* Arithmetic removed, as the packet's safer option advised. |
| OPEN-3 | *"like most States … weeks rather than months"* | **NOT RESOLVED — the repair broke the sentence.** | L51: *"Speed is the point of it. **Speed is the point of it,** and the Commonwealth built the procedure accordingly."* The unsourced clause was over-written by a copy of the preceding sentence and the trailing clause was left attached. The film now says the same five words twice in a row, and *"the Commonwealth built the procedure accordingly"* — the unsourced half of the original claim — is still spoken. See §4-A. |
| OPEN-4 | *"Reconstruction-era"* | **RESOLVED** | L207: *"under section 1983 — the statute that lets a citizen sue a state official for violating a constitutional right."* |
| OPEN-5 | *"that 1950 case about notifying beneficiaries of a trust"* (GL-R8) | **PARTIALLY RESOLVED — one unsourced characterisation swapped for another.** | L255: *"It came from that 1950 case, Mullane, **and it has governed notice ever since**…"* The trust description is gone; the packet quoted only the first half of the v002 sentence and repaired only that half. *"has governed notice ever since"* is (i) nowhere in *Greene*, (ii) a claim about law **as of today**, which ledger gate **G6** ("No claim about present-day law or practice") and Q-01 exist to stop. |
| OPEN-6 | *"establishes it"* — narrator's words inside the Sixth Circuit's quotation | **RESOLVED as to words, new defect as to punctuation.** | L231 restores the clause. Two commas were added that are not in the opinion, changing a restrictive content clause into a parenthetical. See §4-C. |
| OPEN-7 | *"the officer is back in the car"* | **RESOLVED** | L109: *"So step two evaporates, step three happens, and the visit is over."* |
| FLAG-1 | L107 attributes the Court's sentence to the sheriff's brief | **NOT RESOLVED** | L107 still reads *"And then the sentence that undoes it."* The three-word repair the packet specified was not applied. A listener still hears GL-20 (the Court, Part II-B) as the brief's next sentence. |
| FLAG-2 | *"Not a discovery made by the tenants' lawyers. Not something dragged out of a reluctant witness."* — both outside the record | **NOT RESOLVED** | Both sentences are intact at L157. |
| FLAG-3 | Brutscher's stumble smoothed | **NOT RESOLVED** | L175: *"I had been warned beforehand**,** by Mr. Bacon…"* RAW: *"I had been warned beforehand **that**, by Mr. Bacon…"* The word is still missing and a comma has been substituted for it. |

**Three of three flags unapplied**, against a packet that names them as required in the same batch and
against `feedback_no_wasted_cycles`.

---

## 4. Defects the repairs introduced or left behind

### 4-A · L51 — a duplicated sentence, in the fourth minute of the film **[NEW]**

> *"The proceeding was a forcible entry and detainer action — the summary process a landlord uses to get possession back quickly. **Speed is the point of it. Speed is the point of it,** and the Commonwealth built the procedure accordingly."*

v002 read *"Speed is the point of it. Kentucky, like most States, wanted these cases resolved in weeks
rather than months, and built the procedure accordingly."* The OPEN-3 fix pasted the preceding sentence
over the unsourced clause and did not remove the tail. Read aloud this is a stutter. It is also the
single most visible defect in the file and it survived into a script whose manifest says
`script_verified`.

### 4-B · L125 — the breath split left a dangling *not only* **[NEW]**

> *"…would, in many or perhaps most instances, constitute **not only** a constitutionally acceptable means of service. **But indeed —** a singularly appropriate and effective way of ensuring that a person who cannot conveniently be served personally is actually apprised of proceedings against him."*

The craft review's §R15(a) prescribed a different split that removed *not only*:
*"…would in many or perhaps most instances be a constitutionally acceptable means of service.
**And more than that.** A singularly appropriate and effective way…"* The implemented version keeps
*not only*, ends the sentence there, and opens the next with a fragment. Spoken, the listener hears
*"not only"* and waits for a *but* that never arrives inside the sentence. This is the R15 example the
standard itself uses (§10) run backwards: a correlative broken across a full stop.

Related, and pre-existing: L127 *"Singularly appropriate. Singularly effective."* The opinion wrote
*"a singularly appropriate and effective way"*. *"Singularly effective"* is a phrase the Court did not
write, delivered in the Court's voice. The craft review blessed it; it is still a coined quotation.

### 4-C · L231 — the restored Sixth Circuit sentence **[NEW punctuation deviation + R15]**

Opinion (Part I, quoting 649 F.2d at 428):
> *"The uncontradicted testimony by process servers themselves **that** posted summonses are not infrequently removed by persons other than those served **constitutes** effective confirmation…"*

Script L231:
> *"The uncontradicted testimony by process servers themselves**,** that posted summonses are not infrequently removed by persons other than those served**,** constitutes effective confirmation of the conclusion that notice by posting is not reasonably calculated to reach those who could easily be informed by other means at hand."*

Two commas the court did not write. In the opinion the *that*-clause states the **content** of the
testimony. Fenced by commas it reads and — more importantly — **sounds** parenthetical, so the sentence
a listener assembles is *"the uncontradicted testimony … constitutes effective confirmation,"* with the
substance of the testimony demoted to an aside. It is a 47-word sentence with 14 words between subject
and verb. This is the same class as F2 (punctuation instead of wording), one scale smaller, introduced
by the OPEN-6 repair and disclosed nowhere.

The passage also carries two narrator problems in the same breath: the sentence fragment
*"Its own decision, seventy years old, pointing the other way — and the court of appeals said the ground
underneath it had shifted."* (no main verb for the first clause), and the superlative
*"Its line is the sharpest sentence in the whole history of the case"*.

### 4-D · L131 vs L267 — GL-70 is now stated twice **[NEW, caused by the R5 fix]**

L131 (ACT_2, ~9 min): *"The rule underneath that instinct is old and the Court restated it approvingly:
it is reasonable to assume that a property owner will maintain superintendence of his property."*
L267 (ACT_5, ~21 min): the 104-word Mullane n.6 owner presumption, verbatim.

The craft review ordered the insertion at L267 and did not order the removal of L131. Both are now in
the film, 12 minutes apart, and the second is longer. That is not a plant-and-payoff; it is the same
argument delivered twice.

### 4-E · L267 — the insertion blurs where the quotation ends **[NEW]**

> *"The ways of an owner with tangible property, **it quoted**, are such that he usually arranges means to learn of any direct attack upon his possessory or proprietary rights. Entry upon real estate in the name of law may reasonably be expected to come promptly to the owner's attention. **Upon this understanding, a State may in turn conclude that in most cases, the secure posting of a notice on the property of a person is likely to offer that property owner sufficient warning…**"*

The first two sentences are *Mullane*, quoted inside *Greene* n.6. The third is **Brennan's own body
text**, after the footnote marker. The script signals the quotation with *"it quoted"* and never signals
that it ended. A listener hears 104 continuous words attributed to a 1950 case. This is exactly FLAG-1's
defect class, newly created by the fix for R5, in the film's most load-bearing passage.

### 4-F · L191–193 — the film misquotes the two words it holds up as proof of the Court's care **[NEW to both instruments]**

Opinion, Part I:
> *"Appellees **claim** never to have seen **these** posted summonses; they **state** that they did not learn of the **eviction** proceedings until they were served with writs of possession, executed after default judgments had been entered **against them**, and after their opportunity for appeal had lapsed."*

Script L191:
> *"They **claimed** never to have seen **the** posted summonses. They **stated** that they did not learn of the proceedings until they were served with writs of possession, executed after default judgments had been entered — and after their opportunity for appeal had lapsed."*

Script L193:
> *"**Claimed. Stated. Those are the Court's verbs, and the Court kept them.**"*

The Court's verbs are **claim** and **state**, present tense. The film converts both to the past, drops
*eviction* and *against them*, and then asserts in its own voice that it has preserved the Court's verbs.
The passage whose entire purpose is verb fidelity does not have the verbs right.

**This row also convicts the mechanical instrument.** `fact_recheck.v001.md` §4 row 26 records this line
as *"31 words · Q · **LOCKED** · confirmed verbatim against the clean copy after normalisation."* It is
not verbatim: the longest true run is 16 words, broken by the missing *eviction*, and a second run of 8
after the missing *against them*. A 6-word-minimum span matcher will happily report two adjacent regions
as one; the merge rule in §0 item 3 ("adjacent spans separated by ≤14 words were merged") is what made a
two-word deletion invisible. **The sweep can produce a false LOCKED, and did.**

### 4-G · L335 — the majority is made to answer something it was not answering **[NEW to both instruments]**

The script runs: dissent's institutional close (Ferguson v. Skrupa, L333) → *"The majority answered in
one line: the dissent misconstrues the constitutional standard."* (L335) → *"That is where the two
opinions stop talking to each other."* (L337)

In the opinion, *"The dissent misconstrues the constitutional standard"* sits in **n.9**, and n.9's own
first sentence says what it is answering: *"The dissent apparently wishes to dispute the District Court's
finding … and further questions our reliance on the observation in Mullane that the mails are a reliable
means of communication — in light of its own observation that 'unattended mailboxes are subject to
plunder.'"* It answers the **mailbox** passage, which the film places 18 lines earlier at L317. Attaching
it to the Ferguson close constructs an exchange the record does not contain. Nothing false is quoted;
the sequence is the film's.

### 4-H · the newly written HOOK breaks §16.5 and the motif order **[NEW]**

`【L25】`: *"HOOK cuts, about two seconds each — G001 · G002 · G003 · G004 · G005."*

1. **Five cuts.** §16.5 (owner decision, marked *"もう議論しない"*): *"HOOK は 3〜4カット・各約2秒"*.
2. **Five cuts × "about two seconds each" = ~10 s against a `(0:00–0:08)` label** and against the
   `hook_added` acceptance window. The narration is 24 words = 8.2 s. The direction and the header
   disagree by two seconds inside eight.
3. **Motif order.** FILM_BIBLE §3 fixes the seven states in order and makes the loop 1 → … → 1 so that
   the second viewing inverts. The HOOK plays, in eight seconds: G001 (state 1) → G002 (the hand on the
   corner) → G003 (*"the same door bare, two strips of tape and two torn corners"* = states 5+6) →
   G004 (*"one pale rectangle far down the line"* = **state 7**). The film's final image is spent before
   the first sentence ends.
4. Promise-payoff itself is fine — `EP62_greene_CODEX_BATCH_A.v002.md` §5 maps all five plates to body
   slots (G005 → ACT_3 `G076`). The count, the arithmetic and the state order are the failures.

### 4-I · the deleted Tuesday passage left no non-sequitur — but it did leave a contradiction

Checked directly. L121–123 reads cleanly: *"It is not the Court's estimate. The Court put it in
quotation marks and sent it to a footnote… The record does not say what time of day the deputies came.
It says only that in a good percentage of cases, nobody was there."* No dangling reference, no orphaned
pronoun, and the ACT_2 argument still lands. **The removal is clean.** The problem it exposes is L79's
surviving *"in daylight"* (R14 above), which the new sentence now flatly contradicts.

### 4-J · v003 silently dropped the structural locks v002 declared

v002's header declared: *"cold open ≤60s · no explanation block at 80–180s · re-hook ≤150s · mid reveal
45–60% · primary reveal 65–85% · **one reset beat 55–70%** · cold-open callback 70–90%"*. v003's header
declares only `forbidden_claims`, the process-server count, and no new fact after 92 %. The reset beat
(L119) sits at ~30 % of runtime — outside the window v002 declared and v003 stopped declaring. Dropping a
declared lock is not the same as satisfying it; if the lock was wrong, that belongs in a decision record.

---

## 5. R1–R15 re-run fresh against the current text

Old verdicts carried forward: none. Every row below was decided from the file on disk.

| # | Question | Verdict | Evidence |
|---|---|---|---|
| R1 | CONTROLLING IDEA sayable in one sentence | **PASS** | *"国家が「あなたに伝えた」と扱ってよいのは、その伝え方が実際に届いているときだけである"* — the film is entirely organised around it |
| R2 | That sentence is **not** in the script | **FAIL** | The literal sentence is gone (L343 stops at *"A method."*). But L349 speaks FILM_BIBLE §1's subtitle couplet — *"on the difference between what a procedure is written to do and what it was observed doing"* — and L167 states the recognition in plain assertion after the silence reserved for not stating it |
| R3 | Delete every narrator conclusion; does the audience still arrive? | **FAIL** | 16 sentences listed in §2/R3. L189, L227, L245 are the same self-referential move the review deleted at v002 L278 |
| R4 | Recognition in exactly one place | **FAIL** | L155–157 and L163–167 are two institutional-knowledge beats twelve lines apart. Removing the surplus `⟨HELD⟩` removed the marker, not the second recognition |
| R5 | Opposing case at maximum strength before the turn | **PASS** | L125–131 (*singularly appropriate*, *many or perhaps most*, the owner presumption) with the spoiler removed; GL-70 restated at L267 immediately before *"Then the turn."* at L269. The only PASS the second pass converted |
| R6 | Motif states nameable in order | **PASS (script) / FAIL (package)** | L23·91·119·159·197·297·361 + L351 callback, each on a live beat. But `【motif 7: an unfaded square where the paper was】` — the film's last image — **has no commissioned plate** (§8), and the HOOK plays state 7 at 0:06 (§4-H) |
| R7 | Irreproducible detail per major figure | **PASS** | *"Oh, we had plenty of trouble."* · *"probably a couple of times."* · Brutscher's *"the six months I was working at it"* · Village West · Weber 1909 · New York's next-day mailing · *"Usually a deputy. Never a name."* |
| R8 | No villain | **PASS** | L242–243 and *anyway* gone; L353 *"He did what the statute told him to do."* is the design |
| R9 | Stakes rise vertically | **PASS** | three doors (L89) → every door in the project (L211) → eleven States (L311) → the assumption (L357) |
| R10 | Zero new facts in the ENDING | **PASS with one residue** | `seven or eight men` gone; the study/survey/count sentences moved to L171. Residue: *"smaller than its reputation"* (L343) |
| R11 | ENDING returns to the first image | **FAIL** | The script says it does (L351). The plate commissioned for that slot, `G209`, is a **bare** door with the tape gone (§8). Script and order specify opposite pictures for the loop-closing frame |
| R12 | Three silences, positions nameable | **PASS** | L165 (after the recognition) · L293 (after the limit) · L359 (before the last image). Correct count, correct side. L165's effect is cancelled by L167, which is an R2 problem, not an R12 one |
| R13 | Contradictions left contradictory | **PASS with one residue** | L185, L305 and L349 all landed and are the best work in the pass. Residue: *"removed by other tenants"* (L221) never set against ACT_3's all-children testimony |
| R14 | Silences left silent | **FAIL** | The three-women silence is impeccable (L43, L193, L199, L295). But L79 *"in daylight"* survives F4 and is contradicted by L123 forty-four lines later; and FLAG-2's two record-free sentences remain at L157 |
| R15 | Read aloud | **FAIL** | Not performed, and cannot be claimed. Substitute analysis in §6 finds 11 sentences that will not survive a voice record, two of them ungrammatical when spoken |

**PASS 8 / FAIL 6 / (R6 and R11 split against the package).** The craft review's 12 FAILs became
6 FAILs. That is real progress and it is not the standard.

---

## 6. R15 — spoken-form analysis. **This is a substitute, not a read-aloud.**

Nobody has read this script aloud. §16 says *"R15は省略しない"* and the craft review said the same thing
about its own machine substitute. It is still true. What follows is everything a substitute can reach.

### 6.1 Long sentences with no internal comma — nowhere to breathe

| Line | Words | Sentence |
|---|---:|---|
| L229 | 30 | *"It is the same assumption the sheriff's side made and the same one the statute makes: that a step described as a last resort is in fact a last resort."* |
| L279 | 29 | *"The State's continued exclusive reliance on an ineffective means of service is not notice reasonably calculated to reach those who could easily be informed by other means at hand."* |
| L131 | 28 | *"The rule underneath that instinct is old and the Court restated it approvingly: it is reasonable to assume that a property owner will maintain superintendence of his property."* |
| L177 | 28 | *"Then his own account: and the six months I was working at it there was no occasion where I saw anyone tear the writs off of the door."* |
| L223 | 28 | *"Then he ruled that the procedure was constitutionally sufficient — on the ground that posting only comes into play after the officer cannot find the defendant on the premises."* |
| L289 | 28 | *"And it gave up more ground: even conceding that process served by mail is far from the ideal means of providing the notice the Due Process Clause requires."* |
| L311 | 28 | *"…at least 11 States authorizing notice in summary eviction proceedings solely by posting or by leaving the notice at the tenant's residence."* |
| L321 | 27 | *"Kentucky's forcible entry and detainer action is a summary proceeding for quickly determining whether or not a landlord has the right to immediate possession of leased premises."* |
| L125 | 26 | *"But indeed — a singularly appropriate and effective way of ensuring that a person who cannot conveniently be served personally is actually apprised of proceedings against him."* |
| L245 | 26 | *"A dispute about a thumbtack in Jefferson County had become a question about how a summary eviction begins in every State that served notice this way."* |
| L231 | 31 | *"Its line is the sharpest sentence in the whole history of the case: there may have been a time when posting provided a surer means of giving notice than did mailing."* |

### 6.2 The five longest sentences in the film

| Line | Words | Note |
|---|---:|---|
| **L75** | **74** | The statute, verbatim, in one unbroken run — *thereon … thereof … in a conspicuous place on the premises*. It must stay verbatim; it is given **no** staging, no `【】`, no held beat, no lead-in pause. The film's own next line (*"Read it slowly and it sounds careful"*) admits it needs help it was not given |
| L255 | 49 | Contains the unsourced *"and it has governed notice ever since"* (OPEN-5 residue) |
| L69 | 48 | Grannis + Mullane in one sentence with an em-dash pivot |
| L217 | 48 | *Weber* + Sixth Circuit + *section 454.030* + *seventy years* + the presumption clause |
| L231 | 47 | 14 words between subject and verb (§4-C) |

### 6.3 Stacked proper nouns

- **L245 — the worst in the film.** *"William Hoge … Robert Frederick Smith … David Madway … the National Housing Law Project … Lynn Cunningham … the Antioch School of Law …"* Four personal names and two institutions in 84 words, roughly 29 seconds, with no picture assigned and nothing for the ear to hold. This is the failure the review fixed for the eleven States by moving them to `【OST】` and did not fix here.
- **L151 / L181** — *Carter Bacon* and *Gilbert Brutscher* are introduced 30 lines apart and then set against each other; L175 requires the listener to hold *"warned … by Mr. Bacon, Carter Bacon"* while the speaker is Brutscher, who is not named until L181. The speaker of the quotation is identified **six lines after** the quotation ends.
- **L41 / L295** — *Linnie Lindsey, Barbara Hodgens and Pamela Ray* is correct and deliberate; **Barbara Hodgens / William Hoge** are close enough by ear to be worth checking in the voice record.

### 6.4 Numbers in a row

- **L241 + L243:** *"took the appeal in **1981**. It heard argument on the **twenty-third of February 1982**, and decided it that **May**."* Four date tokens across two sentences; the docket number is correctly on screen. This is the review's prescribed form and it is still four.
- **L311–313:** *"at least **11** States … It listed them in a footnote. **Eleven** States."* The same number twice in three sentences, once as a numeral and once as a word.
- **L75 / L79 / L315:** *"sixteen (16) years of age"* spoken three times across the film.
- **"section four five four point oh three oh"** is spoken **six** times (L73, L83, L217, L237, L269, L285). Every instance is nine syllables of digits.

### 6.5 Ambiguous by ear

| Term | Where | Problem |
|---|---|---|
| **appellants / appellees** | L115, L193, L259, L283 | Four survivors, all inside quotations, all unglossed. *appellants* = the sheriff's side; *appellees* = the tenants. L115 (*"we reject appellants' characterization"*) and L283 (*"in failing to afford appellees adequate notice"*) are the two places where mishearing reverses who won. The prose fix does not help a listener who cannot tell the quoted words apart |
| **writs / rights** | *writs* at L53, 143, 147, 175, 177, 185, 191; *rights* at L271 (*"their rights are before the courts"*), L267 (*"possessory or proprietary rights"*) | A near-homophone used ~9 times, and L267/L271 put both families inside 5 lines |
| **posting / postings / posted** | 24 occurrences | *"reliance on posting"*, *"posted notice"*, *"posted summonses"*, *"the posting"* — the ear cannot separate the gerund from the participle, and L237 (*"when notice is served by posting, a copy … within a day of the posting"*) has both in one sentence |
| **in rem / in personam** | L327 | **Handled correctly** — glossed one sentence earlier (*"against a person or against a thing"*). Noted as the model the other terms should follow |
| **forcible entry and detainer** | L51, 55, 89, 131, 321 | Five occurrences of a six-word term of art; L51 and L55 are eight lines apart |
| **thereon / thereof** | L75 | Both inside the 74-word statute, 20 words apart. Verbatim and therefore untouchable — which is an argument for staging the sentence, not for leaving it bare |
| **§ / section** | throughout | Correctly spelled out everywhere. **PASS** |

### 6.6 Sentences whose meaning depends on punctuation a listener cannot hear

1. **L125** — *"constitute not only a constitutionally acceptable means of service. But indeed — a singularly appropriate…"* The full stop reverses a correlative. Spoken, it is ungrammatical (§4-B).
2. **L231** — the two added commas turn the content of the testimony into an aside (§4-C).
3. **L109** — *"there is no household member standing behind the person who did not answer the door — because nobody answered the door."* The clause posits a person who did not answer, then denies any person answered. On the page the dash carries it; in the ear it is a contradiction.
4. **L51** — *"Speed is the point of it. Speed is the point of it, and…"* The repetition will be heard as a recording error and the voice record will be redone (§4-A).
5. **L231** — *"Its own decision, seventy years old, pointing the other way — and the court of appeals said…"* A subject with no verb, resolved only by the dash.

---

## 7. Adversarial pass — the three sentences a hostile viewer quotes

The question is not whether the film is anti-Kentucky. It is whether a hostile viewer could quote it
accurately and make the charge stick. Three sentences do the work.

**(1) L157 — *"The Housing Authority's own staff had told the men doing the posting that the papers came off the doors."***
This is the film's heaviest institutional accusation, spoken flatly in the narrator's own voice.
**Support:** GL-39 (n.7, App. 74) — one deponent, who prefaced it *"but we, **you know, assume —** the
Housing Authority told us…"* The film restores that hesitation four lines earlier (L153) and then
discards it in its own summary. The same deposition page, quoted by the dissent, ends *"So we never had
any problems with that"* — which the film also prints, sixteen lines later (L185), and never brings back
to bear on L157. **Verdict: partially supported.** The words exist; the flat assertion does not. This is
F3 reappearing four lines downstream of its own repair, and it is the strongest ammunition in the film.

**(2) L167 — *"The people responsible for the notice knew the notice did not stay put."***
**Support:** GL-43, the majority's *"As the process servers were well aware…"* But *"the people
responsible for the notice"* is broader than *"the process servers"* — it sweeps in the sheriff and the
Housing Authority. And the sentence is delivered as the film's own finding, immediately after the held
silence, twenty lines before the film discloses that the dissent calls that same testimony *"scant and
conflicting"* and that Brutscher saw nothing in six months. **Verdict: unsupported as stated.**
Q-07 quarantines exactly this move ("overstating the record is the exact charge the dissent makes"), and
this sentence is R2c's un-removed gloss. Removing it fixes R2, R4 and this charge at once.

**(3) L249 — *"Money got a person served. The apartment did not."***
**Support:** GL-72 — appellants conceded at oral argument that if past-due rent were sought,
*"personal service would be required by Kentucky law."* The eight words are accurate about the legal
asymmetry. What a hostile viewer quotes is the **framing** at L247: *"one more thing the sheriff's side
conceded, **because it shows how narrow the ground under them had become**"* — the narrator scoring the
point — followed by the couplet as the act's closing button. Together they assert a Kentucky that valued
money over homes. The record supports the asymmetry, not the preference. **Verdict: the sentence is
supported; its setting is not.** The craft review already deleted the harder version (v002 L243); this is
the same claim at lower volume with the narrator's thumb still on it.

**Runner-up, L59** — *"Every step of what follows was done by the State, to people the State was
housing."* Two lines after the film correctly separates *"a city housing authority, a county sheriff, and
the Commonwealth's own statute"* (L57), it collapses all three into "the State." The opinion does use
"the State" in the holding (GL-63), so this is defensible — but a hostile viewer will say the film merges
three different governments when it suits the sentence and separates them when it suits the sentence.

---

## 8. The package around the script — four defects that reach the render

The script is not the deliverable. These are in the files the script's `【】` directions and
`mandatory_stills` depend on, and none of them is fixed by editing the script.

**8-A · `EP62_greene_CODEX_BATCH_A.v002.md` still carries F1 verbatim.**
The ENDING beat block (line ~651) reads: *"答えは証拠の問題・ここでは**7〜8人の男**の巡回と、公社の一言"*.
That is `seven or eight men` — the craft review's **most important** factual error, ranked above every
craft failure, removed from the script and left standing in the document Codex reads. The same block
also still contains three sentences the review ordered replaced: *"登った男たちは**一段と言った**"*
(R13b), *"テープを押しつけ、**次の住所へ走った**"* (R10c) and *"【コールバック：**テープの角**】"* (R11).

**8-B · the loop-closing plate contradicts the loop-closing direction.**
Script L351: `【callback: motif 1 again — the paper taped flat, corners square. Same framing as HOOK.】`
Batch A `G209`: *"The same door in full daylight, **entirely bare with the tape gone too**, framed
exactly as the first image of the film."* One is a paper on a door; the other is a bare door. Batch A's
own note says *"`G209` は `G001` と同じ構図でなければなりません"* — the framing matches and the subject
is inverted. R11 cannot pass on both documents at once.

**8-C · the film's final image has no plate.**
`【motif 7: an unfaded square where the paper was】` (L361) is the last picture in the film. The ENDING
allocation is `G196`–`G209`; none of the fourteen prompts is an unfaded rectangle (`G208` = two strips of
tape on paint; `G209` = entirely bare, tape gone). `G225` was added for ACT_4 "time passing", not for
this. The craft review's closing item 9 — *"台本確定後、`mandatory_stills` を再導出する … R6 で七状態を
追加したので必ずずれる"* — was not done.

**8-D · the contract and the order disagree about how many stills exist.**
`episode_spec.v001.json` `mandatory_stills` contains **222** entries and is missing `G220`, `G221`,
`G222` (deliberately, per its own notes — thumbnails are packaging, not cuts). Batch A §7 line 858
states *"`mandatory_stills` は `G001`–`G225` の **225件**に更新済みです"*. Batch A §4's plate table is
also still derived from **v002's word counts** (HOOK 142 words, OP 51 words) and still labels its
sections with **v002's time windows** (`ACT_1 1:05–6:45` … `ENDING 28:20–30:00`) — the windows v003's own
header declares *"void"*.

---

## 9. What would have to change

**Must fix before a voice record (each is one sentence or less, except the last two).**

1. **L51** — delete the duplicated sentence and the unsourced tail: *"Speed is the point of it."* Stop.
2. **L167** — delete. R2, R4 and the §7(2) fairness charge close together. `Well aware.` + `⟨HELD⟩` then straight to L169.
3. **L255** — delete *"and it has governed notice ever since"* (present-day claim, gate G6).
4. **L79** — delete *", in daylight,"* (F4's third instance).
5. **L107** — apply FLAG-1: *"And then the Court's own sentence, the one that undoes it."*
6. **L157** — apply FLAG-2: delete both record-free sentences; the paragraph lands harder without them.
7. **L175** — apply FLAG-3: restore *that* — *"I had been warned beforehand that, by Mr. Bacon…"*
8. **L191** — restore the Court's tense and words: *"They **claim** never to have seen **these** posted summonses. They **state** that they did not learn of the **eviction** proceedings … had been entered **against them**, and after their opportunity for appeal had lapsed."* Otherwise L193 is false about its own quotation.
9. **L231** — remove the two added commas; end the attributed quotation at *"That time has passed."* and let the narrator's sentence carry the rest, or restore the clause with the opinion's punctuation. Delete *"Its line is the sharpest sentence in the whole history of the case"* and give the fragment a verb.
10. **L125** — apply the craft review's prescribed split (*"…be a constitutionally acceptable means of service. And more than that. A singularly appropriate…"*). The current split is ungrammatical aloud.
11. **L131 or L267** — pick one. GL-70 cannot be stated twice.
12. **L267** — mark where the quotation ends: *"…come promptly to the owner's attention. On that understanding, the Court went on, a State may conclude…"*
13. **L189, L227, L245** — delete the three self-referential framings. L245's names go to `【OST】`, as the eleven States did.
14. **L335** — either move the majority's answer to follow the mailbox passage it actually answers (after L319), or drop *"answered"* and present n.9 without the call-and-response.
15. **L25** — cut the HOOK to **four** plates and drop `G004` (state 7). Reconcile "about two seconds each" with the 0:00–0:08 label.
16. **The header** — re-derive the section windows from 5,239 words, or stop claiming they were derived.

**Must fix before the render, in the package, not the script.**

17. Rewrite the ENDING beat block in `EP62_greene_CODEX_BATCH_A.v002.md` (F1, R10c, R11, R13b still there).
18. Decide `G209`: paper-on-door (script L351) or bare door (current prompt). Commission the unfaded-square plate for L361 and add it to `mandatory_stills`.
19. Reconcile `mandatory_stills` 222 vs Batch A's claim of 225; re-derive after the `【】` set is final.
20. Re-derive Batch A §4's plate table from v003's measured counts; its section windows are v002's.

**Must fix in the process.**

21. Issue this as **v004** and re-run the `fact_recheck` §0 sweep against it, with the merge rule
    tightened so a two-word deletion inside a 31-word span cannot merge into a single LOCKED region
    (§4-F). Move `manifest.json` back off `script_verified` until the packet passes without open items.

---

## VERDICT

# DOES NOT MEET THE STANDARD

**R1–R15: PASS 8 / FAIL 6** (R2, R3, R4, R11, R14, R15), with R6 passing in the script and failing in the
package. The craft review's 12 FAILs are down to 6, and R5, R8, R9, R12 and R13 were genuinely repaired —
R13 in particular is now the best-argued section of any PD long-form script I have read. That is real work
and this review does not diminish it.

It is still not the standard, for three reasons that are not matters of taste:

1. **A sentence is duplicated in the fourth minute** (L51) and **a quotation is ungrammatical when
   spoken** (L125), in a file whose manifest says `script_verified`.
2. **The film misquotes the two words it holds up as proof of its own fidelity** (L191/L193) — and the
   mechanical instrument certified that passage LOCKED. The instrument has a demonstrated false-positive
   mode, so its 101 other LOCKEDs are now claims rather than measurements until the sweep is re-run with
   the merge rule tightened.
3. **Three of the three flags the verification packet said to apply "in the same batch" were not
   applied**, and the state was advanced past the gate anyway.

The defect-discovery curve has still not converged: this pass found **21** items, of which **9 are new to
all three instruments** (§4-A, 4-B, 4-C, 4-D, 4-E, 4-F, 4-G, 4-H, 8-A). Two of the nine — the L51 stutter
and the L245 name cluster — are the kind that a single read-aloud would have caught in ninety seconds.
**The next instrument should be a voice, not another document.**

**Searches that came back empty, so the reader can weigh what is above:**
`seven or eight` — 0 hits in v003 (F1 clean). `Reconstruction` — 0. `Postal Service` outside the dissent's
quotation — 0. `banned` — 0. `Normet` — 0. `Tuesday` / `night shift` / `second job` — 0. `Pannell` — 0 in
the spec. `appellant`/`appellee` in the narrator's prose — 0. Rhetorical questions in the narrator's voice
— 0. Emotion commands (*imagine*, *shockingly*, *we must*) — 0. National numbers — 0. Any claim about what
became of Linnie Lindsey, Barbara Hodgens or Pamela Ray — 0. The nine contract `forbidden_claims`
re-swept individually — **9/9 clear**, and the film's refusals at L43, L193, L199, L285 and L295 are the
reason this is a re-review and not a rejection.

---

*v001 · 2026-08-04 · adversarial re-review of `EP62_greene_script.en.v003.md` as of mtime 12:52, against `PD_SCREENPLAY_STANDARD.v001.md` §16, `EP62_greene_FILM_BIBLE.v001.md`, `EP62_greene_FACTS_LEDGER.v001.md` and the primary text in `measurements/EP62_greene_RAW.md`. Word counts, sentence statistics, `⟨HELD⟩` positions and the verbatim span sweep were computed from the file; every quotation above was read out of the file or the opinion it names. R15 was not performed and is not claimed.*
