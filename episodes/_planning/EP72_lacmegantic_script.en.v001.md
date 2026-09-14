# EP72 · LAC-MÉGANTIC — SCRIPT v001

> **Design `EP72_lacmegantic_FILM_BIBLE.v001.md` · facts `EP72_lacmegantic_FACTS_LEDGER.v001.md`
> (the only source of any factual line) · contract
> `episodes/PD-2026-072-lacmegantic/episode_spec.v001.json` (`script_words` **[4600, 4800]**,
> `runtime_seconds` **[1740, 1920]**).**
>
> **Citation convention.** Every factual line is followed on the next line by an HTML comment
> carrying its ledger row id. The comment sits on its own line: the narration extractor skips a line
> beginning `<!--`, but a trailing inline comment is tokenised into the word count.
>
> **Register.** Declarative. Past tense. No adjective the record does not carry. Zero emotion
> commands. The two rules that break this film if broken: **three men were tried and all three were
> acquitted** (⛔-01), and the number of hand brakes needed is **never a single figure** (⛔-04).
>
> **Timestamps in the production notes are DESIGN TARGETS at 173 wpm. Re-derive every one of them
> from the delivered ElevenLabs master before captions are locked.**

---

## HOOK

【0:00.0–0:21.0 · voiced from frame 0 · Pictures: a dark railway line behind houses, one window lit → flame on the front of a parked locomotive, distant → boots on gravel → a hand on a valve → wide, tank cars standing in a line under yard lights → the town below, asleep. Push-in f0→f36, scale 1.06→1.00, Easing.out(Easing.cubic), Trail 6 layers decaying to f18. No face resolves.】

Ten minutes to midnight, in a village called Nantes, a woman looked out at the railway line behind her house and saw flames on the front of a parked locomotive.
<!-- LM-06 ✓ VERBATIM ("at about 2350, a local resident reported a fire on the lead locomotive (MMA 5017) to the 911 emergency call centre") -->

She called 911.
<!-- LM-06 ✓ VERBATIM -->

The firefighters who arrived did exactly what they were trained to do, and they did it correctly.
<!-- LM-07 ✓ OURS — characterisation of the actions in LM-07 as trained procedure; the actions themselves are verbatim -->

What nobody standing in that yard knew was that the engine they were about to switch off was the only thing holding seventy-two tank cars of crude oil on the hill above a sleeping town.
<!-- LM-01, LM-04, LM-08 ✓ — the causal link is the report's own: with the locomotives shut down the compressor no longer supplied the air brake system -->

【BrandOpening lands here, gold, 3.5 s, over continuing footage. Motion does not stop.】

---

## OP

【0:21.0–0:52.0 · Pictures: the grade drawn as a line falling left to right → the polymer patch, held → the brake wheel → black.】

This is a story about a repair, a test, and a shift that ended.
<!-- OURS — thesis line, no fact asserted -->

Everything in it was signed off by somebody. The repair was approved. The train was secured according to the railway's own rules. The test that checked the securement was the test the railway specified. The operation itself had been approved by the country's transport regulator.
<!-- LM-21, LM-09, LM-11, AB-03 ✓ — each clause is a ledger row; the sentence asserts approval, not adequacy -->

At the end of it, forty-seven people were dead, and eighteen separate things had gone wrong.
<!-- LM-16 ✓ VERBATIM · LM-24 ✓ VERBATIM ("18 distinct causes and contributing factors") -->

The question this film is about is not who to blame. It is how a system can be arranged so that every step is somebody's job, and the whole thing is nobody's.
<!-- OURS — controlling idea, no fact asserted -->

---

## ACT_1 — THE REPAIR

【0:52.0–5:40.0 · Pictures: a locomotive shop at night · an engine block opened · the grey patch going in · a torque wrench · the locomotive leaving under its own power · a route map · tank cars filling. Cut mean 3.8 s. F01–F13.】

In October of 2012, eight months before any of this, the locomotive at the front of that train failed.
<!-- LM-20 ✓ VERBATIM ("In October 2012, eight months before the Lac-Mégantic accident, the lead locomotive was sent to MMA's repair shop following an engine failure") -->

It went to the railway's own repair shop.
<!-- LM-20 ✓ VERBATIM -->

