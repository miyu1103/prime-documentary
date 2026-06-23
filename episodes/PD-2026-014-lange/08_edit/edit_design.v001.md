# 第14話 lange 仕上げ設計書（Edit / Finish Design） v001

対象: `PD-2026-014-lange`（Lange v. California, 2021 / 軽犯罪の追跡と令状なし住居立入・修正第4条）。Codex がこの設計に従ってラフカット→仕上げを行う。
入力: `04_scenes/shotlist.v001.json`（23ショット・約619.6秒≒10.3分・本編実尺）, `03_script/script.en.v001.md`（`[VO:]`=ナレ本文・**変更禁止**）, `04_scenes/asset_map.v001.md`, AI画像 `H:\pd-media\assets\ai\lange\SPN-XXXX*.png`（生成済み前提）, 実写stock `H:\pd-media\episodes\PD-2026-014-lange\stock\*`（DL済み・asset_map参照）, サムネ `H:\pd-media\assets\ai\thumbs\lange\THUMB-01..06.png`（生成済み前提）。
準拠: `episodes/_planning/VIDEO_RULES.md` §10〜13 / `docs/motion-design-language.md` / `docs/motion-quality-gate.md`。
**この話の論点（厳守・中立）**: 争点は「DUIそのもの」ではなく「**軽犯罪の追跡を理由に、令状なしで自宅（ガレージ）へ立ち入れるか**」。California主張＝「逃走すれば自動的に緊急事態（exigency）→立入可」。判決＝自動ルールを否定し**事案ごと（totality of the circumstances）に判断**。逃走は「考慮要素であって自動トリガーではない」。**評決＝判決（差戻し）は全員一致 9–0／ただし“全員一致の意見”ではない**（Roberts＋Alitoは結論同意・より広いルールを主張）。住居プライバシー vs 警察の安全、双方を公平に。

---

## 1. 完成尺と4部構成（VIDEO_RULES §10 厳守）

| 部 | 構成 | ソース | 目安 |
|---|---|---|---|
| **① フック** | 本編の“盛り上がり”約10カット（各1〜2秒）の高速ハイライト集＋煽り音 | 本編映像/ナレ断片の流用（新規制作しない） | 約20〜30秒 |
| **② オープニング** | 既存ブランドオープニング（`BrandOpening`／`remotion/src/compositions/Opening.tsx`相当） | 既存・作り直さない | 約3.5〜8秒 |
| **③ 本編** | act1〜act4（SPN-0003〜SPN-0023の本編スパン） | shotlist 各ショット | 約9.5分 |
| **④ エンディング** | 結末の総括＋シリーズ統合＋次回（フィナーレ）予告＋CTA（SPN-0019〜0021） | shotlist ending | 約75秒 |

> shotlist の `hook`(SPN-0001) と `opening`(SPN-0002) は本編冒頭スパンでもある。**フック=本編ハイライトの再編集**、**オープニング=ブランドオープニング**は別工程として頭に足す（VIDEO_RULES §10）。SPN-0001/0002 はその後の本編としても通常どおり流す。

> **尺の目標＝約12分（11.5〜12.5分）**。台本（ナレ本文）は変えない。本編ナレ＋**フック(約30秒)＋オープニング＋エンディング(約80〜90秒)＋幕間の“ひと呼吸”**（山場SPN-0013＝9–0判決リビール後の余韻、act転換の短い間）で約12分に寄せる。間延びさせず密度で稼ぐ（カット切替は§2基準＝約4.5秒を維持）。

**フックに使う本編ハイライト候補（priority A 優先・各1〜2秒で速いカット）**:
SPN-0001(ガレージの扉が降り、足が差し込まれる＝本話の象徴) / 0005(扉の下の足＝立入の瞬間) / 0013(2021・9–0・出典 594 U.S. 295 グラフィック) / 0014(「事案ごとに判断＝逃走は要素であってトリガーではない」) / 0015(Roberts＋Alito＝結論同意だが広いルール) / 0016(Vacated & remanded＝破棄差戻し) / 0023(コモンローに自動ルールは無い) / 0020(シリーズ統合) / 0021(フィナーレ予告「大胆な約束はいつ犯罪になるか」) / 0006(「争点はDUIではなく“立入”」)。
→ ナレの決め所断片を1〜2個だけ被せ、最後は無音ぎみ→オープニングへブリッジ。**台本テキストは変えない**。

