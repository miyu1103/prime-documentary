# EP47 mahanoy — Codex スレッドA「素材生成」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN）も実装スレッドB（CODEX_B）のファイルも**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> **唯一の外部真実 = `episodes/_planning/EP47_mahanoy_PRODUCTION_SPEC.v001.json`**（機械生成）。本書の数値はそこから転記したものであり、手書きで発明していない。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP47 / Episode ID: PD-2026-047-mahanoy / slug: mahanoy
Composition id: Ep47Mahanoy（B が Root.tsx に登録・A は staging まで）
事件:       Mahanoy Area School District v. B. L., 594 U.S. ___ (2021), No. 20-255。
            JV チアリーダーの B.L.（＝Brandi Levy・当時未成年）が varsity 落選に腹を立て、
            土曜・校外（Cocoa Hut コンビニ）で Snapchat に怒りの投稿（24時間で消える story・友人約250人）。
            学校は JV から翌年度1年間出場停止。最高裁は 8-1 で B.L. 勝訴（Breyer 法廷意見／Thomas 単独反対／Alito 補足[Gorsuch 同調]）。
            主題は「校外言論を学校は"一切"罰せないとは言っていない。処分は違憲としつつ規制余地を残した
            （diminished, not gone）」。アンカーは Tinker v. Des Moines(1969)「schoolhouse gate」。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**85本の固有プロンプト × 1枚 = 85枚**・バリエーション0） | `H:\pd-media\assets\ai\mahanoy\S<NN>.png` | 2–3.5時間（GPU） |
| A-1b | i2v 種画像の生成（**16本の固有プロンプト × 1枚 = 16枚**・バリエーション0） | `H:\pd-media\assets\ai\mahanoy\M<NN>_src.png` | 30–50分（GPU） |
| A-2 | 静止画のQCと目視（**目視必須**） | `05_visuals/still_qc.v001.json` + コンタクトシート | 1.5時間 |
| A-3 | depth map 生成（`treatment:"depth"` の必須入力） | `H:\pd-media\assets\ai\mahanoy\S<NN>_depth.png` | 20分 |
| A-4 | factory 実写クリップ **92本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | **2.5時間（うち目視だけで1時間以上）** |
| A-5 | i2v モーション化 **16本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\mahanoy\M<NN>_rife.mp4` | 7–19時間（GPU） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 | `05_stock/overlay_selection.v001.json` | 30分 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 20分 |
| A-8 | Remotion public への staging | `remotion/public/mahanoy/{img,factory,motion,overlay}/` | 30分 |

> **★★ 最重要の前提（EP42–45 から継続）: 1シーン1枚・バリエーション0 ★★**
> Codex の画像生成は高精度。**同一ショットの複数バリエーション（`_02`/`_03`）を作らない。**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 85本＝85行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **`--variants 1`**（または variants 指定なし）で回す。**`--variants 3` は使わない。**
> **総生成画像 = still 85 + i2v 種 16 = 101枚（各1回）。** factory 92本は生成でなく在庫からの選抜。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-047-mahanoy/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** Bはスタブで全パイプラインを完走できるので、Aの完了を待っていない。**A も急がなくてよいが途中経過を壊すな。** このマニフェストは **A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致**で共有する（§4）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\mahanoy\**` / `H:\pd-media\assets\ai_video\mahanoy\**` | **A** | 読み書き |
| `episodes/PD-2026-047-mahanoy/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-047-mahanoy/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/mahanoy/{img,factory,motion,overlay}/**` | **A** | 読み書き |
| `episodes/PD-2026-047-mahanoy/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_mahanoy_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-046-*/**` および EP39〜46 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

> **★命名衝突の警告（EP47 固有）:** 旧 `PD-2026-011-mahanoy`（別話・過去作）が既に存在し、`build_mahanoy_audio_v001.py` `gen_narration_mahanoy.py` `compose_mahanoy_thumbnail_v002.py` 等の旧スクリプトが `scripts/` に残っている。**それらは EP47 とは無関係。触らない・上書きしない。** EP47 の新規スクリプトは §0.3 の名前（`select_mahanoy_factory.py` 等）で新規に作る。出力先も必ず `PD-2026-047-mahanoy` / `H:\pd-media\assets\ai\mahanoy\`（新 slug パス）で、旧話のパスに書かない。

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を `read_prompts()` で読む） | `PD-2026-047-mahanoy --variants 1` / `47 --variants 1 --only S01` |
| `scripts/gen_depth_maps.py`（**既存**） | §6.4 の depth map | `--dir "H:/pd-media/assets/ai/mahanoy"` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-047-mahanoy --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit 96 --exclude-used --ep PD-2026-047-mahanoy --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-047-mahanoy` |

**★Aが新規作成するスクリプト（EP45 の cleveland 版を mahanoy 用に複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（複製元・EP45） |
|---|---|---|
| `scripts/qc_mahanoy_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_cleveland_stills.py` |
| `scripts/select_mahanoy_factory.py` | §7 の factory 92本の確定選定・EP39〜46 sha256 除外検証 | `scripts/select_cleveland_factory.py` |
| `scripts/comfy_wan_mahanoy.py` | §8 の i2v 16本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_kidsforcash.py`（最新の実在版・`ls scripts/` で確認してから複製） |
| `scripts/rife_mahanoy.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_kidsforcash.py`（実在版・要 ls 確認） |
| `scripts/build_mahanoy_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_cleveland_asset_manifest.py` |
| `scripts/stage_mahanoy_assets.py` | §10 の staging | `scripts/stage_cleveland_assets.py` |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある（`read_prompts()` で `04_scenes/ai_prompts.v001.md` を読む）。あなたは **`ai_prompts.v001.md` を §5.2 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない**（上の複製元が実在することを `ls scripts/` で確認してから複製する。`comfy_wan_*`/`rife_*` は最新の実在版を複製元にする）。
> **正確性ゲートは `check_mahanoy_facts.py`（B が実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の6制約に一致し、`check_mahanoy_facts.py` を将来通せる文言でなければならない（R-OVERCLAIM / R-VOTE / R-QUOTE / R-MINOR）。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_mahanoy_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_mahanoy_asset_manifest.py --reuse-feasibility
#   → still >=85 / motion >=16 / factory >=92 / distinct 合計 >=193 / first-use >=0.70

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_mahanoy_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全92本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-047-mahanoy
#   → exit 0（factory_clip_qc.v001.json が staging 済み全クリップを reviewed:true で網羅）

# [A-DONE-5] EP39〜EP46 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_mahanoy_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39・EP40・EP41・EP42・EP43・EP44・EP45・EP46 の八つすべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（R1 ＋ 正確性6制約）★★★

**本件は生徒の言論の自由の物語。最高裁は「学校は校外言論を"一切"罰せない」とは言っていない（過大化禁止）。処分を違憲としつつ規制余地を明示的に残した（diminished, not gone）。B.L.（＝Brandi Levy）は当時未成年＝最大限配慮：顔・肖像・身体を一切描かない・象徴のみ。投稿の罵倒語・卑語・中指ジェスチャーを一切再現しない（象徴/ぼかしのみ）。未成年の苦痛を扇情化しない。完全に広告安全。**

## 1.1 R1（生成ビジュアル全般）

1. **実在人物の顔・likeness・肖像を作らない。** B.L.（＝Brandi Levy・当時未成年 R2）・Breyer・Thomas・Alito・Gorsuch を**顔・身体・肖像として描かない**。人物は原則「人を出さない」（象徴オブジェのみ）。判事評言の逐語引用は AE カード（B の担当）であって画像ではない。**未成年（B.L.）は絶対に肖像化しない。**
2. **実在の判決文・判例番号・条文・日付を再現しない。** 投稿画面・出場停止通知・意見書・カレンダー・名簿は雰囲気のみ（判読不能）。判例番号（594 U.S. ___ / No. 20-255 / 393 U.S. 503）・日付（2021-06-23）・票決（8-1）は**画像に描かない**（AE/figures のタイポで出す＝B の担当）。ロゴ（Snapchat 等の商標）は**描かない/ぼかして判読不能**にする。
3. **罵倒語・卑語・中指ジェスチャーを画像に一切出さない。** 投稿は常に「ぼかし/ピクセル化した抽象タイル」として象徴化する。読める卑語・中指・扇情的な怒りの描写を作らない（制約4）。
4. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性6制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **過大化しない（R-OVERCLAIM）。** 最高裁は「学校は校外言論を一切罰せない」とは言っていない。処分を違憲としつつ **規制余地を明示的に残した**（serious bullying/harassment・threats・cheating やレッスン/論文/PC規則違反・school security の突破）。bright-line を意図的に設定せず。**「schools can never punish/regulate/touch off-campus speech」「off-campus speech is always protected」「students can post anything off campus」「a free-fire zone」を書かない。** 許容は "diminished, not gone" / "the school's interest is weakest here" / "the Court left categories open" / "no bright-line rule"。
2. **Tinker(1969)＝アンカー（R-QUOTE）。** 生徒は「校門で言論の自由を脱ぎ捨てない（do not shed ... at the schoolhouse gate）」が、実質的混乱は規制可。校外では学校の Tinker 利益が **diminished（消滅でなく減退）**。**「Tinker was overruled」「rights disappear off campus」を書かない。** Tinker "schoolhouse gate"／Breyer "nurseries of democracy" は台帳一致の逐語で、逐語引用は AE カード（B）であって画像ではない。
3. **票決 8-1・帰属を正確に（R-VOTE）。** Breyer 法廷意見／**Thomas 単独反対**／Alito 補足（Gorsuch 同調）。多数/反対/補足を中立帰属。**票決を 7-2 や 9-0 と書かない・反対者を Thomas 以外にしない・「unanimous」と書かない。**
4. **B.L.（Brandi Levy）は R2（当時未成年）＝最大限配慮（R-MINOR）。** 顔・肖像・身体を描かない。象徴のみ（土曜のコンビニ駐車場・車のダッシュボードの携帯・送信ボタンに親指・24時間カウントダウン・フックに掛かった空のチア制服・空の観客席/体育館・ロッカー・校門/校舎の廊下・裁判所の長い廊下・苗床/若木）。**罵倒語・卑語・中指ジェスチャーを一切再現しない**＝投稿は常に「an angry post / a frustrated Snap」の象徴（ぼかしタイル）。**未成年の苦痛を扇情化しない（泣く少女・distress を作らない）。**
5. **広告適合。** 生徒の言論の自由の物語として枠付け。未成年の苦痛を煽らない・slur/卑語を出さない。完全に広告安全。
6. **数値・引用は台帳一致・捏造ゼロ。** 8-1・JV cheer・varsity 落選・Cocoa Hut・約250人 story・24時間・1年出場停止・Third Circuit が「Tinker は校外に及ばず」と広く判断・混乱は「Algebra で数分＋数名の動揺」程度。**画像には描かない**（判読不能・数値は AE/figures＝B）。confidence:medium（"first time in more than fifty years" の枠付け＝F20）は B のカードでヘッジ帰属を維持。

## 1.3 機械ゲート（`build_mahanoy_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
BANNED_PORTRAIT = re.compile(
    r"\bportrait\b|\bmugshot\b|likeness of|"
    r"face of (b\.?l\.?|brandi|levy|breyer|thomas|alito|gorsuch)|"
    r"recognizable (real )?person|identifiable face|deepfake|深偽|ディープフェイク|"
    r"\b(teen(age)?|young) girl\b|\bminor\b(?! depicted)|crying (girl|teen|student|child)",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"schools? can (never|not) (punish|regulate|touch|reach)[^.]{0,40}off.?campus|"
    r"off.?campus speech is (always|fully|completely) protected|"
    r"students? can (say|post) anything off.?campus|free.?fire zone|"
    r"tinker (was |is )?overrul|rights (disappear|vanish) off.?campus|"
    r"(vote|decided|ruled) (7.?2|9.?0|unanimous)|unanimous(ly)?|"
    r"(profanity|slur|curse word|obscene gesture|middle finger) (shown|visible|reproduced)|"
    r"crying (girl|teen|minor|child)|weeping (girl|family)|"
    r"poverty ?porn|child in distress|minor in distress",
    re.IGNORECASE)
