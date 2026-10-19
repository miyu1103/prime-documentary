# EP39 — Frazier v. Cupp /「警察は、取調べであなたに嘘をつけるのか？」— 制作設計書 ＋ Codex引き継ぎプロンプト

- **Episode ID:** `PD-2026-039-frazier` / slug `frazier` / EP39
- **バージョン:** **v002（2026-07-19）。v001 を上書きする正典。** v001 は「主役未確定・台本未着」前提で書かれており、主舞台・数値・シーン割りが**確定台本と一致しない**。衝突したら常に本書 v002 が勝つ。
- **確定台本（唯一の真実・一字も変更禁止）:** `episodes/_planning/EP39_frazier_script.en.v001.md`（見出しは `script.en.v002`）。
- **上位正典:** `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`（ハードGATE・最優先）＞ `docs/PD_WINNING_PATTERN.md` ＞ `episodes/_planning/VIDEO_RULES.md` ＞ 本書。
- **v001 から引き継ぐ節（変更なし・そのまま有効）:** §3.6 AEマシン固有の罠 / §4 Opening 実装仕様 / §2.2–2.3 JSON契約のスキーマ。本書はそれらを再掲せず**参照**する箇所を明示する。

---

## 0. 受入条件の再掲（Codexは最初にここを読む）

満たすべき v2 row: **row1**(BGM) **row2**(ElevenLabs) **row3/4**(字幕) **row5**(画像長辺≥3840) **row6**(libx264 / preset slow / crf16 / yuv420p / bt709 / aac320k / NVENC禁止 / ラウドネス) **row7**(素材多様性) **row8**(アニメ密度・紙芝居禁止) **row9**(フック) **row10**(4部構成＋earned CTA) **row11/12/13**(サムネ3案・4語以内・A/B) **row14**(OP/EDはBookendsをimport) **row15/16**(台本・リテンション設計)。

```bash
# 中間確認（いつでも）
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 39 --json

# 最終（AE合成後の実ファイルに対して。これが exit 0 になるまで "done" と言わない）
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 39 \
  --render episodes/PD-2026-039-frazier/08_edit/frazier_final_bgm.v003_ae.mp4 --emit-receipt
```

**THE ONE RULE:** validator PASS ＝ done ではない。**独立した受入スクリプトが実 `final.mp4` を測って全ハードGATEを通って初めて done。** 自作の品質ゲートを書いて「合格」と宣言するのは禁止。GATEを緩めて通すのも禁止。

### 0.1 ★ゲート実装を実際に読んで判明した3点（v001 の前提を訂正する）

`scripts/check_final_acceptance.py` を読んだ実測。**推測ではなくコード由来なので、これに従うこと。**

| # | v001／house rules の一般記述 | **実装が実際に測っているもの** | 設計への影響 |
|---|---|---|---|
| 1 | 「フックはヘッド6–10秒」 | `check_structure`（HARD）は**秒数の上限を測っていない**。測るのは (a) ナレーション章ラベルの並び順が `HOOK` → `OPENING` → 本編 → `ENDING\|OUTRO\|CTA\|CLOSE\|CONCLUSION\|CODA`、(b) `remotion/src/data/frazier_film.json` の `hookSeconds >= 5.0`（`HOOK_MIN_SEC`）、(c) `hookLine` が空でないこと。 | **確定台本の 21.6秒フックはそのまま通る。**削るな。`hookSeconds = 21.6` を `frazier_film.json` に書く。VIDEO_RULES §10 の「20〜30秒」側に合致。 |
| 2 | 「準静止 ≤ 全尺の10%／単一ホールド ≤3秒」 | `LOW_MOTION_MAX_FRACTION = 0.10` / **`LOW_MOTION_MAX_SPAN_S = 3.0`**。実レンダのフレーム差分で測る。 | **本作には SILENCE が8箇所・合計21.0秒あり、うち 4.0秒 と 3.0秒×2 が単一スパンで 3.0秒を超える。**無音＝静止にすると**ハードFAILする**。→ §5.4 に「沈黙区間の必須モーション仕様」を新設。ここが本作最大の落とし穴。 |
| 3 | 「字幕はナレとトークン一致 ≥99%」 | `CAPTION_MATCH_MIN = 0.90` | ゲートは0.90だが**設計目標は据え置き0.99**。ゲートに合わせて緩めない。 |

補足の実測値（同ファイル）: `BOOKEND_OP_SEC=3.5` / `BOOKEND_ED_SEC=9.0` / `IMG_MIN_LONG_EDGE=3840` / `FOOTAGE_GENERIC_MAX_USES=2`（天秤・gavel等）/ `FACTORY_SECONDS_PER_CLIP=45`（**45秒あたり最低1本の distinct factory クリップ** ＝ 705秒なら最低16本。設計目標は house rules の30秒基準＝**24本以上**、実配分は§6で90本）/ `LUFS_LO,HI = -16.0,-12.0` / `hook_added`（SOFT）= `runtime − (shotlist.totals.estimated_total_seconds + 12.5) ≥ 25.0`。

---

## 1. 企画（確定・変更不可）

| 項目 | 確定値 |
|---|---|
| 中心の問い | **「警察は、取調べであなたに嘘をつけるのか？」** → **合法。** |
| 必須3要素 | 二人称（YOU）／自分事の脅威（あなたが取調室に座ったら）／司法の線引き（`Frazier v. Cupp, 394 U.S. 731 (1969)`） |
| 主役 | **Barry Laughman**（1963-05-16 – 2024-03-21）。IQ 70。1988年終身刑 → 2003年 Y-STR で排除 → 2004年 全訴因取下げ。**故人・DNA免罪済み。** |
| 語り口 | **100% 一人の受難型。**判例解説型は実測 APV 1.6–7.5%、一人の受難型は 24–42%。**幕1・幕2に判例名を出さない**（出した瞬間に解説型のレンジに落ちる）。 |
| duration profile | `standard` — `manifest.target_duration_minutes = 11.75`、band **11.5–12.5分（690–750秒）** |
| リスク区分 | **R2**（R3隣接2点を封じ込め。§8） |
| 公開lane | 長尺16:9 ＋ 連動Short（縦9:16・35–45秒）1本 |

**実測データ（設計の根拠・2026-07-18時点）:** CTR **2.31%**（フロア4.0%）／本編APV **15–25%**（フロア35%）／登録 **+2**（フロア subs/1,000再生 ≥5）／コメント **0**（≥1）。

---

## 2. 尺の数値根拠（実測ベース・ここが全ての土台）

### 2.1 語数の内訳（実測。推定値を使うな）

`EP39_frazier_script.en.v001.md` から【OST】行・[演出指示]行・見出しを除去した**実発話語数**:

| 章 | 発話語数 | @178.1 wpm |
|---|---|---|
| HOOK | 64 | 21.6s |
| OPENING | 22 | 7.4s |
| ACT I | 268 | 90.3s |
| ACT II | 326 | 109.8s |
| ACT III | 414 | 139.5s |
| ACT IV | 728 | 245.3s |
| ENDING | 154 | 51.9s |
| **合計（VO実発話）** | **1,976** | **665.7s** |

> 尺ゲート `check_script_length.py` が出した **2,136語** は【OST】のラテン文字語も数えている（`count_words()` の既知の挙動）。**TTSに渡るのは 1,976語のほう。**両方を混同するな。

### 2.2 総尺の積算

```
VO 発話           665.7 s
SILENCE 8箇所      21.0 s   (2.5 + 2.0 + 2.0 + 2.0 + 3.0 + 2.5 + 4.0 + 3.0)
BrandOpening        3.5 s
BrandEndcard        9.0 s
──────────────────────────
総尺 目標          699.2 s  ≒ 11:39   → 端数丸めと転換の間で 705 s (11:45) を設計値とする
許容 band         690 – 750 s        （standard profile・HARD）
```

**設計値: 総尺 11:45（705秒）。** フロア690秒に対する余裕は **+15秒しかない**。

### 2.3 ★尺の機械制御ルール（VO実測後に必ず実行する。ここを守らないと `runtime_band` で落ちる）

house rules 記載の fast端リスク（237.4 wpm が williams/florence で観測）が現実化すると VO は 500秒まで縮み、総尺 533秒＝**フロア大幅未達**になる。対策は2段構え。

1. **一次対策＝voice を固定する。** ElevenLabs `VOICE_ID=nPczCjzI2devNBz1zQrb` / `eleven_multilingual_v2` / **stability 0.35 / similarity_boost 0.80 / style 0 / speaker_boost on**。この4値を変えない。
2. **二次対策＝沈黙予算を機械調整する。** ナレ生成後に実VO長 `X`（秒・全チャンク結合、チャンク間ギャップ除く）を測り、次式で沈黙総量 `S` を再配分する:

```
S = 705.0 − X − 12.5        # 12.5 = BrandOpening 3.5 + BrandEndcard 9.0
各沈黙 i の長さ = S × (設計値_i / 21.0)      # 8箇所の比率を保つ
制約: 各沈黙は 1.5s 以上 6.0s 以下にクランプする
```

| 実VO長 X | 沈黙総量 S | 判定 |
|---|---|---|
| 665.7s（設計どおり） | 26.8s | ✅ そのまま |
| 640s | 52.5s | ✅ 沈黙を1.63倍（4.0秒→6.0秒でクランプ、残余は幕間の“ひと呼吸”ビートへ） |
| 610s 未満 | 82.5s 超 | ❌ 沈黙で埋めるのは不可。**停止してオーナーに報告する**（voice設定の誤りを疑え） |
| 700s 超 | 0 未満 | 沈黙を各1.5秒までカット。それでも750s超なら停止して報告 |

