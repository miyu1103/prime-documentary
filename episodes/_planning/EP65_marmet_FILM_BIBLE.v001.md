# EP65 · MARMET HEALTH CARE CENTER v. BROWN — FILM BIBLE v001

**Standard:** `docs/PD_SCREENPLAY_STANDARD.v001.md`（BINDING・2026-08-04）· `PD_ONE_PASS_PRODUCTION_SPEC.v2` 行15
**Case:** *Marmet Health Care Center, Inc. v. Brown*, 565 U. S. 530 (2012) (per curiam) · remand *Brown ex rel. Brown v. Genesis Healthcare Corp.*（Brown II）, 229 W. Va. 382 (2012)
**Facts:** `EP65_marmet_FACTS_LEDGER.v001.md` · `measurements/EP65_brown_remand_RAW.md` · contract `episodes/PD-2026-065-marmet/episode_spec.v001.json`
**Runtime:** 27:00–32:00（spec `runtime_seconds` [1620,1920]）· ナレーション 5,100–5,600語

> この文書は「何を語るか」ではなく「**なぜこの順で、この距離から語るか**」を決める。台本はこれに従属する。
> 事実は台帳が持つ。**ドラマは事実の上に組む。作らない。**

---

## 0. 順序が逆になっている（先に記録しておく）

標準（§17）の工程はこうである。

```
FACTS_LEDGER → FILM_BIBLE → SCRIPT 一周目 → 機械ゲート → §16人間レビュー → SCRIPT 二周目 → HOOK
```

**EP65はこの順で作られていない。** 台帳の次に台本が書かれ、機械ゲートを全部緑で通り、
そのあとでこの設計書が書かれている。標準はこの事態をあらかじめ名指ししている——
「**FILM_BIBLE 無しに台本を書き始めない。書けてしまうが、それは「正確」止まりになる。**」

実測した台本は 5,460語（8区分・369文）。事実の誤りは見つからない。時系列は通っている。
機械ゲートが測る範囲では欠陥がない。**つまり「正確」には届いている。**
そして §19 のレビューは 15項目中 11項目で不合格になる。標準が予告したとおりの結果である。

したがってこの設計書の位置づけは二つある。

1. **§1–§13 は、二周目の台本が従う設計である。**既存台本の追認ではない。
2. **§19 は、既存台本に対する不合格リストである。**該当箇所・削るもの・置き換えるものを一つずつ指定する。

この逆転自体は事故として記録するが、取り戻せる。**一周目が「正確」であることは、二周目を書く土台として悪くない。**

---

## 1. CONTROLLING IDEA（この映画が持つ唯一の思想）

> **署名は、署名した人ではなく、署名させた側の設計を実行する。**

一行で言えるまで削った。この文は**映画の中で一度も口に出さない**。全編がこれを実演する。

なぜこの一文なのか。**証拠は文書の中に既にある。**

契約は、あらゆる紛争を私的な仲裁人に送る。例外は一つだけである——
*"claims to collect late payments owed by the patient."*
裁判所に残された唯一の請求は、施設が自分で起こす請求だった。

この一行が示しているのは、施設の悪意ではない。**設計である。**
その紙は、署名する側が何を必要とするかではなく、**書いた側が将来何を持ち出したいか**で組み立てられている。
署名欄に一筆が入った瞬間、実行されるのはその設計であって、署名した人の意思ではない。

否定テストを通す。「署名は署名した人の意思を実行する」——この否定文に対して、
本編の全区間が反論として機能する。三年の訴訟が決めたのは**どの主権の法が紙に及ぶか**だけであり、
紙が公正かどうかは一度も審理されなかった。署名した人の意思は、最初から議題ではない。

副題として機能する対句：**紙は署名される前に完成している。**

---

## 2. THE PROBLEM THIS FILM HAS, AND WHY IT IS THE FILM

**この映画には、人間の材料がほとんど無い。**PD史上でも最も少ない。

判決文が三人の患者について書くのは、二文だけである。

> *"In each case, a family member of a patient requiring extensive nursing care had signed an agreement with a nursing home on behalf of the patient."*
> *"In each of the three cases, a family member of a patient who had died sued the nursing home in state court, alleging that negligence caused injuries or harm resulting in death."*

年齢が無い。病名が無い。入所日も、死亡日も、看護の内容も、過失とされた行為も無い。
患者の名前は一つしか出てこない——**Pauline Virginia Willett**——それも、キャプションの中だけである。
Brown の患者は無名。Taylor の患者は無名。

そして**署名した人が患者の何であったかは、一行も書かれていない。**
判決文が使う語は四語だけである。*a family member.*
署名した人と後に訴えた人が同一人物かどうかさえ、書いていない。

**したがって contract の `forbidden_claims` にある禁止は、単なる安全策ではなく作劇の前提である。**

> *"Framing the episode around 'your mother'. The opinion never uses the word mother and records no relationships."*

「あなたが預けた親」という枠は、**記録が支えない。使えない。**
これは制約であり、同時に**この映画の主題そのもの**である。

### 欠落を埋めない。欠落を主題にする。

> **この映画では誰も描写されない。彼らが署名した紙も、彼らを描写していなかったからだ。**

admission agreement は、署名する人が誰であるかを問わない。
続柄も、権限も、その日の状態も、書式は要求していない。必要なのは罫線の上の一筆だけである。
判決文が四語で済ませたのは、**紙が四語しか要求していなかったから**である。形式が内容と一致する。

だから：

| 役 | 何を置くか | EP65 |
|---|---|---|
| **主人公** | 状態が変化する**物** | **署名欄の罫線**（空 → 一筆 → 綴じられる → また空） |
| **敵対者** | 誰も検証しない**仮定** | 「**読んで、理解して、署名した**」 |
| **人間の縦糸** | 制度を実行する一人（悪人にしない） | **机の向こう側の手**。毎営業日これをする側 |

**敵対者の仮定は、こちらが言葉にしなくてよい。**州最高裁が先に名指ししている。

