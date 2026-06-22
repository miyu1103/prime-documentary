# 第15話 theranos 仕上げ設計書（Edit / Finish Design） v001 — SERIES FINALE

対象: `PD-2026-015-theranos`（United States v. Holmes / Theranos・詐欺の境界線）。Codex がこの設計に従ってラフカット→仕上げを行う。
入力: `04_scenes/shotlist.v001.json`（24ショット・612.4秒≒10.2分）, `03_script/script.en.v001.md`（`[VO:]`=ナレ本文・**変更禁止**）, `04_scenes/asset_map.v001.md`, AI画像 `H:\pd-media\assets\ai\theranos\SPN-XXXX*.png`（🎨12場面・生成済み前提）, ストック動画（✅7場面・DL済み）, サムネ `H:\pd-media\assets\ai\thumbs\theranos\THUMB-01..06.png`（生成済み前提）。
準拠: `episodes/_planning/VIDEO_RULES.md` §10〜13 / `docs/motion-design-language.md` / `docs/motion-quality-gate.md` / **CLAUDE.md 不変項11（生成映像は記録ではない・実在人物の肖像なし）**。

> **⚠ R3 / 法的高リスク話。公開前に法務レビュー必須（本書 §4・§5）。** 実在人物（Elizabeth Holmes / Ramesh Balwani 等）の**肖像・実写・ディープフェイク・断定的な有罪表現は不可**。表現は象徴的・一般化に徹し、事実は**判決／公開記録ベース**。投資家詐欺の**4件有罪は事実として提示**してよいが、患者関連は「無罪（acquitted）」、3件は「評決不成立（mistrial / no verdict）」であり、**「有罪」と書かない**。意図・認識は**陪審／裁判所に帰属**させ、ナレーター（チャンネル）の断定にしない。台本・claims は一切変更しない。

---

## 1. 完成尺と4部構成（VIDEO_RULES §10 厳守）

| 部 | 構成 | ソース | 目安 |
|---|---|---|---|
| **① フック** | 本編の“盛り上がり”約10カット（各1〜2秒）の高速ハイライト集＋煽り音 | 本編映像/ナレ断片の流用（新規制作しない） | 約20〜30秒 |
| **② オープニング** | 既存ブランドオープニング（`components/Bookends.tsx` の `BrandOpening`） | 既存・作り直さない | 約3.5秒 |
| **③ 本編** | act1〜act4（SPN-0002〜SPN-0019・台本順に再配列） | shotlist 各ショット | 約9分 |
| **④ エンディング** | 結末＋シリーズ総括＋CTA/フォロー誘導（SPN-0020〜0022） | shotlist ending | 約75秒 |

> **章順の注意**: shotlist は `span_id` 昇順だが、`chapter_id` は台本の流れ（act1→act2→act3→act4→ending）に従って配置すること。具体的には **SPN-0023(act1) は SPN-0005 と 0006 の間**、**SPN-0024(act3) は SPN-0012 と 0013 の間** に挿入する（asset_map のナレ対応に一致）。台本テキストは変えない。

**フックに使う本編ハイライト候補（priority A 優先・各1〜2秒で速いカット）**:
SPN-0001(一滴の血＋$9B→$0グラフ) / 0008(他社の機械で検査) / 0013(2022・4件有罪の評決ボード) / 0014(患者は無罪・3件評決なし) / 0015(無罪≠潔白／Balwani全12件) / 0016(量刑 約11年3か月) / 0012(詐欺＝欺く意図) / 0024(検察 vs 弁護の二分) / 0002(シリーズ最終回の問い) / 0021(シリーズ総括への引き)。
→ ナレの決め所断片を1〜2個だけ被せ、最後は無音ぎみ→オープニングへブリッジ。**台本テキストは変えない**。

---

## 2. 全ショット モーション設計（Ken Burns 一辺倒にしない＝VIDEO_RULES §12）

凡例: motion は shotlist の値。**「意味のあるアニメ」列が今回の追加指定**。画像は必ず動かす。**実在人物は一切描かない**（象徴・一般化）。出典は判決/記録ベース。

