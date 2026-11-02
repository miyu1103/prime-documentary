# YouTube Studio UI automation — related video

The related video on a Short is the only official route YouTube gives a Short for sending a viewer
to a long-form. It exists **only in the Studio web UI**: there is no Data API field for it
(`part=relatedVideo` does not exist) and no Analytics API field for it. So it is set the way a
human sets it — in a real, signed-in Chrome, one video at a time — and every save is proved by
reading the control back after a reload.

## One-time step the owner has to do (about 60 seconds)

Everything else here is automatic. This one step cannot be automated, because Google refuses to
accept a sign-in inside an automation-controlled browser.

```bash
node scripts/studio/start_chrome.js
```

A Chrome window opens on YouTube Studio using the dedicated profile
`C:/temp/studio_auto/work_profile`. If it shows the channel, there is nothing to do — the session
is already there and this step is finished. If it shows a Google sign-in page, sign in to the
Prime Documentary channel by hand. That is the whole task; the session then persists in the
profile directory and later runs reuse it.

Leave that window open while the batch runs.

Why a dedicated profile: Chrome refuses `--remote-debugging-port` on the default profile, and
since Chrome 127 a profile directory cannot be copied (App-Bound Encryption). A separate
`--user-data-dir` signed in once by hand is the only way in. That directory holds a live Google
session, so it stays outside the repository and is never copied into it.

## Running the batch

```bash
node scripts/studio/related_link_batch.js --verify-only   # read every field back, change nothing
node scripts/studio/related_link_batch.js --dry-run       # list what it would set
node scripts/studio/related_link_batch.js                 # set what is missing
```

Roughly 12 seconds per Short when the field is already correct and about 45 when it has to be
set, so a full pass over the 81 currently eligible Shorts is 15-25 minutes. Rows already recorded
as done are skipped, so a second pass is fast.

Useful flags: `--only <shortVideoId>` (must be in the worklist), `--limit N`,
`--worklist <path>`.

## What it reads, and what it refuses

**Input is the worklist, never a typed list.** The set of short ids in it is the allowlist:
`--only` with anything else is refused before a browser is even opened, and a row without a
`longform_video_id` is not eligible.

The v001 worklist (`runs/_cache/related_link_worklist.json`, 54 rows) was built by hand and had no
generator, so it went stale the day the next long-form went public. Rebuild it instead:

```bash
py -3.11 scripts/studio/build_related_link_worklist.py            # writes v002 json + markdown
node scripts/studio/related_link_batch.js --worklist runs/_cache/related_link_worklist.v002.json
```

That reads the live channel and emits a destination only where one can be justified, recording the
justification per row in `destination_source`: `legacy+description` (the legacy map and the
Short's own description name the same long-form), `description`, or `legacy`. A Short with no
justified destination goes to `unresolved` with a reason — never to a guess. A destination that is
not public goes to `not_yet_public`, because Studio cannot select a private video in the picker.

**It never touches privacy, publish date, title or description.** Those four fields are read from
the Data API before and after the run and compared; any movement fails the run with exit code 4
and the detail is written to `runs/related_link/metadata_guard.json`. A past-dated `publishAt`
publishes a video immediately, which is why this is a guard and not a comment.

**It never guesses which video to link.** The picker is searched by the long-form *video id*
first, which is unique; the title is only a fallback. If no card matches the intended long-form
the dialog is closed and the row is recorded `NO_MATCH`.

**It never records a success it has not seen.** After saving, the page is fully reloaded and the
related-video control is read back. The row is `VERIFIED` only if the reloaded label contains the
intended long-form title, and the exact label string is stored in the ledger. Three failures in a
row stop the batch instead of grinding through a broken UI.

## Resuming, and where the evidence lives

- `runs/related_link/ledger.jsonl` — one line per short per attempt: status, the exact label read
  back, whether the picker matched by id or title, timestamp. A short whose latest line is
  `VERIFIED` or `ALREADY_SET` **for the same target** is skipped on a re-run, so an interrupted
  batch resumes.
- `runs/related_link/metadata_guard.json` — the before/after snapshot and its diff.
- `runs/related_link/shots/<videoId>.png` — a screenshot for any row that did not resolve.

Statuses: `ALREADY_SET` (the field already pointed at the intended long-form; nothing was clicked)
· `VERIFIED` (set by this run and read back) · `NOT_SET` (verify-only found it empty or pointing
elsewhere) · `NO_MATCH` (with the card titles it did see) · `NO_CONTROL` · `NO_PICKER_INPUT` ·
`NO_SEARCH_BOX` · `NOT_VERIFIED` · `ERROR`.

Each video gets a fresh tab. Studio stacks a `tp-yt-paper-dialog` every time the picker opens and
never removes the old ones — nine were counted in one reused tab — and past a few the search input
in the newest dialog stops being reachable. Three videos failed `NO_SEARCH_BOX` that way on
2026-08-09 and each succeeded first try in a fresh tab. Escape and the close button are not
sufficient; the new tab is what fixed it.

Exit codes: 0 clean · 1 refused/crashed · 2 no debug Chrome on 9222 · 3 profile not signed in ·
4 metadata guard tripped · 5 a row did not verify.

## Measuring whether it worked

The whole point is the `SHRT` traffic-source column on the long-forms, which was 0 across all 12
measured episodes. Analytics runs about two days behind, so measure a window that ends at least
two days ago:

```bash
py -3.11 scripts/yt_funnel_analytics.py 2026-08-07 <a date at least 7 days later>
```

`yt_funnel_analytics.py` prints the per-referrer RELATED_VIDEO list, not the per-video `SHRT`
column from `docs/PD_SHORTS_RELATED_VIDEO_LINKING.v001.md` — that table was assembled by hand and
had no script. It does now:

```bash
py -3.11 scripts/studio/measure_shorts_to_longform.py 2026-08-07 <end date, 2+ days ago>
```

One Analytics request per destination long-form, printing views / REL / SHRT / SUB / SRCH / EXT /
PL per episode and a total. Baseline measured 2026-08-09 over 2026-07-25..08-07, before the links
could have had any effect: **890 views across the destinations, REL 578, SHRT 0.** SHRT moving off
zero, or REL rising with Short ids appearing in section 1 of `yt_funnel_analytics.py`, settles it.

Analytics lags about two days. Measured 2026-08-09: the window 08-07..08-09 returned an entirely
empty report while 08-01..08-07 returned a full one. An end date inside the last 48 hours looks
like a catastrophic result and is not one.

## Language

Studio renders in the account language. Both the Japanese and English control labels are matched
(`すべて表示`/`Show more`, `保存`/`Save`, `自分の動画`/`your videos`). If Studio ships new wording
the batch fails loudly with a screenshot rather than clicking something else.