> *"It may be disingenuous for a nursing home to later assert that the patient or family member consciously, knowingly and deliberately accepted an arbitration clause in the contract..."*

**人間の縦糸に顔を与えない。**contract は staff の描写を明示的に禁じている
（`forbidden_subjects`：*any named or characterised member of staff at Marmet or Clarksburg*）。
この人物は手だけである。名前は無い。台詞は無い。性格づけは無い。悪意も無い。
Brown II が書いたとおり、*"Nursing homes daily sign contracts with patients as a routine course of doing business."*
——**それが仕事だった。それでも紙はああいう形をしていた。**悲劇は道徳ではなく設計にある。

---

## 3. MOTIF — 罫線の七つの状態

モチーフは**一つ**。**署名欄の罫線**。台詞で説明しない。登場順に固定する。

| # | 状態 | 出る場所 | 言わない意味 |
|---|---|---|---|
| 1 | 印刷されたばかりの空の罫線。用紙は束で積まれている | HOOK 冒頭 | 紙は、署名される前に完成している |
| 2 | 罫線の上で止まったペン先。まだ触れていない | ACT_1 前半 | ここで選べることは一つしかない |
| 3 | 読めない一筆。名前の形をしていない | ACT_1 中盤（*a family member* の四語） | 誰が書いたかは、紙に残らない |
| 4 | 同じ書式の罫線が二枚。三枚目だけ、罫線の上の文言が違う | ACT_1 後半（Marchio の紙） | 三家族・二種類の紙 |
| 5 | インクが乾き、紙が閉じられ、ファイルの背に入る | ACT_2 冒頭／18:00 の reset beat で再提示 | 手続きは完了した |
| 6 | 綴じられた記録の中で、その一行だけが残っている。周囲は空白 | ACT_4（five pages） | 二つの最高裁が三年扱ったのは、この一行だけ |
| 7 | 空の罫線に戻る。机の上、二脚目の椅子は空 | ENDING 最終画 | 次の一枚は、もう印刷されている |

**マクロ・ループ**：状態1で始まり、状態7で終わる。**画は同じ。意味が反転する。**
一周目の空の罫線は「まだ書かれていない」。二周目の空の罫線は「**もう決まっている**」。

**プラント → ペイオフ：二脚目の椅子。**
ACT_1（約4:30）で机に椅子が二脚あることを一度だけ見せる。片方は空である。
ENDING（約30:30）でその椅子に戻る。**その紙が扱っている人は、その席に座らなかった。**
根拠は台帳 MB-07 の四語——*on behalf of the patient*——だけ。ナレーションは椅子に一言も触れない。
プラントとペイオフの距離は約26分。標準の「2分以上」を大きく満たす。

**規則**
- モチーフは罫線**一つ**。ペンも椅子も紙束もモチーフではなく、罫線の状態を構成する要素・または一度きりのプラントである。
- 罫線の上の文字は**読めない**。読める文字はcontractが禁じている（`forbidden_subjects`）。
- 例外条項のテロップ（`【OST】`）はモチーフではない。**文字は文字、画は画。**二本立てにしない。

---

## 4. ARC — 五幕の中の三幕

| 幕 | 劇作上の役割 | 起きること | 距離 |
|---|---|---|---|
| HOOK | 約束 | 空の罫線／一筆／例外条項の一行 | 寄り |
| OP | 契約 | 五ページの per curiam。ここに人はいない | 引き |
| **ACT_1** | **設定** | 三つの事件・二種類の紙・例外条項・州法の一文。**制度は整って見える** | 引き→中 |
| **ACT_2** | 設定の崩壊 | 州最高裁が**自州の保護を先に潰す**。そのうえで別の道を作る | 中 |
| **ACT_3** | 対立の最大化 | *tendentious*／*created from whole cloth* → ワシントンの反撃。**相手側が最強の形で勝つ** | 中→寄り |
| **ACT_4** | **転回** | *Vacated.* 勝ちではない。Part II が一ページある | 寄り→中 |
| **ACT_5** | **認知 → 判断 → 限界** | 州が一点だけ譲る／*a modicum of bilaterality*／**誰も証拠を取っていない** | 中 |
| ENDING | 余韻 | 新事実ゼロ。空の罫線と、空いたままの椅子 | 引き |

**賭け金は縦（深さ）に上げる。**記録は横（被害の大きさ）を支えない。

**一枚の紙 → 三つの事件 → 州のカテゴリ全部 → 連邦と州の関係（Supremacy Clause） → §2 の後半（留保条項） → 仮定そのもの。**

最後の段——「読んで、理解して、署名した」という仮定——**が最深部である。**
そこに一度も証拠が入らなかったことが ACT_5 で判明する。それが §5 の認知になる。

---

## 5. TURN と RECOGNITION（一つずつ・置く場所を動かさない）

### TURN（転回・ペリペテイア）— ACT_3 末尾から ACT_4 冒頭 · 約 17:55–18:20

**逆方向に十分進んでから折り返す。**

ACT_3 では**施設側が完全に勝つ**。しかも正当に勝つ。
条文に例外は無い（*"The statute's text includes no exception for personal-injury or wrongful-death claims."*）。
先例が答えを機械的にする（*"the analysis is straightforward: The conflicting rule is displaced by the FAA."*）。
そして四語——***"That rule resolves these cases."***
同型の州法が負けた事件が四つ並ぶ。**観客はここで終わったと思う。**

そして——

> ***"The decision of the State Supreme Court of Appeals must be vacated."***

**Vacated.** 判決を消して差し戻す語である。**勝ち負けを決める語ではない。**
最高裁は Part II を一ページ書き、**自分が何を決めなかったかを列挙した。**

この順序を崩さない。**弱い反論を倒す映画は弱い。**FAA の議論は本当に強く、最高裁は本当にそれを認めた。
それを最強の形で通してから折り返すことが、この映画の説得力の全部である。

