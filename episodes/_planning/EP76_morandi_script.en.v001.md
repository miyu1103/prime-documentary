# EP76 · MORANDI — SCRIPT v001

> **Design `EP76_morandi_FILM_BIBLE.v001.md` · facts `EP76_morandi_FACTS_LEDGER.v001.md` (the only
> source of any factual line) · contract `episodes/PD-2026-076-morandi/episode_spec.v001.json`.**
>
> **Citation convention.** Every factual line is followed on the next line by an HTML comment
> carrying its ledger row id and grade.
>
> **Register.** Declarative. Past tense. Zero emotion commands. Four rules break this film if
> broken: nobody is said to have foreseen or intended the collapse — the court struck that
> circumstance out for every defendant and acquitted all of them of the intentional offences
> (⛔-02); every convicted person is named with *convicted at first instance* and *not final*, and
> every acquitted person with the acquittal, in the same sentence (⛔-01); the number in the box is
> never attributed to a person (⛔-07); the two findings on the first cause are both given, with
> their dates, and are not resolved (⛔-04).
>
> **Sized from measurement, not from a model.** `gen_narration_case.py --measure-section ACT_1`
> was run against this script on 2026-08-21 at the pinned voice settings: 46 chunks / 650 words,
> ffprobed at **211.906 s of speech = 184.0 raw wpm** (173.0 words per finished minute). The script
> then extracts **328 chunks / 5,118 words**, inside `script_words` [4900, 5400]:
> 5,118 / 184.0 × 60 = **1,669.0 s of speech**, plus 320 beat gaps at 0.30 s (96.0 s) and seven
> section boundaries at 1.8 s (12.6 s) = a **1,777.6 s master**, and a **1,786.6 s film (29:47)**
> once the 9.0 s endcard is added — inside `runtime_seconds` [1740, 1920].
>
> `check_script_length` reads 5,287 on this file rather than 5,118; the difference is this
> front-matter and markdown furniture, and it is in the safe direction. **The HTML-comment
> over-count described in `PD_ONE_PASS_PRODUCTION_SPEC.v3` §6.6 was fixed in that script on
> 2026-08-21**; before the fix this file read 5,872 against 5,114 spoken — a +758-word inflation
> that made the gate call a 29:52 script LONG by 392 words.

---

## HOOK

【0:00.0–0:22.4 · voiced from frame 0 · 67 words, 21.8 s of speech at the measured 184.0 wpm plus two 0.3 s beat gaps · Pictures: a valley of roofs, rails and sheds from above → a concrete soffit, close → spalled concrete with steel showing → a printed form, ruled, one empty box → a hand, a pen → the box. Push-in f0→f36, scale 1.06→1.00, Easing.out(Easing.cubic), Trail 6 layers to f18.】

On the first of August 2012, under a motorway viaduct in Genoa, an inspection recorded a beam with the concrete gone, the cables showing, and some of the wires broken.
<!-- MO-53 ✓ VERBATIM · ⛔-07 (no person is named or characterised) -->

Then the form asked for a number. The number written in the box was forty.
<!-- MO-53 ✓ VERBATIM -->

In the company's own manual, broken wires in the prestressing steel are a seventy. And a seventy means measures up to closing the road.
<!-- MO-48, MO-49 ✓ VERBATIM QUOTE (SRC-0003 quoted inside SRC-0001) -->

【BrandOpening lands here, gold, 3.5 s, over continuing footage.】

---

## OP

【0:22.4–0:54.0 · Pictures: the valley again, wider → the four ties of a balanced system against sky → a stay in section, dark → black.】

This is a story about a shell of concrete, a printed form, and a document that was owed by law and never written.
<!-- OURS — thesis line -->

It is not a story about a bridge that fell down. It is a story about the thing you do without thinking, every day, in a car: crossing a structure somebody else is responsible for looking at.
<!-- OURS — controlling idea -->

Over the next half hour you will see what was inside that concrete, what happened the one time anybody cut into it, what the inspections were actually measuring for twenty-five years, and what a court in Genoa decided about all of it, eight years later.
<!-- OURS — opening promise, per structure spec row 10; each clause is answered later -->

---

## ACT_1 — THE SHEATH

【0:52.0–5:45.0 · Pictures: Polcevera valley, industry and rail · a road on stilts over roofs · antennae against cloud · a span diagram drawn · the stay in section, hero · strand macro. F01–F14.】

The Polcevera is a river in Genoa that runs down out of the hills to the sea, and by the middle of the twentieth century almost nothing of the valley floor was still river.
<!-- MO-07 ✓ VERBATIM (densely urbanised and industrialised) -->

There were apartment blocks in it, and industrial plants, and a railway yard, and railway lines, and city streets.
<!-- MO-07 ✓ VERBATIM -->

In 1962 a professor of bridge construction named Riccardo Morandi produced a design to carry a motorway across all of that.
<!-- MO-03, MO-04 ✓ VERBATIM -->

Building started in 1963. It opened in 1967.
<!-- MO-03 ✓ VERBATIM -->

It stood at kilometre zero point five five one of the A10, the motorway that runs west out of Genoa towards Savona and France.
<!-- MO-01 ✓ VERBATIM -->

It was one thousand one hundred and two metres long, and it stood, on average, fifty-six metres above the valley floor.
<!-- MO-05 ✓ VERBATIM -->

Eleven spans. The shortest was sixty-five metres. The longest was two hundred and eight.
<!-- MO-06 ✓ VERBATIM -->

