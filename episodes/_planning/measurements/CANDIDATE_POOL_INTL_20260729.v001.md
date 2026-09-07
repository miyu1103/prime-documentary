# CANDIDATE POOL — INTERNATIONAL & SYSTEMIC-SCALE INJUSTICE (EP57+)

**Built 2026-07-29. This is a POOL, not a slate. Nothing here is ranked into a build order, approved, scheduled or published. No build file was touched.**

**Scope (this file's lane).** Two families only:
- **(a) NON-US cases** — UK beyond the Post Office, Commonwealth (AU/CA/NZ/IE), Japan/Korea/Taiwan, European state failures.
- **(b) SYSTEMIC-SCALE cases** — where the victim count is large enough that *the story is the machine, not one person*. Several US entries appear for that reason only (crime-lab fraud, mass exonerations, tainted-evidence programmes). **Single-victim US institutional cases are a sibling pool-builder's lane and are deliberately absent.**

**Pool size: 44 candidates assessed — 43 live + 1 formally dropped (§4.1).** One further *framing* is dropped without dropping its candidate (§4.2), and one earlier drop is **reversed on evidence** (§4.3). Plus 8 pre-existing bench entries re-confirmed and left where they are (§1.4).

**Inventory at check time: 56 episode directories, `PD-2026-001-miranda` … `PD-2026-056-postoffice`.** No `EP57+` directory exists on disk. 89 `09_package/youtube_meta*.json` files present.

---

## 0. THE FOUR CONSTRAINTS THAT SHAPE EVERY ENTRY

### 0.1 ⚠ PROTAGONIST TYPE IS THE DECISIVE VARIABLE (criterion update, 2026-07-29)

A sibling scan of **3,656 videos via the YouTube API** found that identical doctrine converts at **0.5–0.8% CTR with a convict-seeking-exoneration protagonist** and at **3–18× channel median with a landowner / driver / mechanic / grandmother protagonist**. Our own fresh analytics agree independently: **police-power/doctrine is our best-CTR archetype at 2.45%; wrongful conviction is our worst at 1.13%.** The wrongful-conviction problem is **entry, not retention.**

**This inverts the natural shape of an international-injustice pool.** The instinctive non-US pick — Hakamada, Kiszko, Malkinson, Folbigg, Pora, Chiang, Marshall, Sugaya, Outreau, Ellis — is *exactly* the losing archetype. Every candidate below therefore carries a **`protagonist_type`** field:

| Value | Meaning | Measured direction |
|---|---|---|
| **ordinary-citizen** | A person who was never accused of anything: a parent, a shopkeeper, a retiree, a bereaved relative, or an outside investigator who took the institution on | **The winning archetype (3–18×)** |
| **accused-then-cleared** | Charged or convicted, later acquitted/quashed/pardoned | Middle, and closer to the losing end |
| **convict-seeking-exoneration** | Still convicted, or the film's spine is a bid for exoneration | **The losing archetype (0.5–0.8%)** |

**Consequence for this file: the systemic/programme candidates beat the miscarriage-of-justice candidates on the one variable that was just measured to matter most** — because programmes harm people who were never accused of anything.

**Also adopted:** **loss-verb titles (took / seized / raided / destroyed / drained) score +0.180 (n=47).** Candidates that support a natural loss-verb headline are marked **[LOSS-VERB]**.

### 0.2 ⚠ "NEEDS A PAYOFF" IS DROPPED AS A FILTER

Measured: **villain-unpunished endings do NOT suppress performance (2.22× at 44 min).** Earlier drafts of this file marked candidates down for ending on an inquiry with nobody charged. **That penalty is withdrawn.** What survives is a *duplication* concern only (§0.3), not a quality one — an unpunished ending is fine; an ending that is the *same shape as the episode before it* is not.

### 0.3 EP56 is not one mechanism spend. It is three.

EP56's script is titled *"The Computer Said They Stole."* Its recommended packaged title is *"A Software Bug Sent 236 Innocent People to Prison."* Its closing line is *"as of the summer of 2026, no one has been convicted of anything for doing it."*

| Machine | Also already spent on | Consequence for this pool |
|---|---|---|
| **A computer accuses innocent people** | **EP36 `williams`** — titled *"THE ALGORITHM SAID IT WAS YOU"*, whose Act-I payoff is a detective answering *"No. A computer did."* | Run **twice** now, at n=1 and at mass scale. A third is a duplicate regardless of country. |
| **An institution mass-punishes innocent people using its own flawed system** | EP56 | Kills Norway's NAV scandal outright (§4.1). Constrains Robodebt severely (§3-CW1). |
| **Inquiry finds institutional guilt, nobody prosecuted** | EP56 — and **nowhere else in 56 episodes** (grep M2) | A *duplication* flag only, per §0.2. Marked **[M2]** below. |

### 0.4 US-context cost is now the most heavily weighted risk column

The lane analysis found **international/immigration-flavoured content underperforms badly on the one channel that tested it.** Every entry carries an honest estimate in seconds of foreign-institution setup before a US 55+ male viewer can follow. **Anything over ~45 seconds is a real penalty; anything over ~120 seconds is close to disqualifying.**

**Related and binding:** a same-story runtime experiment on one channel measured **3 min = 18.65× / 1.04M views against 38 min = 0.95× / 53k.** Long-form does **not** inherit short-form demand. Every candidate below is therefore assessed on **whether the premise holds 20–30 minutes on its own merits** (field: **Holds 20–30?**), not on how loud the story is in the news.

### 0.5 International remains FROZEN until E2 reads out

`TOPIC_PIPELINE.v003.md` §0.6: EP56 **is** experiment E2. Decision rule: **GB views ≥300 with AVP ≥45% → open a UK lane at 1 in 6 episodes; else stay US.** EP56 is unrendered, so E2 has produced zero data. Measured basis (`DEEP_RESEARCH_FINDINGS.v001.md` §6/T6): **US = 86% of geo-known views at 24.2% AVP**; non-US AVPs on n=22–110 views each: **GB 60.0 · AU 67.4 · NL 63.2 · CA 57.5.** Roughly 2.5–2.8× on samples far too small to trust. **This file is pool material for after that read-out.** Note that the US systemic candidates in lane (b) are **not** subject to the freeze.

### 0.6 Verification honesty — and the corrections this pass caught

**The session's WebSearch budget was exhausted (200/200) before verification began** — the same failure `TOPIC_PIPELINE.v003.md` §4 logged on 2026-07-28. All work fell back to direct fetching of primary documents, which *improved* quote quality. Tags:

- **[V-PRIMARY★]** — the primary PDF was downloaded and its text extracted directly; **character-exact.**
- **[V-PRIMARY]** — read verbatim on the primary source's own page (court site, Hansard, Oireachtas record, government PDF).
- **[V-SECONDARY]** — captured via a reputable secondary source. **Not screen-safe.** Re-pull before scripting.
- **[NONE VERIFIED]** — **do not put on screen under any circumstances.**

**⚠ TEN CORRECTIONS CAUGHT AT TOPIC STAGE — logged so they cannot re-enter:**
1. **FBI hair review: 257 of 268 trials (96%), and 35 capital defendants with errors in 33 — NOT 32.** Nine had already been executed; five died on death row.
2. **Palmer Report says "the 200 other cases referred to the Rau Inquiry." The widely-cited 247 could not be verified — do not use it.**
3. **Kiszko served 16 years, not 17** (every Hansard reference: 1993, 2003, 2011).
4. **Teina Pora: sources say 20 years (1994–2014), not 21.** Unresolved — settle before use.
5. **Varadkar's line is *"a stifling, oppressive and deeply misogynistic culture"* — "brutally misogynistic" is wrong.**
6. **Grenfell: the widely-quoted "all the deaths were avoidable" is NOT in Phase 2 Volume 1.** The word "avoidable" does not appear in the extracted text.
7. **Arthur Allan Thomas: the famous "unspeakable outrage" line is NOT VERIFIED word-for-word** — the 1980 Royal Commission report was unreachable. See §3-CW7b.
8. **The UK government apologised for forced adoption on 2 July 2026**, reversing its 2023 refusal. Any brief written before that date is stale.
9. **`courts.go.jp`'s English page for the eugenics Grand Bench judgment renders a corrupted date/case-number field (`2025.09.22`).** The text is unmistakably the 3 July 2024 ruling. **Do not put a date on screen from that page alone.**
10. **Minamata: the May 2024 microphone-cutting incident could NOT be verified** by either research stream. The verified and arguably more damning fact is that **on 22 March 2024 the Kumamoto District Court rejected the claims of all 144 plaintiffs.**

**Saturation remains the weakest field.** YouTube search, Invidious mirrors and every search-engine proxy returned CAPTCHAs or blocks. Only **two candidates have real scraped numbers** (UK2, CW6). Four known competitors were confirmed by other means and are flagged: **Netflix on Dookhan/Farak, Netflix on Grenfell, Netflix on Brothers Home, and a Johnny Depp feature on Minamata.**

---

## 1. NOVELTY GATE — PATTERNS RUN AND RESULTS

**Method.** Case-insensitive `ripgrep` over the repository. Where a pattern was polluted by unrelated vocabulary it was re-run with word boundaries (`\b…\b`) scoped to `episodes/`. Both runs are reported.

### 1.1 Sources searched
1. **All 56 episode directory names** (`ls -d episodes/PD-2026-*/` → 56).
2. **`episodes/*/09_package/youtube_meta*.json`** — 89 files, covered by the `episodes/` sweeps.
3. **`episodes/*/03_script/*.md`** — mechanism greps (§1.3) plus full reads of EP36's first four acts and EP56's Act-IV source appendix.
4. **`episodes/_planning/`** — complete reads of `TOPIC_PIPELINE.v001/.v002/.v003`, `DEEP_RESEARCH_FINDINGS.v001` §6/§8, `EP56_postoffice_PACKAGE_DRAFT.v001`.
5. **Whole-repo runs** across `references/`, `scripts/`, `docs/`, `decisions/`, `assets/`, `remotion/`.
6. **Forward-collision check:** `ls -d episodes/*05[7-9]* episodes/*06[0-9]*` → **zero hits.**

### 1.2 Name greps run

| # | Pattern | Scope | Result |
|---|---|---|---|
| N1 | `(Malkinson\|infected blood\|Langstaff\|Windrush\|Hillsborough\|Colin Stagg\|Rachel Nickell\|Napper\|Kiszko\|Robodebt\|Folbigg\|Alvarez Solon\|Cornelia Rau\|Palmer Inquiry\|Motherisk\|Donald Marshall\|Teina Pora\|Arthur Allan Thomas\|Tuam\|Corless\|Magdalene\|McCabe\|Charleton)` | whole repo | **Only `Kiszko`, and only as a *benched* candidate.** One false positive: `Marshall` in `references/opinions/carpenter_585US296_2018.txt`. Everything else **zero**. |
| N2 | `(Hakamada\|eugenic protection\|Minamata\|Chisso\|Ohkawara\|Ashikaga\|Sugaya\|Brothers Home\|형제복지원\|Chiang Kuo-ching\|Hsichih\|Hwaseong\|overseas adoption\|Korean adopt)` | whole repo | **Only `Hakamada`, benched** (v002 §4; v003 §0.6 freeze). **All East Asian systemic topics: zero.** |
| N3 | `\b(toeslagen\|Outreau\|Burgaud\|Servier\|Frachon\|Geirfinnur\|Bolladottir\|Mollath\|Tortora\|Greenland\|Verdingkinder\|Magdalene\|Gillard\|Esidimeni\|Grenfell\|Moseneke\|Dookhan\|Farak\|Ananias\|Gilchrist\|Fred Zain\|Tribble\|Sally Clark\|Roy Meadow\|Cannings\|Letby\|Windrush\|Hillsborough\|Robodebt\|Folbigg\|Motherisk\|Tuam\|Corless\|Minamata\|Chisso\|Sugaya)\b` | `episodes/` | **Three hits, all planning-file bench/reject entries, none an episode:** `Sally Clark` (v002 §3.6 reject), `Dookhan / Farak` (v001 #17), the v002 bench list. |
| N4 | `\b(infected blood\|haemophili\|Factor VIII\|Bloody Sunday\|ninos robados\|stolen babies\|eugenic\|Brothers Home\|Korean adoptee\|Truth and Reconciliation\|melamine\|thalidomide\|NSU\|Baneheia\|Peter Ellis\|Civic Creche\|Guy Paul Morin\|Sophonow\|Milgaard\|Chamberlain\|Timothy Evans\|Guildford\|Birmingham Six\|Bergwall\|Ronald Watts\|Clarissa Glenn\|Curtis McCarty\|Glen Woodall)\b` | `episodes/` | **Only the known v001/v002 bench entries** — Chamberlain (#25), Timothy Evans (#29), Guildford/Birmingham Six (#32), Milgaard (#34), Bergwall (v002 §5). **Every other name: zero.** |
| N5 | **Money-quote screen** (§6c check 1): `(unjustified and unjustifiable\|institutional ignorance\|Ongekend\|unprecedented injustice\|crude and cruel\|virtually every turn\|not an accident\|egregious government misconduct\|systematic dishonesty\|author of his own misfortune)` | whole repo | **Zero collisions.** Only `not an accident` hits — EP16 Titan's thesis line and one `decisions/` file. **No intended money quote in this pool is already spent on screen.** |
| N6 | **Institutional-actor screen** (§6c check 1): `(Criminal Cases Review\|CCRC\|Fujitsu\|Vennells\|Bates v Post\|private prosecution\|Horizon)` | `episodes/PD-2026-056-postoffice/` | 432 occurrences across 5 files. **Load-bearing finding: the CCRC is already on screen in EP56 — as the body that *"began referring them in batches"*, i.e. the rescuer.** Malkinson's film makes the same body the antagonist. A **named-institution role-reversal** that must be deliberate in packaging (§3-UK3). |

**False positives logged** (in the spirit of v002's "Burge ≈ Burger" and v003's "Wharton"): `Vela` matches inside "cle**VELA**nd" (EP45); `Meadow` matches ~40 landscape stock assets in `assets/asset_manifest*.json`; `Quick` (Bergwall's alias "Thomas Quick") matches *"a quick check for weapons"* in EP06 Terry; `Marshall` matches a citation inside the Carpenter opinion.

### 1.3 Mechanism greps — the part that actually matters

| # | Machine screened | Pattern | Scope | Result |
|---|---|---|---|---|
| **M1** | **A computer/algorithm accuses an innocent person** | `(software\|computer system\|IT system\|accounting system\|algorithm\|automated)` | `episodes/**/03_script/*.md` | **31 occurrences across 9 scripts. TWO are the machine itself:** **EP36 `williams`** (11 hits; *titled* "THE ALGORITHM SAID IT WAS YOU") and **EP56 `postoffice`** (the whole film). Rest incidental (FTX `allow_negative`, flash-crash HFT, Swartz). **VERDICT: spent twice.** |
| **M2** | **Inquiry finds institutional guilt, nobody prosecuted** | `(inquiry\|royal commission\|public inquiry\|tribunal\|truth commission\|commission of inquiry)` | `episodes/**/03_script/*.md` | **11 occurrences, ALL in EP56, none anywhere else in 56 episodes** — and it is EP56's *ending*. Per §0.2 this is now a **duplication** flag only. |
| **M3** | **Systemic removal of children / forced sterilisation** | `(sterilis\|steriliz\|child(ren)? (were\|was)? (removed\|taken) from\|deport\|residential school\|orphanage\|laundr(y\|ies)\|adopted out\|forced adoption)` | `episodes/**/03_script/*.md` | **One hit, a false positive** — EP19 Varsity Blues calls Singer's foundation "a laundry". **The entire child-removal / sterilisation lane is untouched. Completely open — and it is the lane whose protagonists are ordinary citizens.** |
| **M4** | **Crime-lab / forensic-programme fraud** | `\b(Dookhan\|Farak\|Gilchrist\|Fred Zain\|Ananias\|crime lab\|lab analyst\|tainted evidence\|mass exoneration)\b` | `episodes/` | **Only the v001 bench listing (#17).** No shipped episode is a lab-fraud film. **Lane open.** |
| **M5** | **Contaminated supply harms the public; the state defends itself** | via N4 (`infected blood`, `haemophili`, `Factor VIII`, `melamine`, `thalidomide`, `Minamata`, `Chisso`) | `episodes/` | **Zero.** Lane open — **but see §5-F: EP58 Camp Lejeune, already slated, is this machine in a US uniform.** |
| **M6** | **A citizen wrongly detained, deported or listed by state error** | v003 §6b, re-confirmed via N1 | `episodes/` | **Zero.** Only hit is the acronym "CBP" in EP34's graphics spec. **Lane open — no EP56 overlap at all.** |
| **M7** | **Corrupt police unit manufactures convictions** | `\b(gang unit\|tactical (team\|unit)\|protection racket\|planted (drugs\|evidence)\|shakedown\|internal affairs)\b` | `episodes/` | **Zero dedicated episode.** ⚠ **Adjacency: EP55 `burge` is a corrupt Chicago police unit** — see §5-J before promoting SY5 Watts. |

### 1.4 Novelty verdict

**Every candidate in §3 is NEW by name.** Exceptions are **pre-existing bench entries, not collisions**, left where they are:

| Already benched | Where | Status |
|---|---|---|
| **Stefan Kiszko** (UK) | v002 §5, v003 §0.6 | Frozen pending E2. Re-assessed at §3-UK6 — it has weakened. |
| **Iwao Hakamada** (JP) | v002 §2.4, v003 §0.6 | Frozen; v003 flags an R-38 packaging defect. **Also now the losing protagonist archetype.** Not re-proposed. |
| **Lindy Chamberlain** (AU) · **Timothy Evans** (UK) · **Guildford Four / Birmingham Six** (UK) · **David Milgaard** (CA) · **Sture Bergwall** (SE) | v001 #25/#29/#32/#34, v002 §5 | Bench. All resolved-form and all accused-then-cleared or worse. Not re-proposed. |
| **Sally Clark** (UK) | v002 §3.6 | **Structural REJECT.** See §3-CW2: Folbigg is the same machine and is the live one. |
| **Dookhan / Farak** (US) | v001 #17 | Bench. Carried forward at §3-SY2 with a Netflix saturation finding that likely kills it. |

**Three candidates are formally DROPPED for machine-level duplication (§4), and six more are constrained (§5).**

---

## 2. THE POOL — SUMMARY TABLE (43 live candidates)

**Legend.** **Protagonist** = the measured variable (§0.1): **ORD** = ordinary-citizen *(winning archetype)* · **A-t-C** = accused-then-cleared · **CSE** = convict-seeking-exoneration *(losing archetype)* · **⚠none** = no carrier verified, which is a blocking gate.
**PT** = present-tense injustice live in 2026 · **Q** = quote verification (★=primary PDF text-extracted, P=primary page, S=secondary, ✗=none) · **US¢** = seconds of foreign-institution setup · **20–30?** = can the premise hold long-form on its own merits · **Sat** = saturation.

### 2.1 UK — beyond the Post Office (EP56 is TAKEN)

| # | Case | Protagonist | Carrier | Stakes gap | PT | Q | US¢ | 20–30? | Ad-safety | Sat | Risk |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **UK1** | Infected blood / Langstaff | **ORD** | Colin Smith Sr. | 1 dose pooled from up to **30,000** donors → **30 of 122** Treloar's boys alive; **17%** of claimants paid 2 yrs on | ✅ | **P** | 45–60 | ✅ | Med-High | unverif | R1/R2 |
| **UK2** | Forced adoption 1949–76 **[LOSS-VERB]** | **ORD** | Ann Lloyd Keen | **£4m** package ÷ **185,000** = **£21.60 each** | ✅ | **P** | **35–45** | ✅ | Med (yellow) | **measured: open** | R2 |
| **UK3** | Andrew Malkinson / CCRC | **A-t-C** | Andrew Malkinson | **2** withheld photos → **17 yrs**; **1** unrequested file → **14** extra | ✅ | **P** | 40–75 | ✅ | High (rape) | unverif | R2 |
| **UK4** | Hillsborough | **ORD** | Andrew Devine | **164** statements altered; **97 dead → 0 convicted** | ✅ | **P** | 100–120 | ✅ | Med | assume HIGH | R1/R2 |
| **UK5** | Windrush | **ORD** | "Nathaniel" | **11,800** files reviewed → **18** errors admitted | ✅ | **P** | **120–150** | ✅ | **High (capture)** | unverif | R2 |
| **UK6** | Stefan Kiszko | **A-t-C** | Stefan Kiszko | **3 days** questioning → **16 years** | ✗ | **P**(part) | 90–110 | ◐ | **Severe** | unverif | R1 |
| **UK7** | Colin Stagg / Rachel Nickell | **A-t-C** | Colin Stagg | **£831,000** paid, **0** officers disciplined | ✗ | **✗** | 60–75 | ✅ | **Severe** | unverif | R2 |
| **UK8** | Grenfell Tower | **ORD** | ⚠none verified | **£293,368** saved → **72 dead**; **0** charged | ✅ | **★** | 60–80 | ✅ | Very high | **HIGH (Netflix)** | R1/R2 |

### 2.2 Commonwealth (AU / CA / NZ / IE)

| # | Case | Protagonist | Carrier | Stakes gap | PT | Q | US¢ | 20–30? | Ad-safety | Sat | Risk |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **CW1** | Robodebt **[LOSS-VERB]** | **ORD** | Rhys Cauzzo | **12 letters + 5 calls + 6 letters + 2 texts + 13 calls** → dead at 28; **470,000** debts | ◐ | **S** | 90–120 | ✅ | High (suicide) | SBS 2025 | R1/R2 |
| **CW2** | Kathleen Folbigg | **A-t-C** | Kathleen Folbigg | **1** amino-acid substitution → **20 yrs**; A$2m ÷ 20 yrs = **A$274/day** | ◐ | **★** | 45–75 | ✅ | Severe | **HIGH (2.27M)** | R2 |
| **CW3** | Alvarez Solon / Palmer **[LOSS-VERB]** | **ORD** | Vivian Alvarez Solon | quadriplegic citizen deported **8 days** after hospital told them; **200** other cases | ✗ | **P** | **150–240** | ◐ | Moderate | **ZERO** | R2 |
| **CW4** | Australian forced adoptions | **ORD** | ⚠none verified | **~150,000** babies; apology 2013; **no** national redress | ◐ | **✗** | 30–40 | ◐ | Med | unverif | R2 |
| **CW5** | Motherisk **[LOSS-VERB]** | **ORD** | Tammy Whiteman | hairspray (**70% alcohol**) → **35,000+** tests; **56** outcomes affected, **4** children home | ◐ | **P** | 60–90 | ✅ | Med-High | **HIGH (CBC 285k)** | R2 |
| **CW6** | Donald Marshall Jr. | **A-t-C** | Donald Marshall Jr. | 1 knife wound → **11 yrs**; inquiry took **93 days, 16,390 pages** | ✗ | **★** | **30–45** | ✅ | **Lowest** | **measured: 25k** | R1 |
| **CW7a** | Teina Pora | **A-t-C** | Teina Pora | mental age **9–10** → **20 yrs** | ✗ | **P** | 90 | ◐ | High | unverif | R2 |
| **CW7b** | Arthur Allan Thomas | **A-t-C** | Arthur Allan Thomas | **1** planted shellcase → **9 yrs**, 2 trials, NZ$950k | ◐ | **S** | 45 | ✅ | Med | unverif | **⚠ see §3** |
| **CW8** | Ireland Mother & Baby / Tuam **[LOSS-VERB]** | **ORD** | **Catherine Corless** | **2** recorded burials vs **796** death certs; **62** DNA samples vs **~9,000** dead | ✅✅ | **P** | 45–70 | ✅ | High | **HIGH (1.15M)** | R1/R2 |
| **CW9** | Maurice McCabe | **ORD** | Maurice McCabe | 1 whistleblower report → a false CSA allegation; **1.5M** phantom breath tests | ✗ | **★** | **150–240** | ✅ | High | unverif | **R3** |

### 2.3 Japan / Korea / Taiwan

| # | Case | Protagonist | Carrier | Stakes gap | PT | Q | US¢ | 20–30? | Ad-safety | Sat | Risk |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **AS1** | Japan eugenic sterilisation | **ORD** | Saburo Kita *(pseud.)* / Yumi Suzuki | **¥3.2m** and only **1,110** ever certified vs **~25,000** sterilised, girls of **9** | ✅ | **P** | 30–150 ⚠ | ✅ | **Highest** | ~194 views | R1/R2 |
| **AS2** | Korea overseas adoption **[LOSS-VERB]** | **ORD** | **Phillip Clay** | TRC recognised **56 of 367** vs **~200,000** sent, **~112,000 to the US** | ✅ | **P** | **~0** | ✅ | Med | Frontline 2024 | R2 |
| **AS3** | Brothers Home | **ORD** | Han Jong-sun | **2½ yrs** served (embezzlement only) vs **657 dead** | ✅ | **P** | 30–60 | ✅ | **SEVEREST** | **Netflix 2025** | R1 |
| **AS4** | Minamata | **ORD** | Shinobu Sakamoto | **3,000** certified vs **70,000+** claiming; **8%** certification rate | ✅ | **P** | **~15** | ✅ | High | **HIGH (Depp film)** | R1/R2 |
| **AS5** | Ohkawara Kakohki | **ORD** | Shizuo Aishima | **7–8** bail refusals → dead of cancer in a cell; **0** charges proven | ✅✅ | **P** | **180–300** | ✅ | **Lowest** | ~zero | R2 |
| **AS6** | Ashikaga / Sugaya | **A-t-C** | Toshikazu Sugaya | **1** first-generation DNA test → **17½ yrs** | ◐ | **P** | **20–30** | ◐ | Med-High | unverif | R1/R2 |
| **AS7** | Chiang Kuo-ching | **A-t-C** | his father's 1996 warning | **37 hrs** interrogation → **executed at 21**; **5** officers fined, **0** charged | ◐ | **P** | 70–120 | ◐ | **Severe** | ~zero | R1 |

### 2.4 European state failures

| # | Case | Protagonist | Carrier | Stakes gap | PT | Q | US¢ | 20–30? | Ad-safety | Sat | Risk |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **EU1** | Netherlands toeslagenaffaire **[LOSS-VERB]** | **ORD** | ⚠none named | **1 missing signature** → **26,000** families, **2,090 children removed** | ✅ | **★** | **45–60** | ✅ | Med-High | **ZERO** | R2 |
| **EU2** | Norway NAV | **⚠none** | anonymised "A" | a holiday inside the EEA → **80** wrongly convicted, error back to **1994** | ◐ | **P** | 90–120 | ◐ | **Very low** | **ZERO** | R2 |
| **EU3** | Mediator / Servier | **ORD** | **Dr Irène Frachon** | 1 provincial lung doctor → **5,000,000** took it, **1,500–2,100** dead | ◐ | **P** | **~30** | ✅ | **Low** | **ZERO** | R1/R2 |
| **EU4** | Greenland IUD campaign | **ORD** | **Naja Lyberth** | **1** doctor in **1** classroom → **4,500** girls and women, youngest **13** | ✅✅ | **P** | **~45** | ✅ | High | **Low** | R2 |
| **EU5** | Gustl Mollath | **A-t-C** | Gustl Mollath | 1 letter to a bank → **7.5 yrs**; €670,000 = **€89,000/yr of his life** | ✗ | **P** | 60–75 | ✅ | Med | **ZERO (Eng)** | R2 |
| **EU6** | Spain — niños robados | **ORD** | Inés Madrigal | **1 cushion** under a dress → **30,000+**; **1** trial, **0** punishment | ◐ | **★** | ~60 | ✅ | Med | **Mod (1.0M)** | R1/R2 |
| **EU7** | Iceland — Guðmundur & Geirfinnur | **CSE** | Erla Bolladóttir | **239 days** solitary for her, **655** for Tryggvi → **5 cleared, 1 not** | ✅ | **P** | 30–45 | ✅ | Low-Med | **SEVERE (11M)** | R2 |
| **EU8** | Enzo Tortora | **A-t-C** | Enzo Tortora | a misread name (**"Tortona"**) → **10 yrs**, dead within 2 of acquittal | ✗ | **✗** | **90–120** | ✅ | Low-Med | **ZERO (Eng)** | R1 |
| **EU9** | Outreau | **A-t-C** | François Mourmand | 1 woman's fabrications → **17 tried, 13 acquitted, 1 dead in a cell** | ✗ | **P** | ~90 | ✅ | **WORST** | **ZERO (Eng)** | R1/R2 |
| **EU10** | Peter Ellis / Civic Creche | **A-t-C** | Peter Ellis (posth.) | NZ's **first** posthumous appeal, **3 yrs** after he died fighting | ✗ | **✗** | 50–65 | ◐ | **Severe** | unverif | R1 |

### 2.5 Mass-scale / systemic — lane (b). **Note: US¢ = n/a, which under §0.4 is now a major structural advantage.**

| # | Case | Protagonist | Carrier | Stakes gap | PT | Q | US¢ | 20–30? | Ad-safety | Sat | Risk |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **SY1** | FBI microscopic hair review | **A-t-C** | Santae Tribble | **1 dog hair** → **257 of 268** trials in error; **33 of 35** capital cases | ◐ | **P** | n/a | ✅ | Low | unverif | R1/R2 |
| **SY2** | Dookhan / Farak | **A-t-C** | Rolando Penate ⚠ | 1 chemist → **21,587 vacated in a day** + ~8,000 | ✗ | **P** | n/a | ✅ | Moderate | **HIGH (Netflix)** | R1/R2 |
| **SY3** | Sgt. Ronald Watts **[LOSS-VERB]** | **A-t-C** *(ORD-shaped)* | **Clarissa Glenn** | a **$1,000** bribe demand → **212** convictions vacated; Watts served **22 months** | ✅ | **P** | n/a | ✅ | Mod-High | **unverif, likely open** | R1/R2 |
| **SY4** | MA breathalyzer / *Ananias* | **⚠none** | ⚠none verified | **432** hidden worksheets → **~27,000** defendants | ◐ | **P** | n/a | ◐ | Low | unverif | R1/R2 |
| **SY5** | Joyce Gilchrist | **CSE→A-t-C** | Curtis McCarty | **1** altered note → **~3,000** cases, **23** death sentences, **12** executed | ✗ | **P** | n/a | ✅ | High | unverif | R1 |
| **SY6** | Fred Zain | **A-t-C** | Glen Woodall | 1 analyst → **134** WV + **180** TX convictions; **$6.5m** settlements | ◐ | **★** | n/a | ✅ | Low-Mod | **unverif, none found** | **R1 (cleanest)** |
| **SY7** | Life Esidimeni | **ORD** | **Christine Nxumalo** | a cost-saving transfer → **144 dead**, **44** still missing | ✅ | **★** | 90–120 | ✅ | High | unverif | R1/R2 |
| **SY8** | Switzerland — Verdingkinder | **ORD** | ⚠none verified | **100,000+** children placed as farm labour, into the **1970s** | ◐ | **✗** | 60–80 | ◐ | Med-High | unverif | R1/R2 |

---

## 3. PER-CANDIDATE DETAIL

### 3.1 UK — BEYOND THE POST OFFICE

---

#### UK1. The infected blood scandal / Langstaff · **ORD** · ★
**Premise.** The NHS treated haemophiliacs with Factor VIII pooled from tens of thousands of paid donors — much of it bought from American prisons — infected them with HIV and hepatitis C, then hid it for forty years.

**Carrier — ordinary-citizen.** **Colin Smith Sr.**, whose young son was infected with HIV. His own evidence, Inquiry Vol 2: *"I got up one morning and there 'AIDS dead' written across the side of the house in good six foot letters, so I'm painting that out. The following day there was 'AIDS dead' scratched into the front door with a big cross…"* A father painting the word off his own house is the cold open. **He was never accused of anything — the winning archetype.**

**Stakes gap.** One dose carried *"a minimum pool size of around 1,500 donors and maximum of around 30,000 donors."* At **Treloar's School**, *"only around 30 of the 122 pupils with haemophilia who attended the school between 1970 and 1987 survive."* Nationally **~1,250 infected with HIV, including 380 children**, three-quarters dead; **~26,800** hepatitis C; **3,000+** deaths.

**Institution + consequence.** NHS and the Department of Health. **No prosecution, no striking-off, no honour removed.** Kenneth Clarke, then health minister, told Parliament **14 Nov 1983**: *"There is no conclusive evidence that acquired immune deficiency syndrome (AIDS) is transmitted by blood products."*

**QUOTE — [V-PRIMARY].**
> *"Standing back, and viewing the response of the NHS and of government, the answer to the question 'was there a cover up?' is that there has been. Not in the sense of a handful of people plotting in an orchestrated conspiracy to mislead, but in a way that was more subtle, more pervasive and more chilling in its implications. To save face and to save expense, there has been a hiding of much of the truth."*
> — **Sir Brian Langstaff**, Chair, **20 May 2024**, Vol 1 p.193. `https://www.infectedbloodinquiry.org.uk/sites/default/files/Volume_1.pdf`

**Living / legal.** Clarke alive — use only his own documented words, reproduced by the report. Aronstam and Prof Arthur Bloom deceased. Nothing verified sub judice. **R1/R2.**

**Present tense — the strongest quantified live grievance in the pool.** IBCA at **14 July 2026: 19,814 registered, 3,358 paid — ~17%, two years after the final report.** `https://ibca.org.uk/statistics/registration-and-compensation-progress-update-16-july-2026/`

**Holds 20–30?** Yes — four decades, two document trails, a school, a cover-up finding and a live payment failure.

**Ad-safety.** MEDIUM-HIGH. 380 infected children; 92 of 122 Treloar's boys dead; HIV/AIDS; coerced-abortion testimony. Politics historical and cross-party.

**Saturation.** **UNVERIFIED.** No major TV drama surfaced — absence of measurement, not evidence of absence.

**US-context cost — 45–60s, and the third item is a hook not a tax.** Britain bought American plasma from paid donors including prisoners. *"American prison blood killed British schoolboys"* travels without a civics lesson.

**⚠ [M2]** — ends on an inquiry. Per §0.2 that is now a duplication flag only, and the natural differentiator is the **17% payment rate**, which is a number rather than a report.

---

#### UK2. UK forced adoption of unmarried mothers, 1949–1976 · **ORD** · **[LOSS-VERB]** · ★
**⚠ The premise changed 27 days ago: the UK government apologised on 2 July 2026, reversing its 2023 refusal.**

**Premise.** For 27 years the state licensed, funded and looked away while ~185,000 unmarried mothers were coerced into surrendering their newborns — then told them, in writing, for fifty years, that it had nothing to apologise for.

**Carrier — ordinary-citizen.** **Ann Lloyd Keen**, former MP and birth mother, who gave evidence to the 2022 JCHR and the 2026 Education Committee: *"When I went into labour and into the hospital, I was given nothing for pain because I was told, 'You will remember the pain because you've been a bad girl.'… This was an NHS hospital in January 1967… I have never felt more worthless in my life."*
**The opening image is already written by her:** she bought her son a bicycle for a sixth birthday she would never attend — *"When I got back to where my car was parked, I knew I could not take it anywhere, so I just left it there. In my heart I had bought him a bike."*

**Stakes gap.** **£4 million** over three years — the entire package announced with the apology — against **185,000** affected. **≈ £21.60 each.** No compensation scheme exists in England.
*Narration caveat: 185,000 is the JCHR's count of birth re-registrations, "the closest we have been able to establish." Do not narrate it as "185,000 babies were taken."*

**Institution + consequence.** The state, local authorities, and homes run by the **Roman Catholic Church, Church of England and Salvation Army** — all three named in the Government's own 2023 response. **No charges, no resignations, ever.** Catholics apologised 2016; the Church of England apologised **18 June 2026** and opened its redress scheme. **The screen line: the churches will pay money; the state will not.**

**QUOTE — [V-PRIMARY]. The strongest single document in this pool.**
> *"Whilst we do not think it is appropriate for a formal Government apology to be given, since the state did not actively support these practices, we do wish to say we are sorry of behalf of society to all those affected."*
> — **HM Government (DfE)**, response to the JCHR, received 21 Feb 2023, published **3 March 2023**. `https://publications.parliament.uk/pa/jt5803/jtselect/jtrights/1180/report.html` · PDF `https://committees.parliament.uk/publications/34106/documents/187682/default/`
> **The typo is real and in the official PDF: *"sorry of behalf of society."*** The sentence in which the British government refuses to apologise is misspelled. That is a beat of screen time.
> Same document: *"These women did not give up their babies voluntarily and were effectively coerced into agreeing to adoption."* **The same page that concedes coercion refuses the apology.**

**Living / legal.** Keen, Sally Ells, Debbie Iromlou, Judy Baker, Diana Defries alive and on the parliamentary record. Anonymous ACU-numbered submissions stay anonymous. **Sir David Amess**, who delivered the campaign's letter to the PM on 27 May 2021, was murdered that October and never saw the apology. **R2.**

**Present tense.** PM Keir Starmer, Commons, **2 July 2026**: *"The shame is not yours. The shame was never yours. The shame is ours."* Still unresolved: **no compensation** (Ireland legislated redress in 2022); records lost or withheld; the apology covers **England only**; Northern Ireland gets a statutory inquiry, England a "testimonials project"; survivors dying.

**Holds 20–30?** Yes — the coercion, the 2022 inquiry, the written refusal, the four-year gap, the churches moving first, the 2026 reversal, the missing money.

**Ad-safety.** YELLOW/limited unless deliberately handled. Coerced separation, infant deaths, **child sexual abuse** in Keen's own evidence, obstetric violence, **suicide** in the JCHR report, three named denominations, adjacency to US abortion discourse. Mitigations: suicide as on-screen text with a helpline card; witnesses' own parliamentary words, never dramatised; no editorialising on abortion; strongest material after 3:00.

**Saturation — one of only two candidates with real scraped numbers.** Largest 20-min+ English item on the British case: ***"Breaking the Silence: Britain's Adoption Scandal"* (51:01, 102,270 views)** — a 2018 copyright re-upload. Also *England's Stolen Children* (1:06:03, 5,351); BBC News (12:06, 99,289). **Nothing substantial post-2022 and nothing at all on the 2026 apology. The field is effectively open.**
> **Measured conflation risk:** DW's *Irish* mother-and-baby documentary (28:27) pulls **351,989 views — 3.4× the largest British one.** **The title and thumbnail must not lead with "mother and baby homes"** — Ireland owns that phrase in US search. **This directly constrains building UK2 and CW8 close together.**

**US-context cost — LOWEST NON-US CASE IN THE POOL, 35–45s.** The US had its own Baby Scoop Era: maternity homes, "go stay with your aunt", sealed birth certificates, adoptees still fighting state legislatures now. Spend ~10s on *"this is England, not Ireland"*, ~15s on the unique hook (a government refusing **in writing**, then reversing four years later), ~10s on church-run homes and the NHS. **Put the US parallel at the end as a turn: Britain finally said sorry; nobody has said it to you.**

---

#### UK3. Andrew Malkinson / the CCRC · **A-t-C**
**Premise.** Seventeen years for a rape he did not commit — because police hid two photographs, and the body built to catch exactly this error turned him away twice across fourteen years.

**Carrier.** **Andrew Malkinson**, sentenced to life with a **7-year minimum**, served **17** — the extra decade purely because he refused to admit guilt to the parole board.

**Stakes gap.** **2** undisclosed photographs of the victim's hands (broken fingernails; Malkinson unmarked) → **17 years.** Second: **1** police file the CCRC never requested → **14** extra years.

**Institution + consequence.** Greater Manchester Police — **nobody sanctioned.** The **CCRC** — real consequences: Chair **Helen Pitcher resigned January 2025**; Dame Vera Baird interim chair; CEO Karen Kneller also departed.

**QUOTE — [V-PRIMARY].**
> *"Perhaps above all, this case demonstrates a deep-seated, system-wide, cultural reluctance, which starts right at the top in the Court of Appeal, to acknowledge our Criminal Justice System will on occasion make mistakes, that entirely innocent defendants will sometimes be convicted."*
> — **Chris Henley KC**, independent reviewer appointed by the CCRC, **18 July 2024**. `https://cdn.websitebuilder.service.justice.gov.uk/uploads/sites/5/2024/10/henleyreport.pdf` *(PDF read in full; its justified text inserts spurious mid-word spaces, restored with no words altered.)*
> Also **[V-PRIMARY]** — **Alex Chalk KC, Lord Chancellor, 26 Oct 2023**: *"An innocent man spent 17 years in prison for a crime he did not commit, whilst a rapist remained on the loose."* `https://www.gov.uk/government/speeches/andrew-malkinson-inquiry`

**Living / legal.** Quashed 26 July 2023 ([2023] EWCA Crim 954). **Sub judice risk live** — the Henley report is redacted at CPS/GMP request and a forensic scientist was barred from speaking to Henley due to an ongoing investigation. **Never name or characterise the alternative DNA suspect. R2.**

**Present tense.** The **Malkinson Inquiry (HHJ Sarah Munro KC) has not reported.** CCRC under emergency leadership. Cited in the Commons 25 March 2026.

**Holds 20–30?** Yes.

**Ad-safety.** HIGH — the offence is rape. Complainant anonymised as "C"; keep her so.

**Saturation.** BBC Two *The Wrong Man: 17 Years Behind Bars*, a Sunday Times podcast series, BBC Sounds. **YouTube specifically UNVERIFIED.**

**US-context cost — 60–75s, dropping to ~40s** if led with *"the Innocence Project, except it's the government — and it turned him down twice."*

**⚠ Institutional-actor note (grep N6).** The CCRC is **already on screen in EP56** as the rescuer. This film inverts it. A real asset, but it must be deliberate.

**⚠ Open item.** The *"saved living expenses"* deduction was **not** verified as abolished and Malkinson's award could not be confirmed. **The "charged rent for his own wrongful imprisonment" beat is unusable until 2026 policy is established.**

**⚠ PROTAGONIST PENALTY (§0.1).** A cleared ex-prisoner seeking vindication is the archetype measured at **0.5–0.8% CTR**. This is the strongest *evidence* package in the UK set and the weakest *entry* package. **It is why UK3 drops out of my top 8 (§6).**

---

#### UK4. Hillsborough · **ORD**
**Premise.** A commander opened a gate, 97 people were crushed to death, the force rewrote its own officers' statements and blamed the dead — and 37 years later not one officer has been convicted.

**Carrier — ordinary-citizen.** **Andrew Devine.** Crushed aged 22, kept alive by his family for **32 years**, died 2021 — then ruled unlawfully killed, becoming the **97th victim**, 32 years after the 15 minutes that killed him.

**Stakes gap.** Pens rated **2,200** → ~**3,000** inside at 3:00pm. **164** statements altered, **116** amended to remove criticism of South Yorkshire Police. **97 dead → 0 officers convicted.**

**Institution + consequence.** South Yorkshire Police. **David Duckenfield** charged 2017, **acquitted at retrial 2019**. **Sir Norman Bettison** charged 28 June 2017, **charges dropped 21 August 2018**; his knighthood is **not** recorded as revoked — **do not claim it was.**

**QUOTE — [V-PRIMARY].**
> *"The families know that there are others who have found that when in all innocence and with a good conscience they have asked questions of those in authority on behalf of those they love the institution has closed ranks, refused to disclose information, used public money to defend its interests and acted in a way that was both intimidating and oppressive."*
> — **Rt Rev James Jones KBE**, *'The patronising disposition of unaccountable power'*, **HC 511, 1 November 2017**, p.6. `https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/655892/6_3860_HO_Hillsborough_Report_2017_FINAL_WEB_updated.pdf`
> Alternate, p.10: *"One of its core features is an instinctive prioritisation of the reputation of an organisation over the citizen's right to expect people to be held to account for their actions."*

**Living / legal — the tightest verb-lock in the pool.** Duckenfield **acquitted** — never imply guilt. Bettison **never tried** — say only that charges were brought and dropped. The 2016 inquest's "unlawful killing" is a **coroner's determination, not a criminal finding against any named person** — state that on screen. **R1/R2.**

**Present tense.** The **Public Office (Accountability) Bill** ("Hillsborough Law") passed the Commons **July 2026** and is in the Lords; families including Ian Byrne MP are fighting carve-outs. *(Re-verify — bills.parliament.uk returned 403.)*

**Holds 20–30?** Yes.

**Ad-safety.** MEDIUM. Mass civilian death including minors; blood-alcohol testing of dead children; tabloid defamation of the dead.

**Saturation.** **UNVERIFIED — assume HIGH.** BBC, ITV and Channel 4 have all made hour-long films.

**US-context cost — 100–120s.** *"Cops lied, rewrote reports, nobody went to jail"* is familiar. Only the **inquest-vs-trial** distinction is genuinely alien; spend ~20s there.

**⚠ [M2]**, but the payoff is a **law**, not a report.

---

#### UK5. Windrush · **ORD**
**Premise.** Britain invited Caribbean citizens to rebuild it, never gave them papers, then demanded papers — and detained, sacked and deported its own citizens.

**Carrier — ordinary-citizen.** **"Nathaniel"** (surname withheld in the review), refused re-entry on the CUKC passport he had held 45 years — *"Nine years after his holiday, Nathaniel died in Jamaica, unable to afford treatment for prostate cancer."* Alternative: **Paulette Wilson** — *"I don't feel British. I am British."* *(Wilson's 2020 death not verified this pass.)*

**Stakes gap.** The Home Office examined **11,800** detention/removal cases, identified 164 pre-1973 arrivals affected, *"and it estimated it was most likely to have acted wrongfully in **18** of these cases."* Independently: **at least 83** wrongly deported, **850** wrongly detained 2012–17, **at least 23** died before compensation.

**Institution + consequence.** The **Home Office** and the "hostile environment". **Amber Rudd stood down 29 April 2018** — over misleading Parliament about removal targets, **not** the deportations. Theresa May left office unsanctioned.

**QUOTE — [V-PRIMARY].**
> *"While I am unable to make a definitive finding of institutional racism within the department, I have serious concerns that these failings demonstrate an institutional ignorance and thoughtlessness towards the issue of race and the history of the Windrush generation within the department, which are consistent with some elements of the definition of institutional racism."*
> — **Wendy Williams**, *Windrush Lessons Learned Review*, **19 March 2020**, p.7. `https://assets.publishing.service.gov.uk/media/5e74984fd3bf7f4684279faa/6.5577_HO_Windrush_Lessons_Learned_Review_WEB_v2.pdf`

**Living / legal.** Rudd, May, Javid, Williams, Anthony Bryan alive. Nothing sub judice. **R2.**

**Present tense.** Home Office at 30 April 2026: **£128.7m paid across 4,032 claims** — but of **11,196** final decisions, **6,474 were "zero entitlement."** First **Windrush Commissioner** appointed only **17 June 2025**.

**Holds 20–30?** Yes.

**Ad-safety — the real problem, and it is not classification.** Race plus immigration, live and partisan on both sides of the Atlantic. **The comment section becomes a US immigration argument within an hour regardless of what the film says.** The hazard is **audience capture**.

**Saturation.** UNVERIFIED. BBC drama ***Sitting in Limbo*** (85 min, 2020) already dramatised the most cinematic story.

**US-context cost — 120–150s. BORDERLINE FATAL.** Four concepts with no US analogue: colonial subjects were legally British citizens; the 1971 Act gave rights but no document; the Home Office is one ministry with no state-level buffer; the "hostile environment" deputised landlords and doctors. A ~60s bridge exists but **it strands the review's best material on the far side of the wall.**

---

#### UK6. Stefan Kiszko · **A-t-C** · *(already benched)*
**⚠ Correction: 16 years, not 17.**

**Premise.** A 23-year-old tax clerk with the mental age of a child confessed to murdering an 11-year-old girl — while forensic evidence proving he could not have done it sat in a police file for sixteen years.

**Carrier.** **Lesley Molseed**, 11, verified from Hansard (Philip Davies MP): she was *"on the way to the shop to buy bread for her mother."* **⚠ The Kiszko sterility / no-sperm detail, the spine of the whole story, could NOT be verified from any primary source.**

**Stakes gap.** **3 days** of questioning (Elfyn Llwyd MP, Hansard 2 Nov 2011) → **16 years.** Sharper: the Lancashire investigation into West Yorkshire Police *"started on 10 May 1991. A report was submitted to the Crown Prosecution Service on 3 June 1993"* — Kiszko was already out, and dead within months.

**Institution + consequence.** **West Yorkshire Police.** Ex-Det Supt **Richard Holland** and forensic scientist **Ronald Outteridge** were **charged with perverting the course of justice**; charges **dropped by Rochdale's stipendiary magistrate**; no appeal. **Nobody was ever convicted.**

**QUOTE.** The famous 1992 Court of Appeal line is **[NONE VERIFIED]** — the judgment predates BAILII/National Archives coverage and is absent from Find Case Law. **Do not use any secondary version.** What *is* **[V-PRIMARY]**:
> *"The Crown Prosecution Service is carefully considering and taking counsel's advice on the possibility of an appeal."*
> — **The Solicitor-General**, written answer to Chris Mullin MP, **22 May 1995**. `https://api.parliament.uk/historic-hansard/written-answers/1995/may/22/stefan-kiszko-case`
> Thirteen words of nothing, then silence forever. Pair on screen with the charge it refers to.
> Also **[V-PRIMARY]** — **PM John Major, 2 Feb 1993**: *"The Home Secretary has agreed that compensation should be paid to Mr. Kiszko."*

**Living / legal.** **Ronald Castree convicted of Molseed's murder 12 November 2007.** Kiszko and his mother Charlotte deceased. **R1.**

**Present tense — WEAK.** Cleared 1992, dead 1993, real killer convicted 2007, accountability closed 1995.

**Holds 20–30?** Marginal alone.

**Ad-safety — SEVERE.** An 11-year-old victim; a sexual element that cannot be excised. **⚠ Landmine: Sir Cyril Smith**, then MP for Rochdale, campaigned for Kiszko and is the source of the most-quoted line — Smith was posthumously exposed as a prolific child abuser. **Do not cite Smith, use his footage, or use that quote.**

**US-context cost — 90–110s, close to fatal standalone.** No CCRC existed, so the only exit was a personal referral by a *politician* (~30s); **committal before a stipendiary magistrate**, which is how the case against Holland and Outteridge died without a jury (~35s); pre-PACE interrogation (~25s).

**➡ Recommendation: do not build standalone. Build it as UK3's opening 90 seconds** — *they built the machine because of Stefan Kiszko, and the machine still didn't work.*

---

#### UK7. Colin Stagg / Rachel Nickell · **A-t-C**
**Premise.** The Met could not break their suspect, so they invented a woman — a five-month fake romance engineered to extract a confession — and while they ran it, the real killer murdered a mother and her four-year-old daughter.

**Carrier.** **Colin Stagg.** Fourteen months on remand, acquitted 1994, then fourteen more years publicly suspected — until DNA convicted another man and on **13 August 2008** the state paid him **£706,000**, followed by a Met apology that December. **Second-act carrier:** the undercover officer "Lizzie James", who retired early in 1998 and received **£125,000** from the Met in 2001 for **psychiatric injury sustained running the operation.**

**Stakes gap.** A ~5-month fake relationship → while Stagg was the focus, **Robert Napper murdered Samantha Bisset and her 4-year-old daughter Jazmine.** Sharper: in **October 1989 Napper's own mother telephoned police** to report he had admitted a rape — **police rejected the information.** And: **£831,000 paid out, 0 officers disciplined** — the IPCC found they had all retired, one had died.

**Institution + consequence.** Metropolitan Police, Operation Edzell / SO10. **No officer ever disciplined.** Psychologist **Paul Britton** faced BPS proceedings **dismissed in 2002 for delay, with no substantial hearing** — never found guilty of anything; say so plainly.

**QUOTE — [NONE VERIFIED]. ❌** Mr Justice Ognall's 1994 ruling could not be obtained word-for-word. The circulating *"excessive zeal… deceptive conduct of the grossest kind"* fragments trace on Wikipedia to an **ITV documentary, not a law report.** **Do not put it on screen.** Clearing it requires the *R v Stagg* transcript (CCC, 14 Sept 1994) or Hansard.

**Living / legal — HANDLE WITH CARE.** Stagg is **alive, innocent, acquitted, compensated and formally apologised to.** Never juxtapose him with the crime scene; **he has litigated before.** **⚠ Napper pleaded guilty to Nickell's killing as manslaughter by diminished responsibility, not murder** — "convicted of murdering Rachel Nickell" is factually wrong. "Lizzie James" is a protected pseudonym. **R2.**

**Present tense — weak.** Settled 2008. The bridge: no officer was disciplined **because they had all retired** — precisely the loophole the Hillsborough Law targets. **This film's ending is the other film's law.**

**Holds 20–30?** Yes.

**Ad-safety — WORST IN THE POOL alongside EU9.** Nickell was stabbed 49 times **in front of her two-year-old son**, found clinging to her body. **Child sexual assault and child murder** (Jazmine, 4). The honeytrap consisted of police-scripted violent sexual fantasy correspondence. **Demonetisation-likely even with careful handling.**

**Saturation.** UNVERIFIED. ITV *Real Crime* (2001); Channel 4 drama ***Deceit*** (2021).

**US-context cost — 60–75s.** Fourteen months' remand without bail lands as outrage. Spend the real time on **why a judge killed the sting** — the US instinct is *"so what, we do that"* (Mr Big, jailhouse plants), and naming that instinct is the beat.

---

#### UK8. Grenfell Tower · **ORD** · carrier gate
**Premise.** A concrete tower that could not burn was wrapped in a product its makers knew would, and 72 people died.

**Carrier — ⚠ NOT SETTLED.** Two candidates surfaced, neither confirmed for 2026: **Behailu Kebede**, in whose flat the fire began, who woke his neighbours, called 999, and has lived under public suspicion since despite the Inquiry finding no fault; and **Marcio Gomes**, whose son **Logan** was stillborn hours after the family escaped and is counted among the 72. **Verify before promoting.**

**Stakes gap.** **£293,368** saved by choosing combustible cladding → **72 dead.** Second: the Met is investigating **up to 57 individuals and 20 organisations** with **zero charges** nine years on.

**Institution + consequence.** **Arconic**, **Celotex/Saint-Gobain**, **Kingspan**, **Rydon**, **Harley Facades**, the **BRE**, the **RBKC** and its TMO. **None criminal to date.** Demolition began September 2025.

**QUOTE — [V-PRIMARY★] (PDF text-extracted).**
> *"One very significant reason why Grenfell Tower came to be clad in combustible materials was systematic dishonesty on the part of those who made and sold the rainscreen cladding panels and insulation products. They engaged in deliberate and sustained strategies to manipulate the testing processes, misrepresent test data and mislead the market."*
> — Grenfell Tower Inquiry Phase 2 Report, **¶2.19**, Sir Martin Moore-Bick, **4 September 2024**. `https://assets.publishing.service.gov.uk/media/66d817aa701781e1b341dbd3/CCS0923434692-004_GTI_Phase_2_Volume_1_BOOKMARKED.pdf`
> Better *opening* line, **¶1.3**: *"How was it possible in 21st century London for a reinforced concrete building, itself structurally impervious to fire, to be turned into a death trap that would enable fire to sweep through it in an uncontrollable way in a matter of a few hours despite what were thought to be effective regulations designed to prevent just such an event?"*
> **¶2.4**: *"We conclude that the fire at Grenfell Tower was the culmination of decades of failure by central government and other bodies in positions of responsibility in the construction industry…"*
> On Celotex: it *"embarked on a dishonest scheme to mislead its customers and the wider market"*, testing a system containing **hidden fire-resistant magnesium oxide boards** and obtaining a report omitting them. On Kingspan: it *"cynically exploited the industry's lack of detailed knowledge"* and relied on tests of modified product **until October 2020** — three years after the fire.
> **⚠ CORRECTION: the widely-quoted "all the deaths were avoidable" is NOT in Phase 2 Volume 1.** The word "avoidable" does not appear in the extracted text. **Do not attribute it.**

**Living / legal — the highest exposure in the pool.** Operation Northleigh is ongoing; as of **May 2026 the Met has said no charging decisions until end-2026**, trials not before 2027. **Everyone named is legally innocent; the Inquiry's findings are not criminal findings and you must say so on screen. R1/R2 only if locked entirely to the Inquiry.**

**Present tense.** Nine years, 72 dead, not one charge. *That is* the film's present tense.

**Holds 20–30?** Yes.

**Ad-safety.** **VERY HIGH.** Mass death by fire, children, a stillborn baby, race and class. Assume limited or no monetisation.

**Saturation — HIGH and confirmed.** Netflix's ***Grenfell: Uncovered*** (June 2025) won the Sheffield DocFest audience award. BBC and Channel 4 also. **Crowded.**

**US-context cost — 60–75s.** Council tower block, TMO, inquiry-vs-trial, and **"stay put"** advice — the last is counter-intuitive to a US audience and is where the deaths happened; budget 20s for it alone. A tower in London's richest borough needs no explanation and is a gift.

---

### 3.2 COMMONWEALTH (AU / CA / NZ / IE)

---

#### CW1. Robodebt (Australia) · **ORD** · **[LOSS-VERB]** · ⚠ SEVERE MECHANISM WARNING
**Premise.** An algorithm averaged a year's tax data across 26 fortnights, invented debts that never existed, and the Commonwealth pursued 470,000 of them against its poorest citizens for four and a half years.

**Carrier — ordinary-citizen.** **Rhys Cauzzo**, 28, Melbourne. Verified: *"Cauzzo had received 12 letters and five phone calls from Centrelink between May and October 2016, then six letters, two text messages and 13 phone calls from Dun and Bradstreet, a private debt collection agency, between October 2016 and January 2017. It was claimed he had a debt of almost $18,000."* He died on Australia Day 2017.

**Stakes gap.** One averaged fortnightly figure → **470,000** wrongly-raised debts; **A$751m** repaid; **A$1.872bn** total settlement approved June 2021; debt notices went to **663** vulnerable people who died soon after.

**Institution + consequence.** DHS/Services Australia under Secretary **Kathryn Campbell**; ministers Morrison, Porter, Tudge, Robert. Campbell suspended, resigned from Defence July 2023 — no charge. **NACC Operation Myrtleford (March 2026) found former Deputy Secretary Serena Wilson and former General Manager Mark Withnell engaged in serious corrupt conduct, and cleared Scott Morrison and Kathryn Campbell.** *(NACC outcomes sourced from Wikipedia only — re-verify against the NACC's own release.)*

**QUOTE — [V-SECONDARY].**
> *"Robodebt was a crude and cruel mechanism, neither fair nor legal, and it made many people feel like criminals."*
> — Commissioner **Catherine Holmes AC SC**, Royal Commission into the Robodebt Scheme, **7 July 2023**. Read verbatim at `https://lsj.com.au/articles/crude-cruel-and-unlawful-robodebt-royal-commission-findings/` *(Law Society Journal NSW — secondary. The royal commission's own domain timed out on every attempt; **re-pull from the primary PDF before burn-in**.)*
> Same source: *"In essence, people were traumatised on the off chance they might owe money."*

**Living / legal.** All principals alive. **Morrison and Campbell were CLEARED by the NACC and any framing must say so. R1/R2.**

**Present tense.** No criminal prosecution of anyone. The March 2026 corrupt-conduct findings are the freshest consequence in this pool.

**Holds 20–30?** Yes.

**Ad-safety.** HIGH — suicide is the emotional engine. On-screen text plus a helpline card, never narration.

**Saturation.** **SBS "The People vs Robodebt", 3-episode docu-drama, 24 September 2025.** YouTube long-form unverified.

**US-context cost — 90–120s.** Centrelink is cheap (~15s: "Social Security, unemployment and food stamps in one agency"); Royal Commission ~20s. **Income averaging is the expensive one (~40s) and it is load-bearing** — an accounting concept, not an image.

**⚠⚠ MECHANISM — THE MOST SERIOUS IN THIS FILE, and an independent researcher reached the same verdict unprompted.** *"It is the same machine. Not diplomatically — structurally. A computer generates a number, the institution treats the number as truth, innocent people are told to prove a negative, the institution disbelieves them for years while insiders warn it is wrong, people die, an official inquiry vindicates the victims, and almost no one is punished."*
The differences mostly make it **harder**, not fresher: Horizon's computer was genuinely broken and produced **criminal prosecutions, 236 imprisonments**; Robodebt's computer worked exactly as designed, the *policy* was unlawful, and **nobody went to prison.** *"The computer wasn't broken, the policy was"* is a harder sell, and the prison stakes are gone.
**Verdict: shelve for ≥12 months / ≥6 episodes from EP56. If ever built, sell it explicitly as the anti-Horizon — "this one wasn't a glitch" — with the March 2026 corrupt-conduct findings as the spine.**

---

#### CW2. Kathleen Folbigg (Australia) · **A-t-C**
**Premise.** Australia's "worst female serial killer" served 20 years for smothering her four babies; one letter of her DNA proved the state had convicted a grieving mother of a genetic disease.

**Carrier.** **Kathleen Folbigg.** The diary line the jury read, 9 Nov 1997, of her third dead child: *"With Sarah all I wanted was her to shut up. And one day she did."* Twenty-six years later the inquiry found that sentence neutral — self-blame, not confession. The science that cleared her came off newborn heel-prick blood cards left in a drawer.

**Stakes gap.** One amino-acid substitution (**CALM2 G114R**) → a 40-year sentence, **20 years served**, and an **A$2m** ex gratia offer in Aug 2025 ≈ **A$274 a day**.

**Institution + consequence.** The NSW Crown. **Essentially none.** Bathurst quoted the prosecutor's closing (*"It is probably more common that a person has been hit by lightning four times than what has happened to this family"*), tied it to Roy Meadow's discredited law, then said ruling on its propriety was "no part of my role."

**QUOTE — [V-PRIMARY★].**
> *"Thus, while the verdicts at trial were reasonably open on the evidence then available, there is now reasonable doubt as to Ms Folbigg's guilt."*
> — Bell CJ, Ward P, Harrison CJ at CL, NSW Court of Criminal Appeal, *Folbigg v R* [2023] NSWCCA 325, **14 Dec 2023**. `https://www.caselaw.nsw.gov.au/decision/18c618d8c0030799c1d962d7`
> Stronger, verified in the 619-page inquiry PDF: *"This portion of the address by the Prosecutor echoes a now discredited theory by the British paediatrician, Sir Roy Meadow…"* — **Hon. Thomas Bathurst AC KC, ¶137, 8 Nov 2023.** And on the ex-husband's claim she carried a gene for murdering children: *"The submission was rank speculation and should not have been made."* (¶1972)

**Living / legal.** Folbigg alive and acquitted. **Craig Folbigg is alive and argued she was still guilty** — real defamation exposure; frame him as a father who lost four children, not a villain. **R2.**

**Present tense.** Live: she called the A$2m *"lowball,"* *"insulting,"* a *"slap in the face"* (ABC, 11 Aug 2025). **Australia has no statutory wrongful-conviction compensation scheme** — pure ministerial discretion.

**Holds 20–30?** Yes.

**Ad-safety.** SEVERE — four dead infants, alleged smothering, maternal mental illness.

**Saturation — HEAVY and measured.** ABC News In-depth / Australian Story, 35:19, **2,270,125 views**; 60 Minutes Australia, 47:23, **931,691**.

**US-context cost — LOW, 45–75s, not fatal.** Jury, appeal, pardon, DNA all map free. Only the judicial inquiry under the Crimes (Appeal and Review) Act is foreign (~25s).

**⚠ Mechanism — internal collision.** Folbigg and **Sally Clark** are **the same machine**. v002 §3.6 already **rejected Sally Clark structurally**. **Only one may ever be built, and Folbigg is the live one.**

---

#### CW3. Vivian Alvarez Solon / Cornelia Rau / the Palmer Inquiry (Australia) · **ORD** · **[LOSS-VERB]**
**Premise.** Australia's immigration department locked up its own citizens by mistake, deported a disabled Australian woman, and when police told them who she was, closed the file and wrote off her removal debt.

**Carrier — ordinary-citizen.** **Vivian Alvarez Solon.** From the Palmer Report: on 12 July 2001 St Vincent's told the department she had *"C4-5 incomplete quadriplegia"* and *"she walks with a 4 wheel walker for safety."* **Eight days later** she was flown to Manila on Qantas **QF019**. Then: *"On 24 August 2001 Vivian Alvarez's debt to the Commonwealth for the cost of removal was written off by a DIMIA officer."* Queensland Police faxed DIMIA naming *"Vivian SOLON @ Young"* on 19 July; DIMIA confirmed her name and DOB the same day; she was deported the next morning. She was gone four years.

**Stakes gap.** One database search never run (a wildcard on "Vivian"/1962 returned 201 matches with her records in the first 70; her citizenship file was accessed twice on 23 July — **three days after deportation**) → **200+ wrongful detentions over six years.**

**⚠ CORRECTION.** Palmer's verified wording is **"the 200 other cases referred to the Rau Inquiry"** (§8.4.4). **The 247 figure could not be verified. Do not put it on screen.**

**Institution + consequence.** DIMIA under Minister Amanda Vanstone and Secretary **Bill Farmer**. **Farmer was made an Officer of the Order of Australia in June 2005 — weeks before the report was tabled — and appointed Ambassador to Indonesia**, his term later extended by the incoming Labor government. No officer prosecuted.

**QUOTE — [V-PRIMARY★].**
> *"She was not a prisoner, had done nothing wrong, and was put there simply for administrative convenience."*
> — **Mick Palmer AO APM**, former AFP Commissioner, Main Finding 12, **July 2005**. `https://www.homeaffairs.gov.au/reports-and-pubs/files/palmer-report.pdf`
> Main Finding 8: *"There is a serious cultural problem within DIMIA's immigration compliance and detention areas… a culture largely unwilling to challenge organisational norms or to engage in genuine self-criticism or analysis."*

**Living / legal.** All alive. Low defamation risk — Palmer named no individual officers; neither should we. **Rau's schizophrenia is the real ethical hazard.** Compensation figures (Solon A$4.5m 2006, Rau A$2.6m 2008) are **Wikipedia-only, unverified.** **R2.**

**Present tense — weak.** Mandatory detention under s189(1) is unchanged; Palmer's Finding 4 was never legislated. No live news peg.

**Holds 20–30?** Marginal — the strongest material is two cases and one report.

**Ad-safety.** Moderate, but **politically flammable**: for a US audience this maps instantly onto ICE detaining US citizens. That is both why it could go big and why it could split the audience.

**Saturation — ZERO.** A 20+ minute filtered search returned **no results**. Largest overall: 60 Minutes Australia, 14:56, **119,866 views** — under 20 minutes. **Genuine white space.**

**US-context cost — 150–240s honestly, cut to ~90–120s only with the ICE analogy** to collapse "mandatory detention on an officer's suspicion, no charge, no judge, no time limit" into one comparison. **Without that framing device the episode dies in act one — and with it, §0.4's international/immigration underperformance warning applies at full force.**

---

#### CW4. Australian forced adoptions · **ORD** · carrier gate
**Premise.** Roughly 150,000 babies were taken from unmarried mothers in Australian hospitals between the 1950s and 1970s, and in 2013 the Prime Minister apologised on the floor of Parliament.

**Carrier — ⚠ NOT NAMED THIS PASS. Blocking gate.**

**Stakes gap.** **~150,000** babies; national apology 21 March 2013; **no national redress scheme** (unlike Ireland's 2022 legislation).

**Institution + consequence.** Hospitals, churches and state agencies. A Senate inquiry (2012) and an apology; no charges.

**QUOTE — [NONE VERIFIED].** Julia Gillard's apology text was not obtained. **Must be established before use.**

**Living / legal.** Many mothers living and organised. **R2.**

**Present tense.** Partial — the absence of redress is the live grievance.

**Holds 20–30?** Marginal without a carrier.

**Ad-safety.** MEDIUM. **Saturation.** UNVERIFIED. **US-context cost — 30–40s** (Baby Scoop Era parallel).

**⚠ Mechanism — internal collision with UK2: the same machine.** **Only one may be built. UK2 is stronger on every measured axis** — a verified primary quote, a 27-day-old news peg, and real scraped saturation showing an open field. **Hold CW4 as UK2's fallback, not as a separate candidate.**

---

#### CW5. Motherisk (Ontario, Canada) · **ORD** · **[LOSS-VERB]**
**Premise.** A children's hospital sold 35,000+ hair tests as scientific proof of parental drug and alcohol abuse; the science was junk, and child-welfare agencies took children on it.

**Carrier — ordinary-citizen, and the single best carrier detail in this pool.** **Tammy Whiteman**, Muskoka. Four tests read her at **16–18 drinks a day.** She wore a court-ordered alcohol ankle monitor for **90 days — the monitor read zero, and the hair test covering those same 90 days still called her a chronic abuser.** The source was her hairspray: **70% alcohol.** Her daughters were already gone.

**Stakes gap.** 1 strand of hair → **35,000+ tests** across **5 provinces**; **16,000** Ontario cases flagged; **1,300** reviewed; testing significantly affected **56** outcomes; **7** families got any remedy; **4** got children home.

**Institution + consequence.** **SickKids Toronto** and lab director **Dr. Gideon Koren**, who won a national research prize for Motherisk in 2011. Lab closed 2015; CPSO investigation from 2017; **Koren surrendered his Ontario licence in 2019 before any hearing**; programme shut April 2019. No charges.

**QUOTE — [V-PRIMARY].**
> *"It was not going to be a nuanced report, it was going to say these results are inadequate and unreliable and no forensic lab in the world conducted tests and interpreted these tests in that manner, nowhere, there was nothing redeeming to be said."*
> — **Justice Susan Lang**, retired Ontario Court of Appeal justice, head of the independent review, first interview, CBC News, **19 Oct 2017**. `https://www.cbc.ca/news/canada/motherisk-hair-testing-families-1.4360577`
> — **Judge Judith Beaman**, Motherisk Commissioner, **26 Feb 2018**: *"The testing was imposed on parents and other caregivers who were among the poorest and most vulnerable members of our society. There was scant regard for due process or their rights to privacy and bodily integrity."* `https://globalnews.ca/news/4047971/motherrisk-hair-testing-ontario-report/`
> **⚠ Do NOT use** the widely-circulated Lang-report sentence about "internationally recognized forensic standards" — the Ontario AG URL is dead and the primary PDF is unreachable. **Unverified.**

**Living / legal — highest exposure in the Commonwealth set.** Koren and lab manager Joey Gareri alive and named; SickKids is a live institution. Everything must be attributed to the review or commission. **R2.**

**Present tense.** Adoptions are irreversible; **52 of the 56 affected families got nothing**; Beaman flagged that **urine testing is still used the same way**; provinces outside Ontario never got a commission.

**Holds 20–30?** Yes.

**Ad-safety.** Moderate-high — child removal, addiction, foster care.

**Saturation — the definitive version exists.** CBC *the fifth estate*, "Motherisk: Tainted Tests & Broken Families," 38:44, **284,814 views** — with the families on camera and Lang's only interview.

**US-context cost — 60–90s, arguably fatal.** Children's Aid Societies have no clean US name, child protection is provincial (so the scandal stops at borders), and the payoff is administrative — **no arrest, no trial, no perp walk.** The one US-legible door: **Colorado courts rejected this same lab's results as "not competent evidence" in 1993, twenty-two years before Canada stopped.**

---

#### CW6. Donald Marshall Jr. (Nova Scotia) · **A-t-C**
**Premise.** A 17-year-old Mi'kmaw boy was convicted of a murder he watched happen, served 11 years, and the court that finally freed him blamed him for his own imprisonment.

**Carrier.** **Donald Marshall Jr.**, Wentworth Park, near midnight, 28 May 1971. The killer Roy Ebsary, a drunk 59-year-old former ship's cook, said **"This is for you, Black man"** and stabbed Sandy Seale. Marshall, slashed and running for help, became the accused. Second detail: after 11 years of protesting innocence, RCMP investigators told him he had better tell them a story they could believe or they would leave and never return — so he confirmed the killer's version, which was then used against him at his own exoneration hearing.

**Stakes gap.** One knife wound → **11 years**; **C$270,000** compensation, raised to a **C$1.5m lifetime pension** in 1990. The inquiry took **93 days, 113 witnesses, 16,390 pages** to establish what four officers could have established in one night.

**Institution + consequence.** **Sergeant of Detectives John MacIntyre, Sydney City Police**, who decided within hours, took an unstable 16-year-old to the scene and fed him the version he wanted, then pressured a frightened 14-year-old on probation to corroborate. **He was later promoted to Chief of Police and never charged.** The Commission expressly declined to recommend charges against anyone. The Court of Appeal judges who called Marshall "the author of his own misfortune" **declined to testify.**

**QUOTE — [V-PRIMARY★] (PDF downloaded and read in full).**
> *"The criminal justice system failed Donald Marshall, Jr. at virtually every turn from his arrest and wrongful conviction for murder in 1971 up to, and even beyond, his acquittal by the Court of Appeal in 1983."*
> — Royal Commission on the Donald Marshall, Jr., Prosecution, *Digest of Findings and Recommendations*, p.1, **December 1989**; Chairman Chief Justice **T. Alexander Hickman**. `https://novascotia.ca/just/marshall_inquiry/_docs/Royal%20Commission%20on%20the%20Donald%20Marshall%20Jr%20Prosecution_findings.pdf`
> Next sentence, same page: *"That they did not is due, in part at least, to the fact that Donald Marshall, Jr. is a Native."*
> **Two production notes:** the report states the finding **twice with different wording** (p.1 vs p.18) — **use p.1, do not blend.** And the PDF is an **OCR scan with artifacts** — eyeball the page image before any on-screen card.

**Living / legal.** **Marshall died 6 Aug 2009**; Ebsary, MacIntyre and MacNeil all dead. **Near-zero defamation risk, and the report carries an explicit reproduction licence. R1.** One honesty item: **Marshall was charged in 2008 with assaulting his wife** — decide in advance how to handle it rather than being caught.

**Present tense — none.** *R. v. Marshall* (1999) upheld Mi'kmaq treaty fishing rights; the "moderate livelihood" fishery is still unimplemented and produced the 2020 Nova Scotia lobster confrontations. Canada took 35 years to create the review body the Commission demanded.

**Holds 20–30?** Yes.

**Ad-safety — LOWEST in the Commonwealth set.** Knife murder plus racial findings, all quotable because a Royal Commission said it.

**Saturation — measured and near zero.** Largest: "Systemic Racism in Canada | the Donald Marshall Jr. Story," Real Crime, 46:08, **25,186 views**. Nothing above 26k. No US channel in the space.

**US-context cost — 30–45s, not fatal.** Coerced teenage witnesses, a detective who decided first, a prosecutor who buried statements, 11 years — the Central Park Five template, no translation needed; Brady is a four-second name-check; Royal Commission ~15s. **Cut the treaty arc from the spine** — a 20-second closing beat is a hook; in act two it adds 60–90s and kills the episode.

---

#### CW7a. Teina Pora (New Zealand) · **A-t-C**
**Premise.** A 17-year-old with foetal-alcohol brain damage confessed to a rape and murder committed by a serial rapist, and served two decades for it.

**Carrier.** **Teina Pora**, arrested at 17, mental age assessed at **9–10** at the time of the crime. *(FASD/mental-age detail from Wikipedia — verify against the Privy Council judgment.)*

**Stakes gap.** One confession by a boy with the mind of a nine-year-old → **20 years served (1994–2014)**; compensation **NZ$2.52m** (June 2016), raised to **NZ$3,509,048** (Nov 2017) after the government was forced to adjust for inflation.
**⚠ CORRECTION: sources say 20 years, not 21. Resolve before use.**

**Institution + consequence.** NZ Police, who took and relied on the confessions while the actual offender **Malcolm Rewa** was at large; Rewa was convicted of Burdett's rape in 1999 and of her **murder in 2019**. No officer sanctioned *(unverified)*.

**QUOTE — [V-PRIMARY].**
> *"The combination of Pora's frequently contradictory and often implausible confessions and the recent diagnosis of his FASD leads to only one possible conclusion and that is that reliance on his confessions gives rise to a risk of a miscarriage of justice. On that account, his convictions must be quashed."*
> — **Lord Kerr**, delivering the judgment of the Judicial Committee of the Privy Council, *Pora v The Queen* [2015] UKPC 9, **¶58, 3 March 2015**. `https://caselaw.nationalarchives.gov.uk/ukpc/2015/9`

**Living / legal.** Pora alive and compensated; Rewa alive in preventive detention; Susan Burdett's family living. Low risk if you stay on the judgment. **R2.**

**Present tense — weak.** Rewa's 2019 murder conviction closed the loop; compensation settled 2017. **This is a historical film.**

**Holds 20–30?** Marginal.

**Ad-safety.** HIGH — rape and murder of a named victim.

**Saturation.** *The Confessions of Prisoner T* (Michael Bennett, 2013). **View counts unverified.**

**US-context cost — ~90s.** FASD ~20s. **The Privy Council is the expensive item (~40–60s)** — but *"his last appeal was heard in London, by judges of a court New Zealand had already abolished"* is a hook, not just overhead.

**⚠ Engine note.** `TOPIC_PIPELINE.v003.md` §5.4 caps the confession engine: EP53 Norfolk and EP57 Hemme are *"the maximum concentration this engine gets."* Pora is single-subject so not barred, but competing for a capped slot.

---

#### CW7b. Arthur Allan Thomas (New Zealand) · **A-t-C** · ⚠ **MY RESEARCH CONTRADICTS THE COORDINATOR'S READ ON TWO POINTS**
**Premise.** Police could not prove their suspect shot a farming couple, so they manufactured the cartridge case that convicted him twice.

**Carrier.** **Arthur Allan Thomas**, an ordinary Waikato farmer, and **exhibit 350** — the .22 shellcase.

**Stakes gap.** One planted shellcase → **9 years** served (released 18 Dec 1979), **NZ$950,000** compensation, **2** trials. The Crewe murders remain **officially unsolved at 56 years**.

**Institution + consequence.** **Det Insp Bruce Hutton** and **Det Sgt Len Johnston**. **Johnston died in 1978, before the Commission reported. Hutton was never charged and denied it until his death in 2013.** — **this part of the coordinator's read is correct and is a genuine asset: both named villains are dead, so defamation exposure on the villains is near zero.**

**QUOTE — ⚠ [NONE VERIFIED] on the line the coordinator cited.**
> **The famous "unspeakable outrage" is NOT verified word-for-word.** The 1980 Royal Commission report was unreachable this session. **Do not put it on screen.**
> What *is* verified, and it is weaker: *"We consider that this explains why Mr. Hutton described shellcase 350 as containing blue-black corrosion when in fact it did not"* — Royal Commission, 1980, **[V-SECONDARY]** via Wikipedia's quotation of the report.
> **Getting the primary report is the single highest-value action on this candidate.** If "unspeakable outrage" verifies, this candidate rises sharply.

**Living / legal — ⚠ THE DISQUALIFYING HAZARD THE COORDINATOR'S SUMMARY DOES NOT COVER.** The villains being dead is true. **But the protagonist is alive: Arthur Allan Thomas (b. 2 Jan 1938) faced sexual assault charges 2019–2022, discontinued on mental-health grounds.** **Any exoneration-hero framing will be destroyed in the comments within an hour of publication.** This is not a reason never to build it; it is a reason it cannot be built as written. **R2 at best, and only with that fact handled on screen rather than omitted.**

**Present tense.** Partial — the murders are unsolved and no officer was ever charged.

**Holds 20–30?** Yes — two trials, a Royal Commission, a pardon, a planted exhibit.

**Ad-safety.** MEDIUM on the crime (double homicide, no children) — **the coordinator's "ad-safe" read is broadly right on the 1970 facts and wrong once the 2019 charges enter the film.**

**Saturation.** UNVERIFIED. **US-context cost — ~45s**, cheaper than Pora (no Privy Council).

**➡ Verdict between the two NZ picks: on protagonist archetype and context cost, Thomas beats Pora. On carrier safety and quote verification, Pora beats Thomas decisively.** Thomas is only viable if (a) the Royal Commission quote verifies and (b) the owner accepts handling the 2019–2022 charges on screen. **Neither condition is met today.**

---

#### CW8. Ireland — Mother and Baby Homes / Tuam · **ORD** · **[LOSS-VERB]** · ★
**Premise.** A local housewife proved 796 children died in one Catholic-run home and almost none had a grave; twelve years later the State is still digging them out from under a housing estate.

**Carrier — ordinary-citizen, and the IJ/Civil-Rights-Lawyer shape: an outsider who took the institution on.** **Catherine Corless** (b. 1954), a local historian. At her own expense she obtained the death certificate of every child recorded as dying at the Tuam Home — **796 names** — then checked them against local burial records and found documented burials for **exactly two.**

**Stakes gap.** **62** DNA reference samples collected from living relatives for the entire identification programme as of 15 July 2026 → approximately **9,000** children died across the institutions investigated, **~15% of all children in their care**. Sharper on screen: **796 dead at Tuam → 99 sets of remains recovered** after a full year of excavation.

**Institution + consequence.** The **Bon Secours Sisters**, running the home for **Galway County Council** — Church *and* State, which is the structural fact of the film. **No prosecutions, no convictions, nobody named or charged.** A 2021 apology and a **€2.5m voluntary contribution** against excavation costs then estimated at €6–13m, explicitly not a settlement. The order still operates as a healthcare provider.

**QUOTE — [V-PRIMARY] (read from the official Oireachtas record).**
> *"It is deeply distressing to note that the very high mortality rates were known to local and national authorities at the time and were recorded in official publications."*
> — **Micheál Martin TD, Taoiseach**, State apology, Dáil Éireann, **13 January 2021**. `https://data.oireachtas.ie/akn/ie/debateRecord/dail/2021-01-13/debate/mul@/main.xml`
> Same record, the Commission's own finding quoted by Minister Roderic O'Gorman: for children born before 1960 *"the homes did not save the lives of 'illegitimate' children; in fact, they appear to have significantly reduced their prospects of survival."*
> **⚠ CORRECTION: the Varadkar line is *"a stifling, oppressive and deeply misogynistic culture"* — "brutally misogynistic" is wrong. Do not use it.**

**Living / legal — lowest legal risk in the Commonwealth set.** Every damning line is a Commission finding, a Taoiseach's words in parliament, or the order's own signed apology. Risk arises only if you assert individual criminal culpability against a named nun or official — **the Commission named none. R1/R2.**

**Present tense — the strongest in this pool, and it is physical.** Per **ODAIT Technical Update 8 (22 July 2026)**: excavation **ongoing**; a subsurface well **halted on safety grounds**; forensic analysis only just begun at a new **€4.1m** facility; **not one child publicly identified**; and the identification programme is **legally blocked** — first cousins are still ineligible to give DNA under the Institutional Burials Act 2022, pending a government amendment. **Hence 62 samples.** `https://odait.ie/news/technical-updates/technical-update-8/`

**Holds 20–30?** Yes — Corless's twelve-year hunt, the certificates, the 2017 test excavation, the apology, the dig, the legal block.

**Ad-safety.** HIGH but manageable: **no images of remains**, frame as forensic investigation, keep narration clinical, and **avoid "mass grave" in the title** in favour of "796 death certificates."

**Saturation — saturated on history, wide open on the present.** Largest: "Tuam Orphanage: Children Of Shame," Best Documentary, 53:45, **1,154,045 views** (Apr 2024); then DW, 28:27, **351,978**. **Every one of them predates the excavation.**

**US-context cost — 45–70s, not fatal, and Irish-American heritage genuinely discounts it.** Taoiseach and Dáil are one-clause glosses; only the Church-State relationship needs a real beat (~30s) and it is *content*, not overhead — **the county council paid the nuns per head.**

**⚠ Mechanism.** Adjacent to UK2 but not identical: UK2's machine is *adoption*, Tuam's is *death and concealment*. **They can coexist but never adjacent** — UK2's measured saturation note warns that US viewers conflate them, and whichever is built second must distinguish itself in the first 30 seconds.

---

#### CW9. Maurice McCabe (Ireland) · **ORD** · **R3**
**Premise.** An Irish police sergeant reported colleagues wiping traffic penalties for friends, and the head of the national force ran a campaign to destroy him — including a child-protection file accusing him of a rape he was never accused of.

**Carrier.** **Sgt Maurice McCabe.** From the tribunal report: a counsellor building a referral form **reused a previous client's form as a template and typed over it**, leaving another woman's allegation of digital penetration on McCabe's file. Charleton: *"This referral jumbling up Ms D with Ms Y and dishing it all up against Maurice McCabe was sent to the Health Service Executive."* His verdict on how: *"What happened was a hideous coincidence."*

**Stakes gap.** One sergeant in one rural station complaining about cancelled penalty points → **almost 1.5 million** phantom breath tests recorded on the police system that were never carried out (7 June 2009 – 10 April 2017), discovered only because McCabe forced outsiders to look.

**Institution + consequence.** **Commissioner Martin Callinan**, who on live television before the Public Accounts Committee (23 Jan 2014) called McCabe's conduct **"disgusting."** He retired in March 2014: **no prosecution, no discipline, full pension.** Press officer **Supt David Taylor** claimed he was following orders; Charleton: *"he claimed for the first time a kind of Nuremberg defence: that he was acting under orders,"* then flatly, *"This is daft evidence."* Commissioner **Nóirín O'Sullivan was vindicated** — and in October 2018, the month the report landed, was appointed **UN Assistant Secretary-General for Safety and Security.**

**QUOTE — [V-PRIMARY★] (PDF fetched and text-extracted).**
> *"In the result, the tribunal has been convinced that there was a campaign of calumny against Maurice McCabe by Commissioner Martin Callinan and that in it he was actively aided by his press officer Superintendent David Taylor."*
> — **Mr Justice Peter Charleton**, Supreme Court judge and sole member of the Disclosures Tribunal, *Third Interim Report*, **11 October 2018**, ~p.274. `https://www.rte.ie/documents/news/2018/10/disclosures-tribunal-third-interim-report.pdf`
> Closing narration, verbatim from the same PDF: *"What has been unnerving about more than 100 days of hearings in this tribunal is that a person who stood up for better standards in our national police force, Sergeant Maurice McCabe, and who exemplified hard work in his own calling, was repulsively denigrated for being no more than a good citizen and police officer."*

**Living / legal — SERIOUS.** Every principal alive; **Ireland's Defamation Act 2009 is claimant-friendly and YouTube publishes into that jurisdiction.** Rules if greenlit: say only what the tribunal found, in the tribunal's words; **state O'Sullivan's vindication unambiguously**; never identify Ms D or Ms Y; do not name the Tusla counsellor even though the report does; do not name the briefed journalists. **R3 — legal review required.**

**Present tense — weak.** Closed 2018.

**Holds 20–30?** Yes.

**Ad-safety.** Worse than Tuam and structurally so: **the engine is a false child-sexual-abuse allegation against a named living man, and the detail that makes it land cannot go in the title or thumbnail.** Strip it out and you are selling a procedural about traffic tickets.

**Saturation.** RTÉ's *Whistleblower: The Maurice McCabe Story* (2018) drew 509,000 average broadcast viewers. A 20+ minute YouTube search returned **zero** results. **Working read: open ground that nobody is asking for.**

**US-context cost — 150–240s, close to fatal.** An Garda Síochána (a single national force — load-bearing, because the horror is that there is nowhere else to go), Garda Commissioner, Tribunal of Inquiry (compels witnesses, delivers no verdict and no penalty — **Americans will wait for a sentencing that never comes**), Tusla, Taoiseach/Tánaiste/Dáil, the PAC, the Protected Disclosures Act. **No Irish-American discount applies** — diaspora affinity attaches to famine, emigration and the Church, not to Garda governance.

---

### 3.3 JAPAN / KOREA / TAIWAN

*Two independent research streams covered this region and disagreed on several details. Every conflict is flagged below rather than smoothed over.*

---

#### AS1. Japan — forced sterilisation under the Eugenic Protection Law · **ORD**
**Premise.** For 48 years a Japanese statute authorised doctors to sterilise disabled citizens — with restraint, anaesthetic and deception permitted **in writing** by the health ministry — and the state defended it in court until 2024.

**Carrier — ordinary-citizen.** **Saburo Kita** (北三郎, a court-granted pseudonym), 81. Sterilised at **14** in a children's home; hid it from his wife through 40+ years of marriage and told her only as she was dying. He makes **paper-flower arrangements**. On the courthouse steps, 3 July 2024: *"I can finally see a ray of hope. I'm sure my wife would also be glad that we won."*
**⚠ Stream conflict:** one stream verified Kita and treats him as the carrier; the other could **not** verify him and names **Yumi Suzuki**, a plaintiff cited in the ruling. **Resolve before use, and note that pseudonymous plaintiffs must never be identified.**

**Stakes gap.** **¥3.2m (~$20,000)** was the entire 2019 payment and only **1,110 people** were ever certified under it — against **~25,000 sterilised, ~16,500 without consent**, girls as young as **nine**. Only **39 people in all of Japan ever sued.**

**Institution + consequence.** Ministry of Health and Welfare; **the Diet passed the law unanimously.** Named instrument: the 24 Dec 1954 notice *"Promotion of Eugenic Operations Subject to Examination."* **Consequence: nothing, to anyone.**

**QUOTE — [V-PRIMARY], from the Supreme Court's own English text.**
> *"in implementing the abovementioned measures, the State actively promoted eugenic operations by, for example, issuing the Vice-Ministerial Notice to prefectural governors, stating that **the use of physical restraint, anesthetics, deception or other means may be permitted** in some cases when performing eugenic operations which required examination"*
> — Supreme Court of Japan, **Grand Bench**. `https://www.courts.go.jp/english/Judgments/search/2066/index.html`
> Same judgment: the state's reliance on the time limit was *"extremely contrary to the principles of justice and fairness"* and an *"abuse of rights."*
> **⚠ CORRECTION 9 (§0.6): that page's date/case-number field renders as `2025.09.22`, which does not match the 3 July 2024 Grand Bench ruling. The reporter citation is *Minshu* Vol. 78 No. 3 (=2024) and the prior instance is Osaka High Court 23 March 2023. The text is unmistakably the eugenics ruling. DO NOT PUT A DATE ON SCREEN FROM THIS PAGE ALONE.**
> **PM Fumio Kishida**, Kantei official English (marked "[Provisional translation]"), **3 July 2024** — `https://japan.kantei.go.jp/101_kishida/statement/202407/03kaiken.html`: *"Sterilization and other procedures trample upon human dignity and are an infringement of human rights that must never be tolerated."* and *"The Government, from the standpoint of having implemented the former Eugenics Protection Law, expresses its sincere remorse and its profound apology regarding this matter."*

**Living / legal.** Plaintiffs alive and elderly; several use **court-granted pseudonyms — do not attempt to identify them.** No named individual villain, so defamation exposure ≈ zero. **R1/R2.**

**Present tense.** A new law (in force Jan 2025) pays ¥15m/¥5m/¥2m. But **prefectural sterilisation records were destroyed in most of Japan**, so most of the 25,000 can never be identified; the ~8,000 who "consented" under duress are a live dispute; forced-abortion victims get one-seventh of what sterilisation victims get; **claimants are dying faster than the state processes them.**

**Holds 20–30?** Yes.

**Ad-safety — HIGHEST in the East Asian set.** Surgical/reproductive content + children + disability + Nazi adjacency + forced abortion. Survivable with clinical vocabulary and zero surgical imagery; **expect limited ads on first pass.**

**Saturation.** Effectively virgin in English long-form — largest verified item **194 views**. NHK World has *"The Unbreakable Silence"*; reach unverified.

**US-context cost — ⚠ THE TWO STREAMS DISAGREE SHARPLY, 30–45s vs 90–150s.**
- The optimistic read: **Buck v. Bell** means America did it first and bigger (~60,000+ sterilised under state laws), so you open on the American law and reveal Japan ran the same programme **until 1996** — a year Americans remember. **~30–45s.**
- The pessimistic read, and I find it more persuasive: the case turns on **除斥期間**, the *period of exclusion* — not a statute of limitations as Americans understand it, but a hard extinguishment running from the act, not from discovery, and untollable. **Explaining why a man sterilised in 1957 was out of time before he knew he had a claim is 45–70s on its own.**
- **Honest planning number: 90s, with Buck v. Bell mandatory as the on-ramp.**

---

#### AS2. South Korea — the overseas adoption programme · **ORD** · **[LOSS-VERB]** · ★
**Premise.** South Korea ran a state-supervised, quota-driven export of its own children — falsifying orphan records and substituting dead babies' identities for living ones — and about 112,000 of them were raised by American families who were never told.

**Carrier — ordinary-citizen, and an American one.** **Phillip Clay**, born **Kim Sang-pil**. Found abandoned in Seoul in 1981 and adopted into a Philadelphia family who never completed his naturalisation. **Deported to Korea in 2012** speaking no Korean and knowing no one. Diagnosed bipolar; care failed on language. **In 2017 he jumped from the 14th floor of a building in Seoul.**
Alternative living carrier: **Adam Crapser**, adopted 1979, abused by two sets of adoptive parents, deported 2016, won a partial judgment against Holt in **May 2023 (~$75,000)**, now lives in Mexico. **⚠ Crapser is litigious and has publicly objected to how his story was dramatised (*Blue Bayou*) — get it exactly right or use Clay.**

**Stakes gap.** **56** — the number of cases the Truth and Reconciliation Commission recognised out of **367** examined — against **~170,000–200,000** children sent abroad since 1950, of whom **~112,000 went to American families**, and roughly **20% of adult Korean adoptees in the US still lack citizenship**.

**Institution + consequence.** The Korean state and the agencies — **Holt Children's Services, Korea Social Service, Eastern Social Welfare, Korea Welfare Services** — operating on government quotas. **Consequence: a commission finding, a presidential apology, and one civil judgment of about $75,000.** No agency lost its licence; no official was prosecuted.

**QUOTE — [V-PRIMARY], and there are three of increasing rank.**
> TRC Chairperson **Park Sun-young**, March 2025: *"Throughout this process, numerous legal and policy shortcomings emerged, leading to serious violations of the rights of adoptees, their biological parents – particularly birth mothers – and others involved."* … *"These violations should never have occurred."*
> From the report itself — **the single most damning line available**: *"If a child in the adoption process passed away or was reclaimed by their biological family, agencies would substitute another child's identity to expedite the adoption, severely violating adoptees' rights to their true identities."*
> `https://www.aljazeera.com/news/2025/3/26/serious-violations-found-in-south-korean-foreign-adoptions-programme`
> **A sitting head of state — President Lee Jae-myung, 2 October 2025**, the day after Korea's ratification of the Hague Adoption Convention took effect: *"Representing South Korea, I extend my sincere apology and consolation to adoptees, their birth families and adoptive families for their sufferings."* `https://www.koreaherald.com/article/10588687`
> **⚠ The official English report — *TRC Report: Human Rights Violations in Intercountry Adoption*, 18 Nov 2025 — is listed at `https://www.jinsil.go.kr/en/nac/selectNoticeDetail.do?bbsId=BBSMSTR_000000000723&nttId=326600` but the PDF link is JavaScript-driven and resolves to "#". Somebody should pull that PDF; it is the primary document.**

**Living / legal.** Crapser alive; Clay dead by suicide 2017. **Holt International is a live, well-resourced US entity that has litigated — stay inside the TRC findings and the 2023 judgment. R2.**

**Present tense.** **311 of 367 applicants were not recognised**, and adoptee groups called the finding *"empty"*; in April 2025 they gathered at the commission demanding a new investigation, and the mandate then lapsed with ~5,000 Brothers-Home-linked cases pending. **More than 100 babies a year were still being sent abroad in the 2020s.** And in the US, **the Adoptee Citizenship Act has never passed** — the Child Citizenship Act of 2000 excluded anyone adopted before 1983 who had already turned 18, so **US-raised adoptees remain deportable in 2026.**

**Holds 20–30?** Yes, comfortably — the programme, the falsified files, Clay, Crapser, the 2025 finding, the apology, and a live American statute.

**Ad-safety.** **MEDIUM — the best profile of the East Asian set.** Child-trafficking framing is the only flag; no sexual violence, no gore. The Clay suicide needs the standard handling and a support-line card.

**Saturation.** Known works: *First Person Plural*, *Twinsters*, *Geographies of Kinship*, the 2021 feature *Blue Bayou*; AP and **PBS Frontline (September 2024)** ran major investigations. **⚠ Frontline is a real competitor and must be measured.** But coverage has been news and festival documentary, **not YouTube long-form, and none of it covers the 2025 state finding.**

**US-context cost — ZERO. THE LOWEST IN THE ENTIRE POOL, AND IT IS NOT CLOSE.** **112,000 of these children were raised in American houses, in American towns, by American parents.** Your viewer either knows an adoptee or grew up in a town that had one. And the story does not stay abroad — **it ends with the United States deporting its own adopted children to a country they never knew, one of whom died.** You can open in Philadelphia. **You never have to explain a single foreign institution before the viewer is committed.**

---

#### AS3. Brothers Home / 형제복지원 (Busan) · **ORD**
**Premise.** Ahead of the 1988 Seoul Olympics, South Korea swept its streets into a walled "welfare" compound where 657 people died — and the director served two and a half years for embezzlement.

**Carrier — ordinary-citizen.** **Han Jong-sun (Hahn Jong-seon)**, taken in as a child with his sister by their father, who then vanished. A **year-long solo protest** outside the National Assembly from 2012; a public head-shaving in 2015; a hunger strike; and in September 2017 **a 500km walk from Busan to the Blue House over two months.** Alternative: **Park Soon-hee**, detained at **age 10** — *"This trauma and stigma will stay with me until I die."*

**Stakes gap.** **2½ years** — the total Park In-geun served, for embezzlement — against **~38,000 detained 1975–1986** and **657 dead**. In 1986 alone the facility held **3,975 inmates**, **3,117 delivered by police**, and bought **250,000 chlorpromazine tablets**.

**Institution + consequence — the most infuriating in the pool.** Ulsan District Court convicted **Park In-geun** on all counts, **23 June 1987, 10 years**; Daegu High Court cut it to 4; **the Supreme Court threw out every illegal-confinement charge on 8 March 1988**, holding the confinement lawful under **Interior Ministry Order No. 410**. Re-charged 2014; proceedings suspended for dementia; **died 2016, never punished for a single day of the detentions.**

**QUOTE — [V-PRIMARY], but not the one we wanted.**
> **Justice Minister Jung Sung-ho**, September 2025, on the government dropping all 52 appeals: *"is a testament to the state's recognition of the human rights violations (that occurred) due to state violence in the authoritarian era."* `https://www.koreaherald.com/article/10575174` *(the parenthetical is the Korea Herald's insertion)*
> The more cinematic verified item — **a 1981 South Korean government propaganda film** described Brothers Home as *"an exemplary social welfare centre for the homeless."* `https://www.aljazeera.com/features/2021/12/10/secrets-of-south-koreas-house-of-horrors-hidden-in-australia`. Survivor **Yeon Seng-mo**, same source: *"If we didn't finish it, we were beaten with baseball bats."*
> **⚠ Both streams independently failed to obtain the TRC's own August 2022 wording** — the TRC English site carries no Brothers Home release and AP/NYT/BBC/DW/Yonhap/Hankyoreh are all blocked. **Budget a dedicated pass for it; AP's Kim Tong-hyung did the definitive reporting.**

**Living / legal.** **Park In-geun dead (2016)** — the dead cannot be defamed and the facts are TRC- and court-established. **R1.** Survivors alive and litigating.

**Present tense.** January 2024 award of **4.535bn won to 13 survivors**, upheld by the **Supreme Court in March 2025**; the government **dropped 52 appeals in September 2025**, covering **647 victims**. As of February 2025 the TRC had confirmed **at least 31 children improperly sent overseas for adoption**, with ~5,000 cases pending. **No state apology has been issued.**

**Holds 20–30?** Yes.

**Ad-safety — SEVEREST IN THE POOL.** Systematic sexual violence against children and adolescents, child deaths, forced labour, chemical restraint, mass graves, and a "Korea's Auschwitz" framing in Korean media. **A faithful treatment will be demonetised.** The only survivable build is the *legal* story — the acquittal, the 2½ years, the 2025 capitulation — keeping the facility at arm's length. **Do not use the Auschwitz comparison in title or thumbnail.**

**Saturation — rising.** **Netflix, *The Echoes of Survivors: Inside Korea's Tragedies*, September 2025, covers Brothers Home.** The window is narrowing.

**US-context cost — 30–60s, with two American anchors.** **The 1988 Seoul Olympics** — this audience watched them on NBC, and *"the people you didn't see were in a camp"* lands instantly. Stronger: **Brothers Home placed children with six named American agencies** — Holt International, Children's Home Society of Minnesota, Dillon International, Children's Home Society of California, Catholic Social Services and Spence-Chapin. **Not context-heavy — ad-safety is what may kill it.**

---

#### AS4. Minamata (Japan) · **ORD**
**Premise.** A chemical company poisoned a fishing bay with mercury for decades, and seventy years later the government still refuses to certify most of the people it crippled.

**Carrier — ordinary-citizen.** **Shinobu Sakamoto** (b. 1956), congenital Minamata patient, who testified at the **1972 UN Conference on the Human Environment in Stockholm at sixteen** and again at the Minamata Convention in Geneva in 2017. Alive.
Alternative, if it verifies: **Shigemitsu Matsuzaki**, 82, whose microphone was cut off three minutes into telling the Environment Minister about his wife **Etsuko, who died in April 2023 still officially unrecognised.** **⚠ MEDIUM CONFIDENCE ONLY — see the correction below.**

**Stakes gap.** **3 minutes** of speaking time against **68 years**. Numerically: **2,265–3,000 ever certified** (sources differ), **1,784 of them dead**, against **45,933** applications under the 2009 relief law and **over 70,000** claiming harm — an **8%** certification rate on the pending pool.

**Institution + consequence.** **Chisso Corporation** (liability shell now **JNC**) discharged methylmercury from the 1930s–40s until **18 May 1968**. The 1976 criminal convictions of two Chisso executives ended in **suspended sentences**. The modern antagonist is the **Ministry of the Environment**.

**QUOTE — [V-PRIMARY], from the court's own official English.**
> *"the failure to exercise the regulatory authorities under the Water Quality Laws in January 1960 and thereafter is extremely unreasonable in light of the purport and purpose of the Water Quality Laws that are the basis of the authorities and the nature of the authorities, and therefore illegal for the purpose of the application of Article 1(1) of the Law Concerning State Liability for Compensation."*
> — Supreme Court of Japan, Second Petty Bench, case 2001(O)1194, **15 October 2004**. `https://www.courts.go.jp/english/Judgments/search/1260/index.html`
> **⚠ CORRECTION 10 (§0.6): the May 2024 microphone-cutting incident could NOT be verified by either stream.** One stream reached Minister **Shintaro Ito** via Jiji English (*"I apologize from the bottom of my heart. I deeply regret it and I am very sorry."*, 8 May 2024, `https://sp.m.jiji.com/english/show/32860`) but could not verify the incident itself; the other could not reach it at all. **The verified and arguably more damning fact is that on 22 March 2024 the Kumamoto District Court rejected the claims of all 144 plaintiffs — six weeks before the microphones were cut.**

**Living / legal.** Sakamoto, Matsuzaki and Ito alive. **Chisso/JNC is a live corporation — attribute to the 2004 judgment and to institutions. R1/R2.**

**Present tense.** ~1,800 in active litigation; Osaka recognised 128 in Sept 2023 and Kumamoto and Niigata followed — **the state appealed.** The promised methylmercury exposure survey is the live accountability test. **There is still no final number of victims.**

**Holds 20–30?** Yes.

**Ad-safety.** HIGH — congenital birth defects and foetal poisoning. Keep symptoms in narration, not on screen.

**Saturation — HIGH, and the highest-confidence saturation call in the East Asian set.** The **2020 Johnny Depp feature *Minamata*** put the American-photographer angle into circulation and crowds every search.

**US-context cost — ~15s, among the cheapest in the pool.** **W. Eugene Smith**, LIFE photographer, lived in Minamata 1971–74 and was **beaten by Chisso-hired men in 1972**; *"Tomoko Uemura in Her Bath"* hangs in MoMA, the Met and the Smithsonian. A 55+ American male was alive when that photo ran.
**⚠ Rights trap that is also the best beat: the Tomoko photograph was withdrawn from circulation in 1997 at the Uemura family's request. DO NOT reproduce it. You may name and describe it.** *"The most famous photograph of this disaster is one you are not allowed to see"* is a gift.

---

#### AS5. Ohkawara Kakohki / Japan's hostage justice · **ORD** · best evidence, worst on-ramp
**Premise.** Tokyo's political police decided a Yokohama machine shop's food-drying equipment was a bioweapons plant, jailed three executives for 332 days to make them confess, let one die of stomach cancer in a cell, dropped the case — and the harshest punishment any officer received was a **one-month 10% pay cut.**

**Carrier — ordinary-citizen.** **Shizuo Aishima**, 72, company adviser. Diagnosed with **advanced stomach cancer inside the detention centre on 7 October 2020**; his lawyer applied for bail **seven or eight times so he could get treatment — refused every time**; died **7 February 2021**, two days after his colleagues were released and five months before charges were dropped. **⚠ Stream conflict: one says seven applications, the other eight. Resolve before use.**
In **August 2025** Tokyo police and prosecutors went to his **grave**, laid flowers and bowed. His widow: *"I accept your apology, but I can never forgive you."*

**Stakes gap.** **332 days** of pre-trial detention (bail granted only on the sixth request for the survivors) → **zero criminal indictments** and a **one-month 10% pay cut** as the maximum sanction, given to two **already-retired** officials. **¥166m (~$1.12m)** for three ruined lives and one death.

**Institution + consequence.** **Tokyo Metropolitan Police Public Security Bureau, Foreign Affairs Division 1** and the **Tokyo District Public Prosecutors Office.** 19 officials disciplined administratively (7 Aug 2025); the Superintendent-General apologised publicly. **Nobody prosecuted.** A Prosecution Review Board found the investigators had proceeded 「立件ありき」 ("charge-first").

**QUOTE — [V-SECONDARY, corroborated across three outlets]. The best single line in this entire pool.**
> **A serving MPD Public Security investigator** (公安部外事一課, rank 警部補, name not public), under questioning in open court, **Courtroom 712, 30 June 2023**, asked whether the Public Security Bureau had fabricated the case:
> 「まあ、捏造ですね」 — ***"Well — it's a fabrication."*** *(translation ours)*
> Sources: `https://www.gentosha.jp/article/28480/` · `https://ja.wikipedia.org/wiki/大川原化工機事件`, which cites Asahi (`https://www.asahi.com/articles/ASR6Z659DR6ZUTIL02P.html`, 30 June 2023), TBS NEWS DIG and NHK. **asahi.com is blocked from this environment; verify against NHK or Asahi before broadcast — but two independent streams reached identical wording.**
> Tokyo District Court, **27 December 2023**: 「必要な捜査を尽くすことなく行われたものであり、違法である」 — *"It was carried out without conducting the necessary investigation, and is illegal."*
> Best **English** verbatim — **Tokyo High Court, 28 May 2025**, Presiding Judge **Teruyoshi Ota**, via Kyodo: the police interpretation *"lacked rationality"*; there were *"fundamental problems"*; the *"arrests lacked reasonable grounds."* `https://www.nationthailand.com/blogs/news/world/40050576`
> Police apology, AP wire reprint — MPD Deputy Superintendent-General **Tetsuo Kamata** at the grave: *"We deeply apologize for our illegal investigation and arrest."* `https://www.bastillepost.com/global/article/5145864-japanese-officials-apologize-at-grave-of-wrongfully-detained-man-denied-timely-cancer-treatment`
> **⚠ AP dates the High Court ruling to "June 2024"; Kyodo and Jiji both say 28 May 2025 — AP is wrong.**

**Living / legal.** Ōkawara (76+) and Shimada (72+) alive; Shimada has testified before the Diet. **Naming the institutions is near-risk-free** — a final, unappealed High Court judgment says the arrests and the indictment were illegal and the MPD admitted it in writing. **Do not attempt to identify 警部補X. R2.**

**Present tense — the most live case in the East Asian set.** In **March 2026** Aishima's family sued the state **over the judges themselves**, arguing it was unconstitutional to refuse bail to a dying man with no flight risk; **37 judges** are implicated. On **29 June 2026 the government moved to have that suit dismissed** — **having apologised at the grave, the state is now fighting the widow in court.** Hostage justice is unreformed.

**Holds 20–30?** Yes.

**Ad-safety — LOWEST IN THE POOL.** No gore, no minors, no sexual content. The only keyword risk is "biological weapons."

**Saturation — essentially virgin in English.** Adjacent: Apple TV+'s *Wanted: The Escape of Carlos Ghosn* has an episode titled "Hostage Justice."

**US-context cost — 180–300s. THE HIGHEST IN THE POOL, AND WITHOUT A SPECIFIC CRUTCH IT IS FATAL.** You must teach four unfamiliar systems: 23-day detention per charge with re-arrest to restart the clock; bail refused to anyone who denies the charge; a ~99.8% conviction rate (so trial is not where guilt is decided); and that "Public Security Bureau" means political police.
**The crutch is Carlos Ghosn and it is genuine.** This audience watched a Nissan CEO held 108 days and flee Japan in a musical-instrument case; the UN Working Group on Arbitrary Detention (Opinion 59/2020) called his detention arbitrary and Japan called that finding *"totally unacceptable."* **Bridge: *"You remember the billionaire who fled Japan in a box. This is what happens to the people who can't."*** With that ramp it works and does 80% of the teaching in 45 seconds. **Without it, do not attempt it. And never open on the spray dryer.**

---

#### AS6. Ashikaga case / Toshikazu Sugaya (Japan) · **A-t-C**
**Premise.** Japan's first DNA conviction was Japan's first DNA exoneration — the same technology that jailed a man for 17½ years freed him, and the real killer has never been caught.

**Carrier.** **Toshikazu Sugaya**, a kindergarten bus driver, arrested December 1991 for the murder of **4-year-old Mami Matsuda**, whose body was found on the bank of the **Watarase River** on 13 May 1990. Released June 2009, acquitted 26 March 2010. Compensation **¥80 million**.

**Stakes gap.** **1** first-generation **MCT118** DNA test → **17½ years**, and **five** dead or missing girls aged 4–8 across a 20km radius of Tochigi/Gunma between 1979 and 1996 whose killer is still free.

**Institution + consequence.** Tochigi Prefectural Police, the Utsunomiya District Prosecutors Office, and **courts that refused DNA re-examination for years.** **Apologies only** — the statute of limitations had run. Journalist **Kiyoshi Shimizu**, not the state, cracked it in 2007.

**QUOTE — [V-PRIMARY]. The single cleanest verbatim in the East Asian set — a sitting judge apologising from the bench.**
> 「菅家さんの真実の声に十分に耳を傾けられず１７年半の長きにわたり、その自由を奪う結果となりましたことを、この事件の公判審理を担当した裁判官として、誠に申し訳なく思います」
> ***"As the judges who presided over the trial in this case, we are truly sorry that we failed to listen sufficiently to Mr Sugaya's true voice, and that the result was to deprive him of his freedom for as long as seventeen and a half years."*** *(translation ours)*
> — Presiding Judge **Masanobu Sato** (佐藤正信), Utsunomiya District Court, retrial acquittal, **26 March 2010**, quoted in the **Japan Federation of Bar Associations' President's Statement** of the same day. `https://www.nichibenren.or.jp/document/statement/year/2010/100326.html`
> Corroborated at `https://ja.wikipedia.org/wiki/足利事件`, which also carries the prosecutor's apology at the sixth retrial hearing.
> **Both streams independently verified this quote and this source. It is the most solid non-English item in the pool.**

**Living / legal.** Sugaya alive (~79), fully exonerated, publicly campaigning — **zero defamation risk in naming him.** The suspected real killer is unnamed and unconvicted — **do not identify him. R1/R2.**

**Present tense.** All five North Kanto cases remain **unsolved with no arrest.** Most are time-barred; the 1996 disappearance of **Yukari Yokoyama**, whose body was never found, is the exception. Interrogations are still not fully recorded in most cases.

**Holds 20–30?** Marginal — the spine is one man, one test and one apology.

**Ad-safety.** MEDIUM-HIGH — a 4-year-old victim and sexual-homicide adjacency. Manageable: the story is about the wrong man, not the crime.

**Saturation.** UNVERIFIED; likely low in English.

**US-context cost — 20–30s, among the cheapest.** DNA exoneration is the most legible justice frame in America. And it carries an inversion the American canon has never shown: **here DNA was the evidence that convicted him.** One sentence on coerced confession and nothing else.

---

#### AS7. Chiang Kuo-ching (Taiwan) · **A-t-C**
**Premise.** Taiwan's air force tortured a 21-year-old conscript into confessing to the rape and murder of a child on his own base, shot him, and fourteen years later admitted it had the wrong man — and the case is still unsolved.

**Carrier.** **Chiang Kuo-ching**, 21. Held **37 hours in a darkened bunker** under round-the-clock interrogation and **forced to watch autopsy video** of the 5-year-old victim until he confessed. **Executed by firing squad 13 August 1997.** His last recorded words: *"I did not kill that person."*
**The better carrier is his father**, who filed a complaint with the Control Yuan **in 1996 — before the execution — saying his son was being tortured. It changed nothing, and he died before the exoneration.**

**Stakes gap.** **37 hours** of interrogation against **14 years** to admit the error, and **zero** criminal convictions of anyone — against **five officers fined a combined NT$59.5 million** and family compensation of **NT$131.8 million**. **⚠ Figures vary by report; verify. One source rendered the crime date as 1986 — wrong; it was 12 September 1996, sentence 26 December 1996, execution 13 August 1997.**

**Institution + consequence.** The **Air Force Combatant Command's Department of Counterintelligence** — a **non-judicial organ** handed the entire investigation. **No criminal charges: the 10-year limitation period for public servants had expired.** **Chen Chao-min**, the Air Force commander who unlawfully handed them the case, **later became Minister of National Defense (2008–09) and was never prosecuted.**

**QUOTE — [V-PRIMARY], and it needs no translation caveat.**
> *"The Department of Counterintelligence was suspected of extracting Chiang's confession through torture for the sake of a quick end to the investigation, leading to his wrongful execution."*
> and *"The Department unlawfully detained Chiang, employing illegal practices such as exhausting and suggestive interrogation, in contravention of Chiang's rights as well as the procedure prescribed by law."*
> — the **Control Yuan**, Taiwan's constitutional oversight branch, **in its own English-language investigation report**. `https://www.cy.gov.tw/en/News_Content.aspx?n=252&s=16384`
> **A branch of the Taiwanese state, in English, saying its own military tortured a man to death.** President Ma Ying-jeou's apology is **[NONE VERIFIED]**.

**Living / legal.** Chiang and his father dead. **Chen Chao-min is alive — name him only as the Control Yuan does.** **Hsu Jung-chou (許榮洲) is alive: convicted in 2011, then released in 2013 when charges were dismissed for insufficient evidence — DO NOT call him the murderer.** Say the state has convicted no one. **R1.**

**Present tense.** **Nobody has been convicted of killing the child.** The man the military produced as the real killer walked. The officers who tortured Chiang escaped on a technicality. **The only people punished were fined.**

**Holds 20–30?** Marginal.

**Ad-safety — SEVERE.** Rape and murder of a five-year-old, torture, and an execution by firing squad. Keep the crime to a single narrated sentence and never in imagery.

**Saturation.** UNVERIFIED; almost certainly near-zero in long-form English.

**US-context cost — 70–120s.** Military justice translates via UCMJ and courts-martial, so this is a translation rather than a lesson — **but "Control Yuan" costs 30 seconds by itself and there is no direct American anchor.**

**➡ Hsichih Trio comparison — take Chiang.** The Trio survived (acquitted 2012 after 21 years), which is a fraction of the moral force; three protagonists dilute the carrier; the 21-year procedural back-and-forth is far more expensive to explain; and the 2012 acquittal rested partly on burden of proof, leaving an ambiguity documentary audiences hate. Chiang gives one face, one age, one sentence, and a father who warned them in writing beforehand.

---

### 3.4 EUROPEAN STATE FAILURES

---

#### EU1. Netherlands — the childcare-benefits scandal (toeslagenaffaire) · **ORD** · **[LOSS-VERB]**
**Premise.** A tax computer flagged 26,000 families as childcare-benefit fraudsters over paperwork errors, clawed back everything, and the state took their children.

**Carrier — ⚠ ordinary-citizen, but NOT NAMED THIS PASS. Blocking gate.** Pick a named parent from the 2020–21 hearings. **The engine detail is structural and brutal:** under the **"alles-of-niets"** (all-or-nothing) rule, **a single missing signature** or a partly unpaid parent contribution voided the entire year's benefit — and the full year was reclaimed, money already spent on childcare.

**Stakes gap.** **One missing signature** → **26,000 families** (~70,000 children); **2,090 children removed from their homes between 2015 and June 2022**; **€30,000** base compensation each; **the entire Rutte cabinet resigned 15 January 2021.**

**Institution + consequence.** **Belastingdienst/Toeslagen.** State Secretary **Menno Snel** resigned Dec 2019; **Eric Wiebes** resigned Jan 2021; **Lodewijk Asscher** quit as PvdA leader; Rutte resigned — **and won the next election.** **No criminal prosecution of any official.** A resigning government is a rare payoff and does not require an inquiry to deliver it.

**QUOTE — [V-PRIMARY★] (PDF downloaded and text-extracted).**
> *"De commissie constateert dat bij de uitvoering van de kinderopvangtoeslag grondbeginselen van de rechtsstaat zijn geschonden. Dit verwijt treft niet alleen de uitvoering – specifiek de Belastingdienst/Toeslagen – maar ook de wetgever en de rechtspraak."*
> **[translation]** *"The committee finds that in the implementation of the childcare benefit, fundamental principles of the rule of law were violated. This reproach applies not only to the implementation — specifically the Tax Authority/Benefits — but also to the legislature and the judiciary."*
> — Parliamentary Interrogation Committee, ***Ongekend onrecht*** ("Unprecedented Injustice"), **December 2020**. `https://www.tweedekamer.nl/sites/default/files/atoms/files/20201217_eindverslag_parlementaire_ondervragingscommissie_kinderopvangtoeslag.pdf`
> Same document: *"Onder druk van een oververhitte politieke behoefte aan fraudebestrijding…"* — *"Under pressure from an overheated political demand for fraud enforcement…"*
> **The report's title alone — "Unprecedented Injustice" — is a title card.**

**Living / legal.** Nearly everyone alive. **Rutte is now NATO Secretary-General — a live, powerful subject.** Officials named in an official parliamentary report = low defamation risk **if you quote the report. R2.**

**Present tense.** Compensation is years behind schedule; the recovery agency (UHT) is paying statutory penalties for missed deadlines; thousands still contest rejections. **Most of the removed children were never returned. That is the open wound.**

**Holds 20–30?** Yes.

**Ad-safety.** Moderate-high. Child removal, family destruction, poverty, suicides, **and an explicit ethnic-profiling dimension** (dual nationality used as a risk flag). Handleable, but **it is a racism story** and the regulator's distinction must be stated exactly: the Dutch DPA found the methods *"discriminatory"* with *"permanent and structural unnecessary negative attention for nationality and dual citizenship"*, while concluding there was **no ethnic profiling in the strict GDPR sense because nationality data is not race data.** **State that accurately or the film is wrong in a way critics will catch.**

**Saturation — effectively ZERO in English.** Largest English item >20 min: a 54-min Dutch-channel interview (*De Nieuwe Wereld*, **11,065 views**). **No BBC/Netflix/major-channel English documentary found. Green flag.**

**US-context cost — 45–60s, and this is the most transplantable European case.** *"The Dutch government pays parents to help with daycare. The tax office decides who's cheating."* That is it. Americans understand the IRS clawing back a credit and CPS taking kids.

**⚠⚠ MECHANISM — THE ALGORITHM FRAMING IS FORMALLY DROPPED (§4.2).** An independent researcher's verdict, unprompted: *"Structurally this is Horizon with a tax office instead of a post office. Running it as the next-but-one episode would read as a rerun."*
**The candidate survives on exactly one spine: the children.** *"Horizon took people's livelihoods, savings, liberty and reputations. The toeslagenaffaire did all that and then took their kids — 2,090 removals, most never reversed."* Open on a child removal and make the repayment machinery the *backstory*. That is **M3**, a lane with zero prior episodes. **Without that spine, do not make it.**

---

#### EU2. Norway — the NAV scandal (trygdeskandalen) · **⚠ no carrier** · **UN-DROPPED THIS PASS**
**Premise.** Norway jailed its own citizens for benefit fraud for taking trips inside Europe — conduct that EEA law had made legal since 1994.

**Carrier — ⚠ THE BLOCKING PROBLEM.** The legal record **anonymises**: the 2021 Supreme Court pilot case concerns a man called only **"A"**, who **served an actual prison sentence** and was then acquitted by a unanimous grand chamber; his case unlocked ~60 others held in abeyance. Named carriers exist in Norwegian press but none was verified. **Per §0.1 and R-22 this candidate has no protagonist at all, which is independently disqualifying until fixed.**

**Stakes gap.** A holiday inside the EEA → **at least 80 wrongly convicted**, **at least 2,400** hit with unlawful repayment demands (Jan 2020 figures); error running back to **1994**; pre-2012 cases still uncounted.

**Institution + consequence.** NAV, plus the courts, the prosecution and Parliament — all of which missed it. Benefits director **Kjersti Monland** stepped down Dec 2019; NAV chief **Sigrun Vågeng** left early Aug 2020; Labour Minister **Anniken Hauglie** resigned Jan 2020. **No one prosecuted.**

**QUOTE — [V-PRIMARY]. A supreme court convicting itself — arguably the strongest single quote in the entire pool.**
> «I dette tilfellet må det erkjennes at de rettsikkerhetsgarantiene som skulle sikres ved domstolsbehandlingen av As sak, ikke fungerte godt nok når feilen i lovanvendelsen ikke ble fanget opp, heller ikke ved Høyesteretts behandling av saken i 2017.»
> **[translation]** *"In this case it must be acknowledged that the rule-of-law safeguards that were to be secured by the courts' handling of A's case did not function well enough, given that the error in the application of the law was not caught — not even in the Supreme Court's own handling of the case in 2017."*
> — Norwegian Supreme Court, grand chamber, **HR-2021-1453-S, 2 July 2021**, first-voting Justice **Kine Steinsvik**. `https://www.rett24.no/articles/enstemmig-storkammer-nav-feil-siden-1994`
> Also verified: the commission report **NOU 2020:9 "Blindsonen"**, 4 Aug 2020, found *"systemic failure in the processing of rules and individual cases."*

**Living / legal.** All alive; convictions quashed. **Low risk. R2.**

**Present tense.** Pre-2012 criminal cases and repayment demands have **still never been systematically reviewed**; the Supreme Court's appeals panel closed off further appeals in April 2025; a related report ("Eksport av velferdsytelser") only became public in **April 2026**.

**Holds 20–30?** Marginal without a carrier.

**Ad-safety — VERY LOW.** Bureaucratic wrongful conviction; almost nothing to trip a filter.

**Saturation — ZERO.** No English-language documentary of any length found.

**US-context cost — 90–120s of the expensive kind.** You must explain NAV, that **Norway is not in the EU but is in the EEA**, and that **EEA free-movement law overrides Norwegian statute.** The third is the whole case and is genuinely alien — there is no American analogue for *"a foreign treaty court silently legalised what our courts were jailing people for."* Survivable only by making the absurdity concrete fast: *"she went to Italy for two weeks; they gave her prison."*

**⚠ MECHANISM — I REVERSED MY OWN EARLIER CALL, AND I AM FLAGGING IT RATHER THAN HIDING IT.** My first pass **dropped NAV as an EP56 duplicate.** The dedicated European researcher argued the opposite, and persuasively: *"No software error, no faulty evidence, no cover-up in the Horizon sense. The state's reading of the law was wrong, and everyone — NAV, prosecutors, defence lawyers, trial courts and the Supreme Court itself — failed to notice for 25 years. Nobody hid anything; the whole legal system was simply, collectively, unanimously wrong. That is a distinct and arguably more disturbing idea: not villainy, but institutional blindness."*
**Revised verdict: MECHANISM CLEARED, schedule-safe near EP56. The blockers are the missing carrier and the 90–120s EEA tax, not duplication.**

---

#### EU3. Mediator / benfluorex (France) · **ORD** · ★
**Premise.** A French drug company sold a diabetes pill as a diet aid for 33 years while knowing it wrecked heart valves, and the state's own drug regulator let it happen.

**Carrier — ordinary-citizen, and the IJ/Civil-Rights-Lawyer shape.** **Dr Irène Frachon**, a pulmonologist at Brest university hospital — an outsider who took the institution on. She did not write a report; **she wrote a book with the death toll in the title**, *Mediator 150 mg: combien de morts?* ("Mediator 150 mg: how many deaths?"), published June 2010. **Servier sued to strip the subtitle.** The book broke the case open.

**Stakes gap.** One provincial lung doctor → **5,000,000 people** took the drug; **1,500 to 2,100 dead**; on the market **1976 to 2009** — years after Switzerland, Spain and Italy had pulled it.

**Institution + consequence — one of only two candidates in the pool with a real punished villain.** **Laboratoires Servier** and the state agency **ANSM/AFSSAPS**. **2021:** Servier fined **€2.7m** for aggravated deception and involuntary manslaughter (acquitted of fraud); ANSM fined ~€303,000; former no. 2 **Jean-Philippe Seta** got **4 years suspended**. **On appeal, December 2023:** fine raised to **€8.75m**, an *escroquerie* conviction added, and Servier ordered to repay **€415m** to the social security and mutual insurers. Victims received ~€180m. **Nobody went to prison.**

**QUOTE — [V-PRIMARY, via archive; corroborated across seven outlets].**
> « Malgré la connaissance qu'ils avaient des risques encourus depuis de très nombreuses années, (…) ils n'ont jamais pris les mesures qui s'imposaient »
> **[translation]** *"Despite the knowledge they had of the risks incurred, over very many years, (…) they never took the measures that were required."*
> — presiding judge **Sylvie Daunis**, Paris *tribunal correctionnel*, **29 March 2021**. `https://web.archive.org/web/20210329085012/https://www.lemonde.fr/societe/article/2021/03/29/scandale-du-mediator-les-laboratoires-servier-condamnes-a-2-7-millions-d-euros-d-amende_6074840_3224.html` *(wording independently corroborated across Les Echos, TV5Monde, franceinfo, Libération, Le Soir, La Dépêche and Sciences et Avenir).* Le Monde also notes the trial ran **over 517 hours**.

**Living / legal.** Frachon alive and cooperative with media. **Jacques Servier died in 2014 before judgment — a huge dramatic fact.** Servier the company is alive, rich, and has litigated against journalists — **quote only the judgments. R1/R2.**

**Present tense.** Victim compensation continues to trickle; the €415m repayment and appeals machinery grind on; **the revolving door between Servier and French drug regulation was never structurally fixed.**

**Holds 20–30?** Yes.

**Ad-safety — LOW, and among the most monetisable in the pool.** Corporate malfeasance and pharma. Note that *"pharma company hid deaths"* can occasionally trip medical-misinformation heuristics — **stick tightly to the court findings.**

**Saturation — ZERO English-language documentary >20 min found.** There is a 2016 French feature film (*La Fille de Brest*) about Frachon, **which proves the story is dramatically strong and confirms nobody has done it for an English audience. Green flag.**

**US-context cost — ~30s. THE CHEAPEST NON-US CASE IN THE POOL AFTER AS2 AND AS4.** *"France's FDA"* is a one-line explanation. Americans have Vioxx, opioids and Purdue.

---

#### EU4. Greenland / Denmark — the IUD campaign (spiralkampagnen) · **ORD**
**Premise.** Danish doctors fitted IUDs into thousands of Inuit women and schoolgirls — some as young as 13 — without consent, to halt Greenland's birth rate.

**Carrier — ordinary-citizen.** **Naja Lyberth** (b. 23 Feb 1962, Maniitsoq), psychologist and spokesperson for the claimant group. From her own account: **the district doctor came into her school classroom** to announce that the girls would be fitted with coils. She was **14**. There was no possibility of refusal, her parents were never informed, she never told them, and the class never spoke of it again. **She first spoke publicly in 2017 — forty years later.**

**Stakes gap.** **One doctor walking into one classroom** → **4,500 girls and women fitted between 1966 and 1975 — roughly half of all fertile women in Greenland.** Youngest recorded: **13.** Claim value: **DKK 300,000 (~US$44,000)** per woman.

**Institution + consequence.** The Danish state. **143 women sued in early 2024** (~DKK 43m), after 67 had tried and been ignored in Oct 2023. Their counsel **Mads Pramming** called it *"danmarkshistoriens største sag mod staten for brud på menneskerettigheder"* — "the largest case in Danish history against the state for breach of human rights." **December 2025:** broad political agreement on compensation. **25 June 2026:** a bill formally introduced. **No individual doctor has ever faced any consequence.**

**QUOTE — [V-PRIMARY], from the ministry's own press release, five weeks old.**
> *"Antikonceptionssagen er et mørkt kapitel i Danmarks og Grønlands historie. […] Vi kan ikke ændre fortiden, og ingen godtgørelse kan fjerne kvindernes og deres familiers smerte. Men med denne lov sætter vi handling bag ordene og viser kvinderne, at vi anerkender og undskylder for den uret, de er blevet udsat for"*
> **[translation]** *"The contraception case is a dark chapter in the history of Denmark and Greenland. […] We cannot change the past, and no compensation can remove the pain of the women and their families. But with this law we put action behind the words and show the women that we acknowledge and apologise for the injustice they have been subjected to."*
> — **Minister for Health and Church Affairs Ida Auken**, official Ministry press release, **25 June 2026**. `https://www.ism.dk/nyheder/2026/juni/lovforslag-skal-sikre-kvinder-godtgoerelse-i-antikonceptionssagen-spiralsagen`
> Also verified — Interior and Health Minister **Sophie Løhde** to KNR: *"det er en dybt ulykkelig sag, som vi skal til bunds i"* — "it is a deeply unfortunate case, which we must get to the bottom of."

**Living / legal.** Lyberth alive and publicly active. Many claimants elderly — **the oldest was 85 as of March 2024**, which is why their lawyer refused to wait for the historical inquiry. **Do not name individual doctors**; the state has accepted institutional responsibility, individuals have not been adjudicated. **R2.**

**Present tense — the strongest live news peg in the European set.**
- The Danish scheme covers only **up to and including 1991**, because Greenland took over its own health service in **1992 — and the practice continued under Greenlandic administration afterwards.**
- Greenland's own compensation window for post-1992 cases **closed 31 December 2025 with 219 applicants.**
- **Danish applications open 1 July 2026 and run to 1 September 2028. The story is live right now.**
- Patienterstatningen is sending **three travelling teams around Greenland** — a jurist-nurse, a Greenlandic psychologist, an interpreter and **a retired judge** — the first in autumn 2026. **That is a filmable, in-progress scene.**

**Holds 20–30?** Yes.

**Ad-safety — HIGH, and it needs deliberate framing.** Non-consensual gynaecological procedures on minors, forced contraception, colonial racism, and a demographic-control policy that shades toward genocide-adjacent language. **To survive: frame it as a state accountability and compensation story — a government apologising and writing cheques — not as a body-horror story.** Lead with the 2026 law, the courtroom and the ministerial apology. Keep procedure description clinical and brief. **Avoid the word "sterilisation" — it is inaccurate anyway; these were IUDs.**

**Saturation — LOW.** Largest English items: **FRANCE 24 English, "Greenland, breaking the silence," 36:04, 72,695 views**; **BBC World Service, "Greenland's lost generation," 26:17, 48,952 views.** Both short-form news documentary. **Nobody has covered the 2026 compensation law.**

**US-context cost — ~45s, and falling.** Normally the Denmark-Greenland colonial relationship would be expensive. **But Greenland has had extraordinary US news salience through 2025–2026 because of American political interest in acquiring it.** You can open on *"You've been hearing a lot about Greenland lately. Here's what Denmark did to it,"* and the context problem largely evaporates. **⚠ That same salience is a political tripwire — the film must not read as commentary on the acquisition question.**

---

#### EU5. Gustl Mollath (Germany) · **A-t-C**
**Premise.** A man told police his wife's bank was smuggling money to Switzerland; the state declared him delusional and locked him in a secure psychiatric hospital for seven and a half years — then the bank's own audit found he was right.

**Carrier.** **Gustl Mollath** (b. 7 Nov 1956, Nuremberg), detained **27 February 2006 to August 2013.** The unrepeatable detail: the psychiatric report used the fact that he kept implicating **more and more people** in his "delusional system" as proof of the delusion — **literally, the more he was disbelieved, the sicker he was deemed.** Meanwhile HypoVereinsbank's own internal special audit (March 2003) concluded, verbatim: *"Alle nachprüfbaren Behauptungen haben sich als zutreffend herausgestellt"* — **"All verifiable claims have turned out to be accurate."**

**Stakes gap.** One letter to a bank's internal audit → **7.5 years** in closed forensic psychiatry; total compensation **€670,000** (€70,000, then €600,000 in a Nov 2019 settlement with the Free State of Bavaria) — roughly **€89,000 per year of his life.**

**Institution + consequence.** The Bavarian judiciary and Justice Minister **Beate Merk**, plus judge **Otto Brixner** and psychiatrist **Klaus Leipziger**. Merk survived; Brixner — who admitted he had **coached the bank manager's handball team in 1980** — faced no consequence. A Landtag inquiry produced no sanctions. **Mollath was retried and acquitted 14 August 2014** (LG Regensburg, 6 KLs 151 Js 4111/13 WA). Germany amended **§63 StGB in 2016** — the one real institutional outcome.

**QUOTE — [V-PRIMARY], with an honest caveat.**
> „Die Finanzbehörden haben gar nicht ermittelt, die Staatsanwaltschaft hat nur einseitig ermittelt, der Generalstaatsanwalt hat gemauert, und die Justizministerin hat vertuscht."
> **[translation]** *"The tax authorities did not investigate at all, the prosecution investigated only one-sidedly, the attorney general stonewalled, and the justice minister covered it up."*
> — **Inge Aures**, SPD member of the Bavarian Landtag's Mollath inquiry committee, plenary debate **17 July 2013**. `https://www.sueddeutsche.de/bayern/fall-mollath-und-die-politik-justizministerin-ohne-rueckendeckung-1.1724186`
> Same article, Florian Streibl (Freie Wähler) on Merk: *"alles, was falsch laufen konnte, ist falsch gelaufen"* — "everything that could go wrong, went wrong."
> **⚠ Caveat, stated plainly: Aures is an opposition legislator on the inquiry committee — an official on the record in parliament, but a partisan one. It is not a judge or a report conclusion.**

**Living / legal — the highest defamation exposure in the European set.** **Mollath is alive**, as are Merk, Brixner, Leipziger and his ex-wife. **His ex-wife was never convicted of anything; a labour court overturned her dismissal; German courts explicitly found no proof she abetted tax evasion. Any implication otherwise is actionable under German law.** Handle via the acquittal, the audit text, and the Landtag record only. **R2.**

**Present tense — none.** Resolved 2014. Whether he was framed to bury the bank story was never established; no official accepted responsibility.

**Holds 20–30?** Yes.

**Ad-safety.** MODERATE. Psychiatric detention and forced medication are sensitive but this is a wrongful-conviction story, not a mental-illness story.

**Saturation — ZERO in English.** Largest found is German: *Der Fall Mollath – Die Story im Ersten*, 43:51, **32,250 views**; a 21:32 German piece at 38,557. **Strong green flag.**

**US-context cost — 60–75s.** You must explain **§63 forensic commitment**: not prison, not a hospital you can leave, indefinite, reviewed by the same system that put you there. But *"they said he was crazy and locked him up so nobody would check the bank"* is grasped instantly — *One Flew Over the Cuckoo's Nest* meets a whistleblower.

**⚠ Adjacency.** *"They put a sane man in a psychiatric institution"* is adjacent to **EP57 Hemme**'s psychiatric-hospital interrogation, though the machines differ. **Not a duplicate; do not schedule near it.**

---

#### EU6. Spain — the stolen babies (niños robados) · **ORD**
**Premise.** For fifty years Spanish doctors, nuns and clinics took newborns from their mothers, told them the baby had died, and handed the child to someone else.

**Carrier — ordinary-citizen.** **Inés Madrigal**, handed over on **6 June 1969**. The court's own findings supply an extraordinary detail: Dr Vela first offered her adoptive mother **a different baby**, instructing her to **fake a pregnancy by stuffing a cushion under her clothes** and simulate morning sickness in front of neighbours — an offer she refused. Weeks later Vela summoned the couple, told them he had a **"regalo"** (a gift) for them, and told them to bring newborn clothes.

**Stakes gap.** **One cushion under a dress** → estimates of **30,000+** children taken into state tutelage 1944–1954 alone (Judge Baltasar Garzón's 2008 filing); thousands of complaints since 2011; **exactly one case has ever reached trial, and it produced zero punishment.**

**Institution + consequence.** **Dr Eduardo Vela Vela** (b. 20 Oct 1932), gynaecologist and medical director of the San Ramón clinic in Madrid 1961–1981. **The prosecution asked for 11 years. He was acquitted — and died before any retrial. Nobody has ever been punished.**

**QUOTE — [V-PRIMARY★] (judgment PDF downloaded and text-extracted).**
> *"no obstante ser de signo absolutorio la presente sentencia, ello lo es por la operatividad del instituto de la prescripción, conteniendo no obstante, en el relato fáctico, la descripción de los hechos relativos a la aportación de datos falsos al Registro en virtud de la falsa certificación emitida por el acusado"*
> **[translation]** *"although the present judgment is one of acquittal, it is so by the operation of the statute of limitations, containing nonetheless, in the statement of facts, the description of the acts relating to the entry of false data in the Register by virtue of the false certification issued by the accused."*
> — **Audiencia Provincial de Madrid, Sección 7ª, Sentencia nº 640/2018, 27 September 2018.** `https://e01-elmundo.uecdn.es/documentos/2018/10/08/bebes_robados.pdf`
> The court also found — verbatim — that Vela certified **in his own handwriting** that he had confirmed the birth through *"su asistencia personal al parto"* ("his personal attendance at the birth") **of a birth that never occurred.**

**Living / legal.** Madrigal alive and a public campaigner. Vela dead. **Church and religious orders are implicated and are litigious — attribute only to court findings. R1/R2.**

**Present tense.** The prescription doctrine still blocks essentially every case; thousands of victims have no legal route; **there is still no comprehensive national DNA database reuniting families.**

**Holds 20–30?** Yes.

**Ad-safety.** MODERATE. Infant trafficking, the Catholic Church, dead-baby deception. The court record does the heavy lifting.

**Saturation — MODERATE, the second-highest in the European set.** DW Documentary, *The stolen babies scandal in Spain*, 42:26, **492,601 views**; 60 Minutes, *Stolen Babies*, 1:07:52, **529,581 views**. **The topic is known; the Vela judgment as a document is not — that is the differentiator.**

**US-context cost — ~60s.** Franco is a dictator most 55+ US men have heard of; *"Catholic hospitals ran the maternity wards"* needs no explanation.

---

#### EU7. Iceland — Guðmundur and Geirfinnur · **CSE** · ⚠ heavily saturated
**Premise.** Iceland convicted six young people of two murders with no bodies, no witnesses and no forensic evidence — using confessions manufactured by years of solitary confinement.

**Carrier — the losing archetype.** **Erla Bolladóttir**, held in solitary for **239 days** (Icelandic Supreme Court record; English sources say 242). She named her own **half-brother, Einar Bollason**, chairman of the Icelandic Basketball Federation, who then sat **105 days in solitary** for a crime that never happened, alongside three other innocent men. **She is the only one of the six never exonerated.**

**Stakes gap.** Zero bodies, zero forensic evidence → six convicted; **Tryggvi Rúnar Leifsson held 655 days in solitary** — the longest documented outside Guantánamo; **ISK 815 million (~€6m)** paid in compensation Jan 2020; Erla received ~**€210,000** and a formal apology in December 2022 **while her conviction stood.**

**Institution + consequence.** Reykjavík police and the Síðumúli prison interrogators, assisted by a German BKA investigator. **No officer was ever prosecuted.** Germany refused a 2019 request to compensate or to reclaim the Icelandic medals awarded for the "solved" case. Síðumúli prison was eventually closed.

**QUOTE — [V-PRIMARY], and it says something better than "they were exonerated".**
> *"Af hálfu ákæruvaldsins er þess krafist að dómfelldu verði sýknaðir af þeim sakargiftum, sem þeir voru sakfelldir fyrir í áðurnefndu hæstaréttarmáli og endurupptaka málsins tekur til. Leiðir af lögum að dómfelldu verða þegar á grundvelli kröfugerðar ákæruvaldsins sýknaðir af þessum sakargiftum"*
> **[translation]** *"On the part of the prosecution it is demanded that the convicted persons be acquitted… It follows from law that the convicted persons shall be acquitted of these charges **already on the basis of the prosecution's own demand**."*
> — Hæstiréttur Íslands, **Mál nr. 521/2017, 27 September 2018.** `https://web.archive.org/web/20190513050927/https://www.haestirettur.is/domar/domur/?id=34b0664d-10ee-4f6d-917e-67ed04c3bc5c`
> **Read what that actually says: the Supreme Court never examined the confessions. The state asked it to acquit, so it acquitted. The court has still never ruled that the interrogations were unlawful.**

**Living / legal.** Erla, Guðjón Skarphéðinsson and Albert Klahn Skaftason alive. Sævar Ciesielski d. 2011, Tryggvi Rúnar d. 2009, Kristján Viðar d. 2021. **Erla's perjury/false-accusation conviction has never been overturned.** A direct search of the ECHR's HUDOC database for "Bolladottir" returned **zero published results** — no ECHR judgment exists as of now. Her post-2022 status is **open**. **R2 — and note she is technically a living convicted person, though the state has apologised and paid her for the detention that produced the conviction; put that distinction to the owner if ever promoted.**

**Present tense.** Her conviction. The bodies. Whether anyone was ever murdered at all. **And the fact that the state paid her while refusing to clear her.**

**Holds 20–30?** Yes.

**Ad-safety.** LOW-MODERATE.

**Saturation — SEVERE, the worst in the pool.** ***Out of Thin Air*** (2017) is on Netflix/BBC and covers the case end to end. On YouTube: **BuzzFeed Unsolved, "The Suspicious Case of the Reykjavik Confessions," 21:12, 10,956,406 views.** BBC Radio 4's *The Reykjavik Confessions* is widely known. **An English-speaking true-crime audience has already been served this story twice.**
**Verdict:** the Erla angle *is* a genuine fresh spine, and *Out of Thin Air* centres her sympathetically without resolving her legal status. **But you would be competing, not discovering. Only worth it if you can get Erla on camera.**

**US-context cost — 30–45s.** 1970s Iceland is exotic in an appealing way and needs no institutional explanation. **Cheapest in the European set — which is exactly why everyone has already made it.**

---

#### EU8. Enzo Tortora (Italy) · **A-t-C**
**Premise.** Italy's most famous television host was arrested at 4am on the word of mafia informants trading testimony for sentence reductions, paraded in handcuffs for the cameras, given ten years, cleared entirely — and dead of cancer within two years.

**Carrier.** **Enzo Tortora.** The "objective evidence" was an address book seized from camorrista Giuseppe Puca containing a handwritten name that looked like *Tortora*; handwriting analysis eventually established the name was **"Tortona"** — and the phone number beside it was not his either. Separately, his only actual contact with accuser Giovanni Pandico was that Pandico had mailed **hand-crocheted doilies** from prison to Tortora's TV show *Portobello* to be auctioned; the production lost them, and Tortora wrote a **polite letter of apology.** **That letter became evidence of a relationship with the Camorra.**

**Stakes gap.** A misread name → **7 months in prison**, house arrest from 18 Jan 1984, a **10-year sentence** on 17 Sept 1985, **19 pentiti** testifying against him, full acquittal 15 Sept 1986, Cassation 1987, **dead 18 May 1988.** He was arrested alongside **855** alleged camorristi in one night.

**Institution + consequence.** Naples prosecutors **Lucio Di Pietro** and **Felice Di Persia**, investigating judge **Giorgio Fontana**, and the pentiti **Giovanni Pandico**, **Pasquale Barra** and **Giovanni Melluso**. **No criminal charge, no disciplinary proceeding, no investigation was ever opened against any magistrate. They all continued their careers.** The case triggered the Nov 1987 referendum on judicial civil liability — **80.2% voted to strip magistrates' immunity** — which Parliament then defanged via the April 1988 "Vassalli law", routing liability to the state and capping a magistrate's exposure at one-third of one year's salary, with no retroactivity.

**QUOTE — [NONE VERIFIED].** The strongest candidate, **flagged as NOT independently verified**, is Naples prosecutor **Cedrangolo**, asked whether he was certain the informants were telling the truth (La Stampa, 18 June 1983, as cited on it.wikipedia — the Wikipedia source text was read, not the La Stampa original): « Non abbiamo l'abitudine di emettere ordini di cattura senza motivo » — *"We are not in the habit of issuing arrest warrants without reason."* A second unverified fragment attributed to the Naples appeal court's written reasons (deposited 17 Dec 1986) holds that the informants' statements were made *"al solo scopo di ottenere uno sconto di pena"*. **Do not put either on screen until someone pulls the La Stampa archive and the 1986 judgment.**

**Living / legal.** Tortora died 1988; most principals dead. **Lowest defamation risk in the European set — but the Camorra is a real organisation and living relatives of the pentiti exist. R1.**

**Present tense — none.** **No magistrate has ever been held responsible.** The Vassalli law remains the framework, and the pentito system that destroyed him is still the backbone of Italian anti-mafia prosecution.

**Holds 20–30?** Yes.

**Ad-safety.** LOW-MODERATE.

**Saturation — ZERO in English.** No English documentary >20 min found on Tortora specifically.

**US-context cost — 90–120s, the most expensive in the European set.** You must explain (1) what a *pentito* is and why Italy let convicted killers buy sentence reductions with testimony; (2) the Camorra as distinct from the Sicilian Mafia; (3) why a TV host mattered enough that his arrest was national trauma — **1980s Italian television has no US referent, and "he was the Johnny Carson of Italy" then requires the audience to care about a foreign Johnny Carson.** Borderline. If built, spend the first 90 seconds on the 4am arrest and the handcuffs in front of the cameras, and back-fill the institutions later.

---

#### EU9. Outreau (France) · **A-t-C** · ⚠ DO NOT BUILD AS A FLAGSHIP
**Premise.** France put 17 people on trial for a child sex ring that mostly did not exist, jailed them for years on the word of one lying woman and coached children, and one of them died in his cell.

**Carrier.** **François Mourmand.** Died in pre-trial detention **9 June 2002, aged 32**, of an undetermined drug overdose, still awaiting a trial that would have cleared him. **At the end of the appeal trial the defence lawyers declined to make closing arguments and asked the court for a minute of silence for him instead.**

**Stakes gap.** One woman's fabricated accusations → **17 tried, 13 acquitted, one dead in a cell**; years of pre-trial detention; compensation claims up to **€1 million each**.

**Institution + consequence.** Investigating magistrate **Fabrice Burgaud**, in post barely a year, plus prosecutor Gérald Lesigne and the psychological experts. In April 2009 the Conseil supérieur de la magistrature sanctioned Burgaud with — **a "réprimande avec inscription au dossier"**, a reprimand noted in his file. Nothing more. André Vallini called it *"presque de la provocation."*

**QUOTE — [V-PRIMARY].**
> « Au nom de la justice dont je suis le garant, je tiens à vous présenter regrets et excuses devant ce qui restera comme un désastre judiciaire sans précédent »
> **[translation]** *"In the name of the justice of which I am the guarantor, I wish to offer you my regrets and apologies for what will remain an unprecedented judicial disaster."*
> — President **Jacques Chirac**, personal letter to each of the thirteen acquitted, **December 2005**. `https://www.ina.fr/ina-eclaire-actu/outreau-justice-fiasco-pedophilie-acquittement-justice`. Each letter closed in Chirac's own handwriting: « Avec tout mon soutien et de tout cœur à vos côtés ».

**Living / legal.** Burgaud alive and never criminally charged — **name him only via the CSM decision and the parliamentary record.** **⚠ CRITICAL ACCURACY POINT: this is NOT a case where nothing happened. Four people were definitively convicted and twelve children were legally recognised as victims and compensated. Real abuse occurred inside the Delay–Badaoui household.** The scandal is the catastrophic over-extension beyond it. **Getting this wrong would be both defamatory and morally indefensible. R1/R2.**

**Present tense — none.** The *juge d'instruction* system survived essentially intact despite the 2006 commission's 80 recommendations.

**Holds 20–30?** Yes.

**Ad-safety — THE WORST IN THE POOL, alongside UK7.** The subject matter is child sexual abuse, including of named real children. **Even a scrupulous treatment sits in YouTube's most aggressively demonetised category. Do not build a channel-critical episode on this.**

**Saturation.** **No English documentary >20 min found.** Heavy French coverage (*Faites entrer l'accusé* on Myriam Badaoui: 2.3M views, French). **The English gap is real — but ad-safety, not saturation, is the binding constraint.**

**US-context cost — ~90s, and it is a gift rather than a tax.** The *juge d'instruction* — a single magistrate who both investigates and builds the case, with no adversarial counterweight, who can hold you for years without trial — lands as *"one guy is cop, prosecutor and grand jury at once, and he can lock you up for three years while he thinks about it."* US viewers find that horrifying and comprehensible.

---

#### EU10. Peter Ellis / Christchurch Civic Creche (NZ) · **A-t-C**
**Premise.** A male childcare worker was convicted in the moral panic of the early 1990s on children's accounts elicited by repeated interviewing — and in 2022, three years after he died still fighting them, New Zealand's Supreme Court quashed his convictions in the country's first posthumous appeal.

**Carrier.** **Peter Ellis** (d. 2019), posthumously.

**Stakes gap.** NZ's **first posthumous appeal**; convictions quashed **2022**, **3 years** after he died.

**Institution + consequence.** New Zealand police and prosecution, and the interviewing practices of the period. **No individual consequence identified.**

**QUOTE — [NONE VERIFIED].** The Supreme Court's 2022 judgment is the correct source.

**Living / legal.** Ellis deceased (**R1** for the protagonist) — **but the complainants are living adults who were children at the time, some of whom maintain their accounts. The film cannot call them liars and must not.**

**Present tense — none.** Closed 2022.

**Holds 20–30?** Marginal.

**Ad-safety — SEVERE.** Child sexual abuse allegations throughout.

**Saturation.** UNVERIFIED.

**US-context cost — 50–65s.** Low; the US has McMartin and its own satanic-panic canon — **which is both the bridge and the reason a US viewer may prefer the American version.**

**⚠ Mechanism — same machine as EU9. ONE ONLY.**

---

### 3.5 MASS-SCALE / SYSTEMIC — lane (b)

*Six of these eight are US, which under §0.4 means **zero foreign-institution setup**. That is now a major structural advantage and it is why three of them enter my top 8.*

---

#### SY1. The FBI's microscopic hair comparison review · **A-t-C**
**Premise.** For over two decades the FBI's hair examiners testified to a certainty the science never supported — and the Bureau's own audit found they did it in nearly every trial it checked.

**Carrier.** **Santae Tribble**, convicted at 17 for a 1978 Washington DC murder. When the 13 hairs from the stocking mask were finally DNA-tested in 2012, not one was his — **and one of them was a dog's.** The FBI examiner had called it human. Tribble served 28 years.

**Stakes gap.** **1 dog hair** → **257 of 268 trials (96%)** contained erroneous FBI testimony; **26 of 28** examiners implicated; ~3,000 cases in scope.

**Institution + consequence.** FBI Laboratory hair and fibre unit / DOJ. **No examiner was criminally charged. The FBI's response was to stop making the statements.**

**QUOTE — [V-PRIMARY].**
> *"In the 268 cases where examiners provided testimony used to inculpate a defendant at trial, erroneous statements were made in 257 (96 percent) of the cases."*
> and *"Defendants in at least 35 of these cases received the death penalty and errors were identified in 33 (94 percent) of those cases."*
> — **FBI/DOJ joint press release, 20 April 2015.** `https://www.fbi.gov/news/press-releases/fbi-testimony-on-microscopic-hair-analysis-contained-errors-in-at-least-90-percent-of-cases-in-ongoing-review` *(fbi.gov 403s to direct fetch; read via the `r.jina.ai` proxy.)*
> **Peter Neufeld**, Innocence Project co-founder, same release: *"These findings confirm that FBI microscopic hair analysts committed widespread, systematic error, grossly exaggerating the significance of their data under oath."*
> **⚠ CORRECTION 1 (§0.6): it is 35 capital defendants with errors in 33, NOT 32. Nine had already been executed; five died on death row. Do not ship "32".**

**Living / legal.** Tribble died in 2020 *(not independently verified — check before use)*. The review's state-and-local tier is still incomplete. **R1/R2.**

**Present tense.** **Thousands of state-lab cases trained by the FBI's method have never been reviewed at all, and no national mechanism exists to notify those defendants.**

**Holds 20–30?** Yes.

**Ad-safety.** LOW. Murder discussed abstractly.

**Saturation.** **UNVERIFIED** — YouTube's results page is not fetchable. No major broadcast documentary surfaced in news indexes.

**US-context cost — n/a.**

**⚠ This is the purest "institution indicts itself" asset in the pool** — exactly the R-38 shape — and the only thing that kept it out of my top 8 is the accused-then-cleared protagonist.

---

#### SY2. Annie Dookhan and Sonja Farak (Massachusetts) · **A-t-C** · ⚠ Netflix owns it
**Premise.** Two chemists in two Massachusetts labs — one faking results to look productive, one high on the evidence — triggered the largest mass dismissal of criminal convictions in American history.

**Carrier — ⚠ NOT FULLY VERIFIED.** The strongest is not a defendant but the case that broke it open: **Rolando Penate**, convicted on Farak's evidence, whose lawyer's dogged subpoena for Farak's mental-health records is what the Attorney General's office concealed. **Needs one more check before a cold open is built on him.**

**Stakes gap.** 1 chemist's handwriting → **21,587 convictions vacated in a single day** (Dookhan, April 2017), plus roughly **8,000 more** (Farak, October 2018). **Over 30,000 total.**

**Institution + consequence.** Dookhan — 3–5 years, paroled by 2016. **And the prosecutors:** the Massachusetts Attorney General's office concealed exculpatory evidence — **AAG Anne Kaczmarek disbarred**; **AAG Kris Foster suspended one year and a day**; supervisor **John Verner publicly reprimanded** — 31 August 2023.

**QUOTE — [V-PRIMARY, cross-checked against CourtListener].**
> *"We are called upon, in the exercise of our broad powers of superintendence over the courts of the Commonwealth, to remedy egregious governmental misconduct arising out of the scandal at the State Laboratory Institute in Amherst at the campus of the University of Massachusetts."*
> — Massachusetts Supreme Judicial Court, **opening line**, *Committee for Public Counsel Services v. Attorney General*, 480 Mass. 700, **11 October 2018**. `https://law.justia.com/cases/massachusetts/supreme-court/2018/sjc-12471.html`
> From *In the Matter of Foster* (SJC, 31 Aug 2023): Kaczmarek bore *"the greatest culpability"* and showed *"a lack of candor and remorse"*; Foster's conduct was *"gross incompetence"* and *"reckless lawyering."* `https://www.courtlistener.com/opinion/9423788/in-the-matter-of-foster/`

**Living / legal.** Dookhan, Farak, Kaczmarek, Foster, Verner all living; all discipline final. **R1/R2.**

**Present tense — weak.** Collateral consequences — deportations, lost housing, lost custody — were never unwound for most of the 30,000.

**Holds 20–30?** Yes.

**Ad-safety.** MODERATE. Drug offences throughout; Farak's addiction narrative.

**Saturation — HIGH, and this is the problem.** **Netflix's four-part *How to Fix a Drug Scandal* (1 April 2020) covers both chemists.** **Recommend skipping unless a genuinely unclaimed angle emerges — the prosecutors' 2023 discipline is the only candidate.**

**US-context cost — n/a.**

---

#### SY3. Sgt. Ronald Watts (Chicago) · **A-t-C, ORD-shaped** · **[LOSS-VERB]** · ★
**Premise.** A police sergeant ran a protection racket out of a public housing project for a decade, and the convictions he manufactured are still being erased one courtroom at a time.

**Carrier — and this is the strongest carrier decision in the pool.** **Clarissa Glenn — not her husband.** Ben Baker went to prison; **Clarissa spent the decade outside fighting to get him out, was herself convicted on Watts's perjured evidence, and her persistence is what eventually cracked the case.** The unrepeatable detail: **she and Baker reported the shakedown to the Chicago Police Department's own Office of Professional Standards — which told Watts about the complaint and named them as the source.**

**Stakes gap.** A **$1,000** bribe demand → **212 convictions vacated** (reported May 2022; growth since unverified).

**Institution + consequence.** Sgt. **Ronald Watts** pleaded guilty in federal court in 2013 to theft of government funds and served **22 months. He was never charged for a single wrongful conviction.** The two officers who reported him, Shannon Spalding and Danny Echeverria, were retaliated against.

**QUOTE — [V-PRIMARY]. The best opening two sentences found in the entire research set.**
> *"When corrupt police officers demanded a bribe from Ben Baker, Baker and his wife, Clarissa Glenn, told the Chicago Police Department Office of Professional Standards (OPS) about the crime. The OPS did nothing to slow down the criminals. Instead, it informed the corrupt officers about the complaint, and named the source."*
> — Appellate Court of Illinois, **opening of *People v. Glenn*, 2018 IL App (1st) 161331, 5 June 2018.** `https://www.courtlistener.com/opinion/4530129/people-v-glenn/`
> **A court, in its first two sentences, describing an internal-affairs body handing a whistleblower's name to the man she reported.**

**Living / legal.** Watts, Baker and Glenn all living; Watts released; civil suits ongoing. **R1/R2.**

**Present tense.** **Watts has never faced consequence for the framings themselves; petitions were still being filed as of 2025.**

**Holds 20–30?** Yes.

**Ad-safety.** MODERATE-HIGH. Police corruption, drugs, race. **Demonetisation risk sits in the thumbnail/title choices, not the content.**

**Saturation — UNVERIFIED on YouTube, but a *New Yorker* long-read (May 2018) exists and no major documentary surfaced. This looks like the most under-served case in the systemic set.**

**US-context cost — n/a.**

**⚠ Mechanism — grep M7 adjacency.** **EP55 `burge` is already a corrupt Chicago police unit.** Watts is a different machine (a protection racket producing false *drug* convictions, versus torture producing false *confessions*) and a different decade, **but it is the same city and the same institution.** See §5-J: **not adjacent, different packaging, and never lead on "Chicago police."**

---

#### SY4. Massachusetts breathalyzer / *Commonwealth v. Ananias* · **⚠ no carrier**
**Premise.** The state lab that certified every breathalyzer in Massachusetts hid the machines' failed calibration tests from the defence — for years.

**Carrier — ⚠ NONE VERIFIED. A real structural weakness; know it before committing.**

**Stakes gap.** **432 hidden worksheets** → approximately **27,000 defendants** notified their OUI convictions were tainted.

**Institution + consequence.** State Police **Office of Alcohol Testing**. The SJC granted affected defendants a conclusive presumption of misconduct. **⚠ It could NOT be verified this pass that director Melissa O'Meara was fired, nor the Ernst & Young audit — do not assert either.**

**QUOTE — [V-PRIMARY].**
> *"OAT intentionally withheld an additional 432 worksheets that reported failures in the annual calibration process; OAT did not inform the prosecutors, the defense attorneys, or the judge that it was withholding the 432 worksheets; and the withheld failed worksheets were exculpatory."*
> — Justice **Frank Gaziano**, Massachusetts SJC, *Commonwealth v. Hallinan*, **26 April 2023.** `https://www.courtlistener.com/opinion/9394291/commonwealth-v-hallinan/`
> The remedy language is also strong: affected defendants receive *"a conclusive presumption of egregious government misconduct."*

**Living / legal.** All living; litigation concluded 2023. **R1/R2.**

**Present tense.** **Most of the 27,000 never moved to withdraw their pleas. The convictions stand by default.**

**Holds 20–30?** Marginal.

**Ad-safety — LOW, but note the sympathy problem: a 55+ US male audience may not extend sympathy to convicted drunk drivers. This is the weakest emotional case in the pool.**

**Saturation.** UNVERIFIED; no documentary found. **US-context cost — n/a.**

---

#### SY5. Joyce Gilchrist (Oklahoma City) · **CSE→A-t-C**
**Premise.** An Oklahoma City police chemist nicknamed "Black Magic" could find what no one else could see — and juries sent people to death row on it.

**Carrier.** **Curtis McCarty**, three times sentenced to death. The unrepeatable detail: in 1983 Gilchrist wrote that the crime-scene hairs were **not** similar to McCarty's. **In 1985, before his arrest, she covertly went back and changed her own notes to reverse the finding.** When the hairs were demanded for DNA testing in 2000, she said they were lost or destroyed. **They have never been found.**

**Stakes gap.** One altered handwritten note → **~3,000 cases** over 21 years; **23 people sentenced to death** in cases she touched, of whom **12 have been executed.** *(The 23/12 figure is reported, not primary-verified — attribute it, do not state it flat.)*

**Institution + consequence.** Oklahoma City Police Department crime lab. Gilchrist fired September 2001. **Never criminally charged.** Died 14 June 2015.

**QUOTE — [V-PRIMARY]. Note the verb.**
> *"Ms. Gilchrist thus provided the jury with evidence implicating Mr. Mitchell in the sexual assault of the victim which she knew was rendered false and misleading by evidence withheld from the defense."*
> — United States Court of Appeals for the Tenth Circuit, *Mitchell v. Gibson*, **13 August 2001.** `https://www.courtlistener.com/opinion/161451/mitchell-v-gibson/`
> **A federal appeals court finding knowledge, not error.**

**Living / legal.** Gilchrist dead (2015). McCarty living, exonerated 11 May 2007 after 22 years. **R1.**

**Present tense.** **The 12 executions cannot be reviewed. Oklahoma has never audited her full caseload.**

**Holds 20–30?** Yes.

**Ad-safety — HIGH.** Sexual assault and child-victim details are close to the surface in several of her cases; the death penalty is a demonetisation trigger. **Script around the forensic fraud, not the underlying crimes.**

**Saturation.** UNVERIFIED; no major documentary surfaced. **US-context cost — n/a.**

---

#### SY6. Fred Zain (West Virginia / Texas) · **A-t-C** · ★ cleanest evidence in the pool
**Premise.** A West Virginia state police serologist invented results for a decade, and the state's own Supreme Court declared every word he ever said in a courtroom worthless.

**Carrier.** **Glen Woodall**, whose conviction Zain's evidence secured and who received a **$1 million** settlement in 1992 — the thread that unravelled everything. *(Alternative: **Jimmie Gardner**, 25+ years in prison, settled for $175,000 in 2019.)*

**Stakes gap.** 1 analyst → up to **134 West Virginia convictions** and up to **180 in Texas**; **$6.5 million** in WV settlements.

**Institution + consequence.** WV State Police Crime Laboratory, Serology Division. **Zain was charged with fraud but a jury deadlocked in 2001; he died of liver cancer on 2 December 2002 without ever standing trial.**

**QUOTE — [V-PRIMARY★] (character-exact, extracted from the court's own PDF).**
> *"The matters brought before this Court by Judge Holliday are shocking and represent egregious violations of the right of a defendant to a fair trial. They stain our judicial system and mock the ideal of justice under law."*
> and immediately following: *"This corruption of our legal system would not have occurred had there been adequate controls and procedures in the Serology Division."*
> — Justice **Miller**, Supreme Court of Appeals of West Virginia, *In the Matter of an Investigation of the West Virginia State Police Crime Laboratory, Serology Division*, No. 21973, **10 November 1993.** `https://www.courtswv.gov/sites/default/pubfilesmnt/2023-11/21973.pdf`
> The operative holding, also exact: *"It is believed that, as a matter of law, any testimonial or documentary evidence offered by Zain at any time in any criminal prosecution should be deemed invalid, unreliable, and inadmissible…"*
> **And the eleven-item list of his acts of misconduct — including *"reporting the results of tests that were never conducted"* and *"reporting scientifically impossible or improbable results"* — is verbatim in the opinion and is already a screen sequence.**

**Living / legal.** **Zain dead. No living-person legal risk. R1 — the cleanest risk profile in the entire pool.**

**Present tense.** A 2006 renewed investigation found the problems extended beyond Zain to the whole division. **WV has never completed notification.**

**Holds 20–30?** Yes.

**Ad-safety.** LOW-MODERATE. Rape/murder cases underlie it; handle at the forensic level.

**Saturation — UNVERIFIED, and no documentary found. Combined with the quality of the primary text, this is the strongest available pick in the systemic set on evidence alone.**

**US-context cost — n/a.**

---

#### SY7. Life Esidimeni (South Africa) · **ORD**
**Premise.** A South African province cancelled the contract that housed its psychiatric patients, scattered them to unlicensed NGOs to save money, and 144 of them died.

**Carrier — ordinary-citizen.** **Christine Nxumalo**, whose sister **Virginia Machpelah** (b. 8 January 1966) died on 15 August 2016 in Atteridgeville. The unrepeatable detail, verbatim from the award at **¶[107]**: Virginia's body was moved between funeral parlours **without the family's consent or knowledge**, and Christine **could only get her sister's body released by pretending she was considering using that parlour for the funeral.** Some bodies at that parlour were being stored in **a disused butchery.**
**And the third act is handed to you:** when Judge Teffo delivered the inquest finding in 2024, **Virginia Machpelah is one of only nine named deceased** whose deaths were found to have been negligently caused. **The carrier's sister is named in the operative legal finding.**

**Stakes gap.** A contract cancelled to save money → **144 dead**, **1,418 survivors exposed to trauma**, **44 patients whose whereabouts remain unknown.**

**Institution + consequence.** Gauteng Department of Health; MEC **Qedani Mahlangu** and mental health director **Dr Makgabo Manamela**. Compensation ordered: **R20,000 funeral + R180,000 shock and trauma + R1,000,000 constitutional damages** per claimant, payable by 19 June 2018.

**QUOTE — [V-PRIMARY★] (character-exact, extracted from the award PDF).**
> *"This is a harrowing account of the death, torture and disappearance of utterly vulnerable mental health care users in the care of an admittedly delinquent provincial government."*
> — Justice **Dikgang Moseneke**, former Deputy Chief Justice of South Africa, Arbitrator, **¶[1]** of the Life Esidimeni Arbitration Award, **19 March 2018.** `https://section27.org.za/wp-content/uploads/2020/10/LifeEsidimeniArbitrationAward.pdf`
> Also exact: *"The death and torture in the Life Esidimeni tragedy stemmed from the irrational and arrogant use of public power."* (¶180) · *"She acted with impunity thinking that she will get away with murder because the users and their families were vulnerable and poorly resourced."* (¶207, on Mahlangu)
> Inquest finding, exact: *"Effectively, Ms Qedani Dorothy Mahlangu and Dr Manamela created circumstances in which the deaths of the deceased were inevitable."* — **Judge M J Teffo**, High Court of South Africa, Gauteng Division, Pretoria, **10 July 2024.** `https://section27.org.za/wp-content/uploads/2024/09/LIFE-ESIDIMENI-INQUEST-JUDGMENT.2024.pdf` (Virginia's cause of death recorded there as *"unascertained, severe malnutrition, dehydration and gangrene were major contributions."*)

**Living / legal.** Mahlangu and Manamela living. The NPA originally **declined to prosecute** all 141 dockets; in August 2025 it emerged it would pursue charges for **only two deaths**; **in April 2026 the NPA announced prosecutions would finally start. Live proceedings — legal review essential before publication. R1/R2.**

**Present tense.** **Nine years on, nobody has been convicted, and the prosecution covers two deaths out of 144.**

**Holds 20–30?** Yes.

**Ad-safety — HIGH.** Starvation, neglect, mental illness, deaths of vulnerable adults. Expect limited monetisation.

**Saturation.** **UNVERIFIED** — no English-language documentary over 20 minutes surfaced.

**US-context cost — 90–120s of pure exposition, and it is front-loaded, which is the worst place for it.** You must explain a provincial MEC (roughly a state health secretary, but appointed not elected); the Gauteng provincial health department; why an *arbitration* rather than a trial produced the finding, and why a retired judge acted as arbitrator; what an inquest is in SA law; and what the NPA is. **Mitigation: open entirely on Christine and the funeral parlour, spend zero seconds on institutions until minute three, and let Moseneke's language teach the viewer what a provincial government is by implication.** Even so, budget the 90 seconds honestly. **This is the highest-friction case in the systemic set for this specific audience — and under §0.4 that penalty just got heavier.**

---

#### SY8. Switzerland — the Verdingkinder ("contract children") · **ORD** · carrier gate
**Premise.** Swiss authorities took more than a hundred thousand children from poor families and placed them with farmers as unpaid labour, a practice that continued into the 1970s.

**Carrier — ⚠ NOT NAMED THIS PASS. Blocking gate.**

**Stakes gap.** **100,000+** children removed, **into the 1970s** — within the lifetime of most of this audience. A **2013 state apology** and a **2016/17 reparations law** followed.

**Institution + consequence.** Swiss cantonal and communal authorities. **Apology and reparations; no prosecutions.**

**QUOTE — [NONE VERIFIED].**

**Living / legal.** Many survivors living and organised. **R1/R2.**

**Present tense.** Partial — the adequacy and reach of the reparations scheme is the live thread. **Unverified.**

**Holds 20–30?** Marginal without a carrier.

**Ad-safety.** MEDIUM-HIGH — child labour and institutional abuse.

**Saturation.** UNVERIFIED.

**US-context cost — 60–80s.** **The single most useful fact for a US audience is the date: this was happening in Switzerland while Americans watched the moon landing.** That framing does most of the work.

**⚠ Mechanism.** M3 cluster (§5-E).

---

## 4. FORMALLY DROPPED — MECHANISM COLLISIONS

### 4.1 ❌ Japan's HIV-tainted blood products (yakugai eizu) — DROPPED as a duplicate of UK1
**What it is.** Japan kept importing unheated American blood concentrate after it knew it carried HIV, infecting **~1,800–2,000 of roughly 5,000 Japanese haemophiliacs; 500–700+ dead.** Carrier: **Ryuhei Kawada**, infected as a haemophiliac child, who **went public under his real name in 1995, aged 19**, when every other victim was anonymous, and later became a national legislator. Aged 26, the day Dr Abe was acquitted: *"We're not simply dying. We're being murdered one by one."*

**Why it is dropped.** It is **the same machine as UK1** — a health system treats haemophiliacs with contaminated blood products, infects them, and conceals it. **Two contaminated-blood films is one too many, and UK1 wins on the measured axes**: a [V-PRIMARY] verbatim cover-up finding from a judge, a live 2026 payment-rate number, an ordinary-citizen carrier, and a US-context cost of 45–60s against Japan's higher scaffolding requirement.

**⚠ But log what Japan has that the UK does not — REAL CONVICTIONS.** **Green Cross** (founded 1950 by **Ryoichi Naito**, an ex-Imperial Army lieutenant-colonel who helped shield Unit 731 members from war-crimes prosecution): Osaka court, 24 Feb 2000 — **Renzo Matsushita** (ex-president, *and formerly head of the Health Ministry's Pharmaceutical Affairs Bureau, the regulator who took over the firm he regulated*) **2 years**; Suyama 18 months; Kawano 16 months. Ministry official **Akihito Matsumura**: conviction for professional negligence causing death **finalised by the Supreme Court 3 March 2008.** **Dr Takeshi Abe acquitted 2001; died 2005 with the appeal pending.** **Cutter Biological (Bayer): never charged anywhere.**
**[V-PRIMARY]** — Tokyo District Court, 28 Sept 2001, convicting Matsumura, as printed by BBC News: *"The accused was responsible for avoiding deaths from Aids by taking measures to ban doctors from using unheated blood products. But the accused neglected the responsibility and continued allowing pharmaceutical firms and doctors to sell and use the products."* `http://news.bbc.co.uk/2/hi/asia-pacific/1568626.stm`
**Best verified framing if it ever returns: *Japan jailed three pharma executives. The United States never charged anyone.***
**⚠ The claim that Japan's plasma came from US paid donors including prisoners is the biggest US hook and the weakest citation — it rests on one Wikipedia-sourced figure (3.14m litres of US plasma imported in 1983). Verify before any use.**

### 4.2 ❌ The Netherlands toeslagenaffaire *told as an algorithm story* — FRAMING DROPPED
See §3-EU1. Told as *"a flawed system wrongly accused innocent people of fraud"* it is **M1 (already run twice — EP36 and EP56) plus M2.** **That framing is dead.** The candidate survives only as a **child-removal** film (M3, zero prior episodes), and only if the 2,090 removals can be anchored to a named mother.

### 4.3 ⚠ REVERSED THIS PASS — Norway's NAV scandal is UN-DROPPED
My first pass dropped NAV as an EP56 duplicate. **The dedicated European researcher argued the opposite and I accept the correction** — see §3-EU2. NAV has **no software error, no faulty evidence and no cover-up**; the state's *reading of the law* was wrong and every institution, including the Supreme Court, missed it for 25 years. **That is institutional blindness, not villainy — a genuinely different film, and schedule-safe near EP56.** Its real blockers are **no carrier** and a **90–120s EEA tax**. Logged here so the reversal is visible rather than silent.

---

## 5. MECHANISM FAMILIES — WHERE THIS POOL COLLIDES WITH ITSELF

**Rule: within each family, only ONE candidate may ever be built.**

| Family | Candidates | Ruling |
|---|---|---|
| **A. A computer/system accuses innocent people** | *EP36 (built)*, *EP56 (built)*, CW1 Robodebt, EU1 Netherlands | **SPENT TWICE.** Robodebt ≥6 episodes from EP56 and only on the March-2026 corrupt-conduct spine. Netherlands only as a child-removal film. **EU2 NAV is cleared out of this family (§4.3).** |
| **B. Mother convicted of killing her babies on flawed expert reasoning** | CW2 Folbigg, *Sally Clark (v002 reject)* | **ONE ONLY.** Folbigg is the live one; if built, Clark's rejection becomes permanent. |
| **C. Contaminated supply harms the public; the state defends itself** | UK1 infected blood, AS4 Minamata, **✗ Japan HIV blood**, *EP58 Camp Lejeune (slated)* | **⚠ SEE §5-F.** Japan dropped. UK1 and AS4 cannot both be built, and neither should sit near EP58. |
| **D. Moral-panic mass child-abuse prosecution** | EU9 Outreau, EU10 Peter Ellis | **ONE ONLY** — and both carry severe ad-safety exposure. |
| **E. Systemic removal of children from families** | UK2, CW4, CW8 Tuam, EU1, EU6 Spain, SY8 Verdingkinder, AS2 Korea, CW5 Motherisk | **The largest family and the emptiest lane in the archive (M3 = zero prior episodes) — and the family whose protagonists are ordinary citizens, which is now the decisive variable.** At most **TWO**, ≥6 episodes apart, running genuinely different sub-machines: adoption coercion (UK2/CW4) ≠ death and concealment (CW8) ≠ falsified export (AS2) ≠ told-the-baby-died (EU6) ≠ removal as labour (SY8) ≠ removal on bad forensics (CW5). **UK2 and CW4 are the same sub-machine — one only. UK2 and CW8 are distinguishable but US audiences conflate them (UK2's measured saturation note) — never adjacent.** |
| **F. Forced sterilisation / reproductive coercion by the state** | AS1 Japan eugenics, EU4 Greenland IUD | **ONE ONLY.** AS1 has the ruling and the compensation law; **EU4 has the sharper premise, a fresher quote (25 June 2026), lower context cost and better ad-safety framing options.** |
| **G. Coerced/false confession → wrongful conviction** | UK6 Kiszko, CW7a Pora, EU7 Iceland, *Hakamada (benched)* | **⚠ CAPPED BY EXISTING CONSTRAINT.** v003 §5.4: EP53 Norfolk + EP57 Hemme are "the maximum concentration this engine gets", no third multi-confession case before EP65. **EU7 Iceland is a multi-person false-confession case and is directly caught — it is Beatrice Six with a volcano.** |
| **H. Crime-lab / forensic-programme fraud** | SY1 FBI hair, SY2 Dookhan/Farak, SY5 Gilchrist, SY6 Zain, CW5 Motherisk | **ONE ONLY, and this is a crowded family.** SY6 Zain has the cleanest evidence and no living-person risk; SY1 has the institution-indicts-itself asset; SY2 is owned by Netflix; SY5 carries the death-penalty ad-safety load; CW5 belongs to family E as much as here. |
| **I. A citizen wrongly detained/deported/listed by state error** | UK5 Windrush, CW3 Alvarez Solon | **Lane completely open (M6). ONE ONLY** — both are "the state expelled its own citizen". **CW3 is far cheaper in context (30–40s vs 120–150s) and far safer in ad terms; UK5 is bigger and more live but carries audience-capture risk.** |
| **J. Corrupt police unit manufactures convictions** | SY3 Watts, *EP55 burge (built)* | **⚠ NEW THIS PASS (grep M7).** Different machines — a protection racket producing false drug convictions versus torture producing false confessions — but **the same city and the same police department.** **Never adjacent to EP55; never lead on "Chicago police"; different title grammar.** |

### 5-F. ⚠ THE CROSS-FILE COLLISION NOBODY HAS FLAGGED YET
**`TOPIC_PIPELINE.v003.md` slates EP58 = Camp Lejeune**: *an institution poisons its own people, its own documents prove it knew, and it litigates against them for decades.* **That is Family C exactly** — the same machine as **UK1 (infected blood)** and **AS4 (Minamata)**.

v003 §5.5 already blocks EP58 against B7 downwinders on precisely this shape (*"the state harms its own people and litigates the proof — never adjacent"*). **That constraint must be extended to UK1 and AS4.** UK1 in particular is the *British* Camp Lejeune, down to the withheld internal documents and the compensation scheme that pays a fraction of claimants.

**Recommendation: if EP58 Camp Lejeune is built, UK1 cannot follow within ~8 episodes — so this pool's strongest evidence-package candidate is date-locked by a US slate decision. That is worth knowing before EP58 is greenlit, not after.**

---

## 6. TOP 8 — RE-FLAGGED ON THE 2026-07-29 CRITERIA

**Weighting applied, in order:** (1) **protagonist_type** — ordinary-citizen strongly preferred (§0.1); (2) **US-context cost** — heavily weighted, ≤45s preferred, >120s near-disqualifying (§0.4); (3) **evidence strength** — verified primary quote, verified carrier, numbers on both ends; (4) **holds 20–30 minutes on its own merits**; (5) saturation; (6) ad-safety.
**"Needs a payoff" was NOT applied** (§0.2). **Loss-verb potential** noted where present.

| # | Candidate | Protagonist | US¢ | Why it ranks here |
|---|---|---|---|---|
| **1** | **AS2 — Korea's overseas adoption programme** | **ORD** | **~0** | **The only candidate in the pool with zero foreign-institution setup.** 112,000 of these children were raised in American houses by American parents, and the story *ends in America* with the US deporting its own adopted children — one of whom, Phillip Clay, jumped from a 14th floor in a country he had no memory of. Verified quotes from a TRC chair **and a sitting head of state**. Loss-verb natural. Holds 30 minutes easily. **Under the new criterion this is no longer a top-5 pick; it is the pick.** |
| **2** | **UK2 — UK forced adoption 1949–76** | **ORD** | **35–45** | Ordinary-citizen carrier with her own devastating verbatim; **the best single document in the pool** (a government refusing to apologise, in writing, with a typo in the refusal); the **only candidate with real scraped saturation numbers showing an open field**; a 27-day-old news peg; and loss-verb packaging. Lowest context cost of any non-US case. |
| **3** | **CW8 — Ireland Mother & Baby Homes / Tuam** | **ORD** | **45–70** | Catherine Corless is the **IJ / Civil-Rights-Lawyer shape** — an ordinary outsider who took the institution on — which is precisely the archetype the 3,656-video scan found converting at 3–18×. Verified Taoiseach quote from the Oireachtas record. **The present tense is physical and happening now: 99 infant remains recovered, 62 DNA samples, first cousins still legally ineligible.** |
| **4** | **EU3 — Mediator / Servier (France)** | **ORD** | **~30** | **NEW ENTRY, and the biggest riser.** Dr Irène Frachon is the same outsider-investigator archetype as Corless. **~30 seconds of context — "France's FDA" — against Vioxx, opioids and Purdue.** Verified presiding judge's quote, **zero English saturation**, a real conviction and a €415m repayment, **and the lowest ad-safety load of any non-US candidate.** A French feature film about Frachon proves the drama works and confirms nobody has made it in English. |
| **5** | **SY3 — Sgt. Ronald Watts / Clarissa Glenn** | **A-t-C (ORD-shaped)** | **n/a** | **NEW ENTRY.** Zero context cost. **The best opening two sentences found anywhere in this research** — an Illinois appellate court describing internal affairs handing a whistleblower's name to the sergeant she reported. Clarissa Glenn is functionally the ordinary-citizen archetype: the wife on the outside who would not stop. Loss-verb natural. Apparently the most under-served case in the systemic set. **Constrained only by the EP55 Chicago adjacency (§5-J).** |
| **6** | **UK1 — Infected blood / Langstaff** | **ORD** | **45–60** | Still the strongest *evidence* package in the non-US pool — a judge's own verbatim finding of a cover-up, an ordinary-citizen carrier with his own quoted testimony, and a hard live 2026 number (**17% of claimants paid, two years on**). The American-plasma thread turns the context cost into a hook. **Drops from #1 to #6 only because §5-F date-locks it against EP58.** |
| **7** | **EU4 — Greenland / Denmark IUD campaign** | **ORD** | **~45** | **NEW ENTRY.** Ordinary-citizen carrier with an unforgettable scene (a doctor walking into her classroom when she was 14). **A ministerial quote five weeks old**, a law introduced 25 June 2026, applications opening 1 July 2026, and travelling compensation teams reaching Greenland in autumn 2026 — **a filmable, in-progress present tense.** Low saturation. Current US news salience about Greenland collapses the context cost. Ad-safety is the constraint, and it is framable. |
| **8** | **SY6 — Fred Zain** | **A-t-C** | **n/a** | Zero context cost, **[V-PRIMARY★] character-exact text from the court's own PDF** (*"They stain our judicial system and mock the ideal of justice under law"*), an eleven-item list of fabrications that is already a screen sequence, a **dead villain and therefore no living-person risk at all** — the cleanest R1 in the pool — and no documentary competition found. **Held to #8 only by the accused-then-cleared protagonist.** |

### 6.1 WHICH OF MY ORIGINALLY-FLAGGED 8 FELL OUT, AND WHY

| Fell out | Was | Reason under the new criteria |
|---|---|---|
| **UK3 Malkinson** | #5 | **Protagonist.** A cleared ex-prisoner seeking vindication is the archetype measured at **0.5–0.8% CTR** and matches our own worst-performing lane (1.13%). Best evidence in the UK set, worst entry. **The single clearest casualty of the criterion update.** |
| **UK4 Hillsborough** | #6 | **Context cost (100–120s) plus assumed-high UK saturation.** Survives on protagonist and on a verified quote, but cannot outrank four candidates at ≤45s. |
| **AS3 Brothers Home** | #7 | **Ad-safety (severest in the pool) plus a Netflix series in September 2025.** Ordinary-citizen protagonist and a 500km-walk carrier keep it high in the pool, not in the top 8. |
| **SY7 Life Esidimeni** | #8 | **US-context cost 90–120s, front-loaded** — exactly what §0.4 now penalises hardest. Gold-standard verbatim keeps it just outside. |
| **CW1 Robodebt** | (was rising) | **Mechanism.** Two independent researchers reached the verdict unprompted that it is structurally the same film as EP56. Ordinary-citizen carrier and a March-2026 corrupt-conduct finding cannot outweigh that at this distance from EP56. |

### 6.2 ON THE COORDINATOR'S READ OF ARTHUR ALLAN THOMAS — TWO CORRECTIONS

The Thomas deep-dive is folded in at **§3-CW7b**. Two points in the summary I was given do not survive verification:

1. **The "unspeakable outrage" quote is [NONE VERIFIED].** The 1980 Royal Commission report was unreachable this session. The only verified line is much weaker (*"…why Mr. Hutton described shellcase 350 as containing blue-black corrosion when in fact it did not"*, and that is **[V-SECONDARY]**). **Do not put "unspeakable outrage" on screen.** Retrieving the primary report is the single highest-value action on this candidate — **if it verifies, Thomas rises sharply.**
2. **"Ad-safe" holds for the 1970 facts and fails on the carrier.** *"Both named villains dead"* is correct — Johnston d. 1978, Hutton d. 2013 — and is a genuine asset. **But the protagonist is alive: Arthur Allan Thomas (b. 2 Jan 1938) faced sexual assault charges 2019–2022, discontinued on mental-health grounds.** An exoneration-hero framing will be dismantled in the comments within an hour. **Not fatal, but it cannot be built as summarised — the 2019–2022 charges have to be handled on screen, not omitted.**

**Verdict between the two NZ picks:** on protagonist archetype and context cost, **Thomas beats Pora**; on carrier safety and quote verification, **Pora beats Thomas decisively**. Thomas is viable only once the Royal Commission quote verifies **and** the owner accepts handling the 2019–2022 charges. **Neither condition is met today, so neither NZ pick enters the top 8.**

### 6.3 JUST OUTSIDE

**SY1 FBI hair** would rank top-5 on evidence — an agency indicting its own testimony in its own words is the purest R-38 asset here — but the protagonist is accused-then-cleared. **EU1 Netherlands** would be top-3 on premise (26,000 families, 2,090 children taken, a whole cabinet resigning, zero English saturation, 45–60s context) **and it has the channel's second-highest measured non-US AVP behind it at NL 63.2%** — but its surviving spine needs a named mother nobody has produced. **EU5 Mollath** has zero English saturation and a high-concept premise but is accused-then-cleared and historical. **AS5 Ohkawara** has the best single line in the pool (*"Well — it's a fabrication"*, from a serving officer under oath) and the lowest ad-safety load, and is kept out by **180–300 seconds** of Japanese criminal procedure that only Carlos Ghosn can shorten.

---

## 7. WHAT MUST HAPPEN BEFORE ANY OF THIS IS PROMOTED

1. **Nothing non-US moves until E2 reads out** (§0.5). **The six US systemic candidates (SY1–SY6) are not subject to that freeze** and are available now.
2. **Verification pass, in priority order** — the items that would most change the ranking:
   (a) the **Korean TRC's official English report PDF** (`jinsil.go.kr` link is JavaScript-driven and resolves to "#") — this is candidate #1's weakest field;
   (b) the **1980 NZ Royal Commission report** — settles Thomas;
   (c) the **Robodebt report PDF** (the Commission's own domain timed out on every attempt);
   (d) the **Japanese Grand Bench judgment date anomaly** (§0.6 correction 9);
   (e) the **Minamata May 2024 microphone incident** — if real, a first-rank R-38 beat;
   (f) the **Brothers Home TRC August 2022 wording** — both streams failed independently; AP's Kim Tong-hyung did the definitive reporting;
   (g) **Ognall J's 1994 ruling** in *R v Stagg*, currently traceable only to a television documentary.
3. **Name the missing carriers.** Seven candidates are blocked on this alone: **UK8 Grenfell, CW4, CW5 Motherisk *(the Whiteman detail is verified but her current willingness is not)*, EU1 Netherlands, EU2 Norway, SY4 Ananias, SY8 Verdingkinder.** A systemic film without a named person is not buildable (R-22) — **and under §0.1 the carrier is now the single most valuable thing in a candidate.**
4. **Measure saturation properly.** Only **two** candidates have real scraped numbers. Four competitors are confirmed by other means and must be respected: **Netflix on Dookhan/Farak, Netflix on Grenfell, Netflix on Brothers Home, a Depp feature on Minamata** — plus **BuzzFeed's 11M-view Iceland video** and **PBS Frontline on Korean adoption**, which is candidate #1's one real competitor.
5. **Settle §5-F before EP58 Camp Lejeune is greenlit** — it date-locks UK1.
6. **Re-run the novelty gate at build time** — `ls -d episodes/*<slug>*`, a fresh name grep, **plus the two §6c checks (money quote + institutional actor, and the mechanism).** The M1/M2/M7 findings in §1.3 are why this file has the shape it does.
7. **Do not let any [V-SECONDARY] or [NONE VERIFIED] quote reach a script.** Every factual claim here is research-grade and must be re-established from primary sources into a `FACTS_LEDGER` (invariant 1).

---

*Provenance: built 2026-07-29 against the full 56-episode inventory. Novelty gate §1 — patterns N1–N6 and M1–M7 — run 2026-07-29. Research: six parallel streams commissioned; **five returned** (UK, Commonwealth, Japan/Korea/Taiwan ×2, Europe, mass-scale systemic) and **one stalled without delivering** (child-removal/border), so Verdingkinder, Australian forced adoptions and Canadian coerced sterilisation are the thinnest entries here. The session's WebSearch budget was already exhausted at 200/200 before verification began, so all streams fell back to direct primary-document fetching — which improved quote quality and degraded saturation measurement. **Ten factual corrections were caught at topic stage and are logged at §0.6 so they cannot re-enter.** Two mechanism calls were reversed on evidence (§4.3) and two points in a coordinator briefing were corrected on evidence (§6.2); both reversals are recorded rather than silently applied. Every quote carries a verification tag. No build file was touched; nothing was approved, scheduled or published; **no git commit was made — the working tree already carried unrelated modifications from other sessions.***







