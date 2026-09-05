# EP64 memphis — 組み立て側への引き継ぎ v001

**2026-08-04 · 設計スレッドから** · 対象: `PD-2026-064-memphis` / *Memphis Light, Gas & Water Division v. Craft*, 436 U.S. 1 (1978)

> **一行**：設計・台本・発注書・事実台帳は揃っている。**画像は1枚も生成されていない。ナレーション・filmconfig・Remotion合成も未着手で、そこからが組み立て側。**
> **state は `script_review` であって `script_verified` ではない。**`manifest.json` 自身がその理由を書き残している（一度 `script_verified` と書かれ、事実でなかったので戻された）。

> ⚠️ **着手前に §3-1 の尺リスクと §4 の HOOK 訂正を必ず読むこと。**この2つは、読まずに進むと画像発注ぶんかVO生成ぶんが丸ごと無駄になる種類の項目である。

---

## 0. いま何が本当なのか（すべてこのスレッドで実測した数字）

| | 状態 | 実測 |
|---|---|---|
| 契約 `episode_spec.v001.json` | ✅ valid | 1620–1920秒（27–32分）/ 5,100–5,600語 / 8区分 / beats 13–17 / distinct_video **234** / people_plates **10** / `mandatory_stills` **215** / forbidden_subjects 9 / forbidden_claims 4 / audio_layers 2 |
| `manifest.json` | ✅ | `target_duration_minutes: 30` · band `[27.0, 32.0]` · **state = `script_review`** |
| 事実台帳 | ✅ | **ML-01〜ML-123 の123行**（欠番0・重複0）· **VERBATIM 110行** · 隔離/未解決 **22行**（⛔12 ／ ○10） |
| FILM_BIBLE | ✅ | 支配思想・モチーフ8状態・転回・認知・拒否事項 |
| 台本 `script.en.v002.md` | ✅ **3ゲート全緑** | `check_script_length` **5,461語**（帯 3,699–5,480）· `check_script_craft` ナレ **5,390語** = 31.16分 @173wpm · `check_episode_spec` valid |
| 台本の自前計測 | — | ナレーション **5,416語** / **398文** / 92%線は **L407**（ENDING冒頭）を通る |
| 演出データ `beats.**v002**.json` | ✅ **101個** | HOOK 3 / OP 4 / **ACT_1〜ACT_5 各17** / ENDING 9。**`beats.v001.json` は破棄（理由と全差分は §10）。組み立てでは参照しない。** |
| 発注書 `CODEX_BATCH_A.v001.md` | ✅ | **`M001`〜`M219` の219枚**（欠番0・重複0）· うち `mandatory_stills` 215枚は全件が発注書に実在 |
| **画像（生成物）** | ❌ **0枚** | `H:\pd-media\assets\ai\memphis\` は**存在しない** |
| **画像の配置** | ❌ **未作成** | `remotion\public\memphis\img\` は**存在しない** |
| 実写プール | ⚠ **採用16本 / 取り込み81本** | 目視57本却下 → `scan_video_shape` 2本 → `check_cross_episode_reuse` 6本 ＝ 却下65本 |
| `filmconfig` | ❌ **存在しない** | `EP64_memphis_filmconfig.*` は無い |
| Remotion composition | ❌ **存在しない** | `remotion\src\Root.tsx` に `Ep64` / `memphis` の記述が**0件** |
| ナレーション / 字幕 | ❌ **未生成** | `06_audio\` `08_edit\` ともディレクトリごと無い |
| thumb_prompts | ✅ 4案 | `M208` `M209` `M210` ＋ `M219`。A/Bタイトル対8本 |
| fact_recheck | ✅ | 引用98行の機械照合済み |
| ショート | ✅ 3本 | `short265` / `short266` / `short267`（導線レコード3件あり） |
| 独立再レビュー | ❌ **DOES NOT MEET THE STANDARD** | R1–R15 で失敗（詳細 §6-2） |
| **R15（音読）** | ❌ **未実施** | 誰も声に出して読んでいない |

**契約の記述と実測がずれている箇所（実測が正）。** 契約 `notes` とショート台帳は事実台帳を
「122行 / VERBATIM 109 / 隔離17」と書いているが、ディスク上の実物は **123行 / 110 / 22** である。
台帳が1行伸びたあと `notes` が更新されなかったものと見られる。**数を引くときは台帳本体を数えること。**

---

## 1. ファイル一覧（全部フルパス・存在を1件ずつ確認済み）

**契約と状態**
```
episodes\PD-2026-064-memphis\episode_spec.v001.json           ✅ 12,769 B ← 数値の唯一の出所。ツールはここしか読まない
episodes\PD-2026-064-memphis\manifest.json                    ✅  1,073 B ← state = script_review
```

**台本と設計**
```
episodes\_planning\EP64_memphis_script.en.v002.md             ✅ 36,676 B ★確定版。v001 は使わない
episodes\_planning\EP64_memphis_FILM_BIBLE.v001.md            ✅ 68,453 B ← なぜこの順で語るか
episodes\_planning\EP64_memphis_FACTS_LEDGER.v001.md          ✅ 65,932 B ← 事実の出所。✓/VERBATIM 以外は使用不可
episodes\_planning\measurements\EP64_memphis_RAW.md           ✅ 62,075 B ← 判決文全文。引用の最終照合先はここ
episodes\_planning\EP64_memphis_beats.v002.json               ✅ ★正典。演出データ101個（§10）
episodes\_planning\EP64_memphis_beats.v001.json               ✅ 21,594 B （残置・使わない・§10）
episodes\_planning\EP64_memphis_script.en.v001.md             ✅ 34,844 B （残置・使わない）
```

**画像**
```
episodes\_planning\EP64_memphis_CODEX_BATCH_A.v001.md         ✅ 69,313 B ← 発注書。§7 と★追加2/★追加 を必ず読む
H:\pd-media\assets\ai\memphis\                                ❌ 存在しない（画像未生成）
remotion\public\memphis\img\                                  ❌ 存在しない（配置先も未作成）
```

**素材（実写）**
```
runs\qc\memphis_title_staging.v001.json                       ✅ 取り込み81本の台帳
runs\qc\memphis_clip_verdicts.v001.json                       ✅ 却下65本の理由つき
runs\qc\memphis_factory\factory_footage_contact_01..05.png    ✅ コンタクトシート5枚（全タイル読了済み）
episodes\PD-2026-064-memphis\05_visuals\factory_clip_qc.v001.json  ✅
```

**パッケージング**
```
episodes\PD-2026-064-memphis\04_scenes\thumb_prompts.v001.md  ✅ サムネ4案＋A/Bタイトル対
episodes\PD-2026-064-memphis\01_research\fact_recheck.v001.md  ✅ 50,549 B 引用98行の機械照合
```

**レビュー記録**
```
episodes\_planning\EP64_memphis_REREVIEW.v001.md              ✅ 60,253 B ← 判定 DOES NOT MEET THE STANDARD
```

**ショート**
```
episodes\_planning\SHORTS_SLATE_EP62-65.v001.md               ✅ §4 が memphis（L234–L303）
episodes\_planning\SHORTS_SLATE_EP62-65_QUOTE_AUDIT.v001.md   ✅ 引用監査（§4 の欠陥を発見した文書）
episodes\PD-2026-064-memphis\09_package\short265_funnel.v001.json  ✅（266 / 267 も同）
```

**存在しないもの（＝そちらが作るもの）**
```
episodes\_planning\EP64_memphis_filmconfig.v001.json          ❌
episodes\PD-2026-064-memphis\06_audio\                        ❌
episodes\PD-2026-064-memphis\08_edit\                         ❌
remotion\src\Root.tsx の Ep64 composition                     ❌
```

---

## 2. そちらの作業（この順で）

### ① ナレーション生成 — **ただし §3-1 を読んでから**

- 声 `nPczCjzI2devNBz1zQrb` / model `eleven_multilingual_v2`
- **台本は `script.en.v002.md` のみ。**`v001` は残置してあるが使わないこと
- ElevenLabs はオーナー承認済み（確認不要）。ただし **cost/character は記録すること**
- **⚠ 最初の1本を出した時点で必ず実測する。**理由は §3-1。ここを飛ばすと画像219枚が無駄になりうる

### ② `filmconfig` を作る（これが無いと何も始まらない）

`EP64_memphis_filmconfig.v001.json` は**存在しない**。必要な欄と、いま埋まるかどうか：

| 欄 | 状態 |
|---|---|
| `slug` / `episode_id` / `out` | すぐ書ける（`memphis` / `PD-2026-064-memphis`） |
| `hookSeconds` | **8.0**（オーナー決定 2026-08-04） |
| `hookLine` | 台本 HOOK（L19）の3文をそのまま |
| `assets` → `05_visuals\asset_manifest.vNNN.json` | **画像が0枚なので今は作れない** |
| `narration_index` → `06_audio\narration_index.v001.json` | ①の生成物 |
| `narration` → `remotion/public/memphis/narration.mp3` | ①の生成物 |
| `captions` → `08_edit\captions.final.v001.srt` | 強制アラインメントの生成物（正典名を変えないこと） |

### ③ カット表は**生成する。手で書かない**

```
py -3.11 scripts\build_case_film_generic.py --config episodes\_planning\EP64_memphis_filmconfig.v001.json
```
**`shotlist` を手書きしないこと。**EP38で廃止済み・二重実装（CLAUDE.md 不変条件14）になる。

### ④ figure beats を書き込む

```
.venv\Scripts\python.exe scripts\set_figure_beats.py --config <filmconfig> --beats episodes\_planning\EP64_memphis_beats.v002.json --min-per-act 13
```
**★ `v002` を使うこと。`v001` は使わない（理由と全差分は §10）。**
実測: `--dry-run` **exit 0 / 101 beat valid**（HOOK 3 / OP 4 / ACT_1–ACT_5 各17 / ENDING 9）。
**⚠ 各幕ちょうど17個＝契約帯 13–17 の上限。**ビートを1つでも落とすと下限側には余裕があるが、
**1つでも足すと契約違反になる。**組み立て中にビートを追加しないこと。
**⚠ `build_case_film_generic.py::build_figures` は `figures[0]` と `figures[-1]` を AI開示の下三分で
上書きする。**v002 は HOOK 先頭と ENDING 末尾に開示カードを**明示的に置いてある**ので、
両端のビートを並べ替えたり足したりすると、置いた文言が黙って消える。

### ⑤ Remotion 合成を登録

`remotion\src\Root.tsx` に `Ep64` / `memphis` の記述が**0件**。`npm run typecheck` を緑にすること。

### ⑥ レンダー前の必須検査

```
.venv\Scripts\python.exe scripts\check_episode_inputs.py --slug memphis     ← 不足を全部潰してから
.venv\Scripts\python.exe scripts\check_spec_satisfied.py --slug memphis     ← film.json 生成後・レンダー前
```

---

## 3. この話に固有の罠

### 3-1. ★★ 尺リスク — **速い読みだと契約下限を4分割り込む**

`check_script_length` 自身が警告を出している。**この警告は無視できない。**

```
narration estimate  slow 33.4m | median 30.7m | fast 23.0m
target band         27.0-32.0 min
! RISK: at the fast end of the measured pace (237.4 wpm, seen on williams/florence)
        this lands at 23.0 min -- under the floor. Either pin the voice speed or write to 6,410 words.
