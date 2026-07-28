# EP57 `review_log.v001` — 台本レビュー記録（R1 FACT AUDIT + R2 CRAFT/RETENTION AUDIT）

**Subject:** `EP57_fieldtest_script.en.v001.md`（narration 実測 **4,750語** · オーナー帯 4,600–4,750 の上端ちょうど）+ `EP57_fieldtest_FACTS_LEDGER.v001.md`（FT-01〜FT-67）
**Reviewer:** Claude（左工程）R1/R2。**R3 = 独立非執筆エージェント（未実施 — 本ログ末尾のプレースホルダ参照）**
**根拠:** `PD_ONE_PASS_PRODUCTION_SPEC.v2.md` rows 15/16、`DEEP_RESEARCH_FINDINGS.v001.md`（MUST群）、`TOPIC_PIPELINE.v004.md` §2/§6（EP57 固有の feed-forward）、`EP57_fieldtest_DESIGN_ARCHITECTURE.v001.md` §6、FACTS_LEDGER ガードレール、`pd-craft-checklist`（26項目）。
**制約の告白（先に書く）:** 本セッションは着手時点で **WebSearch 予算が 200/200 で枯渇**していた。検証はすべて **WebFetch（URL既知）** で行った。到達できなかった一次記録が3件あり、**そのどれからも台本は1文字も引いていない**（§R1-3）。

---

## R1 — FACT AUDIT（台本の全 load-bearing 主張 × 台帳の行単位照合）

台本末尾の `Fact map (claim → ledger)` で **COLD OPEN → ENDING の全ビートを FT 行に1対1で対応**させてある。以下は、検証の過程で **発注ブリーフ／通説と食い違い、台帳と台本の側を一次記録に合わせて直した項目**である。

1. **★最重要の訂正 — 「食べ物だった」は書けない（FT-34）。** ブリーフは *"read 0.0134 g of food debris as crack cocaine"* と書き、サムネ文言に `IT WAS FOOD` を指定していた。**一次記事の実文は** *"The crumb's fragmentation pattern did not match that of cocaine, or any other compound in the lab's extensive database. It was not a drug. It did not contain anything mixed with drugs. **It was a crumb — food debris, perhaps.**"* — **"perhaps" 付きの推測**である。台帳 FT-34 を **permitted-wording 行**に格上げし、台本は「薬物ではなかった」「規制物質は検出されず」「どの化合物とも一致しなかった」だけを断定し、"food debris, perhaps" は **「ファイルを読んだ記者たちはこう書いた」と帰属して**一度だけ使う。**サムネ文言は `IT WASN'T A DRUG` を推奨（FT-66・オーナー判断事項）。** これは事実精度と CTR 文言の両方に効く、本パス最大の発見。
2. **「20時間後に有罪答弁」は記録上の数字ではない（FT-16）。** ブリーフと `TOPIC_PIPELINE` §2 は "Twenty hours later she pleads guilty" と書く。一次記事にあるのは **「午後遅くに逮捕」「9時間後の午前3時37分に収監」「その朝に罪状認否」** だけ。20時間は**こちらの算術**なので、台本は **"before the next morning was over"** に置換した。数字として言わない。
3. **到達できなかった3件を「引かない」で処理した（FT-67）。** `exonerationregistry.org/cases/12059`（403）・Justia の *Ex parte Albritton*, WR-85,184-01（403）・Houston Chronicle（ホスト拒否）。**台本は「彼女の有罪判決はやがて取り消された」以上のことを言わない — 日付なし・裁判所名なし・手続きなし。** 台帳には「どこに実物があるか」だけ記録した。
4. **テキサスは禁止していない（FT-54）。** 2016年12月の Timothy Cole 委員会は研究所確認の**義務化を勧告**したが、翌年の **HB 34 は §8 で「調査」を命じただけ**（enrolled text を capitol.texas.gov から直接取得して確認。施行 2017-09-01、報告期限 2018-12-01）。台本は「A study. Not a requirement.」と明示する。**「テキサスが規制した」と書けば一次法文と矛盾する。**
5. **ヒューストンが止めた理由は精度ではない（FT-55）。** 2017年7月の使用停止は事実だが、**公表された根拠はフェンタニル被曝からの警官保護**であり、Acevedo は officers would rely on their own "expertise" と述べている。台本は両方を同じ段落に置き、**「警察にとって危険になったから止まった。他の全員にとって危険だったからではない」**と着地する。ここを「是正の勝利」に書き替えると事実が壊れる。
6. **119 は現在値ではない（FT-44 / FT-56）。** 119件・残り172件は **2016年夏時点**。2020年の続報が **「ヒューストンだけで250件超」** としているので、台本は 119 に "by the summer of 2016" を必ず付け、Act V で 250 超に更新する。
7. **年齢は書けない（FT-02）。** 同一記事から2回の抽出で **41歳** と **43歳** の両方が返った。**台本は年齢に触れない。** 台帳に矛盾そのものを記録し、後工程が「訂正」してしまうのを防ぐ。
8. **警官は名前を出さない・人物として描かない。** 一次記事は2名の氏名と "You're busted" の発話を記録しているが、**いずれの警官にも何らの認定も下されていない**。台本は発話だけを一度、**無名の「その警官」**として使い、形容詞も動機も付けない。§1.2 R-OFFICER として CODEX_A の機械ゲートにも実装した。
9. **署名済みでない superlative を全部落とした。** 初稿にあった「全米第3位の警察組織」「全米第5位の警察組織」は**どの FT 行にも無い**。台本は「アメリカでも有数の規模の警察組織」「その本部長」に置換（Fact map に明記）。
10. **コロラドは施行日を書かない（FT-62）。** 3ソース（Complete Colorado / GPS 立法ブリーフ / RDTIA）が法案番号・票数（65-0 / 33-0）・署名日（2026-03-26）・条項で一致する一方、**施行日はどのソースにも無い**。台本は書かない。`status_as_of` 2026-07-29、公開前再確認。
11. **引用を1件、使わずに「所在」だけ記録した。** コロラド報道中の *"Tricia Rojo Bushnell, Quattrone Center executive director"* に帰属する一文は、**当センターの役職記録と一致しない**うえセンター発行物に当たれなかった。**どの形でも使わない**とし、台帳に「どこにあるか」だけ書いた。
12. **DUI の扱い（FT-12）。** 2008年ルイジアナの飲酒運転前科（呼気0.0で有罪答弁）は、人格の陰影ではなく**同じ算術の小型版**としてのみ Act II に1段落入れた。使う／使わないは R1 判断で**使う**とした（機械の誤りに二度答弁した、という本作の主題そのもの）。

