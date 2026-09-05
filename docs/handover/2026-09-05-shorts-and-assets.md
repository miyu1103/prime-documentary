# Handover 2026-09-05 — the shorts + assets lane

Since [2026-08-27](2026-08-27-shorts-and-assets.md) this lane has been on one job: **answer, per
shelf asset, "can I put this in a film?"** — and make that answer visible at the moment a clip is
picked, not in a report nobody opens. That job is done to the limit of what machines and one
person's eyes can do. Everything below is measured; the commands are inline.

---

## 1. State at handover

```
usability record   runs/asset_usability.v001.jsonl — one line per asset, 130,285 assets.
                   --path <file> prints the checklist (rights + technical + theme trust + gaps).
                   Spec: docs/PD_ASSET_USABILITY_CHECKLIST.v001.md. REBUILD AFTER ANY RIGHTS PASS.
rights             review_required 21,652 -> ~9,300 pending today's Freesound batch.
                   13,255 resolved usable so far (wikimedia 5,493 / nara 2,313 / freesound 3,998+ /
                   smithsonian 751 / ia 691+). 836+ examined-and-refused, marked so.
eye review         ALL 68 themes reviewed from 20-tile sheets: docs/shelf/theme_eye_review.v001.json.
                   11 themes / ~19k assets QUARANTINE-grade label rot. Nothing deleted.
AI-generated       357 self-tagged assets found marked usable -> now blocked (invariant 11).
ingest             PD-Ingest-IA scheduled task; completed its second full 20-pass run 09-05 11:27.
                   Check by LOG WRITE TIME, never by process list (S4U shows nothing).
uploads            still PAUSED to 2026-12-31. Untouched.
shorts             untouched since 08-27; that work is the main thread's now.
```

## 2. The rights passes, and what each one proved

Chronology matters here because each pass exposed the next problem.

1. **The shelf's "free" was a claim, not a licence** (08-27). 590 IA rows rested on an
   uploader-typed `licenseurl`. Re-decided from collection membership: 313 restored, 148 refused.
2. **The per-item lookup the shelf had been waiting on was never run** (09-02). The reindex had
   correctly written "must be re-read from the id" into 20,731 rows — and nobody ever did.
   `resolve_item_licences.py` does. Wikimedia's ids are truncated at 60 chars, so those 5,540 are
   identified by the **SHA1 of the file's own bytes** (`allimages&aisha1=`) — 99.2% came back free.
3. **Rate limits are not decisions.** Freesound answers 2,000/day (24h window, not calendar);
   Commons throttled at 0.12s (0.5s is fine). An unanswered row keeps NO verdict so the next run
   retries it. Only answered-and-refused rows are marked.
4. **LOC is unreachable**: five endpoints, all 403, browser UA included. 2,724 rows stay held
   with no path forward short of a human opening pages.

Daily until dry: `resolve_item_licences.py --source freesound` then
`apply_item_licence_verdicts.py --stamp <iso>` (stop the ingest task first — no lock).

## 3. The theme labels are rotten, and the metric could not see it

`sample_theme_sheets.py` (even-stride, 20 tiles/theme) + a word-distinctiveness score
(`check_theme_label_honesty.py`) + **opening every sheet**. The score failed in BOTH directions:

```
police_modern     scored 33.3%   holds ZERO real police (cartoon figurines, CG hover-car)
bank_and_branch   scored 12.1%   is ~75% real American bank buildings ("bank" was in my
                                 generic-word list, which destroyed its own theme)
```

So the per-theme truth is the **eye verdict**, now printed on every asset's checklist:

```
  THEME       courtroom_justice  30.3% on-label  |  eye verdict: QUARANTINE
```

Root cause of the rot: pixabay matches queries a word at a time ("judge bench gavel" →
"bank wooden **bench** relax sea") and the ingest filed whatever came back under the theme it had
asked for. 66% of the shelf (pixabay+extra) was never compared to its own request.

What the eyes found that no gate had: **357 assets self-tagged "ai generated" marked usable**
(now blocked — invariant 11 outranks the licence); a **Mickey Mouse figurine**, a **LEGO
minifigure**, a **Bee Gees record**; brand logos everywhere (IKEA, BMW, Canon, Apple, Harrods);
a **"FREE PALESTINE" door sign** and a **masked woman aiming a firearm at camera** (channel
risks); named identifiable people through `war_history` and `navy_harbor`; two visibly corrupted
files. And `misc` — 26 assets nobody would search — holds handcuffs, a police car, $50 bills and
an employment agreement: more PD-relevant than `courtroom_justice` + `police_modern` combined.

Genuinely good and under-used: `documents_paper`, `period_telephone_tech`, `chicago_city`,
`depression_hardship`, `factory_manufacturing`, `stock_market_exchange`, `weather_disasters`,
`ep70_american_suburb`, `medical_lab`, `civic_voting`, `bank_and_branch`.

## 4. Traps measured this session (each cost a real mistake)

| trap | how it presented |
|---|---|
| `git add` on a `.gitignore`d path exits 0 and stages nothing | **three commit messages described review JSONs that were never in the tree** (`runs/` is ignored, line 17). Artefacts now live in `docs/shelf/`, verified in the index before committing |
| contact sheet grabbed the frame at 1s | every archive film showed its Prelinger title card; 15/20 `ep70_american_suburb` tiles were the identical leader. Now seeks 25% in. **Sheets reviewed before the fix had to be redone** |
| `resolve_item_licences.py` rewrites its output wholesale | applied rows drop out of its view; the file reads as if nothing was resolved. **Derive progress from the LEDGER** (`docs/shelf/rights_progress.v001.json` does) |
| regex `\b` typed in a bash heredoc became a backspace char | "uk" matched inside "bucket", "iran" inside "vibrant". Test both directions after writing any pattern from a heredoc |
| "firefly" in an AI-word list | Firefly Aerospace: 21 genuine NASA rows flagged. Word lists need a false-positive pass |
| C: filled to 3.1GB free; ingest died mid-write | 131GB was git GARBAGE from interrupted GCs + my own killed `git add -A`; `git count-objects -vH` names it. Real history: 7.5GB. Also ~150GB moved to F: via junctions (`out`, `runs`, `_demo`); `.git/objects` still holds ~173GB loose objects, cleanup pending a quiet window |

## 5. What is genuinely not done

* **Freesound tail**: ~2,600 rows after today's batch; one more daily run.
* **LOC 2,724**: no machine path. Decide: leave held forever, or hand-review.
* **IA 648**: `opensource_movies` etc — no evidence exists either way. Recommend: leave held.
* **The quarantine decision**: 11 themes flagged QUARANTINE are still searchable by theme name.
  Nothing was deleted or moved — that is an owner decision. The per-asset checklist now warns,
  but `select_factory_assets --theme courtroom_justice` would still serve mountains.
* **Per-asset pixels**: 121k usable assets, ~1,360 looked at (the sheets). Watermark/face/logo
  sweep of individual assets remains impossible by hand; episode-time contact sheets remain the
  real gate.
* **`.git` loose-object cleanup** (~173GB on C:) — needs no other lane running.
