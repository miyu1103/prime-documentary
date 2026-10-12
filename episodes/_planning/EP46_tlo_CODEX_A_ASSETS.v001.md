# EP46 tlo — Codex スレッドA「素材生成」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN）も実装スレッドB（CODEX_B）のファイルも**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> **唯一の外部真実 = `episodes/_planning/EP46_tlo_PRODUCTION_SPEC.v001.json`**（機械生成）。本書の数値はそこから転記したものであり、手書きで発明していない。
> **A↔B 接続点は `asset_manifest.v001.json` ただ1ファイル**（DESIGN/CODEX_B と counts / role enum / overlay枚数 / also_thumb集合を一字一致で共有）。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP46 / Episode ID: PD-2026-046-tlo / slug: tlo
Composition id: Ep46Tlo（B が Root.tsx に登録・A は staging まで）
事件:       New Jersey v. T.L.O., 469 U.S. 325 (1985)。公立高校の副校長が女子生徒の
            purse を捜索した事件。最高裁は 6-3 で、①第4修正は公立学校職員にも「適用される」
            （生徒は校門で権利を失わない）が、②令状不要・相当理由(probable cause)不要で、
            基準は reasonableness＝reasonable suspicion に「引き下げられる」と判示。
            二段テスト（inception＋scope）が判例核。footnote 7 で警察関与時の基準は留保。
            主題は「権利は残るが基準は下がる（no rights でも full rights でもない中間）」。
            T.L.O.は当時14歳の未成年＝象徴のみ・顔/肖像/身体を一切出さない。
            薬物（原事案の押収物）は臨床的・最小限・非扇情に扱う（美化しない）。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**84本の固有プロンプト × 1枚 = 84枚**・バリエーション0） | `H:\pd-media\assets\ai\tlo\S<NN>.png` | 2–3.5時間（GPU） |
| A-1b | i2v 種画像の生成（**16本の固有プロンプト × 1枚 = 16枚**・バリエーション0） | `H:\pd-media\assets\ai\tlo\M<NN>_src.png` | 30–50分（GPU） |
| A-2 | 静止画のQCと目視（**目視必須**） | `05_visuals/still_qc.v001.json` + コンタクトシート | 1.5時間 |
| A-3 | depth map 生成（`treatment:"depth"` の必須入力） | `H:\pd-media\assets\ai\tlo\S<NN>_depth.png` | 20分 |
| A-4 | factory 実写クリップ **92本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | **2.5時間（うち目視だけで1時間以上）** |
| A-5 | i2v モーション化 **16本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\tlo\M<NN>_rife.mp4` | 7–19時間（GPU） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 **12本** | `05_stock/overlay_selection.v001.json` | 30分 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 20分 |
| A-8 | Remotion public への staging | `remotion/public/tlo/{img,factory,motion,overlay}/` | 30分 |

> **★★ 最重要の前提（EP42/43/44/45 から継続）: 1シーン1枚・バリエーション0 ★★**
> Codex の画像生成は高精度。**同一ショットの複数バリエーション（`_02`/`_03`）を作らない。**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 84本＝84行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **`--variants 1`** で回す。**`--variants 3` は使わない。**
> **総生成画像 = still 84 + i2v 種 16 = 100枚（各1回）。** factory 92本は生成でなく在庫からの選抜。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-046-tlo/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** Bはスタブで全パイプラインを完走できるので、Aの完了を待っていない。**A も急がなくてよいが途中経過を壊すな。** このマニフェストは **A(producer)とB(consumer/validator)で counts / role enum / overlay枚数 / also_thumb集合を一字一致**で共有する（§4）。

### ★★ EP45 の事故を繰り返さない（本 EP の最重要ゲート）★★

> **EP45 の build 失敗の直接原因: `asset_manifest` の `factory` 配列と `motion` 配列が空だった。** still だけ書いて factory/motion を書かなかったため、film ビルダーが素材を解決できず落ちた。
> **本 EP では manifest の `factory` 配列に 92 エントリ（`public_path:"tlo/factory/F001__….mp4"` …F092 まで）を全て書き、`motion` 配列に 16 エントリ（`public_path:"tlo/motion/M01_rife.mp4"` …M16 まで）を全て書く。** counts と実配列長が一致しない・factory/motion が空、のいずれも `--verify` を exit 1 にする（§4.2 不変条件2・17・18）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\tlo\**` / `H:\pd-media\assets\ai_video\tlo\**` | **A** | 読み書き |
| `episodes/PD-2026-046-tlo/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-046-tlo/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/tlo/{img,factory,motion,overlay}/**` | **A** | 読み書き |
| `episodes/PD-2026-046-tlo/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_tlo_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-045-*/**` および EP39〜45 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を `read_prompts()` で読む） | `PD-2026-046-tlo --variants 1` / `46 --variants 1 --only S01` |
| `scripts/gen_depth_maps.py`（**既存**） | §6.4 の depth map | `--dir "H:/pd-media/assets/ai/tlo"` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-046-tlo --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit 96 --exclude-used --ep PD-2026-046-tlo --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-046-tlo` |

**★Aが新規作成するスクリプト（EP45 の cleveland 版を tlo 用に複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（複製元・EP45） |
|---|---|---|
| `scripts/qc_tlo_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_cleveland_stills.py` |
| `scripts/select_tlo_factory.py` | §7 の factory 92本の確定選定・EP39〜45 sha256 除外検証 | `scripts/select_cleveland_factory.py` |
| `scripts/comfy_wan_tlo.py` | §8 の i2v 16本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_cleveland.py` |
| `scripts/rife_tlo.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_cleveland.py` |
| `scripts/build_tlo_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_cleveland_asset_manifest.py` |
| `scripts/stage_tlo_assets.py` | §10 の staging | `scripts/stage_cleveland_assets.py` |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある（`read_prompts()` で `04_scenes/ai_prompts.v001.md` を読む）。あなたは **`ai_prompts.v001.md` を §5.2 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない**（上の複製元が実在することを `ls scripts/` で確認してから複製する）。
> **正確性ゲートは `check_tlo_facts.py`（B が実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の6制約に一致し、`check_tlo_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_tlo_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。
#     ★factory 92 / motion 16 の配列が空でなく public_path が全て埋まっていること。

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_tlo_asset_manifest.py --reuse-feasibility
#   → still >=84 / motion >=16 / factory >=92 / distinct 合計 >=192 / first-use >=0.70

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_tlo_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全92本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-046-tlo
#   → exit 0（factory_clip_qc.v001.json が staging 済み全クリップを reviewed:true で網羅）

# [A-DONE-5] EP39〜EP45 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_tlo_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39・EP40・EP41・EP42・EP43・EP44・EP45 の七つすべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（R1 ＋ 正確性6制約）★★★

**最高裁は 6-3 で「第4修正は公立学校職員による捜索にも適用される」と明言した。生徒は校門で権利を失わない。ただし基準を令状不要・相当な理由(probable cause)不要＝合理的疑い(reasonable suspicion)へ「引き下げた」（消滅でなく引き下げ）。判例核は二段テスト（①開始時に正当＝inception、②範囲が相当＝scope）。footnote 7 で警察関与時の基準は留保。主題は「no rights でも full rights でもない中間」。T.L.O.は当時14歳の未成年（R2）＝象徴のみ・顔/肖像/身体を一切出さない。原事案に薬物（所持・売買の証拠）が含まれるが臨床的・最小限・非扇情に扱い、美化しない。**

## 1.1 R1（生成ビジュアル全般）

1. **実在人物・未成年の顔・likeness・肖像を作らない。** T.L.O.（当時14歳の未成年・R2）を**顔・身体・肖像・後ろ姿としても描かない（未成年は絶対に肖像化しない）**。Justice White / Brennan / Marshall / Stevens / 副校長 Choplick を顔・身体として描かない。人物は原則「人を出さない」（象徴オブジェのみ）。判事評言の逐語引用は AE カード（B の担当）であって画像ではない。
2. **実在の判決文・判例番号・条文・日付の可読文字を再現しない。** 意見書・令状フォーム・索引カード・手紙・審判記録・カレンダーは雰囲気のみ（判読不能）。判例番号（**469 U.S. 325**）・日付（**1985-01-15 / January 1985 / 1984**）・票決の数字（6-3）・金額を**画像に描かない**（AE/figures のタイポで出す＝B の担当）。ブランドロゴ（タバコ等）は**ぼかして判読不能**にする。
3. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性6制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **生徒は無権利ではない。** 第4修正は公立学校職員による捜索にも「適用される」。**「students have no rights / lose rights at the door / the 4A does not apply in school / no privacy at school / schools can search anything anytime」を書かない**（過大化禁止＝制約1）。許容は "the Fourth Amendment applies inside a public school" / "students do not shed their rights at the schoolhouse door" / "the standard is lowered, not removed"。
2. **二段テストが判例核。** ①inception（校則or法違反の証拠が出ると疑う reasonable grounds）、②scope（年齢・性別・違反の性質に照らし過度に侵襲的でない）。基準は令状不要・相当理由不要の **reasonable suspicion**。**「probable cause is required in school / schools need a warrant」を真として書かない**（それらは最高裁が退けた easy answer＝制約2）。象徴で「令状フォーム」「相当理由の重り」を描くのは可だが、注記で「必要とされた」と誤らせない。
3. **公立学校職員の基準であり、警察関与時はより高い基準があり得る（footnote 7 で留保）。** この区別を保つ。**「police can search students freely / same rule for police」を書かない**（制約3）。警官バッジは「境界＝警察が入ると基準が戻り得る」の象徴としてのみ。
4. **票決 6-3・中立帰属。** White 法廷意見／Brennan・Marshall・Stevens が一部反対（合理性の引下げ・本件適用に反対）。**「unanimous / 9-0 / 5-4」等の誤った票決を書かない**（制約4）。多数/反対を中立に扱う。
5. **T.L.O.は未成年（R2）・象徴のみ・顔/肖像/身体なし。** 薬物は臨床的・最小限・非扇情（押収物を机に淡く並べる程度・美化しない）。**泣く生徒・困窮・扇情、薬物のグラマー化、strip-search 描写を作らない**（制約5）。原被疑事実（売買）でサムネ/タグを煽らない。
6. **数値・引用は原典一致・捏造ゼロ。** 469 U.S. 325 (1985)・二段テスト逐語・"reasonable grounds"・White執筆。**画像には描かない**（判読不能・数値は AE/figures＝B）。confidence:medium（校名 Piscataway・副校長名 Choplick）は画面に出さない・タグに書かない。

## 1.3 機械ゲート（`build_tlo_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
BANNED_PORTRAIT = re.compile(
    r"\bportrait\b|\bmugshot\b|likeness of|"
    r"face of (t\.?l\.?o\.?|the (girl|student|freshman|minor|teen|teenager)|white|brennan|marshall|stevens|choplick)|"
    r"(fourteen|14)[- ]year[- ]old('?s)?(?:\s+\w+)?\s+(face|body|likeness)|minor'?s (face|body|likeness)|"
    r"recognizable (real )?person|identifiable face|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"students? (have no|lose|shed|leave|surrender|forfeit) (their )?(fourth amendment )?rights|"
    r"no (fourth amendment|4a|privacy) (rights )?(in|at|inside) (a )?school|"
    r"(the )?fourth amendment (does not|doesn'?t|never) appl(y|ies) (in|at|to) (a )?school|"
    r"(schools?|officials?|teachers?) can search (you |a student |anyone )?(anything|everything|anytime|anywhere|whenever|for no reason)|"
    r"search (anything|everything) (anytime|anywhere|for no reason)|"
    r"probable cause (is |was )?(required|needed) (in|at|for|inside) (a )?school|"
    r"(schools?|officials?|teachers?) (need|require|must get) (a )?warrant|"
    r"(unanimous|9-?0|nine to zero|5-?4|five to four|7-?2|8-?1) (ruling|decision|vote|majority)|"
    r"police can search (students|kids|you) freely|same (rule|standard) for (the )?police|"
    r"glamori[sz]e|glamorous drugs|drug[- ]dealing hero|"
    r"strip[- ]search(ed|ing)? (the )?(girl|minor|student|fourteen|kid)|"
    r"crying (student|girl|teen)|weeping (student|family)|poverty ?porn",
    re.IGNORECASE)
