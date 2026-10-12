# Handover 2026-08-27 — the shorts + assets lane

Two things happened today: the CTA card was fixed across the back catalogue and 33 Shorts were
re-rendered, and the shelf's rights basis turned out to be a claim rather than a licence. The
ingest also stopped being this lane's problem — see §4.

Yesterday's document is still current for the Shorts pipeline itself:
[2026-08-26](2026-08-26-shorts-and-assets.md). **Its §9 recipe is obsolete** and §4 below replaces it.

---

## 1. State at handover

```
short310-327   18 RENDERED, 52.1-57.7 s, three gates clean, no shipping blocker left.
short322-324   UNBLOCKED. EP81's thumbnail was rebuilt inside the episode's own scope (§3).
short271-282   12 re-rendered: they now HAVE a funnel card, which they never had.
short289-309   21 re-rendered: their CTA cards no longer read "246 Died in the Texas Freeze. The".
shelf          67,598 free_commercial | 40,474 pd | 21,652 review_required | ledger PASS
ingest         a Windows scheduled task now. NOT a session job. See §4.
uploads        PAUSED until 2026-12-31. Unchanged, owner decision.
```

## 2. The CTA card had three defects, all reaching the back catalogue

Found by looking at rendered frames, not at exit codes.

| defect | measured | fix |
|---|---|---|
| no funnel cut at all | short271-282: plates tagged `role: "close"`, and only `"loop"` fires the card — while the designs already said `loop: true` with a `loop_join` | 16 plates retagged |
| card shows internal shorthand | EP69's design said `"Non-Delegable"`; the episode published as *"One Rod Became Two. The Load on One Beam Doubled."* | `destination_title()` reads the package **before** `design.destination.title`, which also goes stale on every retitle |
| title ends mid-clause | `"A Camera Watches the Woods for 78"` | falls back to ASCII dots so the shortening reads as deliberate |

**Still true and not fixed**: 62 Shorts (short01-66 and 82) have no funnel card. They are an older
format and were left alone deliberately. **short271-282 also run 26.4-44.5 s**, under the 45-57 s
band — that is their original narration, not a regression: no `_timing` file changed.

## 3. EP81's thumbnail said something EP81 forbids

`"100 COUNTS."` was **sourced, not invented** — `EP78-82_PREMISE_VERIFICATION.v001.md` records
no-contest pleas to 100 counts each. It was out of *scope*: that episode's ledger says
`"Until it is, no charge, no plea, no sentence and no name may"` appear, and all three thumbnail
candidates on disk said one. Three Shorts were carrying it on their funnel card.

Rebuilt with `build_case_thumbnails_from_plates.py` from the episode's own plates, headlines taken
from its script: **TWO DOORS. ONE DOOR.** (`script.en.v001.md:9` + `:13`, selected),
FIFTEEN SECONDS. (`:73`), IT DID NOT IGNITE. (`:76`).

All five EP78-82 title+thumbnail pairs now pass `check_packaging_claims` **together**, rc=0, and
the checked pair is written into each `_title_draft.v001.json`. Those titles are still
`draft_awaiting_owner_approval`; changing one means re-rendering that episode's three Shorts.

EP78's `"FAILED BEFORE."` was kept on purpose: sourced to CO-402/404/405, absent from
`forbidden_claims`, and short315 spends its whole runtime giving the 13.1 per cent first-attempt
failure rate so the record cannot be read as the mark of a dangerous man. The hook pulls and the
film corrects. A person should still look at it.

## 4. Never launch the ingest from a chat session again

The main thread registered `PD-Ingest-IA` as a scheduled task tonight
([their note](MAIN_TO_SHORTS_AND_ASSETS_2026-08-27.md)) and killed the foreground copy this lane
had running. **The script has no lock of its own**, and the task's `IgnoreNew` guard only sees other
task instances — a hand-launched copy is an invisible second writer, which is how the ledger was
corrupted before.

```powershell
Get-ScheduledTask -TaskName 'PD-Ingest-IA' | Get-ScheduledTaskInfo   # 267009 = running
Get-Content 'C:\Users\aab15\Documents\prime-documentary\runs\ingest_scheduled.log' -Tail 3
```

**The process list is not the instrument to use here.** The task runs S4U in another session, so
`Get-CimInstance Win32_Process` shows *nothing* matching `ingest_archive_sources` even while it is
working. Measured at 22:47 tonight: zero matching processes, and the log had been written at
22:46:53. **Believe the log's write time, not the process list.**

## 5. The shelf's "free" was a claim, not a licence

`ingest_archive_sources.py` read the item's own `licenseurl` and believed it:

```python
elif "publicdomain" in licurl:
    decision, raw = "pd", licurl
```

On archive.org that field is typed by whoever uploaded the file. **590 rows across the whole shelf
rested on it**, including a Blu-ray remux of a 1964 feature, `Killer Klowns From Outer Space 1988
1080p`, `Robocop: The Animated Series`, a New Kids On The Block concert, a 2017 McDonald's
advertisement and a run of 1996 station recordings whose content is brand advertising. It is the
same mechanism that put Sesame Street on the shelf on 2026-08-25 — and **the title denylist written
that day caught 0 of these**, because none of them look like the last batch.

Only a curated *collection* is evidence now. `collection:prelinger` still yields `pd`; an
uploader-set `licenseurl` yields `review_required` and says so in the raw field.

### The 590 were then decided from collection membership, not from titles

A title says what an uploader called a file. A collection says where archive.org *put* it, which
is the one signal on that site an uploader cannot set. `audit_ia_collections.py` fetches it;
`apply_ia_collection_verdicts.py` writes the verdict back. Deliberately two scripts: the network
step can be re-run any number of times without touching the ledger.

| bucket | n | what it is |
|---|---|---|
| free | 135 | archive-curated PD: prelinger, usgovfilms, us_congress, californiarevealed, nara |
| public_access | 178 | **the creator IS the rights holder** — 174 are "City of East Grand Forks" uploading its own council recordings, plus Albany, Belmont, Beech Street Center |
| paywalled | 99 | collections of other people's copyrighted work |
| unsafe | 49 | archive.org's own `deemphasize` flag, plus fringe / offcenter / jan6archives — a channel risk, not a rights one |
| eyes | 129 | **116 are `opensource_movies`**, the generic anyone-can-upload bucket, which carries no evidence at all |

**313 restored, 148 refused, 129 still held.** The 148 carry `rights_verdict: "reject"` so a later
pass can see they were examined and refused rather than never looked at.

The 129 should probably stay held forever. Looking at them will not help: **you cannot see a
copyright in a picture**, and `opensource_movies` membership tells you nothing either way.

Ledger backed up before each write; `check_ledger_integrity` PASS after both.

## 6. What is left

* **`install_ingest_task_admin.ps1` is now redundant** — the main thread registered the task. Kept
  as the record of what the action should be, since the old one pointed at `H:\pd-media\...`, an
  alias that evaporates on reboot, and had failed with result 1 on every fire.
* **Whether the IA lane should be on at all is still open.** Four ingest tasks were disabled on
  2026-08-10 on the finding that the shelf was already large enough; only `PD-Ingest-IA` is back on.
  Measured today: 33 hours of running added **914 items / 270 GB**, of which 42 per cent landed in
  `review_required`. That is +0.6 per cent on a 129k shelf. The lane is not short of material.
* **62 Shorts still have no funnel card** (short01-66, 82).
* **The mislabelled-shelf problem is untouched.** Nothing in today's work reads a pixel.
