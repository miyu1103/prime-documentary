# PACKAGING_FIX v001 — 公開済み動画のタイトル／サムネ改修提案

**作成:** 2026-07-19
**対象:** すでに公開済みの動画（トラックB）
**性質:** **提案書のみ。YouTube側は一切変更していない**（API書き込み・アップロード・サムネ差し替えなし）。実行はオーナー承認後。

---

## 0. 前提と測定の限界

### 使用したデータ（実測・2026-07-19取得）
- YouTube Analytics `2026-05-01 .. 2026-07-18` / 47本
- チャンネル計: **2,093 views / 平均視聴率 20.5% / 登録+2 / コメント0**
- 内訳（joined.json 47本の集計）: **長尺25本=619 views** / **ショート22本=1,340 views**
  → **視聴の68%はショートが稼ぎ、長尺は32%**。しかし登録・視聴時間の源泉は長尺。
- Studio（2026-07-04時点）: **サムネ表示回数 9,655 / CTR 2.31%**（目標 ≥4%）

### ⚠️ 測定の限界（重要）
**動画別CTRは今回更新できなかった。** `secrets/studio_cookies.txt`（2026-07-04取得）が **HTTP 401** を返すため、
YouTube Studio側の表示回数・動画別CTRは再取得不能。
したがって本提案の優先順位は **views + 視聴維持率(avp) を代理指標** として組んでいる。

- **views が低い** = 露出が回っていない（サムネ／タイトル／初速のいずれか）
- **avp が高いのに views が低い** = **中身は良い。パッケージだけがボトルネック** ← 最も投資効率が高い
- **avp が低い** = タイトルの約束と冒頭が食い違っている疑い（＝タイトルが不正確 or 抽象）

改修の効果検証には Studio Cookie の再取得が必須。**実行前に cookie を更新すること**（変更前後の CTR 比較ができないと、この施策は「やったが測れない」で終わる）。

---

## 1. 改修ルーブリック（実測から導いた3原則）

| # | 原則 | 根拠（実測） |
|---|---|---|
| **R1** | **「権力があなたに何をできるか」＞「有名な犯罪・詐欺の物語」** | ショート: 権利/警察系 n=12 → 1,068 views・平均維持率 70.7%／犯罪・詐欺系 n=10 → 272 views・41.1%。長尺の金融詐欺系は維持率の最下層（Swartz 4.1% / Rajaratnam 3.6% / FTX 2.3%） |
| **R2** | **「ひとりの人間に起きたこと」＞「法理の解説」** | 最良: Rodriguez 42.5% / Hinton 28.1% / 没収一家 24.4% / Cotton 23.1%。最悪: Kelo 1.6% / Mapp 5.3% / Gideon 7.5% ＝**いずれも法理フレームのタイトル** |
| **R3** | **二人称（Your / You）を使う** | 上位パフォーマーに繰り返し出現（"Your Phone…" 25.2%, "Your Front Door…" 18.7%） |

**加えて本チャンネル固有の制約:** 内容はファクト・ドキュメンタリー。
**動画が証明していないことをタイトルで言わない。** 誇張フックは views より先に **維持率を壊す**（Gideon の "Beat the Supreme Court" 7.5% が実例）。

---

## 2. 長尺の「パッケージ改善余地」ランキング

余地 =（維持率が出ている ＝ 中身は合格）×（views が低い ＝ 露出で損している）＋（タイトルが法理フレーム／抽象）

