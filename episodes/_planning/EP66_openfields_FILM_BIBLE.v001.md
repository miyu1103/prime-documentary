# EP66 · THE OPEN-FIELDS DOCTRINE — FILM BIBLE v001

**Standard:** `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` 行15（Academy脚本水準）・行16（リテンション設計）・**行9（2026-08-10改訂・EP66から拘束）**
**Cases:** *Punxsutawney Hunting Club, Inc. & Pitch Pine Hunting Club, Inc. v. Pennsylvania Game Commission and Mark Gritzer*, No. 23 WAP 2023 (Pa., **21 July 2026**) ／ *Terry Rainwaters et al. v. Tennessee Wildlife Resources Agency et al.*, No. W2022-00514-COA-R3-CV (Tenn. Ct. App., **9 May 2024**)
**Facts:** `EP66_openfields_FACTS_LEDGER.v001.md`（98 fact rows / 12 not-decided rows / 15 quarantine / 10 open）— **唯一の事実源**
**Packaging（承認済み・上位文書）:** `EP66_openfields_PACKAGING.v001.md`（タイトル・サムネ・最初の20秒）
**Contract:** `episodes/PD-2026-066-openfields/episode_spec.v001.json` — 27:00–33:00（設計目標 **30:00**）・4,565–5,247語・8区分・幕あたり13–17ビート

> この文書は「何を語るか」ではなく「**なぜこの順で、この距離から語るか**」を決める。台本はこれに従属する。
> 事実は台帳が持つ。**ドラマは事実の上に組む。作らない。**
> **本文中の全ビートは台帳の行IDを持つ。IDの無い主張は台本に入れてはならない（invariant 1）。**

---

## 0. 今回は順序が正しい（先に記録しておく）

EP63・EP64・EP65 はいずれも **台帳 → 台本 → 設計書** の順で作られ、設計書が事後の不合格リストになった。
EP66 は違う。台本は書き始められ、**この設計書が無いという理由で停止された。** 正しい判断である。
標準（行15）の工程はこうであり、今回はこの順に戻っている。

```
FACTS_LEDGER → PACKAGING（承認済み） → FILM_BIBLE ←いまここ → SCRIPT 一周目 → 機械ゲート → 人間レビュー → SCRIPT 二周目
```

したがってこの設計書に **§19 CRAFT REVIEW は無い。** 採点する台本がまだ存在しないからである。
代わりに末尾に **§13「欲しかったが台帳に無いもの」** を置く。この節がこの文書で最も価値のあるページである。

**上位関係。** 事実は台帳が上位。作品の前面（タイトル／サムネ／最初の20秒）は PACKAGING が上位で、
この設計書はそれを **変更しない。到達点として受け取り、そこへ着地する本編を設計する。**
ただし PACKAGING §3 は自分で三点の FACT-LOCK を宣言しており、その解決は台帳を持つこの文書の仕事である（§9）。

---

## 1. CONTROLLING IDEA（この映画が持つ唯一の思想）

> **所有は保護ではない。**

一行で言えるまで削った。この文は**映画の中で一度も口に出さない**。全編がこれを実演する。

なぜこの一文なのか。**二つの記録が、別々に、同じ形をしているからである。**

土地が守られるかどうかを決めているのは、それが誰のものかではない。決めているのは二つだけである。

1. **どの州にあるか。** ペンシルベニアは自州憲法第1条第8節のもとで二つの条文を**文面上**無効とした（PA-31・PA-32）。
   テネシーは同種の条文を**文面上は合憲**とし、この二人への**適用においてのみ**違憲とした（TN-22・TN-27・TN-38）。
   **同じ日に、同じ行為が、州境の右と左で違法にも適法にもなる。**
2. **そこに何をしたか。** ペンシルベニアの規則は「土地」に及ぶのではない。
   ✓ *"a landowner's open fields extends to private land located beyond the curtilage over which the landowner has
   demonstrated a reasonable and legitimate expectation of privacy by taking sufficient steps to exclude intruders
   therefrom."*（PA-29）——**十分な手当てをした地主に及ぶ。**
   テネシーも同じ形である。1926年の *Welch* が引いた線は ✓ *"would not include wild or waste lands, or other lands
   that were unoccupied."*（TN-25）であり、2024年の裁判所が保護を認めた根拠は
   ✓ *"Their lands were secured by gates, accessible only through private drives, and posted with 'no trespassing'
   signs… The Plaintiffs used and occupied their land by farming, fishing, camping, and hunting."*（TN-30）だった。

否定テストを通す。「**自分の土地だから守られる**」——この否定文に対して、本編の全区間が反論として機能する。
そして最後に、勝った側の裁判所自身が脚注24でそれを認める。

> ✓ *"we reserve for another day the question of whether the privacy protections afforded by Article I, Section 8
> extend to landowners who have taken fewer steps than the Hunting Clubs, or even no steps, to exclude intruders
> from their properties."*（ND-01）

副題として機能する対句：**線は土地の縁ではなく、手当ての縁に引かれている。**

---

## 2. THE PROBLEM THIS FILM HAS, AND WHY IT IS THE FILM

**この映画には、繋がっていない二つの事件しかない。**そしてそれが主題である。

台帳は文字列検索で証明している。ペンシルベニアの意見書に `Rainwaters` は **0回**、`Hollingsworth` は **0回**、
`Tennessee Wildlife` は **0回**しか出てこない。ペンシルベニアが引くテネシー判例は 1926年の *Welch* だけである。
二つの裁判所は互いを知らない。判決日は **26か月**離れ、**結論は逆**である（台帳 GOVERNING CAUTION・⛔-01）。

普通のドキュメンタリーはここで嘘をつく。「一つの闘い」「ついに勝った」に均す。**それは禁止されている（⛔-01）。**
均さない代わりに何を得るか。

### 繋がっていないことを、構造にする。

> **この映画が語るのは一つの運動ではない。一つの教義に対する、互いを知らない二つの答えである。**

観客は「連続する闘争」を期待するように訓練されている。**その期待を裏切ることが、この映画の転回になる（§5）。**
そして裏切りは創作ではない。**記録がそう言っている。**

| 役 | 何を置くか | EP66 |
|---|---|---|
| **主人公** | 状態が変化する**物** | **鎖に掛かった南京錠**（閉じている → 迂回される → 濡れる → 州境の向こうの別の錠 → 証拠として読まれる → **錠の無い門柱** → また閉じている） |
| **敵対者** | 誰も検証しない**仮定** | 「**門と鎖と札があれば、そこは私有地として扱われる**」 |
| **人間の縦糸** | 制度を受ける一人（聖人にしない） | **Hunter Hollingsworth** |

**人間の縦糸に Hollingsworth を選ぶ理由は、彼が理想的でないからである。**
台帳が彼について与えるのは、93エーカー（Benton郡とHenry郡にまたがる）、釣り・農・キャンプ・狩り、
鎖の掛かった門と「No Trespassing」の札、恋人と過ごす場所、監視されているという恐れ、訪問の減少——そして、
✓ *"Mr. Hollingsworth's hunting license was suspended for three years in November … 2018 due to a federal dove
baiting offense."*（TN-14）である。

**この一行を落とした映画は、親切なのではなく、鵜呑みにしているだけである（⛔-09）。**
同時に、それを「だから入られて当然だった」に使うのも誤りである。**彼が訴えた立入りは 2016年12月21日**であり、
停止処分の **23か月前**である（TN-15・TN-14）。州は2016年に、2018年に真実になることを知らなかった。

置き場所は ACT_2 の中盤（§6・A2-10）。**観客が「この人は本当に潔白なのか」と思い始めるちょうどその場所に置く。**
語り手は評価を一言も付けない。事実と日付だけを並べ、⟨HELD⟩ を打つ。

### ペンシルベニア側に人間はいない。それも主題である。

原告は **member-owned hunting clubs** であり、意見書は個人を一人も名指ししない（PA-01）。
記録が人について書くのはこれだけである。

> ✓ *"family matters, marital problems, work stressors, romantic feelings, and faith in God."*（PA-06）

**顔も名前も無い。あるのは、そこで話される内容の一覧だけである。**
テネシー側にも同種の一行がある——✓ *"he also uses the property to spend time alone with his girlfriend."*（TN-13）。
**この二つを並べてよい。ただし §12 の接続語規則に従う場合に限る。**

### 官吏を悪役にしない

Mark Gritzer と Kevin Hoofman は**実在する、名前のある、現職の公務員**である（⛔-07・⛔-08）。
記録が支えるのは行為だけであり、意図は一つも記録されていない。契約 `forbidden_claims` はそれを機械可読にしている。
**そして重要なのは、ペンシルベニアの意見書は Gritzer が違法なことをしたとは一言も言っていない**ことである。
違憲とされたのは、彼に権限を与えていた条文のほうである（PA-31）。
**悲劇は道徳ではなく、条文の設計にある。**

---

## 3. MOTIF — 南京錠の七つの状態

