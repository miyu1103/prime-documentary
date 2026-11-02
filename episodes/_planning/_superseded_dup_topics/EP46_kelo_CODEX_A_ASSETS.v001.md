# EP46 kelo — Codex スレッドA「素材生成」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN）も実装スレッドB（CODEX_B）のファイルも**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> **唯一の外部真実 = `episodes/_planning/EP46_kelo_PRODUCTION_SPEC.v001.json`**（機械生成）。本書の数値はそこから転記したものであり、手書きで発明していない。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP46 / Episode ID: PD-2026-046-kelo / slug: kelo
Composition id: Ep46Kelo（B が Root.tsx に登録・A は staging まで）
事件:       Kelo v. City of New London, 545 U.S. 469 (2005)（Susette Kelo・New London, CT）。
            経済開発型の私的転売を伴う収用を、最高裁が 5-4 で UPHELD（合憲と判断）。
            収用は「違法」ではない。憤りの源は「合法とされたこと」＝規範的批判＋後日談。
            Kelo は存命の私人（R2・有罪歴なし）。顔・肖像・身体を描かない。象徴のみ。
            ピンクの家は取壊しでなく解体移築（36 Franklin St）＝「her house was demolished」と書かない。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**85本の固有プロンプト × 1枚 = 85枚**・バリエーション0） | `H:\pd-media\assets\ai\kelo\S<NN>.png` | 2–3.5時間（GPU） |
| A-1b | i2v 種画像の生成（**16本の固有プロンプト × 1枚 = 16枚**・バリエーション0） | `H:\pd-media\assets\ai\kelo\M<NN>_src.png` | 30–50分（GPU） |
| A-2 | 静止画のQCと目視（**目視必須**） | `05_visuals/still_qc.v001.json` + コンタクトシート | 1.5時間 |
| A-3 | depth map 生成（`treatment:"depth"` の必須入力） | `H:\pd-media\assets\ai\kelo\S<NN>_depth.png` | 20分 |
| A-4 | factory 実写クリップ **92本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | **2.5時間（うち目視だけで1時間以上）** |
| A-5 | i2v モーション化 **16本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\kelo\M<NN>_rife.mp4` | 7–19時間（GPU） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 | `05_stock/overlay_selection.v001.json` | 30分 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 20分 |
| A-8 | Remotion public への staging | `remotion/public/kelo/{img,factory,motion,overlay}/` | 30分 |

> **★★ 最重要の前提（EP42〜EP45 から継続）: 1シーン1枚・バリエーション0 ★★**
> Codex の画像生成は高精度。**同一ショットの複数バリエーション（`_02`/`_03`）を作らない。**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 85本＝85行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **`--variants 1`**（または variants 指定なし）で回す。**`--variants 3` は使わない。**
> **総生成画像 = still 85 + i2v 種 16 = 101枚（各1回）。** factory 92本は生成でなく在庫からの選抜。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-046-kelo/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** Bはスタブで全パイプラインを完走できるので、Aの完了を待っていない。**A も急がなくてよいが途中経過を壊すな。** このマニフェストは **A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致**で共有する（§4）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\kelo\**` / `H:\pd-media\assets\ai_video\kelo\**` | **A** | 読み書き |
| `episodes/PD-2026-046-kelo/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-046-kelo/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/kelo/{img,factory,motion,overlay}/**` | **A** | 読み書き |
| `episodes/PD-2026-046-kelo/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_kelo_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-045-*/**` および EP39〜45 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を `read_prompts()` で読む） | `PD-2026-046-kelo --variants 1` / `46 --variants 1 --only S01` |
| `scripts/gen_depth_maps.py`（**既存**） | §6.4 の depth map | `--dir "H:/pd-media/assets/ai/kelo"` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-046-kelo --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit 96 --exclude-used --ep PD-2026-046-kelo --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-046-kelo` |

**★Aが新規作成するスクリプト（EP45 の cleveland 版を kelo 用に複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（複製元・EP45／既存） |
|---|---|---|
| `scripts/qc_kelo_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_cleveland_stills.py` |
| `scripts/select_kelo_factory.py` | §7 の factory 92本の確定選定・EP39〜45 sha256 除外検証 | `scripts/select_cleveland_factory.py` |
| `scripts/comfy_wan_kelo.py` | §8 の i2v 16本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_kidsforcash.py`（最新の実在Wan A14Bドライバ） |
| `scripts/rife_kelo.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_kidsforcash.py`（実在） |
| `scripts/build_kelo_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_cleveland_asset_manifest.py` |
| `scripts/stage_kelo_assets.py` | §10 の staging | `scripts/stage_cleveland_assets.py` |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある（`read_prompts()` で `04_scenes/ai_prompts.v001.md` を読む）。あなたは **`ai_prompts.v001.md` を §5.2 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない**（上の複製元が実在することを `ls scripts/` で確認してから複製する）。
> **正確性ゲートは `check_kelo_facts.py`（B が実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の6制約に一致し、`check_kelo_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_kelo_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_kelo_asset_manifest.py --reuse-feasibility
#   → still >=85 / motion >=16 / factory >=92 / distinct 合計 >=193 / first-use >=0.70

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_kelo_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全92本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-046-kelo
#   → exit 0（factory_clip_qc.v001.json が staging 済み全クリップを reviewed:true で網羅）

# [A-DONE-5] EP39/EP40/EP41/EP42/EP43/EP44/EP45 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_kelo_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39・EP40・EP41・EP42・EP43・EP44・EP45 の七つすべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（R1 ＋ 正確性6制約）★★★

**経済開発型の私的転売を伴う収用は、Kelo v. City of New London(2005)で最高裁が 5-4 で UPHELD（合憲）した。本作は収用を「違法／違憲」だとは決して言わない。多数意見は Fifth Amendment の "public use" を "public purpose" と広く解し、雇用・税収を約束する経済開発を該当としたが、「政府はどんな理由でも家を奪える」とは言っていない。Kennedy 第5票は pretextual/trivial/implausible な便益偽装収用を依然禁止と留保した。O'Connor 反対（Motel 6 / Ritz-Carlton の逐語）と Thomas 別個反対は**反対意見**であって Court の判断ではない。Susette Kelo は存命の私人（R2・有罪歴なし）で、顔・身体・肖像を一切出さない。象徴オブジェのみ。ピンクの家は取壊しでなく解体移築（36 Franklin St）＝「her pink house was demolished」と書かない（近隣宅は取壊し）。困窮・立退きを扇情化しない（poverty porn 禁止）。**

## 1.1 R1（生成ビジュアル全般）

1. **実在人物の顔・likeness・肖像を作らない。** Susette Kelo（存命私人・R2）、Justice Stevens / Kennedy / O'Connor / Thomas / Scalia / Rehnquist / Souter / Ginsburg / Breyer を**顔・身体・肖像として描かない**。人物は原則「人を出さない」（象徴オブジェのみ）。判事の逐語引用は AE カード（B の担当）であって画像ではない。
2. **実在の判決文・判例番号・条文・日付・金額の可読文字を再現しない。** 収用通知（condemnation notice）・免許・deed・設計図・意見書・州法令集・カレンダーは雰囲気のみ（判読不能）。判例番号（545 U.S. 469 / No. 04-108）・日付（June 23, 2005 / 2009 / 2011）・金額（$300 million）・数値（90 acres / ~115 properties / "more than 40 states" / 1,000+ jobs）は**画像に描かない**（AE/figures のタイポで出す＝B の担当）。会社ロゴ（Pfizer 等）・ブランド名（Motel 6 / Ritz-Carlton）は**ぼかして判読不能**にする（対比は形状・グレードで示す）。
3. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性6制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **収用を「違法／違憲（illegal / unconstitutional / struck down）」と書かない。** 最高裁は 5-4 で UPHELD（合憲と判断）。憤りの源は「合法とされたこと」＝規範的批判＋後日談。許容枠は "the Court said the city COULD do this" / "the taking stands" / "upheld" / "the ruling let it happen"。**「the Supreme Court struck it down」「ruled the taking unconstitutional」を書かない。**
2. **ドクトリンを正確に。** 多数意見は "public use" を "public purpose" と広く解し、経済開発（雇用・税収）を該当としたが、**「政府はどんな理由でも家を奪える（government can take any home for any reason）」と過大化しない。** 許容は "economic development can count as a public purpose" / "a genuine, deliberate plan"。
3. **Kennedy 第5票の nuance を落とさない。** pretextual / trivial / implausible な便益偽装収用は依然禁止、疑わしい事案には厳格審査の余地。**「the Court gave government unlimited power」に単純化しない。**
4. **O'Connor / Thomas は反対意見。** 逐語（"any Motel 6 with a Ritz-Carlton, any home with a shopping mall, or any farm with a factory" 等・"use by the public"）は**反対意見として中立帰属**する。**Court／多数意見に帰属させない（"the Court warned…" と書かない）。** 逐語は AE カード（B）＝画像には可読文字を焼かない。
5. **Susette Kelo は R2（存命私人・有罪歴なし）。** 顔・肖像・身体を描かない。象徴のみ（ピンクの家・水辺・空の通り・収用通知・解体重機・更地・雑草・企業の site plan と光る模型・Motel 6 と Ritz-Carlton の対比・州法令集・家をフラットベッドに載せて移築）。**捏造引用禁止。困窮・立退きを扇情化しない（poverty porn 禁止・泣く人・嘆く家族・子どもを描かない）。**
6. **ピンクの家は demolished でない・数値は台帳一致でヘッジ。** 近隣宅は取壊し（cleared/pulled down）だが**Kelo の家は解体して移築**。**「her pink house was demolished / destroyed / bulldozed」を書かない。** 後日談: Pfizer 約$3億拠点が触媒 → **2009離脱**、収用地は長年**更地**（2011ハリケーン後は瓦礫置場）、判決後 **"more than forty states"** が収用改革（正確数はソース差＝**">40州"表記で confidence:medium**・"45/47/all fifty states" と断定しない）。**画像には数値を描かない**（AE/figures＝B）。

## 1.3 機械ゲート（`build_kelo_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
BANNED_PORTRAIT = re.compile(
    r"\bportrait\b|\bmugshot\b|likeness of|"
    r"face of (susette|kelo|stevens|kennedy|o'?connor|thomas|scalia|rehnquist|souter|ginsburg|breyer)|"
    r"recognizable (real )?person|identifiable face|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"(taking|condemnation|seizure|ruling|decision) (was|is|were|are)\s*(illegal|unconstitutional)|"
    r"(supreme court|scotus|the court|majority) (struck (it |the taking )?down|ruled .{0,20}unconstitutional)|"
    r"struck down (the )?(taking|law|ruling)|"
    r"(government|city|state) can take (any|your|a) home for any reason|take any home for any reason|"
    r"unlimited power to (take|seize)|"
    r"the court warned|majority warned|"                # O'Connor/Thomas を Court に帰属させない
    r"(pink house|kelo'?s (pink )?house|her (pink )?house) (was|were|got)? ?(demolished|destroyed|torn down|bulldozed|razed)|"
    r"(forty-?five|forty-?seven|forty-?four|forty-?three|45|47|44|43|all fifty) states|"  # ">40 states" 以外の断定
    r"poverty ?porn|starving child|crying child|weeping family|evicted family crying",
    re.IGNORECASE)
