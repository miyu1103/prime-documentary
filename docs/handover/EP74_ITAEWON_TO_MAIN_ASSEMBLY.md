# EP74 itaewon → メインスレ（組み立て担当）  2026-08-23

**この話数はレンダー待ちです。**そちらの手番は Root.tsx の登録から。EP74スレは閉じます。

---

## 1. お願いした3点（そちらの指示どおりの形で）

| | 値 |
|---|---|
| slug | `itaewon` |
| composition id | `Ep74Itaewon` |
| film.json | `remotion/src/data/itaewon_film.json` |

`Root.tsx` と `compositions/Ep74ItaewonFilm.tsx` は**触っていません**。GPU にも触れていません。
i2v は使っていません（そちらの「不要」判断のとおり、全カットが実素材と生成プレートです）。

登録後に必要なのは1コマンドだけです。

```bash
py -3.11 scripts/check_episode_inputs.py --slug itaewon   # 今 NOT READY の理由は Root.tsx の1件のみ
```

---

## 2. いま緑になっているもの（すべて実測値）

```
film.json      cuts 372 / 5.07 秒per cut / distinct_ratio 1.0 / max_reuse 1 / figures 83
尺             1,895.8 秒 = 31分36秒（宣言帯 1,740–1,920 秒の内側）
素材            factory 253 / stills 92 / people 28 / overlay 4
字幕            554キュー・ナレ一致 PASS・行長 PASS（medium.en 強制アライン）
音              69キュー / 2.192 per 分（下限2.0）/ 環境音7種（下限4）/ coverage 1.0 / unmapped 0
episode_spec   valid（v001）
pool_frame_review  binding=exact・257本すべてに判定あり
```

**目視QCは全数やりました。**826本を1本あたり6コマ、8本1枚で **104枚**のシートにして、
1枚ずつ開いて読みました。採用257本。

---

## 3. 判断1（2語クエリで引き直す）の結果 — そちらの判断は数字で正しかったです

| | クエリ | 追加 | 採用 | 採用率 |
|---|---|---|---|---|
| 第2波 | 2語 × 139本 | 501 | 169 | **34%** |
| 第1波 | 1語・長句 | 325 | 88 | 27% |

前回お伝えした「22%」は3枚のサンプルからの推定で、**全41枚を読んだら27%**でした。訂正します。

却下の中身（多い順）：**読める顔**（ストック俳優／祭りの群衆まるごと）→ **国違い**（NY・ロンドン・パリ・
ワルシャワ・ダッカ・LA など11都市と固有ランドマーク）→ **CG/AI**（3Dパトカー・CGの月・シンセウェイブ）→
**意味が無い**（ボケ・煙・フレア）→ **露出破綻**（真っ黒・白飛び・途中で露出が飛ぶ）→ **途中でカットが変わる**
（複数ショットの寄せ集めが1ファイルになっている）。

---

## 4. そちらに報告すべき発見（次の話数に効くもの）

### ① 北朝鮮の国旗が2本、韓国の話数に入っていました

`AR-v_132352` と `AR-v_24681`。棚のラベルはどちらも `korea flag` で、**機械では区別できません**。
目視で落としました。次に韓国題材をやるときは `forbidden_subjects` に「北朝鮮」側の語が要ります。

### ② AI判定の穴：pixabay の「アンビエンス・ループ」カテゴリ

`block_ai_generated_shelf_clips` は**タイトルに `ai generated` と書いてある棚の793本**を弾きます。
実測：**そのうち0本がこのプールに来ていました＝この防御は効いています。**

穴はその隣です。`dark room rain loop environment ambience` / `rain sounds fireplace sounds` /
`night harbor moon silhouette`（クレーンほどの大きさの月）— **CGなのにタイトルがそう言わない**。
13本入っていました。`wallpaper` `seamless loop` `rain sounds` `fireplace` など10語を
EP74の `forbidden_subjects` に足して機械で除去済みです。**汎用ルールにするかはそちらの判断です。**

### ③ 縦動画20本は機械で除去しました

`stage_footage_by_title` は第1波の時点で形状フィルタを持っていませんでした（現在は入っています）。
20本を `factory_rejected_shape/` へ退避。**EP72/73スレの縦動画の件と同じ根です。**

### ④ episode_spec の v002/v003 はパイプラインから見えていませんでした

実測：`scripts/` の **47本が `episode_spec.v001.json` を名指しで開き**、v002 は4本、glob は4本。
つまり **v001 が機械契約**で、隣に置いた v002/v003 はほとんどのツールに読まれません。
その結果 `build_asset_manifest_motionfirst` が **people=0** と報告しました。顔プレート28枚は
ディスクにあったのに、です。v001 に統合し、v002/v003 は `_superseded_specs/` に測定値付きで移しました。

---

## 5. 既知の逸脱 1件（隠していません）

```
check_spec_satisfied: distinct_video_assets
  実測 253 本 / 宣言 265 本 → 12本不足
```

ただし**同じ検査が「0カットも素材を再使用していない」と出しています**（`max_reuse 1`,
`distinct_ratio 1.0`）。この数字は「同じクリップを何度も切る」のを防ぐためのもので、
その目的は満たされています。1カット5.07秒も上限6.0秒の内側です。

