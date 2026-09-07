# EP45 cleveland — Codex スレッドA「素材生成」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN）も実装スレッドB（CODEX_B）のファイルも**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> **唯一の外部真実 = `episodes/_planning/EP45_cleveland_PRODUCTION_SPEC.v001.json`**（機械生成）。本書の数値はそこから転記したものであり、手書きで発明していない。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP45 / Episode ID: PD-2026-045-cleveland / slug: cleveland
Composition id: Ep45Cleveland（B が Root.tsx に登録・A は staging まで）
事件:       Bearden v. Georgia (1983) と Harriet Cleveland（Montgomery, AL）。
            払えない罰金を理由とする投獄は Bearden(1983)以降 憲法違反（違法）。
            主題は「1983以降 違憲なのに実務で続いた（enforcement failure）」。
            Bearden＝最高裁の線。Cleveland の救済は下級審訴訟＋2014和解であって最高裁判決ではない。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**84本の固有プロンプト × 1枚 = 84枚**・バリエーション0） | `H:\pd-media\assets\ai\cleveland\S<NN>.png` | 2–3.5時間（GPU） |
| A-1b | i2v 種画像の生成（**16本の固有プロンプト × 1枚 = 16枚**・バリエーション0） | `H:\pd-media\assets\ai\cleveland\M<NN>_src.png` | 30–50分（GPU） |
| A-2 | 静止画のQCと目視（**目視必須**） | `05_visuals/still_qc.v001.json` + コンタクトシート | 1.5時間 |
| A-3 | depth map 生成（`treatment:"depth"` の必須入力） | `H:\pd-media\assets\ai\cleveland\S<NN>_depth.png` | 20分 |
| A-4 | factory 実写クリップ **92本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | **2.5時間（うち目視だけで1時間以上）** |
| A-5 | i2v モーション化 **16本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\cleveland\M<NN>_rife.mp4` | 7–19時間（GPU） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 | `05_stock/overlay_selection.v001.json` | 30分 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 20分 |
| A-8 | Remotion public への staging | `remotion/public/cleveland/{img,factory,motion,overlay}/` | 30分 |

> **★★ 最重要の前提（EP42/43/44 から継続）: 1シーン1枚・バリエーション0 ★★**
> Codex の画像生成は高精度。**同一ショットの複数バリエーション（`_02`/`_03`）を作らない。**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 84本＝84行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **`--variants 1`**（または variants 指定なし）で回す。**`--variants 3` は使わない。**
> **総生成画像 = still 84 + i2v 種 16 = 100枚（各1回）。** factory 92本は生成でなく在庫からの選抜。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-045-cleveland/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** Bはスタブで全パイプラインを完走できるので、Aの完了を待っていない。**A も急がなくてよいが途中経過を壊すな。** このマニフェストは **A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致**で共有する（§4）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\cleveland\**` / `H:\pd-media\assets\ai_video\cleveland\**` | **A** | 読み書き |
| `episodes/PD-2026-045-cleveland/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-045-cleveland/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/cleveland/{img,factory,motion,overlay}/**` | **A** | 読み書き |
| `episodes/PD-2026-045-cleveland/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_cleveland_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-044-*/**` および EP39〜44 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を `read_prompts()` で読む） | `PD-2026-045-cleveland --variants 1` / `45 --variants 1 --only S01` |
| `scripts/gen_depth_maps.py`（**既存**） | §6.4 の depth map | `--dir "H:/pd-media/assets/ai/cleveland"` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-045-cleveland --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit 96 --exclude-used --ep PD-2026-045-cleveland --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-045-cleveland` |

**★Aが新規作成するスクリプト（EP44 の tekoh 版を cleveland 用に複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（複製元・EP44） |
|---|---|---|
| `scripts/qc_cleveland_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_tekoh_stills.py` |
| `scripts/select_cleveland_factory.py` | §7 の factory 92本の確定選定・EP39〜44 sha256 除外検証 | `scripts/select_tekoh_factory.py` |
| `scripts/comfy_wan_cleveland.py` | §8 の i2v 16本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_tekoh.py` |
| `scripts/rife_cleveland.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_tekoh.py` |
| `scripts/build_cleveland_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_tekoh_asset_manifest.py` |
| `scripts/stage_cleveland_assets.py` | §10 の staging | `scripts/stage_tekoh_assets.py` |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある（`read_prompts()` で `04_scenes/ai_prompts.v001.md` を読む）。あなたは **`ai_prompts.v001.md` を §5.2 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない**（上の複製元が実在することを `ls scripts/` で確認してから複製する）。
> **正確性ゲートは `check_cleveland_facts.py`（B が実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の6制約に一致し、`check_cleveland_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_cleveland_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_cleveland_asset_manifest.py --reuse-feasibility
#   → still >=84 / motion >=16 / factory >=92 / distinct 合計 >=192 / first-use >=0.70

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_cleveland_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全92本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-045-cleveland
#   → exit 0（factory_clip_qc.v001.json が staging 済み全クリップを reviewed:true で網羅）

# [A-DONE-5] EP39/EP40/EP41/EP42/EP43/EP44 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_cleveland_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39・EP40・EP41・EP42・EP43・EP44 の六つすべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（R1 ＋ 正確性6制約）★★★

**払えない罰金を理由とする投獄は Bearden v. Georgia(1983)以降 憲法違反（違法）。本作は「合法だ」とは決して言わない。主題は「違憲なのに実務で続いた（enforcement failure）」。Bearden＝最高裁の線。Harriet Cleveland の救済は下級審の訴訟＋2014和解であって最高裁判決ではない。Bearden は罰金・手数料そのものを禁じてはいない（能力審査なしの収監だけを禁じた）。Harriet Cleveland は存命の私人（R2）で、顔・身体・肖像を一切出さない。象徴オブジェのみ。家族・子どもを扇情化しない（poverty porn 禁止）。**

## 1.1 R1（生成ビジュアル全般）

1. **実在人物の顔・likeness・肖像を作らない。** Harriet Cleveland（存命私人・R2）、Hub Harrington 判事、Sandra Day O'Connor、Bearden 本人を**顔・身体・肖像として描かない**。人物は原則「人を出さない」（象徴オブジェのみ）。判事評言の逐語引用は AE カード（B の担当）であって画像ではない。
2. **実在の判決文・判例番号・条文・日付・金額の可読文字を再現しない。** 督促状・免許証・支払台帳・請求書・和解書・意見書・カレンダーは雰囲気のみ（判読不能）。判例番号（461 U.S. 660 / 399 U.S. 235 / 401 U.S. 395）・日付・金額（$1,554 / 31 / $200 / $40）・人数（38,000 / 4 states）は**画像に描かない**（AE/figures のタイポで出す＝B の担当）。会社ロゴは**ぼかして判読不能**にする。
3. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性6制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **「合法(legal/lawful)」と書かない。** 払えないだけの投獄は Bearden(1983)以降 違憲（違法）。主題は "違法なのに実務で続く(enforcement failure)"。**「debtors' prison is legal / lawful to jail the poor」を書かない。** 同時に「もう完全に無くなった／どこでも廃止された(gone / abolished everywhere / no longer exists)」も誤りなので書かない。許容は "unconstitutional since 1983 yet it continued" / "the rule held" / "still stands" / "enforcement failure"。
2. **Bearden＝最高裁の線。Cleveland の救済は下級審訴訟＋2014和解であって最高裁判決でない。** **「Supreme Court saved/freed/rescued Cleveland」「Cleveland won/reached the Supreme Court」を書かない。** Cleveland の救済は "a lower court / an ordinary lawsuit / a settlement announced in late 2014" と表す。
3. **Bearden の holding を正確に。** 収監前に「支払い能力（willful refusal か genuine inability か）」と「代替手段（punishment short of a cell）」を検討する義務。Bearden は罰金・手数料・賠償そのものを禁じていない。**「all/every/any fines are unconstitutional」「banned all fines」に過大化しない。** 閉じたのは「能力がないだけでの収監」だけ。
4. **Harriet Cleveland は R2（存命私人）。** 顔・肖像・身体を描かない。象徴のみ（督促状の束・伏せた免許証・空の財布・留置場の扉・booking の時計・支払台帳・請求書・裁判所の長い廊下・バス停・空席の弁護人席）。**家庭・子どもを扇情化しない・尊厳をもって（poverty porn 禁止）。** 泣く人・嘆く家族・困窮の煽情描写を作らない。
5. **制度・営利保護観察（JCS＝Judicial Correction Services）を説明。特定個人を攻撃しない。** JCS は制度として象徴で示す（支払台帳・請求書・ゴム印・料金の skim）。Harrington 判事の公開判決の逐語引用は可（AE カード＝B の担当）だが、**画像で個人を攻撃・同定しない。**
6. **数値は台帳一致・捏造ゼロ。** $1,554 / 31日 / $200月 / $40がJCS / 約38,000人・4州 は原典一致。**画像には描かない**（判読不能・数値は AE/figures＝B）。confidence:medium のもの（$1,554・31日・$200/$40・能力審問なし・免許停止の連鎖・弁護人告知なし）は B のカードでヘッジ帰属を維持。

## 1.3 機械ゲート（`build_cleveland_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
BANNED_PORTRAIT = re.compile(
    r"\bportrait\b|\bmugshot\b|likeness of|"
    r"face of (harriet|cleveland|bearden|harrington|o'?connor|hub)|"
    r"recognizable (real )?person|identifiable face|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"debtors?['’ ]?prisons? (are|is|now)?\s*(legal|lawful)|"
    r"(legal|lawful) to (jail|imprison|lock ?up)|jailing the poor is (legal|lawful)|"
    r"(all|every|any) fines? (are|is|were) unconstitutional|fines? themselves (are|were) unconstitutional|"
    r"banned all fines|abolished all fines|no fines allowed|"
    r"(supreme court|scotus|nine justices) (saved|freed|rescued|ruled for|ruled in favou?r of) (harriet )?cleveland|"
    r"cleveland (won|reached|went to|before) the supreme court|"
    r"debtors?['’ ]?prisons? (are|were|now)?\s*(gone|abolished|over|eliminated everywhere|a thing of the past|no longer exist)|"
    r"no longer happens anywhere|completely (ended|abolished|gone|eradicated)|"
    r"poverty ?porn|starving child|crying child|weeping family",
    re.IGNORECASE)
```

> `BANNED_ACCURACY` は制約1〜4・6を機械化したもの。プロンプト・タグ・`caption_hint`・注記のどこにも該当語を書かない。**"unconstitutional since 1983" / "yet it continued" / "the rule held" / "still stands" / "enforcement failure" / "a lower court settlement in 2014" は許容（射程を正しく限定）。** 禁止は「合法」化・「全罰金違憲」化・「最高裁がClevelandを救った」・「完全に消滅した」・扇情（poverty porn）だけ。

---

# 2. 台本の語数と尺の確定値（SPEC から転記・Aが素材点数を積算する根拠）

**★唯一の真実 = `episodes/_planning/EP45_cleveland_PRODUCTION_SPEC.v001.json`。** 古い資料の wpm・語数は使うな。

```
words_total          = 2,119
narration_seconds    = 713.9   （= 11.9分・[DESIGNED SILENCE 1..3] の実音無音を含む）
wpm_used             = 178.1
総尺（設計）          = 713.9 + BrandOpening 3.50 + BrandEndcard 9.00 = 726.4秒 = 12:06  ≤ 750s
視覚シーン(narrative)  = 48（S01..S48・SPEC derive）
Act 構成（SPEC 秒）: HOOK 24.6 / OPENING 21.6 / BODY 509.0（ACT1+ACT2+ACT3）/ ENDING 138.8
```

**Aにとっての意味は1つ:** > **224カット / distinct 192 / 初出85.71% = still 84 + factory 92 + motion 16。**（§3 で積算）

> **注意（命名差）:** SPEC の視覚シーンは S01..S48。しかし **still は 84 本の固有プロンプトを持つ**ため、still の資産 ID は **S01..S84**（1プロンプト＝1枚）で採番する。48 の narrative シーンに 84 枚を配分する（ドクトリン核の ACT3 が最も厚い）。**still 資産 ID（S01..S84）と narrative シーンコード（S01..S48）は別物。** `covers_scene_id` は still 資産 ID 空間を指す（§7.3）。

---

# 3. ★素材構成の確定値（SPEC の distinct/cuts をそのまま調達する）

## 3.1 SPEC の内訳（★この値で調達する・勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **84枚** | 100カット | 1.19回(≤2) | **84本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **92本** | 92カット | **各1回(1)** | 在庫 11,000本超から選抜（§7）・全点目視・EP39〜44 と sha256 被りゼロ |
| **i2v モーション** | **16本** | 32カット | 各2回(≤2) | 16本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **192点** | **224カット** | | |
| 合成レイヤー（particle/light/vfx） | 12本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |

**SDXL の生成バッチ（本編カットに出ない i2v 種を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **84枚** | 84プロンプト × 1枚（バリエーション0） |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **16枚** | 16種プロンプト × 1枚（バリエーション0） |
| **SDXL 生成バッチ合計** | **84 + 16 = 100枚（各1回）** | **`--variants 1`** |

> **サムネは新規生成しない。** 完成後に body 84枚から6枚を `also_thumb:true` で流用選抜（追加生成ゼロ＝1シーン1枚前提を崩さない）。**role=thumb / still_thumb を作らない。**

> **★紙芝居回避（EP40 の最大の失敗）:** **still-cut 100 / (factory 92 + i2v 32)=video 124** で **still-share 44.64% ≤45%・motion coverage 55.36% ≥45%** を構造的に保証する（§3.3）。**stillを増やしてfactoryを削るな。factory 92 が still-share≤0.45 を守る下限。**

## 3.2 still 84枚・factory 92本・i2v 16本の幕別配分（目安）

| 区間 | narration秒 | still（S番号） | factory | i2v |
|---|---|---|---|---|
| HOOK | 24.6 | 4（S01–S04） | 6 | 2（M01,M02） |
| OPENING | 21.6 | 3（S05–S07） | 3 | 0 |
| ACT1 "The road that ends at a cell" | ~130 | 13（S08–S20） | 12 | 3（M03,M04,M05） |
| ACT2 "The machine" | ~200 | 18（S21–S38） | 16 | 4（M06,M07,M08,M09） |
| ACT3 "Bearden" | ~179 | 26（S39–S64） | 24 | 4（M10,M11,M12,M13） |
| ENDING | 138.8 | 20（S65–S84） | 12 | 3（M14,M15,M16） |
| 繋ぎ（covers_scene_id:null） | — | — | 19 | — |
| **合計** | **713.9** | **84** | **92** | **16** |

> ACT3 は Bearden ドクトリンの核（最も遅く荘厳）なので still も最多の26枚。
> **★幕別の factory 内訳（この表・§7.2・CODEX_B）は非拘束の目安値**（合計 92 のみ確定・幕割当は柔軟）。ゲートは factory を各1回・合計 92 でしか見ない。**確定値は「合計 factory 92」だけ。**

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 224 = still 100 + factory 92 + i2v 32
[2] 平均ショット長 = narration 713.9 / 224 = 3.187秒/カット  ✓ (SPEC mean_shot 3.19・≤6.0)
[3] 静止画占有率(check_animation_mix) = 100/224 = 44.64%  ✓ ≤45%（SPEC still_share 0.4464）
[4] motion coverage = (92+32)/224 = 124/224 = 55.36%     ✓ ≥45%（SPEC 0.553）
[5] per-asset 上限: still 100/84=1.19(≤2) / factory 92/92=1.0(≤1) / motion 32/16=2.0(≤2)  ✓
[6] first-use share = 192/224 = 0.8571                   ✓ ≥0.70（SPEC 一致）
[7] factory 下限: video を 124 カット以上に保たないと still-share が 0.45 を超える。
    i2v 32 は固定なので factory は 92 を下回れない（92+32=124）。→ factory 92 は下限であり水増しではない。
```

> **[3] の余裕は 0.36% しかない。** still が84本を割ったら §6.3 の再生成で回復させ、**still-cut 100 を増やさない**（B側の shotlist が100で固定）。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-045-cleveland/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `cleveland_assets.v1`（固定文字列）
**生産者:** `scripts/build_cleveland_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致。** role enum は **`body | i2v_source | reject` のみ**（`thumb`/`still_thumb` を作らない）。サムネは `also_thumb:true` の body still **ちょうど6枚**。overlay は **ちょうど12本**。

## 4.1 スキーマ（EP44 の `tekoh_assets.v1` と同型。counts を EP45 値に）

```jsonc
{
  "schema_version": "cleveland_assets.v1",
  "episode_id": "PD-2026-045-cleveland",
  "slug": "cleveland",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_cleveland_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 84,          // ==84
    "still_i2v_source": 16,    // ==16
    "motion": 16,              // ==16
    "factory": 92,             // ==92
    "overlay": 12              // ==12（distinct 素材に数えない）
  },
  "stills": [{
    "asset_id": "CLEV-S01",                // body: ^CLEV-S\d{2}$（1..84） / i2v種: ^CLEV-MS\d{2}$
    "scene_id": "S01",                     // still 資産 ID（§5.9 のプロンプト行に対応・S01..S84 空間）
    "role": "body",                        // body|i2v_source|reject（バリエーション概念なし＝各1枚）
    "also_thumb": false,                   // body から6枚だけ true（追加生成しない）
    "act": 0,                              // 0=HOOK/OPENING, 1=ACT1, 2=ACT2, 3=ACT3, 5=ENDING
    "path": "H:/pd-media/assets/ai/cleveland/S01.png",
    "depth_path": "H:/pd-media/assets/ai/cleveland/S01_depth.png",   // role=="body" は実在必須
    "public_path": "cleveland/img/S01.png", // role=="body" のみ非null
    "width": 3840, "height": 2160,         // 長辺>=3840
    "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 42.7,
    "tags": ["citation_stack","kitchen_table","rubber_band","symbolic","overdue"],
    "caption_hint": "a thick stack of unpaid citations bound with a rubber band on a kitchen table",  // check_cleveland_facts 検査対象（制約1-6）
    "seed": 0, "model": "juggernautXL_ragnarokBy",
    "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
    "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
           "has_identifiable_face": false, "has_human_body": false, "notes": ""}
  }],
  "motion": [{
    "asset_id": "CLEV-M01",                // ^CLEV-M\d{2}$（1..16）
    "source_scene_id": "M01_src",
    "source_still": "H:/pd-media/assets/ai/cleveland/M01_src.png",   // role=="i2v_source" の画像
    "path": "H:/pd-media/assets/ai_video/cleveland/M01_rife.mp4",
    "public_path": "cleveland/motion/M01_rife.mp4",
    "act": 0, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
    "sha256": "<64hex>", "tags": ["jail_door","booking"],
    "qc": {"reviewed": true, "on_theme": true, "artifact_free": true,
           "has_identifiable_face": false, "notes": ""}
  }],
  "factory": [{
    "asset_id": "AF-BG-0731",              // 棚 assets/asset_manifest.v001.json の id をそのまま
    "path": "H:/pd-media/assets/factory/backgrounds/AF-BG-0731__...mp4",
    "public_path": "cleveland/factory/AF-BG-0731__...mp4",
    "type": "backgrounds", "subtype": "<label>",   // ★ラベル=検索語の記録。中身の保証ではない（§7.5）
    "kind": "video", "license": "Pexels License",  // ALLOWED_LICENSES のいずれか
    "sha256": "<64hex>", "act": 2, "covers_scene_id": "S24",  // §7.3 の割当のみ。繋ぎは null
    "duration_sec": 7.60, "width": 1920, "height": 1080, "mean_luma": 48.3,
    "eyeballed_content": "a long empty courthouse corridor in cold light, no people",  // ★必須（§7.5）
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
           "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""}
  }],
  "overlay": [{
    "asset_id": "AF-PART-0044", "path": "H:/.../particle_assets/...mp4",
    "public_path": "cleveland/overlay/...mp4", "type": "particle_assets", "subtype": "<label>",
    "license": "Pexels License", "sha256": "<64hex>", "blend_hint": "screen",
    "eyeballed_content": "slow dust motes drifting on black, loops cleanly",
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""}
  }]
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `schema_version=="cleveland_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 84 / i2v_source 16 / motion 16 / factory 92 / overlay 12）に**一致**
3. 全 `path`/`depth_path`/`public_path` がディスクに実在
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `depth_path` と `public_path` が非null かつ実在
7. `qc.has_readable_text==true` / `qc.has_identifiable_face==true` / `qc.has_human_body==true` のいずれかは `role=="reject"`
8. `role=="i2v_source"` は `role=="body"` と**同一 asset_id を共有しない**（distinct 分離。i2v_source は `CLEV-MS\d{2}`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39・EP40・EP41・EP42・EP43・EP44 の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない（＝目視していない本が混じっていない）
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど6**、かつ **`scene_id` 集合が `{S01,S03,S18,S46,S68,S84}`（§4.3）と完全一致**（追加生成ではなく body からの流用。**この集合は CODEX_B §11 と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|reject のみ）
16. `overlay` 配列長が**ちょうど12**

`--reuse-feasibility` では §3.3 [5][6][7] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 84枚（S01..S84）= §5.9 の84プロンプトの生成物。各1枚。
2. i2v_source 16枚（MS01..MS16 / 種画像 M01_src..M16_src）= §8.1 の16種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. also_thumb : body のうち S01 / S03 / S18 / S46 / S68 / S84 の6枚に true（追加生成しない）
4. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

---

# 5. A-1: SDXL 静止画のバッチ生成（84本 × 1枚・バリエーション0）

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-045-cleveland/04_scenes/ai_prompts.v001.md   ← A が §5.2 の形式で書く
出力:  H:\pd-media\assets\ai\cleveland\S<NN>.png（+ remotion/public/cleveland/ に自動コピー）
2段パイプライン: txt2img 1536x864 → hires 3072x1728 → extras R-ESRGAN 4x+ → 3840x2160（長辺≥3840・冪等スキップ）
```

