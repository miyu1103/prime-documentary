# EP63 · CORREA v. HOSPITAL SAN FRANCISCO — FILM BIBLE v001

**Standard:** `docs/PD_SCREENPLAY_STANDARD.v001.md`（BINDING・2026-08-04）· `PD_ONE_PASS_PRODUCTION_SPEC.v2` 行15
**Case:** *Correa v. Hospital San Francisco*, 69 F.3d 1184 (1st Cir. 1995)
**Facts:** `EP63_correa_FACTS_LEDGER.v001.md`（177行・VERBATIM 105行）
**Contract:** `episodes/PD-2026-063-correa/episode_spec.v001.json`
**Images:** `EP63_correa_CODEX_BATCH_A.v001.md`（223枚・発注済み）
**Runtime:** 27–32分 · 5,100–5,600語 · HOOK は **8秒**（オーナー変更 2026-08-04）

> この文書は「何を語るか」ではなく「**なぜこの順で、この距離から語るか**」を決める。
> 事実は台帳が持つ。**ドラマは事実の上に組む。作らない。**

---

## 0. この文書は順番が逆に作られている（先に申告する）

正典 §17 の工程はこうである。

```
FACTS_LEDGER → FILM_BIBLE → SCRIPT 一周目 → 機械ゲート → §16 人間レビュー → SCRIPT 二周目 → HOOK
```

**EP63 では FILM_BIBLE を飛ばして SCRIPT が書かれた。**`EP63_correa_script.en.v001.md`（5,391語・機械ゲート全緑）は台帳から直接書かれている。正典 §17 の最後の一行はこう言っている——**「FILM_BIBLE 無しに台本を書き始めない。書けてしまうが、それは『正確』止まりになる。」**

実際そうなった。v001 は §0 の三水準でいえば「正確」と「上手い」の間にいる。事実の誤りは無い。掴みもある。**主題を語り手が口に出しており、認知が三箇所に散っており、反対側が最強の形で述べられていない。**これは書き手の怠慢ではなく、**設計文書が無い状態で書けば必ずこうなる**という構造の帰結である。

したがってこの文書は二つの仕事をする。

| | 仕事 | どこ |
|---|---|---|
| **Job 1** | この映画が**何であるか**を決める（本来なら台本の前にやる） | §1〜§12 |
| **Job 2** | 既存台本が正典 §16 のどこで水準に届いていないかを**証拠付きで**特定し、二周目の具体的な改稿指示を出す | **§19** |

**Job 2 のほうが価値が高い。**§1〜§12 は遡及的に書かれているぶん、既存台本を追認する誘惑が強い。§19 はその誘惑に対する解毒剤である。**「すでに全部優秀です」と書く設計書には価値が無い。**

---

## 1. CONTROLLING IDEA（この映画が持つ唯一の思想）

> **断らないことは、断ることの上位互換になり得る。**

正典 §1 が EP63 について既に確定させている一文である。**この文は映画の中で一度も口に出さない。**

**エンジンとして働く対句**（これも口に出さない）：

> **断るには、誰かが決めなければならない。呼ばないことには、誰の決定も要らない。**

これがこの事件のすべてである。拒否には行為者がいる。行為者がいれば、責任を負う者がいて、記録が残り、争える。**呼ばれなかったことには行為者がいない。**だから記録も残らず、誰も答えなくてよい。裁判所がこの事件に *constructive*（擬制的）という語を当てたのは、まさに「誰も何もしていないのに、したのと同じ結果になっている」ことを法が捕まえるためである。

**否定文テスト**（§1）：**「断らないことは、断ることより常に軽い」**——全シーンがこれへの反論として機能するか。

| シーン | 反論として機能するか |
|---|---|
| EMTALA の設計（carrot and stick・誰も命令されず、全員が支払われる） | ✓ 命令が無い制度は、不作為を捕まえられなければ空になる |
| 病院自身が書いた四つの規則 | ✓ 規則は「する」ことしか書いていない。「しない」を測る目盛りが無い |
| 記録が一枚も無い | ✓ 何もしなかったことは、何もしなかったという証拠を残さない |
| ninety-nine percent | ✓ 深さの梯子。制度の側の話である |
| **ACT_5 の放棄（waiver）** | ✓ **病院は、自分がやったのと同じやり方で負ける**（§5 参照。これが v001 に欠けている最大の構造） |

**ACT_5 が主題に奉仕していることに v001 は気づいていない。**病院は最良の抗弁を、否定されたのではなく、**一度も持ち出さなかったことで**失った。答弁書でも、日程協議でも、公判前協議でも、公判準備書面でも、二度の Rule 50(a) でも、評決書式への異議でも、**誰も「言わない」と決めていない。ただ言われなかった。**それは待合室で起きたことと同じ形をしている。

**この照応を語り手に説明させてはならない。**リズムと画で並べれば、観客が自分で見つける。見つけた瞬間がこの映画の最上の一秒である。

---

## 2. THE PROBLEM THIS FILM HAS, AND WHY IT IS THE FILM

主人公がいる——が、映せない。

Carmen Gloria Gonzalez Figueroa は 65歳、寡婦、高血圧の糖尿病患者。娘二人と息子一人、孫四人。孫たちの父（Felix）は彼女の五か月前に死んでいる。家族の一人は彼女を *the trunk of the family tree* と呼んだ。**これだけは判決文が書いている。**EP62 の三人と違い、彼女には輪郭がある。

しかし：

- 実在人物の肖像生成は禁止（不変条件11・Q-13・`forbidden_subjects`）
- 死の瞬間・急変・救命の描写は禁止（Q-04・`forbidden_subjects`）
- **そして「なぜ呼ばれなかったのか」は記録が答えない。**動機は認定されていない（Q-02）。受付係の内心は記録に無い（Q-07）。

つまり**この映画には、顔も、死も、理由も無い。**

凡庸な作り手はここで感情の語りで埋める。それは禁止であり、同時に不要である。**この三重の欠落こそが主題だからだ。**誰も彼女を見なかった。だから彼女の記録は無い。だから我々にも見えない。**形式が内容と一致している。**

| | |
|---|---|
| **主人公** | **白紙の整理券**（渡され、持たれ、置かれ、落ち、消える） |
| **敵対者** | **一つの仮定**（「順番が来れば呼ばれる」） |
| **人間の縦糸** | **番号を渡した職員**。悪人ではない。手だけが映る。顔も、性格も、内心も無い |

`forbidden_claims` は「受付係またはスタッフ個人の性格づけ」を明示的に禁じている。**これは法務上の制約ではなく作劇上の必須条件である。**悪意ある一人がいれば話は簡単になり、そして小さくなる（§9）。この事件が 30年後も引かれているのは、**誰も悪くないのに同じことが起きるから**である。

---

## 3. MOTIF — 白紙の整理券の八つの状態

**モチーフは一つ。**空席・空の椅子・空のカウンターは魅力的だが、**それは舞台であってモチーフではない。**二つ置くと象徴が薄まる（§5）。椅子は券が置かれる場所として存在する。

そして重要な設計上の解：**券の面には数字を焼かない。**`forbidden_subjects` は生成画像内の readable numerals を禁じている。これは制約ではなく**発見**である——**番号は紙の上ではなく、制度の中にしか存在しない。だから病院は一枚も出せなかった。**

したがって：

- **数字「47」「24」は、音（アテンダントの声・OST）と Remotion の文字レイヤーだけが持つ。**
- **紙は最初から最後まで白紙である。**

発注済みプレートに、この八状態はすでに存在する（`EP63_correa_CODEX_BATCH_A.v001.md`）。**台本がそれを置いていないだけである。**

| # | 状態 | プレート | 意味（言わない） |
|---|---|---|---|
| 1 | 壁の発券機から白い舌が一枚出ている | `C100` | 制度は誰にでも同じものを渡す |
| 2 | カウンターに同じ白紙の券が扇状に並ぶ | `C099` | ここまでは完全に平等である |
| 3 | 親指と人差し指の間に立つ一枚（近接） | `C001` | 一人の手の中に入った |
| 4 | 空いた座面に表を上にして置かれている | `C136` | 持ち主がそこにいない |
| 5 | 椅子の下の床に落ち、湿気で端が反っている | `C137` | 時間が経った。誰も知らない |
| 6 | **どこにも無い**（引き出し・棚・記録の不在） | ACT_3 の絵 | **渡された番号は、病院の紙の上に一度も存在しなかった** |
| 7 | 真上から見た空席の上の一枚 | `C207` → `C208`（券が消えた座面） | 退場は誰の決定でもない |
| 8 | **状態3に戻る**（`C001` を再使用） | `C001` | 二周目に意味が反転する |

