# EP57 `review_log.v001` — 台本レビュー記録（R1 FACT AUDIT + R2 CRAFT/RETENTION AUDIT）

**Subject:** `EP57_fieldtest_script.en.v001.md`（narration 実測 **4,673語** — R1/R2 時点は 4,750語、**R3 の事実訂正8か所で −77語**。オーナー帯 4,600–4,750 の内側、余裕 +73語）+ `EP57_fieldtest_FACTS_LEDGER.v001.md`（FT-01〜FT-67）
**Reviewer:** Claude（左工程）R1/R2。**R3 = 独立非執筆エージェント（2026-07-29 実施済み・FIX AUTHORITY 行使・§R3 参照）**
> ⚠ **§R1/§R2 は v001 の R3 訂正“前”の記録である。**語数・幕別語数・ladder 位置・AE カード文言・★HP 枚数・figure beat 総数の現行値は **§R3 を正**とする。R1/R2 の数字は履歴として残してある。
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

## R3 — INDEPENDENT REVIEW（独立レビュー・非執筆エージェント・fresh eyes・FIX AUTHORITY 行使済み）

**Reviewer:** 本パッケージの執筆に一切関与していない独立エージェント。**R1/R2 の申告値は1つも信用せず、全部自分で数え直した。**
**Date:** 2026-07-29 · **Scope:** script / FACTS_LEDGER / DESIGN_ARCHITECTURE / CODEX_A_ASSETS の4本 · **Verdict: SHIP-READY（script_verified 可）— ただし公開前の BLOCKING 再検証が2件残る（§R3-8）。**
**Method:** 独立スクリプト3本（`ep57_r3_metrics.py` / `ep57_r3_codexa.py` / `ep57_r3_scan.py`）＋一次資料への独立フェッチ＋`search_archive.py` の実走。
**結果の要約:** **S1×0 · S2×6（全て修正済み）· S3×7（全て修正済み）。台本を8か所訂正して 4,750語 → 4,673語。CODEX_A の ★HP 実測 79枚（37.62%）を 85枚（40.48%）へ是正。DESIGN の figure-beat 92 vs 82 の未決欠陥を 92 で決着。**

---

### R3-1 全メトリクスの独立再計算（申告値との差分を明示する）

自前スクリプトで測定。**「一致した／しなかった」の両方を書く。**

| 指標 | R2 申告 | **R3 独立実測（v001 修正前）** | 差 | 判定 |
|---|---|---|---|---|
| narration 語数 | 4,750 | **4,750** | 0 | **完全一致・詐称なし** |
| 幕別語数 | 117/50/591/720/773/1,014/1,118/367 | **117/50/591/720/773/1,014/1,118/367** | 全項0 | **完全一致** |
| punch share | 34.3% | **34.5%**（119/345文） | +0.2pt | 一致（分文の境界差） |
| you/your per 1000w | 3.2 | **3.16**（生15回） | −0.04 | 一致 |
| 疑問符（narration 内） | 0 | **0** | 0 | 一致 |
| CJK in narration | False | **False** | — | 一致 |
| emotion-command hits | 0 | **0**（同一クラス regex を独立に走らせた） | 0 | **一致** |
| AI-smell hits | 0 | **0** | 0 | 一致 |
| dread-plant 位置 | 13.4% | **13.4%** | 0 | 完全一致 |
| MID REVEAL 開始 | 47.4% | **47.4%** | 0 | 完全一致 |
| MID REVEAL 芯 | 51.7% | **51.7%** | 0 | 完全一致 |
| money quote | 69.6% | **69.8%** | +0.2pt | 一致 |
| resolution | 91.2% | **91.2%** | 0 | 完全一致 |
| ENDING 開始 | 92.3% | **92.3%** | 0 | 完全一致 |
| re-hook 最長 | 46.7s（134w） | **46.7s（134w）** | 0 | **完全一致** |
| 最初の120秒の最大ギャップ | 32.8s | **39.8s**（cold open 段落 114w を1ターンと数えた場合） | +7.0s | **不一致だが両方 ≤45s で合格** |
| REVERSAL 2 | 62.9% | **64.4%** | +1.5pt | **不一致**（R2 は段落頭 "And notice who found this."、R3 は該当文そのもの。どちらも 60–65% 帯） |
| specificity | 15.0/min | **25.6/min**（大文字固有語も数える緩い定義）／**厳密定義でも ≥5/min** | — | 定義差。**どちらでも合格** |
| specificity 最長ギャップ | 22.0s（63w） | **13.3s（38w）** | −8.7s | 不一致だが R3 の方が短い＝より安全。**≪90s** |

**結論:** **数値の詐称はない。** 不一致3件はいずれも測定定義の差であり、R2 が自分に有利な側に丸めた形跡はない（specificity ギャップと re-hook は R2 の方が**厳しい**側の数字を書いている）。

**★R3 の台本訂正後の再実測（最終値）:**

```
語数 4,673（オーナー帯 4,600–4,750 ✓ 余裕 +73語）
幕別 114 / 50 / 582 / 667 / 774 / 1,014 / 1,105 / 367 = 4,673 ✓
sentences 340 · short(<=8w) 118 · punch-share 34.7%          ✓ 20–35%
you/your 3.21 /1000w · 疑問符 0 · CJK False                   ✓
emotion-command 0 · AI-smell 0                                ✓
ladder: dread 13.4% / ACT3 30.2% / MID 46.8% / 芯 51.2% /
        REVERSAL2 64.0% / set-aside 68.4% / money quote 69.5% /
        最後の新事実(Colorado) 89.2% / resolution 91.1% /
        ENDING 92.1% / CTA 99.3%                              ✓ 全マーク帯内
re-hook: mean 16.0s · max 42.2s（121w）· 最初の120秒 max 39.8s ✓ ≤150s / ≤45s
specificity 最長ギャップ 13.3s                                 ✓ ≪90s
```

**60–180s の explanation-block スキャン（R3 が自分で語番号を切って逐語通読）:** 172 wpm 基準で word 172–516、178.1 wpm 基準で word 178–534 の**両方**を出力して読んだ。**化学の説明は1文も無い**（コバルトチオシアネート／1973/1974/1978 は全て ACT III＝30.2% 以降）。帯の内容は「住む・働く・運転する・停められる・降りる・覗き込む・呼ぶ・拾う」で、人が行為している描写が連続する。
**正直に記録する境界事例:** この帯で唯一の抽象ブロックは *"None of that is a crime. A crumb is not a crime, a headache powder is not a crime, and a needle on its own is not a felony. To make any of it into a charge, somebody has to say what the crumb is. In 2010, in one of the largest police departments in America, saying what a crumb was took about ninety seconds and cost two dollars."* である。**厳格読み（"somebody has to say" を行為者と認める）なら連続無行為ブロックは 30語 ≈ 10.5秒**で閾値の半分。**最も敵対的な読み（4文まとめて説明と見なす）でも 70語 ≈ 24.4秒**。R2 は 33語 ≈ 11.5秒 と申告していた。**R3 は厳格読みを採用して PASS とするが、最悪読みが 20秒閾値を超えうることを記録に残す。**（R2 の 11.5秒という数字自体は再現できた。）

