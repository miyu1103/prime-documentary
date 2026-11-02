# DISTRIBUTION ROLLOUT PLAN v001

**Status: prepared, nothing executed. No YouTube write of any kind was performed.**

- prepared: 2026-07-28
- channel: `UCuQPtAz1rca9eJ4xhvX0yKA` (Prime Documentary)
- measurement: `episodes/_planning/measurements/DISTRIBUTION_STATE.v001.json` (read-only API sweep, 2026-07-27T18:03Z)
- source of the strategy: `episodes/_planning/DEEP_RESEARCH_FINDINGS.v001.md` section 5 (R-25 … R-30)

Every number in this document came from a live API read or from a file in this
repo. Nothing is carried over from the earlier research on trust.

---

## 1. Corrected measured state

The research measured **40 long-forms, 19 missing chapters**. Both figures move once
the enumeration and the render rules are checked properly.

| what the research said | what is actually true | why it differs |
|---|---|---|
| 40 long-forms | **42 public long-forms** | The uploads playlist omits 7 videos the channel owns, 2 of them public long-forms (`bYcqabvvxak` Terry 06-21, `Qyad4FejCIc` Hinton 07-14). Any audit that enumerates from `playlistItems(uploads)` under-counts. This audit unions it with `search.list(forMine=true)`. |
| 19 missing chapters | **22 have no chapter block, and 35 of 42 show no chapters to viewers** | 19 was close on the narrow question ("was a block written?" — the unbroken tail run is 20). But 13 more videos DO have a block that YouTube silently refuses to render. |
| chapters dropped after 7/10 | **after 7/07** | The last long-form with a chapter block is `mj9qEKPRatE` (Milken, 07-07). The run of chapterless videos starts 07-08 (Swartz) and has not broken since — 20 consecutive videos. |

### The bigger defect the research missed

YouTube renders a chapter block only if **every chapter is at least 10 seconds long**.
13 videos have a complete, well-written chapter list that never renders, because of
one line:

```
0:00 Hook: the last sound
0:09 Opening: Pure Waste      <-- 9 seconds. Kills the entire block.
0:46 The dream
```

All 13 have the same cause: a chapter marking the brand sting, 3–9 seconds after its
neighbour. It is not 13 separate mistakes, it is one template defect repeated. Root
cause and per-video evidence: `episodes/_planning/CHAPTER_RESTORATION.v001.md`.

**This contaminates experiment E1 in the research.** E1 proposes restoring chapters to
the 19 chapterless videos and measuring against "the 21 chaptered peers". The real
control group is **7 videos**, not 21. Run E1 against the corrected split or it
measures nothing.

### Full measured state, 42 public long-forms

| lever | state |
|---|---|
| chapters rendering correctly | **7 / 42** |
| chapter block written but not rendering (a chapter under 10s) | 13 |
| no chapter block at all | 21 |
| published with placeholder text `(chapters finalized before publish)` | 1 (`Pmh6h5SfWw4`, Kids for Cash) |
| description links any sibling video | **0 / 42** |
| description links a playlist | 4 / 42 |
| member of any playlist | **6 / 42** |
| has a channel-authored comment thread | 4 / 42 |
| has any external comment thread | 1 / 42 |
| end screens | not readable via any API — assume absent, verify in Studio |

### Playlist state

Two playlists exist, holding 7 distinct videos between them, and both are damaged:

- **Landmark Rights Cases** — position 0 is `PjGEqW6F9WM`, a **deleted video**. That is
  the slot the playlist link lands on. Position 3 is a Short.
- **Fraud, Finance & Power** — position 0 is `waA4XJ9bYcE` (FTX), which has the
  **lowest average view percentage in its cluster (4.24%)**. The worst-retaining video
  is the entry point.

---

## 2. What is scriptable, what is manual, what is owner-only

| class | items | mechanism | who |
|---|---|---|---|
| **API-scriptable** | 4 playlists, ordering, 42 descriptions (chapters + WATCH NEXT), posting comments | `playlists.insert/update`, `playlistItems.*`, `videos.update?part=snippet`, `comments.insert` | script, after owner GO |
| **Studio-manual, no API exists** | end screens ×42, **pinning** each comment, Shorts "Related video" links ×57 | YouTube Studio UI only | owner |
| **Owner-only judgement** | approving the 4 playlist names and orders; rewriting 37 production-internal chapter labels; approving the description rewrite; hand-authoring chapters for 3 videos | — | owner |