```

> `BANNED_ACCURACY` は制約1〜6を機械化したもの。プロンプト・タグ・`caption_hint`・注記のどこにも該当語を書かない。**"upheld" / "the Court said the city could" / "the taking stands" / "a public purpose" / "the neighborhood was cleared" / "the pink house was moved / relocated" / "more than forty states" は許容（射程を正しく限定）。** 禁止は「違法／違憲」化・「どんな理由でも」化・「無制限の権力」・O'Connor/Thomas を Court に帰属・「ピンクの家が取壊された」・州数の断定・扇情（poverty porn）だけ。

---

# 2. 台本の語数と尺の確定値（SPEC から転記・Aが素材点数を積算する根拠）

**★唯一の真実 = `episodes/_planning/EP46_kelo_PRODUCTION_SPEC.v001.json`。** 古い資料の wpm・語数は使うな。

```
words_total          = 2,133
narration_seconds    = 718.6   （= 12.0分・[DESIGNED SILENCE 1..3] の実音無音を含む）
wpm_used             = 178.1
総尺（設計）          = 718.6 + BrandOpening 3.50 + BrandEndcard 9.00 = 731.1秒 = 12:11  ≤ 750s
                       （durationInFrames は hook+opening+narration+endcard の4項関数＝B の責務。
                        hookSeconds=8.0 基準で total≈752s まで許容。A はこの値を再計算しない）
視覚シーン(narrative)  = 48（S01..S48・SPEC derive）
Act 構成（SPEC 秒）: HOOK 56.6 / OPENING 48.8 / BODY 417.1（ACT1+ACT2+ACT3）/ ENDING 181.6
```

**Aにとっての意味は1つ:** > **225カット / distinct 193 / 初出85.78% = still 85 + factory 92 + motion 16。**（§3 で積算）

> **注意（命名差）:** SPEC の視覚シーンは S01..S48。しかし **still は 85 本の固有プロンプトを持つ**ため、still の資産 ID は **S01..S85**（1プロンプト＝1枚）で採番する。48 の narrative シーンに 85 枚を配分する（後日談の厚い ENDING と情緒核の ACT3 が最も厚い）。**still 資産 ID（S01..S85）と narrative シーンコード（S01..S48）は別物。** `covers_scene_id` は still 資産 ID 空間を指す（§7.3）。

---

# 3. ★素材構成の確定値（SPEC の distinct/cuts をそのまま調達する）

## 3.1 SPEC の内訳（★この値で調達する・勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **85枚** | 101カット | 1.19回(≤2) | **85本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **92本** | 92カット | **各1回(1)** | 在庫 11,000本超から選抜（§7）・全点目視・EP39〜45 と sha256 被りゼロ |
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
| HOOK | 56.6 | 5（S01–S05） | 6 | 2（M01,M02） |
| OPENING | 48.8 | 4（S06–S09） | 3 | 0 |
| ACT1 "The plan for the point" | ~130 | 17（S10–S26） | 12 | 3（M03,M04,M05） |
| ACT2 "What public use means" | ~150 | 19（S27–S45） | 16 | 3（M06,M07,M08） |
| ACT3 "The four who said no" | ~137 | 20（S46–S65） | 24 | 4（M09,M10,M11,M12） |
| ENDING | 181.6 | 20（S66–S85） | 12 | 4（M13,M14,M15,M16） |
| 繋ぎ（covers_scene_id:null） | — | — | 19 | — |
| **合計** | **718.6** | **85** | **92** | **16** |

> ACT3 は O'Connor/Thomas 反対の情緒核、ENDING は「Nothing built → 更地 → >40州改革 → 移築」の最長後日談なので still も最多（各20枚）。
> **★幕別の factory 内訳（この表・§7.2・CODEX_B）は非拘束の目安値**（合計 92 のみ確定・幕割当は柔軟）。ゲートは factory を各1回・合計 92 でしか見ない。**確定値は「合計 factory 92」だけ。**

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 225 = still 101 + factory 92 + i2v 32
[2] 平均ショット長 = narration 718.6 / 225 = 3.194秒/カット  ✓ (SPEC mean_shot 3.19・≤6.0)
[3] 静止画占有率(check_animation_mix) = 101/225 = 44.89%  ✓ ≤45%（SPEC still_share 0.4489）
[4] motion coverage = (92+32)/225 = 124/225 = 55.11%     ✓ ≥45%（SPEC 0.5511）
[5] per-asset 上限: still 101/85=1.19(≤2) / factory 92/92=1.0(≤1) / motion 32/16=2.0(≤2)  ✓
[6] first-use share = 193/225 = 0.8578                   ✓ ≥0.70（SPEC 一致）
[7] factory 下限: video を 124 カット以上に保たないと still-share が 0.45 を超える。
    i2v 32 は固定なので factory は 92 を下回れない（92+32=124）。→ factory 92 は下限であり水増しではない。
```

