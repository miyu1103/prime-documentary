# EP44 tekoh — Codex スレッドA「素材生成」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN）も実装スレッドB（CODEX_B）のファイルも**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> **唯一の外部真実 = `episodes/_planning/EP44_tekoh_PRODUCTION_SPEC.v001.json`**（機械生成）。本書の数値はそこから転記したものであり、手書きで発明していない。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP44 / Episode ID: PD-2026-044-tekoh / slug: tekoh
Composition id: Ep44Tekoh（B が Root.tsx に登録・A は staging まで）
事件:       Vega v. Tekoh (2022) 6-3。ミランダ違反“単体”を理由に §1983 で警官を民事で訴える道だけが否定された。
            ミランダ自体は存続。未告知供述は刑事公判で排除されうる。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**85本の固有プロンプト × 1枚 = 85枚**・バリエーション0） | `H:\pd-media\assets\ai\tekoh\S<NN>.png` | 2–3.5時間（GPU） |
| A-1b | i2v 種画像の生成（**16本の固有プロンプト × 1枚 = 16枚**・バリエーション0） | `H:\pd-media\assets\ai\tekoh\M<NN>_src.png` | 30–50分（GPU） |
| A-2 | 静止画のQCと目視（**目視必須**） | `05_visuals/still_qc.v001.json` + コンタクトシート | 1.5時間 |
| A-3 | depth map 生成（`treatment:"depth"` の必須入力） | `H:\pd-media\assets\ai\tekoh\S<NN>_depth.png` | 20分 |
| A-4 | factory 実写クリップ **93本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | **2.5時間（うち目視だけで1時間以上）** |
| A-5 | i2v モーション化 **16本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\tekoh\M<NN>_rife.mp4` | 7–19時間（GPU） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 | `05_stock/overlay_selection.v001.json` | 30分 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 20分 |
| A-8 | Remotion public への staging | `remotion/public/tekoh/{img,factory,motion,overlay}/` | 30分 |

> **★★ 最重要の前提（EP42/43 から継続）: 1シーン1枚・バリエーション0 ★★**
> Codex の画像生成は高精度。**同一ショットの複数バリエーション（`_02`/`_03`）を作らない。**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 85本＝85行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **`--variants 1`**（または variants 指定なし）で回す。**`--variants 3` は使わない。**
> **総生成画像 = still 85 + i2v 種 16 = 101枚（各1回）。** factory 93本は生成でなく在庫からの選抜。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-044-tekoh/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** Bはスタブで全パイプラインを完走できるので、Aの完了を待っていない。**A も急がなくてよいが途中経過を壊すな。** このマニフェストは **A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致**で共有する（§4）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\tekoh\**` / `H:\pd-media\assets\ai_video\tekoh\**` | **A** | 読み書き |
| `episodes/PD-2026-044-tekoh/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-044-tekoh/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/tekoh/{img,factory,motion,overlay}/**` | **A** | 読み書き |
| `episodes/PD-2026-044-tekoh/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_tekoh_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` `episodes/PD-2026-040-*/**` `episodes/PD-2026-041-*/**` `episodes/PD-2026-042-*/**` `episodes/PD-2026-043-*/**` および EP39/40/41/42/43 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を `read_prompts()` で読む） | `PD-2026-044-tekoh --variants 1` / `44 --variants 1 --only S01` |
| `scripts/gen_depth_maps.py`（**既存**） | §6.4 の depth map | `--dir "H:/pd-media/assets/ai/tekoh"` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-044-tekoh --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit 96 --exclude-used --ep PD-2026-044-tekoh --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-044-tekoh` |

**★Aが新規作成するスクリプト（EP43 の caniglia 版を tekoh 用に複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（複製元・EP43） |
|---|---|---|
| `scripts/qc_tekoh_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_caniglia_stills.py` |
| `scripts/select_tekoh_factory.py` | §7 の factory 93本の確定選定・EP39/40/41/42/43 sha256 除外検証 | `scripts/select_caniglia_factory.py` |
| `scripts/comfy_wan_tekoh.py` | §8 の i2v 16本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_caniglia.py` |
| `scripts/rife_tekoh.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_caniglia.py` |
| `scripts/build_tekoh_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_caniglia_asset_manifest.py` |
| `scripts/stage_tekoh_assets.py` | §10 の staging | `scripts/stage_caniglia_assets.py` |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある（`read_prompts()` で `04_scenes/ai_prompts.v001.md` を読む）。あなたは **`ai_prompts.v001.md` を §5.2 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない**（上の複製元が実在することを `ls scripts/` で確認してから複製する）。
> **正確性ゲートは `check_tekoh_facts.py`（B が実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の6制約に一致し、`check_tekoh_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_tekoh_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_tekoh_asset_manifest.py --reuse-feasibility
#   → still >=85 / motion >=16 / factory >=93 / distinct 合計 >=194 / first-use >=0.70

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_tekoh_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全93本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-044-tekoh
#   → exit 0（factory_clip_qc.v001.json が staging 済み全クリップを reviewed:true で網羅）

# [A-DONE-5] EP39/EP40/EP41/EP42/EP43 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_tekoh_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39・EP40・EP41・EP42・EP43 の五つすべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（R1 ＋ 正確性6制約）★★★

**Vega v. Tekoh は「警官がミランダ警告を与えなかったこと“単体”を理由に、その警官を §1983 の民事で訴えて金銭賠償を取れるか」だけを扱う。答えは 6-3 で「取れない」。しかしミランダ自体は存続し、未告知供述は刑事公判で排除されうる。本作の絵は「実在人物の顔・身体・肖像を一切出さない」。象徴オブジェのみ。原被疑事実（疑われた罪の性質）は描写も表示もしない。**

## 1.1 R1（生成ビジュアル全般）

1. **実在人物の顔・likeness・肖像を作らない。** Terence Tekoh（存命私人・R2）、Carlos Vega（存命私人・R2）、判事（Alito / Kagan / Breyer / Sotomayor / Roberts / Thomas / Gorsuch / Kavanaugh / Barrett）を**顔・身体・肖像として描かない**。人物は必ず後ろ姿・遠いシルエット・顔外し・手元のみ、原則「人を出さない」。
2. **実在の判決文・判例番号・条文・日付の可読文字を再現しない。** 書類・供述録取書・意見書・カレンダー・投票掲示板は雰囲気のみ（判読不能）。判例番号（No. 21-499 / 384 U.S. 436 (1966) / 42 U.S.C. § 1983）・日付・"6-3" は**画像に描かない**（AE/figures のタイポで出す＝B の担当）。
3. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性6制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **射程を過大化しない。** 否定されたのは「ミランダ違反“単体”を理由に §1983 で警官を民事で訴える」道だけ。ミランダ自体は刑事公判で有効（未告知供述は排除されうる）。**「Miranda is dead」「no right to remain silent」「police need not read rights / police no longer have to read rights / stop reading rights」を出力に一切書かない**（EP14 Lange型事故）。閉じたのは「賠償の第2の扉」だけ＝「排除の扉」は開いたまま、を象徴で必ず併存させる（閉じたドア＋開いたドア）。
2. **6-3（Alito法廷意見／Kagan反対＋Breyer・Sotomayor）。9-0でない。** `"9-0" "9 to 0" "unanimous"` を Vega の判決に対して書かない。多数/反対を中立帰属。
3. **Miranda(1966)/Dickerson(2000) と Vega を混同しない。** Vega はミランダを覆していない＝§1983救済のみ否定。**`"overturned Miranda" "Miranda overruled/reversed/struck down/killed"` を書かない。** Miranda/Dickerson は「存続する書物」として無傷で描く。
4. **§1983 の意味を正確に。** 州の役人を憲法違反で民事提訴する連邦法。「刑事免責」と混同しない。**§1983一般論で `"no immunity"` と断定しない**（qualified immunity がある）。§1983 は「責任を問うための扉」の象徴で示す。
5. **★広告適合性（最重要級）。** Tekoh の原被疑事実（疑われた罪の性質・その内容）を**描写も表示もしない**。タイトル/サムネ/カード/プロンプト/タグ/注記のどこにも罪状の性質・被害・"victim"・"guilty" を出さない。原告は「疑われ、無罪となった私人」として尊厳をもって（象徴：病院の廊下・机の上のペンと書面・署名欄・空の取調台・空の陪審席）。
6. **Tekoh も Vega も存命の私人（R2）。** 顔・肖像・身体を描かない。象徴のみ。個人として同定できる描写をしない。

## 1.3 機械ゲート（`build_tekoh_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
BANNED_PORTRAIT = re.compile(
    r"\bportrait\b|\bmugshot\b|likeness of|"
    r"face of (tekoh|terence|vega|carlos|alito|kagan|breyer|sotomayor|roberts|thomas|gorsuch|kavanaugh|barrett)|"
    r"recognizable (real )?person|identifiable face|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"miranda is dead|miranda (is )?(dead|abolished|overturned|overruled|gone|no longer|struck down)|"
    r"(overturn|overturned|overrule|overruled|reverse|reversed|struck down|kill|killed|end|ended) miranda|"
    r"no (more )?right to remain silent|right to remain silent (is )?(gone|dead|over|abolished)|"
    r"police (need not|no longer (need|have) to|do ?n.?t (need|have) to) (read|give|recite|warn)|"
    r"no (need|longer need) to read (you )?(your )?rights|stop reading (anyone )?(their )?rights|"
    r"\b9-0\b|9 to 0|nine to (zero|nothing)|\bunanimous\b|"
    r"no immunity|"
    r"sexual assault|sex crime|sex offen|\brape\b|molest|assault victim|\bthe victim\b|"
    r"guilty of|actually guilty|he did it|the crime he committed",
    re.IGNORECASE)