A diesel locomotive engine is not a car engine. The block is a structure. When something inside it breaks, the repair is a heavy one: the engine comes apart, the damaged section is machined or replaced, and the locomotive sits out of service while that happens.
<!-- OURS — plain-language explanation of the repair class described in LM-20 and LM-21; asserts no new fact -->

That costs two things a railway does not like spending. Time, and money.
<!-- LM-21 ✓ VERBATIM ("Given the significant time and cost of a standard repair") -->

There was also pressure to get the locomotive back into service.
<!-- LM-21 ✓ VERBATIM ("and the pressure to return the locomotive to service") -->

So the engine was repaired with an epoxy-like material.
<!-- LM-21 ✓ VERBATIM ("the engine was repaired with an epoxy-like material") -->

The investigation's own words for that material are worth hearing exactly. It lacked the strength and the durability required for this use.
<!-- LM-21 ✓ VERBATIM QUOTE ("which did not have the strength and durability required for this use") -->

【F04 hero: the patch, 4.0 s hold, ambient bed only, no music stab.】

Inside that repair, a bearing was seated. When the bolt holding it was tightened, it was tightened too far.
<!-- LM-22 ✓ VERBATIM ("The cam bearing had fractured when the mounting bolt was over-tightened after the cam bearing had been installed as part of a non-standard repair to the engine block") -->

The bearing cracked.
<!-- LM-22 ✓ VERBATIM -->

Nothing happened. That is the part that matters. The locomotive went back out and worked for eight months, and at no point in those eight months did anybody looking at it have a reason to think it was carrying a fracture.
<!-- LM-20, LM-22, LM-23 ✓ OURS — the interval is LM-20's own eight months; the failure sequence is LM-23 -->

What a cracked cam bearing does is quiet and slow. It reduces the oil reaching the valves at the top of one power assembly.
<!-- LM-23 ✓ VERBATIM ("Failure of the cam bearing reduced the engine oil supply to the valve train at the top of the associated power assembly") -->

Less oil means more heat and more wear. The valves were damaged. Eventually a piston crown was punctured.
<!-- LM-23 ✓ VERBATIM ("The decreased lubrication led to valve damage and eventually to a punctured piston crown") -->

A punctured piston lets oil past. The oil went where the exhaust goes, which is into the turbocharger.
<!-- LM-23 ✓ VERBATIM ("Eventually, oil began to accumulate in the body of the turbocharger") -->

A turbocharger is driven by exhaust gas and it runs hot enough to glow.
<!-- OURS — plain-language explanation of the component named in LM-23 -->

So oil collected in a hot metal casing for eight months, and on the night of the fifth of July, twenty thirteen, it caught fire.
<!-- LM-23 ✓ VERBATIM ("where it overheated and caught fire on the night of the derailment") -->

【Re-hook, 2:30 target: the sentence below runs over a hard cut to the tank cars filling.】

That is what was at the front of the train. Behind it, that night, were seventy-two tank cars.
<!-- LM-01 ✓ VERBATIM ("72 Class 111 tank cars") -->

They had been loaded at New Town, in North Dakota, with petroleum crude oil.
<!-- LM-01 ✓ VERBATIM ("Petroleum crude oil from New Town, North Dakota") -->

Seven point seven million litres of it.
<!-- LM-02 ✓ VERBATIM ("7.7 million litres") -->

【F09 number ticker: 0 → 7,700,000, 24 frames, Easing.out(Easing.cubic), label "litres of crude oil".】

The cars were a type called Class 111. They were the ordinary tank car of North American railways at the time, and by the end of this story they would not be.
<!-- LM-01 ✓ VERBATIM (car type) · LM-37 ✓ — the forward reference is to the 2016 phase-out, which is stated in ACT_5 -->

---

## ACT_2 — SEVEN

【5:40.0–11:40.0 · Pictures: the line at dusk · the grade profile drawn · a hand-brake wheel, hero · a coupling · the yard · a hotel corridor. F14–F28.】

At ten minutes to eleven on the night of the fifth of July, the train stopped at Nantes.
<!-- LM-03 ✓ VERBATIM ("at about 2250 Eastern Daylight Time, the train was stopped at Nantes, Quebec") -->

