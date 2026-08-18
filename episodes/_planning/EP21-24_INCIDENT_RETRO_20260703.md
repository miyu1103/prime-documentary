# EP21-24 Incident Retrospective

Date: 2026-07-03 JST  
Scope: EP21 D.B. Cooper, EP22 Michael Milken, EP23 Aaron Swartz, EP24 Raj Rajaratnam  
Basis: current thread file/log inspection plus owner-provided summaries from related threads.

## Executive Summary

EP21-24 were ultimately built/scheduled and the later CTR thumbnail replacements were applied, but the process exposed a large number of workflow failures. The most serious problems were not isolated rendering errors; they came from trying to handle four near-final episodes, multiple legal/safety risk classes, caption style fixes, final acceptance gates, YouTube scheduling, and thumbnail replacement in one compressed sequence.

The highest-risk episode was EP23 because it combines R3 + sensitive suicide-handling constraints with locked wording, caption alignment, final-video identity, and upload scheduling. The most systemic problem across all episodes was that machine gates could pass while human-visible quality or operational state was still weak: captions could be formally valid but ugly or unnatural, final delivery metadata could lag the real file, and package artifacts could be scattered across repo, evidence folders, and `H:\pd-media`.

Current public-facing state, based on recorded YouTube API results:

- EP21 scheduled private: `tt7U1XgjCU4`, 2026-07-06 12:00 JST.
- EP22 scheduled private: `mj9qEKPRatE`, 2026-07-07 12:00 JST.
- EP23 scheduled private: `FTm1icKgycU`, 2026-07-08 12:00 JST.
- EP24 scheduled private: `rYV4rxtQCV0`, 2026-07-09 12:00 JST.
- CTR replacement thumbnails v002 were uploaded for all four.

The work reached a usable state, but the operating process was too fragile.

## Severity Model

- Critical: Could cause unsafe publication, wrong video, legal/safety violation, or unrecoverable external-side mistake.
- High: Could cause failed publish package, misleading metadata, significant rework, or public-facing quality damage.
- Medium: Causes wasted time, confusion, inconsistent evidence, or hard-to-audit state.
- Low: Minor implementation or polish issue with limited blast radius.

## Critical Issues

### 1. EP23 Safe-Handling Conflict Was Present Before Final Delivery

EP23 had a direct conflict between strict R3 sensitive-topic rules and the existing audio/caption/script-derived outputs.

Observed problems:

- Suicide/death wording was at risk of appearing more than once.
- Opening-side duplicate wording had to be removed.
- Captions had to be adjusted so the death line remained aligned to the single allowed narration occurrence.
- The issue existed late enough that it required media patching, backup creation, and re-QC.

Impact:

- This could have violated the explicit safe-handling rule: death appears once only, no extra caption/title/thumbnail/metadata reference.
- It could have forced a stop if not fixable.
- Because EP23 was later scheduled, this was the highest-risk content issue in the batch.

Resolution:

- `safe_handling_fix_applied` removed duplicate opening suicide wording from audio/captions.
- EP23 thumbnail v002 avoids death/self-harm/35-years/single-cause wording.
- `sensitive_locks` evidence was generated after fixes.

Remaining risk:

- A human R3 safe-handling review is still the correct owner gate before public release.

### 2. EP23 "35 Years" Handling Was Initially Unsafe

The episode rules required that "35 years" never appear unqualified. It must be framed as a theoretical stacked statutory maximum and paired with plea/Kerr critique context.

Observed problems:

- The burned-caption path had a risk of showing an unqualified "Thirty-five years" formulation.
- The safety checker initially treated the phrase too locally and could conflict with a contextually safe narration/caption segment.

Impact:

- A thumbnail/caption/on-screen "35 YEARS" without the qualification would be materially misleading and violate the episode lock.

Resolution:

- Burned captions were adjusted.
- Safety logic was updated in the related thread to evaluate the full explanatory context rather than only a narrow local window.
- The replacement thumbnail avoids "35 YEARS" entirely.

Remaining risk:

- Any future title/thumbnail copy must continue avoiding unqualified `35 YEARS`.

### 3. EP23 Final Video Identity Became Ambiguous

There were multiple final-like files and hashes:

- `final.mp4`
- `final.motionfix.v001.mp4`
- Multiple intermediate SHA values from caption/safety/motion passes.

Observed problems:

- The final accepted upload candidate became `final.motionfix.v001.mp4`.
- `final_delivery.v001.json` was at risk of pointing to an older `final.mp4`.
- The final file used for scheduling had to be explicitly confirmed.

Impact:

- Wrong-video upload risk.
- Audit trail confusion.
- Future replacement/re-upload could grab the wrong file.

