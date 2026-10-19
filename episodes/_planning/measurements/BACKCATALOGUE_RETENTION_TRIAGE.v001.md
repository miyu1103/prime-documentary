# BACK-CATALOGUE RETENTION TRIAGE v001

**Date:** 2026-07-28 · **Author:** analysis pass (GPU-free — no renders, no uploads, no API writes)
**Scope:** every published long-form with a real audience-retention curve (20 videos).
**Verdict up front:** the diagnosis is solid and reusable; the *remaster* is not worth doing. See §5.

---

## 0. Method and provenance

| Input | File | Window |
|---|---|---|
| Retention curves (official Analytics API, 100 points each) | `scripts/_yt_retention_curves.json` | 2026-06-01 .. 2026-07-27 |
| Views / AVD / AVP / minutes / subs per video | `scripts/_yt_analytics.json` | same |
| Hook verdicts | `scripts/_yt_hook_health.json` | 2026-06-01 .. 2026-07-13 |
| Impressions + CTR per video | `episodes/_planning/measurements/ctr_baseline_20260725.reconstructed.md` | 28d ending 2026-07-25 |
| Rules judged against | `episodes/_planning/DEEP_RESEARCH_FINDINGS.v001.md` §1 (R-1..R-6), §2 (R-7..R-13), §3 (R-14..R-18) | 2026-07-26 |

`_yt_retention_curves.json` holds 49 videos; **29 are `parse_status: no_rows`** (no audience data). The 20 with
`ok:official_api` are the entire evidence base. Script text at each drop timestamp was read from each episode's
shipped caption file (real timestamps, not estimates); narration chunk boundaries from each episode's
`06_audio/narration_index.*.json`.

Metric definitions used below:
- **HL (half-life)** = first second at which `watch_ratio` crosses below 0.50 (linear interpolation between curve points).
- **r30 / r60 / r120 / r180** = `watch_ratio` at that elapsed second.
- **Worst minute** = largest fall in `watch_ratio` across any 60-second sliding window, with its start timestamp.
- **Mid decay** = (watch_ratio at 30% of length − watch_ratio at 85%) expressed in points per minute. Rule floor: ≤1.5 pt/min (R-4).
- **80–180s cliff** = r80 − r180, the explanation-block danger zone (R-2).
- **rel30** = `rel_perf` at 30s. 0.50 = peer median. This is YouTube's own like-for-like comparison.

### ⚠ Confidence warning — read before acting on any single row

Most of these curves rest on a handful of viewers. Curve granularity = 1 viewer, so a video with 18 views
cannot resolve anything finer than 5.6 points.

| Tier | Views in window | Videos |
|---|---|---|
| **USABLE** (≥100) | 158, 133 | terry, titan |
| **WEAK** (40–99) | 55, 43, 40 | madoff, lange, dbcooper |
| **NOISE** (15–39) | 16–33 | hinton, swartz, onecoin, cotton, carpenter, timbs, milken |
| **UNUSABLE** (<15 or 0 in-window) | 0–11 | rodriguez, katz, gardner, carsearch, flashcrash, hinders, florence, tyler |

**Only terry and titan support a per-video decision.** Everything else is usable as *pattern* evidence in
aggregate (that is how DEEP_RESEARCH_FINDINGS §1 legitimately used it — median of 19 curves), not as a
per-video business case. Treat the individual numbers below as directional, and the §2 cause-mapping —
which is read off the *script*, not the curve — as the durable finding.

---

## 1. Per-video diagnosis

Sorted by impressions (the thing that actually determines value). `n` = views in window.

