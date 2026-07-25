# EP55 `review_log.v001` — 台本レビュー記録（R1 FACT AUDIT + R2 CRAFT/RETENTION AUDIT）

**Subject:** `EP55_burge_script.en.v001.md`（narration 4,689語 → R3修正後 **4,696語**）+ `EP55_burge_FACTS_LEDGER.v001.md`（BU-01〜BU-38）
**Reviewer:** Claude（左工程）R1/R2 ＋ **独立エージェント R3（2026-07-26）**  ·  **Result:** R1/R2/R3 通過（R3 で修正12件適用 → **script_verified 確定**）
**根拠:** `PD_ONE_PASS_PRODUCTION_SPEC.v2.md` rows 15/16、`EP55_burge_DESIGN_ARCHITECTURE.v001.md` §6、FACTS_LEDGER ガードレール。

---

## R1 — FACT AUDIT（台本の全 load-bearing 主張 × 台帳の行単位照合）

3本の並行 WebSearch/WebFetch 検証（2026-07-26・court records / 公式報告書 / 一次報道優先）→ 台帳 BU-01〜BU-38 に確定。台本の全主張を台帳に対応させた（対応表は script 末尾 SELF-CHECK PASS 1 に全行）。**検証で判明し、台本に反映済みの重要訂正:**

1. **Apollo Beach, FL**（発注時仮置きの "Apopka" は誤り）— 逮捕地・居住地とも Tampa 湾岸の Apollo Beach（BU-18/26）。
2. **起訴の内訳は「司法妨害2 + 偽証1」**（"偽証2+妨害1" は誤り）— 2008-10-16 起訴・10-21 逮捕（BU-26）。
3. Burge の無反省声明は **2015年4月・警官ブログ The Conviction Project 宛**（"2014・獄中" は不正確）。verbatim は "human vermin" 行のみ確認。**"so-called victims" は verbatim 未確認＝引用符で使わない**（BU-30）。台本準拠 ✓。
4. **記念碑は「長期遅延」からステータス更新**: 2026-07-08 に着工（5520 S. King Dr・総額$4.7M・2027完成見込み）。台本は「eleven years late, but coming」で反映（BU-34）。
5. Conroy の続報は「十数本」でなく **23本/約17年**（BU-16）。
6. 特別検察官の「合理的疑いを超える立証」は **正確に3件（Wilson/Adkins/Pinex）**・148件審査・約$7M・2006-07-19 公表（BU-20）。
7. 年金は **理事会 4–4**（警官系4 対 civilian 4）→ 維持、Madigan v. Burge（2014-07-03 イリノイ州最高裁）で確定（BU-29）。裁判所自体の 4–3 は M 扱い＝不使用。
8. 恩赦は **2003-01-10（DePaul・4人・innocence）**、翌 **01-11 に167人減刑（Northwestern）**。"demon of error" は DPIC 全文の verbatim（BU-22）。
9. 被害者数は幅で提示: **「100人超・弁護団の記録で少なくとも118人」**（Goldston 50 / PLO 118 / CPTA ~120）。TIRC の 600+ 件は 2016 拡張後の非Burge案件を含む＝Burge数として引用禁止（BU-07/38）。台本準拠 ✓。
10. Andrew Wilson の民事: 陪審 hung → 倒錯評決 → 1993 第7巡回区破棄。**賠償 ~$1M は本人にほぼ届かず**・2007 獄死（BU-11/12）。台本は本人受領に触れず「有罪の男の拷問こそ争点」と正面処理 ✓。
11. Vietnam の field telephone は **同中隊の従軍者証言として帰属**・Burge は否認 — 台本は "men who served in his unit later told reporters… Burge denied" で帰属 ✓（BU-03）。
12. 解雇日は資料間で 2/10 vs 2/11 が割れる → 台本は「February of 1993」に丸め（BU-18）✓。

**逐語引用の照合（台帳 §VERIFIED-VERBATIM の9系統のみ使用・全て一致）:** Raba "a thorough investigation (of this alleged brutality)" ✓ / Goldston "systematic"・"included psychological techniques and planned torture" ✓ / Holmes 3声明 ✓ / Ryan "demon of error…" ✓ / Fitzgerald "are gone" 圧縮引用は地の文に溶かし引用符は "There is no place for torture…" のみ ✓ / Lefkow "How can one trust the system of justice when the system is so defiled?" ✓ / Burge "broken man"・"human vermin" ✓ / Emanuel "a stain on the reputation of this great city"（部分引用・帰属明示）✓ / Jones "I got justice…28 years" ✓。**捏造引用ゼロ。**