> **[3] の余裕は 0.11%（0.45 − 0.4489）しかない。EP45（0.36%）より更に薄い。** still が85本を割ったら §6.3 の再生成で回復させ、**still-cut 101 を増やさない**（B側の shotlist が101で固定）。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-046-kelo/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `kelo_assets.v1`（固定文字列）
**生産者:** `scripts/build_kelo_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致。** role enum は **`body | i2v_source | reject` のみ**（`thumb`/`still_thumb` を作らない）。サムネは `also_thumb:true` の body still **ちょうど6枚**。overlay は **ちょうど12本**。

## 4.1 スキーマ（EP45 の `cleveland_assets.v1` と同型。counts を EP46 値に）

```jsonc
{
  "schema_version": "kelo_assets.v1",
  "episode_id": "PD-2026-046-kelo",
  "slug": "kelo",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_kelo_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 85,          // ==85
    "still_i2v_source": 16,    // ==16
    "motion": 16,              // ==16
    "factory": 92,             // ==92
    "overlay": 12              // ==12（distinct 素材に数えない）
  },
  "stills": [{
    "asset_id": "KELO-S01",                // body: ^KELO-S\d{2}$（1..85） / i2v種: ^KELO-MS\d{2}$
    "scene_id": "S01",                     // still 資産 ID（§5.9 のプロンプト行に対応・S01..S85 空間）
    "role": "body",                        // body|i2v_source|reject（バリエーション概念なし＝各1枚）
    "also_thumb": false,                   // body から6枚だけ true（追加生成しない）
    "act": 0,                              // 0=HOOK/OPENING, 1=ACT1, 2=ACT2, 3=ACT3, 5=ENDING
    "path": "H:/pd-media/assets/ai/kelo/S01.png",
    "depth_path": "H:/pd-media/assets/ai/kelo/S01_depth.png",   // role=="body" は実在必須
    "public_path": "kelo/img/S01.png",     // role=="body" のみ非null
    "width": 3840, "height": 2160,         // 長辺>=3840
    "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 46.2,
    "tags": ["pink_house","point_of_land","water","symbolic","dusk"],
    "caption_hint": "a small pink clapboard house on a point of land where a river meets the sound",  // check_kelo_facts 検査対象（制約1-6）
    "seed": 0, "model": "juggernautXL_ragnarokBy",
    "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
    "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
           "has_identifiable_face": false, "has_human_body": false, "notes": ""}
  }],
  "motion": [{
    "asset_id": "KELO-M01",                // ^KELO-M\d{2}$（1..16）
    "source_scene_id": "M01_src",
    "source_still": "H:/pd-media/assets/ai/kelo/M01_src.png",   // role=="i2v_source" の画像
    "path": "H:/pd-media/assets/ai_video/kelo/M01_rife.mp4",
    "public_path": "kelo/motion/M01_rife.mp4",
    "act": 0, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
    "sha256": "<64hex>", "tags": ["pink_house","water"],
    "qc": {"reviewed": true, "on_theme": true, "artifact_free": true,
           "has_identifiable_face": false, "notes": ""}
  }],
  "factory": [{
    "asset_id": "AF-BG-0731",              // 棚 assets/asset_manifest.v001.json の id をそのまま
    "path": "H:/pd-media/assets/factory/backgrounds/AF-BG-0731__...mp4",
    "public_path": "kelo/factory/AF-BG-0731__...mp4",
    "type": "backgrounds", "subtype": "<label>",   // ★ラベル=検索語の記録。中身の保証ではない（§7.5）
    "kind": "video", "license": "Pexels License",  // ALLOWED_LICENSES のいずれか
    "sha256": "<64hex>", "act": 2, "covers_scene_id": "S28",  // §7.3 の割当のみ。繋ぎは null
    "duration_sec": 7.60, "width": 1920, "height": 1080, "mean_luma": 52.1,
    "eyeballed_content": "a public highway overpass at dusk, no people, no readable signage",  // ★必須（§7.5）
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
           "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""}
  }],
  "overlay": [{
    "asset_id": "AF-PART-0044", "path": "H:/.../particle_assets/...mp4",
    "public_path": "kelo/overlay/...mp4", "type": "particle_assets", "subtype": "<label>",
    "license": "Pexels License", "sha256": "<64hex>", "blend_hint": "screen",
    "eyeballed_content": "slow coastal mist drifting on black, loops cleanly",
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""}
  }]
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `schema_version=="kelo_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 85 / i2v_source 16 / motion 16 / factory 92 / overlay 12）に**一致**
3. 全 `path`/`depth_path`/`public_path` がディスクに実在
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `depth_path` と `public_path` が非null かつ実在
7. `qc.has_readable_text==true` / `qc.has_identifiable_face==true` / `qc.has_human_body==true` のいずれかは `role=="reject"`
8. `role=="i2v_source"` は `role=="body"` と**同一 asset_id を共有しない**（distinct 分離。i2v_source は `KELO-MS\d{2}`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39・EP40・EP41・EP42・EP43・EP44・EP45 の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない（＝目視していない本が混じっていない）
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど6**、かつ **`scene_id` 集合が `{S01,S02,S68,S75,S79,S83}`（§4.3）と完全一致**（追加生成ではなく body からの流用。**この集合は CODEX_B §11 と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|reject のみ）
16. `overlay` 配列長が**ちょうど12**

`--reuse-feasibility` では §3.3 [5][6][7] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 85枚（S01..S85）= §5.9 の85プロンプトの生成物。各1枚。
2. i2v_source 16枚（MS01..MS16 / 種画像 M01_src..M16_src）= §8.1 の16種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. also_thumb : body のうち S01 / S02 / S68 / S75 / S79 / S83 の6枚に true（追加生成しない）
     ＝ ピンクの家(S01) / 水辺(S02) / 更地=Nothing(S68) / 雑草の更地(S75) / フラットベッド移築(S79) / 州法令集(S83)
       ＝ 強い象徴（ピンクの家・水辺・更地・州法令集）から選抜（brief §7・R2 遵守で顔なし）
4. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

---

# 5. A-1: SDXL 静止画のバッチ生成（85本 × 1枚・バリエーション0）

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-046-kelo/04_scenes/ai_prompts.v001.md   ← A が §5.2 の形式で書く
出力:  H:\pd-media\assets\ai\kelo\S<NN>.png（+ remotion/public/kelo/ に自動コピー）
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
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 46 --variants 1 --only S01
#   → ログ "episode=... shots=101 variants=1 ... -> 101 images" の shots が 101 であること

# 全101枚（body 85 + i2v種 16・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-046-kelo --variants 1
#   → 生成 S01.png ... S85.png / M01_src.png ... M16_src.png（各1枚。_02/_03 は作らない）
```

> QC で落ちたシーンの再生成は `--only S37`（**同じプロンプトで別シードを1枚**）。既存の>=3840はスキップ・不足だけ埋まる。**バリエーションを増やして水増ししない。枚数を減らして基準を下げるのも禁止。**

## 5.4 共通スタイル `[STYLE]`（全プロンプト末尾に必ず全文連結）

```
, cinematic still, dark documentary grade, the soft seashell pink of a small clapboard house on a point of land where a tidal river meets the sound, warm amber porch light against a cool coastal dusk and wide grey water, cleared lots and quiet empty streets under a low even sky, a single deed-green accent as the one cool note, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face
```

> **EP39〜EP45 との分離:** `navy interrogation room`/`electric blue`（EP39）・`midday sunlight`/`suburban demolition`/`bleached daylight`（EP40）・`prison cell`/`cellblock`/`sodium prison corridor`/`steel death-row`（EP41）・`Chicago apartment`/`ankle monitor`/`body-worn camera vest`（EP42）・`ambulance red lights`/`tow-truck`/`welfare-check`（EP43）・`teal-green hospital corridor`/`clinical hospital`（EP44）・`worn Alabama kitchen table`/`overdue crimson`/`county-jail booking`/`suspended driver's license`（EP45）を**1語も含めない**。EP46 は 海辺のピンクの一軒家（point of land・river meets the sound）＋更地/空の通り/収用通知＋解体重機/雑草の更地＋企業の site plan と光る waterfront 模型＋Motel 6 と Ritz-Carlton の対比＋大理石の最高裁列柱＋家をフラットベッドに載せて移築＋州法令集の背。**accent は deed-green `#3F8F5F`（B が OP/AEカード/サムネで使用・A は EP41 gold/EP42 blue/EP43 amber/EP44 teal/EP45 crimson の発色を絵で作らない）。**

## 5.5 共通ネガティブ `[NEG]`（各 `Avoid:` の後に必ず全文付ける）

```
text, words, letters, numbers, captions, watermark, logo, brand name, readable document, legible notice, legible condemnation notice, legible case citation, legible statute, legible deed, legible date, legible dollar amount, legible street sign, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, human body, child, crying person, weeping family, evicted family, sensational distress, poverty porn, weapon, gun, blood, gore, nude, bare skin, cartoon, illustration, anime, 3d game render, low quality, blurry, jpeg artifacts, deformed, extra limbs, navy interrogation room, electric blue, prison cell, steel cellblock, barred cell, sodium prison corridor, ankle monitor, body-worn camera, ambulance, tow truck, red emergency lights, teal-green hospital corridor, clinical hospital, hospital bed, worn kitchen-table citation stack, overdue crimson accent, county-jail booking, suspended driver's license
```

> ネガティブにも **制約違反語（"the taking was unconstitutional", "struck down", "take any home for any reason", "her pink house demolished", "45 states", poverty porn 語 等）を書かない**（§1.3）。上のリストにも含めていない。**扇情・子ども・困窮の煽情描写・身体・可読の金額/日付/判例番号・会社/ブランドロゴを NEG で明示的に抑制**（制約2/5）。ロゴやブランド名が要る絵（Pfizer拠点・Motel 6・Ritz-Carlton・請求書）は「blurred into an unreadable smear」で判読不能にし、対比は**建物のグレード・形状**で示す。