**マクロ・ループ**：状態3（HOOK）→ 状態8（ENDING 最終画・同じ絵）。§5 の「最後の状態は最初の状態に戻る」。**新規プレート不要。**

**状態6が心臓である。**そしてこれは**画だけが言う**。ナレーションは AS-11 の範囲（"utter inability to produce any records"）を一歩も出てはならない。「番号はどこにも記録されていなかった」と**言えば**推論であり台帳外だが、**空の引き出しを見せれば**それは観客の推論になる。これが §7（語り手は知っていることより少なく言う）の実装である。

**プラント→ペイオフ距離**：状態1–3（HOOK〜ACT_1、0〜3分）→ 状態6（ACT_3、約16分）→ 状態8（ENDING、30分）。2分以上離す規則（§5）を大きく満たす。

**⛔ Q-14 との整合**：偽の診療記録・受付票を「本物として」生成することは禁止。**不在を映す。偽造を映さない。**台帳がわざわざこう書いている——*"the bitter irony available for free: the real point is that no record existed. Show absence, not a forgery."*

---

## 4. ARC — 五幕の中の三幕

| 幕 | 劇作上の役割 | 起きること | 距離 |
|---|---|---|---|
| HOOK 8s | 約束 | 白紙の券・空席の列・番号の出ていない表示。台詞は20〜25語 | 寄り |
| OP 20s | 契約 | 事件名と、既知の破滅（$700,000 は覆らなかった） | 引き |
| **ACT_1** | **設定** | 朝。争いのある証言。番号・保険証・1時の電話。そして死（他所で・医師の下で） | 中→寄り |
| **ACT_2** | 設定の拡大 | 七人の原告。$700,000。EMTALA の設計＝誰も命令されず、全員が支払われる | 引き |
| **ACT_3** | 証拠の反転（**認知ではない**） | 「適切な」は雲である。病院自身が書いた四つの規則。**記録が一枚も無い** | 中→寄り |
| **ACT_4** | **転回 → 認知** | 病院の主張を最強の形で。そして *spurious*。そして **constructive** | 中 |
| **ACT_5** | 解決の梯子 | 放棄 → 限界 → 金額の理由（**死ではなく待ち時間**） | 中→引き |
| ENDING | 余韻 | 新事実ゼロ。決めていないことの列挙 → 方法 → 番号へ戻る | 引き |

**賭け金は縦（深さ）に上げる**（§4.3）。横（被害の大きさ）には上げない。記録が支えない。

> **一つの番号 → 一つの待合室 → 病院が自分で書いた規則 → 全米の病院の九十九パーセント → 「断る」という概念そのもの**

最後の段が到達点である。*Constructive dumping is the hospital that never turns anybody away.*

---

## 5. TURN と RECOGNITION（この二つが映画の背骨）

**この二つを一箇所ずつ置く。**v001 の最大の欠陥はここが散っていることである（§19 R4）。

### TURN（転回・ペリペテイア）— ACT_4 冒頭・全体の約 64〜67%

**逆方向に十分進んでから折り返す**（§4.1）。**反論を最強の形で述べてから倒す。**

病院の言い分は、記録の中では実際に強い。そしてその強さは**判決文自身が供給している**：

- *"the thicket of conflicting testimony and the chasmal gaps in the direct evidence"*（CT-12）
- *"the evidence in this case is not particularly precise"* / *"the grays predominate here"*（HA-17）
- 病院の主張：伝えられたのは *"dizzy and nauseated"* だけだった（CR-08）
- 病院の証人である医師 Dr. Rojas の証言：胸痛は Hospmed 到着後まで出ていなかった（CR-27）
- 医療過誤の請求は却下され、控訴されていない＝**「診療が適切だったか」はもはや問題ではない**（PR-04）
- そして裁判所自身が認める：*"we recognize that an emergency room cannot serve everyone simultaneously"*（AS-15）
- 病院の主張：*"it gave the patient a number, and would have ministered to her had she waited"*（HA-08）

**ここで観客は「病院が勝つ」と思わなければならない。**列に並び、順番を待たず、自分の意思で出て行った人が、なぜ病院に七十万ドルを払わせられるのか。**この疑問が観客の中に立つまで、次へ進んではいけない。**

そして——

> **This contention is spurious.**

**この順序を崩さない。**（v001 は主張を述べる前に「straw man」「shrill ring of desperation」と語り手がラベルを貼っており、安い勝利になっている。§19 R5）

### RECOGNITION（認知・アナグノリシス）— ACT_4・全体の **70.6%**

> **EMTALA should be read to proscribe both actual and constructive dumping of patients.**

*Constructive.* 法が形式ではなく効果を見るときに使う語。この一語が鳴った瞬間、観客がそれまでの 21分で見てきたもの——白紙の券、空席、呼ばれた別の番号、一枚も無い記録——が**一つの名前を持つ**。

**認知は一箇所（§4.2）。**これがその一箇所である。

**したがって禁止事項が三つ生じる：**

1. **OP でこれを先取りしない。**v001 の OP 第三文 *"The number was simply never called."* は、開始 1分で主題を語り手が言っている。削る。
2. **ACT_3 の中盤反転を「認知」にしない。**`There was no record. Not a thin record. None.`（55.7%）は**証拠の反転**であって意味の反転ではない。契約の `mid reveal 45–60%` を満たすのはこちらで正しい。ただし主題の言葉を纏わせない。
3. **認知の直後に語り手が言い換えない。**v001 は 11行後に *"Nothing was refused. Everything was withheld."* と言い直している。**観客が到達した結論を語り手が回収してしまう。**削る。エコーは ENDING に一度だけ置く。

**⟨HELD⟩ はここに置く。**認知の直後（§11-1）。

---

## 6. THE REFUSALS（この映画が撮らないもの）

契約の `forbidden_subjects` / `forbidden_claims` は機械が読む。**ここに書くのは、それがなぜ作品を良くするか**である。

| 撮らない | 理由（法務ではなく作劇） |
|---|---|
| 死の瞬間・急変・心肺蘇生・救急カート・波形モニタ | この映画の緊張は**待合室**にあり、臨床にない。蘇生を映した瞬間、観客は「助かったか」を見に来る映画になり、**判決文が金を払わせたもの（待たされた時間）から目が離れる**。裁判所自身が sudden-death 事件と本件を区別している（DM-16） |
| 受付係の顔・表情・視線 | 顔が出た瞬間、観客は「悪い人」を探し始める（§9）。**この事件の要点は、誰も何も決めていないこと**である。悪意ある一人がいたほうが話は簡単になり、そして小さくなる |
| 保険証を見た人物が「判断する」演出 | Q-07。カードを検める**手**は映してよい。その人物が何を考えたかを示す画は、記録に無いものを画で言うことになる。**裁判所自身が動機を認定しなかった**（Q-02） |
| 券に焼かれた「47」 | 契約が禁じているだけでなく、**白紙のほうが強い**（§3）。番号は制度の中にしか無い。だから一枚も出てこなかった |
| 法廷内観・木槌・独房・手錠 | `forbidden_subjects`。加えて61話で焼き切れた絵であり、**この事件は法廷の絵で語る事件ではない**。舞台は待合室である。棚の実測でも `waiting room` は 61話で burn 0/24 — この register はまだ誰も使っていない |
| 「今日でも救急室では〜」型の現代接続 | RQ-04：**判決文に統計は一つも無い**。無い数字を出さないことが、この映画の説得力の唯一の源である |
| 遺族のその後 | RQ-05：記録が 1995年の公判で終わっている。**沈黙している記録に声を当てない**（§13） |
| 肩に置く手・涙・カウントダウンの時計 | `forbidden_subjects`。感情を**手続き**から奪う。一つも要らない |

---

## 7. REGISTER — 声の設計

**観客の実測**：93%男性・91%が55歳以上。**制度と権力の観客**である。真犯人当ての観客ではない。

- **判決記録の平明さ。**形容詞は事実が持つものだけ。*"blithely"* は裁判所の副詞であり、我々のものではない——v001 の `Blithely. That is the court's adverb, not ours.` は**この映画で最も規律の効いた三語**であり、二周目でも触らない。
- **最良の台詞は既に書かれている。**Selya の語彙をそのまま鳴らす：*"a high number and a cold shoulder"* / *"the thicket of conflicting testimony and the chasmal gaps"* / *"a mutable cloud which is always and never the same"* / *"esurient"* / *"locking the barn door long after the horse has bolted"*。**語り手はそこに何も足さない。**
- **感情命令ゼロ。**実測ゼロ件（v001 も達成している）。
- **修辞疑問**：1000語あたり2回まで。**実測 0.56回**（3回）。良好。
- **二人称**：1000語あたり8回まで。**実測 0.93回**（5回）。良好。
- **短文（6語以下）**：20〜35%。**実測 30.7%**。良好。
- **語り手が自分の映画について語らない。**v001 は *"this film"* / *"this episode"* を**7回**使っている（§19 R2）。判決記録の声は、自分が映画であることを知らない。

