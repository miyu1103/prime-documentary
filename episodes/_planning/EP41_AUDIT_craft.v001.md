# EP41 (thompson) — CRAFT AUDIT v001
### 対象: `EP41_thompson_script.en.v001.md` / 基準: パルムドール級（カンヌ審査員レンズ・甘くしない）
### 方式: 実機診断のみ（台本は書き換えていない）。数値はすべて下記 evidence の実出力に基づく。

---

## 総評（先に結論）

- **映画の語り: 3.5 / 5。** 職業水準を明確に超える、抑制の効いた散文。だが「パルムドール級=映画」の棒尺で測ると、**(1) HOOKで全プロットを要約してしまい「シーン」でなく「あらすじ」で開く、(2) フレーム後は1回の時間折り(Deegan tease)を除き完全順行、(3) 第4幕でBrady解説が公民の授業に落ちる、(4) 締めが汎用の動員レトリック** — この4点が「優れたテレビ」から「映画」への一線を越えさせていない。落差（14年→処刑1ヶ月前の発見→$14M→5-4で全額消滅）の設計自体は正しく、最強事実は短く置けている。伸びしろは構成の大胆さと第4幕の脱・説明。
- **AI臭: 禁止句0件（クリーン）。だが構造的テクスチャの残滓が実測で複数。** 最重量は **第4幕L120の "It is… It may be… It is…" 三連アナフォラ**（作者が第2幕で解体したはずのIt-アナフォラが第4幕で再発）。ナレ全体で**文頭 "It " が14回**という地の癖も検出。

---

## EVIDENCE（実行コマンドと実出力）

### E1. 禁止句（単語境界 `\b`, 大小無視）— 全て0件
```bash
$ for p in '\bHere is' '\bIt is worth noting' "\bIt's important to" "\bLet's" '\bdelve' '\btapestry' '\bIn a world'; do grep -niE "$p" "$F"; done
# 全パターン (no match)
$ grep -niE 'not just [^,.]+,? but' "$F"   # → (no match)
$ grep -niE 'not only .* but' "$F"          # → (no match)
```
→ **AI常套句・"not just X but Y"・"not only…but" いずれも0件。** 語彙レベルのAI臭はクリーン。

### E2. 文長分布（ナレ地の文のみ, 163文 / 1,925語）
```
mean 11.81 / median 9 / stdev 8.54(pop) / min 1 / max 40
histogram(bucket=5): 0-4:34  5-9:51  10-14:28  15-19:18  20-24:13  25-29:14  30-34:3  35-39:1  40-44:1
極短文(<=4語): 34文 = 全体の20.9%
```
→ **stdev 8.5 は健全な非均等分布（AIのフラット文長ではない）。** ただし極短文が**20.9%**（作者も改稿ログ#10で「21%」と自認）。決め所の断片は効いているが、密度は上限ぎりぎり。

### E3. 「均等長 ±2語 が4文以上連続」— 該当2ブロック（＋緩条件で4ブロック）
```
RUN(±2, 4文) L46: [6,4,3,5] "…is type O." / "It was never his." / "The report existed." / "It sat in a file."
RUN(3語帯,5文) L96-98: [3,3,3,6,3] "Five to four." / "The Court reverses." / "Every dollar, gone." / "Understand what those five votes undid." / "Not a technicality."
RUN(3語帯,4文) L48-56: [6,6,3,3] "It stayed buried for fourteen years." / "Death row is a small place." / "A single cell." / "A steel door."
```
→ L46 と L96-98 は**意図された断片畳みかけ**だが、機械的等長が可聴域。特に L96-98 は5連続で3語帯に張り付く。

### E4. アナフォラ / 文頭Itの癖
```bash
$ sed -n '17,146p' "$F" | grep -oE '(^|[.!?] )It ' | wc -l   # → 14
```
- **L120 = "It is the promise… It may be… It is the difference…"（It三連アナフォラ・同一段落内）** ← 最重量。
- L46 "It was never his. / …It sat in a file." L110/L120/L140/L142 にも文頭It散在。
→ ナレ全体で**文頭 "It " が14回**。地の文のデフォルト主語が "It" に寄る、典型的な説明散文テクスチャ。

