# EP68 pinto — register inventory and producibility gate

**Measured 2026-08-12. Read-only. No render, build, or staging was run.**
Episode: `PD-2026-068-pinto` — Grimshaw v. Ford Motor Co., era **1968–1981, United States**.
Gate: `config/pd_planning_os.v002.json` → `producibility_gate` (green ≤ 0.15, amber ≤ 0.40, red > 0.40).

---

## 0. The answer, first

**CAN THE SHELF DRESS THIS FILM — PARTIALLY.** It can dress the twelve era-neutral
registers (186 of 324 video cuts). It cannot dress the seven era-bound registers
(138 of 324 cuts) at any price in query effort, because the material does not exist
on the shelf.

| reading of "available" | N | utilisation (262 ÷ N) | colour |
|---|---:|---:|:--|
| noun match, any era, any source (union of the nine buckets) | **3,992** | **0.066** | 🟢 green |
| institutional/archival sources, any subject | **1,058** | **0.248** | 🟡 amber |
| archival, surviving EP68 `forbidden_subjects` | **889** | **0.295** | 🟡 amber |
| archival **and** on one of the nine registers | **162** | **1.617** | 🔴 red |
| archival, on-register, ≥720p, not a talking head / council meeting | **24** | **10.92** | 🔴 red |
| archival, EP68-legal, title carries a year 1955–1985 (**any** subject) | **21** | **12.48** | 🔴 red |
| **the era-bound half only: 113 distinct assets needed vs supply** | **~8** | **~14.1** | 🔴 red |

The first row is the number the current pipeline is implicitly using, and it is why the
producibility gate would have said green while a human accepted **1 of 77** clips (1.3%).
The gate is green on *nouns* and red on *era*, on the same shelf, for the same film. That
gap is the entire finding.

---

## 1. The index, and what it does not carry

Two entry points exist and they read different things:

- `scripts/select_factory_assets.py --theme` reads `assets/asset_manifest.v001.json`
  (the **factory** shelf: pexels/pixabay stock, filename = download query, label audit
  measured 40% wrong). Not the archive.
- `scripts/search_archive.py` reads the centralised rights ledger
  `H:\pd-media\assets\archive\_ledger\*.jsonl` — **this is the archive index**, and it is
  what every count below is taken from.

Every ledger row carries exactly these fields:

```
id  source  source_url  title  license_field_raw  license_decision  theme
file_path  bytes  sha256  fetched_at  relevance_score  matched_keywords  kind
```

Factory rows add `subtype / category / theme_recovered / label_verdict / title_provenance`.

**There is no era field. There is no year field, no date-created field, no
`archival` / `period` flag, nothing.** Across all 423,225 ledger rows the only date-like
field of any kind is `date_argued`, present on **40** rows (Oyez/CourtListener audio, not
video). Sweep for confirmation:

```
py -3.11 -c "import json,os,collections;D=r'H:\pd-media\assets\archive\_ledger';\
k=collections.Counter();[k.update(json.loads(l).keys()) for f in os.listdir(D) if f.endswith('.jsonl') \
for l in open(os.path.join(D,f),encoding='utf-8',errors='replace')];print(k)"
```

**This is itself the finding.** The shelf cannot be filtered for period material, because
nothing in it records when a clip was shot. Era can only be *proxied*, two ways, and both
are reported below:

1. **Source class.** `ia · nara · loc · nypl · smithsonian · met · wikimedia` are
   institutional and *may* hold period material. `pexels · pixabay · pixabay_extra ·
   mixkit · coverr · stock · unsplash · factory` are contemporary stock and never do.
2. **A four-digit year or decade word inside the provider title.** Present on 357 of the
   1,058 archival videos; 212 of those years are ≥ 2000.

---

## 2. Universe, after gate-equivalent filtering

Counting rule for everything that follows — DISTINCT clips: `kind == video`, deduped by
`sha256`, file verified present on disk, and withholding exactly what `search_archive.py`
withholds (ban-risk quarantine, `_quarantine` paths, owner-marked-`unusable` theme×source).

```
video rows in the ledgers            40,480
  withheld: ban-risk quarantine         762
  withheld: sitting in _quarantine    1,326
  withheld: owner-marked unusable     9,547
  withheld: duplicate sha256             62
  withheld: file missing on disk      2,682
= DISTINCT PLAYABLE VIDEO           26,101
```

| source class | distinct playable video | share |
|---|---:|---:|
| modern stock (pexels, pixabay, pixabay_extra, mixkit, coverr) | **24,412** | 93.5% |
| archival / institutional (ia 647, nara 411) | **1,058** | **4.1%** |
| other (nasa, noaa — space and weather) | 631 | 2.4% |

