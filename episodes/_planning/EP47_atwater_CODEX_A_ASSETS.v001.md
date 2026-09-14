# EP47 atwater — Codex スレッドA「素材生成」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN）も実装スレッドB（CODEX_B）のファイルも**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> **唯一の外部真実 = `episodes/_planning/EP47_atwater_PRODUCTION_SPEC.v001.json`**（機械生成）。本書の数値はそこから転記したもので、手書きで発明していない。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP47 / Episode ID: PD-2026-047-atwater / slug: atwater
Composition id: Ep47Atwater（B が Root.tsx に登録・A は staging まで）
事件:       Atwater v. City of Lago Vista, 532 U.S. 318 (2001)。決定 2001-04-24。
            シートベルト違反（罰金刑のみ・投獄不能）でも、現行犯なら令状なし custodial arrest は
            第4修正に反しない、と最高裁は 5-4 で判断＝UPHELD（合憲）。
            ★主題は「違法だったから」ではない。「合憲＝許される(the Court said police COULD)」ことの不気味さ。
            Souter 多数意見は逮捕を "pointless indignity" と認めつつ許容し、救済を立法に委ねた。
            O'Connor 反対（+3）が対抗軸。Gail Atwater は存命の私人（顔・身体・肖像を出さない・象徴のみ）。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**85本の固有プロンプト × 1枚 = 85枚**・バリエーション0） | `H:\pd-media\assets\ai\atwater\S<NN>.png` | 2–3.5時間（GPU） |
| A-1b | i2v 種画像の生成（**16本の固有プロンプト × 1枚 = 16枚**・バリエーション0） | `H:\pd-media\assets\ai\atwater\M<NN>_src.png` | 30–50分（GPU） |
| A-2 | 静止画のQCと目視（**目視必須**） | `05_visuals/still_qc.v001.json` + コンタクトシート | 1.5時間 |
| A-3 | depth map 生成（`treatment:"depth"` の必須入力） | `H:\pd-media\assets\ai\atwater\S<NN>_depth.png` | 20分 |
| A-4 | factory 実写クリップ **92本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | **2.5時間（うち目視だけで1時間以上）** |
| A-5 | i2v モーション化 **16本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\atwater\M<NN>_rife.mp4` | 7–19時間（GPU） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 **12本** | `05_stock/overlay_selection.v001.json` | 30分 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 20分 |
| A-8 | Remotion public への staging | `remotion/public/atwater/{img,factory,motion,overlay}/` | 30分 |

> **★★ 最重要の前提（EP42–46 から継続）: 1シーン1枚・バリエーション0 ★★**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 85本＝85行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **`--variants 1`** で回す。**`--variants 3` は使わない。`_02`/`_03` を作らない。**
> **総生成画像 = still 85 + i2v 種 16 = 101枚（各1回）。** factory 92本は生成でなく在庫からの選抜。
> **★`--only S01` のログで `shots=101` を確認**してから本番を回す（85 body + 16 i2v種 = 101）。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-047-atwater/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** このマニフェストは **A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致**で共有する（§4）。

> ★★ **EP45 の事故（本作で必ず回避）:** EP45 は asset_manifest に **stills しか埋めず factory/motion 配列を空のまま**出荷しかけた。**本作の `factory` 配列は 92 エントリ、`motion` 配列は 16 エントリを必ず public_path 付きで実体化する**（§4.4／§4.5 に全 92 + 16 を列挙済み。build スクリプトはこの列挙を消費するだけで、空配列を書かない）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\atwater\**` / `H:\pd-media\assets\ai_video\atwater\**` | **A** | 読み書き |
| `episodes/PD-2026-047-atwater/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-047-atwater/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/atwater/{img,factory,motion,overlay}/**` | **A** | 読み書き |
| `episodes/PD-2026-047-atwater/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_atwater_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-046-*/**` および EP39〜46 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を `read_prompts()` で読む） | `PD-2026-047-atwater --variants 1` / `47 --variants 1 --only S01` |
| `scripts/gen_depth_maps.py`（**既存**） | §6.4 の depth map | `--dir "H:/pd-media/assets/ai/atwater"` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-047-atwater --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit 96 --exclude-used --ep PD-2026-047-atwater --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-047-atwater` |

**★Aが新規作成するスクリプト（直近既存の複製。実在を `ls scripts/` で確認してから複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（複製元・実在確認済み） |
|---|---|---|
| `scripts/qc_atwater_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_cleveland_stills.py`（EP45） |
| `scripts/select_atwater_factory.py` | §7 の factory 92本の確定選定・EP39〜46 sha256 除外検証 | `scripts/select_cleveland_factory.py`（EP45） |
| `scripts/comfy_wan_atwater.py` | §8 の i2v 16本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_kidsforcash.py`（実在） |
| `scripts/rife_atwater.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_kidsforcash.py`（実在） |
| `scripts/build_atwater_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_cleveland_asset_manifest.py`（EP45） |
| `scripts/stage_atwater_assets.py` | §10 の staging | `scripts/stage_cleveland_assets.py`（EP45） |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある。あなたは **`ai_prompts.v001.md` を §5.2 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない。**
> **正確性ゲートは `check_atwater_facts.py`（B が実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の6制約に一致し、`check_atwater_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_atwater_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。
#   → ★factory 配列長==92 / motion 配列長==16 が非空で実体化していること（EP45 事故回避の必須不変条件）

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_atwater_asset_manifest.py --reuse-feasibility
#   → still >=85 / motion >=16 / factory >=92 / distinct 合計 >=193 / first-use >=0.70

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_atwater_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全92本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-047-atwater
#   → exit 0（factory_clip_qc.v001.json が staging 済み全クリップを reviewed:true で網羅）

# [A-DONE-5] EP39〜EP46 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_atwater_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39・EP40・EP41・EP42・EP43・EP44・EP45・EP46 の八つすべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（R1 ＋ 正確性6制約）★★★

**罰金刑のみの軽罪（シートベルト違反・投獄不能）でも、現行犯なら令状なし custodial arrest は第4修正に反しない、と最高裁は 5-4 で判断した＝UPHELD（合憲）。本作は逮捕を「違法(illegal / unconstitutional / struck down)」とは決して言わない。不気味さは「合憲＝許される(the Court said police COULD do this)」ことにある。Souter 多数意見は逮捕を "pointless indignity" と認めつつ許容し、救済を立法に委ねた。O'Connor 反対（+3）が対抗軸で、逐語引用は反対意見に帰属する。Gail Atwater は存命の私人で、顔・身体・肖像を一切出さない。象徴オブジェのみ。同乗の子ども2人を扇情化しない（年齢を強調しない・"empty child seats" 等の象徴のみ・泣く/怯える子どもを描かない）。捏造引用禁止。**

## 1.1 R1（生成ビジュアル全般）

1. **実在人物の顔・likeness・肖像を作らない。** Gail Atwater（存命私人）、Officer Bart Turek、Souter、O'Connor、Rehnquist/Scalia/Kennedy/Thomas/Stevens/Ginsburg/Breyer を**顔・身体・肖像として描かない**。人物は原則出さない（象徴オブジェのみ）。判事評言の逐語引用は AE カード（B の担当）であって画像ではない。
2. **実在の判決文・判例番号・条文・日付・金額の可読文字を再現しない。** チケット・免許証・訴状・意見書・条文ページ・カレンダーは雰囲気のみ（判読不能）。判例番号（532 U.S. 318）・日付（2001-04-24 / 1997）・金額（$25 / $50）・票決（5-4）は**画像に描かない**（AE/figures のタイポで出す＝B の担当）。**通貨は実在紙幣の肖像を描かない**（$50 の象徴は「featureless な紙幣状の紙・no portrait・no legible denomination」で表す）。会社/州のロゴは**ぼかして判読不能**にする。
3. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性6制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **逮捕を「違法(illegal / unlawful / unconstitutional / struck down / overturned)」と書かない。** 5-4 で UPHELD＝合憲。主題は "the Court said police COULD do this"。**"the arrest was illegal / unconstitutional / the Court struck it down / Atwater won" を書かない。** 許容は "constitutional" / "the police could" / "upheld" / "allowed" / "the rule of Atwater still stands"。同時に「もうどこでも逮捕できない／完全に禁止された(banned everywhere / no longer allowed anywhere)」も誤りなので書かない。
2. **Souter 多数意見の nuance を落とさない。** 逮捕を "pointless indignity（無意味な屈辱）" と認めつつ、4Aを事案ごとの利益衡量に曲げず、救済を立法に委ねた。逐語 "Atwater's claim to live free of pointless indignity..." は**多数意見**に帰属（画像には可読で描かない・AEカード＝B）。
3. **O'Connor 反対が対抗軸。** 逐語 "The Court neglects the Fourth Amendment's express command... it cloaks the pointless indignity that Gail Atwater suffered with the mantle of reasonableness." は**反対意見**として中立帰属（Courtに帰属させない・画像には可読で描かない）。
4. **票決 5-4**（Souter多数＝Rehnquist・Scalia・Kennedy・Thomas／O'Connor反対＝Stevens・Ginsburg・Breyer）。画像に数字を描かない（象徴の光点で表す）。
5. **Gail Atwater は存命の私人。顔・肖像・身体を描かない・象徴のみ。同乗の子ども2人を扇情化しない**（年齢を強調しない・"two empty child seats" 等の象徴のみ・泣く/怯える/嘆く子どもを描かない）。捏造引用禁止。
6. **数値: 罰金上限 $50**（テキサス法 $25–$50・no contest で$50）confidence high。判決日 2001-04-24。Officer Turek。confidence:medium（逮捕年1997・子の年齢3・5）はヘッジ／**画面に出さない**。数値はどれも画像に可読で描かない（AE/figures＝B）。

## 1.3 機械ゲート（`build_atwater_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
BANNED_PORTRAIT = re.compile(
    r"\bportrait\b|\bmugshot\b|likeness of|"
    r"face of (gail|atwater|turek|souter|o'?connor|rehnquist|scalia|kennedy|thomas|stevens|ginsburg|breyer)|"
    r"recognizable (real )?person|identifiable face|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"the arrest (was|is|were)\s*(illegal|unlawful|unconstitutional|struck down|overturned|invalidated)|"
    r"(illegal|unlawful|unconstitutional) (arrest|seizure|custodial arrest)|"
    r"(court|scotus|supreme court|justices?) (struck down|overturned|banned|outlawed|invalidated) (the |her |atwater'?s )?(arrest|seizure)|"
    r"atwater (won|prevailed|beat the|defeated)|"
    r"(arrests? (are|were) )?(banned|forbidden|no longer allowed) (everywhere|anywhere)|"
    r"police (can ?not|cannot|can'?t|may not) (ever )?arrest|"
    r"(crying|sobbing|screaming|terrified|weeping|distressed) (child|children|kid|kids|baby|toddler)|"
    r"poverty ?porn|weeping family",
    re.IGNORECASE)