```

> `BANNED_ACCURACY` は制約1〜4・6を機械化したもの。プロンプト・タグ・`caption_hint`・注記のどこにも該当語を書かない。**"diminished, not gone" / "the school's interest is weakest here" / "the Court left categories open" / "no bright-line rule" / "8-1" は許容（射程を正しく限定）。** 禁止は「校外は治外法権」化・「校外は常に保護」化・「Tinker 破棄」・票決誤り・卑語/中指/未成年の扇情の露出だけ。

---

# 2. 台本の語数と尺の確定値（SPEC から転記・Aが素材点数を積算する根拠）

**★唯一の真実 = `episodes/_planning/EP47_mahanoy_PRODUCTION_SPEC.v001.json`。** 古い資料の wpm・語数は使うな。

```
words_total          = 2,131
narration_seconds    = 717.9   （= 11.96分・[DESIGNED SILENCE 1..3] の実音無音を含む）
wpm_used             = 178.1
総尺（設計）          = 717.9 + BrandOpening 3.50 + BrandEndcard 9.00 = 730.4秒 = 12:10  ≤ 750s
                        （durationInFrames 4項＋hookSeconds=8.0 の合成尺 ≈752s は B の領域。A は narration 予算だけ使う）
視覚シーン(narrative)  = 48（S01..S48・SPEC derive）
Act 構成（SPEC 秒）: HOOK 66.4 / OPENING 28.3 / BODY 480.7（ACT1+ACT2+ACT3）/ ENDING 117.6
```

**Aにとっての意味は1つ:** > **225カット / distinct 193 / 初出85.78% = still 85 + factory 92 + motion 16。**（§3 で積算）

> **注意（命名差）:** SPEC の視覚シーンは S01..S48。しかし **still は 85 本の固有プロンプトを持つ**ため、still の資産 ID は **S01..S85**（1プロンプト＝1枚）で採番する。48 の narrative シーンに 85 枚を配分する（ドクトリン核の ACT3 が最も厚い）。**still 資産 ID（S01..S85）と narrative シーンコード（S01..S48）は別物。** `covers_scene_id` は still 資産 ID 空間を指す（§7.3）。

---

# 3. ★素材構成の確定値（SPEC の distinct/cuts をそのまま調達する）

## 3.1 SPEC の内訳（★この値で調達する・勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **85枚** | 101カット | 1.19回(≤2) | **85本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **92本** | 92カット | **各1回(1)** | 在庫 11,000本超から選抜（§7）・全点目視・EP39〜46 と sha256 被りゼロ |
| **i2v モーション** | **16本** | 32カット | 各2回(≤2) | 16本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **193点** | **225カット** | | |
| 合成レイヤー（particle/light/vfx） | 12本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |

**SDXL の生成バッチ（本編カットに出ない i2v 種を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **85枚** | 85プロンプト × 1枚（バリエーション0） |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **16枚** | 16種プロンプト × 1枚（バリエーション0） |
| **SDXL 生成バッチ合計** | **85 + 16 = 101枚（各1回）** | **`--variants 1`** |

> **サムネは新規生成しない。** 完成後に body 85枚から6枚を `also_thumb:true` で流用選抜（追加生成ゼロ＝1シーン1枚前提を崩さない）。**role=thumb / still_thumb を作らない。**

> **★紙芝居回避（EP40 の最大の失敗）:** **still-cut 101 / (factory 92 + i2v 32)=video 124** で **still-share 44.89% ≤45%・motion coverage 55.11% ≥45%** を構造的に保証する（§3.3）。**stillを増やしてfactoryを削るな。factory 92 が still-share≤0.45 を守る下限。**

## 3.2 still 85枚・factory 92本・i2v 16本の幕別配分（目安）

| 区間 | narration秒 | still（S番号） | factory | i2v |
|---|---|---|---|---|
| HOOK | 66.4 | 4（S01–S04） | 6 | 2（M01,M02） |
| OPENING | 28.3 | 3（S05–S07） | 3 | 0 |
| ACT1 "A Saturday, a phone, a squad" | ~120 | 13（S08–S20） | 12 | 3（M03,M04,M05） |
| ACT2 "The schoolhouse gate" | ~175 | 19（S21–S39） | 16 | 4（M06,M07,M08,M09） |
| ACT3 "Diminished, not gone" | ~185 | 28（S40–S67） | 24 | 4（M10,M11,M12,M13） |
| ENDING | 117.6 | 18（S68–S85） | 12 | 3（M14,M15,M16） |
| 繋ぎ（covers_scene_id:null） | — | — | 19 | — |
| **合計** | **717.9** | **85** | **92** | **16** |

> ACT3 は「diminished, not gone」のドクトリン核（8-1・3特徴・nurseries of democracy・4類型・Alito 補足・Thomas 反対）なので still も最多の28枚。
> **★幕別の factory 内訳（この表・§7.2・CODEX_B）は非拘束の目安値**（合計 92 のみ確定・幕割当は柔軟）。ゲートは factory を各1回・合計 92 でしか見ない。**確定値は「合計 factory 92」だけ。**

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 225 = still 101 + factory 92 + i2v 32
[2] 平均ショット長 = narration 717.9 / 225 = 3.191秒/カット  ✓ (SPEC mean_shot 3.19・≤6.0)
[3] 静止画占有率(check_animation_mix) = 101/225 = 44.89%  ✓ ≤45%（SPEC still_share 0.4489）
[4] motion coverage = (92+32)/225 = 124/225 = 55.11%     ✓ ≥45%
[5] per-asset 上限: still 101/85=1.19(≤2) / factory 92/92=1.0(≤1) / motion 32/16=2.0(≤2)  ✓
[6] first-use share = 193/225 = 0.8578                   ✓ ≥0.70（SPEC 一致）
[7] factory 下限: video を 124 カット以上に保たないと still-share が 0.45 を超える。
    i2v 32 は固定なので factory は 92 を下回れない（92+32=124）。→ factory 92 は下限であり水増しではない。
```

