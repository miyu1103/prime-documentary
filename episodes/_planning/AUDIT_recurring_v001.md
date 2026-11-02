# 反復失敗チェックリスト監査 — EP39 frazier / EP40 lech

- 監査日: 2026-07-20
- 監査対象: `EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md`（正典）/ `EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md`（正典）/ `EP39_frazier_CODEX_A_ASSETS.v001.md` / `EP39_frazier_CODEX_B_BUILD.v001.md` / `EP40_lech_CODEX_A_ASSETS.v001.md` / `EP40_lech_CODEX_B_BUILD.v001.md` / `EP39_frazier_script.en.v001.md` / `EP40_lech_script.en.v001.md`
- 方法: 実機（`C:\Users\aab15\Documents\prime-documentary`）で Grep / Read / 実行。evidence は実行コマンドと実際の出力。
- **本監査はファイルを一切修正していない。報告のみ。**

## 総括

| 判定 | 件数 | 項目番号 |
|---|---|---|
| 該当あり | **9** | 1, 2, 3, 4, 5, 7, 10, 12, 13 |
| 該当なし | 4 | 6, 8, 9, 11 |
| **BLOCKER** | **8** | 下表 |

### BLOCKER 一覧（支出・レンダーの前に潰すこと）

| # | 項目 | 内容 |
|---|---|---|
| B1 | 2 / 13 | EP40 v002 のサムネ出力名が `thumbnail_ready`（HARD）のグロブに一致しない → 確実に落ちる |
| B2 | 2 | EP39 v002 の素材配分 110/160 = 0.6875 が `check_asset_reuse` の `MIN_FIRST_USE_SHARE=0.70` を割る |
| B3 | 13 | 実装済み `scripts/check_lech_accuracy.py` が v001 の1文窓のまま → 確定台本に **偽陽性2件**（実行で証明） |
| B4 | 13 | 実装済み `scripts/ae/build_frazier_ae_jsx.py` は6族全部を必須にするが、v002 は HERO_DATA 8枚しか定義しない → `--validate` が必ず FAIL |
| B5 | 11 / 13 | EP39 CODEX_B の `HB7_DECISION_VOTE`（判決の票数・E_VOTE_TALLY）は v002 が「台帳に無い＝捏造」と明示禁止した内容 |
| B6 | 1 | EP40 v002 に **factory の全点目視QC 手順が存在しない**（CODEX_A にはあるが v002 は「v001 を読むな」と指示） |
| B7 | 3 | 全6文書に `sys.stdout.reconfigure(encoding="utf-8")` の指示ゼロ。かつ EP40 v002 の CardTypo 文字列が em-dash を含む（cp932 で encode 不能を実測） |
| B8 | 5 | `remotion/public` は **48GB**。全6文書に `--public-dir` / `public_slim` の指定ゼロ |

---

## 13項目の判定表

| # | 項目 | 判定 | 深刻度 | 根拠（実行コマンド／実際の出力） |
|---|---|---|---|---|
| 1 | ファイル名を信じて中身を見ていない | **該当あり（EP40 v002）** | **BLOCKER** | 下記 §1 |
| 2 | 複数箇所に書かれるのに1箇所しか読まない | **該当あり（両話）** | **BLOCKER** | 下記 §2 |
| 3 | cp932 UnicodeEncodeError | **該当あり（両話・全6文書）** | **BLOCKER** | 下記 §3 |
| 4 | 長時間ジョブの起動方法 | **該当あり（EP39_B）** | HIGH | 下記 §4 |
| 5 | Remotion の public ディレクトリ | **該当あり（両話・全6文書）** | **BLOCKER** | 下記 §5 |
| 6 | 出荷済みファイルの上書き | なし | — | 下記 §6 |
| 7 | スタブと本番でコードパスが分岐 | **該当あり（EP40・軽微）** | MEDIUM | 下記 §7 |
| 8 | 「完成」の定義 | なし | — | 下記 §8 |
| 9 | AEの既知の罠 | なし | — | 下記 §9 |
| 10 | preflight / acceptance の切り分けと支出前停止 | **該当あり（EP39 v002）** | HIGH | 下記 §10 |
| 11 | R2/R3 のリスク封じ込め | なし（v002本体）／ ※B5 は項目13で計上 | — | 下記 §11 |
| 12 | EP40「最高裁が決めた」禁止の全面適用 | **該当あり（部分カバー）** | HIGH | 下記 §12 |
| 13 | v002 と Codex A/B の食い違い | **該当あり（全面）** | **BLOCKER** | 下記 §13 |

---

## §1. ファイル名を信じて中身を見ていない — 【該当あり／BLOCKER】

### EP39: なし（根拠を示す）

`EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md:283-285`

```
### 6.2 ★factory のラベルは信用できない（工程に組み込む）
EP36 で `city_surveillance_camera_dome` が実際にはベオグラードの大聖堂、EP38 で
`documents_on_desk` が牛の映像だった実例がある。**110本をステージングして全点を
目視QCする（約2時間。削るな）。**
```

`EP39_frazier_CODEX_A_ASSETS.v001.md:144,150` にも「全点目視QC 2.0h」「★factory の全点目視QC 2時間は削るな」があり、`eyeballed_content` 相当の記録も要求されている。**EP39 は該当なし。**

### EP40: **該当あり**

EP40_CODEX_A には完璧な手順がある:

```
$ grep -n "目視\|ファイル名\|信用" episodes/_planning/EP40_lech_CODEX_A_ASSETS.v001.md
937:## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★
950:   episodes/PD-2026-040-lech/05_visuals/factory_contactsheet.png にコンタクトシートを出力する
951: 2. **あなたがコンタクトシートを実際に開いて、85本すべてを1本ずつ見る**
954:   **ファイル名を言い換えただけの記述は禁止。** subtype と食い違ったら
      label_matches_content: false を立てて**選定から外す**
433:12. **`factory[].eyeballed_content` が空文字でない**
```

**ところが正典 v002 には、この手順が1行も無い:**

```
$ grep -n "目視\|contact_sheet\|コンタクトシート\|全点\|ファイル名を信\|filename" \
    episodes/_planning/EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md
1274:→ composition `OpeningLech` を選び、0→180 フレームでスクラブして…目視確認する。
1533:| 7 | 9歳男児の描写が特定可能になる | … | **生成後に全150枚を目視確認**（EP38 retro「filenameを信じるな」） |
```

- 1274 は OP のプレビュー確認。1533 は**静止画150枚**の話。**factory クリップの目視QCは1回も出てこない。**
- factory の唯一の記述は `§13.1 C6`:

```
| **C6** | factory 素材の選定 **70本** | `05_stock/factory_selection.v002.json`
（EP39 と sha256 重複除外・`search_keywords` 記録） | なし |
```

→ **`search_keywords`（＝検索語＝ファイル名/メタデータ信頼）だけで70本を確定する指示になっている。** これは EP36 の大聖堂・EP38 の牛と**同一の失敗経路**。

さらに致命的なのは、v002 の Codex プロンプト（`:1547`）が

```
同ディレクトリの v001 は破棄済みで、事実面で v002 と衝突する。v001 を読んで実装してはならない。
```

と指示している点。**Codex は v002 だけを読むので、CODEX_A §7.5 の目視QC手順に到達できない。**

### 修正文字列（EP40 v002 §5 の末尾か §13.1 C6 に追記）

```markdown
### 5.9 ★★★ factory のファイル名とサブタイプは信用できない（工程に組み込む・削るな）★★★

実例: EP36 で `city_surveillance_camera_dome` が実際はベオグラードの大聖堂、
EP38 で `documents_on_desk` が牛の映像だった。**在庫索引のラベルは検証されていない。**

手順（C6 の一部として必須。所要 約2時間。短縮禁止）:
1. `search_keywords` で **85本**をステージングする（採用70本 + 差し替え余裕15本）。
2. `scripts/build_lech_factory_qc.py --contact-sheet` で
   `episodes/PD-2026-040-lech/05_visuals/factory_contactsheet.png` を出力する。
3. **コンタクトシートを実際に開き、85本を1本ずつ見る。**
4. 各クリップに `eyeballed_content`（実際に見た内容を1文・**ファイル名の言い換えは禁止**）と
   `label_matches_content`（bool）を `05_visuals/factory_clip_qc.v001.json` に記録する。
5. `label_matches_content: false` / 顔が識別できる人物が大きく写っている / 夜景（本作は昼が正典・§2）
   のいずれかに該当したら `on_theme: false` にして選定から外し、
   `remotion/public/lech/factory/` からも物理削除する。
6. `./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-040-lech` が
   exit 0 になるまで終わらない（staging 済み全クリップを網羅していること）。
```