| # | Episode | Video | Len | Impr | CTR% | n | HL | r30 | r60 | r120 | r180 | Mid decay | 80–180 cliff | Worst minute | rel30 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 016 titan | `marQjsCagh0` | 2174s | 4,292 | 2.42 | 133 | **123.2s** | 85.8 | 65.3 | 50.6 | 43.6 | 0.33 | 16.5 | −36.0pt @22–87s | 0.368 |
| 2 | 006 terry | `bYcqabvvxak` | 682s | 4,070 | 3.14 | 158 | 36.5s | 57.4 | 32.0 | 22.0 | 14.7 | 1.01 | 8.3 | **−64.8pt @7–68s** | 0.117 |
| 3 | 029 hinton | `Qyad4FejCIc` | 698s | 2,880 | 1.35 | 33 | 46.5s | 64.0 | 43.6 | 29.6 | 26.0 | 0.94 | 9.1 | −60.0pt @7–70s | 0.256 |
| 4 | 037 florence | `SOu4Y1NkGGY` | 552s | 2,260 | 0.71 | 0 | **14.9s** | 37.2 | 34.2 | **39.1↑** | 27.8 | **2.58** | 2.6 | −69.6pt @6–66s | 0.157 |
| 5 | 035 hinders | `Xc_PxdC_75c` | 1156s | 1,855 | 1.24 | 0 | 31.1s | 52.4 | 32.3 | 19.4 | 16.1 | 0.61 | 7.2 | **−71.0pt @12–69s** | 0.167 |
| 6 | 030 cotton | `5L_HCGJxX_U` | 711s | 1,760 | 0.74 | 22 | **21.3s** | 37.4 | 38.4↑ | **40.9↑** | 36.4 | 1.39 | 0.0 | −59.1pt @7–64s | 0.206 |
| 7 | 023 swartz | `FTm1icKgycU` | 1743s | 1,468 | 0.82 | 23 | 33.6s | 56.3 | **17.9** | **4.9** | 4.3 | 0.00 | 8.7 | −65.2pt @17–70s | 0.130 |
| 8 | 005 madoff | `sphERPA4gAc` | 721s | 1,459 | 1.85 | 55 | 30.0s | 50.0 | 35.1 | 28.1 | 22.8 | 1.06 | 10.5 | −59.6pt @7–65s | 0.145 |
| 9 | 021 dbcooper | `tt7U1XgjCU4` | 1782s | 1,367 | 1.39 | 40 | 77.2s | 84.3 | 58.7 | 45.4 | 39.4 | 0.26 | 9.7 | −47.9pt @18–71s | 0.287 |
| 10 | 022 milken | `mj9qEKPRatE` | 1659s | 828 | 1.21 | 16 | 91.2s | 69.7 | 50.0 | 43.8 | 43.8 | **2.05** | 11.4 | −43.8pt @17–83s | 0.299 |
| 11 | 032 carsearch | `bXATF9ZnKLE` | 697s | 779 | 3.85 | 9 | 41.8s | 56.0 | 47.5 | 37.5 | 35.4 | 0.78 | 7.1 | −55.0pt @7–70s | 0.340 |
| 12 | 014 lange | `Sz8zPUoBANM` | 554s | 736 | **4.48** | 43 | 41.6s | 62.3 | 36.5 | 23.9 | 22.6 | 0.94 | 6.2 | −61.9pt @6–66s | 0.206 |
| 13 | 009 timbs | `m-uWzgWHGPg` | 720s | 632 | 2.69 | 18 | 27.0s | 46.5 | 26.3 | 26.3 | 21.1 | 0.80 | 5.3 | **−73.7pt @7–65s** | 0.182 |
| 14 | 008 carpenter | `zE3nCUlUmLY` | 679s | 626 | 2.24 | 18 | **20.4s** | 44.4 | 33.3 | 27.8 | 25.1 | **1.78** | 8.3 | −55.6pt @7–68s | 0.158 |
| 15 | 020 gardner | `1h267U6PY0I` | 1644s | 595 | 1.18 | 10 | **148.0s** | 75.3 | 63.5 | 50.0 | 30.5 | 0.00 | **29.5** | −40.0pt @16–82s | 0.222 |
| 16 | 017 onecoin | `vikfOBHullI` | 1210s | 520 | 3.27 | 23 | 33.3s | 56.5 | 36.2 | 24.3 | 16.5 | 0.00 | 15.5 | −60.0pt @12–73s | 0.119 |
| 17 | 026 katz | `68oWZRiOnB8` | 632s | 460 | 1.74 | 10 | 69.5s | 80.0 | 50.0 | 30.0 | 20.0 | **1.73** | 20.0 | −50.0pt @6–63s | 0.172 |
| 18 | 033 tyler | `rU2vk9XL4vY` | 1107s | 455 | 1.54 | 0 | **298.9s** | **100.0** | 75.8 | **70.0** | 60.0 | 0.99 | 17.7 | −30.0pt @11–66s | **0.444** |
| 19 | 027 rodriguez | `tpAKfHKuwqY` | 648s | 425 | 2.35 | 11 | 55.1s | 73.7 | 45.5 | 45.5 | 38.4 | **1.53** | 7.1 | −54.5pt @6–65s | 0.236 |
| 20 | 018 flashcrash | `5Jap-0h43A4` | 1336s | 241 | 3.32 | 9 | 73.5s | **93.3** | 63.8 | 45.5 | 27.3 | −0.74 | 18.3 | −54.5pt @27–80s | **0.533** |

Channel medians across these 20: **HL 42.5s · r30 62.3% · r120 30.0%**. This reproduces the
DEEP_RESEARCH_FINDINGS §1 figure (median half-life 42s) on an independent recompute — the finding is sound.

**Rule violations, counted:**
- **rel30 ≥ 0.50 (peer median):** 1 of 20 passes (flashcrash 0.533). 19 of 20 lose to peers inside 30 seconds.
  This is the binding constraint, exactly as §2 states.
- **Mid decay ≤1.5 pt/min (R-4):** 4 fail — florence 2.58, milken 2.05, carpenter 1.78, katz 1.73; rodriguez 1.53 borderline.
- **HL below the 42s median:** 11 of 20.
- **The worst single minute is the FIRST minute in 18 of 20 videos** (window starts at 6–27s). Only gardner (16s)
  and flashcrash (27s) start later, and both start late only because their opening holds.

### The cleanest correlation in the data

Sort the 20 by whether the first 5 seconds name a person and state an irreversible event (R-8/R-9), read off the caption files:

| First 5s | Videos | Median HL | Median r30 |
|---|---|---|---|
| **Person + irreversible event** | titan, dbcooper, gardner, tyler, milken, katz, hinton, florence, cotton | **77.2s** | **75.3%** |
| Second-person hypothetical, abstraction, question, or meta-preamble | terry, lange, carpenter, madoff, timbs, hinders, onecoin, swartz, carsearch, rodriguez, flashcrash | **33.6s** | **56.3%** |

Median half-life **more than doubles** when the first sentence obeys R-8. Two members of the top group
(florence, cotton) still collapse — and both collapse in the *packaging-mismatch* signature (§2.4), not the
opening-text signature. Remove those two and the strong-opening median HL is **91.2s**.

---

## 2. Cause mapping — the script line sitting at each drop

Quotes are from each episode's shipped caption file at the stated timestamp. This is the durable part of this
document: it is read off the script, so it does not depend on the noisy view counts.

### 2.1 Second-person hypothetical instead of a person (R-8 fail)

**006 terry** — `08_edit/captions.final.v001.srt` · worst minute −64.8pt starting at **0:07**
> `[0.0] You are walking down a sidewalk when a police officer stops you, turns you around, and runs his hands along the outside of your clothes.`

No one is named. Nothing has happened to anybody. It is a thought experiment, and the viewer is invited to
decline it. The real story — a 39-year veteran detective, two men, a store window, two loaded pistols — is
sitting right there in Act I and does not arrive until **1:04**. Then, at the exact half-life, the film hands
the viewer a doctrine lecture:
> `[30.9] We think of the Fourth Amendment as a simple wall: the police need a warrant, or at least solid evidence, before they can search you. [39.8] For most of American history, that was close to true.`

and follows it with a banned table-of-contents (R-12):
> `[50.9] Over the next twelve minutes: the ordinary afternoon that created the gap, the standard the Supreme Court invented to fill it, and the quiet cost of…`