Verified, not assumed — `videos.list?part=endScreens` and `?part=cards` both return
**HTTP 400 `unknownPart`** against this channel's own video. There is no end-screen or
card resource in the Data API, and no pin endpoint for comments. Evidence lives in
`api_capability_probes` in the state JSON.

---

## 3. Ranked by expected reach lift × ease

Lift is reasoned from the research's own measurements: PLAYLIST traffic runs
**19.6 min/view against a 3.91 min/view channel average** — 10× — on 1.1% of views,
while 100% of suggested traffic is borrowed from other channels' videos. The channel
has no co-watch edges of its own. Everything below exists to manufacture them.

| # | action | lift | ease | why this rank |
|---|---|---|---|---|
| **1** | **Build the 4 playlists** | **5** | **5** | Turns the highest-value traffic source on the channel from 6 videos into 42. One script, 46 calls, 2,300 quota units of a 10,000/day allowance, fully reversible. Nothing else needs it done first, and items 2, 3 and 4 all depend on it. |
| 2 | Fix the 13 render-broken chapter blocks | 4 | 5 | Deleting one line per video restores chapters on 13 videos using the author's own labels and timestamps. No authoring, no judgement, highest confidence in the batch. |
| 3 | End screens ×42 | 5 | 2 | The strongest co-watch signal YouTube offers, and the only item that cannot be automated. ~2 hours of clicking. Do the top 15 by views first: they hold 85% of all long-form views (the top 10 hold 76%), so the first 45 minutes of clicking captures nearly all of the available lift. |
| 4 | WATCH NEXT block in all 42 descriptions | 4 | 4 | Goes out in the same API batch as the chapters. Currently 0/42 descriptions point at anything of ours. |
| 5 | Restore the 21 missing chapter blocks | 3 | 3 | 32 of 35 targets have a staged block, but 37 labels still read "Hook" / "Ending" / bare act names and must be rewritten before publishing — YouTube indexes chapter text for key-moment search, and "Hook" matches nothing a viewer would type. |
| 6 | Pinned comments ×42 | 2 | 2 | Posting is scriptable; pinning is 42 manual clicks. The research itself notes the channel has 1 external comment thread total, so the funnel has little to work with yet. Bundle it with the end-screen session rather than making a separate pass. |
| 7 | Feeder-lane rule for new episodes (R-29) | 4 | 5 | Costs nothing and compounds, but it is a process change for future episodes, not a back-catalogue action. Apply it at the next topic brief. |

**Highest-value first action: build the 4 playlists.** It is simultaneously the
largest lift and the easiest, it is fully reversible, and items 2–4 all reference the
playlist ids.

---

## 4. Execution order

Order matters — steps 2 and 4 embed ids produced by step 1.

| step | action | depends on | effort | artifact |
|---|---|---|---|---|
| 0 | Owner reads and approves the playlist design | — | 15 min | `config/distribution/series_clusters.v001.json`, `PLAYLIST_PLAN.v001.md` |
| 1 | Remove the deleted item from Landmark Rights Cases | 0 | 1 call | `PLAYLIST_PLAN.v001.json` step list |
| 2 | Create 2 new playlists, retitle 2, insert/reorder 41 items | 1 | 46 calls, ~5 min | same |
| 3 | Write the 2 new playlist ids back into the cluster config | 2 | 2 min | config |
| 4 | Re-run `stage_description_batch.py` so WATCH NEXT carries real playlist URLs | 3 | 1 min | `DESCRIPTION_BATCH.v001.md` |
| 5 | Owner rewrites the 37 production-internal chapter labels | — (parallel with 1–4) | ~45 min | `CHAPTER_RESTORATION.v001.md` |
| 6 | Owner hand-authors chapters for the 3 blocked videos | 5 | ~30 min | below |
| 7 | Owner reviews the 42 description diffs line by line | 4, 5, 6 | ~40 min | `DESCRIPTION_BATCH.v001.md` |
| 8 | Apply the description batch | 7 | 42 calls, ~5 min | needs an executor, see §7 |
| 9 | End screens in Studio, highest views first | 2 | ~2 h | `END_SCREENS_WORK_ORDER.v001.md` |
| 10 | Post + pin comments during the same Studio session | 2 | ~1 h | `PINNED_COMMENTS.v001.md` |
| 11 | Re-measure after 4 weeks | 8, 9 | 2 min | re-run `yt_distribution_state.py` |