**R2 の記述で1点だけ事実誤りを見つけた（S3・修正不要だが記録）:** §R2-11 は *「digits は 【OST】 とヘッダにしか無い」* と書くが、narration 本文に **`2010`×3 と `2011`×1 の計4か所**、算用数字が存在する（line 13/19/33/73）。EP56 も同様（"In 2003, in a Hampshire village shop…"）でハウス標準なので**実害なし**。ただし「無い」という申告は間違いなので訂正しておく。

---

### R3-2 敵対的ファクト検証 — 15の最重要主張（独立フェッチ／台帳を見ずに再取得）

台帳の主張を信じず、一次記録に自分で当たった。**ProPublica の URL は R1 が記録した5本のうち4本が 404 だった**ので、シリーズ索引から正しい slug を復元して取り直している（訂正済みURLは台帳末尾に転記した）。

| # | 主張 | 判定 | 根拠 |
|---|---|---|---|
| 1 | **0.0134 g**／"about the same as a tiny pinch of salt"／分析官 Ahtavea Barker／2011-02-23／GC–MS | **CONFIRMED** | 逐語一致: *"The remainder of the 'white chunk substance' … totaled 0.0134 grams, Barker wrote on the examination sheet, about the same as a tiny pinch of salt."* / *"Barker turned to gas chromatography-mass spectrometry analysis, or GC-MS, the gold standard in chemical identification…"* ⚠ NRE は検査日を **2011-02-28** と書く。2/23 は**検査票の日付**。台本は日付を「二月二十三日」と1度だけ言い、NRE を併記しないので矛盾は起きない。 |
| 2 | **45日求刑／21日服役** | **CONFIRMED** | *"Albritton served 21 days of her 45-day sentence."* |
| 3 | 答弁の内容（何に対して有罪答弁したか）・Richardson・Velasquez・上限2年・45日提示 | **CONFIRMED** | *"Richardson told Albritton that she was going to be charged with possession of a controlled substance, crack cocaine … If she pleaded guilty, she would receive a 45-day sentence in the county jail…"* **軽罪への引き下げは無い。重罪の規制物質所持そのものに答弁している。** NRE: *"Albritton pled guilty in Harris County Criminal District Court to possession of a controlled substance."* 記事は後に *"returned home as a felon"* と書く。 |
| 4 | 研究所報告は有罪確定・服役の**後**／逮捕9時間後の午前3時37分収監 | **CONFIRMED（ただし経過時間の表現は CONTRADICTED → 修正した）** | *"Albritton was booked into the Harris County jail at 3:37 a.m., nine hours after she was arrested."* / *"five months after Albritton completed her sentence …"* **⚠ NRE: 逮捕(犯罪日) 2010-08-03、有罪答弁 2010-08-05 — *"Two days later, on August 5, 2010, Albritton pled guilty"*。** 台本の **"before the next morning was over"** はこれと矛盾する。**S2 として "inside two days" へ訂正済み**（§R3-5 D-01）。あわせて "late that August afternoon" は**時刻**であって「8月下旬」ではないことを台帳に明記した（台本は元から "Late afternoon" で正しい）。 |
| 5 | Busted 自身の数字群（Harris County の計数を含む）416 / 251 / 301 / 212 / 93% / 50 / 59% vs 24% / 63% / 119 / 172 / 99.5% / 4日 / 58% / 22日 / 10万人 | **CONFIRMED（全項）** | 全て逐語で回収。例: *"301 of the 416 variants began as arrests by the Houston Police Department"* / *"212 of those 301 arrests were based on evidence that lab analysis determined was not a controlled substance"* / *"Blacks made up 59 percent of those wrongfully convicted in a city where they are 24 percent of the population"* / *"99.5 percent of drug-possession convictions are the result of a guilty plea"* / *"the median time between arrest and plea was four days … the median for defendants [with real drugs] was 22 days"* / *"at least 100,000 people nationwide plead guilty…"* **1件の齟齬もなし。** |
| 6 | **"Police officers aren't chemists…"** の帰属 | **CONFIRMED** | 記事のプルクオート帰属が **"Charles McClelland, former Houston police chief"**。続報も確認: *"McClelland said that if he had known of the false positives Houston's officers were generating, he would have ordered a halt to all field testing departmentwide."* 台本は条件法・過去形のまま。**肩書きは "former chief" が正**（記事内の "assistant chief" は当時の役職を語る別文脈）。 |
| 7 | コバルトチオシアネートの偽陽性化学（ピンク→青／**80種超**／メタドン・にきび薬・家庭用洗剤） | **CONFIRMED（逐語）** | *"a single tube of a chemical called cobalt thiocyanate, which turns blue when it is exposed to cocaine. But cobalt thiocyanate also turns blue when it is exposed to more than 80 other compounds, including methadone, certain acne medications and several common household cleaners."* 3例とも一字一致。 |
| 8 | **今どれだけ使われているか**（Quattrone 2024 の 773,000 / 30,000 ほか）＋2011年の「10管轄中9」 | **PARTIALLY CONFIRMED → 1文削除＋台帳を分割信頼度化** | Quattrone 報告ページで **773,000 · 30,000 · 「白人の約3倍」・「全米初の包括分析」・著者 Ross Miller ほか2名** を確認。**PDF が取得上限を超え／HTML が全て403のため、1.5M の分母・90%・46%・15–38% は独立確認できず。** → **"Measured error rates run from fifteen per cent to as high as thirty-eight." を台本から削除**（15%側が未確認で、38%側は400語前にマサチューセッツの実測として既出＝重複）。残り3項は帰属付きで残し、**CODEX_B がカードを切る前に PDF で確認する BLOCKING 項目**として台帳に登録。**⚠ 名指しの混同リスク:** ProPublica は別途 *2013年の連邦調査で「62%の研究所が、早期に答弁があると警察は物証を提出しないと回答」* と報じている。**46% がこの 62% の変形なら実害のある誤りになる。** 2011年の調査は **CONTRADICTED（帰属先）**: 実文は *"The 2011 national study commissioned by the Justice Department found that prosecutors in nine of the 10 jurisdictions surveyed accepted guilty pleas using unconfirmed field tests."* — **RTI International の名は記録に無い。台本を「司法省が委託した全米調査」へ訂正済み**（§R3-5 D-02）。 |
| 9 | 1973年の発明者たち／**L. J. Scott Jr. の三段→一段** | **CONFIRMED（ただし別人格として）** | *"In 1973 … a pair of California inventors patented a 'disposable comparison detector kit.'"* — **この2名は記事中で名前が出ない。** Scott は別: 1973年に DEA の化学者、1990年に独立、HPD が "his longtime top client"。三段版も逐語確認（コバルトチオシアネート→塩酸→クロロホルムで2層分離）、そして *"For some reason, when he got into the business himself, Scott abandoned the improved three-step model of test and returned to the single chemical interaction. It is unclear why."* — **台本の「記録は理由を書かない、我々も書かない」は原文どおり。** ⚠ **Scott を「カリフォルニアの2人の発明者の一方」と読ませてはならない** → 台帳のガードレールに追記済み。 |
| 10 | **Colorado HB 26-1020** の成立・票数・署名日・条項・施行日 | **CONFIRMED（票数/署名日/条項）／"first state" は UNVERIFIED** | 一次立法記録 `leg.colorado.gov/bills/hb26-1020` で確認: 成立 · **下院 2026-02-10 65 AYE / 0 NO** · **上院 2026-03-06 33 AYE / 0 NO / 2 OTHER** · **2026-03-26 Governor Signed** · 召喚状条項と誤差率告知条項を逐語で回収。**施行日はこの法案固有には記載が無い**（*"any legislation enacted without a safety clause goes into effect on August 12, 2026"* という一般規定のみ）。→ **台本の「施行日を書かない」は正しい。この一般規定を"施行日"として書き足さないよう台帳に明示的な罠として記録した。** ⚠ **「全米初」は立法記録が主張していない。R1 が根拠にした3つの二次情報源に R3 は到達できなかった。** → **公開前の BLOCKING 再検証項目に昇格**（§R3-8）。 ⚠ 上院は 2名 OTHER。**「33対0」は可、「33人全会一致の上院」は不可** — 台帳に記録。 |
| 11 | Albritton の有罪判決は取り消されたか・いつ | **PARTIALLY CONFIRMED → 台帳を M → M-H に格上げ** | Busted: *"The Texas Criminal Court of Appeals overturned Albritton's conviction in late June, but before her record can be cleared, that reversal must be finalized by the trial court in Houston."* **R1 が 403 で到達できなかった NRE に R3 は到達**: 免罪 2016年6月、CCA が破棄、**2016-07-20 に検察が起訴を取り下げ**。⚠ **`Ex parte Albritton, No. WR-85,184-01` は NRE に無く、ドケットにも到達できず＝UNVERIFIED。どこにも印刷しない**（台帳に明記）。**台本は「やがて取り消された」以上を言わないままにした**（尊厳の判断であって、疑いの表明ではない）。 |
| 12 | **★最重要 — 「食べ物だった」は言えるのか** | **CONFIRMED — 執筆者の読みは正しい。バタ書きの "it was food" は言えない。** | 逐語: *"The crumb's fragmentation pattern did not match that of cocaine, or any other compound in the lab's extensive database. **It was not a drug.** It did not contain anything mixed with drugs. **It was a crumb — food debris, perhaps.**"* **"perhaps" は原文にある。** 認定は「データベースとの非一致」であって食品の同定ではない。**台本を全文 grep した: 断定形の "it was food" / "the crumb was food" は0件。** 唯一の出現は *"It was, the reporters who read the file wrote, a crumb. Food debris, perhaps."* — **留保と帰属の両方を持っている。** サムネ文言も `IT WASN'T A DRUG`（FT-34 で断定可能な側）。**この一点で執筆者の判断を全面的に支持する。** |
| 13 | **NBS 1974** と **DOJ 1978** の警告 | **CONFIRMED（逐語・年も一致）** | *"In a 1974 study, however, the National Bureau of Standards warned that the kits 'should not be used as sole evidence for the identification of a narcotic or drug of abuse.'"* / *"By 1978, the Department of Justice had determined that field tests 'should not be used for evidential purposes.'"* |
| 14 | **Texas HB 34 は義務化か調査か**／2017年7月のヒューストン停止の**公表理由** | **CONFIRMED（調査のみ）／officer safety も CONFIRMED、ただし Acevedo の直接引用は取れず** | 法文（capitol.texas.gov 原文）: *"The Texas Forensic Science Commission shall conduct a study regarding the use of drug field test kits…"* / *"Not later than December 1, 2018 … submit … a written report…"* / *"This Act takes effect September 1, 2017."* **研究所確認の義務化条項は無い。台本の "A study. Not a requirement." は正しい。** ヒューストン停止: *"abandoning the use of the kits … because conducting the tests in the field had exposed officers to the dangers posed by potentially lethal drugs such as fentanyl."* **⚠ 同記事に Acevedo の直接引用文は見当たらず、地の文の言い換えに見える。** → **台帳 FT-55 と逐語リスト18番を M-H に格下げ**。台本は元から鉤括弧を使わず *"they have, he said, a wealth of training and experience into…"* という間接話法なので**そのまま可**。**ただしカードには絶対に載せない**と明記した。 |
| 15 | 後年の数字（2020年に250件超・Las Vegas 5件・Multnomah 5件・マサチューセッツ38%・Plourd 2018・Brian David 2021・Safariland・Sirchie） | **CONFIRMED（全項。ただし Safariland の出典が誤り）** | 2020年記事で *"more than 250 in Houston"*、Las Vegas 5件（2011–2013の有罪、うち1名は8か月服役）、Multnomah 5件を確認。2023年記事でマサチューセッツ 38%、Plourd *"does not meet a scientific admissibility standard"*、Brian David *"arbitrary and unlawful guesswork"* を確認。Sirchie の *"ALL TEST RESULTS MUST BE CONFIRMED BY AN APPROVED ANALYTICAL LABORATORY!"* は Busted に実在。**⚠ Safariland の一文は 2020-07-01 の記事ではなく "Unreliable and Unchallenged"（2016-10-28）にある。引用自体は逐語一致。台帳の出典を訂正済み。** |