```

> `BANNED_ACCURACY` は制約1〜5を機械化したもの。プロンプト・タグ・`caption_hint`・注記のどこにも該当語を書かない。**"one door closed while the door of exclusion stays open"／"Miranda stands"／"a fence, not the ground" は許容（射程を正しく限定・制約1/3）。** 禁止は射程の過大化・9-0化・Miranda覆滅・§1983一般免責・原被疑事実の露出だけ。

---

# 2. 台本の語数と尺の確定値（SPEC から転記・Aが素材点数を積算する根拠）

**★唯一の真実 = `episodes/_planning/EP44_tekoh_PRODUCTION_SPEC.v001.json`。** 古い資料の wpm・語数は使うな。

```
words_total          = 2,139
narration_seconds    = 720.6   （= 12.0分・[SILENCE 1..6] の実音無音を含む）
wpm_used             = 178.1
総尺（設計）          = 720.6 + BrandOpening 3.50 + BrandEndcard 9.00 = 733.1秒 = 12:13  ≤ 750s
視覚シーン(narrative)  = 48（S01..S48・SPEC derive）
Act 構成（SPEC 秒）: HOOK 33.0 / OPENING 46.2 / ACT1 "That night" 77.5 / ACT2 "The turn" 150.9 /
                     ACT3 "The doctrine" 212.6 ＋ ACT3 payoff 74.8 / ENDING 111.2
```

**Aにとっての意味は1つ:** > **226カット / distinct 194 / 初出85.84% = still 85 + factory 93 + motion 16。**（§3 で積算）

> **注意（命名差）:** SPEC の視覚シーンは S01..S48。しかし **still は 85 本の固有プロンプトを持つ**ため、still の資産 ID は **S01..S85**（1プロンプト＝1枚）で採番する。48 の narrative シーンに 85 枚を配分する（ドクトリン核の ACT3 が最も厚い）。**still 資産 ID（S01..S85）と narrative シーンコード（S01..S48）は別物。** `covers_scene_id` は still 資産 ID 空間を指す（§7.3）。

---

# 3. ★素材構成の確定値（SPEC の distinct/cuts をそのまま調達する）

## 3.1 SPEC の内訳（★この値で調達する・勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **85枚** | 101カット | 1.19回(≤2) | **85本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **93本** | 93カット | **各1回(1)** | 在庫 11,000本超から選抜（§7）・全点目視・EP39/40/41/42/43 と sha256 被りゼロ |
| **i2v モーション** | **16本** | 32カット | 各2回(≤2) | 16本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **194点** | **226カット** | | |
| 合成レイヤー（particle/light/vfx） | 12本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |

**SDXL の生成バッチ（本編カットに出ない i2v 種を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **85枚** | 85プロンプト × 1枚（バリエーション0） |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **16枚** | 16種プロンプト × 1枚（バリエーション0） |
| **SDXL 生成バッチ合計** | **85 + 16 = 101枚（各1回）** | **`--variants 1`** |

> **サムネは新規生成しない。** 完成後に body 85枚から6枚を `also_thumb:true` で流用選抜（追加生成ゼロ＝1シーン1枚前提を崩さない）。**role=thumb / still_thumb を作らない。**

> **★紙芝居回避（EP40 の最大の失敗）:** **still-cut 101 / (factory 93 + i2v 32)=video 125** で **still-share 44.69% ≤45%・motion coverage 55.31% ≥45%** を構造的に保証する（§3.3）。**stillを増やしてfactoryを削るな。factory 93 が still-share≤0.45 を守る下限。**

## 3.2 still 85枚・factory 93本・i2v 16本の幕別配分（目安）

| 区間 | narration秒 | still（S番号） | factory | i2v |
|---|---|---|---|---|
| HOOK | 33.0 | 4（S01–S04） | 6 | 2 |
| OPENING | 46.2 | 3（S05–S07） | 3 | 0 |
| ACT1 "That night" | 77.5 | 12（S08–S19） | 12 | 3 |
| ACT2 "The turn" | 150.9 | 16（S20–S35） | 16 | 3 |
| ACT3 "The doctrine"＋payoff | 287.4 | 30（S36–S65） | 24 | 5 |
| ENDING | 111.2 | 20（S66–S85） | 12 | 3 |
| 繋ぎ（covers_scene_id:null） | — | — | 20 | — |
| **合計** | **720.6** | **85** | **93** | **16** |

> ACT3 は他幕の約2倍の尺（ドクトリン核・最も遅く荘厳）なので still も最多の30枚。
> **★幕別の factory 内訳（この表・§7.2・CODEX_B）は非拘束の目安値**（合計 93 のみ確定・幕割当は柔軟）。ゲートは factory を各1回・合計 93 でしか見ない。**確定値は「合計 factory 93」だけ。**

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 226 = still 101 + factory 93 + i2v 32
[2] 平均ショット長 = narration 720.6 / 226 = 3.188秒/カット  ✓ (SPEC mean_shot 3.19・≤6.0)
[3] 静止画占有率(check_animation_mix) = 101/226 = 44.69%  ✓ ≤45%（SPEC still_share 0.4469）
[4] motion coverage = (93+32)/226 = 125/226 = 55.31%     ✓ ≥45%（SPEC 0.553）
[5] per-asset 上限: still 101/85=1.19(≤2) / factory 93/93=1.0(≤1) / motion 32/16=2.0(≤2)  ✓
[6] first-use share = 194/226 = 0.8584                   ✓ ≥0.70（SPEC 一致）
[7] factory 下限: video を 125 カット以上に保たないと still-share が 0.45 を超える。
    i2v 32 は固定なので factory は 93 を下回れない（93+32=125）。→ factory 93 は下限であり水増しではない。
```

