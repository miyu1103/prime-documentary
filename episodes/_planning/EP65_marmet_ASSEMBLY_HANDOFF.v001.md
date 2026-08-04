# EP65 marmet — 組み立て側への引き継ぎ v001

**2026-08-04 · 設計スレッドから** · 対象: `PD-2026-065-marmet` / *Marmet Health Care Center, Inc. v. Brown*, 565 U. S. 530 (2012) (per curiam)

> **一行**：**台本と発注書は揃った。画像は1枚も生成されていない。**ナレーション・filmconfig・カット表・Remotion合成は未着手で、そこからが組み立て側。
> **state は `script_review` であって `script_verified` ではない。**反証レビューが現行本文の一つ前の版に **DOES NOT MEET IT（R2/R3/R6/R11/R15 の5不合格）** を出し、その修理を当てた**あとの再レビューをまだ回していない**。

> ⚠️ **この話には他の3話に無い固有リスクが2つある。§3-1（尺）と §3-2（サムネ輝度）を先に読むこと。**

---

## 0. いま何が本当なのか（数字で・全部このスレッドで実測）

| | 状態 | 実測 |
|---|---|---|
| 契約 `episode_spec.v001.json` | ✅ valid（exit 0） | 1620–1920秒（27–32分）／ 5,100–5,600語 ／ 8区分 ／ beats 13–17/幕 ／ `distinct_video_assets` **234** ／ `people_plates_min` 10 ／ `mandatory_stills` **220** ／ `thumbnail_candidates_min` 3 ／ `audio_layers` 2 ／ 禁止被写体10・禁止主張9 |
| `manifest.json` | ✅ | `target_duration_minutes: 30` ／ `runtime_band_minutes [27.0, 32.0]` ／ **state = `script_review`** |
| 台本 `script.en.v002.md` | ✅ 3ゲート緑 | **370行** ／ 総語 **5,274**（`check_script_length`）／ **ナレ 5,172語**（`check_script_craft`・173wpm で 29.90分） |
| 尺の3点測定 | ⚠ | **slow 32.2分 ／ median 29.6分 ／ fast 22.2分**（fast = 実測 237.4 wpm）→ **§3-1** |
| 事実台帳 `FACTS_LEDGER.v001.md` | ✅ | 271行 ／ 主張ID `MB-01`–`MB-53`（53件）／ VERBATIM 表記 38 ／ 隔離 ⛔ 15 ／ 研究指示 ○ 22 |
| FILM_BIBLE | ✅ | `EP65_marmet_FILM_BIBLE.v001.md`（50,427 bytes）支配思想・モチーフ7状態・拒否事項 |
| figure beats | ✅ **97個** | HOOK 3 ／ OP 4 ／ ACT_1 16 ／ ACT_2 16 ／ ACT_3 17 ／ ACT_4 16 ／ ACT_5 17 ／ ENDING 8。**5幕すべて契約帯 13–17 内** |
| 発注書 `CODEX_BATCH_A.v001.md` | ✅ | **224枚 `R001`–`R224`・欠番0・重複0**（定義行を機械カウント） |
| `mandatory_stills` | ✅ 整合 | **220件**＝224 − サムネ4枚（`R217` `R218` `R219` `R224`）。**220件すべてが発注書に実在**（欠落0） |
| 画像（生成物） | ❌ **0枚** | `H:\pd-media\assets\ai\marmet\` は**ディレクトリごと存在しない** |
| 画像（配置） | ❌ **0枚** | `remotion\public\marmet\img` は**存在しない**（顔登録 `P###` も0） |
| 実写プール | ⚠ **11本** | 57本取り込み → **accept 11 / reject 46**（`05_visuals/factory_clip_qc.v001.json`）。契約 `distinct_video_assets` 234 に対し **11** |
| thumb_prompts | ✅ 4案 | `R217` `R218` `R219` ＋ 新規 `R224`。タイトル A/B 4組 |
| fact_recheck | ⚠ | `PASS_WITH_OPEN_ITEMS` — NEEDS SOURCE 5件（いずれも主題非依存）／ 隔離8件は v002 で全消滅 |
| 反証レビュー | ❌ **DOES NOT MEET IT** | `REREVIEW.v001.md`：PASS 10 / **FAIL 5**（R2 / R3 / R6 / R11 / R15）→ **§5-1** |
| ショート | ✅ 3本 | `short268` / `short269` / `short270`（導線レコードあり・`funnel_long_video_id` は3本とも `null` ＝ **video ID 待ちで意図的に不合格**） |
| filmconfig / narration / Remotion合成 | ❌ 全部未作成 | `check_episode_inputs --slug marmet` = **NOT READY・8件** |
| **R15（音読）** | ❌ **未実施** | 誰も声に出して読んでいない |

