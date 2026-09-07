# EP67 — PACKAGING PACKAGE (v001)

**Episode:** `PD-2026-067-ramirez` · slug `ramirez`
**Subject:** *TransUnion LLC v. Sergio L. Ramirez*, **594 U.S. 413 (2021)**, decided 25 June 2021.
A credit bureau matched a consumer's **first and last name only** against the U.S. Treasury's
sanctions list, flagged **8,185** people as potential terrorists and drug traffickers, and the
Supreme Court held **5–4** that **6,332** of them could not sue in federal court because the false
flag had never left the building.
**Written:** 2026-08-11. **Status:** DRAFT — owner approval required before the script is locked.

> **Order of work for this episode (owner rule):** title, thumbnail and the first twenty seconds are
> designed and approved FIRST. The body is written to serve them. This document is that first
> deliverable. Nothing below may be changed by the script writer without a new revision.

---

## 0. What this is built on, and what was measured while building it

Binding inputs read in full before a word of this was written:
`episodes/_planning/EP67_ramirez_FACTS_LEDGER.v001.md` (90 fact rows, 74 machine-verified
✓ VERBATIM quotations, 16 quarantine entries, 10 open questions),
`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`, `docs/PD_CANON.md`, `.claude/rules/19-ship-gate.md`,
`C:/Users/aab15/CLAUDE.md` (the opening design manual, reproduced as §7 below).

**The ledger's verifier was re-run before this package was written**, not taken on trust:

```bash
cd episodes/PD-2026-067-ramirez/01_research/sources && py -3.11 verify_quotes.v001.py
# VERIFIED 74 of 74  FAILED 0
```

Measurements that bind this package:

| Measured | Value | Where it came from |
|---|---|---|
| Title band | **59–100 chars**, no question form, no second person, no case citation | spec v2 row 13; `check_packaging_qc.TITLE_MIN_CHARS/TITLE_MAX_CHARS` |
| Narration pace, end to end | **159.5–169.7 wpm**; EP66's delivered master 4,278 words / 1604.211 s = **160.0** | `docs/PD_CANON.md` rule 25 |
| The narration tool's own `measured wpm` | **171.8 on EP66 — wrong by 7%**, because it counts speech and not the silence between chunks | same rule; do not use it |
| Thumbnail headline ink, this episode's candidates | **178–220 px** at size 248 (floor 150) | replicated `scripts/build_ep62_65_thumbnails.py` fitter, font resolved to `C:/Windows/Fonts/arialbd.ttf` |
| Archive supply for this story | **11,682 clips across 20 registers** (586 queries, two rounds) | `EP67_ramirez_FOOTAGE_PLAN.v001.md` |

**One thing this episode inherits and does not re-litigate.** Every PD long-form before EP66 put
11.5 seconds of silence in front of the first spoken word — an 8-second montage plus a 3.5-second
full-screen title card — straight across the 10→15s window where the channel loses 2.13 retention
points per second. EP66 closed that hole: narration starts at 0:00 and the brand mark became a
lower-band overlay. **EP67 is built on the closed version from the start.** `leadSeconds: 0`,
`openingVariant: 'overlay'`.

---

## 1. Title candidates

Pattern (row 13): `[dramatic present-tense clause] — [what is withheld] | The Case of [Name]`.
All four are third person, inside 59–100 chars, none begins with a question word, none contains
"you", and none contains a case citation or the phrase "Supreme Court Case". Character counts are
`len()` of the exact string including the pipe.

| # | Title | Chars |
|---|---|---|
| **T1 ★** | A Salesman Says His Name Is on a Terrorist List \| The Case of Sergio Ramirez | **76** |
| T2 | A Machine Compared Two Words and Flagged 8,185 Americans \| The Case of Sergio Ramirez | **85** |
| T3 | TransUnion Matched First and Last Name Only — Thousands Were Flagged \| The Case of Sergio Ramirez | **97** |
| T4 | A Jury Awards More Than $60 Million — Then 6,332 Winners Are Removed \| The Case of Sergio Ramirez | **97** |

**Ship T1 as A and T2 as B.** Row 13 requires at least two A/B variants; these two test the same
case from the human side and the machine side, so the difference between them is attributable.

One sentence on each, and where each one can go wrong:

- **T1 — RECOMMENDED.** The only candidate whose whole first clause is a single physical event a
  viewer can see in one beat: a man at a counter, a salesman, a sentence. It is also the only one
  drawn word-for-word from the record — ✓ *"A Nissan salesman told Ramirez that Nissan would not
  sell the car to him because his name was on a 'terrorist list.'"* (SR-03) — so the promise it
  makes is one the body pays off exactly. It withholds the machine, the class, the money and the
  judgment.
- **T2.** The strongest single idea in the case ("two words") attached to its largest number. It is
  accurate: ✓ *"TransUnion did not compare any data other than first and last names."* (LS-14) and
  the stipulated class was **8,185** (MN-02). It is more abstract than T1 and has no person in it,
  which is why it is B and not A.
- **T3.** Names the company. Accurate (LS-14), and "thousands" is safe where a precise figure would
  invite the wrong one. But a corporate name in the first two words reads as business news, and the
  audience is 92% male and 76% over 55 — it opens on the wrong register.
- **T4 — DO NOT SHIP WITHOUT AN OWNER LINE.** Every clause is true (MN-04, HD-11), but the sentence
  as a whole invites exactly the reading the ledger quarantines at ⛔-03: *"the Supreme Court took
  the money away."* It did not. The **Ninth Circuit** had already cut the punitive award from
  $6,353.08 to $3,936.88 per member (MN-06), and the Supreme Court set **no dollar figure at all**
  (MN-11). Kept here because it will be proposed by somebody eventually and this is the record of
  why it was not chosen.

**Accuracy note for whoever writes the metadata.** The three money figures are **not
interchangeable** and must never be blended: **$984.22** statutory *plus* **$6,353.08** punitive per
member as the **jury** awarded (MN-04); **$3,936.88** punitive per member as the **Ninth Circuit**
reduced it (MN-06); and **no figure whatsoever** from the **Supreme Court** (MN-11). Any total after
25 June 2021 is quarantined (⛔-04). Do not write "6–3" anywhere: it was **5–4** (⛔-01).

---

## 2. Thumbnail specification

Buildable by `scripts/build_ep62_65_thumbnails.py` with a `ramirez` entry added to its `SPEC` dict —
**no new builder** (invariant 14). What that builder actually does, read from the source and then
replicated here so every number below is measured rather than hoped for:

- Cover-crops the plate to 16:9 → **1280×720**, then lays a **black scrim at alpha 120 over the top
  66%** (y 0–475), so the picture keeps its own light below that line.
- Searches every contiguous 1–3 line break of the headline × sizes 248→100 step −4 and keeps the
  split whose **tallest glyph ink** is greatest while every line fits 1200 px wide. It warns below
  150 px.
- Kicker: fixed **46 px**, drawn as a filled accent tag under the headline. It has **no fitter**, so
  three short words is the ceiling.
- **The font it resolves to on this machine is `C:/Windows/Fonts/arialbd.ttf`.** It looks for
  `Anton-Regular.ttf` and `Oswald-Bold.ttf`; the repo holds `Anton.ttf` and `Oswald.ttf`, so neither
  matches and it falls through to Arial Bold. Every ink figure below was produced through that same
  resolution path. **If anyone renames the font files, re-measure.**

Gate targets: `thumb_subject_luma` wants subject-box (x 0.20–0.80, y 0.12–0.88) mean luma ≥ 60,
tallest bright connected component ≥ **150 px**, dark outline ring ≥ 12 px. `thumbnail_visibility`
wants selected-thumb mean luma ≥ 33. `episode_spec.thumbnail_candidates_min` is **3**.

**Plate rules for all three, and they are hard.** No real-person likeness — hands, shoulders, backs
and out-of-focus figures only, never a recognisable face presented as a named person, and **never
anything offered as a picture of Sergio Ramirez, of a real TransUnion credit report, of the actual
OFAC Letter, or of the Dublin dealership** (⛔-13, CLAUDE invariant 11). **No readable text anywhere
in the plate**: no legible document, no brand marks, no licence plates, no dealership signage — a
generated plate that reads as a real record is the one failure mode this episode cannot survive.
Generated plates commissioned at long edge ≥ 3840. **The lower third must be the brightest part of
the frame**, because the scrim eats the top 66% and the unscrimmed band at y 475–634 is what carries
`subject_luma`. Daylight or bright interior; no night plates.

### Variant 1 — recommended, pairs with T1