**Success metric (from the research):** any of our own videos appearing in the
`insightTrafficSourceDetail` suggested-feeder table within 8 weeks. Baseline is 0 of 25.

### The 3 videos that need chapters written by hand

| video | episode | why the repo could not supply them |
|---|---|---|
| `SOu4Y1NkGGY` Florence | PD-2026-037 | `03_script/script.en.v001.md` is continuous narration with no act headings, and there is no `script.annotated.json` |
| `tYZuE76Hwdc` Thompson | PD-2026-041 | `03_script/` is empty; the planning docs carry no act structure |
| `X40EbUw5kzQ` Frazier | PD-2026-039 | `script.annotated.stub.json` has placeholder titles only (`ACT I`…`ACT IV`) and its OPENING span does not align to the caption track |

---

## 5. Rollback, per change class

| change class | reversible | procedure | residue |
|---|---|---|---|
| `playlists.insert` | yes | `playlists.delete` on the returned id | none, if no description links it yet — which is why step 4 comes after step 3 |
| `playlists.update` (retitle/description) | yes | re-PUT the `was_title` / `was_description` captured for every update call in `PLAYLIST_PLAN.v001.json` | none |
| `playlistItems.insert` | yes | `playlistItems.delete` | none |
| `playlistItems.update` (reorder) | yes | re-PUT the `was_position` captured in the plan | none |
| `playlistItems.delete` (the dead item) | **no** | — | none worth restoring: it points at a deleted video |
| `videos.update` (description) | yes | `description_before` is stored verbatim for all 42 videos in `DESCRIPTION_BATCH.v001.json`; re-PUT it | **`videos.update?part=snippet` replaces the whole snippet.** Title, tags, category and language must be re-sent or they are cleared. The executor must read the live snippet immediately before each write and merge. |
| end screens | yes | Studio → Editor → End screen → delete element | none; the video file, id and watch history are untouched |
| `comments.insert` | yes | `comments.delete`, or delete in Studio | the comment may have been seen; there is no silent undo |
| pinning | yes | unpin in Studio | none |

Nothing in this plan alters a video file, an id, a publish state, or a schedule. The
riskiest class is the description batch, and its risk is the snippet-replacement
footgun above, not the text itself.

---

## 6. Cost

| resource | amount |
|---|---|
| YouTube API quota, playlists | 2,300 units |
| YouTube API quota, descriptions | ~2,100 units (42 × 50) |
| YouTube API quota, comments | ~2,100 units (42 × 50) |
| daily allowance | 10,000 units |
| paid API spend | **none** |
| GPU | **none** |

Split the description and comment batches across two days, or the day's reads get
squeezed.

---

## 7. What is deliberately not built

`plan_series_playlists.py --execute` **refuses to run** even with every flag supplied.
The executor is intentionally unimplemented. Building it before the owner has approved
`PLAYLIST_PLAN.v001.md` would put a live-channel write path one typo away from firing,
and the guard would then be the only thing between a draft and 46 writes.

When it is built it must: re-read live state immediately before each call, verify each
response before the next call, write an idempotency record per call, and merge rather
than replace video snippets.

---

## 8. Artifacts

| file | what it is |
|---|---|
| `scripts/yt_distribution_state.py` | read-only audit, GET only, no write path |
| `scripts/stage_chapter_restoration.py` | offline chapter recovery, no network |
| `scripts/stage_description_batch.py` | offline description + comment staging, no network |
| `scripts/plan_series_playlists.py` | dry-run planner with a hard `--execute` guard |
| `scripts/plan_end_screens.py` | Studio work order generator |
| `config/distribution/series_clusters.v001.json` | the design — the file the owner approves |
| `episodes/_planning/measurements/DISTRIBUTION_STATE.v001.json` + `.md` | measured state |
| `episodes/_planning/CHAPTER_RESTORATION.v001.md` | 35 chapter blocks, line by line |
| `episodes/_planning/DESCRIPTION_BATCH.v001.md` | 42 unified diffs |
| `episodes/_planning/PINNED_COMMENTS.v001.md` | 42 comment drafts |
| `episodes/_planning/END_SCREENS_WORK_ORDER.v001.md` | 42-row click path |
| `episodes/_planning/DISTRIBUTION_APPROVAL_RECEIPT.template.md` | the approval record |