3. `hook_added`（SOFT）: `705 − (shotlist.totals.estimated_total_seconds + 12.5) ≥ 25` → **`shotlist.totals.estimated_total_seconds ≤ 667.5`**。shotlist の `totals` は**本編（幕1〜ENDING）のみを積算し、HOOK 21.6秒を含めない**こと。

---

## 3. 秒数ベースの全区間タイムライン（設計値。anchor 解決後に実値で置換）

t は総尺 705秒基準。`R#` = 再フック（v2 row16）、`HB#` = AE heroビート、`MG#` = Remotion キネティックカード、`SIL` = 沈黙。

| t (開始) | 長さ | 役割 | 画（scene ID） | 動き／備考 |
|---|---|---|---|---|
| 0.0 | 21.6 | **HOOK**（`hookSeconds=21.6`） | S01→S02→S03→S04 を約2.0秒ずつ×2巡＋決めカット | フラッシュフォワード。**新規素材を作らず本編の決めカットを流用**。ナレ入り＋語同期字幕。`hookLine` = `"Every word of that was invented, and every word of it was legal."` |
| 21.6 | 3.5 | **OPENING** = `BrandOpening`（import。フォーク禁止） | 金タイトル | `OPENING_SEC=3.5` を変更しない |
| 25.1 | 7.4 | OPENING ナレ（3文） | S14（匿名の後ろ姿・机の向こう） | 0.8%/秒の押し込み＋グレイン |
| 32.5 | 8.8 | ACT I 開幕 — Oxford Township | S05 トウモロコシ畑（factory） | **R1**: 農村の光 ↔ HOOK の検死台の落差 |
| 41.3 | 13.1 | 8月13日朝／夜に発見 | S06→S07 | Ken Burns 逆方向で繋ぐ |
| 54.4 | **2.5** | **SIL-1** | S08 無人の台所・網戸・床の錠剤瓶 | **§5.4 の沈黙モーション必須** |
| 56.9 | 14.5 | 被害（象徴のみ・非グラフィック） | S08 続き→S07 | 光だけが動く |
| 71.4 | 18.9 | 近隣からの名前・IQ 70 | S09→S10 | |
| **84.5** | **5.5** | **HB1_IQ_70**（AE・A_BIG_NUMBER `70`） | S14 | anchor `with an IQ of 70` |
| 90.3 | 4.7 | **「指紋が現場にあった」** | S12 指紋カード | **R2**（本作の点火点）。MG1 = 指紋カードのマス目が埋まる→**一瞬で全部空白に戻る**リビール |
| 95.0 | 20.9 | 確認できない／23年前への前振り | S13→S11 | 語同期: `no way to check` |
| 115.9 | 0.7 | `Barry confessed.` | S15 閉まる扉（内側） | 扉が閉じ切る瞬間に語を同期 |
| 116.6 | **2.0** | **SIL-2** | S11 椅子二脚＋机の指紋カード | 沈黙モーション必須 |
| 118.6 | 9.1 | 供述の帰結（16年の予告） | S16 供述調書の紙（判読不能） | 【OST: IQ 70. TOLD: "YOUR PRINTS ARE THERE."】 |
| 127.7 | 2.4 | ACT II「家と合わない」 | S17 手つかずの窓 | |
| 130.1 | 18.5 | 窓・8月12日・野菜畑 | S18 野菜畑の朝（**モチーフ反復＝意味のある反復**） | **R3**。MG2 = 日付の対比カード 8/12 ↔ 8/13 |
| 148.6 | 21.2 | 血液型（A分泌型／B分泌型） | S19 試験管ラック→S20 標本瓶 | MG3 = A/B 抗原の図解組み上げ（**汎用B-roll禁止**） |
| 169.8 | 28.3 | 化学者の誤証言・陪審の前 | S21 証言台→S22 陪審席 | MG4 = 引用リビール（`testified incorrectly` を帰属付きで） |
| 198.1 | **2.0** | **SIL-3** | S23 ガラス瓶の棚＋法廷の空席 | 沈黙モーション必須 |
| 200.1 | 18.9 | **非公開細部（最強の札）** | S24 検死台のステンレス縁（人体なし） | **R4**。抑制した寄り。血・傷を映さない |
| 219.0 | 4.7 | 捜査官の証言 | S16 | |
| 223.7 | **2.0** | **SIL-4** | S24 | 沈黙モーション必須 |
| 225.7 | 6.1 | 訴状の主張・未審理（帰属必須） | S25 訴状の紙束（判読不能） | 【OST】で「allegation, never tried」を明示 |
| **231.8** | **6.0** | **HB2_CONVICTION**（AE・D_CITATION_STAMP `1988`） | S26 | anchor `On December 16, 1988` |
| 239.2 | 7.1 | ACT III — Portland 1964 | S28 1964年の夜の街（factory） | **R5**（場所と時代が飛ぶ＝最大の転換） |
| 246.3 | 14.8 | Rawls の虚偽告知 | S29→S30 回転式電話 | |
| 261.1 | 13.8 | 会話劇（水兵の一言／officer の返し） | S31 1964質感の取調室 | MG5 = 台詞2枚のキネティックタイポ（逐語・引用符付き） |
| 274.9 | 15.8 | 有罪→4年半後→Marshall | S32 最高裁外観（factory） | |
| 290.7 | 14.5 | 中核判示の一文 | S33 無人の法廷（factory） | MG6 = 判示の逐語リビール |
| **296.0** | **6.0** | **HB3_FRAZIER_CITATION**（AE・D_CITATION_STAMP `1969`） | S34 判例集の書架 | anchor `while relevant, insufficient in our view` / bottom `FRAZIER v. CUPP · 394 U.S. 731` |
| 305.2 | 20.9 | 「天秤に乗る」＝関連性 | S35 天秤（**汎用シンボル。本作で使用は1回のみ**） | MG7 = 天秤に重りが載る組み上げ |
| 326.1 | 30.0 | 二つの見落とし（Miranda / 弁護士の一言） | S36 めくれる頁（factory）→S31 | **20秒超の平坦を作らない**: 12秒目でカット替え＋MG8 タイムライン（Escobedo→Frazier→Miranda） |
| 356.1 | 7.1 | **会話の反転** | S31（同アングルの逆側） | **R6**。同じ画に戻ることで「二度目に聴く」を視覚化＝意味のある反復 |
| 363.2 | 8.8 | Miranda が飲み込んだ後に残った規則 | S37 抽象「状況の総体」 | |
| 372.0 | 7.4 | **Barry への橋** | S12 指紋カード（再登場・2回目） | |
| **372.5** | **6.5** | **HB4_THE_FINGERPRINT**（AE・B_SPLIT_RATIO `1` / `0`） | S12 | anchor `when an officer told Barry Laughman about a fingerprint` |
| 379.4 | 15.5 | ACT IV — 1993 / 2003 DNA | S38 ラボ→S39 電気泳動の抽象 | |
| 394.9 | 20.2 | 釈放・再審・訴因取下げ | S40 開いた鉄扉の外・朝 | |
| 415.1 | 4.7 | 「Sixteen years.」 | S40 | |
| **415.1** | **6.0** | **HB5_SIXTEEN_YEARS**（AE・A_BIG_NUMBER `16 YEARS`） | S40 | anchor `He had gone in at twenty-five and come out at forty` |
| 419.8 | **3.0** | **SIL-5** | S40 朝の駐車場（無人） | **3.0秒＝ゲート上限ちょうど。モーション必須（§5.4）** |
| 422.8 | 7.4 | §1983（2文・数値は全てOST） | S42 連邦裁判所（factory） | |
| 430.2 | 25.6 | Parabon / Speelman / 58歳 | S43 家系図の抽象（光の線が繋がる） | **R7**。MG9 = 系譜のノードが1点に収束 |
| **462.6** | **5.5** | **HB7_PAROLE**（AE・D_CITATION_STAMP `2046`） | S42 | anchor `with no parole eligibility until 2046` |
| 468.6 | 7.4 | 死（2024-03-21・60歳） | S44 病院の廊下（抑制） | |
| 476.0 | 14.8 | **自由だった20年の空白** | S45 空のカレンダー壁・埃の光 | 「記録に無い」ことを画で言う |
| 490.8 | **2.5** | **SIL-6** | S41 空の椅子と朝の窓 | 沈黙モーション必須 |
| 493.3 | 13.5 | 257件・平均16年・4,102年 | S46 数字のみの画面 | |
| **500.8** | **6.0** | **HB6_FOUR_THOUSAND**（AE・A_BIG_NUMBER `4,102 YEARS`） | S46 | anchor `they come to four thousand, one hundred and two years` / `anchor_align: "end"` |
| 506.8 | **4.0** | **SIL-7** | S46（数字だけを保持） | **★4.0秒＝ゲート上限3.0秒を超える最長スパン。ここが最大の危険箇所。§5.4 の仕様を必ず実装** |
| 510.8 | 14.8 | 子ども34% ↔ 成人10% | S47 現代の取調室 | MG10 = **C_PERCENT_ARC相当の円弧カード（Remotion側で実装）**。AEに置くと HB6 と8秒しか空かず配置制約違反になるため意図的にRemotionへ回した |
| 525.6 | 7.4 | **Barry への接続1文** | S14（再登場） | |
| 533.0 | 24.6 | 立法（Oregon SB418 / Illinois） | S48 州議事堂（factory） | MG11 = 州地図に色が入る（10州） |
| **551.0** | **5.5** | **HB8_TEN_STATES**（AE・A_BIG_NUMBER `10 STATES`） | S48 | anchor `by 2026 roughly ten states have some version of it` |
| 557.6 | 7.4 | 成人には州法がない | S47 | |
| 565.0 | 35.4 | Cayward（偽の鑑定書の線） | S49 紙の縁と便箋の質感（**書式が本物に見える画像は禁止**） | **R8**。MG12 = 「言ってよい／印刷してはいけない」の二分割 |
| 600.4 | 4.0 | `They may say it.` | S49 | |
| 604.4 | 30.3 | Kassin / AP-LS / Bronx | S33→S47 | MG13 = 提言3点のスタッガー・リスト |
| 634.7 | 23.9 | ENDING — 部屋への回帰 | S11→S01 | 冒頭の問いを閉じる |
| 658.6 | 14.5 | 「sixteen years undoing one sentence」 | S16 | |
| 673.1 | 3.0 | `The print was invented. The permission was not.` | S50 閉じた扉 | MG14 = 2文のキネティックタイポ（対句） |
| 676.1 | **3.0** | **SIL-8**（字幕なし） | S50 | 沈黙モーション必須。**字幕トラックも空にする** |
| 679.1 | 9.1 | **earned CTA（1つだけ・末尾30秒以内）** | S50 | 「見方が変わったなら like/登録を」。一般的な物乞い禁止 |
| 688.2 | 9.0 | `BrandEndcard`（import・`ENDCARD_SEC=9`） | — | 変更禁止 |
| 697.2 | 8.1 | 次回引き（没収／自分の財産を訴える） | S49 | 終了画面（次の本編＋登録） |
| **705.3** | — | 終端 | | band 690–750 ✅ |