- **Image:** a car-dealership sales desk shot from behind the customer's shoulder — two adult hands
  flat on the desk, a set of car keys just out of reach on the far side, a computer monitor turned
  away from camera so its screen is a bloom of light and not a readable display. Showroom glass and
  a bright forecourt fill the lower third. No faces, no logos, no readable paper.
- **Headline:** `NAME ONLY` — **measured ink 184 px at size 248**, breaking `NAME / ONLY`.
- **Kicker:** `NO OTHER CHECK` — accent RED `#D22628`.

### Variant 2

- **Image:** an office desk drawer half open, a single unopened envelope lying inside it, the rest of
  the drawer empty; daylight from the left; the desk surface bright and uncluttered in the lower
  third. This is the majority's own image — ✓ *"as if someone wrote a defamatory letter and then
  stored it in her desk drawer"* (HD-08) — and it is the picture the whole third act argues with.
- **Headline:** `NEVER SENT` — **measured ink 184 px at size 248**, breaking `NEVER / SENT`.
- **Kicker:** `6,332 FILES` — accent GOLD `#E5B53A`.

### Variant 3

- **Image:** a dense field of small identical paper record cards seen from directly above, filling
  the frame, one card lifted slightly out of the grid and catching the light. Nothing on any card is
  legible — the texture reads as *records*, not as documents. Brightest at the bottom edge.
- **Headline:** `8,185 NAMES` — **measured ink 220 px at size 248**, breaking `8,185 / NAMES`.
- **Kicker:** `ONE CHECK EACH` — accent GOLD `#E5B53A`.

Measured alternatives, if a variant has to be replaced: `TWO WORDS` 184 px · `6,332` 220 px ·
`NOT SENT` 184 px · `IN THE DRAWER` 178 px · `$60 MILLION` 217 px · `A TERRORIST LIST` 152 px (this
last one only just clears the floor at size 204 — do not use it three lines deep).

**Archive backing for the plates.** The footage plan measured `car showroom` at **1** usable clip
and `showroom` at **1**; `office drawer`, `file cabinet`, `desk drawer`, `envelope` and `mailbox` all
return **0 usable** clips after both query rounds. **All three thumbnail plates are therefore
generated, not archive stills**, and the archive is not asked to supply the one thing it does not
have. Details and the retries behind each zero are in `EP67_ramirez_FOOTAGE_PLAN.v001.md` §3.

---

## 3. The first twenty seconds, as narration

Written to the katz shape — a time, a place, a person doing one thing, ending on something the
subject is not told — and against the tyler failure, which summarised the outcome inside the first
ten seconds and retained 0.447. **Every one of these words is spoken. There is no silent montage and
no silent card.** The narration audio starts at 0:00.

**Pace basis.** `docs/PD_CANON.md` rule 25: measured **159.5–169.7 wpm end to end**, with EP66's
delivered master at **160.0**. The table below is timed at **160.0 wpm** and is **56 words**, so it
occupies **19.8 s at the fast edge and 21.1 s at the slow edge**. The declared window is
**0:00.0–0:21.2**, and whatever is left over at the fast edge is a hold on the last image, not a
gap in the voice. **Re-time against the real ElevenLabs render before captions are locked** — these
are design targets, not measurements of an audio file that does not exist yet.

**HOOK — 0:00.0–0:21.2** · 56 words · voiced from frame 0 · written before the body, not after it.

| Time | Words spoken | On screen |
|---|---|---|
| **0:00.0–0:01.9** | "Dublin, California. February 27th, 2011." | Archive: a bright suburban Californian forecourt, parked cars in rows, slow 6% push-in. Nobody in frame yet. |
| **0:01.9–0:05.3** | "Sergio Ramirez has come to buy a Nissan Maxima." | Two cuts, ~1.7 s each, motion carried left to right: archive car-lot row; generated plate — a saloon car's door and window from outside, a reflection of sky across the glass. No badge, no plate, no face. |
| **0:05.3–0:08.3** | "His wife is with him, and his father-in-law." | Generated plate — three adults' shoulders and backs at a sales desk, seen from behind, out of focus beyond the near hands. **Nobody in this film is offered as a picture of a real person** (⛔-13). |
| **0:08.3–0:13.9** *(THE BEAT)* | "The salesman runs a credit check, comes back, and says Nissan will not sell him the car." **"credit check" lands at ≈0:10.2; "will not sell" at ≈0:12.3.** | Three plates, ~1.9 s each, hard-cut with 0.35 s motion-blurred pushes: (1) a hand on a keyboard, monitor light on the knuckles; (2) the monitor's back, its glow spilling round the edge — **the screen is never legible**; (3) the keys on the desk, untouched. Cut 3 holds longest. |
| **0:13.9–0:16.5** | "His name is on a terrorist list." | Cut to black-level 12% for 4 frames, then a wide of the empty forecourt through showroom glass. The line lands on the cut, not inside a shot. |
| **0:16.5–0:21.0** | "The letter that follows will not say how to argue with it." | Generated plate — a plain white envelope face down on a kitchen table, one corner lifted, morning light. Slow drift in. No address, no logo, no readable text of any kind. |
| **0:21.0–0:21.2** | *(hold — the question is standing, unasked)* | The envelope, still unopened. |
| **0:21.6–0:24.0** | "His wife buys the car in her own name." *(first line after the window — the reversal seed)* | Same table; the brand overlay rises over the lower band here (§4). |

