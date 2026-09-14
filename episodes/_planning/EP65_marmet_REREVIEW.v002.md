# EP65 · MARMET — 脚本 再々レビュー（RE-REVIEW）v002

**対象：** `episodes/_planning/EP65_marmet_script.en.v002.md`（371行・LF・**現在ディスク上の実体**）
**基準：** `docs/PD_SCREENPLAY_STANDARD.v001.md` §15（即失格）／§16（R1〜R15）／§16.5（HOOK 8秒）
**設計：** `episodes/_planning/EP65_marmet_FILM_BIBLE.v001.md`（§1–§13 設計・§19 一周目への不合格リスト）
**一次資料（逐語照合に使用）：** `episodes/_planning/measurements/EP65_marmet_RAW.md`（SCOTUS 全文・179行）／
`episodes/_planning/measurements/EP65_brown_remand_RAW.md`（Brown II 全文）
**発注書：** `episodes/_planning/EP65_marmet_CODEX_BATCH_A.v001.md`（R001–R224）
**契約：** `episodes/PD-2026-065-marmet/episode_spec.v001.json`（mandatory_stills 220点・R220–R223 を含む）

> **このレビューの立場：** v001 の判定（PASS 10 / FAIL 5）は、**現在ディスクにある版より一つ古い版**に対して書かれた。
> 修理後の再レビューは一度も走っていない。したがって v001 は**過大にも過小にもなり得る**。ここで決着させる。
> 変更履歴は読んでいない。**現在の本文と、一次資料の原文と、発注書の実プロンプトだけを読んだ。**
> **R15（音読）は実施していない。実施したとは書かない。**

---

## 0. 独立実測（自己申告値は採らない）

`scratchpad\ep65_v2_measure.py` で再計算した。

| 指標 | 本レビュー実測 | 台本 L9 の申告 | 判定 |
|---|---|---|---|
| ナレーション語数 | **5,167** | 5,172 | 差 5語（抽出規則差）· 契約帯 [5100,5600] 内 · PASS |
| モデル総尺（HOOK 固定8s ＋ 残り176wpm） | **1,761.0s ＝ 29:21** | 29:23＝1,763秒 | 差 2秒 · **一致** |
| 区分見出しの合計 | **1,763s ＝ 29:23** | 同 | **一致** |
| 92%線 | 1,620.1s ＝ 27:00 | 27:02 | 一致 |
| 最後の新事実（L333）終端 | **1,614.0s ＝ 91.7%** | 91.7% | 一致 · 余裕 **6.1秒** |
| 短文（6語以下）比率 | **24.3%**（84/346） | — | 標準 20–35% · PASS |
| 修辞疑問 | 1（L345）＝0.19/1000語 | — | PASS |
| 二人称 | 1（L64 *"tells you"*）＝0.19/1000語 | — | PASS |
| ⟨HELD⟩（本文） | **3**（L311 / L339 / L367） | 「exactly three」 | 一致 |
| 40語以上の文 | **13**（うち ENDING **0**） | — | 後述 |

**v001 指摘0-A（同一ファイルに尺の数字が4つある）は解消している。** 各区分の実測語数から導いた尺と、
見出しの (mm:ss) は全区分で誤差1秒以内に一致する（ACT_1 285.0/286・ACT_2 350.1/350・ACT_3 318.4/319・
ACT_4 276.1/276・ACT_5 362.7/363・ENDING 137.7/138）。数字は一つになり、自己整合している。

**残る計測上の注意 2件（いずれも新規）：**

- **HOOK が語数超過。** HOOK は 25語。この稿自身のレート 176wpm では **8.5秒**であり、固定枠 8.0秒を
  0.5秒超える。§16.5 の窓（約20〜25語）の上端で、`hook_added` の受入窓（6〜10秒）は割らない。
  ただし「Windows are derived, not chosen」（L7）に対して、HOOK だけは導出でなく固定である。
- **92%線の余裕が 6.1秒しかない。** v001 の版は 28秒あった。最後の新事実 L333 の終端 1,614.0s に対し
  92%線 1,620.1s。**実VOが 176wpm より 0.4% 遅いだけで L333 が 92% を越える。**現状 PASS だが、
  ナレーション収録後に再測定しないと緑を維持できない。

---

## 1. v001 の 5つの FAIL は、いまどうなっているか

| v001 の FAIL | 現在 | 根拠（機械照合・現在の本文） |
|---|---|---|
| **R2**（主題の重要性を語り手が宣言する文が6本） | **解消（PASS）** | 6本すべて消滅。`the reason this` / `worth telling` / `exists to say` / `load-bearing` / `the distance between them` / `Any version of this story` すべて **0件**。跡地は事実文に置換されている（例：L280 は *"The next sentence, in the same paragraph:"*、L296 は *"And the court did not take back the language that had got it reversed."*、L353 は *"The savings clause was there the whole time."*） |
| **R3**（他人の語り直しへの反論・観客への指示） | **解消（PASS）** | 型①は全滅：`retelling` / `most accounts` / `gets left out` / `routinely got wrong` すべて **0件**。型②の *"Take that apart"* / *"Keep that distinction"* も 0件。残置指定の L194 *"Keep the second half. It comes back."* は健在で、**L353 で実際に回収されている**（14分の予告→回収）。型③の *"That is a court …ing"* は 2→**1**（L300 のみ。L148 は *"Disingenuous."* 一語に落ちた） |
| **R6**（モチーフ） | **依然 FAIL・ただし理由が別で、はるかに狭い** | 登場順は修復済（本編内で 1→2→3→4→5→5→6→7 と単調・逸脱2件はいずれも本文で「flash-forward」「callback」と明記）。椅子は HOOK から外れ、L62 が「一度きりのプラント」と明記。手の縦糸（v001 b-4）は**実装された**。**残る不良は一点：状態1に割り当てられたプレート R152 に罫線が写らない**（§5-A） |
| **R11**（画のループ） | **依然 FAIL・ただし理由が別で、はるかに狭い** | v001 の中心根拠（R001 は真上マクロだから椅子が入らない）は**消滅した**。L16 が *"It is NOT the last image of the film."* と明記し、ループ用に **R222 / R223 が実際に発注書へ追加されている**（発注書 §7・2026-08-04 追記・spec の mandatory_stills にも 220点として収録済）。残る不良は R6 と同一（§5-A） |
| **R15**（音読） | **NOT PERFORMED（本レビューでも未実施）** | §19 が指定した具体2件は**両方とも実行済**（L335 は *"dockets on screen only, never in the voice"*・L306 は39語ノーコンマを三文に分割）。ただし通し音読の記録は無く、`EP65_marmet_ASSEMBLY_HANDOFF.v001.md` L33 が自ら「**❌ 未実施**」と記録している |