Most of the deck sat on ordinary concrete trestles, shaped like a letter V.
<!-- MO-10 ✓ VERBATIM -->

But three of the spans were something else, and those three are the reason this story exists.
<!-- OURS — transition; the three balanced systems are MO-09 -->

【F08: the balanced system drawn, line by line, 4.0 s.】

At three points along the viaduct — the piers numbered nine, ten and eleven — Morandi built what the engineers call a balanced system.
<!-- MO-09 ✓ VERBATIM -->

A concrete tower stands up out of the valley. The road runs through it. And from the top of that tower, four enormous diagonal ties run down and take the weight of the deck, two on each side, so that the pull on one side is balanced by the pull on the other.
<!-- MO-09 ✓ VERBATIM -->

The towers stood as much as ninety metres above the ground.
<!-- MO-09 ✓ VERBATIM -->

Between those big spans, the gaps were closed by short decks of six prestressed concrete beams each, thirty-six metres long. In Italian they are called infill decks. There were ten of them.
<!-- MO-11, MO-12 ✓ VERBATIM -->

Morandi had built this before. A few years earlier he had used the same system for a bridge across the mouth of Lake Maracaibo, in Venezuela, and he would use it again in Libya.
<!-- MO-13 ✓ VERBATIM -->

But in Italy there was only ever one of them. Out of the whole national motorway network run by the concession company, the Polcevera viaduct was the only cable-stayed bridge.
<!-- MO-02 ✓ VERBATIM -->

It is worth being precise about what was underneath it, because the ministry's own report is.
<!-- OURS — sets MO-14 -->

The infill decks passed directly over industrial buildings, over railway lines and over roads. The balanced systems stood a few metres from inhabited blocks holding at least five hundred people. And the viaduct was a nodal point for two motorways, for the port of Genoa, and for the industry on either side of it.
<!-- MO-14 ✓ VERBATIM -->

All of that is in a footnote.
<!-- MO-14 ✓ OURS — footnote 13 of SRC-0001 -->

【F04: the phrase held, 3.0 s, ambient only.】

Now the part that matters.
<!-- OURS — bridge into the hero object -->

On a modern cable-stayed bridge, the stays are steel, and you can see them. They are cables in the open air. You can walk up to one, put a hand on it, run an instrument along it.
<!-- OURS — plain-language contrast; the Polcevera arrangement is MO-15 to MO-21 -->

Morandi's stays were concrete.
<!-- MO-09 ✓ VERBATIM -->

Inside each one there was steel — strands of high-tensile wire, half an inch across, running over a saddle at the top of the tower.
<!-- MO-15, MO-16 ✓ VERBATIM -->

【F12: 352 lands left, 112 rises right, staggered 6 frames.】

Three hundred and fifty-two strands carried the weight. Another hundred and twelve did a different job.
<!-- MO-16, MO-17 ✓ VERBATIM -->

The order in which it was built is the whole point, so here it is.
<!-- OURS -->

First the main cables were hung and tensioned, until they were holding up the deck.
<!-- MO-18 ✓ VERBATIM -->

Then, and only then, a sheath of concrete was built around them — precast segments, threaded on from outside, at first free to slide against the steel.
<!-- MO-19 ✓ VERBATIM -->

The second set of cables sat inside that sheath, further out, and they were pulled tight so as to squeeze the sheath itself into compression.
<!-- MO-20 ✓ VERBATIM -->

And then grout was injected into the ducts, and the steel, the second cables and the concrete shell became one solid thing.
<!-- MO-21 ✓ VERBATIM -->

【F11 hero: the sheath in section, mask wipe f0→f150 along the stay axis, then hold 1.5 s.】

The stated reason for all of that, in the record, is a single phrase.
<!-- OURS — sets the quote -->

The advantage of preserving the metal part of the stays from corrosion.
<!-- MO-22 ✓ VERBATIM QUOTE — quote card, attributed on screen to SRC-0001 -->

The concrete was there to protect the steel.
<!-- MO-22 ✓ OURS — restatement of the quoted purpose -->

It is also the reason nobody could look at the steel.
<!-- OURS — controlling idea, derived from MO-22 + MO-23 -->

And the ministry's own commission, half a century later, put the consequence in a sentence that sounds like nothing until you understand what it is about to cost.
<!-- OURS — sets MO-23 -->

It is universally recognised that indirect methods of investigation do not permit quantitative assessment. Direct investigation is therefore indispensable.
<!-- MO-23 ✓ VERBATIM QUOTE -->

Direct investigation means one thing. It means cutting into the concrete.
<!-- OURS — plain-language gloss of MO-23 -->

---

## ACT_2 — ONE OF THREE

【5:45.0–11:30.0 · Pictures: a shop front and a viaduct above it, 1980s texture · hatches cut in a soffit · scaffolding on a tower · a duct clamped to the outside of a concrete tie, hero · three piers drawn, one filling. F15–F28.】

By the beginning of the 1980s the bridge was fifteen years old.
<!-- MO-03 ✓ OURS — arithmetic from the 1967 opening -->

In 1981 the motorway company asked Morandi himself for a report on it.
<!-- MO-30 ✓ VERBATIM -->

We have not read that report, and this film is not going to tell you what was in it.
<!-- AB-04 ✓ ABSENCE — the film states its own limit -->

