# EP65 · MARMET — 反証レビュー（RE-REVIEW）v001

**対象：** `episodes/_planning/EP65_marmet_script.en.v002.md`（371行・CRLF）
**基準：** `docs/PD_SCREENPLAY_STANDARD.v001.md` §16（R1〜R15）
**前提文書：** `EP65_marmet_FILM_BIBLE.v001.md` §19（v001 を 15項目中 11 FAIL と採点）／
`episodes/PD-2026-065-marmet/01_research/fact_recheck.v001.md`（NEEDS SOURCE 5件）／
`EP65_marmet_FACTS_LEDGER.v001.md`／`measurements/EP65_marmet_RAW.md`／`measurements/EP65_brown_remand_RAW.md`

> **このレビューの立場：** 「v002 は水準に達した」という主張を**反証しにいく**。
> 修理の追認はしない。**変更履歴は読まず、現在の本文だけを読んだ。**

---

## 0. 方法と、まず記録する事実

### 0.1 行番号について（fact_recheck の注記は現在の実体と合わない）

`fact_recheck.v001.md` §0 は「`Read` ツールでの表示は11行目以降 −2 ずれる」と書いている。
**現在のファイルではずれていない。** 実測：

| 参照 | fact_recheck の主張 | 実ファイル |
|---|---|---|
| 処分（三つの docket） | L335 | **L335** 一致 |
| Brown/Taylor の命令の状態 | L317 | **L317** 一致 |
| *these cases* の引用 | L323 | **L323** 一致 |

以下の行番号はすべて**ファイル自身の行**であり、fact_recheck の行番号と直接比較できる。

### 0.2 独立実測（自己申告値は採らない）

`scratchpad\ep65r_measure.py` / `ep65r_positions.py` で再計算した。

| 指標 | 実測 | 申告値 | 判定 |
|---|---|---|---|
| ナレーション語数 | **5,184** | fact_recheck「5,201」 | 帯 [5100,5600] 内。ただし**17語の食い違い**（抽出規則の差） |
| 短文（6語以下）比率 | **24.1%**（83/345） | — | 標準 20–35% 内 · PASS |
| 修辞疑問 | 1（0.19/1000語） | — | PASS |
| 二人称 | 1（0.19/1000語） | — | PASS |
| モデル総尺（176wpm・HOOK 8s） | **29:35** | 本文L9「**29:09**」／区分見出しの合計「**29:26**」／fact_recheck「**29:32**」 | **同一ファイルに尺の数字が4つある** |
| 92%線 | 27:13 | fact_recheck 27:11 | 一致 |
| 最後の新事実（L335）終端 | **27:06 ＝ 90.4%** | fact_recheck「27:03・8秒内側」 | 一致（余裕 1.6pt ≒ 28秒） |

**指摘0-A（NEW）：** 本文 L9 は「この稿の実測は **29:09**」と書くが、**同じファイルの区分見出しを足すと 29:26** に、
実測レート再計算では 29:35 になる。**台本が自分の尺について自分と矛盾している。** 26秒の幅は
`hook_added` や `runtime_band` の判定を左右しないが、「Windows are derived, not chosen」（L7）という
この稿の**方法宣言そのものが自分の本文で破られている**。L9 か区分見出しのどちらかは手置きである。

**指摘0-B（NEW）：** `EP65_marmet_CODEX_BATCH_A.v001.md` の219枚は **v001 の語数**で比例配分されている
（発注書 §4：ACT_1 932語 / ACT_2 1,020語 / ACT_3 971語）。**v002 の実測は 865 / 1,011 / 929。**
ACT_1 だけで 67語（‑7.2%）ずれている。spec `notes` と fact_recheck §10-6 が命じる
`mandatory_stills` 再導出は**まだ実行されていない**、という証拠がここにある。

---

## 1. §19 の 11 FAIL — 現在の本文で着地したか

### R2（主題を語り手が言う）→ **PARTIALLY**

指定された5箇所は**全部消えている**（機械照合：`Its own claim, for money` / `Take that apart` /
`That is in the document` / `ever likely to file` / `film exists to say` すべて 0件）。

**しかし削除は個別に当たっただけで、種類には当たっていない。** 同じ型が**6本**残っている。
うち**4本は v001 に同じ文で存在し**、§19 のリストに載っていなかったために生き延びた。

| v002 | 現在の文 | v001 | 種類 |
|---|---|---|---|
| **L90** | *"Any version of this story in which all three signed the same thing has already gone wrong, and the difference sits on the face of the opinion."* | v001 L93 同文 | §19 R3 型①（**他人の語り直しへの反論**）— 5本削って**6本目が残った** |
| **L188** | *"All of them. That word is the hinge of the case."* | v001 L195 同文 | 型③ 意味の言い切り |
| **L240** | *"Every word there is load-bearing, and the last clause is the savings clause from section 2 coming back to be paid."* | v001 L250 同文 | 「ここは重要です」の予告。削除された *"Now the sentence this film exists to say."* と同species |
| **L280** | *"The second move is the reason this case has an ending worth telling."* | v001 L295 同文 | **最も重い。**語り手が「ここからが本作の見どころ」と宣言している |
| **L296** | *"That sentence is built to fit through the savings clause."* | v001 L305 同文 | 起草意図の断定 |
| **L353** | *"Those are different sentences, and the distance between them is the case."* | v001 L256 *"The line between those two sentences is the whole federal law of arbitration, compressed."* | §19 が**削除を命じた文**。語が替わっただけで**機能は残った**（指示は「二文を並べれば足りる」） |

→ **R2 は解消していない。** L353 は §19 の指示に対する**形式的遵守・実質的不履行**である。

### R3（結論文を消しても観客が着くか）→ **PARTIALLY**

- 型①（他人の語り直し）：5本中5本削除 **RESOLVED**。ただし **L90 が同型で残存**（上表）。
- 型②：*"Take that apart slowly."* / *"Keep that distinction."* 削除 **RESOLVED**。
  *"Keep the second half. It comes back."*（L194）は §19 の指示どおり**残置** **RESOLVED**。
- 型③：*"That is a state supreme court telling the Supreme Court..."* → 削除。ただし
  **L148** *"Disingenuous. That is a state supreme court describing, in advance, an argument it expects to be made to it."* と
  **L302** *"That is a court accepting a result while declining to accept the reasoning, in the very document it was ordered to write."* で
  **"That is a court …ing" という同一構文が2回**残っている。
- **残置指定 L185 → v002 L184**（*"Misreading and disregarding. …One is error. The other is choice."*）**RESOLVED**。

