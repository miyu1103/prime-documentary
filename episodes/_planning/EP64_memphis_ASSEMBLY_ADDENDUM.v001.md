# EP64 memphis — 組み立て側へ・追補 v001

**2026-08-05 · 設計スレッドから** · 対象: `PD-2026-064-memphis` / *Memphis Light, Gas & Water Div. v. Craft*, 436 U.S. 1 (1978)
**本書は `EP64_memphis_ASSEMBLY_HANDOFF.v001.md` に優先する。**矛盾があれば本書が正。

---

## 0. 一行

**画像219枚すべて生成・配置済み。台本のゲート全緑。beats は v002 が正典。**
**未生成のプレートはゼロ。**この話は4本のうち**いちばん先に進める状態**にある。

---

## 1. いまの本当の状態（数字で）

| | 状態 | 実測 |
|---|---|---|
| 契約 `episode_spec.v001.json` | ✅ valid | 27–32分 / 5,100–5,600語 / 8区分 / 13–17 beats / distinct_video 234 / people 10 / **mandatory_stills 215** / forbidden_subjects 9 |
| 台本 `EP64_memphis_script.en.v002.md` | ✅ ゲート全緑 | **5,474語**・435行。`check_script_length` PASS / `check_script_craft` PASS |
| state | **`script_review`** | **`script_verified` ではない。** R15（音読）が未実施のため |
| プレート | **219/219 生成・219枚配置** | `M001`–`M219`・欠番なし・重複なし・全て3840×2160 |
| beats | ✅ **`EP64_memphis_beats.v002.json`** | 101個（HOOK 3 / OP 4 / ACT_1–5 各17 / ENDING 9）。**v001 は使わない** |
| filmconfig | ❌ **未作成** | 組み立て側の最初の仕事 |
| 実写素材 | 16/81 accepted | |

---

## 2. beats は v002 を使うこと（v001 は使わない）

`EP64_memphis_beats.v001.json` を全数照合したところ、**画面に焼かれる予定だった文字列に欠陥が出た**。

**引用26本中21本は逐語で正しかった。**捏造文字列は0件。壊れていたのは以下：

| 場所 | v001（焼かれる予定だったもの） | 判決文の実際 |
|---|---|---|
| 反対意見の譲歩 | `…entitlement to continued utility services` で切る | `…continued utility services **as long as the undisputed portions of his utility bills are paid.**` — **条件節を落とすと譲歩でなくなる** |
| 脚注22 | `…structuring of this hearing` | `…structuring of this "hearing," **provided that the customer is afforded adequate time for effective presentation of his complaint prior to termination.**` — **保護規定ごと切断** |
| 脚注7 | `…combine the two accounts properly**.**` | 原文は `properly (A. 146-150), or that,…` と続く。**途中で切って句点を打ち、完結文に見せていた** |
| 控訴審 | `**The** MLG&W notice only **warned**…` | `the MLG&W notice only **warn[ed]**…` — **編集括弧を黙って解消し文頭を大文字化** |

**帰属の誤りが4件。**うち1件は EP62 とまったく同型で、**最高裁が地裁を要約した地の文**が「地裁自身の認定」として出るところだった。他に *Wolff v. McDonnell* の文が最高裁の言葉に、*Mullane* の事件名が `Bank & Trust` 表記の誤り（正しくは `Trust Co.`）、*Trigg* の判示が「テネシー州法」に。

**事実として誤っていた図版：**

- **ENDING の年表カード** — `PD_SCREENPLAY_STANDARD` §12 が正面から禁じる「出来事の要約」。**加えて日付も誤り**で、第六巡回区の判決は **1976年**（534 F. 2d 684）、1977年2月22日は**上告受理の日**である
- **`THE COURT FOUND THE NOTICE INADEQUATE`** — 地裁が認めたのは「異議手続についての告知」の不足。反対意見は *"The District Court did not find that the Division's notice was defective in any respect"* と**明示的に否定している**
- **HOOK `HAD PAID THE BILL`** — 判決文は `paid **a** bill`。定冠詞は ⛔-02 の線を越える
- **棒グラフが「40（％）対 0（件）」** — 単位の違う二数を同じ軸に置いていた

### 仕組みの罠（両方とも設計文書に書かれていなかった）

1. **`build_figures` は beats に時刻を与えない。** 区間を等分に割るだけなので、**配列の何番目にあるかが、そのまま何秒に出るか**になる。v001 は語りの順では正しかったが密度が前半に偏っており、ACT_1 は最初の28%に9枚ぶんの素材があって後半35%にはカードが1枚しかなかった。前半のカードは**最大で約66秒遅れて**出ていた。v002 は全区間を実測した語位置で置き直してある
2. **`build_figures` は `figures[0]` と `figures[-1]` を AI開示テロップで上書きする。** v001 は末尾に**この映画の締めの一撃 `NOTHING HERE SAYS THE BILL WAS WRONG` を置いていた**——**永遠に画面に出ない枠**である。v002 は両端に開示カードを明示配置している

### ゲート自体も壊れていたので直した

`set_figure_beats.py` はレンダラの38種で検証していたが、**実際のビルダーは18種しか受け付けない**。EP65 の beats v001 は最初のHOOKビートでビルドが落ちる代物なのに、ゲートは「97 beat(s) valid」と答えていた。**ビルダー側の許可リストを直接読むように修正済み**（実際に落ちることを確認してから採用）。

---

## 3. この話に固有の拘束

**⛔-08 オーナー裁定（2026-08-04）：名前は可・番地 `1019` は不可。**
ナレーション・テロップ・プレート・ショートの全部に及ぶ。`beats.v002.json` には `1019` は0件。