### E5. 否定対句 "Not X. Not Y." の残数
```
narration実数: L26 "Not the police." / L76 "Not by anyone's conscience," / L84 "Not guilty." /
               L98 "Not a technicality." / L122 "Not fourteen million. Not one dollar." = 約5〜6箇所
```
→ 改稿ログ#5「11回→半減」は達成。残置は概ね load-bearing。**警戒は L122 と L98 の近接**（第3〜4幕で否定断片が再クラスタ化）。

### E6. モチーフ反復
```
"fourteen years"(ナレ): L17,L48,L58,L60,L108 = 5回  + "fourteen winters" L58 + "fourteen million" L90,L122,L138
"eighteen years": L26,L86,L88,L98,L134 ほか
"walk(ed) free/back/into": L126,L134,L136（ENDING内で3回近接）
"the sound of …": L110 のみ（改稿で1回に削減済み・良）
rhetorical "?": L26(OP) と L140(ENDING) の2回のみ = callback対、連打なし（良）
```
→ "fourteen" 系はモチーフとして意図的だが**HOOK/第1/第2/第3幕で反復し密度高**。ENDINGの "walked free/back/into" 3連は無自覚反復の疑い。

---

## レンズ1: 映画の語り（審査員として・甘くしない）

### 1-1. HOOKが「シーン」でなく「あらすじ」で開いている（最重要・構成）
> L17: *A month before the State of Louisiana planned to execute him, an investigator found one sheet of paper. It had been hidden for fourteen years. It proved the blood was not his. The men who buried it were prosecutors. And when John Thompson tried to make them pay, the highest court in America said: no.*

判例名から入らず「1枚の紙」という物から入った点は正しい。だが5文で**物語の全アーク（発見→隠匿14年→血→検察→最高裁の否定）を要約**してしまい、16秒で結末まで割ってしまっている。これは promise 構造の flash-forward として弁護可能だが、**代償として第3幕の 5-4 反転がサプライズとして機能しない**（観客は15秒目に "said: no" を聞いている）。しかも最強の映像＝「処刑1ヶ月前、火事場のように古いファイルを漁る手が1枚を抜く」瞬間が、`an investigator found`という抽象主語で殺されている。
**直し:** HOOKを「要約」から「一つの動作の実況」に寄せる。例: 冒頭を *Thirty days. A man in a records room, going through boxes that were closed years ago. He pulls one sheet. On it: a blood type. Type B. The man scheduled to die in thirty days is Type O.* — 結末("said: no")は明かさず、**「紙が見つかった」までで止め、5-4は第3幕まで温存**。落差を売り切らない。

### 1-2. 反転の直後に法解説4段落を積み、gut-punchを希釈している（構成）
> L96: *Five to four. The Court reverses. Every dollar, gone.*
以降 L100(Thomas) → L102(過去4件) → L104(Scalia) → L108(Ginsburg) と**説明が4段続く**。最強の一撃(L96)を放った直後に、観客の感情がまだ立つ前から法論理の講義に入るため、L96の余韻が冷える。
**直し:** L96の後に**沈黙を1拍**（現状SILENCEはHOOKと第2幕の2箇所のみ。ここに3つ目を置く価値が最も高い）。Thomasの論理は要点を1段に圧縮し、Ginsburgの身体的beat（"let the ceiling of that cell turn gray at dawn"）を反転により近づけて、講義で下がった体温を人間で戻す。

### 1-3. 第4幕 Brady段落が「映画」から「公民の授業」へ落ちる（最も凡庸な段落）
> L120: *The rule those prosecutors broke has a name: Brady. It is the promise that the State must give you the evidence that could prove you innocent — the receipt, the test result, the name of the other suspect. It may be the single most important protection you have if you are ever accused of something you did not do. It is the difference between the twelve people in a jury box hearing everything, and hearing only what one office decides to let them hear.*

ここまで「見せて」きた語りが、**"It is… It may be… It is…" の解説アナフォラ**で一気に教科書化する（AI臭E4とも二重該当）。"the single most important protection you have" は形容の水増し。
**直し:** Bradyを定義で説明せず、**第1幕の血液型報告書という具体物に戻して定義を体現**させる。例: *That rule has a name: Brady. It is why the State was supposed to hand John Thompson one page — the lab report, type B — the morning his trial began. They didn't. Brady is that page, in the right hands or the wrong ones.* アナフォラのItを割り、抽象名詞（protection/difference）を物（the page）に置換。

### 1-4. 締めが個の物語から離れ、汎用の動員レトリックで閉じる（凡庸な段落）
> L144: *…Because the next case we tell could turn on your rights. Your freedom. Your name. And the more of us who understand how thin that line really is, the harder it becomes for anyone to cross it.*

