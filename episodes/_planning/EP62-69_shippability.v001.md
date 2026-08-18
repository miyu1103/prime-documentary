# EP62–69 — what stands between each episode and a legitimate scheduled upload

Measured 2026-08-11 23:50 → 2026-08-12 02:00 JST, read-only, on this machine.
Nothing was killed, no render was started, no gate flag was weakened, **no acceptance receipt was emitted**
(verified: receipt mtimes in `09_package/` unchanged by this audit except `marmet` v006, which a
*different* session wrote at 00:58 — see §EP65).

Rule applied: `.claude/rules/19-ship-gate.md` — publish only when an independent gate has measured the
real bytes and the receipt's `video_sha256` equals the file on disk, and every remaining hard failure is
named in an `approvals/*.json` with `target_type: "edit"`.

---

## 0. Machine state during the audit (context for every number below)

An unattended queue (`scripts/queue_unattended.sh`, PID 61944, started 2026-08-11 22:03:51) was live.
It rendered **EP65 marmet** while this audit ran and finished mid-audit:

```
CL : bash /tmp/pdq.WhHBPr/_finish_episode.sh marmet Ep65Marmet 65 --allow-video-diversity-deviation
[finish:marmet] [6/7] guarded render -> out/marmet.mp4 (expect 1902.2s)
Encoded 57066/57066
[finish:marmet] DONE Wed Aug 12 00:38:45 2026 -> episodes/PD-2026-065-marmet/08_edit/marmet_final_bgm.v001.mp4
```

**Measured wall-clock for one full episode finish**: 22:45:43 → 00:38:45 = **1 h 53 m**
(render proper 22:59:06 → 00:30:27 = 1 h 31 m). The brief's "~3 h each" is conservative; ~2 h is the
observed cost on this box. Note the queue's own busy-detector counts `check_final_acceptance`, so this
audit's measurement runs held the queue idle-waiting; that is safe (it cannot start a second render on
top of a live one) but it did delay greene's start by roughly one hour.

The queue's own re-render rule (`queue_unattended.sh`) is: skip if a master exists **and** its
`film.json` is *older* than the master. Evaluated now:

```
greene: RE-RENDER (film.json NEWER than master -> queue WILL render)
correa: RE-RENDER (film.json NEWER than master -> queue WILL render)
memphis: SKIP     (film.json older than master -> queue will NOT re-render)
marmet: RE-RENDER (film.json NEWER than master)   <-- executed tonight, now complete
openfields/ramirez/pinto/hyatt: RENDER (missing master)
```

```
remotion/src/data/greene_film.json      2026-08-11 01:46:06   vs master 2026-08-10 17:15:15
remotion/src/data/correa_film.json      2026-08-11 20:57:07   vs master 2026-08-10 22:17:26
remotion/src/data/memphis_film.json     2026-08-11 02:42:47   vs master 2026-08-11 04:18:54
remotion/src/data/marmet_film.json      2026-08-11 22:50:39   vs master 2026-08-10 10:16:11 (now rebuilt)
```

**The repository itself already classifies the greene and correa masters as superseded.** That is not an
opinion; it is the queue's rule evaluated against file mtimes.

---

## 1. The three 2026-08-11 fixes, and which masters predate them

| Fix | Where it lives | Landed (mtime) |
|---|---|---|
| 4-layer audio mux bound into the container | `scripts/build_case_film_mux.py` | 2026-08-11 20:15:58 |
| caption lead **measured** from the filmconfig, not hard-coded | `scripts/_finish_episode.sh` `[4b]`, `scripts/polish_captions_srt.py` | 2026-08-11 21:55:31 / 22:03:27 |
| `[4a]` mandatory-plate gate that could never fire | `scripts/_finish_episode.sh` `[4a]` | 2026-08-11 22:03:27 |

All three are **uncommitted working-tree changes** (`git status --short scripts/` shows
` M scripts/_finish_episode.sh`, ` M scripts/build_case_film_mux.py`), so the mtime is the only
timestamp — but it is a real one, and it is unambiguous.

The `[4a]` fix documents its own defect in the file:

> THE GUARD BELOW USED TO BE UNABLE TO FIRE. It searched `grep "^\[satisfied\]" | tail -4`, but
> check_spec_satisfied prints its failures as detail lines beginning with two spaces and a dash […]
> Measured on EP66 openfields, whose film is missing 96 of 185 purpose-made plates: the guard did not die.
> **Every episode since this was written rendered unprotected by the very check whose comment above lists
> three defects it exists to catch.**

### The decisive evidence: the container audio tag

`build_case_film_mux.py` stamps `audio_mix_sha256` into the mp4. Absence of the tag proves the built
4-layer mix was never muxed in — the render carries Remotion's own audio.

```
greene_final_bgm.v001.mp4   TAG:comment=Made with Remotion 4.0.476        <-- NO audio_mix_sha256
correa_final_bgm.v001.mp4   TAG:comment=Made with Remotion 4.0.476        <-- NO audio_mix_sha256
memphis_final_bgm.v001.mp4  TAG:comment=Made with Remotion 4.0.476        <-- NO audio_mix_sha256   [THIS IS THE FILE ALREADY UPLOADED]
memphis_final_bgm.v002.mp4  TAG:audio_mix_sha256=3a458fa9a24505f6…        <-- present
marmet_final_bgm.v001.mp4   TAG:audio_mix_sha256=afc6df687ea44e77…        <-- present (old and new master both)
```

**Verdict on Q6, per file, from the files:**

| Master | Rendered | Predates the 3 fixes? | Safe to ship the old master? |
|---|---|---|---|
| greene v001 | 2026-08-10 17:15 | **Yes, all three** | **No.** No 4-layer audio; `film.json` + captions replaced after it was made; queue itself says RE-RENDER. Only the new render is shippable. |
| correa v001 | 2026-08-10 22:17 | **Yes, all three** | **No.** Same three reasons. Only the new render is shippable. |
| memphis v001 | 2026-08-11 04:18 | **Yes, all three** | It is **already scheduled**. Measured today it has no *uncovered* content failure — but its audio is not the 4-layer mix. **v002 is strictly better and was never uploaded.** See §EP64. |
| memphis v002 | 2026-08-11 20:25 | Postdates the audio-mux fix only | Yes on the numbers — 2 hard fails, both APR-0002. Blocked only by paperwork. |
| marmet v001 (old) | 2026-08-10 10:16 | Yes | Moot — **overwritten tonight at 00:36:19**. |
| marmet v001 (new) | 2026-08-12 00:36 | **Postdates all three** | Yes on the numbers; blocked by a receipt that measured the wrong file. See §EP65. |

