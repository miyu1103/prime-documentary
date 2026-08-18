# EP68 · THE FORD PINTO — FOOTAGE RE-QUERY v001

**2026-08-12 · slug `pinto` · `PD-2026-068-pinto`**
**Companion data: `runs/qc/pinto_requery_plan.v001.json` (the query set and every count below).**

> **Nothing was harvested, staged, copied, ffprobed or rendered to produce this.** Every number
> comes from one read pass over `H:\pd-media\assets\archive\_ledger\*.jsonl`, reproducing
> `scripts/stage_footage_by_title.py`'s own `ledger_rows()`, `OK_LICENSE`, `TITLE_BLOCK`,
> `RIP_SIGNATURE`, `slugify()` and `have_ids` exclusions. The render queue was untouched.

---

## 0. The answer first

**The re-harvest cannot dress this film, and better queries will not change that.**

The contract asks for **265** distinct video assets. A corrected query set run over a corrected
matcher returns **44** fresh clips — **53** if `--max-mb` is raised to admit the archival files.
Reading all 53 titles, about **ten** are plausibly usable for a 1968–1981 American film, and one of
those ten is a clip the reviewers **already accepted** (the cast-iron fly press, `AR-v_109654`).

The fix is still worth shipping. It stops the pipeline pulling Santorini, and it closes two real
holes. But it is a correctness fix, not a supply fix.

```
contract distinct_video_assets                                   265
fresh clips a corrected harvest would return                      44
  ... with --max-mb raised 120 -> 600                             53
  ... if clips staged for other episodes were allowed            430   <- breaks arc_nonrepeat
of the 53, plausibly usable on title inspection                  ~10
```

---

## 1. Read this first: `forbidden_subjects` is binding

`episodes/PD-2026-068-pinto/episode_spec.v001.json` lists **124** `forbidden_subjects`, including
`fire`, `smoke`, `crash`, `wreck`, `wreckage`, `hospital`, `doctor`, `nurse`, `child`, `children`,
`police`, `gun`, `scales`, `gavel`, `handshake`, `cartoon`, `drone`, `beach` and `hourglass`. The
brief circulated to the 12 reviewers did not carry this list. It is treated as binding here, and
every one of the 132 replacement queries carries its own `forbidden_subject_check` field in the
JSON. All 132 read `PASS`. **No query in this plan was widened to buy yield.**

---

## 2. What actually went wrong — three causes, measured

### 2a. The matcher has no word boundaries. This is the big one.

`scripts/stage_footage_by_title.py` line ~215:

```python
if not all(t in title.lower() for t in terms):
    continue
```

`t in title` is a **substring** test. A query term matches the inside of an unrelated word.

Of the 807 candidates in `runs/qc/pinto_prestage_candidates.v001.json`, **100 (12.4 %) matched only
inside a word**; another 173 matched an inflection. Real rows, verbatim:

| query | what the ledger returned | the accident |
|---|---|---|
| `old car` | *a person h**old**ing an atm **car**d* | h(old) + (car)d |
| `old car` | *people protesting and holding placards* | **this is the 2020 BLM footage the reviewers found** |
| `arch` | *people m**arch**ing on the street in protest* | the second BLM source |
| `street town` | *street, **seoul**, korea, down**town*** | the Seoul apartment blocks |
| `car lot` | *man **car**rying bal**lot** box* | |
| `gas` | *vibrant las ve**gas** nightlife* | |
| `corn` | *freshly popped pop**corn*** | |
| `alley` | *canyon, ravine, v**alley*** | |
| `house front` | *a light**house** sits on the water in **front** of a cloudy sky* | |
| `old metal` | *g**old** bars, precious **metal**s* | |
| `form` | *globe of death per**form**ance in circus* | |
| `pump` | *the white church is surrounded by **pump**kins* | |
| `date` | *candi**date**s having an agreement* | |
| `trial` | *indus**trial** worker cleaning factory shop floor* | this accident produced **one of the five accepted clips** |
| `two lane` | *p**lane**t, digital, internet, network* | |
| `car plant` | ***car**pentry **plant*** | |
| `memo` | ***memo**ry card, dslr* | |

The stated cause (a) — "the queries leaned on generic tokens" — is true but downstream of this. A
generic token is only dangerous because the matcher lets it land inside other words. `justice`
returning an animated Iron Man is the same failure.

### 2b. `forbidden_subjects` was never applied. Nothing in the codebase applies it.