**ローカルGPU生成に課金は発生しない。** 禁止は ElevenLabs TTS / 課金画像API / アップロードのみ（§12）。

## 5.2 ★パーサ契約（`read_prompts()` はこの2行形式しか読まない・実装確認済み）

正規表現 `^\s*-\s+` + バッククォート囲みの `<stem>.png` + 次行に `Avoid:` を含む1行:

```
- `S01.png`
<positive prompt> Avoid: <negative>
```

- **1行目:** `` - `S01.png` ``（バッククォート囲み・**行末は `.png` の直後**。プロンプトを同じ行に書かない）
- **2行目:** 正プロンプト → `Avoid:` → 負プロンプト（負は `DEFAULT_NEG` に自動連結される）
- `ai_prompts.v001.md` は **body 84行（S01..S84）＋ i2v 種 16行（M01_src..M16_src、§8.1a）＝ 100 エントリ**を書く。すべて1枚生成。

## 5.3 生成コマンド（★`--variants 1`。`--variants 3` は使わない）

```bash
# まず1枚だけ回して読める行数を確認（★shots=100 でなければ形式が壊れている）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 45 --variants 1 --only S01
#   → ログ "episode=... shots=100 variants=1 ... -> 100 images" の shots が 100 であること

# 全100枚（body 84 + i2v種 16・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-045-cleveland --variants 1
#   → 生成 S01.png ... S84.png / M01_src.png ... M16_src.png（各1枚。_02/_03 は作らない）
```