| SPN | 章 | 種別 | テロップ(on_screen_text) | 意味のあるアニメ（指定） |
|---|---|---|---|---|
| 0001 | hook | 図解/graphic_anim | When does selling a dream become a crime? | 一滴の血が落ちる→波紋。**評価額グラフが $9B まで上昇→一気に $0 へ崩落**。雑誌表紙風モンタージュは**人物を出さず**シルエット/空白の表紙で象徴 |
| 0002 | opening | ai/ken_burns | Finale: one person vs. everyone | シリーズで反転したカメラを象徴。**矢印の向きが「国家→個人」から「個人→everyone」へ反転**。寄り＋微パララックス |
| 0003 | act1 | ai/ken_burns | 2003 — a Stanford dropout's startup | 年表が2003へ進む。**創業の象徴（無人のラボ/空席のデスク）**。実在人物なし |
| 0023 | act1 | ai/ken_burns | Prestige became a substitute for scrutiny | **「著名な肩書きカード」が積み上がり、その陰で“検証”の虫眼鏡が縮む**。権威が監視の代替になる対比 |
| 0004 | act1 | 実写/native | The Edison: hundreds of tests, one drop | 指先一滴 vs 採血針・バイアルの対比。**“Edison”は無地の黒い箱として象徴**（実機の写真は使わない） |
| 0005 | act1 | 図解/graphic_anim | ~$9 billion · prominent board · Walgreens (limited) | **評価額グラフが ~$9B へ上昇**＋**ロゴ壁（無名化した抽象ロゴ）**＋Walgreens は「限定」注記。実ロゴ商標は避け一般化 |
| 0006 | act1 | 実写/native | A story powerful enough to stop the questions | 「製品より物語」。落ち着いた寄り、問いが止む静けさ |
| 0007 | act2 | 図解/graphic_anim | 2015: The Wall Street Journal investigates | **年表が2015へ→調査報道のビート**。新聞名はテキストのみ（紙面画像/記者の顔は出さない） |
| 0008 | act2 | ai/ken_burns | Tests run on other companies' machines | **「自社の革新機」から“他社の市販機”へ矢印が差し替わる**暴露の演出。寄り＋微パララックス |
| 0009 | act2 | ai/ken_burns | — | 医療検査の重み。**誤った数値→誤った判断へ**の連鎖を抽象線で。静かな寄り |
| 0010 | act2 | 図解/graphic_anim | 2018: SEC fraud charge (settled, no admission); company dissolves | **年表が2018へ→SEC民事（“認否なし和解”を明記）→会社解散**。$9B が線で 0 へ。断定有罪表現を避ける |
| 0011 | act2 | 実写/native | Failure — or fraud? | **左右に "Failure" と "Fraud" を並置**し中央に問い。act3への橋渡し |
| 0012 | act3 | ai/ken_burns | Fraud = intent to deceive (not just failure) | **法定義カード「詐欺＝欺く意図（単なる失敗ではない）」**を組み上げる。天秤の象徴。長尺なので2バリアント切替 |
| 0024 | act3 | 実写/native | Prosecution: she knew. Defense: a true believer. | **左右対比（検察＝“知っていた” / 弁護＝“真の信奉者”）**のスプリットスクリーン。人物は出さず役割ラベルで |
| 0013 | act3 | **図解/graphic_anim** | 2022 — GUILTY: 4 counts (investor fraud) | **年表が2022/1/3へ→“count by count”の評決ボードが1件ずつ確定→投資家詐欺4件 GUILTY が金ラインで確定**（本話の山場グラフィック）。出典＝記録ベース |
| 0014 | act3 | ai/ken_burns | ACQUITTED: patient counts · NO VERDICT: 3 counts | **評決ボードの続き**：患者関連＝**ACQUITTED（無罪）**、3件＝**NO VERDICT（評決不成立）**を別色で明示。**「有罪」表記を絶対に出さない** |
| 0015 | act3 | 実写/native | Acquittal ≠ exoneration. Balwani: convicted on all 12. | **「無罪 ≠ 潔白」の注記カラム**＋Balwani は別裁判で全12件有罪（テキストで対比）。人物像は出さない |
| 0016 | act3 | ai/ken_burns | Sentenced: ~11 years, 3 months | **量刑の象徴**：時間（年月）が積み上がるカウンタ「~11y 3m」。法廷光の象徴。実在人物なし |
| 0017 | act4 | ai/ken_burns | "Fake it till you make it" — usually legal | **“Fake it till you make it”の標語が浮かび、多くは合法と注記**。スタートアップ behavior の一般化。軽ズーム |
| 0018 | act4 | 実写/native | The line: knowingly false + relied upon = fraud | **境界の等式「knowingly false ＋ relied upon ＝ fraud」が組み上がる**。本話の核（線＝境界線） |
| 0019 | act4 | ai/ken_burns | — | **「失敗したアプリ＝金の損失」vs「誤った血液検査＝診断の損失」の対比**で stakes を可視化。寄りで余白 |
| 0020 | ending | ai/ken_burns | One question, many costumes: where is the line? | **シリーズ総括**：1つの問いが衣装を替える（stop/arrest, identify/investigate, promise/lie の線が次々）。ゆっくり引き |
| 0021 | ending | 実写/native | — | 「線を引き直し続ける」総合。落ち着いた引き |
| 0022 | ending | ai/ken_burns | Subscribe — one line at a time | **CTA**：Subscribe ボタン演出＋「one line at a time」（1.6秒程度） |