**⟨HELD⟩ は五箇所だけ**（§11・v001 は14箇所＝設計されていない）：

1. HOOK 最終カットの前
2. ACT_1・因果ロック（死は他所で起きた）の直後
3. ACT_3・限界の直後（*we need not decide whether mere negligence...*）
4. **ACT_4・認知の直後**（*constructive dumping* の後）
5. ENDING 最終画の前（*Forty-seven was never called.* の前）

---

## 8. RETENTION MAP（行16・再フックの位置）

実測：**半減42秒・離脱の山は80〜180秒。戦争は冒頭で決まる。**最大間隔150秒（30分尺の[MUST]）。

| 位置 | 仕掛け |
|---|---|
| 0:00–0:08 | HOOK。白紙の券・空席・出ていない番号表示。解決前で切る |
| 0:30 | 「病院は一度も断っていない。それでも七十万ドルを払った」——既知の破滅（§6） |
| 1:30 | 「番号は四十七。二時十五分に呼ばれたのは、二十四」——**反復不能な細部** |
| 3:00 | 争う二つの証言。「両者の間に立つ手段は、もう無い」 |
| 4:30 | 死。**そして即座に**「判決文はこれを病院のせいだと言っていない」——因果ロック |
| 6:00 | 一時の電話（プラント。回収は 21分） |
| 8:00 | 七人の原告と $700,000 の内訳 |
| 10:30 | EMTALA の設計：**誰も命令されない。全員が支払われる** |
| 13:00 | *"Appropriate" is one of the most wonderful weasel words in the dictionary* |
| **15:30** | **中盤反転（証拠）**：病院自身が書いた四つの規則 |
| **16:30** | **記録が一枚も無い**（`mid reveal 45–60%` を満たす。**認知ではない**） |
| 19:00 | *the grays predominate here*——リセット・ビート（空席に4秒） |
| **20:30** | **転回**：病院の主張を最強の形で。観客が「病院が勝つ」と思う |
| 21:30 | *This contention is spurious.* → 一時の電話が戻る |
| **22:00** | **認知**：*constructive dumping*（70.6%）→ ⟨HELD⟩ → 番号のコールバック |
| 24:00 | 放棄（waiver）。**病院は言わなかったことで負ける** |
| 26:30 | 金額の理由：*"the few remaining hours of her life"*——**死ではなく待ち時間** |
| 27:35 | ENDING。新事実ゼロ・再フレームのみ |

---

## 9. HOOK 設計（8秒・**最後に書く**）

**⚠ v001 の HOOK 節は既に stale である。**発注書 `EP63_correa_CODEX_BATCH_A.v001.md` L116–122 が明記している——オーナー変更（2026-08-04）により **HOOK は50秒の導入部ではなく、本編最強ビートの 2秒刻み flash-forward** になった。v001 の HOOK は **139語（約45秒）**あり、**8秒には物理的に入らない**。

**構造**：4〜5カット、各約2秒。本編で最も強い画。台詞は **20〜25語**（8秒÷実測 190wpm）。**説明しない。**問いだけ残す。

**約束と回収**（発注書 L124–130 に既に確定済み）：

| フックのカット | 何の約束か | 回収先 |
|---|---|---|
| `C001` 手の中の白紙の整理券 | 彼女が受け取った唯一のもの | `C136` `C137` `C207` / **ENDING 最終画で `C001` 再使用** |
| `C002` 空の待合椅子の列 | 二時間半 | `C138` `C163` `C210` |
| `C003` 何も出ていない番号表示 | 呼ばれなかった番号 | `C162` `C206` |
| `C004` 誰もいない受付カウンター | 誰も断らなかった | `C014` `C133` |
| `C005` 湿気で曇った救急入口の扉 | 中に入った、という事実だけ | `C197` `C209` |

**台詞の条件**：数字（47／24）を**一つだけ**鳴らす。主題語（*constructive* / 「断らない」）は**絶対に使わない**。事件名も出さない（OP の仕事）。

**書く順序**：本編二周目が固まった後。**フックが本編を決めるのではなく、本編がフックを決める。**

**v001 の HOOK 139語の行き先**：ほぼ全部が **ACT_1 に既に重複して存在する**（`In any event... assigned the patient a number, forty-seven` L52＝HOOK 第3段落／`After approximately one hour, Angel called Esther` L58＝HOOK 第4–5段落）。**重複していないのは四点だけ**——朝の症状（CR-02）・氏名（CR-01）・年齢と寡婦（PF-01）・「一時より前には中にいた」（CR-05）。**この四点を ACT_1 冒頭に戻す**（§19 R2-b）。

---

## 10. WHAT THE IMAGES MUST CARRY

語りが説明を降りる代わりに、画が論証を持つ。発注書 223枚はこの節に従属する。

- **同じ椅子・同じ券を、違う時間・違う状態で繰り返す。**画の反復が、時間経過と制度の反復を同時に言う。
- **人は後ろ姿・手・影のみ。**顔が出た瞬間、観客は「その人の物語」を探し始める。この映画にそれは無い（`people_plates_min: 10` は全て顔なし規則）。
- **institutional な空虚**：誰もいない受付、押し戻された椅子、届かない位置のハンドベル、黒いままの番号表示。**制度は人がいなくても動く。**
- **手の仕事**：券を取る手、カードを検める手、受話器。**制度は手で実行される。**内心は映さない。
- **absence の絵を、object の絵と同じ精度で作る**：空の引き出し、記入されていない棚、券が消えた座面。**状態6はこれだけで成立する。**
- **文字と数字は Remotion のタイポ層だけが持つ。**生成画像には一切焼かない（`forbidden_subjects`）。これは §3 の設計と一致しており、妥協ではない。
- **1991年のプエルトリコ**：湿度、ジャロジー窓、シーリングファン、褪せた institutional な淡緑とクリーム。**現代の病院の光を使わない。**

---

## 11. THE LINE THE FILM IS BUILT ON

> **"EMTALA should be read to proscribe both actual and constructive dumping of patients."**
> — AS-17 / 原文照合済み（`measurements/EP63_correa_RAW.md`）

**この一文に向かって全部が動く。**病院は一度も断っていない。それがこの事件の弁護ではなく、**この事件そのもの**である——というのは我々の解釈ではなく、**裁判所自身の理路**である。

---

## 12. WHAT THIS FILM IS NOT ALLOWED TO SAY

契約 `forbidden_claims` と台帳 §11 の全項目がここに拘束する。とくに：

- **因果ロック（絶対）**：「病院の遅延が彼女を殺した」「診てもらえていれば助かった」と**言わない・匂わせない・画で言わない**。死因は hypovolemic shock、**別の施設で、医師の管理下で**起きた。判決文が是認した損害は、**待たされた時間の苦痛（$200,000）と遺族の悲嘆（$500,000）**である（Q-03・DM-15）
- 「病院は彼女を追い返した」と言わない（Q-01）。**追い返していない。それがこの映画である**
- 「保険を理由に治療を拒んだ」と言わない（Q-02）。**動機は認定されていない**
- 「裁判所が dumping を認定した」と言わない（Q-08）。**陪審が screening 違反を認定し、控訴審がそれを *unimpugnable* と述べた。**別の文である
- 「移送は違法だと判断された」と言わない（Q-09）。**控訴審は脚注7で審査を明示的に見送っている**
- 「EMTALA は治療を保証する」と言わない（Q-10）。保証するのは screening と、緊急状態が見つかった場合の stabilisation だけ
- 「遺族が自分の悲嘆で訴えられると裁判所が決めた」と言わない（Q-11）。**放棄で処理された。決めていない**
- 「全米すべての病院が対象」と言わない（Q-12）。**ninety-nine は ninety-nine のまま**。出典の無い数字であることも裁判所の側の事実である
- 彼女の最期の描写を一行も足さない（Q-04・Q-05）
- 実在人物の顔を生成しない（Q-13）。偽の診療記録・法廷文書を生成しない（Q-14）

**沈黙している記録に声を当てない。**それがこの映画の品位であり、同時にこの映画の主題でもある。

---
---

# 19. CRAFT REVIEW — 既存台本が水準に届いていない箇所

**対象**：`EP63_correa_script.en.v001.md`（5,391語・機械ゲート全緑）
**基準**：`docs/PD_SCREENPLAY_STANDARD.v001.md` §16（R1〜R15）
**方法**：機械計測＋全文精読。行番号は v001 のもの。**全ての改稿案は ✓ または ✓ VERBATIM の台帳行にのみ依拠する。**