### RECOGNITION（認知・アナグノリシス）— ACT_5 · 約 25:20–25:50

**一箇所だけ。**登場人物ではなく観客の中で起きる。

州最高裁が Brown II で保持した契約法の中に、この一文がある。

> ***"Substantive unconscionability may manifest itself in the form of 'an agreement requiring arbitration only for the claims of the weaker party but a choice of forums for the claims of the stronger party.'"***
> ***"Agreements to arbitrate must contain at least 'a modicum of bilaterality' to avoid unconscionability."***

そのすぐ後に、ACT_1 で一度だけ引いた条項が画で戻る（モチーフ状態3の再掲・テロップ）。

> ***"...all disputes, other than claims to collect late payments owed by the patient."***

**ここで観客が自分で到達する結論はこうである。**
「その紙の一行目から見えていたものには、法律上の名前がずっとあった。
そして誰も、その名前をその条項に当てなかった。三年かけて、二つの最高裁を通って、**証拠が一度も取られなかったから**。」

**語り手はこれを言わない。**引用二つと画一つで足りる。

**認知の直後に沈黙（⟨HELD⟩）。**そこからENDINGまでが落下である。

**二つ置かない。**ACT_2 の「州が自州の保護を先に潰した」は**期待の裏切り**であって認知ではない。
ACT_4 の「vacated は valid ではない」は**転回**であって認知ではない。
どちらも ⟨HELD⟩ を与えず、宣言的な語り（「ここが本作の核心だ」式）を一切付けない。**認知は一箇所。**

---

## 6. THE REFUSALS（この映画が撮らないもの）

contract の `forbidden_subjects` は機械が読む。**ここに書くのは、それがなぜ作品を良くするか**である。

| 撮らない | 理由 |
|---|---|
| 患者・傷害・死・看護の描写 | 記録に一行も無い（○-01）。描いた瞬間に創作になる。**無いことがこの映画の主題である** |
| 施設の職員（名前・性格・顔） | 悪役を作った瞬間、話が「悪い人がいた」に縮む。**記録に悪意は無い** |
| 病室・ベッド・人工呼吸器・臨床の場面 | 感情を**紙**から奪う。この映画の緊張は罫線にあり、病室にない |
| 実在の施設・建物と分かる外観／看板 | 名指しは事実として過剰であり、劇としても不要 |
| 法廷内観・木槌・判事席 | 24本中23本を過去話で使い切っている。**そしてこの事件の核心は法廷に入る前に決まっている** |
| 監房・鉄格子・手錠 | 在庫も枯れており、**この映画は収監の話ではない** |
| 読める文字・数字・ロゴ・印章 | 本物の契約書は映せない。**読めない紙のほうが強い**——中身ではなく、誰の設計かが主題だから |
| 肩に置く手・涙・秒読みの時計 | 同情の演出は一つも要らない。**記録が支えるのは書式だけである** |
| 「あなたの母親」「あなたが預けた親」 | 続柄が記録に無い（MB-10）。禁止であり、かつ**設計上不要**——罫線が二人称より強い |

---

## 7. REGISTER — 声の設計

**観客の実測**：93%男性・91%が55歳以上。**制度と権力の観客**である。真犯人当ての観客ではない。

- **判決記録の平明さ。**修飾を削る。形容詞は事実が持つものだけ。
- **感情命令ゼロ。**「想像してみてください」「衝撃的なことに」は一つも書かない。
- **語り手は結論を言わない。**例外条項は**平叙で一度言い、形容詞を付けない**。
  ✓ *"A dispute about how somebody died goes to a private arbitrator. A dispute about an unpaid bill stays in a courthouse."*
  ✗ 「その紙は、施設が自分のために法廷を取っておいた紙だった」——観客の仕事を奪う。
- **他人の語り直しに反論しない。**「多くの解説はここを間違える」「よく誤解されるが」は**すべて削る**。
  それは解説者の口調であり、この映画の語り手は解説者ではない。**正しいことだけ言えば、間違いは勝手に消える。**
- **最良の台詞は既に書かれている。**そのまま鳴らす：
  *"greatly at sea without a chart or compass."* / *"a modicum of bilaterality."* / *"disingenuous."*
- **短文を武器に使う。**30語超の助走を5語以下で切る。「*Vacated.*」「*Summarily.*」「*A panacea.*」

**実測の運用目標**（一周目の実測値・二周目もこの帯を守る）

| 指標 | 標準 | EP65 一周目 実測 |
|---|---|---|
| 短文（6語以下）比率 | 20–35% | **25.5%**（94/369） |
| 修辞疑問 | ≤2 / 1000語 | **0.18**（全1回） |
| 二人称 | ≤8 / 1000語 | **0.18**（全1回） |
| 30語超の助走→5語以下で切る | 各幕に最低1 | ACT_1..5 すべて有り |

**リズムは既に合っている。壊さずに二周目を書く。**

**沈黙（⟨HELD⟩）は三箇所だけ。**（§11）
1. **認知の直後**（*a modicum of bilaterality* → 例外条項 の直後）
2. **限界の直後**（「この判決文は条項を無効と言っていない」の直後）
3. **最終画の前**（空の罫線に戻る直前）

**⟨HELD⟩ を「これから重い一文が来る」という予告に使わない。**沈黙は前の一文が重いときだけ効く。

---

## 8. RETENTION MAP（再フックの位置）

実測：半減42秒・離脱の山は80〜180秒。**戦争は冒頭で決まる。**最大間隔150秒以内。