"Your rights. Your freedom. Your name." は**三断片エスカレーション（tricolon）**、"how thin that line really is" は抽象、"the harder it becomes for anyone to cross it" は汎用の呼びかけ。Thompsonの固有の物語がここで**任意のチャンネルCTAに退行**する。パルムドール級の締めは主語を Thompson の身体に残したまま観客へ渡す。
**直し:** CTAを Thompson の具体（Resurrection After Exoneration / 取り戻した"声"）に接続。tricolonを崩し、"your name" の抽象を「あなたのファイルを持つ誰かの良心」という既出の主題像(L124/L140)へ回収する。

### 1-5. 反転を受けた地の文が数字を再述するだけで体温を下げる（凡庸な段落）
> L60: *John Thompson lived that for fourteen years on death row, eighteen behind bars in all. Outside, the world went on without him.*

直前 L58 が「鍵が1日2回座る音」「夜明けに天井が変わる正確な色」という**具体感覚の最高到達点**なのに、L60で**既出の数字(14/18)を再述**し、"Outside, the world went on without him" という**常套句**で締めて、せっかくの体温を平熱に戻している。ズームアウトして要約する動きはAI的でもある。
**直し:** L58の感覚で止め、L60を削るか、数字ではなく物で受ける。例: *That was fourteen winters. He counted them by the light.* 「world went on without him」は捨てる。

### 1-6. カード比喩が既製品（軽微だが該当）
> L86: *The same State that had spent eighteen years insisting he was a killer could not, when finally forced to show its whole hand, convince a single jury of it.*

"show its whole hand" は使い古したポーカー比喩で、この題材の重量に対して安い。**直し:** 比喩を捨て事実で殴る。例: *…could not, when the jury finally saw the blood type, keep a single one of them.*

**（良かった点・審査員として公平に）** 最強事実の短置は徹底されている（"Five to four." "Every dollar, gone." "Four." "No one did." "Not guilty."）。統計が人物の顔を追い越す旧欠点は解消（Ginsburgの"Four"は独房天井callbackで人に接地）。沈黙2箇所（L19/L66）は的確。「強盗を先に公判にかけ証言を封じた」という戦術的残酷さ(L40-42)は本作の白眉。感情語の名付けもほぼ回避できている。

---

## レンズ2: AI臭の検出（印象でなく実測）— 指摘12件・書き換え案付き

### A1.【最重量】第4幕 It-三連アナフォラ（E4）
`L120 "It is the promise… It may be… It is the difference…"`
- なぜAIっぽいか: LLMは定義・敷衍時に主語Itの並列でリズムを作る。作者は第2幕#57-59で同型を解体済みなのに第4幕で再発。同一段落内の同一構文3反復は機械的。
- 人間ならどう: レンズ1-3の直し参照。Itを割り、物（the page, type B）に着地。

### A2. ナレ地の文で文頭 "It " が14回（E4）
- なぜAIっぽいか: 説明散文のデフォルト主語がItに寄るのは生成テキストの地色。
- 人間なら: 半数を具体主語（the report / the page / that silence / Brady）に置換し、Itの反復を可聴域以下へ。

### A3. L96-98 の5文が3語帯に張り付く等長断片畳みかけ（E3）
`"Five to four." / "The Court reverses." / "Every dollar, gone." / "Understand what those five votes undid." / "Not a technicality."`
- なぜAIっぽいか: 同長断片の連鎖はAIの「劇的演出」既定リズム。決め所が5連続すると演出が定式に見える。
- 人間なら: 決めは "Five to four. Every dollar, gone." の2文に絞り、間に長い実況を1文挟んで谷を作る（"Understand…"の命令はレンズ1-2で沈黙に置換推奨）。

### A4. L46 の等長4連（E3）＋It反復
`"…type O." / "It was never his." / "The report existed." / "It sat in a file."`
- なぜAIっぽいか: 6-4-3-5語の均等断片＋It/Theの単調交替。
- 人間なら: *Type O. The lab had typed the blood years earlier — type B — and filed the page where no juror would ever see it.* 断片を1つの長文に呑ませ、リズムを非対称化。

