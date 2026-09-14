# 他スレに貼る文章

> 下をそのままコピーして、別スレの最初のメッセージに貼る。
> 長い版が要るときだけ `docs/PD_ARCHIVE_SHELF_WORKLOG.v001.md` を読ませる。

---

## 短い版（普段はこれで足りる）

```
素材棚を 2026-08-10 に全面点検した。着手前に docs/PD_CANON.md の §10「素材棚」を読んで。
根拠と罠の全部は docs/PD_ARCHIVE_SHELF_WORKLOG.v001.md にある。

いちばん効くのは3つ:

1. ショットは「監督の言葉」でなく「素材提供者が付ける題名の語彙」で書く。
   police interview room → 0件 / interrogation room detective → 12件
   handcuffs on wrists   → 0件 / person in handcuffs        → 16件
   カバレッジが 85/50/90% → 100/90/100% に上がったのは、棚が増えたからではなく書き方を直したから。
   0件が返ったら --weak-ok --sheet を付けて必ず目で見る（本命が埋まっていた率 12/13）。

2. 棚を数えるコードを書くなら from shelf import shelf_rows を使う。自前で glob("*.jsonl") しない。
   3ツールが各自の定義を持って3つとも壊れていた（削除記録64,640行を在庫に加算して
   197,712点と報告 / ukna の22,348行を在庫と誤報。全部 file_path: null で1本もDLしていない）。

3. 台帳の行を消さない。47%は削除の記録で、消すと取り込みが同じものを取り直す
   （住所録46,707枚が実際に戻ってきた）。削除は absent_index.json が別管理している。
```

---

## 組み立て・レンダー担当スレに貼る版

```
素材棚スレから申し送り。2026-08-10 に棚を全面点検した（docs/PD_ARCHIVE_SHELF_WORKLOG.v001.md）。
そちらの工程に直接効くものだけ:

■ 出荷ゲートは素材の解像度を見ていない
check_final_acceptance.py は完成尺だけを >=1920x1080 で測る。素材側は誰も測っていない。
640x480 の記録映像を1080pのタイムラインに引き伸ばして並べた作品はゲートを通る。

全31,107本の実測索引を作った。(source:id) で引ける:
  R = json.load(open(r"H:\pd-media\assets\archive\_ledger\video_resolution.json", encoding="utf-8"))
  wh = R.get(f"{source}:{item_id}")   # {"w":1920,"h":1080} or None

危ないのは100%SDのテーマではなく、2割だけ混ざるテーマ:
  courtroom_justice 17% / prison_jail 19%   ← 8割HDの中に紛れるので気づかない
  nara 89% / ia 73%、ストック系(pexels/pixabay/mixkit/nasa/coverr)はほぼ0%
  vintage_ads_cartoons と factory_manufacturing は100%なので、むしろ安全（必ずSDと分かって使う）

■ 判定 unusable の theme×source を使わない
_qc/archive_verdicts.jsonl に212組の判定がある（good 103 / mixed 60 / unusable 49）。
search_archive.py 経由で選んだものは自動で外れる。台帳を直接舐めて選ぶコードは危ない。

■ ショット記述の語彙
そちらで shot spec を書くなら、監督の言葉でなく素材の題名の語彙で書く。
書き換え表は config/shot_coverage_shots.v002.json の rephrased_from_v001 にある。

■ factory 棚のファイル名は直った（フォルダは未修正）
88,740点すべてを提供元の実題名にリネーム済み。
  AF-BG-0001__dark_cinematic_background.jpg -> pexels__9665187__white-dust-particles-on-black-background.jpg
旧名はダウンロードに使った検索語であって中身ではなかった。
ただしテーマフォルダの割り当ては直っていないので、目視QCは今も必要。
```

---

## 素材を追加で集めるスレに貼る版

```
素材棚スレから申し送り。取り込みレーンは ia 以外すべて枯渇して正常終了した
（gov / sci / web_video / web_audio が最終ランで0件）。増やすには新クエリか新ソースが要る。

■ 取り込み側のゲート（4レーン共通・すでに入っている）
  1. オーナー判定 unusable の theme×source は取らない（_qc/archive_verdicts.jsonl を読む）
  2. 議事録画は取らない（市議会・公聴会・説教。purge_meeting_recordings.py と語彙を共有）
  3. ban-risk / 肖像 / AI生成 / 医療デマ は quarantine_ban_risk.py で隔離

■ 技術基準を上げないこと
記録系の480p未満は削除でなく隔離する設計。代替不能な記録映像に削除経路を作ると、
過去に帯（band）で書いてニュルンベルク／マウトハウゼンのリールを7本破壊した。
480〜719p を通すのは設計通り。必要なのは基準を上げることでなく見えるようにすること。

■ 新しいソースを足すときに必ず測ること
  - キーワード衝突: bench→公園のベンチ / press→干し草ベーラー / seal→アシカ /
    London→オハイオ州ロンドン / glacier→ISSの冷凍実験装置 / harbor→フライデーハーバーの地方紙
    タグ羅列型のソース(pixabay/pexels)は特に危ない
  - 「絵として使えない」形式: 2時間の議事録画は関連度も技術基準もライセンスも全部通る
  - 解像度: 台帳に幅・高さを書くこと。書いてなければ誰も4Kと320x240を区別できない

■ レーンの起動と生存確認
  powershell -File scripts\launch_ingest_lanes.ps1 ia sci      # 空白区切り。カンマも可
  生存確認は PID + CPU増分。Name='python.exe' だけを見ると python3.11.exe を見落とす。
  Win32_Process の CommandLine で検索するときは、その検索コマンド自身を除外する。
```
