# EP75 · LAHAINA — PACKAGING v001

Title, thumbnail, description and the opening overlay. The thumbnail **art briefs** stay in
`EP75_lahaina_thumb_prompts.v001.md`; this file is the machine-facing packaging document that
`check_design_doc.py` reads, and §7 is the opening design spec required by
`C:/Users/aab15/CLAUDE.md`.

**Everything in §7 was read out of the implementation on 2026-08-21 — `remotion/remotion.config.ts`,
`remotion/src/brand.ts`, `remotion/src/components/Bookends.tsx`. Not one value is remembered or
guessed.**

---

## 1. The trap this episode has, in a sharp form

**This is a fire with a conspiracy audience attached.** The looseness that would dissolve the film's
own argument, and what to write instead:

| Wrong | Right | Why it matters |
|---|---|---|
| "the sirens failed" | **one siren was operable inside the burn perimeter** (Finding 37), and separately, **they were not activated** | No source says "failed". Merging two sources invents a third claim. ⛔-02, ⛔-03 |
| "if the sirens had sounded…" | the system existed, it was for this among other things, it had never once been used for a fire, and it was not used — **then stop** | **Not one of the 84 findings** says it would have changed the outcome. ⛔-01, AB-01 |
| "the cause is still unclear" | **6:34 a.m., pole 25, re-energised broken lines, classified Accidental** | Raising a question and leaving it open is the register of the material this film sits beside. ⛔-04 |
| "the power went out and the pumps stopped" | Finding 21: **uninterrupted power, full capacity, for the duration** | This is the version most viewers arrive with, and the record says the opposite. ⛔-08 |
| "they left too early" | reported out at 14:17 · the County says its crews went **above and beyond** · Finding 67 says the mopup that works in normal weather was insufficient in that weather | Three sentences, in that order, every time. ⛔-16 |

---

## 2. Title candidates

Row 13 of `PD_ONE_PASS_PRODUCTION_SPEC.v3`: **59–100 characters**, third person, no question form,
no second person, no case citation, a searchable proper noun, at least two variants.

Every row was run through `check_packaging_claims.py --slug lahaina --title "<title>"` against the
script and both ledgers (694 sentences). The measured column is that run.

| # | title | chars | measured |
|---|---|---|---|
| **A** | `Hawaii Built the World's Largest Warning Siren Network. It Had Never Been Used for a Fire.` | 90 | **PASS · unsupported=0 · zero soft notes** — recommended, ships with thumbnail T2 |
| **B** | `Only One Siren Was Operable Inside the Burn Perimeter at Lahaina on August 8, 2023.` | 83 | **PASS · unsupported=0 · zero soft notes** — the only title thumbnail T1 may ship with |
| C | `The Evacuation Order Was Sent to Cellphones. Lahaina's Cell Service Had Died That Morning.` | 90 | PASS · unsupported=0 · 3 soft notes |
| D | `The Warning Network Was Tested Every Month. It Had Never Been Used for a Wildfire, Lahaina` | 90 | PASS · unsupported=0 · 2 soft notes |

**Barred title forms for this episode:** anything beginning *How* or *Why*; any question form; any
counterfactual (*would have*, *could have*, *if only*); the words *failed*, *ignored*, *covered up*,
*knew*; and any construction with a named person or agency as the grammatical agent of the outcome.

**A/B pair to ship: A with T2, and C with T4.** They fail differently.

---

## 3. Thumbnail

Four concepts, art briefs and their measured claim checks in
`EP75_lahaina_thumb_prompts.v001.md` §1. Ship **T2** (`NEVER USED` / `FOR FIRE`) with **T4**
(`SENT TO` / `DEAD PHONES`) as the pair; T1 is the third variant `thumbnail_candidates_min` requires.
Subject is the siren pole or the padlocked gate — **never a fire, never an aerial of the burned town,
never a face.**

---

## 4. Description

Draft: `episodes/PD-2026-075-lahaina/09_package/description.draft.v001.txt`, 3,567 characters,
measured **PASS · unsupported=0**. The cause goes above the fold on purpose (⛔-04). The settlement
paragraph is procedural and carries its own date (⛔-15) and **must be re-verified on the day the
packaging is finalised** (⛔-11).

---

## 5. The hook, and where the brand opening sits

**The hook comes BEFORE the brand opening, and the opening never interrupts it.**

| | |
|---|---|
| hook | **0:00.000 – 0:20.266**, voiced from frame 0, measured from `narration_index.v001.json` |
| `BrandOpening` | **starts at 0:20.266**, the instant the hook ends, and runs `OPENING_SEC` = 3.5 s |
| `BrandEndcard` | the last **9.0 s** (`ENDCARD_SEC`), 30:57.4 – 31:06.4 |

`filmconfig.hookSeconds = 20.266`. Spec v3 row 9 requires the brand opening to be off the 10–15 s
window, which is the steepest loss in the channel's measured retention curve; at 20.3 s it is clear
of it.

---

