# AUDIT — 実在性監査 v001（EP39 frazier / EP40 lech）

- 監査日: 2026-07-20
- レンズ: **実在性**（設計書が言及する「モノ」が実機に本当に存在するか）
- 監査対象: `episodes/_planning/` 配下の6ファイル
  - `EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md`（正典）
  - `EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md`（正典）
  - `EP39_frazier_CODEX_A_ASSETS.v001.md` / `EP39_frazier_CODEX_B_BUILD.v001.md`
  - `EP40_lech_CODEX_A_ASSETS.v001.md` / `EP40_lech_CODEX_B_BUILD.v001.md`
- 正誤の基準: v002 ＋ 確定台本（`EP39_frazier_script.en.v001.md` / `EP40_lech_script.en.v001.md`）＋ **実機のコード**
- **ファイルは一切修正していない。報告のみ。**

## 集計

| 深刻度 | 件数 |
|---|---|
| BLOCKER | **8** |
| MAJOR | 5 |
| MINOR | 3 |

---

# BLOCKER

## B-1 【EP40 v002】FigureSpec の `kind` が全て実在しない大文字表記に**先祖返り**している

- **ファイル/位置:** `EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md` L1078–1086（§10.1 種類の配分の表）、および L98（§0.4 R1）、L339
- **何が誤りか:**
  v002 §10.1 は `figures[]` に入れる kind として `ActTitle` / `ComparisonBars` / `QuoteCard` / `MechanismReveal` / `PinDropMap` を指定している。
  **`FigureBeats.tsx` の `FigureSpec` union に、この5つは1つも存在しない。全て小文字の別名である。**
  discriminated union なので TypeScript の型エラーにはなるが、`lech_film.json` は `as unknown as FilmData` でキャストされて流し込まれるため型検査を素通りし、**実行時は該当 kind の JSX が1つも真にならず、無言で何も描画されない**（過去の実害と完全に同型）。

  さらに悪いのは、**この誤りは EP40_lech_CODEX_B_BUILD.v001.md §6.2 で既に明示的に訂正済み**である点。v002 はその訂正を取り込まず旧表記に戻している。

  B_BUILD.v001.md L771–773（引用）:
  > **旧設計書は存在しない kind 名を書いていた。**
  > `ActTitle` / `MechanismReveal` / `QuoteCard` / `ComparisonBars` / `RouteMap` / `PinDropMap` は
  > **`FigureBeats.tsx` に存在しない。そのまま書くと描画されない（無言で消える）。**

- **実行したコマンドと出力:**

```
$ cd remotion/src/components && grep -oE "kind: '[a-zA-Z_]+'" FigureBeats.tsx | sort -u
kind: 'acttitle'
kind: 'arrow'
kind: 'bar'
kind: 'brightline'
kind: 'burdenflip'
kind: 'carcutaway'
kind: 'carkeylock'
kind: 'casetimeline_c'
kind: 'cashstack'
kind: 'compbars'
kind: 'convergemap'
kind: 'curtilage'
kind: 'dochighlight'
kind: 'equitytheft'
kind: 'govtargument'
kind: 'hallladder'
kind: 'highlightring'
kind: 'hinders'
kind: 'kinetic'
kind: 'lowerthird'
kind: 'mechanism'
kind: 'numberticker'
kind: 'oralargtally'
kind: 'pindropmap'
kind: 'probablecause'
kind: 'quote'
kind: 'regionmap'
kind: 'returnledger'
kind: 'routemap'
kind: 'signswap'
kind: 'splitladder'
kind: 'spotlight'
kind: 'stat'
kind: 'statemap'
kind: 'thresholdmeter'
kind: 'timeline'
kind: 'votetally'
kind: 'xrayscan'
```
（`ActTitle` / `ComparisonBars` / `QuoteCard` / `MechanismReveal` / `PinDropMap` は**0件**）

```
$ ./.venv/Scripts/python.exe -c "import json,collections; d=json.load(open('remotion/src/data/lech_film.json',encoding='utf-8')); print(collections.Counter(f['kind'] for f in d['figures']))"
Counter({'lowerthird': 4, 'stat': 3, 'quote': 3, 'mechanism': 3, 'compbars': 2, 'routemap': 1, 'kinetic': 1})
```
→ 実データは全て小文字。v002 の表記でビルドしたら全滅する。

- **具体的な修正文字列（v002 §10.1 の表の kind 列）:**

| v002 の誤り | 正しい実在値 |
|---|---|
| `ActTitle` | `acttitle` |
| `ComparisonBars` | `compbars` |
| `QuoteCard` | `quote` |
| `MechanismReveal` | `mechanism`（★変種は別フィールド `mechanism: 'closingdoor' \| 'gears' \| 'faultsplit'` に入れる） |
| `PinDropMap` | `pindropmap` |

L339 の `` `MechanismReveal` 4枠 `` も `` `mechanism` 4枠 `` に。
（`timeline` / `stat` は既に正しい。触るな。）

---

## B-2 【EP40 v002】`figures[].text` は存在しないフィールド → accuracy_lock が**無言で何も検査しない**