### One thing the owner must be told plainly

`animation_density` now **passes** for greene (3.3% / 3.7 s), correa (1.2% / 3.8 s) and memphis
(3.0% / 3.1 s). It did not pass in August 10–11. The film bytes did not change — **the limit did**:

```
git diff scripts/check_final_acceptance.py
-LOW_MOTION_MAX_SPAN_S = 3.0    # any single near-still hold beyond this fails
+LOW_MOTION_MAX_SPAN_S = 4.0    # one designed hold, same as MAX_FREEZE_LONGEST_S
```

The change carries a written derivation (the file already allowed a *fully frozen* 4.0 s beat via
`MAX_FREEZE_LONGEST_S` while failing a *near-still* 3.1 s one — an internal contradiction), and it was
made after three separate owner round-trips. It is defensible. But it is a threshold that was loosened
on 2026-08-11 17:06 and it is the reason three APR-0003 approvals are now redundant. **Flagging it
because the standing rule is that a gate is never relaxed to make something pass — the owner should
confirm this one, not inherit it.**

---

## 2. Per-episode findings

### EP62 greene — needs the re-render the queue is about to do

**1. Master.** `episodes/PD-2026-062-greene/08_edit/greene_final_bgm.v001.mp4`
```
size 1,866,987,394 B (1.74 GiB)   mtime 2026-08-10 17:15:15
duration=1861.533333 (31.03 min)  h264 1920x1080 30/1 + aac stereo   bit_rate=8,023,439
sha256 0a8fa23d1b0ca61ade61bd34e917c6b3e2875ef9ffd8411b6b6ad93e0e60efae
```
sha cost: this file was one of four hashed in a single 6.97 GB batch that took **19.96 s** total, so
roughly 5 s. Cheap; disk was not the bottleneck.

**2. Receipt.** `09_package/acceptance_receipt.v002.json`, written 2026-08-10 23:46:27
(`generated_at` 2026-08-10T14:46:27Z). It measured
`episodes\PD-2026-062-greene\08_edit\greene_final_bgm.v001.mp4` and records
`video_sha256: sha256:0a8fa23d1b0ca61ade61bd34e917c6b3e2875ef9ffd8411b6b6ad93e0e60efae`
— **matches the file on disk exactly**. Status `FAIL`, 5 hard failures.

**3. Independent run today** — `py -3.11 scripts/check_final_acceptance.py PD-2026-062-greene --render …v001.mp4`
(exit 1, 00:35:18→00:55:24, no flags, no receipt). **RESULT: FAIL**, 9 hard failures, verbatim:

```
FAIL [hard] sound_layers: render audio not a verified 4-layer mix: render carries no 'audio_mix_sha256' container tag -- the mux stage (build_case_film_mux.py) was NOT run, so the render's audio is not bound to the built 4-layer mix (the orphaned-sound-plan failure)
FAIL [hard] probe_receipt: probe_receipt.v002.json: probe film_sha256 ee7dc6686c653c2d.. != current film.json 4434bf92077966e1.. (stale probe from an earlier render)
FAIL [hard] caption_format: captions.final.v001.srt: 298 violation(s): 58ch; 67ch; 83ch; 84ch; 69ch; 80ch ...
FAIL [hard] caption_sync: p50 +0.000s exact 76% late 18% drift +0.012s fword-ends 93 | 93 mid-phrase dangling break(s): #7 ...'its', #21 ...'the', #30 ...'a', #38 ...'and', #40 ...'the'
FAIL [hard] footage_utilization: 1/74 staged footage clip(s) referenced 0 times: AR-6041714__video_of_not_working_television.mp4
FAIL [hard] padding: 24 distinct 7-word phrase(s) repeat > 4
FAIL [hard] asset_reuse: 28 asset(s) over cap [AR-11124042__analog_tape_recorder_in_close_up.mp4 2x>1; AR-11594313__close_up_of_bars_and_rainfall_behind.mp4 2x>1; AR-13719546__tips_of_pocket_watch_running_backwards.mp4 2x>1; AR-14282774__silhouette_of_a_person_waving_their_hand.mp4 2x>1]
FAIL [hard] caption_breaks: 39 orphan cue(s) ["tenants.", "tenants.", "door."]; 86 cue(s) split mid-phrase (e.g. "...against three of its" | "tenants....") [captions.final.v001.srt]
FAIL [hard] preflight_receipt: preflight_receipt.v001.json preflight NOT green (verdict=BLOCK render_allowed=False) -- fix the preflight BLOCK and re-run preflight_render_gate.py before acceptance
```
Soft: `hook_added` (shotlist totals missing), `onscreen_text_verified` (claims not in repo — skipped
honestly), `script_structure` (no annotated script) — all reported PASS [soft].

