# EP48 glover — Codex スレッドA「素材生成」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN）も実装スレッドB（CODEX_B）のファイルも**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> **唯一の外部真実 = `episodes/_planning/EP48_glover_PRODUCTION_SPEC.v001.json`**（機械生成）。本書の数値はそこから転記したもので、手書きで発明していない。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP48 / Episode ID: PD-2026-048-glover / slug: glover
Composition id: Ep48Glover（B が Root.tsx に登録・A は staging まで・hookSeconds=8.0）
事件:       Kansas v. Glover, 589 U.S. ___ (2020) (No. 18-556)。決定 2020-04-06。
            保安官代理がプレートを照合し、登録者 Charles Glover Jr. の免許が「取消(revoked)」と判明。
            運転者を確認しないまま、登録者が運転していると推認して停止＝これは第4修正に反しない、と
            最高裁は 8-1 で UPHELD（合憲）。★停止を「違法」とは決して言わない。
            基準は reasonable suspicion（簡易な捜査的停止＝Terry級）であって probable cause ではない。
            推認は「打ち消す情報が officer に無い場合」に限り合理的で、運転者が明らかに所有者と別人なら消える。
            Thomas 法廷意見／Kagan 補足（Ginsburg 同調＝限界を強調）／Sotomayor 単独反対（逐語）。
            Charles Glover Jr. は存命の私人（免許取消中の運転で有罪）。顔・身体・肖像を出さない・象徴のみ。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**85本の固有プロンプト × 1枚 = 85枚**・バリエーション0） | `H:\pd-media\assets\ai\glover\S<NN>.png` | 2–3.5時間（GPU） |
| A-1b | i2v 種画像の生成（**16本の固有プロンプト × 1枚 = 16枚**・バリエーション0） | `H:\pd-media\assets\ai\glover\M<NN>_src.png` | 30–50分（GPU） |
| A-2 | 静止画のQCと目視（**目視必須**） | `05_visuals/still_qc.v001.json` + コンタクトシート | 1.5時間 |
| A-3 | depth map 生成（`treatment:"depth"` の必須入力） | `H:\pd-media\assets\ai\glover\S<NN>_depth.png` | 20分 |
| A-4 | factory 実写クリップ **92本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | **2.5時間（うち目視だけで1時間以上）** |
| A-5 | i2v モーション化 **16本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\glover\M<NN>_rife.mp4` | 7–19時間（GPU） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 **12本** | `05_stock/overlay_selection.v001.json` | 30分 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 20分 |
| A-8 | Remotion public への staging | `remotion/public/glover/{img,factory,motion,overlay}/` | 30分 |

> **★★ 最重要の前提（EP42–47 から継続）: 1シーン1枚・バリエーション0 ★★**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 85本＝85行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **`--variants 1`** で回す。**`--variants 3` は使わない。`_02`/`_03` を作らない。**
> **総生成画像 = still 85 + i2v 種 16 = 101枚（各1回）。** factory 92本は生成でなく在庫からの選抜。
> **★`--only S01` のログで `shots=101` を確認**してから本番を回す（85 body + 16 i2v種 = 101）。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-048-glover/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** このマニフェストは **A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致**で共有する（§4）。

> ★★ **EP45 の事故（本作で必ず回避）:** EP45 は asset_manifest に **stills しか埋めず factory/motion 配列を空のまま**出荷しかけた。**本作の `factory` 配列は 92 エントリ、`motion` 配列は 16 エントリ、`overlay` は 12 エントリを必ず public_path 付きで実体化する**（§4.4／§4.5／§4.6 に全数列挙済み。build スクリプトはこの列挙を消費するだけで、空配列を書かない）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\glover\**` / `H:\pd-media\assets\ai_video\glover\**` | **A** | 読み書き |
| `episodes/PD-2026-048-glover/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-048-glover/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/glover/{img,factory,motion,overlay}/**` | **A** | 読み書き |
| `episodes/PD-2026-048-glover/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_glover_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-047-*/**` および EP39〜47 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を `read_prompts()` で読む） | `PD-2026-048-glover --variants 1` / `48 --variants 1 --only S01` |
| `scripts/gen_depth_maps.py`（**既存**） | §6.4 の depth map | `--dir "H:/pd-media/assets/ai/glover"` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-048-glover --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit 96 --exclude-used --ep PD-2026-048-glover --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-048-glover` |

**★Aが新規作成するスクリプト（直近既存の複製。実在を `ls scripts/` で確認してから複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（複製元・実在確認済み） |
|---|---|---|
| `scripts/qc_glover_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_atwater_stills.py`（EP47） |
| `scripts/select_glover_factory.py` | §7 の factory 92本の確定選定・EP39〜47 sha256 除外検証 | `scripts/select_atwater_factory.py`（EP47） |
| `scripts/comfy_wan_glover.py` | §8 の i2v 16本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_atwater.py`（EP47・実在） |
| `scripts/rife_glover.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_atwater.py`（EP47・実在） |
| `scripts/build_glover_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_atwater_asset_manifest.py`（EP47） |
| `scripts/stage_glover_assets.py` | §10 の staging | `scripts/stage_atwater_assets.py`（EP47） |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある。あなたは **`ai_prompts.v001.md` を §5.2 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない。**
> **正確性ゲートは `check_glover_facts.py`（B が実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の6制約に一致し、`check_glover_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_glover_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。
#   → ★factory 配列長==92 / motion 配列長==16 / overlay 配列長==12 が非空で実体化していること（EP45 事故回避の必須不変条件）

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_glover_asset_manifest.py --reuse-feasibility
#   → still >=85 / motion >=16 / factory >=92 / distinct 合計 >=193 / first-use >=0.70

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_glover_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全92本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-048-glover
#   → exit 0（factory_clip_qc.v001.json が staging 済み全クリップを reviewed:true で網羅）

# [A-DONE-5] EP39〜EP47 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_glover_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39・EP40・EP41・EP42・EP43・EP44・EP45・EP46・EP47 の九つすべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（R2 ＋ 正確性6制約）★★★

**保安官代理はプレートを照合し、登録者 Charles Glover Jr. の免許が取消(revoked)と判明。運転者を確認しないまま、登録者が運転していると推認して停止した。最高裁は 8-1 でこの停止を UPHELD（合憲・第4修正に反しない）。本作は停止を「違法(illegal / unconstitutional / struck down)」とは決して言わない。基準は reasonable suspicion（簡易な捜査的停止＝Terry級）であって probable cause ではない。推認は「打ち消す情報が officer に無い場合」に限り合理的で、運転者が明らかに所有者と別人なら（例：登録者が60代なのに20代が運転）消える。票決 8-1（Thomas 法廷意見／Kagan 補足＝Ginsburg 同調で限界を強調／Sotomayor 単独反対）。逐語引用は反対/補足として中立帰属。Charles Glover Jr. は存命の私人で、顔・身体・肖像を一切出さない。象徴オブジェのみ。捏造引用禁止。**

## 1.1 R1（生成ビジュアル全般）

1. **実在人物の顔・likeness・肖像を作らない。** Charles Glover Jr.（存命私人）、Deputy Mark Mehrer、Thomas／Kagan／Ginsburg／Sotomayor を**顔・身体・肖像として描かない**。人物は原則出さない。**運転者・所有者は「顔のない影／シルエット」のみ**（"所有者≠運転者" のモチーフに限り featureless silhouette を許すが、顔・識別可能な特徴は描かない）。判事評言の逐語引用は AE カード（B の担当）であって画像ではない。
2. **実在の判決文・判例番号・条文・日付・プレート番号・免許番号の可読文字を再現しない。** プレート・免許証・登録票・訴状・意見書・条文ページ・ダッシュボードのヒット画面は雰囲気のみ（判読不能）。判例番号（589 U.S. / No. 18-556）・日付（2020 / 2020-04-06）・票決（8-1）・**プレート番号**・**免許番号**・**"REVOKED" の可読文字**は**画像に描かない**（AE/figures のタイポで出す＝B の担当）。会社/州/保安官事務所のロゴは**ぼかして判読不能**にする。
3. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性6制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **過大化しない（制約1・R-OVERCLAIM）。** 「police can stop any car / 警察はどんな車でも停められる / プレート照合だけで誰でも停められる」と書かない。判示は「登録者が運転していると推認できて、それを打ち消す情報が officer に無い場合に限り、その停止は合理的」。**推認は打ち消す情報があれば消える。**
2. **reasonable suspicion であって probable cause ではない（制約2・R-STANDARD）。** 基準を "probable cause" と書かない・"probable cause required/needed" と書かない。正しくは "reasonable suspicion"（簡易な捜査的停止＝Terry級）。
3. **停止を「違法」化しない（制約1）。** "the stop was illegal / unlawful / unconstitutional / struck down / overturned"・"Glover won / prevailed" を書かない。8-1 で UPHELD＝合憲。許容は "reasonable" / "upheld" / "allowed" / "constitutional" / "the stop stood" / "a narrow rule"。同時に「もうどこでも停められない／完全に禁止された」も誤りなので書かない。
4. **票決 8-1（制約3・R-VOTE）**（Thomas 法廷意見／Kagan 補足＝Ginsburg 同調／Sotomayor 単独反対）。画像に数字を描かない（象徴の光点で表す・8点 vs 1点）。逐語は AE カード（B）。**Sotomayor 逐語＝"Justice Sotomayor, dissenting"／Kagan 補足＝"Justice Kagan, concurring"** として中立帰属（制約5・R-QUOTE）。
5. **Charles Glover Jr. は存命の私人。顔・肖像・身体を描かない・象徴のみ（制約4・R-FACE）。** 原被疑事実（免許取消中の運転）以外の犯罪性を出さない。捏造引用禁止。
6. **数値・引用は原典一致（制約6）。** 8-1・2020-04-06・589 U.S. ___・No. 18-556。confidence:medium（保安官の氏名 Mehrer・郡・車種・プレート・手続経緯）はヘッジ／**画面に断定で出さない**。数値はどれも画像に可読で描かない（AE/figures＝B）。

## 1.3 機械ゲート（`build_glover_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
BANNED_PORTRAIT = re.compile(
    r"\bportrait\b|\bmugshot\b|likeness of|"
    r"face of (charles |mark )?(glover|mehrer|thomas|kagan|ginsburg|sotomayor)|"
    r"recognizable (real )?person|identifiable face|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"the stop (was|is|were)\s*(illegal|unlawful|unconstitutional|struck down|overturned|invalidated)|"
    r"(illegal|unlawful|unconstitutional) (stop|seizure|traffic stop)|"
    r"(court|scotus|supreme court|justices?) (struck down|overturned|banned|outlawed|invalidated) (the )?(stop|seizure)|"
    r"glover (won|prevailed|beat the|defeated)|"
    r"(police|officers?|cops?|deputy) (can|may|could) stop any (car|vehicle)|"
    r"stop any (car|vehicle) at any time|pull over any (car|vehicle)|"
    r"probable cause (is |was )?(required|needed)|requires probable cause|"
    r"(demographic|racial) profil\w* (is |was )?(allowed|permitted|endorsed|approved)|"
    r"legible (plate|license|registration) (number|plate)",
    re.IGNORECASE)
