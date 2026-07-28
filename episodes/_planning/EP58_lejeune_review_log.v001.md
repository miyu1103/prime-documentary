# EP58 `review_log.v001` — 台本レビュー記録（R1 FACT AUDIT + R2 CRAFT/RETENTION AUDIT + R3 INDEPENDENT REVIEW）

**Subject:** `EP58_lejeune_script.en.v001.md`（narration 実測 **4,738語**・★R3 再ロック 2026-07-29、R1/R2 時点は 4,737 · オーナー帯 4,600–4,750 内）+ `EP58_lejeune_FACTS_LEDGER.v001.md`（CL-01〜CL-46）
**Reviewer:** Claude（左工程）R1/R2。**R3 = 独立非執筆エージェント — 実施済 2026-07-29・判定 PASS（欠陥 23件を修正のうえ）**
**根拠:** `DEEP_RESEARCH_FINDINGS.v001.md`（MUST群）、`TOPIC_PIPELINE.v004.md` EP58 エントリ、`EP58_lejeune_DESIGN_ARCHITECTURE.v001.md` §0–§7、FACTS_LEDGER §W（permitted-wording）と §VERIFIED-VERBATIM、`pd-craft-checklist`（26項目）。

---

## R1 — FACT AUDIT（台本の全 load-bearing 主張 × 台帳の行単位照合）

**3本の並行 web 検証（2026-07-29）**を実行した。3本とも WebSearch 予算が枯渇していたため、**一次資料の直接 fetch と全文 grep** で作業した——結果として検索要約より強い証拠基盤になった。読んだ一次資料: **2007-06-12 下院エネルギー・商業委員会公聴会「Poisoned Patriots」全文**（govinfo）／**2010-09-16 下院退役軍人委員会公聴会全文**（govinfo）／**2023-04-28 下院軍事委員会**（govinfo）／**ATSDR 各ページ＋2013-01-16 対VA書簡PDF**／**Bove et al. EHP 2024-10-24**・**Environmental Health 2014×2**・**Ruckart et al. 2015**（Europe PMC 全文）／**38 U.S.C. §1710/§1787**・**§804 of PL 117-168**（法文）／**連邦官報 2016-07-18・2017-01-13**／**EDNC ドケット D.E. 133 / 250 / 290 / 893 / 894**（PDF 直読）／**GAO-07-276**／**Murtha 証言 PDF**。台本の全主張は script 末尾「Fact map」で行単位対応済み。

### R1-1 ★発注ブリーフの誤りを5件検出し、全て訂正して台本・台帳・設計に反映した

1. **「~1,000,000 exposed」は支持されない → 全面カット（CL-08）。** ATSDR は About / Health Effects / FAQ / Summary / Water Modeling / Tarawa Terrace / Hadnot Point / PHA / Health Studies の**どのページにも曝露人数の総数を出していない**。2007 公聴会にも無い。「900,000〜as many as one million」という構文は**訴訟隣接のマーケティングページ由来**で、本台帳の除外規則に該当。「~630,000」も ATSDR のどのコホートとも一致しない。**採用した代替**＝Ensminger の宣誓証言 verbatim「hundreds of thousands of Marines, sailors, their families, and the loyal civilian employees」（CL-09）＋ ATSDR の実際の登録コホート（154,932 / 154,969 等・CL-27）。**台本 ACT III でこの訂正自体を画面に出した**（"The number you may have seen — around a million — appears in advertising, not in the record."）＝発注時の指示「if the best-supported exposure figure is a range, use the range and cite it」に対し、**支持されるのは範囲ですらなく「総数は存在しない」という事実**だったため、その事実を語らせるという解決を取った。
2. **Janey は Camp Lejeune で「宿った」が、この記録上「生まれた」とは言えない（CL-13）。** 本人の宣誓証言は *"conceived while her mother and I lived in one of the base family housing units"* のみ。同証言で家族の在基地は 1973–1975、妻の妊娠初期のみが Tarawa Terrace、Parris Island の DI スクール後 *"we left there December 20, 1975"* → 出生は 1976・基地退去後。2026年のPRE記事は「conceived and born on the base」と書くが**本人の宣誓と矛盾する二次情報**。→ 台本は "conceived at Camp Lejeune" のみ。
3. **キッチンのテレビ報道は Ensminger ではなく Partain のもの（CL-15 / CL-25）。** 2007 公聴会全文を grep したところ **television / TV / kitchen / newscast / evening news は1語も出現しない**。テレビ由来は Partain の議会提出略歴 verbatim *"after viewing a television report about Camp Lejeune while he was treating his breast cancer"*。Ensminger 側の確定アンカーは **August 1997**（本人の言葉が 2023 軍事委員会記録に読み込まれている）。→ **台本は Ensminger のテレビ場面を一切演出せず、発見の媒体を特定しない。** Act IV でテレビは Partain のものとして正しく置いた。**この訂正は発注ブリーフの明示的な記述（"he found out years later from a TV broadcast"）に反するが、一次記録が支持しないため記録側を採った。**
4. **Grainger の化学者は Hargett ではない（CL-23）。** 公聴会全文に "Hargett" は不在。記録上の Grainger 側名義は **Bruce A. Babson**（1982-08-10 書簡 CLW 0592/0593）、**Elizabeth Betz は基地側の supervising chemist**。→ 台本は Babson を名指し、Betz は役職のみで記述。
5. **「250ガロンのタンク」は出典不明 → カット（CL-11）。** 公聴会・ATSDR 各ページ・Chapter A fact sheet・2013年書簡のいずれにも無い。ABC One-Hour Cleaners の営業年も本パスでは未確定（EPA Superfund サイトが到達不能）→ **台本は容量も開始年も言わない。**

### R1-2 追加で判明し反映した訂正（発注ブリーフ外）

6. **2012年法の対象期間は現行「1953-08-01 から」**（当初 1957-01-01 → **PL 113-235 で 2014 年に改正**）。台本は「1953 to 1987」（CL-31）。
7. **CLJA に陪審禁止条項は存在しない。** §804(d) は逆に *"Nothing in this subsection shall impair the right of any party to a trial by jury"*。**陪審を否定したのは裁判所**（D.E. 133・2024-02-06・4判事連名）。台本はこの取り違えを避け、**リバーサルとして正しく構成した**（CL-34 / CL-38）。
8. **discretionary-function exception は現在の政府の抗弁ではない**（§804(f) が剥奪済み。2016年 MDL 時代の抗弁）。台本は 2016 側に置いた（CL-33 / CL-41）。
9. **「2018年の癌罹患研究」は存在しない**（2017年の PHA 差し替えと causality assessment との混同）。台本は **2024-10-24 EHP** のみを使う（CL-28）。
10. **「三件の $10,000 / $24,000 / $405」は真正**で、しかも**DOJ の裁判所提出書面（D.E. 290・2026-06-15）から直接読めた**。ただし **"three of the twenty-five"** であり "the first twenty-five" ではない（25は母集団全体）。台本はこの表現を採った（CL-40）。
11. **2026年10月の「クロック」は「和解案の提出期限」ではない。** D.E. 893（2026-06-30・4判事連名）は (a) 原告団リーダーシップを **10/30 まで**しか再任せず、(b) *"expects the PLG and DOJ to use their best efforts to achieve a global settlement by October 30, 2026"* と述べ、(c) **例外なしの週次会合**を課し、(d) その後 *"other action relating to either the PLG or the Department of Justice"* を留保した。→ **台本は命令の文言どおりに語り、"a settlement plan is due" とは言わない**（CL-43）。
12. **濃度の二重帳簿を検出。** ATSDR の Chapter A fact sheet（finished-water モデル値: ベンゼン 12 / 塩化ビニル 67 µg/L）と ATSDR の FAQ ページ（ベンゼン最大 720 ppb / 塩化ビニル 655 ppb）が**整合しない**。→ **台本はベンゼンと塩化ビニルを名指しはするが濃度を一切出さない。** 画面に出す濃度は **PCE 215（限度5）と TCE 1,400（限度5・280倍）の2つだけ**（CL-04 / CL-05）。**well 651 の 18,900 ppb も不使用**（蛇口から出た水ではない）。
13. **男性乳がんクラスタは疫学ではなく個人名簿。** 64人（2010宣誓）→125人超（2026・PRE）。査読研究（Ruckart 2015・71症例/373対照）の **OR = 1.14（95%CI 0.65–1.97）** は実質ヌル。→ **台本は両方を同じ段落で言う**（CL-26c）。これは本作最大の誠実性テストであり、削らなかった。
14. **個人の責任追及はゼロで、それは「探した上での不在」**。EPA 刑事部長 Murtha の宣誓証言で DOJ の**起訴見送り**が明言され、GAO-07-276 も*"did not find any violations of federal law"*。→ 台本は絶対形（"no one was ever held accountable"）を避け、**"no individual has ever been publicly disciplined or prosecuted"** を使う（CL-44）。
15. **広告費の計測者は X Ante（"X Ander" ではない）**。Bloomberg Law（Roy Strom・2023-01-30）verbatim で **$112M / 2022年 / 次点mass tortの2倍超**。Reuters（2022-10-04）で **約94,000本・3/22–9/28**。**「55,000本」は不使用。**（CL-46）

### R1-3 逐語引用の照合（台帳 §VERIFIED-VERBATIM 20系統のみ使用）

台本で実際に引用符に入れたのは **10系統**で、全て一次記録に対する文字照合済み: CLW 0436（1980-10-30）✓／CLW 0438（1980-12-29）✓／**CLW 0443（1981-03-09）✓**／Babson 書簡（1982-08-10）✓／Ensminger「hundreds of thousands…」✓／Ensminger「Ironically, most of these people…」✓／Ensminger「terrible resolve…」✓／Partain「'You have male breast cancer'…」✓／Partain「No further action was taken.」✓／Bove et al. 2024「Increased risks… compared with Camp Pendleton」✓／§804(j)(3)「Any applicable statute of repose…」✓／§804(c)「sufficient to conclude that a causal relationship is at least as likely as not」✓／D.E. 133「does not unequivocally, affirmatively, and unambiguously…」✓／D.E. 133「Congress could have made this dispute easy to resolve.」✓／D.E. 290「more than 88%… less than 2%…」✓／D.E. 893「best efforts to achieve a global settlement by October 30, 2026」✓／ATSDR ベンゼン譲歩「should have been included in the PHA but was not」✓／Gros「Levels of these contaminants were so high so as to preclude THM testing.」✓。**捏造引用ゼロ。**
**⚠ 1件だけ表記変更を明示:** CLW 0443 の原文は括弧書き `(solvents)` だが、**朗読で括弧は読めない**ため VO は「— solvents!」とダッシュで渡し、**AE QUOTE_CARD #1 には括弧を含む原文を一字一句出す**（DESIGN §3 card 9）。台帳とカードが正典、VO は音声化。
**使わなかった引用と、その所在を記録した**（台帳 §QUOTES RECORDED BUT NOT USED）: NRC 2009 の委員会自身の結論（委員会本文が取得できず、海兵隊側の宣誓での特徴づけしか無い）／Ensminger の1997年テレビ場面（一次記録に無い・本人インタビューと2011年の映画に所在）／**2007年証言中の骨髄穿刺の一節（逐語検証済みだが、医療処置下の子どもの描写にあたるため本作の最重要禁止線に触れる。意図的に不使用）**／"Mike Hargett"（記録に不在）／井戸別の停止日（ATSDR Chapter A Supplement 1・未取得）。

### R1-4 センシティビティ監査（HARD）