**014 lange** — worst minute −61.9pt at **0:06**. Same construction:
> `[0.0] A police officer tries to pull you over for something small. You are almost home, so you keep going the last few seconds, pull into your own garage…`

Arthur Lange is not named until **1:18**. The half-life lands mid-doctrine:
> `[32.0] The Fourth Amendment protects a lot of places, but it protects your home most of all. As a rule the police cannot enter your home without a warrant -- that is the baseline and the exceptions to it are narrow. [46.8] One of those exceptions is an emergency the law calls exigent circumstances…`

That is a **contiguous ~25s of person-action-free exposition at 32–57s** — a straight R-2 build FAIL. Note that
lange has the **highest CTR on the channel (4.48%)**: the packaging is doing its job and the opening is
throwing the audience away.

**008 carpenter** — HL **20.4s**, the third-shortest, mid decay 1.78 (R-4 fail):
> `[0.0] Right now, the phone in your pocket is keeping a record of where you are. It does it automatically, every few minutes, and it sends that record to your carrier.`

A product-explainer voice, no human. Timothy Carpenter is never named in the first 30 seconds; the film reaches
him only as "one man's location records" at 0:11. Then, at the half-life, a rhetorical question stands in for a
loop (R-10: "a topic-question is not a loop"):
> `[22.3] The question that reached the Supreme Court was simple and enormous: when your phone tracks you, who does that trail belong to?`

### 2.2 Abstraction / imperative / meta-preamble before any human (R-8, R-13, R-19)

**023 swartz — the single worst structural offender on the channel.** r60 **17.9%**, r120 **4.9%**, r180 4.3%.
The film loses ~95% of its starters inside two minutes and then runs for another **27 minutes**.
DEEP_RESEARCH_FINDINGS §3 already names it ("Swartz essay-led, AWT 1:09 — the median clicker never met Act 2");
the narration index shows exactly why. From `06_audio/narration_index.v001.json`:

- `SPN-0001` (0.0–20.7s) — "By the time he was twenty-six years old, he had quietly helped build pieces of the internet… **This is the story of how** both of those things were true" — the banned "This is the story of…" construction, R-8, in the *first* chunk.
- `SPN-0002` (22.9–52.8s) — the half-life sits dead centre of this:
  > `[22.9] Let us start with a simple question, the kind that sounds easy right up until you actually sit with it. Who owns knowledge? Not one book, or one song, or one invention. The whole shared record of what human beings have ever managed to figure out.`

  Thirty seconds of pure abstraction. Opens with a question (0/26 winners do this), commands the viewer to "sit with it" (R-19 emotion-command), and names nobody.
- `SPN-0004` (79.3s) — **the protagonist is finally named at 1:19.** R-9 requires ~0:15.
- `SPN-0005` (98.2–129.6s) — "It is a story about a gap. The distance between what the law technically allows, and what the law is actually for." More abstraction.
- `[131.2]` — "**Over the next half hour we are going to do three things, in order.**" A table-of-contents at 2:11, explicitly banned by R-12.
- `[166.5]` — a self-harm content advisory. Whatever its ethical merit, it lands at 2:47, on top of an audience already down to ~5%.

The subject of the film does not appear until 1:19; by 2:00 there is essentially no one left to meet him.

**017 onecoin** — the shipped edit (`captions.v007.structure_v010.srt`) opens on what was originally the *third*
narration span:
> `[0.0] Here is what you need to know before we start.`

A meta-preamble about the video, not the story — the loser signature in R-13. Ruja Ignatova is not named until
**1:30**, despite being one of the most visually arresting subjects in the catalogue (red gown, roaring London
arena — material the film owns and buries). Half-life at 33.3s lands on:
> `[24.2] To understand how this works, you have to understand the feeling it was built on. It is a very specific feeling, and you have almost certainly had it. It is the feeling of being late.`

**005 madoff** — opens on an imperative pointed at a chart:
> `[0.0] Look at this line. It goes up. Month after month, year after year.`

Half-life at 30.0s lands precisely on the banned construction:
> `[30.7] This is the story of Bernard Madoff — and of the chart that should have given him away.`

Then the 80–180s block is a résumé, not a scene: `[84.5] To understand how so many smart people were fooled, you have to understand who Bernard Madoff was… [106.7] He'd been chairman of a major stock market. [110.2] He sat on industry boards.` — cliff 10.5pt.

**009 timbs** — **worst 60-second drop in the catalogue, −73.7pt starting at 0:07.** Opens on an institution, not a person:
> `[0.0] The police can take your car, your cash, even your house — and never charge you with a crime.`

Tyson Timbs is never named; he is "one man's Land Rover" at 0:15. The half-life at 27.0s is immediately followed
by a definitional block: `[26.9] It is called civil asset forfeiture… [33.1] It is not a fine handed down by a judge after a trial.`

Instructive contrast: **033 tyler** tells a structurally identical story (government takes property over a small
debt) and opens `[0.0] A twenty-three-hundred-dollar bill took the home this woman spent years paying off — and every cent was legal.`
Its half-life is **298.9s** — eleven times timbs'. Same lane, same channel, same voice. The variable is the sentence.

### 2.3 Legislative-history / procedure block at 60–180s (R-2 fail)

**035 hinders** — worst 60-second drop starting at **0:12**, −71.0pt. The opening is second-person with no named
human (`[0.0] No crime. No charge. You kept every deposit under ten thousand dollars…`), and Carole Hinders is
introduced only as "a woman in her late sixties" at 0:18. Then the film enters exactly the block
DEEP_RESEARCH_FINDINGS §1 cites by name:
> `[80.0] It was added sixteen years later, in nineteen eighty-six, when Congress made it a separate crime to deliberately split your cash into smaller deposits to keep them under the ten-thousand-dollar line and dodge that report. [92.8] The aim was to stop launderers from tiptoeing under the threshold.`

That is legislative history — Congress, a year, a statutory purpose — running **65s to ~125s** with no person
acting. Meanwhile the concrete fact that would have held the audience is buried at **3:56**:
> `[231.7] the government emptied the restaurant's checking account. Every cent of it. Thirty-two thousand, eight hundred twenty dollars`

