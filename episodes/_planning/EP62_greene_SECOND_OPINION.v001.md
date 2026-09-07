# EP62 · GREENE v. LINDSEY — SECOND OPINION (independent factual read) v001

**Reviewer lens:** somebody who wants to catch the channel getting a fact wrong, with 456 U.S. 444 open.
**Ground truth:** `episodes/_planning/measurements/EP62_greene_RAW.md` (the opinion), not the ledger.
**Script read:** `episodes/_planning/EP62_greene_script.en.v003.md`.
**Out of scope by instruction:** craft, structure, rhythm, pacing. Facts and attribution only.
**Not duplicated here:** the four errors already found and repaired in v003 (the "whatever the proceeding
is called" fabrication, the "establishes it." fabrication, the three-sentence statute / four-word phrase
miscounts, the night-shift passage). Those are verified fixed and are not re-listed.

Every quotation in the script was normalised (curly quotes, em dashes, `*447`-style page markers
including ones glued mid-word — e.g. RAW `propri *452 etary` → `proprietary`, which the script gets
right) and compared token by token against both copies of the opinion in the RAW file.

Severity: **HARD** = the opinion contradicts it, or it is not in the opinion at all.
**SOFT** = a hedge dropped, a quotation silently truncated or reordered, or an inference in a fact's clothes.

---

## A. HARD — 16 findings

### A1 · ACT_2, line 107 — a sentence of the Court's put in the appellants' mouth
**Script:** "Now the sequence, **in the words of the brief filed for the sheriff.** First, the officer goes to the apartment… Finally, if no one answers the door, a copy of the notice is posted on the premises, usually the door. / **And then the sentence that undoes it.** If no one is at home at the time of that visit, as is apparently true in a good percentage of cases, posting follows forthwith."
**Opinion:** the three-step passage is Brief for Appellants 3, quoted in n.1 — correct. But "But if no one is at home at the time of that visit, as is apparently true in a 'good percentage' of cases, posting follows forthwith" is **Brennan writing in Part II-B at \*454**, immediately after "we reject appellants' characterization". It is the Court demolishing the brief, not the brief undoing itself. The brief never said it.
**Repair:** "And then the sentence the Court set against it. The Court wrote: *But if no one is at home…*"
**Why it matters:** this is the exact defect class the script keeps producing, and it is the single worst one left — the film's central rhetorical move ("the ladder had one rung") is built on a misattributed sentence.

### A2 · ACT_3, line 169 — the two phrases are in the opposite order
**Script:** "It wrote *not infrequently*, **and later**, *a significant number of instances*."
**Opinion (\*453):** "**In a significant number of instances**, reliance on posting … results in a failure to provide actual notice… Indeed, appellees claim… **As the process servers were well aware**, notices … were '**not infrequently**' removed…" — "significant number of instances" comes **first**.
**Repair:** "It wrote *a significant number of instances*, and then, quoting nobody's count, *not infrequently*."

### A3 · ACT_3, line 169 — "There is no count anywhere in this opinion"
**Script:** "There is no count anywhere in this opinion, because nobody had counted."
**Opinion:** contains counts throughout — "at least 11 States", "at least 10 other States", "sixteen (16) years of age", "some 70 years earlier", "the six months I was working at it", "probably a couple of times". Separately, **"because nobody had counted" is ABSENT** — the opinion nowhere says whether anyone counted removals; the film cannot know that.
**Repair:** "The opinion never prints a rate of removal. Nobody put one in front of the Court."

### A4 · ACT_3, line 181 — "same doors"
**Script:** "That man was Gilbert Brutscher, and the dissent set his answer directly against Bacon's. **Same job, same doors,** opposite answers."
**Opinion:** ABSENT. Bacon is placed at Village West (dissent, App. 80). Brutscher's six months are given **no location at all**. The opinion never says the two worked the same buildings.
**Repair:** "Same job, opposite answers. The dissent does not say they worked the same buildings."