> **[3] の余裕は 0.31% しかない。** still が85本を割ったら §6.3 の再生成で回復させ、**still-cut 101 を増やさない**（B側の shotlist が101で固定）。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-044-tekoh/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `tekoh_assets.v1`（固定文字列）
**生産者:** `scripts/build_tekoh_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致。** role enum は **`body | i2v_source | reject` のみ**（`thumb`/`still_thumb` を作らない）。サムネは `also_thumb:true` の body still **ちょうど6枚**。overlay は **ちょうど12本**。

## 4.1 スキーマ（EP43 の `caniglia_assets.v1` と同型。counts を EP44 値に）

```jsonc
{
  "schema_version": "tekoh_assets.v1",
  "episode_id": "PD-2026-044-tekoh",
  "slug": "tekoh",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_tekoh_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 85,          // ==85
    "still_i2v_source": 16,    // ==16
    "motion": 16,              // ==16
    "factory": 93,             // ==93
    "overlay": 12              // ==12（distinct 素材に数えない）
  },
  "stills": [{
    "asset_id": "TEKOH-S01",               // body: ^TEKOH-S\d{2}$（1..85） / i2v種: ^TEKOH-MS\d{2}$
    "scene_id": "S01",                     // still 資産 ID（§5.9 のプロンプト行に対応・S01..S85 空間）
    "role": "body",                        // body|i2v_source|reject（バリエーション概念なし＝各1枚）
    "also_thumb": false,                   // body から6枚だけ true（追加生成しない）
    "act": 0,                              // 0=HOOK/OPENING, 1=ACT1, 2=ACT2, 3=ACT3, 5=ENDING
    "path": "H:/pd-media/assets/ai/tekoh/S01.png",
    "depth_path": "H:/pd-media/assets/ai/tekoh/S01_depth.png",   // role=="body" は実在必須
    "public_path": "tekoh/img/S01.png",    // role=="body" のみ非null
    "width": 3840, "height": 2160,         // 長辺>=3840
    "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 42.7,
    "tags": ["hospital_corridor","pen","signature_line","symbolic","night"],
    "caption_hint": "a pen resting on a written page above a blank signature line",  // check_tekoh_facts 検査対象（制約1-6）
    "seed": 0, "model": "juggernautXL_ragnarokBy",
    "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
    "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
           "has_identifiable_face": false, "has_human_body": false, "notes": ""}
  }],
  "motion": [{
    "asset_id": "TEKOH-M01",               // ^TEKOH-M\d{2}$（1..16）
    "source_scene_id": "M01_src",
    "source_still": "H:/pd-media/assets/ai/tekoh/M01_src.png",   // role=="i2v_source" の画像
    "path": "H:/pd-media/assets/ai_video/tekoh/M01_rife.mp4",
    "public_path": "tekoh/motion/M01_rife.mp4",
    "act": 0, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
    "sha256": "<64hex>", "tags": ["pen","signature_line"],
    "qc": {"reviewed": true, "on_theme": true, "artifact_free": true,
           "has_identifiable_face": false, "notes": ""}
  }],
  "factory": [{
    "asset_id": "AF-BG-0731",              // 棚 assets/asset_manifest.v001.json の id をそのまま
    "path": "H:/pd-media/assets/factory/backgrounds/AF-BG-0731__...mp4",
    "public_path": "tekoh/factory/AF-BG-0731__...mp4",
    "type": "backgrounds", "subtype": "<label>",   // ★ラベル=検索語の記録。中身の保証ではない（§7.5）
    "kind": "video", "license": "Pexels License",  // ALLOWED_LICENSES のいずれか
    "sha256": "<64hex>", "act": 2, "covers_scene_id": "S24",  // §7.3 の割当のみ。繋ぎは null
    "duration_sec": 7.60, "width": 1920, "height": 1080, "mean_luma": 48.3,
    "eyeballed_content": "an empty jury box of twelve wooden seats in cold light, no people",  // ★必須（§7.5）
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
           "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""}
  }],
  "overlay": [{
    "asset_id": "AF-PART-0044", "path": "H:/.../particle_assets/...mp4",
    "public_path": "tekoh/overlay/...mp4", "type": "particle_assets", "subtype": "<label>",
    "license": "Pexels License", "sha256": "<64hex>", "blend_hint": "screen",
    "eyeballed_content": "slow dust motes drifting on black, loops cleanly",
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""}
  }]
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `schema_version=="tekoh_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 85 / i2v_source 16 / motion 16 / factory 93 / overlay 12）に**一致**
3. 全 `path`/`depth_path`/`public_path` がディスクに実在
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `depth_path` と `public_path` が非null かつ実在
7. `qc.has_readable_text==true` / `qc.has_identifiable_face==true` / `qc.has_human_body==true` のいずれかは `role=="reject"`
8. `role=="i2v_source"` は `role=="body"` と**同一 asset_id を共有しない**（distinct 分離。i2v_source は `TEKOH-MS\d{2}`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39・EP40・EP41・EP42・EP43 の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない（＝目視していない本が混じっていない）
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど6**、かつ **`scene_id` 集合が `{S02,S04,S24,S44,S45,S85}`（§4.3）と完全一致**（追加生成ではなく body からの流用。**この集合は CODEX_B §11 と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|reject のみ）
16. `overlay` 配列長が**ちょうど12**

`--reuse-feasibility` では §3.3 [5][6][7] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 85枚（S01..S85）= §5.9 の85プロンプトの生成物。各1枚。
2. i2v_source 16枚（MS01..MS16 / 種画像 M01_src..M16_src）= §8.1 の16種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. also_thumb : body のうち S02 / S04 / S24 / S44 / S45 / S85 の6枚に true（追加生成しない）
4. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

---

# 5. A-1: SDXL 静止画のバッチ生成（85本 × 1枚・バリエーション0）

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-044-tekoh/04_scenes/ai_prompts.v001.md   ← A が §5.2 の形式で書く
出力:  H:\pd-media\assets\ai\tekoh\S<NN>.png（+ remotion/public/tekoh/ に自動コピー）
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
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 44 --variants 1 --only S01
#   → ログ "episode=... shots=101 variants=1 ... -> 101 images" の shots が 101 であること

# 全101枚（body 85 + i2v種 16・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-044-tekoh --variants 1
#   → 生成 S01.png ... S85.png / M01_src.png ... M16_src.png（各1枚。_02/_03 は作らない）
```

> QC で落ちたシーンの再生成は `--only S37`（**同じプロンプトで別シードを1枚**）。既存の>=3840はスキップ・不足だけ埋まる。**バリエーションを増やして水増ししない。枚数を減らして基準を下げるのも禁止。**

## 5.4 共通スタイル `[STYLE]`（全プロンプト末尾に必ず全文連結）

```
, cinematic still, cold cinematic-documentary grade, deep teal-green and charcoal clinical interior with a single pool of warm tungsten desk-lamp light falling on paper, civic and court spaces in pale cold marble grey, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face
```

> **EP39/EP40/EP41/EP42/EP43 との分離:** `navy interrogation room`/`electric blue`（EP39）・`midday sunlight`/`suburban demolition`/`bleached daylight`（EP40）・`prison cell`/`cellblock`/`sodium prison corridor`/`steel death-row`（EP41）・`Chicago apartment`/`ankle monitor`/`body-worn camera vest`（EP42）・`porch-amber house`/`ambulance red lights`/`tow-truck`/`Rhode Island suburban house`（EP43）を**1語も含めない**。EP44 は 冷たいティール緑の病院の廊下（夜）＋暖色ランプ下のペンと署名欄＋淡い大理石の裁判所・空の陪審席・prophylactic の「守りの柵」＋閉じたドア/開いたドアの対比。

## 5.5 共通ネガティブ `[NEG]`（各 `Avoid:` の後に必ず全文付ける）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible paper, legible case citation, legible docket number, legible date, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, human body, patient in a hospital bed, gurney with a person, medical procedure, injury, wound, blood, gore, nude, bare skin, weapon, gun, handgun, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, prison cell, steel cellblock, sodium prison corridor, navy interrogation room, electric blue, midday suburban daylight, bleached sunlight, porch amber house, ambulance, tow truck, ankle monitor
```

> ネガティブにも **制約違反語（"Miranda is dead", "9-0", "no immunity", "overturned Miranda", 原被疑事実語 等）を書かない**（§1.3）。上のリストにも含めていない。**原被疑事実・被害・自傷・患者の身体を NEG で明示的に抑制**（制約5・非グラフィック）。病院は「無人の廊下・空の部屋」のみ、患者・処置・搬送を描かない。

## 5.6 バリエーション軸（★EP44 では無効）

`generate_sdxl_4k.py` の `--variants 1` は各 stem を**1枚だけ**生成する。**`_02`/`_03` を作らない。** 反復回避は「85本の固有プロンプト＝85の別被写体」で担保する。

## 5.7 メタJSON

`generate_sdxl_4k.py` は画像を書くが per-image メタJSONは書かない。**A は QC 時に `qc_tekoh_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.8 プロンプトの絶対ルール（85本すべてに適用）

