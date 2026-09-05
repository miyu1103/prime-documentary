# EP39 frazier — Codex スレッドB「実装」引き継ぎ（v001 / 2026-07-19）

```
あなたは Prime Documentary EP39 の【実装スレッド】担当です。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
このファイルだけを読んで作業できるように全数値・全パス・全コマンドをここに書いてある。
他のファイル（設計書 v001 / スレッドAのプロンプト）を読む必要はない。読まない前提で書かれている。
リポジトリ内の既存スクリプトは「読め」と指示された箇所だけ必ず実際に読むこと。
```

---

## 0. このスレッドの責務（これ以外はやらない）

**コード律速。素材の完成を待たずに、今すぐ全部の実装とテストを終わらせる。**

やること:
1. Remotion オープニング `Frazier39Opening.tsx`（60fps・3.0秒・props量産対応）
2. 本編コンポジション（`CaseFilm` へのデータ供給＋オーバーレイ層の追加）
3. `scripts/build_frazier_film.py` — **素材台帳を消費して `frazier_film.json` を作る**（反復禁止ゲート準拠）
4. **After Effects の守備範囲拡大**: hero データカードに加えて、幕タイトル／証拠書類／時系列／地図図解／幕間ワイプの **6カード族**のビルダ＋コンポジタ
5. **字幕の構文境界分割の新実装**（現行の文字数ベース分割を置き換える）
6. サムネイル3案
7. 台本スロット契約（未確定は `null` で受けてゲートで止める）
8. **スタブ素材での通しドライラン**（Aの完了を待たずに全経路を実測で通す）

やらないこと（**スレッドAの担当。手を出すな**）:
- SDXL 静止画の生成、depth map の生成
- factory クリップの選定・ステージング・目視QC
- Wan i2v モーション生成
- `remotion/public/frazier/**` への**素材ファイルの配置**（スタブを除く。§2.3）
- `episodes/PD-2026-039-frazier/05_visuals/asset_manifest.v001.json` への書き込み（**読むだけ**）
- 台本本文の執筆（別スレッド。あなたは契約とゲートだけ用意する）

---

## 1. もう一方のスレッドとの境界（契約は1ファイルだけ）

```
スレッドA（素材生成）  ──[ 05_visuals/asset_manifest.v001.json ]──>  スレッドB（あなた）
```

- **あなたが読む唯一の共有物** = `episodes/PD-2026-039-frazier/05_visuals/asset_manifest.v001.json`
- **このファイルに書き込むな。読むだけ。** Aが所有している。
- Aは長時間GPUジョブ（SDXL 4–6h ＋ i2v 9–27h ＋ 目視QC 3h）を回しているので、**あなたが着手する時点ではまだ存在しない可能性が高い。**
- → **あなたは `05_visuals/asset_manifest.stub.v001.json`（あなたが自分で作るダミー台帳）で全経路を完走する。** §2.3。
- **スタブと本番でコードパスを分岐させるな。** ローダは `--manifest <path>` を受け取るだけで、中身の扱いは同一。`if stub:` のような分岐を1行も書くな。
- 両スレッドが `episodes/PD-2026-039-frazier/` 配下のディレクトリを `mkdir -p` 相当で作る。**削除・上書きは禁止**（作成のみ冪等に）。

> **名前の衝突注意:** リポジトリ直下の `assets/asset_manifest.v001.json` は **factory 棚の全体索引という全く別のファイル**（読み取り専用）。あなたが読むのは **エピソード配下の** `episodes/PD-2026-039-frazier/05_visuals/asset_manifest.v001.json`。

---

## 2. 完了条件

### 2.1 台本なしで今すぐ緑にできるもの（**これが本スレッドの完了条件**）

| # | 条件 | 検証コマンド |
|---|---|---|
| B-1 | `npm run typecheck` が exit 0 | `cd remotion && npm run typecheck` |
| B-2 | `Frazier39Opening` が3案ともレンダでき、**1920x1080 / 60fps / 3.00s** | §3.5 の ffprobe 実出力 |
| B-3 | サムネ3案＋selected が 1280x720 PNG で出力され、320px 縮小で見出しが読める | §8 |
| B-4 | AEスモーク: **6カード族すべて**が1枚ずつビルド→aerender→ffprobe で 1920x1080/30fps/spec尺 | §5.8 |
| B-5 | スタブ台帳で `build_frazier_film.py` が完走し、**`check_asset_reuse.py` が exit 0** | §2.3 / §4.4 |
| B-6 | スタブ字幕で `check_caption_breaks.py` が exit 0 | §6.5 |
| B-7 | スタブ通しドライランで `check_motion_density.py` / `check_animation_mix.py` が exit 0 | §9.2 |
| B-8 | 台本スロットが未確定（`null`）のとき、パイプラインが**推測で進まず FAIL で停止する**ことを実測で確認 | §7.4 |

### 2.2 台本＋素材が揃ってから緑にするもの（後段）

| # | 条件 |
|---|---|
| B-9 | `check_script_length.py` が exit 0（2,048–2,226語） |
| B-10 | 本番台帳で `check_asset_reuse.py` が exit 0 |
| B-11 | AE 6カード族が **SKIP 0本**で合成される |
| B-12 | `check_final_acceptance.py 39 --render …v003_ae.mp4 --emit-receipt` が exit 0 |

### 2.3 スタブ台帳（**Aを待たないための仕組み**）

`scripts/make_frazier_stub_assets.py` を新規に書く。やること:

1. `remotion/public/frazier/{img,factory,motion,overlay}/` を作る
2. **ffmpeg / PIL で合成のダミーファイルを生成**（外部素材を一切使わない）
   - still 78枚: `3840x2160` の PNG。中央に `S01 v1` 等の巨大な白文字＋シーンごとに異なる背景色（HSV を通し番号で回す＝近似重複にならない）。ファイル名は `S01.png` `S01_02.png` … 本番と同一命名
   - **各 still に `<stem>_depth.png`**（同サイズのグレースケール放射グラデーション）
   - factory 93本: `1920x1080 / 30fps / 6.0s` の mp4。数字が動くカウンタ＋色相スクロール（＝静止フレームではない）
   - motion 19本: `1280x720 / 16fps / 41フレーム`（2.56s）の mp4
   - overlay 34本: `1920x1080 / 30fps / 8.0s` の粒子風ノイズ mp4
3. `episodes/PD-2026-039-frazier/05_visuals/asset_manifest.stub.v001.json` を **§4.2 のスキーマに完全準拠**して書く。全レコード `"stub": true`、`"status": "stub"`
4. `scene_code` は `S01`–`S50` を実際に散らす（distinct 50）。`act` も §3.6 の幕対応で埋める

**冪等**にすること（既存ファイルはスキップ）。**総容量は 3GB 以内に収める**（ダミーに 50GB 使うな）。

**★ 本番台帳が現れたら、`--manifest` の引数を差し替えるだけで本番に切り替わること。それ以外の変更が1行でも必要なら、その設計は間違っている。**

---

## 3. Remotion オープニング `Frazier39Opening`

> **重要な境界:** 本編タイムライン内の OP/ED は `remotion/src/components/Bookends.tsx` の `BrandOpening` / `BrandEndcard` が**唯一の正典**であり、**フォークしない**（`op_ed_bookends` ゲート）。ここで作る `Frazier39Opening` は**独立した 60fps タイトルカード資産**（サムネ動画・Short用リード・A/B用の別レンダ）であり、`CaseFilm` のタイムラインには**差し込まない**。

### 3.0 Composition 設定

`remotion/src/Root.tsx` に追加（既存 id `Opening` は使用済み。**衝突させるな**）:

```tsx
import {Frazier39Opening} from './compositions/Frazier39Opening';

<Composition
  id="Frazier39Opening"
  component={Frazier39Opening}
  durationInFrames={180}        // = 3.0s @ 60fps
  fps={60}
  width={1920}
  height={1080}
  defaultProps={{
    title: 'THEY CAN LIE',
    subtitle: 'FRAZIER V. CUPP · 1969',
    accent: '#E5B53A',
    hasLogo: true,
  }}
/>
```

- ファイル: `remotion/src/compositions/Frazier39Opening.tsx`（**新規**。既存 `compositions/Opening.tsx` を書き換えるな）
- 依存: `@remotion/motion-blur` は `remotion/package.json` に `^4.0.476` で**既に入っている**（確認済み）。バージョン不整合時のみ `npm i @remotion/motion-blur` を `remotion/` 直下で実行し、`remotion` 本体と同じメジャー系に揃える
- `remotion/remotion.config.ts` は**既に正典値。変更するな。** 以下と一致していることだけ確認せよ:

```ts
Config.setVideoImageFormat('png');            // 中間フレームはロスレスPNG
Config.setCodec('h264');                      // libx264 / CPU（NVENC禁止）
Config.setCrf(16);
Config.setX264Preset('slow');
Config.setPixelFormat('yuv420p');
Config.setColorSpace('bt709');
Config.setAudioCodec('aac');
Config.setAudioBitrate('320k');
Config.setConcurrency(os.cpus().length);      // 全コア並列
Config.setChromiumOpenGlRenderer('angle');    // GPU = angle
Config.setOverwriteOutput(true);
```

### 3.1 秒数ベースのタイムライン（全区間・fps=60 / 総尺 3.0s = 180F）

| 秒 | フレーム | 起きること |
|---|---|---|
| **0.00 – 0.50** | 0–30 | レイヤー1 グラデ背景がフェードイン（opacity 0→1、F0–24）。同時に**背景全体が scale 1.08 → 1.00 へ 3.0秒かけてゆっくり縮む**（`Easing.out(Easing.cubic)`・F0–180）。0.10s（F6）でロゴが scale 0.40→1.00 の spring 開始。0.15s（F9）でレイヤー2グリッドが spring reveal 開始（0.8s=48F）。0.25s（F15）でレイヤー3グローが spring 開始（scale 0.60→1.15 / opacity 0→0.85）。0.30s（F18）で**タイトル1文字目**がマスク下から切れ上がり開始。 |
| **0.50 – 1.00** | 30–60 | タイトルの各文字が **0.04s（=2.4F→切り上げ3F）ごとのスタッガー**で順に切れ上がる（各文字 spring `damping:16, mass:1`、translateY 110%→0%）。`Trail`（layers 6 / lagInFrames 1.2 / trailOpacity 0.45）で速い切れ上がりにモーションブラーが乗る。グリッドは 0→48px の縦ドリフト（`Easing.inOut(Easing.sin)`・F0–180）を継続。 |
| **1.00 – 1.40** | 60–84 | 0.95s（F57）で**金アクセント下線が左から scaleX 0→1 でワイプ**（spring `damping:16, mass:0.8`）。1.10s（F66）で**サブタイトル**が translateY 24px→0px ＋ opacity 0→1（spring `damping:20, mass:1`）。 |
| **1.40 – 2.20** | 84–132 | 全要素が定常。背景 scale とグリッドドリフトだけが動き続ける（画面は一瞬も静止しない）。**1.60s（F96）で背景に薄い紺のフラッシュ（opacity 0→0.10→0、F96–108、`Easing.out(Easing.cubic)`）を1回だけ入れて「取調室の扉が閉まる」拍を作る。** |
| **2.20 – 3.00** | 132–180 | 保持。**2.70s（F162）から全体を scale 1.00→1.02（`Easing.out(Easing.cubic)`・F162–180）で微かに押し込む**＝次カットへの運動量継承（velocity reset を作らない）。opacity は落とさない。 |