### R4（認知は一箇所か）→ **RESOLVED**

⟨HELD⟩ は **L313 / L339 / L367 の3個のみ**（機械カウント）。認知は L308（*a modicum of bilaterality*）＋
L310 の callback ＋ L313 の沈黙に**一点集中している**（実測 82.1%）。
§19 が外せと言った L78/L109/L166/L201/L254/L301 の ⟨HELD⟩ はすべて消えた。
L110 の宣言（*"struck down its own state's protection before it did anything else"*）は
**L108 *"The first holding went against the patients."* に落とされた** — 指示どおり。

**ただし L280（上表）が「ここから本作の核心」と別の場所で宣言している。** 認知装置は一つだが、
**"核心の予告" は二つある。**

### R6（モチーフの状態変化）→ **PARTIALLY**（→ §3 と R11 で詳述）

七状態は**すべて本文に入った**（L36=1 / L44=2 / L70=3 / L86=4 / L102=5 / L214=5再 / L224=6 / L369=7）。
椅子のプラントも L62 に入った。**ここまでは着地している。**
**しかし順序が壊れ、ループが成立せず、第二のモチーフが走っている。**§3 参照。

### R8（悪役を作らない）→ **RESOLVED（例外1件）**

指定4箇所すべて処理済み。
- L15 *"Its own claim, for money."* → 削除 ✓
- L74 *"against the patient's side of the table"* → 段落ごと削除 ✓
- L132 *"in the worst week of a family's life"* → **L134 *"The other side does it a few times in a life."*** ✓（→ NS-4）
- L368 → 削除、ENDING は引用＋画で終わる ✓
- 残置指定 L331 → **L329 に健在** *"The forums named in the papers had stopped taking the kind of case the papers were sending them."* ✓

**例外（NEW）：L347** *"A form that sent every dispute to a private arbitrator, **except the single dispute the nursing home might want to bring itself**."*
Q-04 が隔離された理由は「*ever likely to file* は記録にない将来予測」だった。
**"might want to bring itself" は同じ species の、緩和されただけの述語である。**
`might` が付いたぶん弱いが、**法人の意図についての、記録にない推定**であることは変わらない。
§19 R1 がこの一文を主題の実演として褒めたために、隔離の論理が**この一文だけ免除されている。**

### R10（ENDINGに新事実ゼロ）→ **RESOLVED**

- (a) *"Just under three years"*：0件。**移設もされていない** ✓
- (b) Kanawha/Harrison 文：0件。`this time` 0件 ✓
- (c) *"when both reporters closed"* → **L359 *"when both opinions closed"*** ✓
- 最後の新事実は L335（90.4%）で閉じ、92%線（27:13）の**28秒手前**。**PASS。**

**ただし §12 の観点では未達（→ §3-a）。** ENDING の最終楽章（L359–L361・97.4–98.4%）は
**再フレームではなく手続きの要約**になった。標準 §12 の「✗ 出来事の要約」そのものである。

### R11（ENDINGは最初の画に戻るか）→ **NOT RESOLVED**

文字のループは健在（L20 `【OST: OTHER THAN CLAIMS TO COLLECT LATE PAYMENTS】` → L370 `【OST: OTHER THAN】`）。
**画のループは、書かれてはいるが成立しない。**§3-b で証拠を出す。

### R12（沈黙は三箇所）→ **RESOLVED**

9 → **3**。位置も指示どおり。
1. L313 — 認知（L308＋L310）の**直後**
2. L339 — 限界（L337 *"It hands the question back to the circuit courts and stops."*）の**直後**
3. L367 — 最終画（L369）の**直前**
「予告としての沈黙」は消えた。**この修理は完全に着地している。**

*（記録：無音は他に2つある。L62 `【plant, no narration, held 3s】` と L214 `【reset beat, 4s, no narration】`。
後者は §19 が明示的に許容した画の休符。前者は R6 の修理が新たに入れたもの。L5 の
「exactly three ⟨HELD⟩」は⟨HELD⟩記号については真だが、**設計された無音は実際には5つ**である。）*

### R13（矛盾を矛盾のまま）→ **RESOLVED**

- (a) L335 の非一様な処分は**維持**（35494 reversed and remanded / 35546 reversed and remanded / 35636 certified question answered）✓
- (b) ENDING は L361 で **2/1 に割って**述べ、平らにしていない ✓
- (c) reaffirm / modify の並置が **L284・L286・L288** に入った ✓
  > L284 *"And then, plainly: we otherwise reaffirm all of our discussion and holdings in Brown One."*
  > L286 *"And in the next paragraph: however, in light of the parties' additional briefs and arguments, we modify our conclusions in Brown One."*
  > L288 *"Both sentences are in the same opinion."*
  **原文照合済み：** Brown II の該当箇所は *"…we otherwise reaffirm all of our discussion and holdings in Brown I.\n\nHowever, in light of the parties' additional briefs and arguments, we modify our conclusions in Brown I."*
  **「次の段落」は事実として正しい**（文字間隔137字・段落境界あり）。註釈も付いていない。
  **この修理は正確で、しかも一番よく効いている。**

### R14（記録の沈黙を沈黙のまま）→ **RESOLVED（例外1件）**

- (a) *"worst week"* 0件 ✓
- (b) L142 は帰属付きになった：*"**The state court's finding, in Brown One:** people being admitted to long-term care facilities and their families have to sign admission contracts without time to comparison shop…"* ✓（原文照合済み）
- (c) *"not an oversight"* 0件。L74 は **一文だけ**：*"A five-page per curiam opinion is not a narrative."* ✓
- (d) *"read the agreement"* 0件 → L46 は事実のみ ✓
- (e) *"The kind that gets signed at a desk."* はナレーションから落ち、机は L62 の画にだけ出る ✓
- 最良部分（L60–L68）は**無傷で残っている** ✓

**例外（NEW）：L134**（→ NS-4）。**帰属の非対称。**
直前の L132 は *"Most patients, **the court wrote**, do not view the admission process as…"* と帰属を付けるのに、
**次の一文 L134 だけ帰属を落として語り手の声にしている。** 弱いほうに帰属を付け、
**レトリックとして強いほうを地の文にした。**⛔-04 の趣旨（州最高裁の理屈を映画の声にしない）に触れる。

### R15（音読）→ **NOT RESOLVED**