---

## 1. ファイル一覧（全部フルパス・**存在をこのスレッドで確認済み**）

**契約と状態**
```
episodes\PD-2026-065-marmet\episode_spec.v001.json          ✅ 数値の唯一の出所。ツールはここしか読まない
episodes\PD-2026-065-marmet\manifest.json                   ✅ target_duration_minutes 30 / state script_review
```

**台本と設計**
```
episodes\_planning\EP65_marmet_script.en.v002.md            ✅ ★確定版。v001 は使わない
episodes\_planning\EP65_marmet_script.en.v001.md            ✅ 残置（使わない）
episodes\_planning\EP65_marmet_FILM_BIBLE.v001.md           ✅ なぜこの順で語るか
episodes\_planning\EP65_marmet_FACTS_LEDGER.v001.md         ✅ 事実の出所。✓/VERBATIM 以外は使用不可
episodes\_planning\measurements\EP65_marmet_RAW.md          ✅ 判決文全文（CourtListener cluster 623142）
episodes\_planning\measurements\EP65_brown_remand_RAW.md    ✅ Brown II 全文（差戻し後・引用照合先）
episodes\_planning\EP65_marmet_beats.v001.json              ✅ 演出データ97個
```

**画像**
```
episodes\_planning\EP65_marmet_CODEX_BATCH_A.v001.md        ✅ 発注書 224枚（§7 に後追い追記2回）
H:\pd-media\assets\ai\marmet\                               ❌ 存在しない（生成物ゼロ）
remotion\public\marmet\img\                                 ❌ 存在しない（レンダーが読む場所。ここが空だと何も映らない）
```

**素材（実写）**
```
remotion\public\marmet\factory\                             ✅ 57本（★却下46本も同じ場所に入っている）
remotion\public\marmet\factory_pruned_offtopic\             ✅ 存在するが 0 ファイル
episodes\PD-2026-065-marmet\05_visuals\factory_clip_qc.v001.json  ✅ 57本の verdict（accept 11 / reject 46・理由つき）
runs\qc\marmet_clip_verdicts.v001.json                      ✅ 却下記録
runs\qc\marmet_factory\factory_footage_contact_01..03.png   ✅ ラベル付きコンタクトシート3枚
runs\qc\marmet_shape.json                                   ✅ scan_video_shape の出力
```

**パッケージング**
```
episodes\PD-2026-065-marmet\04_scenes\thumb_prompts.v001.md       ✅ サムネ4案＋A/Bタイトル4組
episodes\PD-2026-065-marmet\01_research\fact_recheck.v001.md      ✅ NEEDS SOURCE 5件
runs\qc\marmet_title_staging.v001.json                            ✅
```

**レビュー記録**
```
episodes\_planning\EP65_marmet_REREVIEW.v001.md             ✅ 反証レビュー（PASS 10 / FAIL 5・修理指示10項目）
```

**ショート**
```
episodes\_planning\SHORTS_SLATE_EP62-65.v001.md             ✅ short268/269/270 の設計
episodes\PD-2026-065-marmet\09_package\short268_funnel.v001.json  ✅（269/270 も同）
```

**存在しないもの（作るのは組み立て側）**
```
episodes\_planning\EP65_marmet_filmconfig.v001.json         ❌
episodes\PD-2026-065-marmet\06_audio\narration_index.v001.json  ❌
remotion\public\marmet\narration.mp3                        ❌
episodes\PD-2026-065-marmet\08_edit\captions.final.v001.srt ❌
remotion\src\Root.tsx の Ep65 composition                   ❌（Ep60Surfside / Ep61Weimer しか無い）
```

---

## 2. そちらの作業（この順で）

### ① ナレーション生成 — **ただし §3-1 を読んでから**