### A5. 自己言及フレーム "our question / the answer to / the question we opened with"（E6の "?"＋grep）
`L92 "the answer to our question is yes." / L140 "So the question we opened with."`
- なぜAIっぽいか: 「冒頭の問いに戻る」と明示的にメタ宣言するのは構成の説明。人間の脚本は問いを再掲せず状況で想起させる。
- 人間なら: L92 を *For one moment, the answer was yes. You could make them pay.* とし "our question" を削除。L140 の "So the question we opened with." を落とし、問い自体だけを置く。

### A6. ENDING CTA の tricolon "Your rights. Your freedom. Your name."（E6）
- なぜAIっぽいか: 3断片の同型エスカレーションは生成CTAの定番装飾。
- 人間なら: レンズ1-4参照。断片を崩し Thompson の固有物へ回収。

### A7. "walked free / walked back / walked into" が ENDING内3回近接（E6）
`L126 walked back / L134 walked free / L136 walked into`
- なぜAIっぽいか: 同一動詞の無自覚な近接反復（モチーフ化の意図が薄い）。
- 人間なら: 少なくとも1つを別動作へ（stepped into daylight / came out）。反復するなら意図的callbackとして距離と形を揃える。

### A8. L60 のズームアウト要約＋常套句 "the world went on without him"（レンズ1-5と二重）
- なぜAIっぽいか: 感覚描写の直後に数字を再述し決まり文句で締める「まとめ」動作はAIの段落末リフレイン癖。
- 人間なら: 削るか、物で受ける（レンズ1-5）。

### A9. 否定断片の第3〜4幕クラスタ化（E5）
`L98 "Not a technicality." … L122 "Not fourteen million. Not one dollar."`
- なぜAIっぽいか: "Not X." 断片は強いが、近接反復すると定式に退行。
- 人間なら: L98 の "Not a technicality." を肯定文へ（*This was not a technicality — it was a jury's verdict, erased.* を1文に）、否定断片の決め所を L122 の一対に集約。

### A10. 形容水増し "the single most important protection you have"（L120）
- なぜAIっぽいか: 最上級＋抽象名詞での強調はLLMの説得デフォルト。抑制原則(強い事実ほど短く)に反する。
- 人間なら: 最上級を捨て機能で言う（*It is the one page between you and a cell.*）。

### A11. "in this one narrow, decisive way" 等の抽象副詞句（L140）
`"among the hardest in America to hold to account"`
- なぜAIっぽいか: 具体名詞を避け抽象副詞句で射程をぼかすのは生成散文の逃げ。
- 人間なら: 具体像（既出の "the lawyer in the good suit, with your future in a folder"）に完全に預け、抽象副詞句を削除。

### A12. "how thin that line really is / the harder it becomes for anyone to cross it"（L144）
- なぜAIっぽいか: 汎用の比喩(line)＋汎用の動員節。どのチャンネルの締めにも貼れる=固有性ゼロ。
- 人間なら: Thompson固有の帰結に置換（*The next page like his is being filed right now, by someone. Whether it ever reaches a jury is still, after all this, mostly up to them.*）。

---

## 最も重い指摘 3つ（優先順）

1. **HOOKが16秒で全プロットを要約 → 第3幕 5-4反転のサプライズを先に売り切っている（レンズ1-1 / 構成）。** flash-forwardは「紙が見つかった」までで止め、"said: no" と $14M→$0 の落差は第3幕まで温存する。落差を最大化するために最初に温存せよ。
2. **第4幕 Brady段落の "It is… It may be… It is…" 三連アナフォラ（レンズ1-3 / AI臭A1）。** 作者が第2幕で解体した同型が第4幕で再発し、映画が公民の授業に落ちる最大の一点。物（血液型報告書＝type B の1枚）に定義を体現させて解説を消す。
3. **反転(L96)直後に法解説4段を積み gut-punch を希釈（レンズ1-2 / AI臭A3）。** L96後に3つ目の沈黙を置き、majority論理を1段に圧縮、Ginsburgの身体beatを反転へ近づけて体温を戻す。

## 実測サマリ
- 禁止句: **0件**（クリーン）／ "not just X but Y": **0件**
- 文長: 163文, mean **11.81**, stdev **8.54**, 極短文 **20.9%**
- 均等長4文以上連続: **2ブロック**（L46, L96-98）＋緩条件2
- 文頭 "It ": ナレ地で **14回**（うち同段落内三連アナフォラ **1**）
- 否定断片 "Not X.": narration **約5-6**／自己言及フレーム **2**／ENDING "walked" 反復 **3**
- 映画の語り: **3.5 / 5**
