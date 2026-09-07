# 縦型ショート 完全設計書 — 第28話（PD-2026-028-forfeiture / 民事没収 Sourovelis）別スレッド制作用・自己完結版

第28話（本編 `PD-2026-028-forfeiture`）に1対1で対応する縦型ショート1本。**この設計書だけで別スレッドの Claude Code が単体で完成まで作れるよう、仕様・数値・言い回しロックをすべて本文に書ききる。** 書式・数値・ロックの基準は第25話ショート設計書（`_short_spec_25.md`）／`SHORTS_EP19-24.md`（§0 共通仕様・per-SHORT 表・画像プロンプト・FACT-CHECK・RISK）に完全準拠する。

> **重要（オーナー指示・EP19-24/25 と同一）**
> - ショートは**別スレッドの Claude Code** が制作する。この設計書が唯一の指示書。
> - **Codex 画像生成は必須ではない。** 縦画像は「①`H:\pd-media\assets\factory\` の商用OK**動画フッテージ**（縦クロップ）②本編 `PD-2026-028-forfeiture/05_visuals` の流用 ③必要な所だけローカル（SD3.5 `sd35_gen.py` / SDXL `gen_max.ps1`）で縦生成」で賄ってよい。下の各 `image` プロンプトは**ローカル/SDXLで作る場合の指定**。動く素材でまかなえるものはフッテージ優先（紙芝居回避）。
> - チャンネルは**US英語**。VO・テロップ・サムネ文言は下表の英語をそのまま使う。翻訳工程なし。
> - 動きの基準は本編と同じ新テンプレ思想（フッテージ主役＋2.5D＋モーショングラフィックス、ただの左右パン/ズーム禁止、金の縦スイープ禁止、黄色ウォッシュ禁止）。
> - **題材が繊細（民事没収・存命の家族が実在）。** 中立・法的に正確・実在肖像なしを厳守。特徴付けは必ず帰属し、結末は事実どおり（後述 RISK/LOCKS）。

## §0 共通仕様（`_short_spec_25.md` §0 と同一。要点を再掲）

- **画面**: 縦 9:16 / 1080×1920 / **尺 ~50〜55秒**（本話は5 VOビートで ~55s）/ 字幕（テロップ）常時 / モバイル前提の大きな文字。
- **本人肖像なし**（実在の存命人物 Christos Sourovelis / Markela Sourovelis / 息子 Yianni / 共同原告 Doila Welch・Norys Hernandez・Nassir Geiger の顔・似顔・声真似は禁止・invariant 11）。**画像内に可読な実在テキスト/ロゴ/公印/紋章/事件番号を描かない**（テロップは Remotion で焼く）。
- **ナレ音声**: 本編と同じ声 `ElevenLabs VOICE_ID nPczCjzI2devNBz1zQrb / eleven_multilingual_v2 / stability0.35 / similarity0.80`。英語生成（承認済・追加確認不要）。
- **音**: 4層ミックス（BGM／緊張／環境／SFX）＋ダッキング＋**2パス静的 -14 LUFS**。中盤で音量が痩せないよう `speechnorm+グルー圧縮`（`build_short_mix.py` の short17〜設定を踏襲）。GAP≈2.70s。
- **コンポジション**: 縦Remotion `Short.tsx`（1080×1920）。時間表どおり並べ、上品に動かす。カットはスピーディー・ナレの無音は最大0.6秒。
- **サムネ**: `short28_thumb.png`（<2MB）＋大文言を `ShortThumb` で重ねて書き出し。Shorts公開時は**先頭0.7sにカバーフレーム焼き込み**（libx264 crf18）。
- **VO末尾CTA（共通）**: "Watch the full story on the channel. Follow for more."
- **画像プロンプト末尾に共通スタイルを付す（STYLE suffix）**: *"museum-grade cinematic symbolic documentary still, vertical 9:16, deep-navy / black base, cold electric-blue institutional light, restrained muted-gold warmth for the home, film grain, no faces, no readable text / logos / seals, symbolic reconstruction (not authentic footage)."*
- **画像 HARD RULES（全プロンプト共通・厳守）**: no faces / NO readable text / NO logos, badges, seals or coats-of-arms / NO document, certificate, docket or notice titles (SDXL fakes text) — 被写体は**文字のない象徴のみ**（cold light の下の押収現金、無人の押収車置き場、光の帯に浮かぶ家や車、天秤、無人の法廷）。各1文で書く。
- **保存先**: `H:\pd-media\assets\ai\shorts\short28\`（使う画像＋`short28_thumb.png`）。フッテージ流用時はそのパスを `image` 欄に併記。

## §1 公開ゲート

- **1日1本ちょうど・12:00 JST 予約**（`publishAt`）。新規予約前に全 `publishAt` を監査し空き日へ。衝突は `--replace` で日付修正。
- オーナーが一度OK。**R2 は法務目線レビュー必須**（下の RISK 参照）。存命の家族が実在するため公開前レビューは軽くない。
- 最終チェック: 本人肖像なし・中立・広告安全・**言い回しロック**・字幕がナレに一致・切れ目が自然。
- 本編台本（`PD-2026-028-forfeiture/03_script/script.annotated.v001.json`）が更新されたら VO/FACT-CHECK を取り直す。

---

## SHORT #28 →（本編 第28話 民事没収 / Sourovelis v. City of Philadelphia）A son sold about $40 of heroin — so the city moved to take his parents' house, and treated the house itself as the guilty party.
**The one surprise**: The parents had broken no law and were charged with nothing — yet under a tool called civil forfeiture the city of Philadelphia sued the *house* itself ("the State versus one house"), so the innocent owners had to prove their own home had done nothing wrong; only after the family joined the Institute for Justice in a class action did the city, in 2018, agree to dismantle a machine that between 2002 and 2014 had seized 1,200+ homes and funneled the proceeds back into police and prosecutor budgets.

| time | VO (English) | telop (English, short) | image |
|---|---|---|---|
|0:00-0:03|A court once ordered a family's house seized — not because they broke a law, but because their house supposedly did.|THE HOUSE<br>ON TRIAL|01|
|0:03-0:17|Christos Sourovelis painted houses for a living, and earned a modest two-story home in Somerton, northeast Philadelphia, worth a little over three hundred thousand dollars. In March 2014 his twenty-two-year-old son sold about forty dollars of heroin to a police informant.|A $40<br>SALE|02,03|
|0:17-0:34|So the city of Philadelphia moved — not against the son, but against the house. Using a tool called civil forfeiture, prosecutors won an order to seize and seal the home with no one from the family even present. In these cases the property itself is the defendant — "the State versus one house" — and the innocent owners can be left to prove their own home did nothing wrong.|SEIZE<br>AND SEAL|04,05|
|0:34-0:50|And they were never unusual. Between 2002 and 2014 Philadelphia used forfeiture to take more than twelve hundred homes and over fifty million dollars in cash — the typical seizure just a hundred and seventy-eight dollars — with nearly six million a year flowing back into police and prosecutors' own budgets. So the family and the Institute for Justice filed a class action, and in 2018 the city agreed to dismantle the machine and pay millions back.|1,200+<br>HOMES|06|
|0:50-0:55|Watch the full story on the channel. Follow for more.|WATCH THE<br>FULL STORY|07(hold)|

- `short28_01.png` A modest brick row-house front door at night, sealed and untouchable, washed by cold electric-blue institutional light with the warm home dark behind it, no faces, no notice, no readable text — *[common style suffix]* (**footage alt**: `factory` `AF-BG-1742__front_door_house` / `AF-BG-1667__suburban_house_exterior_night`, vertical crop)
- `short28_02.png` A painter's ladder and paint roller leaning against a modest two-story suburban home in soft warm daylight, an earned lived-in house, no face, no signage, no readable brand — *[common style suffix]* (**footage alt**: `factory` `AF-BG-21903__american_suburb_aerial` or `AF-BG-22092__white_picket_fence`, vertical crop)
- `short28_03.png` An extreme macro of two anonymous twenty-dollar bills passing between gloved hands on a dark rain-slick street, faint red-blue light on brick, no drugs shown, no faces, no readable serial text — *[common style suffix]*
- `short28_04.png` A cold empty courtroom of vacant benches with one hard shaft of light falling on a single bare table where no one from the family sits, bureaucratic and faceless, no bench seal, no text — *[common style suffix]* (**footage alt**: `factory` `AF-BG-14510__courtroom_empty_wide`, vertical crop)
- `short28_05.png` A single modest house lifted into a stark cold shaft of light as if placed in a dock on trial, isolated in deep navy, the building itself as the accused, no faces, no text — *[common style suffix]*
- `short28_06.png` Under cold institutional light, dense stacks of seized cash and rows of car keys and a distant impound lot of silent cars, vast and machine-like, dwarfing one small lonely banknote, no faces, no logos, no readable text — *[common style suffix]* (**footage alt**: `factory` `AF-BG-7989__cash_stacks_money` or `AF-BG-0825__money_cash_counting`, vertical crop)
- `short28_07.png` An ordinary house key turning in a warm front door at golden hour as the cold blue light lifts and daylight returns, generous negative space above for the CTA endcard, no faces, no text — *[common style suffix]* (**footage alt**: `factory` `AF-BG-9208__small_town_main_street` golden-hour clip, vertical crop)
- **thumbnail** `short28_thumb.png` A modest home held in a cold shaft of light behind a sealed front door ／ headline: **"THE HOUSE WAS THE DEFENDANT"** ／ badge: "$40"

> **FACT-CHECK** — court order to seize the house, owners never charged with anything=SPN-0001 (FR-2a + FR-1a); Christos Sourovelis, house painter, modest two-story home in Somerton, NE Philadelphia, worth a little over $300k=SPN-0003 (FR-1a); March 2014, his 22-year-old son (Yianni) sold about $40 of heroin to a police informant=SPN-0005 (FR-1b + FR-1c + FR-1d); May 8 2014 prosecutors won a seize-and-seal order with no family member present, no prior hearing=SPN-0009/SPN-0010 (FR-2a); civil forfeiture makes the property the defendant ("the State v. one house") and can leave the owner to prove the property innocent=SPN-0012/SPN-0013 (FR-2c); 2002-2014 Philadelphia took 1,200+ homes, 3,500+ cars, $50M+ in cash, typical/median cash seizure ~$178=SPN-0019 (FR-4b + FR-4d); ~$6M/yr flowed back into police and DA budgets=SPN-0022 (FR-4a + FR-4f); the Sourovelises + the Institute for Justice filed the firm's first class action, Sourovelis v. City of Philadelphia=SPN-0024 (FR-3a + FR-3b); in 2018 the city agreed (federal consent agreements) to dismantle the program, created a ~$3M repayment fund, and Courtroom 478 was closed=SPN-0028/SPN-0029 (FR-5a + FR-5b).

> **RISK (R2 — sensitive: civil-forfeiture policy + living private family)** — LOCKS:
> 1. **The parents' innocence is explicit and load-bearing.** Christos and Markela Sourovelis broke no law and were charged with nothing. Never imply the parents did wrong. The son's act is stated neutrally as "sold about forty dollars of heroin to a police informant" — do NOT sensationalize, do NOT depict drugs, do NOT moralize about drug policy or about the son.
> 2. **State the outcome accurately — it was a settlement, not a court striking the law down.** In 2018 the **city agreed** (federal consent agreements) to dismantle the program and to a repayment fund; a court did NOT rule civil forfeiture unconstitutional here. NEVER say "the court ruled it illegal / unconstitutional." Say "the city agreed to dismantle the machine." The Sourovelises kept their own home (the city dropped its case against their house within about a year); the class action changed the system for everyone else.
> 3. **Civil forfeiture is a real, still-existing legal tool — describe it, don't call it a crime.** Do NOT say the city "stole," "robbed," or acted "illegally." Attribute the mechanism as fact ("the property itself is the defendant," "burden can flip to the owner"); attribute any characterization of abuse to its source, not to us.
> 4. **Use the 2002-2014 aggregate figures verbatim** — 1,200+ homes, 3,500+ cars, $50M+ cash, ~$178 typical, ~$6M/yr to budgets. Do NOT invent an annual rate (e.g. "300-500 homes a year") and do NOT round up. Numbers are approximations ("more than," "about," "nearly") — keep the hedge words.
> 5. **Do NOT conflate this with any unrelated matter** (e.g. the later, separate case of former DA Seth Williams). This short is only the forfeiture program and the Sourovelis class action.
> 6. **No real-person likeness** of Christos Sourovelis, Markela Sourovelis, their son Yianni, or co-plaintiffs Doila Welch, Norys Hernandez, Nassir Geiger. Symbolic visuals only, no faces. Neutral tone: property-rights of innocent owners vs law-enforcement incentives — both stated fairly. Pre-publish legal-eye review (R2, not light).
> 7. **"The State v. one house" is illustrative of in-rem naming, not a real docket** — never render a fake case number or real caption text on screen (telops are burned in Remotion; images stay text-free).

**Suggested YouTube TITLE**: His Son Sold $40 of Drugs — So the City Tried to Take His Parents' House #Shorts

**DESCRIPTION**: In 2014 Philadelphia moved to seize a family's home over their son's roughly $40 drug sale — using civil forfeiture, where the house itself becomes the "defendant" and innocent owners must prove their own property did nothing wrong. The Sourovelis family and the Institute for Justice filed a class action, and in 2018 the city agreed to dismantle a program that between 2002 and 2014 had taken 1,200+ homes — full breakdown on the channel.

---

## §2 制作・公開手順（別スレッド Claude Code 用チェックリスト）

1. **素材**: 各 `image` を用意 — フッテージ優先（`H:\pd-media\assets\factory\` 縦クロップ、または本編 `PD-2026-028-forfeiture/05_visuals` 流用）、足りない所だけローカル（SD3.5 `sd35_gen.py` / SDXL `gen_max.ps1`）で縦生成し `H:\pd-media\assets\ai\shorts\short28\` へ。**本人肖像なし・ロゴなし・可読な実在テキストなし・公印なし・事件番号なし**。**Codex生成は不要**。
2. **ナレ**: §0の声で英語生成（承認済）。GAP≈2.70s、~50〜55s。
3. **組み立て**: `Short.tsx`（1080×1920）で時間表どおり。フッテージはそのまま／静止画は2.5D・浮遊カード。テロップは上表の英語を大きく焼き込み（下部セーフ・重い黒箱を避ける）。カットはスピーディー・無音は最大0.6秒。
4. **音**: 4層＋ダッキング＋2パス静的 -14 LUFS（`build_short_mix.py`）。中盤で痩せないこと。
5. **サムネ**: `short28_thumb.png`（<2MB）＋大文言を `ShortThumb` で。公開時は先頭0.7sカバーフレーム焼き込み（crf18）。
6. **公開**: **1日1本・12:00 JST 予約**。予約前に全 `publishAt` 監査→空き日。**R2 は法務レビュー必須**（存命の家族が実在）。最終チェック＝本人肖像なし・中立・広告安全・言い回しロック・字幕がナレに一致。
7. **命名衝突に注意**: 既存 `short01`〜`short27` と衝突させない。新規は `short28`。`Root.tsx` へ `Short-short28-yt/-tt` と `ShortThumb-short28` を登録。
8. **整合**: 本編台本（`PD-2026-028-forfeiture/03_script/script.annotated.v001.json`）更新時は VO/FACT-CHECK を取り直す。durable source content_hash は公開前に確定。
