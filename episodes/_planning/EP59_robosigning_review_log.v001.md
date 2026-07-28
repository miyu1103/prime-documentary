# EP59 `review_log.v001` — 台本レビュー記録（R1 FACT AUDIT + R2 CRAFT/RETENTION AUDIT + R3 プレースホルダ）

**Subject:** `EP59_robosigning_script.en.v001.md`（narration 実測 **4,675語** · オーナー帯 4,600–4,750 内）+ `EP59_robosigning_FACTS_LEDGER.v001.md`（RS-01〜RS-88）
**Reviewer:** Claude（左工程）R1/R2。**R3 は未実施（本ログ末尾のプレースホルダ参照）。**
**根拠:** `DEEP_RESEARCH_FINDINGS.v001.md`（MUST 群）、`TOPIC_PIPELINE.v004.md` §2 EP59 / §6 / §7、`EP59_robosigning_DESIGN_ARCHITECTURE.v001.md` §6、FACTS_LEDGER のガードレール、`pd-craft-checklist`（26項目）。

## R1 — FACT AUDIT（台本の全 load-bearing 主張 × 台帳の行単位照合）

**方法:** 3本の並行 web 検証（2026-07-29）＋**一次資料の直接取得と局所解析**。取得できた一次資料: 連邦準備制度理事会の *Independent Foreclosure Review Payment Agreement Details*（2013-04-09・PDF を落として表を1セルずつ加算）、Fed *Independent Foreclosure Review Final Report*（2019-08・PDF 全文抽出）、Fed enforcement release（2011-04-13）、Fed press release（2013-01-07 / 2013-04-17）、**GAO-14-376**（2014-04-29・PDF 全文抽出）、**GAO-26-108448**（2026-01-27 発行 / 2026-02-09 公表・PDF 取得）、Congressional Oversight Panel 報告（2010-11-16・127頁 PDF）、**Jeffrey Stephan の宣誓供述録取の PDF 実物2種**、**連邦地裁ドケット（D. Mass.）の docket XML と訴状本体 PDF**、Florida AG 経済犯罪課プレゼン全文、Nevada AG プレスリリース PDF、CBS News の *60 Minutes* トランスクリプト、CFPB の 2023-04-26 / 2025-01-17 公表物、NCLC の資料・係属中クラスアクションのケースページ、Washington 州 AG（2013-06-03）と New Jersey 州 AG（2013-06-04）のプレスリリース。

**検証で判明し、台本・台帳・DESIGN に反映済みの重要訂正（発注ブリーフとの差分）。ブリーフの記述をそのまま書いていたら、いずれも画面に誤りが出ていた。**