- (a) L40 の Clarksburg 二重名 → **修理済み** ✓（§19 の置き換え案どおり）
- (c) L105–107 の壁 → **修理済み** ✓（L110 の48語 → **L112 *"That is the rule it wrote."*（5語）** → L114 の44語）
- (b) **五桁の docket 三連は残っている。** L335：
  > *"Case number 35494, Brown: reversed and remanded. Case number 35546, Taylor: reversed and remanded. Case number 35636, Marchio: certified question answered."*
  §19 の指示は「**番号を落とし、名前で三つ並べる。docket を残すなら画のテロップに置く。耳に置かない。**」
  **実行されていない。** fact_recheck §5 D-02 は逆に「もしテロップに載せるなら」と書いており、
  **二つの上流文書が矛盾したまま、台本は §19 の指示に従っていない側に落ちている。**
- **音読の記録が存在しない。** 標準 §16 は「R15は省略しない」と明記。§19.1-6 は「二周目の完成後、
  通しで音読し、読了を記録する」と命じた。**記録は無い。**（本レビューも音読していない。§7 は代替である。）

---

## 2. fact_recheck の NEEDS SOURCE 5件

| ID | 現在の本文 | 判定 |
|---|---|---|
| **NS-2**（L96） | *"West Virginia's legislature had put that in the statute books in 1997. Whether it survived contact with a federal statute passed in 1925 was now a question for the state's highest court."* | **RESOLVED** — *"years before any of these three admissions"* は消え、提案された修理が**そのまま**入った |
| **NS-3**（L256） | *"It was not what the defendants had challenged."* | **RESOLVED** — 提案どおり。L152 と整合 |
| **NS-1**（L196） | *"— a line from a per curiam the Court had issued **that same Term**, itself quoting a case from 1985."* | **PARTIALLY・要注意** — *"weeks earlier"* は消えたが、**承認された修理は入っていない。**新しい未検証の時間主張が入った。※下記 |
| **NS-4**（L134） | *"The other side does it **a few times in a life**."* | **PARTIALLY** — 原文は *"People seek medical care in a nursing home for long-term treatment to heal, and do so **only a few times in life**."*（照合済み）。語は近づいたが、**(1) 帰属が無い**（L132 は付いている）、**(2) 主語がずれている** — 原文の主語は「医療を求める人＝患者」、台本の主語は「署名する側＝家族」 |
| **NS-5**（L274） | *"…in the decision **that followed Brown I**."* | **PARTIALLY・退行あり** — *"the reports call Brown Two"* は消えた。しかし※下記 |

**※ NS-1 について。** fact_recheck の提案修理は *"the term before"* だった。
**それは事実として誤りである。** SCOTUS capture の照合結果：*KPMG LLP v. Cocchi*, **565 U. S. ___ (2011)**、
*Marmet* は **565 U. S. 530 (2012)** — **同じ 565巻＝同じ Term**。台本の *"that same Term"* のほうが正しい。
ただし **capture はそれを一言も書いていない**（巻数からの推論である）。
**NS-1 は「未検証の主張が別の未検証の主張に置き換わった」状態**であり、閉じていない。
（なお capture には *"As this Court reaffirmed **last Term**"* が **Concepcion** に付いており、
台本 L198 *"decided the previous term"* はこちらを正しく使っている。）

**※ NS-5 について — 修理が新しい欠陥を作った。**
v002 全体で **`Brown One` が10回、`Brown I` が1回**。その1回が **L274、NS-5 の修理箇所**である。
音声にすると「ブラウン・**ワン**」が10回、「ブラウン・**アイ**（または ワン／ファースト）」が1回。
**表記統一が、修理によって崩れた。** 加えて *"the decision that followed Brown I"* は
「Brown I の**後に来た**判決」としか言っておらず、この映画がこれから20分扱う文書の名前を
**最後まで一度も与えない**（`Brown Two` は0件）。結果、L337 *"that opinion"*、L359 *"both opinions"* の
指示対象が耳では宙に浮く。

**未処理（fact_recheck E-56）：** *"Three families. **Two documents**."*（L90）と
*"Three families sued. **Three papers** were produced."*（L357）は**両方残っている**。
fact_recheck 自身が「耳では矛盾に聞こえる」と警告し repair 案を出したが、**適用されていない。**

---

## 3. 修理が持ち込んだ欠陥（本レビューの本体）

### a. 訂正された ENDING — **精度が、耳で追えないものを作った**

L359–L361（97.4%→98.4%・映画の最後の40秒）：

> **L359** *"Two questions were still standing when both opinions closed. Whether a paper that arbitrates a death and litigates a debt is lop-sided enough that a court should refuse to enforce it as written. And whether the family member who signed it had the authority to sign away anything at all."*
> **L361** *"Neither had been answered. **On the first**, the state court reversed the orders in Brown's case and Taylor's case and permitted the parties to raise and develop their arguments regarding unconscionability anew, and **in the third case** said only that the issue may be raised by the parties on remand. **On the second**, it declined to consider the argument, which should be considered by the trial court first."*

**欠陥1：序数が二系統、交互に鳴る。** 聞こえる順番は
**「第一の…」→「第三の事件では…」→「第二の…」**。
`first` と `second` は**問い**を数え、`third` は**事件**を数えている。
耳は序数の系統を切り替えられない。**「第一・第三・第二」は事故に聞こえる。**

**欠陥2：L361 は46語の一文で、この稿で 5番目に長い**（実測。40語超は全14文）。
しかも **ENDING 唯一の40語超**である。ACT の法文引用が長いのは原典だからだが、
**これは語り手の地の文であり、ENDING に置かれている。**

**欠陥3：ENDING の最終楽章が「再フレーム」から「手続きの要約」に変質した。**
標準 §12 の表は「✗ 出来事の要約 / ✓ 既出の事実が別の意味に見える」。
L359–L361 は**係属状態の説明**であって、意味の反転ではない。
v001 の欠陥（Q-01・郡名と *this time*）は消えたが、**その場所に入ったものが ENDING の仕事をしていない。**

**欠陥4：処分が四度目の説明になっている。** 同じ非一様処分が L128（ACT_2）→ L335（ACT_5）→ L361（ENDING）で
三度述べられ、L337 が要約する。**正確さのための反復が、余韻の尺を食っている。**

*（補足：R10 としては合格である。L361 の事実はすべて既出であり、新事実ではない。
壊れているのは事実ではなく**形**である。）*

### b. 七つの罫線状態 — **入ったが、ループが物理的に成立しない**

**b-1 順序が壊れている。** 標準 §5 は「状態の順序を**先に決めてから**台本を書く」、
FILM_BIBLE §3 は「登場順に固定する」と書く。v002 の実際の登場順は

