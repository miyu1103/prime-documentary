# TikTok scheduled posting

TikTok has no scheduling API for this account, so posting runs through TikTok Studio in a real
Chrome window driven over CDP. `schedule_shorts_tiktok.js` uploads each queued Short, sets a
future date and time, and submits - four a day by default.

## Running it

```bash
node scripts/tiktok/start_chrome.js         # dedicated profile, port 9222; log in once by hand
node scripts/tiktok/schedule_shorts_tiktok.js 2026-08-11 [slots-already-used-on-day-1]
```

The queue is `C:/temp/studio_auto/tt_queue.json` - `[{short, file, caption}, ...]`. Results append
to `tt_clean_result.jsonl`, and a Short already recorded as `SCHEDULED` is skipped, so an
interrupted run resumes. Three failures in a row stop the batch.

Chrome's default profile refuses `--remote-debugging-port` and the profile directory cannot be
copied (App-Bound Encryption, Chrome 127+). A dedicated `--user-data-dir` logged in once by hand
is the only way in.

## Five things that each looked like a different bug

Every one of these produced a run that posted nothing and reported something misleading. They are
listed because the next person will hit them in the same order.

1. **The date and time fields are readOnly.** Assigning `.value` is silently ignored. They open
   pickers.
2. **Searching the whole document for the day number finds the time dropdown.** The hour list also
   contains "11". The symptom was the clock changing and the date never moving. The day search is
   scoped to the calendar grid, found via its `8月 / 2026` header.
3. **`toISOString()` shifts the day.** From JST a local midnight lands on the previous day in UTC,
   so asking for 08-11 scheduled 08-10. The date is formatted from local parts.
4. **A leftover draft blocks everything.** A run that never submitted leaves one, and the uploader
   asks whether to continue editing. 破棄する has to be pressed TWICE - the banner button only
   opens a confirmation dialog, and that dialog is a modal overlay: with it open, every later
   click goes to the overlay, the date picker never opens, and the log says "calendar never
   opened" while a screenshot shows the dialog waiting.
5. **A programmatic `.click()` does nothing** on the calendar cell or on 投稿予約する - these
   listen for a real pointer sequence. Both are marked with an attribute, then clicked through an
   ElementHandle so the browser generates the events.

And the one that mattered most: **TikTok runs its own music-copyright and content checks after the
upload**, and submitting before they finish pops "投稿に進みますか？ 著作権侵害のチェックが完了して
いません" and *stops the check*. A copyright strike is the one failure this channel cannot absorb,
so the script waits for both checks to come back clean instead of clicking through the warning.
Only then does it answer the dialog, if it still appears.

## The AI-generated label

Every one of the 127 videos uploaded before 2026-08-08 carries a "creator labelled this
AI-generated" badge, traced to Remotion's container comment (`Made with Remotion 4.0.476`).
`render_shorts_tiktok.sh` strips container metadata with `-map_metadata -1` as a re-mux, and the
same footage then shows the AI-generated switch OFF in the uploader. The script re-reads that
switch before every post and refuses to continue if it is on.

## The cover, and two ways of being lied to about it

TikTok picks its own frame when no cover is set, and this channel's Shorts open on a near-black
frame. Measured on the live profile on 2026-08-09: a hundred identical black tiles with unreadable
subtitle text on them. The cover cannot be changed afterwards - on a posted or scheduled item every
edit control in Studio renders with `cursor: not-allowed` - so it has to be attached during upload,
and a post that went up without one has to be deleted and replaced.

Both of these produced a run that reported success and delivered nothing:

1. **The editor appears while the file is still uploading** - measured at 57%. A cover set before
   the video lands is discarded when TikTok finishes processing and generates its own frame. Wait
   for `アップロード完了`.
2. **"cover set" only meant a button was clicked.** The script now reads the cover thumbnail's
   image src before and after, and returns `COVER_DID_NOT_STICK` if it did not change.

One more thing that looks like a failure and is not: the public profile grid shows a *video frame*
for a scheduled post, not the cover. Check the Studio list instead - its row thumbnail is the real
cover. Two hours were spent chasing this before looking in the right place.
