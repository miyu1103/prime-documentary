# EP62 · GREENE v. LINDSEY — 再レビュー v002（82箇所修正後・初回の再検査）

**対象:** `episodes/_planning/EP62_greene_script.en.v003.md`（ディスク上の現物・mtime 2026-08-04 21:40）
**基準:** `docs/PD_SCREENPLAY_STANDARD.v001.md` §15（即失格10行）・§16（R1–R15）・§16.5（HOOK 8秒・オーナー決定）・§12（92%以降に新事実を置かない [MUST]）
**設計:** `episodes/_planning/EP62_greene_FILM_BIBLE.v001.md`
**一次資料:** `episodes/_planning/measurements/EP62_greene_RAW.md`（456 U.S. 444 の全文2コピー）
**契約:** `episodes/PD-2026-062-greene/episode_spec.v001.json`
**先行3件（再照合対象）:** `EP62_greene_CRAFT_REVIEW.v001.md`(12 FAIL) · `EP62_greene_REREVIEW.v001.md`(21件・DOES NOT MEET IT) · `EP62_greene_SECOND_OPINION.v001.md`(HARD 16 / SOFT 29)
**プレートID変更:** `EP62_greene_ASSEMBLY_ADDENDUM.v001.md`（2026-08-04・ループは `G227` で閉じ、最後の画は `G231`）

> **正直な断り書き。** 本レビューは**読み上げを行っていない**。R15 は **NOT PERFORMED** とだけ書き、
> 代替分析でPASSを名乗ることはしない。それ以外の全行は、名指しした行を実際に開いて判定した。
> 引用は台本ファイルまたは `EP62_greene_RAW.md` から取り出したものだけである。

---

## 0. 結論（一行）

**DOES NOT MEET IT ——ただし僅差で、原因は3点しかない。**

前回 v001 が挙げた21件は、**実害のあるものが全て消えている**。§15 の即失格10行は **0/10 該当**。
R1–R14 は **12 PASS / 1 FAIL**（R6）。一次資料照合58スパンは**全て一致**（後述 §1-C）。
残っているのは —— **(1)** モチーフ状態1が台本内で自己矛盾している（L25 対 L27）、
**(2)** §12 の [MUST]「92%以降に新事実なし」を ACT_5 の最後3ビートが破っており、
しかも台本ヘッダ L15 が**自分でそのロックを宣言している**、
**(3)** R15（音読）が未実施で、基準が「省略しない」と明記している —— の3点である。

前回からの改善幅は大きい。**これは酷評ではなく、あと2行の直しと1回の音読で届く、という報告である。**

---

## 1. 実測（計測器を明示する）

### 1-A. 語数・尺・区間ウィンドウ

ナレーション＝`##` 見出し配下の非空行のうち、見出し・罫線・太字メタ行・`【】`・`⟨HELD⟩` を除いたもの。
行内の `【】`／`⟨HELD⟩` は除去。英数字を含むトークンのみ語として数える。

| 区分 | ヘッダの申告 | 実測語数 | 実測秒(176wpm) | ヘッダのウィンドウ | 判定 |
|---|---:|---:|---:|---|---|
| HOOK | 25 | **25** | 8.5 | 0:00–0:09 | 一致 |
| OP | 25 | **25** | 8.5 | 0:09–0:17 | 一致 |
| ACT_1 | 1,057 | **1,055** | 359.7 | 0:17–6:17 (360s) | 一致 |
| ACT_2 | 608 | **607** | 206.9 | 6:17–9:45 (208s) | 一致 |
| ACT_3 | 853 | **853** | 290.8 | 9:45–14:35 (290s) | 一致 |
| ACT_4 | 842 | **840** | 286.4 | 14:35–19:22 (287s) | 一致 |
| ACT_5 | 1,645 | **1,643** | 560.1 | 19:22–28:43 (561s) | 一致 |
| ENDING | 195 | **195** | 66.5 | 28:43–29:50 (67s) | 一致 |
| **合計** | 5,250 | **5,243** | **29:47** | band 5,100–5,600 | **PASS** |

**v001 の Finding 0-A（「ウィンドウは再導出されたと書いてあるが実際は導出されていない」）は解消。**
区間ウィンドウは実測から1秒以内で一致する。総語数のみ7語ずれるが、これはハイフン語の数え方の差の範囲で、
`runtime_seconds` [1620,1920] にも `script_words` [5100,5600] にも影響しない。

### 1-B. §10（文のリズム）・§7（抑制）

| 項目 | 基準 | 実測 | 判定 |
|---|---|---:|---|
| 短文（6語以下）比率 | 20〜35% | **32.1%**（389文中125） | PASS |
| 語り手の修辞疑問 | ≤2/1000語 | **0**（`?` は5箇所すべて証言引用の内側 L149・L153） | PASS |
| 二人称 you/your | ≤8/1000語 | **2.10**（11回。うち5回は引用内） | PASS |
| `⟨HELD⟩` | 3・重い文の直後 | **3**（L169・L297・L365） | PASS |
| 各幕に「30語以上の助走→5語以下で切る」 | 最低1 | ACT_1:3 / ACT_2:3 / ACT_3:3 / ACT_4:3 / ACT_5:6 | PASS |

