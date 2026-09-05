# 2026-09-05 — build/publish lane narrative

One seat drove the whole day; the standing mandate was "限界マックス・複数エージェント並行・止めない".
Everything below is verified, not recalled.

## Shipped / booked today

- **EP81 station published** 12:00 JST (KDNJwRywx2M) on schedule.
- **Shorts**: 09-05 gap filled in the morning (short200/201/202 after 16 funnel records were
  authored); the 16:05 timer pushed 09-07's four (short203/204/205/250). 09-06 was already full.
  Calendar is solid through 09-07; backlog 68 after today's pushes.
- **EP79 alaska261** stays booked for 09-08 12:00 (0a_MnQuJF3s).

## The colgan (EP78) story — the day's spine

1. Blocked all month on 4 missing people plates (Codex down). Unblocked with the owner's
   emergency-addition exception: local SD3.5 generated C092/C123/C161/C165.
   Two were bounced on my independent zoom QC for **resolving pseudo-glyphs** (ceiling sign,
   wall plaque) and regenerated with signage engineered out of frame. Verdicts written, bound.
2. First render v001 completed 14:13 (1595.4s). Full 49-sheet read by two agents found exactly
   ONE blocking defect: **cut-0020 (2:13–2:20), generated plate C014 reproduced Delta Air Lines'
   tail livery on three background aircraft** — rights_and_licence. Everything else clean,
   including all four fresh plates in context.
3. C014 blocklisted (colgan-scoped; C-ids are per-episode, unlike shelf ids), every copy
   quarantined (img/rejected, img_unused, E:/pd-media 05_visuals and ai_video archives).
4. **Trap hit and solved**: `_finish_episode.sh` step [0/7] restores img_unused, which resurrected
   125 plates AFTER the verdict file had been re-scaffolded without them — inputs went red with
   125 unjudged plates. The 2026-08-27 review survives in `runs/qc/colgan_plate_decision.v001.json`
   (content) + `runs/qc/colgan_plate_hashes.v001.json` (sha256 binding), so verdicts were restored
   **sha-verified, zero mismatches** (scratchpad restore_colgan_verdicts.py). Lesson: scaffold
   AFTER the restore step, or the binding sees a different set than the build will.
5. Re-render v002 launched 16:34, expected ~19:45. Then: sheets → verify the 2:13–2:20 region +
   spot re-read → review json → ship → **book 09-07 12:00** (quota: 3,400 held, booking 1,650).

## EP83–85 progress (all three now close)

- **max737**: footage 47→74 (agent also caught 3 forbidden-subject clips accepted on 09-04 —
  scales-of-justice/`THE LAW` book); people plates **19/20 shipped** (P019 unsatisfiable in 4
  attempts — panel glyph storms; its design row was rewritten v2: pure macro hands-on-wheel
  against blackness, nothing to write on). Independent 19-plate review running. Thumbnails: 7
  candidates + 320px sheet.
- **threemile**: footage 76 (yesterday); 20/20 plates generated at base res, **4K upscale + depth
  pending GPU**; thumbnails: 8 candidates, all pass calibration.
- **katrina**: footage 63→81 (dup vs threemile resolved — threemile dropped its copy, katrina
  keeps); plates not started; thumbnails: 7 candidates (one dark one kept but not recommended).
- GPU order after colgan's render: threemile 4K+depth → katrina 20 → max737 P019-v2 → reviews.

## Also today

- **Shorts stock unlocked 12→72**: 60 rendered-but-unregistered shorts (EP62–82, 3/episode) had no
  CONFIG entries because their designs lacked destination video_ids. Backfilled 20 design files
  from the channel audit, generated 60 CONFIG rows (`gen_short_publish_config.py`), authored 60
  funnel records via 20 parallel agents, `check_short_funnel.py --all` = 91/91 green.
- **CTA-card QC**: the 9 shorts whose ctathumb.jpg died with the SSD have the card baked intact in
  their rendered mp4s (frame-extracted and eyeballed vs a healthy baseline) — no re-renders needed.
- **register_face_stills.py is a liar**: 7/7 "faces" it found in colgan were false positives
  (a depth map, a suitcase, cockpit gauges…). All fake P copies deleted; memory written.
- **check_script_length.py bug fixed**: its `_episode_band()` never read episode_spec (the
  2026-08-21 fix to check_final_acceptance's twin function never propagated) — alaska261 got a
  false "LONG by 2,433 words" against a band it never declared. Fixed with episode_spec first.
- **EP86–88 slate drafted** (owner decision pending): recommended Columbia / El Faro / Purdue,
  demand-probed; justice lane measured dead (fresh exoneration names median <5k views).
  `episodes/_planning/EP86_88_TOPIC_SLATE_DRAFT.v001.md`.

## Open

- colgan v002: read the changed region, ship, book 09-07 (tonight).
- threemile/katrina plates + reviews; max737 P019-v2; then the three builds.
- Captions (whisper) still needed for max737/threemile/katrina before their builds' polish step.
- Owner decisions parked: readable brands in two published episodes; 20 lost kinetic cards in 15
  published episodes; EP86–88 slate approval.

## Brush-up proposals (owner asked these be kept; implement in coming sessions)

1. **Pre-render livery sweep as a standing preflight step** — proven same-day: the sweep of
   max737's legacy (pre-zoom-standard) plates caught 3 real-carrier liveries (Air France
   tricolor, a DL monogram, carrier-red nacelles) BEFORE the render; colgan's identical defect
   was only caught AFTER a full render. Scope: plates whose design rows mention aircraft/
   vehicles/ships/signage, zoomed 5-8x. Candidate home: a --livery-sweep mode on
   check_plate_verdicts or a small standalone checker wired into ship_episode.sh preflight.
2. **Durable daily shorts push** — replace session-bound sleep timers with a Windows scheduled
   task (schtasks) running yt refresh + fill_short_schedule --apply --reserve <day's need>.
   No PD-ShortsPush task exists today; a thread switch kills the timer.
3. **Scaffold ordering guard** — check_plate_verdicts --scaffold should WARN (or refuse without
   --force) when remotion/public/<slug>/img_unused|motion_unused are non-empty: scaffolding
   then destroys verdicts the next [0/7] restore will need (cost today: 125 rows, recovered
   sha-verified from plate_decision + plate_hashes).
4. **Caption canonical naming** — gen_captions_forced writes captions.vNNN.srt but every
   filmconfig reads captions.final.v001.srt; add a --promote flag or teach the finisher to
   accept the newest vNNN. Manual copy step today for 3 episodes.
5. **Generation agent sizing** — one episode per generation agent, max ~20 plates; the single
   60-plate agent died to a session cap mid-batch and its successor had to reconstruct state
   from disk.
