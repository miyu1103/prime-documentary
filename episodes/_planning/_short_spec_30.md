# 縦型ショート 完全設計書 — 第30話（Ronald Cotton / Jennifer Thompson — 目撃者誤認と DNA 冤罪雪冤）別スレッド制作用・自己完結版

第30話（本編 `PD-2026-030-cotton`）に1対1で対応する縦型ショート1本。**この設計書だけで別スレッドの Claude Code が単体で完成まで作れるよう、仕様・数値・言い回しロックをすべて本文に書ききる。** 書式・数値・ロックの基準は `SHORTS_EP19-24.md`／`_short_spec_25.md`（§0 共通仕様・per-SHORT 表・画像プロンプト・FACT-CHECK・RISK）に完全準拠する。

> **重要（オーナー指示・EP19-25 と同一）**
> - ショートは**別スレッドの Claude Code** が制作する。この設計書が唯一の指示書。
> - **Codex 画像生成は必須ではない。** 縦画像は「①`H:\pd-media\assets\factory\` の商用OK**動画フッテージ**（縦クロップ）②本編 `PD-2026-030-cotton/05_visuals` の流用 ③必要な所だけローカル SD3.5(`sd35_gen.py`) / SDXL(`gen_max.ps1`) で縦生成」で賄ってよい。下の各 `image` プロンプトは**ローカル生成する場合の指定**。動く素材でまかなえるものはフッテージ優先（紙芝居回避）。素の SDXL・FLUX-dev は不可。
> - チャンネルは**US英語**。VO・テロップ・サムネ文言は下表の英語をそのまま使う。翻訳工程なし。
> - 動きの基準は本編と同じ新テンプレ思想（フッテージ主役＋2.5D＋モーショングラフィックス、ただの左右パン/ズーム禁止、金の縦スイープ禁止、黄色ウォッシュ禁止）。

## §0 共通仕様（`_short_spec_25.md` §0 と同一。要点を再掲）

- **画面**: 縦 9:16 / 1080×1920 / **尺 ~50〜55秒**（本話は5 VOビートで ~54s）/ 字幕（テロップ）常時 / モバイル前提の大きな文字。
- **本人肖像なし**（実在人物 Ronald Cotton / Jennifer Thompson / Bobby Poole・当時の刑事の顔・似顔・声真似は禁止・invariant 11）。**画像内に可読な実在テキスト/ロゴ/公印/紋章を描かない**（テロップは Remotion で焼く）。
- **ナレ音声**: 本編と同じ声 `ElevenLabs VOICE_ID nPczCjzI2devNBz1zQrb / eleven_multilingual_v2 / stability0.35 / similarity0.80`。英語生成（承認済・追加確認不要）。
- **音**: 4層ミックス（BGM／緊張／環境／SFX）＋ダッキング＋**2パス静的 -14 LUFS**。中盤で音量が痩せないよう `speechnorm+グルー圧縮`（`build_short_mix.py` の short17〜設定を踏襲）。GAP≈2.70s。
- **コンポジション**: 縦Remotion `Short.tsx`（1080×1920）。時間表どおり並べ、上品に動かす。カットはスピーディー・ナレの無音は最大0.6秒。
- **サムネ**: `short30_thumb.png`（<2MB）＋大文言を `ShortThumb` で重ねて書き出し。Shorts公開時は**先頭0.7sにカバーフレーム焼き込み**（libx264 crf18）。
- **VO末尾CTA（共通）**: "Watch the full story on the channel. Follow for more."
- **画像プロンプト末尾に共通スタイルを付す**: *"museum-grade cinematic symbolic documentary still, vertical 9:16, deep-navy / black base, electric-blue signal, restrained muted-gold accent, film grain, no faces, no likeness, no readable text / logos / seals, no document titles, symbolic reconstruction (not authentic footage)."*
- **画像 HARD RULES（毎枚順守）**: 顔・似顔・実在人物の肖像を描かない（シルエット/後ろ姿/手のみ）／可読な実在テキスト・ロゴ・公印・書類タイトルを描かない（SDXLは文字を捏造するため文字なしの象徴被写体に限る）／暴力・性的加害の描写は一切しない（示唆すら映像化しない）。各プロンプトは1文。
- **保存先**: `H:\pd-media\assets\ai\shorts\short30\`（使う画像＋`short30_thumb.png`）。フッテージ流用時はそのパスを `image` 欄に併記。

## §1 公開ゲート

- **1日1本ちょうど・12:00 JST 予約**（`publishAt`）。新規予約前に全 `publishAt` を監査し空き日へ。衝突は `--replace` で日付修正。
- オーナーが一度OK。**R3 は法務＋センシティビティ・レビュー必須**（下の RISK 参照）。
- 最終チェック: 本人肖像なし・被害者を決して責めない・中立・広告安全・**言い回しロック**・字幕がナレに一致・切れ目が自然。
- 本編台本（`PD-2026-030-cotton/03_script/script.annotated.v001.json` ＝真実の出典）が更新されたら VO/FACT-CHECK を取り直す。

---

## SHORT #30 →（本編 第30話 Ronald Cotton / Jennifer Thompson）A survivor did everything a perfect eyewitness is supposed to do, swore in court she was certain — and still sent an innocent man to prison for more than a decade.
**The one surprise**: The problem was never that Jennifer Thompson wasn't sure enough — she was the careful, deliberate witness a prosecutor dreams of, and she was completely, honestly wrong, because Ronald Cotton was the only man who appeared in both the photo lineup and the live lineup, so she may have been recognizing the police photo, not her attacker; DNA in 1995 excluded Cotton and matched the real perpetrator, and instead of staying accuser and accused, the two became close friends and advocates who helped reform how police run a lineup.

| time | VO (English) | telop (English, short) | image |
|---|---|---|---|
|0:00-0:03|In a courtroom she looked at the man who attacked her and swore she was certain. She was completely wrong.|SHE WAS SURE<br>SHE WAS WRONG|01|
|0:03-0:17|In 1984, in Burlington, North Carolina, a college student named Jennifer Thompson was attacked at knifepoint. She forced herself to memorize her attacker's face. Police showed her a photo lineup, then a live lineup, and both times she chose a man named Ronald Cotton.|MEMORIZED<br>HIS FACE|02|
|0:17-0:34|But Cotton was the only person who appeared in both lineups. By the live lineup, she may have been recognizing the police photo, not her attacker. Detectives told her she'd done great — and that quiet reassurance hardened a careful guess into total certainty. In 1985, it sent Cotton to prison.|THE ONLY MAN<br>IN BOTH LINEUPS|03,04|
|0:34-0:50|He served more than a decade. Then in 1995, DNA testing excluded Ronald Cotton and matched the real attacker — a lookalike inmate named Bobby Poole, who later pleaded guilty. Cotton walked free. Here is the part no one expects: he and Jennifer became close friends and advocates who helped reform how police run a lineup.|DNA FREED<br>THE RIGHT MAN|05,06|
|0:50-0:54|Watch the full story on the channel. Follow for more.|WATCH THE<br>FULL STORY|07(hold)|

- `short30_01.png` A backlit police lineup rendered as five faceless anonymous silhouettes standing in a row behind a cold measuring grid, deep navy, one figure faintly haloed, no faces, no readable text — *[common style suffix]* (**footage alt**: `factory` `AF-BG-14765__police_station_at_night` / `AF-BG-36301__police_station_at_night`, vertical crop)
- `short30_02.png` A sketch artist's pencil resting on an unfinished, featureless composite face on paper, warm desk lamp against navy dark, memory as a rough sketch, no recognizable person, no readable words — *[common style suffix]*
- `short30_03.png` One anonymous silhouette photo-card lifting out of a six-frame array and reappearing inside a backlit live-lineup row — the same faceless figure in both places, electric-blue link line between them, no faces, no text — *[common style suffix]*
- `short30_04.png` A single tentative pencil outline of a face being traced over again and again until it hardens into one bold confident line, motion-graphic of a guess turning into certainty, navy field, no real likeness, no letters — *[common style suffix]* (**footage alt**: `factory` `AF-BG-15127__magnifying_glass_on_document`, vertical crop)
- `short30_05.png` A luminous DNA double helix of electric-blue light beside two banding columns, one clearly not aligning and one snapping into perfect alignment, cold forensic truth, no faces, no readable labels — *[common style suffix]* (**footage alt**: `factory` `AF-BG-25675__dna_double_helix_render` / `AF-BG-18218__dna_laboratory_blue`, vertical crop)
- `short30_06.png` Two anonymous hands reaching across a small table and almost meeting in warm golden light against soft navy, reconciliation and forgiveness, faces unseen, tender and quiet, no text — *[common style suffix]*
- `short30_07.png` Two long shadows walking side by side into a warm bloom of light down a corridor, partners not enemies, generous empty negative space for the CTA endcard, no faces, no logos, no text — *[common style suffix]*
- **thumbnail** `short30_thumb.png` A backlit faceless police lineup with one silhouette softly haloed and a thin electric-blue DNA helix crossing the frame ／ headline: **"SURE — BUT WRONG"** ／ badge: "DNA"

> **FACT-CHECK** — (真実の出典 = `03_script/script.annotated.v001.json` の SPN + FR タグ; `remotion/src/data/cotton_film.json` hookLine/captions 照合済) — courtroom ID, "absolutely certain," and catastrophically wrong = SPN-0001/SPN-0007 (FR-id + FR-trial); summer 1984, Burlington NC, Jennifer Thompson, 22, college student, attacked in her apartment at knifepoint = SPN-0003 (FR-crime); she deliberately forced herself to memorize her attacker's face = SPN-0003 (FR-crime); six-photo array → she narrowed to two → chose Cotton, then a live lineup → chose Cotton again = SPN-0004 (FR-id); **Ronald Cotton was the only man in BOTH the photo lineup and the live lineup** = SPN-0005 (FR-id); confirming feedback ("you did great" / "yes, you picked the right man") hardened a tentative pick into unshakable certainty = SPN-0006 (FR-id + FR-mem); 1985 convicted = SPN-0007 (FR-trial); served more than a decade / "more than ten years" = SPN-0011 (FR-dna); 1995 LabCorp DNA **excluded Cotton and matched Bobby Poole** = SPN-0012 (FR-dna); Poole = lookalike inmate who later **pleaded guilty** = SPN-0009 + SPN-0014 (FR-poole + FR-dna); Cotton freed June 30, 1995, pardoned = SPN-0014 (FR-dna); the two became close friends and advocates and lineup procedure was reformed (blind administration) = SPN-0018 (FR-rec + FR-reform).

> **RISK (R3 — real people, sexual-assault subject; case is exonerated/settled → factually safe but sensitive)** — LOCKS:
> 1. **The exoneration is stateable as fact.** DNA excluded Cotton, he was pardoned, and Bobby Poole pleaded guilty — say "DNA proved Cotton innocent / freed him," never hedge it as opinion.
> 2. **NEVER blame the survivor.** The subject is *memory's fallibility + suggestive lineup procedure*, not Jennifer Thompson. She was sincere, careful, deliberate — the witness a prosecutor dreams of. Do NOT call her careless, foolish, a liar, or at fault. Frame her as honest-and-wrong.
> 3. **Assault is suggested only, never depicted.** No violence, no reenactment, no dramatization of the attack. Respectful, restrained visuals only.
> 4. **No real-person likeness** of Cotton, Thompson, Poole, or any detective. Faceless silhouettes / hands / back-of-head only. No faces.
> 5. **Bobby Poole = the man who pleaded guilty / the DNA-matched perpetrator** — state that plainly. **OMIT Poole's death and the unverified "24 crimes / other assaults count."** Do not invent or imply a number of his crimes.
> 6. **Police / the detective are framed as reformers, not villains.** The lineup procedure was flawed and later fixed (done blind); do not accuse the detective of malice or misconduct.
> 7. **Duration language:** "more than a decade" / "more than ten years." Do not overstate. If a dollar figure is ever shown, state compensation as awarded, no editorializing.
> 8. **Attribute the mechanism as explanation, neutrally:** memory is rebuilt, not replayed; confirming feedback can harden a guess. Keep it as the case's own explanation, not a blanket verdict on all witnesses. Pre-publish legal-eye + sensitivity review (R3).

**Suggested YouTube TITLE**: She Was Certain He Attacked Her — Then DNA Proved She'd Sent the Wrong Man to Prison #Shorts

**DESCRIPTION**: In 1984 in Burlington, North Carolina, Jennifer Thompson memorized her attacker's face and twice picked Ronald Cotton out of a lineup — but Cotton was the only man in both lineups, and he was innocent. DNA in 1995 freed him after more than a decade and matched the real attacker. Then the accuser and the accused became friends and helped reform how police run a lineup — full story on the channel.

---

## §2 制作・公開手順（別スレッド Claude Code 用チェックリスト）

1. **素材**: 各 `image` を用意 — フッテージ優先（`H:\pd-media\assets\factory\` 縦クロップ、または本編 `PD-2026-030-cotton/05_visuals` 流用）、足りない所だけローカル SD3.5(`sd35_gen.py`) / SDXL(`gen_max.ps1`) で縦生成し `H:\pd-media\assets\ai\shorts\short30\` へ。**本人肖像なし・ロゴなし・可読な実在テキストなし・公印なし・書類タイトルなし・暴力/加害の描写なし**。素の SDXL・FLUX-dev 不可。
2. **ナレ**: §0の声で英語生成（承認済）。GAP≈2.70s、~50〜55s。
3. **組み立て**: `Short.tsx`（1080×1920）で時間表どおり。フッテージはそのまま／静止画は2.5D・浮遊カード。テロップは上表の英語を大きく焼き込み（下部セーフ・重い黒箱を避ける）。カットはスピーディー・無音は最大0.6秒。
4. **音**: 4層＋ダッキング＋2パス静的 -14 LUFS（`build_short_mix.py`）。中盤で痩せないこと。
5. **サムネ**: `short30_thumb.png`（<2MB）＋大文言を `ShortThumb` で。公開時は先頭0.7sカバーフレーム焼き込み（crf18）。
6. **公開**: **1日1本・12:00 JST 予約**。予約前に全 `publishAt` 監査→空き日。**R3 は法務＋センシティビティ・レビュー**。最終チェック＝本人肖像なし・被害者を責めない・中立・広告安全・言い回しロック・字幕がナレに一致。
7. **命名衝突に注意**: 既存 `short01`〜`short29` と衝突させない。新規は `short30`。`Root.tsx` へ `Short-short30-yt/-tt` と `ShortThumb-short30` を登録。
8. **整合**: 本編台本（`PD-2026-030-cotton/03_script/`）更新時は VO/FACT-CHECK を取り直す。durable source content_hash は公開前に確定。
