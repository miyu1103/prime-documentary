# サムネ ヒーローショット & タイトル — 第63話 correa（Codex生成用）

**Episode:** `PD-2026-063-correa` · *Correa v. Hospital San Francisco*, 69 F.3d 1184 (1st Cir. 1995)
**Binding:** `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` **行11・行12・行13** ／ `episodes/PD-2026-063-correa/episode_spec.v001.json`
**発注書:** `episodes/_planning/EP63_correa_CODEX_BATCH_A.v001.md` §5「THUMB（3枚）」＝ `C221` `C222` `C223`／§7 増補＝ `C224`–`C226`
**Facts:** `episodes/_planning/EP63_correa_FACTS_LEDGER.v001.md` ／ **Script:** `episodes/_planning/EP63_correa_script.en.v002.md`

ステータス: 設計。**Codexアプリで下のヒーローアートを4枚とも生成→オーナーが1枚選択→Remotion `<Still>` でヘッドラインを重ねて 1280×720 書き出し。**
**アート保存先**: `H:\pd-media\assets\ai\correa\` にファイル名 `C221.png` `C222.png` `C223.png` `C227.png`（発注書 §3 と同じ場所・同じ規則）。
**書き出し先**: `episodes/PD-2026-063-correa/10_thumbnail/thumb-01.png` … `thumb-04.png`、採用1枚を `09_package/thumbnail.selected.v001.png` にコピー。

> **アートに文字を焼かない。**ヘッドラインは Remotion で合成する（発注書 §1 と `forbidden_subjects`「readable text, numerals, signage, logos, seals or emblems in any generated image」）。
> **数字「47」はタイポ層だけが持つ。**紙は白紙のまま。これは制約ではなくこの映画の設計（FILM_BIBLE §3）。
> **実在人物の肖像なし。**顔は1枚も出さない（不変条件11・`forbidden_subjects`・Q-13）。

---

## 0. この話でいちばん危ないのはタイトルである

`episode_spec.v001.json` の `forbidden_claims` が禁じているもののうち、**サムネとタイトルで踏みやすい順**に4つ：

| # | 禁止 | なぜサムネで踏むか |
|---|---|---|
| 1 | **「病院の遅延が彼女を殺した」／「診てもらえていれば助かった」** | 死は最も強いフックに見える。**契約は これを「THE SINGLE MOST LIKELY FACTUAL FAILURE IN THIS EPISODE」と名指ししている。** 死因は hypovolemic shock、**別の施設で、医師の管理下で**起きた（CR-24・Q-03） |
| 2 | **「病院は彼女を追い返した」** | 「追い返された」は定型のサムネ文法。**追い返していない**（CR-15・Q-01） |
| 3 | **「保険を理由に治療を拒んだ」** | カードを検めた事実が動機の物語を誘う。**動機は認定されていない**（CR-18 は *suggesting* 止まり・Q-02） |
| 4 | **「EMTALA は救急治療を保証する」** | 「あなたにはこの権利がある」型のタイトルが自動的にここへ行く。保証するのは *screening* と、緊急状態が見つかった場合の *stabilisation* だけ（Q-10・AS-07） |

**正直な好奇心フックは、死ではなく「誰も何も断っていない」ことである。**
`AS-17` — *EMTALA should be read to proscribe both actual and constructive dumping of patients.* —
病院は一度も No と言っていない。**それがこの事件の弁護ではなく、この事件そのものである。**
下のタイトルとヘッドラインは全部その一点の上に組んであり、**死・追い返し・保険・保証を一語も含まない。**

---

## 1. タイトル（A/B テスト用・英語・全て60字以内・フック先頭）

行13 = 「Title ≤ 60 chars, hook first ／ **≥2 A/B variants** ／ promise-payoff = true」。**4組8本**を用意する。
`char` は実測（空白込み）。**promise** 列は、本編のどこがその約束を回収するかである（払われない約束は出さない）。

| 組 | 版 | タイトル | char | promise を回収する本編の位置 |
|---|---|---|---|---|
| **A** | A1 | `She Was Handed Number 47. Nobody Ever Called It` | 47 | HOOK L30 ／ ACT_1 L62 ／ ENDING L412「Forty-seven was never called.」 |
| **A** | A2 | `They Gave Her Number 47 And Never Called It` | 43 | 同上 |
| **B** | B1 | `Nobody Refused Her Anything. A Jury Gave $700,000` | 49 | OP L40 ／ ACT_2 L123–125（$200,000＋$500,000）／ ACT_5 L383 |
| **B** | B2 | `She Waited Two Hours. Her Family Won $700,000` | 45 | ACT_1 L76（2〜2.5時間）／ ACT_2 L123–125 |
| **C** | C1 | `The Hospital Never Said No. That Was The Problem` | 48 | ACT_4 L300–317（constructive dumping）／ ENDING L409 |
| **C** | C2 | `No One Turned Her Away. No One Looked At Her` | 44 | ACT_1 L80 ／ ACT_3 L249–251 ／ ACT_4 L272 |
| **D** | D1 | `Two Hours In The ER. No Doctor. No Record.` | 42 | ACT_1 L76「No physician saw her.」／ ACT_3 L245–247 |
| **D** | D2 | `The Hospital Had No Record She Was Ever There` | 45 | ACT_3 L241「utter inability to produce any records」／ L247 |

**事実の裏取り（全てレジャーの ✓ 行）**

- `47` / `24` = CR-09 / CR-11。**「47番が呼ばれなかった」は判決文から出る**（47を渡され、退出時に24が呼ばれていた）。
- `$700,000` = PR-10＋PR-11＝PR-12。**陪審が評決し、控訴審は1ドルも減らしていない**（DM-19・CT-09）。「A Jury Gave」と書くのは、court ではなく jury が決めたからである（Q-08 の混同を避ける）。
- `Two Hours` = TL-12（**算術のみ。これ以上細かい数字を出さない**）。
- `No Doctor` = CR-14「No physician saw her」。`No Record` = AS-11「utter inability to produce any records」。
- **B2 が「Her Family Won」であって「She Won」でないのは**、$500,000 が遺族自身の損害で、$200,000 も *payable to the heirs* だからである（PR-10・PR-11）。

**使ってはいけないタイトル（実例・書きたくなるので先に潰す）**

| ✗ 書かない | 理由 |
|---|---|
| `She Died Waiting In The ER` | Q-03。死は別施設で医師の管理下。**待機と死を因果で結ぶ** |
| `The ER That Let Her Die` | Q-03 |
| `They Turned Her Away Over Her Insurance` | Q-01＋Q-02。二重に禁止 |
| `Your ER Cannot Legally Refuse You` | Q-10。EMTALA は治療を保証しない |
| `The Court Ruled They Dumped Her` | Q-08。**陪審が screening 違反を認定し、控訴審はそれを unimpugnable と述べた。**別の文である |
| `Every US Hospital Must Treat You` | Q-12。**ninety-nine は ninety-nine のまま** |

---

## 2. ヘッドライン（合成タイプ層・UPPERCASE・4語以内）

行12 = 「UPPERCASE headline ≤ 3–4 words（auto-split）· one emotional/curiosity idea · huge subject · very high contrast · black/navy bg + **gold `#E5B53A` or electric `#1F6BFF`** + white/silver text · readable at 320 px」。