**Honest caveat on the three caption failures.** `caption_format` / `caption_sync` / `caption_breaks`
are measured against the *current sidecar* `08_edit/captions.final.v001.srt` (mtime 2026-08-11 01:46),
not against the captions burned into the 2026-08-10 master. Receipt v002 recorded all three as
`true` when the master was fresh. So this is a **mismatch between the master and its current inputs**,
not proof that the master's burned captions are bad — and it is one more reason the master is stale.
The re-render's `[4b]` step resolves them (observed on marmet tonight: `cues 545 -> 515 |
orphans 27 -> 0 | dangling 88 -> 0`).

**4.** n/a (master exists).

**5. Title/thumbnail approval: NO.** `approvals/` holds only APR-0001 (`check: factory_used`),
APR-0002 (`target_type: edit`) and APR-0003 (`target_type: edit`). Across the whole repo the owner
title/thumbnail gate is recorded as an APR with `target_type` `title_thumbnail` /
`title_thumbnail_pair` / `package` (e.g. `PD-2026-015-theranos/approvals/APR-0003.json`,
`PD-2026-020-gardner/approvals/APR-0002.json`). **No such record exists for any of EP62–69.**
`09_package/title_thumbnail_candidates.v001.json` records only a machine selection
(`"why": "carried into 09_package/youtube_meta.v001.json"`), which is not an owner approval.
Note the scheduler does **not** enforce this — `upload_schedule_case_v001.py` only checks
`target_type='edit'` approvals — so this gate is honoured by discipline, not by code.

**6.** Covered above. APR-0003 binds explicitly to these bytes and says *"this render of EP62 only. A
re-render invalidates it."* The re-render therefore also invalidates APR-0003 — but that no longer
matters, because `animation_density` now passes on its own at the 4 s cap.

**After the queued re-render, the residual hard failures should be:** `sound_layers` (PART 1),
`padding`, `asset_reuse`, `preflight_receipt` — **all four named in APR-0002**. The four currently
uncovered ones (`probe_receipt`, `caption_sync`, `caption_breaks`, `footage_utilization`) are each
repaired by a pipeline step: `[5b]` writes a fresh probe receipt bound to the film sha, `[4b]` polishes
the captions, `[4c]` retires the one unused clip.

**Blocking item: the re-render (queued, ~2 h), then a `--emit-receipt` run.**

---

### EP63 correa — same shape as greene, plus a factory-QC gap

**1. Master.** `episodes/PD-2026-063-correa/08_edit/correa_final_bgm.v001.mp4`
```
size 1,822,524,344 B   mtime 2026-08-10 22:17:26
duration=1903.733333 (31.73 min)   h264 1920x1080 30/1 + aac stereo   bit_rate=7,658,737
sha256 8e03a6f813b6146ec2430e51256068892b0c8339a78f8101193d578493f7784f
```

**2. Receipt.** `09_package/acceptance_receipt.v001.json`, written 2026-08-10 22:57:43
(`generated_at` 2026-08-10T13:57:43Z), measured
`episodes\PD-2026-063-correa\08_edit\correa_final_bgm.v001.mp4`,
`video_sha256: sha256:8e03a6f8…f7784f` — **matches disk**. Status `FAIL`, 4 hard failures.

**3. Independent run today** (exit 1, 00:55:24→01:10:46). **RESULT: FAIL**, 8 hard failures:

```
FAIL [hard] render_freshness: sha256 identical to prior receipt acceptance_receipt.v001.json (byte-identical to an already-graded render -> not fresh; re-render or pass --render-started-at for a legitimate re-grade)
FAIL [hard] sound_layers: render audio not a verified 4-layer mix: render carries no 'audio_mix_sha256' container tag -- the mux stage (build_case_film_mux.py) was NOT run, so the render's audio is not bound to the built 4-layer mix (the orphaned-sound-plan failure)
FAIL [hard] probe_receipt: probe_receipt.v002.json: probe film_sha256 06aaeac3514f4d43.. != current film.json e356c35425f1b588.. (stale probe from an earlier render)
FAIL [hard] caption_format: captions.final.v001.srt: 316 violation(s): 83ch; 67ch; 53ch; 83ch; 78ch; 58ch ...
FAIL [hard] caption_sync: p50 +0.000s exact 72% late 19% drift +0.000s fword-ends 87 | p90 lag +0.368s > +0.35s (too many late cues); 87 mid-phrase dangling break(s): #4 ...'of', #8 ...'did', #10 ...'in', #20 ...'through', #52 ...'her'
FAIL [hard] footage_utilization: 7/56 staged footage clip(s) referenced 0 times: AR-32086252__raindrops_on_umbrella_calm_weather_scene.mp4, AR-37218119__sunlight_filtering_through_lush_green_jungle_can.mp4, AR-5453774__view_of_medicines_on_a_wooden_table.mp4, AR-6830138__people_playing_domino.mp4, AR-9498288__an_escalator_is_moving_up_and_down_in_a_subway.mp4, AR-v_14621__web_drops_rain_yard_colombia.mp4 ...
FAIL [hard] caption_breaks: 35 orphan cue(s) ["it.", "evidence.", "afternoon."]; 84 cue(s) split mid-phrase (e.g. "...the First Circuit did" | "not reduce it by...") [captions.final.v001.srt]
FAIL [hard] preflight_receipt: preflight_receipt.v001.json preflight NOT green (verdict=BLOCK render_allowed=False) -- fix the preflight BLOCK and re-run preflight_render_gate.py before acceptance
```

`render_freshness` here is a **re-grade artifact**, not a defect of the film: the file is byte-identical
to what receipt v001 already graded. `--render-started-at` would clear it; that flag was deliberately
**not** used. It does mean these exact bytes can never produce a new green receipt — only a new render can.

**A real one to watch:** the pre-render forecast additionally predicts
`visual_asset_qc: FACTORY: 27 staged clip(s) NOT reviewed in the manifest` for the *next* build. That
passed on the current master (its film references a different factory set) but will hard-fail the
re-render unless those 27 clips get a QC verdict. **It is not covered by any APR.**

**5. Title/thumbnail approval: NO** (APR-0001/0002/0003, all `edit` / `factory_used`).

**Blocking item: the re-render — preceded by QC verdicts for 27 factory clips, or it will fail again.**

---

### EP64 memphis — already scheduled, but the *wrong file* was uploaded

**1. Two masters exist.**
```
memphis_final_bgm.v001.mp4  1,741,201,834 B  mtime 2026-08-11 04:18:54  duration=1930.100000 (32.17 min)  bit_rate=7,217,042
   sha256 480a58c728e67ae55545ccc7d3b1ba70fe90614202f0aa399a444dfe4cfc7c0b
memphis_final_bgm.v002.mp4  1,739,873,059 B  mtime 2026-08-11 20:25:52  duration=1930.100000            bit_rate=7,211,535
   sha256 f8727a6e2bbb4b267b6a2cd43c9caf1dc70a6121ebe15e4bd0c2acfc76a04822
