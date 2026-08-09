# 引き継ぎ — 非公開→公開キャンペーン完了後の残作業 v001

**2026-08-09 20:00 JST 作成。** 前スレは「非公開10本を公開へ戻す」を完遂した。
このファイルは (A) 確定した現在地、(B) 残作業3件の詳細、(C) 罠、の順。
**着手前に §A の検証コマンドで現在地を再実測すること（推測しない）。**

---

## A. 確定した現在地（2026-08-09 19:5x API実測）

### チャンネル状態
- **公開中 110本 / 予約済み37本 / 非公開・予約なし 0本 / 限定公開 0本**（総数147）
- 予約は 8/10〜8/17 に毎日自動公開される。**人手は不要。**
  - 長尺（全て12:00 JST・8/10〜8/15連続）: 8/10 norfolk `H8j_K1x9Dog` / 8/11 fieldtest `KPYLtYYODLE` /
    8/12 lejeune `J97Rh1qOTPA` / 8/13 willingham `l7-oHSNEIjc` / 8/14 morton `67gynOvKf1M` /
    8/15 weimer `SpXTxT6nd24`（8/16→8/15へ前倒し、2026-08-09 20:1x 実施・検証済み。
    長尺在庫はこれで尽きている。次の長尺が出来るまで8/16以降の12:00は空き）
  - ショート: 4本/日（6/9/18/21 JST）。**12:00 は長尺専用**（8/9に30本再配置済み）
- **旧・欠陥版7本はオーナー承認のうえ8/9に削除済み**（burge旧/fieldtest旧/willingham旧/
  morton旧/norfolk旧/flowers旧/postoffice旧）。ローカルの旧マスターは各話 `08_edit/` に残存。
- flowers `PfdEpNQyaQQ` / postoffice `4FlCaOVpln0` / burge `Iw-EPUD2nHg` は公開済み。

### 検証コマンド（着手時に必ず）
```bash
cd /c/Users/aab15/Documents/prime-documentary
py -3.11 scripts/yt_channel_index.py            # 索引の和集合を再取得（唯一の列挙口）
py -3.11 scripts/yt_schedule_audit.py | head -45  # 予約が残り何本か・12:00衝突がないか
```

### カレンダー運用の取り決め（オーナー指示 2026-08-09）
- **公開カレンダーの操作（アップロード・予約・再配置）は1セッションだけが行う。**
  8/9 に2スレが同時に reslot を打ち30本ずれた実績がある。
- 日々のショート運用は `bash scripts/daily_shorts_push.sh [reserve]` に集約済み。
  長尺アップロードがある日は `daily_shorts_push.sh 1650`。
- 長尺の予約は `upload_schedule_case_v001.py --ep <slug> --replaces <旧ID>` のみ（ship-gate準拠）。

---

## B. 残作業（優先度順）

### B-1. ショート関連リンク54本の設定（最優先・登録者に直結）

> **2026-08-09 21:xx 更新（実測で訂正）。** この節の前提は2つ間違っていた。
> (1) **54本はすでに全部設定済み**だった。2026-08-07 05:5x〜06:16 に別セッションが
> `C:\temp\studio_auto\run_batch.js`（未コミット）で71本を設定しており、その中に54本が含まれる。
> 今日、54本すべてを Studio 画面から**読み戻して確認済み**（54/54 ALREADY_SET・
> `runs/related_link/ledger.jsonl`）。手作業30分は不要。
> (2) **「関連リンク設定用のツールは未整備」も誤り。**ツールは存在したがリポジトリ外にあった。
> 現在は `scripts/studio/related_link_batch.js` としてリポジトリに取り込み済み
> （入力＝worklist JSON・許可リスト強制・再開可能な台帳・保存後リロードして読み戻し検証・
> title/description/privacy/publishAt を Data API で前後比較するガード付き）。手順は
> `scripts/studio/README.md`。
> (3) **「SHRTがゼロ」の計測は 2026-08-07 04:15 のキャッシュ**で、リンク設定より**前**。
> つまりまだ効果測定になっていない。Analytics は約2日遅れるため、8/08 以降を含む窓で測り直すこと。
> (4) 「まだ設定できない23本」も誤り。うち14本は `runs/_cache/legacy_short_destinations.json` と
> ショート自身の説明文リンクの**両方**が同じ長尺を指しており、すでに設定済み。
> worklist は手作りをやめ `scripts/studio/build_related_link_worklist.py` で再生成する
> （v002＝`runs/_cache/related_link_worklist.v002.json` / 対象81本・行き先の根拠を各行に記録）。
- **事実（実測）**: ショート5,134再生から長尺への流入が**ゼロ**。末尾カードも固定コメントも
  経路として機能していない。唯一の公式経路「関連動画」は **YouTube Studio UIでしか設定できない**
  （Data API・Analytics APIに該当機能なし）。