**再フック点（8箇所・最大間隔 92秒 < 150秒）:** R1 32.5 / R2 90.3 / R3 130.1 / R4 200.1 / R5 239.2 / R6 356.1 / R7 430.2 / R8 565.0。
**平坦区間チェック:** 20秒を超える単一ショット・単一テンションの区間はゼロ。最長の連続ナレ塊（ACT III 326.1–356.1 の30秒）は 12秒目でカット替え＋MG8 を挿入して分割する。

---

## 4. 4部構成の役割ラベルと promise–payoff 対応表

### 4.1 章ラベル（`structure_4part` HARD の入力。**この文字列で書く**）

ナレーション JSON の各 chunk の `section` は次の文字列で始めること（大文字・実装が `startswith` で判定する）:
`HOOK` → `OPENING` → `ACT I` / `ACT II` / `ACT III` / `ACT IV` → `ENDING`。
加えて `remotion/src/data/frazier_film.json` に `"hookSeconds": 21.6` と `"hookLine": "Every word of that was invented, and every word of it was legal."` を入れる（**両方無いと HARD FAIL**）。

### 4.2 promise–payoff 対応表（フックの4つの約束が本編で必ず回収されること）

| # | HOOK が見せた約束 | 回収位置 | 回収するナレ |
|---|---|---|---|
| P1 | 「検死でしか見えない傷を言い当てた」 | **200.1s（ACT II）** | `A wound to her head that, according to the case record, was not visible until the autopsy.` |
| P2 | 「捜査官は伝えていないと証言した」 | **219.0s（ACT II）** | `Officers testified that they had never given those details to Barry, or to his family.` |
| P3 | 「指紋は存在しなかった／一致も無かった」 | **90.3s（ACT I）＋372.0s（ACT III末）** | `Then an officer told him that his fingerprints had been found at the scene.` → `when an officer told Barry Laughman about a fingerprint` |
| P4 | 「その全部が合法だった」 | **290.7–372.0s（ACT III 全体）** | 中核判示 → `That is the rule that was waiting in the room` |

**タイトル／サムネの約束の回収:** タイトルA/B（§9）が約束する「警察は合法に嘘をつける」「16年」は、それぞれ 290.7s / 415.1s で本編が果たす。**約束していないものをサムネに書かない。**

---

## 5. レイヤー構成・モーション設計

### 5.1 レイヤー構成（下から上・最低3レイヤー厳守）

| z | レイヤー | 内容（確定値） |
|---|---|---|
| 0 | ベース | `#05070d` 単色 |
| **1** | **グラデ背景** | `radial-gradient(120% 120% at 50% 35%, #0E1B33 0%, #0A1020 45%, #05070d 100%)`。全尺で scale 1.06→1.00（`Easing.out(Easing.cubic)`）。 |
| **2** | **グリッド／ライン** | `repeating-linear-gradient` 縦横1px・間隔 **64px**・色 `#E5B53A22`、全体 opacity **0.14**、`maskImage: radial-gradient(120% 90% at 50% 45%, black 35%, transparent 80%)`、translateY 0→48px を90秒周期で往復（`Easing.inOut(Easing.sin)`）。 |
| **3** | **グロー** | 中央 `W*0.62 × H*0.36` の `radial-gradient(closest-side, #E5B53A88 0%, #E5B53A22 45%, transparent 75%)` ＋ `blur(28px)`。opacity 0.10–0.22 を12秒周期で呼吸。 |
| **4** | 主役素材 | 静止画（depth-parallax）／factory実写／MGカード |
| **5** | 合成レイヤー | `factory/light_assets`・`particle_assets`・`vfx_overlays` を screen/add 合成 8–18% で常時1枚。**distinct素材に数えない。** |
| **6** | テロップ（`on_screen_text`） | 上部 or 中央ゾーン |
| **7** | 字幕 | 画面下部帯のみ |

### 5.2 トランジションとカット

- 全カット間 **0.3–0.5秒のクロスフェード**。`Sequence` をトランジション長ぶんオーバーラップさせる。**トランジション無しのハードカットはゼロ**（ゲート対象）。
- 平均ショット長 **≤ 6.0秒**（設計目標 4.5秒）。705秒 ÷ 4.5 ≒ **157カット**、上限まで見て 150–170カット。
- 単一ホールド **≤ 2.0秒**（設計上限。ゲートは3.0秒）。
- カットをまたいで運動方向を継承する（速度リセット＝「かくっ」の禁止）。
- **禁止演出:** 紙芝居／左→右の縦スイープライン／全画面の黄・金ウォッシュ／ズーム・パンのみ／リニアイージング／opacity単独の演出。

### 5.3 アニメーション密度の設計目標（ゲート値と設計値）

| ゲート | ハード閾値 | **EP39 設計目標** |
|---|---|---|
| `check_motion_density` kinetic beats/分 | ≥2.5 | **3.2**（705秒＝11.75分 → **38本以上**） |
| 同 coverage | ≥0.25 | **0.32**（≥226秒） |
| 同 variety | ≥3 | **8種以上** |
| `check_animation_mix` still share | ≤0.45 | **≤0.30** |
| 同 motion coverage | ≥0.45 | **≥0.55** |
| 同 5秒超の静止保持 | ≤8回 | **0回** |
| `check_low_motion` 準静止割合 | ≤0.10 | **≤0.06** |
| 同 単一準静止スパン | ≤3.0秒 | **≤2.0秒** |

**キネティックビート 38本の内訳（確定）:** AE heroカード **8** ＋ Remotion MGカード **14**（MG1–MG14・§3のタイムライン）＋ depth-parallax の主体ドリー **10** ＋ factory実写のカットイン **6** = **38**。
**variety 8種:** ① AE数値カード ② 引用リビール ③ タイムライン ④ 図解組み上げ（血液型） ⑤ 地図着色 ⑥ キネティックタイポ ⑦ 円弧パーセント ⑧ depth-parallax ドリー。**同一MGの反復は variety に数えない。**

### 5.4 ★沈黙区間の必須モーション仕様（**本作最大の落とし穴。§0.1 #2 参照**）

`LOW_MOTION_MAX_SPAN_S = 3.0` は**実レンダのフレーム差分**で測る。沈黙8箇所（合計21.0秒、最長4.0秒）を「静止画を置いて音を止める」と実装すると **`low_motion` が HARD FAIL する**。以下を必ず実装する。

沈黙区間に**同時に3つ**を必ず走らせる:

1. **主体の連続ドリー** — depth-parallax で被写体を **1.2%/秒** の等速ではない押し込み（`Easing.inOut(Easing.sin)` で 0.9%→1.5%/秒 に速度変化させる。等速は速度リセットを生むため禁止）。
2. **合成レイヤーの実movement** — `factory/particle_assets` または `light_assets` を screen 合成 opacity **12–18%** で重ねる。粒子・埃・光の揺れが**毎フレーム画素を変える**（これが差分の主要な稼ぎ手）。
3. **グレイン＋ヴィネット呼吸** — film grain 強度 0.035、ヴィネット半径を周期4.0秒で ±3% 呼吸。

**SIL-7（4.0秒・`4,102 YEARS` の画面）の個別仕様:** 数字は静止させてよいが、背後で (a) 金のグロー opacity 0.22→0.10→0.22、(b) 粒子レイヤーが上方向に 18px/秒、(c) 数字自体に letter-spacing 0 → +1.5px の極微ドリフト（4.0秒・`Easing.out(Easing.cubic)`）を掛ける。**画面が「止まって見える」ことと「フレーム差分がゼロ」であることは別物**であり、要求は後者を避けることである。

**SIL-8（3.0秒・字幕なし・閉じた扉）:** 扉の隙間の光量を 100%→0% へ 3.0秒（`Easing.in(Easing.cubic)`）で落とす。**これは opacity 単独ではなく**、同時に扉を 0.8% スケールで押し込む。

---

## 6. 素材構成（`footage_diversity` / `check_asset_reuse` を通す配分）

### 6.1 確定配分（150–170カット / distinct ≥110点）

| 種別 | distinct 点数 | 1点あたり使用上限 | 調達 |
|---|---|---|---|
| SDXL 静止画 | **60枚**（30シーン × 2採用） | **2回** | ローカル A1111（§10） |
| factory 実写クリップ | **90本** | **1回**（再使用禁止） | `H:/pd-media/assets/factory`（在庫11,623本） |
| i2v モーション（Wan 2.2 A14B） | 18本 | 2回 | SDXL採用画から生成 |
| 合成レイヤー（light/particle/vfx） | 随時 | — | **distinct に数えない**（§5.1 z=5） |