| 版 | プレート | ヘッドライン | 語数 | キッカー（小さい方） | アクセント | 組み合わせるタイトル |
|---|---|---|---|---|---|---|
| **V1** | `C221` 手の中の白紙の整理券 | **`NOBODY CALLED 47`** | 3 | `SHE WAITED TWO HOURS` | gold `#E5B53A` | **A1 / A2** |
| **V2** | `C222` 空席の列 | **`SHE WAS NEVER REFUSED`** | 4 | `A JURY GAVE $700,000` | electric `#1F6BFF` | **B1 / B2** |
| **V3** | `C223` 何も出ていない番号表示 | **`NOBODY SAID NO`** | 3 | `THAT WAS THE VIOLATION` | gold `#E5B53A` | **C1 / C2** |
| **V4** | `C227` **どこにも無い**（記録の不在） | **`NO RECORD AT ALL`** | 4 | `TWO HOURS IN THE ER` | electric `#1F6BFF` | **D1 / D2** |

- **1枚につきブランドアクセントは1色だけ。**gold と electric を同じ絵に同居させない（`KidsForCashThumbnails.tsx` / `RolinThumbnails.tsx` の実装済みハウススタイルと同一）。
- 地は `BRAND.color.ink` / `BRAND.color.navy`、文字は white/silver＋**全グリフに極太の黒ストローク**。
- **`47` と `$700,000` はタイプ層にだけ出る。**生成アートには数字を一切焼かない（§0 の注記・`forbidden_subjects`）。
- `NOBODY CALLED 47` の `47` は数字1つ。**「FORTY-SEVEN」と綴らない**——320px で読ませるには字数が多すぎる。
- V3 のキッカー `THAT WAS THE VIOLATION` は **陪審が認定した screening 違反**を指す。*dumping* の語をタイプ層に置かない（Q-08）。