Applying EP68's own 124-word `forbidden_subjects` list word-wise to the filename, exactly
as `check_spec_satisfied.py` does: archival survivors **889**, modern survivors **22,144**.

Two further facts about the 1,058-clip archival pool:

- **681 of 1,058 (64%) are below 720p.** Source: `_ledger/video_resolution.json`.
- Its themes are `war_history 240 · government_buildings 221 · navy_harbor 181 ·
  pd_feature_films 119 · courtroom_justice 88 · prison_jail 69 · japan 34`. It is a
  Second-World-War and civic-building shelf. It is not an American-life shelf.
- **26 clips channel-wide carry a title year in 1955–1985** (21 after EP68's forbidden
  filter). All 21 are listed in §5. None of them is a road, a car, a production line, a
  1970s courtroom, a 1970s office, or American domestic life.

---

## 3. Bucket inventory — the nine registers asked for

Method, reproducible: word-boundary `re` over the **provider title** of every distinct
playable video row (definition in §2), case-insensitive, `re.I`. Modern-vs-archival split
is by source class (§1). `yr` = title contains any 4-digit year or decade word.
`era` = title contains a year in 1955–1985.

| # | bucket | regex (verbatim) | total | archival | modern | yr | era |
|---|---|---|---:|---:|---:|---:|---:|
| a | roads / highways / traffic | `\b(highway\|freeway\|interstate\|expressway\|turnpike\|motorway\|traffic\|roadway\|road\|street scene\|main street\|intersection\|toll\|driving\|motorist\|thoroughfare)\b` | **1,316** | **7** | 1,308 | 1 | **0** |
| b | cars of the era | `\b(automobile\|automobiles\|car\|cars\|sedan\|coupe\|station wagon\|pickup\|ford\|chevrolet\|chrysler\|plymouth\|buick\|pontiac\|oldsmobile\|cadillac\|volkswagen\|datsun\|vehicle\|vehicles\|motor car\|jalopy\|used car\|car lot\|dealership\|hot rod)\b` | **891** | **4** | 876 | 2 | **1** |
| c | assembly line / factory / industrial | `\b(assembly line\|assembly\|factory\|plant\|manufactur\w*\|industrial\|industry\|foundry\|machine shop\|welding\|welder\|conveyor\|production line\|worker\|workers\|labor\|steel mill\|mill\|riveting\|lathe\|press shop)\b` | **411** | **4** | 399 | 0 | **0** |
| d | courtroom / judge / jury | `\b(court\|courtroom\|courthouse\|judge\|judges\|jury\|juror\|jurors\|trial\|testimony\|witness stand\|attorney\|lawyer\|counsel\|litigation\|verdict\|deposition\|supreme court\|appeal)\b` | **88** | **42** | 46 | 9 | **0** |
| e | documents / memos / files / drawings | `\b(document\|documents\|memo\|memorandum\|memoranda\|typewriter\|typing\|typist\|filing cabinet\|file cabinet\|files\|paperwork\|ledger\|blueprint\|blueprints\|drafting\|draftsman\|engineering drawing\|schematic\|dossier\|records\|archive\|report\|form\|forms\|stamp\w*)\b` | **283** | **7** | 273 | 5 | **0** |
| f | hospitals / burn wards / ambulances | `\b(hospital\|clinic\|emergency room\|surgery\|surgical\|operating room\|nurse\|nurses\|doctor\|physician\|patient\|ambulance\|paramedic\|stretcher\|gurney\|burn\|burns\|intensive care\|infirmary\|medical\|ward)\b` | **219** | **12** | 206 | 0 | **0** |
| g | period suburbia / domestic interiors | `\b(suburb\|suburban\|suburbia\|subdivision\|neighborhood\|housing\|home\|homes\|house\|houses\|family\|kitchen\|living room\|dining room\|bedroom\|backyard\|front lawn\|porch\|driveway\|domestic\|household\|housewife)\b` | **431** | **30** | 395 | 17 | **3** |
| h | corporate offices of the era | `\b(office\|offices\|boardroom\|board room\|conference room\|executive\|corporate\|corporation\|business\|desk\|secretary\|meeting\|management\|headquarters\|company)\b` | **682** | **26** | 654 | 17 | **1** |
| i | vehicle fire and wreckage | `\b(fire\|fires\|burning\|blaze\|flames\|explosion\|explode\w*\|wreck\|wreckage\|crash\|collision\|smash\|accident\|derail\w*\|firefighter\|fire truck\|fire engine\|salvage\|junkyard\|scrap\|debris)\b` | **415** | **37** | 373 | 3 | **0** |
| | **union of all nine, distinct** | | **3,992** | **162** | 3,830 | | |