A named woman, a real number, a door-knock — sitting four minutes deep in a film whose audience is at 19.4% by 2:00.

**027 rodriguez** — opens on a question (`[0.0] How long can the police keep you at the side of the road?`), and at
the half-life restates the question rather than escalating: `[45.4] We spend a lot of energy arguing about when the police can pull you over. This case is about something quieter, and more personal — the clock.` Mid decay 1.53 (R-4 borderline fail).

**026 katz** — a genuinely good scene-built cold open (`[0.0] Los Angeles, 1965. A man steps into a glass phone booth… [9.1] He believes he is alone. [10.9] He is wrong.`) that holds to r30 80.0%, then throws it away with a table-of-contents at 1:12:
> `[72.5] Over the next twelve minutes: the hidden microphone that started it, the old rule it broke, and the single sentence that moved the Constitution from guarding places to guarding people.`

80–180s cliff 20.0pt, mid decay 1.73. **katz is the clearest single demonstration in the catalogue that the
R-12 "over the next N minutes" construction costs real audience** — the opening works, and the loss begins at
the exact second the film stops telling the story and starts describing itself.

**020 gardner** — same lesson, larger. Best-in-class opening (HL 148.0s), then the biggest 80–180s cliff on the
channel (**29.5pt**) starting at:
> `[135.3] What exactly vanished, and why it can never simply be sold. [140.2] Everything the FBI will and won't say about who did it. And why, after more than three decades and a ten-million-dollar reward…`

### 2.4 Packaging⇔opening mismatch (R-6) — the rising-curve signature

**037 florence** — HL **14.9s** (shortest on the channel), then the curve *rises*: r60 34.2 → **r120 39.1**.
**030 cotton** — HL **21.3s**, then r30 37.4 → r60 38.4 → **r120 40.9**.

Both openings are strong by R-8 (`florence [0.0] He was carrying the receipt. Proof, in his own hand, that the fine had already been paid. He showed it to the officer. He was arrested anyway.` / `cotton [0.0] She looked him in the eyes, in a court of law, and said: that is the man who attacked me… [9.1] And she was completely, catastrophically wrong.`).

A curve that craters and then climbs is not an opening failure. It is the wrong audience arriving, bouncing in
under 20 seconds, and leaving behind a small correctly-targeted audience that then behaves normally. This is the
exact signature R-6 tells us to monitor for. Both also carry the banned preamble a few seconds later
(`florence [18.7] This is the story of how a paperwork error…` / `cotton [18.6] This is the story of how the most careful, most confident eyewitness imaginable…`), which is worth fixing on principle — but it is not what is
producing these curves.

**Both were re-titled and re-thumbnailed in the 2026-07-25 packaging refresh.** Per the task scope and
`RUNBOOK_CTR_REMEASURE_0808.md`, they are class (b), already in flight, and are **excluded** from this plan.
Their CTRs (0.71% and 0.74%) are the two lowest long-form CTRs on the channel, which is consistent with
mismatch being the dominant cause. **Do not touch them before the 8/8 read.**

### 2.5 The three that work — what to copy

| Ep | Opening line | HL | Why it holds |
|---|---|---|---|
| **033 tyler** | `A twenty-three-hundred-dollar bill took the home this woman spent years paying off — and every cent was legal.` | 298.9s | Number + irreversible loss + incongruity, one sentence. r30 = 100%. |
| **020 gardner** | `Two men in police uniforms walked into a Boston museum and walked out with half a billion dollars of masterpieces. Eighty-one minutes. Thirteen works. And more than thirty years later — not one has ever been found.` | 148.0s | Actors, place, scale, unresolved. Four hard specifics in 12s. |
| **016 titan** | `There is a sound most people never hear. The sound of a door being closed from the outside.` | 123.2s | The one abstraction that works — because it is a *physical* image resolving into an irreversible act by 0:23. |

---

## 3. Ranked remaster candidates by expected recovered watch-time

### 3.1 Model

For each video: current mean watch fraction = trapezoidal area under its curve. Post-fix curve assumes opening
surgery closes **50% of the gap** between the video's r120 and the benchmark r120 of **50.0%** (median of the six
strong-opening videos that also held: titan, dbcooper, gardner, tyler, milken, katz). Survivors past 120s scale
multiplicatively (mid-video decay is unchanged — the data says mid-video is already healthy); the 0–120s head
gains at a discounted rate. Recovered watch-time = (28-day views from impressions × CTR) × Δ mean-watch-minutes.

This is deliberately conservative on the retention side and deliberately **generous on one assumption that turns
out to be false** — that the video keeps its impressions. See §3.3.

### 3.2 Gross ranking (assuming impressions survive)