> QC で落ちたシーンの再生成は `--only S37`（**同じプロンプトで別シードを1枚**）。既存の>=3840はスキップ・不足だけ埋まる。**バリエーションを増やして水増ししない。枚数を減らして基準を下げるのも禁止。**

## 5.4 共通スタイル `[STYLE]`（全プロンプト末尾に必ず全文連結）

```
, cinematic still, cold-and-warm documentary grade, a worn working-class Alabama kitchen table under warm tungsten lamplight where ordinary paper piles up, set against cold grey institutional county-jail and courthouse interiors in pale marble and fluorescent light, a single overdue-notice crimson accent as the one warm-red note, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face
```

> **EP39〜EP44 との分離:** `navy interrogation room`/`electric blue`（EP39）・`midday sunlight`/`suburban demolition`/`bleached daylight`（EP40）・`prison cell`/`cellblock`/`sodium prison corridor`/`steel death-row`（EP41）・`Chicago apartment`/`ankle monitor`/`body-worn camera vest`（EP42）・`porch-amber house`/`ambulance red lights`/`tow-truck`（EP43）・`teal-green hospital corridor`/`clinical hospital`（EP44）を**1語も含めない**。EP45 は 暖色ランプ下の労働者階級の台所（督促状の束・伏せた免許証・空の財布）＋冷たい灰色の郡拘置所 booking（無人・鉄格子/独房を描かない）＋淡い大理石の裁判所の長い廊下・空席の弁護人席＋アラバマの陽炎の空き道路とバス停＋朱色（督促）の一点差し色＋夜明けの採光。