Equivalent one-shot lookups against the same index:

```
py -3.11 scripts/search_archive.py --shot "assembly line 1970s automobile plant" --kind video --md
py -3.11 scripts/search_archive.py --shot "interstate highway two lane 1970s" --kind video --md
py -3.11 scripts/search_archive.py --shot "courtroom judge jury 1970s" --kind video --md
```

### Reading the table

- **Bucket (i) is moot for this episode regardless of supply.** EP68's
  `forbidden_subjects` bans `fire · flame · burning · crash · collision · accident ·
  wreck · wreckage · smoke` in the source filename, and a match is an automatic build
  failure. That is deliberate (`EP68_pinto_FOOTAGE_PLAN.v001.md` §2). Bucket (f) is
  likewise banned end to end: `hospital · ambulance · doctor · nurse · patient · burn`.
  Two of the nine registers asked for are contractually unusable at any inventory level.
- **Every bucket is 93–99% modern stock.** Bucket (a): 1,308 of 1,316. Bucket (b): 876 of
  891. Bucket (c): 399 of 411. This is the retrieval failure the hand review found —
  the nouns are there in five figures and the era is absent.
- **The archival remainder is not what its bucket name suggests.** The 162 archival
  on-register clips, after removing talking heads and council meetings, drop to 149; of
  those only **24 are ≥720p**, and here is that entire list, verbatim:

  `Trump's Fraud Trial: Day #2` · `Trump's Criminal Trial` · `The $83.3 Million Dollar
  Verdict` · `Alonzo Mann, Sworn In For The Defendant… Leo Frank Trial` (1913) ·
  `Judge Leonard S. Roan's Jury Instructions in the Leo Frank Trial` · `Sunday, 27th
  July 1913, All in Readiness for Leo Frank's Trial` · `Baby Judge Judy Funny and Cute
  Moments` · `Judge Metal Sonic - The Series` · `America's Funniest Home Videos - Season
  19` · `Link-Up Video 12/26/2014, Prescott AZ Courthouse Square` · `Japanese Planes Bomb
  Pearl Harbor, USS Arizona Explodes & Sinks` · `Goering Takes Stand in War Criminals
  Trial` · `Combat Rifle Company (25th Infantry Division)` · `Allied Drive on in Italy –
  1944` · `Newsreel: Fire Power! U.S. Guns Open Upon Nazis In Italy` · `Fire at Evin
  Prison` · `The Business of Incarceration` · `In US Town That Embraces Refugees, Auto
  Shop Business Flourishes` · plus five city-council meeting recordings.

  Not one of those can appear in a film about a 1972 sedan on Interstate 15.

---

## 4. Utilisation and the gate

From `episodes/PD-2026-068-pinto/episode_spec.v001.json`: `distinct_video_assets = 265`,
`target_cut_sec = 3.7`, `era_setting.years = [1968, 1981]`, `era_setting.country = USA`.
`EP68_pinto_FOOTAGE_PLAN.v001.md` §5 allocates **324 video cuts / 265 distinct sources**
(distinct fraction 0.818). The brief's figure of **262** is used as the numerator below;
the spec's 265 changes nothing.

Staged today: **43** mp4 files under `remotion/public/pinto/`.

The film's own nineteen registers split cleanly on whether the frame must *read* as
1968–1981:

| | registers | cuts | distinct assets (×0.818) |
|---|---|---:|---:|
| **era-bound** — a modern frame betrays the film | R1 car · R2 freeway · R4 factory · R8 corporate office · R10 press/broadcast · R15 crowd · R19 period media | **138** | **113** |
| **era-neutral** — the frame carries no era marker | R3 liquid · R5 drafting hands · R6 instruments · R9 paper · R11 civic/federal · R12 stone columns · R13 farmland · R14 counting · R16 hands & backs · R17 clock · R18 rust · R20 dusk | **186** | **152** |

Supply against each half, using the replacement query set of §6 (distinct, EP68-legal):

| half | needed | available | utilisation | colour |
|---|---:|---:|---:|:--|
| era-neutral | 152 | **747** | **0.203** | 🟡 amber — dressable with a named staging plan |
| era-bound | 113 | **74 raw / ~8 era-true** | **1.53 / ~14.1** | 🔴 red under every reading |

**Gate colour for EP68 as a whole: 🔴 RED.** The film-level utilisation that matters is the
era-bound one, and it is 1,400%. Producing the green 0.066 headline number requires
counting a Kazakh government building, an Indian textile mill and an LED-lit motorway as
supply for a 1972 Ford story — which is precisely what the 465-query harvest did.

