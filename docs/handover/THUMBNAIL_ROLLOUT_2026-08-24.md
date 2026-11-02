# Thumbnail rollout plan — the new set into the calendar

Written 2026-08-24 23:20 JST, after the thumbnail lane delivered EP71–76 (plus EP77–82 and EP35)
in the winner style. This says how they reach the channel, what is automatic, and the one decision
that is not.

---

## 1. What is already wired, and needs nothing

`upload_schedule_case_v001.py:771` resolves the thumbnail as
`sorted(PKG.glob("thumbnail.selected.v*.png"))` — **the highest revision at upload time**. The new
files are `thumbnail.selected.v001.png` in each `09_package/`, in place since 22:15.

`PD-LongformPush` runs daily at 16:05 and calls that script. So:

| upload | episode | thumbnail it will carry |
|---|---|---|
| 8/25 16:05 | EP71 oroville | **the new one** — `188,000 / OUT.` |
| 8/26 16:05 | EP74 itaewon | the new one — `3.2 METRES.` |
| 8/27 16:05 | EP75 lahaina | the new one — `NEVER USED.` |
| 8/28 16:05 | EP76 morandi | the new one — `98%` |
| 8/29 16:05 | EP72 lacmegantic | the new one — `NO ONE ABOARD.` |
| 8/30 16:05 | EP73 uri | the new one — `$9,000` |

**No action required for any of these.** Nothing to remember, nothing to type. The upload sets the
thumbnail in the same call that books the slot.

## 2. The one episode that is not automatic: EP70 wronghouse

EP70 went public today at 12:00 (`1nxecNneBVk`) carrying the thumbnail made before the winner
style existed. Replacing it is one call, `thumbnails.set`, **50 quota units**, and there is a
generic tool for it: `scripts/set_video_thumbnail.py --video-id 1nxecNneBVk --file <png> --apply`
(dry-run by default, writes a receipt).

It is not automatic because it is a change to a live video, and because there is a reason to wait:

* **EP35 is the measured test.** The lane replaced its thumbnail live today and recorded the
  baseline — 28-day window, 7,436 impressions, CTR 1.00%. That is the first clean before/after the
  channel has ever had on this style.
* EP70 has been public for hours, not days. Swapping now mixes two variables — a new style AND a
  video still in its first-day surge — and neither number will mean anything afterwards.

**Recommendation: leave EP70 alone until EP35's numbers move**, then swap it with the same tool and
record its own baseline first. That is an owner call, not mine, and it costs 50 units whenever it
is made.

## 3. What the lane still owes, and what it does not

**Does not owe anything for the six episodes above.** They are delivered and in place.

Two open items, neither blocking a publish:

1. **EP74 has one A/B variant, not three.** `thumbnail_ready` wants ≥3 candidates plus a selection;
   EP74's raw plate stock is a single `T01_bg.v002.png`, the rest being older files with type
   already burned in. Either two more raw plates get ordered, or the episode ships with the
   deviation recorded. EP74 uploads 8/26, so there is a day for the first option.
2. **EP81 station and EP82 valdez headlines have no record to check against** — their scripts are
   still stubs, so `check_packaging_claims` had zero rows to match. **Those two must be re-run
   after `script_verified`.** Recorded here because the check passing on an empty record is exactly
   the kind of green that means nothing.

## 4. What this thread does NOT do to them

The 150 px text-height floor in `check_thumb_subject_luma` **does not apply to this style and will
not be enforced against it.** The lane measured the channel's live best-CTR thumbnail at ~94 px of
text; my floor came from a single EP31 pair. Their evidence is CTR, mine was a calibration set, and
CTR wins. Where their thumbnails fail that check, the failure is the check's, and it is recorded
rather than fixed by making the type bigger.

One change to that gate was kept, because it is not about this style: `outline` used to count dark
rings starting at the glyph's own antialiasing, so it could only ever see a PAINTED stroke and
scored every shipped thumbnail on the channel 0 px — including the live EP77–82 set. It now skips
the antialias band and also credits plain contrast, and it still returns 0 for white type on a
white field. The floor was not lowered.