```

> `BANNED_ACCURACY` は制約1・2・3を機械化したもの。プロンプト・タグ・`caption_hint`・注記のどこにも該当語を書かない。**"reasonable suspicion" / "upheld" / "allowed" / "constitutional" / "a narrow rule" / "dissolves with contrary information" / "not probable cause"（"probable cause required" ではない）は許容。** 禁止は「停止の違法化」・「どこでも停められる/完全禁止」化・「Glover が勝った」・probable cause を基準と書くこと・profiling 是認・可読のプレート/免許/登録番号だけ。

---

# 2. 台本の語数と尺の確定値（SPEC から転記・Aが素材点数を積算する根拠）

**★唯一の真実 = `episodes/_planning/EP48_glover_PRODUCTION_SPEC.v001.json`。** 古い資料の wpm・語数は使うな。

```
words_total          = 2,136
narration_seconds    = 719.6   （= 12.0分・[SILENCE 1..] の実音無音を含む）
wpm_used             = 178.1
mean_shot            = 3.19秒/カット（SPEC 3.19・max_shot 6.0）
視覚シーン(narrative)  = 48（S01..S48・SPEC derive）
Act 構成（SPEC 秒・概算）: HOOK(8.0s cold-open) / OPENING / ACT1(最短) / ACT2 / ACT3（最長・最も荘厳）/ ENDING
```

**Aにとっての意味は1つ:** > **総カット 225 / distinct 193 / 初出 85.8% = still 85 + factory 92 + motion 16。**（§3 で積算）

> **注意（命名差）:** SPEC の視覚シーンは S01..S48。しかし **still は 85 本の固有プロンプトを持つ**ため、still の資産 ID は **S01..S85**（1プロンプト＝1枚）で採番する。48 の narrative シーンに 85 枚を配分する（ドクトリン核の ACT3 が最も厚い）。**still 資産 ID（S01..S85）と narrative シーンコード（S01..S48）は別物。** `covers_scene_id` は still 資産 ID 空間を指す（§7.3）。

---

# 3. ★素材構成の確定値（SPEC の distinct/cuts をそのまま調達する）

## 3.1 SPEC の内訳（★この値で調達する・勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **85枚** | 101カット | 1.19回(≤2) | **85本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **92本** | 92カット | **各1回(1)** | 在庫 11,000本超から選抜（§7）・全点目視・EP39〜47 と sha256 被りゼロ |
| **i2v モーション** | **16本** | 32カット | 各2回(≤2) | 16本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **193点** | **225カット** | | |
| 合成レイヤー（particle/light/vfx） | 12本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |

**SDXL の生成バッチ（本編カットに出ない i2v 種を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **85枚** | 85プロンプト × 1枚（バリエーション0） |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **16枚** | 16種プロンプト × 1枚（バリエーション0） |
| **SDXL 生成バッチ合計** | **85 + 16 = 101枚（各1回）** | **`--variants 1`** |

> **サムネは新規生成しない。** 完成後に body 85枚から6枚を `also_thumb:true` で流用選抜（追加生成ゼロ）。**role=thumb / still_thumb を作らない。**

> **★紙芝居回避（EP40 の最大の失敗）:** **still-cut 101 / (factory 92 + i2v 32)=video 124** で **still-share 44.89% ≤45%・motion coverage 55.11% ≥45%** を構造的に保証する（§3.3）。**stillを増やしてfactoryを削るな。factory 92 が still-share≤0.45 を守る下限。**

## 3.2 still 85枚・factory 92本・i2v 16本の幕別配分（目安・非拘束。合計だけが確定）

| 区間 | still（S番号） | factory | i2v |
|---|---|---|---|
| HOOK | 5（S01–S05） | 6 | 2（M01,M02） |
| OPENING | 3（S06–S08） | 3 | 0 |
| ACT1「その停止」 | 16（S09–S24） | 12 | 4（M03,M04,M05,M06） |
| ACT2「推認の論理」 | 18（S25–S42） | 16 | 3（M07,M08,M09） |
| ACT3「限界（判例核）」 | 28（S43–S70） | 24 | 4（M10,M11,M12,M13） |
| ENDING | 15（S71–S85） | 12 | 3（M14,M15,M16） |
| 繋ぎ（covers_scene_id:null） | — | 19 | — |
| **合計** | **85** | **92** | **16** |

> ACT3 は判例核（8-1・限界・Kagan補足・Sotomayor反対）なので still も最多の28枚。**幕別の factory/i2v 内訳は非拘束の目安値**（合計 92 / 16 のみ確定）。ゲートは factory を各1回・合計 92 でしか見ない。

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 225 = still 101 + factory 92 + i2v 32
[2] 平均ショット長 = narration 719.6 / 225 = 3.198秒/カット  ✓ (SPEC mean_shot 3.19・≤6.0)
[3] 静止画占有率(check_animation_mix) = 101/225 = 44.89%  ✓ ≤45%（SPEC still_share 0.4489・余裕0.11%）
[4] motion coverage = (92+32)/225 = 124/225 = 55.11%     ✓ ≥45%
[5] per-asset 上限: still 101/85=1.19(≤2) / factory 92/92=1.0(≤1) / motion 32/16=2.0(≤2)  ✓
[6] first-use share = 193/225 = 0.8578                   ✓ ≥0.70（SPEC 0.858 一致）
[7] factory 下限: i2v 32 は固定なので factory は 92 を下回れない（92+32=124=video）。→ factory 92 は下限であり水増しではない。
```

