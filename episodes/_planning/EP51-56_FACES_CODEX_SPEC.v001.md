# EP51–56 追加「顔」生成スペック（Codex用・one-shot・肌クリーン）v001 / 2026-07-28

オーナー方針:「顔が少ない話はCodexで追加。画像ができ次第、各話フォルダに保存していく仕様」。本書はその**確定仕様**。Codexはこの表の各行を **1プロンプト＝1枚（one-shot、バリアント選抜なし [[feedback-codex-one-shot-images]]）** で生成し、指定パスに保存する。私(Claude)のビルドが自動でこの `P##` を人物プールに取り込む。

## 運用フロー（この仕様で確定）
1. Codexが下表の1行につき1枚だけ生成。
2. 保存先は**2箇所**（両方に同名で保存）:
   - `H:/pd-media/assets/ai/<slug>/P<NN>.png`  （マスター）
   - `remotion/public/<slug>/img/P<NN>.png`   （レンダー用）
   - ※ `norfolk` は `remotion/public/norfolk/img/` が未作成 → 先に作る。
3. `<slug>` と採番:
   | 話 | slug | 採番 | 備考 |
   |---|---|---|---|
   | EP51 | willingham | **P25–P32**（8枚・上乗せ） | 既にP01–24あり。衝突回避で25から |
   | EP52 | morton | **P01–P16** | 既存はT01–03のみ |
   | EP53 | norfolk | **P01–P16** | 既存T01–03のみ・public/img新規 |
   | EP54 | flowers | **P01–P16** | 既存T01–03のみ |
   | EP55 | burge | **P01–P16** | 既存T01–03のみ |
   | EP56 | postoffice | **P01–P16** | 既存T01–03のみ・英国設定 |
4. 生成後、私が各話で人物を i2v（動きを付与）＋静止インサートとして使用。ビルド前に鉄壁ゲート（[[feedback-lessons-must-be-gates]] / PD_IRONCLAD_GATES）を通す。

## 全プロンプト共通ルール（Codexは各行プロンプトの前後にこれを必ず適用）
**● 共通スタイル（前置）**：`cinematic documentary film still, photoreal, 16:9 landscape, period-accurate, moody low-key cinematic lighting, muted cinematic color grade, 35mm film grain, shallow depth of field, natural realistic proportions,`
**● 共通品質（肌・ピント。オーナー指摘の傷/シミ/ボケ対策）**：`clean clear healthy skin with NO blemishes, NO scars, NO moles, NO acne, smooth natural skin, sharp crisp focus on the face, tack-sharp eyes, no motion blur, no lens blur on the subject,`
**● 共通フレーミング（後で動かすため頭上に余白）**：`framed with headroom above the head, subject not cropped tight, room for subtle camera motion,`
**● 共通の禁止（避けるべき）**：`AVOID: skin blemishes, scars, facial scars, spots, moles, acne, blotchy or leathery skin, over-detailed pores, blurry or soft face, plastic/CGI skin, cartoon, illustration, deformed hands, extra fingers, text, watermark, logo, modern smartphones, modern cars, anachronisms.`
**● 法的フレーム（厳守）**：全て **匿名の一般人**。実在の当事者（被告・被害者・実名の捜査官/検事/判事）の**肖像・そっくりさん・特定可能な人物は禁止**。各プロンプトは「a fictional generic period person, NOT a portrait of any real identifiable individual」を含める。被害者・遺族は**尊厳をもって・事件描写なし・暴力/遺体は一切描かない**。

---