---

## 3. ヒーローアート4案（各1枚・文字は入れない＝Remotion側で重ねる）

`C221`–`C223` は **発注書 §5「THUMB（3枚）」で既に発注済み**。**文言は一字も変えない**（§0「1プロンプト＝1枚」・作り直しは1枚1回まで）。
`C227` は**この文書で新規に足す4枚目**で、`episode_spec.v001.json` の `mandatory_stills` 末尾（`C226` の次）に続く**未使用の最小 ID** である。

### 既発注（発注書 §5 のまま・再掲）

- `C221.png` — **ヘッドライン `NOBODY CALLED 47`**
  A blank paper ticket held up close in a hand, dead centre in the frame, hard directional light and deep shadow behind it, the composition leaving the upper third of the frame clear for a headline [STYLE] Avoid: [NEG]
- `C222.png` — **ヘッドライン `SHE WAS NEVER REFUSED`**
  One empty chair in a row of empty waiting chairs, shot dead centre and low, strong side light raking across the seats, upper third of the frame clear [STYLE] Avoid: [NEG]
- `C223.png` — **ヘッドライン `NOBODY SAID NO`**
  A dark blank display panel on a painted wall, dead centre, hard raking light across the wall texture, upper third of the frame clear [STYLE] Avoid: [NEG]

### 新規（4枚目・`C227`）

> ⚠ **発注を実行する担当者へ：この1枚は `EP63_correa_CODEX_BATCH_A.v001.md` §7 の表と一覧に追記してから流すこと。**
> §7 は現在 `C224`–`C226` で終わっている。追記する行はこれである：
> `| C227 | THUMB 4枚目（サムネ候補・本編では未使用可） | 状態6「どこにも無い」＝記録の不在。thumb_prompts.v001 §3 で追加 |`
> 追記しないと `mandatory_stills` の再導出と発注書が食い違う（spec notes が明示的に警告している失敗モード）。

- `C227.png` — **ヘッドライン `NO RECORD AT ALL`**
  A shallow wooden filing drawer pulled fully open on a painted metal cabinet and completely empty inside, the bare board of its base showing, the runners and the dust line where files used to stand still visible, one hard shaft of daylight falling squarely into the open drawer so the inside of it is the brightest thing in the frame, shot square on and close, dead centre in the frame, upper third of the frame clear for a headline [STYLE] Avoid: [NEG]

**`C227` が「記録の不在」でなければならない理由**：FILM_BIBLE §3 の**状態6が映画の心臓**であり、ACT_3 の中盤反転（`There was no record. Not a thin record. None.`）がそこに立っている。
そして `Q-14`——**偽の診療記録・受付票・カルテを「本物として」生成することは禁止**。**不在を映す。偽造を映さない。**空の引き出しは、その禁止を守ったまま同じことを言う唯一の絵である。

### `[STYLE]` / `[NEG]`（発注書 §2 のまま・展開してから生成する）

`[STYLE]` と `[NEG]` は `EP63_correa_CODEX_BATCH_A.v001.md` §2 の文字列をそのまま連結する。**この4枚も例外ではない。**

### ⚠ THUMB だけの明るさ上乗せ（`thumbnail_visibility` 対策・**必ず読む**）

本編の `[STYLE]` は *muted desaturated colour, low contrast, low-key* である。**この指定のままサムネを作ると輝度ゲートで落ちる。**
`C221`–`C223` の文言はさらに *deep shadow* / *dark blank display panel* と言っており、**素で作れば mean luma が 33 を割る絵になる。**
したがって **THUMB の4枚に限り**、`[STYLE]` の後ろに次の一句を足して生成する（**本編プレートには足さない**）：

> `, the subject itself brightly and evenly lit and clearly the brightest thing in the frame, the background dark but never crushed and still holding visible detail, high local contrast between the subject and the ground, graded up for legibility on a phone screen at 320 pixels wide`

これでも足りない場合は **Remotion 側で持ち上げる**（`KidsForCashThumbnails.tsx` の実績パターン——ヒーローを明るくグレードし、輝度を足すアクセント面を置き、**ヘッドラインを載せる側の1/3だけをスクリム**する）。**アートを作り直す前に、まず測る**（§5）。

---

## 4. 生成後の目視チェック（1枚ずつ・発注書 §1 Q1–Q9 に加えて）