**3 → 1 → 2 → 3 → 4 → 5 → 5 → 6 → 3 → 7**

**状態3が、状態1と2より先に出る。** L16 が HOOK を *"motif state 3, flash-forward"* と宣言しているので
意図的だが、その結果 §5 のマクロ・ループ（「状態1で始まり状態7で終わる／画は同じ・意味が反転」）は
**設計として置き換わってしまった。**

**b-2 「同じ画」が同じ画ではない。素材の実体で確認した。**

> **L16**（最初のカット）：*"R001 — a ballpoint pen lying across the ruled line at the foot of an admission form, and on that line one unreadable stroke of ink. **This exact frame returns as the last image of the film, empty.**"*
> **L369**（最後のカット）：*"motif state 7, final image: **the same frame as the first shot of the film** — the ruled line at the foot of an admission form, **the pen gone, the line empty. Beyond it on the desk, the second chair is still pushed in.**"*

`EP65_marmet_CODEX_BATCH_A.v001.md` §5 の R001 のプロンプト（実物）：

> *"A ballpoint pen lying across the ruled line at the foot of an admission form, and on that line one unreadable stroke of ink that does not resemble any letter, **seen from directly above at close range** in the flat grey light of a reception counter at four in the afternoon"*

**R001 は真上からの近接マクロである。** そのフレームに *"Beyond it on the desk, the second chair"* は**入らない。**
真上・近接で罫線の脚部を撮った画に、机の向こうの椅子は写らない。
**L369 は L16 が約束した「同じフレーム」として撮影不可能である。**
さらに L16 は *"This exact frame returns … empty"* と書くが、
**ペンが有る／無い、インクが有る／無い、椅子が入る／入らない** — 三点で違う。
**"exact frame" は文言として自己矛盾している。**

→ **R11 の是正は、言葉の上でだけ実行された。**§19 R11 の指示は「状態1と状態7で**同一構図を撮る**」だった。
現在の台本は**同一構図を宣言しているが、指定している中身が同一構図ではない。**

**b-3 第二のモチーフが走っている。** 標準 §5「モチーフは**一つ**。二つ置くと象徴が薄まる」。
FILM_BIBLE §3 も「椅子はモチーフではなく**一度きりのプラント**」と明記した。実際には——

| 空いた椅子の出現 | 出典 |
|---|---|
| HOOK 0:02（R002 *"the chair on the far side pushed neatly in"*） | 発注書 §5 |
| HOOK 0:06（R004 *"An empty upholstered armchair…"*） | 発注書 §5 |
| L62（2:47・3秒ホールド） | 台本 |
| L369（最終画） | 台本 |
| ACT_2 `R075` / ACT_5 `R176` / ENDING `R201` | 発注書 §5 回収表 |

**「一度きりのプラント」が7回出る。** しかも**HOOK の4カットのうち2カットが椅子系**である。
8秒のうち約4秒が第二モチーフに使われ、**罫線のモチーフが開幕で薄まっている。**

**b-4 人間の縦糸が、台本に一行も無い。**
FILM_BIBLE §2 は第三の役として **「机の向こう側の手」**（毎営業日これをする側）を置いた。
§10 も *"手の仕事：ペン、書式を回す手、クリップ、ファイルの背。制度は手で実行される"* と命じた。

**機械照合：v002 に `hand` は1回しか無く、それは L337 の動詞 *"It **hands** the question back"* である。**
`finger` `arm` `clerk` `staff` `someone` すべて **0件**。
七つの状態はすべて**行為者のいない受動描写**である（L102 *"the sheet turned face down and squared into a folder, the folder pushed home into a drawer"* — 誰が、が無い）。

→ **設計された三役のうち、主人公（罫線）と敵対者（仮定）はある。人間の縦糸だけが実装されていない。**

### c. ⟨HELD⟩ 9 → 3 — **副作用は見つからなかった**

三箇所とも「重い一文の**後**」にあり、予告としての沈黙は消えた（§1 R12）。
**転回（L212 *"must be vacated."*）に沈黙が無くなった**が、直後の L214 が4秒の reset beat であり、
実効的な間は残っている。**これは正しい設計変更である。欠陥は見つからない。**

### d. 施設の形容詞を削った結果 — **施設が「無い」のではない。しかし居ない**

**まず反証を試みて、失敗した部分を先に書く。** 施設は消えていない。

- `nursing home` は **30回**、`Marmet` は 5回、`Marchio` 12回、`arbitration` 50回。
- 施設側の主張は**最強の形で二度**鳴っている：ACT_3 全体（11:10–16:27・全尺の 17.9%）と、
  L264 *"Counsel for Marmet Health Care Center argued the reverse — that the 2011 decision had been wrong because there was insufficient evidence in the record to support a finding that the arbitration clause was unconscionable."*
- L134 前半 *"One side of that desk does this every working day."* は原文（*"as a routine course of doing business"*）に根拠がある。
- L146 の *disingenuous* 文（51語・この稿最長の引用）は帰属付き・過去形で、州最高裁の言葉として鳴る。

**したがって「施設に存在感が無い」という単純な指摘は成立しない。存在感は、法廷の中にある。**

**問題は別の場所にある。施設は「議論の当事者」としては強く居るが、「毎日この紙を回している組織」としては画に一度も居ない。**
b-4 のとおり**手が無い**。机（`desk` 5回）と椅子はあるが、**その向こうに人がいた形跡が画に一つも無い。**
FILM_BIBLE §2 が「悲劇は道徳ではなく設計にある」と書いたときの設計の実行者が、映像から消えている。
形容詞を削る作業が、**形容詞と一緒に行為者を削った。**

**その結果として起きること：** 罫線は誰かが引いたのではなく、勝手にそこにある物に見える。
CONTROLLING IDEA は「**署名させた側の設計**を実行する」だが、**「させた側」が画面に一度も現れない。**
主題の半分が、映像から欠けている。

---

## 4. 残存リスクの検証：L317 と L323 は隣接しているか

**していない。これは仮定の話ではなく、現在のファイルの状態である。**

fact_recheck §3.3 B-02 は次のように書いて **LOCKED** を出した：

> *"**L317 names only Brown's order and Taylor's order in the two sentences immediately before the quote**, so "these cases" resolves the way the source resolves it."*

**この前提は現在の本文で偽である。** 実体：