| Rank | Ep | Class | Impr | CTR% | v/28d | r120 → post-fix | AWT min → post-fix | **Recovered min/28d** |
|---|---|---|---|---|---|---|---|---|
| 1 | **006 terry** | **(a) opening** | 4,070 | 3.14 | 127.8 | 22.0 → 36.0 | 1.90 → 2.77 | **110.0** |
| 2 | 023 swartz | **(c) structural** | 1,468 | 0.82 | 12.0 | 4.9 → 27.4 | 1.99 → 9.24 | 87.3 |
| 3 | **029 hinton** | **(a) opening** | 2,880 | 1.35 | 38.9 | 29.6 → 39.8 | 3.11 → 3.96 | **32.8** |
| 4 | **014 lange** | **(a) opening** | 736 | 4.48 | 33.0 | 23.9 → 36.9 | 2.13 → 2.98 | **27.7** |
| 5 | **017 onecoin** | **(a) opening** | 520 | 3.27 | 17.0 | 24.3 → 37.2 | 3.48 → 5.01 | **26.0** |
| 6 | **035 hinders** | **(a) opening** | 1,855 | 1.24 | 23.0 | 19.4 → 34.7 | 1.77 → 2.74 | **22.4** |
| 7 | 005 madoff | (a) opening | 1,459 | 1.85 | 27.0 | 28.1 → 39.0 | 2.61 → 3.40 | 21.5 |
| 8 | 032 carsearch | (a) opening | 779 | 3.85 | 30.0 | 37.5 → 43.8 | 3.60 → 4.08 | 14.6 |
| 9 | 008 carpenter | (a) opening | 626 | 2.24 | 14.0 | 27.8 → 38.9 | 2.92 → 3.87 | 13.4 |
| 10 | 009 timbs | (a) opening | 632 | 2.69 | 17.0 | 26.3 → 38.2 | 2.13 → 2.85 | 12.2 |
| 11 | 021 dbcooper | — | 1,367 | 1.39 | 19.0 | 45.4 → 47.7 | 7.96 → 8.32 | 6.9 |
| 12 | 026 katz | (a) R-12 trim | 460 | 1.74 | 8.0 | 30.0 → 40.0 | 2.38 → 2.93 | 4.5 |
| 13 | 037 florence | **(b) packaging** | 2,260 | 0.71 | 16.0 | 39.1 → 44.6 | 2.39 → 2.65 | 4.2 |
| 14 | 022 milken | — | 828 | 1.21 | 10.0 | 43.8 → 46.9 | 6.32 → 6.71 | 4.0 |
| 15 | 030 cotton | **(b) packaging** | 1,760 | 0.74 | 13.0 | 40.9 → 45.5 | 3.13 → 3.41 | 3.7 |
| 16 | 027 rodriguez | — | 425 | 2.35 | 10.0 | 45.5 → 47.7 | 4.33 → 4.51 | 1.8 |
| 17 | 018 flashcrash | — | 241 | 3.32 | 8.0 | 45.5 → 47.7 | 3.21 → 3.33 | 1.0 |
| 18 | 016 titan | **none** | 4,292 | 2.42 | 103.9 | 50.6 (at benchmark) | 10.58 | 0.0 |
| 19 | 020 gardner | **none** | 595 | 1.18 | 7.0 | 50.0 (at benchmark) | 6.82 | 0.0 |
| 20 | 033 tyler | **none** | 455 | 1.54 | 7.0 | 70.0 (above benchmark) | 8.30 | 0.0 |

**Total across all 20 = 394 min / 28 days = 6.6 hours.** Channel currently earns **2,778 min/28d**, so a
*complete* back-catalogue remaster is worth **+14%** of channel watch-time — before costs, and before §3.3.

**Top 5 class-(a) opening-surgery candidates = terry + hinton + lange + onecoin + hinders = 219 min/28d (3.7 hours).**

Fix-class assignment:
- **(a) opening surgery** — 10 videos. The whole loss is in the first 45–70s and the body is healthy (mid decay ≤1.5).
- **(b) packaging only** — florence, cotton. Rising curves, lowest CTRs. Already re-packaged 7/25; **excluded** pending the 8/8 read.
- **(c) structural** — swartz alone. r120 = 4.9% is not an opening problem; a 29-minute essay with its subject
  named at 1:19 and a table-of-contents at 2:11 cannot be rescued by re-recording 45 seconds. Its CTR (0.82%) is
  also third-worst, so both the entrance and the film fail independently. **Not worth rebuilding** — see §5.
- **none** — titan, gardner, tyler are at or above the benchmark. dbcooper, milken, rodriguez, flashcrash are
  within ~5pt of it. Touching any of these risks losing a working asset for a rounding error.

### 3.3 ⚠ The blocker that invalidates the gross ranking

**YouTube cannot replace the video file of a published video.** There is no such API and no such Studio feature.
The repository's own precedent confirms the only available path — `scripts/replace_miranda_youtube_v004.py`:

> uploads the premium MP4 to YouTube as private first · sets the selected flashy thumbnail · uploads English
> captions · waits for processing · **makes the new upload public** · **sets the old published upload private**

That is a **delete-and-reupload**. The new file gets a new video ID, and the old video's entire accumulated
history — impressions, ranking, session position, suggested-traffic edges — goes private with it.

**This has already been run once on this channel, and it is measured.** Miranda was remastered and re-uploaded
on **2026-06-23** (`youtube_replacement_verify.v004.json`: old `PjGEqW6F9WM` → private, new `cQFql7tT1fE` →
public, verified). Five weeks later, in the 7/25 baseline:

| | Impressions (28d) | CTR | Views in window |
|---|---|---|---|
| **miranda, remastered + re-uploaded 6/23** | **143** | **0.70%** | **1** |
| terry, never touched | 4,070 | 3.14% | 158 |
| titan, never touched | 4,292 | 2.42% | 133 |

The remaster produced a video that YouTube does not show to anyone. Against a channel median of ~700
impressions, 143 is a cold start that never recovered in five weeks.

**Every number in §3.2 is multiplied by the impressions the video keeps — and it keeps none.** For terry, the
video whose 110 min/28d makes the whole exercise look worthwhile, the surgery means trading a live asset
earning **269 min/28d on 4,070 impressions** for a new upload starting at zero. The expected value of
opening surgery on terry is not +110 min/28d. On the only evidence this channel has, it is **strongly negative**.

The gross ranking in §3.2 is retained because it correctly measures *where the retention is being lost* and
therefore what to fix **in new episodes**. It does not measure the value of remastering.

---

## 4. Five drafted cold opens

Written to DEEP_RESEARCH_FINDINGS §2 verbatim: R-7 (sound from frame 0), R-8 (declarative first sentence,
person + hard specific + incongruity; never a question; no "This is the story of…"), R-9 (protagonist named
≤0:15, opposing force ≤0:28), R-10 (BUT-contradiction loop by ~0:32, before the sting), R-11 (brand sting ≤5s,
audio-continuous, fused with the ritual title line), R-12 (post-brand = ONE escalating concrete + date/place
anchor), R-13 (no table-of-contents, one new concrete every 3–8s), R-19 (zero emotion-command imperatives).