Nantes was the designated crew change point.
<!-- LM-03 ✓ VERBATIM ("the designated MMA crew change point") -->

That is a routine thing. A train arrives, one crew stops work, another takes it on. What was not routine, and what the investigation would spend a great deal of its length on, is where the train was standing when it stopped.
<!-- LM-03 ✓ OURS — framing; the fact asserted is only that Nantes was a crew change point -->

It was parked on a descending grade, on the main track.
<!-- LM-04 ✓ VERBATIM ("parked on a descending grade on the main track") -->

【F16: the grade drawn as a single falling line, 3.0 s, the town marked at the low end.】

Just over seven miles away, at the bottom of that grade, was the town of Lac-Mégantic.
<!-- LM-04 ✓ VERBATIM ("just over seven miles from Lac-Mégantic") -->

A parked train is held by two different things, and the difference between them is the whole of this film.
<!-- OURS — explanatory framing of LM-08 and LM-09 -->

The first is the air brake. Air brakes are held on by pressure, and that pressure is made by a compressor, and the compressor is driven by a running locomotive engine.
<!-- LM-08 ✓ OURS — plain-language statement of the dependency the report states in LM-08 -->

The second is the hand brake. A hand brake is a wheel on the end of a car that a person turns, by hand, one car at a time, in the dark. It does not need pressure. It does not need anything. Once it is on, it stays on.
<!-- LM-09 ✓ OURS — description of the mechanism named in LM-09 -->

【F17 hero: the brake wheel, 4.5 s, a hand entering frame at f60, no face.】

That night, hand brakes were applied on five locomotives and two other cars.
<!-- LM-09 ✓ VERBATIM ("Engineer applied hand brakes on 'five locomotives and two other cars'") -->

Seven.
<!-- LM-09 ✓ OURS — arithmetic on LM-09 -->

The investigation later concluded that the number actually needed was a minimum of seventeen, and possibly as many as twenty-six.
<!-- LM-10 ✓ VERBATIM ("a minimum of 17 and possibly as many as 26 hand brakes were actually needed") · ⛔-04: never a single figure -->

【B1 kinetic: 7 lands left; 17 and 26 rise on the right, staggered 6 frames, spring damping 14. The card never resolves to one number.】

Now, the rules did not leave that to guesswork. There was a test.
<!-- LM-11 ✓ OURS — framing of the test described in LM-11 -->

The railway's rules required that the hand brakes alone be capable of holding the train, and that this be verified.
<!-- LM-11 ✓ VERBATIM (the requirement and the verification) -->

The way you verify it is straightforward. You release everything else, and you see whether the train moves. If it holds with nothing but the hand brakes, the hand brakes are enough.
<!-- LM-11 ✓ OURS — plain-language statement of the test the report describes -->

That test was performed.
<!-- LM-11 ✓ VERBATIM -->

【Re-hook, 8:00 target. Cut to black for 8 frames before the next line.】

It was performed with the locomotive air brakes still applied.
<!-- LM-11 ✓ VERBATIM ("Test conducted 'with the locomotive air brakes still applied,' preventing identification of insufficient hand brake force") -->

So the thing that was holding the train during the test was not the thing being tested.
<!-- LM-11 ✓ OURS — restatement of the report's own conclusion -->

The train held. Of course it held. The air brakes were on.
<!-- LM-11 ✓ OURS -->

And because it held, nobody in that yard had any way of knowing that seven hand brakes were not enough.
<!-- LM-11 ✓ VERBATIM (the test "prevent[ed] identification of insufficient hand brake force") -->

【F22: the test, drawn twice — once as intended, once as performed. 5.0 s total, the second version overlaying the first.】

It is worth being precise about what that means, because this is the point where the story is usually told wrongly.
<!-- OURS — ⛔-01 framing -->

This was not a man skipping a check. The check was done. It was the check itself that could not fail.
<!-- LM-11 ✓ OURS — restatement -->

The train was secured. The paperwork was correct. The rule had been complied with. And the train was not being held by anything that would still be there in an hour.
<!-- LM-09, LM-11, LM-08 ✓ OURS — each clause restates a ledger row -->

By the accounts published afterwards, the engineer finished his shift and went to a hotel in the town at the bottom of the hill.
<!-- LM-05 ✓ SECONDARY — hedged as reported; not load-bearing -->

