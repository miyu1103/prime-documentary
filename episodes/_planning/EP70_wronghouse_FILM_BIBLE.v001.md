# EP70 · THE WRONG HOUSE — FILM BIBLE v001

**Episode `PD-2026-070-wronghouse` · slug `wronghouse` · topic `TOP-20260812-001` · written 2026-08-12**
**Machine contract:** `episodes/PD-2026-070-wronghouse/episode_spec.v001.json` — 45:00, 2445–2835 s,
6,900–7,500 words, nine sections, 160 plates, 300 distinct video assets, 209 forbidden subjects,
22 forbidden claims.
**Facts:** `EP70_wronghouse_FACTS_LEDGER.v001.md` (94/94 quotations re-locate by exact string search).
**Producibility:** `measurements/EP71_WRONGHOUSE_REGISTER_INVENTORY.v001.json` — **the `EP71_` prefix on
that file and on its generator is deliberate and is not a mistake.** The measurement was signed under the
episode's pre-renumber id and keeps its name so the numbers stay traceable to the run that produced them
(`EP70_wronghouse_IDENTITY_NOTE.v001.md`). Everything else in this episode is `EP70_`.
**Judged by:** `docs/PD_EDITORIAL_DIRECTION.v002.md` and `config/pd_planning_os.v002.json` (score 110, FLAGSHIP).
**Built to:** `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`.

**This document carries intent, tone and direction. It reads no numbers into any tool. Every number a
tool needs is in `episode_spec.v001.json`, and where the two appear to disagree, the spec is right and
this file is wrong.**

---

## 1. The contradiction, in one sentence

> **They were the wrong house, the government admitted it within five minutes, and for eight and a half
> years its legal answer has been that nobody can be held responsible — because deciding whether to look
> at the number on the mailbox was a policy judgement.**

That sentence is the film. Everything else is evidence for it.

## 2. What this episode is *about*, which is not the same thing

It is not about the FBI. It is not about a raid. It is about **the space between a wrong that everyone
agrees happened and a remedy that nobody can reach** — and about the fact that Congress built the bridge
across that space in 1974, specifically and explicitly for this exact situation, and the bridge did not
hold.

`S01 THE HIDDEN RULE` is the series slot; `S30 WHY NOBODY FIXED IT` is the engine inside it.
Assigned role (v002 §8): **acquisition**, with a conversion tail. It is judged on new viewers and on
30-second retention, not on watch-time alone.

## 3. Who the film is for, and the one promise it makes

PD's measured audience is 92.5% male and 77% aged 55+. This premise needs none of that: the point of
contact is the viewer's own front door at four in the morning, and there is no demographic that does not
have one. **The promise made in the first twenty-two seconds is: *you are about to find out what happens
if they come to your house by mistake.*** The promise is paid in ACT_3 and again in ACT_6 — and the honest
answer, in 2026, is *nothing has happened yet*, which is worse than a bad answer and is the reason the
film exists.

## 4. Tone

A storyteller who knows something you don't. Never a professor, never an advocate, never angry.
The film's own voice is **flat, exact and unhurried**, and it lets the documents be loud. Where the
record contains two versions, the film says so and slows down rather than picking one.

**The system states its own reason before its failure is shown, every time.** The discretionary-function
exception exists so that courts do not second-guess policy through tort suits — that is a real and
defensible idea, and it is said properly, in the government's own words, before the film shows what it
did here. The friction between the two is the brand (`v002 §9`). A film that only quotes Justice
Sotomayor is an advocacy film and will not be made here; the majority's answer to the family's best
argument — *legislative history is not the law* — is spoken in ACT_4, at full strength, and is not
rebutted.

## 5. Structure — six acts, and the length is carried by the aftermath

The raid is **five minutes long**. The film is forty-five. That ratio is the thesis: an incident-weighted
film would run twelve minutes and be forgotten; this one is a film about *what happens next*, which is the
only thing anyone in the audience will ever actually experience.

