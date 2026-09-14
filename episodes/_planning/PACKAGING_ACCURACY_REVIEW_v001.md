# PACKAGING_ACCURACY_REVIEW v001 — タイトル案の法的・事実的正確性の検証

**作成:** 2026-07-19
**対象:** `PACKAGING_FIX_v001.md` §3「TOP 12 個別提案」の全タイトル（現行12本＋新案36案 = 48件）
**方法:** 各判例の一次資料（判決全文 / Cornell LII / supremecourt.gov / FindLaw全文）＋ 事件当事者系は Innocence Project・DPIC・IJ・裁判記録。Wikipediaは出発点のみで出典不採用。
**性質:** 検証レポート。**YouTube側への書き込みは一切していない**（Data API は read-only 呼び出しのみ）。

---

## ⚠️ 最重要 — 検証中に判明した2つの想定外

### (1) 実行順1〜3は「すでにYouTube上で適用済み」

`PACKAGING_FIX_v001.md` は「YouTube側は一切変更していない」と記載しているが、**Data APIで実測した現在のライブタイトルは、すでに候補Aに差し替わっていた。**

| video_id | 提案書が言う「現行」 | **実際のライブタイトル（2026-07-19実測）** |
|---|---|---|
| `tpAKfHKuwqY` | How Long Can the Police Keep You at a Traffic Stop? | **The Traffic Stop Was Over. Then the Dog Arrived.**（＝候補A） |
| `bYcqabvvxak` | Police Searched Him With No Warrant | **Police Can Stop and Frisk You Without Arresting You**（＝候補A） |
| `Sz8zPUoBANM` | Your Front Door Won't Stop the Police | **He Drove Home Honking. The Police Followed Him Inside.**（＝候補A） |

→ **朗報: 最大の欠陥だった Lange の REVERSED タイトルは、すでにライブ上では是正済み**。
→ **問題: 提案書の「現行タイトル」列と views/avp 実測が、実際の状態とずれている。**効果測定のベースラインとして使えない。以降の判定では「提案書の現行」「ライブの現行」を区別して記載する。

### (2) `XWYWAgkExH4` は Carpenter の重複ではない。**Riley本編に Carpenter のタイトルが載っている**

詳細は §3。**重複ではなく、タイトルと中身の不一致**。提案書の「共食いしているので弱いほうを限定公開に落とす」という処方は**誤り**であり、実行すると健全なRiley回を消すことになる。

---

## 1. 判定表 — REVERSED / OVERSTATED を上に

### 🔴 REVERSED（判旨・事実と逆。最優先で是正）

| # | EP | 対象 | タイトル | 判定理由 | ライブ状態 |
|---|---|---|---|---|---|
| R1 | 014 Lange | 提案書の現行 | `Your Front Door Won't Stop the Police` | Lange判決は「軽罪被疑者の追跡は**自動的には**無令状侵入を正当化しない」＝**玄関はむしろ止める側**。判決文: "pursuit of a fleeing misdemeanor suspect does not always—that is, categorically—justify a warrantless entry"。しかも**9-0の全員一致でLange勝訴（破棄差戻）** | ✅ **是正済み**（候補Aに差替済） |
| R2 | 002 Gideon | **ライブの現行** | `He Had No Lawyer — So He Beat the Supreme Court` | **最高裁はGideonに味方している（9-0で彼の主張を採用、Betts判例を破棄）。** 彼が破ったのはフロリダ州。さらに最高裁では Abe Fortas が代理人に選任されており「弁護士がいなかった」も当てはまらない。前半と後半が自己矛盾 | 🔴 **未是正・公開中** |
| R3 | 028 Forfeiture | **ライブの現行** | `They Took Their House Over $40 — and Never Charged Anyone` | **二重に事実と逆。** ①家は取られていない — 約1週間の締め出し後に一家は帰宅し、2015/6の部分和解で**没収は取下げ＝一家は家を守った**。②誰も起訴されていない、も誤り — 息子 Yianni Sourovelis は逮捕・訴追され、no contest答弁でリハビリ処分。**リポジトリ内の `EP28_forfeiture_fact_recheck.v001.md` 自身が「一家は家を守った」「息子は逮捕」と明記しており、タイトルが自社の検証済みファクトと矛盾している** | 🔴 **未是正・公開中** |
| R4 | 028 Forfeiture | 新案A | `They Took the House Over $40 — No Charges, No Trial` | R3と同じ2つの誤りを継承。加えて "No Trial" も誤り（没収手続は現に係属し、息子の刑事事件は答弁で決着） | — |
| R5 | 028 Forfeiture | 新案B | `A $40 Sale Cost Them Their Home. Nobody Was Charged.` | 「家を失った」も「誰も起訴されず」も事実と逆 | — |
| R6 | 010 Kelo | 新案B | `She Lost Her Home So a Company Could Build. It Never Did.` | **Pfizerは建てている。** 約$300Mの研究拠点は**2005年の判決より前の2001年に、収用対象外の隣接地で開業済み**。建たなかったのはホテル／住宅／オフィス複合のほう。主語を取り違えている | — |
| R7 | 007 Riley | **ライブの現行**（`XWYWAgkExH4`） | `Police Pulled 127 Days of His Location` | **中身は Riley v. California（逮捕に伴う携帯電話の捜索）。127日のCSLIは Carpenter の事実であり、この動画では扱っていない。** 説明文・チャプター（"Can police open your phone?" / "David Riley's arrest" / "Get a warrant"）はすべてRiley。タイトルだけが別エピソードの事実 | 🔴 **未是正・公開中** |