1. **Lorraine Brown の量刑日は 2013-06-25。ブリーフの「November 2013」は誤り。** 2012-11-20 は**有罪答弁**の日であって量刑日ではない。刑期は5年＋監督付き釈放2年＋罰金15,000ドル、Middle District of Florida、Henry Lee Adams Jr. 上級判事（RS-40）。
2. **Linda Green は元 Wells Fargo 職員ではない。** *60 Minutes* の逐語は「In 2003, she was a shipping clerk for auto parts」。銀行で働いたことは一度もなく、彼女の名前が Wells Fargo の書類に**載せられた**だけ。ブリーフの記述をそのまま使えば実在の一般人に関する事実誤認を放送していた（RS-31）。
3. **60 Minutes は Linda Green にインタビューしていない。** トランスクリプト逐語:「The real Linda Green didn't want to be interviewed.」出演したのは Chris Pendley と Shawanna Crite。台本は「彼女が語った」ではなく「彼女は取材を断った／制作陣に語った内容として番組が伝えた」枠でしか書かない（RS-36）。
4. **Florida AG プレゼンの作成者は3名**（June M. Clarkson, Theresa B. Edwards **and Rene D. Harrod**）。ブリーフは2名（RS-35）。
5. **Nevada の「10万件以上の notice of default」は不支持。** Nevada AG 自身の文言は「tens of thousands」。**F 判定＝使用禁止**（RS-45）。
6. **「コンサルタントに20億ドルが支払われた」は一次資料にない。** GAO の実文言は「**完了までに残る**コンサルタント費用が**少なくとも20億ドル**と見積もられた」。すでに支払われた額ではない。台本は GAO の言い回しのまま「終わらせるのに、あと最低20億ドルかかると告げられた」に書き換え済み（RS-70）。
7. **IFR の「最終」数値は3種類あり、母集団が違う。** $8.5bn（2013-01-07・10社）／$9.3bn＝$3.6bn+$5.7bn（13社・小切手発行時点）／最終 $3.9bn 現金・約440万人・15社。**$300 の比率を語るときだけ「390万人」を使う**（RS-65/RS-66/分母規律）。
8. **「2.36 million of 3.9 million が $300」は正確。** Fed が 2013-04-09 に公表した支払区分表を1セルずつ加算して **2,358,441 / 3,949,896 = 59.7%** を独立に再現した。台本の数値はこの再計算に基づく（RS-66）。
9. **不渡り小切手の件数は存在しない。** Fed は件数を公表しておらず、どの一次資料にもない。台本は「一部は換金できなかった」と書き、**件数を出さない**。代わりに GAO が数えている別の誤り（約96,000件の過少支払い・翌月約4,500万ドルで是正）を使う（RS-69）。
10. **「差押えのうち何件が偽造書類だったか」という数字は存在しない。** これは欠落ではなく**発見**であり、三つの一次根拠（IFR がファイルの約14%しか最終レビューされずに打ち切られた／代替の支払いは被害の有無を問わず行われた／唯一の定量的な代理指標である OCC の6.5%は「サービサーのあらゆる過誤による金銭的被害」であって書類偽造率ではない）で支えられる。**6.5% を robo-signing 率として提示しない**（RS-76）。
11. **CFPB の現状は「hollowed out」と自分の声で断定しない。** 記録（予算上限の半減・stop-work order・監督検査の終了・エンフォースメント案件の打ち切り・大多数への RIF 通知）を述べ、**その状態が連邦裁判所の差止めで係属中である**ことまで書く。GAO 自身が「CFPB は GAO との面談を拒否し、資料を提供しなかった」「草案に対し正確性への懸念を述べたが、どの事実が誤りかは示さなかった」と記録しており、2026年の像は**確定ではなく係争中**である（RS-86/RS-87）。
12. **2024–2026 の robo-signing 再発は「見つからなかった」であって「存在しない」ではない。** 検索予算が尽きたため、台本は「再発していない」と**言わない**。現在時制の類例としては zombie second mortgage の係属中クラスアクションを指す（RS-88/RS-84）。

---

## R2 — CRAFT / RETENTION AUDIT（`DEEP_RESEARCH_FINDINGS.v001` の MUST 群をネイティブ検査）

### R2-1 尺・語数ゲート（実行出力・2026-07-29）
```
$ ./.venv/Scripts/python.exe scripts/check_script_length.py --lo 1740 --hi 1860 episodes/_planning/EP59_robosigning_script.en.v001.md
PASS script_length: 4,675 words (need 3,973-5,309)
  narration estimate  slow 28.6m | median 26.2m | fast 19.7m
  target band         29.0-31.0 min
  ! RISK: at the fast end of the measured pace (237.4 wpm, seen on williams/florence) this lands at 19.7 min -- under the floor. Either pin the voice speed or write to 6,885 words.
```
- narration 本体実測（COLD OPEN→ENDING・ゲート同一 regex・ヘッダ/OST/appendix 除外）= **4,675語** → オーナー帯 4,600–4,750 内。
- RISK 行への処置: EP55/EP56 と同一 — Brian 正典設定（stability≈0.35 / similarity≈0.80 / style 0 / speaker_boost on）で fast 端は実績帯 167–182 wpm に入る。**TTS 実測後に durationInFrames を再ロック**（DESIGN §5 の re-lock 手順・EP55 は −71.2s、EP56 は −71.8s ドリフトした）。

