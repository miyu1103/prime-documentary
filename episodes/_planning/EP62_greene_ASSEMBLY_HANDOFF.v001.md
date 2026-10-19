# EP62 greene — 組み立て側への引き継ぎ v001

**2026-08-04 · 設計スレッドから** · 対象: `PD-2026-062-greene` / *Greene v. Lindsey*, 456 U.S. 444 (1982)

> ⚠️ **2026-08-04 追補あり。`EP62_greene_ASSEMBLY_ADDENDUM.v001.md` を先に読むこと。**
> 目視QCでモチーフの連鎖（同じ一枚のドアの七つの状態）が作られていないことが分かり、**13枚を差し替え・1枚追加**した。
> 本書と矛盾する場合は**追補が正**。

> **一行**：設計と画像は揃った。**ナレーション・filmconfig・Remotion合成は未着手で、そこからが組み立て側**。
> **state は `script_review` であって `script_verified` ではない。**私が一度 `script_verified` と書いて、それが事実でなかったので戻した。

---

## 0. いま何が本当なのか（数字で）

| | 状態 | 実測 |
|---|---|---|
| 契約 `episode_spec.v001.json` | ✅ valid | 27–32分 / 5,100–5,600語 / 8区分 / 13–17 beats / distinct_video 234 / mandatory_stills **223** |
| `manifest.json` | ✅ | `target_duration_minutes: 30` · **state = `script_review`** |
| 事実台帳 | ✅ | 107行（VERBATIM 69 / 隔離 15） |
| FILM_BIBLE | ✅ | 支配思想・モチーフ7状態・転回・認知・拒否事項 |
| 台本 `script.en.v003.md` | ✅ 両ゲート緑 | **5,250語 = 29:50**（176語/分・gap込み） |
| 画像 | ✅ **226枚** | 全部 3840×2160・欠番0・重複0・変種0 |
| 画像の配置 | ✅ | `remotion/public/greene/img/` に226枚＋顔登録 `P001–P014` |
| 実写プール | ⚠ **9本** | 47本取り込み → 目視38本却下 → 形状/話またぎで3本追加却下 |
| figure beats | ✅ 96個 **v002** | 各幕15–17（契約帯13–17）· `set_figure_beats --dry-run` exit 0 · **v001は破棄**（台本v004と不整合・引用5件が非逐語） |
| thumb_prompts | ✅ 4案 | `G220/G221/G222` ＋ 新規 `G240` 案（旧 `G226` 案は廃止） |
| fact_recheck | ✅ | 108主張（LOCKED 101 / 要出典5 / 隔離2）※その後の修理で全件処理 |
| ショート | ✅ 3本 | `short259` / `short260` / `short261`（導線レコードあり・**video ID待ちで意図的に不合格**） |
| **R15（音読）** | ❌ **未実施** | 4話とも。誰も声に出して読んでいない |

---

## 1. ファイル一覧（全部フルパス）

**契約と状態**
```
episodes\PD-2026-062-greene\episode_spec.v001.json          ← 数値の唯一の出所。ツールはここしか読まない
episodes\PD-2026-062-greene\manifest.json                   ← target_duration_minutes 30 / state script_review
```

**台本と設計**
```
episodes\_planning\EP62_greene_script.en.v003.md            ★ 確定版。v001/v002 は使わない
episodes\_planning\EP62_greene_FILM_BIBLE.v001.md           ← なぜこの順で語るか
episodes\_planning\EP62_greene_FACTS_LEDGER.v001.md         ← 事実の出所。✓/VERBATIM 以外は使用不可
episodes\_planning\measurements\EP62_greene_RAW.md          ← 判決文の全文。引用の照合先はここ
episodes\_planning\EP62_greene_beats.v002.json              ★ 演出データ96個（**これを使う**。v001は台本v004と不整合＝破棄）
```