実例（実測で拾ったもの）:
L119 39語 → **"The ladder had one rung."** / L165 44語 → **"Well aware."** /
L193 36語 → **"Claim."** / L213 35語 → **"They lost."** / L219 48語 → **"That was 1909."**

### 1-C. 一次資料との逐語照合（58スパン）

`EP62_greene_RAW.md` に対し、正規化（カーリー引用符・全角ダッシュ・`*452` 形式のページ標識・
`§`→除去・角括弧補記の展開）後の部分文字列一致で58スパンを検査。**実質的な不一致ゼロ。**

機械が MISS を返した8件はすべて**台本側の意図的な口語化**であることを RAW を開いて確認した：

| MISS | 台本 | RAW | 判定 |
|---|---|---|---|
| L79 | "over sixteen years of age" | "over sixteen (16) years of age" | 口語化・可 |
| L111 | "posting follows forthwith" | 途中に脚注番号 `8` が挟まる | 可 |
| L119 / L273 / L289 | "section 454.030" | "§ 454.030" | 音読形・可 |
| L337 | "that Kentucky should adopt" | "that [Kentucky] should adopt" | 角括弧の展開・**正しい** |
| L187 | "We always put them up high." | 反対意見は "always put [the writs] up high"、多数意見 n.7 App.74 は "so we always put **them** up high" | **正しい**（供述者の原語） |
| L157 | "They would take them off." | "They would take [the writs] off." | 角括弧を代名詞に戻した。軽微（後述 F-08） |

固有事実も RAW で個別確認済み：Joseph Greene / Jefferson County Sheriff（RAW L38）・
*Weber* 169 F. 522 (1909)・"some 70 years earlier"（L39）・Argued February 23, 1982（L121）・
O'Connor with THE CHIEF JUSTICE and REHNQUIST（L156）・S. Carter Bacon = App. 80 = "probably a couple
of times" / Village West（L165）・Gilbert Brutscher（L165）・Antioch School of Law amici urging
affirmance（L172）・"The cost will be minimal"（L62）。

### 1-D. 契約・工程

`check_episode_spec.py --slug greene` = **valid**（223 mandatory_stills・`G227`–`G231` を含み、
廃止された `G206`/`G209`/`G226` を含まない）。`manifest.json` の `state` は **`script_review`**
（v001 の指摘どおり `script_verified` から巻き戻し済み）。

---

## 2. §15「即失格の条件」——10行を1行ずつ

| # | 条件 | 判定 | 根拠（行番号と現物） |
|---|---|---|---|
| 1 | 事実の捏造（日付・数字・名前・動機・内面） | **該当なし** | 58スパンを RAW と照合し一致（§1-C）。SECOND_OPINION の HARD 16件は**全件解消**（§4）。人物の内面・動機を述べる文はゼロ |
| 2 | 感情命令 | **該当なし** | `imagine` / `shockingly` / `picture this` = 全て 0 hit。二人称 2.10/1000。※ L67 *"Consider what a summary eviction actually requires"*、L81 *"Read it slowly"*、L83 *"Look at the middle step"* は分析的指示であって感情命令ではない |
| 3 | 説教 | **該当なし** | `we must` / `we should` / `we need to` = 0 hit |
| 4 | 真犯人当ての枠組み | **該当なし** | L51 で三人の主張、L111 で制度の崩れ、L165 で認知を先に開示する。§6 の「既知の破滅」型 |
| 5 | 沈黙している記録への声当て | **該当なし** | `must have` / `would have felt` / `no doubt` / `presumably` / `probably thought` = 全て 0 hit |
| 6 | 悪役の創作 | **該当なし** | L359 *"He did what the statute told him to do."* · L231 *"That is not a contradiction in the judge's logic."* · L61 家主は政府機関 · 反対意見を L303–L339 で最強の形で載せる |
| 7 | 語り手が結論を言う | **該当なし（最も僅差）** | CONTROLLING IDEA の文は台本に無い。語り手の断定は約10文まで減ったが、L323 *"The majority never proved the mails were better. It proved this door was worse."* と L349 *"What the case leaves is smaller than a rule and more durable than a remedy."* は観客の仕事を先取りしている。**失格ではないが、ここが唯一の余地**（F-10） |
| 8 | カテゴリだけの人物造形 | **該当なし** | L45 *"No ages. No jobs. No families."* —— 欠落そのものを主題にしている。FILM_BIBLE §2 の設計どおり |
| 9 | 数字の発明 | **該当なし** | L171 *"It did not write a percentage."*。作中の数値（11 States / 10 other States / 1909 / 1975 / 70 years / six months / sixteen）は全て RAW で確認済み |
| 10 | 隔離済み（Q-01〜Q-15）の主張の使用 | **該当なし** | 15件を個別照合。Q-01 現在法：narrator に `today` 0（L305 の "today" は反対意見の引用内）／Q-03 は L289 *"The Court did not ban posting."*／Q-05 は L299 *"What became of Linnie Lindsey, Barbara Hodgens and Pamela Ray is not in the opinion. It simply stops."*／Q-11 は L299 *"Affirmed does not mean three tenants walked out holding a key."*／Q-13 は L303 *"The opinion prints no tally of the votes on the other side."*／Q-10（Normet との混同）は L325 で事件名を出さず引用のみ |

