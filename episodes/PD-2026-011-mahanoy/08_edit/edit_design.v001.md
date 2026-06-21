# 第11話 mahanoy 仕上げ設計書（Edit / Finish Design） v001

対象: `PD-2026-011-mahanoy`（Mahanoy Area School District v. B.L. / 学校外でのSnapchat投稿と生徒の言論の自由）。Codex がこの設計に従ってラフカット→仕上げを行う。
入力: `04_scenes/shotlist.v001.json`（28ショット・606秒≒10.1分）, `03_script/script.en.v001.md`（`[VO:]`=ナレ本文・**変更禁止**）, `04_scenes/asset_map.v001.md`, AI画像 `H:\pd-media\assets\ai\mahanoy\SPN-XXXX*.png`（生成済み前提）, サムネ `H:\pd-media\assets\ai\thumbs\mahanoy\THUMB-01..06.png`（生成済み前提）。
準拠: `episodes/_planning/VIDEO_RULES.md` §10〜13 / `docs/motion-design-language.md` / `docs/motion-quality-gate.md`。
本話の論点: **学校は、生徒が学校外・週末に自分のスマホで投稿した言葉を罰せるか**（Tinker の "substantial disruption" 基準 / "schoolhouse gate" / 8–1 判決 / Breyer "nurseries of democracy" / Thomas 単独反対）。

> 広告安全（最重要）: 投稿本文の罵倒語は**絶対に読まない・表示しない**。常に **CENSORED/ぼかし** で扱う（台本冒頭の ADVERTISER SAFETY 指示）。実在人物（Brandi Levy 含む）の肖像は出さない＝象徴表現のみ（invariant 11）。

---

## 1. 完成尺と4部構成（VIDEO_RULES §10 厳守）

| 部 | 構成 | ソース | 目安 |
|---|---|---|---|
| **① フック** | 本編の“盛り上がり”約10カット（各1〜2秒）の高速ハイライト集＋煽り音 | 本編映像/ナレ断片の流用（新規制作しない） | 約20〜30秒 |
| **② オープニング** | 既存ブランドオープニング（`Bookends.tsx` の `BrandOpening`） | 既存・作り直さない | 約3.5秒（`OPENING_SEC`） |
| **③ 本編** | act1〜act4（SPN-0003〜0021,0026〜0028 を物語順に） | shotlist 各ショット | 約9.0分 |
| **④ エンディング** | 結末＋次回予告＋CTA/フォロー誘導（SPN-0022〜0025） | shotlist ending | 約75秒 |

**フックに使う本編ハイライト候補（priority A 優先・各1〜2秒で速いカット）**:
SPN-0001(深夜のスマホで投稿＝コールドオープン) / 0006(「スナップは“消える”—スクショは消えない」転機) / 0014(2021・8–1判決グラフィック) / 0027(Breyer「民主主義の苗床」) / 0016(「混乱＝授業中の数分のざわつきだけ」) / 0018(Thomas単独反対) / 0017(「それでも届く範囲：いじめ・脅迫・カンニング」) / 0021(「自由は“嫌いな言論”で試される」) / 0015(Breyer判決理由) / 0024(次回への引き)。
→ ナレの決め所断片を1〜2個だけ被せ、最後は無音ぎみ→オープニングへブリッジ。**台本テキストは変えない**。投稿文の罵倒は**音声でも字幕でも出さない**。

---

## 2. 全ショット モーション設計（Ken Burns 一辺倒にしない＝VIDEO_RULES §12）

凡例: motion は shotlist の値。**「意味のあるアニメ」列が今回の追加指定**。画像は必ず動かす。本話の論点（学校の権限 vs 生徒の声 / "schoolhouse gate"＝門 / 8–1）に即して各ショットに意味を割り当てる。

