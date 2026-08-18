# EP38 — Kids for Cash — Claim Ledger / 裏取り台帳 v001

> 目的: 台本 v003 の各 `[L]` を出典に紐づけて確定（invariant #1: 未裏取りの事実は承認台本に入れない）。
> ステータス: `LOCKED`=出典一致で確定 / `VARIANCE`=出典間で差あり・台本の採用値を明記 / `REVIEW`=公開前に法務/オーナー確認。
> 主要出典: Wikipedia "Kids for cash scandal" / Juvenile Law Center (jlc.org) / NPR / Philadelphia Inquirer / CNN(2009) / NBC News / Democracy Now / Hillary Transue 上院証言(2022 PDF)。

| ID | 主張（台本の値） | 判定 | 出典・メモ |
|---|---|---|---|
| CLM-01 | 事件地=ペンシルベニア州ルザーン郡・Wilkes-Barre の Court of Common Pleas | LOCKED | Wikipedia / CNN 2009 |
| CLM-02 | 判事2名: Mark Ciavarella（少年裁判所）／Michael Conahan（管理判事＝president judge） | LOCKED | Wikipedia / Inquirer |
| CLM-03 | 期間: 2003–2008 に子供を営利施設へ送致 | LOCKED | Wikipedia |
| CLM-04 | 営利拘置施設: PA Child Care ／ Western PA Child Care | LOCKED | Wikipedia / JLC |
| CLM-05 | 建設=Robert Mericle（開発業者）／運営・共同オーナー=Robert Powell（弁護士・実業家） | LOCKED | CNN 2009 / Wikipedia |
| CLM-06 | 判事らが受領した総額 ≈ **$2.8M**（3年） | VARIANCE | Wikipedia/CNN=「$2.8M(3年)」。一部報道=「$2.6M」。**台本採用=$2.8M**。※Ciavarella個人へのMericle分は別途「$1M」と報じる社もあり（NBC）。数字カードは$2.8Mで統一 |
| CLM-07 | Conahan が郡営少年拘置所を財源縮小し閉鎖へ／営利施設へ誘導（placement guarantee 系合意） | LOCKED（詳細語はREVIEW） | Wikipedia。"placement guarantee agreement" の語は台帳で最終文言確認 |
| CLM-08 | Ciavarella の前で**弁護士を放棄した子の約50%が施設送り**（州平均 **8.4%**） | LOCKED | JLC / 複数報道（"about 50% vs 8.4% statewide"） |
| CLM-09 | Ciavarella の弁護士放棄率は他管轄の **7〜11倍** | LOCKED | JLC / 報道 |
| CLM-10 | Hillary Transue: 偽MySpaceページで副校長を揶揄→**3か月**判決（審理時**17歳**・2007年4月／実際は約1か月で釈放） | VARIANCE（年齢） | Transue上院証言(2022)/報道。年齢は15/17で揺れ→**17でロック**。台本v003を15→17に修正済 |
| CLM-11 | Edward Kenzakoski: 薬物付属品所持・**17歳**・ブートキャンプ30日判決だが PA Child Care 系施設に数か月→**23歳で自死** | LOCKED | Today.com / Democracy Now / 報道。**自死は方法描写なし（センシティブ）** |
| CLM-12 | 母 Sandy Fonzo が法廷（連邦裁）前で Ciavarella を面罵 | LOCKED | 報道多数（confrontation on courthouse steps） |
| CLM-13 | Juvenile Law Center（フィラデルフィア）が2008–09に調査・州最高裁へ申立 | LOCKED | JLC |
| CLM-14 | ペンシルベニア州最高裁が Ciavarella 法廷の審判を大量取消・記録抹消 | VARIANCE（件数） | NPR=「有罪 **2,251件** を無効」／JLC=「最大 **約6,500件**」／報道=「**約4,000件**」。**台本表現=「数千件／最大数千人」で安全側**。数字カードは "THOUSANDS VACATED"（具体数を焼かない） |
| CLM-15 | Conahan: 恐喝共謀で有罪答弁→**17.5年**／Ciavarella: 公判で有罪（**39件中12件**・RICO等）→**28年** | LOCKED | Wikipedia / NBC News（28年）/ NPR |
| CLM-16 | 民事で判事らに **$2億超**の賠償命令（2022） | LOCKED | NPR 2022（"more than $200 million"） |
| CLM-17 | 2024年、**Conahan の刑をバイデンが減刑**（早期釈放） | LOCKED | Times Observer 2024 / The Daily Beast |
| CLM-18 | 事件後、ペンシルベニアは少年審理での弁護士確保など改革 | LOCKED（詳細REVIEW） | NPR "After Scandal, New Rules"。具体条文は台本では一般表現に留める |
| CLM-19 | Conahan が営利施設への収容を保証する合意（placement guarantee agreement）に署名 | REVIEW | Wikipedia/報道で「placement guarantee agreement」の存在は既知。**正確な文言・当事者を台帳で最終確認**してから断定 |
| CLM-20 | 送金は側口座・仲介を経て隠され、"finder's fee" として偽装 | LOCKED | Wikipedia/FindLaw（Mericle→Powell経由の referral fee 構造） |
| CLM-21 | 連邦（FBI）が並行して捜査。台本は「wiretap」を断定せず「連邦捜査」に留める | LOCKED（一般表現） | 連邦訴追は事実。盗聴の具体は断定回避 |
| CLM-22 | 事件を広く知らしめたドキュメンタリー「Kids for Cash」（2014, dir. Robert May） | LOCKED | 公開作品。実在。年・監督を台帳で確認済 |
| CLM-23 | 2003–2008 の期間に営利施設へ送られた子供は累計「数千人」 | LOCKED（安全表現） | 抹消対象 最大 約4,000–6,500（CLM-14）と整合。台本は「thousands」表現 |

## 公開前 REVIEW（R2）
- 未成年の私人（Transue/Kenzakoski 他）: 実名は公的報道・本人の公開証言に基づく範囲に限定。**顔・肖像は出さない**（画像は匿名シルエット）。
- **自死（Kenzakoski）**: 事実提示のみ。方法・手段・遺体を描かない。センセーショナルにしない。
- 判事（有罪確定の公人）: 記録に基づく中立記述。動機の断定を避ける。
- 数字は上記ロック値で台本を固定。以後ナレ本文は変えない（3チェック済 v003 を確定稿とする）。

## 出典リンク（主）
- Wikipedia: https://en.wikipedia.org/wiki/Kids_for_cash_scandal
- Juvenile Law Center: https://jlc.org/luzerne-kids-cash-scandal
- NPR（$200M, 2022）: https://www.npr.org/2022/08/18/1118108084/michael-conahan-mark-ciavarella-kids-for-cash
- NPR（改革）: https://www.npr.org/2012/03/03/147876810/after-scandal-new-rules-for-juveniles-in-pa-courts
- CNN 2009: https://www.cnn.com/2009/CRIME/02/23/pennsylvania.corrupt.judges/
- NBC（28年）: https://www.nbcnews.com/id/wbna44105072
- Democracy Now（Transue/Kenzakoski）: https://www.democracynow.org/2014/2/4/kids_for_cash_inside_one_of
- Transue 上院証言(2022): https://judiciary.pasenategop.com/wp-content/uploads/sites/42/2022/05/transue.pdf
- 減刑2024: https://www.timesobserver.com/news/local-news/2024/12/bidens-clemency-for-kids-for-cash-judge-questioned/