- 声 `nPczCjzI2devNBz1zQrb` ／ `eleven_multilingual_v2` ／ stability≈0.35 ／ similarity_boost≈0.80 ／ style 0 ／ speaker_boost on
- 台本は **`script.en.v002.md` のみ**
- **⚠ 私は回していない。**この話は**速い読みで 22.2分**まで落ちる。**最初の1本を出した直後に実尺を測り、27分床を割らないことを確認してから画像作業に入ること**（§3-1）

### ② `filmconfig` を作る（これが無いと何も始まらない）

`episodes\_planning\EP65_marmet_filmconfig.v001.json` は**存在しない**。雛形は `EP60_surfside_filmconfig.v001.json`。

| 欄 | 状態 |
|---|---|
| `slug` / `episode_id` / `out` | すぐ書ける（`marmet` / `PD-2026-065-marmet`） |
| `hookSeconds` | **8.0**（台本 HOOK は 0:00–0:08・4カット固定：R001 2.2s → R002 1.8s → R005 2.0s → R003 2.0s） |
| `hookLine` | 台本 L18 の2文をそのまま |
| `assets` → `05_visuals\asset_manifest.vNNN.json` | **未作成**。画像が配置されるまで作れない |
| `narration_index` → `06_audio\narration_index.v001.json` | ①の生成物 |
| `narration` → `remotion/public/marmet/narration.mp3` | ①の生成物 |
| `captions` → `08_edit\captions.final.v001.srt` | 強制アラインメントの生成物 |

### ③ カット表は**生成する。手で書かない**

```
py -3.11 scripts\build_case_film_generic.py --config episodes\_planning\EP65_marmet_filmconfig.v001.json
```
`shotlist` の手書きは EP38 で廃止済み（CLAUDE.md 不変条件14＝二重実装の禁止）。

### ④ figure beats を書き込む

```
.venv\Scripts\python.exe scripts\set_figure_beats.py --config <filmconfig> --beats episodes\_planning\EP65_marmet_beats.v001.json --min-per-act 13
```
97個・各幕16–17。**config ができるまで書き込めないだけ**で、データ側は揃っている。

### ⑤ Remotion 合成を登録

`remotion\src\Root.tsx` に `Ep65` で始まる composition が**無い**。`npm run typecheck` を緑にすること。

### ⑥ レンダー前の必須検査

```
.venv\Scripts\python.exe scripts\check_episode_inputs.py --slug marmet      ← 現在 8件の不足
.venv\Scripts\python.exe scripts\check_spec_satisfied.py --slug marmet      ← film.json 生成後・レンダー前
```

---

## 3. この話に固有の罠（先に読むと事故が減る）

### 3-1. ★ 尺 — **4話のなかでいちばん短く着地する。速い読みで 22.2分**

`check_script_length` の実出力（このスレッドで実行・PASS）：

```
PASS script_length: 5,274 words (need 3,699-5,480)
  narration estimate  slow 32.2m | median 29.6m | fast 22.2m
  target band         27.0-32.0 min
  ! RISK: at the fast end of the measured pace (237.4 wpm, seen on williams/florence)
    this lands at 22.2 min -- under the floor.
```

**22.2分は契約下限 27.0分を 4.8分下回る。**4話のなかで最も低い値である。原因は語数ではなく**読み速度の分散**で、
過去に williams / florence で **237.4 wpm** が実測されている。設計側の 176 wpm（gap込み）では 29:23 で収まる。

**やること（順序を守る）**

1. **声速を固定する。**ElevenLabs の設定を1回決めたら、全チャンクで同じにする。
2. **最初のナレーション書き出しを、必ず実尺で測る。**（`ffprobe` で連結後の秒数）
3. **27分床を満たすことを確認してから画像作業に入る。**足りなければ台本側で埋める。
   埋め方は**説明の追加ではなく帰属句（「州最高裁はこう書いた」型のリードイン）**である
   （`REREVIEW.v001.md` 末尾の指定）。
4. **VO を回したあとで台本を伸ばさない。**EP61 はそれで作り直しになっている。

### 3-2. ★ サムネ輝度 — **この話の `[STYLE]` は輝度ゲートと正面衝突する**

発注書 §2 の `[STYLE]` は全枚に **"flat overcast Appalachian daylight, low contrast, low-key"** を課している。
一方 `check_final_acceptance.py` のサムネ判定は**両方 HARD**：