**§15：0/10 該当。**

---

## 3. R1–R15（現物から新規に判定。旧判定は一切引き継がない）

| # | 問い | 判定 | 決め手となった行と引用 |
|---|---|---|---|
| **R1** | CONTROLLING IDEA を一文で言えるか | **PASS** | 「国家が『あなたに伝えた』と扱ってよいのは、その伝え方が実際に届いているときだけである」。L49（紙が貼られた瞬間に送達成立）→ L111（`posting follows forthwith`）→ L165（`well aware`）→ L273（転回）→ L363（*"That the paper would still be there."*）が全てこの一文の実演になっている |
| **R2** | その一文が台本に**書かれていない**か | **PASS** | 直訳文は無い。v001 が FAIL の根拠にした2件は消えている：旧L167 の解説文（*"The people responsible for the notice knew the notice did not stay put."*）は**削除**、旧L349 の副題対句（*"…the difference between what a procedure is written to do and what it was observed doing"*）も**削除**。近接するのは L231 *"Read the words of the law and it is. Read the depositions and it is not."* だが、これは対句であって主題文ではない |
| **R3** | 語り手の結論文を全部削っても観客は着くか | **PASS（残渣あり）** | v001 が挙げた16文のうち **9文が完全削除・4文が短縮**。残る断定は L221 *"The presumption was doing all the work."*、L241、L253、L281、L319、L323、L343、L349、L355。うち L121 *"The ladder had one rung."* は基準 §10 が模範として挙げる形そのもの。証拠連鎖（条文 → forthwith → 供述 → well aware → 地裁の自己矛盾 → 転回 → 限界）だけで観客は同じ結論に着く。残渣は F-10 |
| **R4** | 認知は**一箇所**か | **PASS** | v001 が「12行離れた二つの認知」と指摘した構造は残るが、**性質が変わった**。L161 は *"It came out of a deposition, from the men themselves. The Housing Authority, **one of them said**, had told the servers that the children would take the writs off."* ——**帰属付きの証拠**になった（旧文の断定 *"The Housing Authority's own staff had told…"* は削除）。L165 が *"The Court's summary of **all this** was one sentence"* と明示して前段を包摂し、L167 *"Well aware."* → L169 `⟨HELD⟩` に単独で落ちる。認知は一箇所 |
| **R5** | 転回の前に反対側を**最強の形**で述べたか | **PASS** | L129（58語・*"…constitute not only a constitutionally acceptable means of service — but indeed a singularly appropriate and effective way…"*）→ L131 *"Singularly appropriate and effective."* → L133 *"Many or perhaps most."* → L271（Mullane n.6 の所有者推定を逐語）→ L273 *"Then the turn. But whatever the efficacy of posting in many cases…"*。擁護してから覆す順序が保たれている |
| **R6** | モチーフの状態変化を順に言えるか | **FAIL** | 台本上の並びは正しい：L25(1)・L95(2)・L123(3・リセットビート)・L163(4)・L199(5)・L301(6)・L357(1へ回帰 `G227`)・L367(7 `G231`)。**しかし L25 と L27 が矛盾する**（F-01）。L25 は 【motif 1: the paper taped flat, **corners square**】、その2行下の L27 は *"G001 the sheet taped square to the painted door, **one corner lifted**"*。`G001` の実プロンプト（`CODEX_BATCH_A.v002.md` L174）も *"the lower left corner lifted a centimetre clear of the paint and holding there"*。**状態1が最初から状態2である。**七状態の最初の変化が画面に存在しない |
| **R7** | 各主要人物に反復不能な細部があるか | **PASS** | Carter Bacon = *"probably a couple of times"* / Village West（L153・L155）· Gilbert Brutscher = *"the six months I was working at it there was no occasion where I saw anyone tear the writs off of the door"*（L179・L183）· App.82 の供述者 = *"Oh, we had plenty of trouble."* / *"I would go back and tell them to put it back. They don't know. They didn't know."*（L147・L151）· App.74 の供述者 = *"so we always put them up high"*（L157・L187）· 地裁判事 = *"conditions had changed since Weber"* ＋ 1909年の推定（L219–L225）· O'Connor = *"unattended mailboxes are subject to plunder by thieves"*（L321） |
| **R8** | 悪役を作っていないか | **PASS** | L61 *"Their landlord was not a landlord."* · L231 *"That is not a contradiction in the judge's logic."* · L323 *"That is a real argument."*（反対意見に対して）· L359 *"He did what the statute told him to do."* |
| **R9** | 賭け金は縦（深さ）に上がっているか | **PASS** | L93 三つのドア → L213 *"it was inadequate on every door in the project, and on every door in every project served the same way"*（**"That was the theory of the class"** と明示・B25 の修正済み） → L315 *"At least eleven."* → L359 *"followed correctly from a single assumption."* |
| **R10** | ENDING に新事実がゼロか | **PASS** | ENDING（L349–L363・195語）を1文ずつ照合。L351 の証拠は ACT_3 既出、L353 の *"the three dissenting Justices said so"* は L303/L307 既出、L355 の梯子は L81/L121 既出、L359 の 1975年・writ・order of possession は L43/L51 既出。**新事実ゼロ。**ただし §12 の 92% [MUST] は ACT_5 側で破れている（F-02・下の別行） |
| **R11** | ENDING は最初の画に戻るか | **PASS** | L357 【callback: motif 1 again — **G227**, the paper taped flat and square, same framing and lens as G001 in the HOOK. The loop closes here, not on G230.】。L11 のヘッダ宣言（`G001` opens · `G227` returns it · `G231` is the last image）と一致。v001 の 8-B（`G209`＝素のドアで矛盾）は ADDENDUM の差し替えで**解消**。※ただし R6 の F-01 が「戻る先の状態1」の定義そのものを曖昧にしている |
| **R12** | 沈黙の位置を三つ言えるか | **PASS** | L169（認知 *"Well aware."* の直後）· L297（限界 *"…posted service accompanied by mail service is constitutionally preferable to posted service alone."* の直後）· L365（最終画 【motif 7】 の直前）。基準 §11 が指定する三箇所と完全に一致。L169 の直後を打ち消していた解説文は削除済み |
| **R13** | 矛盾する記録を、矛盾のまま出したか | **PASS（本作の最良部）** | L175 *"The testimony was not all one way, and the dissent said so directly."* · L183 *"Same job, opposite answers. The dissent does not say they worked the same buildings."* · L187 *"The majority quoted the first half. The dissent quoted the second."* · L225 *"Removed by other tenants, the District Court wrote — the depositions in the footnote had said children."*（v001 の残渣を**明示的に矛盾として提示**する形で解消） · L309 *"The District Court had called the same testimony undisputed."* · L355 *"The men who climbed it did not describe it the same way as each other."* |
| **R14** | 記録の沈黙を、沈黙のまま扱ったか | **PASS（軽微な残渣あり）** | L45 · L127 *"The opinion does not say what time of day the process servers came."*（旧 *"in daylight"* は**削除済み**・A12/F4 解消） · L173 *"The opinion names nothing else."* · L189 *"The opinion does not say where or when each of them worked."* · L197 *"Nobody ever tried that question. It never got that far."* · L299 · L303 · L359 *"the opinion does not say which"*。残渣は「the record」と「the opinion」の混用3箇所（F-07） |
| **R15** | 声に出して読んだか | **NOT PERFORMED** | 本レビューは読み上げを実施できない。基準 §16 は *"R15は省略しない"* と明記しており、**代替分析でPASSを名乗らない**。未実施のまま出荷判定はできない |