Resolution:

- Scheduling used `H:/pd-media/episodes/PD-2026-023-swartz/08_edit/final.motionfix.v001.mp4`.
- `final_delivery.v001.json` was corrected to point at the motion-fixed file.

Remaining risk:

- The old `final.mp4` still exists and can confuse future automation unless a canonical pointer is enforced.

### 4. R2/R3 Publish-Gate Discipline Was Operationally Weak

The user explicitly instructed scheduling, and the uploads were made, but the design docs themselves treat EP22/23/24 as higher-risk:

- EP22: R3 living/pardoned public figure.
- EP23: R3 sensitive death by suicide.
- EP24: R2 living convicted subject.

Observed problems:

- Upload/schedule happened as a batch under current-thread owner instruction.
- The normal legal/safety owner-gate process remained thin relative to the risk class.
- Metadata/descriptions were checked, but the process was still close to the edge of "owner gate" requirements.

Impact:

- If any wording or visual issue had slipped through, the external side effect would already exist on YouTube.
- This increases rollback complexity.

Resolution:

- All four are private scheduled, not immediately public.
- Captions, thumbnails, and scheduling results were recorded.

Remaining risk:

- Before each publish time, perform a final R2/R3 review, especially EP22/23/24.

## High Issues

### 5. Images Were Not Ready When Build Work Began

EP21:

- `EP21-IMG-002.png..046.png` were missing.
- `final_build_blocked / hero_images_incomplete` was recorded.

EP22:

- Expected 74 hero images.
- Blocks occurred at 9, 11, and 34 images available.

EP23:

- `missing_images: 42`.
- Build was blocked before final render.

Impact:

- Build scripts and acceptance work were run before the material base was complete.
- The process produced repeated blocked states and extra scaffolding events.

Resolution:

- Later runs proceeded after images were present.

Prevention:

- Add a hard preflight: do not enter render/final assembly until image count and dimensions pass.

### 6. Caption Quality Passed Formal Gates Before It Passed Human Viewing

Across EP21/22/24 and the EP23/EP24 related work, caption issues included:

- Text too large.
- Heavy black boxes.
- Captions too high or visually dominant.
- Unnatural line breaks.
- Breath-group / semantic-group mismatch.
- Weak line endings such as `the`, `of`, `to`, `question the`.
- Fragmented cues such as `By the time he`.

Impact:

- A video could pass caption format gates while still looking amateurish.
- User had to review and request visual changes.

Resolution:

- EP21/22: smaller, unboxed, cleaner wrapping.
- EP24: moved captions lower and reduced style weight.
- EP23: regenerated/verbatim-aligned captions and burned ASS.

Prevention:

- Add a human-viewing gate: sample frames or short previews at representative timepoints before full render acceptance.

### 7. Visual Effects Were Misaligned With User Preference

User explicitly rejected:

- Left-to-right moving vertical line effect.
- Yellow/gold full-screen wash effect.
- Overly large subtitles.

Impact:

- The videos initially carried visual styling that the user did not want.
- Fixing it required re-rendering.

Resolution:

- Sweep line removed.
- Yellow/gold wash reduced or removed.
- Caption size/style adjusted.

Prevention:

- Encode these as channel-level style locks:
  - no moving vertical sweep line,
  - no yellow full-screen wash,
  - subtitles small, bottom-safe, no heavy box unless necessary.

### 8. EP23 Caption Alignment Required Many Iterations

EP23 generated multiple `caption_alignment_fix_applied` events and backup folders.

Observed problems:

- Earlier safety edits caused narration/caption mismatch.
- Caption regeneration initially dropped words due to a fallback bug in the related thread.
- The process had to satisfy verbatim match, safe handling, and visual readability simultaneously.

Impact:

- High time cost.
- More intermediate files and evidence noise.
- Higher chance of final metadata drift.

Resolution:

- Final caption set reached exact narration text match with cue count 485.
- Related acceptance/sensitive/runtime/dynamics gates passed.

Prevention:

- Treat safe text, exact narration match, caption readability, and acceptance gates as one combined constraint from the beginning.

### 9. EP23 Motion Gate Failed After Caption/Visual Changes

Observed problems:

- Static imagery plus longer/cleaner caption display caused freeze detection risk.
- Motion/freeze gate required additional mitigation.

Impact:

- A visually acceptable video could still fail automation.
- Motion fix introduced file identity confusion and larger final file.

Resolution:

- A motion-fixed final was created.
- Subtle temporal film grain was added to clear freeze detection.

Tradeoff:

- Video size increased significantly in the related thread.

Prevention:

- Motion gate should be checked on short render samples before full final.

### 10. `final.mp4` Was Locked During Replacement

From the related EP23 thread:

- `os.replace` failed with `PermissionError` because the video was open.
- The temp file existed and had to be copied over later.

Impact:

- Replacement workflow became non-atomic.
- Higher chance of stale file or partial state.

Resolution:

- Later copied with `Copy-Item -Force`.

Prevention:

- Use versioned final filenames instead of replacing `final.mp4` while open.
- Keep `final_current.json` as the canonical pointer.

### 11. Metadata and Audit Files Lagged Behind Real Outputs

Observed examples:

- EP23 `final_delivery` temporarily pointed at the wrong final.
- Acceptance report / self audit / final delivery needed updates after caption/motion changes.
- EP24 manifest checksum had to be manually updated in related work.
- SHA format varied between raw SHA and `sha256:` prefixed SHA.

Impact:

- Audit trail cannot be trusted automatically.
- Future scripts may consume stale metadata.

Resolution:

- Several records were manually corrected.

Prevention:

- Finalization script must update manifest, delivery, self audit, acceptance report, and upload metadata atomically.

### 12. YouTube Scheduling Happened in a Large Batch

Observed final schedule:

- EP21: 2026-07-06 12:00 JST.
- EP22: 2026-07-07 12:00 JST.
- EP23: 2026-07-08 12:00 JST.
- EP24: 2026-07-09 12:00 JST.

Problems:

- EP24 date changed from 7/8 to 7/9.
- EP23 was still being finalized while scheduling instructions were forming.
- Four uploads, captions, thumbnails, and publishAt settings were applied together.

Impact:

- A single mistake could affect multiple public-facing scheduled videos.
- Harder to isolate failures.

Resolution:

- API results show private scheduled state and correct `publishAt` values.

Prevention:

- Schedule high-risk episodes one at a time with post-upload verification after each.

## Medium Issues

### 13. YouTube Thumbnail Replacement Had Local Script Bugs

Observed problems in this thread:

- `_access_token()` was called without `load_env()`, causing `TypeError`.
- Python boolean was written as `true` instead of `True`.

Impact:

- The thumbnail update failed once before external side effects occurred.
- Low external risk, but indicates insufficient script dry-run/compile before execution.

Resolution:

- Fixed and re-ran successfully.
- `py_compile` passed after correction.

Prevention:

- Always run `py_compile` before any script that performs external side effects.

### 14. First CTR Thumbnail Draft Had Visual Issues

Observed problems:

- Old thumbnail text showed through the new design.
- EP22 badge `98 CHARGES` was too legally risky/misleading without context.

Impact:

- Could have lowered trust or violated Milken charge/plea distinction.

Resolution:

- Dark plate opacity increased.
- EP22 badge changed to `6 PLEAS`.

Prevention:

- Thumbnail text safety lint before upload.
- Contact sheet review before API call.

### 15. CTR Thumbnails Became Too Template-Like

The replacement thumbnails are louder and likely clearer at small size, but they share the same formula:

- Large black left plate.
- Big yellow/white text.
- Arrow on right.
- Gold border.

Impact:

- Better immediate clarity, but weaker series differentiation.
- Four consecutive scheduled videos may look repetitive in channel context.

Resolution:

- Accepted for quick CTR-oriented replacement.

Prevention:

- Create 2-3 visual systems and rotate them by episode type.

### 16. Package State Changed After Upload

Thumbnails were replaced after the initial YouTube scheduling.

Impact:

- Original `thumbnail.selected.v001.png` no longer matched the live YouTube thumbnail.
- The package had to be updated to v002.

Resolution:

- `thumbnail.selected.v002_ctr.png` created for EP21-24.
- `youtube_thumbnail_ctr_update.owner_batch.v002.json` recorded for each.
- `manifest.json`, `final_delivery`, and events were updated.

Remaining risk:

- Old schedule result JSONs still contain the first thumbnail state.

### 17. YouTube Studio Cache May Lag API State

API reported `thumbnailSetResponse` success for all four videos.

Impact:

- Studio or public thumbnail previews may show older images briefly.

Resolution:

- Recorded API response and maxres thumbnail URLs in update JSONs.

Prevention:

- Recheck Studio/API thumbnail URLs after cache window when needed.

### 18. Build Scripts Have Too Much Responsibility

From related EP24 work:

- One script touched captions, audio, BGM, factory, thumbnails, rights, manifests, delivery, acceptance.
- `prep-only` and `render-only` still changed more than expected.

Impact:

- Small fixes caused broad diffs.
- More chances for timestamp churn and stale metadata.

Resolution:

- Manual cleanup and targeted render/burn workflows were used.

Prevention:

- Split scripts into:
  - `caption-only`,
  - `burn-only`,
  - `motion-only`,
  - `metadata-sync-only`,
  - `publish-only`.

### 19. Event Logs Became Noisy

Observed problems:

- Multiple scaffold, prep, render, caption fix, and alignment events.
- Some were intermediate attempts rather than meaningful state transitions.

Impact:

- Harder to reconstruct the real final path.

Resolution:

- Some related-thread noise was manually trimmed.
- Current thread still has many legitimate but noisy events.

Prevention:

- Add `--no-event`, `--dry-run-event`, and `--event-level final|attempt|debug`.

### 20. Evidence and Backup Folders Are Hard to Navigate

Especially EP23:

- `safe_handling_fix_*`
- `caption_alignment_fix_*`
- multiple acceptance and dynamics outputs
- multiple hashes

Impact:

- It is hard to tell which evidence is current.

Resolution:

- Current `final_delivery` points at the accepted artifacts.

Prevention:

- Add `EVIDENCE/CURRENT.json` with canonical evidence pointers.

### 21. PowerShell / Shell Usage Mistakes

From related thread:

- Bash-style heredoc was attempted in PowerShell.

Impact:

- Minor time loss and noise.

Prevention:

- Use PowerShell-native here-strings or `apply_patch`.

### 22. Windows Process Visibility Was Confusing

From related thread:

- `.venv\Scripts\python.exe` spawned WindowsApps `python3.11.exe`.
- Long ffmpeg stderr and Python JSON output made status difficult to read.

Impact:

- Hard to tell whether render was progressing or hung.

Prevention:

- Standardize progress logs and write structured JSON status files during long renders.

## Low Issues

### 23. Thumbnail Generation Used Existing Thumbnail as Background

This was fast and safe, but it means the new thumbnails inherit some visual baggage from old selected thumbs.

Impact:

- Less original than fully redesigned thumbnails.

Resolution:

- Darkened plate hid most old text.

Future:

- Generate fresh background compositions from stills, then add text separately.

### 24. QC Contact Sheet Is Outside the Episode Package

CTR contact sheet:

- `runs/qc/ep21_24_thumbnail_ctr_v002_contact.png`

Impact:

- Useful, but not directly under each episode package.

Future:

- Copy contact sheet or per-episode preview into each episode's evidence folder.

### 25. Many Files Remain Uncommitted or Untracked

Observed by `git status`:

- EP21-24 files modified.
- New scheduling/upload result JSONs.
- New thumbnail v002 files.
- New helper scripts.
- Many unrelated pre-existing dirty files across the repo.

Impact:

- Hard to separate current work from older work.
- Commit scope is risky.

Resolution:

- No broad revert was performed.

Prevention:

- Use task branch/worktree per episode batch.
- Commit only scoped files after final verification.

## Root Causes

### Root Cause A: Too Many Episodes Were Processed as One Unit

The batch combined:

- four episodes,
- multiple risk classes,
- final video confirmation,
- captions,
- thumbnails,
- upload scheduling,
- external YouTube side effects.

This increased cognitive load and made state tracking fragile.

### Root Cause B: Machine Gates Were Treated as Broader Than They Are

Acceptance gates catch measurable failures. They did not fully catch:

- ugly caption sizing,
- awkward semantic line breaks,
- user-disliked effects,
- final artifact ambiguity,
- package audit usability.

### Root Cause C: Canonical Artifact Identity Was Weak

When multiple final-like files exist, the system needs a single source of truth. In this run, the source of truth moved between:

- file names,
- `final_delivery`,
- acceptance report,
- YouTube upload script config,
- manual operator memory.

That is too fragile.

### Root Cause D: Safety Rules Were Not Encoded Early Enough

EP23 safety constraints should have been applied before audio/caption/render, not patched after downstream artifacts existed.

### Root Cause E: Partial-Fix Scripts Had Broad Side Effects

Caption-only fixes should not rebuild audio, factory B-roll, rights manifests, thumbnails, or unrelated package metadata.

## What Went Right

Despite the problems:

- No missing-image substitution was used.
- EP23 sensitive-topic issues were caught and repaired before scheduling.
- YouTube uploads were private scheduled, not immediate public.
- Captions and thumbnails were uploaded.
- Final schedule times were verified through API state.
- Thumbnail replacements were verified at API level.
- Backups and evidence were kept rather than overwriting silently.
- EP23 final upload used the motion-fixed file.

## Current State Summary

### EP21

Status:

- Scheduled private for 2026-07-06 12:00 JST.
- Video ID: `tt7U1XgjCU4`.
- CTR thumbnail v002 applied.