- **顔なし・身体なし・裸体なし。** 人物は原則出さない。出す場合は遠いシルエット/後ろ姿/影/手元のみ（制約6・R1）。
- **可読文字なし。** 供述録取書・意見書・判例番号・カレンダー・投票掲示板は雰囲気のみ（判読不能）。日付・数値・"6-3" を描かない。
- **Tekoh も Vega も個人として描かない**（制約6）。象徴オブジェのみ（病院の廊下・ペンと書面・署名欄・空の取調台・空の陪審席・最高裁列柱・守りの柵・閉じた扉/開いた扉）。
- **原被疑事実を描かない**（制約5）: 疑われた罪の性質・被害・患者・処置・搬送・拘束された人を一切描かない。病院は無人の廊下と空室のみ。
- **射程を過大化しない**（制約1）: 閉じた扉（§1983賠償）と開いた扉（刑事公判の排除）を象徴で必ず併存させる。「ミランダ廃止・黙秘権消滅」に見える絵を作らない。
- **6-3＝分かれた判断**（制約2）: 全会一致に見せない。分割は「一列の席が影の線で大小に分かれる」象徴で（数字は描かない・カードはBの担当）。
- **Miranda/Dickerson 非混同**（制約3）: 両者は「無傷で立つ書物」。Vega が覆したように見せない。
- **§1983＝民事救済の扉**（制約4）: 「責任を問う扉」の象徴で。免責を断定する絵を作らない。

## 5.9 確定プロンプト（★`ai_prompts.v001.md` にこの85エントリをそのまま書く・各1枚）

> 各行の `[STYLE]` は §5.4 を、`Avoid:` の後の `[NEG]` は §5.5 を**全文展開**して書く（下記は簡潔表記のマクロ。省略記号ではなく定義済み定数）。全て顔なし・身体なし・象徴・判読不能・原被疑事実なし。