---

## ACT_3 — THE THING THEY SWITCHED OFF

【11:40.0–17:40.0 · Pictures: the yard · flame at distance, no people · a hose line as silhouette · a hand on a breaker panel · the gauge, hero · the empty yard · the town. F29–F46. Music bed drops 6 dB across the gauge hold.】

At ten minutes to midnight, a resident of Nantes saw flames on the lead locomotive and called the emergency line.
<!-- LM-06 ✓ VERBATIM -->

The locomotive was MMA 5017. It was the one with the repair in it.
<!-- LM-06 ✓ VERBATIM (identifier) · LM-20 ✓ (the same locomotive) -->

The fire was in the turbocharger, where eight months of oil had been collecting.
<!-- LM-23 ✓ VERBATIM -->

The fire service arrived and did the correct thing for a fire on a diesel engine. You cut the fuel and you cut the power.
<!-- LM-07 ✓ OURS — characterisation of LM-07's actions as correct procedure -->

They shut off the locomotive's fuel supply.
<!-- LM-07 ✓ VERBATIM ("Firefighters 'shut off the locomotive's fuel supply'") -->

They moved the electrical breakers inside the cab to the off position.
<!-- LM-07 ✓ VERBATIM ("and moved 'electrical breakers inside the cab to the off position'") -->

The fire went out. Nobody was hurt. Everyone did their job.
<!-- LM-07 ✓ OURS — no casualty is asserted at Nantes; the ledger records none -->

【Silence for 12 frames. Then the gauge.】

And with every locomotive shut down, the air compressor stopped supplying the air brake system.
<!-- LM-08 ✓ VERBATIM ("with all the locomotives shut down, the air compressor no longer supplied air to the air brake system") -->

【B2 hero: the gauge needle, f0→f210, rotation −4° → −38°, Easing.inOut(Easing.quad). Ambient bed −6 dB across the span. No narration for 4.0 s.】

Air brakes do not fail suddenly. They leak.
<!-- LM-12 ✓ OURS — restatement of the gradual pressure loss the report describes -->

The pressure holding seventy-two loaded tank cars on a descending grade began to fall, slowly, in an empty yard, with nobody watching it, for about an hour.
<!-- LM-12 ✓ VERBATIM (the falling pressure and the timing) · LM-04 ✓ (grade) -->

Just before one in the morning, the pressure reached the point where the combination of what was left of the air brakes and the seven hand brakes could no longer hold the train.
<!-- LM-12 ✓ VERBATIM ("the air pressure had dropped to a point at which the combination of locomotive air brakes and hand brakes could no longer hold the train") -->

And the train began to roll.
<!-- LM-12 ✓ VERBATIM ("it began to roll downhill") -->

【Re-hook, 14:00 target: the cold-open question is answered on this line. Cut rate lifts to 2.6 s mean for the next 90 seconds.】

There was nobody on it.
<!-- LM-12 ✓ OURS — the train was unattended, which the report states -->

Seven miles of descending grade, and a train that had no driver, no dispatcher watching it move, and no brake that was going to come back.
<!-- LM-04, LM-08, LM-12 ✓ OURS — restatement -->

It reached a top speed of sixty-five miles an hour.
<!-- LM-13 ✓ VERBATIM ("the train reached 'a top speed of 65 mph'") -->

It derailed near the centre of the town at about a quarter past one in the morning.
<!-- LM-13 ✓ VERBATIM ("It derailed near the centre of the town at about 1:15 a.m.") -->

【F44: light on rooftops, smoke crossing a streetlamp, reflection in a puddle two streets away. No fire with a person in frame. 6 cuts, 3.2 s mean.】

Sixty-three of the seventy-two tank cars came off the track.
<!-- LM-14 ✓ VERBATIM ("72 Class 111 tank cars; 63 derailed") -->

Approximately six million litres of crude oil were released.
<!-- LM-15 ✓ VERBATIM ("approximately 'six million litres' released") -->

---

## ACT_4 — EIGHTEEN

【17:40.0–23:40.0 · Pictures: the wreck wide and still · investigators at distance · the report cover · blank document grounds with Remotion typography · the polymer patch returning · a corridor. F47–F61.】

