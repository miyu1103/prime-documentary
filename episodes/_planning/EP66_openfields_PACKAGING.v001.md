# EP66 — PACKAGING PACKAGE (v001)

**Episode:** `PD-2026-066-rainwaters` (proposed slot; `episodes/PD-2026-06*` currently stops at 065)
**Subject:** government officers entering private land beyond the curtilage without a warrant.
Two cases: *Punxsutawney Hunting Club v. Pennsylvania Game Commission* (Pa. S.Ct., 21 July 2026,
overruling its own precedent) and *Rainwaters v. Tennessee Wildlife Resources Agency*
(Tenn. Ct. App., 9 May 2024).
**Written:** 2026-08-10. **Status:** DRAFT — owner approval required before the script is written.

> **Order of work for this episode (owner rule):** title, thumbnail and the first 20 seconds are
> designed and approved FIRST. The body is written to serve them. This document is that first
> deliverable. Nothing below may be changed by the script writer without a new revision.

---

## 0. What this is built on, and one thing I measured while building it

Binding inputs read in full: `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` (row 13 as rewritten
2026-08-10), `docs/PD_WINNING_PATTERN.md` (the ⚠ 2026-08-10 override block, which voids the
second-person / question-form / 11–12-minute conclusions below it), `docs/PD_CANON.md`.

The measurements that bind this package (all 2026-08-10, restated so this file is self-contained):

| Measured | Value |
|---|---|
| Channel CTR | **1.38%** against a 4–6% floor |
| Unseen's 25 recent titles | **59–100 chars, median ~82**; shortest (29) is its worst |
| PD question-form titles | its three worst videos |
| PD second-person vs third-person titles | median **4** views vs **17** |
| Retention at 10s / 15s / 20s / 30s | 87.6% / **76.9%** / 71.4% / 60.4% |
| Steepest loss in the whole film | **10→15s, 2.13 points per second** (6× the post-60s rate) |
| Top six openings | 91.4% @10s → 91.1% @20s. Bottom six: 84.2% → 56.3% |
| Best-retained opening (katz, 0.818) | time + place + one action, ending on what the subject does not know |
| Worst (tyler, 0.447) | summarises the outcome in the first ten seconds |
| Audience | 92% male, 76% aged 55+; emotional commands measure badly |

### The finding: the first 11.5 seconds of every PD long-form contain no voice

Not opinion — read out of the code while writing this:

- `remotion/src/compositions/CaseFilm.tsx` has exactly **one** `<Audio>` (line 771) and it sits
  **inside the Body `<Sequence>`**, which starts at `hook + OPENING_SEC` frames.
- `remotion/src/data/greene_film.json`: `hookSeconds: 8.0`, so Body starts at **11.5s**.
- `scripts/build_case_film_audio.py` lines 103–120 state it explicitly:
  `lead = hookSeconds + OPENING_SEC`, and *"hook/opening intro … **no VO in these regions**"*.

So on every shipped episode: 0.0–8.0s is a silent visual montage, 8.0–11.5s is a silent
full-screen gold title card, and the narrator's first word lands at **11.5s** — the exact
midpoint of the 10→15s window where the film loses 2.13 points per second. The spoken hook line
is then delivered at 11.5s, three and a half seconds after the picture has already moved on.

This package is designed to close that hole. It is the reason deliverable 3 is 20 seconds of
**narration** and not a montage.

---

## 1. Title candidates

Pattern (row 13): `[dramatic present-tense clause] — [what the powerful party does NOT know] | The Case of [Name]`.
All four are third person, 59–100 chars, no question form, no case citation, no doctrine word
("open fields", "curtilage", "Fourth Amendment" appear in none of them), real name as suffix.
Character counts are `len()` of the exact string including the em dash and pipe.