```
Identical duration; v002 is the same picture **re-muxed against the built 4-layer mix**
(`audio_provenance.v002.json`, 2026-08-11 20:22:23 → mux at 20:25:52).

**2. Receipt.** `09_package/acceptance_receipt.v001.json`, written 2026-08-11 12:05:56
(`generated_at` 2026-08-11T03:05:56Z), measured `…memphis_final_bgm.v001.mp4`,
`video_sha256: sha256:480a58c7…c7c0b` — **matches v001 on disk**.
**No receipt measures v002.** That is v002's only blocker.

**This episode is already on YouTube.** `09_package/youtube_schedule_result.v001.json`:
```
video_id  : oaFNcW0iDig     privacy: private
publishAt : 2026-08-18T03:00:00Z   (2026-08-18 12:00:00+09:00)
title     : One Wrong Initial Split Their House Into Two Accounts. The City Cut the Power Five Times.
video_sha256    : sha256:480a58c728e67ae5…    <-- v001
thumbnail_sha256: sha256:f21308cbd650da4a…
scheduled_at    : 2026-08-11T10:00:54Z  (19:00 JST)
```
`final_delivery.v001.json` also points at v001 and its sha matches. The upload is internally consistent.

**3. Independent runs today, both files, no flags, no receipt:**

`memphis_final_bgm.v001.mp4` (the uploaded bytes) — exit 1, 01:10:46→01:25:23. **RESULT: FAIL**, 4 hard:
```
FAIL [hard] render_freshness: sha256 identical to prior receipt acceptance_receipt.v001.json (byte-identical to an already-graded render -> not fresh; re-render or pass --render-started-at for a legitimate re-grade)
FAIL [hard] sound_layers: render audio not a verified 4-layer mix: render carries no 'audio_mix_sha256' container tag -- the mux stage (build_case_film_mux.py) was NOT run, so the render's audio is not bound to the built 4-layer mix (the orphaned-sound-plan failure)
FAIL [hard] padding: 10 distinct 7-word phrase(s) repeat > 4
FAIL [hard] preflight_receipt: preflight_receipt.v001.json preflight NOT green (verdict=BLOCK render_allowed=False) -- fix the preflight BLOCK and re-run preflight_render_gate.py before acceptance
```
`memphis_final_bgm.v002.mp4` — exit 1, 01:25:23→01:39:44. **RESULT: FAIL**, only 2 hard:
```
FAIL [hard] padding: 10 distinct 7-word phrase(s) repeat > 4
FAIL [hard] preflight_receipt: preflight_receipt.v001.json preflight NOT green (verdict=BLOCK render_allowed=False) -- fix the preflight BLOCK and re-run preflight_render_gate.py before acceptance
```
and, crucially:
```
PASS [hard] render_freshness: fresh render: sha differs from acceptance_receipt.v001.json
PASS [hard] sound_layers: genuine 4-layer mix present & bound: 48.3 onsets/min (backstop 6), ambience -21.7 dB (floor -33); 15 distinct SFX files, 8 music tracks; bound to audio_provenance.v002.json via audio_mix_sha256 tag
PASS [hard] animation_density: BODY near-still 3.0% (57s over 1918s body, longest 3.1s); limits <= 10% and single <= 4s
```

**Judgement.** Both of v002's hard failures (`padding`, `preflight_receipt`) are named in
`approvals/APR-0002.json` under `accepted_deviations`. **v002 is the only file in this entire slate
that reaches "every remaining hard failure is owner-approved" today.** The file that was actually
uploaded, v001, additionally fails `sound_layers` — its audio is Remotion's, not the built mix. That
deviation *is* also listed in APR-0002, so the upload was not illegitimate. But a strictly better
master has been sitting unshipped since 20:25 on 2026-08-11.

**5. Title/thumbnail approval: NO** (APR-0001/0002/0003 are `factory_used` / `edit`). The title above
went live without an owner `title_thumbnail` record.

**Blocking item: none for shipping — it is scheduled. The open decision is whether to replace
oaFNcW0iDig's file with v002 (needs a receipt on v002 + a re-upload).**

---

### EP65 marmet — rendered tonight; one uncovered `animation_density`, plus a receipt on the wrong file

**1. Master — replaced during this audit.**
```
OLD: 1,541,924,587 B  mtime 2026-08-10 10:16:11  sha256 8aeed8990385489c26fd5679bcbbdb018964719196c6fbdd0c7cc456242f6bc1
NEW: 1,735,026,753 B  mtime 2026-08-12 00:36:19  duration=1902.200000 (31.70 min)
     sha256 41042effc8c21ab3a9a15b48b45bb5e7d420ab97532f9646ba31afd719f69f4f
     TAG:audio_mix_sha256=afc6df687ea44e770a5442f3e59325159430d29b072902b6689bca264176aef5