## 19.0 判定

| # | 問い | 判定 |
|---|---|---|
| R1 | CONTROLLING IDEA を一文で言えるか | **PASS** |
| R2 | その一文は台本に書かれて**いない**か | **FAIL** |
| R3 | 語り手の結論文を全部削っても観客は同じ結論に着くか | **FAIL** |
| R4 | 認知は一箇所か | **FAIL** |
| R5 | 転回の前に反対側を最強の形で述べたか | **FAIL** |
| R6 | モチーフの状態変化を順に言えるか | **FAIL** |
| R7 | 各主要人物に反復不能な細部があるか | **PASS** |
| R8 | 悪役を作っていないか | **FAIL** |
| R9 | 賭け金は縦（深さ）に上がっているか | **PASS** |
| R10 | ENDING に新事実がゼロか | **PASS** |
| R11 | ENDING は最初の画に戻るか | **PASS** |
| R12 | 沈黙の位置を三つ言えるか | **FAIL** |
| R13 | 矛盾する記録を矛盾のまま出したか | **PASS** |
| R14 | 記録の沈黙を沈黙のまま扱ったか | **FAIL** |
| R15 | 声に出して読んだか | **FAIL** |

**FAIL 9件（R2・R3・R4・R5・R6・R8・R12・R14・R15）／ PASS 6件（R1・R7・R9・R10・R11・R13）。**

内訳の性質：**R2〜R6 は「設計文書が無いまま書いた」ことの直接の帰結**（主題・認知・転回・モチーフはすべて台本より前に決めるべきもの）。**R8・R14 は規律の局所的な緩み**（二箇所の条件文崩れ・一箇所の未帰属引用）で、修正は各1〜2文。**R12・R15 は工程の未実施**（沈黙の設計と音読）。**事実の誤り・捏造・隔離済み主張の使用はゼロ。**§15 の即失格条件には一つも触れていない。

---

## R1 — CONTROLLING IDEA を一文で言えるか　**PASS**

言える（§1）。**断らないことは、断ることの上位互換になり得る。**否定文テストも全幕が通る（§1 の表）。**題材の選定そのものは正しい。**

---

## R2 — その一文は台本に書かれていないか　**FAIL**

**主題が四回、語り手の口から出ている。**そのうち一回は**開始 1分**（全体の 3.6%）である。

**証拠**

| 行 | 台詞 | 何が起きているか |
|---|---|---|
| L36（OP・3.6%） | *"The number was simply never called."* | **開始1分で機構を名指ししている。**観客が 22分かけて到達すべき結論を、語り手が先に言っている |
| L310（ACT_4・72.2%） | *"Nothing was refused. Everything was withheld."* | 認知（L299）の **11行後**。観客が到達した結論を語り手が回収している |
| L366（ACT_5・91.3%） | *"Not her death. The waiting."* | ここは良い（因果ロックの payoff）。ただし直前の二文が台無しにしている（R14 参照） |
| L398・L401（ENDING） | *"Nothing was refused. Nothing was said." / "Forty-seven was never called."* | **ここだけが正しい位置。**ループとして機能する |

**さらに：語り手が自分の映画について 7回語っている。**（正典 §7・§15-7）

```
L 77  "This film will not add to it."
L 79  "And here is the thing this episode is most likely to get wrong, so it gets said once, plainly, and early."
L 90  "The court chose those words with care, and so will this film."
L256  "...and it is why this film keeps saying what a jury could have found rather than what happened."
L264  "Now the argument this whole episode exists to examine."
L362  "The reason given for it is the sentence to carry out of this film."
L394  "...and this film has not invented one."
```

**これは倫理の表明であって作劇ではない。**判決記録の声は、自分が映画であることを知らない。L79 は最悪で、**制作用語（"this episode"）で観客に自作の失敗リスクを説明している。**フレームが完全に壊れる。

### 二周目の指示 R2

**R2-a｜L36 の第三文を削り、既知の破滅に置き換える**（§6 劇的アイロニー）

- 削る：`The number was simply never called.`
- 置く：`A jury awarded her family seven hundred thousand dollars, and the First Circuit did not reduce it by a dollar.`
- 根拠：PR-12（$700,000）・DM-19／CT-09（no remittitur, affirmed）
- 効果：主題の代わりに**結末**を先に渡す。観客は「なぜ？」を28分抱える。正典 §6 の「既知の破滅」型。

**R2-b｜L79 を全削除し、因果ロックの導入を一文にする**

- 削る（22語）：`And here is the thing this episode is most likely to get wrong, so it gets said once, plainly, and early.`
- 置く：`One thing about that death has to be said plainly, because the rest of this case depends on it.`
- L81–84 の本体（因果ロック）は**そのまま維持**。あれは正しい。

**R2-c｜L77 後半を削る**

- 削る：`This film will not add to it.`
- 残す：`That is the whole of what the record says about how she died.`
- 理由：**前半が事実で、後半は映画が自分を褒めている。**沈黙は沈黙のまま置けば効く（§7）。

**R2-d｜L90 の自己言及を削る**

- 現：`The court chose those words with care, and so will this film.`
- 後：`The court chose those words with care.`

**R2-e｜L256 の後半を削る**

- 現：`That is a modest thing to write while affirming a seven-hundred-thousand-dollar verdict, and it is why this film keeps saying what a jury could have found rather than what happened.`
- 後：`That is a modest thing to write while affirming a seven-hundred-thousand-dollar verdict.`

**R2-f｜L264 を書き換える**

- 現：`Now the argument this whole episode exists to examine.`
- 後：`The hospital had one more argument, and it was the one that should have worked.`
- （これは R5 の steelman ブロックの導入にもなる）

**R2-g｜L310 を全削除**

- 削る：`Nothing was refused. Everything was withheld.`
- 理由：**認知の 11行後に語り手が言い換えている。**同じ対句は ENDING L398 に一度だけ残す。

**R2-h｜L394 の末尾を削る**

- 現：`Nobody was shown to have looked at an insurance card and formed a judgment about the person holding it, and this film has not invented one.`
- 後：`Nobody was shown to have looked at an insurance card and formed a judgment about the person holding it.`

---

## R3 — 語り手の結論文を全部削っても、観客は同じ結論に着くか　**FAIL**

判定は主題ではなく**因果ロック**で落ちる。

**証拠**：因果ロック（「遅延は彼女を殺していない」）が**三回**語られている。

```
L 81-84  "The opinion never says the hospital's delay killed her. It never says she would have lived. ... It is about what happened while she was still sitting there."
L 366    "Not her death. The waiting."
L 388    "And it does not say that a wait killed a woman. It says a woman waited, unattended, and that the law had already promised her otherwise."
```

**三回言わなければならないのは、構造が逆を向いているからである。**「症状 → 待つ → 出て行く → 死ぬ」という順に事実を並べれば、観客は必ず因果を結ぶ。台本はそれを**語り手の否定文で毎回押し戻している。**これが「依存している」ということである。

**構造に運ばせる材料は既に台本の中にある**——ただし使われていない。

1. **L105**：`The malpractice claim did not survive. The district court dismissed it, and that ruling was never appealed. ... Whatever a doctor should or should not have done for Carmen Gonzalez was no longer the question.`（PR-04）
   ——**これが構造上の因果ロックである。**「医療として正しかったか」は法廷から降りている。
2. **L113 の内訳**：$200,000 は *on the decedent's account*、$500,000 は *for the pain, suffering, and mental anguish experienced by the survivors*（PR-10・PR-11）。
   ——**金の割り方そのものが、何に対して払われたかを言っている。**
3. **DM-15**：*"Due to the Hospital's failure to provide even the most rudimentary screening, Ms. Gonzalez spent the few remaining hours of her life in agony..."*
   ——裁判所自身が **screening の不在 → 苦痛**とだけ結んでおり、**死には結んでいない。**

### 二周目の指示 R3

**R3-a｜L105 を因果ロックの構造的支柱に昇格させる**

- 現在の位置（ACT_2 冒頭）はそのまま。ただし一文追加する：
  `From that point on, nobody in this case was arguing about whether she was treated well. Only about whether she was looked at.`
- 根拠：PR-04・PR-05（陪審に行ったのは EMTALA 二理論のみ）・AS-06（*EMTALA does not create a cause of action for medical malpractice*）。**新事実ゼロ。**

**R3-b｜L113 の金額提示を「内訳を先に、合計を後に」に組み替える**

- 現在：$200,000 →$500,000 → `Seven hundred thousand dollars in total.`
- 変更後も語は変えないが、**$200,000 が何に対するかを裁判所の語で先に置く**：
  `Two hundred thousand dollars on the decedent's account, payable to the heirs.` の直後に、ACT_5 の DM-15 への伏線として ⟨無音〉を置かず、そのまま $500,000 へ。**ACT_5 L360–366 が回収する。**