- **作業リスト**: `episodes/_planning/SHORTS_RELATED_LINK_WORKLIST.v001.md`
  （今すぐ設定できる54本。URL・対象長尺ID付き。生成元=`runs/_cache/related_link_worklist.json`）
- **手順書**: `docs/PD_SHORTS_RELATED_VIDEO_LINKING.v001.md`（1本20-30秒×54本≒30分。
  「すべて表示」を開く→関連動画欄→長尺IDで検索→保存）
- **自動化するなら**: Studio UI自動化は既に実績あり（専用ブラウザプロファイル＋初回手動ログイン
  方式。複製プロファイル・既定プロファイルは保護で不可）。ただし**関連リンク設定用のツールは
  未整備**（新規構築が要る）。cookie方式のスクレイパー（`yt_studio_ctr.py`、
  `secrets/studio_cookies.txt`）は読み取り専用でリンク設定には使えない。
- **効果測定**: 設定7日後に `py -3.11 scripts/yt_funnel_analytics.py 2026-08-07 <7日後>` を実行し、
  長尺の `SHRT` 列が0から動くかを見る。1でも入れば因果確定。
- 予約中の長尺（8/13 willingham等）は**公開後でないと選べない**。リストの「まだ設定できない23本」
  は長尺公開後に `runs/_cache/related_link_worklist.json` を再生成してから。

### B-2. probe受領書の自動発行（機構修正・次の長尺から効く）
- **問題**: `scripts/probe_before_render.sh` はprobeを実行するが**受領書を書かない**。
  受入ゲートの `probe_receipt` は古い `09_package/probe_receipt.v*.json`（旧filmのsha束縛）を見て
  必ずFAILし、毎回APRで全尺スキャンをやり直している（norfolk/willingham/morton全部そうなった）。
- **直し方**: probe成功時に `probe_receipt.v(N+1).json` を書く。スキーマは既存v001/v002参照
  （slice_sha256 / film_sha256 / generated_at ほか）。film_sha256は
  `remotion/src/data/<slug>_film.json` のsha256。
- **§4.6遵守**: 追加後、わざと古いfilm shaを書いた受領書で受入が落ちること、新しい受領書で
  通ることの両方向を実証してから頼ること。
- **代替の実測手順（ツールを直すまでの間）**: 全尺スキャンで受領書より強い証拠を作れる。
  `ffmpeg -i <master> -vf "blackdetect=d=0.5:pix_th=0.10,freezedetect=n=-60dB:d=2" -an -f null -`
  黒/凍結イベント0（または黒<1.2s）ならAPRに実測値を書く（burge APR-0003文例）。

### B-3. check_shipped_frames のマスター選択罠の恒久修正
- **問題**: `--slug` だけ渡すと `08_edit/<slug>_final_bgm.v*.mp4` の**リビジョン最大**を掴む。
  willinghamでは古い `v002`（7/30）が今日の `v001` に勝ち、**旧レンダーの焼き込み名札3件を
  現行マスターの違反と誤認しかけた**（読者2名の読解が丸ごと無効になった）。