## 5.5 共通ネガティブ `[NEG]`（各 `Avoid:` の後に必ず全文付ける）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible paper, legible citation, legible license number, legible dollar amount, legible date, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, human body, child, crying person, weeping family, sensational distress, poverty porn, weapon, gun, blood, gore, nude, bare skin, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, prison cell, steel cellblock, barred cell, sodium prison corridor, navy interrogation room, electric blue, teal-green hospital corridor, clinical hospital, hospital bed, midday suburban daylight, suburban demolition, tow truck, ambulance, porch amber house, ankle monitor, body-worn camera
```

> ネガティブにも **制約違反語（"debtors' prison is legal", "all fines unconstitutional", "supreme court saved cleveland", "gone / abolished everywhere", poverty porn 語 等）を書かない**（§1.3）。上のリストにも含めていない。**扇情・子ども・困窮の煽情描写・身体・可読の金額/日付/判例番号・会社ロゴを NEG で明示的に抑制**（制約2/4）。会社ロゴが必要な絵（請求書・契約）は「blurred into an unreadable smear」で判読不能にする。

## 5.6 バリエーション軸（★EP45 では無効）

`generate_sdxl_4k.py` の `--variants 1` は各 stem を**1枚だけ**生成する。**`_02`/`_03` を作らない。** 反復回避は「84本の固有プロンプト＝84の別被写体」で担保する。

## 5.7 メタJSON

`generate_sdxl_4k.py` は画像を書くが per-image メタJSONは書かない。**A は QC 時に `qc_cleveland_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.8 プロンプトの絶対ルール（84本すべてに適用）

- **顔なし・身体なし・裸体なし。** 人物は原則出さない（制約4・R1）。Harriet Cleveland を個人として描かない。
- **可読文字なし。** 督促状・免許証・支払台帳・請求書・和解書・意見書・カレンダーは雰囲気のみ（判読不能）。判例番号・日付・金額・人数・会社ロゴを描かない（ロゴはぼかす）。
- **象徴オブジェのみ:** 督促状の束（輪ゴム）・伏せた免許証・空の財布・留置場の扉/booking の時計・支払台帳/請求書（ロゴぼかし）・裁判所の長い廊下・バス停（車社会の孤立）・空席の弁護人席・古い法律書（Bearden）・大理石の最高裁列柱・開くドア/採光。
- **扇情化しない**（制約4）: 泣く人・嘆く家族・子ども・困窮の煽情を描かない。尊厳をもって物だけで示す。
- **「合法」化しない**（制約1）: 「投獄は合法/正当」に見える絵を作らない。閉じたドア（違法な収監）と、開いたドア/採光（1983のルールが立っている）の対比を象徴で持つ。
- **最高裁と下級審を混同しない**（制約2）: 最高裁の列柱＝Bearden の線。Cleveland の救済は「 modest county courthouse / 折り畳まれた和解書（2014）」で下級審として描く。
- **全罰金違憲化しない**（制約3）: 罰金・手数料・賠償の物は「そのまま立っている（untouched）」象徴で。閉じたのは「能力がないだけでの収監」だけ。

## 5.9 確定プロンプト（★`ai_prompts.v001.md` にこの84エントリをそのまま書く・各1枚）

> 各行の `[STYLE]` は §5.4 を、`Avoid:` の後の `[NEG]` は §5.5 を**全文展開**して書く（下記は簡潔表記のマクロ。省略記号ではなく定義済み定数）。全て顔なし・身体なし・象徴・判読不能・扇情なし。