```
- `S01.png`
An empty hospital corridor at night rendered in cold teal-green clinical light, a long polished floor receding into shadow, quiet and deserted, the ordinary place a private night began, no people, no readable signage [STYLE] Avoid: [NEG]
- `S02.png`
A single fountain pen resting on a written page under a warm low desk lamp on a plain table in a dim room, the page filled with abstract unreadable handwriting, the quiet center of everything, no legible text, no people, no hand [STYLE] Avoid: [NEG]
- `S03.png`
An extreme close view of a blank signature line at the bottom of a written page under a warm lamp, the line waiting to be signed, abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S04.png`
An empty interrogation table in a bare room lit by cold pale light, a single sheet of paper and a pen set at its center, no audio recorder present, the room where a warning never came, no people, no readable text [STYLE] Avoid: [NEG]
- `S05.png`
A single thin blade of warm light lying across a signature on a dark page, the whole promise reduced to one line, the characters abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S06.png`
The pale marble facade and tall columns of a supreme high court at night, cold stone lit from below, monumental and distant, the far place a hospital-table signature was carried to, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S07.png`
A written page on a plain table in warm lamp light in the foreground with the cold marble colonnade of a high court faint and distant beyond it, the span from a signature to the highest court, no legible text, no people [STYLE] Avoid: [NEG]
- `S08.png`
A hospital identification lanyard hanging from a hook beside a locker in cold teal light, an ordinary worker's badge with an abstract unreadable card, an anonymous hospital employee implied by objects, no face, no name, no legible text [STYLE] Avoid: [NEG]
- `S09.png`
A long hospital corridor at night with faint blurred motion far down its length, an ordinary place people pass and forget, cold clinical light, deliberately anonymous, no identifiable people, no readable signage [STYLE] Avoid: [NEG]
- `S10.png`
An empty chair pulled up to a plain table in a quiet hospital back room at the end of a long shift, a jacket over the chair back, someone about to sit down implied only by objects, no body, no face [STYLE] Avoid: [NEG]
- `S11.png`
A bare questioning room with a plain table and two facing chairs in cold pale light, one chair slightly turned, tension held in an empty room, no people, no readable text [STYLE] Avoid: [NEG]
- `S12.png`
A single blank sheet of paper and a pen set precisely at the center of a plain table under cold light, the paper that would come out of the room, quiet and waiting, no legible text, no people [STYLE] Avoid: [NEG]
- `S13.png`
A page half filled with abstract unreadable handwriting resting under a warm lamp on a plain table, a written statement in a private hand, the marks illegible, no legible words, no people, no visible hand [STYLE] Avoid: [NEG]
- `S14.png`
A plain table holding only a page and a pen with a conspicuously empty spot where a recorder would sit, the thing missing from the room, cold light, no people, no readable text [STYLE] Avoid: [NEG]
- `S15.png`
A pen poised just above a blank signature line on a written page under a warm lamp, no warning card anywhere in the frame, the instant before a signature, abstract and unreadable, no legible words, no people, no hand [STYLE] Avoid: [NEG]
- `S16.png`
A closed plain door of a small room seen from inside with a thin line of warm hallway light beneath it, the ordinary room a conversation happened in, quiet, no people, no readable number [STYLE] Avoid: [NEG]
- `S17.png`
A finished written page lying on a plain table with a pen resting across it, the statement complete, the handwriting abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S18.png`
A slow-push composition on a pen resting across a finished written page under a warm lamp, the room utterly still, the aftermath of a signature, abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S19.png`
The same bare questioning room afterward in cold pale light, the page and pen left on the empty table, the room after everything, no people, no readable text [STYLE] Avoid: [NEG]
- `S20.png`
A written page sealed inside a clear evidence sleeve being carried out of a room, a private statement about to travel to court, cold light, no legible text, no face, no visible body [STYLE] Avoid: [NEG]
- `S21.png`
The empty interior of a courtroom at night, a vacant bench and witness stand in cold pale wood and marble light, solemn and deserted, the place a page was carried to, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S22.png`
A document stamped as evidence lying on a plain courtroom table under cold light, the stamp abstract and unreadable, an ordinary page reclassified into the government's case, no legible text, no people [STYLE] Avoid: [NEG]
- `S23.png`
A single written page lying alone in a hard shaft of courtroom light, a private hand turned into evidence, the marks illegible, quiet and cold, no legible words, no people [STYLE] Avoid: [NEG]
- `S24.png`
An empty jury box of twelve vacant wooden seats aligned in a courtroom under cold light, warm wood against pale marble, twelve strangers rendered as empty chairs, no people, no text [STYLE] Avoid: [NEG]
- `S25.png`
The same empty jury box held in a still frame, twelve vacant seats in cold light, a held silence before a verdict, no people, no text [STYLE] Avoid: [NEG]
- `S26.png`
An open courtroom door with pale daylight beyond it and an empty gallery, the way out after a verdict, quiet and unremarkable, the man cleared implied only by absence, no people, no readable sign [STYLE] Avoid: [NEG]
- `S27.png`
An empty defendant's table and single chair in a deserted courtroom, papers cleared away, the trial over and the seat vacated, cold light, no people, no readable text [STYLE] Avoid: [NEG]
- `S28.png`
A single written page lying in a hard cold shaft of light on a courtroom table, a private statement used against its author, the object turned into a weapon rendered plainly and without drama, no legible words, no people [STYLE] Avoid: [NEG]
- `S29.png`
The closed doors of a civil courthouse seen frontally in cold stone light, the entrance to a different kind of case, monumental and shut, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S30.png`
A pair of empty scales beside a plain folded form on a dark desk under cold light, a claim measured not in prison but in money, the form's text abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S31.png`
An old leather-bound federal statute volume closed on a dark desk under a warm lamp, its spine worn and its title abstract and unreadable, a law with deep roots known only by a number, no legible text, no people [STYLE] Avoid: [NEG]
- `S32.png`
A single plain doorway set into a cold marble wall, standing slightly open onto warm light, a door built to hold an official to account, symbolic and severe, no people, no readable text [STYLE] Avoid: [NEG]
- `S33.png`
A courtroom bench and jury box seen twice in a doubled reflection under cold light, two trials rendered as one repeated empty room, no people, no text [STYLE] Avoid: [NEG]
- `S34.png`
A folded court verdict set aside under a desk lamp with its printed lines reduced to abstract illegible marks, a first result thrown out over a flaw, a plain object, no legible text, no people [STYLE] Avoid: [NEG]
- `S35.png`
The cold stone facade of a federal court of appeals building lit at night, tall and institutional, the appellate court that reached further before the case went up, no people, no readable sign [STYLE] Avoid: [NEG]
- `S36.png`
The tall columns and pale marble facade of a supreme high court seen frontally at night, monumental and solemn, the case carried up to be decided, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S37.png`
An extreme close view of a single small keyhole in a cold marble surface, one narrow almost technical question rendered as one tiny opening, symbolic and abstract, no people, no text [STYLE] Avoid: [NEG]
- `S38.png`
An old law volume standing upright and intact on a marble shelf under cold light, the famous 1966 case rendered as a book that still stands, its title abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S39.png`
A courtroom lectern and an empty counsel chair in cold marble light with a faint suggestion of the familiar warnings implied by absence, the case everyone already knows, no people, no readable text [STYLE] Avoid: [NEG]
- `S40.png`
A second, quieter law volume standing beside the first on a marble shelf, the ruling from the year 2000, intact and undisturbed, its title abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S41.png`
A single deep foundation stone beneath a marble building revealed in cold light, a rule rooted so deeply it cannot be swept away, monumental and abstract, no people, no text [STYLE] Avoid: [NEG]
- `S42.png`
Three plain objects arranged in a row on a marble surface like a simple equation, a rule then a break then a remedy, an argument that sounds almost like arithmetic, abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S43.png`
A hard single line of shadow splitting a cold marble floor into two unequal sides, an argument that looked simple meeting a court that did not, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S44.png`
A long judicial bench with nine tall vacant seats aligned behind it in cold marble light, a hard band of shadow dividing them into a larger group and a smaller group, a split court rendered as empty chairs, no people, no numbers, no text [STYLE] Avoid: [NEG]
- `S45.png`
A low protective fence or railing standing in a ring around a small raised marble pedestal in cold light, a safeguard built around something deeper, the guard rendered as a fence, no people, no text [STYLE] Avoid: [NEG]
- `S46.png`
A close view of a protective fence casting its shadow across the cold marble ground it encloses, the fence and the ground it protects held clearly apart, symbolic and abstract, no people, no text [STYLE] Avoid: [NEG]
- `S47.png`
A single band of engraved-looking light running across a cold marble wall, the deeper guarantee it stands for rendered only as light, the characters abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S48.png`
A protective gate in a low fence left unlatched and slightly ajar in cold light, a safeguard that is not itself the thing it guards, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S49.png`
A single plain door in a cold marble wall standing firmly shut, outlined by a thin cold line of light, the one door the ruling closed, quiet and severe, no people, no readable number [STYLE] Avoid: [NEG]
- `S50.png`
A pair of empty scales tipped and holding nothing on a marble desk under cold light, a claim for money left unpaid, an accounting that came to zero, abstract, no people, no text [STYLE] Avoid: [NEG]
- `S51.png`
A single written page being lifted and set aside away from a courtroom table in cold light, a statement kept from the case, the marks abstract and unreadable, no legible words, no people, no visible hand [STYLE] Avoid: [NEG]
- `S52.png`
Two doorways in a long marble wall, one glowing warm and standing open while the other stands cold and shut, the protection kept open beside the one that closed, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S53.png`
A single door caught mid-swing closing while a second door beside it stays deliberately open onto warm light, only the second door shut, the exact line of the ruling, no people, no readable text [STYLE] Avoid: [NEG]
- `S54.png`
A long empty judicial bench in a marble chamber with a shaft of cold colonnade light moving slowly across it, monumental and deserted, a held silence, no people, no text [STYLE] Avoid: [NEG]
- `S55.png`
A single empty chair drawn up to a plain hospital-style table in cold teal light, your own chair in that room, quiet and waiting, deliberately anonymous, no people, no readable text [STYLE] Avoid: [NEG]
- `S56.png`
An empty jury box of twelve vacant seats with an open exit door and pale daylight beyond it, a person cleared and free to go, cold light, no people, no text [STYLE] Avoid: [NEG]
- `S57.png`
A closed civil-courthouse door at the end of a cold corridor with an unpaid folded bill resting on the step before it, a check that cannot be collected, the form's text abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S58.png`
An empty price tag hanging by a thread from a safeguard rail in cold light, a protection people assumed carried a price, the tag blank and unreadable, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S59.png`
Three separate short stacks of pages set slightly apart from a thick closed folder on a dark marble bench, three writing separately in dissent, cold light, no legible text, no people [STYLE] Avoid: [NEG]
- `S60.png`
The quieter law volume from the year 2000 reopened under a warm lamp, its pages abstract and unreadable, the ruling a dissent returned to, no legible words, no people [STYLE] Avoid: [NEG]
- `S61.png`
A single sheet held under warm light with a faint shape of a right printed on it and an empty enforcement slot behind it, a right with no remedy standing behind it, abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S62.png`
A page bearing an abstract emblem of a guarantee set beside an empty locked bracket in cold light, a right that slowly stops feeling like a right without a remedy, symbolic, no legible words, no people [STYLE] Avoid: [NEG]
- `S63.png`
A folded promise on paper resting beside a broken latch under one lamp, a guarantee handed over with no way to enforce it, the text abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S64.png`
A faint person-shaped absence standing before a closed civil-courthouse door with nothing in its outstretched hands, someone left with nothing to collect and no one to answer, deliberately anonymous, no face, no visible body detail [STYLE] Avoid: [NEG]
- `S65.png`
The marble colonnade of a high court at night with a single cold shaft of light lingering along the stone, a dissent's warning left hanging in the air, monumental and still, no people, no text [STYLE] Avoid: [NEG]
- `S66.png`
An empty chair beside a plain hospital-style table under a single warm light, one ordinary life under all of the doctrine, quiet and anonymous, no people, no readable text [STYLE] Avoid: [NEG]
- `S67.png`
An empty jury box with an open door and pale daylight beyond, a jury that heard the whole case and let a man go, cold light softening to warm, no people, no text [STYLE] Avoid: [NEG]
- `S68.png`
A written page inside a folder resting on a courtroom table in cold light, a private statement once carried into a courtroom, the marks abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S69.png`
A single heavy closed door set into a cold institutional wall at the end of a bare corridor, the confinement a written page was used to argue for, no bars, no people, no readable text [STYLE] Avoid: [NEG]
- `S70.png`
A closed plain door at the end of a long cold corridor with a faint line of warm light beneath it, the civil courts a man turned to next, quiet and severe, no people, no readable number [STYLE] Avoid: [NEG]
- `S71.png`
The marble colonnade of a supreme high court at night, the final word given, cold stone lit from below, monumental and distant, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S72.png`
A single narrow path of cold light leading across marble to a firmly shut door, one particular road closed off at its end, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S73.png`
A single signature alone on a written page under one warm lamp, the whole story reduced to one line on paper, abstract and unreadable, a held silence, no legible words, no people [STYLE] Avoid: [NEG]
- `S74.png`
A single plain door standing firmly shut in cold light with a thin cold outline around its edge, a narrow question answered plainly, quiet and final, no people, no readable text [STYLE] Avoid: [NEG]
- `S75.png`
A bare interrogation-style table in cold teal light with a single page held back at its edge, an unwarned statement kept out of the room where it would decide a fate, no legible words, no people [STYLE] Avoid: [NEG]
- `S76.png`
An empty jury box with a single written page withheld just outside it under cold light, the warning still shaping what a jury is ever allowed to hear, the marks abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S77.png`
A written page on one side of a cold marble threshold and an empty pair of scales on the other, a right and a remedy held plainly apart as two different things, abstract, no legible words, no people [STYLE] Avoid: [NEG]
- `S78.png`
An abstract shield of cold light raised inside a marble courtroom, the protection the law still lifts for you inside a trial, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S79.png`
An open empty hand of light above an unpaid folded bill on a cold step, the payment a person had to win for himself and could not, abstract and unreadable, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S80.png`
A low protective fence held firmly around a raised marble ground, the first of two things you can still hold onto, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S81.png`
A blank flat wall where a doorway was expected in cold light, a remedy that was never there to take, quiet and severe, symbolic and abstract, no people, no readable text [STYLE] Avoid: [NEG]
- `S82.png`
A single fountain pen resting on a blank page under a warm lamp, a line drawn in plain words before the day it is needed, abstract and unreadable, no legible words, no people, no hand [STYLE] Avoid: [NEG]
- `S83.png`
The empty hospital corridor at night receding into cold teal shadow, quiet and settled, the ordinary place the story began now at rest, no people, no readable signage [STYLE] Avoid: [NEG]
- `S84.png`
A single lit window turning from the last deep blue of night toward grey dawn over a quiet city skyline, one warm room among many, open-ended and calm, no people, no visible address [STYLE] Avoid: [NEG]
- `S85.png`
A plain closed door with a thin line of cold light around its edge in a slow pull-back composition, the held final image, quiet and unresolved, the door at the end of everything, no people, no readable number [STYLE] Avoid: [NEG]
```

**枚数チェック:** 上記 85 エントリ（S01..S85）。§5.3 の `--only S01` ログで `shots=101`（body 85 + i2v種 16）を確認してから本番を回す。

---

# 6. A-2/A-3: 静止画のQC・目視・depth map

## 6.1 機械QC（body 85 + i2v種 16 = 全101枚・`qc_tekoh_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `35.0<=mean_luma<=225.0`（EP44は夜・冷たいティール病院＋暗い法廷が多い→黒潰れ側が本命リスク。`check_visual_asset_qc.DARK_LUMA_FLOOR=45.0` を下回りすぎる本に注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject（`check_visual_asset_qc.NEARDUP_SIM=0.90`）。**バリエーション0なので本来ほぼ衝突しないはず。衝突したらプロンプトが被っている**（特に多数ある「病院の廊下」「大理石の扉」「空の陪審席」「守りの柵」系に注意） | 片方 reject＋プロンプト見直し |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・判例番号・日付・"6-3"・ロゴが写っていないか（R1・制約2） | `has_readable_text=true`→reject |
| Q6 | 顔の混入 | **目視。** 識別可能な顔が写っていないか（R1・制約6） | `has_identifiable_face=true`→reject |
| Q7 | 身体/原被疑事実の混入 | **目視。** 人体・裸体・患者・処置・搬送・拘束された人・原被疑事実を示唆する物が写っていないか（制約5/6） | `has_human_body=true`→reject |