モチーフは**一つ**。**鎖に掛かった南京錠**。台詞で説明しない。登場順に固定する。

なぜ錠なのか。**27分のあいだ、それは何の役にも立たなかった物である。**誰も止めなかった。
そして最後に、それが**唯一効いていた物**だと分かる——物理的にではなく、法的に。
PA-07 の ✓ *"installed locked gates at all public entrances"* と TN-13 の
✓ *"behind a chained gate at the entrance to his property with a 'No Trespassing' sign"* が、
二つの州で、保護を**買った**唯一のものだった。**同じ画の意味が反転する。**

| # | 状態 | 出る場所 | 言わない意味 | 根拠 |
|---|---|---|---|---|
| 1 | 農道を横切る鎖。錠は閉じている。朝の光 | ACT_1 冒頭（0:44 付近） | これが、人を入れないということだと思われている | TN-13 |
| 2 | **同じ錠が、閉じたまま。向こう側の泥に足跡がある** | ACT_1 の反転（0:52–1:05） | 開けられてはいない。**迂回された** | TN-01・TN-13・§13-10 |
| 3 | 雨。錠が濡れている。誰も来ない | ACT_3 末（17:20 付近） | 記録は無い。数も分からない | TN-02・TN-08 |
| 4 | **別の錠。別の造り。別の門。**背後の樹相が変わっている | THE TURN（17:40）reset beat | 同じ物、違う州 | PA-07 |
| 5 | 平板な記録光で正面から撮られた錠。証拠品のような画 | ACT_4 後半（23:30 付近） | 裁判所はこれを**読んだ** | PA-29・TN-30 |
| 6 | **何も掛かっていない門柱。**針金の輪が垂れている。奥は空の畑 | ACT_5 の認知（26:20） | 脚注24の地主 | ND-01 |
| 7 | 状態1と**同一構図**。閉じた錠。朝の光 | ENDING 最終画 | これは人を入れない物ではない。**審理を受ける資格を買う物である** | — |

**マクロ・ループ**：状態1で始まり、状態7で終わる。**画は同じ。意味が反転する。**

**プラント → ペイオフ（三本・すべて2分以上離す）**

| プラント | 位置 | ペイオフ | 位置 | 距離 |
|---|---|---|---|---|
| HOOK 最終画：レンズが見るような、空の畑（PACKAGING §3・0:17.8–0:20.3） | 0:18 | モチーフ状態6：錠の無い門柱と空の畑（脚注24） | 26:20 | **26分** |
| コメント質問「あなたの土地にカメラが付いたら、何日で気づくか」 | 1:14 | ✓ *"That camera remained on Punxsutawney's property for **78 days**."*（PA-13）。**数字を言って、止まる。** | 21:10 | **20分** |
| 切られた枝とカメラ（HOOK 0:09.9–0:15.0・タイトルT1の約束） | 0:10 | その枝もカメラも車内捜索も動画も、**上訴では争点ではなかった**（TN-15・TN-16）。州の行為か連邦の行為かも**未解決**（ND-11） | 27:40 | **27分** |
| OP：教義を映画自身の言葉で述べる | 0:24 | PA-21 の**原文**が ACT_4 の一行目として鳴る | 18:00 | **17.5分** |

**規則**
- モチーフは錠**一つ**。門・鎖・札・紫のペイントは錠の状態を構成する要素であり、独立したモチーフにしない。
- 切られた枝は**モチーフではなくプラント**である。HOOK で一度、ACT_5 で一度。**中間で出さない。**
- 一ドルはモチーフにしない。**一度だけ言い、形容詞を付けない**（⛔-14）。
- 生成プレートの上に**読める文字を焼き込まない**（契約 `forbidden_subjects` 散文規則）。
  **紫のペイントは文字ではなく色である。**この事件の標識体系が、そのままこの制約の解になっている（PA-10）。

---

## 4. ARC — 五幕の中の三幕

| 幕 | 三幕上の役割 | 起きること | 距離 |
|---|---|---|---|
| HOOK | 約束 | 2017年11月30日。木。切られた枝。ボルトで留められたカメラ。誰も知らされない | 寄り |
| OP | 契約 | 家の周りの狭い輪の外は、法が **open field** と呼ぶ土地である | 引き |
| **ACT_1** | **設定** | 二人の土地、鎖、札、立入り、記録が取られていないこと。**そして門は法的な線ではない** | 中→寄り |
| **ACT_2** | 対立 | 州が「自分は何をしてよいか」を述べる。**その主張が最強の形で立つ。**そして人間の複雑さ（TN-14） | 中 |
| **ACT_3** | 対立の最大化 → **転回** | テネシーの答え。**文面上は合憲。**差止め無し。一ドル。映画は終わったように見える → **別の州** | 中→引き |
| **ACT_4** | **反対の答え** | *Russo* 破棄。*"possessions" … includes land.* 二条文が文面上無効。差戻し無し | 引き→中 |
| **ACT_5** | **認知 → 限界** | まだできること四つ／行政捜索／**脚注24**／枝は争点ではなかった | 寄り |
| ENDING | 余韻 | 新事実ゼロ。閉じた錠に戻る | 引き |

**三幕の切れ目**
- **第一幕（設定）= HOOK + OP + ACT_1。** 終わり方：門も鎖も札も、法的な線ではない。それでも二人は訴えた——**州**憲法で。
- **第二幕（対立）= ACT_2 + ACT_3。** 終わり方：**転回**。
- **第三幕（解決）= ACT_4 + ACT_5 + ENDING。** 終わり方：解決ではなく、**保留された問い**。

**賭け金は縦（深さ）に上げる。**記録は横（被害の大きさ）を支えない。数字は一つも足せない（⛔-06・○-04）。

**一本の木 → 93エーカー → 二人の全区画 → 州内の掲示された私有地すべて → 「possessions」という一語 →
州憲法 → そして、何もしなかった地主。**

最後の段——**何もしなかった地主**——が最深部である。そこに答えが無いことが ACT_5 の認知になる。

---

## 5. TURN と RECOGNITION（一つずつ・置く場所を動かさない）

### TURN（転回・ペリペテイア）— ACT_3 末尾 · 約 **17:40**（全体の 59%）

**逆方向に十分進んでから折り返す。**

ACT_3 では**州側が実質的に勝つ。しかも正当に勝つ。**

- 文面審査の基準は厳しい：✓ *"the challenger must establish that no set of circumstances exist under which the
  Act would be valid"*（TN-29）。
- そして原告自身が譲っている：荒蕪地への立入りは合憲であることを ✓ *"do not dispute"*（ND-10）。
- ゆえに ✓ *"the statute is facially constitutional because there are applications of the statute that are
  constitutionally permissible."*（TN-27）——**第一審の文面違憲判断は破棄された。**
- 差止めは第一審で否定され、上訴されず、✓ *"we do not review the trial court's denial of injunctive relief."*（TN-41）。
- 残ったのは ✓ *"one dollar ($1.00) in nominal damages"*（TN-40）。

**観客はここで終わったと思う。**答えは「州は入れる」だと思う。錠は雨に濡れている（モチーフ状態3）。

そして——**ハードカット。別の州。**

> ペンシルベニアでは、同じ問いが別の裁判所に係属していた。**Commonwealth Court は 2023年9月29日にそれを退けていた**——
> テネシーの意見書が出る **7か月以上前**である（ID-03・PA-16・ID-06）。
> 両方の裁判所は、互いのことを知らない。ペンシルベニアの意見書で `Rainwaters` を検索すると、**0件**である。

**この順序を崩さない。弱い側を先に倒す映画は弱い。**テネシーの結論は本当に小さく、その小ささを削ってはならない。
それを最強の形で通してから折り返すことが、この映画の説得力の全部である。

**転回は「彼らが勝った」ではない。「答えが場所によって違う」である。**
reset beat（無音4秒・モチーフ状態4）を置く。⟨HELD⟩ は使わない（§7）。

### RECOGNITION（認知・アナグノリシス）— ACT_5 · 約 **26:20**（全体の 88%）

**一箇所だけ。**登場人物ではなく観客の中で起きる。

ペンシルベニアが線を引いた場所を、まず引用で置く。

> ✓ *"Truly open fields—i.e., private land that is unposted and unbounded—is fundamentally different in kind than
> private land conspicuously posted with 'no trespassing' signs and purple paint and/or bounded by fences, gates,
> and other structures."*（PA-28）

そのすぐ後に、**脚注24**。

> ✓ *"we reserve for another day the question of whether the privacy protections afforded by Article I, Section 8
> extend to landowners who have taken fewer steps than the Hunting Clubs, or even no steps, to exclude intruders
> from their properties."*（ND-01）

同時に画がモチーフ状態6に落ちる——**何も掛かっていない門柱。奥は空の畑。**
これは HOOK の最終画（0:17.8–0:20.3・空の畑）と**同一構図**である。26分ぶりに戻ってくる。

