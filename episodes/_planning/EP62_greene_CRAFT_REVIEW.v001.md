# EP62 · GREENE v. LINDSEY — CRAFT REVIEW v001

**対象:** `episodes/_planning/EP62_greene_script.en.v002.md`
**基準:** `docs/PD_SCREENPLAY_STANDARD.v001.md` §16（R1〜R15・BINDING 2026-08-04）
**設計:** `episodes/_planning/EP62_greene_FILM_BIBLE.v001.md`（主題・モチーフ・転回・認知はここが正典）
**事実:** `EP62_greene_FACTS_LEDGER.v001.md` · 一次資料 `measurements/EP62_greene_RAW.md` · 契約 `episodes/PD-2026-062-greene/episode_spec.v001.json`
**形式:** `EP65_marmet_FILM_BIBLE.v001.md` §19 に準拠

> **判定：15項目中 PASS 3 / FAIL 12。**
> **うち事実誤り 4件**（craft ではなく invariant 1 の問題。**最優先で直す**）。
> 行番号は台本ファイルの行。引用は原文のまま（英語）。機械ゲートは全緑。**以下は機械が測れない部分である。**

---

## 0. 実測値（この review が依拠する数字・2026-08-04 計測）

| 指標 | 実測 | 標準 | 判定 |
|---|---|---|---|
| ナレーション語数 | **5,286**（見出し・`【】`・`⟨HELD⟩` を除く） | 5,100–5,600 | 帯内 |
| 文数 | 393 | — | — |
| 短文（6語以下）比率 | **30.8%**（121/393） | 20–35% | **合格** |
| 語り手の修辞疑問 | **0**（`?` は5個すべて証言の引用内） | ≤2/1000語 | **合格** |
| 二人称 you/your | 19 = **3.6/1000語** | ≤8/1000語 | **合格** |
| `⟨HELD⟩` | **9個**（L27, 60, 117, 156, 187, 242, 261, 316, 325） | 3個 | **不合格** |
| 区分別語数 | HOOK 141 / OP 51 / ACT_1 1001 / ACT_2 660 / ACT_3 830 / ACT_4 866 / ACT_5 1448 / ENDING 289 | — | HOOK が設計の6倍（§16.1） |

**リズムの数値は合格帯にある。**したがって以下の不合格は「文が下手」ではなく、**語り手が結論を言い、沈黙を予告に使い、モチーフを画に持たせていない**という設計の問題である。

---

## 1. R1〜R15 判定表

| # | 問い | 判定 | 証拠 |
|---|---|---|---|
| R1 | CONTROLLING IDEA を一文で言えるか | **PASS** | 言える。**国家が「あなたに伝えた」と扱ってよいのは、その伝え方が実際に届いているときだけである** |
| R2 | その一文は台本に**書かれていない**か | **FAIL** | L332 が主題をほぼ逐語で音読している：*"Before the State may treat a person as having been told something, it has to ask whether its way of telling them actually works"* |
| R3 | 語り手の結論文を全部削っても着くか | **FAIL** | 結論文14箇所・約306語。L163 *"Two words in that sentence carry the case."*／L278 *"Now the part that gets misremembered, and this film is going to spend real time on it."* |
| R4 | 認知は**一箇所**か | **FAIL** | 候補5つ。設計上の認知（L161–163 *well aware*）だけが `⟨HELD⟩` を持たない |
| R5 | 転回の前に反対側を最強の形で述べたか | **FAIL** | 述べた直後に L128 が種明かしする：*"That is the Court defending the practice it is about to hold inadequate."* しかも転回まで13分ある |
| R6 | モチーフの状態変化を順に言えるか | **FAIL** | 七状態は台本に**一つも指定が無い**。`【】` は4個で、紙の状態指定は L340 `【callback: the taped corner】` のみ |
| R7 | 各主要人物に反復不能な細部があるか | **PASS** | Bacon *"probably a couple of times."*／Brutscher *"the six months I was working at it"*／*"Oh, we had plenty of trouble."*／Village West／Weber 1909／New York の翌日郵送 |
| R8 | 悪役を作っていないか | **FAIL** | L243 *"The State took more care to find you when it wanted your money than when it wanted your home."*／L216 *"ruled against them anyway"* |
| R9 | 賭け金は縦（深さ）に上がっているか | **PASS** | 三つのドア(L91) → 団地全戸(L204) → 十一州(L300) → 仮定そのもの(L342–344) |
| R10 | ENDING に新事実がゼロか | **FAIL** | L334 *"seven or eight men"* ——**記録に無い数字**（92%線 27:36／ENDING 28:20 開始） |
| R11 | ENDING は最初の画に戻るか | **FAIL** | 言葉では戻る。画は L340 が状態5（破れた角）を指定しており、設計の状態1に戻っていない |
| R12 | 沈黙の位置を三つ言えるか | **FAIL** | 9個。しかも**9個すべてが重い一文の直前**＝太鼓の連打。§11 の「直後」が0個 |
| R13 | 矛盾する記録を矛盾のまま出したか | **FAIL** | L154 が同一証言の免責側 *"So we never had any problems with that."* を落とし、L338 が *"The men who climbed it described one."* で矛盾を平らにする |
| R14 | 記録の沈黙を沈黙のまま扱ったか | **FAIL** | L46/L288 は PD 最良級。しかし L124 が記録に無い社会像を丸ごと創作している |
| R15 | 声に出して読んだか（機械代替） | **FAIL** | L126（58語・3階層）／L234（数字4個）／L300（州名11連）／appellant 11回 vs appellee 3回（音で判別不能） |

---

# 2. 事実誤り — **craft より先に直す**（invariant 1／台帳 G5）