### 🟡 OVERSTATED（方向は合うが留保・条件を落としている）

| # | EP | 対象 | タイトル | 落としている留保 |
|---|---|---|---|---|
| O1 | 012 Arbitration | **ライブの現行** | `The Fine Print That Quietly Took Your Right to Sue` | 仲裁条項は提訴権を**消滅させない。個別仲裁に振り替える**だけ。失うのは**集団訴訟と陪審／法廷という場**。*Concepcion* で最高裁が支持した AT&T の条項は**少額裁判所での提訴を明示的に留保**しており、$7,500の最低回収額と弁護士費用倍額まで定めていた。「訴権を奪った」は判例の土台と逆 |
| O2 | 012 Arbitration | 新案A | `You Signed Away Your Right to Sue. You Just Didn't Know.` | O1と同じ |
| O3 | 012 Arbitration | 新案B | `The Clause in Your Phone Contract That Bans Lawsuits` | 同上。*Concepcion* の当の携帯契約が少額訴訟を許容していた |
| O4 | 012 Arbitration | 新案C | `Why You Can't Sue the Company That Wronged You` | 4案中最も強い断定。REVERSED寸前。訴えられる — **ただし単独でのみ** |
| O5 | 008 Carpenter | 新案C | `Police Can Map Everywhere You've Been. Now They Need a Warrant.` | Carpenterは**7日分の履歴CSLIへのアクセスが捜索にあたる**と述べたのみ。**リアルタイムCSLI・基地局ダンプ・従来型監視（防犯カメラ）・外交/安全保障目的の収集は明示的に判断せず**、緊急状況の例外も温存。「あらゆる追跡に令状」は判旨より大幅に広い |
| O6 | 008 Carpenter | 新案B | `Your Phone Kept 12,898 Location Points. Police Asked for Them.` | **12,898点は携帯電話が保持していたのではなく、通信事業者（MetroPCS/Sprint）の業務記録。**この区別こそが第三者法理の争点そのもの。また "Asked for" は SCA §2703(d) の**裁判所命令による強制取得**を「お願い」に薄めている |
| O7 | 027 Rodriguez | 新案B | `Police Held Him 7 Extra Minutes. The Supreme Court Said No.` | 7〜8分は判決文どおりで正確。ただし "Said No" はRodriguezの勝訴を含意する。実際は**破棄差戻しにとどまり、合理的疑いの有無は未判断**。差戻審（8th Cir. 799 F.3d 1222）は good-faith 例外で証拠排除を認めず、**Rodriguez本人は敗訴** |
| O8 | 027 Rodriguez | 新案C | `Your Traffic Stop Has a Time Limit. One Dog Sniff Set It.` | 論理が反転。上限を画するのは**停止の任務（mission）**であって、犬の臭気検査はそれを**超過した側**。「Sniffが上限を設定した」は因果が逆 |
| O9 | 003 Mapp | **ライブの現行** | `The Police Broke In — So the Court Let Her Go` | 最高裁は**証拠法上の理由で有罪判決を破棄・差戻した**のであって「解放した」のではない。無罪認定でもない（オハイオ州が再訴しなかっただけ）。「見逃してもらった」と読める点は提案書の指摘どおり |
| O10 | 003 Mapp | 新案A | `Police Waved a Paper They Called a Warrant. It Wasn't.` | 記録が立証しているのは「**公判で令状が提出されず、不提出の説明もなかった**」こと。「令状ではなかった」という積極的認定まではしていない（オハイオ州最高裁も存在に「相当の疑い」と述べるにとどまる） |
| O11 | 029 Hinton | 新案B | `The State Had One Piece of Evidence. It Was Wrong.` | 二重に強い。①別件強盗の被害者による写真面割りもあり「唯一の証拠」は殺人2件についてのみ成立。②弾道鑑定は「誤りと証明された」のではなく**「同一銃と結論づけられない＝立証不能」**（Alabama州法研自身の2015年再鑑定でも一致せず） |
| O12 | 029 Hinton | 新案C | `30 Years on Death Row for a Bullet Match That Wasn't` | 死刑囚房での期間は**約28年**（1986年宣告〜2015年釈放）。逮捕からでも約29年9か月。"30 years on death row" は約2年の過大 |
| O13 | 028 Forfeiture | 新案C | `Police Can Take Your House Without Charging You` | 機序としては正しい（対物訴訟＝有罪判決不要）が、①**没収を申し立てるのは警察でなく検察**、②2026年時点で**約15〜16州が有罪判決要件を導入**、Maine/Montana/New Mexico は民事没収を廃止。PA州2017年Act 13は立証責任を政府に移したが**有罪判決要件は課していない**ので、本件の管轄では依然妥当 |