```

> `BANNED_ACCURACY` は制約1・4・5を機械化したもの。プロンプト・タグ・`caption_hint`・注記のどこにも該当語を書かない。**"constitutional" / "the police could" / "upheld" / "allowed" / "pointless indignity"（帰属付き・AE） / "the rule of Atwater still stands" / "the remedy is legislative" は許容。** 禁止は「逮捕の違法化」・「どこでも禁止/完全禁止」化・「Atwaterが勝った」・子どもの扇情（泣く/怯える）だけ。

---

# 2. 台本の語数と尺の確定値（SPEC から転記・Aが素材点数を積算する根拠）

**★唯一の真実 = `episodes/_planning/EP47_atwater_PRODUCTION_SPEC.v001.json`。** 古い資料の wpm・語数は使うな。

```
words_total          = 2,135
narration_seconds    = 719.3   （= 12.0分・[SILENCE 1..] の実音無音を含む）
wpm_used             = 178.1
mean_shot            = 3.19秒/カット（SPEC 3.2）・max_shot 6.0
視覚シーン(narrative)  = 48（S01..S48・SPEC derive）
Act 構成（SPEC 秒・概算）: HOOK / OPENING / ACT1 / ACT2 / ACT3（最長・最も荘厳）/ ENDING
```

**Aにとっての意味は1つ:** > **総カット 225 / distinct 193 / 初出 85.78% = still 85 + factory 92 + motion 16。**（§3 で積算）

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

## 3.2 still 85枚・factory 92本・i2v 16本の幕別配分（目安・非拘束。合計だけが確定）

| 区間 | still（S番号） | factory | i2v |
|---|---|---|---|
| HOOK | 5（S01–S05） | 6 | 2（M01,M02） |
| OPENING | 3（S06–S08） | 3 | 0 |
| ACT1「その停止」 | 16（S09–S24） | 12 | 4（M03,M04,M05,M06） |
| ACT2「§1983の問い」 | 18（S25–S42） | 16 | 3（M07,M08,M09） |
| ACT3「合憲（判例核）」 | 28（S43–S70） | 24 | 4（M10,M11,M12,M13） |
| ENDING | 15（S71–S85） | 12 | 3（M14,M15,M16） |
| 繋ぎ（covers_scene_id:null） | — | 19 | — |
| **合計** | **85** | **92** | **16** |

> ACT3 は判例核（最も遅く荘厳）なので still も最多の28枚。**幕別の factory/i2v 内訳は非拘束の目安値**（合計 92 / 16 のみ確定）。ゲートは factory を各1回・合計 92 でしか見ない。

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 225 = still 101 + factory 92 + i2v 32
[2] 平均ショット長 = narration 719.3 / 225 = 3.197秒/カット  ✓ (SPEC mean_shot 3.2・≤6.0)
[3] 静止画占有率(check_animation_mix) = 101/225 = 44.89%  ✓ ≤45%（SPEC still_share 0.4489・余裕0.11%）
[4] motion coverage = (92+32)/225 = 124/225 = 55.11%     ✓ ≥45%
[5] per-asset 上限: still 101/85=1.19(≤2) / factory 92/92=1.0(≤1) / motion 32/16=2.0(≤2)  ✓
[6] first-use share = 193/225 = 0.8578                   ✓ ≥0.70（SPEC 一致）
[7] factory 下限: i2v 32 は固定なので factory は 92 を下回れない（92+32=124=video）。→ factory 92 は下限であり水増しではない。
```

