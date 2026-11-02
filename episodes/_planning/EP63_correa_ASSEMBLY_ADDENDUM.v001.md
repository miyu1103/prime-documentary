# EP63 correa — 組み立て側へ・緊急追補 v001

**2026-08-05 · 設計スレッドから** · 対象: `PD-2026-063-correa` / *Correa v. Hospital San Francisco*, 69 F.3d 1184 (1st Cir. 1995)
**本書は `EP63_correa_ASSEMBLY_HANDOFF.v001.md` に優先する。**矛盾があれば本書が正。

---

## 0. 一行

**画像は227枚そろい、配置も済んだ。ただしモチーフの連鎖が壊れている。**
`C207` `C208` を差し替え発注した（**2枚がまだ生成されていない**）。
それ以外は**今すぐ組み立てに進める**。

---

## 1. 何が壊れていたか（目視で確認した事実）

この映画のモチーフは「**一つの物の八つの状態**」——受付で渡される**無地の整理券**である。
台本 L15 の MOTIF ロックがそう宣言している。

その連鎖を1枚ずつ開いた。**状態4と状態7の「同じ座席」が、3枚とも別の椅子だった。**

| プレート | 指定 | 生成されたもの |
|---|---|---|
| `C136` 状態4 | その座席に整理券が face-up | **茶色レザーの肘なし側椅子**・目線。券は無地の長方形 |
| `C207` 状態7 | **同じ座席を真上から**、券あり | **オリーブ色の成形プラ椅子**。しかも券が**切り込み入りの映画チケット**に変わっている |
| `C208` 状態7完了 | **同じ座席を真上から**、券が消えている | **緑のビニール肘掛け椅子**・目線の引き。**真上ですらない** |

つまり **状態7が完成せず、ループの落ちが画として存在しない。**
EP62 の `G226` とまったく同じ失敗である。

### 原因は発注側にある（設計ミス）

`C207` / `C208` の本文が「**the same seat**」としか書いていなかった。
Codex は **1プロンプト＝1枚**で走るので、**前の枚を参照できない**。
「同じ座席」は、毎回その椅子の特徴を全部書き下ろさない限り成立しない。券も同じで、
「切符」とだけ書けば映画チケットが出てくる。

再発注では **椅子（中世紀の待合用側椅子・肘なし・暗い赤褐色のレザーレット・前縁が擦れて色が抜けている・
細い黒スチール四脚・灰色テラゾー床・背後の壁は淡緑の腰壁）と、券（四辺が直線の無地クリーム色の紙片・
切り込みなし・ミシン目なし・印字なし）を毎回全文書いている。**

---

## 2. 差し替え表（発注は `EP63_correa_CODEX_BATCH_A.v001.md` §「★再発注」に追記済み）

| 新 | 廃止 | 役 |
|---|---|---|
| `C228` | `C207` | 状態7。同じ座席を真上から、券あり |
| `C229` | `C208` | 状態7完了・**映画の落ち**。同じ座席を真上から、券が消えている |

`C136` は良いので残し、**その椅子を正典**とした。`C228` `C229` はその椅子でなければならない。

**生成後に必ず並べて見ること**：`C136` → `C228` → `C229` の3枚が、
**同じ一脚の椅子・同じ券**に見えるか。ここが今回の全部である。
`C229` は**券がどこにも無い**こと（「消えたあと」であって「まだ在る」ではない）。

### 差し替えていないが弱い1枚

`C099`（状態2・同じ券が扇に広げられている）は、廃墟のような廊下の引きの中で
小さく放射状に並んでおり、**装飾模様に見える**。使えなくはないが弱い。
差し替えは判断に委ねる。

---

## 3. いまの本当の状態（数字で）