```
THUMB_MIN_MEAN_LUMA    = 33.0
THUMB_MIN_CONTRAST_STD = 40.0
```

**扱いは設計側で既に固定してある。組み立て側は次の3点を動かさないこと。**

- **サムネ4枚（`R217` `R218` `R219` `R224`）には輝度オーバーライドが掛かっている。**
  発注書末尾に明記：*「サムネプレートだけは本編の低輝度指定を上書きし、平均輝度38以上・標準偏差45以上を狙うこと」*。
  **★ここに本編の house style（low contrast / low-key）を「戻さない」。**戻した瞬間に T8 を落とす。
- **ただし `R217` `R218` `R219` のプロンプト本文は1文字も書き換えない。**この3枚は本編プレートとして
  `[STYLE]` 付きで発注済みであり、`R001`–`R219` は ids・prompt bodies ともに byte-identical で機械検証されている。
  **明るさとコントラストは合成側（グレード）で作る**（`thumb_prompts.v001.md` §T8注記）。
- **`R224` だけは `[STYLE]` を使わない。**スタイルを本文に書き切ってある（硬いキーライト＋長い影＋明るいカウンター）。
  `[NEG]` のみ発注書 §2 のものを逐語で使う。**記録された逸脱**である。
- 輝度で落ちる可能性が最も高いのは **`R219`**（暗い室内＋冬窓）。合成後に測って落ちたら**候補から外す。持ち上げて眠い絵にしない。**

### 3-3. 実写が11本しかない。**これは欠陥ではなく設計**

`check_episode_inputs` の実出力：

> `asset_reuse will FAIL: 11+0 distinct video assets vs ~234 footage cuts, so ~223 clip(s) must repeat`
> `only 11 clip(s) survived visual QC, but a 0-minute film needs about 117 at the reuse cap (46 were rejected)`

**そのとおりで、想定内。**57本取り込み → 目視・形状・話またぎで46本却下 → 残 11本。
契約 `distinct_video_assets` 234 − 実写11 = **223** が発注枚数の根拠になっている（§7 に計算が書いてある）。

**⚠ 決定的な事実（コードで確認済み・`scripts/check_spec_satisfied.py` L37/L89/L131）：**

```python
VIDEO_SUFFIXES = (".mp4", ".mov", ".webm", ".m4v")
videos = {n for n in names if n.lower().endswith(VIDEO_SUFFIXES)}
need = int(spec["distinct_video_assets"])
if len(videos) < need: ...
```

**`distinct_video_assets` は動画ファイル名しか数えない。静止画は1枚も数えない。**
つまり **224枚は、動かして初めて資産になる**。i2v（Wan2.2 5B / `ae-demo\comfy_wan.py`）か
深度パララックス（`gen_depth_maps.py` → `DepthImage`）で `remotion/public/marmet/motion/` に書き出すこと。
**ズーム/パンだけは不可**（オーナーが紙芝居として却下済み）。動いているかは連続フレーム差分で実測してから出す。