Pace model **178 wpm** (per `scripts/gen_narration_case.py` / EP56 DESIGN §5): 0:32 ≈ 95 words, 0:45 ≈ 133 words.
Every fact below is taken from the episode's own shipped caption file. Items marked **[VERIFY]** are anchors I
could not confirm in the captions and which must be checked against `01_research` before recording.

**These are written to be usable either way** — as re-record scripts if the owner overrules §3.3, or (the
recommendation) as the pattern library for new builds and for any future episode covering the same case.

---

### 4.1 — 006 terry · `bYcqabvvxak` · 121 words ≈ 0:41

> Detective Martin McFadden had thirty-nine years on the force when he spun John Terry around on a Cleveland
> sidewalk and ran his hands down the outside of his coat. No warrant. No crime committed in front of him.
> He pulled a loaded pistol out of that coat.
>
> McFadden's whole reason was that he had watched Terry walk past one store window about a dozen times.
>
> That is a hunch. A hunch had never been enough to touch anyone.
>
> But in nineteen sixty-eight the Supreme Court looked at what McFadden did and, instead of striking it down,
> wrote him a rule.
>
> 【BRAND STING ≤5s — "This is the case of Terry versus Ohio."】
>
> That rule is now the legal basis for street stops in every state in the country.
> Downtown Cleveland. October, nineteen sixty-three.

Pre-sting 99 words ≈ 0:33 ✓ · post-brand 20 words ≈ 0:07 ✓ · named at 0:04 ✓ · opposing force at 0:00 ✓ ·
BUT-loop at 0:28 ✓ · zero imperatives ✓ · six hard specifics in the first 33s ✓.
Facts verified in `captions.final.v001.srt`: "McFadden, thirty-nine years on the force", "He feels the shape of
a pistol", "It is October 1963, in downtown Cleveland, Ohio", "about a dozen trips in all".

### 4.2 — 029 hinton · `Qyad4FejCIc` · 118 words ≈ 0:40

> For nearly thirty years the state of Alabama kept a date to kill Anthony Ray Hinton.
>
> On the night of the robbery that put him on death row, Hinton was fifteen miles away, locked inside a
> supermarket warehouse, working a night shift. He was clocked in. A supervisor could place him there.
> His own time card could place him there.
>
> The state sent him to death row anyway.
>
> Because prosecutors had something they believed could beat any alibi on earth — two bullets, and an old
> thirty-eight revolver taken out of his mother's house.
>
> 【BRAND STING ≤5s — "This is the case of Anthony Ray Hinton."】
>
> It would be sixteen years before anyone qualified was allowed to look at those bullets.
> Jefferson County, Alabama **[VERIFY year and county in `01_research`]**.

Pre-sting 94 words ≈ 0:32 ✓ · named at 0:04 ✓ · BUT-loop ("The state sent him to death row anyway") at ~0:23 ✓.
This is a **re-ordering**, not new material: the alibi currently lands at 1:50 and the bullets at 2:24. R-3
requires the emotional core by 0:90; moving it to 0:20 is the entire fix.
Facts verified: "fifteen miles away, locked inside a supermarket warehouse", "He was clocked in", "His own time
card could place him there", ".38-caliber revolver that belonged to Hinton's mother, recovered from her home",
"It had taken sixteen years".

### 4.3 — 014 lange · `Sz8zPUoBANM` · 124 words ≈ 0:42

> Arthur Lange was about a hundred feet from his own driveway, playing his music too loud and honking his horn.
> A California Highway Patrol officer flipped on his lights. Lange kept going, pulled into his attached garage,
> and hit the button.
>
> As the door came down, the officer put his foot underneath it. The door went back up. He walked into Lange's
> home. No warrant.
>
> For a noise complaint.
>
> But California's position was that he had never needed one — that anyone who fails to pull over, even for the
> smallest offense, can be followed straight through their own front door.
>
> 【BRAND STING ≤5s — "This is the case of Lange versus California."】
>
> In twenty twenty-one, nine justices had to decide whether a honking horn can cost you the walls of your house.
> Sonoma County, California.

Pre-sting 98 words ≈ 0:33 ✓ · named at 0:01 ✓ · opposing force at 0:07 ✓ · BUT-loop at 0:27 ✓.
Facts verified: "Lange, in Sonoma County, California", "playing his music loudly and honking his horn a few
times", "roughly a hundred feet away", "pulls into his attached garage", "puts his foot underneath it",
"In 2021, the Supreme Court".
**Highest-CTR video on the channel (4.48%) — the packaging promise is already correct; this makes the opening match it (R-6).**

### 4.4 — 017 onecoin · `vikfOBHullI` · 124 words ≈ 0:42

> On a stage in a London arena, in a red gown, Doctor Ruja Ignatova told a roaring crowd she had built the
> currency that would kill Bitcoin.
>
> She had a doctorate in law. She had the magazine covers. She had, in the end, more than four billion dollars
> of other people's money.
>
> She did not have a coin. There was no blockchain behind it. Nothing to mine, nothing to look up, nothing
> anyone could check. Not one line of it was ever real.
>
> But the people handing her their savings were not fools — and that is the part that should worry you.
>
> 【BRAND STING ≤5s — "This is the case of OneCoin."】
>
> On the twenty-fifth of October, twenty seventeen, she boarded a flight out of Bulgaria to Athens and was
> never seen again.

Pre-sting 101 words ≈ 0:34 ✓ · named at 0:07 ✓ · BUT-loop at 0:29 ✓. Replaces the meta-preamble
("Here is what you need to know before we start") with material the film already owns but currently buries
until 1:30.
Facts verified: "There was a woman in a red gown", "London arena", "Ruja Ignatova", "A doctorate in law",
"Over four billion dollars", "on the twenty-fifth of October", "Bulgaria, to Athens, Greece", "She calls it the
Bitcoin killer".

### 4.5 — 035 hinders · `Xc_PxdC_75c` · 125 words ≈ 0:42

