# EP75 — HANDOVER v002 (paste this into the thread that will write it)

**Supersedes v001 for everything except why this episode was chosen.** v001 stays on disk: it holds
the demand measurement and the original brief. Where the two disagree, **this file governs**, because
the primary record has now been read and it corrected the brief in three places.

## Where the episode actually is

| artifact | state |
|---|---|
| `episodes/PD-2026-075-lahaina/episode_spec.v001.json` | **written and valid** — `py -3.11 scripts/check_episode_spec.py --slug lahaina` exits 0 |
| `episodes/_planning/EP75_lahaina_FACTS_LEDGER.v001.md` | **written** — 11 sources, ~90 rows, 7 absences, 13 quarantine rules |
| `EP75_lahaina_FILM_BIBLE.v001.md` | **not written — start here** |
| script, image order, thumb prompts, scene plan, fact_recheck | not written |

Committed as `57f9a498` on `claude/vibrant-archimedes-2mmr5h`. Research process notes:
`docs/handover/2026-08-21-ep75-research.md`.

**Do not re-do the research.** Everything narratable is in the ledger, and everything that is NOT in
the ledger may not be narrated (⛔-10).

## The film, in one sentence

> Hawaiʻi built the largest outdoor warning siren network in the world and tested it on the first
> business day of every month — and on the day a town burned from the mountain side down, one siren
> inside the burn perimeter was operable, the system had never once been used to warn of a wildfire,
> and the alerts that were sent went to phones on towers that had already gone dark.

The brief in v001 said "the sirens did not sound." **That is not the strongest true version and it is
not what the state's own investigation says.** The two findings that carry the film, read from FSRI's
Phase Two findings appendix on the Attorney General's own site:

- **Finding 37** — "Only one (1) siren from the All-Hazard Outdoor Warning Siren System was operable
  within the burn perimeter of the Lahaina area on August 8, 2023."
- **Finding 38** — "The All-Hazard Outdoor Warning Siren System had not been utilized for warning of
  WUI fires prior to August 8, 2023."

Add the reported detail that Maui's 80 sirens include four in the Lahaina area and **all four are
sited by the ocean**. A network built for a wave arriving from the sea, in a town that burned from
the mountains down. That is the controlling idea, and its specificity is also the defence against
trap 1 below.

## Three received facts the record contradicts — do not write any of them

1. **"A power outage disabled the water pumps."** Finding 21: no pumps are used outside the
   production facilities, and "both systems had uninterrupted electrical power during the August 2023
   fires and produced water at capacity for the duration of the fire." The pressure loss is Finding 24
   — burned structures' plumbing bleeding the system dry. `⛔-08`.
2. **"How it rekindled is undetermined."** The County of Maui's own release says the embers "remained
   undetected and were rekindled by a severe wind event at approximately 2:52 p.m." *Undetermined* is
   the name of a classification the fire did **not** receive; it is classified **Accidental**.
3. **"The sirens failed."** Nothing says that. One was operable inside the burn perimeter; none were
   activated. Those are two facts from two sources and merging them invents a third. `⛔-02`, `⛔-03`.

## Five things that will cost you a day if you do not know them

**1. `check_script_length` over-counts. Do not size the script with it.** It does not strip HTML
comments, and every script since EP66 carries a citation comment under each factual line. Measured
inflation: EP69 +2,195 words, EP68 +1,798, EP71 +1,256. On EP72 it read 5,751 while the TTS extractor
saw 4,876 — four minutes of finished film. **Size with
`py -3.11 scripts/gen_narration_case.py --ep PD-2026-075-lahaina --dry-run`.**

**2. The registry's 171.79 wpm model is 11 % slow for this house style.** EP72 measured **191.7 wpm**.
The spec's `script_words` **[4900, 5400]** was derived from that measurement, but it is a frame, not a
sizing method: run `--measure-section ACT_1` (~$1, ElevenLabs is pre-approved) **before writing to
length**. EP72's projection from that measurement came within 0.33 % of the delivered master.

**3. Faces are allowed and wanted** (owner decision 2026-08-21). Keep `human face`, `facial features`,
`eye contact`, `headshot` OUT of the `[NEG]`. Keep `identifiable person`, `recognisable person`,
`likeness of a real individual` IN — they satisfy the face/likeness family that
`check_image_order_neg.py` requires. `people_plates_min` is **24** in the spec.

**4. `preflight_render_gate.py` is not advisory.** It has failed on 25 of 32 episodes and been
overridden on 10. Green before render, no exceptions.

**5. Codex's image generation is capped at 1672×941** (measured 2026-08-20). The proven route to
3,840 px is `scripts/upscale_oroville_4k_esrgan_v001.py` — Real-ESRGAN x4plus then LANCZOS to
3840×2160. Clone per episode.

## The traps specific to this episode — read all five before writing a line