> **[3] の余裕は 0.11% しかない。** still が85本を割ったら §6.3 の再生成で回復させ、**still-cut 101 を増やさない**（B側の shotlist が101で固定）。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-048-glover/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `glover_assets.v1`（固定文字列）
**生産者:** `scripts/build_glover_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致。** role enum は **`body | i2v_source | reject` のみ**（`thumb`/`still_thumb` を作らない）。サムネは `also_thumb:true` の body still **ちょうど6枚**。overlay は **ちょうど12本**。

## 4.1 スキーマ（`glover_assets.v1`）

```jsonc
{
  "schema_version": "glover_assets.v1",
  "episode_id": "PD-2026-048-glover",
  "slug": "glover",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_glover_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 85,          // ==85
    "still_i2v_source": 16,    // ==16
    "motion": 16,              // ==16
    "factory": 92,             // ==92
    "overlay": 12              // ==12（distinct 素材に数えない）
  },
  "stills":  [ /* §4.3: body 85 (GLOV-S01..S85) + i2v_source 16 (GLOV-MS01..MS16) */ ],
  "motion":  [ /* §4.5: GLOV-M01..M16 全16本・public_path 必須（★非空） */ ],
  "factory": [ /* §4.4: 92本・public_path 必須（★非空・EP45事故回避の核心） */ ],
  "overlay": [ /* §4.6: 12本 */ ]
}
```

### 4.1a stills[] のエントリ形（body 例）

```jsonc
{
  "asset_id": "GLOV-S01",                 // body: ^GLOV-S\d{2}$（01..85） / i2v種: ^GLOV-MS\d{2}$
  "scene_id": "S01",                      // still 資産 ID 空間（§5.9 のプロンプト行に対応・S01..S85）
  "role": "body",                         // body|i2v_source|reject（各1枚・バリエーション概念なし）
  "also_thumb": false,                    // body から6枚だけ true（§4.3・追加生成しない）
  "act": 0,                               // 0=HOOK/OPENING, 1=ACT1, 2=ACT2, 3=ACT3, 5=ENDING
  "path": "H:/pd-media/assets/ai/glover/S01.png",
  "depth_path": "H:/pd-media/assets/ai/glover/S01_depth.png",   // role=="body" は実在必須
  "public_path": "glover/img/S01.png",    // role=="body" のみ非null
  "width": 3840, "height": 2160,          // 長辺>=3840
  "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 32.1,
  "tags": ["two_lane_road","kansas","night","symbolic","patrol"],
  "caption_hint": "an empty two-lane Kansas road at night under a patrol-steel sky, no people",
  "seed": 0, "model": "juggernautXL_ragnarokBy",
  "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
  "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
         "has_identifiable_face": false, "has_human_body": false, "notes": ""}
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `schema_version=="glover_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 85 / i2v_source 16 / motion 16 / factory 92 / overlay 12）に**一致**
3. 全 `path`/`depth_path`/`public_path` がディスクに実在
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `depth_path` と `public_path` が非null かつ実在
7. `qc.has_readable_text==true` / `qc.has_identifiable_face==true` / `qc.has_human_body==true` のいずれかは `role=="reject"`
8. `role=="i2v_source"` は `role=="body"` と**同一 asset_id を共有しない**（i2v_source は `^GLOV-MS\d{2}$`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39・EP40・EP41・EP42・EP43・EP44・EP45・EP46・EP47 の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない（＝目視していない本が混じっていない）
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど6**、かつ **`scene_id` 集合が `{S03,S04,S06,S12,S27,S43}`（§4.3）と完全一致**（body からの流用。**この集合は CODEX_B と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|reject のみ）
16. `overlay` 配列長が**ちょうど12**
17. ★**`factory` 配列長==92 かつ全エントリ `public_path` が非空**（EP45 事故回避・空配列/stub を許さない）
18. ★**`motion` 配列長==16 かつ全エントリ `public_path` が非空**（同上）

`--reuse-feasibility` では §3.3 [5][6][7] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 85枚（S01..S85）= §5.9 の85プロンプトの生成物。各1枚。
2. i2v_source 16枚（MS01..MS16 / 種画像 M01_src..M16_src）= §8.1a の16種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. also_thumb : body のうち S03 / S04 / S06 / S12 / S27 / S43 の6枚に true（追加生成しない）
     （plate-on-laptop=S03・REVOKED-hit-screen=S04・night-highway-taillights=S06・
      revoked-license=S12・scales=S27・SCOTUS-columns=S43）
4. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

## 4.4 ★`factory[]` 全92エントリ（★必ず実体化・public_path 非空。EP45事故回避の核心）

> `select_glover_factory.py` が下表の **public_path / act / covers_scene_id / subtype を pre-assign 済み**として消費し、`asset_id`（棚 id）/`path`（`H:/pd-media/assets/factory/...`）/`sha256`/`duration_sec`/`width`/`height`/`mean_luma`/`license`/`eyeballed_content`/`qc` を選抜・目視時に埋める（§7）。**空配列を書かない。** 各 public_path は `glover/factory/F0NN_<subtype>.mp4`。`type:"backgrounds"`, `kind:"video"`。covers は still 資産 ID 空間（§7.3）。

```jsonc
// HOOK (act 0) — 6本
{ "public_path":"glover/factory/F001_two_lane_kansas_road_night.mp4",   "act":0, "covers_scene_id":"S01",  "subtype":"two_lane_kansas_road_night" },
{ "public_path":"glover/factory/F002_rural_highway_night.mp4",          "act":0, "covers_scene_id":null,   "subtype":"rural_highway_night" },
{ "public_path":"glover/factory/F003_patrol_car_idling_shoulder.mp4",   "act":0, "covers_scene_id":null,   "subtype":"patrol_car_idling_shoulder" },
{ "public_path":"glover/factory/F004_prairie_road_dark.mp4",            "act":0, "covers_scene_id":null,   "subtype":"prairie_road_dark" },
{ "public_path":"glover/factory/F005_night_highway_taillights.mp4",     "act":0, "covers_scene_id":"S06",  "subtype":"night_highway_taillights" },
{ "public_path":"glover/factory/F006_empty_road_night_wide.mp4",        "act":0, "covers_scene_id":null,   "subtype":"empty_road_night_wide" },
// OPENING (act 0) — 3本
{ "public_path":"glover/factory/F007_supreme_court_columns_night.mp4",  "act":0, "covers_scene_id":"S07",  "subtype":"supreme_court_columns_night" },
{ "public_path":"glover/factory/F008_kansas_small_town_dusk.mp4",       "act":0, "covers_scene_id":null,   "subtype":"kansas_small_town_dusk" },
{ "public_path":"glover/factory/F009_county_courthouse_exterior.mp4",   "act":0, "covers_scene_id":null,   "subtype":"county_courthouse_exterior" },
// ACT1 (act 1) — 12本
{ "public_path":"glover/factory/F010_douglas_county_road_night.mp4",    "act":1, "covers_scene_id":"S09",  "subtype":"douglas_county_road_night" },
{ "public_path":"glover/factory/F011_patrol_car_cruising_night.mp4",    "act":1, "covers_scene_id":null,   "subtype":"patrol_car_cruising_night" },
{ "public_path":"glover/factory/F012_county_courthouse_dusk.mp4",       "act":1, "covers_scene_id":"S16",  "subtype":"county_courthouse_dusk" },
{ "public_path":"glover/factory/F013_courthouse_corridor_cold.mp4",     "act":1, "covers_scene_id":"S24",  "subtype":"courthouse_corridor_cold" },
{ "public_path":"glover/factory/F014_rural_kansas_road_evening.mp4",    "act":1, "covers_scene_id":null,   "subtype":"rural_kansas_road_evening" },
{ "public_path":"glover/factory/F015_prairie_highway_straight.mp4",     "act":1, "covers_scene_id":"S21",  "subtype":"prairie_highway_straight" },
{ "public_path":"glover/factory/F016_patrol_car_parked_night.mp4",      "act":1, "covers_scene_id":null,   "subtype":"patrol_car_parked_night" },
{ "public_path":"glover/factory/F017_small_town_street_night.mp4",      "act":1, "covers_scene_id":null,   "subtype":"small_town_street_night" },
{ "public_path":"glover/factory/F018_roadside_shoulder_night.mp4",      "act":1, "covers_scene_id":null,   "subtype":"roadside_shoulder_night" },
{ "public_path":"glover/factory/F019_gravel_road_night.mp4",            "act":1, "covers_scene_id":null,   "subtype":"gravel_road_night" },
{ "public_path":"glover/factory/F020_highway_overpass_night.mp4",       "act":1, "covers_scene_id":null,   "subtype":"highway_overpass_night" },
{ "public_path":"glover/factory/F021_dark_two_lane_road.mp4",           "act":1, "covers_scene_id":null,   "subtype":"dark_two_lane_road" },
// ACT2 (act 2) — 16本
{ "public_path":"glover/factory/F022_empty_courtroom.mp4",             "act":2, "covers_scene_id":"S31",  "subtype":"empty_courtroom" },
{ "public_path":"glover/factory/F023_courthouse_corridor_long.mp4",     "act":2, "covers_scene_id":"S40",  "subtype":"courthouse_corridor_long" },
{ "public_path":"glover/factory/F024_federal_courthouse_dusk.mp4",      "act":2, "covers_scene_id":"S42",  "subtype":"federal_courthouse_dusk" },
{ "public_path":"glover/factory/F025_patrol_car_roadside_dusk.mp4",     "act":2, "covers_scene_id":"S37",  "subtype":"patrol_car_roadside_dusk" },
{ "public_path":"glover/factory/F026_marble_hallway_cold.mp4",          "act":2, "covers_scene_id":null,   "subtype":"marble_hallway_cold" },
{ "public_path":"glover/factory/F027_courtroom_bench_empty.mp4",        "act":2, "covers_scene_id":null,   "subtype":"courtroom_bench_empty" },
{ "public_path":"glover/factory/F028_law_library_shelves.mp4",          "act":2, "covers_scene_id":null,   "subtype":"law_library_shelves" },
{ "public_path":"glover/factory/F029_marble_stairs_cold.mp4",           "act":2, "covers_scene_id":null,   "subtype":"marble_stairs_cold" },
{ "public_path":"glover/factory/F030_clerk_office_cold.mp4",            "act":2, "covers_scene_id":null,   "subtype":"clerk_office_cold" },
{ "public_path":"glover/factory/F031_empty_road_wide_night.mp4",        "act":2, "covers_scene_id":"S36",  "subtype":"empty_road_wide_night" },
{ "public_path":"glover/factory/F032_courthouse_columns_day.mp4",       "act":2, "covers_scene_id":null,   "subtype":"courthouse_columns_day" },
{ "public_path":"glover/factory/F033_office_corridor_fluorescent.mp4",  "act":2, "covers_scene_id":null,   "subtype":"office_corridor_fluorescent" },
{ "public_path":"glover/factory/F034_highway_horizon_dusk.mp4",         "act":2, "covers_scene_id":null,   "subtype":"highway_horizon_dusk" },
{ "public_path":"glover/factory/F035_marble_floor_light.mp4",           "act":2, "covers_scene_id":null,   "subtype":"marble_floor_light" },
{ "public_path":"glover/factory/F036_courthouse_exterior_night.mp4",    "act":2, "covers_scene_id":null,   "subtype":"courthouse_exterior_night" },
{ "public_path":"glover/factory/F037_federal_building_facade.mp4",      "act":2, "covers_scene_id":null,   "subtype":"federal_building_facade" },
// ACT3 (act 3) — 24本
{ "public_path":"glover/factory/F038_supreme_court_columns_frontal.mp4","act":3, "covers_scene_id":"S43",  "subtype":"supreme_court_columns_frontal" },
{ "public_path":"glover/factory/F039_supreme_court_steps_night.mp4",    "act":3, "covers_scene_id":null,   "subtype":"supreme_court_steps_night" },
{ "public_path":"glover/factory/F040_marble_colonnade_night.mp4",       "act":3, "covers_scene_id":"S59",  "subtype":"marble_colonnade_night" },
{ "public_path":"glover/factory/F041_supreme_court_facade_day.mp4",     "act":3, "covers_scene_id":null,   "subtype":"supreme_court_facade_day" },
{ "public_path":"glover/factory/F042_marble_hallway_grand.mp4",         "act":3, "covers_scene_id":null,   "subtype":"marble_hallway_grand" },
{ "public_path":"glover/factory/F043_law_library_old_volumes.mp4",      "act":3, "covers_scene_id":null,   "subtype":"law_library_old_volumes" },
{ "public_path":"glover/factory/F044_courtroom_grand_empty.mp4",        "act":3, "covers_scene_id":null,   "subtype":"courtroom_grand_empty" },
{ "public_path":"glover/factory/F045_marble_columns_light.mp4",         "act":3, "covers_scene_id":null,   "subtype":"marble_columns_light" },
{ "public_path":"glover/factory/F046_state_capitol_dome_dusk.mp4",      "act":3, "covers_scene_id":null,   "subtype":"state_capitol_dome_dusk" },
{ "public_path":"glover/factory/F047_capitol_rotunda_cold.mp4",         "act":3, "covers_scene_id":null,   "subtype":"capitol_rotunda_cold" },
{ "public_path":"glover/factory/F048_marble_bench_curved.mp4",          "act":3, "covers_scene_id":null,   "subtype":"marble_bench_curved" },
{ "public_path":"glover/factory/F049_courthouse_dome_night.mp4",        "act":3, "covers_scene_id":null,   "subtype":"courthouse_dome_night" },
{ "public_path":"glover/factory/F050_marble_wall_shadow.mp4",           "act":3, "covers_scene_id":null,   "subtype":"marble_wall_shadow" },
{ "public_path":"glover/factory/F051_grand_staircase_marble.mp4",       "act":3, "covers_scene_id":null,   "subtype":"grand_staircase_marble" },
{ "public_path":"glover/factory/F052_law_books_shelf.mp4",              "act":3, "covers_scene_id":null,   "subtype":"law_books_shelf" },
{ "public_path":"glover/factory/F053_courtroom_gallery_empty.mp4",      "act":3, "covers_scene_id":null,   "subtype":"courtroom_gallery_empty" },
{ "public_path":"glover/factory/F054_marble_pillar_detail.mp4",         "act":3, "covers_scene_id":null,   "subtype":"marble_pillar_detail" },
{ "public_path":"glover/factory/F055_supreme_court_plaza.mp4",          "act":3, "covers_scene_id":null,   "subtype":"supreme_court_plaza" },
{ "public_path":"glover/factory/F056_government_building_dusk.mp4",     "act":3, "covers_scene_id":null,   "subtype":"government_building_dusk" },
{ "public_path":"glover/factory/F057_marble_corridor_deep.mp4",         "act":3, "covers_scene_id":null,   "subtype":"marble_corridor_deep" },
{ "public_path":"glover/factory/F058_courthouse_interior_cold.mp4",     "act":3, "covers_scene_id":null,   "subtype":"courthouse_interior_cold" },
{ "public_path":"glover/factory/F059_archive_shelves_cold.mp4",         "act":3, "covers_scene_id":null,   "subtype":"archive_shelves_cold" },
{ "public_path":"glover/factory/F060_flag_pole_dusk_generic.mp4",       "act":3, "covers_scene_id":null,   "subtype":"flag_pole_dusk_generic" },
{ "public_path":"glover/factory/F061_marble_engraving_light.mp4",       "act":3, "covers_scene_id":null,   "subtype":"marble_engraving_light" },
// ENDING (act 5) — 12本
{ "public_path":"glover/factory/F062_two_lane_road_night_ending.mp4",   "act":5, "covers_scene_id":"S84",  "subtype":"two_lane_road_night_ending" },
{ "public_path":"glover/factory/F063_empty_road_evening.mp4",           "act":5, "covers_scene_id":null,   "subtype":"empty_road_evening" },
{ "public_path":"glover/factory/F064_kansas_road_horizon.mp4",          "act":5, "covers_scene_id":null,   "subtype":"kansas_road_horizon" },
{ "public_path":"glover/factory/F065_open_highway_dawn.mp4",            "act":5, "covers_scene_id":null,   "subtype":"open_highway_dawn" },
{ "public_path":"glover/factory/F066_quiet_town_evening.mp4",           "act":5, "covers_scene_id":null,   "subtype":"quiet_town_evening" },
{ "public_path":"glover/factory/F067_residential_driveway_night.mp4",   "act":5, "covers_scene_id":"S71",  "subtype":"residential_driveway_night" },
{ "public_path":"glover/factory/F068_road_vanishing_point.mp4",         "act":5, "covers_scene_id":null,   "subtype":"road_vanishing_point" },
{ "public_path":"glover/factory/F069_night_sky_open.mp4",               "act":5, "covers_scene_id":null,   "subtype":"night_sky_open" },
{ "public_path":"glover/factory/F070_corridor_door_light.mp4",          "act":5, "covers_scene_id":null,   "subtype":"corridor_door_light" },
{ "public_path":"glover/factory/F071_highway_evening_wide.mp4",         "act":5, "covers_scene_id":null,   "subtype":"highway_evening_wide" },
{ "public_path":"glover/factory/F072_prairie_evening.mp4",              "act":5, "covers_scene_id":null,   "subtype":"prairie_evening" },
{ "public_path":"glover/factory/F073_dark_highway_taillights.mp4",      "act":5, "covers_scene_id":null,   "subtype":"dark_highway_taillights" },
// 繋ぎ connective (covers null) — 19本
{ "public_path":"glover/factory/F074_marble_light_shaft.mp4",           "act":1, "covers_scene_id":null,   "subtype":"marble_light_shaft" },
{ "public_path":"glover/factory/F075_dust_in_light_bg.mp4",             "act":1, "covers_scene_id":null,   "subtype":"dust_in_light_bg" },
{ "public_path":"glover/factory/F076_rain_asphalt_night.mp4",           "act":1, "covers_scene_id":null,   "subtype":"rain_asphalt_night" },
{ "public_path":"glover/factory/F077_headlights_road_night.mp4",        "act":1, "covers_scene_id":null,   "subtype":"headlights_road_night" },
{ "public_path":"glover/factory/F078_cloud_timelapse_night.mp4",        "act":1, "covers_scene_id":null,   "subtype":"cloud_timelapse_night" },
{ "public_path":"glover/factory/F079_prairie_field_wind.mp4",           "act":2, "covers_scene_id":null,   "subtype":"prairie_field_wind" },
{ "public_path":"glover/factory/F080_empty_parking_lot_night.mp4",      "act":2, "covers_scene_id":null,   "subtype":"empty_parking_lot_night" },
{ "public_path":"glover/factory/F081_flag_texture_generic.mp4",         "act":2, "covers_scene_id":null,   "subtype":"flag_texture_generic" },
{ "public_path":"glover/factory/F082_marble_texture_pan.mp4",           "act":2, "covers_scene_id":null,   "subtype":"marble_texture_pan" },
{ "public_path":"glover/factory/F083_road_lines_passing.mp4",           "act":2, "covers_scene_id":null,   "subtype":"road_lines_passing" },
{ "public_path":"glover/factory/F084_fluorescent_ceiling_pan.mp4",      "act":2, "covers_scene_id":null,   "subtype":"fluorescent_ceiling_pan" },
{ "public_path":"glover/factory/F085_courthouse_window_light.mp4",      "act":3, "covers_scene_id":null,   "subtype":"courthouse_window_light" },
{ "public_path":"glover/factory/F086_night_treeline.mp4",               "act":3, "covers_scene_id":null,   "subtype":"night_treeline" },
{ "public_path":"glover/factory/F087_water_reflection_night.mp4",       "act":3, "covers_scene_id":null,   "subtype":"water_reflection_night" },
{ "public_path":"glover/factory/F088_asphalt_shimmer_night.mp4",        "act":3, "covers_scene_id":null,   "subtype":"asphalt_shimmer_night" },
{ "public_path":"glover/factory/F089_marble_floor_reflection.mp4",      "act":3, "covers_scene_id":null,   "subtype":"marble_floor_reflection" },
{ "public_path":"glover/factory/F090_night_sky_gradient.mp4",           "act":5, "covers_scene_id":null,   "subtype":"night_sky_gradient" },
{ "public_path":"glover/factory/F091_road_shoulder_gravel.mp4",         "act":5, "covers_scene_id":null,   "subtype":"road_shoulder_gravel" },
{ "public_path":"glover/factory/F092_horizon_line_night.mp4",           "act":5, "covers_scene_id":null,   "subtype":"horizon_line_night" }
```

**内訳検算:** HOOK 6 + OPENING 3 + ACT1 12 + ACT2 16 + ACT3 24 + ENDING 12 + 繋ぎ 19 = **92** ✓。全 `public_path` 非空 ✓（不変条件17）。

## 4.5 ★`motion[]` 全16エントリ（★必ず実体化・public_path 非空）

> エントリ形は §4.1a 準拠 + 動画フィールド。`asset_id ^GLOV-M\d{2}$`。`source_still` は §8.1a の種画像、`source_scene_id`=`MS<NN>`。runtime で `sha256`/`width 1280`/`height 720`/`fps 48`/`frames`/`duration_sec`/`qc` を埋める（§8.4）。**空配列を書かない。**

```jsonc
{ "asset_id":"GLOV-M01","source_scene_id":"MS01","source_still":"H:/pd-media/assets/ai/glover/M01_src.png","path":"H:/pd-media/assets/ai_video/glover/M01_rife.mp4","public_path":"glover/motion/M01_rife.mp4","act":0, "tags":["taillights","night_highway"] },
{ "asset_id":"GLOV-M02","source_scene_id":"MS02","source_still":"H:/pd-media/assets/ai/glover/M02_src.png","path":"H:/pd-media/assets/ai_video/glover/M02_rife.mp4","public_path":"glover/motion/M02_rife.mp4","act":0, "tags":["laptop_screen","hit_alert"] },
{ "asset_id":"GLOV-M03","source_scene_id":"MS03","source_still":"H:/pd-media/assets/ai/glover/M03_src.png","path":"H:/pd-media/assets/ai_video/glover/M03_rife.mp4","public_path":"glover/motion/M03_rife.mp4","act":1, "tags":["dashboard_laptop","plate_query"] },
{ "asset_id":"GLOV-M04","source_scene_id":"MS04","source_still":"H:/pd-media/assets/ai/glover/M04_src.png","path":"H:/pd-media/assets/ai_video/glover/M04_rife.mp4","public_path":"glover/motion/M04_rife.mp4","act":1, "tags":["side_mirror","light_bar"] },
{ "asset_id":"GLOV-M05","source_scene_id":"MS05","source_still":"H:/pd-media/assets/ai/glover/M05_src.png","path":"H:/pd-media/assets/ai_video/glover/M05_rife.mp4","public_path":"glover/motion/M05_rife.mp4","act":1, "tags":["pickup_pulling_over","shoulder"] },
{ "asset_id":"GLOV-M06","source_scene_id":"MS06","source_still":"H:/pd-media/assets/ai/glover/M06_src.png","path":"H:/pd-media/assets/ai_video/glover/M06_rife.mp4","public_path":"glover/motion/M06_rife.mp4","act":1, "tags":["revoked_license","light_move"] },
{ "asset_id":"GLOV-M07","source_scene_id":"MS07","source_still":"H:/pd-media/assets/ai/glover/M07_src.png","path":"H:/pd-media/assets/ai_video/glover/M07_rife.mp4","public_path":"glover/motion/M07_rife.mp4","act":2, "tags":["balance_scale","hunch_vs_proof"] },
{ "asset_id":"GLOV-M08","source_scene_id":"MS08","source_still":"H:/pd-media/assets/ai/glover/M08_src.png","path":"H:/pd-media/assets/ai_video/glover/M08_rife.mp4","public_path":"glover/motion/M08_rife.mp4","act":2, "tags":["fourth_amendment_page","light"] },
{ "asset_id":"GLOV-M09","source_scene_id":"MS09","source_still":"H:/pd-media/assets/ai/glover/M09_src.png","path":"H:/pd-media/assets/ai_video/glover/M09_rife.mp4","public_path":"glover/motion/M09_rife.mp4","act":2, "tags":["magnifying_glass","license"] },
{ "asset_id":"GLOV-M10","source_scene_id":"MS10","source_still":"H:/pd-media/assets/ai/glover/M10_src.png","path":"H:/pd-media/assets/ai_video/glover/M10_rife.mp4","public_path":"glover/motion/M10_rife.mp4","act":3, "tags":["supreme_court_colonnade","night"] },
{ "asset_id":"GLOV-M11","source_scene_id":"MS11","source_still":"H:/pd-media/assets/ai/glover/M11_src.png","path":"H:/pd-media/assets/ai_video/glover/M11_rife.mp4","public_path":"glover/motion/M11_rife.mp4","act":3, "tags":["eight_vs_one_light","vote"] },
{ "asset_id":"GLOV-M12","source_scene_id":"MS12","source_still":"H:/pd-media/assets/ai/glover/M12_src.png","path":"H:/pd-media/assets/ai_video/glover/M12_rife.mp4","public_path":"glover/motion/M12_rife.mp4","act":3, "tags":["owner_vs_driver_silhouettes","dissolve"] },
{ "asset_id":"GLOV-M13","source_scene_id":"MS13","source_still":"H:/pd-media/assets/ai/glover/M13_src.png","path":"H:/pd-media/assets/ai_video/glover/M13_rife.mp4","public_path":"glover/motion/M13_rife.mp4","act":3, "tags":["law_volumes","dust"] },
{ "asset_id":"GLOV-M14","source_scene_id":"MS14","source_still":"H:/pd-media/assets/ai/glover/M14_src.png","path":"H:/pd-media/assets/ai_video/glover/M14_rife.mp4","public_path":"glover/motion/M14_rife.mp4","act":5, "tags":["silhouette_resolving","seeing_clearly"] },
{ "asset_id":"GLOV-M15","source_scene_id":"MS15","source_still":"H:/pd-media/assets/ai/glover/M15_src.png","path":"H:/pd-media/assets/ai_video/glover/M15_rife.mp4","public_path":"glover/motion/M15_rife.mp4","act":5, "tags":["night_highway_taillights","evening"] },
{ "asset_id":"GLOV-M16","source_scene_id":"MS16","source_still":"H:/pd-media/assets/ai/glover/M16_src.png","path":"H:/pd-media/assets/ai_video/glover/M16_rife.mp4","public_path":"glover/motion/M16_rife.mp4","act":5, "tags":["laptop_cursor","final_pullback"] }
```

**検算:** 16エントリ ✓・全 public_path 非空 ✓（不変条件18）・`^GLOV-M\d{2}$` ✓。

## 4.6 `overlay[]` 12エントリ（distinct 素材に数えない）

```jsonc
// particle 6
{ "public_path":"glover/overlay/P01_marble_dust_motes.mp4",  "type":"particle_assets","subtype":"marble_dust_motes",  "blend_hint":"screen" },
{ "public_path":"glover/overlay/P02_courtroom_dust.mp4",     "type":"particle_assets","subtype":"courtroom_dust",     "blend_hint":"screen" },
{ "public_path":"glover/overlay/P03_archive_dust.mp4",       "type":"particle_assets","subtype":"archive_dust",       "blend_hint":"screen" },
{ "public_path":"glover/overlay/P04_fine_grain_dust.mp4",    "type":"particle_assets","subtype":"fine_grain_dust",    "blend_hint":"screen" },
{ "public_path":"glover/overlay/P05_night_road_dust.mp4",    "type":"particle_assets","subtype":"night_road_dust",    "blend_hint":"screen" },
{ "public_path":"glover/overlay/P06_shadow_dust.mp4",        "type":"particle_assets","subtype":"shadow_dust",        "blend_hint":"screen" },
// light 4
{ "public_path":"glover/overlay/L01_cold_patrol_steel_shaft.mp4","type":"light_assets","subtype":"cold_patrol_steel_shaft","blend_hint":"screen" },
{ "public_path":"glover/overlay/L02_cold_fluorescent_flicker.mp4","type":"light_assets","subtype":"cold_fluorescent_flicker","blend_hint":"screen" },
{ "public_path":"glover/overlay/L03_marble_light_shaft.mp4", "type":"light_assets","subtype":"marble_light_shaft",   "blend_hint":"screen" },
{ "public_path":"glover/overlay/L04_steel_edge_glow.mp4",    "type":"light_assets","subtype":"steel_edge_glow",      "blend_hint":"screen" },
// vfx 2
{ "public_path":"glover/overlay/V01_film_grain.mp4",         "type":"vfx_overlays","subtype":"film_grain",           "blend_hint":"overlay" },
{ "public_path":"glover/overlay/V02_cold_light_noise.mp4",   "type":"vfx_overlays","subtype":"cold_light_noise",     "blend_hint":"screen" }
```

runtime で `asset_id`/`path`/`sha256`/`license`/`eyeballed_content`/`qc` を埋める（§9）。**overlay は `cuts[].src` に出さない。** 発色は B が accent `#5B8DB8`（patrol-steel）に寄せる想定・A は他話色（gold/blue #3B7DD8/amber/teal/crimson/green/civil-violet）の素材を選ばない。**overlay 配列長ちょうど12**（不変条件16）。