| 順 | EP | video_id | 現行タイトル | views | avp | 症状 |
|---|---|---|---|---|---|---|
| 1 | 027 rodriguez | `tpAKfHKuwqY` | How Long Can the Police Keep You at a Traffic Stop? | 10 | **42.5%** | 中身は全社最強。露出ゼロ |
| 2 | 006 terry | `bYcqabvvxak` | Police Searched Him With No Warrant | **158** | 15.0% | 露出は最大。維持率が落ちている |
| 3 | 014 lange | `Sz8zPUoBANM` | Your Front Door Won't Stop the Police | 43 | 18.7% | **タイトルが判決と逆向き**（後述） |
| 4 | 028 forfeiture | `YhEJHK279f8` | They Took Their House Over $40 — and Never Charged Anyone | 3 | 24.4% | タイトルは良い→**サムネ側の問題** |
| 5 | 029 hinton | `Qyad4FejCIc` | Alabama Tried to Execute an Innocent Man for 30 Years | 14 | 28.1% | 主語が「州」。接点が弱い |
| 6 | 008 carpenter | `zE3nCUlUmLY` | Your Phone Is Tracking You — and the Police Wanted the Map | 17 | 25.2% | 良題。ただし**重複公開で共食い** |
| 7 | 030 cotton | `5L_HCGJxX_U` | She Studied His Face to Be Certain. She Convicted the Wrong Man. | 22 | 23.1% | 文学的すぎ・検索語ゼロ |
| 8 | 009 timbs | `m-uWzgWHGPg` | Police Took His $42,000 Car. The Supreme Court Drew a Line. | 18 | 17.7% | 後半が抽象 |
| 9 | 012 arbitration | `1pox44KsaV8` | The Fine Print That Quietly Took Your Right to Sue | 5 | 13.6% | 二人称◎だが映像が浮かばない |
| 10 | 002 gideon | `ch2hQ5jhDmQ` | He Had No Lawyer — So He Beat the Supreme Court | 5 | 7.5% | **誇張フックが維持率を壊した例** |
| 11 | 003 mapp | `An0to4U0hJQ` | The Police Broke In — So the Court Let Her Go | 2 | 5.3% | 誰の話か不明・軽い |
| 12 | 010 kelo | `89SQoRgAD7U` | Your Home for a Developer? The Kelo Supreme Court Case | 2 | **1.6%** | **法理フレーム最悪例**（判例名） |

**対象外にした長尺（9本）** — Titan(125/22.4%), D.B. Cooper(37/19.9%), Madoff(53/19.5%), Milken(16/21.1%), Gardner(10/24.1%), Varsity Blues(6/17.1%), OneCoin(22/15.9%), Flash Crash(9/15.3%), Swartz(22/4.1%), Rajaratnam(4/3.6%), FTX(3/2.3%), Katz(6/9.3%)。
理由: **R1により、これらはパッケージ改修で救えるカテゴリではない**。犯罪・詐欺の「物語」系は本チャンネルの視聴者層に刺さっていない。タイトルを書き換えても土台の需要が違う。ここに時間を使うより、権利／警察レーンの12本に集中するほうが期待値が高い。
（例外候補: **Titan は長尺で最多の125 views・22.4%** と単体では健闘。改修するなら13番目。ただし他9本と違い「予見された警告を無視した組織」という構造なので、R1の「権力 vs 個人」に寄せた再パッケージは可能。）

---

## 3. TOP 12 個別提案

**サムネ共通仕様（ハウススタイル準拠 / `EP28`・`EP29` thumb_prompts に一致）**
> 1280×720・巨大主題・超高コントラスト・黒/深ネイビー背景・アクセントは **gold `#E5B53A` か electric `#1F6BFF` の1色のみ**・シネマティック・**320pxで判読できること**・実在人物の顔なし・**背景アートに文字を入れない**（見出しは Remotion `<Still>` で載せる）・見出し用ネガティブスペースを残す。
> 見出しは **UPPERCASE ≤4語**。

---

### 1位 ─ EP027 Rodriguez `tpAKfHKuwqY`
**現行:** `How Long Can the Police Keep You at a Traffic Stop?` — **10 views / 維持率 42.5%（チャンネル最高）**

**なぜ負けているか:** 維持率42.5%は「見た人はほぼ最後まで見る」ことを意味する。つまり**中身は完成している。損失は100%パッケージ側**。現行タイトルは疑問形で二人称(You)もあるが、**主語が制度**で「誰に何が起きたか」がゼロ。R2に完全に反する。サムネで指を止める理由がない。

