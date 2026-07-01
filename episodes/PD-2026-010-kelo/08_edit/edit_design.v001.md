# 第10話 kelo 仕上げ設計書（Edit / Finish Design） v001

対象: `PD-2026-010-kelo`（Kelo v. New London / 収用権）。Codex がこの設計に従ってラフカット→仕上げを行う。
入力: `04_scenes/shotlist.v001.json`（28ショット・628秒≒10.5分）, `03_script/script.en.v001.md`（`[VO:]`=ナレ本文・**変更禁止**）, `04_scenes/asset_map.v001.md`, AI画像 `H:\pd-media\assets\ai\kelo\SPN-XXXX*.png`（生成済み）, サムネ `H:\pd-media\assets\ai\thumbs\kelo\THUMB-01..06.png`（生成済み前提）。
準拠: `episodes/_planning/VIDEO_RULES.md` §10〜13 / `docs/motion-design-language.md` / `docs/motion-quality-gate.md`。

---

## 1. 完成尺と4部構成（VIDEO_RULES §10 厳守）

| 部 | 構成 | ソース | 目安 |
|---|---|---|---|
| **① フック** | 本編の“盛り上がり”約10カット（各1〜2秒）の高速ハイライト集＋煽り音 | 本編映像/ナレ断片の流用（新規制作しない） | 約20〜30秒 |
| **② オープニング** | 既存ブランドオープニング（`remotion/src/compositions/Opening.tsx`） | 既存・作り直さない | 約5〜8秒 |
| **③ 本編** | act1〜act4（SPN-0003〜SPN-0028） | shotlist 各ショット | 約9.5分 |
| **④ エンディング** | 結末＋次回予告＋CTA/フォロー誘導（SPN-0023〜0026） | shotlist ending | 約60秒 |