**Q5/Q6/Q7 は機械で判定しない。** コンタクトシートを出して**全101枚を実際に目視**する:

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-044-tekoh --media image
#   → runs/qc/tekoh_footage_contact_NN.png（20枚/シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-43 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** SDXL は平気で読める文字・顔・身体を描く。**特に制約5（原被疑事実の非描写・患者や身体を出さない）・制約6（Tekoh/Vega 非人物化）は目視でしか守れない。** S09（病院の廊下）は識別可能な人物・患者・処置が写っていないこと、S13/S51/S68 の書面は読める文字が写っていないこと、S44 の分割ベンチは数字が写っていないことを必ず目で確認する。

## 6.2 出力

```
episodes/PD-2026-044-tekoh/05_visuals/still_qc.v001.json     # 101枚全部の行（reject も残す・sha256/phash/mean_luma/long_edge）
（build_footage_contact_sheet が runs/qc に出す）
```

## 6.3 accepted が101枚に届かなかったとき

```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 44 --variants 1 --only S37   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_tekoh_stills.py
```
accepted body >= 85 かつ i2v_source >= 16 になるまで繰り返す。**基準を下げない・バリエーションを足して水増ししない。**

## 6.4 depth map（★新規スクリプトを作らず既存を使う）

```bash
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir "H:/pd-media/assets/ai/tekoh"
```
- モデル `Intel/dpt-large`。出力 `<stem>_depth.png`（同サイズ L グレースケール）。冪等。
- **role が `body` の静止画は depth 必須**（`treatment:"depth"` が隣に `_depth.png` を要求。無いとレンダーがクラッシュ）。i2v 種（`M<NN>_src.png`）は depth 不要。
- staging 後に `remotion/public/tekoh/img/` 側でも同名ペアが揃っていること（§10）。

---

# 7. A-4: factory 実写クリップ 93本の選定と全点目視QC

## 7.1 在庫の実態

```
H:\pd-media\assets\factory\   フラット構成
  backgrounds/     11,000本超（.mp4）  ← ★主力（病院の廊下/外観・冷たい大理石の裁判所・空の陪審席/法廷・空の廊下・列柱・夜〜夜明けの街・繋ぎ）
  light_assets/    …            合成レイヤー（冷たいティール臨床光・暖色ランプ・列柱の光条）
  particle_assets/ …            合成レイヤー（大理石法廷の埃・記録庫の塵）
  vfx_overlays/    …            合成レイヤー（グレイン・光ノイズ）
  texture_assets/  …            紙・石・大理石のテクスチャ
  loops/           …            抽象的な繋ぎ
ファイル名規約: AF-<TYPECODE>-<4桁>__<subtype_slug>.<ext>（TYPECODE = BG|LIGHT|LOOP|PART|TEX|VFX）
棚レジストリ: C:\Users\aab15\Documents\prime-documentary\assets\asset_manifest.v001.json
   （トップキーは schema と assets。★必ず encoding="utf-8" で開く。cp932 既定だと落ちる）
```

## 7.2 選定条件

- **`kind=="video"` のみ。** 静止画 factory は使わない
- **93本ちょうど**（§3.3[7] より 93 は still-share≤0.45 を守る下限。減らせない）
- **各1回しか使わない**（`check_asset_reuse.MAX_USES_FACTORY=1`）
- 幕別割り当て（§3.2）: HOOK=6 / OPENING=3 / ACT1=12 / ACT2=16 / ACT3=24 / ED=12 ＋ 繋ぎ=20 ＝ 93
- **EP39（夜/取調室/青）・EP40（郊外/昼/破壊）・EP41（監獄/鉄/石の独房）・EP42（シカゴのアパート/足首モニタ）・EP43（RI の一軒家/porch-amber/救急車/レッカー）の絵柄を選ばない。** EP44 は 冷たいティール緑の病院の廊下（夜・無人）＋淡い大理石の裁判所・空の陪審席・空の法廷・列柱＋夜〜夜明けの街。**患者・処置・搬送・救急車・拘束された人を含むクリップを選ばない（制約5）。**

**既存の選定ツールで候補出し（新規に検索ロジックを書くな）:**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes   # テーマ一覧と件数
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query courthouse --limit 96 --exclude-used --ep PD-2026-044-tekoh --json
```
`--exclude-used` は `check_arc_nonrepeat.build_universe()` と同じ指紋集合を使うので出荷ゲート `arc_nonrepeat` と食い違わない。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・SDXLで作らない情景）

> **★`covers_scene_id` は still 資産 ID 空間（S01..S85・§2 注記）を指す。narrative シーン（DESIGN の S01..S48）とは別体系。** B はこの値を still 資産 ID として解決し、narrative シーンコードにクロスマップしない。

| covers | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S01 | 無人の病院の廊下（夜） | `hospital_corridor_night` / `empty_hospital_hallway` | 1 |
| S06 | 最高裁/大法廷ファサード・列柱 | `supreme_court_building` / `marble_columns` | 0 |
| S09 | 病院の廊下（無人・遠い動き） | `hospital_hallway` / `hospital_interior_night` | 1 |
| S21 | 無人の法廷内観 | `empty_courtroom` / `courtroom_interior` | 2 |
| S24 | 空の陪審席 | `empty_jury_box` / `jury_box` | 2 |
| S29 | 民事裁判所の入口/外観 | `courthouse_exterior` / `courthouse_entrance_night` | 2 |
| S35 | 連邦控訴審の建物ファサード | `federal_courthouse` / `court_building_facade` | 2 |
| S36 | 最高裁の列柱（正面） | `supreme_court_columns` / `courthouse_columns_night` | 3 |
| S54 | 無人の大理石法廷・列柱の光 | `marble_chamber` / `courtroom_bench_empty` | 3 |
| S71 | 最高裁の列柱（夜） | `supreme_court_night` / `marble_facade_night` | 5 |
| S83 | 夜の病院の廊下（受け・無人） | `hospital_corridor` / `clinical_hallway_night` | 5 |

**残り本数は covers を持たない繋ぎ・情景クリップ**（`covers_scene_id:null`）: 冷たい大理石の廊下・空の法廷/陪審席・列柱の光条・無人の病院の廊下と外観・夜〜夜明けの街・雨のアスファルト・冷たい窓・抽象 `loops`。**暗いクリップに偏りすぎない**（§7.5 の暗側閾値・全体の1/3=約31本まで。列柱の光・臨床光・夜明け側を優先）。

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）

```python
ALLOWED_LICENSES = {"cc0","royalty_free","generated_owned","Pexels License","Pixabay Content License"}
```

## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★

> **推測ではなく実際に起きた事故。** EP36: `city_surveillance_camera_dome` が大聖堂。EP38: 牛が `documents_on_desk`。`subtype` は「その検索語で取った」記録であって**中身の保証ではない**。

**選抜93本は例外なく次を経る:**

```bash
# 1) 選定した93本を staging フォルダに集め、ラベル付きコンタクトシートを出す
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py \
    --ep PD-2026-044-tekoh --media video --dir "<93本の staging フォルダ>"
