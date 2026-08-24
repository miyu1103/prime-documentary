# サムネレーン引き継ぎ — 2026-08-24 深夜（前スレ終了時点）

このレーンの担当は**サムネとタイトルのパッケージングだけ**（CTR最大・目標10〜15%）。
本編制作・レンダ・投稿・カレンダーは別レーン。他レーンのファイルに触らない。

## 現在地（全部完了している）

- **13話×3枚=37枚完成・オーナー承認2回済み**（EP71〜76 / EP77〜82 / EP35）。
  各話 `episodes/<EPID>/09_package/thumbnail.selected.v001.png` 確定済み（EP35のみ v003）。
  02/03は公開時のTest & compare用。承認記録: `episodes/_planning/EP77-82_THUMB_SELECTION.v001.md` 冒頭。
- **EP35（Xc_PxdC_75c）はライブ反映済み**。差し替え前ベースライン = **28日窓 7,436imp / CTR 1.00%**。
  ここがプレミアム版デザインの最初の成績表になる。
- EP71が8/26 16:05から毎日1本、8/31のEP73まで順次公開（メインスレのPD-LongformPushが実施）。
- メインスレへの完了報告: `docs/handover/THUMBNAILS_TO_MAIN_2026-08-24.md`（要点全部入り）。

## スタイルの正典（二重実装禁止）

- `scripts/build_case_thumbnails_from_plates.py` の `style:"winner"` ＝ ライブ最高CTR
  （Sz8zPUoBANM 4.48%）を採寸した様式: 2〜3語縦積み・1語赤・**Anton書体**
  （`assets/fonts/`・OFL同梱）・シネマグレード・文字背後の暗プール＋グロー。
- 文字契約 = `config/thumbnails/<slug>.json`（plate/lines/accent_line/accent_color/side/provenance）。
  **行幅は実質7文字まで**。編集→ `py -3.11 scripts/build_case_thumbnails_from_plates.py --slug <slug>`。
- 近接不合格の救済 = `scripts/thumb_autograde.py`（帯外は書込拒否。明るい画素3%未満だけ再生成）。
- ライブ差し替え = `scripts/set_video_thumbnail.py --video-id X --file Y --apply`（dry-run既定・受領書付き・約50units）。
- **150pxの文字ゲートはwinnerスタイルでは意図的に不適合**（勝者実測94px）。直そうとしない。

## 次にやる仕事（優先順）

1. **実測**: 数日後（8/27〜）に `scripts/yt_studio_video_ctr.py` でEP35のCTRがベースライン1.00%から
   動いたか測る（cookie失効注意 `secrets/studio_cookies.txt`）。公開されたEP71〜も同様に追う。
2. **A/B投入の確認**: 各話公開時にStudio UI「テストして比較」へ01/02/03を入れる
   （API不可・Studio UI自動化はpd-studio-ui-automation参照。実施レーンをメインと要調整）。
3. **EP74の生プレート追加**: itaewonはABが1枚だけ。3枚にするなら生プレート2枚をCodexに発注
   （夜の路地系・文字なし・NEG準拠）。
4. **EP81/82のサムネ文字claims再実行**: station/valdezは照合先recordが0行のままPASSしている
   （台本スタブ）。script_verified後に `check_packaging_claims.py --thumb-text` を再実行。
5. **9/7**: 39本改題実験の判定日。EP35は除外扱い（サムネ差し替えで交絡）。判定後、
   REPACKAGING_WAVE2（上位20本）にwinnerスタイル展開を提案できる。

## 守る制約

公開済み70本は9/7まで改題不可 / タイトル×サムネのペアはオーナー承認ゲート /
文字は合成のみ（生成グリフ禁止）・実在人物肖像禁止 / サムネ文字はタイトルと同じ数字・事実を
言わない（分業） / 全headlineはclaims照合必須。

## 追記 2026-08-24（後続セッション・実測済み）

- **③完了（発注書まで）**: EP74の生プレート2枚の発注書を作成
  `episodes/_planning/THUMBNAIL_ORDERS_2026-08-24/EP74_itaewon_thumbnails.txt`
  （T07=路地の口・大通り越し / T08=電話の画面と手。CTR最優先節＋EP74正典[NEG]同梱、
  `check_image_order_neg.py` PASS）。**Codexの生成待ち**（前バッチ同様、Codexがこの.txtを読む）。
  見出し側の注意: タイトルAと数字重複のため FOUR OF ELEVEN / ELEVEN CALLS は02/03に使えない。
  残る claims済み候補 = 137 OFFICERS / NOBODY ORGANISED IT / NO LAW REQUIRED IT。
- **④は引き続きブロック**: EP81/82 は `01_research/` `03_script/` とも空（実測）。台本完成後に
  `check_packaging_claims.py --thumb-text` 再実行。
- **②の現状**: A/B用途（01/02/03=Test & compare）は `THUMBNAILS_TO_MAIN_2026-08-24.md` に記載済み。
  ただし**どのレーンがStudio UIで投入するかは未決** — EP71公開（8/26 16:05）までにメインと要調整。
- ①CTR実測は8/27以降（変更なし）。

## 前スレの教訓（メモリにも保存済み: retro-thumbnail-lane-20260824）

**ゲート適合≠ベスト。新しい見た目を作る前に、実際に勝った現物を取得して採寸する。**
補正で救える絵に再生成を使わない。宣言したら即着手（無言停止しない）。
削除を含む複合コマンドは全体ブロックされる。JSONはオブジェクトとして編集。
