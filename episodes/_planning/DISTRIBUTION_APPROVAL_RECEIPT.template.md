# DISTRIBUTION APPROVAL RECEIPT — template

Copy this file to `episodes/_planning/approvals/APR-XXXX_distribution_v001.md`,
fill it in, and commit it. Nothing in the distribution rollout may run until the
matching section below is signed.

Per `.claude/rules/16-approval-boundaries.md`, approval targets an **exact revision**
and cannot be inferred from conversation. Per `.claude/rules/08-destructive-actions.md`,
each outward-facing class is approved separately — approving the playlists does not
approve the description batch.

---

## Identity

| field | value |
|---|---|
| approval id | `APR-____` |
| date | |
| approver | |
| channel | `UCuQPtAz1rca9eJ4xhvX0yKA` |
| plan | `episodes/_planning/DISTRIBUTION_ROLLOUT_PLAN.v001.md` |
| design revision | `config/distribution/series_clusters.v001.json` **v001** |
| measurement | `episodes/_planning/measurements/DISTRIBUTION_STATE.v001.json` measured `2026-07-27T18:03:08Z` |

### Revision binding

Record the hashes at approval time. If any differs when the change runs, the
approval is void and must be re-taken (invariant 12).

```
sha256  config/distribution/series_clusters.v001.json         ____________________
sha256  episodes/_planning/measurements/PLAYLIST_PLAN.v001.json    ____________________
sha256  episodes/_planning/measurements/DESCRIPTION_BATCH.v001.json ____________________
```

Regenerate with:

```
python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" <path>
```

---

## Class A — Series playlists

Reviewed: `episodes/_planning/PLAYLIST_PLAN.v001.md` (46 calls, 2,300 quota units).

- [ ] The 4 playlist **titles** are approved as written
- [ ] The **descriptions** are approved as written
- [ ] The **ordering** and each **entry point** are approved
- [ ] I accept retitling "Landmark Rights Cases" → "Police Power: What They Can Actually Do to You", and that 4 live descriptions currently name the old title
- [ ] I approve deleting the dead item `PjGEqW6F9WM` from position 0 (not reversible; it points at a deleted video)
- [ ] Renaming the research's "Unsolved & Disaster" cluster to "The System Got It Wrong" is approved

Deviations from the design I am approving instead: _______________________________

**Approved / Rejected / Approved with changes:** ______   signature: ______

---

## Class B — Description batch (42 videos)

Reviewed: `episodes/_planning/DESCRIPTION_BATCH.v001.md`, all 42 diffs.

- [ ] I read every diff, not the summary table
- [ ] The 37 production-internal chapter labels ("Hook", "Ending", bare act names) have been **rewritten**, and the rewrites are in the staged blocks
- [ ] Chapters for the 3 blocked videos (`SOu4Y1NkGGY`, `tYZuE76Hwdc`, `X40EbUw5kzQ`) are either authored or explicitly excluded from this batch
- [ ] WATCH NEXT blocks carry **real** playlist URLs, not the `<PLAYLIST URL - fill in…>` placeholder
- [ ] The first two lines of every description are unchanged
- [ ] I accept that `videos.update?part=snippet` replaces the whole snippet, and the executor must merge title/tags/category/language rather than re-send blanks

Videos excluded from this batch: _______________________________________________

**Approved / Rejected / Approved with changes:** ______   signature: ______

---

## Class C — Comments

Reviewed: `episodes/_planning/PINNED_COMMENTS.v001.md`.

- [ ] The 4 cluster templates are approved as written
- [ ] I accept that a posted comment is publicly visible immediately and that deleting it is not a silent undo
- [ ] Pinning is manual and I will do it in the same Studio session

**Approved / Rejected / Approved with changes:** ______   signature: ______

---

## Class D — End screens (Studio, manual)

Reviewed: `episodes/_planning/END_SCREENS_WORK_ORDER.v001.md`.

- [ ] I confirm end screens cannot be set by any API and this stays manual
- [ ] Slot 1 = next video in the cluster, slot 2 = series playlist, is approved
- [ ] Scope: all 42 / top ____ by views (circle one)

**Approved / Rejected / Approved with changes:** ______   signature: ______

---

## Execution record (fill in AFTER running)

| class | started | finished | calls made | failures | quota used | operator |
|---|---|---|---|---|---|---|
| A playlists | | | | | | |
| B descriptions | | | | | | |
| C comments | | | | | | |
| D end screens | | | | n/a | n/a | |

New playlist ids created:

```
forfeiture_files      PL____________________
system_got_it_wrong   PL____________________
```

- [ ] New ids written back into `config/distribution/series_clusters.v001.json`
- [ ] `stage_description_batch.py` re-run so WATCH NEXT carries the real URLs
- [ ] `yt_distribution_state.py` re-run; the new state file is committed as the post-change baseline

## Rollback record (only if rolled back)

| what | when | why | restored from | verified by |
|---|---|---|---|---|
| | | | | |

---

## Re-measure at +4 weeks

Target date: __________

- [ ] `yt_distribution_state.py` re-run
- [ ] `insightTrafficSourceDetail` pulled — **is any of our own videos now a suggested feeder?** (baseline: 0 of 25)
- [ ] Playlist traffic share vs the 1.1% / 19.6 min-per-view baseline
- [ ] E1 chapter experiment read against the corrected control group of **7** already-rendering videos, not 21