### A5 · ACT_3, line 187 — "different buildings, over different years"
**Script:** "a handful of men, describing a practice they had each seen differently, **in different buildings, over different years**."
**Opinion:** ABSENT. No deponent's building is given except Village West (twice, and by two servers who agreed), and **no dates or years are given for any deponent's service** other than Brutscher's "six months".
**Repair:** "…describing a practice they had each seen differently. The opinion does not say where or when each of them worked."

### A6 · ACT_1, line 43 — "a shared address"
**Script:** "Three names and **a shared address**."
**Opinion:** "Appellees Linnie Lindsey, Barbara Hodgens, and Pamela Ray are tenants in a Louisville, Ky., housing project." Three tenants, three apartments, three doors — the script itself says "**Three doors**" 46 lines later (line 89) and "three particular apartments" (line 199). They shared a project, not an address.
**Repair:** "Three names and a housing project."

### A7 · ACT_4, line 205 — "the system that had taken the apartments"
**Script:** "In the system that **had taken the apartments**, there was no door left to knock on."
**Contract, `forbidden_claims` row 5:** "'They lost their homes' / any account of what happened to Linnie Lindsey, Barbara Hodgens or Pamela Ray afterwards. The opinion does not say." The opinion says default judgments were entered and writs of possession served — and even that sits inside "**they state that**". It never says an apartment was taken from anyone.
**Repair:** "In the state courts, there was no door left to knock on."

### A8 · ACT_5, line 255 — "it has governed notice ever since"
**Script:** "It came from that 1950 case, Mullane, and **it has governed notice ever since**."
**Contract, `forbidden_claims` row 1 / ledger G6:** no claim about present-day law. The opinion is from 17 May 1982 and establishes nothing about the forty-four years since.
**Repair:** "It came from that 1950 case, Mullane, and it was already thirty-two years old when Brennan reached for it."

### A9 · ACT_4, lines 215 and 245 — "the sheriff and the officials"
**Script (215):** "the District Court granted judgment for **the sheriff and the officials**". **Script (245):** "William Hoge argued for **the sheriff and the officials**."
**Opinion, Part I:** "**Appellants are the Sheriff of Jefferson County, Ky., and certain unnamed Deputy Sheriffs** charged with responsibility for serving process." The Housing Authority and the public officials were named as **defendants below** but are not the appellants; judgment was "for appellants" and Hoge "argued the cause and filed a brief for appellants."
**Repair:** "for the sheriff and his deputies" in both places.

### A10 · ACT_5, line 325 — "the sentence that decides the case"
**Script:** "The majority answered that directly, and **its answer is the sentence that decides the case**. From the perspective of the tenant, it wrote, it is difficult to see how a means of serving process that fails to afford actual notice in a not insubstantial number of cases can be deemed either prompt or certain."
**Opinion:** the quotation itself is now correct (verified word for word against n.4). But it is **footnote 4**, a reply to the dissent's "prompt and certain" argument. The sentence that decides the case is Part III: "We conclude that in failing to afford appellees adequate notice… the State has deprived them of property without the due process of law required by the Fourteenth Amendment." A film that tells the audience a footnote is the holding has got the opinion's architecture wrong.
**Repair:** "The majority answered in a footnote, and the answer is the tightest sentence in the opinion."

### A11 · ACT_5, line 267 — a footnote quotation of Mullane spliced onto the Court's own body text
**Script:** "The ways of an owner with tangible property, **it quoted**, are such that he usually arranges means to learn of any direct attack upon his possessory or proprietary rights. Entry upon real estate in the name of law may reasonably be expected to come promptly to the owner's attention. **Upon this understanding, a State may in turn conclude that in most cases, the secure posting of a notice** on the property of a person is likely to offer that property owner sufficient warning…"
**Opinion:** the first two sentences are **footnote 6**, quoting *Mullane* at 316. "Upon this understanding, a State may in turn conclude…" is **body text at \*452**, and in the opinion "this understanding" refers back to the body's own preceding sentence ("The frequent restatement of this rule impresses upon the property owner…"), not to the footnote. The script fuses a footnote quotation of a 1950 case and a 1982 body sentence into one continuous-sounding utterance, and silently re-points "this understanding".
**Repair:** close the Mullane quotation explicitly ("that is Mullane, quoted in a footnote"), then restart: "On that understanding, Brennan wrote in the body of the opinion, a State may conclude…"

