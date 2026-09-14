# SHORTS REFRESH — Execution Plan v001 (prep only; NO renders/reschedules run)

Authored 2026-07-24. Planning + local inspection only. GPU is busy on a film re-render; this
plan is staged so that when the GPU frees, execution is fast and unambiguous.
Spec governing every short: `episodes/_planning/SHORTS_METHOD.v001.md` (12 rules).
Reference implementation of the spec in code: composition `short40m` (data
`remotion/src/data/short40m.ts` + `short40m_timing.ts`; the `method:true` prop path in
`remotion/src/compositions/Short.tsx`).

Render config is global in `remotion/remotion.config.ts` (png frames, h264/libx264, CRF16,
x264 preset slow, yuv420p, bt709, aac 320k, concurrency = all cores, Chromium ANGLE). Do NOT
pass per-render codec flags; the config already sets quality. All `npx remotion` commands run
from `C:\Users\aab15\Documents\prime-documentary\remotion`. All `py`/`.sh` scripts run from the
repo root `C:\Users\aab15\Documents\prime-documentary`.

GPU vs CPU legend: **[GPU]** = Remotion render / Still (Chromium ANGLE; depth shorts also use
three.js WebGL) — must wait for the GPU. **[CPU]** = ffmpeg / TTS / forced-alignment / upload —
can run now while the GPU is busy. **[AE]** = After Effects (separate app).

---

## KEY CORRECTION TO PRIOR CONTEXT — the reference short WAS already rendered

Prior verification said `short40m` was "DESIGNED + REGISTERED but NEVER RENDERED (no mp4)".
That was a filename-only check for `short40m*.mp4`. In fact the reference short was rendered
2026-07-23 12:09–12:11 under an ad-hoc name. ffprobe confirms these ARE the `short40m`
composition (duration 42.233s = `SHORT40m_TOTAL_SEC` 42.239; 1080×1920):

- `remotion/out/kidsforcash_short_method_yt.mp4` (25.9 MB) — the YT master
- `remotion/out/kidsforcash_short_method_tt.mp4` (25.9 MB) — the TikTok master
- `remotion/out/kidsforcash_short_method_reels.mp4` (25.9 MB) — the Reels master (rule 11)
- `remotion/out/kidsforcash_short_method_yt_coverfirst.mp4` (21.3 MB) — coverfirst variant

So the reference short already exists in all four variants (yt / tt / reels / coverfirst) at
**42.23s**. It is (a) UNDER the 60s hard cap but OVER the 20–40s target (rule 4), (b) named
inconsistently (not `short40m_*`), and (c) never scheduled. Two paths below.

---

## DELIVERABLE 1 — Reference-short (`short40m`) execution card

### Path A (preferred per task): trim to ≤40s, then re-render
The 42.239s runtime is padded by four inter-line gaps of ~0.72s (L1→L2, L2→L3, L3→L4,
L4→L5) plus ~1.0s trailing tail. Tightening each gap to ~0.30s recovers ~1.68s and trimming
~0.6s of tail lands ≈39.9s. This is a **[CPU]** mix/timing regen done BEFORE the GPU render.

```bash
# 1. [CPU] Re-generate the -14 LUFS mix + captions/timing with tighter inter-line gaps so total <=40s.
#    build_short_mix.py rewrites remotion/src/data/short40m_timing.ts and the audio mix in
#    remotion/public/shorts/short40m/audio/. Confirm the exact flag name in the script header;
#    the gap/pad control is what shortens the runtime (target lead-gap ~0.30s, trim trailing tail).
py -3.11 scripts/build_short_mix.py --short 40m --max-sec 40 --lead-gap 0.30
#    -> verify: the new SHORT40m_TOTAL_SEC in short40m_timing.ts is <= 40.000
```

```bash
# 2. [GPU] Render the trimmed masters (from remotion/). depth:false + method:true are baked into
#    the composition defaultProps, so no --props needed.
npx remotion render Short-short40m-yt out/short40m_yt.mp4
npx remotion render Short-short40m-tt out/short40m_tt.mp4
```

