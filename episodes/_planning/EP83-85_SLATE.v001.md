# EP83–85 SLATE v001 — CTR最大化から逆算した3本

**Built 2026-08-25.** **Status: PROPOSAL.** Nothing approved; `state` は全て `idea`。
Method = TOPIC_PIPELINE.v005 の確立手順そのまま: **需要÷現職**（definitive長尺の不在）を
`scripts/topic_demand_probe.py` で実測してから選ぶ。加えて本スレートは **CTRから逆算**する:
CTR_PLAYBOOK.v002 の実測式（夜の story-frame・結末を見せない・自CH勝者 carsearch 4.48% / terry 3.14%）
でサムネが成立する題材だけを通した。

## 0. 実測（このスレートのために新規に測った分・2026-08-25）

`TOPIC_DEMAND_PROBE_EP83_85.v001.json`（API ~800 units消費）。
EP73-76スレートの採点上位でまだ未計測だった8本:

| candidate (rubric順位) | median | ≥100k ch | 最大長尺(現職) | verdict |
|---|---|---|---|---|
| Takata airbag (#1, 119点) | **398** | 1 | 1.86M (26m) | **REJECT — 採点1位が需要ゼロ。ルーブリックは需要を測れない(3例目)** |
| East Palestine (#2) | 50,053 | 5 | 1.24M (21m) | 弱PASS — 帯域下限(lacmegantic 110k)未満 |
| San Bruno (#3) | 67,484 | 2 | **67k (NTSB公式)** | 枠は完全に空だが需要が帯域未満 |
| Firestone/Ford (#4) | 5,412 | 1 | 115k | REJECT |
| Deepwater Horizon (#5) | 270,672 | 9 | **5.3M neo** | REJECT — 現職が definitive |
| Door plug (#6) | 194,778 | 3 | **1.9M Mentour 41m** | REJECT — 航空は Mentour の庭 |
| Wells Fargo (#7) | 465 | 4 | 388k | REJECT |
| Aliso Canyon (#9) | 6,136 | 0 | なし | REJECT |

## 1. 決定の1段落

採点上位はほぼ全滅で、答えは既測定データの中にあった。
**EP83 = 冤罪×補償ゼロ**（`wrongfully convicted man receives no compensation from state`:
**median 1,927,083 / max 29.2M / 最大長尺 1.66M** = 盤上の全未着手候補で最大の需要×空き枠。
2026-08-11実測・EP70_45MIN probe）。**EP84 = エストニア号沈没**（median 297k / 現職1.21M、
海難ミステリは自CHの最強レーン=Titan・DBCooper の機構そのもの。SLATE50実測済み）。
**EP85 = トライアングル工場火災**（median 115k / **現職最大長尺 104k** = 需要が現職を上回る
盤上唯一の候補。SLATE50実測済み）。

## 2. 3本の中身

### EP83 — 冤罪×補償ゼロ · 仮題 *"The State Admitted He Was Innocent. It Owes Him Nothing."*

- **矛盾（1行）**: 州が無実を認めた瞬間に、州の補償義務が消えた。
- 有力な実話: **Kevin Strickland**（Missouri・43年服役・2021年11月釈放。州の補償法はDNA冤罪
  のみ対象で彼は対象外→州からの支払い**$0**）。○ 対抗馬として Glynn Simmons（OK・48年）と
  CourtListener shortlist 上位（Jardine III v. State HI 2024 / Stringer v. Bucks County 3d Cir 2025 =
  免責特権）を R3 で比較すること。判例原文は CASELAW_SHORTLIST.md にリンク済み。
- **CTR逆算**: 自CHのCTR上位2枚（carsearch 4.48% / terry 3.14%）は両方「夜×警察×あなた」の
  story-frame。この題材はその絵がそのまま撮れる（夜の刑務所ゲート・1灯のナトリウム灯・
  出てくる男は**シルエット**=実在存命人物の肖像firewall）。文字は2-4語で結末を見せない。
- **被り管理（必須）**: 冤罪本編は既に多数（hinton/cotton/centralpark/morton/norfolk/weimer…）。
  本作は**有罪の物語ではなく釈放後の補償の物語**として設計する。逮捕・裁判は前史3分以内。
- 注意: 固有名クエリ（kevin strickland）は median 7.7k = **名前は需要を運ばない。前提が運ぶ**。
  タイトルに人名を入れない（TITLE SPEC v002 とも一致）。

### EP84 — MS Estonia (1994) · 仮題 *"The Visor Was Found a Kilometre From the Wreck."*

- **矛盾（1行）**: 原因を確定できる物証を海底に残したまま、調査は閉じられ、現場は墓と宣言された。
- 852人死亡・欧州最大の海難。バウバイザー脱落→2020年の船体の穴の映像発見→再調査、の
  「閉じた調査が開き直る」構造は DBCooper 型の未解決機構。
- **CTR逆算**: 夜のバルト海・嵐・フェリーの灯 = プレイブックの「暗い・1光源・シアン寒色」を
  自然に満たす。Titan(自CH#1)と同じ「結末を知って見る海難」。
- リスク: 欧州題材（視聴者は91%米国55+男）— ただし Titan/Concordia が海難は国境を越えると実証済み。
  ○ 墓域指定(treaty)と2023年再調査結論のsensitivityをR3で確認。**Herald of Free Enterprise
  (med 105k)は同型のro-roフェリーのため本スレートから除外**（同型被り）。

### EP85 — Triangle Shirtwaist (1911) · 仮題 *"The Doors Were Locked So the Workers Couldn't Steal."*

- **矛盾（1行）**: 会社の財産を守るための施錠が、会社の労働者146人を閉じ込めた。
- **需要が現職を上回る盤上唯一の候補**（med 115k vs 最大長尺104k）。米国・制度の物語
  （この火事がNY労働法とニューディールを書いた）。犠牲者は全員1911年没=肖像リスクが最小。
- **CTR逆算**: 暗い階段室・施錠された扉・扉の下から漏れる暖色の火明かり=完璧な night story-frame。
- リスク2件（正直に）: ①1911年=時代再現。era_setting を episode_spec で厳密宣言しないと
  生成画像が現代に流れる。②**EP81 station（2003・出口の火事）と主題が近い**。EP81/82の台本が
  まだ無い今なら公開順を離せる。オーナー判断事項。

## 3. 次点（EP85の差し替え候補・実測済み）

| candidate | median | 現職 | 落とした理由 |
|---|---|---|---|
| San Bruno PG&E | 67k | 67k(公式のみ)=空 | 需要が帯域(110k)未満。書類が悪役の構造はSurfside級に良い |
| East Palestine | 50k | 1.24M | 需要帯域未満＋ニュース既視感。和解進行中でR2以上 |
| Uberlingen空中衝突 | 404k | 5.99M | 需要は立派だが現職がdefinitive |
| Hillsborough | 148k | 258k=空き | 英国サッカー×群集事故=itaewonと被り |

## 4. 承認ゲートと次の工程

1. オーナー: 3本の承認 or 差し替え（§3から）。特にEP85の station 被り判断。
2. 承認後: novelty check → `TOPIC_PIPELINE` 手順で R3 リサーチ（EP83は補償法制の法務確認=R3必須。
   EP84は treaty/再調査結論。EP85は一次資料が全てパブリックドメイン）。
3. 尺は実測ベースで設計（v005 §2: 長尺が正当化されるのは前提がTitan級の時だけ。
   EP83は1.93Mでその資格がある。EP84/85は11-12分帯から）。

**quota消費の記録**: 本スレートの新規実測 = search 8回 ≈ 800 units（8/25、上限10k/日）。