| SPN | 章 | 種別 | テロップ(on_screen_text) | 意味のあるアニメ（指定） |
|---|---|---|---|---|
| 0001 | hook | stock/native | Can your school punish your weekend post? | 深夜のスマホ画面に**投稿がタイプされ→送信→[CENSORED]の黒バーが被さる**。寄り＋微パララックス。罵倒は表示しない |
| 0002 | opening | 図解/graphic_anim | "...at the schoolhouse gate" — Tinker, 1969 | **"schoolhouse gate"（校門）が線で描かれ、その上に First Amendment 条文タイポ**。"gate" を金で強調。Tinker,1969 を出典金ラインで |
| 0003 | act1 | 図解/graphic_anim | Mahanoy, PA — 2017 | 地図ロケーター：PA→Mahanoy に**ピンが落ちて地名＋2017が描かれる** |
| 0004 | act1 | ai/ken_burns | — | JV(控え)に留め置かれ、年下が昇格＝**落胆**。机/教室へ寄り、上方向に小さな矢印（昇格）と対の下向き（留置）の含意 |
| 0005 | act1 | stock/native | [caption censored] | 象徴Snapchatフレーム。**キャプション帯は常時 [CENSORED] でぼかし**。手は影絵・顔なし。投稿の“勢い”だけを示す |
| 0006 | act1 | ai/ken_burns | Snaps "disappear" — screenshots don't | **“消える”アニメ（フェードアウト）→スクショのフラッシュで“固定”**。`camera_shutter`同期。本話の転機ビート |
| 0007 | act1 | stock/native | Suspended from JV cheer — 1 year | スマホ→処分。**"1 year" を強調**（懲戒の重さ）。やや速いカット |
| 0008 | act1 | ai/ken_burns | School's order vs. a student's voice | **左右対比：左＝学校の命令（重く）／右＝生徒の声（小さく）**。中央で対立を示す |
| 0028 | act1 | stock/native | — | 「どれほど“ありふれた”発言だったか」。脅威なし・標的なし＝**静かな寄り**で余白 |
| 0026 | act2 | 図解/graphic_anim | 1965: armbands to mourn the war dead | **1965へ年表が戻り、黒い腕章のシルエット**が描かれる（沈黙の抗議）。Tinkerの背景 |
| 0009 | act2 | 図解/graphic_anim | Tinker v. Des Moines (1969) | **年表が1969へ進む→事件名カードが確定**。出典金ライン |
| 0010 | act2 | ai/ken_burns | Test: "substantial disruption" | **基準カード「substantial disruption」が中央に組み上がる**。下線ハイライト |
| 0011 | act2 | stock/native | — | 「50年は機能した＝“場所”があったから」。落ち着いた寄り |
| 0012 | act2 | ai/ken_burns | The phone erased the gate | **校門（gate）の線が、スマホの光で消去/溶解する**アニメ（本話の中心メタファ）。`whoosh_short`同期 |
| 0013 | act2 | ai/ken_burns | — | 「論理に“止まる場所”がない」＝**24hの時計＋四方へ広がる波紋**で“際限なさ”を示す |
| 0014 | act3 | **図解/graphic_anim** | 2021 — 8–1 / Mahanoy v. B.L., 594 U.S. 180 | **年表が2021へ進む→8–1の票が並ぶ→出典 594 U.S. 180 が金ラインで確定**（本話の山場グラフィック） |
| 0015 | act3 | stock/native | — | Breyer 多数意見の理由。落ち着いた寄り＋微パララックス（実写） |
| 0016 | act3 | ai/ken_burns | Disruption: a few minutes of class chatter | **「混乱」の天秤がほぼ動かない**＝実害ごく僅か。`data_blip`軽く |
| 0027 | act3 | ai/ken_burns | "nurseries of democracy" — Breyer | **“苗床”＝若木/芽が育つモチーフ＋引用符**。Breyerの核心。引用は金で強調 |
| 0017 | act3 | ai/ken_burns | Still reachable: bullying · threats · cheating | **3つのアイコン（いじめ/脅迫/カンニング）が順に点灯**＝学校が届きうる例外。白紙小切手は与えない |
| 0018 | act3 | stock/native | Dissent: Thomas, J. (alone) | **8人の中で1票だけ色が反転**＝単独反対。`low_boom`軽く |
| 0019 | act4 | ai/ken_burns | — | 「保護はあるが意図的に曖昧」＝**点線（pencil line）が揺れる境界**。寄り |
| 0020 | act4 | ai/ken_burns | — | 「壁ではない＝深刻ケースには扉が開く」。**閉じた壁→一部の扉が開く**含意 |
| 0021 | act4 | stock/native | Free speech is tested by speech we dislike | 本話の主題。**テロップを大きく**＝主張の核。落ち着いた寄り |
| 0022 | ending | ai/ken_burns | — | 結末の総括（14歳の週末が時代の境界線に）。ゆっくり引き |
| 0023 | ending | ai/ken_burns | — | シリーズ統合（捜索→追跡→収用→言論）。**4テーマが1本の線でつながる**。ゆっくり引き |
| 0024 | ending | stock/native | Next: the right you sign away | **次回予告**。引き＋タイトル示唆のタイポ（“署名で手放す権利”＝強制仲裁） |
| 0025 | ending | ai/ken_burns | Subscribe | **CTA**：Subscribe ボタン演出＋フォロー誘導（1.6秒） |

> AI画像は1スパンに複数バリアントあり（`SPN-XXXX_02.png`等）。長いスパン（0017/0023等）は**約4.5秒ごとに別カット/別バリアントへ切替**し、静止・長居を避ける。importer が自動で複数取り込み。
> 物語順の注意: shotlist の SPN番号は時系列と一致しない。**章順（act1→act2→act3→act4→ending）で並べる**こと。特に 0028 は act1、0026 は act2、0027 は act3 に挿入する（上表の並び＝編集順）。