---

## 2. 全ショット モーション設計（Ken Burns 一辺倒にしない＝VIDEO_RULES §12）

凡例: motion は shotlist の値。**「意味のあるアニメ」列が今回の追加指定**。実写は再生、画像は必ず動かす。

| SPN | 章 | 種別 | テロップ(on_screen_text) | 意味のあるアニメ（指定） |
|---|---|---|---|---|
| 0001 | hook | 実写/video_native | Can a cop follow you into your home? | ガレージ扉が降りる実写。**降りる扉に“足”が差し込まれ止まる瞬間**にカット頭を合わせる。低い緊張ドローン |
| 0002 | opening | ai/ken_burns | The home: warrant required (with narrow exceptions) | 自宅＝聖域。寄り＋微パララックス。**"warrant required" を下線＋ハイライト**、"(narrow exceptions)" は小さく添える |
| 0003 | act1 | **図解/graphic_anim** | Sonoma County, CA — loud music & honking | 地図ロケーター：CA→Sonoma County に**ピンが落ちて地名が描かれる**。夜・車のアイコンを薄く |
| 0004 | act1 | ai/ken_burns | ~100 feet from home | 自宅へ近づく構図へゆっくり寄る。**"~100 feet" 距離ラベル**を路上→玄関に向け描画 |
| 0005 | act1 | 実写/video_native | Foot under the door — entry | **扉の下に足が入り扉が止まる→押し上がる**瞬間で再生。立入の決定的ビート。短く速い |
| 0006 | act1 | 実写/video_native | The question: the ENTRY, not the DUI | **"ENTRY" を強調・"the DUI" に薄い取り消し線**で「争点はDUIではない」を視覚化。落ち着いた寄り |
| 0007 | act1 | ai/ken_burns | California: any flight = automatic entry | **「any flight → automatic entry」の等式/矢印**が組み上がる（州の主張）。軽いズームパンチ |
| 0008 | act2 | ai/ken_burns | — | 「なぜ裁判所が悩んだか」への導入。寄り＋微パララックス（テロップ無し・余白） |
| 0009 | act2 | 実写/video_native | Exigent circumstances: danger · evidence · escape | **3アイコン（危険/証拠隠滅/逃走）が順に組み上がる**定義カード。実写の上にオーバーレイ |
| 0010 | act2 | ai/ken_burns | — | hot pursuit が高リスク時に成立する論理。寄り（テロップ無し） |
| 0011 | act2 | ai/ken_burns | Don't let suspects escape — vs — don't gut the home | **左右対比**：左「逃がすな（警察の安全）」右「家を空洞化するな（住居の保護）」。中央で天秤が揺れる |
| 0022 | act2 | 実写/video_native | Misdemeanor: assault ... or a noise complaint | **「軽犯罪」の振れ幅**：重い側(assault)→軽い側(noise complaint)へラベルがスライド。スケール感 |
| 0012 | act2 | 実写/video_native | — | act3への橋渡し（「逃走だけで足りるか」）。落ち着いた寄り＋フェード |
| 0013 | act3 | **図解/graphic_anim** | 2021 — 9–0 (in judgment) / Lange v. California, 594 U.S. 295 | **年表が2021へ進む→9マス全点灯(9–0)＋"in judgment"注記→出典 594 U.S. 295 が金ラインで確定**（本話の山場グラフィック）。`LightSweep`色=GOLD |
| 0014 | act3 | ai/ken_burns | Judge each case — flight is a factor, not a trigger | **"factor" と "trigger" を対置**、trigger に×印／factor を強調。Kagan法廷意見の核心 |
| 0023 | act3 | ai/ken_burns | No automatic rule at common law | **年表/書面が過去（コモンロー）へ遡る**演出。「自動ルールは無かった」を巻物＋印章で示す |
| 0015 | act3 | ai/ken_burns | Roberts + Alito: concur in result, want a broader rule | **同じ結論（→）だが別の道筋**：結論は一致・理由は分岐する二股の線。9–0だが意見は割れることを公平に |
| 0016 | act3 | 実写/video_native | Vacated & remanded | **判決ラベルが押印され、矢印が下級審へ戻る**（破棄＝差戻し）。`stamp_seal`同期 |
| 0017 | act4 | ai/ken_burns | — | 実務上の帰結：令状か本物の緊急事態が要る。寄り（テロップ無し・余白） |
| 0018 | act4 | ai/ken_burns | — | 「明快な線ではない＝判断は増える」内省。**揺れる境界線**をゆっくり描く |
| 0019 | ending | 実写/video_native | The line at your front door | **玄関先＝最も守られる一線**。"line" を玄関に重ねて描画。落ち着いた寄り |
| 0020 | ending | ai/ken_burns | — | シリーズ統合（路上→電話→追跡→収用→DNA→言論→そして自宅）。点が連なるタイムライン演出。ゆっくり引き |
| 0021 | ending | ai/ken_burns | Finale: when does a bold promise become a crime? | **次回（フィナーレ）予告**。引き＋タイトル示唆のタイポ。CTA（Subscribe）をエンドカードで連結 |