## 6. Opening variant and leadSeconds — decided

**`openingVariant: "overlay"`. `leadSeconds: 0`.** Both are written in
`EP75_lahaina_filmconfig.v001.json` and both are deliberate:

- `leadSeconds: 0` because the hook is voiced from frame 0, so there is **no silent runway** in front
  of the body for a full-screen card to occupy. Under the `card` layout the opening would not render.
- `openingVariant: "overlay"` because the brand furniture then sits in a band across the bottom while
  **the picture and the narration keep running underneath** — nothing cuts away and nothing pauses.

---

## 7. OPENING OVERLAY — 動画オープニング設計書ルール準拠

`C:/Users/aab15/CLAUDE.md`（動画オープニング設計書の作成ルール）に従い、すべて数値で書く。
同ルールが禁じる抽象表現はこの節に一つも無い。**フレーム直書きはしない。**F値はすべて
`Math.round(秒 * fps)` の算出結果であり、括弧内は 30fps のときの実数である。

EP75 は EP66 以降と同じ **overlay** レイアウトである。**新規部品は作らない。**既存の
`remotion/src/components/Bookends.tsx` の `BrandOpening` を `variant='overlay'` で呼ぶだけで、
本節はその実装の実数を書き写したものである（推測値はひとつも無い）。

### 7.0 環境・Remotion設定（マニュアル セクション0）

リポジトリから読んだ実値。**記憶ではない。**実装者はここだけ見れば調べ直す必要がない。

| 項目 | 値 | 出所 |
|---|---|---|
| 解像度 | **1920 × 1080** | `remotion/src/brand.ts:22` `BRAND.video` |
| fps | **30**（マニュアルの例示は60だが PD 長尺は 30。**F値は必ず `useVideoConfig()` の fps から算出**） | 同上 |
| composition id | **`Ep75Lahaina`**（`Root.tsx` に未登録。`lahaina_film.json` が出来た時点で追加する） | `remotion/src/Root.tsx` |
| durationInFrames | `lahainaFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps)` ＝ `Math.round((narrationSeconds + ENDCARD_SEC) * fps)`。実測では `Math.round((1857.403 + 9.0) * 30)` = **55,992F** | **直書き禁止** |
| 中間画像フォーマット | **png**（`setVideoImageFormat('png')`） | `remotion/remotion.config.ts:3` |
| コーデック | **h264 / libx264**・**CRF 16**・`x264Preset: slow` | 同上 4–6 |
| pixelFormat | **yuv420p** | 同上 7 |
| colorSpace（色空間） | **bt709**（`setColorSpace`） | 同上 8 |
| 音声 | **aac**・ビットレート **320k** | 同上 9–10 |
| 並列度 concurrency | `os.cpus().length`。ただし WebGL/深度を含む長尺は **`--concurrency=4`** | 同上 11 ＋ `feedback_perceptual_motion_and_verify` |
| GPU | **angle**（`setChromiumOpenGlRenderer('angle')`） | 同上 12 |

必要な依存パッケージ（**導入済み。再インストール不要**）:

```bash
npm i @remotion/motion-blur     # Trail。7.3 の入退場に使う
```

### 7.1 前提と不変条件

- 対象は既存部品 `Bookends.tsx` の `BrandOpening`。**新規作成も fork もしない**（invariant 14）。
- `OPENING_SEC = 3.5` と `ENDCARD_SEC = 9` は**変更しない**（`Bookends.tsx:34-35`）。
- overlay は `seriesLabel` と `title` だけを描く。`subtitle` は card 版のみが使う。
- 帯の位置とサイズは実装の `OVERLAY` 定数が持つ（`bandHeightRatio: 0.22` ＝ 1080px で 238px）。

### 7.2 秒数ベースのタイムライン（開始 20.266s ／ 全長 3.50s ／ 全区間を記述）

開始位置は `filmconfig` の `hookSeconds: 20.266`。フックが終わった瞬間に帯が上がる。

| 区間 | 秒（映画上） | 秒（相対） | F | 内容 | out |
|---|---|---|---|---|---|
| in | 20.266–20.666 | 0.000–0.400 | 0–12 | スクリム帯とモノグラムが画面下端から上がる | — |
| in | 20.399–20.866 | 0.133–0.600 | 4–18 | シリーズ名がマスクで切り上がる（+4F） | — |
| in | 20.533–21.066 | 0.267–0.800 | 8–24 | エピソードタイトルがマスクで切り上がる（+8F） | — |
| hold | 21.066–22.866 | 0.800–2.600 | 24–78 | 静止。裏の本編カットとナレーションは止まらない | — |
| out | 22.866–23.766 | 2.600–3.500 | 78–105 | 3要素が下へ抜ける（-6F の逆スタッガー） | **out** |

**ナレーションは止めない。**この 3.5 秒の裏で `OP` セクションの台詞が進む。
これが overlay を選ぶ唯一の理由であり、full-screen card との違いのすべてである。