**R1–R14：PASS 12 / FAIL 1（R6）。R15：NOT PERFORMED。**

---

## 4. 先行3レビューの FAIL 指摘 —— 現物で消化を確認

### 4-A. CRAFT_REVIEW の12 FAIL

| R | v001 時点の判定 | v003（現在）の判定 | 現行の本文 |
|---|---|---|---|
| R2 | PARTIALLY | **解消** | 解説文 *"The people responsible for the notice knew…"* 削除。L167 は *"Well aware."* 単独 |
| R3 | NOT RESOLVED | **概ね解消** | 16文中9文削除・4文短縮（§3 R3） |
| R4 | PARTIALLY | **解消** | L161 に *"one of them said"* を付与、L165 で *"all this"* と包摂 |
| R5 | RESOLVED | **維持** | L129–L135 ＋ L271 → L273 |
| R6 | script PASS / package FAIL | **script FAIL（新規・F-01）／package 解消** | `G227`–`G231` 発注済み・状態7のプレート存在。ただし L25 対 L27 が矛盾 |
| R8 | RESOLVED | **維持** | — |
| R10 | RESOLVED + 残渣 | **解消** | 残渣だった *"smaller than its **reputation**"* は消え、L349 は *"smaller than a rule and more durable than a remedy"*（`reputation` の grep = 0 hit） |
| R11 | script PASS / package FAIL | **解消** | ADDENDUM で `G209`→`G227` に差し替え・`episode_spec` も更新済み |
| R12 | RESOLVED | **維持** | L169・L297・L365 |
| R13 | RESOLVED + 残渣 | **完全解消** | L225 が「children 対 other tenants」を明示的に対置 |
| R14 | PARTIALLY | **解消** | *"in daylight"* grep = **0 hit** |
| R15 | NOT RESOLVED | **未実施のまま** | 下記 F-04 |

### 4-B. REREVIEW v001 §9 の「変えなければならない21項目」