---

## 3. テロップ／字幕／出典のレイアウト（被らせない＝VIDEO_RULES §13）

- **字幕（ナレ全文・forced alignment）**: 画面**下部の帯**。常時ナレと語単位同期。**投稿の罵倒語は字幕にも出さない**（描写文のみ）。
- **テロップ（キーワード＝on_screen_text）**: **上/中央**。短く・大きく。字幕帯と**重ねない**。
- **出典（金ライン）**: 例 `Mahanoy Area School Dist. v. B.L., 594 U.S. 180 (2021)` / `Tinker v. Des Moines, 393 U.S. 503 (1969)`。**右下など別ポジション**固定。字幕・テロップと別レイヤ・別位置。
- **CENSORED帯**: 投稿/キャプションのぼかしは**映像レイヤ**で、字幕・テロップとは独立に常時被せる（SPN-0001/0005）。
- 4者（字幕/テロップ/出典/CENSORED）を同じ場所に重ねない（読めない/被るのは不可）。

## 4. 品質ゲート（書き出し前チェック＝motion-quality-gate）
- [ ] フック→オープニング→本編→エンディングの**4部**になっている
- [ ] `coded/cards = 0`（全ショット実素材 or 図解で埋まっている）
- [ ] 全ショットにモーション（静止画ゼロ）／Ken Burns 一辺倒でない
- [ ] 字幕・テロップ・出典・CENSORED帯が**位置で分離**し被っていない
- [ ] **投稿の罵倒語が音声・字幕・画面のどこにも出ていない**（広告安全）
- [ ] 実在人物（Brandi Levy・各判事）の肖像なし・象徴表現のみ
- [ ] 音4層＋**ダッキング**でナレ最優先（`06_audio/audio_cue_sheet.v001.md`）
- [ ] 中立・台本/claims 不改変・SPNは章順に並んでいる

## 5. この話の編集ポリシー
- **中立**: 学校の懲戒権限 vs 生徒の言論の自由、どちらにも肩入れしない。多数意見（Breyer）・例外（いじめ/脅迫/カンニング）・反対意見（Thomas）を**公平**に提示。
- **広告安全が最優先**: 投稿の罵倒語は読まない・出さない。常に描写＋CENSORED。
- **実在人物・判事の肖像なし**（象徴的に）。ディープフェイク不可（invariant 11）。生徒は未成年であり、特に配慮する。
- 台本・claims・shotlist は**不改変**（Read専用）。SPNの章順並べ替えのみ編集側で行う。

---

## 6. 実装方針＝Premium級コード演出（★重要・汎用RoughCutでは出ない）

§2 の「意味あるアニメ」は**汎用 `RoughCut` では描画されない**（`RoughCut-mahanoy` は Ken Burns＋動画＋テロップ＋グレイン止まり）。
→ EP11は**bespokeな `remotion/src/compositions/MahanoyPremium.tsx` を新規作成**し、既存 `CarpenterPremium.tsx` / `GideonPremium.tsx` / `MadoffPremium.tsx` を雛形にする。`RoughCut-mahanoy` は素材ステージング/下見用に残してよいが、**最終書き出しは `MahanoyPremium`**。

### 使う既存コード部品（再利用・新規実装を最小化）
- `components/Motion.tsx`: `MovingStage`（カメラ＋粒子＋光）, `CameraRig`, `Particles`, `LightSweep`, `Vignette`。
- `components/Grain.tsx`: `Grain`（フィルムグレイン）。
- `components/Bookends.tsx`: `BrandOpening`（`seriesLabel="Prime Documentary"` title="Mahanoy" subtitle="The phone and the schoolhouse gate"）/ `BrandEndcard`（固定エンドカード）, 定数 `OPENING_SEC`/`ENDCARD_SEC`。
- `components/SceneArt.tsx`: `SceneArt`（`visualMode`/`motifHint`/`onScreenText`/`seed` で **timeline（年表）/map（USマップ＋ピン波紋）/document（書類＋印章）/courtroom/scales（天秤）/gavel** を自動選択）。`pickArt` のヒント語に注意（"court"→courtroom、"justice/scales"→scales、"document/seal/constitution"→document）。
- `CarpenterPremium.tsx` の流用可能なビズ（同ファイル内で定義・コピーして使う）: `Vote`（票グラフィック・**8–1へ改変**）, `TwoColumn`（左右対比）, `Doors`（アイコン列）, `BigNumber`, `CourtColumns`, `Boundary`（揺れる境界線＝“pencil line”）, `MapGrid`, `SceneShell`（多画像Ken Burns＋光＋グレイン＋テロップ）。