What the record does say is that from the 1980s onward — in part following that report — the viaduct became the subject of a series of maintenance works, ordinary and extraordinary.
<!-- MO-30 ✓ VERBATIM -->

Surfaces were repaired. The drainage was renewed. And hatches were cut into the deck so that people could get inside it and look.
<!-- MO-31 ✓ VERBATIM -->

Between 1986 and 1993 there was more. The lower edge of the infill-deck beams was strengthened. The underside of the box girders was repaired. New barriers went in along the middle of the road. New bearings were fitted. Access holes were made for inspections. And cables were installed to strengthen the lower slab of the box girder at pier nine.
<!-- MO-32 ✓ VERBATIM -->

Then, in 1992, they went to pier eleven.
<!-- MO-33 ✓ VERBATIM -->

Pier eleven was the one nearest the city.
<!-- MO-33 ✓ VERBATIM -->

The plan was modest. Patch the concrete, protect it, move on.
<!-- MO-33 ✓ OURS — paraphrase of "un intervento di parziale integrazione e di protezione del calcestruzzo" -->

Before starting, they ran some checks. Not to find anything. To price the job — to work out how much patching there was going to be.
<!-- MO-33 ✓ VERBATIM ("verifiche preliminari, condotte per meglio calibrare gli interventi") -->

【F19: a drill core coming out, 3.0 s.】

The record's phrase for what those checks turned up is a far more worrying situation.
<!-- MO-33 ✓ VERBATIM QUOTE -->

There were voids inside the concrete. There was concentrated deterioration, worst of all at the point where the stays met the cross-beam at the top of the tower. And there was corrosion in the cables.
<!-- MO-33 ✓ VERBATIM -->

So they opened it up properly, and here is what they found.
<!-- MO-34 ✓ OURS — transition into the quote -->

【F21 hero quote card, 5.0 s hold, ambient bed only.】

The investigations therefore brought to light the grave state of oxidation of the internal prestressing cables. Numerous strands were severed, or heavily oxidised, with advanced reduction of section. Other strands appeared visibly slackened, suggesting a significant loss of pretension.
<!-- MO-34 ✓ VERBATIM QUOTE -->

Severed means broken through. Reduction of section means there was less steel there than there was supposed to be. Slackened means it had stopped pulling.
<!-- OURS — plain-language gloss of MO-34's three terms -->

This was 1992, and the bridge was twenty-five years old.
<!-- MO-03, MO-33 ✓ OURS — arithmetic -->

The repair was designed by an engineer who had worked with Morandi on the original construction.
<!-- MO-35 ✓ VERBATIM -->

He did not change how the bridge worked. He kept the same arrangement — the stay with its compressed collaborating sheath — and he added to it.
<!-- MO-35 ✓ VERBATIM -->

What he added were new cables, and he put them on the outside.
<!-- MO-36 ✓ VERBATIM -->

【F24 hero: the external duct, clamped to the flank of the concrete tie. 4.0 s.】

They ran down the flanks of the existing stay, in polyethylene ducts, in the open air.
<!-- MO-36 ✓ VERBATIM -->

The record gives the reason for that in four words. To permit their future maintenance.
<!-- MO-36 ✓ VERBATIM QUOTE -->

Twenty-eight years after Morandi wrapped the steel in concrete to protect it, the man who came to fix it put the new steel where somebody could reach it.
<!-- MO-22, MO-36 ✓ OURS — arithmetic, 1963 construction to the 1992 works -->

The work took years, not months. One pier.
<!-- MO-33, AB-10 ✓ OURS — the report's own dates for the pier 11 works differ between sections, so the film gives no end year -->

It was done without closing the road, using temporary structures built for the purpose, which stayed afterwards in the possession of the motorway company.
<!-- MO-37 ✓ VERBATIM -->

In 2006 a steel walkway was added at the Genoa end of the same pier.
<!-- MO-38 ✓ VERBATIM -->

So by the end of it they knew what was inside a Morandi stay on this bridge. They had a method for fixing it. They owned the equipment.
<!-- MO-33, MO-34, MO-36, MO-37 ✓ OURS — synthesis of four verbatim rows -->

【F26: three piers drawn; 9, 10 and 11 labelled; the eleven fills; nine and ten stay hollow. 4.0 s, AE beat B2.】

The intervention was carried out only at pier eleven.
<!-- MO-37 ✓ VERBATIM QUOTE -->

There were three stayed piers on that bridge.
<!-- MO-09 ✓ VERBATIM -->

Twenty-six years after that work began, one of the other two came down.
<!-- MO-24, MO-08, MO-33 ✓ OURS — arithmetic, 1992 to 2018 -->

---

## ACT_3 — THE NUMBER IN THE BOX

【11:30.0–17:30.0 · Pictures: a printed form, ruled, hero · a gantry under a deck · hi-vis at distance, no insignia · spalled concrete, cables in view · a graph rising · a falling bar. F29–F44.】

From here the story is made of paper, and the paper is more frightening than the bridge.
<!-- OURS — act transition -->

The way the company checked its structures was by inspection. Somebody went and looked, and wrote down what they saw, and gave each defect a score out of a hundred.
<!-- MO-47, MO-61 ✓ VERBATIM -->

The scores were not arbitrary. There was a manual, written by the company, that said what each number meant and what each number obliged them to do.
<!-- MO-48, MO-49, MO-50 ✓ VERBATIM -->

【F30 quote card, 3.5 s.】

