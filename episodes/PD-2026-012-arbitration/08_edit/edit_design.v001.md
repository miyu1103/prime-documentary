# 第12話 arbitration 仕上げ設計書（Edit / Finish Design） v001

対象: `PD-2026-012-arbitration`（AT&T Mobility v. Concepcion 2011 / Epic Systems v. Lewis 2018 / 強制仲裁条項＋集団訴訟放棄）。Codex がこの設計に従ってラフカット→仕上げを行う。
タイトル: 「The Fine Print That Took Away Your Right to Sue」。
入力: `04_scenes/shotlist.v001.json`（25ショット・610.4秒≒10.2分）, `03_script/script.en.v001.md`（`[VO:]`=ナレ本文・**変更禁止**）, `04_scenes/asset_map.v001.md`, AI画像 `H:\pd-media\assets\ai\arbitration\SPN-XXXX*.png`（生成済み前提）, サムネ `H:\pd-media\assets\ai\thumbs\arbitration\THUMB-01..06.png`（生成済み前提）。
準拠: `episodes/_planning/VIDEO_RULES.md` §10〜13 / `docs/motion-design-language.md` / `docs/motion-quality-gate.md`。
**中立厳守**: これは本物の政策論争。critics（「forced arbitration＝裁判所の扉を閉じる」）と defenders（「速く・安く・合意済み」）を**公平**に提示。中立語は「mandatory / pre-dispute arbitration」。実在判事の肖像は出さない。

---

## 1. 完成尺と4部構成（VIDEO_RULES §10 厳守）

| 部 | 構成 | ソース | 目安 |
|---|---|---|---|
| **① フック** | 本編の“盛り上がり”約10カット（各1〜2秒）の高速ハイライト集＋煽り音 | 本編映像/ナレ断片の流用（新規制作しない） | 約20〜30秒 |
| **② オープニング** | 既存ブランドオープニング（`BrandOpening`／`Bookends.tsx`） | 既存・作り直さない | 約3.5秒 |
| **③ 本編** | act1〜act4（SPN-0003〜SPN-0019,0023〜0025） | shotlist 各ショット | 約9.0分 |
| **④ エンディング** | 結末＋シリーズ統合＋次回予告（DNA採取）（SPN-0020〜0022） | shotlist ending | 約65秒 |

**フックに使う本編ハイライト候補（priority A 優先・各1〜2秒で速いカット）**:
SPN-0001(「I agree」を押す指＋スクロールする細字) / SPN-0002(arbitration条項＋集団訴訟放棄) / SPN-0013(2011・5–4・563 U.S. 333 のグラフィック) / SPN-0024(Ginsburg反対意見を法廷で読み上げ) / SPN-0015(Breyer反対意見「唯一の現実的救済か？」) / SPN-0016(2018 Epic Systems＝あなたの仕事にも拡張) / SPN-0019(声高に取られたのではなく“自分で手放した”) / SPN-0014(Scalia多数意見) / SPN-0021(シリーズ統合＝search/track/take/police speech) / SPN-0022(次回への引き＝DNA)。
→ ナレの決め所断片（「$30 → law of the land」「two basic rights」）を1〜2個だけ被せ、最後は無音ぎみ→オープニングへブリッジ。**台本テキストは変えない**。

---

## 2. 全ショット モーション設計（Ken Burns 一辺倒にしない＝VIDEO_RULES §12）

凡例: motion は shotlist の値。**「意味のあるアニメ」列が今回の追加指定**。画像/動画は必ず動かす。論点（仲裁＝個別・1人ずつ／集団訴訟＝束ねる／放棄＝扉が閉じる）を演出に落とす。

