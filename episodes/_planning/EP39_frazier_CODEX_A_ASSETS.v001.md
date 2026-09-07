# EP39 frazier — Codex スレッドA「素材生成」引き継ぎ（v001 / 2026-07-19）

```
あなたは Prime Documentary EP39 の【素材生成スレッド】担当です。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
このファイルだけを読んで作業できるように全数値・全パス・全コマンドをここに書いてある。
他のファイル（設計書 v001 / スレッドBのプロンプト）を読む必要はない。読まない前提で書かれている。
```

---

## 0. このスレッドの責務（これ以外はやらない）

**GPU律速の長時間ジョブと在庫からの選抜・目視QCを全部引き受け、EP39 が「同じ絵の使い回し」に落ちない量の素材を作り、1本の機械可読な台帳に出す。**

やること:
1. **factory 実写クリップの選抜・ステージング・全点目視QC**（110本 → on_theme 90本以上）← **工数の最大項目**
2. SDXL静止画の生成（**30シーン × 3バリエーション = 90枚**、長辺 ≥3840px）
3. 静止画の depth map 生成（CaseFilm の parallax treatment が要求する）
4. Wan 2.2 A14B による i2v モーション化（22本生成 → 18本以上採用）
5. 合成レイヤー（light / particle / vfx / loops）のステージング
6. 画像QC（暗すぎ・似すぎ・肖像違反・解像度不足の除去）
7. **境界契約ファイル `episodes/PD-2026-039-frazier/05_visuals/asset_manifest.v001.json` の出力**

やらないこと（**スレッドBの担当。手を出すな**）:
- Remotion のコード（`remotion/src/**`）、`remotion/props/**`
- After Effects スクリプト（`scripts/ae/**`）— **図解・トランジション・タイポグラフィは在庫が0本なので全部AEで自作する。それはBの担当。あなたは待たない。**
- 字幕生成スクリプト、ゲートスクリプト、film.json の生成
- サムネイル
- ナレーション（ElevenLabs）
- **台本に関わる一切**（台本は第3のスレッドで制作中。このスレッドは台本を1文字も読まないし待たない）

---

## 1. もう一方のスレッドとの境界（契約は1ファイルだけ）

```
スレッドA（あなた）  ──[ 05_visuals/asset_manifest.v001.json ]──>  スレッドB（実装）
```

- **あなたが書く唯一の共有物** = `episodes/PD-2026-039-frazier/05_visuals/asset_manifest.v001.json`
- スレッドBはこのファイルだけを読んで素材を割り当てる。**それ以外のあなたの中間生成物をBは読まない。**
- Bはあなたの完了を待たずに、`05_visuals/asset_manifest.stub.v001.json`（Bが自分で作るダミー台帳）で実装とドライランを完走する。**したがってあなたが遅れてもBはブロックされない。**
- **`asset_manifest.stub.v001.json` は絶対に触るな**（Bの持ち物）。あなたが書くのは `asset_manifest.v001.json` だけ。
- 両スレッドが `episodes/PD-2026-039-frazier/` 配下のディレクトリを `mkdir -p` 相当で作る。**削除・上書きは禁止**（作成のみ冪等に行う）。

> **名前の衝突注意（重要）:** リポジトリ直下に `assets/asset_manifest.v001.json` という**別物**（factory 棚の全体索引、読み取り専用）が既に存在する。あなたが書くのは **エピソード配下の** `episodes/PD-2026-039-frazier/05_visuals/asset_manifest.v001.json` である。**リポジトリ直下の `assets/asset_manifest.v001.json` を書き換えるな。**

---

## 2. 完了条件（これが全部緑になったら終わり）

| # | 条件 | 検証 |
|---|---|---|
| A-1 | `05_visuals/asset_manifest.v001.json` が §7 のスキーマに完全一致し `status: "final"` | §7.4 の自己検査を **assert** で（print で流すな） |
| A-2 | 台帳の `kind="factory"` が **90件以上**、全て `reviewed=true` かつ `on_theme=true` | §5.5 |
| A-3 | 台帳の `kind="still"` が **75件以上**、全て `long_edge_px >= 3840`、`qc.pass = true` | §7.4 |
| A-4 | 台帳の `scene_code` の**種類数が 45以上**（全kind合算。＝別の被写体が45種類以上ある） | §7.4。★最重要 |
| A-5 | 台帳の `kind="motion"` が **18件以上**、全て 41フレーム以上・1280x720 以上 | §6.4 |
| A-6 | 全 `public_path` が `remotion/public/` 配下に実在し `sha256` が実ファイルと一致 | §7.4 |
| A-7 | `05_visuals/factory_clip_qc.v001.json` が staging 済み全クリップを網羅 | `py -3.11 scripts/check_visual_asset_qc.py --ep PD-2026-039-frazier` が exit 0 |
| A-8 | 静止画の暗さ・近似重複がゲート閾値内 | 同上 |
| A-9 | 全静止画に `<stem>_depth.png` が隣接して存在 | §4.5 |
| A-10 | 合成レイヤーが `overlays` セクションに 30件以上（`assets` には入れない） | §5.6 / §7.3 |

**A-7 / A-8 は既存ゲート `scripts/check_visual_asset_qc.py` の実測結果のみが合否。自作の品質判定を書いて「合格」と宣言するな。**

---

## 3. 素材構成の設計（この数字が本スレッドの存在理由）

### 3.1 機械ゲート `check_asset_reuse.py`（レンダー前にブロックされる）

```bash
python scripts/check_asset_reuse.py <film.json>
```

実装済みの定数（`scripts/check_asset_reuse.py` L44-47。読んで確認済み）:

| 種別 | 同一素材の使用上限 | 理由 |
|---|---|---|
| factory クリップ | **1回**（再使用禁止） | 在庫が11,623本ある。繰り返す理由が無い |
| i2v モーション | **2回** | 1本あたり 24–73 GPU分と高コスト |
| SDXL 静止画 | **2回** | 生成コストはあるが安い |

さらに全体条件: **`first_use_share = distinct_assets / cuts_with_asset >= 0.70`**

kind の判定ロジック（同 L60-66）: パスに `/factory` を含むか `af-bg-` にマッチ → `factory`。`.mp4/.mov/.webm` で終わる → `motion`。それ以外 → `still`。
→ **台帳の `public_path` の置き場所がそのまま kind 判定になる。§7.2 のディレクトリ規則を厳守。**

実測した現状（2026-07-19・現行13本すべてFAIL）: rodriguez は62枚を188カットに回して平均3.03回、williams は73素材で344カット＝平均4.71回、EP38 は平均2.12回。最良の rolin は factory 188本を全て1回使用でクリア済み＝**この基準は達成可能**。

### 3.2 ★実測した在庫（`H:\pd-media\assets`。2026-07-19 実測）

| カテゴリ | 実測本数 | 性質 |
|---|---|---|
| `factory/backgrounds` | **11,623** | 実写クリップ。**動いている** |
| `factory/light_assets` | 1,401 | 合成レイヤー |
| `factory/particle_assets` | 1,225 | 合成レイヤー |
| `factory/vfx_overlays` | 1,196 | 合成レイヤー |
| `factory/loops` | 454 | 合成レイヤー |
| `ai`（既存生成物） | 1,287 | 他話の生成物。**EP39では使わない**（arc_nonrepeat） |
| `stock` | 235 | |