1. **文字・数字が1文字も写っていないか**を拡大して見る。整理券・表示パネル・引き出しのラベルは**特に**見る（`forbidden_subjects`）。
2. **顔が1つも無いか。**手・後ろ姿・影のみ（不変条件11・Q-13）。
3. **上1/3が空いているか**（ヘッドラインの居場所）。
4. **320px に縮めて、主題が何か分かるか。**分からなければ主題が小さすぎる（行12「huge subject」）。
5. **`C227` が「空の引き出し」であって「書類の入った引き出し」ではないか。**中身が1枚でも写っていたら Q-14 側に倒れる。作り直す。
6. 長辺 **3840px 以上**・16:9・PNG（行5・発注書 §3）。

---

## 5. 書き出しと検証（**自己申告禁止・必ずコマンドで測る**）

### 5.1 合成して 1280×720 で書き出す

`remotion/src/compositions/CorreaThumbnails.tsx` を `KidsForCashThumbnails.tsx` と**同一構造**で作り（ハウススタイルを fork しない・不変条件14）、`Root.tsx` に `<Still>` を4本登録する。

```
<Still id="Thumb-correa-01" component={CorreaThumbnail} width={1280} height={720} defaultProps={{concept: CORREA_THUMBS[0]}} />
```

```bash
npx remotion still remotion/src/index.ts Thumb-correa-01 episodes/PD-2026-063-correa/10_thumbnail/thumb-01.png
npx remotion still remotion/src/index.ts Thumb-correa-02 episodes/PD-2026-063-correa/10_thumbnail/thumb-02.png
npx remotion still remotion/src/index.ts Thumb-correa-03 episodes/PD-2026-063-correa/10_thumbnail/thumb-03.png
npx remotion still remotion/src/index.ts Thumb-correa-04 episodes/PD-2026-063-correa/10_thumbnail/thumb-04.png
```

### 5.2 ゲートの実数（`scripts/check_final_acceptance.py` が実ファイルを測る値）

| ゲート | 何を見るか | 合格条件 |
|---|---|---|
| `thumbnail_ready`（行11） | `10_thumbnail/*.png` ＋ `09_package/thumbnail*.png` | **1280×720 の PNG が3枚以上**、かつ `09_package/thumbnail.selected*.png` が1枚存在 |
| **`thumbnail_visibility`（行12）** | **採用した1枚だけ**（`09_package/thumbnail.selected*.png` の最新） | **mean luma ≥ 33.0**（0–255）／ luma stddev ≥ 40.0 |
| `packaging`（行13・現状 manual） | タイトル | **≤60字・フック先頭・A/B 2組以上**（§1 で8本・4組） |

> **`thumbnail_visibility` は採用した1枚にしか効かない。**候補が明るくても、**選んだ1枚が暗ければ落ちる。**
> **ほぼ黒のフレームは不合格である。**校正実測（2026-07-04）＝却下された暗い v001 は mean **24.9–29.5**、承認された v002 は **36.4–48.0**。
> この話の `[STYLE]` は low-key なので、**4枚とも素では 33 を割る前提で作る**（§3 の明るさ上乗せ）。

### 5.3 選ぶ前に測る（`feedback_measure_before_explaining`）

4枚を書き出したら、**選ぶ前に**全部の実数を出す。暗い順に落とす。

```bash
./.venv/Scripts/python.exe -c "from PIL import Image, ImageStat; import glob; [print(p, *[round(v,1) for v in (ImageStat.Stat(Image.open(p).convert('L')).mean[0], ImageStat.Stat(Image.open(p).convert('L')).stddev[0])]) for p in sorted(glob.glob('episodes/PD-2026-063-correa/10_thumbnail/*.png'))]"
```

採用1枚を `09_package/thumbnail.selected.v001.png` にコピーしてから：

```bash
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 63 --json
```

`thumbnail_ready` と `thumbnail_visibility` が `ok: true` になるまで、**サムネを「できた」と言わない。**

---

## 6. 下流への申し送り

- **`C227` を発注書 §7 に追記する**（§3 の枠内に追記行の文面がある）。追記者はこの文書の作成者ではない。
- `episode_spec.v001.json` の `mandatory_stills` は現在 `C001`–`C226`。**`C227` はサムネ専用で本編ビートを持たない**ため、`mandatory_stills` に足すと `check_spec_satisfied.py` が「カットに出てこない」と正しく落とす。**足さないこと。**発注書 §7 にだけ載せる。
- タイトルとサムネの最終確定は**オーナーゲート**である（CLAUDE.md §3「title/thumbnail approval」・`.claude/rules/16-approval-boundaries.md`）。この文書は候補を出すところまでで止まる。

*v001 · 2026-08-04 · 参照モデル `episodes/PD-2026-009-timbs/04_scenes/thumb_prompts.v001.md`*
