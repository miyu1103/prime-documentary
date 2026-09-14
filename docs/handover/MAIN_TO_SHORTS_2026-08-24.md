# Main thread → Shorts lane, 2026-08-24

**The Shorts calendar runs dry on 29 August at 21:00 JST. Nothing after that is booked.**
Seven finished or nearly-finished long-forms — EP70 through EP76 — have **zero** Shorts between
them. This is the request to build them, with every measurement and every path you need.

Nothing here is a guess. Every number in this file was measured this morning with the command
printed beside it.

---

## 1. What is actually booked, and when it stops

```
py -3.11 scripts/yt_schedule_audit.py
```

| | measured |
|---|---|
| Shorts scheduled, all private with `publishAt` | **24** |
| Last one | **2026-08-29 21:00 JST** |
| Daily Shorts slots | **06:00 / 09:00 / 18:00 / 21:00 JST** — four a day |
| First empty day | **2026-08-30**, and every day after it |
| Long-form slot | 12:00 JST, filled through 8/30 by this thread — do not touch it |

So the runway is **six days**. Four slots a day means **the first genuinely empty slot is
2026-08-30 06:00 JST**, and each further day costs four.

## 2. What has no Shorts at all

```
for d in episodes/PD-2026-07*; do echo "$(basename $d): $(ls $d/09_package/short*_lines.v001.json 2>/dev/null | wc -l)"; done
```

```
PD-2026-070-wronghouse  0        PD-2026-074-itaewon   0
PD-2026-071-oroville    0        PD-2026-075-lahaina   0
PD-2026-072-lacmegantic 0        PD-2026-076-morandi   0
PD-2026-073-uri         0
```

The last Shorts made were **short283–288** (EP60 surfside, EP61 weimer). **Next free number is
289.** At the established three per episode, EP70–76 is **21 Shorts, short289–short309** — five
days of slots, which buys back the runway with a day to spare.

## 3. Where the material is (all seven, exact paths)

| | path |
|---|---|
| finished master | `episodes/<EPID>/08_edit/<slug>_final_bgm.v001.mp4` |
| the film as built | `remotion/src/data/<slug>_film.json` (cuts, figures, captions with timings) |
| narration script | `episodes/<EPID>/03_script/script.en.v001.md` (`[VO:]` lines, and the `(SFX:)` cues) |
| **the facts** | `episodes/_planning/EP<NN>_<slug>_FACTS_LEDGER.v*.md` — **the only place a Short may take a claim from** |
| machine contract | `episodes/<EPID>/episode_spec.v*.json` — **read the HIGHEST revision**, see §5 |
| plates (4K) | `remotion/public/<slug>/img/*.png` |
| i2v motion | `remotion/public/<slug>/motion/*.mp4` |
| reviewed stock | `remotion/public/<slug>/factory/*.mp4` |
| what was rejected and why | `runs/qc/<slug>_clip_verdicts.v001.json`, `runs/qc/<slug>_plate_verdicts.v001.json` |
| captions | `episodes/<EPID>/08_edit/captions.final.v001.srt` |

State of each master, measured:

| slug | master | shipped-frames review |
|---|---|---|
| wronghouse | done, **booked 8/24 12:00** (`1nxecNneBVk`) | PASS, 58 sheets |
| oroville | done | PASS, 61 sheets |
| itaewon | done | not read yet |
| lahaina | done | not read yet |
| morandi | rendering as this is written | not read yet |
| lacmegantic | not rendered — pool QC and figures outstanding | — |
| uri | not rendered — same | — |

**You do not have to wait for a master.** The lines file is written from the SCRIPT and the
LEDGER, so lacmegantic and uri can be designed today.

## 4. The deliverable, unchanged

`episodes/<EPID>/09_package/short<NNN>_lines.v001.json` — a list of line objects, exactly the
shape short282 already has:

```json
{"id": "L1", "delivery": "intense", "source": "rerecord",
 "text": "No one was ever charged with a crime.",
 "provenance": ["No one was ever charged with a crime."]}
```

`provenance` is the sentence in the long-form script or the facts ledger that the line comes
from. **It is not decoration.** A Short states a claim to an audience that has not seen the film,
and `factual_support` is one of the four classes that can stop a ship (`.claude/rules/19`).

Then the usual: `scripts/build_short_design_skeletons.py`, `assemble_short.py`,
`build_short_mix.py`, `verify_short_designs.py`, `verify_short_plates.py`, and
`scripts/daily_shorts_push.sh` for the 16:20 run.

## 5. Six traps measured in the last 24 hours that will bite a Short too

Every one of these cost the long-form line real time today. They are all in shared code, so they
reach you.

1. **Read the HIGHEST spec revision, not `v001`.** `episode_spec.v001.json` was hard-coded in
   19 scripts. lahaina's v001 says `people_plates: null`; its **v003** lists 24. A v001 reader
   builds a film that believes the episode has no faces in it. Use
   `check_episode_spec.spec_path(epdir)` — imported, not restated.
2. **The blocklist matches by STEM, so a rule kills the plate and its clip together.**
   `V003.png` and `V003.mp4` share one id. EP76 blocked 52 hallucinating clips and the same rule
   removed 52 correct plates. Rows now take `"applies_to": ["motion"]`. If you block anything for
   a Short, say which medium.
3. **Sound kinds must come from `ONESHOT_MAP`'s own alias vocabulary.** EP76's plan was written
   as physical description — `stone`, `wind`, `room tone`, `pen` — and **51 of 64 cues resolved
   to no sample**: 0.91 cues/min against a floor of 2.0. The 56 valid aliases are in
   `scripts/build_case_film_audio.py`. Verify by running the mixer with `--dry-run` and reading
   `unmapped=0`, never by counting your own cues.
4. **A dark plate, a dead plate and a plate that is empty ON PURPOSE are three different things.**
   The manifest now measures peak luma and stdev to tell the first two apart, and the third must
   be declared in `episode_spec.intentionally_empty_stills`. A bare ground given a cut of its own
   reads to `blackdetect` as a dropout and stops the render — it happened twice today (EP71 O086,
   EP76 V010) and both were fixed by putting the film's own words on the plate.
5. **cp932.** Printing the blocklist's reason text crashed the whole finisher because a reason
   contains `⛔`. Any script of yours that prints ledger text needs
   `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`.
6. **i2v invents people.** 52 of EP76's 120 clips and 32 of EP70's 160 grew a hand, an arm or a
   face that is not in the plate. Negative prompts and seed changes were measured NOT to fix it
   (16/16 failed). The only thing that works is not sending a plate that has room for a person.

## 6. Quota, and the one rule about the calendar

```
py -3.11 scripts/yt_quota.py --status      # resets at 16:00 JST (Pacific midnight)
```

Daily budget 10,000 units. One long-form upload is 1,650 with its thumbnail; four Shorts are
6,600. **Total 8,250 — it fits, with 1,750 to spare, and only if there is exactly one long-form.**
This thread uploads the long-form at **16:00–16:20**, before your 16:20 automation. Do not add a
second long-form on any day, and if you need more than four Shorts in a day, tell this thread
first so the long-form can move.

**One thread operates the publishing calendar and it is this one** — for the 12:00 long-form slot.
The Shorts automation at 16:20 is yours and stays yours. The line between them is the slot time,
not the tool.

## 7. What would help most, in order

1. **short289–291 for EP70 wronghouse** — it publishes today at 12:00, so its Shorts have the
   most to gain from being close to it.
2. **short292–294 for EP71 oroville** (publishes 8/25).
3. Then itaewon, lahaina, morandi, lacmegantic, uri — the order this thread is booking them in.

If you can only do part of it, do whole episodes rather than one Short each: three Shorts from one
film share a read of the script and the ledger, and that is where the hours go.
