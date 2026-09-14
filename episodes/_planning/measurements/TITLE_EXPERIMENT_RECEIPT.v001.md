# Back-catalogue title rewrite — experiment receipt v001

**Applied 2026-08-10 ~23:55 JST. 39 of 39 written and independently verified.**

| artifact | path |
|---|---|
| the 39 proposals (persisted) | `episodes/_planning/measurements/TITLE_BATCH_39.v001.json` |
| per-video record + rollback | `episodes/_planning/measurements/TITLE_APPLY_39.applied.v001.json` |
| applier / rollback tool | `scripts/apply_title_batch.py` |
| before-figures source | `scripts/_yt_studio_video_ctr.20260810.json` (28d window ending 2026-08-10) |

---

## 1. Result

| | count |
|---|---|
| proposed | 39 |
| **applied** | **39** |
| skipped (failed re-verification) | 0 |
| refused (locked window) | 0 |

Independent re-read after the batch — a **fresh `videos.list`**, not the PUT's own echo:

| check | result |
|---|---|
| title == intended new title | **39 / 39** |
| description byte-identical to pre-change | **39 / 39** |
| `privacyStatus` unmoved | **39 / 39** |
| `publishAt` unmoved | **39 / 39** |
| locked-window videos byte-identical | **44 / 44** (0 overlap with the written set) |

Quota spent: **~2,010 units** (39 × `videos.update` @50 = 1,950, plus ~60 `videos.list` @1).
**No 403 occurred.** The ledger read "11,097 of 10,000 spent" before the batch and the writes
went through regardless — confirming the ledger is an estimate, which is exactly why it was
changed to warn rather than refuse. `exhausted_observed_403` was never recorded.

### One thing that looked like a failure and was not

On the immediate post-PUT re-read, **7 rows reported `title_changed: False`** —
`Qyad4FejCIc`, `5L_HCGJxX_U`, `rU2vk9XL4vY`, `Xc_PxdC_75c`, `gR_nzXIyIlk`, `AxOlQ2NIaBU`,
`i95peRcdtz4`. Every one of them had `description_identical: True`, and each PUT returned
HTTP 200. A fresh `videos.list` moments later showed **all 7 carrying the intended title**.
This is **read-after-write propagation lag** in the Data API, not a failed write —
established by re-measuring, not by assuming. A future applier should re-read once after a
short delay before declaring a row failed. Recorded in the JSON as `note_on_first_pass`.

---

## 2. Provenance — the proposals were nearly lost

The 39 were **never written into the repo**. The producing agent left them in a scratchpad
script, `…/scratchpad/titles.py` (mtime 2026-08-10 20:08), and its report surfaced only a
partial table with "full list of 39 available on request". A repo-wide grep for the batch
returns zero hits; the two title JSONs that *are* in the repo are decoys:

| file | rows | date | state |
|---|---|---|---|
| `measurements/TITLE_REFRESH_WAVE2.v001.json` | 20 | 08-03 | staged, never approved, **not** this batch |
| `title_refresh_mapping.v001.json` | 17 | 07-25 | already applied on 07-25 |

Both are 43–65 chars, i.e. mostly **below the new 59 floor**; had either been mistaken for
the approved set, the batch would have collapsed to 9 rows of the wrong titles. The 39 are
now persisted at `TITLE_BATCH_39.v001.json`. **A deliverable that exists only in a
transcript is a deliverable that has been lost.**

---

## 3. Re-verification — done independently, and stricter

Band imported from `scripts/check_packaging_qc.py` (`TITLE_MIN_CHARS=59`,
`TITLE_MAX_CHARS=100`), not retyped. All 39 pass on length (69–89 chars, median 81), question
form, second person, case citation, and pipe.

My check deliberately differs from the earlier one in four places, and **the earlier check
had a latent defect worth fixing before it is reused**:

| rule | earlier check | mine |
|---|---|---|
| question form | `new.rstrip().endswith("?")` — misses mid-title questions | any `?` |
| second person | `\b[Yy]our?\b` — misses `yours`, `yourself` | adds both |
| pipe | `" \| "` — misses an unspaced pipe | any `\|` |
| **locked window** | **`snippet.publishedAt`** | **`status.publishAt`** |

The last one is the real hazard: for a *scheduled* video `publishedAt` is the upload time,
not the release time, so a video uploaded 08-05 and scheduled for 08-15 would not have
tripped the lock. It happened not to bite here — I checked both fields against all 39 and
they agree, because all 39 are long-published videos — but the guard was wrong for the case
it existed to catch. `apply_title_batch.py` uses `status.publishAt`.

The locked set was enumerated live (union of uploads playlist + `search forMine`): **40**
videos with `publishAt >= 2026-08-10` (the brief said 41 — one has since gone public) plus
**4** published today, **44 locked total**, scheduled range 08-10 → 08-19. The applier
recomputes this on every run and hard-asserts before the first write.

---

## 4. Before-state (the measurement baseline)

Full per-video before-figures — old title, new title, impressions, CTR, views, description
SHA-256 — are in `TITLE_APPLY_39.applied.v001.json`. Window: **YouTube Studio default
trailing 28 days, ≈ 2026-07-14 → 2026-08-10.** Metric keys are
`VIDEO_THUMBNAIL_IMPRESSIONS` and `VIDEO_THUMBNAIL_IMPRESSIONS_VTR` (**not** `impressions`).
Treated total: **44,921 impressions**.

| video_id | imp | CTR | new title |
|---|---|---|---|
| `Xc_PxdC_75c` | 7,332 | 1.01% | She Banked Under $10,000 Because That Is What the Till Held. The IRS Took $32,820. |
| `SOu4Y1NkGGY` | 6,327 | 0.74% | He Showed the Officer the Paid Receipt. He Was Jailed and Strip-Searched Twice. |
| `marQjsCagh0` | 4,751 | 2.97% | OceanGate Fired the Man Who Wrote the Safety Report in 2018. Five People Dove in 2023. |
| `bYcqabvvxak` | 4,132 | 3.12% | A Detective Watched Two Men Pace a Store Window. The Frisk He Ran Became National Law. |
| `Qyad4FejCIc` | 3,025 | 1.29% | Alabama Held an Execution Date on Him for 30 Years. The Ballistics Were Wrong. |
| `tt7U1XgjCU4` | 2,039 | 2.31% | He Jumped Into a Storm With $200,000. Fifty Years On the FBI Cannot Name Him. |
| `5L_HCGJxX_U` | 1,831 | 0.76% | She Memorised His Face on Purpose So She Would Be Certain. She Named the Wrong Man. |
| `FTm1icKgycU` | 1,501 | 0.80% | The Site He Downloaded From Dropped It. Prosecutors Filed 13 Felonies Anyway. |
| `sphERPA4gAc` | 1,490 | 1.81% | He Handed the SEC the Arithmetic in 2000. Madoff Kept Running Until 2008. |
| `bXATF9ZnKLE` | 1,313 | 3.96% | Police Searched the Motorcycle in His Driveway. The Court Found the One Line Left. |
| `mj9qEKPRatE` | 880 | 1.70% | One Banker Was Paid $550 Million in a Year. Then the Government Came for Him. |
| `i95peRcdtz4` | 834 | 0.48% | A Seatbelt Ticket Carried No Jail Time. She Was Handcuffed in Front of Her Children. |

(27 further rows, all under 800 impressions, in the JSON.)

---

## 5. Hinders and Tyler — the owner's separate question

**Both ARE in the 39, and both were applied.** They get their own row as asked:

| | `Xc_PxdC_75c` Hinders | `rU2vk9XL4vY` Tyler |
|---|---|---|
| before imp / CTR | **7,332 / 1.01%** (most of any long-form) | 728 / 1.24% |
| title until 07-25 | "The IRS Seized Her Entire Bank Account — For…" | "Can the Government Take Your Home Over a Small Tax Debt?" |
| title 07-25 → tonight | "Following the deposit rule is what made her a suspect" (53) | "The county sold her condo and kept the extra $25,000" (52) |
| **new title (applied)** | **She Banked Under $10,000 Because That Is What the Till Held. The IRS Took $32,820.** (82) | **She Owed the County $15,000. It Sold Her Home for $40,000 and Kept All of It.** (77) |

Both dollar figures were checked against the episodes' own files before shipping —
`32,820` appears in the Hinders episode; `15,000` and `40,000` in the Tyler episode.

### The premise behind the question does not survive measurement

The brief treats it as settled that the 07-25 rewrite *hurt* these two, with "untouched
controls holding to two decimals". I reconstructed the full paired before/after from
`ctr_baseline_20260725.reconstructed.md` (28d ending 07-25) against tonight's pull, matching
on duration. **28 videos matched:**

| group | n | mean ΔCTR | mean impression change |
|---|---|---|---|
| **treated** (07-25 rewrites) | 15 | **+0.11 pp** | ×1.47 |
| **untouched controls** | 13 | **−0.04 pp** | ×1.26 |

The treated group moved **up** relative to controls. Hinders (−0.23) and Tyler (−0.30) are
real but they are not the group: DB Cooper **+0.92**, Titan **+0.55**, Milken **+0.49**,
Rajaratnam **+0.36** all rose. And the controls did not generally hold — Flashcrash
**−0.52**, Unlock **−0.51**, Miranda **+0.53**, OneCoin **+0.50**. The three controls named
in the brief are exactly the three whose impressions were flattest (×1.02, ×1.00, ×1.02);
**selecting controls on flat impressions selects for flat CTR**, so that comparison is
circular. Hinders' own impressions went **1,855 → 7,332 (×3.95)**, the largest expansion on
the channel; a 0.23 pp dip while absorbing four times the (colder) impressions is not
attributable to the title.

**Not overclaiming the reverse:** bucketing purely by impression growth shows no systematic
penalty either (flat <1.25× → +0.04 pp, n=21; grown ≥1.25× → +0.05 pp, n=7). The honest
reading is that **no title-shape effect is detectable in PD's data in either direction** —
the noise exceeds any signal at these volumes.

**A trap I nearly published:** comparing CTR *levels* (07-25 treated 1.41% weighted vs
untouched 1.95%) appears to condemn the rewrites, but it is confounded — the big, low-CTR
videos are the ones selected for treatment. Only the paired delta is valid. Do not quote the
level comparison.

---

## 6. The control group, and what this batch risks

Of the **43** public long-forms with ≥150 impressions, **30 are now treated** and **13
remain untouched**. That is a usable control, but note two asymmetries before judging it:

1. **The control skews low.** Treated holds 43,923 impressions, control 12,362. Control CTRs
   run 0.44–3.02% while the treated set contains every top performer. Expect
   **regression to the mean to flatter the control and penalise the treated** independent of
   any title effect.
2. **The channel's best titles were rewritten.** `Sz8zPUoBANM` (4.40%), `bXATF9ZnKLE`
   (3.96%), `vikfOBHullI` (3.77%), `bYcqabvvxak` (3.12%) were all in the approved 39 and are
   now changed. Given §5 found no measurable benefit from the rule set, **this is the real
   downside exposure of tonight's batch.** If the September read is a LOSS, these four are
   the first to roll back.

Surviving control (long-form, ≥150 imp, untouched): `bSnyfsulna8`, `tYZuE76Hwdc`,
`yRwxBfrOY5o`, `6ozsIfwqrP0`, `Enok7A7wGBA`, `m-uWzgWHGPg`, `2pLWw_vhfI8`, `GGW1SIAAgkY`,
`YhEJHK279f8`, `Iw-EPUD2nHg`, `4FlCaOVpln0`, `PfdEpNQyaQQ`, `Wo-SvvGsv8g`.
**Do not retitle any of these before 2026-09-07** or the experiment loses its comparison.