> **[3] の余裕は 0.11% しかない。** still が85本を割ったら §6.3 の再生成で回復させ、**still-cut 101 を増やさない**（B側の shotlist が101で固定）。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-047-atwater/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `atwater_assets.v1`（固定文字列）
**生産者:** `scripts/build_atwater_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致。** role enum は **`body | i2v_source | reject` のみ**（`thumb`/`still_thumb` を作らない）。サムネは `also_thumb:true` の body still **ちょうど6枚**。overlay は **ちょうど12本**。

## 4.1 スキーマ（`atwater_assets.v1`）

```jsonc
{
  "schema_version": "atwater_assets.v1",
  "episode_id": "PD-2026-047-atwater",
  "slug": "atwater",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_atwater_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 85,          // ==85
    "still_i2v_source": 16,    // ==16
    "motion": 16,              // ==16
    "factory": 92,             // ==92
    "overlay": 12              // ==12（distinct 素材に数えない）
  },
  "stills":  [ /* §4.3: body 85 (ATWA-S01..S85) + i2v_source 16 (ATWA-MS01..MS16) */ ],
  "motion":  [ /* §4.5: ATWA-M01..M16 全16本・public_path 必須（★非空） */ ],
  "factory": [ /* §4.4: 92本・public_path 必須（★非空・EP45事故回避の核心） */ ],
  "overlay": [ /* §4.6: 12本 */ ]
}
```

### 4.1a stills[] のエントリ形（body 例）

```jsonc
{
  "asset_id": "ATWA-S01",                 // body: ^ATWA-S\d{2}$（01..85） / i2v種: ^ATWA-MS\d{2}$
  "scene_id": "S01",                      // still 資産 ID 空間（§5.9 のプロンプト行に対応・S01..S85）
  "role": "body",                         // body|i2v_source|reject（各1枚・バリエーション概念なし）
  "also_thumb": false,                    // body から6枚だけ true（§4.3・追加生成しない）
  "act": 0,                               // 0=HOOK/OPENING, 1=ACT1, 2=ACT2, 3=ACT3, 5=ENDING
  "path": "H:/pd-media/assets/ai/atwater/S01.png",
  "depth_path": "H:/pd-media/assets/ai/atwater/S01_depth.png",   // role=="body" は実在必須
  "public_path": "atwater/img/S01.png",   // role=="body" のみ非null
  "width": 3840, "height": 2160,          // 長辺>=3840
  "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 40.2,
  "tags": ["two_lane_road","texas","dusk","symbolic","road"],
  "caption_hint": "an empty two-lane Texas road at afternoon under a civil-violet sky, no people",
  "seed": 0, "model": "juggernautXL_ragnarokBy",
  "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
  "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
         "has_identifiable_face": false, "has_human_body": false, "notes": ""}
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `schema_version=="atwater_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 85 / i2v_source 16 / motion 16 / factory 92 / overlay 12）に**一致**
3. 全 `path`/`depth_path`/`public_path` がディスクに実在
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `depth_path` と `public_path` が非null かつ実在
7. `qc.has_readable_text==true` / `qc.has_identifiable_face==true` / `qc.has_human_body==true` のいずれかは `role=="reject"`
8. `role=="i2v_source"` は `role=="body"` と**同一 asset_id を共有しない**（i2v_source は `^ATWA-MS\d{2}$`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39・EP40・EP41・EP42・EP43・EP44・EP45・EP46 の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない（＝目視していない本が混じっていない）
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど6**、かつ **`scene_id` 集合が `{S01,S04,S13,S27,S30,S43}`（§4.3）と完全一致**（body からの流用。**この集合は CODEX_B と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|reject のみ）
16. `overlay` 配列長が**ちょうど12**
17. ★**`factory` 配列長==92 かつ全エントリ `public_path` が非空**（EP45 事故回避・空配列/stub を許さない）
18. ★**`motion` 配列長==16 かつ全エントリ `public_path` が非空**（同上）

`--reuse-feasibility` では §3.3 [5][6][7] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 85枚（S01..S85）= §5.9 の85プロンプトの生成物。各1枚。
2. i2v_source 16枚（MS01..MS16 / 種画像 M01_src..M16_src）= §8.1a の16種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. also_thumb : body のうち S01 / S04 / S13 / S27 / S30 / S43 の6枚に true（追加生成しない）
     （road=S01・handcuffs=S04・empty child seats=S13・scales=S27・$50-ticket=S30・SCOTUS=S43）
4. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

## 4.4 ★`factory[]` 全92エントリ（★必ず実体化・public_path 非空。EP45事故回避の核心）

> `select_atwater_factory.py` が下表の **public_path / act / covers_scene_id / subtype を pre-assign 済み**として消費し、`asset_id`（棚 id）/`path`（`H:/pd-media/assets/factory/...`）/`sha256`/`duration_sec`/`width`/`height`/`mean_luma`/`license`/`eyeballed_content`/`qc` を選抜・目視時に埋める（§7）。**空配列を書かない。** 各 public_path は `atwater/factory/F0NN_<subtype>.mp4`。`type:"backgrounds"`, `kind:"video"`。covers は still 資産 ID 空間（§7.3）。

```jsonc
// HOOK (act 0) — 6本
{ "public_path":"atwater/factory/F001_two_lane_texas_road.mp4",        "act":0, "covers_scene_id":"S01",  "subtype":"two_lane_texas_road" },
{ "public_path":"atwater/factory/F002_empty_road_heat_shimmer.mp4",    "act":0, "covers_scene_id":null,   "subtype":"empty_road_heat_shimmer" },
{ "public_path":"atwater/factory/F003_rural_highway_dusk.mp4",         "act":0, "covers_scene_id":null,   "subtype":"rural_highway_dusk" },
{ "public_path":"atwater/factory/F004_roadside_shoulder_afternoon.mp4","act":0, "covers_scene_id":null,   "subtype":"roadside_shoulder_afternoon" },
{ "public_path":"atwater/factory/F005_texas_hill_country_road.mp4",    "act":0, "covers_scene_id":null,   "subtype":"texas_hill_country_road" },
{ "public_path":"atwater/factory/F006_open_road_wide_sky.mp4",         "act":0, "covers_scene_id":null,   "subtype":"open_road_wide_sky" },
// OPENING (act 0) — 3本
{ "public_path":"atwater/factory/F007_lakeside_town_dusk.mp4",         "act":0, "covers_scene_id":"S06",  "subtype":"lakeside_town_dusk" },
{ "public_path":"atwater/factory/F008_supreme_court_columns.mp4",      "act":0, "covers_scene_id":"S07",  "subtype":"supreme_court_columns" },
{ "public_path":"atwater/factory/F009_small_town_texas_street_dusk.mp4","act":0,"covers_scene_id":null,   "subtype":"small_town_texas_street_dusk" },
// ACT1 (act 1) — 12本
{ "public_path":"atwater/factory/F010_country_road_pickup_distant.mp4","act":1, "covers_scene_id":null,   "subtype":"country_road_pickup_distant" },
{ "public_path":"atwater/factory/F011_police_station_exterior.mp4",    "act":1, "covers_scene_id":"S16",  "subtype":"police_station_exterior" },
{ "public_path":"atwater/factory/F012_municipal_building_night.mp4",   "act":1, "covers_scene_id":null,   "subtype":"municipal_building_night" },
{ "public_path":"atwater/factory/F013_empty_road_afternoon.mp4",       "act":1, "covers_scene_id":null,   "subtype":"empty_road_afternoon" },
{ "public_path":"atwater/factory/F014_rural_road_fence_line.mp4",      "act":1, "covers_scene_id":null,   "subtype":"rural_road_fence_line" },
{ "public_path":"atwater/factory/F015_texas_dusk_sky.mp4",            "act":1, "covers_scene_id":null,   "subtype":"texas_dusk_sky" },
{ "public_path":"atwater/factory/F016_patrol_car_parked_dusk.mp4",     "act":1, "covers_scene_id":null,   "subtype":"patrol_car_parked_dusk" },
{ "public_path":"atwater/factory/F017_station_hallway_cold.mp4",       "act":1, "covers_scene_id":null,   "subtype":"station_hallway_cold" },
{ "public_path":"atwater/factory/F018_small_town_intersection.mp4",    "act":1, "covers_scene_id":null,   "subtype":"small_town_intersection" },
{ "public_path":"atwater/factory/F019_open_highway_heat.mp4",          "act":1, "covers_scene_id":null,   "subtype":"open_highway_heat" },
{ "public_path":"atwater/factory/F020_roadside_grass_wind.mp4",        "act":1, "covers_scene_id":null,   "subtype":"roadside_grass_wind" },
{ "public_path":"atwater/factory/F021_country_road_evening.mp4",       "act":1, "covers_scene_id":null,   "subtype":"country_road_evening" },
// ACT2 (act 2) — 16本
{ "public_path":"atwater/factory/F022_courthouse_corridor.mp4",        "act":2, "covers_scene_id":"S40",  "subtype":"courthouse_corridor" },
{ "public_path":"atwater/factory/F023_empty_courtroom.mp4",            "act":2, "covers_scene_id":"S31",  "subtype":"empty_courtroom" },
{ "public_path":"atwater/factory/F024_marble_hallway_cold.mp4",        "act":2, "covers_scene_id":null,   "subtype":"marble_hallway_cold" },
{ "public_path":"atwater/factory/F025_courthouse_exterior_dusk.mp4",   "act":2, "covers_scene_id":"S42",  "subtype":"courthouse_exterior_dusk" },
{ "public_path":"atwater/factory/F026_federal_building_facade.mp4",    "act":2, "covers_scene_id":null,   "subtype":"federal_building_facade" },
{ "public_path":"atwater/factory/F027_courtroom_bench_empty.mp4",      "act":2, "covers_scene_id":null,   "subtype":"courtroom_bench_empty" },
{ "public_path":"atwater/factory/F028_law_library_shelves.mp4",       "act":2, "covers_scene_id":null,   "subtype":"law_library_shelves" },
{ "public_path":"atwater/factory/F029_marble_stairs_cold.mp4",        "act":2, "covers_scene_id":null,   "subtype":"marble_stairs_cold" },
{ "public_path":"atwater/factory/F030_clerk_office_cold.mp4",         "act":2, "covers_scene_id":null,   "subtype":"clerk_office_cold" },
{ "public_path":"atwater/factory/F031_patrol_car_roadside.mp4",        "act":2, "covers_scene_id":"S37",  "subtype":"patrol_car_roadside" },
{ "public_path":"atwater/factory/F032_empty_road_wide.mp4",           "act":2, "covers_scene_id":"S36",  "subtype":"empty_road_wide" },
{ "public_path":"atwater/factory/F033_highway_overpass_dusk.mp4",      "act":2, "covers_scene_id":null,   "subtype":"highway_overpass_dusk" },
{ "public_path":"atwater/factory/F034_texas_road_horizon.mp4",       "act":2, "covers_scene_id":null,   "subtype":"texas_road_horizon" },
{ "public_path":"atwater/factory/F035_courthouse_columns_day.mp4",     "act":2, "covers_scene_id":null,   "subtype":"courthouse_columns_day" },
{ "public_path":"atwater/factory/F036_office_corridor_fluorescent.mp4","act":2, "covers_scene_id":null,   "subtype":"office_corridor_fluorescent" },
{ "public_path":"atwater/factory/F037_marble_floor_light.mp4",        "act":2, "covers_scene_id":null,   "subtype":"marble_floor_light" },
// ACT3 (act 3) — 24本
{ "public_path":"atwater/factory/F038_supreme_court_columns_night.mp4","act":3, "covers_scene_id":"S43",  "subtype":"supreme_court_columns_night" },
{ "public_path":"atwater/factory/F039_supreme_court_steps_night.mp4",  "act":3, "covers_scene_id":null,   "subtype":"supreme_court_steps_night" },
{ "public_path":"atwater/factory/F040_marble_colonnade_night.mp4",     "act":3, "covers_scene_id":"S59",  "subtype":"marble_colonnade_night" },
{ "public_path":"atwater/factory/F041_supreme_court_facade_day.mp4",   "act":3, "covers_scene_id":null,   "subtype":"supreme_court_facade_day" },
{ "public_path":"atwater/factory/F042_marble_hallway_grand.mp4",       "act":3, "covers_scene_id":null,   "subtype":"marble_hallway_grand" },
{ "public_path":"atwater/factory/F043_law_library_old_volumes.mp4",    "act":3, "covers_scene_id":null,   "subtype":"law_library_old_volumes" },
{ "public_path":"atwater/factory/F044_courtroom_grand_empty.mp4",      "act":3, "covers_scene_id":null,   "subtype":"courtroom_grand_empty" },
{ "public_path":"atwater/factory/F045_marble_columns_light.mp4",       "act":3, "covers_scene_id":null,   "subtype":"marble_columns_light" },
{ "public_path":"atwater/factory/F046_state_capitol_dome_dusk.mp4",    "act":3, "covers_scene_id":"S57",  "subtype":"state_capitol_dome_dusk" },
{ "public_path":"atwater/factory/F047_capitol_rotunda_cold.mp4",       "act":3, "covers_scene_id":null,   "subtype":"capitol_rotunda_cold" },
{ "public_path":"atwater/factory/F048_marble_bench_curved.mp4",        "act":3, "covers_scene_id":null,   "subtype":"marble_bench_curved" },
{ "public_path":"atwater/factory/F049_courthouse_dome_night.mp4",      "act":3, "covers_scene_id":null,   "subtype":"courthouse_dome_night" },
{ "public_path":"atwater/factory/F050_marble_wall_shadow.mp4",         "act":3, "covers_scene_id":null,   "subtype":"marble_wall_shadow" },
{ "public_path":"atwater/factory/F051_grand_staircase_marble.mp4",     "act":3, "covers_scene_id":null,   "subtype":"grand_staircase_marble" },
{ "public_path":"atwater/factory/F052_law_books_shelf.mp4",           "act":3, "covers_scene_id":null,   "subtype":"law_books_shelf" },
{ "public_path":"atwater/factory/F053_courtroom_gallery_empty.mp4",    "act":3, "covers_scene_id":null,   "subtype":"courtroom_gallery_empty" },
{ "public_path":"atwater/factory/F054_marble_pillar_detail.mp4",       "act":3, "covers_scene_id":null,   "subtype":"marble_pillar_detail" },
{ "public_path":"atwater/factory/F055_supreme_court_plaza.mp4",        "act":3, "covers_scene_id":null,   "subtype":"supreme_court_plaza" },
{ "public_path":"atwater/factory/F056_government_building_dusk.mp4",   "act":3, "covers_scene_id":null,   "subtype":"government_building_dusk" },
{ "public_path":"atwater/factory/F057_marble_corridor_deep.mp4",       "act":3, "covers_scene_id":null,   "subtype":"marble_corridor_deep" },
{ "public_path":"atwater/factory/F058_courthouse_interior_cold.mp4",   "act":3, "covers_scene_id":null,   "subtype":"courthouse_interior_cold" },
{ "public_path":"atwater/factory/F059_archive_shelves_cold.mp4",       "act":3, "covers_scene_id":null,   "subtype":"archive_shelves_cold" },
{ "public_path":"atwater/factory/F060_flag_pole_dusk_generic.mp4",     "act":3, "covers_scene_id":null,   "subtype":"flag_pole_dusk_generic" },
{ "public_path":"atwater/factory/F061_marble_engraving_light.mp4",     "act":3, "covers_scene_id":null,   "subtype":"marble_engraving_light" },
// ENDING (act 5) — 12本
{ "public_path":"atwater/factory/F062_two_lane_road_dusk.mp4",         "act":5, "covers_scene_id":"S71",  "subtype":"two_lane_road_dusk" },
{ "public_path":"atwater/factory/F063_empty_road_evening.mp4",         "act":5, "covers_scene_id":null,   "subtype":"empty_road_evening" },
{ "public_path":"atwater/factory/F064_texas_road_horizon_violet.mp4",  "act":5, "covers_scene_id":null,   "subtype":"texas_road_horizon_violet" },
{ "public_path":"atwater/factory/F065_open_highway_dawn.mp4",          "act":5, "covers_scene_id":null,   "subtype":"open_highway_dawn" },
{ "public_path":"atwater/factory/F066_quiet_town_evening.mp4",         "act":5, "covers_scene_id":null,   "subtype":"quiet_town_evening" },
{ "public_path":"atwater/factory/F067_library_shelf_warm.mp4",        "act":5, "covers_scene_id":null,   "subtype":"library_shelf_warm" },
{ "public_path":"atwater/factory/F068_marble_shelf_light.mp4",        "act":5, "covers_scene_id":null,   "subtype":"marble_shelf_light" },
{ "public_path":"atwater/factory/F069_road_vanishing_point.mp4",      "act":5, "covers_scene_id":null,   "subtype":"road_vanishing_point" },
{ "public_path":"atwater/factory/F070_dusk_sky_open.mp4",             "act":5, "covers_scene_id":null,   "subtype":"dusk_sky_open" },
{ "public_path":"atwater/factory/F071_corridor_door_light.mp4",       "act":5, "covers_scene_id":null,   "subtype":"corridor_door_light" },
{ "public_path":"atwater/factory/F072_highway_evening_wide.mp4",      "act":5, "covers_scene_id":null,   "subtype":"highway_evening_wide" },
{ "public_path":"atwater/factory/F073_lakeside_evening.mp4",          "act":5, "covers_scene_id":null,   "subtype":"lakeside_evening" },
// 繋ぎ connective (covers null) — 19本
{ "public_path":"atwater/factory/F074_marble_light_shaft.mp4",        "act":1, "covers_scene_id":null,   "subtype":"marble_light_shaft" },
{ "public_path":"atwater/factory/F075_dust_in_light_bg.mp4",         "act":1, "covers_scene_id":null,   "subtype":"dust_in_light_bg" },
{ "public_path":"atwater/factory/F076_rain_asphalt_night.mp4",        "act":1, "covers_scene_id":null,   "subtype":"rain_asphalt_night" },
{ "public_path":"atwater/factory/F077_headlights_road_night.mp4",     "act":1, "covers_scene_id":null,   "subtype":"headlights_road_night" },
{ "public_path":"atwater/factory/F078_cloud_timelapse_dusk.mp4",      "act":1, "covers_scene_id":null,   "subtype":"cloud_timelapse_dusk" },
{ "public_path":"atwater/factory/F079_texas_field_wind.mp4",         "act":2, "covers_scene_id":null,   "subtype":"texas_field_wind" },
{ "public_path":"atwater/factory/F080_empty_parking_lot_dusk.mp4",    "act":2, "covers_scene_id":null,   "subtype":"empty_parking_lot_dusk" },
{ "public_path":"atwater/factory/F081_flag_texture_generic.mp4",      "act":2, "covers_scene_id":null,   "subtype":"flag_texture_generic" },
{ "public_path":"atwater/factory/F082_marble_texture_pan.mp4",        "act":2, "covers_scene_id":null,   "subtype":"marble_texture_pan" },
{ "public_path":"atwater/factory/F083_road_lines_passing.mp4",        "act":2, "covers_scene_id":null,   "subtype":"road_lines_passing" },
{ "public_path":"atwater/factory/F084_fluorescent_ceiling_pan.mp4",   "act":2, "covers_scene_id":null,   "subtype":"fluorescent_ceiling_pan" },
{ "public_path":"atwater/factory/F085_courthouse_window_light.mp4",   "act":3, "covers_scene_id":null,   "subtype":"courthouse_window_light" },
{ "public_path":"atwater/factory/F086_dusk_treeline.mp4",            "act":3, "covers_scene_id":null,   "subtype":"dusk_treeline" },
{ "public_path":"atwater/factory/F087_water_reflection_dusk.mp4",     "act":3, "covers_scene_id":null,   "subtype":"water_reflection_dusk" },
{ "public_path":"atwater/factory/F088_asphalt_heat_shimmer.mp4",      "act":3, "covers_scene_id":null,   "subtype":"asphalt_heat_shimmer" },
{ "public_path":"atwater/factory/F089_marble_floor_reflection.mp4",   "act":3, "covers_scene_id":null,   "subtype":"marble_floor_reflection" },
{ "public_path":"atwater/factory/F090_evening_sky_gradient.mp4",      "act":5, "covers_scene_id":null,   "subtype":"evening_sky_gradient" },
{ "public_path":"atwater/factory/F091_road_shoulder_gravel.mp4",      "act":5, "covers_scene_id":null,   "subtype":"road_shoulder_gravel" },
{ "public_path":"atwater/factory/F092_horizon_line_dusk.mp4",         "act":5, "covers_scene_id":null,   "subtype":"horizon_line_dusk" }
```

**内訳検算:** HOOK 6 + OPENING 3 + ACT1 12 + ACT2 16 + ACT3 24 + ENDING 12 + 繋ぎ 19 = **92** ✓。全 `public_path` 非空 ✓（不変条件17）。

## 4.5 ★`motion[]` 全16エントリ（★必ず実体化・public_path 非空）

> エントリ形は §4.1a 準拠 + 動画フィールド。`asset_id ^ATWA-M\d{2}$`。`source_still` は §8.1a の種画像、`source_scene_id`=`MS<NN>`。runtime で `sha256`/`width 1280`/`height 720`/`fps 48`/`frames`/`duration_sec`/`qc` を埋める（§8.4）。**空配列を書かない。**

```jsonc
{ "asset_id":"ATWA-M01","source_scene_id":"MS01","source_still":"H:/pd-media/assets/ai/atwater/M01_src.png","path":"H:/pd-media/assets/ai_video/atwater/M01_rife.mp4","public_path":"atwater/motion/M01_rife.mp4","act":0, "tags":["seatbelt","cab"] },
{ "asset_id":"ATWA-M02","source_scene_id":"MS02","source_still":"H:/pd-media/assets/ai/atwater/M02_src.png","path":"H:/pd-media/assets/ai_video/atwater/M02_rife.mp4","public_path":"atwater/motion/M02_rife.mp4","act":0, "tags":["road","patrol_lights"] },
{ "asset_id":"ATWA-M03","source_scene_id":"MS03","source_still":"H:/pd-media/assets/ai/atwater/M03_src.png","path":"H:/pd-media/assets/ai_video/atwater/M03_rife.mp4","public_path":"atwater/motion/M03_rife.mp4","act":1, "tags":["handcuffs","dashboard"] },
{ "asset_id":"ATWA-M04","source_scene_id":"MS04","source_still":"H:/pd-media/assets/ai/atwater/M04_src.png","path":"H:/pd-media/assets/ai_video/atwater/M04_rife.mp4","public_path":"atwater/motion/M04_rife.mp4","act":1, "tags":["empty_child_seats","cab"] },
{ "asset_id":"ATWA-M05","source_scene_id":"MS05","source_still":"H:/pd-media/assets/ai/atwater/M05_src.png","path":"H:/pd-media/assets/ai_video/atwater/M05_rife.mp4","public_path":"atwater/motion/M05_rife.mp4","act":1, "tags":["station_door","cold"] },
{ "asset_id":"ATWA-M06","source_scene_id":"MS06","source_still":"H:/pd-media/assets/ai/atwater/M06_src.png","path":"H:/pd-media/assets/ai_video/atwater/M06_rife.mp4","public_path":"atwater/motion/M06_rife.mp4","act":1, "tags":["booking_clock","hold"] },
{ "asset_id":"ATWA-M07","source_scene_id":"MS07","source_still":"H:/pd-media/assets/ai/atwater/M07_src.png","path":"H:/pd-media/assets/ai_video/atwater/M07_rife.mp4","public_path":"atwater/motion/M07_rife.mp4","act":2, "tags":["balance_scale","citation_vs_handcuffs"] },
{ "asset_id":"ATWA-M08","source_scene_id":"MS08","source_still":"H:/pd-media/assets/ai/atwater/M08_src.png","path":"H:/pd-media/assets/ai_video/atwater/M08_rife.mp4","public_path":"atwater/motion/M08_rife.mp4","act":2, "tags":["fourth_amendment_page","light"] },
{ "asset_id":"ATWA-M09","source_scene_id":"MS09","source_still":"H:/pd-media/assets/ai/atwater/M09_src.png","path":"H:/pd-media/assets/ai_video/atwater/M09_rife.mp4","public_path":"atwater/motion/M09_rife.mp4","act":2, "tags":["courthouse_corridor","dolly"] },
{ "asset_id":"ATWA-M10","source_scene_id":"MS10","source_still":"H:/pd-media/assets/ai/atwater/M10_src.png","path":"H:/pd-media/assets/ai_video/atwater/M10_rife.mp4","public_path":"atwater/motion/M10_rife.mp4","act":3, "tags":["supreme_court_colonnade","night"] },
{ "asset_id":"ATWA-M11","source_scene_id":"MS11","source_still":"H:/pd-media/assets/ai/atwater/M11_src.png","path":"H:/pd-media/assets/ai_video/atwater/M11_rife.mp4","public_path":"atwater/motion/M11_rife.mp4","act":3, "tags":["five_vs_four_light","vote"] },
{ "asset_id":"ATWA-M12","source_scene_id":"MS12","source_still":"H:/pd-media/assets/ai/atwater/M12_src.png","path":"H:/pd-media/assets/ai_video/atwater/M12_rife.mp4","public_path":"atwater/motion/M12_rife.mp4","act":3, "tags":["law_volumes","dust"] },
{ "asset_id":"ATWA-M13","source_scene_id":"MS13","source_still":"H:/pd-media/assets/ai/atwater/M13_src.png","path":"H:/pd-media/assets/ai_video/atwater/M13_rife.mp4","public_path":"atwater/motion/M13_rife.mp4","act":3, "tags":["mantle_shadow","marble"] },
{ "asset_id":"ATWA-M14","source_scene_id":"MS14","source_still":"H:/pd-media/assets/ai/atwater/M14_src.png","path":"H:/pd-media/assets/ai_video/atwater/M14_rife.mp4","public_path":"atwater/motion/M14_rife.mp4","act":5, "tags":["open_door","closed_door"] },
{ "asset_id":"ATWA-M15","source_scene_id":"MS15","source_still":"H:/pd-media/assets/ai/atwater/M15_src.png","path":"H:/pd-media/assets/ai_video/atwater/M15_rife.mp4","public_path":"atwater/motion/M15_rife.mp4","act":5, "tags":["two_lane_road","evening"] },
{ "asset_id":"ATWA-M16","source_scene_id":"MS16","source_still":"H:/pd-media/assets/ai/atwater/M16_src.png","path":"H:/pd-media/assets/ai_video/atwater/M16_rife.mp4","public_path":"atwater/motion/M16_rife.mp4","act":5, "tags":["door_ajar","final"] }
```

**検算:** 16エントリ ✓・全 public_path 非空 ✓（不変条件18）・`^ATWA-M\d{2}$` ✓。

## 4.6 `overlay[]` 12エントリ（distinct 素材に数えない）

```jsonc
// particle 6
{ "public_path":"atwater/overlay/P01_marble_dust_motes.mp4",  "type":"particle_assets","subtype":"marble_dust_motes",  "blend_hint":"screen" },
{ "public_path":"atwater/overlay/P02_courtroom_dust.mp4",     "type":"particle_assets","subtype":"courtroom_dust",     "blend_hint":"screen" },
{ "public_path":"atwater/overlay/P03_archive_dust.mp4",       "type":"particle_assets","subtype":"archive_dust",       "blend_hint":"screen" },
{ "public_path":"atwater/overlay/P04_fine_grain_dust.mp4",    "type":"particle_assets","subtype":"fine_grain_dust",    "blend_hint":"screen" },
{ "public_path":"atwater/overlay/P05_light_dust_drift.mp4",   "type":"particle_assets","subtype":"light_dust_drift",   "blend_hint":"screen" },
{ "public_path":"atwater/overlay/P06_shadow_dust.mp4",        "type":"particle_assets","subtype":"shadow_dust",        "blend_hint":"screen" },
// light 4
{ "public_path":"atwater/overlay/L01_warm_afternoon_shaft.mp4","type":"light_assets","subtype":"warm_afternoon_shaft","blend_hint":"screen" },
{ "public_path":"atwater/overlay/L02_cold_fluorescent_flicker.mp4","type":"light_assets","subtype":"cold_fluorescent_flicker","blend_hint":"screen" },
{ "public_path":"atwater/overlay/L03_marble_light_shaft.mp4", "type":"light_assets","subtype":"marble_light_shaft",   "blend_hint":"screen" },
{ "public_path":"atwater/overlay/L04_violet_edge_glow.mp4",   "type":"light_assets","subtype":"violet_edge_glow",     "blend_hint":"screen" },
// vfx 2
{ "public_path":"atwater/overlay/V01_film_grain.mp4",         "type":"vfx_overlays","subtype":"film_grain",           "blend_hint":"overlay" },
{ "public_path":"atwater/overlay/V02_cold_light_noise.mp4",   "type":"vfx_overlays","subtype":"cold_light_noise",     "blend_hint":"screen" }
```

runtime で `asset_id`/`path`/`sha256`/`license`/`eyeballed_content`/`qc` を埋める（§9）。**overlay は `cuts[].src` に出さない。** 発色は B が accent `#7A5CD0`（civil-violet）に寄せる想定・A は他話色（gold/blue/amber/teal/crimson/green）の素材を選ばない。