### A12 · ACT_1, line 79 — "in daylight"
**Script:** "That is a conversation on a doorstep, **in daylight**, with a person who lives there."
**Opinion:** ABSENT — and the script contradicts itself at line 123: "**The record does not say what time of day the deputies came.**" Nothing in the statute, the brief or any deposition mentions daylight.
**Repair:** "That is a conversation on a doorstep, with a person who lives there."

### A13 · ACT_1, line 55 — "The deputies are named … not at all"
**Script:** "The deputies are named the way the record names them, **which is to say not at all**. … Usually a deputy. **Never a name.**"
**Opinion:** the dissent names two of the men who served process — "**Mr. S. Carter Bacon**" and "**Mr. Gilbert Brutscher**" — and the script itself supplies both names later (lines 151 and 181). The caption's phrase is "certain **known and** unknown Deputy Sheriffs", which also concedes that some were known.
**Repair:** "The deputy sheriffs are unnamed in the caption of the case. Two of the men who did the work get their names back later, and only in the dissent."

### A14 · ACT_3, line 157 — "Not a discovery made by the tenants' lawyers"
**Script:** "**Not a discovery made by the tenants' lawyers.** Not something dragged out of a reluctant witness. The Housing Authority's own staff had told the men doing the posting that the papers came off the doors."
**Opinion, n.7:** "**The depositions before the District Court** included the following statements by the process servers." A deposition taken in this litigation is precisely a discovery made by the tenants' lawyers — it is a lawyer's question that produced the answer. The claim is backwards.
**Repair:** "It came out of a deposition, from the men themselves — the Housing Authority's own staff had told the men doing the posting that the papers came off the doors."

### A15 · ACT_5, lines 333–335 — the majority's one-line reply is attached to the wrong charge
**Script:** the dissent's institutional close (Ferguson) and the lipservice charge, then "**The majority answered in one line:** the dissent misconstrues the constitutional standard."
**Opinion, n.9:** "The dissent apparently wishes to dispute the District Court's finding that 'notices posted on apartment doors are often removed,' and further questions our reliance on the observation in Mullane that the mails are a reliable means of communication — in light of its own observation that 'unattended mailboxes are subject to plunder.' Post, at 460. **The dissent misconstrues the constitutional standard.**" It answers the *undisputed-finding* and *mailbox* points, not the institutional objection — which the majority never answers at all.
**Repair:** move the line to follow the mailbox passage (after script line 317/319), where the opinion puts it.

### A16 · HOOK line 21 / ENDING line 353 — the tape is the film's central image and is not established
**Script (HOOK):** "Kentucky said a paper **taped** to a door was service. The men who **taped** it up…" **Script (ENDING):** "a deputy **pressed a strip of tape** onto a painted door."
**Opinion, n.1:** "'Posting' refers to the practice of placing the writ on the property **by use of a thumbtack, adhesive tape, or other means.**" The opinion never says which was used on Lindsey's, Hodgens' or Ray's doors. Nothing says the doors were painted. Under invariant 11 / Q-12 the film may not present an invented reconstruction as the record.
**Repair:** HOOK — "Kentucky said a paper fixed to a door was service. The men who put it there…"; ENDING — "a deputy fixed a writ to a door — by thumbtack, or tape, or other means; the opinion does not say which." (The `【】` motif can stay tape; the *narration* must not assert it.)

---

## B. SOFT — 29 findings

**Hedges dropped and quotations silently cut**