**センシティビティ監査（HARD）:**
- ❌「拷問罪で有罪」と一度も書いていない — "never charged with torture" を3回明示・4.5年は常に「嘘」に紐付け ✓（R-BURGE-CONVICT）。
- 存命サバイバーの法的地位: 恩赦4人のみ innocence 断定・Kitchen/Jackie Wilson は台帳準拠の表現・**Andrew Wilson は「guilty」と明言**し拷問の不当性と分離 ✓（R-VICTIM-STATUS）。
- Midnight Crew 個人名: 拷問実行者として個人名を挙げず「his men / his detectives」。Yucaitis/O'Hara も台本では匿名（"the two detectives charged alongside him… suspended"）✓（R-CREW-NAME）。
- 拷問描写: ACT I で1回だけ・リスト形式・臨床的・「The film will not show it to you」と宣言。以後は "the box" 等の換喩のみ ✓（R-TORTURE-DEPICT）。
- Fahey/O'Brien は実名・哀悼付き・再現なし ✓。Daley は文書化された連鎖のみ・動機の断定なし（"Hold that name however you like" は評価を視聴者に委ねる構文で、事実主張を含まない）✓。
- 人種: "almost every one of them a Black man" を正面から・扇情なし・silhouette 規律は DESIGN/CODEX_A に接続 ✓（R-RACE）。
- hedge: "more than one hundred / at least 118 by his victims' lawyers' count"・"about seven million"・"roughly three thousand dollars"・"roughly fifteen separate injuries"・"$210M+ years ago and still climbing" ✓。exact-of-record（4½年・3 counts・6/28/2010・4–4・5/6/2015・$5.5M/57・9/19/2018）は断定 ✓（R-NUM）。

**R1 判定: PASS**（捏造ゼロ・全主張が BU 行にトレース・矛盾は台帳に注記済み）。

---

## R2 — CRAFT / RETENTION AUDIT（row 15/16）

**Hook-8s / cold open:** 冒頭8秒 = 「医師が説明のつかない火傷と電極痕を見つける」— 具体・即時・固有。20秒以内にオープンループ（「その手紙は33年後、教科書になる」）。HOOK-AUDIO（0:00から声）前提の一文目 ✓。
**Open loop（本編の背骨）:** 「拷問では一度も起訴されていない — なのに連邦刑務所に入った。この間にあるものが本作」= OPENING で明示し、ACT IV まで保持 → SPLIT_COMPARE で回収 ✓。
**Re-hook 節奏（~75–90秒毎に teased-then-delayed）:** "Remember the letter. It's coming back." / "watch that number climb" / "the machine made its one great mistake"（ACT I→II転換）/ "paper keeps coming back" / "It should have been [the end]. Because…"（ACT II→III）/ "The clock was his alibi" / "That should be the end of the story. It is not — because of four sheets of paper"（ACT III中腹）/ "He had just handed the government the only weapon it would ever get"（ACT III→IV）/ "Keep those two words in your ear… the city was about to answer them"（ACT IV内リフト）— 計9本・約2,600語/9 ≈ 290語(≈98秒)間隔・最長間隔でも~2分 ✓。
**Payoff order（最大の払い戻しを最後に）:** 有罪 → 4.5年の正直な怒り → 年金4–4の追い打ち → "human vermin" → 【史上初のリパレーション】 → 【カリキュラム＝真実が教科書になる】 → 無反省の死 → 着工した記念碑 → ENDING「Nobody beats the curriculum.」— 感情の最高点は最後の6分に集中 ✓。
**平坦区間:** 20秒超の無変化説明なし。唯一の法解説（時効）は「Holmes 1973→時計は1976に死んだ」の物語算術で処理（講義化回避）✓。ACT III 冒頭は意図した唯一のスローダウン（earned breath 対応・DESIGN §2）。
**AI臭キルリスト（全文 grep + 音読チェック済み）:** "little did / But here's the thing / needless to say / tapestry / testament to / chilling / shocking truth / dark secret / 3連対句の乱用 / rhetorical question 連打" = 0件。統計文体の平板さ回避: 文長 4語〜60語で変調・第二人称は宣言的箇所のみ（"Sit with that sentence." 等）・比喩は物語内在物（時計・紙・箱・声）に限定 ✓。
**Honesty bar:** 4.5年を「insult と感じるならその感覚を信じろ」と正面から書き、同時に「唯一の刑事罰だった」という逆側の真実も保持 — 誇張も慰めもなし ✓。
**尺・語数ゲート（実行出力の貼付・2026-07-26）:**