```

> `BANNED_ACCURACY` は制約1〜5を機械化したもの。プロンプト・タグ・`caption_hint`・注記のどこにも該当語を書かない。**"the fourth amendment applies inside a public school" / "students do not shed their rights at the schoolhouse door" / "the standard is lowered to reasonable suspicion" / "reserved when police get involved" は許容（射程を正しく限定）。** 禁止は「無権利」化・「probable cause/令状が学校で必要」化・「警察も同じ/自由に捜索」・誤った票決・薬物のグラマー化・未成年の肖像化・扇情だけ。

---

# 2. 台本の語数と尺の確定値（SPEC から転記・Aが素材点数を積算する根拠）

**★唯一の真実 = `episodes/_planning/EP46_tlo_PRODUCTION_SPEC.v001.json`。** 古い資料の wpm・語数は使うな。

```
words_total          = 2,125
narration_seconds    = 715.9   （= 11.9分・[DESIGNED SILENCE 1..2] の実音無音を含む）
wpm_used             = 178.1
総尺（設計）          = 715.9 + BrandOpening 3.50 + BrandEndcard 9.00 = 728.4秒 = 12:08  ≤ 750s
視覚シーン(narrative)  = 48（S01..S48・SPEC derive）
Act 構成（SPEC 秒）: HOOK 48.5 / OPENING 43.5 / ACT1 121.3 / ACT2 109.2 / ACT3 253.7 / ENDING 115.6
```

**Aにとっての意味は1つ:** > **224カット / distinct 192 / 初出85.71% = still 84 + factory 92 + motion 16。**（§3 で積算）

> **注意（命名差）:** SPEC の視覚シーンは S01..S48。しかし **still は 84 本の固有プロンプトを持つ**ため、still の資産 ID は **S01..S84**（1プロンプト＝1枚）で採番する。48 の narrative シーンに 84 枚を配分する（ドクトリン核の ACT3 が最も厚い）。**still 資産 ID（S01..S84）と narrative シーンコード（S01..S48）は別物。** `covers_scene_id` は still 資産 ID 空間を指す（§7.3）。

---

# 3. ★素材構成の確定値（SPEC の distinct/cuts をそのまま調達する）

## 3.1 SPEC の内訳（★この値で調達する・勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **84枚** | 100カット | 1.19回(≤2) | **84本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **92本** | 92カット | **各1回(1)** | 在庫 11,000本超から選抜（§7）・全点目視・EP39〜45 と sha256 被りゼロ |
| **i2v モーション** | **16本** | 32カット | 各2回(≤2) | 16本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **192点** | **224カット** | | |
| 合成レイヤー（particle/light/vfx） | 12本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |

**SDXL の生成バッチ（本編カットに出ない i2v 種を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **84枚** | 84プロンプト × 1枚（バリエーション0） |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **16枚** | 16種プロンプト × 1枚（バリエーション0） |
| **SDXL 生成バッチ合計** | **84 + 16 = 100枚（各1回）** | **`--variants 1`** |

> **サムネは新規生成しない。** 完成後に body 84枚から6枚を `also_thumb:true` で流用選抜（追加生成ゼロ）。**role=thumb / still_thumb を作らない。**

> **★紙芝居回避（EP40 の最大の失敗）:** **still-cut 100 / (factory 92 + i2v 32)=video 124** で **still-share 44.64% ≤45%・motion coverage 55.36% ≥45%** を構造的に保証する（§3.3）。**stillを増やしてfactoryを削るな。factory 92 が still-share≤0.45 を守る下限。**

## 3.2 still 84枚・factory 92本・i2v 16本の幕別配分（目安）

| 区間 | narration秒 | still（S番号） | factory | i2v |
|---|---|---|---|---|
| HOOK | 48.5 | 6（S01–S06） | 6 | 2（M01,M02） |
| OPENING | 43.5 | 6（S07–S12） | 4 | 0 |
| ACT1 "The search" | 121.3 | 16（S13–S28） | 14 | 3（M03,M04,M05） |
| ACT2 "Rights at the schoolhouse" | 109.2 | 16（S29–S44） | 14 | 3（M06,M07,M08） |
| ACT3 "Reasonableness" | 253.7 | 28（S45–S72） | 24 | 5（M09,M10,M11,M12,M13） |
| ENDING | 115.6 | 12（S73–S84） | 12 | 3（M14,M15,M16） |
| 繋ぎ（covers_scene_id:null） | — | — | 18 | — |
| **合計** | **715.9** | **84** | **92** | **16** |

> ACT3 は判例核（二段テスト・6-3・footnote 7）なので still も最多の28枚（最も遅く荘厳）。
> **★幕別の factory 内訳（この表・§7.2・CODEX_B）は非拘束の目安値**（合計 92 のみ確定・幕割当は柔軟）。ゲートは factory を各1回・合計 92 でしか見ない。**確定値は「合計 factory 92」だけ。**

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 224 = still 100 + factory 92 + i2v 32
[2] 平均ショット長 = narration 715.9 / 224 = 3.196秒/カット  ✓ (SPEC mean_shot 3.2・≤6.0)
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

**パス:** `episodes/PD-2026-046-tlo/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `tlo_assets.v1`（固定文字列）
**生産者:** `scripts/build_tlo_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致。** role enum は **`body | i2v_source | reject` のみ**（`thumb`/`still_thumb` を作らない）。サムネは `also_thumb:true` の body still **ちょうど6枚**。overlay は **ちょうど12本**。
**★★ `factory` 92 エントリ・`motion` 16 エントリを必ず全て書く（空配列禁止・EP45 の build 失敗の直接原因）。★★**

## 4.1 スキーマ（EP45 の `cleveland_assets.v1` と同型。counts / prefix を EP46 値に）

```jsonc
{
  "schema_version": "tlo_assets.v1",
  "episode_id": "PD-2026-046-tlo",
  "slug": "tlo",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_tlo_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 84,          // ==84
    "still_i2v_source": 16,    // ==16
    "motion": 16,              // ==16
    "factory": 92,             // ==92
    "overlay": 12              // ==12（distinct 素材に数えない）
  },
  "stills": [{
    "asset_id": "TLO-S01",                 // body: ^TLO-S\d{2}$（1..84） / i2v種: ^TLO-MS\d{2}$
    "scene_id": "S01",                     // still 資産 ID（§5.9 のプロンプト行に対応・S01..S84 空間）
    "role": "body",                        // body|i2v_source|reject（バリエーション概念なし＝各1枚）
    "also_thumb": false,                   // body から6枚だけ true（追加生成しない）
    "act": 0,                              // 0=HOOK/OPENING, 1=ACT1, 2=ACT2, 3=ACT3, 5=ENDING
    "path": "H:/pd-media/assets/ai/tlo/S01.png",
    "depth_path": "H:/pd-media/assets/ai/tlo/S01_depth.png",   // role=="body" は実在必須
    "public_path": "tlo/img/S01.png",      // role=="body" のみ非null
    "width": 3840, "height": 2160,         // 長辺>=3840
    "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 42.7,
    "tags": ["restroom_door","smoke_haze","symbolic","schoolhouse"],
    "caption_hint": "a school restroom door swinging shut with a thin haze of cigarette smoke over the sinks, no people",  // check_tlo_facts 検査対象（制約1-6）
    "seed": 0, "model": "juggernautXL_ragnarokBy",
    "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
    "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
           "has_identifiable_face": false, "has_human_body": false, "notes": ""}
  }],
  "motion": [{                             // ★16 エントリ全て記載（空配列禁止）
    "asset_id": "TLO-M01",                 // ^TLO-M\d{2}$（1..16）
    "source_scene_id": "M01_src",
    "source_still": "H:/pd-media/assets/ai/tlo/M01_src.png",   // role=="i2v_source" の画像
    "path": "H:/pd-media/assets/ai_video/tlo/M01_rife.mp4",
    "public_path": "tlo/motion/M01_rife.mp4",                  // ★必ず tlo/motion/…_rife.mp4
    "act": 0, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
    "sha256": "<64hex>", "tags": ["restroom_door","smoke"],
    "qc": {"reviewed": true, "on_theme": true, "artifact_free": true,
           "has_identifiable_face": false, "notes": ""}
  }],
  "factory": [{                            // ★92 エントリ全て記載（空配列禁止）
    "asset_id": "AF-BG-0731",              // 棚 assets/asset_manifest.v001.json の id をそのまま
    "path": "H:/pd-media/assets/factory/backgrounds/AF-BG-0731__...mp4",
    "public_path": "tlo/factory/F001__school_hallway_lockers.mp4",  // ★F001..F092 連番・必ず tlo/factory/ 下
    "type": "backgrounds", "subtype": "<label>",   // ★ラベル=検索語の記録。中身の保証ではない（§7.5）
    "kind": "video", "license": "Pexels License",  // ALLOWED_LICENSES のいずれか
    "sha256": "<64hex>", "act": 2, "covers_scene_id": "S34",  // §7.3 の割当のみ。繋ぎは null
    "duration_sec": 7.60, "width": 1920, "height": 1080, "mean_luma": 48.3,
    "eyeballed_content": "a long empty high-school hallway lined with metal lockers in cold light, no people",  // ★必須（§7.5）
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
           "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""}
  }],
  "overlay": [{
    "asset_id": "AF-PART-0044", "path": "H:/.../particle_assets/...mp4",
    "public_path": "tlo/overlay/...mp4", "type": "particle_assets", "subtype": "<label>",
    "license": "Pexels License", "sha256": "<64hex>", "blend_hint": "screen",
    "eyeballed_content": "slow dust motes drifting on black, loops cleanly",
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""}
  }]
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `schema_version=="tlo_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 84 / i2v_source 16 / motion 16 / factory 92 / overlay 12）に**一致**
3. 全 `path`/`depth_path`/`public_path` がディスクに実在
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `depth_path` と `public_path` が非null かつ実在
7. `qc.has_readable_text==true` / `qc.has_identifiable_face==true` / `qc.has_human_body==true` のいずれかは `role=="reject"`
8. `role=="i2v_source"` は `role=="body"` と**同一 asset_id を共有しない**（distinct 分離。i2v_source は `TLO-MS\d{2}`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39・EP40・EP41・EP42・EP43・EP44・EP45 の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない（＝目視していない本が混じっていない）
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど6**、かつ **`scene_id` 集合が `{S10,S15,S46,S52,S60,S78}`（§4.3）と完全一致**（追加生成ではなく body からの流用。**この集合は CODEX_B §11 と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|reject のみ）
16. `overlay` 配列長が**ちょうど12**
17. **`factory` 配列長が**ちょうど92**・全エントリに非空の `public_path`（`tlo/factory/` を含む）がある（空配列禁止＝EP45 事故）**
18. **`motion` 配列長が**ちょうど16**・全エントリに非空の `public_path`（`tlo/motion/` かつ `_rife.mp4`）がある（空配列禁止＝EP45 事故）**

`--reuse-feasibility` では §3.3 [5][6][7] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 84枚（S01..S84）= §5.9 の84プロンプトの生成物。各1枚。
2. i2v_source 16枚（MS01..MS16 / 種画像 M01_src..M16_src）= §8.1 の16種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. also_thumb : body のうち S10 / S15 / S46 / S52 / S60 / S78 の6枚に true（追加生成しない）
   = schoolhouse gate(S10) / purse on the desk(S15) / SCOTUS columns(S46) / scales(S52) / two-part staircase(S60) / locker hallway(S78)
4. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

---

# 5. A-1: SDXL 静止画のバッチ生成（84本 × 1枚・バリエーション0）

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-046-tlo/04_scenes/ai_prompts.v001.md   ← A が §5.2 の形式で書く
出力:  H:\pd-media\assets\ai\tlo\S<NN>.png（+ remotion/public/tlo/ に自動コピー）
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
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 46 --variants 1 --only S01
#   → ログ "episode=... shots=100 variants=1 ... -> 100 images" の shots が 100 であること

# 全100枚（body 84 + i2v種 16・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-046-tlo --variants 1
#   → 生成 S01.png ... S84.png / M01_src.png ... M16_src.png（各1枚。_02/_03 は作らない）
```