| # | Line | Script | Opinion | Repair |
|---|---|---|---|---|
| B1 | 255 | "…to apprise interested parties of the pendency of the action." | "…of the pendency of the action **and afford them an opportunity to present their objections.**" (\*450, emphasis in original) | Restore the second half — it is the half this film is about. |
| B2 | 275 | "**Where** the subject matter of the action also happens to be the mailing address…" | "**Particularly where** the subject matter…" (\*455) | Restore "Particularly" — without it an illustration becomes a rule. |
| B3 | 275 | "…would surely go a long way toward providing the constitutionally required assurance." (delivered as a whole sentence) | continues: "…**assurance that the State has not allowed its power to be invoked against a person who has had no opportunity to present a defense despite a continuing interest in the resolution of the controversy.**" | Mark the cut or restore it. |
| B4 | 115 | "we reject appellants' characterization of the procedure." | "…**of the procedure contemplated by § 454.030 as one in which 'posting' is used as a method of service only as a last resort.**" | Quote to the end of the object; it is the whole point. |
| B5 | 123 | "It says only that in a good percentage of cases, nobody was there." | "as is **apparently** true in a 'good percentage' of cases" | Keep "apparently" — the Court hedged its own inference. |
| B6 | 311 | "**Eleven States.**" | "the **at least 11** States" | "At least eleven." |
| B7 | 231 | "The uncontradicted testimony by process servers themselves**,** that posted summonses are not infrequently removed by persons other than those served**,** constitutes…" | no commas in 649 F.2d at 428 as quoted | Drop the commas — they turn a restrictive clause into a blanket claim that *all* process-server testimony was uncontradicted. |
| B8 | 185 | "**They** always put the writs up high — so we never had any problems with that." | dissent: "the process servers '**always put [the writs] up high. So we never had any problems with that.**'" — the deponent's word is *we* | "We always put them up high. So we never had any problems with that." |
| B9 | 317 | "**Posting, at least, gives assurance** that the notice has gotten as far as the tenant's door." | "Moreover, unlike the use of the mails, **posting notice at least gives assurance** that the notice has gotten as far as the tenant's door." | Restore the word order inside the quotation. |
| B10 | 303 | "the Court confidently overturns the work of the Kentucky Legislature." | "…**and, by implication, that of at least 10 other States.**" | Optional, but the cut clause is what makes the eleven-States beat land eight lines later. |

**Inference wearing a fact's clothes**