## EP51 willingham（1991年 テキサス州コルシカナ／放火冤罪・火災科学・死刑）— P25–P32（上乗せ8枚）
既存P01–24を補完。放火捜査官・火災科学・小さな町・死刑制度の周辺人物を追加。
| P## | one-shotプロンプト（共通ルールと連結して使用） |
|---|---|
| P25 | a weathered Texas deputy state fire marshal in his 50s, 1991, khaki uniform, examining a scorched floor with a flashlight, medium shot, grim |
| P26 | a soft-spoken independent fire-science expert in his 60s, 1990s, wire glasses and a tweed jacket, studying photos at a desk, warm lamp light, close-up |
| P27 | a young overworked court-appointed defense attorney in a cheap 1991 suit, tired, standing in a dim county courthouse hallway, medium close-up |
| P28 | a Texas prison chaplain in his 50s in black clerical shirt, calm and heavy-hearted, dim corridor, close-up |
| P29 | a middle-aged white small-town Texas juror in a plaid shirt, 1991, sitting stiffly in a jury box, medium shot, ambivalent expression |
| P30 | a Huntsville-unit corrections officer in his 40s at a steel gate at night, cold blue light, medium shot, no insignia |
| P31 | a 1991 local newspaper reporter with a spiral notebook outside a courthouse, overcast, medium shot |
| P32 | an elderly rural Texas woman in a plain 1991 dress on a porch, sorrowful, soft dusk light, close-up |

## EP52 morton（1986年 テキサス州ウィリアムソン郡／妻殺害冤罪・ブレイディ・DNA・検事投獄）— P01–P16
| P## | one-shotプロンプト |
|---|---|
| P01 | a stern Texas county sheriff's investigator in his 40s, 1986, short haircut, holstered sidearm, standing in a suburban driveway, medium shot |
| P02 | a confident elected district attorney in his 40s in a sharp 1986 suit, courthouse steps, low angle medium shot (generic, not a real DA) |
| P03 | a supermarket manager in his early 30s in a 1986 store apron, exhausted and stunned, fluorescent aisle light, close-up |
| P04 | a 1980s forensic technician in a white coat at a lab bench with evidence bags, side light, medium close-up |
| P05 | a grandmother in her 60s in a modest 1986 dress, grief on her face, holding a tissue in a hallway, close-up |
| P06 | a defense attorney in his 50s, 1986, reading a case file under a desk lamp late at night, medium close-up |
| P07 | a modern Innocence-Project appellate lawyer in her 40s, 2010s, business blazer, holding a DNA report, bright office, medium shot |
| P08 | a shadowy man in a dark jacket seen from behind beside a green 1980s van at the treeline, no face visible, dusk, wide shot |
| P09 | a diverse 1986 Texas jury of twelve in a jury box, varied ordinary faces, wide shot, courtroom |
| P10 | a veteran homicide sergeant in his 50s, 1986, rumpled shirt and tie, at an interview-room table, cold light, medium shot |
| P11 | a court stenographer, a woman in her 30s, 1986, typing at a machine, profile, medium shot |
| P12 | a corrections officer in his 40s at a Texas prison visiting-room window, cold light, medium shot |
| P13 | a middle-aged man in a modern suit at a legal press conference, hopeful relief, camera flashes, close-up (generic exoneree, not a likeness) |
| P14 | a stern trial judge in black robes on the bench, 1986, low angle medium shot, wood-paneled courtroom |
| P15 | a young evidence clerk in a records room with boxed case files on steel shelves, medium shot, dim |
| P16 | a group of local reporters with 1986 microphones and cameras outside a courthouse, wide shot, midday |

## EP53 norfolk（1997年 バージニア州ノーフォーク／海軍水兵・虚偽自白・Det.Ford）— P01–P16
※水兵は**実在の4人と特定できない一般人**。被害者/遺族は尊厳・非描写。
| P## | one-shotプロンプト |
|---|---|
| P01 | a young generic US Navy enlisted sailor in his early 20s in 1997 dress-blue uniform, anxious, precinct interview room, close-up (fictional, not any real person) |
| P02 | a coercive plainclothes detective in his 50s, 1997, leaning over an interrogation table, hard overhead light, tense, medium shot (generic, not a real detective) |
| P03 | a Navy JAG defense attorney in service uniform, 1997, reviewing papers in a bare office, medium close-up |
| P04 | a Norfolk apartment-block exterior at night with a lone police cruiser, 1997, no people, wide establishing shot |
| P05 | a prosecutor in his 40s in a 1997 suit at a courtroom podium, medium shot |
| P06 | a grieving young Navy husband in his late teens, 1997, dignified sorrow, plain jacket, close-up (restrained, generic) |
| P07 | a 1997 interrogation room, empty steel chair under a bare bulb, cold, no people, medium shot |
| P08 | a Black man in his mid-20s in a 1997 jail jumpsuit, calm and resigned, holding-cell light, close-up (generic, the sole true offender archetype — not a likeness) |
| P09 | a federal judge in black robes, 2000s, thoughtful, at the bench, medium shot |
| P10 | four generic young sailors of mixed background in 1997 casual off-duty clothes, from behind, walking on a Navy base street, wide shot (backs only, unidentifiable) |
| P11 | a Virginia state trooper/press scrum outside a courthouse, 1997, overcast, wide shot |
| P12 | a forensic DNA analyst in a white coat at a 2000s lab, holding a printout, medium close-up |
| P13 | a group of exoneration supporters holding plain signs outside a government building, 2017, hopeful, wide shot |
| P14 | a middle-aged man in a modern suit at a 2017 pardon press conference, relief, camera flashes, close-up (generic) |
| P15 | a defense investigator in a 1997 car reviewing a case file, night, dashboard light, medium close-up |
| P16 | a Navy chaplain in uniform in a base chapel, calm, soft window light, medium shot |