### 3.2 タイミング定数（**フレーム直書き禁止。fps から算出する**）

```ts
export const frazier39OpeningDurationInFrames = (fps: number) => Math.round(fps * 3.0); // 180 @60fps
const sec = (fps: number, s: number) => Math.round(fps * s);

const T = {
  bgIn: 0.00,        // 背景フェード/ズーム開始
  logoIn: 0.10,      // ロゴ
  gridIn: 0.15,      // グリッド出現
  glowIn: 0.25,      // グロー出現
  titleIn: 0.30,     // タイトル切れ上がり開始
  charStagger: 0.04, // 1文字ごとのディレイ（@60fps → 2.4F、Math.max(1, ...) で3F）
  accentIn: 0.95,    // アクセント下線ワイプ
  subIn: 1.10,       // サブタイトル
  flashAt: 1.60,     // 紺フラッシュ
  pushAt: 2.70,      // 終端の押し込み
} as const;
```

### 3.3 各要素のイージング・移動量・damping（確定値）

| 要素 | 開始F(@60) | 終了F | 変化量 | イージング |
|---|---|---|---|---|
| 背景 scale | 0 | 180 | `1.08 → 1.00` | `Easing.out(Easing.cubic)` |
| 背景 opacity | 0 | 24 | `0 → 1` | interpolate（**必ず scale と併用。opacity単独禁止**） |
| グリッド translateY | 0 | 180 | `0 → 48px` | `Easing.inOut(Easing.sin)` |
| グリッド reveal | 9 | 57 | `0 → 1`（最終 opacity は `reveal * 0.18`） | `spring{damping:200, mass:1}` / `durationInFrames = sec(fps,0.8)` |
| グロー scale | 15 | — | `0.60 → 1.15` | `spring{damping:18, mass:1.2}` |
| グロー opacity | 15 | — | `0 → 0.85` | 同 spring（scale と同期＝単独禁止） |
| タイトル各文字 translateY | `18 + i*3` | — | `110% → 0%` | `spring{damping:16, mass:1}` |
| タイトル各文字 opacity | `18 + i*3` | +約6F | `0 → 1`（spring値 0→0.25 を 0→1 にマップ・clamp） | 同 spring |
| タイトル Trail | 全域 | — | `layers=6 / lagInFrames=1.2 / trailOpacity=0.45` | — |
| アクセント下線 scaleX | 57 | — | `0 → 1`（`transformOrigin:'left center'`） | `spring{damping:16, mass:0.8}` |
| サブタイトル translateY | 66 | — | `24px → 0px` | `spring{damping:20, mass:1}` |
| サブタイトル opacity | 66 | — | `0 → 1` | 同 spring（translateY と併用） |
| ロゴ scale | 6 | — | `0.40 → 1.00` | `spring{damping:14, mass:0.9}` |
| ロゴ opacity | 6 | — | `0 → 1` | 同 spring |
| 紺フラッシュ opacity | 96 | 108 | `0 → 0.10 → 0` | `Easing.out(Easing.cubic)` |
| 終端押し込み scale | 162 | 180 | `1.00 → 1.02` | `Easing.out(Easing.cubic)` |

**禁止（実装時に自己チェック）:** イージング指定なしの等速 `interpolate` を使わない。`opacity` **だけ**が変化する要素を作らない。複数要素は必ずスタッガー。速い動きには `Trail`。

### 3.4 レイヤー構成（下から上。**主役の裏に最低3レイヤー**）

| z | レイヤー | 内容 |
|---|---|---|
| 0 | ベース | `AbsoluteFill` `backgroundColor: '#05070d'` |
| **1** | **グラデ背景** | `radial-gradient(120% 120% at 50% 35%, #0E1B33 0%, #0A1020 45%, #05070d 100%)`。scale 1.08→1.00 |
| **2** | **グリッド/ライン** | `repeating-linear-gradient` 縦横 1px / 間隔 **64px** / 色 `${accent}22`。全体 opacity = `gridReveal * 0.18`。`maskImage: radial-gradient(120% 90% at 50% 45%, black 35%, transparent 80%)`。translateY 0→48px |
| **3** | **グロー** | 中央に `width = W*0.62` `height = H*0.36` の `radial-gradient(closest-side, ${accent}88 0%, ${accent}22 45%, transparent 75%)` ＋ `filter: blur(28px)`。scale 0.60→1.15 |
| **3.5** | **紺フラッシュ** | 全面 `#0B1A2B`、F96–108 のみ opacity 0→0.10→0 |
| **4** | **主役タイトル** | `Trail` 内に `AbsoluteFill`（中央寄せ再指定）→ flex 横並びの1文字 `<span>`。外側 span `overflow:hidden` ＋ `paddingBottom:'0.12em'`、内側 span `transform: translateY(${y}%)`。`fontFamily:'"Oswald","Archivo",Impact,sans-serif'` / `fontWeight:800` / `fontSize:132` / `letterSpacing:-2` / `color:#F5F7FA` / `lineHeight:1.05` / `transform:'translateY(-70px)'` |
| **5** | **アクセント下線＋サブタイトル** | 縦並び（`gap:18`・`transform:'translateY(55px)'`）。下線＝`240×6`・`borderRadius:3`・`backgroundColor:accent`・`boxShadow:'0 0 24px ' + accent + 'aa'`・`transformOrigin:'left center'`。サブタイトル＝`fontSize:38` / `fontWeight:500` / `letterSpacing:6` / `textTransform:'uppercase'` / `color:'#C8CDD6'` |
| **6** | **ロゴ**（`hasLogo` のときのみ） | `position:absolute` `top:64` `left:72` `84×84` `borderRadius:20`、`linear-gradient(135deg, ${accent}, #ffffff22)`、`border: 2px solid ${accent}`、`boxShadow: '0 0 30px ' + accent + '66'` |

### 3.5 props 定義・バリアント・確認方法

```ts
export type Frazier39OpeningProps = {
  title: string;      // 主役タイトル。1文字ずつスタッガー。推奨 <= 14文字（132px で1行に収まる上限）
  subtitle: string;   // 下段。UPPERCASE前提・推奨 <= 32文字
  accent: string;     // アクセントカラー（HEX 6桁・"#" 込み）。既定 '#E5B53A'
  hasLogo: boolean;   // 左上のPDロゴマークを出すか
};
```

`remotion/props/` に置く量産用バリアント:

| ファイル | title | subtitle | accent | hasLogo |
|---|---|---|---|---|
| `props/frazier_op_a.json` | `THEY CAN LIE` | `FRAZIER V. CUPP · 1969` | `#E5B53A` | true |
| `props/frazier_op_b.json` | `IT IS LEGAL` | `POLICE DECEPTION IN THE ROOM` | `#1F6BFF` | true |
| `props/frazier_op_c.json` | `I DID IT` | `A CONFESSION THAT WAS FALSE` | `#E5B53A` | false |

```bash
cd C:/Users/aab15/Documents/prime-documentary/remotion
npm run typecheck
npm run studio            # = remotion studio。左のリストから "Frazier39Opening" を選ぶ

npx remotion render Frazier39Opening out/frazier_op_a.mp4 --props=./props/frazier_op_a.json
npx remotion render Frazier39Opening out/frazier_op_b.mp4 --props=./props/frazier_op_b.json
npx remotion render Frazier39Opening out/frazier_op_c.mp4 --props=./props/frazier_op_c.json
```

**検収:** ffprobe で **1920x1080 / 60fps / 3.00s** を実測。目視で ①静止フレーム0 ②文字が1文字ずつ順に立ち上がる ③切れ上がりの瞬間に残像（Trail）が見える ④下線が左から伸びる ⑤背景・グリッド・グローの3層が識別できる。

---

## 4. 素材台帳の消費と `frazier_film.json` の生成

### 4.1 反復禁止ゲート（**設計段階で超えておけ。後から直すと作り直し**）

```bash
python scripts/check_asset_reuse.py remotion/src/data/frazier_film.json
```

実装済み定数（`scripts/check_asset_reuse.py` L44-47。**読んで確認せよ**）:

| 種別 | 使用上限 | 判定条件（`kind_of()` L60-66） |
|---|---|---|
| factory | **1回** | パスに `/factory` を含む or `af-bg-` にマッチ |
| motion | **2回** | `.mp4/.mov/.webm` で終わる（`/factory` を含まない） |
| still | **2回** | 上記以外 |

全体条件: **`first_use_share = distinct_assets / cuts_with_asset >= 0.70`**

**EP39 の確定配分（226カット / distinct 176）:**

| 種別 | distinct | 使用回数 | 生成カット |
|---|---|---|---|
| factory | 90 | 各1回 | 90 |
| still | 68 | 42枚×2 + 26枚×1 | 110 |
| motion | 18 | 8本×2 + 10本×1 | 26 |
| **計** | **176** | | **226** |

検算: `176 / 226 = 0.779 >= 0.70`。**PASS。**

> **⚠ 旧設計の内訳「factory 50 + still 50（各2回）+ i2v 15（各2回）」は自分のゲートを通らない。**
> 検算: 50 + 100 + 30 = 180カット、distinct 115、`115/180 = 0.639 < 0.70` → **FAIL**。上限いっぱいに使う設計は原理的に share を下げる。上表を使え。