> このクラスは「上手いかどうか」ではない。**台帳が禁じた種類の言明が台本に入っている。**
> 4件のうち2件は ENDING にあり、1件は引用の書き換えである。

### F1（最重要）· L334 — 記録に無い人数

> *"In this case the evidence was seven or eight men describing their rounds..."*

**判決文はこの人数をどこにも書いていない。**一次資料で数えられるのは、多数意見 n.7 の三つの供述抜粋（App. 74 / 80 / 82）、n.8 の App. 76、反対意見の Bacon・Brutscher・App. 74 の男・CA6 p.74 の男だけであり、重複を最大に見積もっても**5人前後**である。判決文自身の語は *"a handful of process servers"*（GL-74）。
さらに**台本は自分で矛盾している**——L179 で *"a handful of men"* と正しく言い、ENDING で *"seven or eight"* に膨らませている。

台帳 G5：「No number appears that the opinion does not print」。契約 `forbidden_claims`：判決文が持たない数字の禁止。**これは craft の指摘ではなく違反である。**

**置き換え**：*"In this case the evidence was a handful of men describing their rounds, and the Housing Authority telling those men that the papers came off the doors."*
（L179 と同じ語にそろえる。人数を数えない。）

---

### F2 · L310 — 引用の書き換えが意味を変えている

台本：
> *"...it is difficult to see how a means of serving process that fails to afford actual notice in a not insubstantial number of cases can be deemed **adequate — whatever the proceeding is called**."*

原文（n.4・GL-62）：
> *"...can be deemed **either prompt or certain**."*

**これは要約ではなく差し替えである。**原文の *"prompt or certain"* は、反対意見が持ち出した**手続の目的（迅速性）**をその目的の言葉で打ち返している——だからこの一文は答弁として効く。*"adequate"* に替えると、ただの結論の反復になり、**台本が「これが事件を決める一文だ」と紹介した根拠が消える。**

**置き換え**：*"From the perspective of the tenant, it wrote, it is difficult to see how a means of serving process that fails to afford actual notice in a not insubstantial number of cases can be deemed either prompt or certain."*
（*whatever the proceeding is called* は削る。原文がやっている仕事を語り手が言い直す必要が無い。）

---

### F3 · L154 / L157–159 — 引用から躊躇の語が消え、その上に山場が建っている

台本：
> *"They never took them off when we were present, but the Housing Authority told us that they would take them off, so we always put them up high."*

原文（GL-39・App. 74）：
> *"They never took them off when we were present, but we, **you know, assume —** the Housing Authority told us that they would take them off, so we always put them up high."*

証人は「我々は**推測している**」と言いかけて言い直している。台本はその途切れを黙って消し、直後に `⟨HELD⟩` を打ち、*"The Housing Authority told us."* を単独の一行にして、L159 で *"The landlord's own staff had told the men doing the posting that the papers came off the doors, and the men doing the posting kept posting them."* と続ける。**削った語の上に、一番重い告発が建っている。**

これは台帳 Q-07（記録の誇張＝反対意見が突いているまさにその欠点）に該当する。

**置き換え**：省略記号ごと原文を鳴らす。*"They never took them off when we were present, but we, you know, assume — the Housing Authority told us that they would take them off, so we always put them up high."*
L159 は *"and the men doing the posting kept posting them."* を削り、*"The Housing Authority's own staff had told the men doing the posting that the papers came off the doors."* で止める（**継続の非難を足さない**）。

---

### F4 · L124 — 記録に一行も無い社会像

> *"Think about who is behind the doors of a public housing project on a Tuesday at eleven in the morning. People at work. People at a second job. People taking a child somewhere, or standing in a queue at an office, or asleep after a night shift. The population most likely to miss a single daytime knock is the population the procedure was aimed at."*

**火曜日も、十一時も、二つ目の仕事も、夜勤も、窓口の列も、記録に無い。**最後の一文は手続の**狙い**についての主張で、Q-08（動機の帰属禁止）の隣に立つ。§15 の即失格条件5「沈黙している記録への声当て」に該当する。
種は L94 *"in the middle of a working day"* にもある——判決文は *"a good percentage"* の訪問で不在だったと書いているだけで、**訪問が日中だったとは言っていない。**

**置き換え**（記録が持つ語だけで同じ仕事をする）：
> *"The record does not say what time of day the deputies came. It says only that in a good percentage of cases, nobody was there. The word is the appellants' own."*

L94 の *"in the middle of a working day"* は削り、*"when a deputy walked up to a door in a Louisville housing project"* で止める。

---

### F5（軽微・ただし修正必須）

| 行 | 問題 | 置き換え |
|---|---|---|
| L236 | *"Briefs came in from the National Housing Law Project, and from the Antioch School of Law, urging the Court to affirm."* — *urging affirmance* は**Antioch にだけ**付いている（GL-11） | *"David Madway filed a brief for the National Housing Law Project. Lynn Cunningham filed one for the Antioch School of Law, urging the Court to affirm."* |
| L236 | *"a question about how every summary eviction in the country begins"* — 全国規模の断定。記録が支えるのは反対意見の**11州**だけ | *"a question about how a summary eviction begins in every State that served notice this way."* |
| L214 | 地裁の認定引用から *"by other tenants"* が落ちている（GL-32）。**子どもの話に見えてしまう** | *"...notices posted on the apartment doors of tenants are often removed by other tenants."* |
| L268 | *"The Postal Service is an efficient and inexpensive means of communication."* — 多数意見の語は *"the mails"*。*Postal Service* は**反対意見の語** | *"The mails, it wrote, are an efficient and inexpensive means of communication."* |
| L294 | *"On this flimsy basis, the Court overturns the work of the Kentucky Legislature."* — *confidently* と *"and, by implication, that of at least 10 other States"* が無表示で落ちている | *confidently* を戻す。後半は L300 の11州と重複するので落としてよいが、**同じ段落内で処理する** |
| L259 | 転回の引用が *"reliance on posting under this statute"*（原文 *"pursuant to the provisions of § 454.030"*） | 音読のための短縮として**許容**。ただし §454.030 は L75 で既出なので *"reliance on posting under section 454.030"* が正確かつ同じ長さ |