Exact words at exact seconds, as asked: *"Dublin"* at 0:00.0 · *"Ramirez"* at ≈0:02.6 ·
*"wife"* at ≈0:05.7 · *"salesman"* at ≈0:08.8 · *"credit"* at ≈0:10.2 · *"sell"* at ≈0:12.4 ·
*"terrorist"* at ≈0:15.5 · *"letter"* at ≈0:17.2 · *"argue"* at ≈0:20.1.

**What is deliberately absent from these twenty-one seconds:** the word "court", the word "Supreme",
the ruling, the vote, the class, the money, the name TransUnion, the word OFAC, and any statement of
who won. A viewer at 0:21 knows that a man was refused a car because a list had his name on it and
that the letter he got would not tell him how to fight it. **That viewer does not know whether any
of this was allowed, and does not know that 8,184 other people got the same letter.** That is the
standing question, and the body spends twenty-eight minutes paying it off.

### Every clause traced to the ledger, before this is recorded

| Clause | Ledger row | Status |
|---|---|---|
| "Dublin, California. February 27th, 2011." | SR-01 ✓ VERBATIM | exact |
| "has come to buy a Nissan Maxima" | SR-01 ✓ *"seeking to buy a Nissan Maxima"* | exact |
| "His wife is with him, and his father-in-law." | SR-01 ✓ *"accompanied by his wife and his father-in-law"* | exact |
| "The salesman runs a credit check" | SR-02 (the report was produced and carried the alert) | supported |
| "says Nissan will not sell him the car" | SR-03 ✓ *"Nissan would not sell the car to him"* | exact |
| "His name is on a terrorist list." | SR-03 ✓ *"because his name was on a 'terrorist list'"* | exact, and it is the **salesman's** sentence — §6 fixes how it is attributed on screen |
| "The letter that follows will not say how to argue with it." | SR-10 ✓ *"the OFAC Letter did not include instructions for initiating a dispute"* | exact |
| "His wife buys the car in her own name." | SR-04 ✓ VERBATIM | exact |

**Nothing in the hook is an inference about anyone's state of mind**, which is what ⛔-05 and ⛔-07
forbid, and **the salesman is never named, characterised or given invented dialogue** (⛔-08). The
one line of his that appears is the line the Supreme Court printed.

---

## 4. Where the brand opening and the brand endcard go

**`BrandOpening` is placed at 0:21.6**, as a 3.5-second lower-band overlay running **0:21.6–0:25.1**,
over footage and narration that never stop. **`BrandEndcard` is placed at the tail**, 9.0 seconds
long, starting at `narrationSeconds` and running to the end of the composition — i.e. at
**≈28:40–28:49** at the design centre. Both are the canonical components in
`remotion/src/components/Bookends.tsx`; **neither is forked** (invariant 14, spec v2 row 14, which
fixes `OPENING_SEC = 3.5` and `ENDCARD_SEC = 9.0`).

**OP — 0:21.6–0:33.0.** The `OP` narration section runs under and past the overlay; the voice does
not stop for the brand mark. This is the whole reason the overlay exists.

Why 21.6 and not earlier: the hook window closes at 21.2, and a brand mark that arrives on top of a
standing question costs less than one that arrives instead of a question. Deleting it is not
available — `op_ed_bookends` is a hard gate and is measured on the built film by
`check_final_acceptance.check_bookends`, which was rewritten on 2026-08-10 precisely because
`leadSeconds: 0` with no variant used to render **no opening at all** and still pass.

`film.json` for this episode therefore declares, explicitly, both of:

```
"leadSeconds": 0,            // narration starts at frame 0; no silent lead
"openingVariant": "overlay"  // BrandOpening renders as a lower band, not a full-screen card
```

An `openingVariant` that is absent means `'card'`, and `leadSeconds: 0` with `'card'` is the
combination that renders nothing. **Both keys are declared. Neither is inferred.**

---

## 5. Subscribe ask and comment question

Both sit at **the moment the viewer's own assumption breaks**, not at the end. The reversal in this
film is not the Supreme Court's ruling — that is the third-act turn. It is earlier and smaller: the
viewer assumes a credit bureau checks who you are. It compared two words, and for every other kind
of data on the same report it used a second identifier.

**Reversal beat, ≈1:05–1:22 (script guidance, not final prose):** the identifiers OFAC itself
publishes are named one at a time — full name, address, nationality, passport, tax number, place of
birth, date of birth, former names (LS-08) — and then: *"It compared the first name. And the last
name. For tax liens, and for bankruptcies, the same company used a second identifier. OFAC data was
the only kind it matched on a name alone."* (LS-17)

**Subscribe ask, ≈1:22–1:31. Every clause is true and checkable:**

> "There are more cases like this one on the channel already, and there are more coming.
> If you want them, subscribe."

- "more like this one already" — true; the catalogue is warrants, searches, seizures and records.
- "more coming" — true; the 12:00 JST long-form slot is filled with further episodes in build. It
  promises no sequel to *this* episode, which the owner has rejected before as a lie.
- No emotional command, no "smash", no "if this made you angry". The audience measures badly on
  those.
- **Do not** add "and hit like" here. The earned Like ask stays in the ending.

**Comment question, pinned and spoken once at ≈1:31–1:38:**

> "TransUnion matched a first name and a last name, and nothing else.
> Name one other thing it could have compared that would have taken five seconds."

Answerable by anyone who has just heard the list (date of birth is the obvious answer and the
Third Circuit said so in 2010), specific to this episode, not a yes/no, not an emotional prompt.
Pin it at publish and put it verbatim in the description's second line.

---

## 6. Where I chose against something binding, and why

1. **The 8-second silent montage hook (spec v2 row 9) is replaced by a 21.2-second voiced cold open
   written FIRST.** Same deviation EP66 took, same reason: the current row-9 structure lays 11.5
   seconds of silence across the steepest retention loss in the film. **This needs an owner approval
   record (APR) before the build starts.** It is a deviation from a binding row, not a reading of it.
2. **The hook's central line is a quotation of the salesman, delivered in the narrator's voice.**
   ✓ *"A Nissan salesman told Ramirez that Nissan would not sell the car to him because his name was
   on a 'terrorist list.'"* is the record (SR-03), but the narrator says "the salesman … says", which
   makes the attribution audible. **On screen it is additionally set as an attributed quotation
   card** at 0:13.9. The salesman is never named, never depicted identifiably, never given a second
   sentence (⛔-08).
3. **The word "terrorist" appears in the title and in the hook, and is in
   `forbidden_subjects` for footage.** That is deliberate and not a contradiction. The word is what
   the salesman said and is the whole point of the episode; a *clip whose title contains the word* is
   almost certainly stock war or extremism footage and would be defamatory next to this story. The
   contract forbids the pictures, not the sentence.
4. **AE kinetic beats: six, not the "one or two" the 2026-08-04 approval names.** The owner's
   2026-08-11 instruction is 「AEはガッツリ使ってほしい。とにかく紙芝居をやめたい」, and this record has
   four numbers that carry the argument (8,185 / 1,853 / 6,332 / 5–4) plus the two-word comparison
   and the jury's two figures. Six beats over twenty-nine minutes is one every ~4.5 minutes, all of
   them mid-film. Named and bound to their script lines in `scripts/ae/jobs_ep67_ramirez.json` and in
   the film bible §12.5. **This widening also wants an owner line.**
5. **The ending is designed to work with the record's last day, 25 June 2021, as its last day.**
   Open question ○-04 — what happened on remand, whether the 1,853 recovered, whether it settled —
   could not be closed: CourtListener returned **HTTP 429** on the research pass and returns it until
   roughly 09:00. The ending does not gesture at an answer and does not invent one; §7 of the film
   bible marks the exact beat where a retrieved fact would slot in, and what would have to change.

---

## 7. OPENING OVERLAY — 動画オープニング設計書ルール準拠