### R2-2 Opening formula v2（FINDINGS R-7..R-13 — 実測）
| 項目 | 判定 | 証拠 |
|---|---|---|
| 第1文 = 宣言文・人物+固有具体+不可逆な出来事 | **PASS** | "On the ninth of January 2010, Charlie Cardoso stood outside a house in Spring Hill, Florida, and cut the padlocks off his own front door." — 人物名は word 6 ≈ **2.0秒**、疑問文でない、"This is the story of" なし、抽象語なし |
| 人物名 ≤0:15 / 対立勢力 ≤0:28 | **PASS** | Cardoso ≈0:02；"Bank of America's crews had come the previous summer" = word 55 ≈ **0:18** |
| BUT-loop がスティング前（~0:32） | **PASS** | "But nobody caught the mistake, because catching it would have meant reading something." = words 108–124 ≈ **0:36–0:42**…**⚠ 実測で 0:32 をわずかに超える**（下の是正参照） |
| Brand sting ≤5s・audio-continuous・loop後 | **PASS（設計値）** | 台本に §BRAND STING を明示（gold Bookends の ≤5s cut・title line 融合）— ビルドで sting 実測 ≤5.0s を検証（DESIGN §5） |
| Post-brand = 1エスカレーション文＋日付/場所アンカー | **PASS** | 60語・"more than a million sworn documents…no one has ever counted" 1文 → "New Bedford, Massachusetts, 2005." |
| First-45s 禁止事項 | **PASS** | subscribe/自己紹介/スポンサーなし。新具体は 2–6 秒ごと（9 Jan 2010／Spring Hill／$139,000／cash／five years／no mortgage／the previous summer／the listing agent／across the street／ten doors down／10,000 a month） |

**⚠ 正直な偏差1件と是正:** cold open は **170語 ≈ 57秒**あり、BUT-loop が **≈0:36–0:42** に落ちる。FINDINGS は「~0:32 までに loop、その直後に ≤5s sting」を求めており、**実測は 4–10 秒遅い**。**是正はビルド側で行う**（DESIGN §5 の指示）: sting を **0:40–0:45** に置き、post-brand の1文を 0:45–0:57 に収める。cold open 自体を切り詰めて loop を 0:32 に前倒しする案は、**「自分の家の鍵を切っている男」という不可逆イベントの提示に必要な具体（現金・住所違い・読まれていない）を落とす**ため採らない。**この偏差は記録として残す（隠さない）。**

### R2-3 60–180s explanation-block スキャン（FINDINGS R-2 — 本作最大のリスク）
60s≈word 178 〜 180s≈word 534 を逐語で通読し、**段落ごとに person-action-free の連続秒数を測った。**

| 位置 | 秒 | 語数 | 内容 | 判定 |
|---|---|---|---|---|
| post-brand | 54–74s | 60 | 1文のエスカレーション＋場所/年アンカー | 具体のみ |
| ACT I 冒頭 | 74–100s | 79 | 2人の名前・都市・購入・住所・金額（**人の行為**） | OK |
| "what cash means" | 100–138s | 111 | **★初稿で 127語/43秒の純説明ブロックだった。書き直して人の行為に接着**: "When the Cardosos paid cash…" → "a deed, signed at a closing table and then carried into the Hernando County recorder's office and stamped by a clerk" → "Anyone in Florida could have walked into that building, asked at the counter…"。抽象のみの連続は冒頭4文＝**約45語/15秒** | OK（<20s） |
| tenant の電話 | 138–153s | 46 | テナントが電話し、3人が来て、家を空にして施錠（**全て行為**） | OK |
| 適正な差押えとは | 153–171s | 54 | **EP33 の矛盾を名指しする1ブロック＝18秒**。前後を行為の段落で挟んでいる | OK（<20s） |
| Charlie が電話 | 171–192s | 60 | ¶11 の行為 | OK |

**≥20秒の person-action-free 連続ブロック = 0。** **securitisation / MERS / assignment chain は台本に一語も出てこない**（連鎖の説明は AE-12 のダイアグラムへ外部化・DESIGN §3）。**初稿は R-2 に違反していた。測って、直した。**