**タイトル候補（≤70字）**
- **A** `The Traffic Stop Was Over. Then the Dog Arrived.` (47)
- **B** `Police Held Him 7 Extra Minutes. The Supreme Court Said No.` (58)
- **C** `Your Traffic Stop Has a Time Limit. One Dog Sniff Set It.` (56)

**サムネ案:** 夜の高速路肩を車の後方から。ブレーキランプの赤は使わず、**electric blue** のパトカー光が路面を斜めに切る。手前にK9のリードだけがシルエットで垂れる（犬の全身は見せない）。上部を大きく空ける。
見出し: `THE STOP WAS OVER`

**⚠️ 精度リスク:** B案の "Said No" は注意。Rodriguez判決が否定したのは「用務完了後の *de minimis* な延長」であり、**合理的疑いがあれば延長は適法**という留保が残っている（本件も差戻し）。断定調が気になるなら B を `Police Held Him 7 Extra Minutes Too Long` に緩める。**推奨は A**（事実そのままで最も強い）。

---

### 2位 ─ EP006 Terry `bYcqabvvxak`
**現行:** `Police Searched Him With No Warrant` — **158 views（長尺最多）/ 維持率 15.0%**

**なぜ負けているか:** 長尺で**最も表示回数を持っている＝絶対値で一番効くレバー**。一方で維持率15%は低く、タイトルが三人称・既視感が強く、**何が争点なのか（逮捕なしで身体検査ができる）が伝わっていない**ため、来た人が冒頭で離脱している。
**決定的な証拠:** 同主題のショート `Police Can Stop & Frisk You Without an Arrest #Shorts` は **188 views / 維持率 50.8%** とチャンネル2位。**同じ主題で、言い回しだけが違い、3倍の維持率**。ショートで実証済みの表現を長尺に移植するのが最も低リスク。

**タイトル候補（≤70字）**
- **A** `Police Can Stop and Frisk You Without Arresting You` (50) ← ショート実証済み表現
- **B** `No Warrant, No Arrest — Why Police Can Still Search You` (54)
- **C** `The Pat-Down Rule: How Police Can Search You on the Street` (57)

**サムネ案:** 夜の街路、壁に両手をつく人物の**背中**（顔なし）を画面いっぱいに。警官の手が上着の外側に触れる瞬間だけを **gold** のハードライトで抜く。左上を空ける。
見出し: `NO WARRANT NEEDED`

**⚠️ 精度リスク:** なし。ただし A は「合理的疑いがある場合」という条件付きなので、**サムネ見出しは断定でも、説明欄の1行目で条件を書く**こと。

---

### 3位 ─ EP014 Lange `Sz8zPUoBANM`
**現行:** `Your Front Door Won't Stop the Police` — **43 views / 維持率 18.7%**

**なぜ負けているか:** 二人称は◎で views も長尺3位。**しかしタイトルが判決内容と逆を約束している。** Lange判決は「軽罪の被疑者を追跡する場合、**自動的には**令状不要にならない」＝むしろ**玄関はある程度police を止める**。視聴者はタイトルの約束（＝玄関は無力）で入り、本編で逆を聞かされる。これが維持率18.7%の説明として最も有力。**精度の欠陥と数字の伸び悩みが同じ原因**なので、修正の一石二鳥性が最も高い。

**タイトル候補（≤70字）**
- **A** `He Drove Home Honking. The Police Followed Him Inside.` (53)
- **B** `Police Chased Him Into His Garage Over a Misdemeanor` (51)
- **C** `When Can Police Follow You Through Your Own Front Door?` (54)

**サムネ案:** **家の内側から見た**ガレージシャッターが半分上がった構図。外側からの光は **electric blue** のみ、内側は深いネイビーの闇。人物は影のみ。
見出し: `HE WENT INSIDE`

**⚠️ 精度リスク:** **現行タイトルが最大のリスク（判決と逆）。最優先で是正。** 新案A/Bは事実記述のみで安全。C は疑問形なので判決の「場合による」を正しく反映する。

---