カット尺は既存 `scripts/build_case_film_assets.py` の実測サイクルをそのまま使う:
```
DUR_CYCLE = [1.7, 2.1, 5.6, 1.8, 3.0, 6.5, 2.0, 1.6, 4.2, 2.4, 5.2, 1.9]   # 平均 3.117s
```
（オーナー指示「毎回同じペースで画面が切替わるのは疲れる」への対応。**等間隔のメトロノームにするな。**）

### 4.2 台帳スキーマ（Aが出す。**あなたは読むだけ**）

```jsonc
{
  "episode_id": "PD-2026-039-frazier",
  "manifest_version": "v001",
  "status": "final",                              // "stub" はスタブ台帳
  "counts": { "still": 78, "factory": 93, "motion": 19, "total": 190,
              "overlays": 34, "distinct_scene_codes": 50 },
  "caps": { "still": 2, "factory": 1, "motion": 2 },
  "assets": [
    {
      "asset_id": "ST-039-001",          // ^(ST|FC|MO)-039-[0-9]{3}$
      "kind": "still",                    // "still" | "factory" | "motion"
      "max_uses": 2,                      // still=2 / factory=1 / motion=2
      "public_path": "frazier/img/S01.png",   // ★remotion/public/ からの相対。cuts[].src にそのまま入る
      "abs_path": "…",
      "source_path": "…",
      "scene_code": "S01",                // ★全kind必須。S01–S50
      "act": 0,                            // 0=hook/主舞台 1|2|3|4=幕
      "variant": 1,                        // still のみ 1..3
      "depth_map": "frazier/img/S01_depth.png",   // still のみ。それ以外 null
      "width": 3840, "height": 2160, "long_edge_px": 3840,
      "duration_sec": null, "fps": null, "frames": null,
      "sha256": "…", "bytes": 8123456,
      "median_luma": 41.2,
      "af_id": null, "theme": null, "subtype": null, "saw": null,
      "tags": ["interrogation", "night"],
      "source": "sdxl_juggernautXL",
      "license": "internal_generated",
      "reviewed": true, "on_theme": true,
      "qc": { "pass": true, "notes": "" },
      "stub": false
    }
  ],
  "overlays": [
    {
      "overlay_id": "OV-039-001",         // ^OV-039-[0-9]{3}$
      "category": "light_assets",          // light_assets | particle_assets | vfx_overlays | loops
      "public_path": "frazier/overlay/AF-LT-00123__dust_motes.mp4",
      "duration_sec": 8.40, "fps": 30,
      "blend_hint": "add",                 // add | screen | overlay
      "sha256": "…", "af_id": "AF-LT-00123"
    }
  ]
}
```

**使用ルール:**
- `assets` のうち **`qc.pass == true` のものだけ**を `cuts[].src` に使う
- `overlays` は **`cuts[].src` に入れない**（入れると distinct 数を水増しする不正になる）。静止画カットの上に重ねる合成レイヤーとして使う → §4.5
- `scene_code` / `act` / `tags` が「幕に合った絵」を選ぶ唯一の手がかり

### 4.3 `scripts/build_frazier_film.py`（新規）

**既存の `scripts/build_case_film_assets.py` を書き換えるな**（他エピソードが使っている）。台帳駆動の割り当てが必要なので EP39 専用に新規作成する。ただし**出力の JSON キーは既存 `remotion/src/data/kidsforcash_film.json` と完全に同じ**にすること（`CaseFilm` が読む形）:

```
episode_id, fps, narration, narrationSeconds, hookSeconds, hookLine, hook, cuts, captions, graphics, figures
```

`cuts` の1要素（実物から確認済み）:
```json
{"start": 0.0, "dur": 1.7, "kind": "footage",
 "src": "frazier/factory/AF-BG-04601__interrogation_room_table.mp4",
 "seed": "frazier-0", "treatment": "footage"}
```

**CLI:**
```bash
py -3.11 scripts/build_frazier_film.py \
  --manifest episodes/PD-2026-039-frazier/05_visuals/asset_manifest.stub.v001.json \
  --annotated episodes/PD-2026-039-frazier/03_script/script.annotated.v001.json \
  --captions  episodes/PD-2026-039-frazier/08_edit/captions.final.v001.json \
  --out       remotion/src/data/frazier_film.json
```
`--manifest` を本番パスに差し替えるだけで本番になること。**分岐を書くな。**

**割り当てアルゴリズム（この順に決定・推測禁止）:**

1. 台帳から `qc.pass == true` のプールを作り、kind ごとに分ける
2. カット境界を `DUR_CYCLE` で総尺ぶん敷き、各カットに `act`（台本の幕）を紐づける
3. 目標ミックスを守る: **factory 90カット / still 110カット / motion 26カット**。各カットの kind は `[factory, still, factory, still, motion, still, factory, still]` の循環で決め、在庫が尽きた kind は次に譲る
4. kind 内での1枚の選定は、次の優先順:
   a. `asset.act == cut.act` のもの（幕が一致）
   b. **直近8カット以内に同じ `scene_code` が出ていないもの**（連続で同じ被写体を出さない）
   c. `uses < max_uses` のもの（**超えたら絶対に選ばない**）
   d. `uses` が最小のもの
   e. それでも同点なら `asset_id` 昇順（決定的にする。乱数を使うな）
5. `treatment`: still → `"depth_parallax"`（`depth_map` が非 null であることを事前に検証。null なら **FAIL で停止**）。factory / motion → `"footage"`
6. 割り当て不能なカットが1つでも出たら **例外を投げて停止する**。空 `src` のカットや、同じ素材を上限超で使う「とりあえずの埋め」を絶対に作るな

**最後に自分で検算して print する**（ゲートの代わりにはならないが、走らせる前に落とせる）:
```
distinct=176 cuts=226 first_use_share=0.779 (floor 0.70)
factory max_uses=1 still max_uses=2 motion max_uses=2  violations=0
```

### 4.4 検証

```bash
python scripts/check_asset_reuse.py remotion/src/data/frazier_film.json
# PASS asset_reuse: 176 distinct assets over 226 cuts (mean 1.28x)
#   first-use share 78% (floor 70%)
```
**これが exit 0 になるまで先に進むな。**

### 4.5 オーバーレイ層（**同じ静止画を別物に見せる・反復対策**）

在庫は light 1,401 / particle 1,225 / vfx 1,196 点ある。**枚数を増やすより安い反復対策。**

1. `remotion/src/compositions/CaseFilm.tsx` を**先に読む**
2. `cut.overlay`（省略可・`string | null`）を受け付けるように**最小限の追加**をする。`cut.overlay ?? null` でガードし、**既存エピソードの出力がバイト同一のままであること**を確認する（`overlay` を持たない film.json は挙動が1ピクセルも変わってはいけない）
3. 実装: 静止画カットの上に `<OffthreadVideo src={staticFile(cut.overlay)} />` を `mixBlendMode`（`blend_hint` に対応: add→`'plus-lighter'` / screen→`'screen'` / overlay→`'overlay'`）＋ `opacity: 0.28` で重ねる。素材が尺不足ならループさせる
4. `build_frazier_film.py` は **still の全カットに** `overlays` を round-robin で割り当てる。**同じ overlay が連続2カットに来ないこと**
5. overlay は `check_asset_reuse` の対象外（`cuts[].src` ではないため）。**src に入れて distinct を水増しするな**

### 4.6 本編側の既定（変更するな）

- エンジン: `remotion/src/compositions/CaseFilm.tsx`（正典）。**EP39専用の新規コンポを作らない。**データで駆動する
- OP/ED: `components/Bookends.tsx` の `BrandOpening`（`OPENING_SEC=3.5`）/ `BrandEndcard`（`ENDCARD_SEC=9`）を **import して使う**（再実装・フォーク禁止 = `op_ed_bookends` ゲート）
- 1920×1080 / **30fps** / 全クリップを30fpsに統一
- トランジション: **0.3–0.5秒のクロスディゾルブ**。Sequence をトランジション長ぶん**オーバーラップ**させる（1フレームの黒/ジャンプを作らない）。カットをまたいで運動方向を継承する
- `AmbientMotion` オーバーレイを全ビートに載せ、静止フレームを作らない
- 平均ショット長 **≤6.0秒**、単一静止の保持 **≤3.0秒**
- **禁止**: 左→右の縦スイープライン／全画面の黄・金ウォッシュ／ズーム・パンのみの演出

---

## 5. After Effects — **守備範囲を6カード族に拡大する**（本エピソードの主要要求）

### 5.1 パイプラインの原則（EP38で実測確立。**これに従う。逸脱するな**）

1. **Remotion で本編を作り、その完成 mp4 に AE製カードを ffmpeg で overlay する。Remotion を再レンダしない。**
2. 各カード = **1920x1080 @ 30fps** の AEコンプ。**不透明フルフレームで書き出し**、`enable='between(t,start,end)'` で重ねる。**元の図版を完全置換＝二重描画なし。音声は `-c:a copy`。**
3. **Python が .jsx を生成する**（全数値をPython側で制御）。**カウントアップ等の数値文字列は Python で全事前計算**（JS側で数値整形しない）。
4. **サイドカー JSON が jsx とコンポジタの両方を駆動する**（単一の真実）。
5. **コンポジタは mp4 が欠損／サイズ違い／短尺のカードを SKIP する**（その区間は元のまま＝作品が壊れない）。
6. **出荷済みファイルを絶対に上書きしない**（`frazier_final_bgm.v002.mp4` → `frazier_final_bgm.v003_ae.mp4`）。

**★着手前に必ず読め（雛形。読まずに書くな）:**
- `scripts/ae/build_kfc_hero_jsx.py`（382行）— jsx生成・`count_keys()`・`ease()`（spatial判定）・`psName()` フォント解決・`addText()`・`revealUp()`・OM/RSテンプレ適用・完了マーカー書き出し
- `scripts/ae/composite_kfc_hero.py`（108行）— ffmpeg overlay・SKIPロジック・duration検証

作るもの（**EP38版を書き換えるな。新規に作れ**）:
- `scripts/ae/build_frazier_ae_jsx.py`
- `scripts/ae/composite_frazier_ae.py`

### 5.2 なぜAEに寄せるのか / どこをAEに寄せるのか

**Remotionでやると安っぽくなる箇所**をAEに移す。判断基準は「文字と図形が主役で、質感（グロー・ブラー・光の抜け）が効く画」。