`C:/Users/aab15/CLAUDE.md`（動画オープニング設計書の作成ルール）に従い、すべて数値で書く。
同ルールが禁じる抽象表現はこの節に一つも無い。**フレーム直書きはしない。**F値はすべて
`Math.round(秒 * fps)` の算出結果であり、括弧内は 30fps のときの実数である。

### 7.0 環境・Remotion設定（マニュアル セクション0）

リポジトリから読んだ実値。**記憶ではない。**実装者はここだけ見れば調べ直す必要がない。

| 項目 | 値 | 出所 |
|---|---|---|
| 解像度 | **1920 × 1080** | `remotion/src/brand.ts` `BRAND.video` |
| fps | **30**（オープニング設計書ルールの例示は60だが PD 長尺は 30。**F値は必ず `useVideoConfig()` の fps から算出**） | 同上 |
| composition id | **`Ep67Ramirez`**（`remotion/src/Root.tsx` に登録・中身は既存 `CaseFilm` を呼ぶだけ） | `Root.tsx` |
| durationInFrames | `Math.round((narrationSeconds + ENDCARD_SEC) * fps)`（`leadSeconds: 0` のため hook 分の加算は無い） | `CaseFilm.tsx` の算出式。**直書き禁止** |
| 中間画像フォーマット | **png**（`setVideoImageFormat('png')`） | `remotion/remotion.config.ts` |
| コーデック | **h264 / libx264**・**CRF 16** | 同上 |
| pixelFormat | **yuv420p** | 同上 |
| colorSpace（色空間） | **bt709**（`setColorSpace`） | 同上 |
| 音声 | **aac**・ビットレート **320k**（`setAudioBitrate`） | 同上 |
| GPU | **angle**（`setChromiumOpenGlRenderer('angle')`） | 同上 |
| 並列度 concurrency | `os.cpus().length`。ただし WebGL/深度を含む長尺は **`--concurrency=4`** | 同上＋正典 §7 |

必要な依存パッケージ（**導入済み。再インストール不要**）:

```bash
npm i @remotion/motion-blur     # Trail。7.3 の入退場に使う
```

**新規 Composition を作らない。** `Ep67Ramirez` は `CaseFilm` を呼び、`BrandOpening` に
`variant='overlay'` を渡すだけである。部品を fork しないこと（invariant 14）。

### 7.1 前提と不変条件

- 対象は既存部品 `remotion/src/components/Bookends.tsx` の `BrandOpening`。**新規作成しない**。
- 追加するのは `variant` プロップのみ。既定 `'card'` は現行の全画面3.5秒であり、
  **EP62–65 は1ビットも変わらない**。EP67 は `'overlay'` を指定する。
- `OPENING_SEC = 3.5` と `ENDCARD_SEC = 9.0` は**変更しない**（row 14 が固定と定める）。
- `BrandEndcard` は末尾 **9.0秒**（`Math.round(9.0 * fps)` = 270F）。位置は
  `from={Math.round(narrationSeconds * fps)}`。

### 7.2 秒数ベースのタイムライン（開始 21.60s ／ 全長 3.50s）

| 区間 | 秒 | F（30fps） | 起きること |
|---|---|---|---|
| in | 21.60–22.00 | 0–12 | スクリム帯とモノグラムが**下から**入る |
| in | 21.73–22.20 | 4–18 | シリーズ名が**マスク切り上がり**（+4F） |
| in | 21.87–22.40 | 8–24 | タイトルが**マスク切り上がり**（+8F） |
| hold | 22.40–24.20 | 24–78 | 静止。**本編カットとナレーションは裏で流れ続ける** |
| out | 24.20–25.10 | 78–105 | 3要素が **-6F ずつ逆スタッガー**で下へ抜ける |

**ナレーションは止めない。**この 3.5 秒の裏で `OP` セクションの台詞が進む
（0:21.6–0:33.0・約30語）。これが本節の存在理由である。

### 7.3 各モーションの数値（**等速は禁止**・opacity 単独も禁止）

