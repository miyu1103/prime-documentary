# サムネ ヒーローショット & タイトル — 第62話 greene（Codex生成用）

**ステータス:** 設計。**アートは `EP62_greene_CODEX_BATCH_A.v002.md` の THUMB プレートで既に発注済み。新規に絵を起こさない。**
Codex が `G220`–`G222`（＋本書で追加する `G226`）を生成 → オーナーが1枚選択 → Remotion `<Still>` で見出しを重ねて **1280×720** 書き出し。

**アート保存先:** `H:\pd-media\assets\ai\greene\` に `G220.png` `G221.png` `G222.png` `G226.png`（長辺3840px以上・16:9・PNG）。
**書き出し先:** `episodes/PD-2026-062-greene/09_package/thumbnail.v001.png` … `thumbnail.v004.png`、採用分を `thumbnail.selected.v001.png`。
（`check_final_acceptance.py` の `thumbnail_ready` はこの2箇所しか見ない。`10_thumbnail/*.png` でも可。）

**事件:** *Greene v. Lindsey*, 456 U.S. 444 (1982)。1975年、ルイビル住宅公社が3人の入居者に対して立退き手続を開始し、
ケンタッキー州法 §454.030 に基づき **令状をアパートのドアに貼る**ことで送達とされた。事実は `EP62_greene_FACTS_LEDGER.v001.md`。

---

## 0. 拘束条件（`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` 行11・12・13）

| 行 | 要求 | 本書での満たし方 |
|---|---|---|
| 11 | **候補3枚以上**・**1280×720**・アートは **Codex が事前生成**・`selected` を1枚決める | 候補**4枚**（`G220` `G221` `G222` `G226`）。うち3枚は発注済み、`G226` のみ追加発注 |
| 12 | 見出しは**大文字・3〜4語まで**・好奇心の芯は**一つ**・**主題は巨大**・**超高コントラスト**・地は黒/紺・アクセントは金 `#E5B53A` か電光青 `#1F6BFF`・文字は白/銀・**320pxで読める** | 見出し4案すべて4語。Remotion 側で合成（下記§2） |
| 12 | **実在人物の肖像を使わない** | 人物は後ろ姿・シルエット・手のみ。3人の被上告人（Linnie Lindsey / Barbara Hodgens / Pamela Ray）およびその住居の描写は契約 `forbidden_subjects` で禁止 |
| 11/12 | **生成アートの中に読める文字を入れない** | プロンプト本文に文字要素を一切書かない。見出しは **Remotion が合成する**。モデルには描かせない |
| 13 | タイトル **60字以内・フック先頭**・**A/Bペアを2組以上** | A/Bペア**3組**（§1）。最長49字 |

### ★ `thumbnail_visibility` ゲート — 真っ黒なサムネは落ちる

`check_final_acceptance.py` の `thumbnail_visibility` は **HARD** ゲートで、`09_package/thumbnail.selected*.png` の
**平均輝度（mean luma）が 33 以上**、かつコントラスト（標準偏差）が下限以上であることを要求する。
較正実績：**却下された暗い v001 = 平均 24.9〜29.5／承認された明るい v002 = 平均 36.4〜48.0。**

**本エピソードは特にここで落ちやすい。** `CODEX_BATCH_A.v002.md` §2 の `[STYLE]` は
*muted natural colour / low contrast / low-key* を指定しており、**本編の絵作りのままサムネを作ると平均輝度が 33 を割る。**

したがって **THUMB プレートだけは `[STYLE]` の低照度指定を上書きする**（§3 の各プロンプトに明記した）。
さらに **選択前に必ず実測する**こと。1枚でも 33 未満なら採用しない。

```
./.venv/Scripts/python.exe -c "from PIL import Image, ImageStat; import sys; [print(p, *[round(v,1) for v in (lambda s: (s.mean[0], s.stddev[0]))(ImageStat.Stat(Image.open(p).convert('L')))]) for p in sys.argv[1:]]" episodes/PD-2026-062-greene/09_package/thumbnail.v*.png
```

出力は `パス 平均輝度 コントラスト`。**平均輝度 ≥ 33 が必須。** 見出しを重ねた後の最終PNGで測ること（測るのは選択済みファイル）。

---

## 1. タイトル（A/Bペア3組・すべて60字以内・フック先頭）

**契約 `forbidden_claims` に触れないこと。** タイトルで特に危ないのは3つ：
①「最高裁は掲示を禁止した」（**禁止していない**）②現在形の主張（**1982年の判決**）③全国規模の数字（**判決文に無い**）。
加えて④「彼女は通知を見なかった」を**事実として**書かない（**主張であって認定ではない**）。

| 組 | 版 | タイトル | 字数 | 対になるプレート／見出し |
|---|---|---|---:|---|
| **1** | **A** | `The Men Who Taped It Up Knew It Came Off The Door` | 49 | `G222` / **THE PAPER CAME OFF** |
| **1** | **B** | `They Taped It To The Door. It Did Not Stay There.` | 49 | `G222` / **THE PAPER CAME OFF** |
| **2** | **A** | `A Paper Taped To A Door Counted As Legal Notice` | 47 | `G220` / **THIS COUNTED AS NOTICE** |
| **2** | **B** | `Kentucky Called Tape On A Door Legal Service` | 44 | `G220` / **THIS COUNTED AS NOTICE** |
| **3** | **A** | `One Knock. Nobody Home. The Paper Went Up.` | 42 | `G226` / **ONE KNOCK WAS ENOUGH** |
| **3** | **B** | `The Deputy Knocked Once. That Was The Procedure.` | 48 | `G226` / **ONE KNOCK WAS ENOUGH** |

**予備（`G221` 用・A/B相手なし）**

| 版 | タイトル | 字数 | 対になるプレート／見出し |
|---|---|---:|---|
| 予備 | `They Say They Never Saw The Paper On Their Door` | 47 | `G221` / **DID SHE EVER KNOW?** |

> 予備タイトルの `They Say` は**削らないこと**。削ると `forbidden_claims` の
> 「"She never saw the notice" stated as established fact」に直撃する（判決文は *claim* / *state* という動詞を保っている・GL-23 / GL-25）。

**タイトルで使ってはいけない語（この案件固有）**

- `banned` / `outlawed` / `struck down` — 判決は §454.030 の掲示を **as applied** で不十分としただけ（GL-66・Q-03・Q-15）
- `now` / `today` / `still` — 1982年の判決である（Q-01）
- `landlord`（強欲な家主の含意で） — 原告側の相手は**市の住宅公社**（GL-04・Q-08）
- 全国の件数・割合・人数（Q-04）
- `won` / `got their homes back` — 差戻しの是認である（GL-71・Q-11）

---

## 2. 見出し（Remotion が合成する・アートには焼き込まない）

4語以内・大文字・好奇心の芯は一つ。

| プレート | 見出し | 語数 | 芯にある問い |
|---|---|---:|---|
| `G220` | **THIS COUNTED AS NOTICE** | 4 | 「これが？」 |
| `G221` | **DID SHE EVER KNOW?** | 4 | 「中の人は知っていたのか」 |
| `G222` | **THE PAPER CAME OFF** | 4 | 「剥がれたら、どうなる」 |
| `G226` | **ONE KNOCK WAS ENOUGH** | 4 | 「一度だけ？」 |

**合成仕様（`BRAND.thumb` / Remotion `<Still>` 1280×720）**

- 地：黒〜濃紺（`#080B12`〜`#0E1626`）。アートは画面下 2/3。**上 1/3 は各プレートで空けてある**（§3 プロンプト参照）。
- 文字：白/銀（`#FFFFFF` / `#DCE3EC`）、太字、**320pxに縮小して読めること**。1行2〜3語で2行まで。
- アクセント：金 `#E5B53A`（`G220` `G222` `G226`）／電光青 `#1F6BFF`（`G221`）。**1枚につき1色だけ**。
  アクセントは見出しの下線かキッカーチップのどちらか一方に限る。両方は使わない。
- アートは主題が画面高の 60% 以上を占めること（行12「巨大な主題」）。

---

## 3. サムネ候補4枚（プレートID・プロンプト）

`G220`–`G222` は **`EP62_greene_CODEX_BATCH_A.v002.md` §5 THUMB の発注そのまま**。
本書は **輝度の上書き指示だけを足している**（`thumbnail_visibility` 対策）。**構図・被写体は変えない。**

`[STYLE]` `[NEG]` は同発注 §2 の定義。下では**展開済みの完全形**を書く（この1ファイルだけで生成できるように）。

**★ THUMB 4枚に共通の上書き（本編の絵作りと違う点）:**
> `bright even key light, the subject clearly separated from the ground, deep blacks kept but the subject held well above mid-grey, high micro-contrast`
> — `[STYLE]` の `low contrast, low-key` を**この4枚に限り打ち消す**。理由は §0 の輝度ゲート。

---

- `G226.png` — **【新規・本書で追加】ONE KNOCK WAS ENOUGH**

  A long run of identical apartment doors along an open-air concrete walkway seen down its length under bright flat overcast daylight, one single pale rectangle of paper on one door far down the line, the concrete and the painted doors bright and clearly separated, the upper third of the frame left clear, bright even key light, the subject clearly separated from the ground, deep blacks kept but the subject held well above mid-grey, high micro-contrast, cinematic still, muted natural colour, flat humid Ohio Valley light, soft falloff toward the edges, shallow depth of field, restrained documentary framing, mid-1970s to early-1980s American public housing period detail, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage. Avoid: text, lettering, numerals, handwriting, signatures, seals, emblems, logos, signage, house numbers, street signs, police uniform, sheriff badge, patrol car, courtroom interior, gavel, judge's bench, prison bars, razor wire, handcuffs, furniture on a pavement, people being evicted, crying, a hand on a shoulder, golden hour, sunset glow, postcard scenery, drone shot, cosy fireplace, Christmas, tropical, modern smartphones, modern cars, flat CGI, cartoon, illustration, oversaturated.

  *なぜ足すか*：`G220`–`G222` は3枚とも**寄りで低照度**である。輝度ゲート（平均33以上）を**確実に**満たす明るい引きの候補が1枚も無い。
  さらにこの絵は本編の賭け金の梯子（一つのドア → 一つの団地 → 十一の州）の二段目そのもので、台本 L47・L113 と一致する。

- `G220.png` — **THIS COUNTED AS NOTICE**（発注済み・§5 THUMB より）

  A single blank sheet of paper taped to a plain painted door, shot dead centre and close under hard directional light from the left, the upper third of the frame left clear, bright even key light, the subject clearly separated from the ground, deep blacks kept but the subject held well above mid-grey, high micro-contrast [STYLE] Avoid: [NEG]

- `G221.png` — **DID SHE EVER KNOW?**（発注済み・§5 THUMB より）

  A woman's silhouette on the inside of a drawn curtain with a pale rectangle of paper visible on the door beside the window, hard side light, the upper third of the frame left clear, bright even key light, the subject clearly separated from the ground, deep blacks kept but the subject held well above mid-grey, high micro-contrast [STYLE] Avoid: [NEG]

  *注意*：シルエットは**特定の実在人物ではない**。顔を出さない。3人の被上告人を描いたものとして扱わない（契約 `forbidden_subjects`）。
  4枚のうち**最も輝度が落ちやすい**。実測して33未満なら採用しない。

- `G222.png` — **THE PAPER CAME OFF**（発注済み・§5 THUMB より）

  A torn corner of paper still held under tape on an otherwise bare painted door, shot extreme close under strong contrast, the upper third of the frame left clear, bright even key light, the subject clearly separated from the ground, deep blacks kept but the subject held well above mid-grey, high micro-contrast [STYLE] Avoid: [NEG]

  *記録との対応*：これは台本 L197 のモチーフ状態5（破れた角がテープの下に残る）であり、
  多数意見の *"not infrequently removed by children or other tenants"*（GL-43）が画になったもの。**本命候補。**

---

## 4. `G226` の発注手順（発注者側の作業）

`G226` は **`EP62_greene_CODEX_BATCH_A.v002.md` にまだ入っていない**。生成を回す人は先に次をやること。

1. 同ファイル **§7（★追加発注）の末尾に `G226` を追記する。** `G001`–`G225` は**一語も触らない**。
   §7 の表と同じ書式で、区分は **THUMB**、用途は「サムネ候補（明るい引き・輝度ゲート対策）」。
2. プロンプト本文は**本書 §3 の展開済み全文をそのまま貼る**（`[STYLE]` の低照度指定を打ち消しているので、`[STYLE]` トークンに戻さない）。
3. `episode_spec.v001.json` の `mandatory_stills` に **`G226.png` を追加**して 226 件にする。
   （現在は `G001.png`–`G225.png` の 225 件。`check_spec_satisfied.py` の唯一の防波堤なので空欄・欠番を作らない。）
4. 保存先は他と同じ `H:\pd-media\assets\ai\greene\G226.png`。長辺3840px以上・16:9・PNG。

---

## 5. 生成後の検査（1枚ずつ・目視 → 実測の順）

1. **文字が写り込んでいないか。** 紙の上・ドア・壁・遠景すべて。1文字でもあれば不採用（行11/12・契約 `forbidden_subjects`）。
   紙の印字は「文字」ではなく **溶けた灰色の帯**として写っていること。
2. **顔が判別できないか。** 後ろ姿・シルエット・手のみ。実在人物に似ていないか。
3. **禁止被写体が無いか。** 制服・バッジ・パトカー・法廷・木槌・鉄格子・手錠・歩道の家具・立退きの最中・肩に置く手。
4. **上 1/3 が空いているか。** 見出しを乗せる場所。ここに主題がかかっていたら不採用。
5. **9:16 に切っても壊れないか**（ショート転用の可能性・`CODEX_BATCH_A.v002.md` §5.5 と同じ基準）。
6. **320px に縮小して主題が判るか。** 縮めて判らないものは1280×720でも効かない。
7. **輝度を実測する**（§0 のコマンド）。**平均輝度 33 未満は採用しない。** 見出しを重ねた最終PNGで測る。
8. 4枚を**並べて**見て、`selected` を1枚決める。決めたら `09_package/thumbnail.selected.v001.png` に置く。

> **自己申告の「派手です」は不可。** 採用の根拠は §0 の実測値（平均輝度・コントラスト）と、この8項目の目視結果である。
> タイトルとサムネの組はオーナー承認ゲート（`CLAUDE.md` §3「title/thumbnail approval」）。承認前に本番反映しない。