> QC で落ちたシーンの再生成は `--only S37`（**同じプロンプトで別シードを1枚**）。既存の>=3840はスキップ・不足だけ埋まる。**バリエーションを増やして水増ししない。枚数を減らして基準を下げるのも禁止。**

## 5.4 共通スタイル `[STYLE]`（全プロンプト末尾に必ず全文連結）

```
, cinematic still, cold-and-warm documentary grade, an American public high school of the mid-1980s where ordinary objects carry a case, the warm wood of a vice principal's desk under a low tungsten lamp and a school hallway lined with grey metal lockers under cool institutional light, set against the pale marble and tall columns of the United States Supreme Court in cold monumental light, a single schoolhouse-green accent as the one steady note, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, no human body
```

> **EP39〜EP45 との分離:** `navy interrogation room`/`electric blue`（EP39）・`midday sunlight`/`suburban demolition`/`bleached daylight`（EP40）・`prison cell`/`cellblock`/`sodium prison corridor`/`steel death-row`（EP41）・`Chicago apartment`/`ankle monitor`/`body-worn camera vest`（EP42）・`porch-amber house`/`ambulance red lights`/`tow-truck`（EP43）・`teal-green hospital corridor`/`clinical hospital`（EP44）・`worn kitchen table citation stack`/`county-jail booking`/`empty wallet on a kitchen table`（EP45）を**1語も含めない**。EP46 は 1980年代の公立高校（トイレのドア・廊下のロッカー・空の教室・副校長の木の机の上の purse・タバコ/巻紙）＋淡い大理石の最高裁列柱＋象徴の天秤（probable cause↔reasonable suspicion）＋二段の大理石階段（inception→scope）＋校門/校旗＋警官のバッジ（footnote 7 の境界）＋schoolhouse-green の一点差し色。

