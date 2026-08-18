# TOPIC PIPELINE v001 — Prime Documentary (feeder for EP51+)
**A ranked, evidence-tied, novelty-checked list of high-outlier-potential topics for the channel's lane.** Built 2026-07-24 from the 62,527-video corpus theme-mining (see `CTR_GROWTH_REFERENCE.v001.md` Parts F–G). Companion to that reference. Consult before proposing any new episode; re-run the novelty gate (`pd-topic-novelty-gate`) at build time in case the inventory has grown.

> **Selection logic (evidence-first, top-1% not average).** The corpus says the top of our lane is powered by four stackable STORY ENGINES (Part F): **① confession/interrogation drama (5.36× lift), ② a vivid killer/villain (2.79×, in 24.5% of top-decile titles), ③ a relatable family victim (1.64×, 22.4%), ④ a wronged innocent ("wronged" 5.3× lift).** Pure SCOTUS-doctrine explainers carry NONE of these → structural CTR liability. So this pipeline is **tilted from doctrine toward character-driven injustice narratives** that stack multiple engines. Each pick is tagged with the engines it fires, a packaging angle (title grammar + thumbnail concept per the CTR_PLAYBOOK), a format length (per Part E: build these as **16–24-min narrative films, NOT 12-min explainers**), and an ad-safety flag.

> **Novelty status.** Re-checked **2026-07-25** against the now-**52-episode** inventory (slugs `PD-2026-001…052`, name-grep across `episodes/`). None of the **38** picks below (picks 1–18 + the 2026-07-25 EXPANSION BLOCK, picks 19–38) is a dedicated existing episode; two obvious cases (Dassey/Avery) were found already-rejected by an existing guardrail and are logged in the exclusion note. Where a case is *referenced inside* another episode as precedent, it's flagged. Already-covered adjacents noted so we don't repeat: EP29 Hinton, EP30 Cotton (eyewitness), EP36 Williams (facial-recog wrongful arrest), EP39 Frazier (police-lie false confession), EP41 Connick v. Thompson (Brady/hidden evidence), EP50 Central Park Five.

> **⚠ PIPELINE UPDATE 2026-07-25 — two Tier-S picks are now IN PRODUCTION:** **#1 Cameron Todd Willingham = EP51** (`PD-2026-051-willingham`) and **#2 Michael Morton = EP52** (`PD-2026-052-morton`). They are struck from the "build next" queue below (kept for their engine/packaging notes as templates). **Next-to-build from Tier S = #3 Walter McMillian, #4 Norfolk Four, #5 Scottsboro, #6 Brown v. Mississippi**, plus the newly added Tier-S picks in the 2026-07-25 EXPANSION block (George Stinney Jr., Curtis Flowers). **Packaging note for all picks:** apply the Phase-4 measured title grammar (CTR_GROWTH_REFERENCE Part I) — lead with the **dramatic-irony / time-jump** hook ("Executed. 20 Years Later, the Science Was Fake"; "He Didn't Know DNA Would Free Him 39 Years Later"), optionally a **dark adjective**, and wrap the slate in a **fixed franchise mark** (Part J, e.g. `… | American Injustice`). AVOID the cargo-cult features (when-clause / 2nd-person / quote-overlay / colon / superlative) — measured as channel-brand, not portable levers.

---

## TIER S — build these first (max outlier potential: 3–4 engines stacked, landmark recognition, ad-workable)

**1. Cameron Todd Willingham — "Texas Executed Him. The Fire Was an Accident."**  ✅ NOW IN PRODUCTION = EP51 (`PD-2026-051-willingham`)
- Engines: ④ wronged innocent + ③ family victim (his three daughters died in the fire) + ② villain = junk arson "science" / the state.
- Why outlier: the single most gut-wrenching premise in the wrongful-conviction canon — a father executed for a fire that forensic science later showed was accidental. "They killed an innocent dad" is the exact family-victim + wronged stack the data rewards, plus a timely systemic hook (forensic-science reform).
- Packaging: 3rd-person shock-verb title ("Texas Executed an Innocent Father — The Science Was Fake"); thumbnail = restrained anguished face + fire glow, red-bar "EXECUTED / THE FIRE WAS AN ACCIDENT."
- Length 20–24 min. **Ad-safety: MEDIUM** — child death + execution; treat with documentary restraint, no gore. Novelty: confirmed new.