### 🟢 ACCURATE

| EP | 対象 | タイトル | 備考 |
|---|---|---|---|
| 027 Rodriguez | 提案書の現行 | `How Long Can the Police Keep You at a Traffic Stop?` | 任務時間の判旨に合致。疑問形が差戻しの未確定性を正しく回避 |
| 027 Rodriguez | 新案A（ライブ適用済） | `The Traffic Stop Was Over. Then the Dog Arrived.` | 書面警告の交付後に臭気検査、という判決文どおりの時系列。**推奨** |
| 006 Terry | 提案書の現行 | `Police Searched Him With No Warrant` | 事実として正確（判決自身が frisk を "nothing less than a search" と呼ぶ） |
| 006 Terry | 新案A（ライブ適用済） | `Police Can Stop and Frisk You Without Arresting You` | 判旨の簡潔な言い換え。**推奨** |
| 006 Terry | 新案B | `No Warrant, No Arrest — Why Police Can Still Search You` | 可。ただし裸の "search you" はポケット・カバンまで含むと誤読されうる |
| 006 Terry | 新案C | `The Pat-Down Rule: How Police Can Search You on the Street` | "Pat-down" が外衣への限定を正しく示す。3案中もっとも精密 |
| 014 Lange | 新案A（ライブ適用済） | `He Drove Home Honking. The Police Followed Him Inside.` | 判決文の事実摘示どおり。**推奨** |
| 014 Lange | 新案B | `Police Chased Him Into His Garage Over a Misdemeanor` | 可。厳密には追跡の端緒は騒音の**違反（infraction）**で、軽罪DUIは侵入後に判明 |
| 014 Lange | 新案C | `When Can Police Follow You Through Your Own Front Door?` | 「事案ごとの判断」という判旨を疑問形が正確に反映 |
| 029 Hinton | ライブの現行 | `Alabama Tried to Execute an Innocent Man for 30 Years` | 概数として可（実際は逮捕から約29年9か月）。無罪放免・起訴取下げ済み |
| 029 Hinton | 新案A | `Nearly 30 Years on Death Row. The Bullets Never Matched.` | "Nearly 30" が正確、"never matched" は3名の専門家＋州法研の結論と一致。**3案中最良** |
| 030 Cotton | ライブの現行 | `She Studied His Face to Be Certain. She Convicted the Wrong Man.` | 両節とも裏付けあり（Thompson本人が同じ枠組みで語っている） |
| 030 Cotton | 新案A | `She Was 100% Certain. She Picked the Wrong Man.` | 「100%確信していた」は本人の発言として確認済み |
| 030 Cotton | 新案B | `A Decade in Prison Because an Eyewitness Was Certain` | **服役10年6か月（1984/7逮捕〜1995/6/30釈放）＝"A Decade" は正確。**提案書が懸念した数字リスクはクリア |
| 030 Cotton | 新案C | `The Eyewitness Was Certain — and Completely Wrong` | 可 |
| 009 Timbs | ライブの現行 | `Police Took His $42,000 Car. The Supreme Court Drew a Line.` | $42,000は判決文の数字。"Drew a Line" は編入判断にとどめており、**没収を違憲と断じていないので安全** |
| 009 Timbs | 新案A | `They Seized His $42,000 Car. The Max Fine Was $10,000.` | 両数字とも判決文の同一文からの逐語。**3案中最良** |
| 009 Timbs | 新案B | `Can the Punishment Cost 4x the Maximum Fine?` | 判決文の "more than four times" に一致。疑問形が「均衡性は未判断」という状態を正しく表す |
| 009 Timbs | 新案C | `His Car Was Worth More Than the Fine — So He Fought Back` | 正確だが4倍差を「より高い」に薄めており最も弱い |
| 008 Carpenter | ライブの現行 | `Your Phone Is Tracking You — and the Police Wanted the Map` | 可 |
| 008 Carpenter | 新案A | `Police Pulled 127 Days of His Location — Without a Warrant` | 127日は逐語、無令状（§2703(d)命令）も正確。**ただし §3 の衝突問題あり — 単純採用不可** |
| 010 Kelo | ライブの現行 | `Your Home for a Developer? The Kelo Supreme Court Case` | 事実としては正確（維持率の問題は精度でなくパッケージ） |
| 010 Kelo | 新案A | `The City Took Her Pink House. Then Built Nothing.` | ピンクの家✓／収用は現に実行され Kelo は5-4で敗訴✓／彼女の区画は2025年6月時点でも空地✓ |
| 010 Kelo | 新案C | `They Took Her House for a Development That Never Happened` | 収用地について正確、かつ家屋の物理的な行方に何も主張しないため最も安全 |
| 002 Gideon | 新案A | `He Wrote to the Supreme Court in Pencil. He Won.` | 鉛筆・獄中便箋・勝訴すべて確認済（国立公文書館） |
| 002 Gideon | 新案B | `A Prisoner's Pencil Letter Gave You the Right to a Lawyer` | 正確。留保は下記 |
| 002 Gideon | 新案C | `If You Can't Afford a Lawyer — One Man Made That a Right` | 正確。ただし *Miranda*(1966) の警告文と混同されうる |
| 003 Mapp | 新案B | `They Searched Her Home Illegally — So the Case Collapsed` | 違法捜索✓／有罪判決破棄・再訴なし✓ |
| 003 Mapp | 新案C | `Why Illegally Seized Evidence Can't Be Used Against You` | Mappの判旨として正確 |