```
$ ./.venv/Scripts/python.exe scripts/check_script_length.py --lo 1740 --hi 1860 episodes/_planning/EP55_burge_script.en.v001.md
PASS script_length: 4,807 words (need 3,973-5,309)
  narration estimate  slow 29.4m | median 27.0m | fast 20.2m
  target band         29.0-31.0 min
  ! RISK: at the fast end of the measured pace (237.4 wpm, seen on williams/florence) this lands at 20.2 min -- under the floor. Either pin the voice speed or write to 6,885 words.
```

- narration 本体のみの実測 = **4,689語**（COLD OPEN→ENDING・ゲートと同一 regex で計測・ヘッダ装置118語を除く）→ オーナー帯 4,600–4,750 内 ✓。ゲートのファイル計 4,807 も要求帯 3,973–5,309 内で **PASS**。
- RISK 行への処置: fast 端 237wpm は williams/florence の声設定ドリフト起因（ゲート内コメント参照）。EP55 は Brian 正典設定（stability≈0.35 / similarity≈0.80・spec v2 row 2）で生成し、TTS 実測後に durationInFrames を再ロック（DESIGN §5）。設定固定で fast 端は発生実績帯 167–182wpm に入る＝帯内。
**息継ぎ字幕適性:** 短文主体・カンマ節が息継ぎ単位で切れる構造（"No answer. No investigation. Nothing." 等）。長リスト文（ACT I の手法列挙）は複数 cue に自然分割可 ✓。

**R2 判定: PASS**。

---

## R3 — INDEPENDENT REVIEW（別エージェント・fresh eyes・FIX AUTHORITY 行使）**実施済み 2026-07-26**

**Reviewer:** 独立 R3 エージェント（本パッケージの非執筆者）。**手法:** オーナー標準チェックリスト全項目の実測（語数・秒数・cadence は自前で再計算）＋ 15 load-bearing 主張の敵対的 WebSearch 再検証（台帳を信用せず独立照合）＋ センシティビティ・ハードゲート監査 ＋ 5文書クロス整合（S-row 全210・F-row 全235・検算再実行）。**修正はすべて本人が直接適用済み。**

### R3-1 オーナー標準チェックリスト（実測値つき）
| 項目 | 判定 | 証拠 |
|---|---|---|
| Hook = 冒頭8秒（≈24語）で具体・固有 | **PASS** | 第1文がちょうど24語（"In February of 1982, a doctor… injuries he could not explain away"）。謎（説明不能な傷）は word 19 ≈ 6.4s で開く |
| Open loop ~20秒以内 | **PASS** | word ~70（≈24s）で「電極痕」、~50s で「33年後に教科書になる」の約束、OPENING で「拷問では一度も起訴されず — なのに連邦刑務所」の本編ループ確定 |
| COLD OPEN → OPENING → 4幕 → payoffs LAST → 決定的エンディング | **PASS** | 有罪→年金4–4→"human vermin"→史上初リパレーション→カリキュラム→無反省の死→記念碑着工→「手紙が章になる」の順で最後の6分に最高点集中。ENDING は reparations/curriculum ビートで着地 |
| Re-hook ≤ ~90s @178wpm（自前再計算） | **PASS** | 36本の narrative turn の word-offset を実測。平均間隔 ≈44s、最長 91.0s（"sign so many confessions"→"It started early"）— その区間自体が Midnight Crew の手法列挙＝最高緊張の素材。90秒超の平坦区間ゼロ |
| AI臭ハント | **PASS（1件修正）** | キルリスト grep 0件。唯一の破綻構文「one month before Ryan's pardons had even settled into memory」（時系列が逆・恩赦は10ヶ月前）を修正 → "with Ryan's pardons still fresh in the city's memory" |
| ナレーションに日本語ゼロ | **PASS** | 全ファイル CJK 文字 0（実測） |
| 一流作家レジスター | **PASS** | 文長4〜60語で変調・比喩は物語内在物のみ・"Hold that name however you like" 等の声あり。R3 の修正はすべて事実精度であり文体は既に基準超え |
| buried-letter の背骨が閉じる | **PASS** | ENDING: "The letter was buried in a file in 1982. It came back as a chapter." ＋ OST "THEY BURIED THE LETTER. IT BECAME A CHAPTER." |
| 語数帯 4,600–4,750 | **PASS** | 修正後 narration 実測 **4,696語**（ゲート同一 regex）・ゲートfile-level 4,814 PASS（出力貼付は R3-4） |