`config/ship_policy.v001.json` の止める4クラス（実在人物・権利・事実・偽造記録）には当たりません。
**出すなら `release_deviations.v001.json` に記録、埋めるならもう1周クエリ**、どちらもそちらの判断です。
埋める場合は却下542本のうち「国違い」で落とした夜景空撮が候補で、質は下がります。

---

## 6. 材料の置き場所（全部）

```
film.json ........... remotion/src/data/itaewon_film.json
filmconfig .......... episodes/_planning/EP74_itaewon_filmconfig.v001.json
  （作り直すなら  py -3.11 scripts/build_ep74_itaewon_filmconfig.py）
機械契約 ............ episodes/PD-2026-074-itaewon/episode_spec.v001.json
アセット目録 ........ episodes/PD-2026-074-itaewon/05_visuals/asset_manifest.v001.json
クリップQC .......... episodes/PD-2026-074-itaewon/05_visuals/factory_clip_qc.v001.json
目視判定（正典） .... runs/qc/itaewon_clip_verdicts.v001.json   ← runs/ はgit管理外。ローカルにのみ実在
  判定の生ログ ...... runs/qc/_ep74_verdicts_r1.txt / _ep74_verdicts_r2.txt
  読んだシート ...... runs/qc/pool_frames/itaewon/dense/  （104枚）
素材（採用257本） ... remotion/public/itaewon/factory/
  却下の退避先 ...... remotion/public/itaewon/factory_rejected_review/  （542本）
                      remotion/public/itaewon/factory_rejected_shape/   （縦20本）
                      remotion/public/itaewon/factory_rejected_r2/      （ループ13本）
画像プレート ........ remotion/public/itaewon/img/  （I001–I120、うち顔28枚）
ナレ音声 ............ remotion/public/itaewon/narration.mp3
ナレ索引 ............ episodes/PD-2026-074-itaewon/06_audio/narration_index.v001.json  （343チャンク）
字幕（正典名） ...... episodes/PD-2026-074-itaewon/08_edit/captions.final.v001.srt
  ツールの生出力 .... episodes/PD-2026-074-itaewon/08_edit/captions.v002.srt
音のルール .......... config/sound_rules/itaewon.json
台本 ................ episodes/_planning/EP74_itaewon_script.en.v007.md（5,464語）
事実台帳 ............ episodes/_planning/EP74_itaewon_FACTS_LEDGER.v005.md（94行・11 ABSENCE）
映像バイブル ........ episodes/_planning/EP74_itaewon_FILM_BIBLE.v002.md
サムネ案 ............ episodes/_planning/EP74_itaewon_thumb_prompts.v002.md
```

---

## 7. 切るときに気をつけてほしい3本（判定ファイルにも記録済み）

R3（実在の死者159名）なので、**丸ごと切らないでください**。

| クリップ | 条件 |
|---|---|
| `AR-27856` | 1コマ目と3コマ目が真っ黒。**明るい中盤だけ**使う |
| `AR-pexels_15201563` | 末尾がカーテンに切り替わる。**尻を切る** |
| `AR-v_24603` | プール内で最も密度の高い群衆。ただし**中盤に読める顔が1コマある**。ブレている区間のみ |

図版（figures）側の縛りも2つ入れてあります。`_figure_sources._readme` に理由を書きました。

- **ACT_4 の「WHAT THIS FILM DOES NOT SAY」と「'WOULD HAVE'」を外さないでください。**
  外すと 137人 vs 10万人 のカードが、記録が支持していない告発として読めてしまいます。
- **ACT_5 の「APPEALS PENDING」と「SUSPENDED, NOT DECIDED」も同様。**
  Lee Im-jae らは存命で、控訴は**中断であって未決**です。有罪を出したカードの直後に必ず置いています。

---

## 8. 音について（前回の1920年代の件・解決済み）

HOOK に禁酒法時代の道路音が入っていた件は直しました。原因は、キーワードに当たらない章が
`AMBIENCE_KEYWORDS` の**先頭**に落ちる仕様で、かつ `CHAPTER_AMBIENCE_DEFAULT` が別の話数の章名
（`opening`, `act1`）で書かれていたため、EP74の8章中6章に既定値が無かったことです。

`config/sound_rules/<slug>.json` に `{"ambience": "<章id>", "bed": "<amb_*.mp3>"}` を書けば
キーワードより先に効く仕組みを足しました（既存の話数の挙動は変わりません）。EP74は8章とも宣言済みです。

**密度ゲートはこれを検出できません。**「異なるベッドが4種類以上」しか数えないので、
7種類が全部間違っていても緑になります。耳でしか分かりません。

あわせて、退役した専用スクリプトにあった「**27ビートを名指しで無音**」が移設で落ちていたので、
`write_sound_plan.py` に `silent` 行の仕組みとして戻しました。死者数や "crushed to death" の上に
ワンショットの効果音が乗ると、この作品が絵で禁じたものを音で演出することになるためです。

---

## 9. コミットについて（申し送り）

**EP74のファイルが、また別セッションのコミットに巻き込まれました**（`8a520a46 ADR-0011: After Effects...`）。
中身は全部入っています（`git ls-files` で7つの主要成果物すべて追跡確認済み）。
push 済みの共有ブランチを書き換えるほうが危険なので、**履歴は直さず記録だけ**残します。
同じことが起きるのは2回目です。`git add -A` を打つスレが複数あるのが原因です。