> AI画像は1スパンに複数バリアントあり（`SPN-XXXX_02.png`等）。長いスパン（0015=50秒, 0011=38秒, 0017=34秒 等）は**約4.5秒ごとに別カット/別バリアントへ切替**し、静止・長居を避ける。importer が自動で複数取り込み。
> 実写stockは1スパンに複数あり（asset_map参照）。**数秒ずつ切替**して動きを保つ。

---

## 3. テロップ／字幕／出典のレイアウト（被らせない＝VIDEO_RULES §13）

- **字幕（ナレ全文・forced alignment）**: 画面**下部の安全帯**。**ナレと語単位でぴったり同期（ズレ≤約120ms）**・一字一句一致（`gen_captions_forced.py` 系の語単位タイムスタンプ）。早出し/遅出しを作らない。
- **見やすさ（VIDEO_RULES §13・数値）**: 文字 ≈48〜60px（1080p基準）・本文太字・**白文字＋濃い縁取り/影＋半透明黒帯(不透明度~55〜70%)**・最大2行・中央寄せ・**下部安全帯（下端から十分内側）**・1〜2行ずつ送り読み切れる表示時間（高速点滅切替しない）。
- **テロップ（キーワード＝on_screen_text）**: **上/中央**。短く・大きく。字幕帯と**重ねない**。
- **出典（金ライン）**: 例 `Lange v. California, 594 U.S. 295 (2021)`。**右下など別ポジション**固定。字幕・テロップと別レイヤ・別位置。
- 3者を同じ場所に重ねない（読めない/被るのは不可）。

## 4. 品質ゲート（書き出し前チェック＝motion-quality-gate）
- [ ] フック→オープニング→本編→エンディングの**4部**になっている
- [ ] `coded/cards = 0`（全ショット実素材 or 図解で埋まっている）
- [ ] 全ショットにモーション（静止画ゼロ）／Ken Burns 一辺倒でない
- [ ] 字幕・テロップ・出典が**位置で分離**し被っていない
- [ ] 音4層＋**ダッキング**でナレ最優先（`06_audio/audio_cue_sheet.v001.md`）
- [ ] 中立・実在人物の肖像なし・台本/claims 不改変
- [ ] **評決表記が正確**：本編・テロップ・サムネで「9–0（**判決＝差戻しは全員一致**／意見は不一致＝Roberts＋Alitoは結論同意・別理由）」を取り違えない

## 5. この話の編集ポリシー
- **中立**（住居プライバシー vs 警察の安全、どちらにも肩入れしない）。Kagan法廷意見・Roberts＋Alitoの別意見を**公平**に提示。
- **論点を取り違えない**：争点は「立入の可否」であって「DUIの有罪/無罪」ではない（SPN-0006で明示）。California主張も“悪役化”せず一つの立場として提示。
- **評決は正確に**：「9–0」は**判決（破棄差戻し）の全員一致**であり、**全員一致の意見ではない**（台本ヘッダの NEUTRALITY 指示）。
- **実在人物・判事の肖像なし**（象徴的に）。Arthur Lange 本人の顔も出さない。ディープフェイク不可。
- 実写stockは権利クリーン素材のみ（rights_note 準拠・商用可・出典記録）。曖昧な権利の素材は自動配置しない。