| § | heading in the script | minutes | words | plates | what carries it |
|---|---|--:|--:|--:|---|
| HOOK | 5:00 a.m. | 0:31 | 83 | 8 | one woman, one room, one thing she does not know |
| OP | brand band | 0:05 | 14 | 2 | `BrandOpening`, imported not forked, after the hook |
| ACT_1 | **The five minutes** | 6:31 | 1,059 | 25 | the raid, told twice, because the record tells it twice |
| ACT_2 | **The reason** | 6:55 | 1,123 | 23 | Operation Red Tape, the Camaro, the mailbox, the GPS in the bin, and the four things that did not fit |
| ACT_3 | **The paperwork years** | 8:10 | 1,327 | 28 | claim → suit → discovery → **they win two counts** → mediation fails → *Kordash* → everything gone |
| ACT_4 | **Collinsville, April 1973** | 5:19 | 863 | 23 | private bills, the Giglottos, the Askews, the Senate committee, the 1974 proviso — and the majority's answer to it |
| ACT_5 | **The argument** *(§ ACT_5)* | 7:14 | 1,175 | 24 | 29 April 2025; THE MOMENT; a unanimous Court; and what it did *not* decide |
| ACT_5 | **And still no trial** *(`### ACT_5 · PART TWO`)* | 5:13 | 847 | 18 | Courtroom 339; THE SYSTEM MAP; THE HIDDEN RULE |
| ENDING | | 2:32 | 412 | 9 | preparedness, and an ask that is a card and not a sentence |
| | | **42:32 speech + 0:09 endcard = 42:41** | **6,903** | **160** | |

**Eight sections, six movements, and the reason they are not the same number.**
`gen_narration_case.section_for_heading` — the extractor the paid narration run is built from — knows
`HOOK / OP / ACT_1…ACT_5 / ENDING` and nothing else, and `extract_events` **drops prose under an unmapped
heading**. The first draft of this script headed its final movement `## ACT_6`, and **847 words, the whole
of the last movement, vanished from the count.** It was caught by *running* the extractor, not by reading
it. The sixth movement is therefore headed `### ACT_5 · PART TWO`, maps to `ACT_5`, and the extractor now
returns **0 orphans and eight non-empty sections**. `section_vocabulary` in the spec is eight entries, and
`figure_beats_per_act` runs to 26 rather than 18 because `ACT_5` is now a double-length act.

**Word counts above are the extractor's, not a word processor's.** `check_script_length` reads 7,203 for
the same file because its own counter does not strip HTML citation comments or blockquoted front matter;
both gates are green and the difference is furniture, not narration.

**Plate derivation, and it is arithmetic rather than taste.** One commissioned plate per **48 narration
words**, section by section, rounded, with a floor of **8** for the HOOK and **2** for the OP because those
two sections cut far faster than the film's average:

```
HOOK      83 /48 -> 2   floor 8   ->  8
OP        14 /48 -> 0   floor 2   ->  2
ACT_1  1,059 /48 -> 22            -> 22
ACT_2  1,123 /48 -> 23            -> 23
ACT_3  1,327 /48 -> 28            -> 28
ACT_4    863 /48 -> 18            -> 18
ACT_5  1,175 /48 -> 24            -> 24
ACT_5b   847 /48 -> 18            -> 18
ENDING   412 /48 ->  9            ->  9
                                    152
```

**Eight are then added for supply, not for style, and both additions are named in §9:**
**ACT_4 +5** (the April 1973 register returns at most three usable archival clips on the entire shelf and
not one of them is an American street, house, car or hearing room) and **ACT_1 +3** (the 5 a.m. breach
returns exactly one usable modern clip). **Total 160**, which is the number in the spec's
`mandatory_stills` and in the Codex order, and it fits under the still ceiling of 186 cuts at the SHORT
edge of the runtime band.

### The turn in each act

Every act ends on a door opening onto a worse room. This is the retention spine (spec v2 row 16) and it
is designed, not hoped for.

- **ACT_1 →** the agents realise, apologise, leave a business card, and go and do the raid properly three
  houses away. *The viewer assumes this is the beginning of a straightforward compensation story.*
- **ACT_2 →** there was no rule requiring any of it. Not the site survey, not the GPS, not the street sign,
  not the wait. *So there was no rule to break.*
- **ACT_3 →** they win. And then, fifteen weeks later, on a case decided a month after their win, they lose
  everything. **This is the strongest turn in the film and it is factually true.**
- **ACT_4 →** Congress already fixed this. In 1974. On purpose. Because of two houses in Illinois.
- **ACT_5 →** nine justices, no dissents, and the family still has not been inside a courtroom for a trial.
- **ACT_6 →** the case goes back to the same court that dismissed it, and as of today nobody has ruled.

### Answer Reversal (v002 §8 — now a script gate)

The viewer is deliberately allowed to form, and then lose, three wrong answers:

1. *"Obviously they were compensated."* → taken away in ACT_2 (there is no rule) and ACT_3 (Counts III–VI go
   in September 2022).