### v001 が VERDICT で挙げた7つの理由の現況

| # | v001 の理由 | 現況 |
|---|---|---|
| 1 | R11 の是正が物理的に実行不能（R001 に椅子は入らない） | **解消。** R222/R223 が発注済。L369 が *"Do NOT substitute R001"* と明記 |
| 2 | モチーフが一つでない（椅子が7回・HOOK 8秒の半分） | **台本内では解消**（HOOK は4カット・椅子専用カット0）。**発注書では未解消**（§4-C） |
| 3 | 人間の縦糸が台本に一行も無い | **解消。** 手が4回（L36 R152・L44 R066・L86 R038・L102 R064）。**4枚とも実在プロンプトと一致**（例 R152 = *"A hand pressing a stack of blank sheets square against a desk, no face"*） |
| 4 | L317↔L323 が分離し *"these cases"* の先行詞が *"specific cases"* になっている | **解消。** L321 が *"So it sent **Brown's case and Taylor's case** down rather than answering them. In its own words."* を挟んでから引用に入る。`specific cases` は L315 に**1回だけ**（v001 は2連） |
| 5 | 最初の台詞と最後の台詞が免責文と反対の形 | **解消。** L18 は *"**Two papers said this:** a dispute about how somebody died goes to a private arbitrator."*、L365 は *"The clause, once more, **as the two papers wrote it.**"*。どちらも帰属付き・紙が主語 |
| 6 | 五桁 docket 三連が耳に置かれている | **解消。** L333 は名前のみ、L335 が 【OST, dockets on screen only, never in the voice】 |
| 7 | ENDING の序数二系統・46語の一文・「出来事の要約」化 | **序数と長さは解消**（L361 は「第一の問い／マルキオの件／第二の問い」で一系統、最長文 ~30語、**ENDING に40語超は0件**）。要約→再フレームも実質解消（§7）。**残渣：L361 が L333 の処分を二度目に述べている** |
| 0-A | 尺の数字が4つある | **解消**（§0） |
| 0-B | `mandatory_stills` が v001 語数で比例配分されたまま | **未解消・悪化**（§4-D） |

---

## 2. 所見表