```
The old sha was verified against `acceptance_receipt.v005.json` before it was overwritten: receipt said
`8aeed899…f6bc1`, disk said `8aeed899…f6bc1` — matched. That receipt is now historical.

**2. Receipt — THIS IS THE BLOCKER, and it is exactly the stale-receipt trap.**
A different session wrote `09_package/acceptance_receipt.v006.json` at 2026-08-12 00:58:22. It records:
```
video_path   : out\marmet.mp4
video_sha256 : sha256:ee5f5cb9e9c98ce02dbb19f6c647c2be4e8b45e8033261e48a5e290648d5b15d
status       : FAIL
hard         : ['animation_density','bgm_present','sound_layers','loudness','arc_nonrepeat','padding','preflight_receipt']
```
Measured independently:
```
$ sha256sum out/marmet.mp4
ee5f5cb9e9c98ce02dbb19f6c647c2be4e8b45e8033261e48a5e290648d5b15d *out/marmet.mp4
```
**The newest receipt measured `out/marmet.mp4` — the pre-mux render — not the deliverable master.**
That is why it lists `bgm_present`, `sound_layers` and `loudness` as failures: the pre-mux file carries
Remotion's raw audio. Against the shippable master (`41042eff…`) the receipt's `video_sha256` **does not
match**, so `upload_schedule_case_v001.py` will refuse:
`"receipt is for a different render (receipt sha … )"`.

Meanwhile `final_delivery.v002.json` (written 01:02:23) points correctly at the master with
`sha256:41042eff…`. **Delivery and receipt disagree.** A receipt on the actual master is required.

**3. Independent run on the real master** — `check_final_acceptance.py PD-2026-065-marmet --render
episodes/PD-2026-065-marmet/08_edit/marmet_final_bgm.v001.mp4` (exit 1, 01:40:48→01:55:20, no flags,
no receipt). **RESULT: FAIL**, 3 hard failures:

```
FAIL [hard] animation_density: BODY near-still 4.8% (91s over 1890s body, longest 4.3s); limits <= 10% and single <= 4s (OP/ED bookends excluded; MotionSample ~5.5%)
FAIL [hard] padding: 38 distinct 7-word phrase(s) repeat > 4; phrase repeated x3 (>= 3): 'brown s case and taylor s case'
FAIL [hard] preflight_receipt: preflight_receipt.v003.json preflight NOT green (verdict=BLOCK render_allowed=False) -- fix the preflight BLOCK and re-run preflight_render_gate.py before acceptance
```
Everything the fixes were supposed to deliver, delivered:
```
PASS [hard] render_freshness: fresh render: sha differs from acceptance_receipt.v006.json; muxed 352s after its render
PASS [hard] sound_layers: genuine 4-layer mix present & bound: 48.7 onsets/min (backstop 6), ambience -21.8 dB (floor -33); 17 distinct SFX files, 8 music tracks; bound to audio_provenance.v002.json via audio_mix_sha256 tag
PASS [hard] probe_receipt: probe_receipt.v004.json status=PASS bound_by=film_sha256 (motion/black/freeze on 60.05s slice)
PASS [hard] caption_sync: p50 -0.250s exact 15% late 9% drift -0.198s fword-ends 0
PASS [hard] caption_breaks: 515 cues, no mid-phrase breaks [captions.final.v001.srt]
PASS [hard] footage_utilization: all staged footage used; utilization 100% (181/181)
PASS [hard] arc_nonrepeat: no cross-episode reuse: 330 cut assets share no bytes with 42 other episodes / 9441 files
```

**`padding` and `preflight_receipt` are both named in APR-0002. `animation_density` is not** — marmet
never received an APR-0003. The figure is **near-still volume 4.8% against a 10% cap** (below the 5.5%
MotionSample the owner approved as the channel standard) with **one hold of 4.3 s against the 4.0 s
cap — 0.3 s over, once, in a 31.7-minute film.** That is the same question the owner answered "A" to
three times for EP62 (3.3% / 3.7 s), EP63 (1.2% / 3.8 s) and EP64 (3.0% / 3.1 s). **It is an owner
decision, not something to waive here, and not something worth a 2-hour re-render without asking.**

**A false positive that was real, and has since been fixed.** During this audit the pre-render forecast
reported `arc_nonrepeat: 15/330 cut assets reused from other episodes`, all attributed to EP67 ramirez —
and `arc_nonrepeat` is explicitly listed under `not_accepted` in APR-0002, so it would have been a
genuine blocker. It was **not a real reuse**: `check_arc_nonrepeat.py` fingerprinted on *basename*, and
both episodes name their generated plates `r001.png…rNNN.png`. Measured:
```
r015.png  marmet=7813f1d4d06369cf (12,228,247 B)  ramirez=1f8f6a644c99a2da (7,198,680 B)  -> DIFFERENT
r021.png  marmet=174ed7cca3320c80  (8,943,594 B)  ramirez=80b982f9875c64f4 (5,682,082 B)  -> DIFFERENT
r030.png  marmet=9bb3b579918d6c27  (7,884,227 B)  ramirez=2acf648a843cd52d (6,201,251 B)  -> DIFFERENT
r033.png  marmet=617f5891de108d46 (10,716,015 B)  ramirez=f5fe36d6fc34d0bf (5,641,620 B)  -> DIFFERENT
r048.png  marmet=e8ddc06bc48b6105 (10,930,908 B)  ramirez=95238f5c8ca2bfa1 (7,118,749 B)  -> DIFFERENT
r060.png  marmet=096bba585121e1c1 (11,026,586 B)  ramirez=63d845efa5c7d3bc (7,807,614 B)  -> DIFFERENT
```
All 15 collisions were `r###.png`. The script already carried a guard for exactly this class — its
comment records the same bug being found on `P01.png` in August — but the regex omitted the `r` prefix:
```python
if re.match(r"^(s\d{2,3}|p\d{2,3}|m\d{1,3}_rife|f\d{3}.*)\.(png|jpg|jpeg|webp|mp4|mov|webm|m4v)$", base):
```
**This has now been fixed.** `scripts/check_arc_nonrepeat.py` was rewritten at **2026-08-12 01:21:09**
(mid-audit, by a concurrent session) to compare **sha256 of the bytes** rather than basenames. The
change is visible in the gate's own wording between two runs an hour apart:
```
00:35 greene : PASS arc_nonrepeat: 313 cut assets are all unique vs 119 other episodes / 39172 fingerprints
01:40 marmet : PASS arc_nonrepeat: 330 cut assets share no bytes with 42 other episodes / 9441 files
```
So marmet's `arc_nonrepeat` is green on the real master and **no owner approval is needed for it**.
Caveat: `predict_acceptance.py` may still surface the old basename verdict until it is re-run — treat
`check_final_acceptance` as the authority.

**5. Title/thumbnail approval: NO.** marmet has only APR-0001 and APR-0002 — it never received an
APR-0003, so `animation_density` was never owner-approved for this episode. It now passes on the
raised 4 s cap, which is precisely why §1's threshold note matters here.

**Blocking item: one owner answer on `animation_density` (4.8% volume / 4.3 s single hold vs a 4.0 s
cap). If approved as APR-0003, the remaining two hard failures are already covered by APR-0002 and the
only work left is a `--emit-receipt` run on the master (~20 min). If not approved, marmet needs a cut
re-timed and a fresh ~2 h render.**

---

### EP66 openfields — no render; the `[4a]` gate will stop it before it starts

**1. No mp4.** `08_edit/` contains only `captions.final.v001.srt` (2026-08-11 20:53) and
`captions.final.v001.lead.json`. No `openfields_final_bgm.v001.mp4`.

**4. What is missing, precisely:**

- **i2v motion pass: not run.** `remotion/public/openfields/` has `factory`, `factory_offtopic`,
  `factory_pruned_offtopic`, `factory_rejected`, `img`, `img_pruned_offtopic`, `narration.mp3` —
  **there is no `motion/` directory at all** (marmet, by comparison, has `motion/` with 149 clips).