- **ファイル/位置:** `EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md` L94（対象パス一覧）、L98（R1）、L1099（§10.2-6）
- **何が誤りか:**
  v002 は accuracy_lock の検査対象として `figures[].text` と `figures[].lines[]` を指定している。
  **`FigureSpec` に `text` フィールドを持つ variant は1つも存在しない。** 実在するテキスト保持フィールドは:
  - `acttitle` → `title` / `kicker`
  - `quote` → **`quote`** / `attribution`
  - `lowerthird` → `primary` / `secondary`
  - `kinetic` → `lines[]`
  - `stat` / `numberticker` → `label` / `topLabel`

  つまり v002 §10.2-6 が「`QuoteCard` の引用文は accuracy_lock 検査対象（`figures[].text` を対象パスに含める）」と書いている当の引用文（`quote` フィールド）は、**指定どおり実装しても1文字も検査されない**。ゲートは0件で PASS を返す＝偽グリーン。

  実装済みの `scripts/check_lech_accuracy.py` の ZONE_KEYS は既に `figures.title` / `figures.primary` / `figures.label` を持つが、**`figures.quote` と `figures.lines` が欠けている**。

- **実行したコマンドと出力:**

```
$ grep -nE "kind: 'quote'|kind: 'acttitle'|kind: 'kinetic'" -A3 remotion/src/components/FigureBeats.tsx
72:  | {start: number; end: number; kind: 'quote'; quote: string; attribution: string}
79:      kind: 'kinetic';
80:      lines: string[];
84:  | {start: number; end: number; kind: 'acttitle'; title: string; kicker?: string; index?: number}

$ grep -n "ZONE_KEYS" -A5 scripts/check_lech_accuracy.py
25:ZONE_KEYS = {
26:    "title_candidates", "thumb_headlines", "hook.lines", "beats.top", "beats.bottom",
27:    "ed.cta_line", "package.title", "figures.title", "figures.primary",
28:    "figures.label", "props.subtitle", "subtitle", "title", "top", "bottom",
29:}
```
（`figures.text` はコードにも存在しない。`figures.quote` / `figures.lines` も無い）

- **具体的な修正文字列:**
  - v002 L94 の `` `figures[].text` / `figures[].lines[]` `` → `` `figures[].title` / `figures[].primary` / `figures[].label` / `figures[].quote` / `figures[].lines[]` ``
  - v002 L98 の `` `figures[].text`（`ActTitle` kind のみ）`` → `` `figures[].title`（`acttitle` kind のみ）``
  - v002 L1099 の `` `figures[].text` を対象パスに含める `` → `` `figures[].quote` を対象パスに含める ``
  - `scripts/check_lech_accuracy.py` L27–28 の ZONE_KEYS に `"figures.quote", "figures.lines"` を追加

---

## B-3 【EP40】v002 の 28枠でも B_BUILD の 17枠でも `check_motion_density` は**FAIL する**（実測）

- **ファイル/位置:**
  - `EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md` L1072（見出し「Remotion MGビート 28枠 — AEの8枠と合わせて36枠」）、L1100–1109（§10.3 密度の最終検算）
  - `EP40_lech_CODEX_B_BUILD.v001.md` L33 / L749 / L751–758（§6.1 密度の検算「AE 23 + Remotion 17 = 40 → 3.24/分 ✓」）
- **何が誤りか:**
  両方の検算が **AEカードを分子に足している**。しかし `check_motion_density.py` が数えるのは `<slug>_film.json` の **`graphics[] + figures[] + heroCuts[]` だけ**。AEカードは Remotion レンダ後に ffmpeg で焼き込む別工程で、`lech_film.json` には1件も入らない。したがって:

  - v002 案（figures 28）: 28 / 12.01分 = **2.33/分 < 2.5 → FAIL**。coverage も 28×5.5秒=154秒 = 21.4% < 25% → FAIL。
  - B_BUILD 案（figures 17）: 17 / 12.01分 = **1.42/分 → FAIL**（現に実ビルド済みファイルが FAIL している）

  **どちらの仕様に従っても出荷できない。** これが本監査で最も重い1件。

- **実行したコマンドと出力:**

```
$ ./.venv/Scripts/python.exe scripts/check_motion_density.py --ep lech
  film json   : ...\remotion\src\data\lech_film.json
  episode     : PD-2026-040-lech
  density     : 1.42/min   (floor 2.5)
  coverage    : 13.7%    (floor 25%)
  variety     : 7 forms   (floor 3)
  beats       : 17  [0 typo / 17 figures / 0 hero3d]  vs 226 Ken-Burns cuts
  RESULT: FAIL  — premium animation too sparse (紙芝居 risk): kinetic-beat density
  1.42/min < 2.5 (17 beats over 12.0min); animated coverage 13.7% < 25%
```

ゲートの分子の定義（`scripts/check_motion_density.py` L179–185・引用）:
```
    A "premium kinetic beat" = a graphics typography beat, an animated figure,
    or a 3D heroCut. Plain cuts[] (Ken-Burns/parallax/depth over stills) are NOT counted.
    graphics = film.get("graphics") or []
    figures  = film.get("figures") or []
    heroes   = film.get("heroCuts") or []
    beats = n_g + n_f + n_h
```