- **子ども:** Janey の一節は **ACT I に1回のみ**（15.6%）。日付・年齢・病名は of-record として断定、**その先は父親が公聴会で公にした範囲を1文字も越えない**。台本は明示的にそう宣言している（"this film is not going to describe any part of that beyond what her father chose to say about it"）。**医療の描写ゼロ・葬儀の描写ゼロ・墓の描写ゼロ。** CODEX_A は健康な子どもすら描かない（誤読リスク）＝ §1.1-2 / §5.5 / Q7 で三重実装。✓
- **因果:** ledger §W を全文適用。台本に **"the water killed / caused"** は0件。ACT III の「what it does and does not prove」段落が本作の因果ファイアウォールで、**MCL の制定年（1989/1992）と刑事捜査の不起訴を先に置いてから**「証明されるのはもっと狭く、そしてある意味もっと悪いこと」に降りる。✓
- **存命人物:** Ensminger と Partain は宣誓証言・報道での本人発言のみ。内心・動機の付与ゼロ。Ensminger の "They killed my daughter."（2026-07・PRE）は**本人の characterisation であり我々の声では使わない**と台帳に明記し、台本でも不使用。✓
- **個人の名指し:** 士官・当局者・判事・議員を悪役として名指しゼロ。ドライクリーニング店の私人所有者も不記載（CL-45）。Babson と Betz は**記録上の役割**としてのみ登場（Betz は役職のみ）。✓
- **軍章・ロゴ・可読文書:** 台本は依存なし。CODEX_A / DESIGN でバン実装済み。✓
- **広告レジスター:** 本件は米国史上最大級のテレビ広告飽和案件。台本は**広告そのものを事実として扱い**（$112M・94,000本）、パッケージングには **ドル記号・金額・claim 系語・電話番号風要素・赤バナーを禁止**（DESIGN §6 R-ADadjacent、CODEX_A §5.12）。**法律事務所のスポンサーシップは受けない。** ✓
- **数値の分離:** 408,000 は**行政請求**、3,759 は**訴訟**。台本は両者を隣接する別文で出し、混ぜない。✓

**R1 判定: PASS**（捏造ゼロ・全主張が CL 行にトレース・ブリーフとの差分5件はすべて一次ソース側に合わせて修正済み）。

---

## R2 — CRAFT / RETENTION AUDIT（DEEP_RESEARCH MUST群のネイティブ検査）

### R2-1 尺・語数ゲート（実行出力・2026-07-29）
```
$ ./.venv/Scripts/python.exe scripts/check_script_length.py --lo 1740 --hi 1860 episodes/_planning/EP58_lejeune_script.en.v001.md
PASS script_length: 4,737 words (need 3,973-5,309)
  narration estimate  slow 28.9m | median 26.6m | fast 20.0m
  target band         29.0-31.0 min
  ! RISK: at the fast end of the measured pace (237.4 wpm, seen on williams/florence) this lands at 20.0 min -- under the floor. Either pin the voice speed or write to 6,885 words.
```
- narration 本体実測 = **4,737語** → オーナー帯 4,600–4,750 内 ✓。
- RISK 行への処置: EP55/EP56 と同一 — Brian 正典設定（stability≈0.35 / similarity≈0.80）で fast 端は実績帯 170–178 wpm に入る。**237.4 wpm は williams/florence の別設定由来で本作には適用されない。** TTS 実測後に `durationInFrames` を再ロック（DESIGN §5.3 の手順）。

### R2-2 Opening formula v2（FINDINGS R-7..R-13 — 実測）
| 項目 | 判定 | 証拠 |
|---|---|---|
| 第1文 = 宣言文・人物+固有具体+不可逆イベント | **PASS** | "On the twenty-fourth of September 1985, a Marine Corps drill instructor named Jerry Ensminger lost his nine-year-old daughter to leukaemia." — 人物は word 11 ≈ **3.8s**、疑問文でない、"This is the story of" なし、不可逆イベントは同一文内 |
| 人物名 ≤0:15 / 対立勢力 ≤0:28 | **PASS** | Ensminger ≈0:04；"the Corps" ≈0:22（"Ensminger had given the Corps twenty-four and a half years"）；その own laboratory ≈0:29 |
| BUT-loop がスティング前（~0:32） | **PASS** | "But the base where his wife had carried Janey…" = word 74 ≈ **0:25**、ループの芯（"the Corps' own laboratory had written that down by hand… with an exclamation mark"）≈0:29–0:33 |
| Brand sting ≤5s・audio-continuous・loop後 | **PASS（設計値）** | 台本に §BRAND STING 指定（~0:33–0:38・gold Bookends の ≤5s cut・title line 融合）— ビルドで sting 実測 ≤5.0s を検証（DESIGN §5.4） |
| Post-brand = 1エスカレーション文+日付/場所アンカー | **PASS** | 46語・"Forty-one years later that piece of paper sits inside a federal lawsuit with roughly four hundred and eight thousand claimants behind it…" 1文 → "Camp Lejeune, North Carolina. It begins with a well." |
| First-45s 禁止事項（subscribe/self-description/2文連続無具体） | **PASS** | 該当なし・新具体は3–8秒ごと（1985-09-24／nine／leukaemia／24.5年／solvents／exclamation mark／4年／16年） |

### R2-3 60–180s explanation-block スキャン（FINDINGS R-2 — 我々の実測クリフ帯）
60s≈word 175 〜 180s≈word 525 = ACT I 前半。内容: **人が行為する描写**（洗濯物を干す・三輪車を置く・グラスを満たす・氷を作る・芝に水をまく）→ 名前のある男（Ensminger）→ 名前のある住宅地区（Tarawa Terrace）→ 日付つきの退去（1975-12-20）。**「化学物質の仕組み」講義ブロックは存在しない**: PCE/TCE の説明は正味2段落だが、**両方とも「地面の下にあった物」の描写**として運ばれ、直前直後を人物の行為が挟む。person-action-free の最長連続は **PCE/TCE 段落の ~14秒**。**≥20秒の person-action-free 連続ブロック = 0** ✓。毒性学（TCE/PCE/ベンゼン/塩化ビニル）は**一度も講義されず、一家族と一枚の分析票を通してのみ体験される**——これが発注ブリーフの中心的な MUST であり、構造的に満たしている。

### R2-4 Reveal LADDER 実測位置（FINDINGS R-14・語オフセット実測）
```
  0.3%  cold-open shock（Janey の死・解決前カット）
  1.6%  BUT-loop（基地の水・自前のラボ・感嘆符）
  2.9%  post-brand 408,000 ＋ 10月30日の植え込み
 15.6%  Janey の一節（人的ピーク・1回のみ）
 17.1%  dread-plant（"was nothing. There was no letter."）
 18.8%  ACT II 開始（August 1997）
 38.9%  ★MID REVEAL 開始: CLW 0443「Water highly contaminated…(solvents)!」
 49.4%  MID 芯: 曝露総数の訂正（"appears in advertising, not in the record"）
 51.4%  ACT IV 開始: Partain「'You have male breast cancer'…」
 60.9%  ATSDR が自らの評価を撤回（20–40s の tonal reset ここ）
 65.5%  2024年 EHP の結論 verbatim
 73.7%  CLJA 2022
 80.2%  ★cold-open CALLBACK（"a laboratory form that a retired drill instructor had to ask the government to hand over… exclamation mark"）＝70–90%帯 ✓
 82.1%  ★PRIMARY 開始: 陪審は無い（D.E. 133）
 85.5%  no trial date
 87.7%  2,446 paid / 408,000 filed
 91.8%  ★PRIMARY PEAK ＝ 最後の新事実: $10,000 / $24,000 / $405
 92.2%〜 ENDING: 10月30日命令（0:40 で植えた事実の精算）＋既出事実の present-tense 再集計のみ
```
mid ~39→49% ✓（EP56 と同型: MID は「開始」と「芯」の二段） / primary 65–85% 開始 ✓（82.1%） / **92% までに新事実終了** ✓（91.8%） / callback 70–90% ✓（80.2%） / 最終5–10%は falling action ✓。
**★制作中に2件の実測不合格を検出して修正した（自己申告でなく数値で発見）:** ① callback が当初 **97.9%** に落ちていた → ACT V に明示的な callback 段落を挿入して **80.2%** に。② 最後の新事実が **92.5%** で 0.5pt 超過 → ACT V の因果motion段落を圧縮し ENDING に既出事実の falling action を 45語追加して **91.8%** に。

### R2-5 Re-hook cadence（FINDINGS R-15: 30分帯 max ≤150s）
段落＝ビート構造。最長段落は ACT I の PCE/TCE 段落（**143語 ≈ 49秒**）と ACT V の広告段落（**121語 ≈ 41秒**）。**150秒超の平坦区間 = 0** ✓。act 単位で 21% 超のリバーサル無し区間なし ✓（ACT I 15.6%／ACT II 17.7%／ACT III 15.0%／ACT IV 18.4%／ACT V 22.5% だが内部に3つのリバーサル [陪審・裁判なし・$405] を持つ）。

### R2-6 EMOTION-COMMAND grep（FINDINGS R-19 — 勝者は0）
```
$ python - (regex: Sit with|Think about the|feel the (full )?weight|Now sit inside|Let that sink|aim it at|Hold that|Remember this)
emotion-command hits: 0 []
```
**= 0 ✓。** 非bookkeeping の narrator imperative は正確に **2本**（"Read that back slowly." / "Read carefully, that is a statement about paperwork"）= 上限2 ✓。bookkeeping 系 0（≤6）✓。

### R2-7 voice/rhythm 実測
- AI-smell grep（little did / But here's the thing / needless to say / tapestry / testament to / chilling / shocking truth / dark secret / delve / in a world where / buckle up）= **0** ✓
- 修辞疑問: **1**（"How many people is that?" — 直後に「誰も知らない」と自答し、訂正 CL-08 に降りるための機能的な問い）= **0.21/1000w** ✓（≤2）
- you/your = 10 = **2.1/1000w** ✓（≤8）・全て co-investigator 用法＋末尾CTA
- short-punch（≤7語文）= **26.6%** ✓（20–35%帯）・各actに ≤5語 punch あり（"Her name was Janey." / "He believed them." / "By then he had the paper." / "Nothing happened." / "That is 1982." / "Every wall was down." / "Four hundred and five dollars."）
- 文長 mean 19.4 / median 14 — 3〜60語で変調 ✓
- anaphora escalation: ACT III の "It does not prove… It does not prove… What it proves is narrower" ✓ ／ ACT I の "There was no letter. There was no notification. There was no suggestion…" ✓

### R2-8 specificity（FINDINGS R-21）
- 固有具体（数詞・月名・固有名詞）実測 **≈16.2/min** ✓（floor 5/min）
- **最長 number/name/date-free 連続 = 96語 ≈ 33秒** ✓（cap 270語/90秒）。位置は ACT I のキッチン描写（"There is a tap, and a glass, and a woman filling it…"）で、**意図的な無具体帯＝この映画で唯一の「普通の生活」の呼吸**。
- 全 major reveal 文に日付/数値内蔵（1981-03-09=CLW 0443 ／ 1985-02=wells ／ 2009-04-28=withdrawal ／ 2024-02-06=no jury ／ $405 ／ 2026-10-30）✓