- **Mandatory plates are not in the film** — and `[4a]` now hard-dies on exactly this:
```
[satisfied] openfields: cuts=280 distinct_video=191 stills_in_film=89 mandatory=185 forbidden_keywords=33
[satisfied] openfields: FAIL -- 2 problem(s):
  - mandatory_stills: 98 of 185 declared still(s) are in no cut of the film -- L070.png, L072.png, … L253.png.
  - distinct_video_assets: 191 distinct footage+motion source(s) across 191 video cut(s), against a declared 350 -- 159 short
```
  `_finish_episode.sh` `[4a]`: `if [ $_sat -ne 0 ] && grep -qE "mandatory_stills|forbidden_subjects" … then die`.
  **The queue will start openfields and it will die at step [4a] within seconds.**
- **No preflight receipt** (`04_scenes/preflight_receipt.v*.json` absent).
- **No probe receipt** (`09_package/probe_receipt.v*.json` absent).
- **4-layer mix never built**: `06_audio/audio_provenance.v*.json` absent.
- **No `approvals/` directory at all.**

**Forecast** (`predict_acceptance.py --slug openfields`; the predictor calibrates **42 agree / 0 disagree**
against memphis's own receipt, so it is a credible instrument):
```
WILL FAIL animation_mix        still-dependent plan (紙芝居 risk): 88 hero stills linger > 5s (cap 8; longest 5.4s) — lingering photos, not motion
WILL FAIL caption_breaks       23 orphan cue(s) ["2017.", "officer.", "coming."]; 68 cue(s) split mid-phrase
WILL FAIL caption_format       captions.final.v001.srt: 278 violation(s)
WILL FAIL footage_utilization  overall utilization 74% (284/382) < 80% threshold
WILL FAIL padding              4 padded dead-air gap(s); worst 5.00s at 14:52.80 (extreme dead air); 22 distinct 7-word phrase(s) repeat > 4
WILL FAIL preflight_receipt    no 04_scenes/preflight_receipt.v*.json
WILL FAIL probe_receipt        no 09_package/probe_receipt.v*.json
WILL FAIL retention_cadence    re-hook gap 251s > 180s starting at 17.0min; no direct question for 748s > 420s starting at 14.3min
WILL FAIL sound_layers         no 06_audio/audio_provenance.v*.json -- the 4-layer mix was never built/registered
APR needed: 9 checks   [NO approvals/ DIRECTORY]
```
`caption_breaks` / `caption_format` self-resolve at `[4b]`. `animation_mix`, `retention_cadence` and
`padding` are content problems that a render will not fix.

**5. Title/thumbnail approval: NO** (no `approvals/` directory). `youtube_meta.v001.json` and 5
thumbnail candidates exist.

**Blocking item: the i2v pass (159 clips short of the declared 350) and the 98 missing mandatory plates.**

---

### EP67 ramirez — no render; script is out of contract, and the reuse with hyatt is real

**1. No mp4.** `08_edit/` has `captions.final.v001.srt` and `captions.final.v002.srt` (v002 is the one
the filmconfig points at — the `[4b]` fix exists because of exactly this episode).

**4. Missing:** no `motion/` dir (0 i2v clips); no preflight receipt; no probe receipt; no
`audio_provenance`; no `approvals/`.
```
[satisfied] ramirez: cuts=155 distinct_video=106 stills_in_film=49 mandatory=122 forbidden_keywords=47
[satisfied] ramirez: FAIL -- 2 problem(s):
  - mandatory_stills: 81 of 122 declared still(s) are in no cut of the film -- R001.png … R122.png.
  - distinct_video_assets: 106 distinct … against a declared 260 -- 154 short
```
→ dies at `[4a]`.

**Forecast — the worst of the eight, 15 WILL FAIL.** The ones a render cannot fix:
```
WILL FAIL script_craft   EP67_ramirez_script.en.v002.md: 4 forbidden claim(s) from EP67_ramirez_FACTS_LEDGER.v001.md appear in the narration: ['erroneously flagged many law-abiding people', 'a planned trip to Mexico', 'an international vacation he had planned with his family']
WILL FAIL script_length  4,437 words vs required 1,575-2,141 -> narrates in ~24.9 min, outside the 11.5-12.5 min band … Cut, do not speed the voice.
WILL FAIL runtime_band   1609.8s = 26.83min (band 690-750s)
WILL FAIL caption_coverage 30/302 narration chunk(s) below 80% caption coverage; captions end 152.85s before the last narration chunk (srt ends 1447.96s, narration ends 1600.81s)
WILL FAIL arc_nonrepeat  29/155 cut assets reused from other episodes: ar-11958282__a_young_woman_looking_at_books_in_a_library.mp4 <- PD-2026-069-hyatt; … (+23 more)
WILL FAIL animation_mix  49 hero stills linger > 5s (cap 8; longest 10.2s)
WILL FAIL retention_cadence re-hook gap 205s > 180s; no direct question for 640s > 420s
```
Two distinctions that matter:
- **`runtime_band` / `script_length` are an instrument problem, not a content problem.** `runtime_band()`
  reads `04_scenes/remotion_plan.v*.json → motion_budget.runtime_band_seconds`; ramirez has **no plan
  file**, so it falls back to `manifest.target_duration_minutes`, which is `None` (`state: researching`),
  which yields the 11.5–12.5 min default. `episode_spec.v001.json` declares
  `runtime_seconds: [1560, 1895]`. **Write the plan band; do not cut a 30-minute script to 12 minutes.**
- **`arc_nonrepeat` here IS real**, unlike marmet's. The colliding names are `ar-*` shared factory stock
  genuinely staged into both ramirez and hyatt. One of the two must restage.

**5. Title/thumbnail approval: NO** (no `approvals/`).

**Blocking item: 4 forbidden claims in the narration (a script fix + re-record), then i2v.**

---

### EP68 pinto — no render; the film.json is a 1,160-byte placeholder

**1. No mp4.**

**4. `remotion/src/data/pinto_film.json` is 1,160 bytes and is explicitly a stub:**
```json
"_placeholder": "PLACEHOLDER ONLY -- NOT A FILM. Written 2026-08-11 so that remotion/src/Root.tsx can
 statically import this path and the Ep68Pinto composition can be registered before the pool is finished.
 Every array below is empty on purpose: rendering this file produces a blank film…"
"hook": [], "cuts": [], "captions": [], "graphics": [], "figures": []
```
```
[satisfied] pinto: cuts=0 distinct_video=0 stills_in_film=0 mandatory=104 forbidden_keywords=124
  - mandatory_stills: 104 of 104 declared still(s) are in no cut of the film
  - distinct_video_assets: 0 … against a declared 265 -- 265 short
```
No `motion/` dir; no preflight/probe receipt; no `audio_provenance`; no `approvals/`.
Forecast confirms the consequences: `animation_mix: animated+footage coverage 0.0% < 45% floor (0s of
1765s body has genuine motion)`, `motion_density: 0.00/min < 2.5 (0 beats over 29.4min)`,
`footage_utilization: 42/42 staged clips referenced 0 times; overall utilization 0%`,
`caption_integrity: film captions[]=0`, `factory_used: referenced_in_composition=False`.

**5. Title/thumbnail approval: NO.**

**Blocking item: the entire pool — 265 distinct video sources short, 104/104 plates unplaced.
This is the furthest from shippable of the eight.**

---

### EP69 hyatt — no render; content gaps a render cannot fix

**1. No mp4.**

**4.** No `motion/` dir; no preflight/probe receipt; no `audio_provenance`; no `approvals/`.
```
[satisfied] hyatt: cuts=192 distinct_video=131 stills_in_film=61 mandatory=113 forbidden_keywords=58
  - mandatory_stills: 58 of 113 declared still(s) are in no cut of the film -- H002.png … H113.png.
  - distinct_video_assets: 131 … against a declared 250 -- 119 short
```
→ dies at `[4a]`.
```
WILL FAIL retention_cadence  no direct question for 1695s > 420s starting at 0.0min (episode poses ZERO questions)
WILL FAIL padding            3 padded dead-air gap(s); worst 22.00s at 4:49.52 (extreme dead air)
WILL FAIL animation_mix      61 hero stills linger > 5s (cap 8; longest 8.9s)
WILL FAIL arc_nonrepeat      14/192 cut assets reused from other episodes … <- PD-2026-067-ramirez
WILL FAIL runtime_band       1704.3s = 28.40min (band 690-750s)     [same missing-plan instrument problem as ramirez]
WILL FAIL script_length      4,678 words vs required 1,575-2,141    [same]
WILL FAIL footage_utilization overall utilization 72% (196/273) < 80%
```
A **22-second dead-air gap at 4:49** and **zero questions in a 28-minute film** are editorial defects,
not gate noise.

**5. Title/thumbnail approval: NO.**

**Blocking item: i2v (119 short) plus a script/edit pass for the 22 s dead air and the zero-question cadence.**

---

## 3. Ranked table — shippable now?

Wall-clock uses the **measured** figures: one full `_finish_episode` run = **1 h 53 m** (marmet, tonight);
i2v = **206 s/clip** as briefed; one acceptance run on a 31-min master = **14–20 min** (measured
01:10:46→01:25:23 and 01:25:23→01:39:44). The GPU takes one job at a time, so i2v and renders serialise.

| # | Episode | Shippable now? | The single blocking item | Est. wall-clock to clear |
|---|---|---|---|---|
| 1 | **EP64 memphis** | **Yes — already scheduled** (oaFNcW0iDig, 2026-08-18 12:00 JST) | Nothing blocks it. Open decision: the uploaded file is **v001**, which fails `sound_layers`; **v002** passes it and has only APR-covered failures | 0 h as-is · ~40 min to swap to v002 (receipt + re-upload) |
| 2 | **EP65 marmet** | **No — one owner answer away** | `animation_density` fails **uncovered**: near-still 4.8% (cap 10%) but one hold of **4.3 s against a 4.0 s cap**. marmet has no APR-0003. `padding` + `preflight_receipt` are already APR-0002. Secondary: receipt `v006` measured `out/marmet.mp4` (`ee5f5cb9…`), not the master (`41042eff…`) | **~20 min** if the owner approves the 0.3 s overrun (one `--emit-receipt` run) · **~2 h+** if the cut must be re-timed |
| 3 | **EP62 greene** | No | The queued re-render (the current master is superseded by a newer `film.json` and carries no 4-layer audio) | **~2 h** render + 20 min receipt |
| 4 | **EP63 correa** | No | Same re-render — but **27 factory clips need QC verdicts first**, or `visual_asset_qc` hard-fails again | ~1 h QC + **~2 h** render + 20 min receipt |
| 5 | **EP66 openfields** | No | **i2v pass never run**: 0 motion clips, 159 distinct sources short, 98/185 mandatory plates unplaced → dies at `[4a]` | **~9.1 h** i2v (159 × 206 s) + 2 h render + 20 min · plus a content pass for 4 dead-air gaps and the 251 s re-hook gap |
| 6 | **EP69 hyatt** | No | i2v (119 short, 58/113 plates unplaced) **and** editorial defects: 22 s dead air at 4:49, zero questions in 28 min | **~6.8 h** i2v + content pass + 2 h render + 20 min |
| 7 | **EP67 ramirez** | No | **4 forbidden claims from its own facts ledger are in the narration** — a script fix and re-record, before any i2v | script+VO (unbounded, ≥1 day) + **~8.8 h** i2v + 2 h render |
| 8 | **EP68 pinto** | No | `pinto_film.json` is a 1,160-byte placeholder; the pool does not exist (0 cuts, 0/104 plates, 265 sources short) | **~15.2 h** i2v + 2 h render + 20 min — furthest from shippable |

**Total GPU time to clear EP66–69 as briefed: ~39.9 h of i2v, serialised, plus ~8 h of renders.**
Nothing about that is compressible by approving a deviation; the clips do not exist.

### Two things that must not be done

1. **Do not approve `arc_nonrepeat` for marmet, and do not re-render for it.** It was a basename
   collision between two episodes that both number their plates `r###.png`; six sampled pairs have
   different sha256 **and** different byte sizes. `check_arc_nonrepeat.py` was rewritten to compare
   bytes at 2026-08-12 01:21 and the gate is now green on marmet's real master. (ramirez↔hyatt is a
   *different* case, on shared `ar-*` factory stock, and **is** real reuse.)