**逐語引用の照合（台帳 §VERIFIED-VERBATIM 20系統のみ使用・全て一致）:** McClelland「Police officers aren't chemists…」✓ / 現場の "You're busted" ✓（無名） / 検査票 "N.C.S. No controlled substance identified" ✓ / "totaled 0.0134 grams … about the same as a tiny pinch of salt" ✓ / "It was not a drug… It was a crumb — food debris, perhaps." ✓（留保付きで帰属） / "it was just a syringe" ✓ / Munier 書簡 "Dear Sir or Madam" + "you were prosecuted for a criminal drug offense and convicted in error" ✓ / Albritton「I knew it! I told them!」「No. You're not ever free and clear of it…」「with the bend over, cough」「If the law said you had crack, you had crack」✓ / Richardson「The entire country works on these field-test kits, right?」✓（台本では引用せず地の文へ吸収） / Anderson「a breakdown at every point in the system」✓ / NBS 1974 ✓ / DOJ 1978 ✓ / Scott「No field test is fail safe…」「I would. But that's just me.」✓ / Scott 社サイト "possible (though unlikely)" ✓ / Timothy Cole 委員会 ✓（冒頭のコスト節を省略、省略部は Fact map に記載） / Plourd 2018 ✓ / Brian David 2021「arbitrary and unlawful guesswork」✓ / Acevedo「a wealth of training and experience…」✓ / Safariland ✓ / Ross Miller ✓。**捏造引用ゼロ。**

