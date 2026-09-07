# 縦型ショート 完全設計書 — 第26話 Katz v. United States（別スレッド制作用・自己完結版）

第26話「Katz v. United States (1967)」に1対1で対応する縦型ショート1本。**この設計書だけで別スレッドの Claude Code が単体で完成まで作れるよう、仕様・数値・言い回しロックをすべて本文に書ききる。** 元の話スレッドや口頭指示に依存しない。フォーマットは `SHORTS_EP19-24.md` と同一。

> **重要（オーナー指示・EP19-24と同じ）**
> - ショートは**別スレッドの Claude Code** が制作する。この設計書が唯一の指示書。
> - **Codex 画像生成は必須ではない。** 縦画像は「①`H:\pd-media\assets\factory\` の商用OK**動画フッテージ**（縦クロップ）②既存エピソード素材（`PD-2026-026-katz/05_visuals`）の流用 ③必要な所だけローカルSDXL(7860)で縦生成」で賄ってよい。下の各 `image` プロンプトは**SDXLで作る場合の指定**。動く素材＝紙芝居回避のためフッテージ優先。
> - チャンネルは**US英語**。VO・テロップ・サムネ文言は下表の英語をそのまま使う。翻訳工程なし。
> - 動きの基準は本編と同じ新テンプレ思想（フッテージ主役＋2.5D＋モーショングラフィックス、ただの左右パン/ズーム禁止、金の縦スイープ禁止、黄色ウォッシュ禁止）。

## §0 共通仕様（`SHORTS_EP19-24.md` §0 と同一。ここに要点を再掲）

- **画面**: 縦 9:16 / 1080×1920 / 尺 **約50〜55秒** / 字幕（テロップ）常時 / モバイル前提の大きな文字。
- **本人肖像なし**（実在人物の顔・似顔・声真似は禁止・invariant 11）。Charles Katz・各判事の顔/似顔を描かない。**画像内に可読な実在テキスト/ロゴ/印章/数字を描かない**（テロップは Remotion で焼く）。
- **ナレ音声**: 本編と同じ声 `ElevenLabs VOICE_ID nPczCjzI2devNBz1zQrb / eleven_multilingual_v2 / stability0.35 / similarity0.80`。英語生成（承認済・追加確認不要）。
- **音**: 4層ミックス（BGM／緊張／環境／SFX）＋ダッキング＋**2パス静的 -14 LUFS**。中盤で音量が痩せないよう `speechnorm+グルー圧縮`（`build_short_mix.py` の short17〜設定を踏襲）。GAP≈2.70s。
- **コンポジション**: 縦Remotion `Short.tsx`（1080×1920）。時間表どおり並べ、**上品に動かす**（フッテージはそのまま／静止画は2.5D・浮遊カード）。**カットは結構スピーディー**・ナレの無音は最大0.6秒。
- **サムネ**: `short26_thumb.png`（<2MB）＋大文言を `ShortThumb` で重ねて書き出し。Shorts公開時は**先頭0.7sにカバーフレーム焼き込み**（libx264 crf18）。
- **VO末尾CTA（共通）**: "Watch the full story on the channel. Follow for more."
- **画像プロンプト末尾に共通スタイルを付す**: *"museum-grade cinematic symbolic documentary still, vertical 9:16, deep-navy / black base, electric-blue signal, silver highlights, restrained muted-gold accent, film grain, no faces, no readable text / logos / seals, symbolic reconstruction (not authentic footage)."*
- **保存先**: `H:\pd-media\assets\ai\shorts\short26\`（使う画像＋`short26_thumb.png`）。フッテージ流用時はそのパスを `image` 欄に併記。

## §1 公開ゲート（本編と共通）

- **1日1本ちょうど・12:00 JST 予約**（`publishAt`）。新規予約前に全 `publishAt` を監査し空き日へ。衝突は `--replace` で日付修正。
- オーナーが一度OK。**R2 は法務目線レビュー必須**（下の RISK 参照）。
- 最終チェック: 本人肖像なし・中立・広告安全・**言い回しロック**・字幕がナレに一致・切れ目が自然。
- 本編台本（`PD-2026-026-katz/03_script/script.en.v001.md`）が更新されたら VO/FACT-CHECK を取り直す。

---

## SHORT #26 →（本編 第26話 Katz v. United States, 1967）The FBI recorded a man in a phone booth without ever touching it — and the Supreme Court still called it an illegal search.
**The one surprise**: The agents never opened the door, never stepped inside, never laid a finger on him — no trespass at all — yet in 1967 the Supreme Court ruled it an illegal search, retiring a 40-year-old rule and declaring that the Fourth Amendment "protects people, not places."

| beat | time | VO (English) | telop (English, UPPERCASE, 2 lines) | image |
|---|---|---|---|---|
|L1 (hook, intense)|0:00-0:06|The FBI recorded every word he said — and never once opened the door. The Supreme Court still called it an illegal search.|NEVER OPENED<br>THE DOOR|01,02|
|L2 (building)|0:06-0:19|Los Angeles, 1965. Charles Katz stepped into a glass phone booth to place illegal betting calls. To catch him, agents taped a hidden microphone to the outside of the glass — and never set foot inside.|A MIC ON<br>THE OUTSIDE|02,03|
|L3 (building)|0:19-0:34|For nearly forty years, the rule was simple: no physical trespass, no search. By that logic, the agents had broken no rule. But Katz had shut the door and paid the toll — to keep his words private, not his face.|NO TRESPASS —<br>NO SEARCH?|04,05|
|L4 (climax)|0:34-0:50|December 18th, 1967 — seven to one. "The Fourth Amendment protects people, not places." Recording him without a warrant was unconstitutional — the fix was never a ban on wiretaps, just a judge's permission first. And Justice Harlan's concurrence gave the two-part "reasonable expectation of privacy" test that still governs surveillance today.|PEOPLE,<br>NOT PLACES|06,07|
|L5 (CTA, calm)|0:50-0:55|Watch the full story on the channel. Follow for more.|WATCH THE<br>FULL STORY|07(hold)|

- `short26_01.png` A lone 1960s glass telephone booth glowing warm on a rain-slick empty night street, an anonymous silhouette inside seen through misted glass, deep-navy void around it, one shaft of muted-gold light, no readable signage, no face (**footage alt**: `factory` night-street / neon-reflection clip, vertical crop)
- `short26_02.png` An extreme macro of a small hidden microphone and thin wire taped to the metal top edge on the OUTSIDE of a glass booth, cold electric-blue rim light, clandestine surveillance detail, no text, no logos
- `short26_03.png` A vintage reel-to-reel recorder turning slowly in shadow with one faint red record glow and headphones nearby, surveillance noir, electric blue on black, no faces, no text (**footage alt**: `factory` tape-reel / analog-recorder clip, vertical crop)
- `short26_04.png` A heavy old wooden door and a brass keyhole in deep shadow — the outdated idea that privacy needs a physical wall to breach — cold navy with a single muted-gold light, no readable text
- `short26_05.png` An anonymous silhouette pulling a booth door shut and dropping a coin, a warm interior glow sealing the space, while a cold electric-blue sound-wave leaks out through the glass — intimacy versus intrusion, faceless, no readable dial or numbers
- `short26_06.png` A minimalist balance scale in low key: a small model house on one pan sinking, a small warm human figure of light on the other rising to prominence — "people, not places" — symbolic, no faces, no baked-in text, no seals
- `short26_07.png` A modern smartphone glowing on a dark table with faint electric-blue data-streams and signal arcs rising into the night — the "phone booth" of today, ambient surveillance — no readable screen, no icons, no faces, no logos, generous negative space for the CTA endcard
- **thumbnail** `short26_thumb.png` A lone glowing glass phone booth on a dark wet street with a cold electric-blue sound-wave leaking through the glass and a faint muted-gold aura around the unseen person inside ／ headline: **"NEVER TOUCHED / STILL A SEARCH"** ／ badge: "1967"

> **FACT-CHECK** — 1965 LA, FBI taped a listening/recording device to the OUTSIDE of a public glass phone booth Katz used for interstate wagering calls, agents never entered=CLM-0005; recording his words without any physical entry was ruled a Fourth Amendment "search"=CLM-0001; the ~40-year physical-trespass rule (Olmstead) = "no trespass, no search," later set aside=CLM-0007; a man who shuts the booth door and pays the toll is entitled to assume his words are not broadcast to the world=CLM-0006; Dec 18 1967 / **7-1** / Stewart wrote the opinion / Black lone dissenter=CLM-0002; "the Fourth Amendment protects people, not places" (exact majority quote)=CLM-0003; what you knowingly expose to the public is unprotected, what you seek to keep private can be protected even in a public place=CLM-0004; unconstitutional **because no warrant** — agents had probable cause but never got prior judicial authorization; **not a ban on wiretapping**=CLM-0008; the two-part "reasonable expectation of privacy" test = **Justice Harlan's CONCURRENCE**, not the majority holding=CLM-0009; Harlan's formulation was later adopted as the standard test and still governs modern surveillance=CLM-0011.

> **RISK (R2 — decided historical SCOTUS case; real person by role; illegal gambling)** — LOCKS:
> 1. **The holding is stateable as fact** (7-1, 1967, a "search" under the Fourth Amendment). Do **NOT** say "unanimous" or "5-4"; the vote was **7-1**, Black dissenting alone (Marshall took no part).
> 2. **NEVER "the Court banned wiretapping"** or "the police can never record a suspect." Katz **required a warrant / prior judicial authorization** — surveillance like this is lawful **with** a warrant. Frame the fault as **"no warrant," not "surveillance itself."**
> 3. **"Reasonable expectation of privacy" (two-part test) = HARLAN'S CONCURRENCE**, never the majority holding. Never say "the majority created the reasonable-expectation test."
> 4. **"protects people, not places"** is an exact public-domain quote from Justice Stewart's majority — OK verbatim.
> 5. The device was on the **OUTSIDE**; agents **never entered**. Never say they "broke into," "drilled," or "entered" the booth.
> 6. **Gambling is only the factual reason** for the surveillance — never glamorized, never depicted as action; the legal question, not the bets, is the subject.
> 7. **No real-person likeness** of Charles Katz or any justice; symbolic, faceless visuals only. Pre-publish legal-eye review.

### YouTube metadata

- **TITLE**: `How Did the FBI Record Him Without Ever Touching the Phone Booth? #Shorts`
- **DESCRIPTION**: In 1967, the Supreme Court ruled that secretly recording a man in a glass phone booth — without ever opening the door — was an illegal search, declaring the Fourth Amendment "protects people, not places." It didn't ban wiretaps; it demanded a warrant. Watch the full story on the channel.