| id | R番号／§15行 | 判定 | 行 | 根拠（現在の本文・原文・実プロンプト） | 直すもの |
|---|---|---|---|---|---|
| F-01 | R1 | **PASS** | L18 / L80 / L347 | 主題「署名は、署名した人ではなく、署名させた側の設計を実行する」を、口に出さず三度実演。L347 *"A form that sent every dispute to a private arbitrator, except one — a claim to collect late payments owed by the patient. A form that made whoever filed first pay to file. And in one of the three cases, a form with no exceptions in it at all."* — v001 が唯一の実演として挙げた *"the single dispute the nursing home might want to bring itself"* は**削除され、記録に無い意図推定を含まない形になった** | — |
| F-02 | R2 | **PASS** | — | 6本すべて0件（§1） | — |
| F-03 | R3 | **PASS** | L194→L353 | 型①0件・型③1件。L194 の予告が L353 で回収 | — |
| F-04 | R4 | **PASS** | L306→L308/L309→L311 | 認知は一箇所（81.9%）。⟨HELD⟩ 3個。「ここが核心」の予告は全滅 | — |
| F-05 | R5 | **PASS** | L160–L212 / L264 | ACT_3 が 934語・319秒（全尺 18.1%）を施設側の完勝に使い、L206 *"Preempted. Preempted. Preempted. Preempted."* → L212 *"must be vacated."*。施設側の反対主張も L264 で鳴る（原文照合済・Brown II） | — |
| **F-06** | **R6** | **FAIL** | **L36** | 状態1の指定は *"a stack of admission forms just off the printer, **the ruled line at the foot of the top sheet still empty**"*（plate R152）。**R152 の実プロンプトは *"A hand pressing a stack of blank sheets square against a desk, no face"*** — 罫線も、入所用紙も、カウンターも入っていない。**この映画唯一のモチーフが、状態1のプレートに写らない** | L36 を R222 の構図に寄せる（下記 §9-1） |
| F-07 | R7 | **PASS** | L48 / L50 / L68 / L325 | 反復不能な細部が健在。L50 *"after hearing argument of counsel, reviewing the respective briefs and the record"*（Brown II 註126 と逐語一致）／L325 の *January 1, 2003* と *"Friday, July 24, 2009"*（Brown II 註230 と逐語一致）。`Sutphin` `Canoe` は 0件（禁止遵守） | — |
| F-08 | R8 | **PASS** | L327 | v001 唯一の例外 *"might want to bring itself"* は **0件**。`worst week` 0件。手本 L327 *"The forums named in the papers had stopped taking the kind of case the papers were sending them."* は無傷 | — |
| F-09 | R9 | **PASS** | L48→L38→L126→L210→L192→L317 | 縦に上がる。L126 *"Not this clause. Not these three clauses. Any such clause, in any nursing home admission agreement in the state."*。統計・パーセントは 0件 | — |
| F-10 | R10 | **PASS（余裕6.1秒）** | L333 / L347–L365 | 最後の新事実は L333（91.7%）。ENDING の全節を逐一照合し、**新事実は無い**（§7）。ただし 92%線まで 6.1秒 | 収録後に再測定 |
| **F-11** | **R11** | **FAIL** | **L36 ↔ L369** | 文字のループは成立（L20 →L370）。画のループは、閉じる側（L369 = R223 *"its ruled line bare and no pen anywhere on it, and beyond the counter … the far chair still pushed in square"*）は**実在し正しい**が、**開く側（L36 = R152）に罫線が無い**ため、同じ物の状態変化として閉じない。台本自身が *"The loop is the LINE, not one lens"* と書いているのに、**その LINE が state 1 に無い** | F-06 と同一の一手で閉じる |
| F-12 | R12 | **PASS** | L311 / L339 / L367 | 3個。すべて重い一文の直後（認知直後／限界 L337 直後／最終画直前）。ほかに画の休符2件（L62 3秒・L214 4秒）は §19 が許容した種類 | — |
| F-13 | R13 | **PASS** | L284 / L286 / L288 / L333 / L361 | reaffirm↔modify の並置を**原文で再照合**：Brown II 本文46行目 *"…we otherwise reaffirm all of our discussion and holdings in Brown I."* → 48行目 *"However, in light of the parties' additional briefs and arguments, we modify our conclusions in Brown I."* — **段落が実際に隣接**しており L286 の *"in the next paragraph"* は正しい。註釈なし。処分の非一様性も L333／L361 で平らにしていない | — |
| **F-14** | **R14** | **FAIL（3件・すべて狭い）** | **L317 / L134 / L347** | (a) **L317** *"There was no evidence to weigh, **because nobody had been permitted to take any**."* — 「取らせてもらえなかった」は Brown II 48行目の**原告側の主張**（*"counsel for the plaintiffs asserted — because the trial courts did not permit the parties to develop evidence…"*）。裁判所自身の語は *"the circuit court **has not had the opportunity to** comprehensively analyze"*（50行目）。**主張が語り手の認定になっている**（§13）。(b) 同 L317 の *"that court **had never** comprehensively analysed"* も、原文の *"has not had the opportunity to"* を落として断定側に寄せている。(c) **机**：FILM_BIBLE §19 R14(e) は「机は記録に無い。**画で出して語らない**。ナレーションからは落とす」と明記したが、L134 *"One side of **that desk**"*・L347 *"signed at **an admission desk**"* の2回、ナレーションに残っている。しかも L134 の *"that desk"* は**音声上の先行詞が無い**（机の初出は L36/L62 の画指定のみ） | (a)(b) は L317 の一文だけ／(c) は2語 |
| F-15 | R15 | **NOT PERFORMED** | — | 通し音読の記録は存在しない。`EP65_marmet_ASSEMBLY_HANDOFF.v001.md` L33 が自ら「**R15（音読）❌ 未実施**」と記録。本レビューも音読していない。§19 が指定した具体2件（L335 docket・L306 の呼吸）は**実行済**。文字から機械的に導ける残存危険は §6 | 通しで読んで記録する |
| **F-16** | **§8（1分あたり5〜12個の硬い事実）** | **FAIL** | **L130–L140** | 320語・109.1秒（28.2%→33.8%）に**日付0・固有名0・金額0・地名0**。行為者は最後まで *"the court"* / *"the courts of this State"* だけ。§8 の下限 5個/分に対し **0個/1.82分**。詳細は §5-B | §5-B の三点 |
| **F-17** | **§13（記録に忠実）** | **FAIL（新規発見）** | **L132 / L134** | ACT_2 は Brown One（2011年6月29日）の節であり、L132 は *"The court also said something about admission day that would matter **a year later**."* と**2011年の発言として枠付けする**。しかし Brown II 56行目を見ると、4文のうち **fn20 と fn21 の2文だけが Brown I からの引用**で、***"Nursing homes daily sign contracts with patients as a routine course of doing business."*** と ***"People seek medical care in a nursing home for long-term treatment to heal, and do so only a few times in life."*** は**引用符も脚注も無い Brown II（2012年）自身の地の文**である。**手元の捕捉は、この2文を2011年に置く根拠を持たない。**しかも L134 はその2文の上に建っている | §9-4 |
| F-18 | §15-1（事実の捏造） | **該当なし（F-17 は日付の帰属ずれであり、捏造ではない）** | — | 照合した範囲で、存在しない事実・数字・名前・動機・内面は見つからなかった。L118 の Syllabus Point 21 全文（Brown II 38行目）・L104 *"an extensive opinion with three holdings"*（同28行目）・L110/L114（同32行目）・L166（同146行目）・L142（同160行目）・L292（同34行目）・L294/L282/L361（同12行目）・L333（同104/106/108/110行目）・L325/L329/L331（同230/234/236行目）、および SCOTUS 側 L182/L186/L190/L196/L198/L200/L202/L204/L208/L210/L212/L228/L232/L234/L238/L246 をすべて原文と突き合わせた | — |
| F-19 | §15-2（感情命令） | **該当なし** | — | `imagine` `shocking` `astonish` `devastating` `tragic` すべて 0件 | — |
| F-20 | §15-3（説教） | **該当なし・ただし1箇所が接近** | L258 | `we must` `we should` 0件。ただし L258 *"…and **nobody should be told** which Justices stood behind it, because the document does not say."* は「この話をどう語るべきか」という**語り手の指示**であり、§19 が一掃した解説者の register の唯一の生き残り | 後半節を落とす（§5-C） |
| F-21 | §15-4（真犯人当ての枠組み） | **該当なし** | — | 謎解き構造なし。結末は冒頭 L18 で先に開示されている（劇的アイロニー型） | — |
| F-22 | §15-5（沈黙する記録への声当て） | **該当（F-14a と同一）** | L317 | 上記 | — |
| F-23 | §15-6（悪役の創作） | **該当なし** | — | 個人・法人とも造形なし。`Sutphin` 0件。施設側の主張は L264 で最強の形で提示 | — |
| F-24 | §15-7（語り手が結論を言う） | **該当なし** | — | §1 の通り、宣言型は全滅。残る解釈文は L300 / L236 / L266 の3件で、いずれも文書についての観察であって主題の言明ではない | — |
| F-25 | §15-8（カテゴリだけの人物造形） | **該当なし** | — | そもそも人物を描かない設計（FILM_BIBLE §2）。L68 *"No ages. No conditions. No dates of admission, no dates of death."* が欠落そのものを主題化している | — |
| F-26 | §15-9（数字の発明） | **該当なし** | — | パーセント・統計・平均 0件。L82 は *"The opinion states no dollar figure."* と明記している | — |
| F-27 | §15-10（隔離済み⛔の使用） | **該当なし** | — | ⛔-01（家族は仲裁に送られた）：L18/L365 とも紙が主語で回避。⛔-04（州の理屈を映画の声にしない）：L132/L134/L142 に帰属が付いた。⛔-05（三家族を混ぜない）：L88/L128/L333/L361 で分離維持。⛔-10（per curiam＝全員一致と言わない）：L258 が明示的に否定 | — |
| **F-28** | 発注書との不整合（§4） | **FAIL（台本外だが出荷を止める）** | 発注書 L150–L154 / L132–L137 / L658 | 発注書が**まだ旧ループ（R001 が閉じる）を宣言**し、**椅子を4箇所で意味付き**に発注し、**v001 の語数で枚数を比例配分**している。台本 v002 とすべて衝突 | §4 |