各案の実測換算:
```
$ ./.venv/Scripts/python.exe -c "..."
lech: narrationSeconds=720.8 body_min=12.01
   figures=17 -> 1.42/min  FAIL (floor 2.5)
   figures=28 -> 2.33/min  FAIL (floor 2.5)
   figures=40 -> 3.33/min  PASS (floor 2.5)
EP40 v002 plan: 28 x 5.5s = 154.0 s -> 21.4 % vs floor 25%
```

- **具体的な修正文字列:**
  - v002 §10 見出し → `# 10. Remotion MGビート **34枠**（`figures` 契約）— ゲートの分子に入るのは Remotion の figures だけ。AEの8枠は `lech_film.json` に入らないので**分子に足すな**`
  - v002 §10.3 の検算ブロックを次に置換:
    ```
    check_motion_density の分子 = lech_film.json の graphics[] + figures[] + heroCuts[] のみ
    （AEカードは合成工程なので分子に入らない）

    figures 34枠 / 12.01分 = 2.83/分     ✓ ≥2.5
    coverage  34枠 × 平均6.0秒 = 204秒 / 720.8秒 = 28.3%   ✓ ≥25%
    variety   7 kind                     ✓ ≥3
    ```
  - v002 §10.2-4「1枠の長さは 4.0–8.0秒」→ **「1枠の長さは 5.5–8.0秒（平均6.0秒。coverage 25%フロアの直接の入力）」**
  - B_BUILD.v001 §6.1 の検算ブロックも同様に AE 23 を分子から外し、figures を 17 → 34 に増やす

---

## B-4 【EP40】`validate_lech_beats.py` が v001 の枠数（AE 23 / figures 17）を**ハードコード**しており、v002 に従うと必ず FAIL する

- **ファイル/位置:** `scripts/validate_lech_beats.py` L54–55, L131–132 vs `EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md` L751（「§9 After Effects ヒーロービート（8枠）」）/ L1072（figures 28枠）
- **何が誤りか:**
  v002 は AE 8枠・Remotion 28枠。ところが Codex が既に実装済みのバリデータは 23 と 17 を定数で持っている。v002 の枠数でデータを作った瞬間、`beats_count` と `figures_count` の2件で機械的に FAIL する。v002 側にこのバリデータを直す指示が無い。
- **実行したコマンドと出力:**

```
$ grep -nE "len\(beats\) != |len\(figures\) != " scripts/validate_lech_beats.py
54:    if len(beats) != 23:
55:        violations.append({"rule": "beats_count", "actual": len(beats), "expected": 23})
131:    if len(figures) != 17:
132:        violations.append({"rule": "figures_count", "actual": len(figures), "expected": 17})
```
- **具体的な修正文字列:** v002 §9 / §10 に次の1行を追加せよ —
  「**`scripts/validate_lech_beats.py` L54 の `!= 23` を `!= 8` に、L131 の `!= 17` を `!= 34` に更新すること。この2定数を直さない限り v002 の枠数は必ず FAIL する。**」

---

## B-5 【EP40】accuracy_lock R2 の実装が **1文窓のまま**で、確定台本を誤って FAIL させる（v002 が「使うな」と名指しした v001 版）

- **ファイル/位置:** `scripts/check_lech_accuracy.py` L18–21（ALLOWED_CONTEXT）/ L86–88（1文窓ループ） vs `EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md` L100–110（§0.4 R2）
- **何が誤りか:**
  v002 §0.4 R2 は明示的に「**★2文窓。v001 の1文窓は誤検知するので使うな**」と書き、ALLOWED_CONTEXT に `denial of review` / `it declined` / `expressed no view` / `petition` を追加した版を指定している。
  ところが実装済みのゲートは **1文窓のまま**、正規表現も v001 版（`petition` / `denial of review` / `it declined` / `expressed no view` を含まない）。
  現在このゲートは「PASS」を返すが、それは**確定台本がまだ `03_script/` に配置されていないから**（3パターン skip）。台本を置いた瞬間に2件の偽FAILが出る。
- **実行したコマンドと出力:**

```
$ ./.venv/Scripts/python.exe scripts/check_lech_accuracy.py
PASS lech_accuracy: 0 violation(s), 3 skipped pattern(s)      ← 台本未配置による偽グリーン

$ ./.venv/Scripts/python.exe -c "<check_lech_accuracy.py を import し、確定台本に対して同じ1文窓ロジックを適用>"
R2 violations with SHIPPED 1-sentence window: 2
  - 〔CARD: $5,000〕 That figure appears in the family's own petition to the Supreme Court, described in those words, as help with temporary living expenses
  - He asked the Supreme Court to take the case.
```
（v002 が予告した "He asked the Supreme Court to take the case." がそのまま再現。加えて `petition` 文も落ちる）