---

## 6. 実装方針＝Premium級コード演出（★重要・汎用RoughCutでは出ない）

§2 の「意味あるアニメ」は**汎用 `RoughCut` では描画されない**（RoughCutは Ken Burns＋動画＋テロップ＋グレイン止まり）。`RoughCut-lange`（`data/lange_roughcut.ts`・`Root.tsx`登録済）は素材ステージング/下見用に残してよいが、**最終書き出しは新規 `LangePremium`**。
→ EP14は**bespokeな `remotion/src/compositions/LangePremium.tsx` を新規作成**し、既存 `CarpenterPremium.tsx`（雛形主）／`RileyPremium.tsx`／`MadoffPremium.tsx` を参照する。

### 使う既存コード部品（再利用・新規実装を最小化）
- `components/Motion.tsx`: `MovingStage`（カメラ＋粒子＋光）, `Particles`, `LightSweep`, `Vignette`, `CameraRig`。
- `components/Grain.tsx`: `Grain`（フィルムグレイン）。
- `components/Bookends.tsx`: `BrandOpening`（seriesLabel/title/subtitle） / `BrandEndcard`（固定エンドカード＝Subscribe誘導）。`OPENING_SEC`/`ENDCARD_SEC`。
- `components/SceneArt.tsx`: `SceneArt`（`visualMode`/`motifHint`/`onScreenText`/`seed` で **小槌/天秤/書類＋印章/USマップのピン波紋/年表マーカー/法廷光/取調室ランプ** を自動選択）。motifHint 例: `"scales"`,`"gavel"`,`"document"/"seal"`,`"court"`,`visualMode="map"`,`visualMode="timeline"`。
- `CarpenterPremium.tsx` の流用可能なビズ（同ファイル内・必要分を `LangePremium.tsx` へコピー/移植）：`SceneShell`（多画像Ken Burns＋光＋粒子＋下部テロップ`Lower`＋`ReconLabel`）、`Vote`（9マスの票・**5–4表記は9–0用に改修**）、`MapGrid`、`TwoColumn`（左右対比）、`Doors`（アイコン列）、`BigNumber`、`CourtColumns`、`Boundary`（揺れる境界線）、`Triptych`。
  - 注: `Vote` は現状 `i<5` で5–4・テキスト"5–4"固定。**Langeでは「全マス点灯＝9–0」かつテキスト"9–0"／"in judgment"** に手直しして使う（または `VoteUnanimous` を `LangePremium` 内に新規・9マス全点灯）。