---

## 3. R1〜R14 集計

**PASS 11 ／ FAIL 3（R6・R11・R14）／ R15 は NOT PERFORMED。**
（v001 は PASS 10 / FAIL 5。一周目の §19 は PASS 4 / FAIL 11。）

**R6 と R11 は同一の不良を二つの行から見たものであり、原因はプレート1枚である。**
**R14 は一文と二語である。**

---

## 4. 台本の外にある不整合（脚本の判定には入れないが、この状態で組むと壊れる）

### 4-A. 発注書がまだ「R001 が映画を閉じる」と宣言している

発注書 L150（HOOKの約束→回収表）：

> | `R001` ペンと読めない一筆 | 「受付で署名した紙」＝この映画の主題そのもの | ENDING `R191` `R192` `R205` `R206`（**同一構図で閉じる**）／ACT_1 `R035` |

発注書 L658：

> | ループ結合＝1コマ目に戻る | `R074` → `R191` → `R001` |

台本 L16 は正反対を書く：*"It is NOT the last image of the film. The macro loop is state 1 … returning as state 7 … plate R223."*
**同じパッケージの二つの文書が、映画の最終画について反対のことを言っている。**

### 4-B. HOOK の枚数

発注書 L123–L130 は **HOOK＝R001–R005 の5枚**、L125 は「HOOKの各プレートは本編のどこかで必ずもう一度出る」。
台本 L15 は **4カット**（R001 2.2s → R002 1.8s → R005 2.0s → R003 2.0s）で、R004 を HOOK から外して ACT_5 へ回す。
台本側でこの処理は明示・正当化されているが、**発注書の回収表 L153 は R004 を依然 HOOK プレートとして扱っている。**

### 4-C. 椅子は、台本では一度きり／発注書では意味付きで4回

台本 L62 は *"It is a plant, not a motif: the empty chair is not to be cut in anywhere else, and R004 / R075 / R176 / R201 are ordinary cuts, not chair beats."* と宣言する。
しかし発注書 L153 は R004 の**意味**を「署名しなかった人の不在」と定め、回収先を **ACT_2 `R075` ／ ACT_5 `R176` ／ ENDING `R201`** と指定している。
**台本の宣言では、発注書がプレートに与えた意味は消せない。**標準 §5「モチーフは一つ」は、台本内では守られ、パッケージ全体では守られていない。

### 4-D. `mandatory_stills` はまだ v001 の語数で配分されている（v001 指摘0-B・**未解消かつ悪化**）

発注書 L132–L137 の配分根拠と、v002 の実測語数：

| 区分 | 発注書の根拠（v001） | v002 実測 | 差 |
|---|---:|---:|---:|
| ACT_1 | 932 | **836** | −96（**−10.3%**） |
| ACT_2 | 1,020 | **1,027** | +7 |
| ACT_3 | 971 | **934** | −37（−3.8%） |
| ACT_4 | 873 | **810** | −63（−7.2%） |
| ACT_5 | 957 | **1,064** | **+107（+11.2%）** |
| ENDING | 445 | **404** | −41（−9.2%） |
| 合計 | 5,434 | **5,167** | −267 |

spec `notes` と FILM_BIBLE §19.1-8 が命じた再導出は**まだ実行されていない**。ACT_5 が 11.2% 過小配分になっている。

### 4-E. プレートIDが区分をまたいでいる

発注書 L132–L136 の ID 範囲は区分ごとに固定（ACT_1＝R011–R045／ACT_2＝R046–R083／ACT_4＝R121–R153）。
台本は **R152 を ACT_1（L36）**、**R066 を ACT_1（L44）**、**R022 を ACT_2（L102）** に使う。3枚が区分をまたぐ。
プロンプトの中身は台本の指定と一致しているので画は撮れる（R066 = *"A pen offered across a counter, held out by the barrel, both hands cropped at the wrist"*、R022 = *"A metal filing cabinet drawer pulled out to show a row of identical unlabelled tabs"*）が、**区分別の枚数は発注書と合わない。**

---

## 5. 指定された検査箇所

### 5-A. R6／R11 の残る一点 — 状態1のプレートに罫線が無い

実プロンプトを発注書から直接読んだ。

