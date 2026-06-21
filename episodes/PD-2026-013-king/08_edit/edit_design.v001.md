# 第13話 king 仕上げ設計書（Edit / Finish Design） v001

対象: `PD-2026-013-king`（Maryland v. King / 逮捕時のDNA採取は「身元確認」か「捜索」か）。Codex がこの設計に従ってラフカット→仕上げを行う。
入力: `04_scenes/shotlist.v001.json`（23ショット・603.2秒≒10.1分）, `03_script/script.en.v001.md`（`[VO:]`=ナレ本文・**変更禁止**）, `04_scenes/asset_map.v001.md`, AI画像 `H:\pd-media\assets\ai\king\SPN-XXXX*.png`（生成済み前提・13スパン）, 実写動画（asset_map の `🎬 *.mp4`・6スパン分・ダウンロード済み）, サムネ `H:\pd-media\assets\ai\thumbs\king\THUMB-01..06.png`（生成済み前提）。
準拠: `episodes/_planning/VIDEO_RULES.md` §10〜13 / `docs/motion-design-language.md` / `docs/motion-quality-gate.md`。
題材の扱い（厳守）: **King は暴行(assault)で逮捕**された。レイプはDNAデータベース照合による**事後のヒット**であり、**綿棒採取が逮捕理由であるかのように示唆しない**。性犯罪題材は**ソバー**に（生々しい描写・被害再現は不可）。

---

## 1. 完成尺と4部構成（VIDEO_RULES §10 厳守）

| 部 | 構成 | ソース | 目安 |
|---|---|---|---|
| **① フック** | 本編の“盛り上がり”約8〜10カット（各1〜2秒）の高速ハイライト集＋煽り音 | 本編映像/ナレ断片の流用（新規制作しない） | 約20〜30秒 |
| **② オープニング** | 既存ブランドオープニング（`components/Bookends.tsx` の `BrandOpening`） | 既存・作り直さない | 約3.5秒 |
| **③ 本編** | act1〜act4（SPN-0003〜SPN-0018＋章内の0022/0023） | shotlist 各ショット | 約9.0分 |
| **④ エンディング** | 結末＋シリーズ統合＋次回予告（SPN-0019〜0021） | shotlist ending | 約75秒 |

**フックに使う本編ハイライト候補（priority A 優先・各1〜2秒で速いカット）**:
SPN-0001(綿棒→DNAがデータベースへ) / 0005(2003未解決事件と「一致(Match)」) / 0012(2013・5–4判決グラフィック) / 0014(Scalia＋リベラル3名の異色の反対) / 0015(「rightly or wrongly, and for whatever reason」) / 0018(一票で決まった取引) / 0020(身元確認か捜査か＝シリーズ統合) / 0021(次回への引き)。
→ ナレの決め所断片（例「In 2013, by a single vote …」「rightly or wrongly, and for whatever reason」）を1〜2個だけ被せ、最後は無音ぎみ→オープニングへブリッジ。**台本テキストは変えない**。

---

## 2. 全ショット モーション設計（Ken Burns 一辺倒にしない＝VIDEO_RULES §12）

凡例: motion は shotlist の値。**「意味のあるアニメ」列が今回の追加指定**。画像は必ず動かす。この話の論点＝**「fingerprint（身元確認）」vs「search（捜索）」**の対比と、**逮捕→綿棒→DB照合→一致**の因果線を視覚化する。