A sixty meant the defect affected the structure but did not reduce the safety margins significantly. It required work in the short term — and the manual defined short term as less than two years.
<!-- MO-50 ✓ VERBATIM QUOTE -->

A seventy was different.
<!-- OURS -->

【F30/F31: the manual's two lines, mask-up, staggered 6 frames, held 4.5 s.】

Seventy. Defect at an advanced state. Has an influence on the statics and reduces the safety coefficient. Reduction of the prestressing steel section — broken wires.
<!-- MO-48 ✓ VERBATIM QUOTE -->

And for a seventy: immediate measures are provided, such as traffic restrictions, up to closure of the carriageway, generally followed by temporary works and then by an intervention of extreme urgency.
<!-- MO-49 ✓ VERBATIM QUOTE -->

Closure of the carriageway. That is in the company's own manual, written by the company, about its own roads.
<!-- MO-49 ✓ OURS — restatement -->

Now here is what the inspections of the Polcevera viaduct actually recorded, in the ministry's own summary of them.
<!-- OURS — sets the sequence -->

In October 1991, on a stay at pier eleven: oxidised cables, oxidised and severed strands, fine cracks across the section. That one was scored seventy.
<!-- MO-51 ✓ VERBATIM -->

It was found in 1991. It was repaired in 1994.
<!-- MO-51 ✓ VERBATIM -->

In February 1997, a deck slab had dropped and was vibrating, because the bearing underneath it had partly failed. Scored forty-three. To be reported.
<!-- MO-54 ✓ VERBATIM -->

Found in 1997. Repaired twelve years later.
<!-- MO-54 ✓ VERBATIM -->

In December 2006, steel bars severed by a slab failure. Scored forty.
<!-- MO-55 ✓ VERBATIM -->

The ministry's commission said that score was absolutely not coherent with the damage found, and that in its view it should have been a seventy — with immediate measures.
<!-- MO-55 ✓ VERBATIM QUOTE -->

In August 2011, two defects in the deck beams. Scored sixty — work within two years.
<!-- MO-52 ✓ VERBATIM -->

Found in 2011. Repaired in 2016.
<!-- MO-52 ✓ VERBATIM -->

In August 2012 — the inspection this film opened with — concrete detached, cables in view, some of the wires broken. Scored forty.
<!-- MO-53 ✓ VERBATIM -->

Broken wires in the prestressing steel is the manual's own example of a seventy.
<!-- MO-48 ✓ VERBATIM -->

【F37/F38: 40 in the box, then the manual's line under it, 5.0 s hold. Score-box fill f0→f20.】

And in June 2013, inside the box girders, in the chambers you have to climb into: corroded cables. Scored fifty.
<!-- MO-56 ✓ VERBATIM -->

The commission said sixty. It also recorded something else about that one. It was found in 2013 and never repaired.
<!-- MO-56 ✓ VERBATIM -->

There is one more entry worth having, and it is an absence rather than a score.
<!-- OURS -->

Across all the inspection sheets, the first and only visit in which the foundations are said to have been examined was in October 2017.
<!-- MO-57 ✓ VERBATIM -->

Fifty years after it was built.
<!-- MO-03, MO-57 ✓ OURS — arithmetic -->

【F40 hero: the observations box, empty, 4.0 s.】

Every inspection sheet had a box on it marked observations, where the inspector wrote in words what the numbers could not carry.
<!-- MO-58 ✓ VERBATIM -->

The ministry's report puts it like this.
<!-- OURS -->

From the twenty-eighth of March 2013 to the twenty-fourth of October 2017, there are no further comments in the observations box of the sheet filled in during the inspections, and all the text annotated in previous years is deleted.
<!-- MO-58 ✓ VERBATIM QUOTE -->

Not blank. Deleted.
<!-- MO-58 ✓ OURS — restatement of "viene cancellato tutto il testo annotato negli anni precedenti" -->

Two weeks after the collapse, the company sent the ministry a technical note with graphs in it, reconstructing the scores its inspectors had given over the years. The commission read those graphs, and this is what it wrote about them.
<!-- MO-60 ✓ VERBATIM -->

【F41: the graph draws itself — flat at zero, then a near-vertical rise, then flat again. 6.0 s.】

The unreliability of the scores assigned to the defects found, given the logical — before even technical — improbability of the perfect conservation of the structures for very long periods, even in the absence of maintenance. Score zero for twenty-five years. Followed by four years of extremely rapid evolution of the deterioration, up to critical threshold values. Followed by a stabilisation of the phenomenon — and all of it without any maintenance or repair work.
<!-- MO-60 ✓ VERBATIM QUOTE -->

A structure does not sit at zero for twenty-five years, fall apart in four, and then stop.
<!-- MO-60 ✓ OURS — restatement of the commission's own reasoning -->

Which brings us to the money, because the money is the part that is not in dispute.
<!-- OURS — transition -->

The commission asked the company for everything it had spent on structural work on the whole viaduct, and totalled it.
<!-- MO-39 ✓ VERBATIM -->

From 1982 to 2018: twenty-four million, six hundred and ten thousand, five hundred euros.
<!-- MO-39 ✓ VERBATIM -->

Ninety-eight per cent of that was spent before 1999 — the year the motorway company was privatised.
<!-- MO-40 ✓ VERBATIM -->

After 1999, two per cent.
<!-- MO-40 ✓ VERBATIM -->

【F43: 98 and 2, split card, held 4.0 s.】