| 位置 | 仕掛け |
|---|---|
| 0:00 | HOOK（§9・**最後に書く**） |
| 1:20 | 「五ページ。この三家族について知りたいことは、ほとんど書かれていない」——欠落の提示 |
| 2:40 | Brown を却下した命令は**一段落**しかない |
| 4:00 | **例外条項**。平叙で一度。形容詞なし |
| 5:30 | 三枚目の紙には例外が無い（Marchio）——「三人は同じ紙に署名していない」 |
| 7:40 | **州最高裁が自州の保護を先に潰す**（期待の裏切り。認知ではない） |
| 10:20 | *disingenuous* ——州最高裁が、これから来る主張を先回りで名指しする |
| 13:00 | *tendentious* / *created from whole cloth* |
| 15:40 | *"That rule resolves these cases."* ——四語 |
| 17:00 | *Preempted. Preempted. Preempted. Preempted.* |
| **18:00** | **転回**：*Vacated.* ＋ reset beat（モチーフ状態5・無音4秒） |
| 20:30 | 最高裁が**決めなかったこと**の列挙（Part II） |
| 23:00 | 州最高裁が一点だけ譲る：*"we overrule Syllabus Point 21"* |
| **25:30** | **認知**：*a modicum of bilaterality* → 例外条項 ⟨HELD⟩ |
| 27:00 | **限界**：誰も証拠を取っていない。処分は三件で同じではない ⟨HELD⟩ |
| 28:30 | ENDING（新事実ゼロ・再フレームのみ） |

---

## 9. HOOK 設計（**最後に書く**）

**構造**：3〜4カット、各約2秒。本編で最も強い画。1本の台詞。開いた問い。

| フックのカット | 回収先 |
|---|---|
| 空の罫線（モチーフ状態1） | ENDING 最終画（状態7・同じ画・意味が反転） |
| 罫線の上の、読めない一筆 | ACT_1（*a family member* の四語） |
| 【OST】例外条項の一行 | ACT_5 の認知 |

**台詞は説明しない。**問いだけ残す。例外条項は**引用で置き、解釈を付けない。**

### ⚠️ 未解決の契約衝突（二周目の前にオーナー判断が要る）

- `PD_ONE_PASS_PRODUCTION_SPEC.v2` 行9（BINDING）：**HOOK は 0:00〜約0:08**、受入ゲート `hook_added` は **6〜10秒**。
- 一周目の台本：`## HOOK (0:00-0:57)`・**169語**（実測 ≈57秒）。

**このまま組むと受入ゲートで落ちる。**二周目に入る前に、次のどちらかを owner が決める必要がある。

- (a) **v2 準拠**：HOOK を 8秒に切り、いまの57秒ぶんは OP の前の cold-open として別区分に置く
  → ただし `section_vocabulary` は8キー固定なので、区分の増設は spec 改訂を伴う。
- (b) **偏差承認（APR）**：EP65 は 57秒の HOOK で行くと明記し、受入ゲートの当該項目を承認済み偏差として記録する。

**この設計書は勝手にどちらも選ばない。**選んだ側を APR に記録してから二周目を書く。

---

## 10. WHAT THE IMAGES MUST CARRY

語りが説明を降りる代わりに、画が論証を持つ。Codex 発注書（`EP65_marmet_CODEX_BATCH_A.v001.md`・219点）はこの節に従属する。
※ 台本を改訂したら `mandatory_stills` を**必ず再導出する**（spec `notes` の明示指示）。

- **同じ罫線を、違う状態で繰り返す。**画の反復が、書式の反復（毎営業日おこなわれること）を同時に言う。
- **人は後ろ姿・手・影のみ。**顔が出た瞬間、観客は「その人の物語」を探し始める。**この映画にそれは無い。**
- **institutional な空虚**：誰もいない受付、空の椅子、積まれた用紙、閉じたファイルの背。制度は人がいなくても動く。
- **手の仕事**：ペン、書式を回す手、クリップ、ファイルの背。**制度は手で実行される。**
- **文字は読めない。**罫線は読める。**その対比が主題である。**
- **既存棚の使い方**（2026-08-04 実測）：elderly 104点(burn 5/24)・wheelchair 43(4/24)・elevator 62(4/24)・curtain 149(2/24)。
  **法曹ジャンルの棚は使わない**（courtroom 23/24、cell 20/24、prison 18/24 が消費済み）。

---

## 11. THE LINE THE FILM IS BUILT ON

> ***"On remand, the West Virginia court must consider whether, absent that general public policy, the arbitration clauses in Brown's case and Taylor's case are unenforceable under state common law principles that are not specific to arbitration and pre-empted by the FAA."***
> — MB-49 / 原文照合済み

**この一文に向かって全部が動く。**そしてこの一文の意味は、「まだ誰も答えていない」である。

もう一本、映画を開く一行：

> ***"...a clause requiring the parties to arbitrate all disputes, other than claims to collect late payments owed by the patient."***
> — MB-23 / 原文照合済み

**MB-25 が冒頭、MB-49 が結末。**台帳が既にそう書いている。

---

## 12. WHAT THIS FILM IS NOT ALLOWED TO SAY

contract の `forbidden_claims` と台帳の ⛔ 全項目がここに拘束する。とくに：

- **「最高裁は条項を有効と判断した」と言わない。**判断していない。vacate して差し戻しただけである（⛔-01）。
- **「家族は仲裁に送られた」と言わない。**最高裁は誰にも仲裁を命じていない。
- **per curiam を「全員一致」と言わない。**著者名も票も記録されていない（⛔-10）。
- **三家族を混ぜない。**Marchio の紙は例外条項も手数料条項も無い、別の紙である（⛔-05）。
- **統計を一つも出さない。**この判決文に該当する数字は一つも無い（⛔-03）。
- **署名の法的効力について断定しない。**「相続人の権利を放棄させられるか」は**差し戻された未解決問題**である（⛔-09）。
- **州最高裁の理屈を映画の声にしない。**必ず帰属付き・過去形（⛔-04）。
- **処分を一本化しない。**35494 Brown＝reversed and remanded／35546 Taylor＝reversed and remanded／
  35636 Marchio＝**certified question answered**。**「三件とも差し戻された」は誤りである。**
- **その後どうなったかを語らない。**Brown II で記録は終わっている（⛔-06）。

**沈黙している記録に声を当てない。**それがこの映画の品位であり、同時にこの映画の主題でもある。

---
---