**逐語引用の再照合:** 台帳の VERIFIED-VERBATIM 20系統のうち、**19系統は独立に再取得できた**。**1系統（18番 Acevedo）は再取得できず、R3 がリストから外して M-H に落とした。** 捏造引用は**ゼロ**。

---

### R3-3 センシティビティ再監査（存命私人・警官・企業・薬物描写）

- **Amy Albritton（存命私人）:** 内心描写ゼロ・創作台詞ゼロを全文で確認。身体検査は**本人の言葉のみ・1回・映像は人物なし**（DESIGN §1 で「この beat に人物を置かない」と固定、CODEX_A の S059 は「閉じた鉄扉のみ」）。障害のある息子は1節・医学的詳細なし・氏名なし・映像なし。**★R3 が1件だけ越境を見つけて削った:** *"A friend had decided it was safer to tell her employer nothing at all — she was going to be fired anyway, he reasoned…"* — **どの FT 行にも無く、しかも存命の第三者の思考を代弁している。**HARD FRAME の「invented interiority 禁止」と invariant 1 の両方に触れるので **53語まるごと削除**（§R3-5 D-03）。
- **逮捕警官:** 台本全文で氏名ゼロ。形容詞ゼロ。動機の推測ゼロ。*"You're busted"* は1回だけ、無名で、修飾なし。**ENDING の締め *"No court ever found that the officer did anything wrong."* は正確か** — 独立検証の結果、**いずれの警官についても司法・懲戒いずれの認定も記録に存在しない。**この文は「不在」を述べており、記録を超えていない。しかも直前の *"Nobody was disciplined. Nobody lost a job over it except her."* と対で置かれ、**悪役を「制度」に確定させる機能**を果たしている。**この着地は妥当であり、変更しない。**
- **製造者（企業）:** Scott Company・Sirchie・Safariland のいずれも、**自社の公表文言と裁定済み事実のみ**。「隠した」「知っていて売った」に類する断定はゼロ。★R3 が1件是正: *"In another company's kits"* は Safariland と NIK を別会社として提示していたが **Safariland は NIK ブランドの保有者**であり、企業関係の断定は記録に無い。→ **"In one manufacturer's own kits" へ訂正**（§R3-5 D-04）。
- **人種（FT-43）:** 59% / 24% / 63% が**隣接して1回、形容詞ゼロ**で置かれ、直後に「1グラム未満というカテゴリ全体」へ移る。演出・群衆・対比構図はゼロ。CODEX_A §1.2 R-RACE も同旨。**合格。**
- **薬物使用描写:** CODEX_A の 267プロンプトを機械走査。**皮膚に刺さる注射針・吸引・服用・見せ場の粉末はゼロ。** 注射針は S041（「ピント外の灰色の形。決して被写体にせず、決して皮膚の近くに置かない」）と M系に無し。血・傷・遺体・苦悶もゼロ。**S048 の "wound"（＝「傷が見えないように切る」という否定文脈）だけがゲートの誤検知源だったので "injury" へ書き換え、誤検知そのものを消した。**
- **実在肖像:** `[NEG]`/`[HNEG]`/`[TNEG]`/`[FNEG]` の4本すべてに実名10名＋likeness/mugshot/deepfake が入っている。267本の本文側に実名は0件（機械確認）。