| # | 項目 | 判定 | 現行の本文（引用） |
|---|---|---|---|
| 1 | L51 重複文 | **解消** | L53 *"Speed is the point of it."* で停止。不出典の尾部 *"and the Commonwealth built the procedure accordingly"* も消滅 |
| 2 | L167 削除 | **解消** | L167 *"Well aware."* → L169 `⟨HELD⟩` → L171 *"And notice what the Court did not write."* |
| 3 | *"has governed notice ever since"* | **解消** | L259 *"It came from that 1950 case, Mullane, and it was already thirty-two years old"*（grep `governed notice` = 0） |
| 4 | *", in daylight,"* | **解消** | L83 *"That is a conversation on a doorstep, with a person who lives there."* |
| 5 | FLAG-1（Court の文を brief に帰属） | **解消** | L111 *"And then the **Court's own sentence**, the one that undoes it."* |
| 6 | FLAG-2（記録に無い2文） | **解消** | L161 *"It came out of a deposition, from the men themselves."* |
| 7 | FLAG-3（Brutscher の *that* 欠落） | **解消** | L177 *"I had been warned beforehand **that**, by Mr. Bacon, Carter Bacon, that he suspected…"*（RAW L166 と一致） |
| 8 | L191 の時制と欠落語 | **解消** | L193 *"They **claim** never to have seen **these** posted summonses. They **state** that they did not learn of the **eviction** proceedings … had been entered **against them**, and after their opportunity for appeal had lapsed."*。L195 *"Claim. State. Those are the Court's verbs, and the Court kept them."* が真になった |
| 9 | L231 の余分なコンマ・最上級・動詞欠け | **解消** | L233 は RAW 通りコンマ無し。*"the sharpest sentence"* は消滅。L233 冒頭 *"Its own decision **was** seventy years old and pointed the other way"*（動詞あり） |
| 10 | L125 の *not only* 破断 | **解消** | L129 は1文に統合：*"…constitute not only a constitutionally acceptable means of service — but indeed a singularly appropriate and effective way…"*。造語だった *"Singularly effective."* も L131 *"Singularly appropriate and effective."* に |
| 11 | GL-70 の二重掲載 | **解消** | ACT_2 側の引用は口語 L135 *"That instinct is old. You watch your own door."* に置換され、逐語は ACT_5 L271 の1回だけ |
| 12 | 引用の終わり位置 | **解消** | L271 *"**That is the 1950 case, in a footnote.** Then the body of the opinion drew the conclusion from it. Upon this understanding…"* |
| 13 | 自己言及3文（旧L189/227/245） | **解消** | L191 *"What the tenants themselves said was narrow."*／L229 は三段の反復に置換／L247＋L249【OST】に人名を移動 |
| 14 | n.9 の答えを郵便受けの段へ | **解消** | L321（mailbox）→ L323 *"Its answer to the mailbox came in a footnote, in one line. The dissent misconstrues the constitutional standard."*。Ferguson の段は L341 *"The majority's opinion does not answer that one."* で正しく閉じる |
| 15 | HOOK を4枚に・状態7を外す | **解消** | L27 は4カット（`G001`・`G002`・`G004`・`G005`）。`G003` は明示的に除外され *"it is the answer, and it belongs to ACT_3"*。`G004` のプロンプト（BATCH_A L180）は *"a single small pale rectangle of **paper** on a door far down the line"* ＝紙であって状態7ではない |
| 16 | ヘッダのウィンドウ再導出 | **解消** | §1-A で全区間1秒以内の一致を実測 |
| 17–20 | パッケージ側4件 | **一部解消** | `episode_spec` は 223件・新番号で valid。`G227`–`G231` 発注済み。**未解消は F-05**（BATCH_A の §4 プレート表・§5 のループ指示・§7 の枚数・L650 の F1 文言） |
| 21 | v004 発行・sweep 再実行・manifest 巻き戻し | **一部解消** | `manifest.state` = `script_review` に巻き戻し済み。**しかし v004 は発行されず、`fact_recheck.v001.md`(12:48) と `beats.v001.json`(12:22) は 21:40 の台本に対して未再実行**（F-03） |
| 4-J | v002 の構造ロック取り下げ | **解消** | L17 が再宣言し、**逸脱2件を名指しで開示**：*"Deviations: reset beat ≈25%, not 55–70% … callback 96%, not 70–90%"*。実測でも L123≈25.8%、L357≈96% |

### 4-C. SECOND_OPINION の HARD 16件

**16/16 解消。** 現行本文で確認した対応は以下（番号は SECOND_OPINION のもの）。

A1→L111（Court's own sentence）· A2→L171 *"It wrote a significant number of instances, and then, in quotation marks, not infrequently."*（順序が正） ·
A3→L171 *"The opinion never prints a rate of removal."* · A4→L183 · A5→L189 · A6→L45 *"Three names and a housing project."* ·
A7→L207 *"The three tenants had no way to reopen the evictions in the state courts."*（*"the system that had taken the apartments"* は消滅） ·
A8→L259 · A9→L217 *"granted judgment for the sheriff and his deputies"*・L249【OST】*"for the appellants"* ·
A10→L329 *"The majority answered that in a footnote, and the answer is the tightest sentence in the opinion."* ·
A11→L271 · A12→L83 · A13→L57 *"The deputy sheriffs are unnamed in the caption of the case — certain known and unknown Deputy Sheriffs. … Two of the men who did the work get their names back later, and only in the dissent."* ·
A14→L161 · A15→L323 ·
A16→HOOK L23 *"a piece of paper **fixed** to a door was service"*／ENDING L359 *"an officer **fixed** a writ to a door — by thumbtack, or adhesive tape, or other means; the opinion does not say which."*