### R2-4 Reveal LADDER 実測位置（FINDINGS R-14・語オフセット）
```
  0.0%  cold-open shock（自分の家の鍵を切る・解決前カット）
 15.2%  ACT II
 16.2%  REVERSAL 1「誰も折り返してこなかった」
 18.0%  ボルトカッター（cold open の解決＝ここで初めて閉じる）
 22.0%  スケール宣言（2010年だけで約120万件）
 26.9%  ACT III
 32.5%  宣誓録取が始まる
 34.1%  ★量の逐語「a round number of ten thousand」
 36.1%  ★「So these documents wouldn't be executed on your own personal knowledge?」—「Right.」
 41.0%  メイン州最高裁「a disturbing example of a reprehensible practice」＝ACT III の out
 44.5%  ACT IV
 46.8%  ★MID REVEAL「一つの名前、十二の手」（Linda Green・免責と同じ息で）
 50.8%  時給10ドル・1時間350枚・1日4,000枚
 55.1%  フロリダ州司法長官の5枚のスライド
 58.8%  差押えの停止（23州）
 62.7%  全50州の司法長官
 64.4%  ★PRIMARY REVEAL 開始（ACT V・250億ドル）
 66.0%  25分の1.5＝6%
 67.9%  1,480ドル
 74.5%  2,358,441人が300ドル
 78.6%  「その数字はどこにも存在しない」
 79.7%  ネバダ606件の却下／Lorraine Brown 5年／LPS 3,500万ドル
 82.4%  Boone郡の登記官 Bettie Johnson
 83.5%  Nyerges（保安官と引越しトラックで銀行を差押えに行く）
 87.6%  ★cold-open CALLBACK（Cardoso 和解・裏の網戸）＋ ENDING 用ループの植え込み
 90.0%  ENDING
```
mid reveal **46.8%**（帯 45–60% ✓）／primary reveal 開始 **64.4%**（帯 65–85% に対し **0.6%pt 早い＝許容内と判断**）／callback **87.6%**（帯 70–90% ✓）。
**⚠ 正直な偏差2件（隠さない）:**
1. **宣誓録取の逐語（34–36%）は mid reveal の帯より早い。** これは意図的で、ACT III を「録取＝ACT III の payoff」、ACT IV 冒頭の「一つの名前、十二の手」を mid reveal として設計したため。ラダーは **shock 0% → 録取 36% → mid 47% → primary 64–85% → callback 88%** の5段になっている。
2. **ENDING（90.0%–100%）は zombie second mortgage と CFPB の現状という新情報を含む。** R-14 の「92%以降に新 core fact を置かない」に対し、これは**縁に触れている**。正当化は2点で、どちらも記録として残す: (a) **87.6% に「the paper from those years is not finished with people yet」というループを明示的に植えてある**ので、ENDING はその payoff＝falling action である。(b) **live-case rule（v003 §5.6）が最後の60秒を差し替え可能に書くことを要求している**ため、この位置以外に置けない。**これは設計上の既知の妥協であり、R3 の裁定に付す。**

### R2-5 Re-hook cadence（FINDINGS R-15: 30分帯 max ≤150s）
段落＝ビート構造。**最長段落 = 159語 ≈ 53.6秒**（cold open）。本編中の最長は **121語 ≈ 40.8秒**。**150秒超の平坦区間 = 0。** act 単位で 21% を超えるリバーサル無し区間なし（ACT I 15.2%・ACT II 11.7%・ACT III 17.6%・ACT IV 19.9%・ACT V 25.6% — **ACT V のみ 21% 超だが、内部に arithmetic の段（6%・$1,480・$300・存在しない数字）と criminal reckoning と2件の restored victim という 6 つのターンを含む**）。

### R2-6 EMOTION-COMMAND grep（FINDINGS R-19 — 勝者は0）
```
$ regex: Sit with|Think about the|feel the (full )?weight|Now sit inside|Let that sink|aim it at|Hold that|Remember this|Imagine (for a moment|how)
emotion-command hits: 0 []
imperative-opening sentences: []
```
**= 0。** 初稿には1件（"Now hold that story next to the scale it sits inside."）あり、"That story sits inside a much larger number." に書き換えて解消。**narrator imperative も 0**（bookkeeping 系も使っていない）。

