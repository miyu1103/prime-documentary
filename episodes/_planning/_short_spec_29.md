# 縦型ショート 完全設計書 — 第29話（Anthony Ray Hinton — 無実の死刑囚）別スレッド制作用・自己完結版

第29話（本編 `PD-2026-029-hinton`）に1対1で対応する縦型ショート1本。**この設計書だけで別スレッドの Claude Code が単体で完成まで作れるよう、仕様・数値・言い回しロックをすべて本文に書ききる。** 書式・数値・ロックの基準は `_short_spec_25.md`（§0 共通仕様・5ビート表・画像プロンプト・FACT-CHECK・RISK）に完全準拠する。

> **重要（オーナー指示・EP19-25 と同一）**
> - ショートは**別スレッドの Claude Code** が制作する。この設計書が唯一の指示書。
> - **Codex 画像生成は必須ではない。** 縦画像は「①`H:\pd-media\assets\factory\` の商用OK**動画フッテージ**（縦クロップ）②本編 `PD-2026-029-hinton/05_visuals`（`hinton/img`）の流用 ③必要な所だけローカル高品質(SD3.5 `sd35_gen.py` / SDXL `gen_max.ps1`)で縦生成」で賄ってよい。下の各 `image` プロンプトは**生成する場合の指定**。動く素材でまかなえるものはフッテージ優先（紙芝居回避）。素のSDXL・FLUX-dev は不可。
> - チャンネルは**US英語**。VO・テロップ・サムネ文言は下表の英語をそのまま使う。翻訳工程なし。
> - 動きの基準は本編と同じ新テンプレ思想（フッテージ主役＋2.5D＋モーショングラフィックス、ただの左右パン/ズーム禁止、金の縦スイープ禁止、黄色ウォッシュ禁止）。
> - **題材は実在の存命人物**（無実で釈放された Anthony Ray Hinton）。**尊厳をもって共感的に描く。似顔・声真似・肖像なし。処刑や暴力を扇情化しない。** 数値は本編台本（下記FACT-CHECK）と厳密一致。

## §0 共通仕様（`_short_spec_25.md` §0 と同一。要点を再掲）

- **画面**: 縦 9:16 / 1080×1920 / **尺 ~50〜55秒**（本話は5 VOビートで ~55s）/ 字幕（テロップ）常時 / モバイル前提の大きな文字。
- **本人肖像なし**（実在人物 Anthony Ray Hinton / Bryan Stevenson / Andrew Payne / 被害者・検察官の顔・似顔・声真似は禁止・invariant 11）。**画像内に可読な実在テキスト/ロゴ/公印/紋章/書類タイトルを描かない**（SDXLは文字を捏造する。テロップは Remotion で焼く）。
- **ナレ音声**: 本編と同じ声 `ElevenLabs VOICE_ID nPczCjzI2devNBz1zQrb / eleven_multilingual_v2 / stability0.35 / similarity0.80`。英語生成（承認済・追加確認不要）。
- **音**: 4層ミックス（BGM／緊張／環境／SFX）＋ダッキング＋**2パス静的 -14 LUFS**。中盤で音量が痩せないよう `speechnorm+グルー圧縮`（`build_short_mix.py` の short17〜設定を踏襲）。GAP≈2.70s。
- **コンポジション**: 縦Remotion `Short.tsx`（1080×1920）。時間表どおり並べ、上品に動かす。カットはスピーディー・ナレの無音は最大0.6秒。
- **サムネ**: `short29_thumb.png`（<2MB）＋大文言を `ShortThumb` で重ねて書き出し。Shorts公開時は**先頭0.7sにカバーフレーム焼き込み**（libx264 crf18）。
- **VO末尾CTA（共通）**: "Watch the full story on the channel. Follow for more."
- **画像プロンプト末尾に共通スタイルを付す**: *"museum-grade cinematic symbolic documentary still, vertical 9:16, deep-navy / black base, electric-blue signal, restrained muted-gold accent, film grain, no faces, no readable text / logos / seals / document titles, symbolic reconstruction (not authentic footage), dignified and never graphic."*
- **保存先**: `H:\pd-media\assets\ai\shorts\short29\`（使う画像＋`short29_thumb.png`）。フッテージ流用時はそのパスを `image` 欄に併記。

## §1 公開ゲート

- **1日1本ちょうど・12:00 JST 予約**（`publishAt`）。新規予約前に全 `publishAt` を監査し空き日へ。衝突は `--replace` で日付修正。
- オーナーが一度OK。**R2 は法務目線＋尊厳レビュー必須**（下の RISK 参照）。
- 最終チェック: 本人肖像なし・中立・広告安全・**言い回しロック**・字幕がナレに一致・切れ目が自然・**数値が本編台本と一致**。
- 本編台本（`PD-2026-029-hinton/03_script/script.en.v001.md`）が更新されたら VO/FACT-CHECK を取り直す。

---

## SHORT #29 →（本編 第29話 Anthony Ray Hinton）Alabama planned to execute a man for thirty years — on a single bullet "match" that his broke, mistaken defense could never fight, and that the state, in the end, could not reproduce at all.
**The one surprise**: The entire capital case rested on one claim — that crime-scene bullets matched an old .38 revolver from his mother's home — yet his court-appointed lawyer, *wrongly* believing Alabama capped expert money at a thousand dollars, never asked for the funds to hire a real forensic expert; the "scientist" he could afford was blind in one eye and could not even work the comparison microscope. Nearly thirty years later, when the state finally had to prove that bullet "match" again with modern experts, it simply couldn't — and in 2014 a **unanimous** Supreme Court (*Hinton v. Alabama*) threw out the conviction, freeing an innocent man who had kept his mind alive on death row with a prison book club.

| time | VO (English) | telop (English, short) | image |
|---|---|---|---|
|0:00-0:04|For thirty years, Alabama planned to execute Anthony Ray Hinton — for two murders he did not commit.|THIRTY YEARS<br>INNOCENT|01|
|0:04-0:17|The entire case rested on a single claim: that bullets from the crime scenes matched an old .38 revolver from his mother's home. No eyewitness. No fingerprints. No confession. Only that match.|ONLY<br>THE BULLETS|02,03|
|0:17-0:33|To fight it he needed a real forensic expert. But his lawyer wrongly believed the state capped that money at a thousand dollars. There was no cap. The witness he could afford was blind in one eye and couldn't work the microscope. A jury convicted him in 1986 — in about an hour.|A $1,000<br>MISTAKE|04,05|
|0:33-0:50|For nearly thirty years on death row, he kept his mind free — a book club, imagined travels — while he counted fifty-four men walked to the chair. Then Bryan Stevenson's Equal Justice Initiative proved the bullets matched nothing, and in 2014 a unanimous Supreme Court threw out his conviction. He walked free in 2015 — the 152nd person cleared from death row.|9–0<br>FREED 2015|06|
|0:50-0:55|Watch the full story on the channel. Follow for more.|WATCH THE<br>FULL STORY|07(hold)|

- `short29_01.png` A lone death-row cell door in a cold navy dark, a single hard shaft of electric-blue light falling across a bare concrete floor, sense of thirty years pressing in, no faces, no readable text — *[common style suffix]* (**footage alt**: `factory` `AF-BG-6842__jail_cell_bars` or `AF-BG-4885__prison_corridor`, vertical crop)
- `short29_02.png` An extreme macro of a single spent bullet on a cold steel evidence tray under clinical light, one hairline crack of blue running through it as the whole case balanced on it, no readable text — *[common style suffix]* (**footage alt**: `factory` `AF-BG-18182__evidence_bag` / `AF-BG-14901__evidence_locker_shelves`, vertical crop)
- `short29_03.png` An old .38-style revolver lying still in a shadowed drawer of a quiet home, dust and years on it, restrained and non-glorified, no hands, no faces, no text — *[common style suffix]*
- `short29_04.png` A comparison microscope under hard courtroom light with one eyepiece left dark and unfocused, a low muted-gold bar pressing down over it like a false ceiling (abstract, no readable digits), the fatal mistaken limit as pure form, no faces, no text — *[common style suffix]* (**footage alt**: `factory` `AF-BG-25898__microscope_slide_macro` / `AF-BG-32479__microscope_lab`, vertical crop)
- `short29_05.png` An empty jury box and a single lone defendant's chair in a shadowed courtroom, one hard hour implied by a clock hand blurred in motion, dignified and sober, no faces, no seals, no text — *[common style suffix]* (**footage alt**: `factory` `AF-BG-14618__jury_box_empty` / `AF-BG-0510__courtroom_interior`, vertical crop)
- `short29_06.png` A heavy prison gate swinging open onto an overwhelming warm dawn horizon, cold navy giving way to flooding gold light, cold silhouetted scales of justice balancing at last, no faces, no seals, no readable text — *[common style suffix]* (**footage alt**: `factory` `AF-BG-62984__prison_gate_closing` reversed / `AF-BG-3297__courthouse_steps`, vertical crop)
- `short29_07.png` A free horizon at first light — an open road under warm sun after the navy, a single empty chair left behind in the dark foreground, generous negative space for the CTA endcard, no faces, no logos, no text — *[common style suffix]* (**footage alt**: `factory` `AF-BG-5673__lone_person_silhouette_walking` distant, vertical crop)
- **thumbnail** `short29_thumb.png` A lone dark cell with one bright blade of light under the door and a single cracked bullet macro overlaid ／ headline: **"INNOCENT — 30 YEARS"** ／ badge: "9–0"

> **FACT-CHECK** — Alabama sought his execution ~30 yrs / two 1985 murders he did not commit=SPN-0001/SPN-0022 (FR-tl + FR-scotus); the only evidence tying him to the killings was a claim that crime-scene bullets matched an **old .38-caliber revolver from Hinton's mother's home** — no eyewitness, no fingerprints, no confession=SPN-0007/SPN-0008 (FR-ev); the **$1,000 "cap" was the court-appointed lawyer's MISTAKEN belief — there was NO such cap** and the money was available for the asking=SPN-0009 (FR-cap); the defense expert (civil engineer **Andrew Payne**) admitted he had **sight in only one eye** and could not properly operate the **comparison microscope**=SPN-0010 (FR-cap); jury convicted him of both murders in **September 1986, in about an hour**, and he was sentenced to die=SPN-0012 (FR-tl); on death row he kept his mind alive with a book club (James Baldwin) and imagination=SPN-0014/SPN-0015 (FR-hum); **fifty-four men taken to the electric chair = Hinton's own count/testimony** (attribute, "Hinton says")=SPN-0017 (FR-hum); **Bryan Stevenson / Equal Justice Initiative** fought 16 yrs and in **2002 put three of the country's top firearms experts (one FBI)** on the stand — the crime bullets could not be matched to that revolver=SPN-0018 (FR-eji); **Hinton v. Alabama (2014) was UNANIMOUS 9–0**, holding the original trial unconstitutional because counsel's failure to seek expert funding (built on the false $1,000 belief) denied a real defense=SPN-0020 (FR-scotus); when the state had to prove the ballistics match again with modern experts it **could not reproduce it**, and prosecutors moved to drop the charges=SPN-0021 (FR-scotus); **freed April 3, 2015, after nearly thirty years — the 152nd person freed from U.S. death row after being wrongly condemned**=SPN-0022 (FR-scotus); **the two murders were never solved** — no alternate suspect is named=SPN-0023 (FR-cr).

> **RISK (R2 — real, living, publicly EXONERATED person; death-penalty + race sensitivities → mandatory legal-eye + dignity review)** — LOCKS:
> 1. **"Exonerated / wrongfully convicted / innocent" is stateable as fact** here — the state dropped the charges after a unanimous Supreme Court reversal (FR-scotus). Do NOT hedge his innocence as opinion or allegation.
> 2. **Confirm every number against the script**: "thirty years" / "nearly thirty years" (NOT a precise "28"), convicted **1986**, freed **April 3, 2015**, **152nd** freed from death row, **9–0** in **2014**, **fifty-four** executions = **Hinton's own count** (attribute). Do not invent figures the script does not state.
> 3. **The $1,000 is a MISTAKE, never a real law.** NEVER say Alabama "capped" or "limited" expert money at $1,000 as fact. Always frame it as the lawyer's *wrongly believed* cap that never existed (FR-cap).
> 4. **Attribute contested framing.** Race/poverty as a cause = **Hinton's / EJI's view**, not asserted by us. The "54 executions" = **Hinton's testimony**. The 2002 ballistics conclusion = **the experts' finding**. The 2014 holding = **the Court's ruling**.
> 5. **The murders were never solved — name NO alternate suspect, imply none.** Do not suggest who "really" did it (FR-cr).
> 6. **No real-person likeness** of Hinton, Stevenson, Payne, the victims, or officials. Symbolic visuals only, no faces. **Never sensationalize the execution or the deaths** — the empty chair / corridor motifs must be restrained and non-graphic. No blood, no gore, no re-enacted violence.
> 7. **Dignified, sympathetic tone throughout.** He is a real man who survived this; frame it as endurance and exoneration, not true-crime spectacle. No mockery of the one-eyed expert — it is systemic failure, told soberly. Pre-publish legal-eye + dignity review required (R2).

**Suggested YouTube TITLE**: He Spent 30 Years on Death Row for a Bullet That Matched Nothing #Shorts

**DESCRIPTION**: In 1985, two Alabama murders went unsolved — and Anthony Ray Hinton nearly paid with his life. Convicted on a single bullet "match" his broke, mistaken defense could never fight, he spent nearly thirty years on death row before Bryan Stevenson's Equal Justice Initiative and a unanimous Supreme Court (Hinton v. Alabama, 2014) helped free him in 2015. Full breakdown on the channel.

---

## §2 制作・公開手順（別スレッド Claude Code 用チェックリスト）

1. **素材**: 各 `image` を用意 — フッテージ優先（`H:\pd-media\assets\factory\` 縦クロップ、または本編 `PD-2026-029-hinton/05_visuals`（`hinton/img`）流用）、足りない所だけローカル高品質(SD3.5 `sd35_gen.py` / SDXL `gen_max.ps1`)で縦生成し `H:\pd-media\assets\ai\shorts\short29\` へ。**本人肖像なし・ロゴなし・可読な実在テキストなし・公印なし・書類タイトルなし**。**Codex生成は不要**。
2. **ナレ**: §0の声で英語生成（承認済）。GAP≈2.70s、~50〜55s。
3. **組み立て**: `Short.tsx`（1080×1920）で時間表どおり。フッテージはそのまま／静止画は2.5D・浮遊カード。テロップは上表の英語を大きく焼き込み（下部セーフ・重い黒箱を避ける）。カットはスピーディー・無音は最大0.6秒。
4. **音**: 4層＋ダッキング＋2パス静的 -14 LUFS（`build_short_mix.py`）。中盤で痩せないこと。
5. **サムネ**: `short29_thumb.png`（<2MB）＋大文言を `ShortThumb` で。公開時は先頭0.7sカバーフレーム焼き込み（crf18）。
6. **公開**: **1日1本・12:00 JST 予約**。予約前に全 `publishAt` 監査→空き日。**R2 は法務＋尊厳レビュー**。最終チェック＝本人肖像なし・中立・広告安全・言い回しロック・字幕がナレに一致・数値が本編台本と一致。
7. **命名衝突に注意**: 既存 `short01`〜`short28` と衝突させない。新規は `short29`。`Root.tsx` へ `Short-short29-yt/-tt` と `ShortThumb-short29` を登録。
8. **整合**: 本編台本（`PD-2026-029-hinton/03_script/`）更新時は VO/FACT-CHECK を取り直す。durable source content_hash は公開前に確定。