### 4位 ─ EP028 Forfeiture `YhEJHK279f8`
**現行:** `They Took Their House Over $40 — and Never Charged Anyone` — **3 views / 維持率 24.4%**

**なぜ負けているか:** **タイトルはすでに本ルーブリックに合致している**（権力 vs 個人・具体的な数字・一家の物語）。それで3 views ということは、**問題はタイトルではなくサムネ、または公開初速**。→ この1本は**サムネ差し替えが本命**、タイトルは微調整に留める。

**タイトル候補（微調整・≤70字）**
- **A** `They Took the House Over $40 — No Charges, No Trial` (50)
- **B** `A $40 Sale Cost Them Their Home. Nobody Was Charged.` (51)
- **C** `Police Can Take Your House Without Charging You` (46) ← R3（二人称）適用版

**サムネ案:** 既存 `EP28_forfeiture_thumb_prompts.v001.md` の **T2（分割構図）** に変更。左に暗がりの手の中の$20札2枚（小さく）、右に画面いっぱいの玄関ドア、間に黒いガター。**electric blue** のアクセント1本。
見出し: `$40 → THEIR HOUSE`
**先に確認すること:** 現在サムネにT1（夜の煉瓦の家）が使われているか。T1のままなら T2 へ差し替えてA/B。T1が未適用（デフォルトフレーム）なら、それ自体が3 viewsの原因。

**⚠️ 精度リスク:** C案の "Police Can Take Your House" は民事没収一般としては正しいが、**州法により手続きは大きく異なる**。説明欄で管轄の限定を明示すること。

---

### 5位 ─ EP029 Hinton `Qyad4FejCIc`
**現行:** `Alabama Tried to Execute an Innocent Man for 30 Years` — **14 views / 維持率 28.1%（チャンネル2位）**

**なぜ負けているか:** 維持率は極めて高い＝中身は強い。タイトルも悪くないが**主語が「Alabama（州）」**で、視聴者との接点が遠い。また "30 years" が文中に埋もれて数字のインパクトを失っている。R2的には「彼に何が起きたか」を主語にすべき。

**タイトル候補（≤70字）**
- **A** `Nearly 30 Years on Death Row. The Bullets Never Matched.` (55)
- **B** `The State Had One Piece of Evidence. It Was Wrong.` (49)
- **C** `30 Years on Death Row for a Bullet Match That Wasn't` (51)

**サムネ案:** 既存 `EP29_hinton_thumb_prompts.v001.md` の **T3（弾丸マクロ）**。鋼の面に置かれた1発の弾丸を極端なマクロで、光の亀裂が横切る。**gold** の輝き1点、右側に見出し余白。
見出し: `THE MATCH WAS WRONG`（既存案の `THE BULLETS LIED` は擬人化＋断定が強いので副案）

**⚠️ 精度リスク:** 「捏造した(fabricated)」表現は避け、**「一致しなかった／誤りだった」に留める**。死刑・人種を扱う主題なので、扇情に振りすぎず尊厳を保つこと（既存 thumb_prompts の方針を踏襲）。

---

### 6位 ─ EP008 Carpenter `zE3nCUlUmLY`
**現行:** `Your Phone Is Tracking You — and the Police Wanted the Map` — **17 views / 維持率 25.2%**

**なぜ負けているか:** 二人称◎・維持率◎で、タイトル自体は上位クラス。弱点は**後半 "the map" が抽象**で数字がないこと。
**より大きな問題:** `XWYWAgkExH4` "Police Pulled 127 Days of His Location"（**7 views / 15.7%**）が**同一主題で別途公開されている**。検索・推薦で共食いしており、両方が弱い。
（メタデータ上 `XWYWAgkExH4` は `PD-2026-007-riley/09_package` 配下のファイルに記録されているが、タイトル内容はCarpenter主題。**どちらが何の本編なのか、実物を再生して要確認**。）

**タイトル候補（≤70字）**
- **A** `Police Pulled 127 Days of His Location — Without a Warrant` (57)
- **B** `Your Phone Kept 12,898 Location Points. Police Asked for Them.` (61)
- **C** `Police Can Map Everywhere You've Been. Now They Need a Warrant.` (62)