```
$ sed -n '18,21p;86,88p' scripts/check_lech_accuracy.py
ALLOWED_CONTEXT = re.compile(
    r"declined to hear|refused to hear|denied review|did not take the case|"
    r"cert(iorari)?\s+(was\s+)?denied|let the ruling stand|never ruled on",
    re.IGNORECASE,
)
    for s in sentences(text):
        if re.search(r"Supreme\s+Court", s, re.IGNORECASE) and not ALLOWED_CONTEXT.search(s):
            violations.append({"file": str(path), "rule": "R2_context", "sentence": s})
```

- **具体的な修正文字列（`scripts/check_lech_accuracy.py`）:**
  - L18–21 を v002 §0.4 の正規表現に置換:
    ```python
    ALLOWED_CONTEXT = re.compile(
        r"declined to hear|refused to hear|denied review|denial of review|"
        r"did not take the case|cert(iorari)?\s+(was\s+)?denied|let the ruling stand|"
        r"never ruled on|it declined|expressed no view|petition", re.IGNORECASE)
    ```
  - L86–88 を2文窓に:
    ```python
    ss = sentences(text)
    for i, s in enumerate(ss):
        if re.search(r"Supreme\s+Court", s, re.IGNORECASE):
            window = s + " " + (ss[i + 1] if i + 1 < len(ss) else "")
            if not ALLOWED_CONTEXT.search(window):
                violations.append({"file": str(path), "rule": "R2_context", "sentence": s})
    ```

---

## B-6 【EP39】v002 が指示する AE スクリプト名が実在せず、Codex が既に**別名で実装済み**

- **ファイル/位置:** `EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md` L561（C6）/ L662（引き継ぎプロンプト本文）/ L566（C11）
- **何が誤りか:**
  v002 は `scripts/ae/build_frazier_hero_jsx.py` と `scripts/ae/composite_frazier_hero.py` を作れと指示している。
  しかし Codex は B_BUILD.v001 の指示に従って **`build_frazier_ae_jsx.py` / `composite_frazier_ae.py`** を既に実装済み。v002 の名前のファイルはディスク上に存在しない。v002 をそのまま読むと**同じ機能の2本目を別名で作る**か、存在しないファイルを実行して落ちる。
- **実行したコマンドと出力:**

```
$ ls -la scripts/ae/ | grep -iE "frazier"
-rwxr-xr-x 1 aab15 197609  9303 Jul 20 01:07 build_frazier_ae_jsx.py
-rwxr-xr-x 1 aab15 197609  4072 Jul 20 01:07 composite_frazier_ae.py

$ test -f scripts/ae/build_frazier_hero_jsx.py; echo $?
1     （= 存在しない）
$ test -f scripts/ae/composite_frazier_hero.py; echo $?
1     （= 存在しない）

$ grep -n "build_frazier_ae_jsx\|composite_frazier_ae" episodes/_planning/EP39_frazier_CODEX_B_BUILD.v001.md
425:- `scripts/ae/build_frazier_ae_jsx.py`
426:- `scripts/ae/composite_frazier_ae.py`
621:py -3.11 .../scripts/ae/build_frazier_ae_jsx.py --validate
633:py -3.11 .../scripts/ae/composite_frazier_ae.py \
892:6. `build_frazier_ae_jsx.py --validate` → AEビルド → aerender → `composite_frazier_ae.py` → `v003_ae.mp4`
```

- **具体的な修正文字列:** v002 L561 / L566 / L662 の
  `scripts/ae/build_frazier_hero_jsx.py` → **`scripts/ae/build_frazier_ae_jsx.py`**
  `scripts/ae/composite_frazier_hero.py` → **`scripts/ae/composite_frazier_ae.py`**
  （実装済みの2本を正とする。新規作成の指示は削除し「既存を拡張する」に変えること）

---

## B-7 【EP39】v002 §10.2 の `factory_query` に**存在しない theme 名が4つ**あり、0件ヒットで無言に終わる

- **ファイル/位置:** `EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md` §10.2 の表 — S06/S18（`nature_rural`）、S23（`science_lab`）、S29（`nature_water`）、S44（`medical`）
- **何が誤りか:**
  `select_factory_assets.py --theme` が受け付ける theme は `factory_themes.theme_of()` が subtype から導出する20種に限られる。`nature_rural` / `science_lab` / `nature_water` / `medical` は**そのどれでもない**。
  `--theme` に未知の値を渡してもエラーにならず「0 match」を返して静かに終わる＝**そのシーンの素材が1本も集まらないことに気づけない**。
  （※ EP39_frazier_CODEX_A_ASSETS.v001.md 側の `--theme` は6件すべて実在値。**誤っているのは v002 だけ**）
- **実行したコマンドと出力:**