| # | Title | Chars |
|---|---|---|
| **T1 ★** | An Officer Cuts a Branch to Hide a Camera — The Farmer Never Knew \| The Case of Terry Rainwaters | **96** |
| T2 | A Warden Crosses the Gate 22 Times — The Club Is Never Told \| The Case of Punxsutawney | 86 |
| T3 | A Camera Watches the Woods for 78 Days — The Owners Are Never Told \| The Case of Punxsutawney | 93 |
| T4 | The State Walks Onto 136 Gated Acres — Nobody Has to Tell Him \| The Case of Terry Rainwaters | 92 |

One sentence each:

- **T1 — RECOMMENDED.** It is the only candidate whose first clause is a physical act a 55-year-old
  man can picture in one beat (a man with a blade, in trees), and "cuts a branch" is a retrieved
  verbatim fact rather than a characterisation, so the promise it makes is one the body can pay off
  exactly.
- **T2.** The strongest number (22 entries) attached to the newest ruling, but "warden" and "the
  club" are both abstractions, and Punxsutawney reads as a Groundhog Day joke before it reads as a
  hunting club — curiosity, but the wrong kind.
- **T3.** 78 days is the single most quotable figure in the research and the clause is concrete, but
  it duplicates T1's camera image without T1's human actor, so it is the natural A/B partner rather
  than the lead.
- **T4.** Closest to the literal Unseen grammar ("Nobody Has to Tell Him" is the withheld thing
  stated as a rule) and the 136-acre number is specific, but "The State Walks Onto" is a
  construction rather than an event and reads as commentary.

**Ship T1 as A and T3 as B** (row 13 requires ≥2 A/B variants). They test the same case from the
human side and the number side; the difference between them is attributable.

Accuracy note for whoever writes the metadata: **22 entries and the 78-day camera are Punxsutawney
(Pennsylvania). "Exposed" and the **136** gated acres are **Rainwaters**; the **cut branch**, **Henry County** and the **93** acres are **Hollingsworth** — this note previously assigned the cut branch to Rainwaters and was itself the source of the hook's error (TN-09 vs TN-13).**
Do not cross them.

---

## 2. Thumbnail specification

Buildable by `scripts/build_ep62_65_thumbnails.py` with an EP66 entry added to `SPEC` — no new
builder. What that builder actually does, read from the source before writing this:

- Cover-crops the plate to 16:9 → 1280×720, then lays a **black scrim at alpha 120 over the top 66%**
  (y 0–475) so the picture keeps its own light below that.
- Searches every contiguous 1–3 line break of the headline × sizes 248→100 step −4, keeps the split
  whose **tallest glyph ink** is greatest while every line fits 1200px wide. Warns below 150px.
- Kicker: fixed 46px, drawn as a filled accent tag under the headline.
- **The font it resolves to is `C:/Windows/Fonts/arialbd.ttf`.** It looks for `Anton-Regular.ttf`
  and `Oswald-Bold.ttf`; the repo has `Anton.ttf` and `Oswald.ttf`, so neither matches and it falls
  through to Arial Bold. Every ink figure below was measured with that same resolution path, so they
  are what the builder will produce today. If anyone renames the font files, re-measure.

Gate targets: `thumb_subject_luma` wants subject-box (x 0.20–0.80, y 0.12–0.88) mean luma ≥ 60,
tallest bright connected component ≥ **150px**, dark outline ring ≥ 12px.
`thumbnail_visibility` wants selected-thumb mean luma ≥ 33.

**Plate rules for all three:** no real-person likeness (hands, boots, backs and silhouettes only —
no face, no identifiable body); **no readable text anywhere in the plate** (posted signs must be
blank, weathered or shot at an angle that destroys the lettering; no lens badges, no printed
labels); generated plates commissioned at long edge ≥ 3840 (row 5). **The lower third must be the
brightest part of the frame** — the scrim eats the top 66%, so the unscrimmed band at y 475–634 is
what carries `subject_luma`. Daylight or low sun; no night plates.

### Variant 1 — recommended, pairs with T1/T3

- **Image:** a weatherproof camera housing strapped to a rough tree trunk at chest height, lens
  turned out toward a sunlit open field, pale cut wood showing where a branch was removed just
  below it; no people, no text on the housing.