**サムネ案:** 黒背景に都市の点群マップを巨大に、**electric blue** の光跡が1本だけ都市を貫く。手前下にスマホの輪郭がシルエットで小さく。上部を大きく空ける。
見出し: `127 DAYS. NO WARRANT.`

**⚠️ 精度リスク:** C案は要注意。Carpenter判決は **7日以上の履歴CSLI** に限定した判断で、「警察は今後あらゆる追跡に令状が必要」ではない（リアルタイム位置情報・基地局ダンプ等は明示的に判断を留保）。C を採るなら `Now They Usually Need a Warrant` に緩めるか、**A を推奨**（事実記述のみで安全）。

**併せて実施:** 重複2本のうち弱いほう（`XWYWAgkExH4` / 7 views）を**限定公開に落として1本へ集約**。重複が消えるだけで残ったほうの露出が改善する見込み。

---

### 7位 ─ EP030 Cotton `5L_HCGJxX_U`
**現行:** `She Studied His Face to Be Certain. She Convicted the Wrong Man.` — **22 views / 維持率 23.1%**

> **⚠️ 指示書の誤りを訂正:** 本タスクの前提資料ではこの動画を「Williams（顔認証による誤認逮捕）」としていたが、
> リポジトリ照合の結果 **`5L_HCGJxX_U` = `PD-2026-030-cotton`（目撃証言による誤認／Ronald Cotton事件）** だった。
> EP036 Williams（video_id `gR_nzXIyIlk`）は **7/21公開予定でまだ非公開**のため、この分析データセットには存在しない。
> 「顔認証」という語をタイトルに入れると**内容と食い違う**ので絶対に避けること。

**なぜ負けているか:** 文章として美しいが、**検索語が一つも入っていない**（eyewitness / lineup / misidentification / exoneration いずれもなし）。誰の話かも何の事件かも分からない。R2の「ひとりの物語」は満たしているが、**発見可能性がゼロ**。

**タイトル候補（≤70字）**
- **A** `She Was 100% Certain. She Picked the Wrong Man.` (46)
- **B** `A Decade in Prison Because an Eyewitness Was Certain` (51)
- **C** `The Eyewitness Was Certain — and Completely Wrong` (48)

**サムネ案:** 暗闇に浮かぶ写真ラインナップ（6枠、中身は**すべて顔なしのシルエット**）。1枠だけ **gold** のリングで囲まれる。上部に大きな余白。
見出し: `SHE WAS CERTAIN`

**⚠️ 精度リスク:** B案の服役年数は **本編台本の確定値に合わせること**。不確かなら "A Decade"（概数）表記が安全。数字を出すなら台本の claim と一致させる。

---

### 8位 ─ EP009 Timbs `m-uWzgWHGPg`
**現行:** `Police Took His $42,000 Car. The Supreme Court Drew a Line.` — **18 views / 維持率 17.7%**

**なぜ負けているか:** 前半（$42,000の車を取られた）は強い。後半 "Drew a Line" が抽象で、**何が決まったのか分からない**。金額の非対称（罰金上限より遥かに高い没収）という一番強い事実がタイトルに出ていない。

**タイトル候補（≤70字）**
- **A** `They Seized His $42,000 Car. The Max Fine Was $10,000.` (53)
- **B** `Can the Punishment Cost 4x the Maximum Fine?` (43)
- **C** `His Car Was Worth More Than the Fine — So He Fought Back` (55)

**サムネ案:** 黒背景、車のフロントグリルの一部だけを画面いっぱいに（車種特定できない角度）。**gold** のリムライト1本。下端に押収タグが小さく揺れる。
見出し: `$42,000 FOR THIS`

**⚠️ 精度リスク（重要）:** **Timbs判決が示したのは「過大な罰金条項が州にも適用される」ことだけで、この没収を違憲と結論づけていない（差戻し）。**
→ `The Supreme Court Made Them Give It Back` / `He Got His Car Back` のようなタイトルは**事実と異なるので使用禁止**。上記A/B/Cはいずれも判決の結論に踏み込んでいないので安全。