### 4-D. SECOND_OPINION の SOFT 29件

**主要26件は解消。**確認した代表例：B1→L259 に *"and afford them an opportunity to present their objections"* を復旧／
B2・B3→L279 に *"Particularly where"* と assurance 節の全文／B4→L119 に目的語の全文／B5→L127 *"apparently"* 保持／
B6→L315 *"At least eleven."*／B7→L233 コンマ削除／B8→L187 *"We always put them up high."*／B9→L321 語順復旧／
B10→L307 *"and, by implication, that of at least 10 other States"*／**B11→ `women`/`she`/`her` の grep = 0 hit**（契約ロック達成）／
B12→L147 *"One deposition…"* L153 *"Another excerpt in the same footnote…"* L157 *"A third excerpt…"*（人数を数えない）／
B13→L49 *"Under the procedure…"*／B14→L51 *"when the writs of possession were served"*／B15→L81 *"post it somewhere conspicuous on the premises. In practice, the door."*／
B16→L83 *"lets the officer explain it"*／B17→L83 *"because of what it assumes"*／B18→L81 *"a family member over sixteen"*／
B19→L117 *"at whatever hour the one visit happened to fall"*／B21→L67 *"Whatever a person has to arrange…"*／B25→L213 *"That was the theory of the class"*／
B26→L237 *"also did the arithmetic"*／B27→削除／B28→L267 *"borrowing a line from a 1925 case"*／B29→L275・L279・L283 で全て Mullane に帰属。
順序系3件（L115 の *"had already refused"*、L337 の *"Earlier, in a footnote"*）も解消。

**未解消の SOFT 3件は F-06〜F-09。**

---

## 5. モチーフ整合性と ENDING（本依頼の指定検査）

### 5-A. 「同じドア、七つの状態」の内部整合

宣言は3箇所にあり、**互いに一致している**：

- L11（ヘッダ）: *"`G001` opens · `G227` returns it in the same framing · `G231` (state 7) is the last image."*
- L357（ENDING）: *"callback: motif 1 again — **G227** … The loop closes here, **not on G230**."*
- ADDENDUM §2-1: `G227`←`G206`（状態1の帰り）／`G231`←`G226`（状態7・最後の画）

`G230` は状態6（テープも消えた無地）で、L301 【motif 6: the door, nothing on it】 の受け皿。
**「G230 では閉じない」という註記は正しく、曖昧さを潰している。** ID の指定に矛盾は無い。

`episode_spec.v001.json` も `G227`–`G231` を含み、廃止された `G206`/`G209`/`G226` を含まない（実測）。
**v001 の 8-B（ループ画が逆）と 8-C（最後の画にプレートが無い）は解消済み。**

**ただし状態1の定義が台本内で割れている（F-01）。**

```
L25  【motif 1: the paper taped flat, corners square】
L27  【… G001 the sheet taped square to the painted door, one corner lifted …】
```

`G001` の実プロンプト（`CODEX_BATCH_A.v002.md` L174）：
> *"A blank sheet of plain paper taped square to a painted apartment door … **the lower left corner lifted a centimetre clear of the paint and holding there**"*

さらに `G227`（ループを閉じる画）のプロンプト（同 L955）：
> *"…the sheet PORTRAIT format with two short tabs of masking tape at its top corners only and **its lower edge just beginning to curl away**…"*

結果：**状態1（「手続きは完了した」）が最初から状態2（「完了していない」）を含む。**
FILM_BIBLE §3 の七状態の**最初の遷移が画面に存在しない**。L95 【motif 2: one corner lifted from the paint】 は
HOOK の1枚目と同じことを2度目に見せることになり、§5 の「最後の状態は最初の状態に戻る。二周目に意味が反転する」
というループの反転も鈍る。これが R6 を FAIL にした唯一の理由である。

### 5-B. ENDING は新事実を足していないか

ENDING（L349–L363・195語）を1文ずつ既出照合した結果、**新事実ゼロ**。

| ENDING の文 | 既出箇所 |
|---|---|
| L351 *"the evidence was a handful of men describing their own work, and one of them repeating what the Housing Authority had said"* | L145・L157・L161・L189 |
| L353 *"the three dissenting Justices said so"* | L303（三人）・L307（*scant and conflicting*） |
| L355 *"The statute described a ladder with three rungs. The men who climbed it did not describe it the same way as each other."* | L81・L91・L121・L175–L189 |
| L359 *"Somewhere in Louisville in 1975 … by thumbtack, or adhesive tape, or other means"* | L43（1975）・L103（n.1 の三手段）・L49（officer が貼る）・L51（writs of possession） |
| L363 *"That the paper would still be there."* | 敵対者＝仮定。基準 §12 が模範として挙げる形そのもの |

**R10 は PASS。** ENDING は要約ではなく再フレームになっている。

### 5-C. ただし §12 の [MUST]「92%以降に新事実を置かない」は破れている（F-02）