### R2-7 voice/rhythm 実測
- AI-smell grep（little did / but here's the thing / needless to say / tapestry / testament to / chilling / shocking truth / dark secret / delve / at the end of the day / it is important to note）= **0**
- 疑問符 **5**＝**1.1/1000w**（上限2）。**うち4件は宣誓録取の逐語 Q**、1件は "Does the person who signs actually read them." で、**意図的に疑問符を付けず平叙で置いてある**（＝ナレーターの修辞疑問は実質 0）
- you/your = **14 = 3.0/1000w**（上限8）・すべて co-investigator 用法
- short-punch（≤7語文）= **23.3%**（帯 20–35%）。各幕に ≤5語の punch あり: "There was no debt." / "He asked the man to please double-check." / "Right, Stephan said." / "Ten thousand a month." / "That left one."
- 文長 mean 16.5 / median 14（4〜48語で変調）
- anaphora: "It means there is no lender. Nobody held a lien… no loan… no monthly payment… no note" の否定連打、"Do you read every paragraph…? No. What do you read? I look for the figures." の Q&A 連打（逐語）

### R2-8 specificity（FINDINGS R-21）
- 固有具体（数詞・月名・固有名詞）実測 **≈22.0/min**（floor 5/min）
- **最長 number/name/date-free 連続 = 101語 ≈ 34.0秒**（cap 270語/90秒 — 3倍近い余裕）
- 全 major reveal 文に日付/数値内蔵（10 Dec 2009・9 Feb 2012・25 Jun 2013・2,358,441 / 3,949,896・$1,480・$300）

### R2-9 craft-checklist 自己採点 = **29/29**（house の26項目テーブルを EP56 と同じ A–G 体系で展開したもの。行数は29、内容は同じ26チェック）
| # | 判定 | 証拠（1行） |
|---|---|---|
| A1 concrete cold open | ✓ | 人物＋日付＋場所＋不可逆行為（自分の家の鍵を切る）。thesis なし |
| A2 ending stakes in open | ✓ | "one man was putting his signature on ten thousand sworn court documents a month"＝着地の規模を名を伏せて約束 |
| A3 ≥2 loops past 25% | ✓ | 25%: 書類の数／鍵のかかったドア／権利証 ・50%: 数／名前／誰も数えていない ・75%: 数／callback／存在しない数字 |
| A4 macro loop ≥50% | ✓ | 「誰も読んでいない書類の数」（22% 植え → 34% 録取 → 47% 工場 → 78% 「その数字は存在しない」） |
| A5 re-hook ≤150s | ✓ | 最長 53.6秒（§R2-5） |
| A6 top reveals last 35% + 名前遅延 | ✓ | primary 64.4–83.5%；"a man named Jeffrey Stephan"（32.5%）は "one man… ten thousand a month"（0:40 の予告）から **約31分ぶんの遅延**で命名 |
| A7 local resolutions | ✓ | cold open は 18.0% で閉じる（ボルトカッター）／各ケースビートが3分内で開閉 |
| B1 villain by 25% + record detail | ✓ | 15–18%：「誰も折り返してこなかった」＝制度が悪役。record detail＝自社の担当エージェントが誤りを伝えた（¶12） |
| B2 adjectives ≤2文 from record | ✓ | 評言はすべて逐語か認定に隣接（"a disturbing example of a reprehensible practice" は判決文） |
| B3 verbatim per act | ✓ | I: "steamrolled right ahead" / II: 銀行広報の声明 / III: 録取2系統＋判決 / IV: Pendley・Crite・FL AG / V: Holder・Fed・GAO・DOJ |
| B4 villain status beat | ✓ | ACT I の「登記所の記録は誰でも見られる公的事実」＝制度の正当性を先に立ててから壊す |
| C1 unrepeatable details | ✓ | Cardoso＝イラク third tour の帰国式を逃した／屋根裏だけ見つからなかった／芝生のタイヤ跡 ・Pendley＝"Yeah, can't you tell?" ・Green＝名前が短くて綴りやすいから ・Nyerges＝謝罪状で名前を綴り間違えた ・Johnson＝自分の書庫を検索した |
| C2 planted object pays ≥2min | ✓ | 権利証（ACT I）→「9168 Geneva Street was theirs the entire time」（87.6%）／ボルトカッター（0%）→ callback |
| C3 victim violence ≤1 clause | ✓ | 暴力ゼロ。損害は物と部屋で語る |
| D1 emotion commands | ✓ | 0（§R2-6） |
| D2 ≥3 registers/act + warm 1st half | ✓ | warm（ACT I の家）・procedural（登記所）・dry（"It took a federal lawsuit to get a bank to agree with it."）・grave（ACT III 判決）・near-comedy（Nyerges）・elegiac（ENDING） |
| D3 false-relief → reversal | ✓ | 「銀行が間違いを認め、1時間で折り返すと言った」→誰も折り返さない／差押え停止（58.8%）→17日後に再開／$25bn の見出し→$1,480 |
| D4 held-beat per act | ✓ | "There was no debt." / "Nobody ever called him back." / "Right, Stephan said." / "Ten thousand a month." / "That left one."（slow-read cue は CODEX_B へ） |
| E1 punch share 20–35% | ✓ | 23.3% |
| E2 you ≤8/1000 | ✓ | 3.0/1000 |
| E3 rhetorical Q ≤2/1000 | ✓ | 実質0（疑問符5件のうち4件は逐語 Q） |
| E4 AI-smell 0 | ✓ | grep 0 |
| E5 anaphora run | ✓ | "no lender / no lien / no loan / no payment / no note"、録取 Q&A 連打 |
| F1 ≥5 specifics/min | ✓ | ≈22.0/min |
| F2 no >90s gap | ✓ | 最長 34.0秒 |
| F3 reveal sentences dated | ✓ | 全件 |
| G1 honest ending | ✓ | 「誰も数えなかった」で終わる。慰めゼロ・現在時制・date-stamped |
| G2 flat aftermath → planted button | ✓ | 集計 → 現在の zombie second → 「明日の朝、誰かが読まずに署名する」＝植えた素材のみ |
| G3 CTA 1文・末尾 | ✓ | "If you think a house somebody paid for in full should not be able to disappear into a filing error…" |