```
$ ./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes
88850 assets across 20 category/theme groups (theme derived from subtype):
     522  backgrounds/abstract
    8487  backgrounds/atmosphere_symbolic
    1204  backgrounds/civic_voting
    3388  backgrounds/crime_police
    2995  backgrounds/documents_paper
    4888  backgrounds/finance_money
    1337  backgrounds/forensics_dna
    4303  backgrounds/legal_court
    2358  backgrounds/medical_lab
   11560  backgrounds/misc_background
    5824  backgrounds/nature_landscape
    3674  backgrounds/property_home
    1131  backgrounds/school_youth
    6625  backgrounds/surveillance_tech
    5968  backgrounds/urban_night
    7428  light_assets/light
     454  loops/abstract_loop
    6564  particle_assets/particle
    3911  texture_assets/texture
    6229  vfx_overlays/vfx

$ for t in nature_rural science_lab nature_water medical nature_landscape medical_lab; do
    echo -n "$t -> "; ./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme $t --kind video --limit 1 | head -1; done
nature_rural -> 0 match (of 88850 in shelf)
science_lab  -> 0 match (of 88850 in shelf)
nature_water -> 0 match (of 88850 in shelf)
medical      -> 0 match (of 88850 in shelf)
nature_landscape -> 1 match (of 88850 in shelf)
medical_lab      -> 1 match (of 88850 in shelf)
```

- **具体的な修正文字列（v002 §10.2 の表）:**

| ID | v002 の誤り | 正しい実在値 |
|---|---|---|
| S06 | `theme nature_rural` | `theme nature_landscape` |
| S18 | `theme nature_rural` | `theme nature_landscape` |
| S23 | `theme science_lab` | `theme medical_lab` |
| S29 | `theme urban_night or nature_water` | `theme urban_night`（`nature_water` は存在しないので削除） |
| S44 | `theme medical or urban_night` | `theme medical_lab or urban_night` |

---

## B-8 【EP39】v002 と CODEX_A の `S01–S50` が**同じコードで別の被写体**を指している（50件中46件不一致）

- **ファイル/位置:** `EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md` §10.1/§10.2 の表 vs `EP39_frazier_CODEX_A_ASSETS.v001.md` §4.2「50シーンの一覧」
- **何が誤りか:**
  scene_code は素材（A が生成）とカット割り（B が消費・v002 のタイムラインが参照）を繋ぐ唯一の鍵だが、**同じ `Sxx` が両文書で全く違う絵を指している。**
  スキーマ検査・ファイル存在検査は全て通る（コードは実在するので）が、**中身が別物なので全ビートで違う絵が出る＝無言の意味破壊**。
  例（`S03`）:
  - v002 §10.1: 「検死台のステンレス縁（人体なし）」= An extreme close-up of the polished stainless steel edge ... of an empty autopsy table
  - CODEX_A §4.2: 「一方向ミラー越し」= 取調室のマジックミラー（i2v 一覧 L538 も "reflections drift across the one-way mirror"）

  他の代表例:

  | ID | CODEX_A v001 の被写体 | v002 の被写体 |
  |---|---|---|
  | `S04` | 静かな郊外の庭 | 実験室のラック（1987血清学） |
  | `S06` | 深夜のダイナー | 8月のトウモロコシ畑 |
  | `S13` | 倒されたままの椅子 | 空の照合ファイル |
  | `S20` | 時計の針が進む | 標本瓶と綿棒 |
  | `S21` | 蛍光灯のちらつき | 証言台（無人） |
  | `S45` | 独房の窓の光 | 空白の20年（無記入カレンダー） |
  | `S49` | 大理石床の金色の光 | 便箋の縁と質感（Cayward） |

- **実行したコマンドと出力:**

```
$ ./.venv/Scripts/python.exe -c "<両ファイルの Sxx→主題 の表を正規表現で抽出し突合>"
A codes 50 V codes 51
mismatched subjects: 46 of 50
```
（EP39 の確定台本には `[Sxx]` 記法が1件も無いため、台本による裁定ができない:
`$ python -c "import re; print(len(set(re.findall(r'\bS\d{2}\b', open('EP39_frazier_script.en.v001.md',encoding='utf-8').read()))))"` → `0`）

