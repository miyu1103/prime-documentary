# EP73 · TEXAS / WINTER STORM URI — SCRIPT v002

> **v002, 2026-08-22 — sized to the contract.** v001 came in at **2,845 spoken words** against a
> `script_words` floor of 4,900: a 16-minute film in a 30-minute frame. It was not padded up. The
> deficit was filled with (a) the four ledger rows v001 never used — **TX-20** (the final report's
> 28 recommendations), **TX-36** (the two unreconciled cost ranges, narrated under ⛔-06 with both
> attributed and neither adopted), **TX-42** (the exemption criticism, narrated under ⛔-07 as those
> senators' words), and **AB-02** (the counterfactual the record does not run) — and (b) the
> explanatory passages the film was assuming rather than earning: what a cascade is, what an
> ambient design temperature is, the difference between a recommendation and a standard, why an
> operator alone will not spend on winterization, why Texas demand climbs in the cold, what
> "significantly slowed restoration" means, what wellhead / gathering / midstream are, and what
> shutting a well in is. **Now 5,230 spoken words, ~29.3 finished minutes.** Every added factual
> line carries a row id like every other line; every added argument is marked OURS and asserts no
> fact. 45 of the ledger's 46 rows are now cited — the exception is **AB-04**, which records what
> we did not read and belongs in the ledger, not in the narration.
>
> Measured with a counter that strips the HTML citations (`scratchpad/count_ep73.py`).
> `check_script_length.py` counts those comments as speech and over-counts this script by roughly
> 1,300 words; **do not size with it.**

> **Design `EP73_uri_FILM_BIBLE.v001.md` · facts `EP73_uri_FACTS_LEDGER.v001.md` (the only source of
> any factual line) · contract `episodes/PD-2026-073-uri/episode_spec.v001.json`
> (`script_words` **[4900, 5400]**, `runtime_seconds` **[1740, 1920]**).**
>
> **Sized to a measurement, not a model.** EP72's narration delivered at **191.7 wpm** end-to-end in
> this register; the narration registry's 171.79 model is 11 % slow and sizing to it produced a
> script four minutes short. Confirm with `gen_narration_case.py --ep PD-2026-073-uri --dry-run`
> before generating, and with `--measure-section ACT_1` before accepting the length.
>
> **Citation convention.** Every factual line is followed on the next line by an HTML comment
> carrying its ledger row id. `check_script_length` counts those comments as speech and is not the
> instrument to size this script with.
>
> **Register.** Declarative. Past tense. Zero emotion commands. Four rules break this film if broken:
> no fuel type is blamed (⛔-03); the grid did not collapse (⛔-02); winterization was recommended,
> not required (⛔-01); 246 is the only death figure stated as fact (⛔-04).

---

## HOOK

【0:00.0–0:20.0 · voiced from frame 0 · Pictures: U001 control room from behind → U002 a hand beside a console telephone → U003 a suburban street half lit → U004 an iced wellhead in open country → U005 a transmission line → U006 the town, dark. Push-in f0→f36, scale 1.06→1.00, Easing.out(Easing.cubic).】

At twenty past one in the morning, in a control room north of Austin, an operator gave an order that had never been given at that scale in American history.
<!-- TX-10 ✓ VERBATIM (01:20 CT, 15 February 2021) · TX-13 ✓ VERBATIM (largest manually controlled load shedding event in US history) -->

Cut the power to twenty thousand megawatts of customers. Now. Before the grid takes itself apart.
<!-- TX-13 ✓ VERBATIM · TX-10 ✓ VERBATIM ("to prevent the risk of a systemwide blackout") -->

It was the correct order.
<!-- TX-10, TX-12 ✓ OURS — the report describes it as preventing a systemwide blackout -->

What nobody in that room could have followed, in the minutes they had, was that the customers about to lose their power included the gas fields that fuelled the plants they were trying to save.
<!-- TX-17 ✓ VERBATIM ("most natural gas production and processing facilities in ERCOT were not identified as critical load, and thus the controlled load shedding took fuel sources offline") -->

【BrandOpening, gold, 3.5 s, over continuing footage.】

---

## OP

【0:20.0–0:52.0 · Pictures: U007 the map ground with the three grids composited → U008 the frequency screen → U009 ice on a live oak branch → U010 black.】

This is a story about a recommendation that was written down and not made a rule.
<!-- TX-06, TX-07 ✓ — thesis line, both rows verbatim -->

Over the next half hour you will see why the state of Texas runs its own electricity grid and answers to nobody outside its borders, what happened the last time this exact weather arrived, how close the whole thing came to going down, and what the grid did to itself trying to stay up.
<!-- OURS — the opening's "what you'll learn", per spec v3 row 10; each clause is answered later -->

Two hundred and forty-six people died.
<!-- TX-26 ✓ VERBATIM · ⛔-04: the state's final figure, and the only one stated as fact -->

And the fix had been in a federal report for ten years.
<!-- TX-05, TX-06 ✓ VERBATIM -->

---

## ACT_1 — THE ISLAND

【0:52.0–5:55.0 · Pictures: U011 a line at dusk · U012 substation through a fence · U013 the straight road to the horizon · U014 the 1930s office · U015 the blank ledger · U016 the blank agreement · U017 the old switchyard · U018 a mid-century city at night · U019 the blank wall map · U021 the pylon from below · U022 iced turbine · U023 iced wellhead · U024 an ordinary street · U030 the week before. Light state B, into A. F01–F14.】

There are three electricity grids in the United States.
<!-- TX-04 ✓ OURS — the standard description of the interconnections, implied by TX-04 -->

One covers the east. One covers the west. And one covers most of Texas, and does not connect meaningfully to either of the other two.
<!-- TX-04 ✓ OURS — restatement of the isolation the row describes -->

That is not geography. It is a decision, and you can date it.
<!-- TX-01, TX-02 ✓ OURS — framing -->

In nineteen thirty-five, the federal government passed a law giving a federal commission authority over electricity sales that crossed state lines.
<!-- TX-01 ✓ VERBATIM ("the Federal Power Act... tasked a regulatory agency with overseeing electricity sales that crossed state lines") -->

The reasoning was ordinary. Electricity was becoming a national business, run by very large holding companies, and somebody outside those companies ought to be able to look at what they charged.
<!-- TX-01 ✓ OURS — plain-language explanation of the law's purpose -->

Texas utilities read the law carefully and noticed the words that mattered. Crossed state lines.
<!-- TX-02 ✓ VERBATIM -->

If no power ever left the state, no sale was interstate. If no sale was interstate, the federal government had nothing to regulate.
<!-- TX-02 ✓ VERBATIM ("If they never sent power across state lines, they were not engaged in interstate commerce, and therefore, the federal government could not regulate their rates or operations") -->

And notice which two things the law reached. Rates, and operations. Not only what you charge. How you run the thing.
<!-- TX-02 ✓ VERBATIM — the row's own two words -->

Because federal jurisdiction over an electricity system is not really a pricing power. It is the authority to say that a system has to be built and run to a standard somebody outside it sets — and to turn up and check that it was.
<!-- TX-01, TX-02 ✓ OURS — plain-language explanation of the jurisdiction the rows describe -->

So keeping the wires inside the border did not just keep Texas rates out of Washington. It kept Texas operations out of Washington, permanently, on every question that would ever arise. And in nineteen thirty-five, when the question on the table was bookkeeping, that looked like a straightforward win.
<!-- TX-02 ✓ OURS — argument; sets the film's spine at minute two -->

So they kept the wires inside the border.
<!-- TX-02 ✓ VERBATIM -->

Think for a second about what that actually requires, because it is not a policy statement. It is a physical arrangement. Every generator, every substation, every transmission line, laid out so that the electricity made in Texas is used in Texas and the machinery never has to shake hands with the machinery next door.
<!-- TX-02 ✓ OURS — plain-language description of what intrastate operation requires; asserts no new fact -->

And a grid is not a pipe. It is one enormous synchronised machine. Joining two of them does not mean opening a tap between them; it means locking every spinning generator on both sides into the same rhythm, permanently, and accepting that a disturbance on one side is now a disturbance on yours.
<!-- OURS — plain-language explanation of synchronous interconnection; asserts no new fact -->

Texas declined the handshake.
<!-- TX-02 ✓ OURS -->

【Re-hook, 2:30 target.】

This was not an accident of history that nobody revisited. The utilities put it in writing, and bound themselves to operating only within the state.
<!-- TX-03 ✓ SECONDARY -->

An agreement is a different object from an oversight. An oversight is corrected by the next person who notices it. An agreement is a thing somebody has to go back and undo, on purpose, and that means somebody has to want to.
<!-- TX-03 ✓ OURS — argument -->

Thirty years later, in nineteen sixty-five, a cascading failure took out the power across much of the north-eastern United States and parts of Canada, and the country decided that grids needed somebody watching them.
<!-- TX-04 ✓ SECONDARY — the 1965 blackout as the row describes it -->

Cascading is worth defining here, because you will need it later in this film. It is what happens when one part of a grid drops out and the electricity it was carrying has to go somewhere. It redistributes onto the lines that are left. Those lines are now carrying more than they were built for, so their own protection disconnects them to save them. The load moves again, onto fewer lines still.
<!-- OURS — plain-language definition of a cascade; asserts no new fact -->

Every step in that sequence is a machine doing exactly what it was designed to do. The sum of them is a region going dark in seconds.
<!-- OURS -->

Five years after that, the Electric Reliability Council of Texas was formed to oversee the Texas grid.
<!-- TX-04 ✓ SECONDARY ("Five years after a 1965 blackout... ERCOT was formed") -->

And it was formed, deliberately, outside the reach of the federal regulator.
<!-- TX-04 ✓ SECONDARY -->

So there is a body responsible for keeping the lights on in Texas, and the rules that body works to are made in Texas. That sounds unremarkable until you ask the follow-up question. What happens when the people who decide the reliability rules conclude that a particular reliability measure costs more than it is worth? In most of the United States there is somebody sitting above that decision. On the question this film is about, in Texas, there was not.
<!-- TX-04, TX-07 ✓ OURS — argument, restating the isolation and setting up Act 2 -->

Now, being an island has a real advantage and it is worth stating plainly, because the film is not going to pretend this was stupid. A grid that answers to one state can be built and changed quickly, without a federal process, and Texas has built an enormous amount of generation very fast.
<!-- OURS — argument; no fact asserted beyond TX-04 -->

That is not a small thing. Permission that takes one state's time rather than a federal process is permission that actually arrives, and the version of the Texas argument worth answering is not "nobody thought about this". It is "we thought about it, and we chose speed."
<!-- OURS — argument; asserts no fact -->

It also has one specific cost, and the cost is the entire second half of this film. When a grid is connected to its neighbours, a shortage can be covered by borrowing. When it is not, the shortage has to be solved inside the fence, or the lights go out.
<!-- OURS — plain-language explanation of interconnection; asserts no new fact -->

【F11: an iced wind turbine and an iced gas wellhead in the same cut, 4.0 s. This is the only time turbines appear.】

One more thing before the cold arrives, because you already have an opinion about this and it is worth setting it down.
<!-- ⛔-03 ✓ — naming the trap -->

Whatever you have heard about which kind of power station failed in Texas, the record does not support a single villain. Freeze-related outages happened across fuel types, and the largest single problem was not a type of plant at all. It was fuel that could not get to the plants.
<!-- TX-16 ✓ VERBATIM · ⛔-03 -->

That answer is inconvenient for everybody, which is usually a sign that it is the real one. It does not hand the people who dislike wind turbines the film they were hoping for, and it does not hand the people who dislike gas that film either.
<!-- TX-16 ✓ OURS — argument · ⛔-03 -->

What it hands you instead is a supply chain, a list, and a decision taken in twenty eleven.
<!-- TX-16, TX-17, TX-06 ✓ OURS — sets the three acts that follow -->

That is where this is going. Hold on to it.
<!-- OURS -->

---

## ACT_2 — THE RECOMMENDATION

【5:55.0–11:30.0 · Pictures: U031 a street under thin snow, ten years older · U032 rime on plant pipework · U033 the empty hearing room · U034 the blank report · U035 the blank page held · U036 pipe lagging being wrapped · U037 heat-trace cable · U039 the empty chair · U040 blank binders · U041 the blank calendar · U042 the training room · U046 the corridor · U048 the road across flat land. F15–F28.】

In two thousand and eleven, Texas got weather like this.
<!-- TX-05 ✓ VERBATIM -->

Not as long and not as deep, but the same kind: a hard freeze reaching further south than the equipment was built for.
<!-- TX-05, TX-09 ✓ OURS — restatement -->

Power plants tripped offline. Rolling blackouts were ordered. And afterwards, the federal energy regulator and the organisation that writes American grid reliability standards went and looked at why.
<!-- TX-05 ✓ VERBATIM ("Texas experienced extreme cold weather in 2011... a joint federal inquiry followed") -->

They produced a report, and the report made a recommendation.
<!-- TX-06 ✓ VERBATIM -->

It recommended the development of winterization standards.
<!-- TX-06 ✓ VERBATIM QUOTE ("recommended development of winterization standards") -->

【Silence 10 frames. Then the pipe lagging.】

It is worth being concrete about what winterization is, because it is not exotic.
<!-- OURS — framing -->

It is insulation wrapped around pipework that carries water or condensate. It is electrical heating tape run along the outside of a pipe to keep what is inside it above freezing. It is windbreaks around instrument panels. It is heaters in the small enclosures where sensing lines live, because a sensing line freezing is enough to make a power station think something is wrong and shut itself down.
<!-- OURS — plain-language description of the measures the row names; asserts no new fact -->

It is not difficult engineering. It is ordinary work, and it costs money, and it has to be done to every unit whether or not that unit ever sees the cold.
<!-- OURS -->

The recommendation was made. And then this happened.
<!-- TX-06, TX-07 ✓ — framing -->

【Re-hook, 8:00 target. Cut to black for 8 frames. B1 kinetic: the recommendation types on; DECLINED masks up beneath it, 3.5 s.】

The standards organisation ultimately declined to act on it.
<!-- TX-07 ✓ VERBATIM ("NERC ultimately declined to act on that") -->

There is no drama in that sentence and that is exactly the problem. Nobody refused in a room with a table. A recommendation was made, it was considered, and it did not become a standard.
<!-- TX-07 ✓ OURS — restatement · ⛔: no individual named -->

It is worth being exact about those two words, recommendation and standard, because the entire film turns on the distance between them.
<!-- TX-06, TX-07 ✓ — framing -->

A recommendation is a document. It says: here is what we found, and here is what we think should be done about it. Nobody audits a recommendation. Nobody is penalised for not following one. It is published, and the people who read it and act on it are largely the people who were going to do the work anyway.
<!-- TX-06 ✓ OURS — plain-language explanation of the term the row uses -->

A standard is a rule with a mechanism behind it. It has a number. Somebody comes and checks. If the work has not been done there is a penalty, and the penalty is set high enough that doing the work is the cheaper option.
<!-- TX-06, TX-40 ✓ OURS — plain-language explanation; the penalty structure is TX-40's, arriving in Act 5 -->

The twenty eleven report asked for the second thing. What existed after it was the first thing.
<!-- TX-06, TX-07 ✓ OURS — restatement -->

And you can see how that happens without anyone in the story being a villain.
<!-- OURS — framing -->

Winterizing a power station costs money now, for a benefit that only arrives in weather that might not come for a decade. The plant that spends the money is not paid any more for having spent it. In a market that pays for electricity delivered rather than for readiness to deliver it, that spending is pure cost.
<!-- OURS — argument; asserts no fact -->

And every operator running that calculation is running it alone, knowing that the value of their own preparation depends on everyone else having prepared too. A winterized plant in a state that has gone dark is a machine with nowhere to send its power.
<!-- OURS — argument -->

Which is precisely the situation a standard exists to resolve. It takes the decision away from the party who carries the cost, and gives it to the system that carries the consequence.
<!-- OURS — argument -->

The federal regulator's chairman said afterwards, in plain terms, that the twenty eleven recommendations were not acted on.
<!-- TX-08 ✓ VERBATIM -->

What did happen instead was reminders. Every year, through regional workshops, generators were reminded about cold weather preparation.
<!-- TX-09 ✓ VERBATIM ("annual reminders via Regional Entity workshops") -->

A workshop is a good thing and this is not a sneer at it. People attend, people learn, and some of them go back and do the work. What a workshop cannot do is reach the operator who did not attend, or bind the operator who did attend and then decided against the spending. It informs. It does not require. And nothing about it changes on the day somebody decides not to act on it.
<!-- TX-09 ✓ OURS — plain-language explanation of the mechanism the row names -->

And here is the measurement that tells you what a reminder is worth. When February twenty twenty-one arrived, generating units failed from freezing **above their own stated ambient design temperature**.
<!-- TX-09 ✓ VERBATIM ("generating units experienced freeze-related outages above the unit's stated ambient design temperature") -->

Read that again. Not below the temperature the unit was built to survive. Above it.
<!-- TX-09 ✓ OURS — restatement -->

The machines were failing in weather they were rated for.
<!-- TX-09 ✓ OURS -->

Give that one more turn, because it is the most damning measurement in the whole report and it is easy to hear it as a technicality.
<!-- TX-09 ✓ — framing -->

Every generating unit has an ambient design temperature. That is not a marketing figure. It is the engineering statement of the coldest air the machine was built to go on working in.
<!-- TX-09 ✓ OURS — plain-language explanation of the term the row uses -->

A unit that fails below that temperature is a unit meeting its specification and being asked for more than it promised. That is weather beating equipment, and it is nobody's fault.
<!-- TX-09 ✓ OURS -->

A unit that fails above it is a unit that is not meeting its specification at all. And that is what the report found, in twenty twenty-one, after ten years of annual reminders.
<!-- TX-09 ✓ OURS — restatement -->

Ten years passed between the report and the storm.
<!-- TX-05, TX-10 ✓ OURS — arithmetic -->

---

## ACT_3 — FOUR MINUTES AND TWENTY-THREE SECONDS

【11:30.0–18:10.0 · Pictures: U049 the cloud mass · U050 first snow on brown grass · U051 flat farmland under thin snow · U052 the strip-mall car park · U053 the frozen fountain · U054 the iced pool · U055 the iced sprinkler · U056 snow in a pickup bed · U057 the control room working · U058 the screen wall · U059 the frequency trace (hero) · U061 the clock · U062 the street going dark · U063 the dead traffic signal · U064 the breaker panel and torch · U065 the candle · U066 the blanket over the doorway · U067 breath indoors · U072 the unshovelled driveway · U079 four days. Light state A throughout. F29–F44.】

The storm came down through the middle of the country in the second week of February.
<!-- TX-10 ✓ OURS — framing; the date is the row's -->

In Texas it did the thing Texas is not built for. It got cold, and it stayed cold, for days, across the entire state at once.
<!-- TX-14 ✓ OURS — restatement of the duration and extent -->

That last part is the part that matters. A grid handles a cold snap in one region by leaning on another region. There was no other region.
<!-- TX-02, TX-04 ✓ OURS — restatement of the isolation -->

Demand rose for a reason that is not obvious to anyone who lives somewhere cold, and it is worth a moment.
<!-- OURS — framing -->

In much of the United States a house is heated by burning something. Gas, oil. The electricity only runs the fan. In Texas, a great many houses are heated by the electricity itself — by a heat pump, which moves warmth from the outside air into the house, and by resistance heating that takes over when it gets cold enough that there is no warmth outside left to move.
<!-- OURS — plain-language description of electric heating; asserts no new fact -->

Which means that in Texas, cold weather does not merely make people turn the heating on. It makes the electricity demand of every one of those houses climb steeply, at the exact hour the machines are least able to meet it. A grid built around a summer peak was being asked for a winter one.
<!-- OURS — argument; asserts no fact -->

Demand rose. Generation fell. Plants that were running began to trip offline, and plants that were meant to start could not.
<!-- TX-09, TX-16 ✓ OURS — restatement -->

At twenty past one on the morning of the fifteenth, the grid operator ordered load shedding.
<!-- TX-10 ✓ VERBATIM -->

Load shedding is the polite phrase. What it means is that the operator chooses which customers lose power, and cuts them off, on purpose, to keep the system standing.
<!-- TX-10 ✓ OURS — plain-language definition -->

It is not a failure. It is the thing you do so that the failure does not happen.
<!-- TX-10, TX-12 ✓ OURS -->

And it is worth being clear about what that room actually looks like when the order is given, because it is not a room with a red telephone in it.
<!-- TX-10 ✓ — framing -->

It is a room of screens, and on the screens are numbers, and the numbers are moving in one direction. There is the generation the operator has. There is the demand the state is asking for. And the gap between the two is widening every few minutes as another unit drops off.
<!-- TX-10 ✓ OURS — plain-language description; asserts no fact beyond the row -->

The operator cannot make a power station start. Nobody in that room can build capacity in the next hour, or borrow it from a neighbour, because there is no neighbour. The only variable that operator controls is how much of the state is permitted to draw.
<!-- TX-02, TX-04, TX-10 ✓ OURS — restatement of the isolation, now operational -->

So the order is given. At twenty past one in the morning. And the people it reaches are asleep.
<!-- TX-10 ✓ OURS -->

【F34 number ticker: 0 → 20,000, 24 frames, label "megawatts of customers cut off".】

Twenty thousand megawatts were shed.
<!-- TX-13 ✓ VERBATIM -->

It was the largest manually controlled load shedding event in the history of the United States.
<!-- TX-13 ✓ VERBATIM QUOTE -->

And it was not enough. Through that hour, plants kept failing, and the operator kept shedding, and something began happening to the grid that has a number attached to it.
<!-- TX-11 ✓ OURS — framing -->

【Re-hook, 14:00 target. B2: the frequency trace, f0→f240, 60.0 → 59.3 Hz, Easing.inOut(Easing.quad), bed −6 dB. No narration for 4.0 s.】

An alternating current grid runs at a fixed frequency. In North America that is sixty cycles a second, and it is not a target, it is a physical consequence: the generators are all spinning together, locked to each other, and the frequency is how fast they are spinning.
<!-- OURS — plain-language explanation of grid frequency -->

When demand exceeds what the machines can supply, they are pulled down. They slow. The frequency falls.
<!-- OURS -->

And every generator on the system carries protection that disconnects it if the frequency stays too low for too long, because running a machine that size below its design speed will destroy it.
<!-- TX-12 ✓ OURS — the mechanism the row's consequence implies -->

That morning, the frequency of the Texas grid fell below fifty-nine point four hertz, and stayed there for four minutes and twenty-three seconds.
<!-- TX-11 ✓ VERBATIM ("pushing grid frequency below 59.4 Hz for four minutes and 23 seconds") -->

【B3: two bars — the short one filling to 4:23, the long one waiting at 9:00. Held 5.0 s. Not a countdown; a margin.】

The line was nine minutes.
<!-- TX-12 ✓ VERBATIM ("Had the grid's frequency remained below 59.4 Hz for nine minutes or more") -->

Had it stayed below that frequency for nine minutes or more, more generation would have tripped.
<!-- TX-12 ✓ VERBATIM -->

And that is the point at which the words change. Not blackouts. A system-wide shutdown, cutting power to millions more, significantly slowing restoration, and damaging units across the grid.
<!-- TX-12 ✓ VERBATIM QUOTE -->

Damaging units across the grid. That is the phrase to hold on to, because it is what makes the difference between days and weeks. A grid that sheds load can be brought back when the machines are ready. A grid that trips its machines has to repair them first.
<!-- TX-12 ✓ OURS — restatement -->

And there is a quieter consequence in that sentence that is easy to read past. Significantly slowed restoration.
<!-- TX-12 ✓ VERBATIM QUOTE — the phrase, isolated -->

Bringing a grid back from a total shutdown is not a switch. Most power stations need electricity in order to start: to turn the shaft, to run the pumps, to drive the controls. In a state where everything is off, that electricity has to come from somewhere. It comes from a small number of units that can start themselves without help, which then energise a path to the next unit, and the next, in stages, each of which has to hold before the following one is attempted.
<!-- TX-12 ✓ OURS — plain-language explanation of the restoration the row calls "significantly slowed" -->

That is the difference between a grid that sheds load and a grid that goes down. One of them is waiting. The other is rebuilding itself, in the cold, with the clock running in every unheated house in the state.
<!-- TX-12 ✓ OURS — restatement -->

Texas got to within four minutes and thirty-seven seconds of that.
<!-- TX-11, TX-12 ✓ OURS — arithmetic: nine minutes less four minutes twenty-three seconds -->

【Silence 12 frames.】

More than four and a half million people lost power.
<!-- TX-14 ✓ VERBATIM -->

Some of them for four days.
<!-- TX-14 ✓ VERBATIM -->

And in most of those houses, what the cold did first was not dramatic. The heating stopped. The house held its warmth for a few hours and then began giving it up through the walls, because the walls were built for July.
<!-- OURS — plain-language description; no fact asserted -->

Then the sequence, in the order it arrives. The lights go, and it is an inconvenience. The heating goes, and it is uncomfortable. The phone battery goes, and it starts to be frightening — because the phone was the only thing still telling you how long this was going to last. And then the taps go, and it stops being a power cut.
<!-- OURS — the film's own reconstruction, not attributed to any individual · ⛔-05 -->

By the second day people were living in one room, under everything they owned, with the doorways hung with blankets. Cars were being run in driveways for twenty minutes at a time, to charge a phone and get warm. Food was being kept cold on a back step, which was the one thing the weather was good for.
<!-- OURS — the film's own reconstruction, not attributed to any individual · ⛔-05 -->

And in some houses that went on for four days.
<!-- TX-14 ✓ VERBATIM -->

---

## ACT_4 — THE LOOP

【18:10.0–24:40.0 · Pictures: U081 the gas field under snow · U082 the iced wellhead (hero) · U083 the iced gauge · U084 the frozen separator · U085 the compressor station lit · U086 the same, dark · U089 the blank critical-load list (hero) · U090 the blank page held · U091 the disconnect switch · U092 the loop ground · U093 the plant with no vapour · U096 the water plant · U098 the brown tap · U099 the bathtub filling · U100 the stripped shelf. F45–F60.】

Now we go to the other end of the wire.
<!-- OURS — framing -->

Most of the electricity that Texas burns in a cold snap is made from natural gas, and natural gas is not stored at the power station. It arrives, continuously, through pipes, from wells.
<!-- OURS — plain-language explanation -->

During the storm, gas production in Texas fell by about forty-five per cent.
<!-- TX-15 ✓ SECONDARY -->

Close to half the fuel, gone, in the week the state was asking for more of it than it had ever asked for.
<!-- TX-15 ✓ OURS — restatement -->

The federal report broke down why, and the two numbers are worth hearing separately.
<!-- TX-16 ✓ — framing -->

Forty-three point three per cent of the fuel supply problem was caused by freezing temperatures and weather.
<!-- TX-16 ✓ VERBATIM -->

Wellheads freeze. Water is produced along with gas, and where that water sits in a valve or a line and the temperature drops far enough, it becomes ice, and the well stops.
<!-- TX-16 ✓ OURS — plain-language description of a freeze-off -->

That is weather doing what weather does to equipment nobody insulated.
<!-- TX-16, TX-06 ✓ OURS -->

And then there is the second number, and it uses three words that are worth ten seconds of your time, because between them they are the whole gas chain.
<!-- TX-16 ✓ — framing -->

The wellhead is where gas comes out of the ground. Gathering is the web of small pipes that collects it from hundreds of scattered wells and brings it to one place. Midstream is what happens next: the processing that takes water and other liquids out of the gas, and the compression that pushes what remains down a large pipe at pressure.
<!-- TX-16 ✓ OURS — plain-language explanation of the terms the row uses -->

And every one of those stages runs on electricity. Not a trickle of it. Compression in particular is a heavy electrical load, because what it is doing is physically hard: making a gas take up less room so that it will move.
<!-- TX-16 ✓ OURS — plain-language explanation; asserts no new fact -->

Twenty-one point five per cent of the fuel supply problem was caused by power losses at midstream, wellhead or gathering facilities.
<!-- TX-16 ✓ VERBATIM -->

Power losses. The gas stopped because the electricity stopped.
<!-- TX-16 ✓ OURS — restatement -->

【F49 hero: the blank critical-load list under a lamp, 4.5 s.】

Every grid keeps a list. It is called critical load, and it is the set of customers who do not get shed no matter what: hospitals, water plants, emergency services, and the infrastructure the grid itself depends on.
<!-- TX-17 ✓ OURS — plain-language definition of the term the row uses -->

Being on that list is not a courtesy. It is the difference between having power in an emergency and not having it.
<!-- TX-17 ✓ OURS -->

And the list is not a judgement about who matters. It is an operational document, written in advance, in calm weather, by people trying to answer one question: what does this grid need in order to keep running?
<!-- TX-17 ✓ OURS — plain-language explanation of the term the row uses -->

Which means the list is only ever as good as the imagination of the people writing it.
<!-- TX-17 ✓ OURS — argument -->

The obvious answers are on it. Hospitals. Water treatment. Emergency dispatch. The substations and control rooms of the grid itself.
<!-- TX-17 ✓ OURS — restatement of the categories the row implies -->

And then there is the answer that is not obvious at all, right up until the moment it is catastrophic.
<!-- TX-17 ✓ — framing -->

Most natural gas production and processing facilities in Texas were not identified as critical load.
<!-- TX-17 ✓ VERBATIM ("Most natural gas production and processing facilities in ERCOT were not identified as critical load") · the film's turn -->

【Re-hook, 20:30 target. B4: the loop drawn once — grid, load shed, gas — arrows closing the circle, 5.0 s. Drawn once in the whole film.】

So when the operator shed twenty thousand megawatts to save the grid, some of what went dark was the gas industry that fuelled it.
<!-- TX-17 ✓ VERBATIM ("thus the controlled load shedding took fuel sources offline") -->

Compressor stations stopped. Processing plants stopped. Wells that needed power stopped.
<!-- TX-16, TX-17 ✓ OURS — restatement -->

Which took fuel sources offline.
<!-- TX-18 ✓ VERBATIM -->

Which forced further load shedding.
<!-- TX-18 ✓ VERBATIM ("forcing further load shedding") -->

That is the loop, and it is not a metaphor. It is the sequence the federal report describes. The grid cut power to save itself, the power it cut fed the fuel system, the fuel system stopped, and the grid had to cut more.
<!-- TX-17, TX-18 ✓ OURS — restatement of two verbatim rows -->

Walk it once slowly, because the speed of it is the whole problem.
<!-- OURS — framing -->

The grid loses generation and sheds load to hold its frequency up. Somewhere inside the load it sheds is a compressor station, pushing gas along a pipe. The compressor stops. The pressure in that pipe begins to fall. And a gas-fired power station somewhere down the line — one that was running, one that nobody shed, one that no operator made any decision about at all — finds that its fuel is arriving at a pressure it cannot use, and comes off the grid.
<!-- TX-17, TX-18 ✓ OURS — restatement of the mechanism the two verbatim rows describe -->

The grid has now lost generation it never chose to lose, because of a decision it took minutes earlier to save itself. And the response to losing generation is to shed more load.
<!-- TX-18 ✓ OURS — restatement -->

Nobody in that chain did anything wrong at the moment they did it. That is what makes it a loop and not a mistake.
<!-- TX-17, TX-18 ✓ OURS — argument -->

Some facilities were shut in deliberately, to stop them freezing. Others were taken offline by frozen equipment. Others simply lost their electricity.
<!-- TX-19 ✓ VERBATIM -->

Shutting in is worth understanding, because it reads like a failure and it is the opposite of one. If you can see that a well is about to freeze and be damaged, you close it yourself, in a controlled way, so that you still have a well to reopen afterwards.
<!-- TX-19 ✓ OURS — plain-language explanation of the term the row uses -->

Which is the same logic as load shedding, one industry along. Accept the small loss now, to avoid the permanent one.
<!-- TX-19, TX-10 ✓ OURS — the film's connection between two rows -->

And that is the sentence this act exists for. At the same hour, in the same weather, two industries were each doing the disciplined, correct, defensible thing — and each one's correct decision was making the other one's problem worse.
<!-- TX-17, TX-18, TX-19 ✓ OURS — restatement -->

【Beat. Then the water.】

And then the water went.
<!-- TX-25 ✓ — framing -->

Water treatment is electrical. Pumps, filtration, pressure. When a treatment plant loses power it stops moving water, and when a pipe network loses pressure it stops being safe, because anything outside the pipe can get in.
<!-- TX-25 ✓ OURS — plain-language explanation -->

Pipes froze and burst — in a state where a great many water pipes run through unheated attics and along outside walls, because they were never expected to need protecting.
<!-- TX-25 ✓ VERBATIM ("pipes froze and leaked") + OURS on the construction -->

Nearly fifteen million Texans had their main source of drinking water disrupted.
<!-- TX-21 ✓ VERBATIM -->

One thousand one hundred and five boil-water notices were issued, covering about fourteen and a half million people.
<!-- TX-22 ✓ VERBATIM -->

Of the roughly half of the state that lost running water altogether, the average outage was fifty-two hours.
<!-- TX-24 ✓ VERBATIM ("Of the 49 percent of Texans who lost running water, their average disruption was 52 hours") -->

And on the sixteenth of February, one point four million people still had no reliable drinking water.
<!-- TX-23 ✓ VERBATIM — the number only; the source's own interval is inconsistent and is not narrated -->

A boil-water notice, in a house with no electricity, is an instruction to boil water on a stove that may not light, in a pot filled from a tap that may not run.
<!-- TX-22, TX-25 ✓ OURS — restatement -->

And a water system does not come back at the moment the power does. A network that has lost its pressure has to be refilled, and flushed, and tested before a notice can be lifted, and none of those steps is instant. Which is why the water outages outlast the power outages, and why the average was fifty-two hours rather than four.
<!-- TX-24, TX-25 ✓ OURS — plain-language explanation of the restoration behind the row's 52-hour average -->

---

## ACT_5 — THE PRICE

【24:40.0–29:20.0 · Pictures: U106 the thaw · U107 the number ground · U108 the emptied room with one chair · U109 the blank statement and the face-down phone · U110 hands flat on a table · U111 the utility office, nobody there · U112 the empty chamber · U113 the blank bill · U114 the blank map board · U116 new lagging · U117 new heat trace · U118 the same field in summer. Light state B. F61–F75.】

The Texas Department of State Health Services counted the dead six times, and each count was larger than the one before.
<!-- TX-29 ✓ SECONDARY -->

In March of twenty twenty-one the figure was a hundred and eleven. By July it was two hundred and ten.
<!-- TX-29 ✓ SECONDARY -->

The sixth and final report, in January of twenty twenty-two, put it at two hundred and forty-six.
<!-- TX-26 ✓ VERBATIM -->

【F61: 246 holds longer than any other card in the film. 5.0 s. No motion but the ambient bed.】

Close to two-thirds of them died of hypothermia.
<!-- TX-27 ✓ VERBATIM -->

The rest: ten per cent from the worsening of an illness they already had, nine per cent in motor vehicle accidents, eight per cent from carbon monoxide poisoning, four per cent in fires, four per cent from falls.
<!-- TX-28 ✓ VERBATIM -->

Carbon monoxide is what happens when people try to heat a house with something that was not meant to heat a house, or sit in a running car in a closed garage to get warm.
<!-- TX-28 ✓ OURS — plain-language explanation · ⛔-05: no individual described -->

And look at what that list is. Hypothermia. Carbon monoxide. Fires. Falls. An illness someone already had, getting worse.
<!-- TX-27, TX-28 ✓ OURS — restatement -->

Not one of those causes is electrical. The power going off did not kill anybody. What killed people was what a house becomes, and what people do inside it, once the power has been off for long enough.
<!-- TX-27, TX-28 ✓ OURS — argument -->

Some analysts believe the true figure is much higher. One outlet reported, when the official count stood at a hundred and fifty-one, that the real number was likely four or five times what the state had acknowledged.
<!-- TX-30 ✓ SECONDARY · ⛔-04: attributed and labelled -->

This film uses the state's number, because it is the state's number, and says plainly that the question is not settled.
<!-- AB-03 ✓ — declared absence -->

【Re-hook, 27:00 target. Cut to the blank statement.】

Then the bills arrived.
<!-- TX-31 ✓ — framing -->

During the emergency, the Texas utility regulator set the wholesale price of electricity at the system-wide cap. Nine thousand dollars per megawatt-hour.
<!-- TX-31 ✓ VERBATIM -->

For scale, that is a price meant to exist for minutes, as a signal to anyone who can generate that they should generate right now. It ran for days.
<!-- TX-31 ✓ OURS — plain-language explanation of a scarcity price cap -->

Most Texans are insulated from that by a fixed-rate contract. Some were not, because they had signed up to plans that passed the wholesale price straight through, which in an ordinary month is cheaper.
<!-- TX-32 ✓ OURS — plain-language explanation of the plan type the row implies -->

Some of those households received bills of seventeen thousand dollars.
<!-- TX-32 ✓ SECONDARY -->

That retailer later settled with the state, and its customers were released from the bills.
<!-- TX-33 ✓ SECONDARY -->

The wider cost did not go away, it moved. One analysis published that June put the excess energy costs loaded onto Texas ratepayers at nearly thirty-eight billion dollars.
<!-- TX-34 ✓ SECONDARY -->

The pricing decision itself went to court. An appeals court held that the regulator had set prices too high; the state's supreme court subsequently affirmed the regulator's orders.
<!-- TX-35 ✓ SECONDARY — verify the final posture before publish -->

As for what the storm cost the state in total, this film is not going to give you a number, and it is worth saying why rather than just leaving it out. Loss estimates cited by the Federal Reserve Bank of Dallas ranged from eighty billion dollars to a hundred and thirty billion. A separate figure of over a hundred and ninety-five billion also circulates. They are estimates, they are not reconciled with each other, and choosing the one you like best is how a number stops being evidence and becomes an argument.
<!-- TX-36 ✓ SECONDARY · ⛔-06: both ranges given, both attributed, neither adopted -->

【Beat.】

Then the report came, and the report was not thin.
<!-- TX-20 ✓ — framing -->

The federal inquiry into February twenty twenty-one made twenty-eight formal recommendations — among them, revisions to the reliability standards on generator winterization, and on gas–electric coordination.
<!-- TX-20 ✓ VERBATIM -->

Which is to say that the second report asked for the thing the first report had asked for, and added the part the first one had not seen: that the gas system and the electricity system are not two systems. They are one, and they had better be planned as one.
<!-- TX-20, TX-06 ✓ OURS — the film's connection between two verbatim rows -->

And the legislature did the thing that had been recommended ten years earlier.
<!-- TX-37, TX-06 ✓ — framing -->

Senate Bill Three required the state's oil and gas regulator to make rules requiring critical facilities to weatherize their equipment.
<!-- TX-37 ✓ VERBATIM -->

Not power stations only. The gas supply chain: the wells, the processing, the storage, the pipelines that feed the generators.
<!-- TX-38 ✓ VERBATIM -->

A committee was created to identify the critical infrastructure and to map the state's electricity supply chain, and to update that map at least once a year.
<!-- TX-39 ✓ VERBATIM -->

Which is to say: somebody now has to keep the list that the gas fields were not on.
<!-- TX-17, TX-39 ✓ OURS — the film's own connection between two verbatim rows -->

Penalties run from five thousand dollars per violation per day to one million dollars per violation per day.
<!-- TX-40 ✓ VERBATIM -->

There is the difference between a recommendation and a standard, expressed in dollars per day.
<!-- TX-40, TX-06, TX-07 ✓ OURS — closes the Act 2 argument -->

It did not arrive clean. In September of twenty twenty-one, Texas senators publicly criticised the regulator over a winterization exemption — one that lawmakers had themselves written into the law whose enforcement they were complaining about.
<!-- TX-42 ✓ SECONDARY · ⛔-07: narrated as those senators' criticism, not as a finding -->

And the rules themselves were adopted on the thirtieth of August, twenty twenty-two.
<!-- TX-41 ✓ VERBATIM -->

Eleven years, five months and nineteen days after the report that recommended them.
<!-- TX-05, TX-41 ✓ OURS — arithmetic from the 2011 event to 30 August 2022 -->

---

## ENDING

【29:20.0–30:20.0 · Pictures: U119 the transmission line in ordinary weather · U120 the empty bathtub, held 9.0 s with ambient motion only · then BrandEndcard. No typography over the bath.】

So here is what the record holds.
<!-- OURS -->

A grid deliberately built to answer to nobody outside one state. A recommendation, ten years old, that was never made a standard. Machines that failed in weather they were rated for. An order to cut power that was correct, and that cut the fuel supply of the plants it was protecting. Four minutes and twenty-three seconds of margin. Two hundred and forty-six people.
<!-- TX-02, TX-06, TX-07, TX-09, TX-10, TX-17, TX-11, TX-26 ✓ — each clause restates a row -->

No individual was ever established as the cause of it.
<!-- AB-01 ✓ — established absence -->

And there is a question this film will not answer, which you should hear stated rather than left to hang. Whether winterizing to the twenty eleven recommendation would have stopped this particular storm doing what it did is not a finding anywhere in the record. The report recommends standards. It does not run the counterfactual, and neither will we.
<!-- AB-02 ✓ — declared absence -->

What the record does establish is narrower and, if anything, worse. The measure was identified. It was written down. It was not made a rule. And when the weather came back, the machines failed in conditions they were rated for.
<!-- TX-06, TX-07, TX-09 ✓ OURS — restatement of three rows -->

【The bathtub.】

In the days before the storm, Texans were told to fill their bathtubs.
<!-- TX-21, TX-25 ✓ OURS — the standard instruction the water failure made necessary -->

It is sensible advice and it is worth noticing what it is. It is a public authority telling several million people that the water in their walls is about to become unreliable, and that the plan is a bathtub.
<!-- OURS — argument -->

Every system you depend on has a version of the bathtub. It is the point at which the system stops being a system and becomes your problem.
<!-- OURS — second-person turn -->

And what decides where that point sits is not the weather. It is a set of decisions taken years earlier by people who will not be there when it arrives — about what is on the critical list, about which recommendation becomes a rule, and about who is allowed to look.
<!-- TX-17, TX-06, TX-07, TX-02 ✓ OURS — restatement -->

【CTA over the endcard: "If this changed how you look at the switch on your wall, subscribe — that is the whole series."】