**フックに使う本編ハイライト候補（priority A 優先・各1〜2秒で速いカット）**:
SPN-0001(孤立する家) / 0006(立ち退きの転機) / 0014(2005・5–4判決グラフィック) / 0016(O'Connor反対意見) / 0020(結局何も建たなかった空き地) / 0021(2009 Pfizer撤退) / 0008(「それは“公共の用”か？」) / 0027(Kennedy補足) / 0028(人的コスト) / 0025(次回への引き)。
→ ナレの決め所断片を1〜2個だけ被せ、最後は無音ぎみ→オープニングへブリッジ。**台本テキストは変えない**。

---

## 2. 全ショット モーション設計（Ken Burns 一辺倒にしない＝VIDEO_RULES §12）

凡例: motion は shotlist の値。**「意味のあるアニメ」列が今回の追加指定**。画像は必ず動かす。

| SPN | 章 | 種別 | テロップ(on_screen_text) | 意味のあるアニメ（指定） |
|---|---|---|---|---|
| 0001 | hook | ai/parallax | Your home — for a private developer? | 孤立した家へ多層パララックスでゆっくり寄る。周囲の更地は奥へ流す |
| 0002 | opening | ai/ken_burns | 5th Amendment: takings only "for public use" | 憲法条文タイポを出し、**"for public use" を下線＋ハイライト**で強調 |
| 0003 | act1 | 実写/native | Fort Trumbull, New London, CT | 地図ロケーター：CT→New London→Fort Trumbull に**ピンが落ちて地名が描かれる** |
| 0004 | act1 | ai/ken_burns | Not blighted. Owner did nothing wrong. | 「小さなピンクの家」へ寄り、**ラベル吹き出し**を添える |
| 0005 | act1 | ai/ken_burns | The plan: offices, hotel, jobs, taxes | **アイコン4種（オフィス/ホテル/雇用/税）が順に組み上がる**ダイアグラム |
| 0006 | act1 | 実写/native | — | 立ち退き＝転機。やや速いカットで緊張を上げる |
| 0007 | act1 | ai/ken_burns | — | 住民の抵抗を象徴。寄り＋微パララックス |
| 0008 | act1 | ai/ken_burns | Is that "public use"? | **疑問符を中央に強調**（中心の問い）。軽いズームパンチ |
| 0009 | act2 | 実写/native | Narrow: the public actually uses it | 定義カード「狭義」を左に提示 |
| 0010 | act2 | ai/ken_burns | Broad: any "public purpose" | 定義カード「広義」を右に。**0009と左右対比**で並置 |
| 0011 | act2 | ai/ken_burns | City: economic development = public use | **「経済開発 ＝ 公共の用」の等式**が組み上がる |
| 0012 | act2 | 実写/native | — | 利害の重み。落ち着いた寄り |
| 0013 | act2 | ai/ken_burns | — | act3への橋渡し。フェード＋微移動 |
| 0014 | act3 | **図解/graphic_anim** | 2005 — 5–4 / Kelo v. New London, 545 U.S. 469 | **年表が2005へ進む→5–4の票が並ぶ→出典 545 U.S. 469 が金ラインで確定**（本話の山場グラフィック） |
| 0015 | act3 | ai/ken_burns | "Public use" = "public purpose" | **2語が重なって等号で結ばれる**モーフ（多数意見） |
| 0016 | act3 | 実写/native | Dissent (O'Connor): "for public use" — erased? | 反対意見。**"for public use" に取り消し線が走る**演出 |
| 0027 | act3 | ai/ken_burns | Kennedy: pretextual takings still barred | **補足の注記カラム**で「口実的収用は依然禁止」を提示 |
| 0017 | act3 | ai/ken_burns | — | act4への転換。寄り引き |
| 0018 | act4 | ai/ken_burns | Backlash: bipartisan | **左右（保守/リベラル）の矢印が中央で合流**（超党派の反発） |
| 0019 | act4 | 実写/native | ~40+ states reformed (many criticized as weak) | **全米地図で州が順に点灯し「40+」へカウントアップ** |
| 0020 | act4 | ai/ken_burns | The development was never built. | 空き地へ**非常にゆっくり押す**。静寂の余韻 |
| 0021 | act4 | **図解/graphic_anim** | 2009: Pfizer leaves New London | **年表が2009へ→皮肉のビート**（撤退を線で示す） |
| 0022 | act4 | ai/ken_burns | The pink house was moved, not destroyed | **家が横へ移動する**モーション（移築） |
| 0028 | act4 | ai/ken_burns | — | 人的コスト。寄りで感情の余白 |
| 0023 | ending | 実写/native | — | 結末の総括。落ち着いた寄り |
| 0024 | ending | ai/ken_burns | — | 論点の統合。ゆっくり引き |
| 0025 | ending | ai/ken_burns | Next: where does free speech end? | **次回予告**。引き＋タイトル示唆のタイポ |
| 0026 | ending | 実写/native | Subscribe | **CTA**：Subscribe ボタン演出＋フォロー誘導（1.6秒） |

> AI画像は1スパンに複数バリアントあり（`SPN-XXXX_02.png`等）。長いスパンは**約4.5秒ごとに別カット/別バリアントへ切替**し、静止・長居を避ける。importer が自動で複数取り込み。

---

## 3. テロップ／字幕／出典のレイアウト（被らせない＝VIDEO_RULES §13）

- **字幕（ナレ全文・forced alignment）**: 画面**下部の帯**。常時ナレと語単位同期。
- **テロップ（キーワード＝on_screen_text）**: **上/中央**。短く・大きく。字幕帯と**重ねない**。
- **出典（金ライン）**: 例 `Kelo v. New London, 545 U.S. 469 (2005)`。**右下など別ポジション**固定。字幕・テロップと別レイヤ・別位置。
- 3者を同じ場所に重ねない（読めない/被るのは不可）。

## 4. 品質ゲート（書き出し前チェック＝motion-quality-gate）
- [ ] フック→オープニング→本編→エンディングの**4部**になっている
- [ ] `coded/cards = 0`（全ショット実素材 or 図解で埋まっている）
- [ ] 全ショットにモーション（静止画ゼロ）／Ken Burns 一辺倒でない
- [ ] 字幕・テロップ・出典が**位置で分離**し被っていない
- [ ] 音4層＋**ダッキング**でナレ最優先（`06_audio/audio_cue_sheet.v001.md`）
- [ ] 中立・実在人物の肖像なし・台本/claims 不改変

## 5. この話の編集ポリシー
- **中立**（公共の用 vs 個人の家、どちらにも肩入れしない）。判決の多数意見・反対意見・Kennedy補足を**公平**に提示。
- **実在人物・判事の肖像なし**（象徴的に）。ディープフェイク不可。

---

## 6. 実装方針＝Premium級コード演出（★重要・汎用RoughCutでは出ない）

§2 の「意味あるアニメ」は**汎用 `RoughCut` では描画されない**（RoughCutは Ken Burns＋動画＋テロップ＋グレイン止まり）。
→ EP10は**bespokeな `remotion/src/compositions/KeloPremium.tsx` を新規作成**し、既存 `CarpenterPremium.tsx` / `RileyPremium.tsx` / `MadoffPremium.tsx` を雛形にする。`RoughCut-kelo` は素材ステージング/下見用に残してよいが、**最終書き出しは `KeloPremium`**。

### 使う既存コード部品（再利用・新規実装を最小化）
- `components/Motion.tsx`: `MovingStage`（カメラ＋粒子＋光）, `Particles`, `LightSweep`, `Vignette`, `CameraRig`。
- `components/Grain.tsx`: `Grain`（フィルムグレイン）。
- `components/Bookends.tsx`: `BrandOpening` / `BrandEndcard`（オープニング/エンドカード）。
- `components/SceneArt.tsx`: `SceneArt`（`visualMode`/`motifHint`/`onScreenText` で **小槌/天秤/年表マーカー/USマップのピン波紋/書類＋印章** を自動選択）。
- `CarpenterPremium.tsx` の流用可能なビズ：`Vote`(5–4票)、`MapGrid`、`TwoColumn`(左右対比)、`Doors`(アイコン列)、`BigNumber`、`CourtColumns`。

### ショット→実装の割り当て（§2の演出をコードに対応）
| SPN | 演出（§2） | 実装（部品） |
|---|---|---|
| 0001 | 孤立した家へパララックス寄り | AI画像＋`MovingStage`（多層パララックス） |
| 0002 | "for public use" 下線強調 | AI画像＋タイポ下線（`Lower`系の手組み） |
| 0003 | Fort Trumbull ロケーター | `SceneArt visualMode="location" motifHint="map pin"`（USマップ＋ピン波紋）or `MapGrid` |
| 0005 | 計画アイコン4種が組み上がる | `Doors`（offices/hotel/jobs/taxes ラベル）順次フェード |
| 0008 | 「それは公共の用か？」疑問符 | AI画像＋大疑問符タイポ＋軽ズーム |
| 0009/0010 | 狭義 vs 広義の左右対比 | `TwoColumn`(left=Narrow / right=Broad) |
| 0011 | 「経済開発＝公共の用」等式 | `TwoColumn` or 手組み等式（= で結ぶ） |
| 0014 | **年表→2005→5–4→出典確定（山場）** | `SceneArt motifHint="timeline"`（年表マーカー）＋`Vote`(5–4)＋`SceneArt motifHint="seal"`（書類＋印章で 545 U.S. 469）。`LightSweep`色=GOLD |
| 0015 | 2語が等号で結ばれるモーフ | 手組みタイポ（"public use"="public purpose"） |
| 0016 | "for public use" に取り消し線 | AI画像/実写＋取り消し線アニメ（手組み・`whoosh_short`同期） |
| 0019 | **USマップで州が点灯し40+へカウント** | `SceneArt motifHint="map"`＋`BigNumber`("40+") カウントアップ |
| 0021 | 年表2009・撤退の皮肉 | `SceneArt motifHint="timeline"`（2009へ） |
| 0022 | 家が横移動（移築） | AI画像＋横トランスフォーム |
| 0026 | CTA Subscribe | 手組みSubscribeボタン＋`soft_impact` |
| その他のai_image | 寄り/引き＋微パララックス | `SceneShell`相当（多画像Ken Burns＋`Particles`/`Vignette`/`Grain`） |
| stock_video | 実写再生 | `<Video>`＋`Vignette`/`Grain` |

### 実装ステップ
1. `KeloPremium.tsx` を作成（`scenes[]` に28スパン＋hook/opening/ending を kind 付きで定義。AI画像は `remotion/public/kelo/SPN-XXXX*.png` を参照）。
2. `Root.tsx` に `KeloPremium`（`id="KeloPremium"`）を登録（ハイフンのみ）。
3. `npm run studio` で `KeloPremium` を確認 → §2の各演出が出ているか／4部構成かをチェック。
4. 書き出しは `KeloPremium`（§7参照）。

> 注：今DL中の共有素材棚（factory: vfx/light/particle/loops）は**このPremium経路では使わない**（コード演出＝`Particles`/`LightSweep` 等で代替。stock素材は将来のギャップ補完・バリエーション用）。