**もう1点：`remotion\public\marmet\factory\` には却下46本も入ったままである。**
ビルダーは**フォルダではなく `05_visuals/factory_clip_qc.v001.json` の `verdict == "accept"` を読むこと。**

### 3-4. 発注書の**枚数の記述が古い**。数えたほうを信じる

発注書の散文には、実体と合わない数字が3か所ある（**プレート定義そのものは正しい**）。

| 場所 | 書いてある | 機械カウントの実体 |
|---|---|---|
| タイトル行 | 「219枚」 | **224枚** |
| §3 | 「`R001.png` … `R219.png`。欠番を作らない」 | **`R001`–`R224`**・欠番0・重複0 |
| §7 冒頭 | 「合計は **223枚**になります」 | **224枚**（`R224` 追記後に直す指示が実行されていない） |
| §7 末尾 | 「`mandatory_stills` は **R001〜R223（223件）**へ更新済み」 | **220件**（`R217`–`R219` を除外済み。PEOPLE 10枚は**含まれている**） |
| §7 最終行 | 「本編 220枚 + PEOPLE 10 + THUMB 4」 | 足すと234で合わない。正しくは **本編220（PEOPLE 10 を内包）+ THUMB 4 = 224** |

### 3-5. `R224` を `mandatory_stills` に**足さない**（文書が矛盾している）

- `thumb_prompts.v001.md` §6-2 は **「`mandatory_stills` に `"R224.png"` を追加せよ」**と書いている。
- 発注書 §7 末尾（**後に書かれたほう**）は **「サムネ専用なので `mandatory_stills` には追加しない」**と書いている。
  理由：`check_spec_satisfied.py` は「宣言された静止画がどのカットにも無い」で落ちる。

**現在の spec は 220件で、`R224` は入っていない。これが正しい状態である。足し戻さないこと。**
同じ理由で `R217` `R218` `R219` も意図的に除外してある。

### 3-6. `R220` / `R221` は `[NEG]` を**1語だけ**削って展開する

`[NEG]` には `wheelchair,` が入っている。**この2枚に限りその1語だけを削る**（他は一切変えない）。
削り忘れると指定した被写体を打ち消したまま生成される。`R222` `R223` は `[NEG]` をそのまま使う。
`R220` `R221` に**顔・医療機器・点滴・モニタが写ったら不合格**（発注書 Q10）。

### 3-7. 椅子は**プラントであってモチーフではない**

- `R222` = ACT_1（台本 L60・**ナレーションなし・3秒ホールド**）／ `R223` = ENDING の最終画（約26分後の回収）。
- **`R004` / `R075` / `R176` / `R201` は普通のカットであり、椅子ビートとして切らないこと**（台本 L62 の指示）。
- ループは **モチーフ状態1（ACT_1 冒頭の空の罫線）→ 状態7（ENDING の `R223`）**で閉じる。
  **`R001`（HOOK 1枚目）は最後の画ではない。**`R001` は真上からのマクロで、椅子も机も入らない。

### 3-8. docket 番号は**画面だけ・声には乗せない**

台本 L335：`【OST, dockets on screen only, never in the voice: No. 35494 REVERSED AND REMANDED · No. 35546 REVERSED AND REMANDED · No. 35636 CERTIFIED QUESTION ANSWERED】`
**字幕・ナレーションに戻さないこと。**（`No. 35494` は台本全体で**この1回だけ**出現する）

### 3-9. 台本に引用符が**1つも無いのは設計**

`script.en.v002.md` の引用符文字数は **0**（`"` `“` `”` `‘` `’` `「` `」` すべて0・コードポイント計数で確認）。
判決文の言葉は**帰属句（「州最高裁はこう書いた」）で立て、地の文として読ませる**形になっている。
**字幕やテロップを作り直すときに引用符を足さないこと。**足すと、口語化のために文法を整えた4か所
（§4 の表）が「逐語引用」に化ける。

---

## 4. 「間違って見えるが直してはいけないもの」

| | 理由 |
|---|---|
| 実写が11本 | §3-3。画像で埋める設計。234 − 11 = 223 が発注枚数の根拠 |
| `mandatory_stills` が224でなく220 | §3-5。サムネ4枚を意図的に外してある |
| サムネ4枚だけ明るい・硬い光 | §3-2。本編の `[STYLE]` を**意図的に上書き**している。戻すと輝度ゲートで落ちる |
| 台本に引用符が1つも無い | §3-9。帰属句で立てる設計 |
| 判決文の語を文法だけ変えている6か所 | 逐語ではなく**間接話法**だから。意味は原文と同一（機械照合済み・§下表） |
| HOOK の8秒のうち2カットが椅子 | `R004` は「一度きりのプラント」。第二モチーフではない（台本 L15） |
| 「三家族」を1つに束ねていない | **Marchio の契約は内容が違う**（carve-out なし・filing fee の記載なし）。`forbidden_claims` |
| 「全員が差し戻された」と言っていない | 処分が**一様でない**。Brown/Taylor = Reversed and remanded、Marchio = 認証質問に「Yes」。`spec.notes` |
| 票数・執筆者を出さない | **per curiam**。原文に著者名も票数も印字されていない |
| 患者の年齢・容態・死因を語らない | **5ページの per curiam に書かれていない。**埋めない（台帳 ○-01） |
| 「あなたの母親」と言わない | 判決文に *mother* が**一度も出てこない**。関係性は記録に無い（`forbidden_claims`） |
| 疑問文が全編で **1つだけ** | 意図的。`check_script_craft` の上限 2.0/1000語に対し 0.19/1000語で PASS |