- （追加の語は不要。**プラント→ペイオフ距離は約 18分**で §5 の 2分規則を大きく満たす）

**R3-c｜L388 を削除する**

- 削る（全2文・約35語）：`And it does not say that a wait killed a woman. It says a woman waited, unattended, and that the law had already promised her otherwise.`
- 理由：**ACT_5 L366 の "Not her death. The waiting." が既に payoff である。**ENDING で三度目を言うのは、観客を信用していない。
- ENDING の「決めていないことの列挙」は四項目で終える（R10 の構成を参照）。

**この三つを入れると、L81–84 の一回だけで因果ロックが立つ。**

---

## R4 — 認知は一箇所か　**FAIL**

**三箇所に散っている。**

| 位置 | 台詞 | 何を主張しているか |
|---|---|---|
| L36（**3.6%**） | `The number was simply never called.` | 機構の名指し（＝主題） |
| L234（**55.7%**） | `There was no record. Not a thin record. None.` | 証拠の反転 |
| L299（**70.6%**） | `EMTALA should be read to proscribe both actual and constructive dumping of patients.` | 意味の反転 |
| L310（72.2%） | `Nothing was refused. Everything was withheld.` | 主題の言い換え |
| L366（91.3%） | `Not her death. The waiting.` | 因果ロックの payoff |

正典 §4.2：**「認知は一箇所。二つ置くと両方薄まる。」**現状は実質三つ（L36・L234・L299）が同格に鳴っている。

**なお契約の structural lock は `mid reveal 45–60%` と `primary reveal 65–85%` の**両方**を要求しており、これは §4.2 と衝突するように見える。衝突しない。**役割が違う。**

- **mid reveal（55.7%・L234）＝証拠の反転。**「病院は自分の規則を守った証拠を一枚も出せない」。これは**事実の発見**である。
- **primary reveal（70.6%・L299）＝認知。**「断らないという方法がある」。これは**意味の発見**である。

### 二周目の指示 R4

**R4-a｜認知を L299 に一点固定する。**⟨HELD⟩ をここに置く（現在は L296＝直前にある。**直後に移す**）。

**R4-b｜L36 を削る**（R2-a と同じ操作）。

**R4-c｜L234 周辺から主題語を外し、証拠の言葉だけにする。**

- 維持：`There was no record. Not a thin record. None.`（**これは優れている。触らない**）
- 維持：L236 `A hospital whose own rules demanded a written record of every visit could not produce one for a patient who had been inside it for two hours.`
- **追加しない。**現状ここに主題語は無い。**⟨HELD⟩ を L233 から外す**（§19 R12）ことで、認知との格の差をつける。

**R4-d｜L310 を削る**（R2-g と同じ操作）。**認知の直後に語り手が言い換えない。**

---

## R5 — 転回の前に、反対側を最強の形で述べたか　**FAIL**

**述べていない。しかも三回、主張を聞かせる前に語り手がラベルを貼っている。**

**証拠**

| 行 | 何が起きているか |
|---|---|
| L168–172 | 病院の第一主張（EMTALA 不適用）を提示 → **即座に** `The court's reply runs nine words. This argument has the shrill ring of desperation.` |
| L182 | `Then the straw man.` ——**主張を述べる前に語り手が「藁人形」と宣言している** |
| L266–270 | 唯一の steelman。ただし **40語**（`On its face it was the strongest thing the hospital had. Nobody sent her away. Nobody told her the department was full, or that her plan was wrong. She was in the queue. She left the queue.`）。**直後に** `The court's answer is four words. This contention is spurious.` |
| L290 | `Much depends upon circumstances. We recognize that an emergency room cannot serve everyone simultaneously.` ——**裁判所自身が病院に与えた最強の材料が、否定の後に置かれている** |

**弱い反論を倒す映画は弱い**（§4.1）。そして本件では、**判決文自身が病院側の材料を大量に供給している**のに、台本はそれを全部「否定の後」または「否定の中」に配置してしまっている。

**利用可能な材料は全て ✓ 行である**：CT-12（*thicket / chasmal gaps*）・HA-17（*not particularly precise* / *the grays predominate here*）・CR-08（病院版の主訴）・CR-27（Dr. Rojas の胸痛時期証言）・PR-04（過誤請求は却下・非控訴）・AS-15（*cannot serve everyone simultaneously*）・HA-08（*would have ministered to her had she waited*）。

現状これらは L44・L190–194・L254–256・L290 に**散在**しており、**一度も一塊にならない。**だから観客は「病院が勝つ」と一度も思わない。

### 二周目の指示 R5

**R5-a｜ACT_4 に「病院の言い分」ブロックを新設する。**位置＝現 L264 の直後、`The hospital said it had neither denied...`（L266）の**前**。約 150語。

```
The hospital's case, put at its strongest, went like this.

The court itself described the record it was working from as the thicket of
conflicting testimony and the chasmal gaps in the direct evidence. It said the
evidence in this case is not particularly precise, and that the grays predominate
here. The Hospital maintained that its personnel were told only that Ms. Gonzalez
felt dizzy and nauseated. Its own witness, Dr. Rojas — the physician who treated
her that afternoon — testified that she did not develop chest pains until some
time after she arrived at Hospmed. The malpractice claim, the one that asks
whether her care was competent, had been dismissed and was not on appeal. And the
court agreed, in the middle of its own holding, that an emergency room cannot
serve everyone simultaneously.

Nobody sent her away. Nobody told her the department was full. She was given a
number, and she left before it was called.
```

- 根拠行：CT-12・HA-17・CR-08・CR-27・PR-04・AS-15・HA-08。**全て ✓。新事実ゼロ。**
- **語り手の評価語を一つも入れない。**「もっともらしいが」「一見すると」を書かない。**病院が正しく見えたまま置く。**
- 続けて既存 L266–270（`Its point was that it gave the patient a number...`）を残し、その後に `The court's answer is four words. This contention is spurious.`

**R5-b｜L290 の AS-15 を R5-a ブロックへ移す。**現在の L290–292 は次のように縮める：

- 現：`Much depends upon circumstances. We recognize that an emergency room cannot serve everyone simultaneously. / That caveat is not decoration. Every emergency department runs a queue. The court is not saying that waiting is unlawful. It is saying that in this case, absent any explanation or mitigating circumstances, ...`
- 後：`Much depends upon circumstances. The court was not saying that waiting is unlawful. It was saying that in this case, absent any explanation or mitigating circumstances, the jury could rationally conclude that the Hospital's inaction here amounted to a deliberate denial of screening.`
- （*cannot serve everyone simultaneously* は R5-a で先に鳴っている。ENDING L380 の再掲はそのまま残す＝§12 の再フレーム）

**R5-c｜L182 の `Then the straw man.` を削る。**

- 後：`Then the second argument.`
- 理由：*straw man* は裁判所の語（HA-05）だが、**主張を述べる前に語り手が採用すると安い勝利になる。**裁判所の語は L184 の `This theory of defense, the panel wrote, is doubly flawed.` で既に鳴っている。

**R5-d｜L168–172 の順序を入れ替える。**

- 現：主張 → `This argument has the shrill ring of desperation.` → 理由
- 後：主張 → **理由（マニュアルと管理者の証言・L174–176）** → `The court's reply runs nine words. This argument has the shrill ring of desperation.`
- 効果：**皮肉を観客が先に見つけ、裁判所の九語がその答え合わせになる。**現状は裁判所の評価が先に来て、観客の仕事が消えている。

---

## R6 — モチーフの状態変化を順に言えるか　**FAIL**

**言えない。番号は状態を二つしか持たず、しかも 18分間消えている。**

**証拠**（機械計測・モチーフ言及の位置）

```
L 21  47 が渡される         (HOOK)
L 26  24 が呼ばれる         (HOOK)
L 36  「呼ばれなかった」     (OP)
L 52  47 が渡される（再掲）  (ACT_1)
L 58  24 が呼ばれる（再掲）  (ACT_1)
      ─────── ここから 18分、モチーフ不在 ───────
L262  "A high number and a cold shoulder."（裁判所の語・約 19分）
L307  47 と 24 のコールバック（約 22分）
L398  24 が呼ばれる         (ENDING)
L401  47 は呼ばれなかった   (ENDING)
```

**これはモチーフではなく bookend である。**正典 §5 は「同じ物を、違う状態で、順番に見せる」「状態の順序を先に決めてから台本を書く」と要求している。番号は**状態変化していない**（渡された／呼ばれなかった、の二値）。ACT_2・ACT_3・ACT_5 の 15分間、モチーフは論証を一切運んでいない。