- **具体的な修正:** v002 §10.1/§10.2 の scene_code 割当を正とし、**CODEX_A v001 §4.2 の50シーン表を v002 の表で丸ごと置換**すること。A が既に生成済みの画像があるなら scene_code を振り直す（`H:\pd-media\assets\ai\frazier\` の現物を目視して v002 の主題に再マップ）。放置すると全ビートで絵が合わない。

---

# MAJOR

## M-1 【EP40】CODEX_A の「50シーン / S01–S64」は確定台本に存在しない（台本は S01–S25）

- **ファイル/位置:** `EP40_lech_CODEX_A_ASSETS.v001.md` L25（A-1「50シーン × 3バリエーション = 150枚」）/ L260 / L264 / L333（`^S\d{2}$`・"§5.9 の S01..S64"）
- **何が誤りか:** 確定台本 `EP40_lech_script.en.v001.md` が参照する scene_code は **S01–S25 のちょうど25件**。v002 §5.7 はこれに1:1対応している（正しい）。CODEX_A の S26–S64 は**どの台本ビートからも参照されない画像**を39シーンぶん作る指示になっている。
- **実行したコマンドと出力:**

```
$ ./.venv/Scripts/python.exe -c "import re; s=open('episodes/_planning/EP40_lech_script.en.v001.md',encoding='utf-8').read(); c=sorted(set(re.findall(r'\bS\d{2}\b',s))); print(len(c)); print(c)"
25
['S01','S02','S03','S04','S05','S06','S07','S08','S09','S10','S11','S12','S13','S14','S15','S16','S17','S18','S19','S20','S21','S22','S23','S24','S25']
```

- **具体的な修正文字列:** CODEX_A L25 の「**50シーン × 3バリエーション = 150枚**」→「**25シーン × 6バリエーション = 150枚（scene_code は S01–S25 のみ。確定台本の `[Sxx]` に1:1対応。S26 以降は存在しない）**」。L260 / L264 / L333 のコメントも同様に S01–S25 に修正。

## M-2 【EP40】v002 と CODEX_A/B で素材配分が三者三様

| 項目 | v002（正典） | CODEX_A v001 | CODEX_B v001 / 実データ |
|---|---|---|---|
| シーン数 | 25（×6） | 50（×3） | — |
| factory | 70本 | 85本 | — |
| distinct 合計 | 167 | 171 | 実測 171 |
| AEカード | 8枠 | — | 23枚 |
| figures | 28枠 | — | 17枠（実装済み） |

- **実行したコマンドと出力:**
```
$ ./.venv/Scripts/python.exe scripts/check_asset_reuse.py remotion/src/data/lech_film.json | tail -4
PASS asset_reuse: 171 distinct assets over 226 cuts (mean 1.32x)
  first-use share 76% (floor 70%)
  caps  factory 1 | motion 2 | still 2
```
（asset_reuse は現状 PASS。数値の食い違いはゲート違反ではないが、A が85本 staging して B が70本前提で組むと空き番が出る）
- **修正:** v002 §5.1 の数値（factory 70 / distinct 167）を正とし、CODEX_A L28 / L234 / L265 の「85本」を「70本」に統一。

## M-3 【EP39】v002 §5.3 の「キネティックビート 38本」の内訳がゲートの分子と一致しない

- **ファイル/位置:** `EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md` L239 / L248
- **何が誤りか:** v002 L248 は「38本 = AE hero 8 ＋ Remotion MG 14 ＋ depth-parallax の主体ドリー 10 ＋ factory実写のカットイン 6」と内訳を書いているが、`check_motion_density` の分子は `graphics[]+figures[]+heroCuts[]` のみ。**AE 8 / parallax 10 / factory 6 の計24本は1本も数えられない。** v002 どおり figures を14枠しか置かなければ 14/11.71分 = **1.20/分 → HARD FAIL**。
  （実ビルドは figures 42枠で作られているため現状は PASS。つまり Codex は v002 の内訳に従わなかったから助かっている）
- **実行したコマンドと出力:**
```
$ ./.venv/Scripts/python.exe scripts/check_motion_density.py --ep frazier
  density     : 3.59/min   (floor 2.5)
  beats       : 42  [0 typo / 42 figures / 0 hero3d]  vs 222 Ken-Burns cuts
  RESULT: PASS

$ ./.venv/Scripts/python.exe -c "print(14/(702.8/60))"
1.1953...   ← v002 の内訳どおり figures 14 にした場合
```
- **具体的な修正文字列:** L248 を
  「**キネティックビート 38本 = すべて `frazier_film.json` の `figures[]` に入れる。** AEカード・depth-parallax・factory カットインは `check_motion_density` の分子に**入らない**（分子は `graphics[]+figures[]+heroCuts[]` のみ）ので、内訳として数えるな。」に置換。

## M-4 【EP40】`build_lech_hero_jsx.py` が §9.8 の罠のうち3件を実装していない

- **ファイル/位置:** `scripts/ae/build_lech_hero_jsx.py`（230行）vs `EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md` §9.8 罠 #1 / #2 / #6
- **何が誤りか:** 設計書 §9.8 の記述自体は**正しい**（雛形 `build_kfc_hero_jsx.py` に実装があることを確認）。しかし実装済みの lech 版には次が無い:
  - 罠#1 `setTemporalEaseAtKey` の次元ガード（`prop.isSpatial ? 1 : ...`）→ **無言で等速になる**
  - 罠#2 レンダテンプレ `applyTemplate("最良設定")` / OM `"H.264 - レンダリング設定を一致 - 15 Mbps"`
  - 罠#6 jsx 末尾の `app.quit()`
- **実行したコマンドと出力:**
```
$ grep -nE "applyTemplate|isSpatial|app.quit" scripts/ae/build_lech_hero_jsx.py
（0件）

$ grep -nE "applyTemplate|isSpatial|app.quit" scripts/ae/build_kfc_hero_jsx.py
175:        if (!prop.isSpatial) { var v0 = prop.value; dim = (v0 instanceof Array) ? v0.length : 1; }
336:        try { it.applyTemplate("最良設定"); } catch (e) { try { it.applyTemplate("Best Settings"); } catch (e2) {} }
338:        var omOK = false, omNames = ["H.264 - レンダリング設定を一致 - 15 Mbps",
339:                                     "H.264 - Match Render Settings - 15 Mbps"];