# 19. CRAFT REVIEW — 一周目台本が標準に届いていない箇所

対象：`episodes/_planning/EP65_marmet_script.en.v001.md`（実測 5,460語・369文・8区分）
適用：`PD_SCREENPLAY_STANDARD.v001.md` §16（R1〜R15）
機械ゲートは全緑。**以下は機械が測れない部分である。**

> **判定：15項目中 PASS 4 / FAIL 11。**
> 行番号は台本ファイルの行。引用は原文のまま（英語）。

---

### R1 — CONTROLLING IDEA を一文で言えるか → **PASS**

言える（§1）。**署名は、署名した人ではなく、署名させた側の設計を実行する。**
台本の中にもその実演は存在する。L348 が最も近い。

> *"A form that sent every dispute to a private arbitrator, except the single dispute the nursing home might want to bring itself."*

**ただし構造上の注記。**台本を18分間支配しているのは主題ではなく**法律上の訂正命題**である——
「vacated は valid ではない」。これは §2 の言う「出来事の説明」であって「出来事が何であったか」ではない。
主題は ENDING でようやく前に出る。R2/R3/R10 の不合格はすべてここから派生している。
**二周目は §1 の一文を全編の底に敷き、訂正命題は ACT_4 の転回に格下げする。**

---

### R2 — その一文は台本に**書かれていない**か → **FAIL**

例外条項が強すぎるため、語り手が繰り返し解釈してしまっている。**四箇所。**

**(a) L15（HOOK）**
> *"That is the entire exception. Everything went to a private arbitrator except one category of claim, and the category left in a courthouse belonged to the nursing home. Its own claim, for money."*

**削る**：`"and the category left in a courthouse belonged to the nursing home. Its own claim, for money."`
引用文にすでに *owed by the patient* と書いてある。誰が取り立てる側かは、観客が読める。
**置き換え**：引用のあと一拍空けて次へ。何も足さない。

**(b) L74（ACT_1）**
> *"Take that apart slowly. All disputes go to arbitration. One kind does not. The kind that does not is a claim to collect late payments owed by the patient — which is the nursing home's claim, against the patient's side of the table, for money."*

**段落ごと削る。**直後の L76 が完成形であり、この段落はその劣化版の前置きにすぎない。
**残す**：L72 の引用 → L76。
> *"A dispute about how somebody died goes to a private arbitrator. A dispute about an unpaid bill stays in a courthouse."*

**(c) L79**
> *"That is in the document. It is not a reading of the document."*

**削る。**語り手が自分の読みすぎを自分で弁護している。弁護が要るのは読みすぎたときだけである。
(b) を削れば、この一文の必要も消える。

**(d) L368（ENDING 最終行）**
> *"The nursing home kept a courthouse for the only claim it was ever likely to file."*

**削る。**二つ問題がある。①主題を語り手が言い切っている。②*"ever likely to file"* は記録にない予測である。
**置き換え**：L366 の引用（例外条項）で止め、画をモチーフ状態7に落として終わる。ナレーションは足さない。

**加えて L255。**
> *"Now the sentence this film exists to say."*

**削る。**語り手が自分の主題を予告している。§7 の抑制違反として最も重い一行。

---

### R3 — 語り手の結論文を全部削っても、観客は同じ結論に着くか → **FAIL**

着かない箇所がある以前に、**結論文の総量が多すぎる。**とくに一つの型が反復している。

**型①：他人の語り直しへの反論（5箇所）**
- L103 *"...and it is the one that gets left out of every retelling."*
- L218 *"Vacated is a precise word. This is where most accounts of this case go wrong."*
- L228 *"It is the half of the decision that vanishes in the retelling..."*
- L234 *"That is why the outcome of this case cannot be described in one sentence."*
- L267 *"One more thing is routinely got wrong."*

**全部削る。**これは解説者の口調である。映画が「他人の間違い」を相手にした瞬間、
観客は制度ではなく語り手の正しさを見せられる。**正しく語れば、誤解は勝手に消える。**
**置き換え**：L218 → *"To vacate a judgment is to wipe it out and send the case back."*（L224 を繰り上げ）だけ。

**型②：観客への指示（3箇所）**
- L74 *"Take that apart slowly."*（R2(b) で削除済）
- L128 *"Keep that distinction. The rest of this story is nothing but that distinction."*
- L195 *"Keep the second half. It comes back."*

**L128 は削る。**区別が効いているかどうかは、ACT_4 で自然に分かる。
**L195 は残してよい。**§2 の savings clause は ENDING で回収される実際の仕掛けであり、
「覚えておけ」ではなく「これは後で戻る」という短い予告として最短の形をしている（8語）。

**型③：意味の言い切り（2箇所）**
- L167 *"That is a state supreme court telling the Supreme Court of the United States that it invented the modern law of arbitration."* → **削る。**直前の *created from whole cloth* が既に言っている。
- L250 *"The line between those two sentences is the whole federal law of arbitration, compressed."* → **削る。**自賛。二文を並べれば足りる。

**残す（削ってはいけない）：L185。**
> *"Misreading and disregarding. Two words, and they are not the same accusation. One is error. The other is choice."*

これは結論ではなく**語彙の観察**であり、判決文自身の選語から出ている。この映画の質を上げている一節である。

---

### R4 — 認知は**一箇所**か → **FAIL**

**四つある。**⟨HELD⟩ が9個打たれており、そのうち少なくとも4つが「ここが核心」の顔をしている。

| 行 | 何を「核心」として提示しているか |
|---|---|
| L78–79 | 例外条項 |
| L109–110 | *"The state court struck down its own state's protection before it did anything else."* |
| L254–255 | *"Now the sentence this film exists to say."* → L257 の訂正命題 |
| L314–315 | 例外条項の再掲（**これが本来の認知**） |
| L339–340 | *"Nothing in that opinion holds these clauses unenforceable."* |

さらに L352 *"It did not decide the paper was good."* が ENDING で五度目の「実は」を出している。