**センシティビティ判定: PASS（越境1件を発見し、自分で削除した）。**

---

### R3-4 DESIGN 一級監査（§ごと・台本との突合）

**§0 品質バー:** 5軸すべて台本と整合。★1点訂正: 「17 AE hero cards ≈ 95 s」は**個別duration の合計が 100.5 s**（5+6+5+6.5+5.5+5+6.5+6+7+5+6.5+6+5.5+5+8+6+6）。**≈95s → 100.5s（picture 1,829s の 5.5%）へ訂正**し、§1.5 の表とも揃えた。

**§1.5 四層算術 — R3 が自分で足した:**
```
[1] 563 = 252 + 227 + 84                                  ✓ 一致
[2] 1829.0 / 563 = 3.249 s                                ✓ ≤7.0
[3] 227 / 563 = 40.32 %                                   ✓ ≤45（余裕 4.68pt）
[4] (252+84) / 563 = 59.68 %                              ✓ ≥45
[5] still 227/210=1.081 · archive 252/252=1.000 · motion 84/42=2.000  ✓
[6] 504 / 563 = 0.8952                                    ✓ ≥0.70
[7] 563 / 504 = 1.1171                                    ✓ ≤1.4
[8] 1829.0 / 30 = 60.97 → ≥61（v001 は「61.0 → ≥62」）    ✓ ★R3 が丸めを訂正
distinct = 252 + 210 + 42 = 504                           ✓
四層%: 44.76 / 40.32 / 14.92 = 100.00 %                   ✓
```
**四層予算のパーセンテージは DESIGN §1.5 に存在していたが CODEX_A §3.1 の表には無かった。→ CODEX_A 側に `% of 563` 列を追加し、両文書が同じ 44.8 / 40.3 / 14.9 を持つようにした（オーナー指示の archive ≥40% がどちらの文書だけでも検算できる）。**

**§3 AE 17枚 — 全カードが台帳の実在事実に接続しているか（1枚ずつ照合）:** ACT_TITLE ×5 は文言のみ。残る12枚のうち **11枚は FT 行に完全に接続**（.02 grms=FT-08 / 4日↔22日+58%=FT-19 / 45日+21日=FT-15,18 / 1974+1978=FT-22,23 / $2+9,000=FT-11,30 / Scott 引用=FT-28 / 0.0134+塩ひとつまみ=FT-33 / 416+251+212=FT-40,41 / 119+172=FT-44 / McClelland=FT-49 / 773,000+30,000=FT-61 / Colorado 33↔0=FT-62）。**捏造統計は1枚も無い。**
**★1枚だけ不合格を出した:** `CENTER_STACK` **"HE WROTE '.02 GRMS' / THERE WAS NO SCALE"**。**FT-08 は書式の記入内容しか支持しておらず、「秤が無かった」はどの行にも無い推論。**カードは6秒静止して読ませる場所なので推論を置くには最悪。→ **`".02 GRMS CRACK COCAINE" / WHAT THE OFFICER WROTE ON THE FORM`（FT-08 exact-of-record）へ差し替え**、台本の同趣旨の2文と OST も同時に修正した（§R3-5 D-05）。

**§4 figure-beat の未決欠陥 — R3 が決着させた（本項が本レビューの主要成果の1つ）:**
> v001 は **幕別合計 92**、**kind 合計 82**、そして *「CODEX_B は ACT II と ACT V の lowerthird を2本落として 82 に合わせよ」* と書いていた。**92 − 2 = 90 であって 82 ではない。** 指示は算術的に実行不能で、CODEX_B に解けない契約を渡すところだった。
> **92 で決着させた。理由3つ:** ①幕別の数字は **§2 の各幕記述に独立に二重記載**されている（ACT I "14 figure beats" / ACT II 16 / ACT III 12 / ACT IV 22 / ACT V 18）。外れ値は「82」と kind 表だけ。②**82 は目標ではなく下限**（`≥82`）であり、`check_motion_density` の実フロアは **2.5 beats/min**（ソースを読んで確認: `MIN_KINETIC_BEATS_PER_MIN = 2.5`）。**92 beats / 30.48 min = 3.02/min** で余裕、82 なら 2.69/min。③オーナーの常設フィードバックは *「アニメがまた少ない」*。曖昧さを下方向に解消するのは筋が悪い。
> **kind 配分を 92 に組み直した（10本の増分は動きの濃い kind にだけ振り、本文が自ら「最低価値」と呼ぶ `lowerthird` には1本も足していない）:** `lowerthird` 24 · `kinetic` **16**(+4) · `stat` **9**(+2) · `mechanism` **8**(+2) · `compbars` 6 · `numberticker` **6**(+1) · `timeline` 5 · `bar` 4 · `arrow` **4**(+1) · `highlightring` 3 · `spotlight` 3 · `acttitle` 2 · `pindropmap` 1 · `regionmap` 1 · `routemap` 0 = **92** ✓
> あわせて **「variety 15 kinds」も訂正**（`routemap` が 0 なので実使用は **14 kinds**）。**CODEX_B は何も削らなくてよい。**

**§5 measured-VO re-lock 手順:** 存在する（ffprobe でナレーション chunk 合計を測る／gap を比例再配分／`durationInFrames` 再ロック／provisional と measured の両方を記録／**再TTS 禁止**）。**手順として完全。** 172 wpm モデルの両端を R3 が自分で計算し直した:

| wpm | narration | gap | endcard | TOTAL | 判定 |
|---|---:|---:|---:|---:|---|
| 178.1（チャンネル中央値） | 1,574.3 s | 198.9 | 9 | **1,782.2 s = 29:42** | ✓ 1740–1860（ratio 1.132） |
| 172.0（本作の provisional） | 1,630.1 s | 198.9 | 9 | **1,838.0 s = 30:38** | ✓（ratio 1.128） |
| 170.4（EP55 実測） | 1,645.4 s | 198.9 | 9 | **1,853.3 s = 30:53** | ✓（ratio 1.126） |

**★R3 は台本を77語削ったが TOTAL / picture / durationInFrames を1フレームも動かしていない** — 差分は gap budget（172.0 → 198.9 s）に吸収した。**これにより §1.5 の8行の算術と 563カットの設計が全て有効なまま残る。**（許容 gap 帯も再計算: narration 1,574–1,646 s に対し gap 86.0–277.0 s。実測がどこに落ちても台本を触る必要はない。）

**§5 チャプター（非ネタバレ）:** 7本、`guilty/verdict/exonerated/innocent/cleared` いずれも不使用。**"A Pinch of Salt" は結末を匂わせるが解決しない**（塩のひとつまみが何なのかは開かない）。**合格。**