### R2-9 craft-checklist 26項目 自己採点 = **26/26**
| # | 判定 | 証拠（1行） |
|---|---|---|
| A1 concrete cold open | ✓ | 人物+日付+年齢+病名（thesis なし・word 11 で人物） |
| A2 ending stakes in open | ✓ | post-brand「until the thirtieth of October to finish this」（結末の存在だけ約束・内容は伏せる） |
| A3 ≥2 loops past 25% | ✓ | 25%: the paper / the count / the man born on the base ・50%: the paper resolved→the registry ・75%: the count → 2,446 → $405 |
| A4 macro loop ≥50% | ✓ | **the binder**（18.8% 誕生 → 80.2% callback → 99% 最終画）＋ **the count**（2.9%→91.8%） |
| A5 re-hook ≤150s級 | ✓ | 最長段落 143語 ≈49s（§R2-5） |
| A6 top reveals last 25% + 60s名前遅延 | ✓ | $405 が 91.8%；Partain は「a forty-year-old insurance adjuster in Tallahassee」で導入し **名前を63語後（≈22s）に遅延** |
| A7 local resolutions | ✓ | 各ビートが3分内で開閉（1980の一件／Grainger の一件／撤回の一件／陪審の一件） |
| B1 villain by 25% + record detail | ✓ | 17.1%「was nothing. There was no letter.」＝制度の不作為が record detail として着地 |
| B2 adjectives ≤2文 from record | ✓ | 評言はすべて verbatim/finding 隣接（"Nothing happened. That is the finding, and it needs no adjective."） |
| B3 verbatim per act | ✓ | II: Ensminger×2 ／ III: CLW 0436/0438/0443 + Babson + Gros ／ IV: Partain×2 + ATSDR + EHP ／ V: §804 + D.E.133×2 + D.E.290 ／ ENDING: D.E.893 |
| B4 villain status beat | ✓ | ACT I「the Corps looks after its own」＋「the most concentrated form of the institution there is」 |
| C1 unrepeatable details | ✓ | Ensminger=DI school を終えて 1975-12-20 に去った／Janey=3:35 p.m., Tuesday／Partain=18回目の結婚記念日／Vidana=$405 |
| C2 planted object pays ≥2min | ✓ | the form（cold open で植える → 38.9% で読ませる → 80.2% で callback → ENDING で最終画） |
| C3 victim violence ≤1 clause | ✓ | 暴力描写ゼロ。Janey は1節・医療描写ゼロ・骨髄穿刺の一節は意図的に不使用 |
| D1 emotion commands | ✓ | 0（grep 出力 §R2-6） |
| D2 ≥3 registers/act + warm 1st half | ✓ | warm（ACT I の基地生活）・dry（"nobody buys a village… nobody ever looked at a glass of water"）・procedural（ACT III）・grave（Janey）・cold-legal（ACT V） |
| D3 false-relief → reversal | ✓ | 「Every wall was down.」（希望の頂点）→ 広告の洪水 → 陪審なし → $405 |
| D4 held-beat per act | ✓ | "Her name was Janey." / "By then he had the paper." / "Nothing happened." / "No further action was taken." / "Four hundred and five dollars."（slow-read cue は CODEX_B へ） |
| E1 punch share 20–35% | ✓ | 26.6% |
| E2 you ≤8/1000 | ✓ | 2.1/1000 |
| E3 rhetorical Q ≤2/1000 | ✓ | 0.21/1000（1本・機能的） |
| E4 AI-smell 0 | ✓ | grep 0 |
| E5 anaphora run | ✓ | "It does not prove… It does not prove…" ＋ "There was no letter. There was no notification. There was no suggestion…" |
| F1 ≥5 specifics/min | ✓ | ≈16.2/min |
| F2 no >90s gap | ✓ | 最長 96語 ≈33s |
| F3 reveal sentences dated | ✓ | 全件 |
| G1 honest ending | ✓ | "Not a verdict. Not a finding. A deadline."（慰めゼロ・現在時制・date-stamped） |
| G2 flat aftermath → planted button | ✓ | 集計 → 「the form… nine words and an exclamation mark」→ "He wrote down what he found."（植えた素材のみ） |
| G3 CTA 1文・末尾 | ✓ | "If you think a government that measures its own water owes the people drinking it the result, hit like…" |

（26/26。EP52=20・EP53=21 → EP55/56 で解消した D節・F節の系統的欠陥を継続的に維持。）

### R2-10 known-outcome dread（R-18）
本件は「誰も罰されていない・まだ裁判が1つも開かれていない」が周知の外形＝**行き先を宣言して how を売る**構成。ACT I 17.1% "was nothing" → ACT V 85.5% "Not one of those cases has been tried." → ENDING "No court has ever ruled…"。Titan パターンの移植 ✓。**tonal reset（20–40s・55–70%帯）= ATSDR 撤回の 60.9%** ✓。

### R2-11 息継ぎ字幕適性・発音注意
短文主体・カンマ節が息継ぎ単位で切れる。**発音注意リスト（CODEX_B 向け）:** Lejeune（**ル・ジューン** /ləˈdʒuːn/ — 米海兵隊/地元の標準。フランス語風「ルジュヌ」は誤り・**要試聴**）・Tarawa Terrace（タ**ラ**ワ）・Hadnot（**ハド**ノット）・Ensminger（**エンズ**ミンガー）・Partain（パー**テイン**）・Jacksonville・tetrachloroethylene・trichloroethylene・halogenated・Fiolek・Vidana・Pendleton・McPherson。**"CHCL2BR" は綴りで読ませない**（VO では引用のこの部分を読まず、AE/OST に出す判断を CODEX_B に申し送り）。

**R2 判定: PASS**。

---

## R3 — INDEPENDENT REVIEW（別エージェント・fresh eyes・FIX AUTHORITY）— **実施 2026-07-29 · 判定 PASS（欠陥19件を修正のうえ）**

**Reviewer:** 独立エージェント。本パッケージの執筆に一切関与していない。**R1/R2 の申告値は1つも信用せず全て再計算した。** WebSearch はセッション上限に達していたため、**一次資料の直接 fetch（govinfo 公聴会全文 / ATSDR / VA / EDNC ドケット / GAO / 現行法文 / NAP）＋ リポジトリ上での機械計測＋アーカイブ検索の実再実行**で作業した。**FIX AUTHORITY を行使し、下記は全て修正済み。**

> **一行要約:** 台本の**文章**はおおむね健全だった。壊れていたのは ①**時間の算術**（クールドオープンが注記の45%増、スティング位置が物理的に不可能）、②**訂正の伝播**（訂正は台本には入り、CODEX_A の絵には入っていなかった＝ACT2 にテレビ資産が11点残存、しかもサムネアンカー）、③**「濃度の二重帳簿」という誤診**（実際は矛盾していない）、④**逐語の帰属**（ATSDR が言っていない文字列が verbatim として台帳に入っていた）。**②が本レビュー最大の発見。**

---

### R3-0 全メトリクスの独立再計算（R2 の申告を破棄して測り直した）

計測器は自前で書いた。語オフセットは `check_script_length.py` と**同一の抽出規則**で数え、**開幕のタイミングだけは「TTS が実際に読む発話トークン」で数え直した** — `1985` は 1 語ではなく `nineteen eighty-five` の 3 語として発話される。**R2 はここを書記素で数えており、それが時間の誤りの根本原因。**

| 項目 | R2 の申告 | **R3 実測（修正前）** | **R3 実測（最終）** | 基準 | 判定 |
|---|---|---|---|---|---|
| narration 語数 | 4,737 | 4,737 ✓ | **4,738** | 4,600–4,750 | ✓（残余19語） |
| cold-open callback | 80.2% | 80.18% | **79.96%** | 70–90% | ✓ |
| primary reveal 開始 | 82.1% | **81.38%**（申告 0.7pt 過大） | **81.17%** | 65–85% | ✓ |
| 最後の新事実 | 91.8% | **91.51%** | **91.44%** | ≤92% | ✓ |
| ENDING 開始 | 92.2% | 92.19% | **92.12%** | — | ✓ |
| MID reveal 開始／芯 | 38.9 / 49.4% | 38.91 / 48.81% | **38.74 / 48.57%** | 45–60%（芯） | ✓ |
| tonal reset | 60.9% | 60.90% | **60.52%** | 55–70% | ✓ |
| Janey の一節 | 15.6% | **14.63%** | **14.44%** | 1回のみ | ✓ |
| emotion-command grep | 0 | **0** | **0** | 0 | ✓ |
| narrator imperative（非bookkeeping） | 2 | **1** — R2 が2本目に数えた "Read carefully, that is a statement about paperwork" は**独立文でなく従属節**で命令文として立っていない | **1** | ≤2 | ✓ |
| AI-smell grep | 0 | **0** | **0** | 0 | ✓ |
| 因果禁止語 grep（water killed / caused her / linked to 等） | — | **0** | **0** | 0 | ✓ |
| short-punch share | 26.6% | **26.3%** | **26.4%** | 20–35% | ✓ |
| you/your | 2.1/1000w | **2.11** | 2.11 | ≤8 | ✓ |
| 修辞疑問 | 0.21/1000w | **0.21** | 0.21 | ≤2 | ✓ |
| 最長 number/name/date-free 連続 | 96語 / 33s | **44語 / 14.8s**（申告は2倍以上の過大） | **46語 / 15.5s** | ≤270語 / 90s | ✓ |
| 最長段落（re-hook 間隔） | 143語 / 49s | **152語 / 51s@178・54s@170.4** | 152語 | ≤150s | ✓ |
| act 語数配分 | ACT5 22.5% | **ACT5 23.50%**（CODEX_A §2 の概算行は 900語＝19%と書いていた。実測 1,113語） | 同 | act内リバーサル要 | ✓（3本あり） |

**ラダー・grep・密度は全項目 PASS。**R2 の申告には7か所の誤差があったが判定は覆らない。覆るのは次項だけ。

---

### R3-1 ★★ 欠陥 H-1（HIGH）— クールドオープンの尺とスティング位置が算術的に成立していなかった

発話トークンで数えると v001 のクールドオープンは **142トークン = 47.8s @178.1 wpm / 50.0s @170.4**。台本ヘッダと DESIGN §2 はこれを **「~33s」**、スティングを **0:33–0:38** と書いていた。**45%の過大申告。**

| 要素 | v001 実測 @178.1 | 規則 | 判定 |
|---|---|---|---|
| 人物（"a Marine Corps drill instructor"） | 3.37s | ≤5s | ✓ |
| **不可逆イベント動詞 "lost"** | **5.73s** | **≤5s** | **✗ FAIL** |
| BUT-loop 開始 | 27.29s | ~0:32まで | ✓ |
| **BUT-loop の芯** | **35.71s** | スティング(0:33–0:38)より前 | **✗ FAIL — スティングがループを文の途中で断ち切る** |

**R-11「スティングはループ成立後にのみ置く」が、注記どおり実装したら物理的に破れる**構造だった。R2 の craft A1 は「人物は word 11 ≈ 3.8s」で通していたが、これは書記素カウントである。**26/26 は実際には 25/26 だった。**

**ハウス基準（EP56 を実測）:** クールドオープン **113トークン = 38.1s**、イベント動詞 "watched" は **4.38s**。EP58 は **26%長く、イベントは1.35s遅い**。

**適用した修正:** 冒頭日付を `On the twenty-fourth of September 1985,`（発話9トークン）→ **`In September 1985,`（4トークン）**。完全な日付（3:35 p.m.・Tuesday・24 September 1985）は **ACT I に1回だけ**残り、**C1「反復しない細部」がむしろ強化され重複も消えた**。さらに `and when it was over` 削除、`usually`→`always`、`of his life` 削除、`contaminated wells`→`wells`。**注記を実測に書き換え（0:33→0:44）。**

| 要素 | 修正後 @178.1 | @170.4 | 判定 |
|---|---|---|---|
| 人物 | **2.02s** | 2.11s | ✓ |
| 氏名 "Jerry Ensminger" | 3.71s | 3.87s | ✓（R-9 の0:15に大幅内側） |
| **不可逆イベント動詞 "lost"** | **4.38s** | 4.58s | **✓ PASS（EP56 と同値）** |
| BUT-loop 開始 | 23.25s | 24.30s | ✓ |
| **BUT-loop の芯** | **31.67s** | 33.10s | **✓ PASS（~0:32 に着地）** |
| 全長 | **43.5s** | 45.4s | スティングは 0:44 |

**残す偏差（意図的・記録する）:** 43.5s は EP56 の 38.1s より 5.4s 長い。これ以上は切らなかった — 残るのは「四年前／十六年前」の算術と "on a printed form"（マクロループ C2 の植え付け）だけで、**どちらも本作の背骨**。R-10（ループを0:32までに植える＝23.3s ✓）と R-11（スティングはループ成立後＝31.7s の後 ✓）は**規則の文言としては両方満たす**。**壊れていたのは注記であって構造ではない**、というのが判定。

---

### R3-2 ★★★ 欠陥 H-2（HIGH · 本レビュー最大の発見）— 訂正が「台本には入り、絵には入っていなかった」

CODEX_A §4.3a の `also_thumb` 集合に **`LEJ-S058 (a television's cold light thrown across a dark kitchen wall … — the broadcast)`** と書かれていた。S058 は **ACT 2（AUGUST 1997 ＝ Ensminger の発見）**の still であり、**ACT 2 のサムネイル背景アンカー**でもある。

**訂正3（CL-15 / §W）はこう書いてある** — *"he saw it on the evening news"（Ensminger について）は禁止／発見の媒体を特定しない／**テレビ場面を Ensminger に演出しない***。台本は完璧に守っていた。**CODEX_A は1文字も守っていなかった。**

禁止文の説明ではなく**実プロンプト行を読んで**確認した残存物:

| id | act | v001 の内容 | 問題 |
|---|---|---|---|
| motif 名 | 2 | **`the_news_that_travelled — 3 — S052, S056, S058`** | motif 名そのものが「届いたニュース」 |
| S052 | 2 | wood-veneer console television, screen a blue-white glow | Ensminger の幕にテレビ本体 |
| S053 (★HP) | 2 | anonymised adult … **the changing light of a television washing over one shoulder** | 「テレビを見て固まる男」＝禁止された発見場面そのもの |
| S055 | 2 | **a television remote control** on a chair arm | 同上（小道具） |
| S056 | 2 | hallway … **pulsing with the cold changing light of a television** | 同上 |
| **S058** | 2 | television light across **a dark kitchen** … *"an ordinary room receiving news"* | **禁止語 "kitchen / television / news" の三重一致、かつ also_thumb** |
| S004 | 0 | doorway … **the cold flicker of a television** across his back | HOOK にも同じ含意 |
| F004 | 0 | `television_glow_on_wall.mp4` | 同上 |
| F053 / F054 | 2 | `crt_television_static_dark` / `television_glow_on_wall_02`（F054 は S058 担当） | 同上 |
| M02 | 0 | seed `television_light_about_to_change` | i2v で「テレビの光が変わる瞬間」 |
| M11 | 2 | seed `a_man_standing_still_before_a_screen` | 「画面の前で固まる男」 |
| L04 | — | overlay `television_flicker_cold` | 幕の制限なし |

**絵は台帳だけでなく台本にも DESIGN にも反していた。** DESIGN §1a の per-act 表は ACT II にテレビを**一切割り当てていない**（L1=タイプライタ/封筒/書庫、L3=静止/白紙のノート/バインダー誕生、L4=受話器/封筒/引き出し）。**CODEX_A だけが単独で逸脱していた。** 機械ゲートは検出不能 — `BANNED_ACCURACY` にテレビ語が無いからである。

**適用した修正:**
- ACT 0 / ACT 2 からテレビを**全撤去**（S004 / S052 / S053 / S055 / S056 / S058、F004 / F053 / F054、M02 / M11 の11点）。
- motif 名 `the_news_that_travelled` → **`the_room_that_was_not_told`**。
- **S058（also_thumb）を差し替え** → *"A single lit kitchen window seen from far out in a dark yard, the only light anywhere in a low brick house…"* ＝**台本が実際に書いている絵**（*"A retired drill instructor at a kitchen table in North Carolina, working through the evening after dinner"*）。暗所に一点光源で、サムネ背景としても旧案より強い。
- **テレビを記録が置いている場所へ移設** → **ACT 4 の S133**（＋F136 を S133 担当に振替）。CL-25 verbatim: *"Michael became involved with the Camp Lejeune after viewing a television report about Camp Lejeune while he was treating his breast cancer."* ACT 5 の広告ビート（F181 / M36 / S177–S178）は**元から正しい**ので温存。
- overlay `L04` に `"act_restriction":[4,5]` を付与。
- **機構化（意志でなく仕組み）:** CODEX_A §1.2 に **`R-TVMEDIUM`** を新設、`--verify` 用の正規表現つき機械チェックを本文に記載（`act` が 4/5 以外でテレビ語ヒット → exit 1）。DESIGN §6 のゲート列と ledger §W にも同じ規則を追記。

**残存確認:** 全文再掃引でテレビ語のヒットは **act 4 の S133/F136 と act 5 の S177/S178/F181/M36、および規則本文だけ**。act 0 / act 2 のヒット **0**。

---

### R3-3 ★ 発注の本丸① — **5件の訂正の「過剰訂正」再検査**

**結論を先に: 5件のうち3件が過剰訂正だった。** 訂正の**結論**（何を画面から外すか）は5件とも維持できたが、**根拠は3件が誤っており、うち1件は台本が画面で虚偽を主張していた。** 全て修正済み。

> **R1 の失敗モードは一貫している** — **2007年公聴会 transcript を1本 grep して見つからないことを「存在しない」の証明として扱った。** テレビ・Hargett・250ガロンの3件が同じ形で滑り、曝露総数も同じ形で滑った。**否定的主張は必ず「どの文書を見たか」で scope しなければならない。**
> ⚠ **provenance 規律:** 下記のうち **R3 が自分で一次文書を開いて確認したもの**と、**調査パスの報告に留まるもの**を区別して書いた。後者は台帳でも `UNVERIFIED` と明記してある。

| # | 訂正 | R3 の独立検証 | **判定と処置** |
|---|---|---|---|
| **1** | 「~1,000,000 exposed」を全カットし、**画面で訂正を宣言** | **★過剰訂正。しかも台本が画面で虚偽を主張していた。** R1 の旧文は *"appears in advertising, **not in the record**"*。**R3 はその「record」を開いて figure を見つけた** — **House Science & Technology, Subcommittee on Investigations and Oversight,「Camp Lejeune: Contamination and Compensation, Looking Back, Moving Forward」2010-09-16, Serial No. 111-108**（`CHRG-111hhrg58485`・**R3 が primary .htm を fetch して読んだ**）。**Hearing Charter:** *"As many as one million individuals have been exposed to these contaminants."* **Miller 委員長 prepared statement:** *"For thirty years, as many as one million Marines and their families training and living on the base at Camp LeJeune were exposed to toxic chemicals in their drinking water."* ⚠ **ただしこれは省庁の推計ではない** — 小委員会スタッフの文章と、議員による規模の characterisation である。否定側も R3 が独自に固めた: **ATSDR のランディング／About／FAQ／Health Studies、VA の曝露ページ、どこにも総数は無い** | **✗→修正済（本レビューで最も出荷リスクが高かった1件）。** 旧文は**証明不能な普遍否定**であり、**2010年公聴会を1回検索すれば反証される**。→ 画面文を **R3 が自分で開いて確認できた事実ちょうど**に置き換えた: ***"There is no official total. No federal health agency has ever published one. The number you may have seen — around a million — comes from a congressional hearing in 2010."*** **3節すべて検証済みで、しかも旧文より damning**（「広告の数字」ではなく「議会が出典なしに口にした数字」になる）。⚠ **✗「630,000」の罠を台帳に登録** — あれは Nebraska Ordnance Plant の TCE の ppb 値であって人数ではない |
| **2** | Janey は Lejeune で「宿った」 | 2007年公聴会を R3 が自分で fetch し逐語一致: *"My daughter Janey was **conceived** while her mother and I lived in one of the base family housing units…"* | **訂正は正当。変更なし** |
| **3** | キッチンのテレビは Ensminger ではなく Partain | **★過剰訂正（人物の取り違えではなく、「無い」と言ったのが誤り）。** **両者にテレビ由来があり、矛盾しない。** Partain のものは2010年議会記録に verbatim（R3 確認済み）。**Ensminger のものも実在し**、調査パスは **C-SPAN *Q&A*（Brian Lamb・2012-03-15）の本人発言**に同定した — *"that revelation on the news didn't happen until 1997… I was walking into the living room with a plate of spaghetti, and the reporter on the TV said… And I dropped my plate of spaghetti right there on the living room floor."* ⚠ **R3 自身は C-SPAN を開いていない＝UNVERIFIED として台帳に明記。** また**「キッチン」ではなく「リビング」**で、kitchen 表記は映画クリップの "UNIDENTIFIED PARTICIPANT" 由来＝推論 | **訂正の結論は維持、根拠を全面的に組み替えた。** *「彼のテレビ談は存在しない」は誤り*。正しい規則は ***「この映画は彼の発見の媒体を語らないと決めた以上、絵でもそれを主張してはならない」*** という**整合性の規則**で、これはテレビ談の真偽と無関係に成立する。→ 台帳を書き換え、**R-TVMEDIUM** として機械ゲート化（R3-2）。✓ **将来解禁するなら道筋も書いた:** C-SPAN を帰属してナレーションで語る→**そのときだけ**絵に出してよい |
| **4** | Grainger の化学者は Hargett ではなく **Bruce A. Babson** | **★部分的過剰訂正。Hargett は実在する。** **R3 が2010年公聴会を開いて確認:** Hearing Charter verbatim *"…previous conversations she had had with **Grainger Lab co-owner Mike Hargett**."* Partain 証言 *"**Mr. Hargett** then contacted Camp Lejeune's Base Supervisory Chemist, Elizabeth Betz, and informed her that the synthetic organic cleaning solvents PCE and TCE were found in both samples…"* **2010年公聴会に25回登場・2007年公聴会に0回** — R1 が 2007 だけを見たから false negative になった | **✗→修正済。台本で Hargett を名指しするようにした。** 二人は**別の行為**をしている: **Hargett が1982年5月に電話で警告し、Babson が同年8月10日の書簡に署名した。** どちらも Grainger、どちらも基地に警告した側で、**どちらも wrongdoer ではない**。→ 台本を *"In May 1982 a co-owner of a private contract laboratory called Grainger, **a chemist named Mike Hargett**, telephoned the base's own supervising chemist… In August **his colleague Bruce Babson** put it in a letter to the Commanding General"* に。**Betz は引き続き役職のみ** |
| **5** | 「250ガロンのタンク」は出典不明 → カット | **★過剰訂正（理由づけが誤り）。** 250ガロンは **EPA の一次文書4本に逐語で存在**（OU-1 ROD 1993-01-26 pp.21/77/104、OU-2 ROD 1994-09-06 pp.11/70、Third Five-Year Review 2013 p.20、ROD abstract）。**ただし「地下に漏れた量」ではなく「建物脇の地上貯蔵タンクの容量」** | **カットの結論は維持、理由を差し替え。** *"unsourceable"* ではなく **「容量であって流出量ではなく、耳では流出量として聞こえる」**。★同時に**記録が実際に支持するもっと強い素材**を台帳へ（CL-11）: 貯蔵タンクは**浄化槽から4フィート**、使用済み PCE は**浄化槽へ直接投棄**、1960年代に**床排水を増設**、蒸留残渣は**30年で約1トンを砂利道の穴埋めに散布**、**ATSDR 再構成値＝1953–1985 に土壌・地下水へ到達した PCE 約6,000ポンド＝約430ガロン＝ドラム約7.8本、ATSDR 自身が「最小値」と呼ぶ**。**次版の第一候補**（v001 は語数帯に余裕が無く未採用） |

**★訂正1と4の副産物 — 2010年公聴会を開いたことで、R1/R2 が持っていなかった一次情報が3つ手に入った:**
1. **分析票の日付は「受領日」である。** Hearing Charter が1980年10月の様式のメタデータを再録している: *"**Date Collected: 21 Oct. 1980, Date Received: 30 Oct. 1980, Data Analyzed: 31 Oct. 1980**."* → **「30 October 1980」は受領日。** 台本を *"on the analysis of samples"* → ***"on a Hadnot Point sample form"*** に変更（どの読みでも真）。9 March 1981 は元から *"on samples dated…"* で中立なので維持。**✗「採取された」「分析された」とは言わない。**
2. **1980年10月の筆跡には名前がある** — ***William C. Neal, Jr., Chief, Laboratory Services, U.S. Army Environmental Hygiene Agency***。⚠ **✗ この名前を CLW 0443（1981年3月）に転用してはならない。** ENDING が乗っているのは3月の手であり、**そちらは依然として無名**。片方だけ名前を出すと視聴者が両者を融合させるので、**v001 はナレーションでどちらも名指さない**（10月分だけは将来解禁可、と台帳に明記）。
3. **✗ 年表を崩壊させかねない誤帰属を1件、事前に潰した。** *"Water highly contaminated with other chlorinated hydrocarbons (solvents)!"* は **陸軍環境衛生局の TTHM 様式への書き込みであって Grainger のものではなく**、Grainger より約18か月早い。**Army 1980–81 → Grainger 1982 → 井戸停止 1984–85** という Act III の背骨は、両者を混ぜた瞬間に死ぬ。**R3 が台本・§W・CL-21/CL-23 を全て確認 → 本パッケージは全箇所で正しく陸軍に帰属している。修正不要。後続パスが「整理」して壊さないよう記録した。**

**★もう1件、台帳の帰属を締めた:** **Bove et al. 2024（EHP）は ATSDR の公式見解ではない** — 著者は ATSDR の科学者だが、論文は *findings do not necessarily represent the official position of CDC/ATSDR* という定型 disclaimer を負っている。**✗「ATSDR states/found」と書いてはならない。** ✓ 台本は元から *"a cancer incidence study"* / *"The 2024 study"* としか呼んでおらず無傷。**ATSDR を finder として名指してよいのは2017年 causality assessment（CL-29a）だけ。**

