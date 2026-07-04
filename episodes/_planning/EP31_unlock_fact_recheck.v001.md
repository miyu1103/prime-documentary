# EP31 `fact_recheck.v001` (R2) — Compelled Phone Unlock（第4/第5修正）

**Status:** 出典付きで確定（2026-07-04 リサーチ・独立検証済み）。判例なので原則 confidence 高。ただし**未決着=「割れている/最高裁未判断」を必ず明示**。2件は最終ロック前に一次ソース要確認（下記⚠CONFIRM）。

## ★ 確定ファクト（confidence: H=高 / M=中）

### 中核ドクトリン
- **Riley v. California, 573 U.S. 373 (2014)（H）**：2014/6/25、全員一致（Roberts長官）。**逮捕に伴う捜索でも、スマホの中身を見るには原則令状が必要**。名台詞「get a warrant」。⚠**Riley は"中身を捜索する"話であり、"本人に開けさせる"話ではない**（後者は第5修正の別問題）。
- **第5修正の"testimonial（供述的）"（H）**：privilege は「①強制され②不利で③供述的」な伝達のみを守る。"供述的"＝**頭の中の中身（知っている事実）を明かす**こと。基準は *Doe v. United States*, 487 U.S. 201 (1988) の**「金庫の暗証番号（言わなくてよい）vs 鍵（渡せる）」**比喩。
- **暗証番号＝供述的（守られやすい）／生体＝物理的で非供述的（守られにくい）（H）**：指をセンサーに置く・顔を向けるのは "no cognitive exertion"＝採血・指紋採取・ラインナップと同類（*Schmerber v. California*, 384 U.S. 757 (1966)；*United States v. Dionisio*, 410 U.S. 1 (1973)）。⚠ただしこの非対称は**トレンドであって全国ルールではない**（Brown が反例）。
- **"foregone conclusion（既知の結論）"法理（H）**：起源 *Fisher v. United States*, 425 U.S. 391 (1976)。産出行為の供述的側面も、政府が既に"合理的特定性"で知っていれば privilege を破る。**核心の争点＝この法理の対象を「暗証番号そのもの」（政府勝ちやすい）とみるか「中のデータ」（本人勝ちやすい）とみるか**。ここで裁判所が割れる。

### 暗証番号を巡る州の分裂
- **守られた側（H）**：*Commonwealth v. Davis*, 220 A.3d 534 (Pa. 2019)（4–3。パスワードは供述的、foregone conclusion は記憶した暗証番号には及ばない）／*Seo v. State*, 148 N.E.3d 952 (Ind. 2020)（解除の強制は違反）／*State v. Valdez*, 2023 UT 26 (Utah 2023)（口頭の暗証番号は供述的、foregone conclusion 不適用）。
- **強制できる側（H）**：*State v. Andrews*, 243 N.J. 447 (2020)（4–3。産出は供述的だが foregone conclusion で privilege 敗退＝"降伏"に過ぎない、対象は**暗証番号そのもの**）／*People v. Sneed*, 2023 IL 127968 (Ill. 2023)（同法理適用・暗証番号に焦点）。
- **フロリダは州内で分裂（H）**：守る *G.A.Q.L. v. State*, 257 So. 3d 1058 (Fla. 4th DCA **2018**) ↔ 強制可 *State v. Stahl*, 206 So. 3d 124 (Fla. 2d DCA 2016)。州最高裁は未解決。

### 生体認証を巡る連邦の分裂
- **強制OK（非供述的）（H）**：*United States v. Payne*, 99 F.4th 495 (9th Cir. 2024)（2024/4/17）。警察が**親指を押し当てて解除**＝供述的でない＝採血/指紋と同類。留保①「**どの指か本人に選ばせていたら違ったかも**」②Payne は**既に自分の電話だと認めていた**③foregone conclusion には依拠していない。**9th Cir. 内でのみ拘束**。
- **強制NG（供述的）（H）**：*United States v. Brown*, 125 F.4th 1186 (D.C. Cir. 2025)（2025/1）。**指紋解除は供述的＝違反**（「開け方を知っている」と伝えるから）。Payne を「①命令 vs 物理的に指を掴む②指の選択」の点で区別。＝**生体も裁判所が対立**。