**1. This topic shares its search terms with an active conspiracy audience** (directed-energy-weapon
claims). **The film must be so specific that it cannot be mistaken for that material, and it must
never gesture at unexplained causes.** The cause is on the record: 6:34 a.m., unmaintained vegetation
by utility pole 25, molten metal from the re-energisation of broken power lines, classified
Accidental. State it plainly and cite it. **The words "some say", "many believe", "questions remain"
and "we may never know" are forbidden** (`⛔-04`) — raising a question and leaving it open is exactly
the register you are being confused with.

**2. Native Hawaiian land with a live cultural and political dimension.** Lahaina was the capital of
the Hawaiian Kingdom. Water rights and diverted streams are part of the record and part of an ongoing
argument — **but no primary source for them has been read**, so they are NOT in the ledger and cannot
be narrated from it (`AB-07`, `⛔-09`). If the film wants that material, source it first. Never use
Hawaiian cultural imagery decoratively. The word "paradise" does not appear in this film.

**3. R3, recent, litigated, and paying out this month.** About a hundred people died in 2023; families
are living. The $4.037 billion settlement's first award notices went out 17 June 2026 and the first of
four annual payments was expected in July or August 2026 — **the month this film publishes**. Every
row in the ledger's section 9 must be re-verified on the day of writing (`⛔-11`). No victim is named,
shown or characterised; no burned vehicle implying anyone inside; no remains, no body bags, no
memorial with a face (`⛔-07`). **Search results for this topic surface victims' names — do not carry
one into any file.**

**4. The visual trap is beauty.** Maui footage on every shelf is holiday footage. The spec already
bars it: 65 `forbidden_subjects` including `resort`, `turquoise water`, `sunset palm`, `luau`,
`surfing`, `drone over hotel`. The era-neutral register is ash, corrugated steel, melted aluminium,
chain-link fence and a standing stone wall — not scenery. `footage_review_required` is true and a
labelled contact sheet must be read by a person before any clip enters a cut.

**5. The ledger has no acreage, no structure count, no wind speed and no evacuation timing.** Those
numbers exist in secondary reporting only and were deliberately left out. **Either source them from
the primary record and add ledger rows, or do not say them** (`⛔-10`, `AB-06`). The death toll is
"at least 102" as the County stated it on 3 October 2024 — never an early figure, never rounded.

## How to read the primary sources (this cost an hour to work out)

`ag.hawaii.gov`, `fsri.org`, `mauicounty.gov` and `mauirecovers.org` all return **403 to WebFetch**.
`curl` with a browser user-agent gets them:

```
curl -sSL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0" -o out.pdf <url>
py -3.11 <scratchpad>/pdftxt.py out.pdf     # pypdf 6.14.2 is installed; pdfminer is not
```

Still unread, and named as unread in `AB-05`: Phase One (375 pages + a 12,000-record minute-by-minute
timeline), Phase Three, and the full MFD/ATF Origin and Cause Report. **Phase One is where the
minute-by-minute of the afternoon lives** — if the script needs the shape of the hours, that is the
document to read, and it is the one gap most likely to be worth closing.

## The binding documents

| what | where |
|---|---|
| how a film must be made | `docs/PD_ONE_PASS_PRODUCTION_SPEC.v3.md` — **v3, not v2** |
| this episode's machine contract | `episodes/PD-2026-075-lahaina/episode_spec.v001.json` — **written; read it, do not rewrite it** |
| what may be said | `episodes/_planning/EP75_lahaina_FACTS_LEDGER.v001.md` — **binding** |
| what may stop a ship | `config/ship_policy.v001.json` — four blocking classes only |
| claim discipline | `.claude/rules/09-claims-and-scripts.md` |
| the worked example to copy | **EP72 `PD-2026-072-lacmegantic`** — film bible, script v003, image order, thumb prompts, scene plan, fact_recheck |

## What to do first, in order

1. **`EP75_lahaina_FILM_BIBLE.v001.md`** — 14 sections, EP72's structure. Controlling idea: the siren.
   Hook **voiced from frame 0 and written FIRST** (spec v3 row 9): a time, a place, one person doing
   one thing, ending on something the subject does not know. **Do not summarise the outcome in it.**
2. Script, sized by `--dry-run`, then `--measure-section ACT_1`, then written to the measurement.
   Section vocabulary is fixed by the spec: HOOK / OP / ACT_1–5 / ENDING. Every factual line carries
   its ledger row id in an HTML comment underneath.
3. Image order (24+ people plates), thumb prompts (≥3), scene plan, fact_recheck.
4. Before any render: `check_episode_inputs.py`, then a **green** `preflight_render_gate.py`.

## The one number to beat

EP72 landed at a **measured 29:44** against a declared 29:00–32:00 band, sized on a measurement
rather than a model. That is the standard for this batch.
