# EP52 Morton — distinct video asset revision

Measured on 2026-08-07 against `remotion/src/data/morton_film.json`:

- Video cuts: 264
- Distinct video basenames: 221
- Maximum reuse: 2
- Rejected Baku government-house source: absent
- Rejected Kashmir newspaper source: absent
- Rebel / Rebel News / y2mate / 2mate sources: absent

`episode_spec.v001.json` previously declared 223 distinct video assets. That was the
correct count before the shipped-frame safety remediation removed the Baku and Kashmir
sources. The current declaration is 221 because the current film is exactly two sources
lower. This records a measured safety removal; it is not a declaration lowered merely to
pass a gate.
