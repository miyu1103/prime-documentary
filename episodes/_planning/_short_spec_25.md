# 縦型ショート 完全設計書 — 第25話（Kyllo v. United States）別スレッド制作用・自己完結版

第25話（本編 `PD-2026-025-kyllo`）に1対1で対応する縦型ショート1本。**この設計書だけで別スレッドの Claude Code が単体で完成まで作れるよう、仕様・数値・言い回しロックをすべて本文に書ききる。** 書式・数値・ロックの基準は `SHORTS_EP19-24.md`（§0 共通仕様・per-SHORT 表・画像プロンプト・FACT-CHECK・RISK）に完全準拠する。

> **重要（オーナー指示・EP19-24 と同一）**
> - ショートは**別スレッドの Claude Code** が制作する。この設計書が唯一の指示書。
> - **Codex 画像生成は必須ではない。** 縦画像は「①`H:\pd-media\assets\factory\` の商用OK**動画フッテージ**（縦クロップ）②本編 `PD-2026-025-kyllo/05_visuals` の流用 ③必要な所だけローカルSDXL(7860)で縦生成」で賄ってよい。下の各 `image` プロンプトは**SDXLで作る場合の指定**。動く素材でまかなえるものはフッテージ優先（紙芝居回避）。
> - チャンネルは**US英語**。VO・テロップ・サムネ文言は下表の英語をそのまま使う。翻訳工程なし。
> - 動きの基準は本編と同じ新テンプレ思想（フッテージ主役＋2.5D＋モーショングラフィックス、ただの左右パン/ズーム禁止、金の縦スイープ禁止、黄色ウォッシュ禁止）。

## §0 共通仕様（`SHORTS_EP19-24.md` §0 と同一。要点を再掲）

- **画面**: 縦 9:16 / 1080×1920 / **尺 ~50〜55秒**（本話は5 VOビートで ~55s）/ 字幕（テロップ）常時 / モバイル前提の大きな文字。
- **本人肖像なし**（実在人物 Danny Kyllo / William Elliott / Antonin Scalia / John Paul Stevens の顔・似顔・声真似は禁止・invariant 11）。**画像内に可読な実在テキスト/ロゴ/公印/紋章を描かない**（テロップは Remotion で焼く）。
- **ナレ音声**: 本編と同じ声 `ElevenLabs VOICE_ID nPczCjzI2devNBz1zQrb / eleven_multilingual_v2 / stability0.35 / similarity0.80`。英語生成（承認済・追加確認不要）。
- **音**: 4層ミックス（BGM／緊張／環境／SFX）＋ダッキング＋**2パス静的 -14 LUFS**。中盤で音量が痩せないよう `speechnorm+グルー圧縮`（`build_short_mix.py` の short17〜設定を踏襲）。GAP≈2.70s。
- **コンポジション**: 縦Remotion `Short.tsx`（1080×1920）。時間表どおり並べ、上品に動かす。カットはスピーディー・ナレの無音は最大0.6秒。
- **サムネ**: `short25_thumb.png`（<2MB）＋大文言を `ShortThumb` で重ねて書き出し。Shorts公開時は**先頭0.7sにカバーフレーム焼き込み**（libx264 crf18）。
- **VO末尾CTA（共通）**: "Watch the full story on the channel. Follow for more."
- **画像プロンプト末尾に共通スタイルを付す**: *"museum-grade cinematic symbolic documentary still, vertical 9:16, deep-navy / black base, electric-blue signal, restrained muted-gold accent, film grain, no faces, no readable text / logos / seals, symbolic reconstruction (not authentic footage)."*
- **保存先**: `H:\pd-media\assets\ai\shorts\short25\`（使う画像＋`short25_thumb.png`）。フッテージ流用時はそのパスを `image` 欄に併記。

## §1 公開ゲート

- **1日1本ちょうど・12:00 JST 予約**（`publishAt`）。新規予約前に全 `publishAt` を監査し空き日へ。衝突は `--replace` で日付修正。
- オーナーが一度OK。**R2 は法務目線レビュー必須**（下の RISK 参照）。
- 最終チェック: 本人肖像なし・中立・広告安全・**言い回しロック**・字幕がナレに一致・切れ目が自然。
- 本編台本（`PD-2026-025-kyllo/03_script/script.en.v001.md`）が更新されたら VO/FACT-CHECK を取り直す。

---

## SHORT #25 →（本編 第25話 Kyllo v. United States）A federal agent scanned a man's home from a public street without ever touching it — and the Supreme Court still called it a "search."
**The one surprise**: The agent never knocked, never crossed the lawn, and never went through the wall — he only read heat that had already leaked into the open air — yet in 2001 the Supreme Court held, 5-4, that pointing a thermal-imaging device at a home is a Fourth Amendment "search" that needs a warrant, drawing a "firm but bright" line at the front door.

| time | VO (English) | telop (English, short) | image |
|---|---|---|---|
|0:00-0:03|He never knocked. He never crossed the lawn. The Supreme Court still called it a search of the home.|NEVER<br>ENTERED|01|
|0:03-0:16|On a freezing night in January 1992, a federal agent sat in a car on a public street in Florence, Oregon. He pointed a thermal-imaging device at Danny Kyllo's home and read the heat leaking off the walls.|THERMAL<br>SCAN|02,03|
|0:16-0:33|The garage roof and one wall glowed hot — to the agent, the signature of powerful indoor grow lamps. That reading helped win a warrant, and inside were more than a hundred marijuana plants. But the device never saw through the wall. It only measured heat already drifting into the open air.|HEAT<br>LEAKS OUT|04,05|
|0:33-0:50|On June 11, 2001, the Court split five to four. Justice Scalia wrote that using a device not in general public use to learn what is inside a home is a search — one that needs a warrant. The dissent called it merely reading heat off the outside. But the majority drew a line at the front door it called firm, and bright.|FIRM<br>BRIGHT LINE|06|
|0:50-0:55|Watch the full story on the channel. Follow for more.|WATCH THE<br>FULL STORY|07(hold)|

- `short25_01.png` A dark suburban home at night rendered as a restrained thermal bloom, cold navy walls with one concentrated white-hot core glowing through the roof, no rainbow, no faces, no readable text — *[common style suffix]* (**footage alt**: `factory` night-suburb or thermal-shimmer clip, vertical crop)
- `short25_02.png` A quiet POV from inside a parked car across an empty pre-dawn street toward a modest triplex silhouette, breath-fog on cold glass, electric-blue night, no faces, no signage — *[common style suffix]*
- `short25_03.png` An anonymous handheld sensing device raised in gloved hands toward a distant home, a faint electric-blue scan-line reaching across the dark street, no logos, no readable screen, no face — *[common style suffix]*
- `short25_04.png` An extreme macro of a garage-eave seam leaking intense warm gold light and heat-shimmer into freezing navy night air, heat-as-information motif, no plants, no drugs, no text — *[common style suffix]* (**footage alt**: `factory` heat-haze / vent-steam clip, vertical crop)
- `short25_05.png` A cold navy exterior wall with a hot-white human-scale glow pressing through it from inside, heat escaping a solid barrier, faceless silhouette of warmth only, no readable text — *[common style suffix]*
- `short25_06.png` A closed front door at the threshold of a home with a single firm, bright electric-blue line drawn sharply across the entrance, cold navy around it, iconic and severe, no seals, no text — *[common style suffix]*
- `short25_07.png` An ordinary home at night ringed by faint modern sensing — a tiny distant drone silhouette, a soft doorbell-camera glow, subtle thermal shimmer — the moving line of the future, no logos, no faces, no text, generous negative space for the CTA endcard — *[common style suffix]*
- **thumbnail** `short25_thumb.png` A dark home glowing as a restrained thermal bloom with one firm bright line drawn across the front door ／ headline: **"NEVER WENT IN"** ／ badge: "5–4"

> **FACT-CHECK** — agent on a public street / no trespass / raised a device and read wall heat=SPN-0001/SPN-0007/SPN-0010 (CLM-0005 + CLM-0009); Jan 16 1992, ~3 a.m., Florence, Oregon triplex, Danny Kyllo, agent William Elliott, thermal imager (Agema Thermovision 210)=SPN-0003/SPN-0005 (CLM-0005 + CLM-0006); thermal imager measures escaping heat, does **not** see through walls=SPN-0005 (CLM-0008); garage roof + one wall hotter → agent read it as grow lamps=SPN-0006 (CLM-0006); scan + informant tip + high power bills → warrant; inside, 100+ marijuana plants=SPN-0008 (CLM-0007); June 11 2001, 5-4, Scalia majority=SPN-0014 (CLM-0002); holding = device "not in general public use" revealing the home's interior that couldn't be known without entering is a search, presumptively unreasonable without a warrant=SPN-0016 (CLM-0001); "firm but bright" line at the entrance of the house=SPN-0015 (CLM-0003); Stevens dissent = "off-the-wall" heat, not "through-the-wall" surveillance=SPN-0018 (CLM-0002 + CLM-0009).

> **RISK (R2 — decided Supreme Court case, low risk)** — LOCKS:
> 1. **The holding is stateable as fact** (a decided case): "the Supreme Court held it was a search that needs a warrant." Do NOT hedge it as opinion.
> 2. **The Court did NOT ban thermal imaging.** NEVER say "banned," "outlawed," or "made thermal cameras illegal." The rule is **"get a warrant first."**
> 3. **Frame the split as fact**: "the Court split 5-4" / "the dissent argued…". Attribute the dissent view to Stevens (or "the dissent"), never assert it as the law. Attribute the majority rule to the Court/Scalia.
> 4. **Quote the line accurately**: the entrance line must be "firm" and "bright" (Scalia: "not only firm but also bright"). Telop "FIRM / BRIGHT LINE" is fine; do not invent other quoted wording.
> 5. **The grow-op is only ever heat/light and the found plants** — state "more than a hundred marijuana plants" as what agents found (CLM-0007); do NOT depict drugs, do NOT editorialize on marijuana policy.
> 6. **No real-person likeness** of Kyllo, Elliott, Scalia, or Stevens. Symbolic visuals only, no faces. Neutral tone: privacy-of-the-home vs law-enforcement need, both fair. No editorializing beyond the ruling.
> 7. **"not in general public use"** is the Court's phrase — keep it verbatim, do not paraphrase into "rare device" in a way that changes the legal test. Pre-publish legal-eye review (light, R2).

**Suggested YouTube TITLE**: He Never Set Foot on the Property — So Why Did the Supreme Court Call It a "Search"? #Shorts

**DESCRIPTION**: In 1992 a federal agent scanned a home's heat from a public street without ever touching it. In Kyllo v. United States (2001) the Supreme Court split 5-4 and drew a "firm but bright" line at your front door — full breakdown on the channel.

---

## §2 制作・公開手順（別スレッド Claude Code 用チェックリスト）

1. **素材**: 各 `image` を用意 — フッテージ優先（`H:\pd-media\assets\factory\` 縦クロップ、または本編 `PD-2026-025-kyllo/05_visuals` 流用）、足りない所だけ SDXL(7860) で縦生成し `H:\pd-media\assets\ai\shorts\short25\` へ。**本人肖像なし・ロゴなし・可読な実在テキストなし・公印なし**。**Codex生成は不要**。
2. **ナレ**: §0の声で英語生成（承認済）。GAP≈2.70s、~50〜55s。
3. **組み立て**: `Short.tsx`（1080×1920）で時間表どおり。フッテージはそのまま／静止画は2.5D・浮遊カード。テロップは上表の英語を大きく焼き込み（下部セーフ・重い黒箱を避ける）。カットはスピーディー・無音は最大0.6秒。
4. **音**: 4層＋ダッキング＋2パス静的 -14 LUFS（`build_short_mix.py`）。中盤で痩せないこと。
5. **サムネ**: `short25_thumb.png`（<2MB）＋大文言を `ShortThumb` で。公開時は先頭0.7sカバーフレーム焼き込み（crf18）。
6. **公開**: **1日1本・12:00 JST 予約**。予約前に全 `publishAt` 監査→空き日。**R2 は法務レビュー**。最終チェック＝本人肖像なし・中立・広告安全・言い回しロック・字幕がナレに一致。
7. **命名衝突に注意**: 既存 `short01`〜`short24` と衝突させない。新規は `short25`。`Root.tsx` へ `Short-short25-yt/-tt` と `ShortThumb-short25` を登録。
8. **整合**: 本編台本（`PD-2026-025-kyllo/03_script/`）更新時は VO/FACT-CHECK を取り直す。durable source content_hash は公開前に確定。