**中身0の空フォルダ:** `diagram_assets` / `transitions` / `typography_assets` / `parallax_layers` / `lottie_assets` / `ai_video_shots` / `sfx`
→ **図解・トランジション・タイポは在庫が存在しない。全部 After Effects で自作する（スレッドBの担当）。あなたはここを埋めようとしないし、待たない。**

### 3.3 ★素材構成の是正（オーナー指摘 2026-07-19「全て画像じゃなくてもいいんだよ。大量の素材があるからね」）

**旧案「静止画120枚」は SDXL に寄せすぎ。** 11,623本の実写在庫を使わずに静止画を積むのは、遅くて高くて、しかも**動いていないぶん `animation_mix` の motion coverage に不利**。

**確定する素材構成（226カット / distinct 176点）:**

| 種別 | distinct 点数 | 使用回数 | 生成カット数 | 調達 |
|---|---|---|---|---|
| **factory backgrounds** | **90本** | **1回** | 90 | 在庫11,623本から選抜。空気・情景・質感・繋ぎ |
| **SDXL静止画** | **68枚** | ≤2回（42枚×2 + 26枚×1） | 110 | **この作品にしか無い絵だけ**（匿名再現・固有の場所・象徴） |
| **i2v モーション** | **18本** | ≤2回（8本×2 + 10本×1） | 26 | 上のSDXLから選抜 |
| **合成レイヤー** (light/particle/vfx/loops) | 随時 | — | **0（カットに数えない）** | 静止画の上に重ねて動きを作る |
| — | **distinct 176** | | **226カット** | |

検算: `first_use_share = 176 / 226 = 0.779`（フロア 0.70 に対し 0.08 の余裕）。factory は全て1回（cap 1）、still 最大2回（cap 2）、motion 最大2回（cap 2）。**PASS。**

**合成レイヤー3,822点（light 1,401 + particle 1,225 + vfx 1,196）は distinct 素材に数えない。** これは `cuts[].src` に入れず、静止画の上に重ねるオーバーレイとして使う（→ §5.6 / §7.3 の `overlays` セクション）。**同じ静止画を別物に見せる**ために使えるので、**枚数を増やすより安い反復対策**である。

> **⚠ 旧設計書 v001 §8 の内訳「factory 約50本 ＋ 静止画 約50枚（各2回）＋ i2v 約15本（各2回）」は自分のゲートを通らない。**
> 検算: 50×1 + 50×2 + 15×2 = 180カット、distinct = 115、`115/180 = 0.639 < 0.70` → **FAIL**。上限いっぱいに使う設計は原理的に share を下げる。上表を使え。

### 3.4 シーン数は50を維持。ただし調達先を振り分ける

**シーン（＝別の被写体）は50個。** 反復感の原因は総枚数ではなくシーン数なので、ここは減らさない。減らすのは「SDXLで作るシーン数」だけ。

| 調達 | シーン数 | 判断基準 |
|---|---|---|
| **SDXL で作る** | **30シーン**（§4.2 の ★SDXL 列 = ✅） | 主役の匿名再現・この作品固有の場所（取調室・観察室・独房・面会室）・象徴カット。**在庫に存在しないもの** |
| **factory 実写で賄う** | **20シーン**（§4.2 の ★SDXL 列 = ▫） | 情景・繋ぎ・一般的な場所（郊外の通り・ダイナー・夜の街・最高裁外観・法廷・書架・廊下）。**在庫にあるもの** |

**フォールバック規則:** factory 側の20シーンについて、目視QCを通る適切なクリップが在庫から見つからなかった場合に限り、そのシーンを SDXL に回してよい（`ai_prompts.v001.md` に追記して `--only` で生成）。**逆は禁止**（SDXL 指定の30シーンを factory で代用しない。EP39固有の絵が在庫にあるはずがなく、代用は必ず「別の映画の映像」になる）。

### 3.5 生成量（QC落ちを見込んだ発注数）と工数見積り

| 種別 | 発注数 | 想定歩留まり | 納品（台帳） | Bの使用 | 見込み時間 |
|---|---|---|---|---|---|
| factory | **110本ステージング** | ≥82% | ≥90 | 90 | 選抜0.5h ＋ **全点目視QC 2.0h** ＋ 差し替え0.5h = **約3時間** |
| SDXL静止画 | **30シーン × 3 = 90枚** | ≥84% | ≥75 | 68 | 1枚あたり実測2–4分 → **4–6時間**（無人・冪等） |
| depth map | 採用枚数ぶん | 100% | — | — | 0.5–1時間 |
| i2v モーション | **22本** | ≥82% | ≥18 | 18 | 1本 24–73 GPU分 → **9–27時間**（無人・冪等） |
| 合成レイヤー | 40点ステージング | 100% | 30以上 | 随時 | 0.5時間 |

**★factory の全点目視QC 2時間は削るな。** これはコストではなく、EP36 の再発を防ぐ唯一の防御である（§5.5）。

---

## 4. 静止画（SDXL）— 手順

### 4.1 まず `ai_prompts.v001.md` を書く（**フォーマット厳守**）

保存先: `episodes/PD-2026-039-frazier/04_scenes/ai_prompts.v001.md`
**書くのは §4.2 で ★SDXL = ✅ の30シーンだけ。** ▫ のシーンを書くと無駄に90枚が180枚になる。

`scripts/generate_sdxl_4k.py` の `read_prompts()`（L73-86。読んで確認済み）は次の形しか解釈しない:

1. `- ` ＋ バッククォートで囲んだ `*.png` **のみ**の行
2. その次の行がプロンプト本文。**`Avoid:` 以降が negative prompt** として切り出される
3. positive は `Avoid:` の手前まで、末尾のピリオドは除去される
4. negative には `generate_sdxl_4k.py` の `DEFAULT_NEG`（実在人物・顔・肖像・可読テキスト・ロゴ・透かし・低解像度・変形など）が**自動で追加される**

**この形から外れた行は無視され、その画像は永久に生成されない。** 見出し（`## …`）や引用（`> …`）は自由に書いてよい（パーサは無視する）。

**共通スタイル接尾（全プロンプトの `Avoid:` の直前に必ず入れる）:**
```
, cinematic still, dramatic volumetric lighting, moody, deep blacks and navy blue with electric-blue and gold accents, silver highlights, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, film grain, no text, no watermark, no logo
```

**共通ネガティブ（各行の `Avoid:` の直後に必ず入れる）:**
```
text, words, letters, captions, watermark, logo, real celebrity, recognizable real person, identifiable face, cartoon, low quality, deformed, extra limbs, nudity, explicit, gore, blood, violence, restraint, child
```