**是正**
- **認知は L310–L315 の一箇所に確定する**（§5）。⟨HELD⟩ はその直後に置く。
- L78/L109/L166/L201/L254/L301 の ⟨HELD⟩ を**外す**。
- L339 の ⟨HELD⟩ は「限界の直後」（§11 位置2）として**残す**が、位置を L340 の**後**に移す。
- L255 は削除（R2）。L110 は宣言をやめ、事実だけにする：
  *"Nobody appealed that holding."*（L112 に既にある）で足りる。
- L352 は残してよいが、**ENDING で初出の「実は」にしない**——L257 の言い換えとして機能させ、
  新しい暴露の顔をさせない。

---

### R5 — 転回の前に、反対側を**最強の形で**述べたか → **PASS**

述べている。**この台本で最もよく出来ている部分である。**

- 州最高裁の第一判示が施設側に有利であること（L105–112）を先に出し、
  *"The picture of a state court simply defying Washington does not survive that."*
- §2 の条文（L191）、*"The statute's text includes no exception..."*（L197）、
  Concepcion（L199）、そして四つの先例（L206）。
- そして L208 *"Preempted. Preempted. Preempted. Preempted."*

**FAA の議論は本当に強く、最高裁は本当にそれを認めた。**台本はそれを弱めていない。
州最高裁の *tendentious* を**先に**置いて反撃の理由を与えている順序も正しい（L158–179）。
⛔-04（州の理屈を映画の声にしない）も守られている——帰属付き・過去形。

*（軽微：L158 "it is worth hearing how..." は司会の言い回し。"West Virginia had described Washington first." 程度に締めてよい。）*

---

### R6 — モチーフの状態変化を順に言えるか → **FAIL**

**言えない。台本に状態変化を持つ物が存在しない。**

台本に出る物体は三つだけである。
- L11 *"The kind that gets signed at a desk."*
- L132 *"One side of that desk..."*
- L216 `【reset beat: hold on the blank form, no narration, 4s】`

`blank form` が一度だけ出るが、**前にも後にも状態が無い。**単発の絵であって、論証を運んでいない。
現状モチーフの役を負っているのは**文字列**（`【OST: OTHER THAN CLAIMS TO COLLECT LATE PAYMENTS】`）であり、
§5 の「同じ物を、違う状態で、順番に見せる」を満たしていない。

**是正**：§3 の七状態を、以下の位置に**台本本文の指定として**入れる。

| 状態 | 挿入位置（現行行） |
|---|---|
| 1 空の罫線・用紙の束 | HOOK 冒頭（L11 の前） |
| 2 触れていないペン先 | L11 の直後 |
| 3 読めない一筆 | L65（*"The signature is described twice, in the same four words."*）に合わせる |
| 4 二枚は同じ書式・三枚目だけ違う | L85–87（Marchio の紙） |
| 5 乾いたインク・閉じられる | L216 の reset beat を**この状態に書き換える**（`blank form` ではなく `closing file`） |
| 6 記録の中に残る一行 | L228（*"Part Two is one page long."*）付近 |
| 7 空の罫線に戻る・空いた椅子 | L370 の最終画 |

**同時に**、ACT_1 に**二脚目の椅子**を一度だけプラントする（L60–L66 のあいだ、ナレーションなし）。

---

### R7 — 各主要人物に反復不能な細部があるか → **PASS**

十分にある。**カテゴリで済ませていない。**

- Brown：*"That order is one paragraph long."*(L46) / *"devoid of any findings of fact or conclusions of law"*(L319) / August 25, 2009
- Taylor：September 29, 2009 / *"had some findings of fact"* だが包括的分析はなし(L319)
- Marchio：*"executrix of the estate of Pauline Virginia Willett"* / June 2, 2010 / 認証質問 / **例外条項も手数料条項も無い紙**(L85)
- Willett：*"named only in the caption"*(L64) ——**細部そのものが「名前だけ」であることが細部になっている**
- 裁判所：*"Ketchum, Chief Justice"*(L283) / *"greatly at sea without a chart or compass"*(L321)
- 施設側の書式：AAA が 2003年1月1日以降 individual patients を受けない／NAF が
  *"Friday, July 24, 2009"* にミネソタ州司法長官との和解で消費者仲裁を停止(L329)
  ——**反復不能な細部として最良のもの。**

**署名した人にだけ細部が無いのは正しい。**それが §2 の設計である。
**追加禁止**：Brown II には *Robin Sutphin*（管理者）と *Canoe Hollow Properties, LLC* が出るが、
contract が staff の描写を禁じている。**二周目でも足さない。**

---

### R8 — 悪役を作っていないか → **FAIL**

個人は作っていない（spec 遵守・良い）。**しかし語り手の形容で法人の悪役を作っている。四箇所。**

**(a) L15** *"Its own claim, for money."* → R2(a) で削除。*for money* は嘲りである。
**(b) L74** *"against the patient's side of the table"* → R2(b) で段落ごと削除。「陣営」を作る語。
**(c) L132**
> *"One side of that desk does this every working day. The other side does it once, in the worst week of a family's life."*

前半は**残す**（Brown II の *"as a routine course of doing business"* に根拠がある）。
後半 *"in the worst week of a family's life"* は**削る**——記録に無い断定であり、
かつ対立構図を作っている（R14 とも重複）。
**置き換え**：*"The other side does it once."* で止める。**短いほうが強い。**

**(d) L368**（映画の最終行）
> *"The nursing home kept a courthouse for the only claim it was ever likely to file."*

**削る**（R2(d)）。**映画の最後の一文が施設に対する道徳判決になっている。**
§9 の言うとおり、誰かが悪いのならそれは小さい話である。
**置き換え**：引用（L366）＋モチーフ状態7。**判決は観客が下す。**

**残す**：L331 *"The forums named in the papers had stopped taking the kind of case the papers were sending them."*
——形容詞ゼロで、最も効いている一文。これが手本である。

---

