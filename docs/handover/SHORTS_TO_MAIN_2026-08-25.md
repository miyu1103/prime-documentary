# Shorts lane → Main thread, 2026-08-25

**All 21 Shorts for EP70-76 are designed.** short289-294 were already delivered; short295-309
(EP74, EP75, EP76, EP72, EP73 — your booking order) were authored today. Five design files in
`episodes/_planning/short_designs/`, `check_short_design.py` and `check_short_constraints.py`
both 0 problems on all five, word counts 161-178 against the 159-180 band, specs read at their
highest revision (lahaina v003), prose forbidden_claims read by hand against every Short.
Lines files for the narration generator are emitted for all fifteen.

**The lane is not building them yet.** Owner's direction today: this thread does footage DL and
Shorts creation, and Shorts are stopped for a while. So the designs are frozen, deliberately
complete: when Shorts un-stop, the next command is `build_all_short_audio.py --only 295-309`
(resumable), then the usual assemble/mix/verify, then the 16:20 push from 8/29 as your pause
note planned.

Two things you may care about before then:

1. **Plate attrition.** The constraint gate checks a plate exists on disk; on lahaina 14 reviewed
   plates no longer exist as PNGs (consumed by i2v), morandi has only 60 of ~120. The designs
   name only plates verified present today. If a re-render regenerates or removes plates,
   re-run `check_short_constraints.py` on the five files — it will name any missing plate.
2. **Your six traps from the 8/24 brief were all honoured** — highest spec revision via
   `check_episode_spec.spec_path`, no v001 hard-coding, and no Short states a claim its episode's
   spec forbids. The one trap that bit anyway was new: `--cap-gb` on the ingest is cumulative
   against the whole archive, not per-run.

Quota-wise nothing changes: this lane uploads nothing until 8/29, and PD-LongformPush at 16:05
remains the only spender during the pause.
