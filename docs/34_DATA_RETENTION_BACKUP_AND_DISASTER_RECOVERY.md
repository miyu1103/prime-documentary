# 34 — Data Retention, Backup and Disaster Recovery

## 1. Data classes

### Tier 0 — Irreplaceable
- metadata DB
- event log
- approvals
- source/claim ledger
- final script
- project files
- final masters
- rights evidence
- credentials backup metadata, not raw credentials

### Tier 1 — Expensive to recreate
- approved image masters
- master narration
- selected music
- final thumbnails
- edit timeline revisions

### Tier 2 — Reproducible but useful
- rejected candidates
- draft voices
- proxies
- intermediate renders

### Tier 3 — Ephemeral
- temp files
- caches
- partial downloads
- debug render

## 2. Retention policy

- Tier 0: long-term, multiple backups
- Tier 1: long-term while channel active
- Tier 2: configurable 30–180 days after publish
- Tier 3: automatic cleanup after validation

Never delete based only on file age. Check artifact references and approval state.

## 3. Backup strategy

Use a 3-2-1 style principle where practical:
- primary working copy
- local independent backup
- off-device/offsite backup

## 4. Backup content

- database dump
- event log
- configs without secrets
- schema versions
- manifests
- approved artifacts
- DaVinci project exports/backups
- source registry metadata
- rights evidence
- package files

## 5. Verification

A backup that has not been restored is not proven.

Monthly restore drill:
- restore isolated DB
- validate schema
- reconcile artifact hashes
- open representative project
- regenerate status report
- confirm approval history

## 6. RPO/RTO targets

Initial suggested targets:
- metadata RPO: 24 hours or better
- active project files RPO: 24 hours or better
- recovery target: within one working day

Adjust after production value increases.

## 7. Disaster cases

- Windows disk failure
- Mac disk failure
- NAS failure
- accidental deletion
- ransomware
- project DB corruption
- credential loss
- provider account suspension

Each case has a runbook and ownership.

## 8. Reconciliation

After restore:
- scan manifests
- verify hashes
- detect missing artifacts
- detect unregistered files
- rebuild derived indexes
- mark downstream stale if required
- do not assume filesystem state equals DB state

## 9. Archiving

Published episode archive includes:
- final video
- final audio
- selected assets
- final script
- claim/source registry
- rights manifest
- title/thumbnail history
- analytics snapshots
- retrospective
- reproducibility metadata
