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

## Post-Publish Standard Operations (EP10+, mandatory)

EP10以降は公開/予約の直後に必ず実行（詳細・根拠は docs/09 §17）：

1. Read-only audit: `uploadStatus=processed`, privacy正, no rejection/failure, `madeForKids=False`, `defaultAudioLanguage=en`。
2. Upload final caption sidecar (`captions.final.vNNN.srt`, `en/standard`). **proxy SRT 禁止**。最終SRTが無ければ公開前に生成。
3. Assign to the correct playlist per docs/31 taxonomy（未登録ゼロ）。
4. Post the pinned engagement comment (`pinned_comment.md`) as `@PrimeDocumentaryStudio`。pin自体はAPI不可＝手動。
5. Verify caption track + playlist membership by re-read; record in manifest/events.

Gate add-on: `captions_sidecar_final_uploaded`, `playlist_assigned`, `pinned_comment_posted` がすべて true。
Tooling: `scripts/yt_apply_playlist_captions.py`（冪等）, `scripts/yt_full_audit.py`（確認）。
API不可（Studio/手動）: サムネA/Bテスト, CTR/impressions, コメントpin。

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