| 要素 | 開始F | 終了F | 移動量 | イージング | opacity |
|---|---|---|---|---|---|
| スクリム帯 | 0 | 12 | translateY **+72 → 0 px** | `spring({fps, config:{damping: 20, mass: 0.6}})` | 0 → 0.82（**translateY と併用**） |
| モノグラム | 0 | 12 | translateY **+40 → 0 px** ／ scale **0.94 → 1.0** | `spring({fps, config:{damping: 18, mass: 0.5}})` | 0 → 1（併用） |
| シリーズ名 | 4 | 18 | translateY **+100% → 0 px**（親 `overflow:hidden`） | `Easing.out(Easing.cubic)` | 常時 1（**マスクで見せる**） |
| タイトル | 8 | 24 | translateY **+100% → 0 px**（親 `overflow:hidden`） | `Easing.out(Easing.cubic)` | 常時 1（同上） |
| 退場（3要素） | 78 / 84 / 90 | +15 | translateY **0 → +64 px** | `Easing.in(Easing.cubic)` | 1 → 0（併用） |

- **スタッガー**：入場は +4F ずつ、退場は -6F ずつ。3要素を同時に動かさない。
- **モーションブラー**：入退場の translate に `@remotion/motion-blur` の `Trail`
  （`layers={6} lagInFrames={1.2}`）。hold 区間には掛けない。
- 数値はすべて**定数として1箇所**に置く：`OVERLAY = { inF: 12, holdF: 54, outF: 15, bandH: 360, scale: 0.36 }`。

### 7.4 レイヤー構成（下から。最低3層の要件を満たす）

1. **本編カット**（`OffthreadVideo` ／ 静止画）— 止めない。overlay は上に乗るだけ
2. **スクリム帯**（画面下 22%・`rgba(8,10,14,0.82)`・上端 12px はグラデでフェード）
3. **モノグラム**（左・高さ 64px）
4. **文字**（シリーズ名 28px ／ タイトル 46px・`overflow:hidden` の親でマスク）

全画面カードと違い **1層目が生き続ける**。「話が止まらない」の実装上の意味はこれである。

### 7.5 props と型

```ts
type BrandOpeningProps = {
  seriesLabel: string;
  title: string;
  subtitle?: string;
  variant?: 'card' | 'overlay';   // 既定 'card' = 現行。EP62-65 は無変更
};
```

`film.json` 側が受け取る props 名は **`openingVariant`**（`'card' | 'overlay'`）と
**`leadSeconds`**（number）。EP67 は `openingVariant: 'overlay'`・`leadSeconds: 0`。
どちらも任意項目であり、宣言しない既存話の挙動は変わらない。

### 7.6 確認方法

`npm run studio` で `Ep67Ramirez` を開き、**21.6s と 25.1s の前後 15F** を1コマ送りで確認する。
見る点は3つ——①本編カットが裏で動き続けているか ②文字が下から**マスクで**現れるか
（フェードだけになっていないか） ③3要素が同時に動いていないか。

**書き出しコマンド**（マニュアル §5 の「props 差し替えで量産できる形」）:

```bash
# 本番（全尺）
bash scripts/_finish_episode.sh ramirez Ep67Ramirez 67

# オープニングだけ確認する（0:19–0:27 ＝ frames 570-810 @30fps）
cd remotion && npx remotion render Ep67Ramirez ../out/ep67_op_check.mp4 \
  --public-dir=public_ep67 --frames=570-810

# variant を差し替えて比較する（card = 現行の全画面 ／ overlay = 本設計）
cd remotion && npx remotion render Ep67Ramirez ../out/ep67_op_card.mp4 \
  --public-dir=public_ep67 --frames=570-810 \
  --props='{"openingVariant":"card"}'
```

**props を差し替えるだけで両方が出せること自体が要件である。**`variant` をコードに直書きしない。

## 8. What must happen next, in order

1. **Owner approves T1 (+T2 as B), one thumbnail variant, and the 21-second cold open** — this
   package, before the script is locked.
2. **APRs written** for the three deviations in §6: the row-9 hook inversion, the six AE beats, and
   the ending written without ○-04.
3. **○-04 retried** after 09:00 (CourtListener quota reset). If it returns, the slot marked in the
   film bible §7 takes it; if it does not, the ending stands as designed.
4. `episodes/PD-2026-067-ramirez/episode_spec.v001.json` — **written and validating** (it is).
5. Footage staged from `EP67_ramirez_FOOTAGE_PLAN.v001.md` §4, **with a labelled contact sheet
   looked at by a person before any clip enters a cut**.
6. Script written to serve items 1–3, not the other way round.

*This document is the contract for the front of EP67. If a later stage wants to change the title,
the thumbnail or the first twenty seconds, it writes v002 and gets it approved again — it does not
edit this file.*