```bash
# 3. [GPU-light] Render the cover Still used by coverfirst (writes the PNG the .sh expects).
npx remotion still ShortThumb-short40m out/short40m_thumb.png
```

```bash
# 4. [CPU] Bake the designed cover onto the first 1.5s (reads short40m_yt.mp4 + short40m_thumb.png).
bash scripts/coverfirst.sh 40m
#    -> remotion/out/short40m_yt_coverfirst.mp4
```

```bash
# 5. [CPU] Reels export (rule 11). The Short component has no 'reels' platform; the TikTok master
#    is platform-neutral (CTA "Full story on our profile"), so Reels reuses the tt master, re-muxed
#    faststart. (This mirrors how kidsforcash_short_method_reels.mp4 == the tt render.)
ffmpeg -y -i out/short40m_tt.mp4 -c copy -movflags +faststart out/short40m_reels.mp4
```

```bash
# 6. [AE, optional] Premium AE hero-beats (per premium-animation mandate). Produces *_ae variants.
py -3.11 scripts/ae/composite_shorts_hero.py --short short40m
#    -> remotion/out/short40m_yt_coverfirst_ae.mp4
```

### Path B (shortcut): accept 42.23s as-is (under the 60s cap)
If the owner accepts 42.23s, NO GPU work is needed — just rename the four existing renders and
schedule. Rule 4 allows >40s "if the payoff needs it"; 42s is marginal.

```bash
# [CPU] rename the existing 2026-07-23 renders to the canonical short40m_* names, then schedule.
cp out/kidsforcash_short_method_yt.mp4            out/short40m_yt.mp4
cp out/kidsforcash_short_method_tt.mp4            out/short40m_tt.mp4
cp out/kidsforcash_short_method_reels.mp4         out/short40m_reels.mp4
cp out/kidsforcash_short_method_yt_coverfirst.mp4 out/short40m_yt_coverfirst.mp4
```

