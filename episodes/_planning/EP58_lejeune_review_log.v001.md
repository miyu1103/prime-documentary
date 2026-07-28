# EP58 `review_log.v001` — 台本レビュー記録（R1 FACT AUDIT + R2 CRAFT/RETENTION AUDIT + R3 プレースホルダ）

**Subject:** `EP58_lejeune_script.en.v001.md`（narration 実測 **4,737語** · オーナー帯 4,600–4,750 内）+ `EP58_lejeune_FACTS_LEDGER.v001.md`（CL-01〜CL-46）
**Reviewer:** Claude（左工程）R1/R2。**R3 = 独立非執筆エージェント — 未実施（下記 R3 節はプレースホルダ）**
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

## R3 — INDEPENDENT REVIEW（別エージェント・fresh eyes・FIX AUTHORITY） — **PLACEHOLDER · 未実施**

**この節はプレースホルダである。** R3 はまだ走っていない。実施時に本節を上書きし、`check_planning_package.py 58 lejeune --require-r3` を通すこと。

R3 に必ずやらせること（本パスが自分で見つけられない種類の欠陥を狙う）:
1. **全メトリクスの独立再計算**（語数・ladder 各%・emotion grep・specificity 最長ギャップ・punch share）。R2 の申告値を信用しない。
2. **本パスが訂正した5件の再検証**（特に ① 曝露総数が本当に ATSDR に存在しないか、② Ensminger のテレビ場面が本当に一次記録に無いか、③ Hargett/Babson、④ 250ガロン、⑤ Janey の出生地）。**訂正が過剰訂正でないかも見る。**
3. **本パスが取得できなかった一次資料の追撃**: ABC One-Hour Cleaners の営業年と EPA Superfund プロファイル／ATSDR *Chapter A Supplement 1* の井戸別停止日／NRC 2009 の委員会自身の結論文／GAO-07-933。
4. **ベンゼン・塩化ビニル濃度の二重帳簿（R1-2 §12）の決着** — ATSDR の2製品が食い違う理由を特定し、台本の「濃度を出さない」判断が妥当か再判定。
5. **因果ファイアウォールの敵対的読み** — ACT III の "what it does and does not prove" 段落と ACT IV のクラスタ段落を、**原告側にも被告側にも寄りすぎていないか**両方向から読む。
6. **CL-43 の10月30日命令**をドケットから再取得し、**R3 実施日時点で有効か**を確認（本作は present-tense がすべて）。
7. **5文書クロス整合の機械検査**（script ↔ ledger ↔ DESIGN ↔ CODEX_A の語数・秒数・カード枚数・素材点数・also_thumb 集合）。
8. **CODEX_A の全267プロンプトへの ban-regex 掃引**（BANNED_PORTRAIT / BANNED_ACCURACY）と、★HP 85行の変化マトリクス自己監査。

---

## 現時点のゲート出力（2026-07-29 実行）

```
$ ./.venv/Scripts/python.exe scripts/check_script_length.py --lo 1740 --hi 1860 episodes/_planning/EP58_lejeune_script.en.v001.md
PASS script_length: 4,737 words (need 3,973-5,309)
  narration estimate  slow 28.9m | median 26.6m | fast 20.0m
  target band         29.0-31.0 min
  ! RISK: at the fast end of the measured pace (237.4 wpm, seen on williams/florence) this lands at 20.0 min -- under the floor.
  （処置は R2-1 と同一: Brian 正典設定の実績帯 170-178 wpm・TTS 実測後に durationInFrames 再ロック）

$ ./.venv/Scripts/python.exe scripts/check_planning_package.py 58 lejeune
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
info word-ish count (latin tokens): 6725

RESULT: PASS (0 warn)

$ ./.venv/Scripts/python.exe scripts/check_prompt_diversity.py episodes/_planning/EP58_lejeune_CODEX_A_ASSETS.v001.md
ok   prompt coverage 100% (267/266 referenced asset ids)
info prompts extracted: 267 | boilerplate tokens dropped: 11 (df>30%)
ok   no same-series pair reaches Jaccard 0.5
WARN 4 cross-series twin(s) (still/motion pairs are often intentional — eyeball them):
  0.54  M42 ~ S210   shared: absolutely, anywhere, band, early, flat, frame, grey, horizon
  0.53  M23 ~ S112   shared: beyond, blank, cold, desk, folder, folders, form, macro
  0.52  M33 ~ S167   shared: band, document, extreme, hand, heavy, line, macro, pale
  0.50  M13 ~ S064   shared: adult's, curled, desk, framed, hands, keys, lamp, platen

RESULT: PASS (0 dup-pairs, 0 generic)
  ← 267 = full asset count（S210 + M42 + T3 + F12）。coverage 100% は「参照される全 asset id に literal プロンプトがある」ことの機械確認。
    4件の cross-series twin は全て意図した still↔i2v poised ペア（同ビートの静止版と「動く直前」版）＝設計どおり。
```

## 申し送り（次工程）
1. **R3 独立レビュー（未実施）** — 上の8項目。完了後 `--require-r3` を通す。
2. ElevenLabs マスター生成（Brian 正典設定）→ **ffprobe で speech と gap を別々に実測** → `durationInFrames` 再ロック（**DESIGN §5.3 の手順・~175 wpm を想定し、178.1 から何も再導出しない**）。EP55 +71.2s / EP56 +71.8s の実績があるので **FAIL_STOP は想定内**。
3. CODEX_A（`EP58_lejeune_CODEX_A_ASSETS.v001.md`）で素材を発注: still 210（★HP 85 = 40.5%）+ i2v 種 42 + thumb_face 3 + F-series 12 + **archive/factory 235（`search_archive.py` ＋ ラベル付きコンタクトシート必須・棚ラベルは約40%が壊れている）** + overlay 30。
4. CODEX_B 執筆時: DESIGN §3 の 17カード表を B 契約表へ・`check_lejeune_facts.py` を `check_postoffice_facts.py` から clone（R-CAUSATION / R-CHILD-HARM / R-LIVING / R-JANEY / R-NOBODY-CHARGED / R-LIABILITY / R-NUM / R-INSIGNIA / R-READABLE / R-DOCHL / R-DATESTAMP / R-QUOTE / R-ADadjacent）・held-beat 5本に slow-read cue・sting ≤5.0s 実測ゲート・**"CHCL2BR" の読み上げ回避**・Lejeune の発音試聴。
5. **公開週に台帳 §RE-CHECK を必ず実行**（10月30日の期限・DOJ の支払総額・請求/訴訟件数・Track 1 の裁判期日・両名の存命）。**ENDING の最後60秒は再カット可能に書いてある。**