### R3-2 敵対的ファクト・スポットチェック（15件・全件独立 WebSearch 照合）
1. **Raba 書簡（1982-02）** — VERIFIED。診察 2/15–16・書簡 "a thorough investigation of this alleged brutality"・Brzeczek→Daley 転送 **1982-02-25**・返答/捜査ゼロ（PLO・Wilson 民事記録・CPTA）。
2. **Andrew Wilson は有罪** — VERIFIED。Fahey/O'Brien 射殺（1982-02-09）・二度の有罪・拘置所搬入時 ~15 injuries・radiator 燒痕（7th Cir. 記録）。台本は有罪を正面から明言 ✓。
3. **Conroy "House of Screams"** — VERIFIED。Chicago Reader **1990-01-25**・以後17年で計 **23本**（CJR: 初報+22本）。
4. **Goldston 報告** — VERIFIED。"systematic"・"included psychological techniques and planned torture" 逐語一致・50人列挙・市が封印→**1992年連邦裁判所命令で公開**。
5. **解雇 1993-02** — VERIFIED。Police Board、2/10 vs 2/11 は資料割れ（台本の「February 1993」丸めは正当）。Yucaitis/O'Hara は15ヶ月停職→復職。**ただし Board の認定語は "physically abusing"＝「拷問」ではない → 台本の誤帰属を修正（R3-3 S1）**。
6. **特別検察官 2006** — VERIFIED。Egan/Boyle・2002任命・2006-07公表・**148件**・費用 **~$7M**（Wikipedia の "$17M" は同時代報道に不支持＝台帳が正）・**BRD はちょうど3件（Wilson/Adkins/Pinex）**・起訴ゼロ。台本は Wilson のみ実名 ✓。
7. **Ryan 恩赦** — VERIFIED。**2003-01-10 に Patterson/Hobley/Orange/Howard を innocence で恩赦**、翌 **01-11 に167人減刑**・"demon of error" 逐語一致（DPIC/forejustice）。
8. **Hobley interrogatories 2003-11** — VERIFIED。DOJ: 起訴は Hobley 2003 民事訴訟の宣誓回答に基づく（US v. Burge 記録）。
9. **起訴内訳・年表** — VERIFIED。**司法妨害2＋偽証1**・起訴 2008-10-16/逮捕 10-21 Apollo Beach・**2010-06-28 全訴因有罪**・2011-01 に **4.5年（54ヶ月）**・Butner NC（DOJ 発表）。
10. **Fitzgerald 逐語** — VERIFIED（"There is no place for torture… federal lawsuits."）。★原文は **"they're gone"** — 台本が "are gone" を引用符で出していたのを**地の文パラフレーズに修正**（R3-3 S5）。
11. **年金 4–4** — VERIFIED。2011-01 理事会、警官系4（維持）vs 市任命4（剥奪）・同数=維持。Madigan 提訴 → **イリノイ州最高裁 2014-07-03**（AG に管轄なし）・死亡まで受給。VOTE_SPLIT カード（4↔4・1回のみ）は BU-29 で完全に裏付く ✓。
12. **リパレーション 2015-05-06** — VERIFIED。全会一致・**$5.5M/57人**（~$100k each）・公式謝罪（Emanuel "…removing a stain on the reputation of this great city" 逐語）・**8年生+10年生必修 "Reparations Won"**（2017発表・2018春から授業）・CTJC・**市立カレッジ無償は本人+子+孫**・「全米初」は Amnesty 準拠のフレーズ ✓。
13. **記念碑** — VERIFIED・date-stamped。**2026-07-08 着工**・5520 S. King Dr・"Breath, Form & Freedom"・2027完成見込み（WTTW/Sun-Times/Block Club/市発表、2026-07-26 時点最新）。台本は「in the summer of 2026 … broke ground」で現在時点整合 ✓。
14. **死去** — VERIFIED。**2018-09-19**・70歳・年金受給のまま・無反省（WTTW 訃報）。"human vermin"（2015-04・警官ブログ宛声明）逐語一致。
15. **被害者数と公費** — VERIFIED as hedged。"more than one hundred… almost every one a Black man"（Goldston 50 / PLO 118 / CPTA ~120 / 2026 記念碑報道 "more than 125"）・TIRC 総数と非混同 ✓。**$210M+ は「years ago」で date-stamp**（Injustice Watch 2022-06）✓。
補強: Holmes 1973 ＋ 3逐語（CPTA/公判記録）VERIFIED / Melvin Jones **1982-02-05＝Wilson の9日前**＋"I got justice… 28 years"（WBEZ 2010-06-28）VERIFIED / Lefkow "…when the system is so defiled?"（UIC law repository・PLO sentencing report）VERIFIED。**捏造引用ゼロを再確認。**