### ショット→実装の割り当て（§2の演出をコードに対応）
| SPN | 演出（§2） | 実装（部品） |
|---|---|---|
| 0001 | ガレージ扉＋足で止まる瞬間 | 実写`<Video>`（asset_map のmp4）＋`Vignette`/`Grain`。カット頭=足の瞬間 |
| 0002 | "warrant required" 下線強調 | AI画像＋`SceneShell`＋タイポ下線（`Lower`系の手組みハイライト） |
| 0003 | Sonoma County ロケーター | `SceneArt visualMode="map"`（USマップ＋ピン波紋）or `MapGrid`＋地名タイポ |
| 0004 | "~100 feet" 距離ラベル | AI画像＋手組み距離ラベル（路上→玄関） |
| 0005 | 扉の下の足＝立入 | 実写`<Video>`＋`Vignette`/`Grain`。短尺・速い |
| 0006 | "ENTRY" 強調／"the DUI" 取り消し線 | 実写`<Video>`＋手組みタイポ（強調＋取り消し線アニメ・`whoosh_short`同期） |
| 0007 | 「any flight = automatic entry」等式 | AI画像＋手組み等式/矢印（= と → で結ぶ） |
| 0009 | exigency 3アイコン組み上げ | 実写`<Video>`＋`Doors`（danger/evidence/escape ラベル）順次フェード |
| 0011 | 逃がすな vs 家を空洞化するな | `TwoColumn`(left="Don't let suspects escape" / right="Don't gut the home")＋`SceneArt motifHint="scales"`（天秤）を背後に |
| 0022 | 軽犯罪の振れ幅(assault↔noise) | 実写`<Video>`＋手組みスケール・バー（重→軽へラベルスライド） |
| 0013 | **年表→2021→9–0→出典確定（山場）** | `SceneArt visualMode="timeline"`（年表マーカー→2021）＋`VoteUnanimous`(9–0・"in judgment")＋`SceneArt motifHint="seal"`（書類＋印章で 594 U.S. 295）。`LightSweep`色=GOLD |
| 0014 | factor vs trigger 対置 | `TwoColumn`(left="A FACTOR" / right="NOT A TRIGGER")＋trigger側に×印（手組み） |
| 0023 | コモンローに自動ルール無し | `SceneArt visualMode="timeline"`（過去へ遡る）or `SceneArt motifHint="document"`（巻物＋印章） |
| 0015 | 9–0だが理由は分岐（Roberts+Alito） | `SceneArt motifHint="court"`＋手組み二股線（同じ結論→・別の道筋）。テロップで別意見を明示 |
| 0016 | Vacated & remanded（破棄差戻し） | 実写`<Video>`＋手組み押印＋下級審へ戻る矢印（`stamp_seal`同期） |
| 0018 | 揺れる境界線（明快な線ではない） | `Boundary`（CarpenterPremium流用の wobble する境界線。ラベルは "CASE-BY-CASE"） |
| 0020 | シリーズ統合（点が連なる） | `MapGrid` or 手組みタイムライン＋`Triptych`相当（Terry/Riley/Carpenter…の系譜を点で連結） |
| 0021 | フィナーレ予告 | AI画像＋予告タイポ→`BrandEndcard`（Subscribe）へ連結 |
| その他のai_image (0008/0010/0017) | 寄り/引き＋微パララックス | `SceneShell`（多画像Ken Burns＋`Particles`/`Vignette`/`Grain`） |
| stock_video (0012) | 実写再生 | `<Video>`＋`Vignette`/`Grain` |

### 実装ステップ
1. `LangePremium.tsx` を作成（`CarpenterPremium.tsx` を雛形にコピーし、`scenes[]` に23スパン＋hook/opening/ending を `kind` 付きで定義。AI画像は `remotion/public/lange/SPN-XXXX*.png`、実写は `remotion/public/lange/stock/*.mp4` を参照。`sceneImages('s..')` 相当のヘルパでバリアント連番を束ねる）。
   - **`Vote` を 9–0 用に改修**（全9マス点灯・テキスト"9–0"・"in judgment"注記）。または `VoteUnanimous` を新規。SPN-0013 で使用。
   - スパン尺は shotlist の `estimated_seconds` を採用（合計≒619.6秒＋オープニング/エンドカード）。`TOTAL_SEC` を実値に更新。
2. `Root.tsx` に `LangePremium`（`id="LangePremium"`・ハイフン無し＝既存Premiumと同様）を登録。`import {LangePremium, langePremiumDurationInFrames} from './compositions/LangePremium';` と `<Composition id="LangePremium" .../>` を追加。
3. `npm run studio` で `LangePremium` を確認 → §2の各演出が出ているか／4部構成か／**9–0表記が正確か**をチェック。
4. 書き出しは `LangePremium`（quality-first・libx264・§4ゲート通過後）。

> **加飾レイヤ（VIDEO_RULES §4/§12）＝DL済みファクトリ素材を活かす**: `assets/asset_manifest.v001.json`（商用OK・DL済み）から**トーンの合うものだけ**を `scripts/select_factory_assets.py` で選び `remotion/public/lange/factory/` へコピー → `LangePremium` に **背景プレート(下地)＋light/particle/vfxオーバーレイ(screen/add)＋texture(overlay)** の3層で重ね、奥行きと光で美しくダイナミックに。**意味あるアニメはコード演出が主役・factoryは加飾**（過剰にしない・合わない素材は使わない・licenseはallowedのみ）。**美しくダイナミックに**＝映画的カメラ（`MovingStage`/`CameraRig` で全カットに寄り引き/パララックス＋イージング・リニア禁止）＋ファクトリ三層加飾（背景プレート/オーバーレイ/texture）＋**山場（SPN-0013＝9–0）の“ため→開放”をSFX同期**で。詳細割り当ては §7。