**106 of the 807** candidates carry a forbidden term as a whole word in their own ledger title:
`drone` 26, `burning` 14, `beach` 11, `smoke` 10, `fire` 5, `flame` 5, `gun` 4, `police` 4,
`girl` 3, `fireworks` 3, `soldier` 2, `blood` 2, `crash` 2, `hourglass` 2, `bitcoin` 1.

Worse: **19 of the 465 shipped queries *are* forbidden subjects** — `accident`, `ash`, `black
smoke`, `bonfire`, `burn`, `burning`, `campfire`, `candle flame`, `car crash`, `crash`, `ember`,
`fire`, `flame`, `hourglass`, `smoke`, `smoke rising`, `smoke slow`, `soot`, `wreck`.

The provenance is documented in the query file's own note
(`config/episode_footage_queries.v001.json`, `episodes.pinto.note`):

> *"The 124 forbidden_subjects in episode_spec are deliberately NOT encoded here — they are applied
> to candidate titles before staging."*

They are not. `prestage_footage_review.py` runs four mechanical filters — `junk_words`,
`blocklist`, `shape`, `cross_episode_reuse` — and none of them reads `forbidden_subjects`. It
loads the spec at line 480 and uses only `era_setting`, to print a banner. The author wrote the
queries relying on a downstream filter that does not exist.

### 2c. The `off_label` marker — the brief is half right, and the obvious fix would be wrong

**130 of the 216** presented candidates carried the `off_label` prefix on their tile, and yes, they
were queued for human review anyway.

But that prefix is **not** a ledger `off_label` tier. `scripts/check_pool_frames.py:964`:

```python
lead = "off_label " if s["flags"] else ""
```

`flags` is set whenever a sample has *any* flag at all, including the entirely benign
`look:vehicle` (482 samples) and `look:person` (382). **Dropping all 130 would delete the vehicle
register this film is about.** The name is a misnomer inherited from the ledger vocabulary.

The flags that *are* a judgement are `setting_mismatch:*` and `mobile_phone:*`. **18** candidates
carry one — Toronto, Vancouver, Bangkok, Tokyo, Kazan, Sicily, Indian railway station, a broken
iPhone, a smartphone close-up — and the human review **accepted 0 of the 18.** That is the cut to
make: precise, free, and it never touches a usable clip.

---

## 3. Worst ten shipped queries by yield

`--per-query 2` was in force, so no query could produce more than 2 candidates and "produced" is
capped at 2 by construction. 425 of 465 queries produced ≥1 candidate; 807 candidates total; **299
distinct candidates reached the 12 reviewers; 5 were accepted (1.7 %)**. Ranking is therefore by
damage per candidate, not volume. Full table with all counters is in the JSON.

