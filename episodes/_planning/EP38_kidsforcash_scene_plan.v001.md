# EP38 — Kids for Cash — Scene Plan / シーン割り v001

> 目的: 台本 v003 の1ビートごとに「絵・動き・語同期・画面文字」を割り当て、**ナレの意味と画を一致**させる（設計書§4）。汎用B-rollの流し込み禁止・素材被り禁止（footage_diversity）。
> 動きの型: **[W]**=Wan2.2 A14B i2v（実写風に本当に動かす・見せ場・約10カットに限定）／**[D]**=2.5D深度ドリー（ヒーロー静止画）／**[MK]**=motionkit部品（動く図）／**[AE]**=After Effects見せ場（数字カード・タイトル・判決）／**[FT]**=実写B-roll（OpenCLIP意味検索）。
> source/truth: 画像=ai_codex/symbolic（演出・実記録ではない）。数字カード=motiongraphic/factual（台帳CLM準拠）。実写=footage/factual。

## HOOK（先頭・語同期・約16s）
| ビート（ナレ要旨） | 絵/資産 | 動き | 語同期→リビール | 画面文字 | source/truth |
|---|---|---|---|---|---|
| 17歳の少女が副校長を揶揄する偽ページを作った | S02 寝室モニタ | [D] | "web page" で画面点灯 | — | ai/symbolic |
| いたずら。せいぜい居残りのはずだった | S01 学校の廊下 | [D] ゆるドリー | "prank" | — | ai/symbolic |
| 判事は3か月、施設へ送った | S03 90秒の審理 | **[W]** | "three months" | 〔CARD 3 MONTHS〕[AE] StampReveal | ai/symbolic + card/factual(CLM-10) |
| 審理は約90秒、弁護士も告げられず | S03（寄り） | [D] | "ninety seconds"/"lawyer" | 〔CARD 90 SECONDS〕NumberTicker＋〔NO LAWYER〕 | card/factual(CLM-08) |
| 判事は送った子の数だけ金を受けていた | S07 金の流れ | **[W]** | "being paid"/"every child" | — | ai/symbolic |

## OP（ブランドタイトル）
| — | Bookends OPタイトル | [AE] 文字スタッガー＋マスク切上げ | — | 番組ロゴ | brand |

## ACT 1 — 普通の子供たち
| ビート | 絵/資産 | 動き | 語同期 | 画面文字 | source/truth |
|---|---|---|---|---|---|
| ルザーン郡・炭鉱町・裁判所は second chance の場のはずだった | S21 炭鉱町の裁判所 | [D] 引き→寄り | "second chance" | LowerThird "Luzerne County, PA" | ai/symbolic |
| 子供たちの罪は小さかった（喧嘩・万引き・悪ふざけ） | S24 学校から消えた席 → S02 | [D]×カット刻み | "small things" | — | ai/symbolic |
| 始まりは署名。弁護士放棄の用紙にサインさせられた | S22 権利放棄の署名 | **[W]** 手元の微動 | "signature"/"lawyer" | 〔WAIVER OF COUNSEL〕StampReveal | ai/symbolic + card |
| ロー姿の男＝Ciavarella | S03 審理（判事席の影） | [D] あおり | "Ciavarella" | LowerThird "Mark Ciavarella — Juvenile Court Judge" | ai/symbolic |
| 放棄した子の約50%が施設へ／州平均8.4% | S26 50% vs 8.4%（象徴） | **[MK] ComparisonBars** | "eight point four percent" | 〔8.4% vs ~50%〕 | motiongraphic/factual(CLM-08) |
| placement は同日連行・数か月・学校も親の顔も失う | S23 連行→S25 移送→S06 独房 | [D]×3 速いカット | "taken that same day" | — | ai/symbolic |
| 速い。1〜2分。側扉から連れ去られる | S23 側扉 | **[W]** 扉が閉まる | "a minute. two." | — | ai/symbolic |
| 親は判事を信じた。その信頼が最初の売り物 | S11 傍聴の親／S23 | [D] | "who doesn't believe a judge" | — | ai/symbolic |

## ACT 2 — 仕組み（金の流れ）
| ビート | 絵/資産 | 動き | 語同期 | 画面文字 | source/truth |
|---|---|---|---|---|---|
| 金を追え。一階上から始まる | S28 権力の椅子（Conahan） | [D] ドリーイン | "follow the money" | LowerThird "Michael Conahan — President Judge" | ai/symbolic |
| 郡営拘置所を財源で干して閉鎖へ | S29 施設が閉じる/建設 | [D] | "starved it of funding" | — | ai/symbolic |
| 残るは営利施設2つ | S05 営利施設 外観 | **[W]** 光・空気が動く | "for-profit jail" | — | ai/symbolic |
| 満床＝利益。ベッドは一人ずつ埋まる | S08 子供＝商品 | **[W]**（本エピの核カット） | "one child at a time" | — | ai/symbolic |
| Mericleが建て、Powellが運営。3年で$2.8M | S30 数えられる札束 | **[MK] MoneyFlow**（施設→判事の経路） | "two point eight million" | 〔$2.8 MILLION〕[AE]数字カード | motiongraphic/factual(CLM-05,06) |
| 呼び名は"finder's fee"。真名はもっと簡単 | S15 押収/証拠 | [AE] StampReveal "FINDER'S FEE"→"BRIBE" | "finder's fee" | 〔FINDER'S FEE→BRIBE〕 | motiongraphic |
| 子供が判事に送られ、支払いが続いた | S07 金の流れ（別角度） | [D] | "a payment followed" | — | ai/symbolic |
| 弁護士無し出廷は他所の7〜11倍＝抵抗できない | S18 権力vs子供 | **[MK] NumberTicker/RadialGauge** | "seven to eleven times" | 〔7–11×〕 | motiongraphic/factual(CLM-09) |
| 速すぎる審理は不機嫌ではない。在庫管理だ | S08（寄り）/S17 記録棚 | [D] | "inventory" | 〔INVENTORY〕小 | ai/symbolic |