---

## §2. 複数箇所に書かれるのに1箇所しか読まない — 【該当あり／BLOCKER ×2】

### B1: EP40 v002 のサムネ出力名がゲートのグロブに一致しない

実装（`scripts/check_final_acceptance.py:632-642`）:

```python
def check_thumbnail(epdir: Path) -> dict:
    """>=3 thumbnail PNGs at 1280x720 + a selected one must exist."""
    cands = list((epdir / "10_thumbnail").glob("*.png")) + \
            list((epdir / "09_package").glob("thumbnail*.png"))
    good = [p for p in cands if _png_dims(p) == (THUMB_W, THUMB_H)]
    selected = list((epdir / "09_package").glob("thumbnail.selected*.png"))
    ok = len(good) >= MIN_THUMB_VARIANTS and bool(selected)
    return {"check": "thumbnail_ready", "ok": ok, "hard": True, ...}
```

設計書（EP40 v002）:

```
$ grep -n "thumbnail_selected\|thumb_{1" episodes/_planning/EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md
1321:- 3枚レンダ後、**T1 を `selected` にする**（`09_package/thumbnail_selected.png`）
1420:| **C13** | サムネ実装 3案 | … + `09_package/thumb_{1,2,3}.png` + `thumbnail_selected.png` | C5 |
```

- `thumbnail_selected.png`（アンダースコア）は `thumbnail.selected*.png`（ドット）に**一致しない** → `selected` が空 → `thumbnail_ready`（**HARD**）FAIL。
- `thumb_1.png` は `thumbnail*.png` に**一致せず**、`10_thumbnail/` にも無い → `good` が 0 → 二重に FAIL。
- `thumbnail_visibility` も `thumbnail.selected*.png` を見るので skip される。

**EP39 v002 は正しい**（`:386`）: `09_package/thumbnail.v001-01.png` … ＋ `thumbnail.selected.v001.png` → グロブ一致。つまり EP40 側だけの退行。

**修正文字列（EP40 v002 §12.2 `:1321` と §13.1 C13 `:1420`）:**

```markdown
- 3枚レンダ後、**T1 を selected にする**。
  出力名は `check_final_acceptance.py::check_thumbnail` のグロブに一致させること（変更禁止）:
    09_package/thumbnail.v002-01.png
    09_package/thumbnail.v002-02.png
    09_package/thumbnail.v002-03.png
    09_package/thumbnail.selected.v002.png   ← T1 の複製。ドット区切り必須
  ※ `thumbnail_selected.png` / `thumb_1.png` はゲートのグロブ
    （`09_package/thumbnail*.png` と `09_package/thumbnail.selected*.png`）に一致せず、
    `thumbnail_ready`(HARD) が必ず FAIL する。
```

### B2: EP39 v002 が `footage_diversity` だけを見て `check_asset_reuse` を見ていない

EP39 v002 `:278`:

```
- `distinct/total ≥ 0.40` に対し設計値 **110 / 160 = 0.69**。
```

しかし素材の再利用ゲートは**2本ある**。もう1本の実装（`scripts/check_asset_reuse.py:44-47`）:

```python
MAX_USES_FACTORY = 1     # free + 11,443 available -> never repeat
MAX_USES_MOTION = 2
MAX_USES_STILL = 2
MIN_FIRST_USE_SHARE = 0.70   # >=70% of cuts must be the first appearance of their asset
```

**110 / 160 = 0.6875 < 0.70 → `check_asset_reuse` HARD FAIL。** v002 は `check_asset_reuse` にも `first_use_share` にも1度も触れていない。

一方 `EP39_frazier_CODEX_A_ASSETS.v001.md:86,122,126-127` はこのゲートを正しく把握しており、v002 の配分を先回りで否定している:

```
86: さらに全体条件: **`first_use_share = distinct_assets / cuts_with_asset >= 0.70`**
122: 検算: `first_use_share = 176 / 226 = 0.779`（フロア 0.70 に対し 0.08 の余裕）
126: > ⚠ 旧設計書 v001 §8 の内訳…は自分のゲートを通らない。
127: > 検算: 50×1 + 50×2 + 15×2 = 180カット、distinct = 115、`115/180 = 0.639 < 0.70` → **FAIL**。
        上限いっぱいに使う設計は原理的に share を下げる。
```

**修正文字列（EP39 v002 §6.1 の表の下・`:278` を差し替え）:**

```markdown
- 素材の反復ゲートは **2本ある。両方を満たすこと。**
  1. `check_footage_diversity`: `distinct/total ≥ 0.40`
  2. `check_asset_reuse`: **`first_use_share = distinct / cuts ≥ 0.70`**
     （`scripts/check_asset_reuse.py::MIN_FIRST_USE_SHARE = 0.70`。
      cap は factory 1回 / motion 2回 / still 2回 = `MAX_USES_*`）
- ★旧記載「110 / 160 = 0.69」は **0.6875 < 0.70 で `check_asset_reuse` が HARD FAIL する。破棄する。**
- **確定配分（226カット / distinct 176点）:**
  | 種別 | distinct | 使用回数 | カット |
  |---|---|---|---|
  | factory backgrounds | 90本 | 1回 | 90 |
  | SDXL 静止画 | 68枚 | ≤2回（42×2 + 26×1）| 110 |
  | i2v モーション | 18本 | ≤2回（8×2 + 10×1）| 26 |
  | **合計** | **176** | | **226** |
  検算: `176 / 226 = 0.779 ≥ 0.70` ✅ / `176 / 226 = 0.779 ≥ 0.40` ✅
- 平均ショット長 = 705 / 226 = **3.12秒** ≤ 6.0秒 ✅（§5.2 の「150–170カット」も同時に破棄する）
```

> 補足（同種の失敗の再発点）: A/B候補の所在。リポジトリの慣習は
> `09_package/title_thumbnail_candidates.v001.json`（`build_ep19_varsityblues_final.py:1070` /
> `build_arbitration_thumbnails_v001.py:245` 等）だが、EP40 v002 §13.1 C19 は
> `09_package/title_candidates.json` という**別名**を指定している。EP39 v002 は
> A/B候補の JSON 出力先を**一切指定していない**。両方とも既存慣習に合わせること。

---

## §3. cp932 UnicodeEncodeError — 【該当あり／BLOCKER】

### 指示の不在

```
$ grep -rn "reconfigure" episodes/_planning/EP39_*.md episodes/_planning/EP40_*.md
（ヒット0件）
```

6文書のどこにも `sys.stdout.reconfigure(encoding="utf-8")` の指示が無い。一方リポジトリでは確立された慣習である:

```
$ grep -rln "stdout.reconfigure" scripts/*.py | wc -l
（多数。add_real_assets.py:44 / ai_image_brief.py:59 / build_case_film_audio.py:1075 など）
```

### 実際に新規作成済みのスクリプトが全滅している

```
$ for f in scripts/ae/build_frazier_ae_jsx.py scripts/ae/composite_frazier_ae.py \
      scripts/ae/build_lech_hero_jsx.py scripts/ae/composite_lech_hero.py \
      scripts/check_lech_accuracy.py scripts/validate_lech_beats.py \
      scripts/validate_lech_slots.py scripts/build_frazier_film.py \
      scripts/build_lech_film_data.py; do
    printf "%-45s reconfigure=%s\n" "$f" "$(grep -c 'stdout.reconfigure' $f)"; done

scripts/ae/build_frazier_ae_jsx.py            reconfigure=0
scripts/ae/composite_frazier_ae.py            reconfigure=0
scripts/ae/build_lech_hero_jsx.py             reconfigure=0
scripts/ae/composite_lech_hero.py             reconfigure=0
scripts/check_lech_accuracy.py                reconfigure=0
scripts/validate_lech_beats.py                reconfigure=0
scripts/validate_lech_slots.py                reconfigure=0
scripts/build_frazier_film.py                 reconfigure=0
scripts/build_lech_film_data.py               reconfigure=0
```

**9/9 が未対応。** うち `check_lech_accuracy.py` は違反文字列をそのまま `print` する（`print(json.dumps(result, ensure_ascii=False, indent=2))`）。

### em-dash が cp932 で encode 不能であることの実測

```
$ ./.venv/Scripts/python.exe -c "'—'.encode('cp932')"
UnicodeEncodeError: 'cp932' codec can't encode character '—' in position 0:
illegal multibyte sequence
```

**そして EP40 v002 の CardTypo 文字列が em-dash を含む:**