- **Headline:** `78 DAYS` — measured **ink 184px @ size 248, one line**.
- **Kicker:** `NOBODY WAS TOLD` — accent GOLD `#E5B53A`.

### Variant 2

- **Image:** a padlocked metal farm gate across a dirt track into woodland, chain in the
  foreground, a blank weathered sign wired to the top bar, fresh boot prints in the mud on the far
  side of the gate; sunlit field visible through the gap.
- **Headline:** `ENTERED ANYWAY` — measured **ink 178px @ size 248**, breaking `ENTERED / ANYWAY`.
- **Kicker:** `GATED. POSTED.` — accent RED `#D22628`.

### Variant 3

- **Image:** close on a freshly cut branch stump on a trunk, pale exposed wood filling the lower
  frame, a black mounting strap running past the edge, blurred woodland behind.
- **Headline:** `CUT THE BRANCH` — measured **ink 184px @ size 248**, breaking `CUT THE / BRANCH`.
- **Kicker:** `FOR THE CAMERA` — accent GOLD `#E5B53A` (three words; the builder's kicker is fixed
  at 46px with no fitter, so keep it at or under three short words).

Archive backing (queried 2026-08-10 via `scripts/search_archive.py`, so the compositor knows what
already exists and what must be generated): woodland/forest **8 hits** incl. 3840×2160 drone
plates; misty forest at sunrise **6**; barbed/wire fence and padlock-in-fence **8+**; farmland
aerial **5** at up to 3840×2160; `no trespassing sign` **1**; deer in forest **5+**.
`farm gate metal`, `trail camera tree` and `wooden gate path` return **0 hits** — the gate, the
housing and the cut stump must be **generated plates**. Archive supplies the establishing woodland,
the fence/padlock texture and the aerial land; generated plates supply everything with a camera in it.

---

## 3. The first 20 seconds, as narration

Written to the katz shape (a time, a place, a person doing one thing, ending on something not
known) and against the tyler failure (no outcome in the first ten seconds). No "this is a true
story". No emotional command. **The strongest beat — the branch and the camera — occupies
0:09.9–0:15.0, straddling the 10→15s window where the film currently loses 2.13 points per second.**

Pace basis: `PD_CANON.md` §7 item 25 — measured 159.5–169.7 wpm, **not** 173. Timings below are
computed at **165 wpm = 2.75 words/sec** plus the stated holds. 48 words, 17.5s of speech, 2.8s of
designed silence. **Re-time against the actual ElevenLabs render before locking captions** — these
are the design targets, not measurements of an audio file that does not exist yet.