In the seventeen years to 1999, structural work on the Polcevera viaduct averaged one point three million euros a year.
<!-- MO-41 ✓ VERBATIM -->

In the nineteen years after it, it averaged twenty-three thousand.
<!-- MO-42 ✓ VERBATIM -->

【F44 / AE beat B3: money decay, bar falls to 1.8 % over 3.2 s, label counts down, ambient bed −6 dB.】

The whole list of structural works on that bridge, over thirty-six years, is seven lines long, and you can hear all of it.
<!-- MO-44 ✓ OURS — the table in SRC-0001 p.77 has seven rows -->

1982: three million, on ordinary maintenance to the piers. 1986: fourteen point six million — barriers, cantilevers, bearings, antennae and stays, and new cables in the pier nine slab. 1992: six and a half million, on the stays of pier eleven.
<!-- MO-44 ✓ VERBATIM -->

Then 2005: fifty thousand. 2009: thirty-seven thousand five hundred. 2009 again: ninety-five thousand. 2015: two hundred and eighty-eight thousand.
<!-- MO-44 ✓ VERBATIM -->

That is the whole of it.
<!-- MO-44 ✓ OURS -->

The concession under which the company held the road had been signed in October 2007.
<!-- MO-46 ✓ VERBATIM -->

There was other spending. About four hundred and twenty-three thousand a year on things that were not structural — including new safety barriers along a bridge, which added weight to it without any corresponding strengthening.
<!-- MO-43 ✓ VERBATIM -->

The commission drew the obvious conclusion, and it wrote it down in the language of the concession contract.
<!-- OURS — sets MO-45 -->

Not doing simple ordinary maintenance today means wanting to do a great deal of extraordinary maintenance tomorrow, at certainly higher costs, with a mirror-image higher remunerativeness. From which it follows, as a logical corollary, a maximisation of profits by using the contractual clauses to one's own exclusive advantage.
<!-- MO-45 ✓ VERBATIM QUOTE — quote card, attributed on screen -->

---

## ACT_4 — THE THING NOBODY WROTE

【17:30.0–23:45.0 · Pictures: a folder spine with a date · a card index, one tab empty, hero · a committee room, empty chairs · a lectern · a stack of bound drawings · a viaduct at midday, wide · a road that stops. F45–F62.】

There is one document at the centre of this story, and it is the one that was never written.
<!-- OURS — act thesis -->

In 2003 Italy issued an order requiring the owners of strategic structures — the ones that matter in a civil-protection emergency, or whose collapse would be serious — to carry out a formal assessment of their safety.
<!-- MO-62 ✓ VERBATIM -->

For the Polcevera viaduct, the deadline was March 2013.
<!-- MO-62 ✓ VERBATIM -->

The commission explains why that assessment matters, and it is worth being exact about it, because it is the difference between the whole of this story and a story with no dead in it.
<!-- OURS — sets MO-63 -->

From that assessment, if correctly carried out, would have come the best possible estimate of structural safety against the risk of collapse.
<!-- MO-63 ✓ VERBATIM QUOTE -->

In July 2014 the ministry's supervision directorate wrote to the motorway concession companies asking where they had got to.
<!-- MO-69 ✓ VERBATIM -->

The company replied that same month with assurances that the safety assessments were about to be completed. It repeated those assurances, for the last time, in 2017.
<!-- MO-69 ✓ VERBATIM -->

On the twenty-third of June 2017, in a numbered letter to the ministry, the company stated that for the Polcevera viaduct the assessment had been carried out.
<!-- MO-64 ✓ VERBATIM -->

【F49 hero: the card index, one tab, nothing behind it. 4.0 s.】

Here is the commission's finding on that.
<!-- OURS -->

In the documents requested and obtained by this Commission, that assessment had not, at the date of delivery of the present report, in fact been carried out.
<!-- MO-65 ✓ VERBATIM QUOTE -->

Elsewhere in the same report the commission puts it flatter still: for the Polcevera viaduct, no safety analysis and no seismic assessment of the viaduct was ever made.
<!-- MO-67 ✓ VERBATIM QUOTE -->

Four months after the letter that said it was done, in October 2017, the designer of the repair project was asked by the project's own verifier whether the seismic requirements had been dealt with. He answered that the question was also under way.
<!-- MO-66 ✓ VERBATIM QUOTE -->

The commission notes the contradiction between those two statements without further comment, and so will we.
<!-- MO-66 ✓ OURS — the film declines to attribute a motive -->

There was a form on file. A level-zero seismic verification summary sheet, revised in October 2011. The commission read it and recorded that it contained descriptive data about the viaduct that were absolutely not pertinent.
<!-- MO-68 ✓ VERBATIM QUOTE -->

The assurances themselves, the commission wrote, appear certainly adequate from a merely formal point of view.
<!-- MO-69 ✓ VERBATIM QUOTE -->

Meanwhile there was a project, and the project is where the language starts doing work.
<!-- OURS — transition -->

【F52: the word RETROFITTING, held, 3.0 s.】

It was called a structural retrofitting intervention.
<!-- MO-81 ✓ VERBATIM -->

Here is what it actually was.
<!-- OURS -->

The retrofitting project consisted of the construction of a system of external tensioning of the concrete stays of piers nine and ten — necessary to make up for the progressive loss of functionality of the prestressing cables embedded within the stay itself.
<!-- MO-70 ✓ VERBATIM QUOTE -->