- `distinct/total ≥ 0.40` に対し設計値 **110 / 160 = 0.69**。
- `FACTORY_SECONDS_PER_CLIP=45` → 最低16本のところ **90本**。house rules の30秒基準（24本）も大きく超過。
- **汎用シンボル上限 2回**: 天秤は S35 の**1回のみ**。gavel（法槌）は**本作では一切使わない**（Cayward の主題と紛らわしいうえ枠を消費する）。
- 「意味のある反復」として意図的に再登場させるのは **S12 指紋カード（90.3s / 372.0s）**、**S14 匿名の後ろ姿（25.1s / 525.6s）**、**S18 野菜畑（130.1s と HOOK 流用）**、**S31 1964取調室（261.1s / 356.1s の反転）** の4点のみ。それ以外の再登場は禁止。

### 6.2 ★factory のラベルは信用できない（工程に組み込む）

EP36 で `city_surveillance_camera_dome` が実際にはベオグラードの大聖堂、EP38 で `documents_on_desk` が牛の映像だった実例がある。**110本をステージングして全点を目視QCする（約2時間。削るな）。** さらに本作は R2 なので **「顔が識別できる人物が大きく写っているクリップ」は `on_theme:false` として除去する。**

---

## 7. AE heroビート設計（8本・確定値）

パイプライン原則・レイアウト内部仕様（`A_BIG_NUMBER` / `B_SPLIT_RATIO` / `C_PERCENT_ARC` / `D_CITATION_STAMP` / `E_VOTE_TALLY` の全数値、共通タイムライン表）と**このマシン固有の罠15項目は v001 §3.1 / §3.3 / §3.6 をそのまま使う（変更なし）。** 本節は EP39 の**スロット内容だけ**を確定する。

### 7.1 スロット確定表

すべて `claim_id` 必須。`start` は `null` で出し、`anchor_phrase` の語タイム一致で解決する（**手書き禁止・ヒット0件または2件以上なら FAIL で停止**）。

| id | slot | layout | value | prefix/suffix | top | bottom | anchor_phrase（ナレ本文に逐語1回のみ存在） | align | dur | 設計t | claim |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hb01 | `HB1_IQ_70` | `A_BIG_NUMBER` | 70 | — / `""` | `MEASURED IQ` | `FUNCTIONED AT TEN` | `with an IQ of 70` | start | 5.5 | 84.5 | C-09 |
| hb02 | `HB2_CONVICTION` | `D_CITATION_STAMP` | 1988 | — | `THE VERDICT` | `DEC 16, 1988 · LIFE` | `On December 16, 1988` | start | 6.0 | 231.8 | C-12 |
| hb03 | `HB3_FRAZIER_CITATION` | `D_CITATION_STAMP` | 1969 | — | `THE RULE` | `FRAZIER v. CUPP · 394 U.S. 731` | `while relevant, insufficient in our view` | start | 6.0 | 296.0 | C-04 |
| hb04 | `HB4_THE_FINGERPRINT` | `B_SPLIT_RATIO` | 1 / **value2 = 0** | — | `PRINTS CLAIMED` / **top2** `PRINTS THAT EXISTED` | `TOLD TO BARRY LAUGHMAN` | `when an officer told Barry Laughman about a fingerprint` | start | 6.5 | 372.5 | C-08 |
| hb05 | `HB5_SIXTEEN_YEARS` | `A_BIG_NUMBER` | 16 | — / `" YEARS"` | `TAKEN` | `IN AT 25 · OUT AT 40` | `He had gone in at twenty-five and come out at forty` | start | 6.0 | 415.1 | C-14 |
| hb06 | `HB6_FOUR_THOUSAND` | `A_BIG_NUMBER` | 4102 | — / `" YEARS"` | `257 EXONERATIONS` | `END TO END` | `they come to four thousand, one hundred and two years` | **end** | 6.0 | 500.8 | C-19 |
| hb07 | `HB7_PAROLE` | `D_CITATION_STAMP` | 2046 | — | `NO PAROLE UNTIL` | `PLEADED GUILTY 2023` | `with no parole eligibility until 2046` | start | 5.5 | 462.6 | C-17 |
| hb08 | `HB8_TEN_STATES` | `A_BIG_NUMBER` | 10 | — / `" STATES"` | `BY 2026` | `CHILDREN ONLY` | `by 2026 roughly ten states have some version of it` | start | 5.5 | 551.0 | C-23 |

`thousands`: hb06 のみ `true`、他は `false`（**hb02/hb03/hb07 は年号なので `thousands=false` 必須**。`1,988` と表示されたらバグ）。`decimals` は全て `0`。

### 7.2 配置制約の検証（全て充足済み）

| 制約 | 結果 |
|---|---|
| `start ≥ 20.0` | 最小 84.5 ✅ |
| `end ≤ 総尺 − 25.0`（= 680.3） | 最大 556.5 ✅ |
| 任意の2ビート間隔 ≥ 20.0秒 | 最小ギャップ = hb05終(421.1) → hb07(462.6) = **41.5秒** ✅ |
| 合計時間 | 47.0秒 / 705秒 = **6.7%** ✅ |

### 7.3 意図的にAEに置かなかったもの（理由付き・勝手に戻すな）

- **34% / 10%（子どもの虚偽自白率）** → HB6 の終端（506.8）から 4.0秒しか空かず、配置制約「間隔≥20秒」に違反する。**Remotion 側の円弧カード MG10** として実装する。
- **257件** → HB6 と同一段落。Remotion の小型カウンタで処理。
- **票数（E_VOTE_TALLY）** → **Frazier の票数は fact ledger に無い。数えて書けば捏造になる。よって E レイアウトは本作では使用しない**（実装は再利用のため残してよいが、spec には出さない）。
- **§1983 の事件番号・被告名・日付** → 台本の指示どおり全て【OST】。AEカードにしない（allegation を「認定事実」に見せる演出になるため）。

### 7.4 数値の出所ロック

hb01–hb08 の全数値は確定台本のナレ本文および `fact_recheck` の C-04 / C-08 / C-09 / C-12 / C-14 / C-17 / C-19 / C-23 に一致する。**台帳に無い数値をカードにしない。** `4,102` は「257件 × 平均16年」の集計値として台本が明示しているものをそのまま使う（再計算して丸めない）。

---

## 8. リスク・安全（R2 ＋ R3隣接2点の封じ込め・例外なし）

**総合区分: R2。** 中心判例は公刊判例で争いがなく、主役は DNA で排除され地方検事が全訴因を取下げ、真犯人が有罪答弁し、本人は2024年に死去している。**専用法務レビューは不要（R2の fact/right review で足りる）。**

### 8.1 R3隣接要素と封じ込め条件（この3点は逐語ロック・ナレ確定後に変更禁止）

| # | 対象 | 封じ込め |
|---|---|---|
| 1 | **Christopher Speelman**（存命の有罪確定者＝R3トリガー） | **裁判記録事実のみ。**「2023年6月22日に第三級殺人・住居侵入で有罪答弁、強姦は不抗争、25〜50年、2046年まで仮釈放不可」。**推測・動機付け・人物描写・映像化を一切しない。**名前は幕4で1回のみ。 |
| 2 | **Edna Laughman**（85歳・性的暴行被害者） | 描写は **無人の台所／開いたままの網戸／床に落ちた錠剤の瓶／朝の庭** の象徴のみ。**身体・被害・暴力の再現は全面禁止。顔・肖像を作らない。**（S07 / S08 / S18） |
| 3 | **Holtz / Blevins / Roadcap**（実在の元州警察官・化学者） | §1983 の**主張（allegation）であって認定事実ではない**。ナレは必ず「訴状によれば」「Laughman 側は主張した」と帰属。**「捏造した」と断定しない。**血液型の証言内容は法廷記録として述べてよいが、**動機の断定は禁止。** |

### 8.2 実在私人の肖像（全等級で不可侵）

- **Barry Laughman / Edna Laughman / Christopher Speelman / Holtz / Blevins / Roadcap のいずれについても、顔が識別できる肖像・AI生成の似顔・実写映像・ディープフェイクは全面禁止。**
- Laughman を描く許容表現: **後ろ姿のシルエット／手元だけ／机の向こう側の空席／取調室の椅子とテーブル（無人）／蛍光灯／閉まる鉄扉／指紋カード／供述調書の紙（文字は読めない質感のみ）**。人物像そのものはOK（＝「実在の特定人物と分かる顔」だけが禁止）。
- **サムネにも実在人物の肖像を使わない。**（§9 の3案は全て無人）
- **読める判決文・鑑定書・供述調書を作らない。**とくに **偽の鑑定書ビジュアルは Cayward の主題と紛らわしいので、書式が本物に見える画像は禁止**（S49 は紙の縁と便箋の質感のみ）。
- **AI画像は全カットで AI と開示。**本件は「実在の歴史的場面の再現／実在人物の行動／証拠写真に見える」に該当するため強めに。表記: `AI-assisted visualization` / `Illustrative reenactment`。**1987年の現場・取調室を描く全ショットに常時または区間表示**（下部・字幕帯と縦に離した位置・シルバー `#C8CDD6` 24px）。

### 8.3 中立性

- 警察の欺瞞は**「合法である」と判例に帰属**させる。賛否は「批判者は（Innocence Project、Kassin ら研究者）／擁護者は（Reid and Associates、多数の裁判所）」と両論帰属。
- Frazier の射程についての評価は**法廷意見に帰属**。**無罪＝潔白と言わない。**故意の判断は陪審／裁判所に帰属。

### 8.4 素材権利

- **実写のニュース映像・事件報道映像は使わない**（禁止取得元に該当しうる）。
- 全ビジュアルは **AI生成（source=`ai_sdxl` / `ai_codex`, `commercial_use=allowed`, `sha256`）または商用可ストック**に限定。`05_stock/stock_ledger.v001.json` に**1点1行**で記録。
- 禁止取得元: 通常の YouTube / TikTok / Instagram / X、ニュース番組・TV番組・映画・アニメ・MV・スポーツ映像・まとめサイト・Google画像検索。

