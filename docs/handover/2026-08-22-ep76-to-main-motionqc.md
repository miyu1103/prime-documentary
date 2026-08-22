# EP76 morandi → メインスレ（組み立て担当）への申し送り

2026-08-22 実測。素材レーンからの報告です。**アップロードは一切していません。**
コミット `0b92d617`。

---

## 1. i2v は 120/120 完了。ただし **52本は使えません**

指示どおり `py -3.11 scripts/qc_motion_clips.py --slug morandi --samples 6 --per-sheet 6` を
回し、**20枚のシートを全部読みました**。警告は正確でした。

| 分類 | 本数 | 中身 |
|---|---|---|
| 湧いた点検者 | 47 | 手が伸びて腐食した鋼線に触る／桁の上を人が歩く／クリップボードを持った女性が現れる |
| 湧いた顔 | 2 | V010（無地の黒からフォトリアルな女性の顔）・V064（カメラ目線の男性） |
| 壊れたクリップ | 2 | V026・V056（黒くなって戻らない） |
| 禁止対象 | 1 | V120（切断された車道に車が走り込む。原寸で確認） |
| **合計** | **52** | 残り **68本が使用可能** |

47本は全部、**「誰かが見ていた／点検していた」の含意**を作ります。この話数が唯一
言ってはいけない「崩落は予見されていた」に直結するので、taste ではなく事実側の問題です。

**登録先**: `config/footage_blocklist.v001.json` に `episodes:["morandi"]` で登録済み。
**`motion/` からファイルは動かしていません**（[1/7]がフレーム連番から作り直し、[2/7]が
アーカイブから再コピーするため）。実際の読み手で検証済み:

```
morandi = 86 ids / oroville = 34 / global = 34 / 漏れ 0
V003.mp4 -> wan_hallucinated_inspector (episode-scoped to morandi)
```

再現用スクリプト: `scripts/block_morandi_motion_rejects.py`

**判断が要るところ**: 52本はプレート静止画に落ちます。EP70の実測で「ネガティブ
プロンプトもシード変更も16/16で失敗」とのことなので、私は再生成を回していません。
再挑戦するかどうかはそちらの判断でお願いします。

---

## 2. 素材プールを作り直しました（61 → 29 → **41**）

`runs/qc/morandi_footage_reviewed.v001.json` に「コンタクトシートで確認済み」と書いてあった
61本を、`check_pool_frames.py` でクリップの尺全体からサンプルし直し、**読めるサイズ**で
21枚読みました。**32本が生き残りませんでした。**

そして、その32本の大半は**私が400pxのタイルで採用したもの**です。悪い順に:

- `MO-33068304` … タイプライターの紙に**ドイツ語の文章が3行はっきり読める**
- `MO-34964490 / 34964501` … Shell のロゴが写る給油所
- `MO-29927991` … クレーンに **EVERGREEN / CMA CGM** が読める
- `MO-29089174` … **アメリカの高速道路**（ボンネット型トラクター）。spec が禁じる register
- `MO-32244801` … 作業員のベストに外国語の文字
- `MO-30850349` … インドの街路（ナンバープレートまで読める）

その後 `prestage_footage_review.py` で**2ラウンド**回しました（候補101本・シート36枚・
棚の上で89本却下＝1本もコピーせず）。**採用は12本だけ**です。棚はこの作品のレジスターでは
ほぼ掘り尽くしています（第3ラウンドは49本中3本）。

- 判定: `runs/qc/morandi_clip_verdicts.v001.json`（41 accept / 119 reject、全部に理由付き）
- 却下した32本は `remotion/public/morandi/factory_rejected/` に退避（削除していません）
- `AR-40` は**タイルで採用 → 原寸で却下**しました（右の商店の看板とすり抜けるバイクで東南アジアと判明）

---

## 3. `check_episode_inputs` は **残り1件**

```
[inputs] morandi: stills=120 (faces 24) factory=41 motion=120 | narration 329 chunks, 30.7 min
[inputs] morandi: NOT READY -- 1 problem(s):
  - no Remotion composition id starting with Ep76 in Root.tsx
```

Root.tsx は**意図的に触っていません**。`data/morandi_film.json` が無い状態で composition を
足すと全話数の Remotion アプリが壊れるためです。そちらの工程でお願いします。

---

## 4. 先に知っておいてほしい3件

**(a) asset_reuse はまだ落ちます。** 41+120 = 161 distinct に対して cut は約266。
約105本が繰り返しになります。棚を掘り切った上での数字なので、**既知の偏差として記録**する
前提で見てください。黙って通すべきではないと思っています。

**(b) AI生成クリップが候補に2本混ざっていました。**
`AR-pixabay_353278`（"ai generated, volcano"）と `AR-v_366249`（"ai generated, rain..."）。
**タイトルに自分で "ai generated" と書いてあるのに機械フィルタが落としていません。**
AI生成は全面禁止のはずなので、これは morandi だけの話ではなく、フィルタ側の穴だと思います。

**(c) 採用済みプールに話またぎの被りが3本あります。**
`MO-30911562`（コンクリート表面）→ EP60 surfside、`MO-27732553`（錆びた門）→ EP66 openfields、
`MO-30117908`（古い書類をめくる手）→ EP54 flowers。
content de-dup は**新しい候補**しか除外しないので、すでに staged 済みのものは素通りします。
特に MO-30911562 は同じ崩落ものの EP60 と被るので、使いどころを避けたほうがいいかもしれません。

---

## 5. 音の手当ては済んでいます

`episodes/PD-2026-076-morandi/03_script/script.en.v001.md` に `(SFX:)` を **64個**書き込み済み。
30:51 に対して **2.07/分**（下限2.0）。生成は `scripts/write_morandi_sound_plan.py`。

2つだけ他話数と違います。**ガベル（木槌）は1つもありません**（イタリアの法廷は使わず、
`forbidden_subjects` でも禁止）。そして **11:36 には何も鳴りません** — 崩落の語彙は NEVER リストで
先に弾いてあるので、"deck" や "road" の音が事故に当たることはありません。あの瞬間は「止まること」で
持たせる設計です。

---

## 6. 材料の場所

| もの | 場所 |
|---|---|
| プレート（4K, 120枚） | `E:\pd-media\assets\ai\morandi\_v002_4k` |
| モーション（120本・うち52本ブロック） | `remotion/public/morandi/motion/` |
| 実写プール（41本） | `remotion/public/morandi/factory/` |
| 却下した実写（32本） | `remotion/public/morandi/factory_rejected/` |
| 台本＋SFX | `episodes/PD-2026-076-morandi/03_script/script.en.v001.md` |
| filmconfig | `episodes/_planning/EP76_morandi_filmconfig.v001.json` |
| 事実台帳 | `episodes/_planning/EP76_morandi_FACTS_LEDGER.v001.md` |
| モーションQCシート | `runs/qc/motion_frames/morandi/` (20枚) |
| プールQCシート | `runs/qc/pool_frames/morandi/` (21枚) ＋ `prestage_frames/morandi{,_r3}/` (36枚) |

---

## 7. 正直に、この報告が保証していないこと

私が保証できるのは「**77枚のシートを全部人の目で読んだ**」ことと「その判断が理由付きで
ファイルに残っている」ことだけです。**採用した41本と68本が"良い"ことは保証していません。**
今日2回、タイルでの判断が原寸で覆りました（AR-40、そして32本のうちの大半）。
最終カットの前に、そちらでも一度目で見てください。