## 5.5 共通ネガティブ `[NEG]`（各 `Avoid:` の後に必ず全文付ける）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible paper, legible citation, legible case number, legible U.S. Reports citation, legible date, legible year, legible dollar amount, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, minor, child, teenager, kid, student face, schoolgirl, human face, human body, hand, arm, finger, crying person, weeping student, sensational distress, poverty porn, glamorized drugs, glamorous drug imagery, drug close-up, big pile of drugs, weapon, gun, blood, gore, nude, bare skin, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, navy interrogation room, electric blue, suburban demolition, prison cell, steel cellblock, sodium prison corridor, ankle monitor, body-worn camera, porch amber house, ambulance, tow truck, teal-green hospital corridor, clinical hospital, worn kitchen table, county-jail booking counter, empty wallet on a kitchen table
```

> ネガティブにも **制約違反語（"students have no rights", "no fourth amendment in school", "probable cause required in school", "unanimous", poverty porn 語, glamorized drugs 等）を書かない**（§1.3）。上のリストにも制約違反の断定文は含めていない。**未成年・子ども・生徒の顔・身体・手・扇情・薬物のグラマー化・可読の判例番号/日付/金額・ブランドロゴを NEG で明示的に抑制**（制約2/5）。ブランドロゴが写り得る絵（タバコの箱）は「plain unbranded pack」「blurred into an unreadable smear」で判読不能にする。

## 5.6 バリエーション軸（★EP46 では無効）

`generate_sdxl_4k.py` の `--variants 1` は各 stem を**1枚だけ**生成する。**`_02`/`_03` を作らない。** 反復回避は「84本の固有プロンプト＝84の別被写体」で担保する。

## 5.7 メタJSON

`generate_sdxl_4k.py` は画像を書くが per-image メタJSONは書かない。**A は QC 時に `qc_tlo_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.8 プロンプトの絶対ルール（84本すべてに適用）

- **顔なし・身体なし・手なし・裸体なし。** 人物は原則出さない（R1・制約5）。**T.L.O.（未成年）を後ろ姿・手元・シルエットでも描かない。**
- **可読文字なし。** 意見書・令状フォーム・索引カード・手紙・審判記録・カレンダーは雰囲気のみ（判読不能）。判例番号（469 U.S. 325）・日付（1985/1984）・票決の数字・金額・ブランドロゴを描かない（ロゴはぼかす）。
- **象徴オブジェのみ:** トイレのドア／薄い煙／木の机の上の purse／タバコの箱・巻紙（臨床的）／廊下のロッカー／空の教室・生徒机／裁判官席／令状フォーム／天秤（相当理由↔合理的疑い）／二段の大理石階段（inception→scope）／校門・校旗／大理石の最高裁列柱／警官のバッジ／schoolhouse-green の光条。
- **未成年を肖像化しない・扇情化しない**（制約5）: 泣く生徒・困窮・生徒の姿を描かない。尊厳をもって物だけで示す。
- **薬物を美化・グラマー化しない**（制約5）: 押収物は木の机に淡く・臨床的に・最小限に並べる程度。大量の薬物・グロー・きらめきを作らない。
- **過大化しない**（制約1）: 「生徒に権利がない／4Aが学校で不適用」に見える絵を作らない。校門で権利が生き残る象徴（半開きのドア・schoolhouse-green の光条）を持つ。
- **令状/相当理由を「学校で必要」と誤らせない**（制約2）: 令状フォームや相当理由の重りは「最高裁が退けた easy answer」の象徴としてのみ。注記で必要とされたと書かない。
- **警察と学校職員を混同しない**（制約3）: 警官のバッジは「footnote 7 の境界＝警察が入ると基準が戻り得る」の象徴。学校職員＝警官と描かない。

## 5.9 確定プロンプト（★`ai_prompts.v001.md` にこの84エントリをそのまま書く・各1枚）

> 各行の `[STYLE]` は §5.4 を、`Avoid:` の後の `[NEG]` は §5.5 を**全文展開**して書く（下記は簡潔表記のマクロ。省略記号ではなく定義済み定数）。全て顔なし・身体なし・手なし・象徴・判読不能・扇情なし・薬物非美化。