```
$ grep -n "INTENTIONAL ACTS BY GOVERNMENT OFFICIALS" \
    episodes/_planning/EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md
322:| R3 | 227.5 | 3:47 | 逃げ場の消滅 | 〔CARD: INTENTIONAL ACTS BY GOVERNMENT OFFICIALS — EXCLUDED〕 |
726:| `c04` | **227.50 – 234.50** | `INTENTIONAL ACTS BY GOVERNMENT OFFICIALS — EXCLUDED` | …
727:| `c05` | … | `NOT BINDING PRECEDENT — MAY BE CITED FOR ITS PERSUASIVE VALUE` | …
```

§9.8 罠13 は **AEレイヤーの豆腐対策としてのみ** ASCII ハイフン化を書いており、**Remotion 側 CardTypo（§8）と `figures[].text` は em-dash のまま**。`check_lech_accuracy.py` / `validate_lech_slots.py` がこの文字列を違反として print した瞬間に落ちる。

さらに実測で日本語の文字化けも確認済み（下記 §13 B3 の出力に `?kCARD` として現れている）。

### 修正文字列（EP39 v002 §14 直前 と EP40 v002 §13 直前に共通節として新設）

```markdown
## X. 新規 Python スクリプトの共通必須ヘッダ（例外なし・全スクリプト）

このマシンは Windows・日本語ロケール・既定コンソールが **cp932**。
非ASCII を print した瞬間に UnicodeEncodeError で落ちる。**すべての新規/改修スクリプトの
`main()` 冒頭（argparse より前）に次の3行を必ず入れる。**

```python
import sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
try: sys.stderr.reconfigure(encoding="utf-8")
except Exception: pass
```

対象（本設計書が作成を指示する全スクリプト）:
  scripts/check_lech_accuracy.py / scripts/validate_lech_slots.py /
  scripts/validate_lech_beats.py / scripts/measure_vo_wpm.py /
  scripts/ae/build_lech_hero_jsx.py / scripts/ae/composite_lech_hero.py /
  scripts/ae/build_frazier_ae_jsx.py / scripts/ae/composite_frazier_ae.py /
  scripts/build_frazier_film.py / scripts/build_lech_film_data.py /
  scripts/select_lech_factory.py / scripts/qc_lech_stills.py ほか全部

加えて **U+2014 EM DASH（—）は cp932 で encode 不能**（実測）。
- ファイルパス・ログ・print 文字列に em-dash を使わない。
- **画面に出す文字列も ASCII ハイフン `-` に統一する。**
  §8 の `c04` = `INTENTIONAL ACTS BY GOVERNMENT OFFICIALS - EXCLUDED`
  §8 の `c05` = `NOT BINDING PRECEDENT - MAY BE CITED FOR ITS PERSUASIVE VALUE`
  §3.4 R3 のラベルも同様。（AE だけでなく Remotion / figures[].text / beats.json も対象）
```

---

## §4. 長時間ジョブの起動方法 — 【該当あり／HIGH】

### EP39_CODEX_B: 該当あり

`EP39_frazier_CODEX_B_BUILD.v001.md:623-630`

```bash
# 2) ビルド（AfterFX でコンプ作成 → .aep 保存 → app.quit()）
#    jsx 末尾が render/_build_ok.txt を書く。これをポーリングする。早期killしない。
"/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.com" -noui -r \
  "…/08_edit/ae_hero/frazier_ae.jsx" &        ← ★ここ
```

**末尾 `&` によるシェルバックグラウンド起動。** これは EP38 retro で「orphan / kill される」として潰したパターンそのもの。同 `:648` の罠表には「デタッチ起動＋出力ファイルのポーリング」と正しく書いてあるのに、**実行コマンド例が `&` になっていて矛盾している。** Codex はコマンド例をコピーする。

`run_in_background` / AE自己デタッチの指定は**6文書すべてに1件も無い**:

```
$ grep -c "run_in_background" episodes/_planning/EP39_*.md episodes/_planning/EP40_*.md
（全ファイル 0）
```

### EP40: 該当なし（根拠）

`EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md:1059-1063` はフォアグラウンド起動＋マーカーポーリングで、`&` もリダイレクトも使っていない:

```bash
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "…/08_edit/ae_hero/lech_hero.jsx"
# → render/_build_ok.txt が出るまで待つ（最大300秒）
# → 続いて render/b0*.mp4 が8本揃うまで待つ（最大600秒）
```

なお実行体はどちらも実在する（`.com` / `.exe` 両方）ので、そこは問題なし:

```
$ ls "/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/" | grep -iE "AfterFX|aerender"
AfterFX.com / AfterFX.exe / aerender.exe   ← すべて実在
```

### 修正文字列（EP39_CODEX_B §5.7 `:625-626`）

```bash
# 2) ビルド（AfterFX でコンプ作成 → .aep 保存 → app.quit()）
#    ★シェルの `&` でバックグラウンド化してはならない（orphan 化して kill される）。
#      run_in_background でこのコマンド自体を投げるか、Python から
#      subprocess.Popen(..., creationflags=subprocess.DETACHED_PROCESS) で自己デタッチさせる。
#    ★nohup / リダイレクト（> log 2>&1）での起動も禁止。
"/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.com" -noui -r \
  "…/08_edit/ae_hero/frazier_ae.jsx"
# → render/_build_ok.txt が出るまでポーリング（21コンプなので最大 600秒）。早期killしない。
```

---

## §5. Remotion の public ディレクトリ — 【該当あり／BLOCKER】

### 実測

```
$ du -sh remotion/public
48G     public

$ du -sh remotion/public/* | sort -rh | head -5
3.5G    public/king
2.9G    public/carsearch
2.8G    public/rolin
2.7G    public/titan
2.5G    public/onecoin
```

### 指定の不在

```
$ grep -n "public_slim\|--public-dir\|publicDir" \
    episodes/_planning/EP39_frazier_*.md episodes/_planning/EP40_lech_*.md
（ヒット0件）
```

6文書すべてに `--public-dir` 相当の指定が無い。レンダーコマンドは以下のように素で書かれている:

```
EP40 v002:1295  npx remotion render Ep40Lech out/lech_final.mp4 --props=./src/data/lech_film.json
EP40 v002:1278  npx remotion render OpeningLech out/lech_opening.mp4 --props=./props/lech.json
EP39 v002:544   npx remotion render Frazier39Opening out/frazier_op_a.mp4 --props=./props/frazier_op_a.json
```

→ **1レンダーごとに 48GB のバンドルコピーが発生する。** EP38 retro で明示的に潰した項目。EP39/EP40 は自分の素材だけ（`public/frazier/**`・`public/lech/**`・`public/lech_dryrun/**`）しか参照しないので、slim 化は無損失。

### 修正文字列（EP39 v002 §13 / EP40 v002 §11.6 の各レンダーコマンド節の直前に共通で追記）

