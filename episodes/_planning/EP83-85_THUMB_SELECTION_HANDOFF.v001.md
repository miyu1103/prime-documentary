# EP83–85 サムネ選定スレ 引き継ぎプロンプト v001（2026-08-25）

下の枠内をそのまま新スレに貼る。

---

EP83-85のサムネ選定を担当します。着手前に `git pull`。

## 現在地（実測・2026-08-25時点）

- 題材は確定: **EP83=Boeing 737 MAX / EP84=Three Mile Island / EP85=Katrina堤防決壊**
  （正典 `episodes/_planning/EP83-85_SLATE.v004.md`・APPROVED）。
- 生プレート **30枚納品済み・29枚合格**（`episodes/<EPID>/10_thumbnail/T01–T10.png`・全て3840×2160）。
  不合格1枚 = **EP85 T06（5枚コラージュで出力）**。再生成発注書は
  `episodes/_planning/THUMBNAIL_ORDERS_2026-08-25/EP85_T06_REDO.txt`（未実行・A/B枠外なので急がない）。
- **A/B候補9枚が合成済み**（各話3枚）: `episodes/<EPID>/09_package/thumbnail.<slug>.01–03.v001.png`
  - EP83 `max737`: 01=T01 コックピット「WHO IS FLYING?」/ 02=T02 トリムホイール「IT PUSHED BACK.」/
    03=T10 レコーダー「IT WAS ALL THERE.」
  - EP84 `threemile`: 01=T01 警報の壁「IT BEGAN AT 4 A.M.」/ 02=T02 赤タイル「NO LIGHT.」/
    03=T07 避難の車列「STAY OR GO?」
  - EP85 `katrina`: 01=T02 破られた壁「BELOW DESIGN.」/ 02=T09 越流「NOT THE STORM.」/
    03=T04 水没バス「THEY NEVER MOVED.」
- 文字契約は `config/thumbnails/{max737,threemile,katrina}.json`（style:"winner"）。
  再ビルドは `py -3.11 scripts/build_case_thumbnails_from_plates.py --slug <slug>`。
- **オーナー目視済み・9枚とも合格（2026-08-25「全部良かった」）。selected は未確定＝このスレの仕事。**
- QC全記録 = `episodes/_planning/EP83-85_THUMB_QC.v001.md`。
  文字設計の全候補（差し替え用の予備見出し込み）= `EP83-85_THUMB_TEXT.v001.md`。

## このスレでやること

1. 9枚を **320px相当**で見比べ、各話1枚を選ぶ（オーナー決定。Claudeは推しを言ってよいが決めない）。
   Claudeの推し（拘束しない）: EP83=03 / EP84=01 / EP85=03。
2. 選定後: `09_package/thumbnail.selected.v001.png` へコピー（**上書きせず新規**）。
3. 残る2枚は公開時の Test & compare（Studio UIのA/B）に回す。API不可・Studio UI自動化は
   メモリ `pd-studio-ui-automation` 参照。
4. **文字の最終確定は台本後**。数字入り見出し（IT BEGAN AT 4 A.M. / BELOW DESIGN /
   THEY NEVER MOVED）は claims 未照合の○。台本完成後に
   `py -3.11 scripts/check_packaging_claims.py --slug <slug> --title "<title>" --thumb-text "<text>"`
   を通し、落ちたら THUMB_TEXT.v001 の「断定なし」見出しへ差し替えて再ビルド。

## 絶対に触らない・変えないこと

- **`check_thumb_subject_luma` のFAILを直そうとしない。** 9枚中8枚がFAILだが、これは既知かつ意図的
  （文字150px床と輝度60床は winnerスタイルと矛盾。ライブ最高CTR 4.48%のサムネ自身が通らない）。
  緑にするために明るく・大きくすると、実測で負けている見た目に戻る。
- タイトルとサムネ文字で同じ数字・事実を言わない（分業）。タイトル正典 = `EP83-85_TITLES.v004.md`。
- 実在人物の肖像禁止。**EP85は顔そのものが禁止**（プレートも顔なしで発注済み）。
- 生成グリフ禁止（文字は必ずRemotion/ビルダーで合成）。
- 本編制作・台本・レンダ・投稿は別レーン。そちらのファイルに触らない。

---

以上。
