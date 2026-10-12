# EP83–85 設計スレ引き継ぎプロンプト v001（2026-08-25）

下の枠内をそのまま新スレに貼る。

---

EP83-85の設計スレを開始します。着手前に `git pull` し、`docs/HANDOVER.md` → `docs/PD_CANON.md` →
`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` → `docs/PD_EPISODE_SPEC_STANDARD.v001.md` を読むこと。

## 決定済み（オーナーGO 2026-08-25・変更しない）

- **EP83 = Boeing 737 MAX** (PD-2026-083-max737) / **EP84 = Three Mile Island** (PD-2026-084-threemile) /
  **EP85 = Katrinaの堤防決壊** (PD-2026-085-katrina)。
- 選定正典 = `episodes/_planning/EP83-85_SLATE.v004.md`（APPROVED・CTR逆算の根拠と実測全部入り）。
- ワーキングタイトル = `EP83-85_TITLES.v004.md` の★3本。**公開タイトルの確定は台本後の
  claims照合＋ペア承認**（全話共通ゲート）。
- サムネは別レーン進行中: プレート30枚をCodexが生成中（`THUMBNAIL_ORDERS_2026-08-25/`）、
  文字設計= `EP83-85_THUMB_TEXT.v001.md`。**設計スレはサムネのファイルに触らない。**

## やること（1話ずつ完結・EP83から。並行しない）

1. **novelty check → R3リサーチ**。R3の最優先はワーキングタイトルの立証3点:
   - EP83: 「Boeing Knew」の立証枠組み＝**1回目墜落後のFAA自身のリスク分析（追加墜落予測）と
     飛行継続の決定**、＋2016年社内メッセージ、＋DOJ訴追延期合意の事実認定。**訴訟はliveなので
     公開前の再確認をゲートに入れる。**
   - EP84: 刑事記録の一次照合（1983起訴→1984 Met-Ed答弁）。改竄されたのは正確には**漏えい率試験**。
     タイトルの「Safety Tests」への一般化が台本の実文で支えられるか、を先に決める。
   - EP85: In re Katrina Canal Breaches（Duval判事のRobinson判決→第5巡回区の免責逆転）。
     **過失認定の範囲はMR-GO側**——タイトルの帰属表現は判示の言い回しに合わせて調整。
     race-chargedな実話（サムネの顔全面禁止は決定済み）。
2. FACTS_LEDGER → `episodes/<EPID>/episode_spec.v001.json`（**28-35分帯**・forbidden_subjects/
   forbidden_claims必須。根拠=TOPIC_POOL_500 §F2: 25-43分のAVP 47.5%）。
3. 設計書＋台本（3回パス・アカデミー基準・editorial v002「人→異常事→なぜ→制度」・フック8秒・
   OP/ED正典Bookends・死者数をタイトルに書かない）。script_verified まで。

## 制約（再掲・拘束）

実在人物の肖像禁止（83は遺族・殉職乗員、84は運転員・知事、85は実在住民）/
本編画像はCodex原則（SDXL勝手起動禁止）/ 台帳にない数字は台本・タイトル・サムネの
どこにも書かない / 尺はfps由来・フレーム直書き禁止（Remotion側）/
`check_packaging_claims.py` は台本完成時に `--title --thumb-text` 両方で実行。

## 引き継ぎの終わり方

各話 script_verified 到達時に `docs/HANDOVER.md` 更新＋ `docs/handover/YYYY-MM-DD.md` に経緯。
組み立て・レンダ・投稿はさらに別レーン（PD_CANONのレーン分担に従う）。

---

以上。