**ここで観客が自分で到達する結論はこうである。**
「守られたのは土地ではない。**紫のペイントと、腰の高さの針金と、公道側の門に掛けた錠**だった。
それを買えなかった人については、勝った裁判所自身が『またの日に』と書いた。」

**語り手はこれを言わない。**引用二つと画一つで足りる。**認知の直後に沈黙（⟨HELD⟩）。**

**二つ置かない。**
- ACT_1 の「門は法的な線ではない」は**期待の裏切り**であって認知ではない（そして PACKAGING が指定した反転点である）。
- ACT_3 末の「別の州があった」は**転回**であって認知ではない。
どちらにも ⟨HELD⟩ を与えず、「ここが本作の核心だ」式の宣言的な語りを一切付けない。**認知は一箇所。**

---

## 6. THE BEAT MAP（幕あたり13–17ビート・全ビートに台帳IDを付す）

契約の `section_vocabulary` は8キー固定：**HOOK, OP, ACT_1…ACT_5, ENDING**。台本の見出しはこの綴りに完全一致させる
（EP61 は `OPENING` と書いて下流に警告を出した）。

**語数配分**（30:00 設計・実測ペース 159.5–169.7 wpm・契約帯 4,565–5,247語／設計値 **≈4,800語**）

| 区分 | 時間 | 秒 | 目標語数 | ビート数 |
|---|---|---|---|---|
| HOOK | 0:00–0:20.3 | 20.3 | **48（PACKAGING 固定）** | 6 |
| OP | 0:20.7–0:32 | 11.3 | ≈34 | 2 |
| ACT_1 | 0:32–7:00 | 388 | ≈1,050 | **16** |
| ACT_2 | 7:00–13:00 | 360 | ≈960 | **15** |
| ACT_3 | 13:00–18:00 | 300 | ≈800 | **15** |
| ACT_4 | 18:00–25:00 | 420 | ≈1,120 | **17** |
| ACT_5 | 25:00–28:30 | 210 | ≈560 | **13** |
| ENDING | 28:30–30:00 | 90 | ≈230 | 4 |
| **計** | **30:00** | 1800 | **≈4,802** | — |

> **注意。**契約の `figure_beats_per_act: [13,17]` は**モーション図版ビート**の床であって、この節の**物語ビート**とは
> 別の指標である。両者を **1対1で対応させる**こと——各物語ビートに図版／タイポグラフィ／カット群を一つ割り当てれば、
> `motion_density` は設計から自動的に満たされる。**別々に数えると、どちらかが必ず落ちる。**

---

### HOOK — 0:00–0:20.3 · **PACKAGING §3 で承認済み。変更しない。**

割付は PACKAGING §3 の表がそのまま拘束する。ここでは**台帳との突合結果**だけを記す（詳細は §9）。

| # | ビート | 台帳 |
|---|---|---|
| H-1 | 「Henry County, Tennessee. 2017.」 | TN-13（93エーカーは Benton郡と Henry郡にまたがる）／TN-16（2017年11月30日） |
| H-2 | 州の野生動物取締官が、鎖の掛かった門と掲示された札の脇を通る | TN-13・TN-01 |
| H-3 | 木のところまで歩く | TN-16 |
| H-4 | **枝を切り落とし、その跡にカメラをボルトで留める**（"camera" が ≈0:13.2 に着地） | **TN-16 ✓ VERBATIM** |
| H-5 | 「Ninety-three acres.」 ← **PACKAGING の「A hundred and thirty-six acres」を修正（§9・§13-1）** | TN-13 |
| H-6 | 「Nobody tells the man who farms them.」／空の畑で保持 | **TN-02 ✓ VERBATIM**・TN-13 |

**HOOK が禁じるもの（PACKAGING §3）**：判決、「legal」「court」、教義名、両事件名、勝敗。
0:20 の時点で観客が知っているのは「農場の木にカメラが付いた。農場主は知らされない」だけであり、
**それが許されることなのかを知らない。**それが立っている問いである。

---

### OP — 0:20.7–0:32 · 教義（≈34語・ブランド帯が 20.5–24.0 に重なる）

| # | ビート | 台帳 |
|---|---|---|
| O-1 | 「Nobody has to.」（HOOK 直結の反転の種・PACKAGING 指定） | TN-02 |
| O-2 | **教義を、映画自身の言葉で一度だけ。**家の周りには curtilage と呼ばれる狭い輪がある。その外側の土地を、法は open field と呼ぶ。**そこに連邦憲法は届かない。** | PA-21（**原文引用は ACT_4 まで温存**）・PA-18・TN-26 |

**ここでペンシルベニアもテネシーも名指ししない。**PA-21 を原文で鳴らすのは 18:00 である（§3 プラント表）。

---

### ACT_1 — 0:32–7:00 · **THE LINE IS NOT WHERE YOU THINK IT IS**（16ビート）

| # | 時刻 | ビート | 台帳 |
|---|---|---|---|
| A1-01 | 0:32 | 93エーカー、Benton郡と Henry郡にまたがる。釣り、農、キャンプ、狩り。landlocked——隣人の砂利道と門を通らないと入れない | TN-13 |
| A1-02 | 0:44 | **モチーフ状態1。**入口の鎖の掛かった門。「No Trespassing」の札。ナレーション最小 | TN-13 |
| A1-03 | **0:52–1:05** | **反転（PACKAGING §5 指定）。**門を言う。鎖を言う。札を言う。そして——**そのどれも線ではない。線は家のずっと近くに引かれている。**モチーフ状態2 | PA-21・PA-18・TN-26・`forbidden_claims` 4 |
| A1-04 | 1:05–1:14 | **登録の依頼（9秒）。**§8 に全文 | — |
| A1-05 | 1:14–1:20 | **コメント質問（6秒）。**§8 に全文。20分後の 78日を仕込む | — |
| A1-06 | 1:20 | もう一人。Terry Rainwaters。136エーカーの本宅地（住宅二棟、"in a regular and conspicuous manner" に耕作）、69エーカー（全周フェンス＋鎖の門）、20エーカー（借地・landlocked・施錠門）、Harmon Creek の123エーカー（兄弟からの借地） | TN-09 |
| A1-07 | 2:10 | 安全のための取り決め——✓ *"hunters should know the location of everyone else on the property."* **人がどこにいるかを、全員が知っている土地である** | TN-10 |
| A1-08 | 2:40 | 2017年、三回。Kevin Hoofman が Harmon Creek に入り、写真を撮った | TN-11 |
| A1-09 | 3:10 | Hollingsworth 側の立入りは**一回**。**2016年12月21日**、deer baiting の調査、写真。当事者は、上訴で争点になるのはこの一回だけだと合意している | **TN-15** |
| A1-10 | 3:50 | 2017年11月30日、木にカメラ。**枝を一本切って**取り付けた。カメラの所有者は **United States Fish and Wildlife Service**。Rainwaters の土地にも同年11月に設置され、12月に外された。**これらが州の行為か連邦の行為かは、当事者間で争いがあり、決着していない** | **TN-16・ND-11** |
| A1-11 | 4:40 | 2017年12月、Hollingsworth の土地に入り、車を捜索し、その後 Hollingsworth を動画に撮った | TN-16 |
| A1-12 | 5:20 | ✓ *"The TWRA does not create records of all of its agents' entries onto private property and does not provide notice to property owners."* そして ✓ *"Officers enter private property, sometimes conceal themselves thereupon, and look for violations of wildlife laws."* | **TN-02・TN-03** |
| A1-13 | 5:50 | どこに入るかの決め方——以前に狩人を見た、噂、**銃声を聞く**。調査対象でない土地も、目的地へ行くために横切る | TN-04・TN-05 |
| A1-14 | 6:15 | 頻度の制限も、時刻の制限も、滞在時間の制限も無い。**判断のための成文方針も無い** | TN-06 |
| A1-15 | 6:35 | **何回入られたか、誰も知らない。**機関も知らない。二人も知らない | **TN-08** |
| A1-16 | 6:45 | **幕の転回。**二人は Benton郡の巡回裁判所に提訴した（三名の裁判官合議体）。機関が主張する権限は、✓ *"the statutory authority to go upon any property, outside of buildings, posted or otherwise"*——**ただしこれは機関の言い分の引用であり、意見書は条文そのものを一度も引いていない** | ID-06・ID-10・TN-07・⛔-15 |

---

### ACT_2 — 7:00–13:00 · **WHAT THE STATE SAYS IT MAY DO**（15ビート）