$ grep -nE "applyTemplate|isSpatial|app.quit" scripts/ae/build_frazier_ae_jsx.py
138:    try {{ rq.applyTemplate('最良設定'); }} catch (e1) {{ try {{ rq.applyTemplate('Best Settings'); }} catch (e2) {{}} }}
140:    try {{ om.applyTemplate('H.264 - レンダリング設定を一致 - 15 Mbps'); }} ...
149:  app.quit();
```
（frazier 版は実装済み。lech 版だけ欠落）
- **修正:** `build_lech_hero_jsx.py` に `build_frazier_ae_jsx.py` L138–149 相当を移植。

## M-5 【EP40】`lech_film.json` の still treatment が3種のみ（`duotone` / `card` / `bleed` 未使用）

- **ファイル/位置:** `remotion/src/data/lech_film.json` vs `remotion/src/compositions/CaseFilm.tsx` L29（「FIVE distinct still treatments」）
- **実行したコマンドと出力:**
```
$ ./.venv/Scripts/python.exe -c "<kind×treatment のクロス集計>"
lech_film.json  Counter({('footage','footage'):101, ('img','scan'):43, ('img','depth'):41, ('img','focus'):41})
frazier_film.json Counter({('footage','footage'):93, ('footage','motion'):38, ('img','scan'):37, ('img','focus'):35, ('img','depth'):10, ('img','duotone'):9})
```
- **注記（自分の計測器の疑い）:** `frazier_film.json` に `treatment:"motion"` が38件あり CaseFilm の switch に無いが、**これらは全て `kind:"footage"` のカット**で `FactoryClip`（動画）経路に流れるため treatment は参照されない。**誤報ではない＝これは finding にしない。**
- 実害: lech の静止画が3パターンの反復になり単調。ゲート違反ではないので MAJOR 止まり。

---

# MINOR

## m-1 【EP39】v002 §10.1 の SDXL シーン数が見出しの「30」と合わず実際は31行

```
$ ./.venv/Scripts/python.exe -c "<§10.1/§10.2 の表の行を正規表現でカウント>"
10.1 SDXL rows: 31 ['S01','S02','S03','S04','S05','S08','S11','S12','S13','S14','S15','S16','S17','S19','S20','S21','S22','S24','S25','S26','S31','S37','S38','S39','S41','S43','S45','S46','S47','S49','S50']
10.2 factory rows: 20
union 51
```
§10 見出し「30シーン × 3枚 = 90枚」/ §10.3 コメント「全30シーンを1枚ずつ（=30枚）」→ 実際は **31シーン / 93枚**。
**修正文字列:** 「30シーン × 3枚 = 90枚発注」→「**31シーン × 3枚 = 93枚発注**」、§10.3 の `# PASS 1: 全30シーンを1枚ずつ（=30枚）` → `# PASS 1: 全31シーンを1枚ずつ（=31枚）`。

## m-2 【EP40】CODEX_A のバリエーション数が文書内で矛盾（3 vs 6）

- L25 / L247「50シーン × **3**バリエーション」 vs L568 `# scene_index: 1..64, variation: 1..6` / L572「S64_03」/ §5.6 は `_01`/`_02`/`_03` の3軸のみ列挙。
- v002 は「25シーン × **6**バリエーション = 150枚」（L438）。
- **修正:** CODEX_A を「25シーン × 6バリエーション = 150枚」に統一し、§5.6 に `_04`（曇天拡散光）/ `_05`（寄り）/ `_06`（別構図）の3軸を追記。`seed_for` のコメント `scene_index: 1..64` → `1..25`。

## m-3 【EP39】factory 在庫本数の表記が実測と合わない

- v002 §6.1 / CODEX_A L234 が「在庫11,623本」、`check_asset_reuse.py` の docstring は「11,443-clip library」。
- 実測:
```
$ ./.venv/Scripts/python.exe -c "import json,collections; d=json.load(open('assets/asset_manifest.v001.json',encoding='utf-8'))['assets']; print(collections.Counter(x.get('kind') for x in d))"
Counter({'image': 73167, 'video': 15683})
```
→ 動画クリップは **15,683本**。設計判断に影響しないため MINOR。

---

# 実機で確認して「問題なし」だった項目（誤報を出さないための記録）