**画像**
```
episodes\_planning\EP62_greene_CODEX_BATCH_A.v002.md        ← 発注書。§7に3回ぶんの追記あり（後述）
H:\pd-media\assets\ai\greene\G001.png … G240.png            ← 生成物（原本）
remotion\public\greene\img\                                 ★ レンダーが読むのはここ。226枚＋P001–P014 配置済み
```

**素材（実写）**
```
remotion\public\greene\factory\                             ← 47本。うち採用9本
runs\qc\greene_clip_verdicts.v001.json                      ← 却下38本の理由つき
episodes\PD-2026-062-greene\05_visuals\factory_clip_qc.v001.json
```

**パッケージング**
```
episodes\PD-2026-062-greene\04_scenes\thumb_prompts.v001.md ← サムネ4案＋A/Bタイトル対
episodes\PD-2026-062-greene\01_research\fact_recheck.v001.md
```

**レビュー記録（読まなくても組めるが、なぜ今の形かはここにある）**
```
episodes\_planning\EP62_greene_CRAFT_REVIEW.v001.md         ← 初回 12 FAIL
episodes\_planning\EP62_greene_REREVIEW.v001.md             ← 再採点 6 FAIL・21指摘
episodes\_planning\EP62_greene_SECOND_OPINION.v001.md       ← 敵対的な事実読み・45指摘（HARD 16）
```

**ショート**
```
episodes\_planning\SHORTS_SLATE_EP62-65.v001.md             ← short259/260/261 の設計
episodes\PD-2026-062-greene\09_package\short259_funnel.v001.json  （260/261 も同）
```

---

## 2. そちらの作業（この順で）

### ① ナレーション生成

```
py -3.11 scripts\gen_newshort_narration.py  ...    ※長尺用の生成器名は現行のものに読み替え
```

- 声 `nPczCjzI2devNBz1zQrb` / `eleven_multilingual_v2` / stability≈0.35 / similarity≈0.80
- **台本は `script.en.v003.md` のみ。**`v001` `v002` は残置してあるが使わないこと
- **⚠ 私はまだ回していない。**理由は §5「未解決」を読んでから判断してほしい

### ② `filmconfig` を作る（これが無いと何も始まらない）

`episodes\_planning\EP62_greene_filmconfig.v001.json` は**存在しない**。EP61 のものが唯一の雛形。必要な欄と、いま埋まるかどうか：

| 欄 | 状態 |
|---|---|
| `slug` / `episode_id` / `out` | すぐ書ける |
| `hookSeconds` | **8.0**（オーナー決定 2026-08-04） |
| `hookLine` | 台本 HOOK の25語をそのまま |
| `assets` → `05_visuals\asset_manifest.vNNN.json` | **未作成**。画像は配置済みなので生成できる |
| `narration_index` → `06_audio\narration_index.v001.json` | ①の生成物 |
| `narration` → `remotion/public/greene/narration.mp3` | ①の生成物 |
| `captions` → `08_edit\captions.final.v001.srt` | 強制アラインメントの生成物 |

### ③ カット表は**生成する。手で書かない**

```
py -3.11 scripts\build_case_film_generic.py --config episodes\_planning\EP62_greene_filmconfig.v001.json
```
→ `04_scenes\greene_beatsheet.v001.json` と `greene_build_manifest.v001.json` が出る。
**`shotlist` を手書きしないこと。**EP38で廃止されており、二重実装（CLAUDE.md 不変条件14）になる。

### ④ figure beats を書き込む

```
.venv\Scripts\python.exe scripts\set_figure_beats.py --config <filmconfig> --beats episodes\_planning\EP62_greene_beats.v002.json --min-per-act 13
```
`--dry-run` は既に exit 0（97個・各幕15–17）。**config ができるまで書き込めないだけ。**

### ⑤ Remotion 合成を登録

`remotion\src\Root.tsx` に `Ep62` で始まる composition が**無い**。`npm run typecheck` を緑にすること。

### ⑥ レンダー前の必須検査

```
.venv\Scripts\python.exe scripts\check_episode_inputs.py --slug greene      ← 6件の不足を全部潰してから
.venv\Scripts\python.exe scripts\check_spec_satisfied.py --slug greene      ← film.json 生成後・レンダー前
```

