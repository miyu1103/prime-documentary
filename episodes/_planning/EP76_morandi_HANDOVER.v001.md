# EP76 — HANDOVER (paste this into the thread that will design it)

## What this episode is

**EP76 `PD-2026-076-morandi` — the Morandi bridge collapse, Genoa, 14 August 2018. 30 minutes.**

A motorway viaduct that a city drove across every day dropped about 200 metres of deck into the
valley beneath it. Forty-three people died. The bridge had been in service since 1967, its condition
had been the subject of engineering argument for decades, and it was operated under a private
motorway concession.

**The subject of the film is the thing the viewer does without thinking: driving over a structure
somebody else is responsible for inspecting.**

## Why it was chosen — the three gates, with numbers

Measured 2026-08-21 with `scripts/topic_demand_probe.py`, against three candidates that failed.

| gate | result |
|---|---|
| demand ÷ incumbent | median **90,124** views, max 800,009, **5 distinct channels above 100k** — R-36 PASS. Seven results run over 20 minutes but **the biggest of them is 188,464 views**. Ratio **0.48** |
| producibility | **2018 = contemporary.** The shelf is 93.5 % modern stock. And uniquely in this batch, **Italy makes the shelf's European bias an advantage** — for EP73 (Texas) a European street is an error; here it is correct |
| "this could happen to you" | You drove over a bridge today |

Rejected against it, same session: Ghost Ship warehouse fire (median 2,575, **zero** channels above
100k), Turkey earthquake building amnesty (median **23**, one channel). Hard Rock Hotel collapse
could not be measured — the API rate-limited — and is the one candidate worth probing if this
episode is ever reconsidered.

**Read the saturation number honestly.** Seven long-form videos already exist. This is not an empty
slot like EP75 Lahaina (biggest long-form 74,091 against a 3.5M-view demand). It is a **crowded slot
that nobody has won** — the field's best is 188k against a median of 90k. That is a different bet:
it says the audience is there and no one has made the definitive film, not that no one has tried.

## The binding documents

| what | where |
|---|---|
| how a film must be made | `docs/PD_ONE_PASS_PRODUCTION_SPEC.v3.md` — **v3, not v2** |
| the machine contract | `episodes/PD-2026-076-morandi/episode_spec.v001.json` — **not written yet; write it first** |
| the spec standard | `docs/PD_EPISODE_SPEC_STANDARD.v001.md` |
| what may stop a ship | `config/ship_policy.v001.json` — four blocking classes only |
| claim discipline | `.claude/rules/09-claims-and-scripts.md` |
| **the worked example to copy** | **EP72 `PD-2026-072-lacmegantic`** — spec, ledger v001–v003, film bible, script v003, image order, thumb prompts, scene plan, fact_recheck |

## Five things that will cost you a day if you do not know them

**1. `check_script_length` over-counts. Do not size the script with it.** It does not strip HTML
comments, and every script since EP66 carries a citation comment under each factual line. Measured
inflation: EP69 +2,195 words, EP68 +1,798, EP71 +1,256. On EP72 the gate read 5,751 words while the
TTS extractor saw 4,876 — four minutes of finished film. **Size with
`gen_narration_case.py --ep <EPID> --dry-run`**, which reports the words that will be spoken.

**2. The registry's 171.79 wpm model is 11 % slow for this house style.** EP72 measured **191.7 wpm**.
Run `--measure-section ACT_1` (~$1, one act, ffprobed) **before writing to length**. EP72's
projection from that measurement came within 0.33 % of the delivered master.

**3. Faces are allowed and wanted** (owner decision 2026-08-21). Keep `human face`, `facial
features`, `eye contact`, `headshot`, `profile of a face` OUT of the `[NEG]`. Keep
`identifiable person`, `recognisable person`, `likeness of a real individual` IN — they satisfy the
face/likeness family that `check_image_order_neg.py` requires.

**4. `preflight_render_gate.py` is not advisory.** It has failed on 25 of 32 episodes and been
overridden on 10. On 2026-08-20, EP70 and EP71 were each one command away from a three-hour render
of a captionless slideshow. Green before render, no exceptions.