---

### 9位 ─ EP012 Arbitration `1pox44KsaV8`
**現行:** `The Fine Print That Quietly Took Your Right to Sue` — **5 views / 維持率 13.6%**

**なぜ負けているか:** 二人称◎（R3準拠）だが、"Fine Print" が抽象で**サムネにする絵が浮かばない**＝サムネが弱くなる構造的問題。ショート版（65 views / 39.8%）は中位で、**主題自体は弱くない**。具体（どこに書いてあるのか）を入れる。

**タイトル候補（≤70字）**
- **A** `You Signed Away Your Right to Sue. You Just Didn't Know.` (55)
- **B** `The Clause in Your Phone Contract That Bans Lawsuits` (51)
- **C** `Why You Can't Sue the Company That Wronged You` (45)

**サムネ案:** 黒背景に契約書の一節を巨大に（判読はできるが読み込めない粒度）。**1行だけ gold でハイライト**され、その左にチェック済みのボックス。上部に見出し余白。
見出し: `YOU ALREADY AGREED`

**⚠️ 精度リスク:** 「絶対に訴えられない」は言い過ぎ。実際は**多くの場合「集団訴訟でなく個別仲裁に回される」**。C案は特に断定が強いので、採用するなら説明欄冒頭で「仲裁条項＝訴権の完全消滅ではない」と明記。**推奨は A**。

---

### 10位 ─ EP002 Gideon `ch2hQ5jhDmQ`
**現行:** `He Had No Lawyer — So He Beat the Supreme Court` — **5 views / 維持率 7.5%**

**なぜ負けているか:** **"Beat the Supreme Court" は事実として成立しない。** 彼は最高裁を打ち負かしたのではなく、最高裁が彼の主張を**認めた**。フックのために正確さを犠牲にした典型で、**その代償が維持率7.5%**（法理フレーム3本の一つ）。視聴者が冒頭で「話が違う」と感じている。

**タイトル候補（≤70字）**
- **A** `He Wrote to the Supreme Court in Pencil. He Won.` (47)
- **B** `A Prisoner's Pencil Letter Gave You the Right to a Lawyer` (56)
- **C** `If You Can't Afford a Lawyer — One Man Made That a Right` (55)

**サムネ案:** 罫線入りの便箋に鉛筆書きの手紙（**筆跡は読めない粒度**）。真上から硬いスポットライト、**gold**。紙の縁だけが光る。周囲は黒。右側に見出し余白。
見出し: `WRITTEN IN PENCIL`

**⚠️ 精度リスク:** B案の "Gave You the Right to a Lawyer" は正確（重罪の州裁判における選任弁護人の権利を各州に及ぼした）。ただし**「すべての事件で」ではない**ので、説明欄で重罪／軽罪の範囲に触れること。

---

### 11位 ─ EP003 Mapp `An0to4U0hJQ`
**現行:** `The Police Broke In — So the Court Let Her Go` — **2 views / 維持率 5.3%**

**なぜ負けているか:** "Let Her Go" が軽く、**事件の重さが伝わらない**。誰の話かも不明で二人称もゼロ。R2/R3ともに不適合。また「見逃してもらった」ように読めるため、**違法収集証拠排除という主題が誤って伝わる**。

**タイトル候補（≤70字）**
- **A** `Police Waved a Paper They Called a Warrant. It Wasn't.` (53)
- **B** `They Searched Her Home Illegally — So the Case Collapsed` (55)
- **C** `Why Illegally Seized Evidence Can't Be Used Against You` (54)

**サムネ案:** 内側から見た**蹴破られた玄関ドア**、木片が散る。床に落ちた**1枚の紙**にだけハードなスポット（**gold**）。人物なし。上部に見出し余白。
見出し: `IT WASN'T A WARRANT`

**⚠️ 精度リスク:** A案は「警官が令状と称する紙を提示した」という記録に基づく。**台本の claim と一致していることを確認**してから採用すること。一致が取れないなら B を採る。