| 台本の指定 | プレート | 実プロンプト（発注書） |
|---|---|---|
| **L36 = motif state 1**「印刷したての用紙の束・一番上の罫線はまだ空」 | `R152` | *"A hand pressing a stack of blank sheets square against a desk, no face"* |
| L62 = 椅子のプラント | `R222` | *"An admission desk seen from the visitor's side at waist height with two chairs in the frame, the near one drawn out and turned slightly away, the far one pushed in square and empty, **one form squared on the counter between them**, the light flat and grey"* |
| **L369 = motif state 7**（最終画） | `R223` | *"The foot of an admission form lying on a counter, **its ruled line bare and no pen anywhere on it**, and beyond the counter and slightly out of focus the far chair still pushed in square, the late afternoon light gone flat"* |

**R223 は正しい。R222 も正しい。R152 だけが、この映画の唯一のモチーフを含んでいない。**
`blank sheets` は「白紙」であって「罫線のある入所用紙」ではなく、カウンターも椅子も入らない。
したがって台本 L369 の *"state 1's empty line at the head of ACT_1 returns here as state 7"* は、
**開く側の画が存在しないために成立しない。**

**最短の修理（新規プレート0枚・語数0）：** L36 の画指定を **R222** に振り替え、L62 のプラント（3秒ホールド）と統合する。
R222 には *"one form squared on the counter"* が既に入っており、R223 と**同じ視点・同じ机・同じ椅子**である。
これで state 1（R222）→ state 7（R223）が**実在する二枚で同一構図のループ**になり、椅子のプラントも同じカットに乗る。
代償はプラント位置が 2:36 → 0:31 へ動くこと（回収距離は約28.7分。標準の「2分以上」を大きく満たす）。
台本 L5 の lock 文（*"motif state 1 at the head of ACT_1"*）とも矛盾しない — むしろ現行より合う。
**R152（手が束を揃える）は、状態1ではなく「手の一回目」として同じ位置に残せばよい。**

### 5-B. L130–L140 — 320語・109.1秒・28.2%→33.8%（依頼の主眼）

**測って確認した。**6行（L130 / L132 / L134 / L136 / L138 / L140）= 33+73+44+58+58+54 = **320語**、
485.6s→594.7s = **109.1秒**。この 109秒に、**日付0・人名0・機関の固有名0・金額0・地名0。**
行為者は最初から最後まで *"the court"* / *"the courts of this State"* だけである（Brown One の名が戻るのは L142）。

**判定：抽象に落ちている。シネマとして持たない。** 根拠は三つあり、いずれも標準の明文である。

1. **§8 の下限割れ。**「1分あたり5〜12個の硬い事実」に対して、**1.82分で0個**。反復不能な細部が一つも無い。
2. **§2 の離脱点。**「説明が三つ続いたら、そこが離脱点である」。ここは**六つ続く**。
   L130（構造の要約「二つの扉」）→ L132（入所日の一般論）→ L134（両側の頻度）→ L136（unconscionability の定義）→
   L138（何を言っていないかの断り）→ L140（adhesion contract の定義）。全部が教義の説明である。
3. **§10 の壁が再発している。**第一コンマまで29語以上の文は、この稿に6つあるうち **L138（32語）と L140（29語）が隣接**している。
   これは FILM_BIBLE §19 R15(c) が L105–L107 で名指しし、**L112 *"That is the rule it wrote."*（6語）を挟んで修理した壁と同型**である。
   同じ修理がここには当たっていない。逃げ場は L136 末尾の *"It is not a rule about arbitration. It is a rule about contracts."* だけ。
4. **画も無い。**【 】の画・モチーフ・OST 指定は L102 の次が L214 であり、**668秒（11分08秒）にわたって一つも無い。**
   これはこの稿で最長の視覚指定空白であり（次点は L224→L254 の170秒）、L130–L140 はその中心にある。

**何が担うべきか（すべて既出の事実・新事実ゼロ）：**

- **(あ) 二枚の同じ紙と、三枚目の違う紙。**L78（*"The relevant parts of the agreements in Brown's case and Taylor's case were identical."*）と
  L88（*"No carve-out for late payments. Nothing about who pays to file."*）は、この映画自身が持っている
  *"leaves the subscribing party little or no opportunity to alter the substantive terms"*（L140 の定義）の**実物**である。
  L140 の定義の直後に、**15語以内でこの三枚に戻す。**教義の直後に物を置く。
- **(い) 手数料条項。**L82 の *"The party filing the arbitration is responsible for paying a filing fee … The opinion states no dollar figure."* は
  「一方的さ」の**唯一の具体物**であり、5分半前に一度出たきり L347 まで使われない。
  L136 の *"That is unconscionability."* の直後に置けば、抽象語が即座に物に着地する。
- **(う) 画を一枚入れる。**発注書 L152 が既に **`R036` `R037`（2枚同一・1枚だけ違う紙）** を ACT_1 の回収として発注済である。
  ここに置くのが最も安い（新規発注0）。
- **(え) L138 と L140 のあいだに5語以下の一文を挟む**（§10・L112 と同じ手）。

**この4つは合計で語数を増やさない**（(あ)+(い) で +25語前後、L136/L138 の重複説明を落として −25語）。

### 5-C. L252–L260 — 166語・56.6秒・66.7%→69.0%

L252(48) + L256(49) + L258(50) + L260(19) = **166語**、1,158.6s→1,215.2s = **56.6秒**。

**判定：持つ。ただし2点。**
硬い事実はある（*"The five pages do not mention it."* / *"Charleston"* / per curiam の三属性）。
L254 に 【callback: the carve-out line, held on screen】 があり、画の空白でもない。

- **(1) L258 は L28 の再定義である。**L28 が既に *"per curiam — an opinion issued by the Court with no author's name on it and no vote reported"* と定義しており、
  L258 の *"There is no author, no reported vote"* は**21分後に同じ内容を繰り返している**。新しいのは
  *"no separate writing attached to the text"* と *"It is not a synonym for unanimous"* の2点だけである。