```
- `S01.png`
A school restroom door swinging shut in a mid-1980s public high school under cool fluorescent light, a thin haze of cigarette smoke hanging over a row of empty sinks, quiet and ordinary, no people, no reflection of a face, no readable sign [STYLE] Avoid: [NEG]
- `S02.png`
A thin veil of cigarette smoke drifting across an empty restroom mirror and sink in cool light, the moment a small school rule was broken, no people, no reflected face, no readable text [STYLE] Avoid: [NEG]
- `S03.png`
A worn canvas purse landing on a vice principal's wooden desk under a warm desk lamp against a cool office wall, the everyday bag about to be taken apart, still and central, no people, no readable text [STYLE] Avoid: [NEG]
- `S04.png`
A closed canvas purse sitting upright and alone on an administrator's wooden desk in warm lamplight, an ordinary object holding an entire case, no people, no readable text [STYLE] Avoid: [NEG]
- `S05.png`
A single plain unbranded pack of cigarettes resting on a wooden desk beside a closed purse under warm light, the first thing found on top of the bag, clinical and plain, no people, no readable text, no brand logo [STYLE] Avoid: [NEG]
- `S06.png`
A high-school hallway lined with grey metal lockers receding into low institutional light, the schoolhouse where the question begins, empty and quiet, no people, no readable numbers [STYLE] Avoid: [NEG]
- `S07.png`
A single student backpack hanging alone on a metal locker hook in a school hallway under cool light, the private cargo everyone carries into school, no people, no readable text [STYLE] Avoid: [NEG]
- `S08.png`
A closed school locker with its narrow vent slats in cool institutional light, the small private space a rule now reaches into, no people, no readable numbers [STYLE] Avoid: [NEG]
- `S09.png`
A heavy schoolhouse entrance door standing shut beneath a plain transom in cool morning light, the threshold the Fourth Amendment either crosses or waits outside, no people, no readable sign [STYLE] Avoid: [NEG]
- `S10.png`
A weathered schoolhouse gate beside a bare flagpole against a pale sky, the civic edge of a public school, quiet and monumental, no people, no readable sign, no legible flag insignia [STYLE] Avoid: [NEG]
- `S11.png`
The pale marble facade and tall columns of the United States Supreme Court at night, cold stone lit from below, the court that answered this in the mid-1980s, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S12.png`
A closed purse on a wooden desk in the warm foreground with the cold marble colonnade of the highest court faint and distant beyond it, the span from a school office to Washington, no people, no readable text [STYLE] Avoid: [NEG]
- `S13.png`
A girls' restroom in a public high school with two sinks and a shut stall door under cool fluorescent light, the ordinary room where a school rule was broken, no people, no readable sign [STYLE] Avoid: [NEG]
- `S14.png`
A front-office counter in a mid-1980s high school under cool light, warm wood against a pale institutional wall, where two students were sent after the restroom, no people, no readable text [STYLE] Avoid: [NEG]
- `S15.png`
A canvas purse tipped over on a vice principal's wooden desk under warm lamplight, its plain everyday contents implied only in soft shadow, the search about to begin, no people, no readable text [STYLE] Avoid: [NEG]
- `S16.png`
An empty assistant vice principal's office with a wooden desk, a vacant chair and a closed door in warm-and-cool light, the room where the questions were asked, no people, no readable text [STYLE] Avoid: [NEG]
- `S17.png`
A single plain unbranded pack of cigarettes standing upright on a wooden desk under warm light, the first object lifted from the top of the bag, clinical and plain, no people, no readable text, no brand logo [STYLE] Avoid: [NEG]
- `S18.png`
A thin plain packet of cigarette rolling papers lying in plain view on a wooden desk beside a pack of cigarettes, the small ordinary object that became the hinge of the whole case, clinical and muted, no people, no readable text [STYLE] Avoid: [NEG]
- `S19.png`
A plain overhead of a wooden desk where a rolling-papers packet sits just beside a pack of cigarettes, one item quietly pointing to the next, restrained and clinical, no people, no readable text [STYLE] Avoid: [NEG]
- `S20.png`
A small set of plain evidence items laid out in a neat row on a wooden desk under flat cool light, unglamorized and muted, the search widening step by step, no drugs glorified, no people, no readable text [STYLE] Avoid: [NEG]
- `S21.png`
A single empty small plastic bag and a plain simple pipe set clinically on a sheet of paper on a desk, muted and unsensational, evidence put down without drama, no drugs glorified, no people, no readable text [STYLE] Avoid: [NEG]
- `S22.png`
A plain fold of unmarked small bills held by a band on a wooden desk under cool light, the denominations abstract and completely unreadable, a quiet sign the search had changed, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S23.png`
A single index card lying on a wooden desk under warm light, a short handwritten list of names abstract and entirely unreadable, the record that reframed the search, no legible text, no people [STYLE] Avoid: [NEG]
- `S24.png`
Two plain folded letters resting on a wooden desk in cool light, their writing abstract and unreadable, documents that read as dealing, no legible words, no people [STYLE] Avoid: [NEG]
- `S25.png`
A juvenile courtroom bench and rail standing empty in cool institutional light, warm wood against pale plaster, where delinquency charges were brought, no people, no readable text [STYLE] Avoid: [NEG]
- `S26.png`
A plain motion document set down beside a resting gavel on a courtroom table under cool light, the request to throw the purse out, the text abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S27.png`
A closed purse sitting alone in a hard shaft of cool courtroom light, the single object the whole suppression fight was about, no people, no readable text [STYLE] Avoid: [NEG]
- `S28.png`
The modest brick facade of a 1980s county courthouse at dusk, ordinary and civic, the first rung of a climb toward Washington, no people, no readable sign [STYLE] Avoid: [NEG]
- `S29.png`
An empty classroom of the mid-1980s with rows of vacant wooden desks under cool light, the building full of students that a rule has to run, no people, no readable text [STYLE] Avoid: [NEG]
- `S30.png`
A single empty student desk holding one closed bag under cool classroom light, the private space at the center of the argument, no people, no readable text [STYLE] Avoid: [NEG]
- `S31.png`
A worn wooden chair behind a teacher's desk in an empty classroom under warm-and-cool light, the adult who stands in for order implied only by objects, no people, no readable text [STYLE] Avoid: [NEG]
- `S32.png`
A plain empty judge's bench in a courtroom under cool light, the neutral authority the school's easy answer wanted to bypass, no people, no readable text [STYLE] Avoid: [NEG]
- `S33.png`
A blank warrant form lying on a courtroom table beside a pen under cool light, the paperwork the police standard would have demanded, the print abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S34.png`
A long bank of grey metal school lockers receding under cool institutional light, the thousand private spaces a single school holds, no people, no readable numbers [STYLE] Avoid: [NEG]
- `S35.png`
A pair of plain scales resting on a school desk, an open everyday bag on one pan and a closed rulebook on the other, the two easy answers weighed and refused, abstract, no legible words, no people [STYLE] Avoid: [NEG]
- `S36.png`
A firmly closed schoolhouse door crossed by a single band of schoolhouse-green light, the position that the Constitution simply stops here, an answer the Court refused, no people, no readable sign [STYLE] Avoid: [NEG]
- `S37.png`
A plain police-style badge lying face-up on a cool institutional surface set apart from a school hallway beyond it, the police standard the Court also turned down for educators, no people, no readable text [STYLE] Avoid: [NEG]
- `S38.png`
An empty classroom doorway open onto a bright hallway of lockers, the Fourth Amendment travelling across the threshold with the student, warm light beyond the cool, no people, no readable sign [STYLE] Avoid: [NEG]
- `S39.png`
A single band of schoolhouse-green light running along a cool wall where a hallway meets an office, the right that does not stop at the schoolhouse door, symbolic and steady, no legible words, no people [STYLE] Avoid: [NEG]
- `S40.png`
A closed rulebook and one small everyday object resting together on a school desk under cool light, the balance between order and privacy the Court had to strike, abstract, no legible words, no people [STYLE] Avoid: [NEG]
- `S41.png`
A blank warrant form and a closed bag set on opposite ends of a desk under cool light, the choice between a criminal warrant and a school search the Court rejected, the print unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S42.png`
A schoolhouse door held half open onto a corridor of lockers in warm-and-cool light, the moment the Court said students keep their rights inside, warm light spilling in, no people, no readable sign [STYLE] Avoid: [NEG]
- `S43.png`
A pale marble step rising toward tall columns at dusk, the case climbing from a school office toward the highest court, monumental and quiet, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S44.png`
The tall columns of the United States Supreme Court seen frontally in cool evening light, the argument arriving where it would be decided, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S45.png`
An old leather-bound volume of law reports closed on a dark desk under a warm lamp, its worn spine title abstract and unreadable, the ruling rendered as a book, no legible text, no people [STYLE] Avoid: [NEG]
- `S46.png`
The tall columns and pale marble facade of the United States Supreme Court seen frontally at night, monumental and solemn, where the line was drawn six to three, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S47.png`
A single opinion volume lying open under a warm desk lamp, its pages reduced to abstract illegible lines, the majority opinion being written, no legible words, no people [STYLE] Avoid: [NEG]
- `S48.png`
A pale marble wall holding a single carved-looking band of light, the plain holding that the Fourth Amendment applies inside a public school, the characters abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S49.png`
A schoolhouse door standing open a hand's width onto warm light, students do not shed their rights at the schoolhouse door, symbolic and steady, no people, no readable sign [STYLE] Avoid: [NEG]
- `S50.png`
A pair of plain scales on a marble surface with a heavy weight being lifted off one pan, the bar lowered from probable cause toward a lighter standard, abstract and severe, no legible words, no people [STYLE] Avoid: [NEG]
- `S51.png`
Two plain scales standing side by side, one loaded heavy and one loaded light, probable cause on the street beside reasonable suspicion in a school, the labels abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S52.png`
A single balanced pair of scales in cool marble light weighing one everyday object against a closed rulebook, the reasonableness standard held level, abstract and dignified, no legible words, no people [STYLE] Avoid: [NEG]
- `S53.png`
A marble surface where a student's small private things rest on one side and a school's plain order rests on the other, the two interests weighed against each other, abstract, no legible words, no people [STYLE] Avoid: [NEG]
- `S54.png`
A wallet and a small plain personal object resting together on a school desk in warm light, the small private cargo a student carries, weighed in the balance, no legible text, no people [STYLE] Avoid: [NEG]
- `S55.png`
A low two-step marble staircase rising in cool light, the two-part test rendered as two stairs, symbolic and exact, no people, no text [STYLE] Avoid: [NEG]
- `S56.png`
The first step of a marble staircase lit while the second waits in shadow, a search justified at its inception, abstract and severe, no people, no text [STYLE] Avoid: [NEG]
- `S57.png`
The second step of a marble staircase catching the light above the first, a search reasonably related in scope, abstract, no people, no text [STYLE] Avoid: [NEG]
- `S58.png`
A narrow marble path that widens too far past a marked line, a search that outgrew its own excuse, symbolic and abstract, no people, no text [STYLE] Avoid: [NEG]
- `S59.png`
A single band of light dividing a marble floor into a small justified reason and a larger overreach, the limit the scope prong sets, abstract, no legible words, no people [STYLE] Avoid: [NEG]
- `S60.png`
A clean two-tier marble staircase seen frontally in cool light, inception below and scope above, the whole two-part inheritance of the case, monumental and abstract, no people, no text [STYLE] Avoid: [NEG]
- `S61.png`
A closed purse on a wooden desk with a marble staircase faint behind it, the bag measured against the two-part test, no people, no readable text [STYLE] Avoid: [NEG]
- `S62.png`
A plain unbranded pack of cigarettes on a desk beside an open bag under warm light, the reasonable grounds that justified opening it at first, clinical and plain, no people, no readable text, no brand logo [STYLE] Avoid: [NEG]
- `S63.png`
A rolling-papers packet lying in plain view on a desk turning the search toward drugs, the plain-view step that justified going further, muted and clinical, no people, no readable text [STYLE] Avoid: [NEG]
- `S64.png`
A neat clinical row of small evidence items on a wooden desk under flat light, each object tied to the one before it, unglamorized and minimal, no drugs glorified, no people, no readable text [STYLE] Avoid: [NEG]
- `S65.png`
A plain division scored abstractly into cool marble, one larger group set against a smaller group, the vote that decided the case rendered without numerals, the figures abstract and unreadable, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S66.png`
Six pale columns standing lit beside three columns held in shadow on a marble facade, a division rendered in stone, the balance of the ruling, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S67.png`
Three separate opinion volumes set apart from a larger stack on a dark shelf under a warm lamp, the justices who broke with the Court in part, their titles abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S68.png`
A single pair of scales tilted back toward the heavy side under cool light, the dissent's warning that a softened standard is easy to misuse, abstract and severe, no legible words, no people [STYLE] Avoid: [NEG]
- `S69.png`
An old worn law volume standing among newer ones on a marble shelf, two centuries of probable cause the dissent invoked, the spines abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S70.png`
A plain police-style badge resting apart on a cool surface at the edge of a school hallway, the line the Court drew for when law enforcement gets involved, no people, no readable text [STYLE] Avoid: [NEG]
- `S71.png`
A closed schoolhouse door beside a separate institutional door under cool light, the boundary between an educator keeping order and police using a school as a shortcut, no people, no readable sign [STYLE] Avoid: [NEG]
- `S72.png`
A single small band of light held at the foot of a tall marble column, the question the Court expressly reserved for another day, abstract and quiet, no legible words, no people [STYLE] Avoid: [NEG]
- `S73.png`
The same worn canvas purse resting on a vice principal's wooden desk under warm light, the object the whole question returns to, still and plain, no people, no readable text [STYLE] Avoid: [NEG]
- `S74.png`
A schoolhouse door standing open onto warm daylight, the Fourth Amendment walking into school with the student, the answer that has held since the mid-1980s, no people, no readable sign [STYLE] Avoid: [NEG]
- `S75.png`
A city street and a school hallway held together in one cool-and-warm frame, the full warrant protection outside beside the lighter protection within, no people, no readable sign [STYLE] Avoid: [NEG]
- `S76.png`
A single band of schoolhouse-green light holding steady across a wall of school lockers, the in-between standard built for one specific place, no legible words, no people [STYLE] Avoid: [NEG]
- `S77.png`
A pair of scales set level on a school desk in warm light, not no rights and not full rights but a standard held in between, abstract and calm, no legible words, no people [STYLE] Avoid: [NEG]
- `S78.png`
A long bank of school lockers receding into soft warm light, every locker and backpack the ruling reached after her, quiet and open, no people, no readable numbers [STYLE] Avoid: [NEG]
- `S79.png`
A single student backpack resting closed on a hallway bench under warm light, the private thing a real reason is still needed to open, no people, no readable text [STYLE] Avoid: [NEG]
- `S80.png`
A closed purse on a wooden desk with a single shaft of warm light across it, the line one student's bag drew for everyone who came after, no people, no readable text [STYLE] Avoid: [NEG]
- `S81.png`
A school hallway of lockers with a distant open door and warm light beyond, the room rising into a designed silence, no people, no readable sign [STYLE] Avoid: [NEG]
- `S82.png`
A schoolhouse door easing open onto a bar of soft morning light at the end of a locker-lined hall, a silence that finally carries a distant bell, no people, no readable sign [STYLE] Avoid: [NEG]
- `S83.png`
An empty classroom at first light with rows of quiet desks, the ordinary place the rule now governs, open-ended and calm, no people, no readable text [STYLE] Avoid: [NEG]
- `S84.png`
A single school locker left slightly ajar onto soft morning light in a slow pull-back, the held final image, unresolved but open, no people, no readable number [STYLE] Avoid: [NEG]
```

