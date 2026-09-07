# 縦型ショート 完全設計書 — 第27話 Rodriguez v. United States（別スレッド制作用・自己完結版）

本編 `PD-2026-027-rodriguez`（Rodriguez v. United States, 2015 / 米連邦最高裁 修正第4条・交通停止の「時間」）に1対1で対応する縦型ショート1本。**この設計書だけで別スレッドの Claude Code が単体で完成まで作れるよう、仕様・数値・言い回しロックをすべて本文に書ききる。** 形式は `SHORTS_EP19-24.md` と同一。EP25 Kyllo（家＝壁）・EP26 Katz（人＝壁なし）に続く3部作の最終話（時間）。

> **重要（オーナー指示 踏襲）**
> - ショートは**別スレッドの Claude Code** が制作。この設計書が唯一の指示書。
> - **Codex 画像生成は必須ではない。** 縦画像は「①`H:\pd-media\assets\factory\` の商用OK**動画フッテージ**（縦クロップ／夜道・ハイウェイ・車内・パトライト系）②本編 `PD-2026-027-rodriguez/05_visuals` 素材の流用 ③足りない所だけローカルSDXL(7860)で縦生成」で賄ってよい。各 `image` プロンプトは**SDXLで作る場合の指定**で、動く素材で代替できるものはフッテージ優先（紙芝居回避）。
> - チャンネルは**US英語**。VO・テロップ・サムネ文言は下表の英語をそのまま使う。翻訳工程なし。
> - 動きは本編と同じ新テンプレ思想（フッテージ主役＋2.5D＋モーショングラフィックス、ただの左右パン/ズーム禁止、金の縦スイープ禁止、黄色ウォッシュ禁止）。

## §0 共通仕様（`SHORTS_EP19-24.md` §0 と同一。要点を再掲）

- **画面**: 縦 9:16 / 1080×1920 / 尺 **50〜55秒** / 字幕（テロップ）常時 / モバイル前提の大きな文字。
- **本人肖像なし**（実在人物 Dennys Rodriguez・Officer Struble の顔・似顔・声真似は禁止・invariant 11）。**画像内に可読な実在テキスト/ロゴ/数字/紋章/シールを描かない**（テロップは Remotion で焼く）。
- **ナレ音声**: 本編と同じ声 `ElevenLabs VOICE_ID nPczCjzI2devNBz1zQrb / eleven_multilingual_v2 / stability0.35 / similarity0.80`。英語生成（承認済・追加確認不要）。
- **音**: 4層ミックス（BGM／緊張／環境／SFX）＋ダッキング＋**2パス静的 -14 LUFS**。中盤で痩せないよう `speechnorm+グルー圧縮`（`build_short_mix.py` の short17〜設定を踏襲）。GAP≈2.70s。
- **コンポジション**: 縦Remotion `Short.tsx`（1080×1920）。時間表どおり並べ上品に動かす。フッテージはそのまま／静止画は2.5D・浮遊カード。**カットはスピーディー**・ナレの無音は最大0.6秒。
- **画像プロンプト末尾に共通スタイルを付す**: *"museum-grade cinematic symbolic documentary still, vertical 9:16, deep-navy / black base, electric-blue signal, muted-gold accent, film grain, no faces, no readable text/logos/seals, symbolic reconstruction (not authentic footage)."*
- **サムネ**: `short27_thumb.png`（<2MB）＋大文言を `ShortThumb` で重ねて書き出し。Shorts公開時は**先頭0.7sにカバーフレーム焼き込み**（libx264 crf18）。
- **VO末尾CTA（共通）**: "Watch the full story on the channel. Follow for more."
- **保存先**: `H:\pd-media\assets\ai\shorts\short27\`（使う画像＋`short27_thumb.png`）。フッテージ流用時はそのパスを `image` 欄に併記。
- **公開ゲート**: 1日1本ちょうど・12:00 JST 予約（`publishAt`）。予約前に全 `publishAt` 監査→空き日。**R2 は法務目線レビュー必須**（下 RISK 参照）。最終チェック＝本人肖像なし・中立・広告安全・言い回しロック・字幕がナレに一致・切れ目が自然。`Root.tsx` へ `Short-short27-yt` と `ShortThumb-short27` を登録（`short01`〜`short26` と命名衝突させない）。

---

## SHORT #27 →（本編 第27話 Rodriguez v. United States, 2015）Everything the officer did was legal — the case turned entirely on how long the stop lasted.
**The one surprise**: The traffic stop was already *over* — the warning was written and the papers handed back — yet the officer held the driver seven or eight more minutes for a drug dog. The Supreme Court (6–3, Ginsburg) said those minutes were the violation: once a stop's "mission" is done, the clock stops, and prolonging it for a dog — even briefly — needs its own reasonable suspicion. It didn't ban dog sniffs and it didn't set Rodriguez free.

| time | VO (English) | telop (English, short) | image |
|---|---|---|---|
|0:00-0:04|The traffic stop was already over — the ticket written, the papers handed back. So how did the next seven minutes break the Constitution?|THE STOP WAS OVER / SO WHY 7 MINUTES?|01|
|0:04-0:16|Just after midnight in Nebraska, a K-9 officer pulled over Dennys Rodriguez for drifting onto the shoulder. He ran the checks, wrote a warning, handed everything back. By any ordinary sense, the stop's job — its "mission" — was done.|MIDNIGHT, NEBRASKA / WARNING WRITTEN — DONE|02,03|
|0:16-0:34|But the officer never said "you're free to go." He held Rodriguez seven to eight more minutes, waited for a second unit, then walked a drug dog around the car. The dog alerted. What the search found came in the stretch of time after the stop was finished, not before.|HELD FOR A DOG / AFTER THE JOB WAS DONE|04,05|
|0:34-0:48|In 2015 the Supreme Court drew the line, six to three. A stop, Justice Ginsburg wrote, becomes unlawful when it is "prolonged beyond the time reasonably required to complete the mission." Once the traffic work is done, the clock stops — holding you for a dog needs its own reason. It didn't ban dog sniffs, and it didn't free him — it sent the case back.|6–3 · 2015 / THE CLOCK STOPS|06,07|
|0:48-0:55|Watch the full story on the channel. Follow for more.|WATCH THE FULL STORY / FOLLOW FOR MORE|07(hold)|

- `short27_01.png` A lone car pulled onto the shoulder of an empty two-lane highway just after midnight, cold headlight cones on wet asphalt, restrained red-and-blue patrol light reflected low on the road (never a full wash), no plates, no faces, generous negative space for text (**footage alt**: `factory` night-highway / roadside patrol-light clip, vertical crop)
- `short27_02.png` A working police-dog silhouette resting alert in the back seat of a patrol car, cold blue cast through the glass, procedural and neutral, no handler face, no badge or logo
- `short27_03.png` Anonymous hands passing a single folded blank paper slip between them through a dark car window, faint dashboard glow — the written warning, its business finished — no readable text on the paper
- `short27_04.png` An analog stopwatch hovering over an empty gravel roadside shoulder at night, sweeping second hand caught in electric-blue light, the dead time of waiting, no legible numerals, tense stillness (**footage alt**: `factory` clock / ticking-mechanism macro, vertical crop)
- `short27_05.png` A leashed police-dog silhouette circling a stopped car in cold headlight beams on a dark road, restrained blue light on the paint, procedural — never attacking — no faces, no plates, no logos
- `short27_06.png` A symbolic hourglass in deep-navy low key, the sand rendered as electric-blue light running low, a single muted-gold rim — the constitutional limit measured in time, not sequence — no text baked in
- `short27_07.png` A thin electric-blue line drawn cleanly across dark asphalt with a car's taillights just past it — "how long is too long," the moment a lawful stop becomes an unlawful seizure — minimalist premium composition, wide negative space for the CTA endcard
- **thumbnail** `short27_thumb.png` An empty night highway on the shoulder with restrained red-and-blue light low on wet asphalt and a stopwatch overlaid in electric-blue ／ headline (<=2 lines): **"THE STOP WAS OVER"** / **"7 MINUTES TOO LONG"** ／ badge: "6–3 · 2015"

> **FACT-CHECK** — everything the officer did was legal; case turned on added time, not the sniff itself=CLM-0004 + CLM-0001; just after midnight Mar 27 2012, Nebraska, K-9 officer Struble stopped Dennys Rodriguez (Mercury Mountaineer) for veering onto the shoulder=CLM-0005; checks + **written warning** + documents returned = mission complete=CLM-0006 + CLM-0003; **~7–8 min** post-warning detention, second officer, dog **alerted**, search found methamphetamine, **~29 min** total=CLM-0007; dog sniff not part of the mission / what matters is whether it **adds time**, not order before/after ticket=CLM-0004; Court rejected the Government's **"de minimis"** argument / officer cannot bank saved time=CLM-0008; 2015, **6–3**, majority by **Justice Ginsburg**=CLM-0002; quote **"prolonged beyond the time reasonably required to complete the mission"** (opinion quoting *Illinois v. Caballes*, 2005)=CLM-0011; did **not** ban sniffs, did **not** free Rodriguez — **vacated and remanded** on reasonable suspicion=CLM-0009; dissent Thomas (joined Alito; Kennedy exc. Part III) + Alito + Kennedy=CLM-0010; leading authority on how long a stop may last=CLM-0012.
> **RISK (R2 — decided Supreme Court case; real people on the public record)** — LOCKS: **The holding is a DECIDED case and is stateable as fact** (6–3, decided **April 21, 2015**, Ginsburg majority — never "unanimous," never "5–4"). **NEVER "the Court banned dog sniffs," "banned traffic stops," or "police can never hold you after a ticket."** The Court **did NOT free Rodriguez** — it **vacated and remanded** on the reasonable-suspicion question; never "Rodriguez went free / was acquitted." The rule is: prolonging past the mission **without independent reasonable suspicion** is unlawful — **reasonable suspicion could still justify the extension**; never a flat "any delay is unconstitutional." It was a **WRITTEN WARNING**, not a ticket or arrest; the stop was for the **shoulder veer**, never "speeding" or "for drugs." Keep **~7–8 min post-warning** and **~29 min total**. Treat the methamphetamine only as **"what the search found," never depicted as drugs**; the dog is **procedural, never attacking**. Use `"prolonged beyond the time reasonably required to complete the mission"` as an **attributed quotation** (from *Caballes*), not paraphrase presented as Rodriguez's own words. **No real-person likeness** of Rodriguez or Officer Struble; no plates, no readable text/logos/seals. Pre-publish legal review.

- **YouTube TITLE**: `The Traffic Stop Was Already Over — So How Was It Unconstitutional? #Shorts`
- **DESCRIPTION**: In 2015, the Supreme Court ruled in Rodriguez v. United States that once a traffic stop's job is done, the clock stops — and holding a driver even a few extra minutes for a drug dog needs its own reason. Watch the full story on the channel.

