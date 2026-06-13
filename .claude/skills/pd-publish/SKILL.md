---
name: pd-publish
description: Uploads or schedules a PD video only after validating current approvals, channel allowlist, rights, hashes, metadata and privacy safeguards.
---

# PD Publish Workflow

## Preconditions

- package_ready
- current publish approval
- render checksum valid
- rights clear
- critical claims supported
- expected channel allowlisted
- budget within limit

## Procedure

1. Revalidate all preconditions immediately before side effects.
2. Check for duplicate video hash or existing upload.
3. Upload with private visibility by default.
4. Apply metadata, thumbnail, subtitles, chapters and playlist.
5. Confirm platform processing and resulting video ID.
6. Re-read platform state.
7. If approved for scheduling, set explicit timezone and time.
8. Confirm scheduled/public state.
9. Save URL, IDs, timestamps and settings.
10. Register analytics monitoring windows.

## Never

- Public publish with stale or missing approval.
- Upload to an unknown channel.
- Retry a timed-out upload without checking whether it completed.
- Delete or replace a public video without a separate approval.

## Output

- platform result
- final state
- URL
- scheduled time
- manifest/event updates
- monitoring jobs