---

## 9. パッケージング（タイトル A/B ＋ サムネ3案）

### 9.1 タイトル（≤60字・二人称・フック前置き・A/B 2案）

| 案 | タイトル | 字数 | 狙い |
|---|---|---|---|
| **A** | `Police Can Legally Lie to You. He Got 16 Years.` | 47 | 二人称＋合法性＋代償。勝ち型「警察はあなたに何ができるか」に直撃 |
| **B** | `They Told Him His Prints Were There. There Were None.` | 53 | 具体の嘘そのもの。好奇心ギャップ最大 |

**A/Bの回し方:** A × T1、B × T2 を最初の組にする。T3 は差し替え用。

### 9.2 サムネ3案（1280×720 PNG・UPPERCASE ≤4語・320pxで可読・**実在人物の肖像なし**）

共通: 背景＝黒 or 濃紺 `#0B1A2B`／アクセント＝金 `#E5B53A` または エレクトリックブルー `#1F6BFF`／文字＝白 `#F5F7FA`・シルバー `#C8CDD6`／**被写体が画面高の60%以上**／超高コントラスト／`thumbnail_visibility`（選択サムネの luma平均 ≥33）を通すこと。

| 案 | 視覚要素（具体・数値付き） | テキスト（≤4語） | 色・コントラスト方針 |
|---|---|---|---|
| **T1「存在しない指紋」** ★selected 推奨 | 画面左60%を**巨大な指紋カード**が占める（縦にはみ出す構図・カードの10マスが**すべて空白**）。右上から蛍光灯1灯の硬い光。カード右下に赤の斜めスタンプ **`NO MATCH`**（唯一の赤要素・幅220px・回転 −14°）。背景は黒（luma ≤12）。人物ゼロ。 | **`POLICE CAN LIE`** | カード＝純白（luma 88–94）／背景＝黒（≤12）で最大コントラスト。見出しは金 `#E5B53A`・Anton 128px・黒縁6px。赤は `NO MATCH` の1要素のみ。 |
| **T2「その一言」** | **無人の取調室**を正面から。中央の鋼鉄机に**紙1枚**だけ。上から caged fluorescent 1灯が紙だけを白く飛ばす（紙 luma 90／室内 luma 18）。奥に空の椅子2脚のシルエット。人物ゼロ。 | **`"YOUR PRINTS ARE THERE"`**（4語） | 濃紺 `#0B1A2B` の室内 × 白飛びした紙。見出しは白 `#F5F7FA`・Anton 116px・黒縁6px、下1/3に配置。引用符付きで「これは警察の台詞」だと一目で分かる形にする。 |
| **T3「16年」** | 閉じた**鉄の扉**が画面右65%を占め、左の隙間から朝の光が1本。扉面に **`16`** を彫り込んだようにシルバーで巨大配置（文字高 = 画面高の55%・`#C8CDD6`・エンボス）。人物ゼロ。 | **`IT WAS ALL LEGAL`**（4語） | 黒＋シルバーの2色に絞って320pxでの識別性を最大化。光の帯のみ金。見出しは白・Anton 104px・上部配置（`16` と重ねない）。 |

**出力:** `09_package/thumbnail.v001-01.png` / `-02.png` / `-03.png` ＋ `thumbnail.selected.v001.png`（= T1 の複製）。Remotion `<Still>` 1280×720 でレンダし、**実際に320pxへ縮小して可読性を目視確認する。**

### 9.3 連動Short（縦9:16・35–45秒）

- 同じ問いの30秒版: 「警察は取調べであなたに嘘をついていい。1969年に最高裁がそう決めた。ある男はそれで16年を失った。」
- **CTA は1つだけ＝「続きは本編で」**（登録の直請けをしない）。
- 固定コメントに問いを1つ: `If an officer told you your fingerprints were at a scene — could you check?`
- 概要欄1行目に本編パーマリンク。

---

## 10. 画像プロンプト群（SDXL 30シーン × 3枚 = 90枚発注 / 採用60枚）

`scripts/generate_sdxl_4k.py` の `read_prompts()` が解釈する形式**のみ**を書く（それ以外の行は無視され、その画像は永久に生成されない）:

1. `- ` ＋ バッククォートで囲んだ `*.png` **のみ**の行
2. 次の行がプロンプト本文。**`Avoid:` 以降が negative prompt**

保存先: `episodes/PD-2026-039-frazier/04_scenes/ai_prompts.v001.md`。生成物は `H:\pd-media\assets\ai\frazier\<ID>.png`（1枚目）/ `<ID>_02.png` / `<ID>_03.png` ＋ `remotion/public/frazier/` 直下。**採用分のみ `remotion/public/frazier/img/` へコピー**（QCと depth map はこのフォルダを見る）。

**共通スタイル接尾（`Avoid:` の直前に必ず入れる）:**
```
, cinematic still, dramatic volumetric lighting, moody, deep blacks and navy blue with electric-blue and gold accents, silver highlights, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, film grain, no text, no watermark, no logo
```

**共通ネガティブ（`Avoid:` の直後に必ず入れる）:**
```
text, words, letters, captions, watermark, logo, real celebrity, recognizable real person, identifiable face, portrait, cartoon, low quality, deformed, extra limbs, nudity, explicit, gore, blood, violence, restraint, child, legible document, official letterhead, readable report
```

> ネガティブに `legible document` / `official letterhead` / `readable report` を追加している（v001には無い）。**§8.2 の「書式が本物に見える画像の禁止」を機械的に担保するため。外すな。**

### 10.1 SDXL 生成シーン（30枚・✅）

| ID | 主題 | プロンプト本文（共通接尾の前まで） |
|---|---|---|
| `S01` | 取調室（1987・無人・主舞台） | An empty rural police interrogation room in 1987 at night, one scarred steel table, two facing wooden chairs, a single caged ceiling bulb, painted cinderblock walls stained with damp, a dark observation window, utterly still and oppressive, period-accurate late-1980s fittings, no people |
| `S02` | 閉まる鉄扉（内側から） | A heavy steel interrogation-room door caught in the act of closing, seen from inside the room, a narrowing blade of corridor light across a worn linoleum floor, cold blue outside and dead warm fluorescent inside, the world shutting out, no people |
| `S03` | 検死台のステンレス縁（人体なし） | An extreme close-up of the polished stainless steel edge and drainage channel of an empty autopsy table in a dark morgue, one overhead lamp reflecting along the rim, clinical and utterly restrained, absolutely no body and no tissue, cold and silent |
| `S04` | 実験室のラック（1987血清学） | A rack of glass test tubes and stoppered specimen bottles on a dark laboratory bench in the late 1980s, one warm lamp raking across the glass, faint condensation, analogue instruments out of focus behind, clinical and period-accurate, no people |
| `S05` | 主役の日常（作業机） | A cluttered rural home workbench under a single warm lamp, hand tools and an unfinished repair laid out mid-task, a work jacket over the chair back, late-1980s domestic objects, nobody present, ordinary life interrupted |
| `S08` | 無人の台所（象徴・被害） | An empty rural farmhouse kitchen in the morning, a screen door standing open onto a garden, a small pill bottle lying on the linoleum floor, a chair pushed back, warm morning light against cold shadow, deeply restrained and symbolic, absolutely no people and no disturbance or damage |
| `S11` | 取調室（椅子二脚＋机上の指紋カード） | An empty interrogation table shot from above at a slight angle, two chairs facing each other, a single blank fingerprint record card lying at the centre, one hard overhead lamp, long shadows, waiting and accusatory, no people |
| `S12` | 指紋カード（本作の核・判読不能） | A close-up of a blank ten-print fingerprint record card on a dark steel table, its ruled boxes completely empty, one raking light across the paper fibre, a magnifying loupe resting beside it, all printed wording deliberately blurred beyond reading, symbolic of evidence that does not exist |
| `S13` | 空の照合ファイル | An open manila case folder on a dark desk with nothing inside but one empty transparent sleeve, a cold spotlight, dust suspended in the air, all labels deliberately illegible, stark and minimal |
| `S14` | 主役（匿名・後ろ姿） | A lone anonymous figure seen from directly behind, seated small at a steel table in a vast dark room, shoulders low, head slightly bowed, face entirely out of frame, one hard overhead light, overwhelming institutional emptiness around them |
| `S15` | 扉が閉まる（外側から） | A heavy steel door swinging shut seen from the corridor outside, the lit gap collapsing to a thin line, worn institutional paint and a small dark wired-glass window, finality, no people |
| `S16` | 供述調書の紙（質感のみ） | A stack of typed statement pages fanned across a dark desk under one lamp, every line dissolved into unreadable grey texture, a cheap ballpoint laid across the top sheet, bureaucratic weight, nothing readable anywhere |
| `S17` | 手つかずの窓（外側） | The exterior of a farmhouse sash window at dawn, undisturbed dust and cobweb along the sill, paint intact, a garden reflected in the glass, quiet forensic emptiness, no people |
| `S19` | 試験管ラック（血清学） | A late-1980s serology bench, glass tubes in a metal rack each holding a different pale fluid, handwritten labels blurred beyond reading, one cold overhead tube light, analogue centrifuge behind, clinical, no people |
| `S20` | 標本瓶と綿棒（象徴・非グラフィック） | A single sealed glass specimen jar and a sterile swab tube standing on a dark laboratory bench under one cold light, contents opaque and unreadable, absolutely non-graphic and clinical, symbolic only, no people |
| `S21` | 証言台（無人） | An empty wooden witness stand in a dim 1980s American county courtroom, one shaft of light across the rail and the small swing gate, dust motes suspended, solemn, no people |
| `S22` | 陪審席（無人・12脚） | Twelve empty high-backed wooden jury chairs in two rows in a dim county courtroom, one raking beam of light, worn varnish and brass rail, expectant emptiness, no people |
| `S24` | 検死台の縁（P1回収） | A tight low-angle detail of the rim of an empty stainless autopsy table and a single overhead surgical lamp switched off, cold reflections, extreme restraint, absolutely no body, no tissue, no instruments in use |
| `S25` | 訴状の紙束（判読不能） | A thick bound federal complaint lying closed on a dark desk beside a brass lamp, a blue backing cover, all text and captions dissolved into unreadable grey, one hard side light, institutional and weighty |
| `S26` | 判決の日（1988・カレンダー） | A cheap institutional wall calendar in a dark office, the page curling, one date circled hard in ballpoint, the numbers and month deliberately blurred, harsh side light, the weight of a fixed date, no people |
| `S31` | 取調室（1964・ポートランド） | A 1964 American police interview room, green painted walls, a scratched wooden table, two bentwood chairs, a hooded desk lamp, venetian blind stripes across the wall, period-accurate mid-century fittings, no people |
| `S37` | 抽象「状況の総体」 | An abstract cinematic image of many separate points of golden light falling onto a black still water surface, each ripple spreading and overlapping into a single pattern, symbolic of many circumstances weighed as one whole, minimal |
| `S38` | 現代DNAラボ | A modern forensic DNA laboratory at night, rows of sealed sample tubes in a robotic rack, a thermal cycler glowing faintly, blue instrument light against deep shadow, precise and clinical, no people |
| `S39` | 電気泳動の抽象 | An abstract macro of luminous vertical bands of light on a dark gradient field, evoking a genetic profile readout without any legible text or numbers, cold blue and gold, scientific and beautiful, minimal |
| `S41` | 空の椅子と朝の窓 | A single empty wooden chair beside a bright morning window in a plain room, dust turning in the light, a coat hook empty on the wall, aching quiet absence, no people |
| `S43` | 家系図の抽象 | An abstract cinematic image of fine luminous lines branching across deep darkness and converging to a single bright node, like a family tree drawn in light, no text, no names, minimal and cold |
| `S45` | 空白の20年 | An empty wall of blank unmarked calendar pages in a dim room, edges curling, a bar of daylight crossing them, dust in the air, symbolic of years that left no record, nothing written anywhere, no people |
| `S46` | 数字だけの画面（4,102） | A vast empty dark field with a faint golden horizon glow and drifting dust, deliberately negative space at the centre for a large numeral to be composited, minimal, no text of any kind |
| `S47` | 現代の取調室 | A contemporary interrogation room lit by flat white LED panels, a small wall-mounted recording camera in the upper corner, laminate table and moulded plastic chairs, clinical and bare, no people |
| `S49` | 紙の縁と便箋の質感（Cayward） | An extreme raking macro of the edge and embossed grain of a sheet of official letterhead paper on a dark surface, the printed area entirely out of frame, only fibre, edge and impression visible, absolutely nothing readable, cold and clinical |
| `S50` | 閉じた扉（ENDING） | A closed heavy steel door filling the frame in near darkness, a single thin blade of pale light along its bottom edge, worn institutional paint, absolute finality, no people |

