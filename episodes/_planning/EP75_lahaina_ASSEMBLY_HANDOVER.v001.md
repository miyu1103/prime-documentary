# EP75 · LAHAINA — 組み立てスレへの引き継ぎ v001

**作成 2026-08-22 ／ 直近コミット `a66fa936` ／ branch `claude/vibrant-archimedes-2mmr5h`**

このスレでやったのは **左工程（設計・台本・ナレ・字幕・画像・映像収集）** です。
**組み立て以降は未着手**で、そこからがこの引き継ぎの読み手の担当です。

数字はすべて実測です。推測値は1つも入っていません。

---

## 0. まず3行

- **31:06 の映画。台本・ナレーション・字幕・画像135枚は完成し、全部ディスク上にあります。**
- **残りは「映像810本から使えるものを選んで staging」→「film.json を組む」→「レンダー」だけ。**
- **絵の判定が6枚ぶん手続き上リセットされているので、組み立て前にそこだけ処理が要ります（§5）。**

---

## 1. 完成しているもの — 実測

| 成果物 | 実測値 |
|---|---|
| ナレーション master | **1,857.403 s**、357 chunk、`made=311 skipped=46 failed=0` |
| 完成尺（+ENDCARD 9.0s） | **1,866.4 s = 31:06** — `runtime_seconds [1740,1920]` の中、下126s・上54sの余裕 |
| フック着地 | **20.266 s**（設計は「編集で詰めて0:20」→ **詰め不要**） |
| 台本 | **5,338語 / 357 chunk**、発話221行すべてに台帳の行ID |
| 字幕 | 907キュー、**切れ位置の不良3.5%**（上限5%）、機能語終わり **0**、ナレ逐語一致 5,316語 |
| 画像 | **135枚納品・135枚を3840×2160化・129枚が合格** |
| 映像候補 | **810本 / 14.8 GB**、全部が商用利用可として台帳に記録 |

### 通っているゲート

```
check_design_doc     --slug lahaina    →  75/75 PASS  (exit 0)
check_episode_spec   --slug lahaina    →  valid (episode_spec.v003.json)
check_script_craft   (--wpm 184.1)     →  全項目 green
check_image_order_neg                  →  必須5系統すべて所持
check_prompt_diversity                 →  PASS（重複0・生重複0）
check_packaging_claims (題名+サムネ+説明文) → PASS  unsupported=0
check_plate_delivery                   →  135/135・比率違い0・欠番0
```

---

## 2. 材料の保存先 — これが本体です

### 2.1 設計・台本・契約（すべて git 管理下・リポジトリ内）

```
episodes/_planning/
  EP75_lahaina_FILM_BIBLE.v001.md         設計書（17節・支配的アイデア・5幕・モーション数値）
  EP75_lahaina_script.en.v001.md          台本（発話221行、各行の直下に台帳の行ID）
  EP75_lahaina_FACTS_LEDGER.v001.md       事実台帳 ★拘束
  EP75_lahaina_FACTS_LEDGER.v002.md       事実台帳 追補 ★拘束（v001と併せて有効）
  EP75_lahaina_SCENE_PLAN.v001.md         場面表（§2は実測クロック・§3.0にDL素材の予算）
  EP75_lahaina_PACKAGING.v001.md          題名候補・サムネ・§7=オープニング設計書
  EP75_lahaina_FOOTAGE_PLAN.v001.md       素材計画（棚の実測・§5.4に重要な訂正）
  EP75_lahaina_CODEX_BATCH_A.v001.md      画像発注書 135枚
  EP75_lahaina_thumb_prompts.v001.md      サムネ4案＋実測付きタイトル表
  EP75_lahaina_filmconfig.v001.json       ★組み立ての入口。figure card 83枚・hookSeconds 実測値

episodes/PD-2026-075-lahaina/
  episode_spec.v003.json                  ★機械契約（最新版。v001/v002は残置）
  03_script/script.annotated.v001.json    ★組み立てが必須で読む。8章80span・画面表示
  06_audio/narration_index.v001.json      ★357chunkの時刻表。すべての時刻の出所
  08_edit/captions.final.v001.srt         ★正典の字幕（文法分割版）
  08_edit/captions.mechanical.v001.srt    旧生成器版（不良15.4%）。比較用に残置・使わない
  01_research/fact_recheck.v001.md        ★R3事前検証パケット（§3.1は公開日に再検証）
  09_package/description.draft.v001.txt   説明文 3,567字（ゲート通過済み）
  05_stock/stock_ledger.v001.json         ★映像810本の権利台帳（出典/作者/ライセンス/sha256）

scripts/ae/jobs_ep75_lahaina.json         AEキネティック文字3本＋禁止事項
```

### 2.2 メディア実体（git 管理外）