**センシティビティ監査（HARD）:**
- ❌ Albritton を「実は持っていたかも」と読める記述ゼロ。**そもそも無実を「主張」していない** — 研究所の結果を報告している（R-NOT-A-DRUG）。
- ❌ 逮捕警官を犯罪者・悪役として描く記述ゼロ。名前ゼロ、動機の推測ゼロ、標章ゼロ（R-OFFICER）。ENDING は明示的に *"No court ever found that the officer did anything wrong"* と書き、**悪役は「制度」だと言い切る**。
- ❌ 薬物使用の描写ゼロ。注射針は「報告書の一行」と「ピント外の物体」のみ（R-NO-DRUG-DEPICTION）。
- **存命私人の尊厳:** 内心描写ゼロ・創作台詞ゼロ。身体検査は**本人の6語**のみで、映像は人物なしと DESIGN §1 で固定。障害のある息子は1節・医学的詳細なし・氏名なし。
- **人種（FT-43）:** 59% / 24% / 63% を**隣接して一度、形容詞なし**で置き、直後に「1グラム未満というカテゴリ全体」へ移る。演出ゼロ。
- **数値ヘッジ:** "roughly thirty thousand" / "about seven hundred and seventy-three thousand" / "more than two hundred and fifty" / "before the next morning was over" / "roughly six months later" ✓。**exact-of-record 断定**（$2・0.0134・.02・45・21・3:37・4日・58%・22日・416・251・301・212・93%・50・59%・24%・63%・119・172・99.5%・9,000・1973・1974・1978・2011-02-23・2014-07-29・2026-03-26・65-0・33-0）✓。
- **ロゴ/実在肖像/可読文書:** 台本に依存なし。CODEX_A §1.2 と DESIGN §6 でバン実装 ✓。

**R1 判定: PASS**（捏造ゼロ・全主張が FT 行にトレース・ブリーフとの差分は**すべて一次記録の側に合わせて修正済み**・到達不能な3記録からは何も引いていない）。

---

## R2 — CRAFT / RETENTION AUDIT（DEEP_RESEARCH MUST群のネイティブ検査）

### R2-1 尺・語数ゲート（実行出力・2026-07-29）

```
$ ./.venv/Scripts/python.exe scripts/check_script_length.py --lo 1740 --hi 1860 episodes/_planning/EP57_fieldtest_script.en.v001.md
PASS script_length: 4,750 words (need 3,973-5,309)
  narration estimate  slow 29.1m | median 26.7m | fast 20.0m
  target band         29.0-31.0 min
  ! RISK: at the fast end of the measured pace (237.4 wpm, seen on williams/florence) this lands at 20.0 min -- under the floor. Either pin the voice speed or write to 6,885 words.
```
- narration 本体実測（COLD OPEN→ENDING・ゲート同一 regex・ヘッダ/OST/appendix 除外）= **4,750語** → オーナー帯 4,600–4,750 の**上端ちょうど** ✓。
- RISK 行への処置: EP55/EP56 と同一 — Brian 正典設定（stability≈0.35 / similarity≈0.80）で fast 端は実績帯 167–182 wpm に入る。**さらに本作は provisional を 178.1 ではなく 172.0 wpm で立てている**（DESIGN §5）。EP55 が +71.2s、EP56 が +71.8s ドリフトした事実を先に予算へ入れた。両端検証: 178.1 wpm → 29:41、170.4 wpm → 30:53、**どちらも帯内**。

### R2-2 Opening formula v2（FINDINGS R-7..R-13 — 実測）

| 項目 | 判定 | 証拠 |
|---|---|---|
| 第1文 = 宣言文・人物+固有具体+不調和 | **PASS** | "In August 2010, in a strip-mall parking lot in Houston, Amy Albritton watched a police officer drop a crumb from her car floor into a vial of pink liquid." — 疑問文でない、"This is the story of" なし、抽象語なし |
| 人物名 ≤0:15 / 対立勢力 ≤0:28 | **PASS** | Albritton は **word 11 ≈ 0:04**；警官（試薬を持つ側）は word 17 ≈ 0:06 |
| BUT-loop がスティング前（~0:30） | **PASS** | "But the crumb was not cocaine. It wasn't a drug at all — and the state's own laboratory would prove it, six months after she had already confessed to it in open court." = words 70–117 ≈ **0:24–0:30** |
| Brand sting ≤5s・audio-continuous・loop後 | **PASS（設計値）** | 台本に §BRAND STING 指定（~0:30–0:35・gold Bookends の ≤5s cut・title line 融合）— ビルドで sting 実測 ≤5.0s を検証（DESIGN §5） |
| Post-brand = 1エスカレーション文+日付/場所アンカー | **PASS** | 43語1文（"In one American county, two hundred and twelve people were convicted the same way she was…"）→ "Houston, Texas. Late afternoon, August 2010." |
| First-45s 禁止事項 | **PASS** | subscribe/自己紹介/スポンサー なし。新具体は 3–8 秒ごと（2010年8月/ヒューストン/駐車場/ピンクの液体/青/2語/9時間/翌朝/重罪/6か月/212件/2ドル） |
| R-6 packaging⇔opening | **PASS** | サムネ画（青くなるアンプル・暗いフロアマットの白い粒・パトカーの光）＝**literal first shot**；サムネ文言 `IT WASN'T A DRUG` は **≈0:22 に発話**（"It wasn't a drug at all"） |