---

# 5. A-1: SDXL 静止画のバッチ生成（85本 × 1枚・バリエーション0）

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-047-atwater/04_scenes/ai_prompts.v001.md   ← A が §5.2 の形式で書く
出力:  H:\pd-media\assets\ai\atwater\S<NN>.png（+ remotion/public/atwater/ に自動コピー）
2段パイプライン: txt2img 1536x864 → hires 3072x1728 → extras R-ESRGAN 4x+ → 3840x2160（長辺≥3840・冪等スキップ）
```

**ローカルGPU生成に課金は発生しない。** 禁止は ElevenLabs TTS / 課金画像API / アップロードのみ（§12）。

## 5.2 ★パーサ契約（`read_prompts()` はこの2行形式しか読まない）

```
- `S01.png`
<positive prompt> Avoid: <negative>
```

- **1行目:** `` - `S01.png` ``（バッククォート囲み・行末は `.png` の直後）
- **2行目:** 正プロンプト → `Avoid:` → 負プロンプト
- `ai_prompts.v001.md` は **body 85行（S01..S85）＋ i2v 種 16行（M01_src..M16_src、§8.1a）＝ 101 エントリ**を書く。すべて1枚生成。

## 5.3 生成コマンド（★`--variants 1`。`--variants 3` は使わない）

```bash
# まず1枚だけ回して読める行数を確認（★shots=101 でなければ形式が壊れている）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 47 --variants 1 --only S01
#   → ログ "episode=... shots=101 variants=1 ... -> 101 images" の shots が 101 であること