```
- `S01.png`
A thick stack of unpaid traffic citations bound with a single rubber band on a worn kitchen table under warm lamplight, the paper edges printed in overdue crimson, ordinary paper piling into a sentence, no legible text, no people [STYLE] Avoid: [NEG]
- `S02.png`
A driver's license lying face-down on a worn kitchen table under warm lamplight, the one thing that let her look for work turned over and silenced, no legible text, no face, no people [STYLE] Avoid: [NEG]
- `S03.png`
An open wallet lying flat and completely empty on a kitchen table in warm lamplight, nothing inside it, quiet and plain, no legible text, no people [STYLE] Avoid: [NEG]
- `S04.png`
A heavy county intake door standing shut in a cold grey booking area under fluorescent light, a plain institutional door closed on a corridor, no bars, no cell, no people, no readable sign [STYLE] Avoid: [NEG]
- `S05.png`
A quiet working-class Montgomery Alabama street at dusk with modest houses and a bare front yard, an ordinary neighborhood where a small debt began, warm sky over cold pavement, no people, no readable signage [STYLE] Avoid: [NEG]
- `S06.png`
The pale marble facade and tall columns of the United States Supreme Court at night, cold stone lit from below, monumental and distant, the court that answered this in 1983, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S07.png`
A single overdue notice edged in crimson resting on a plain table in warm lamplight in the foreground with the cold marble colonnade of the highest court faint and distant beyond it, the span from a small debt to the highest court, no legible text, no people [STYLE] Avoid: [NEG]
- `S08.png`
A single ordinary traffic citation tucked under a windshield wiper on a parked car at dusk, the commonest kind of ticket, the paper edge crimson, no legible text, no people [STYLE] Avoid: [NEG]
- `S09.png`
The stack of citations grown thicker and rebound with a fresh rubber band on the kitchen table, a debt that sits and grows instead of staying still, no legible text, no people [STYLE] Avoid: [NEG]
- `S10.png`
A suspended driver's license face-down beside a folded suspension notice on a kitchen table under warm light, the license taken for tickets unpaid, the paper's text abstract and unreadable, no legible words, no face, no people [STYLE] Avoid: [NEG]
- `S11.png`
An empty two-lane Alabama road shimmering in heat under a hard sky, no bus and no ride in sight, the distance a life still has to cross, no people, no readable signage [STYLE] Avoid: [NEG]
- `S12.png`
A lone roadside bus-stop pole on an empty rural shoulder in the Alabama heat with no bus coming, the transit that does not reach the work, no people, no readable sign [STYLE] Avoid: [NEG]
- `S13.png`
A single worn car key resting beside an empty wallet on a car dashboard in flat daylight, driving as the only way left, no legible text, no people [STYLE] Avoid: [NEG]
- `S14.png`
An unpaid insurance form curling on a car's passenger seat in hard light, coverage she cannot afford, the printed lines abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S15.png`
A growing pile of citations and fee slips fanned across the kitchen table, each remedy costing more than the thing it fixed, edges printed in overdue crimson, no legible text, no people [STYLE] Avoid: [NEG]
- `S16.png`
A plain courthouse desk holding a signed order, a pen and a gavel in cold pale light, the sum and the cell decided on one page, the document's text abstract and unreadable, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S17.png`
An empty county-jail intake counter in a cold grey booking area under fluorescent light, a plain institutional room, no bars, no cell, no people, no readable text [STYLE] Avoid: [NEG]
- `S18.png`
A heavy institutional booking door standing shut beneath a plain wall clock in cold grey light, the door closing on a debt that was never a crime, no bars, no people, no readable time [STYLE] Avoid: [NEG]
- `S19.png`
A bare grey booking corridor receding under cold fluorescent light, a plain government hallway, no bars, no cell, deliberately austere, no people, no readable signage [STYLE] Avoid: [NEG]
- `S20.png`
A plain wall clock at booking held in a still frame, its second hand caught mid-sweep in cold grey light, a held silence, no people, no readable numerals [STYLE] Avoid: [NEG]
- `S21.png`
A payment ledger book open on an office desk under cold light, ruled columns filled with abstract unreadable figures, a debt turned into a bookkeeping line, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S22.png`
A monthly invoice on a desk with the company logo at its top deliberately blurred into an unreadable smear, cold office light, a private company billing for punishment, no legible text, no people [STYLE] Avoid: [NEG]
- `S23.png`
A rubber stamp resting upright beside an ink pad on a probation-office desk in cold light, the small machine that processes a person into revenue, no legible text, no people [STYLE] Avoid: [NEG]
- `S24.png`
A long courthouse corridor receding into cold institutional light, polished floor and closed doors, the passage a case is handed down, no people, no readable signage [STYLE] Avoid: [NEG]
- `S25.png`
A narrow payment window with a worn counter slot in a municipal office under cold light, where the monthly money is taken, no legible text, no people [STYLE] Avoid: [NEG]
- `S26.png`
A printed spreadsheet of abstract figures pinned to an office wall in cold light, a person reduced to a row of numbers, the marks unreadable, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S27.png`
A row of monthly payment envelopes on a desk with one set apart to the side, the company's cut lifted off the top before any fine is touched, no legible text, no people [STYLE] Avoid: [NEG]
- `S28.png`
Two uneven stacks of plain banknote-shaped paper split on a desk under cold light, the larger toward the fine and a small share skimmed away, the denominations abstract and unreadable, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S29.png`
An office nameplate turned face-away beside a vacant desk chair in cold light, the company employee implied only by objects, no person, no legible name [STYLE] Avoid: [NEG]
- `S30.png`
An empty counsel chair pulled up to a vacant defense table in a courtroom under cold light, the one seat whose whole job was to speak left unfilled, no people, no readable text [STYLE] Avoid: [NEG]
- `S31.png`
A plain empty seat at a bare table where an advocate should sit, a single missing voice rendered as an empty chair, cold light, no people, no readable text [STYLE] Avoid: [NEG]
- `S32.png`
A wall map of Alabama studded with many small pins across its towns in cold office light, one company reaching into court after court, the labels abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S33.png`
Rows of anonymous case folders receding on office shelves under cold light, thousands of people filed as paper, no legible text, no people [STYLE] Avoid: [NEG]
- `S34.png`
A small-town courtroom bench and rail standing empty in cold light, warm wood against pale plaster, an ordinary room where the debt was tallied, no people, no readable text [STYLE] Avoid: [NEG]
- `S35.png`
A folded court order set down hard beside a resting gavel on a bench in cold light, a practice a judge would soon name plainly, the document abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S36.png`
A single gavel resting on its sounding block in a deserted courtroom under cold light, the authority of a court held still, no people, no readable text [STYLE] Avoid: [NEG]
- `S37.png`
A single hearing-transcript page lying alone in a hard shaft of light on a courtroom table, the word a judge put into the permanent record, the marks abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S38.png`
The modest brick facade of a small Alabama town courthouse at dusk, ordinary and civic, the kind of court the practice ran through, no people, no readable sign [STYLE] Avoid: [NEG]
- `S39.png`
An old leather-bound volume of law reports closed on a dark desk under a warm lamp, its worn spine title abstract and unreadable, the 1983 promise rendered as a book, no legible text, no people [STYLE] Avoid: [NEG]
- `S40.png`
The tall columns and pale marble facade of the United States Supreme Court seen frontally at night, monumental and solemn, the case carried up to be decided, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S41.png`
A worn ledger page on a desk under warm light showing an old small debt broken into an abstract payment schedule, a fine and a restitution owed on dates, the numbers illegible, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S42.png`
A borrowed-money envelope half emptied beside a folded payment schedule on a dark desk, the first payment made and the balance impossible, the text abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S43.png`
An empty factory time-clock rack with the last card pulled, cold flat light, the work that vanished and took the income with it, no legible text, no people [STYLE] Avoid: [NEG]
- `S44.png`
A closed beginner's reading primer resting beside the heavy law volume under a warm lamp, a man who could not read the papers that bound him, the covers abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S45.png`
A plain institutional door swinging shut at the end of a bare grey corridor, probation revoked over a balance that could not be paid, no bars, no cell, no people, no readable sign [STYLE] Avoid: [NEG]
- `S46.png`
The marble colonnade of the Supreme Court at night lit from below, the case climbing all the way up, monumental and distant, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S47.png`
A single opinion volume lying open under a warm desk lamp, its pages reduced to abstract illegible lines, the narrow rule being written, no legible words, no people [STYLE] Avoid: [NEG]
- `S48.png`
A hard single line of light dividing a cold marble floor into two unequal sides, the line between a willful refusal and a genuine inability to pay, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S49.png`
A fork splitting a narrow marble path into two roads under cold light, the two findings a court must make before it may jail anyone, symbolic and abstract, no people, no text [STYLE] Avoid: [NEG]
- `S50.png`
A pair of plain scales weighing a small everyday object against a closed institutional door under cold light, an alternative to prison the court is bound to consider, abstract, no legible words, no people [STYLE] Avoid: [NEG]
- `S51.png`
A single band of engraved-looking light running across a cold marble wall where two streams of light meet, due process and equal protection converging, the characters abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S52.png`
Two older law volumes standing on a marble shelf beside the newer one under cold light, the rulings of 1970 and 1971 that came before the capstone, their titles abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S53.png`
A single capstone set atop an arch built of stacked law volumes under cold light, one ruling completing a line of older ones, monumental and abstract, no legible text, no people [STYLE] Avoid: [NEG]
- `S54.png`
A row of fine, fee and restitution objects still standing intact on a marble surface under cold light, the punishments the ruling left untouched, the labels abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S55.png`
A full wallet resting beside a firmly closed institutional door under cold light, the person who has the money and simply refuses to pay, still answerable, no legible text, no people [STYLE] Avoid: [NEG]
- `S56.png`
An empty wallet resting beside the same firmly closed institutional door under cold light, jailed for the single reason of having nothing, and no one having asked, no legible text, no people [STYLE] Avoid: [NEG]
- `S57.png`
A signed order lying across a bright hard line drawn on a cold marble floor, an order that stepped straight over the line because no one stopped to ask, the text abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S58.png`
The marble Supreme Court seen distant and shut at the end of a cold plaza, no rescue riding back in, the highest court that this case never reached, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S59.png`
A modest county courthouse of plain brick and stone under an ordinary sky, the lower court where relief actually came, civic and unremarkable, no people, no readable sign [STYLE] Avoid: [NEG]
- `S60.png`
A folded settlement document resting on a plain table under a warm lamp, a rule written out a second time by hand in 2014, the printed lines abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S61.png`
A payment plan with its extra layered fees crossed through on a desk under warm light, charges to be reduced under a settlement, the numbers abstract and unreadable, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S62.png`
A folded contract with a private company being set aside and cancelled on a desk, the company logo blurred into an unreadable smear, a city ending the arrangement, no legible text, no people [STYLE] Avoid: [NEG]
- `S63.png`
An old bound volume standing untouched on a courthouse shelf in a shaft of cold light, a law that had not changed in three decades, its title abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S64.png`
A thick federal complaint folder resting on a desk under cold light while an office beyond it goes dark, a racketeering suit and a company closing its doors, the text abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S65.png`
The signed court order lying alone under a warm lamp showing an amount or a stretch of days, a single page holding a fork, the numbers abstract and unreadable, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S66.png`
A checkbook and pen resting beside an open door and pale daylight under warm light, for a person with the money it was never a choice at all, no legible text, no people [STYLE] Avoid: [NEG]
- `S67.png`
The same order page with a firmly closed cold door standing behind it, the jail sentence that existed only for the person who could not pay, no legible text, no people [STYLE] Avoid: [NEG]
- `S68.png`
A paper receipt lying loose on one side of a single frame and a locked cold door on the other, the same page meaning nothing to one person and a cell to another, abstract, no legible text, no people [STYLE] Avoid: [NEG]
- `S69.png`
A wall calendar with a run of days marked out in cold light, a stretch of confinement that was only ever a price for what she did not have, the dates abstract and unreadable, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S70.png`
A suspended driver's license lying beside a set of car keys under warm light, the very license she needed to earn the money the tickets demanded, no legible text, no face, no people [STYLE] Avoid: [NEG]
- `S71.png`
A single car key going dark on a table as the daylight drains from the room, the driving gone and the work leaving with it, the debt with nowhere to climb but up, no legible text, no people [STYLE] Avoid: [NEG]
- `S72.png`
The Constitution rendered as a heavy closed book on a courthouse shelf in cold light, the words that already existed, its title abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S73.png`
The same closed book on the shelf with a single shaft of warm light falling across it, a right that was already hers in 1983, the characters abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S74.png`
A shaft of light falling just short of a closed book on a courthouse shelf, no one reaching for the words that morning, symbolic and severe, no hand, no people, no text [STYLE] Avoid: [NEG]
- `S75.png`
A small deserted courtroom at first light with a single empty seat before the bench, the morning a name was called and no one reached for the rule, no people, no readable text [STYLE] Avoid: [NEG]
- `S76.png`
The Constitution standing upright on a high shelf while the courtroom floor below it stays empty in cold light, the law on her side yet never walking into the room, its title abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S77.png`
A heavy institutional booking door standing shut again in cold grey light, the cold question of the opening returned, no bars, no people, no readable sign [STYLE] Avoid: [NEG]
- `S78.png`
A single steady band of engraved-looking light holding firm across a cold marble wall, the answer that has stood since 1983, the characters abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S79.png`
Two distant marble buildings held in one cold frame, a settled book in one city and a courtroom a thousand miles away, the gulf between a written answer and an obeyed one, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S80.png`
A receding line of plain county courthouses fading into cold haze, county after county where the simple act of following the rule kept failing, no people, no readable signage [STYLE] Avoid: [NEG]
- `S81.png`
A long courthouse corridor in cold light with an empty wallet resting in the near foreground, the low hum of the building rising into a designed silence, no legible text, no people [STYLE] Avoid: [NEG]
- `S82.png`
A heavy door beginning to open onto a bar of warm daylight at the end of a cold corridor, a silence that finally carries sound, no people, no readable sign [STYLE] Avoid: [NEG]
- `S83.png`
An empty rural road and a lone bus-stop pole under a grey dawn sky, quiet and open-ended, the city just beginning to stir, no people, no readable sign [STYLE] Avoid: [NEG]
- `S84.png`
A plain door left slightly ajar onto soft morning light in a slow pull-back, the held final image, unresolved but open, no people, no readable number [STYLE] Avoid: [NEG]
```

**枚数チェック:** 上記 84 エントリ（S01..S84）。§5.3 の `--only S01` ログで `shots=100`（body 84 + i2v種 16）を確認してから本番を回す。

---

# 6. A-2/A-3: 静止画のQC・目視・depth map

## 6.1 機械QC（body 84 + i2v種 16 = 全100枚・`qc_cleveland_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `35.0<=mean_luma<=225.0`（EP45は暖色台所と冷たい灰色 booking・大理石廊下・夜明けが混在→暗い booking/廊下側が黒潰れリスク。`check_visual_asset_qc.DARK_LUMA_FLOOR=45.0` を下回りすぎる本に注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject（`check_visual_asset_qc.NEARDUP_SIM=0.90`）。**バリエーション0なので本来ほぼ衝突しないはず。衝突したらプロンプトが被っている**（特に多数ある「督促状の束」「留置場の扉/booking」「裁判所の長い廊下」「大理石の最高裁列柱」「閉じたドア」系に注意） | 片方 reject＋プロンプト見直し |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・判例番号・日付・金額・人数・会社ロゴが写っていないか（R1・制約2/6） | `has_readable_text=true`→reject |
| Q6 | 顔の混入 | **目視。** 識別可能な顔が写っていないか（R1・制約4） | `has_identifiable_face=true`→reject |
| Q7 | 身体/扇情の混入 | **目視。** 人体・裸体・泣く人・嘆く家族・子ども・困窮の煽情（poverty porn）が写っていないか（制約4） | `has_human_body=true`→reject |