```
E:\pd-media\assets\ai\lahaina\                    135枚（生・1672×941）
   └ _codex_redo_20260822_02\                     最終の作り直し6枚（取り込み済み）
remotion\public\lahaina\img\                      ★135枚（3840×2160）
remotion\public\lahaina\img_rejected\             却下7枚（削除せず退避）
episodes\PD-2026-075-lahaina\04_scenes\generated_images\   ★129枚 ← 組み立てが読む場所
remotion\public\lahaina\narration.mp3             ★1,857.403 s
E:\pd-media\episodes\PD-2026-075-lahaina\06_voice\master\vc_master_v001.mp3   ナレ原本
E:\pd-media\episodes\PD-2026-075-lahaina\05_stock\candidates\   ★映像810本 14.8GB
remotion\public\lahaina\factory\                  ★空。ここに映像を staging する
runs\qc\lahaina_plate_verdicts.v001.json          ★プレート判定（git管理外）
runs\qc\lahaina_plate_contact_01..06.png          画像の目視シート
runs\qc\lahaina_stock\candidates_footage_contact_01..21.png   映像の目視シート
```

---

## 3. 残作業 — この3つだけ

| # | やること | 目安 |
|---|---|---|
| ① | **絵6枚の判定をやり直す**（§5に手順。中身は確認済み・全部合格相当） | 15分 |
| ② | **映像810本から選んで `factory/` に staging**（40本以上必須） | 2時間 |
| ③ | **film.json を組む → `Ep75Lahaina` を Root.tsx に登録 → preflight 緑 → レンダー** | 半日 |

### 組み立てコマンド

```bash
py -3.11 scripts/build_case_film_assets.py --ep PD-2026-075-lahaina \
    --hookline "Three o'clock on a Tuesday afternoon, on the mountain side of a town on Maui, an engine crew"
```

**このツールが読むもの**（全部そろっています）:
`04_scenes/generated_images/` ・ `06_audio/narration_index.v001.json` ・
`08_edit/captions.final.v001.srt` ・ `03_script/script.annotated.v001.json` ・
`remotion/public/lahaina/factory/` ・ `config/storage.local.json` の media ルート

---

## 4. 先に知らないと詰まること 5つ

**① メディアルートは `E:\pd-media` です。`H:` ではありません。**
`config/storage.local.json` は正しく E: を指していますが、**リポジトリの238本のスクリプトが `H:/pd-media` を直書き**しています。このスレでは `subst H: E:\` を効かせて回避しました。**再起動で消えます。** 解除は `subst H: /D`。

**② ファクトリ棚（中央の素材保管庫）は空です。**
`select_factory_assets.py` は 88,850点と答えますが、それはインデックスで、**実ファイルは0件**です。過去59話に配られたコピー5,806本が `D:\pd-public\<slug>\factory\` に残っていますが、**全部が他話数で使用済み**です。だから今回は**新規ダウンロード810本**を用意しました。詳細は `FOOTAGE_PLAN.v001.md` §5.4。

**③ 組み立ては `04_scenes/generated_images/` から絵を読みます。**
`remotion/public/lahaina/img/` ではありません。却下板をそこに置くと本編に入ります（EP64 memphis の事故）。**現在129枚が置いてあり、却下4枚は入っていません。**

**④ 映像クリップは「1本につき1カットまで」**（再利用0）。
プールが必要数より少ないと、ツールは**繰り返さずに映像カットを減らして絵で埋め**、不足数を警告します。**紙芝居に見えないよう、絵側の深度パララックス（設計書§9で40%以上）を必ず有効にしてください。**

**⑤ `check_script_length` は使わないでください。**
HTMLコメントを発話語数に数えるため、この台本を約1,800語ぶん過大に読みます。尺は `narration_index` が正です。

---

## 5. 組み立て前に必ず通す手続き（絵の判定）

いま `check_episode_inputs` が6件で止まっています。**中身の問題ではなく手続きです。**

```
- H104, H119 が判定後に追加された（未判定）
- H006, H058, H077, H099 が作り直され、sha が変わって判定が無効化
- その4枚がまだ img/ に残っている
```

**6枚とも中身は確認済みで、発注どおりに直っています**（このスレで Codex のコンタクトシートを読んで確認）。特に **H077** は⛔-07（焼けた車両に人がいると示唆しない）に関わる最重要の1枚で、**「ドアが開き、車内が空だと見える」形に直っています。**

手順:

```bash
py -3.11 scripts/check_plate_verdicts.py --slug lahaina --scaffold --reviewer "<担当>"
#   → 6枚が unresolved になる
#   → runs/qc/lahaina_stock/... ではなく、下のシートを見て判定を記録する
#      E:\pd-media\assets\ai\lahaina\_codex_redo_20260822_02\contact_sheet.v003.png
#   → accept にしたら 04_scenes/generated_images/ へコピー
#   → reject が1枚でも img/ に残っていないことを確認
py -3.11 scripts/check_episode_inputs.py --slug lahaina
```

---

## 6. 絶対に破ってはいけない4つ（⛔規則の要）

台帳の ⛔-01〜⛔-18 が全部拘束ですが、**映像・カード・サムネで破りやすいのはこの4つ**です。

1. **「サイレンが鳴っていれば結果は変わった」を、どの形でも言わない。**
   84の所見のどれもそう言っていません。**唯一許される形は否定文**で、台本の ENDING にあります。
2. **Finding 37（焼失範囲内で作動可能なサイレンは1基）と「鳴らされなかった」を同じカードに載せない。**
   別々の出典の別々の事実です。混ぜると誰も言っていない第3の主張になります。
3. **サイレンが「故障した／失敗した」と書かない。** どの出典も言っていません。
4. **14:17（鎮火報告）と14:55（再燃）の38分を、非難として置かない。**
   郡の「消防は十分以上の注意を払った」と所見67（通常気象で有効な残火処理が、あの日の気象では不十分だった）と**同じ場面に必ず一緒に置く**。

**⛔-07：犠牲者は名指しも描写もしない。中に人がいると示唆する焼けた車両も不可。**

---

## 7. 公開前に必ず再検証すること

**和解の状況は、この映画が公開される月に動きます。**

2026-08-21 時点：**支払いは1件も行われていません。** 弁護士費用をめぐる控訴が 2026-08-05 にハワイ最高裁へ上がり、係争中は支払い不可。9月にも判断が出る見込みです。

台本は **「2026年8月時点で」と声に出して言う**形にしてあるので、判断が出ても**古くなるだけで嘘にはなりません。** ただし `fact_recheck.v001.md` §3.1 の指示どおり、**パッケージングを書く日**と**予約投稿する日**に再検証してください。

---

## 8. パッケージング（決定済み・実測付き）

| | |
|---|---|
| **推奨タイトル** | `Hawaii Built the World's Largest Warning Siren Network. It Had Never Been Used for a Fire.`（90字・**PASS unsupported=0・soft note 0**） |
| A/B の相手 | `The Evacuation Order Was Sent to Cellphones. Lahaina's Cell Service Had Died That Morning.` |
| **サムネ** | **T2「NEVER USED / FOR FIRE」**（サイレンの筒を大きく）と **T4「SENT TO / DEAD PHONES」** の2案。詳細は `thumb_prompts.v001.md` |
| 説明文 | `09_package/description.draft.v001.txt`（3,567字・ゲート通過） |