**枚数チェック:** 上記 84 エントリ（S01..S84）。§5.3 の `--only S01` ログで `shots=100`（body 84 + i2v種 16）を確認してから本番を回す。

---

# 6. A-2/A-3: 静止画のQC・目視・depth map

## 6.1 機械QC（body 84 + i2v種 16 = 全100枚・`qc_tlo_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `35.0<=mean_luma<=225.0`（EP46 は暖色ランプの机と冷たいロッカー廊下・大理石が混在→冷たい廊下/大理石側の黒潰れリスク。`check_visual_asset_qc.DARK_LUMA_FLOOR=45.0` を下回りすぎる本に注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject（`check_visual_asset_qc.NEARDUP_SIM=0.90`）。**バリエーション0なので本来ほぼ衝突しない。衝突したらプロンプトが被っている**（多数ある「purse on the desk」「ロッカー廊下」「大理石列柱」「天秤」「大理石階段」「schoolhouse door」系に注意） | 片方 reject＋プロンプト見直し |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・判例番号（469 U.S. 325）・日付（1985/1984）・金額・ブランドロゴが写っていないか（R1・制約2/6） | `has_readable_text=true`→reject |
| Q6 | 顔/未成年の混入 | **目視。** 識別可能な顔・未成年・生徒が写っていないか（R1・制約5） | `has_identifiable_face=true`→reject |
| Q7 | 身体/扇情/薬物美化の混入 | **目視。** 人体・手・裸体・泣く生徒・扇情、薬物の大量/グラマー化が写っていないか（制約5） | `has_human_body=true`→reject |

**Q5/Q6/Q7 は機械で判定しない。** コンタクトシートを出して**全100枚を実際に目視**する:

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-046-tlo --media image
#   → runs/qc/tlo_footage_contact_NN.png（20枚/シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-45 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** SDXL は平気で読める文字・顔・身体を描く。**特に制約2（可読の判例番号/日付/金額/ブランドロゴの非露出）・制約5（未成年の非肖像化・薬物の非美化）は目視でしか守れない。** S05/S17/S62（タバコ箱）はブランドロゴが判読不能であること、S23/S24/S26/S33（索引カード・手紙・令状フォーム）は読める文字が写っていないこと、S20/S21/S64（押収物）が薬物を大量・グラマーに描いていないこと、全 restroom/classroom/hallway 系に生徒・未成年・顔が写り込んでいないことを必ず目で確認する。

## 6.2 出力

```
episodes/PD-2026-046-tlo/05_visuals/still_qc.v001.json     # 100枚全部の行（reject も残す・sha256/phash/mean_luma/long_edge）
（build_footage_contact_sheet が runs/qc に出す）
```

## 6.3 accepted が100枚に届かなかったとき

```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 46 --variants 1 --only S37   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_tlo_stills.py
```
accepted body >= 84 かつ i2v_source >= 16 になるまで繰り返す。**基準を下げない・バリエーションを足して水増ししない。**

## 6.4 depth map（★新規スクリプトを作らず既存を使う）

```bash
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir "H:/pd-media/assets/ai/tlo"
```
- モデル `Intel/dpt-large`。出力 `<stem>_depth.png`（同サイズ L グレースケール）。冪等。
- **role が `body` の静止画は depth 必須**（`treatment:"depth"` が隣に `_depth.png` を要求。無いとレンダーがクラッシュ）。i2v 種（`M<NN>_src.png`）は depth 不要。
- staging 後に `remotion/public/tlo/img/` 側でも同名ペアが揃っていること（§10）。

---

# 7. A-4: factory 実写クリップ 92本の選定と全点目視QC

## 7.1 在庫の実態

```
H:\pd-media\assets\factory\   フラット構成
  backgrounds/     11,000本超（.mp4）  ← ★主力（学校の廊下/ロッカー・空の教室・校舎外観・校門/校旗・
                                          冷たい大理石の最高裁列柱・裁判所の外観/内観・夜の街・繋ぎ）
  light_assets/    …            合成レイヤー（暖色ランプ・冷たい fluorescent・大理石の光条）
  particle_assets/ …            合成レイヤー（教室/書庫の埃・大理石法廷の塵）
  vfx_overlays/    …            合成レイヤー（グレイン・光ノイズ）
  texture_assets/  …            紙・木・大理石のテクスチャ
  loops/           …            抽象的な繋ぎ
ファイル名規約: AF-<TYPECODE>-<4桁>__<subtype_slug>.<ext>（TYPECODE = BG|LIGHT|LOOP|PART|TEX|VFX）
棚レジストリ: C:\Users\aab15\Documents\prime-documentary\assets\asset_manifest.v001.json
   （トップキーは schema と assets。★必ず encoding="utf-8" で開く。cp932 既定だと落ちる）
```

## 7.2 選定条件

- **`kind=="video"` のみ。** 静止画 factory は使わない
- **92本ちょうど**（§3.3[7] より 92 は still-share≤0.45 を守る下限。減らせない）
- **各1回しか使わない**（`check_asset_reuse.MAX_USES_FACTORY=1`）
- 幕別割り当て（§3.2）: HOOK=6 / OPENING=4 / ACT1=14 / ACT2=14 / ACT3=24 / ED=12 ＋ 繋ぎ=18 ＝ 92
- **EP39（夜/取調室/青）・EP40（郊外/昼/破壊）・EP41（監獄/鉄/石の独房）・EP42（シカゴのアパート/足首モニタ）・EP43（RI の一軒家/porch-amber/救急車/レッカー）・EP44（ティール緑の病院の廊下/臨床）・EP45（労働者階級の台所/郡拘置所 booking）の絵柄を選ばない。** EP46 は 学校の廊下/ロッカー・空の教室・校舎外観・校門/校旗＋淡い大理石の最高裁列柱・裁判所の外観/内観＋夜〜夕暮れの civic 情景。**独房/鉄格子・病院・台所・booking を含むクリップを選ばない。生徒・子ども・未成年が写るクリップ、泣く人・扇情、薬物のグラマー映像を選ばない（制約5）。**

**既存の選定ツールで候補出し（新規に検索ロジックを書くな）:**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes   # テーマ一覧と件数
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query school_hallway --limit 96 --exclude-used --ep PD-2026-046-tlo --json
```
`--exclude-used` は `check_arc_nonrepeat.build_universe()` と同じ指紋集合を使うので出荷ゲート `arc_nonrepeat` と食い違わない。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・SDXLで作らない情景）

> **★`covers_scene_id` は still 資産 ID 空間（S01..S84・§2 注記）を指す。narrative シーン（DESIGN の S01..S48）とは別体系。** B はこの値を still 資産 ID として解決し、narrative シーンコードにクロスマップしない。

| covers | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S06 | 学校の廊下/ロッカー | `school_hallway` / `high_school_lockers` | 0 |
| S11 | 最高裁ファサード・列柱 | `supreme_court_building` / `marble_columns` | 0 |
| S13 | 学校のトイレ内観（無人） | `school_restroom` / `empty_school_bathroom` | 1 |
| S28 | 1980年代の郡庁舎外観（夕暮れ） | `county_courthouse` / `courthouse_exterior_dusk` | 1 |
| S29 | 空の教室（無人） | `empty_classroom` / `classroom_interior` | 2 |
| S32 | 法廷内観（無人・裁判官席） | `empty_courtroom` / `courtroom_bench` | 2 |
| S34 | ロッカーの列（学校の廊下） | `locker_bank` / `school_corridor` | 2 |
| S44 | 最高裁の列柱（正面・夕） | `supreme_court_columns` / `marble_facade` | 2 |
| S46 | 最高裁の列柱（正面・夜） | `supreme_court_night` / `courthouse_columns_night` | 3 |
| S66 | 大理石の列柱（分割の象徴） | `marble_colonnade` / `stone_columns` | 3 |
| S78 | 学校のロッカー廊下（受け） | `school_lockers_hallway` / `empty_school_corridor` | 5 |

**残り本数は covers を持たない繋ぎ・情景クリップ**（`covers_scene_id:null`）: 学校の廊下・空の教室・校門/校旗・校舎外観・冷たい大理石の列柱/廊下・法廷の外観/内観・夕暮れ〜夜の civic 情景・書庫の棚・抽象 `loops`。**暗いクリップに偏りすぎない**（§7.5 の暗側閾値・全体の1/3=約30本まで。暖色ランプ・昼光の教室・実用光を優先）。

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
    --ep PD-2026-046-tlo --media video --dir "<92本の staging フォルダ>"
#   → runs/qc/tlo_footage_contact_NN.png（各タイルにファイル名ラベル）
```

