# EP74 · ITAEWON — SCRIPT v004

> **Supersedes v003. This is the revision written to THIS episode's own measured pace.**
> `--measure-section ACT_1` generated 49 chunks / 734 words and ffprobed 222.025 s of speech —
> **198.4 raw wpm**, 186.3 words per finished minute. That is 15.5 % faster than the registry model
> and 3.8 % faster than EP72. At that rate v003's 5,267 words made a **28:28** film, thirty-two
> seconds under the runtime floor, so the word band was re-derived a final time to **[5370, 5930]**
> and this revision adds the Enforcement Decree — `IT-81`, `IT-83`, both PRIMARY — to reach it.
> **⛔-15 is new and binding on the added material: the five-item list is read as what the rule now
> requires, and the film stops there. No counterfactual.**
>
> **Superseded note, kept for the record.** v002 measured **4,669 narration words** — 26:11 of finished film against a
> runtime floor of 1,740 s. Measuring it also exposed a defect in `episode_spec.v001.json`: at the
> measured 191.1 wpm its declared word floor of 4,900 produced a 27:28 film, ninety-two seconds
> below its own runtime floor, so the two bands could never both have been satisfied. The word band
> was re-derived from the runtime band to **[5180, 5720]** before the spec was committed.
> `EP74_itaewon_FACTS_LEDGER.v003.md` adds `IT-78`…`IT-82` — the statute itself, read in the
> statute — and this revision is written from them. Structure unchanged.
>
> **Superseded note, kept for the record.** v001 measured **3,883 narration words** — 21:50 of finished
> film against a 29:00–32:00 band. The shortfall was research, not writing:
> `EP74_itaewon_FACTS_LEDGER.v002.md` adds rows `IT-55`…`IT-77` from a peer-reviewed study of the
> crowd itself, a government page, the Constitutional Court's impeachment ruling and the foreign
> victims' families, and this revision is written from them. Nothing in v001's structure changed:
> five acts, five hero objects, the same hook, the same word for word.
>
> **Design `EP74_itaewon_FILM_BIBLE.v001.md` · facts `EP74_itaewon_FACTS_LEDGER.v001.md` +
> `.v002.md` (the only source of any factual line) · contract
> `episodes/PD-2026-074-itaewon/episode_spec.v001.json`.**
>
> **One deviation from the bible, declared.** FILM_BIBLE §6 ACT_5 beat map runs F59–F74 and does not
> contain the impeachment of the Interior and Safety Minister, because v001 of the ledger did not
> have it. ACT_5 now carries it between F70 and F71 (rows IT-71–IT-73). The controlling idea is
> unchanged and strengthened: three state bodies looked at the same night and gave three different
> answers, in that order.
>
> **Citation convention.** Every factual line is followed on the next line by an HTML comment
> carrying its ledger row id. A line with no row id does not enter the film.
>
> **Five rules break this film if broken.** The toll is **159** and never 160 (⛔-03). No named
> person appears without their verified legal status, its date and its court **in the same sentence**,
> and no appellate outcome is asserted at all (⛔-04, AB-02). The police did not do nothing — they
> received eleven and went to four (⛔-07). No counterfactual: nothing "would have" prevented it
> (⛔-08). And **the crush is never depicted, in any frame** (⛔-02) — the event is carried by sound,
> by the width of the walls, by the slope, and now by numbers that were measured after the fact.
>
> **Two `UNREAD` rows are deliberately absent from this script**: IT-58 (the Seoul Metro passenger
> figures) and IT-74 (the Constitutional Court's "many factors" line). Both are strong. Neither has
> been read in the article. ⛔-10.

---

## HOOK

【0:00.0–0:22.0 · voiced from frame 0 · Pictures: a narrow alley at night, empty, wet → a phone screen lighting a hand → the mouth of the alley from below → sodium light on a brick wall at arm's length → a stairwell of an underground station. Push-in f0→f36, scale 1.06→1.00, Easing.out(Easing.cubic), Trail 6 layers to f18. NO CROWD YET.】

Thirty-four minutes past six, on a Saturday evening in Seoul, someone pushed their way out of a crowded alley, took out a phone, and called the police.
<!-- IT-13, IT-14, IT-63 ✓ VERBATIM (time) · ⛔-13 caller never identified -->

It was not a crime they were reporting.
<!-- OURS — characterisation of a 112 call about crowding -->

They said people were being forced uphill into a place where there was no room to come back down, and that somebody should come and control it.
<!-- IT-14 ✓ VERBATIM (paraphrase; the quotation lands in ACT_2) -->

Ten more people were going to make that same call.
<!-- IT-13 ✓ VERBATIM -->

【BrandOpening lands here, 3.5 s, over continuing footage. Imported, never forked.】

---

## OP

【0:22.0–0:57.0 · Pictures: the street plan drawn from above, the alley picked out in a single stroke → the width line beginning to draw → a shuttered shopfront → black. Width line draw f0→f45, stroke 0→100 %, Easing.inOut(Easing.quad).】

This is a story about a street, a telephone number, and a definition.
<!-- OURS — thesis line -->

The street is about fifty metres long. At the top it is about five metres wide. At the bottom it is three point two.
<!-- IT-02 ✓ VERBATIM -->

The telephone number is one-one-two, which in South Korea is what you dial for the police.
<!-- OURS — explanatory; the number itself is IT-13 -->

And the definition is the one the country's disaster and safety law used for an event: something with an organiser, somebody whose name is on it, somebody who files a safety plan in advance.
<!-- IT-26, IT-27 ✓ SECONDARY -->

That definition is a real sentence in a real statute with a number on it, and by the end of this film you are going to hear the sentence that replaced it.
<!-- IT-79 ✓ VERBATIM (PRIMARY) — forward reference, resolved in ACT_5 -->

On the night this film is about, an estimated hundred thousand people came to a district where nothing had an organiser at all.
<!-- IT-55 ✓ VERBATIM · IT-26 ✓ SECONDARY -->

By the end of that night a hundred and fifty-nine people were dead, and by the end of the following year a court had convicted one official, acquitted another, and explained the difference in a single sentence about who the law was written for.
<!-- IT-22 ✓ VERBATIM · IT-30, IT-33, IT-34 ✓ VERBATIM -->

Over the next half hour you will hear what eleven people said when they called, what the state did with four of those calls and did not do with seven, where its officers were instead, and why the district office walked out of court.
<!-- OURS — the opening's "what you'll learn"; each clause is answered later -->

The question is not who to blame. It is what happens to a warning after somebody makes it.
<!-- OURS — controlling idea -->

---

## ACT_1 — THREE POINT TWO

【Pictures: the alley empty at dawn, hosed, wet → the same alley from the top → the same alley from the bottom → a hand flat against a wall → the dimension line, drawn, 5 m at the top. Still cuts 3.8 s, scale 1.000→1.055, y 0→−18 px.】

Start with the street, because the street is the part of this that anyone can stand in.
<!-- OURS — register -->

It runs off Itaewon-ro, the main road through the district, up between the back of the Hamilton Hotel and the buildings behind it, toward the streets above.
<!-- IT-01 ✓ SECONDARY -->

Exit One of Itaewon station comes up almost at the foot of it.
<!-- IT-01 ✓ SECONDARY -->

If you have been to any city in the world, you have walked up a street like this one. It is a shortcut. It is the way people get from the station to the bars without going the long way round.
<!-- OURS — register; no factual claim -->

It is about fifty metres long. That is a short walk. Twenty-five seconds, at a normal pace, without stopping.
<!-- IT-02 ✓ VERBATIM · OURS — the walking time is characterisation -->

【Width line completes to 3.2 m. Held. Width figure spring damping 14, mass 0.6. HERO — the longest card in the act.】

At the top it is about five metres across. At the bottom — the end that opens onto the main road — it is three point two.
<!-- IT-02 ✓ VERBATIM -->

Three point two metres is two cars parked side by side. It is a domestic living room, turned on its end and stretched out for fifty metres.
<!-- OURS — comparison for scale -->

A study published in 2024 by researchers writing in the journal PLOS One put the average width of that alley at under four metres along its length.
<!-- IT-61 ✓ VERBATIM · ⛔-11 — source named in narration -->

And it is not flat. The street slopes. It rises from the main road up toward the streets behind, which means that anybody standing in it is standing on a hill.
<!-- IT-04 ✓ SECONDARY -->

【Slope drawn, single stroke, left to right, f0→f60, Easing.out(Easing.cubic). NO NUMBER ON IT — AB-01.】

Nobody has published how steep. There is a figure for the width and a figure for the length and there is no figure for the gradient, so this film will not give you one. What it will tell you is the direction: up, away from the main road.
<!-- AB-01 ✓ ABSENCE -->

That direction matters more than any number would, because it decides which way the weight goes.
<!-- IT-04 ✓ SECONDARY -->

【Pictures: the hotel's rear elevation → a terrace structure, in silhouette, no signage legible → a building-permit drawing composited in Remotion, blank of any real text.】

There is one more thing about the width, and it had been on file with the district for over a year.
<!-- IT-05, IT-06 ✓ VERBATIM -->

The Hamilton Hotel had illegally extended a terrace on the northern side of its main building — seventeen point two square metres of it — along the side that faces the alley.
<!-- IT-05 ✓ VERBATIM -->

The Korea Times, reading the building records a few days after, wrote that the extension had made the narrow path even narrower.
<!-- IT-05 ✓ VERBATIM · ⛔-11 -->

The district office already knew. It had notified the hotel of the violation and levied fines the previous year.
<!-- IT-06 ✓ VERBATIM -->

So the state's knowledge of that street was not zero. Somebody had measured it, written it down, and issued a penalty about it, in 2021.
<!-- IT-06 ✓ VERBATIM · OURS -->

What nobody had done was ask what the street was for on a Saturday night.
<!-- OURS — no counterfactual -->

【Pictures: dusk, signage coming on, shutters going up → a station platform filling → costume as silhouette and colour at distance, never a face held. NO WESTERN DAYTIME CROWDS. NO FESTIVAL STOCK.】

The date was the twenty-ninth of October, 2022. A Saturday.
<!-- IT-07 ✓ VERBATIM -->

It was the first Halloween in three years without distancing rules, and the first with the outdoor mask requirement lifted.
<!-- OURS — period context -->

Itaewon is where that happens in Seoul. It is the district with the foreign restaurants and the bars that stay open, a few minutes from a station on two lines, and for one weekend a year it is where the whole city goes to be somewhere crowded.
<!-- OURS — place description -->

Al Jazeera, reporting three days later, put the number at an estimated hundred thousand people, many of them in their teens and twenties, and dressed in costume.
<!-- IT-55 ✓ VERBATIM · ⛔-11 -->

A hundred thousand people is a stadium. It is a city the size of a small county town, arriving in one district, on foot, over about six hours, in the dark.
<!-- IT-55 ✓ VERBATIM · OURS — scale comparison -->

And it was not a surprise that it happened. Itaewon fills for Halloween. It does it every year, and every year that alley is the fastest way between the station at the bottom and the street at the top. What was different about 2022 was that for two years it had not happened at all, and then it did.
<!-- OURS — period context; no figure claimed -->

Nobody organised it. There was no ticket, no promoter, no stage, no permit, no name on anything.
<!-- IT-26 ✓ SECONDARY — the film's central fact, planted here -->

Hold on to that, because in two years' time a court is going to build an acquittal on it.
<!-- IT-33, IT-34 ✓ VERBATIM — forward reference, resolved in ACT_5 -->

By the middle of the evening the alley was full, and it was full in both directions: people coming up from the station at the bottom, and people coming down from the streets at the top, in a passage that narrows as it descends.
<!-- IT-02, IT-04, IT-62 ✓ -->

Remember that too. Both directions. It is going to turn out to be the whole mechanism.
<!-- IT-62 ✓ VERBATIM — forward reference, resolved in ACT_3 -->

At thirty-four minutes past six, somebody in it decided that this was a matter for the police.
<!-- IT-13, IT-14, IT-63 ✓ VERBATIM -->

---

## ACT_2 — ELEVEN CALLS

【Pictures: the call log — eleven ruled rows, empty, composited in Remotion → row 1 timestamped. HERO. Row fill 8 f, stagger 4 f, spring damping 16, mass 0.5. THE SEVEN NEVER FILL: outline only, 1 px, 42 % opacity.】

Between six thirty-four in the evening and eleven minutes past ten, the police in Itaewon received eleven distress reports about dangerous levels of overcrowding.
<!-- IT-13 ✓ VERBATIM -->

That is the sentence the Korea Times printed in March of this year, reporting an investigative hearing, and it is worth taking apart slowly, because every word in it is doing work.
<!-- IT-13, IT-47 ✓ VERBATIM · ⛔-11 -->

Eleven reports. Not eleven people complaining about noise. Reports about dangerous levels of overcrowding, made to the police, by the people standing in it.
<!-- IT-13 ✓ VERBATIM -->

Here is the first one.
<!-- — -->

【Quote card. Typography composited in Remotion. Attributed on the card: "112 call, 18:34 · translated from a police-released transcript · as rendered by the South China Morning Post".】

Looks like you can get crushed to death with people keep coming up here while there's no room for people to go down. I barely managed to leave but there are too many people, looks like you should come and control.
<!-- IT-14 ✓ VERBATIM -->

That is a translation, and it is worth saying so. The caller was speaking Korean. Different outlets rendered it differently — Al Jazeera published it as *I feel like I would be almost crushed to death here because people continued to come up even though no more can go down.*
<!-- IT-15 ✓ VERBATIM — the two-translation rule, honoured out loud -->

The wording moves. What does not move is the content. Four hours before anything happened, a person standing in that alley used the words *crushed to death*, and asked for somebody to come and control it.
<!-- IT-14, IT-15 ✓ VERBATIM -->

【Row 1 fills.】

Officers were sent.
<!-- IT-18 ✓ VERBATIM -->

That matters, and this film is going to be careful about it, because the easy version of this story is that nobody did anything, and the easy version is false.
<!-- IT-18 ✓ VERBATIM · ⛔-07 -->

Officers went. They dispersed crowds where they went.
<!-- IT-18 ✓ VERBATIM -->

【Pictures: hi-vis at distance, a torch beam across a wall, a radio in a hand. NO FACE, NO BADGE, NO UNIT MARKING.】

The next call in the study's timeline came at nine minutes past eight.
<!-- IT-63 ✓ VERBATIM -->

One hour and thirty-five minutes after the first one.
<!-- IT-65 ✓ OURS — arithmetic on IT-63 -->

【Quote card, 20:09.】

There are people who fell over and got hurt because there are too many people.
<!-- IT-16 ✓ VERBATIM -->

Read that as a piece of information arriving at a police switchboard. Not *it is busy*. Not *it is uncomfortable*. People have fallen over, and people have been hurt, and the reason given is the number of people.
<!-- IT-16 ✓ VERBATIM · OURS — reading of the text -->

Two hours before anything was reported as an accident, the word *fallen* was already in the record.
<!-- IT-16, IT-63 ✓ VERBATIM -->

The calls kept coming, and the language in them stopped being about congestion.
<!-- IT-17 ✓ VERBATIM -->

【Quote cards, two in succession, 3.2 s each, no dissolve between.】

We are on the verge of a terrible accident due to the massive crowds.
<!-- IT-17 ✓ VERBATIM -->

I am almost being crushed to death.
<!-- IT-17 ✓ VERBATIM -->

Those are two different people, on two different calls, on the same evening, in the same street.
<!-- IT-13, IT-17 ✓ VERBATIM -->

The last of the eleven came in at eleven minutes past ten.
<!-- IT-13 ✓ VERBATIM -->

【AE KINETIC BEAT 1 — "ELEVEN". Full-frame. render_beats.sh.】

Eleven calls.
<!-- IT-13 ✓ VERBATIM -->

【AE KINETIC BEAT 2 — "FOUR".】

Officers were deployed to four of them.
<!-- IT-18 ✓ VERBATIM -->

【The log, complete. Four rows filled. Seven rows outline-only. Held 4.0 s — the longest hold in the act.】

On the other seven, according to Al Jazeera's reporting at the time, there was no action.
<!-- IT-18 ✓ VERBATIM · ⛔-11 -->

【AE KINETIC BEAT 3 — "3:37".】

Three hours and thirty-seven minutes separate the first of those calls from the last one.
<!-- IT-21 ✓ OURS -->

Three hours and thirty-seven minutes is long enough to drive across a country. It is longer than a football match and its half-time and the drive home afterwards. It is long enough that the shift you started the evening on is a different shift by the end of it.
<!-- OURS — scale comparison -->

And across all of it, the width of the street did not change.
<!-- IT-02 ✓ VERBATIM · OURS — consequence voice -->

【Pictures: the width line returns, silent, no figure, 2.0 s → the alley from the top, empty → black.】

The National Police Commissioner, Yoon Hee-keun, said afterwards that crowd control at the scene had been inadequate, and that there had been multiple reports to the police indicating the seriousness at the site just before the accident occurred.
<!-- IT-19, IT-57 ✓ VERBATIM -->

The Prime Minister, Han Duck-soo, said the police must conduct thorough inspections and provide a clear and transparent explanation to the public.
<!-- IT-20 ✓ VERBATIM -->

There is a version of this story in which those eleven calls are the whole of the scandal, and that version is not quite right either.
<!-- OURS — act bridge -->

A call is a piece of information arriving at an organisation. What an organisation does with information depends on what else it is doing, how many people it has, and where those people are standing at the time.
<!-- OURS — act bridge -->

That is not an excuse. It is the next question.
<!-- OURS -->

Both of those statements are true and neither of them is an answer, because neither of them says where the officers were.
<!-- OURS — sets up ACT_4 -->

That answer took three years, and it did not come from the police.
<!-- IT-12 ✓ VERBATIM — forward reference -->

---

## ACT_3 — UPHILL

【Pictures: the slope, drawn again, no number, 2.0 s → the alley EMPTY, wide → the alley ORDINARILY BUSY, mid-evening, unremarkable → the alley AFTER: hosed, lit, nobody in it. THREE STATES ONLY. ⛔-02 — nothing else exists in this act.】

This film is not going to show you what happened in that street, and it is worth saying why rather than just doing it.
<!-- OURS — the film's own rule, stated -->

A hundred and fifty-nine people died there. Their families are alive. Their names are in the public record and are not going to be in this film.
<!-- IT-22 ✓ VERBATIM · ⛔-01 -->

So the street will appear three ways and no other way: empty, ordinarily busy, and afterwards.
<!-- OURS — production rule, ⛔-02 -->

What can be described is the shape of the problem, and in this case somebody has measured it.
<!-- IT-59, IT-60, IT-62 ✓ VERBATIM -->

【Pictures: an abstract density diagram, built in Remotion — a rectangle, then dots resolving to a solid field. NO PHOTOGRAPHIC CROWD UNDER THIS SECTION.】

In 2024 four researchers published a study of that night in PLOS One, reconstructing the crowd from the record.
<!-- IT-59, IT-62 ✓ VERBATIM · ⛔-11 -->

They put the average density during the crush at seven point five seven people per square metre, with a maximum of nine point nine five.
<!-- IT-59 ✓ VERBATIM -->

One square metre is a doormat. Nine people, standing on a doormat.
<!-- IT-59 ✓ VERBATIM · OURS — comparison for scale -->

They calculated the pressure inside it. On average it peaked at one thousand and sixty-three newtons per metre, and at maximum, one thousand nine hundred and sixty-one.
<!-- IT-60 ✓ VERBATIM -->

Those are not numbers most people have a feel for, so here is the one that matters instead. In an area of eighteen square metres, the study records that over three hundred people were concentrated.
<!-- IT-61 ✓ VERBATIM -->

Eighteen square metres is a small bedroom.
<!-- IT-61 ✓ VERBATIM · OURS — comparison -->

At the density those researchers measured, a person cannot lift their arms. They cannot choose where to put their feet. They are not standing in a crowd any more; they are part of one, and the direction they travel is decided by the people behind them.
<!-- IT-59, IT-60 ✓ VERBATIM · OURS — characterisation of the measured density, not of any individual -->

That is the condition those numbers describe, and it is why a narrow sloping alley is a different kind of place from a wide flat one, at the same headcount.
<!-- IT-59, IT-60, IT-62, IT-04 ✓ -->

【The density diagram holds, 3.0 s, then cuts to the slope line.】

And the mechanism they identify is the thing planted at the end of the first act.
<!-- IT-62 ✓ VERBATIM -->

The primary causes, in their words, were the substantial population, bidirectional collision, and escalating panic — a bidirectional stream of pedestrians colliding in a narrow alley.
<!-- IT-62 ✓ VERBATIM -->

People going up and people coming down, in a passage that gets narrower as it descends, on a hill.
<!-- IT-02, IT-04, IT-62 ✓ -->

A crowd on flat ground that becomes too dense has one thing going for it: the pressure has somewhere to go, in every direction at once.
<!-- OURS — general characterisation, non-numeric -->

A crowd in a passage between two buildings has two directions instead of every direction. A crowd being fed into that passage from both ends has none.
<!-- IT-02, IT-62 ✓ -->

And the incline decided which way the weight went. It went downward.
<!-- IT-04 ✓ SECONDARY -->

【Pictures: the width line and the slope line, together, once, held 3.0 s → cut to the alley empty.】

The study's timeline puts the first report of a crushing accident, involving approximately ten people, at fifteen minutes past ten.
<!-- IT-63 ✓ VERBATIM -->

Three minutes later, at eighteen minutes past, the police chief ordered all available personnel to the scene.
<!-- IT-63 ✓ VERBATIM -->

The first emergency rescue team arrived at twenty-eight minutes past ten.
<!-- IT-63 ✓ VERBATIM -->

【Number card: "22:15 → 22:28". Ticker settles. Held 4.0 s.】

Thirteen minutes.
<!-- IT-64 ✓ OURS — arithmetic on IT-63 -->

Written down like that, thirteen minutes is a short time. Measured against what the study says was happening inside eighteen square metres, it is not a short time at all.
<!-- IT-61, IT-63, IT-64 ✓ -->

There is no siren in this part of the film and there is no footage of the response, and that is deliberate.
<!-- OURS -->

The next part is a count, and the count moved for two months.
<!-- IT-24 ✓ SECONDARY -->

【Number ticker, f0→f24, Easing.out(Easing.cubic). Three values, in sequence, each held 2.5 s.】

In the immediate aftermath, the figure reported was a hundred and fifty-seven.
<!-- IT-24 ✓ SECONDARY -->

By the fourteenth of November it was a hundred and fifty-eight.
<!-- IT-24 ✓ SECONDARY -->

By the third of January it was a hundred and fifty-nine. The last of them was a high-school student who had been in that street and survived it, found dead on the twelfth of December, and recognised by the Ministry of the Interior and Safety as a victim of the disaster.
<!-- IT-24 ✓ SECONDARY · ⛔-01 -->

【"159" — full frame. THE LONGEST CARD IN THE FILM. Held 5.0 s. No motion but the ticker settling.】

A hundred and fifty-nine.
<!-- IT-22 ✓ VERBATIM -->

A further hundred and ninety-six people were injured.
<!-- IT-66 ✓ SECONDARY -->

Reuters described the dead as mostly young people, and that is as far as this film will characterise them, with one exception, which is a matter of public record and is about countries rather than about people.
<!-- IT-23 ✓ VERBATIM · ⛔-01 -->

Twenty-six of the a hundred and fifty-nine were foreign nationals, from fourteen countries.
<!-- IT-67 ✓ VERBATIM -->

Three years later, in October 2025, forty-six relatives of twenty-one of those twenty-six travelled to Seoul for a week, at the official invitation of the Korean government, and went to the site.
<!-- IT-69, IT-70 ✓ VERBATIM -->

They came from twelve nations. Iran, Russia, the United States, Australia, China, Japan, France, Austria, Norway, Sri Lanka, Kazakhstan, Uzbekistan.
<!-- IT-68 ✓ VERBATIM -->

That is a list of countries, not a list of people, and it is the only list this film is going to read out.
<!-- IT-68 ✓ VERBATIM · ⛔-01 -->

【Pictures: departure boards, at distance, unreadable → an aircraft window → the alley, morning, hosed. NO FAMILIES IN FRAME. ⛔-01.】

There is a second toll figure in circulation, and you may see it if you go looking. This film is not going to use it, and here is the reason.
<!-- IT-25 ✓ SECONDARY · ⛔-03 -->

The official figure, the one recorded by the ministry and carried by the reporting, is a hundred and fifty-nine. A study published in July of this year by the special investigation commission works from a slightly larger set. Until the official figure changes, this film uses the official figure.
<!-- IT-22, IT-25 ✓ · ⛔-03 — 160 is never said aloud -->

That study is worth knowing about for a different reason.
<!-- IT-25 ✓ SECONDARY -->

【Pictures: a medical-records folder, blank, composited → a corridor → the alley after, hosed.】

It was carried out by the Department of Forensic Medicine at Pusan National University School of Medicine, between December and May, working from death certificates, post-mortem reports, emergency logs and medical records.
<!-- IT-25 ✓ SECONDARY -->

It found that about one in ten of the dead may not have died of asphyxiation at all — that the cause may have been crush syndrome, or rhabdomyolysis, or damage to internal organs from compression.
<!-- IT-25 ✓ SECONDARY -->

The distinction is not academic. Asphyxiation is fast. The others are not.
<!-- OURS — characterisation of the medical distinction -->

And the commission's conclusion from it was that more people might have survived if rescue efforts had continued immediately after the incident.
<!-- IT-25 ✓ SECONDARY — attributed as theirs -->

That is their finding, published in 2026, three and a half years afterwards. It is theirs and not this film's, and this film is not going to extend it into a sentence about what would have happened, because nobody has established that.
<!-- IT-25 ✓ SECONDARY · AB-05 ✓ · ⛔-08 -->

【The alley, morning. A street cleaner's hose. Nobody in frame. 4.0 s. Hold, then black.】

By the morning of the thirtieth of October, the street was open again.
<!-- OURS — characterisation of the aftermath -->

Which leaves the question the rest of this is about: on a Saturday night, in a district that fills up every Halloween, in a city with one of the largest police forces in the world, where were the officers?
<!-- OURS — the act-turn question -->

---

## ACT_4 — TWO KILOMETRES

【Pictures: the map of Yongsan, drawn, dark. HERO. Pin drop f0→f21 each, 9 f apart, spring damping 12, mass 0.7. Pin one: the alley. Pin two: the presidential office.】

A hundred and thirty-seven.
<!-- IT-08, IT-56 ✓ VERBATIM -->

【AE KINETIC BEAT 4 — "137".】

That is the number of police officers deployed to Itaewon for Halloween, as the police themselves had previously said, and as Al Jazeera reported three days afterwards.
<!-- IT-56 ✓ VERBATIM · ⛔-11 -->

A hundred and thirty-seven officers is a real deployment. It is not nothing. Spread across a district of bars and restaurants on the busiest night of its year, against an estimated hundred thousand people, most of them working on crime rather than on crowds, it is also not very many.
<!-- IT-56, IT-55 ✓ VERBATIM · OURS — characterisation -->

That is one officer for every seven hundred and thirty people.
<!-- IT-55, IT-56 ✓ OURS — arithmetic on the two declared figures -->

The obvious question is why there were not more, and for three years the obvious question had no official answer.
<!-- IT-12 ✓ VERBATIM -->

It got one on the twenty-third of October, 2025.
<!-- IT-12 ✓ VERBATIM -->

【Pictures: a report cover, blank, composited in Remotion → three departmental signs, photographed at an angle, none legible → the map again.】

On that date the Korea Times reported the findings of a joint audit, carried out together by the Office for Government Policy Coordination, the National Police Agency, and the Ministry of the Interior and Safety.
<!-- IT-12 ✓ VERBATIM · ⛔-11 -->

Three government bodies, including the police themselves, auditing what the police had done.
<!-- IT-12 ✓ VERBATIM -->

And what they found was about a building.
<!-- IT-10 ✓ VERBATIM -->

【Pin two enlarges. The map holds.】

In 2022, the President of South Korea moved the presidential office. It left the compound it had occupied for decades and moved into Yongsan — the same district as Itaewon, a little over two kilometres from that alley.
<!-- IT-10 ✓ VERBATIM -->

A presidential office is not just a building. It is a place people come to be heard outside of.
<!-- OURS — characterisation -->

【Figure beat: two values, animated between. AE KINETIC BEAT 5 — "34 → 921". The steepest number in the film.】

Rallies and demonstrations inside the Yongsan police station's jurisdiction went from thirty-four in the whole of 2021 to nine hundred and twenty-one between May and October of 2022.
<!-- IT-09 ✓ VERBATIM -->

Thirty-four in a year. Nine hundred and twenty-one in six months.
<!-- IT-09 ✓ VERBATIM -->

That is not a rounding error in a workload. That is a different job.
<!-- OURS — characterisation -->

Police resources in the district had been redirected to the Samgakji area, near the presidential office.
<!-- IT-11 ✓ VERBATIM -->

And the audit's own sentence, three years after the fact, was this.
<!-- IT-10, IT-12 ✓ VERBATIM -->

【Quote card. The largest card in the act. Attributed: "joint audit — Office for Government Policy Coordination · National Police Agency · Ministry of the Interior and Safety, reported 23 October 2025".】

The relocation of the presidential office to Yongsan increased the demand for police deployment in the area, which was a key factor behind the lack of crowd control officers in Itaewon.
<!-- IT-10 ✓ VERBATIM -->

Read it slowly, because it is the closest thing in this story to a structural answer.
<!-- OURS -->

Nobody in that sentence decided that Itaewon should be short of officers on Halloween. Nobody wrote that down. Nobody signed it.
<!-- OURS — characterisation of the finding -->

A government made a decision about where a president should sit. That decision created a standing demand for officers in one part of a district. The officers came from the same place all officers in that district come from. And on the last Saturday in October, in the other part of the district, there were a hundred and thirty-seven.
<!-- IT-08, IT-09, IT-10, IT-11, IT-56 ✓ -->

【Pictures: the map, both pins lit, held 4.0 s → the pins go out, one at a time → black.】

This film is not going to tell you that more officers would have changed the outcome, because nobody has established that, and a film that says *would have* about a hundred and fifty-nine deaths is making something up.
<!-- AB-05 ✓ ABSENCE · ⛔-08 — stated as a rule, out loud -->

What can be said is narrower and worse. Eleven people called the number the state gives you for exactly this. Four of those calls were attended. And the reason the district was thin that night has now been written down by the government itself, three years later, in a document it published about its own conduct.
<!-- IT-13, IT-18, IT-10, IT-12 ✓ -->

Three years is a long time for a sentence like that to take.
<!-- IT-12 ✓ VERBATIM · OURS -->

By the time it was published, the courts had already finished with it, and so had the Constitutional Court.
<!-- IT-30, IT-35, IT-72 ✓ VERBATIM -->

---

## ACT_5 — NOBODY ORGANISED IT

【Pictures: a corridor with a bench → a stack of files → a closed door → a row of empty chairs. NO GAVEL — Korean courts do not use one. NO COURTROOM RECONSTRUCTION.】

Three separate state bodies looked at that night, and they gave three different answers, in this order.
<!-- IT-72, IT-30, IT-10 ✓ — the act's spine -->

【Pictures: a chamber, empty, at distance → a vote board, blank, composited → a bench of nine chairs.】

The first was the Constitutional Court.
<!-- IT-72 ✓ VERBATIM -->

In February 2023, the National Assembly voted to impeach Lee Sang-min, the Interior and Safety Minister, over the disaster.
<!-- IT-71 ✓ SECONDARY -->

On the twenty-fifth of July that year, all nine judges of the Constitutional Court rejected the impeachment, unanimously, and he was reinstated as minister.
<!-- IT-72 ✓ VERBATIM · ⛔-04 — outcome, date and court in the same sentence -->

【Quote card. Attributed: "Constitutional Court of Korea, 25 July 2023".】

The court's reasoning was that the emergency response system used to handle the incident was not significantly deficient, given the frequent communication and coordination between the ministry, the police and the Itaewon district office.
<!-- IT-73 ✓ VERBATIM -->

Hold that sentence next to the one you heard four minutes ago, from the government's own audit, two years later. Not significantly deficient. And: a key factor behind the lack of crowd control officers in Itaewon.
<!-- IT-73, IT-10 ✓ VERBATIM — the film's central juxtaposition -->

Both are official. Both are in writing. They are about the same night.
<!-- IT-73, IT-10 ✓ VERBATIM -->

【Pictures: the corridor again → a date stamp → a stack of files.】

The second body was a criminal court.
<!-- IT-30 ✓ VERBATIM -->

On the thirtieth of September, 2024, the Seoul Western District Court delivered its judgment on the officials who had been indicted over that night.
<!-- IT-30, IT-36 ✓ VERBATIM -->

Everything that follows is a first-instance judgment. That distinction is going to matter before the end of this act.
<!-- AB-02 ✓ ABSENCE — flagged early -->

Lee Im-jae, then fifty-four, the former chief of the Yongsan police station, was sentenced at first instance that day to three years in prison without labour, on charges of professional negligence resulting in death and injury.
<!-- IT-30 ✓ VERBATIM · ⛔-04 -->

【Quote card.】

The court's reasoning was that the danger had been visible in advance: that it was either foreseen or it could have been anticipated that a large crowd of people gathering at the slanted alleyway in Itaewon for the 2022 Halloween could cause a serious danger to bodies from pedestrians pushing.
<!-- IT-31 ✓ VERBATIM -->

The court found that he had neglected to establish and implement a safety management plan to prevent it.
<!-- IT-32 ✓ VERBATIM -->

Two others from the same police station were sentenced at first instance on the same day: Song Byung-ju, who had headed the station's one-one-two situation room, to two years without labour, and a former situation team leader to one year, suspended for two.
<!-- IT-37 ✓ VERBATIM · ⛔-04 -->

On the other charges against him — perjury before the National Assembly, and drawing up and using a false official document — the former station chief was acquitted at first instance.
<!-- IT-38 ✓ VERBATIM · ⛔-04 -->

【Pictures: a district office sign, at an angle, not legible → the corridor again → an empty chair.】

And then the same court, the same day, turned to the district.
<!-- IT-33 ✓ VERBATIM -->

Park Hee-young, the chief of the Yongsan ward office, and other ward officials, were also indicted. The same court found them not guilty.
<!-- IT-33 ✓ VERBATIM · ⛔-04 -->

Not *insufficient evidence*. Not *we cannot be sure*. Something more specific than that, and it is the sentence this whole film has been walking toward.
<!-- IT-34 ✓ VERBATIM -->

【THE LARGEST QUOTE CARD IN THE FILM. Held 6.0 s. Attributed: "Seoul Western District Court, 30 September 2024".】

Related law and regulations did not require them to come up with safety measures for events without organizers.
<!-- IT-34 ✓ VERBATIM -->

And: there were no obligatory regulations specifying the need to establish separate safety management plans.
<!-- IT-34 ✓ VERBATIM -->

In the court's own language, it was hard to find that the district chief bore a specific and direct professional duty of care, under the disaster and safety laws, to add to, revise or supplement a safety management plan in preparation for Halloween 2022.
<!-- IT-34a ✓ VERBATIM -->

【Hold. Cut to the width line, silent, one last time. 2.5 s. No figure. Then black.】

That is not a loophole somebody found. It is what the law said.
<!-- IT-26, IT-27 ✓ SECONDARY -->

Under South Korea's framework law on disaster and safety management, a voluntary event with no organiser did not have to notify the police or the fire service of a safety plan in advance, and it was ambiguous where responsibility for safety on the ground actually sat.
<!-- IT-26 ✓ SECONDARY -->

Until the law was revised, it set out administrative duty and liability for official events and for local festivals — the ones where it was clear whose event it was.
<!-- IT-27 ✓ SECONDARY -->

A hundred thousand people walking into a district because it is the twenty-ninth of October is not anybody's event. There is no form for it. And so, in the judgment of that court, there was no duty attached to it.
<!-- IT-26, IT-34, IT-55 ✓ -->

【Pictures: a statute page composited in Remotion, blank of any real typeface → an article number drawn onto it → a date. NO PHOTOGRAPH OF A REAL LEGAL DOCUMENT — ⛔ fabricated_record.】

There is now.
<!-- IT-79 ✓ VERBATIM (PRIMARY) -->

Article sixty-six dash eleven of the Framework Act on the Management of Disasters and Safety is titled *safety management measures when holding a local festival*. It was inserted into that act in 2013. On the twenty-sixth of December, 2023, its first paragraph was amended.
<!-- IT-78 ✓ VERBATIM (PRIMARY) -->

【THE SECOND-LARGEST QUOTE CARD IN THE FILM. Held 6.0 s. Attributed: "Framework Act on the Management of Disasters and Safety, Article 66-11(1), amended 26 December 2023 · Korea Law Information Center".】

Where a local festival at which the participation of a crowd is expected has no organiser, or its organiser is unclear, the head of the competent local government shall establish a local-festival safety management plan, taking into account the expected scale of participants and the venue.
<!-- IT-79 ✓ VERBATIM (PRIMARY) — the statute, read in the statute -->

That is the sentence. On the night this film is about, it was not law.
<!-- IT-79 ✓ VERBATIM (PRIMARY) · OURS -->

And one thing has to be said about the order of those dates, because it is easy to get backwards. The amendment was already law in September 2024, when that court delivered the acquittal. The court was not ignoring it. A criminal court applies the law as it stood on the night in question, and on the night in question the sentence did not exist.
<!-- IT-78, IT-79, IT-30, IT-34 ✓ · ⛔-04 -->

【Pictures: a parliamentary chamber, empty, at distance → a stack of bills, blank → a calendar page.】

Seventeen lawmakers proposed bills to fix it, making the head of a local government liable where a large crowd is expected.
<!-- IT-28 ✓ SECONDARY -->

A year after the disaster, in October 2023, the Korea Herald reported that a year of parliamentary debate had produced no legislation holding a local government legally liable when people are hurt while crowded into a public space.
<!-- IT-29 ✓ SECONDARY · ⛔-11 -->

There is one more acquittal in this record.
<!-- IT-35 ✓ VERBATIM -->

Kim Kwang-ho, the former Seoul police chief and the highest-ranking officer indicted over that night, was acquitted on the seventeenth of October, 2024, along with two other police officers. The court said it was hard to establish beyond reasonable doubt, with the evidence put forward by the prosecution, that the defendants committed professional negligence.
<!-- IT-35 ✓ VERBATIM · ⛔-04 -->

【Pictures: a filing counter → a date stamp → a document tray.】

On the seventh of October, 2024, prosecutors appealed. They appealed against the former station chief, against the district office chief, against four other police officers and three other ward officials.
<!-- IT-39 ✓ VERBATIM -->

Their grounds, as reported by MBC, were that although the defendants' negligence and its consequences were very grave, they were shifting the blame and not seriously reflecting; that the court had misapprehended the law on the district chief's duty under the disaster and safety act; and that on the false-document acquittal, the time of arrival at the scene and other matters had plainly been recorded falsely.
<!-- IT-39 ✓ VERBATIM · ⛔-11 -->

【Black. 1.5 s. No picture. This is the film's one designed silence.】

And here this film stops, because the honest thing to do is tell you what it does not know.
<!-- AB-02 ✓ ABSENCE -->

Those appeals went to the Seoul High Court. As this film was made, no appellate judgment in any of these cases could be verified, in English or in Korean, and no Supreme Court decision exists that this production has been able to confirm.
<!-- AB-02, AB-03 ✓ ABSENCE -->

So nothing you have just heard is final. One conviction and several acquittals, all at first instance, all under appeal, and a record that is still moving.
<!-- IT-30, IT-33, IT-35, IT-39, AB-02 ✓ · ⛔-04 -->

【Pictures: a lectern from behind → a chamber → a folder marked only with a date.】

The third body is still working, and it is the reason this story is not over.
<!-- IT-43, IT-49 ✓ -->

In January 2024, the President at the time, Yoon Suk Yeol, rejected a special act to investigate the disaster; the government's argument was that an opposition-driven investigation committee undermined constitutional principles.
<!-- IT-41 ✓ SECONDARY -->

A commission was eventually established, in September 2024, with a name that is itself a sentence: the National Commission for the Investigation of the October 29 Itaewon Disaster and Prevention of Recurrence.
<!-- IT-43 ✓ VERBATIM (name) / SECONDARY (date) -->

In July 2025 a new President, Lee Jae Myung, ordered the setting up of a further investigation team of police and prosecutors, to work alongside it.
<!-- IT-44 ✓ VERBATIM -->

【Quote card.】

He apologised. As the head of the state, he said, I would like to formally apologize on behalf of the government for failing to fulfill its responsibility to protect the lives and safety of the people.
<!-- IT-45 ✓ VERBATIM -->

At the same time, a lawyer representing the victims' families, Song Hae-jin, said police records and information about the government's response had been withheld from the commission.
<!-- IT-46 ✓ VERBATIM -->

In March of this year the commission held an investigative hearing at which a survivor testified and police officials traded blame.
<!-- IT-47 ✓ SECONDARY -->

In May it asked prosecutors to investigate the district office chief again, and a former Itaewon station chief over an allegation of perjury at a parliamentary hearing.
<!-- IT-48 ✓ VERBATIM · ⛔-04 -->

And in June it concluded that it needed another year and three months, extending itself to December 2027, and said it would be looking upward — at the chain of command, including the Office of the President and the Office of National Security.
<!-- IT-49 ✓ SECONDARY -->

Four years on, the question of who was responsible for that street is still open, and it is being asked higher up than it was.
<!-- IT-49 ✓ SECONDARY -->

---

## ENDING

【Pictures: World Food Street, present day, evening → the temporary median barrier, low, plastic, running down the middle → a warning sign → traffic police at distance → a CCTV housing on a pole → the alley, from the top, ordinary. HERO: the barrier. Still cut 3.8 s, scale 1.000→1.055.】

Go to Itaewon now, on the last weekend in October, and you will find that something has changed.
<!-- IT-50, IT-51, IT-52 ✓ VERBATIM -->

There is a temporary median barrier down the middle of World Food Street, put there to make people walk one way.
<!-- IT-50 ✓ VERBATIM -->

Officers and station staff guide people through the underground station to stop it backing up. A mobile patrol unit starts at six in the evening. Streets are checked for hazards, and somebody makes sure the cameras and the emergency bells work. When the road gets crowded, traffic police blow whistles.
<!-- IT-51 ✓ VERBATIM -->

And there are signs. The Korea JoongAng Daily quoted one of them: crowded areas can be dangerous.
<!-- IT-52 ✓ VERBATIM · ⛔-11 -->

【Hold on the sign, 3.0 s.】

Above all of that there is now a system, and the Seoul Metropolitan Government describes it in its own words as an intelligent people counting system, which automatically monitors crowding and raises alarms if it detects signs of dangerous crowd problems.
<!-- IT-75 ✓ VERBATIM (PRIMARY) -->

Cameras connected to analytical software automatically calculate the number of people per unit area, and when they see something, they tell the local disaster situation rooms, the city government, the fire and disaster headquarters, and the police.
<!-- IT-76, IT-77 ✓ VERBATIM (PRIMARY) -->

The city listed seventy-one areas where large crowds were expected, and put nine hundred and nine cameras into them.
<!-- IT-77 ✓ VERBATIM -->

【Number card: "909 cameras · 71 areas". Held 3.0 s. Cut to the plastic barrier, low in frame.】

The page does not say at what density the alarm goes off, and this film is not going to invent a number for it.
<!-- AB-08 ✓ ABSENCE -->

Nine hundred and nine cameras, and a plastic barrier at knee height.
<!-- IT-77, IT-50 ✓ VERBATIM -->

That is the part worth sitting with. What was missing in that street was not technology and it was not money. It was a barrier, a direction, and somebody whose job it was to decide those two things before the evening started.
<!-- IT-50, IT-34 ✓ · OURS -->

The law now knows that a crowd can happen without anybody calling it an event. It learned that in December 2023, fourteen months late.
<!-- IT-27, IT-78, IT-79 ✓ -->

The act says who has to write the plan. A second document, the enforcement decree of the same act, says what has to be in it.
<!-- IT-81 ✓ VERBATIM (PRIMARY) -->

Article seventy-three dash nine. Where a festival has no organiser, or its organiser is unclear, the plan is written by the mayor, the county governor, or the district head with jurisdiction.
<!-- IT-81 ✓ VERBATIM (PRIMARY) -->

【Pictures: a five-item list drawn on, one line at a time, composited in Remotion. Stagger 3 f per line, translateY 48 → 0 px, spring damping 14, mass 0.6. NO REAL DOCUMENT IN FRAME — ⛔ fabricated_record.】

And the plan has to contain five things. An outline of the event. The person responsible for safety management, the organisation that manages it, and its duties. Measures to prevent loss of life from fire and from crowd concentration. A plan for securing and deploying safety-management personnel. And emergency response procedures, with the contact details of the relevant agencies.
<!-- IT-83 ✓ VERBATIM (PRIMARY) -->

That is the list. It is not long, and there is nothing clever in it.
<!-- IT-83 ✓ VERBATIM · OURS -->

Every line of it is the kind of thing somebody has to sit down and decide in advance, on paper, with their name on it — which is the one thing a street that belonged to nobody did not have.
<!-- IT-83, IT-26 ✓ · OURS -->

This film is not going to tell you what such a plan would have done on the twenty-ninth of October, 2022, because nobody has established that, and it is not a thing anybody can know.
<!-- AB-05 ✓ ABSENCE · ⛔-08, ⛔-15 -->

What can be said is that the list exists now, that it did not exist then, and that it is written in the language of the thing that happened: fire, crowd concentration, personnel, deployment, and who is responsible.
<!-- IT-83, IT-79 ✓ VERBATIM (PRIMARY) -->

It is worth knowing what that duty is still missing. In April of this year a member of the National Assembly proposed adding a penalty to it — an administrative fine of up to two million won for failing to draw up and file one of those plans, and an explicit power for a local government to demand that a bad plan be improved.
<!-- IT-82 ✓ SECONDARY -->

The reason given was that the duty was already a legal obligation, and there was no basis on which to sanction anybody who ignored it.
<!-- IT-82 ✓ SECONDARY -->

Three and a half years after a hundred and fifty-nine people died in a street that belonged to nobody, the rule saying somebody must plan for a street that belongs to nobody exists — and the penalty for ignoring it was still a bill.
<!-- IT-22, IT-79, IT-82 ✓ -->

You go into crowds. Everybody does — a station at rush hour, a stadium emptying, a street at New Year. The next time you are in one and it stops feeling like a crowd and starts feeling like a current, the useful question is not whether somebody is watching. It is whether anybody has been given the job.
<!-- OURS — second-person turn -->

If this is the kind of thing you want more of — the mechanism rather than the headline — subscribe, and tell us in the comments which crowded place you have stood in that you would not stand in again.
<!-- OURS — the ask -->

【ENDCARD 9.0 s. BGM resolves on a musical cadence, not a cut.】