---

## 3. この話に固有の罠（先に読むと事故が減る）

### 3-1. 実写が9本しかない。**これは欠陥ではなく設計**

`check_episode_inputs` はこう言う：

> `asset_reuse will FAIL: 9+0 distinct video assets vs ~234 footage cuts`

**そのとおりで、想定内。**この話はアーカイブで成立しない。実測：

- 47本取り込み → **目視で38本却下**（東京・京都・砂浜・鹿・ホラーピエロ・トイレットペーパー。全部検索語には合っていた）
- さらに `scan_video_shape` が3本（720p）、`check_cross_episode_reuse` が0本を却下
- **`front door` `mailbox` `stairwell` は14万行のアーカイブでヒット0**

だから **234 − 9 = 225枚を発注した**（＋最後の画1枚で226）。

**⚠ 決定的な事実：`check_spec_satisfied.py` の `distinct_video_assets` は、実写と `remotion/public/greene/motion/*.mp4` だけを数える。静止画は1枚も数えない。**

```python
videos = {n for n in names if n.lower().endswith(VIDEO_SUFFIXES)}
need = int(spec["distinct_video_assets"])
if len(videos) < need: ...
```

**つまり226枚は、動かして初めて資産になる。**i2v（Wan2.2 5B / `ae-demo\comfy_wan.py`）か深度パララックス（`gen_depth_maps.py` → `DepthImage`）で `motion/` に書き出すこと。**ズーム/パンだけは不可**（オーナーが紙芝居として却下済み）。動いているかは連続フレーム差分で実測してから出すこと。

### 3-2. `mandatory_stills` は223件。サムネ3枚は**入っていない**

`check_spec_satisfied` は「宣言された静止画がどのカットにも無い」で落ちる。サムネはカットではないので、**`G220/G221/G222` は意図的に除外してある**。**足し戻さないこと。**

### 3-3. 発注書 §5 の ENDING ビート欄は**古い台本のコピー**

`CODEX_BATCH_A.v002.md` の §5 ENDING 節には、v003 で消えた表現（「7〜8人の男」など）が残っている。**§7 に読み替え表がある。**画像生成には影響しないが、そこから台本の文言を拾わないこと。

### 3-4. ループは `G227` で閉じる。`G230` ではない

台本 ENDING のコールバックは `G227`（紙が平らに貼られた同フレーム）。`G230`（テープごと消えた無地）は ENDING の別カット。**最後の画は `G231`**（褪せていない四角い跡）。§7 追加3 に明記。

### 3-5. `check_script_length` は前書きの散文も数える

上限がナレーション語数の**約200語上にしかない**。設計書の説明文を足すと映画本体が押し出される。台本ファイルに解説を書き足すときは注意。

---

## 4. 「間違って見えるが直してはいけないもの」

| | 理由 |
|---|---|
| 実写が9本 | §3-1。画像で埋める設計 |
| `mandatory_stills` が226でなく223 | §3-2。サムネを外してある |
| 「三人の**借主**」であって「三人の女性」ではない | **判決文に she / her / women / woman が0回**。性別は記録にない |
| 「紙が**貼られた**」であって「テープで」ではない | 判決文は *thumbtack, adhesive tape, **or other means*** としか言わない。**どれが使われたかは書いていない**。`【】`の演出指示はテープでよいが、**ナレーションは断定しない** |
| 反対意見の書き手は **O'Connor** | 契約の旧版が Stevens と誤記していた。Stevens はこの判決文に一度も出てこない（Stevens の反対意見は EP64） |
| 「掲示を禁止した」と言っていない | 判決文が明示的に *"we hold **only** that posted notice pursuant to §454.030 is constitutionally inadequate"* と限定している |
| 三人のその後を語らない | **判決文が沈黙している。**埋めない |
| 票数を出さない | **判決文に票数が印字されていない** |

---

## 5. 未解決（そちらの判断が要る／私が閉じられなかった）