```markdown
### ★レンダー前に必ず public を slim 化する（48GB コピー対策・EP38 retro）

`remotion/public` は **48GB** ある。素で `npx remotion render` すると毎回全量が
バンドルにコピーされ、レンダーのたびに数十分を捨てる。本作が参照するのは
`public/<slug>/**` と `public/fonts` `public/brand` だけなので、slim ディレクトリを作って渡す。

```bash
cd C:/Users/aab15/Documents/prime-documentary/remotion
rm -rf public_slim && mkdir -p public_slim
# 本作のアセットと共有アセットだけをリンク/コピーする（EP40 なら lech / lech_dryrun）
cp -r public/lech public_slim/ 2>/dev/null || true
cp -r public/lech_dryrun public_slim/ 2>/dev/null || true
cp -r public/fonts public/brand public_slim/ 2>/dev/null || true
du -sh public_slim     # ★数GB以内であることを目で確認してから次へ進む
```

**以後の全レンダー・全 Still レンダーに `--public-dir=public_slim` を必ず付ける:**

```bash
npx remotion render Ep40Lech out/lech_final.mp4 \
  --props=./src/data/lech_film.json --public-dir=public_slim
npx remotion render OpeningLech out/lech_opening.mp4 \
  --props=./props/lech.json --public-dir=public_slim
npx remotion still LechThumb1 ../episodes/PD-2026-040-lech/09_package/thumbnail.v002-01.png \
  --public-dir=public_slim
```

（EP39 は `public/frazier` を同様に slim 化し、`Frazier39Opening` / `CaseFilm` /
サムネ Still の**すべて**に `--public-dir=public_slim` を付ける。）
`npm run studio` も `--public-dir=public_slim` を付けて起動する。
```

---

## §6. 出荷済みファイルの上書き — 【該当なし】

根拠（全6文書の `v003_ae` 出現数と、上書き禁止の明文）:

```
$ grep -c "v003_ae" episodes/_planning/EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md \
    episodes/_planning/EP39_frazier_CODEX_A_ASSETS.v001.md \
    episodes/_planning/EP39_frazier_CODEX_B_BUILD.v001.md \
    episodes/_planning/EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md \
    episodes/_planning/EP40_lech_CODEX_A_ASSETS.v001.md \
    episodes/_planning/EP40_lech_CODEX_B_BUILD.v001.md

EP39 v002 : 6
EP39 A    : 0   ← A は素材スレッドで mp4 を出さないので該当外（正当）
EP39 B    : 8
EP40 v002 : 5
EP40 A    : 0   ← 同上
EP40 B    : 5
```

明文の例:
- `EP39_CODEX_B:656` 「| 15 | 上書き | **出荷済みファイルを絶対に上書きしない。** 出力は必ず `*_v003_ae.mp4` の新規版名 |」
- `EP40 v002:1032` 「**出荷済みファイルを絶対に上書きしない。** 出力は必ず `_v003_ae` サフィックス。」
- `EP40 v002:1013-1014` `BASE = …lech_final_bgm.v002.mp4` / `OUT = …lech_final_bgm.v003_ae.mp4`
- `EP40 v002:1455` 「公開済み mp4 を再レンダリング/上書きしない。」

**該当なし。** ただし §2 の B1 と併せて、v002 のサムネ出力名だけは別問題として要修正。

---

## §7. スタブと本番でコードパスが分岐 — 【該当あり（軽微）／MEDIUM】

### 大枠は模範的（該当なしの根拠）

`EP40_lech_CODEX_B_BUILD.v001.md:57-58` は、まさにこの失敗を先回りで禁止している:

```
> `is_stub` の値によって**処理を変えない**。分岐したらドライランの意味が消える。
> （`is_stub` はログ出力と受入判定にのみ使う。カットの組み立てロジックには一切使わない。）
```

`:745` にも再掲:
```
**`--assets` に渡されたファイルの `is_stub` によって処理を変えないこと**（§0.2）
```

スタブの分離も「分岐」ではなく**ディレクトリ分離**で実現しており正しい:
```
:376  remotion/public/lech_dryrun/{img,factory,motion,overlay}/ を作る
:386  （`is_stub: true`、`public_path` の先頭を `lech_dryrun/` にする）
:628  ドライランの出力は …/08_edit/_dryrun/ 配下に置き、本番ファイル名を使わない。
```

### 残っている分岐（該当あり）

**ゲートの重大度が `--dryrun` で変わる箇所が2つある。**

```
EP40_CODEX_B:625   | `true` | `false` | **exit 1**（台本工程に差し戻し）。
                     **ただし `--dryrun` のときは警告にして続行**
EP40_CODEX_B:1275  8. `facts[fact_id].verified == false` かつ `required == true` → **exit 1**
                     （`--dryrun` では警告にして続行）
```

これは「スタブでは通るが本番では落ちる」＝**ドライランで検出できない失敗を作る分岐**であり、`is_stub` 禁止の趣旨と矛盾する。加えて既存の `check_lech_accuracy.py` は `--dryrun` で**成果物の書き出しごとスキップ**する分岐を持っている（`if not args.dryrun: OUT.write_text(...)`）。

### 修正文字列（EP40_CODEX_B `:625` / `:1275`）

```markdown
| `true` | `false` | **exit 1**（台本工程に差し戻し）。
  ★`--dryrun` でも exit 1 は変えない。判定ロジックを実行モードで分岐させない。
  ドライランで「本番なら落ちる状態」を通すと、ドライランの意味が消える。
  `--dryrun` が変えてよいのは **出力先パス（`_dryrun/` 配下）と入力素材（スタブ）だけ**であり、
  **判定・重大度・exit code は一切変えない。**
```

---

## §8. 「完成」の定義 — 【該当なし】

すべての文書で、完了条件が**既存スクリプトの exit 0** に紐づけられている。自己申告での完了宣言を明示禁止している。

- `EP39 v002:24` 「**THE ONE RULE:** validator PASS ＝ done ではない。**独立した受入スクリプトが実 `final.mp4` を測って全ハードGATEを通って初めて done。** 自作の品質ゲートを書いて「合格」と宣言するのは禁止。GATEを緩めて通すのも禁止。」
- `EP40 v002:38` 同趣旨 ＋ 「予約は `--emit-receipt` で出た receipt（`video_sha256` 一致）が無い限り不可。」
- `EP40 v002:1495` 「**全て exit 0 でなければ `package_ready` にしない。自己申告のQCは無効。**」
- `EP39_CODEX_A:51-61` 完了条件が全て `scripts/check_*.py … が exit 0` の形。
- `EP39_CODEX_A:353` 「**閾値はスクリプト内の定数が唯一の正**…値をここに書き写して信じるな。**実行して exit 0 を得ること。**」
- `EP40_CODEX_A:171` 「判定は `python scripts/check_script_length.py <script> --json` が**唯一の正**。自己申告・体感による判断は禁止。」
- `EP40_CODEX_A:1173` 「**この3つが exit 0 になったら**、スレッドBに…と伝えてよい。」

**該当なし。**（ただし §13 のとおり、その exit 0 の中身が v001 実装のままである点は別問題。）

---

## §9. AEの既知の罠 — 【該当なし】

9項目の網羅状況を実機で照合した。

| 罠 | EP39 v002（プロンプト内） | EP39_CODEX_B §5.8 | EP40 v002 §9.8 | EP40_CODEX_B §7.7 |
|---|---|---|---|---|
| `setTemporalEaseAtKey` の次元（spatial は要素1個） | `:674-675` ✅ | `:643` ✅ | `:1038` ✅ | ✅ |
| ローカライズOM/RSテンプレ名（RS`最良設定` / OM`H.264 - レンダリング設定を一致 - 15 Mbps`） | `:676-677` ✅ | `:644` ✅ | `:1039` ✅ | ✅ |
| TextDocument の改行に `\n` 不可 | `:678` ✅ | `:645` ✅ | `:1040` ✅ | ✅ |
| `app.newProject()` は headless でハング | `:679` ✅ | `:646` ✅ | `:1041` ✅ | ✅ |
| `layer.motionBlur` はレイヤー個別 | `:682` ✅ | `:649` ✅ | `:1044` ✅ | ✅ |
| 2Dは `ADBE Rotate Z`（`ADBE Rotation` は null） | `:683` ✅ | `:650` ✅ | `:1045` ✅ | `:1240` ✅ |
| inPoint と outPoint の両方 | `:684` ✅ | `:651` ✅ | `:1046` ✅ | `:1241` ✅ |
| `conformFrameRate` | `:685` ✅ | `:652` ✅ | `:1047` ✅ | `:1242` ✅ |
| ビルド遅延・完了マーカーのポーリング / `app.quit()` | `:680-681` ✅ | `:647-648` ✅ | `:1042-1043` ✅ | `:1238` 系 ✅ |

追加で GPU=SOFTWARE / bitsPerChannel=8 / taskkill / Python側で数値事前計算 / em-dash 豆腐 も両話に記載あり。

**該当なし（9項目すべて4文書に存在）。**
※ ただし em-dash 対策が **AEレイヤーに限定**されている点は §3 で BLOCKER として計上済み。

---

## §10. preflight / acceptance の切り分けと支出前停止 — 【該当あり／HIGH】

### EP40: 該当なし（模範）

`EP40 v002:1463-1493` はゲートを**支出順に明示的に並べている**:

```
**ゲートは以下の順で走らせる。★語数ゲートが最初** — TTS とレンダーに課金する前に落とすため。

# 0. ★語数ゲート（最優先。課金の前に必ずここで止める）
#    → 2,048–2,226語の外なら exit != 0
# 1. 水増しゲート        check_padding.py
# 2. 事実性ゲート        check_lech_accuracy.py
# 3. スロット/ビート契約  validate_lech_slots.py / validate_lech_beats.py
# 4. ★VO速度検証（ナレ生成直後・ミックス前）  measure_vo_wpm.py
#    → 168.0–190.0 wpm の外なら音声を破棄して再発注
# 5. レンダ前プリフライト  preflight_render_gate.py --ep lech
# 6. 本編の最終受入        check_final_acceptance.py 40 --render … --emit-receipt
```

さらに `:1434`「**有料。オーナー承認済みの範囲でのみ実行。本設計フェーズでは起動しない**」、`:1454`「**有料プロバイダジョブを一切起動しない**…C5 の画像生成は**オーナーが明示的にGOを出した後**」と支出境界が明記されている。

### EP39: **該当あり**

```
$ grep -c "preflight_render_gate" episodes/_planning/EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md
0
$ grep -c "preflight_render_gate" episodes/_planning/EP39_frazier_CODEX_A_ASSETS.v001.md \
    episodes/_planning/EP39_frazier_CODEX_B_BUILD.v001.md
0 / 0
$ ls scripts/preflight_render_gate.py
scripts/preflight_render_gate.py        ← 実在する
```

- **実在する `preflight_render_gate.py` を EP39 の3文書すべてが1度も呼んでいない。**（v001 には1件あったが v002 で落ちた）
- `check_script_length.py` も EP39 v002 の受入手順に**登場しない**（§2.1 で語数の話はしているが、ゲートとしては呼ばない）。
- §15 受入チェックリスト（`:590-608`）は**フラットな箇条書き**で、どれが preflight でどれが acceptance か、どれが課金前に効くのかが一切書かれていない。
- 支出前停止の記述は `:586`「中間ゲート（ナレ課金・ラフカット・初稿・タイトル/サムネ）では**止まらない**」のみで、**「課金の前にこのゲートで止まる」という記述が無い。** ElevenLabs（有料）は C9 で起動するが、その直前に走らせるべきゲートが指定されていない。

### 修正文字列（EP39 v002 §15 の冒頭に新設）

```markdown
### 15.0 ゲートの実行順（★支出の前に落とす。この順を変えない）

| 段階 | いつ | コマンド | 何を守るか |
|---|---|---|---|
| **P0 preflight** | 台本配置直後・**課金の前** | `./.venv/Scripts/python.exe scripts/check_script_length.py episodes/PD-2026-039-frazier/03_script/script.en.v001.md --json` | 尺band。ここで落ちれば TTS 課金ゼロ |
| **P1 preflight** | shotlist 確定直後・**レンダーの前** | `./.venv/Scripts/python.exe scripts/check_padding.py --ep frazier --json` | 水増し |
| **P2 preflight** | shotlist 確定直後・**レンダーの前** | `./.venv/Scripts/python.exe scripts/check_asset_reuse.py --ep frazier` | first_use_share ≥0.70（§6.1）。レンダー後に直すと作り直し |
| **P3 preflight** | AE spec 確定直後 | `./.venv/Scripts/python.exe scripts/ae/build_frazier_ae_jsx.py --validate` | anchor 未解決・配置制約 |
| **P4 preflight** | **ナレ生成直後・ミックスの前** | 実VO長を測り §2.3 の沈黙再配分を実行。VO < 610秒なら停止して報告 | runtime_band。ミックス後に気づくと全工程やり直し |
| **P5 preflight** | **本編レンダーの前** | `./.venv/Scripts/python.exe scripts/preflight_render_gate.py --ep frazier` | 画像長辺・欠損素材。レンダー時間の空費を防ぐ |
| **A1 acceptance** | CaseFilm レンダー後 | `./.venv/Scripts/python.exe scripts/check_final_acceptance.py 39 --json` | 中間確認 |
| **A2 acceptance** | **AE合成後の実ファイル**（最終・唯一の done 判定） | `./.venv/Scripts/python.exe scripts/check_final_acceptance.py 39 --render episodes/PD-2026-039-frazier/08_edit/frazier_final_bgm.v003_ae.mp4 --emit-receipt` | 全ハードGATE ＋ receipt |

**有料ジョブ（ElevenLabs）は P0–P2 が exit 0 になるまで起動しない。**
**本編レンダーは P5 が exit 0 になるまで起動しない。**
```

---

## §11. R2/R3 のリスク封じ込め — 【該当なし（v002本体）】

### EP39 v002: 十分

`:336-351` の §8.1 / §8.2 が3点すべてを具体的に封じている。

```
:340 | 1 | **Christopher Speelman**（存命の有罪確定者＝R3トリガー） | **裁判記録事実のみ。**
      「2023年6月22日に第三級殺人・住居侵入で有罪答弁、強姦は不抗争、25〜50年、
      2046年まで仮釈放不可」。**推測・動機付け・人物描写・映像化を一切しない。**名前は幕4で1回のみ。
:341 | 2 | **Edna Laughman**（85歳・性的暴行被害者） | 描写は 無人の台所／開いたままの網戸／
      床に落ちた錠剤の瓶／朝の庭 の象徴のみ。**身体・被害・暴力の再現は全面禁止。顔・肖像を作らない。**
:342 | 3 | **Holtz / Blevins / Roadcap** | §1983 の**主張（allegation）であって認定事実ではない**。
      …**「捏造した」と断定しない。**…**動機の断定は禁止。**
:346 - Barry Laughman / Edna Laughman / Christopher Speelman / Holtz / Blevins / Roadcap の
      いずれについても、顔が識別できる肖像・AI生成の似顔・実写映像・ディープフェイクは全面禁止。
:348 - **サムネにも実在人物の肖像を使わない。**（§9 の3案は全て無人）
:349 - **読める判決文・鑑定書・供述調書を作らない。**とくに 偽の鑑定書ビジュアルは Cayward の
      主題と紛らわしいので、書式が本物に見える画像は禁止
```

センシティブ描写の非グラフィック化も画像プロンプト側で機械的に担保されている（`:413` 共通ネガティブに `gore, blood, violence, restraint, child, legible document, official letterhead, readable report`。`:416` 「**外すな**」）。§9.2 のサムネ3案は全て「人物ゼロ」。

### EP40 v002: 十分

`:463-472` の §5.5 が未成年・被害者・警察官・住所・書類・自死描写を個別に封じ、`:150-156` の R8 で**正規表現による機械検査**まで落としている。`:471` 「Baker のケースの自死は**画で描かない**（ナレのみ・カットは閉じたドアの外観）」、`:472` 「Lech の amicus brief に含まれる実際の被害写真（p.6-7）は使用禁止」。

**v002 本体は該当なし。**

### ただし警告（項目13で BLOCKER として計上）

`EP39_CODEX_A/B` には Speelman / Laughman が**1文字も出てこない**:

```
$ grep -c "Speelman\|Laughman" EP39_frazier_CODEX_A_ASSETS.v001.md \
    EP39_frazier_CODEX_B_BUILD.v001.md EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md
EP39_CODEX_A : 0
EP39_CODEX_B : 0
EP39 v002    : 12
```

A/B は「主役未確定」時代の文書なので R3隣接の封じ込めを**構造的に持ち得ない**。A/B を単独で読んだ Codex は §8.1 の逐語ロックに到達しない。→ §13 参照。

---

## §12. EP40「最高裁が決めた」禁止の全面適用 — 【該当あり（部分カバー）／HIGH】

### 機械化されている部分（該当なしの根拠）

`EP40 v002:97-118` で正規表現ゲートとして定義されている:

```python
# R1 — パッケージゾーンでの Supreme Court 全面禁止
BANNED_ZONE = re.compile(r"supreme\s*court|最高裁|SCOTUS", re.IGNORECASE)
# R2 — 本文の文脈制限（★2文窓）
ALLOWED_CONTEXT = re.compile(
    r"declined to hear|refused to hear|denied review|denial of review|"
    r"did not take the case|cert(iorari)?\s+(was\s+)?denied|let the ruling stand|"
    r"never ruled on|it declined|expressed no view|petition", re.IGNORECASE)
# R3 — 肯定的動詞の禁止（Supreme Court の後 60文字以内）
BANNED_VERB = re.compile(r"\b(ruled|held|decided|upheld|affirmed|found|concluded|sided)\b", re.IGNORECASE)
```

台本4箇所の実測（`EP40_lech_script.en.v001.md`）:

```
$ grep -n "Supreme Court" episodes/_planning/EP40_lech_script.en.v001.md
71:  …the family's own petition to the Supreme Court, described in those words…
115: He asked the Supreme Court to take the case. On June 29, 2020, it declined.
135: In November 2024, when the Supreme Court declined to hear Vicki Baker's case…
145: …six years after the Supreme Court declined to hear him…
```

4箇所とも R2（2文窓）・R3 を通る。**設計書の「該当4箇所はすべてこの2文窓で pass する」という主張は正しい。**
タイトルA/B（`:1306-1307`）・サムネ3案（`:1329,1340,1351`）にも `Supreme Court` は無く、`:1318` で明示禁止している。

### 該当あり: カバーされていないゾーン

| ゾーン | R1（禁止語ゾーン）| 実際のカバー |
|---|---|---|
| タイトル | ✅ `title_candidates[]`, `package.title` | OK |
| サムネ | ✅ `thumb_headlines[]` | OK |
| フック | ✅ 本文の一部として R2/R3 | OK |
| 本文 | ✅ R2/R3 | OK |
| **ビートラベル（AE `beats.json` の `top`/`bottom`/`caption`/`footnote`）** | ❌ **R1 の対象外** | **散文の注意書きのみ** |
| **`figures[].text`（ActTitle 以外の kind）** | ❌ R1 は `ActTitle` kind のみ | 未カバー |
| **連動 Short の台本** | ❌ 検査対象ファイル一覧に無い | 未カバー |

- `:90` の検査対象ファイル一覧には `beats.json` の `top/bottom/caption/footnote` が入っているが、**R1 の適用対象（`:98`）には入っていない。**
- ビートラベルへの禁止は `:901` の散文注意のみ:
  ```
  > **`footnote` に "SUPREME COURT" を書かない。** 不受理の事実は幕3のナレと Remotion timeline 図版で扱う。
  ```
  → **正規表現ゲートになっていない。**「メモに頼らずゲートにする」というメタルールに反する。
- Short: `:1534` の premortem #8 は「`09_package/*` と Shorts の台本も検査対象に含める」と書いているが、`:87-93` の検査対象ファイル一覧に **Shorts の台本パスが無い**。仕様が自己矛盾している。

### 該当あり: R3 のスコープが曖昧で、設計書自身の概要欄を落とす可能性

`:117` の R3 は「**本文全体**で」と書かれているが、`:87-93` の検査対象には `09_package/*.txt` が含まれる。Codex がスコープを「検査対象ファイル全部」と解釈すると、設計書自身の §12.3 概要欄が落ちる:

```
:1362  The Supreme Court has never decided the underlying question.
       └─ "Supreme Court" の直後 18文字に "decided"（BANNED_VERB）→ R3 FAIL
```

**どちらの解釈も可能な書き方になっており、Codex がどちらを実装しても「仕様どおり」になってしまう。**

### 修正文字列（EP40 v002 §0.4）

```markdown
**R1 — 禁止ゾーンでの `Supreme Court` 全面禁止（★ゾーンを全面拡張）**

次のフィールドに部分一致で1回でも出たら FAIL:
```python
BANNED_ZONE = re.compile(r"supreme\s*court|最高裁|SCOTUS", re.IGNORECASE)

R1_ZONES = [
    # パッケージ
    "09_package/*.json :: title_candidates[]",
    "09_package/*.json :: thumb_headlines[]",
    "09_package/*.json :: package.title",
    # ★Remotion 図版（kind を問わず全部。ActTitle 限定をやめる）
    "remotion/src/data/lech_film.json :: figures[].text",
    "remotion/src/data/lech_film.json :: figures[].lines[]",
    "remotion/props/lech*.json :: subtitle",
    # ★AE ビートラベル（新規追加。ここが従来抜けていた）
    "08_edit/ae_hero/beats.json :: top",
    "08_edit/ae_hero/beats.json :: bottom",
    "08_edit/ae_hero/beats.json :: caption",
    "08_edit/ae_hero/beats.json :: footnote",
    "08_edit/ae_hero/beats.json :: tally[].place",
    "08_edit/ae_hero/beats.json :: tally[].circuit",
    "08_edit/ae_hero/beats.json :: tally[].verdict",
    "08_edit/_dryrun/ae_hero/beats.json :: 上記すべて",
    # ★〔CARD〕タイポ
    "03_script/lech_slots.v002.json :: cards[].text",
    # ★Short
    "09_package/short_script.v002.md :: 全文",
    "09_package/short_pinned_comment.v002.txt :: 全文",
]
```
> `§9.4.2 b06 の footnote に "SUPREME COURT" を書かない` は散文の注意ではなく、
> 上記 R1 で**機械的に止まる**ようにする。散文の禁止は守られない前提で設計する。

**R3 — 肯定的動詞の禁止（★スコープを明示する）**

適用範囲は **`03_script/script.en.v002.md` の本文のみ**とする。
`09_package/description.txt` は R3 の対象外とする（理由: §12.3 の概要欄は
"The Supreme Court has never decided the underlying question." という
**否定文で正確に書く必要があり**、`decided` が 60文字以内に入るため R3 では必ず落ちる）。
概要欄には代わりに R3B を適用する:
```python
# R3B — 概要欄・固定コメント用。否定辞を伴わない肯定的動詞のみを禁止する
R3B_BANNED = re.compile(
    r"Supreme\s+Court(?!.{0,40}\b(never|not|no|declined|denied|refused)\b).{0,60}"
    r"\b(ruled|held|decided|upheld|affirmed|found|concluded|sided)\b",
    re.IGNORECASE | re.DOTALL)
```
```

---

## §13. v002 と Codex A/B の食い違い — 【該当あり／BLOCKER・全件列挙】

**結論: Codex A/B 4文書は全て v001 時代の数値で書かれており、v002 と両立しない。
さらに、すでに実装されリポジトリに存在するスクリプト群は v001 側の仕様で書かれている。**

### 13.1 EP39 — v002 と CODEX_A/B の食い違い（全件）

| # | 項目 | **v002（正典）** | CODEX_A / CODEX_B | 深刻度 |
|---|---|---|---|---|
| 1 | 総カット数 | 150–170（`v002:230`） | **226**（`A:112`, `B:260`） | **BLOCKER**（§2 B2） |
| 2 | distinct 素材点数 | ≥110（`v002:269,278`） | **176**（`A:120`, `B:260`） | **BLOCKER** |
| 3 | `first_use_share` | 記載なし（実質 110/160 = **0.6875 → FAIL**） | **176/226 = 0.779 → PASS**（`A:122`） | **BLOCKER** |
| 4 | SDXL 採用枚数 | **60枚**（`v002:273`） | **68枚**（`A:117`）／完了条件 A-3 は **≥75件**（`A:57`） | HIGH |
| 5 | i2v 使用回数 | 2回・18本（`v002:275`） | 18本・26カット（`A:118`） | LOW |
| 6 | **シーンID の中身** | S03=検死台の縁 / S08=無人の台所 / S12=指紋カード / S13=空の照合ファイル（`v002:424,427,429,430`） | **S03=一方向ミラー越し / S08=玄関の人影 / S09=パトカー後部座席 / S12=夜勤の廊下(factory) / S13=引かれたままの椅子**（`A:196,201,202,205,206`） | **BLOCKER** |
| 7 | AE カード枚数 | **8枚**（HERO_DATA のみ・`v002:299-306`） | **21枚 / 6族**（HERO_DATA 8 + ACT_TITLE 4 + EXHIBIT_DOC 3 + TIMELINE_TRACK 2 + MAP_DIAGRAM 2 + INTERSTITIAL_WIPE 4・`B:432-439`） | **BLOCKER** |
| 8 | AE 総尺 | **47.0秒 / 6.7%**（`v002:317`） | **95.3秒 / 13.5%**（最大106.3秒 / 15.1%）（`B:441`） | **BLOCKER** |
| 9 | **AE スロットの中身** | hb01 IQ 70 / hb02 1988 / hb03 Frazier引用 / hb04 指紋 / hb05 16年 / hb06 4,102年 / hb07 2046 / hb08 10州 | **HB1 取調べの継続時間 / HB3 存在しない証拠の件数 / HB5 失った年数 / HB6 虚偽自白の関与率 / HB7 判決の票数 / HB8 免罪年**（`B:486-493`） | **BLOCKER** |
| 10 | **E_VOTE_TALLY（票数）** | **使用禁止**（`v002:323`「**Frazier の票数は fact ledger に無い。数えて書けば捏造になる**」） | **`HB7_DECISION_VOTE`＝判決の票数・E_VOTE_TALLY を条件付き採用**（`B:492`） | **BLOCKER（捏造リスク）** |
| 11 | 幕の開始秒 | ACT II=127.7 / ACT III=239.2 / ACT IV=379.4（`v002:133,143,155`） | ACT_TITLE 配置制約 = **170.0 / 370.0 / 540.0 秒 ±1.5秒**（`B:611`） | **BLOCKER** |
| 12 | **AEスクリプト名** | `build_frazier_hero_jsx.py` / `composite_frazier_hero.py`（`v002:561,662-663`） | `build_frazier_ae_jsx.py` / `composite_frazier_ae.py`（`B:425-426,621,633`） | **BLOCKER** |
| 13 | R3隣接の封じ込め | Speelman / Edna / Holtz-Blevins-Roadcap を逐語ロック（12箇所） | **0箇所**（grep 実測） | HIGH |
| 14 | props 種類数 | 表は **3種**（`v002:537-539`） | プロンプト本文は「**props 4種**」（`v002:660`・v002 内部の自己矛盾） | LOW |

**実機で確認した致命点:**

```
$ ls -la scripts/ae/*frazier*
-rwxr-xr-x  9303 Jul 20 01:07 scripts/ae/build_frazier_ae_jsx.py     ← v002 が指定した名前と違う
-rwxr-xr-x  4072 Jul 20 01:07 scripts/ae/composite_frazier_ae.py     ← 同上
```

**すでに CODEX_B 仕様で実装済み。** しかもそのバリデータは6族すべてを必須にしている:

```python
# scripts/ae/build_frazier_ae_jsx.py:23
FAMILIES = {"HERO_DATA", "ACT_TITLE", "EXHIBIT_DOC", "TIMELINE_TRACK", "MAP_DIAGRAM", "INTERSTITIAL_WIPE"}
# :68-69
    if missing_families:
        raise SystemExit("FAIL frazier_ae: missing card families: " + ", ".join(sorted(missing_families)))
```

→ **v002 の「HERO_DATA 8枚だけ」の spec を渡すと、既存バリデータは必ず `missing card families: ACT_TITLE, EXHIBIT_DOC, INTERSTITIAL_WIPE, MAP_DIAGRAM, TIMELINE_TRACK` で FAIL する。**
かつ v002 `:709` は自ら「**実在しないスクリプト名・テンプレ名を使わない。使う前に必ずファイルを読んで実在を確認する。**」と書きながら、`:561,662-663` で実在しない `build_frazier_hero_jsx.py` の新規作成を指示している（＝既存実装と二重化する）。

### 13.2 EP40 — v002 と CODEX_A/B の食い違い（全件）

| # | 項目 | **v002（正典）** | CODEX_A / CODEX_B | 深刻度 |
|---|---|---|---|---|
| 1 | 総尺 | **734.47秒**（`v002:267`） | **741.4秒**（`A:179`, `B:444,479`） | **BLOCKER** |
| 2 | `hookSeconds` | **26.62**（`v002:280`） | **8.1**（`B:486`） | **BLOCKER** |
| 3 | `durationInFrames` | **22,034**（`v002:1145`） | **22,242**（`B:492`） | **BLOCKER** |
| 4 | AE カード枚数 | **8枚**（b01–b08・`v002:767-774`） | **23枚**（`B:35,91,125,553,833`。`B:831`「**旧設計はAEカード8枚だった。EP40では23枚に広げる。**」） | **BLOCKER** |
| 5 | Remotion `figures[]` | **28枠**（`v002:1087`） | **17枠**（`B:616,720,749,787`） | **BLOCKER** |
| 6 | MGビート合計 | 36（8+28・`v002:1106`） | 40（23+17・`B:754`） | HIGH |
| 7 | 総カット数 | **224**（`v002:416`） | **226**（`A:236,271`, `B:679`） | MEDIUM |
| 8 | distinct 素材 | **167**（factory 70 / i2v 18 / 静止画 79・`v002:422-423`） | **171**（factory **85** / i2v **16** / 静止画 **70**・`A:233-236`） | **BLOCKER** |
| 9 | SDXL 生成構成 | **25シーン × 6 = 150枚**（`v002:438,576`） | **50シーン × 3 = 150枚**（`A:25,247`） | **BLOCKER** |
| 10 | **シーンID の中身** | S10=粉塵と光(アスベスト) / S14=eminent domain / S16=脚注 / S17=2年後の空き地 / S18=Indiana / S19=Texas / S20=Tennessee / S22=Las Vegas（`v002:528-565`） | **S10=平穏な郊外の通り / S14=最初のパトカー / S16=封鎖テープ / S17=ブラインド越し / S18=通りの封鎖 / S19=無線機の手元 / S20=装備の脚元 / S22=夜の投光器と住宅地**（`A:907-914`） | **BLOCKER** |
| 11 | ビジュアルレーン | **昼**（真昼〜夕方）＋夜明け1箇所のみ（`v002:212`） | `A:914` **S22=夜の投光器と住宅地**、`A:678` golden hour など | HIGH |
| 12 | factory 本数 | **70本**（`v002:422,431`） | **85本**（`A:28,234,265`, `A:1148`） | HIGH |
| 13 | AE 待機本数 | `render/b0*.mp4` が **8本**（`v002:1063`） | `render/*.mp4` が **23本**、ビルド **21コンプ**（`B:1257`） | **BLOCKER** |
| 14 | accuracy_lock 出力 | `09_package/accuracy_lock.v002.json`（`v002:158`） | 実装は `accuracy_lock.v001.json`（`check_lech_accuracy.py:15`） | MEDIUM |
| 15 | R2 の窓 | **2文窓**（`v002:104-112`） | **実装は1文窓**（`check_lech_accuracy.py:88-90`） | **BLOCKER** |
| 16 | R4/R5/R7/R8 | 係属中断定禁止 / 限定免責禁止 / 中立2文の存在チェック / 未成年匿名化（`v002:120-157`） | **実装に一切存在しない**（`check_lech_accuracy.py` 全文確認） | **BLOCKER** |
| 17 | AE start の決め方 | **ハードコード秒**（`v002:767-774`） | EP39 は `anchor_phrase` 解決を必須にしている（一貫性の欠如） | LOW |

**実機で証明した致命点（B3）— 既存 `check_lech_accuracy.py` が確定台本を偽陽性で落とす:**

```
$ cat scratchpad/probe.py
import importlib.util; from pathlib import Path
spec = importlib.util.spec_from_file_location("acc", r"...\scripts\check_lech_accuracy.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
p = Path(r"...\episodes\_planning\EP40_lech_script.en.v001.md")
v = []; m.check_file(p, v)
print("VIOLATIONS:", len(v))
for x in v: print(" -", x.get("rule"), "|", (x.get("sentence") or x.get("text") or "")[:120])

$ ./.venv/Scripts/python.exe scratchpad/probe.py
VIOLATIONS: 2
 - R2_context | ?kCARD: $5,000?l That figure appears in the family's own petition to the Supreme Court, described in those words, as help
 - R2_context | He asked the Supreme Court to take the case.
```

- **偽陽性2件。** v002 `:112` が予告した「"He asked the Supreme Court to take the case." が1文窓では落ちる」がそのまま再現した。
- 実装の該当箇所（`check_lech_accuracy.py:88-90`）:
  ```python
  for s in sentences(text):                                    # ← 1文ずつ
      if re.search(r"Supreme\s+Court", s, re.IGNORECASE) and not ALLOWED_CONTEXT.search(s):
          violations.append({... "rule": "R2_context", "sentence": s})
  ```
- `ALLOWED_CONTEXT` に v002 が追加した `denial of review|it declined|expressed no view|petition` が**入っていない**（`check_lech_accuracy.py:18-22`）。
- 出力の `?kCARD` は **cp932 での文字化け**（§3 の実証を兼ねる）。

> 注: このゲートを素で実行すると `PASS lech_accuracy: 0 violation(s), 3 skipped pattern(s)` と出る。
> **台本がまだ `03_script/` に配置されていないため検査対象0件で通っているだけ**であり、
> 「緑だから安全」ではない。配置した瞬間に赤になる（＝EP38 retro の「偽の緑ゲート」と同型）。

### 13.3 修正文字列

**（a）EP39 v002 §14.1 C6（`:561`）と Codex プロンプト（`:662-663`）を差し替え:**

```markdown
| C6 | **既存の `scripts/ae/build_frazier_ae_jsx.py` と `scripts/ae/composite_frazier_ae.py`
       を改修する（新規作成ではない。同名以外のファイルを作らない）。**
       着手前に両ファイルを必ず読むこと。
       ★`build_frazier_ae_jsx.py:23` の `FAMILIES` は6族すべてを必須にしている
       （`missing card families` で SystemExit する）。本設計 §7 は HERO_DATA 8枚しか
       定義していないので、**そのままでは `--validate` が必ず FAIL する。**
       採る方針を1つだけ選び、勝手に両方を残さない:
         方針X（推奨・設計変更なし）: `FAMILIES` を `{"HERO_DATA"}` に縮小し、
           `missing_families` チェックを HERO_DATA のみに限定する。
         方針Y: §7 を CODEX_B §5.2 の6族21枚に拡張する（AE総尺 95.3秒 = 13.5%）。
           この場合 §7.1 のスロット表・§7.2 の配置検証・§5.3 のビート内訳38本を全部書き直す。
       いずれにせよ **E_VOTE_TALLY / 票数カードは使わない**（Frazier の票数は fact ledger に
       無く、書けば捏造。CODEX_B の `HB7_DECISION_VOTE` は**破棄**する）。
| 成果物 | `scripts/ae/build_frazier_ae_jsx.py` / `scripts/ae/composite_frazier_ae.py`（既存を改修）|
```

**（b）EP39 v002 の冒頭（`:7` の直後）に「A/B文書の効力」節を新設:**

```markdown
## 0.0 ★`EP39_frazier_CODEX_A_ASSETS.v001.md` / `EP39_frazier_CODEX_B_BUILD.v001.md` の扱い

A/B は **v001 時代（主役未確定）の文書**であり、v002 と衝突する。効力を次のとおり確定する。

| 節 | 効力 |
|---|---|
| A §3（素材配分 226カット / distinct 176 / first_use_share 0.779）| **有効。v002 §6.1 の「150–170カット / distinct 110」を上書きする**（0.6875 では `check_asset_reuse` が落ちる）|
| A §5.5（factory 全点目視QC・`eyeballed_content`）| **有効。必ず実施する** |
| A §4.2 の**シーンID対応表（S01–S50 の主題）**| **無効。v002 §10.1 / §10.2 が勝つ。** 同じ ID に別の主題が割り当てられているので、A の表で画像を作ると本編タイムラインと絵が一致しない |
| B §5.2（AE 6族21枚・95.3秒）／ B §5.5 の HB スロット表 | **v002 §7 と衝突。C6 の方針X/Yで一本化するまで着手しない** |
| B §5.5 `HB7_DECISION_VOTE`（票数・E_VOTE_TALLY）| **恒久破棄。台帳に無く、書けば捏造**（v002 §7.3）|
| B §5.7 の実行コマンド | **有効（スクリプト名は `*_ae` が正）。ただし末尾の `&` は削除する**（§4）|
| B §5.8（AEの罠15項目）| **有効** |
| A/B のいずれにも無い R2/R3 封じ込め（§8）| **v002 §8 が唯一の正。A/B に記載が無いことを「制約なし」と読まない** |
```

**（c）EP40 v002 §0.4 の末尾に追記:**

```markdown
### 0.4.9 ★既存実装 `scripts/check_lech_accuracy.py` は v001 仕様である（必ず改修する）

このファイルは**すでに存在するが、v001 の1文窓のまま**であり、確定台本に対して
**偽陽性2件**を出すことを実測済み:

```
$ ./.venv/Scripts/python.exe -c "<check_file を確定台本に適用>"
VIOLATIONS: 2
 - R2_context | …the family's own petition to the Supreme Court, described in those words…
 - R2_context | He asked the Supreme Court to take the case.
```

必須の改修（1つでも欠けたら未完了）:
1. `check_file()` の R2 を **1文窓 → 2文窓**にする
   （`for i, s in enumerate(sents): window = " ".join(sents[i:i+2])`）
2. `ALLOWED_CONTEXT` に `denial of review|it declined|expressed no view|petition` を追加する
3. **R4（係属中2件の結果断定禁止）/ R5（限定免責の全面禁止）/ R7（中立2文の存在チェック）/
   R8（未成年匿名化）を新規実装する**（現状すべて未実装）
4. `R1_ZONES` を §0.4 R1 の拡張版（beats.json の top/bottom/caption/footnote/tally[] と
   Short 台本を含む）に差し替える
5. 出力先を `09_package/accuracy_lock.v002.json` に変える
6. `main()` 冒頭に `sys.stdout.reconfigure(encoding="utf-8")` を入れる（§X。現状 cp932 で文字化け）
7. `--dryrun` で判定・exit code を変えない（§7。出力先だけ変える）

**注意: 現状このゲートは `PASS lech_accuracy: 0 violation(s), 3 skipped pattern(s)` と出るが、
これは台本が `03_script/` にまだ無く検査対象0件だからである。緑を「安全」と読まないこと。
`skipped` が1件でもある間は PASS を信用しない。**
```

**（d）EP40 v002 §0（`:25` の直後）に「A/B文書の効力」節を新設:**

```markdown
## 0.0 ★`EP40_lech_CODEX_A_ASSETS.v001.md` / `EP40_lech_CODEX_B_BUILD.v001.md` の扱い

「v001 は破棄」という指示は **`EP40_lech_DESIGN_and_CODEX_PROMPTS.v001.md` に対するもの**であり、
CODEX_A / CODEX_B は破棄ではなく**部分的に有効**である。効力を次のとおり確定する。

| 節 | 効力 |
|---|---|
| **A §7.5（factory のファイル名を信用しない・コンタクトシート・`eyeballed_content`）**| **有効。必須。本書 §5.9 として本文に取り込む**（v002 本文から欠落していた）|
| A §6（静止画 QC の Q6/Q7 目視・全150枚）| **有効** |
| A §3.4 の素材配分（factory 85 / i2v 16 / 静止画 70 / 226カット）| **無効。本書 §5.1（factory 70 / i2v 18 / 静止画 79 / 224カット）が勝つ** |
| A §5 のシーン一覧（50シーン × 3）| **無効。本書 §5.7（S01–S25 × 6）が勝つ。** 同じ ID に別主題が割り当たっている |
| B §7（AEカード23枚）| **無効。本書 §9.2 の b01–b08（8枚）が勝つ。** B:831「23枚に広げる」は破棄 |
| B §6（figures 17枠）| **無効。本書 §10（28枠）が勝つ** |
| B の総尺 741.4秒 / hookSeconds 8.1 / 22,242F | **無効。本書 §3.1（734.47秒 / 26.62 / 22,034F）が勝つ** |
| **B §0.2（`is_stub` で処理を分岐させない）**| **有効。必須** |
| B §3.4（`lech_dryrun/` への staging）| **有効** |
| B §7.7（AEの罠12項目）| **有効。ただし本書 §9.8 の13項目が上位** |
```

---

## 付録: 実行した検証コマンド一覧

```bash
cd C:/Users/aab15/Documents/prime-documentary

# 対象ファイルの存在とサイズ
wc -c episodes/_planning/EP39_frazier_*.md episodes/_planning/EP40_lech_*.md

# 項目3
grep -rn "reconfigure" episodes/_planning/EP39_*.md episodes/_planning/EP40_*.md          # → 0件
grep -rn "stdout.reconfigure" scripts/*.py | head -20                                     # → 多数（慣習）
for f in scripts/ae/build_frazier_ae_jsx.py … ; do grep -c 'stdout.reconfigure' $f; done  # → 9/9 が 0
./.venv/Scripts/python.exe -c "'—'.encode('cp932')"                                       # → UnicodeEncodeError

# 項目4
grep -n "nohup\|&$\|デタッチ" episodes/_planning/EP{39,40}*.md
ls "/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/" | grep -iE "AfterFX|aerender"

# 項目5
du -sh remotion/public                                                                    # → 48G
grep -n "public_slim\|--public-dir\|publicDir" episodes/_planning/EP{39,40}*.md            # → 0件

# 項目2
sed -n '630,643p' scripts/check_final_acceptance.py                                       # thumbnail グロブ
grep -n "MIN_FIRST_USE_SHARE\|MAX_USES" scripts/check_asset_reuse.py                      # → 0.70 / 1,2,2
grep -n "thumbnail_selected\|thumb_{1" episodes/_planning/EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md

# 項目9
grep -n "setTemporalEaseAtKey\|最良設定\|newProject\|ADBE Rotate Z\|conformFrameRate\|motionBlur\|outPoint" \
  episodes/_planning/EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md \
  episodes/_planning/EP39_frazier_CODEX_B_BUILD.v001.md \
  episodes/_planning/EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md \
  episodes/_planning/EP40_lech_CODEX_B_BUILD.v001.md

# 項目10
ls scripts/preflight_render_gate.py scripts/check_script_length.py scripts/measure_vo_wpm.py
grep -c "preflight_render_gate" episodes/_planning/EP{39,40}*.md

# 項目11
grep -c "Speelman\|Laughman" episodes/_planning/EP39_frazier_CODEX_A_ASSETS.v001.md \
  episodes/_planning/EP39_frazier_CODEX_B_BUILD.v001.md \
  episodes/_planning/EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md                        # → 0 / 0 / 12

# 項目12
grep -n "Supreme Court" episodes/_planning/EP40_lech_script.en.v001.md                     # → 4箇所

# 項目13
ls -la scripts/ae/*frazier* scripts/ae/*lech*
sed -n '20,70p' scripts/ae/build_frazier_ae_jsx.py                                        # FAMILIES 6族必須
cat scripts/check_lech_accuracy.py                                                        # v001 仕様
./.venv/Scripts/python.exe scripts/check_lech_accuracy.py                                 # → PASS（対象0件の偽の緑）
./.venv/Scripts/python.exe <probe.py>                                                     # → VIOLATIONS: 2（偽陽性）
```
```