**しかも救いは既に発注済みである。**`EP63_correa_CODEX_BATCH_A.v001.md` には**白紙の券の八状態が全部ある**（`C100` `C099` `C001` `C136` `C137` `C207` `C208`）。**台本がそれを置いていないだけである。**

### 二周目の指示 R6

**R6-a｜§3 の八状態を、台本のビートとして明示的に置く。**新規プレート不要。追加語数は合計約 40語。

| 状態 | 置く場所 | 台本に足す語（全て既存事実） |
|---|---|---|
| 1 発券機 | ACT_1 冒頭（現 L52 の直前） | **語を足さない。画のみ**（`C100`）。⚠ 発券機・機械という語は CR-09 の *a Hospital employee assigned the patient a number* を超える。**台詞は現行のまま**。券がどこから来たかは画だけが言う |
| 2 同じ券の束 | ACT_1（L52 の直後） | **語を足さない。画のみ**（`C099`） |
| 3 手の中 | HOOK / ACT_1 | 既存 |
| 4 空席の上 | ACT_1 末（L68 の後） | **語を足さない。画のみ**（`C136`） |
| 5 床・湿気で反る | ACT_3（L232 の直前・時間経過の表現） | **語を足さない。画のみ**（`C137`） |
| **6 どこにも無い** | **ACT_3 L234**（`There was no record.`） | **既存の台詞のまま。画を「空の引き出し／記入の無い棚」に確定する** |
| 7 券が消えた座面 | ENDING（L392 のコールバック） | 既存 |
| 8 状態3に戻る | **ENDING 最終画** | `C001` を再使用（`C208` の後） |

**R6-b｜ACT_2 に一度だけ番号を戻す。画だけで。語は足さない。**

現在 ACT_2（6:45–12:15・1,088語）にモチーフが一言も無い。$700,000 の内訳（L113）の直後の 3秒を、**`C099`（カウンターに扇状に並ぶ同じ白紙の券）**に当てる。

⚠ **ここに台詞を足してはならない。**「七十万ドル、一枚の券と一時間半に対して」の類は、$700,000 と待ち時間の間に語り手が因果を作る操作であり、DM-15 が結んでいるのは *failure to provide screening → agony* であって待ち時間の長さではない。**画の隣接だけが許される。**

**R6-c｜ACT_5 に番号を戻す。**放棄（waiver）の列挙（L339）の**画**を、ACT_1 の待機の列挙と同じリズム・同じ構図で切る。**語は足さない。**（§1 の照応。§19 R9 と同一操作）

**R6-d｜⚠ mandatory_stills の再導出が必要。**`episode_spec.v001.json` の notes が明記している——*"RE-DERIVE THIS LIST if the script is revised: the order is derived from the script's beats."* 状態の並べ替えはビート移動なので、二周目の後に **223件の順序を再導出**し、`check_spec_satisfied.py` を通し直す。

---

## R7 — 各主要人物に反復不能な細部があるか　**PASS**

**カテゴリで済ませている人物が一人もいない。**この台本の最も強い部分である。

| 人物 | 反復不能な細部 | 行 |
|---|---|---|
| Carmen Gonzalez | 65歳・寡婦・高血圧の糖尿病患者・降圧剤を**二倍量**服用・血圧 **90/60**・*the trunk of the family tree* | L17, L70, L196, L358 |
| Angel Correa | 番号**二十四**が呼ばれるのを聞きながら出て行った・信用性が *relatively unscathed* | L26, L258 |
| Esther | *some fifteen minutes later* に到着 | L23 |
| 孫四人 | 父を**祖母の五か月前**に亡くしている・祖母の家で育った | L354 |
| Dr. Rojas | Hospmed の**所長**・救急車を *could not commandeer*・**病院側が呼んだ証人** | L66, L72, L276 |
| Judge Selya | Emerson の *mutable cloud*・*esurient*・*vellicate*・*anent*・*chasmal gaps* | L206, L320, L358, L231, L48 |
| 病院 | **自分で書いた四つの規則**・*dutifully instructed his staff*・**省略記号を付けずに反対の意味で判例を引用した** | L227, L174, L356 |
| 受付係・スタッフ | **意図的に無記述**（`forbidden_claims` 準拠。*"blithely"* は裁判所の語であることを明示） | L62 |

**L62 は模範例である**：`Blithely. That is the court's adverb, not ours, and it is the only description of the staff's conduct anywhere in the record.`（R2 で *not ours* の自己言及を削る案は出さない。**ここは帰属の明示であって自己称賛ではない**）

**二周目の指示：なし。触らない。**

---

## R8 — 悪役を作っていないか　**FAIL**

個人の悪役は作っていない（受付係は無記述・スタッフは裁判所の語だけ）。**しかし条件文が二箇所で崩れ、病院の意図を事実として断定している。**これは制度を悪役に変える操作であり、しかも**台帳外**である。

**証拠 1｜L276**

> `The hospital's own witness described a call from it, sending its patient elsewhere.`

- 台帳 CR-18 は *"a datum **suggesting** that HSF **tried to** shunt Ms. Gonzalez to Hospmed"* としか言っていない。
- **`sending its patient elsewhere` は完了した行為の断定である。**Q-02（保険を理由に治療を拒んだ）に接近する。
- **しかも同じ台本が L90 で自分にそれを禁じている**：`Probably. Perhaps. Suggesting. ... Nobody ever proved why the call was made, or by whom.`

**証拠 2｜L280**

> `If the hospital had arranged for her to be seen at Hospmed, then the hospital is the reason she got up and drove there. The wait it says she abandoned is a wait it had already ended.`

- 第一文は正しく条件文。**第二文で条件が消えて直説法になっている。**（`is a wait it had already ended`）
- 裁判所の原文（HA-08）は最後まで条件文である：*"If the jury believed the physician's testimony, it could well have found that HSF never intended to treat the decedent, or, at the least, was itself responsible for truncating her wait."*
- **裁判所より雑になっている**（§13）。

### 二周目の指示 R8

**R8-a｜L276 を書き換える**

- 現：`The hospital's own witness described a call from it, sending its patient elsewhere.`
- 後：`The hospital's own witness described a call she said came from the hospital, about a patient who would be coming to her instead.`
- 根拠：CR-17（*a nurse called from HSF to advise her that the patient would be coming to Hospmed for treatment*）。**帰属を証人に戻す。**

**R8-b｜L280 の第二文に条件を戻す**

- 現：`The wait it says she abandoned is a wait it had already ended.`
- 後：`Then the wait it says she abandoned would be a wait it had already ended.`

**R8-c｜L278 の引用を条件のまま鳴らす**（現状は既に `If the jury believed...` で正しい。**触らない**）

**R8-d｜ACT_3 の皮肉の組み立て（L174–176）は残す。**

> `It had written a manual about complying with EMTALA. Its executive told a jury he had trained the staff on it. And then it argued that EMTALA did not apply.`

三つとも ✓ 行（HA-02）であり、**語り手は評価を一語も足していない。**皮肉は観客が組んでいる。§7 の模範。ただし R5-d により、**この段落を裁判所の *shrill ring of desperation* より前に置く。**

---

## R9 — 賭け金は縦（深さ）に上がっているか　**PASS**

横（被害の大きさ）に逃げていない。**「他にも大勢いる」「今でも起きている」を一度も言っていない。**RQ-04（統計は判決文に無い）を完全に守っている。

縦の梯子は成立している：

```
一つの番号（L21）→ 一つの待合室（L64）→ 病院自身が書いた四つの規則（L227）
→ ninety-nine percent of American hospitals（L178）→「断る」という概念そのもの（L299）
```

**弱点（FAIL ではない）**：ninety-nine percent が**賭け金として使われず、注意書きとして使われている**（L180 `Ninety-nine is not one hundred.`）。この慎重さ自体は正しい（Q-12）ので、**現状維持を推奨する。**深さの段としては L299 の *constructive* が十分に効いている。

**二周目の任意指示 R9-a｜ACT_5 の放棄を主題の最終段として鳴らす。**

病院は最良の抗弁を、**否定されたのではなく、一度も持ち出さなかったことで**失った。L339 は既にその列挙になっている（答弁書・日程協議・公判前協議・準備書面・二度の Rule 50(a)・評決書式）。**語を一語も足さず、ACT_1 の待機描写と同じ編集リズム・同じ構図で切る。**照応を語り手に説明させない。観客が見つける。

---

## R10 — ENDING に新事実がゼロか　**PASS**

**一項目ずつ照合した。新事実ゼロ。**