> **契約側の誤記（台本の誤りではない）**：`episode_spec.v001.json` の `forbidden_claims` が **"Pannell Ray"** と書いている。判決文と台帳は **Pamela Ray**。台本は正しい。**spec 側を次の改訂で直すこと**（本 review はファイルを一つしか作らないため未修正）。

---

# 3. 不合格項目ごとの改訂指示

## R2 — 主題を語り手が音読している → **FAIL**

**(a) L332（ENDING 冒頭・最重量）**
> *"What the case leaves is smaller than its reputation and more durable than its remedy. Not a rule about envelopes. A method. **Before the State may treat a person as having been told something, it has to ask whether its way of telling them actually works** — here, in these buildings, on these doors, under the conditions the State itself has described in its own brief."*

太字部分が FILM_BIBLE §1 の CONTROLLING IDEA そのものである。§1 は「**この文は映画の中で一度も口に出さない**」と定めている。**43語、丸ごと削る。**

**残す**：*"What the case leaves is smaller than its reputation and more durable than its remedy. Not a rule about envelopes. A method."*
**その後に何も足さない。**「どんな method か」を言った瞬間、観客の仕事が消える。L338 と L342–344 が既にそれを実演している。

**(b) L38（OP）**
> *"What follows is not really a story about eviction. It is a story about a piece of paper, and about what a State is allowed to assume once it has let go of one."*

主題の**予告**であり、同時に「この映画は何の話か」というメタ発言（§7）。
**置き換え**：*"The case is about a piece of paper."* ——8語。契約としてはこれで足りる。

**(c) L163**
> *"Two words in that sentence carry the case. **Well aware.**"*

語り手が「ここが核心だ」と宣言している。EP65 の *"Now the sentence this film exists to say."* と同型で、§7 抑制違反として最も重い。
**置き換え**：前置きを削り、*"**Well aware.**"* を単独で置く。**そして `⟨HELD⟩` をこの直後に移す**（R4/R12 と同一作業）。

**(d) L278**
> *"Now the part that gets misremembered, and this film is going to spend real time on it."*

①他人の語り直しへの反論（解説者の口調）②自分の構成の予告（メタ）。**削る。**直後の L280 *"The Court did not ban posting."* が単独で立つ。

**(e) L167 / L192 — 「この映画は〜しない」という自己申告**
> L167 *"It would be dishonest to leave the record there, and this film is not going to."*
> L192 *"That distinction is not a hedge. It is the difference between a documentary and a story."*

**両方削る。**§13 は「沈黙している記録に声を当てない」ことを**品位**と呼んでいる。品位は実行するものであって申告するものではない。L167 は *"The testimony was not all one way, and the dissent said so directly."* から始めればよい。L192 は L190 で完結している。

---

## R3 — 結論文の総量 → **FAIL**

**削る（型①：他人の語り直しへの反論・メタ）** — R2(d)(e) と L284 *"in a clause almost nobody quotes"*。

**削る（型②：直前の引用を語り手が言い直す）**

| 行 | 文 | 理由 |
|---|---|---|
| L266 | *"Missing someone once tells you nothing about them. It tells you something about the time of day."* | 直前 L264 の引用（*hardly suggests that the tenant has abandoned his interest*）が既に言っている |
| L274 | *"Not the paper on the door — the decision to let the paper be the only thing."* | *"Continued exclusive reliance."* の断片だけ残す。**短いほうが強い** |
| L312 | *"Speed is a reason to keep a procedure short. It is not a reason to keep it from working."* | 直前 L310 の多数意見の答弁の劣化コピー。F2 で原文を正しく戻せば不要になる |
| L48 | *"That absence is not sloppiness. It is what this kind of case looks like from the inside."* | 同じ段落の残り（*"The question in front of the courts was never whether these three women were good tenants..."*）が完成形 |
| L58 | *"There is a temptation, in a story like this, to reach for the landlord who wants somebody out. Reach for it here and you have the facts wrong."* | 語り手が観客の読み方を管理している。次の二文（*"The body that started these proceedings was a government body. The men who carried the paper were sworn officers."*）だけで事実として足りる |
| L122 | *"The people defending the system are the ones telling you how often the first knock finds nobody home."* | 直前の *"It is not the Court's estimate. It is the appellants' own."* で完了している |
| L61 | *"Which is why it became a constitutional question at all."* | 接続の説明。L63 の question presented が自分で示す |

**残す（削ってはいけない）**

- **L306** *"The majority never proved the mails were better. It proved this door was worse."* ——結論文だが、Q-02/Q-03（「郵便を義務づけた」「掲示を禁止した」）への**唯一の防波堤**であり、形容詞ゼロ。**手本。**
- **L118** *"The ladder had one rung."* ——標準 §10 が挙げている型そのもの（長い助走を5語で切る）。**位置だけ直す**（`⟨HELD⟩` を後ろへ）。
- **L240** *"Money got a person served. The apartment did not."* ——記録（GL-72）に密着した8語。**L243 のほうを削る**（R8）。
- **L46** *"No ages. No jobs. No families. No rent figures, no arrears, no account of what they were supposed to have done. Three names and a shared address."* ——**PD 全話でも上位の一節。触らない。**
- **L69**（*"A hearing that a person does not know about is not a hearing they failed to attend. It is a hearing that happened to them."*）——語り手の結論だが、L332 を削るなら**この一箇所だけは残してよい。**主題の断定ではなく *notice* の定義の言い換えであり、位置が前半（観客が自分で組む余地が後ろに残る）。**L69 と L332 の両方を残すことは認めない。**