### 10.2 factory 実写で賄うシーン（20点・SDXLを書かない）

| ID | 主題 | `factory_query` |
|---|---|---|
| `S06` | 8月のトウモロコシ畑 | theme `nature_rural` / `corn field`, `farmland summer`, `crops wind` |
| `S07` | 農村の家と庭（朝） | theme `property_home` / `farmhouse`, `rural house morning`, `garden vegetable` |
| `S09` | 1987年式パトカー・夜 | theme `crime_police` / `police car night`, `patrol vehicle`, `emergency lights` |
| `S10` | 田舎の警察署の廊下 | theme `crime_police` / `corridor institutional`, `station interior`, `hallway doors` |
| `S18` | 野菜畑の朝（モチーフ） | theme `nature_rural` / `vegetable garden`, `morning dew plants`, `tomato rows` |
| `S23` | ガラス瓶の並んだ棚 | theme `science_lab` / `laboratory shelf`, `glass bottles`, `specimen jars` |
| `S27` | 州刑務所の外壁・夜 | theme `crime_police` / `prison wall`, `razor wire night`, `institution exterior` |
| `S28` | 1964年の夜の街 | theme `urban_night` / `vintage street night`, `neon 1960s`, `wet asphalt` |
| `S29` | 港と係留 | theme `urban_night` or `nature_water` / `harbor night`, `dock water`, `moored vessel` |
| `S30` | 回転式電話・1960年代の署内 | theme `documents_paper` / `rotary phone`, `vintage office`, `filing cabinet` |
| `S32` | 最高裁 外観 | theme `legal_court` / `supreme court`, `courthouse exterior`, `marble columns` |
| `S33` | 無人の法廷 | theme `legal_court` / `courtroom interior`, `judicial bench`, `empty courtroom` |
| `S34` | 判例集の書架 | theme `documents_paper` / `law books`, `library shelf`, `bound volumes` |
| `S35` | **天秤（本作で1回のみ）** | theme `legal_court` / `scales of justice`, `balance` |
| `S36` | めくれる頁 | theme `documents_paper` / `pages turning`, `book close up`, `paper flipping` |
| `S40` | 開いた鉄扉の外・朝 | theme `property_home` or `legal_court` / `door opening light`, `doorway daylight`, `exit threshold` |
| `S42` | 連邦裁判所 外観 | theme `legal_court` / `federal courthouse`, `government building`, `stone facade` |
| `S44` | 病院の廊下（抑制） | theme `medical` or `urban_night` / `hospital corridor`, `clinic hallway night` |
| `S48` | 州議事堂 | theme `legal_court` / `state capitol`, `government dome`, `legislature building` |
| `S50b` | 現代の街の夜（次回引き） | theme `surveillance_tech` / `city street night`, `surveillance camera` |

### 10.3 生成コマンド（2パス方式・冪等・中断再開可能・**有料APIを一切使わない**）

前提: ローカル A1111 が `http://127.0.0.1:7860` で稼働。

```bash
cd C:/Users/aab15/Documents/prime-documentary

# PASS 1: 全30シーンを1枚ずつ（=30枚）。どこで止まっても「30種類の被写体が揃った状態」を確保する。
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-039-frazier --variants 1

# PASS 2: 3枚まで増やす（+60枚 = 合計90枚）。長辺3840済みはスキップされるので二重生成にならない。
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-039-frazier --variants 3

# 単一シーンだけ作り直す
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-039-frazier --variants 3 --only S12

# 採用分を img/ へ（QCとdepthはこのフォルダを見る）→ depth map（忘れるとレンダが落ちる）
mkdir -p remotion/public/frazier/img
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir remotion/public/frazier/img
```

**不採用基準（1つでも該当したら `img/` に入れない・台帳にも載せない）:** 長辺 <3840px ／ 顔が識別できる（R2違反）／ 判読可能な文字・ロゴ・透かし ／ 四肢の破綻 ／ median luma が極端に低い ／ 同一シーンの他バリエーションと見分けがつかない（**3枚を無理に残さなくてよい**）。

---

## 11. 音の4層設計（v2 row1・row6）

| 層 | 仕様（確定値） |
|---|---|
| **ナレ** | ElevenLabs `VOICE_ID=nPczCjzI2devNBz1zQrb` / `eleven_multilingual_v2` / **stability 0.35 / similarity_boost 0.80 / style 0 / speaker_boost on**。常に最前面。**SAPI / local は出荷禁止**（タイミング下書きのみ）。 |
| **BGM** | 章ごとに1トラック（HOOK / ACT I / ACT II / ACT III / ACT IV / ENDING の6本）。**VO下で −22 LUFS のフロアを割らない（無音まで落とさない）**。無音 >25秒の区間ゼロ。エンディングは尻切れさせず ENDCARD 末で自然減衰。 |
| **SFX** | カット・リビール・数値出現に短いヒット。**AE heroビートのカウント開始（コンプローカル 0.55s）に tick、着地（1.55s）に impact を同期**。指紋カードのリビール（90.3s）と扉が閉まる瞬間（115.9s）に低域インパクト。 |
| **環境音ベッド** | 幕1–2＝取調室（空調のハム・蛍光灯のジー音）／夏の農村（虫・風）。幕3＝1964年の街・法廷のざわめき。幕4＝現代ラボの静電。薄く常時。**沈黙8箇所でもベッドは切らない**（“無音”は語りの停止であって音の停止ではない）。 |

**総合ラウドネス −16 … −12 LUFS**（`LUFS_LO/HI` 実装値）。

---

## 12. 字幕・テロップのゾーン分離（v2 row3/4）

- forced alignment（`faster-whisper` 語タイム）で**語単位**に整列。台本からのコピペ禁止。**音とのズレ ≤120ms**、トークン一致 **≥0.99**（ゲートは0.90だが緩めない）。
- 1キュー = 1息継ぎ群。**≤2行 / 1行 ≤42字 / 1.0s ≤ キュー ≤ 6.0s / キュー間 ≥2フレーム / ≤17cps / 単語割り禁止 / 1語孤立キュー禁止。**
- `.srt` がランタイムの **≥95%** をカバー。
- **ゾーン（一度も重ねない）:** 字幕＝**画面下部帯**（48–60px・白 `#F5F7FA` ＋濃い縁取り＋半透明黒帯 不透明度 55–70%・中央寄せ）／ テロップ見出し `on_screen_text`＝**上部 or 中央**／ 出典テロップ（金ライン `#E5B53A`）＝字幕と**縦に離す**／ AI開示表記＝字幕帯のさらに下または左下隅。
- **SIL-8（676.1–679.1s）は字幕トラックを空にする**（台本の指示「字幕なし」）。