**2. Michael Morton — "His Wife Was Murdered. The DA Hid the Proof He Was Innocent."**  ✅ NOW IN PRODUCTION = EP52 (`PD-2026-052-morton`)
- Engines: ④ wronged + ③ family victim (wife bludgeoned; his young son a witness) + ② villain (the prosecutor who buried evidence; and the real killer, who **murdered a second woman** while Morton sat in prison) + a Brady-law hook.
- Why outlier: near-perfect narrative arc (wrongful conviction → hidden evidence → a second victim → DNA exoneration → the prosecutor is himself jailed — a rare *justice-restored* ending). Distinct from EP41 Connick (different case, far stronger human story).
- Packaging: "They Hid the Evidence. An Innocent Man Rotted While the Killer Struck Again." Thumbnail = split mugshot-vs-family-photo, or the prosecutor's face + red circle.
- Length 22–24 min. **Ad-safety: OK** (adult homicide, no child). Novelty: confirmed new.

**3. Walter McMillian — "Framed for Murder in Monroeville (the Just Mercy Case)."**
- Engines: ④ wronged + ② villain (corrupt sheriff/DA, coerced witnesses) + ① coerced-testimony drama + race-injustice + built-in recognition (the *Just Mercy* film / Bryan Stevenson / EJI).
- Why outlier: borrowed authority (Just Mercy) + a Deep-South frame-up + a Black man on death row for a crime with an airtight alibi. Recognition + injustice = browse/suggested magnet.
- Packaging: "An Alibi in Front of a Whole Church — They Sent Him to Death Row Anyway." Thumbnail = defiant/weary face behind mesh, EJI-era restraint.
- Length 20–24 min. **Ad-safety: OK.** Novelty: confirmed new.

**4. The Norfolk Four — "Four Innocent Sailors Confessed to a Murder They Didn't Commit."**
- Engines: ① confession/interrogation drama (the **5.36× top engine**) + ④ wronged + ② villain (the detective who extracted the false confessions; the actual lone killer who later confessed).
- Why outlier: the definitive coerced-false-confession story — four separate innocent men talked into confessing to the same crime by interrogation pressure. Directly hits the highest-lift engine in the corpus, one our slate barely uses.
- Packaging: "How Do You Confess to a Murder You Didn't Commit? Four Men Did." Thumbnail = interrogation-room framing, timestamp, a broken face under the lamp.
- Length 20–24 min. **Ad-safety: MEDIUM** (rape/murder of the victim — keep off-screen, focus on the interrogation). Novelty: confirmed new.

**5. Scottsboro Boys / Powell v. Alabama — "Nine Teenagers, a Lie, and a Near-Lynching That Rewrote the Constitution."**
- Engines: ④ wronged + ② villain (a mob + a rigged system) + ③ young victims + landmark constitutional hook (6th Amendment right to counsel — a true doctrine ANCHOR wrapped in an unbearable human story).
- Why outlier: this is how to make a SCOTUS case a top-decile story — the doctrine (Powell v. Alabama, 1932) rides on nine Black teenagers pulled off a train, falsely accused, tried in a day, and nearly lynched. Massive historical weight, still-relevant themes.
- Packaging: "Nine Teens. One Lie. A Day to Live or Die." Thumbnail = period-authentic group behind bars, sepia, red-bar count "9."
- Length 22–24 min. **Ad-safety: MEDIUM** (historical rape accusation + racial violence — handle as history, sober tone). Novelty: confirmed new.

**6. Brown v. Mississippi — "They Whipped a Confession Out of Him. The Supreme Court Said Enough."**
- Engines: ① confession drama (5.36×) + ② villain (deputies who tortured) + ④ wronged + constitutional hook (coerced-confession / due-process landmark, 1936).
- Why outlier: visceral confession-engine case with a clean constitutional payoff; pairs as a "how confessions became inadmissible" companion to Miranda (EP1) and Frazier (EP39) without duplicating either.
- Packaging: "A Confession Beaten Out of Him — and the Case That Banned It." Length 18–22 min. **Ad-safety: MEDIUM** (torture depicted verbally). Novelty: confirmed new.