**R2 判定: PASS（偏差2件を明記して記録。R2-2 の sting 位置と R2-4 の ENDING 新情報は R3 の裁定に付す）。**

### R2-10 known-outcome dread（R-18）
本件は **R-18 を部分適用**する。米国の視聴者の多くは「2008年以降に大量の差押えがあった」「誰も刑務所に行かなかった」という結末を漠然と知っている。よって**行き先（誰も数えなかった／刑務所に行ったのは一人）を早めに宣言し、how を売る**。ACT II 冒頭で「読まれていない」という結末を宣言し、ACT V で精算し、ENDING で現在時制に落とす。**ただし冒頭の一軒の家の結末は伏せる**（cold open は resolution 前で切る・R-14）。

### R2-11 息継ぎ字幕適性・発音
短文主体・カンマ節が息継ぎ単位で切れる構造にした。**CODEX_B 向け発音ウォッチリスト:** *affidavit*（AF-ih-DAY-vit）・*notarised / notarized*・*Alpharetta*（al-fuh-RET-uh）・*escrow*・*assignment of mortgage*・*Szymoniak*（shim-OH-nee-ak・**画面表記のみ、VO では「a Florida investigator」で回避する選択肢も可**）・*Pendley*・*Crite*（クライト）・*Duval*。ElevenLabs 試聴で要確認。**数字の読み上げ**は台本本文で英単語に開いてある（"one thousand four hundred and eighty dollars" 等）ので TTS が桁を誤読しない。

### R2-12 このエピソード固有の最大リスクと、その処置（finance-explainer 対策）
チャンネルの計測上、金融解説は **AVP 3.97% の底**。本作はその真ん中に落ちる題材なので、**R-2 の「60–180秒に説明ブロックを置かない」だけでは足りない**と判断し、三重に対策した。
1. **証券化・MERS・譲渡連鎖は台本に一度も出てこない。** 出てくるのは「銀行が判事に紙を出す」「その紙は宣誓されている」「宣誓した人間が読んでいない」の三つだけ。譲渡連鎖の説明は **AE-12 のダイアグラム1枚に外部化**した（DESIGN §3）。
2. **抽象は必ず一人の人間の動作に接着する。** ACT III の「personal knowledge」は、定義ではなく「判事は銀行を信じているのではなく、読んだと誓った一人の人間を信じている」という**人の話**として提示する。
3. **AE の4枚が説明の荷重を負う**（DESIGN §3 のハードカード表）。カウンター（AE-09）・一つの名前と十二の手（AE-11）・切れる連鎖（AE-12）・25億の解像（AE-15）。**この4枚が弱いと本作は失敗する**と設計書に明記済み。