### R2-3 60–180s explanation-block スキャン（FINDINGS R-2 — 我々の実測クリフ帯）

60s ≈ word 171 〜 180s ≈ word 515（provisional 172 wpm 基準）= **ACT I 前半**。逐語で通読した内容:

```
apartment complex in Monroe Louisiana ... Frances Place ... run it for two years ... The job came with
an apartment ... She had two sons ... Her mother a pharmacy technician had died of colon cancer ...
She was in Houston that August with a man ... He was driving her white Chrysler Concorde ... he changed
lanes ... The lights came on behind them ... The officer's report records ... He asked the driver to step
out ... The officer leaned in ... What the search turned up was this ... a small white crumb ...
None of that is a crime ... To make any of it into a charge somebody has to say what the crumb is
```

**この帯は全編が「人が行為している描写」**（住む・働く・運転する・停められる・降りる・覗き込む・呼ぶ・拾う）。**化学の説明はこの帯に1文も存在しない** — コバルトチオシアネートも1973年も1974年の警告も**すべて ACT III（31–47%）に置き、しかも発明者と製造者という人物を通して語る**。**≥20秒の person-action-free 連続ブロック = 0** ✓。
**正直な記録:** この帯で最も「人の行為」から離れるのは *"None of that is a crime. A crumb is not a crime, a headache powder is not a crime, and a needle on its own is not a felony."* の **約 33語 ≈ 11.5秒**で、直後に *"somebody has to say what the crumb is"* で行為へ復帰する。**20秒閾値の約半分。**

### R2-4 Reveal LADDER 実測位置（FINDINGS R-14・語オフセットで機械計測）

```
   0.0%  cold-open shock（青に変わる瞬間・解決前カット）
  13.4%  dread-plant（"Keep two numbers running through this film" = macro loop の宣言）
  18.3%  REVERSAL 1 の入口（45日の提示）
  30.9%  ACT III 開始（物の伝記へ）
  47.4%  ★MID REVEAL 開始: 2011-02-23 の研究所（GC–MS）
  51.7%  MID REVEAL 芯: "And she wrote the weight" → 0.0134g / a tiny pinch of salt（macro loop 決済）
  62.9%  REVERSAL 2: "the institution that convicted them is the institution that found them"
  67.3%  取り立てられなかった封筒（Act IV の gut-punch）
  68.7%  ★PRIMARY REVEAL 開始: 元本部長へのインタビュー
  69.6%  money quote「Police officers aren't chemists…」
  71.4%  ★cold-open CALLBACK（年9,000個のうちの1個が、2010年8月に路肩で開けられ、自分の車に座る女性の前に掲げられた）— **70–90% 帯 ✓**
  89.3%  ★最後の新事実: コロラド HB 26-1020（2026-03-26・65-0 / 33-0）
  91.2%  resolution: "Colorado is the first state… One state, out of fifty."
  92.3%〜 ENDING: 既出事実のみの present-tense 精算（新 core fact ゼロ）
```
mid 45–60% ✓ / primary 65–85% 開始 ✓ / **92% までに新事実終了（89.3%）** ✓ / callback 70–90%（71.4%）✓ / 最終 7.7% は falling action ✓。
**★設計上の意図的な移動を記録する:** 初稿ではコロラド法と Amy の resolution が ENDING（92%以降）にあり、**新事実が 96% に落ちていた**。R2 でこれを検出し、**コロラドを ACT V 末尾へ、「有罪判決はやがて取り消された」を ACT IV 末尾（68%）へ**移した。ENDING は既出材料の再集計のみになった。