---

## 13. Remotion 実装の確定値

- 本編は `remotion/src/compositions/CaseFilm.tsx`（正典）にデータを与える方式。**EP39専用コンポを作らない。**データ = `remotion/src/data/frazier_film.json`。
- **`op_ed_bookends`（HARD）**: `check_bookends` は `frazier_film.json` の存在を見て **`CaseFilm.tsx` を検査**する。`components/Bookends` の import ＋ `BrandOpening` ＋ `BrandEndcard` の3つが揃っていること。**フォーク・再実装は不合格。`OPENING_SEC=3.5` / `ENDCARD_SEC=9` を変更しない。**
- 1920×1080 / **30fps** / 全クリップを30fpsに統一。
- `remotion.config.ts` は**既に正典値。変更するな**（png / h264 libx264 / crf16 / preset slow / yuv420p / bt709 / aac 320k / 全コア concurrency / angle / **NVENC禁止**）。
- タイトルカード資産 `Frazier39Opening`（1920×1080 / **fps 60** / 180F = 3.0秒 / props `{title, subtitle, accent, hasLogo}`）の**完全仕様は v001 §4.0–4.5 をそのまま使う**（イージング表・レイヤー表・props3種・レンダーコマンド）。これは**本編タイムラインに差し込まない独立資産**（サムネ動画・Short用リード・A/B別レンダ用）なので `op_ed_bookends` に影響しない。props の EP39 既定値のみ差し替える:

| ファイル | title | subtitle | accent | hasLogo |
|---|---|---|---|---|
| `props/frazier_op_a.json` | `THEY CAN LIE` | `FRAZIER V. CUPP · 1969` | `#E5B53A` | true |
| `props/frazier_op_b.json` | `NO SUCH PRINT` | `WHAT THEY TOLD BARRY LAUGHMAN` | `#1F6BFF` | true |
| `props/frazier_op_c.json` | `SIXTEEN YEARS` | `AND EVERY WORD WAS LEGAL` | `#E5B53A` | false |

```bash
cd C:/Users/aab15/Documents/prime-documentary/remotion
npm run studio
npx remotion render Frazier39Opening out/frazier_op_a.mp4 --props=./props/frazier_op_a.json
npm run typecheck
```

---

## 14. 工程分担（誰が何をやるか・明示）

### 14.1 Codex が単体で実装可能（**今すぐ着手・台本は既に確定済み**）

| # | タスク | 成果物 |
|---|---|---|
| C1 | エピソード雛形作成 | `episodes/PD-2026-039-frazier/{03_script,04_scenes,05_stock,06_audio,08_edit,09_package,approvals,events}/` |
| C2 | 確定台本を `03_script/script.en.v001.md` へ配置し、§4.1 の章ラベルで `script.annotated.v001.json` を作る（**ナレ本文は一字も変えない**） | `03_script/script.annotated.v001.json` |
| C3 | §10 の `ai_prompts.v001.md` 作成 → SDXL 90枚生成 → QC → 採用60枚を `img/` へ → depth map | `04_scenes/ai_prompts.v001.md` / `remotion/public/frazier/img/` / `05_stock/stock_ledger.v001.json` |
| C4 | §10.2 の factory 110本ステージング → **全点目視QC（約2h・削るな）** → 90本採用 | `04_scenes/asset_manifest.v001.json` |
| C5 | §9.2 のサムネ3案を Remotion `<Still>` 1280×720 でレンダ＋320px可読性確認 | `09_package/thumbnail.v001-0{1,2,3}.png` ＋ `thumbnail.selected.v001.png` |
| C6 | AEスクリプト2本を新規作成（雛形 = 実在する `scripts/ae/build_kfc_hero_jsx.py` / `composite_kfc_hero.py`。**先に必ず読む**）。レイアウトは A / B / C / D を実装（**E は本作で使わない**） | `scripts/ae/build_frazier_hero_jsx.py` / `scripts/ae/composite_frazier_hero.py` |
| C7 | AEスモークテスト（ダミー1ビート → build → aerender → ffprobe で 1920×1080 / 30fps / 尺を実測） | `08_edit/ae_hero/render/_smoke.mp4` ＋ ffprobe出力 |
| C8 | §13 の `Frazier39Opening.tsx`（v001 §4 の数値どおり）＋ props3種 | `remotion/src/compositions/Frazier39Opening.tsx` |
| C9 | ナレ生成（ElevenLabs・§11）→ **実VO長を測って §2.3 の沈黙再配分を実行** | `06_audio/` ＋ 沈黙配分表 |
| C10 | forced alignment → 字幕3形式 → shotlist → `frazier_film.json`（**`hookSeconds=21.6` / `hookLine` 必須**）→ CaseFilm レンダ → 4層ミックス | `08_edit/frazier_final_bgm.v002.mp4` |
| C11 | hero anchor 解決 → jsx → AEビルド／レンダ → overlay 合成 | `08_edit/frazier_final_bgm.v003_ae.mp4` |
| C12 | HOOK（0–21.6s）を**本編素材から最後に組む** | 完成版 |
| C13 | 全ゲート実行 → `--emit-receipt` | `09_package/acceptance_receipt.v001.json` |

### 14.2 Claude 側（別工程・Codexはやらない）＝ DSPゲート

| # | タスク |
|---|---|
| E1 | **`fact_recheck.v001.json`（claim台帳 C-01〜C-27）の逐語ロック。** C-28 は使用禁止。**Speelman / Holtz / Blevins / Roadcap への言及文言はここで固定し、ナレ確定後に変更しない**（§8.1） |
| E2 | **`EP39_FILM_BIBLE.v001.md`** の作成（コールドオープンの問い・三幕・エスカレート・人間のスルーライン・モチーフ・転回とペイオフ・抑制されたナレ） |
| E3 | **DSPゲートの事前試算**: `motion_density`（38本 / 0.32 / variety 8）と `animation_mix`（still ≤0.30 / motion ≥0.55）が shotlist 設計段階でフロアを超えるかを**レンダー前に**算出する。超えないなら shotlist を直す（レンダ後に直すと作り直しになる） |
| E4 | **`low_motion` 事前監査**: 沈黙8箇所＋長ホールド候補を列挙し、§5.4 のモーション3点が各区間に設計されているかを shotlist 上で確認する |
| E5 | R2 安全レビュー（AI肖像0件・非グラフィック・中立帰属・AI開示表記の全カット確認） |
| E6 | 連動Short の台本＋固定コメント文＋概要欄1行目 |
| E7 | 公開後 72h / 7d / 28d の北極星4指標の記録（CTR / APV / 30秒残存 / subs per 1,000） |

### 14.3 オーナー専管（**唯一の停止点**）

- **YouTube アップロード・公開予約はオーナー操作のみ。** Codex / Claude は完成物とパッケージを用意して**アップロード直前で停止**する。
- 即時停止する例外: 台本／claims の重大な事実誤り、権利・実在人物の肖像リスク、R3 の法務レビュー未了。
- 中間ゲート（ナレ課金・ラフカット・初稿・タイトル/サムネ）では**止まらない**。

---

## 15. 受入チェックリスト（全部緑で package_ready）

- [ ] `structure_4part`（HARD）: 章ラベルが `HOOK`→`OPENING`→`ACT I..IV`→`ENDING` の順。`frazier_film.json` の `hookSeconds=21.6 ≥ 5.0` かつ `hookLine` 非空。
- [ ] promise–payoff: §4.2 の P1–P4 が全て本編に出現。
- [ ] `runtime_band`（HARD）: 690–750秒。設計 705秒。**§2.3 の沈黙再配分を実行済み。**
- [ ] `voice_is_master`: narration provider に `eleven` を含み `sapi`/`local` を含まない。
- [ ] `caption_narration_match ≥ 0.99`（ゲート0.90）／ `.srt` がランタイムの ≥95% ／ キューQC 0違反 ／ ズレ ≤120ms。
- [ ] `bgm_present`: 無音 >25秒なし・VO下でも −22 LUFS を割らない。`loudness` −16…−12 LUFS。
- [ ] `image_resolution`: 使用stillの長辺 ≥3840・NEG違反0。
- [ ] `footage_diversity`: distinct/total ≥0.40（設計0.69）／同一クリップ ≤4回（設計 factory 1回）／汎用シンボル ≤2回（**天秤1回・gavel 0回**）／45秒あたり最低1本の factory（設計90本）／空spanゼロ。
- [ ] `motion_density`: ≥2.5 beats/分（設計3.2＝38本）／coverage ≥0.25（0.32）／variety ≥3（8）。
- [ ] `animation_mix`: still share ≤0.45（0.30）／motion coverage ≥0.45（0.55）／5秒超の静止保持 ≤8（0）／opening合計 ≤12秒。
- [ ] **`low_motion`: 準静止 ≤10%（設計 ≤6%）／単一スパン ≤3.0秒。★沈黙8箇所すべてに §5.4 の3点モーションが入っていることを実レンダで確認。**
- [ ] `op_ed_bookends`（HARD）: `CaseFilm.tsx` が `components/Bookends` を import し `BrandOpening` / `BrandEndcard` を使用。
- [ ] `thumbnail_present`: 1280×720 PNG ≥3枚 ＋ selected 1枚。`thumbnail_visibility`: selected の luma平均 ≥33。見出し ≤4語。320pxで可読を実測。
- [ ] タイトル ≤60字・A/B 2案（§9.1）。
- [ ] **AE heroビート 8本が SKIP されずに合成された**（コンポジタのログで確認。1本でもSKIPなら原因を潰して再合成）。
- [ ] **合成後の `v003_ae.mp4` に対して** `check_final_acceptance.py 39 --emit-receipt` が exit 0、`video_sha256` 一致の receipt を発行。
- [ ] R2安全: AI肖像0件・グラフィック表現0件・読める偽書類0件・AI開示表記が該当全ショットに存在。