## EP54 flowers（1996年 ミシシッピ州ウィノナ／ゴスペル歌手・6度の裁判・人種的陪審排除）— P01–P16
※主役級の黒人男性は**Flowersと特定できない一般人**。人種的緊張は事実に基づき慎重に。
| P## | one-shotプロンプト |
|---|---|
| P01 | a dignified Black man in his mid-20s in a modest 1996 Sunday suit, calm and steady, singing in a gospel choir, warm church light, close-up (fictional, not any real person) |
| P02 | a white Southern district attorney in his 50s in a 1996 suit, self-assured, at a courtroom lectern, medium shot (generic, not a real DA) |
| P03 | a small Mississippi town main street, 1996, modest storefronts, midday heat haze, no people, wide establishing shot |
| P04 | a jury-selection scene, a courtroom gallery of prospective jurors, mixed Black and white faces, 1996, wide shot, tense |
| P05 | a Black grandmother in a church hat in a 1996 courtroom gallery, quiet strength, close-up |
| P06 | a defense attorney in his 40s, 1996, frustrated, conferring at the defense table, medium close-up |
| P07 | a rural county courthouse exterior, red brick with white columns, Mississippi, 1996, overcast, wide shot, no people |
| P08 | a jailhouse informant type, a hard-faced man in his 30s in a 1996 jumpsuit, shifty, holding-cell light, close-up (generic, not a likeness) |
| P09 | a Black gospel family group in modest 1996 Sunday clothes on church steps, hopeful and worried, medium wide shot |
| P10 | a white county investigator in his 40s, 1996, short sleeves and tie, at a case board, medium shot |
| P11 | a modern appellate attorney in a sharp blazer holding a Supreme Court brief, 2010s, bright office, medium shot |
| P12 | a courtroom stenographer, a woman in her 40s, 1996, typing, profile, medium shot |
| P13 | a Southern trial judge in black robes on the bench, 1996, low angle, medium shot |
| P14 | a documentary/radio reporter with recording gear on a small-town Mississippi street, 2010s, medium shot (generic, no branding) |
| P15 | a Black man in his 40s in modern casual clothes stepping out of a courthouse into daylight, cautious relief, medium shot (generic exoneree) |
| P16 | a diverse group of townspeople on a Winona sidewalk, 1996, varied faces, wide shot, summer |