**合計削除見込み：約306語**（内訳は §5 の予算表）。

---

## R4 — 認知が5つある → **FAIL**

FILM_BIBLE §5 は認知を **L161–163 の *As the process servers were well aware*** 一点に固定している。台本にはそれと同格に見える瞬間が5つある。

| 行 | 認知を名乗っているもの | 判定 |
|---|---|---|
| L117–118 | `⟨HELD⟩` → *"The ladder had one rung."*（条文の梯子の崩壊） | **転回でも認知でもない。期待の裏切り。** `⟨HELD⟩` を外す |
| L156–159 | `⟨HELD⟩` → *"The Housing Authority told us."* | **本来の認知の5行手前で、本来の認知が持つべき沈黙を奪っている。** `⟨HELD⟩` を外す |
| **L161–163** | *"As the process servers were well aware..."* → *"Well aware."* | **これが唯一の認知。`⟨HELD⟩` が無い。付ける** |
| L187–188 | `⟨HELD⟩` → *"Nobody ever tried that question. It never got that far."* | 重要だが**限界の提示**。ACT_5 の限界と役割が重複。`⟨HELD⟩` を外す |
| L242–243 | `⟨HELD⟩` → *"The State took more care to find you..."* | 認知ではなく**語り手の道徳判決**。R8 で行ごと削除 |

**是正（一括）**
1. L163 の前置きを削り、*"**Well aware.**"* の**直後**に `⟨HELD⟩` を移す。
2. L27, 60, 117, 156, 187, 242, 316, 325 の `⟨HELD⟩` を**外す**。
3. `⟨HELD⟩` は三つだけ残す（R12 参照）。
4. L120 の `【reset beat: hold on the walkway, no narration, 4s】` は沈黙ではなく**画の休符**なので残す。ただし R6 に従い被写体を walkway から**紙の状態3（風に持ち上がる角）**に書き換える。

---

## R5 — 反対側は述べているが、語り手が種明かしをしている → **FAIL**

**述べてはいる。**L126–L132 は PD が書いた中で最も長い「相手側の最強形」である——*"singularly appropriate and effective"*、*"many or perhaps most instances"*、そして L132 の所有者推定（GL-70）。**素材は足りている。** 不合格の理由は二つ、どちらも構造である。

**(a) L128 が効果を自分で壊している。**
> *"Singularly appropriate. Singularly effective. That is the Court defending the practice it is about to hold inadequate."*

§4.1 が要求するのは「**観客はここで負けると思う**」状態である。*"about to hold inadequate"* と言った瞬間、観客は負けると思わない。**これは仕掛けの種明かしであり、13分後の転回を安い勝利に変える一文である。**
**削る**：*"That is the Court defending the practice it is about to hold inadequate."*
**残す**：*"Singularly appropriate. Singularly effective."* ——形容詞は判決文が持っているものだけ。何も足さない。

**(b) 最強形と転回のあいだが13分ある。**
擁護は ACT_2（L126–133・約9分地点）、転回は ACT_5（L259・約22分地点）。あいだに ACT_3 の証言と ACT_4 の訴訟史が入り、**転回の直前（L249–257）にあるのは Mullane の基準と *practical application* ——転回に反対する材料ではなく、転回を用意する材料である。**

**是正**：転回の直前に、**掲示を支える推定を判決文自身の言葉で一度だけ戻す。**新規の説明は書かない。台帳 GL-70 が引く Mullane n.6 を使う。

L257（*"Practical application. Not the words of the statute. What the thing does."*）と L259（転回）のあいだに挿入：

> *"And the Court had just restated the reason posting normally works. The ways of an owner with tangible property, it quoted, are such that he usually arranges means to learn of any direct attack upon his possessory or proprietary rights. Entry upon real estate in the name of law may reasonably be expected to come promptly to the owner's attention. On that understanding, a State may conclude that in most cases a notice secured to a person's property is warning enough."*

（GL-70 / RAW 註6 · **逐語**。約60語。）**その直後に L259 の *But whatever the efficacy of posting in many cases...* が来る。**擁護と転回が接する。

**(c) 反対意見側も同じ処置が要る。**L308 は *Lindsey v. Normet* の引用を一文に圧縮しているが、反対意見が最も強いのは経済の具体である。**Q-10 に従い事件名は絶対に出さず**、引用だけ足す：
> *"Many expenses of the landlord continue to accrue whether a tenant pays his rent or not."*
（GL-77 · 逐語・15語。**「リンジー」という語を出さない。**）

---

## R6 — モチーフが存在しない → **FAIL（最重量）**

FILM_BIBLE §3 は紙の七状態を**登場順に固定**している。台本の `【】` 指定は**4個しかない**。

| 行 | 現行の指定 | 紙の状態か |
|---|---|---|
| L30 | `【OST: A PIECE OF PAPER】` | 文字。画ではない |
| L120 | `【reset beat: hold on the walkway, no narration, 4s】` | walkway。紙ではない |
| L340 | `【callback: the taped corner】` | **状態5のみ**（唯一の紙） |
| L346 | `【OST: STILL THERE】` | 文字 |

