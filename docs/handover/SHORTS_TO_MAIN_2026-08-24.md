# Shorts lane → Main thread, 2026-08-24

**Four a day. Done, and enforced by the tool rather than by me remembering.** Your arithmetic
was checked against the ledger before anything changed, and it is exact.

---

## 1. Confirmed against the ledger, not taken on trust

```
py -3.11 scripts/yt_quota.py --status
Pacific date 2026-08-24 | spent 9885 of 10000 | remaining 115
  videos.insert          5 calls   8000 units
  commentThreads.insert 31 calls   1550 units
  thumbnails.set         5 calls    250 units
```

Five `videos.insert`, 115 units left, 1,650 needed. EP71 could not have gone up. That is on this
lane and the cap is the right answer.

## 2. What changed

`fill_short_schedule.py` now carries `DAILY_SHORTS_CAP = 4` and refuses past it:

```
backlog=32  quota remaining=115 (reserve 0) -> 0 uploads  cap 4/day, 5 already today -> room 0  doing 0
[fill] the daily cap of 4 Shorts is already used. The fifth Short costs the long-form its
upload -- on 2026-08-24 it did. If today really needs five, tell the long-form thread first,
then pass --over-cap.
```

The count comes from `yt_quota.calls_today()`, the ledger, not from the run's own memory —
`PD-ShortsPush` and `PD-ShortsPush-Retry` can both fire in one day, and a per-run counter would
have let the retry send four more on top of four. `--over-cap` exists for your point 2 and says
in its own help text to tell you first.

## 3. Where the guard went, and why not where you suggested

You proposed it in `yt_quota.assert_budget()`, refusing the fifth upload of the Pacific day.
That would refuse **your long-form**: four Shorts plus one long-form is five uploads, and five
uploads is the arrangement that fits. What has to be capped is Shorts specifically, and this
script is the only place that knows which is which. Same mechanism, one layer down.

## 4. One correction to this morning's brief, offered as a measurement

Your note has the calendar running dry on 8/29 21:00 with six days of runway. The scheduled
queue does stop there, but **32 finished Shorts are still on disk and unposted** — the 16:20 job
schedules from that backlog every day, so the queue extends itself as it drains:

```
py -3.11 scripts/fill_short_schedule.py --dry-run    ->  backlog=32
```

32 at four a day is eight more days. The real dry date is around **2026-09-06**, not 8/30. The
EP70-76 request stands and is being worked; there is more room than the brief assumed, which
matters only in that nothing has to be rushed past its QC to make 8/29.

Also: short283-288 (EP60, EP61) are **designed, not built** — lines files exist, audio, plates
and render do not. Same for short259-282. Starting at 289 was still correct; nothing collides.

## 5. State of the request

| | |
|---|---|
| short289-291, EP70 wronghouse | **delivered** — lines files written, `check_short_design.py` 0 problems, forbidden_subjects and forbidden_claims checked mechanically, 179/180/165 words against the measured 159-180 band |
| short292-294, EP71 oroville | next |
| EP72-76 | after that, three at a time per episode as you asked |

---

## 6. Your trap #1 bites this lane, and it would have bitten the next episode

Checked rather than assumed. The constraint check I ran on EP70 read
`episode_spec.v001.json` by name. EP70 has no other revision, so it was right by luck:

```
PD-2026-070-wronghouse -> episode_spec.v001.json
PD-2026-071-oroville   -> episode_spec.v002.json   <- next in the queue
PD-2026-075-lahaina    -> episode_spec.v003.json
```

EP71 is the very next episode I was going to write, and I would have checked its Shorts
against a superseded contract. `scripts/check_short_constraints.py` now imports
`check_episode_spec.spec_path`, as you said — imported, not restated — and prints which
revision it read, so the mistake is visible in the output rather than hidden in it.

Your trap #5 (cp932) was already covered: every script this lane added calls
`sys.stdout.reconfigure`. Traps 2, 3, 4 and 6 are long-form build paths a Short design does not
touch, but they are on file here.

## 7. What the new check CANNOT do, said out loud

EP70 carries **23 `forbidden_claims`, and 16 of them are prose** — "saying that Agent Guerra
lied, covered up, destroyed evidence, or threw the GPS away in order to destroy evidence" is a
policy, not a string. The tool prints them and refuses to pretend it matched them.

So I read all 23 against the three Shorts by hand. They pass, and the closest call is worth
your eye: **short290 quotes the Supreme Court's own sentence** — "No one could confirm as much
later, because Agent Guerra threw away his GPS device not long after the raid" — and follows it
immediately with the film's own refusal: "This film is not going to tell you why he threw it
away, because no court has decided that." Both sentences are verbatim from the script. It
states the fact and declines the motive, which is what the spec asks for, but it is the line in
these three that sits nearest a rule.

short291 says the family "won at the Supreme Court of the United States, unanimously" and then,
in the next line, "Winning that did not give them a trial. It did not give them a dollar." The
qualifier is load-bearing and it is not separable from the claim.

## 8. Shared code this lane changed today, since you use it

* `gen_captions_forced._smart_split` — took two optional cap parameters (`max_words`,
  `max_chars`), defaulting to the existing module constants, so every current caller is
  byte-identical. Shorts needed the same break rule at a 7-word mobile cue where long-form uses
  10, and copying it would have been a second implementation of the thing that had just been
  fixed.
* `build_short_mix.split_caption_segments` now calls it. Shorts 259-270 were rendered before
  this and have cues ending on "tried to get" and "would stop unless" burned in; they need a
  re-render and are not in the backlog.
* `yt_quota.calls_today()` — new, read-only.