| # | 時刻 | ビート | 台帳 |
|---|---|---|---|
| A2-01 | 7:00 | テネシー憲法第1条第7節の全文。✓ *"persons, houses, papers and **possessions**"* | TN-23 |
| A2-02 | 7:40 | そこに無い語——***effects***。テネシーは1796年、1834年、1870年の三つの憲法で、それを選ばなかった | TN-24 |
| A2-03 | 8:10 | *Welch v. State*（1926）。✓ *"the word 'possessions' was added for a purpose"*／✓ *"refers to property, real or personal, actually possessed or occupied."* | TN-24 |
| A2-04 | 8:40 | **同じ文の中にある限界（プラント）。**✓ *"would not include wild or waste lands, or other lands that were unoccupied."* | **TN-25** |
| A2-05 | 9:00 | ✓ *"Tennessee has a robust history of protecting land outside the curtilage of a home as a 'possession'…"* | TN-26 |
| A2-06 | 9:20 | **州側の主張を、最強の形で。**✓ *"TWRA officers enter private property only when—and only in areas where— they believe hunting activity is taking place or has taken place."* | TN-34 |
| A2-07 | 9:50 | 州はまず「この件はもう終わっている」と言った——2018年9月以降、入っていない | TN-18 |
| A2-08 | 10:10 | 退けられた。機関は自らの行為が合憲だと ✓ *"insists"* し、提訴後も他人の土地に入り続けている。**狩りをしない人の土地にも入る** | TN-42・TN-20・TN-21 |
| A2-09 | **10:40** | **複雑さ（必須・省略不可）。**2018年11月、Hollingsworth の狩猟免許は、連邦の dove baiting 違反により**三年間停止された** | **TN-14** |
| A2-10 | 11:00 | **日付を並べる。**彼が訴えた立入りは **2016年12月21日**。停止処分は **2018年11月**。**23か月後である。**——評価は付けない。**⟨HELD⟩ 1本目** | TN-15・TN-14 |
| A2-11 | 11:25 | **記録が止まる場所。**この二人について、意見書は年齢を書かない。職業を書かない。なぜ訴えたのかを書かない。あるのは土地と、その使い方と、恋人と、恐れと、免許停止だけである | ○-05 |
| A2-12 | 11:50 | Rainwaters。使用を控えるようになった。客を招くのをためらう。監視への恐れ、そして**取締官を撃ってしまう恐れ**。✓ *"He testified that he felt 'exposed'…"* | **TN-12** |
| A2-13 | 12:10 | Hollingsworth。取締官が自分を、恋人を、客を見ているかもしれないと恐れ、訪問を減らした | TN-17 |
| A2-14 | 12:25 | 適用される原則は一行である。✓ *"warrantless searches and seizures are presumptively unreasonable."* そして機関は、令状の例外を**一つも援用しなかった**。黙示の同意の主張は ✓ *"waived."* | TN-35・TN-33 |
| A2-15 | **12:40** | **幕の転回。**では、州に入られたくない男はどうすればよいのか。口頭弁論で機関はこう答えた——✓ *"they should desist in hunting thereupon."* **reset beat（無音4秒）** | **TN-19** |

---

### ACT_3 — 13:00–18:00 · **THE ANSWER, AND ITS SIZE**（15ビート）

| # | 時刻 | ビート | 台帳 |
|---|---|---|---|
| A3-01 | 13:00 | 2024年5月9日、三名一致。Usman判事執筆、Goldin判事・Armstrong判事同調 | ID-07・ID-06 |
| A3-02 | 13:20 | 文面違憲の基準——✓ *"no set of circumstances exist under which the Act would be valid"*／✓ *"in all applications."* | TN-29 |
| A3-03 | 13:45 | そして原告自身が譲っていた。荒蕪地への立入りが合憲であることを ✓ *"do not dispute"* | ND-10 |
| A3-04 | **14:00** | ✓ *"the statute is facially constitutional because there are applications of the statute that are constitutionally permissible."* **第一審の文面違憲判断は破棄された** | **TN-27・⛔-02** |
| A3-05 | 14:25 | もう一つの理由。条文には ✓ *"work"* がある——それが無ければ、取締官の立入りは刑事不法侵入に当たる | TN-28 |
| A3-06 | 14:45 | 決めなかったこと。*Patel* の連邦基準がテネシーで妥当するかは判断していない | ND-07 |
| A3-07 | 15:05 | ここからもう半分。✓ *"Their lands were secured by gates, accessible only through private drives, and posted with 'no trespassing' signs intended to limit access to them. The Plaintiffs used and occupied their land by farming, fishing, camping, and hunting."* | **TN-30** |
| A3-08 | 15:30 | ✓ *"such activities, recreational though they may be, constitute actual use of the property."* | TN-31 |
| A3-09 | 15:50 | ✓ *"not wild or waste lands … but instead 'possessions' subject to constitutional protection."* **A2-04 の回収** | **TN-32** |
| A3-10 | 16:10 | 決め手。✓ *"each agent is empowered with the discretionary authority to determine for himself or herself…"*／✓ *"There is no clear system of judicial review…"* | TN-36 |
| A3-11 | **16:40** | ✓ *"The TWRA searches, which it claims are reasonable, bear a marked resemblance to the arbitrary discretionary entries of customs officials more than two centuries ago in colonial Boston."* | **TN-37** |
| A3-12 | 17:00 | ✓ *"what the TWRA claims is reasonable is not."*／§§ 70-1-305(1),(7) は**適用において**違憲。脚注50：機関は、なぜ相当な理由でなく合理的疑いで足りるのかを説明していない | TN-38・TN-39 |
| A3-13 | **17:20** | **それが何になったか。**差止めは第一審で否定され、上訴されず、審理もされていない。残ったのは ✓ *"one dollar ($1.00) in nominal damages"*——Ed Carter に対して。主権免責の主張は**中身を判断されず、waived** とされた。**形容詞を付けない** | TN-41・ND-08・**TN-40**・ND-09・⛔-14 |
| A3-14 | 17:30 | **モチーフ状態3。**雨。濡れた錠。条文は残っている。二人が持っているのは、宣言判決と一ドルである | — |
| A3-15 | **17:40** | **THE TURN。**ハードカット。別の州。Commonwealth Court は **2023年9月29日**に同じ問いを退けていた——テネシーの意見書の**7か月以上前**である。二つの裁判所は互いを知らない。ペンシルベニアの意見書に `Rainwaters` は **0件**。**reset beat（無音4秒・モチーフ状態4）** | ID-03・PA-16・ID-06・⛔-01 |

---

### ACT_4 — 18:00–25:00 · **THE OTHER ANSWER**（17ビート）

| # | 時刻 | ビート | 台帳 |
|---|---|---|---|
| A4-01 | **18:00** | **原文で。**✓ *"Open fields are afforded no constitutional protection from warrantless searches and seizure under the Fourth Amendment to the United States Constitution."* **OP の回収** | **PA-21** |
| A4-02 | 18:20 | Clearfield郡。**4,400エーカーと1,100エーカー**、いずれも連続した一筆。家は五棟と一棟。会員はそこに泊まる | PA-01・PA-02 |
| A4-03 | 18:45 | 会員がそこですること——狩り、ハイキング、スキー、標的射撃、そして ✓ *"find[] solitude in nature."* ✓ *"a private place—a sanctuary—where they can come to escape from the hustle and bustle of daily life."* | PA-03・PA-04 |
| A4-04 | 19:05 | 自分の土地を選ぶ理由。✓ *"strangers will not unexpectedly walk in and spook nearby wildlife or accidentally step into their line of fire."* | PA-05 |
| A4-05 | 19:25 | そこで話されること。✓ *"family matters, marital problems, work stressors, romantic feelings, and faith in God."* | **PA-06** |
| A4-06 | **19:50** | **手当ての一覧。**✓ *"posted their properties' boundary lines with clearly visible 'no trespassing' signs and purple paint, installed locked gates at all public entrances, and fenced some of their properties' boundaries with waist-high, metal wire…"* 紫のペイントは州法が認めた標識である（Philadelphia郡と Allegheny郡を除く）。公道沿いには常緑樹を植えて "screen" を作った。入れるのは会員、その客、業者、そして地下鉱業権を持つガス会社だけ | **PA-07**・PA-10・PA-08・PA-09 |
| A4-07 | 20:20 | Mark Gritzer。その地区の game warden。**公務としての資格で被告になっている**。**行為だけを言う** | PA-11・ID-01・⛔-07 |
| A4-08 | **20:40** | ✓ *"Since 2013, Warden Gritzer and other Commission officers have entered the Hunting Clubs' land without consent, a warrant, or probable cause **at least 15 to 22 times**…"* **この幅は裁判所自身の幅である。一つの数字に丸めない** | **PA-12**・○-06 |
| A4-09 | **21:10** | ✓ *"Warden Gritzer even placed a trail camera on Punxsutawney's property in an attempt to develop probable cause for charges of illegal elk feeding. That camera remained on Punxsutawney's property for **78 days**."* **1:14 のコメント質問の回収。数字を言って、止まる** | **PA-13** |
| A4-10 | 21:30 | ✓ *"On some occasions, Warden Gritzer has cited individuals for violations of the Code."* **意見書はこれ以上書いていない。**誰を、いつ、何で、その後どうなったかは記録に無い | PA-14・○-07 |
| A4-11 | 21:50 | 条文そのもの。§303(c)：✓ *"shall have the right and authority to go upon or enter any property, posted or otherwise, outside of buildings."* §901(a)(2)：✓ *"Go upon any land or water outside of buildings, **except curtilage**, posted or otherwise…"* | PA-17・PA-18 |
| A4-12 | 22:20 | *Russo*（2007）。狩猟解禁の ✓ *"approximately nine minutes after the opening of Pennsylvania's bear-hunting season"* に熊が撃たれ、取締官が掲示された私有林に令状なしで入り、apple mash の山と corn feeder を見つけた。Cappy長官が反対意見を書き、Baer判事と Baldwin判事が同調した | PA-38・PA-39 |
| A4-13 | 22:50 | 下級審。Commonwealth Court は en banc で、✓ *"it was bound by this Court's decision in Russo."* と結論した。McCullough判事は補足意見で、Cappy長官の**反対意見**に賛成すると述べた | PA-16 |
| A4-14 | **23:20** | **蝶番。**✓ *"the original meaning of the term 'possessions' as used in Article I, Section 8, unlike the term 'effects' as used in the Fourth Amendment, includes land."* **モチーフ状態5。reset beat（無音4秒）** | **PA-25** |
| A4-15 | 23:50 | 先例拘束。*Russo* は 18年余りで、公刊判例で適用された例が一つも無い。✓ *"the Court's reasoning and result in Russo have not aged well."*／✓ *"slavish adherence to our decision in Russo must give way…"*／✓ *"we hereby overrule Russo…"* | PA-26・PA-23・PA-22・PA-27 |
| A4-16 | 24:20 | **規則と命令。**✓ *"…extends to private land located beyond the curtilage over which the landowner has demonstrated a reasonable and legitimate expectation of privacy by taking sufficient steps to exclude intruders therefrom."* ✓ *"Government officials, therefore, must obtain a warrant based upon probable cause or satisfy one of the recognized exceptions…"* | PA-29・PA-30 |
| A4-17 | 24:40 | **処分。**§303(c) と §901(a)(2) は第1条第8節に違反する。**文面上**——✓ *"we cannot contemplate any circumstance under which Sections 303(c) and 901(a)(2) would be valid…"* 可分性は否定され、条項は全部倒れた。命令は破棄。**差戻しは無い**——striking したこと自体が求められた救済を与えたからである。四名が法廷意見に加わり、Todd長官と Wecht判事（McCaffery判事同調）が **concurring and dissenting** を書いた。**「全員一致」とも「4対3」とも言わない** | PA-31・PA-32・PA-33・ID-04・ID-05・**⛔-10** |

