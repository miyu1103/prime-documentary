# EP65 marmet — 組み立て側へ・追補 v001

**2026-08-05 · 設計スレッドから** · 対象: `PD-2026-065-marmet` / *Marmet Health Care Center v. Brown*, 565 U.S. 530 (2012) ＋ 差戻後の *Brown II*
**本書は `EP65_marmet_ASSEMBLY_HANDOFF.v001.md` に優先する。**矛盾があれば本書が正。

---

## 0. 一行

**画像224枚生成・222枚配置済み。台本ゲート全緑。beats は v002 が正典。**
**ループの2枚（`R225` `R226`）だけが未生成。**それ以外は今すぐ組み立てに進める。

---

## 1. ループが壊れていたので作り直した（目視と実測の結果）

この映画のモチーフは **罫線**である。状態1（ACT_1 冒頭の空の罫線）が、状態7（最後の画の空の罫線）として戻ってくることでループが閉じる。台本 L5 のロックがそう宣言している。

| プレート | 指定 | 生成されたもの |
|---|---|---|
| `R222` 状態1 | 受付カウンターを来訪者側から。奥に2脚の椅子（手前は引き出され、奥は角に押し込まれたまま）。カウンター上の用紙に**罫線**が見えること | **暗く引きすぎて罫線が読めない。** 部屋も家庭的で、椅子は暗い張り椅子 |
| `R223` 状態7 | **同じ目・同じカウンター・同じ奥の椅子**。罫線は裸でペンが無い | 画そのものは良い（罫線が裸・ペンが無い）。しかし**部屋も椅子も別物**（`R222` との相関 **−0.233**） |

つまり台本が「**奥に押し込まれたままの、あの椅子**」と言うのに、**観客が一度も見ていない椅子**が戻ってくる。
そして**モチーフの一枚目でモチーフが判別できない**——状態1が存在しない。

**`R225` `R226` を対として発注し直した。** カウンター・2脚の椅子・光・罫線の特徴を**両方の本文に全文書き下ろしてある**。
原因は EP62・EP63 と同じで、**1プロンプト＝1枚では前の枚を参照できない**ため、「同じ椅子」は毎回書き下ろすしかない。

**生成後に必ず並べて見ること**：`R225` と `R226` が**同じ部屋・同じカウンター・同じ二脚の椅子**に見えるか。両方で**罫線が一目で読める**か。ここが今回の全部である。

**`R222` `R223` は廃止。**配置からも外してある（原本は `H:` に残す）。

### 私の見誤りを1件訂正

`R035` を「短剣に見える」と疑ったが、拡大すると**バインダーのリングに挟まったボールペン**で指定どおりだった。縮小表示で判断したのが誤り。**縮小で defect を判定しないこと。**

---

## 2. いまの本当の状態（数字で）

| | 状態 | 実測 |
|---|---|---|
| 契約 `episode_spec.v001.json` | ✅ valid | 27–32分 / 5,100–5,600語 / 8区分 / 13–17 beats / distinct_video 234 / people 10 / **mandatory_stills 220** / forbidden_subjects 10 |
| 台本 `EP65_marmet_script.en.v002.md` | ✅ ゲート全緑 | **5,235語**・374行 |
| state | **`script_review`** | R15（音読）未実施 |
| プレート発注 | 226枚 | `R001`–`R226`・欠番なし |
| プレート生成 | **224枚** | `R225` `R226` のみ未生成 |
| 配置 | **222枚** | 廃止2枚（`R222` `R223`）は外してある |
| beats | ✅ **`EP65_marmet_beats.v002.json`** | 102個（HOOK 3 / OP 4 / ACT_1–5 各17 / ENDING 10）。**v001 は使わない** |
| filmconfig | ❌ **未作成** | |
| 実写素材 | 11/57 accepted | |

---

## 3. beats は v002 を使うこと（v001 はそもそもビルドできない）

**`EP65_marmet_beats.v001.json` は最初のHOOKビートでビルドが落ちる。**
`build_case_film_generic.py` は `dochighlight` を明示的に禁止しており、v001 はこれを6箇所＋`brightline` 1箇所使っている。
にもかかわらず `set_figure_beats.py --dry-run` は「97 beat(s) valid」と答えていた——**検証していたのがレンダラの38種で、ビルダーの18種ではなかった**からである。
**ゲート側を修正済み**（ビルダーの許可リストを直接読む）。実際に落ちることを確認してから採用した。