### R3-3 発見欠陥と適用済み修正（重大度順・すべて修正済み）
- **S1（HIGH・誤帰属）** 台本: 解雇は「For the torture of Andrew Wilson — the board said it plainly」。Board の認定は **"physically abusing"** であり「board が torture と明言」は誤り → **"For the physical abuse of Andrew Wilson — the board's own words."** に修正（直後の「A man was fired for torture」は語り手の要約＝報道多数と整合・維持）。
- **S2（HIGH・引用捏造リスク）** 「even the judge called it a fraction of what the underlying conduct deserved」— Lefkow のそのような発言は確認不能（実発言は "so much pain could have been avoided…" 系）→ 判事帰属を外し語り手の判断に書き換え。
- **S3（HIGH・文書間矛盾）** DESIGN HARD FRAME が「perjury ×2 + obstruction」— 台帳 BU-26（★今セッション訂正済みの当該項目）と正逆 → **obstruction ×2 + perjury ×1** に修正。
- **S4（MED・時系列破綻）** 「In November 2003, one month before Ryan's pardons…」（恩赦は10ヶ月前）→ "with Ryan's pardons still fresh in the city's memory" に修正。
- **S5（MED・逐語不一致）** Fitzgerald "are gone" の引用符 → 原文 "they're gone" のため地の文パラフレーズ化（R1 の記載とも整合）。
- **S6（MED・未検証主張）** 「Anthony Holmes … is in the curriculum」→ 検証可能な事実（教員研修で自らの物語を語った・Rethinking Schools）に差し替え: "has told his story to the teachers who teach it."
- **S7（MED・過大表現）** OPENING「for almost twenty years he commanded detectives」— 指揮は 1981–91（巡査部長 1977–）・拷問期 1972–91 → "as detective, sergeant, and finally commander … he and the men around him" に修正。
- **S8（MED・カード検算）** DESIGN §3 デッキ「CENTER_STACK ×8・計~17枚」だが署名カード列挙は CENTER_STACK **9枚**（計18）→ **×9・18枚・≈100s** に統一（§0 の "~17 AE hero cards" も ~18 に）。A側 asset counts への影響ゼロ。
- **S9（LOW・語の捏造）** ENDING「four words — a thorough investigation, please」— "please" は Raba の語でない → **"three words — a thorough investigation."**
- **S10（LOW）** 「law students digging through transcripts」（台帳外）→ "lawyers"。
- **S11（LOW）** 年金の即時受給を示唆する語順 → "In time he had a police pension…" に修正。
- **S12（LOW・A文書内整合）** CODEX_A §5.13 F-series 12枚 と §5.10 "shots=255" 断言が衝突 → 「base 255 検証後に F 12行を追記・追記後 shots=267 が正」の R3 clarifier を §5.13 に追加（EP52 と同型の罠を先回り）。
- **（INFO・非修正）** R1 の hedge 列挙にある「at least 118 by his victims' lawyers' count」は台本本文には不使用（"more than one hundred" のみ＝台帳準拠で適法）。R1 の記載が台本を過大記述していた点のみ注記。／ 数値装置の連鎖更新: narration 4,689→**4,696**・narration_seconds 1,579.7→**1,582.1**・designed_gap 202.3→**199.9**（total 1,791.0・53,730f・563cuts・§3.3 検算[1]–[8] は全て不変のまま独立再計算で一致）。