---

## TIER A — strong (2–3 engines; landmark + relevance; mostly ad-safe)

**7. Korematsu v. United States — Japanese-American internment.** ④ wronged (a whole community) + timely civil-liberties hook + landmark. "The Government Locked Up 120,000 Citizens — and the Supreme Court Said Yes." Length 20–24 min. Ad-safety OK. Novelty new. High-authority, emotional, evergreen-relevant.

**8. Whren v. United States — pretextual traffic stops ("driving while ___").** ② system-villain + strong 2nd-person relatability + hot topic (racial profiling). Fits the measured 2nd-person win for rights/explainer. "Any Cop Can Stop You for Anything — This Case Is Why." Length 16–20 min. Ad-safety OK. Novelty new. (More emotional than the average 4A explainer because of the profiling angle.)

**9. Tennessee v. Garner / Graham v. Connor — police use of deadly force.** ③ young victim (Garner: a 15-year-old shot fleeing an unarmed burglary) + high relevance/emotion + constitutional standard. "When Can Police Shoot You in the Back? The Case That Set the Rule." Length 18–22 min. Ad-safety MEDIUM. **Novelty check flag:** Garner is *referenced inside* EP14 (lange) — confirm it's not the episode's core before building; treat as new dedicated topic. 

**10. Roper v. Simmons / Miller v. Alabama — juvenile death penalty / juvenile life-without-parole.** ③ child defendant + ④ (moral-weight) + 8th-Amendment landmark. "He Was 17. They Sentenced Him to Die." Length 18–22 min. Ad-safety MEDIUM (juvenile crime). Novelty new. Pairs the youth-victim engine with a doctrine anchor.

**11. Ryan Ferguson — convicted on a "dream" confession; his father's 10-year fight.** ① confession drama + ④ wronged + ③ family (the father who never quit). "A Witness Dreamed the Crime — and an Innocent Teen Got 40 Years." Length 20 min. Ad-safety OK. Novelty new.

**12. Kirk Bloodsworth — first US death-row inmate exonerated by DNA.** ④ wronged + ③ child victim + ② real-killer reveal + a DNA-science hook. "The First Innocent Man DNA Pulled Off Death Row." Length 18–22 min. Ad-safety MEDIUM (child victim — keep restrained). Novelty new.

---

## TIER B — bench (high emotion, some recognition; watch ad-safety / saturation)

**13. West Memphis Three** — satanic-panic teen wrongful conviction; huge recognition (Paradise Lost / HBO). ④+② + built-in audience. Ad-safety MEDIUM-LOW (murdered children — handle very carefully; heavily covered elsewhere, so differentiate on the constitutional/false-confession angle). Novelty new.

**14. Rubin "Hurricane" Carter** — boxer wrongfully convicted; Dylan song + Denzel film = borrowed authority. ④ + race + recognition. Ad-safety OK. Novelty new.

**15. Randall Dale Adams (The Thin Blue Line)** — wrongfully convicted of killing a police officer; a documentary literally freed him (meta-hook). ④ + ② (the real killer) + confession-adjacent. Ad-safety OK. Novelty new.

**16. Glynn Simmons** — exonerated 2023 after ~48 years, the longest US wrongful imprisonment. ④ + timeliness ("longest ever, freed in 2023"). Ad-safety OK. Novelty new. Good news-jack candidate.

**17. Annie Dookhan / Sonja Farak — Massachusetts crime-lab fraud (~40,000 tainted convictions).** ② villain (the chemist who faked drug tests) + systemic scale. "One Chemist Faked the Tests. 40,000 Convictions Collapsed." Length 18–22 min. Ad-safety OK. Novelty new. Different flavor (white-collar villain + mass injustice) that still stacks villain+wronged+scale.

**18. Tulia, Texas drug sting** — one lying undercover agent, dozens of Black residents wrongly convicted. ② villain + ④ (many wronged) + race. Ad-safety OK. Novelty new.

---

---

