# EP75 — HANDOVER (paste this into the thread that will design it)

## What this episode is

**EP75 `PD-2026-075-lahaina` — the Lahaina fire, Maui, 8 August 2023. 30 minutes.**

A wind-driven fire destroyed a town and killed about a hundred people. Hawaii owns **the largest
outdoor siren network in the world**, and on the day it was needed **it was not sounded**. The film
is about a warning system that existed, was paid for, was tested monthly, and did not fire.

## Why it was chosen — the three gates, with numbers

Measured 2026-08-20/21 with `scripts/topic_demand_probe.py`.

| gate | result |
|---|---|
| demand ÷ incumbent | median **90,938** views, max **3,527,309**, 4 videos above 100k across 2 channels — R-36 PASS at the line. The decisive number: **the biggest result over 20 minutes is 74,091 views.** Ratio **1.23** — the emptiest documentary slot on the whole measured slate |
| producibility | **2023 = contemporary.** The shelf is 93.5 % modern stock and this register — a Pacific small town, cars, a shoreline road, a burnt lot — sits in its strong half |
| "this could happen to you" | An evacuation warning is a thing every viewer assumes will reach them |

**The R-36 pass is at the line — 2 channels, not 5 or 8.** That is the weakest number in this
episode's case and it should be re-probed if the build slips by months.

## The binding documents

| what | where |
|---|---|
| how a film must be made | `docs/PD_ONE_PASS_PRODUCTION_SPEC.v3.md` — **v3, not v2** |
| the machine contract | `episodes/PD-2026-075-lahaina/episode_spec.v001.json` — **not written yet; write it first** |
| the spec standard | `docs/PD_EPISODE_SPEC_STANDARD.v001.md` |
| what may stop a ship | `config/ship_policy.v001.json` — four blocking classes only |
| claim discipline | `.claude/rules/09-claims-and-scripts.md` |
| **the worked example to copy** | **EP72 `PD-2026-072-lacmegantic`** — spec, ledger v001–v003, film bible, script v003, image order, thumb prompts, scene plan, fact_recheck |

## Five things that will cost you a day if you do not know them

**1. `check_script_length` over-counts. Do not size the script with it.** It does not strip HTML
comments, and every script since EP66 carries a citation comment under each factual line. Measured
inflation: EP69 +2,195 words, EP68 +1,798, EP71 +1,256. On EP72 it read 5,751 while the TTS
extractor saw 4,876 — four minutes of finished film. **Size with
`gen_narration_case.py --ep <EPID> --dry-run`.**

**2. The registry's 171.79 wpm model is 11 % slow for this house style.** EP72 measured **191.7 wpm**.
Run `--measure-section ACT_1` (~$1) **before writing to length**; EP72's projection from that
measurement came within 0.33 % of the delivered master.

**3. Faces are allowed and wanted** (owner decision 2026-08-21). Keep `human face`, `facial
features`, `eye contact`, `headshot` OUT of the `[NEG]`. Keep `identifiable person`,
`recognisable person`, `likeness of a real individual` IN — they satisfy the face/likeness family
that `check_image_order_neg.py` requires.

**4. `preflight_render_gate.py` is not advisory.** It has failed on 25 of 32 episodes and been
overridden on 10. Green before render, no exceptions.

**5. Codex's image generation is capped at 1672×941** (measured 2026-08-20). The proven route to
3,840 px is `scripts/upscale_oroville_4k_esrgan_v001.py` — Real-ESRGAN x4plus then LANCZOS to
3840×2160. Clone per episode.

## The traps specific to this episode — read all four before writing a line

**1. This topic is adjacent to an active conspiracy audience.** The same search terms are used by
people asserting the fire was started by a directed-energy weapon. **The film must be so specific
that it cannot be mistaken for that material, and it must never gesture at unexplained causes.**
Cause and spread are documented; stay on the record and cite it. Do not "raise questions" as a
rhetorical device — that is the register of the thing you are being confused with.

**2. It is Native Hawaiian land with a live cultural and political dimension.** Lahaina was the
capital of the Hawaiian Kingdom. Water rights and diverted streams are part of the record and part
of an ongoing argument. **Handle both as documented facts with attribution, never as colour.** Do not
use Hawaiian cultural imagery decoratively; do not use the word "paradise".

**3. R3, recent, and litigated.** About a hundred people died in 2023; families are living; a very
large settlement has been negotiated and challenged. **Verify the current status of every legal claim
at the time of writing.** No victim is named, shown or characterised. No burned vehicle with a
person implied inside. No human remains, no body bags, no memorials with faces.

**4. The visual trap is beauty.** Maui footage on any shelf is holiday footage — turquoise water,
palms, sunsets, drone-over-resort. **This film is grey smoke, a shoreline road, a burnt lot, a
chain-link fence.** Put `resort`, `beach holiday`, `turquoise water`, `sunset palm`, `luau`,
`surfing`, `drone over hotel` in `forbidden_subjects`, and be aware that the era-neutral register
here is ash, corrugated steel, melted aluminium and a standing stone wall — not scenery.

## What to do first, in order

1. `episode_spec.v001.json` — copy EP72's shape. Runtime `[1740, 1920]`. `script_words` **[4900,
   5400]** because of the measured pace. `people_plates_min` 24. `era_setting` bars the holiday
   register above and any mainland-US or European street. Validate with
   `check_episode_spec.py --slug lahaina`.
2. `FACTS_LEDGER.v001` — the load-bearing rows are the siren system (what it exists for, who may
   sound it, what was decided that day), the utility's lines and the power-shutoff question, the
   water-access dispute, the official after-action review, and the death toll. **Primary sources for
   each; the state's own reports and the utility's filings, not a news summary of them.**
3. `FILM_BIBLE.v001` — 14 sections, EP72's structure. Hook **voiced from frame 0 and written FIRST**
   (spec v3 row 9): a time, a place, one person doing one thing, ending on something the subject does
   not know. The controlling idea should be the siren — a system that was maintained and not used.
4. Script → `--measure-section` → write to the measurement.
5. Image order, thumbnails, scene plan, fact_recheck.

## The one number to beat

EP72 landed at a **measured 29:44** against a declared 29:00–32:00 band, sized on a measurement
rather than a model. That is the standard for this batch.
