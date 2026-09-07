# PD Editorial Direction v002 — the channel is not a law channel

**Owner directive, 2026-08-11 (evening).** Machine form: `config/pd_planning_os.v002.json`.
Premise inventory: `config/pd_premise_seeds.v001.json`. Scored with
`py -3.11 scripts/score_premise.py --os v002 --score <premise>.json`.

This supersedes `docs/PD_EDITORIAL_STRATEGY.v001.md` and `config/pd_planning_os.v001.json` for
topics chosen from 2026-08-12. Both earlier files stay on disk, unmodified: they are the record of
what EP60–EP69 were judged by, and those judgements must remain reproducible.

---

## 1. The decision

Prime Documentary is **not** a law channel, a police channel, a true-crime channel or an AI channel.

> **True stories about money, power, technology and the hidden systems that shape ordinary lives.**
> *The world you live in, but never see.*

Every episode is the same shape:

```
an ordinary person
  → an ordinary day
    → contact with a system they did not know existed
      → an outcome common sense says should be impossible
        → why?
          → anatomy of the hidden system
            → the outcome
              → and this concerns you
```

The subject may be police, a bank, a hospital, an insurer, an algorithm, an airport or a landlord.
The antagonist is always THE SYSTEM, which is why the subject space can triple without the channel
scattering. Netflix carries crime, war, business and sport because the *viewing experience* is
unified, not the topic. This is the same move.

**The selection rule inverts.** Do not look for an interesting rule and then illustrate it. Look for
a person to whom something abnormal happened, and let the system explain itself afterwards:
`person → abnormal event → why? → system`, never `system → person`.

## 2. What is now binding

| | v001 (until 2026-08-11) | v002 (from 2026-08-12) |
|---|---|---|
| gate | GO ≥ 85 / IMPROVE / NO-GO, one line | REJECT <80 · RESERVE 80 · PRODUCTION 90 · PRIORITY 100 · FLAGSHIP 110 |
| rubric | 8 axes | 11 axes + four +5 bonuses; **contradiction is the primary feature** |
| slate | 8 pillars by count | portfolio: 50 core / 25 adjacent / 15 emerging / 10 moonshot |
| series | 12 | 25 formats, run as a programme schedule of playlists |
| runtime | fixed band | story dictates length; three tiers (Daily 8–11 / Investigates 15–22 / Prime Original 18–30) |
| emotion | not specified | 40 dark reality / 30 hidden systems / 20 human battles / 10 world wonders |
| funnel | 1,000 → 5 built | 1,000 judged **per day** → 10 built; the KPI is premises judged, not videos uploaded |

**Contradiction is the highest-value feature.** A criminal losing money is not a story. A man never
charged losing money is. Every premise must state its contradiction in one sentence — *normal
expectation → actual outcome → the gap* — before a single title is written. `score_premise.py --os
v002` refuses to return a verdict without it.

**Title and thumbnail form one sentence and never repeat each other.**
`Police Took His $86,900. He Was Never Charged.` + `0 CHARGES`. Titles are Subject + Verb +
Consequence, built from verbs (*took, lost, hid, refused, vanished, cost, locked, failed, knew*) and
not from *how / history / explained / framework*. Write a Core title and a Broad title every time;
ship Broad. Thumbnails come in three kinds per episode — human emotion, **evidence**, symbolic — and
the deliberate shift is toward evidence: a document, a figure, a form, rather than another AI face.

**Craft rules that are now measurable intent, not taste.** No two explanation blocks in a row. Every
60 seconds delivers a new fact, question, emotion, visual or consequence. One Moment of Truth per
episode where music and motion stop for a single document and a single sentence. One System Map per
episode. The narrator is a storyteller who knows something you don't, never a professor — open on the
scene, enter the system afterwards.

**Fear lands on preparedness.** The last beat converts *the world is frightening* into *now I can see
it*. At least 15–20% of episodes are a person defeating the system; unrelieved dread exhausts an
audience long before two million.

## 3. Two numbers in the directive that do not resolve, and what was done

Neither was silently patched. Both are marked in the JSON as `FLAGGED FOR OWNER`.

1. **The rubric sums to 120, and is called 100.** The eleven axis weights (15·4 + 10·5 + 5·2) total
   120, but the directive states a 100-point total, thresholds of 80/90/100/110, and a ceiling of 120
   with bonuses. Re-weighting the owner's own ranking to force a sum of 100 would change the ranking;
   instead the raw sum is **normalised** — `normalised = round(raw × 100 / 120)` — after which the
   four +5 bonuses apply. Every number the owner stated then holds exactly, including the 120 ceiling.
   If a 120-point base with a 140 ceiling was intended, set `normalise_to: 120` and multiply the gate
   by 1.2. One line, one field.
2. **Two emotion mixes are given** — 60/20/10/10 early, 40/30/20/10 later. The later, more specified
   one is taken as binding, following the v001 precedent that the newer statement wins.