| Time | Words spoken | On screen |
|---|---|---|
| **0:00.0–0:01.5** | "Henry County, Tennessee. `[YEAR]`." | Archive drone plate, farmland at low sun, slow 6% push-in. The land, before anyone is in it. |
| 0:01.5–0:02.1 | *(hold, 0.6s)* | Same shot continues; the push-in does not stop. |
| **0:02.1–0:06.5** | "A state wildlife officer steps past a locked gate and a posted sign." | Two cuts, ~2.2s each, motion carried left-to-right through both: (a) archive — padlock in a wire fence, rack focus; (b) generated plate — a blank posted sign wired to a gate bar, boots passing behind it, no face. |
| 0:06.5–0:07.2 | *(hold, 0.7s)* | Boots in leaf litter, low angle, moving away. |
| **0:07.2–0:09.4** | "He walks out to a tree." | Generated plate — a single trunk in mid-ground woodland, the figure reduced to a dark shape at frame edge. Camera drifts in. |
| 0:09.4–0:09.9 | *(hold, 0.5s)* | The trunk, alone. This half-second is the set-up for the beat. |
| **0:09.9–0:15.0** *(THE BEAT)* | "He cuts a branch off it, — and bolts a camera where the branch was." **"camera" lands at ≈0:13.2.** | Three generated plates, ~1.7s each, hard-cut with 0.35s motion-blurred pushes: (1) gloved hands at a branch, no face; (2) the branch coming away, pale wood exposed; (3) the housing tight against bark, lens turning toward the open field. Cut 3 holds longest and ends on the lens. |
| 0:15.0–0:15.7 | *(hold, 0.7s)* | Cut 3 continues; the lens fills more of the frame. |
| **0:15.7–0:17.5** | "Ninety-three acres."  <!-- CORRECTED 2026-08-10: was "a hundred and thirty-six", which is RAINWATERS' land (TN-09). This hook is in Henry County and shows the cut branch, both HOLLINGSWORTH (TN-13, TN-16), whose parcel is "approximately 93 acres crossing Benton and Henry Counties". Found by the film bible; one number, no timing change. --> | Archive aerial of the farmland, wide. A MOTIONKIT kinetic figure counts to **93** over the plate — a number on the picture, not a fake map or a fake document (invariant 11). |
| 0:17.5–0:17.8 | *(hold, 0.3s)* | Aerial continues drifting. |
| **0:17.8–0:20.3** | "Nobody tells the man who farms them." | Generated plate — the field as the lens would see it: slightly vignetted, flatter contrast, empty. Nobody in the frame. |
| **0:20.3** | *(window ends — the question is standing, unasked)* | Holds on the empty field. |
| 0:20.7–0:21.8 | "Nobody has to." *(first line after the window — the reversal seed)* | Same empty field. The brand overlay rises here (§4). |

Exact words at exact seconds, as asked: *"Henry"* at 0:00.0; *"officer"* at ≈0:03.0; *"gate"* at
≈0:05.4; *"tree"* at ≈0:09.0; *"cuts"* at ≈0:10.3; *"branch"* at ≈0:10.9; **"camera" at ≈0:13.2**;
*"hundred"* at ≈0:16.1; *"Nobody"* at 0:17.8; *"farms"* at ≈0:19.5.

**What is deliberately absent:** the ruling, the word "legal", the word "court", the doctrine, both
case names, any statement of who won. A viewer at 0:20 knows a camera went up on a farm and the
farmer was not told, and does not know whether that was allowed. That is the standing question.

### FACT-LOCK before this is recorded (R2/R3)

Every clause must be traced to the ledger. Three items are not yet supported by the retrieved facts
and must be confirmed or cut — **not guessed**:

1. **`[YEAR]`** — the katz exemplar opens on a year and this line has a slot for one. The retrieved
   facts do not give the install year. **If R2 cannot source it, delete the year and ship
   "Henry County, Tennessee."** alone. Do not approximate.
2. **"steps past a locked gate and a posted sign"** — supported for Rainwaters at the level of
   "136 gated, posted acres". Confirm the officer's route crossed a gate; if the record only
   supports posted boundaries, change to "steps past a posted sign onto a farm that is not his."
3. **"Nobody tells the man who farms them"** — the retrieved Punxsutawney language is "without
   consent, a warrant, or probable cause". Confirm the equivalent for Rainwaters. If the record
   only supports the absence of a warrant, change to "He is not carrying a warrant. He does not
   need one." (which also lands the reversal earlier, and is a legitimate alternate ending to the
   window).

---

## 4. Where the brand opening goes

**Today:** `CaseFilm.tsx` line 766 renders `<BrandOpening>` as a full-screen `<Sequence>` from
`hook` to `hook + OPENING_SEC` — 8.0s to 11.5s — an opaque `INK` frame with a sunrise plate over it,
**with no narration under it**, in the single worst window the retention data contains.

**For EP66:** it becomes a **3.5-second lower-band overlay at 0:20.5–0:24.0**, over footage and
narration that never stop.

Why 20.5 and not earlier: the 10→15s stretch loses 2.13 pts/s and 15→20 loses 1.1 pts/s; 20→30
loses 1.1 pts/s and, unlike the earlier windows, the cold-open loop is already open by then, so the
brand mark arrives on top of a question instead of in place of one. It is the least-bad remaining
slot. Deleting it is not available: `op_ed_bookends` is a **hard** gate and `OPENING_SEC = 3.5` is
fixed by invariant 14.