---

### R3-5 欠陥台帳と適用した修正（S1 = 公開ブロック級 / S2 = 事実精度 / S3 = 衛生）

**S1: 0件。**

| ID | 重大度 | 欠陥 | 適用した修正 |
|---|---|---|---|
| **D-01** | **S2** | 台本 COLD OPEN が *"before the next morning was over she had pleaded guilty"* と述べる。NRE は逮捕 2010-08-03 / 答弁 2010-08-05（*"Two days later"*）。**一晩で答弁した、は記録と矛盾する。** | 台本を **"inside two days"** へ。FT-16 を全面書き換えし、`"twenty hours"` `"before the next morning was over"` `"inside a day"` `"overnight"` を明示的に BAN。あわせて *"late that August afternoon"* が時刻であって「8月下旬」ではないことを罠として記録。 |
| **D-02** | **S2** | 台本が **"the research organisation RTI International"** に帰属。**公表記録は調査実施者を名指ししていない**（"a 2011 national study commissioned by the Justice Department"）。 | 台本を **「司法省が委託した全米調査」** へ。FT-20 を差し替え、**RTI を名指ししない**を BINDING 化。語数は ±0。 |
| **D-03** | **S2** | 台本 ACT II の53語 *"A friend had decided it was safer to tell her employer nothing at all … he reasoned …"* が **どの FT 行にも無く、存命の第三者の思考を代弁**（invariant 1 ＋ HARD FRAME 違反）。 | **53語を削除。** FT-46 が支持する「解雇された／家財が路上に出された」だけを残した。台帳に「復活させるなら先に逐語抽出付きの FT 行を作れ」と記録。 |
| **D-04** | **S2** | 台本 ACT III の **"In another company's kits"** が Safariland と NIK を別会社として断定。**Safariland は NIK ブランドの保有者。** | **"In one manufacturer's own kits"**（＝台帳 FT-26 が元々推奨していた文言）へ。FT-26 に「50+ と 80+ を混ぜるな／2社として書くな」を追記。 |
| **D-05** | **S2** | 台本 ACT I の *"He had not weighed it. There was no scale at the side of the road."* ＋ AE カード **"THERE WAS NO SCALE"** ＋ OST。**路肩に何が有ったか／無かったかを支持する行は台帳に存在しない。** | 台本を **"It was a figure written in ink at the side of a road, and it became the first official number in the file."** へ（−9語）。**AE カードを `".02 GRMS CRACK COCAINE" / WHAT THE OFFICER WROTE ON THE FORM` へ差し替え**、OST も同文言に。FT-08 に「路肩の設備について何も断定しない」を BINDING で追記。**対比の効果は ACT IV の実測値との並置が担うので演出上の損失は無い。** |
| **D-06** | **S2** | Quattrone の **15–38% の誤差率レンジ**が独立確認できず、しかも **38% はマサチューセッツの実測として400語前に既出**（重複）。 | **当該1文を削除**（−13語）。残る 1.5M / 90% / 46% は帰属付きで存置し、**CODEX_B がカードを切る前に PDF で確認する BLOCKING 項目**として台帳に登録（62% との混同リスクも名指しで記録）。 |
| **D-07** | **S3** | 台本が自分で数えた語数を2か所間違えている。*"she answered in six words"* → 実際は **"Oh, yes — with the bend over, cough." = 7語**。*"Her answer was four words"* → 実際は **"I knew it! I told them!" = 6語**。 | **"seven words" / "six words" へ訂正**（±0語）。台帳に「引用を導入する文の語数は毎回数え直す」を追記。（Scott の *"I would. But that's just me."* = 6語、cold open の *"you're busted"* = 2語 は元から正しい。） |
| **D-08** | **S2** | **CODEX_A の ★HP が宣言 85枚（40.5%）に対し実測 79枚（37.62%）。** オーナーの常設指示は **★HP ≥40% を誕生時から**。§3.2・§3.3 [9][11]・§5.7・DESIGN §1 の4か所が実体と食い違っていた。**210枚焼き終わってから発覚すれば GPU 5〜8時間の焼き直し。** | **object レーンの6行を ★HP レーンへ転換**（S017 / S066 / S084 / S132 / S151 / S203）。**総枚数・幕別枚数・cuts 563 は不変。** 転換先は anti-samey 変化マトリクス（距離×角度×光×setting×姿勢）で既存85枚と衝突しない軸を選定。**ブロック見出しの ★HP 数6か所も実体へ訂正。** 再実測 = **85 / 210 = 40.48%**、幕別 4/16/18/8/22/13/4 ✓。**§5.7a に REGEN LIST を新設。** |
| **D-09** | **S2** | **CODEX_A §1.3 の機械ゲート正規表現が、本書自身の 267本のプロンプトのうち 264本を落とす。** 全プロンプトが `no readable text` で終わるため `readable` に必ず当たり、`no likeness` / `unreadable as a portrait` が `likeness` `portrait` に当たる。**実装すれば全件 reject になるか、実装者がゲートを緩める（invariant 15 違反）かの二択だった。** | **「許容フレーズを先に剥がしてから禁止語を探す」`PERMITTED` + `scan()` を確定仕様として §1.3 に書き込んだ。** `Avoid:` 以降は走査対象外であることも明記。**実証済み: 修正版 = 0/267 reject、v001 版 = 264/267 reject。** 唯一残った誤検知（S048 の "wound"）はプロンプト側を "injury" に書き換えて消した。 |
| **D-10** | **S3** | **CODEX_A §5.9 のパーサ見本が実在ID `S001.png` を使っている。** `generate_sdxl_4k.py` の `read_prompts()` は重複排除しないので、本書をパーサに通すと **S001 が `<positive prompt>` という中身で二重登録**され、`shots=255` の確認が 256 になる。 | 見本IDを **`S###.png`** へ（`^-\s*`?[SMTF]\d{2,3}` にも `\b[SMTF]\d{2,3}\b` にも当たらない）。**「この見本行は `ai_prompts.v001.md` に転記しない／転記するのは267行だけ」** を明記。再実測で重複0。 |
| **D-11** | **S3** | DESIGN §0・§3・§1.5 の **AE 17枚「≈95 s」が実際は 100.5 s**（5.5pt の過小申告）。 | **100.5 s（picture の 5.5%）へ訂正**、3か所を揃えた。 |
| **D-12** | **S3** | **DESIGN §4 の figure-beat が 92（幕別）と 82（kind）で不一致、しかも本書自身が提案した「2本落とす」が算術的に成立しない。** | **92 で決着し、kind 表を 92 に組み直した**（§R3-4 参照）。「variety 15 kinds」→ 実使用 **14 kinds** も訂正。 |
| **D-13** | **S3** | `[8] archive 下限 = 1829.0/30 = 61.0 → ≥62本` の丸め（ceil(60.97) = 61）。 | **≥61 へ訂正**（DESIGN・CODEX_A の両方）。設計値252には影響なし。 |
| **D-14** | **S3** | 台帳の出典誤り2件（Safariland を 2020-07-01 記事に帰属／ProPublica の slug 5本中4本が 404）。台帳の逐語リスト18番（Acevedo）が再現できない。 | Safariland を **"Unreliable and Unchallenged"（2016-10-28）** へ訂正。**動作する slug 5本＋新規1本を台帳に転記。** 18番を逐語リストから外し **M-H に格下げ**（間接話法でのみ可・カード禁止）。**逐語リストは20系統→19系統。** |
| **D-15** | **S3** | R2 §R2-11 の *「digits は 【OST】 とヘッダにしか無い」* が事実と異なる（narration 本文に `2010`×3 / `2011`×1）。 | ハウス標準（EP56 も同様）につき台本は変更せず、**本 R3 に訂正を記録**。 |

**語数の帳尻:** −3（D-01）−9（D-05）−53（D-03）−13（D-06）+1（D-04）±0（D-02, D-07）= **−77語 → 4,673語**。**オーナー帯 4,600–4,750 の内側、しかも v001 の「上端ちょうど・余裕ゼロ」から +73語 の余裕を確保した。**（v001 は帯の天井に貼り付いていたため、**どんな訂正も加筆では入らない**状態だった。これ自体が構造的リスクだったので記録する。）

---

### R3-6 CODEX_A 整合スポットチェック（20行の無作為抽出＋全数の機械検算）

**§3.3 チェックサム [1]–[13] を R3 が自分で足した:** [1] 563 ✓ · [2] 3.249s ✓ · [3] 40.32% ✓ · [4] 59.68% ✓ · [5] 1.081/1.000/2.000 ✓ · [6] 0.8952 ✓ · [7] 1.1171 ✓ · [8] ★訂正（≥61）· [9] 40.48% ✓（**是正後**）· [10] 15+40+38+34+46+27+10 = **210** ✓ · [11] 4+16+18+8+22+13+4 = **85** ✓（**是正後**）· [12] 14+46+44+40+58+38+12 = **252** ✓ · [13] 3+8+8+6+9+6+2 = **42** ✓。

**S番号の連番性:** S001–S210 を機械列挙。**欠番0・重複0**（D-10 修正前は §5.9 の見本が S001 を重複させていた）。M01–M42 欠番0。T01–T03 ✓。F001–F012 ✓。**プロンプト総数 267 = 210+42+3+12** ✓。

**[HSTYLE] = 85 の確認:** 是正後 **85/210 = 40.48%**、幕別 ACT0 4 / ACT1 16 / ACT2 18 / ACT3 8 / ACT4 22 / ACT5 13 / ENDING 4。**レーン混用0件・`Avoid:` ブロック不整合0件**（`[HSTYLE]`→`[HNEG]`、`[STYLE]`→`[NEG]` が全行で対応）。i2v 種の `[HSTYLE]` は **18本**（M04/06/07/09・M12/14/15/17/18・M22・M27/29/30/32/33・M35/37/39）で §4.5 の H001–H018 と一致 ✓。

**無作為20行のスポットチェック（台本ビートとの接続＋禁止事項）:** S003（ポーチを裂く／COLD OPEN）· S010（助手席のシルエット／"She was not driving"）· S013（手書き記入／".02 grms"）· S023（ルイジアナの目抜き通り／Act I の世界）· S031（窓に映る像／移動）· S041（**ピント外の注射針** — R-NO-DRUG-DEPICTION 上限を守っている）· S045（ピンク→青の比較ストリップ／"the whole apparatus of proof"）· S059（**閉じた鉄扉のみ・人物なし** — 身体検査 beat の dignity 規定どおり）· S072（演台を後ろから／答弁）· S076（答弁書＝判読不能）· S094（1973年の特許図＝判読不能）· S111（チョコレートと青い試験管／偽陽性）· S112（ポーチの壁／supply shelf）· S118（**三段のうち二段が消えた作業台** — Scott の決断を動機を語らずに絵にしている）· S129（GC–MS）· S141（天秤皿の上の粒／also_thumb）· S147（伏せられた検査票／paper 状態2）· S165（**回収されない封筒** — Act IV の gut-punch）· S196（署名下の条文＝判読不能・amber）· S208（未開封のポーチ／ENDING）。
**20/20 が台本の該当ビートに正しく接続。可読文字0・実在肖像0・薬物使用0・識別可能標章0。** vial の8状態・paper の5状態・two-weights の2状態・empty seat の3状態も §5.5a の宣言どおりに実在した（状態外の余分な行は無い）。

**`AR` 接頭辞の判断が正しいか — `check_prompt_diversity.py` と `check_asset_reuse.py` のソースを読んで検証:**
- `check_prompt_diversity.py` の被参照ID抽出は `ID_REF = re.compile(r"\b([SMTF])(\d{2,3})\b")`。**`AR001` は `A` の直後に `R` が来るため `\b` が立たず、マッチしない**（実証済み: `ID_REF.findall("…/AR001_x.mp4 AR252_y.jpg") == []`）。**もし EP55 と同じ `F001…F252` 命名を使っていたら、F013–F252 の240個が「リテラルプロンプトの無い被参照ID」として分母に入り、coverage が機械的に崩れる**（実証済み: `F013`/`F252` は両方マッチする）。**執筆者の説明は正しい。**
- `check_asset_reuse.kind_of()` は `if "/factory" in p or re.search(r"\baf-bg-", p): return "factory"` を **最初に** 評価する。`fieldtest/factory/AR001_….mp4` は `/factory` を含むので **`.mp4` の motion 判定より先に factory に分類される**。**ディレクトリ名を `factory` のまま据え置くという指示が、この分類を保っている。破ってはならない。**

**アーカイブ・クエリの独立実走（棚の40%誤ラベル対策 — 5本走らせた）:**
```
$ ./.venv/Scripts/python.exe scripts/search_archive.py chemistry chemical reaction --limit 6
[  pixabay|free_commercial|medical_lab           |    0.1MB] chemical reaction science chemistry
    H:\pd-media\assets\factory\backgrounds\AF-BG-5085__laboratory_glassware.jpg