| 行 | 内容 | 位置 |
|---|---|---|
| **L317** | *"The circuit court's order in **Brown's case** is devoid of any findings of fact… **Taylor's** order had some findings of fact, but that court had never comprehensively analysed… There was no evidence to weigh, because nobody had been permitted to take any."* | 24:25–24:46 |
| L319 | *"Its own line for a record in that condition, from Brown One: without factual or legal findings, this Court is greatly at sea without a chart or compass."* | 24:46–24:56 |
| L321 | *"It also had a sentence of the Supreme Court's own to lean on. Claims of coercion, fraud, or unequal bargaining power … are best left for resolution in **specific cases**. **Specific cases** need facts. Given that position, the state court wrote, further development of the factual record by the parties is proper."* | 24:56–25:17 |
| **L323** | *"So it sent the question down rather than answering it. **We conclude the correct course is to remand these cases** to the circuit courts for the taking of evidence…"* | 25:17–25:32 |

**間に2段落・88語・約31秒ある。**「直前の二文」ではない。

**そして最悪の形で悪い。** L323 の *"these cases"* の**直近の複数形先行詞は L321 の "specific cases" である。**
しかも L321 は **"specific cases" を2回続けて鳴らしてから** L323 に渡す。

> *"…best left for resolution in **specific cases**. **Specific cases** need facts. … So it sent the question down rather than answering it. We conclude the correct course is to remand **these cases**…"*

**耳で聞くと、"these cases" は「今言った specific cases」に結び付く。**
Brown と Taylor に限定するスコープは、L317 の 31秒手前にあり、あいだに *Gilmer* 引用（他事件の一般論）が挟まっている。

**結論：** fact_recheck が「後の編集で分離したら壊れる」と警告したことは、**警告時点で既に壊れていた。**
（あるいは警告の後に L319/L321 が挿入された。どちらであっても現状は同じ。）

**分離すると何が壊れるか（＝いま壊れているもの）：**
1. *"these cases"* が Brown+Taylor から**三件全部**に広がって聞こえる。
2. その瞬間、**Marchio に証拠採取命令が出たことになる。** 出ていない。Brown II はマルキオには
   認証質問への回答を返しただけで、unconscionability は *"may be raised by the parties on remand"*（¶12）である。
3. これは Q-01（v001 最悪の事実欠陥）と**同じ誤り**であり、v002 は ENDING でそれを直した一方、
   **ACT_5 の引用で同じ誤りが耳から入る経路を開いたままにしている。**

**最小の修理（事実に触れない）：** L323 の頭を *"So it sent Brown's case and Taylor's case down rather than answering them."* にするか、
L321 を L317 の前へ移して L317→L323 を隣接させる。**どちらも語数は増えない。**

---

## 5. この話固有の罠 — 「形」は何を残すか

最高裁は vacate して差し戻した。有効とも言っていないし、誰にも仲裁を命じていない。
**台本はそう書いている。**L248（19:04）：

> *"The Supreme Court of the United States did not hold that any of these three arbitration clauses was valid. It did not order anyone to arbitrate anything. It did not decide whether these families could sue…"*

**これは免責文である。観客が持ち帰るのは形である。以下は形として反対を語っている。**

### 5-1 映画の**最初の台詞**（L18・0:08）

> ***"A family member signed one line on an admission form. Everything went to arbitration except claims to collect late payments owed by the patient."***

**二文の因果に聞こえる。「署名した。→ すべてが仲裁に行った。」過去形の完了である。**
`⛔-01` が名指しで隔離しているのは **「the families were forced into arbitration」** であり、
**この一文はその形をしている。** 意図は「紙の条項がそう定めていた」だが、
**台本はその枠（"under the form" / "the clause said"）を一語も与えていない。**
v001 L21 は *"Everything went to a private arbitrator except one category of claim"* だった。
**§19 は末尾の道徳（*Its own claim, for money.*）だけを削り、この主節には触れなかった。**
その結果、8秒のフックで最も強調される命題が、**この映画が20分かけて否定する命題**になっている。

### 5-2 映画の**最後の台詞**（L365・29:29・99.7%）

> ***"All disputes go to arbitration. Other than claims to collect late payments owed by the patient."***

**現在形。無主語。帰属なし。** 引用であることは画（`【callback: the carve-out】`）でしか示されない。
**耳で最後に残る文が「すべての紛争は仲裁に行く」である。**
FILM_BIBLE §12 が禁じた「家族は仲裁に送られた」は言っていない。**言っていないが、鳴っている。**

### 5-3 終盤の強調が非対称

| 位置 | 文 | 誰にとっての「無」か |
|---|---|---|
| 19:04（64.5%） | *"did not hold that any of these three arbitration clauses was valid"* | 施設にとっての無 |
| **27:06（91.6%）＋⟨HELD⟩** | *"**Nothing in that opinion holds these clauses unenforceable.** It hands the question back to the circuit courts and stops."* | **家族にとっての無** |
| 29:06–29:29（98.4%） | *"Neither had been answered…"* | **家族にとっての無** |

**映画の最後の三分の一で、「条項は無効とされなかった」は2回鳴り、「条項は有効ともされなかった」は0回鳴る。**
L337 は ACT_5 の締めであり、直後に ⟨HELD⟩ がある — **この稿で構造的に最も大きな位置の一つ**である。
そこに置かれた否定形が、**家族側の敗北の形をしている。**

**記録の中に対称形の材料はある。** L248 に既にある。
**問題は事実ではなく、配置である。**

### 5-4 最後の文字

L370 `【OST: OTHER THAN】` — 文が付かない断片で終わる。
**ループとしては良い。**だが 5-2 の直後に出るため、耳の「All disputes go to arbitration」と
目の「OTHER THAN」が合わさると、**残るのは「例外つきで、すべては仲裁へ」という一つの完成した命題**である。

**判定：この映画の形は、免責文が正しいまま、視聴者に「紙は生き残り、家族は法廷から出された」と持ち帰らせる。**
最も安い修理は L18 と L365 の**時制と主語**であり、事実の変更を一切伴わない。

---

## 6. R15 の代替 — **音声形式分析（音読ではない。音読はしていない。）**

> **これは R15 の履行ではなく代替である。** 標準 §16 は「声に出して読んだか」を問う。
> 本レビューは読んでいないし、読んだと主張しない。以下は**文字から機械的に導ける音声上の危険箇所**であり、
> **通しの音読と読了記録は依然として未履行である**（§1 R15）。

### 6-1 25語超・内部コンマ無し（実測4文）