> **[3] の余裕は 0.11% しかない（101/225=0.44889・cap 0.45・差 0.0011）。** still が85本を割ったら §6.3 の再生成で回復させ、**still-cut 101 を増やさない**（B側の shotlist が101で固定）。**factory を92未満にすると即 still-share>0.45 で FAIL。**

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-047-mahanoy/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `mahanoy_assets.v1`（固定文字列）
**生産者:** `scripts/build_mahanoy_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致。** role enum は **`body | i2v_source | reject` のみ**（`thumb`/`still_thumb` を作らない）。サムネは `also_thumb:true` の body still **ちょうど6枚**。overlay は **ちょうど12本**。

## 4.1 スキーマ（EP45 の `cleveland_assets.v1` と同型。counts を EP47 値に）

```jsonc
{
  "schema_version": "mahanoy_assets.v1",
  "episode_id": "PD-2026-047-mahanoy",
  "slug": "mahanoy",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_mahanoy_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 85,          // ==85
    "still_i2v_source": 16,    // ==16
    "motion": 16,              // ==16
    "factory": 92,             // ==92
    "overlay": 12              // ==12（distinct 素材に数えない）
  },
  "stills": [{
    "asset_id": "MAHA-S01",                // body: ^MAHA-S\d{2}$（1..85） / i2v種: ^MAHA-MS\d{2}$
    "scene_id": "S01",                     // still 資産 ID（§5.9 のプロンプト行に対応・S01..S85 空間）
    "role": "body",                        // body|i2v_source|reject（バリエーション概念なし＝各1枚）
    "also_thumb": false,                   // body から6枚だけ true（追加生成しない）
    "act": 0,                              // 0=HOOK/OPENING, 1=ACT1, 2=ACT2, 3=ACT3, 5=ENDING
    "path": "H:/pd-media/assets/ai/mahanoy/S01.png",
    "depth_path": "H:/pd-media/assets/ai/mahanoy/S01_depth.png",   // role=="body" は実在必須
    "public_path": "mahanoy/img/S01.png", // role=="body" のみ非null
    "width": 3840, "height": 2160,         // 長辺>=3840
    "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 34.2,
    "tags": ["phone_screen","countdown","parking_lot","symbolic","weekend"],
    "caption_hint": "a phone face-up on a car dashboard in an empty convenience-store lot with a faint 24-hour countdown glowing, no legible text",  // check_mahanoy_facts 検査対象（制約1-6）
    "seed": 0, "model": "juggernautXL_ragnarokBy",
    "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
    "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
           "has_identifiable_face": false, "has_human_body": false, "notes": ""}
  }],
  "motion": [{
    "asset_id": "MAHA-M01",                // ^MAHA-M\d{2}$（1..16）
    "source_scene_id": "M01_src",
    "source_still": "H:/pd-media/assets/ai/mahanoy/M01_src.png",   // role=="i2v_source" の画像
    "path": "H:/pd-media/assets/ai_video/mahanoy/M01_rife.mp4",
    "public_path": "mahanoy/motion/M01_rife.mp4",
    "act": 0, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
    "sha256": "<64hex>", "tags": ["send_button","thumb"],
    "qc": {"reviewed": true, "on_theme": true, "artifact_free": true,
           "has_identifiable_face": false, "notes": ""}
  }],
  "factory": [{
    "asset_id": "AF-BG-0731",              // 棚 assets/asset_manifest.v001.json の id をそのまま
    "path": "H:/pd-media/assets/factory/backgrounds/AF-BG-0731__...mp4",
    "public_path": "mahanoy/factory/AF-BG-0731__...mp4",
    "type": "backgrounds", "subtype": "<label>",   // ★ラベル=検索語の記録。中身の保証ではない（§7.5）
    "kind": "video", "license": "Pexels License",  // ALLOWED_LICENSES のいずれか
    "sha256": "<64hex>", "act": 2, "covers_scene_id": "S22",  // §7.3 の割当のみ。繋ぎは null
    "duration_sec": 7.60, "width": 1920, "height": 1080, "mean_luma": 40.1,
    "eyeballed_content": "a small-town school entrance seen frontally in cold light, no people",  // ★必須（§7.5）
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
           "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""}
  }],
  "overlay": [{
    "asset_id": "AF-PART-0044", "path": "H:/.../particle_assets/...mp4",
    "public_path": "mahanoy/overlay/...mp4", "type": "particle_assets", "subtype": "<label>",
    "license": "Pexels License", "sha256": "<64hex>", "blend_hint": "screen",
    "eyeballed_content": "slow dust motes drifting on black, loops cleanly",
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""}
  }]
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `schema_version=="mahanoy_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 85 / i2v_source 16 / motion 16 / factory 92 / overlay 12）に**一致**
3. 全 `path`/`depth_path`/`public_path` がディスクに実在
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `depth_path` と `public_path` が非null かつ実在
7. `qc.has_readable_text==true` / `qc.has_identifiable_face==true` / `qc.has_human_body==true` のいずれかは `role=="reject"`
8. `role=="i2v_source"` は `role=="body"` と**同一 asset_id を共有しない**（distinct 分離。i2v_source は `MAHA-MS\d{2}`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39〜EP46 の staged 素材**と1件も衝突しない（§7.7・八つ）
12. `factory[].eyeballed_content` が空でない（＝目視していない本が混じっていない）
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど6**、かつ **`scene_id` 集合が `{S01,S03,S13,S16,S22,S68}`（§4.3）と完全一致**（追加生成ではなく body からの流用。**この集合は CODEX_B §11 と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|reject のみ）
16. `overlay` 配列長が**ちょうど12**

`--reuse-feasibility` では §3.3 [5][6][7] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 85枚（S01..S85）= §5.9 の85プロンプトの生成物。各1枚。
2. i2v_source 16枚（MS01..MS16 / 種画像 M01_src..M16_src）= §8.1 の16種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. also_thumb : body のうち S01 / S03 / S13 / S16 / S22 / S68 の6枚に true（追加生成しない）
     - S01 スマホ＋24時間カウントダウン（駐車場・HOOK）
     - S03 送信ボタンに掛かる親指（HOOK）
     - S13 空の観客席/体育館（ACT1）
     - S16 フックに掛かった空のチア制服（ACT1）
     - S22 校門/校舎の入口（schoolhouse gate・ACT2）
     - S68 駐車場に回帰したダッシュボードのスマホ（ENDING）
4. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

---

# 5. A-1: SDXL 静止画のバッチ生成（85本 × 1枚・バリエーション0）

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-047-mahanoy/04_scenes/ai_prompts.v001.md   ← A が §5.2 の形式で書く
出力:  H:\pd-media\assets\ai\mahanoy\S<NN>.png（+ remotion/public/mahanoy/ に自動コピー）
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
- `ai_prompts.v001.md` は **body 85行（S01..S85）＋ i2v 種 16行（M01_src..M16_src、§8.1a）＝ 101 エントリ**を書く。すべて1枚生成。

## 5.3 生成コマンド（★`--variants 1`。`--variants 3` は使わない）

```bash
# まず1枚だけ回して読める行数を確認（★shots=101 でなければ形式が壊れている）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 47 --variants 1 --only S01
#   → ログ "episode=... shots=101 variants=1 ... -> 101 images" の shots が 101 であること