### 5-1. ★ R15（音読）が未実施 — **本番VO前にここを通したい**

4話とも、**誰も声に出して読んでいない**。基準は「R15は省略しない。リズムは黙読では測れない」と定めている。担当4体は全員、代替の口語形分析を出したうえで「**読んでいないのに読んだ記録は書かない**」と明記した。

EP62で機械的に潰した口語形の欠陥：`not only … but indeed` の相関接続の分断、動詞の無い断片、固有名詞の壁（弁護士4名＋機関2つを一息）→ OSTに移動。

**残っているのは、聴かないと分からない部分。**下書き音声（SAPI等・無料）を作って一度聴いてから本番VOを回すのが、EP61の轍（VO生成後に台本が900語伸びて作り直し）を踏まない唯一の方法。

### 5-2. 台本は「基準を満たす」と私は言えない

3つの独立した検査が3回とも新しい欠陥を出した。最終の再レビューは **8 PASS / 6 FAIL**、その後82編集の修理を当てたが、**修理後の再々レビューはまだ回していない**。

修理で直った代表：
- 映画の中心的な一手が誤帰属だった（準備書面の言葉として、**それを倒すために裁判所が書いた文**を提示していた）
- 「この判決文にはどこにも数が無い」＝**偽**（11州・16年・6か月を数えている）
- 引用の末尾を書き手が書いていた箇所が**3件**

### 5-3. ML相当の未処理

- `G210` / `G211` は「女性」として発注済み。**ナレーションはもう性別に依存していない**ので、絵として使う分には矛盾しないが、再発注するなら性別を外せる
- 顔検出で14枚が `P###` に登録された（最大11.6%）。**設計は「顔が判別できない人物」**なので、目視QCの結果しだいで差し替えが要る（QC実行中）

### 5-4. ショート3本は導線が意図的に不合格

`check_short_funnel.py --short 259` は落ちる。**長尺の video ID が無いから**で、正しい挙動。長尺を非公開アップロードした時点で解ける。

---

## 6. 記録に残っている決定

| 日付 | 決定 |
|---|---|
| 2026-08-04 | **HOOKは8秒**（`PD_ONE_PASS_PRODUCTION_SPEC.v2` 行9）。研究側の「≤60秒」との矛盾はオーナー裁定で決着。`PD_SCREENPLAY_STANDARD` §16.5 に記録 |
| 2026-08-04 | **`script_words` を [4400,4900] → [5100,5600] に是正。**実測 wpm（EP60 191.4 / EP61 194.3）が設計値173を否定したため |
| 2026-08-04 | **各話30分。**`manifest.target_duration_minutes: 30` |
| 2026-08-04 | 契約の反対意見の書き手を **Stevens → O'Connor** に訂正 |
| 2026-08-04 | 契約の `forbidden_claims` の **Pannell Ray → Pamela Ray** |
| 2026-08-04 | ショート番号を **182–193 → 259–270** に変更（別スレが182–193を使用済みだった） |

---

## 7. 検査コマンドまとめ

```
.venv\Scripts\python.exe scripts\check_episode_spec.py --slug greene
.venv\Scripts\python.exe scripts\check_script_length.py episodes\_planning\EP62_greene_script.en.v003.md --lo 1620 --hi 1920
.venv\Scripts\python.exe scripts\check_script_craft.py  episodes\_planning\EP62_greene_script.en.v003.md --ledger episodes\_planning\EP62_greene_FACTS_LEDGER.v001.md --words 5100 5600
.venv\Scripts\python.exe scripts\check_episode_inputs.py --slug greene
.venv\Scripts\python.exe scripts\check_spec_satisfied.py --slug greene      # film.json 生成後
.venv\Scripts\python.exe scripts\check_final_acceptance.py PD-2026-062-greene --render <mp4> --emit-receipt
```

**受領書が緑になるまで予約も投稿もしない**（`.claude/rules/19-ship-gate.md`）。

---

*v001 · 2026-08-04 · 設計スレッドから。この文書に書いていない数字は、私が測っていない数字。*