## 5.6 バリエーション軸（★EP46 では無効）

`generate_sdxl_4k.py` の `--variants 1` は各 stem を**1枚だけ**生成する。**`_02`/`_03` を作らない。** 反復回避は「85本の固有プロンプト＝85の別被写体」で担保する。

## 5.7 メタJSON

`generate_sdxl_4k.py` は画像を書くが per-image メタJSONは書かない。**A は QC 時に `qc_kelo_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.8 プロンプトの絶対ルール（85本すべてに適用）

- **顔なし・身体なし・裸体なし。** 人物は原則出さない（制約5・R1）。Susette Kelo を個人として描かない。判事を描かない。
- **可読文字なし。** 収用通知・免許・deed・設計図・意見書・和解書・州法令集・カレンダーは雰囲気のみ（判読不能）。判例番号・日付・金額・数値・会社/ブランドロゴを描かない（ロゴはぼかす）。
- **象徴オブジェのみ:** ピンクの家（点在する更地に一軒だけ残る）・水辺（川と入江）・空の通り・ドアに貼る収用通知・解体重機/更地/雑草・企業の site plan と光る waterfront 模型・Motel 6 と Ritz-Carlton の対比・farm と factory の対比・home と shopping mall の対比・大理石の最高裁列柱・古い法律書/州法令集の背・家をフラットベッドに載せて移築。
- **扇情化しない**（制約5）: 泣く人・嘆く家族・立退きの困窮・子どもを描かない。尊厳をもって物と場所だけで示す。
- **「違法／違憲」化しない**（制約1）: 収用を「struck down / unconstitutional」に見える絵を作らない。多数が UPHELD した事実は、**立ったまま残る大理石の列柱・そのまま実行される収用**として象徴で持つ。
- **多数と反対を混同しない**（制約4）: O'Connor/Thomas の逐語モチーフ（Motel 6 vs Ritz-Carlton・home vs shopping mall・farm vs factory・"use by the public"）は**反対意見の警句**として象徴する（Court が言ったように見せない・可読引用を焼かない）。
- **ピンクの家は demolished でない**（制約6）: 近隣宅は取壊し（cleared/pulled down）だが**ピンクの家は解体して移築**（board by board / flatbed / relocated）。取壊される絵に**ピンクの家を含めない**。

## 5.9 確定プロンプト（★`ai_prompts.v001.md` にこの85エントリをそのまま書く・各1枚）

> 各行の `[STYLE]` は §5.4 を、`Avoid:` の後の `[NEG]` は §5.5 を**全文展開**して書く（下記は簡潔表記のマクロ。省略記号ではなく定義済み定数）。全て顔なし・身体なし・象徴・判読不能・扇情なし。

```
- `S01.png`
A small pink clapboard house standing at the end of a street on a point of land where a tidal river meets the sound, painted the soft pink of a seashell, warm amber porch light in the coastal dusk, quiet and dignified, no people, no readable sign [STYLE] Avoid: [NEG]
- `S02.png`
Wide grey coastal water seen through the windows of a modest waterfront house, a river opening into the sound under a low even sky, the view a home was bought for, no people, no readable text [STYLE] Avoid: [NEG]
- `S03.png`
An empty residential street where every other house is already gone, bare cleared lots and open foundations on either side, quiet and depopulated at dusk, no people, no readable signage [STYLE] Avoid: [NEG]
- `S04.png`
An idle wrecking crew's excavator parked on a cleared block at dusk, the machine waiting, bare graded earth around it, no people, no readable text [STYLE] Avoid: [NEG]
- `S05.png`
The small pink house left standing alone on an otherwise cleared street, one lit home surrounded by empty lots, the last holdout, warm amber against cool grey, no people, no readable sign [STYLE] Avoid: [NEG]
- `S06.png`
The pale marble colonnade of the United States Supreme Court at night, cold stone lit from below, monumental and distant, the court that would answer this in 2005, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S07.png`
An aged parchment of the Fifth Amendment rendered as a single framed document under warm light, its lines abstract and unreadable, four words about public use implied but never legible, no legible text, no people [STYLE] Avoid: [NEG]
- `S08.png`
A public highway and bridge at dusk, the ordinary kind of taking everyone agrees on, cold pavement carrying traffic light trails, a road built for public use, no people, no readable signage [STYLE] Avoid: [NEG]
- `S09.png`
The small pink house small in the near foreground on its point of land, the faint pale marble colonnade of the highest court distant beyond the water, the span from one home to the Supreme Court, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S10.png`
A shuttered brick factory with dark windows beside a fading New England waterfront, industry thinned and jobs gone, cold grey light, a city that had been losing for a long time, no people, no readable sign [STYLE] Avoid: [NEG]
- `S11.png`
A closed federal facility gate behind chain-link fencing at dusk, padlocked and still, the nearby installation that had shut its doors, no people, no readable signage [STYLE] Avoid: [NEG]
- `S12.png`
The waterfront skyline of a small fading Connecticut city at dusk, modest rooftops along a grey river mouth, a place labeled distressed, cool coastal light, no people, no readable signage [STYLE] Avoid: [NEG]
- `S13.png`
A gleaming corporate pharmaceutical research campus rising beside an old waterfront neighborhood, glass and steel under construction, its company logo blurred into an unreadable smear, the anchor that started it all, no people, no legible text [STYLE] Avoid: [NEG]
- `S14.png`
An architect's redevelopment site plan spread across a table under cold office light, abstract drafting lines and blocks of a peninsula, the marks unreadable, a whole point of land redrawn, no legible text, no people [STYLE] Avoid: [NEG]
- `S15.png`
A glowing architectural scale model of a gleaming waterfront development under gallery light, tiny towers and a marina lit from within, the promise rendered in miniature, no people, no legible text [STYLE] Avoid: [NEG]
- `S16.png`
An aerial-style map of a ninety-acre peninsula where a river meets the sound, the point of land marked for a grand plan, contours abstract and unreadable, no legible text, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S17.png`
A clean architectural rendering of a waterfront hotel and office towers on a point of land, glass conference space and research blocks, the upscale future promised on paper, no people, no legible text [STYLE] Avoid: [NEG]
- `S18.png`
A rendering of a marina and riverwalk with moored boats along a redeveloped waterfront, promenade lamps and new piers, the amenities the plan promised, no people, no readable signage [STYLE] Avoid: [NEG]
- `S19.png`
A row of modest older clapboard houses in a quiet working waterfront neighborhood at dusk, ordinary porches and small yards, the homes people actually lived in, no people, no readable sign [STYLE] Avoid: [NEG]
- `S20.png`
A tight cluster of modest homes on a peninsula seen from a low rise, roughly a neighborhood of small properties on a point of land, quiet and lived-in, no people, no readable signage [STYLE] Avoid: [NEG]
- `S21.png`
A small old house with a long-worn porch and a lived-in front garden at dusk, the kind of home someone was born in and never left, warm amber light in the windows, no people, no readable sign [STYLE] Avoid: [NEG]
- `S22.png`
The small pink house restored with care on its parcel by the water, fresh paint and a mended porch under amber light, a nurse's home made her own, one plot on a numbered plan, no people, no legible numbers [STYLE] Avoid: [NEG]
- `S23.png`
A single condemnation notice taped to a weathered front door in cold grey light, the printed lines abstract and unreadable, the paper that marks a home for the plan, no legible text, no people [STYLE] Avoid: [NEG]
- `S24.png`
A row of condemnation notices taped to door after door down an emptying street at dusk, homes marked not for any wrong but for standing where the plan wants something else, the paper unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S25.png`
A gavel resting on a deed and a folded government order on a bare table in cold light, the state's power to force a sale rendered as objects, the documents abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S26.png`
A thick legal complaint folder resting on a plain table under warm lamplight beside worn law books, a small public-interest firm carrying a neighborhood's refusal toward Washington, the text abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S27.png`
The marble steps of the Supreme Court ascending into cold night light, a case climbing all the way up the way these cases do, monumental and steep, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S28.png`
A classic public highway and a stone bridge under cold light, the plainest picture of a public use, a road the public rides, no people, no readable signage [STYLE] Avoid: [NEG]
- `S29.png`
An empty public rail platform with tracks receding under cold light, a rail line the public could ride, the ordinary meaning of public use, no people, no readable signage [STYLE] Avoid: [NEG]
- `S30.png`
A run-down blighted block of boarded windows and crumbling brick under grey light, the kind of neighborhood an earlier case had let a city clear, decay standing untouched, no people, no readable sign [STYLE] Avoid: [NEG]
- `S31.png`
Construction cranes rising over a cleared block of former blight in cold light, land handed to private builders after the old buildings came down, the earlier precedent rendered as a worksite, no people, no readable signage [STYLE] Avoid: [NEG]
- `S32.png`
Open farmland held under a wide sky, quiet fields once owned by only a tiny handful, the land at the center of an earlier ruling, no people, no readable signage [STYLE] Avoid: [NEG]
- `S33.png`
Surveyor's stakes and string dividing an open field into new parcels in cold light, farmland broken up and sold off to ordinary buyers, the earlier case rendered as a survey, no legible text, no people [STYLE] Avoid: [NEG]
- `S34.png`
A tidy modest waterfront street where nothing is falling down, well-kept clapboard homes under even grey light, a neighborhood that was not blighted at all, no people, no readable sign [STYLE] Avoid: [NEG]
- `S35.png`
A waterfront point of land at first light with the sun rising over the sound, growth and revival rendered as dawn over a dying city's harbor, the promise of jobs and taxes as light, no people, no legible text [STYLE] Avoid: [NEG]
- `S36.png`
The pale marble facade and tall columns of the Supreme Court seen frontally at night, solemn and about to decide, the whole case narrowed to four words, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S37.png`
A wall calendar turned to a single early-summer month in cold light, one day faintly ringed, the marks abstract and unreadable, the morning a decision came down, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S38.png`
A long courtroom bench with nine empty high-backed seats under cold marble light, five on one side faintly warmer than four, a split rendered as chairs, no people, no readable text [STYLE] Avoid: [NEG]
- `S39.png`
A single opinion volume lying open under a warm desk lamp, its pages reduced to abstract illegible lines, the majority opinion being written, no legible words, no people [STYLE] Avoid: [NEG]
- `S40.png`
The words public use dissolving into the words public purpose across a cold marble wall, both phrases abstract and unreadable, a reading stretched from one to the other, no legible words, no people [STYLE] Avoid: [NEG]
- `S41.png`
An architect's blueprint overlaid on a faint city skyline under warm light, economic development framed as a long-accepted function of government, the drafting marks abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S42.png`
Layered maps and studies stacked on a courthouse table under cold light, a careful, comprehensive plan the city had drawn up, the documents abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S43.png`
An empty referee's chair set to the side of a marble hall in cold light, a court declining to sit as a referee over the wisdom of a plan, deference rendered as an empty seat, no people, no readable text [STYLE] Avoid: [NEG]
- `S44.png`
A single narrow shaft of light falling on one page of an open volume in cold light, the holding narrower than the anger around it, a genuine deliberate plan rendered as a thin beam, no legible words, no people [STYLE] Avoid: [NEG]
- `S45.png`
A heavy marble door left deliberately ajar at the end of a cold colonnade, a fifth vote's warning that pretextual takings stay forbidden, a door kept open on purpose, no people, no readable sign [STYLE] Avoid: [NEG]
- `S46.png`
Four empty high-backed chairs set apart at a marble bench under cold light, the four justices who dissented rendered as vacant seats, solemn and separate, no people, no readable text [STYLE] Avoid: [NEG]
- `S47.png`
A separate opinion page lying alone in a hard shaft of light on a bench, the words people carry out of this case, the marks abstract and unreadable, a dissent rendered as a single page, no legible words, no people [STYLE] Avoid: [NEG]
- `S48.png`
A single pen resting across a closed opinion volume under cold light, the principal dissent set down beside the ruling it could not stop, abstract and severe, no legible text, no people [STYLE] Avoid: [NEG]
- `S49.png`
A long shadow of a wrecking crane thrown across the rooftops of an ordinary street at dusk, a specter of condemnation hanging over all property, symbolic and severe, no people, no readable sign [STYLE] Avoid: [NEG]
- `S50.png`
A plain low budget motel on one side of a single frame and a grand luxury hotel tower on the other under cold light, both brand names blurred into unreadable smears, one replaced by the other, no legible text, no people [STYLE] Avoid: [NEG]
- `S51.png`
A modest single-family home on one side of a frame and a sprawling shopping mall on the other under cold light, a home traded for a mall, the comparison rendered by grade and scale, no people, no readable signage [STYLE] Avoid: [NEG]
- `S52.png`
A quiet family farm on one side of a frame and a large industrial factory on the other under cold light, a farm traded for a factory, the swap rendered as two buildings, no people, no readable signage [STYLE] Avoid: [NEG]
- `S53.png`
A modest empty house at dusk dissolving into the rendering of a gleaming luxury tower, the ordinary home fading and the tower resolving, a designed silence rendered as a dissolve, no people, no legible text [STYLE] Avoid: [NEG]
- `S54.png`
A pair of scales tilted hard under cold light, one pan weighed down by glass corporate towers and the other holding a single small house, the harm falling unequally, no legible text, no people [STYLE] Avoid: [NEG]
- `S55.png`
Glass corporate towers rising cold and reflective against a night sky, the beneficiaries with disproportionate influence and power rendered as height and glass, no people, no readable signage [STYLE] Avoid: [NEG]
- `S56.png`
A glossy scale model of clustered development towers under gallery light, large corporations and development firms rendered as a gleaming maquette, no people, no legible text [STYLE] Avoid: [NEG]
- `S57.png`
A folded deed sliding along an arrow of cold light from a small modest house toward a towering glass building, property transferred from those with fewer resources to those with more, abstract, no legible text, no people [STYLE] Avoid: [NEG]
- `S58.png`
A single small modest house standing alone under cold grey light, the household with fewer resources, quiet and exposed, no people, no readable sign [STYLE] Avoid: [NEG]
- `S59.png`
A gated luxury estate and a glass tower under cold light, the owners with more resources and more influence, wealth rendered as scale, no people, no readable signage [STYLE] Avoid: [NEG]
- `S60.png`
An older leather-bound law volume standing open beside the newer one under a warm lamp, a separate originalist dissent reaching further back, the spine titles abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S61.png`
A village common or public green under open sky where the public actually gathers, the original meaning of public use rendered as land used by the public, no people, no readable signage [STYLE] Avoid: [NEG]
- `S62.png`
The engraved-looking words for public use fading from a marble wall, the phrase dissolving into blank stone, a written limit quietly erased, the characters abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S63.png`
A founding-era parchment and a resting quill under warm lamplight, a limit the Founders wrote down on purpose, the writing abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S64.png`
A receding row of small modest homes fading into cold haze, the neighborhoods always easiest to condemn, the burden falling hardest on the poor and powerless, no people, no readable signage [STYLE] Avoid: [NEG]
- `S65.png`
A gavel come to rest on a folded order over a deed under cold light while a marble colonnade stands untouched beyond, the dissent lost and the city allowed, the taking left standing, the documents abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S66.png`
A demolished residential block of splintered timber and rubble at dusk, the neighborhood homes pulled down and hauled away, the cleared street quiet, no people, no readable sign [STYLE] Avoid: [NEG]
- `S67.png`
A point of land scraped flat and graded bare under a wide grey sky, the whole neighborhood cleared and made ready for a grand plan, raw earth to the waterline, no people, no readable signage [STYLE] Avoid: [NEG]
- `S68.png`
An utterly empty flat cleared lot on a waterfront point under an even grey sky, nothing built where a grand plan was promised, bare ground and open horizon, no people, no readable signage [STYLE] Avoid: [NEG]
- `S69.png`
A curling abandoned site plan pinned to a leaning post on a deserted worksite, a stalled crane dark beyond it, financing that never came together, the drawing abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S70.png`
A rusting blank construction sign standing over an empty overgrown site at dusk, the grand plan fallen apart, the board weathered and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S71.png`
A gleaming corporate research campus gone dark with empty windows behind a chain-link fence, the anchor that started it all announcing its departure, its logo blurred into an unreadable smear, no people, no legible text [STYLE] Avoid: [NEG]
- `S72.png`
A vast empty corporate parking lot at dusk with faded painted lines and no cars, the research center closed and its jobs gone, the marks abstract and unreadable, no people, no legible text [STYLE] Avoid: [NEG]
- `S73.png`
A hollow abandoned office interior in cold light with bare desks and dark windows, a tax break expiring as the anchor leaves, empty and still, no people, no readable text [STYLE] Avoid: [NEG]
- `S74.png`
The bare parcel where the pink house once stood, a single empty waterfront lot at dusk with the sound beyond, first weeds beginning to break the graded earth, no people, no readable sign [STYLE] Avoid: [NEG]
- `S75.png`
A weed-grown vacant lot of chest-high grass on a waterfront point under grey light, years of nothing, no tax revenue and no towers, wild growth where a neighborhood stood, no people, no readable signage [STYLE] Avoid: [NEG]
- `S76.png`
The empty overgrown lot at dusk with a single lone deed-green marker post standing in the weeds, not one dollar of the promised revenue, quiet and abandoned, no people, no legible text [STYLE] Avoid: [NEG]
- `S77.png`
A heaped pile of storm debris and broken branches dumped across the cleared lot after a hurricane, the redevelopment ground turned into a dumping place, grey wreckage over weeds, no people, no readable sign [STYLE] Avoid: [NEG]
- `S78.png`
The small pink house being carefully taken apart board by board by preservation scaffolding, each plank saved and stacked, the one home spared and dismantled to be moved, no people, no readable text [STYLE] Avoid: [NEG]
- `S79.png`
The small pink house lifted whole onto a flatbed trailer rolling down a road to a new lot, the house saved and relocated rather than lost, a small stubborn survivor in transit, no people, no readable sign [STYLE] Avoid: [NEG]
- `S80.png`
The small pink house set down and settled on a new street elsewhere in the city under amber light, a modest monument to a fight its owner had lost, rebuilt on fresh ground, no people, no readable sign [STYLE] Avoid: [NEG]
- `S81.png`
A single spark drifting over a wide map under warm light, a decision landing like a match in dry grass, the map's labels abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S82.png`
A wide map of the United States under cold light with many states quietly glowing deed-green, a reaction crossing the whole country left and right, the labels abstract and unreadable, no legible text, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S83.png`
A tall stack of state statute-book spines standing on a courthouse shelf under warm light, many volumes of new law reining in eminent domain, the titles abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S84.png`
An uneven row of law volumes on a shelf under cold light, some thick and sweeping and some barely more than a slip, reforms that varied from state to state, the spine titles abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S85.png`
The relocated pink house on its new street at first light with the sound faintly beyond, the cold-open question returned and left open, warm amber against a grey dawn, no people, no readable sign [STYLE] Avoid: [NEG]
```

