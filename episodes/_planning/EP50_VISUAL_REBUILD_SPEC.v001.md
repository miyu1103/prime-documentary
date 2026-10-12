# EP50 VISUAL REBUILD SPEC (v001, 2026-07-25) — owner watch-through feedback

The "finished" EP50 (`centralpark_final.v003_coldopen.mp4`) FAILED the owner's watch-through. I had only checked technical defects (haze/warp/scanline via frame scan) + AE alignment + audio — NOT the actual watching experience. Repeat of [[feedback-ep3941-eyeball-final-render]]. This is the fix list; **re-render then WATCH THE WHOLE RUNTIME before showing again.**

## Owner complaints (verbatim, 2026-07-25) → root cause (measured)
1. **紙芝居 / no free stock / sparse AE** → film.json is **41% static stills by time**, `stock` references = **0** (none of the downloaded free stock is used), factory clips are mostly static Ken-Burns (motion-diff YAVG ~1.1) not real footage, AE = 36 cards / 61 min (~1 per 1.7 min).
2. **"似た画像が多すぎる・楽しくない・飽きる・視聴維持率が落ちる"** → source imagery is repetitive (dark cold-blue institutional/interrogation rooms over and over); low variety.
3. **人間の顔が全く出てこない** → no SDXL faces inserted (humans were silhouettes/from-behind). Owner: "SDXLでいいから造って差し込もう."
4. **所々画像がゆがんでる** → warping still present in places (depth/i2v/extreme-zoom). Must locate + kill.
5. **字幕4行が醜い** → captions wrap to 4 lines; owner wants **~2 lines max**.
6. **いつものオープニング無し** → my cold-open trim removed the gold BrandOpening. Restore it.
7. **フックの画像連射がチカチカ不快** → hook cuts are 0.17–0.48 s (5–6 cuts/sec bursts). Slow to calm holds.

## Fix plan (rebuild film.json → re-render → full watch)
- **A. VARIETY + MOTION (biggest):** generate a LARGE DIVERSE new image set with SDXL — varied locations (NYC 1989 streets/park/subway/precinct/courtroom/press/prison/homes/press-scrum/protests), varied shots (wide/med/close/detail/overhead), documentary/archival textures — NOT more dark rooms. Integrate REAL free stock video (H:/pd-media/downloads/video, assets/stock) in meaningful places for real motion. Lower still-share from 41% → ≤~20%; prefer real motion + i2v.
- **B. FACES / HUMANS:** SDXL generic PEOPLE with visible faces — detectives, prosecutors, defense lawyers, family, reporters, courtroom crowd, guards, era New Yorkers, protesters. ALL generic/anonymized, NOT resembling the real Five (Black/Latino youth) — use the 2-stage illustrative firewall; the Five themselves stay silhouette/non-identifying per guardrail, but the WORLD around them gets human faces.
- **C. AE DENSITY:** more AE moments (target ~1 per 45–60 s), spread across all acts.
- **D. CAPTIONS → 2 lines:** cap caption wrap at 2 lines (shorter caption segments and/or wider wrap); build_centralpark_film.py caption path.
- **E. HOOK CUTS:** slow hook to ~0.8–1.5 s holds, remove the 0.17 s bursts (SECTION HOOK tuple in build_centralpark_film.py).
- **F. OPENING:** keep the gold BrandOpening card (do NOT trim it away). Cold-open audio-from-0:00 is DE-PRIORITIZED vs keeping the usual opening.
- **G. WARP:** find warped shots (i2v/depth/extreme Ken-Burns zoom) and replace/retreat.

## Applies to EP51/52 too
Same pipeline → same risks. Fix the pipeline (variety, stock, faces, AE density, 2-line captions, calm hook) once and reuse for EP51/52. Do NOT ship EP51/52 with these defects.

## Status
Rebuild STARTED 2026-07-25: diverse SDXL people/face generation first (GPU free; other session is on GPU-free CTR research — coordinate so only one session hits the GPU). Then stock integration → film.json rebuild → re-render → FULL watch-through QC.