**CAN THE SHELF DRESS THIS FILM — PARTIALLY.** 186 of 324 cuts yes; 138 of 324 cuts no.

---

## 5. Buying the missing coverage with GPU time

Contract: `F + 2M ≥ 262`, at **206 s per i2v conversion**.
Channel norm from `producibility_gate.ai_motion_caution`: ~68% archive footage, **0% AI
motion**; EP62–65 drifted to 44–57% AI motion and that is recorded as a regression, not a
standard.

| scenario | F | M | GPU time | AI-motion share of 324 cuts |
|---|---:|---:|---:|---:|
| A. ship on today's pool, convert the rest | 43 | **110** | **6.29 h** | 68% — worse than the recorded regression |
| B. re-harvest generically (measured 1.3% accept on 3,992) | ~52 | **105** | **6.01 h** | 65% |
| C. **re-harvest the era-neutral half properly, i2v buys only the era-bound half** | 152 | **55** | **3.15 h** | 34% |
| D. as C, sized on the era-bound register alone (113 needed, ~8 on shelf) | — | **53** | **3.03 h** | 33% |

**Recommended: C/D — about 53–55 conversions, ~3.0–3.2 GPU hours**, run off period-correct
stills (Codex per rule 19; local SD3.5/SDXL only for repair or emergency top-up), covering
R1, R2, R4, R8, R10, R15, R19 and nothing else. That lands the film at ~33% AI motion:
above the channel norm, below the EP62–65 regression band, and it is the only lever that
produces a 1972 freeway at all.

Note the compounding hazard named in the gate config: `solve_totals` splits video
proportionally to pool capacity, so an oversized AI pool pushes archive cuts off screen
(measured on correa: 52 → 46 → 41 archive cuts at +0/+20/+40 plates). Generate **exactly**
the era-bound count. Do not generate a buffer.

---

## 6. Replacement query set

The queries were wrong **for the era-neutral half only**. For the era-bound half no query
set can help, and §3 of the existing footage plan already recorded this without naming it:
`1970s` → 0 · `archival` → 0 · `super 8` → 0 · `8mm film` → 0 · `film reel` → 0 ·
`old film` → 0 · `crash test` → 0 · `blueprint` → 0 · `typewriter` → 0 · `courtroom` → 0 ·
`fuel pump` → 0. Every one of those zeros was then "solved" by substituting a bare generic
token — `hit` (641), `arch` (468), `line` (374), `street` (350) — and those substitutions
are what delivered Santorini, Seoul and TradingView.

Yields below are counted against the index, not harvested. Same filtering as §2, plus
EP68's `forbidden_subjects`. `shelf` = distinct clips whose title matches.

### Era-neutral — use these; supply is real

| register | replacement phrase (no bare generic tokens) | shelf | arch | mod |
|---|---|---:|---:|---:|
| R3 | `liquid poured into glass vessel` / `pouring water close` | 9 | 0 | 9 |
| R5 | `hand drawing with pencil ruler` / `sketching on paper` | 9 | 0 | 9 |
| R6 | `laboratory instrument dial gauge` / `test tube microscope` | 215 | 5 | 210 |
| R9 | `stack of paper pages turning` / `documents on a desk` | 13 | 0 | 13 |
| R12 | `stone column civic facade` / `marble colonnade` | 25 | 0 | 25 |
| R14 | `counting coins on a table` / `calculator arithmetic` | 76 | 0 | 76 |
| R16 | `hands on a table no face` / `back of a figure silhouette` | 267 | 2 | 265 |
| R17 | `clock hands second sweep` / `analog clock face` | 5 | 0 | 5 |
| R18 | `rusted metal corroded surface` / `salvage yard derelict` | 33 | 0 | 33 |
| R20 | `empty street at dusk` / `twilight quiet street` | 108 | 0 | 108 |
| | **distinct union** | **747** | **7** | **740** |

747 candidates against 152 needed distinct assets = **0.203, amber**. At the ~25% eyeball
accept rate these phrases should earn (they name a subject, unlike `light` or `city`),
that is ~187 usable — enough, with the staging plan the amber band requires.

### Era-bound — these are written for completeness; the supply is not there

| register | replacement phrase | shelf | arch | mod |
|---|---|---:|---:|---:|
| R1 | `vintage car interior dashboard` / `antique car classic car` | 11 | **0** | 11 |
| R2 | `two lane asphalt centre line` / `road lane marking` | 1 | **0** | 1 |
| R4 | `metal press stamping line` / `conveyor production line` | 12 | **0** | 12 |
| R8 | `wood panel meeting room` / `conference table panelled` | 1 | **0** | 1 |
| R10 | `rotary press newsprint fold` / `linotype printing press` | 9 | **0** | 9 |
| R19 | `8mm home movie grain` / `16mm film reel projector` | 40 | **28** | 12 |
| | **distinct union** | **74** | **28** | 46 |