| # | カード族 | 何を解決するか | 枚数 | 区間長 |
|---|---|---|---|---|
| F1 | `HERO_DATA` | 数値の山場（既存の5レイアウト） | 6必須＋2条件 | 5.5–6.5s |
| F2 | `ACT_TITLE` | **幕の転換。**Remotionのテキストアニメは「テンプレ感」が出る | 4 | 3.0s |
| F3 | `EXHIBIT_DOC` | **証拠書類の提示。**紙の質感・墨消し・スキャンラインはAEでしか出ない | 3 | 5.0s |
| F4 | `TIMELINE_TRACK` | **時系列の可視化。**ノードのスタッガー着地＋モーションブラー | 2 | 7.0s |
| F5 | `MAP_DIAGRAM` | **地図・図解。**ノードとコネクタの組み上げ | 2 | 6.5s |
| F6 | `INTERSTITIAL_WIPE` | **幕間トランジション。**二重ワイプはRemotionだと軽い | 4 | 1.2s |

**AE総尺:** 必須のみ 36.5 + 12.0 + 15.0 + 14.0 + 13.0 + 4.8 = **95.3秒**（705秒の 13.5%）。条件付きheroを含めて最大 106.3秒（15.1%）。
**上限: AE合計 ≤ 本編の18%（≤127秒）。** 超えたら「AEの作品」になってしまう。

### 5.3 共通仕様（全カード族に適用）

- 1920×1080 @ 30fps、コンプ名 prefix **`FRZ_`**
- 色: `GOLD=[0.898,0.710,0.227]` / `WHITE=[0.961,0.969,0.980]` / `SILVER=[0.588,0.627,0.682]` / `NAVY=[0.043,0.102,0.169]`
- フォント: 実行時に `app.fonts.allFonts` から解決（Anton regular / Oswald medium）。**サイレント代替を許さない**（`psName()` をそのまま流用）
- **黒シームdip**: head/tail 各 `4/30 = 0.1333s`（F6のみ `2/30`）。opacity 100→0 / 0→100、`ease(prop, 40)`
- **背景 still**（F6を除く）: `fill = max(W/sw, H/sh)*100`、scale `fill → fill*1.08`（ease 25）、position `[W/2−18, H/2+10] → [W/2+18, H/2−10]`（ease 20）
- **クールグレード**: solid `[0.04,0.07,0.13]`、`BlendingMode.MULTIPLY`、opacity 38（F2は46 / F3は52）
- **ビネット**: 黒 solid ＋ 楕円マスク `rx=W*0.62, ry=H*0.62`、`MaskMode.SUBTRACT`、feather `[260,260]`、opacity 62
- **字幕ロワーサード**（F6を除く全族）: 暗バー solid `[0.02,0.04,0.08]` `W×130` at `[W/2, H*0.90]`、opacity キー `0.2→0 / 0.5→64 / dur−0.4→64 / dur−0.1→0`。テキストは Oswald 42 WHITE tracking 20 at `[W/2, H*0.90−6]`、opacity `0.3→0 / 0.6→100 / dur−0.4→100 / dur−0.12→0`。**`one_line(maxchars=50)` で必ず1行に保つ**
- **使用する matchName は雛形に出てくるものだけ**: `ADBE Transform Group` / `ADBE Position` / `ADBE Scale` / `ADBE Opacity` / `ADBE Anchor Point` / `ADBE Rotate Z` / `ADBE Mask Parade` / `ADBE Mask Atom` / `ADBE Mask Shape` / `ADBE Mask Feather` / `ADBE Ramp`(-0001..-0005) / `ADBE Radial Wipe` / `ADBE Effect Parade` / `ADBE Text Properties` / `ADBE Text Document`。**これ以外のエフェクトを使うな**（実在確認していないものは無言で失敗する）

### 5.4 F1 `HERO_DATA` — 5レイアウトの数値仕様

**共通タイムライン（コンプローカル秒。`dur` はスロット表の区間長）**

| t | 出来事 |
|---|---|
| 0.000 | 黒dip 100% → `head=0.1333s` で 0%（ease 40） |
| 0.000 → dur | 静止画 push-in（§5.3） |
| 0.150 | 上ラベル `revealUp`：position y+46 → y（0.5s・ease 80）＋ opacity 0→100（0.4s・ease 70） |
| 0.450 | 大数字 opacity 0 → 100（0.12s）※`numReveal = t_num0 − 0.10` |
| 0.500 → 1.250 | ライトスイープ position `[-300, H/2]` → `[W+300, H/2]`（ease 45）／ opacity 0→18→0 |
| 0.550 → 1.050 | 金アクセントライン scaleX 0 → 100（ease 90・**motionBlur ON**） |
| **0.550 → 1.550** | **数値カウントアップ**（18キー・`ease_out_cubic` / hold補間 / +0.02s で target に着地して保持）＝ `count_keys()` をそのまま使う |
| 0.550 / 0.900 / 1.200 | 数字 scale `42` → `112` → `100`（オーバーシュート・ease 75・**motionBlur ON**） |
| 0.000 / 0.700 / dur | グロー opacity 0 → 22 → 14（ease 60） |
| 1.150 | 下ラベル `revealUp` |
| dur−tail | 黒dip 0% → 100%（ease 40） |

**レイアウト別の差分:**

- **`A_BIG_NUMBER`** — 基準形。大数字 Anton 250 GOLD を `[W/2, H*0.42]`、上ラベル Oswald 44 SILVER tracking 340 を `H*0.205`、アクセント線 GOLD `460×6` を `H*0.485`（opacity 92）、下ラベル Oswald 64 WHITE tracking 120 を `H*0.60`
- **`B_SPLIT_RATIO`** — 大数字を2つ。左 `[W*0.30, H*0.42]`（fontSize 210・GOLD・カウントアップ）／右 `[W*0.70, H*0.42]`（fontSize 210・SILVER・`"0"` 固定）。中央に縦の分割線 solid `6×H*0.30` を `[W/2, H*0.42]`、scaleY 0→100（0.40→0.85s・ease 90）。上ラベルは左右それぞれ `H*0.255` に fontSize 36（文字列は spec の `top` / `top2`）
- **`C_PERCENT_ARC`** — 大数字（suffix `"%"`）の背後にリング。金 solid にマスク楕円 `rx=ry=300`（feather 0）＋ 内側 `rx=ry=270` を `SUBTRACT` でリング化（外径600 / 内径540）、中心 `[W/2, H*0.42]`。そのリングに `ADBE Radial Wipe` を適用し `Transition Completion` を `100 → (100 − target)` へ 0.55→1.55s（ease 75）
- **`D_CITATION_STAMP`** — 年を大数字（`thousands=false`・4桁）。その下 `H*0.545` に fontSize 56 / SILVER / tracking 180 で引用文字列（spec の `bottom`）。1.60s で**スタンプ打刻**: 引用文字列 scale `130 → 100`（1.60→1.78s・ease 85）＋ opacity 0→100（1.60→1.70s）＋ 同時に金アクセント線を scaleX `100→104→100`（0.12s）
- **`E_VOTE_TALLY`** — 数字は spec の文字列を**固定表示**（カウントアップしない）。上に票マーカー: 金の丸 solid（マスク楕円 rx=ry=28）を `value` 個、`[W/2 − (n−1)*40 + i*80, H*0.30]` に並べ、i番目を `0.55 + i*0.08` 秒に scale `0 → 118 → 100`（3キー・ease 80・**motionBlur ON**）で着地。反対票は SILVER の丸で右端に続ける

**8スロット:**

| slot | 配置(幕) | 数値カテゴリ | layout | 区間長 | 必須 |
|---|---|---|---|---|---|
| `HB1_INTERROGATION_LENGTH` | 幕2前半 | 取調べの継続時間 | `A_BIG_NUMBER` | 6.0s | ✅ |
| `HB2_SUBJECT_VULNERABILITY` | 幕1後半 | 主役の年齢 | `A_BIG_NUMBER` | 5.5s | ✅ |
| `HB3_THE_LIE` | 幕2中盤 | 存在しない証拠の件数 | `B_SPLIT_RATIO` | 6.5s | ✅ |
| `HB4_THE_CASE` | 幕3冒頭 | `394 U.S. 731` / `1969` | `D_CITATION_STAMP` | 6.0s | ✅ |
| `HB5_YEARS_LOST` | 幕3後半 | 失った年数 | `A_BIG_NUMBER` | 6.0s | ✅ |
| `HB6_FALSE_CONFESSION_RATE` | 幕4前半 | 虚偽自白の関与率 | `C_PERCENT_ARC` | 6.5s | ✅ |
| `HB7_DECISION_VOTE` | 幕3中盤 | 判決の票数 | `E_VOTE_TALLY` | 5.5s | ⭕条件付き |
| `HB8_EXONERATION_YEAR` | 幕4後半 | 免罪・釈放の年 | `D_CITATION_STAMP` | 5.5s | ⭕条件付き |

### 5.5 F2–F6 — 新カード族の数値仕様（**この数値どおりに実装する**）

#### F2 `ACT_TITLE`（4枚・dur 3.0s）

| t | 要素 | 数値 |
|---|---|---|
| 0.000 | 黒dip | 100→0（head 0.1333s・ease 40） |
| 0→dur | 背景 still | scale `fill → fill*1.06`（ease 25）／ position `[W/2−14, H/2+8] → [W/2+14, H/2−8]`（ease 20） |
| 0→0.4 | グレード | MULTIPLY opacity 46（固定） |
| 0.20→0.80 | 金の水平線 | GOLD solid `900×4` at `[W/2, H*0.455]`、scaleX 0→100（ease 90・**motionBlur ON**） |
| 0.25 / 0.55 / 0.80 | 幕番号 | Anton 120 GOLD at `[W/2, H*0.335]`、scale `60 → 108 → 100`（ease 75・**motionBlur ON**）。opacity 0→100（0.25→0.40） |
| 0.55 | 幕タイトル | Oswald 84 WHITE tracking 60 at `[W/2, H*0.585]`、`revealUp`（y+52→y・0.5s・ease 80 ＋ opacity 0→100・0.4s・ease 70） |
| 0.85 | サブ | Oswald 40 SILVER tracking 220 at `[W/2, H*0.685]`、`revealUp` |
| 0.45→1.15 | ライトスイープ | 白 solid `300 × H*1.6`、`ADBE Rotate Z`=18、ADD、`[-260,H/2] → [W+260,H/2]`（ease 45）、opacity 0→16→0 |
| dur−tail | 黒dip | 0→100（ease 40） |

#### F3 `EXHIBIT_DOC`（3枚・dur 5.0s）