## EP55 burge（シカゴ 1972–1991／警察拷問・Area 2）— P01–P16
※拷問は**一切描写しない（人物のみ）**。指揮官/刑事は匿名・肖像禁止。生存者は尊厳。
| P## | one-shotプロンプト |
|---|---|
| P01 | a hard-faced white Chicago police detective in his 40s, 1982, cheap sport coat and shoulder holster, dim squad room, medium shot (generic, not a real officer) |
| P02 | a menacing plainclothes police commander in his late 30s, early 1980s, standing in a dark Area-station corridor, low light, medium shot (generic, not a likeness) |
| P03 | a Black man in his late 20s, early 1980s Chicago, dignified and wary, plain shirt, interview-room light, close-up (generic survivor archetype) |
| P04 | a South Side Chicago police station exterior at night, 1980s, brick and sodium streetlight, no people, wide establishing shot |
| P05 | a civil-rights defense attorney in his 40s in a 1980s corduroy jacket, determined, cluttered law office, medium shot |
| P06 | an empty grim interrogation room with a bolted steel chair and a bare bulb, 1980s, cold, no people, medium shot |
| P07 | a young US Army MP in Vietnam-era 1968 fatigues, field radio nearby, humid jungle base, medium shot (backstory, restrained, generic) |
| P08 | a Black grandmother in a 1980s South Side kitchen holding a photo, sorrowful, soft window light, close-up |
| P09 | a special prosecutor in a 2000s suit reviewing a thick report at a desk, medium close-up |
| P10 | a Chicago newspaper reporter at a 1990s cluttered newsroom desk with a rotary phone, medium shot |
| P11 | a torture-inquiry commission panel of officials at a long table, 2000s, wide shot |
| P12 | a Black man in his 50s in modern clothes at a 2003 press conference, weary vindication, camera flashes, close-up (generic pardonee) |
| P13 | a federal judge in black robes on the bench, 2010, medium shot |
| P14 | a line of uniformed Chicago police at a 1980s political press event outside City Hall, wide shot |
| P15 | a young Black man in a 1980s holding cell, frightened but composed, cold light, close-up (generic, no injury shown) |
| P16 | a group of community protesters holding plain signs outside a Chicago courthouse, 1990s, wide shot |

## EP56 postoffice（英国 1999–2015／Horizon IT冤罪・機関が加害者）— P01–P16
※英国設定（かつら/法服、英国の高街、村の郵便局）。実名の当事者・肖像禁止。Royal Mail等の商標は出さない。
| P## | one-shotプロンプト |
|---|---|
| P01 | a worried British sub-postmaster in his 50s behind a small village post-office counter, late 1990s, cardigan, staring at a beige computer terminal, close-up (fictional, not any real person) |
| P02 | a British sub-postmistress in her 40s in a modest cardigan, anxious, standing in a cramped village post-office branch, early 2000s, medium shot |
| P03 | a stern Post Office investigator in a grey suit with a lanyard, 2000s, institutional office, medium shot (generic official, not a real person) |
| P04 | a Fujitsu-era IT engineer in his 30s in a 1999 server room with tall beige computer racks, fluorescent light, medium shot (no logos) |
| P05 | a British barrister in a white horsehair wig and black court gown, dignified, outside the Royal Courts, medium shot |
| P06 | a modern British solicitor in a sharp suit holding a legal bundle on the steps of a court, 2020s, overcast, medium shot |
| P07 | a quiet English village high street with a small post office, red pillar box, overcast, no people, wide establishing shot |
| P08 | an elderly Welsh former sub-postmaster in his 60s in a flat cap and coat, weary dignity, close-up (generic) |
| P09 | a British public-inquiry hearing room, 2022, panel table and screens, wide shot, no identifiable faces |
| P10 | a High Court judge in British judicial robes, 2019, thoughtful, at the bench, medium shot (generic) |
| P11 | a distressed sub-postmaster at a kitchen table at night with account ledgers and bills, single lamp, close-up (restrained) |
| P12 | a calm silver-haired campaigner in his 60s in a plain jacket addressing a small group of supporters outside a hall, 2010s, medium shot (generic, not a likeness) |
| P13 | a corporate executive in a tailored suit behind a boardroom table, 2010s, cool light, medium shot (generic institution figure) |
| P14 | a group of British postmasters and supporters with plain placards outside Parliament, 2020s, wide shot |
| P15 | a British TV news reporter with a microphone on a London street, 2020s, medium shot (no branding) |
| P16 | a young British court usher in a modern courtroom, 2020s, medium shot |

---

## 生成後に私(Claude)がやること
- 各 `P##` を i2v（Wan）で軽く動かして人物モーションクリップ化 → `H:/pd-media/assets/ai_video/<slug>/` に追加（顔が静止＝紙芝居を避ける）。
- 静止インサートは `remotion/public/<slug>/img/` から直接使用。
- 人物比率 ≥40%（craftルール）を満たすよう asset_manifest に取り込み → build → 鉄壁ゲート → レンダー。
- Codex生成物も念のため黒スタブ/真っ黒をゲートで検査（<50KB or luma<8 は弾く）。