## EXPANSION BLOCK — 2026-07-25 (picks 19–38; extends the feeder to 38 novelty-checked topics)
*Added in the Phase-5 pass. All novelty-confirmed against the 52-episode slug inventory (`PD-2026-001…052`) AND name-grepped across `episodes/` on 2026-07-25 (see the exclusion note at the end — two obvious "big" cases were found to be already-rejected by an existing guardrail). These are overwhelmingly **exonerees / cleared / posthumously-pardoned** subjects, which is the safe side of the living-convicted-person guardrail: the wronged-innocent IS our lane. Packaging for every pick applies CTR_GROWTH_REFERENCE Part I (dramatic-irony + time-jump + dark-adjective, franchise wrapper) and the **Part O mandate: import the outrage/reversal grammar onto the documentary — lead with the injustice + the reversal, never the literary line.** Length 16–24 min per Part E unless noted.*

### TIER S EXPANSION — build alongside picks #3–6 (4 engines, landmark recognition, decade-scale time-jump built in)

**19. George Stinney Jr. — "14 Years Old. Executed in 84 Days. Exonerated 70 Years Too Late."** Engines: ④ wronged + ③ child + ② race/system villain + ① rushed "confession" (no records, no defense). The youngest person executed in 20th-century America (1944, SC), conviction VACATED 2014 — a **70-year time-jump** (the largest in the whole feeder, Part I2's highest-lift lever native to the case). Packaging: "They Executed a 14-Year-Old. 70 Years Later a Judge Said He Was Innocent." Thumb = small boy dwarfed by an electric chair / period restraint, red-bar "AGE 14." **Ad-safety: MEDIUM-LOW** (child execution — sober history, zero sensationalism). Novelty: confirmed new.

**20. Curtis Flowers — "One Prosecutor Tried Him Six Times for the Same Murders."** Engines: ② villain (DA Doug Evans, serial misconduct) + ④ wronged + ① (jailhouse-snitch/coerced testimony) + built-in recognition (APM's *In the Dark* season 2; *Flowers v. Mississippi*, SCOTUS 2019, 7-2). Why outlier: the "**six trials**" number is an unbearable specific + a clean SCOTUS payoff; the villain is a single named prosecutor (Part F ②). Packaging: "Tried Six Times by the Same Man — The Supreme Court Finally Stopped Him." Thumb = weary face + a stamped "TRIAL 6." **Ad-safety: OK.** Novelty: confirmed new.

**21. Kalief Browder — "Three Years in Rikers for a Backpack He Never Stole. No Trial."** Engines: ④ wronged + ③ youth (16 at arrest) + ② system villain (bail/speedy-trial collapse, solitary) + huge recognition (Jay-Z/Spike TV doc). Why outlier: not a conviction at all — the injustice is **3 years jailed WITHOUT a trial** then released, a premise that reframes "innocent until proven guilty." Packaging: "16, Innocent, and Held 3 Years Without a Trial." **Ad-safety: MEDIUM** (he later took his own life — handle with grave restraint, focus on the system, follow the living-people/self-harm guardrails). Novelty: confirmed new. High-recognition news-adjacent.

**22. Henry McCollum & Leon Brown — "Two Disabled Brothers, a Coerced Confession, 30 Years on Death Row."** Engines: ① confession/interrogation drama (**the 5.36× top engine**) + ④ wronged + ② villain (the real killer, whose DNA freed them) + ③ (intellectually disabled teens). NC, 1983 → DNA exoneration 2014. Packaging: "They Signed a Confession They Couldn't Read. DNA Freed Them 30 Years Later." **Ad-safety: MEDIUM** (child victim — keep off-screen, focus on the interrogation). Novelty: confirmed new.

**23. Ricky Jackson — "39 Years for a Murder a 12-Year-Old Lied About."** Engines: ④ wronged + ② (the coached child witness who recanted) + a **39-year time-jump** (one of the longest US wrongful imprisonments; freed 2014 when the sole witness admitted he saw nothing). Packaging: "The Only Witness Was 12 and Lying. It Cost an Innocent Man 39 Years." **Ad-safety: OK.** Novelty: confirmed new.

### TIER A EXPANSION — strong (2–3 engines, recognition, mostly ad-workable)

**24. Troy Davis — "Seven of Nine Witnesses Recanted. Georgia Executed Him Anyway."** ④ wronged + ② (system) + global-campaign recognition (2011, "I Am Troy Davis"). The dramatic-irony of near-certain doubt + an irreversible outcome. "Doubt Is Supposed to Save You. It Didn't Save Troy Davis." **Ad-safety: MEDIUM** (execution — sober). Novelty new.

**25. Lindy Chamberlain — "'A Dingo Took My Baby' — and Australia Convicted the Mother."** ③ family/mother + ④ wronged + massive recognition (the phrase is global pop-culture; a royal commission overturned it). A mother wrongly convicted of killing her own infant, cleared when the baby's jacket was found. "The Whole Country Mocked Her. She Was Telling the Truth." **Ad-safety: OK** (infant death — restraint, no imagery). Novelty new. Rare international + top recognition.

**26. Carlos DeLuna — "Texas Executed Him for a Murder the *Other* Carlos Did."** ④ wronged + executed-innocent + dramatic-irony (mistaken identity; the real killer, Carlos Hernandez, bragged about it for years). Columbia Law's "Los Tocayos Carlos" investigation. "Two Men, One Name — Texas Killed the Wrong One." **Ad-safety: MEDIUM.** Novelty new.

**27. Anthony Porter — "48 Hours From Execution, Freed by a Journalism Class."** ④ wronged + a **ticking-clock** drama (measured his last meal; stayed twice) + the meta-hook that undergrad students (Northwestern's David Protess) proved his innocence and got the real killer to confess — the case that triggered Illinois's death-penalty moratorium. "He Was Two Days From Death. College Students Saved Him." **Ad-safety: OK.** Novelty new.

**28. The Groveland Four — "Framed by a Sheriff in 1949 Florida. Pardoned in 2019."** ④ wronged + ② villain (Sheriff Willis McCall) + race + a **70-year time-jump**; Pulitzer-winning *Devil in the Grove* (borrowed authority). "A Sheriff Framed Four Men. It Took Florida 70 Years to Admit It." **Ad-safety: MEDIUM** (racial violence — sober history). Novelty new.

**29. Timothy Evans — "Hanged for the Murders His Neighbor Committed."** ④ wronged + ② villain (serial killer John Christie, whose later confession exposed it) + wrongful-execution; the case that helped ABOLISH the UK death penalty. "They Hanged an Innocent Man — His Neighbor Was the Real Killer." **Ad-safety: MEDIUM.** Novelty new. International, clean villain-reveal arc.

**30. Joe Arridy — "'The Happiest Man on Death Row' Was Innocent — and Executed in 1939."** ④ wronged + ③ vulnerable (an intellectually disabled man who didn't understand his sentence, played with a toy train to the end) + posthumous pardon (2011, a **72-year** reversal). Devastating restraint-driven premise (Part C's calm-dissonance). "He Didn't Understand He Was Going to Die. Colorado Executed Him Anyway." **Ad-safety: MEDIUM.** Novelty new.

**31. Anthony Graves — "18 Years, 12 on Death Row, for a Crime the Killer Said He Did Alone."** ④ wronged + ② (a prosecutor's misconduct; the real killer recanted implicating him) + a **justice-restored arc** (freed 2010, became a reform advocate — a satisfying ending, like Morton). "The Real Killer Confessed He Acted Alone. It Still Took 18 Years." **Ad-safety: OK.** Novelty new.

### TIER B EXPANSION — bench (recognition or a distinct angle; watch ad-safety / saturation)

**32. The Guildford Four / Birmingham Six — UK IRA-bombing false confessions.** ① confession drama (5.36×, beaten/coerced) + ④ (wrongly jailed 15+ years) + recognition (*In the Name of the Father*). International; clean "confessions banned/overturned" payoff pairs with Brown v. Mississippi (#6). Ad-safety OK. Novelty new.

**33. Darryl Hunt — NC, 19 years for a rape-murder he didn't commit; DNA + a second confession.** ④ + race + documentary recognition (*The Trials of Darryl Hunt*). Ad-safety MEDIUM (adult rape-murder — off-screen). Novelty new.

**34. David Milgaard — Canada, 23 years wrongfully imprisoned; his mother's relentless crusade freed him.** ④ + ③ family (the mother, Joyce — a rare *parent-fights-for-child* engine) + the real killer (Larry Fisher) reveal + time-jump. Ad-safety MEDIUM. Novelty new. International.

**35. Glenn Ford — Louisiana, 30 years on death row, exonerated 2014; the prosecutor publicly apologized.** ④ + a rare *prosecutor-repents* beat + time-jump. Ad-safety OK. Novelty new. Good pairing with Morton (#2) on the "prosecutor reckons with it" theme.

**36. Leo Frank — 1913 Atlanta; wrongful conviction, commuted sentence, then lynched; the case birthed the ADL.** ④ + antisemitism + ② (a mob) + recognition. Ad-safety MEDIUM (lynching — sober history). Novelty new. Distinct historical/hate-crime angle.

**37. The Beatrice Six — Nebraska; SIX people were convinced by police they'd committed a murder none did (false-memory confessions).** ① confession engine at its most extreme (six false confessions to one crime — even beyond the Norfolk Four) + ④; DNA cleared all six. "Police Talked SIX Innocent People Into Confessing to the Same Murder." Ad-safety OK. Novelty new.

**38. Kerry Max Cook — Texas; ~20 years on death row across multiple trials for a murder later tied to another man.** ④ + ② (prosecutorial misconduct) + a marathon-trials arc (memoir *Chasing Justice*). Ad-safety MEDIUM (sexual homicide — restraint). Novelty new.

### ⚠ EXCLUDED BY EXISTING GUARDRAIL (do NOT queue — logged so they aren't re-proposed)
Name-grep surfaced that these were already **considered and rejected**, and the same rule bars them now:
- **Brendan Dassey** and **Steven Avery** (*Making a Murderer*) — REJECTED. EP39 planning (`EP41-43_TOPIC_PROPOSALS_v001.md`, `EP39_frazier_…`) already dropped Dassey on the **living-subject-whose-conviction-still-stands** guardrail (有罪確定・存命). Avery fails identically (living, conviction affirmed, innocence contested). Do not build them as protagonists.
- By the same guardrail, avoid **Amanda Knox** and **Adnan Syed** as *dedicated* wrongful-conviction films — living + legally unresolved/contested. (Knox: acquitted but the narrative is a living-person minefield; Syed: conviction reinstated then vacated then contested.) They may be *referenced* as precedent only.

### DOCTRINE ANCHORS AVAILABLE (use sparingly — 1 per ~3 narrative films, always wrapped in a protagonist per the Scottsboro model)
Not ranked as outlier picks (they fire NO character engine on their own, Part F), but kept as the "anchor" slot: **In re Gault** (juvenile due-process), **Escobedo v. Illinois** (counsel-during-interrogation, pre-Miranda), **Atkins v. Virginia** (barring execution of the intellectually disabled — pairs naturally with Arridy #30 / McCollum #22), **Batson v. Kentucky** (racial jury-strikes). Build any of these ONLY behind a human story, never as a pure explainer.

---

## HOW TO USE THIS
1. **Default to Tier S for EP51–55.** They stack the most measured engines and clear the ad-safety bar with documentary restraint. Willingham or Morton is the strongest single next pick (engine-density + arc).
2. **Build them at 16–24 min** (Part E), packaging-first: lock the shock-verb title + restrained-emotion thumbnail concept BEFORE the script (Part 1 §4 / CTR_PLAYBOOK).
3. **Balance the slate away from pure doctrine.** Keep 1 doctrine anchor per ~3 narrative films; when you DO run a doctrine case, wrap it in a human protagonist (the Scottsboro model) so it fires an engine.
4. **Re-run the novelty gate at build time** (`pd-topic-novelty-gate`): `ls -d episodes/*<slug>*` + name-grep, since the inventory grows.
5. **Feed winners back:** once we have our own per-video CTR/retention (still blocked — see reference Part H), re-rank this list on OUR outlier data, not just corpus inference.

*Confidence: topic-ENGINE mapping = MEDIUM-HIGH (measured corpus lifts, n≥900). Per-title outlier forecast = INFERRED — these are hypotheses to test with real packaging + our own CTR, not guarantees. Ad-safety flags are directional; do a per-episode YPP/advertiser-friendly review before production.*