**枚数チェック:** 上記 85 エントリ（S01..S85）。§5.3 の `--only S01` ログで `shots=101`（body 85 + i2v種 16）を確認してから本番を回す。

---

# 6. A-2/A-3: 静止画のQC・目視・depth map

## 6.1 機械QC（body 85 + i2v種 16 = 全101枚・`qc_kelo_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `35.0<=mean_luma<=225.0`（EP46は暖色ピンクの家/夕暮れと冷たい大理石/夜/更地の灰色が混在→冷たい列柱・更地・夜側が黒潰れリスク。`check_visual_asset_qc.DARK_LUMA_FLOOR=45.0` を下回りすぎる本に注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject（`check_visual_asset_qc.NEARDUP_SIM=0.90`）。**バリエーション0なので本来ほぼ衝突しないはず。衝突したらプロンプトが被っている**（特に多数ある「ピンクの家」「大理石の最高裁列柱」「更地/空き lot」「収用通知」「対比構図(Motel/home/farm)」系に注意） | 片方 reject＋プロンプト見直し |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・判例番号・日付・金額・州数・会社/ブランドロゴが写っていないか（R1・制約2/6） | `has_readable_text=true`→reject |
| Q6 | 顔の混入 | **目視。** 識別可能な顔が写っていないか（R1・制約1/5・Kelo/判事の顔） | `has_identifiable_face=true`→reject |
| Q7 | 身体/扇情の混入 | **目視。** 人体・裸体・泣く人・嘆く家族・立退きの困窮・子ども（poverty porn）が写っていないか（制約5） | `has_human_body=true`→reject |