| # | 検査対象 | コマンド | 結果 |
|---|---|---|---|
| 1 | Remotion composition id の実在と重複 | `grep -oE 'id="[^"]+"' remotion/src/Root.tsx \| sort \| uniq -d` | 重複0件。`Ep39Frazier` / `Frazier39Opening` / `Ep40Lech` / `OpeningLech` / `Thumb-frazier-*` / `Thumb-lech-0*` すべて実在 |
| 2 | EP39 AE hb01–hb08 の `anchor_phrase` が確定台本に逐語1回だけ存在するか | 8語句を `str.count()` | **8件すべて `1`**（0件も2件以上も無し。v002 §7.1 は正しい） |
| 3 | `Frazier39Opening` の props 名 | `grep -nE "title\|subtitle\|accent\|hasLogo" remotion/src/compositions/Frazier39Opening.tsx` | `{title, subtitle, accent, hasLogo}` 実在。`props/frazier_op_{a,b,c}.json` も3本とも実在 |
| 4 | v002 §0.1 が主張するゲート定数 | `grep -nE "^HOOK_MIN_SEC\|^LOW_MOTION_MAX_SPAN_S\|..." scripts/check_final_acceptance.py` | `HOOK_MIN_SEC=5.0` / `LOW_MOTION_MAX_FRACTION=0.10` / `LOW_MOTION_MAX_SPAN_S=3.0` / `CAPTION_MATCH_MIN=0.90` / `BOOKEND_OP_SEC=3.5` / `BOOKEND_ED_SEC=9.0` / `IMG_MIN_LONG_EDGE=3840` / `FOOTAGE_GENERIC_MAX_USES=2` / `FACTORY_SECONDS_PER_CLIP=45` / `LUFS -16.0,-12.0` — **全て記述どおり** |
| 5 | v002 §13 の `check_bookends` の挙動説明 | `scripts/check_final_acceptance.py` L494–518 を読む | `<slug>_film.json` があれば `CaseFilm.tsx` を検査する、と実装が一致。`CaseFilm.tsx` L23 に `BrandOpening/BrandEndcard/OPENING_SEC/ENDCARD_SEC` の import 実在 |
| 6 | `cuts[].kind` の値 | `frazier_film.json` / `lech_film.json` を集計 | `img` / `footage` の2値のみ。`CaseFilm.tsx` L39 の `kind: 'img' \| 'footage'` と一致 |
| 7 | CLI フラグの実在 | `--help` を6本実行 | `check_final_acceptance.py <ep> --json --render --emit-receipt` / `generate_sdxl_4k.py <ep> --variants --only` / `gen_depth_maps.py --dir --force` / `check_motion_density.py --ep` / `check_padding.py --ep` / `preflight_render_gate.py --ep` / `check_visual_asset_qc.py --ep` — **記述どおり全て受け付ける** |
| 8 | AE 実行体と OM/RS テンプレ名 | `ls "/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/"` | `AfterFX.exe` / `AfterFX.com` / `aerender.exe` 実在。RS `"最良設定"` / OM `"H.264 - レンダリング設定を一致 - 15 Mbps"` は `build_kfc_hero_jsx.py` L336–339 で実使用 = 記述は正しい |
| 9 | jsx API `ADBE Rotate Z` | `grep "ADBE Rotate Z" scripts/ae/build_kfc_hero_jsx.py` | L260 で実使用。設計書の「`ADBE Rotation` は null を返す」は雛形の実装と整合 |
| 10 | npm パッケージ | `remotion/package.json` | `@remotion/motion-blur ^4.0.476` / `@remotion/three` / `remotion ^4.0.0` すべて実在。`npm run studio` / `typecheck` も定義済み |
| 11 | H: ドライブのパス | `ls H:/pd-media/assets/` → `ai ai_video characters factory stock`；`ls H:/pd-media/assets/ai/` に `frazier` / `lech` 実在 | `config/storage.local.json` の `roots.media.path = "H:\\pd-media"` と一致 |
| 12 | `py -3.11` ランチャ | `py -3.11 -c "print('ok')"` | `py3.11 OK`（CODEX_A/B が使う起動方法は有効） |
| 13 | SDXL プロンプト書式（EP39 CODEX_A） | 実パーサ `read_prompts()` を CODEX_A に適用 | 1件（S01 の見本）だけヒット。**これは「この2行組を30個書け」という見本提示であり欠陥ではない**（誤報を出しかけた箇所） |
| 14 | `treatment:"motion"`（frazier 38件） | kind×treatment のクロス集計 | 全て `kind:"footage"` = `FactoryClip` 経路で treatment 不参照。**誤報にしない** |
| 15 | `check_asset_reuse` | 両 film.json に対して実行 | frazier 86% / lech 76%（フロア70%）— **両方 PASS** |

---

# Codex への伝達サマリ（優先順）

1. **B-3 が最優先。** EP40 は v002・B_BUILD どちらの仕様に従っても `check_motion_density` が FAIL する。`lech_film.json` の `figures[]` を **34枠（平均6.0秒）** に増やすまで出荷不可。
2. **B-1 / B-2 を直さずに figures を書き足すと全部無言で消える。** kind は小文字の実在値、テキストフィールドは `title` / `quote` / `primary` / `lines`。
3. **B-4** — 枠数を変えたら `validate_lech_beats.py` の 23 / 17 を必ず同時に更新。
4. **B-5** — 確定台本を `03_script/` に置く前に `check_lech_accuracy.py` を2文窓に直す。今の PASS は台本未配置による偽グリーン。
5. **B-6 / B-7 / B-8** — EP39 は v002 とスレッドA/Bの間で「AEスクリプト名」「factory theme 名」「scene_code の意味」が食い違っている。**B-8（46/50 の被写体不一致）は素材を作り直す規模の実害**なので、GPU ジョブを止めて scene_code を先に確定させること。