| SPN | 章 | 種別 | テロップ(on_screen_text) | 意味のあるアニメ（指定） |
|---|---|---|---|---|
| 0001 | hook | 図解/graphic_anim | Arrested — not convicted. They take your DNA. | 綿棒モチーフ→**DNA二重らせんがデータベース格子へ吸い込まれる**動き。booking部屋の質感・顔なし・象徴的（AI開示） |
| 0002 | opening | ai/ken_burns | Identification — or a search? | 「身元確認」と「捜索」の2語をタイポで提示し、**"or" を境に左右へ分かれる**。憲法（第4修正）の質感を背景に |
| 0003 | act1 | 図解/graphic_anim | Maryland, 2009 — arrested for assault | 地図ロケーター：**USマップ→Maryland にピン波紋**＋年表が **2009** へ進む。テロップで「assault（暴行）」を明示し前提を固定 |
| 0004 | act1 | ai/ken_burns | The swab was NOT the reason for arrest | 綿棒のカットへ寄り、**"NOT" を赤系で強調**（誤解防止の最重要テロップ）。落ち着いた寄り |
| 0005 | act1 | 図解/graphic_anim | Match: an unsolved 2003 case | **DNAプロファイルがDB格子を走査→1セルが「MATCH」点灯**（ソバー・非グラフィック）。年表に **2003** を小さく示す |
| 0006 | act1 | 実写/native | A cold case solved — vs — a suspicionless search | **2つの見方を左右対比**で提示（解決した未解決事件 ／ 嫌疑なき捜索）。やや速いカットで緊張 |
| 0007 | act1 | ai/ken_burns | — | 「両方とも真実」への転換。寄り＋微パララックス・フェード |
| 0008 | act2 | ai/ken_burns | Fingerprint or search? | **中心の問い**。指紋アイコンと虫眼鏡アイコンを左右に置き、軽いズームパンチ |
| 0009 | act2 | 実写/native | Booking: fingerprints + photo = identify | booking手続の実写。**「指紋＋写真＝身元確認」の等式カード**を下に重ねる |
| 0010 | act2 | ai/ken_burns | State: "the fingerprint of the 21st century" | 州側の主張。**指紋→DNAへモーフ**し「21世紀の指紋」ラベルを添える |
| 0011 | act2 | ai/ken_burns | CODIS — the FBI's national DNA database | **CODIS＝全米DNAデータベースのネットワーク図**。多数のノードが点灯し中央へ収束（規模感）。批判側の論点 |
| 0022 | act2 | 実写/native | A fingerprint vs. a genetic blueprint | **指紋（点の集合）と遺伝子の設計図を左右対比**。「指紋＝情報少／DNA＝設計図」の質的差を静かに示す |
| 0012 | act3 | **図解/graphic_anim** | 2013 — 5–4 ／ Maryland v. King, 569 U.S. 435 | **年表が2013へ進む→5–4の票が並ぶ→出典 569 U.S. 435 が金ラインで確定**（本話の山場グラフィック） |
| 0013 | act3 | 実写/native | "like fingerprinting and photographing" | 多数意見（Kennedy）。法廷/小槌の実写に**引用句テロップ**「指紋・写真撮影と同様」。落ち着いた寄り |
| 0023 | act3 | ai/ken_burns | — | Kennedyの「identification は名前より広い」理由づけ。**注記カラム**で「危険性/逃亡/拘束中の安全処理」を静かに提示 |
| 0014 | act3 | ai/ken_burns | Dissent: Scalia + Ginsburg, Sotomayor, Kagan | **異色の連合**。保守(Scalia)とリベラル3名の名が**中央で1本に合流**する図（通常の対立軸を越えた一致） |
| 0015 | act3 | ai/ken_burns | "...rightly or wrongly, and for whatever reason" | Scalia反対意見の決め句。**引用句が1語ずつ刻まれる**タイポ。重さのある寄り（誇張せず） |
| 0016 | act4 | 実写/native | — | 「全米で逮捕＝DNA提供」へ。実写を数秒ずつ切替、落ち着いた進行 |
| 0017 | act4 | ai/ken_burns | It solves crimes. It also files the merely arrested. | **天秤の両皿**：左「事件解決」右「単に逮捕された人々の登録」。**どちらにも傾けすぎない**バランス演出 |
| 0018 | act4 | ai/ken_burns | — | 「一票で決まった取引」。寄りで感情の余白。中立に締める |
| 0019 | ending | 実写/native | Identify you — or investigate you? | 結末の総括。**「身元確認 ／ 捜査」を最後にもう一度左右対比**。ゆっくり引き |
| 0020 | ending | ai/ken_burns | — | シリーズ統合「pockets→phone→property→contracts→body」。**5つの語が順に積み上がり最後に "body" で確定** |
| 0021 | ending | ai/ken_burns | Next: can a cop follow you into your home? | **次回予告**。「home（家）」のドアのモチーフへ引き＋タイトル示唆のタイポ |

> AI画像は1スパンに複数バリアントあり（`SPN-XXXX_02.png`等）。長いスパン（例 0011=47s, 0015=49s）は**約4.5秒ごとに別カット/別バリアントへ切替**し、静止・長居を避ける（`SceneShell` が複数画像を自動クロスフェード）。
> 実写スパン（0006/0009/0013/0016/0019/0022）は asset_map の `🎬 *.mp4` を数秒ずつ切替。**人物の顔・実在人物は出さない**（象徴的素材のみ）。

---

## 3. テロップ／字幕／出典のレイアウト（被らせない＝VIDEO_RULES §13）