> AI画像は1スパンに複数バリアントあり（`SPN-XXXX_02.png`等）。長いスパン（0012=45秒, 0015=43秒, 0002=40秒, 0020=36秒）は**約4.5秒ごとに別カット/別バリアントへ切替**し、静止・長居を避ける。importer が自動で複数取り込み。

---

## 3. テロップ／字幕／出典のレイアウト（被らせない＝VIDEO_RULES §13）

- **字幕（ナレ全文・forced alignment）**: 画面**下部の帯**。常時ナレと語単位同期。
- **テロップ（キーワード＝on_screen_text）**: **上/中央**。短く・大きく。字幕帯と**重ねない**。
- **出典（金ライン）**: 例 `United States v. Holmes (N.D. Cal.) — verdict Jan 3, 2022` / `SEC charges 2018 (settled, no admission)`。**右下など別ポジション**固定。字幕・テロップと別レイヤ・別位置。判決/記録ベースのみ。
- **AI画像には常時 `symbolic reconstruction` ラベル**（`CarpenterPremium` の `ReconLabel` を流用）。生成映像は記録ではない旨を画面で明示（不変項11）。
- 3者＋ラベルを同じ場所に重ねない（読めない/被るのは不可）。

## 4. 品質ゲート（書き出し前チェック＝motion-quality-gate）
- [ ] フック→オープニング→本編→エンディングの**4部**になっている
- [ ] `coded/cards = 0`（全ショット実素材 or 図解で埋まっている）
- [ ] 全ショットにモーション（静止画ゼロ）／Ken Burns 一辺倒でない
- [ ] 字幕・テロップ・出典が**位置で分離**し被っていない／AI画像に `symbolic reconstruction` ラベル
- [ ] 音4層＋**ダッキング**でナレ最優先（`06_audio/audio_cue_sheet.v001.md`）
- [ ] **R3表現チェック**：実在人物の肖像/実写/ディープフェイクなし・断定有罪なし・**患者関連は無罪/評決不成立であり「有罪」表記なし**・意図は陪審/裁判所に帰属
- [ ] **公開前 法務レビュー（R3）を実施・記録**（本書 §5 / EP15 は公開前に法務レビュー必須）
- [ ] 中立・台本/claims 不改変

## 5. この話の編集ポリシー（★R3・最重要）
- **中立**（「失敗 or 詐欺」の問いに肩入れしない）。検察主張・弁護主張・陪審の評決（有罪/無罪/評決不成立）を**公平**に提示。
- **実在人物（Holmes / Balwani 等）の肖像・実写・ディープフェイク不可**。象徴的・一般化した表現のみ。雑誌表紙・記者・実機・実ロゴは出さず抽象化。
- **断定的な有罪表現をしない**。投資家詐欺**4件の有罪は判決事実として提示**してよいが、患者関連＝**無罪**、3件＝**評決不成立**であり「有罪」と書かない。「無罪 ≠ 潔白」を明記。意図/認識は**陪審・裁判所に帰属**させ、ナレーター断定にしない。
- **事実は判決／公開記録ベース**（LLMを出典にしない）。数字（$9B・4件・約11年3か月・全12件）は単位・対象・期間を確認。
- **公開前に法務レビュー必須（R3）**。本動画は法務レビュー記録（exact revision/hash）なしに `publish_approved` へ進めない（CLAUDE.md §3 高リスク承認・§4 不変項2、`.claude/rules/16-approval-boundaries.md`）。
- 台本・claims を一切改変しない（Read専用）。claims 変更時は全依存を stale 化（不変項12）。