---

## R3 (independent) — PLACEHOLDER

**未実施。** 本パッケージを執筆していない独立エージェントが、台帳・R1・R2 を信用せずに次を行うこと。

1. **全メトリクスの自前再計算**（語数・emotion-command grep・specificity・reveal ladder の語オフセット・re-hook 間隔・punch share・you/your・AI-smell）。R2 の申告値と ±2%pt を超えて食い違ったら R2 の申告を誤りとして記録する。
2. **敵対的ファクト検証**。最優先で再取得すべきもの:
   - **Jeffrey Stephan の宣誓供述録取の原本 PDF**（本パスが取得した2種）を**自分で開いて逐語照合**する。台本の引用が転写と一字一致しない場合は引用を落とす。
   - **住宅所有者側の一次記録**（連邦地裁ドケットと訴状本体）を自分で開き、金額・年・所在地・結末が台本と一致するか確認する。
   - **DOJ の2013-06-25 リリース**を .gov ホストから取得できる環境で再取得する（本パスは Akamai により 403 で、逐語再掲サービス経由のため A− 止まり）。
   - **OCC の 2011-04-13 プレスリリース**（本パスは occ.gov に到達不能）。URL を確定できなければ台本・設計書から OCC の URL 表記を落とす。
   - **GAO-26-108448 のブリーフィング・スライド**（PDF 内が画像のため本パスは法律事務所要約経由）。**88% という数字を画面に出すなら、ここを読んでからにする。**
3. **公開直前の再検証**（台帳末尾の re-check リスト）: CFPB の係属状況と長官人事、*Hodges v. NewRez* の状況、州法の動き、2026年の新規エンフォースメント。**ENDING の最後の60秒はここだけ差し替えられるように書いてある。**
4. **CODEX_A のスポットチェック**: S001–S210 の穴なし・重複なし、★HP 88枚の S番号集合、`[HSTYLE]` 行数 106（body 88 + seed 18）、`FC001`–`FC235` の subtype 全ユニーク、`M01`–`M42` / `T01`–`T03` / `F001`–`F012` 完備、§3.3 の検算 [1]–[9] の自力再計算、そして **全267プロンプトに対する「可読署名」「可読文書」「実在ロゴ／印章」「強制退去」「実在人物 likeness」の 5系統 ban 掃引**。
5. **オーナー基準の1周**（feedback_retro_ep37 の教訓）: 8秒フック先頭・OP/ED が既存テイスト・字幕サイズ・素材被り・切りの良い終わり・紙芝居でないこと——を、見せる前に自分で通しで確認する。

---

## 現時点のゲート出力（2026-07-29 実行・すべて実出力の貼り付け）

```
$ ./.venv/Scripts/python.exe scripts/check_script_length.py --lo 1740 --hi 1860 episodes/_planning/EP59_robosigning_script.en.v001.md
PASS script_length: 4,675 words (need 3,973-5,309)
  narration estimate  slow 28.6m | median 26.2m | fast 19.7m
  target band         29.0-31.0 min
  ! RISK: at the fast end of the measured pace (237.4 wpm, seen on williams/florence) this lands at 19.7 min -- under the floor. Either pin the voice speed or write to 6,885 words.
  （処置は R2-1 のとおり: Brian 正典設定の実績帯 167–182wpm・TTS 実測後に durationInFrames 再ロック）

$ ./.venv/Scripts/python.exe scripts/check_planning_package.py 59 robosigning
ok   F1 script_length gate PASS (1740-1860s)
ok   F2 narration body is CJK-free
ok   F3 hook->OP->acts structure markers present
ok   F5 'dochighlight' absent or explicitly banned
ok   F6 'DATE_STAMP' absent or explicitly banned
ok   F7 DESIGN carries figure-beat density budget
ok   F8 CODEX_A carries 1-scene-1-image / no-variants rule
ok   F9 CODEX_A carries the real-person likeness ban
ok   F10 review log has R1+R2
ok   thumb: CODEX_A includes emotive-face thumbnail stills
info word-ish count (latin tokens): 6959

RESULT: PASS (0 warn)

$ ./.venv/Scripts/python.exe scripts/check_prompt_diversity.py episodes/_planning/EP59_robosigning_CODEX_A_ASSETS.v001.md
ok   prompt coverage 106% (267/252 referenced asset ids)
info prompts extracted: 267 | boilerplate tokens dropped: 11 (df>30%)
ok   no same-series pair reaches Jaccard 0.5
WARN 5 cross-series twin(s) (still/motion pairs are often intentional — eyeball them):
  0.62  M20 ~ S110   shared: condensation, conference, deep, focus, glass, long, made, pause
  0.59  M19 ~ S094   shared: cropped, desk, distance, file, forearms, hands, holding, lamp
  0.54  M37 ~ S166   shared: banded, bundles, carton, document, evidence, grey, inside, lamp
  0.52  M33 ~ S173   shared: address, all, bare, blank, canvas, envelopes, hall, hamper
  0.51  M25 ~ S130   shared: abstract, carrying, corners, dark, different, document, each, every

RESULT: PASS (0 dup-pairs, 0 generic)
```