2. *"Well, they won in September — so it ended fine."* → taken away on 30 December 2022.
3. *"The Supreme Court ruled for them unanimously, so it's over."* → taken away in ACT_5's last minute and
   in ACT_6. **The Court answered two questions and neither of them was whether this family gets a trial.**

The real answer, landed in ACT_6: *the case is still going, and the rule that decides it has never been
settled by anyone.*

### THE MOMENT (one per episode)

**ACT_5, at 29 April 2025.** All music stops. One card, one timestamp, and the words as they were said in
the room:

> **JUSTICE GORSUCH:** *"Yeah, you might look at the address of the house before you knock down the door."*
>
> **MR. LIU:** *"— number at the end of the driveway means exposing the agents to potential lines of fire
> from the windows."*

Then five seconds of nothing before the bed returns. **This is the only place in the film where the
government's position is stated in its own voice at full length, and it must not be cut short to make it
sound sillier than it is.** It is a real answer to a real risk, and it is also the whole film.

### THE SYSTEM MAP (one per episode)

**ACT_6, roughly 38:00.** Not a diagram of the FTCA. A diagram of **the door the family has to get
through**, drawn once and then walked:

```
        a federal officer harms you
                    ↓
      §1346(b): the United States waives immunity        ← the front door, 1946
                    ↓
      §2680: thirteen exceptions claw it back
                    ↓
   (h) intentional torts ── barred ──┐
                    ↓                │  1974 proviso: six torts by law enforcement get through
   (a) discretionary function ───────┴──→  ← THIS is the door that is still shut
                    ↓
      state law: would a private person be liable?
                    ↓
                  a trial
```

Three of the five gates are still unopened for this family nine years in, and the Supreme Court's whole
2025 decision moved them **one** gate. State that plainly; do not dress it.

### THE HIDDEN RULE (closing sentence, ACT_6)

> **The rule is this: when the government harms you by accident, the question is almost never whether it
> happened. It is whether the mistake it made was the kind of mistake somebody was allowed to make.**

## 6. Numbers become life units (v002 §8)

Never read a figure aloud without translating it.

- **Eight years, nine months and twenty-five days** since the door came in → *the seven-year-old under the
  blanket is old enough to drive.* (Our arithmetic; labelled as ours; his age today is never stated —
  `forbidden_claims`.)
- **Seven months of leave** → *from one autumn to the next spring, she did not go to work.*
- **Ten to twenty seconds** → *read the sentence, out loud, at the speed you are reading it. That was the
  wait.*
- **Three or four houses** → *the distance you walk to put the bins out.*
- **Forty-four years and six months** between Collinsville and Denville Trace → *a law older than either
  parent in that house.*
- **Thirteen exceptions** → *thirteen ways the sentence "you can sue the government" ends in "except".*

## 7. What may not be shown, and what is shown instead — the binding substitution table

This is the other half of `forbidden_subjects`. Every row is a decision, not a preference. **The
emotional centre of this film is a seven-year-old under a blanket and he will never be on screen.**

| The film will not show | It shows instead |
|---|---|
| the child, in any form, at any age, in any style | the doorway of an empty room seen from floor height; a blanket's edge; a hallway light-line under a closed door; the corridor of an empty school at night |
| Curtrina Martin, Toi Cliatt, or any likeness of them | a woman's hand flat on a closet floor, cropped at the wrist; a man's shoulder and cuffed hands, back to camera, face out of frame; two coffee cups on a kitchen counter at 5 a.m. |
| Lawrence Guerra, any agent, any judge, any justice, any attorney | armour and equipment without a face — a shoulder, a glove on a doorframe, boots on a step; a bench and an empty chair; a lectern, from behind |
| a real photograph of either house | the *type*: a beige split-level on a corner lot with a large tree, shot as architecture, never as a specific address; the mailbox at the end of a driveway, numbers legible, then out of focus |
| the moment of the breach, as violence | the door **before**; the doorframe **after**; the flash as light on a ceiling in another room; a plate of the hallway with the front door open onto darkness |
| the flash-bang as an explosion | one frame of white, then afterimage; light under a door; the smell of it implied by a dust-hang in a beam |
| a gun pointed at a person | the muzzle-shadow on a wall; a rifle's foregrip against a doorframe; a torch beam crossing a closet rail of hanging clothes |
| any document as an authentic record | documents built as *illustration* and always framed as such — a form with real headings and unreadable body text, shallow focus, never a full legible page; and where a real quotation is on screen it is set as **typography on black**, in the brand face, credited to the document by name |
| Collinsville 1973 as archive footage | commissioned 1973 plates, and the two or three genuinely period archival clips the shelf holds (8mm house party, 16mm demolition), used as **texture, never as evidence of the raids themselves** |
| Joseph Riley, in any form | 3741 Landau Lane as a shape on a map, and nothing else |

