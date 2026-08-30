# Handover — 2026-08-30 17:10 JST, the build/publish + design lane

This session held both lanes: assembling and booking, and EP77–85 design. Whoever picks this up
holds both. **Exactly one session schedules.** Every number below was measured at the timestamp
above, not remembered. Where a thing is unverified, it says so.

---

## 1. The calendar, and the two days that were lost

```
8/26 12:00  EP74 itaewon      RFDPSfllbk0   PUBLIC
8/27 12:00  EP75 lahaina      3AgCeXG3qGI   PUBLIC
8/28 12:00  EP76 morandi      ippMyC49OyI   PUBLIC
8/29 12:00  EP72 lacmegantic  MISSED -- master exists, never uploaded
8/30 12:00  EP73 uri          MISSED -- master exists, never uploaded
8/31 +      empty
```

**Two slots went empty with finished masters sitting on disk.** Not a render failure and not a
gate: the renders finished at 02:43 and 04:17 on 8/28, and the session ran out before the
shipped-frames read that has to happen before booking. That is the single most important fact
in this document. `docs/PD_CANON` / ship_policy already says it — *a day not shipped is gone*.

**The first job is to book what is already built.** Three masters are ready and none is booked:

| slug | master | size | runtime | black | review |
|---|---|---|---|---|---|
| lacmegantic | `episodes/PD-2026-072-lacmegantic/08_edit/lacmegantic_final_bgm.v001.mp4` | 2,567 MB | 29:44 | 0 | none written |
| uri | `episodes/PD-2026-073-uri/08_edit/uri_final_bgm.v001.mp4` | 2,509 MB | 30:02 | 0 | **stale, see below** |
| concordia | `episodes/PD-2026-080-concordia/08_edit/concordia_final_bgm.v001.mp4` | 1,965 MB | 27:56 | 0 | none written |

Black-stretch count measured on the bytes just now, not taken from a gate.