### Post-render re-check list (run after Path A or before scheduling Path B)
```bash
# [CPU] runtime <=40 (Path A) and container/format sanity
ffprobe -v error -show_entries stream=width,height -show_entries format=duration \
  -of default=noprint_wrappers=1 out/short40m_yt.mp4          # expect 1080x1920, <=40.0 (Path A)
# [CPU] loudness back at -14 LUFS (spec: build_short_mix targets -14)
ffmpeg -i out/short40m_yt.mp4 -af loudnorm=print_format=json -f null -   # read input_i ~= -14
```
Manual eyeball checklist (watch the WHOLE runtime, per the repo's "watch end-to-end" lesson):
- Frame 0 vs last frame: loop-tail image+telop == hook (`$2.8 MILLION / TO JAIL KIDS`) — clean visual loop (rule 5).
- Persona mark ("▶ PRIME DOCUMENTARY", top-center) present every frame (rules 9b/10).
- Captions sit in the center-safe band (method mode, y1000–1320), clear of the YT/TT/Reels
  bottom title + right action rail (rule 11).
- Hook lands in the first 1s muted AND with sound (rule 1); no static hold >2s (rule 6).
- Non-real judge/child faces only; no real-person likeness (ad-safety).

---

## DELIVERABLE 2 — Scheduled-shorts inventory (all still PRIVATE; none public)

Authoritative source: `runs/new_shorts/schedule/short<NN>.result.json` (12 records) cross-checked
against the batch schedulers `scripts/schedule_new_shorts_v001..v004.py`. Channel
`UCuQPtAz1rca9eJ4xhvX0yKA`. Every record is `privacy: private`, `coverfirst: true`,
`thumbnail_set: true`, with a future `publishAt` — i.e. scheduled, not yet public. Uploaded render
= `short<NN>_yt_coverfirst.mp4` (v001/v002/v003) or `short<NN>_yt_coverfirst_ae.mp4` (v004).

| short | comp id (`Short-short<NN>-yt/-tt`) | video_id | publishAt (UTC) | runtime | render state | method? |
|---|---|---|---|---|---|---|
| 38 | Short-short38 | EP-iiuy6L-o | 2026-08-02T03:00Z | (n/a*) | yt+coverfirst rendered; **no tt/reels** | NO |
| 39 | Short-short39 | gZknzRSgRaw | 2026-08-03T03:00Z | (n/a*) | yt+coverfirst rendered; **no tt/reels** | NO |
| **40 (OLD)** | Short-short40 | **sP_lQebksIQ** | **2026-08-04T03:00Z** | 58.17s | yt+coverfirst rendered (non-method) | NO |
| 41 | Short-short41 | v6CrJ9HtFlg | 2026-08-05T03:00Z | 56.17s | yt+coverfirst rendered; **no tt/reels** | NO |
| 42 | Short-short42 | tFHwI4R4tJY | 2026-08-06T03:00Z | 57.70s | yt+coverfirst rendered; **no tt/reels** | NO |
| 43 | Short-short43 | g7q-9SOPDbE | 2026-08-07T03:00Z | 53.11s | yt+coverfirst rendered; **no tt/reels** | NO |
| 46 | Short-short46 | HBUYD8Uv4Ak | 2026-08-08T03:00Z | 54.50s | yt+tt+coverfirst rendered; no reels | NO |
| 47 | Short-short47 | TIWAscG6On8 | 2026-08-09T03:00Z | 56.13s | yt+tt+coverfirst rendered; no reels | NO |
| 48 | Short-short48 | nFEJBlEijdw | 2026-08-10T03:00Z | 55.85s | yt+tt+coverfirst rendered; no reels | NO |
| 49 | Short-short49 | wNqYS4j_VwM | 2026-08-11T03:00Z | 55.89s | yt+tt+coverfirst rendered; no reels | NO |
| 50 | Short-short50 | 1FHZ5qA6pgA | 2026-08-12T03:00Z | 55.52s | yt+tt+coverfirst+**AE** rendered | NO |
| 51 | Short-short51 | lDpfSAuFMS8 | 2026-08-13T03:00Z | 59.28s | yt+tt+coverfirst+**AE** rendered | NO |

\*short38/39 runtime not read this pass (data files not opened); they are the same v001 pre-method
batch as 40–43 and should be treated as ~55s until confirmed by their `short38/39_timing.ts`.

Reference `short40m` is NOT in the ledger — never uploaded/scheduled. It is the intended
method-spec replacement for the OLD short40 (sP_lQebksIQ, 08-04), which is a separate, non-method
58s short that must be superseded, not edited.

Gaps: short44 and short45 have data/timing files but are NOT registered compositions and have NO
schedule record — orphaned/superseded (EP44 tekoh shipped as short46, EP45 cleveland as short47).
Ignore them for this refresh.

---

## DELIVERABLE 3 — Per-short rebuild plan (score vs 12 rules)

All 9 registered batch shorts (41,42,43,46,47,48,49,50,51) share an IDENTICAL defect profile —
verified directly in code for short41 and short51, and confirmed for the rest by their identical
Root.tsx registration (all `depth:true`, none `method:true`, all end on a bare `cta` beat) and
their 53–59s runtimes. short38/39 are the same v001 pre-method batch. So one canonical rebuild
spec applies to all, with a per-short delta table.

### 12-rule scorecard (canonical, applies to every batch short)
| rule | state | fix |
|---|---|---|
| 1 · 1s hook | PARTIAL — opens on hook telop + lightrays | keep; verify first line teases payoff in 1s |
| 2 · packaging-first cover | PASS — coverfirst baked | none |
| 3 · open-loop → payoff | PASS — hook question, payoff at L4 | none |
| 4 · length 20–40s | **FAIL — 53–59s** | trim script → re-gen VO (TTS) → build_short_mix → new timing; target ~38–40s |
| 5 · loop design | **FAIL — ends on bare CTA, no loop-back** | add a `loop` beat mirroring the hook (image+telop), as in short40m |
| 6 · muted-first captions + interrupt ≤2s | PARTIAL — captions in LOW band; cadence OK | fix via method captions (rule 11) |
| 7 · faces + emotion + motion | PASS — depth stills move; face at hook | none |
| 8 · franchise format | PASS — fits "the law said ___" | none |
| 9 · sub-conversion (CTA+funnel+persona) | PARTIAL — spoken+on-screen CTA & funnel present; **no persona mark** | set `method:true` (adds PersonaMark) |
| 10 · anonymous persona | PARTIAL — Brian VO yes; **no fixed visual signature** | set `method:true` (persona mark + kinetic caption style) |
| 11 · cross-platform + UI-safe captions | **FAIL — captions collide w/ UI; 38–43 have no tt; nobody has reels** | `method:true` center-safe captions; render tt for 38–43; produce reels for all |
| 12 · retention iteration | N/A pre-publish | log per-short after publish |

### Canonical rebuild recipe (per short)
1. **[edit] Root.tsx** — add `method: true` to that short's `-yt` and `-tt` `defaultProps`
   (keep `depth: true`). This single change fixes rules 9b/10 and the caption half of rule 11
   (PersonaMark + center-safe captions), and matches short40m. Highest leverage, ~1 line each.
2. **[edit] data file** — append a `loop` cut to CUTS mirroring the `hook` (same image + hook
   telop, `motion:'pushin', fast:true`), exactly like `short40m.ts`'s L5 `loop` beat, so the last
   frame matches the first (rule 5).
3. **[CPU/TTS] length** — tighten the narration script to ~150–165 words (≈40s at ~178 wpm) and
   re-synthesize the Brian VO, then re-run `build_short_mix.py --short <NN>` to regenerate
   `short<NN>_timing.ts` + the -14 LUFS mix. This is the expensive step; do it in prep while the
   GPU is busy. (If a same-day script trim is too much, minimum viable rule-4 pass = tighten
   inter-line gaps only, like short40m Path A, buying ~2–4s without rewriting.)
4. **[GPU]** render `Short-short<NN>-yt` and `-tt` → `short<NN>_yt.mp4`, `short<NN>_tt.mp4`.
5. **[GPU-light]** `npx remotion still ShortThumb-short<NN> out/short<NN>_thumb.png`.
6. **[CPU]** `bash scripts/coverfirst.sh <NN>` → `short<NN>_yt_coverfirst.mp4`.
7. **[CPU]** reels: `ffmpeg -y -i out/short<NN>_tt.mp4 -c copy -movflags +faststart out/short<NN>_reels.mp4`.
8. **[AE, optional per premium mandate]** `py -3.11 scripts/ae/composite_shorts_hero.py --short short<NN>`.
9. **[CPU] re-schedule** — the video is already PRIVATE+scheduled, but the render changed, so
   supersede: delete the existing private `video_id` and re-upload the new coverfirst render with
   the same `publishAt` (the v004 scheduler already follows the delete-old-then-upload pattern;
   or `scripts/schedule_short_youtube.py --short <NN> --publish-at <UTC>`). Must complete BEFORE
   that short's publishAt.

### Per-short delta table (priority = earliest publishAt first)
| order | short | publishAt | special notes beyond canonical recipe |
|---|---|---|---|
| 1 | 38 | 08-02 | pre-method v001 batch; also render tt (missing). Confirm runtime from timing file. |
| 2 | 39 | 08-03 | same as 38. |
| 3 | 40 (OLD) | 08-04 | **REPLACE, don't rebuild.** Supersede sP_lQebksIQ with the `short40m` reference (Deliverable 1). Delete the old video, schedule short40m coverfirst to 08-04. |
| 4 | 41 | 08-05 | verified in code; add tt+reels. Hook "THE PRINTS DID NOT EXIST". |
| 5 | 42 | 08-06 | 57.7s (longest non-AE); needs the biggest script trim. add tt+reels. |
| 6 | 43 | 08-07 | add tt+reels. |
| 7 | 46 | 08-08 | tt already rendered; still needs method flag + loop + trim + reels. |
| 8 | 47 | 08-09 | same as 46. |
| 9 | 48 | 08-10 | same as 46. |
| 10 | 49 | 08-11 | same as 46. |
| 11 | 50 | 08-12 | already AE-enhanced; still needs method+loop+trim, then re-run AE. |
| 12 | 51 | 08-13 | verified in code; already AE-enhanced; 59.3s (longest) → biggest trim. |

Note: flipping `method:true` and adding a loop beat both REQUIRE a re-render (they change the
frames), so every scheduled short must be re-rendered and re-uploaded regardless — the current
private uploads are all non-method.

---

## DELIVERABLE 4 — Ordered execution queue (run when the GPU frees)

### PHASE 0 — prep now, GPU-free (do while the film re-render holds the GPU) — **[CPU/edit/TTS]**
0.1 Decide reference-short path: A (trim ≤40, re-render) or B (accept 42.23s, rename only).
0.2 If Path A: run `build_short_mix.py --short 40m` trim → confirm timing ≤40s. **[CPU]**
0.3 Root.tsx: add `method:true` to every batch `-yt`/`-tt` (41,42,43,46,47,48,49,50,51; add
    38/39 once confirmed). **[edit]**
0.4 Each batch data file: append the `loop` beat mirroring the hook. **[edit]**
0.5 Length trims: rewrite each script to ~40s, re-gen Brian VO, re-run `build_short_mix.py`
    per short → new timing + mix. **[CPU/TTS]** (start with the earliest/longest: 42, 51, then by date.)
0.6 `npm run typecheck` in remotion/ to confirm Root/data edits compile. **[CPU]**

### PHASE 1 — reference short first (proven template) — **[GPU then CPU]**
1.1 [GPU] render `Short-short40m-yt`, `Short-short40m-tt`.
1.2 [GPU] still `ShortThumb-short40m` → `short40m_thumb.png`.
1.3 [CPU] `coverfirst.sh 40m`; [CPU] reels remux from tt; [AE opt] composite_shorts_hero.
1.4 [CPU] post-render re-checks (ffprobe ≤40s, loudnorm −14, watch full, loop match).
1.5 [CPU] schedule: supersede OLD short40 (sP_lQebksIQ) — delete it, upload short40m coverfirst
    PRIVATE with publishAt 2026-08-04T03:00Z (its slot), set the cover as custom thumbnail.

### PHASE 2 — rebuilds by publish-date urgency — **[GPU then CPU], repeat per short**
Order strictly by publishAt: 38 (08-02) → 39 (08-03) → [40 done in Phase 1] → 41 (08-05) →
42 → 43 → 46 → 47 → 48 → 49 → 50 → 51 (08-13). For each short run canonical recipe steps 4–9:
- [GPU] render `-yt` + `-tt`; [GPU-light] still thumb.
- [CPU] coverfirst.sh; [CPU] reels remux; [AE opt] hero-beats (mandatory re-run for 50/51).
- [CPU] re-check (ffprobe ≤40, loudnorm −14, watch full, loop+persona+caption-safe).
- [CPU] supersede: delete old private video_id, re-upload new coverfirst, re-apply publishAt.

Timeline note: today is 2026-07-24; earliest publishAt is 08-02 (~9 days runway). Front-load
Phase 0 script trims for 38/39/41/42/43 (the 08-02→08-06 head of the queue) since VO re-gen is
the critical path and is GPU-free. 50/51 (08-12/13) have the most slack.

### Hard guardrails (from repo memory/gates)
- No real-person likeness anywhere (illustrative non-real faces only); AI-disclosure line stays.
- Watch each short END-TO-END before scheduling (don't sign off from one frame).
- Measure, don't estimate: ffprobe every runtime; loudnorm every mix.
- Verify the real artifact (the mp4), not an agent/script "done" message.
- Delete the old private upload before re-uploading (avoid the double-upload orphan pattern).