**七状態のうち画として指定されているのは1つ。**紙はナレーションの話題としては何度も出るが（L21・L99–103・L342）、**状態が順に変化していないので、画が論証を運んでいない。**§5 の「同じ物を、違う状態で、順番に見せる」を満たしていない。現状、モチーフの役を負っているのは**文字列**である（EP65 と同じ失敗）。

**是正：七状態を台本本文の `【】` 指定として入れる。**ナレーションは一語も足さない（＝**語数は増えない。R6 を語数不足の穴埋めに使えない**）。

| 状態 | 指定 | 挿入位置 |
|---|---|---|
| 1 テープで平らに貼られている | `【motif 1: the paper taped flat, corners square】` | **L21 の直後**（HOOK・*"A thumbtack, or a strip of tape."*） |
| 2 角が浮いている | `【motif 2: one corner lifted from the paint】` | **L91 の直後**（*"Three doors. No conversation on any doorstep."*） |
| 3 風に持ち上がる | `【motif 3: wind lifts the sheet, nobody in frame】` | **L120 の reset beat を書き換える**（walkway → 紙） |
| 4 段の下に落ちて濡れている | `【motif 4: the sheet on concrete under the stair, wet through】` | **L161 の直前**（認知の直前・無音で） |
| 5 破れた角がテープの下に残る | `【motif 5: a torn corner still under the tape】` | **L188 の直後**（*"It never got that far."*） |
| 6 何も無いドア | `【motif 6: the door, nothing on it】` | **L288 の直後**（*"The record simply stops."*） |
| 7 褪せていない四角い跡 | `【motif 7: an unfaded square where the paper was】` | **L338 の直後**（ENDING・callback の直前） |

**プラント→ペイオフ**：ACT_2 のテープ（L99–101・約7分）と ENDING の L340（約29分）で**22分**離れている。craft 規則（2分以上）を大きく満たす。**この配線は既に正しい。壊さない。**

---

## R8 — 二箇所で悪役を作っている → **FAIL**

個人は作っていない。執行官の扱い（L342 *"He did what the statute told him to do."*）は**設計どおりで、この台本の最良部の一つ**である。問題は**制度に向けた語り手の形容**である。

**(a) L242–243（`⟨HELD⟩` 付き・最重量）**
> ⟨HELD⟩
> *"The State took more care to find you when it wanted your money than when it wanted your home."*

三つ問題がある。①**記録が支えない**——GL-72 が言うのは「家賃請求ならケンタッキー法が対人送達を要求した」であって、州が**より気にかけた**という意思の帰属ではない。②二人称で州を告発している（*your money / your home*）。③**沈黙が語り手の論説に与えられている**（R12）。
**行ごと削る。`⟨HELD⟩` も外す。**
**残す**：直前の L240 *"Money got a person served. The apartment did not."* ——**8語で、記録の内側で、同じ落差が立っている。**§9 の「誰かが悪いのなら、それは小さい話である」が求めるのは、まさにこの止め方である。

**(b) L216**
> *"Undisputed testimony. Often removed. The judge who ruled against these women wrote that down, and then ruled against them **anyway**..."*

*anyway* は嘲りである。しかも L222 が6行後に *"That is not a contradiction in the judge's logic."* と正しく擁護しており、**台本が自分の非難を自分で取り消している。**
**置き換え**：*"The judge wrote that down. Then he ruled that the procedure was constitutionally sufficient — on the ground that posting only comes into play after the officer cannot find the defendant on the premises."*
（*"The judge who ruled against these women"* → *"The judge"*。*anyway* を落とす。**事実の並びだけで十分に奇妙である。**）

**(c) L159** *"and the men doing the posting kept posting them."* → F3 で削除済み。継続の非難を足さない。

---

## R10 — ENDING に新事実がある → **FAIL**

尺30:00・**92%線＝27:36**。ENDING は 28:20 開始なので、**ENDING 全体（289語）が 92% 以降**である。

**(a) L334 *"seven or eight men"*** → **F1。新事実であり、かつ記録に無い数字。**最優先。

**(b) L336**
> *"The majority did not weigh the servers' testimony against a study, or a survey, or a count. There was nothing else to weigh it against."*

「他に証拠が無かった」という**確認された不在**は台帳（§5 前文）が持つが、**台本ではここが初出**である。ENDING の仕事は再フレームであって情報ではない（§12）。
**是正**：この二文を **ACT_3 の L165 の直後**（*"...the Court used the words the record supported and no stronger ones."*）に移す。ENDING では前提として響くだけになる。**語数は移動なので増減ゼロ。**

**(c) L342 の *"a painted door"* と *"drove to the next address"*** は FILM_BIBLE §12 が設計した最終画であり、**画としては承認済み**。ただしナレーションが**特定の一人の行動を叙述**している形になっている。
**是正**：*"Somewhere in Louisville in 1975 a deputy pressed a strip of tape onto a painted door."* までを残し、*"and drove to the next address"* は**ナレーションから落として `【】` に移す**（`【the hand leaves frame; the walkway is empty】`）。事実の主張を減らし、画を増やす。

---

## R11 — 画のループが閉じていない → **FAIL**

**言葉では戻っている。**HOOK L21（*"a strip of tape"*）→ ENDING L342（*"pressed a strip of tape"*）、および L23（*"once it was on the door, the tenant had been served"*）→ L344（*"That the paper would still be there."*）。**この二層は良い。残す。**

**画では戻っていない。**FILM_BIBLE §3 のマクロ・ループは**状態1で始まり状態1に戻る**（`G208`→`G209`）。台本の最終指定は L340 `【callback: the taped corner】` ＝**状態5**である。破れた角に戻ると「壊れた」で終わる。設計は逆で、**二周目に見たとき意味が反転する同一構図**が要る。