引用も **10件を訂正**した。焼かれる予定だったもののうち重いもの：

| v001 | 原文 |
|---|---|
| `State and federal courts must enforce the Federal Arbitration Act **with respect to**…` | `…the Federal Arbitration Act **(FAA), 9 U. S. C. §1 et seq.,** with respect to…` — **法令引用を省略記号なしで落としていた** |
| `Finding that there is an adhesion contract…not the end of it.` — **Brown I (2011)** | 実際は ***State ex rel. Dunlap v. Berger* (2002)**（Brown II 脚注36）。**別の判例** |
| `It may be disingenuous…` — **Brown I (2011)** | **Brown II (2012) 自身の地の文** |
| `On remand,…principles that are not specific to arbitration.` | `…not specific to arbitration **and pre-empted by the FAA.**` — 次の行が指している尾を落としていた |
| `Substantive unconscionability may manifest itself…` — Brown II | 内側の引用は ***Mercuro v. Superior Court***（脚注38）で、Brown II の言葉ではない |
| `…modicum of bilaterality…` — Brown II | ***Abramson v. Juniper Networks***（脚注40） |

**根拠のない数字を1件削除**：`100 : 1` の棒グラフ。台帳に支えが無く、しかも台本の「a few times in life」と矛盾していた。

**この映画の中心の一文にカードが1枚も無かった。** *"…all disputes, other than claims to collect late payments owed by the patient."* ——`forbidden_claims` の中心でもあるこの句が画面に出ていなかったので、v002 で追加した。

**`figures[-1]` の罠**：v001 は末尾に**この映画の締めの一撃 `OTHER THAN.`** を置いていた。`build_figures` が AI開示カードで上書きする枠なので、**永遠に画面に出ない**。

### UNVERIFIABLE として明示したもの

**Brown I（228 W. Va. 646 (2011)）が手元のコーパスに無い。** Brown I 帰属の引用5件は、**「Brown II が Brown I として引用している文字列」としてのみ**検証されている。Brown I 本体との照合はしていない。**入手できたら再照合すること。**

---

## 4. 組み立て側の作業（順番に）

1. **ナレーション生成**（ElevenLabs `nPczCjzI2devNBz1zQrb` / `eleven_multilingual_v2`）。台本は確定していて、`R225`/`R226` の差し替えで**一語も変えていない**
2. **filmconfig の作成**
3. **beats を焼き込む**（`EP65_marmet_beats.v002.json`）：
   ```
   .venv/Scripts/python.exe scripts/set_figure_beats.py \
     --config episodes/_planning/EP65_marmet_filmconfig.v001.json \
     --beats  episodes/_planning/EP65_marmet_beats.v002.json \
     --min-per-act 13
   ```
4. **生成カット表 → Remotion 合成 → 字幕**

### ⚠ 最優先の警告 — この話が4本中いちばん短く落ちる

`check_script_length` は緑だが：

> at the fast end of the measured pace (237.4 wpm) this lands at **22.1 min** — under the floor.

契約の下限は27分。**速い読みだと5分足りない。**声の速度を固定し、**最初のナレーションを書き出して実尺を測るまで、画像作業を確定させないこと。**

### この話に固有の拘束

- **`[STYLE]` が low contrast / low-key** で、サムネの輝度ゲート（平均33以上）と正面から衝突する。
  **THUMB 4枚（`R217` `R218` `R219` `R224`）は上書き指定を持っている。ハウススタイルに「戻さない」こと。**
- **書かれた名前を表す語を、発注本文でもテロップでも使わない。** 視覚的には**署名を描かない**——モチーフの一筆は**判読できない痕**であって、名前ではない
- **医療機器・点滴・モニタを介護施設のプレートに出さない。車椅子を広告調に演出しない**（`forbidden_subjects`）
- **この映画の主張は「最高裁が何を決めなかったか」である。** 判示を広く言うカードは様式ではなく**事実の誤り**として扱う