> Carole Hinders had run the same small cash restaurant in northwest Iowa for thirty-eight years. She cooked,
> she worked the register, and she carried the day's takings to the bank herself.
>
> Then the federal government emptied the restaurant's checking account. Every cent of it. Thirty-two thousand,
> eight hundred and twenty dollars.
>
> She was never charged with a crime. She was never accused of one. Every dollar had come from plates she had
> sold that day.
>
> But the government did not have to accuse her of anything — because under this law it was not accusing her at
> all. It was accusing her money.
>
> 【BRAND STING ≤5s — "This is the case of Mrs. Lady's."】
>
> The rule that emptied her account had been written to catch cartels tiptoeing under a reporting threshold.
> Northwest Iowa. Mrs. Lady's Restaurant.

Pre-sting 100 words ≈ 0:34 ✓ · named at 0:02 ✓ · BUT-loop at 0:30 ✓. The $32,820 figure currently sits at
**3:56**; this moves it to 0:20. The Bank Secrecy Act legislative history (currently 65–125s, the R-2 violation)
is compressed to the single post-brand sentence and the rest folds in one sentence at a time after the first
payoff, per R-2 and reconciliation R-d.
Facts verified: "Carole Hinders", "Mrs. Lady's", "of northwest Iowa", "For thirty-eight years", "the government
emptied the restaurant's checking account. Every cent of it. Thirty-two thousand, eight hundred twenty dollars",
"to stop launderers from tiptoeing under the threshold".

### 4.6 Audio / edit steps required

**Total re-record: 612 words ≈ 3,430 characters ≈ $1.03 of ElevenLabs credit** (at the recorded
$0.30/1k chars). The narration cost is negligible. Everything expensive is downstream.

Voice settings are already pinned and must not be varied — `voice_id nPczCjzI2devNBz1zQrb`,
`model_id eleven_multilingual_v2`, HOOK section → `intense` preset
(`stability 0.38 / similarity_boost 0.84 / style 0.44 / speaker_boost on`), master loudnorm `I=-16:TP=-1.5:LRA=11`.