**是正**：R6 の状態1（L21 直後・`【motif 1: the paper taped flat, corners square】`）と、ENDING の最終画を**同一アングル・同一サイズで**撮る。L340 を次に差し替える。

```
【callback: motif 1 again — the paper taped flat, corners square. Same framing as HOOK.】
```
そして L344（*"That the paper would still be there."*）のあと、`【OST: STILL THERE】` の直前に **`【motif 7: the unfaded square】`** を置く。
**順序：状態1（同一構図）→ 台詞 → 状態7 → OST。**これで「同じ画・違う意味」と「制度は自分の痕跡を残す」が二段で立つ。

---

## R12 — 沈黙が9個あり、**9個すべてが太鼓の連打** → **FAIL**

`⟨HELD⟩` は L27, 60, 117, 156, 187, 242, 261, 316, 325 の**9個**。標準は三箇所（§11）。数より悪いのは配置である。**9個すべてが「次に重い一文が来る」予告として重い文の直前に置かれている。**

| 行 | ⟨HELD⟩ の直後に来る文 |
|---|---|
| L27 | *"Their landlord was not a landlord."* |
| L60 | *"Which is why it became a constitutional question at all."* |
| L117 | *"The ladder had one rung."* |
| L156 | *"The Housing Authority told us."* |
| L187 | *"Nobody ever tried that question."* |
| L242 | *"The State took more care to find you..."* |
| L261 | *"And so posting on the apartment door could not be considered a reliable means..."* |
| L316 | *"The category was not the question."* |
| L325 | *"That is where the two opinions stop talking to each other."* |

§11：「**沈黙は、直前の一文が重いときにだけ効く。**」**直後に置かれた `⟨HELD⟩` は0個である。**現状の9個は、重い一文が来ることを毎回予告しており、**九回予告された驚きは驚きではない。**

**是正：三つに削り、すべて「重い一文の後」に置く。**

1. **認知の直後** — L163 の *"**Well aware.**"* の**後**
2. **限界の直後** — L286（*"...posted service accompanied by mail service is constitutionally preferable to posted service alone."*）の**後**
   ※ L280–286 が §7「限界」の本体。**L261 の `⟨HELD⟩` はここへ移す**（転回の途中ではなく、限界を言い終わってから止める）
3. **最終画の前** — L344（*"That the paper would still be there."*）と `【motif 7】` のあいだ

残り6個は削除。L120 の `【reset beat ... 4s】` は画の休符なので残す（内容は R6 に従い状態3へ）。

---

## R13 — 矛盾を語り手が解いている → **FAIL**

**良い部分がある。**L167–L179 は反対側の証言を実名で載せており（Brutscher の *"the six months I was working at it there was no occasion where I saw anyone tear the Writs off of the door."*、および L177 の「一度も見たことがない」証人）、L179 は *"a handful of men, describing a practice they had each seen differently"* と正しく閉じている。**§9 の「片側だけの映画は弱い」を満たしている数少ない PD 台本である。** それでも三点で不合格になる。

**(a) 同一供述の免責側が落ちている（最重要・F3 と一体）。**
多数意見が引いた App. 74 の証人は、**反対意見が引く同じ供述の続きで**こう言っている：
> *"...always put [the writs] up high. **So we never had any problems with that.**"* (RAW · dissent · App. 74)

台本は L154 でこの証人の前半だけを使い、`⟨HELD⟩` と一段落の論評を与えたうえで、後半を一度も出さない。**同じ口から出た二つの半分のうち、片方だけを使っている。**§13 が最も厳しく禁じる形である。
**是正**：L177 の反対証言の段落に、**同一人物であることを明示して**足す。
> *"The man who said the Housing Authority had warned them said something else in the same deposition. They always put the writs up high — so we never had any problems with that. The majority quoted the first half. The dissent quoted the second."*
（**どちらが正しいとも言わない。**これが §13 の「記録は自分自身と一致していない」である。）

**(b) L338 が、25行前に自分が出した矛盾を平らにしている。**
> *"The statute described a ladder with three rungs. The men who climbed it described one."*

**記録では、男たちは一つに揃っていない。**Brutscher は六か月で一度も見ていない。もう一人は苦情を受けたことも子どもが試みるのを見たこともない。この一文は多数意見の読みを**映画の声**にしている。
**置き換え**：
> *"The statute described a ladder with three rungs. The men who climbed it did not describe it the same way as each other. Both descriptions were in the record, and the Court chose the one made by the men who said the paper came off."*
（**+15語。**「観測が割れている」という事実を残したまま、裁判所が選んだことを述べる。）

**(c) *undisputed* と *scant and conflicting* が一度も突き合わされない。**
台帳 GL-47 が名指ししているとおり、**地裁は同じ証言を *undisputed* と呼び（L214）、反対意見は *scant and conflicting* と呼んだ（L294）。**台本は両方を出すが、80行離れており、観客が並べられない。
**是正**：L294 の直後に一文だけ置く。
> *"The District Court had called the same testimony undisputed."*
（**+8語。**論評しない。二つの語を隣に置くだけで矛盾が立つ。）

---

## R14 — 沈黙を三箇所で埋めている → **FAIL**

**最良の部分は絶対に削らない。**
- **L46** *"No ages. No jobs. No families. No rent figures, no arrears, no account of what they were supposed to have done. Three names and a shared address."*
- **L183–185** *"Claimed. Stated. Those are the Court's verbs, and the Court kept them."*
- **L190** *"What is established is the practice. What is alleged, and never tested, is what happened at three particular apartments in 1975."*
- **L288** *"What became of Linnie Lindsey, Barbara Hodgens and Pamela Ray is not in the opinion. The record simply stops."*