### ショット→実装の割り当て（§2の演出をコードに対応）
| SPN | 演出（§2） | 実装（部品） |
|---|---|---|
| 0001 | 投稿タイプ→送信→CENSORED | stock `<Video>`＋手組みCENSORED黒バー＋`Vignette`/`Grain` |
| 0002 | 校門＋First Amendment条文／"gate"金強調 | 手組み“gate”SVG＋タイポ（出典金ライン）。`SceneArt motifHint="constitution"` を背景に併用可 |
| 0003 | Mahanoy,PA—2017 ロケーター | `SceneArt visualMode="map" motifHint="map"`（USマップ＋ピン波紋） |
| 0006 | “消える→スクショで固定” | AI画像＋フェードアウト→白フラッシュ（`camera_shutter`同期）。`SceneShell`ベース |
| 0008 | 学校の命令 vs 生徒の声 | `TwoColumn`(left="School's order" right="A student's voice") |
| 0026 | 1965・黒い腕章 | `SceneArt visualMode="timeline" motifHint="timeline"`＋手組み腕章シルエット |
| 0009 | Tinker 1969 年表＋事件カード | `SceneArt visualMode="timeline" motifHint="timeline"`（出典金ライン） |
| 0010 | "substantial disruption" カード | 手組みカード（下線ハイライト）or `TwoColumn` 単カラム |
| 0012 | **校門がスマホの光で消える（中心メタファ）** | 手組み“gate”SVG＋`LightSweep`で溶解＋`whoosh_short`。`SceneShell`上に重畳 |
| 0013 | 24h時計＋四方の波紋（際限なさ） | `SceneArt motifHint="map"`（波紋流用）＋手組み24h時計 or `Boundary`（境界が定まらない含意） |
| 0014 | **年表→2021→8–1→出典確定（山場）** | `SceneArt motifHint="timeline"`（2021）＋`Vote`(**8–1に改変**)＋`SceneArt motifHint="seal/document"`（594 U.S. 180）。`LightSweep`色=GOLD |
| 0016 | 「混乱」の天秤がほぼ動かない | `SceneArt visualMode="object" motifHint="scales"`（天秤・僅かな傾き） |
| 0017 | いじめ/脅迫/カンニングが点灯 | `Doors labels={['bullying','threats','cheating']}`（順次点灯） |
| 0018 | 8人中1票だけ反転＝Thomas単独反対 | `Vote` 改変（8–1で1マスだけ色反転を強調）or `TwoColumn`(left="Majority 8" right="Thomas, J. alone") |
| 0019 | 揺れる点線の境界（pencil line） | `Boundary`（揺れる境界線。ラベル="A line in pencil"） |
| 0020 | 壁→一部の扉が開く | `Doors`（1枚だけ開＝深刻ケースの例外） |
| 0023 | 4テーマが1本の線でつながる | `Triptych` 相当を4枠に手組み（search/track/property/speech）or `Doors labels={['search','track','take','speak']}` |
| 0025 | CTA Subscribe | 手組みSubscribeボタン＋`soft_impact`（or 直接 `BrandEndcard` へブリッジ） |
| その他のai_image (0004/0007*/0011*/0015*/0021*/0022/0027) | 寄り/引き＋微パララックス | `SceneShell`相当（多画像Ken Burns＋`Particles`/`Vignette`/`Grain`）。※0007/0011/0015/0021/0024/0028はstock動画＝`<Video>`＋`Vignette`/`Grain` |

> `Vote` は CarpenterPremium 内で 5–4 固定（9マス・i<5 を yes 着色・テキスト"5–4"）。本話は **8マスを多数・1マスを反対**に変え、テキストを"8–1"にする（`MahanoyPremium.tsx` 側にコピーして改変。元ファイルは触らない）。

### 実装ステップ
1. `MahanoyPremium.tsx` を作成（`scenes[]` に28スパン＋hook/opening/ending を kind 付きで定義。**章順に並べる**。AI画像は `remotion/public/mahanoy/SPN-XXXX*.png`、stock動画は `remotion/public/mahanoy/<file>.mp4` を参照）。
2. `Root.tsx` に `MahanoyPremium`（`id="MahanoyPremium"`）を登録（ハイフンのみ・既存 `MadoffPremium` ブロックに倣う）。`import {MahanoyPremium, mahanoyPremiumDurationInFrames} from './compositions/MahanoyPremium';`。
3. `npm run studio` で `MahanoyPremium` を確認 → §2の各演出（gate消去/8–1/天秤/苗床/3アイコン/単独反対）が出ているか・4部構成か・**罵倒語が一切出ていない**かをチェック。
4. 書き出しは `MahanoyPremium`（quality-first・CPU/libx264）。

> 注：今DL中の共有素材棚（factory: vfx/light/particle/loops）は**このPremium経路では使わない**（コード演出＝`Particles`/`LightSweep`/`SceneArt` 等で代替。stock素材は将来のギャップ補完・バリエーション用）。