### R3-4 ★ 発注の本丸② — **ベンゼン／塩化ビニル濃度の「二重帳簿」を決着**

**R1 の診断は誤診だった。矛盾は存在しない。軸は「井戸 vs 蛇口」1本である。**

ATSDR FAQ ページを直接 fetch（2026-07-29）したところ、**ページが自分でレジスタを明示していた**:
> *"In **one Hadnot Point supply well**, benzene levels as high as **720 μg/L** were detected."*
> *"In **another Hadnot Point supply well**, vinyl chloride levels as high as **655 μg/L** were detected."*

並行検証が **Chapter A の原表まで降りて特定した**:

| 数値 | レジスタ | 実測/モデル | 日付・出典 |
|---|---|---|---|
| ベンゼン **720 µg/L** | **井戸 HP-602** | 実測 | 1984-12-10・Table A5（*"ranged from 1.6 μg/L of benzene in well HP-608 to 720 μg/L of benzene in well HP-602"*。Table A5 全体の最大値） |
| 塩化ビニル **655 µg/L** | **井戸 HP-651** | 実測 | 1985-01-16・Table A4 |
| ベンゼン **12 µg/L** | **finished water** | **モデル** | 1984-04（*"Reconstructed benzene concentrations in Hadnot Point drinking water reached a maximum level of 12 μg/L during April 1984."*） |
| 塩化ビニル **67 µg/L** | **finished water** | **モデル** | 1983-11（同上の再構成。TCE 783 / DCE 435 / PCE 39 も同月） |
| **PCE 215 µg/L** | **finished water・Tarawa Terrace** | **実測** | **1985-02-11**（*"The maximum observed PCE concentration was 215 μg/L measured on February 11, 1985"*。モデル最大は 183・1984-03） |
| **TCE 1,400 µg/L** | **finished water・Hadnot Point** | **実測** | **1982-05**（*"Measured TCE concentrations in finished water at the HPWTP during the period May 1982 through February 1985 ranged from 1.2 μg/L to 1,400 μg/L"*） |

**なぜ矛盾しないか:** グラブサンプルは月平均を超えうるし、生の井戸水は混合・処理後の水を大きく超えうる。だから **1,400 > 783** も **720 > 12** も同時に真である。**CL-06（well 651 の TCE 18,900 ppb vs 蛇口の 1,400）と完全に同型。**

**判定と処置。**
- **「濃度を出さない」判断は維持。ただし理由を差し替えた。** ソースが矛盾するからではなく、**この映画が画面に出す濃度は全部「蛇口の数字」だから**。3桁の蛇口値の隣に4桁の井戸値を置けば視聴者は平均してしまう。
- **CL-05 を全面書き換え**（矛盾の記述→解決の記述）。**CL-04 に "drinking water" と実測日を追記。**
- **台本を修正:** *"In the Tarawa Terrace **supply**…"* は「井戸の供給」と誤読しうる。→ ***"In the **drinking water** at Tarawa Terrace…"* / *"In the **drinking water** at Hadnot Point…"***。**台本のレジスタが台帳と一字で一致した。**
- **⚠ 逆流防止を台帳に明記:** 「この決着は**台帳が事実を述べる許可**であって、**映画が数字を出す許可ではない**」。
- **★well 651 の罠を新たに封じた:** Ensminger の書面陳述は *"18,900 ppb of TCE and 655 ppb of Vinyl Chloride during early February 1985 testing"* と**1サンプルに束ねている**が、Table A4 は 655 を **1985-01-16**、2月4日サンプルは 168/179（口頭では633）としている。**✗ 18,900 と 655 を1つの読みに合成してはならない。**

---

### R3-5 ★ 新たに見つかった事実 — **警告は3回ではなく4回だった**

govinfo の2007年公聴会を R3 が自分で fetch し、Ensminger の prepared statement の年表を並べ替えずに取り直した。R1/R2 は3件（CLW 0436 / 0438 / 0443）としていたが、**間にもう1件ある**:
> *"Once again samples were taken of the same system on **30 January 1981** and the U.S. Army laboratory wrote on the analytical result form **You need to analyze for chlorinated organics by GC/MS**"*

**陸軍の研究所は Hadnot Point について、4か月10日の間に4枚の分析票に書いていた** — 30 Oct 1980 / 29 Dec 1980 / **30 Jan 1981** / 9 Mar 1981。CLW 番号は30 Jan の分だけ宣誓文に無い（**✗ 番号を付けてはならない**）。

**処置:** 語数帯に余裕が無いためナレーションは触らず、**AE カード8に載せた** — `30 OCT 1980 · "HIGHLY CONTAMINATED"`（4.5s）→ **`FOUR NOTES ON FOUR FORMS · 30 OCT 1980 · 29 DEC 1980 · 30 JAN 1981 · 9 MAR 1981`（5.5s）**。デッキ合計 81.5s → **82.5s**。台帳に **CL-21(d)** を新設。

⚠ **日付の性質は決着しなかった。** R3 の一読は 9 March を**採取日**とし（*"more samples … were **collected and analyzed**"*）、並行検証は3枚を**受領日**とし採取を 21 Oct 1980 / 18 Dec 1980 / 26 Feb 1981 とする。**両立しないまま。** → CL-21c のヘッジを**維持**し、台本の *"on samples dated the ninth of March 1981"* / *"on the analysis of samples from Hadnot Point"* という**どちらの読みでも真になる中立形**を正典とした。**✗「採取された」とも「報告された」とも言わない。**

---

### R3-6 15の load-bearing 主張 — 逐条判定

| # | 主張 | 判定 | 出典 |
|---|---|---|---|
| 1 | 汚染期間と物質（TT=PCE / HP=TCE＋PCE・ベンゼン・分解生成物 trans-1,2-DCE と塩化ビニル） | **CONFIRMED** | ATSDR "About Camp Lejeune" 逐語（R3 が fetch） |
| 2 | 濃度 PCE **215**（限度5）／TCE **1,400**（280倍）＝**両方 finished drinking water の実測** | **CONFIRMED＋強化**（実測日 1985-02-11 / 1982-05 を新規確定） | ATSDR FAQ 逐語 |
| 3 | ベンゼン720・塩化ビニル655 は**井戸**、12/67 は**モデル finished water** ＝矛盾なし | **RESOLVED**（R1 の「二重帳簿」は誤診） | ATSDR FAQ ＋ Chapter A Tables A4/A5（§R3-4） |
| 4 | 1980-81 の分析票の逐語（CLW 0436 / 0438 / 0443） | **CONFIRMED 逐語一致**、かつ **4枚目（30 Jan 1981）を発見** | govinfo CHRG-110hhrg37793 全文 |
| 5 | CLW 0443＝9 March 1981・Hadnot Point・"…(solvents)!" | **CONFIRMED**（⚠ 採取日/受領日は両論あり・中立形を維持） | 同上 |
| 6 | Grainger は1982年5月に Betz へ電話、**Bruce A. Babson**（"a chemist with Grainger laboratories"）が 1982-08-10 に司令官へ書簡（CLW 0592/0593） | **CONFIRMED 逐語一致** | 同上 |
| 7 | 井戸閉鎖 | **CONFIRMED（窓）／✗ 訂正（件数）** — ATSDR *Chapter A–Supplement 1* は Nov 1984–Feb 1985 に **8本**（HP-602 11/30・HP-608 12/6・HP-660 12/6・HP-634 12/14・HP-637 12/14・HP-651 2/4・HP-652 2/8・HP-653 2/8）＝**Nov–Dec 1984 は5本で「7本」ではない**。Tarawa Terrace は最悪の2本（TT-23/TT-26）が 1985-02-08、浄水場閉鎖は **1987年3月** | ATSDR FAQ ＋ Chapter A Supplement 1 |
| 8 | Janey: **Lejeune で宿った**・6歳で ALL・約2年半闘病・**1985-09-24 15:35 に9歳で死去** | **CONFIRMED** | 2007公聴会逐語 |
| 9 | Jerry が知ったのは **1997年8月**／死去からは **約12年**（13年ではない） | **CONFIRMED＋算術訂正** | 2023 下院軍事委員会記録＋自算 |
| 10 | Partain: 2007年・39歳・男性乳がん／2010年宣誓 **"one of 64 men"**／現在 **125人超** | **CONFIRMED**（"one of 64 men" は**口頭**証言。提出書面は "about sixty four"。台本は口頭版を引用＝正しい。"above a hundred and twenty-five" も PRE の "more than 125" に一致） | 2010公聴会 |
| 11 | 男性乳がんの疫学（Ruckart 2015・71/373・OR 1.14, 95%CI 0.65–1.97）と登録簿の並置 | **CONFIRMED＋文言強化**（下記） | Ruckart 2015 |
| 12 | ATSDR 1997 PHA →**2009-04-28 に自ら撤回**／ベンゼン譲歩 | **CONFIRMED（撤回）／✗ 訂正（1997年の結論の性格づけ）**（下記） | 2010公聴会 staff memo ＋ ATSDR |
| 13 | 2024-10-24 EHP の結論逐語と、台本が誠実に載せるヌル結果 | **CONFIRMED＋精密化**（軍側コホートの窓は **1975–1985**、1972–1985 ではない。1972-10 は民間従業員 arm のみ。larynx と soft tissue の CI は1をまたぐが、論文自身が *"Statistical significance testing was not used"* と述べ HR≥1.20 で screen しているので台本は誤っていない。**✗「統計的に有意」とは決して言わない**） | Bove 2024（PMID 39446420） |
| 14 | 法: 窓 1953-08-01〜1987-12-31（1957 から PL 113-235 で改正）／CLJA=PL 117-168 §804／**陪審を否定したのは議会でなく裁判所**（D.E. 133・2024-02-06・34頁・4判事連名） | **CONFIRMED 全項目。陪審命令は 2026-07-29 時点で依然有効**（第4巡回区は mandamus を却下、中間上訴の認証も無し、**実体判断をした上訴審は存在しない**） | 38 U.S.C. §1710 現行条文／D.E. 133 PDF／EDNC ドケット |
| 15 | 現在時制: **408,000 / 3,759**・**2,446人受領**・**$723,850,000**・**88%/2%**・**$10,000 / $24,000 / $405**・**Track 1 は公判ゼロ・期日ゼロ**・**D.E. 893 の 2026-10-30 は依然有効** | **CONFIRMED 全項目。** D.E. 894（2026-07-01）が 10月30日目標を明示的に再確認、**global settlement 未成立**。6/15 以降に新しい settlement status report は**提出されていない**＝408,000 等が**依然最新の裁判所提出値**。DOJ 自身のページ（2026-07-20 更新）は *"As of July 17, 2026, … settlement offers exceed $968 million and settlement payouts exceed $801 million."* 唯一の新規カレンダーは **2026-08-17 の status conference**（Jones 治安判事） | EDNC ドケット PDF／justice.gov |

**#11 の強化（適用済み）:** Ruckart の高曝露サブグループは **両方向に振れる** — PCE 1.20 / trans-1,2-DCE 1.50 / 塩化ビニル 1.19 が null 超、**TCE 0.93・ベンゼン 0.57・総汚染物質 0.82・居住期間 0.89 が null 未満**。著者自身 *"A monotonic exposure-response relationship was observed only for categorized cumulative exposure to PCE based on two exposed cases."* さらに **ATSDR 2017 は乳がん（男女）を TCE・PCE・ベンゼンいずれについても "Below Equipoise"（下から2番目）**に格付けしている。→ 台本の *"the science is suggestive and not established"* は**positive 側に寄りすぎ**と判定し、***"the results point both ways and nothing is established"*** に変更。**✗ 用量反応を示唆しない・TCE/ベンゼン/総量からの上昇を示唆しない。** → CODEX_B に「Partain のビートと causation リストを同一カードに置かない」を申し送り。