**Q5/Q6/Q7 は機械で判定しない。** コンタクトシートを出して**全100枚を実際に目視**する:

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-045-cleveland --media image
#   → runs/qc/cleveland_footage_contact_NN.png（20枚/シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-44 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** SDXL は平気で読める文字・顔・身体を描く。**特に制約2（可読の金額/日付/判例番号/会社ロゴの非露出）・制約4（Cleveland 非人物化・扇情なし）は目視でしか守れない。** S10/S70（免許証）は読める免許番号が写っていないこと、S16/S60/S65（命令・和解・命令）は読める金額/日付が写っていないこと、S22/S62（請求書・契約）は会社ロゴが判読不能にぼけていること、S28（分割された金）は読める額面が写っていないことを必ず目で確認する。

## 6.2 出力

```
episodes/PD-2026-045-cleveland/05_visuals/still_qc.v001.json     # 100枚全部の行（reject も残す・sha256/phash/mean_luma/long_edge）
（build_footage_contact_sheet が runs/qc に出す）
```

## 6.3 accepted が100枚に届かなかったとき

```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 45 --variants 1 --only S37   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_cleveland_stills.py
```
accepted body >= 84 かつ i2v_source >= 16 になるまで繰り返す。**基準を下げない・バリエーションを足して水増ししない。**

## 6.4 depth map（★新規スクリプトを作らず既存を使う）

```bash
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir "H:/pd-media/assets/ai/cleveland"
```
- モデル `Intel/dpt-large`。出力 `<stem>_depth.png`（同サイズ L グレースケール）。冪等。
- **role が `body` の静止画は depth 必須**（`treatment:"depth"` が隣に `_depth.png` を要求。無いとレンダーがクラッシュ）。i2v 種（`M<NN>_src.png`）は depth 不要。
- staging 後に `remotion/public/cleveland/img/` 側でも同名ペアが揃っていること（§10）。

---

# 7. A-4: factory 実写クリップ 92本の選定と全点目視QC

## 7.1 在庫の実態

```
H:\pd-media\assets\factory\   フラット構成
  backgrounds/     11,000本超（.mp4）  ← ★主力（アラバマの街/夕暮れ・空き道路/バス停・郡拘置所や庁舎の外観・冷たい大理石の裁判所/長い廊下・空の法廷・最高裁列柱・夜〜夜明けの街・繋ぎ）
  light_assets/    …            合成レイヤー（暖色ランプ・冷たい fluorescent・大理石の光条）
  particle_assets/ …            合成レイヤー（大理石法廷の埃・書庫の塵）
  vfx_overlays/    …            合成レイヤー（グレイン・光ノイズ）
  texture_assets/  …            紙・石・大理石のテクスチャ
  loops/           …            抽象的な繋ぎ
ファイル名規約: AF-<TYPECODE>-<4桁>__<subtype_slug>.<ext>（TYPECODE = BG|LIGHT|LOOP|PART|TEX|VFX）
棚レジストリ: C:\Users\aab15\Documents\prime-documentary\assets\asset_manifest.v001.json
   （トップキーは schema と assets。★必ず encoding="utf-8" で開く。cp932 既定だと落ちる）
```

## 7.2 選定条件

- **`kind=="video"` のみ。** 静止画 factory は使わない
- **92本ちょうど**（§3.3[7] より 92 は still-share≤0.45 を守る下限。減らせない）
- **各1回しか使わない**（`check_asset_reuse.MAX_USES_FACTORY=1`）
- 幕別割り当て（§3.2）: HOOK=6 / OPENING=3 / ACT1=12 / ACT2=16 / ACT3=24 / ED=12 ＋ 繋ぎ=19 ＝ 92
- **EP39（夜/取調室/青）・EP40（郊外/昼/破壊）・EP41（監獄/鉄/石の独房）・EP42（シカゴのアパート/足首モニタ）・EP43（RI の一軒家/porch-amber/救急車/レッカー）・EP44（ティール緑の病院の廊下/臨床）の絵柄を選ばない。** EP45 は アラバマの街/空き道路/バス停＋郡拘置所や庁舎の外観＋淡い大理石の裁判所の長い廊下・空の法廷・空席の弁護人席・最高裁列柱＋夜〜夜明けの街。**鉄格子/独房/cellblock を含むクリップを選ばない（EP41 分離）。泣く人・困窮の煽情・子どもを含むクリップを選ばない（制約4）。**

**既存の選定ツールで候補出し（新規に検索ロジックを書くな）:**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes   # テーマ一覧と件数
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query courthouse --limit 96 --exclude-used --ep PD-2026-045-cleveland --json
```
`--exclude-used` は `check_arc_nonrepeat.build_universe()` と同じ指紋集合を使うので出荷ゲート `arc_nonrepeat` と食い違わない。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・SDXLで作らない情景）

> **★`covers_scene_id` は still 資産 ID 空間（S01..S84・§2 注記）を指す。narrative シーン（DESIGN の S01..S48）とは別体系。** B はこの値を still 資産 ID として解決し、narrative シーンコードにクロスマップしない。

| covers | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S05 | 労働者階級の街（夕暮れ） | `montgomery_street` / `small_town_street_dusk` | 0 |
| S06 | 最高裁ファサード・列柱 | `supreme_court_building` / `marble_columns` | 0 |
| S11 | アラバマの空き道路（陽炎） | `empty_rural_road` / `two_lane_highway_heat` | 1 |
| S12 | バス停（無人・路傍） | `bus_stop_roadside` / `empty_bus_stop` | 1 |
| S24 | 裁判所の長い廊下 | `courthouse_corridor` / `long_courthouse_hallway` | 2 |
| S34 | 小さな町の法廷内観（無人） | `empty_courtroom` / `courtroom_interior` | 2 |
| S38 | 小さな町の庁舎外観（夕暮れ） | `county_courthouse` / `courthouse_exterior_dusk` | 2 |
| S40 | 最高裁の列柱（正面・夜） | `supreme_court_columns` / `marble_facade_night` | 3 |
| S46 | 最高裁の列柱（夜） | `supreme_court_night` / `courthouse_columns_night` | 3 |
| S59 | 郡の庁舎（下級審・modest） | `county_courthouse_entrance` / `small_courthouse` | 3 |
| S83 | 夜明けの空き道路/バス停（受け） | `empty_road_dawn` / `roadside_dawn` | 5 |

**残り本数は covers を持たない繋ぎ・情景クリップ**（`covers_scene_id:null`）: 冷たい大理石の廊下・空の法廷・列柱の光条・郡庁舎の外観・アラバマの街と空き道路・夜〜夜明けの街・雨のアスファルト・書庫の棚・抽象 `loops`。**暗いクリップに偏りすぎない**（§7.5 の暗側閾値・全体の1/3=約30本まで。暖色ランプ・大理石の昼光・夜明け側を優先）。

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）

```python
ALLOWED_LICENSES = {"cc0","royalty_free","generated_owned","Pexels License","Pixabay Content License"}
```

## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★

> **推測ではなく実際に起きた事故。** EP36: `city_surveillance_camera_dome` が大聖堂。EP38: 牛が `documents_on_desk`。`subtype` は「その検索語で取った」記録であって**中身の保証ではない**。

**選抜92本は例外なく次を経る:**

```bash
# 1) 選定した92本を staging フォルダに集め、ラベル付きコンタクトシートを出す
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py \
    --ep PD-2026-045-cleveland --media video --dir "<92本の staging フォルダ>"