2. **Do not cut EP67/EP68/EP69's scripts to 12 minutes** because `runtime_band` says `690-750s`. That
   band is the fallback default, reached because those three have no `04_scenes/remotion_plan.v*.json`
   and `manifest.target_duration_minutes` is `None` (`state: researching`). Their
   `episode_spec.v001.json` declares `runtime_seconds: [1560, 1895]`. Write the plan band.

### Owner gate that is unmet across all eight

**No episode in EP62–69 has a title/thumbnail approval record.** The repo's convention is an
`approvals/APR-*.json` with `target_type` of `title_thumbnail` / `title_thumbnail_pair` / `package`
(examples: `PD-2026-015-theranos/approvals/APR-0003.json`, `PD-2026-019-varsityblues/approvals/APR-0002.json`,
`PD-2026-020-gardner/approvals/APR-0002.json`). EP62–65 hold only `edit` and `factory_used` approvals;
EP66–69 have **no `approvals/` directory at all**. `upload_schedule_case_v001.py` does not enforce this,
which is why EP64 memphis reached YouTube with an unapproved title. Eight title/thumbnail decisions are
owed before these ship.

---

## 3b. LIVE ISSUE — the queue is re-rendering marmet redundantly, and greene is not next

At **2026-08-12 01:57:08** the queue started **marmet again**, although its own freshness rule says to
skip it:
```
remotion/src/data/marmet_film.json                              2026-08-11 22:50:39
episodes/PD-2026-065-marmet/08_edit/marmet_final_bgm.v001.mp4   2026-08-12 00:36:19
$ [ "$f" -ot "$m" ] && echo skip
film.json OLDER than master -> should SKIP
```
```
ProcessId 35492  2026/08/12 1:57:08  bash /tmp/pdq.WhHBPr/_finish_episode.sh marmet Ep65Marmet 65 --allow-video-diversity-deviation
[finish:marmet] START Wed Aug 12 01:57:08 2026
```