#   → runs/qc/tekoh_footage_contact_NN.png（各タイルにファイル名ラベル）
```

2. **コンタクトシートを実際に開き、93本すべてを1本ずつ見る**
3. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて**選定から外す**
4. 実写シネマティックB-roll（アニメ/CG臭排除）・EP44テーマ（無人の病院の廊下/淡い大理石の裁判所/空の陪審席/列柱/夜〜夜明けの街）・ウォーターマークなし・識別可能な実在人物なし（制約6・R1）を確認
5. **★制約5の目視:** 病院系クリップ（S01/S09/S83 系）は **`eyeballed_content` に「an empty corridor, no patients, no people, no medical procedure」を必ず明記**。患者・処置・搬送・拘束された人・原被疑事実を示唆する要素が写るクリップは使わない。**判事席に実在の顔が写るニュース映像を使わない（制約6）。**
6. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=45.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。
> **EP44 は夜・冷たいティール病院＋暗い法廷が多いので暗側が本命リスク。** 平均輝度45未満のクリップが全体の40%を超えると FAIL。**暗いクリップは約31本（1/3）までに抑え、列柱の光・臨床光・夜明けの実用光がある本を優先する。**

**1フレームで判断がつかない本は VLC/ffplay で再生して確認**（near-still は `check_animation_mix` を落とす）。

## 7.6 出力

```
episodes/PD-2026-044-tekoh/05_stock/factory_selection.v001.json   # 選定理由と幕割り当て
episodes/PD-2026-044-tekoh/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39/EP40/EP41/EP42/EP43 との重複ゼロ（BLOCKING）