# 全101枚（body 85 + i2v種 16・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-047-atwater --variants 1
#   → 生成 S01.png ... S85.png / M01_src.png ... M16_src.png（各1枚。_02/_03 は作らない）
```

> QC で落ちたシーンの再生成は `--only S37`（同じプロンプトで別シードを1枚）。**基準を下げない・バリエーションで水増ししない。**

## 5.4 共通スタイル `[STYLE]`（全プロンプト末尾に必ず全文連結）

```
, cinematic still, dark documentary grade, dusty warm Texas afternoon light over an open two-lane road and a worn pickup-truck interior, set against the cold institutional interior of a small-town police station booking area and the pale marble of a courthouse and the United States Supreme Court, a single civil-violet accent as the one cool signature note, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, low-key deep-shadow lighting, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face
```

> **EP39〜EP46 との分離（1語も含めない）:** `navy interrogation room`/`electric blue`（EP39 frazier）・`suburban demolition`/`bleached daylight`（EP40 lech）・`prison cell`/`cellblock`/`sodium prison corridor`（EP41 thompson・gold）・`Chicago apartment`/`ankle monitor`/`body-worn camera`（EP42 young・blue #3B7DD8）・`porch-amber house`/`ambulance red lights`/`tow-truck`（EP43 caniglia・amber #E0913C）・`teal-green hospital corridor`/`clinical hospital`（EP44 tekoh・teal #2FA6A0）・`warm-tungsten kitchen table`/`overdue crimson citation stack`（EP45 cleveland・crimson #B23A48）・EP46 tlo の green `#3F8F5F` 系。**EP47 は 埃っぽい暖色のテキサス午後の二車線道・ピックアップ車内（空のチャイルドシート2つ）・冷たい小さな町の警察署 booking・淡い大理石の裁判所と最高裁列柱・civil-violet `#7A5CD0` の一点差し色・夕暮れ。**

## 5.5 共通ネガティブ `[NEG]`（各 `Avoid:` の後に必ず全文付ける）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible ticket, legible citation, legible case citation, legible statute number, legible dollar amount, legible date, u.s. reports number, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, human body, child, crying child, terrified child, distressed child, weeping family, sensational distress, poverty porn, weapon, gun, blood, gore, nude, bare skin, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, navy interrogation room, electric blue, suburban demolition, tow truck, ambulance, porch amber house, ankle monitor, body-worn camera, prison cell, steel cellblock, barred cell, sodium prison corridor, teal-green hospital corridor, clinical hospital, warm tungsten kitchen table, overdue crimson citation stack
```

> ネガティブにも **制約違反語（"illegal arrest", "unconstitutional", "atwater won", poverty porn 語 等）を書かない**（§1.3）。**扇情・泣く子ども・身体・可読の金額/日付/判例番号・通貨の肖像・会社/州ロゴを NEG で明示的に抑制**（制約2/5）。ロゴが必要な絵は「blurred into an unreadable smear」で判読不能に。

## 5.6 バリエーション軸（★EP47 では無効）

`--variants 1` は各 stem を**1枚だけ**生成する。反復回避は「85本の固有プロンプト＝85の別被写体」で担保。

## 5.7 メタJSON

`generate_sdxl_4k.py` は per-image メタJSONを書かない。**A は QC 時に `qc_atwater_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.8 プロンプトの絶対ルール（85本すべてに適用）

- **顔なし・身体なし・裸体なし。** Gail Atwater・Officer Turek・判事を個人として描かない（制約1/5）。
- **可読文字なし。** チケット・免許証・訴状・意見書・条文ページ・カレンダーは雰囲気のみ。判例番号・日付・金額（$25/$50）・票決（5-4）・会社/州ロゴを描かない。
- **通貨は実在紙幣の肖像を描かない。** $50 の象徴は「plain featureless banknote-shaped paper, no portrait, no legible denomination」。
- **象徴オブジェのみ:** テキサスの二車線道／ピックアップ車内の空のチャイルドシート2つ／外れたシートベルトのバックル／開いた手錠／警察署の扉／booking 台・指紋パッド・空の booking カメラ／$50 の featureless 紙幣／天秤（罰金票 vs 手錠）／最高裁列柱・9席・大理石／開いた扉と閉じた扉（救済は立法へ）／条文ページ（判読不能）／州境の地図（判読不能）。
- **子どもを扇情化しない**（制約5）: 泣く/怯える/嘆く子ども・家族を描かない。子どもは「空のチャイルドシート」等の象徴のみ・非露出。
- **逮捕を「違法」化しない**（制約1）: 逮捕が違法/無効に見える絵を作らない。不気味さは「合憲＝許される」。
- **票決を数字で描かない**（制約4）: 5-4 は光点/光の分割の象徴で（可読数字なし）。
- **多数/反対の逐語を可読で描かない**（制約2/3）: "pointless indignity" / "mantle of reasonableness" は AE カード（B）。画像は象徴のみ。

## 5.9 確定プロンプト（★`ai_prompts.v001.md` にこの85エントリをそのまま書く・各1枚）

> 各行の `[STYLE]` は §5.4 を、`Avoid:` の後の `[NEG]` は §5.5 を**全文展開**して書く（下記は簡潔表記のマクロ）。全て顔なし・身体なし・象徴・判読不能・子ども非扇情。