---

# 5. A-1: SDXL 静止画のバッチ生成（85本 × 1枚・バリエーション0）

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-048-glover/04_scenes/ai_prompts.v001.md   ← A が §5.2 の形式で書く
出力:  H:\pd-media\assets\ai\glover\S<NN>.png（+ remotion/public/glover/ に自動コピー）
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
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 48 --variants 1 --only S01
#   → ログ "episode=... shots=101 variants=1 ... -> 101 images" の shots が 101 であること

# 全101枚（body 85 + i2v種 16・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-048-glover --variants 1
#   → 生成 S01.png ... S85.png / M01_src.png ... M16_src.png（各1枚。_02/_03 は作らない）
```

> QC で落ちたシーンの再生成は `--only S37`（同じプロンプトで別シードを1枚）。**基準を下げない・バリエーションで水増ししない。**

## 5.4 共通スタイル `[STYLE]`（全プロンプト末尾に必ず全文連結）

```
, cinematic still, dark documentary grade, cold Kansas night over a quiet two-lane road and the low glow of a patrol-car dashboard laptop, set against the cold institutional interior of a county courthouse and the pale marble of the United States Supreme Court, a single patrol-steel blue accent as the one cool signature note, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, low-key deep-shadow lighting, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no visible face, any human presence only as a featureless shadow or distant silhouette
```

> **EP39〜EP47 との分離（1語も含めない）:** `navy interrogation room`/`electric blue`（EP39 frazier）・`suburban demolition`/`bleached daylight`（EP40 lech）・`prison cell`/`cellblock`/`sodium prison corridor`（EP41 thompson・gold）・`Chicago apartment`/`ankle monitor`/`body-worn camera`（EP42 young・blue #3B7DD8）・`porch-amber house`/`ambulance red lights`/`tow-truck`（EP43 caniglia・amber）・`teal-green hospital corridor`/`clinical hospital`（EP44 tekoh・teal）・`warm-tungsten kitchen table`/`overdue crimson citation stack`（EP45 cleveland・crimson）・EP46 tlo の green 系・`dusty warm Texas afternoon`/`pickup child seats`/`booking area`/`civil-violet`（EP47 atwater・violet）。**EP48 は 夜の二車線 Kansas の道・パトカーのダッシュボードに載ったラップトップとその照合ヒット画面・夜のハイウェイのテールランプ・取消の判子が押された免許証・登録票・天秤（推認 vs 個別的疑い）・"所有者≠運転者" の顔なしシルエット対比（年配の男 vs 若い女）・最高裁の列柱と9席・patrol-steel `#5B8DB8` の一点差し色・夜〜夕暮れ。**