| t | 要素 | 数値 |
|---|---|---|
| 0→dur | 書類 still | scale `fill*0.72 → fill*0.76`（ease 25）、`ADBE Rotate Z` = **−3.5**、position `[W*0.42, H*0.52]` |
| — | 影 | 黒 solid `W*0.55 × H*0.72` at `[W*0.42+10, H*0.52+14]`、opacity 55（書類の下のレイヤー） |
| 0→0.4 | グレード | MULTIPLY opacity 52 |
| 0.50→1.60 | スキャンライン | GOLD solid `W*0.62 × 3`、ADD、position y `H*0.16 → H*0.88`（ease 55）、opacity 0→70→0 |
| 1.70 / 1.95 / 2.20 | **墨消しバー ×3** | 黒 solid `W*0.30 × 26` at `[W*0.42, H*0.40 / H*0.50 / H*0.60]`、各 scaleX 0→100 を **0.28s** で（ease 90・**motionBlur ON**）。＝「消された証拠」の可視化 |
| 0.55→1.05 | 金の縦線 | GOLD solid `6 × H*0.22` at `[W*0.665, H*0.42]`、scaleY 0→100（ease 90） |
| 0.60 | 右ラベル | Oswald 44 SILVER tracking 300 at `[W*0.78, H*0.34]`、`revealUp` |
| 0.95 | 右本文 | Oswald 60 WHITE tracking 40 at `[W*0.78, H*0.44]`、`revealUp`（**≤22文字**） |
| 2.40→2.55 | 出典スタンプ | Oswald 30 SILVER tracking 160 at `[W*0.78, H*0.56]`、opacity 0→100 |
| — | 字幕ロワーサード | §5.3 共通 |

#### F4 `TIMELINE_TRACK`（2枚・dur 7.0s・ノード数 N = 3〜6）

| t | 要素 | 数値 |
|---|---|---|
| 0→dur | 背景 still | scale `fill → fill*1.05`（ease 25） |
| 0.30→1.30 | 軌道線 | GOLD solid `(W*0.76) × 4` at `[W/2, H*0.52]`、scaleX 0→100（ease 85・**motionBlur ON**） |
| — | ノード座標 | `x_i = W*0.12 + i*(W*0.76/(N−1))`、`y = H*0.52` |
| `1.10 + i*0.45` | ノード | GOLD 丸 solid（マスク楕円 rx=ry=17・feather 0）、scale `0 → 126 → 100`（3キー: t / t+0.16 / t+0.30・ease 80・**motionBlur ON**） |
| ノード着地 +0.05 | 年ラベル | Anton 56 WHITE at `[x_i, H*0.435]`、position y+22→y（0.28s・ease 80）＋ opacity 0→100 |
| ノード着地 +0.10 | イベントラベル | Oswald 34 SILVER tracking 80 at `[x_i, H*0.615]`、同上（**≤16文字・1行**） |
| 0.30 → `1.10+(N−1)*0.45` | 進行ヘッド | GOLD solid `8 × 56`、ADD、position x を `W*0.12 → x_(N−1)` へ（ease 45） |
| 0.15 | 上ラベル | Oswald 44 SILVER tracking 340 at `[W/2, H*0.205]`、`revealUp` |
| — | 字幕ロワーサード | §5.3 共通 |

#### F5 `MAP_DIAGRAM`（2枚・dur 6.5s・ノード数 N = 2〜4）

| t | 要素 | 数値 |
|---|---|---|
| 0→dur | 背景 still（地図/空撮/建物） | scale `fill → fill*1.05`（ease 25） |
| 0→0.40 | 暗幕 | 黒 solid 全面、opacity 0→58（ease 60）＝図解を読ませるため |
| `0.55 + i*0.35` | ノード（金リング） | GOLD solid にマスク楕円 `rx=ry=44` ＋ 内側 `rx=ry=34` を `SUBTRACT` でリング化。座標は spec の `nodes[i].pos = [W*px, H*py]`。scale `0 → 118 → 100`（3キー: t / t+0.18 / t+0.32・ease 80・**motionBlur ON**） |
| 後ノード着地 −0.05 → +0.37 | コネクタ | GOLD solid `L × 4`（`L` = 2点間距離。**Pythonで事前計算**）、`ADBE Anchor Point` を左端に、`ADBE Rotate Z` = `atan2(dy,dx)` の度（**Pythonで事前計算**）、scaleX 0→100（ease 85・**motionBlur ON**） |
| ノード着地 +0.08 | ノードラベル | Oswald 36 WHITE tracking 60 at `ノード座標 + [0, −70]`、opacity 0→100 |
| 0.15 | 上ラベル | Oswald 44 SILVER tracking 340 at `[W/2, H*0.205]`、`revealUp` |
| 1.60 | 下ラベル | Oswald 60 WHITE tracking 120 at `[W/2, H*0.82]`（**heroの H*0.60 ではない**。ノードと干渉するため）、`revealUp` |
| — | 字幕ロワーサード | §5.3 共通 |

#### F6 `INTERSTITIAL_WIPE`（4枚・dur 1.2s・**still 不要**）

| t | 要素 | 数値 |
|---|---|---|
| 0.000 | 黒dip | 100→0（head `2/30 = 0.0667s`・ease 40） |
| — | ベース | 黒 solid `W×H` |
| 0.05→0.95 | 金ワイプ | GOLD solid `W*1.3 × H*1.6`、`ADBE Rotate Z`=18、position `[-W*0.9, H/2] → [W*1.9, H/2]`（ease 60）、opacity 100 |
| 0.15→1.05 | 紺ワイプ（追走） | NAVY solid 同サイズ・同経路を **0.10s 遅らせる**（二重ワイプ）、opacity 100 |
| 0.35 / 0.55 / 0.85 | 中央マーク | Oswald 38 SILVER tracking 400 at `[W/2, H/2]`、文字列は spec の `top`、opacity 0→100→0 |
| dur−tail | 黒dip | 0→100（tail `2/30`・ease 40） |

### 5.6 spec ファイルと anchor 解決

**入力（台本スレッドが埋める）:** `episodes/PD-2026-039-frazier/04_scenes/ae_cards.spec.v001.json`

```jsonc
{
  "episode_id": "PD-2026-039-frazier",
  "fps": 30,
  "cards": [
    {
      "id": "hb01",                        // ^(hb|at|ex|tl|mp|iw)[0-9]{2}$ 通し・欠番禁止
      "family": "HERO_DATA",               // HERO_DATA|ACT_TITLE|EXHIBIT_DOC|TIMELINE_TRACK|MAP_DIAGRAM|INTERSTITIAL_WIPE
      "slot": "HB1_INTERROGATION_LENGTH",  // HERO_DATA のみ。§5.4 の enum
      "layout": "A_BIG_NUMBER",            // HERO_DATA のみ
      "dur": 6.0,                          // §5.2 の族ごとの区間長
      "anchor_phrase": "for forty-eight hours",  // script.annotated の text 内に逐語で1回だけ存在すること
      "anchor_align": "start",             // start|end
      "still": "S07",                      // 素材台帳の scene_code。INTERSTITIAL_WIPE は null
      "top": "IN THAT ROOM",               // ASCII大文字・<=18文字
      "top2": null,                        // layout=B_SPLIT_RATIO のみ必須・<=18文字
      "bottom": "NO LAWYER PRESENT",        // <=22文字。ACT_TITLE ではサブタイトル
      "value": null,                        // ★未確定は null。null のまま生成しようとしたら FAIL
      "value2": null,
      "decimals": 0, "thousands": false, "prefix": "", "suffix": " HOURS",
      "nodes": null,                        // TIMELINE_TRACK / MAP_DIAGRAM のみ。§5.5 参照
      "claim_id": "C-039-014",              // 必須・null禁止。fact_recheck に存在すること
      "start": null,                        // ★生成時に anchor から解決。手書き禁止（null で出す）
      "end": null
    }
  ]
}
```

**後方互換:** `ae_cards.spec.v001.json` が無く `04_scenes/hero_beats.spec.v001.json` だけがある場合は、後者を `family: "HERO_DATA"` として読む。**両方無ければ FAIL で停止**（推測でカードを置くな）。

**anchor 解決アルゴリズム（`build_frazier_ae_jsx.py` が実装）:**
1. `captions.final.v001.json` の語タイム列を連結し、`anchor_phrase` を正規化（小文字化・句読点除去・連続空白1つ）して逐語検索
2. **ヒット0件 or 2件以上 → そのカードを `unresolved` として出力し FAIL を返す**（推測で置かない）
3. `anchor_align="start"` → `start = 一致語列の先頭語の開始秒 − 0.25`。`"end"` → `start = 一致語列の末尾語の終了秒 − dur + 0.35`
4. `end = start + dur`
5. 字幕1行は `nearest_caption(start,end)` → `one_line(maxchars=50)`。**改行文字を絶対に含めない**

**配置制約（`--validate` で機械検証。違反は FAIL）:**
- 全カード: `start >= 20.0` かつ `end <= 総尺 − 25.0`
- `HERO_DATA` 同士の間隔 **≥ 20.0秒**（数字カードが連続するのを禁止）
- 異なる族の間隔 **≥ 8.0秒**
- **唯一の例外**: `INTERSTITIAL_WIPE` の直後に `ACT_TITLE` を隣接させてよい（間隔0。ワイプが助走になる）
- `ACT_TITLE` の配置: 幕1のカードは **20.0–24.0秒**。幕2/3/4 のカードは各幕開始（**170.0 / 370.0 / 540.0 秒**）の **±1.5秒**以内
- **AE合計尺 ≤ 本編の18%**
- 各カードは `truth_status="verified"` かつ `claim_ids` 非空のナレビート上にのみ載る（`HERO_DATA` / `EXHIBIT_DOC` / `TIMELINE_TRACK` / `MAP_DIAGRAM`。`ACT_TITLE` と `INTERSTITIAL_WIPE` は免除）

**サイドカー出力:** `08_edit/ae_hero/cards.json`（jsx とコンポジタの両方を駆動する単一の真実）。EP38の `beats.json` と同じ役割・同じフィールド（`id/start/end/dur/still/out/…`）＋ `family` を追加。

### 5.7 実行手順（このマシンの実パス）