---

## 7. Which videos are the clean test

Both candidates in the brief were checked against my own pull. **One confirms, one does not.**

| candidate | brief says | measured | verdict |
|---|---|---|---|
| `Enok7A7wGBA` | 1,090 imp @ 0.46%, already compliant | **1,101 imp @ 0.45%**, 62 chars, 0 violations | **CONFIRMED** |
| `i95peRcdtz4` | the only high-impression video violating the rules | **834 imp** @ 0.48%, violated on **length only** (54) | **CORRECTED** |

`i95peRcdtz4` was not high-impression (rank ~20) and was not the only violator: **30 of 43**
long-forms violated the rules, including the channel's #1 (`Xc_PxdC_75c`, 53 chars). It was
also *inside* the 39, so it is now treated and cannot serve as a control.

**The clean test is therefore:**

- **`Enok7A7wGBA`** — fully rule-compliant title, **worst CTR of any high-impression
  long-form (0.45%)**, and deliberately left untouched. This is the standing evidence that
  the **thumbnail, not the title, is the ceiling.** Change only its thumbnail and nothing
  else; if CTR moves, the title rules were never the lever.
- **`bYcqabvvxak` (Terry)** would have been the ideal control — best high-impression CTR
  (3.12%) on a doubly non-compliant title (51 chars, second person) with flat impressions
  (×1.02). **It is in the 39 and is now treated**, so it converts from best control to
  highest-stakes single data point: if the rules work anywhere, this is where a rewrite
  should hold 3.12%; if it drops, the rules cost the channel its best asset.

---

## 8. When to re-read this, and what counts as a win

**Re-read on 2026-09-07** — 28 days after tonight, so the trailing 28-day window contains
**no** pre-change impressions. Reading earlier mixes two regimes; that is the mistake the
07-28 note already flags ("no verdict is possible yet").

Pull with `py -3.11 scripts/yt_studio_video_ctr.py`. **Snapshot the JSON before pulling** — a
cookie rotation mid-run once overwrote the only copy of a baseline. Compare against
`TITLE_APPLY_39.applied.v001.json`.

Judge on the **paired ΔCTR of the 30 treated long-forms vs the 13 controls** (§6), never on
levels (§5), restricted to videos with ≥150 before-impressions.

| outcome | verdict |
|---|---|
| treated mean ΔCTR exceeds control by **≥ +0.30 pp** | **WIN** — the 59–100 band transfers to PD. Keep it in the spec and apply it to new episodes. |
| treated − control within **±0.30 pp** | **NULL** — three separate looks will then have found no title effect. Retire the band as a *hard* gate, keep it as a default, and move the effort to thumbnails (`Enok7A7wGBA`, §7). |
| treated falls short of control by **≥ 0.30 pp** | **LOSS** — roll back via §9, starting with the four top performers in §6, and remove the imported Unseen band from spec row 13. |

The ±0.30 pp threshold is the channel's own noise floor: it is roughly the spread already
seen among *untouched* controls between 07-25 and 08-10 (−0.52 to +0.53). **State the
limitation up front rather than discovering it in September:** with control impressions at
12,362 and that much per-video variance, only a large effect will clear this bar. A NULL
result will be genuinely ambiguous between "no effect" and "underpowered" — it should be
read as "stop spending on this lever", not as proof of absence.

**The honest prior:** these rules come from Unseen (1.41M subs), not from PD. PD's own
numbers have now twice failed to show that title shape predicts CTR. This batch was applied
as a **measurement**, not as a fix, and it should be judged as one.

---

## 9. Rollback

```
py -3.11 scripts/apply_title_batch.py --rollback \
    episodes/_planning/measurements/TITLE_APPLY_39.applied.v001.json
```

Restores every pre-change title from the complete `snippet_before` captured before the first
write. Same guarantees as the apply path: `part=snippet` only, no `status` object ever
constructed, description echoed back byte-identical.