## 5.5 共通ネガティブ `[NEG]`（各 `Avoid:` の後に必ず全文付ける）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible license plate, legible plate number, legible license number, legible registration, legible revocation stamp, the word revoked, legible case citation, legible statute number, legible dollar amount, legible date, u.s. reports number, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, human body, weapon, gun, blood, gore, nude, bare skin, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, civil-violet, dusty texas afternoon, pickup child seats, booking area, navy interrogation room, electric blue, suburban demolition, tow truck, ambulance, porch amber house, ankle monitor, body-worn camera, prison cell, steel cellblock, barred cell, sodium prison corridor, teal-green hospital corridor, clinical hospital, warm tungsten kitchen table, overdue crimson citation stack, green courthouse
```

> ネガティブにも **制約違反語（"illegal stop", "unconstitutional", "glover won", "stop any car", "probable cause required" 等）を書かない**（§1.3）。**可読のプレート番号/免許番号/登録番号/"REVOKED" の文字・可読の金額/日付/判例番号・実在人物の顔・通貨の肖像・会社/州/保安官ロゴを NEG で明示的に抑制**（制約2/6）。ロゴやプレート数字が必要な絵は「blurred into an unreadable smear」で判読不能に。**シルエットは featureless（顔・識別特徴なし）**に限る。

## 5.6 バリエーション軸（★EP48 では無効）

`--variants 1` は各 stem を**1枚だけ**生成する。反復回避は「85本の固有プロンプト＝85の別被写体」で担保。

## 5.7 メタJSON

`generate_sdxl_4k.py` は per-image メタJSONを書かない。**A は QC 時に `qc_glover_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.8 プロンプトの絶対ルール（85本すべてに適用）

- **顔なし・身体なし・裸体なし。** Charles Glover Jr.・Deputy Mehrer・判事を個人として描かない（制約4/5）。**運転者・所有者は featureless silhouette / shadow のみ**（"所有者≠運転者" のモチーフでも顔・識別特徴を描かない）。
- **可読文字なし。** プレート・免許証・登録票・ダッシュボードのヒット画面・条文ページは雰囲気のみ。**プレート番号・免許番号・"REVOKED" の可読文字**・判例番号・日付・票決（8-1）・会社/州/保安官ロゴを描かない。
- **過大化しない（制約1）:** 「どんな車でも停められる」に見える絵（無数の車を無差別に停める等）を作らない。停止は narrow で個別的。
- **停止を「違法」化しない（制約3）:** 停止が違法/無効に見える絵を作らない。8-1 で UPHELD。
- **基準は reasonable suspicion（制約2）:** probable cause を象徴する絵（確証・完全な証拠の山）を「基準」として描かない。天秤は「hunch と proof の中間」を表す。
- **票決を数字で描かない（制約4）:** 8-1 は光点/光の分割の象徴で（可読数字なし・8点 vs 1点）。
- **逐語を可読で描かない（制約5）:** Sotomayor/Kagan の逐語は AE カード（B）。画像は象徴のみ。

## 5.9 確定プロンプト（★`ai_prompts.v001.md` にこの85エントリをそのまま書く・各1枚）

> 各行の `[STYLE]` は §5.4 を、`Avoid:` の後の `[NEG]` は §5.5 を**全文展開**して書く（下記は簡潔表記のマクロ）。全て顔なし・身体なし・象徴・判読不能・過大化なし。