**メーターは「2個」ではなく「2組」。** 判決文は *two **sets** of meters*——ガス2・電気2の**計4個**である。
旧HOOKの「一つの壁に二つのメーター」は事実として誤りで、**HOOKは `M003` / `M048` / `M005` に作り直してある**。
`M001` `M002` `M004` は廃棄せず、ACT_1 と ACT_5 の通常カットに戻っている。
サムネのキッカーとショートのテロップも `TWO METER SETS` に訂正済み。

**台帳の件数は 123行 / 110 verbatim / 12隔離。** 以前どこかにあった 122/109/17 は**誰も数えていない数字**だったので訂正した。

**`ML-60` は台本に存在する**（L257・`grep -c` = 1）。引き継ぎ書 §6-1 が「記録なく消えた」としていたが、22:07 の修正で復元済みで、beats v002 の `ACT_4[2]` が語位置 0.147 でこれを担当する。

---

## 4. 組み立て側の作業（順番に）

1. **ナレーション生成**（ElevenLabs `nPczCjzI2devNBz1zQrb` / `eleven_multilingual_v2`）
2. **filmconfig の作成**（このエピソードにはまだ無い）
3. **beats を焼き込む** — `EP64_memphis_beats.v002.json` を使う：
   ```
   .venv/Scripts/python.exe scripts/set_figure_beats.py \
     --config episodes/_planning/EP64_memphis_filmconfig.v001.json \
     --beats  episodes/_planning/EP64_memphis_beats.v002.json \
     --min-per-act 13
   ```
4. **生成カット表 → Remotion 合成 → 字幕**

### ⚠ 最優先の警告 — 声の速度を先に固定して、最初のナレーションを実測すること

`check_script_length` は緑だが、こう警告している：

> at the fast end of the measured pace (237.4 wpm, seen on williams/florence) this lands at **23.0 min** — under the floor.

契約の下限は27分である。**速い読みで回すと4分足りない。**
声の速度を固定し、**最初のナレーションを書き出して実尺を測るまで、画像作業に何も確定させないこと。**

### やってはいけないこと

- `EP64_memphis_beats.v001.json` を焼き込まない（§2）
- `M208` `M209` `M210` `M219` を `mandatory_stills` に足さない。THUMB専用で本編のカットにならないため、宣言すると `check_spec_satisfied.py` が「宣言された静止画がどのカットにも無い」で落ちる。**215件で正しい**
- `1019` をどこにも出さない

---

## 5. ファイル一覧（全部存在を確認済み）

```
episodes/PD-2026-064-memphis/episode_spec.v001.json          ← 数字はここだけが正
episodes/PD-2026-064-memphis/manifest.json                   ← state=script_review / target 30分
episodes/PD-2026-064-memphis/04_scenes/thumb_prompts.v001.md
episodes/PD-2026-064-memphis/01_research/fact_recheck.v001.md
episodes/_planning/EP64_memphis_script.en.v002.md            ← 台本（正典）
episodes/_planning/EP64_memphis_FILM_BIBLE.v001.md
episodes/_planning/EP64_memphis_FACTS_LEDGER.v001.md         ← 123行/110 verbatim/12隔離
episodes/_planning/EP64_memphis_CODEX_BATCH_A.v001.md        ← 画像発注（219枚・追加発注なし）
episodes/_planning/EP64_memphis_beats.v002.json              ← ★正典。v001 は使わない
episodes/_planning/EP64_memphis_REREVIEW.v001.md
episodes/_planning/EP64_memphis_ASSEMBLY_HANDOFF.v001.md     ← 本書が優先
episodes/_planning/measurements/EP64_memphis_RAW.md          ← 引用の唯一の典拠
H:\pd-media\assets\ai\memphis\M001.png … M219.png            ← 生成物（原本）
remotion/public/memphis/img/                                 ← 配置済み219枚
```

---

## 6. まだ残っている未解決（正直に）

- **R15（音読）未実施。** state が `script_review` のままなのはこれが理由
- **filmconfig が無い**
- **全枚目視QCが未完了。** 現在別プロセスで219枚を1枚ずつ見ている。結果は `runs/qc/memphis_plate_verdicts.v001.md` に出る。**EP62 では全226枚を見て13枚の欠陥が出た**（年代違い・紙幣の文字・法廷に見える議場・輝度12.6・識別可能な顔）。**その結果を待たずに画像を確定させないこと**
- 実写素材 16/81 accepted は契約の `distinct_video_assets` 234 に対して薄い。**静止画は distinct_video に数えられない**（動かして初めて数えられる）前提のままである
- 短文比率が **33.2%**（帯域 20–35%）。上限まで1.8ポイントしかない。**組み立て中に短い行を足すと赤になる**
- 台帳に無いが判決文には逐語で存在する引用が数件ある（監査記録の欠落であって事実の誤りではない）

---

## 7. 検算コマンド

```bash
cd C:/Users/aab15/Documents/prime-documentary
.venv/Scripts/python.exe scripts/check_episode_spec.py --slug memphis
.venv/Scripts/python.exe scripts/check_episode_inputs.py --slug memphis
.venv/Scripts/python.exe scripts/check_script_length.py episodes/_planning/EP64_memphis_script.en.v002.md --lo 1620 --hi 1920
.venv/Scripts/python.exe scripts/check_script_craft.py  episodes/_planning/EP64_memphis_script.en.v002.md --words 5100 5600
```

プレート数（発注ファイル側）— 期待値 `219 219 M219`:

```bash
.venv/Scripts/python.exe -c "import re,pathlib;t=pathlib.Path('episodes/_planning/EP64_memphis_CODEX_BATCH_A.v001.md').read_text(encoding='utf-8');i=re.findall(r'^- .(M\d{3})\.png.\s*$',t,re.M);print(len(i),len(set(i)),i[-1])"
```