---

## 7. ファクトリ素材の本格活用（テーマ別 b-roll／背景／オーバーレイ）

DL済み（商用OK・`assets/asset_manifest.v001.json`／インベントリ＝`episodes/_planning/FACTORY_INVENTORY.md`）のファクトリ棚を **本格的に活かす**。本話は警察追跡・自宅（ガレージ）への立入・夜の雨と赤青灯・司法という具体イメージが豊富で、棚の `crime_police / property_home / urban_night / light / legal_court / atmosphere_symbolic` が直に効く。**実在サブタイプ名のみ**使用（下表の subtype はすべて FACTORY_INVENTORY 記載の実名）。

### 7.1 三層構成（役割を取り違えない）
- **主役＝コード演出（意味のあるアニメ）**: 票（9–0）/年表/地図ピン/天秤/等式/二股線/押印 等。SPN-0003・0013 など §2/§6 の手組みグラフィックが情報を運ぶ。**ファクトリで置き換えない**。
- **ヒーロー＝AI画像**（`remotion/public/lange/SPN-XXXX*.png`）: 象徴・情景の主たる絵。
- **確立・b-roll・背景・overlay・texture＝ファクトリ素材**: establishing／カットアウェイ／背景プレート（薄く下地）／light・particle・vfx の screen/add 加飾／texture の overlay 下地。**加飾であって主役にしない**。1カット1〜2レイヤを目安（VIDEO_RULES §12 / §4 第6項）。

### 7.2 SPN → ファクトリ割り当て表
kind 凡例: `bg`=背景プレート(下地・薄く) / `cutaway`=数秒の確立/b-rollカット / `overlay`=screen/add加飾 / `texture`=overlay下地。層 凡例: factory=確立/b-roll/背景/加飾（主役はコード or AI）。

| SPN | シーン | theme | subtype(実在) | 層 | kind |
|---|---|---|---|---|---|
| 0001 | hook ガレージ扉＋足 | light / atmosphere_symbolic | headlights_in_rain / front_door_house | factory | overlay / bg |
| 0002 | 自宅＝聖域（thesis） | property_home / atmosphere_symbolic | suburban_house_exterior_night / front_door_house | factory | bg / cutaway |
| 0003 | Sonoma ロケーター（地図は主役=コード） | crime_police / urban_night | police_car_lights_night / rain_on_city_street_neon | factory | cutaway / bg |
| 0004 | ~100 feet from home | property_home | front_door_house / white_picket_fence | factory | bg / cutaway |
| 0005 | 扉の下の足＝立入 | atmosphere_symbolic / light | front_door_house / police_strobe_red_and_blue | factory | bg / overlay |
| 0006 | 争点は ENTRY（DUIでない） | crime_police | police_badge_close_up | factory | cutaway |
| 0007 | 州主張「flight=automatic」 | crime_police / light | police_car_lights_night / police_strobe_red_and_blue | factory | cutaway / overlay |
| 0008 | act2 導入（テロップ無） | legal_court | courtroom_interior | factory | bg |
| 0009 | exigency 3定義（アイコンは主役=コード） | crime_police | police_station_at_night / crime_scene_tape_night | factory | bg / cutaway |
| 0010 | hot pursuit の論理 | urban_night / light | rain_on_city_street_neon / headlights_in_rain | factory | bg / overlay |
| 0011 | 逃がすな vs 家を空洞化（天秤=コード） | legal_court / atmosphere_symbolic | balance_scale_brass / front_door_house | factory | cutaway / bg |
| 0022 | 軽犯罪の振れ幅（スケール=コード） | legal_court | police_badge_close_up / judge_gavel_wooden | factory | cutaway |
| 0012 | act3への橋渡し | urban_night | empty_parking_garage | factory | bg |
| 0013 | **山場 2021→9–0→出典（票/年表=主役コード）** | legal_court / light | us_constitution_document / judge_gavel_wooden | factory | texture / cutaway |
| 0014 | factor vs trigger（対置=コード） | legal_court | courtroom_interior | factory | bg |
| 0023 | コモンローに自動ルール無し | legal_court / documents_paper | us_constitution_document / law_library_books | factory | texture / cutaway |
| 0015 | 9–0だが理由分岐（Roberts+Alito） | legal_court | courtroom_interior / judge_gavel_wooden | factory | bg / cutaway |
| 0016 | Vacated & remanded（押印=コード） | legal_court | balance_scale_brass / courthouse_steps | factory | cutaway |
| 0017 | 令状か本物の緊急事態 | atmosphere_symbolic | padlock_and_chain / front_door_house | factory | cutaway / bg |
| 0018 | 揺れる境界線（Boundary=コード） | atmosphere_symbolic | front_door_house | factory | bg |
| 0019 | 玄関先＝守られる一線 | property_home / atmosphere_symbolic | front_door_house / suburban_house_exterior_night | factory | bg / cutaway |
| 0020 | シリーズ統合 | urban_night | city_skyline_dusk / empty_road_sunset | factory | bg / cutaway |
| 0021 | フィナーレ予告 | atmosphere_symbolic | storm_clouds_dramatic | factory | bg |

