# APR-0006 — Series playlists (4) creation/repair on the live channel

- **Approved by:** owner, 2026-07-28, verbatim: 「①→実行して」 (in reply to a three-option summary in which ① was "再生リスト4本の作成").
- **Scope approved:** run `scripts/plan_series_playlists.py --execute` for the plan recorded in
  `episodes/_planning/measurements/PLAYLIST_PLAN.v001.json` — 46 API calls / 2,300 quota units:
  create 2 new playlists, update+reorder 2 existing ones, insert 42 playlist items, and delete
  ONE playlist item (a "Deleted video" placeholder sitting at position 0 of "Landmark Rights Cases",
  the slot every playlist link lands on).
- **NOT approved by this record:** any change to video titles, descriptions, thumbnails, visibility,
  schedules, chapters, comments, or end screens. Those remain owner-gated separately.
- **Evidence base:** playlist traffic measures 19.6 min/view against a 3.91 min channel average
  (DEEP_RESEARCH_FINDINGS.v001 §5 / memory `pd-distribution-actions`), and only 6 of 42 long-forms
  are currently in any playlist. Both existing playlists are damaged (deleted video at position 0;
  worst-retention video as an entry point).
- **Reversibility:** playlists can be deleted and items removed at any time. The single DELETE is
  irreversible in form only — it points at a video that no longer exists, so there is nothing to
  restore.
- **Executed by:** Claude (parent session), immediately after this record was written.