**Splice points** (start of the first surviving chunk, from each episode's `06_audio/narration_index.*.json`):

| Ep | Replace | Splice at | Notes |
|---|---|---|---|
| terry | `VC-0001` (HOOK 0–25.8s) + `VC-0002` (OPENING 26.2–54.6s) | **54.942s** = `VC-0003` "ACT I" | Cleanest splice in the set. Act I already opens on the scene ("It is October 1963, in downtown Cleveland"). |
| hinton | `VC-0001` (12.3s) + `VC-0002` (14.2s) | **not clean** — `VC-0003` is a single 50.2s chunk (27.2–77.4s) containing the victim-backstory block | `VC-0003` must itself be re-cut, so this is a ~77s rewrite, not a 45s one. Add ~60 words. |
| lange | `VC-0001` (HOOK 0–31.7s) + `VC-0002` (OPENING 32.0–75.9s) | **76.21s** = `VC-0003` "ACT I" | Clean. The doctrine block being deleted is entirely inside VC-0002. |
| onecoin | cold-open spans `SPN-0001`–`SPN-0005` | **re-derive from the shipped edit** | The shipped cut (`captions.v007.structure_v010.srt`) re-orders the narration index — the index's SPN-0003 is the film's 0:00. Do not trust index offsets here. |
| hinders | `VC-0001`–`VC-0005` (HOOK+OPENING, 0–~33s) | **after the structuring block ends ~125s** | The R-2 violation sits *past* the OPENING boundary, so the splice must swallow 33–125s. Largest of the five. |

**Caption regeneration: required in every case**, and it is not optional — total runtime changes, so every
downstream timestamp moves.
1. Edit only the `## COLD OPEN` / `## OPENING` blocks of the `_planning` script `.md`. `gen_narration_case.py`
   hashes each chunk's text and re-spends credit only on changed chunks.
2. ⚠ `VC-NNNN` ids are **positional**. Changing the *number* of chunks in the opening renumbers everything
   downstream and forces a full index remaster. Keep the opening's chunk count identical where possible;
   otherwise run `--remaster` (free, no TTS) to rebuild master + index from the existing paid mp3s.
3. `VC-0001.start` must stay `0.0` (HOOK-AUDIO, `BODY_START_SEC = 0.0`).
4. Regenerate `08_edit/captions.final.v001.srt` **as a new revision — never overwrite an approved one**
   (invariant 6), then mirror `captions[]` into `remotion/src/data/<slug>_film.json`.
5. Re-lock `durationInFrames` and shift every timing-anchored element: BGM, AE `film_offset`, and the brand
   sting to its new ~0:32 position. **Full re-render required** — this is the real cost, not the $1 of voice.
6. Re-mux with `build_case_film_mux.py` (stamps a new `audio_mix_sha256`), then re-run
   `check_final_acceptance.py`.
7. New render sha ⇒ `EXPECTED_HASH` in `schedule_<slug>.py` and `APR-0001.json`
   (`content_hash` + `video_sha256`) need **owner re-approval**.
8. **Then §3.3 applies**: publishing it means delete-and-reupload. There is no in-place replacement.

Realistic cost per episode: one full long-form render (WebGL, `--concurrency=4`), plus caption re-alignment,
plus re-approval — call it **3–4 hours of wall-clock and owner attention each, ~16–18 hours for five**.
Against 219 min/28d of *gross* upside that §3.3 shows is not collectable.

---

## 5. Honest counter-analysis — where the data does NOT support remastering

### 5.1 Do not bother — impressions too small to pay for any effort

Nine videos where the *entire* modelled upside is under 5 minutes of watch-time per 28 days. At any
plausible hourly cost this is negative:

| Ep | Impr | Upside (min/28d) | Why not |
|---|---|---|---|
| 027 rodriguez | 425 | 1.8 | Already r120 45.5%, near benchmark |
| 018 flashcrash | 241 | 1.0 | **Best rel30 on the channel (0.533)** — the only video that beats peer median. Do not touch. |
| 022 milken | 828 | 4.0 | Opening works (HL 91s); its issue is mid decay 2.05, which opening surgery does not address |
| 026 katz | 460 | 4.5 | Worth the R-12 trim *only* if the episode is ever rebuilt for another reason |
| 021 dbcooper | 1,367 | 6.9 | HL 77s, decay 0.26 — one of the healthiest curves in the catalogue |
| 016 titan | 4,292 | **0.0** | At benchmark. Highest impressions on the channel. **Touching this is pure downside risk.** |
| 020 gardner | 595 | 0.0 | At benchmark (HL 148s) |
| 033 tyler | 455 | 0.0 | **Above** benchmark (HL 298.9s, r30 100%) — this is the reference build |
| 037 florence / 030 cotton | 2,260 / 1,760 | 4.2 / 3.7 | Class (b). Re-packaged 7/25; **excluded pending 8/8** |

### 5.2 Do not bother — the curve cannot support the decision

18 of 20 curves have fewer than 100 views; 8 have fewer than 15 or zero in-window. hinders, florence and tyler
show **zero views** in the analytics window — their curves come from outside it entirely. Spending a render on
a per-video verdict derived from 9 viewers is not measurement, it is superstition. Only **terry** and **titan**
clear the bar, and titan needs nothing.

### 5.3 Do not rebuild swartz — the worst offender is also the worst investment

swartz is unambiguously the **single worst structural offender**: r60 17.9%, r120 4.9%, subject unnamed until
1:19, table-of-contents at 2:11, 29 minutes long. It also ranks #2 on the gross table (87.3 min/28d) purely
because its curve is so bad that any multiplicative improvement looks enormous — off a base of **23 views**,
where one viewer is 4.3 percentage points.

But: CTR 0.82% (third-worst), and the failure is in the *architecture* — an essay where a narrative belongs.
Fixing it means rewriting the script, re-recording ~29 minutes of narration, re-cutting the film, and then
re-uploading into a cold start. That is a new episode's worth of work with a used episode's ceiling. **Make a
new film about Aaron Swartz built to formula v2 instead**, if the subject is worth revisiting at all.

### 5.4 The structural blocker (restating §3.3, because it is the whole answer)

There is no in-place video replacement on YouTube. The channel has already run this experiment: miranda,
remastered and re-uploaded 2026-06-23, now draws **143 impressions and 0.70% CTR** — a dead video, five weeks
on. Remastering does not improve a video; it retires a video with history and publishes a stranger.

The videos worth fixing are worth fixing *because* they have impressions. Remastering is the one operation
guaranteed to destroy exactly the asset that justified it. This is not a marginal-cost argument — it is a
sign-of-the-result argument.

### 5.5 Opportunity cost versus new episodes

- Five opening surgeries ≈ **16–18 hours** (612 words of voice, ~$1 — the render and re-approval are the cost), gross upside 219 min/28d, collectable upside ~0 (§3.3), and a
  realistic downside of losing terry's 269 min/28d.
- One new episode built natively to formula v2 — the EP56 pattern — costs more, but **titan alone earns
  1,097 min/28d**. A single well-packaged new film is worth **2.8× the entire remaster pool of all twenty videos**.
- The channel's binding constraint is not retention on 20 old films. It is that **19 of 20 videos lose to peer
  median inside 30 seconds** — a *production-recipe* problem, now precisely diagnosed, that is fixed going
  forward at zero marginal cost.
- The other measured lever remains untouched and cheaper than either: DEEP_RESEARCH_FINDINGS §6 —
  end screens, playlists, interlinks (PLAYLIST traffic already measures 19.6 min/view, versus 0.16 for the
  Shorts feed). Nothing in this triage competes with that on ROI.

### 5.6 Recommendation

**Do not remaster. Harvest the diagnosis and put it into new episodes.**

1. **Zero re-uploads.** The miranda precedent settles it empirically on this channel's own data.
2. **Adopt the five cold opens in §4 as the pattern library** for `pd-script` and any future episode covering
   these cases. They cost nothing to keep and they encode the measured rule.
3. **Add two gates that this triage shows are not yet caught.** Both are cheap and both are script-time:
   - a first-sentence check for R-8 (person + hard specific + incongruity; reject second-person hypotheticals,
     questions, imperatives, and "This is the story of…"), and
   - a grep for the table-of-contents construction — "Over the next N minutes", "we are going to do three
     things". It appears in terry (0:50), katz (1:12), gardner (2:15), swartz (2:11), flashcrash (1:23), and in
     every case it sits on a measurable cliff. `check_retention_cadence.py` currently does not catch it.
4. **Leave florence and cotton alone until the 8/8 CTR read.** Their rising curves say packaging, and packaging
   was already changed on 7/25. Touching them now destroys the only clean experiment in flight.
5. **If the owner wants one remaster anyway**, the only defensible candidate is a video with nothing to lose —
   swartz (0.82% CTR) or cotton (0.74%) — never terry or titan. Even then, expect the miranda outcome.

---

## 6. Cross-references and non-overlap

- `episodes/_planning/BACKCATALOGUE_REMASTER_PLAN.v001.md` (2026-07-25) is a **different exercise**: a picture-grade
  re-render (scanline + haze removal) of **7 still-private, 0-view episodes** (EP41–47) that have never published.
  No overlap — that plan has no impressions to lose, which is exactly why it is sound and this one is not.
  Its TRAP 1 (sha + APR re-approval) and TRAP 2 (finalize-if-exists silently re-publishing the old video) apply
  verbatim to any work here.
- `episodes/_planning/measurements/RUNBOOK_CTR_REMEASURE_0808.md` owns the class-(b) packaging verdict. Nothing
  in this document should be executed before that read lands.
- `episodes/_planning/DEEP_RESEARCH_FINDINGS.v001.md` §1 is confirmed on independent recompute (median HL 42.5s
  vs its stated 42s). §2's rules are the ones used to write §4.
- Not touched by this document: EP50–56 build files, ingest-agent files, any published metadata.

**Nothing in this document has been executed. No render, no upload, no API write, no script modified.**