| SPN | 章 | 種別 | テロップ(on_screen_text) | 意味のあるアニメ（指定） |
|---|---|---|---|---|
| 0001 | hook | 実写/native | "I agree" — to what? | 「I Agree」を押す指へ寄り、**細字の利用規約が下へ無限スクロール**。最後の一語に色が灯る |
| 0002 | opening | ai/ken_burns | Arbitration clause + class-action waiver | 契約書面に寄り、**"arbitration clause" と "class-action waiver" の2語を順に下線＋ハイライト**で確定 |
| 0003 | act1 | ai/ken_burns | "Free" phones — ~$30 in tax | 「FREE」表示の携帯に寄り、**請求書に "+$30 tax" が打刻される**（皮肉のビート） |
| 0004 | act1 | 実写/native | $30 × millions = real money | **「$30」が1個→群衆ぶんに増殖して "tens of millions" へカウントアップ**。小被害が巨額化する核心 |
| 0005 | act1 | 実写/native | Class action = many small claims, bundled | **散らばった小さな点が1束に集まる**（束ねる＝集団訴訟）モーション |
| 0006 | act1 | ai/ken_burns | CA 'Discover Bank' rule: waiver unenforceable | 州法カードを左に提示。**"unenforceable" に光のスタンプ**（カリフォルニア＝放棄無効） |
| 0007 | act1 | ai/ken_burns | — | 連邦法へ橋渡し。寄り＋微パララックス（古い1925法の予感） |
| 0008 | act2 | 実写/native | — | 「2つのこと」導入。落ち着いた寄り（短尺6.8s） |
| 0009 | act2 | **図解/graphic_anim** | Federal Arbitration Act — 1925 | **年表が1925へ進む→FAAの条文カードが点灯**。長く静かに眠っていた法、を線で示す |
| 0010 | act2 | ai/ken_burns | The waiver: one person at a time | **多数の人型が1人ずつに切り離される**（"one at a time"＝束を解く逆モーション） |
| 0011 | act2 | ai/ken_burns | Critics: closes the courthouse door | **裁判所の扉が静かに閉まる**（critics の主張）。やや暗いトーン。中立のため次0012と対 |
| 0012 | act2 | 実写/native | Defenders: faster, cheaper, agreed-to | defenders カードを右に。**0011と左右対比**（速い/安い/合意済み）。同じ尺感で公平に |
| 0023 | act2 | 実写/native | You 'agree' just by using it | **起動/開封/クリック/出勤の4アイコンが順に点灯**＝"使うだけで同意"。take-it-or-leave-it |
| 0013 | act3 | **図解/graphic_anim** | 2011 — 5–4 ／ AT&T Mobility v. Concepcion, 563 U.S. 333 | **年表が2011へ→5–4の票が並ぶ→出典 563 U.S. 333 が金ラインで確定**（本話の山場①） |
| 0014 | act3 | ai/ken_burns | — | Scalia多数意見。**「州法が連邦の仲裁政策の障害」→州法に取り消し線**（多数意見の理路） |
| 0015 | act3 | ai/ken_burns | Dissent (Breyer): the only realistic remedy? | Breyer反対意見。**疑問符を中央に**＋「数ドルの請求＝集団訴訟が唯一の現実的救済」を注記カラム |
| 0016 | act3 | **図解/graphic_anim** | 2018: Epic Systems extends it to your job | **年表が2018へ→「phone」アイコンから「job」アイコンへ矢印が伸びる**（5–4・Gorsuch・労働法も適用外）山場② |
| 0024 | act3 | ai/ken_burns | Dissent (Ginsburg) — read from the bench | Ginsburg反対意見。**法廷から読み上げ＝強い反対の象徴**。マイク/演壇の光、声の波形を象徴的に |
| 0017 | act4 | 実写/native | — | 影響の総括。落ち着いた寄り（phone/bank/streaming/job が日常に） |
| 0018 | act4 | ai/ken_burns | The debate is real. The mechanism is not. | **左（debate＝揺れる天秤）と右（mechanism＝固定された印章）を対置**。論争は本物・仕組みは確定、を視覚化 |
| 0025 | act4 | ai/ken_burns | — | 「実際できることは少ない／だが議論は続く」。引き＋微移動、余白 |
| 0019 | act4 | ai/ken_burns | — | **本話の決め所**：声高に取られたのではなく“自分で手放した”。ボタンを押す手へ非常にゆっくり押す、静寂 |
| 0020 | ending | 実写/native | — | 結末「$30が最も静かで広い線を引いた」。落ち着いた寄り |
| 0021 | ending | ai/ken_burns | — | **シリーズ統合**：search→track→take→police speech の4語が順に並び、最後に "by contract" が加わる |
| 0022 | ending | ai/ken_burns | Next: can they take your DNA? | **次回予告**。引き＋タイトル示唆のタイポ（DNA／逮捕時の採取） |

> AI画像は1スパンに複数バリアントあり（`SPN-XXXX_02.png`等）。長いスパン（0010,0012,0016,0023等の20s超）は**約4.5秒ごとに別カット/別バリアントへ切替**し、静止・長居を避ける。importer が自動で複数取り込み。
> エンドカード（`BrandEndcard`＝Subscribe）は固定ブランド演出。本話のエンディング（0020〜0022）の後に既存エンドカードを連結する（作り直さない）。

---

## 3. テロップ／字幕／出典のレイアウト（被らせない＝VIDEO_RULES §13）

- **字幕（ナレ全文・forced alignment）**: 画面**下部の帯**。常時ナレと語単位同期。
- **テロップ（キーワード＝on_screen_text）**: **上/中央**。短く・大きく。字幕帯と**重ねない**。
- **出典（金ライン）**: 例 `AT&T Mobility v. Concepcion, 563 U.S. 333 (2011)`。**右下など別ポジション**固定。字幕・テロップと別レイヤ・別位置。
- 3者を同じ場所に重ねない（読めない/被るのは不可）。