| ENDING の記述 | 初出 |
|---|---|
| *some procedure, administered even-handedly* | L212 |
| stabilisation if an emergency condition is found | L142 |
| *A hospital that examines you badly has not broken this law* | L218 |
| *cannot serve everyone simultaneously* | L290 |
| *mere negligence* を判断していない | L242 |
| *so egregious and lacking in justification* | L240 |
| 陪審の認定を *unimpugnable* とした | L244 |
| *constructive dumping* | L299 |
| 移送の認定は未審査 | L111 |
| Vital signs / written chart / referral | L227・L238 |
| 一枚も出せなかった | L234 |
| 二十四が呼ばれた | L26・L58 |

**構成上の指摘（PASS の範囲内）**：ENDING 378語のうち**約 230語（61%）が「決めていないことの列挙」**であり、これは再フレームというより**判決要旨の朗読**である（§12 の ✗ 側に近い）。R3-c で一項目（L388）を削れば四項目になり、残り約 150語の再フレーム部（`There is no villain in this record...` 以降）との比が改善する。**それ以上は削らない**——`forbidden_claims` の 10項目のうち 4項目は、この列挙でしか観客に伝わらない。

---

## R11 — ENDING は最初の画に戻るか　**PASS**

```
HOOK   : 白紙の券 → 空席 → 出ていない番号表示 →【OST: NUMBER FORTY-SEVEN】
ENDING : ...an attendant called number twenty-four. → ⟨HELD⟩ → Forty-seven was never called. →【OST: NUMBER FORTY-SEVEN】
```

**ループは閉じている。**OST も一致している。

**二周目の任意指示 R11-a**：最終画を `C208`（券が消えた座面）ではなく **`C001` の再使用**（手の中の白紙の券）で終える。§5 の「最後の状態は最初の状態に戻る。二周目に意味が反転する」。新規プレート不要。

---

## R12 — 沈黙の位置を三つ言えるか　**FAIL**

**⟨HELD⟩ が 14箇所ある。**設計ではなく句読点として使われている。

**証拠**（全 14箇所・直後の台詞）

```
 1 HOOK  L 25  Twenty-four.                                          ← 正しい
 2 ACT_1 L 76  That is the whole of what the record says...          ← 正しい
 3 ACT_1 L 83  It is about what happened while she was still sitting there.
 4 ACT_1 L 92  Keep the call. It comes back.                         ← ★最悪
 5 ACT_2 L123  Why they failed depends on what this statute promises...
 6 ACT_2 L154  The duty to look does not depend on what the looking would have found.
 7 ACT_2 L161  So the statute applied — if the hospital did.
 8 ACT_3 L224  HSF had written down what an appropriate screening was.
 9 ACT_3 L233  There was no record. Not a thin record. None.
10 ACT_4 L296  And then the sentence the whole case is built on.     ← 認知の「前」
11 ACT_4 L309  Nothing was refused. Everything was withheld.
12 ACT_4 L326  The court decided none of this on motive.
13 ACT_5 L349  Not decided. Forfeited.
14 END   L400  Forty-seven was never called.                          ← 正しい
```

正典 §11：**「沈黙は、直前の一文が重いときにだけ効く。軽い文の後の沈黙は事故に見える。」**#3 #5 #7 #8 は導入文・接続文の後に置かれており、**重さが無い。**

**#4 は単独で最も深刻**：`Keep the call. It comes back.` ——**語り手が「これは伏線です」と観客に告知している。**§5 の「近いと仕掛けが見える」以前の問題で、**仕掛けを自分で開示している。**その後に沈黙まで置いている。

### 二周目の指示 R12

**R12-a｜L93 `Keep the call. It comes back.` を ⟨HELD⟩ ごと全削除。**

- 直前の L90（`Nobody ever proved why the call was made, or by whom, or what was in anybody's mind. What the jury had was a physician's recollection of a call, placed at about the hour a card was checked.`）で段落を終える。**それで十分に残る。**
- 回収（L275 `The first is the telephone call.`）までの距離は約 15分。§5 の 2分規則を大きく満たす。**告知は不要。**

**R12-b｜⟨HELD⟩ を五箇所に削減する。**残すのは #1・#2・#9→#10 の再配置・#14 と、下記の一箇所。

| 残す | 位置 | 根拠 |
|---|---|---|
| 1 | HOOK 最終カットの前（`Twenty-four.` の前） | 約束の直前 |
| 2 | L76（`That is the whole of what the record says about how she died.` の前） | 因果ロックの重み |
| 3 | **L242 の直後**（`thus, we need not decide whether mere negligence in failing to expedite screening would itself violate the federal statute.`） | §11-2 **限界の直後**（現在ここには無い。**新設**） |
| 4 | **L299 の直後**（`EMTALA should be read to proscribe both actual and constructive dumping of patients.`） | §11-1 **認知の直後**（現在は L296＝**直前**にある。移す） |
| 5 | L400（`Forty-seven was never called.` の前） | §11-3 最終画の前 |

**削除する ⟨HELD⟩：**L83・L92・L123・L154・L161・L224・L233・L296・L309（R2-g で台詞ごと削除）・L326・L349。**11箇所削除・1箇所新設・1箇所移動。**

---

## R13 — 矛盾する記録を、矛盾のまま出したか　**PASS**

**この台本の二番目に強い部分である。**

**証拠 1｜受付での会話（L44–50）**

> `Angel Correa testified that he implored the receptionist to have someone take care of my mother... The Hospital disagreed, maintaining that its personnel were told only that Ms. Gonzalez felt dizzy and nauseated.`
> `Two accounts. One counter. No way, now, to stand between them.`

**どちらも選んでいない。**そして直後に CT-11 の視認規則（*in the light most hospitable to the jury's verdict*）を置き、`So this is the version of that afternoon a jury was entitled to believe. It is not the only one offered.` と宣言している。**台帳 §9 の Framing rule を完全に実装している。**

**証拠 2｜胸痛の発症時期（L190–194）**

> `The hospital's answer was to point at Dr. Rojas, who had testified that Ms. Gonzalez did not develop chest pains until some time after she arrived at Hospmed. Believe the physician, it said. Not the son.`
> `There is no principled way in which we can accommodate HSF's request, the court replied. Credibility choices are generally for the jury, not for the court of appeals.`

**矛盾を矛盾のまま出し、解決を陪審に返した裁判所の距離を保っている。**

**証拠 3｜L256** `it is why this film keeps saying what a jury could have found rather than what happened.`（自己言及は R2-e で削るが、**実践そのものは台本全体で守られている**）

**二周目の指示：なし。**（ただし R8 の二箇所の条件文崩れは、**同じ規律が電話の件だけで緩んだ**ものである。R8 の修正で全体が揃う）

---

## R14 — 記録の沈黙を、沈黙のまま扱ったか　**FAIL**

台本は沈黙を守る場面で**極めて優秀**である：

```
L 68  The opinion does not describe anyone turning her away. It does not describe anyone discharging her.
L 77  That is the whole of what the record says about how she died.
L 90  Nobody ever proved why the call was made, or by whom, or what was in anybody's mind.
L394  There is no villain in this record. No decision was ever testified to.
```

**しかし一箇所、判決文の中で唯一の思弁的な文が、帰属なしにナレーションされる。**

**証拠｜L362–364**

> `The reason given for it is the sentence to carry out of this film. It states precisely what the case was about and what it was not.`
> `Due to the Hospital's failure to provide even the most rudimentary screening, Ms. Gonzalez spent the few remaining hours of her life in agony, beset by nausea, dizziness, and chest pains. It is hard to imagine — let alone to quantify in dollars — the sheer terror that she must have felt while waiting for medical attention that never came.`

- これは DM-15 の VERBATIM 引用であり、**書かれた文としては完全に正しい。**
- **しかし音になったとき、聴き手には引用だと分からない。**直前の二文は引用の導入ではなく、語り手の評価（「この映画から持ち帰る一文」）である。
- 結果、*"the sheer terror that she must have felt"* は**語り手が彼女の内心を推測した文として聞こえる。**これは正典 §15-7（沈黙している記録への声当て）そのものである。
- **台本の他の引用は全て帰属されている**（L44 *the court wrote* / L60 *the opinion says* / L130 *this is the House report* / L202 *Then it quoted the Sixth Circuit* / L354 *The testimony indicated*）。**この一箇所だけが抜けている。しかもそれが最も危険な一文である。**

### 二周目の指示 R14

**R14-a｜L362 の二文を削り、帰属の一文に置き換える**

- 削る（26語）：`The reason given for it is the sentence to carry out of this film. It states precisely what the case was about and what it was not.`
- 置く：`The court gave its reason in two sentences.`

**R14-b｜引用の内側に可聴の帰属を挿入する**（引用語を変えない挿入句）

