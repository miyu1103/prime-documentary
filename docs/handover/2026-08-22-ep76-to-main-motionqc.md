# EP76 morandi → メインスレ（組み立て担当）への引き継ぎ【最終版】

2026-08-22 実測。素材レーンはここで作業終了です。**アップロードは一切していません。**
コミット `0b92d617` / `33a3a5a9` / `27ecf4e9`。

---

## 0. 一行で

**素材はすべて揃い、目視QCも全部終わりました。`check_episode_inputs` の残り課題は
Root.tsx の composition 1件だけで、それはそちらが一括で入れる方針のものです。**

```
[inputs] morandi: stills=120 (faces 24) factory=42 motion=120 | narration 329 chunks, 30.7 min
[inputs] morandi: NOT READY -- 1 problem(s):
  - no Remotion composition id starting with Ep76 in Root.tsx
```

---

## 1. **一つだけ確認したいこと（これが唯一の未確定）**

**EP76 の `data/morandi_film.json` を誰が作るのか。**

オーナーからは以前「組み立てはメインの専用スレで実施する」と聞いていました。
一方で今回の連絡は「各スレは film.json を作った時点で slug・composition id・パスを渡して」
と読めます。**まだ film.json は存在しません。**

- そちらが作る → こちらは何もしません。この文書がそのまま入力です。
- こちらが作る → 一声いただければ着手します。Root.tsx には触れません。

---

## 2. i2v は 120/120 完了。ただし **52本は使えません**（残り68本）

指示どおり `qc_motion_clips.py --slug morandi --samples 6 --per-sheet 6` を回し、
**20枚のシートを全部読みました**。警告どおりでした。

| 分類 | 本数 | 中身 |
|---|---|---|
| 湧いた点検者 | 47 | 手が伸びて腐食した鋼線に触る／桁の上を人が歩く／クリップボードを持った女性が現れる |
| 湧いた顔 | 2 | V010（無地の黒からフォトリアルな女性の顔）・V064（カメラ目線の男性） |
| 壊れたクリップ | 2 | V026・V056（黒くなって戻らない） |
| 禁止対象 | 1 | V120（切断された車道に車が走り込む。原寸で確認） |

47本は全部「誰かが見ていた／点検していた」の含意を作ります。この話数が唯一
言ってはいけない「崩落は予見されていた」に直結するため、taste ではなく
`factual_support` として扱いました。

**登録先**: `config/footage_blocklist.v001.json` に `episodes:["morandi"]`。
**`motion/` からファイルは動かしていません。** 実際の読み手で検証済み：
morandi 86 ids / 他の話数 34 のまま / 漏れ 0。
再現用: `scripts/block_morandi_motion_rejects.py`

**再生成はしていません**（EP70で16/16無効の実測、ご指示どおり）。52本は静止画に落ちます。

---

## 3. 実写プールを作り直しました（61 → 29 → **42**）

「確認済み」と記録されていた61本を、クリップの尺全体からサンプルし直して**読めるサイズ**で
見たら 32本が落ちました。**しかもその大半は私が400pxタイルで採用したもの**です。

- `MO-33068304` … タイプライターの紙に**ドイツ語が3行はっきり読める**
- `MO-34964490 / 501` … Shell のロゴ
- `MO-29927991` … クレーンに **EVERGREEN / CMA CGM**
- `MO-29089174` … **アメリカの高速道路**（ボンネット型トラクター）
- `MO-32244801` … 作業員のベストに外国語の文字

その後 prestage を **3ラウンド**（候補116・シート42枚・棚の上で102却下＝1本もコピーせず）
回して14本追加、MO-30911562 を差し替えで除外、**最終42本**。

- 判定: `runs/qc/morandi_clip_verdicts.v001.json`（42 accept / 120 reject・全件理由付き）
- 却下分33本: `remotion/public/morandi/factory_rejected/`（削除していません）
- `check_pool_frames`: **PASS**（42本・273フレーム・binding=exact）

---

## 4. ご指示4件、すべて対応済み

**(a) asset_reuse → 偏差として記録**
`episodes/PD-2026-076-morandi/09_package/release_deviations.v001.json`
実測 162 distinct 対 約266 cut → 約104本が繰り返し。「棚を掘り切った」を数字で残しました
（4ラウンド・候補217・シート77枚、歩留まり 61→29 / 52→10 / 49→3 / 15→2）。
※**レンダー前の記録**である旨と「受領記録ではない」ことを本文に明記してあります。