```
- `S01.png`
An empty two-lane rural road in Lago Vista Texas stretching to the horizon in dusty warm afternoon light under a wide civil-violet sky, the ordinary road where a small offense began, no people, no readable signage [STYLE] Avoid: [NEG]
- `S02.png`
The interior of a worn pickup-truck cab seen from the passenger side in warm afternoon light, two small empty child seats beside the driver's seat, the children present only as empty seats, quiet and dignified, no people, no face, no readable text [STYLE] Avoid: [NEG]
- `S03.png`
A close view of a single unbuckled seatbelt buckle hanging loose in a pickup-truck cab, the metal tongue swinging free in warm light, the small thing at the center of it all, no people, no readable text [STYLE] Avoid: [NEG]
- `S04.png`
A pair of open handcuffs resting on a pickup-truck dashboard in hard afternoon light, cold steel against warm dust, the tool that answered a seatbelt, no people, no readable text [STYLE] Avoid: [NEG]
- `S05.png`
An empty booking camera on a plain tripod facing a blank institutional wall in cold light, the flash yet to fire, a photograph waiting to be taken of no one, no people, no readable text [STYLE] Avoid: [NEG]
- `S06.png`
A quiet small Texas lake town at dusk, modest houses on the edge of still water under a fading civil-violet sky, the ordinary place this happened, no people, no readable signage [STYLE] Avoid: [NEG]
- `S07.png`
The pale marble facade and tall columns of the United States Supreme Court at night, cold stone lit from below, monumental and distant, the court that answered this in 2001, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S08.png`
A single unbuckled seatbelt buckle in warm foreground focus with the cold marble colonnade of the highest court faint and distant beyond it, the span from a fifty dollar offense to the highest court, no people, no readable text [STYLE] Avoid: [NEG]
- `S09.png`
A worn pickup truck pulled onto a two-lane road shoulder in the afternoon with a patrol car drawing in behind it, both seen at a distance in warm dusty light, the stop beginning, no people, no readable signage [STYLE] Avoid: [NEG]
- `S10.png`
The reflection of a patrol car's light bar caught in a pickup truck's side mirror in warm afternoon light, the approach seen only as a reflection, no people, no readable text [STYLE] Avoid: [NEG]
- `S11.png`
A closed traffic-citation ticket book left unopened on a patrol-car hood in hard afternoon light, the ticket that was never written, the paper abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S12.png`
A pair of open handcuffs held in hard afternoon light against the flank of a worn pickup truck, cold steel raised where a citation should have been, no people, no readable text [STYLE] Avoid: [NEG]
- `S13.png`
Two small empty child seats side by side in a pickup-truck cab in warm afternoon light, the children referenced only as empty seats, quiet and dignified, never shown, no people, no face, no readable text [STYLE] Avoid: [NEG]
- `S14.png`
A pickup truck's open driver door and empty seat with a loose seatbelt hanging out into the afternoon light, the driver removed, only objects remaining, no people, no readable text [STYLE] Avoid: [NEG]
- `S15.png`
The empty caged back seat of a patrol car seen through its window in cold afternoon light, a plain partition and vinyl bench, no bars of a cell, no people, no readable text [STYLE] Avoid: [NEG]
- `S16.png`
The plain brick exterior of a small-town Texas police station at dusk under a civil-violet sky, ordinary and civic, the door she was driven to, no people, no readable sign [STYLE] Avoid: [NEG]
- `S17.png`
A heavy station intake door standing shut under a plain wall light in a cold grey booking area, a plain institutional door closed, no bars, no cell, no people, no readable sign [STYLE] Avoid: [NEG]
- `S18.png`
An empty booking desk and intake counter in a cold grey station under fluorescent light, a plain institutional room, no bars, no cell, no people, no readable text [STYLE] Avoid: [NEG]
- `S19.png`
An empty fingerprint pad and ink roller resting on a booking desk in cold grey light, the small machine that records a person, no legible marks, no people, no readable text [STYLE] Avoid: [NEG]
- `S20.png`
A shallow property tray on a booking counter holding a pair of empty shoes and a few plain personal effects in cold light, shoes removed and possessions relinquished, no legible text, no people [STYLE] Avoid: [NEG]
- `S21.png`
An empty booking camera facing a blank height backdrop with no visible markings in cold grey light, a photograph of no one, no legible numerals, no people, no face, no readable text [STYLE] Avoid: [NEG]
- `S22.png`
A plain holding-room door locked from the outside with a bare bench faint beyond a small window in cold grey light, a spare municipal room, no steel bars, no cellblock, no people, no readable text [STYLE] Avoid: [NEG]
- `S23.png`
A plain wall clock in a cold grey booking area with its second hand caught mid-sweep, marking about an hour of waiting, a held silence, no legible numerals, no people [STYLE] Avoid: [NEG]
- `S24.png`
A magistrate's plain desk holding a folded bond form and a released-property envelope in cold light, the release that followed the hour, the paper abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S25.png`
An old parchment page suggesting the text of the Fourth Amendment under a warm lamp, the words abstract and unreadable, a single civil-violet band of light across it, the promise of reasonableness, no legible words, no people [STYLE] Avoid: [NEG]
- `S26.png`
A thick federal complaint folder resting on a plain desk in cold light, an ordinary person taking an official to court, the text abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S27.png`
A pair of plain balance scales weighing a small paper citation on one pan against a set of steel handcuffs on the other in cold light, the ticket against the arrest, symbolic and abstract, no legible text, no people [STYLE] Avoid: [NEG]
- `S28.png`
The same balance scales seen from a low angle with the handcuffs pan sinking heavy and the citation pan rising light in cold marble light, the weight of a full arrest, no legible text, no people [STYLE] Avoid: [NEG]
- `S29.png`
A single traffic-citation form lying alone on a courtroom table in cold light, its edge touched with civil-violet, the small ticket that could have ended it, the paper abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S30.png`
A pair of open handcuffs coiled beside a plain featureless banknote-shaped paper on a cold surface, a tiny fine set against the full weight of an arrest, no portrait, no legible denomination, no people, no readable text [STYLE] Avoid: [NEG]
- `S31.png`
An empty courtroom bench and rail standing in cold pale marble light, warm wood against pale stone, the room where the question would be argued, no people, no readable text [STYLE] Avoid: [NEG]
- `S32.png`
A rubber filing stamp resting upright beside an ink pad on a clerk's desk in cold light, the small machine that turns an arrest into a record, no legible text, no people [STYLE] Avoid: [NEG]
- `S33.png`
A fanned set of plain traffic-citation forms spread across a desk in cold light, the commonest kind of ticket multiplied, edges abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S34.png`
A cold marble wall carrying a single engraved-looking band of light where the word reasonable would live, the characters abstract and unreadable, the one measure the amendment uses, no legible words, no people [STYLE] Avoid: [NEG]
- `S35.png`
Two clean paths of light diverging across a cold marble floor, two opposing arguments pointing in opposite directions, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S36.png`
A single pickup truck seen tiny on a vast open Texas road beneath an enormous dusk sky, every driver the police might ever stop, small under the law, no people, no readable signage [STYLE] Avoid: [NEG]
- `S37.png`
A patrol car parked alone at a two-lane roadside at dusk in civil-violet light, empty and waiting, the ordinary traffic stop, no people, no readable text [STYLE] Avoid: [NEG]
- `S38.png`
A single badge-shaped glint of cold light on a dark surface, authority implied by one abstract highlight, probable cause conceded, no name, no legible text, no people [STYLE] Avoid: [NEG]
- `S39.png`
A traffic-citation pad and a pair of open handcuffs resting side by side on a patrol-car hood in cold light, the choice between the ticket and the cuffs laid bare, no legible text, no people [STYLE] Avoid: [NEG]
- `S40.png`
A long courthouse corridor receding into cold institutional light with polished floor and closed doors, the passage a case is carried up, no people, no readable signage [STYLE] Avoid: [NEG]
- `S41.png`
A neat stack of bound legal briefs on a desk in cold light, the arguments filed on both sides, the spines abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S42.png`
The modest stone facade of a federal courthouse at dusk under a civil-violet sky, civic and unremarkable, the lower courts the case passed through, no people, no readable sign [STYLE] Avoid: [NEG]
- `S43.png`
The pale marble facade and tall columns of the United States Supreme Court seen frontally at night, monumental and solemn, the court that would decide it, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S44.png`
An empty curved bench of nine seats in a grand marble courtroom under cold light, the nine places rendered without any person, solemn and still, no people, no readable text [STYLE] Avoid: [NEG]
- `S45.png`
Five points of civil-violet light standing against four dimmer points on a dark marble field, a bare majority rendered as light, no numerals, symbolic, no people, no text [STYLE] Avoid: [NEG]
- `S46.png`
A cold marble floor divided into a slightly larger lit share and a slightly smaller darker share, a single-vote margin rendered as light, no numerals, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S47.png`
An old volume of law reports lying open under a warm desk lamp, its pages reduced to abstract illegible lines, the centuries of inherited law the majority read, no legible words, no people [STYLE] Avoid: [NEG]
- `S48.png`
A receding shelf of old leather-bound law volumes in warm lamplight, the inherited common law of the founding era, the spine titles abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S49.png`
A founding-era quill and inkwell resting beside a heavy old statute volume under a warm lamp, the rules the framers would have known, the pages abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S50.png`
A single clean straight band of civil-violet light running across a cold marble floor, a clear bright-line rule easy to apply, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S51.png`
An old pocket watch on a dark surface with its hands blurred in swift motion under cold light, the split-second judgment forced on an officer at the roadside, no legible numerals, no people [STYLE] Avoid: [NEG]
- `S52.png`
A patrol car at a two-lane roadside at dusk with the road running on into civil-violet distance, the practical moment of a stop, empty and still, no people, no readable text [STYLE] Avoid: [NEG]
- `S53.png`
A single unbuckled seatbelt buckle held solemn in a hard shaft of cold light on a dark surface, her sympathetic case set apart, quiet and dignified, no people, no readable text [STYLE] Avoid: [NEG]
- `S54.png`
A pair of open handcuffs resting in a single hard shaft of cold light on pale marble, a gratuitous weight the Court named yet permitted, symbolic and severe, no people, no readable text [STYLE] Avoid: [NEG]
- `S55.png`
A single small folded paper set apart from a vast receding pile of case folders in cold light, one sympathetic case too small to bend the rule, the papers abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S56.png`
An open statute book under a warm lamp resting beside a closed constitution on a marble shelf, the fix written by the people who write the laws, the pages abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S57.png`
A state capitol dome at dusk under a civil-violet sky, civic and distant, the legislature where the remedy the majority pointed to belongs, no people, no readable sign [STYLE] Avoid: [NEG]
- `S58.png`
A plain map of the United States with some regions lit in civil-violet and others left in shadow in cold light, the many states that legislated limits, the labels abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S59.png`
The marble colonnade of the Supreme Court at night lit from below, cold and distant, the Constitution that simply did not forbid it, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S60.png`
Four points of civil-violet light standing apart from five brighter points on a dark marble field, the four who could not accept it, no numerals, symbolic, no people, no text [STYLE] Avoid: [NEG]
- `S61.png`
A pair of balance scales in cold light with the citizen's-liberty pan hanging heavy and the state's-interest pan riding light, the reasonableness balancing the dissent demanded, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S62.png`
A pair of open handcuffs looming large in the foreground over a tiny paper citation in cold light, the heaviest thing set on the smallest offense, the balance tipping, no legible text, no people [STYLE] Avoid: [NEG]
- `S63.png`
A single traffic-citation form standing alone in a shaft of warm light on a cold surface, the ticket the dissent said should have been written, the paper abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S64.png`
A cold marble wall bearing an engraved-looking band of light being slowly darkened by an encroaching shadow, an express command clouded over, symbolic and abstract, no legible words, no people [STYLE] Avoid: [NEG]
- `S65.png`
A heavy fold of shadow drawn like a mantle across an engraved-looking marble surface in cold light, a pointless indignity cloaked in the appearance of reason, symbolic, no legible words, no people [STYLE] Avoid: [NEG]
- `S66.png`
Four empty seats set slightly apart and in shadow at the end of a curved marble bench in cold light, the dissent that lost, solemn and still, no people, no readable text [STYLE] Avoid: [NEG]
- `S67.png`
A single gavel resting on its sounding block in a deserted grand marble courtroom under cold light, the authority of the Court held still, no people, no readable text [STYLE] Avoid: [NEG]
- `S68.png`
The pale marble facade of the Supreme Court seen frontally at night, the decision handed down and standing, monumental and cold, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S69.png`
A closed opinion volume set down under a warm lamp, its narrow rule now written, the pages abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S70.png`
A single unbuckled seatbelt buckle and a pair of open handcuffs together in one cold frame on a dark surface, the smallest offense and the full arrest joined, what the Court permitted, no legible text, no people [STYLE] Avoid: [NEG]
- `S71.png`
The empty two-lane Texas road again at dusk under a deep civil-violet sky, the question returning to where it began, quiet and open, no people, no readable signage [STYLE] Avoid: [NEG]
- `S72.png`
A single unbuckled seatbelt buckle hanging loose in a pickup cab in fading evening light, the small thing that started it, held once more, no people, no readable text [STYLE] Avoid: [NEG]
- `S73.png`
A pair of open handcuffs resting on a pickup dashboard in fading civil-violet light, the answer that they may, though they need not, no people, no readable text [STYLE] Avoid: [NEG]
- `S74.png`
An open statute book standing on a plain shelf under a warm lamp, the remedy that is a legislature and not a court, the pages abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S75.png`
A plain map of the United States divided by a bright civil-violet seam into a lit side and a shadowed side, states that protect against states that do not, the labels abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S76.png`
A single bright seam of civil-violet light drawn across a dark map surface, one side lit and one side dark, a protection only as strong as a statute, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S77.png`
A closed constitution rendered as a heavy book on a cold marble shelf with a single shaft of civil-violet light falling across it, a right only as strong as the law beneath it, its title abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S78.png`
An open door onto warm daylight standing beside a firmly closed door in cold shadow, the remedy left open to legislatures and the constitutional door held shut, symbolic, no people, no readable sign [STYLE] Avoid: [NEG]
- `S79.png`
A plain featureless banknote-shaped paper folded small beside a pair of open handcuffs on a cold surface, the smallest possible offense against the full weight of an arrest, no portrait, no legible denomination, no people [STYLE] Avoid: [NEG]
- `S80.png`
A worn pickup truck seen small on an open Texas road beneath a vast dusk sky, the mother in the pickup rendered only as a distant truck, quiet and dignified, no people, no readable signage [STYLE] Avoid: [NEG]
- `S81.png`
Two small empty child seats in a pickup cab once more in soft evening light, the children present only as quiet empty seats, dignified and never shown, no people, no face, no readable text [STYLE] Avoid: [NEG]
- `S82.png`
A seatbelt now fastened neatly across an empty pickup seat in warm evening light, buckled up at last, the small rule obeyed, no people, no readable text [STYLE] Avoid: [NEG]
- `S83.png`
A plain featureless banknote-shaped paper laid flat and settled on a plain surface in warm light, the fine paid and done, no portrait, no legible denomination, no people, no readable text [STYLE] Avoid: [NEG]
- `S84.png`
The empty two-lane road stretching to a deep civil-violet horizon at dusk, the line the Court drew and has not erased, open-ended and unresolved, no people, no readable signage [STYLE] Avoid: [NEG]
- `S85.png`
A plain door left slightly ajar onto soft evening light in a slow pull-back, the held final image, unresolved but open, no people, no readable sign [STYLE] Avoid: [NEG]
```

**枚数チェック:** 上記 85 エントリ（S01..S85）。§5.3 の `--only S01` ログで `shots=101`（body 85 + i2v種 16）を確認してから本番を回す。

---

# 6. A-2/A-3: 静止画のQC・目視・depth map

## 6.1 機械QC（body 85 + i2v種 16 = 全101枚・`qc_atwater_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `35.0<=mean_luma<=225.0`（EP47 は暖色のテキサス午後道と冷たい booking/大理石・夜の最高裁が混在→暗い booking/夜側が黒潰れリスク。`DARK_LUMA_FLOOR=45.0` を下回りすぎる本に注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject。**バリエーション0なので本来ほぼ衝突しない。衝突は道路系(S01/S71/S84)・手錠系(S04/S12/S73)・シートベルト系(S03/S53/S72)・最高裁列柱系(S07/S43/S59/S68)・空のチャイルドシート(S02/S13/S81)・光点の票決(S45/S46/S60)・扉(S17/S78/S85) の被りに注意** | 片方 reject＋プロンプト見直し |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・判例番号(532 U.S. 318)・日付(2001/1997)・金額($25/$50)・票決(5-4)・会社/州ロゴが写っていないか（R1・制約2/6） | `has_readable_text=true`→reject |
| Q6 | 顔の混入 | **目視。** 識別可能な顔・**通貨上の肖像**が写っていないか（R1・制約1/5） | `has_identifiable_face=true`→reject |
| Q7 | 身体/扇情の混入 | **目視。** 人体・裸体・**泣く/怯える子ども**・家族の扇情が写っていないか（制約5） | `has_human_body=true`→reject |