**#12 の訂正（適用済み）:** 台本の *"concluding that exposures were unlikely to have caused harm to adults"* を**削除**した。1997年 PHA（1997-08-04）は **ATSDR のサイトから撤去済み**（2004-10-01 以前の PHA/HC は全て retired・記録請求先へのリダイレクトのみ）で結論文が取得できず、さらに並行検証は**同 PHA が3件の past public health hazard（水道水の鉛・3系統の VOC 曝露・旧保育施設の農薬）を宣言していた**と報告した — 事実なら「無害と結論」は要約ではなく**性格づけの誤り**になる。→ 台本は **ATSDR が公表し、ベンゼンを落としていたので撤回した**という完全に典拠のある事実だけを述べる。付随して *"An agency withdrew its own **reassurance**… they were probably fine"* も *"withdrew its own **assessment**… published a judgement"* に変更。
**さらにベンゼン譲歩の引用を日付で固定した** — 強い方の文（*"should have been included in the PHA but was not"*）は **2009年5月8日の update 版**のもので、ATSDR は**現行ページで緩めた版に差し替えている**（*"…not enough data to rule out earlier exposures to benzene."*・2009-07-06 review）。**両版とも真正な ATSDR テキスト**なので、日付を打たないと批判者が現行ページを出して「誤引用」と主張できる。→ 台本を *"The reason ATSDR gave **that May**…"* に修正。
**「機関史上初の撤回」は ATSDR ではなく Partain の主張**（2009年4/7/10月・2010年1月の CAP 議事録に ATSDR 職員の同旨発言なし）。**台本は既に *"According to Partain's sworn testimony"* と帰属しており正しい。**

**補助的な是正（15件の外側だが load-bearing）:**
- **✗ 台帳の「ATSDR 逐語」が ATSDR の文字列ではなかった。** *"43 times higher…"* / *"280 times higher…"* は、ATSDR Water Modeling Summary の **2014/2016/2018/2021/2024 の5キャプチャのどれにも存在しない**。倍率は**我々の算術**（215÷5=43・1400÷5=280、両方正しい）。**台本は倍率を ATSDR に帰属していないので出荷物は無傷**だが、台帳の引用符を外し、**✗ AE カードで倍率を ATSDR に帰属しない**と明記。
- **✗ GAO-07-276 の帰属が誤っていた。** *"did not find any violations of federal law"* は **GAO 自身の所見ではなく EPA 犯罪捜査部（CID）の所見**（p.48: *"A criminal investigation conducted by EPA and reviewed by the Department of Justice (DOJ) did not find any violations of federal law…"*）。台帳の逐語を実文に差し替え帰属を明記。**台本は元から正しく書いており変更不要。**
- **✗ 新規の罠を1件、禁止として登録（CL-44a）:** 「EPA 捜査官が司法妨害での起訴を進言したが DOJ に覆された」説（Wikipedia／2009年 LA Times 経由で流布）は、**当の捜査官 Tyler Amon が宣誓で否定**している（*"I concurred with the Department of Justice's decision not to proceed with charges."* / *"No, I did not."*）。
- **ATSDR 2017 の術語は "sufficient causal evidence" ではなく "sufficient evidence for causation"**（定義文: *"Sufficient evidence for causation: the evidence is sufficient to conclude that a causal relationship exists."*）。4階層（Sufficient / Equipoise and Above / Below Equipoise / Against）は **IOM 2008** の VA 推定障害スキームであり、枯葉剤でも湾岸戦争でもない。→ **台本を ATSDR の術語に修正。** Sufficient 層には台帳が落としていた **TCE＋心奇形**と**ベンゼン＋NHL**も含まれる（台本のリストは**部分リスト**であり網羅を主張していない）。**⚠ ATSDR 自身の2017年 PHA は放棄されたカテゴリ "modest" をまだ使っている — PHA と assessment を並べて引用しない。**
- **CTS Corp. v. Waldburger は 7–2** であり **Camp Lejeune の事件ではない**（Asheville の電子部品工場事件）。台本は両方とも侵していない。台帳に注記。
- **2016年 MDL の却下理由は時効法だけではない**（discretionary function / Feres / 主権免除も独立の理由）。台本は §804(f) の文で discretionary function を別途扱っており誤導していない。台帳に「後の版で単一原因に『整えて』はならない」と明記。**MDL 判事は Thomas W. Thrash, Jr.**（Forrester ではない）。
- **§804(j)(2) は "later of" 条項**（行政請求否認から180日という第2の枝）。→ 台本を **"and for almost everyone it closed on the tenth of August 2024"** に修正。
- **D.E. 893 の週次会合は絶対ではない** — 原文は *"…absent a written request to the Settlement Masters for such exception and written approval by the Settlement Masters of the exception."* **台帳の引用が但し書きを省略記号で落としており**、台本がそれを絶対として書いていた。→ **台帳の引用を復元、台本を「settlement masters が書面で承認した場合のみ1週飛ばせる」に修正。** Settlement Masters は **D.E. 892/894 で指名**されており D.E. 893 ではない。
- **2010年公聴会の委員会名に疑義。** R1 は House Veterans' Affairs、独立検証は **House Science and Technology（Investigations and Oversight 小委員会）**とする。**決着せず。** 台本は *"a committee of Congress"* としか言わず安全だが、**DESIGN の AE カード12 は委員会名を画面に出していた** → **"sworn testimony to Congress, 16 September 2010" に変更**。**✗ 確定するまでどのカード・概要欄・字幕でも委員会名を出さない。**
- **VA の現行ページは対象疾患を「16」と書く**（2012年法の条文は15）。台本の「fifteen」は**2012年法が作った制度の記述として正しい**。出荷前の再確認項目として台帳に登録。

---

### R3-7 センシティビティ監査（本スレート最難・**プロンプト行を実データで読んで**判定）

- **★子どもの描写:** フラグ宣言文ではなく、**267本のリテラルプロンプトを機械抽出して全数正規表現掃引**した。`child|kid|toddler|baby|infant` に当たる**正のプロンプトは1行のみ** — **S021** の *"a child's chalk line faded on the concrete beside it"*＝**路面に残ったチョークの線**であり**子どもは写らない**。DESIGN §1 の「不在で運ぶ」原則そのもの。**病気の子ども・医療下の子ども・健康な子ども・棺・墓 = すべて0。** ✓
- **医療描写:** `hospital` の当たりは **F129（hospital_exterior_far_dusk）**と **S126**（*"A low mid-century naval hospital block seen from across a lawn at dusk … no signage or emblem"*）＝**遠景外観のみ**。診察・機器・ベッド・処置 = 0。✓
  - ⚠ **軽微な自己矛盾を1件発見・修正:** §1.1-3 は医療の気配の上限を「**無人の**待合の椅子列」と書いていたが、**S127 は匿名の成人が1人座っている**。DESIGN §1 は「匿名の成人」を明示的に許可しているので、**矛盾していたのは §1.1-3 の文言のほう**。→ 実プロンプトに一致させた（**絵は変更なし＝再生成不要**）。
- **実在人物の likeness:** `BANNED_PORTRAIT` を全267プロンプトに掃引 → **0件**。全人物行が `[HSTYLE]`（背向き／シルエット／目から下でクロップ／浅い被写界深度）で、`[HNEG]` は Ensminger・Janey・Partain・実在議員/判事/将官を名指しで排除。✓
- **`BANNED_ACCURACY` 掃引 → 1件ヒット（修正済み）:** **S129** の *"no **legible lettering**"* が `legible (…|letter)` に一致。**否定形なので絵は正しいが、書き手自身の機械ゲートが自分のプロンプトで exit 1 する**。→ *"every gilt title dissolved into an unreadable smear"* に変更。**修正後 0件。**
- **存命の公人:** 宣誓証言・本人発言のみ。内心/動機の付与ゼロ。*"They killed my daughter."* は台帳で封じられ台本でも不使用。✓
- **★クールドオープンが Janey について因果を主張していないか（発注の名指し確認）:** 修正後の第1文と BUT 文を並べて読んだ。
  > *"In September 1985, a Marine Corps drill instructor named Jerry Ensminger **lost** his nine-year-old daughter to leukemia."* … *"**But** the base where his wife had carried Janey **had been putting** industrial solvents into its own drinking water for decades…"*
  **2つの事実は "But" で並置されているだけで、両者を結ぶ動詞は存在しない。** 「水が→白血病を」に相当する述語は無い。**修正で動詞は "lost" と "had been putting" のまま＝この性質は変わっていない。** 因果 grep も0。✓
- **因果ファイアウォールの敵対的読み（両方向）:**
  - *被告寄りに寄りすぎていないか* — ACT III は *"It does not prove a conspiracy; a federal criminal investigation looked for one for eighteen months, found no violation of federal law…"* と政府に有利な事実を先に置くが、直後に *"What it proves is narrower and, in its way, worse"* で反転し **"took between three and six years to turn off the taps — and then did not go and find the people who had been drinking it"** に着地する。**逃げていない。**
  - *原告寄りに寄りすぎていないか* — ACT IV は登録簿（64→125+）を出した直後に *"That list is a registry one man assembled. It has no denominator and no control group."* と自分で殴り、OR 1.14 と CI が1をまたぐことまで言う。**R3 はこれをさらに厳しくした**（"suggestive"→"point both ways"）。
  - **判定: どちらにも寄っていない。** 残るのは「隣接による誤読」だけで、CODEX_B への申し送りとした。
- **広告レジスター:** $112M / 94,000本を**事実として扱い**、パッケージングには ドル記号・金額・claim 語・電話番号風要素・赤バナー禁止（R-ADadjacent）。法律事務所のスポンサーシップは受けない。✓

---

### R3-8 DESIGN の一次監査（§ごとに台本と突き合わせ）

| § | 監査 | 判定 |
|---|---|---|
| §0 | 563 cuts / mean_shot 3.16 / still-share 0.4334 / first-use 0.8650 / avg-uses 1.156 を**全部再計算 → 全一致** | ✓ |
| §0.5 | 「5件の訂正は binding」と書いてあるが、**書いてあるだけで CODEX_A に届いていなかった** | **✗→修正済** |
| **§1a 四層** | **L1 235/563=41.74% ／ L3 244/563=43.34% ／ L4 84/563=14.92% ／ 合計 100.00%** — 再計算し **CODEX_A §3.1/§3.3 と一字一致**。85/210=40.48%（★HP）と 18/42（人物 i2v 種）も**実データで数え直して一致**（`[HSTYLE]` 85 / `[STYLE]` 125 / 計 210） | ✓ |
| §1a の AE 行 | *"≈100 s"* と書いてあったが §3 の duration 列の実計は **81.5s** → **82.5s に統一**（カード8の増分込み） | **✗→修正済** |
| §1a / §7.0 の在庫点数 | *"111,821-item archive + 88,740-item factory shelf"* = 合計 200,561。**実測 `search_archive.py --stats` は 113,460**（image 93,403 / video 17,871 / audio 2,186、`review_required` 802 = 使用不可）。**アーカイブと factory 棚は別勘定ではなく同一インデックスに同居**している | **✗→修正済** |
| §2 | 台本の幕構造と一致。ただし **HOOK "~33s" が実測 43.5s**、スティング 0:33–0:38 も同様 | **✗→修正済** |
| **§3 AE 17枚** | **全17枚を1枚ずつ台帳行に当てた。捏造統計0。** カード位置も再計算ラダーと突合（card 9 表記38.9% vs 実測38.74／card 12 51.4% vs 51.13／card 14 60.9% vs 60.52／card 17 91.8% vs 91.44）＝**全て0.4pt以内**。⚠ **card 6 だけ台帳行が無かった**（"DIAGNOSED 1983" の 1983 は導出値でどの CL 行にも無い）→ **CL-14b を新設して導出を明文化し参照を張り替え**。**card 8 は4枚目の分析票を載せる形に強化。card 12 は委員会名を削除** | **✗×2→修正済／他 ✓** |
| §4 図ビート | **86 = 5+12+14+20+17+15+3**（再加算一致）。**86/(1790/60) = 2.883/min** ✓（下限75 = 2.5/min × 29.83）。`dochighlight` 0 / `quote` 0 / `votetally` 0 も宣言どおり | ✓ |
| **§5.1 尺算術** | 4,737→**4,738** に再ロック。178.1 wpm で narration **1,596.2s**、gap **184.8s**、total 1,790.0s、**53,700 frames**、mean_shot **3.163s**。**170.4 / 172 / 175 wpm も全部引き直して表にした**（gap 115.2 / 128.2 / 156.5、ratio 1.075 / 1.085 / 1.104 ＝全て band 内） | ✓（値更新） |
| **§5.3 再ロック手順** | **★算術の誤りを発見。** *"If measured speech exceeds **1,791 s**…"* — `gap = 1790 − speech − 9` なので speech 1,791 では **gap = −10s**＝「床を割る」どころか**存在し得ない**。~60s の gap 床が破れるのは **speech > 1,721.0 s**（4,738語なら **164.9 wpm**）で、EP55 の 170.4 実績を思えば**到達しうる**。→ **1,721 に訂正し、なぜ 1,791 があり得ないかを本文に残した** | **✗→修正済** |
| §5.4 | VO onset 0.0 / Brian 正典 / 実音声禁止 / 息継ぎ字幕 0.60s リード ＝台本と整合。スティング時刻のみ修正 | ✓ |
| §5 chapters | 7章・数値なし・結末なし・"settlement"/"$405"/"nobody" なし ＝**非スポイラー**（"The Two-Year Window" の "Two-Year" は数詞だが結果を漏らさないので許容と判定） | ✓ |
| §6 ゲート | **R-TVMEDIUM を追加** | ✓（強化） |