総語数 5,243 の 92% ＝ **語 4,824 ＝ 27:24**。実測では **L329 の途中**（累計 4,778→4,834）に落ちる。
つまり **L331 以降がすべて最終8%の内側**。そこに置かれているもの：

- **L331**（27:28〜）: *"There is one more thing the Court declined to do … whether an action was against a person or against a thing — in personam or in rem … As in Mullane, we decline to resolve the constitutional question…"*
  → `in rem` / `in personam` は **grep でこの行が初出**。作中で一度も触れていない論点を、残り2分20秒で新規に導入している。
- **L337**: *"Earlier, in a footnote, the dissent had already accused the majority of doing the very thing it disclaimed. The Court gives lipservice to…"*
  → 反対意見 n.2 の lipservice 弾劾は**ここが初出**（`lipservice` の grep = L337 のみ）。
- **L339**: *"…we have long since discarded the concept that due process authorizes courts to hold laws unconstitutional when they believe the legislature has acted unwisely."*
  → *Ferguson* の制度論も**ここが初出**（`unwisely` の grep = L339 のみ）。

そして台本ヘッダ **L15 が自分で** *"no new core fact after 92%"* とロックを宣言している。
**宣言したロックを本文が満たしていない。** これは趣味の問題ではなく [MUST] 違反であり、
v001 が「宣言だけ落として満たしたことにする」を批判した（4-J）のと同じ形の裏返しである。

---

## 6. 所見表

| id | R番号／§15行 | 判定 | 行 | 根拠（現物） | 何を変えるか |
|---|---|---|---|---|---|
| **F-01** | R6 · §5 モチーフ | **FAIL** | L25／L27（＋`BATCH_A` L174・L955） | L25 *"the paper taped flat, **corners square**"* 対 L27 *"G001 … **one corner lifted**"*。`G001` プロンプトも *"the lower left corner lifted a centimetre clear"*、`G227` も *"its lower edge just beginning to curl away"* | 状態1を真に平らにする。最小コスト＝**未生成の `G227` から *"and its lower edge just beginning to curl away"* を削る**＋**冒頭用に真に平らな1枚（`G241`）を追加発注**し、L27 の1枚目を `G241`、L95 の motif 2 を `G001` に割り当てる。台本側は L27 の *"one corner lifted"* を削るだけ |
| **F-02** | §12 [MUST]／ヘッダ L15 の宣言 | **FAIL** | L331・L337・L339（92%線＝語4,824＝27:24、L331 は語4,834＝27:28） | `in rem`/`in personam`・反対意見 n.2 の lipservice・*Ferguson* が**いずれも初出**で最終8%に入る | L331 を **L329 より前**（n.4 の反論より前、例えば L317 の【OST】直後）へ移す。L337–L341 も同様に前倒しするか、いずれかを削る。移動が嫌なら L15 の宣言を撤回して decision record に理由を残す（黙って落とすのは不可） |
| **F-03** | 工程（invariant 6 / rules 12） | **FAIL** | ファイル mtime | 82箇所を**再び v003 に上書き**。`v004` は存在しない。`fact_recheck.v001.md`=12:48、`beats.v001.json`=12:22 に対し台本=21:40。証明器が台本より9時間古い | **v004 として発行**し、`fact_recheck` の逐語sweepと `beats` を v004 に対して再実行。v001 §9-21 が指摘した「2語欠落が31語スパンに吸収されて誤 LOCKED になる」マージ規則も併せて締める |
| **F-04** | R15 | **NOT PERFORMED** | — | 本レビューでは音読できない。基準 §16 *"R15は省略しない"* | 下読みTTS（またはナレーターの仮録り）を1回通し、オーナーが聴く。ADDENDUM §6 も「4話とも未実施」と自認している |
| **F-05** | パッケージ（v001 §9-17〜20 の残り） | **未解消** | `CODEX_BATCH_A.v002.md` L129–140・L167–171・L647・L658・L858 | §4 のプレート配分表は**v002 語数のまま**（HOOK 142語／OP 51語／ENDING 292語／計 5,318語。v003 は 25／25／195／5,243）。§5 ENDING 見出しは *"28:20–30:00"*（v003 は 28:43–29:50）。L658 *"`G209` は `G001` と同じ構図でなければなりません。ここでループが閉じます"* は ADDENDUM に矛盾したまま残る。L650 に F1 の *"7〜8人の男"* が原文のまま残る（L906 の訂正表で打ち消してはいる）。L858 は *"225件"*、`episode_spec` の実数は **223** | §4 を v003 実測から再導出。§5 の `G209`/`G206` ループ指示と L650–653 のビートブロックを**書き換える**（Codex は1プロンプト＝1枚で読むので、矛盾が残っていると拾われる）。L858 を 223 に訂正。**L361 【the hand leaves frame; the walkway is empty】 に割り当てプレートが無い**ので併せて確定 |
| **F-06** | R14 · B24 | 軽微 | L61 | *"The body that started these proceedings was a government body — **Louisville's own** housing authority."* 判決文は *"the Housing Authority of Louisville"* としか書かず、市との関係を述べない | *"Louisville's housing authority"* |
| **F-07** | R14 · B20 | 軽微 | L145・L171・L189 | *"**The record** was made of depositions…"*／*"What **the record** supported was a description"*／*"That is the entire evidentiary base."* 本作が読んだのは**判決文**であって記録全体ではない | *"the opinion"* に統一するか、L189 は *"That is what the opinion prints."* |
| **F-08** | §15-1（極軽微） | 軽微 | L153・L157 | L157 は判決文の *"They would take **[the writs]** off."* を *"them"* に置換。L153 は App.80 の *"Q. You did? A. Uh-huh."* を無標で省略 | 角括弧の展開は許容範囲だが、引用の無標省略は避ける（`…` を置くか復元） |
| **F-09** | 論理の軽微な破れ | 軽微 | L75／L87 | L75 *"It is two sentences long and it is worth hearing **in full**"* の直後に読まれるのは第1文のみ。第2文は12行後の L87 *"There is one more sentence in section 454.030"* | *"worth hearing whole, in two parts"* 等に |
| **F-10** | R3 · §15-7 の余地 | 軽微 | L323・L343・L349・L355 | *"The majority never proved the mails were better. It proved this door was worse."*／*"That is where the two opinions stop talking to each other."*／*"What the case leaves is smaller than a rule and more durable than a remedy."*／*"…the Court chose the one made by the men who said the paper came off."* いずれも観客が組むべき判断を語り手が組んでいる | 必須ではない。切れば「クラス」寄りになる。4文とも削っても L319・L321・L351–L363 だけで同じ結論に着く |