**Q5/Q6/Q7 は機械で判定しない。全101枚を実際に目視:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-047-atwater --media image
#   → runs/qc/atwater_footage_contact_NN.png（20枚/シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-46 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** SDXL は平気で読める文字・顔・身体を描く。**特に S05/S21（booking カメラ）は読める数字/顔が無いこと、S25/S34（条文/reasonable）は読める英字が無いこと、S30/S79/S83（$50 紙幣）は肖像・可読の額面が無いこと、S45/S46/S60（票決）は可読の数字が無いこと、S58/S75（地図）はロゴ/州名が判読不能なこと、S02/S13/S81（空のチャイルドシート）は子どもが写らず扇情でないこと、を必ず目で確認する。**

## 6.2 出力

```
episodes/PD-2026-047-atwater/05_visuals/still_qc.v001.json     # 101枚全部の行（reject も残す）
（build_footage_contact_sheet が runs/qc に出す）
```

## 6.3 accepted が101枚に届かなかったとき

```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 47 --variants 1 --only S37   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_atwater_stills.py
```
accepted body >= 85 かつ i2v_source >= 16 になるまで繰り返す。**基準を下げない・水増ししない。**

## 6.4 depth map（★既存を使う）

```bash
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir "H:/pd-media/assets/ai/atwater"
```
- モデル `Intel/dpt-large`。出力 `<stem>_depth.png`。冪等。
- **role が `body` の静止画は depth 必須**（無いとレンダーがクラッシュ）。i2v 種（`M<NN>_src.png`）は depth 不要。
- staging 後に `remotion/public/atwater/img/` 側でも同名ペアが揃っていること（§10）。

---

# 7. A-4: factory 実写クリップ 92本の選定と全点目視QC

## 7.1 在庫の実態

```
H:\pd-media\assets\factory\   フラット構成
  backgrounds/     11,000本超（.mp4）  ← ★主力（テキサスの二車線道/空き道路・夕暮れの小さな町・警察署や庁舎の外観・大理石の裁判所/長い廊下・空の法廷・最高裁列柱・州会議事堂・夜〜夕暮れ・繋ぎ）
  light_assets/    …            合成レイヤー（暖色午後光・冷たい fluorescent・大理石の光条・violet 差し）
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
- **各1回しか使わない**（`MAX_USES_FACTORY=1`）
- 幕別割り当て（§4.4）: HOOK=6 / OPENING=3 / ACT1=12 / ACT2=16 / ACT3=24 / ED=12 ＋ 繋ぎ=19 ＝ 92
- **EP39〜EP46 の絵柄を選ばない（§7.7 の分離語）。** EP47 は テキサスの二車線道/空き道路・夕暮れの小さな町・警察署/庁舎の外観・大理石の裁判所の長い廊下/空の法廷/最高裁列柱・州会議事堂・夜〜夕暮れの道。**鉄格子/独房/cellblock を選ばない（EP41 分離）。病院/臨床を選ばない（EP44 分離）。泣く子ども・家族の扇情・実在の顔が写るニュース映像を選ばない（制約5・R1）。**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes   # テーマ一覧と件数
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query courthouse --limit 96 --exclude-used --ep PD-2026-047-atwater --json
```
`--exclude-used` は出荷ゲート `arc_nonrepeat` と同じ指紋集合を使う。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・§4.4 に pre-assign 済み）

> **★`covers_scene_id` は still 資産 ID 空間（S01..S85）を指す。narrative シーン（S01..S48）とは別体系。**

| covers | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S01 | テキサスの二車線道（午後） | `two_lane_texas_road` / `rural_highway_afternoon` | 0 |
| S06 | 湖畔の小さな町（夕暮れ） | `lakeside_town_dusk` / `small_texas_town` | 0 |
| S07 | 最高裁ファサード・列柱 | `supreme_court_building` / `marble_columns` | 0 |
| S16 | 警察署の外観 | `police_station_exterior` / `small_town_police` | 1 |
| S31 | 空の法廷（無人） | `empty_courtroom` / `courtroom_interior` | 2 |
| S36 | 広い空き道路（俯瞰） | `empty_road_wide` / `open_highway` | 2 |
| S37 | 路傍のパトカー（夕暮れ） | `patrol_car_roadside` / `police_car_dusk` | 2 |
| S40 | 裁判所の長い廊下 | `courthouse_corridor` / `long_courthouse_hallway` | 2 |
| S42 | 連邦裁判所の外観（夕暮れ） | `courthouse_exterior_dusk` / `federal_courthouse` | 2 |
| S43 | 最高裁の列柱（正面・夜） | `supreme_court_columns` / `marble_facade_night` | 3 |
| S57 | 州会議事堂のドーム | `state_capitol_dome` / `capitol_dusk` | 3 |
| S59 | 最高裁の列柱（夜） | `marble_colonnade_night` / `courthouse_columns_night` | 3 |
| S71 | 夕暮れの空き道路（受け） | `two_lane_road_dusk` / `empty_road_evening` | 5 |

**残り本数は covers を持たない繋ぎ・情景クリップ**（`covers_scene_id:null`）: 大理石の廊下・空の法廷・列柱の光条・庁舎の外観・テキサスの空き道路・夜〜夕暮れの道・雨のアスファルト・書庫の棚・抽象 `loops`。**暗いクリップに偏りすぎない**（暗側は全体の1/3=約30本まで。暖色午後光・大理石の昼光・夕暮れ側を優先）。

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）

```python
ALLOWED_LICENSES = {"cc0","royalty_free","generated_owned","Pexels License","Pixabay Content License"}
```

## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★

> **推測ではなく実際に起きた事故。** EP36: `city_surveillance_camera_dome` が大聖堂。EP38: 牛が `documents_on_desk`。`subtype` は「その検索語で取った」記録であって**中身の保証ではない**。

**選抜92本は例外なく次を経る:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py \
    --ep PD-2026-047-atwater --media video --dir "<92本の staging フォルダ>"
#   → runs/qc/atwater_footage_contact_NN.png（各タイルにファイル名ラベル）
```

2. **コンタクトシートを実際に開き、92本すべてを1本ずつ見る**
3. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて**選定から外す**
4. 実写シネマティックB-roll（アニメ/CG臭排除）・EP47テーマ・ウォーターマークなし・識別可能な実在人物なし（制約1/5・R1）を確認
5. **★制約5の目視:** 人物が写るクリップは避け、写る場合も後ろ姿/遠景/顔外しのみ。**泣く/怯える子ども・家族の扇情を含むクリップは使わない。** 実在の判事/警官の顔が写るニュース映像を使わない。**鉄格子/独房/cellblock（EP41）・病院/臨床（EP44）を含むクリップを使わない。**
6. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=45.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。
> **EP47 は冷たい大理石・夜の最高裁が多いので暗側が本命リスク。** 平均輝度45未満が全体の40%を超えると FAIL。**暗いクリップは約30本（1/3）までに抑え、暖色午後光・大理石の昼光・夕暮れの実用光がある本を優先。**

**1フレームで判断がつかない本は VLC/ffplay で再生して確認**（near-still は `check_animation_mix` を落とす）。

## 7.6 出力

```
episodes/PD-2026-047-atwater/05_stock/factory_selection.v001.json   # 選定理由と幕割り当て
episodes/PD-2026-047-atwater/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39〜EP46 との重複ゼロ（BLOCKING）