- **字幕（ナレ全文・forced alignment）**: 画面**下部の帯**。常時ナレと語単位同期。
- **テロップ（キーワード＝on_screen_text）**: **上/中央**（`Lower` は左上）。短く・大きく。字幕帯と**重ねない**。
- **出典（金ライン）**: 例 `Maryland v. King, 569 U.S. 435 (2013)`。**右下など別ポジション**固定。字幕・テロップと別レイヤ・別位置。
- 「AI開示」「symbolic reconstruction」表示（`ReconLabel`＝右上）は出典・テロップと**位置で分離**。
- 3者（字幕・テロップ・出典）を同じ場所に重ねない（読めない/被るのは不可）。

## 4. 品質ゲート（書き出し前チェック＝motion-quality-gate）
- [ ] フック→オープニング→本編→エンディングの**4部**になっている
- [ ] `coded/cards = 0`（全ショット実素材 or 図解で埋まっている）
- [ ] 全ショットにモーション（静止画ゼロ）／Ken Burns 一辺倒でない
- [ ] 字幕・テロップ・出典が**位置で分離**し被っていない
- [ ] 音4層＋**ダッキング**でナレ最優先（`06_audio/audio_cue_sheet.v001.md`）
- [ ] **「綿棒＝逮捕理由」と誤読させる演出がない**（0003/0004で前提を固定）／性犯罪題材はソバー
- [ ] 中立・実在人物の肖像なし（Kennedy/Scalia/Ginsburg等を肖像で描かない）・台本/claims 不改変

## 5. この話の編集ポリシー
- **中立**（公共安全 vs プライバシー、どちらにも肩入れしない）。Kennedy多数意見と Scalia反対意見を**公平**に提示。
- **題材の節度**: King の逮捕理由（暴行）と、事後のDB照合（レイプ事件の解決）を**明確に分離**して描く。被害の再現・センセーショナルな描写は不可。
- **実在人物・判事の肖像なし**（象徴・タイポで代替）。ディープフェイク不可。AI画像は必ず開示。

---

## 6. 実装方針＝Premium級コード演出（★重要・汎用RoughCutでは出ない）

§2 の「意味あるアニメ」は**汎用 `RoughCut` では描画されない**（RoughCutは Ken Burns＋動画＋テロップ＋グレイン止まり）。
→ EP13は**bespokeな `remotion/src/compositions/KingPremium.tsx` を新規作成**し、既存 `CarpenterPremium.tsx`（同シリーズ・同論点系）を雛形にする。`RoughCut-king`（`Root.tsx` に登録済）は素材ステージング/下見用に残してよいが、**最終書き出しは `KingPremium`**。

### 使う既存コード部品（再利用・新規実装を最小化）
- `components/Motion.tsx`: `MovingStage`（カメラ＋粒子＋光）, `Particles`, `LightSweep`, `Vignette`, `CameraRig`。
- `components/Grain.tsx`: `Grain`（フィルムグレイン）。
- `components/Bookends.tsx`: `BrandOpening`（`seriesLabel`/`title`/`subtitle`）/ `BrandEndcard`（固定エンドカード）/ `OPENING_SEC`(3.5)/`ENDCARD_SEC`(9)。
- `components/SceneArt.tsx`: `SceneArt`（props=`visualMode`/`motifHint`/`onScreenText`/`seed`）。`motifHint` で **timeline / map / document(=seal,constitution) / scales(=justice) / gavel / courtroom / room** を自動選択。
- `CarpenterPremium.tsx` の流用可能なビズ（**同ファイル内・private なので KingPremium へ移植/再実装**）：`Vote`(5–4票)、`MapGrid`、`TwoColumn`(左右対比)、`Doors`(アイコン/語の列・順次)、`BigNumber`、`CourtColumns`、`Triptych`、`Boundary`、`SceneShell`（多画像Ken Burns＋光＋粒子＋`Lower`テロップ＋`ReconLabel`＋`Vignette`＋`Grain`）。

