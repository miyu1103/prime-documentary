# EP29 hinton — production retrospective (detailed)

Scope: taking EP29 from "images ready" to a GREEN acceptance receipt + a private, scheduled
(2026-07-14) YouTube upload, with the new depth-parallax motion tier. Written to be applied to
EP30/EP31 and forward.

---

## ✅ What went WELL

1. **Root-caused the recurring `animation_density` (紙芝居) fail.** The real bug: every still
   treatment AND footage computed motion progress as `interpolate(f, [0, useVideoConfig()
   .durationInFrames])`, but inside a Sequence that returns the FULL ~20k-frame film → `p≈0` →
   the parallax/Ken-Burns barely moved after the entrance. Threading each cut's own duration
   fixed it (12.5% → 8.9% near-still, longest 7.4s → 1.8s). **This helps EP28 and every future
   data-driven episode**, not just EP29.
2. **Shipped a genuinely new capability into production** (not a prototype): the `depth`
   treatment (real DPT depth-map displacement in `@remotion/three`) now lives in `CaseFilm.tsx`
   as a rotation option, plus a batch `gen_depth.py`.
3. **Verification discipline caught a false "green."** I reported green once on a *stale* v003
   mix (v004 had crashed at 10% and the mixer silently reused the old final). A sha check
   (receipt sha == file sha, and ≠ old sha) caught it → re-rendered → real green. Never declared
   done on self-report; only on the independent gate + sha match.
4. **Visual footage QC (contact sheet) caught mislabeled clips** the machine gates cannot see
   (cartoon cauldron on greenscreen, starfield labeled "prison_corridor", a bright family dinner
   in a death-row film). Culled 12, tone unified.
5. **Held the R2 publish gate.** Did not blindly publish a living-person death-penalty film;
   ran legal diligence (no fabrication, no defamatory named-party claims, accurate reporting of
   public court record, no real-person likeness, AI disclosure) and required explicit owner
   sign-off before scheduling.
6. **Audio note actioned fast** (VO buried) — mux-only fix (VO +5 dB, deeper sidechain duck),
   no re-render.

## ❌ What FAILED / was painful

1. **Animation still felt too little — even after the polish.** This is the biggest miss.
   `animation_density` PASSED (a machine floor: "not frozen"), but the **subjective/owner feel**
   did not. Gate ≠ perceived dynamism. Bumping parallax amplitude is not the same as *engaging*
   motion. **The real levers I under-used:** more `depth` cuts (only ~1/4), no animated
   `FigureBeats` (data shown as flat typography, not moving figures), few hero/marquee motion
   moments, no Blender hero plate. I optimized to the gate, not to the eye.
2. **Reported a false green** (see Well #3). Root cause: I trusted "acceptance PASS" without
   first confirming the re-render actually produced a NEW output file. Cost a full re-render +
   the owner's trust for a beat.
3. **Long WebGL renders crashed transiently.** v004 died at frame ~1992/20906 at `concurrency=6`
   (memory pressure with per-cut ThreeCanvas). Re-ran at `concurrency=4` and it completed.
4. **Slow feedback loop.** Every motion/footage tweak = a full ~40-min, 20,906-frame render.
   Several were burned before landing.
5. **Factory label breakage bit us again** (known issue `[[pd-factory-shelf-mislabeled]]`), and
   I only caught it *after* the owner said "animation felt off," not before the first render.
6. **Trivial self-inflicted cycles:** `gen_depth.py` crashed on a `\Users` path (unicode escape
   in a non-raw docstring); Blender 5.1 renamed half its Python API (EEVEE id, compositor node
   group, Glare sockets, slotted Actions) costing iterations.

## 🔧 ROOT PATTERNS → concrete next-time actions

- **A machine gate is necessary but NOT sufficient for "見ごたえ."** Add a *perceptual* motion
  budget the builder enforces, e.g. per 12-min episode: **≥ 40% of image cuts on `depth`**, **≥ 6
  animated `FigureBeats`** for every data/number/timeline moment, **≥ 2 hero motion plates**
  (Blender or big 3D move). Don't ship until those counts are met — then check the gate.
- **Verify the artifact chain by CONTENT, not by exit code.** After any re-render: assert the
  output file exists AND its sha ≠ the previous render's sha BEFORE mixing/acceptance. Bake this
  into the mix/acceptance wrapper.
- **Visual QC before the first render, every episode.** Auto-build the footage contact sheet in
  the builder and require a human glance (the labels are unreliable; gates can't catch tone).
- **Probe before the 40-min render.** Render a representative 60–90 s slice, measure
  `animation_density` + eyeball motion, iterate there; only then commit the full render.
- **Long depth/WebGL renders: `concurrency=4` (or segment-render).** Don't run 20k WebGL frames
  at max concurrency.
- **Python: raw-string any docstring/const with Windows paths.** Pin Blender API quirks in
  `[[pd-motion-toolkit]]` (already done) so they're not re-discovered.

## Ship facts (for the record)
- Final: `remotion/out/hinton_final.v001.bgm.mp4` — acceptance STATUS PASS, sha `69dc3efd…`.
- Thumbnail: A "30 YEARS. INNOCENT." (派手 grade). Title: "Alabama Tried to Execute an Innocent
  Man for 30 Years". Schedule: private, public **2026-07-14 12:00 JST**, containsSyntheticMedia=true.
- Owner shipped this cut knowing animation is on the light side — the fix is scoped above for EP30/31.