- **(2) L258 後半が唯一残った解説者の声。** *"…and **nobody should be told** which Justices stood behind it, because the document does not say."*
  「誰も〜と告げられるべきでない」は、事件ではなく**この話の語られ方**についての指示である（F-20）。
  *"…and the document does not say which Justices stood behind it."* で足りる。**−7語。**

*（併記：L248→L250→L252→L256 は否定形の文が4連続する。事実として正しく、この映画の内容そのものだが、
耳は「無かったこと」を4つ数えられない。上の(1)(2)で L258 を縮めると、否定の連鎖も一つ短くなる。）*

### 5-D. L230–L236 — 140語・47.7秒・58.9%→60.9%

L230(38) + L232(36) + L234(35) + L236(31) = **140語**、1,023.9s→1,071.6s = **47.7秒**。

**判定：持つ。**具体の錨がある（*"Two of the three papers had been condemned twice … The third had been condemned once"*）。
原文照合済（SCOTUS 149–163行）。終わりが物の像である（L236 *"sitting in the middle of the contract analysis"*）。

- **唯一の注記：** `alternative holding` が L228 を含めて**5回・68秒**に出る。耳では術語の反復に聞こえる。
  L232 の *"the state court's alternative holding"* か L234 の *"In its discussion of the alternative holding"* の
  どちらかを *"there"* に落とせる（原文の意味は変わらない・**−4語**）。
- L236 は L234 の引用が既に届けた結論を語り手が言い直している。ただしこれは §19 が「削るな」と指定した
  L184（*"Misreading and disregarding…"*）と同種の**語彙の観察**であり、削る側に倒す必要はない。

### 5-E. L304–L311 — 122語・41.5秒・80.7%→81.9%

L304(60) + L306(62) = **122語**、1,401.0s→1,442.5s = **41.5秒**。直後が L308/L309 の callback と L311 の ⟨HELD⟩。

**判定：L306 は PASS。L304 は認知を薄めている。**

- **L306 は修理が効いている。** v001 が「この稿で最悪」と名指しした39語ノーコンマ文は、**三文に割られた**：
  *"…may manifest itself in the form of an agreement requiring arbitration only for the claims of the weaker party. **But a choice of forums for the claims of the stronger party.** Agreements to arbitrate, the court wrote, must contain at least a modicum of bilaterality to avoid unconscionability."*
  対句が対句として聞こえる。**原文照合済**（Brown II 84行目）。語は一つも足さず引かず、句読点だけを変えている。
  *（注記：*"But a choice of forums…"* は原文では従属節であり、独立文として鳴らすと文法的には断片になる。
  音では正しい。文字テロップに出す場合だけ注意が要る。）*
- **L304（60語）は不要である。** これは sliding scale の教義（*"procedurally and substantively unconscionable"* / *"vice versa"*）で、
  **この稿で最も専門語密度が高い60語**が、**映画唯一の認知の直前**に置かれている。
  §4.2 は「前半はここへ向かって組み、後半はここから落ちる」と書く。認知の直前は絞る場所であって、厚くする場所ではない。
  そして**認知は L304 を必要としない** — L306 の対句と *a modicum of bilaterality* だけで成立する。
  **L304 を丸ごと落とすと −60語で、認知が締まる。**

---

## 6. R15 の代替（音読ではない。音読はしていない）

> **これは R15 の履行ではない。**標準 §16 は「声に出して読んだか」を問う。本レビューは読んでいない。
> 以下は**文字から機械的に導ける音声上の危険箇所**である。通しの音読と読了記録は依然として未履行である。

**修理済み（実測で確認）：**
- L40 の Clarksburg 二重名 → §19 の置換案が**そのまま**入っている。
- L110（76語）→ **L112 *"That is the rule it wrote."*（6語）** → L114 の壁割り。
- L192 の「聞こえないコンマ」→ *"And then, in the same sentence of the statute, an exception that decides everything that follows."* に置換。**`Then a comma` は0件。**
- `Brown I` **0件**・`Brown One` **12件**。表記は完全に統一された（v001 は1件混在）。
- 五桁 docket 三連 → **耳から消えた**（L333 は名前のみ／L335 は 【OST … never in the voice】）。
- 第一コンマまで25語以上の文：**10 → 6**（L114 25 / L138 32 / L140 29 / L196 27 / L202 27 / L298 45）。

**残る危険（実測）：**
- **L298 は第一コンマまで45語**（この稿の最長）。主語 *"The Supreme Court"* と述語 *"summarily concluded"* が
  29語のダッシュ挿入句で隔てられている。**原文どおり**（Brown II 42行目）なので事実としては動かせないが、耳では主語が失われる。
- **L138(32語) と L140(29語) が隣接**（§5-B-3）。
- **Marmet / Marchio の三連は残っている。** L38–L40：*"Brown sued **Marmet** Health Care Center. Taylor sued **Marmet** Health Care Center. **Marchio** sued a nursing home in Clarksburg."* — 「マー」で始まる語が3文連続。
- **L292 に数字が3つ**：*"Syllabus Point 11 … section 15(c) by section 2 of the FAA"*。
- **引用符が本文に0個。** ナレーションの相当部分が逐語引用だが、音声上の境界は**リードインだけ**が担っている。
  v002 はリードインを大幅に増やした（*"in the court's own phrase"* / *"the court wrote"* / *"In its own words."* /
  *"The state court's finding, in Brown One:"* / *"in the words it reaffirmed:"* / *"quoted in the opinion:"* /
  *"Its own sentence, quoted back to it the next year in Washington."*）ので v001 時点より大きく改善しているが、
  **引用の終端の合図は依然として段落の切れ目だけ**である。
- `unconscionable` の初出は L46（約1:10）、定義は L136（約9:00）。**約8分の空白**は v001 のまま。

---

## 7. L144 の裁定（依頼事項）

**現在の本文（L144）：**