---

### 12位 ─ EP010 Kelo `89SQoRgAD7U`
**現行:** `Your Home for a Developer? The Kelo Supreme Court Case` — **2 views / 維持率 1.55%（チャンネル最低）**

**なぜ負けているか:** **法理フレームの最悪例。** 前半は二人称で正しく始まっているのに、**後半 "The Kelo Supreme Court Case" が全部を台無しにしている**。判例名が入った瞬間に「授業」になり、一般視聴者は自分に関係ない話だと判断する。維持率1.55%は「サムネ／タイトルの期待と冒頭が噛み合っていない」ことの最も強い証拠。**判例名はタイトルから完全に外すべき**（これは他の全エピソードにも適用すべき原則）。

**タイトル候補（≤70字）**
- **A** `The City Took Her Pink House. Then Built Nothing.` (48)
- **B** `She Lost Her Home So a Company Could Build. It Never Did.` (56)
- **C** `They Took Her House for a Development That Never Happened` (56)

**サムネ案:** 荒れた更地が画面の大半を占める。その中央に**1軒の家の輪郭だけ**が残像のように浮かぶ（実体はない、空白のシルエット）。**gold** の低い斜光。空が広く空いている。
見出し: `THEY BUILT NOTHING`

**⚠️ 精度リスク（2点）:**
1. **「取り壊された」と書かないこと。** Kelo氏の家は**解体ではなく移築**された。A案の "Took Her Pink House" は所有権の収用を指すので可だが、サムネで瓦礫を描くのは不正確。
2. 「開発は実現しなかった」は事実（跡地は長く未利用のまま）だが、**台本が触れている範囲に収めること**。本編が跡地のその後に言及していないなら、A/B/Cは使えない。その場合は `The Government Took Her Home to Give It to a Developer`（62）に差し替え。

---

## 4. ショートの扱い ─ 続けるべきか

### データ
- ショート22本 = **1,340 views（チャンネル視聴の約68%）**、**登録 0**
- 上位5本はすべて権利／警察系: 199 / 188 / 149 / 145 / 125 views、維持率 69.6% / 50.8% / 46.2% / **92.1%** / (計測異常)
- 犯罪・詐欺系ショートは 3〜56 views で沈没
- コメント **0**

### 判定: **続けるべき。ただし本数を増やすのではなく、レーンを絞る。**

理由は3つ。
1. **ショートは今このチャンネルで唯一「露出が回っている」導線。** CTR 2.31%の長尺と違い、ショートは1本で188 viewsを取れている。この露出を捨てるのは、唯一動いているエンジンを止めるのと同じ。
2. **ショートは長尺の「タイトル実験場」として実証価値がある。** EP006 Terry のショート（188 views / 50.8%）と長尺（158 views / 15.0%）の対比が、**同じ主題でも言い回しで維持率が3倍変わる**ことを実証した。本提案の第2位はこの発見に基づいている。**ショートは無料のA/Bテスト装置**。
3. **一方で、犯罪・詐欺系ショート（n=10 / 平均27 views）は今すぐ止めるべき。** ここは需要がない。**権利／警察レーン専業にする。**

### 登録が0である原因と、変えるべき「たった1つのこと」

**原因の特定:** 上位ショートの維持率は 50〜92%。つまり**視聴者は最後まで見ている**。それでも登録0ということは、離脱地点の問題ではなく、**「最後まで見た人に何も要求していない」**ことが原因。動画が終わって、それで終わっている。

**変えるべき1つ:** **全ショートの末尾3秒を「対応する長尺への誘導」に置き換える。**

具体的には —
- 末尾3秒に固定カードを入れる: 本編のサムネ縮小＋`FULL CASE →` の一行。ナレーションで一言「the full case is on the channel」。
- 併せて**固定コメントに本編URLを1本だけ**置く（コメント0なので、固定コメントが常にトップに出る。コストゼロ）。