```bash
./.venv/Scripts/python.exe scripts/select_atwater_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` 〜 `episodes/PD-2026-046-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP47 の92本の積集合が**空**であることを確認。1件でも exit 1。**EP39〜EP46 のファイルは読むだけ。書き込み・移動・削除は一切しない。**

**分離レーン（色・素材・語）:** EP41 gold #E5B53A（監獄）／EP42 blue #3B7DD8（ankle monitor）／EP43 amber #E0913C（porch/救急車/レッカー）／EP44 teal #2FA6A0（病院）／EP45 crimson #B23A48（暖色台所/督促）／EP46 green #3F8F5F。**EP47 = civil-violet #7A5CD0（INK #0A0A0C）。** これら他話の絵柄・色・被写体を1本も選ばない。

---

# 8. A-5: i2v モーション化 16本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする16本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）

種画像は §5 と同じ `generate_sdxl_4k.py --variants 1` で `M<NN>_src.png` として生成（`ai_prompts.v001.md` に §8.1a の16行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `ATWA-MS01..MS16`、モーション成果物は `ATWA-M01..M16`。

| # | asset_id | 種画像 | 動きの意味 | act |
|---|---|---|---|---|
| 1 | ATWA-M01 | M01_src | 外れたシートベルトのバックルがゆっくり揺れる | 0 |
| 2 | ATWA-M02 | M02_src | 二車線道・背後からパトカーの灯が近づく | 0 |
| 3 | ATWA-M03 | M03_src | ダッシュボード上の開いた手錠・光が移ろう | 1 |
| 4 | ATWA-M04 | M04_src | 車内の空のチャイルドシート2つへの緩いプッシュ | 1 |
| 5 | ATWA-M05 | M05_src | 警察署の扉が閉じる寸前 | 1 |
| 6 | ATWA-M06 | M06_src | booking の壁時計・秒針が動く（約1時間） | 1 |
| 7 | ATWA-M07 | M07_src | 天秤（罰金票↔手錠）・手錠側が沈む | 2 |
| 8 | ATWA-M08 | M08_src | 第4修正の条文ページ・violet の光が横切る | 2 |
| 9 | ATWA-M09 | M09_src | 裁判所の長い廊下への緩い前進ドリー | 2 |
| 10 | ATWA-M10 | M10_src | 最高裁の列柱・冷たい光が動く | 3 |
| 11 | ATWA-M11 | M11_src | 5つの violet 光点が4つに対して立つ（5-4・可読数字なし） | 3 |
| 12 | ATWA-M12 | M12_src | 古い法律書の棚・ランプの埃が舞う | 3 |
| 13 | ATWA-M13 | M13_src | 大理石の刻字に影が mantle のように広がる | 3 |
| 14 | ATWA-M14 | M14_src | 開く扉と閉じた扉（救済は立法へ） | 5 |
| 15 | ATWA-M15 | M15_src | 二車線道が夕暮れへ移る | 5 |
| 16 | ATWA-M16 | M16_src | わずかに開いた扉・夕光への緩い pull-back（最終） | 5 |

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの16行を追加・各1枚）

```
- `M01_src.png`
A single unbuckled seatbelt buckle hanging loose in a worn pickup-truck cab in warm afternoon light, still and poised to swing, the small thing at the center of it, no people, no readable text [STYLE] Avoid: [NEG]
- `M02_src.png`
An empty two-lane Texas road in warm afternoon light with a faint patrol-car light glow rising in the far distance behind, still and poised, no people, no readable signage [STYLE] Avoid: [NEG]
- `M03_src.png`
A pair of open handcuffs resting on a pickup-truck dashboard in hard afternoon light, cold steel still and poised, the tool that answered a seatbelt, no people, no readable text [STYLE] Avoid: [NEG]
- `M04_src.png`
Two small empty child seats side by side in a pickup-truck cab in warm afternoon light, the children present only as empty seats, still and poised for a slow push, dignified, no people, no face, no readable text [STYLE] Avoid: [NEG]
- `M05_src.png`
A heavy small-town police-station intake door in a cold grey booking area caught just before it swings shut, no bars, no cell, framed and still, no people, no readable sign [STYLE] Avoid: [NEG]
- `M06_src.png`
A plain wall clock in a cold grey booking area with its second hand poised mid-sweep, framed for a slow hold of about an hour, no legible numerals, no people [STYLE] Avoid: [NEG]
- `M07_src.png`
A pair of plain balance scales weighing a small paper citation against a set of steel handcuffs in cold light, still and poised with the handcuffs pan about to sink, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `M08_src.png`
An old parchment page suggesting the Fourth Amendment under a warm lamp with the words abstract and unreadable and a single civil-violet band of light poised to cross it, still, no legible words, no people [STYLE] Avoid: [NEG]
- `M09_src.png`
A long courthouse corridor receding into cold institutional light with closed doors along it, framed for a slow forward move, no people, no readable signage [STYLE] Avoid: [NEG]
- `M10_src.png`
The pale marble colonnade of the United States Supreme Court at night lit from below, monumental and still, poised for a slow move, no people, no readable inscription [STYLE] Avoid: [NEG]
- `M11_src.png`
Five points of civil-violet light standing against four dimmer points on a dark marble field, a bare majority rendered as light, still and poised, no numerals, symbolic, no people, no text [STYLE] Avoid: [NEG]
- `M12_src.png`
A shelf of old leather-bound law volumes in warm lamplight with dust hanging in the beam, still and poised for a slow push, the spine titles abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `M13_src.png`
A cold marble surface bearing an engraved-looking band of light with a heavy fold of shadow poised to draw across it like a mantle, still and symbolic, no legible words, no people [STYLE] Avoid: [NEG]
- `M14_src.png`
An open door beginning to open onto a bar of warm daylight beside a firmly closed door in cold shadow, poised and still, the remedy left open and the constitutional door shut, no people, no readable sign [STYLE] Avoid: [NEG]
- `M15_src.png`
An empty two-lane Texas road under a deep civil-violet dusk sky turning slowly toward evening, still and open-ended, no people, no readable signage [STYLE] Avoid: [NEG]
- `M16_src.png`
A plain door left slightly ajar onto soft evening light, poised and still for a slow pull-back, the held final image, no people, no readable sign [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_kidsforcash.py` を下敷きにパスと SHOTS だけ差し替え）

```python
HOST = "http://127.0.0.1:8188"                              # ローカル ComfyUI
HIGH = "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors"
LOW  = "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors"
VAE  = "wan_2.1_vae.safetensors"       # ★2.1（2.2 ではない・無言の品質劣化の原因）
CLIP = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
WIDTH, HEIGHT = 1280, 720
FRAMES = 41        # 4090 の全ロード上限@720p
STEPS = 40 / SPLIT = 20 / SHIFT = 5.0   # ★SHIFT 5.0（8.0 は 5B からの無言持ち越しでバグ）
CFG = 3.5 / SAMPLER,SCHEDULER = "euler","simple" / FPS = 16
STILL_DIR     = H:\pd-media\assets\ai\atwater      # 種画像 M<NN>_src.png を読む
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\atwater
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, text, watermark, identifiable face, real person likeness, child, crying person, gore, blood"
```

**ゲート:** `dry_validate`（length=5 で1回POSTして配線エラーを安く検出）/ `assert_loaded_completely` / `assert_frame_math`。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す）

```bash
py -3.11 scripts/comfy_wan_atwater.py --build            # グラフだけ（GPU触らない）
py -3.11 scripts/comfy_wan_atwater.py --run --shot M01   # 1本本番して目視
py -3.11 scripts/comfy_wan_atwater.py --run-all          # 残り15本（冪等・既存スキップ）
```
1本 24–73 GPU分・16本で 7–19時間。`/queue` `/history` を30秒間隔でポーリング。

## 8.4 RIFE で 48fps 化（`rife_atwater.py`・`rife_kidsforcash.py` と同手順）

```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは length=5 検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番にリネーム → RIFE 2x を**2回**（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. **フレーム数検証** `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC

- 顔・身体・**子ども・泣く人**が生成されていないこと（NEG で抑えているが**必ず目視**・制約5）
- モーフィング/ちらつき/ワープが無いこと → あれば別シードで再生成
- M02/M15（道路）は**識別可能な人物・車のナンバー・読める標識**が写り込んでいないこと（制約2）
- M11（5-4 光点）は**可読の数字が出ていない**こと（制約4）
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（16本 × 2回 = 32カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど12本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **6本** | 大理石法廷の埃・書庫の塵。黒背景 drift を screen 合成 |
| `light_assets` | **4本** | 暖色午後光・冷たい fluorescent・大理石の光条・violet の差し |
| `vfx_overlays` | **2本** | 微細なグレイン・冷たい光ノイズ |
| **合計** | **12本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/atwater/overlay/` に置き、`atwater_film.json` の `cuts[].src` には**出さない**。黒背景でループするものを選び `blend_hint` を書く（§4.6 の12本に対応）。発色は B が accent `#7A5CD0`（civil-violet）に寄せる想定・A は他話色を選ばない。**§7.5 の目視QC対象**（12本）。

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --kind video --query dust_particles --limit 20 --exclude-used --ep PD-2026-047-atwater --json
```

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_atwater_assets.py`）

```
remotion/public/atwater/img/     ← role=body の静止画85枚（+ 同名 _depth.png）
remotion/public/atwater/factory/ ← 選定 factory .mp4 92本（§4.4 の F001..F092 名で）
remotion/public/atwater/motion/  ← i2v M<NN>_rife.mp4 16本
remotion/public/atwater/overlay/ ← 合成レイヤー 12本（§4.6 の P/L/V 名で）
```
- `public_path` はマニフェストの値（§4.4/§4.5/§4.6）と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する）:**
- factory の `public_path` は必ず `atwater/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も**含めない**
- 合成レイヤーは `atwater/overlay/` に置き `cuts[].src` に出さない

> **B のレンダは `--public-dir=public_slim`（Root.tsx に `id="Ep47Atwater"`）を使う想定だが、`public_slim` の構築は B の責務。** A は `remotion/public/atwater/` に正典を置くところまで。

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`

全静止画・i2v・factory・overlay を1行ずつ: `asset_id`/`path`/`source`（`ai_codex` or `factory`）/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力

```bash
./.venv/Scripts/python.exe scripts/build_atwater_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_atwater_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_atwater_asset_manifest.py --reuse-feasibility
```
この3つが exit 0 で「マニフェストが本番になった」。**★factory 92 / motion 16 が非空で実体化しているか（不変条件17/18）を必ず確認。** Bのファイルを直接書き換えて知らせようとしない。

---

# 11. 素材反復禁止ゲートの実仕様（`check_asset_reuse.py`）

```python
MAX_USES_FACTORY = 1
MAX_USES_MOTION  = 2
MAX_USES_STILL   = 2
MIN_FIRST_USE_SHARE = 0.70
```
種別判定は**パス文字列**（`kind_of()`）: `/factory` or `af-bg-` → factory / `.mp4|.mov|.webm` or `ai_video` or `_rife` → motion / それ以外 → still。§10.1 の命名規則を守る。

EP47 の設計値: still 101/85=1.19(≤2) / factory 92/92=1.0(≤1) / motion 32/16=2.0(≤2) / first-use 193/225=0.8578(≥0.70)。**全て達成可能。**

---

# 12. 絶対にやらないこと

- **EP39（frazier）〜EP46（tlo）のファイルに一切触らない。** 読み取りのみ可。素材・色・音のレーンも分離（§7.7）。EP47 の accent は **civil-violet #7A5CD0**（INK #0A0A0C・B が OP/AEカード/サムネで使用・A は絵で流用色を作らない）。
- **スレッドBの所有ファイル（§0.2）に触らない。** 特に `remotion/src/**` `scripts/ae/**` `scripts/build_atwater_film.py` `manifest.json` `04_scenes/shotlist*` `figures`。
  - **ただし `04_scenes/ai_prompts.v001.md` は A が書く**（§5.9/§8.1a）。B は読むだけ。
- **図解・トランジション・タイポの素材を探しに行かない。** 在庫が薄い/無いカテゴリは B が自作する。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。ローカル A1111・ComfyUI・RIFE は GPU を使うだけで課金なし。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness・身体をどこにも作らない**（§1・制約1/5）。特に **Gail Atwater・Officer Turek・判事を個人として描かない。通貨の肖像も描かない。**
- **6制約に反する文言・絵をプロンプト・タグ・注記・ファイル名のどこにも作らない**（§1.2/§1.3）:
  - 逮捕の「違法(illegal/unconstitutional/struck down)」化（制約1）／「どこでも禁止/完全禁止」化（制約1）／「Atwaterが勝った」（制約1）／票決の可読数字化（制約4）／逐語の可読描画（制約2/3）／子どもの扇情（泣く/怯える）（制約5）／可読の金額/日付/判例番号/ロゴ（制約2/6）。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。反復回避は distinct 85 で担保。
- **role=thumb / still_thumb を作らない・overlay を12本以外にしない。** サムネは also_thumb=true の body 6枚（§4.3 = {S01,S04,S13,S27,S30,S43}）。
- **★factory 92 / motion 16 の配列を空・stub のまま出荷しない**（EP45 の事故。§4.4/§4.5 を必ず実体化・public_path 非空）。
- **★dochighlight figure（黒バー/box/underline）を作らない・言及しない。** A の `tags`/`caption_hint`/`notes` にも `dochighlight` という文字列を書かない（grep で 0 を保つ）。
- **枚数・本数を「だいたい」で決めない。** §3 の確定値（still 85 / factory 92 / i2v 16 / distinct 193 / first-use 0.8578 / still-share 0.4489 / MG≥30 / 12.0分）と §3.3 の検算をそのまま使う。合わなければ実装ではなく**本書を疑って報告**。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** EP36は大聖堂を、EP38は牛を通した。**生成物・在庫クリップを実際に見る**（特に制約1/2/5は目視でしか守れない）。

---

# 13. 完了報告に含めるもの

```
1. accepted 静止画の枚数と内訳（body 85 / i2v_source 16 / also_thumb 6 [S01/S04/S13/S27/S30/S43] / reject N）
2. factory 選定 92本のリスト（asset_id / subtype / eyeballed_content）と、subtype と食い違って外した本数、道路/書面クリップの「no readable text / no logo / no face」確認
3. EP39〜EP46（八話）重複ゼロの確認結果
4. i2v 16本の frames / duration_sec と、SHORT? の有無
5. 合成レイヤー12本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code をそのまま貼る）＋ factory 92/motion 16 が非空で実体化した確認
7. §3.3 の検算 [1]〜[7] を自分で再計算した結果
8. asset_manifest.v001.json の counts ブロック（still_body 85 / still_i2v_source 16 / motion 16 / factory 92 / overlay 12）
9. 6制約・1枚前提の自己申告（逮捕の違法化なし/どこでも禁止化なし/Atwater勝訴化なし/票決可読数字なし/逐語可読描画なし/子ども扇情なし・バリエーション0・Atwater/Turek/判事 非人物化を目視確認・dochighlight 文字列ゼロ・A↔B同一スキーマ [schema atwater_assets.v1 / role enum body|i2v_source|reject / counts / also_thumb 集合 {S01,S04,S13,S27,S30,S43} / overlay 12]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