| 行 | 語数 | 文 |
|---|---:|---|
| **L308** | **39** | *"On the substance of a term: substantive unconscionability may manifest itself in the form of an agreement requiring arbitration only for the claims of the weaker party but a choice of forums for the claims of the stronger party."* |
| **L300** | **45** | *"The Supreme Court — without elucidating how and why the FAA applies to negligence actions that arise subsequently and only incidentally to a contract containing an arbitration clause — summarily concluded that the holding was a categorical rule contrary to the terms and coverage of the FAA."* |
| L264 | 34 | *"Counsel for Marmet Health Care Center argued the reverse — that the 2011 decision had been wrong because there was insufficient evidence in the record to support a finding that the arbitration clause was unconscionable."* |
| L138 | 32 | *"We are hostile toward contracts of adhesion that are unconscionable and rely upon arbitration as an artifice to defraud a weaker party of rights clearly provided by the common law or statute."* |

**L308 が最悪である。理由は長さではなく位置。**
これは**この映画の認知（RECOGNITION）を運ぶ一文**（82.1%・⟨HELD⟩ の直前）であり、
39語・息継ぎ点ゼロ・`unconscionability`（8音節）を含み、
*"only for the claims of the weaker party"* と *"a choice of forums for the claims of the stronger party"* という
**対句が対句として聞こえるための間が、書かれていない。**
映画の一点集中の設計が、**その一文の呼吸設計だけ空欄になっている。**

**L300 は第一コンマまで45語**（実測最長）。ダッシュの挿入句が29語あり、
主語 *"The Supreme Court"* と述語 *"summarily concluded"* が **29語離れている。** 耳では主語が失われる。

### 6-2 第一コンマまで25語以上（＝息が続かない助走・実測10文）

L46(25) · L114(26) · **L138(32)** · L140(29) · L196(25) · L202(27) · L264(34) · **L292(32)** · **L300(45)** · **L308(39)**

L292 は *"On the first of them: the parties have not challenged our holding in Syllabus Point 11 of Brown One regarding the preemption of **section 15(c)** by **section 2** of the FAA, and we need not revisit it."*
— **一つの節に条番号が二つ**（15(c) と 2）、加えて *"Syllabus Point 11"*。三つの数字が息継ぎ無しで並ぶ。

### 6-3 五桁 docket 三連（L335・26:45–27:06）

> *"Case number **35494**, Brown: reversed and remanded. Case number **35546**, Taylor: reversed and remanded. Case number **35636**, Marchio: certified question answered."*

- **35494 / 35546 / 35636** — 5桁、いずれも「3-5-」で始まり、**第2・第3桁が 5/4, 5/5, 6/3** と近接。
  耳では三つとも「サーティファイブ・サウザンド・…」で始まり、**区別できない。**
- しかも**この段落は R13 の合格点**であり、非一様な処分を伝える映画唯一の場所である。
  **番号が耳を塞ぐことで、いちばん守りたい情報が守られない。**
- §19 R15(b) が明示した是正（番号を落として名前で並べる／docket は画へ）は**未実行**。
- 加えて L150 に **11-391 と 11-394** がある。**下一桁だけ違う二つの番号**で、これも耳では同一に聞こえる。

### 6-4 耳で混同する固有名詞

| 混同ペア | 実測 | 危険箇所 |
|---|---|---|
| **Marmet / Marchio** | Marmet 5回 · Marchio 12回 | **L38–L40 の三連**：*"Brown sued **Marmet** Health Care Center. Taylor sued **Marmet** Health Care Center. **Marchio** sued a nursing home in Clarksburg."* — 同じ「マー」で始まる語が3文連続。**3文目だけ別語であることが、耳では聞き分けにくい。** |
| **Brown（原告）/ Brown One（判決）** | Brown 26回 · Brown One 10回 | L276 *"we overrule Syllabus Point 21 of **Brown One**"* の直後に L282–L292 で *Brown One* が4回、そのあいだ L317 で *"**Brown's** case"*。**人と文書が同じ音で交互に来る。** |
| **Brown I / Brown One** | **Brown I 1回（L274）· Brown One 10回** | 表記が統一されていない（→ NS-5）。TTS は L274 だけ別に読む可能性が高い |
| **Syllabus Point 21 / Syllabus Point 11 / Part Two / section 2** | 21が2回・11が1回・Part Two 1回・section 2 が4回 | L276（Point 21）→ L292（Point 11 と section 2 が同一文）→ L226（Part Two）。**「トゥエンティワン」と「イレブン」、「パート・トゥー」と「セクション・トゥー」が同じ数分内に鳴る** |

### 6-5 定義前に使われる用語 / 説明が必要な語

| 語 | 初出 | 定義 | 空白 |
|---|---|---|---|
| `unconscionable` / `unconscionability`（計18回） | **L46（1:10頃）** *"an unconscionable contract of adhesion"* | **L136（9:20頃）** *"That is unconscionability. It is not a rule about arbitration. It is a rule about contracts."* | **約8分** |
| `per curiam`（6回） | L28 — **同じ文で定義**（*"an opinion issued by the Court with no author's name on it and no vote reported"*）| ✓ | 0 |
| `per curiam`（**名詞用法**） | **L196** *"a line from **a per curiam** the Court had issued that same Term"* | L28 は形容詞的にしか定義していない。**「一つの per curiam」＝一件の判決、という用法は定義されていない** | 未定義 |
| `Section 15(c)`（4回） | L46 | 括弧の読み方が台本に書かれていない（「フィフティーン・シー」か「セクション・フィフティーン・サブセクション・シー」か） | **音声形が未指定** |

### 6-6 意味が「聞こえない句読点」に依存する箇所

**L192 — この稿で最も明白な例。台本自身がコンマに言及している。**

> *"Valid, irrevocable, and enforceable. **Then a comma**, and an exception that decides everything that follows. Save upon such grounds as exist at law or in equity for the revocation of any contract."*

**聴者はコンマを聞けない。**「そこにコンマがある」と言われても、直前の文には既に2つコンマがあり、
**どのコンマのことか特定できない。** 画のテロップが無ければ、この一文は音声上ほぼ機能しない。

**L238 — 映画がその上に建っている一文（41語）。**

> *"On remand, the West Virginia court must consider whether, absent that general public policy, the arbitration clauses in Brown's case and Taylor's case are unenforceable under state common law principles that are **not specific to arbitration and pre-empted by the FAA**."*

末尾の *"not specific to arbitration and pre-empted by the FAA"* は
**"not" が "pre-empted" にも掛かるのか掛からないのか**で意味が逆になる（原典由来の有名な曖昧さ）。
台本は L240 で *"Every word there is load-bearing"* と述べるだけで**どちらとも解さない**（それ自体は §13 に忠実）。
だが**耳ではそもそも二通りに分岐していることが認識できない。** 目なら止まって読める。音では止まれない。