**空振りに終わった検索（読者が上の重みを測れるように記録する）:**
`in daylight` 0 · `same doors` 0 · `shared address` 0 · `seven or eight` 0 · `reputation` 0 ·
`governed notice` 0 · `Reconstruction` 0 · `women`/`woman`/`she`/`her` **0** · `imagine` 0 ·
`shocking` 0 · `we must`/`we should`/`we need to` 0 · `must have`/`would have felt`/`no doubt`/`presumably` 0 ·
語り手の修辞疑問 0 · 発明された百分率 0 · 三人のその後への言及 0 · `forbidden_claims` 9行・`Q-01`〜`Q-15` の15行を個別再掃引して **全件クリア**。

---

## 7. 総合判定

# DOES NOT MEET IT

**ただし、v001 の「21件・9件が新規発見」という状態からは質的に別の段階に来ている。**

- **§15：0/10 該当。** 前2回で最も重かった事実問題（Brennan の文を brief に帰属・脚注を判旨と呼ぶ・
  *"same doors"* / *"different years"* / *"in daylight"*・*claim/state* の時制取り違え）は**全て消えている**。
  一次資料58スパンの照合で実質的不一致ゼロ。**この台本はもう「正確」を通過している。**
- **R1–R14：12 PASS / 1 FAIL。** R13（矛盾を矛盾のまま出す）と R12（沈黙の三箇所）は、
  基準が模範として書いた形にそのまま到達している。R5 の「擁護してから覆す」も崩れていない。
- 残るのは **3点だけ**である。

**水準に届かせるための最短の変更（これで全部）:**

1. **F-01** — `G227` のプロンプトから *"and its lower edge just beginning to curl away"* を削る。
   真に平らな状態1のプレートを1枚（`G241`）追加発注し、L27 の1枚目を差し替え、
   L27 の *"one corner lifted"* を削る（`G001` は L95 の motif 2 に回す）。
   **台本の変更は1行、発注は1枚。**
2. **F-02** — L331（in rem / in personam）と L337–L339（反対意見 n.2・*Ferguson*）を
   **92%線（語4,824・27:24）より前**へ移す。最も自然なのは L317 の【OST: the eleven States, listed】の直後。
   **移動のみ。1語も書き足さない。**
3. **F-04** — **音読を1回行う。** 基準が省略を禁じている唯一の項目であり、
   未実施のまま「水準を満たした」と書くことはできない。

**工程として併せて必要（作品の質ではなく規律の問題）:**

4. **F-03** — v004 として発行し、`fact_recheck` の sweep と `beats` を v004 に対して再実行する。
   82箇所の修正が3度目の上書きで v003 に入っており、証明器が台本より9時間古いままである。
5. **F-05** — `CODEX_BATCH_A.v002.md` の §4 プレート表・§5 の `G209` ループ指示・L650 の F1 文言・
   L858 の枚数を v003 と ADDENDUM に合わせる。L361 の【the hand leaves frame】にプレートを与える。

F-06〜F-10 は**出荷を止めない**。ただし F-10 の4文を切ると、この台本は §0 の「上手い」から
「クラス」の側へはっきり移る。判断はオーナーに委ねる。

---

*v002 · 2026-08-04 · `EP62_greene_script.en.v003.md`（mtime 21:40・82箇所修正後）に対する再レビュー。
語数・文統計・`⟨HELD⟩` 位置・92%線・逐語58スパンは全て当該ファイルとその一次資料 `EP62_greene_RAW.md` から
計算した。引用は名指しした行を開いて取り出した。**R15（音読）は実施しておらず、実施したとは主張しない。***