**完成形の例（S01。この2行組を30個書く）:**
```
- `S01.png`
  An empty police interrogation room at night, one steel table bolted to the floor, two facing chairs, a single caged ceiling light, a dark one-way mirror on the wall, cold institutional green-grey walls, utterly still and oppressive, no people, cinematic still, dramatic volumetric lighting, moody, deep blacks and navy blue with electric-blue and gold accents, silver highlights, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, film grain, no text, no watermark, no logo. Avoid: text, words, letters, captions, watermark, logo, real celebrity, recognizable real person, identifiable face, cartoon, low quality, deformed, extra limbs, nudity, explicit, gore, blood, violence, restraint, child
```

### 4.2 50シーンの一覧（★SDXL 列で調達先が決まる）

**列の意味:** `★SDXL` = ✅ なら SDXL で作る（30シーン）／ ▫ なら **factory 実写で賄う**（20シーン。§5.2 の `factory_query` でクリップを探す）。`P` は優先度（1が最優先）。

#### HOOK / 主舞台（S01–S03）

| ID | ★SDXL | P | 主題 | プロンプト本文（✅） / factory_query（▫） |
|---|---|---|---|---|
| S01 | ✅ | 1 | 取調室（無人・主舞台） | An empty police interrogation room at night, one steel table bolted to the floor, two facing chairs, a single caged ceiling light, a dark one-way mirror on the wall, cold institutional green-grey walls, utterly still and oppressive, no people |
| S02 | ✅ | 1 | 閉まる鉄扉（内側から） | A heavy steel interrogation-room door caught in the act of closing, seen from inside the room, a narrowing blade of corridor light on the floor, cold blue outside and warm dead fluorescent inside, symbolic of the world shutting out |
| S03 | ✅ | 1 | 一方向ミラー越し | The view through a dark one-way observation mirror into a lit interrogation room, the glass carrying a faint reflection of the dark observation side, an empty chair visible beyond, cold surveillance detachment, no people |

#### 幕1 — その夜（S04–S15）

| ID | ★SDXL | P | 主題 | プロンプト本文（✅） / factory_query（▫） |
|---|---|---|---|---|
| S04 | ▫ | 1 | 平穏な郊外の朝 | theme `property_home` / query `suburban street`, `residential morning`, `neighborhood house` |
| S05 | ✅ | 2 | 主役の日常（作業机） | A cluttered home workbench under a single warm desk lamp, hand tools and an unfinished repair job laid out mid-task, a cold jacket over the chair back, nobody present, intimate ordinary life interrupted |
| S06 | ▫ | 2 | 夕方のダイナー | theme `urban_night` / query `diner`, `cafe interior`, `neon window` |
| S07 | ▫ | 2 | 雨の夜のバス停 | theme `urban_night` / query `rain street night`, `bus stop`, `wet asphalt reflection` |
| S08 | ✅ | 1 | 玄関の人影 | The frosted glass panel of a front door at night seen from inside a dark hallway, the blurred silhouettes of two standing figures on the other side, porch light glaring through, unreadable and imminent, no visible faces |
| S09 | ✅ | 1 | パトカー後部座席 | The empty back seat of a police cruiser at night seen through the steel divider cage, vinyl bench worn and cold, streetlights sliding past the window glass, oppressive confinement, no people |
| S10 | ▫ | 2 | 夜の街の警光灯 | theme `crime_police` / query `police lights night`, `patrol car`, `emergency light street` |
| S11 | ▫ | 2 | 警察署の受付 | theme `crime_police` / query `police station interior`, `precinct desk`, `station lobby` |
| S12 | ▫ | 1 | 夜勤の廊下 | theme `crime_police` or `legal_court` / query `corridor`, `hallway institutional`, `doors receding` |
| S13 | ✅ | 2 | 引かれたままの椅子 | A single steel chair pulled out from a bolted interrogation table under one hard overhead lamp, the seat empty, long hard shadow across the floor, waiting and accusatory, no people |
| S14 | ✅ | 1 | 主役（匿名・後ろ姿） | A lone anonymous figure seen from behind, seated small at a steel table in a vast dark room, shoulders low, head slightly bowed, face entirely out of frame, one hard overhead light, overwhelming institutional emptiness around them |
| S15 | ✅ | 1 | 扉が閉まる（外側から） | A heavy steel door swinging shut seen from the corridor outside, the lit gap collapsing to a thin line, worn institutional paint and a small dark wired-glass window, finality, no people |

#### 幕2 — 嘘（S16–S30）

| ID | ★SDXL | P | 主題 | プロンプト本文（✅） / factory_query（▫） |
|---|---|---|---|---|
| S16 | ✅ | 1 | 取調官（匿名シルエット） | The silhouette of a standing investigator leaning over a table, seen from behind and below, faceless and backlit, one hand flat on a stack of papers, looming and authoritative, cold blue rim light, no identifiable features |
| S17 | ✅ | 1 | 「証拠」の紙束 | A thick stack of official-looking papers pushed across a steel table under a hard overhead lamp, the top page deliberately blurred and illegible, a faint red stamp impression, symbolic of evidence that does not exist |
| S18 | ✅ | 1 | 空の証拠袋 | An empty clear evidence bag lying open on a dark table, its label blank and illegible, a single cold spotlight, dust in the air, deeply symbolic of nothing inside, minimal and stark |
| S19 | ✅ | 2 | 供述調書の束 | A dense stack of typed statement pages fanned across a dark desk under one lamp, every line deliberately blurred into unreadable grey texture, a fountain pen laid across the top sheet, bureaucratic weight |
| S20 | ✅ | 1 | 時間の経過（壁時計） | A plain institutional wall clock in a dark room, its hands smeared into a long motion-blurred arc implying many hours passing, cold blue light, a lone empty chair below it, exhaustion and duration made visible |
| S21 | ✅ | 1 | 蛍光灯の明滅 | A close-up of a flickering caged fluorescent tube on a stained ceiling, harsh glare blooming into the lens, moths of light, seen from the point of view of someone lying back exhausted, disorienting and relentless |
| S22 | ✅ | 2 | 冷めたコーヒーと灰皿 | A styrofoam cup of cold coffee and an overfilled tin ashtray on a scarred interrogation table, harsh top light, everything grey and stale, the residue of many hours, no people |
| S23 | ✅ | 1 | 録音機／テープ | An old reel-to-reel or cassette recorder on a steel table, its red record light glowing in the dark, tape turning, one shaft of light, symbolic of words being captured forever |
| S24 | ✅ | 2 | 手首の時計と机 | An extreme close-up of a cheap wristwatch lying face up on scarred dark wood beside a bare forearm cropped at the frame edge, the hands reading deep into the small hours, harsh raking light, no face |
| S25 | ✅ | 2 | 観察室（無人） | A dark police observation room behind the one-way glass, one empty swivel chair, a small monitor glowing, a notepad and a cold cup, watching without being watched, no people |
| S26 | ✅ | 2 | 窓のない部屋 | A windowless holding room with water-stained painted cinderblock walls, one bolted steel chair, a floor drain, a caged bulb, the air visibly stale, brutally plain, no people |
| S27 | ✅ | 2 | 疲弊の主観 | A distorted wide-angle upward view of a stained institutional ceiling and glaring light fixture, walls bending inward at the edges of frame, disorienting exhaustion, seen from below, no people |
| S28 | ✅ | 1 | 署名の手 | Anonymous hands holding a pen above a document at the moment before signing, the paper deliberately illegible, hands trembling slightly, one warm lamp against cold darkness, no face, the weight of an irreversible act |
| S29 | ✅ | 1 | 折れた瞬間 | An anonymous figure collapsed forward onto a steel table, arms folded under a lowered head, shot from behind and above so no face is visible, one hard overhead light, total surrender, shoulders only |
| S30 | ✅ | 2 | 運ばれるファイル | Anonymous hands carrying a thick manila file down a dim institutional corridor, the file's label deliberately illegible, motion in the frame, cropped at the shoulders, no face |