| # | Line | Script | Opinion | Repair |
|---|---|---|---|---|
| B11 | 45, 89, 199 | "these three **women**", "For all three **women**" | ABSENT — the opinion gives three names and never states their sex; no pronoun is ever used for them | "these three tenants" / "all three". |
| B12 | 143–153 | "**One of them**… **A second server**… **A third** described…" | n.7 prints excerpts from App. 74, App. 80 and App. 82 and never says how many deponents they represent. The dissent establishes only that App. 74 ≠ App. 80 (Bacon) | "One deposition… another… a third excerpt in the same footnote…" — keep the count off the men. (The film's own lock forbids counting process servers; this is that lock leaking.) |
| B13 | 47 | "An officer went to an apartment door in Louisville and **knocked. Nobody answered.** He took a piece of paper and fixed it to the outside of the door." | ABSENT for these three. The opinion says only "In each instance, notice took the form of posting a copy of the writ … on the door of the tenant's apartment." What a visit looked like comes from the *brief's* general description | Frame as the procedure: "Under the procedure, an officer went to the door. If nobody answered…" |
| B14 | 49 | "when **officers arrived with** an order to take the apartment back" | "until **they were served with writs of possession**" — passive, no actor named | "…when the writs of possession were served." |
| B15 | 77, 85 | "Failing that, **put it on the door**" (as the statute's third step) | statute: "by posting a copy thereof **in a conspicuous place on the premises**" — the statute never says *door*; the door is what the practice did | "Failing that, post it somewhere conspicuous on the premises. In practice, the door." |
| B16 | 79 | "The statute even **tells the officer to** explain it" | "he **may** explain and leave a copy" — permissive. Only the *dissent* glosses it as "the statute **directs** the server to explain" | "The statute even lets the officer explain it" — or attribute the stronger reading to the dissent. |
| B17 | 79 | "it tells you **what the legislature pictured**… Somebody old enough to understand a court paper and to pass it on" | ABSENT — the opinion says nothing about legislative intent behind the family-member step | "Look at the middle step, because of what it assumes." |
| B18 | 77 | "find **an adult** in the household" | "any member of the defendant's family thereon **over sixteen (16) years of age**" — sixteen is not an adult, and the film's own point rests on that | "find a family member over sixteen". |
| B19 | 113 | "at whatever hour **the route** happened to reach that door" | ABSENT — no routes, schedules or rounds anywhere in the opinion | "at whatever hour the one visit happened to fall". |
| B20 | 123, 295, 171 | "**The record** does not say…", "**The record** simply stops", "There was nothing else to weigh it against" | These are claims about the *whole record* (App. 41–113, the CA6 appendix, the oral argument). The film has read the **opinion** | "The opinion does not print…", "the opinion stops", "nothing else in the opinion". |
| B21 | 65 | "A day off work, or a shift swapped, or **a child minded**." | ABSENT — nothing in the opinion about any tenant's job, hours or children. This is the surviving residue of the removed night-shift passage, in a softer register | Keep it explicitly hypothetical ("whatever a person has to arrange") or cut. |
| B22 | 167 | "The people responsible for the notice knew **the notice did not stay put**." | "were '**not infrequently**' removed **by children or other tenants**" — Q-07 forbids upgrading this to a general disappearance | "…knew the notice did not always stay put." |
| B23 | 93, 109, 123, 353 | "a **deputy** walked up to a door", "**The deputy** knocks", "what time of day **the deputies** came", "a **deputy** pressed a strip of tape" | The opinion calls the deponents "**process servers**" throughout; the brief says the officer is "**usually** a Jefferson County Deputy Sheriff" — the script quotes that "usually" at line 55 and then drops it | Use "process server" where the opinion does. |
| B24 | 59 | "the **city's own** housing authority" | "the Housing Authority of Louisville" — the opinion never states its municipal relationship | "Louisville's housing authority". |
| B25 | 211 | "it was inadequate on **every door in the project, and on every door in every project** served the same way" | The Court held the opposite of a sweeping rule: "we hold **only** that posted notice pursuant to § 454.030 is constitutionally inadequate" (n.9) | Mark it as the class action's theory, not the outcome: "that was the theory of the class." |
| B26 | 235 | "the arithmetic that constitutional cases **usually** avoid" | narrator's generalisation about constitutional litigation; nothing in the opinion supports it | Cut "usually", or cut the clause. |
| B27 | 245 | "**The people in the room** are worth naming" | Madway and Cunningham **filed briefs** as amici; the caption does not put them in the courtroom | "The people on the papers are worth naming." |

**Attribution boundaries — quoted authority delivered as the Court's own voice**

| # | Line | Script | Opinion | Repair |
|---|---|---|---|---|
| B28 | 263 | "**A procedure's effect must be judged in the light of its practical application to the affairs of men as they are ordinarily conducted.**" — delivered as the Court's test | The Court is quoting ***North Laramie Land Co. v. Hoffman*, 268 U.S. 276, 283 (1925)**. The script names *Grannis* (1914) and *Mullane* (1950) elsewhere but not this one | "…borrowing a line from a 1925 case: *its effect must be judged…*" |
| B29 | 271, 275, 279 | "a **reliable means of acquainting interested parties** of the fact that their rights are before the courts"; "the mails, **it wrote**, provide an **efficient and inexpensive means of communication**"; "not notice **reasonably calculated to reach those who could easily be informed by other means at hand**" | All three are ***Mullane*** at 315, 319 and 319, in quotation marks in the opinion. "it wrote" in the middle one is wrong — the Court quoted it | One clause fixes all three: "quoting Mullane again…". |

**Sequencing claims about the opinions (low, but checkable)**

- **line 115** — the script puts "we reject appellants' characterization" *after* "posting follows forthwith" and "Neither the statute…". The opinion's order is the reverse: reject → "To be sure, the statute requires…" → "But if no one is at home… forthwith" → "Neither the statute…". The script's "So when the Court came to that account… it wrote" asserts a sequence that is not the opinion's. Repair: drop the temporal framing.
- **line 333** — "**It went further**, and accused the majority of…" places dissent n.2 after the *Ferguson* close. Dissent n.2 hangs off the mails passage at \*459–460, **before** the close. Repair: "Earlier, in a footnote, it had already accused…".
- **line 41** — "The Court's opinion **names them once**" is true of the body (verified: the sentence appears once per copy of the opinion), but "Lindsey" also stands in the caption. Defensible; noted only so nobody is surprised by it.
- **line 73** — "It is two sentences long and it is worth hearing **in full**", followed by the first sentence only; the second arrives 10 lines later as "There is one more sentence". The two-sentence count is now correct; "in full" is not.

---

## Not my lane, but it is a defect not a taste call

**ACT_1 line 51** prints the same sentence twice: "Speed is the point of it. **Speed is the point of it,** and the Commonwealth built the procedure accordingly." That is a paste artefact, not a rhetorical repeat — the second instance runs into a different clause.

---

## What is clean

Recorded so the next reviewer does not re-litigate it. Verified word for word against the RAW file:
the question presented (61) · § 454.030 first sentence (75) and second sentence (83) · the n.1 posting
definition (99) · the n.1 three-step brief passage (105) · "Neither the statute, nor the practice…" (111)
· the property-superintendence line (131) · all three majority deposition excerpts, App. 74 / 80 / 82
(143–153) · "As the process servers were well aware…" (161) · the Brutscher passage (175–177) · the
"up above where … a small child can't reach it" passage (183) · the appellees' claim/state sentence (191)
and "claim to have suffered" (193) · "thus without recourse" (205) · the *Weber* passage (217) · the
District Court's "conditions have changed" quotation (221) · the Sixth Circuit passage (231, wording
correct — only the added commas are at issue) · the n.2 cost and New York passages (235, 237) · the
argued/decided dates and No. 81-341 (241, 243) · all four names in the caption block (245) · the
past-due-rent concession (247) · "significant interest in property" (259) · "But whatever the efficacy…"
(269) · "cannot be considered a reliable means…" (271) · "Failure to effect personal service on the
first visit…" (273) · "continued exclusive reliance" (279) · the Part III holding (283) · all three n.9
limits (285, 289, 291) · the dissent's opening (301), its "sole ground" charge (303), its "not a single
case" charge (307), its "at least 11 States" (311, and the footnote does list exactly eleven — Ala.,
Colo., Fla., Kan., Ky., La., Miss., Neb., N.H., N.C., W.Va.), its summary-proceeding definition and the
*Lindsey v. Normet* block (321), "prompt and certain" (323), the n.4 reply (325, wording), the in
rem / in personam refusal (327), the *Ferguson* close and the lipservice charge (333), and "The dissent
misconstrues the constitutional standard" (335, wording).

The script also correctly avoids every `forbidden_claims` row except A7 and A8: it never says the
tenants won, never gives a vote tally, never confuses *Lindsey v. Normet* with Linnie Lindsey, never
reaches for the private-landlord frame, never states "she never saw the notice" as a finding, and says
outright that the Court did not ban posting and did not order the mail.

---

## COUNT

**45 factual or attribution findings: 16 HARD, 29 SOFT.** (Plus one duplicated sentence noted above.)

**Would I sign this off as factually sound? No** — not while a sentence Brennan wrote to demolish the
appellants' brief is delivered to the audience as the brief's own words (A1), a footnote reply is
announced as the sentence that decides the case (A10), and three details that appear nowhere in the
opinion — "same doors", "different buildings, over different years", "in daylight" — are spoken as
record.