---

## §1 制作・公開手順（別スレッド Claude Code 用チェックリスト）

1. **素材**: 各 `image` を用意 — フッテージ優先（`H:\pd-media\assets\factory\` の夜道/パトライト/時計マクロを縦クロップ、または本編 `PD-2026-027-rodriguez/05_visuals` 流用）、足りない所だけ SDXL(7860) で縦生成し `H:\pd-media\assets\ai\shorts\short27\` へ。**本人肖像なし・ロゴ/シールなし・可読な実在テキストなし**。Codex生成は不要。
2. **ナレ**: §0の声で英語生成（承認済）。GAP≈2.70s、50〜55s。
3. **組み立て**: `Short.tsx`（1080×1920）で時間表どおり。フッテージはそのまま／静止画は2.5D・浮遊カード。テロップは上表の英語を大きく焼き込み（下部セーフ・重い黒箱を避ける）。カットはスピーディー・無音は最大0.6秒。
4. **音**: 4層＋ダッキング＋2パス静的 -14 LUFS（`build_short_mix.py`）。中盤で痩せないこと。
5. **サムネ**: `short27_thumb.png`（<2MB）＋大文言を `ShortThumb` で。公開時は先頭0.7sカバーフレーム焼き込み（crf18）。
6. **公開**: 1日1本・12:00 JST 予約。予約前に全 `publishAt` 監査→空き日。**R2 は法務レビュー必須**。最終チェック＝本人肖像なし・中立・広告安全・言い回しロック・字幕がナレに一致・切れ目が自然。
7. **整合**: 本編台本（`PD-2026-027-rodriguez/03_script/`）更新時は VO/FACT-CHECK を取り直す。durable source content_hash は公開前に確定。
