# TOPIC PIPELINE v002 — EP53/54/55 slate (all 30-min) + ranked feeder
**Built 2026-07-26 by the theme-selection session (per `THEME_SELECTION_HANDOFF.v001.md`). Supersedes v001 for EP53+ selection; v001 remains the deep bench (38 picks + engine notes).**

**Owner directives applied (2026-07-26): EP53, EP54, EP55 are ALL 30-minute films.**

---

## 0. Evidence base (our own measured data, not guesses)

Sources: `scripts/_yt_studio_video_ctr.json` (Studio per-video CTR, 28-day window, cached 2026-07-25 22:43 — the live cookie 401'd on 07-26, it rotates <1h; refresh before next measurement) + `scripts/_yt_analytics.json` (Analytics API retention, cached 07-23) + `CTR_GROWTH_REFERENCE.v001.md` corpus engines.

1. **Title grammar is confirmed on OUR data**: curiosity-gap + villain + concrete number wins CTR — Caniglia "He Drove Home Honking…" **4.48%**, car-search "…Except One Place" **3.85%**, Kids for Cash "A Judge Took $2.8M…" **2.99%**, Terry **3.14% at 4,070 impressions**. Doctrine explainers die: Kelo 0.81%, Mahanoy 0.52%, Tekoh 0.70%.
2. **The wrongful-conviction cluster retains best but was packaged worst**: Hinton = top-2 long-form retention (27.4% AVP) yet CTR only **1.35%** on 2,880 impressions because the title carried no dramatic-irony/time-jump number. → Every EP53+ title MUST carry the time-jump/count number.
3. **Narrative long-form is the suggested-traffic engine, validating 30-min**: Titan (36 min) pulled the channel's most impressions (4,292) AND the longest watch-from-impression (525 s); Gardner (27 min) 24.1% AVP / 396 s. Narrative long-form yields 3-4× the watch-time per view of 12-min explainers at comparable AVP. The old "kill 27-36 min" reading applied to *doctrine/finance explainers* (Swartz 27 min = 4.0% AVP), not narrative films. 30 min stands ONLY with a multi-act story (≈8+ beats, reversal every ~75-90 s of story time).
4. **Corpus story engines** (Part F): ① confession/interrogation drama **5.36×** (strongest, barely used by our slate so far), ② vivid named villain 2.79×, ③ relatable family victim 1.64×, ④ wronged innocent 5.3×. Best arcs end with *real killer revealed* and/or *villain punished* (EP52 Morton = both).

## 0b. Novelty gate — run 2026-07-26, PASS

Inventory at check time: **EP1–52 on disk** (`PD-2026-001-miranda … PD-2026-052-morton`; EP53 is the next number). Grepped: `episodes/` (all dirs/files incl. `09_package/youtube_meta*.json`, `03_script/`, `_planning/EP*_fact_recheck`), `scripts/build_*`, `docs/`, `decisions/`, `config/` — case-insensitive, by case name + party names + slugs. **All 16 v001-feeder candidates and all 12 new-research candidates: ZERO duplicates, zero slug/build-script collisions.** (Full per-candidate evidence in section 4.) Three cross-candidate constraints found — see section 3.

---

## 1. THE SLATE (recommended)

| EP | Topic | Runtime | Why this slot |
|----|-------|---------|---------------|
| **EP53** | **The Norfolk Four** | 30 min | Only candidate firing ALL four engines at full power; the 5.36× confession engine IS the 30-min spine; double payoff (killer + detective both imprisoned) |
| **EP54** | **Curtis Flowers** | 30 min | "Six trials" = a built-in act structure; the most vivid living named villain in the canon, condemned by name in a SCOTUS opinion |
| **EP55** | **Jon Burge torture ring** | 30 min | Confession-factory at system scale + villain actually jailed + first-ever US police-torture reparations; escalates the slate from person → prosecutor → institution |

Slate logic: three distinct villain shapes (one detective / one DA / one institutional torture crew), three distinct arcs (domino false confessions / marathon retrials / decades-long cover-up exposed), all in the proven US wrongful-conviction suggested cluster, all guardrail-clean. Bold wildcard available: **Hakamada (#4)** can swap into EP55 if the owner wants the international mega-number bet (see entry).

---

## 2. RANKED CANDIDATES (EP53+)

### 1. The Norfolk Four → **EP53** ★30-min 5/5
- **切り口 (angle)**: The domino nightmare — four separate innocent sailors talked into confessing to the same murder, each new DNA mismatch producing a NEW suspect instead of a release; and the detective who did it ends up in federal prison. Frame: *"the film Frontline couldn't finish"* — the only famous doc (2010) predates the entire third act (2011 Ford conviction, 2016 vacatur, 2017 absolute pardons, 2018 $8.4M).
- **Hook (one line)**: "4 Men Confessed to 1 Man's Murder — 20 Years Later, the Detective Went to Prison."
- **Story engines**: ①×4 (the whole spine is interrogation collapse — 11-hour sessions, death-penalty threats, fake polygraphs) + ② Det. Robert Glenn Ford (named, convicted) + ③ victim Michelle Moore-Bosko, 18-year-old Navy wife + ④×4. **Payoff: BOTH** — Omar Ballard (sole DNA match, confessed alone, pleaded guilty 2000) AND Ford sentenced to 12.5 years federal (extortion/lying to FBI, 2011). One of the only US cases where the interrogating detective himself went to prison.
- **30-min beats (9+)**: murder → Williams' 11-hr confession → DNA mismatch #1 (Reversal A: they find a SECOND man instead) → Dick/Tice/Wilson cascade to an evidence-free "8-man gang" theory → Ballard's prison letter + sole DNA match (Reversal B) → prosecutors keep the four convicted anyway → 26 FBI agents + 10 former AGs campaign → conditional pardons 2009 → Ford convicted Oct 2010 (sentenced Feb 2011, 12.5 yrs) → Oct 2016 federal vacatur (Gibney) → 2017 absolute pardons → $8.4M (2018). *(R3 correction 2026-07-26: the oft-cited "By any measure, extraordinary" quote could not be verified against the opinion — do not use it; the script's Gibney quotes are the verified verbatims.)*
- **Novelty**: NEW — zero hits anywhere in episodes/ (only the v001 proposal listing). Engine-adjacent to EP39 frazier / EP50 centralpark but the case is absent. Constraint: **Beatrice Six (v001 #37) is the same engine at the same extreme — benched while Norfolk is built.**
- **Thumbnail CTR angle**: four silhouetted sailors in white Navy caps under a single interrogation lamp; red-bar text "ALL 4 CONFESSED" / "0 WERE GUILTY". Title carries the count + time-jump numbers.
- **Living-persons sensitivity**: all four exonerees alive but FULLY pardoned + vacated = protagonist-safe. Ford alive (released ~2021-22) — defamation-proof via his own federal conviction + federal court findings. Ballard convicted lifer, safe to name. **Care**: victim's parents long believed the four guilty — treat the family with restraint or omit. Rape element verbal/off-screen only (ad-safety MEDIUM, Frontline precedent).
- **Confidence**: HIGH. Full engine stack + double payoff + under-saturated (definitive doc is 15 years stale) + US military protagonists for a US-centric audience.
- Sources: PBS Frontline (Ford); CBS (2017 pardons); Criminal Legal News ($8.4M); Navy Times (settlement).

### 2. Curtis Flowers → **EP54** ★30-min 5/5
- **切り口**: One prosecutor, one man, six trials, 23 years — told as a numbers-driven thriller ("6 trials, 4 death sentences, 2 hung juries, 1 man"), with the midpoint bombshell that the state's star witness fabricated his story AND later committed a triple murder.
- **Hook**: "Tried 6 Times by the Same Man. 4 Death Sentences. 23 Years. Then Every Charge Was Dropped."
- **Story engines**: ② strongest living named villain available — DA Doug Evans, condemned by name in Flowers v. Mississippi (2019, 7-2, Kavanaugh: "relentless, determined effort to rid the jury of black individuals") + ④ maximal + ③ (four murder victims incl. a 16-year-old) + ① half (Hallmon's fabricated jailhouse confession, pressured witnesses). **Payoff — tell it honestly**: Flowers free + $500k + 2023 civil settlement; voters rejected Evans (2022), retired 2023, law-license suspension petition 2025. But the real killer was NEVER identified and Evans was never criminally punished (immunity). The honest ending = SCOTUS names the villain, the town votes him out.
- **30-min beats (10)**: Tardy Furniture murders → Evans fixes on Flowers → trials 1-3 convictions, each REVERSED for Evans' own misconduct → trials 4-5 hung on racial lines → trial 6 death → In the Dark demolishes the case (Reversal A) → Hallmon recants on tape + his 2016 triple murder revealed (Reversal B) → SCOTUS 2019 → charges dropped 2020 → aftermath/reckoning.
- **Novelty**: NEW — only the v001 proposal listing. Prosecutorial-misconduct adjacency to EP41 Connick and EP52 Morton; no case overlap. **Spacing note: schedule after EP52 Morton with EP53 between them — both are "prosecutor villain" arcs.** (Satisfied by this slate order.)
- **Thumbnail CTR angle**: one silhouetted man facing six courtroom doors/gavels in a row; "TRIED 6 TIMES" big / "0 EVIDENCE". The count "6" is the CTR asset.
- **Living-persons sensitivity**: Flowers alive, fully exonerated = safe. **Evans ALIVE and never punished** — defamation-proof ONLY by quoting the SCOTUS opinion and reversal records verbatim (strongest privilege); no editorializing beyond the record. Hallmon convicted triple murderer, safe. **Do NOT name In the Dark's alternative suspect (living, never charged).** Race-charged (jury strikes) → silhouette rule.
- **Confidence**: HIGH. Podcast-famous but YouTube-thin (news clips only); the numbers-thriller cut is unclaimed.
- Sources: APM In the Dark (Hallmon recantation, updates); Flowers v. Mississippi 593 U.S.; Mississippi Today (license petition 2025); Bolts (Evans retires); 60 Minutes 2021.

### 3. Jon Burge torture ring (Chicago) → **EP55** ★30-min 5/5
- **切り口**: The confession factory — a decorated commander's "Midnight Crew" electro-shocked and suffocated 100+ Black men into confessions for 20 years; the statute of limitations made torture unprosecutable, so the feds jailed him for LYING about it. The law's own irony is the engine.
- **Hook**: "He Tortured 100+ Confessions Out of Innocent Men. They Could Only Jail Him for Lying About It."
- **Story engines**: ① at industrial scale (the extreme of the 5.36× engine) + ② named villain ACTUALLY JAILED (4.5 years, perjury/obstruction, 2010) + ④ (20+ exonerations, death-row inmates freed). **Payoff**: villain imprisoned + the first police-torture reparations in US history (2015: $5.5M package + formal apology + mandatory Chicago-schools curriculum) — a payoff shape no other candidate has.
- **30-min beats (9)**: Vietnam-vet commander rises → the Midnight Crew's methods → death sentences built on tortured confessions → a doctor's ignored warnings → journalist's decades-long dig (John Conroy) → fired but untouchable (limitations wall) → the federal perjury gambit → conviction 2010 → reparations 2015 + Death-Row-10 exonerations aftermath.
- **Novelty**: NEW — zero hits (the only "Burge" hit in the repo is a false positive on Chief Justice "Burger" in EP45's script). No slug/build collision.
- **Thumbnail CTR angle**: electrodes + a police badge; "100+ TORTURED CONFESSIONS" / "JAILED FOR LYING." Restraint-styled (dark, documentary), no gore.
- **Living-persons sensitivity**: Burge died 2018, convicted — safe. Victims/exonerees mostly alive and public advocates (sympathetic). Torture depiction = sound/shadow abstraction only, ad-safety MEDIUM. Race-charged → silhouette rule.
- **Confidence**: HIGH. Heavily reported but no definitive YouTube long-form; connects to the channel's Miranda/confession doctrine spine without becoming an explainer.
- Sources: ACLU (reparations); Chicago Torture Justice Center; federal conviction record 2010.

### 4. Iwao Hakamada (Japan) ★30-min — BOLD WILDCARD (swap-in for EP55, or EP56+)
- **切り口**: The world-record number nobody in English long-form has claimed: 46 years on death row (longest-serving death-row inmate in world history), acquitted at 88, evidence ruled FABRICATED, record ¥217M compensation (= ¥12,500 per day held), and a chief prosecutor bowing in apology in his living room. English-language long-form on this is a **vacuum** (news clips only — verified 2026-07-26).
- **Hook**: "46 Years on Death Row. The World Record. He Was Innocent — and They Paid Him $12 a Day for It."
- **Story engines**: ① 20-day interrogation forced confession (retracted at trial) + ④ + ③ (sister Hideko's 60-year fight — the parent-fights engine). **Payoff**: full acquittal 2024 (court: evidence fabricated) + record state compensation 2025 + prosecutor's personal apology. Reversal gold: Judge Kumamoto, who wrote the death sentence believing him innocent and repented publicly for decades (re-verify against primary sources at scripting).
- **30-min beats (8)**: boxer → miso-factory fire murders → 20-day interrogation → the "5 items of clothing" → death sentence + the dissenting judge's lifetime of guilt → decades in solitary, mental collapse → 2014 DNA release → 2024 acquittal → 2025 compensation + apology.
- **Novelty**: NEW — zero repo hits.
- **Thumbnail CTR angle**: old man silhouette in a cell; "46 YEARS" giant / "INNOCENT" stamp. The number is the biggest time-jump figure available in any candidate anywhere.
- **Living-persons sensitivity**: Hakamada alive (frail, represented by his sister — she is the public voice, sympathetic); legally FULLY acquitted = protagonist-safe. Villain is institutional (Shizuoka police/prosecution) — low individual defamation risk.
- **Confidence**: MEDIUM-HIGH. The story is top-1% raw material and the space is empty; the risk is lane-fit (our audience is US-centric, our franchise mark is "American Injustice"; suggested-cluster carryover unproven). Recommended play: hold for EP56+ as the international expansion test once the 30-min format has 2-3 US data points — OR swap into EP55 now if the owner prefers the bigger swing.
- Sources: Amnesty (2024 acquittal); CBS; record payout reporting (2025-03).

### 5. Walter McMillian ★30-min 4/5 — hold for EP56+ with packaging constraints
- **切り口**: The Mockingbird irony — Monroeville sold itself as the home of *To Kill a Mockingbird*, staging the play yearly, while framing a real Black man for murder a mile from the museum. This angle, NOT the Just Mercy retread, is the differentiation (the movie made this case the most saturated of the Tier-S set).
- **Hook**: "The Jury Said Life. The Judge Said Death. The Town Was Busy Performing To Kill a Mockingbird."
- **Story engines**: ② Sheriff Tom Tate (on-record racist quote) + ④ maximal + ① half (Myers' coerced false testimony). **Payoff: WEAK — the anti-Morton.** No real killer ever identified; nobody prosecuted or disciplined; Tate kept getting re-elected; no apology ever; McMillian died 2013 with trauma-linked dementia. Payoff must be reframed as: this case built EJI and ended Alabama's judicial override.
- **30-min beats (8-10)**: murder in Mockingbird town → arrest despite church-fish-fry alibi with dozens of witnesses → **on death row 15 months BEFORE trial** → 1.5-day trial → jury votes LIFE, judge overrides to DEATH → Stevenson finds the hidden tape of Myers' first interview → 60 Minutes 1992 → exoneration 1993 → the dark aftermath.
- **Novelty**: NEW as a case — BUT **repeat-protagonist collision with EP29 Hinton**: Bryan Stevenson/EJI is EP29's Act-III hero (22 mentions in EP29 files; "Equal Justice Initiative" is already a published YouTube tag on EP29). **Binding packaging rules if built**: lead with the sheriff/DA frame-up + alibi, hold Stevenson to a late-act entrance, never say "Just Mercy" in the title, don't re-spend the EJI tag.
- **Thumbnail CTR angle**: silhouetted man behind death-row bars, small-town water tower behind; "GUILTY BEFORE TRIAL" or "TRIAL: 1½ DAYS".
- **Living-persons sensitivity**: McMillian d. 2013; Stevenson alive (hero); Sheriff Tate presumed alive — record-backed only (court records + bestselling memoir + studio film = effectively nil risk). Race-charged → silhouette.
- **Confidence**: MEDIUM-HIGH story, MEDIUM slot-fit (saturation + weak payoff + Stevenson repeat). Right home: EP56+ spaced away from other Deep-South-sheriff arcs (NOT adjacent to a Groveland Four build, same shape).

### 6. Baltimore Gun Trace Task Force (Wayne Jenkins) ★30-min
- **切り口**: The elite police unit that WAS a robbery crew — told from the victims'/mass-exoneration side (≈800 convictions overturned/dismissed), which is exactly the side HBO's drama and the theatrical doc did NOT center.
- **Hook**: "The City's Elite Gun Squad Was a Robbery Crew With Badges. 800 Convictions Died With It."
- **Story engines**: ② Jenkins (25 years federal, 2018; 8 officers convicted) + ③ (citizens robbed/planted) + ④ (the ~800). **Payoff**: pure villain-punished, plus a live epilogue (Jenkins seeking early release, 2026).
- **Beats**: hero cop myth → robberies/planted guns/drug resale → FBI wiretap → Det. Sean Suiter's death the day before his grand-jury testimony (MUST stay both-theories, undetermined) → arrests → trial → mass vacatur → now.
- **Novelty**: NEW — zero repo hits. **Saturation is the catch**: HBO's We Own This City + the doc I Got a Monster = highest saturation of the new finds; the victims-side cut is the only defensible angle.
- **Thumbnail**: badge + banded cash + handcuffs; "THE POLICE WERE THE ROBBERS."
- **Sensitivity**: villains all convicted (safe); Suiter death legally undetermined — both-theories framing mandatory.
- **Confidence**: MEDIUM-HIGH content, MEDIUM differentiation. Feeder, not the 53-55 slate.

### 7. UK Post Office Horizon scandal ★30-min
- **切り口**: For a US audience: a corporation's software bug prosecuted 900+ innocent small postmasters, and the UK had to pass an unprecedented LAW to mass-exonerate them. Angle = "a company was allowed to run its own prosecutions."
- **Hook**: "1 Bug. 900 Criminals. 0 Crimes. Parliament Had to Legalize Their Innocence."
- **Story engines**: ② Paula Vennells (CBE stripped, wept at the public inquiry) + ③ family-shop postmasters (suicides, a woman imprisoned pregnant) + ④ at record scale. **Payoff incomplete**: no individual criminal conviction yet (inquiry ongoing) — the payoff is the unprecedented blanket-exoneration act + CBE stripping.
- **Novelty**: NEW — zero repo hits. UK-saturated (ITV drama), **US YouTube long-form thin** = the opening.
- **Sensitivity**: Vennells alive, NOT criminally charged — stick strictly to inquiry findings/court judgments; never assert "she lied" beyond the record.
- **Confidence**: MEDIUM. Strongest mass-scale number; weakest villain-payoff of the top group. EP56+ feeder.

### 8. Jeffrey Deskovic — strongest 20-min bench (NOT for the 30-min slate)
- **Hook**: "The DNA Excluded Him. The Jury Convicted Him Anyway. The Real Killer Killed Again While He Sat in Prison."
- **Engines**: ① (16-year-old, 7-hour interrogation, false confession) + ④; **payoff full** — DNA hit on Steven Cunningham, who had murdered Patricia Morrison DURING Deskovic's 16 years; $41.6M verdict; Deskovic became a lawyer.
- **Novelty**: NEW. **Runtime honesty: 20 min, not 30** — 6-7 beats. Queue for the next 20-min slot. Sensitivity: Deskovic alive, fully exonerated, self-public (low risk); Cunningham convicted.
- **Confidence**: HIGH for its length class.

---

## 3. Cross-candidate constraints (from the novelty sweep — binding on future picks)

1. **Norfolk Four vs Beatrice Six**: same engine (multi-person false-memory confession) at the same extreme. Norfolk chosen → Beatrice Six benched indefinitely (revisit only with a distinct angle, e.g. false-memory science).
2. **McMillian ↔ EP29 Hinton**: repeat-protagonist (Stevenson/EJI). Packaging rules in entry #5 are binding.
3. **McMillian ↔ Groveland Four**: same corrupt-Southern-sheriff shape — never adjacent in the schedule.
4. **Troy Davis / Carlos DeLuna**: both "executed despite doubt" — EP51 Willingham holds that emotional slot; space any of these 10+ episodes out.
5. **Kalief Browder ↔ EP50**: word-only Rikers overlap, but visually the same setting one cluster after EP50 — if built, differentiate the visual language.
6. Rejects for the 30-min slot (honest structural calls): **Stinney** = 18-22 min story (83-day arc, no middle) + double child ad-safety burden; **Scottsboro** = 90-min sprawl, best future cut is a ~20-min Judge Horton film; **Brown v. Mississippi** = 12-15 min story → short/cold-open material; **Christopher Tapp** = pending homicide trial of a living defendant (Rodimer) → frozen until verdict; **Sally Clark/Meadow** = villain unpunished + protagonist's tragic death, no payoff (revisit only as a bundled "Meadow's Law" film).

## 4. Novelty-gate evidence (per candidate)

All checks run 2026-07-26 against EP1-52 + `_planning` + `scripts/build_*` + `docs/` + `decisions/` + `config/`, case-insensitive, by case + party names:
- **NEW, zero hits beyond v001 proposal listings**: Norfolk Four (incl. all 4 sailors + Ballard), Curtis Flowers (+Evans, Winona), Burge, Hakamada, GTTF/Jenkins, Post Office/Vennells, Deskovic, McMillian (+Monroeville, Just Mercy — zero hits inside EP29 hinton dir), Scottsboro/Powell, Brown v. Mississippi/Ellington, Stinney, Browder ("Rikers" hits are EP50's Korey Wise passages only), McCollum/Brown, Ricky Jackson, Troy Davis, Guildford/Birmingham Six, Beatrice Six, Groveland, Graves, Porter, DeLuna, Kiszko, Timothy Cole, Elkins, Malcolm X exonerations (Aziz/Islam), Bergwall, Watts, Tapp.
- **False positive logged**: "Burge" ≈ "Burger" (Chief Justice) in `EP45_bearden_script.en.v001.md:159`.
- Known thematic adjacencies (not dupes): EP29 Hinton (AL death row), EP30 Cotton (eyewitness), EP39 Frazier (police-lie confession), EP41 Connick (Brady), EP50 CP5 (coerced juvenile confessions), EP51/52.

## 5. Remaining deep bench

v001 picks #3-38 not promoted above stay live as the feeder (Korematsu, Whren, Garner, Roper/Miller, Ferguson, Bloodsworth, WM3, Carter, Adams, Simmons, Dookhan/Farak, Tulia, Flowers-adjacent doctrine anchors, etc.), PLUS new-research bench: **Stefan Kiszko** (UK, 20-min, full killer-payoff — strongest UK single-case), **Timothy Cole** (posthumous TX exoneration, ignored confession letters, his name became a law), **Clarence Elkins** (solved his own case with a cigarette butt in prison — ad-safety caution), **Malcolm X exonerations** ($36M, 55-year jump — differentiate from Netflix by centering the two men, not "who did it"), **Sture Bergwall** ("8 murders, 0 victims" — Sweden, bizarre-index #1), **Ronald Watts** (212-conviction mass vacatur, villain got only 22 months — irony play), **Ray Krone / Debra Milke / Ford Heights Four / Joyce Gilchrist / Fred Zain** (reserve).

## 6. Next actions

1. Owner approves/edits the EP53/54/55 slate (topic gate: state=approved).
2. On approval: packaging-first (lock title + thumbnail concept per CTR_PLAYBOOK.v002 BEFORE scripting), then 30-min scripts at the measured 178 wpm → **~5,300-5,400 narration words** for a 30:00 target (EP52 Morton convention; re-verify against `check_script_length.py` bands).
3. Refresh `secrets/studio_cookies.txt` (<1 h rotation) before the next CTR measurement pass; re-rank this file on our own per-video CTR after the 2026-08-08 re-measure.
4. Re-run the novelty slug check at build time (`ls -d episodes/*norfolk* *flowers* *burge*` etc.) per `pd-topic-novelty-gate`.

*Provenance: novelty sweep + Tier-S 30-min deep-dive + fresh outlier research executed by 3 parallel agents 2026-07-26; all shocking-fact claims carry web sources in the entries above and MUST be re-verified in each episode's fact_recheck at script time (invariant 1). Confidence labels are per-entry. No build files touched; nothing scheduled or published.*