**coverage 106% の読み方:** 分子 267 = literal プロンプト総数（S210 + M42 + T3 + F12）、分母 252 = 本文が語形境界つきで言及した asset id の数。**全 267 資産に literal プロンプトがあり、improvise される資産はゼロ。** 100% を超えるのは、`FC001_…` 形式の factory 名と `M01_src.png` 形式のファイル名が正規表現の語形境界に掛からず分母に入らないため（**この命名は §4.4 で意図的に選んだもの**で、EP55/EP56 にあった factory ↔ emotive-face の ID 空間衝突を消してある）。

**cross-series twin 5組は意図設計。** 各 i2v 種は対応する still の「動く直前」版ではなく**別の瞬間**を撮るよう §8.1a で書き直してあり（初回計測で 20組・最大 0.94 だったものを 22行の書き直しで 5組・最大 0.62 まで落とした）、残る5組は同じ小道具を共有しているだけで構図・動作が異なる。**出荷前に §6.1 Q4 の phash watch-list で目視すること。**

## 申し送り（次工程）
1. **R3 独立レビュー（未実施）** — 本ログ末尾のプレースホルダの5項目を、本パッケージを書いていないエージェントが実施する。**最優先は Stephan 逐語の原本再照合と、Cardoso 訴状の自力読解。**
2. **ElevenLabs マスター生成（Brian 正典設定）→ ffprobe 実測 → durationInFrames 再ロック**（DESIGN §5 の手順。EP55 −71.2s / EP56 −71.8s の実績があるので、**ドリフトは gap 予算で吸収し、再 TTS も台本編集もしない**）。
3. **CODEX_A（`EP59_robosigning_CODEX_A_ASSETS.v001.md`）で素材発注** — still 210（★HP 88 = 41.9% を誕生時から）＋ i2v 種 42 ＋ thumb_face 3 ＋ F系 12 ＝ 267枚、実写 235本、overlay 30本。**実写は `search_archive.py` / `select_factory_assets.py` 経由＋ラベル付きコンタクトシート目視が必須**（棚ラベルの 40% が誤り・§7.2）。
4. **CODEX_B 執筆時:** DESIGN §3 の 17カード表を B の契約表へ一字一致で転記・`check_robosigning_facts.py` を `check_burge_facts.py` から clone（R-SIGN-ILLEGIBLE / R-READABLE / R-NO-LOGO / R-GREEN-VICTIM / R-STEPHAN-EMPLOYEE / R-BROWN-SCOPE / R-PRISON-WORDING / R-LIVING / R-NO-EVICTION-VIOLENCE / R-NUM / R-DOCHL / R-QUOTE / R-DATE）・held-beat 5本に slow-read cue・**sting は 0:40–0:45 に置き、実測 ≤5.0s をゲートにする**（R2-2 の偏差処置）。
5. **公開直前:** FACTS_LEDGER 末尾の re-check リスト（CFPB の係属・人事、*Hodges v. NewRez*、州法、2026年の新規エンフォースメント）。**ENDING の最後の60秒はここだけ差し替えられるように書いてある。**