**Q5/Q6/Q7 は機械で判定しない。** コンタクトシートを出して**全101枚を実際に目視**する:

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-046-kelo --media image
#   → runs/qc/kelo_footage_contact_NN.png（20枚/シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-45 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** SDXL は平気で読める文字・顔・身体を描く。**特に制約2（可読の金額/日付/判例番号/会社・ブランドロゴの非露出）・制約5（Kelo 非人物化・扇情なし）は目視でしか守れない。** S13/S71（Pfizer拠点）・S50（Motel 6/Ritz-Carlton）は**ブランド名/ロゴが判読不能にぼけている**こと、S07/S40/S62（条文・語）は読める語が写っていないこと、S16/S37/S82（面積/日付/州数）は読める数値が写っていないこと、S23/S24（収用通知）は読める通知文が写っていないこと、S78/S79/S80（移築）は**ピンクの家が取壊されているように見えない**（board by board で保存・flatbed で移送されている）ことを必ず目で確認する。

## 6.2 出力

```
episodes/PD-2026-046-kelo/05_visuals/still_qc.v001.json     # 101枚全部の行（reject も残す・sha256/phash/mean_luma/long_edge）
（build_footage_contact_sheet が runs/qc に出す）
```

## 6.3 accepted が101枚に届かなかったとき

```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 46 --variants 1 --only S37   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_kelo_stills.py
```
accepted body >= 85 かつ i2v_source >= 16 になるまで繰り返す。**基準を下げない・バリエーションを足して水増ししない。**

## 6.4 depth map（★新規スクリプトを作らず既存を使う）

```bash
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir "H:/pd-media/assets/ai/kelo"
```
- モデル `Intel/dpt-large`。出力 `<stem>_depth.png`（同サイズ L グレースケール）。冪等。
- **role が `body` の静止画は depth 必須**（`treatment:"depth"` が隣に `_depth.png` を要求。無いとレンダーがクラッシュ）。i2v 種（`M<NN>_src.png`）は depth 不要。
- staging 後に `remotion/public/kelo/img/` 側でも同名ペアが揃っていること（§10）。

---

# 7. A-4: factory 実写クリップ 92本の選定と全点目視QC

## 7.1 在庫の実態

```
H:\pd-media\assets\factory\   フラット構成
  backgrounds/     11,000本超（.mp4）  ← ★主力（New England の海辺/川と入江・空の通り/更地・郊外の住宅街・大理石の裁判所/最高裁列柱・空の法廷・高速道路/橋/鉄道・農地/工場・企業キャンパス/ガラスの高層・夜〜夜明けの水辺・繋ぎ）
  light_assets/    …            合成レイヤー（暖色の porch 光・冷たい大理石の光条・夕暮れの採光）
  particle_assets/ …            合成レイヤー（海辺の霧/靄・大理石法廷の埃）
  vfx_overlays/    …            合成レイヤー（グレイン・光ノイズ）
  texture_assets/  …            紙・石・大理石・木材のテクスチャ
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
- **EP39（夜/取調室/青）・EP40（郊外/昼/破壊）・EP41（監獄/鉄/石の独房）・EP42（シカゴのアパート/足首モニタ）・EP43（RI の一軒家/救急車/レッカー）・EP44（ティール緑の病院の廊下/臨床）・EP45（暖色台所の督促状/郡拘置所 booking/アラバマ）の絵柄を選ばない。** EP46 は New England の海辺の街/川と入江/空の通り/更地・郊外住宅街・淡い大理石の裁判所と最高裁列柱・空の法廷・高速道路/橋/鉄道・農地/工場・企業キャンパス/ガラスの高層・夜〜夜明けの水辺。**鉄格子/独房/cellblock を含むクリップを選ばない（EP41 分離）。泣く人・立退きの困窮・子どもを含むクリップを選ばない（制約5）。**

**既存の選定ツールで候補出し（新規に検索ロジックを書くな）:**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes   # テーマ一覧と件数
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query waterfront --limit 96 --exclude-used --ep PD-2026-046-kelo --json
```
`--exclude-used` は `check_arc_nonrepeat.build_universe()` と同じ指紋集合を使うので出荷ゲート `arc_nonrepeat` と食い違わない。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・SDXLで作らない情景）

> **★`covers_scene_id` は still 資産 ID 空間（S01..S85・§2 注記）を指す。narrative シーン（DESIGN の S01..S48）とは別体系。** B はこの値を still 資産 ID として解決し、narrative シーンコードにクロスマップしない。

| covers | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S03 | 空の通り・更地の街区 | `empty_street_dusk` / `cleared_neighborhood_lot` | 0 |
| S06 | 最高裁ファサード・列柱（夜） | `supreme_court_building` / `marble_columns_night` | 0 |
| S12 | 海辺の小都市のスカイライン（夕暮れ） | `waterfront_town_dusk` / `harbor_city_skyline` | 1 |
| S19 | 古い modest な住宅街 | `old_clapboard_houses` / `working_class_neighborhood` | 1 |
| S28 | 高速道路・橋（public use） | `highway_overpass` / `stone_bridge` | 2 |
| S32 | 開けた農地 | `open_farmland` / `farm_fields` | 2 |
| S36 | 最高裁列柱（正面・夜） | `supreme_court_columns` / `marble_facade_night` | 2 |
| S50 | 廉価モーテル と 高級ホテル | `roadside_motel` / `luxury_hotel_tower` | 3 |
| S55 | ガラスの企業高層 | `glass_corporate_towers` / `skyscrapers_night` | 3 |
| S75 | 雑草の更地（水辺） | `vacant_lot_weeds` / `overgrown_empty_lot` | 5 |
| S82 | 合衆国の地図 | `usa_map` / `united_states_map` | 5 |
| S85 | 夜明けの水辺・川口（受け） | `river_estuary_dawn` / `coastal_water_dawn` | 5 |