```bash
# 1) 生成（Python が jsx と派生 json を書く。AEはまだ起動しない）
py -3.11 C:/Users/aab15/Documents/prime-documentary/scripts/ae/build_frazier_ae_jsx.py --validate

# 2) ビルド（AfterFX でコンプ作成 → .aep 保存 → app.quit()）
#    jsx 末尾が render/_build_ok.txt を書く。これをポーリングする。早期killしない。
"/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.com" -noui -r \
  "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-039-frazier/08_edit/ae_hero/frazier_ae.jsx" &

# 3) 書き出し（レンダーキューを丸ごと）
"/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/aerender.exe" \
  -project "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-039-frazier/08_edit/ae_hero/frazier_ae.aep"

# 4) 合成（完成mp4に overlay。音声は copy。別名出力）
py -3.11 C:/Users/aab15/Documents/prime-documentary/scripts/ae/composite_frazier_ae.py \
  "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-039-frazier/08_edit/frazier_final_bgm.v002.mp4" \
  "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-039-frazier/08_edit/frazier_final_bgm.v003_ae.mp4"
```

### 5.8 このマシン固有の罠（**踏むと無言で壊れる。全部実測済み**）

| # | 罠 | 対処（そのまま実装せよ） |
|---|---|---|
| 1 | 環境 | AE **2026**・**日本語ロケール**・RTX4090。実行体は `/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/` の `AfterFX.com`（ビルド用）と `aerender.exe`（書き出し用） |
| 2 | **イーズが無言で効かず等速になる** | `setTemporalEaseAtKey` は Position など **spatial プロパティでは要素1個の配列**。`var dim = prop.isSpatial ? 1 : (prop.value instanceof Array ? prop.value.length : 1);` で次元を決める。間違えるとエラーも出ずリニアになる |
| 3 | **テンプレ名がローカライズ済み** | 有効値は RS `"最良設定"` / OM `"H.264 - レンダリング設定を一致 - 15 Mbps"`。**英語名は失敗する**。try/catch で英語名にフォールバックしてよいが、日本語名を先に試すこと |
| 4 | **字幕の改行** | AE の `TextDocument` の改行は `\n` **ではない**。**字幕は必ず1行に保つ**（`one_line(maxchars=50)`）。どうしても改行するなら `\r` |
| 5 | **`app.newProject()` は headless (`-noui`) でハングする** | 使うな。代わりに既存の同名コンプを防御的に削除する（`for (i=proj.numItems; i>=1; i--) if (item instanceof CompItem && name.indexOf("FRZ_")===0) item.remove();`） |
| 6 | **ビルドは遅い / レンダは速い** | ビルド ~100–120秒（今回は21コンプなので**~350–450秒を見込め**）、レンダは 6コンプ ~21秒。**jsx が書く完了マーカー（`render/_build_ok.txt`）をポーリングせよ。早期killするな** |
| 7 | 起動方式 | AfterFX / aerender は**デタッチ起動＋出力ファイルのポーリング**。jsx の末尾で必ず `app.quit()`。強制終了後のクラッシュ修復ダイアログが次回起動を全ブロックする |
| 8 | **モーションブラー** | `layer.motionBlur = true` を**レイヤー個別に**設定する。コンプの `comp.motionBlur = true` だけでは無効。数字・アクセント線・票マーカー・ノード・墨消しバー・コネクタに必須 |
| 9 | **2Dレイヤーの回転** | `"ADBE Rotation"` は **null** を返す。`"ADBE Rotate Z"` を使え（ライトスイープ18° / F3の−3.5° / F5のコネクタ / F6のワイプ18°） |
| 10 | **レイヤーの outPoint** | `inPoint` だけ設定すると `outPoint` がコンプ末尾に残る。**両方設定せよ** |
| 11 | **画像シーケンスのfps** | AE は画像シーケンスを prefs 既定の 30fps で読む。`item.mainSource.conformFrameRate = FPS` が無いと**全カードの timing が無言でズレる**。単一 PNG でも明示せよ |
| 12 | GPU不安定 | `proj.gpuAccelType = GpuAccelType.SOFTWARE;` / `proj.bitsPerChannel = 8;` を try/catch で設定 |
| 13 | 残留プロセス | aerender 前に `taskkill //F //IM AfterFX.com` `//IM AfterFX.exe` で残骸を落とす |
| 14 | 数値整形 | **JS側で数値を整形しない。** カウントアップの全キー文字列・コネクタの角度と長さ・ノード座標を Python 側で事前計算して jsx に埋め込む |
| 15 | 上書き | **出荷済みファイルを絶対に上書きしない。** 出力は必ず `*_v003_ae.mp4` の新規版名 |

### 5.9 コンポジタの要件（`composite_frazier_ae.py`）

`scripts/ae/composite_kfc_hero.py` の構造をそのまま踏襲。**必ず維持する挙動:**
- `cards.json` を読み、各カードの `render/<id>.mp4` を検査
- **SKIP 条件**（その区間は元のカットのまま＝作品が壊れない）:
  - mp4 が存在しない
  - `probe_wh(mp4) != "1920x1080"`
  - `probe_dur(mp4) < card.dur - 0.3`
  - `card.end > base_dur`
- filter_complex: `[N:v]setpts=PTS-STARTPTS+<start>/TB,format=yuv420p[bK]` → `[prev][bK]overlay=0:0:eof_action=pass:enable='between(t,<start>,<end>)'[vK]`
- 出力: `-c:v libx264 -preset medium -crf 16 -pix_fmt yuv420p -c:a copy`（**音声は必ず copy**）
- 出力尺が base と 0.5秒以上ずれたら WARN を出す
- SKIP したカードの id と理由を stderr に列挙する
- ffmpeg/ffprobe の実パス: `C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe` / `ffprobe.exe`

**受入:** **SKIP 0本**。1本でも SKIP されたら原因を潰して再合成する。

---

## 6. 字幕 — **構文境界で切る実装に置き換える**（オーナー指摘・機械ゲート）

### 6.1 いま何が壊れているか

現行 `scripts/gen_captions_case.py` の L16:
```python
MAX_WORDS, MAX_CHARS = 7, 42
```
これは**純粋な語数・文字数カウントで、構文をまったく見ていない**。結果、実測で**現行全話が14〜32%不正**。EP38の出荷済みSRTの実例:

```
24  "...ends with a warning and a ride"
25  "home."                                  <- 孤立キュー・句の切断
27  "A child was handed a form giving up the right"
28  "to a lawyer -"                          <- "the right | to a lawyer" で切断
33  "...taught to trust the adults"
34  "in the room, signed away..."            <- "the adults | in the room" で切断
```

**文字数は上限であって分割基準ではない。** これを直す。

### 6.2 ゲート

```bash
python scripts/check_caption_breaks.py episodes/PD-2026-039-frazier/08_edit/captions.final.v001.srt
```

実装済みの判定（`scripts/check_caption_breaks.py` を**読んで確認せよ**）。3クラスを測る:
- **A. dangling line** — 複数行キューの行末が機能語で終わり、句読点が無い
- **B. orphan cue** — `MIN_CUE_WORDS = 3` 未満で、かつ「大文字始まり＋終止符号終わりの完全文」でないキュー
- **C. boundary split** — キュー末に句読点が無く、次のキューが小文字で始まる。末尾語が機能語なら `hard`、そうでなければ `soft`

**PASS 条件:** `dangling_lines == 0` かつ `orphan_cues == 0` かつ `boundary_splits_hard == 0` かつ `bad_share <= 0.05`。
機能語リストは `scripts/fix_caption_dangling.py` の `NO_DANGLE_END` を **import して使う**（**再定義するな**。定義が二重化すると必ずドリフトする）。

### 6.3 新実装 `scripts/gen_captions_syntax.py`（新規）

**`gen_captions_case.py` を書き換えるな**（他の全エピソードが使っている）。新規に作り、EP39 はこちらを使う。

**踏襲する部分**（`gen_captions_case.py` から流用）:
- `faster-whisper small.en`（cpu/int8）で語タイムを取り、`08_edit/_whisper_words.v001.json` にキャッシュ（**2回目以降は再転写しない**）
- `06_audio/narration_index.v001.json` の chunk 単位で台本語と語タイムをアラインする既存ロジック
- SRT 書式・タイムスタンプ整形・キュー重なり解消

**置き換える部分＝分割ロジック（`split_lines()` を捨てて下を実装する）:**

**分割候補の優先順位（高い順に切る。文字数は上限としてのみ効く）:**

| P | 境界 | 条件 |
|---|---|---|
| **P1** | 文末 | 語末が `. ? !` |
| **P2** | 節境界 | 語末が `; :` または `—` / 直前がカンマ かつ 残り語数 ≥3 |
| **P3** | 従属節の前 | 次の語が `because although while when if since after before until unless whereas though so that who which whose` のいずれか（＝**その語の前**で切る） |
| **P4** | 等位接続の前 | 次の語が `and but or nor yet` かつ、その後ろ2語以内に動詞候補がある（＝節の等位） |
| **P5** | 前置詞句の前 | 次の語が `in on at to for with from into over under during without through against between` かつ、そのPPの長さが **3語以上** |
| **P6** | 不定詞の前 | 次の語が `to` かつ その次が動詞原形 |

**絶対に切ってはいけない位置（P1–P6 より強い禁止則）:**
- 限定詞・所有格とその名詞の間（`the | room` / `his | statement`）
- 前置詞とその目的語の間（`to | a lawyer` / `in | the room`）
- 助動詞と本動詞の間（`had | confessed` / `was | told`）
- 否定辞と動詞の間（`did not | say`）
- 数詞とその単位の間（`forty-eight | hours`）
- **`NO_DANGLE_END` に含まれる語の直後**（終止符号が続く場合を除く）

**分割後のハード制約（超えたら再分割 or 併合）:**

| 項目 | 値 |
|---|---|
| 1キュー最大語数 | **14** |
| 1行最大文字数 | **42** |
| 1キュー最大行数 | **2**（→ 1キュー最大84文字） |
| 1キュー最小語数 | **3**（完全文なら1語でも可） |
| キュー長 | **1.0s ≤ x ≤ 6.0s** |
| 読速 | **≤17 cps** |
| キュー間ギャップ | **≥2フレーム = 0.0667s @30fps** |
| 音と字幕のズレ | **≤120ms** |

**併合パス（分割後に必ず走らせる）:**
- 3語未満のキューは隣に併合する。**どちら側に付けるかは構文で決める**: そのキューが小文字始まりなら**前**に付ける（前の文の続き）／前のキューが終止符号で終わっているなら**次**に付ける
- 併合の結果 14語 or 84文字を超えるなら、P1→P6 の順で最も高い優先度の内部境界で再分割する