### R2-5 Re-hook cadence（FINDINGS R-15: 30分帯 max ≤150s）

90本の narrative turn の word-offset を機械計測（主要行）:

```
  4189  +134w ( 46.7s)  The study's lead author…                 ← 最長
  4508  +119w ( 41.5s)  Go back to the object one last time
   868  +110w ( 38.4s)  Plead guilty, and the sentence would be…
   989  +100w ( 34.9s)  There is a phrase for what happened next
  1940   +96w ( 33.5s)  The courtroom where a field test would be thrown out
   570   +94w ( 32.8s)  He waved the vial in front of her face
  3195   +93w ( 32.4s)  She was not there.
  4332   +88w ( 30.7s)  Colorado is the first state…
（他82本はすべて ≤30s）
mean 52w = 18.3s ／ max 134w = 46.7s
```
**150s 超の平坦区間 = 0** ✓（最長でも上限の 31%）。act 単位で 21% 超のリバーサル無し区間なし ✓（ACT IV 21.3% と ACT V 23.6% はいずれも内部にリバーサルを持つ）。
**R-3（最初の2分は ≤45s ごとに新情報）:** 0–120s 帯の最大ギャップは **32.8s** ✓。

### R2-6 EMOTION-COMMAND grep（FINDINGS R-19 — 勝者は0）

```
$ python - (regex: Sit with|Think about the|feel the (full )?weight|Now sit inside|Let that sink|aim it at|Hold that|Remember this)
emotion-command hits: 0 []
AI-smell hits: 0   (in today's world|delve|tapestry|testament to|it is important to note|
                    navigate the complexities|shed light on|at the end of the day)
```
**= 0 ✓**（EP52=9・EP53=14 からの是正を維持）。非 bookkeeping の narrator imperative は正確に **2本**（"Now do the arithmetic she had to do" / "Go back to the object one last time"）= 上限2 ✓。bookkeeping 系（"Keep two numbers running through this film"）= **1本**（≤6）✓。

### R2-7 voice/rhythm 実測

```
sentences=344  short(<=8w)=118  punch-share=34.3%      ✓ 20–35%
you/your = 3.2 /1000w                                   ✓ ≤8
rhetorical questions = 0.0 /1000w                       ✓ ≤2
question marks in narration = 0
CJK in narration body = False                           ✓（F2 ゲート）
```
> ★ punch-share 34.3% は帯の上端。TTS 後に息継ぎ字幕が細かくなりすぎないか、`check_caption_breaks` で再確認する（申し送り3）。

### R2-8 specificity（FINDINGS R-21）

```
hard specifics ≈ 415 over 27.6 min = 15.0 /min          ✓ ≥5/min
longest stretch without number/date/proper noun
   = 63 words = 22.0 s (ends ~26.8%)                     ✓ ≪90s
```
主要 reveal 文はすべて日付か数字を持つ（0.0134g / 2011-02-23 / 416 / 212 / 119 / 2016-03 / 2017-09-01 / 2020 / 2024 / 2026-03-26 / 65-0）✓。

### R2-9 craft-checklist 26項目 自己採点 = **26/26**