---

### ACT_5 — 25:00–28:30 · **HOW FAR THE NO REACHES**（13ビート）

| # | 時刻 | ビート | 台帳 |
|---|---|---|---|
| A5-01 | 25:00 | **変わらなかったもの。**✓ *"We, therefore, do not discuss and/or question the federal open fields doctrine further."* 連邦の教義はそのまま立っている | PA-36・ND-04・⛔-05 |
| A5-02 | 25:20 | **取締官がなおできること四つ、全文で。**掲示も柵も無い土地の令状なし捜索／掲示された土地でも plain view にある違反の観察／情報を得たうえでの令状取得／認められた例外の適用 | **PA-34** |
| A5-03 | 25:45 | さらに行政捜索。✓ *"Today's decision does not preclude administrative searches conducted pursuant to an appropriate statutory framework…"*（Donohue補足意見）。同意見は、機関が自分の準備書面で **open fields の教義と行政捜索の例外を取り違えている**とも書いた | PC-06・ND-05・PC-05 |
| A5-04 | 26:00 | §901(a)(8)（行政検査）は倒れていない。✓ *"We are not declaring that section constitutional, although it is presumptively so until a court decides otherwise."* | ND-03 |
| A5-05 | 26:15 | 環境権修正（第1条第27節）は下げられていない。✓ *"not a diminution of the importance of our citizens' right to the conservation, maintenance, and protection of wildlife under the ERA."* | PA-35・PC-03・PC-07 |
| A5-06 | **26:20** | **RECOGNITION。**PA-28（"Truly open fields…"）→ **脚注24**（ND-01）。**モチーフ状態6**——錠の無い門柱、空の畑。**HOOK 最終画と同一構図。⟨HELD⟩ 2本目** | **PA-28・ND-01** |
| A5-07 | 26:55 | そして境界のもう一方も、同じ形をしていた。1926年の *Welch* が除いたのは ✓ *"wild or waste lands, or other lands that were unoccupied."* 2024年に保護を認めた根拠は、門と、私道と、札と、**実際に使っていたこと**だった。**接続語を使わない（§12）** | TN-25・TN-30・TN-32 |
| A5-08 | 27:15 | ペンシルベニアは適用範囲も限った。✓ *"we cannot ignore that this case is about rural, undeveloped land, not a suburban one-acre plot…"* ✓ *"We resolve only the question of whether the Hunting Clubs here have done so."* | ND-02 |
| A5-09 | **27:40** | **タイトルの画のペイオフ。**枝。カメラ。車内捜索。動画。**そのどれも、上訴の争点ではなかった**——当事者が争点としたのは、Hollingsworth については 2016年12月21日の一回だけである。そしてカメラの件が州の行為だったのか連邦の行為だったのかは、✓ *"The parties dispute…"* のまま**決着していない** | **TN-15・TN-16・ND-11** |
| A5-10 | 28:00 | **二人が持っているもの。**適用違憲の宣言、差止め無し、一ドル。条文はテネシーの法令集に残っており、**文面上は合憲**である。**⟨HELD⟩ 3本目** | TN-22・TN-40・TN-41 |
| A5-11 | 28:15 | **クラブが持っているもの。**二つの条文が消え、差戻しも無く、求めた救済がその場で与えられた | PA-31 |
| A5-12 | 28:22 | どちらの判決も、相手の州には何も及ばない。どちらも合衆国憲法修正第4条については何も決めていない | ND-12・⛔-05・⛔-06 |
| A5-13 | 28:26 | **知らないことを言う。**テネシーが州最高裁へ上訴したかどうかは、この記録では分からない。2026年7月21日以降ペンシルベニアで何が起きたかも分からない。**言わない（⛔-12）** | ○-02・○-03・○-01 |

---

### ENDING — 28:30–30:00 · **新事実ゼロ**（4ビート）

| # | 時刻 | ビート |
|---|---|---|
| E-1 | 28:30 | **モチーフ状態7。**状態1と同一構図。朝の光。閉じた錠。**ナレーションは錠に一言も触れない** |
| E-2 | 28:45 | 再フレームだけ。何一つ新しい事実を出さない。同じ行為、同じ門、二つの答え。**そして片方の裁判所は、自分の「否」がどこまで届くかを書かなかった** |
| E-3 | 29:20 | **獲得された Like の依頼（行10・最後の30秒以内）。**「この30分で、自分の土地のどこに線が引かれているかの見え方が変わったなら、Like を押してほしい」——**感情命令にしない。sequel を約束しない** |
| E-4 | 29:35 | ⟨HELD⟩ 3本目の直後に最終画 → `BrandEndcard`（`ENDCARD_SEC = 9`・`Bookends.tsx` 正典・fork 禁止） |

**ENDING に出してよい数字はゼロ個である。**「一ドル」も「78日」も「15から22回」も、すべて本編で済ませてある。

---

## 7. REGISTER — 声の設計

**観客の実測**：92%男性・76%が55歳以上。**制度と権力の観客**である。

- **判決記録の平明さ。**修飾を削る。形容詞は事実が持つものだけ。
- **感情命令ゼロ。**「想像してみてください」「衝撃的なことに」は一つも書かない（`check_script_craft.py` が機械で落とす）。
- **語り手は結論を言わない。**一ドルも、78日も、23か月も、**平叙で一度言い、形容詞を付けない。**
  ✓ *"The remedy was one dollar."*
  ✗ 「たった一ドルである」——観客の仕事を奪う。
- **他人の語り直しに反論しない。**「よく誤解されるが」「多くの解説はここを間違える」は**すべて削る**。
  **正しいことだけ言えば、間違いは勝手に消える。**
- **最良の台詞は既に書かれている。**そのまま鳴らす：
  *"they should desist in hunting thereupon."* ／ *"colonial Boston."* ／ *"or even no steps."* ／ *"have not aged well."*
- **短文を武器に使う。**30語超の助走を5語以下で切る。各幕に最低1回。
  「*Twenty-three months earlier.*」「*Zero hits.*」「*One dollar.*」「*Seventy-eight days.*」
- **日付がリズムである。**2016年12月21日／2017年11月30日／2018年11月／2018年9月／2023年9月29日／2024年5月9日／
  2025年4月9日／2026年7月21日。平叙で言えば、それが時計の役をする。
- **仕組みの説明は一文で済ませ、あとは見せる。**文面違憲と適用違憲、名目的損害、破棄と差戻し——各一行。段落にしない。
- **法域を一文ごとに分ける。**州憲法の話と連邦憲法の話を同じ文に混ぜない（契約 `forbidden_claims` 4）。