**行内の折り返し:**
- 42文字を超えるキューは**キュー内の最高優先度の構文境界**で2行に割る。**中央付近で機械的に割るな**（現行 `wrap2()` の `half` 方式は禁止）
- どちらの行も `NO_DANGLE_END` の語で終わってはならない

**自己検証（生成の最後に必ず実行してから終了する）:**
```python
# gen_captions_syntax.py の末尾で
rc = subprocess.run([sys.executable, "scripts/check_caption_breaks.py", str(OUT)]).returncode
if rc != 0:
    raise SystemExit("caption breaks gate FAILED — do not ship this SRT")
```

### 6.4 字幕の見た目（v2 row3/4・VIDEO_RULES §13）

- forced alignment で**語単位**に整列。音と字幕のズレ ≤120ms
- 文字サイズ 48–60px、白＋濃い縁取り、背後に半透明黒帯（不透明度 55–70%）、画面下部の安全帯、中央寄せ
- **ゾーン分離厳守**: 下＝字幕／上・中央＝テロップ（`on_screen_text`）／出典テロップ（金ライン）は字幕と縦に離す。**一度も重ねない**
- 出力3形式: `04_scenes/captions.final.v001.{srt,json,ass}` ＋ `08_edit/captions.final.v001.srt`
- **字幕は台本からのコピペ禁止。発話音声に整列させる**（`caption_narration_match >= 99%`）

### 6.5 スタブでの検証（台本を待たずに今できる）

スタブのナレ音声（TTSではなく**無音＋既知の語タイム JSON を手で書いたもの**）で `gen_captions_syntax.py` の分割ロジックだけを単体テストする。**ElevenLabs を叩くな。**

`scripts/tests/test_caption_syntax.py` を書き、少なくとも下の6ケースが**切られないこと**を assert する:

| # | 入力断片 | 期待 |
|---|---|---|
| 1 | `...a warning and a ride home.` | `ride \| home.` に割らない |
| 2 | `giving up the right to a lawyer` | `the right \| to a lawyer` に割らない |
| 3 | `trust the adults in the room` | `the adults \| in the room` に割らない |
| 4 | `he was held for forty-eight hours` | `forty-eight \| hours` に割らない |
| 5 | `the officer did not tell him` | `did not \| tell` に割らない |
| 6 | 任意の1〜2語キューが生成されないこと | orphan 0件 |

```bash
py -3.11 scripts/tests/test_caption_syntax.py
python scripts/check_caption_breaks.py <生成したスタブSRT>   # exit 0
```

---

## 7. 台本スロット契約（**未確定は `null` で受けてゲートで止める**）

### 7.1 台本の語数（実測にもとづく確定値）

- ナレーション速度の**実測中央値 178.1 wpm**（2026-07-19・31話の実TTS音声から測定。範囲 163.7–237.4）
- **目標 2,140語 / 許容 2,048–2,226語**
- 判定は **`python scripts/check_script_length.py <script>` のみ**。自己申告・体感は禁止

```bash
python scripts/check_script_length.py episodes/PD-2026-039-frazier/03_script/script.en.v001.md
```

根拠（`scripts/check_script_length.py` の docstring より・読んで確認済み）:
```
690s (11.5 min) @ 178.1 wpm = 2,048 words
750s (12.5 min) @ 178.1 wpm = 2,226 words
```
過去38話中30話が宣言した目標尺に未達。EP38 は 1,675語で **9.40分**（ゲートの予測9.4分と実測が一致）。**1,700–1,860語帯で書くと必ず10分台前半で終わる。**

**水増し禁止:** 言い換え反復・冗長な接続・無意味な間で語数を稼ぐのは `scripts/check_padding.py` で FAIL する。

### 7.2 台本の品質水準

オーナー指定「**パルムドール級・AI臭なし**」。台本は別スレッドで制作中。
**あなたは値の中身を書かない。** スロット（契約）だけを定義し、**未確定は `null` で受けてゲートで止める**設計にする。

### 7.3 待ち受けるファイル

| # | ファイル | 生成者 | あなたの依存 |
|---|---|---|---|
| S1 | `03_script/EP39_FILM_BIBLE.v001.md` | 台本プロセス | 参照のみ |
| S2 | `03_script/script.en.v001.md` | 台本プロセス | **必須** |
| S3 | `03_script/script.annotated.v001.json` | 台本プロセス | **必須**（TTS・字幕・shotlist の入力） |
| S4 | `03_script/fact_recheck.v001.json` | 台本プロセス | **必須**（カード数値の出典） |
| S5 | `04_scenes/ae_cards.spec.v001.json` | 台本＋研究 | **必須**（AEカードの数値・anchor） |

`script.annotated.v001.json` の契約（あなたが検証する側）:

```jsonc
{
  "episode_id": "PD-2026-039-frazier",   // 固定。一致しなければFAIL
  "slug": "frazier",
  "target_duration_minutes": 11.75,
  "duration_profile": "standard",
  "wpm_assumed": 178.1,                   // 実測中央値(31話)。推定値に戻すな
  "total_words": 2140,                    // 2048 <= x <= 2226 でなければFAIL
  "sections": [{
    "role": "hook",                       // enum: hook|opening|body|ending（4つ全部が1回以上・この順）
    "act": null,                          // body のとき 1|2|3|4、それ以外 null
    "beats": [{
      "beat_id": "B001",                  // ^B[0-9]{3}$ 通し・欠番禁止
      "text": "...",                      // ナレ逐語。TTSに渡る唯一の真実。生成後は一字も変えない
      "words": 23,                        // text の語数（半角空白split）。不一致ならFAIL
      "est_sec": 7.75,                    // words / 178.1 * 60。±0.05 以内
      "visual_question": "...",
      "visual_verb": "...",               // reveal|close|approach|tick|split|collapse|rise|hold
      "start_state": "...", "end_state": "...", "eye_target": "...",
      "sync_words": ["lied", "confessed"],
      "source_type": "ai_still|factory_clip|mg_card|ae_card|blender",
      "truth_status": "verified|attributed|characterization",
      "claim_ids": ["C-039-014"],         // verified の beat は 1個以上必須
      "on_screen_text": null
    }]
  }]
}
```

**あなたが実行する検証:**
- `role` が hook→opening→body→ending の順に少なくとも1回ずつ出現
- hook セクションの `est_sec` 合計 = **6.0–10.0秒**
- hook で teased した reveal が body/ending に必ず出現（promise-payoff）
- 全 beat の `est_sec` 合計が **690–750秒**
- `truth_status = "verified"` の beat は `claim_ids` 非空

### 7.4 未確定時の挙動（**B-8 の検証対象**）

**必ずこう振る舞うこと:**
- `ae_cards.spec` の `value` が `null` のカードをビルドしようとしたら → **例外を投げて停止**。`0` や推測値で埋めるな
- `anchor_phrase` が語タイム列に **0件 or 2件以上**ヒットしたら → そのカードを `unresolved` として報告し **FAIL を返して停止**。推測で配置するな
- `claim_id` が `fact_recheck.v001.json` に存在しなければ → **FAIL**
- S2–S5 のいずれかが存在しなければ → **その旨を明示して停止**（「台本待ち」と報告する。ダミー台本を書いて進めるな）

**実測で確認せよ:** `value: null` のスペックを1件作ってビルドを走らせ、**実際に非0で停止すること**を出力付きで示す。

### 7.5 台本確定後の実行順（この順に自動で進む）

1. `script.annotated.v001.json` の `text` を連結 → **ElevenLabs**（`VOICE_ID=nPczCjzI2devNBz1zQrb`, `eleven_multilingual_v2`, stability 0.35 / similarity_boost 0.80 / style 0 / speaker_boost on）でナレ生成。**SAPI/ローカルは出荷禁止**
2. レンダ済みナレ音声に **forced alignment** → `gen_captions_syntax.py`（§6）で `captions.final.v001.{srt,json,ass}`
3. 語タイムから各 `beat_id` の実 `start`/`end` を確定 → `04_scenes/shotlist.v001.json`
4. `build_frazier_film.py`（§4.3）→ `remotion/src/data/frazier_film.json` → `check_asset_reuse.py`
5. `CaseFilm` レンダ → 4層ミックス → `08_edit/frazier_final_bgm.v002.mp4`
6. `build_frazier_ae_jsx.py --validate` → AEビルド → aerender → `composite_frazier_ae.py` → `v003_ae.mp4`
7. **フック（0–8秒）を本編素材から最後に組む**（新規素材を作らない）
8. 全ゲート → `--emit-receipt`

**音（4層・v2 row1）:** ナレ＝常に最前面・明瞭。BGM＝章ごとに1トラック、**ナレ下でも −22 LUFS を下回らない**（無音に落とさない）、無音区間25秒超は FAIL。SFX＝カット/リビール/数値出現に短いヒット（heroカードのカウントアップ開始 0.55s に tick、着地 1.55s に impact を同期）。環境音＝取調室（空調のハム・蛍光灯）／夜の街／法廷のざわめき、薄く。総合ラウドネス **−16 … −12 LUFS**。

---

## 8. サムネイル3案

共通仕様（v2 row11/12・全案必須）:
- **1280×720** の Remotion `<Still>` として3案すべてレンダ。`09_package/thumbnail.v001-0{1,2,3}.png` ＋ `thumbnail.selected.v001.png`
- 見出しは **UPPERCASE・4語以内**・自動改行。感情/好奇心のアイデアは**1つだけ**
- **被写体は巨大**（顔/手/物体が画面高の60%以上）。超高コントラスト。**320pxに縮小しても読める**こと（**実際に縮小して確認する**）
- 背景 = 黒 or 濃紺 `#0B1A2B`。アクセント = 金 `#E5B53A` **または** エレクトリックブルー `#1F6BFF`。文字 = 白 `#F5F7FA` / シルバー `#C8CDD6`。**実在人物の肖像は不可**
- `thumbnail_visibility` ゲート（選択サムネの輝度平均 ≥33 ＋ コントラスト下限）を通ること