**`runs/qc/uri_shipped_frames_review.v001.json` is bound to the WRONG BYTES.** It reads
`verdict: REJECT` against sha `2e383500…`, which was the *first* uri render of 21:50 on 8/27.
That reject was for one defect — a bar chart captioned `FORFEITURE CASES / YEAR` — and the
component was fixed and uri re-rendered at 04:17. I extracted 14:34 from the new master an hour
ago: the heading is gone, the bars and their own labels ("263 / Held below 59.4 Hz", "540 / The
nine-minute threshold") are correct. **Do not ship on that stale review, and do not delete it —
re-read the new sheets and write a review bound to the new sha.** `ship_episode.sh` will refuse
the mismatch on its own, which is the guard working.

Re-dating: the CONFIG entries still say 08-29 and 08-30, which are now in the past, and a past
`publishAt` **publishes immediately**. Move them before booking. Everything from 8/31 is
untouched and still correct.

---

## 2. Where every episode stands

```
                film   plates  i2v    stock   design   render   booked
EP72 lacmegantic  ✅    n/a     n/a    109     ✅       ✅       -- QC + book
EP73 uri          ✅    n/a     n/a    98      ✅       ✅       -- QC + book
EP77 keybridge    ✅    128     128    42      ✅       started 05:47, NO MASTER
EP80 concordia    ✅    185     181    53      ✅       ✅       -- QC + book
EP81 station      ✅    184     183    0 ←     ✅       FAILED on 0 stock clips
EP82 valdez       --    179     4      --      ✅       --
EP78 colgan       --    156     0      30      ✅       --
EP79 alaska261    --    190     0      51      ✅       --
EP84 threemile    --    181     0      0       ✅       --
EP83 max737       --    184     0      0       ✅       --
EP85 katrina      --    173     0      0       ✅       --
```

"design ✅" means filmconfig + youtube_meta exist and pass `figure_spec`, `check_packaging_claims`
and `check_packaging_qc`. All eleven do. All eleven are in `upload_schedule_case_v001.CONFIG`.

**i2v is the long pole and it is not running.** 1,059 clips remain at 3.08 min each ≈ **54 hours
of GPU**. I stopped the chain on 8/27 to get renders through and never restarted it. Restart it
before anything else that is not a booking:

```
bash scripts/_chain_i2v_ep78_82.sh          # read its header first; it resumes from delivered counts
```

Two episodes cannot render until their own blocker clears:
- **EP81 station: zero stock clips, floor is 40.** A staging agent got as far as reading 12 of
  135 strips and died on the account's weekly limit. Its queries and candidate list are on disk.
- **EP77 keybridge: FIXED, needs a re-render.** Its 05:47 render stopped at `[4b] polish
  captions` saying *"only 1 of 358 narration chunks line up with a cue start -- this srt does
  not belong to this narration index"*. That was false and the falsity was mine: I stripped
  `<!-- KB-113 -->` markers out of the captions on 8/27 so they could not be burned into the
  picture, and the narration index still carries them, so the comparison measured 5,030
  narration words against 4,768 cue words. `_lead_words` in `polish_captions_srt.py` now
  strips markers from both sides. Re-run: lead measured over 275 of 358 chunks, cues 504 →
  445, orphans 36 → 0, dangling ends 74 → 0. **Just render it.**

---

## 3. What must not be undone

**EP77's 17 regenerated clips.** keybridge invents people: a full comparison of all 128 clips
against their plates found 17 still carrying an invented person, five of them resolving a face
into recognisable features, in an episode that names people charged with crimes. They were
regenerated and verified clip by clip (`runs/qc/keybridge_i2v_vs_plate.v002.json`: 0 of 17
invent a person, 0 of 17 resolve a face, transient bumps H017 6.74→0.00, H066 5.71→0.00,
H083 4.69→0.00). I re-checked H123 and H052 by hand at the exact frames the faces used to be.
The originals are archived in `runs/qc/keybridge_person_v2/` — **do not restore them.**

That regeneration took four attempts and **three of them reported success while changing
nothing**, all caught by sha256 and by nothing else:
1. the GPU lock said `keybridge-regen` while the chain calls itself `keybridge`, so it read its
   own claim as another chain's and refused;
2. the chain FILLS GAPS rather than replacing — with the mp4s present it said "17 already done,
   0 to do" and ran 27 minutes;
3. `E:/pd-media/assets/ai_video/keybridge/motion/` restored the old mp4s, so the assembler saw
   "128 already render-visible" and skipped. **Remove from the pool AND the E: archive, then
   run `assemble_episode_i2v.py`.**

**Two selected thumbnails were replaced and must stay replaced** (both as `v002`, because the
uploader takes the highest `thumbnail.selected.v*.png`):
- concordia v001 showed the wreck heeled over with a yellow funnel — the real operator's livery
  — and was a visible collage. Its own spec forbids capsized/listing/heeled ship by name.
- uri v001 burned `$9,000` over a domestic electricity meter. `$9,000` is the wholesale cap per
  MWh (script :396); the household figure is `$17,000` (:402). Rebuilt from the same plate.

---

## 4. Gaps that are real and still open

- **Nothing reads `forbidden_subjects` against a PICTURE.** All 33 thumbnail candidates were
  opened this session and **10 must not ship, two of them the selected one**. Eight were
  invisible to `check_packaging_claims` by construction, because it reads the wording of the
  selected thumbnail only. Do-not-ship list with reasons:
  `runs/qc/thumbnail_candidate_audit.v001.json` and `runs/qc/thumbnail_rejected_candidates.v001.json`.
- **Provenance does not bind a number to a picture.** `config/thumbnails/uri.json` carried a
  correctly-filled provenance reading "nine thousand dollars per megawatt-hour" — and that
  per-MWh figure still sat on a domestic meter.
- **The Studio cookie is 11 days old and returns 401.** No CTR reading is possible until it is
  re-captured, which needs the owner. Also found while trying: the "EP35 baseline 1.00% /
  7,436imp" handed over by the packaging lane is **not a baseline** — that video is a treated
  unit in the live `title-band-2026-08-10` experiment and the figure is 9 days post-treatment.
  And the 9/7 read date may rest on a false premise: the tool labels its output `28d` but 55 of
  61 videos grew monotonically, which is since-publish cumulative behaviour. Settle with one
  live response body before 9/7. Full analysis: `runs/qc/ctr_reading_2026-08-28.v001.json`.
- **Only 3 of 11 episodes satisfy the declared runtime band.** Owner set a floor on 8/28:
  *20分を超えてればOK*. All eleven clear it (25:36 to 29:52). EP84 and EP85 carry
  `approvals/APR-0001.json` for the shortfall; no declared value was lowered anywhere.
- **EP84 T138's defect is in the ORDER SHEET**, not the generator: the prompt asks for "a modern
  domestic fuse board" in a 1979 film. Regenerating will reproduce it.
- **EP78 colgan is at 18 people-plates against a declared floor of 20.**

---

## 5. Fixed this session, with the measurement

| what | evidence |
|---|---|
| `build_render_public_dir` kept STALE staged assets | `if dst.exists(): return "kept"`. All 17 fixed keybridge clips were still the old bytes in `public_ep77/`, sha-identical to the archived rejects, three hours from render. Now compares size+mtime and replaces. Proved three ways. |
| 9 of 11 episodes had NO scheduler CONFIG entry | `--ep keybridge` was an invalid argument: every gate green, booking dies at the last command. All nine added, 08-31→09-08, no collisions, no past dates. |
| `Figures.tsx` captioned every bar chart `FORFEITURE CASES / YEAR` | Hardcoded string; 13 episodes, 21 charts, most already public. Now an optional `title`, drawing nothing when absent. |
| captions burned `<!-- KB-113 -->` into the picture | 103 of 525 cues on keybridge, 0 on morandi and lahaina. Stripped where cue text is made. |
| descriptions over YouTube's 5,000 cap | colgan 6,279, valdez 5,591 — both would have been rejected at the upload call. Now a hard problem in `check_packaging_qc`. |
| `check_packaging_claims` never read 11 episodes' thumbnail wording | keyed on `thumbnail_headline` vs `thumbnail_text`. Fixed; it immediately caught morandi. |
| `apply_plate_decision` erased the reviewer | colgan's 166 plates said "unknown". Fixed and repaired. |
| `polish_captions_srt` compared a cleaned srt against an uncleaned index | keybridge's render died on it. Both sides now normalised. |
| `check_still_luma.py` is new | a backdrop cut in as a picture is a 4-second hole. Found 3 in lacmegantic before its render. Dark-SHARE rule added after a human beat the check on EP81 S080. |

---

## 6. QC done this session — do not repeat it

Plates read tile by tile: **1,110** across EP78/79/81/82/83/84/85. 49 rejected, including the
Twin Towers skyline in katrina, Chernobyl's sarcophagus in threemile, the Alaska Airlines Eskimo
emblem on two alaska261 plates, and a two-photograph collage that every machine check passed.

Stock clips read at full frame: **317**. 56 rejected — legible US tail registrations N100CW and
N6424J, a Cyrillic watch dial, IndiGo livery, Holland America Line and SILJA and VIKING on
hulls.

i2v compared against plates: **497 clips**. keybridge 17 of 128 bad (regenerated), station 1 of
188, concordia 0 of 181. The explicit prompt holds at ~0.5%; the default was 27–42%.

Shipped frames read: **296** across lahaina, morandi, lacmegantic (74, unrecorded — redo) and
uri (74, bound to superseded bytes — redo).

---

## 7. Next actions, in order

1. **Book lacmegantic and uri and concordia.** Re-date their CONFIG entries first — 08-29 and
   08-30 are in the past. For each: `prepare` → read every sheet → write the review bound to
   THAT sha → `ship <slug> <NN>` → hand-read the title against the script → `--book`.
2. **Restart the i2v chain.** 54 hours of GPU stand between now and EP82/78/79/83/84/85.
3. **EP81 station stock footage** — 0 of 40. Resume the staging agent; its candidate list and
   135 strips are on disk.
4. **EP77 keybridge** — the caption blocker is fixed; render it.
   `bash scripts/_render_keybridge_after.sh` runs it alone with the pre-render checks.
5. Ask the owner to re-capture `secrets/studio_cookies.txt`.

## 8. Two mistakes of mine, so they are not repeated

**I ran a writing tool at a published episode believing it had `--dry-run`.**
`polish_captions_srt.py` has no such flag; it writes. lahaina's srt was restored from git;
morandi's `08_edit/` is untracked so git could not, but the damage is nil and measured rather
than assumed — its `morandi_film.rendered.json` snapshot and the live film json both hold 510
cues, and the shipped master has its captions burned in. **Check a tool's flags before pointing
it at anything already public.**

**I let the calendar slip while fixing quality.** Every defect caught this session was worth
catching, and two dated slots still went empty with finished masters on disk. The order that
works is: book what is already built, then fix. Not the reverse.

Commits this session: `6eea8489` `24c5a531` `e37c4f30` `caf31d61` `e0a931f9` `a2680365`
`057aaf86` `e31d2ca5` `de7c8312` `bc169f8d` `b38d5126` `d0a64e37` `0634df1c` `bc9672e1` `98e40ab0` — all pushed.
