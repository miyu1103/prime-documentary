# Handover — 2026-08-25 evening, the build/publish lane

This session held the publishing calendar. Whoever picks this up holds it next. **Exactly one
session schedules.** Nothing below is a plan; every number was measured.

---

## 1. Where the calendar actually stands

```
8/26 12:00  EP74 itaewon   RFDPSfllbk0   BOOKED, processed/succeeded, 0 problems
8/27 12:00  EP75 lahaina   master done 23:02, NOT yet QC'd or booked   <-- next job
8/28 12:00  EP76 morandi   re-render RUNNING (started 23:06)
8/29 12:00  EP72 lacmegantic   never rendered
8/30 12:00  EP73 uri           never rendered
8/31+       EMPTY on every slot
```

Shorts are held **indefinitely** (`config/shorts_pause.v001.json`, `paused_until 2026-12-31`,
set by the shorts lane on owner's decision). The Windows task `PD-ShortsPush` still shows
`Ready` and fires at 16:20 — it reads the pause and uploads nothing. That is expected; do not
"fix" it.

Consequence the owner should keep in view: after 8/30 there is no long-form left and no Shorts
either. 8/31 has one Short at 06:00 and then the channel goes quiet until EP77+ arrive.

---

## 2. The immediate job, in order

**a. Book EP75 lahaina for 8/27.** The master is `episodes/PD-2026-075-lahaina/08_edit/
lahaina_final_bgm.v001.mp4`, 2,658 MB, 31:06, written 23:02, POST-RENDER GATE **PASS**.
Nothing has been QC'd yet. The chain, exactly as it ran for itaewon tonight:

```
py -3.11 scripts/check_shipped_frames.py --slug lahaina --which-master     # confirm the bytes
py -3.11 scripts/check_shipped_frames.py --slug lahaina --sheets-only --force
   -> READ EVERY SHEET, tile by tile. ~55 sheets, ~35 min. Do not skip this.
   -> write runs/qc/lahaina_shipped_frames_review.v001.json with reviewed_sheets
      and render_sha256 bound to THOSE bytes
py -3.11 scripts/check_shipped_frames.py --slug lahaina                     # must say PASS
py -3.11 scripts/write_final_delivery.py --slug lahaina --render <the mp4>
py -3.11 scripts/check_final_acceptance.py 75 --emit-receipt                # ~12 min
py -3.11 scripts/upload_schedule_case_v001.py --ep lahaina --explain-policy # want blocking=0
py -3.11 scripts/upload_schedule_case_v001.py --ep lahaina --dry-run
py -3.11 scripts/upload_schedule_case_v001.py --ep lahaina                  # ~15 min for 2.7GB
py -3.11 scripts/yt_video_status.py --slug lahaina                          # channel is the truth
```

Before the real upload, **read the title against the film by hand**. The policy says a green
from `check_packaging_claims` is not a substitute, and it is right. For itaewon this took one
grep and found all three claims stated verbatim in `script.en.v001.md`.

**b. When morandi's finisher exits, do the same for it, and start lacmegantic immediately.**
Never let the GPU idle: start the next `_finish_episode.sh` first, then QC the one that just
landed. The two do not compete.

```
bash scripts/_finish_episode.sh lacmegantic Ep72Lacmegantic 72 > out_finish_lacmegantic.log 2>&1
bash scripts/_finish_episode.sh uri Ep73Uri 73 > out_finish_uri.log 2>&1
```

**c. Quota.** An upload costs ~1,650 units of 10,000, and the day resets at **16:00 JST**.
itaewon spent one today. Four more tonight is 6,600, which fits, but leaves ~1,750 spare — so
push **uri's upload past 16:00 JST on 8/26** into the fresh quota day rather than squeezing it in.
Note: the ledger in `handover_snapshot.py` did **not** move after tonight's upload (still 1,488).
Treat its number as a floor, not the truth.

---

## 3. Measured cost per episode (use these for planning, not estimates)

```
finisher end to end, including the render   2h 36m   (itaewon, 56,874 frames, 15:06 -> 17:42)
render rate                                 ~755 frames/min
sheets extraction                           11 min
reading 55 sheets tile by tile              ~35 min
final_delivery + acceptance receipt         ~15 min
upload 3 GB + verify on the channel         ~15 min
--------------------------------------------------
GPU-bound per episode                       ~2h 40m
my own work per episode (GPU free)          ~1h 15m
```

Pipelined, the GPU is the limit: ~9/day in theory. With the re-render rate actually observed
tonight (1 of 4), plan on **4 a day**.

---

## 4. What went wrong tonight and what now prevents it

**EP75 lahaina failed its POST-RENDER GATE on three black stretches after a 2.5-hour render.**
All three came from one clip, `lahaina/motion/H014.mp4`: a 3.37s exposure ramp, luma YAVG
28 -> 110, whose first 1.20s ffmpeg calls black. A cut loops a ~3.4s source into ~6.3s, so that
one head became **two** holes per cut, and the builder used it twice. Its 81 generated frames
are faithful — the source plate is itself near-black. A dark plate, not an i2v failure.

Three instruments and one of my own moves were wrong along the way. All four are worth knowing:

1. **`check_motion_saturation` had measured H014 that afternoon and passed it** — s10=0.10,
   s50=17.8, s90=32.0. Chroma *rising* from zero is not a collapse, and the check only ever
   asked about direction. It now also runs ffmpeg `blackdetect` at the same pixel threshold the
   post-render gate uses, and is deliberately stricter than the gate it forecasts: 0.40s at the
   head, 0.80s elsewhere, against the gate's 1.2s. Demonstrated both ways.
2. **Hand-quarantining the clip did not hold.** Finisher step `[1/7]` re-assembled it from
   `ae-demo/wan_frames_lahaina_H014/`, and `[2b/7]` pruned nothing because
   `pd_footage_blocklist` reads `blocked` and nothing else — the row had gone into
   `quality_deferred`, which binds nothing.
3. **Renaming the frame dir in place made it worse.** The assembler takes the clip name FROM
   THE DIRECTORY, so it produced `motion/H014_black_head_rejected_20260825.mp4`: the same bad
   clip back in the pool under a name no blocklist row matched. **A rejected frame dir has to
   leave `ae-demo` entirely.** They now live in `E:/pd-media/_rejected_i2v_frames/`.
4. **The E: archive restores what you remove from the pool.** `[2/7]` copies
   `E:/pd-media/assets/ai_video/<slug>/motion/` into the render-visible dir. Remove from both.

Each of those was caught at `[3/7]`, before the GPU was spent. Only the first render was wasted.

`config/footage_blocklist.v001.json` gained a fifth category, **`cat5_build_breaking_asset`** —
an asset a gate refuses, so leaving it in the pool costs a render every run. This is NOT a
re-opening of the taste rejects demoted on 08-05; those were demoted because enforcing them
emptied the calendar, and a build-breaking file empties it too. Rows of this kind must be
episode-scoped: `H014` names a different picture in other episodes.

---

## 5. The next three episodes were measured BEFORE their renders

```
morandi      68 clips   clean
lacmegantic 120 clips   2 bad -- both removed
uri         120 clips   clean
```

`lacmegantic/motion/L092.mp4` is black from 0.43s to 3.33s of a 3.37s clip — 87 per cent. At
full frame it is the edge of a curtain for two tenths of a second and then nothing.
`L010.mp4` opens with 0.77s of black and at 2.5s also carries a person facing camera with
legible features — the i2v-invents-people defect. Neither was visible at contact-sheet scale.
Both are out of the public pool and the E: archive, blocked episode-scoped, frame dirs moved
out of `ae-demo`. That is two renders that will not have to be thrown away.

**Run this before every render from now on:**

```
py -3.11 scripts/check_motion_saturation.py --slug <slug>
```

---

## 6. EP74 itaewon: what was actually shipped

55 sheets read tile by tile, 1,098 frames from 272 cuts, coverage complete 0:00–31:35.
**Zero** wrong-country footage — which was the whole point of the rebuild, after three episodes
running shipped Seoul with Shenzhen, Moscow and Taipei in it. Zero held identifiable faces,
zero bodies, zero readable records, zero depth maps as picture. ComparisonBars renders
28,437 / 31,878 / 51,585 / 81,573 with separators and no NaN; 31,878 matches
`script.en.v001.md:80` and `film.json` exactly.

Receipt v004 is `status=FAIL` with 9 hard failures and the policy still says `permit`,
`blocking=0`, because none of them is in the four classes. **They are recorded, not excused**,
in `09_package/release_deviations.v001.json`. The ones worth fixing in the next episodes:

- 87 hero stills linger over 5s (cap 8, longest 7.1s) — still-dependent, reads as 紙芝居
- 53.7% of 95 stills are too dark (median luma < 45; allowance 40%)
- caption p90 lag +0.47s against a +0.35s limit
- the script is body-first: no HOOK section, no re-hook beat in 2,042s, no question for 976s
- 2 of 272 cut assets are byte-identical to assets in EP76 morandi

One soft finding was recorded rather than rejected: cut0105 (12:15–12:21) uses a clip whose
filename contains `huangpu` (Shanghai) while the frames are unmistakably a Korean folk village.
Rename or replace it before that clip is reused; re-rendering 31 minutes for a 7-second shot
whose pixels are correct is not a trade worth making.

---

## 7. Lane boundaries as of tonight

- **This lane**: assemble, render, read the shipped frames, book. Also holds the calendar.
- **Design lane (new thread as of tonight)**: EP77–85 up to `check_episode_inputs --slug <slug>`
  printing **READY to build**. Anything short of that gets sent back without spending the GPU.
- **Shorts lane**: paused indefinitely; owns `config/shorts_pause.v001.json`.

**Image counts, measured tonight — the previous design thread's "EP82 has 0 images" is wrong:**

```
EP77 keybridge  131/121   EP78 colgan  168/136   EP79 alaska261 198/192
EP80 concordia  185/181   EP81 station 188/188   EP82 valdez    183/184  (1 short)
EP83 max737     188/188   EP84 threemile 186/186
EP85 katrina    100/186   (86 short)  <-- the only real gap
```

Also unresolved and not this lane's to fix: **`PD-2026-078-colgan` and `PD-2026-078-fukushima`
carry the same episode number.** `fukushima` is empty.

---

## 8. When Shorts can resume alongside long-form

The arithmetic works — one long-form (1,650) plus four Shorts (6,600) is 8,250 of 10,000. What
failed on 8/25 was ordering, not capacity: the long-form was not ready at 16:05 and the Shorts
push spent the allowance by 16:20. `daily_shorts_push.sh` already takes a `--reserve` argument
that holds back 1,650 per episode due that day, **but its default is 0**. Two changes make
resumption safe, and neither needs a waiting period:

1. default `--reserve` to 1650 (3300 to be safe)
2. make the Shorts push refuse to run until the day's long-form upload has actually **succeeded**
   — today it is only ordered by clock time, so a failed long-form is silently skipped over

Not implemented. Owner's call when to resume.

---

## 9. Tooling changed tonight

- `scripts/check_motion_saturation.py` — black-head/black-body detection added, `--selftest`
  proves 9 cases both directions
- `scripts/check_image_order_spec.py` — reads THUMBNAIL orders too, and its forbidden-subject
  matcher no longer fires on `rio` inside `interior`, `rome` inside `chrome`, `paris` inside
  `comparison`. It still fires on `nobody present` and `bodywork`, which is the original reason
  the file exists. `--selftest` proves 9 cases. This cleared a false red on all three EP83–85
  plate orders.
- Found by that tool and not yet acted on by anyone: **EP85 katrina's thumbnail candidate T04
  was ordered as "a bus yard of yellow school buses standing up to their windows in dark
  floodwater", and that episode's own spec forbids `school bus`, `buses in floodwater` and
  `abandoned bus`.** It was generated, reviewed, and recommended by the thumbnail lane. Do not
  select it. `check_packaging_claims` passes its headline "THEY NEVER MOVED." only because the
  script contains the sentence "Nothing in the record moved," which is about the record, not
  about buses.

Commits: `c738ef28`, `3716d669`, `dc8e4448`, `31b99e2f`, `f2b56f06`.