- 後：`Due to the Hospital's failure to provide even the most rudimentary screening, the court wrote, Ms. Gonzalez spent the few remaining hours of her life in agony, beset by nausea, dizziness, and chest pains. It is hard to imagine — let alone to quantify in dollars — the sheer terror that she must have felt while waiting for medical attention that never came.`
- **DM-15 の語順・語彙は一字も変わっていない。**放送慣行の挿入句のみ。

**R14-c｜L366 `Not her death. The waiting.` はそのまま。**R14-a で直前の説明が消えるので、**この四語が引用の直後に立つ。**これが ACT_5 の payoff である。

**R14-d｜同種の未帰属引用がないか、二周目で全 VERBATIM 引用の可聴帰属を一括点検する。**（L210 の screening test・L216 の AS-06・L240 の AS-08 は直前の文脈で帰属されており可。L284 の AS-14 は `the court wrote` があり可）

---

## R15 — 声に出して読んだか　**FAIL**

**読んだ形跡が無い。**そして音読で必ず引っかかる箇所が四つ残っている。

**証拠 1｜ACT_1 に「長い助走を短い一撃で切る」箇所が一つも無い**（§10）

機械計測（30語以上の文の直後に 5語以下の文が来る回数）：

```
HOOK 0 / OP 0 / ACT_1 0 / ACT_2 2 / ACT_3 1 / ACT_4 3 / ACT_5 3 / ENDING 0
```

正典 §10：**「各幕に最低一つ、30語以上の助走を5語以下で切る箇所」。ACT_1 が 0 である。**（HOOK・OP・ENDING は短尺なので免除。ACT_1 は 774語あり免除されない）

**証拠 2｜音にならない文字列**

| 行 | 文字列 | 問題 |
|---|---|---|
| L284 | `...can constitute a denial of an appropriate medical screening examination under section 1395dd(a).` | **「セクション・サーティーンナインティファイブ・ディーディー・エー」**——認知の直前で観客の集中を切る |
| L358 | `The sums awarded do not shock or even vellicate our collective conscience.` | *vellicate* が無注釈。*esurient* は L322 で `Esurient. Greedy.` と注釈されているのに、ここだけ放置 |
| L231 | `...the Hospital's utter inability to produce any records anent Ms. Gonzalez's visit.` | *anent* が無注釈。**中盤反転の直前**であり、意味が通らないと反転が効かない |
| L339 | `...renewed that motion at the close of all the evidence without adding it...` | 一文 **117語**。放棄の列挙としては意図的で効果的だが、**息継ぎ位置を字幕分割と合わせて設計する必要がある**（`_smart_split` の文法分割に任せると破綻する長さ） |

**証拠 3｜HOOK が 8秒に対して 139語**（§9・約45秒分）。**音読すれば即座に分かる不整合。**

### 二周目の指示 R15

**R15-a｜ACT_1 に 30語超→5語以下の切りを一箇所作る。**L60–64 を統合する：

- 現：`Now accompanied by her daughter, the opinion says, Ms. Gonzalez maintained her unproductive vigil for an additional forty-five to seventy-five minutes. The Hospital staff continued blithely to ignore her.` … `Add up the clock. She was inside that emergency room for something between two hours and two and a half. No physician saw her in that time.`
- 後：`Add up the clock. From no later than one o'clock until somewhere between three and half past three, she was inside that emergency room — something between two hours and two and a half — with a number in her hand and a card that had already been checked.` **`No physician saw her.`**
- （31語＋4語。CR-05・CR-13・CR-09・TL-12 の範囲内。**新事実ゼロ**）

**R15-b｜L284 の引用末尾を切る。**引用を短くすることは許される。

- 後：`...can constitute a denial of an appropriate medical screening examination.`
- （AS-14 の全文は台帳が保持する）

**R15-c｜L358 の *vellicate* は、注釈せず引用を短くする。**

- 現：`The sums awarded do not shock or even vellicate our collective conscience.`
- 後：`The sums awarded, the court said, do not shock our collective conscience.`
- 処理＝**引用の一部使用**（DM-13）。⚠ *esurient* と同じ「Vellicate. Twitch.」型の注釈は**採用しない**——*vellicate = twitch* は辞書的定義であって台帳に行が無い。*Esurient. Greedy.* が許されるのは L320 の文脈が *greedy* の意味を判決文自身の文（*ample provocation to discriminate*）で供給しているからである。

**R15-d｜L231 の *anent* は、語を置換せず引用の末尾を切る。**

- 現：`...and the Hospital's utter inability to produce any records anent Ms. Gonzalez's visit.`
- 後：`...and the Hospital's utter inability to produce any records.`
- 処理＝**末尾切断**（AS-11 の一部使用）。⚠ *anent* を *of* に置換**してはならない**。VERBATIM 引用の語を書き換えることになる。**引用は短くしてよいが、変えてはならない。**

**R15-e｜二周目の後、必ず音読する。**測定できるのは短文比率だけで、**リズムは黙読では測れない**（§16 R15）。音読で確認する項目：(1) ACT_1 の切り、(2) L339 の 117語文の息継ぎ、(3) 判決文引用の帰属が全て可聴か（R14-d）、(4) 数字の読み上げ（*ninety-nine* / *forty-seven* / *twenty-four* / *seven hundred thousand*）が混線しないか。

---

## 19.16 二周目の実行順（**一括で当てて、レンダーは一回**）

`feedback_no_wasted_cycles` / `feedback_retro_EP35`：**全 fail を一括把握してから一回で直す。**バッチを分けない。

| # | 操作 | 対象行 | 種別 |
|---|---|---|---|
| 1 | HOOK を 8秒（20〜25語）に書き直す | HOOK 全体 | **最後にやる**（§17） |
| 2 | HOOK の非重複 4事実を ACT_1 冒頭へ戻す | L40 の前 | 追加 +90語 |
| 3 | OP 第三文を既知の破滅に差し替え | L36 | 置換 |
| 4 | 自己言及 7箇所を除去 | L77, 79, 90, 256, 264, 362, 394 | 削除 −約 95語 |
| 5 | **steelman ブロックを新設** | L264–266 の間 | 追加 +150語 |
| 6 | AS-15 を steelman へ移動・L290 を縮約 | L290 | 移動 |
| 7 | `Then the straw man.` を中立化 | L182 | 置換 |
| 8 | 皮肉と裁判所評価の順序を入れ替え | L168–176 | 並べ替え |
| 9 | 条件文の崩れを二箇所修復 | L276, L280 | 置換 |
| 10 | 主題の言い換えを削除 | L310 | 削除 −6語 |
| 11 | 因果ロックの三度目を削除 | L388 | 削除 −35語 |
| 12 | `Keep the call. It comes back.` を削除 | L92–93 | 削除 −6語 |
| 13 | ⟨HELD⟩ を 14→5 に整理（1新設・1移動・11削除） | 全編 | 構造 |
| 14 | DM-15 引用に可聴帰属を挿入 | L362–364 | 置換 |
| 15 | モチーフ八状態をビートに固定（語は最小限） | 全編 | +約 40語 |
| 16 | 音にならない三箇所を引用切断で処理 | L231, L284, L358 | 置換 |
| 17 | ACT_1 に 30→5 の切りを作る | L60–64 | 置換 |
| 18 | **全文音読** | — | 検証 |
| 19 | `check_script_length` / `check_script_craft` 再実行 | — | 機械 |
| 20 | **`mandatory_stills` 223件を再導出** → `check_spec_satisfied.py` | spec | **必須** |

## 19.17 語数の収支

| | 語数 |
|---|---|
| v001 実測 | **5,391** |
| 削除（HOOK 139→25、自己言及、L310、L388、L92、引用切断ほか） | **−約 270** |
| 追加（steelman 150、ACT_1 復帰 90、モチーフ 40、帰属 15） | **+約 295** |
| **v002 見込み** | **約 5,415** |
| 契約帯域 `script_words` | **5,100–5,600** ✓ |

**帯域内。**尺の作り直しは不要。

## 19.18 下流への影響

- **`mandatory_stills` は必ず再導出**（spec notes の明示要求）。ビートが動く＝プレート順が動く。
- **HOOK プレート `C001`–`C005` は変更不要。**発注書 L124–130 の promise-payoff 表が 8秒版を前提に既に組まれている。
- **ENDING 最終画に `C001` を再使用**（R11-a）。新規生成ゼロ。
- **状態6（記録の不在）の絵**が ACT_3 帯（`C082`–`C125`）に十分あるかは、二周目確定後に目視 QC で確認する（`pd-factory-shelf-mislabeled` の教訓：ラベルではなく絵を見る）。
- **v001 は破棄しない。**`v002` を新規 revision として作る（不変条件6）。

---

*v001 · 2026-08-04 · `docs/PD_SCREENPLAY_STANDARD.v001.md` に従って書かれた二本目。ただし §0 のとおり、**台本の後に書かれた**。*