---

### R3-9 CODEX_A 整合（20行サンプル・チェックサム・S番号・★HP・アーカイブ検索の独立再実行）

**§3.3 チェックサム全項目再計算 → 全一致:**
```
[1] 563 = 244 + 235 + 84                             OK
[3] 244/563 = 43.34%  (<=45%)                        OK
[4] (235+84)/563 = 56.66%  (>=45%)                   OK
[5] 244/210=1.162 / 235/235=1.0 / 84/42=2.0          OK
[6] 487/563 = 0.8650  (>=0.70)                       OK
[7] 563/487 = 1.156   (<=1.4)                        OK
    487 = 210 + 235 + 42                             OK
```
**S番号 = S001–S210 が穴も重複もなく210行**（機械抽出。211件目は §5.9 パーサ契約の**書式サンプル**であり実プロンプトではない＝欠陥ではない）。**幕別 15/36/34/40/40/30/15 = 210 も範囲サイズと完全一致。** M01–M42 = 42（穴なし）／F001–F235 = 235（穴なし）。
**★HP = 85** — motif ヘッダの宣言合計（65ヘッダ／計85）と**本文の `[HSTYLE]` 行の実数85**が一致。i2v 種は `[HSTYLE]` 18 / `[STYLE]` 24 = 42。**§5.6 の per-act ★HP 内訳（3+16+14+15+16+18+3）も85に一致。**
**`also_thumb` = ちょうど4枚**（S001 / S058 / S104 / S186）。§4.3a と §5.7 で一字一致（S058 の説明文は R3 で差し替え済み）。

**20行ランダムサンプル（seed 58）** — S004 / S011 / S027 / S050 / S051 / S052 / S053 / S067 / S073 / S074 / S091 / S104 / S108 / S116 / S149 / S158 / S165 / S190 / S206 / S207。**20/20 が台本のビートに実際に対応し、禁止線（子ども・医療・likeness・可読文字・部隊章・数値）を1件も踏んでいない。** 特に S073（*"Then he started using index tabs"* の逐語対応）・S104（MID REVEAL の紙）・S149（ATSDR が自分の評価を棚に戻す）・S190（31本の因果 motion の deposition）・S207（SIGNATURE A の最終状態＝夜明けの空のグラス）は**台本の文と1対1で読める**。

**★アーカイブ検索の独立再実行（棚ラベル40%破損を「信じずに検証」）— 16本のうち5本を R3 が自分で叩いた:**

| # | R3 が実行 | R3 の実測 | 一致 |
|---|---|---|---|
| 2 | `search_archive.py "camp lejeune"` | **`-- 0 hits total`** | **✓** 「事件固有の実写ゼロ」という四層設計の根拠は本物 |
| 6 | `search_archive.py "faucet"` | 27 hits。**`AF-BG-0506__courtroom_interior.jpg` = "tap black faucet kitchen sink"**（theme `legal_court`）／**`AF-BG-9994__balance_scale_brass.jpg` = "water tap brass tap brass faucet"**／`AF-VFX-1117__water_splash_black_background.jpg` = "faucet sink tap tap water flow" | **✓** ファイル名・実体・theme すべて一致。**誤ラベルの実在を独立確認** |
| 4 | `search_archive.py "water tower"` | 16 hits。**`AF-BG-9073__rural_road_america.mp4` = "4k aerial drone video of water tower in the mississippi delta"**（37.0MB video, theme `property_home`） | **✓**（同検索6件目は NARA の `_quarantine` 行で `review_required`＝§7.1 が正しく除外） |
| 9 | `search_archive.py "marsh"` | 77 hits。**`AF-BG-21082__foggy_harbor_dawn.jpg` = "foggy marsh"**／**`AF-BG-35488__forest_fog_morning.jpg` = "fog marsh landscape wetlands"** | **✓** |
| 15 | `search_archive.py "congress hearing"` | **`-- 0 hits total`** | **✓** 公聴会の実写が在庫に無いという判断は本物 |

**判定: 5/5 が記載どおり。§7.0a の16行は捏造ではない。** 棚ラベル破損も実在を確認（`courtroom_interior`→蛇口、`balance_scale_brass`→蛇口、`rural_road_america`→給水塔、`foggy_harbor_dawn`→湿地）。**⚠ ただし在庫点数の記載だけは誤っていた**（§R3-8・修正済）。

**★regen list（CODEX_A の変更行 — まだ1枚も生成されていないので「再生成」ではなく発注前の差し替え）:**
```
STILL   : S004, S052, S053, S055, S056, S058(also_thumb), S129, S133
I2V SEED: M02, M11        （＋ manifest tags: M02, M11）
FACTORY : F004, F053, F054, F136   （F136 は covers_scene_id を null -> S133 に変更）
OVERLAY : L04             （act_restriction [4,5] を付与）
文書のみ : §1.1-3 の医療上限文言 / §1.2 に R-TVMEDIUM 新設 / §4.3a の S058 説明 /
          §5.5a Q4 watch-list に「夜の窓/夜の家」群を追加 / §7.0 の在庫点数 / §2 の語数・尺
```
**点数は1点も動いていない**（still 210 / factory 235 / i2v 42 / overlay 30 / thumb 3 / F 12 / cuts 563 / distinct 487）。したがって §3.3 のチェックサムも `check_prompt_diversity` の coverage も影響を受けない。

---

### R3-10 craft-checklist 26項目 — 独立再採点

**修正前 = 25/26。修正後 = 26/26。**

R2 は 26/26 と自己採点していたが、**A1 は落ちていた** — *"cold open = person + irreversible event inside 5s"* に対し不可逆イベント動詞 "lost" は **5.73s**（発話トークン実測）。R2 は `1985` を1語として数えており、TTS が3語で読むことを勘定に入れていなかった。**修正後 4.38s で PASS。**

他25項目は独立採点でも ✓ で一致。実測で裏を取ったもの: **D1**（emotion-command grep 0）／**E1** 26.4%／**E2** 2.11/1000w／**E3** 0.21/1000w／**E4** grep 0／**F1** 29.0/min／**F2** 最長46語=15.5s（cap 270語/90s）／**A5** 最長段落152語=51s（cap 150s）。
**C1（反復しない細部）は R3 の修正でむしろ強くなった** — 完全な日付 "3:35 p.m., Tuesday, 24 September 1985" が、クールドオープンとの重複を解消して **ACT I の1回だけ**になった。

⚠ **チェックリスト自体への所見（次話への申し送り）:** 26項目は**今回の2大欠陥をどちらも検出できなかった** — 尺の算術（A1 を書記素で通してしまう）と、訂正の伝播（そもそも絵を見る項目が無い）。**推奨する追加2項目: 「A0 — 開幕の各要素の位置を*発話トークン*で測る」「H1 — 台帳の各訂正が CODEX_A の実プロンプト行に到達しているか grep で確認する」。**

---

### R3-11 未達のまま残した項目（正直に記録する）

- **NRC 2009 委員会自身の結論文** — nap.nationalacademies.org の該当章は**画像化されており本文が取れない**（R1 と同じ壁）。CL-30 の「海兵隊側の宣誓による characterisation として帰属、または省略」を**維持**。台本は不使用。
- **2016年 MDL 命令の逐語** — CourtListener と camplejeunecourtinfo の PDF は**いずれも JBIG2 画像**で、本セッションのどの fetch でもテキスト化できなかった。**「井戸が使用停止になった年」を 1985 とする読みと 1987 とする読みが両立してしまう**ため、**台本から年の算術（「1985→1995」）を削除**した。
- **1997年 PHA の結論文** — ATSDR がサイトから撤去済み（2004年以前の PHA/HC は全て retired）。→ 台本から性格づけを削除（§R3-6 #12）。
- **分析票の日付が採取日か受領日か** — 二読が対立したまま。中立形を正典化（§R3-5）。
- **ABC One-Hour Cleaners の営業年 / EPA Superfund プロファイル** — 未取得。台本は営業年も容量も言わない（CL-11）。
- **GAO-07-933** — **GAO-07-933T**（2007-06-12 の証言版・*"Defense Health Care: Issues Related to Past Drinking Water Contamination at Marine Corps Base Camp Lejeune"*）として実在を確認。GAO-07-276 の証言版であり台帳の主張を動かさない。
- **Murtha の逐語** — §VERIFIED-VERBATIM #19 を **⚠ 隔離**した。同じ govinfo 記録に対して R1 と R3 が**別の文字列**を得た（prepared statement と口頭の差と推定）。**実体（18か月の EPA 刑事捜査・DOJ の不起訴）は H で無傷。台本はこの引用を使っていないので出荷物に影響なし。** 一方を文字照合できるまで**画面使用禁止**。
- **ATSDR 2017 の "Equipoise and Above" 層の完全リスト** — 抽出時に列ズレが起きた由で **MEDIUM**。台本はこの層を使わない（Sufficient 層のみ）ので影響なし。
- **2010年公聴会の委員会名** — 二説対立のまま。台本は "a committee of Congress" で安全、カードから委員会名を削除（§R3-6）。

---

### R3-12 深刻度別の欠陥一覧と処置