-- 1 hits total

$ ... search_archive.py courthouse corridor --limit 6
[      loc|free_commercial|courtroom_justice     |    0.2MB] Corridor. Federal Building and U.S. Courthouse, Phoenix, Ari
    E:\pd-archive\courtroom_justice\loc__2017661063__corridor-federal-building-and-u-s-courthouse-phoenix-arizona.jpg
-- 1 hits total

$ ... search_archive.py laboratory technician --limit 6
[   pexels|free_commercial|forensics_dna         |    5.8MB] a laboratory technician putting samples in a machine
    H:\pd-media\assets\factory\backgrounds\AF-BG-7109__dna_laboratory_blue.mp4
[   pexels|free_commercial|medical_lab           |    0.2MB] technician operating laboratory equipment
    H:\pd-media\assets\factory\backgrounds\AF-BG-5121__modern_medical_lab.jpg

$ ... search_archive.py parking lot --limit 6
[   pexels|free_commercial|urban_night           |   11.2MB] aerial night view of illuminated parking lot
    H:\pd-media\assets\factory\backgrounds\AF-BG-14767__police_station_at_night.mp4

$ ... search_archive.py laboratory glassware --limit 6
[   pexels|free_commercial|forensics_dna         |    0.1MB] vials with liquids in holder
    H:\pd-media\assets\factory\backgrounds\AF-BG-2000__laboratory_glassware.jpg
[   pexels|free_commercial|medical_lab           |    0.2MB] close up view of laboratory glasswares and colorful chemical
    H:\pd-media\assets\factory\backgrounds\AF-BG-2003__laboratory_glassware.jpg