**運用目標**（一周目からこの帯で書く）

| 指標 | 目標 |
|---|---|
| 短文（6語以下）比率 | 20–35% |
| 修辞疑問 | ≤2 / 1000語（§8 の設問は本数で管理し、修辞疑問に数えない） |
| 二人称 | ≤8 / 1000語（コメント質問と Like 依頼で使い切る想定） |
| 30語超の助走→5語以下で切る | 各幕に最低1 |

**沈黙（⟨HELD⟩）は三箇所だけ。すべて「重い一文の後」に置く。**
1. **A2-10 の直後**（「23か月前である」の後）
2. **A5-06 の直後**（脚注24の後）
3. **E-3 の後・最終画の前**

**⟨HELD⟩ を「これから重い一文が来る」という予告に使わない。**沈黙は前の一文が重いときだけ効く。
これとは別に **reset beat（画の休符・無音4秒）を三箇所**置く：A2-15（"desist in hunting"）／A3-15（THE TURN）／A4-14（"includes land"）。
**合計で無音は7箇所を超えない。**

---

## 8. RETENTION MAP（行16・再フックと設問）

実測：10秒87.6% → **15秒76.9%** → 20秒71.4% → 30秒60.4%。**最大の落下は 10→15秒で毎秒2.13ポイント**。
60秒時点で43%が残っている。30分時点ではほとんど残っていない。**依頼は前に置く。**

| 位置 | 再フック |
|---|---|
| 0:00 | HOOK（PACKAGING 固定・**0:00から声がある**） |
| **0:09.9–0:15.0** | **最強のビート（枝とカメラ）が、毎秒2.13ポイント落ちる窓の真上に来る** |
| 0:52 | 門も鎖も札も、法的な線ではない |
| **1:05–1:20** | **登録の依頼 → コメント質問（下記）** |
| 2:10 | 全員が、他の全員がどこにいるかを知っている土地 |
| 3:50 | 枝を切ってカメラを付けた。所有者は連邦機関だった |
| 5:20 | 記録は取られない。通知もされない。取締官は身を隠すことがある |
| 6:35 | **何回入られたか、誰も知らない** |
| 7:40 | テネシーが選ばなかった語——*effects* |
| 8:40 | *"wild or waste lands, or other lands that were unoccupied."* |
| **10:40** | **免許停止（2018年11月）→ 23か月** ⟨HELD⟩ |
| 11:50 | *"exposed"* |
| **12:40** | ***"they should desist in hunting thereupon."*** reset beat |
| 14:00 | **文面上は合憲。第一審が破棄される** |
| 15:30 | *"recreational though they may be, constitute actual use"* |
| 16:40 | *"colonial Boston."* |
| 17:20 | **一ドル** |
| **17:40** | **THE TURN——別の州。0件** reset beat |
| 19:50 | 紫のペイント、施錠された門、腰高の針金 |
| 20:40 | 2013年以降、**少なくとも15回から22回** |
| **21:10** | **78日**（1:14 の回収） |
| 22:20 | 解禁から**九分後**に撃たれた熊 |
| 23:20 | *"possessions" … "includes land."* reset beat |
| 24:40 | **差戻しは無い** |
| 25:20 | それでも取締官にできること、四つ |
| **26:20** | **RECOGNITION——脚注24** ⟨HELD⟩ |
| 27:40 | **枝は、争点ではなかった** |
| 28:30 | ENDING（新事実ゼロ） |

**最大間隔は 17:40 → 19:50 の 130秒。**150秒の上限内。20秒を超える平坦な説明区間は作らない。

### 立てる問い（7分に最低1回・少なくとも6本）

| 位置 | 問い |
|---|---|
| 0:20 | （不問のまま立っている）カメラが付いた。それは許されることなのか |
| **1:14** | **コメント質問（下記）** |
| 6:35 | 誰も書き留めなかったものを、どう数えるのか |
| 12:35 | では、州に入られたくない男は何をすればよいのか →（機関の答え・TN-19） |
| 17:40 | これが答えである。**別の場所に立っていない限り** |
| 24:45 | この判断は、実際にはどこまで届くのか |
| 26:20 | （裁判所自身が保留した問い・ND-01） |

### 登録の依頼 — **1:05–1:14（9秒）**・反転の直後

> **"There are more cases like this one on the channel already, and there are more coming. If you want them, subscribe."**

- 「more like this one already」＝真（公開長尺55本・令状／捜索／押収のカタログ）。
- 「more coming」＝真（12:00 JST 枠は埋まっている）。**この話の続編は約束しない。**
- 「smash」「もし腹が立ったら」等の感情命令は使わない。**Like の依頼はここに入れない**（ENDING の E-3）。

### コメント質問 — **1:14–1:20（6秒）**・一度だけ話す

> **"If a camera went up on your land today — strapped to a tree, lens pointed at your field — how long before you found it?"**

答えられる（誰でも数を持っている）。この回に固有である。Yes/No ではない。感情を要求していない。
**そして 21:10 の「78日」がその答えになる。**そこで語り手は何も言わない。

> ⚠ **PACKAGING §5 との差分（オーナー承認が要る）。**承認済みの文言は
> *"The camera in Pennsylvania stayed up for 78 days before anyone found it. If one went up on your land today, how
> long before you found it?"* である。**1:14 の時点でこの映画はまだペンシルベニアに入っておらず、78日は 21:10 の
> ペイオフである。**承認文言をそのまま話すと、20分ぶんのプラントを冒頭で使い切る。
> **提案：話す版は上記に差し替え、固定コメントと概要欄の2行目には承認済み文言をそのまま使う。**
> これは PACKAGING の変更であり、**v002 と APR が要る。設計書は勝手に決めない。**

---

## 9. HOOK — **既に書かれ、承認されている**（PACKAGING §3・行9）

行9は EP66 から拘束する：**ナレーションは 0:00 から鳴り、フックは約20秒あり、最初に書かれる。**
EP66 のフックは既にその通りに書かれている。**この設計書はそれを変更せず、着地点として受け取る。**

### FACT-LOCK の解決（PACKAGING §3 が R2/R3 に委ねた三点）

| # | PACKAGING の未確定 | 台帳による解決 |
|---|---|---|
| 1 | **`[YEAR]`** | **2017。**カメラ設置は 2017年11月30日（TN-16）。**近似しない。** |
| 2 | 「steps past a locked gate and a posted sign」 | **支持される。**Hollingsworth の土地は ✓ *"behind a chained gate at the entrance to his property with a 'No Trespassing' sign"*（TN-13）。ただし **"locked"** ではなく **"chained"** が原文語であるため、ナレーションは *"a chained gate and a posted sign"* とする。 |
| 3 | 「Nobody tells the man who farms them」 | **支持される。**✓ *"does not provide notice to property owners"*（TN-02）。彼は farming にその土地を使っている（TN-13）。 |

### ⚠ 承認済み HOOK の中の事実誤り（**修正が要る・§13-1**）

PACKAGING §3 の 0:15.7 行は **"A hundred and thirty-six acres."** であり、同 §1 の注記は
「the cut branch, the 136 gated acres … are Rainwaters」と書いている。**台帳はそう言っていない。**

- **136エーカーは Terry Rainwaters の本宅地**（TN-09）。
- **枝を切ってカメラを付けられた木は Hunter Hollingsworth の土地**にある（TN-16）。彼の土地は
  ✓ *"approximately **93 acres** crossing Benton and Henry Counties"*（TN-13）。
- **Henry County** は Hollingsworth の土地がまたがる郡である（TN-13）。**Rainwaters の土地の郡は台帳に無い**（§13-2）。

つまり承認済みフックは、**Henry郡（Hollingsworth）＋切られた枝（Hollingsworth）＋136エーカー（Rainwaters）** を
一人の男に合成している。**invariant 1 違反であり、そのままでは録音できない。**

**最小修正（他の全ビート・全カット・全タイミングを保存する）**

> 0:15.7–0:17.5 の **"A hundred and thirty-six acres."** を **"Ninety-three acres."** に置き換える。

音節数が減るため 0:15.7–0:17.5 の枠に余裕が出る。**間を詰めず、後続の 0:17.5 の hold を 0.3秒 → 0.6秒に伸ばして吸収する。**
MOTIONKIT のカウントアップ図版は **136 → 93** に変更する。
タイトル T1／T3 の *"The Case of Terry Rainwaters"* は**変更不要**——事件の caption が
*Terry Rainwaters et al. v. TWRA* であり、Rainwaters は筆頭原告だからである（ID-06）。
**この修正は PACKAGING v002 として記録する。**

### HOOK が本編に負わせた義務（すべて §6 に配線済み）

| フックの要素 | 回収先 |
|---|---|
| 空の畑（0:17.8–0:20.3） | A5-06・モチーフ状態6（**同一構図・26分後**） |
| 枝とカメラ（0:09.9–0:15.0） | A1-10（記録として）→ A5-09（**争点ではなかった**） |
| 「Nobody tells…」 | A1-12（TN-02 原文）→ OP の「Nobody has to.」が教義になる |
| 木に向けられたレンズ | A4-09（78日）→ A5-09 |