| # | 判定 | 証拠（1行） |
|---|---|---|
| A1 concrete cold open | ✓ | 人物+場所+2010年8月+ピンク→青（thesis なし・疑問文なし） |
| A2 ending stakes in open | ✓ | "the state's own laboratory would prove it, six months after she had already confessed"（結末の存在だけ約束・内容は伏せる） |
| A3 ≥2 loops past 25% | ✓ | 25%: 二つの重さ／報告書の中身／父の一言 ・50%: 誰も処分されたか／機械はまだ動いているか ・75%: 同左＋一州か |
| A4 macro loop ≥50% | ✓ | 「二つの重さ」= 12.0%（".02 grms"）→ 51.7%（0.0134g）→ 95%（ENDING で並置）＝ 83%pt スパン |
| A5 re-hook ≤150s | ✓ | 平均 18.3s・最長 46.7s（§R2-5） |
| A6 top reveals last third + 名前遅延 | ✓ | primary 68.7%／最後の新事実 89.3%；"the man who had run the Houston Police Department"（68.7%）→ McClelland 命名（69.0%）は短いが、**発明者は "The man who invented the test Houston was using has a name."（43.6%）→ L. J. Scott（43.8%）で意図的に1文遅延** |
| A7 local resolutions | ✓ | 各ケースビートが3分内で開閉（BC Powder／注射針／三段テスト／封筒） |
| B1 villain by 25% + record detail | ✓ | 12.0%：警官が秤なしで ".02 grms" と書く＝**制度が悪役**であることを記録で示す最初の一撃 |
| B2 adjectives ≤2文 from record | ✓ | 評言はすべて verbatim か算術に隣接（"A study. Not a requirement." は HB34 §8 の直後） |
| B3 verbatim per act | ✓ | I: "You're busted" / II: 4日・22日・58%（記録数値） / III: NBS 1974 + DOJ 1978 + Scott / IV: N.C.S.・0.0134・"convicted in error" / V: McClelland + Timothy Cole + Acevedo + Safariland + Miller |
| B4 villain status beat | ✓ | ACT III「科学の見た目を帯びていた」＝キットの権威づけ／ACT V「警察に危険だから止めた」＝制度の自己保存 |
| C1 unrepeatable details | ✓ | Albritton=**仕事に付いてきたアパート**と路上に出された家具／警官=**秤の無い手書きの .02**／Barker=**「ひとつまみの塩」**／Scott=**捨てた三段テスト**／Munier=**"Dear Sir or Madam"** |
| C2 planted object pays ≥2min | ✓ | vial（0:10 で登場 → 71.4% で「年9,000個のうちの1個」として callback → ENDING で未開封のまま座席に） |
| C3 victim violence ≤1 clause | ✓ | 身体検査は**本人の6語のみ**。暴力描写ゼロ・薬物使用ゼロ |
| D1 emotion commands | ✓ | 0（grep 出力 §R2-6） |
| D2 ≥3 registers/act + warm 1st half | ✓ | warm（Frances Place の朝・鍵・階段）・dry-wit（"It was just a syringe." / "Everybody in that building does."）・procedural（研究所）・grave（封筒）・flat-anger（"A study. Not a requirement."） |
| D3 false-relief → reversal | ✓ | 21日で出所＝偽の解放 → 半年後に報告書／2015年の地検改革＝希望 → 2017年テキサスは「調査」だけ |
| D4 held-beat per act | ✓ | "It turned blue."／"The innocent plead five times faster than the guilty."／"In Amy Albritton's case, somebody eventually did."／"It was six months late, and it was addressed to nobody."／"He did not defend them."（slow-read 指定は CODEX_B の cue へ） |
| E1 punch share 20–35% | ✓ | 34.3%（§R2-7） |
| E2 you ≤8/1000 | ✓ | 3.2/1000 |
| E3 rhetorical Q ≤2/1000 | ✓ | 0.0/1000（疑問符ゼロ。"Which raises the only question that matters." は平叙で受ける） |
| E4 AI-smell 0 | ✓ | grep 0（§R2-6） |
| E5 anaphora run | ✓ | "A crumb is not a crime, a headache powder is not a crime, and a needle on its own is not a felony." ／ ENDING の "It does not give back…" 連続 |
| F1 ≥5 specifics/min | ✓ | 15.0/min（§R2-8） |
| F2 no >90s gap | ✓ | 最長 22.0s |
| F3 reveal sentences dated | ✓ | 全件（§R2-8） |
| G1 honest ending | ✓ | "Nobody was disciplined. Nobody lost a job over it except her."／"One state, out of fifty."（慰めゼロ・現在時制） |
| G2 flat aftermath → planted button | ✓ | 二つの重さの再集計 → 未開封のポーチ → "room for a whole life to fall through"（すべて既出素材） |
| G3 CTA 1文・末尾 | ✓ | "If you think nobody should be a felon before the evidence has been tested, hit like…" |

（**26/26**。EP52=20・EP53=21 → D節・F節の系統的欠陥は EP56 に続き本話でもネイティブ解消。）

### R2-10 known-outcome dread（R-18）— **適用外**