```
- `S01.png`
A quiet two-lane road at the edge of a small Kansas town at night, a lone sheriff's patrol car idling on the gravel shoulder with its running lights low, traffic yet to pass, the ordinary road where it began, no people, no readable signage [STYLE] Avoid: [NEG]
- `S02.png`
The rear of an ordinary pickup truck seen from behind on a dark two-lane road, its blank license plate deliberately smeared unreadable in the patrol car's low beams, a vehicle that had done nothing wrong, no legible plate number, no visible face [STYLE] Avoid: [NEG]
- `S03.png`
A patrol-car dashboard at night with a bolted mobile laptop glowing patrol-steel blue, an abstract unreadable plate query typed into a blank field, the plate run on nothing but a hunch, no legible characters, no visible face [STYLE] Avoid: [NEG]
- `S04.png`
A close view of a patrol-car laptop screen in the dark glowing with a single highlighted status field in cold patrol-steel light, the record answering back, the alert abstract and unreadable, no legible words, no visible face [STYLE] Avoid: [NEG]
- `S05.png`
A patrol car's roof light bar flicking to life on a black two-lane road, cold blue-white light thrown across empty asphalt, the stop about to begin, no people, no readable text [STYLE] Avoid: [NEG]
- `S06.png`
The red taillights of a pickup truck receding down a dark Kansas highway, twin points of red against deep night, the driver present only as a car pulling away, no visible face, no readable signage [STYLE] Avoid: [NEG]
- `S07.png`
The pale marble columns of the United States Supreme Court at night lit coldly from below, distant and monumental, the court that would answer this in 2020, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S08.png`
A pickup truck's driver seat seen from outside at night, the figure behind the wheel only a featureless black silhouette, unknowable, owner or stranger, no visible face, no readable text [STYLE] Avoid: [NEG]
- `S09.png`
A rural Douglas County Kansas road at night with a patrol car cruising slowly, prairie darkness on either side, an ordinary patrol, no people, no readable signage [STYLE] Avoid: [NEG]
- `S10.png`
A patrol-car dashboard laptop glowing in the dark as an abstract unreadable registration record loads, the check an officer can run at will, no legible text, no visible face [STYLE] Avoid: [NEG]
- `S11.png`
An abstract vehicle registration card lying on a dark surface under cold light, its printed fields deliberately illegible, the truck traced to a name, no legible text, no people [STYLE] Avoid: [NEG]
- `S12.png`
A driver's license lying face-up on a dark surface under cold patrol-steel light, a heavy revocation stamp pressed across it rendered abstract and unreadable, the privilege withdrawn, no legible text, no portrait, no visible face [STYLE] Avoid: [NEG]
- `S13.png`
The interior of a pickup truck at night with the driver reduced to a featureless shadow against the windshield, identity withheld, the person never shown, no visible face, no readable text [STYLE] Avoid: [NEG]
- `S14.png`
The view down a dark two-lane road over a patrol car's hood toward a lone pickup ahead, its taillights small in the distance, the truck the deputy chose to follow, no visible face, no readable signage [STYLE] Avoid: [NEG]
- `S15.png`
A pickup truck pulled onto a night roadside with a patrol car drawn in behind it, both seen at a cold distance under a single light bar, the stop made, no people, no readable signage [STYLE] Avoid: [NEG]
- `S16.png`
The plain limestone exterior of a small Kansas county courthouse at dusk under a patrol-steel sky, civic and ordinary, where the case would be argued, no people, no readable sign [STYLE] Avoid: [NEG]
- `S17.png`
A folded suppression motion resting on a courtroom table under cold light, the paper abstract and unreadable, the challenge to the stop itself, no legible text, no people [STYLE] Avoid: [NEG]
- `S18.png`
A thin stack of driving-record papers on a dark desk in cold light, a habitual pattern reduced to abstract illegible lines, no legible text, no people [STYLE] Avoid: [NEG]
- `S19.png`
A single license plate resting isolated in a shaft of cold light on a dark surface, its characters deliberately unreadable, the one fact the whole stop rested on, no legible plate number, no people [STYLE] Avoid: [NEG]
- `S20.png`
An empty patrol-car front seat at night with the dashboard laptop gone dark, the machine that started it now silent, no people, no readable text [STYLE] Avoid: [NEG]
- `S21.png`
A wide empty Kansas prairie highway running straight to a black horizon at night, vast and quiet, the open road the case is set on, no people, no readable signage [STYLE] Avoid: [NEG]
- `S22.png`
A pickup truck's side mirror at night catching the cold reflection of an approaching patrol light bar, the stop seen only as a reflection, no visible face, no readable text [STYLE] Avoid: [NEG]
- `S23.png`
A closed traffic-citation book left unopened on a patrol-car hood in cold light, the ticket that was never the point, the paper abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S24.png`
A long county-courthouse corridor receding into cold institutional light with a polished floor and closed doors, the passage a case is carried up, no people, no readable signage [STYLE] Avoid: [NEG]
- `S25.png`
An old parchment page suggesting the text of the Fourth Amendment under a cold lamp, the words abstract and unreadable, a single band of patrol-steel light across it, the promise of reasonableness, no legible words, no people [STYLE] Avoid: [NEG]
- `S26.png`
A single car halted alone beneath a lone streetlight on a black road, caught and held in a cold cone of light, a seizure of a few minutes, no visible face, no readable text [STYLE] Avoid: [NEG]
- `S27.png`
A pair of plain balance scales on a dark surface weighing a small feather-light token against a heavy solid weight in cold patrol-steel light, a hunch against proof with the truth resting in between, symbolic and abstract, no legible text, no people [STYLE] Avoid: [NEG]
- `S28.png`
The same balance scales seen from a low angle poised almost level, neither certainty nor a mere guess, the in-between weight of reasonable suspicion, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S29.png`
A magnifying glass held over a driver's license on a dark desk in cold light, the license fields abstract and unreadable beneath the lens, looking closer at a name, no legible text, no visible face [STYLE] Avoid: [NEG]
- `S30.png`
A single traffic-citation form lying alone on a courtroom table in cold light, its edge touched with patrol-steel, the everyday ticket at the center of the fight, the paper abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S31.png`
An empty courtroom bench and rail standing in cold pale light, warm wood against pale stone, the room where the question would be weighed, no people, no readable text [STYLE] Avoid: [NEG]
- `S32.png`
A rubber filing stamp resting upright beside an ink pad on a clerk's desk in cold light, the small machine that turns a stop into a case, no legible text, no people [STYLE] Avoid: [NEG]
- `S33.png`
A fanned set of plain traffic-citation forms spread across a desk in cold light, the commonest kind of stop multiplied, edges abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S34.png`
A cold marble wall carrying a single engraved-looking band of light where the word reasonable would live, the characters abstract and unreadable, the one measure the amendment uses, no legible words, no people [STYLE] Avoid: [NEG]
- `S35.png`
Two clean paths of patrol-steel light diverging across a cold marble floor, two opposing arguments pointing in opposite directions, the state's and the driver's, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S36.png`
A single pickup truck seen tiny on a vast open Kansas road beneath an enormous night sky, one ordinary driver a plate might belong to, small under the law, no visible face, no readable signage [STYLE] Avoid: [NEG]
- `S37.png`
A patrol car parked alone at a two-lane roadside at dusk in patrol-steel light, empty and waiting, the ordinary traffic stop, no people, no readable text [STYLE] Avoid: [NEG]
- `S38.png`
A single badge-shaped glint of cold light on a dark surface, authority implied by one abstract highlight, no name, no legible text, no people [STYLE] Avoid: [NEG]
- `S39.png`
A vehicle registration card and a driver's license laid side by side on a dark surface in cold light, the name on the paper against the person at the wheel, both fields abstract and unreadable, no legible text, no visible face [STYLE] Avoid: [NEG]
- `S40.png`
A long courthouse corridor receding into cold institutional light with polished floor and closed doors, the passage a case climbs, no people, no readable signage [STYLE] Avoid: [NEG]
- `S41.png`
A neat stack of bound legal briefs on a desk in cold light, the arguments filed on both sides, the spines abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S42.png`
The modest stone facade of a federal courthouse at dusk under a patrol-steel sky, civic and unremarkable, the lower courts the case passed through, no people, no readable sign [STYLE] Avoid: [NEG]
- `S43.png`
The pale marble facade and tall columns of the United States Supreme Court seen frontally at night, monumental and solemn, the court that would decide it, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S44.png`
An empty curved bench of nine seats in a grand marble courtroom under cold light, the nine places rendered without any person, solemn and still, no people, no readable text [STYLE] Avoid: [NEG]
- `S45.png`
Eight points of patrol-steel light standing bright against a single dimmer point on a dark marble field, a lopsided majority rendered as light, no numerals, symbolic, no people, no text [STYLE] Avoid: [NEG]
- `S46.png`
A cold marble floor divided into a broad lit share and a single narrow darker sliver, an eight-to-one margin rendered as light, no numerals, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S47.png`
An old volume of law reports lying open under a cold desk lamp, its pages reduced to abstract illegible lines, the plain common sense the majority read into it, no legible words, no people [STYLE] Avoid: [NEG]
- `S48.png`
A receding shelf of old leather-bound law volumes in cold lamplight, the inherited body of precedent, the spine titles abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S49.png`
A founding-era quill and inkwell resting beside a heavy old statute volume under a cold lamp, the everyday reasoning the Court leaned on, the pages abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S50.png`
A single clean straight band of patrol-steel light running across a cold marble floor, a narrow bright-line rule easy to apply, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S51.png`
An old pocket watch on a dark surface with its hands blurred in swift motion under cold light, the split-second judgment forced on an officer at the roadside, no legible numerals, no people [STYLE] Avoid: [NEG]
- `S52.png`
A patrol car at a two-lane roadside at dusk with the road running on into patrol-steel distance, the practical moment of a stop, empty and still, no people, no readable text [STYLE] Avoid: [NEG]
- `S53.png`
A single license plate held solemn in a hard shaft of cold light on a dark surface, the one fact the deputy actually had, its characters unreadable, no legible plate number, no people [STYLE] Avoid: [NEG]
- `S54.png`
A driver's license bearing an abstract revocation stamp resting in a single hard shaft of cold light on dark marble, the status that made the inference reasonable, no legible text, no portrait, no people [STYLE] Avoid: [NEG]
- `S55.png`
Two featureless silhouettes set side by side in cold light, a tall older figure and a slighter younger one, plainly not the same person, the example that dissolves the suspicion, no faces, no readable text [STYLE] Avoid: [NEG]
- `S56.png`
A single featureless silhouette behind a windshield slowly resolving out of shadow in cold light, the moment the officer can see he is likely wrong, no visible face, no readable text [STYLE] Avoid: [NEG]
- `S57.png`
Two driver's licenses laid apart on a dark surface in cold light, one stamped abstractly as revoked and one merely marked, the revoked-versus-suspended line the concurrence drew, no legible text, no portrait, no people [STYLE] Avoid: [NEG]
- `S58.png`
A plain map of the United States with some regions lit in patrol-steel and others left in shadow in cold light, the many states and their driving records, the labels abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S59.png`
The marble colonnade of the Supreme Court at night lit from below, cold and distant, the narrow rule handed down, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S60.png`
A single point of patrol-steel light standing alone against eight brighter points on a dark marble field, the one who could not accept it, no numerals, symbolic, no people, no text [STYLE] Avoid: [NEG]
- `S61.png`
A pair of balance scales in cold light with the citizen's-liberty pan hanging heavy and the state's-burden pan riding light, the burden of proof the dissent said was lowered, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S62.png`
A single clean road of patrol-steel light being paved straight across a dark marble field, a road built from a profile rather than a fact, the dissent's warning rendered abstract, no people, no text [STYLE] Avoid: [NEG]
- `S63.png`
A single traffic-citation form standing alone in a shaft of cold light on a dark surface, the closer look the dissent said an officer should take, the paper abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S64.png`
A cold marble wall bearing an engraved-looking band of light being slowly darkened by an encroaching shadow, a burden of proof quietly lowered, symbolic and abstract, no legible words, no people [STYLE] Avoid: [NEG]
- `S65.png`
A heavy fold of shadow drawn like a mantle across an engraved-looking marble surface in cold light, a warning about where the rule could lead, symbolic, no legible words, no people [STYLE] Avoid: [NEG]
- `S66.png`
A single empty seat set slightly apart and in shadow at the end of a curved marble bench in cold light, the lone dissent that lost, solemn and still, no people, no readable text [STYLE] Avoid: [NEG]
- `S67.png`
A single gavel resting on its sounding block in a deserted grand marble courtroom under cold light, the authority of the Court held still, no people, no readable text [STYLE] Avoid: [NEG]
- `S68.png`
The pale marble facade of the Supreme Court seen frontally at night, the decision handed down and standing, monumental and cold, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S69.png`
A closed opinion volume set down under a cold lamp, its narrow rule now written, the pages abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S70.png`
A single license plate and a revocation-stamped driver's license together in one cold frame on a dark surface, the name and the status the Court let an officer act on, no legible text, no people [STYLE] Avoid: [NEG]
- `S71.png`
A single car sitting in a private driveway at night under a soft porch light, ordinary and still, your own car in your own driveway, no visible face, no readable plate [STYLE] Avoid: [NEG]
- `S72.png`
A patrol-car dashboard laptop glowing patrol-steel in the dark as an abstract plate query is entered again, the same machine on a new road, no legible characters, no visible face [STYLE] Avoid: [NEG]
- `S73.png`
A driver's license with an abstract revocation stamp resting in cold light, the kind of fact about an owner that can make a brief stop reasonable, no legible text, no portrait, no people [STYLE] Avoid: [NEG]
- `S74.png`
The interior of a car at night with the driver held as a featureless shadow, the brief moment of not knowing, no visible face, no readable text [STYLE] Avoid: [NEG]
- `S75.png`
A featureless silhouette behind a windshield emerging clearly out of shadow in cold light, the instant the officer can see the driver is plainly not the owner and the reason for the stop is gone, no visible face, no readable text [STYLE] Avoid: [NEG]
- `S76.png`
A single bright seam of patrol-steel light drawn across a dark map surface, one side lit and one side dark, a protection drawn as a narrow line, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S77.png`
A closed constitution rendered as a heavy book on a cold marble shelf with a single shaft of patrol-steel light falling across it, a right measured word by word, its title abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S78.png`
An open door onto cold night air standing beside a firmly closed door in deep shadow, the narrow permission open only for a moment, symbolic, no people, no readable sign [STYLE] Avoid: [NEG]
- `S79.png`
A patrol-car dashboard laptop glowing on a dark road with an abstract plate query poised in a blank field, the plate typed into every laptop on every quiet road after his, no legible characters, no visible face [STYLE] Avoid: [NEG]
- `S80.png`
A pickup truck seen small on an open Kansas road beneath a vast night sky, the man in the truck rendered only as a distant vehicle, quiet and dignified, no visible face, no readable signage [STYLE] Avoid: [NEG]
- `S81.png`
The red taillights of a pickup receding down a dark highway toward a black horizon, the case going on past him, no visible face, no readable signage [STYLE] Avoid: [NEG]
- `S82.png`
A vehicle registration card laid flat and settled on a plain surface in cold light, the record closed, its fields abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S83.png`
A pair of balance scales settling gently to a poised level in cold patrol-steel light, reasonable, specific, and in between, the measure the case leaves behind, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S84.png`
The empty two-lane Kansas road stretching to a deep patrol-steel horizon at night, the exact line the Court drew and has not erased, open-ended and unresolved, no people, no readable signage [STYLE] Avoid: [NEG]
- `S85.png`
A patrol-car laptop screen in the dark with an abstract cursor poised in a blank plate field, the next plate on the next road, the held final image, no legible characters, no visible face [STYLE] Avoid: [NEG]
```

**枚数チェック:** 上記 85 エントリ（S01..S85）。§5.3 の `--only S01` ログで `shots=101`（body 85 + i2v種 16）を確認してから本番を回す。**also_thumb 6枚 = {S03,S04,S06,S12,S27,S43}**（§4.3）。

---

# 6. A-2/A-3: 静止画のQC・目視・depth map

## 6.1 機械QC（body 85 + i2v種 16 = 全101枚・`qc_glover_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `30.0<=mean_luma<=225.0`（EP48 は夜のKansasの道・冷たいダッシュボード/booking・夜の最高裁が多く暗側リスク大。`DARK_LUMA_FLOOR=40.0` を大きく下回る本に注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject。**道路系(S01/S21/S84)・ラップトップ画面系(S03/S04/S72/S79/S85)・免許系(S12/S54/S73)・プレート系(S02/S19/S53)・最高裁列柱系(S07/S43/S59/S68)・シルエット系(S08/S13/S56/S74/S75)・光点の票決(S45/S60)・天秤(S27/S28/S61/S83)・扉(S78) の被りに注意** | 片方 reject＋プロンプト見直し |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・**プレート番号**・**免許番号**・**"REVOKED" の文字**・判例番号(589 U.S./18-556)・日付(2020)・票決(8-1)・会社/州/保安官ロゴが写っていないか（R1・制約2/6） | `has_readable_text=true`→reject |
| Q6 | 顔の混入 | **目視。** 識別可能な顔が写っていないか（シルエットも顔特徴が出ていないか）（R1・制約4/5） | `has_identifiable_face=true`→reject |
| Q7 | 身体/扇情の混入 | **目視。** 露出した人体・裸体・暴力・血が写っていないか（制約5・広告適合） | `has_human_body=true`→reject |