# 全101枚（body 85 + i2v種 16・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-047-mahanoy --variants 1
#   → 生成 S01.png ... S85.png / M01_src.png ... M16_src.png（各1枚。_02/_03 は作らない）
```

> QC で落ちたシーンの再生成は `--only S37`（**同じプロンプトで別シードを1枚**）。既存の>=3840はスキップ・不足だけ埋まる。**バリエーションを増やして水増ししない。枚数を減らして基準を下げるのも禁止。**

## 5.4 共通スタイル `[STYLE]`（全プロンプト末尾に必ず全文連結）

```
, cinematic still, dark documentary grade, a cold night-blue base lit by the glow of a phone screen, a single digital-violet accent (#7A5CD0) as the one cool light note, an ordinary small Pennsylvania town of empty convenience-store parking lots, quiet school interiors, and long courthouse corridors, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, no minor depicted
```

> **EP39〜EP46 との分離:** `navy interrogation room`/`electric blue`（EP39）・`midday sunlight`/`suburban demolition`/`bleached daylight`（EP40）・`prison cell`/`cellblock`/`sodium prison corridor`/`steel death-row`（EP41）・`Chicago apartment`/`ankle monitor`/`body-worn camera vest`（EP42）・`porch-amber house`/`ambulance red lights`/`tow-truck`（EP43）・`teal-green hospital corridor`/`clinical hospital`（EP44）・`warm working-class kitchen table`/`overdue crimson`/`county-jail booking`（EP45・crimson）・EP46 の green レーンの絵柄を**1語も含めない**。EP47 は **デジタル・バイオレット #7A5CD0** の夜青ベース：土曜のコンビニ駐車場（無人）＋ダッシュボードのスマホ・送信ボタンに親指・24時間カウントダウン＋空の体育館/観客席・フックの空チア制服・ロッカー＋校門/校舎の廊下＋1969の黒い腕章のシルエット（Tinker・顔なし）＋裁判所の長い廊下＋若木/苗床（nurseries of democracy）＋校内 vs 校外の対比。**#7A5CD0 は紫寄りのバイオレットで、EP42 の青 #3B7DD8 とも EP39 の electric blue とも別（NEG で両者を排除）。**

## 5.5 共通ネガティブ `[NEG]`（各 `Avoid:` の後に必ず全文付ける）

```
text, words, letters, numbers, captions, legible screen text, legible post, legible caption, profanity, slur, curse word, obscene gesture, middle finger, raised finger, watermark, logo, brand logo, snapchat logo, readable document, legible citation, legible case number, legible date, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, minor, teenager, teenage girl, child, girl, human face, human body, crying person, weeping family, distressed teen, sensational distress, poverty porn, weapon, gun, blood, gore, nude, bare skin, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, electric blue, navy interrogation room, prison cell, steel cellblock, sodium prison corridor, teal-green hospital corridor, clinical hospital, porch amber house, ambulance, tow truck, ankle monitor, warm crimson kitchen table, county jail booking, forest green
```

> ネガティブにも **制約違反語（"schools can never punish off-campus", "off-campus speech is always protected", "free-fire zone", "Tinker overruled", "unanimous", poverty porn 語 等）を書かない**（§1.3）。上のリストにも含めていない。**卑語・中指・未成年の身体/顔・扇情・可読の投稿文/判例番号/日付・商標ロゴを NEG で明示的に抑制**（制約2/4）。ロゴが写り得る絵（スマホ画面・請求）は「blurred into an unreadable smear」で判読不能にする。

## 5.6 バリエーション軸（★EP47 では無効）

`generate_sdxl_4k.py` の `--variants 1` は各 stem を**1枚だけ**生成する。**`_02`/`_03` を作らない。** 反復回避は「85本の固有プロンプト＝85の別被写体」で担保する。

## 5.7 メタJSON

`generate_sdxl_4k.py` は画像を書くが per-image メタJSONは書かない。**A は QC 時に `qc_mahanoy_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.8 プロンプトの絶対ルール（85本すべてに適用）

- **顔なし・身体なし・裸体なし・未成年を出さない。** 人物は原則出さない（制約4・R1）。B.L.（Brandi Levy・未成年）を個人として描かない。
- **可読文字なし。** 投稿画面・出場停止通知・意見書・名簿・カレンダーは雰囲気のみ（判読不能）。判例番号・日付・票決・人数・商標ロゴを描かない（ロゴはぼかす）。
- **象徴オブジェのみ:** 土曜のコンビニ駐車場（無人）・車のダッシュボードのスマホ・送信ボタンに親指・24時間カウントダウン・ぼかしタイルの投稿（卑語/中指を描かない）・空の体育館/観客席・フックの空チア制服・ロッカー・校門/校舎の廊下・1969の黒い腕章のシルエット・裁判所の長い廊下・若木/苗床・校内 vs 校外の対比・開/閉の校門。
- **卑語・中指・扇情を描かない**（制約4）: 罵倒語・卑語・中指ジェスチャー・泣く少女・distress の煽情を作らない。投稿は常にぼかし/ピクセルの抽象タイル。尊厳をもって物だけで示す。
- **過大化しない**（制約1）: 「校外は治外法権/常に自由」に見える絵を作らない。半開きの校門（消滅でなく減退）や「学校がなお届く4つの扉」で規制余地を象徴に持つ。
- **Tinker を正確に**（制約2）: 黒い腕章のシルエット（1969・顔なし）／半開きの schoolhouse gate（rights kept at the gate だが実質的混乱は規制可）。
- **票決を正確に**（制約3）: 8枚の開いた扉と1枚の閉じた扉（8-1）を象徴に。数字自体は画像に描かない（AE＝B）。

## 5.9 確定プロンプト（★`ai_prompts.v001.md` にこの85エントリをそのまま書く・各1枚）

> 各行の `[STYLE]` は §5.4 を、`Avoid:` の後の `[NEG]` は §5.5 を**全文展開**して書く（下記は簡潔表記のマクロ。省略記号ではなく定義済み定数）。全て顔なし・身体なし・未成年なし・象徴・判読不能・卑語/中指なし・扇情なし。

```
- `S01.png`
A phone lying face-up on a car dashboard in an empty convenience-store parking lot on a bright quiet Saturday, a faint digital-violet 24-hour countdown ring glowing on its darkened screen, off campus and on her own time, no legible text, no gesture, no people [STYLE] Avoid: [NEG]
- `S02.png`
The plain storefront of a small-town convenience store on an empty Saturday, generic signage blurred into an unreadable smear, a bare parking lot in cool morning light, no legible text, no people [STYLE] Avoid: [NEG]
- `S03.png`
An extreme close view of a single thumb hovering just above a glowing send button on a phone screen, the screen content abstract and pixelated beyond reading, digital-violet interface glow, no legible text, no face, no people [STYLE] Avoid: [NEG]
- `S04.png`
A 24-hour countdown rendered as a glowing violet arc on an otherwise dark phone screen, the ephemeral post set to vanish in a day, the numerals abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S05.png`
A quiet small Pennsylvania town at dusk with modest houses and a distant water-tower silhouette, an ordinary place where a weekend post began, digital-violet sky over cool streets, no people, no readable signage [STYLE] Avoid: [NEG]
- `S06.png`
The pale facade and tall columns of the United States Supreme Court at night, cold stone lit from below, monumental and distant, the court that would answer this in 2021, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S07.png`
A single phone glowing faint violet on a plain surface in the foreground with the cold marble colonnade of the highest court distant and out of focus beyond it, the span from a weekend snap to the Supreme Court, no legible text, no people [STYLE] Avoid: [NEG]
- `S08.png`
The ordinary brick facade of a small-town high school in flat afternoon light, an unremarkable civic building, quiet and empty, no people, no readable sign [STYLE] Avoid: [NEG]
- `S09.png`
An empty high-school gymnasium with a polished floor and folded bleachers under cool light, the varsity floor she tried out for and did not make, no people, no readable text [STYLE] Avoid: [NEG]
- `S10.png`
A tryout roster sheet pinned to a gymnasium wall in cool light, the printed lines abstract and unreadable, a place on the list conspicuously absent, no legible words, no people [STYLE] Avoid: [NEG]
- `S11.png`
A pair of cheer pom-poms resting still on an empty locker-room bench in cool light, the squad rendered as objects, quiet and dignified, no people, no readable text [STYLE] Avoid: [NEG]
- `S12.png`
A single closed school locker among a row in an empty hallway under cool light, one ordinary locker, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S13.png`
Empty gymnasium bleachers rising in cool violet-tinged light, the season watched from the stands rather than the floor, still and vacant, no people, no readable text [STYLE] Avoid: [NEG]
- `S14.png`
A convenience-store parking lot at cool dusk with a single parked car, the off-campus spot a few miles from school where the weekend post was made, no people, no readable signage [STYLE] Avoid: [NEG]
- `S15.png`
A phone screen showing two abstract pixelated photo tiles in a vanishing story, the content blurred entirely beyond reading, an angry weekend post reduced to a smear of light, no legible text, no gesture, no face, no people [STYLE] Avoid: [NEG]
- `S16.png`
An empty cheer uniform hanging alone on a single wall hook in cool light, the season taken away rendered as an empty uniform, dignified and still, no people, no readable text [STYLE] Avoid: [NEG]
- `S17.png`
The same empty cheer uniform on its hook seen closer with a digital-violet shadow behind it, quiet and restrained, a season she would lose, no people, no readable text [STYLE] Avoid: [NEG]
- `S18.png`
A school hallway lined with lockers receding into cool light, screenshots traveling phone to phone implied by nothing but distance, no people, no legible text [STYLE] Avoid: [NEG]
- `S19.png`
A coach's clipboard lying face-down on an empty bleacher in cool light, a squad rule about respect invoked, the paper abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S20.png`
A wall calendar with a long run of days marked out under cool light, a full upcoming year of suspension from the squad, the dates abstract and unreadable, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S21.png`
A modest federal courthouse exterior at dusk in cool light, the family taking the school to court, civic and plain, no people, no readable sign [STYLE] Avoid: [NEG]
- `S22.png`
The front doors of a small-town school seen frontally as a threshold in cool light, the literal schoolhouse gate, symbolic and still, no people, no readable sign [STYLE] Avoid: [NEG]
- `S23.png`
An old 1969-era photograph in a plain frame on a dark surface implying black armbands by silhouette only, the arms and faces cropped entirely out of frame, the Tinker protest as a relic, no faces, no legible text, no people [STYLE] Avoid: [NEG]
- `S24.png`
A single black cloth armband resting alone on a wooden school desk in a shaft of cool light, the 1969 protest rendered as one quiet object, symbolic, no arm, no person, no legible text [STYLE] Avoid: [NEG]
- `S25.png`
An empty 1960s-style classroom with rows of wooden desks in cool light, where students kept their rights at the door, austere and vacant, no people, no readable text [STYLE] Avoid: [NEG]
- `S26.png`
The schoolhouse front doors standing open onto a bar of cool light, the promise that students do not shed their rights at the gate, symbolic, no people, no readable sign [STYLE] Avoid: [NEG]
- `S27.png`
A heavy old law volume closed on a dark desk under a cool lamp, the 1969 precedent rendered as a book, its spine title abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S28.png`
A single hard line across a school floor dividing inside from outside in cool light, the disruption line a school may still enforce within the gate, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S29.png`
A phone glowing on one side of a hard floor line and a schoolhouse door on the other, a weekend post held against the schoolhouse world, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S30.png`
An embossed appellate-court seal implied as an abstract disc on a cold marble wall, the federal appeals court, the emblem unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S31.png`
A long courthouse corridor receding into cool institutional light, the case climbing the courts, polished floor and closed doors, no people, no readable signage [STYLE] Avoid: [NEG]
- `S32.png`
A wall map narrowing from a small Pennsylvania town toward a distant capital with a faint thread between them, the labels abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S33.png`
A clean bright line drawn hard straight across a cold floor, the appeals court's broad bright-line rule that a school has no reach off campus, deliberately severe and unqualified, no people, no text [STYLE] Avoid: [NEG]
- `S34.png`
A darkened home doorway at night with a phone glowing faint violet just inside it, a threat typed at home implied only by the glow, restrained and symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S35.png`
An empty bedroom desk with a phone face-down under a single cool lamp, harassment run from a bedroom phone implied only by absence, no legible text, no people [STYLE] Avoid: [NEG]
- `S36.png`
A school security door with a small keycard reader panel in cool light, one of the interests a rule too broad would tie a school's hands over, abstract, no legible text, no people [STYLE] Avoid: [NEG]
- `S37.png`
Two plain doors side by side, one a school door and one a home door, the on-campus and off-campus worlds a rule must learn to tell apart, symbolic, no people, no readable sign [STYLE] Avoid: [NEG]
- `S38.png`
A knot of tangled cord resting on a cold desk in a shaft of light, the line-drawing knot the justices agreed to untangle, symbolic and abstract, no legible text, no people [STYLE] Avoid: [NEG]
- `S39.png`
The tall marble columns and pale facade of the United States Supreme Court seen frontally at night, the case taken up for review, monumental and solemn, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S40.png`
A single opinion volume lying open under a cool lamp, its pages reduced to abstract illegible lines, the careful narrow ruling being written, no legible words, no people [STYLE] Avoid: [NEG]
- `S41.png`
A spare row of eight empty chairs with one chair set apart to the side in cool light, an eight-to-one split rendered only as chairs, symbolic, no people, no readable text [STYLE] Avoid: [NEG]
- `S42.png`
A single lit lectern in an empty marble chamber under cool light, the opinion of the Court delivered, austere and still, no people, no readable text [STYLE] Avoid: [NEG]
- `S43.png`
A schoolhouse door standing neither fully shut nor fully open in cool light, a school's power over off-campus speech neither vanished nor unlimited, diminished not gone, symbolic, no people, no readable sign [STYLE] Avoid: [NEG]
- `S44.png`
A threshold with a narrow band of cool light spilling across it, the school's interest that stays real in some off-campus cases, symbolic and restrained, no legible text, no people [STYLE] Avoid: [NEG]
- `S45.png`
A short row of four plain doors left slightly ajar in cool light, the categories a school may still reach rendered as four open doors, serious bullying, threats, cheating, and school security, no legible text, no people [STYLE] Avoid: [NEG]
- `S46.png`
A single closed school security panel on a cold wall, a breach of school security as one of the doors the Court left open, abstract, no legible text, no people [STYLE] Avoid: [NEG]
- `S47.png`
An empty two-lane road stretching from a school building toward the horizon under cool light, off campus and on her own time, symbolic distance, no people, no readable signage [STYLE] Avoid: [NEG]
- `S48.png`
A hard single line of cool light dividing a marble floor into two unequal sides, a school's diminished interest set against a student's strong right to speak, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S49.png`
An empty family porch at dusk with a doorway lit soft and warm, the zone of a parent's responsibility off campus rather than a principal's, symbolic, no people, no readable sign [STYLE] Avoid: [NEG]
- `S50.png`
A twenty-four-hour clock face rendered abstractly on a cold wall in cool light, the whole day a student's speech would fall under if a school could police both worlds, no legible numerals, no people [STYLE] Avoid: [NEG]
- `S51.png`
A single young sapling in a pale pot standing in a shaft of cool light on a marble sill, the nurseries of democracy rendered as one small tree, dignified, no people, no legible text [STYLE] Avoid: [NEG]
- `S52.png`
A row of small saplings in a nursery bed under soft cool light, unpopular ideas protected so that they can grow, symbolic and quiet, no people, no legible text [STYLE] Avoid: [NEG]
- `S53.png`
A single sapling sheltered under a cupped cool light against a dark ground, protecting the unpopular voice that needs it most, dignified and still, no people, no legible text [STYLE] Avoid: [NEG]
- `S54.png`
A phone glowing faint violet on a marble surface framed within the open schoolhouse doors, B.L.'s weekend post placed back inside the doctrine, symbolic, no legible text, no gesture, no face, no people [STYLE] Avoid: [NEG]
- `S55.png`
An empty algebra classroom with a chalkboard of abstract unreadable marks in cool light, a few minutes of chatter over a couple of days, quiet and vacant, no legible text, no people [STYLE] Avoid: [NEG]
- `S56.png`
A scatter of empty student desks with a single chair turned aside in cool light, some upset teammates rendered as one turned chair, restrained, no people, no readable text [STYLE] Avoid: [NEG]
- `S57.png`
A pair of plain scales weighing a phone against an empty classroom under cool light, the disruption far short of Tinker's demanding standard, symbolic, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S58.png`
A schoolhouse door swinging back open onto cool daylight, the suspension found to have crossed the line and the right restored, symbolic, no people, no readable sign [STYLE] Avoid: [NEG]
- `S59.png`
A second opinion volume set slightly apart under a cool lamp, a concurrence written separately, its title abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S60.png`
A single house key resting on a marble ledge in cool light, only a slice of a parent's authority handed to a school and only for what a school is for, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S61.png`
A small doorway set within a much larger doorway in cool light, only a slice of parental authority passing through the schoolhouse door, symbolic, no people, no readable sign [STYLE] Avoid: [NEG]
- `S62.png`
A lone opinion volume closed and set apart in a shaft of cool light, a single dissent written alone, its spine abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S63.png`
An old row of century-worn law books on a dark shelf in cool light, more than a century of history the lone dissent looked back on, the titles abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S64.png`
A phone glowing faint violet with a thin line of light running from it back toward a schoolhouse door, the dissent's view that the post traveled back onto school grounds, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S65.png`
Eight doors standing open and one still shut along a cool corridor, eight justices one way and one the other, symbolic, no people, no readable sign [STYLE] Avoid: [NEG]
- `S66.png`
An empty cheer uniform lifted back onto its wall hook in cool restored light, the courts ordering her put back on the squad, symbolic and quiet, no people, no readable text [STYLE] Avoid: [NEG]
- `S67.png`
A wiped-clean page lying in a shaft of cool light on a courthouse table, the suspension ordered erased from her record, the marks gone, no legible text, no people [STYLE] Avoid: [NEG]
- `S68.png`
The convenience-store parking lot again at dusk with a single phone glowing faint violet on a car dashboard, back where it began, a post built to vanish in a day, no legible text, no people [STYLE] Avoid: [NEG]
- `S69.png`
A phone screen with a 24-hour countdown near its end rendered as a thinning violet arc, the post about to disappear, the numerals abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S70.png`
A small-town school building at three-o'clock light with the day emptying out, when school was a building you leave behind at the end of the day, symbolic, no people, no readable sign [STYLE] Avoid: [NEG]
- `S71.png`
A phone glowing faint violet in a pocket-dark frame, school following you home on a device with you every waking hour, symbolic and restrained, no legible text, no people [STYLE] Avoid: [NEG]
- `S72.png`
A schoolhouse gate at cool dusk with its long shadow stretching far out across an empty parking lot, the question of where the gate now falls, symbolic and severe, no people, no readable sign [STYLE] Avoid: [NEG]
- `S73.png`
A single cool line drawn carefully across a marble floor, an answer that is neither a wall nor an open field but a line drawn with care, symbolic, no people, no text [STYLE] Avoid: [NEG]
- `S74.png`
The schoolhouse door standing open onto cool daylight, a school does not lose all authority the second a student logs off its property, symbolic, no people, no readable sign [STYLE] Avoid: [NEG]
- `S75.png`
The four slightly-open doors again in cool light, genuine threats, real harassment, cheating, and school security, the narrow things a school can still reach, no legible text, no people [STYLE] Avoid: [NEG]
- `S76.png`
A phone glowing soft and warm on a plain weekend table, an ordinary off-campus vent where a school's reach is weakest and the right to speak is strongest, symbolic, no legible text, no gesture, no face, no people [STYLE] Avoid: [NEG]
- `S77.png`
An open field seen beyond an open schoolhouse gate in cool light, a student's private phone not turned into school property, symbolic and open, no people, no readable sign [STYLE] Avoid: [NEG]
- `S78.png`
A schoolhouse gate held from expanding, its long shadow stopping short of wrapping around a whole life, symbolic and restrained, no people, no readable sign [STYLE] Avoid: [NEG]
- `S79.png`
Two doorways held in one cool frame, the phone in your hand and the power of the people who grade you, the careful line drawn between them, no people, no legible text [STYLE] Avoid: [NEG]
- `S80.png`
A phone screen going dark on a plain surface in cool light, the weekend post finally gone, a quiet resolution, no legible text, no people [STYLE] Avoid: [NEG]
- `S81.png`
An empty school hallway with the low glow of a phone rising into a designed silence, sound-forward and still, cool light, no people, no legible text [STYLE] Avoid: [NEG]
- `S82.png`
A single notification chime rendered as a faint violet ring of light on a dark phone screen, dimming toward black, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S83.png`
The empty convenience-store parking lot at first grey light of dawn, quiet and open-ended, the small town just beginning to stir, no people, no readable signage [STYLE] Avoid: [NEG]
- `S84.png`
A schoolhouse gate at first light standing open and calm in cool dawn light, the right that mostly follows a student back out through it, symbolic, no people, no readable sign [STYLE] Avoid: [NEG]
- `S85.png`
A phone left face-down and dark on a plain weekend table in soft cool morning light, the held final image, unresolved but at rest, no people, no legible text [STYLE] Avoid: [NEG]
```

**枚数チェック:** 上記 85 エントリ（S01..S85）。§5.3 の `--only S01` ログで `shots=101`（body 85 + i2v種 16）を確認してから本番を回す。

---

# 6. A-2/A-3: 静止画のQC・目視・depth map

## 6.1 機械QC（body 85 + i2v種 16 = 全101枚・`qc_mahanoy_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `30.0<=mean_luma<=225.0`（EP47 は夜青ベースにスマホの局所グロー＝**全体が暗い**。`check_visual_asset_qc.DARK_LUMA_FLOOR=45.0` を下回る本が多いはずなので暗側偏りに注意。黒潰れ本は reject） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject（`check_visual_asset_qc.NEARDUP_SIM=0.90`）。**バリエーション0なので本来ほぼ衝突しないはず。衝突したらプロンプトが被っている**（特に多数ある「スマホ画面/グロー」「校門/校舎の廊下」「裁判所の長い廊下」「開/閉の扉」「駐車場」系に注意） | 片方 reject＋プロンプト見直し |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・投稿文・判例番号・日付・票決・商標ロゴ（Snapchat等）が写っていないか（R1・制約2/6） | `has_readable_text=true`→reject |
| Q6 | 顔の混入 | **目視。** 識別可能な顔・**未成年（少女）の姿**が写っていないか（R1・制約4） | `has_identifiable_face=true`→reject |
| Q7 | 身体/卑語/扇情の混入 | **目視。** 人体・裸体・**中指ジェスチャー・読める卑語・泣く人・distress の煽情**が写っていないか（制約4） | `has_human_body=true`→reject |

**Q5/Q6/Q7 は機械で判定しない。** コンタクトシートを出して**全101枚を実際に目視**する:

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-047-mahanoy --media image
#   → runs/qc/mahanoy_footage_contact_NN.png（20枚/シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-46 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** SDXL は平気で読める文字・顔・身体・ジェスチャーを描く。**特に制約2（可読の投稿文/判例番号/日付/商標ロゴの非露出）・制約4（B.L.＝未成年を出さない・卑語/中指/扇情なし）は目視でしか守れない。** S03/S04/S15/S69/S80/S82（スマホ画面）は読める投稿文・卑語・中指・Snapchatロゴが写っていないこと（ぼかしタイルであること）、S02（店舗）はロゴが判読不能にぼけていること、S10/S20（名簿・カレンダー）は読める文字/日付が写っていないこと、S23/S24（腕章）は顔・身体が一切写っていないことを必ず目で確認する。

## 6.2 出力

```
episodes/PD-2026-047-mahanoy/05_visuals/still_qc.v001.json     # 101枚全部の行（reject も残す・sha256/phash/mean_luma/long_edge）
（build_footage_contact_sheet が runs/qc に出す）
```

## 6.3 accepted が101枚に届かなかったとき

```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 47 --variants 1 --only S37   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_mahanoy_stills.py
```
accepted body >= 85 かつ i2v_source >= 16 になるまで繰り返す。**基準を下げない・バリエーションを足して水増ししない。**

## 6.4 depth map（★新規スクリプトを作らず既存を使う）

```bash
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir "H:/pd-media/assets/ai/mahanoy"
```
- モデル `Intel/dpt-large`。出力 `<stem>_depth.png`（同サイズ L グレースケール）。冪等。
- **role が `body` の静止画は depth 必須**（`treatment:"depth"` が隣に `_depth.png` を要求。無いとレンダーがクラッシュ）。i2v 種（`M<NN>_src.png`）は depth 不要。
- staging 後に `remotion/public/mahanoy/img/` 側でも同名ペアが揃っていること（§10）。

---

# 7. A-4: factory 実写クリップ 92本の選定と全点目視QC

## 7.1 在庫の実態

```
H:\pd-media\assets\factory\   フラット構成
  backgrounds/     11,000本超（.mp4）  ← ★主力（小さな町の街並み・コンビニ駐車場/店舗・学校の外観/廊下/ロッカー・空の体育館/観客席・裁判所の長い廊下・空の法廷・最高裁列柱・夜〜夜明けの街・空き道路・繋ぎ）
  light_assets/    …            合成レイヤー（スマホグロー・冷たい fluorescent・大理石の光条）
  particle_assets/ …            合成レイヤー（廊下の埃・書庫の塵）
  vfx_overlays/    …            合成レイヤー（グレイン・光ノイズ・UIグロー）
  texture_assets/  …            紙・石・大理石・スクリーンのテクスチャ
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
- **EP39（夜/取調室/青）・EP40（郊外/昼/破壊）・EP41（監獄/鉄/石の独房）・EP42（シカゴのアパート/足首モニタ）・EP43（RI の一軒家/porch-amber/救急車/レッカー）・EP44（ティール緑の病院の廊下/臨床）・EP45（暖色台所/朱の督促/郡拘置所 booking）・EP46（green レーン）の絵柄を選ばない。** EP47 は 小さな町の街並み・コンビニ駐車場/店舗＋学校の外観/廊下/ロッカー/空の体育館/観客席＋裁判所の長い廊下・空の法廷・最高裁列柱＋夜〜夜明けの街・空き道路。**鉄格子/独房/cellblock を含むクリップを選ばない（EP41 分離）。実在人物の顔・未成年・泣く人・卑語/中指・扇情を含むクリップを選ばない（制約4）。**

**既存の選定ツールで候補出し（新規に検索ロジックを書くな）:**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes   # テーマ一覧と件数
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query courthouse --limit 96 --exclude-used --ep PD-2026-047-mahanoy --json
```
`--exclude-used` は `check_arc_nonrepeat.build_universe()` と同じ指紋集合を使うので出荷ゲート `arc_nonrepeat` と食い違わない。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・SDXLで作らない情景）

> **★`covers_scene_id` は still 資産 ID 空間（S01..S85・§2 注記）を指す。narrative シーン（DESIGN の S01..S48）とは別体系。** B はこの値を still 資産 ID として解決し、narrative シーンコードにクロスマップしない。

| covers | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S02 | コンビニ店舗外観（土曜・無人） | `convenience_store_exterior` / `small_store_storefront` | 0 |
| S06 | 最高裁ファサード・列柱（夜） | `supreme_court_building` / `marble_columns_night` | 0 |
| S08 | 小さな町の高校の外観 | `high_school_exterior` / `small_town_school_building` | 1 |
| S09 | 空の体育館（無人） | `empty_gymnasium` / `school_gym_interior` | 1 |
| S18 | 学校のロッカーの廊下 | `school_hallway_lockers` / `empty_locker_corridor` | 1 |
| S22 | 校門/校舎の入口（正面） | `school_entrance_doors` / `schoolhouse_front` | 2 |
| S25 | 古い教室（無人・木の机） | `empty_classroom` / `vintage_classroom_interior` | 2 |
| S31 | 裁判所の長い廊下 | `courthouse_corridor` / `long_courthouse_hallway` | 2 |
| S39 | 最高裁の列柱（正面・夜） | `supreme_court_columns` / `marble_facade_night` | 3 |
| S47 | 学校から伸びる空き道路 | `empty_two_lane_road` / `rural_road_from_town` | 3 |
| S70 | 学校の外観（放課後の光） | `school_building_afternoon` / `empty_schoolyard_dusk` | 5 |
| S83 | 夜明けの駐車場/空き道路（受け） | `empty_parking_lot_dawn` / `roadside_dawn` | 5 |

**残り本数は covers を持たない繋ぎ・情景クリップ**（`covers_scene_id:null`）: 小さな町の街並み・コンビニ駐車場・学校の廊下/ロッカー/体育館・観客席・裁判所の長い廊下・空の法廷・列柱の光条・夜〜夜明けの街・空き道路・書庫の棚・抽象 `loops`。**暗いクリップに偏りすぎない**（§7.5 の暗側閾値・全体の1/3=約30本まで。昼光・夕暮れ・夜明けの実用光がある本を優先）。

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
    --ep PD-2026-047-mahanoy --media video --dir "<92本の staging フォルダ>"
#   → runs/qc/mahanoy_footage_contact_NN.png（各タイルにファイル名ラベル）
```

2. **コンタクトシートを実際に開き、92本すべてを1本ずつ見る**
3. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて**選定から外す**
4. 実写シネマティックB-roll（アニメ/CG臭排除）・EP47テーマ（小さな町/コンビニ駐車場/学校の外観・廊下・体育館・観客席/裁判所の長い廊下/最高裁列柱/夜〜夜明けの街・空き道路）・ウォーターマークなし・識別可能な実在人物なし（制約4・R1）を確認
5. **★制約4/6の目視:** 人物が写るクリップは避け、写る場合も後ろ姿/遠景/顔外しのみ。**未成年（生徒・少女）・泣く人・distress の煽情・中指/卑語を含むクリップは使わない。** 学校や街頭に実在の顔が写るニュース映像を使わない（制約4）。**鉄格子/独房/cellblock を含むクリップを使わない（EP41 分離）。**
6. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=45.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。
> **EP47 は夜青ベース＋スマホグロー＋夜の街が多いので暗側が本命リスク。** 平均輝度45未満のクリップが全体の40%を超えると FAIL。**暗いクリップは約30本（1/3）までに抑え、昼光の学校/街・夕暮れ・夜明けの実用光がある本を優先する。**

**1フレームで判断がつかない本は VLC/ffplay で再生して確認**（near-still は `check_animation_mix` を落とす）。

## 7.6 出力

```
episodes/PD-2026-047-mahanoy/05_stock/factory_selection.v001.json   # 選定理由と幕割り当て
episodes/PD-2026-047-mahanoy/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39〜EP46 との重複ゼロ（BLOCKING）

```bash
./.venv/Scripts/python.exe scripts/select_mahanoy_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` 〜 `episodes/PD-2026-046-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP47 の92本の積集合が**空**であることを確認。1件でも exit 1 で差し替え。**EP39〜EP46 のファイルは読むだけ。書き込み・移動・削除は一切しない。** 旧 `PD-2026-011-mahanoy`（同 slug の別話・過去作）も存在するなら**読むだけ・素材を流用しない**。

---

# 8. A-5: i2v モーション化 16本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする16本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）

種画像は §5 と同じ `generate_sdxl_4k.py --variants 1` で `M<NN>_src.png` として生成する（`ai_prompts.v001.md` に下記16行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `MAHA-MS01..MS16`、モーション成果物の asset_id は `MAHA-M01..M16`。

| # | asset_id | 種画像 | 動きの意味 | act |
|---|---|---|---|---|
| 1 | MAHA-M01 | M01_src | 送信ボタンに親指が触れる寸前・スクリーングロー | 0 |
| 2 | MAHA-M02 | M02_src | 24時間カウントダウンの弧が少しずつ減る | 0 |
| 3 | MAHA-M03 | M03_src | 土曜のコンビニ駐車場・光が微かに移ろう | 1 |
| 4 | MAHA-M04 | M04_src | フックの空チア制服が僅かに揺れる | 1 |
| 5 | MAHA-M05 | M05_src | 空の体育館/観客席・冷たい光が移ろう | 1 |
| 6 | MAHA-M06 | M06_src | 校門/校舎の入口への緩い前進ドリー | 2 |
| 7 | MAHA-M07 | M07_src | 机上の黒い腕章・埃が光の中を漂う（1969・顔なし） | 2 |
| 8 | MAHA-M08 | M08_src | 裁判所の長い廊下への緩い前進ドリー | 2 |
| 9 | MAHA-M09 | M09_src | 床を横切る一条の硬い光（校内 vs 校外の線） | 2 |
| 10 | MAHA-M10 | M10_src | 開いた意見書・ランプの光と埃 | 3 |
| 11 | MAHA-M11 | M11_src | 最高裁の列柱・冷たい光が動く | 3 |
| 12 | MAHA-M12 | M12_src | 若木の葉が微かに揺れる（nurseries of democracy） | 3 |
| 13 | MAHA-M13 | M13_src | 半開きの校門が採光へ少し開く（diminished, not gone） | 3 |
| 14 | MAHA-M14 | M14_src | スマホ画面のグローが暗転していく（受け） | 5 |
| 15 | MAHA-M15 | M15_src | 校門が夜明けの光へ静かに開く | 5 |
| 16 | MAHA-M16 | M16_src | 夜明けの駐車場/空き道路が朝へ移る | 5 |

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの16行を追加・各1枚）

```
- `M01_src.png`
A single thumb poised just above a glowing send button on a phone screen, the screen content abstract and pixelated beyond reading, digital-violet interface glow, framed and still for a slow push, no legible text, no face, no people [STYLE] Avoid: [NEG]
- `M02_src.png`
A 24-hour countdown rendered as a glowing violet arc on a dark phone screen, poised to tick slowly down, the numerals abstract and unreadable, framed for a slow hold, no legible text, no people [STYLE] Avoid: [NEG]
- `M03_src.png`
A convenience-store parking lot on a quiet Saturday with a single parked car in cool dusk light, still and poised for a slow drift of light, off campus, no people, no readable signage [STYLE] Avoid: [NEG]
- `M04_src.png`
An empty cheer uniform hanging on a single wall hook in cool light, still and poised to sway almost imperceptibly, dignified, no people, no readable text [STYLE] Avoid: [NEG]
- `M05_src.png`
Empty gymnasium bleachers rising in cool violet-tinged light, still and poised for a slow shift of light, vacant and quiet, no people, no readable text [STYLE] Avoid: [NEG]
- `M06_src.png`
The front doors of a small-town school seen frontally as a threshold in cool light, framed for a slow forward move toward the schoolhouse gate, no people, no readable sign [STYLE] Avoid: [NEG]
- `M07_src.png`
A single black cloth armband resting alone on a wooden school desk in a shaft of cool light with fine dust hanging in the beam, still and poised, no arm, no person, no legible text [STYLE] Avoid: [NEG]
- `M08_src.png`
A long courthouse corridor receding into cool institutional light with closed doors along it, framed for a slow forward move, no people, no readable signage [STYLE] Avoid: [NEG]
- `M09_src.png`
A hard single line of cool light dividing a marble floor into two unequal sides, on campus and off campus held apart, still and poised for the light to creep, symbolic, no people, no text [STYLE] Avoid: [NEG]
- `M10_src.png`
A single opinion volume lying open on a dark desk under a cool lamp with dust hanging in the light, its pages abstract and unreadable, still and poised for a slow push, no legible words, no people [STYLE] Avoid: [NEG]
- `M11_src.png`
The pale marble colonnade of the United States Supreme Court at night lit from below, monumental and still, poised for a slow move, no people, no readable inscription [STYLE] Avoid: [NEG]
- `M12_src.png`
A single young sapling in a pale pot in a shaft of cool light, its leaves poised to stir almost imperceptibly, the nurseries of democracy as one small tree, still, no people, no legible text [STYLE] Avoid: [NEG]
- `M13_src.png`
A schoolhouse door standing half open onto a bar of cool daylight, poised to open a little further, a school's reach diminished not gone, still, no people, no readable sign [STYLE] Avoid: [NEG]
- `M14_src.png`
A phone screen glowing faint violet on a plain surface, poised to dim slowly toward black, the post about to vanish, still and held, no legible text, no people [STYLE] Avoid: [NEG]
- `M15_src.png`
A schoolhouse gate beginning to open onto the cool light of dawn, poised and still, calm and open-ended, no people, no readable sign [STYLE] Avoid: [NEG]
- `M16_src.png`
An empty convenience-store parking lot and an open road under a grey dawn sky turning slowly toward morning, still and open-ended, no people, no readable sign [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。実在の `comfy_wan_*.py` を下敷きにパスと SHOTS だけ差し替え）

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
STILL_DIR     = H:\pd-media\assets\ai\mahanoy      # 種画像 M<NN>_src.png を読む
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\mahanoy
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, text, watermark, identifiable face, real person likeness, minor, teenager, child, crying person, obscene gesture, middle finger, gore, blood"
```

**ゲート:** `dry_validate`（length=5 で1回POSTして配線エラーを安く検出）/ `assert_loaded_completely`（部分ロード検出）/ `assert_frame_math`（フレーム計算）。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す）

```bash
py -3.11 scripts/comfy_wan_mahanoy.py --build            # グラフだけ（GPU触らない）
py -3.11 scripts/comfy_wan_mahanoy.py --run --shot M01   # 1本本番して目視
py -3.11 scripts/comfy_wan_mahanoy.py --run-all          # 残り15本（冪等・既存スキップ）
```
1本 24–73 GPU分・16本で 7–19時間。`/queue` `/history` を30秒間隔でポーリング。

## 8.4 RIFE で 48fps 化（`rife_mahanoy.py`・実在の `rife_*.py` と同手順）

```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは length=5 検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番にリネーム → RIFE 2x を**2回**（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. **フレーム数検証** `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC

- 顔・身体・未成年・卑語/中指・扇情（泣く人）が生成されていないこと（NEG で抑えているが**必ず目視**・制約4）
- モーフィング/ちらつき/ワープが無いこと → あれば別シードで再生成
- M01/M02/M14（スマホ画面）は**読める投稿文・卑語・中指・Snapchat ロゴ**が写り込んでいないこと（制約2/4・ぼかしタイルのままであること）
- M03/M16（駐車場・道路）は**識別可能な人物・車のナンバー・読める標識**が写り込んでいないこと（制約2）
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（16本 × 2回 = 32カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど12本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **6本** | 廊下の埃・書庫の塵。黒背景 drift を screen 合成 |
| `light_assets` | **4本** | スマホグロー・冷たい fluorescent・大理石の光条・夜明けの採光 |
| `vfx_overlays` | **2本** | 微細なグレイン・冷たい光ノイズ／UIグロー |
| **合計** | **12本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/mahanoy/overlay/` に置き、`mahanoy_film.json` の `cuts[].src` には**出さない**（出すと factory 判定で1回制限を食う）。同じレイヤーを何度重ねてもよい（素材ではなく加工）。黒背景でループするものを選び `blend_hint` を書く。**§7.5 の目視QC対象**（12本・12分）。**合成レイヤーの発色は B が accent `#7A5CD0`（デジタル・バイオレット）に寄せる想定・A は色被りの素材を作らない（他話の gold/blue/amber/teal/crimson/green を選ばない）。**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --kind video --query dust_particles --limit 20 --exclude-used --ep PD-2026-047-mahanoy --json
```

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_mahanoy_assets.py`）

```
remotion/public/mahanoy/img/     ← role=body の静止画85枚（+ 同名 _depth.png）
remotion/public/mahanoy/factory/ ← 選定 factory .mp4 92本
remotion/public/mahanoy/motion/  ← i2v M<NN>_rife.mp4 16本
remotion/public/mahanoy/overlay/ ← 合成レイヤー 12本
```
- `public_path` はマニフェストの値と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー（`import_to_remotion.py` の `conform_video(...,fps=30)` と同じ）
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する・外すと誤分類）:**
- factory の `public_path` は必ず `mahanoy/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も**含めない**
- 合成レイヤーは `mahanoy/overlay/` に置き `cuts[].src` に出さない

> **B のレンダは `--public-dir=public_slim`（Root.tsx に `id="Ep47Mahanoy"`）を使う想定だが、`public_slim` の構築は B の責務。** A は `remotion/public/mahanoy/` に正典を置くところまで（B が slim を派生させる）。

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`

全静止画・i2v・factory・overlay を1行ずつ: `asset_id`/`path`/`source`（`ai_codex` or `factory`）/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力

```bash
./.venv/Scripts/python.exe scripts/build_mahanoy_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_mahanoy_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_mahanoy_asset_manifest.py --reuse-feasibility
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

EP47 の設計値: still 101/85=1.19(≤2) / factory 92/92=1.0(≤1) / motion 32/16=2.0(≤2) / first-use 193/225=0.8578(≥0.70)。**全て達成可能。**

---

# 12. 絶対にやらないこと

- **EP39（frazier）/EP40（lech）/EP41（thompson）/EP42（young）/EP43（caniglia）/EP44（tekoh）/EP45（cleveland）/EP46（green レーン）のファイルに一切触らない。** 読み取りのみ可。素材・色（EP41 gold #E5B53A / EP42 blue #3B7DD8 / EP43 amber #E0913C / EP44 teal #2FA6A0 / EP45 crimson #B23A48 / EP46 green #3F8F5F）・音のレーンも分離。EP47 の accent は **digital-violet #7A5CD0**（INK #0A0A0C・B が OP/AEカード/サムネで使用・A は絵で流用色を作らない）。
- **旧 `PD-2026-011-mahanoy`（同 slug の別話・過去作）にも触らない。** 素材・スクリプト（`build_mahanoy_audio_v001.py` 等）を流用しない。EP47 の出力は必ず `PD-2026-047-mahanoy` / `H:\pd-media\assets\ai\mahanoy\` の新パスに書く。
- **スレッドBの所有ファイル（§0.2）に触らない。** 特に `remotion/src/**` `scripts/ae/**` `scripts/build_mahanoy_film.py` `manifest.json` `04_scenes/shotlist*` `figures`。
  - **ただし `04_scenes/ai_prompts.v001.md` は A が書く**（`generate_sdxl_4k.py` の入力・§5.9/§8.1a）。B は読むだけ。
- **図解・トランジション・タイポの素材を探しに行かない。** 在庫が薄い/無いカテゴリは B が自作する。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。ローカル A1111・ComfyUI・RIFE は GPU を使うだけで課金なし（オーナー許可済み）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness・身体をどこにも作らない**（§1・制約4）。特に **B.L.（Brandi Levy・未成年）を個人として描かない。**
- **6制約に反する文言・絵をプロンプト・タグ・注記・ファイル名のどこにも作らない**（§1.2/§1.3）:
  - 過大化（「schools can never punish off-campus」「off-campus speech is always protected」「free-fire zone」・制約1）／Tinker 誤り（「Tinker overruled」「rights disappear off campus」・制約2）／票決誤り（「unanimous」「7-2」「9-0」・制約3）／卑語・中指・未成年の顔/身体・扇情（distress/poverty porn）（制約4）／可読の投稿文/判例番号/日付/票決/商標ロゴ（制約2/6）。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。反復回避は distinct 85 で担保（§0.1・§5.6）。
- **role=thumb / still_thumb を作らない・overlay を12本以外にしない。** サムネは also_thumb=true の body 6枚（§4.3 = {S01,S03,S13,S16,S22,S68}）。
- **★dochighlight figure（黒バー/box/underline）を作らない・言及しない。** これは figures の責務（B）だが、A の `tags`/`caption_hint`/`notes` にも `dochighlight` という文字列を書かない（grep で 0 を保つ）。
- **枚数・本数を「だいたい」で決めない。** §3 の確定値（still 85 / factory 92 / i2v 16 / distinct 193 / first-use 0.8578 / still-share 0.4489 / MG≥30 / 11.96分）と §3.3 の検算をそのまま使う。合わなければ実装ではなく**本書を疑って報告**。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** EP36は大聖堂を、EP38は牛を通した。**生成物・在庫クリップを実際に見る**（特に制約2/4は目視でしか守れない・投稿文の可読文字・商標ロゴ・中指/卑語・未成年/扇情描写も目視で排除）。

---

# 13. 完了報告に含めるもの

```
1. accepted 静止画の枚数と内訳（body 85 / i2v_source 16 / also_thumb 6 [S01/S03/S13/S16/S22/S68] / reject N）
2. factory 選定 92本のリスト（asset_id / subtype / eyeballed_content）と、subtype と食い違って外した本数、スマホ画面/道路クリップの「no readable text / no logo / no gesture」確認
3. EP39/EP40/EP41/EP42/EP43/EP44/EP45/EP46 重複ゼロの確認結果
4. i2v 16本の frames / duration_sec と、SHORT? の有無
5. 合成レイヤー12本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code をそのまま貼る）
7. §3.3 の検算 [1]〜[7] を自分で再計算した結果
8. asset_manifest.v001.json の counts ブロック（still_body 85 / still_i2v_source 16 / motion 16 / factory 92 / overlay 12）
9. 6制約・1枚前提の自己申告（過大化なし/Tinker 正確/票決 8-1 帰属正確/未成年 非肖像化＋卑語・中指・扇情ゼロを目視確認/バリエーション0/dochighlight 文字列ゼロ/A↔B同一スキーマ [schema mahanoy_assets.v1 / role enum body|i2v_source|reject / counts / also_thumb 集合 {S01,S03,S13,S16,S22,S68} / overlay 12]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