---

## 6. 実装方針＝Premium級コード演出（★重要・汎用RoughCutでは出ない）

§2 の「意味あるアニメ」は**汎用 `RoughCut` では描画されない**（RoughCutは Ken Burns＋動画＋テロップ＋グレイン止まり）。
→ EP15は**bespokeな `remotion/src/compositions/TheranosPremium.tsx` を新規作成**し、既存 `CarpenterPremium.tsx`（雛形）／`MadoffPremium.tsx`（金融詐欺・近題材）を参考にする。`RoughCut-theranos` は素材ステージング/下見用に残してよいが、**最終書き出しは `TheranosPremium`**。意味あるアニメはコード演出が主役、**DL済みファクトリ素材は加飾レイヤとして活かす**（§6末尾の加飾レイヤ参照・実在人物想起素材は不可）。

### 使う既存コード部品（再利用・新規実装を最小化／実在確認済み）
- `components/Motion.tsx`: `MovingStage`（カメラ＋粒子＋光）, `Particles`, `LightSweep`, `Vignette`, `CameraRig`。
- `components/Grain.tsx`: `Grain`（フィルムグレイン）。
- `components/Bookends.tsx`: `BrandOpening`（`seriesLabel`/`title`/`subtitle`）／`BrandEndcard`（固定エンドカード・`OPENING_SEC=3.5` / `ENDCARD_SEC=9`）。
- `components/SceneArt.tsx`: `SceneArt`（props=`visualMode`/`motifHint`/`onScreenText`/`seed`）で **小槌(gavel)/天秤(scales)/年表(timeline)/USマップ(map)/書類＋印章(document)/法廷(courtroom)/取調室ランプ(room)** を自動選択（`pickArt`）。
- `CarpenterPremium.tsx` の流用可能なビズ（同ファイル内 export 前提でコピー/移植）：`Vote`(5–4票・**本話は使わず代わりに評決ボードへ改変**)、`MapGrid`、`TwoColumn`(左右対比)、`Doors`(アイコン/ラベル列)、`BigNumber`、`CourtColumns`、`Boundary`(境界線)、`Triptych`、`SceneShell`(多画像Ken Burns＋光＋粒子＋`ReconLabel`＋`Lower`)。