#### 幕3 — それは合法だった（S31–S42）

| ID | ★SDXL | P | 主題 | プロンプト本文（✅） / factory_query（▫） |
|---|---|---|---|---|
| S31 | ▫ | 1 | 最高裁 外観 | theme `legal_court` / query `supreme court`, `courthouse exterior`, `marble columns` |
| S32 | ▫ | 1 | 法廷内（無人） | theme `legal_court` / query `courtroom interior`, `judicial bench`, `empty courtroom` |
| S33 | ▫ | 1 | 判例集の書架 | theme `documents_paper` or `legal_court` / query `law books`, `library shelf`, `bound volumes` |
| S34 | ▫ | 2 | 1969年の署内 | theme `documents_paper` / query `filing cabinet`, `vintage office`, `rotary phone` |
| S35 | ▫ | 3 | 輪転機／印刷 | theme `documents_paper` / query `printing press`, `newspaper`, `paper machine` |
| S36 | ▫ | 2 | 判事席（無人） | theme `legal_court` / query `judge bench`, `courtroom wood`, `witness stand` |
| S37 | ▫ | 2 | 引き出される1巻 | theme `documents_paper` / query `book pulled shelf`, `hand book`, `archive` |
| S38 | ✅ | 2 | 「状況の総体」（抽象） | An abstract cinematic image of many separate points of golden light falling onto a black still water surface, each ripple spreading and overlapping into one pattern, symbolic of many circumstances judged as a whole, minimal |
| S39 | ✅ | 2 | 嘘という道具 | An abstract symbolic image of a polished tool laid on black velvet under a single spotlight, ordinary and clinical yet sinister, implying a permitted instrument, cold metal and gold light, minimal |
| S40 | ▫ | 3 | 傍聴席（無人） | theme `legal_court` / query `gallery benches`, `courtroom seats`, `wooden pews` |
| S41 | ▫ | 3 | 大理石の階段と柱 | theme `legal_court` / query `marble staircase`, `colonnade`, `government building interior` |
| S42 | ▫ | 2 | めくれる法典の頁 | theme `documents_paper` / query `pages turning`, `book close up`, `paper flipping` |

#### 幕4 — あなたの番（S43–S50）

| ID | ★SDXL | P | 主題 | プロンプト本文（✅） / factory_query（▫） |
|---|---|---|---|---|
| S43 | ▫ | 1 | 匿名の列（普遍化） | theme `urban_night` or `crime_police` / query `crowd silhouette`, `people waiting line`, `pedestrian silhouettes` |
| S44 | ✅ | 1 | 現代の取調室 | A modern interrogation room lit by flat white LED panels, a small wall-mounted recording camera in the upper corner, laminate table and moulded plastic chairs, clinical and contemporary, no people |
| S45 | ✅ | 1 | 独房の夜 | A bare holding cell at night, a thin mattress on a metal bunk, a small barred window casting a cold blue grid across the floor, completely empty of people, lonely and still |
| S46 | ▫ | 2 | 不在の家庭 | theme `property_home` / query `kitchen night`, `empty chair table`, `home interior lamp` |
| S47 | ✅ | 2 | 面会室 | A prison visitation booth seen head on, scratched acrylic divider, a handset on its hook on each side, two empty moulded stools, harsh overhead light, no people |
| S48 | ▫ | 1 | 釈放の扉／朝 | theme `property_home` or `legal_court` / query `door opening light`, `doorway daylight`, `exit threshold` |
| S49 | ✅ | 1 | 権利の線 | A single stark line of golden light drawn across a dark marble floor, a lone figure standing just behind it seen from far away and from behind, symbolic of the constitutional limit, minimal, contemplative |
| S50 | ▫ | 2 | 現代の街の夜（ED） | theme `surveillance_tech` or `urban_night` / query `surveillance camera`, `city street night`, `cctv` |

**★SDXL = ✅ の30シーン（この30個だけ `ai_prompts.v001.md` に書く）:**
`S01 S02 S03 S05 S08 S09 S13 S14 S15 S16 S17 S18 S19 S20 S21 S22 S23 S24 S25 S26 S27 S28 S29 S30 S38 S39 S44 S45 S47 S49`

**★R2 安全ルール（絶対・例外なし。違反した1枚も台帳に載せるな）**
1. **実在人物の肖像・認識可能な顔を生成しない。**
2. 人物は**後ろ姿・シルエット・顔が画角外・肩から下・手元のみ・遠景の小さな人影**に限る。
3. 暴力・拘束・自傷の直接描写をしない。象徴（閉まる鉄扉・空の椅子・録音機・蛍光灯・時計）に置き換える。
4. **読める判決文・供述調書・実在書式を作らない**（文字は判読不能に）。
5. 未成年の再現画像を作らない。
6. 禁止取得元（YouTube/TikTok/Instagram/X・ニュース番組・TV/映画/アニメ/MV・スポーツ映像・Google画像検索）から何も取得しない。
7. **factory 実写クリップにも同じ基準を適用する。** 目視QCで「顔が識別できる人物が大きく写っている」クリップは `on_theme:false` として除去する（EP39 は R2）。

### 4.3 生成コマンド（**2パス方式・冪等・中断再開可能**）

前提: ローカル A1111 が `http://127.0.0.1:7860` で稼働。**有料APIもアップロードも一切しない。**

**なぜ2パスか:** `--variants 3` を最初から回すと S01 の3枚 → S02 の3枚 … の順に埋まるため、途中で止まると**後半のシーンが1枚も無い**状態になる。先に全30シーンを1枚ずつ埋めれば、**どこで中断しても「30種類の被写体が揃った使える状態」**が保たれる。

```bash
cd C:/Users/aab15/Documents/prime-documentary

# PASS 1: 全30シーンを1枚ずつ（= 30枚）。被写体の網羅を最優先で確保する。
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-039-frazier --variants 1

# PASS 2: 全30シーンを3枚に増やす（= +60枚、合計90枚）。
#         PASS 1 の1枚目は長辺3840なのでスキップされ、二重生成にならない。
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-039-frazier --variants 3

# 中断したらそのまま同じコマンドを再実行してよい（既に長辺>=3840 の PNG はスキップされる）
# 単一シーンだけ作り直す:
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-039-frazier --variants 3 --only S20
```