## 4. 品質ゲート（書き出し前チェック＝motion-quality-gate）
- [ ] フック→オープニング→本編→エンディングの**4部**になっている
- [ ] `coded/cards = 0`（全ショット実素材 or 図解で埋まっている）
- [ ] 全ショットにモーション（静止画ゼロ）／Ken Burns 一辺倒でない
- [ ] 字幕・テロップ・出典が**位置で分離**し被っていない
- [ ] 音4層＋**ダッキング**でナレ最優先（`06_audio/audio_cue_sheet.v001.md`）
- [ ] 中立・実在人物の肖像なし・台本/claims 不改変
- [ ] critics と defenders を**同程度の尺・トーン**で提示（0011/0012, 0015/0024 が一方に偏らない）

## 5. この話の編集ポリシー
- **中立**（mandatory arbitration の是非に肩入れしない）。critics（裁判所の扉が閉じる／小被害に救済なし）と defenders（速い・安い・合意の尊重）を**公平**に提示。Concepcion多数意見（Scalia）・反対意見（Breyer）、Epic多数意見（Gorsuch）・反対意見（Ginsburg）を**公平**に。
- 経験的論点（コスト・速度・結果）は**決着していない**ものとして扱う（台本どおり、どちらの主張も断定しない）。
- 「forced arbitration」は**critics の語**として帰属表示し、地の文は中立語（mandatory / pre-dispute arbitration）。
- **実在人物・判事の肖像なし**（象徴的に）。ディープフェイク不可。台本・claims 不改変。

---

## 6. 実装方針＝Premium級コード演出（★重要・汎用RoughCutでは出ない）

§2 の「意味あるアニメ」は**汎用 `RoughCut` では描画されない**（RoughCutは Ken Burns＋動画＋テロップ＋グレイン止まり）。
→ EP12は**bespokeな `remotion/src/compositions/ArbitrationPremium.tsx` を新規作成**し、既存 `CarpenterPremium.tsx`（雛形）／`MadoffPremium.tsx`／`MappPremium.tsx`／`GideonPremium.tsx` を参考にする。`RoughCut-arbitration`（`Root.tsx` に登録済み・`data/arbitration_roughcut.ts`）は素材ステージング/下見用に残してよいが、**最終書き出しは `ArbitrationPremium`**。

### 使う既存コード部品（再利用・新規実装を最小化）
- `components/Motion.tsx`: `MovingStage`（カメラ＋粒子＋光）, `Particles`, `LightSweep`, `Vignette`, `CameraRig`。
- `components/Grain.tsx`: `Grain`（フィルムグレイン）。
- `components/Bookends.tsx`: `BrandOpening` / `BrandEndcard`（`OPENING_SEC`=3.5 / `ENDCARD_SEC`=9）。
- `components/SceneArt.tsx`: `SceneArt`（`visualMode`/`motifHint`/`onScreenText`/`seed` で **小槌(gavel)/天秤(scales)/年表(timeline)/USマップ(map)/書類＋印章(document/seal)/法廷光(courtroom)/取調室ランプ(room)** を自動選択。motifHint文字列で分岐：`gavel`/`scales|justice`/`document|seal|constitution`/`court`、visualMode=`timeline`/`map` 等）。
- `CarpenterPremium.tsx` の流用可能なビズ：`Vote`(5–4票)、`MapGrid`、`TwoColumn`(左右対比)、`Doors`(アイコン列)、`BigNumber`、`CourtColumns`、`Boundary`、`Triptych`、`SceneShell`（多画像Ken Burns＋光＋粒子＋`Lower`テロップ＋出典＋`Vignette`＋`Grain` を内包）。