### 最高裁の姿勢
- **統一ルールなし（H）**：上告不受理を繰り返す＝*Pennsylvania v. Davis* No.19-1254（2020/10/5 denied）／*Andrews v. New Jersey* No.20-937（2021/5/17 denied）／*Sneed v. Illinois* No.23-5827（2024/2/26 denied）。**最高裁は強制暗証番号/生体解除を一度も本案判断していない**＝州境で権利が変わる。
- **国境例外（M・補足）**：国境/空港では border-search exception で令状不要の主張。1st/4th/9th 巡回は forensic 捜索に reasonable suspicion 要、11th は不要、S.D.N.Y. *Smith*(2023) は令状要と判断＝ここも流動的。⚠Riley（逮捕付随）と国境は別枠。

## ✅ CONFIRM 済（一次ソース確認完了・2026-07-04）
1. **Utah *Valdez*（No. 23-1020）（H）**：**2024/6/24 上告不受理（cert denied）**（Order List 602 U.S.／SCOTUS公式ドケット）。原判決 *State v. Valdez*, 2023 UT 26（2023/12/14）＝口頭の暗証番号は供述的・foregone conclusion 不適用。→ 「最高裁は受理せず＝未解決のまま」の裏付け。
2. **S.D.N.Y. *United States v. Smith*（H）**：**673 F. Supp. 3d 381 (S.D.N.Y. 2023)**、Rakoff判事、No.22-cr-352(JSR)、2023/5/11。国境でのスマホ捜索に令状を要すると判断した初の地裁（ただし good-faith 例外で証拠排除は認めず）。

## 🚫 SCRIPT GUARDRAILS（台本Pass1で必ずチェック）
- **第4修正（捜索＝Riley）と第5修正（強制自白＝解除）を混同しない**。「令状があれば開けさせられる」と短絡しない。
- **判旨は中立に**。各事件の被告の犯罪内容（児童ポルノ・薬物・情報漏洩等）は**深入り禁止**。主役は"あなた"と法理であって被告ではない。
- **"あなたにアドバイスしている"口調を避ける**。「多くの裁判所は」「州による」「まだ決着していない」で括り、**法的助言にしない**。
- **Payne を"全生体OKの青信号"にしない**（留保①②③・9th Cir. 限定）。**Brown を"生体は守られる"の全国ルールにしない**。

## 🧨 禁止（MYTHS＝事実として言わない・row15点検で除去）
1. ❌「最高裁が"警察はスマホを開けさせられない"と判断した」→ **未判断**。Riley は"捜索"のみ。
2. ❌「Riley で常に令状が要る」→ 逮捕付随の話。緊急例外・国境例外は別。**開けさせる**強制も別。
3. ❌「暗証番号は全米で常に守られる」→ NJ/Il 等は強制可。**州次第**。
4. ❌「生体認証は絶対に守られない」→ Brown(D.C. 2025) は逆。**割れている**。
5. ❌「顔・指は無防備／番号は聖域、という綺麗な全国ルールがある」→ **トレンド**であり反例あり。「多くの裁判所」「主流の流れ」と表現。
6. ❌「暗証番号を拒めば不利に扱われない」→ 一様でない（*Valdez* は不利な言及を禁じたが全国ルールでない）。強制可の州では**法廷侮辱**の恐れ。