**UNVERIFIABLE: 該当なし。**48件すべてについて一次資料で判定可能だった。

---

## 2. REVERSED / OVERSTATED への代替案（弱めずに事実へ寄せる）

> 原則: 削るのではなく、**本当に起きたことのほうが元のフックより強い**ことを利用して差し替える。

### R2 Gideon（最優先・未是正）
| | |
|---|---|
| 現行 | `He Had No Lawyer — So He Beat the Supreme Court` |
| **推奨** | **`He Had No Lawyer. So He Wrote the Supreme Court in Pencil.`** (57) |
| 代替 | `A Pencil, Prison Paper, and a 9-0 Supreme Court Win` (50) |
| 代替 | `He Wrote to the Supreme Court in Pencil. He Won.` (47) ＝新案Aそのまま |

「最高裁を打ち負かした」より「**鉛筆で最高裁に手紙を書いた**」のほうが具体的で画になり、しかも事実。9-0という数字も使える。

### R3/R4/R5 Forfeiture（最優先・未是正）
真実は「家を取られた」より強い。**息子は起訴された。両親は何もしていないのに家を狙われた。**この非対称こそがフック。

| | |
|---|---|
| 現行 | `They Took Their House Over $40 — and Never Charged Anyone` |
| **推奨** | **`Their Son Was Charged. The City Came for His Parents' House.`** (60) |
| 代替 | `They Were Locked Out of Their Own Home. They Were Never Charged.` (64) |
| 代替 | `$40 of Heroin — and the DA Moved to Take the Whole House` (56) |
| 新案C差替 | `Prosecutors Can Take Your House Without Charging You` (51) |