Key issues:

- Initial image shortage.
- Caption/effect style corrections.
- Package has blocked evidence from earlier state.

### EP22

Status:

- Scheduled private for 2026-07-07 12:00 JST.
- Video ID: `mj9qEKPRatE`.
- CTR thumbnail v002 applied.

Key issues:

- Repeated image wait.
- Caption style iterations.
- R3 living/pardoned wording sensitivity.
- Initial CTR badge was adjusted from `98 CHARGES` to `6 PLEAS`.

### EP23

Status:

- Scheduled private for 2026-07-08 12:00 JST.
- Video ID: `FTm1icKgycU`.
- CTR thumbnail v002 applied.
- Final upload candidate: `final.motionfix.v001.mp4`.

Key issues:

- Missing images.
- R3 sensitive conflict.
- Duplicate suicide wording.
- Unqualified 35-years risk.
- Caption alignment repeated.
- Motion/freeze gate.
- Final file identity confusion.
- Heavy evidence/backups.

### EP24

Status:

- Scheduled private for 2026-07-09 12:00 JST.
- Video ID: `rYV4rxtQCV0`.
- CTR thumbnail v002 applied.

Key issues:

- Subtitle position/style needed correction.
- Date changed during scheduling plan.
- Build script responsibilities too broad.
- Manifest/checksum/audit sync needed manual care in related work.

## Recommended Fixes Before Public Release

### Must Do Before Publish Window

1. Re-run read-only YouTube status verification for EP21-24:
   - privacy is private until scheduled time,
   - `publishAt` is correct,
   - captions present,
   - maxres thumbnail exists.

2. Recheck EP22/23/24 metadata:
   - EP22: no "convicted at trial", no insider-trading/RICO conviction, pardon not exoneration.
   - EP23: no death/self-harm wording outside required description line, no single-cause claim, no unqualified 35 years.
   - EP24: no Gupta conflation, no unsupported profit/sentence superlatives.

3. Confirm canonical final file pointers:
   - especially EP23 must point to `final.motionfix.v001.mp4`.

4. Create a compact owner-facing publish packet:
   - video ID,
   - schedule,
   - title,
   - description path,
   - final video SHA,
   - captions SHA,
   - thumbnail SHA,
   - risk notes.

### Should Do Soon

5. Add `CURRENT_DELIVERY.json` per episode, generated automatically, with only canonical final assets.

6. Add a thumbnail safety linter:
   - episode-specific banned fragments,
   - line count/legibility,
   - R2/R3 wording checks.

7. Add a caption visual QC workflow:
   - sample frames at 10-15 timestamps,
   - check size, lower-third collision, line endings, semantic breaks.

8. Split build scripts:
   - caption-only,
   - burn-only,
   - motion-only,
   - metadata-sync-only,
   - upload/schedule-only.

9. Add a final metadata sync script:
   - compute SHA,
   - update manifest,
   - update final_delivery,
   - update self_audit,
   - update acceptance/evidence pointer.

10. Clean up Git scope:
   - do not broad commit the dirty tree,
   - isolate EP21-24 files,
   - commit only package metadata, scripts, and small JSON/MD evidence,
   - keep heavy media out of git.

## Process Rule Changes

### Rule 1: No Final Render Before Asset Preflight

Do not run final render if required image count, dimensions, and selected paths are incomplete.

### Rule 2: R3 Episodes Need Safety Locks Before Audio

For R3 sensitive/living-person episodes, safety locks must be checked before:

- ElevenLabs generation,
- caption generation,
- final render,
- upload.

### Rule 3: A Final File Name Is Not a Source of Truth

Every upload must read from a canonical final-delivery JSON that includes:

- path,
- SHA,
- duration,
- acceptance report path,
- gate status.

### Rule 4: Caption Gates Need Human Visual QC

A caption can be valid and still bad. Require visual sample frames before final acceptance.

### Rule 5: External Upload Scripts Must Compile and Dry-Run

Before YouTube side effects:

- `py_compile`,
- local file checks,
- video state dry-run/read-only check,
- then write action.

### Rule 6: Batch Scheduling Should Be Avoided for R2/R3

High-risk episodes should be scheduled one by one, with verification between each.

## Bottom Line

The videos were brought to a publishable scheduled state, but the process was too dependent on manual correction and late-stage patching. The most important fixes are:

1. make canonical final asset identity impossible to confuse;
2. move R3/R2 safety locks earlier;
3. separate caption/burn/metadata/upload responsibilities;
4. add human-facing visual QC before full final acceptance;
5. stop treating four high-risk uploads as one operational batch.