**このスクリプトの実際の挙動（読んで確認済み）:**
- モデル `juggernautXL_ragnarokBy` / txt2img `1536x864` / steps 34 / cfg 5.5 / sampler `DPM++ 2M Karras`
- hires-fix Latent → `3072x1728`（denoise 0.22 / 2nd pass 16 steps）→ extras `R-ESRGAN 4x+` → **最終 3840x2160**
- シード = `720180 + (hash(stem) % 100000) + v * 9973`
- **冪等**: 出力先の PNG の長辺が既に 3840 以上ならスキップ（`png_long_edge()` L119-126）。**これが再開可能性の根拠。**
- 保存先2箇所: 素材棚 `H:\pd-media\assets\ai\frazier\S01.png` / Remotion 側 `remotion/public/frazier/S01.png`（**`img/` サブフォルダではない点に注意**）
- ファイル名規則: 1枚目 `<stem>.png`、2枚目以降 `<stem>_02.png` / `_03.png`

**優先度順に回したい場合**（P1 → P2 → P3）:
```bash
for S in S01 S02 S03 S08 S09 S14 S15 S16 S17 S18 S20 S21 S23 S28 S29 S44 S45 S49; do
  ./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-039-frazier --variants 3 --only $S
done   # 上が P1 の18シーン。続けて P2 の12シーンを回す。
```

### 4.4 採用画像を `img/` に移す（**必須**）

`check_visual_asset_qc.py` と `gen_depth_maps.py` は **`remotion/public/<slug>/img/`** を見る。生成直後は `remotion/public/frazier/` 直下にあるので、**QCを通した採用分だけ**を `img/` にコピーする。

```bash
mkdir -p remotion/public/frazier/img
# 採用した75枚以上を remotion/public/frazier/img/ にコピー（不採用は入れない）
```

不採用の基準（1つでも該当したら `img/` に入れない・台帳にも載せない）:
- 長辺 < 3840px
- 顔が識別できる／実在人物に似ている（R2違反）
- 判読可能な文字・ロゴ・透かしが写り込んでいる
- 四肢の破綻・重大なアーティファクト
- median luma が極端に低く被写体が潰れている（§4.6 のゲートで落ちる）
- **同一シーン内の他のバリエーションと見分けがつかない**（→ 1枚だけ残す。**バリエーションを無理に3枚残さなくてよい**）

### 4.5 depth map の生成（**忘れるとレンダが落ちる**）

CaseFilm の depth-parallax treatment は、各静止画の隣に `<stem>_depth.png` が無いとレンダー時にクラッシュする（`Could not load .../<stem>_depth.png`）。

```bash
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir remotion/public/frazier/img
```

- モデル `Intel/dpt-large`（初回のみ約1.4GBのダウンロード）
- `*_depth.png` はスキップ対象なので二重生成しない。**既存があればスキップ＝冪等**（`--force` で再生成）
- グレースケール 'L'、元画像と同サイズで書き出す
- **`img/` に画像を追加したら必ず再実行する**（1枚でも depth 欠けがあるとレンダが落ちる）

### 4.6 画像QCゲート（既存スクリプト。自作するな）

```bash
py -3.11 scripts/check_visual_asset_qc.py --ep PD-2026-039-frazier
```

2つの独立サブチェック（`scripts/check_visual_asset_qc.py` を読んで確認済み）:
1. **factory クリップQCマニフェスト必須** → §5.5 で作る
2. **staged still の luma ＋ variety**: `remotion/public/frazier/img/*.png`（`*_depth.png` 除く）について各画像の median luma を測り「暗い」割合が上限を超えたら FAIL。さらに 16x16 ゼロ平均グレースケールのコサイン類似度で近似重複を測り `variety_score = 1 - near_dup_fraction` がフロアを下回ったら FAIL。

**閾値はスクリプト内の定数が唯一の正**（`DARK_LUMA_FLOOR` / `MAX_DARK_FRACTION` / `NEARDUP_SIM` / `MIN_VARIETY`）。値をここに書き写して信じるな。**実行して exit 0 を得ること。** FAIL したら:
- 暗すぎ → そのシーンのプロンプトに `one strong practical light source, clear subject separation, lifted shadows` を足して `--only S<NN>` で再生成
- 近似重複 → 同一シーンのバリエーション同士なら**似ている方を `img/` から外すだけでよい**。**別シーン同士**が似ている場合は被写体・場所・時間帯を実際に変えたプロンプトに書き直す

---

## 5. factory 実写クリップ — **本スレッド最大の工程**

### 5.1 棚の実体

- 実体: `H:/pd-media/assets/factory/backgrounds` に **11,623本**（実写・動いている）
- 索引: リポジトリ直下の **`assets/asset_manifest.v001.json`**（読み取り専用。**書き換え禁止**）
- 各アセット: `id`（`AF-BG-#####`）/ `path`（`H:/pd-media/assets/` からの相対）/ `kind`（image|video）/ `type` / `subtype` / `tags` / `license`

### 5.2 選定（`--exclude-used` を必ず付ける）

```bash
# テーマ一覧と本数を確認
python scripts/select_factory_assets.py --themes

# §4.2 の ▫ 行の factory_query に従って抽出する。例:
python scripts/select_factory_assets.py --theme legal_court     --kind video --limit 40 \
  --exclude-used --ep PD-2026-039-frazier --json
python scripts/select_factory_assets.py --theme crime_police    --kind video --limit 40 \
  --exclude-used --ep PD-2026-039-frazier --json
python scripts/select_factory_assets.py --theme documents_paper --kind video --limit 28 \
  --exclude-used --ep PD-2026-039-frazier --json
python scripts/select_factory_assets.py --theme urban_night     --kind video --limit 28 \
  --exclude-used --ep PD-2026-039-frazier --json
python scripts/select_factory_assets.py --theme property_home   --kind video --limit 20 \
  --exclude-used --ep PD-2026-039-frazier --json
python scripts/select_factory_assets.py --theme surveillance_tech --kind video --limit 16 \
  --exclude-used --ep PD-2026-039-frazier --json
# 個別クエリ（§4.2 の query 語をそのまま使う）
python scripts/select_factory_assets.py --query "corridor" --kind video --limit 20 \
  --exclude-used --ep PD-2026-039-frazier --json
```

`--exclude-used` は `check_arc_nonrepeat.build_universe()` を呼び、**他エピソードで既にカット済み／ステージング済みのクリップを basename で除外する**（`select_factory_assets.py` L27-47）。これを付けないと `arc_nonrepeat` 出荷ゲートを踏む。

**EP39 のテーマ配分（合計110本ステージング）:**

| theme | 本数 | 対応シーン |
|---|---|---|
| `crime_police` | 26 | S10 S11 S12 S43 |
| `legal_court` | 26 | S31 S32 S33 S36 S40 S41 S48 |
| `documents_paper` | 22 | S33 S34 S35 S37 S42 |
| `urban_night` | 20 | S06 S07 S43 S50 |
| `property_home` | 10 | S04 S46 S48 |
| `surveillance_tech` | 6 | S50 |
| **合計** | **110** | |

**除外する subtype（近静止＝紙芝居化するため）:** `texture` `wall` `empty` `still_life` `gradient` `pattern` `backdrop` `fog` `haze` `sky` `clouds` `bokeh` `abstract` `aerial_static` `wallpaper` `surface` `blank` `dark_cinematic_background` `moody_atmosphere` `atmosphere` を名前に含むもの。（既存 `scripts/stage_case_factory_assets.py` の `FEATURELESS` タプルと同一。）