#   → runs/qc/cleveland_footage_contact_NN.png（各タイルにファイル名ラベル）
```

2. **コンタクトシートを実際に開き、92本すべてを1本ずつ見る**
3. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて**選定から外す**
4. 実写シネマティックB-roll（アニメ/CG臭排除）・EP45テーマ（アラバマの街/空き道路/バス停・郡庁舎・大理石の裁判所の長い廊下/空の法廷/列柱・夜〜夜明けの街）・ウォーターマークなし・識別可能な実在人物なし（制約4・R1）を確認
5. **★制約4/6の目視:** 人物が写るクリップは避け、写る場合も後ろ姿/遠景/顔外しのみ。**泣く人・嘆く家族・子ども・困窮の煽情（poverty porn）を含むクリップは使わない。** 判事席や街頭に実在の顔が写るニュース映像を使わない（制約4）。**鉄格子/独房/cellblock を含むクリップを使わない（EP41 分離）。**
6. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=45.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。
> **EP45 は冷たい灰色 booking＋長い大理石廊下＋夜が多いので暗側が本命リスク。** 平均輝度45未満のクリップが全体の40%を超えると FAIL。**暗いクリップは約30本（1/3）までに抑え、暖色ランプ・大理石の昼光・夜明けの実用光がある本を優先する。**

**1フレームで判断がつかない本は VLC/ffplay で再生して確認**（near-still は `check_animation_mix` を落とす）。

## 7.6 出力

```
episodes/PD-2026-045-cleveland/05_stock/factory_selection.v001.json   # 選定理由と幕割り当て
episodes/PD-2026-045-cleveland/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39〜EP44 との重複ゼロ（BLOCKING）