Forty-seven people were killed.
<!-- LM-16 ✓ VERBATIM ("47 people dead") · ⛔-05: none is named, shown or characterised -->

【F49: the number holds longer than any other card in the film. 5.0 s. No motion but the ambient bed.】

Much of the centre of the town was destroyed.
<!-- LM-17 ✓ VERBATIM ("much of the downtown core was destroyed") -->

By the accounts published afterwards, more than thirty buildings in the town centre were lost, and most of what was left had to be taken down because the ground was contaminated.
<!-- LM-19 ✓ SECONDARY — hedged as reported -->

The Transportation Safety Board of Canada investigated for just over a year, and in August of twenty fourteen it published what it had found.
<!-- LM-24, LM-29 ✓ — the report and the news release of 19 August 2014 -->

It identified eighteen distinct causes and contributing factors.
<!-- LM-24 ✓ VERBATIM ("18 distinct causes and contributing factors") -->

【B3 kinetic: count-up 1 → 18, 24 frames. Each factor appears as a line that does not stay. The list is felt, not read.】

Eighteen is a strange number to be given at the end of a story like this, because it is not an answer. It is the refusal of one.
<!-- OURS — argument, no fact asserted -->

Some of the eighteen were about that night. Most of them were not.
<!-- LM-24 ✓ OURS — characterisation supported by LM-26, LM-27, LM-28 which are not events of that night -->

The railway had a safety management system. It had written one in two thousand and two.
<!-- LM-26 ✓ VERBATIM ("MMA 'developed a safety management system in 2002'") -->

It did not begin implementing it until two thousand and ten.
<!-- LM-26 ✓ VERBATIM ("but did not 'begin to implement this safety management system until 2010'") -->

And by twenty thirteen it was still not functioning effectively.
<!-- LM-26 ✓ VERBATIM ("and by 2013, it was still not functioning effectively") -->

That is eleven years in which a document existed and the thing it described did not.
<!-- LM-26 ✓ OURS — arithmetic on LM-26 -->

The regulator's regional office did not audit that system until twenty ten.
<!-- LM-27 ✓ VERBATIM ("Transport Canada's Quebec office 'did not audit it until 2010'") -->

【Re-hook, 20:00 target.】

And the cargo itself was not what its papers said it was.
<!-- LM-28 ✓ OURS — framing of LM-28 -->

The crude oil in those tank cars was more volatile than the shipping documents described.
<!-- LM-28 ✓ VERBATIM ("Petroleum crude oil 'was more volatile than described on the shipping documents'") -->

【F57 hero: the shipping document as a blank card. Typography composited in Remotion. Never a generated document.】

That matters because volatility is what decides whether a derailment is a spill or a fire.
<!-- OURS — plain-language explanation; asserts no new fact -->

The Board called for physical defences against runaway trains, and for more thorough audits of safety management systems.
<!-- LM-29 ✓ VERBATIM ("the TSB called for additional physical defences to prevent runaway trains, and more thorough audits of safety management systems") -->

And there is one sentence the report did not write, which is the sentence almost everybody expects.
<!-- OURS — framing of LM-25 -->

The train was operated that night by one person. It has been argued ever since that a second crew member would have changed what happened.
<!-- AB-03 ✓ — the single-person operation is context, not a finding -->

The investigation was not able to conclude that.
<!-- LM-25 ✓ VERBATIM ("Investigation 'was not able to conclude that having another crew member would have prevented the accident'") -->

Single-person operation is not among the eighteen.
<!-- AB-03 ✓ — established absence -->

---

## ACT_5 — WHO ANSWERED

【23:40.0–29:00.0 · Pictures: an office emptied · a ledger · a corridor with a bench · a stack of files · three name-plates as typography · the empty chair, hero. F62–F76.】

In August of twenty thirteen, the railway and its Canadian subsidiary filed for bankruptcy protection.
<!-- LM-31 ✓ SECONDARY — hedged by attribution in the ledger; corroborated by SRC-0007 -->

It did not have enough insurance to cover the claims against it.
<!-- LM-31 ✓ VERBATIM ("MMA did not have enough insurance to cover the hundreds of millions of dollars in claims against it") -->

Its assets were sold in January of twenty fourteen, and the line went on operating under a new name.
<!-- LM-32 ✓ SECONDARY -->