※ 「取り返した／守り抜いた」という結末は**維持率にむしろ有利**（後半に解決がある）。現行タイトルは結末をネタバレしないどころか、逆の結末を約束してしまっている。

### R6 Kelo 新案B
| | |
|---|---|
| 現行案 | `She Lost Her Home So a Company Could Build. It Never Did.` |
| **推奨** | **`She Lost Her Home for a Hotel. It Was Never Built.`** (49) |
| 代替 | `She Lost Her Home for Pfizer. Pfizer Left. Nothing Was Built.` (61) |

⚠️ **賞味期限あり:** 跡地は2023年1月にRJ Developmentへ売却、2024年9月に New London市が500戸の集合住宅に$6.5Mの税優遇を承認、コミュニティセンターは着工済み。Kelo氏の区画自体は空地のままだが、「何も建たなかった」は数年で使えなくなる。`20 Years Later, It's Still an Empty Lot` のように**彼女の区画に限定する**言い回しが長持ちする。
⚠️ サムネで**瓦礫を描かない**（提案書の指摘は正しい。家屋は2008年に Avner Gregory が 36 Franklin Street へ移築、現存）。

### O1〜O4 Arbitration（4案すべて要差替）
真の争点は「訴えられない」ではなく「**一人でしか訴えられない**」。こちらのほうが挑発的で、かつ正確。

| | |
|---|---|
| 現行 | `The Fine Print That Quietly Took Your Right to Sue` |
| **推奨** | **`The Fine Print That Quietly Took Your Right to a Jury`** (52) |
| 代替 | `The Fine Print That Killed Your Lawsuit Before You Signed It` (59) |
| A差替 | `You Signed Away Your Day in Court. You Just Didn't Know.` (55) |
| B差替 | `The Clause in Your Phone Contract That Bans Class Actions` (56) |
| C差替 | **`You Can Still Sue Them. Just Never With Anyone Else.`** (52) |

※ C差替案は、近年の**マス仲裁**（2024年に28万件超の個別申立て／AAAの企業側申立手数料$8,125）という逆転オチへの導線にもなる。企業が要求した「個別仲裁」に企業自身が溺れている構図は、第3幕として強い。
※ 2022年 EFAA（性的暴行・ハラスメント紛争は請求者の選択で仲裁条項を無効化）にも触れれば「絶対ではない」の裏づけになる。

### O5/O6 Carpenter
| | |
|---|---|
| B案 | `Your Phone Kept 12,898 Location Points. Police Asked for Them.` |
| **B差替** | **`His Phone Company Logged 12,898 Location Points. Police Took Them.`** (66) |
| C案 | `Police Can Map Everywhere You've Been. Now They Need a Warrant.` |
| **C差替** | **`Police Mapped 127 Days of His Life. Now That Needs a Warrant.`** (61) |
| 代替 | `They Tracked Him for 127 Days. The Court Said: Get a Warrant.` (58) |

### O7/O8 Rodriguez
| | |
|---|---|
| B案 | `Police Held Him 7 Extra Minutes. The Supreme Court Said No.` |
| **B差替** | **`A Dog Sniff Can't Add 7 Minutes to Your Traffic Stop`** (52) |
| C案 | `Your Traffic Stop Has a Time Limit. One Dog Sniff Set It.` |
| **C差替** | **`Your Traffic Stop Ends When the Ticket Does. Not a Minute Later.`** (63) |

※ ライブは既に候補A。差替の必要はないが、B/Cを将来使う場合の版として残す。

### O9/O10 Mapp
| | |
|---|---|
| 現行 | `The Police Broke In — So the Court Let Her Go` |
| **推奨** | **`The Police Broke In With No Warrant — So the Conviction Fell`** (59) |
| 代替 | `They Waved a Paper and Called It a Warrant. It Never Appeared.` (61) |
| A差替 | `Police Waved a Paper They Called a Warrant. No One Ever Saw It Again.` (67) |