## ACT 3 — 壊れた一家（人間の代償）
| ビート | 絵/資産 | 動き | 語同期 | 画面文字 | source/truth |
|---|---|---|---|---|---|
| 数字は沈黙する。一つの家に立つ | S27 空席の机 | [D] 静かな寄り | "stand in one house" | — | ai/symbolic |
| Ed Kenzakoski・17歳・レスラー・小さな罪で送られた | S24／S06 独房 | [D] | （名は字幕）"seventeen" | LowerThird "Edward Kenzakoski, 17" | ai/symbolic + factual(CLM-11) |
| 帰ってきた少年は別人。23歳で自らの命を絶った | S10 空の椅子（喪失） | **[W]** 光がゆっくり消える | "took his own life" | — | ai/symbolic ※自死は象徴のみ |
| 母 Sandy Fonzo が裁判所前で対峙 | S33 対峙（母と元判事） | **[W]** or [D] | "Sandy Fonzo" | LowerThird "Sandy Fonzo — his mother" | ai/symbolic + factual(CLM-12) |
| 数千人の子。13歳15歳で犯罪者と言われ信じた。記録が一生追う | S18 権力vs子供／S17 | [D]×カット刻み | "thousands of children" | — | ai/symbolic |

## ACT 4 — 暴かれる（司法が司法を裁く）
| ビート | 絵/資産 | 動き | 語同期 | 画面文字 | source/truth |
|---|---|---|---|---|---|
| 何年も握り潰された（相手が子供と親だから） | S17 官僚機構の腐敗 | [D] | "waved off" | — | ai/symbolic |
| 一本の電話→フィラデルフィアの Juvenile Law Center | S31 FBI/調査 → 事務所 | [D] | "Juvenile Law Center" | LowerThird "Juvenile Law Center, Philadelphia" | ai/symbolic + factual(CLM-13) |
| 数件でなく「機械」だった：数百人・同じ型 | S17／S08 | **[MK] MechanismReveal** | "a machine" | — | motiongraphic |
| 州最高裁が法廷を"なかったこと"に。数千件抹消 | S13 記録の抹消 | **[MK] RecordsScan**＋[AE] | "vacating thousands" | 〔THOUSANDS VACATED〕（具体数焼かない） | motiongraphic/factual(CLM-14) |
| だが記録は消せても、失った年月は戻らない | S27／S10 | [D] | "the time could not" | — | ai/symbolic |
| FBIは聴いていた。Conahan 17.5年 / Ciavarella 28年 | S31 盗聴 → S35 収監 | **[W]** 収監の扉／[AE] | "twenty-eight" | 〔28 YEARS〕NumberTicker＋〔17.5 YEARS〕 | ai/symbolic + card/factual(CLM-15) |
| 司法が司法を裁いた（ローブに告発の光） | S14 司法が司法を裁く | **[W]** 光が差す | "the men who had sold it" | — | ai/symbolic |
| $2億超の賠償命令 | S15／S30 | **[MK] NumberTicker** | "two hundred million" | 〔$200 MILLION+〕 | motiongraphic/factual(CLM-16) |
| 改革：子供に弁護士を | S36 弁護士が隣に | [D] 暖色 | "a lawyer at their side" | — | ai/symbolic + factual(CLM-18) |

## ED — 余韻＋射程＋登録CTA
| ビート | 絵/資産 | 動き | 語同期 | 画面文字 | source/truth |
|---|---|---|---|---|---|
| 法廷は金が外に留まる唯一の部屋のはずだった | S12 裁判所 外観 | **[W]** 夕光が動く | "outside the door" | — | ai/symbolic |
| その約束に値札。一人あたり数千ドル | S26／S08 | [D] | "a few thousand dollars a head" | — | ai/symbolic |
| 判事は去った。一人は減刑され早期釈放。子供は年月を返されない | S35 収監→S20 権利の線 | [D]→[AE] | "commuted" | LowerThird "Conahan — sentence commuted, 2024" | ai/symbolic + factual(CLM-17) |
| 埋もれさせないなら登録を。次回も普通の人と制度の話 | S19 平穏な日常／S20 | [D]＋[AE] CTA | "subscribe" | 登録CTA（語同期・自然文） | brand |
| ED タイトル | Bookends ED | [AE] | — | 番組ED | brand |

---
### 動き配分サマリ（binding）
- **[W] Wan i2v ＝ 10カット**（S03, S07, S08, S05, S22, S23側扉, S10, S33, S35, S14/S12いずれか）＝最重要の見せ場のみ。各41フレーム・§5.5数値。→ G-CAP-1/G-TIME-1 で事前検算。
- **[MK] motionkit ＝ 8種**（ComparisonBars, MoneyFlow, NumberTicker, RadialGauge, MechanismReveal, RecordsScan, StampReveal, VerdictReversal）。
- **[AE] 見せ場 ＝ 数字カード5枚＋OP/ED＋判決**（$2.8M / 90s / 8.4% / 28y / $200M）。文字は§5.6タイポ・brand色。
- 残りは [D] 2.5D と [FT] 実写。全カット静止で止めない。素材被り禁止・天秤等の汎用象徴は使わない。
- 語同期は faster-whisper 語タイムに±1フレーム。数字カードは具体数を焼く/焼かないを CLM に従う（抹消件数は焼かない）。