```bash
./.venv/Scripts/python.exe scripts/select_tekoh_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` `episodes/PD-2026-040-*/` `episodes/PD-2026-041-*/` `episodes/PD-2026-042-*/` `episodes/PD-2026-043-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP44 の93本の積集合が**空**であることを確認。1件でも exit 1 で差し替え。**EP39/EP40/EP41/EP42/EP43 のファイルは読むだけ。書き込み・移動・削除は一切しない。**

---

# 8. A-5: i2v モーション化 16本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする16本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）

種画像は §5 と同じ `generate_sdxl_4k.py --variants 1` で `M<NN>_src.png` として生成する（`ai_prompts.v001.md` に下記16行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `TEKOH-MS01..MS16`、モーション成果物の asset_id は `TEKOH-M01..M16`。

| # | asset_id | 種画像 | 動きの意味 | act |
|---|---|---|---|---|
| 1 | TEKOH-M01 | M01_src | ペンが署名欄の上で構えられ、ランプの光が微かに揺れる | 0 |
| 2 | TEKOH-M02 | M02_src | 無人の取調台への緩いプッシュイン | 0 |
| 3 | TEKOH-M03 | M03_src | ランプ下の手書きの供述録取ページへの緩いプッシュ | 1 |
| 4 | TEKOH-M04 | M04_src | 夜の病院の廊下・遠くに微かな動き | 1 |
| 5 | TEKOH-M05 | M05_src | ペンが横たわる完成した供述書への緩いプッシュ | 1 |
| 6 | TEKOH-M06 | M06_src | 空の陪審席・冷たい光が移ろう | 2 |
| 7 | TEKOH-M07 | M07_src | 証拠スタンプの押された書面に法廷の光 | 2 |
| 8 | TEKOH-M08 | M08_src | 光の帯の中で武器のように置かれた1枚の書面 | 2 |
| 9 | TEKOH-M09 | M09_src | 最高裁の列柱・冷たい光が動く | 3 |
| 10 | TEKOH-M10 | M10_src | 守りの柵がそれが囲む地面に影を落とす・光が移ろう | 3 |
| 11 | TEKOH-M11 | M11_src | 大理石の壁を一条の光が横切る（深い権利の核） | 3 |
| 12 | TEKOH-M12 | M12_src | 1つの扉が閉じる一方、隣の扉は開いたまま | 3 |
| 13 | TEKOH-M13 | M13_src | 無人の大理石法廷を列柱の光がゆっくり横切る | 3 |
| 14 | TEKOH-M14 | M14_src | 1枚の署名だけが残る書面への緩いプッシュ | 5 |
| 15 | TEKOH-M15 | M15_src | 冷たい廊下の奥で閉じた民事裁判所の扉 | 5 |
| 16 | TEKOH-M16 | M16_src | 窓の外の最後の青が夜明けへ移る | 5 |

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの16行を追加・各1枚）

```
- `M01_src.png`
A fountain pen poised just above a blank signature line on a written page under a warm low lamp, the room still, framed before any motion, the marks abstract and unreadable, no legible words, no people, no hand [STYLE] Avoid: [NEG]
- `M02_src.png`
A bare interrogation table in cold pale light with a single page and a pen at its center and no recorder present, framed for a slow push-in, quiet and unremarkable, no people, no readable text [STYLE] Avoid: [NEG]
- `M03_src.png`
A page half filled with abstract unreadable handwriting resting under a warm lamp, a written statement poised and still, no legible words, no people, no visible hand [STYLE] Avoid: [NEG]
- `M04_src.png`
An empty hospital corridor at night in cold teal-green clinical light with faint distant motion far down its length, deliberately anonymous, poised and still, no identifiable people, no readable signage [STYLE] Avoid: [NEG]
- `M05_src.png`
A finished written page on a plain table with a pen resting across it under a warm lamp, the statement complete and still, the marks abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `M06_src.png`
An empty jury box of twelve vacant wooden seats in a courtroom under cold light, warm wood against pale marble, still and waiting, no people, no text [STYLE] Avoid: [NEG]
- `M07_src.png`
A document stamped as evidence lying on a plain courtroom table in a cold shaft of light, the stamp abstract and unreadable, still and poised, no legible words, no people [STYLE] Avoid: [NEG]
- `M08_src.png`
A single written page lying in a hard cold shaft of courtroom light, a private statement used against its author, the marks abstract and unreadable, still, no legible words, no people [STYLE] Avoid: [NEG]
- `M09_src.png`
The pale marble colonnade of a supreme high court at night lit from below, monumental and still, poised for a slow move, no people, no readable inscription [STYLE] Avoid: [NEG]
- `M10_src.png`
A low protective fence casting its shadow across the cold marble ground it encloses, the fence and the ground held clearly apart, still and poised, symbolic, no people, no text [STYLE] Avoid: [NEG]
- `M11_src.png`
A single thin band of pale light lying across a cold marble wall, abstract and unreadable, the deeper guarantee rendered as light, no legible words, no people [STYLE] Avoid: [NEG]
- `M12_src.png`
A single plain door caught just before closing while a second door beside it stays open onto warm light, poised in cold marble light, no people, no readable text [STYLE] Avoid: [NEG]
- `M13_src.png`
The interior of a grand empty marble high-court chamber with a shaft of cold colonnade light resting across a long vacant bench, monumental and still, no people, no text [STYLE] Avoid: [NEG]
- `M14_src.png`
A single signature alone on a written page under a warm lamp, the whole story reduced to one line, abstract and unreadable, still and held, no legible words, no people [STYLE] Avoid: [NEG]
- `M15_src.png`
A closed civil-courthouse door at the end of a long cold corridor with a faint line of warm light beneath it, quiet and severe, poised and still, no people, no readable number [STYLE] Avoid: [NEG]
- `M16_src.png`
A single lit window with the last deep blue of night turning to grey dawn over a quiet city skyline, one warm room, still and open-ended, no people, no visible address [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_caniglia.py` を下敷きにパスと SHOTS だけ差し替え）

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
STILL_DIR     = H:\pd-media\assets\ai\tekoh          # 種画像 M<NN>_src.png を読む
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\tekoh
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, text, watermark, identifiable face, real person likeness, patient, medical procedure, gore, blood, self-harm"
```

**ゲート:** `dry_validate`（length=5 で1回POSTして配線エラーを安く検出）/ `assert_loaded_completely`（部分ロード検出）/ `assert_frame_math`（フレーム計算）。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す）

```bash
py -3.11 scripts/comfy_wan_tekoh.py --build            # グラフだけ（GPU触らない）
py -3.11 scripts/comfy_wan_tekoh.py --run --shot M01   # 1本本番して目視
py -3.11 scripts/comfy_wan_tekoh.py --run-all          # 残り15本（冪等・既存スキップ）
```
1本 24–73 GPU分・16本で 7–19時間。`/queue` `/history` を30秒間隔でポーリング。

## 8.4 RIFE で 48fps 化（`rife_tekoh.py`・`rife_caniglia.py` と同手順）

```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは length=5 検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番にリネーム → RIFE 2x を**2回**（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. **フレーム数検証** `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC

- 顔・身体・患者・原被疑事実が生成されていないこと（NEG で抑えているが**必ず目視**・制約5/6）
- モーフィング/ちらつき/ワープが無いこと → あれば別シードで再生成
- M04（病院の廊下）は**識別可能な人物・患者・処置が写り込んでいない**こと（制約5）
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（16本 × 2回 = 32カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど12本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **6本** | 大理石法廷の埃・記録庫の塵。黒背景 drift を screen 合成 |
| `light_assets` | **4本** | 冷たいティール臨床光・暖色ランプ・列柱の光条・冷たい大理石の光 |
| `vfx_overlays` | **2本** | 微細なグレイン・冷たい光ノイズ |
| **合計** | **12本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/tekoh/overlay/` に置き、`tekoh_film.json` の `cuts[].src` には**出さない**（出すと factory 判定で1回制限を食う）。同じレイヤーを何度重ねてもよい（素材ではなく加工）。黒背景でループするものを選び `blend_hint` を書く。**§7.5 の目視QC対象**（12本・12分）。**合成レイヤーの発色は B が accent `#2FA6A0` に寄せる想定・A は色被りの素材を作らない（他話の gold/blue/amber を選ばない）。**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --kind video --query dust_particles --limit 20 --exclude-used --ep PD-2026-044-tekoh --json
```

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_tekoh_assets.py`）

```
remotion/public/tekoh/img/     ← role=body の静止画85枚（+ 同名 _depth.png）
remotion/public/tekoh/factory/ ← 選定 factory .mp4 93本
remotion/public/tekoh/motion/  ← i2v M<NN>_rife.mp4 16本
remotion/public/tekoh/overlay/ ← 合成レイヤー 12本
```
- `public_path` はマニフェストの値と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー（`import_to_remotion.py` の `conform_video(...,fps=30)` と同じ）
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する・外すと誤分類）:**
- factory の `public_path` は必ず `tekoh/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も**含めない**
- 合成レイヤーは `tekoh/overlay/` に置き `cuts[].src` に出さない

> **B のレンダは `--public-dir=public_slim`（Root.tsx に `id="Ep44Tekoh"`）を使う想定だが、`public_slim` の構築は B の責務。** A は `remotion/public/tekoh/` に正典を置くところまで（B が slim を派生させる）。

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`

全静止画・i2v・factory・overlay を1行ずつ: `asset_id`/`path`/`source`（`ai_codex` or `factory`）/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力

```bash
./.venv/Scripts/python.exe scripts/build_tekoh_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_tekoh_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_tekoh_asset_manifest.py --reuse-feasibility
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

EP44 の設計値: still 101/85=1.19(≤2) / factory 93/93=1.0(≤1) / motion 32/16=2.0(≤2) / first-use 194/226=0.8584(≥0.70)。**全て達成可能。**

---

# 12. 絶対にやらないこと

- **EP39（frazier）/EP40（lech）/EP41（thompson）/EP42（young）/EP43（caniglia）のファイルに一切触らない。** 読み取りのみ可。素材・色（EP41 gold #E5B53A / EP42 blue #3B7DD8 / EP43 amber #E0913C）・音のレーンも分離。EP44 の accent は **interrogation-teal #2FA6A0**（INK #0A0A0C・B が OP/AEカード/サムネで使用・A は絵で流用色を作らない）。
- **スレッドBの所有ファイル（§0.2）に触らない。** 特に `remotion/src/**` `scripts/ae/**` `scripts/build_tekoh_film.py` `manifest.json` `04_scenes/shotlist*` `figures`。
  - **ただし `04_scenes/ai_prompts.v001.md` は A が書く**（`generate_sdxl_4k.py` の入力・§5.9/§8.1a）。B は読むだけ。
- **図解・トランジション・タイポの素材を探しに行かない。** 在庫が薄い/無いカテゴリは B が自作する。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。ローカル A1111・ComfyUI・RIFE は GPU を使うだけで課金なし（オーナー許可済み）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness・身体をどこにも作らない**（§1・制約6）。特に **Tekoh も Vega も個人として描かない**。
- **6制約に反する文言・絵をプロンプト・タグ・注記・ファイル名のどこにも作らない**（§1.2/§1.3）:
  - 「Miranda is dead / 黙秘権消滅 / 警察は権利を読まなくてよい」断定（制約1）／「9-0・全会一致」（制約2）／「Vega が Miranda を覆した」（制約3）／§1983一般で「no immunity」断定（制約4）／原被疑事実・被害・患者・処置の描写や表示（制約5）。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。反復回避は distinct 85 で担保（§0.1・§5.6）。
- **role=thumb / still_thumb を作らない・overlay を12本以外にしない。** サムネは also_thumb=true の body 6枚（§4.3 = {S02,S04,S24,S44,S45,S85}）。
- **枚数・本数を「だいたい」で決めない。** §3 の確定値（still 85 / factory 93 / i2v 16 / distinct 194 / first-use 0.8584 / still-share 0.4469 / MG≥31 / 12.0分）と §3.3 の検算をそのまま使う。合わなければ実装ではなく**本書を疑って報告**。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** EP36は大聖堂を、EP38は牛を通した。**生成物・在庫クリップを実際に見る**（特に制約5/6は目視でしか守れない・病院クリップの患者写り込み・判事の顔写り込みも目視で排除）。

---

# 13. 完了報告に含めるもの

```
1. accepted 静止画の枚数と内訳（body 85 / i2v_source 16 / also_thumb 6 [S02/S04/S24/S44/S45/S85] / reject N）
2. factory 選定 93本のリスト（asset_id / subtype / eyeballed_content）と、subtype と食い違って外した本数、病院クリップの「no patients, no people」確認
3. EP39/EP40/EP41/EP42/EP43 重複ゼロの確認結果
4. i2v 16本の frames / duration_sec と、SHORT? の有無
5. 合成レイヤー12本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code をそのまま貼る）
7. §3.3 の検算 [1]〜[7] を自分で再計算した結果
8. asset_manifest.v001.json の counts ブロック（still_body 85 / still_i2v_source 16 / motion 16 / factory 93 / overlay 12）
9. 6制約・1枚前提の自己申告（Miranda廃止断定/9-0化/Vega が Miranda 覆滅/§1983一般 no immunity/原被疑事実描写 が全出力に皆無・バリエーション0・Tekoh/Vega 非人物化を目視確認・A↔B同一スキーマ [schema tekoh_assets.v1 / role enum body|i2v_source|reject / counts / also_thumb 集合 {S02,S04,S24,S44,S45,S85} / overlay 12]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