That is the same fix they had carried out at pier eleven, twenty-five years later, on the two piers that had never had it.
<!-- MO-36, MO-37, MO-70 ✓ OURS — synthesis; arithmetic 1992 to 2017 -->

The works were worth twenty million, one hundred and fifty-nine thousand, three hundred and forty-four euros and twenty-six cents.
<!-- MO-74 ✓ VERBATIM -->

At that value, the law required the design to be validated by an independent accredited inspection body. The commission's finding on whether that happened is three words long: it does not appear from the file.
<!-- MO-74 ✓ VERBATIM QUOTE -->

What there was instead was an internal verification, by an engineer inside the group. And the officer running the procedure gave that verifier an instruction.
<!-- MO-71, MO-75 ✓ VERBATIM -->

【F55: the instruction, mask-up, held 5.0 s.】

It was concluded that the intervention on the stays, by reason of its particularity, and the precedents to which it refers back — see pier eleven — constitutes an extremely specialist activity whose development translates into constructive and dimensional choices strongly overseen at the design stage. It is therefore not considered necessary to intervene on the aspects mentioned above.
<!-- MO-75 ✓ VERBATIM QUOTE -->

In plain words: the stays are the hard part, the people who designed them know what they are doing, so the verifier need not check them.
<!-- MO-75 ✓ OURS — gloss -->

The commission's response to that is one of the sharpest sentences in the whole report.
<!-- OURS -->

From that instruction of the officer, illogical as well as contrary to the rules, it followed that the verifier would not have to concern himself, in the verification process, with the part of the highest engineering demand — denying the principles and the very purposes of the verification process, and vitiating its final formulation.
<!-- MO-76 ✓ VERBATIM QUOTE -->

The verifier raised sixty-two observations anyway.
<!-- MO-77 ✓ VERBATIM -->

Number fourteen asked why the repairs covered only the stretch between piers nine and eleven and not the rest of the structure. The answer was that the rest — piers one to eight — would be the subject of a subsequent contract.
<!-- MO-78 ✓ VERBATIM QUOTE -->

Number thirty-six asked how, precisely, the new cables were going to be tensioned. The answer was that the tensioning methods were being further studied.
<!-- MO-79 ✓ VERBATIM QUOTE -->

The commission's note on that: it is entirely evident that a statement of this kind at the executive-project stage is unacceptable.
<!-- MO-79 ✓ VERBATIM QUOTE -->

To the verifier's correct and precise observations, the report says, evasive and inconclusive answers were given. The verification concluded positively.
<!-- MO-80 ✓ VERBATIM QUOTE -->

Then the project went to the ministry, and the way it was described to the ministry decided who would look at it.
<!-- MO-82 ✓ VERBATIM -->

It was presented as a mere conservative repair of the structure, in order to extend its useful life.
<!-- MO-82 ✓ VERBATIM QUOTE -->

Described that way, it did not look complicated enough to send up to the Superior Council of Public Works — the body that exists to look hard at difficult things.
<!-- MO-82 ✓ VERBATIM -->

It went instead to a regional technical committee, which met on the first of February 2018.
<!-- MO-85 ✓ VERBATIM -->

Two days before that meeting, and again four weeks after it, the company wrote to chase the approval. The second of those letters said that continued delay would have repercussions for its economic planning — and for the increase in safety necessary on the viaduct.
<!-- MO-83, MO-84 ✓ VERBATIM QUOTE (notes of 30 January and 28 February 2018) -->

Its own words. The increase in safety necessary on the viaduct.
<!-- MO-84 ✓ VERBATIM QUOTE — quote card -->

【F58: the committee room, empty, held 4.0 s.】

At that meeting the project was explained to the committee by the technicians of the concession company who had drawn it up.
<!-- MO-85 ✓ VERBATIM -->

The commission: such a procedure — the illustration of the project under examination by the designer himself — must be regarded as irregular and inappropriate for a neutral examination of the project.
<!-- MO-85 ✓ VERBATIM QUOTE -->

The favourable opinion therefore came after a rapid and apparently not thorough examination.
<!-- MO-86 ✓ VERBATIM QUOTE -->

Nobody, then — neither the company, nor the ministry division, nor the committee — grasped the need to assess the importance of the project and its coherence with the particular and complex load-bearing structure of the Polcevera viaduct.
<!-- MO-87 ✓ VERBATIM QUOTE -->

And there is one more thing in the project file, which the commission found by reading the calculations rather than the covering letter.
<!-- OURS — sets MO-94 -->

In the project's own numbers, the safety check on one of the deck's edge beams did not pass — not in bending, and not in shear.
<!-- MO-94 ✓ VERBATIM -->

【F59: 0.71 and 0.58, split card, 4.0 s.】

The ratio of what the beam could carry to what it was being asked to carry came out, depending on how much deterioration you assumed, between zero point seven one and one point zero one in bending, and between zero point five eight and zero point nine three in shear.
<!-- MO-94 ✓ VERBATIM -->

Below one means it does not pass.
<!-- MO-94 ✓ OURS — gloss -->

These are wholly unacceptable values, the commission wrote, which under the technical rules in force required a safety measure that could not be postponed. From the information available to this Commission, no measure of that kind was taken.
<!-- MO-95 ✓ VERBATIM QUOTE -->

The commission also recorded that this information, of evidently enormous importance, was — according to what the company's own managers told it — not known to them.
<!-- MO-96 ✓ VERBATIM -->