**(b) AI生成 → 2本ではなく171本、全体ブロック**
最初ファイル名で走査して76本見つけたが、**発端の2本が漏れていました。**
E:にあって `pixabay__357485__id.mp4` という名で、ディスク上にタイトルを持たない。
ラベルは台帳にしかなく、ファイル名走査では原理的に見つからないものでした。
台帳から引き直して171本。`ai-generated-office-clutter-documents-papers` のような、
**書類の検索で普通に出てくるもの**が混ざっています。
既存 film.json 全件と照合して**使用ゼロ**を確認してから global 行にしたので、過去作に
新しい失敗は出ません。実際の読み手で2本ともBLOCKED確認済み。
`scripts/block_ai_generated_shelf_clips.py`（再実行可）。
**ingest側で次の1本を止める仕組みは作っていません＝そちらの担当のままです。**

**(c) 話またぎ → MO-30911562 差し替え、残り2本は記録のみ**
EP60と同じ崩落もので署名的質感が被るのは実害、というご判断に同意。
プールが40本ぴったりになったので第4ラウンドで2本足して42本にしました。

**(d) 52本の再生成 → していません。**

---

## 5. 音は済んでいます

`03_script/script.en.v001.md` に `(SFX:)` **64個**、30:51 に対し **2.07/分**（下限2.0）。
生成: `scripts/write_morandi_sound_plan.py`

他話数と違う点が2つ。**木槌は1つもありません**（イタリアの法廷は使わず
`forbidden_subjects` でも禁止）。**11:36 には何も鳴りません** — 崩落の語彙は NEVER リストで
先に弾いてあるので "deck" や "road" の音が事故に当たることはありません。
あの瞬間は「止まること」で持たせる設計です。

---

## 6. 材料の場所

| もの | 場所 | 数 |
|---|---|---|
| プレート 4K（`img/`に配置済・3840x2160） | `remotion/public/morandi/img/` | 120 |
| プレート原本 | `E:\pd-media\assets\ai\morandi\_v002_4k` | 120 |
| モーション（52本ブロック・使用可68） | `remotion/public/morandi/motion/` | 120 |
| 実写プール | `remotion/public/morandi/factory/` | 42 |
| 却下した実写 | `remotion/public/morandi/factory_rejected/` | 33 |
| 台本＋SFX | `episodes/PD-2026-076-morandi/03_script/script.en.v001.md` | 329 chunks |
| ナレーション | `episodes/PD-2026-076-morandi/06_audio/`（30.7分） | — |
| filmconfig | `episodes/_planning/EP76_morandi_filmconfig.v001.json` | — |
| 事実台帳 | `episodes/_planning/EP76_morandi_FACTS_LEDGER.v001.md` | 171行 |
| 映像設計書 | `episodes/_planning/EP76_morandi_FILM_BIBLE.v001.md` | 14節 |
| 偏差記録 | `episodes/PD-2026-076-morandi/09_package/release_deviations.v001.json` | 3件 |
| プレート判定 | `runs/qc/morandi_plate_verdicts.v001.json`（binding=exact・PASS） | 120 |
| 実写判定 | `runs/qc/morandi_clip_verdicts.v001.json`（binding=exact・PASS） | 162 |
| モーションQCシート | `runs/qc/motion_frames/morandi/` | 20枚 |
| プールQCシート | `runs/qc/pool_frames/morandi/` ＋ `prestage_frames/morandi{,_r3,_r4}/` | 57枚 |

---

## 7. 副産物としてわかった、こちらでは直さなかったこと

1. **staged済みプールの話またぎ監査が存在しません。** content de-dup は
   *新規候補*しか見ません。今回3本とも、チェックではなくステージングのログを
   読んで見つけました。
2. **AI生成の ingest フィルタ**（次の1本を止める仕組み）は未着手＝そちらの担当。
3. **Wanは、人が入りうるプレートには人を描きます。** 特に書類・部屋のレジスターが
   最も被害を受けました（シート14/15/16で18本中13本が全滅）。この作品の主題そのものです。

---

## 8. 正直に、この引き継ぎが保証していないこと

保証できるのは「**シート77枚を全部人の目で読んだ**」ことと「その判断が理由付きで
ファイルに残っている」ことだけです。**残した42本と68本が"良い"ことは保証していません。**

今日**2回**、タイルでの判断が原寸で覆りました（AR-40、および61本中の大半）。
原因は私の注意力ではなく、**400pxのタイルには判断に必要な情報が入っていない**ことです。
プール段階の目視は「候補を絞る」までで、「これで出せる」は言えません。

**出荷可否は実レンダーのコンタクトシートで**、というそちらの指摘はその通りだと思います。
最終カット前に、必ずそちらでも一度目で見てください。