### O11/O12 Hinton
| | |
|---|---|
| B案 | `The State Had One Piece of Evidence. It Was Wrong.` |
| **B差替** | **`The Only Evidence Tying Him to the Murders Couldn't Be Matched`** (61) |
| C案 | `30 Years on Death Row for a Bullet Match That Wasn't` |
| **C差替** | **`Nearly 30 Years on Death Row for a Bullet Match That Wasn't`** (58) |
| 現行の微調整（任意） | `Alabama Spent Nearly 30 Years Trying to Execute an Innocent Man` (63) |

### O13 Forfeiture 新案C
`Prosecutors Can Take Your House Without Charging You` (51) — 主体を検察に修正。説明欄で州ごとの差（15〜16州が有罪判決要件、Maine/Montana/New Mexicoは廃止、PAは2017年改革後も有罪判決要件なし）に触れること。

---

## 3. `zE3nCUlUmLY` と `XWYWAgkExH4` — 重複ではない。**タイトル取り違え**

### 実測（YouTube Data API / read-only / 2026-07-19）

| | `zE3nCUlUmLY` | `XWYWAgkExH4` |
|---|---|---|
| ライブタイトル | Your Phone Is Tracking You — and the Police Wanted the Map | **Police Pulled 127 Days of His Location** |
| 公開 | 2026-06-23 03:00 UTC | 2026-06-22 03:00 UTC |
| 尺 | 11:19 | 10:47 |
| views | 18 | 7 |
| リポジトリ上のEP | `PD-2026-008-carpenter` | **`PD-2026-007-riley`** |
| 説明文の主題 | **Carpenter v. United States**（127日のCSLI、第三者法理、2018年判決） | **Riley v. California**（逮捕に伴う携帯捜索、2014年判決） |
| チャプター | 127 days, no warrant／Detroit, 2010-2011／12,898 location points／The third-party doctrine／Terry, Riley, Carpenter | Can police open your phone?／**David Riley's arrest**／The old pocket-search rule／Get a warrant／**Next: location records** |

### 結論

**重複ではない。シリーズとして正しく設計された連続2本である。**
`XWYWAgkExH4`(Riley, 6/22) の説明文は末尾で "Next episode: the location trail your phone leaves behind." と次回予告し、翌日 6/23 に `zE3nCUlUmLY`(Carpenter) が公開されている。**意図的な2部構成であり、共食いではない。**

**実際の問題は、Riley回のタイトルだけが Carpenter の事実になっていること。**
- `XWYWAgkExH4` のライブタイトル `Police Pulled 127 Days of His Location` の「127日の位置情報」は **Carpenter事件の事実であって、Riley事件には登場しない**（Rileyは逮捕時のスマホ内容の捜索）。
- リポジトリ側の意図されたタイトルは `episodes/PD-2026-007-riley/09_package/youtube_meta.v006.json` に **`The Supreme Court Case That Put a Warrant on Your Phone`** と記録されている。どこかの工程で別エピソードのタイトルが載った。
- これは**維持率15.7%の有力な説明**でもある。127日の位置情報を期待して入った視聴者が、逮捕時の携帯捜索の話を聞かされている。Lange と同型の「タイトルの約束と中身の不一致」。

### 処方（提案書の処方を否定する）

❌ **提案書の「弱いほう `XWYWAgkExH4` を限定公開に落として1本へ集約」は実行してはならない。** 健全な独立エピソード（Riley回）を消すことになり、しかも Carpenter回への導線（次回予告）も失う。

✅ **正しい対応は、`XWYWAgkExH4` のタイトルを Riley の内容に戻すこと。**
- 推奨: `Police Took His Phone. Then They Opened It.` (44)
- 代替: `Can Police Open Your Phone After Arresting You?` (47)
- リポジトリ記録どおりに戻すなら: `The Supreme Court Case That Put a Warrant on Your Phone` (55)

✅ **併せて、Carpenter回 `zE3nCUlUmLY` の新案A `Police Pulled 127 Days of His Location — Without a Warrant` は、この取り違えを固定化するので採用順位を下げる。**Riley回のタイトルを直すまでは、Carpenter側は C差替案 `Police Mapped 127 Days of His Life. Now That Needs a Warrant.` (61) を推す。両方に127日を持たせると、今度こそ本当の共食いが起きる。