| | 状態 | 実測 |
|---|---|---|
| 契約 `episode_spec.v001.json` | ✅ valid | 27–32分 / 5,100–5,600語 / 8区分 / 13–17 beats / distinct_video 234 / people 10 / **mandatory_stills 223** |
| 台本 `EP63_correa_script.en.v002.md` | ✅ ゲート全緑 | **5,306語**・409行。`check_script_length` PASS / `check_script_craft` PASS（全項目緑） |
| state | **`script_review`** | **`script_verified` ではない。** R15（音読）が未実施のため |
| プレート発注 | 229枚 | `C001`–`C229`・欠番なし・重複なし |
| プレート生成 | **227枚** | `C228` `C229` のみ未生成 |
| 配置 `remotion/public/correa/img` | **225枚** | 廃止2枚（`C207` `C208`）は外してある |
| beats | ⚠ **v001 は台本より古い** | §5 を読むこと |
| 実写素材 | 8/54 accepted | 46本却下（43本は目視、3本は `scan_video_shape`） |

---

## 4. ファイル一覧（全部存在を確認済み）

```
episodes/PD-2026-063-correa/episode_spec.v001.json          ← 数字はここだけが正
episodes/PD-2026-063-correa/manifest.json                   ← state=script_review / target 30分
episodes/PD-2026-063-correa/04_scenes/thumb_prompts.v001.md
episodes/PD-2026-063-correa/01_research/fact_recheck.v001.md
episodes/_planning/EP63_correa_script.en.v002.md            ← 台本（正典）
episodes/_planning/EP63_correa_FILM_BIBLE.v001.md
episodes/_planning/EP63_correa_FACTS_LEDGER.v001.md
episodes/_planning/EP63_correa_CODEX_BATCH_A.v001.md        ← 画像発注（末尾に★再発注）
episodes/_planning/EP63_correa_beats.v001.json              ← ⚠ 古い（§5）
episodes/_planning/EP63_correa_REREVIEW.v001.md
episodes/_planning/EP63_correa_ASSEMBLY_HANDOFF.v001.md     ← 本書が優先
episodes/_planning/measurements/EP63_correa_RAW.md          ← 引用の唯一の典拠
H:\pd-media\assets\ai\correa\C001.png … C227.png            ← 生成物（原本）
remotion/public/correa/img/                                 ← 配置済み225枚
```

---

## 5. beats について（重要）

`EP63_correa_beats.v001.json`（HOOK 4 / OP 3 / ACT_1 16 / ACT_2 17 / ACT_3 17 / ACT_4 17 / ACT_5 16 / ENDING 8）は
**台本の修正より前に書かれている**。EP62 で同じ状態の beats を作り直したところ、次が出た：

- **画面に焼かれる引用が5件、逐語でなかった**（1件は**別の判例**の文だった）
- 数字ラベルが1件、出典より広く言っていた
- 台本が言っていないことを主張するカードが12枚
- ENDING に、脚本規約が禁じる**出来事の年表**が入っていた
- **仕組みの罠**：`build_case_film_generic.py::build_figures` は beats に時刻を与えず区間を等分するだけなので、
  **配列の何番目にあるかが、そのまま何秒に出るか**になる。物語順に並べると数枠ずれて出る
- 同関数は **`figures[0]` と `figures[-1]` を AI開示カードで上書きする**。
  両端に本物のビートを置くと**永遠に描画されない**

**EP63 の beats も同じ作り直しを走らせている。** 完了すると `EP63_correa_beats.v002.json` が出る。
**v002 が出るまで beats を焼き込まないこと。**

---

## 6. 組み立て側がいま**できること**（2枚を待たない）

1. **ナレーション生成**（ElevenLabs `nPczCjzI2devNBz1zQrb` / `eleven_multilingual_v2`）。
   台本は確定していて、差し替えは**画像だけ。一語も台本を変えていない**。
2. **filmconfig の作成**（このエピソードにはまだ無い）。
3. **生成カット表**。プレートIDは `C228` `C229` を使う（`C207` `C208` ではない）。
4. **Remotion 合成と字幕。**

**⚠ 最優先の警告 — 声の速度を先に固定して、最初のナレーションを実測すること。**
`check_script_length` は緑だが、こう警告している：