## FR ラベル（`script.annotated.v001.json` の `claim_ids` 対応）
- **FR-R** — Riley v. California, 573 U.S. 373 (2014)：スマホの中身の捜索には原則令状（"見る"の話）。
- **FR-T** — 第5修正の"testimonial"／金庫の暗証番号 vs 鍵（Doe 1988）：記憶した番号＝供述的・体の特徴＝非供述的。
- **FR-P** — U.S. v. Payne, 99 F.4th 495 (9th Cir. 2024)：強制指紋解除は非供述的＝合違反でない（留保①どの指か選ばせたら別②本人が電話と認めていた・9th Cir.限定）。
- **FR-B** — U.S. v. Brown, 125 F.4th 1186 (D.C. Cir. 2025)：強制指紋解除は供述的＝違反（Payneと対立）。
- **FR-PC-prot** — 暗証番号は守られた：Davis(Pa 2019)/Seo(Ind 2020)/Valdez(Utah 2023)。
- **FR-PC-comp** — 暗証番号は強制可：Andrews(NJ 2020)/Sneed(Ill 2023)。
- **FR-FC** — foregone conclusion（Fisher 1976）：対象を「番号」か「中のデータ」かで結論反転。
- **FR-SC** — 最高裁は未判断：Davis(2020/10/5)/Andrews(2021/5/17)/Sneed(2024/2/26) 上告不受理＋Valdez(2024/6/24) 不受理＝州境で権利が変わる。
- **FR-FL** — フロリダ州内分裂：G.A.Q.L.(4th DCA 2018 守る) vs Stahl(2d DCA 2016 強制可)。（本編未使用・予備）
- **FR-BORDER** — 国境例外は別枠・流動的：Smith(S.D.N.Y. 2023)ほか。（本編未使用・予備）

## 出典（検証済URL）
Riley: supreme.justia.com/cases/federal/us/573/373 ／ Fisher: supreme.justia.com/cases/federal/us/425/391 ／ Davis(Pa): law.justia.com/cases/pennsylvania/supreme-court/2019/56-map-2018 ＋ scotusblog Pennsylvania v. Davis ／ Seo(Ind): law.justia.com/cases/indiana/supreme-court/2020/18s-cr-595 ＋ eff.org 2020-06 ／ Andrews(NJ): law.justia.com/cases/new-jersey/supreme-court/2020/a-72-18 ＋ scotusblog ／ G.A.Q.L./Stahl(Fla): jolt.law.harvard.edu/digest/compelled-decryption-in-florida-a-foregone-conclusion ／ Payne(9th): cdn.ca9.uscourts.gov/datastore/opinions/2024/04/17/22-50262.pdf ／ Brown(D.C.): arnoldporter.com 2025-03 "When Your Fingers Do the Talking" ／ Valdez(Utah): law.justia.com/cases/utah/supreme-court/2023/20210175 ／ Sneed(Ill): law.justia.com/cases/illinois/supreme-court/2023/127968 ／ 国境: congress.gov/crs-product/LSB10387 ＋ eff.org 2023-05 ／ 生体まとめ: americanbar.org（compelled-biometrics-fifth-amendment-rights）。

## Vivid（本編で効く"見せられる"真実・全て出典あり）
1. **金庫の暗証番号 vs 鍵**（Doe 1988）＝あなたの記憶は明かさなくていいが、体は差し出させられる。
2. **同じ行為・真逆の結論**：親指解除は 9th Cir.（Payne）で合法、D.C. Cir.（Brown）で違反。**同じ国で答えが割れている**。
3. **州境で変わる権利**：Pa/In/Ut では番号が守られ、NJ/Il では開けさせられる。
4. **最高裁が3回、扉を閉めた**：Davis・Andrews・Sneed で上告不受理＝誰も統一していない。
5. **分かれ目は"何を既知とみるか"**：番号（政府勝ち）か、中のデータ（あなた勝ち）か——foregone conclusion の一線。
6. **Payne の留保**：もし"どの指で開けるか本人に選ばせて"いたら、結論は違ったかもしれない＝**選ぶ＝頭を使う＝供述的**の境界。