A settlement fund was assembled for the victims. In October of twenty fifteen a United States bankruptcy judge approved it.
<!-- LM-33 ✓ VERBATIM (approval and date) -->

It came to somewhere between four hundred and forty-six and four hundred and fifty million Canadian dollars.
<!-- LM-33 ✓ VERBATIM ("a $446 million Cdn settlement fund" / "the roughly 25 companies that have agreed to contribute to the $450 million") -->

About twenty-five companies paid into it.
<!-- LM-33 ✓ VERBATIM ("The roughly 25 companies that have agreed to contribute") -->

One did not.
<!-- LM-34 ✓ VERBATIM ("Canadian Pacific Railway is the only company accused in the disaster to have refused to contribute") -->

Canadian Pacific was the only company accused in the disaster that refused to contribute. It maintained that it bore no responsibility, and it asked for permission to appeal the settlement's approval.
<!-- LM-34 ✓ VERBATIM -->

It later dropped its objection, and the fund was approved.
<!-- LM-34 ✓ VERBATIM ("after Canadian Pacific Railway Ltd. dropped its objection to the settlement plan") -->

【Re-hook, 26:00 target. Cut to the corridor.】

And then there was a criminal trial.
<!-- LM-35 ✓ -->

Three men were charged with criminal negligence causing death. The locomotive engineer, the rail traffic controller, and the manager of train operations.
<!-- LM-35 ✓ VERBATIM (the three roles and the charge) -->

They were the three people at the operating end of everything this film has described.
<!-- OURS — argument -->

In January of twenty eighteen, after nine days of deliberation, the jury acquitted all three.
<!-- LM-35 ✓ VERBATIM ("After nine days of deliberations, jurors acquitted the three former MMA railway employees charged with criminal negligence causing death"; "The 12 jurors found Harding, Labrie and Demaitre not guilty") -->

【B4 kinetic: three name-plates as typography rise and hold; the word ACQUITTED masks up beneath all three. Held 4.0 s. ⛔-01: this card is the film's largest.】

The engineer said afterwards that he was deeply sorry.
<!-- LM-36 ✓ VERBATIM QUOTE ("'I am deeply sorry,' says Tom Harding") -->

The rules did change. Canada ordered the tank car in this story out of crude oil service by November of twenty sixteen, six months earlier than had originally been planned.
<!-- LM-37 ✓ VERBATIM ("Transport Minister Marc Garneau ordered the retirement of all DOT-111 railcars by November 1st, 2016, six months earlier than originally planned") -->

A stronger design replaced it, and from April of twenty twenty-five it became the only tank car allowed to carry flammable liquids in the country.
<!-- LM-37 ✓ VERBATIM ("the TC-117 tank car... became the only acceptable tank car for all flammable liquids in Canada after April 30, 2025") -->

---

## ENDING

【29:00.0–30:00.0 · Pictures: the empty chair, hero, 9.0 s hold with ambient motion only · then BrandEndcard at tail. No typography over the chair.】

So here is what the record holds at the end of it.
<!-- OURS -->

A repair that was made with the wrong material because the right one cost time and money. A test that could not have failed. A safety system that existed on paper for eleven years. A regulator that audited it once, three years before. Papers that described a cargo less dangerous than the cargo was. Eighteen findings, and a company that no longer exists.
<!-- LM-21, LM-11, LM-26, LM-27, LM-28, LM-24, LM-31 ✓ — each clause restates a ledger row -->

And three men who were tried, and acquitted.
<!-- LM-35 ✓ VERBATIM · ⛔-01 -->

No individual was ever established as the cause of it.
<!-- AB-01 ✓ — established absence -->

That is not a loose end. That is the finding.
<!-- OURS — argument -->

Every system you depend on is arranged the same way. Somebody approves the repair. Somebody writes the rule. Somebody performs the test. Somebody signs the audit, or does not. Each of those people is doing a job that is defined, and bounded, and complete on its own terms.
<!-- OURS — second-person turn, no fact asserted -->

The question is never whether one of them fails. It is whether anybody in the whole arrangement is responsible for the arrangement.
<!-- OURS -->

【CTA over the endcard: specific, one line. "If this changed how you look at the things that are supposed to be holding still, subscribe — that is the whole series."】