**Exact build (no fork of `Bookends.tsx` — invariant 14; `op_ed_bookends` only checks that the
composition imports `components/Bookends` and names `BrandOpening`/`BrandEndcard`, verified in
`check_final_acceptance.py` lines 553–563):**

```
<Sequence from={Math.round(20.5*fps)} durationInFrames={Math.round(OPENING_SEC*fps)} name="Opening">
  <AbsoluteFill style={{justifyContent:'flex-end', pointerEvents:'none'}}>
    <div style={{position:'absolute', left:0, right:0, top:660, height:360,
                 overflow:'hidden', opacity:bandFade}}>
      <div style={{position:'absolute', left:'-50%', top:'-100%', width:'200%', height:'300%',
                   transform:'scale(0.36)', transformOrigin:'50% 50%'}}>
        <BrandOpening seriesLabel={seriesLabel} title={title} subtitle={subtitle} />
      </div>
    </div>
  </AbsoluteFill>
</Sequence>
```

- `bandFade`: `interpolate(f, [0, 0.25*fps, 3.25*fps, 3.5*fps], [0,1,1,0], {extrapolate:'clamp'})`.
- Do **not** use `mixBlendMode:'screen'` to knock out the `INK` backdrop — it also screens
  `banner_sunrise.png` over the picture, which is the banned full-frame gold wash (v2 §C2).
  Clipping to a band is what keeps the sunrise plate inside the brand furniture.
- **Verification before the full render:** render a `<Still>` at 0:21.5s, downscale to 320px wide,
  and confirm the title is legible. I could not render-test this (a long-form render is running);
  it is specified, not measured. If it is not legible at 320px, raise `scale` to 0.44 and `height`
  to 440 and re-check — do not shrink the band and ship it anyway.

**Engine changes this requires** (all of them, so they land in one batch — `PD_CANON.md` §8.2):

1. `CaseFilm.tsx` — move `<Audio src={staticFile(data.narration)}/>` out of the Body `<Sequence>`
   to the composition root at frame 0. The narration now starts with the film.
2. `CaseFilm.tsx` — Body `<Sequence>` starts at frame 0. Cut starts in `<slug>_film.json` are
   already Body-relative, so with a zero lead they become absolute and the cold open is simply the
   first cuts.
3. `<slug>_film.json` — add `leadSeconds: 0`. `build_case_film_audio.py` currently computes
   `lead = hookSeconds + OPENING_SEC` (lines 114, 1117); it must read `leadSeconds` when present and
   fall back to the old formula when absent, so EP62–65 are bit-identical.
4. `hookSeconds: 20.3` and `hookLine` = the cold open's closing line. `structure_4part` requires
   `hookSeconds >= HOOK_MIN_SEC (5.0)` and a non-empty `hookLine`, and requires narration section
   order HOOK → OPENING/OP → body → ENDING. Sections for EP66: **HOOK 0:00.0–0:20.3**,
   **OP 0:20.7–≈0:32** (spoken under and after the overlay), then ACT_1…, then ENDING.
5. `episode_spec.v001.json` must declare `section_vocabulary` including `OP` (the gate reads the
   opening label from the contract, lines 470–480) — an undeclared value is an error, never a
   default (CLAUDE §4.6).

---

## 5. Subscribe ask and comment question

Both are placed at **the moment the fact reverses**, which in this film is at **≈0:55–1:10** — not
at the end. 43% of viewers are still there at 60 seconds; almost nobody is at 30 minutes. The
reversal is not the Pennsylvania ruling (that is the third-act turn); it is the viewer's own
assumption breaking: a locked gate, a posted sign and a fence are the things a 55-year-old
landowner believes make entry unlawful, and beyond the curtilage they do not.

