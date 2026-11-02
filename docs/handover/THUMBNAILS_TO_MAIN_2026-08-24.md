# Thumbnail lane → Main thread, 2026-08-24 深夜

**EP71〜76、全部納品済み。ついでにEP77〜82とEP35も同じ水準に刷新した。**
オーナー承認2回取得済み（初版セット＋プレミアム版。記録は
`episodes/_planning/EP77-82_THUMB_SELECTION.v001.md` 冒頭）。以下、そちらが知るべきことだけ。

## 納品物

- 全13話 × `episodes/<EPID>/09_package/thumbnail.selected.v001.png`（EP35のみ `v003`。
  v001/v002は既存の不変リビジョン）。EP71〜76はそちらの指示どおり placeholder を上書きした。
- 各話 `thumbnail.<slug>.01/02/03.v001.png` = 公開時の Test & compare 用3枚
  （01が本命=selectedと同一。**EP74だけ1枚** — 生プレートが `T01_bg.v002.png` の1枚しか
  なく、他8枚は旧文字焼き込みで再利用不可。ABを3枚にしたければ生プレート2枚の追加発注が要る）。
- **EP35はライブ反映済み**（`thumbnails.set` HTTP 200 ×2回、受領書
  `episodes/_planning/thumbnail_set_receipt.Xc_PxdC_75c.*.json`）。差し替え前ベースライン =
  28日窓 7,436imp / CTR 1.00%。効果測定はここから。

## スタイルの正体（再現方法）

`build_case_thumbnails_from_plates.py` の `style: "winner"`。ライブ最高CTR
（Sz8zPUoBANM、4.48%）を採寸して作った: 2〜3語縦積み・1語だけ赤・Anton書体
（`assets/fonts/`、SIL OFLライセンス同梱）・シネマグレード（影=青緑/光=暖色＋ビネット）・
文字背後の暗プール＋差し色グロー。契約は `config/thumbnails/<slug>.json`
（lines / accent_line / accent_color / side）。**編集→ `--slug` で再ビルド→公開後でも
`scripts/set_video_thumbnail.py --video-id X --file Y --apply`（汎用・dry-run既定・受領書付き）**。

## そちらの2つの注意書きへの返答

1. **150px文字ゲートは意図的に満たしていない。** ライブ勝者の実測は文字高さ約94px。
   winner行のゲートFAILは仕様（スクリプトがその旨を出力する）。「直そう」としないこと。
2. bright-core問題は暗プールとストロークで回避済み。白空プレート（lahaina）も確認済み。

## 文字の事実照合

全headline `check_packaging_claims.py` PASS。ただし**EP81 station / EP82 valdez は照合先
record が0行**（台本スタブ）— script_verified 後に再実行が必須。新規に検証した主張:
NO ONE ABOARD（lacmegantic）/ 3.2 METRES（itaewon）。

## タイトル（オーナー経由で意見済みだが要点だけ）

6本の方向は正しい。ただし **EP74の54字はレーン実測の負け帯**（勝ちタイトルは全部59〜100字、
≤60字時代の実測CTR 1.38%）。第1文を残して2文目に「Eleven Calls」を足す案を出した。
EP72は「7 vs 9」だけだと初見に賭け金が伝わらない（死者数か町の炎上を2文目に）。
採否はそちらの判断でいい。**サムネ文字はタイトルと同じ数字を言わない設計にしてある**
（uri=$9,000 / morandi=98%）。タイトルを変えるならこの分業が崩れないかだけ見てほしい。

## 帳簿

コミット: 3d65c19f 〜 52e44dac（本レーン分のみ、他レーンのファイルは触っていない）。
画像本体はrepo内 `09_package/`・`10_thumbnail/`、選定過程の生プレートはE:\pd-media。