## 8. Craft rules this film is held to

- **No two explanation blocks in a row** (v002). The FTCA is explained three times in this film and never
  twice consecutively: each explanation is separated from the next by a scene, a document or a voice.
- **A new fact, question, emotion, image or consequence every 60 seconds.** The beat map in
  `EP70_wronghouse_shotlist.v001.json` carries the check.
- **Re-hook every 2–3 minutes**: a question the viewer cannot answer yet. There are eighteen in the script
  and they are marked.
- **The narrator opens on the scene and enters the system afterwards, every single time.** Never
  *"under the Federal Tort Claims Act…"* as the top of a section.
- **No CTA before the ending.** The ask is one sentence, specific, and earned by the last beat.
- **Every motion is specified in numbers** in the shotlist, never in adjectives (spec v2 row 14).
- **Average shot ≤ 4.2 s** (`target_cut_sec`), designed transitions 0.3–0.5 s, no naked hard cut, no held
  frame above 2 s, `Bookends` imported and not forked.

## 9. The producibility problem, named here so it is not discovered at assembly

Measured 2026-08-12 over the same 26,101-clip pool EP68 and EP70 used, reproducible from
`measurements/EP71_wronghouse_registers.py`.

**The good news is real.** The era-neutral registers this film actually lives in — hands, paper, doors,
mail, clocks, first light, corridors, weather, files, texture, maps, screens — union **7,534** clips, which
is **0.053 utilisation, green**, and they are the film's visual language anyway. A door. A mailbox. A
hallway. Paper. This is the shelf's genuine strength and this premise sits directly on it.

**The bad news was not where it was expected.** The premise was chosen partly because it is contemporary,
and contemporary is 93.5% of the shelf. That held for the house — sixty-odd usable modern suburban
exteriors, none of which the archival side could have supplied — and it **failed completely for the raid**.
An independent re-measurement returns **ten distinct titles** for swat / tactical / breach / raid /
flashbang across the entire shelf: seven are Second World War naval raids, one is a balaclava'd car thief,
one is a Pakistani police still, and **one** is usable. Channel-wide there are 177 titles containing
police / officer / patrol / sheriff and 50 containing front door / suburban / residential / driveway /
porch.

**So the shelf can dress the aftermath and cannot dress the incident.** Which is, by luck, exactly the
right way round for a film that is 5 minutes of incident and 45 minutes of aftermath — and it is why the
breach is built from **commissioned plates plus a named i2v budget** (roughly 14 conversions, 0.8 GPU-hours)
rather than from queries that will return Pearl Harbor.

**ACT_4 is the other hole**, and this one was expected: 218 raw titles, 54 archival, 9 archival *and*
period-titled, of which at most three are usable and not one is an American street, house, car or hearing
room. Budgeted at roughly 16 conversions, 0.9 GPU-hours.

Both budgets total **~30 conversions, ~1.7 GPU-hours, ~7% AI motion across the film** — above the channel
norm of 0% and far below the EP62–65 regression band of 44–57%. **Both require owner approval before the
build starts** (`episode_spec.approved_deviations`), and both must be generated to *exactly* that count,
because `solve_totals` splits video proportionally to pool capacity and a buffer pushes archive cuts off
the screen.

## 10. Risk

**R3.** Every fact comes from published federal opinions, the parties' own filings, a Supreme Court
transcript and two dockets. No living private individual is accused of a crime by this film.

The four disciplines, all of which are also in `forbidden_claims`:

1. **The case is live.** Everything about the officers' conduct is *alleged*, *the family swore*, or *the
   court found*. Nothing is the film's own accusation.
2. **Two accounts of the same five minutes.** Attributed, both, every time.
3. **A real child.** Not named, not aged, not depicted, not imagined.
4. **No politics.** The remand panel's appointing presidents are on the public record and are deliberately
   not used, because naming them would import exactly the colour the brand forbids.

**Before scheduling:** re-verify §9 of the facts ledger. The Eleventh Circuit could rule at any time, and
if it does, ACT_6 and the ending are rewritten before the film goes out — not patched afterwards.