**Reversal beat, ≈0:52–1:05 (script guidance, not final prose):**
the gate, the lock and the sign are named one at a time, then: *"None of them are the line. The
line is drawn much closer to the house than that."*

**Subscribe ask, ≈1:05–1:14. Every clause is true and checkable:**

> "There are more cases like this one on the channel already, and there are more coming.
> If you want them, subscribe."

- "more like this one already" — true: 55 public long-forms (`scripts/yt_channel_index.py`,
  2026-08-10), the catalogue is warrants/searches/seizures.
- "more coming" — true: the 12:00 JST long-form slot is filled through 8/15 with further episodes
  in build; no promise of a sequel to *this* episode, which the owner rejected as a lie.
- No emotional command, no "smash", no "if this made you angry". The audience measures badly on
  those.
- **Do not** add "and hit like" here. The earned Like ask stays in the ending (row 10).

**Comment question, pinned and spoken once at ≈1:14–1:20:**

> "The camera in Pennsylvania stayed up for 78 days before anyone found it.
> If one went up on your land today, how long before you found it?"

Answerable (everyone has a number), specific to this episode (the 78-day figure is from the
Punxsutawney record and appears nowhere else on the channel), not a yes/no, and not an emotional
prompt. Pin it as the top comment at publish; put it verbatim in the description's second line.

---

## 6. Where I chose against the measured evidence, and why

1. **The 8-second montage hook (v2 row 9) is replaced by a 20.3-second voiced cold open, and it is
   written FIRST, not last.** Row 9 is BINDING and says the opposite on all three points. Reason:
   the owner's instruction for this episode inverts the order, and the measurement in §0 shows the
   current row-9 structure puts 11.5 seconds of *silence* across the steepest loss in the film.
   **This needs an owner approval record (APR) before the build starts** — it is a deviation from a
   binding row, not an interpretation of it.
2. **The katz shape opens with a year; T1's cold open has a `[YEAR]` slot instead of a year.** The
   retrieved facts do not contain the install year and invariant 1 forbids supplying one. §3
   FACT-LOCK 1 gives the fallback.
3. **Three of the four titles invert the Unseen pattern's second segment.** The pattern is "what the
   *powerful* party does not know"; here the withheld knowledge runs the other way — the landowner
   is the one not told. Writing it the pattern's way round would be false. T4 keeps the pattern's
   grammar by stating the withholding as a rule ("Nobody Has to Tell Him"); T1–T3 state it plainly.
4. **The brand opening is moved, not removed,** even though the measurement says any full-stop in
   the first 30 seconds costs retention. `op_ed_bookends` is a hard gate and `OPENING_SEC` is fixed
   by invariant 14; a band overlay at 20.5s is the strongest available compromise.
5. **`docs/PD_WINNING_PATTERN.md` §3 and §8 were not applied.** They mandate second-person,
   question-form, 11–12 minute packaging. The ⚠ override block at the top of that same file voids
   all three with a larger sample, and instructs that the section not be used as a design basis.
   I followed the override.

---

---

## 7. OPENING OVERLAY — 動画オープニング設計書ルール準拠（2026-08-10 追記）

`C:/Users/aab15/CLAUDE.md`（動画オープニング設計書の作成ルール）に従って数値で書く。
同ルールが禁じる「重ねる、1〜2秒」のような抽象表現は、この節には一つも無い。
セクション0（Remotion設定）と5（レンダーコマンド）は PD で既に確定しているため再掲しない。

### 7.0 環境・Remotion設定（マニュアル セクション0）

リポジトリから読んだ実値。**記憶ではない。**実装者がここを見れば調べ直す必要がない。