**三人のその後の沈黙は完全に守られている。**契約 `forbidden_claims` の「その後を語らない」も、Q-05・Q-06・Q-11 も違反していない。**R14 の不合格は三人についてではない。**

**埋めている三箇所**
- **(a) L124** — 火曜日・十一時・二つ目の仕事・夜勤・窓口の列。→ **F4 で全面置換。**
- **(b) L94** — *"in the middle of a working day"*。→ **F4 で削除。**
- **(c) L334** — *"seven or eight men"*。記録が数えていない人数を数えている。→ **F1。**

**(d) 軽微**：L67 *"A day off work, or a shift swapped, or a child minded."* は特定の三人についての記述ではなく、*notice* が何を要求するかの一般化として読める。**残してよい。**ただし L124 を削った後は、この一文が「生活の具体」を担う唯一の場所になるので、**ここを膨らませない**こと。

---

## R15 — 音で壊れる箇所（機械代替による判定） → **FAIL**

数値上のリズムは合格帯にある（短文30.8%・修辞疑問0・二人称3.6/1000）。**したがって不合格の根拠は指標ではなく、音読すれば必ず残らない具体箇所である。**

**(a) L126 — 58語・従属3階層。この台本で最長の文。**
> *"Short of providing personal service, it wrote, posting notice on the door of a person's home would, in many or perhaps most instances, constitute not only a constitutionally acceptable means of service, but indeed a singularly appropriate and effective way of ensuring that a person who cannot conveniently be served personally is actually apprised of proceedings against him."*

従属開始（*Short of...*）→ 挿入（*it wrote*）→ not only/but indeed → 関係節（*that a person*）→ その中の関係節（*who cannot conveniently be served*）。**R5 が依存している一文であり、音で失うわけにいかない。**
**置き換え**（引用を割る。語は変えない）：
> *"Short of providing personal service, it wrote, posting notice on the door of a person's home would in many or perhaps most instances be a constitutionally acceptable means of service. **And more than that.** A singularly appropriate and effective way of ensuring that a person who cannot conveniently be served personally is actually apprised of proceedings against him."*

**(b) L234 — 一文に数字が4つ。**
> *"The Supreme Court noted probable jurisdiction in 1981, heard argument on the twenty-third of February 1982, and decided it on the seventeenth of May, as number 81-341 on its docket."*

1981／1982年2月23日／5月17日／81-341。EP65 の L337 と同じ事故である。
**置き換え**：*"The Supreme Court took the appeal in 1981. It heard argument on the twenty-third of February 1982, and decided it that May."*
**ドケット番号 81-341 と決定日は `【OST】` に置く。耳に置かない。**

**(c) L300 — 州名11連。**
> *"Alabama, Colorado, Florida, Kansas, Kentucky, Louisiana, Mississippi, Nebraska, New Hampshire, North Carolina and West Virginia."*

固有名詞11個の連続は約9秒の単調な壁になる。ただし**十一州は §4.3 の賭け金の梯子の一段**であり、落とせない。
**是正**：**数はナレーションが言い、名前は画が言う。**
> *"It listed them in a footnote. Eleven States."*
> `【OST: the eleven States, listed】`

**(d) L210 — 固有名詞と数字の重ね置き（54語）。**
> *"Some seventy years earlier, in Weber v. Grand Lodge of Kentucky, the Sixth Circuit had upheld posting under the predecessor statute to section 454.030 — on the ground that it was reasonable for the State to presume that a notice posted on the door of the building in dispute would give the tenant actual notice in time to contest the action."*

*Weber* ／*Grand Lodge of Kentucky*／*Sixth Circuit*／*section 454.030*／*seventy years* が一息に来る。
**置き換え**：*"It leaned on a case called Weber, decided by the Sixth Circuit some seventy years earlier. Weber had upheld posting under the statute that came before section 454.030 — on the ground that it was reasonable for the State to presume that a notice on the door of the building in dispute would reach the tenant in time to contest the action."*

**(e) appellant / appellee — 全編で音が判別できない。**
実測：*appellant* 11回・*appellee* 3回。**この二語は耳でほぼ同じである。**しかも本作では appellants ＝保安官側、appellees ＝住人側で、**取り違えると立場が反転する。**
**是正**：引用の内側（L115 *"we reject appellants' characterization"*、L185 *"appellees claim to have suffered"*、L276 の holding など）は原文どおり残し、**地の文はすべて言い換える**——L89 *"The appellants — the sheriff and the officials —"* → *"The sheriff's side"*、L105 *"in the appellants' own words, from their brief"* → *"in the sheriff's side's own brief"*、L183 → *"The three women"*。**引用の外に appellant/appellee を残さない。**

**(f) L249–L257 と L268 — 長い引用の壁が二度。**
- L249：54語の Mullane 基準がそのまま置かれ、直後 L253・L255 でさらに三つの引用が続く。**L255 は二つの引用が一段落に融合している。**
- L268：三つの引用（*efficient and inexpensive* ／*would surely go a long way* ／*Particularly where the subject matter...*）が約85語で連続する。

**是正**：§10 の「30語超の助走を5語以下で切る」を**引用の連続にも適用する**。L255 の二引用のあいだに *"Then the test itself."*（4語）、L268 の二つ目と三つ目のあいだに *"And then the shape of it."*（6語）を挟む。**内容は足さない。息継ぎだけを足す。**

**手順**：改訂後、**通しで音読し、読了を記録する。**§16 は「R15は省略しない」と明記している。本 review は機械代替（最長文・数字密度・固有名詞連続・同音語）で判定しており、**音読の代わりにはならない。**

