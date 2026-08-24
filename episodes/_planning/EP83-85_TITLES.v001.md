# EP83–85 TITLES v001 — CTR最大化の実測ルールで書いた候補

**Built 2026-08-25. Status: DRAFT.** 全タイトル**○未検証** — 台本完成後に
`check_packaging_claims.py` を通すまで1本も確定しない（虚偽タイトル2本が機械ルール全通過した前歴）。

## 適用した実測ルール（全て測定済み・出典つき）

| ルール | 実測 | 出典 |
|---|---|---|
| 検索される事件名を入れる | impressions約2倍(690 vs 366) | TOPIC_POOL_500 §0.5 |
| died/killed/deaths を書かない | 競合0.06×・自CH CTR 1.09% vs 1.68% | 同上 |
| 権力を主語に開く(Boeing/The Court/The FAA…) | CTR 2.12% vs 1.47% | TOPIC_POOL_500 冒頭 |
| 2文構成（前提。裏切り。） | CTR 1.79% vs 1.25% | 同上 |
| コロン・emダッシュ・疑問形・you・ALLCAPS語を避ける | 0.34×/0.43×/0.83×/0.44×/0.45× | CTR_PLAYBOOK v002 §2 |
| 60字超を恐れない | 自CH 81字+でCTR 1.92% | TOPIC_POOL_500 §0.5 |
| 結末の判決・数字をサムネ文字と重複させない | 分業原則 | ship-gate |

## EP83 — Boeing 737 MAX

| # | 候補 | メモ |
|---|---|---|
| **A★** | **Boeing Knew the 737 MAX Could Do This. The Pilots Were Never Told the System Existed.** | 権力主語・2文・事件名・89字。映画の背骨 |
| **B★** | **The FAA Let the 737 MAX Keep Flying After the First Crash. It Fell Again in 19 Weeks.** | 規制側の物語。○「19週間」要台帳検証 |
| C | The System That Brought Down Two 737 MAX Jets Was Left Out of the Pilot Manual. | 1文型の保険 |
| D | Boeing Called the 737 MAX Fix a Software Update. Every Country on Earth Grounded It. | スケール型 |
| E | Two 737 MAX Crews Fought a System They Did Not Know Was on Board. | 人間側の保険 |

## EP84 — Three Mile Island

| # | 候補 | メモ |
|---|---|---|
| **A★** | **The Safety Tests at Three Mile Island Were Being Faked Before the Meltdown.** | 核心の矛盾そのまま。○刑事記録(1984 Met-Ed答弁)と照合必須 |
| **B★** | **The Operators at Three Mile Island Followed Their Training. The Training Was Wrong.** | 2文・人vs制度の逆転 |
| C | A Stuck Valve at Three Mile Island Lied for Two Hours. The Control Room Believed It. | ○「2時間」要検証 |
| D | The Utility at Three Mile Island Was Convicted of Faking Safety Records. No One Went to Prison. | 法廷を正面に。○要検証 |
| E | Three Mile Island Was Melting Down While the Gauges Said It Was Not. | 1文型の保険 |

## EP85 — Katrina堤防決壊

| # | 候補 | メモ |
|---|---|---|
| **A★** | **The Court Ruled the Levees Sank New Orleans. A 1928 Law Says No One Can Be Sued.** | 権力主語・2文・映画の結末の矛盾。○In re Katrina Canal Breaches の判示表現と照合必須 |
| **B★** | **Katrina Missed the Worst of New Orleans. The Levees Are What Sank the City.** | 最強の裏切り。○「missed」の言い過ぎ判定は台帳次第（減衰上陸＋越流でなく構造破壊、の線） |
| C | Engineers Warned for Years the New Orleans Floodwalls Could Fail. The Builder Cannot Be Sued. | 警告×免責 |
| D | The Floodwalls in New Orleans Fell Below Their Design Storm. The Law Shields Their Designer. | 技術に寄せた保険 |
| E | The Levees Failed Before Katrina's Worst Arrived in New Orleans. | 1文型の保険 |

## 分業の予約（サムネ文字が使えなくなる数字）

タイトルA/B確定後、その数字・事実はサムネ文字で**使用禁止**になる。予約表:
- EP83: A/B確定なら「19 weeks」「two crashes」系はサムネ不可 → サムネはモノ側（TRIM WHEEL/ONE SENSOR系）へ。
- EP84: 「faked tests」をタイトルに使うならサムネは「2:00 AM」「ONE VALVE」系へ。
- EP85: 「1928」をタイトルに使うならサムネは「17TH STREET」「THE WALLS」系へ。

## 次の工程

1. オーナー: 各話 A/B ペアの仮承認（本承認は台本後の claims PASS が条件）。
2. 台本完成 → `check_packaging_claims.py --title --thumb-text` → ペア承認ゲート → 確定。