### 5.3 ステージング

`scripts/stage_case_factory_assets.py` は `PLANS` 辞書にスラッグ別の配分を持つ（`hinton` / `forfeiture` / `cotton` / `carsearch` のみ）。**`frazier` のエントリを §5.2 の配分で追加してから実行する。既存キーは変更するな。**

```bash
python scripts/stage_case_factory_assets.py --slug frazier
ls remotion/public/frazier/factory/*.mp4 | wc -l   # 110 であること
```

出力先: `remotion/public/frazier/factory/`（→ `check_asset_reuse.py` の kind 判定で `factory` になる。§3.1）

### 5.4 ★★ factory のラベルは信用できない（**この節を読み飛ばすな**）

**ファイル名と subtype は当てにならない。実測の被害:**

| 話 | ラベル | 実際の中身 |
|---|---|---|
| EP36 williams | `AF-BG-25521__city_surveillance_camera_dome.mp4` | **ベオグラードの正教会大聖堂**（監視カメラではなく宗教建築。冒頭1カット目に入って出荷された） |
| EP38 kidsforcash | `documents_on_desk` ラベルのクリップ | **牛の映像** |
| 過去のQC | `evidence_bag` | 漫画のカウボーイ |
| 過去のQC | `judge_gavel` | 水車小屋 |

**したがって、機械にクリップの中身は判定できない。** `check_visual_asset_qc.py` はこの前提で設計されており、**Pythonで内容を判定しない代わりに、レビュー済みマニフェストの存在を強制する**。

### 5.5 全点目視QC（**110本すべて。約2時間。削るな**）

```bash
# 1) ラベル付きコンタクトシートを作る（1クリップ1フレーム・ファイル名入り）
python scripts/build_footage_contact_sheet.py --ep PD-2026-039-frazier
#    -> runs/qc/frazier_footage_contact_NN.png
# 2) シートを1枚ずつ拡大して全点を目で見る。1フレームで判断がつかないものは実際に再生する。
```

出力: `episodes/PD-2026-039-frazier/05_visuals/factory_clip_qc.v001.json`

```jsonc
{
  "episode_id": "PD-2026-039-frazier",
  "reviewed_at": "2026-07-19",
  "reviewer": "codex-thread-A",
  "clips": [
    {
      "file": "AF-BG-04601__interrogation_room_table.mp4",  // staging ディレクトリ内の実ファイル名（完全一致）
      "saw": "steel table in a dark room, overhead lamp, no people",  // 実際に見えたものを1文で
      "scene_code": "S12",                                   // §4.2 のどのシーンに充てるか
      "reviewed": true,
      "on_theme": true                                       // false のクリップは staging から物理削除する
    }
  ]
}
```

**ルール:**
- **staging 済みの全 `.mp4` がこの JSON に載っていること。** 1本でも欠けると FAIL（未レビュー扱い）。
- `on_theme: false` にしたクリップは **`remotion/public/frazier/factory/` から物理的に削除する**（false のまま残すのも FAIL）。
- `saw` は「ファイル名を言い換えたもの」ではなく**実際にフレームで見たもの**を書く。ここが EP36 の失敗点であり、この欄が唯一の防御。
- **顔が識別できる人物が大きく写っているクリップは `on_theme:false`**（EP39 は R2）。
- 判定後に残った本数が **90本以上**であること。下回ったら §5.2 に戻って追加抽出し、再度シートを作って見る。

```bash
py -3.11 scripts/check_visual_asset_qc.py --ep PD-2026-039-frazier   # exit 0 になるまで
```

### 5.6 合成レイヤーのステージング（**カットに数えない・静止画を別物に見せるため**）

在庫: `light_assets` 1,401 / `particle_assets` 1,225 / `vfx_overlays` 1,196 / `loops` 454。
**同じ静止画の上に別のレイヤーを重ねれば、視聴者には別のカットに見える。** 枚数を増やすより安い反復対策。

```bash
python scripts/select_factory_assets.py --category light_assets    --kind video --limit 15 \
  --exclude-used --ep PD-2026-039-frazier --json
python scripts/select_factory_assets.py --category particle_assets --kind video --limit 15 \
  --exclude-used --ep PD-2026-039-frazier --json
python scripts/select_factory_assets.py --category vfx_overlays    --kind video --limit 10 \
  --exclude-used --ep PD-2026-039-frazier --json
```

- 出力先: **`remotion/public/frazier/overlay/`**（`factory/` にも `motion/` にも置くな）
- 選定基準: 埃・光条・煙・粒子・フィルムグレイン・レンズフレア・光漏れ。**具体的な被写体が写っているものは選ばない**（重ねると絵が二重になる）
- **台帳では `assets` ではなく `overlays` セクションに書く**（§7.3）。`cuts[].src` に入らないので `check_asset_reuse` の対象外
- 目標 **30点以上**

---

## 6. i2v モーション（Wan 2.2 A14B）— 手順

### 6.1 雛形

`scripts/comfy_wan_kidsforcash.py` を**必ず先に読んでから**、EP39 用に `scripts/comfy_wan_frazier.py` を新規作成する。**EP38版を書き換えるな。**

雛形との重要な差分:
- EP38版は `04_scenes/shotlist.v001.json` を入力にしている（`wan == true` のショットを拾う）。**shotlist は台本依存＝このスレッドでは存在しない。**
- → **EP39版は shotlist を読まない。** 入力は §6.3 の固定リスト（静止画IDのハードコード配列）にする。これで台本を待たずに走れる。

### 6.2 Known-good レジストリ（`docs/42_AI_MOTION_PIPELINE_HARDENING_AND_GATES.md` §5。数値を変えるな）

| 項目 | 値 | 備考 |
|---|---|---|
| high-noise expert | `wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors` | |
| low-noise expert | `wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors` | |
| VAE | `wan_2.1_vae.safetensors` | **2.1。2.2 ではない** |
| CLIP | `umt5_xxl_fp8_e4m3fn_scaled.safetensors` | |
| 解像度 | `1280 x 720` | |
| フレーム数 | **41** | 4090フルロードの上限。81にすると部分ロードで3倍遅くなる |
| steps | 40 | |
| expert 切替 | step **20**（50%） | |
| **shift** | **5.0** | ★8.0 は 5B からの無言の持ち越し。**必ず 5.0** |
| cfg | 3.5 | |
| sampler / scheduler | `euler` / `simple` | |
| fps（会計用） | 16 | |
| ホスト | `http://127.0.0.1:8188`（ローカル ComfyUI） | 有料APIなし |

**ネガティブプロンプト（固定）:**
```
static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, text, watermark, identifiable face, real person likeness
```

### 6.3 動かす22枚（**§4.2 の ✅ SDXLシーンから、動きが意味を持つものだけ**）

選定基準: **煙・水・雨・光の変化・機械の回転・人の微細な動き**が絵の意味そのものになるショット。人物が大きく写る絵は morph するので避ける。
▫（factory）のシーンは**既に実写で動いている**ので i2v にかけない。