**Q5/Q6/Q7 は機械で判定しない。全101枚を実際に目視:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-048-glover --media image
#   → runs/qc/glover_footage_contact_NN.png（20枚/シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-47 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** SDXL は平気で読める文字・顔・身体を描く。**特に S03/S04/S72/S79/S85（ラップトップ画面）は読めるプレート番号/"REVOKED"文字が無いこと、S12/S54/S57/S73（免許）は読める免許番号・肖像が無いこと、S02/S19/S53（プレート）は読めるプレート番号が無いこと、S08/S13/S55/S56/S74/S75（シルエット）は識別可能な顔が出ていないこと、S45/S46/S60（8-1票決）は可読の数字が無いこと、S58/S76（地図）はロゴ/州名が判読不能なこと、を必ず目で確認する。**

## 6.2 出力

```
episodes/PD-2026-048-glover/05_visuals/still_qc.v001.json     # 101枚全部の行（reject も残す）
（build_footage_contact_sheet が runs/qc に出す）
```

## 6.3 accepted が101枚に届かなかったとき

```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 48 --variants 1 --only S37   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_glover_stills.py
```
accepted body >= 85 かつ i2v_source >= 16 になるまで繰り返す。**基準を下げない・水増ししない。**

## 6.4 depth map（★既存を使う）

```bash
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir "H:/pd-media/assets/ai/glover"
```
- モデル `Intel/dpt-large`。出力 `<stem>_depth.png`。冪等。
- **role が `body` の静止画は depth 必須**（無いとレンダーがクラッシュ）。i2v 種（`M<NN>_src.png`）は depth 不要。
- staging 後に `remotion/public/glover/img/` 側でも同名ペアが揃っていること（§10）。

---

# 7. A-4: factory 実写クリップ 92本の選定と全点目視QC

## 7.1 在庫の実態

```
H:\pd-media\assets\factory\   フラット構成
  backgrounds/     11,000本超（.mp4）  ← ★主力（夜のKansasの二車線道/空き道路・夜のハイウェイのテールランプ・パトカー・小さな町の庁舎/郡裁判所・大理石の裁判所/長い廊下・空の法廷・最高裁列柱・州会議事堂・夜〜夕暮れ・繋ぎ）
  light_assets/    …            合成レイヤー（冷たい patrol-steel の光条・冷たい fluorescent・大理石の光条）
  particle_assets/ …            合成レイヤー（大理石法廷の埃・書庫の塵・夜道の塵）
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
- **EP39〜EP47 の絵柄を選ばない（§7.7 の分離語）。** EP48 は 夜のKansasの二車線道/空き道路・夜のハイウェイのテールランプ・パトカー・郡裁判所/庁舎の外観・大理石の裁判所の長い廊下/空の法廷/最高裁列柱・州会議事堂・夜〜夕暮れの道。**鉄格子/独房/cellblock を選ばない（EP41 分離）。病院/臨床を選ばない（EP44 分離）。EP47 の「暖色のテキサス午後・空のチャイルドシート・booking area」は選ばない。実在の顔が写るニュース映像を選ばない（制約4/5・R1）。**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes   # テーマ一覧と件数
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query supreme_court --limit 96 --exclude-used --ep PD-2026-048-glover --json
```
`--exclude-used` は出荷ゲート `arc_nonrepeat` と同じ指紋集合を使う。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・§4.4 に pre-assign 済み）

> **★`covers_scene_id` は still 資産 ID 空間（S01..S85）を指す。narrative シーン（S01..S48）とは別体系。**

| covers | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S01 | 夜のKansas二車線道 | `two_lane_road_night` / `rural_road_night` | 0 |
| S06 | 夜のハイウェイのテールランプ | `night_highway_taillights` / `taillights_road` | 0 |
| S07 | 最高裁ファサード・列柱（夜） | `supreme_court_building` / `marble_columns` | 0 |
| S09 | Douglas County の夜の道 | `rural_county_road_night` / `patrol_road` | 1 |
| S16 | 郡裁判所の外観（夕暮れ） | `county_courthouse` / `small_town_courthouse` | 1 |
| S21 | Kansas プレーリーの直線道 | `prairie_highway` / `straight_rural_highway` | 1 |
| S24 | 裁判所の長い廊下 | `courthouse_corridor` / `long_hallway` | 1 |
| S31 | 空の法廷（無人） | `empty_courtroom` / `courtroom_interior` | 2 |
| S36 | 広い空き道路（俯瞰・夜） | `empty_road_wide_night` / `open_highway_night` | 2 |
| S37 | 路傍のパトカー（夕暮れ） | `patrol_car_roadside` / `police_car_dusk` | 2 |
| S40 | 裁判所の長い廊下 | `courthouse_corridor` / `marble_hallway` | 2 |
| S42 | 連邦裁判所の外観（夕暮れ） | `federal_courthouse` / `courthouse_exterior_dusk` | 2 |
| S43 | 最高裁の列柱（正面・夜） | `supreme_court_columns` / `marble_facade_night` | 3 |
| S59 | 最高裁の列柱（夜） | `marble_colonnade_night` / `columns_night` | 3 |
| S71 | 夜の私道/住宅街 | `residential_driveway_night` / `quiet_street_night` | 5 |
| S84 | 夜の空き二車線道（受け） | `two_lane_road_night` / `empty_road_evening` | 5 |

**残り本数は covers を持たない繋ぎ・情景クリップ**（`covers_scene_id:null`）: 大理石の廊下・空の法廷・列柱の光条・庁舎の外観・Kansas の空き道路・夜〜夕暮れの道・雨のアスファルト・書庫の棚・抽象 `loops`。**暗いクリップに偏りすぎない**（暗側は全体の1/3=約30本まで。大理石の昼光・夕暮れ側も混ぜる）。

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）

```python
ALLOWED_LICENSES = {"cc0","royalty_free","generated_owned","Pexels License","Pixabay Content License"}
```

## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★

> **推測ではなく実際に起きた事故。** EP36: `city_surveillance_camera_dome` が大聖堂。EP38: 牛が `documents_on_desk`。`subtype` は「その検索語で取った」記録であって**中身の保証ではない**。

**選抜92本は例外なく次を経る:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py \
    --ep PD-2026-048-glover --media video --dir "<92本の staging フォルダ>"
#   → runs/qc/glover_footage_contact_NN.png（各タイルにファイル名ラベル）
```

2. **コンタクトシートを実際に開き、92本すべてを1本ずつ見る**
3. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて**選定から外す**
4. 実写シネマティックB-roll（アニメ/CG臭排除）・EP48テーマ・ウォーターマークなし・識別可能な実在人物なし（制約4/5・R1）を確認
5. **★制約の目視:** 人物が写るクリップは避け、写る場合も後ろ姿/遠景/顔外しのみ。実在の判事/警官の顔が写るニュース映像を使わない。**鉄格子/独房/cellblock（EP41）・病院/臨床（EP44）・暖色テキサス午後/child seats（EP47）を含むクリップを使わない。**
6. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=40.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。
> **EP48 は夜のKansasの道・冷たい大理石・夜の最高裁が多いので暗側が本命リスク。** 平均輝度40未満が全体の40%を超えると FAIL。**暗いクリップは約30本（1/3）までに抑え、大理石の昼光・夕暮れ・実用光がある本を混ぜる。**

**1フレームで判断がつかない本は VLC/ffplay で再生して確認**（near-still は `check_animation_mix` を落とす）。

## 7.6 出力

```
episodes/PD-2026-048-glover/05_stock/factory_selection.v001.json   # 選定理由と幕割り当て
episodes/PD-2026-048-glover/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39〜EP47 との重複ゼロ（BLOCKING）