**Zero archival supply in five of the six era-bound registers.** The 28 archival hits in
R19 are the `ia` home-movie collection — that is the only genuinely period American moving
image on this shelf, it is 8mm/16mm grain of family scenes and train trips, 1920s–1970s,
and it is texture, not subject. Everything else in the era-bound column is modern stock
that used the word "vintage" in its own title.

The 21 EP68-legal archival clips carrying a 1955–1985 year, channel-wide, any subject —
this is the complete list, and it is what "period American footage on this shelf" means:

```
Playhouse 90: Judgement At Nuremberg (CBS, 1959)      Chicago riots, Chicago, Illinois (1968)
Fleet Review. Secretary Honored… 1956/09/17           Storm Havoc. Hurricane Kills 43… 1955/08/15
FBI Scans The Deteriorating Masks… 1962 Alcatraz      The Naked Kiss 1964 (feature)
Johnny Cool 1963 (feature)                            New Orleans Uncensored 1955 (feature)
A Life At Stake 1955 (feature)                        Home movie 000432: 1967 SF peace march
Parker, Randall — Destruction Of The Victory Theater 1978, 16mm
Maya the Bee Movie (1977, English dub)                AMC Theaters Pre-Rolls 1983-2009
1957 Campaign Firecamp Training                       One-Eyed Jacks 1961 (western)
The Deadly Companions 1961 (western)                  Joshua 1976 (western)
The Lemurs — Ex-Lemurs House Party, 1978 — 8mm        Dandelion 1976 silent movie
Thunderbirds Super 8mm Film (1965)                    Alonzo Mann Affidavit 1982, Sullivan County TN
```

Plausibly usable in EP68: **three** — the 1967 peace march (R15 crowd), the 1978 house
party 8mm (R19 grain), the 1978 theater demolition 16mm (R18). That is the honest N for
the era-bound half, and it is why §5 recommends buying it with GPU time.

---

## 7. Generalisation — what this shelf is and is not, for the premise gate

**This shelf is strong in the contemporary and the era-neutral: close-focus abstraction and
timeless surfaces** — hands, paper, liquids, instruments, coins, rust, stone facades, dusk,
weather, machinery in the abstract — where 22,144 EP68-legal modern-stock clips mean any
episode can dress its metaphor lane, its silences and its data beats without a gap.
**It is structurally unable to dress anything that must *look like a specific past*** —
period vehicles, period streets, period workplaces, period consumer life, period broadcast
— because it holds only 1,058 institutional videos (4.1% of playable video), 64% of them
sub-720p, themed on the Second World War, harbours and government buildings, of which
**26 channel-wide name a year between 1955 and 1985**; and because no ledger field records
when anything was shot, the shelf cannot even be *asked* for period material, so a
noun-based producibility measurement returns green while the era-based one returns 1,400%.
**Therefore the premise gate must score utilisation on the era-bound register alone** —
count only the cuts whose frame must read as the period, and measure them against archival
sources only — and treat every episode set before roughly 1995 as amber-or-red by default
with its AI-motion budget agreed at premise time, not discovered at assembly.

---

## Appendix — exact reproduction

- Index: `H:\pd-media\assets\archive\_ledger\*.jsonl`, excluding
  `ban_risk_quarantine.jsonl`, `purged.jsonl`, `shot_feedback.jsonl`, `rejects*`,
  `*_removed.jsonl`, `*_dedup_removed.jsonl`, `*_candidates.jsonl`.
- Withheld, matching `scripts/search_archive.py`: rows in the ban-risk quarantine ledger,
  rows whose `file_path` contains `_quarantine`, rows whose `(theme, source)` is marked
  `unusable` in `H:\pd-media\assets\archive\_qc\archive_verdicts.jsonl`.
- Distinct = unique `sha256`; every counted row was `os.path.exists`-verified.
- Resolution from `H:\pd-media\assets\archive\_ledger\video_resolution.json`, keyed
  `source:id`.
- `forbidden_subjects` applied word-wise to `os.path.basename(file_path).lower()`, the same
  way `check_spec_satisfied.py` does.
- Bucket regexes are printed verbatim in §3; replacement-set patterns in §6.
- Contract for the ledger: `H:\pd-media\assets\archive\_ledger\CONTRACT.md`.