---

## Codex 引き継ぎプロンプト（そのまま貼る）

```
あなたは Prime Documentary EP39 の実装担当です。リポジトリは
C:\Users\aab15\Documents\prime-documentary です。

# 唯一の仕様書
episodes/_planning/EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md
※ v001 は古い（主役未確定の前提で書かれており主舞台・数値・シーン割りが確定台本と一致しない）。
   v002 が勝つ。ただし v002 が「v001 §3.1/§3.3/§3.6/§4 を参照」と書いている箇所だけは
   v001 の該当節を読んで使うこと。
全ての数値・レイアウト・イージング・パス・契約は設計書に書いてある。書いていないことを
推測で決めない。曖昧だと感じたら「推測して進める」のではなく、その場で停止して報告する。

# 確定台本（一字も変更禁止）
episodes/_planning/EP39_frazier_script.en.v001.md（見出しは script.en.v002）
ナレ本文・語順・句読点を変えない。【OST】行と[演出指示]行はナレーションではない（TTSに渡さない）。
実発話語数は 1,976語 = 665.7秒 @178.1wpm。尺ゲートが出す 2,136語 は OST を含む別の数え方。

# 受入契約（最初に読む・これを満たさない限り "done" と言わない）
docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md の row1..row16。最終検証は必ず自分で実行し exit 0 を確認:
  ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 39 --json
  ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 39 \
    --render episodes/PD-2026-039-frazier/08_edit/frazier_final_bgm.v003_ae.mp4 --emit-receipt
自作の品質ゲートを書いて「合格」と宣言しない。既存の check_*.py の測定結果のみが合否。
GATE を緩めて通すのも禁止。

# ★この作品で最も落ちやすい3点（設計書 §0.1 / §2.3 / §5.4）
1. low_motion（HARD）: LOW_MOTION_MAX_SPAN_S = 3.0。本作は SILENCE が8箇所あり最長 4.0秒。
   「静止画を置いて音を止める」実装は必ず落ちる。設計書 §5.4 の3点（連続ドリー / 粒子・光の
   合成レイヤー 12-18% / グレイン＋ヴィネット呼吸）を全沈黙区間に必ず入れる。
2. runtime_band（HARD）: 設計 705秒に対しフロア 690秒まで余裕15秒しかない。ナレ生成後に
   実VO長を測り、設計書 §2.3 の式で沈黙総量を再配分する。VO が 610秒未満なら停止して報告。
3. structure_4part（HARD）: 章ラベルは HOOK / OPENING / ACT I..IV / ENDING で始める文字列。
   加えて remotion/src/data/frazier_film.json に hookSeconds=21.6 と hookLine
   "Every word of that was invented, and every word of it was legal." が必要（両方無いと FAIL）。
   ※フックの「6-10秒」という上限はゲート実装には存在しない。21.6秒の確定フックを削るな。

# 着手順
 1. episodes/PD-2026-039-frazier/{03_script,04_scenes,05_stock,06_audio,08_edit,09_package,
    approvals,events} を作成。確定台本を 03_script/ へ配置し script.annotated.v001.json を作る。
 2. 設計書 §10 のとおり 04_scenes/ai_prompts.v001.md を書き（SDXL は ✅ の30シーンだけ）、
    2パス方式で90枚生成 → QC → 採用60枚を remotion/public/frazier/img/ へ → gen_depth_maps.py。
    ★共通ネガティブに legible document / official letterhead / readable report を必ず含める。
 3. 設計書 §10.2 の factory 20テーマを 110本ステージングし、全点を目視QCする（約2時間・削るな）。
    factory のファイル名とサブタイプは信用できない（EP36で大聖堂、EP38で牛の実例）。
    R2 なので「顔が識別できる人物が大きく写っているクリップ」も除去する。
 4. 設計書 §9.2 のサムネ3案を Remotion <Still> 1280x720 でレンダ。実際に320pxへ縮小して可読確認。
 5. 設計書 §13 の Frazier39Opening.tsx を v001 §4 の数値どおりに実装（fps=60 / 180F / props 4種）。
    既存の compositions/Opening.tsx と components/Bookends.tsx は書き換えない・フォークしない。
 6. AE: scripts/ae/build_frazier_hero_jsx.py と composite_frazier_hero.py を新規作成。
    雛形は実在する scripts/ae/build_kfc_hero_jsx.py と composite_kfc_hero.py。必ず先に読む。
    レイアウトは A_BIG_NUMBER / B_SPLIT_RATIO / C_PERCENT_ARC / D_CITATION_STAMP を実装
    （E_VOTE_TALLY は本作で使わない＝Frazier の票数は台帳に無く、書けば捏造になる）。
    スロット8本の値は設計書 §7.1 の表そのまま。start は null で出し anchor_phrase で解決する。
    anchor が語タイム列に0件または2件以上ヒットしたら推測で置かず FAIL を返して停止。
 7. ナレ生成 → §2.3 の沈黙再配分 → forced alignment → shotlist → frazier_film.json →
    CaseFilm レンダ → 4層ミックス(v002) → hero 合成(v003_ae) → HOOK を最後に組む → 全ゲート → receipt。

# このマシン固有の罠（AE。設計書が参照する v001 §3.6 の15項目を全部守れ）
 - AE 2026・日本語ロケール・RTX4090。実行体は
   /c/Program Files/Adobe/Adobe After Effects 2026/Support Files/ の AfterFX.com と aerender.exe。
 - setTemporalEaseAtKey は Position など spatial プロパティでは要素1個の配列。
   dim = prop.isSpatial ? 1 : (value.length||1)。間違えるとイーズが無言で効かず等速になる。
 - RS/OM テンプレ名はローカライズ済み。有効値は RS "最良設定" /
   OM "H.264 - レンダリング設定を一致 - 15 Mbps"。英語名は失敗する。
 - AE の TextDocument の改行は \n ではない。字幕は必ず1行に保つ（one_line(maxchars=50)）。
 - app.newProject() は headless(-noui) でハングする。使うな。既存の同名コンプを防御的に削除する。
 - ビルドは遅い(~100-120秒)がレンダは速い(6コンプ~21秒)。jsx が書く完了マーカーを
   ポーリングせよ。早期killするな。jsx の末尾で必ず app.quit()。
 - layer.motionBlur はレイヤー個別に設定が必要（コンプのスイッチだけでは無効）。
 - 2Dレイヤーの "ADBE Rotation" は null。"ADBE Rotate Z" を使え。
 - inPoint だけ設定すると outPoint がコンプ末尾に残る。両方設定せよ。
 - item.mainSource.conformFrameRate = 30 が無いと全ビートの timing が無言でズレる。
 - proj.gpuAccelType = GpuAccelType.SOFTWARE / proj.bitsPerChannel = 8 を try/catch で設定。
 - aerender の前に taskkill //F //IM AfterFX.com と //IM AfterFX.exe で残骸を落とす。
 - 数値カウントの全キー文字列は Python 側で事前計算する（JS側で整形しない）。
 - 出荷済み mp4 を絶対に上書きしない（出力は *_v003_ae.mp4）。音声は -c:a copy。

# R2 安全（絶対・例外なし。設計書 §8）
 - Barry Laughman / Edna Laughman / Christopher Speelman / Holtz / Blevins / Roadcap の
   顔が識別できる肖像・AI似顔・実写・ディープフェイクを作らない/使わない。サムネにも使わない。
 - 人物は後ろ姿・シルエット・顔が画角外・手元のみ・遠景の小さな人影に限る。
 - 性的暴行・暴力・拘束の描写を一切しない。象徴のみ（無人の台所、開いた網戸、床の錠剤の瓶、朝の庭、
   閉まる鉄扉、空の椅子、検死台の縁だけ）。
 - 読める判決文・鑑定書・供述調書を作らない。とくに書式が本物に見える偽鑑定書は禁止
   （Cayward の主題と紛らわしい）。
 - 1987年の現場・取調室を描く全ショットに AI 開示表記
   （AI-assisted visualization / Illustrative reenactment）を入れる。字幕帯と縦に離す。
 - Holtz/Blevins/Roadcap は「訴状の主張」であって認定事実ではない。断定しない。
 - ニュース映像・事件報道映像を使わない。全素材は AI生成 か 商用可ストックのみ。
   05_stock/stock_ledger.v001.json に1点1行（source, commercial_use=allowed, sha256）。

# 禁止
 - YouTube へのアップロード・公開予約をしない（オーナー専管）。完成物を用意して停止する。
 - 有料APIを使わない（画像はローカル A1111、i2v はローカル ComfyUI）。ナレのみ ElevenLabs。
 - 確定台本のナレ本文を編集しない。
 - 実在しないスクリプト名・テンプレ名を使わない。使う前に必ずファイルを読んで実在を確認する。
 - 紙芝居・左右の縦スイープライン・全画面の黄/金ウォッシュ・ズーム/パンのみ・リニアイージング・
   opacity単独の演出。

# 完了報告に必ず含めること
 1. 作成/変更したファイルの絶対パス一覧
 2. 実VO長（秒）と §2.3 で再配分した沈黙8箇所の実値、最終ランタイム
 3. 生成画像の枚数・長辺の最小値・QC不採用件数と理由の内訳
 4. factory 目視QCの結果（ステージング本数 / on_theme:false にした本数と理由）
 5. AE hero 8本それぞれの anchor 解決結果（start秒）と、SKIP が0件であることの合成ログ
 6. サムネ3案のパスと320px縮小での可読性確認結果
 7. check_final_acceptance.py 39 の全チェック結果（JSON）と receipt の video_sha256
 8. low_motion の実測値（準静止割合・最長スパン秒）と、沈黙8箇所それぞれの実測差分
```