**なぜ「登録して」ではなく「本編へ」なのか:** ショート視聴者は登録の意思決定をショート単体では下さない。一方、**長尺を1本見た視聴者は登録する**（実際、+2の登録のうち1件は長尺Madoffから発生している）。ショート→長尺→登録、という順路を作るのが、1,340 viewsという既存資産を最も効率よく換金する方法。**登録を直接求めるのは、順路を1段飛ばしている。**

**測定方法:** 変更後14日で、長尺の「トラフィックソース: Shorts feed / 関連動画」の内訳をStudioで確認。ここが0のままなら仮説が外れている。

**注意:** 公開済みショートの末尾を変えるには再アップロードが必要（＝既存の views/評価がリセットされる）。**既存22本は固定コメントの追加のみに留め、末尾3秒のCTAは新規ショートから適用する**のが安全。

---

## 5. 実行順 ─ 最初に変える3本

**一度に3本だけにする理由:** CTR変化の帰属を保つため。同時に10本変えると、何が効いたのか永久に分からなくなる。また実行前に **`secrets/studio_cookies.txt` を再取得**すること（現在401。変更前のベースラインCTRが取れないと効果測定が成立しない）。

| 実行順 | 動画 | 変更内容 | 選定理由 |
|---|---|---|---|
| **1** | **EP027 Rodriguez** `tpAKfHKuwqY` | タイトル → **A** `The Traffic Stop Was Over. Then the Dog Arrived.`／サムネ差し替え | **非対称性が最大。** 維持率42.5%（チャンネル最高）に対し10 views。中身は完成済みで、損失は純粋にパッケージ側。改修の期待値が全12本で最も高く、かつ**この1本が伸びれば「権利レーン×個人の物語」仮説そのものが検証される** |
| **2** | **EP006 Terry** `bYcqabvvxak` | タイトル → **A** `Police Can Stop and Frisk You Without Arresting You`／サムネ差し替え | **表示回数の土台が最大（158 views・長尺1位）＝ CTRを1pt動かしたときの絶対効果が最も大きい。** しかも新タイトルは推測ではなく、**同主題ショートが188 views / 維持率50.8%で実証済みの表現**。最も低リスクな改善 |
| **3** | **EP014 Lange** `Sz8zPUoBANM` | タイトル → **A** `He Drove Home Honking. The Police Followed Him Inside.`／サムネ差し替え | **唯一「数字の問題」と「正確性の欠陥」が同一原因の案件。** 現行タイトルは判決と逆の約束をしており、維持率18.7%の主因である可能性が高い。数字のためだけでなく、**ファクト・ドキュメンタリーとしての信頼性のために放置できない** |

**次点（第2バッチ・上記の結果を見てから）:** 4位 EP028 Forfeiture（サムネのみ）／5位 EP029 Hinton／6位 EP008 Carpenter（＋重複動画の限定公開化）

**やらないこと:** 犯罪・詐欺系の長尺12本のパッケージ改修。R1により、ここは表現の問題ではなく需要の問題。改修コストを権利／警察レーンに寄せる。

---

## 6. 全体に適用する原則（今後の新規エピソードにも）

1. **タイトルに判例名を入れない**（`The Kelo Supreme Court Case` = 維持率1.55%）
2. **主語は制度でなく人**（`Alabama Tried to…` より `Nearly 30 Years on Death Row…`）
3. **動画が証明していないことを書かない。** 誇張フックは views を買う前に維持率を壊す（Gideon 7.5%が実例）
4. **数字を1つ入れる**（127 days / $42,000 / 7 minutes / $40）— 具体は抽象に勝つ
5. **可能なら二人称**。ただし2と衝突する場合は2を優先
6. **長尺の見出しは、先にショートで試す**（無料のA/Bテスト）

---

## 付記 ─ 本提案で行っていないこと

- YouTube API への書き込み: **なし**
- タイトル／説明文の更新: **なし**
- サムネイルのアップロード: **なし**
- 動画の公開設定変更: **なし**

すべてオーナー承認後に実施。実施時は **1バッチ3本まで**、変更前に Studio のベースライン（表示回数・CTR）を必ずスナップショット保存すること。