### やってはいけないこと

- `EP65_marmet_beats.v001.json` を焼き込まない（**ビルドが落ちる**）
- `R222` `R223` をカットに使わない
- `R217` `R218` `R219` `R224` を `mandatory_stills` に足さない。**220件で正しい**

---

## 5. ファイル一覧（全部存在を確認済み）

```
episodes/PD-2026-065-marmet/episode_spec.v001.json          ← 数字はここだけが正
episodes/PD-2026-065-marmet/manifest.json                   ← state=script_review / target 30分
episodes/PD-2026-065-marmet/04_scenes/thumb_prompts.v001.md
episodes/_planning/EP65_marmet_script.en.v002.md            ← 台本（正典）
episodes/_planning/EP65_marmet_FILM_BIBLE.v001.md
episodes/_planning/EP65_marmet_FACTS_LEDGER.v001.md
episodes/_planning/EP65_marmet_CODEX_BATCH_A.v001.md        ← 画像発注（末尾に★再発注 R225/R226）
episodes/_planning/EP65_marmet_beats.v002.json              ← ★正典。v001 はビルドできない
episodes/_planning/EP65_marmet_REREVIEW.v001.md / .v002.md
episodes/_planning/EP65_marmet_ASSEMBLY_HANDOFF.v001.md     ← 本書が優先
episodes/_planning/measurements/EP65_marmet_RAW.md          ← Marmet (2012) 原文
episodes/_planning/measurements/EP65_brown_remand_RAW.md    ← Brown II (2012) 原文
H:\pd-media\assets\ai\marmet\R001.png … R224.png            ← 生成物（原本）
remotion/public/marmet/img/                                 ← 配置済み222枚
```

---

## 6. 生成側（Codex）への発注

`episodes/_planning/EP65_marmet_CODEX_BATCH_A.v001.md` の**末尾ブロック「★再発注」だけ**を回す。
**`R001`–`R224` は一語も触らず、再生成もしない**（廃止2枚は使わないだけで消さない）。

- 出力先: `H:\pd-media\assets\ai\marmet\R225.png` `R226.png`
- 長辺3840px以上・16:9・PNG
- 生成後に `remotion/public/marmet/img/` へ配置（222枚 → 224枚）

検査：`R225` と `R226` を並べて、**同じ部屋・同じカウンター・同じ二脚の椅子**に見えるか。**両方で罫線が一目で読める**か。`R226` に**ペンがどこにも無い**か。文字が1文字も無いか。

---

## 7. まだ残っている未解決（正直に）

- **R15（音読）未実施**
- **filmconfig が無い**
- **全枚目視QCが未完了。** 現在別プロセスで224枚を1枚ずつ見ている。結果は `runs/qc/marmet_plate_verdicts.v001.md`。**この話の `[STYLE]` は意図的に低照度**なので、携帯で真っ黒になる枚が多い可能性がある。**結果を待たずに画像を確定させないこと**
- **Brown I が未入手**（§3）
- 実写素材 11/57 accepted は契約 234 に対して薄い
- 再レビュー v002 の判定は **DOES NOT MEET IT**。指摘された render 影響のある4件は修正済みだが、**修正後の再レビューは走らせていない**

---

## 8. 検算コマンド

```bash
cd C:/Users/aab15/Documents/prime-documentary
.venv/Scripts/python.exe scripts/check_episode_spec.py --slug marmet
.venv/Scripts/python.exe scripts/check_episode_inputs.py --slug marmet
.venv/Scripts/python.exe scripts/check_script_length.py episodes/_planning/EP65_marmet_script.en.v002.md --lo 1620 --hi 1920
.venv/Scripts/python.exe scripts/check_script_craft.py  episodes/_planning/EP65_marmet_script.en.v002.md --words 5100 5600
```

プレート数（発注ファイル側）— 期待値 `226 226 R226`:

```bash
.venv/Scripts/python.exe -c "import re,pathlib;t=pathlib.Path('episodes/_planning/EP65_marmet_CODEX_BATCH_A.v001.md').read_text(encoding='utf-8');i=re.findall(r'^- .(R\d{3})\.png.\s*$',t,re.M);print(len(i),len(set(i)),i[-1])"
```