**5. Codex's image generation is capped at 1672×941** (measured 2026-08-20; it cannot be prompted
out of it). The proven route to the required 3,840 px long edge is
`scripts/upscale_oroville_4k_esrgan_v001.py` — Real-ESRGAN x4plus to 6688×3764, then LANCZOS to
exactly 3840×2160. Clone it per episode. A plain 2× enlargement does not clear the floor.

## The traps specific to this episode

**1. The record is in Italian, and the load-bearing part of it is technical.** The engineering
argument about this structure — its stay cables, their concrete encasement, what could and could not
be inspected, and what reports said when — is the film's spine and it exists in Italian technical and
judicial documents. **Do not narrate an English secondary summary as though it were the record.**
Budget research time for the Italian sources, and grade every row honestly: a news article about a
report is SECONDARY, not the report.

**2. A criminal trial has been running against executives and officials.** Verify, at the time of
writing, exactly who has been charged, convicted, acquitted or is still on trial — and **state that
status in the same breath as any description of them**. This is EP72's `⛔-01` transplanted, and it
is the rule that governs the title, the thumbnail text and the description as much as the narration.
Italy's appeal structure means a first-instance outcome is not a final one; say which stage you are
describing.

**3. Never state as fact that the collapse was foreseen.** "The designer warned about corrosion" is
the sentence every retelling reaches for, and it is exactly the kind of claim that needs the primary
document behind it, with its date, its subject and its scope. **If the record supports a narrower
statement, narrate the narrower statement.** EP72 handled the same temptation with a
`forbidden_claims` entry; do the same here.

**4. Never depict the fall, the vehicles, or the dead.** Forty-three people died and their families
are living. The collapse is shown as the gap afterwards, as scale, as a severed road with a barrier
across it. No falling car, no wreckage with a person implied inside, no rescue, no funeral, no
memorial with faces.

**5. The signage rules invert.** For EP73 (Texas) a European street is an error; here **Italian
signage is correct and American signage is the error**. Italy drives on the right, so
right-hand-drive traffic is still wrong. Put `US route shield`, `american highway sign`,
`right-hand-drive traffic`, `UK street`, `asian street` in `forbidden_subjects`, and keep Italian
lettering unreadable rather than absent — a Ligurian street with no writing anywhere reads as a set.

**6. The replacement bridge is a real ending and it is not a consolation.** A new viaduct was built
and opened quickly. Use it as fact, not as uplift, and do not let it resolve the film's argument —
the argument is about who is responsible for the inspection of a thing you drive across, and a new
bridge does not answer that.

## What to do first, in order

1. `episode_spec.v001.json` — copy EP72's shape. Runtime `[1740, 1920]`. `script_words` **[4900,
   5400]** because of the measured pace, not EP72's [4600,4800]. `people_plates_min` 24.
   `era_setting`: Genoa and Liguria, 1967–2020s; Italian signage; Mediterranean port city, hills,
   viaducts, tunnels; bar the American and British registers and the holiday-Italy register
   (Tuscany, vineyards, Amalfi, gondolas — wrong city, wrong film). Validate with
   `py -3.11 scripts/check_episode_spec.py --slug morandi`.
2. `FACTS_LEDGER.v001` — grade every row VERBATIM / OURS / SECONDARY / ABSENCE, with a ⛔ quarantine
   section. Load-bearing rows are the structure's design and condition history, the inspection
   regime, the concession, the day itself, the death toll, and the legal outcomes. Primary Italian
   sources for each.
3. `FILM_BIBLE.v001` — 14 sections, EP72's structure. Hook **voiced from frame 0 and written FIRST**
   (spec v3 row 9): a time, a place, one person doing one thing, ending on something the subject does
   not know. Five hero objects; one per act.
4. Script → `--measure-section ACT_1` → write to the measurement.
5. Image order (~120 plates), thumbnails, scene plan, fact_recheck.

## The one number to beat

EP72 landed at a **measured 29:44** against a declared 29:00–32:00 band, from a script sized on a
measurement rather than a model. That is the standard for this batch.