**文法だけ調整した4か所（逐語ではないと承知のうえで使っている）**

| 台本 | 原文 | 変更 |
|---|---|---|
| L88 | *"...but made no exceptions ... and did not mention filing fees."* | 主語 `it` を2回補った |
| L82 | *"The contracts included a provision holding the party filing the arbitration responsible for paying..."* | 分詞句を独立文（`is responsible for`）に |
| L228 | *"not addressing the question whether..."* | `not addressing` → `had not addressed` |
| L198 | *"[W]hen state law prohibits outright..."* | 角括弧を外した（音声化のため） |
| L78 | *"The contracts included a clause requiring the parties to arbitrate all disputes..."* | `included` → `Both contained` |
| L182 | *"...the Federal Arbitration Act (FAA), 9 U. S. C. §1 et seq., with respect to..."* | 法令引用 `9 U. S. C. §1 et seq.` を省略記号なしで落とした |

---

## 5. 未解決（そちらの判断が要る／私が閉じられなかった）

### 5-1. ★ 台本は「基準を満たす」と私は言えない

`EP65_marmet_REREVIEW.v001.md` の結論は **DOES NOT MEET IT（PASS 10 / FAIL 5：R2 / R3 / R6 / R11 / R15）**で、
10項目の修理順序が付いている。**その修理を当てた結果が現在の v002 である**（レビューが読んだ版は 371行・5,184語、
現在は **370行・5,172語**）。機械的に確認できた着地：

| 指示 | 現在の本文 |
|---|---|
| 2. HOOK と最終行の時制・帰属を直す | ✅ `"Everything went to arbitration"` = **0件** ／ `"All disputes go to arbitration."` = **0件** |
| 4. 語り手の宣言文6本を削る | ✅ `"the reason this case has an ending worth telling"` = 0件 ／ `"the distance between them is the case"` = 0件 ／ `"has already gone wrong"` = 0件 |
| 5. docket 三つを画へ移す | ✅ `No. 35494` は **OST の1回のみ**（§3-8） |
| — 語数 | ✅ 5,172語（帯 5,100–5,600 内）。レビューが警告した「5,090に落ちて下限割れ」は**起きていない** |

**しかし、修理後の本文に対する再レビューは回していない。**だから state は `script_review` のままである。
R6（モチーフが一つでない＝椅子が7回出る）と R11（`R001` と最終画の構図一致）は**本文の宣言で処理しており**
（台本 L15/L16/L62 が「椅子はプラント・`R001` は最後の画ではない」と明記）、
**それが十分かどうかは判定されていない。**

### 5-2. ★ R15（音読）が未実施

**誰も声に出して読んでいない。**`PD_SCREENPLAY_STANDARD` §16 は「R15は省略しない。リズムは黙読では測れない」と定めている。
レビュー担当は代替分析を出したうえで「**読んでいないのに読んだ記録は書かない**」と明記している。
**下書き音声（無料の合成音声）を1回聴いてから本番VOを回すのが、§3-1 の尺リスクと同時に潰せる唯一の順序である。**

### 5-3. 実写 11本 対 契約 234

§3-3 のとおり設計だが、**契約数値そのものは緩めていない**。`check_spec_satisfied` は
静止画を1枚も数えないので、**224枚を motion に変換しない限りこの検査は必ず落ちる。**
「知って受け入れる偏差」にするか、motion 化で満たすかは組み立て側の判断。**黙って通さないこと。**

### 5-4. `fact_recheck` の NEEDS SOURCE 5件

`PASS_WITH_OPEN_ITEMS`。5件はいずれも主題に載っていない（テーゼ非依存）で、修理案が書かれている。
**隔離8件は v002 で全て消えている**ことを確認済み。

### 5-5. 引用監査の残余 — **UNSOURCED は0件**

このスレッドで機械監査を回した結果（正規表現抽出 + 語境界照合 + 逆方向のファジー整列）：