```bash
./.venv/Scripts/python.exe scripts/select_glover_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` 〜 `episodes/PD-2026-047-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP48 の92本の積集合が**空**であることを確認。1件でも exit 1。**EP39〜EP47 のファイルは読むだけ。書き込み・移動・削除は一切しない。**

**分離レーン（色・素材・語）:** EP41 gold（監獄）／EP42 blue #3B7DD8（ankle monitor）／EP43 amber（porch/救急車/レッカー）／EP44 teal（病院）／EP45 crimson（暖色台所/督促）／EP46 green／EP47 civil-violet #7A5CD0（暖色テキサス午後/booking/child seats）。**EP48 = patrol-steel #5B8DB8（INK #0A0A0C）。** これら他話の絵柄・色・被写体を1本も選ばない。**特に EP42 の blue #3B7DD8 と近色だが、EP48 は ankle monitor/Chicago apartment/body-worn camera の被写体を選ばない**（色ではなく被写体で分離）。

---

# 8. A-5: i2v モーション化 16本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする16本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）

種画像は §5 と同じ `generate_sdxl_4k.py --variants 1` で `M<NN>_src.png` として生成（`ai_prompts.v001.md` に §8.1a の16行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `GLOV-MS01..MS16`、モーション成果物は `GLOV-M01..M16`。

| # | asset_id | 種画像 | 動きの意味 | act |
|---|---|---|---|---|
| 1 | GLOV-M01 | M01_src | 夜のハイウェイをテールランプが遠ざかる | 0 |
| 2 | GLOV-M02 | M02_src | ダッシュボードのラップトップ画面が抽象的なヒット表示に解決する | 0 |
| 3 | GLOV-M03 | M03_src | ラップトップにプレート照会が打たれる（カーソルの動き） | 1 |
| 4 | GLOV-M04 | M04_src | サイドミラーにパトランプが映り込み光が掃く | 1 |
| 5 | GLOV-M05 | M05_src | ピックアップが路肩へ寄って停まる寸前 | 1 |
| 6 | GLOV-M06 | M06_src | 取消判子の免許証を patrol-steel の光が横切る | 1 |
| 7 | GLOV-M07 | M07_src | 天秤（hunch↔proof）が中間へ落ち着く | 2 |
| 8 | GLOV-M08 | M08_src | 第4修正の条文ページを patrol-steel の光が横切る | 2 |
| 9 | GLOV-M09 | M09_src | 虫眼鏡が免許証の上を移動する | 2 |
| 10 | GLOV-M10 | M10_src | 最高裁の列柱・冷たい光が動く | 3 |
| 11 | GLOV-M11 | M11_src | 8つの光点が1つに対して立つ（8-1・可読数字なし） | 3 |
| 12 | GLOV-M12 | M12_src | 年配の男と若い女の顔なしシルエット対比（推認が消える） | 3 |
| 13 | GLOV-M13 | M13_src | 古い法律書の棚・ランプの埃が舞う | 3 |
| 14 | GLOV-M14 | M14_src | 影の運転者シルエットがゆっくり見えてくる（見えた瞬間） | 5 |
| 15 | GLOV-M15 | M15_src | 夜のハイウェイのテールランプが遠ざかる | 5 |
| 16 | GLOV-M16 | M16_src | ラップトップの空プレート欄でカーソルが点滅・緩い pull-back（最終） | 5 |

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの16行を追加・各1枚）

```
- `M01_src.png`
The red taillights of a pickup truck on a dark Kansas highway, still and poised to recede into the night, the driver present only as a car pulling away, no visible face, no readable signage [STYLE] Avoid: [NEG]
- `M02_src.png`
A patrol-car dashboard laptop screen in the dark, still and poised with a single highlighted status field about to glow in cold patrol-steel light, the alert abstract and unreadable, no legible words, no visible face [STYLE] Avoid: [NEG]
- `M03_src.png`
A patrol-car dashboard laptop glowing patrol-steel at night with an abstract plate query poised in a blank field, still and framed for a slow cursor move, no legible characters, no visible face [STYLE] Avoid: [NEG]
- `M04_src.png`
A pickup truck's side mirror at night holding the cold reflection of a patrol light bar, still and poised for the lights to sweep, no visible face, no readable text [STYLE] Avoid: [NEG]
- `M05_src.png`
A pickup truck angled onto a dark roadside shoulder with a patrol car behind it, still and poised to slow to a stop, no people, no readable signage [STYLE] Avoid: [NEG]
- `M06_src.png`
A driver's license with an abstract revocation stamp on a dark surface in cold light, still and poised for a band of patrol-steel light to cross it, no legible text, no portrait, no people [STYLE] Avoid: [NEG]
- `M07_src.png`
A pair of plain balance scales weighing a light token against a heavy weight in cold light, still and poised to settle toward the middle, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `M08_src.png`
An old parchment page suggesting the Fourth Amendment under a cold lamp with the words abstract and unreadable and a single patrol-steel band of light poised to cross it, still, no legible words, no people [STYLE] Avoid: [NEG]
- `M09_src.png`
A magnifying glass held over a driver's license on a dark desk in cold light, the fields abstract and unreadable, still and poised for a slow move across the card, no legible text, no visible face [STYLE] Avoid: [NEG]
- `M10_src.png`
The pale marble colonnade of the United States Supreme Court at night lit from below, monumental and still, poised for a slow move, no people, no readable inscription [STYLE] Avoid: [NEG]
- `M11_src.png`
Eight points of patrol-steel light standing against a single dimmer point on a dark marble field, a lopsided majority rendered as light, still and poised, no numerals, symbolic, no people, no text [STYLE] Avoid: [NEG]
- `M12_src.png`
Two featureless silhouettes side by side in cold light, a taller older figure and a slighter younger one plainly not the same person, still and poised, no faces, no readable text [STYLE] Avoid: [NEG]
- `M13_src.png`
A shelf of old leather-bound law volumes in cold lamplight with dust hanging in the beam, still and poised for a slow push, the spine titles abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `M14_src.png`
The interior of a car at night with a featureless silhouette behind the windshield poised to resolve slowly out of shadow, the moment of seeing clearly, no visible face, no readable text [STYLE] Avoid: [NEG]
- `M15_src.png`
The red taillights of a pickup receding down a dark Kansas highway toward a black horizon, still and open-ended, no visible face, no readable signage [STYLE] Avoid: [NEG]
- `M16_src.png`
A patrol-car laptop screen in the dark with an abstract cursor poised in a blank plate field, still and framed for a slow pull-back, the held final image, no legible characters, no visible face [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_atwater.py` を下敷きにパスと SHOTS だけ差し替え）

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
STILL_DIR     = H:\pd-media\assets\ai\glover      # 種画像 M<NN>_src.png を読む
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\glover
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, text, watermark, identifiable face, real person likeness, legible plate number, gore, blood"
```

**ゲート:** `dry_validate`（length=5 で1回POSTして配線エラーを安く検出）/ `assert_loaded_completely` / `assert_frame_math`。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す）

```bash
py -3.11 scripts/comfy_wan_glover.py --build            # グラフだけ（GPU触らない）
py -3.11 scripts/comfy_wan_glover.py --run --shot M01   # 1本本番して目視
py -3.11 scripts/comfy_wan_glover.py --run-all          # 残り15本（冪等・既存スキップ）
```
1本 24–73 GPU分・16本で 7–19時間。`/queue` `/history` を30秒間隔でポーリング。

## 8.4 RIFE で 48fps 化（`rife_glover.py`・`rife_atwater.py` と同手順）

```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは length=5 検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番にリネーム → RIFE 2x を**2回**（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. **フレーム数検証** `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC

- 顔・識別可能な人物が生成されていないこと（NEG で抑えているが**必ず目視**・制約4/5）。シルエット（M12/M14）も顔特徴が出ていないこと
- モーフィング/ちらつき/ワープが無いこと → あれば別シードで再生成
- M01/M15（テールランプ道路）は**識別可能な人物・読めるプレート・読める標識**が写り込んでいないこと（制約2）
- M02/M03/M16（ラップトップ画面）は**可読のプレート番号/"REVOKED"文字**が出ていないこと（制約2/6）
- M11（8-1 光点）は**可読の数字が出ていない**こと（制約4）
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（16本 × 2回 = 32カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど12本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **6本** | 大理石法廷の埃・書庫の塵・夜道の塵。黒背景 drift を screen 合成 |
| `light_assets` | **4本** | 冷たい patrol-steel の光条・冷たい fluorescent・大理石の光条・steel の縁光 |
| `vfx_overlays` | **2本** | 微細なグレイン・冷たい光ノイズ |
| **合計** | **12本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/glover/overlay/` に置き、`glover_film.json` の `cuts[].src` には**出さない**。黒背景でループするものを選び `blend_hint` を書く（§4.6 の12本に対応）。発色は B が accent `#5B8DB8`（patrol-steel）に寄せる想定・A は他話色を選ばない。**§7.5 の目視QC対象**（12本）。

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --kind video --query dust_particles --limit 20 --exclude-used --ep PD-2026-048-glover --json
```

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_glover_assets.py`）

```
remotion/public/glover/img/     ← role=body の静止画85枚（+ 同名 _depth.png）
remotion/public/glover/factory/ ← 選定 factory .mp4 92本（§4.4 の F001..F092 名で）
remotion/public/glover/motion/  ← i2v M<NN>_rife.mp4 16本
remotion/public/glover/overlay/ ← 合成レイヤー 12本（§4.6 の P/L/V 名で）
```
- `public_path` はマニフェストの値（§4.4/§4.5/§4.6）と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する）:**
- factory の `public_path` は必ず `glover/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も**含めない**
- 合成レイヤーは `glover/overlay/` に置き `cuts[].src` に出さない

> **B のレンダは `--public-dir=public_slim`（Root.tsx に `id="Ep48Glover"`）を使う想定だが、`public_slim` の構築は B の責務。** A は `remotion/public/glover/` に正典を置くところまで。

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`

全静止画・i2v・factory・overlay を1行ずつ: `asset_id`/`path`/`source`（`ai_codex` or `factory`）/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力

```bash
./.venv/Scripts/python.exe scripts/build_glover_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_glover_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_glover_asset_manifest.py --reuse-feasibility
```
この3つが exit 0 で「マニフェストが本番になった」。**★factory 92 / motion 16 / overlay 12 が非空で実体化しているか（不変条件16/17/18）を必ず確認。** Bのファイルを直接書き換えて知らせようとしない。

---

# 11. 素材反復禁止ゲートの実仕様（`check_asset_reuse.py`）

```python
MAX_USES_FACTORY = 1
MAX_USES_MOTION  = 2
MAX_USES_STILL   = 2
MIN_FIRST_USE_SHARE = 0.70
```
種別判定は**パス文字列**（`kind_of()`）: `/factory` or `af-bg-` → factory / `.mp4|.mov|.webm` or `ai_video` or `_rife` → motion / それ以外 → still。§10.1 の命名規則を守る。

EP48 の設計値: still 101/85=1.19(≤2) / factory 92/92=1.0(≤1) / motion 32/16=2.0(≤2) / first-use 193/225=0.8578(≥0.70)。**全て達成可能。**

---

# 12. 絶対にやらないこと

- **EP39（frazier）〜EP47（atwater）のファイルに一切触らない。** 読み取りのみ可。素材・色・音のレーンも分離（§7.7）。EP48 の accent は **patrol-steel #5B8DB8**（INK #0A0A0C・B が OP/AEカード/サムネで使用・A は絵で流用色を作らない）。
- **スレッドBの所有ファイル（§0.2）に触らない。** 特に `remotion/src/**` `scripts/ae/**` `scripts/build_glover_film.py` `manifest.json` `04_scenes/shotlist*` `figures`。
  - **ただし `04_scenes/ai_prompts.v001.md` は A が書く**（§5.9/§8.1a）。B は読むだけ。
- **図解・トランジション・タイポの素材を探しに行かない。** 在庫が薄い/無いカテゴリは B が自作する。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。ローカル A1111・ComfyUI・RIFE は GPU を使うだけで課金なし。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness・身体をどこにも作らない**（§1・制約4/5）。特に **Charles Glover Jr.・Deputy Mehrer・判事を個人として描かない。運転者・所有者は featureless silhouette のみ（顔・識別特徴なし）。**
- **6制約に反する文言・絵をプロンプト・タグ・注記・ファイル名のどこにも作らない**（§1.2/§1.3）:
  - 過大化「どんな車でも停められる/stop any car」（制約1）／停止の「違法(illegal/unconstitutional/struck down)」化（制約3）／「Glover が勝った」（制約3）／基準を "probable cause" と書く（制約2）／票決の可読数字化（制約4）／逐語の可読描画（制約5）／可読のプレート/免許/登録番号・"REVOKED" 文字・判例番号/日付/ロゴ（制約2/6）／profiling 是認。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。反復回避は distinct 85 で担保。
- **role=thumb / still_thumb を作らない・overlay を12本以外にしない。** サムネは also_thumb=true の body 6枚（§4.3 = {S03,S04,S06,S12,S27,S43}）。
- **★factory 92 / motion 16 / overlay 12 の配列を空・stub のまま出荷しない**（EP45 の事故。§4.4/§4.5/§4.6 を必ず実体化・public_path 非空）。
- **★dochighlight figure（黒バー/box/underline）を作らない・言及しない。** A の `tags`/`caption_hint`/`notes` にも `dochighlight` という文字列を書かない（grep で 0 を保つ）。
- **枚数・本数を「だいたい」で決めない。** §3 の確定値（still 85 / factory 92 / i2v 16 / distinct 193 / first-use 0.8578 / still-share 0.4489 / MG≥30 / 12.0分）と §3.3 の検算をそのまま使う。合わなければ実装ではなく**本書を疑って報告**。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** EP36は大聖堂を、EP38は牛を通した。**生成物・在庫クリップを実際に見る**（特に制約2/4/5は目視でしか守れない）。

---

# 13. 完了報告に含めるもの

```
1. accepted 静止画の枚数と内訳（body 85 / i2v_source 16 / also_thumb 6 [S03/S04/S06/S12/S27/S43] / reject N）
2. factory 選定 92本のリスト（asset_id / subtype / eyeballed_content）と、subtype と食い違って外した本数、道路/画面/書面クリップの「no readable text / no legible plate / no logo / no face」確認
3. EP39〜EP47（九話）重複ゼロの確認結果
4. i2v 16本の frames / duration_sec と、SHORT? の有無
5. 合成レイヤー12本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code をそのまま貼る）＋ factory 92/motion 16/overlay 12 が非空で実体化した確認
7. §3.3 の検算 [1]〜[7] を自分で再計算した結果
8. asset_manifest.v001.json の counts ブロック（still_body 85 / still_i2v_source 16 / motion 16 / factory 92 / overlay 12）
9. 6制約・1枚前提の自己申告（過大化なし/停止の違法化なし/Glover勝訴化なし/基準=reasonable suspicion（probable cause と書かない）/票決可読数字なし/逐語可読描画なし・バリエーション0・Glover/Mehrer/判事 非人物化を目視確認・シルエットに顔特徴なし・可読プレート/免許/REVOKED 文字なし・dochighlight 文字列ゼロ・A↔B同一スキーマ [schema glover_assets.v1 / role enum body|i2v_source|reject / counts / also_thumb 集合 {S03,S04,S06,S12,S27,S43} / overlay 12]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
