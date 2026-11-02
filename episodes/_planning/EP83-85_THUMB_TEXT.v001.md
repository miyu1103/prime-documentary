# EP83–85 THUMB TEXT v001 — winnerスタイルの文字と構成（プレート生成と並行）

**Built 2026-08-25. Status: DRAFT.** 数字を含む見出しは全て**○未検証**（FACTS_LEDGER成立後に
`check_packaging_claims.py --thumb-text` PASSが確定条件）。プレート納品後の目視QCで
勝ちプレートを選んでから `config/thumbnails/<slug>.json` に書き写す。

## 0. 様式（正典 = build_case_thumbnails_from_plates.py の style:"winner"）

- **2〜3語の縦積み・全大文字・Anton・アクセント1語（赤・accent_line指定）・行幅実質7文字**
- 文字背後に**暗プール＋グロー**（スクリプトが自動描画）
- **150px文字ゲートは意図的に不適合のまま**（勝者実測94px。直そうとしない）
- 配置は各プレートの設計済み空き（下表side）。顔があるプレートでは**顔に文字を被せない**

## 1. 設計原理 — 「サムネが問い、タイトルが答える」

タイトル（確定済みv004）が**答え**（Boeingは知っていた/検査は改竄/免責）を言うので、
サムネ文字は**問いと違和感**だけを言う。同じ事実の重複は分業違反かつクリック理由の消滅。
- 使用禁止語（タイトル由来）: EP83 KNEW/NEVER TOLD系 · EP84 FAKED系/WORST MELTDOWN ·
  EP85 JUDGE/IMMUNE/SUE/NEGLIGENT系
- **訂正**: TITLES v004の分業予約に「2:00 AM」とあるのは誤り。TMI事故開始は**4:00 AM○**。
  本書で「4 A.M.」に置き換える（○一次資料照合必須）。

## 2. EP83 — 737 MAX

**A/B 3枠の第一候補**（プレートの出来で入れ替え可）:

| 枠 | 見出し（縦積み） | accent | 想定プレート | side | 狙い |
|---|---|---|---|---|---|
| 01 | **WHO IS / FLYING?** | FLYING? | T01 夜のコックピット警告灯 | top | 操縦者は誰か=映画の芯。質問形は自CH勝者(YOUR DOOR? 4.48%)の型 |
| 02 | **IT / PUSHED / BACK.** | PUSHED | T02 トリムホイール | left | 機械が抗った、の違和感。事実断定なし=claims安全 |
| 03 | **ONE / SENSOR.** | ONE | T04 AoAベーン | left | 物の1枚。単一センサー依存○要台帳 |

**全プレート割り付け**（QCで上3枚が死んだ時の代替）:

| plate | 見出し | accent | side | claims |
|---|---|---|---|---|
| T03 機列 | ALL OF / THEM. | ALL | bottom | 世界一斉停止○ |
| T05 シミュレータ | NOT / TRAINED. | NOT | upper-left | ○訓練不要販売の言い換え。タイトル被り注意=保留気味 |
| T07 パイロットの顔 | WHOSE / PLANE? | WHOSE | left | 質問形・安全 |
| T08 尾翼 | (文字なし枠のまま保留) | — | — | 弱プレート想定 |
| T09 ゲートの窓 | STILL / BOARDING. | STILL | top | 停止前の日常の不気味さ・断定なし |
| T10 レコーダー | IT WAS / ALL / THERE. | ALL | left | 記録は語っていた○ |

## 3. EP84 — Three Mile Island

| 枠 | 見出し | accent | 想定プレート | side | 狙い |
|---|---|---|---|---|---|
| 01 | **4 A.M.** | 4 A.M. | T01 警報の壁×シルエット | bottom | 時刻1つの最小フック（勝者3.2 METRES型）○開始時刻要照合 |
| 02 | **THE / GAUGES / LIED.** | LIED. | T05 振り切れた記録計 | left | 計器が嘘をついた=タイトルの改竄とは別の事実○ |
| 03 | **STAY OR / GO? ** | GO? | T07 避難のテールランプ | upper-left | 住民の問い。避難勧告の混乱○ |

| plate | 見出し | accent | side | claims |
|---|---|---|---|---|
| T02 警報タイル | NO / LIGHT. | NO | right | 弁位置の表示灯が無かった○ |
| T03 川向こうの塔 | NEXT / DOOR. | NEXT | top | 暮らしの隣、の違和感・断定なし |
| T04 台所の母 | STAY OR / GO? | GO? | left | 03と同文の顔あり版 |
| T06 クリップボード | (保留=改竄系はタイトル領域) | — | — | 分業違反リスクで文字なし |
| T08 電話ボックス | WHO DO / I CALL? | WHO | right | 質問形・安全 |
| T09 会見場 | UNDER / CONTROL. | CONTROL. | top | 皮肉引用○広報発言の照合 |
| T10 バルブ | ONE / VALVE. | ONE | left | 1つの弁○ |

## 4. EP85 — Katrina堤防決壊

| 枠 | 見出し | accent | 想定プレート | side | 狙い |
|---|---|---|---|---|---|
| 01 | **NOT THE / STORM.** | NOT | T01 水没した通りの夜 | top | 映画の反転を問いの形で。タイトルが「では何か」に答える |
| 02 | **BELOW / DESIGN.** | BELOW | T02/T09 破られた壁・越流 | left | 設計水位未満で壊れた○ILIT照合 |
| 03 | **THEY / NEVER / MOVED.** | NEVER | T04 スクールバスの列 | left | 使われなかったバス○ |

| plate | 見出し | accent | side | claims |
|---|---|---|---|---|
| T03 屋根のシルエット | STILL / WAITING. | STILL | top | 断定なし |
| T05 屋根裏の光 | (文字なし推奨) | — | — | 文字を載せると遺体連想が立つ |
| T06 設計図の机 | ON / PAPER. | PAPER. | right | 失敗は紙の上に既にあった・断定なし |
| T07 水位線の手 | SIX / FEET.（○実測水位次第） | SIX | top | 数字は台帳成立まで仮 |
| T08 スーパードーム | NO WAY / OUT.は禁止(恐怖煽り)→ INSIDE. 単語1枚 | INSIDE. | bottom | 慎重枠 |
| T10 ランタンの手 | STILL / HERE. | HERE. | left | 残った人・断定なし |

## 5. 分業チェック（機械照合の予告）

タイトルv004の語幹（boeing/knew/737max/pilots/told/system/utility/faking/safety/tests/meltdown/
katrina/judge/corps/negligent/flooding/court/immune）と本書の全見出し語幹は**交差ゼロ**を維持する。
config化の際に `check_packaging_claims.py --title --thumb-text` を両方掛けて機械確認。

## 6. 工程（プレート納品後）

1. 目視QC（コンタクトシート）→ 各話の勝ちプレート3枚選定
2. 台帳照合: ○付き見出し（4 A.M. / ONE SENSOR / BELOW DESIGN / THEY NEVER MOVED / SIX FEET等）
   はFACTS_LEDGER成立まで**仮**。落ちたら同表の断定なし見出しに差し替え
3. `config/thumbnails/max737.json / threemile.json / katrina.json` を書く（下書き雛形）:

```json
[
  {"plate": "T01.png", "style": "winner", "headline": "WHO IS FLYING?",
   "lines": ["WHO IS", "FLYING?"], "accent_line": 1,
   "provenance": "EP83 record (claims PENDING): MCAS operated without pilot knowledge"}
]
```

4. ビルド → 320px縮小で目視 → タイトル×サムネのペア承認（オーナー）→ 09_package確定