---

# 4. R1〜R15 の外側 — 未解決の契約衝突（改訂前にオーナー判断が要る）

**HOOK が設計の6倍ある。**

- `PD_ONE_PASS_PRODUCTION_SPEC.v2` 行9（BINDING）・および **本エピソードの FILM_BIBLE §4／§9**：**HOOK は 8秒・台詞20〜25語。**
- 台本 v002：`## HOOK (0:00–0:50)`・**実測141語**（≈48秒）。台本 L11 はこれを *"cold open ≤60s"* として正当化している。

**設計書と台本が正面から食い違っており、どちらも BINDING である。**受入ゲート `hook_added`（6〜10秒）はこのままだと落ちる。EP65 §9 が同じ衝突を記録し、未決のままである。

**この review はどちらも選ばない。**次のどちらかを APR に記録してから改訂すること。
- **(a) v2 準拠**：8秒の HOOK を最後に書き（FILM_BIBLE §9 の3カット／回収表に従う）、現行141語は OP 前の cold open として別扱いにする → `section_vocabulary` は8キー固定なので spec 改訂を伴う。
- **(b) 偏差承認**：EP62 は48秒の HOOK で行くと明記し、受入ゲートの当該項目を承認済み偏差として記録する。

**なお、HOOK の中身自体は設計と整合している。**L21 のテープ／L25 の「知らないまま負けた」／L28 の `⟨HELD⟩` 直後の *"Their landlord was not a landlord."* は FILM_BIBLE §9 の回収表どおりである（ただし §12 の `⟨HELD⟩` 是正で L27 の沈黙は外す）。

---

# 5. 語数予算 — **下限5,100を割らせない**

改訂は削除が中心である。**必ず先に足し戻し分を確定してから削ること。**

| | 語数 |
|---|---|
| 現行 | **5,286** |
| 削除見込み（R2 L332/L38/L163/L278/L167/L192 ・R3 の7箇所 ・R5 L128 ・R8 L243 ・F4 L124 ・R15 の圧縮） | **−306** |
| 小計 | **4,980** ← **下限を120語割る** |
| **足し戻し（すべて台帳の逐語。一般論は書かない）** | |
| GL-70 · Mullane 註6 の所有者推定（R5・転回の直前） | +60 |
| GL-77 · *"Many expenses of the landlord continue to accrue whether a tenant pays his rent or not."*（R5(c)・**事件名は出さない／Q-10**） | +15 |
| GL-46 + RAW 註 · App.74 証人の後半 *"So we never had any problems with that."*（R13(a)） | +35 |
| GL-39 · *"we, you know, assume —"* の復元（F3） | +5 |
| GL-62 · *"either prompt or certain"* の復元と n.4 の家主側視点（F2） | +25 |
| GL-32 · *"by other tenants"* の復元（F5） | +3 |
| GL-11 · amici の帰属訂正（F5） | +8 |
| R13(b) L338 の正確な言い換え | +15 |
| R13(c) *"The District Court had called the same testimony undisputed."* | +8 |
| GL-42 · *"a good percentage"* を証言として明示（F4 の置換文） | +25 |
| **合計 足し戻し** | **+199** |
| **改訂後見込み** | **5,179**（帯 [5,100, 5,600] · 下限まで79語の余裕） |

**注意二点。**
1. **R6 のモチーフ七状態は `【】` 指定であり、ナレーション語数は1語も増えない。**語数不足の穴埋めに使えない。
2. **説明を足して埋めない。**足し戻しは**すべて台帳の逐語行**である。一般論を足すと具体性フロア（§8・1分あたり5〜12個の硬い事実）が下がり、機械ゲートは通るが水準が落ちる。

---

# 6. まとめ — 二周目が一度で通るための順序

**変更は一括で当てる**（`feedback_no_wasted_cycles`：全 fail を出し切ってから一回で直す）。

1. **事実誤り4件を先に直す**（F1 *seven or eight men* ／F2 引用の書き換え ／F3 削られた躊躇 ／F4 創作された社会像）。**これは craft ではなく invariant 1 である。**F5 の軽微6件も同じバッチで。
2. **R6/R11 が最重量**：紙の七状態を `【】` として本文に入れ、状態1と最終画を同一構図にする。他の修正はこの上に乗る。
3. **R2/R3/R8 は同じ削除作業**：主題の音読（L332）・メタ発言（L38/L163/L167/L192/L278）・語り手の言い直し・形容による悪役化（L243/L216）を一掃する。**足す作業はほぼ無い。削るだけである。**
4. **R4/R12 は一つの作業**：`⟨HELD⟩` を 9→3 に減らし、**すべて重い一文の後**に置き直す。認知は L161–163 に確定。
5. **R5 は挿入一箇所**：GL-70 を転回の直前に置き、L128 の種明かしを削る。**擁護と転回を接触させる。**
6. **R13/R10 は ACT_3 と ENDING**：同一供述の後半を足し、L338 を書き換え、L336 を ACT_3 に移す。
7. **R15 は最後**：L126／L234／L300／L210／appellant-appellee／引用の壁を直してから、**通しで音読して読了を記録する。**
8. **HOOK の 8秒 vs 48秒（§4）を APR で決着させてから**、HOOK を最後に書く。
9. 台本確定後、**`mandatory_stills` を再導出する**（現行222点。R6 で七状態を追加したので**必ずずれる**）。

---

*v001 · 2026-08-04 · `PD_SCREENPLAY_STANDARD.v001.md` §16 に基づく人間レビュー。機械ゲート全緑の台本に対して PASS 3 / FAIL 12。*