2. **コンタクトシートを実際に開き、92本すべてを1本ずつ見る**
3. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて**選定から外す**
4. 実写シネマティックB-roll（アニメ/CG臭排除）・EP46テーマ（学校の廊下/ロッカー・空の教室・校門/校旗・校舎外観・大理石の列柱/法廷）・ウォーターマークなし・識別可能な実在人物なし（制約5・R1）を確認
5. **★制約5の目視:** **生徒・子ども・未成年が写るクリップは使わない**（写る場合も後ろ姿/遠景/顔外しのみだが、学校題材ゆえ未成年が写り込みやすい＝厳格に排除）。**泣く人・扇情、薬物のグラマー映像を含むクリップを使わない。** 判事席・街頭の実在の顔が写るニュース映像を使わない（制約5）。**独房/鉄格子・病院・booking を含むクリップを使わない（他話分離）。**
6. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=45.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。
> **EP46 は冷たいロッカー廊下＋大理石＋夜の列柱が多いので暗側がリスク。** 平均輝度45未満のクリップが全体の40%を超えると FAIL。**暗いクリップは約30本（1/3）までに抑え、暖色ランプ・昼光の教室・夕暮れの実用光がある本を優先する。**

**1フレームで判断がつかない本は VLC/ffplay で再生して確認**（near-still は `check_animation_mix` を落とす）。

## 7.6 出力

```
episodes/PD-2026-046-tlo/05_stock/factory_selection.v001.json   # 選定理由と幕割り当て
episodes/PD-2026-046-tlo/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39〜EP45 との重複ゼロ（BLOCKING）

```bash
./.venv/Scripts/python.exe scripts/select_tlo_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` 〜 `episodes/PD-2026-045-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP46 の92本の積集合が**空**であることを確認。1件でも exit 1 で差し替え。**EP39〜EP45 のファイルは読むだけ。書き込み・移動・削除は一切しない。**

---

# 8. A-5: i2v モーション化 16本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする16本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）

種画像は §5 と同じ `generate_sdxl_4k.py --variants 1` で `M<NN>_src.png` として生成する（`ai_prompts.v001.md` に下記16行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `TLO-MS01..MS16`、モーション成果物の asset_id は `TLO-M01..M16`。

| # | asset_id | 種画像 | 動きの意味 | act |
|---|---|---|---|---|
| 1 | TLO-M01 | M01_src | 学校のトイレのドアが閉じる寸前＋薄い煙 | 0 |
| 2 | TLO-M02 | M02_src | canvas purse が木の机に落ちて収まる | 0 |
| 3 | TLO-M03 | M03_src | 机に伏せた purse への緩いプッシュ | 1 |
| 4 | TLO-M04 | M04_src | 巻紙の packet（plain view）・ランプの光が揺れる | 1 |
| 5 | TLO-M05 | M05_src | 机に並べた押収物への緩いドリー（臨床的） | 1 |
| 6 | TLO-M06 | M06_src | 空の教室・生徒机の列への緩い前進 | 2 |
| 7 | TLO-M07 | M07_src | ロッカーの長い列への緩い前進ドリー | 2 |
| 8 | TLO-M08 | M08_src | schoolhouse door が廊下へ半分開く | 2 |
| 9 | TLO-M09 | M09_src | 最高裁の列柱・冷たい光が動く | 3 |
| 10 | TLO-M10 | M10_src | 古い法律書・ランプの光と埃 | 3 |
| 11 | TLO-M11 | M11_src | 天秤が水平に落ち着く（reasonableness） | 3 |
| 12 | TLO-M12 | M12_src | 二段の大理石階段・inception→scope の緩いティルトアップ | 3 |
| 13 | TLO-M13 | M13_src | 警官のバッジ・冷たい光が移ろう（footnote 7） | 3 |
| 14 | TLO-M14 | M14_src | 机の上の purse への緩いプッシュ（受け） | 5 |
| 15 | TLO-M15 | M15_src | schoolhouse door が採光へ開き始める | 5 |
| 16 | TLO-M16 | M16_src | ロッカーが夜明けの光へ・緩いプルバック | 5 |

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの16行を追加・各1枚）

```
- `M01_src.png`
A school restroom door in a mid-1980s high school caught just before it swings shut under cool fluorescent light with a thin haze of cigarette smoke over the sinks, framed and still, no people, no reflected face, no readable sign [STYLE] Avoid: [NEG]
- `M02_src.png`
A worn canvas purse resting on a vice principal's wooden desk under a warm lamp, framed and poised, the everyday bag about to be taken apart, no people, no readable text [STYLE] Avoid: [NEG]
- `M03_src.png`
A canvas purse tipped over on a wooden desk under warm lamplight with its plain contents implied in soft shadow, still and poised for a slow push, no people, no readable text [STYLE] Avoid: [NEG]
- `M04_src.png`
A thin plain packet of cigarette rolling papers lying in plain view beside a pack of cigarettes on a wooden desk under warm light, still and poised, the hinge of the case, no people, no readable text, no brand logo [STYLE] Avoid: [NEG]
- `M05_src.png`
A small clinical row of plain evidence items laid out on a wooden desk under flat cool light, unglamorized and muted, still and poised for a slow dolly, no drugs glorified, no people, no readable text [STYLE] Avoid: [NEG]
- `M06_src.png`
An empty classroom of the mid-1980s with rows of vacant wooden desks under cool light, framed for a slow forward move, no people, no readable text [STYLE] Avoid: [NEG]
- `M07_src.png`
A long bank of grey metal school lockers receding into cool institutional light, framed for a slow forward dolly, no people, no readable numbers [STYLE] Avoid: [NEG]
- `M08_src.png`
A schoolhouse door held half open onto a corridor of lockers in warm-and-cool light, poised and still, the moment students keep their rights inside, no people, no readable sign [STYLE] Avoid: [NEG]
- `M09_src.png`
The pale marble colonnade of the United States Supreme Court at night lit from below, monumental and still, poised for a slow move, no people, no readable inscription [STYLE] Avoid: [NEG]
- `M10_src.png`
An old leather-bound law volume closed on a dark desk under a warm lamp with dust hanging in the light, still and poised, its title abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `M11_src.png`
A single balanced pair of scales in cool marble light weighing an everyday object against a closed rulebook, held level and poised, abstract, no legible words, no people [STYLE] Avoid: [NEG]
- `M12_src.png`
A clean two-tier marble staircase seen frontally in cool light, inception below and scope above, still and poised for a slow tilt up, symbolic and abstract, no people, no text [STYLE] Avoid: [NEG]
- `M13_src.png`
A plain police-style badge resting on a cool institutional surface at the edge of a school hallway under shifting cold light, still and poised, the reserved boundary, no people, no readable text [STYLE] Avoid: [NEG]
- `M14_src.png`
A closed canvas purse resting on a wooden desk under warm lamplight, still and held, the object the question returns to, no people, no readable text [STYLE] Avoid: [NEG]
- `M15_src.png`
A heavy schoolhouse door beginning to open onto a bar of warm daylight at the end of a locker-lined corridor, poised and still, no people, no readable sign [STYLE] Avoid: [NEG]
- `M16_src.png`
A long bank of school lockers under a soft grey dawn light turning slowly toward morning, still and open-ended, no people, no readable numbers [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_cleveland.py` を下敷きにパスと SHOTS だけ差し替え）

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
STILL_DIR     = H:\pd-media\assets\ai\tlo      # 種画像 M<NN>_src.png を読む
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\tlo
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, text, watermark, identifiable face, real person likeness, minor, child, student, crying person, gore, blood, glamorized drugs"
```

**ゲート:** `dry_validate`（length=5 で1回POSTして配線エラーを安く検出）/ `assert_loaded_completely`（部分ロード検出）/ `assert_frame_math`（フレーム計算）。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す）

```bash
py -3.11 scripts/comfy_wan_tlo.py --build            # グラフだけ（GPU触らない）
py -3.11 scripts/comfy_wan_tlo.py --run --shot M01   # 1本本番して目視
py -3.11 scripts/comfy_wan_tlo.py --run-all          # 残り15本（冪等・既存スキップ）
```
1本 24–73 GPU分・16本で 7–19時間。`/queue` `/history` を30秒間隔でポーリング。

## 8.4 RIFE で 48fps 化（`rife_tlo.py`・`rife_cleveland.py` と同手順）

```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは length=5 検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番にリネーム → RIFE 2x を**2回**（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. **フレーム数検証** `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC

- 顔・身体・未成年・扇情（泣く生徒）・薬物のグラマー化が生成されていないこと（NEG で抑えているが**必ず目視**・制約5）
- モーフィング/ちらつき/ワープが無いこと → あれば別シードで再生成
- M07/M16（ロッカー廊下）・M06（教室）は**識別可能な生徒・未成年・読める標識/番号**が写り込んでいないこと（制約2/5）
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（16本 × 2回 = 32カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど12本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **6本** | 教室/書庫の埃・大理石法廷の塵。黒背景 drift を screen 合成 |
| `light_assets` | **4本** | 暖色ランプ・冷たい fluorescent・大理石の光条・夜明けの採光 |
| `vfx_overlays` | **2本** | 微細なグレイン・冷たい光ノイズ |
| **合計** | **12本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/tlo/overlay/` に置き、`tlo_film.json` の `cuts[].src` には**出さない**（出すと factory 判定で1回制限を食う）。同じレイヤーを何度重ねてもよい（素材ではなく加工）。黒背景でループするものを選び `blend_hint` を書く。**§7.5 の目視QC対象**（12本・12分）。**合成レイヤーの発色は B が accent `#3F8F5F`（schoolhouse-green）に寄せる想定・A は色被りの素材を作らない（他話の gold/blue/amber/teal/crimson を選ばない）。**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --kind video --query dust_particles --limit 20 --exclude-used --ep PD-2026-046-tlo --json
```

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_tlo_assets.py`）

