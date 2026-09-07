# PD 014-015 After Owner Approval Runbook v001

This runbook is for after the owner explicitly approves exact hashes. It does not grant approval by itself.

## Current Gate State

- PD-2026-014-lange is at `edit_review`.
- PD-2026-015-theranos is at `edit_review`.
- Public upload, schedule, publish, and paid narration are still blocked until exact approvals are recorded.
- Theranos requires legal/rights approval before any upload or schedule.

## Review Entry Points

- Review dashboard: `episodes/_planning/pd_014_015_owner_review.html`
- Approval copy packet: `episodes/_planning/pd_014_015_owner_approval_packet.v001.md`
- Publish readiness preflight: `episodes/_planning/pd_014_015_publish_readiness_preflight.v001.json`
- Approval dry-run result: `episodes/_planning/pd_014_015_prepare_owner_approvals.dry_run.v001.json`

## Step 1: Capture Owner Approval Text

Create one or both input files only after the owner sends exact approval text from the approval copy packet.

```powershell
notepad episodes\PD-2026-014-lange\approvals\OWNER_APPROVAL_INPUT.v001.txt
notepad episodes\PD-2026-015-theranos\approvals\OWNER_APPROVAL_INPUT.v001.txt
```

Do not paraphrase the approval. Keep exact episode id, target path, and SHA-256 lines.

## Step 2: Dry-Run APR Creation

```powershell
python scripts\prepare_lange_theranos_approvals.py
```

Expected before real approval text exists:

```text
BLOCKED: missing owner approval input file
```

Expected after valid approval text exists:

```text
WOULD_CREATE: episodes/PD-2026-014-lange/approvals/APR-0002.json
```

or the matching APR files for the gates that were approved.

## Step 3: Apply APR Files

Only after dry-run shows the intended `WOULD_CREATE` lines:

```powershell
python scripts\prepare_lange_theranos_approvals.py --apply
```

This creates APR files and updates manifest approvals. It still does not upload, schedule, publish, or make paid API calls.

## Step 4: Re-run Publish Readiness Preflight

```powershell
python scripts\preflight_lange_theranos_publish_readiness.py
```

The preflight must stay `BLOCKED` until all required APRs exist:

- Lange: APR-0002 first cut, APR-0003 title/thumbnail, APR-0004 narration release, APR-0005 publish/schedule.
- Theranos: APR-0002 first cut, APR-0003 title/thumbnail, APR-0004 narration release, APR-0005 legal/rights, APR-0006 publish/schedule.

## Step 5: Standard Verification

```powershell
py -3.11 -m unittest tests.test_lange_theranos_safety_scripts -v
python scripts\validate_episode.py 14
python scripts\validate_episode.py 15
python scripts\verify_rights_hashes.py episodes\PD-2026-014-lange\09_package\rights_manifest.v001.json
python scripts\verify_rights_hashes.py episodes\PD-2026-015-theranos\09_package\rights_manifest.v001.json
```

Expected current rights summaries:

```text
Lange:    OK=173 MISMATCH=0 MISSING=0 NO-HASH=0
Theranos: OK=160 MISMATCH=0 MISSING=0 NO-HASH=0
```

## Hard Stops

- Do not run upload/schedule scripts until publish readiness preflight allows it and the owner has explicitly approved the exact final delivery hash.
- Do not make ElevenLabs or other paid narration calls without explicit cost approval.
- Do not publish Theranos without legal/rights approval for the exact package hash and publish/schedule approval for the exact final delivery hash.
- Do not infer approval from prior script approval or general encouragement.