| 深刻度 | # | 欠陥 | 処置 |
|---|---|---|---|
| **HIGH** | H-1 | クールドオープンが注記の45%増（47.8s vs ~33s）。不可逆イベント動詞 5.73s（>5s 違反）。BUT-loop の芯 35.7s ＝**注記どおりにスティングを置くとループを断ち切る** | 圧縮＋日付短縮 → イベント 4.38s／ループ芯 31.7s／全長 43.5s。注記を実測に是正。DESIGN §2・§5.4 も同期 |
| **HIGH** | H-2 | **訂正3（テレビ）が CODEX_A に伝播せず、ACT0/ACT2 にテレビ資産11点が残存。うち1点は ACT2 のサムネアンカー** | 11点を全書き換え・テレビを ACT4（Partain）へ移設・**R-TVMEDIUM を機械ゲート化**して台帳/DESIGN/CODEX_A の三箇所に固定 |
| **MED** | M-1 | ACT II *"almost thirteen years after she died"* が算術的に誤り（実際11年11か月）で、ACT I の *"for twelve years"* と**自己矛盾** | **"almost twelve"** に修正。CL-14b で導出を明文化 |
| **MED** | M-2 | ACT V が**出典未確認の年の算術**（「井戸1985→時効1995」）を事実として断定 | 削除し *"taken out of use in the nineteen-eighties"* に。CL-33 に二読の食い違いを記録 |
| **MED** | M-3 | ACT V が D.E. 893 の週次会合を**無条件**として語っていた（台帳の引用が但し書きを省略記号で落としていた） | 台帳の引用を復元、台本を「書面承認があれば1週飛ばせる」に |
| **MED** | M-4 | **井戸の本数「seven of them」が ATSDR の per-well 表と不一致**（Nov–Dec 1984 は5本、Nov 1984–Feb 1985 で8本） | 件数を削除し **"came out of service between November 1984 and February 1985"** に。CL-24 に8本の実名と日付を記録 |
| **MED** | M-5 | ACT IV が**1997年 PHA の結論を性格づけ**していた（検証不能・かつ「public health hazard を宣言していた」との対立報告あり） | 性格づけを削除。*"reassurance"→"assessment"* も同期 |
| **MED** | M-6 | ベンゼン譲歩の引用が**無日付**で、ATSDR が現行ページで緩めた版に差し替えている | 台本を *"The reason ATSDR gave **that May**…"* に。台帳に両版と日付を記録 |
| **MED** | M-7 | Ruckart の *"suggestive and not established"* が **positive 側に寄りすぎ**（サブグループ ORs は両方向・ATSDR は乳がんを "Below Equipoise"） | ***"the results point both ways and nothing is established"*** に |
| **MED** | M-8 | 英国綴り（leukaemia×9 / litre / oesophagus）が、**米国の海兵隊・米連邦法・ATSDR の逐語（"leukemia" "esophagus"）と同居**。ハウス実績も米国題材は米国綴り（EP50/52/55） | 米国綴りに統一（11箇所） |
| **MED** | M-9 | DESIGN §5.3 の再ロック閾値 **1,791s が算術的に不可能**（gap = −10s）。正しくは **1,721s**（＝164.9 wpm） | 訂正＋根拠を本文に記載 |
| **MED** | M-10 | 台帳が **ATSDR が言っていない文字列（"43 times higher" / "280 times higher"）を verbatim として掲載** | 引用符を外し、倍率は「我々の算術」と明記。**✗ カードで ATSDR に帰属しない** |
| **MED** | M-11 | 台帳が **GAO の所見でないものを GAO の逐語として掲載** | p.48 の実文に差し替え、EPA CID への帰属を明記（台本は元から正しい） |
| **MED** | M-12 | AE カード12が **2010年公聴会の委員会名を画面に出していた**（二説対立・未決着） | *"sworn testimony to Congress, 16 September 2010"* に変更 |
| **LOW** | L-1 | S129 の *"no legible lettering"* が**自分の `BANNED_ACCURACY` 正規表現に一致** | ハウス表現 *"unreadable smear"* に |
| **LOW** | L-2 | §1.1-3 の医療上限「**無人の**待合椅子」が S127（匿名成人1名）と矛盾 | 文言を実プロンプトに一致（絵は変更なし） |
| **LOW** | L-3 | AE card 6 の "1983" にどの CL 行も対応していなかった | **CL-14b** 新設・参照を張り替え |
| **LOW** | L-4 | §1a の AE 時間 *"≈100s"* が §3 の実計と不一致 | **82.5s** に統一 |
| **LOW** | L-5 | 在庫点数 "111,821 + 88,740" が実測 **113,460** と不一致（別勘定ではなく同一インデックス） | 実測と内訳に差し替え |
| **LOW** | L-6 | §VERIFIED-VERBATIM #19（Murtha）が二読で別文字列 | ⚠ 隔離。画面使用禁止（台本は不使用） |
| **強化** | E-1 | 分析票の警告は **3回ではなく4回**（30 Jan 1981 を発見） | CL-21(d) 新設・**AE card 8 を4枚シーケンスに強化**（4.5→5.5s） |
| **強化** | E-2 | ベンゼン/塩化ビニルの「二重帳簿」は**誤診**。井戸 vs 蛇口の1軸だった | CL-05 全面書き換え・CL-04 に実測日とレジスタ追記・**台本を "in the drinking water at…" に修正** |
| **強化** | E-3 | 訂正1に **VA 自身の曝露ページ**という新しい否定証拠 | CL-08 に追記。**画面の訂正文はそのまま出せる** |
| **強化** | E-4 | 流布する「EPA 捜査官が起訴進言→DOJ が却下」説は**本人が宣誓で否定** | **CL-44a として ✗ 登録**（将来の逆流防止） |
| **強化** | E-5 | ATSDR の術語は *"sufficient evidence for causation"*；Sufficient 層に **TCE＋心奇形**と**ベンゼン＋NHL**が欠けていた | 台本を術語に修正・CL-29a に4階層と完全リストを記載 |

---

### R3 判定: **PASS（欠陥19件を修正のうえ）**

**出荷可能。** 台本 4,738語（帯 4,600–4,750・残余 12語）、ラダー／grep／密度は全項目基準内、15の load-bearing 主張は全て一次資料に着地（うち7件は R3 が独立に取り直し、3件は R1 の誤りを是正）、センシティビティは**プロンプト行の実データ掃引**で child 0 / medical 0 / likeness 0 / ban-regex 0、CODEX_A のチェックサムと S 番号は無傷、アーカイブ検索は 5/5 が記載どおり。

**次工程が最初にやるべきこと:** ① CODEX_A の差し替え14行を発注前に確認（§R3-9 の regen list）。② TTS 実測後に DESIGN §5.3 の**訂正済み**手順で再ロック（閾値は **1,721s** であって 1,791s ではない）。③ CODEX_B に **R-TVMEDIUM** と「Partain のビートと ATSDR causation リストを同一カードに置かない」と「委員会名を出さない」を申し送る。④ 公開週に §RE-CHECK（10月30日・DOJ 総額・件数・Track 1 期日・2026-08-17 の status conference・両名の存命）。

---

## 現時点のゲート出力（★R3 実施後・2026-07-29 再実行）

```
$ ./.venv/Scripts/python.exe scripts/check_script_length.py --lo 1740 --hi 1860 episodes/_planning/EP58_lejeune_script.en.v001.md
PASS script_length: 4,738 words (need 3,973-5,309)
  narration estimate  slow 28.9m | median 26.6m | fast 20.0m
  target band         29.0-31.0 min
  ! RISK: at the fast end of the measured pace (237.4 wpm, seen on williams/florence) this lands at 20.0 min -- under the floor. Either pin the voice speed or write to 6,885 words.
```
> **RISK 行への処置（R1/R2 と同一・R3 も維持）:** 237.4 wpm は williams/florence の別ボイス設定由来で本作には適用されない。Brian 正典設定（`nPczCjzI2devNBz1zQrb`・stability≈0.35 / similarity≈0.80）の実績帯は **170.4–178.1 wpm**（EP55 170.4 / EP56 175.1）。**TTS 実測後に DESIGN §5.3 の★訂正済み手順で `durationInFrames` を再ロックする。gap 床の引き金は 1,721 s（≒164.9 wpm）であって 1,791 s ではない。**

```
$ ./.venv/Scripts/python.exe scripts/check_planning_package.py 58 lejeune --require-r3
ok   F1 script_length gate PASS (1740-1860s)
ok   F2 narration body is CJK-free
ok   F3 hook->OP->acts structure markers present
ok   F5 'dochighlight' absent or explicitly banned
ok   F6 'DATE_STAMP' absent or explicitly banned
ok   F7 DESIGN carries figure-beat density budget
ok   F8 CODEX_A carries 1-scene-1-image / no-variants rule
ok   F9 CODEX_A carries the real-person likeness ban
ok   F10 review log has R1+R2
ok   F10 review log has substantive R3
ok   thumb: CODEX_A includes emotive-face thumbnail stills
info word-ish count (latin tokens): 7620

RESULT: PASS (0 warn)
```
> `--require-r3` **PASS**。★このゲートは R3 実施中に一度 **FAIL** した — R3 節を書いた後も、**文書タイトル行と Reviewer 行に「R3 プレースホルダ」「未実施」が残っていた**ため、`re.search` が最初の `R3` 見出し（＝タイトル行）を掴み、本文に「プレースホルダ」が含まれると判定した。**ゲートは正しく、こちらが古い文言を消し忘れていた。**両行を実施済みに書き換えて PASS。

```
$ ./.venv/Scripts/python.exe scripts/check_prompt_diversity.py episodes/_planning/EP58_lejeune_CODEX_A_ASSETS.v001.md
ok   prompt coverage 100% (267/268 referenced asset ids)
info prompts extracted: 267 | boilerplate tokens dropped: 11 (df>30%)
ok   no same-series pair reaches Jaccard 0.5
WARN 4 cross-series twin(s) (still/motion pairs are often intentional — eyeball them):
  0.54  M42 ~ S210   shared: absolutely, anywhere, band, early, flat, frame, grey, horizon
  0.53  M23 ~ S112   shared: beyond, blank, cold, desk, folder, folders, form, macro
  0.52  M33 ~ S167   shared: band, document, extreme, hand, heavy, line, macro, pale
  0.50  M13 ~ S064   shared: adult's, curled, desk, framed, hands, keys, lamp, platen

RESULT: PASS (0 dup-pairs, 0 generic)
```
> 267 = 全 asset 点数（S210 + M42 + T3 + F12）。coverage の分母が 266→268 に増えたのは、R3 が **F136 の `covers_scene_id` を null → S133** に振り替えた（テレビを ACT4 の Partain に移設）ためで、**参照される全 asset id にリテラルプロンプトがある**状態は維持されている。
> 4件の cross-series twin は全て意図した still↔i2v poised ペア（同ビートの静止版と「動く直前」版）＝設計どおり。**R3 が書き換えた 14 行はいずれも新しい twin を作っていない**（再実行して確認済み）。

**3ゲートの exit code: 0 / 0 / 0（すべて 0 = PASS）**

## 申し送り（次工程）

1. **R3 独立レビュー = 完了（2026-07-29）**。`--require-r3` を含む全ゲート PASS。**未実施のレビューは残っていない。**
2. **★最優先：CODEX_A の差し替え 14 行を発注前に確認**（§R3-9 の regen list）。**旧版のテレビ素材を生成してはならない**（R-TVMEDIUM）。
3. ElevenLabs マスター生成（Brian 正典設定）→ **ffprobe で speech と gap を別々に実測** → `durationInFrames` 再ロック。**DESIGN §5.3 の★訂正済み手順を使う — gap 床の引き金は 1,721 s（≒165.2 wpm）であって 1,791 s ではない。** EP55 +71.2s / EP56 +71.8s の実績があるので FAIL_STOP は想定内。**178.1 から何も再導出しない。**
4. CODEX_A で素材を発注: still 210（★HP 85 = 40.5%）+ i2v 種 42 + thumb_face 3 + F-series 12 + **archive/factory 235**（`search_archive.py` ＋ラベル付きコンタクトシート必須。**R3 が 5 クエリを再実行して棚ラベル破損を実確認済み**）+ overlay 30。**在庫は 113,460 点の単一インデックス**（R3 実測）。
5. **CODEX_B 執筆時の R3 由来の拘束事項:**
   - DESIGN §3 の 17 カード表を B 契約表へ（**card 8 = 4枚シーケンス 5.5s / card 12 = 委員会名なし / デッキ合計 82.5s**）。
   - `check_lejeune_facts.py` に **R-TVMEDIUM** を実装（act 4/5 以外のテレビ語 = FAIL）。
   - **✗ Partain のビートと ATSDR causation リストを同一カードに置かない**（隣接による誤読防止・CL-26c）。
   - **✗ 2010年公聴会の委員会名をどのカード・概要欄・字幕にも出さない**（二説対立・未決着）。
   - **✗ 濃度の倍率（43倍/280倍）を ATSDR に帰属しない**（ATSDR の文字列ではない・CL-04）。
   - **✗ §VERIFIED-VERBATIM #19（Murtha）は隔離中 — 画面使用禁止。**
   - held-beat に slow-read cue・sting ≤ 5.0s 実測ゲート・**"CHCL2BR" の読み上げ回避**・Lejeune の発音試聴（**ル・ジューン** /ləˈdʒuːn/）。
6. **公開週に台帳 §RE-CHECK を必ず実行**（10月30日の期限・DOJ の支払総額（R3 時点で offers >$968M / payouts >$801M・2026-07-17）・請求/訴訟件数・Track 1 の裁判期日（R3 時点でゼロ・**2026-08-17 に status conference**）・両名の存命）。**ENDING の最後60秒は再カット可能に書いてある。**
7. **次話への機構提案（R3-10）:** craft-checklist に **A0（開幕の位置を*発話トークン*で測る）** と **H1（台帳の各訂正が CODEX_A の実プロンプト行に到達しているか grep）** の2項目を追加すること。今回の2大欠陥はどちらも既存の26項目では捕まらなかった。