### R9 — 賭け金は縦（深さ）に上がっているか → **PASS**

上がっている。

**一段落の命令(L46) → 三つの事件(L42) → 州内のあらゆる入所契約(L122) → Supremacy Clause(L212) → §2 後半の留保条項(L244)。**

横（被害の大きさ）に逃げていない。統計もゼロ（⛔-03 遵守）。

*（注記：最深部は §4 のとおり「読んで、理解して、署名した」という仮定である。
現行台本はそこまで降りず、教義（unconscionability）で止まっている。
二周目で認知（R4）を確定させれば、最後の一段は自動的に付く。修正指示は R4 に統合。）*

---

### R10 — ENDING に新事実がゼロか → **FAIL**

92%線 ≈ 28:32（実測語数からの推定尺 ≈31分）。ENDING は 28:20 開始なので**ほぼ全体が該当**する。**二件。**

**(a) L358**
> *"Just under three years of litigation, from the first dismissal in August 2009 to the last opinion in June 2012..."*

*"Just under three years"* は**この時点で初出の算出値**である。両端の日付は既出だが、期間は既出ではない。
**是正**：ACT_5 の処分（L337）の直前に *"Two years and ten months after the first dismissal."* として置き、
ENDING では算術をしない。または削る。

**(b) L362** — 新事実であり、かつ**誤り**（R13 参照）
> *"Both had been handed to a circuit judge in Kanawha County and a circuit judge in Harrison County, with instructions to take evidence this time."*

Brown II が証拠採取を命じたのは Brown と Taylor の巡回裁判所（Kanawha）である。
Harrison County には認証質問への回答が返り、unconscionability は**当事者が持ち出せる**とされただけで、
証拠採取の指示は出ていない。*"this time"* は記録に無い叱責のニュアンスを足している。
さらに Brown と Taylor は**別々の命令**であり、*"a circuit judge"* 単数はそれを一人に丸めている。
**置き換え**：*"Neither had been tried. Both were sent to circuit courts that had never taken a day of evidence on them."*
（郡名も単複も持ち出さない。処分の非一様性は L337 が既に正確に述べている。）

*（軽微：L360 *"when both reporters closed"* の "reporters"（判例集）は音で誤解される。"when both opinions closed" に。）*

---

### R11 — ENDING は最初の画に戻るか → **FAIL**

**言葉では戻っている。画では戻っていない。**

- 戻っている：`【OST: OTHER THAN CLAIMS TO COLLECT LATE PAYMENTS】`(L22) → `【OST: OTHER THAN】`(L370)
  ——**この文字のループは良い。二周目でも残す。**
- 戻っていない：§5 が要求するのは**モチーフの状態が最初に戻る**ことである。
  R6 のとおりモチーフが存在しないので、視覚のループも存在しない。

**是正**：R6 の状態1（HOOK 冒頭・空の罫線）と状態7（L370・空の罫線と空いた椅子）で**同一構図**を撮る。
文字のループはその上に重ねる。**二層になって初めて「意味だけが変わった」が成立する。**

---

### R12 — 沈黙の位置を三つ言えるか → **FAIL**

⟨HELD⟩ が**9個**（L19, 78, 109, 166, 201, 254, 301, 314, 339）。標準は三箇所（§11）。
数より悪いのは**使い方**である。**9個のうち8個が「次に重い一文が来る」予告**として直前に置かれている。

例：L201 の ⟨HELD⟩ の直後が *"That rule resolves these cases."*、
L254 の直後が *"Now the sentence this film exists to say."*。
**沈黙が太鼓の連打になっている。**§11 は逆を言う——沈黙は**重い一文の後**にだけ効く。

**是正**：⟨HELD⟩ を**三つに削る。すべて直後に置く。**
1. **認知の直後**：L315（例外条項の再掲）の後
2. **限界の直後**：L340（*"It hands the question to two circuit courts and stops."*）の後
3. **最終画の前**：L366（例外条項）と L370（最終画）のあいだ

残る6個は削除。L216 の `【reset beat ... 4s】` は沈黙ではなく画の休符なので、**残してよい**（内容は R6 に従い状態5へ）。

---

### R13 — 矛盾する記録を、矛盾のまま出したか → **FAIL**

**三つに分けて判定する。**

**(a) 処分の非一様性 — L337 は正しい。**
> *"Case number 35494, Brown: reversed and remanded. Case number 35546, Taylor: reversed and remanded. Case number 35636, Marchio: certified question answered..."*

spec の警告（*"THE DISPOSITION IS NOT UNIFORM — do not write 'all three were sent back'"*）を守っている。**ここは合格。**

**(b) しかし ENDING(L362) が 25行後にそれを平らにしている。** → R10(b) の是正で解消する。**この一点で R13 は不合格。**

**(c) Brown II 自身の自己矛盾を落としている。**
同じ意見が二つのことを言っている。

> *"we otherwise reaffirm all of our discussion and holdings in Brown I."*
> *"However, in light of the parties' additional briefs and arguments, we modify our conclusions in Brown I."*

**reaffirm しつつ modify している。**台本は L293 で reaffirm 側だけを引き、
修正のほうは L317–325 で「適用できなかった理由」として説明に均している。
§13 は「どちらかを選ばない」と命じる。
**是正**：L293 の直後に modify の一文を並置し、註釈を付けない。
**置き換え案**：*"We otherwise reaffirm all of our discussion and holdings in Brown I. And: we modify our conclusions in Brown I. Both sentences are in the same opinion."*
——それ以上何も言わない。

*（(d) 参考：条文の 15(c)/15(e) と docket 35636/35635 の揺れは OCR 由来の捕捉ノイズであり、
司法判断の矛盾ではない。spec の決定（15(c) と 35636 を採る）どおりでよい。
**二周目で誰かが「修正」しないよう、この判断を設計書側に固定しておく。**）*

---

### R14 — 記録の沈黙を、沈黙のまま扱ったか → **FAIL**