### 7.3 各モーションの数値（**等速線形は禁止**・opacity 単独も禁止）

| 要素 | 開始F | 終了F | 移動量 | イージング | opacity |
|---|---|---|---|---|---|
| スクリム帯 | 0 | 12 | translateY **+72 → 0 px** | `spring({fps, config:{damping: 20, mass: 0.6}})` | 0 → 0.82（**translateY と併用**） |
| モノグラム | 0 | 12 | translateY **+40 → 0 px** ／ scale **0.94 → 1.0** | `spring({fps, config:{damping: 18, mass: 0.5}})` | 0 → 1（併用） |
| シリーズ名 | 4 | 18 | translateY **+100% → 0 px**（親 `overflow: hidden`） | `Easing.out(Easing.cubic)` | 常時 1（**マスクで見せる**） |
| タイトル | 8 | 24 | translateY **+100% → 0 px**（親 `overflow: hidden`） | `Easing.out(Easing.cubic)` | 常時 1（同上） |
| 退場（3要素） | 78 / 84 / 90 | +15 | translateY **0 → +64 px** | `Easing.in(Easing.cubic)` | 1 → 0（併用） |

- **スタッガー**：入場は +4F ずつ、退場は -6F ずつ。3要素を同時に動かさない。
- **モーションブラー**：入退場の translate に `@remotion/motion-blur` の `Trail`
  （`layers={6} lagInFrames={1.2}`）。hold 区間には掛けない（画素が変わらず時間だけ食う）。
- 数値はすべて**定数として1箇所**に置く：実装の `OVERLAY = { bandHeightRatio, scrimRisePx: 72,
  monoRisePx: 40, monoScaleFrom: 0.94, seriesDelaySec: 0.133, titleDelaySec: 0.267,
  outStartSec: 2.6, outStaggerSec: 0.2, outSec: 0.5 }`。
- **opacity だけで出る要素はひとつも無い。**上表のとおり全要素が translateY か scale を伴う。
- 秒はすべて `Math.round(sec * fps)` で F に変換する（`useVideoConfig()` の fps を使う）。

### 7.4 レイヤー構成（下から。最低3層の要件を満たす）

1. **本編カット**（`OffthreadVideo` ／ 静止画）— 止めない。overlay は上に乗るだけ
2. **スクリム帯**（画面下 22% ＝ 238px・`rgba(8,10,14,0.82)`・上端 12px はグラデでフェード）
3. **モノグラム**（左・高さ 64px・グロー無し）
4. **文字レイヤー**（シリーズ名 28px ／ タイトル 46px・いずれも `overflow: hidden` の親でマスク）

### 7.5 props と型

`type BrandOpeningProps = { seriesLabel: string; title: string; subtitle?: string; variant?: 'card' | 'overlay' }`

| prop | 型 | 値 |
|---|---|---|
| `seriesLabel` | `string` | `"PRIME DOCUMENTARY"` |
| `title` | `string` | `"Lahaina"` |
| `subtitle` | `string?` | `"The largest warning network in the world, and the one thing it had never been used for."`（endcard のみ） |
| `variant` | `'card' \| 'overlay'` | `'overlay'` |

`film.json` 側が受け取る props 名は **`openingVariant`**（`'card' \| 'overlay'`）と
**`leadSeconds`**（number）。EP75 は `openingVariant: 'overlay'`・`leadSeconds: 0`。

**§2 の YouTube タイトル（83–90字）は帯には入らない。**帯に出るのは `"Lahaina"` である。

### 7.6 確認方法

`npm run studio` で `Ep75Lahaina` を開き、**20.3s と 23.8s の前後 15F** を1コマ送りで確認する。
見る点は3つ——①本編カットが裏で動き続けているか ②文字が下からマスクで現れるか
（フェードだけになっていないか） ③3要素が同時に動いていないか。

**書き出しコマンド**（マニュアル §5 の「props 差し替えで量産できる形」）:

```bash
# 本番（全尺）
bash scripts/_finish_episode.sh lahaina Ep75Lahaina 75

# オープニングだけ確認する（0:19–0:25 ＝ frames 570-750 @30fps）
cd remotion && npx remotion render Ep75Lahaina ../out/ep75_op_check.mp4 \
  --public-dir=public_ep75 --frames=570-750

# variant を差し替えて比較する（card = 全画面 ／ overlay = 本設計）
cd remotion && npx remotion render Ep75Lahaina ../out/ep75_op_card.mp4 \
  --public-dir=public_ep75 --frames=570-750 \
  --props='{"openingVariant":"card"}'
```

**props を差し替えるだけで両方が出せること自体が要件である。**`variant` をコードに直書きしない。

---

## 8. What a human still has to confirm

The nine items in `EP75_lahaina_FILM_BIBLE.v001.md` §17, and above all the first three: that nothing
in the package completes the sentence *"if the sirens had sounded…"*, that the package never raises a
question it leaves open, and that the 14:17 → 14:55 gap never sits next to a word implying fault.