### ショット→実装の割り当て（§2の演出をコードに対応）
| SPN | 演出（§2） | 実装（部品） |
|---|---|---|
| 0001 | 一滴の血＋$9B→$0崩落グラフ | 手組み**ValuationGraph**（上昇→崩落・新規小コンポ）＋`Particles`。雑誌表紙は人物なしの抽象板 |
| 0002 | 矢印が「国家→個人」へ反転 | AI画像＋`MovingStage`＋手組み矢印（反転） |
| 0003 | 2003年表・創業の象徴 | `SceneArt visualMode="timeline"`（2003マーカー）＋AI画像（無人ラボ） |
| 0023 | 権威カードが積み“検証”が縮む | `Doors`（著名肩書きラベル列）＋手組み虫眼鏡縮小 |
| 0004 | 一滴 vs 採血針・黒い箱 | `<Video>`（ストック）＋`Vignette`/`Grain`。Edison は無地黒箱の手組み |
| 0005 | ~$9B 上昇＋ロゴ壁＋Walgreens限定 | **ValuationGraph**（~$9Bへ）＋`Doors`（抽象ロゴ壁）＋注記 |
| 0006 | 物語が問いを止める | `<Video>`＋`Vignette`/`Grain` |
| 0007 | 2015 調査報道 | `SceneArt visualMode="timeline"`（2015マーカー）。新聞名はテキストのみ |
| 0008 | 自社機→他社市販機へ差替 | AI画像＋`TwoColumn`(left="own device" / right="others' machines")＋差替アニメ |
| 0009 | 誤数値→誤判断の連鎖 | AI画像＋`SceneShell`相当（多画像Ken Burns）＋細線アニメ |
| 0010 | 2018 SEC和解→解散・$9B→0 | `SceneArt visualMode="timeline"`（2018）＋**ValuationGraph**（0へ）＋“no admission”注記 |
| 0011 | Failure vs Fraud 並置 | `<Video>`＋`TwoColumn`(left="Failure" / right="Fraud") |
| 0012 | 法定義「詐欺＝欺く意図」 | `SceneArt motifHint="scales"`（天秤）＋手組み定義カード |
| 0024 | 検察 vs 弁護の二分 | `<Video>`＋`TwoColumn`(left="Prosecution: she knew" / right="Defense: true believer") |
| 0013 | **2022→count by count 評決ボード（山場）** | `SceneArt visualMode="timeline"`（2022/1/3）＋**VerdictBoard**（`Vote` を改変：4件 GUILTY を1件ずつ確定）＋`SceneArt motifHint="document"`（記録確定）。`LightSweep`色=GOLD |
| 0014 | 患者=無罪・3件=評決なし | **VerdictBoard** 続き（ACQUITTED/NO VERDICT を別色・**GUILTY表記なし**）＋AI画像 |
| 0015 | 無罪≠潔白／Balwani全12件 | `<Video>`＋`TwoColumn`(left="Acquittal ≠ exoneration" / right="Balwani: all 12") |
| 0016 | 量刑 約11年3か月 | AI画像＋`BigNumber`(top="~11y 3m" bottom="sentenced")＋`SceneArt motifHint="court"`光 |
| 0017 | “Fake it till you make it”標語 | AI画像＋手組みタイポ＋注記「usually legal」 |
| 0018 | 境界の等式 | 手組み等式（knowingly false ＋ relied upon ＝ fraud）／`Boundary`（線） |
| 0019 | アプリ損失 vs 検査の損失 | AI画像＋`TwoColumn`(left="a failed app: money" / right="a wrong test: a diagnosis") |
| 0020 | シリーズ総括「many costumes」 | AI画像＋`Triptych`相当（stop/arrest・identify/investigate・promise/lie の線） |
| 0021 | 線を引き直し続ける | `<Video>`＋`Vignette`/`Grain` |
| 0022 | CTA Subscribe | 手組みSubscribeボタン＋`soft_impact`（`BrandEndcard` 直前） |
| その他のai_image | 寄り/引き＋微パララックス | `SceneShell`相当（多画像Ken Burns＋`Particles`/`Vignette`/`Grain`＋`ReconLabel`） |
| stock_video | 実写再生 | `<Video>`＋`Vignette`/`Grain` |

> **VerdictBoard / ValuationGraph は新規小コンポ**（`Vote` と `BigNumber` を改変・流用）。実在人物を描かない・断定有罪表記を避けるための専用ビズ。SVG/CSS・$0。

### 実装ステップ
1. `TheranosPremium.tsx` を作成（`scenes[]` に24スパン＋hook/opening/ending を `kind` 付きで定義。**章順は §1 の注記どおり台本順に並べる**。AI画像は `remotion/public/theranos/SPN-XXXX*.png` を参照）。
2. `Root.tsx` に `TheranosPremium`（`id="TheranosPremium"`・ハイフンのみ）を `<Composition>` 登録（`MadoffPremium` 等と同形・`durationInFrames={theranosPremiumDurationInFrames(BRAND.video.fps)}`）。`THERANOS_ROUGHCUT` のRoughCut登録は残してよい。
3. `npm run studio` で `TheranosPremium` を確認 → §2の各演出が出ているか／4部構成か／**R3表現チェック（§4）**をチェック。
4. 書き出しは `TheranosPremium`（quality-first CPU/libx264）。**公開前に法務レビュー（§5）を通すまで `publish_approved` に進めない。**

> **加飾レイヤ（VIDEO_RULES §4/§12）＝DL済みファクトリ素材を活かす**: `assets/asset_manifest.v001.json`（商用OK・DL済み）から**トーンの合うものだけ**を `scripts/select_factory_assets.py` で選び `remotion/public/theranos/factory/` へコピー → `TheranosPremium` に **背景プレート(下地)＋light/particle/vfxオーバーレイ(screen/add)＋texture(overlay)** の3層で重ね、奥行きと光で美しくダイナミックに。**意味あるアニメはコード演出が主役・factoryは加飾**（過剰にしない・合わない素材は使わない・licenseはallowedのみ）。**実在人物を想起させる素材は使わない（R3）。** 映画的カメラ＝`MovingStage`/`CameraRig`。