The same conditions were, with high probability, true of all ten of the infill decks, which were identical in design, execution, age and exposure. Three of them had been strengthened.
<!-- MO-97 ✓ VERBATIM -->

For the western part of the viaduct, at the date of the collapse, no work at all was planned. The commission's phrase for why is: for reasons unknown to this Commission.
<!-- MO-98 ✓ VERBATIM QUOTE -->

There is one more finding in the report, and it concerns the equipment that hung under the deck so that people could inspect it.
<!-- OURS — sets MO-99 -->

The gantry that ran along the underside was bolted to the edge beams. The commission found no record of any precaution taken, when those fixings went in, to avoid cutting through the steel inside those beams — and wrote that such work, repeated over the years, could have reduced their strength substantially, and could have contributed to the collapse.
<!-- MO-99 ✓ VERBATIM QUOTE -->

The committee's opinion was signed off in February 2018, and passed on in March.
<!-- MO-85, MO-89 ✓ VERBATIM -->

【F60: the viaduct, wide, ordinary daylight. Cut hard on the timecode card.】

At eleven thirty-six in the morning, on the fourteenth of August 2018, the balanced system at pier nine, and the two infill decks joining it to the spans on either side, came down.
<!-- MO-24 ✓ VERBATIM -->

About two hundred and forty-three metres of road.
<!-- MO-25 ✓ VERBATIM -->

【F62: 43, held longest of any card in the film, 6.0 s, ambient only.】

Forty-three people were killed. Thirteen were injured.
<!-- MO-26 ✓ VERBATIM · ⛔-05 (nobody is named, shown or characterised) -->

Given the condition of the two remaining stayed piers, the authorities ordered the houses underneath them to be emptied, and marked out a danger zone under the ground around all three.
<!-- MO-28 ✓ VERBATIM -->

---

## ACT_5 — WHAT WAS DECIDED

【23:45.0–29:00.0 · Pictures: a road that stops, barrier across it · dark windows in a block under a viaduct · two bound reports side by side · a corridor with a bench · a lectern · an empty chair · the barrier again, hero. F63–F78.】

A commission was appointed the same day, and reported a month later. It was made up of engineers from the state's own advisory body on public works, two university professors of structural engineering, and a councillor of the national audit court.
<!-- SRC-0001 title page ✓ VERBATIM (D.M. 386 of 14/08/2018; membership) -->

Its finding on what broke first is more careful than the one you will usually read, and the care is the point.
<!-- OURS -->

The commission held it more likely that the first cause was to be sought not so much in the rupture of one or more stays, as in that of one of the remaining structural elements — the edge beams of the infill decks, or the box-girder decks — whose survival was conditioned by the advanced state of corrosion present in the structural elements.
<!-- MO-100 ✓ VERBATIM QUOTE -->

It then said something that almost no institution says out loud.
<!-- OURS -->

It had a month. It had not been able to see video material which, from press reports, appeared to carry very important information. And therefore, it wrote, the causes and mechanism of the collapse are listed as plausible but not definitive working hypotheses.
<!-- MO-102 ✓ VERBATIM QUOTE -->

Two years later, a panel of experts appointed by the investigating judge filed a report of about five hundred pages, answering forty questions put by the prosecutors.
<!-- MO-107 ✓ SECONDARY — attributed on screen to the named outlets; ⛔-13 -->

As reported at the time, that panel identified the cause as corrosion in the upper part of the south stay, on the Genoa side, of pier nine — and concluded that checks and maintenance, if they had been carried out correctly, would with high probability have prevented the event.
<!-- MO-108, MO-109 ✓ SECONDARY QUOTE — attribution card on screen -->

We have not read that report. This film is not going to pretend otherwise, and it is not going to choose between the two findings.
<!-- AB-03, AB-05 ✓ ABSENCE -->

What both of them rest on is the same thing, and on that the ministry's commission is unambiguous.
<!-- OURS -->

The ordinary reinforcement, and some of the prestressing, in the simply supported spans had no cover — expelled years earlier. The quality of the grouting of the prestressing ducts was modest, both in the beams and in the stays. All of it had been known to the concessionaire for years.
<!-- MO-103 ✓ VERBATIM QUOTE -->

Direct investigations were therefore indispensable, and had been for years, and that requirement was known — and could not have been otherwise — to the company.
<!-- MO-104 ✓ VERBATIM QUOTE -->

And then the sentence the whole report is built towards.
<!-- OURS -->

【F70: a road sign gantry, blank. 4.0 s.】

The most significant immediate responsibility, the commission wrote, consists in the fact that, notwithstanding all the critical points highlighted above, the concessionaire did not, in this specific case, make use of the powers to restrict or prohibit traffic on the viaduct conferred on it by the highway code — and consequently did not carry out all the works necessary to avoid the collapse that occurred.
<!-- MO-105 ✓ VERBATIM QUOTE -->

The company that operated the bridge could have closed the bridge. That power was in the road traffic act, and it was theirs.
<!-- MO-105 ✓ OURS — restatement -->

The commission's closing paragraph puts the rest of it on the country.
<!-- OURS -->

This latest grievous event, which caused forty-three victims, must not be consumed without the Nation becoming conscious of the fact that this system of management of public infrastructure has not worked, and in particular has not guaranteed the safety of users.
<!-- MO-106 ✓ VERBATIM QUOTE -->