`TOPIC_PIPELINE.v004` §6 の EP57 固有指示どおり、**R-18 は適用しない**。結末は有名でなく、行き先を先に告げると mid reveal（研究所）が死ぬ。代わりに **dread-plant（13.4%「二つの数字を数え続けろ」）だけを置き、内容は伏せる**（tease existence, withhold content）。

### R2-11 息継ぎ字幕適性・レジスター

- 数字はすべて**綴りで**書いた（"zero point zero one three four grams" / "forty-five days" / "ninety-nine and a half per cent"）— TTS の読み崩れと字幕分割の両方を避けるため。**digits は 【OST】 とヘッダにしか無い。**
- 三語の研究所所見（no controlled substance）は**キュー跨ぎ禁止**として DESIGN §5 に明記済み。
- 固有名詞の発音注意（narration 工程へ申し送り）: **Albritton**（AL-brih-tuhn）· **Ahtavea Barker** · **Velasquez** · **Acevedo** · **Multnomah** · **Quattrone** · **cobalt thiocyanate**（KOH-bawlt thy-oh-SY-uh-nayt）· **Concorde**。

**R2 判定: PASS**（26/26・emotion-command 0・60–180s ブロック 0・ladder 全マーク帯内・re-hook 最長 46.7s・specificity 15.0/min）。

---

## R3 — INDEPENDENT REVIEW（別エージェント・fresh eyes・FIX AUTHORITY）

**★ PLACEHOLDER — 未実施。** 本パッケージの執筆に一切関与していない独立エージェントが、以下を**自分で再計算・再検証**すること。R1/R2 の申告値を信用しない。

1. **全メトリクスの独立再計算** — 語数・幕別比率・ladder 位置・re-hook cadence・punch share・specificity を自前スクリプトで出し、**§R2 の申告値との差分を明示的に印字する**（EP56 の「±2%pt 内で一致 — 詐称なし」に相当する行を必ず残す。**一致した／しなかったの両方を書く**）。
2. **敵対的ファクト検証** — 少なくとも以下を一次資料で直接照合: ①0.0134g と "tiny pinch of salt" の実文 ②"food debris, perhaps" の留保が本当に原文にあるか ③416/251/301/212/93%/50/59%/24%/63% の各数値 ④119 と 172 の日付スコープ ⑤HB 34 §8 の条文（義務化でないこと） ⑥2017年7月のヒューストン停止の**公表理由** ⑦コロラド HB 26-1020 の票数と署名日（**施行日が本当に不明か**） ⑧Quattrone の 773,000 / 30,000 / 90% / 46% / 15–38% / 3× ⑨McClelland 引用の文字単位一致 ⑩到達不能だった3記録（NRE 12059 / WR-85,184-01 / Houston Chronicle）に**別ルートで到達できるか**——到達できたら台帳 FT-67 を格上げすること。
3. **センシティビティ再監査** — 存命私人の尊厳／警官の無名性と無認定／薬物使用描写ゼロ／人種数値の扱い／障害のある家族の1節。**1件でも越えていれば S1 として自分で直す。**
4. **DESIGN 一級監査** — §1.5 の四層算術（563 = 252+227+84）と §3.3 の [1]–[13] を**自分で足す**。§4 の figure-beat 配分が **92 と申告されていて 82 に調整が必要**と本書自身が書いている点（DESIGN §4）を確認し、**どの2本を落とすかを決めて CODEX_B へ渡す**。
5. **CODEX_A 整合スポットチェック** — 幕別 still 枚数（15/40/38/34/46/27/10=210）と ★HP（4/16/18/8/22/13/4=85）を数え直す。`AR` 接頭辞が coverage ゲート回避のために必要だという説明が正しいか、`check_prompt_diversity.py` のソースを読んで確認する。
6. **欠陥台帳**（S1=公開ブロック級 / S2=事実精度 / S3=衛生）を作り、**発見したものは自分で修正する**。
7. **公開前 re-check** — 台帳末尾の moving-facts リスト（コロラドの現況・第二の州の有無・ハリス郡の現在の取消総数・テキサス委員会の調査の帰結）を R3 時点で消化する。

**R3 判定: 未実施。** `check_planning_package.py 57 fieldtest --require-r3` は現時点で**意図的に FAIL する**（プレースホルダのため）。R3 完了までこのパッケージは script_verified に進めない。