**注意：** `T1「ONE SIREN」` は単独だと不完全な主張なので、**「inside the burn perimeter」を含むタイトルとだけ**組めます。
**注意：** 説明文で消防局を正式名称（`County of Maui Department of Fire and Public Safety`）に戻さないでください。`Public Safety` が所見30の否定文と衝突して**偽の CONTRADICTED で出荷が止まります。** `Maui Fire Department` を使ってください。

---

## 9. このスレで直した道具（組み立てでも使います）

| ツール | 何をした |
|---|---|
| `scripts/check_plate_delivery.py` | 新規。未着・比率違い・解像度不足・余計なファイルを1発で出す |
| `scripts/export_codex_batch_paste.py` | 新規。発注書→貼り付け用に分割。`--outstanding` で未完了分だけ自動再発注（判定の却下も拾う） |
| `scripts/build_annotated_script_lahaina.py` | 新規。annotated script をナレ索引＋figure card から生成 |
| `scripts/upscale_oroville_4k_esrgan_v001.py` | **汎用化**（`--slug/--src/--dst/--skip-wrong-aspect`）。既定はEP71のまま |
| `scripts/check_prompt_diversity.py` | 表形式を読めるよう修正＋**生トークン比較を追加**（同一プロンプト30枚がPASSしていた） |
| `scripts/build_footage_contact_sheet.py` | cp932 クラッシュを修正（真の診断が隠れていた） |
| `scripts/build_motion_from_plates.py` | spec を最新版で解決するよう修正（v002 を黙って無視していた） |
| `scripts/fetch_stock_lahaina_batch.sh` / `_batch2.sh` | 映像取得。2回目は1回目の目視結果から検索語を絞ってある |

---

## 10. 機械が測れないこと — 人が見るしかない

`check_design_doc` が自分で「これは判定しない」と列挙している8項目のうち、この映画を決めるのは3つです。

1. **フックが結末を隠せているか**（0:00〜0:20で結果を言っていないか）
2. **文章がAI臭くないか**
3. **素材がラベルどおりか** ← **今回はここが最大の穴**。ファクトリ棚の台帳が失われており、
   ダウンロードした810本もファイル名がIDだけです。**コンタクトシートを人が見る以外に方法がありません。**

このスレで **画像135枚は全部目視し、4枚を却下**しました（記録は `runs/qc/lahaina_plate_verdicts.v001.json`）。
**映像810本のうち、最初の413本は目視済み**で、歩留まりは Pexels 約45% / Pixabay 約20%。
**残り約400本（2回目の取得分）は未目視**です。組み立てスレで見てください。

**目視の結論（1回目）:** 人・オフィス・書類を検索語にすると、顔が写った企業ストックや画面に文字のあるものしか返りません。**その領域は129枚の絵が担当**します。当たった検索語は、乾いた草・山火事の煙・焼け跡・嵐の雲・路面・金網と有刺鉄線・鉄塔と電柱・熾火・水道管・廊下でした。
