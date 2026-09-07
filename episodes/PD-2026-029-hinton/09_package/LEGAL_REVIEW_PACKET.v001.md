# EP29 hinton — R2 PRE-PUBLISH LEGAL / RIGHTS REVIEW PACKET

**Binding gate.** EP29 is **R2** (real, living person + death penalty + race). Per the design
(`EP29_hinton_DESIGN.v001.md`) and CLAUDE invariants 2/3/11, this human review MUST be signed
off **before** any public scheduling. Claude has prepared everything up to this gate but will
**not** upload or schedule until a human signs below and sets `publish_approved=true`.

- Video: `remotion/out/hinton_final.v001.bgm.mp4` (acceptance STATUS PASS, sha `69dc3efd…`)
- Facts source of truth: `episodes/.../03_script/script.annotated.v001.json` + `EP29_hinton_fact_recheck.v001.md`

## Review checklist (tick each)

1. **No fabricated facts.** Every ★ claim in the script traces verbatim to a public source
   (Hinton v. Alabama 2014 opinion, EJI, court records, national reporting). Confirm the
   ballistics/one-eyed-expert/$1,000-misunderstanding, "nearly 30 years", 9–0 reversal, and
   2015 release are all sourced — no invented dialogue, dates, or causation. [ ]
2. **Defamation — living/named parties.** Statements about **Anthony Ray Hinton** are true and
   favorable (legally exonerated). Statements about the State of Alabama, prosecution, original
   defense counsel, and the state's expert describe **official conduct / matters of public
   record** — verify each is accurate and attributed, and that no living, *named* individual is
   asserted to have committed a crime beyond the established record. [ ]
3. **No real-person likeness (invariant 11).** Confirm no AI image depicts Hinton or any real,
   identifiable person; only anonymous/representative figures. [ ]
4. **Rights.** All b-roll from the rights-cleared factory shelf; music from the rights-tracked
   library (Suno-origin, ingested as assets); no third-party archival of the real people. [ ]
5. **Synthetic-media disclosure.** Description states AI imagery is illustration only; upload
   sets `containsSyntheticMedia=true`, `madeForKids=false`. [ ]
6. **Dignity.** Race and capital punishment handled soberly, not sensationalized. [ ]
7. **Title / thumbnail honest.** "Alabama Tried to Execute an Innocent Man for 30 Years" and the
   selected thumbnail match what the body delivers (no clickbait the film does not pay off). [ ]

## ⚠️ Known open item (carry into review)
Per `[[pd-factory-shelf-mislabeled]]`, the factory shelf labels are unreliable. Claude removed 12
off-theme/mislabeled clips after a contact-sheet QC, but a reviewer should spot-check the final
render for any remaining off-tone footage before public release.

## Sign-off
- Reviewer: ____________________  Date: __________
- Decision: [ ] Approve for 2026-07-14 publish   [ ] Changes required: ____________________
- On approval: set `youtube_meta.v001.json` `publish_approved: true` (+ approval id), then run the
  private-upload-and-schedule step in `PUBLISH_READINESS.v001.md`.