**HOOK に判決・勝敗・教義名・事件名を入れない。**0:20 の時点で問いは立ったまま出る。

---

## 10. WHAT THE IMAGES MUST CARRY

語りが説明を降りる代わりに、画が論証を持つ。Codex 発注書はこの節に従属する。
契約値（2026-08-11 時点の episode_spec.v001.json と一致）：**distinct_video_assets 308／still cuts 164／target_cut_sec 3.1／people_plates 20**。人物プレート L235-L254 は顔を写す方針（実在人物の肖像のみ禁止）で、初稿の「10枚・無顔」から改定済み。

- **境界の語彙で全編を通す。**門、鎖、錠、針金、紫の帯、砂利道、轍、幹、林縁、畑の縁、朝霧。
  **法廷は一度も映さない**（契約 `forbidden_subjects` が courtroom・gavel・judge・jury を禁じている）。
  **判決の15分間は、土地とタイポグラフィと図版だけで持たせる。**それがこの映画の様式である。
- **読める文字は Remotion のタイポグラフィと MOTIONKIT 図版だけに存在する。**生成プレートには一文字も焼かない。
  掲示標識は**風化した無地の板・角度・色**として発注する。**紫のペイントは文字ではなく色である**（PA-10）。
- **二つの州を画で区別する。17:40 のカットで観客が「移動した」と体で分かること。**
  - **テネシー** — 中部テネシーの平坦な農地、川底、砂利の私道、鎖と南京錠、低い冬の光、湿った土。
  - **ペンシルベニア** — アパラチアの落葉樹林、起伏、腰高の金属針金、幹の**紫の帯**、公道沿いの常緑樹の列。
- **人は後ろ姿・手・長靴・霧の中の遠景のみ。**顔が出た瞬間、観客は「その人の物語」を探し始める。
  **この映画にそれは無い**（実在人物の肖像は全面禁止・⛔-11）。
- **カメラは、小さくて安っぽい灰色の樹脂の箱である。**緑のナイトビジョン、十字線、CCTV グリッド、
  サーマルの偽色は禁止（契約散文規則）。**地味であることがこの物語の要点である。**
- **⚠ 罠：`forbidden_subjects` に `drone` が入っている。**PACKAGING §3 は空撮プレートを指定している。
  空撮そのものは問題ないが、**カットや素材の名称・キーワードに `drone` の語を入れると
  `check_spec_satisfied.py` が落とす。**`aerial farmland` 等で発注・命名すること。
- **狩りの獲物、銃、剥製は一切映さない。**原告が hunting club であっても、この映画は財産権の映画である。
- **既存棚の実測（PACKAGING §2・2026-08-10）**：woodland/forest 8（3840×2160 のプレート含む）・
  misty forest at sunrise 6・barbed/wire fence と padlock-in-fence 8+・farmland aerial 5・no trespassing sign 1・
  deer in forest 5+。**`farm gate metal`／`trail camera tree`／`wooden gate path` は 0件** ——
  門・カメラ筐体・切株は**生成プレート**で作る。**350点に届くかは register ごとに実測してから確定する**（契約 notes）。

---

## 11. THE LINE THE FILM IS BUILT ON

映画が向かう一文。

> ✓ ***"we reserve for another day the question of whether the privacy protections afforded by Article I, Section 8
> extend to landowners who have taken fewer steps than the Hunting Clubs, or even no steps, to exclude intruders
> from their properties."***
> — ND-01（PA-LEAD 脚注24・原文照合済）

**この一文の意味は、「勝った側の裁判所が、自分の否がどこまで届くかを言わなかった」である。**

法が立っていた場所を示す一文。

> ✓ ***"Open fields are afforded no constitutional protection from warrantless searches and seizure under the Fourth
> Amendment to the United States Constitution."***
> — PA-21（PA-LEAD 一行目・原文照合済）

そして真ん中に置く一文。

> ✓ ***"the TWRA asserted at oral argument that, if the Plaintiffs wish to avoid reentry by the TWRA upon their
> properties, they should desist in hunting thereupon."***
> — TN-19（原文照合済）

**PA-21 が法の初期状態、TN-19 が中点、ND-01 が終点。**台帳の「THE SHAPE THE FACTS ALREADY HAVE」が既にそう書いている。
唯一の差は配置である——PACKAGING がフックを固定したため、**PA-21 は 0:00 ではなく 18:00 に原文で鳴る**（§3 プラント表）。

---

## 12. WHAT THIS FILM IS NOT ALLOWED TO SAY

契約の `forbidden_claims` と台帳の ⛔ 全15項目がここに拘束する。とくに：

- **二つの事件を繋がない（⛔-01・最重要）。**「ペンシルベニアはテネシーに続いた」「一方が他方を引用した」
  「一つの運動の二つの段階」は**すべて捏造**である。`Rainwaters`・`Hollingsworth`・`Tennessee Wildlife` は
  ペンシルベニアの意見書に **0件**である。
  **接続語の禁止リスト**：*meanwhile / likewise / similarly / just as in Tennessee / following / in the wake of /
  the same fight / elsewhere the same*。
  **二つの記録を並べてよいのは、直前に「この二つは互いを知らない」と述べた場合だけ**であり、
  並べ方は**接続語ではなく、ハードカット＋新しい州名＋新しい日付＋新しい憲法条文**である。
- **「テネシーは法律を無効にした」と言わない（⛔-02）。**✓ *"facially constitutional but unconstitutional as
  applied."* 第一審の文面違憲判断は**破棄された**。**両方言うか、どちらも言わないか**である。
- **「TWRA は立入りを禁じられた」と言わない（⛔-03・ND-08）。**差止めは否定され、審理もされていない。
- **「ペンシルベニアでは私有地に入るのに令状が要る」と平叙で言わない（⛔-04）。**
  規則は**十分な手当てをした土地**にしか及ばず、PA-34 の四つは残り、行政捜索も残っている。
- **「ペンシルベニアが open fields の教義を廃止した」と言わない（⛔-05）。***Hester* と *Oliver* は立っている。
  **「第1条第8節のもとで」を毎回付けるか、その行を削るか**である。
- **数字を一つも足さない（⛔-06・○-04）。**「96%」も、面積の割合も、州の数も、台帳に無い。
  **唯一の量的表現は「at least 15 to 22 times」「78 days」「three years」「23 months」「one dollar」だけ**で、
  すべて原文の数字である。**15–22 を「約20回」に丸めない。**
- **Gritzer と Hoofman の動機・性格・非行を一言も言わない（⛔-07・⛔-08）。**記録が支えるのは行為だけである。
  **意見書は Gritzer が違法なことをしたとは言っていない。**
- **Hollingsworth を無垢な狩人として描かない。免許停止を落とさない（⛔-09）。**
  同時に、それが立入りを**正当化した**と匂わせない。立入りは 23か月**前**である。
- **ペンシルベニアの判決を「全員一致」とも「4対3」とも言わない（⛔-10）。**
  Todd と Wecht（McCaffery 同調）は **concurring and dissenting** であり、その内容は読まれていない（○-01）。
  **法廷意見の脚注に出る二つの引用を超えて性格づけしない。**
- **一ドルを「賠償を勝ち取った」と言わない（⛔-14）。**名目的損害である。
- **Tenn. Code Ann. § 70-1-305(1)(7) の条文を「引用」しない（⛔-15）。**意見書は一度も引いていない。
  画面に条文カードを出すなら、**先に法令集そのものを読む**（○-08）。
- **その後どうなったかを語らない（⛔-12）。**記録は 2024年5月9日と 2026年7月21日で終わっている。
- **生成映像を本物の記録として提示しない（⛔-11・invariant 11）。**両事件とも実在の人物と実在の区画である。

**沈黙している記録に声を当てない。**それがこの映画の品位であり、同時にこの映画の主題でもある。

---

## 12.5 AFTER EFFECTS キネティック文字 — **3ビート**（設計に明記・2026-08-11 追記）

`scripts/check_design_doc.py` が 70/72 で落とした2項目のうちの1つ。**ビートは既に作ってあったのに、
この設計書にも画像発注書にも After Effects の四文字が一度も出てこなかった。**承認済みの機能が
使われないのは、いつもこの形で起きる（`docs/PD_CANON.md` の AE 節）。だからここに書く。

オーナー承認（2026-08-04）の使い方は「**中盤の数字と転換に1〜2回**」。この話は数字が3つあり、
どれも土地を持つ人の腹に来る種類なので3回にする。実体は
`scripts/ae/jobs_ep66_openfields.json`、書き出しは `scripts/ae/render_beats.sh`、
出来たクリップは film.json にカットとして置く。