```
**5本すべてで、主張されたファイル名・プロバイダ由来タイトル・ライセンス・ファイルサイズまで一致した。** とりわけ:
- **`chemistry chemical reaction` が本当に「1件だけ」** — DESIGN §1.6 query 7 と CODEX_A §7.3 の *「呈色反応そのものは実写で撮れない＝vial 連鎖を Codex に置く根拠」* は**測定結果として本物**。設計判断が趣味ではなく実測に基づいている。
- **`courthouse corridor` も本当に索引中1件**。
- **`AF-BG-14767__police_station_at_night.mp4` の実体は「照明された駐車場の空撮」**（テーマは `urban_night`）。**ファイル名は "police_station" なのに中身は駐車場** — §7.5 の「棚のラベルは信用できない」という警告が、本作が自分で選んだ代表ヒットの中で既に実証されている。**ラベル付きコンタクトシートの全点目視は形式ではなく必須。この行を落とすことは許されない。**
**アーカイブ証拠表は捏造ではない。**

---

### R3-7 craft-checklist 26項目 — R3 の独立再採点

**先に記録する構造的な指摘:** `pd-craft-checklist` の正典は **26 の二値チェック**（A hooks/loops · B villain · C victim · D emotion · E voice · F specificity · G ending）。**R2 の採点表は A1–G3 の 29行**を並べて「26/26」と書いている。**行数と申告が合っていない（S3）。** R3 は正典の26項目相当で採点し、R2 の29行についても全項を確認した。

**R3 独立採点 = 26/26（R2 と同点。ただし2項目は R2 と違う根拠で通している）。**

| 節 | R3 の判定 | R3 自身が確認した証拠 |
|---|---|---|
| **A 冒頭・ループ（7）** | 7/7 | 第1文は宣言文・人物+固有具体+不調和（疑問文ゼロ／"This is the story of" ゼロ）· Albritton は **word 11 ≈ 0:04**（172wpm 換算で 5s = 14.3語、余裕あり）· BUT-loop は sting 前 · 25%/50%/75% の各時点で**生きているループ ≥2**（二つの重さ／報告書の中身／誰も処分されたか／父の一言）· macro loop は 12.0%→51.2%→95% で**83pt スパン**（≥50% 要件の1.7倍）· re-hook 平均 16.0s・最長 42.2s · 名前遅延は発明者で意図的に1文（"The man who invented the test Houston was using has a name." → L. J. Scott）· 局所解決は3分以内（BC Powder／注射針／三段テスト／封筒） |
| **B 悪役（4）** | 4/4 | 12%地点で「秤の話をせずに」記録が悪役を指す（**R3 の D-05 修正後も成立する** — 手書きの数字と6か月後の実測の並置がそのまま告発になる）· 形容詞ではなく記録目録で damn（"A study. Not a requirement." は HB34 §8 の直後）· **幕ごとに逐語記録が1本以上**（I: "You're busted" / II: 4日・22日・58% / III: NBS 1974 + DOJ 1978 + Scott / IV: N.C.S.・0.0134・"convicted in error" / V: McClelland + Timothy Cole + Safariland + Miller）· status beat 2本（「科学の見た目」／「警察に危険だから止めた」） |
| **C 被害者（3）** | 3/3 | 各主要人物に**反復不能の具体**（Albritton = 仕事に付いてきたアパートと路上の家具／Barker = 「ひとつまみの塩」／Scott = 捨てた三段テスト／Munier = "Dear Sir or Madam"）· 植えた物体（vial）が 0:10 → 71% → ENDING で回収 · 暴力・薬物使用の描写ゼロ、身体検査は本人の言葉のみ |
| **D 感情（4）** | 4/4 | **emotion-command 0（R3 が独立に grep）**・非 bookkeeping 命令法は**正確に2本**（"Now do the arithmetic she had to do" / "Go back to the object one last time"）＝上限ちょうど・bookkeeping 1本（≤6）· 幕ごとに ≥3 レジスタ（warm / dry-wit "It was just a syringe." / procedural / grave / flat-anger）· false-relief → reversal が2組（21日で出所→半年後の報告書／2015年の改革→2017年は「調査」だけ）· held-beat 5本 |
| **E 声（5）** | 5/5 | punch share **34.7%**（20–35%）· you/your **3.21/1000w**（≤8）· 修辞疑問 **0/1000w**・疑問符0 · AI-smell **0** · anaphora 2連（"A crumb is not a crime…" / ENDING の "It does not…"） |
| **F 具体性（3）** | 3/3 | 具体密度は厳密定義でも ≥5/min を大きく超える · **最長ギャップ 13.3s**（90s 閾値の 15%）· 主要 reveal 文は全て日付か数字を持つ |
| **G 結末（3）** | 3/3 | 慰めゼロ（"Nobody was disciplined." / "One state, out of fifty."）· 既出素材のみの精算 → 植えた button（未開封のポーチ）· CTA 1文・末尾 |

**★R3 が R2 と異なる根拠で通した2項目:** **B1** は R2 が「秤なしで .02 と書く」を根拠にしていたが R3 がその根拠自体を削ったため、**手書きの数字と実測の並置**に根拠を差し替えて通した。**C1** は R2 の挙げた例のうち「路上に出された家具」が D-03 の削除段落の隣にあるが、**当該具体は FT-46 に直接支持されており削除の影響を受けない**ことを確認した。

---

### R3-8 公開前 re-check（R3 が消化した分と、残る BLOCKING）

**R3 が消化した（もはや unknown ではない）:**
- コロラド HB 26-1020 の**成立・票数・署名日・条項** → 一次立法記録で確定（§R3-2 #10）。
- **施行日が本当に不明か** → **法案固有の施行日は無い。** 一般規定（2026-08-12）は存在するが、それを施行日として書いてはならないという罠として台帳に記録。
- **Albritton の免罪の日付** → NRE に到達して確定（2016年6月 CCA 破棄／2016-07-20 起訴取り下げ）。**台本は依然として日付を言わない**（尊厳判断）。`WR-85,184-01` は **UNVERIFIED** として印刷禁止に。
- **Quattrone の 773,000 / 30,000 / 3×** → 確定。
- **HB 34 が義務化でないこと** → 法文原文で確定。
- **ヒューストン停止の公表理由** → 確定（フェンタニル被曝からの警官保護）。**Acevedo の直接引用は取れなかった**ので格下げ。

**残る BLOCKING（この2件を潰さずに公開しない）:**
1. **コロラドが「全米初」か（FT-62）。** 立法記録は primacy を主張していない。R1 の3つの二次情報源に R3 は到達できなかった。**これは ENDING の最後の30秒と締めの OST が丸ごと乗っている主張。** 独立2ソースで再確認するか、"the only state that has done it" へ帰属付きで書き換えるか、公開前に決着させる。**第二の州が出ていないかも同時に確認。**
2. **Quattrone の 1.5M / 90% / 46%（FT-61）。** PDF が開けていない。**とくに 46% は ProPublica の別記事にある「2013年連邦調査・62%」の変形である可能性がある。** CODEX_B がこの数字でカードや figure beat を作る**前**に PDF で確認する。

**その後の moving facts（従来どおり）:** ハリス郡の現在の取消総数（119 → 250+ → ?）· テキサス法科学委員会の HB-34 調査の帰結 · 製造者による製品撤回の有無 · **Albritton 本人の現況は調べない・更新しない**（私人であり、映画は公表記録の終わるところで止まる）。

---

### R3 判定

**SHIP-READY — `script_verified` へ進めてよい。**
S1 = 0。S2 = 6件、**すべて R3 が自分で修正した**。S3 = 7件、すべて修正済み（1件は記録のみ）。台本は 4,673語で帯の内側、ladder の全マークが帯内、emotion-command 0、60–180s に説明ブロック無し、craft 26/26。四層予算・§3.3 の13本の検算・AE 17枚の台帳接続・S番号の連番性・★HP 85枚（40.48%）・`AR` 接頭辞の判断・アーカイブ・クエリ5本、いずれも R3 が自分で再計算／再実行して確認した。

**次工程への申し送り（R3 発）:**
1. **CODEX_A の REGEN LIST は §5.7a の7枚だけ**（S017 / S048 / S066 / S084 / S132 / S151 / S203）。他の203枚のプロンプトは1文字も変えていない。レーンが変わる6枚は必ず `[HSTYLE]/[HNEG]` で焼くこと。
2. **CODEX_B は figure beat を 92 で書く。** 何も削らない。kind 配分は DESIGN §4 の新表（`lowerthird` 24 / `kinetic` 16 / `stat` 9 / `mechanism` 8 / …）。
3. **§1.3 の機械ゲートは必ず `PERMITTED` 剥がしを先に実装する。** 実装したら「修正版=0件 reject / v001版=264件 reject」の2通りを走らせて確認してから本番に使う。**ゲートを緩めて通すのではなく、ゲートを正しくする。**
4. **AE カード#2 の文言は `".02 GRMS CRACK COCAINE" / WHAT THE OFFICER WROTE ON THE FORM`。** 旧文言 "THERE WAS NO SCALE" を復活させない。
5. **公開前 BLOCKING 2件（§R3-8）を潰すまで予約投稿しない。**
6. **TTS 実測後の再ロックは gap budget 198.9 s を起点に比例再配分する。** TOTAL 1,838.0 s / picture 1,829.0 s / `durationInFrames` 55,140 は R3 の台本訂正でも動いていないので、§1.5 の算術はそのまま有効。**再TTSで数字を合わせにいかない。**

---

## ★ 最終ゲート出力（R3 完了後・2026-07-29 実行・貼り付け）

```
$ ./.venv/Scripts/python.exe scripts/check_planning_package.py 57 fieldtest --require-r3
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
info word-ish count (latin tokens): 7037