| # | query | produced | judged | accepted | forbidden hits | non-US | modern tell | interior-of-word | what came back |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `street town` | 2 | 2 | 0 | 0 | 2 | 0 | 2 | **seoul/korea**; bergamo/italy |
| 2 | `autumn` | 2 | 1 | 0 | 1 | 2 | 1 | 0 | ukraine **drone**; maple/**japan** |
| 3 | `date` | 2 | 1 | 0 | 1 | 0 | 1 | 2 | "candi**date**s having an agreement"; **drone** over dilapidated building |
| 4 | `old building` | 2 | 1 | 0 | 1 | 2 | 1 | 0 | sicily **drone**; mexico kiosk |
| 5 | `old footage` | 2 | 1 | 0 | 1 | 1 | 1 | 1 | **drone** over crimea; freezing water macro |
| 6 | `houses` | 2 | 1 | 0 | 1 | 1 | 1 | 0 | **drone** over city street; **santorini** |
| 7 | `alley` | 2 | 2 | 0 | 0 | 0 | 0 | 2 | canyon/ravine/v**alley** ×2 |
| 8 | `coin` | 2 | 2 | 0 | 0 | 0 | 1 | 1 | coins on wood; **silver and gold bitcoins** |
| 9 | `corn` | 2 | 2 | 0 | 0 | 0 | 0 | 2 | pop**corn** at an amusement park ×2 |
| 10 | `form` | 2 | 2 | 0 | 0 | 0 | 0 | 2 | globe of death per**form**ance in circus; rotating globe |

Just outside the ten, and named in the brief: `chart` (2/2/0) returned *"man analyzing a chart"* and
*"dynamic stock market chart analysis setup"* — the TradingView screens; `accounting` (2/1/0)
returned *"woman, investment, bitcoin, currency, business, finances"*; `coins` returned the second
Bitcoin clip; `library` returned the Harry Potter cosplay; `banknote` and `debris` returned the euro
notes; `speech` and `street people` returned the 2020 protest footage alongside `old car`/`arch`.

Every named reject in the brief traces to this table or to §2a: Iceland and Santorini via `houses`
and place-blind tokens, Seoul via `street town`, Bitcoin via `coin`/`coins`, TradingView via
`chart`, BLM via `old car` and `arch`, Harry Potter cosplay via `library`, euro banknotes via
`banknote`/`debris`/`overcast`, drone aerials via 26 forbidden-`drone` titles nothing screened out.

---

## 4. The two mechanism fixes (plus the one that matters more)

### (i) Apply `forbidden_subjects` at harvest time

**File: `scripts/prestage_footage_review.py`** — it already loads the spec at line 480 and already
owns the mechanical-filter chain and its drop receipt. Add a fifth filter, `forbidden_subjects`,
between `blocklist` and `shape` (cheap text test before the expensive ffprobe):

```python
def filter_forbidden(rows: list[dict], spec: dict | None) -> tuple[list[dict], list[dict]]:
    """episode_spec's forbidden_subjects, applied to the CANDIDATE's ledger title and staged name.

    config/episode_footage_queries.v001.json's pinto note states these 'are applied to candidate
    titles before staging'. Nothing did. 106 of EP68's 807 candidates carried one as a whole word
    -- drone 26, burning 14, smoke 10, fire 5, police 4 -- and reviewers found every one of them.
    check_spec_satisfied matches these word-wise against the STAGED filename, so a survivor here
    is an automatic build failure later; catching it at candidate time costs one regex.
    """
    terms = sorted({str(w).lower() for w in (spec or {}).get("forbidden_subjects") or []})
    if not terms:
        return rows, []
    rx = re.compile(r"\b(" + "|".join(re.escape(w) for w in terms) + r")\b", re.I)
    keep, drop = [], []
    for r in rows:
        m = rx.search(f"{r.get('title') or ''} {r['name']}")
        if m:
            r["drop_reason"] = f"episode_spec forbidden_subject {m.group(0)!r}"
            r["dropped_by"] = "forbidden_subjects"
            drop.append(r)
        else:
            keep.append(r)
    return keep, drop
```

Wire it in beside the others (`rows, d_forb = filter_forbidden(rows, spec if not spec_problems
else None)`), add `"forbidden_subjects"` to the `order` list and to `dropped_by`, and add
`d_forb` to `dropped`. On EP68's existing candidate list this removes 106 of 807 before any frame
is extracted.

**Belt-and-braces, same term list, in `scripts/stage_footage_by_title.py`** so a standalone
`--emit-candidates` run is covered too — inside the per-query loop, right after the `TITLE_BLOCK`
test.

### (ii) Drop the decisive contradictions before sheet generation

**File: `scripts/prestage_footage_review.py`**, immediately after `content_look()` returns and
before `presented` is built:

```python
    # A CANDIDATE THE PIPELINE HAS ALREADY CONVICTED DOES NOT GO ON A BALLOT. `setting_mismatch`
    # and `mobile_phone` are place/period contradictions read off the clip's own ledger title;
    # unlike `look:*` (which only says "magnify this") they are a finding. 18 of EP68's 216
    # presented candidates carried one -- Toronto, Bangkok, Tokyo, Kazan, an iPhone -- and the
    # 12 reviewers accepted 0 of the 18. Do NOT extend this to every flagged tile: the
    # `off_label` prefix on a sheet fires on ANY flag, including look:vehicle (482 samples), and
    # cutting on it would delete the vehicle register EP68 is about.
    DECISIVE = ("setting_mismatch:", "mobile_phone:")
    convicted = {c["clip"] for c in receipt.get("clips", [])
                 if any(str(f).startswith(DECISIVE) for f in (c.get("era_prompts") or []))}
    if convicted:
        for r in rows:
            if r["name"] in convicted:
                r["drop_reason"] = "pipeline already found a place/period contradiction"
                r["dropped_by"] = "decisive_contradiction"
        dropped += [r for r in rows if r["name"] in convicted]
        rows = [r for r in rows if r["name"] not in convicted]
        print(f"[prestage] 5b. decisive contradiction: -{len(convicted):4d} -> {len(rows)} left")
```

### (iii) The word-boundary matcher — bigger than both

**File: `scripts/stage_footage_by_title.py`**, replacing `all(t in title.lower() for t in terms)`:

```python
    # SUBSTRING MATCHING IS WHY `old car` RETURNED CREDIT CARDS AND BLM PLACARDS (EP68, 2026-08-11:
    # 100 of 807 candidates, 12.4%, matched only INSIDE another word -- h(old)ing a (car)d,
    # m(arch)ing, (car)rying bal(lot), las ve(gas), pop(corn), v(alley), per(form)ance,
    # candi(date)s). Match on word starts instead, which keeps the plural/inflection hits the
    # ledger relies on (car -> cars, tire -> tires) and kills the interior accidents.
    words = re.findall(r"[a-z0-9]+", title.lower())
    if not all(any(w.startswith(t) for w in words) for t in terms):
        continue
```

### Which files are safe to edit **now**, and which must wait

The live queue is `scripts/_finish_ep62_65.sh` → `scripts/_finish_episode.sh`. Its execution set is:
`assemble_episode_i2v.py`, `build_asset_manifest_motionfirst.py`, `build_case_bgm_generic.py`,
`build_case_film_audio.py`, `build_case_film_generic.py`, `build_case_film_mux.py`,
`build_render_public_dir.py`, `check_caption_breaks.py`, `check_episode_inputs.py`,
`check_spec_satisfied.py`, `pd_postrender_gate.py`, `pd_render_guarded.sh`, `pd_splice_cuts.py`,
`polish_captions_srt.py`, `probe_before_render.sh`, `prune_pool_by_blocklist.py`,
`retire_unused_pool_clips.py`.

| file | status | why |
|---|---|---|
| `scripts/stage_footage_by_title.py` | **SAFE NOW** | not in the queue's execution set, not imported by anything in it |
| `scripts/prestage_footage_review.py` | **SAFE NOW** | same; it *calls* stage_footage_by_title, it is never called by the queue |
| `config/episode_footage_queries.v001.json` (`episodes.pinto` key only) | **SAFE NOW** | read only by `stage_episode_footage.py` / `prestage_footage_review.py`; `greene`/`correa`/`memphis`/`marmet` keys must not be touched |
| `scripts/check_pool_frames.py` | **MUST WAIT** | `check_episode_inputs.py:380` does `from check_pool_frames import pool_state`, and `check_episode_inputs.py` runs in the queue |
| `scripts/check_final_acceptance.py`, `scripts/check_shipped_frames.py` | **MUST WAIT** | both had live processes at the time of writing (greene and marmet acceptance) |
| anything else in the execution set above | **MUST WAIT** | until `out_finish_ep62_65.log` reports DONE |

Fixes (i), (ii) and (iii) all land in the two SAFE-NOW files. **Nothing in this plan requires
touching a file the queue executes.**

---

## 5. What the shelf actually holds — the finding that decides it

```
ledger video rows with a usable licence                        39,092
  after TITLE_BLOCK / RIP_SIGNATURE                            37,922
  after size band 1-120MB                                      34,395
  after forbidden_subjects (124 terms)                         30,495
  after file exists on disk                                    23,899
  after excluding ids already staged or rejected elsewhere     17,022   <- EP68's addressable pool
```

Of those 17,022: **16,776 (98.6 %) are modern royalty-free stock** — pixabay 12,231, pexels 3,268,
mixkit 1,264, coverr 13. The genuinely archival sources contribute **191** (ia 111, nara 80).

**The index has no era field.** The ledger title is the only searchable text, and it almost never
states a period:

- titles in the addressable pool carrying **any** era token: **86** of 17,022
- titles carrying an era token **and** a US token: **2** — *"vintage globe with north america
  highlighted"* and *"colosseum, rome, marcello theater, historical centre, capitol"*

1968–1981 is not selectable from this shelf by any query. That is not a query-writing problem.

### The period props exist, and every one is already spoken for

| term | on the shelf | free for EP68 | where they went |
|---|---|---|---|
| `typewriter` | 83 | **0** | all 83 staged for other episodes |
| `rotary phone` | 8 | **0** | all 8 staged elsewhere |
| `printing press` | 9 | **0** | all 9 staged elsewhere |
| `courthouse` | 5 | **0** | all 5 staged elsewhere |
| `vintage car` | 22 | **0** | 11 staged, 11 human-rejected |
| `classic car` | 10 | **0** | 4 staged, 6 human-rejected |

130 `factory*` folders hold **10,073** clip ids; recorded verdicts burn another **5,302**; the
union is **12,143**. Sixty-odd prior episodes have eaten the period shelf.

And these the shelf has **never** held, at any size, under any filter: drafting board, filing
cabinet, teletype, switchboard, station wagon, license plate, tube TV / CRT, carbon paper, punch
card, slide rule, American assembly line, `archival`, `1970s`.

### One real lever inside the harvester: the size band

`--max-mb` defaults to **120**. NARA's video rows have a **median of 145 MB**, IA's **253 MB**. The
default band was excluding the only genuinely archival material on the shelf — 279 of 403 NARA rows
and 872 of 1,303 IA rows. Raising it to 600 is correct and free.

It buys **9 clips**. NARA's video holdings are almost entirely WWII: *USS TIRANTE COMBAT FILM*,
*INVASION OF PELELIU*, *MILITARY POLICE TRAFFIC PATROL, X CORPS, KOREA* — every one of them
`military` / `war` / `police`, forbidden here. IA is mostly present-day city-council recordings.

---

## 6. The replacement query set

132 queries across 8 registers, in `runs/qc/pinto_requery_plan.v001.json`. Each register carries the
**intent phrase** (what the film needs, written as era-and-subject) and the **index-checkable
terms** the ledger's title field can actually be asked — because a literal
`"1970s american highway traffic archival"` is a five-term AND against a title and returns exactly
zero, on this ledger, forever.

| register | intent | queries | fresh clips (word-boundary) | + max-mb 600 |
|---|---|---|---|---|
| `period_automobile` | late-60s/70s American passenger car, interior, rear end | 22 | 4 | 6 |
| `period_road` | two-lane and early interstate, period signage | 14 | 5 | 7 |
| `ford_engineering` | assembly line, drafting office, product-review interior | 26 | 10 | 11 |
| `records_and_paper` | filing, carbon copy, newsprint web, hot-metal printing | 18 | **0** | **0** |
| `federal_regulator_dc` | US federal civic architecture, hearing room | 13 | 2 | 2 |
| `indiana_county` | northern Indiana farmland, county courthouse, main street | 15 | **0** | 3 |
| `period_domestic_tech` | CRT television, rotary telephone, radio set | 13 | **0** | **0** |
| `era_neutral_mood` | weather, sky, paper texture, flag — what the spec allows | 11 | 23 | 24 |
| **total distinct** | | **132** | **44** | **53** |

Two registers return **zero**: `records_and_paper` and `period_domestic_tech` — the typed paper and
the CRT, two of the four things the film is actually about. `indiana_county` returns 3, of which
one is a 1952 California earthquake and one is a Portuguese town square.

Reading all 53 titles from the best scenario: 5 Netherlands highways, a Rome colosseum, an
Afghanistan flag, a Soviet flag, 8 3D green-screen flagpole loops, a WWII battleship reel, a car
ferry. Plausibly usable: **about ten** — and one of those ten is `AR-v_109654`, the cast-iron fly
press the reviewers already accepted.

---

## 7. Recommendation

1. **Ship fixes (i), (ii) and (iii) regardless of what EP68 does.** They are cheap, they are
   correct, they land only in files the queue does not execute, and they stop the next episode
   repeating this. Fix (iii) alone would have removed 100 of the 807 candidates and both BLM
   sources.
2. **Do not plan EP68 around a re-harvest.** 44–53 fresh clips cannot cover 265 required assets,
   and no query set changes that. The material is not on the shelf.
3. **Three real levers, for the owner to choose between:**
   - **(a) The AI plate track, which is already healthy** — `runs/qc/pinto_plate_verdicts.v001.json`
     records **123 of 123 plates accepted** at content review, and the footage plan already assigns
     the four impossible registers (typed paper, the underside of a car, an American courthouse,
     and the period itself) to plates R001–R080. This is the shortest path and it is largely built.
   - **(b) A scoped reuse exemption.** Allowing clips staged for other episodes lifts the yield from
     44 to **430**, and the period props come back: typewriter 83, capitol 33, vintage car 22,
     printing press 9, courthouse 7, rotary phone 5. This breaks `arc_nonrepeat` and the owner's
     standing no-repeat directive, so it needs an explicit APR naming which clips and which
     episodes they are shared with. It is the only lever that produces period material this week.
   - **(c) Targeted ingest** — NARA's non-military film series, Prelinger. Only this one grows the
     shelf, and it is the only durable answer for any future period episode.

The owner asked for the truth over a plan. The truth is that (b) or (c) is required; the query set
in this plan is worth shipping either way, but on its own it delivers ten clips.