**v002 IS the binding gate.** The owner switched it on 2026-08-12 and settled the arithmetic at the
same time: the 100-point reading stands, so the raw sum normalises by ×100/120 and the four +5
bonuses apply on top, giving the 120 ceiling the directive states. `score_premise.py` defaults to
v002; `--os v001` still re-scores EP60–EP69 under the rubric they were actually judged by, because
those judgements must stay reproducible.

## 4. What the production side adds, from measurement

These are not in the directive. They come from this repository's own numbers and they constrain it.

**A producibility gate, after the score and before greenlight.** Register abundance decides whether
an episode can be dressed at all. EP66 openfields is a field-and-woods story: the shelf holds 3,572
nature clips and it used 5% of its register. EP63 correa is a 1995 emergency room: the shelf holds
258 hospital clips, it needed 74%, and it fell short. Same shelf, same week. This is not a
search-quality problem and more querying does not fix it. So:
`utilisation = clips_needed / clips_available`, green ≤ 0.15, amber ≤ 0.40, red above.

**The new categories are the ones most likely to fail it.** Algorithms, data brokers, banking rails
and dependency stories have the thinnest archive registers on the shelf. Generating AI plates instead
makes it worse, not better: the channel's normal visual shape is ~68% archive and 0% AI motion, and
`solve_totals` splits video proportionally to pool capacity, so a bigger AI pool pushes archive cuts
off the screen — measured on correa at 52 → 46 → 41 archive cuts for +0/+20/+40 plates. The visual
solution for an abstract subject must be budgeted at the premise stage, not discovered at assembly.

**The audience PD actually has is 77% aged 55+ and 92.5% male** (measured 2026-08-11, correcting the
91% on record). Forfeiture, wrongful conviction, AI voice scams, medical bills, insurance and
property land inside that base. Dark patterns, gig-work algorithms, digital ownership and simulation
formats are bets on an audience PD does not yet have. They are correct bets — but they are
acquisition experiments and must not be judged against the same CTR expectation as core.

**The directive's central claim is supported by the strongest measurement available.** The only
mechanism ever observed to grow this channel is being linked to by external videos after publication,
and the apparent long-form advantage is confounded — its whole margin is carried by OceanGate and
D.B. Cooper, the two topics with a large external feed. Length was never the variable. *A famous,
adjacent premise* is. Widening the subject space is precisely how the number of premises with an
external feed increases. Long-form CTR is 1.61% impression-weighted (median 1.26%): impressions are
arriving and packaging is where they are lost, which is a fixable problem, not an absent market.

## 5. What this does not change

- EP62–EP69 are approved and in production. Their specs, bands and gates stand.
- EP70's current rework target remains 85 under v001 until the owner switches the default. The fix is
  the same under either rubric — centre a named evacuee family, move the promise from *a dam nearly
  failed* to *the government knew, in writing, for twelve years, and nobody told the people living
  below it* — because it raises personal relevance, story arc and contradiction together.
- Every ship gate, acceptance check and integrity rule is untouched. A build verdict is not a
  greenlight, and a greenlight is not an acceptance receipt.
- Titles in `pd_premise_seeds.v001.json` are hypotheses. No figure, name or outcome in that file may
  enter a script before primary sources support it.

## 6. The next ten

Deliberately spread across psychological triggers, so the experiment answers *which trigger dominates
for PD's own audience* rather than confirming what is already believed.

1. Police Took His Life Savings. He Was Never Charged. — core
2. He Confessed to a Crime He Didn't Commit. — core
3. His Daughter Called Crying. It Wasn't Her. — emerging
4. She Owed Hundreds. Then She Lost Her Home. — adjacent
5. What Happens in the 2 Seconds After You Tap Your Card? — moonshot
6. The Algorithm Said He Was a Fraudster. It Was Wrong. — emerging
7. The Hospital Saved His Life. Then the Bill Arrived. — adjacent
8. What Happens If GPS Stops for 24 Hours? — moonshot
9. The Button They Didn't Want You to Find. — emerging
10. He Got Every Dollar Back. — core (positive reversal)

## 7. The editorial layer, which is where the next build effort goes

The owner's closing judgement: PD has already solved the hard problem — it can manufacture. That is
also the trap. *Able to make, so make. Able to publish, so publish.* Continued, it produces the
world's most efficient average channel. The leverage is no longer in making video 10% faster; it is
in finding, rejecting, packaging and learning.

Seven roles, to be built as agents: **Scout** (finds anomalies, not news — *find events where the
outcome violates what an ordinary American would reasonably expect*), **Investigator** (primary
sources and the institution's own account), **Editor** (deletes explanation — *what can be removed
without weakening the story?*), **Packaging Director** (**holds a veto before production**: if the
title and thumbnail cannot win on a home feed, it is not built), **Devil's Advocate** (AI drifts
toward the protagonist; this role exists to stop that), **Audience Predictor** (PD's own history, not
general YouTube lore), **Portfolio Manager** (decides from data, saturation and upside, explicitly
ignoring what anyone feels like making).