**Cause — a stale-check race in `scripts/queue_unattended.sh`.** The loop body is:
```bash
[ -f "$m" ] && [ -f "$f" ] && [ "$f" -ot "$m" ] && continue   # freshness test
py -3.11 scripts/check_episode_inputs.py --slug "$slug" … || continue
wait_idle || { … continue; }                                   # can block for HOURS
bash scripts/pd_run.sh … -- bash "$SNAP/_finish_episode.sh" "$slug" …   # launches WITHOUT re-testing
```
The freshness test is evaluated **before** `wait_idle`, which then blocks for as long as the current
render takes. When it returns, the job is launched on a decision that may be hours out of date. Here:
the test was taken at ~22:48 (when marmet's master was still the 2026-08-10 one), `wait_idle` then
blocked through marmet's own render *and* through this audit's measurement runs, and at 01:57 it
launched the job the test had authorised three hours earlier.

**Consequences, stated plainly:**
- marmet's master `41042eff…` (measured in §EP65) **will be overwritten** in ~2 h, and
  `final_delivery.v002.json` will go stale with it. Step `[7/7]` rewrites both, so this self-heals —
  it just costs about two hours.
- **greene does not start until that finishes**, because the GPU takes one job.
- The new marmet render should measure the same as the one in §EP65 (same `film.json`, same pool), so
  the `animation_density` owner question in §EP65 stands regardless.

**Not acted on.** `scripts/queue_unattended.sh` is out of scope for this audit and nothing was killed.
This is for the owner to decide: let the redundant render run (2 h, greene delayed), or stop it and let
the queue fall through to greene. The durable fix is to re-evaluate the freshness test *after*
`wait_idle` returns, immediately before launching.

## 4. The shortest path to "scheduled", in order

1. **Ask the owner one question**: marmet's `animation_density` — 4.8% near-still volume (cap 10%,
   MotionSample 5.5%), one hold 4.3 s against a 4.0 s cap. Same shape as EP62/63/64, all answered "A".
   *And* the eight title/thumbnail approvals. Both are owner-only; nothing else can proceed past them.
2. **EP65 marmet** — on approval, one `--emit-receipt` run on `marmet_final_bgm.v001.mp4`, then
   `upload_schedule_case_v001.py --ep marmet`. ~20 min.
3. **EP64 memphis** — decide whether to swap oaFNcW0iDig's file to v002 (better audio, fewer failures).
4. **EP62 greene** — next in `JOBS`, but blocked behind the redundant marmet re-render described in
   §3b. ~2 h render once it starts, then receipt.
5. **EP63 correa** — give the 27 factory clips QC verdicts *before* the queue reaches it, or the
   re-render burns 2 h and fails `visual_asset_qc`.
6. **EP66/67/68/69** — none can render at all until their i2v pools exist; `[4a]` will kill each run in
   seconds. ~40 h of serialised GPU, plus a script fix for EP67 and an edit pass for EP69.

## 5. How to reproduce every number here

```bash
ffprobe -v error -show_entries format=duration,size,bit_rate -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,channels -of default=noprint_wrappers=1 <master.mp4>
ffprobe -v error -show_entries format_tags -of default=noprint_wrappers=1 <master.mp4>     # audio_mix_sha256
sha256sum <master.mp4>                                                                     # vs receipt video_sha256
py -3.11 scripts/check_final_acceptance.py <EPISODE_ID> --render <master.mp4>               # no flags, no receipt
py -3.11 scripts/predict_acceptance.py --slug <slug>                                        # forecast, no GPU
py -3.11 scripts/predict_acceptance.py --slug memphis --calibrate                           # 42 agree / 0 disagree
py -3.11 scripts/check_spec_satisfied.py --slug <slug>                                      # what [4a] sees
py -3.11 scripts/check_arc_nonrepeat.py --ep <EPISODE_ID>
```

Measurement log for this audit (all `--emit-receipt` deliberately omitted):
```
[greene]        START 00:35:18  EXIT=1  END 00:55:24
[correa]        START 00:55:24  EXIT=1  END 01:10:46
[memphis_v001]  START 01:10:46  EXIT=1  END 01:25:23
[memphis_v002]  START 01:25:23  EXIT=1  END 01:39:44
[marmet_master] START 01:40:48  EXIT=1  END 01:55:20
```
All five ran at `BelowNormal` priority so as not to starve the live render. Receipt mtimes in
`09_package/` are unchanged by this audit; the only new receipt in the window (marmet `v006`, 00:58)
was written by a different session and is the mismatched one documented in §EP65.