**引用境界が音声で示されない（構造的）。** fact_recheck の実測で
**ナレーションの 42.9%（2,257語）が検証済みの逐語引用**である。
v002 の本文には**引用符が一つも無い**（すべて地の文に流し込まれている）。
リードインのある箇所（L110 *"The reasoning was a rule the court stated for itself."*、L142 *"The state court's finding, in Brown One:"*）は良いが、
**L124** は *"From that the court drew the public policy that gave the case its shape."* の直後に48語の判示が続き、**終了位置の合図が無い。**
→ 耳では**州最高裁の言葉と語り手の言葉の境目が消える。**⛔-04 が禁じた
「州最高裁の理屈を映画の声にしない」は、**文字では守られ、音では守られない。**

### 6-7 40語以上の文（実測14件・全体の 4.1%）

L92(51) · L110(48) · L114(44) · L118(50) · L124(48) · L140(41) · **L146(51)** · L166(43) · **L190(59)** · L202(40) · L238(41) · L300(45) · L331(43) · **L361(46)**

13件は原典引用であり、§10 の「30語超を5語以下で切る」は各幕で満たされている（例：L110→**L112(5語)**→L114）。
**L361 だけが語り手の地の文であり、しかも ENDING にある**（→ §3-a）。
**L190（59語・最長）**は §2 の全文引用で、直後 L192 が受けているので構造は正しい。

### 6-8 追加：数え方が10分離れて食い違う（fact_recheck E-56・未処理）

L90 *"Three families. **Two documents**."*（4:50頃）と L357 *"Three families sued. **Three papers** were produced."*（28:20頃）。
片方は書式の種類、片方は物理的な紙。**どちらも正しく、耳では矛盾する。**
fact_recheck が repair 案（*"Three papers were signed."*）を出したが**適用されていない。**

---

## 7. R1〜R15 再判定（v002 に対して新規に）

| # | 判定 | 根拠（本文からの引用） |
|---|---|---|
| **R1** | **PASS** | 一文で言える：「署名は、署名した人ではなく、署名させた側の設計を実行する」。実演は L347 *"A form that sent every dispute to a private arbitrator, except the single dispute the nursing home might want to bring itself."* |
| **R2** | **FAIL** | 主題を言うのではなく、**主題の重要性を語り手が宣言する文が6本**。最重は **L280** *"The second move is the reason this case has an ending worth telling."* と **L353** *"Those are different sentences, and the distance between them is the case."*（§19 が削除を命じた文の言い換え）。他に L90 / L188 / L240 / L296 |
| **R3** | **FAIL** | 型①が **L90** *"Any version of this story in which all three signed the same thing has already gone wrong…"* で残存。型③の構文 *"That is a court …ing"* が **L148 / L302** で反復。5本削って型は残った |
| **R4** | **PASS** | ⟨HELD⟩ は L313 / L339 / L367 の3個のみ。認知は L308→L310→L313 に一点集中（82.1%）。*（例外：L280 が別の場所で「核心」を予告している — R2 に計上）* |
| **R5** | **PASS** | ACT_3（全尺の17.9%）が施設側の勝利を最強の形で通す。L206 *"Preempted. Preempted. Preempted. Preempted."* → L212 *"must be vacated."*。加えて L264 で施設側の反対主張も鳴らす |
| **R6** | **FAIL** | 七状態は本文に入ったが **(1)** 登場順が 3→1→2→3→4→5→5→6→3→7 で状態3が状態1より先、**(2)** 空いた椅子が7回出て第二モチーフになっている（HOOK 8秒のうち2カットが椅子系）、**(3)** 全状態に行為者がいない（`hand` の実出現は L337 の動詞1件のみ、`clerk`/`staff`/`someone` は0） |
| **R7** | **PASS** | 反復不能な細部は健在：L48 *"That order is one paragraph long."* / L68 *"named only in the caption"* / L88 マルキオの紙 / L319 *"greatly at sea without a chart or compass"* / L327 AAA 2003年1月1日・NAF *"Friday, July 24, 2009"*。`Sutphin` `Canoe` は0件（禁止遵守） |
| **R8** | **PASS（例外1）** | 形容による悪役化は4箇所とも解消。手本 L329 は無傷。**例外＝L347 *"the single dispute the nursing home might want to bring itself"***（Q-04 と同 species の、記録にない意図の推定） |
| **R9** | **PASS** | 縦に上がる：一段落の命令(L48) → 三件(L38) → 州内の全入所契約(L126) → Supremacy Clause(L210) → §2 後半(L192) → 「誰も証拠を取っていない」(L317)。統計は0件 |
| **R10** | **PASS** | 最後の新事実 L335 は **90.4%** で閉じる（92%線 27:13 に対し 27:06）。*"Just under three years"* / `this time` / 郡名は ENDING に0件 |
| **R11** | **FAIL** | 文字のループ（L20→L370）は成立。**画のループは成立しない。**L16 *"This exact frame returns as the last image of the film, empty."* に対し L369 は *"the pen gone, the line empty. **Beyond it on the desk, the second chair is still pushed in.**"*。R001 の実プロンプトは *"seen from directly above at close range"* — **真上近接マクロに机の向こうの椅子は写らない** |
| **R12** | **PASS** | 9→3。3つとも重い一文の直後（L313=認知後 / L339=限界後 / L367=最終画前）。予告としての沈黙は消滅 |
| **R13** | **PASS** | L335 の非一様処分維持、L361 も 2/1 に分割。L284/L286/L288 の reaffirm↔modify 並置は**原文で段落隣接を確認済み**、註釈なし |
| **R14** | **PASS（例外1）** | 4箇所の削除・帰属付けすべて着地。最良部分 L60–L68 無傷。**例外＝L134** *"The other side does it a few times in a life."* — 直前 L132 が *"the court wrote"* と帰属するのに、この一文だけ帰属を落とし、原文の主語（患者）を家族にずらしている |
| **R15** | **FAIL** | **通しの音読記録が存在しない**（標準 §16「R15は省略しない」）。§19 の3件のうち L40 と L105-107 は修理済み、**L335 の五桁三連は未修理**。§6 で列挙した音声上の破断（L308 の39語ノーコンマ認知文、L192 の「聞こえないコンマ」、`Brown I`/`Brown One` 混在、Marmet/Marchio 三連、引用境界の消失）はいずれも音では残らない |

