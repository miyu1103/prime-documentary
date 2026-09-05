# EP74 — HANDOVER (paste this into the thread that will design it)

## What this episode is

**EP74 `PD-2026-074-itaewon` — the Itaewon crowd crush, Seoul, 29 October 2022. 30 minutes.**

159 people died in a sloping alley 3.2 metres wide during Halloween crowds. Emergency calls warning
of the danger were made hours before. The question the film is built on is the one PD keeps asking:
**a crowd is a system, and whose job is it?**

## Why it was chosen — the three gates it passed, with numbers

Measured 2026-08-21 with `scripts/topic_demand_probe.py`. **All three gates, not one.**

| gate | result |
|---|---|
| demand ÷ incumbent | median **98,102** views, max 3,094,297, **4 distinct channels above 100k** — R-36 PASS. And **only ONE result over 20 minutes exists, at 446,612 views, and it is in Korean.** The English-language long-form slot is empty |
| producibility | **2022 = contemporary.** 93.5 % of the shelf's playable clips are modern stock. Compare the four period candidates (1911/1987/1988/1989) rejected on 2026-08-21 because the shelf holds 26 clips with a title year in 1955–1985 |
| "this could happen to you" | You go into crowds. The brand test in `config/pd_planning_os.v002.json` is that every episode must land on this, and a crowd in a narrow street lands harder than most |

Do not re-litigate the choice. Do re-run the probe if six months pass.

## The binding documents

| what | where |
|---|---|
| how a film must be made | `docs/PD_ONE_PASS_PRODUCTION_SPEC.v3.md` — **v3, not v2** |
| the machine contract | `episodes/PD-2026-074-itaewon/episode_spec.v001.json` — **not written yet; write it first** |
| the spec standard | `docs/PD_EPISODE_SPEC_STANDARD.v001.md` |
| what may stop a ship | `config/ship_policy.v001.json` — four blocking classes only |
| claim discipline | `.claude/rules/09-claims-and-scripts.md` |
| **the worked example to copy** | **EP72 `PD-2026-072-lacmegantic`** — spec, ledger v001–v003, film bible, script v003, image order, thumb prompts, scene plan, fact_recheck. Same shape, one episode ahead |

## Five things that will cost you a day if you do not know them

**1. `check_script_length` over-counts. Do not size the script with it.** It strips `【…】`, `[…]`,
`(…)` and headings but **not HTML comments**, and every script since EP66 carries a citation comment
under each factual line. Measured inflation: EP69 +2,195 words, EP68 +1,798, EP71 +1,256. On EP72 the
gate read 5,751 words while the TTS extractor saw 4,876 — a four-minute difference in finished film.
**Size with `py -3.11 scripts/gen_narration_case.py --ep <EPID> --dry-run`**, which reports the words
that will actually be spoken.

**2. The registry's 171.79 wpm model is wrong for this register.** EP72 measured **191.7 wpm** —
11 % faster — because PD's house style is short declaratives. Run
`--measure-section ACT_1` (about $1, generates one act and ffprobes it) **before writing to length**.
EP72's prediction from that measurement came within 0.33 % of the delivered master.

**3. Faces are allowed and wanted.** Owner decision 2026-08-21. The `[NEG]` must NOT contain
`human face`, `facial features`, `eye contact`, `headshot`, `profile of a face`. It MUST contain
`identifiable person`, `recognisable person`, `likeness of a real individual` — which also satisfies
the "face / likeness" family that `scripts/check_image_order_neg.py` requires.
**But this episode carries a real carve-out:** see the traps below.

**4. The pre-render gate is not advisory.** `preflight_render_gate.py` has failed on 25 of 32
episodes and been overridden on 10 of them. On 2026-08-20 EP70 and EP71 were both one command from a
three-hour render that would have produced a captionless slideshow. **Green preflight before render,
no exceptions.**

**5. Codex's image generation is capped at 1672×941.** Measured 2026-08-20. It cannot be prompted
out of it. The proven route to the required 3,840 px long edge is
`scripts/upscale_oroville_4k_esrgan_v001.py` — Real-ESRGAN x4plus to 6688×3764, then LANCZOS down to
exactly 3840×2160. Clone it per episode. A plain 2× enlargement does not clear the floor.

## The traps specific to this episode

**R3, and the hardest likeness problem PD has had.** 159 people died, they were mostly in their
twenties, they are named in public reporting, and their families are living and politically active.

- **No victim is named, shown or characterised.** No face in a crowd plate may be built from, or
  resemble, any real person who was there.
- **The crowd is the subject and it must have faces** — a faceless crowd is both dishonest and
  visually dead — **but every face must be manifestly invented.** Prefer: crowds at distance and in
  motion blur; partial faces at the frame edge; faces lit from behind; the backs of heads with a few
  turned three-quarters. Never a held close-up of one person's face in the alley.
- **Never depict the crush itself.** No compressed bodies, no people on the ground, no CPR, no
  stretchers, no blood. The alley is shown empty, or full and ordinary, or after. The event is
  carried by sound, by the width of the walls, and by the gradient.
- **Korean signage must be Korean and unreadable.** A Japanese or Chinese shopfront in an Itaewon
  plate is the same class of error as an EU number plate in a Texas film.

**The accountability record is contested and partly ongoing.** Officials were charged; outcomes have
moved through the courts over several years. **Verify the current legal status of every named
official from a primary or named-outlet source at the time you write, and state it in the same
breath as any description of them.** This is `⛔-01` in EP72's ledger, transplanted — and the reason
EP72's title, thumbnail and description all had to survive being read cold.

**The special-investigation and parliamentary record is in Korean.** Budget research time for it and
do not narrate an English secondary summary as though it were the record.

## What to do first, in order

1. `episode_spec.v001.json` — copy EP72's shape. Runtime `[1740, 1920]`. `script_words` **[4900,
   5400]**, not EP72's [4600,4800], because of the measured pace. `people_plates_min` 24.
   `era_setting` must bar: European and American streets, Japanese and Chinese signage, daytime-clean
   crowds, festival imagery that reads as celebration. Validate with
   `py -3.11 scripts/check_episode_spec.py --slug itaewon`.
2. `FACTS_LEDGER.v001` — every row graded VERBATIM / OURS / SECONDARY / ABSENCE, with a ⛔ quarantine
   section. Load-bearing rows need a primary source; the special investigation report and the court
   record, not a news summary of them.
3. `FILM_BIBLE.v001` — 14 sections, EP72's structure. The controlling idea is the same family:
   nobody's job. The hook is **voiced from frame 0 and written FIRST** (spec v3 row 9), 0:00–0:20,
   a time, a place, one person doing one thing, ending on something the subject does not know.
4. Script, then `--measure-section`, then write to the measurement.
5. Image order, thumbnails, scene plan, fact_recheck.

## The one number to beat

EP72 landed at a **measured 29:44** against a declared band of 29:00–32:00, from a script sized on a
measurement rather than a model. That is the standard for this batch.