> *"But being a form is not a verdict, and the court said so. **Finding that there is an adhesion contract is the beginning point for analysis, not the end of it. What courts aim at doing is distinguishing good adhesion contracts which should be enforced from bad adhesion contracts which should not.**"*

**(1) 逐語照合 — 正確である。**
原文は `episodes/_planning/measurements/EP65_brown_remand_RAW.md` 80行目：

> *As we recognized in State ex rel. Dunlap v. Berger, "[f]inding that there is an adhesion contract is the beginning point for analysis, not the end of it; **what courts aim at doing is distinguishing good adhesion contracts which should be enforced from bad adhesion contracts which should not**."*

台本との差は二つだけで、どちらも語を変えていない。
① *"[f]inding"* → *"Finding"*（引用開始のブラケット外し・標準的処理）。
② 原文のセミコロン → ピリオド＋ *"What"* の大文字化（**音読のための分割**）。
**語の追加・削除・並べ替えはゼロ。正確な引用である。**

*（一点だけ帰属の注記：原文では Brown II が* State ex rel. Dunlap v. Berger *を引用した「引用の中の引用」である。
台本は *"the court said so"* とだけ言い、Dunlap を出さない。判断としては正しい（人名を増やさない）が、
これは F-17 と同じ種類の帰属の粗さである。*"—an older case, quoted back"* 相当の3語で解消できる。）*

**(2) 実測 — 39語。**（18語＋21語。依頼文の「38語」との差1は *"[f]inding"* の数え方による。）
176wpm で **13.3秒**。後半文は21語・内部コンマ無しで **7.2秒を一息**。

**(3) 裁定：逐語のまま残す。省略記号での短縮はしない。**

理由は、内部反復が**欠陥ではなく、この文が耳に残る唯一の理由**だからである。

> *"distinguishing **good** adhesion contracts **which should be enforced** / from **bad** adhesion contracts **which should not**"*

左右の腕が **6語ずつで完全に対称**である。対句反復は、聴者が予測できるために**最も聞き取りやすい構造**であり、
これは v001 が「最悪」と判定した L306 の39語（左右が非対称で、間が書かれていなかった）とは**逆の性質**を持つ。
省略記号で削れば *"distinguishing good adhesion contracts … from bad"* となり、**短くならないうえに対句が壊れる。**

**推奨する唯一の手当（語を変えない）：** *"from"* の前にコンマを一つ置く
（*"…which should be enforced, from bad adhesion contracts which should not."*）。
軸語 *"from"* は無強勢で、そこが対句の折り返し点である。**±0語。**

**ただし、この一文の本当の問題は文そのものではなく位置である。**
L144 は 608.7s→626.4s、つまり **§5-B が不合格にした109秒の抽象帯の、すぐ延長線上**にある。
L144 単体は原典の力で持つが、**その前の 320語が空気になっているために、この引用も空気の中で鳴る。**
直すべきは L144 ではなく L130–L140 である。

---

## 8. ENDING の検証（依頼事項）

**判定：再フレームになっている。新事実ゼロ。**

ENDING は L343–L370（1,623.2s→1,761.0s・**404語・137.7秒**）。全節を既出情報と突き合わせた。

| 行 | 内容 | 既出か | 初出位置 |
|---|---|---|---|
| L345 | *"So what was the paper?"* | 問い | — |
| L347 | 家族の署名／extensive nursing care／carve-out／filing fee／三件目は例外なし | **全部既出** | L64 / L78 / L82 / L88 |
| L349 | *"a written provision in a contract evidencing a transaction involving commerce"* ／ 1925年 | **既出** | L190 / L96・L168 |
| L351 | *"It did not decide the paper was good."* | **再フレーム**（L248 の言い直し） | L248 |
| L353 | §2 の両半分／*"The savings clause was there the whole time."* | **既出＋回収** | L190・L192・**L194 の予告を14分越しに回収** |
| L355 | 州が一点だけ譲り、残りを保持 | **既出** | L276 / L284 / L294 |
| L357 | *"Three families sued. Three papers were signed."* ／ どの主権の法が及ぶかだけが決まった | **既出** | L38 / L64 / L248 |
| L359 | 未解決の二つの問い | **既出** | L313（unconscionability 未適用）／L329・L331（署名権限） |
| L361 | 二つの問いに対する Brown II の処分 | **既出**（原文照合済・Brown II 12行目） | L333 |
| L365 | carve-out の再掲・*"as the two papers wrote it"* | **既出・帰属付き** | L18 / L78 |

**新事実は無い。**「92%以降に新事実を置かない」（[MUST]）は満たされている。

**再フレームとして機能しているか — している。**
標準 §12 の「✓ 既出の事実が**別の意味に見える**ようにする」に対して、ENDING がやっているのは：
① 紙を**もう一度、記録の言葉だけで描き直す**（L347）→ ② *"It decided the paper was covered by the statute. It did not decide the paper was good."*（L349–L351）で
**同じ紙の意味を反転**させ → ③ L194 で植えた savings clause を **L353 で払う** → ④ 三年の訴訟の成果を
*"which sovereign's law applied to those papers, and almost nothing about whether they were fair"*（L357）に**再評価**する。
**「出来事の要約」ではない。**v001 が指摘した欠陥3は実質的に解消している。

**残る形の不良は一つだけ：**
**L361（69語・98.2%→99.5%）が、L333（91.7%）で既に述べた Brown II の処分をもう一度述べている。**
事実としては正しく、新事実でもない（F-10 PASS）。しかし**映画の最後の33秒のうち23.5秒を処分の再説明が占める。**
v001 が指摘した序数の交錯（第一→第三→第二）と46語の一文は**両方とも直った**（現在は「第一の問い／マルキオの件／第二の問い」で系統が一本、
最長文は約30語、**ENDING に40語超は0件**）。残っているのは長さではなく**重複**である。
L359 が二つの問いを立てているので、L361 は *"Neither had been answered."* ＋ 各問い1文（合計 ~35語）で足りる。**−34語。**