```
remotion/public/tlo/img/     ← role=body の静止画84枚（+ 同名 _depth.png）
remotion/public/tlo/factory/ ← 選定 factory .mp4 92本（F001..F092 連番にリネーム）
remotion/public/tlo/motion/  ← i2v M<NN>_rife.mp4 16本
remotion/public/tlo/overlay/ ← 合成レイヤー 12本
```
- `public_path` はマニフェストの値と実ファイルが一致すること（factory=`tlo/factory/F0NN__<subtype>.mp4` / motion=`tlo/motion/M<NN>_rife.mp4` / still=`tlo/img/S<NN>.png`）
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー（`import_to_remotion.py` の `conform_video(...,fps=30)` と同じ）
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する・外すと誤分類）:**
- factory の `public_path` は必ず `tlo/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む（`tlo/motion/` の下）
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も**含めない**
- 合成レイヤーは `tlo/overlay/` に置き `cuts[].src` に出さない

> **B のレンダは `--public-dir=public_slim`（Root.tsx に `id="Ep46Tlo"`）を使う想定だが、`public_slim` の構築は B の責務。** A は `remotion/public/tlo/` に正典（img/factory/motion/overlay 全メディア）を置くところまで（B が slim を派生させる）。**★factory/motion を空にしない（EP45 の build 失敗の直接原因）。**

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`

全静止画・i2v・factory・overlay を1行ずつ: `asset_id`/`path`/`source`（`ai_codex` or `factory`）/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力

```bash
./.venv/Scripts/python.exe scripts/build_tlo_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_tlo_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_tlo_asset_manifest.py --reuse-feasibility
```
この3つが exit 0 で「マニフェストが本番になった」。**★特に `--verify` の不変条件17・18（factory 92 / motion 16 の非空・public_path 充填）を確認する。Bのファイルを直接書き換えて知らせようとしない。**

---

# 11. 素材反復禁止ゲートの実仕様（`check_asset_reuse.py`）

```python
MAX_USES_FACTORY = 1        # 無料 + 11,000本超 → 繰り返す理由が無い
MAX_USES_MOTION  = 2
MAX_USES_STILL   = 2
MIN_FIRST_USE_SHARE = 0.70
```
種別判定は**パス文字列**（`kind_of()`）: `/factory` or `af-bg-` → factory / `.mp4|.mov|.webm` or `ai_video` or `_rife` → motion / それ以外 → still。§10.1 の命名規則を守る。

EP46 の設計値: still 100/84=1.19(≤2) / factory 92/92=1.0(≤1) / motion 32/16=2.0(≤2) / first-use 192/224=0.8571(≥0.70)。**全て達成可能。**

---

# 12. 絶対にやらないこと

- **EP39（frazier）/EP40（lech）/EP41（thompson）/EP42（young）/EP43（caniglia）/EP44（tekoh）/EP45（cleveland）のファイルに一切触らない。** 読み取りのみ可。素材・色（EP41 gold #E5B53A / EP42 blue #3B7DD8 / EP43 amber #E0913C / EP44 teal #2FA6A0 / EP45 crimson #B23A48）・音のレーンも分離。EP46 の accent は **schoolhouse-green #3F8F5F**（INK #0A0A0C・B が OP/AEカード/サムネで使用・A は絵で流用色を作らない）。
- **スレッドBの所有ファイル（§0.2）に触らない。** 特に `remotion/src/**` `scripts/ae/**` `scripts/build_tlo_film.py` `manifest.json` `04_scenes/shotlist*` `figures`。
  - **ただし `04_scenes/ai_prompts.v001.md` は A が書く**（`generate_sdxl_4k.py` の入力・§5.9/§8.1a）。B は読むだけ。
- **図解・トランジション・タイポの素材を探しに行かない。** 在庫が薄い/無いカテゴリは B が自作する。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。ローカル A1111・ComfyUI・RIFE は GPU を使うだけで課金なし（オーナー許可済み）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物・未成年の肖像・likeness・身体をどこにも作らない**（§1・制約5）。特に **T.L.O.（当時14歳）を後ろ姿・手元・シルエットでも描かない。**
- **6制約に反する文言・絵をプロンプト・タグ・注記・ファイル名のどこにも作らない**（§1.2/§1.3）:
  - 「生徒に権利なし/4A不適用/学校は何でも捜索できる」（制約1）／「令状・相当理由が学校で必要」化（制約2）／「警察も同じ/自由に捜索」（制約3）／誤った票決（unanimous/9-0/5-4 等）（制約4）／未成年の肖像化・薬物のグラマー化・扇情（制約5）／可読の判例番号(469 U.S. 325)/日付(1985/1984)/金額/ブランドロゴ（制約2/6）。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。反復回避は distinct 84 で担保（§0.1・§5.6）。
- **role=thumb / still_thumb を作らない・overlay を12本以外にしない。** サムネは also_thumb=true の body 6枚（§4.3 = {S10,S15,S46,S52,S60,S78}）。
- **★asset_manifest の factory/motion を空にしない。** factory 92・motion 16 を全エントリ public_path 付きで書く（§4.2 不変条件17・18＝EP45 の build 失敗の直接原因）。
- **★dochighlight figure（黒バー/box/underline）を作らない・言及しない。** これは figures の責務（B）だが、A の `tags`/`caption_hint`/`notes` にも `dochighlight` という文字列を書かない（grep で 0 を保つ）。
- **枚数・本数を「だいたい」で決めない。** §3 の確定値（still 84 / factory 92 / i2v 16 / distinct 192 / first-use 0.8571 / still-share 0.4464 / MG≥30 / 11.9分）と §3.3 の検算をそのまま使う。合わなければ実装ではなく**本書を疑って報告**。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** EP36は大聖堂を、EP38は牛を通した。**生成物・在庫クリップを実際に見る**（特に制約2/5は目視でしか守れない・書面の可読文字・ブランドロゴ・未成年・薬物のグラマー化も目視で排除）。

---

# 13. 完了報告に含めるもの

```
1. accepted 静止画の枚数と内訳（body 84 / i2v_source 16 / also_thumb 6 [S10/S15/S46/S52/S60/S78] / reject N）
2. factory 選定 92本のリスト（asset_id / subtype / eyeballed_content）と、subtype と食い違って外した本数、書面/タバコ箱クリップの「no readable text / no logo」確認、生徒/未成年が写らない確認
3. EP39/EP40/EP41/EP42/EP43/EP44/EP45 重複ゼロの確認結果
4. i2v 16本の frames / duration_sec と、SHORT? の有無
5. 合成レイヤー12本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code をそのまま貼る）
7. §3.3 の検算 [1]〜[7] を自分で再計算した結果
8. asset_manifest.v001.json の counts ブロック（still_body 84 / still_i2v_source 16 / motion 16 / factory 92 / overlay 12）と、
   ★factory 配列長=92・motion 配列長=16 が非空で public_path 充填済みであることの確認
9. 6制約・1枚前提の自己申告（無権利化/令状・相当理由が学校で必要/警察も同じ/誤票決/未成年肖像化/薬物グラマー化/扇情 が全出力に皆無・バリエーション0・T.L.O.非肖像化を目視確認・dochighlight 文字列ゼロ・A↔B同一スキーマ [schema tlo_assets.v1 / role enum body|i2v_source|reject / counts / also_thumb 集合 {S10,S15,S46,S52,S60,S78} / overlay 12 / factory 92 非空 / motion 16 非空]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