- **今回の回避**: 旧v002は `episodes/PD-2026-051-willingham/08_edit/superseded/` へ隔離済み。
- **直し方**: リビジョン番号でなく **納品記録（final_delivery.v*.json の最新）が指すファイル**
  または **mtime最新** を選ぶ。修正後、verdict JSONの `"render":` パスと
  `render_sha256` が実ファイルのsha256と一致することを必ず確認。
- **検査した結果を使う前に必ず**: `grep '"render"' runs/qc/<slug>_shipped_frames.v001.json` で
  どのファイルを測ったか見る癖をつける（今回これで発覚した）。

---

## C. このキャンペーンで踏んだ罠（新規分のみ・既知分はPD_RETRO_20260805参照）

1. **過去日付の publishAt は「即時公開」になる**。norfolkが16:01に一瞬publicになった。
   ガードは二重装備済み（initiate側＋main側）で、過去日付はdry-runでも拒否される。
   **CONFIGの日付は必ず未来かを目視**（dry-runが表示する `OK schedule local=` を読む）。
2. **videos.update直後のGETはpublishAt=Noneを返すことがある**（read-after-write遅延、実測8秒）。
   verifyは3回リトライ化済み。手でAPIを叩くときも1回のGETで断定しない。
3. **supersede受領書（youtube_schedule_result.v002.json）はアップロード前に書かれる**。
   「受領書の存在」を完了マーカーに使うと早発火する（実際にチェーンが早く進んだ。今回は
   結果オーライだが、次は `WATCH https://` 行の存在などアップロード後にしか出ない印を使う）。
4. **一度publicになった動画にはpublishAtをすぐ付けられないことがある**。private化→数秒待って
   再PUTで付いた。ダメなら日時指定のタスク（schtasks等）で公開時刻にprivacy切替。
5. **2セッション同時にカレンダーを触らない**（§Aの取り決め。30本ずれた実績）。
6. 削除は「private・予約なしを全件ガード検証→DELETE→再GETで0本確認」の3段で。

---

## E. 環境メモ（次スレが知らないと困ること）

- **バックグラウンドジョブは全て終了済み**（レンダーキュー・監視・自動アップロードチェーン。
  残プロセスなし。前スレのscratchpadスクリプトは使い捨てで再利用不要）。
- **C: の空きは約105GB**。8/9に `%TEMP%\Adobe` 配下のAE一時領域77GBを削除し、
  `After Effects` / `After Effects 2026` は **H:\ae-temp へのジャンクション**に差し替え済み
  （以後AEがC:を食い潰さない）。レンダー失敗の「browser setup 30秒タイムアウト」は
  ディスク以外でも起きるため `pd_render_guarded.sh` の既定タイムアウトは120秒にしてある。
- willingham の旧マスター `willingham_final_bgm.v002.mp4` は
  `episodes/PD-2026-051-willingham/08_edit/superseded/` にある（削除していない。
  誤って 08_edit/ 直下へ戻すと §B-3 の罠が再発する）。
- YouTube APIクォータ: 日次10,000ユニット・**リセット16:00 JST**。アップロード1本≒1650-2050。

## D. 参照ファイル

- 完了記録: `episodes/_planning/RESUME_UNPAUSE_CAMPAIGN.v001.md`（チェックポイント積層）
- インシデント: `episodes/_planning/INCIDENT_20260809_OLD_UPLOADS_REPUBLISHED.v001.md`（クローズ済み）
- 失敗全集: `docs/PD_RETRO_20260805_UNPAUSE.v001.md`（15件）
- 別件（このスレ管轄外・状態不明のまま）: EP62 greene i2v再開=`EP62_greene_I2V_RESUME.v001.md` /
  EP63 correa QC=`EP63_correa_PLATE_QC_FINDINGS.v001.md` / EP64 memphis ポストゲートFAILで停止中