**この台本の最良の部分と最悪の部分が同居している。**

**最良（絶対に削らない）：L58–L66。**
> *"Now the part where the record stops."* … *"That is the whole account."* … *"No ages. No conditions. No dates of admission, no dates of death."* … *"Brown's patient is unnamed. Taylor's patient is unnamed."*

**これが §3 の解決の実演である。**PD の全話でも上位の一節。

**しかし三箇所で埋めている。**

**(a) L132** *"in the worst week of a family's life"* → **削る**（R8(c)）。家族の体験についての創作。

**(b) L140**
> *"Take it or leave it. On a day when leaving it is not really available."*

後半は語り手による事実主張になっている。**根拠はある**——Brown II 註20 の
*"people ... have to sign admission contracts without time to comparison shop"*——
が、それは**州最高裁の認定**であって語り手の観察ではない。
**置き換え**：帰属を付ける。*"Take it or leave it. The state court's phrase for that day was 'urgency, confusion, and stress.'"*

**(c) L68**
> *"That absence is not an oversight, and this film is not going to fill it. A five-page per curiam opinion is not a narrative."*

*"not an oversight"* は、**判決文が短い理由**を断定している。映画はそれを知らない。
また *"this film is not going to fill it"* はメタ発言であり、§7 の抑制に反する（自分の禁欲を宣言している）。
**置き換え**：段落を **"A five-page per curiam opinion is not a narrative."** の一文だけにする。
**沈黙を守っていることを、口に出して誇らない。**

**(d) L17（HOOK）**
> *"A judge in Kanawha County read the agreement and dismissed the case."*

*"read the agreement"* は記録に無い。むしろ L48/L319 が、その命令には認定も分析も無かったと述べており、
**映画が後で自分の冒頭を否定する形**になっている。
**置き換え**：*"A judge in Kanawha County dismissed the case in one paragraph."*
——事実だけで、しかも強い。

*（(e) 軽微：L11 *"The kind that gets signed at a desk."* の「机」も記録に無い。
ただしモチーフの導入として画に必要であり、**画で出して語らない**なら許容する。ナレーションからは落とす。）*

---

### R15 — 声に出して読んだか → **FAIL**

**読んだ形跡が無い。**（読了記録が無く、以下の三箇所は音読すれば必ず残らない。）

数値上のリズムは**合格帯にある**（§7 の実測表）。したがって不合格の根拠は指標ではなく、**音で壊れる具体箇所**である。

**(a) L40** — 同じ固有名詞を一文で二度、しかも6語の名称で。
> *"Marchio sued Clarksburg Nursing Home and Rehabilitation Center — in the Supreme Court's caption, Clarksburg Nursing Home and Rehabilitation Center, doing business as Clarksburg Continuous Care Center."*

音では言い直しか事故に聞こえる。
**置き換え**：*"Marchio sued a nursing home in Clarksburg. In the Supreme Court's caption it has two names — Clarksburg Nursing Home and Rehabilitation Center, doing business as Clarksburg Continuous Care Center."*

**(b) L337** — **五桁の番号が三つ連続する。**しかも三つ目に、コロンのあとダッシュ二重の挿入句が付く。
> *"Case number 35494, Brown: reversed and remanded. Case number 35546, Taylor: reversed and remanded. Case number 35636, Marchio: certified question answered — yes, ... — with unconscionability left to be raised by the parties on remand, because the trial court had never considered it."*

**この段落は R13 の合格点であり、音で失うわけにいかない。**
**置き換え**：番号を落とし、名前で三つ並べる。
*"Brown: reversed and remanded. Taylor: reversed and remanded. Marchio: the certified question answered. Yes — the Nursing Home Act's waiver ban is preempted. Unconscionability was left for the parties to raise, because the trial court had never reached it."*
（docket 番号を残す必要があるなら**画のテロップに置く。耳に置かない。**）

**(c) L105–L107** — 48語と45語の法文引用が**連続する**。音では壁になる。
**是正**：あいだに5語以下の一文を挟んで切る（§10 の「30語超を5語以下で切る」を、ここでは**二回連続の壁**に適用する）。
例：L105 の引用の後に *"That is the rule it wrote."* を挟み、L107 の適用文へ。

**手順**：二周目の完成後、**通しで音読し、読了を記録する。**§16 は「R15は省略しない」と明記している。

---

## 19.1 まとめ — 二周目が一度で通るための順序

**変更は一括で当てる。**（`feedback_no_wasted_cycles`：全 fail を出し切ってから一回で直す）

1. **R6/R11 が最重量**：モチーフ七状態と画のループを台本本文に入れる。他の修正は全部これに乗る。
2. **R2/R3/R8 は同じ削除作業**：語り手の結論・他人の語り直しへの反論・形容による悪役化を一掃する。**足す作業はほぼ無い。削るだけである。**
3. **R4/R12 は一つの作業**：⟨HELD⟩ を 9 → 3 に減らし、すべて「重い一文の後」に置き直す。認知は L310–315 に確定。
4. **R10/R13 は ENDING の一段落**：L358 と L362 を差し替える。L337 の正確さを ENDING で壊さない。
5. **R14 は四箇所の削除と帰属付け**：L132 後半・L140 後半・L68 前半・L17。
6. **R15 は最後**：通し音読。L40／L337／L105-107 を直してから読む。
7. **HOOK は最後に書く**（§9）。**その前に §9 の契約衝突（8秒 vs 57秒）を APR で決着させる。**
8. 台本が確定したら **`mandatory_stills` を再導出**する（spec `notes` の明示指示・219点）。

**削除が中心なので、二周目は語数が減る。**現在 5,460語、band は [5100, 5600]。
概算で 250〜350語の削除になるため、**下限 5,100 を割る危険がある。**
不足分は §3 のモチーフ状態記述と、ACT_5 の Brown II 引用（*"greatly at sea"* 周辺・AAA/NAF の経緯）で埋める。
**説明を足して埋めない。**引用と画で埋める。