| # | 元画像 | モーション prompt（positive に足す） |
|---|---|---|
| 1 | `S02.png` | the heavy steel door slowly swings closed, the blade of corridor light narrowing across the floor |
| 2 | `S15.png` | the door swings shut from the outside, the lit gap collapsing to a thin line |
| 3 | `S17.png` | a hand slides the stack of papers slowly across the steel table toward camera |
| 4 | `S20.png` | the clock hands sweep forward, light shifting across the wall as hours pass |
| 5 | `S21.png` | the fluorescent tube stutters and flickers, glare pulsing into the lens |
| 6 | `S23.png` | the tape reels turn steadily, the red record light pulsing in the dark |
| 7 | `S01.png` | slow lateral dolly across the empty interrogation room, light shifting on the table |
| 8 | `S03.png` | reflections drift across the one-way mirror as the lit room beyond stays still |
| 9 | `S09.png` | streetlights slide past the cruiser window, the cage bars steady in the foreground |
| 10 | `S14.png` | the seated figure shifts almost imperceptibly, shoulders sinking lower, camera creeps closer |
| 11 | `S19.png` | pages riffle and settle, the pen rocking slightly on the top sheet |
| 12 | `S27.png` | the ceiling light glare pulses and the walls breathe inward, disorienting drift |
| 13 | `S30.png` | the file is carried down the corridor, light and shadow sliding across the manila cover |
| 14 | `S38.png` | points of golden light fall onto the black water, ripples spreading and overlapping |
| 15 | `S44.png` | the recording camera LED blinks, flat LED light humming, faint air movement in the empty room |
| 16 | `S45.png` | the barred window light bar crawls slowly across the cell floor |
| 17 | `S49.png` | the line of golden light brightens and widens slowly across the marble floor |
| 18 | `S08.png` | the silhouettes behind the frosted glass shift and one raises a hand to knock |
| 19 | `S25.png` | the monitor glow flickers in the dark observation room, faint reflections on the glass |
| 20 | `S26.png` | the caged bulb sways almost imperceptibly, its shadow crawling across the cinderblock |
| 21 | `S13.png` | slow push in on the empty chair, the hard shadow lengthening across the floor |
| 22 | `S28.png` | the pen lowers toward the page, the hand trembling, lamp light wavering |

### 6.4 実行と検収

```bash
# 1) グラフだけ書く（GPU・ネットワークに触らない。まず目で確認する）
py -3.11 scripts/comfy_wan_frazier.py --build

# 2) 実行（ローカル ComfyUI にキュー投入）。1本あたり実測 24–73 GPU分。22本で 9–27時間。
py -3.11 scripts/comfy_wan_frazier.py --run --shot S02
```

**バッチ実行は `scripts/queue_wan_batch.py` の構造を踏襲した EP39 版を新規に書く**（`scripts/queue_wan_frazier_batch.py`）。EP38版は `SHOTS` と `DRIVER` がハードコードされているので**書き換えるな**。踏襲すべき挙動:
- 1本ずつドライバをサブプロセス起動し、stdout から `prompt_id=` を拾う
- `GET /queue` を30秒間隔でポーリングし `queue_running` と `queue_pending` が両方0になるまで待つ
- 完了後 `GET /history/<prompt_id>` で出力フレーム数を数え、**40フレーム未満は失敗扱い**
- **中断・再開可能にする**: 出力 mp4 が既に存在し 41フレーム以上あるショットは queue に入れずスキップする（冪等）
- **表の上から順に投入する**（表の並びが優先度順。途中で止めても強いショットから揃う）

出力先: `H:\pd-media\assets\ai_video\frazier\<SHOT>.mp4` → 採用分を **`remotion/public/frazier/motion/`** にコピー

**検収（1本ずつ）:**
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,nb_frames,r_frame_rate \
  -of default=nw=1 remotion/public/frazier/motion/S02.mp4
