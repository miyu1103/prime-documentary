# 縦型ショート 完全設計書 — 第31話（Can They Force Your Phone Open? / 強制ロック解除・第4/第5修正）別スレッド制作用・自己完結版

第31話（本編 `PD-2026-031-unlock`）に1対1で対応する縦型ショート1本。**この設計書だけで別スレッドの Claude Code が単体で完成まで作れるよう、仕様・数値・言い回しロックをすべて本文に書ききる。** 書式・数値・ロックの基準は `_short_spec_25.md`（§0 共通仕様・per-SHORT 表・画像プロンプト・FACT-CHECK・RISK）に完全準拠する。

> **重要（オーナー指示・EP25/EP19-24 と同一）**
> - ショートは**別スレッドの Claude Code** が制作する。この設計書が唯一の指示書。
> - **Codex 画像生成は必須ではない。** 縦画像は「①`H:\pd-media\assets\factory\` の商用OK**動画フッテージ**（縦クロップ）②本編 `PD-2026-031-unlock/05_visuals`（または `remotion/src/data/unlock_film.json` が参照する `unlock/img/*` と `unlock/factory/*`）の流用 ③必要な所だけローカル（第一選択=SD3.5 `sd35_gen.py`／フォールバック=SDXL `gen_max.ps1`・素のSDXL/FLUX-dev不可）で縦生成」で賄ってよい。下の各 `image` プロンプトは**ローカル/Codexで作る場合の指定**。動く素材でまかなえるものはフッテージ優先（紙芝居回避）。
> - チャンネルは**US英語**。VO・テロップ・サムネ文言は下表の英語をそのまま使う。翻訳工程なし。
> - 動きの基準は本編と同じ新テンプレ思想（フッテージ主役＋2.5D＋モーショングラフィックス、ただの左右パン/ズーム禁止、金の縦スイープ禁止、黄色ウォッシュ禁止）。

## §0 共通仕様（`_short_spec_25.md` §0 と同一。要点を再掲）

- **画面**: 縦 9:16 / 1080×1920 / **尺 ~50〜55秒**（本話は5 VOビートで ~55s）/ 字幕（テロップ）常時 / モバイル前提の大きな文字。
- **本人肖像なし**（実在人物 Jeremy Travis Payne / 該当 Brown 被告 / Chief Justice John Roberts ら判事の顔・似顔・声真似は禁止・invariant 11）。**画像内に可読な実在テキスト/ロゴ/ブランドマーク/公印/紋章を描かない**（Apple ロゴ・林檎マーク・iPhone/Face ID の商標表示・州章・裁判所印・法典タイトルはすべて禁止。テロップは Remotion で焼く）。
- **ナレ音声**: 本編と同じ声 `ElevenLabs VOICE_ID nPczCjzI2devNBz1zQrb / eleven_multilingual_v2 / stability0.35 / similarity0.80`。英語生成（承認済・追加確認不要）。
- **音**: 4層ミックス（BGM／緊張／環境／SFX）＋ダッキング＋**2パス静的 -14 LUFS**。中盤で音量が痩せないよう `speechnorm+グルー圧縮`（`build_short_mix.py` の short17〜設定を踏襲）。GAP≈2.70s。
- **コンポジション**: 縦Remotion `Short.tsx`（1080×1920）。時間表どおり並べ、上品に動かす。カットはスピーディー・ナレの無音は最大0.6秒。
- **サムネ**: `short31_thumb.png`（<2MB）＋大文言を `ShortThumb` で重ねて書き出し。Shorts公開時は**先頭0.7sにカバーフレーム焼き込み**（libx264 crf18）。
- **VO末尾CTA（共通）**: "Watch the full story on the channel. Follow for more."
- **画像プロンプト末尾に共通スタイルを付す**: *"museum-grade cinematic symbolic documentary still, vertical 9:16, deep-navy / black base, electric-blue signal, restrained muted-gold accent, film grain, no faces, no readable text / logos / seals, symbolic reconstruction (not authentic footage)."*
- **保存先**: `H:\pd-media\assets\ai\shorts\short31\`（使う画像＋`short31_thumb.png`）。フッテージ流用時はそのパスを `image` 欄に併記。

## §1 公開ゲート

- **1日1本ちょうど・12:00 JST 予約**（`publishAt`）。新規予約前に全 `publishAt` を監査し空き日へ。衝突は `--replace` で日付修正。
- オーナーが一度OK。**R2 は法務目線レビュー必須**（下の RISK 参照）。
- 最終チェック: 本人肖像なし・中立・広告安全・**言い回しロック**・字幕がナレに一致・切れ目が自然。
- 本編台本（`PD-2026-031-unlock/03_script/script.en.v002.md`）と `fact_recheck.v001` が更新されたら VO/FACT-CHECK を取り直す。

---

## SHORT #31 →（本編 第31話 Compelled Phone Unlock）An officer can press your own thumb to your phone and open it — but the passcode you keep only in your head may be the one lock the government cannot force, and American courts flatly disagree about it.
**The one surprise**: The convenience is the vulnerability. The Face ID and fingerprint you set up because they were fast may be the *weakest* locks in a courtroom — because pressing a thumb or showing a face asks nothing of your mind, while a memorized passcode is "testimony" many courts say you can refuse. The same forced thumbprint was ruled lawful by one federal court (9th Cir., 2024) and unconstitutional by another (D.C. Cir., 2025); states split on passcodes; and the Supreme Court has turned the question away every time — so your right can change at a state line.

| time | VO (English) | telop (English, short) | image |
|---|---|---|---|
|0:00-0:03|An officer at your window wants your phone open. He can take your face. He can take your thumb. Your mind may be the last lock he can't force.|UNLOCK<br>IT|01|
|0:03-0:16|Your phone isn't a phone — it's your whole life. In 2014, in Riley versus California, the Supreme Court said police generally need a warrant to search it. But a warrant is worthless if they can't get in. So the real fight isn't searching — it's whether they can force *you* to open it.|GET A<br>WARRANT|02,03|
|0:16-0:33|That question jumps to the Fifth Amendment, which shields what's testimonial — the contents of your mind. A passcode is a combination you keep in your head, so many courts say it may be protected. But your face and your thumb are on your body — no thought required — and the law often treats them like a fingerprint at booking.|MIND<br>VS BODY|04,05|
|0:33-0:50|So in 2024 one federal court let officers press a man's own thumb to unlock. A year later another federal court called almost the same act unconstitutional. States split on passcodes too — and the Supreme Court has refused to settle it. Your right can change at a state line.|SAME ACT<br>OPPOSITE ANSWER|06|
|0:50-0:55|Watch the full story on the channel. Follow for more.|WATCH THE<br>FULL STORY|07(hold)|

- `short31_01.png` A night car-window point of view with a single glowing smartphone held up in a faceless silhouetted hand, cold blue screen-light the only glow in the dark, no face, no logos, no readable text — *[common style suffix]* (**footage alt**: `unlock/factory/AF-BG-1979__smartphone_in_dark.mp4` or `AF-BG-1899__police_car_lights_night.mp4`, vertical crop)
- `short31_02.png` A modern smartphone standing upright reimagined as a heavy steel bank-safe, a bright ring of light where the lock screen would be, deep navy void around it, no brand marks, no readable text — *[common style suffix]*
- `short31_03.png` A glowing padlock of pure light hovering over a phone-shaped dark slab while a translucent scroll of light dissolves beside it, signalling that permission to search is not the power to open, no seals, no readable document text, no logos — *[common style suffix]* (**footage alt**: `unlock/factory/AF-BG-0510__courtroom_interior.mp4` or `AF-BG-6598__supreme_court_building.mp4`, vertical crop)
- `short31_04.png` A cool blue wireframe of a human head in profile with a small glowing combination lock suspended inside it, the idea of a secret held only in the mind, no facial detail, no likeness, no readable text — *[common style suffix]*
- `short31_05.png` An anonymous gloved hand pressing a featureless fingertip onto a phone's glowing sensor, a ring of light blooming open at the touch, the body opening the lock without thought, no faces, no logos, no readable screen — *[common style suffix]*
- `short31_06.png` Two identical courthouse doorways side by side under a cold sky, one swinging open in warm gold light and the other sealed shut in blue, a single hairline fracture of light running down the seam between them, no seals, no signage, no readable text — *[common style suffix]* (**footage alt**: `unlock/factory/AF-BG-3283__courthouse_steps.mp4` or `AF-BG-3351__judge_gavel_wooden.mp4`, vertical crop)
- `short31_07.png` A single glowing locked smartphone centered in a dark frame with a bright key of light hovering beside it but never turned, generous negative space around it for the CTA endcard, no face, no logo, no readable text — *[common style suffix]*
- **thumbnail** `short31_thumb.png` A locked glowing phone split by a hairline crack of light, a bright combination-lock symbol over the screen ／ headline: **"YOUR THUMB OR YOUR MIND?"** ／ badge: "5TH AMEND."

> **FACT-CHECK** — officer holds your phone / the phone holds your whole life = SPN-0001 (FR-P + FR-T); 2014 Riley v. California, unanimous, "get a warrant," and it is about *searching* the phone, not forcing you to *open* it = SPN-0004/SPN-0005 (FR-R); the Fifth Amendment shields only what is "testimonial" (the contents of the mind); the safe-combination-vs-key analogy from Doe v. United States (1988) = SPN-0008/SPN-0009 (FR-T); a memorized passcode is a combination that may be protected, while face/thumb are physical, non-testimonial like fingerprints/blood at booking (Schmerber/Dionisio) = SPN-0010/SPN-0011 (FR-T + FR-PC-prot); 2024, U.S. v. Payne (9th Cir.), officers pressed a man's own thumb to the sensor → NOT a Fifth Amendment violation (9th Cir. only; caveats: he'd conceded the phone was his, and choosing *which* finger might differ) = SPN-0012/SPN-0029 (FR-P); 2025, U.S. v. Brown (D.C. Cir.), forcing a fingerprint unlock DID violate the Fifth Amendment = SPN-0015 (FR-B); states split on passcodes — protected in PA/IN/UT (Davis/Seo/Valdez), compellable in NJ/IL (Andrews/Sneed) = SPN-0016/SPN-0033 (FR-PC-prot + FR-PC-comp); the crux is the "foregone conclusion" doctrine (Fisher 1976) — is the government's target the passcode itself or the data behind it = SPN-0017 (FR-FC); the Supreme Court has repeatedly declined (Davis 2020 / Andrews 2021 / Sneed 2024 / Valdez 2024 cert denied) → no national rule, right changes at a state line = SPN-0019/SPN-0020 (FR-SC).

> **RISK (R2 — real, undecided legal question; needs a light legal-eye pass)** — LOCKS:
> 1. **Never say the Supreme Court "decided/ruled/banned/allowed" forcing an unlock.** It has *repeatedly declined* to hear it (Davis/Andrews/Sneed/Valdez cert denied). The ONLY Supreme Court holding you may state as fact is **Riley (2014): police generally need a warrant to *search* a phone** — and Riley is about searching, not compelling you to open it.
> 2. **Keep the two amendments distinct.** Fourth = search (Riley). Fifth = being forced to unlock. NEVER say "a warrant lets them force it open." A warrant permits looking inside; whether you can be *made to open it yourself* is the separate, unsettled Fifth Amendment fight.
> 3. **Never state the pattern as an absolute national rule.** Do NOT say a passcode is "always" protected (NJ/IL compel it) or biometrics are "never" protected (Brown, D.C. Cir. 2025, is the opposite). Frame with **"many courts," "may," "often," "split," "depends on the state," "still unsettled."**
> 4. **Attribute each ruling to its court; no over-reading.** Payne (9th Cir. 2024) is NOT a green light for all biometrics (9th Cir. only; caveats). Brown (D.C. Cir. 2025) is NOT a national rule that biometrics are protected. Say "one federal court… another federal court…," attributing to the specific court, never to "the courts" or "the law" generally.
> 5. **No real-person likeness** of any defendant (Payne / the Brown appellant) or any justice (Roberts). Omit the defendants' underlying crimes entirely — the subject is **"you" and the legal doctrine**, not the defendants. Symbolic, faceless visuals only.
> 6. **Not legal advice.** No "you should" second-person instructions. Use "many courts / it depends / it's unsettled." The power-off / "before first unlock" device fact (FR-BFU) and the border-search exception (FR-BORDER) are NOT used in this 5-beat cut; if a variant adds them, frame BFU as a device-security fact (not advice) and the border as unsettled and binding almost no one.
> 7. **No brand marks or trademarks.** No Apple logo, no "iPhone/Face ID/Touch ID" wordmarks, no Android robot, no court seals, no readable statute or case titles (SDXL fakes text). Symbolic subjects only (glowing locked phone, padlock of light, key never turned, courthouse-vs-hidden-backdoor, encryption as a wall of light). Pre-publish legal-eye review (light, R2).

**Suggested YouTube TITLE**: The Police Can Force Your Thumb — But Maybe Not Your Passcode #Shorts

**DESCRIPTION**: An officer can press your own thumb to your phone and open it — but the passcode in your head may be the one lock the government can't force. In 2024 one federal court called a forced thumbprint legal; in 2025 another called it unconstitutional; the states split and the Supreme Court keeps refusing to decide — so your right can change at a state line. Full breakdown on the channel.

---

## §2 制作・公開手順（別スレッド Claude Code 用チェックリスト）

1. **素材**: 各 `image` を用意 — フッテージ優先（`H:\pd-media\assets\factory\` 縦クロップ、または本編 `unlock/factory/*` ＝ `remotion/src/data/unlock_film.json` 参照素材／`PD-2026-031-unlock/05_visuals` 流用）、足りない所だけローカル（SD3.5 `sd35_gen.py` 優先 / SDXL `gen_max.ps1`・素のSDXL/FLUX-dev不可）で縦生成し `H:\pd-media\assets\ai\shorts\short31\` へ。**本人肖像なし・ロゴ/ブランドマークなし・可読な実在テキストなし・公印なし**。**Codex生成は不要**。
2. **ナレ**: §0の声で英語生成（承認済）。GAP≈2.70s、~50〜55s。
3. **組み立て**: `Short.tsx`（1080×1920）で時間表どおり。フッテージはそのまま／静止画は2.5D・浮遊カード。テロップは上表の英語を大きく焼き込み（下部セーフ・重い黒箱を避ける）。カットはスピーディー・無音は最大0.6秒。
4. **音**: 4層＋ダッキング＋2パス静的 -14 LUFS（`build_short_mix.py`）。中盤で痩せないこと。
5. **サムネ**: `short31_thumb.png`（<2MB）＋大文言を `ShortThumb` で。公開時は先頭0.7sカバーフレーム焼き込み（crf18）。
6. **公開**: **1日1本・12:00 JST 予約**。予約前に全 `publishAt` 監査→空き日。**R2 は法務レビュー**。最終チェック＝本人肖像なし・中立・広告安全・言い回しロック・字幕がナレに一致。
7. **命名衝突に注意**: 既存 `short01`〜`short30` と衝突させない。新規は `short31`。`Root.tsx` へ `Short-short31-yt/-tt` と `ShortThumb-short31` を登録。
8. **整合**: 本編台本（`PD-2026-031-unlock/03_script/`）・`fact_recheck.v001` 更新時は VO/FACT-CHECK を取り直す。durable source content_hash は公開前に確定。