---

## §2 制作・公開手順（別スレッド Claude Code 用チェックリスト）

1. **素材**: 各 `image` を用意 — フッテージ優先（`H:\pd-media\assets\factory\` 縦クロップ、または本編 `PD-2026-026-katz/05_visuals` 流用）、足りない所だけ SDXL(7860) で縦生成し `H:\pd-media\assets\ai\shorts\short26\` へ。**本人肖像なし・ロゴなし・可読な実在テキストなし・印章なし**。**Codex生成は不要**。
2. **ナレ**: §0の声で英語生成（承認済）。GAP≈2.70s、50〜55s。
3. **組み立て**: `Short.tsx`（1080×1920）で時間表どおり。フッテージはそのまま／静止画は2.5D・浮遊カード。テロップは上表の英語を大きく焼き込み（下部セーフ・重い黒箱を避ける）。カットはスピーディー・無音は最大0.6秒。
4. **音**: 4層＋ダッキング＋2パス静的 -14 LUFS（`build_short_mix.py`）。中盤で痩せないこと。
5. **サムネ**: `short26_thumb.png`（<2MB）＋大文言を `ShortThumb` で。公開時は先頭0.7sカバーフレーム焼き込み（crf18）。
6. **公開**: **1日1本・12:00 JST 予約**。予約前に全 `publishAt` 監査→空き日。**R2 は法務レビュー必須**。最終チェック＝本人肖像なし・中立・広告安全・言い回しロック・字幕がナレに一致。
7. **命名衝突に注意**: 既存 `short01`〜`short24` と衝突させない。新規は `short26`。`Root.tsx` へ `Short-short26-yt/-tt` と `ShortThumb-short26` を登録。
8. **整合**: 本編台本（`PD-2026-026-katz/03_script/`）更新時は VO/FACT-CHECK を取り直す。durable source content_hash は公開前に確定。