**どちらを残すか＝両方残す。**主題が異なり、シリーズとして連結されている。

---

## 4. 実行順の修正提案

提案書 §5 の3本はすでに適用済みなので、次バッチは**精度欠陥の残り3件を最優先**にすべき。views最適化より先に、事実の誤りを消す。

| 順 | 動画 | 変更 | 理由 |
|---|---|---|---|
| **1** | EP007 Riley `XWYWAgkExH4` | タイトル → `Police Took His Phone. Then They Opened It.` | **タイトルと中身が別事件。**視聴者への裏切りが最も直接的で、維持率15.7%の説明にもなる |
| **2** | EP028 Forfeiture `YhEJHK279f8` | タイトル → `Their Son Was Charged. The City Came for His Parents' House.` | **自社の検証済みファクト文書と正面から矛盾。**ファクト・ドキュメンタリーとして放置不可。views 3 なので機会損失も最小のうちに直せる |
| **3** | EP002 Gideon `ch2hQ5jhDmQ` | タイトル → `He Had No Lawyer. So He Wrote the Supreme Court in Pencil.` | 判旨と逆＋自己矛盾。維持率7.5%の主因である可能性が高い |

その後に views最適化（Hinton / Cotton / Timbs / Kelo / Mapp / Arbitration）。
**Arbitration は4案すべてが OVERSTATED なので、差替案を採らない限り着手しない。**

---

## 5. 台本側への申し送り（タイトルではなく本編の注意点）

一次資料の確認過程で、本編・説明欄が踏んではならない地雷が出た。

- **Timbs:** 2019年の最高裁は**編入を判断しただけで、この没収を違憲としていない**。車が実際に戻ったのは**2020年5月末**（州の下級審経由）、州最高裁の確定は**2021年6月**。なお$42,000は**購入価格**（SCOTUS）で、インディアナ州最高裁は押収時価値**$35,000／上限罰金の3.5倍**を使っている。**2つの数字を混ぜないこと。**
- **Carpenter:** footnote 3 は「**7日という基準を作らなかった**」ことを明示している（"we need not decide whether there is a limited period..."）。「7日ルール」と言うのは誤り。7日は本件事実における下限。
- **Rodriguez:** 差戻審で Rodriguez 本人は good-faith 例外により**敗訴**。「彼は勝った」と言わないこと。
- **Lange:** 判決は**9-0（Robertsは結論同意の別意見、Alitoが加わる／反対意見なし）**。6-3やRoberts反対と書かないこと。ガレージのシャッター下に足を入れた描写は記録・報道由来で、**最高裁意見書には無い**ので「最高裁が認定した」とは書かない。
- **Hinton:** **証拠は捏造ではない**。「同一と結論づけられない」立証不能。また最高裁（Hinton v. Alabama, 2014, per curiam）が判断したのは**弁護人の無効な援助**（$1,000の鑑定費用上限という誤解に基づく）だけで、**無罪を宣言していない**。
- **Mapp:** 警察が探していたのは**爆破事件の被疑者と賭博関係の物**で、わいせつ物ではない。最高裁が彼女を**無罪としたわけではない**。
- **Gideon:** 当時の射程は**重罪**。軽罪（拘禁刑を伴うもの）への拡張は **Argersinger v. Hamlin (1972)**。また最高裁では Abe Fortas が代理人だった。
- **Cotton:** 面通しでの identification は**即断ではない**。「4番と5番のあいだ」と述べてから5番（Cotton）を選び、**その後の確認フィードバックで確信が固まった**。これが本件の科学的な核心であり、「最初から確信していた」と描くのは誤り。1987年の再審では**2件のレイプ**で有罪となっており、両方とも真犯人 Bobby Poole の犯行。
- **Forfeiture:** 息子への言及は「約$40のヘロイン売却で逮捕、のちリハビリ」まで（既存 guardrails どおり）。**両親が家を守った**という結末を落とさないこと。

---

## 付記 — 本レビューで行っていないこと

- YouTube API への書き込み: **なし**（`videos.list` の読み取りのみ）
- タイトル／説明文の更新: **なし**
- サムネイルのアップロード: **なし**
- 公開設定の変更: **なし**
- `PACKAGING_FIX_v001.md` の編集: **なし**（本ファイルは別文書として追加）