| id | 画 | 秒 | 乗る台本行（台帳） |
|---|---|---|---|
| `ep66_kin_78_days` | **78** ／ DAYS ON HIS TREE | 2.4 | カメラは78日間そこにあった（PA-13）・ACT_4 |
| `ep66_kin_22_times` | **15–22** ／ ENTRIES. NO WARRANT. | 2.4 | 令状も同意も相当な理由もなく、少なくとも15〜22回（PA-12） |
| `ep66_kin_one_dollar` | **ONE DOLLAR** | 2.4 | 州が争ったのは1ドル（TN-40） |

**15–22 は丸めない。**判決文はこの幅を一度も狭めておらず、○-06 が丸めを禁じている。だから
両方の数字を画面に出す。

**置き場所の規則**：3つとも中盤（ACT_3〜ACT_5）に置き、**フックとENDINGには置かない**。
フックは声と実景で持たせる区間であり、ENDINGは新事実ゼロの区間だから。

## 12.6 字幕をどこで切るか（設計に明記・2026-08-11 追記）

落ちた2項目のもう1つ。**息継ぎ単位で切る。**画面の横幅で切らない。

- 分割は文法単位（`scripts/polish_captions_srt.py` の `_smart_split`）。
  前置詞・冠詞・接続詞で行を終わらせない
- 1キューは **最長 6.8 秒**（`MAX_CUE_SECONDS`）。EP65 で、設計された無音をまたいで
  2文が1キューに融合し 8.56 秒になった事故の再発防止
- 物理行は 50 字以内、CPS は 27 以下
- **リードは 0.60 秒**（この話の宣言値。`filmconfig` の `captionLeadSeconds` が正典で、
  house 既定の 0.25 ではない）。リードは**行き先であって加算値ではない**——
  `captions.final.v001.lead.json` が「既に入っている量」を持ち、差分だけを適用する
- 検査：`check_caption_breaks` / `caption_format` / `caption_narration_match`（100%一致）

## 13. THE LIST — 欲しかったが、台帳が持っていないもの

**この節がこの文書で最も価値のあるページである。**以下はいずれも**書かなかった**。書く前に、行を作るか、形を変える。
番号順は「これが埋まらないと台本が止まる」順である。

### 台本を止めるもの（**着手前に閉じる**）

| # | 欲しかった事実 | なぜ必要か | 台帳の状態 | 埋まらない場合にとる形 |
|---|---|---|---|---|
| **1** | **承認済み HOOK の「136エーカー」が誰のものか** | フックが Henry郡（Hollingsworth）＋切られた枝（Hollingsworth）＋136エーカー（Rainwaters）を**一人に合成している**。PACKAGING §1 の注記（「the cut branch … are Rainwaters」）も台帳と一致しない | **矛盾。**TN-13＝Hollingsworth 93エーカー（Benton・Henry郡）／TN-09＝Rainwaters 136エーカー／TN-16＝枝を切ったのは Hollingsworth の木 | **§9 の最小修正**：0:15.7 を **"Ninety-three acres."** に置換。**PACKAGING v002 ＋ APR が要る** |
| **2** | **テネシーが州最高裁へ上訴したか（○-03）** | 台帳自身が「**エンディングを一語でも書く前に確認せよ**」と書いている。上訴中なら A5-10 と ENDING は「暫定」であり、確定として語ると誤りになる | **未取得。**2024年5月9日の控訴審意見書からは分からない | 確認できなければ、A5-13 で「この記録ではその先は分からない」と**言い切る**（⛔-12 準拠）。**推測で「確定した」と書かない** |
| **3** | **コメント質問の 78日をどこで話すか** | 承認文言は 1:14 でペンシルベニアと78日を名指しし、**21:10 の20分プラントを冒頭で使い切る** | PACKAGING §5 が承認済み・変更にはオーナー判断が要る | **§8 の提案**：話す版を差し替え、固定コメント／概要欄は承認文言のまま。**PACKAGING v002 ＋ APR** |

### 形を変えれば書けるもの

| # | 欲しかった事実 | なぜ必要か | 台帳の状態 | とる形 |
|---|---|---|---|---|
| 4 | **Rainwaters の土地がある郡** | フックは郡名で開く。彼で開くなら郡が要る | **無い。**巡回裁判所は Benton郡（ID-06）だが、それは**裁判所の郡**であって土地の郡ではない | フックは Hollingsworth（Henry郡・TN-13）で開く。**Rainwaters に郡名を付けない** |
| 5 | **ペンシルベニア事件の提訴年** | 「2021年に提訴され、2026年に決着した」は転回を強くする | **無い。**あるのは docket `No. 456 MD 2021` と Commonwealth Court の命令日 2023年9月29日（ID-03） | 「**2023年9月29日に Commonwealth Court が退けていた**」と言う。**docket 番号から提訴年を推論しない** |
| 6 | **Hester (1924) と Oliver (1984)** | 連邦教義の背景を一文で置きたい | 台帳の ⛔-05／ND-04 に**名前だけ**出る。**判決年を検証した行が無い** | 教義は **PA-21 を根拠に映画自身の言葉で**述べる（OP）。**事件名と年を口に出さない**。出すなら先に行を作る |
| 7 | **二つの土地の距離** | 「州境の向こう」を体感させたい | **無い**（Clearfield郡 PA と Benton/Henry郡 TN の距離を書いた行は無い） | 距離を言わない。**画で移動させる**（§10 の樹相・地形の差） |
| 8 | **Hollingsworth の木からカメラが外された日** | モチーフの「カメラは消え、傷だけが残る」を事実で支えたい | **無い。**Rainwaters の土地のカメラは 2017年12月に外された（TN-16）が、Hollingsworth の分は記録が無い | カメラの撤去を語らない。A5-09 は**争点ではなかったこと**と**帰属未決**で構成する |
| 9 | **15–22回の立入りの中身**（日時・滞在時間・カメラが何を写したか） | ACT_4 に人間の細部が欲しい | **無い（○-06・○-07）。**PA-12 と PA-13 が記録の全部 | 幅をそのまま言う。**「約20回」に丸めない。**細部の代わりに **PA-06 の会話の一覧**を人間の材料として使う |
| 10 | **取締官が門をどう越えたか**（乗り越えた／迂回した／水路から） | モチーフ状態2「錠は閉じたまま、向こう側に足跡」を**事実として**語りたい | **無い。**TN-01 は「入った」としか書いていない | **画では出してよい。ナレーションでは語らない。**（EP65 の「机」と同じ扱い） |
| 11 | **ペンシルベニア側の個人** | 行15 の「human throughline」を両幕で通したい | **無い。**原告は member-owned clubs で、意見書は会員を一人も名指ししない（PA-01） | 縦糸は **Hollingsworth**（§2）。ACT_4 の人間材料は **PA-06 の一覧**と **PA-04 の "sanctuary"** だけで作る。**会員を創作しない** |
| 12 | **Todd・Wecht・McCaffery・Mundy が実際に書いたこと（○-01）** | 分裂を語れれば ACT_4 の結末が厚くなる | **未読。**法廷意見の脚注2箇所の言及だけ | 票数の算術（ID-04・ID-05）と「concurring and dissenting」という語だけを言う。**性格づけしない（⛔-10）** |
| 13 | **Tenn. Code Ann. § 70-1-305(1),(7) の条文（○-08）** | 二州の条文を並べる画（PA §303(c) / §901(a)(2) の隣）を作りたい | **無い（⛔-15）。**意見書は一度も引いていない | **ペンシルベニア側だけ条文を出す。**テネシー側は **TN-07（機関の言い分）** として明示的に区別して出す |
| 14 | **2026年7月21日以降のペンシルベニア（○-02）** | 「で、どうなったのか」に答えたい | **無い** | A5-13 で分からないと言う。**立法対応も運用変更も語らない（⛔-12）** |
| 15 | **教義が及ぶ土地の量（面積・割合・州の数）** | 賭け金を横に上げたい | **禁止（⛔-06・○-04・○-09）。**96% は出典が HTTP 403 で検証できない | **賭け金は縦に上げる**（§4）。数字は一つも足さない |

---

*Built 2026-08-10. 参照した拘束文書：`EP66_openfields_FACTS_LEDGER.v001.md`（98 fact rows）・
`EP66_openfields_PACKAGING.v001.md`（承認済み前面）・`episodes/PD-2026-066-openfields/episode_spec.v001.json`・
`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` 行9/10/15/16・`EP65_marmet_FILM_BIBLE.v001.md`（構造の手本）。
**この文書は事実を一つも作っていない。**本文の全ビートは台帳の行IDを持ち、持てなかったものは §13 に置いた。
台本一周目はこの設計書に従属する。§13 の 1〜3 が閉じるまで、台本は書き始めない。*

---

> **Correction, 2026-08-12.** `distinct_video_assets` was corrected in `episode_spec.v002.json` because the original figure was never derived from the allocator. Superseded numbers may remain in the body above for provenance; the spec is authoritative. See `decisions/0009-DISTINCT-VIDEO-ASSETS-CORRECTION.md`.