### ショット→実装の割り当て（§2の演出をコードに対応）
| SPN | 演出（§2） | 実装（部品） |
|---|---|---|
| 0001 | 「I agree」へ寄り＋細字スクロール | `<Video>`（実写）＋`Vignette`/`Grain`＋手組みスクロールテキスト |
| 0002 | "arbitration clause"/"waiver" 2語を下線確定 | AI画像＋タイポ下線（`Lower`系の手組み・2段階ハイライト） |
| 0003 | 「FREE」携帯に "+$30 tax" 打刻 | AI画像＋手組みスタンプ（`stamp_seal`同期）＋`SceneShell` |
| 0004 | $30が群衆ぶんに増殖→カウントアップ | `BigNumber`("$30"→"tens of millions") カウントアップ＋`<Video>` |
| 0005 | 散らばる点が1束に集まる | 手組みSVG（点→束）または `Doors` の逆＝集約モーション |
| 0006 | Discover Bank 州法カード＋"unenforceable"印 | `TwoColumn`(left=CA rule / right=waiver) ＋ `SceneArt motifHint="seal"`（印章） |
| 0009 | **年表→1925→FAAカード点灯** | `SceneArt visualMode="timeline"`（年表マーカー）＋ FAAカード手組み |
| 0010 | 多数の人型が1人ずつ切り離される | `Doors` ラベル分割 or 手組み（束→個）逆アニメ |
| 0011/0012 | critics（扉が閉じる）vs defenders（速い/安い） | `TwoColumn`(left=Critics / right=Defenders)。0011=扉クローズSVG、0012=`<Video>` |
| 0023 | 4アイコン（起動/開封/クリック/出勤）点灯 | `Doors`(activate/open/click/show-up) 順次フェード＋`<Video>` |
| 0013 | **年表→2011→5–4→出典563 U.S.333確定（山場①）** | `SceneArt motifHint="timeline"`＋`Vote`(5–4)＋`SceneArt motifHint="seal"`（書類＋印章で 563 U.S. 333）。`LightSweep`色=GOLD |
| 0014 | Scalia多数意見→州法に取り消し線 | `SceneArt motifHint="gavel"` or AI画像＋取り消し線アニメ（手組み・`whoosh_short`同期） |
| 0015 | Breyer反対意見＝疑問符＋注記カラム | AI画像＋大疑問符タイポ＋手組み注記カラム（"only realistic remedy?"） |
| 0016 | **年表→2018→phone→job 矢印（山場②）** | `SceneArt motifHint="timeline"`（2018へ）＋`TwoColumn`(left=phone / right=job)＋矢印手組み |
| 0024 | Ginsburg反対意見＝法廷から読み上げ | `SceneArt motifHint="court"`（法廷光）＋演壇/声の波形を象徴（実在肖像なし） |
| 0018 | debate(天秤) vs mechanism(印章) 対置 | `SceneArt motifHint="scales"`（左・揺れる天秤）＋`SceneArt motifHint="seal"`（右・固定印章）2分割 |
| 0019 | **決め所**：ボタンを押す手へ静かに押す | AI画像＋`CameraRig`（超低速push-in）＋`Particles`抑えめ |
| 0021 | シリーズ統合 search→track→take→speech＋"by contract" | `Doors`/手組み4語シーケンス＋最終語追加 |
| 0022 | 次回予告（DNA） | AI画像＋引き＋タイトル示唆タイポ（"Next: can they take your DNA?"） |
| その他のai_image (0007,0020,0025) | 寄り/引き＋微パララックス | `SceneShell`相当（多画像Ken Burns＋`Particles`/`Vignette`/`Grain`） |
| stock_video (0008,0017,0020) | 実写再生 | `<Video>`＋`Vignette`/`Grain` |

### 実装ステップ
1. `ArbitrationPremium.tsx` を作成（`scenes[]` に25スパン＋hook/opening/ending を `kind` 付きで定義。`CarpenterPremium` の `Scene`/`SceneShell`/`SceneContent` 構造を踏襲。AI画像は `remotion/public/arbitration/SPN-XXXX*.png` を参照、実写は `remotion/public/arbitration/*.mp4`）。出典は `Scene.citation` に格納（例 `563 U.S. 333`）。
2. `Root.tsx` に `ArbitrationPremium`（`id="ArbitrationPremium"`・ハイフン無しのキャメル）を `<Composition>` 登録。`import {ArbitrationPremium, arbitrationPremiumDurationInFrames} from './compositions/ArbitrationPremium';` を追加し、`durationInFrames={arbitrationPremiumDurationInFrames(BRAND.video.fps)}`。GideonPremium/MadoffPremium の登録ブロックと同形。
3. `npm run studio` で `ArbitrationPremium` を確認 → §2の各演出が出ているか／4部構成か／critics・defenders が公平かをチェック。
4. 書き出しは `ArbitrationPremium`（quality-first・CPU/libx264）。

> **加飾レイヤ（VIDEO_RULES §4/§12）＝DL済みファクトリ素材を活かす**: `assets/asset_manifest.v001.json`（商用OK・DL済み）から**トーンの合うものだけ**を `scripts/select_factory_assets.py` で選び `remotion/public/arbitration/factory/` へコピー → `ArbitrationPremium` に **背景プレート(下地)＋light/particle/vfxオーバーレイ(screen/add)＋texture(overlay)** の3層で重ね、奥行きと光で美しくダイナミックに。**意味あるアニメはコード演出が主役・factoryは加飾**（過剰にしない・合わない素材は使わない・licenseはallowedのみ）。映画的カメラ＝`MovingStage`/`CameraRig` で全カットに寄り引き/パララックス＋イージング。
> 注意：`CarpenterPremium` 内の `ReconLabel`（"symbolic reconstruction"）は AI画像/図解スパンにのみ付け、実写stockスパンには付けない（実写を「象徴的再現」と誤表示しない＝invariant 11）。