### R3-4 クロス文書整合の実測
- **S001–S210 gap-free**: §5.6 motif レンジを全数照合 — 幕別 15/42/50/42/46/15＝210・レンジ連続・穴なし。★HP 57枚（10/14/10/23）＝27.1% は DESIGN §1 と一字一致。
- **factory F001–F235**: grep 実数 **235行**・全行 `public_path` 非空・subtype/act/covers_scene_id pre-assign 済み（stub なし）。motion **42行**・overlay **30行**（15P/10L/5V）実体化済み。
- **§3.3 検算の独立再計算**: [1] 244+235+84=563 ✓ [2] 1782/563=3.166 ✓ [3] 244/563=43.34% ✓ [4] 319/563=56.66% ✓ [5] 1.162/1.0/2.0 ✓ [6] 487/563=0.8650 ✓ [7] 563/487=1.156 ✓ [8] 59.4→235 ✓。
- **バン照合（プロンプト20+件精読）**: box は全プロンプトで inert・"connected to nothing"・無人室のみ（S021/S037/S066/M05/M18…）。装置+人体の同一フレーム記述ゼロ。サバイバー silhouette は全て "dignified, upright, backlit"（S054/S138/S160/H004/H011/H014/H015）。Yucaitis/O'Hara は台本で匿名・CODEX_A §1.2-5/§1.3 で prompt/tags 禁止 ✓。実在人物 likeness 禁止は [NEG]/[HNEG]/[TNEG]/[FNEG] 全レーンに実装 ✓。教室ビートの子供は out-of-focus のみ ✓。
- **VOTE_SPLIT**: 使用は年金 4–4 の1回のみ・BU-29（H）裏付け・ダウングレード時の CENTER_STACK フォールバックも記載済み ✓。

### R3-5 最終ゲート出力（R3 修正適用後・実行 2026-07-26）
```
$ ./.venv/Scripts/python.exe scripts/check_planning_package.py 55 burge --require-r3
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
info word-ish count (latin tokens): 6067

RESULT: PASS (0 warn)

$ ./.venv/Scripts/python.exe scripts/check_script_length.py --lo 1740 --hi 1860 episodes/_planning/EP55_burge_script.en.v001.md
PASS script_length: 4,814 words (need 3,973-5,309)
  narration estimate  slow 29.4m | median 27.0m | fast 20.3m
  target band         29.0-31.0 min
  ! RISK: at the fast end of the measured pace (237.4 wpm, seen on williams/florence) this lands at 20.3 min -- under the floor. Either pin the voice speed or write to 6,885 words.
  (RISK 処置は R2 と同一: Brian 正典設定固定・TTS 実測後に durationInFrames 再ロック)
```
**R3 判定: PASS — script_verified 確定。** EP15 Theranos 同様、公開前法務レビュー推奨の但し書きは維持（存命サバイバー多数・ただし全主張 court record/公式報告書ソース）。

## 申し送り（次工程）
1. ElevenLabs マスター生成（Brian 正典設定固定）→ 実測 forced-align → durationInFrames 再ロック（DESIGN §5）。※課金はオーナー承認フロー準拠（ElevenLabs は standing approval 済・cost 記録継続）。
2. CODEX_A（`EP55_burge_CODEX_A_ASSETS.v001.md`）で素材255枚+factory235+i2v42を発注。
3. CODEX_B は未執筆 — DESIGN §3 の**18カード表（R3 で ×9 CENTER_STACK に確定）**・§5 のタイミングを B 契約表に落とすこと。
4. `check_burge_facts.py` を EP52 の `check_morton_facts.py` から clone（R-BURGE-CONVICT / R-VICTIM-STATUS / R-CREW-NAME / R-TORTURE-DEPICT / R-RACE / R-NUM / R-FACE / R-READABLE / R-DOCHL / R-QUOTE / R-DATE）。