---

## 現時点のゲート出力（2026-07-29 実行）

```
$ ./.venv/Scripts/python.exe scripts/check_script_length.py --lo 1740 --hi 1860 episodes/_planning/EP57_fieldtest_script.en.v001.md
PASS script_length: 4,750 words (need 3,973-5,309)
  narration estimate  slow 29.1m | median 26.7m | fast 20.0m
  target band         29.0-31.0 min

$ ./.venv/Scripts/python.exe scripts/check_planning_package.py 57 fieldtest
（下の「最終ゲート出力」を参照 — 全 ok / RESULT: PASS）

$ ./.venv/Scripts/python.exe scripts/check_prompt_diversity.py episodes/_planning/EP57_fieldtest_CODEX_A_ASSETS.v001.md
ok   prompt coverage 104% (267/256 referenced asset ids)
info prompts extracted: 267 | boilerplate tokens dropped: 10 (df>30%)
ok   no same-series pair reaches Jaccard 0.5
WARN 8 cross-series twin(s) (still/motion pairs are often intentional — eyeball them):
  0.72  M35 ~ S175 / 0.70  M32 ~ S164 / 0.61  M16 ~ S076 / 0.60  M14 ~ S071
  0.54  M06 ~ S028 / 0.54  M42 ~ S208 / 0.52  M23 ~ S117 / 0.50  M05 ~ S032

RESULT: PASS (0 dup-pairs, 0 generic)
  ← 267 = 全アセット数（S210 + M42 + T3 + F12）。coverage が 100% を超えるのは、
    F系12枚が side lane で本文中の他所から参照されないため（分母 256 < 分子 267）。
    8件の twin は**全て意図した still↔i2v poised ペア**（同ビートの静止版と「動く直前」版）で、
    §8.1a の設計そのもの。同系列（S~S / M~M）の重複は 0。
```

## 申し送り（次工程）

1. **R3 独立レビュー（未実施・最優先）** — 上記7項目。**特に §R3-4 の figure-beat 92→82 の調整**は CODEX_B を書く前に決着させる。
2. **サムネ文言のオーナー判断（FT-66）** — ブリーフの `IT WAS FOOD` は台帳が支持しない。`IT WASN'T A DRUG` / `0.0134 GRAMS` / `NO CONTROLLED SUBSTANCE` の3案。**R-6 のため、決めた文言が最初の20秒で発話されることを台本側で再確認すること**（現状 `IT WASN'T A DRUG` は ≈0:22 に存在）。
3. **ElevenLabs マスター生成（Brian 正典設定）→ ffprobe 実測 → `durationInFrames` 再ロック**（DESIGN §5 の手順）。**provisional は 172.0 wpm で立ててある**ので、EP55/EP56 級のドリフト（+71s）が出ても帯内に着地するはず。**再TTSで数字を合わせにいかないこと。**
4. **CODEX_A（`EP57_fieldtest_CODEX_A_ASSETS.v001.md`）で素材発注** — still 210 + i2v種 42 + thumb 3 + F系 12 = 267枚、アーカイブ 252本、overlay 30本。**★HP 85 = 40.5% を誕生時から。** アーカイブは §7.3 のクエリ表から始め、**ラベル付きコンタクトシート審査を飛ばさない**（棚の40%誤ラベル）。
5. **CODEX_B 執筆時** — DESIGN §3 の17カード表を B の契約表へ・`check_fieldtest_facts.py` を `check_burge_facts.py` から clone（R-NOT-A-DRUG / R-OFFICER / R-LIVING / R-NO-TEXAS-BAN / R-HOUSTON-REASON / R-COLORADO / R-NO-DRUG-DEPICTION / R-RACE / R-NUM / R-FACE / R-READABLE / R-LOGO / R-DOCHL / R-QUOTE / R-DATE）・held-beat 5本に slow-read cue・sting ≤5.0s 実測ゲート・**四層予算（archive ≥40% of cuts）の実測**。
6. **`footage_diversity` の名指しリスク** — 本作は法廷＋研究所の話で、棚は真鍮の天秤とガベルを大量に出す。**汎用象徴 ≤2 を必ず守る**（オーナーの積年の苦情）。