Then the law moved, and it moved quickly.
<!-- OURS -->

Within six weeks a decree created a national agency for the safety of road and motorway infrastructure, with an office in Genoa, and a national register of public works.
<!-- MO-134 ✓ VERBATIM -->

Two years after that, the ministry issued national guidelines for classifying, assessing and monitoring the risk of existing bridges.
<!-- MO-135 ✓ VERBATIM -->

The company changed hands. In June 2021 the Italian state's investment arm, together with two international infrastructure funds, agreed to buy eighty-eight per cent of it, and the purchase completed in May 2022.
<!-- MO-137 ✓ VERBATIM -->

And the criminal proceedings took eight years.
<!-- MO-114, MO-115 ✓ OURS — arithmetic from 2018 to 2026 -->

The trial opened in Genoa in July 2022, with fifty-seven defendants.
<!-- MO-114, MO-116 ✓ SECONDARY -->

On the sixteenth of July 2026, the court read out its decision.
<!-- MO-115 ✓ VERBATIM -->

【F73 / AE beat B4: 32 lands left, 25 rises right, then "at first instance" masks up beneath both, 3.0 s hold.】

Thirty-two people were convicted. Twenty-five were acquitted, or their charges were declared time-barred.
<!-- MO-116 ✓ SECONDARY · MO-117, MO-118, MO-124 to MO-129 ✓ VERBATIM -->

The former chief executive of the motorway company, Giovanni Castellucci, was convicted at first instance and sentenced to twelve years. His lawyers said they would appeal, and the judgment is not final.
<!-- MO-120 ✓ VERBATIM · MO-133 ✓ SECONDARY · ⛔-01 -->

Thirty-one others received sentences between eleven years and one year and eleven months, all at first instance, and all of them subject to appeal.
<!-- MO-120, MO-121 ✓ VERBATIM (32 convicted less Castellucci) · ⛔-01 -->

Added up, the sentences come to a hundred and seventy-seven years and twenty-five days.
<!-- MO-122 ✓ SECONDARY -->

All of the convicted except five were barred from public office for as long as their sentences run.
<!-- MO-123 ✓ VERBATIM -->

Now the parts of that judgment that the headlines did not carry, and that this film exists to say.
<!-- OURS -->

The convictions are for negligence. For every one of those defendants the court expressly struck out the aggravating circumstance of having acted while foreseeing the event.
<!-- MO-119 ✓ VERBATIM · ⛔-02 -->

And every defendant charged with the two intentional offences — attack on the safety of transport, and wilful omission of precautions against accidents — was acquitted, on the formula that the fact does not exist.
<!-- MO-124 ✓ VERBATIM QUOTE · ⛔-02 -->

Roberto Ferrazza, the former head of the regional public works office, was acquitted, because the fact does not constitute an offence. So were ten others charged alongside him, and nine more on the same formula.
<!-- MO-126, MO-127 ✓ VERBATIM · ⛔-01 -->

The engineer who signed the retrofitting project in 2017 was not judged at all. The proceedings against him were closed for the extinction of the offences following the death of the accused.
<!-- MO-128 ✓ VERBATIM QUOTE · MO-71 -->

The counts of causing injury, as opposed to death, had run out of time.
<!-- MO-129 ✓ VERBATIM -->

The court ordered the convicted to compensate the civil parties, with the amounts to be worked out in separate civil proceedings, and it refused every application for an interim payment.
<!-- MO-130, MO-131 ✓ VERBATIM -->

And then it gave itself ninety days to write down why.
<!-- MO-132 ✓ VERBATIM -->

Which is where this stands as this film is made. We know what was decided. We do not yet know the reasoning, we will not know it for weeks, and it is a first-instance judgment in a country with three instances.
<!-- AB-01, AB-02 ✓ ABSENCE -->

---

## ENDING

【29:00.0–29:53.0 · Pictures: the new viaduct, flat daylight, no music swell · a road that stops, barrier across it, hero, 9.0 s hold · endcard.】

There is a new bridge. It is a thousand and sixty-seven metres long, it was designed by Renzo Piano, it opened on the third of August 2020, and it cost about two hundred and two million euros.
<!-- MO-138, MO-139, MO-140 ✓ SECONDARY -->

You will read that it carries forty-three lights, one for each of the dead. Forty-three points of light were in the original design, and the number was reduced.
<!-- MO-141 ✓ SECONDARY · ⛔-10 -->

The new bridge is a fact. It is not an answer.
<!-- OURS — controlling idea -->

The question this film has been asking is who is responsible for looking at the thing you drive across, and a new bridge in Genoa does not answer it for the bridge you used this morning.
<!-- OURS -->

Italy began counting its bridges after this. The national register has recorded more than twenty thousand road bridges, viaducts and overpasses so far, and the count is not finished — many authorities have still not registered their structures or carried out a first inspection.
<!-- MO-136 ✓ SECONDARY -->

【F78 hero: the road that stops. 9.0 s hold, ambient motion only, no typography.】

The concrete was put around the steel to keep the steel safe. For fifty-one years it did something else. It meant that the only way to know was to cut into it, and that the easier thing was always to write a number in a box.
<!-- MO-22, MO-23, MO-47 ✓ OURS — the film's argument, from three verbatim rows -->

Tell me in the comments which bridge you crossed today, and whether you have any idea who is supposed to be inspecting it. I read them.
<!-- OURS — the one specific ask -->

【Endcard 9.0 s.】