| 項目 | 値 | 出所 |
|---|---|---|
| 解像度 | **1920 × 1080** | `remotion/src/brand.ts` `BRAND.video` |
| fps | **30** | 同上（※オープニング設計書ルールの例示は60fps だが、PD の長尺は30fps。**F値は必ず `useVideoConfig()` の fps から算出**する） |
| composition id | `Ep66Openfields` | `remotion/src/Root.tsx` に登録 |
| durationInFrames | `Math.round((hookSeconds + narrationSeconds + OPENING_SEC + ENDCARD_SEC) * fps)` | `CaseFilm.tsx` の算出式。**直書きしない** |
| 中間画像形式 | **png**（`setVideoImageFormat`） | `remotion/remotion.config.ts` |
| コーデック | h264 / CRF **16** / `yuv420p` | 同上 |
| 色空間 | **bt709**（`setColorSpace`） | 同上 |
| 音声 | **aac 320k**（`setAudioBitrate`） | 同上 |
| GPU | **angle**（`setChromiumOpenGlRenderer`） | 同上 |
| 並列度 | `os.cpus().length`（WebGL を含む長尺は `--concurrency=4`） | 同上＋正典 §7 |

必要な依存パッケージ（**既に導入済み。再インストール不要**）:

```bash
npm i @remotion/motion-blur     # Trail。7.3 の入退場で使用
```

**新規 Composition は作らない。** `Ep66Openfields` は既存の `CaseFilm` を呼ぶだけで、
`BrandOpening` に `variant='overlay'` を渡す。部品を fork しないこと（invariant 14）。

### 7.1 前提と不変条件

- 対象は既存部品 `remotion/src/components/Bookends.tsx` の `BrandOpening`。**新規作成しない**
  （invariant 14・row 14「canonical、fork するな」）。
- 追加するのは **`variant` プロップのみ**。既定 `'card'` は現在の全画面3.5秒で、
  **EP62–65 は1ビットも変わらない**。EP66 だけ `'overlay'` を指定する。
- `OPENING_SEC = 3.5` と `ENDCARD_SEC = 9` は**変更しない**（row 14 が固定と定めている）。
- **fps は `useVideoConfig()` から取得**。フレーム数の直書きは禁止。以下の F は
  `Math.round(秒 * fps)` で算出した値であり、30fps のときの実数を括弧で示す。

### 7.2 秒数ベースのタイムライン（開始 20.5s / 全長 3.5s）

| 区間 | 秒 | F（30fps） | 起きること |
|---|---|---|---|
| in  | 20.50–20.90 | 0–12   | スクリム＋モノグラムが**下から**入る |
| in  | 20.63–21.10 | 4–18   | シリーズ名が**マスク切り上がり**（+4F スタッガー） |
| in  | 20.77–21.30 | 8–24   | タイトルが**マスク切り上がり**（+8F スタッガー） |
| hold| 21.30–23.10 | 24–78  | 静止。**本編カットとナレーションは裏で流れ続ける** |
| out | 23.10–24.00 | 78–105 | 3要素が **-6F ずつ逆スタッガー**で下へ抜ける |

**ナレーションは止めない。**この3.5秒の裏で `OP` セクションの台詞（≈34語）が進行する。
これが本節の存在理由であり、全画面カードを 8.0–11.5s に置く現行方式が
**毎秒2.13pt 落ちる区間**を無言で潰していた問題への対処である。

### 7.3 各モーションの数値（**等速線形は禁止**・opacity単独は禁止）

| 要素 | 開始F | 終了F | 移動量 | イージング | opacity |
|---|---|---|---|---|---|
| スクリム帯 | 0 | 12 | translateY **+72 → 0 px** | `spring({fps, config:{damping: 20, mass: 0.6}})` | 0 → 0.82（**translateY と併用**） |
| モノグラム | 0 | 12 | translateY **+40 → 0 px** ／ scale **0.94 → 1.0** | `spring({fps, config:{damping: 18, mass: 0.5}})` | 0 → 1（併用） |
| シリーズ名 | 4 | 18 | translateY **+100% → 0**（親 `overflow:hidden`） | `Easing.out(Easing.cubic)` | 常時 1（**マスクで見せる**） |
| タイトル | 8 | 24 | translateY **+100% → 0**（親 `overflow:hidden`） | `Easing.out(Easing.cubic)` | 常時 1（同上） |
| 退場（3要素） | 78 / 84 / 90 | +15 | translateY **0 → +64 px** | `Easing.in(Easing.cubic)` | 1 → 0（併用） |