```bash
./.venv/Scripts/python.exe scripts/select_cleveland_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` 〜 `episodes/PD-2026-044-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP45 の92本の積集合が**空**であることを確認。1件でも exit 1 で差し替え。**EP39〜EP44 のファイルは読むだけ。書き込み・移動・削除は一切しない。**

---

# 8. A-5: i2v モーション化 16本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする16本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）

種画像は §5 と同じ `generate_sdxl_4k.py --variants 1` で `M<NN>_src.png` として生成する（`ai_prompts.v001.md` に下記16行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `CLEV-MS01..MS16`、モーション成果物の asset_id は `CLEV-M01..M16`。

| # | asset_id | 種画像 | 動きの意味 | act |
|---|---|---|---|---|
| 1 | CLEV-M01 | M01_src | 留置場の重い扉が閉じる寸前（冷たい灰色 booking） | 0 |
| 2 | CLEV-M02 | M02_src | booking の壁時計・秒針が動く | 0 |
| 3 | CLEV-M03 | M03_src | 輪ゴムで束ねた督促状の束への緩いプッシュ | 1 |
| 4 | CLEV-M04 | M04_src | 伏せた免許証・ランプの光が微かに揺れる | 1 |
| 5 | CLEV-M05 | M05_src | アラバマの空き道路の陽炎・バス停・バスは来ない | 1 |
| 6 | CLEV-M06 | M06_src | 支払台帳への緩いプッシュ（抽象の桁） | 2 |
| 7 | CLEV-M07 | M07_src | ゴム印とロゴぼかしの請求書・冷たい光が移ろう | 2 |
| 8 | CLEV-M08 | M08_src | 裁判所の長い廊下への緩い前進ドリー | 2 |
| 9 | CLEV-M09 | M09_src | 空席の弁護人席・冷たい光が移ろう | 2 |
| 10 | CLEV-M10 | M10_src | 古い法律書（Bearden）・ランプの光と埃 | 3 |
| 11 | CLEV-M11 | M11_src | 最高裁の列柱・冷たい光が動く | 3 |
| 12 | CLEV-M12 | M12_src | 大理石の床を分ける一条の光（能力ありの拒否 vs ないだけ） | 3 |
| 13 | CLEV-M13 | M13_src | 折り畳まれた和解書への緩いプッシュ（2014） | 3 |
| 14 | CLEV-M14 | M14_src | 空の財布への緩いプッシュ（受け） | 5 |
| 15 | CLEV-M15 | M15_src | 重い扉が採光へ開き始める | 5 |
| 16 | CLEV-M16 | M16_src | バス停・空き道路が夜明けへ移る | 5 |

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの16行を追加・各1枚）

```
- `M01_src.png`
A heavy county-jail intake door in a cold grey booking area caught just before it swings shut under fluorescent light, no bars, no cell, framed and still, no people, no readable sign [STYLE] Avoid: [NEG]
- `M02_src.png`
A plain wall clock at booking in cold grey light with its second hand poised mid-sweep, framed for a slow hold, no people, no readable numerals [STYLE] Avoid: [NEG]
- `M03_src.png`
A thick stack of unpaid citations bound with a rubber band on a worn kitchen table under warm lamplight, the paper edges printed crimson, still and poised for a slow push, no legible text, no people [STYLE] Avoid: [NEG]
- `M04_src.png`
A suspended driver's license lying face-down on a worn kitchen table under warm lamplight, still and poised, the one thing turned over, no legible text, no face, no people [STYLE] Avoid: [NEG]
- `M05_src.png`
A lone roadside bus-stop pole on an empty Alabama road shimmering in heat under a hard sky, no bus, still and poised, no people, no readable sign [STYLE] Avoid: [NEG]
- `M06_src.png`
A payment ledger open on an office desk under cold light with ruled columns of abstract unreadable figures, still and poised for a slow push, no legible numbers, no people [STYLE] Avoid: [NEG]
- `M07_src.png`
A rubber stamp resting beside an invoice with a blurred unreadable company logo on a probation-office desk in cold light, still and poised, no legible text, no people [STYLE] Avoid: [NEG]
- `M08_src.png`
A long courthouse corridor receding into cold institutional light with closed doors along it, framed for a slow forward move, no people, no readable signage [STYLE] Avoid: [NEG]
- `M09_src.png`
An empty counsel chair pulled up to a vacant defense table in a courtroom under cold light, the missing voice rendered as an empty chair, still and poised, no people, no readable text [STYLE] Avoid: [NEG]
- `M10_src.png`
An old leather-bound law volume closed on a dark desk under a warm lamp with dust hanging in the light, still and poised, its title abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `M11_src.png`
The pale marble colonnade of the United States Supreme Court at night lit from below, monumental and still, poised for a slow move, no people, no readable inscription [STYLE] Avoid: [NEG]
- `M12_src.png`
A hard single line of light dividing a cold marble floor into two unequal sides, a willful refusal and a genuine inability held apart, still and poised, symbolic, no people, no text [STYLE] Avoid: [NEG]
- `M13_src.png`
A folded settlement document on a plain table under a warm lamp, a rule written out a second time by hand, still and poised for a slow push, the lines abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `M14_src.png`
An open empty wallet lying flat on a kitchen table in warm lamplight, nothing inside it, still and held, no legible text, no people [STYLE] Avoid: [NEG]
- `M15_src.png`
A heavy door beginning to open onto a bar of warm daylight at the end of a cold corridor, poised and still, no people, no readable sign [STYLE] Avoid: [NEG]
- `M16_src.png`
A lone bus-stop pole and an empty road under a grey dawn sky turning slowly toward morning, still and open-ended, no people, no readable sign [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_tekoh.py` を下敷きにパスと SHOTS だけ差し替え）

```python
HOST = "http://127.0.0.1:8188"                              # ローカル ComfyUI
HIGH = "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors"
LOW  = "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors"
VAE  = "wan_2.1_vae.safetensors"       # ★2.1（2.2 ではない・無言の品質劣化の原因）
CLIP = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
WIDTH, HEIGHT = 1280, 720
FRAMES = 41        # 4090 の全ロード上限@720p（81 で部分ロード=3倍遅い）
STEPS = 40 / SPLIT = 20 / SHIFT = 5.0   # ★SHIFT 5.0（8.0 は 5B からの無言持ち越しでバグ）
CFG = 3.5 / SAMPLER,SCHEDULER = "euler","simple" / FPS = 16
STILL_DIR     = H:\pd-media\assets\ai\cleveland      # 種画像 M<NN>_src.png を読む
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\cleveland
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, text, watermark, identifiable face, real person likeness, child, crying person, gore, blood"
```

**ゲート:** `dry_validate`（length=5 で1回POSTして配線エラーを安く検出）/ `assert_loaded_completely`（部分ロード検出）/ `assert_frame_math`（フレーム計算）。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す）

```bash
py -3.11 scripts/comfy_wan_cleveland.py --build            # グラフだけ（GPU触らない）
py -3.11 scripts/comfy_wan_cleveland.py --run --shot M01   # 1本本番して目視
py -3.11 scripts/comfy_wan_cleveland.py --run-all          # 残り15本（冪等・既存スキップ）
```
1本 24–73 GPU分・16本で 7–19時間。`/queue` `/history` を30秒間隔でポーリング。

## 8.4 RIFE で 48fps 化（`rife_cleveland.py`・`rife_tekoh.py` と同手順）

```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは length=5 検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番にリネーム → RIFE 2x を**2回**（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. **フレーム数検証** `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC

- 顔・身体・子ども・扇情（泣く人）が生成されていないこと（NEG で抑えているが**必ず目視**・制約4）
- モーフィング/ちらつき/ワープが無いこと → あれば別シードで再生成
- M05/M16（道路・バス停）は**識別可能な人物・車のナンバー・読める標識**が写り込んでいないこと（制約2）
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（16本 × 2回 = 32カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど12本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **6本** | 大理石法廷の埃・書庫の塵。黒背景 drift を screen 合成 |
| `light_assets` | **4本** | 暖色ランプ・冷たい fluorescent・大理石の光条・夜明けの採光 |
| `vfx_overlays` | **2本** | 微細なグレイン・冷たい光ノイズ |
| **合計** | **12本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/cleveland/overlay/` に置き、`cleveland_film.json` の `cuts[].src` には**出さない**（出すと factory 判定で1回制限を食う）。同じレイヤーを何度重ねてもよい（素材ではなく加工）。黒背景でループするものを選び `blend_hint` を書く。**§7.5 の目視QC対象**（12本・12分）。**合成レイヤーの発色は B が accent `#B23A48`（督促の朱）に寄せる想定・A は色被りの素材を作らない（他話の gold/blue/amber/teal を選ばない）。**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --kind video --query dust_particles --limit 20 --exclude-used --ep PD-2026-045-cleveland --json
```

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_cleveland_assets.py`）

```
remotion/public/cleveland/img/     ← role=body の静止画84枚（+ 同名 _depth.png）
remotion/public/cleveland/factory/ ← 選定 factory .mp4 92本
remotion/public/cleveland/motion/  ← i2v M<NN>_rife.mp4 16本
remotion/public/cleveland/overlay/ ← 合成レイヤー 12本
```
- `public_path` はマニフェストの値と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー（`import_to_remotion.py` の `conform_video(...,fps=30)` と同じ）
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する・外すと誤分類）:**
- factory の `public_path` は必ず `cleveland/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も**含めない**
- 合成レイヤーは `cleveland/overlay/` に置き `cuts[].src` に出さない

> **B のレンダは `--public-dir=public_slim`（Root.tsx に `id="Ep45Cleveland"`）を使う想定だが、`public_slim` の構築は B の責務。** A は `remotion/public/cleveland/` に正典を置くところまで（B が slim を派生させる）。

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`

全静止画・i2v・factory・overlay を1行ずつ: `asset_id`/`path`/`source`（`ai_codex` or `factory`）/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力

```bash
./.venv/Scripts/python.exe scripts/build_cleveland_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_cleveland_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_cleveland_asset_manifest.py --reuse-feasibility
```
この3つが exit 0 で「マニフェストが本番になった」。**Bのファイルを直接書き換えて知らせようとしない。**

---

# 11. 素材反復禁止ゲートの実仕様（`check_asset_reuse.py`）

```python
MAX_USES_FACTORY = 1        # 無料 + 11,000本超 → 繰り返す理由が無い
MAX_USES_MOTION  = 2
MAX_USES_STILL   = 2
MIN_FIRST_USE_SHARE = 0.70
```
種別判定は**パス文字列**（`kind_of()`）: `/factory` or `af-bg-` → factory / `.mp4|.mov|.webm` or `ai_video` or `_rife` → motion / それ以外 → still。§10.1 の命名規則を守る。

EP45 の設計値: still 100/84=1.19(≤2) / factory 92/92=1.0(≤1) / motion 32/16=2.0(≤2) / first-use 192/224=0.8571(≥0.70)。**全て達成可能。**

---

# 12. 絶対にやらないこと

- **EP39（frazier）/EP40（lech）/EP41（thompson）/EP42（young）/EP43（caniglia）/EP44（tekoh）のファイルに一切触らない。** 読み取りのみ可。素材・色（EP41 gold #E5B53A / EP42 blue #3B7DD8 / EP43 amber #E0913C / EP44 teal #2FA6A0）・音のレーンも分離。EP45 の accent は **crimson #B23A48（督促の朱）**（INK #0A0A0C・B が OP/AEカード/サムネで使用・A は絵で流用色を作らない）。
- **スレッドBの所有ファイル（§0.2）に触らない。** 特に `remotion/src/**` `scripts/ae/**` `scripts/build_cleveland_film.py` `manifest.json` `04_scenes/shotlist*` `figures`。
  - **ただし `04_scenes/ai_prompts.v001.md` は A が書く**（`generate_sdxl_4k.py` の入力・§5.9/§8.1a）。B は読むだけ。
- **図解・トランジション・タイポの素材を探しに行かない。** 在庫が薄い/無いカテゴリは B が自作する。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。ローカル A1111・ComfyUI・RIFE は GPU を使うだけで課金なし（オーナー許可済み）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness・身体をどこにも作らない**（§1・制約4）。特に **Harriet Cleveland を個人として描かない**。
- **6制約に反する文言・絵をプロンプト・タグ・注記・ファイル名のどこにも作らない**（§1.2/§1.3）:
  - 「合法/正当（legal/lawful）」化（制約1）／「もう完全に無くなった」（制約1）／「最高裁がClevelandを救った」（制約2）／「全罰金違憲」（制約3）／扇情（poverty porn・泣く人・子ども）（制約4）／個人攻撃・同定（制約5）／可読の金額/日付/判例番号/会社ロゴ（制約2/6）。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。反復回避は distinct 84 で担保（§0.1・§5.6）。
- **role=thumb / still_thumb を作らない・overlay を12本以外にしない。** サムネは also_thumb=true の body 6枚（§4.3 = {S01,S03,S18,S46,S68,S84}）。
- **★dochighlight figure（黒バー/box/underline）を作らない・言及しない。** これは figures の責務（B）だが、A の `tags`/`caption_hint`/`notes` にも `dochighlight` という文字列を書かない（grep で 0 を保つ）。
- **枚数・本数を「だいたい」で決めない。** §3 の確定値（still 84 / factory 92 / i2v 16 / distinct 192 / first-use 0.8571 / still-share 0.4464 / MG≥30 / 11.9分）と §3.3 の検算をそのまま使う。合わなければ実装ではなく**本書を疑って報告**。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** EP36は大聖堂を、EP38は牛を通した。**生成物・在庫クリップを実際に見る**（特に制約2/4は目視でしか守れない・書面の可読文字・会社ロゴ・扇情描写も目視で排除）。

---

# 13. 完了報告に含めるもの

```
1. accepted 静止画の枚数と内訳（body 84 / i2v_source 16 / also_thumb 6 [S01/S03/S18/S46/S68/S84] / reject N）
2. factory 選定 92本のリスト（asset_id / subtype / eyeballed_content）と、subtype と食い違って外した本数、書面/道路クリップの「no readable text / no logo」確認
3. EP39/EP40/EP41/EP42/EP43/EP44 重複ゼロの確認結果
4. i2v 16本の frames / duration_sec と、SHORT? の有無
5. 合成レイヤー12本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code をそのまま貼る）
7. §3.3 の検算 [1]〜[7] を自分で再計算した結果
8. asset_manifest.v001.json の counts ブロック（still_body 84 / still_i2v_source 16 / motion 16 / factory 92 / overlay 12）
9. 6制約・1枚前提の自己申告（合法化/全罰金違憲/最高裁がClevelandを救った/完全消滅/扇情=poverty porn が全出力に皆無・バリエーション0・Cleveland 非人物化を目視確認・dochighlight 文字列ゼロ・A↔B同一スキーマ [schema cleveland_assets.v1 / role enum body|i2v_source|reject / counts / also_thumb 集合 {S01,S03,S18,S46,S68,S84} / overlay 12]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