```

- 中央値 **30.7分** なら契約帯のど真ん中で問題ない
- しかし **williams / florence で実測された 237.4 wpm** が出ると **23.0分**、**下限27分を4.0分割り込む**
- **`runtime_band` はオーナー承認済みの唯一のハード偏差**だが、4分の不足は「偏差」の規模ではない

**必ずこの順で守ること。**

1. **声のスピードをピン留めする**（`speed` を明示指定し、生成器の既定に任せない）
2. **最初のナレーションを出した時点で実尺を測る。**推定ではなく生成された音声ファイルの実測値
3. **その実測が27分の下限を満たすと確認できるまで、画像219枚の生成に入らない**

EP61 は VO 生成後に台本が伸びて作り直しになっている。**ここは測ってから進む工程である。**

### 3-2. 実写が16本しかない。**これは欠陥ではなく設計**

実測（`runs\qc\memphis_clip_verdicts.v001.json`）：

- **81本取り込み → 目視で57本却下**（暖炉ループ6本・ストロボ・墓地・サッカースタジアム・結婚式・
  仮想通貨のモニタ…全部検索語には合っていた）
- さらに `scan_video_shape` が**2本**却下（1366×720 と **1080×1920 の縦クリップ**。
  コンタクトシートは全タイルを同じ大きさで描くので、縦であることが見えなかった）
- `check_cross_episode_reuse` が**6本**却下（lech / flowers / young / onecoin・thompson・titan で使用済み）
- **却下65本・採用16本**

`check_episode_inputs` は `asset_reuse will FAIL: 16 distinct video assets vs ~234 footage cuts`
と言うはずで、**そのとおりで想定内**。だから `234 − 16 = 218枚` を発注してある（＋サムネ `M219` で219枚）。

**⚠ 決定的な事実：`check_spec_satisfied.py` の `distinct_video_assets` は実写と
`remotion/public/memphis/motion/*.mp4` だけを数える。静止画は1枚も数えない。**
**つまり219枚は、動かして初めて資産になる。**i2v（Wan2.2 5B / `ae-demo\comfy_wan.py`）か
深度パララックス（`gen_depth_maps.py` → `DepthImage`）で `motion/` に書き出すこと。
**ズーム/パンだけは不可**（オーナーが紙芝居として却下済み）。動いているかは連続フレーム差分で実測してから出す。

### 3-3. アーカイブに「この話の物」が無い

`heater` `radiator` `electricity meter` `fuse box` `power line` は**アーカイブにヒット0**
（`heater` の検索は `theater` を返す）。生き残った16本は炎・冬・カーテン・壁の影・ガスの火口・街灯である。
**うち5本がろうそく・3本がマッチ。**カット表がここに寄ると `footage_diversity` が落ちる。

### 3-4. 発注書 §4 の HOOK 表は古い → **§4 を読むこと**

`CODEX_BATCH_A.v001.md` の **§4（L144–L151）の HOOK 表は旧版**である。
正しい読み替えは同ファイル **★追加2（L775–L789）**にある。詳細は本書 §4。

### 3-5. 台本の反復は**全部わざと**

機械掃引の結果は §5 に全件載せた。**1件も直さないこと。**この台本は
「判決文を逐語で置く → 次の1文でその鍵語だけを反響させる」という型で書かれている
（`Missed work.` / `Possible.` / `Not at will. Only for cause.`）。反復を潰すと型が壊れる。

### 3-6. `check_script_craft` の短文比率が上限すれすれ

**33.4%（帯 20–35%・133文 / 398文）。** 緑ではあるが**天井まで1.6ポイントしかない。**
組み立て中に台本へ短い文を足すと（テロップ用の一言、つなぎの断片など）**簡単に赤へ落ちる。**
台本を触ったら必ず `check_script_craft` を再実行すること。

---

## 4. ★★ HOOK プレートの訂正（必読・発注書 §4 は古い）

**旧 HOOK の「一つの壁に二つのメーター」は事実として誤りだった。**
判決文（`RAW` L33 / ML-17）は *two separate gas and electric **meters** and only one water meter* ——
すなわち **two *sets* of meters**（ガス2＋電気2＋水道1）である。「壁」については判決文は**一言も書いていない**。

### HOOK に実際に出るのは、この3枚だけ

| HOOKカット | プレート | 内容（発注書の本文と一致を確認済み） |
|---|---|---|
| 1 | **`M003`** | 罫線まで一致する2通の請求書（フォルミカのテーブル、真上から） |
| 2 | **`M048`** | 最終通知がテーブル中央に1枚だけ置かれている（状態4／状態8で回収） |
| 3 | **`M005`** | 台に戻されないまま垂れた受話器（ACT_5 で回収） |

### `M001` / `M002` / `M004` は HOOK から外れた

**廃棄しない。**プレート自体は正しい。**ACT_1 と ACT_5 の通常カットへ降格**する。
プレートは1枚も増減していないので、**生成する枚数は219枚のまま**である。

台本 L17 の演出指示はこの訂正どおりに書かれている（`M003` / `M048` / `M005` を名指しし、
`M001` `M002` `M004` の降格を明記）。**台本と発注書 ★追加2 が正、発注書 §4 の表が誤。**

### この誤りが残っていた最後の場所（本スレッドで修正済み）

`episodes\PD-2026-064-memphis\04_scenes\thumb_prompts.v001.md` **L258** のタイトル案が
`Two Meters on One Wall. Both of Them Were Running`（49字）のままだった。
**`Two Sets of Meters. Both of Them Were Running`（45字）へ修正済み**（ML-17 ＋ ML-21 で裏づけ）。

**まだ残っている関連表現（判断が要る・§7-3）：** 同ファイル L117 のキッカー `TWO METERS` と、
ショート台帳 L255 のテロップ `TWO METERS`。**どちらも「壁」とは言っていない**ので本書では触っていないが、
*sets* を *meters* と言い換えている点では同じ数え違いである。

### ★ オーナー裁定 ⛔-08（2026-08-04）— **名前は可・番地 1019 は不可**

**narration・テロップ・プレート・ショートの全部に及ぶ。**

- `Willie S. Craft` / `Mary Craft` / `Alaska Street` は**使ってよい**
- **番地 `1019` は、どこにも出してはならない**
- 台帳 ML-16 の原文は *"Willie S. and Mary Craft, respondents here, reside **at 1019 Alaska Street** in Memphis."*
  ショート台帳 L253 は `…` で**省略して**短縮している（改変ではなく省略）。**この扱いを踏襲すること**
- 台本 v002 は L37 で番地を含まずに書かれている（`reside on Alaska Street in Memphis`）

---

## 5. 「間違って見えるが直してはいけないもの」

| | 理由 |
|---|---|
| 実写が16本 | §3-2。画像219枚で埋める設計 |
| `mandatory_stills` が219でなく**215** | サムネ4枚 **`M208` `M209` `M210` `M219`** を意図的に除外してある。`check_spec_satisfied` は「宣言された静止画がどのカットにも無い」で落ちるが、サムネはカットではない。**足し戻さないこと** |
| `mandatory_stills` の M208–M210 が欠番 | 同上。欠番ではなく**除外** |
| ACT_1〜ACT_5 の beats が全部17 | 契約帯13–17の上限ちょうど。§2④ |
| L19 が「二つのメーター」で始まらない | §4。**事実の訂正であって、フックを弱めたのではない** |
| 契約 `notes` が `mandatory_stills` を218と書いている | サムネ3枚を外して215になった経緯が `notes` 末尾に記録されている。**実測215が正** |
| 「五回」と「several occasions」が両方出てくる | 判決文が自分と食い違っている（多数意見＝5回・反対意見＝several）。**Court が解決していないので台本も解決しない。**帰属つきでのみ言う |
| 「請求書が誤っていた」と一度も言わない | ⛔-02。**誰も、クラフト家が払う義務を負っていたかを判断していない。**「過大請求された」は使用不可 |
| 「聴聞を経れば止められない」と言わない | ML-76。裁判所は**聴聞のあとに止める権限を電力会社に残した**。ここが本話最大の誤読リスク |
| 票数を出さない | ⛔-01。判決文に票数も Powell への同調者リストも印字されていない |
| クラフト家のその後を語らない | ⛔-05 / ○-01。損害賠償は下級審へ差し戻され、記録はそこで止まっている |
| 台本の反復（`Pay or face termination.` が2回、`several occasions, said the dissent` が2回 等） | §3-5・§5 の掃引結果。**全部わざと** |

---

## 6. 未解決（そちらの判断が要る／私が閉じられなかった）

### 6-1. ~~★ `ML-60` が記録なしで消えている~~ → **解消済み（2026-08-05 実測）**

**現在ディスク上の `script.en.v002.md` L257 に入っている**（`grep -c -i coerce` = **1**）。
> *It refused to let a rulebook override that. A public utility should not be able to coerce a customer to pay a disputed claim.*

本書 v001 が書かれた 19:50 時点の台本には無く、**22:07 の台本修正で復元された**ものと見られる。
`beats.v002.json` の `ACT_4[2]` がこの一文を逐語の quote カードとして担っている（語位置 w158/1076 = 0.147・スロット 0.147 でぴったり乗る）。
**以下は当時の記録として残す。**

台帳 **L161 の `ML-60`** は ✓ VERBATIM の行である：

> *"A public utility should not be able to coerce a customer to pay a disputed claim."*（*Trigg* 引用・判決文 Part III）

これは **v001 の台本 L255 に入っていた**（`grep -i coerce` で1件）。
**v002 では0件。消えている。**そして**どの変更記録にも載っていない** ——
`fact_recheck` §2.1–§2.3 にも、§2.2 の復元表にも、§19 の削除リストにも無い。

**削除の理由は「語数の都合で後回しにした」以上のものが記録に残っていない。**
台本は語数上限 5,600 に対して 5,461 語（`check_script_length` 計測）で、**残りは139語**。
`ML-60` は約16語なので**入る余地はある。**

- これは、台本が保持している `ML-59`（誤れば電力会社が損害賠償責任を負う）の**自然な相方**であり、
  「電力会社は遮断を交渉材料に使ってはならない」と言う唯一のテネシー州法の行である
- **より重要なのは、これが1件見つかったということは `fact_recheck` §2 の変更目録が完全ではないということ。**
  「resolved 8 / restored 5 / removed 8」を**完全な差分として扱ってはならない**

**そちらへの依頼：復元するか、しないと決めて記録するか、どちらかを実行すること。**黙って進めないこと。

### 6-2. 独立再レビューの判定は **DOES NOT MEET THE STANDARD**

`EP64_memphis_REREVIEW.v001.md` の判定。文書自身の集計は **9 PASS / 6 FAIL**（v001 は 4 PASS / 11 FAIL）。
ただし**節見出しを機械的に数えると PASS 8 / FAIL 7**（FAIL = R3・R5・R6・R9・R10・R14・R15）である。
**この食い違いは私が解消していない。**

再レビューが blocking と名指しした5件を、**現在のディスク上の台本で私が実測した結果**：

| # | 項目 | 実測 |
|---|---|---|
| B1 | `Two meters on one wall` | 台本**0件**・beats の HOOK に `ONE WALL` カード**無し** → **解消済み**。最後の生き残り（サムネのタイトル案）は §4 で修正した |
| B2 | `the only two people still in the case` | 台本**0件** → **解消済み** |
| B3 | `It is the one that almost never gets quoted` | 台本**0件** → **解消済み** |
| B4 | 92%線より後ろの初出素材 190語（L397 / L399） | 92%線は現在 **L407（ENDING冒頭）**を通る。**L397 / L399 は線の手前**にある → 名指しされた位置は解消。**ただし ENDING 自体が初出事実を含まないかは私は測っていない** |
| B5 | モチーフ状態8の内容が未定義 | 台本 L431 が内容を明示（状態4の通知であって状態7の書き直し版ではない、と名指し）→ **解消したように見える。**FILM_BIBLE との突き合わせは未実施 |

**つまり再レビュー文書は B1–B3 について一版古い。**判定そのもの（R3・R5・R6・R9・R10・R14 の構造的な指摘）は
**まだ有効**であり、`script_verified` へ上げるにはそこを閉じる必要がある。

### 6-3. R15（音読）が未実施

**誰も声に出して読んでいない。**基準は「R15は省略しない。リズムは黙読では測れない」と定めている。
再レビュー担当も「読んでいないのに読んだ記録は書かない」と明記して FAIL を出した。
**§3-1 の下書き音声を作る工程と兼ねられる。**本番VOの前に一度聴くこと。

### 6-4. 実写プールの目視QCは「コンタクトシート越し」である

`reviewed_by: "claude, read every tile of all 5 sheets"` と記録されている。
**そのシート上では、1080×1920 の縦クリップがガスの火口に見えていた**（全タイルが同じ大きさで描画されるため）。
`scan_video_shape` が後から捕まえたが、**これは「シートは形を映さない」という一般的な欠陥**である。
採用16本を実際にカットへ入れる前に、**動画そのものを1本ずつ再生して確認すること。**

### 6-5. 本監査が裏を取れなかったもの

- **`distinct_video_assets` の 234 という数字の導出根拠**を、私は一次資料で確認していない。契約に書かれている値をそのまま使った
- **`figure_beats_per_act` の 13–17 という帯の根拠**も同様
- ~~ショート `short265` の Payoff 行の `and and` 重複~~（`SHORTS_SLATE_EP62-65.v001.md` L248）→ **本スレッドで修正済み**。ナレーションに乗る行だったため

---

## 7. 本スレッドで実施した監査の結果（要点のみ）

### 7-1. 重複掃引 — **実欠陥0件**

台本398文を機械掃引した。

- **1文の中で4語以上の句が2回**：1件（L255）。**判決文の逐語**（*Trigg* 引用）なので原文どおり
- **40行以内の完全同一文**：**0件**
- 完全同一文（距離無制限）：3件 — L19↔L157（138行）・L93↔L409（316行）・L363↔L411（48行）。**全部わざとの回収**
- 40行以内の5語以上の句の反復：12組。**全部が「逐語引用 → 次の文で鍵語を反響」の型**

**修正なし。**

### 7-2. 引用監査 — **ライブ文書に誤引用0件**

3ファイルから引用断片を**正規表現で機械抽出**した（記憶で選ばない）。

- **一致（語境界完全一致）11件** · **改変5件** · **不一致32件**
- 「改変5件」の内訳：3件は引用ではない（契約の `forbidden_subjects`、台帳の自前の散文）。
  1件は私の正規化による見かけ上のもの（`[T]he` の角括弧）。**1件は意図的な省略** ——
  ML-16 の `…` で番地1019を落としたもので、⛔-08 の裁定どおり
- 「不一致32件」は全て JSON のキー名・契約の禁止事項・ショートの自作フック文。**判決文の引用と称しているものは1件も無い**

**⚠ 構造的な注意：台本は引用符をほとんど使わない。**逐語を地の文として置く書き方なので、
**正規表現による引用抽出だけでは台本は「きれい」に見えてしまう**（実際、台本から抽出できた引用符つき断片は1件だけだった）。
そこで台本398文を1文ずつ判決文と照合し直した：**完全逐語108文・部分一致38文・自前の文143文。**
部分一致38文は全て、①ナレーション用の数字の読み下し（`$35`→`thirty-five dollars`、`$2.50`→`two dollars and fifty cents`、
`33,000`→`thirty-three thousand`、`December 30, 1974`→`the thirtieth of December, 1974`）、
②原典側の角括弧（`[T]he` `[n]one` `[d]ue process`）、③引用符号の除去 —— のいずれかで説明がつく。**捏造なし。**

### 7-3. 既知欠陥文字列の全リポジトリ掃引

`"would retain the option to terminate service after affording the notice and hearing required"`
—— これは **436 U.S. 1 に存在しない**。実際の判決文（`RAW` L93）はこうである：

> And petitioners would retain the option to terminate `*19` service after affording **this opportunity and concluding that the amount billed was justly due.**

（`*19` は星番ページ区切り。n-gram 照合はこれで一度切れるので、**機械照合の際は注意**）

**言い換えの出所も同じ段落にあった。**同じ L93 に *"The utility's interests are not incompatible with
affording **the notice and procedure described above**."* という別の実在の文がある。
欠陥文字列はこれと ML-76 が混線したものと見られる。

**掃引結果：残存コピーは4ファイル9行。全部が「欠陥として記録している」文脈であり、
判決文の言葉として主張しているものは0件。**

| ファイル | 行 | 性格 |
|---|---|---|
| `episodes\_planning\SHORTS_SLATE_EP62-65_QUOTE_AUDIT.v001.md` | L31 / L99 / L103 / L417 | **欠陥を発見した監査文書**。L417 は `ALTERED` と判定済み |
| `episodes\PD-2026-064-memphis\01_research\fact_recheck.v001.md` | L179 / L181 / L186 | 「NOT PRESENT・台本には0件」と記録 |
| `episodes\_planning\EP64_memphis_FILM_BIBLE.v001.md` | L267 | 事故の記録 |
| `episodes\PD-2026-064-memphis\episode_spec.v001.json` | L266 | 契約 `notes` の事故記録 |

**ライブのショート台帳（`SHORTS_SLATE_EP62-65.v001.md` L293）は正しい文字列に修正済み**であることを、
台帳との語境界完全一致で確認した。**台本 v002 にも0件。**

---

## 8. 記録に残っている決定

| 日付 | 決定 |
|---|---|
| 2026-08-04 | **⛔-08 オーナー裁定：名前は可・番地 1019 は不可。**narration・テロップ・プレート・ショートの全部に及ぶ |
| 2026-08-04 | **HOOK は M003 / M048 / M005。**`M001` `M002` `M004` は ACT_1 / ACT_5 の通常カットへ降格。理由＝旧HOOKの「一つの壁に二つのメーター」が事実誤り |
| 2026-08-04 | **HOOKは8秒**（`PD_ONE_PASS_PRODUCTION_SPEC.v2` 行9） |
| 2026-08-04 | **`script_words` を [4400,4900] → [5100,5600] に是正。**実測 wpm（EP60 191.4 / EP61 194.3）が設計値173を否定したため |
| 2026-08-04 | **各話30分。**`manifest.target_duration_minutes: 30` |
| 2026-08-04 | `mandatory_stills` からサムネ3枚（`M208`–`M210`）を除外。後から追加された `M219` も**入れない** |
| 2026-08-04 | **state を `script_verified` → `script_review` へ差し戻し**（`manifest.state_note` に理由あり） |
| 2026-08-04（本書） | サムネのタイトル案 Pair 4A を `Two Meters on One Wall…` → `Two Sets of Meters…` へ修正 |

---

## 9. 検査コマンドまとめ（期待値つき）

```
.venv\Scripts\python.exe scripts\check_episode_spec.py --slug memphis
  → [spec] memphis: valid -- runtime 1620-1920s, script 5100-5600 words, 8 sections,
     beats 13-17/act, 234 distinct video assets, 10 people plates, 215 mandatory still(s),
     9 forbidden subject(s)                                            exit 0

.venv\Scripts\python.exe scripts\check_script_length.py episodes\_planning\EP64_memphis_script.en.v002.md --lo 1620 --hi 1920
  → PASS script_length: 5,461 words (need 3,699-5,480)
     slow 33.4m | median 30.7m | fast 23.0m                            exit 0
     ※ fast 23.0m の RISK 行が出るのが正常。§3-1

.venv\Scripts\python.exe scripts\check_script_craft.py episodes\_planning\EP64_memphis_script.en.v002.md --words 5100 5600
  → PASS every mechanical craft gate is green                          exit 0
     narration 5390 words -> 31.16 min @173.0 wpm
     emotion 0 / AI-smell 0 / spoken CTA 0 / you-your 1.11 / questions 0.00
     short sentences 33.4% (band 20-35%) [133/398]   ← 天井まで1.6pt。§3-6
     longest bare stretch 15.3s / specific 11.39 per min / quarantined 0

# 以下はまだ通らない（入力が無いため。通らないのが現状の正しい姿）
.venv\Scripts\python.exe scripts\check_episode_inputs.py --slug memphis
.venv\Scripts\python.exe scripts\check_spec_satisfied.py --slug memphis      # film.json 生成後
.venv\Scripts\python.exe scripts\check_final_acceptance.py PD-2026-064-memphis --render <mp4> --emit-receipt
```

**受領書が緑になるまで予約も投稿もしない**（`.claude\rules\19-ship-gate.md`）。

---

## 10. figure beats を作り直した（2026-08-05）— v001 は使わない

**正典: `episodes/_planning/EP64_memphis_beats.v002.json`（101個 / HOOK 3・OP 4・ACT_1〜ACT_5 各17・ENDING 9）。**
契約 `figure_beats_per_act` 13–17 を全幕で満たす。`set_figure_beats.py --dry-run` **exit 0（101 beat valid）**。
**`beats.v001.json` は上書きせず残す**（`.claude/rules/05` `12`）。**組み立てでは参照しない。**

### 10-1. なぜ作り直したか（仕組みの話）

`build_case_film_generic.py::build_figures` は beats に時刻を与えない。**区間の中で等間隔に置く**：

```
start = lo + span * (i + 0.5) / N      # N = その区間の beat 数
```

つまり **配列の何番目にあるかが、そのまま画面に出る秒**になる。
v001 は「語りの順番」では正しかったが「語りの**語数の位置**」では合っていない。
台本 v002 のナレーションを区間ごとに語数で実測した（HOOK 24 / OP 59 / ACT_1 686 / ACT_2 1,111 /
ACT_3 697 / ACT_4 1,076 / ACT_5 1,295 / ENDING 440 語）ところ、**素材の密度が前半に極端に偏っていて、
等間隔のスロットとまったく噛み合っていない**ことが分かった。ACT_1 は最初の 28% に9個ぶんの素材が
あり、後半 35%（w447 以降・仕事を休んだ話から提訴まで）にはカードが**1枚しか置かれていなかった**。
その結果、前半のカードは自分の一節より最大 **+0.28 区間ぶん（約66秒）遅れて**出ることになる。

v002 は**全101個を語数位置で置き直し、必要な所ではカードを新設し、余った所では統合した。**

### 10-2. 直した文字列（照合先は `measurements/EP64_memphis_RAW.md` のみ）

RAW は**文の途中に星番ページ（`terminate *19 service`）と脚注番号（`computers,[20]`）が入っている**ので、
照合の前に正規化した。v002 の**引用37本は全数が RAW と逐語一致**（正規化後の完全一致・0 失敗）。

| 場所 | v001（画面に焼かれる予定だった） | v002（RAW 逐語） |
|---|---|---|
| ACT_5 反対意見の譲歩 | "…a legitimate claim of entitlement to continued utility services" で切る | "…continued utility services **as long as the undisputed portions of his utility bills are paid.**"（**条件節を落とすと譲歩の意味が変わる**） |
| ACT_5 n.22 | "The public utility enjoys a broad discretion in the scheduling and structuring of this hearing"（原文の hearing を囲む引用符を削除・**保護条項を切り落とし**） | "…structuring of this "hearing," **provided that the customer is afforded adequate time for effective presentation of his complaint prior to termination.**" |
| ACT_1 n.7 | "…failed to combine the two accounts properly**.**"（原文は `properly (A. 146-150), or that,…` と続く。**途中で切って句点を打ち、完結した文に見せていた**） | 句点を削除（EP62 と同じ家内規則＝途中で切った引用は終止符を打たない） |
| ACT_2 控訴審 | "**The** MLG&W notice only **warned** the customer…"（**原文の編集括弧 `warn[ed]` を黙って解消し、文頭を大文字にしていた**） | "the MLG&W notice only **warn[ed]** the customer to pay or face termination."（原文どおり） |
| ACT_3 出典 | "respondents had not been given adequate notice…" 出典＝**"The District Court's own finding, quoted by the Court"** | **地裁の言葉ではない。**RAW の引用符は次の `"[n]one…"` から始まる。この句は**最高裁自身が地裁を要約した地の文**。→ この位置は `compbars`（0 / 2・ML-48 の後半）に置き換え |
| ACT_4 出典 | "some kind of hearing is required at some time…" 出典＝**"The Court, on what the hearing had to be"** | **_Wolff v. McDonnell_, 418 U. S. 539, 557-558 (1974) の言葉**を最高裁が引用したもの。→ 誤帰属のまま出せないので削除（語位置にも空きが無かった） |
| ACT_4 出典 | Mullane の基準に出典名が無い（"The notice standard the Court applied"） | "**Mullane v. Central Hanover Trust Co., 339 U. S. 306, 314 (1950)** — notice to the beneficiaries of a trust fund, quoted in Craft"（RAW の表記は *Bank &* ではなく *Trust Co.*） |
| ACT_4 出典 | bona fide dispute の例外に出典名が無い（"Tennessee law, as the Court found it"） | "**Trigg v. Middle Tennessee Electric Membership Corp. (Tenn. App. 1975)**, quoted in Craft" |
| ACT_3 出典 | "terminations which should have been unnecessary…" 出典＝"in **the order** ruling for the utility" | 1974年12月30日の**命令**（n. 5）とは別の文書。→ "in **the same decision that gave judgment to the utility**" |

**捏造文字列 `would retain the option to terminate service after affording the notice and hearing required` は
v001 にも v002 にも 0件**（機械掃引で確認）。ACT_5／ENDING が持っているのは RAW L93 の逐語である。

### 10-3. 事実として誤っていた図版（引用ではないもの）

| 場所 | v001 | 直した理由 |
|---|---|---|
| ENDING `casetimeline_c` | 1972→1973→Feb 1974→Dec 1974→1977→1 May 1978 の年表 | **`PD_SCREENPLAY_STANDARD` §12「ENDING は要約ではなく再フレーム」に正面から違反**（出来事の年表は要約そのもの）。**その上で内容も誤り**：第六巡回区の判決は **1976年**（534 F. 2d 684 (1976)）で、1977年2月22日は**上告受理**の日である。→ 削除（年表は ACT_2 に手続きの時計として一つ残る） |
| ACT_3 kinetic | "THE CRAFTS LOST. / THE COURT FOUND / **THE NOTICE INADEQUATE**." | 地裁が認めたのは「**異議を申し立てる手続きについての告知**が不十分だった」ことで、通知そのものではない。反対意見は ✓ *"The District Court did not find that the Division's notice was defective in any respect"*（ML-98）と**明示的に否定**している。→ 削除し、同じ位置を `compbars`（実質的剥奪 0 / 例外として名指しされた者 2・ML-48 逐語）に |
| HOOK lowerthird | "MEMPHIS, TENNESSEE / Alaska Street · 1972" | **HOOK の24語はこれを一言も語らない**（ACT_1 の事実）。フックで本編の事実を先出ししない。しかも §10-6 の罠でどのみち画面に出ない |
| HOOK kinetic | "…AND SAID SHE / HAD PAID **THE** BILL." | 台本 L19 と RAW は ✓ *"explained that she had paid **a** bill"*。定冠詞にすると「どの請求書か」を確定してしまい、**⛔-02（誰も支払義務を判断していない）**の線を越える。→ "HAD PAID **A** BILL." |
| ACT_2 compbars | 「サービス復旧の案内を載せた紙 1 / 異議申立先を載せた紙 0」 | **記録の沈黙からの推論。**n. 4 は cutoff notice が復旧情報を「与える」と書いているだけで、争いについて**書いていないとは言っていない**。しかも第二のフライヤーは実際に異議申立先を書いている。→ 削除 |
| ACT_2 compbars | 「フライヤーを送られた顧客の割合 **40** / この家に届いた保証 **0**」 | **単位の違う二つの数（パーセントと件数）を同じ棒グラフに並べていた。**→ `numberticker` 40 **suffix `%`** 一枚にまとめ、「どちらのフライヤーがアラスカ通りに届いたかは記録が確定していない」をラベルの二文目に |
| ACT_2 numberticker | 40「…the dissent says 30 or 40」 | 数字を 40 に確定しておいてラベルで打ち消す形。→ ticker をやめ、`lowerthird`「PHONE 523-0711 · INFORMATION CENTER」の副文に *"30 or 40 employees"* を原文の幅のまま置いた |
| ACT_2 casetimeline_c | "Day 4 / Day 20 / Day 24" | 原文は全部 ✓ *"Approximately"*。→ "About day 4 / About day 20 / About day 24 / Four days later / About five days on" |
| ACT_4 arrow | "That gets them through the door. **It says nothing yet about what they were owed inside.**" | 二文目は台本に無い。台本 L269 は "That gets the Crafts through the door." の一文のみ。→ arrow ごと削除（語位置に空きが無く、Mullane 逐語を優先） |
| ACT_3 lowerthird | "RECOMMENDED, NOT ORDERED / The utility **rewrote the notice** anyway" | 記録が言うのは ✓ *"instituted some new procedures"*（n. 5）と ✓ *"moved to clarify and regularize their notice procedure"*（n. 16）。→ 台本 L209 の言い方に統一した kinetic「RECOMMENDED. / NOT ORDERED. / THE UTILITY DID IT ANYWAY.」に |
| ACT_5 lowerthird | "JUSTICE STEVENS, DISSENTING / with the Chief Justice and Justice Rehnquist" | 誤りではないが、語位置に単独の枠が取れなかった。→ ML-94 の逐語カードの `attribution` に畳んだ（"Stevens, J., dissenting, joined by the Chief Justice and Justice Rehnquist"）。**情報は一つも落ちていない** |

### 10-4. 数字の裏づけ（台帳の行）

| beat | 数 | 根拠 |
|---|---|---|
| ACT_1 stat | 2（メーターの**組**） | **ML-17 ＋ ML-21**。*"two separate gas and electric meters and only one water meter"* ＋ *"combine the meters into **one gas and one electric meter**"* ＝ ガス2・電気2・水道1。**「二つのメーター」ではなく「二組」**（§4 の訂正どおり） |
| ACT_1 stat | 5（遮断回数） | **ML-23**。ラベルに ML-24（月・期間・季節・金額のいずれも無い）を併記 |
| ACT_2 numberticker | 30（日） | **ML-35**（n. 22・Brief for Petitioners 28） |
| ACT_2 numberticker | 11,216 | **ML-96**（反対意見 n. 1・App. 74） |
| ACT_2 numberticker | 40**%** | **ML-42**（*"about 40% of the utility's customers"*）。**"about" をラベルに残した** |
| ACT_2 / ENDING numberticker | 33,000 | **ML-38**（n. 14・Mullen 証言・App. 130） |
| ACT_2 lowerthird 副文 | 30 or 40 | **ML-97**（反対意見）。**幅のまま** |
| ACT_3 numberticker | $35 | **ML-49** |
| ACT_3 numberticker | $2.50 | **ML-120**（反対意見 n. 5・この文書で唯一の反復する金額） |
| ACT_3 compbars | 3 対 0 | **ML-86 / ML-119** ＋ 台本 L223（地裁・控訴審・最高裁の三つ） |
| ACT_3 compbars | 0 対 2 | **ML-48** 逐語（*"[n]one of the individual plaintiffs… except in the possible instance of Mr. and Mrs. Craft"*） |
| ACT_4 compbars | 1 対 0 | **ML-66** 逐語（告知としては足りるが、異議の機会を知らせるものではない） |
| ACT_5 / ENDING stat | 0 | **ML-84 / ML-86 / ML-91** ＋ 台本 L337–341 |
| ENDING compbars | 2 対 0 | **ML-117**（本文と n. 7 の二つの説明・裁判所はどちらも採らない） |
| ACT_5 引用内 | 約2,000/月 | **ML-107**。数字は**反対意見の逐語カードの中**にあり、独立した ticker にはしていない |

**支えられなかったので落とした数字は1件：ACT_2 の compbars「異議申立先を載せた紙 = 0」**（§10-3）。
これは台帳のどの行でも支えられない**記録の沈黙からの推論**だった。他に台帳の裏づけを欠く数字は無かった。

### 10-5. 並べ替え（語位置で置き直した結果）

丸括弧内は**台本 v002 のナレーション語位置**（区間内の割合）。矢印の右はそのカードが実際に出る割合。

**HOOK**（4 → 3）：v001 は 24語・8秒に4枚＝1枚あたり約1.5秒ずつ重なる。3枚なら重なりは約0.6秒。

```
v001: [場所テロップ] [2通の請求書 stat] [PAY OR FACE] [MARY CRAFT TELEPHONED]
v002: [AI開示 §10-6] [PAY OR FACE (0.25)→0.31] [MARY CRAFT TELEPHONED (0.42)→0.64]
```

**OP**（3 → 4）：59語・約20秒。3枚だと POWELL のカードが「差し戻し」の文に落ちる。4枚で全部が自分の文に乗る。

```
v002: 事件名+引用 (0.00)→0.13 · JUSTICE POWELL (0.37)→0.38 · AFFIRMED/差し戻し (0.47)→0.63 · THREE JUSTICES DISSENTED (0.73)→0.88
```

**ACT_1**（17 → 17・中身は7枚入れ替え）

```
v001 の並び：幕題・アラスカ通り・1972年10月・stat2・売主・一年・1973年・WILLIE S/C・
             ハイライトリング・1973年10月・faultsplit・引用(本文)・引用(脚注)・compbars・
             「記録が一致しない」・stat5・「no satisfaction」
             ← 最初の10枚が語位置 0.02–0.28 に固まり、後半 0.58–1.00 にはカードが1枚しか無い

v002 の並び（右は語位置）：
 0 幕題 (—)                              1 アラスカ通り＋1972年10月＋duplex (0.073)
 2 stat 2（メーターの組・売主の一言を副文に統合）(0.104)
 3 WILLIE S. CRAFT / WILLIE C. CRAFT (0.197)
 4 1973年10月・検針員と自前の業者 (0.280) 5 「自分たちで払った」(0.337)
 6 引用・本文（業者の失敗）(0.362)        7 「脚注の中の第二の説明」(0.442)
 8 引用・n.7（会社の失敗）(0.462)         9 faultsplit (0.532)
10 stat 5 ＋ 月も期間も金額も無い (0.579) 11 「仕事を休んだ」(0.652)
12 引用・good faith の認定 (0.685)        13 引用「was given no satisfaction」(0.781)
14 引用「手続きは十分に説明されなかった」(0.824)
15 引用「権限の不確かな従業員」n.19 (0.892) 16 1974年2月・提訴 (0.968)
```

**新設5枚**（11–15）は、v001 が空にしていた後半 35% を埋めるためのもの。全部が台本の逐語である。
**統合4枚**（売主・一年・1973年・ハイライトリング → 2 と 3 の副文へ）。
**削除**：compbars（ENDING に同じものが残る）・kinetic「THE RECORD DOES NOT AGREE WITH ITSELF」
（同じ位置で `faultsplit` の絵が同じことを言う）。

**ACT_2**（17 → 17）：語位置 0.00–0.09 に4事実、0.40–0.63 に梯子と分割払い、0.70–0.87 にフライヤー2種。

```
 0 幕題  1 「請求書を送っていたのは市だった」(0.038)  2 四段の手続き (0.146)
 3 casetimeline_c・約4日/約20日/約24日/4日後/約5日後 (0.237)  4 引用・段(iii) (0.230)
 5 numberticker 30日 (0.342)  6 numberticker 11,216 (0.392)
 7 PHONE 523-0711（30〜40人・3日止められる）(0.415)  8 「番号は通知に印刷されていた」(0.500)
 9 四つの段（相談員→主任→監督→委員会）(0.518)  10 分割払い制度 (0.576)
11 引用・控訴審「pay or face termination」(0.679)  12 numberticker 40%（＋どちらが届いたか不明）(0.712)
13 引用・第二のフライヤー (0.786)  14 numberticker 33,000 (0.849)
15 「梯子はあった。書かれていなかった」(0.903)  16 適用されなかったテネシー州法 (0.954)
```

**削除**：MLG&W の身元テロップ（1 の主張と重複）・STEP THREE テロップ（4 の逐語と重複）・
stat 2,000（**ACT_5 の反対意見の逐語カードが同じ数字を運ぶ**）・compbars 2件（§10-3）。
**落とした素材**：*"depended on the vagaries of 'word of mouth referral'"*（語位置 0.925 だが
スロットが 0.912 と 0.971 しかなく、0.971 は「適用されなかった州法」が正確に乗る）。ナレーションでは語られる。

**ACT_3**（17 → 17）：v001 の順は語位置とほぼ合っていた区間で、入れ替えは3枚。

```
 0 幕題  1 compbars 0/2 (0.080)  2 引用「hope」(0.146)  3 $35 (0.166–0.229)
 4 引用「不要だったはずの遮断」(0.230)  5 RECOMMENDED / NOT ORDERED / DID IT ANYWAY (0.323)
 6 1974年12月30日の命令 (0.334–0.394)  7 引用・n.8「possible gas overcharges」(0.461)
 8 「POSSIBLE / GAS OVERCHARGES」(0.506)  9 引用・反対意見 n.5「split billing」(0.527)
10 $2.50 (0.581)  11 compbars 3/0 (0.671)  12 引用「損害賠償は下級審の判断事項」(0.699)
13 THE CLASS STAYED DEAD (0.772)  14 第六巡回区の二つの柱＋上告受理 (0.795–0.869)
15 引用「もう聴聞は望んでいない」(0.908)  16 引用「損害賠償請求がムート性から救う」(0.970)
```

**新設4枚**：9（反対意見の split billing・逐語）・15・16（**訴訟が消えかけた区間 0.88–0.97 に v001 は
1枚も置いていなかった**）・6。**削除**：DISTRICT COURT テロップ（ACT_1 末尾の提訴テロップと重複）・
kinetic「THE CRAFTS LOST…」（§10-3）・kinetic「NOBODY EVER DECIDED…」（同じ位置の compbars 3/0 が同じことを言う）。

**ACT_4**（17 → 17）

```
 0 幕題  1 引用・Trigg の例外 (0.075)  2 引用・ML-60「coerce してはならない」(0.147)
 3 NOT AT WILL / ONLY FOR CAUSE (0.201)  4 引用・Mullane (0.282)
 5 「起きると伝えよ / 異議を言えると伝えよ」(0.322)  6 compbars 1/0 (0.337–0.379)
 7 引用・n.15「where, during which hours, and before whom」(0.448)
 8 WHERE. / WHAT HOURS. / BEFORE WHOM.（maskslide・ENDING で回収）(0.472)
 9 A DESIGNATED EMPLOYEE (0.551–0.590)  10 引用「両下級審が認定した」(0.588)
11 引用・Mathews の二要素（生活の必需＋コンピュータ依存）(0.667–0.707)
12 電力会社の最後の主張 (0.743)  13 引用「uniquely final deprivation」(0.792)
14 引用「弁護士を頼むには小さすぎる額」(0.835)  15 ハイライトリング・半額前払い (0.901)
16 THE JUDGMENT … IS AFFIRMED (0.981)
```

**`ML-60` はここで初めてカードになる**（§6-1）。**削除**：TENNESSEE LAW テロップ（語位置 0.015 に
スロットが無い）・「1950年の信託の事件」テロップ（**Mullane カードの attribution に畳んだ**）・
arrow（§10-3）・stat 3（直後の maskslide が三行そのもので同じことを言う）・
引用「some kind of hearing…」（**Wolff の言葉の誤帰属**・§10-2）。

**ACT_5**（17 → 17・**ここが一番動いた**）。v001 は多数意見と反対意見の交替が語位置とずれていた。

```
 0 幕題「RETAIN THE OPTION」(—・0.017 の反響の上に乗る)
 1 stat 0（復旧命令も差止も金も無し）(0.065–0.084)〔多数〕
 2 引用・n.22 broad discretion（**保護条項つき**）(0.132–0.157)〔多数〕
 3 POSSIBLE. / NOT HELD. (0.195)〔多数〕
 4 引用「I have no quarrel…」(0.237)〔反対・書き手の紹介を attribution に統合〕
 5 引用「二つの口座は独立していた」(0.310–0.342)〔反対〕
 6 引用「権限のある職員に会っていた」(0.378)〔反対〕
 7 引用「他方でも払えと言われた … 職員は解決した」(0.426–0.456)〔反対 n.7〕
 8 引用「反対意見は独自の読みを述べる」(0.489)〔**多数** n.19〕
 9 引用「家の持ち主に苦情の言い方を教える必要はない」(0.543)〔反対〕
10 引用「paternalistic predicate」(0.591)〔反対〕
11 SAME BUILDING / SAME STAFF / A DIFFERENT SIGN (0.659)〔反対の帰結〕
12 引用「Lay consumers … should be informed clearly」(0.727)〔**多数** n.15〕
13 引用「約2,000件/月・健康被害の実例は記録に無い」(0.750–0.781)〔反対〕
14 SERIOUS ENOUGH TO SUE OVER, OR TOO SMALL TO BE CONSTITUTIONAL (0.821)〔反対〕
15 引用「政策判断であって憲法解釈ではない」(0.867)〔反対〕
16 引用「弁護士なしで誰もが動けるほど簡単な手続きを憲法は要求しない」(0.967)〔反対〕
```

**話者が入れ替わる 8 と 12 は、どちらも多数意見が反対意見に答える脚注**で、v002 はその2箇所を
カードの側でも守っている（7 反対 → 8 多数 → 9 反対 / 11 反対 → 12 多数 → 13 反対）。
**ACT_5 の逐語「And petitioners would retain the option…」は ENDING へ移した。**理由は §10-6。

**ENDING**（8 → 9・**年表を落として最後の枠を開示カードに明け渡した**）

```
 0 compbars 2/0（誰の過失か）(0.070–0.143)   1 faultsplit（同じ一文の二つの読み）(0.173–0.245)
 2 FIVE TERMINATIONS / SEVERAL OCCASIONS (0.286–0.318)
 3 stat 0（金額を判断した裁判所）(0.350–0.420)  4 numberticker 33,000 (0.505)
 5 WHERE. / WHAT HOURS. / BEFORE WHOM.（ACT_4 の回収）(0.655)
 6 引用「And petitioners would retain the option…」(0.748)  7 gears（時計がまた回る）(0.802–0.868)
 8 AI開示（§10-6 により強制的にここになる）
```

**ENDING に新事実は0件**（`PD_SCREENPLAY_STANDARD` §12）。8枚すべてが本編で既に出た事実で、
**意味だけが変わっている。**削除した年表（§10-3）のほか、テロップ「NOTHING HERE SAYS THE BILL WAS
WRONG」も落とした（内容は 3 の stat 0 と ENDING の地の文が担う）。

### 10-6. 仕掛けの副作用（v001 が踏んでいた罠）

`build_figures` は最後に **`figures[0]` と `figures[-1]` を AI開示の下三分で上書きする**：

```python
if figures:
    figures[0]  = {**figures[0],  **disclosure}
    figures[-1] = {**figures[-1], **disclosure}
```

つまり映画の**最初の1枚と最後の1枚は、何を書いても開示カードになる**。
v001 は HOOK 先頭に「MEMPHIS, TENNESSEE / Alaska Street · 1972」を、ENDING 末尾に
「NOTHING HERE SAYS THE BILL WAS WRONG」を置いていたので、**その2枚は画面に出ないはずだった。**
v002 は両端に開示カードを**明示的に置き**、枠を無駄にしていない。
その代わり ENDING の決め台詞の位置には、**ENDING で二度目に語られる ML-76 の逐語**（6番）を置いた。

### 10-7. 検算コマンド

```
.venv\Scripts\python.exe scripts\set_figure_beats.py --config <filmconfig> --beats episodes\_planning\EP64_memphis_beats.v002.json --min-per-act 13 --dry-run
  → [beats] 101 beat(s) valid: HOOK:3, OP:4, ACT_1:17, ACT_2:17, ACT_3:17, ACT_4:17, ACT_5:17, ENDING:9   exit 0
```

---

*v001 · 2026-08-04 · 設計スレッドから（§10 のみ 2026-08-05 追記）。**この文書に書いていない数字は、私が測っていない数字。***