**集計：PASS 10（うち例外付き2）／ FAIL 5。**（v001 は PASS 4 / FAIL 11）

---

## 8. 敵対的パス — 施設側に不公平だと攻撃するなら、どの三文か

| # | 引かれる文 | 支えはあるか |
|---|---|---|
| **1** | **L347** *"A form that sent every dispute to a private arbitrator, **except the single dispute the nursing home might want to bring itself**."* | **支えは半分。** 条項の文言（*other than claims to collect late payments owed by the patient*）は逐語で検証済み（MB-23）。**しかし「施設が持ち出したいと思うかもしれない唯一の紛争」は施設の意図についての推定であり、両 capture のどこにも無い。**Q-04 が同じ理由で隔離された。**この一文は隔離基準に触れており、しかも映画の主題文である。**攻撃はここに当たる |
| **2** | **L134** *"One side of that desk does this every working day. The other side does it a few times in a life."* | **前半は支えられる**（Brown II *"Nursing homes daily sign contracts with patients as a routine course of doing business."*）。**後半は帰属が落ちている。**原文は *"People seek medical care in a nursing home … and do so only a few times in life."* — **主語は患者であって署名した家族ではない。**「施設 対 家族」の対立構図を、語り手の声で、州最高裁の観察を借りて作っている、と読める |
| **3** | **L18**（映画の最初の台詞）*"A family member signed one line on an admission form. **Everything went to arbitration** except claims to collect late payments owed by the patient."* | **支えられない、というより逆向きに危うい。**これは施設に不利というより**事実として起きていないこと**を述べている（`⛔-01`：誰も仲裁に送られていない）。敵対的視聴者は「この映画は冒頭8秒で、起きなかったことを起きたと言った」と引用できる。**皮肉なことに、この一文は施設にとっても家族にとっても不正確である** |

**予備（4番手）：L329** *"The forums named in the papers had stopped taking the kind of case the papers were sending them."*
— 形容詞ゼロで、AAA/NAF の日付は逐語検証済み（E-52）。**支えられる。**
ただし「紙が送ろうとしていた」という現在進行の言い方は、施設が機能しない仲裁機関を意図的に指名したかのように響く。
原告側の主張として提示する余地はあるが、**現状は語り手の地の文**である。攻撃されれば守れるが、無料ではない。

---

## 9. VERDICT

> # **DOES NOT MEET IT — R1〜R15 のうち 5項目が不合格（R2 / R3 / R6 / R11 / R15）**

**v001 の PASS 4 / FAIL 11 から、PASS 10 / FAIL 5 へ。改善は本物である。**
R4・R12・R13 の三つは**完全に着地しており、R13(c) の reaffirm↔modify 並置は原文照合まで通っている。**
事実面では、fact_recheck が隔離した8件すべてが実際に消えており、確認した限り**新しい事実の誤りは1件も無い。**

**それでも水準に達していない理由は、以下が**すべて**未解決だからである。**

1. **R11 の是正が物理的に実行不能な形で書かれている。**（§3-b：R001 は真上近接マクロ。L369 の「同じフレーム」に椅子は入らない）
   — これは意見ではなく、素材プロンプトの実体で確認した事実である。
2. **モチーフが一つではない。**空いた椅子が7回出る（HOOK 8秒の半分を含む）。
3. **人間の縦糸が台本に一行も存在しない。**`hand` は動詞1件、`clerk`/`staff`/`someone` は0件。
   CONTROLLING IDEA の「署名させた側」が画面に一度も現れない。
4. **L317↔L323 は既に分離しており**（88語・31秒）、*"these cases"* の直近先行詞は L321 の *"specific cases"* である。
   fact_recheck の **B-02 LOCKED は偽の前提の上に立っている。**
5. **映画の最初の台詞と最後の台詞が、この映画の免責文と反対の形をしている。**
   L18 *"Everything went to arbitration"* ／ L365 *"All disputes go to arbitration."*
6. **R15 は音読記録が無く、L335 の五桁三連という §19 の明示指示が未実行。**
7. **修理された ENDING は事実として正しいが、序数が二系統で交錯し（第一→第三→第二）、46語の一文になり、
   §12 が禁じた「出来事の要約」に変質している。**

### 手を入れる順序（全部を一括で当てる。`feedback_no_wasted_cycles`）

| 優先 | 作業 | 語数への影響 |
|---:|---|---|
| 1 | **L16 と L369 の構図を一致させる**（どちらかを他方に合わせる。椅子を最終画から外すか、R001 を机の視点に変える）。**画の変更＝発注書 §5 の改訂を伴う** | 0 |
| 2 | **L18 と L365 の時制・帰属を直す**（例：*"Under that form, every dispute went to a private arbitrator — except…"* ／ 最終行を引用として立てる） | ±5語 |
| 3 | **L321 を L317 の前へ移す**（L317→L323 を隣接させる） | 0 |
| 4 | **L280 / L353 / L240 / L188 / L296 / L90 を削る** | **−90語前後** |
| 5 | **L335 の docket 三つを画へ移す**（§19 R15(b) の未実行分） | −9語 |
| 6 | **L361 を二文に割り、序数を一系統にする**（「第三の事件」を「マルキオの件」に） | ±0 |
| 7 | **L134 に帰属を付ける**／ L274 を `Brown One` に統一／ L357 を *"Three papers were signed."* に | +6語 |
| 8 | **L308 に息継ぎを入れる**（*"…only for the claims of the weaker party. And a choice of forums for the claims of the stronger party."*） | +2語 |
| 9 | **通しで音読し、読了を記録する**（R15） | — |
| 10 | **`mandatory_stills` を再導出**（§0-B：発注書は v001 語数で配分済み・ACT_1 で 67語ずれ） | — |

**削除が中心なので語数は 5,184 → 約 5,090 になり、契約帯の下限 5,100 を割る。**
不足分は **§6-6 で指摘した引用境界のリードイン**（「州最高裁はこう書いた」型の短い帰属句）で埋めるのが正しい。
**説明では埋めない。帰属で埋める。**——それは同時に ⛔-04 の音声上の穴も塞ぐ。

---

*v001 · 2026-08-04 · 反証レビュー。実測は `ep65r_measure.py` / `ep65r_positions.py`、
原文照合は `measurements/EP65_marmet_RAW.md`・`measurements/EP65_brown_remand_RAW.md`・
`EP65_marmet_CODEX_BATCH_A.v001.md` §5 に対して直接おこなった。音読は実施していない（§6 は代替である）。*