RESULT: PASS (0 warn)
EXIT=0

$ ./.venv/Scripts/python.exe scripts/check_prompt_diversity.py episodes/_planning/EP57_fieldtest_CODEX_A_ASSETS.v001.md
ok   prompt coverage 104% (267/256 referenced asset ids)
info prompts extracted: 267 | boilerplate tokens dropped: 10 (df>30%)
ok   no same-series pair reaches Jaccard 0.5
WARN 8 cross-series twin(s) (still/motion pairs are often intentional — eyeball them):
  0.72  M35 ~ S175 / 0.70  M32 ~ S164 / 0.61  M16 ~ S076 / 0.60  M14 ~ S071
  0.54  M06 ~ S028 / 0.54  M42 ~ S208 / 0.52  M23 ~ S117 / 0.50  M05 ~ S032

RESULT: PASS (0 dup-pairs, 0 generic)
EXIT=0

$ ./.venv/Scripts/python.exe scripts/check_script_length.py --lo 1740 --hi 1860 episodes/_planning/EP57_fieldtest_script.en.v001.md
PASS script_length: 4,673 words (need 3,973-5,309)
  narration estimate  slow 28.5m | median 26.2m | fast 19.7m
  target band         29.0-31.0 min
```
> **R3 の7枚の差し替え（S017/S048/S066/S084/S132/S151/S203）を入れても diversity は PASS のまま、8件の cross-series twin も増減なし**（＝新しい重複を作っていない）。**`--require-r3` が緑になったのは R3 が実施され、本ログに実測入りの §R3 が入ったため。**

---

## R1/R2 時点のゲート出力（履歴・2026-07-29 実行・**R3 訂正前**）

```
$ ./.venv/Scripts/python.exe scripts/check_script_length.py --lo 1740 --hi 1860 episodes/_planning/EP57_fieldtest_script.en.v001.md
PASS script_length: 4,750 words (need 3,973-5,309)
  narration estimate  slow 29.1m | median 26.7m | fast 20.0m
  target band         29.0-31.0 min

$ ./.venv/Scripts/python.exe scripts/check_planning_package.py 57 fieldtest
（全 ok / RESULT: PASS。--require-r3 は当時 意図的に FAIL）

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

1. ~~**R3 独立レビュー（未実施・最優先）**~~ → **完了（2026-07-29）。§R3 参照。figure-beat の 92 vs 82 は 92 で決着済み（何も削らない）。★HP は 79→85 に是正済み。台本は 4,673語。** 残る最優先は **§R3-8 の公開前 BLOCKING 2件**（コロラド「全米初」の再確認 / Quattrone の 1.5M・90%・46% を PDF で確認）。
2. **サムネ文言のオーナー判断（FT-66）** — ブリーフの `IT WAS FOOD` は台帳が支持しない。`IT WASN'T A DRUG` / `0.0134 GRAMS` / `NO CONTROLLED SUBSTANCE` の3案。**R-6 のため、決めた文言が最初の20秒で発話されることを台本側で再確認すること**（現状 `IT WASN'T A DRUG` は ≈0:22 に存在）。
3. **ElevenLabs マスター生成（Brian 正典設定）→ ffprobe 実測 → `durationInFrames` 再ロック**（DESIGN §5 の手順）。**provisional は 172.0 wpm で立ててある**ので、EP55/EP56 級のドリフト（+71s）が出ても帯内に着地するはず。**再TTSで数字を合わせにいかないこと。**
4. **CODEX_A（`EP57_fieldtest_CODEX_A_ASSETS.v001.md`）で素材発注** — still 210 + i2v種 42 + thumb 3 + F系 12 = 267枚、アーカイブ 252本、overlay 30本。**★HP 85 = 40.5% を誕生時から。** アーカイブは §7.3 のクエリ表から始め、**ラベル付きコンタクトシート審査を飛ばさない**（棚の40%誤ラベル）。
5. **CODEX_B 執筆時** — DESIGN §3 の17カード表を B の契約表へ・`check_fieldtest_facts.py` を `check_burge_facts.py` から clone（R-NOT-A-DRUG / R-OFFICER / R-LIVING / R-NO-TEXAS-BAN / R-HOUSTON-REASON / R-COLORADO / R-NO-DRUG-DEPICTION / R-RACE / R-NUM / R-FACE / R-READABLE / R-LOGO / R-DOCHL / R-QUOTE / R-DATE）・held-beat 5本に slow-read cue・sting ≤5.0s 実測ゲート・**四層予算（archive ≥40% of cuts）の実測**。
6. **`footage_diversity` の名指しリスク** — 本作は法廷＋研究所の話で、棚は真鍮の天秤とガベルを大量に出す。**汎用象徴 ≤2 を必ず守る**（オーナーの積年の苦情）。