> 補足: 夜の雨／赤青灯の雰囲気は `light: headlights_in_rain / police_strobe_red_and_blue` と `urban_night: rain_on_city_street_neon` を screen/add で薄く重ねる。司法パートは `legal_court` の `courtroom_interior / judge_gavel_wooden / balance_scale_brass / us_constitution_document` を確立/下地に。敷居・境界の象徴は `atmosphere_symbolic: front_door_house(玄関/敷居) / padlock_and_chain`。ガレージは `urban_night: empty_parking_garage`。

### 7.3 取り込み例（select → public/lange/factory/）
```
# テーマ別 b-roll 動画を抽出（警察追跡）
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme crime_police --kind video
# 自宅/敷居（静止背景＋確立）
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme property_home
./.venv/Scripts/python.exe scripts/select_factory_assets.py --subtype front_door_house
# 司法（確立・下地）
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme legal_court --kind video
# 夜の雨/赤青灯（オーバーレイ）
./.venv/Scripts/python.exe scripts/select_factory_assets.py --subtype police_strobe_red_and_blue
./.venv/Scripts/python.exe scripts/select_factory_assets.py --subtype headlights_in_rain
# 抽出後 remotion/public/lange/factory/ へコピーして LangePremium で参照
```
> license が allowed のものだけ。出典/作者/取得日/sha256 を記録（VIDEO_RULES §5）。トーン（黒/紺/青/金）に合うものだけ採用。

### 7.4 合成指針（過剰回避・中立・権利）
- **背景プレート**＝シーン背後に `bg` を**薄く**敷く（ベタ塗り回避・被写体くっきり分離）。`MovingStage`/`CameraRig` でパララックス。
- **オーバーレイ**＝`light/vfx/particle` を **screen/add** で reveal・空気感に。**山場 SPN-0013（9–0＝判決の全員一致）**は光（`police_strobe`は使わず GOLD 系 `LightSweep`＋上品な vfx）で**ため→開放**。票/年表/出典のコード演出を邪魔しない。
- **texture**＝書類/年表/出典カードの下地に `us_constitution_document` 等を overlay。
- **中立**＝`crime_police`/`light: strobe` は緊張演出に有効だが**警察を悪役化しない**。住居プライバシー vs 警察の安全を公平に（California主張も一立場として）。
- **権利/illustrative**＝ファクトリは一般ストック。**この事件の実物・実在人物そのものとして提示しない**（symbolic/illustrative のみ）。実在人物の肖像なし。一般ストックで「Langeの自宅」「当該パトカー」等の**実物提示をしない**。
- **評決の不可侵**＝SPN-0013 周辺の加飾は「**9–0＝判決（差戻し）の全員一致**であって、**意見の全員一致ではない**（Roberts＋Alitoは結論同意・別理由）」という区別を一切侵さない（§4・§5 厳守）。加飾は雰囲気のみ・文言や記号を足さない。
- **過剰回避**＝1カット1〜2レイヤ。ナレ・字幕・テロップ・出典（金ライン）を隠さない（§3 ゾーン分離）。