The purpose of that layer is **rejection**. Judging a thousand premises costs less than making one
video. Harvest 1,000 a day, score 100, package 20, build 10.

## 8. The second half of the directive — from "make good videos" to "own a way of seeing"

Delivered the same evening, and folded into the same v002 rather than a third revision. Nothing here
contradicts §1–§7; it says what the channel must own that a competitor with the same tools cannot copy.

**Sell the discovery, not only the case.** Alongside *incident → explanation*, add *ordinary act →
fifteen minutes of machinery*. `FOLLOW THE ___` (S26) is the strongest new format: never describe the
card network — follow one $4 coffee through six companies. The same technique carries one 911 call,
one paycheck, one claim, one returned package, one evidence bag.

**The enemy is the design.** Not a bad officer, a bad company, a bad government — bad incentives, bad
information, bad rules, bad defaults. That is what makes `SYSTEM BUG`, `WHO BENEFITS?` and
`WHY NOBODY FIXED IT` possible, and it is the single strongest protection against the channel being
pulled left or right. Every episode states the system's own rationale before showing its failure.

**Answer Reversal is now a script gate.** A curiosity gap withholds the answer; this is stronger —
let the viewer form a *wrong* answer, take it away, offer a second, take that away, then land the real
one. Frozen account → fraud suspected → he committed no fraud → a bank error? → no: an outside
database. Scored on the script, not admired afterwards.

**One episode, one case, then the pattern.** `THIS KEEPS HAPPENING` (S33) lifts a single person's
misfortune into a structure: one person, then *but he is not the only one*, then fifty, then the
system. Numbers can also run the other way — an anomaly in the data (why did one county seize so much
more?) leads to the human being.

**Numbers become life units.** Not `$50,000` but three years of rent. Not `20 years` but from the day
his daughter was born until she was an adult. Reading a figure aloud is what a machine does;
translating it is the job.

**Every episode is assigned one role** — acquisition, conversion, retention, revenue or brand — and is
judged by that role alone. 50k views with 1,500 subscribers can be worth more than 100k with 100. And
the audience is built in three layers on purpose: Curious Mass in, Smart Professionals deeper, Core
Fans at the centre. Buzz → trust → habit. That funnel is the fix for *plenty of views, no
subscribers*.

**The Content Genome is the largest idea in the directive.** Stop filing episodes by theme; record
each one's DNA — protagonist type, system, contradiction, stakes, hook, evidence, structure, title
verb, thumbnail kind, ending emotion, and the performance that followed. Then, when something wins,
do **not** make ten more like it. Extract the DNA and transplant it: *cash + no crime + authority +
an exact amount* moves from a traffic stop to a bank freeze, a tax lien, an HOA. Copy the structure,
change the subject. Generate → test → measure → crossbreed → mutate → select. It may well turn out
that "police" was never the reason at all, and that *specific number + ordinary person +
institutional contradiction* was — in which case the pattern moves anywhere and the channel stops
depending on one theme.

**Three format signatures, three named concepts.** THE SYSTEM MAP, THE MOMENT (sound stops, a
timestamp, one line) and THE HIDDEN RULE (one closing sentence naming the rule the story exposed),
plus PD's own vocabulary — *System Collision*, *Expectation Gap*, *Invisible Decision*. When a viewer
says "this is another System Collision story", the channel owns a way of seeing, and that is not
copyable.

**The moat is not the toolchain.** Competitors have the same models. What they cannot have: a tipline
that brings PD cases nobody else has (target: 5% of episodes at 100k subscribers, 15% at 500k, 30% at
2M), PD's own recurring datasets published as an annual report, the genome database, and the audience
history behind it.

**And a brand filter with teeth.** A premise that would score well and does not look like PD —
celebrity scandal, outrage bait, conspiracy, gore — is rejected by the Portfolio Manager. Short-term
numbers, long-term damage. The metric that proves it worked is **brand elasticity**: does the audience
still watch when the subject is not police?

**The stated risk, in the owner's words.** The danger is not that PD fails. It is that PD succeeds
small and hardens into "the police-and-law AI channel" — a size that can reach a modest monthly
revenue and can never reach two million. The next 30–40 episodes are therefore a market experiment,
not a content plan; five shapes and ten deliberately off-pattern titles are listed in
`experiments` in the planning OS, and if any of them beats the police pattern, that category becomes
the second pillar.

## 9. The line the channel is held to

> **We do not tell viewers what to think. We show them what they didn't know.**

Do not name the villain up front; stack facts until the viewer arrives at *wait, that is allowed?* on
their own. State the system's own rationale before showing its abuse — civil forfeiture exists to
freeze criminal assets quickly, *and* it takes money from people never charged. Both are true, and
the friction between them is the brand. Police, government and justice pull a channel left or right;
political colour buys short-term CTR and costs long-term trust. Evidence first.

The measure of success is not two million subscribers. It is a million people for whom PD is a
habit — and someone asking *have you seen that Prime Documentary video about ___?* where the blank
can be filled with anything at all.