| 案 | 視覚要素（具体） | テキスト（4語以内） | 色/コントラスト方針 |
|---|---|---|---|
| **T1「嘘のファイル」** | 取調室の机の上、**画面いっぱいの手**が「共犯者の自白調書」らしき紙束を被疑者側へ滑らせる。紙は判読不能。紙の上に**赤い「FAKE」スタンプ**が斜めに強く押されている。奥に椅子のシルエット（顔なし）。上からの蛍光灯1灯で紙だけが白く飛ぶ | **`POLICE CAN LIE`** | 背景ほぼ黒（輝度10%以下）／紙は純白（輝度90%）で**最大コントラスト**／`FAKE` スタンプのみ赤系 → 金 `#E5B53A` の見出しで受ける。赤は1要素のみ |
| **T2「言っていない自白」** | **口元のみの超クローズアップ**（目より上は画角外＝肖像回避）。口の前に浮かぶ吹き出しの中に手書き風の `"I DID IT"`。口と吹き出しの間に**細い金の線が切断**されている（＝言葉と真実の断絶）。背景は濃紺のグラデ | **`I DIDN'T DO IT`** | 濃紺 `#0B1A2B` × 肌のハイライトを強く飛ばす／吹き出しは白／断裂線のみ金／見出しは白＋黒縁。**顔は下1/3のみ＝肖像に該当しない構図** |
| **T3「時計と扉」** | 画面左に**巨大な壁時計**（針が異常に多く重なり長時間経過を示す）、右に**閉じた鉄の取調室ドア**。中央に細い光の帯。人物は**ドアの磨りガラス越しの小さなシルエット1つのみ** | **`48 HOURS ALONE`**（※時間数は台帳確定後に差し替え。**未確定なら `NO ONE COMING`**） | 黒背景／時計盤だけエレクトリックブルー `#1F6BFF` で発光／ドアはシルバー質感／見出しは白。青と白の2色に絞って320pxでの識別性を最大化 |

**A/Bの回し方（v2 row13）:** T1 と T2 を**タイトル × サムネの2組**として先に出す。タイトル案（≤60文字）:
- A: `Police Are Allowed to Lie to You in the Interrogation Room`（58字）
- B: `He Confessed to a Crime He Didn't Commit. It Was Legal.`（54字）

---

## 9. ゲートとドライラン

### 9.1 アニメーション密度（**着手前に閾値を把握せよ。後から直すと作り直し**）

`scripts/check_motion_density.py`（実測ハードフロア・AND条件）:
- `MIN_KINETIC_BEATS_PER_MIN = 2.5` — (graphics + figures + heroCuts) / 本編分。**11.75分なら最低30本**
- `MIN_ANIMATED_COVERAGE = 0.25` — ビート窓の和集合 / 本編秒。**最低176秒ぶん**
- `MIN_ANIMATED_VARIETY = 3` — 異なるアニメ形式の種類数（**同じMGの反復は不可**）

`scripts/check_animation_mix.py`:
- `MAX_STILL_SHARE = 0.45` / `MIN_MOTION_COVERAGE = 0.45`
- `LONG_HOLD_SECONDS = 5.0` / `MAX_LONG_STILL_HOLDS = 8`（5秒超の静止保持は最大8回）
- `MAX_OPENING_SECONDS = 12.0`

**EP39 の設計目標（余裕を持たせた値）:** キネティックビート **38本以上**（3.2/分）／ アニメカバレッジ **0.32以上**／ **バラエティ 10種以上**／ 静止シェア **0.30以下**／ 5秒超の静止保持 **4回以下**。

**バラエティ10種の内訳（AEの6族が効く）:**
`HERO_DATA` / `ACT_TITLE` / `EXHIBIT_DOC` / `TIMELINE_TRACK` / `MAP_DIAGRAM` / `INTERSTITIAL_WIPE` / Remotionキネティックタイポ / Remotion図解 / i2vモーションショット / factory実写フッテージ

**factory 90本は実写＝動いている**ので `motion_coverage` に直接効く。静止画を増やすより有利。

### 9.2 スタブでの通しドライラン（**Aを待たずに今やる**）

```bash
# 0) スタブ素材＋スタブ台帳を作る
py -3.11 scripts/make_frazier_stub_assets.py

# 1) film.json を作る
py -3.11 scripts/build_frazier_film.py \
  --manifest episodes/PD-2026-039-frazier/05_visuals/asset_manifest.stub.v001.json \
  --annotated episodes/PD-2026-039-frazier/03_script/script.annotated.stub.json \
  --captions  episodes/PD-2026-039-frazier/08_edit/captions.final.stub.json \
  --out       remotion/src/data/frazier_film.json

# 2) 反復禁止ゲート
python scripts/check_asset_reuse.py remotion/src/data/frazier_film.json

# 3) 密度ゲート
py -3.11 scripts/check_motion_density.py --ep PD-2026-039-frazier
py -3.11 scripts/check_animation_mix.py  --ep PD-2026-039-frazier

# 4) 短尺プレビューをレンダして目で見る（全編は不要。フレーム範囲で）
cd remotion && npx remotion render CaseFilm out/frazier_dryrun.mp4 --frames=0-1800
```

**ドライランの目的は「動くこと」ではなく「ゲートが緑になること」。** 4) の目視は補助。

### 9.3 その他の受入ゲート（全て既存スクリプト）

```bash
py -3.11 scripts/check_caption_integrity.py --ep PD-2026-039-frazier
py -3.11 scripts/check_visual_asset_qc.py   --ep PD-2026-039-frazier
python  scripts/check_script_length.py episodes/PD-2026-039-frazier/03_script/script.en.v001.md
python  scripts/check_caption_breaks.py episodes/PD-2026-039-frazier/08_edit/captions.final.v001.srt
python  scripts/check_asset_reuse.py   remotion/src/data/frazier_film.json
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 39 --json
```

**最終ゲート（これが緑になるまで "done" と言わない）:**
```bash
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 39 \
  --render episodes/PD-2026-039-frazier/08_edit/frazier_final_bgm.v003_ae.mp4 --emit-receipt
```
→ `09_package/acceptance_receipt.v001.json`（`video_sha256` 付き）。**AE合成後のファイルに対して receipt を発行する**（合成前の v002 に対する receipt は無効）。

### 9.4 受入チェックリスト（全部緑で package_ready）

- [ ] `structure_4part`：hook / opening / body / ending が順に存在。hook = 6–10秒
- [ ] `hook_added` ＋ promise-payoff
- [ ] `runtime_band`：11.5–12.5分
- [ ] `script_length`：2,048–2,226語
- [ ] `voice_is_master`：narration provider に `eleven` を含む。sapi/local を含まない
- [ ] `caption_narration_match >= 99%` / `captions_final` が runtime の ≥95% をカバー
- [ ] **`caption_breaks`：dangling 0 / orphan 0 / hard split 0**
- [ ] `bgm_present`：無音25秒超なし・VO下でも −22 LUFS を下回らない。総合 −16…−12 LUFS
- [ ] `image_resolution`：全使用静止画の長辺 ≥3840
- [ ] **`asset_reuse`：factory ≤1回 / motion ≤2回 / still ≤2回 / first-use share ≥0.70**
- [ ] `footage_diversity`：distinct/total ≥0.40
- [ ] `motion_density`：≥2.5 beats/min ＋ coverage ≥0.25 ＋ variety ≥3（設計目標 3.2 / 0.32 / 10）
- [ ] `animation_mix`：still share ≤0.45 ／ motion coverage ≥0.45 ／ 5秒超保持 ≤8 ／ opening ≤12秒
- [ ] `op_ed_bookends`：`BrandOpening`/`BrandEndcard` を import（フォークしていない）
- [ ] `thumbnail_present` / `thumbnail_visibility`：selected の輝度平均 ≥33
- [ ] タイトル ≤60字・A/B 2案
- [ ] **AEカード：6族すべてが SKIP されずに合成された**
- [ ] **合成後の `v003_ae.mp4` に対して** `check_final_acceptance.py 39 --emit-receipt` が exit 0
- [ ] R2安全：AI肖像0件・グラフィック表現0件・読める偽書類0件

---

## 10. 禁止事項

- **YouTube へのアップロード・公開予約をしない**（オーナー専管）。完成物とパッケージを用意して停止する
- **有料ジョブをドライラン中に起動しない**（ElevenLabs は台本確定後の §7.5-1 だけ）
- **出荷済み mp4 を上書きしない**（出力は必ず `*_v003_ae.mp4`）
- **`05_visuals/asset_manifest.v001.json` に書き込まない**（スレッドAの持ち物。読むだけ）
- **`remotion/public/frazier/{img,factory,motion,overlay}/` に本番素材を置かない**（スタブのみ。本番はAが置く）
- **既存の共有スクリプトを書き換えない**: `scripts/gen_captions_case.py` / `scripts/build_case_film_assets.py` / `scripts/ae/build_kfc_hero_jsx.py` / `scripts/ae/composite_kfc_hero.py`。**新規ファイルを作れ**
- **`components/Bookends.tsx` をフォークしない**（`op_ed_bookends` ゲート）
- **`remotion/src/compositions/Opening.tsx`（id=`Opening`）を書き換えない**
- **`remotion/remotion.config.ts` を変更しない**
- **`check_caption_breaks.py` の機能語リストを再定義しない**（`fix_caption_dangling.NO_DANGLE_END` を import）
- **実在しないスクリプト名・テンプレ名・matchName・エフェクト名を使わない。** 使う前に必ずファイルを読んで実在を確認する
- **自作の品質ゲートを書いて「合格」と宣言しない。** 既存 `check_*.py` の測定結果のみが合否
- **スタブと本番でコードパスを分岐させない。** `if stub:` を1行も書くな
- **曖昧だと感じた箇所を「推測して進める」な。** その場で停止して報告する

---

## 11. 完了報告に必ず含めること

1. 作成／変更したファイルの**絶対パス**一覧
2. `cd remotion && npm run typecheck` の実出力（exit 0）
3. `Frazier39Opening` 3案の**ffprobe 実出力**（1920x1080 / 60fps / 3.00s）
4. サムネ3案のパスと、**実際に320pxへ縮小して見出しが読めたか**の判定
5. **AEスモークテストの ffprobe 実出力（6カード族すべて）** — 1920x1080 / 30fps / spec尺
6. スタブ通しドライランの結果:
   - `check_asset_reuse.py` の標準出力（distinct / cuts / first-use share）
   - `check_motion_density.py` / `check_animation_mix.py` の標準出力
7. `scripts/tests/test_caption_syntax.py` の実出力（6ケース全PASS）＋ スタブSRTに対する `check_caption_breaks.py` の標準出力
8. **`value: null` のスペックでビルドが実際に停止したことの出力**（B-8）
9. `CaseFilm.tsx` に `overlay` を追加した差分と、**既存エピソードの出力が変わらないことの確認方法と結果**
10. 台本待ち・素材待ちで着手できなかった項目の一覧（何を待っているかを明示）
</content>