- 台本の**ハード事実 48種**（日付・年・数値・条項番号・docket）を語境界で原典corpus（判決文＋Brown II＋台帳）に照合 → **corpus に無いもの 0件**
- 台帳の引用スパン59件のうち **32件が台本に逐語で存在**、**10件がファジー一致**（うち実際の語句調整は **6件**・§4 の表／残り4件は照合窓の境界による副産物。**意味が変わるもの 0件**）、**12件は台本が使っていない**
- spec の引用断片14件は**すべて `forbidden_claims` / `notes` の「言ってはいけない文」か Brown II の逐語**であり、映画が主張する事実ではない
- **UNSOURCED（裏の無い引用）は 0件。**

### 5-6. 具体性がいちばん薄い区間（`check_script_craft` は 9.70 sentences/min で床5.0を大きく上回るが、分布は均一でない）

**最長の「固有名詞・日付・金額・地名が1つも出ない区間」= 台本 L130–L140。**
**ナレーション6行・320語・176wpm で約 109秒。**内容は Brown I の附合契約（adhesion contract）の教義で、
*"the court"* としか言わない抽象論が2分近く続く。**画で具体を入れるならここ。**

次点：L252–L260（4行・166語・約57秒）／ L230–L236（4行・140語・約48秒）／ L304–L311（3行・123語・約42秒）。

### 5-7. ショート3本は導線が意図的に不合格

`short268` / `short269` / `short270` の `funnel_long_video_id` は3本とも `null`。
**長尺の video ID が無いから**で、正しい挙動。長尺を非公開アップロードした時点で解ける。

---

## 6. 検査コマンドまとめ（**期待値つき**・すべてこのスレッドで実行した実出力）

```
.venv\Scripts\python.exe scripts\check_episode_spec.py --slug marmet
→ [spec] marmet: valid -- runtime 1620-1920s, script 5100-5600 words, 8 sections,
         beats 13-17/act, 234 distinct video assets, 10 people plates,
         220 mandatory still(s), 10 forbidden subject(s)          exit 0

.venv\Scripts\python.exe scripts\check_script_length.py episodes\_planning\EP65_marmet_script.en.v002.md --lo 1620 --hi 1920
→ PASS script_length: 5,274 words (need 3,699-5,480)
   slow 32.2m | median 29.6m | fast 22.2m                          exit 0
   ! RISK: fast end (237.4 wpm) = 22.2 min -- under the floor      ← §3-1

.venv\Scripts\python.exe scripts\check_script_craft.py episodes\_planning\EP65_marmet_script.en.v002.md --words 5100 5600
→ narration 5172 words -> 29.90 min at 173.0 wpm
   emotion 0 / AI-smell 0 / spoken CTA 0 / you-your 0.19 per 1000w
   questions 0.19 per 1000w [1 total] / short sentences 24.3% [84/345]
   longest bare stretch 15.6s / specific sentences per min 9.70
   quarantined claims used 0
   PASS  every mechanical craft gate is green                      exit 0

.venv\Scripts\python.exe scripts\check_episode_inputs.py --slug marmet
→ NOT READY -- 8 problem(s):
   filmconfig / narration index / narration audio / 0 stills /
   0 people stills / 220 of 220 mandatory_stills missing /
   11 clips survived QC / no Ep65 composition in Root.tsx
   ★ 8件すべて潰してからレンダーへ

.venv\Scripts\python.exe scripts\check_spec_satisfied.py --slug marmet     # film.json 生成後・レンダー前
.venv\Scripts\python.exe scripts\check_final_acceptance.py PD-2026-065-marmet --render <mp4> --emit-receipt
```

**プレートの機械検算（発注書を書き換えたら必ず再実行する）**

```
発注書の定義行 `- `RNNN.png``          → 224行・distinct 224・R001..R224・欠番0・重複0
spec.mandatory_stills                   → 220件・distinct 220・全件が発注書に実在
発注書にあって mandatory_stills に無い  → R217 / R218 / R219 / R224（サムネ4枚・★これが正しい）
THUMB 見出し配下                        → R217 / R218 / R219（+ §7末尾の R224）
PEOPLE 見出し配下                       → R207..R216（10枚・people_plates_min 10 と一致）
```

**受領書が緑になるまで予約も投稿もしない**（`.claude/rules/19-ship-gate.md`）。

---

*v001 · 2026-08-04 · 設計スレッドから。**この文書に書いていない数字は、私が測っていない数字。***