---

## 9. VERDICT

> # **DOES NOT MEET IT — R1〜R14 のうち 3項目が不合格（R6 / R11 / R14）＋ §8 が1箇所不合格。R15 は未実施。**

**v001 の PASS 10 / FAIL 5 から、PASS 11 / FAIL 3 へ。改善は本物であり、しかも v001 の判定は
「過小」でも「過大」でもなく、両方だった。**

- **過小に評価していた点：**R2 と R3 は完全に解消している。v001 が「形式的遵守・実質的不履行」と断じた
  L353 も含め、**6本の宣言文はすべて実際に消えており、置き換えは事実文である。**
  v001 が VERDICT に並べた7つの理由のうち **6つが解消**しており、そのうち3つ（R222/R223 の発注、
  手の縦糸4回、L317↔L323 の隣接化）は**発注書と原文を実物で確認して解消を確認した。**
  事実面では、原文と突き合わせた30箇所以上に**新しい誤りは1件も無い。**
- **過大に評価していた点はない。むしろ v001 が見ていなかった不良を2件見つけた** ——
  **F-17（ACT_2 の日付帰属）** と **F-16（L130–L140 の抽象帯）** である。後者は依頼どおり実測して確認した。

**水準に達していない理由は、次の4件である。すべて狭く、すべて安い。**

1. **状態1のプレート R152 に罫線が無い**（F-06 / F-11）。この映画唯一のモチーフが、ループの開く側に写らない。
2. **L317 の一文が、原告の主張を語り手の認定にしている**（F-14a）。§13 が名指しで禁じた形。
3. **L130–L140 の109秒に硬い事実が0個**（F-16）。§8 の下限を割り、§2 の離脱点条件（説明3連続）を倍で満たす。
4. **L132/L134 が Brown II（2012）の地の文を Brown One（2011）の発言として枠付けている**（F-17）。

### 手を入れる順序（全部を一括で当てる · `feedback_no_wasted_cycles`）

| 優先 | 作業 | 対象 | 語数 | 新規プレート |
|---:|---|---|---:|---:|
| **1** | **L36 の画指定を `R152` から `R222` に振り替え、L62 のプラントと統合する。**`R152`（手が束を揃える）は「手の一回目」としてその位置に残す | L36 / L62 | **0** | **0** |
| **2** | **L317 の第3文を書き換える。** *"There was no evidence to weigh, because nobody had been permitted to take any."* → ***"There was no evidence to weigh. The record had never been developed."***（*development of a record* は Brown II 自身の語）。同文の *"had never comprehensively analysed"* は *"had not had the opportunity to analyse comprehensively"*（原文どおり）に戻す | L317 | **+2** | 0 |
| **3** | **L130–L140 を具体に着地させる**（§5-B）。(あ) L140 の直後に三枚の紙へ15語以内で戻す ／ (い) L136 の *"That is unconscionability."* の直後に L82 の手数料条項を1文で置く ／ (う) `R036`/`R037` を画に入れる（**発注済**） ／ (え) L138–L140 のあいだに5語以下の一文を挟む。同時に L136/L138 の重複説明を削る | L130–L140 | **±0** | **0** |
| **4** | **L132 の枠付けを直す。** *"…that would matter a year later"* を外し、Brown I 引用（fn20/fn21 の2文）と Brown II 自身の2文を**言い分ける**。最小案：L134 の頭を *"The court would put it this way the next year:"* にして、L134 を Brown II の声として鳴らす | L132 / L134 | **+6** | 0 |
| 5 | **L304（sliding scale・60語）を落とす。**認知（L306→L308→L311）が締まる | L304 | **−60** | 0 |
| 6 | **L361 を L359 の二つの問いに一対一で対応させる** | L361 | **−34** | 0 |
| 7 | **L258 後半を落とす。** *"…and the document does not say which Justices stood behind it."* | L258 | **−7** | 0 |
| 8 | **L144 の *"from"* の前にコンマを置く**（語は変えない） | L144 | ±0 | 0 |
| 9 | **机をナレーションから外す**（L134 *"that desk"* → *"One side of the counter"* 等／L347 *"at an admission desk"* → *"at admission"*） | L134 / L347 | −2 | 0 |
| 10 | `alternative holding` の5回のうち1回を *"there"* に落とす | L232 or L234 | −4 | 0 |
| **11** | **発注書 `EP65_marmet_CODEX_BATCH_A.v001.md` を台本に合わせて改訂する** — L150 の R001 回収先（旧ループ）・L153 の R004 の意味と回収先（椅子）・L658 のループ表・L130 の HOOK 5枚 | 発注書 | — | 0 |
| **12** | **`mandatory_stills` を v002 の実測語数で再導出する**（ACT_5 が +11.2% 過小配分・§4-D） | spec / 発注書 | — | — |
| 13 | **通しで音読し、読了を記録する**（R15） | — | — | — |
| 14 | 収録後に L333 の終端位置を再測定する（92%線まで **6.1秒**しかない） | — | — | — |

**語数への影響：5,167 → 約 5,068。契約帯の下限 5,100 を 32語割る。**
不足分は **§6 で指摘した引用の終端合図**（「州最高裁はそこで止めた」型の短い帰属句）で埋めるのが正しい。
**説明では埋めない。帰属で埋める。**——それは同時に ⛔-04 の音声上の穴も塞ぐ。

---

*v002 · 2026-08-04 · 実測は `scratchpad\ep65_v2_measure.py`。原文照合は
`episodes/_planning/measurements/EP65_marmet_RAW.md`（全179行を読了）と
`episodes/_planning/measurements/EP65_brown_remand_RAW.md`、プレート照合は
`episodes/_planning/EP65_marmet_CODEX_BATCH_A.v001.md` の実プロンプトに対して直接おこなった。
**音読（R15）は実施していない。§6 は代替であって履行ではない。**
台本は一文字も編集していない。*