**残り本数は covers を持たない繋ぎ・情景クリップ**（`covers_scene_id:null`）: 冷たい大理石の廊下・空の法廷・列柱の光条・海辺の街と川・空の通りと更地・農地/工場・企業キャンパス/ガラスの高層・夜〜夜明けの水辺・雨のアスファルト・書庫の棚・抽象 `loops`。**暗いクリップに偏りすぎない**（§7.5 の暗側閾値・全体の1/3=約30本まで。暖色 porch 光・大理石の昼光・夕暮れ側を優先）。

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
    --ep PD-2026-046-kelo --media video --dir "<92本の staging フォルダ>"
#   → runs/qc/kelo_footage_contact_NN.png（各タイルにファイル名ラベル）
```

2. **コンタクトシートを実際に開き、92本すべてを1本ずつ見る**
3. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて**選定から外す**
4. 実写シネマティックB-roll（アニメ/CG臭排除）・EP46テーマ（海辺の街/川と入江/空の通り/更地・大理石の裁判所と最高裁列柱・空の法廷・高速道路/橋/鉄道・農地/工場・企業キャンパス/ガラスの高層・夜〜夜明けの水辺）・ウォーターマークなし・識別可能な実在人物なし（制約1/5・R1）を確認
5. **★制約5/6の目視:** 人物が写るクリップは避け、写る場合も後ろ姿/遠景/顔外しのみ。**泣く人・嘆く家族・立退きの困窮・子ども（poverty porn）を含むクリップは使わない。** 判事席や街頭に実在の顔が写るニュース映像を使わない（制約1）。**鉄格子/独房/cellblock を含むクリップを使わない（EP41 分離）。企業ロゴ/ブランド名が判読可能なクリップを避ける（Pfizer/Motel 6/Ritz-Carlton・制約2）。**
6. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=45.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。
> **EP46 は冷たい大理石の列柱＋夜＋更地/空の通りが多いので暗側が本命リスク。** 平均輝度45未満のクリップが全体の40%を超えると FAIL。**暗いクリップは約30本（1/3）までに抑え、暖色 porch 光・海辺の昼光・夕暮れ・夜明けの実用光がある本を優先する。**

**1フレームで判断がつかない本は VLC/ffplay で再生して確認**（near-still は `check_animation_mix` を落とす）。

## 7.6 出力

```
episodes/PD-2026-046-kelo/05_stock/factory_selection.v001.json   # 選定理由と幕割り当て
episodes/PD-2026-046-kelo/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39〜EP45 との重複ゼロ（BLOCKING）