### ショット→実装の割り当て（§2の演出をコードに対応）
| SPN | 演出（§2） | 実装（部品） |
|---|---|---|
| 0001 | 綿棒→DNAらせんがDBへ吸い込まれる | 手組みSVG（らせん→格子）＋`MovingStage`。`SceneArt motifHint="document"` を背景下地に流用可。`ReconLabel`（AI開示）併記 |
| 0002 | 「identification か search か」左右分岐 | 手組みタイポ＋`TwoColumn`(left="Identification" / right="Search") |
| 0003 | Maryland 2009 ロケーター＋年表 | `SceneArt visualMode="map" motifHint="map pin"`（USマップ＋ピン波紋）＋`SceneArt visualMode="timeline"`（2009）。テロップ "assault" |
| 0004 | "NOT the reason" 強調 | AI画像（綿棒/booking）＋`Lower`テロップ（"NOT" を赤系で手組み強調） |
| 0005 | DB走査→1セルが MATCH 点灯 | `MapGrid`（格子）＋手組みハイライト点灯（`data_blip`同期）。`BigNumber` 不使用、ソバー |
| 0006 | 解決 vs 嫌疑なき捜索 の対比 | `<Video>` 実写＋`TwoColumn`(left="Cold case solved" / right="Suspicionless search") |
| 0008 | 指紋 or 捜索（中心の問い） | AI画像＋手組み（指紋アイコン／虫眼鏡）＋軽ズーム |
| 0009 | 指紋＋写真＝身元確認 | `<Video>` 実写＋手組み等式カード（fingerprints + photo = identify） |
| 0010 | 指紋→DNAへモーフ「21世紀の指紋」 | AI画像＋手組みモーフ＋ラベル |
| 0011 | CODIS ネットワーク図が収束 | 手組みSVGノードネットワーク（`Particles`流用可）＋`Lower`テロップ "CODIS" |
| 0022 | 指紋 vs 遺伝子の設計図 | `<Video>` 実写＋`TwoColumn`(left="Fingerprint" / right="Genetic blueprint") |
| 0012 | **年表→2013→5–4→出典確定（山場）** | `SceneArt visualMode="timeline"`（2013）＋`Vote`(5–4)＋`SceneArt motifHint="seal"`（書類＋印章で 569 U.S. 435）。`LightSweep`色=GOLD・`scene.kind="ruling"` |
| 0013 | 「指紋・写真と同様」引用句 | `<Video>` 実写（法廷/小槌）＋`Lower`引用句テロップ＋`CourtColumns`（背景・薄） |
| 0023 | Kennedyの「広いidentification」注記 | AI画像＋手組み注記カラム（dangerousness / flight risk / safe processing） |
| 0014 | Scalia＋リベラル3名が合流 | AI画像＋手組み（4名の名→1本に合流するライン）。肖像は不可・名前タイポのみ |
| 0015 | "rightly or wrongly..." を1語ずつ刻む | AI画像＋手組みタイポ（`whoosh_short`/`ui_tick`同期） |
| 0017 | 天秤の両皿（解決 ／ 単なる逮捕者登録） | `SceneArt motifHint="scales"`（天秤）＋左右ラベル。傾けすぎない |
| 0019 | 身元確認 ／ 捜査（締めの対比） | `<Video>` 実写＋`TwoColumn`(left="Identify you" / right="Investigate you") |
| 0020 | pockets→phone→property→contracts→body 積み上げ | `Doors` または手組み積層（5語順次フェード・最後 "body" を金で確定） |
| 0021 | 次回「home」ドアへ引き | AI画像（家/ドア）＋`Lower`テロップ（次回予告） |
| その他のai_image (0007/0018) | 寄り/引き＋微パララックス | `SceneShell`相当（多画像Ken Burns＋`Particles`/`Vignette`/`Grain`） |
| stock_video (0016) | 実写再生 | `<Video>`＋`Vignette`/`Grain` |

### 実装ステップ
1. `KingPremium.tsx` を作成（`scenes[]` に23スパン＋hook/opening/ending を `kind` 付きで定義。`start`/`dur` は shotlist の `estimated_seconds` を積算。AI画像は `remotion/public/king/SPN-XXXX*.png`、実写は `remotion/public/king/<*.mp4>` を参照）。`CarpenterPremium.tsx` を雛形にコピーし、private な `Vote`/`MapGrid`/`TwoColumn`/`Doors`/`BigNumber`/`CourtColumns`/`Boundary`/`Triptych`/`SceneShell`/`Lower`/`ReconLabel` を本ファイルに移植。
2. `Root.tsx` に `KingPremium`（`id="KingPremium"`・ハイフンのみ）を登録（`import {KingPremium, kingPremiumDurationInFrames} from './compositions/KingPremium';` ＋ `<Composition id="KingPremium" ... durationInFrames={kingPremiumDurationInFrames(BRAND.video.fps)} />`）。既存 `RoughCut-king` は残す。
3. `npm run studio` で `KingPremium` を確認 → §2の各演出（特に 0012 山場・0014 異色連合・0017 天秤バランス）が出ているか／4部構成か／§4ゲートをチェック。
4. 書き出しは `KingPremium`（CPU/libx264・品質優先）。

> 注：共有素材棚（factory: vfx/light/particle/loops）は**このPremium経路では使わない**（コード演出＝`Particles`/`LightSweep` 等で代替。factory(stock)は使わない）。AI画像・実写stock(.mp4)のみ素材として取り込む。