> at the fast end of the measured pace (237.4 wpm, seen on williams/florence) this lands at **22.4 min** — under the floor.

契約の下限は27分である。**速い読みで回すと4分半足りない。**
声の速度を固定し、**最初のナレーションを書き出して実尺を測るまで、画像作業に何も確定させないこと。**

**やってはいけないこと：**

- `C207` `C208` を**カットに使わない**（配置からは外してある。原本は `H:` に残す）。
- `C221` `C222` `C223` `C227` を `mandatory_stills` に**足さない**。この4枚は THUMB で、
  本編のカットにならない。宣言すると `check_spec_satisfied.py` が
  「宣言された静止画がどのカットにも無い」で落ちる。現在223件で正しい。

---

## 7. 生成側（Codex）への発注

`episodes/_planning/EP63_correa_CODEX_BATCH_A.v001.md` の**末尾ブロック「★再発注」だけ**を回す。
**`C001`–`C227` は一語も触らず、再生成もしない**（廃止2枚は使わないだけで消さない＝
`.claude/rules/05-episode-artifacts.md`「stale artifact を削除せず再計算対象として示す」）。

- 出力先: `H:\pd-media\assets\ai\correa\C228.png` `C229.png`
- 長辺3840px以上・16:9・PNG
- 生成後に `remotion/public/correa/img/` へ配置（現在225枚 → 227枚）

生成後の検査：

1. `C136` `C228` `C229` を並べて、**同じ一脚の椅子**に見えるか。**ここが今回の全部。**
2. 券が**四辺直線の無地の紙片**か（切り込み・ミシン目・印字があれば不合格）。
3. `C229` に**券がどこにも無い**か。
4. 文字が1文字も無いか。
5. 顔が写っていないか。

---

## 8. まだ残っている未解決（正直に）

- **R15（音読）未実施。** 下読みTTSをオーナーが聴く工程がまだ無い。state が `script_review` のままなのはこれが理由。
- **`EP63_correa_beats.v002.json` がまだ無い**（§5）。
- **`filmconfig` がこのエピソードにはまだ無い。**
- **コンタクトシートが `C100` までしか作られていない。** `C101` 以降の127枚は、
  今回モチーフ連鎖を目視した数枚を除いて**誰も見ていない**。EP62 では全枚目視して13枚の欠陥が出た。
- 実写素材 8/54 accepted は契約の `distinct_video_assets` 234 に対して薄い。
  **静止画は distinct_video に数えられない**（動かして初めて数えられる）前提のままである。
- 引用監査で**出典不明はゼロ**だったが、L365 に1件、`the court said` の枠内で
  語を落とした省略がある（`do not shock our collective conscience` ／原文は
  `do not shock **or even vellicate** our collective conscience`）。意図的な可能性が高いので触っていない。
- 台帳に無いが判決文には逐語で存在する引用が3件（L179・L197・L201）。監査記録の欠落であって事実の誤りではない。

---

## 9. 検算コマンド

```bash
cd C:/Users/aab15/Documents/prime-documentary
.venv/Scripts/python.exe scripts/check_episode_spec.py --slug correa
.venv/Scripts/python.exe scripts/check_episode_inputs.py --slug correa
.venv/Scripts/python.exe scripts/check_script_length.py episodes/_planning/EP63_correa_script.en.v002.md --lo 1620 --hi 1920
.venv/Scripts/python.exe scripts/check_script_craft.py episodes/_planning/EP63_correa_script.en.v002.md --words 5100 5600
```

プレート数（発注ファイル側）:

```bash
.venv/Scripts/python.exe -c "import re,pathlib;t=pathlib.Path('episodes/_planning/EP63_correa_CODEX_BATCH_A.v001.md').read_text(encoding='utf-8');i=re.findall(r'^- .(C\d{3})\.png.\s*$',t,re.M);print(len(i),len(set(i)),i[-1])"
```

期待値: `229 229 C229`