```bash
./.venv/Scripts/python.exe scripts/select_kelo_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` 〜 `episodes/PD-2026-045-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP46 の92本の積集合が**空**であることを確認。1件でも exit 1 で差し替え。**EP39〜EP45 のファイルは読むだけ。書き込み・移動・削除は一切しない。**

---

# 8. A-5: i2v モーション化 16本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする16本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）

種画像は §5 と同じ `generate_sdxl_4k.py --variants 1` で `M<NN>_src.png` として生成する（`ai_prompts.v001.md` に下記16行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `KELO-MS01..MS16`、モーション成果物の asset_id は `KELO-M01..M16`。

| # | asset_id | 種画像 | 動きの意味 | act |
|---|---|---|---|---|
| 1 | KELO-M01 | M01_src | ピンクの家の窓の外で水面が微かに揺れる夕暮れ | 0 |
| 2 | KELO-M02 | M02_src | 川と入江の灰色の水がゆっくり動く | 0 |
| 3 | KELO-M03 | M03_src | ドアに貼った収用通知の端が風で持ち上がる | 1 |
| 4 | KELO-M04 | M04_src | 光る waterfront 模型を光がゆっくり這う | 1 |
| 5 | KELO-M05 | M05_src | 更地に停まる解体重機・微かな待機 | 1 |
| 6 | KELO-M06 | M06_src | 最高裁の列柱へ緩い前進ドリー | 2 |
| 7 | KELO-M07 | M07_src | "public use" が "public purpose" へ溶ける | 2 |
| 8 | KELO-M08 | M08_src | 公共の高速道路/橋の光跡がゆっくり流れる | 2 |
| 9 | KELO-M09 | M09_src | Motel 6 と Ritz-Carlton の対比・冷たい光が移ろう | 3 |
| 10 | KELO-M10 | M10_src | modest な家が高級タワーへ溶暗する | 3 |
| 11 | KELO-M11 | M11_src | 四つの空席への緩いプッシュ（反対の4人） | 3 |
| 12 | KELO-M12 | M12_src | "for public use" の語が大理石から消えていく | 3 |
| 13 | KELO-M13 | M13_src | 雑草の更地に風が渡る（水辺の受け） | 5 |
| 14 | KELO-M14 | M14_src | 瓦礫の山越しに灰色の水が動く | 5 |
| 15 | KELO-M15 | M15_src | ピンクの家がフラットベッドで新しい通りへ転がる | 5 |
| 16 | KELO-M16 | M16_src | 新しい通りのピンクの家が夜明けへ移る（緩い引き） | 5 |

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの16行を追加・各1枚）

```
- `M01_src.png`
A small pink clapboard house on a point of land at dusk with wide grey water beyond its windows, warm amber porch light, still and poised for a slow hold, no people, no readable sign [STYLE] Avoid: [NEG]
- `M02_src.png`
Wide grey coastal water where a tidal river meets the sound under a low even sky, still and poised for a slow drift, the view a home was bought for, no people, no readable text [STYLE] Avoid: [NEG]
- `M03_src.png`
A single condemnation notice taped to a weathered front door in cold grey light, its printed lines abstract and unreadable, an edge poised to lift, no legible text, no people [STYLE] Avoid: [NEG]
- `M04_src.png`
A glowing architectural scale model of a gleaming waterfront development under gallery light, tiny lit towers and a marina, still and poised for light to crawl across it, no people, no legible text [STYLE] Avoid: [NEG]
- `M05_src.png`
An idle wrecking crew's excavator parked on a cleared block at dusk, the machine waiting on bare graded earth, still and poised, no people, no readable text [STYLE] Avoid: [NEG]
- `M06_src.png`
The pale marble colonnade of the United States Supreme Court at night lit from below, monumental and still, poised for a slow forward move, no people, no readable inscription [STYLE] Avoid: [NEG]
- `M07_src.png`
The words public use poised to dissolve into the words public purpose across a cold marble wall, both phrases abstract and unreadable, still and poised, no legible words, no people [STYLE] Avoid: [NEG]
- `M08_src.png`
A public highway and a stone bridge under cold light with faint traffic light trails, the plainest picture of a public use, framed for a slow drift, no people, no readable signage [STYLE] Avoid: [NEG]
- `M09_src.png`
A plain low budget motel and a grand luxury hotel tower held in one cold frame, both brand names blurred into unreadable smears, still and poised, no legible text, no people [STYLE] Avoid: [NEG]
- `M10_src.png`
A modest empty house at dusk poised to dissolve into the rendering of a gleaming luxury tower, still and held for a slow dissolve, no people, no legible text [STYLE] Avoid: [NEG]
- `M11_src.png`
Four empty high-backed chairs set apart at a marble bench under cold light, the four who dissented rendered as vacant seats, still and poised for a slow push, no people, no readable text [STYLE] Avoid: [NEG]
- `M12_src.png`
The engraved-looking words for public use poised to fade from a cold marble wall into blank stone, the characters abstract and unreadable, still and held, no legible words, no people [STYLE] Avoid: [NEG]
- `M13_src.png`
A weed-grown vacant lot of tall grass on a waterfront point under grey light with the sound beyond, still and poised for wind to move across the grass, no people, no readable signage [STYLE] Avoid: [NEG]
- `M14_src.png`
A heaped pile of storm debris and broken branches on a cleared waterfront lot with grey water beyond, still and poised for a slow drift, no people, no readable sign [STYLE] Avoid: [NEG]
- `M15_src.png`
The small pink house lifted whole onto a flatbed trailer on a road, the saved house poised to roll toward a new lot, still and framed for a slow move, no people, no readable sign [STYLE] Avoid: [NEG]
- `M16_src.png`
The relocated pink house on a new street at first light with the sound faintly beyond, warm amber against a grey dawn, still and open-ended, no people, no readable sign [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_kidsforcash.py` を下敷きにパスと SHOTS だけ差し替え）

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
STILL_DIR     = H:\pd-media\assets\ai\kelo      # 種画像 M<NN>_src.png を読む
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\kelo
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, text, watermark, identifiable face, real person likeness, child, crying person, gore, blood"
```

**ゲート:** `dry_validate`（length=5 で1回POSTして配線エラーを安く検出）/ `assert_loaded_completely`（部分ロード検出）/ `assert_frame_math`（フレーム計算）。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す）

```bash
py -3.11 scripts/comfy_wan_kelo.py --build            # グラフだけ（GPU触らない）
py -3.11 scripts/comfy_wan_kelo.py --run --shot M01   # 1本本番して目視
py -3.11 scripts/comfy_wan_kelo.py --run-all          # 残り15本（冪等・既存スキップ）
```
1本 24–73 GPU分・16本で 7–19時間。`/queue` `/history` を30秒間隔でポーリング。

## 8.4 RIFE で 48fps 化（`rife_kelo.py`・`rife_kidsforcash.py` と同手順）

```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは length=5 検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番にリネーム → RIFE 2x を**2回**（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. **フレーム数検証** `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC

- 顔・身体・子ども・扇情（泣く人・立退きの困窮）が生成されていないこと（NEG で抑えているが**必ず目視**・制約5）
- モーフィング/ちらつき/ワープが無いこと → あれば別シードで再生成
- M09（Motel/Ritz）・M04（模型）は**識別可能なブランド名/ロゴ**が写り込んでいないこと（制約2）
- M15/M16（フラットベッド・移築）は**ピンクの家が取壊されているように見えない**こと（保存・移送＝制約6）
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（16本 × 2回 = 32カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど12本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **6本** | 海辺の霧/靄・大理石法廷の埃・書庫の塵。黒背景 drift を screen 合成 |
| `light_assets` | **4本** | 暖色の porch 光・冷たい大理石の光条・夕暮れ/夜明けの採光 |
| `vfx_overlays` | **2本** | 微細なグレイン・冷たい光ノイズ |
| **合計** | **12本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/kelo/overlay/` に置き、`kelo_film.json` の `cuts[].src` には**出さない**（出すと factory 判定で1回制限を食う）。同じレイヤーを何度重ねてもよい（素材ではなく加工）。黒背景でループするものを選び `blend_hint` を書く。**§7.5 の目視QC対象**（12本・12分）。**合成レイヤーの発色は B が accent `#3F8F5F`（deed-green）に寄せる想定・A は色被りの素材を作らない（他話の gold/blue/amber/teal/crimson を選ばない）。**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --kind video --query coastal_mist --limit 20 --exclude-used --ep PD-2026-046-kelo --json
```

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_kelo_assets.py`）

```
remotion/public/kelo/img/     ← role=body の静止画85枚（+ 同名 _depth.png）
remotion/public/kelo/factory/ ← 選定 factory .mp4 92本
remotion/public/kelo/motion/  ← i2v M<NN>_rife.mp4 16本
remotion/public/kelo/overlay/ ← 合成レイヤー 12本
```
- `public_path` はマニフェストの値と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー（`import_to_remotion.py` の `conform_video(...,fps=30)` と同じ）
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する・外すと誤分類）:**
- factory の `public_path` は必ず `kelo/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も**含めない**
- 合成レイヤーは `kelo/overlay/` に置き `cuts[].src` に出さない

> **B のレンダは `--public-dir=public_slim`（Root.tsx に `id="Ep46Kelo"`）を使う想定だが、`public_slim` の構築は B の責務。** A は `remotion/public/kelo/` に正典を置くところまで（B が slim を派生させる）。

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`

全静止画・i2v・factory・overlay を1行ずつ: `asset_id`/`path`/`source`（`ai_codex` or `factory`）/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力

```bash
./.venv/Scripts/python.exe scripts/build_kelo_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_kelo_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_kelo_asset_manifest.py --reuse-feasibility
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

EP46 の設計値: still 101/85=1.19(≤2) / factory 92/92=1.0(≤1) / motion 32/16=2.0(≤2) / first-use 193/225=0.8578(≥0.70)。**全て達成可能。**

---

# 12. 絶対にやらないこと

- **EP39（frazier）/EP40（lech）/EP41（thompson）/EP42（young）/EP43（caniglia）/EP44（tekoh）/EP45（cleveland）のファイルに一切触らない。** 読み取りのみ可。素材・色（EP41 gold #E5B53A / EP42 blue #3B7DD8 / EP43 amber #E0913C / EP44 teal #2FA6A0 / EP45 crimson #B23A48）・音のレーンも分離。EP46 の accent は **deed-green #3F8F5F（土地・権利証・"greenlight"）**（INK #0A0A0C・B が OP/AEカード/サムネで使用・A は絵で流用色を作らない）。
- **スレッドBの所有ファイル（§0.2）に触らない。** 特に `remotion/src/**` `scripts/ae/**` `scripts/build_kelo_film.py` `manifest.json` `04_scenes/shotlist*` `figures`。
  - **ただし `04_scenes/ai_prompts.v001.md` は A が書く**（`generate_sdxl_4k.py` の入力・§5.9/§8.1a）。B は読むだけ。
- **図解・トランジション・タイポの素材を探しに行かない。** 在庫が薄い/無いカテゴリは B が自作する。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。ローカル A1111・ComfyUI・RIFE は GPU を使うだけで課金なし（オーナー許可済み）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness・身体をどこにも作らない**（§1・制約1/5）。特に **Susette Kelo を個人として描かない・判事を描かない**。
- **6制約に反する文言・絵をプロンプト・タグ・注記・ファイル名のどこにも作らない**（§1.2/§1.3）:
  - 収用の「違法／違憲（illegal/unconstitutional/struck down）」化（制約1）／「どんな理由でも家を奪える」過大化（制約2）／Kennedy nuance の消去（制約3）／O'Connor・Thomas を Court に帰属（制約4）／扇情（poverty porn・泣く人・子ども・立退きの困窮）（制約5）／「ピンクの家が取壊された」（制約6）／州数の断定（"45/47/all fifty states"・制約6）／可読の金額/日付/判例番号/会社・ブランドロゴ（制約2/6）。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。反復回避は distinct 85 で担保（§0.1・§5.6）。
- **role=thumb / still_thumb を作らない・overlay を12本以外にしない。** サムネは also_thumb=true の body 6枚（§4.3 = {S01,S02,S68,S75,S79,S83}）。
- **★dochighlight figure（黒バー/box/underline）を作らない・言及しない。** これは figures の責務（B）だが、A の `tags`/`caption_hint`/`notes` にも `dochighlight` という文字列を書かない（grep で 0 を保つ）。
- **枚数・本数を「だいたい」で決めない。** §3 の確定値（still 85 / factory 92 / i2v 16 / distinct 193 / first-use 0.8578 / still-share 0.4489 / MG≥30 / 12.0分）と §3.3 の検算をそのまま使う。合わなければ実装ではなく**本書を疑って報告**。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** EP36は大聖堂を、EP38は牛を通した。**生成物・在庫クリップを実際に見る**（特に制約2/5は目視でしか守れない・書面の可読文字・会社/ブランドロゴ・扇情描写も目視で排除）。

---

# 13. 完了報告に含めるもの

```
1. accepted 静止画の枚数と内訳（body 85 / i2v_source 16 / also_thumb 6 [S01/S02/S68/S75/S79/S83] / reject N）
2. factory 選定 92本のリスト（asset_id / subtype / eyeballed_content）と、subtype と食い違って外した本数、書面/対比/移築クリップの「no readable text / no logo / not demolished」確認
3. EP39/EP40/EP41/EP42/EP43/EP44/EP45 重複ゼロの確認結果
4. i2v 16本の frames / duration_sec と、SHORT? の有無
5. 合成レイヤー12本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code をそのまま貼る）
7. §3.3 の検算 [1]〜[7] を自分で再計算した結果
8. asset_manifest.v001.json の counts ブロック（still_body 85 / still_i2v_source 16 / motion 16 / factory 92 / overlay 12）
9. 6制約・1枚前提の自己申告（違法/違憲化・どんな理由でも化・Kennedy nuance 消去・O'Connor/Thomas を Court に帰属・扇情=poverty porn・ピンクの家 demolished・州数断定 が全出力に皆無・バリエーション0・Kelo/判事 非人物化を目視確認・dochighlight 文字列ゼロ・A↔B同一スキーマ [schema kelo_assets.v1 / role enum body|i2v_source|reject / counts / also_thumb 集合 {S01,S02,S68,S75,S79,S83} / overlay 12]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
</content>
</invoke>