- **スタッガー**：入場 +4F ずつ、退場 -6F ずつ。同時に動かさない。
- **モーションブラー**：入場・退場の translate に `@remotion/motion-blur` の `Trail`
  （`layers={6} lagInFrames={1.2}`）。hold 区間には掛けない。
- 数値はすべて**定数として1箇所に置く**（`OVERLAY = {inF: 12, holdF: 54, outF: 15, ...}`）。

### 7.4 レイヤー構成（下から。**最低3層**の要件を満たす）

1. **本編カット**（`OffthreadVideo` / 静止画）— 止めない。overlay は上に乗るだけ
2. **スクリム帯**（画面下 22%・`rgba(8,10,14,0.82)` の上端を 12px でフェード）
3. **モノグラム**（左・高さ 64px）
4. **文字**（シリーズ名 28px / タイトル 46px・`overflow:hidden` の親でマスク）

全画面カードと違い、**1層目が生き続ける**。これが「話が止まらない」の実装上の意味である。

### 7.5 props と型

```ts
type BrandOpeningProps = {
  seriesLabel: string;
  title: string;
  subtitle?: string;
  variant?: 'card' | 'overlay';   // 既定 'card' = 現行。EP62-65 は無変更
};
```

`film.json` 側は `openingVariant?: 'card' | 'overlay'` と `leadSeconds?: number`
（既定 `hookSeconds + OPENING_SEC`、EP66 は **0**）を受け取る。
どちらも任意であり、宣言しない既存話の挙動は変わらない。

### 7.6 確認方法

`npm run studio` で `Ep66Openfields` を開き、**20.5s と 24.0s の前後 15F** を1コマ送りで見る。
確認する点は3つ——①本編カットが裏で動き続けているか ②文字が下から**マスクで**現れるか
（フェードだけになっていないか）③3要素が同時に動いていないか。

**書き出しコマンド**（マニュアル §5 の「props差し替えで量産できる形」）:

```bash
# 本番（全尺）。film.json が overlay と leadSeconds を運ぶので追加フラグは要らない
bash scripts/_finish_episode.sh openfields Ep66Openfields 66

# オープニングだけ確認する（0:18–0:26 の8秒＝frames 540-780 @30fps）
cd remotion && npx remotion render Ep66Openfields ../out/ep66_op_check.mp4 \
  --public-dir=public_ep66 --frames=540-780

# variant を差し替えて比較する（card = 現行の全画面／overlay = 本設計）
cd remotion && npx remotion render Ep66Openfields ../out/ep66_op_card.mp4 \
  --public-dir=public_ep66 --frames=540-780 \
  --props='{"openingVariant":"card"}'
```

**props を差し替えるだけで両方が出せる**こと自体が要件である（マニュアル「再利用部品は
props化してコマンドで量産可能にする」）。`variant` をコードに直書きしてはならない。

## 8. What must happen next, in order

1. **Owner approves T1 (+T3 as B), one thumbnail variant, and the 20-second cold open** — this
   package, before any script exists.
2. **APR written** for the row-9 deviation in §6.1.
3. **R2/R3 fact ledger** resolves the three FACT-LOCK items in §3.
4. `episodes/PD-2026-066-rainwaters/episode_spec.v001.json` written (duration profile, section
   vocabulary incl. `OP`, `forbidden_subjects`, `forbidden_claims`, mandatory stills).
5. Engine changes §4.1–4.5 applied through `scripts/pd_edit.py`, with EP62–65 re-verified
   bit-identical (the `leadSeconds` fallback).
6. Script written to serve items 1–3, not the other way round.

*This document is the contract for the front of EP66. If a later stage wants to change the title,
the thumbnail or the first twenty seconds, it writes v002 and gets it approved again — it does not
edit this file.*