```
- 幅×高さ ≥ 1280x720 / フレーム数 ≥ 41
- 目視: 顔の morph・チラつき・warp が無い（あればそのショットは不採用）

**採用18本以上**にならなければ ✅ シーンの未使用分（S05 / S16 / S18 / S22 / S24 / S29 / S39 / S47）から追加生成する。

---

## 7. 境界契約: `asset_manifest.v001.json`（**このスレッドの最終成果物**）

### 7.1 パス

```
C:\Users\aab15\Documents\prime-documentary\episodes\PD-2026-039-frazier\05_visuals\asset_manifest.v001.json
```

（再掲・重要: リポジトリ直下の `assets/asset_manifest.v001.json` は**別物・読み取り専用**。混同するな。）

### 7.2 ディレクトリ規則（この配置が kind 判定そのもの）

| kind | 置き場所（`remotion/public/` からの相対） | `check_asset_reuse.py` の判定根拠 |
|---|---|---|
| `still` | `frazier/img/<name>.png` | `.mp4/.mov/.webm` でなく `/factory` も含まない → still |
| `factory` | `frazier/factory/<name>.mp4` | パスに `/factory` を含む → factory（cap 1） |
| `motion` | `frazier/motion/<name>.mp4` | `.mp4` で終わり `/factory` を含まない → motion（cap 2） |
| （overlay） | `frazier/overlay/<name>.mp4` | **`cuts[].src` に入れないのでゲートの対象外** |

> **⚠ 混ぜるな:** i2v の mp4 を `frazier/factory/` に置くと factory（cap 1）扱い。factory クリップを `frazier/motion/` に置くと無料素材を2回使う設計になる。オーバーレイを `factory/` に置くと distinct 数を水増しする不正になる。**ディレクトリを厳密に分けること。**

### 7.3 スキーマ（**このとおりに書く。フィールドを増やすな・減らすな**）

```jsonc
{
  "episode_id": "PD-2026-039-frazier",
  "manifest_version": "v001",
  "generated_at": "2026-07-19T21:00:00+09:00",   // ISO8601
  "status": "final",                              // "partial" は作業中のみ。納品は "final"
  "producer": "codex-thread-A",
  "counts": { "still": 78, "factory": 93, "motion": 19, "total": 190,
              "overlays": 34, "distinct_scene_codes": 50 },
  "caps": { "still": 2, "factory": 1, "motion": 2 },   // check_asset_reuse.py の CAPS と一致させる
  "assets": [
    {
      "asset_id": "ST-039-001",          // ^(ST|FC|MO)-039-[0-9]{3}$  通し・欠番禁止・重複禁止
      "kind": "still",                    // "still" | "factory" | "motion"
      "max_uses": 2,                      // still=2 / factory=1 / motion=2。caps と必ず一致
      "public_path": "frazier/img/S01.png",                       // remotion/public/ からの相対。film.json の src にそのまま入る
      "abs_path": "C:/Users/aab15/Documents/prime-documentary/remotion/public/frazier/img/S01.png",
      "source_path": "H:/pd-media/assets/ai/frazier/S01.png",     // 素材棚の originals。無ければ null
      "scene_code": "S01",                // ★全kind必須。§4.2 の50シーンのどれに充てるか
      "act": 0,                            // 0=hook/主舞台 1|2|3|4=幕。§4.2 の見出しに対応
      "variant": 1,                        // still のバリエーション番号 1..3。factory/motion は null
      "depth_map": "frazier/img/S01_depth.png",   // still のみ必須。factory/motion は null
      "width": 3840,
      "height": 2160,
      "long_edge_px": 3840,               // still は 3840 以上必須
      "duration_sec": null,               // factory/motion 必須（小数2桁）。still は null
      "fps": null,                         // factory/motion 必須。still は null
      "frames": null,                      // motion 必須（41以上）。それ以外 null
      "sha256": "…64hex…",                // public_path の実ファイルのハッシュ
      "bytes": 8123456,
      "median_luma": 41.2,                // still のみ（0-255）。factory/motion は null
      "af_id": null,                       // factory のみ "AF-BG-04601"。それ以外 null
      "theme": null,                       // factory のみ "legal_court" 等。それ以外 null
      "subtype": null,                     // factory のみ。それ以外 null
      "saw": null,                         // ★factory のみ必須。目視で実際に見えたもの1文（§5.5 と同一文字列）
      "tags": ["interrogation", "night", "empty_room"],   // 1件以上。Bの割り当てヒント
      "source": "sdxl_juggernautXL",      // "sdxl_juggernautXL" | "factory_shelf" | "wan22_a14b_i2v"
      "license": "internal_generated",     // "internal_generated" | "commercial_ok"
      "reviewed": true,                    // factory は目視QC済み。still/motion も true にする
      "on_theme": true,                    // factory の目視判定。still/motion は true
      "qc": { "pass": true, "notes": "" }, // pass=false のものは台帳に載せない
      "stub": false                        // 本番素材は必ず false（true は B のダミー台帳専用）
    }
  ],
  "overlays": [
    {
      "overlay_id": "OV-039-001",         // ^OV-039-[0-9]{3}$
      "category": "light_assets",          // "light_assets" | "particle_assets" | "vfx_overlays" | "loops"
      "public_path": "frazier/overlay/AF-LT-00123__dust_motes.mp4",
      "duration_sec": 8.40,
      "fps": 30,
      "blend_hint": "add",                 // "add" | "screen" | "overlay"
      "sha256": "…64hex…",
      "af_id": "AF-LT-00123"
    }
  ]
}
```

**Bはこの台帳のうち `qc.pass == true && stub == false` の要素だけを `cuts[].src` に使う。** `overlays` は合成レイヤーとして別に使い、**distinct 数には数えない。**
**`scene_code` / `act` / `tags` は B が「幕に合った絵」を割り当てるための唯一の手がかり**なので必ず正確に埋めること。

### 7.4 自己検査（納品前に必ず実行する）

`scripts/validate_frazier_asset_manifest.py` を新規に書き、以下を **assert** で落とす（print で流すな）:

1. `episode_id == "PD-2026-039-frazier"` かつ `status == "final"`
2. `asset_id` が `^(ST|FC|MO)-039-\d{3}$` に一致し、重複が無い
3. `kind` 別件数: **factory ≥ 90 / still ≥ 75 / motion ≥ 18**
4. **`scene_code` の distinct 数 ≥ 45**（全kind合算。★最重要）
5. 全レコードで `scene_code` が非 null かつ §4.2 の `S01`–`S50` のいずれか
6. 同一 `scene_code` の still が **4件以上ある場合は WARN**（バリエーション過多）
7. `max_uses` が kind と一致（still 2 / factory 1 / motion 2）
8. 全 `public_path` が `remotion/public/` 配下に実在
9. `sha256` を実ファイルから再計算して一致
10. still: `long_edge_px >= 3840` かつ `depth_map` が実在
11. factory: `public_path` が `frazier/factory/` で始まり、`reviewed && on_theme`、かつ **`saw` が非空**
12. motion: `public_path` が `frazier/motion/` で始まり、`frames >= 41` かつ `width >= 1280`
13. overlays: **30件以上**、全て `public_path` が `frazier/overlay/` で始まる
14. 全件 `qc.pass == true` かつ `stub == false`
15. `counts` が実際の件数と一致（`overlays` / `distinct_scene_codes` を含む）
16. **配分の検算**: `factory×1 + still×2 + motion×2 >= 226` かつ
    `(factory + still + motion) / 226 >= 0.70` が成立すること

**この検査を通してから完了報告すること。**

---

## 8. 禁止事項

- **有料ジョブを起動しない**（ElevenLabs / クラウドAPI / アップロード）。SDXL・Wan・DPTは全部ローカル。
- **YouTube へのアップロード・公開予約をしない**（オーナー専管）。
- **出荷済みファイルを上書きしない。**
- **リポジトリ直下の `assets/asset_manifest.v001.json` を書き換えない。**
- **`scripts/stage_case_factory_assets.py` / `scripts/queue_wan_batch.py` / `scripts/comfy_wan_kidsforcash.py` の既存エントリを書き換えない**（`PLANS` に `frazier` キーを**追加**するのは可）。
- **`remotion/src/**` と `scripts/ae/**` に一切触らない**（スレッドBの担当領域）。図解・トランジション・タイポの在庫が0本でも、あなたが作らない。
- **`05_visuals/asset_manifest.stub.v001.json` に触らない**（スレッドBの持ち物）。
- **実在しないスクリプト名・テンプレ名を使わない。** 使う前に必ずファイルを読んで実在を確認する。
- **自作の品質ゲートを書いて「合格」と宣言しない。** 既存 `check_*.py` の測定結果のみが合否。
- **実在人物の肖像を生成しない。**
- **factory の全点目視QCを省略しない。** ファイル名・subtype・過去の記憶を根拠に `on_theme:true` と書かない。**見たものだけ書く。**
- **SDXL指定（✅）の30シーンを factory で代用しない。**
- **合成レイヤーを `assets` に混ぜて distinct 数を水増ししない。**

---

## 9. 完了報告に必ず含めること

1. `asset_manifest.v001.json` の絶対パスと `counts`（factory / still / motion / total / **overlays** / **distinct_scene_codes**）の実数
2. `scripts/validate_frazier_asset_manifest.py` の実出力（全16項目のPASS。特に項目16の配分検算）
3. **factory**: ステージング本数 / 目視した本数 / `on_theme:false` にして削除した本数と**その具体例（ラベルと実際に見えたもの）** / 最終残存本数 / QCに要した実時間
4. `py -3.11 scripts/check_visual_asset_qc.py --ep PD-2026-039-frazier` の**実際の標準出力**（exit code 付き）
5. **SDXL**: シーン数 / 生成枚数 / 採用枚数 / 長辺の最小値 / R2違反で落とした枚数
6. **i2v**: 生成本数 / 採用本数 / 各本の ffprobe 実出力（width x height / frames）/ 総GPU時間
7. depth map の生成枚数と `img/` の PNG 枚数が一致していること
8. 合成レイヤーのステージング点数とカテゴリ内訳
9. 作成／変更したファイルの絶対パス一覧
10. 未達の項目があれば、その数値と原因（推測ではなく実測値で）
</content>
